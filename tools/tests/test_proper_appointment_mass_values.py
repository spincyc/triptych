"""Closed source Mass fact bindings do not become a second applicability resolver."""
from __future__ import annotations

import copy
import importlib.machinery
import importlib.util
import json
import os
from pathlib import Path
import sys
import unittest
from unittest.mock import patch

ROOT = Path(os.environ.get("TRIPTYCH_REVIEW_ROOT", Path(__file__).resolve().parents[2]))
MODULE_ROOT = Path(os.environ.get("TRIPTYCH_MASS_FACT_MODULE_ROOT", ROOT))
sys.path.insert(0, str(ROOT / "scripts"))
sys.path.insert(0, str(MODULE_ROOT / "scripts"))
import _calendars as C

loader = importlib.machinery.SourceFileLoader("_mass_fact_checker", str(MODULE_ROOT / "tools/check-calendar-masses"))
spec = importlib.util.spec_from_loader(loader.name, loader)
CHECK = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = CHECK
loader.exec_module(CHECK)

EDITION = "roman-1962"
BASIS = "Technical exact source Mass binding fixture; no historical classification is asserted."
FACT = "fixture-subject"


def facts():
    return {FACT: {"edition": EDITION, "values": ["general", "widow"], "basis": BASIS,
                   "mass_values": {"fixture-general": {"value": "general", "basis": BASIS},
                                   "fixture-widow": {"value": "widow", "basis": BASIS}}}}


def fixture():
    masses = [{"key": key, "name": "Technical " + key, "registry": key, "propers": [{"name": "Gradual", "source": "composed", "text": "Technical source-owned body.", "ordinary_disposition": {"kind": "conditional", "group": "subject-gradual", "basis": BASIS, "when": {"fact": FACT, "in": ["widow"]}}}]} for key in ("fixture-general", "fixture-widow", "fixture-unbound")]
    return {"calendar": EDITION, "proper_appointment_facts": facts(), "sections": {"common": {"kind": "common", "masses": masses}}}


class ProperAppointmentMassFactTests(unittest.TestCase):
    def test_exact_source_mass_bindings_round_trip_without_mutation(self):
        source = fixture(); value = source["proper_appointment_facts"]
        snapshot = copy.deepcopy(source)
        self.assertIs(C.validate_proper_appointment_facts(value, EDITION), value)
        self.assertIs(C.validate_proper_appointment_facts(value, EDITION, document=source), value)
        self.assertEqual(source, snapshot)

    def test_exactly_one_selector_is_required(self):
        for selector in ("both", "neither", "usage_values"):
            value = facts(); fact = value[FACT]
            if selector == "both": fact["season_values"] = {"lent": "general"}
            elif selector == "neither": fact.pop("mass_values")
            else: fact["usage_values"] = fact.pop("mass_values")
            with self.subTest(selector=selector), self.assertRaises(ValueError):
                C.validate_proper_appointment_facts(value, EDITION)

    def test_mass_binding_shape_values_and_basis_are_closed(self):
        for binding in (None, "widow", {}, {"value": "widow"}, {"value": "widow", "basis": ""}, {"value": "widow", "basis": None}, {"value": None, "basis": BASIS}, {"value": "unheld", "basis": BASIS}, {"value": "widow", "basis": BASIS, "default": True}):
            value = facts(); value[FACT]["mass_values"]["fixture-widow"] = binding
            with self.subTest(binding=binding), self.assertRaises(ValueError):
                C.validate_proper_appointment_facts(value, EDITION)

    def test_selector_mapping_and_source_keys_cannot_be_labels_or_wildcards(self):
        for bindings in ({}, None, [], {"Widow Label": {"value": "widow", "basis": BASIS}}, {"*": {"value": "general", "basis": BASIS}}, {1: {"value": "general", "basis": BASIS}}):
            value = facts(); value[FACT]["mass_values"] = bindings
            with self.subTest(bindings=bindings), self.assertRaises(ValueError):
                C.validate_proper_appointment_facts(value, EDITION)

    def test_source_mass_landing_requires_the_available_document(self):
        source = fixture(); value = facts()
        value[FACT]["mass_values"]["unheld-source-key"] = {"value": "widow", "basis": BASIS}
        # The producer has a legitimate shape-only two-argument call.
        self.assertEqual(C.validate_proper_appointment_facts(value, EDITION), value)
        with self.assertRaisesRegex(ValueError, "unheld source Mass"):
            C.validate_proper_appointment_facts(value, EDITION, document=source)

    def test_resolver_and_checker_pass_the_full_source_document(self):
        for invalid in (False, True):
            source = fixture()
            if invalid:
                source["proper_appointment_facts"][FACT]["mass_values"]["unheld-source-key"] = {"value": "widow", "basis": BASIS}
            _, problems = C.resolve_propers(source, C.mass_index(source)["fixture-widow"])
            self.assertEqual(any("unheld source Mass" in problem for problem in problems), invalid)
            checked = []
            with patch.object(CHECK, "read_yaml", return_value=source):
                CHECK.check_file(ROOT / ".scratch/technical-mass-fact-source.yaml", checked)
            self.assertEqual(any("unheld source Mass" in problem for problem in checked), invalid)

    def test_unbound_current_mass_remains_unresolved_without_python_inference(self):
        source = fixture(); snapshot = copy.deepcopy(source)
        raw = C.mass_index(source)["fixture-unbound"]
        rows, problems = C.resolve_propers(source, raw, appointments=True)
        self.assertEqual(problems, [])
        self.assertEqual(rows[0][1]["ordinary_disposition"]["when"], {"fact": FACT, "in": ["widow"]})
        self.assertNotIn("fixture-unbound", source["proper_appointment_facts"][FACT]["mass_values"])
        self.assertEqual(source, snapshot)
        self.assertEqual(rows[0][1]["text"], raw["propers"][0]["text"])

    def test_edition_value_enum_and_global_basis_guards_still_apply(self):
        for mutate in (lambda f: f.update(edition="foreign"), lambda f: f.update(values=[]), lambda f: f.update(values=["widow", "widow"]), lambda f: f.update(basis=""), lambda f: f.update(extra="unknown")):
            value = facts(); mutate(value[FACT])
            with self.subTest(value=value), self.assertRaises(ValueError):
                C.validate_proper_appointment_facts(value, EDITION)

    def test_existing_season_selector_and_null_unknown_are_unchanged(self):
        season = {"fixture-season": {"edition": EDITION, "values": ["general", "widow"], "basis": BASIS, "season_values": {"lent": "general", "unsettled": None}}}
        self.assertIs(C.validate_proper_appointment_facts(season, EDITION), season)
        for invalid in ({}, [], {"lent": "unheld"}, {"Wrong Label": "general"}):
            bad = copy.deepcopy(season); bad["fixture-season"]["season_values"] = invalid
            with self.subTest(invalid=invalid), self.assertRaises(ValueError):
                C.validate_proper_appointment_facts(bad, EDITION)
        source = fixture(); source["proper_appointment_facts"].update(season)
        self.assertEqual(C.resolve_propers(source, C.mass_index(source)["fixture-widow"])[1], [])

    def test_foreign_multihop_does_not_inherit_or_relabel_source_bindings(self):
        source = fixture(); snapshot = copy.deepcopy(source)
        middle = C._apply_departures({"calendar": "foreign-middle", "sections": {}}, source, EDITION)
        target = C._apply_departures({"calendar": "foreign-target", "sections": {}}, middle, "foreign-middle")
        self.assertNotIn("proper_appointment_facts", middle)
        self.assertNotIn("proper_appointment_facts", target)
        for key, raw in C.mass_index(source).items():
            rows, problems = C.resolve_propers(target, C.mass_index(target)[key], appointments=True)
            self.assertEqual(problems, [])
            self.assertEqual(len(rows), 1)
            marker = rows[0][1]["appointment_applicability"]
            self.assertEqual((marker["source_edition"], marker["target_edition"]), (EDITION, "foreign-target"))
            self.assertEqual(rows[0][1]["text"], raw["propers"][0]["text"])
            self.assertNotIn("ordinary_disposition", rows[0][1])
        self.assertEqual(source, snapshot)
        self.assertNotIn("mass_values", json.dumps(target))


if __name__ == "__main__":
    unittest.main()
