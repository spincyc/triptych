"""Daily readiness is not the structural complete-year gate or a body count."""
from __future__ import annotations

import copy
import importlib.machinery
import importlib.util
import itertools
import json
from pathlib import Path
import sys
import unittest
from unittest import mock

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))
from _missal_coverage import summarize, unit
from _missal_readiness import CALENDARS, CYCLE_YEARS, build_readiness
from tools.tests.test_complete_missal_report import REPORT, fixture_reports


def body(*, identity="target", occurrence="use", english="study", latin=True):
    owner = {"translations": []}
    if latin:
        owner.update(text="Synthetic Latin body", latin={
            "provenance": {"status": "collated", "relationship": "editorial-projection-exact-to-target"},
            "publication": {"status": "permitted", "basis": "public-domain"},
        })
    if english:
        owner["translations"] = [{
            "lang": "en", "text": "Synthetic English body",
            "rights": "project-created" if english == "study" else "public-domain",
            "source_id": "" if english == "study" else "edition.historical",
            "witness_relation": "antecedent" if english == "historical" else None,
        }]
    return unit(owner, target_id=identity, occurrence_id=occurrence)


def composed(units=None):
    report = REPORT.build_report(*fixture_reports())
    units = [body()] if units is None else units
    report["coverage"] = []
    for calendar in CALENDARS:
        proper = summarize(units, "calendar")
        proper["expected_inventory"] = {
            "whole_inventory_state": "unresolved", "target_states": {"represented": len(units)},
            "boundaries": [{"id": "unmodeled-options", "state": "unenumerated"}],
            "not_represented": [],
        }
        report["coverage"].append({"calendar": calendar, "propers": proper,
                                   "ordinary": summarize([body()], "ordinary")})
    return report


class DailyReadinessTests(unittest.TestCase):
    def test_held_bodies_and_structural_success_do_not_prove_execution(self):
        source = composed()
        source["check"]["resolved"] = True
        source["complete"] = True
        source["status"] = "ready"
        report = build_readiness(source)
        self.assertFalse(report["ready"])
        self.assertEqual(report["status"], "unresolved")
        for family in report["calendars"]:
            self.assertEqual(family["execution_extent"]["state"], "unresolved")
            self.assertIn("conclusion-free texts are not presumed incomplete",
                          family["execution_extent"]["per_target_classification"])
        self.assertFalse(report["scope"]["runtime_executed"])

    def test_study_english_is_allowed_and_not_claimed_approved_or_reviewed(self):
        family = build_readiness(composed())["calendars"][0]
        english = family["source_inventory"]["propers"][0]
        self.assertEqual(english["available_targets"], 1)
        self.assertEqual(english["relationship_occurrences"]["study-translation"], 1)
        self.assertEqual(english["exact_target_targets"], 0)
        self.assertFalse(family["english_policy"]["approved_liturgical_translation_required"])
        self.assertEqual(family["english_policy"]["study_translations"], "source-admitted-study-translations-with-visible-qualification")
        self.assertEqual(family["english_policy"]["fidelity_review"]["state"], "unresolved")

    def test_historical_english_is_kept_distinct_from_target_fidelity(self):
        family = build_readiness(composed([body(english="historical")]))["calendars"][0]
        english, latin = family["source_inventory"]["propers"]
        self.assertEqual(english["relationship_occurrences"]["historical-antecedent"], 1)
        self.assertEqual(english["exact_target_targets"], 0)
        self.assertEqual(latin["exact_target_targets"], 1)

    def test_missing_english_cannot_be_hidden_by_held_latin(self):
        report = build_readiness(composed([body(english=None)]))
        self.assertEqual(report["status"], "incomplete")
        english, latin = report["calendars"][0]["source_inventory"]["propers"]
        self.assertEqual(english["unavailable_targets"], 1)
        self.assertEqual(latin["unavailable_targets"], 0)

    def test_repeated_appointments_do_not_inflate_source_targets(self):
        family = build_readiness(composed([
            body(occurrence="use-1"), body(occurrence="use-2"),
        ]))["calendars"][0]
        for lang in family["source_inventory"]["propers"]:
            self.assertEqual((lang["targets"], lang["occurrences"]), (1, 2))
            self.assertEqual((lang["available_targets"], lang["available_occurrences"]), (1, 2))

    def test_multiple_witnesses_do_not_inflate_available_targets(self):
        one = unit({"translations": [
            {"lang": "en", "source_id": f"edition.{number}", "text": "Synthetic English",
             "rights": "public-domain", "witness_relation": "antecedent"}
            for number in (1, 2)
        ]}, target_id="target", occurrence_id="use")
        english = build_readiness(composed([one]))["calendars"][0]["source_inventory"]["propers"][0]
        self.assertEqual(english["available_targets"], 1)
        self.assertEqual(len(english["witnesses"]), 2)

    def test_scripture_delegation_is_not_silently_dropped_from_scope(self):
        one = unit({"source": "scripture"}, target_id="scripture", occurrence_id="use")
        family = build_readiness(composed([one]))["calendars"][0]
        for lang in family["source_inventory"]["propers"]:
            self.assertEqual(lang["scripture_targets"], 1)
            self.assertEqual(lang["targets"], 0)
        self.assertEqual(family["scripture_execution"]["state"], "unresolved")

    def test_actual_missing_source_ids_and_choice_limits_remain_actionable(self):
        source = composed()
        missing = {"id": "calendar:mass:prayer", "kind": "text-slot", "slice_id": "source-slice"}
        source["coverage"][0]["propers"]["expected_inventory"]["not_represented"] = [missing]
        family = build_readiness(source)["calendars"][0]
        self.assertEqual(family["status"], "incomplete")
        self.assertEqual(family["expected_universe"]["not_represented"], [missing])
        self.assertFalse(family["choice_space"]["caller_choice_required_is_a_source_gap"])
        self.assertTrue(family["choice_space"]["unresolved_common_selections"])

    def test_report_is_read_only_and_does_not_retain_prayer_bodies(self):
        source = composed()
        before = copy.deepcopy(source)
        report = build_readiness(source)
        self.assertEqual(source, before)
        self.assertNotIn("Synthetic Latin body", json.dumps(report))
        self.assertNotIn("Synthetic English body", json.dumps(report))

    def test_absent_typed_report_is_unknown_not_an_empty_complete_book(self):
        report = build_readiness(REPORT.build_report(*fixture_reports()))
        self.assertFalse(report["ready"])
        self.assertEqual(report["status"], "unresolved")
        for family in report["calendars"]:
            self.assertEqual(family["source_inventory"]["reason"], "typed-coverage-not-reported")

    def test_malformed_owner_counts_are_refused(self):
        source = composed()
        source["coverage"][0]["propers"]["languages"][0]["available_targets"] += 1
        with self.assertRaises(ValueError):
            build_readiness(source)

    def test_cli_readiness_gate_is_distinct_and_nonzero_while_unresolved(self):
        with mock.patch.object(REPORT, "owning_reports", return_value=fixture_reports()), \
                mock.patch.object(REPORT, "print_json") as output:
            status = REPORT.main(["--readiness", "--require-resolved", "--json"])
        self.assertEqual(status, 1)
        self.assertEqual(output.call_args.args[0]["schema"], "triptych-daily-missal-readiness/v1")

    def test_six_year_contract_covers_the_joint_cycles_using_the_calendar_owner(self):
        loader = importlib.machinery.SourceFileLoader("readiness_calendar_owner", str(ROOT / "tools/calendar-days"))
        spec = importlib.util.spec_from_loader(loader.name, loader)
        calendar = importlib.util.module_from_spec(spec)
        sys.modules[loader.name] = calendar
        loader.exec_module(calendar)
        for ending, sunday, weekday in CYCLE_YEARS:
            self.assertEqual((calendar.sunday_cycle(ending), calendar.weekday_cycle(ending)), (sunday, weekday))
            start, end = calendar.first_sunday_of_advent(ending - 1), calendar.first_sunday_of_advent(ending)
            self.assertIn((end - start).days, {364, 371})
        required = set(itertools.product("ABC", ("I", "II")))
        self.assertEqual({(sunday, weekday) for _, sunday, weekday in CYCLE_YEARS}, required)
        self.assertNotEqual({(sunday, weekday) for _, sunday, weekday in CYCLE_YEARS[:3]}, required)


if __name__ == "__main__":
    unittest.main()
