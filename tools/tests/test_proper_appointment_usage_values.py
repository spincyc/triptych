"""Closed source usage maps preserve applicability obligations for the runtime."""
from __future__ import annotations

import copy
import importlib.machinery
import importlib.util
import itertools
import os
from pathlib import Path
import sys
import unittest
from unittest.mock import patch

ROOT = Path(os.environ.get("TRIPTYCH_REVIEW_ROOT", Path(__file__).resolve().parents[2]))
MODULE_ROOT = Path(os.environ.get("TRIPTYCH_USAGE_FACT_MODULE_ROOT", ROOT))
sys.path.insert(0, str(ROOT / "scripts"))
sys.path.insert(0, str(MODULE_ROOT / "scripts"))
import _calendars as C

loader = importlib.machinery.SourceFileLoader("_usage_fact_checker", str(MODULE_ROOT / "tools/check-calendar-masses"))
spec = importlib.util.spec_from_loader(loader.name, loader)
CHECK = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = CHECK
loader.exec_module(CHECK)

EDITION = "roman-1962"
BASIS = "Technical closed source usage fixture; no calendar or historical rule is asserted."
FACT = "fixture-use"


def facts():
    return {FACT: {"edition": EDITION, "values": ["active", "inactive"], "basis": BASIS, "usage_values": {"own-sunday": "active", "borrowed-feria": "inactive"}}}


def fixture():
    mass = {"key": "fixture", "name": "Technical usage fixture", "registry": "fixture", "season": "advent", "propers": [{"name": "Alleluia", "source": "composed", "text": "Technical source-owned body.", "ordinary_disposition": {"kind": "conditional", "group": "fixture-alleluia", "basis": BASIS, "when": {"fact": FACT, "in": ["active"]}}}]}
    return {"calendar": EDITION, "proper_appointment_facts": facts(), "sections": {"seasonal": {"kind": "seasonal", "masses": [mass]}}}


class ProperAppointmentUsageFactTests(unittest.TestCase):
    def test_closed_usage_map_round_trips_arbitrary_declared_enum_values(self):
        value = facts(); snapshot = copy.deepcopy(value)
        self.assertIs(C.validate_proper_appointment_facts(value, EDITION), value)
        self.assertEqual(value, snapshot)
        # Source standing does not prescribe the enum vocabulary or outcomes.
        value[FACT]["usage_values"]["borrowed-feria"] = "active"
        self.assertEqual(C.validate_proper_appointment_facts(value, EDITION), value)

    def test_exactly_one_of_three_selectors_is_required(self):
        selectors = {"usage_values": {"own-sunday": "active", "borrowed-feria": "inactive"}, "season_values": {"advent": "active"}, "mass_values": {"fixture": {"value": "active", "basis": BASIS}}}
        for count in (0, 2, 3):
            for names in itertools.combinations(selectors, count):
                fact = {"edition": EDITION, "values": ["active", "inactive"], "basis": BASIS, **{name: selectors[name] for name in names}}
                with self.subTest(selectors=names), self.assertRaises(ValueError):
                    C.validate_proper_appointment_facts({FACT: fact}, EDITION)

    def test_both_usage_keys_are_required_and_unknown_or_default_keys_refuse(self):
        for usages in ({}, None, [], {"own-sunday": "active"}, {"borrowed-feria": "inactive"}, {"own-sunday": "active", "borrowed-feria": "inactive", "unknown": "active"}, {"own-sunday": "active", "borrowed-feria": "inactive", "default": "active"}, {"*": "active"}, {"Own Sunday": "active", "borrowed-feria": "inactive"}):
            value = facts(); value[FACT]["usage_values"] = usages
            with self.subTest(usages=usages), self.assertRaises(ValueError):
                C.validate_proper_appointment_facts(value, EDITION)

    def test_usage_values_are_direct_declared_strings_without_null_unknown(self):
        for answer in (None, True, 1, {}, ["active"], "unheld", {"value": "active", "basis": BASIS}):
            value = facts(); value[FACT]["usage_values"]["own-sunday"] = answer
            with self.subTest(answer=answer), self.assertRaises(ValueError):
                C.validate_proper_appointment_facts(value, EDITION)

    def test_envelope_edition_basis_values_and_unknown_fields_still_refuse(self):
        for mutate in (lambda f: f.update(edition="foreign"), lambda f: f.update(basis=""), lambda f: f.update(values=[]), lambda f: f.update(values=["active", "active"]), lambda f: f.update(default="active")):
            value = facts(); mutate(value[FACT])
            with self.subTest(value=value), self.assertRaises(ValueError):
                C.validate_proper_appointment_facts(value, EDITION)

    def test_existing_season_and_mass_facts_coexist_without_reinterpretation(self):
        source = fixture(); value = source["proper_appointment_facts"]
        value["fixture-season"] = {"edition": EDITION, "values": ["active", "inactive"], "basis": BASIS, "season_values": {"advent": "active", "unsettled": None}}
        value["fixture-subject"] = {"edition": EDITION, "values": ["active", "inactive"], "basis": BASIS, "mass_values": {"fixture": {"value": "active", "basis": BASIS}}}
        snapshot = copy.deepcopy(source)
        self.assertIs(C.validate_proper_appointment_facts(value, EDITION, document=source), value)
        self.assertEqual(source, snapshot)
        value["fixture-subject"]["mass_values"]["unheld-key"] = {"value": "active", "basis": BASIS}
        with self.assertRaisesRegex(ValueError, "unheld source Mass"):
            C.validate_proper_appointment_facts(value, EDITION, document=source)

    def test_source_checker_and_resolver_validate_without_deriving_usage(self):
        for invalid in (False, True):
            source = fixture()
            if invalid: source["proper_appointment_facts"][FACT]["usage_values"]["default"] = "active"
            mass = C.mass_index(source)["fixture"]
            rows, problems = C.resolve_propers(source, mass, appointments=True)
            self.assertEqual(bool(problems), invalid)
            checked = []
            with patch.object(CHECK, "read_yaml", return_value=source):
                CHECK.check_file(ROOT / ".scratch/technical-usage-fact-source.yaml", checked)
            self.assertEqual(any("usage_values" in problem for problem in checked), invalid)
            if not invalid:
                self.assertEqual(len(rows), 1)
                self.assertEqual(rows[0][1]["text"], mass["propers"][0]["text"])
                self.assertEqual(rows[0][1]["ordinary_disposition"]["when"], {"fact": FACT, "in": ["active"]})
                self.assertNotIn("usage", source)
                self.assertNotIn("selected", rows[0][1])

    def test_foreign_multihop_preserves_unsupported_marker_and_raw_body(self):
        source = fixture(); snapshot = copy.deepcopy(source)
        middle = C._apply_departures({"calendar": "foreign-middle", "sections": {}}, source, EDITION)
        target = C._apply_departures({"calendar": "foreign-target", "sections": {}}, middle, "foreign-middle")
        self.assertNotIn("proper_appointment_facts", middle)
        self.assertNotIn("proper_appointment_facts", target)
        rows, problems = C.resolve_propers(target, C.mass_index(target)["fixture"], appointments=True)
        self.assertEqual(problems, [])
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0][1]["text"], C.mass_index(source)["fixture"]["propers"][0]["text"])
        self.assertNotIn("ordinary_disposition", rows[0][1])
        marker = rows[0][1]["appointment_applicability"]
        self.assertEqual((marker["source_edition"], marker["target_edition"]), (EDITION, "foreign-target"))
        self.assertEqual(source, snapshot)


if __name__ == "__main__":
    unittest.main()
