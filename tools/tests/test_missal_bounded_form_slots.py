"""A source slice may establish appointed slots without closing a whole Mass."""
from __future__ import annotations

import copy
import importlib.machinery
import importlib.util
import json
from pathlib import Path
import sys
import unittest


ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))
from _missal_coverage import bounded_form_text_slots, expectations


def mass_propers():
    loader = importlib.machinery.SourceFileLoader("bounded_mass_propers", str(ROOT / "tools/mass-propers"))
    spec = importlib.util.spec_from_loader(loader.name, loader)
    module = importlib.util.module_from_spec(spec)
    loader.exec_module(module)
    return module


def pentecost(rows):
    return next(row for row in rows if row["mass"] == "pentecost" and row["form"] == "main")


class BoundedFormSlotTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        propers = mass_propers()
        cls.masses = [mass for _, mass in propers.masses_of(
            propers.load_calendar(ROOT / "src/sources/calendars", "roman-1962"))]
        cls.inventory = ROOT / "src/sources/inventories/missal-expected-targets-v1.toml"

    def classify(self, masses=None):
        return expectations(self.inventory, "roman-1962", self.masses if masses is None else masses)

    def test_1962_pentecost_has_thirteen_bounded_source_appointments(self):
        report = self.classify()
        row = pentecost(bounded_form_text_slots(report))
        self.assertEqual((row["expected"], row["represented"], row["not_represented"],
                          row["unresolved"]), (13, 13, 0, 0))
        self.assertEqual(row["denominator_state"], "bounded")
        self.assertEqual(row["whole_form_state"], "unresolved")
        self.assertTrue(any(boundary["kind"] == "text-slots" and
                            boundary["state"] == "unenumerated" and
                            boundary["slice_id"] == row["source_slices"][0]["id"]
                            for boundary in report["boundaries"]))
        self.assertNotIn("source_refs", json.dumps(row))

    def test_missing_lesson_and_changed_preface_stay_missing_with_same_denominator(self):
        masses = copy.deepcopy(self.masses)
        mass = next(row for row in masses if row["key"] == "pentecost")
        mass["propers"] = [row for row in mass["propers"] if row["name"] != "Lesson"]
        mass["ordinary_appointments"]["preface"]["option"] = "trinitate"
        report = self.classify(masses)
        row = pentecost(bounded_form_text_slots(report))
        self.assertEqual((row["expected"], row["represented"], row["not_represented"],
                          row["unresolved"]), (13, 11, 2, 0))
        absent = {target["id"] for target in report["targets"]
                  if target.get("calendar_mass_key") == "pentecost" and
                  target["state"] == "not-represented" and target["kind"] == "text-slot"}
        self.assertEqual(absent, {
            "roman-1962.temporal.pentecost:reading:1",
            "roman-1962.temporal.pentecost:preface:1",
        })

    def test_incomplete_source_slice_keeps_only_a_lower_bound(self):
        report = self.classify()
        pentecost_slice = next(target["slice_id"] for target in report["targets"]
                               if target["id"] == "roman-1962.temporal.pentecost:reading:1")
        next(row for row in report["slices"] if row["id"] == pentecost_slice)[
            "enumeration_state"] = "partial"
        row = pentecost(bounded_form_text_slots(report))
        self.assertEqual((row["denominator_state"], row["expected"],
                          row["lower_bound"], row["represented"]),
                         ("unresolved", None, 13, 13))


if __name__ == "__main__":
    unittest.main()
