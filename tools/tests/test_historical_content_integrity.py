"""Corpus-level honesty checks for the historical Missal states.

These checks intentionally derive their expectations from the current corpus.
Evidence-backed additions may fill a typed gap, add a recension departure, or
complete a Common without updating a hand-maintained count here. What may not
change silently is the meaning of a remaining gap, a reference, or inherited
text: absences stay visibly typed, references resolve to their source, and the
emitted pre-1955 structure retains its recension stamp and aggregate coverage.
"""

from __future__ import annotations

import json
import sys
import tomllib
import unittest
from importlib.machinery import SourceFileLoader
from importlib.util import module_from_spec, spec_from_loader
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CALENDARS = ROOT / "src" / "sources" / "calendars"
PROPER_STRUCTURES = ROOT / "src" / "web" / "data" / "structure" / "propers"
ORDINARY_STRUCTURES = ROOT / "src" / "web" / "data" / "structure" / "ordinary"
ORDINARY_INVENTORIES = ROOT / "src" / "sources" / "inventories"
HISTORICAL_CALENDARS = ("roman-1962", "roman-pre-1955")
ORDINARY_FRAME_APPLICABILITY = {"full", "none", "unavailable"}
PRE_1955_EXCEPTIONAL_ORDINARY_FRAMES = {
    "blessing-of-palms": "none",
    "good-friday": "none",
    "palm-sunday": "unavailable",
    "easter-vigil": "unavailable",
}
PLACEHOLDER_PROSE_PREFIX = "This entry is a placeholder"
PRE_1955_TYPED_GAPS = {
    "palm-sunday",
    "blessing-of-palms",
    "chrism-mass",
    "mass-of-the-lords-supper",
    "good-friday",
    "easter-vigil",
}
PRE_1955_WITNESS_GAP = (
    "artifact.catholic-church.missale-romanum.vatican-typica-1920."
    "missale-romanum-1920-text-aa646196"
)

sys.path.insert(0, str(ROOT / "scripts"))

import _calendars  # noqa: E402


def load_mass_propers():
    loader = SourceFileLoader(
        "historical_content_mass_propers", str(ROOT / "tools" / "mass-propers")
    )
    spec = spec_from_loader(loader.name, loader)
    assert spec is not None
    module = module_from_spec(spec)
    loader.exec_module(module)
    return module


def masses(document: dict):
    for section_name, body in (document.get("sections") or {}).items():
        if not isinstance(body, dict):
            continue
        for mass in body.get("masses") or []:
            if isinstance(mass, dict):
                yield section_name, body, mass


def direct_propers(mass: dict):
    for proper in mass.get("propers") or []:
        if isinstance(proper, dict):
            yield "", proper
    for form in mass.get("forms") or []:
        if not isinstance(form, dict):
            continue
        label = str(form.get("name") or "")
        for proper in form.get("propers") or []:
            if isinstance(proper, dict):
                yield label, proper


def reference_nodes(mass: dict):
    yield mass
    for _, proper in direct_propers(mass):
        yield proper


class HistoricalProperIntegrityTest(unittest.TestCase):
    def test_pre_1955_holy_week_gaps_are_typed_not_pseudo_propers(self):
        """Structural evidence is retained without inventing liturgical text."""
        document = _calendars.load_document(
            CALENDARS, "roman-pre-1955", effective=False
        )
        source_masses = _calendars.mass_index(document)
        self.assertLessEqual(PRE_1955_TYPED_GAPS, set(source_masses))
        expected_status = {
            "state": "unavailable",
            "scope": "missal-formulary",
            "reasons": [
                {"kind": "witness-gap", "source_id": PRE_1955_WITNESS_GAP}
            ],
        }
        for key in PRE_1955_TYPED_GAPS:
            with self.subTest(mass=key):
                mass = source_masses[key]
                self.assertEqual(mass.get("text_status"), expected_status)
                self.assertEqual(list(direct_propers(mass)), [])

    def test_common_and_other_proper_references_resolve_in_both_states(self):
        """A Common is a source address, not a euphemism for missing material."""
        for calendar in HISTORICAL_CALENDARS:
            document = _calendars.load_document(CALENDARS, calendar)
            rows = list(masses(document))
            common_keys = {
                str(mass.get("key"))
                for section_name, body, mass in rows
                if body.get("kind") == "common" or section_name == "common"
            }
            self.assertTrue(common_keys, calendar)
            common_references = []
            for _, _, mass in rows:
                appointed, problems = _calendars.resolve_propers(document, mass)
                self.assertEqual(problems, [], (calendar, mass.get("key"), problems))
                for node in reference_nodes(mass):
                    reference = _calendars.reference_of(node)
                    if reference and str(reference.get("mass")) in common_keys:
                        common_references.append((mass, reference, appointed))

            self.assertTrue(common_references, calendar)
            for mass, reference, appointed in common_references:
                target = str(reference.get("mass"))
                self.assertTrue(appointed, (calendar, mass.get("key"), target))
                if node_name := reference.get("proper"):
                    self.assertTrue(
                        any(
                            provenance
                            and provenance.get("mass") == target
                            and provenance.get("proper") == node_name
                            for _, _, provenance in appointed
                        ),
                        (calendar, mass.get("key"), target, node_name),
                    )

    def test_generated_pre_1955_output_preserves_gaps_and_provenance(self):
        """The served recension must not drop the facts that keep it provisional."""
        raw = _calendars.load_document(
            CALENDARS, "roman-pre-1955", effective=False
        )
        document = _calendars.load_document(CALENDARS, "roman-pre-1955")
        source_masses = _calendars.mass_index(document)
        generated = json.loads(
            (PROPER_STRUCTURES / "roman-pre-1955.json").read_text(encoding="utf-8")
        )
        self.assertEqual(generated["recension_coverage"], raw["recension_coverage"])
        self.assertEqual(generated["advisory"], raw["advisory"])
        self.assertTrue(generated["advisory"].strip())
        generated_masses = {str(mass["key"]): mass for mass in generated["masses"]}
        self.assertEqual(set(generated_masses), set(source_masses))

        expected_placeholders = set()
        for key, mass in source_masses.items():
            stamp = mass.get("recension")
            self.assertIsInstance(stamp, dict, key)
            self.assertTrue(stamp.get("calendar"), key)
            if stamp.get("stated"):
                self.assertEqual(stamp.get("text_from"), "", key)
            else:
                self.assertEqual(stamp.get("text_from"), stamp.get("calendar"), key)
            if stamp.get("kind"):
                self.assertTrue(str(stamp.get("basis") or "").strip(), key)
            for additional in stamp.get("also") or []:
                self.assertTrue(additional.get("kind"), key)
                self.assertTrue(str(additional.get("basis") or "").strip(), key)

            appointed, problems = _calendars.resolve_propers(document, mass)
            self.assertEqual(problems, [], (key, problems))
            expected_placeholders.update(
                (key, form)
                for form, proper, _ in appointed
                if proper.get("name") == "Placeholder"
            )

            self.assertEqual(generated_masses[key].get("recension"), stamp, key)

        emitted_placeholders = [
            (str(mass["key"]), str(proper.get("form") or ""), proper)
            for mass in generated["masses"]
            for proper in mass.get("propers") or []
            if proper.get("name") == "Placeholder"
        ]
        self.assertEqual(
            {(key, form) for key, form, _ in emitted_placeholders},
            expected_placeholders,
        )
        for key, form, proper in emitted_placeholders:
            self.assertFalse(str(proper.get("text") or "").strip(), (key, form))

    def test_non_recension_structures_do_not_invent_recension_coverage(self):
        for calendar in ("roman-1962", "postconciliar"):
            with self.subTest(calendar=calendar):
                payload = json.loads(
                    (PROPER_STRUCTURES / f"{calendar}.json").read_text(
                        encoding="utf-8"
                    )
                )
                self.assertNotIn("recension_coverage", payload)
                self.assertNotIn("advisory", payload)

    def test_generated_historical_propers_do_not_emit_placeholder_prose(self):
        """Repository status prose is never emitted as appointed liturgical text."""
        sentinel_texts = set()
        for calendar in HISTORICAL_CALENDARS:
            document = _calendars.load_document(CALENDARS, calendar, effective=False)
            for _, _, mass in masses(document):
                for _, proper in direct_propers(mass):
                    text = str(proper.get("text") or "").strip()
                    if proper.get("name") == "Placeholder" or text.startswith(
                        PLACEHOLDER_PROSE_PREFIX
                    ):
                        self.assertTrue(text, (calendar, mass.get("key")))
                        sentinel_texts.add(text)

        for calendar in HISTORICAL_CALENDARS:
            payload = json.loads(
                (PROPER_STRUCTURES / f"{calendar}.json").read_text(encoding="utf-8")
            )
            for mass in payload["masses"]:
                for proper in mass.get("propers") or []:
                    self.assertNotEqual(
                        proper.get("name"),
                        "Placeholder",
                        (calendar, mass.get("key")),
                    )
                    text = str(proper.get("text") or "").strip()
                    self.assertNotIn(
                        text,
                        sentinel_texts,
                        (calendar, mass.get("key"), proper.get("name")),
                    )


class Pre1955OrdinaryFrameIntegrityTest(unittest.TestCase):
    def test_exceptional_rites_state_ordinary_frame_applicability(self):
        """Non-Mass and uncollated rites may not inherit a full Mass frame."""
        document = _calendars.load_document(
            CALENDARS, "roman-pre-1955", effective=False
        )
        source_masses = _calendars.mass_index(document)

        for key, expected in PRE_1955_EXCEPTIONAL_ORDINARY_FRAMES.items():
            self.assertIn(key, source_masses)
            frame = source_masses[key].get("ordinary_frame")
            self.assertIsInstance(frame, dict, key)
            self.assertEqual(frame.get("applicability"), expected, key)
            self.assertTrue(str(frame.get("basis") or "").strip(), key)

        for key, mass in source_masses.items():
            frame = mass.get("ordinary_frame")
            if frame is None:
                continue
            self.assertIsInstance(frame, dict, key)
            self.assertIn(frame.get("applicability"), ORDINARY_FRAME_APPLICABILITY, key)
            self.assertTrue(str(frame.get("basis") or "").strip(), key)

    def test_generated_structures_omit_default_frames_and_preserve_exceptions(self):
        """Only source-declared mappings cross the browser serialization boundary."""
        propers = load_mass_propers()
        tokens = propers.book_tokens()
        for calendar in ("postconciliar", *HISTORICAL_CALENDARS):
            with self.subTest(calendar=calendar):
                source = _calendars.load_document(CALENDARS, calendar)
                expected = {
                    key: mass["ordinary_frame"]
                    for key, mass in _calendars.mass_index(source).items()
                    if isinstance(mass.get("ordinary_frame"), dict)
                }
                generated = propers.calendar_structure(CALENDARS, calendar, tokens)
                emitted = {
                    str(mass["key"]): mass["ordinary_frame"]
                    for mass in generated["masses"]
                    if "ordinary_frame" in mass
                }

                self.assertEqual(emitted, expected)
                self.assertTrue(
                    all(isinstance(frame, dict) for frame in emitted.values())
                )
                if calendar == "roman-pre-1955":
                    self.assertEqual(
                        set(emitted), set(PRE_1955_EXCEPTIONAL_ORDINARY_FRAMES)
                    )
                else:
                    self.assertEqual(emitted, {})


class HistoricalOrdinaryIntegrityTest(unittest.TestCase):
    def test_every_unheld_historical_ordinary_side_names_a_typed_absence(self):
        """No empty translation cell may be mistaken for a liturgical omission."""
        for calendar in HISTORICAL_CALENDARS:
            payload = json.loads(
                (ORDINARY_STRUCTURES / f"{calendar}.json").read_text(encoding="utf-8")
            )
            source = tomllib.loads(
                (ORDINARY_INVENTORIES / f"{calendar}-ordo-missae-v1.toml").read_text(
                    encoding="utf-8"
                )
            )
            source_absences = {
                str(row["key"]): row for row in source.get("absences") or []
            }
            absence_rows = {str(row["key"]): row for row in payload["absences"]}
            language_sides = {"en": "english", "la": "latin"}
            references = {key: 0 for key in absence_rows}

            for section in payload["sections"]:
                for element in section["elements"]:
                    held = {str(row["lang"]) for row in element.get("translations") or []}
                    for language in payload["languages"]:
                        lang = str(language["lang"])
                        context = (calendar, element["key"], lang)
                        reason = (element.get("absent") or {}).get(language_sides[lang])
                        self.assertNotEqual(lang in held, bool(reason), context)
                        if reason:
                            self.assertIn(reason, absence_rows, context)
                            self.assertTrue(absence_rows[reason].get("kind"), (calendar, reason))
                            self.assertEqual(
                                set(absence_rows[reason]),
                                {"key", "count", "state", "kind"},
                                (calendar, reason),
                            )
                            self.assertIn(reason, source_absences, (calendar, reason))
                            self.assertTrue(
                                str(source_absences[reason].get("what") or "").strip(),
                                (calendar, reason),
                            )
                            references[reason] += 1

            self.assertEqual(
                references,
                {key: int(row["count"]) for key, row in absence_rows.items()},
                calendar,
            )


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
