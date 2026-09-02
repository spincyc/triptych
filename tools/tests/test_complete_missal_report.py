#!/usr/bin/env python3
"""Focused contract tests for the composed complete-Missal report."""
from __future__ import annotations

import copy
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
        "roman-pre-1955": (1, 1, 2, 3),
        "roman-1962": (2, 2, 2, 2),
        "postconciliar": (3, 4, 3, 4),
    }
    for index, (
        calendar,
        (raw_masses, celebrations, effective_masses, effective_celebrations),
    ) in enumerate(
        rows.items()
    ):
        calendars[calendar] = {
            "masses": raw_masses,
            "ranks": [
                {
                    "rank": "demo",
                    "entries": raw_masses,
                    "celebrations": celebrations,
                }
            ],
        }
        finding.append(
            {
                "calendar": calendar,
                "direct_resolved_occurrences": 3,
                "effective_celebrations": effective_celebrations,
                "masses_resolving_no_propers": 1,
                "placeholder_proper_records": 1,
                "referenced_resolved_occurrences": 2,
                "resolution_errors": ([{"mass": "broken"}] if index == 2 else []),
                "resolved_proper_occurrences": 5,
                "unresolved_common_set_selections": (
                    [
                        {
                            "candidates": ["c1", "c2"],
                            "group": "orations",
                            "mass": f"unresolved-{index}",
                            "target": "common-demo",
                        }
                    ]
                    if index < 2
                    else []
                ),
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
                "translation_ledger_calendar": calendar,
                "translation_ledger_calendars": (
                    ["roman-1962", "roman-pre-1955"]
                    if calendar == "roman-pre-1955"
                    else [calendar]
                ),
                "translation_ledger_inherited": calendar == "roman-pre-1955",
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
                    {
                        "declared": index == 0,
                        "key": f"unplaced-{index}",
                        "name": f"Unplaced {index}",
                        "section": "common",
                        "why": "no rule fixes a date",
                    }
                ],
                "span": {"first": 2020, "last": 2120},
            }
        )
        ordinary.append(
            {
                "absent": [
                    {
                        "count": 3,
                        "key": "witness-gap",
                        "kind": "witness-gap",
                        "state": "unavailable",
                    }
                ],
                "calendar": calendar,
                "elements": 3,
                "exclusions": [],
                "language_absences": [
                    {
                        "count": 1,
                        "key": "witness-gap",
                        "kind": "witness-gap",
                        "lang": "en",
                        "state": "unavailable",
                    },
                    {
                        "count": 2,
                        "key": "witness-gap",
                        "kind": "witness-gap",
                        "lang": "la",
                        "state": "unavailable",
                    },
                ],
                "language_coverage": [
                    {
                        "absent": 1,
                        "elements": 3,
                        "held": 2,
                        "lang": "en",
                        "missing": 1,
                    },
                    {
                        "absent": 2,
                        "elements": 3,
                        "held": 1,
                        "lang": "la",
                        "missing": 2,
                    },
                ],
                "relation_coverage": [
                    {
                        "collation": "not-applicable",
                        "count": 1,
                        "lang": "en",
                        "relation": "own",
                    },
                    {
                        "collation": "collated",
                        "count": 1,
                        "lang": "en",
                        "relation": "antecedent",
                    },
                    {
                        "collation": "uncollated",
                        "count": 1,
                        "lang": "la",
                        "relation": "antecedent",
                    },
                ],
                "witnesses": [],
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
        self.assertEqual(expected["lower_bound"], 3)
        self.assertEqual(expected["effective_celebrations"], 3)
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
        self.assertEqual(postconciliar["filled_text_slots"]["lower_bound"], 4)
        self.assertEqual(
            postconciliar["filled_text_slots"][
                "ordinary_target_edition_held_by_language"
            ],
            {"en": 1, "la": 0},
        )
        self.assertEqual(
            postconciliar["filled_text_slots"]["ordinary_relation_coverage"],
            [
                {
                    "collation": "collated",
                    "count": 1,
                    "lang": "en",
                    "relation": "antecedent",
                },
                {
                    "collation": "not-applicable",
                    "count": 1,
                    "lang": "en",
                    "relation": "own",
                },
                {
                    "collation": "uncollated",
                    "count": 1,
                    "lang": "la",
                    "relation": "antecedent",
                },
            ],
        )
        self.assertIsNone(postconciliar["filled_text_slots"]["count"])
        self.assertEqual(postconciliar["inherited_reference_slots"]["count"], 2)
        self.assertEqual(postconciliar["malformed_slots"]["lower_bound"], 1)
        self.assertEqual(postconciliar["orphan_texts"]["lower_bound"], 2)
        self.assertIsNone(postconciliar["unreachable_texts"]["count"])
        self.assertEqual(
            postconciliar["unreachable_texts"]["known_unplaced_masses"],
            {"declared": 0, "undeclared": 1},
        )

        pre_1955 = rows["roman-pre-1955"]["textual"]
        self.assertEqual(
            pre_1955["filled_text_slots"]["english"][
                "translation_ledger_calendars"
            ],
            ["roman-1962", "roman-pre-1955"],
        )
        self.assertTrue(
            pre_1955["filled_text_slots"]["english"][
                "translation_ledger_inherited"
            ]
        )

    def test_unresolved_common_choices_remain_typed_unknown_rows(self) -> None:
        report = REPORT.build_report(*fixture_reports())
        family = {row["calendar"]: row for row in report["families"]}[
            "roman-pre-1955"
        ]
        unknown = family["textual"]["unknown_slots"]
        self.assertEqual(unknown["lower_bound"], 1)
        self.assertEqual(
            unknown["known_counts"]["unresolved_common_set_selections"], 1
        )
        self.assertEqual(
            unknown["unresolved_common_set_selections"],
            [
                {
                    "candidates": ["c1", "c2"],
                    "group": "orations",
                    "mass": "unresolved-0",
                    "target": "common-demo",
                }
            ],
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

    def test_malformed_census_rows_are_refused(self) -> None:
        cases = (
            (
                "family row",
                lambda reports: reports[0]["calendars"].__setitem__(
                    "roman-1962", []
                ),
                "roman-1962 must be an object",
            ),
            (
                "rank row",
                lambda reports: reports[0]["calendars"]["roman-1962"][
                    "ranks"
                ].append("not-an-object"),
                "ranks\\[1\\] must be an object",
            ),
            (
                "rank label",
                lambda reports: reports[0]["calendars"]["roman-1962"][
                    "ranks"
                ][0].__setitem__("rank", []),
                "rank must be a non-empty string",
            ),
            (
                "rank fields",
                lambda reports: reports[0]["calendars"]["roman-1962"][
                    "ranks"
                ][0].__setitem__("legacy", 1),
                "fields are not exact",
            ),
            (
                "rank entries",
                lambda reports: reports[0]["calendars"]["roman-1962"][
                    "ranks"
                ][0].__setitem__("entries", "two"),
                "entries must be a non-negative integer",
            ),
            (
                "duplicate rank",
                lambda reports: reports[0]["calendars"]["roman-1962"][
                    "ranks"
                ].append(
                    dict(reports[0]["calendars"]["roman-1962"]["ranks"][0])
                ),
                "rank repeats",
            ),
            (
                "rank partition",
                lambda reports: reports[0]["calendars"]["roman-1962"][
                    "ranks"
                ][0].__setitem__("entries", 1),
                "does not partition its masses",
            ),
            (
                "resolution error row",
                lambda reports: reports[0]["finding_aid_coverage"][2][
                    "resolution_errors"
                ].append("not-an-object"),
                r"resolution_errors\[1\] must be an object",
            ),
        )
        for label, mutate, message in cases:
            with self.subTest(case=label):
                reports = copy.deepcopy(fixture_reports())
                mutate(reports)
                with self.assertRaisesRegex(REPORT.Refused, message):
                    REPORT.build_report(*reports)

    def test_missing_or_malformed_effective_celebration_count_is_refused(self) -> None:
        cases = (
            (
                "missing",
                lambda reports: reports[0]["finding_aid_coverage"][0].pop(
                    "effective_celebrations"
                ),
                "effective_celebrations must be a non-negative integer",
            ),
            (
                "not an integer",
                lambda reports: reports[0]["finding_aid_coverage"][0].__setitem__(
                    "effective_celebrations", "three"
                ),
                "effective_celebrations must be a non-negative integer",
            ),
            (
                "fewer than effective masses",
                lambda reports: reports[0]["finding_aid_coverage"][0].__setitem__(
                    "effective_celebrations", 1
                ),
                "cannot be less than effective mass rows",
            ),
        )
        for label, mutate, message in cases:
            with self.subTest(case=label):
                reports = copy.deepcopy(fixture_reports())
                mutate(reports)
                with self.assertRaisesRegex(REPORT.Refused, message):
                    REPORT.build_report(*reports)

    def test_missing_or_malformed_common_selection_rows_are_refused(self) -> None:
        cases = (
            (
                "missing array",
                lambda row: row.pop("unresolved_common_set_selections"),
                "unresolved_common_set_selections must be an array",
            ),
            (
                "row",
                lambda row: row["unresolved_common_set_selections"].__setitem__(
                    0, "not-an-object"
                ),
                r"unresolved_common_set_selections\[0\] must be an object",
            ),
            (
                "exact fields",
                lambda row: row["unresolved_common_set_selections"][0].__setitem__(
                    "state", "unresolved"
                ),
                "fields are not exact",
            ),
            (
                "identity",
                lambda row: row["unresolved_common_set_selections"][0].__setitem__(
                    "mass", ""
                ),
                "mass must be a non-empty string",
            ),
            (
                "candidate array",
                lambda row: row["unresolved_common_set_selections"][0].__setitem__(
                    "candidates", []
                ),
                "candidates must contain at least two unique non-empty strings",
            ),
            (
                "duplicate candidate",
                lambda row: row["unresolved_common_set_selections"][0].__setitem__(
                    "candidates", ["c1", "c1"]
                ),
                "candidates must contain at least two unique non-empty strings",
            ),
            (
                "duplicate selection",
                lambda row: row["unresolved_common_set_selections"].append(
                    copy.deepcopy(row["unresolved_common_set_selections"][0])
                ),
                "repeats Common selection",
            ),
        )
        for label, mutate, message in cases:
            with self.subTest(case=label):
                reports = copy.deepcopy(fixture_reports())
                mutate(reports[0]["finding_aid_coverage"][0])
                with self.assertRaisesRegex(REPORT.Refused, message):
                    REPORT.build_report(*reports)

    def test_missing_or_malformed_translation_ledger_provenance_is_refused(
        self,
    ) -> None:
        cases = (
            (
                "missing owner",
                lambda row: row.pop("translation_ledger_calendar"),
                "translation_ledger_calendar must be a non-empty string",
            ),
            (
                "owner chain",
                lambda row: row.__setitem__("translation_ledger_calendars", {}),
                "translation_ledger_calendars must be a non-empty unique string array",
            ),
            (
                "duplicate owner",
                lambda row: row.__setitem__(
                    "translation_ledger_calendars",
                    ["roman-1962", "roman-1962"],
                ),
                "translation_ledger_calendars must be a non-empty unique string array",
            ),
            (
                "nearest owner",
                lambda row: row.__setitem__(
                    "translation_ledger_calendar", "roman-1962"
                ),
                "must name the last ledger",
            ),
            (
                "inherited type",
                lambda row: row.__setitem__("translation_ledger_inherited", "true"),
                "translation_ledger_inherited must be a boolean",
            ),
            (
                "inherited consistency",
                lambda row: row.__setitem__("translation_ledger_inherited", False),
                "translation_ledger_inherited is inconsistent",
            ),
        )
        for label, mutate, message in cases:
            with self.subTest(case=label):
                reports = copy.deepcopy(fixture_reports())
                mutate(reports[0]["english_coverage"][0])
                with self.assertRaisesRegex(REPORT.Refused, message):
                    REPORT.build_report(*reports)

    def test_real_corpus_preserves_effective_common_and_ledger_evidence(self) -> None:
        report = REPORT.build_report(*REPORT.owning_reports())
        families = {row["calendar"]: row for row in report["families"]}

        pre_1955 = families["roman-pre-1955"]
        expected = pre_1955["structural"]["expected_celebrations"]
        self.assertEqual(expected["effective_celebrations"], 490)
        self.assertEqual(expected["effective_mass_rows"], 489)
        self.assertEqual(expected["lower_bound"], 490)

        pre_unknown = pre_1955["textual"]["unknown_slots"]
        roman_unknown = families["roman-1962"]["textual"]["unknown_slots"]
        post_unknown = families["postconciliar"]["textual"]["unknown_slots"]
        self.assertEqual(pre_unknown["lower_bound"], 7)
        self.assertEqual(roman_unknown["lower_bound"], 7)
        self.assertEqual(post_unknown["lower_bound"], 0)
        self.assertEqual(len(pre_unknown["unresolved_common_set_selections"]), 7)
        for row in pre_unknown["unresolved_common_set_selections"]:
            self.assertEqual(set(row), {"mass", "target", "group", "candidates"})

        english = pre_1955["textual"]["filled_text_slots"]["english"]
        self.assertEqual(english["with_english"], 86)
        self.assertEqual(
            english["translation_ledger_calendars"],
            ["roman-1962", "roman-pre-1955"],
        )
        self.assertEqual(
            english["translation_ledger_calendar"], "roman-pre-1955"
        )
        self.assertTrue(english["translation_ledger_inherited"])

    def test_malformed_ordinary_language_rows_are_refused(self) -> None:
        cases = (
            (
                "legacy alias",
                lambda row: row.__setitem__(
                    "languages", row.pop("language_coverage")
                ),
                "fields are not exact",
            ),
            (
                "witness array",
                lambda row: row.__setitem__("witnesses", {}),
                "witnesses must be an array",
            ),
            (
                "row",
                lambda row: row["language_coverage"].__setitem__(0, []),
                r"language_coverage\[0\] must be an object",
            ),
            (
                "fields",
                lambda row: row["language_coverage"][0].__setitem__("legacy", 1),
                "fields are not exact",
            ),
            (
                "lang",
                lambda row: row["language_coverage"][0].__setitem__("lang", None),
                "lang must be a non-empty string",
            ),
            (
                "duplicate",
                lambda row: row["language_coverage"][1].__setitem__("lang", "en"),
                "lang repeats",
            ),
            (
                "universe",
                lambda row: row["language_coverage"][0].__setitem__("elements", 4),
                "does not match its target-recension universe",
            ),
            (
                "partition",
                lambda row: row["language_coverage"][0].__setitem__("held", 1),
                "does not partition elements",
            ),
            (
                "absent",
                lambda row: row["language_coverage"][0].__setitem__("absent", 0),
                "absent does not equal missing",
            ),
        )
        for label, mutate, message in cases:
            with self.subTest(case=label):
                reports = copy.deepcopy(fixture_reports())
                mutate(reports[2]["coverage"][1])
                with self.assertRaisesRegex(REPORT.Refused, message):
                    REPORT.build_report(*reports)

    def test_malformed_ordinary_relation_rows_are_refused(self) -> None:
        cases = (
            (
                "row",
                lambda row: row["relation_coverage"].__setitem__(0, []),
                r"relation_coverage\[0\] must be an object",
            ),
            (
                "relation",
                lambda row: row["relation_coverage"][0].__setitem__(
                    "relation", "borrowed"
                ),
                "relation must be own or antecedent",
            ),
            (
                "own collation",
                lambda row: row["relation_coverage"][0].__setitem__(
                    "collation", "collated"
                ),
                "own text must use not-applicable collation",
            ),
            (
                "antecedent collation",
                lambda row: row["relation_coverage"][1].__setitem__(
                    "collation", []
                ),
                "antecedent text must be collated or uncollated",
            ),
            (
                "unknown language",
                lambda row: row["relation_coverage"][0].__setitem__("lang", "fr"),
                "lang must name a covered language",
            ),
            (
                "duplicate",
                lambda row: row["relation_coverage"].append(
                    dict(row["relation_coverage"][0])
                ),
                "repeats relation bucket",
            ),
            (
                "zero count",
                lambda row: row["relation_coverage"][0].__setitem__("count", 0),
                "count must be positive",
            ),
            (
                "partition",
                lambda row: row["relation_coverage"][0].__setitem__("count", 2),
                "relation buckets do not partition held elements",
            ),
        )
        for label, mutate, message in cases:
            with self.subTest(case=label):
                reports = copy.deepcopy(fixture_reports())
                mutate(reports[2]["coverage"][1])
                with self.assertRaisesRegex(REPORT.Refused, message):
                    REPORT.build_report(*reports)

    def test_malformed_ordinary_absence_rows_are_refused(self) -> None:
        cases = (
            (
                "typed state",
                lambda row: row["absent"][0].__setitem__(
                    "state", "rights-restricted"
                ),
                "state is inconsistent with kind",
            ),
            (
                "language row",
                lambda row: row["language_absences"].__setitem__(0, []),
                r"language_absences\[0\] must be an object",
            ),
            (
                "language type",
                lambda row: row["language_absences"][0].__setitem__(
                    "kind", "no-exemplar"
                ),
                "does not retain its absence type",
            ),
            (
                "duplicate language row",
                lambda row: row["language_absences"].append(
                    dict(row["language_absences"][0])
                ),
                "repeats language absence",
            ),
            (
                "absence partition",
                lambda row: row["absent"][0].__setitem__("count", 4),
                "language counts do not partition its count",
            ),
            (
                "zero language count",
                lambda row: row["language_absences"][0].__setitem__("count", 0),
                "count must be positive",
            ),
            (
                "language partition",
                lambda row: (
                    row["language_absences"][0].__setitem__("count", 2),
                    row["language_absences"][1].__setitem__("count", 1),
                ),
                "absence counts do not partition missing elements",
            ),
        )
        for label, mutate, message in cases:
            with self.subTest(case=label):
                reports = copy.deepcopy(fixture_reports())
                mutate(reports[2]["coverage"][1])
                with self.assertRaisesRegex(REPORT.Refused, message):
                    REPORT.build_report(*reports)

    def test_typed_ordinary_unresolved_absence_is_preserved(self) -> None:
        reports = copy.deepcopy(fixture_reports())
        ordinary = reports[2]["coverage"][2]
        ordinary["absent"][0]["kind"] = "rights-unresolved"
        ordinary["absent"][0]["state"] = "unresolved"
        for row in ordinary["language_absences"]:
            row["kind"] = "rights-unresolved"
            row["state"] = "unresolved"
        family = REPORT.build_report(*reports)["families"][2]
        self.assertEqual(
            family["provenance"]["rights_pending_texts"]["ordinary_absences"],
            [
                {
                    "count": 3,
                    "key": "witness-gap",
                    "kind": "rights-unresolved",
                    "state": "unresolved",
                }
            ],
        )

    def test_malformed_ordinary_exclusion_rows_are_refused(self) -> None:
        valid = {
            "basis": "the row is outside the target recension",
            "evidence": [
                {
                    "artifact_id": "artifact.example",
                    "element": "older-only-row",
                    "lang": "en",
                    "relation": "own",
                    "source_id": "edition.example",
                }
            ],
            "key": "section/older-only-row",
            "sources": ["edition.example"],
            "state": "not-in-target-recension",
        }
        reports = copy.deepcopy(fixture_reports())
        reports[2]["coverage"][0]["exclusions"].append(copy.deepcopy(valid))
        report = REPORT.build_report(*reports)
        self.assertEqual(
            report["families"][0]["textual"]["expected_text_slots"][
                "ordinary_exclusions"
            ],
            [valid],
        )

        cases = (
            (
                "row",
                lambda rows: rows.__setitem__(0, []),
                r"exclusions\[0\] must be an object",
            ),
            (
                "state",
                lambda rows: rows[0].__setitem__("state", "unavailable"),
                "state must be not-in-target-recension",
            ),
            (
                "sources",
                lambda rows: rows[0].__setitem__("sources", []),
                "sources must be a non-empty sorted unique string array",
            ),
            (
                "evidence row",
                lambda rows: rows[0]["evidence"].__setitem__(0, []),
                r"evidence\[0\] must be an object",
            ),
            (
                "own extras",
                lambda rows: rows[0]["evidence"][0].__setitem__(
                    "collation", "not-applicable"
                ),
                "own relation has inapplicable fields",
            ),
            (
                "source identity mismatch",
                lambda rows: rows[0].__setitem__("sources", ["edition.other"]),
                "do not exactly name the evidence source_id values",
            ),
        )
        for label, mutate, message in cases:
            with self.subTest(case=label):
                reports = copy.deepcopy(fixture_reports())
                rows = reports[2]["coverage"][0]["exclusions"]
                rows.append(copy.deepcopy(valid))
                mutate(rows)
                with self.assertRaisesRegex(REPORT.Refused, message):
                    REPORT.build_report(*reports)

    def test_malformed_placement_rows_are_refused(self) -> None:
        cases = (
            (
                "row",
                lambda rows: rows.append("not-an-object"),
                "masses_never_placed\\[1\\] must be an object",
            ),
            (
                "key",
                lambda rows: rows[0].__setitem__("key", []),
                "key must be a non-empty string",
            ),
            (
                "fields",
                lambda rows: rows[0].pop("why"),
                "fields are not exact",
            ),
            (
                "name",
                lambda rows: rows[0].__setitem__("name", []),
                "name must be a non-empty string",
            ),
            (
                "declared",
                lambda rows: rows[0].__setitem__("declared", "false"),
                "declared must be a boolean",
            ),
            (
                "duplicate",
                lambda rows: rows.append(dict(rows[0])),
                "key repeats",
            ),
        )
        for label, mutate, message in cases:
            with self.subTest(case=label):
                reports = copy.deepcopy(fixture_reports())
                mutate(reports[1]["coverage"][1]["masses_never_placed"])
                with self.assertRaisesRegex(REPORT.Refused, message):
                    REPORT.build_report(*reports)

        for span, message in (
            ([], "span must be an object"),
            ({"first": 2020, "last": 2120, "extra": 1}, "fields are not exact"),
            ({"first": 2021, "last": 2120}, "expected 2020-2120"),
        ):
            with self.subTest(span=span):
                reports = copy.deepcopy(fixture_reports())
                reports[1]["coverage"][1]["span"] = span
                with self.assertRaisesRegex(REPORT.Refused, message):
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
