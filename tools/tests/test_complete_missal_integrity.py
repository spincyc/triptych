#!/usr/bin/env python3
"""Bounded integrity gates for the composed Missal command surface.

The opt-in complete-year gate owns exhaustive date coverage.  This module uses
one ordinary Sunday instead: it is small enough for the ordinary test run while
still crossing all three calendars, both requested languages, the Propers, and
the Ordinary.  Expectations are structural and source-derived; filling a gap or
adding a Mass must not require editing a count snapshot here.
"""

from __future__ import annotations

import collections
import hashlib
import json
import subprocess
import sys
import tempfile
import time
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from _parallel import gather  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]
TPT = ROOT / "tools" / "tpt"

CALENDARS = ("postconciliar", "roman-1962", "roman-pre-1955")
LANGUAGES = ("en", "la")
REPRESENTATIVE_DATE = "2026-11-29"
COMMAND_TIMEOUT_SECONDS = 30
MATRIX_BUDGET_SECONDS = 75


def run_tpt(*arguments: str) -> subprocess.CompletedProcess[str]:
    """Run only through the registered launcher, with a hard per-call bound."""

    return subprocess.run(
        [str(TPT), *arguments],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
        timeout=COMMAND_TIMEOUT_SECONDS,
    )


def duplicate_values(values: list[str]) -> list[str]:
    return sorted(value for value, count in collections.Counter(values).items() if count > 1)


def command_summary(finished: subprocess.CompletedProcess[str]) -> str:
    """Describe a failure without echoing a complete liturgical payload."""

    stream = finished.stderr or finished.stdout
    try:
        payload = json.loads(stream)
    except json.JSONDecodeError:
        return json.dumps(
            {
                "returncode": finished.returncode,
                "stdout_bytes": len(finished.stdout.encode("utf-8")),
                "stderr_bytes": len(finished.stderr.encode("utf-8")),
            },
            sort_keys=True,
        )
    problems = []
    for problem in payload.get("problems", []):
        if not isinstance(problem, dict):
            continue
        problems.append(
            {
                "component": problem.get("component"),
                "error": str(problem.get("error") or "")[:300],
            }
        )
    return json.dumps(
        {
            "returncode": finished.returncode,
            "status": payload.get("status"),
            "code": payload.get("code"),
            "error": str(payload.get("error") or "")[:300],
            "problems": problems,
        },
        ensure_ascii=False,
        sort_keys=True,
    )


def output_digest(output: str) -> str:
    return hashlib.sha256(output.encode("utf-8")).hexdigest()


class CompleteMissalDeterminismTests(unittest.TestCase):
    def assert_unique_ids(self, values: list[object], where: str) -> None:
        rendered = [str(value or "") for value in values]
        self.assertTrue(all(rendered), f"{where} includes an empty ID")
        self.assertEqual(duplicate_values(rendered), [], f"duplicate IDs in {where}")

    def assert_ordinary_ids(self, ordinary: object, calendar: str) -> None:
        self.assertIsInstance(ordinary, dict)
        assert isinstance(ordinary, dict)
        self.assertEqual(ordinary.get("schema"), "triptych-ordinary-structure/v1")
        self.assertEqual(ordinary.get("calendar"), calendar)

        sections = ordinary.get("sections")
        self.assertIsInstance(sections, list)
        assert isinstance(sections, list)
        self.assertTrue(sections)
        self.assertTrue(all(isinstance(section, dict) for section in sections))
        self.assert_unique_ids(
            [section.get("key") for section in sections],
            f"{calendar} Ordinary sections",
        )

        elements = []
        for section in sections:
            section_elements = section.get("elements")
            self.assertIsInstance(section_elements, list)
            assert isinstance(section_elements, list)
            self.assertTrue(all(isinstance(element, dict) for element in section_elements))
            elements.extend(section_elements)
        self.assertTrue(elements)
        self.assert_unique_ids(
            [element.get("key") for element in elements],
            f"{calendar} Ordinary elements",
        )

        slots = ordinary.get("slots")
        self.assertIsInstance(slots, list)
        assert isinstance(slots, list)
        self.assertTrue(all(isinstance(slot, dict) for slot in slots))
        self.assert_unique_ids(
            [slot.get("key") for slot in slots],
            f"{calendar} Ordinary slots",
        )

        variants = ordinary.get("variants")
        self.assertIsInstance(variants, list)
        assert isinstance(variants, list)
        self.assertTrue(all(isinstance(variant, dict) for variant in variants))
        self.assert_unique_ids(
            [variant.get("group") for variant in variants],
            f"{calendar} Ordinary variant groups",
        )
        for variant in variants:
            options = variant.get("options")
            self.assertIsInstance(options, list)
            assert isinstance(options, list)
            self.assertTrue(all(isinstance(option, dict) for option in options))
            self.assert_unique_ids(
                [option.get("id") for option in options],
                f"{calendar} Ordinary variant {variant.get('group')}",
            )

    def test_representative_matrix_is_deterministic_and_bounded(self) -> None:
        """Six coordinates run twice; the exhaustive year remains opt-in."""

        started = time.monotonic()
        coordinates = [
            (calendar, language) for calendar in CALENDARS for language in LANGUAGES
        ]

        def command_for(calendar: str, language: str) -> tuple[str, ...]:
            return (
                "mass-today",
                "show",
                "--date",
                REPRESENTATIVE_DATE,
                "--calendar",
                calendar,
                "--lang",
                language,
                "--ordinary",
                "--json",
            )

        # Twelve cold `mass-today` runs --- six coordinates, each run twice to
        # prove the bytes repeat --- and no coordinate depends on another, so
        # the waiting is shared. Both runs of a pair are still two separate
        # processes over the same inputs, which is the whole of what the
        # determinism claim needs; overlapping them exercises it under a
        # different schedule rather than a weaker one.
        outcomes = gather(
            lambda pair: (run_tpt(*command_for(*pair)), run_tpt(*command_for(*pair))),
            coordinates,
        )

        for (calendar, language), (first, second) in zip(coordinates, outcomes):
            with self.subTest(calendar=calendar, language=language):
                    command = command_for(calendar, language)
                    self.assertEqual(first.returncode, 0, command_summary(first))
                    self.assertEqual(second.returncode, 0, command_summary(second))
                    self.assertEqual(first.stderr, "")
                    self.assertEqual(second.stderr, "")
                    self.assertTrue(
                        first.stdout == second.stdout,
                        "repeat output bytes differ: "
                        f"{output_digest(first.stdout)} != {output_digest(second.stdout)}",
                    )

                    payload = json.loads(first.stdout)
                    self.assertEqual(payload.get("v"), 1)
                    self.assertEqual(payload.get("status"), "ok")
                    self.assertEqual(payload.get("problems"), [])
                    self.assertEqual(payload.get("date"), REPRESENTATIVE_DATE)
                    self.assertEqual(len(payload.get("days", [])), 1)
                    day = payload["days"][0]
                    self.assertEqual(day.get("calendar"), calendar)
                    masses = day.get("masses")
                    self.assertIsInstance(masses, list)
                    assert isinstance(masses, list)
                    self.assertTrue(all(isinstance(mass, dict) for mass in masses))
                    self.assert_unique_ids(
                        [mass.get("key") for mass in masses],
                        f"{calendar}/{language} appointed masses",
                    )
                    self.assert_ordinary_ids(day.get("ordinary"), calendar)

        elapsed = time.monotonic() - started
        self.assertLess(
            elapsed,
            MATRIX_BUDGET_SECONDS,
            f"six-cell deterministic matrix took {elapsed:.2f}s",
        )

    def test_complete_mass_catalog_ids_are_unique(self) -> None:
        """Derive the current catalog and reject duplicate key or registry IDs."""

        for calendar in CALENDARS:
            with self.subTest(calendar=calendar):
                finished = run_tpt(
                    "mass-propers", "list", "--calendar", calendar, "--json"
                )
                self.assertEqual(finished.returncode, 0, command_summary(finished))
                self.assertEqual(finished.stderr, "")
                payload = json.loads(finished.stdout)
                self.assertEqual(payload.get("v"), 1)
                calendars = payload.get("calendars")
                self.assertIsInstance(calendars, dict)
                assert isinstance(calendars, dict)
                self.assertEqual(set(calendars), {calendar})
                rows = calendars[calendar]
                self.assertIsInstance(rows, list)
                self.assertTrue(rows)
                self.assertTrue(all(isinstance(row, dict) for row in rows))
                self.assert_unique_ids(
                    [row.get("key") for row in rows],
                    f"{calendar} mass keys",
                )
                self.assert_unique_ids(
                    [row.get("registry") for row in rows],
                    f"{calendar} registry IDs",
                )


class CompleteMissalRefusalTests(unittest.TestCase):
    FIXTURE_HEAD = """\
schema: triptych-calendar-masses/v1
edition: test edition
calendar: test
series: test series
ordering: test ordering
registry: test registry
psalm_numbering: vulgate
citation_convention: test convention
orthography: test orthography
verification: unverified test fixture
sections:
  seasonal:
    kind: seasonal
    label: Seasonal
    masses:
"""

    def check_fixture(self, rows: str) -> subprocess.CompletedProcess[str]:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / "calendars"
            path = root / "test" / "propers.yaml"
            path.parent.mkdir(parents=True)
            path.write_text(self.FIXTURE_HEAD + rows, encoding="utf-8")
            return run_tpt(
                "check-calendar-masses",
                "--root",
                str(root),
                "--calendar",
                "test",
                "--json",
            )

    def test_validator_rejects_duplicate_mass_and_registry_ids(self) -> None:
        base = """\
    - key: {first_key}
      name: First
      registry: "{first_registry}"
      season: test
      propers:
      - {{name: Collect, source: composed, text: First.}}
    - key: {second_key}
      name: Second
      registry: "{second_registry}"
      season: test
      propers:
      - {{name: Collect, source: composed, text: Second.}}
"""
        cases = (
            (
                "mass key",
                base.format(
                    first_key="repeated",
                    second_key="repeated",
                    first_registry="01",
                    second_registry="02",
                ),
                "duplicate mass keys: repeated",
            ),
            (
                "registry ID",
                base.format(
                    first_key="first",
                    second_key="second",
                    first_registry="01",
                    second_registry="01",
                ),
                "duplicate registry IDs: 01",
            ),
        )
        for label, rows, expected in cases:
            with self.subTest(label=label):
                finished = self.check_fixture(rows)
                self.assertEqual(finished.returncode, 1, finished.stdout)
                self.assertEqual(finished.stderr, "")
                payload = json.loads(finished.stdout)
                self.assertEqual(payload.get("v"), 1)
                self.assertEqual(payload.get("status"), "error")
                self.assertTrue(
                    any(expected in problem for problem in payload.get("problems", [])),
                    payload,
                )

    def test_validator_rejects_duplicate_normalized_chant_in_one_slot(self) -> None:
        """An I/J or presentation-label variation cannot mint an occurrence."""

        common = """\
    - key: advent-1
      name: First Sunday of Advent
      registry: "01"
      season: advent
      propers:
      - name: Alleluia (Tempore paschali)
        incipit: Virga {first_spelling} floruit
        source: composed
        text: >-
          Alleluia, alleluia. V. Virga {first_spelling} floruit: Virgo Deum et
          hominem genuit: pacem Deus reddidit, in se reconcilians ima summis.
      - name: Alleluia (Tempore paschali)
        incipit: Virga {second_spelling} floruit
        source: composed
        text: >-
          Alleluia, alleluia. V. Virga {second_body_spelling} floruit: Virgo Deum et
          hominem genuit: pacem Deus reddidit, in se reconcilians ima summis.
"""
        cases = (
            (
                "byte-equivalent body behind I/J incipit metadata",
                common.format(
                    first_spelling="Iesse",
                    second_spelling="Jesse",
                    second_body_spelling="Iesse",
                ),
            ),
            (
                "canonically equivalent I/J body",
                common.format(
                    first_spelling="Iesse",
                    second_spelling="Jesse",
                    second_body_spelling="Jesse",
                ),
            ),
            (
                "NFC case whitespace and punctuation presentation",
                """\
    - key: advent-1
      name: First Sunday of Advent
      registry: "01"
      season: advent
      propers:
      - name: Alleluia (Tempore paschali)
        incipit: Virga Iesse floruit
        source: composed
        text: "ALLELUIA, alleluia. V. Virga Iesse floruit: María."
      - name: Alleluia (Tempore paschali)
        incipit: Virga Jesse floruit
        source: composed
        text: >-
          alleluia alleluia v virga Jesse floruit — María
""",
            ),
        )
        for label, rows in cases:
            with self.subTest(label=label):
                finished = self.check_fixture(rows)
                self.assertEqual(finished.returncode, 1, finished.stdout)
                self.assertEqual(finished.stderr, "")
                payload = json.loads(finished.stdout)
                self.assertEqual(payload.get("status"), "error")
                diagnostic = "\n".join(str(one) for one in payload.get("problems", []))
                self.assertIn("advent-1", diagnostic)
                self.assertIn("Alleluia (Tempore paschali)", diagnostic)
                self.assertIn("duplicate normalized Proper body", diagnostic)

    def test_duplicate_normalization_keeps_distinct_slot_and_form_identity(self) -> None:
        """A repeated formula in another appointed slot or form is not a duplicate."""

        rows = """\
    - key: repeated-in-distinct-slots
      name: Repeated in Distinct Slots
      registry: "01"
      season: test
      propers:
      - name: Introit
        incipit: Ad te levavi
        source: composed
        text: Ad te levavi animam meam.
      - name: Offertory
        incipit: Ad te levavi
        source: composed
        text: Ad te levavi animam meam.
    - key: repeated-in-distinct-forms
      name: Repeated in Distinct Forms
      registry: "02"
      season: test
      forms:
      - id: first
        name: First form
        propers:
        - name: Introit
          incipit: Requiem aeternam
          source: composed
          text: Requiem aeternam dona eis, Domine.
      - id: second
        name: Second form
        propers:
        - name: Introit
          incipit: Requiem aeternam
          source: composed
          text: Requiem aeternam dona eis, Domine.
"""
        finished = self.check_fixture(rows)
        self.assertEqual(finished.returncode, 0, finished.stdout)
        self.assertEqual(finished.stderr, "")
        payload = json.loads(finished.stdout)
        self.assertEqual(payload.get("status"), "ok")
        self.assertEqual(payload.get("problems"), [])

    def test_duplicate_normalization_preserves_substantive_latin_readings(self) -> None:
        """The duplicate detector is not the search index's broad Latin fold."""

        template = """\
    - key: distinct-reading
      name: Distinct Reading
      registry: "01"
      season: test
      propers:
      - name: Alleluia
        incipit: First reading
        source: composed
        text: "{first}"
      - name: Alleluia
        incipit: Second reading
        source: composed
        text: "{second}"
"""
        cases = (
            ("ae/ligature", "caelum", "cælum"),
            ("oe/ligature", "poena", "pœna"),
            ("v/u", "vivit", "uiuit"),
            ("y/i", "mysterium", "misterium"),
            ("diacritic", "Maria", "María"),
        )
        for label, first, second in cases:
            with self.subTest(label=label):
                finished = self.check_fixture(
                    template.format(first=first, second=second)
                )
                self.assertEqual(finished.returncode, 0, finished.stdout)
                self.assertEqual(finished.stderr, "")
                payload = json.loads(finished.stdout)
                self.assertEqual(payload.get("status"), "ok")
                self.assertEqual(payload.get("problems"), [])

    def test_invalid_inputs_are_typed_json_failures(self) -> None:
        cases = (
            (
                "invalid date",
                ("--date", "not-a-date", "--calendar", "postconciliar"),
                "--date must be an ISO date",
            ),
            (
                "unknown calendar",
                ("--date", REPRESENTATIVE_DATE, "--calendar", "not-a-calendar"),
                "no calendar 'not-a-calendar'",
            ),
        )
        for label, arguments, expected in cases:
            with self.subTest(label=label):
                finished = run_tpt(
                    "mass-today", "show", *arguments, "--lang", "en", "--json"
                )
                self.assertEqual(finished.returncode, 2, finished.stderr)
                self.assertEqual(finished.stdout, "")
                payload = json.loads(finished.stderr)
                self.assertEqual(payload.get("v"), 1)
                self.assertEqual(payload.get("status"), "error")
                self.assertEqual(payload.get("code"), "input")
                self.assertIn(expected, payload.get("error", ""))
                self.assertNotIn("days", payload)


if __name__ == "__main__":
    unittest.main()
