#!/usr/bin/env python3
"""Focused contract tests for the composed complete-Missal report."""
from __future__ import annotations

import contextlib
import importlib.machinery
import importlib.util
import io
import json
import unittest
from pathlib import Path
from unittest import mock


ROOT = Path(__file__).resolve().parents[2]
PATH = ROOT / "tools" / "complete-missal"
LOADER = importlib.machinery.SourceFileLoader("complete_missal_tool", str(PATH))
SPEC = importlib.util.spec_from_loader(LOADER.name, LOADER)
assert SPEC is not None
REPORT = importlib.util.module_from_spec(SPEC)
LOADER.exec_module(REPORT)


def fixture_reports() -> tuple[dict, dict, dict]:
    calendars = {}
    finding = []
    english = []
    placement = []
    ordinary = []
    rows = {
        "roman-pre-1955": (1, 1, 2),
        "roman-1962": (2, 2, 2),
        "postconciliar": (3, 4, 3),
    }
    for index, (calendar, (raw_masses, celebrations, effective_masses)) in enumerate(
        rows.items()
    ):
        calendars[calendar] = {
            "masses": raw_masses,
            "ranks": [{"rank": "demo", "celebrations": celebrations}],
        }
        finding.append(
            {
                "calendar": calendar,
                "direct_resolved_occurrences": 3,
                "masses_resolving_no_propers": 1,
                "placeholder_proper_records": 1,
                "referenced_resolved_occurrences": 2,
                "resolution_errors": ([{"mass": "broken"}] if index == 2 else []),
                "resolved_proper_occurrences": 5,
            }
        )
        english.append(
            {
                "calendar": calendar,
                "ledgered_untranslated": 1,
                "outside_the_ledger": 0,
                "rights_restricted": 0,
                "slots": 4,
                "stale_translation_records": 0,
                "unaccounted": 1,
                "unmatched_records": 1,
                "with_english": 2,
            }
        )
        placement.append(
            {
                "calendar": calendar,
                "masses": effective_masses,
                "masses_never_placed": [
                    {"declared": index == 0, "key": f"unplaced-{index}"}
                ],
            }
        )
        ordinary.append(
            {
                "absent": [{"count": 1, "key": "witness-gap"}],
                "calendar": calendar,
                "elements": 3,
                "witnesses": [
                    {"held": 2, "lang": "en"},
                    {"held": 1, "lang": "la"},
                ],
            }
        )
    propers = {
        "calendars": calendars,
        "english_coverage": english,
        "finding_aid_coverage": finding,
        "latin_recension_coverage": {
            "calendar": "postconciliar",
            "resident_bodies": 3,
            "unmatched_overlay_records": 1,
        },
    }
    return propers, {"coverage": placement}, {"coverage": ordinary}


class CompleteMissalReportTests(unittest.TestCase):
    def test_every_family_has_exactly_the_fifteen_warrant_dimensions(self) -> None:
        report = REPORT.build_report(*fixture_reports())
        self.assertEqual(report["schema"], "triptych-complete-missal-completeness/v1")
        self.assertEqual(report["status"], "unresolved")
        self.assertEqual(report["check"]["unresolved_dimension_cells"], 39)
        self.assertTrue(report["check"]["valid"])
        self.assertFalse(report["check"]["resolved"])

        for family in report["families"]:
            found = {
                name
                for group in REPORT.GROUPS
                for name in family[group]
            }
            self.assertEqual(found, REPORT.DIMENSIONS)
            self.assertEqual(len(found), 15)
            for group in REPORT.GROUPS:
                for dimension in family[group].values():
                    if dimension["state"] == "unresolved":
                        self.assertIsNone(dimension["count"])
                        self.assertIsInstance(dimension["lower_bound"], int)
                        self.assertIsInstance(dimension["reason"]["kind"], str)
                    else:
                        self.assertIsInstance(dimension["count"], int)

    def test_representation_and_expectation_are_not_conflated(self) -> None:
        report = REPORT.build_report(*fixture_reports())
        families = {row["calendar"]: row for row in report["families"]}

        recension = families["roman-pre-1955"]
        represented = recension["structural"]["represented_celebrations"]
        expected = recension["structural"]["expected_celebrations"]
        missing = recension["structural"]["missing_celebrations"]
        self.assertEqual(represented["count"], 1)
        self.assertEqual(represented["scope"], "recension-delta")
        self.assertEqual(represented["effective_mass_rows"], 2)
        self.assertIsNone(expected["count"])
        self.assertEqual(expected["lower_bound"], 2)
        self.assertEqual(expected["reason"]["kind"], "expectation-model-gap")
        self.assertIsNone(missing["count"])

        postconciliar = families["postconciliar"]
        self.assertEqual(
            postconciliar["structural"]["represented_celebrations"]["count"], 4
        )
        self.assertEqual(
            postconciliar["textual"]["expected_text_slots"]["lower_bound"], 8
        )

    def test_known_slices_are_lower_bounds_not_false_complete_totals(self) -> None:
        report = REPORT.build_report(*fixture_reports())
        rows = {row["calendar"]: row for row in report["families"]}
        postconciliar = rows["postconciliar"]["textual"]
        self.assertEqual(postconciliar["filled_text_slots"]["lower_bound"], 5)
        self.assertIsNone(postconciliar["filled_text_slots"]["count"])
        self.assertEqual(postconciliar["inherited_reference_slots"]["count"], 2)
        self.assertEqual(postconciliar["malformed_slots"]["lower_bound"], 1)
        self.assertEqual(postconciliar["orphan_texts"]["lower_bound"], 2)
        self.assertIsNone(postconciliar["unreachable_texts"]["count"])
        self.assertEqual(
            postconciliar["unreachable_texts"]["known_unplaced_masses"],
            {"declared": 0, "undeclared": 1},
        )

    def test_the_full_year_runtime_gate_is_linked_but_not_counted(self) -> None:
        report = REPORT.build_report(*fixture_reports())
        gate = report["scope"]["runtime_year_gate"]
        self.assertFalse(gate["included"])
        self.assertEqual(gate["expected_renders"], 4380)
        self.assertIn("test_complete_missal_year", gate["command"])

    def test_report_bytes_are_deterministic_for_the_same_owned_inputs(self) -> None:
        first = REPORT.build_report(*fixture_reports())
        second = REPORT.build_report(*fixture_reports())
        serialise = lambda value: json.dumps(  # noqa: E731
            value, ensure_ascii=False, sort_keys=True, separators=(",", ":")
        )
        self.assertEqual(serialise(first), serialise(second))

    def test_an_owner_partition_failure_is_refused_not_reported_as_zero(self) -> None:
        reports = fixture_reports()
        reports[0]["english_coverage"][0]["slots"] = 99
        with self.assertRaisesRegex(REPORT.Refused, "does not partition"):
            REPORT.build_report(*reports)

    def test_untyped_unknown_is_refused(self) -> None:
        report = REPORT.build_report(*fixture_reports())
        family = report["families"][0]
        family["textual"]["unknown_slots"]["reason"] = {}
        with self.assertRaisesRegex(REPORT.Refused, "typed unresolved reason"):
            REPORT.validate_family(family)

    def test_integrity_check_succeeds_and_resolved_check_is_red(self) -> None:
        reports = fixture_reports()
        with mock.patch.object(REPORT, "owning_reports", return_value=reports):
            with contextlib.redirect_stdout(io.StringIO()):
                self.assertEqual(REPORT.main([]), 0)
            with contextlib.redirect_stdout(io.StringIO()):
                self.assertEqual(REPORT.main(["--check"]), 0)
            with contextlib.redirect_stdout(io.StringIO()):
                self.assertEqual(REPORT.main(["--require-resolved"]), 1)


if __name__ == "__main__":
    unittest.main()
