#!/usr/bin/env python3
"""Structural regression gate for a complete year of ``mass-today`` dumps.

The ordinary test run checks the fixed matrix, the ``tpt`` registration, and
the validator without retaining any liturgical text.  The expensive live pass
is deliberately opt-in::

    TRIPTYCH_COMPLETE_MISSAL_YEAR=1 \
      python -m unittest tools.tests.test_complete_missal_year

That pass asks ``tools/tpt mass-today`` for one JSON dump and one plain-text
dump per date, calendar, and language.  It validates each in memory and
immediately discards it.  It records neither copyrighted prose nor a volatile
snapshot of known corpus gaps.
"""

from __future__ import annotations

import concurrent.futures
import copy
import datetime as dt
import hashlib
import json
import os
import subprocess
import unittest
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
TPT = ROOT / "tools" / "tpt"

FIRST_DATE = dt.date(2026, 8, 26)
LAST_DATE = dt.date(2027, 8, 25)
CALENDARS = ("postconciliar", "roman-1962", "roman-pre-1955")
LANGUAGES = ("en", "la")
EXPECTED_DAYS = 365
EXPECTED_DUMPS = EXPECTED_DAYS * len(CALENDARS) * len(LANGUAGES)
EXPECTED_RENDERS = EXPECTED_DUMPS * 2

FULL_RUN_ENV = "TRIPTYCH_COMPLETE_MISSAL_YEAR"
WORKERS_ENV = "TRIPTYCH_COMPLETE_MISSAL_YEAR_WORKERS"
CASE_TIMEOUT_SECONDS = 120
MAX_REPORTED_FAILURES = 20


@dataclass(frozen=True, order=True)
class DumpCase:
    """One non-textual coordinate in the audit matrix."""

    date: dt.date
    calendar: str
    language: str

    @property
    def label(self) -> str:
        return f"{self.date.isoformat()} {self.calendar} {self.language}"


def audit_dates() -> tuple[dt.date, ...]:
    """Return the inclusive, fixed audit interval."""

    return tuple(
        FIRST_DATE + dt.timedelta(days=offset)
        for offset in range((LAST_DATE - FIRST_DATE).days + 1)
    )


def audit_matrix() -> tuple[DumpCase, ...]:
    """Return every date/calendar/language coordinate in stable order."""

    return tuple(
        DumpCase(date, calendar, language)
        for date in audit_dates()
        for calendar in CALENDARS
        for language in LANGUAGES
    )


def dump_command(case: DumpCase) -> list[str]:
    """Build the one authoritative command used by the live audit."""

    return [
        str(TPT),
        "mass-today",
        "show",
        "--date",
        case.date.isoformat(),
        "--calendar",
        case.calendar,
        "--lang",
        case.language,
        "--ordinary",
        "--why",
        "--format",
        "json",
    ]


def text_dump_command(case: DumpCase) -> list[str]:
    """Build a plain-text sentinel command for the requested language."""

    command = dump_command(case)
    command[-1] = "text"
    return [*command, "--style", "plain"]


def _require(condition: bool, path: str, expectation: str) -> None:
    if not condition:
        raise ValueError(f"{path}: expected {expectation}")


def _validate_citation(citation: object, path: str) -> None:
    _require(isinstance(citation, dict), path, "an object")
    assert isinstance(citation, dict)
    _require(isinstance(citation.get("book"), str), f"{path}.book", "a string")
    _require(isinstance(citation.get("ref"), str), f"{path}.ref", "a string")
    ranges = citation.get("ranges")
    _require(isinstance(ranges, list), f"{path}.ranges", "an array")
    for range_index, one_range in enumerate(ranges):
        range_path = f"{path}.ranges[{range_index}]"
        _require(isinstance(one_range, dict), range_path, "an object")
        assert isinstance(one_range, dict)
        for endpoint in ("begin", "end"):
            value = one_range.get(endpoint)
            endpoint_path = f"{range_path}.{endpoint}"
            _require(isinstance(value, dict), endpoint_path, "an object")
            assert isinstance(value, dict)
            _require(
                isinstance(value.get("chapter"), int),
                f"{endpoint_path}.chapter",
                "an integer",
            )
            # Whole-chapter citations deliberately have no verse number.
            _require(
                value.get("verse") is None or isinstance(value.get("verse"), int),
                f"{endpoint_path}.verse",
                "an integer or null",
            )


def _validate_proper_material(material: object, path: str) -> None:
    _require(isinstance(material, dict), path, "an object")
    assert isinstance(material, dict)
    verses = material.get("verses", [])
    _require(isinstance(verses, list), f"{path}.verses", "an array")
    for verse_index, citation in enumerate(verses):
        _validate_citation(citation, f"{path}.verses[{verse_index}]")


def _validate_proper(proper: object, case: DumpCase, path: str) -> None:
    _require(isinstance(proper, dict), path, "an object")
    assert isinstance(proper, dict)
    _require(
        isinstance(proper.get("name"), str) and bool(proper.get("name")),
        f"{path}.name",
        "a non-empty string",
    )
    _require(
        isinstance(proper.get("source"), str) and bool(proper.get("source")),
        f"{path}.source",
        "a non-empty string",
    )
    selection = proper.get("language_selection")
    _require(isinstance(selection, dict), f"{path}.language_selection", "an object")
    assert isinstance(selection, dict)
    _require(
        selection.get("requested") == case.language,
        f"{path}.language_selection.requested",
        case.language,
    )
    _require(
        isinstance(selection.get("status"), str) and bool(selection.get("status")),
        f"{path}.language_selection.status",
        "a non-empty string",
    )
    _validate_proper_material(proper, path)

    for field, allowed in (("cycles", {"A", "B", "C"}),
                           ("weekday_cycles", {"I", "II"})):
        if field not in proper:
            continue
        branches = proper[field]
        _require(isinstance(branches, dict), f"{path}.{field}", "an object")
        assert isinstance(branches, dict)
        _require(bool(branches), f"{path}.{field}", "at least one branch")
        _require(set(branches).issubset(allowed), f"{path}.{field}", "known cycle keys")
        for key, material in branches.items():
            _validate_proper_material(material, f"{path}.{field}.{key}")


def _validate_ordinary(ordinary: object, case: DumpCase, path: str) -> None:
    _require(isinstance(ordinary, dict), path, "an object")
    assert isinstance(ordinary, dict)
    _require("refused" not in ordinary, path, "an available Ordinary")
    _require(
        ordinary.get("schema") == "triptych-ordinary-structure/v1",
        f"{path}.schema",
        "triptych-ordinary-structure/v1",
    )
    _require(ordinary.get("calendar") == case.calendar, f"{path}.calendar", case.calendar)

    sections = ordinary.get("sections")
    _require(isinstance(sections, list) and bool(sections), f"{path}.sections", "a non-empty array")
    assert isinstance(sections, list)
    for section_index, section in enumerate(sections):
        section_path = f"{path}.sections[{section_index}]"
        _require(isinstance(section, dict), section_path, "an object")
        assert isinstance(section, dict)
        _require(isinstance(section.get("key"), str), f"{section_path}.key", "a string")
        _require(isinstance(section.get("elements"), list), f"{section_path}.elements", "an array")

    _require(isinstance(ordinary.get("slots"), list), f"{path}.slots", "an array")
    languages = ordinary.get("languages")
    _require(isinstance(languages, list), f"{path}.languages", "an array")
    assert isinstance(languages, list)
    declared = {
        row.get("lang")
        for row in languages
        if isinstance(row, dict) and isinstance(row.get("lang"), str)
    }
    _require(case.language in declared, f"{path}.languages", f"a {case.language} row")


def _validate_ordinary_result(day: dict, case: DumpCase, path: str) -> None:
    """Require an Ordinary or an exact, structurally justified suppression."""

    ordinary = day.get("ordinary")
    if isinstance(ordinary, dict):
        _require("ordinary_suppressed" not in day, path, "one result, not two")
        _validate_ordinary(ordinary, case, path)
        return

    _require(ordinary is None, path, "an object or a typed suppression")
    suppression = day.get("ordinary_suppressed")
    _require(isinstance(suppression, dict), path, "an object or a typed suppression")
    assert isinstance(suppression, dict)
    suppression_path = path.removesuffix(".ordinary") + ".ordinary_suppressed"
    kind = suppression.get("kind")
    _require(
        kind in {
            "territory-choice-required",
            "mass-choice-required",
            "form-choice-required",
            "ordinary-frame",
            "ferial-formulary-unavailable",
            "day-unsettled",
        },
        f"{suppression_path}.kind",
        "a recognized suppression kind",
    )
    if kind == "territory-choice-required":
        _require(
            day.get("territory_choice_required") is True
            and day.get("selected_mass") is None,
            suppression_path,
            "an unresolved territory choice",
        )
    elif kind == "mass-choice-required":
        _require(
            day.get("choice_required") is True and day.get("selected_mass") is None,
            suppression_path,
            "an unresolved Mass choice",
        )
    elif kind == "form-choice-required":
        selected = day.get("selected_mass")
        mass = next(
            (
                row
                for row in day.get("masses") or []
                if isinstance(row, dict) and row.get("key") == selected
            ),
            None,
        )
        _require(
            isinstance(mass, dict) and mass.get("form_choice_required") is True,
            suppression_path,
            "a selected Mass with an unresolved form choice",
        )
    elif kind == "ordinary-frame":
        frame = day.get("ordinary_frame")
        _require(
            isinstance(frame, dict)
            and frame.get("applicability") in {"none", "unavailable"}
            and isinstance(frame.get("basis"), str)
            and bool(frame["basis"].strip()),
            suppression_path,
            "a typed non-full Ordinary frame",
        )
    elif kind == "ferial-formulary-unavailable":
        implied_without_formulary = any(
            isinstance(branch, dict)
            and branch.get("settled") is True
            and isinstance(branch.get("winner"), dict)
            and branch["winner"].get("source") == "implied"
            and branch["winner"].get("key") is None
            and branch["winner"].get("formulary") is None
            for branch in day.get("branches") or []
        )
        _require(
            day.get("settled") is True
            and day.get("selected_mass") is None
            and implied_without_formulary,
            suppression_path,
            "a settled implied feria with no held formulary",
        )
    else:
        _require(
            day.get("settled") is not True and bool(day.get("unsettled")),
            suppression_path,
            "an actually unsettled day",
        )


def validate_dump(payload: object, case: DumpCase) -> None:
    """Validate identity and structure while deliberately ignoring prose."""

    _require(isinstance(payload, dict), "$", "an object")
    assert isinstance(payload, dict)
    _require(payload.get("v") == 1, "$.v", "1")
    _require(payload.get("status") == "ok", "$.status", "ok")
    _require(payload.get("problems") == [], "$.problems", "an empty array")
    _require(payload.get("date") == case.date.isoformat(), "$.date", case.date.isoformat())

    language = payload.get("language")
    _require(isinstance(language, dict), "$.language", "an object")
    assert isinstance(language, dict)
    _require(
        language.get("mode") == "language-projection",
        "$.language.mode",
        "language-projection",
    )
    _require(language.get("requested") == case.language, "$.language.requested", case.language)
    selection = language.get("selection")
    _require(isinstance(selection, dict), "$.language.selection", "an object")
    assert isinstance(selection, dict)
    _require(selection.get("lang") == case.language, "$.language.selection.lang", case.language)

    days = payload.get("days")
    _require(isinstance(days, list) and len(days) == 1, "$.days", "exactly one day")
    assert isinstance(days, list)
    day = days[0]
    _require(isinstance(day, dict), "$.days[0]", "an object")
    assert isinstance(day, dict)
    _require(day.get("calendar") == case.calendar, "$.days[0].calendar", case.calendar)
    for field in ("commemorations", "masses", "unsettled"):
        _require(isinstance(day.get(field), list), f"$.days[0].{field}", "an array")
    _require(isinstance(day.get("why"), dict), "$.days[0].why", "an object")
    _require(
        day.get("settled") is None or isinstance(day.get("settled"), bool),
        "$.days[0].settled",
        "a boolean or null",
    )
    _validate_ordinary_result(day, case, "$.days[0].ordinary")

    masses = day["masses"]
    mass_keys: list[str] = []
    for mass_index, mass in enumerate(masses):
        mass_path = f"$.days[0].masses[{mass_index}]"
        _require(isinstance(mass, dict), mass_path, "an object")
        assert isinstance(mass, dict)
        _require("refused" not in mass, mass_path, "available propers")
        key = mass.get("key")
        _require(isinstance(key, str) and bool(key), f"{mass_path}.key", "a non-empty string")
        assert isinstance(key, str)
        mass_keys.append(key)
        _require(isinstance(mass.get("propers"), list), f"{mass_path}.propers", "an array")
        for proper_index, proper in enumerate(mass["propers"]):
            _validate_proper(proper, case, f"{mass_path}.propers[{proper_index}]")
    _require(len(mass_keys) == len(set(mass_keys)), "$.days[0].masses", "unique mass keys")


def _run_dump(case: DumpCase) -> str | None:
    """Run and validate one dump, returning only non-textual failure detail."""

    try:
        finished = subprocess.run(
            dump_command(case),
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=False,
            timeout=CASE_TIMEOUT_SECONDS,
        )
    except subprocess.TimeoutExpired:
        return f"{case.label}: timed out after {CASE_TIMEOUT_SECONDS} seconds"
    except OSError as error:
        return f"{case.label}: tpt could not start ({error.__class__.__name__})"

    if finished.returncode != 0:
        return f"{case.label}: tpt exited {finished.returncode}"
    if finished.stderr:
        return f"{case.label}: tpt wrote to stderr"
    try:
        payload = json.loads(finished.stdout)
    except json.JSONDecodeError as error:
        return f"{case.label}: invalid JSON at line {error.lineno}, column {error.colno}"
    try:
        validate_dump(payload, case)
    except ValueError as error:
        return f"{case.label}: {error}"
    return None


def _run_text_fingerprint(case: DumpCase) -> tuple[str | None, int, str]:
    """Validate a transient text dump, returning only size and identity."""

    try:
        finished = subprocess.run(
            text_dump_command(case),
            cwd=ROOT,
            capture_output=True,
            check=False,
            timeout=CASE_TIMEOUT_SECONDS,
        )
    except subprocess.TimeoutExpired:
        return (
            f"{case.label}: text dump timed out after {CASE_TIMEOUT_SECONDS} seconds",
            0,
            "",
        )
    except OSError as error:
        return (
            f"{case.label}: text dump could not start ({error.__class__.__name__})",
            0,
            "",
        )

    if finished.returncode != 0:
        return (f"{case.label}: text tpt exited {finished.returncode}", 0, "")
    if finished.stderr:
        return (f"{case.label}: text tpt wrote to stderr", 0, "")
    if not finished.stdout.strip():
        return (f"{case.label}: text tpt produced no non-whitespace output", 0, "")
    return (None, len(finished.stdout), hashlib.sha256(finished.stdout).hexdigest())


def _run_complete_case(case: DumpCase) -> str | None:
    """Validate both reproducible representations for one audit coordinate."""

    failure = _run_dump(case)
    if failure:
        return failure
    failure, _, _ = _run_text_fingerprint(case)
    return failure


def _synthetic_payload(case: DumpCase) -> dict:
    """A prose-free envelope used to test the structural validator itself."""

    return {
        "v": 1,
        "status": "ok",
        "problems": [],
        "date": case.date.isoformat(),
        "language": {
            "mode": "language-projection",
            "requested": case.language,
            "selection": {"lang": case.language},
        },
        "days": [{
            "calendar": case.calendar,
            "commemorations": [],
            "masses": [{
                "key": "synthetic-mass",
                "propers": [{
                    "name": "Synthetic proper",
                    "source": "scripture",
                    "language_selection": {
                        "requested": case.language,
                        "status": "scripture-delegated",
                    },
                    "verses": [{
                        "book": "Synthetic book",
                        "ref": "Synthetic reference",
                        "ranges": [{
                            "begin": {"chapter": 1, "verse": None},
                            "end": {"chapter": 1, "verse": None},
                        }],
                    }],
                    "cycles": {"A": {"verses": []}},
                }],
            }],
            "settled": True,
            "unsettled": [],
            "why": {},
            "ordinary": {
                "schema": "triptych-ordinary-structure/v1",
                "calendar": case.calendar,
                "sections": [{"key": "synthetic-section", "elements": []}],
                "slots": [],
                "languages": [{"lang": language} for language in LANGUAGES],
            },
        }],
    }


class CompleteMissalYearContractTests(unittest.TestCase):
    def test_fixed_interval_and_matrix_are_complete_and_unique(self) -> None:
        dates = audit_dates()
        self.assertEqual(len(dates), EXPECTED_DAYS)
        self.assertEqual((dates[0], dates[-1]), (FIRST_DATE, LAST_DATE))
        self.assertTrue(all(right - left == dt.timedelta(days=1)
                            for left, right in zip(dates, dates[1:])))

        matrix = audit_matrix()
        self.assertEqual(len(matrix), EXPECTED_DUMPS)
        self.assertEqual(len(set(matrix)), EXPECTED_DUMPS)
        for date in dates:
            coordinates = {
                (case.calendar, case.language)
                for case in matrix
                if case.date == date
            }
            self.assertEqual(
                coordinates,
                {(calendar, language) for calendar in CALENDARS for language in LANGUAGES},
            )

    def test_every_command_uses_tpt_and_requests_the_complete_json_surface(self) -> None:
        for case in audit_matrix():
            command = dump_command(case)
            self.assertEqual(command[:3], [str(TPT), "mass-today", "show"])
            self.assertEqual(command.count("--date"), 1)
            self.assertEqual(command[command.index("--date") + 1], case.date.isoformat())
            self.assertEqual(command[command.index("--calendar") + 1], case.calendar)
            self.assertEqual(command[command.index("--lang") + 1], case.language)
            self.assertIn("--ordinary", command)
            self.assertIn("--why", command)
            self.assertEqual(command[command.index("--format") + 1], "json")

            text_command = text_dump_command(case)
            self.assertEqual(text_command[:3], [str(TPT), "mass-today", "show"])
            self.assertEqual(text_command[text_command.index("--format") + 1], "text")
            self.assertEqual(text_command[text_command.index("--style") + 1], "plain")
            self.assertEqual(text_command[text_command.index("--lang") + 1], case.language)

    def test_tpt_registers_the_composed_read_only_tool(self) -> None:
        finished = subprocess.run(
            [str(TPT), "--info", "mass-today", "--json"],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(finished.returncode, 0, "tpt could not describe mass-today")
        self.assertEqual(finished.stderr, "")
        record = json.loads(finished.stdout)
        self.assertEqual(record["name"], "mass-today")
        self.assertTrue(record["json"])
        self.assertFalse(record["mutates"])
        self.assertEqual(
            set(record["requires"]),
            {"calendar-days", "calendar-rubrics", "mass-ordinary", "mass-propers"},
        )

    def test_representative_text_dumps_honor_each_language(self) -> None:
        cases = [
            DumpCase(FIRST_DATE, calendar, language)
            for calendar in CALENDARS
            for language in LANGUAGES
        ]
        with concurrent.futures.ThreadPoolExecutor(max_workers=len(cases)) as executor:
            results = dict(zip(cases, executor.map(_run_text_fingerprint, cases)))

        for case, (error, size, _) in results.items():
            if error:
                self.fail(error)
            self.assertGreater(size, 0, f"{case.label}: empty text dump")
        for calendar in CALENDARS:
            english = results[DumpCase(FIRST_DATE, calendar, "en")][2]
            latin = results[DumpCase(FIRST_DATE, calendar, "la")][2]
            self.assertTrue(
                english != latin,
                f"{calendar}: en and la text dumps are byte-identical",
            )

    def test_validator_checks_identity_failures_without_comparing_prose(self) -> None:
        case = audit_matrix()[0]
        payload = _synthetic_payload(case)
        validate_dump(payload, case)

        partial = copy.deepcopy(payload)
        partial["status"] = "partial"
        with self.assertRaisesRegex(ValueError, r"\$\.status"):
            validate_dump(partial, case)

        wrong_calendar = copy.deepcopy(payload)
        wrong_calendar["days"][0]["calendar"] = "another-calendar"
        with self.assertRaisesRegex(ValueError, r"\$\.days\[0\]\.calendar"):
            validate_dump(wrong_calendar, case)

        wrong_language = copy.deepcopy(payload)
        wrong_language["language"]["requested"] = "another-language"
        with self.assertRaisesRegex(ValueError, r"\$\.language\.requested"):
            validate_dump(wrong_language, case)

        ignored_proper_language = copy.deepcopy(payload)
        ignored_proper_language["days"][0]["masses"][0]["propers"][0][
            "language_selection"
        ]["requested"] = "another-language"
        with self.assertRaisesRegex(ValueError, r"language_selection\.requested"):
            validate_dump(ignored_proper_language, case)

        refused = copy.deepcopy(payload)
        refused["days"][0]["ordinary"] = {"refused": "synthetic"}
        with self.assertRaisesRegex(ValueError, r"\$\.days\[0\]\.ordinary"):
            validate_dump(refused, case)

        suppressed = copy.deepcopy(payload)
        suppressed_day = suppressed["days"][0]
        suppressed_day.pop("ordinary")
        suppressed_day["selected_mass"] = None
        suppressed_day["choice_required"] = True
        suppressed_day["ordinary_suppressed"] = {"kind": "mass-choice-required"}
        validate_dump(suppressed, case)

        ferial = copy.deepcopy(payload)
        ferial_day = ferial["days"][0]
        ferial_day.pop("ordinary")
        ferial_day["selected_mass"] = None
        ferial_day["branches"] = [{
            "settled": True,
            "winner": {"source": "implied", "key": None, "formulary": None},
        }]
        ferial_day["ordinary_suppressed"] = {
            "kind": "ferial-formulary-unavailable",
        }
        validate_dump(ferial, case)


@unittest.skipUnless(
    os.environ.get(FULL_RUN_ENV) == "1",
    f"set {FULL_RUN_ENV}=1 to execute all {EXPECTED_RENDERS} live renderings",
)
class CompleteMissalYearLiveTests(unittest.TestCase):
    def test_every_live_json_and_text_dump_is_well_formed(self) -> None:
        try:
            workers = int(os.environ.get(WORKERS_ENV, min(8, os.cpu_count() or 1)))
        except ValueError as error:
            self.fail(f"{WORKERS_ENV} must be an integer: {error}")
        if not 1 <= workers <= 32:
            self.fail(f"{WORKERS_ENV} must be between 1 and 32")

        matrix = iter(audit_matrix())
        failures: list[str] = []
        completed = 0
        with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as executor:
            pending = {
                executor.submit(_run_complete_case, case): case
                for case in (next(matrix, None) for _ in range(workers))
                if case is not None
            }
            while pending:
                done, _ = concurrent.futures.wait(
                    pending,
                    return_when=concurrent.futures.FIRST_COMPLETED,
                )
                for future in done:
                    pending.pop(future)
                    completed += 1
                    failure = future.result()
                    if failure:
                        failures.append(failure)
                    if len(failures) >= MAX_REPORTED_FAILURES:
                        for waiting in pending:
                            waiting.cancel()
                        pending.clear()
                        break
                    case = next(matrix, None)
                    if case is not None:
                        pending[executor.submit(_run_complete_case, case)] = case

        if failures:
            self.fail(
                f"{len(failures)} JSON/text dump failures after {completed} cases "
                f"(showing at most {MAX_REPORTED_FAILURES}):\n"
                + "\n".join(sorted(failures))
            )
        self.assertEqual(completed, EXPECTED_DUMPS)


if __name__ == "__main__":
    unittest.main()
