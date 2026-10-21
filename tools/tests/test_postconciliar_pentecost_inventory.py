"""Source-local Pentecost appointments must not become target-book completion."""
from __future__ import annotations

import copy
import importlib.machinery
import importlib.util
from pathlib import Path
import sys
import unittest


ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))
import _missal_coverage as coverage

INVENTORY = ROOT / "src/sources/inventories/missal-expected-targets-v1.toml"
PREFIX = "postconciliar:pentecost:"


class PostconciliarPentecostInventoryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        loader = importlib.machinery.SourceFileLoader(
            "postconciliar_pentecost_propers", str(ROOT / "tools/mass-propers"))
        spec = importlib.util.spec_from_loader(loader.name, loader)
        propers = importlib.util.module_from_spec(spec)
        loader.exec_module(propers)
        document = propers.load_calendar(ROOT / "src/sources/calendars", "postconciliar")
        cls.mass = next(mass for _, mass in propers.masses_of(document)
                        if mass["key"] == "pentecost")

    def report(self, mass=None):
        return coverage.expectations(
            INVENTORY, "postconciliar", [self.mass if mass is None else mass])

    def states(self, report):
        return {row["id"]: row["state"] for row in report["targets"]
                if row["id"].startswith(PREFIX)}

    def test_partial_source_bounds_do_not_claim_an_exact_form_denominator(self):
        report = self.report()
        rows = {row["form"]: row for row in coverage.bounded_form_text_slots(report)
                if row["mass"] == "pentecost"}
        self.assertEqual(set(rows), {"day", "vigil"})
        for form, lower, represented, unresolved in (
            ("day", 15, 1, 14), ("vigil", 13, 2, 11),
        ):
            with self.subTest(form=form):
                row = rows[form]
                self.assertEqual((row["lower_bound"], row["represented"],
                                  row["not_represented"], row["unresolved"]),
                                 (lower, represented, 0, unresolved))
                self.assertEqual((row["denominator_state"], row["expected"],
                                  row["whole_form_state"]),
                                 ("unresolved", None, "unresolved"))
        self.assertEqual(report["whole_inventory_state"], "unresolved")
        self.assertTrue(any(row["id"] ==
                            "postconciliar-pentecost-lectionary-options-and-response-units"
                            and row["state"] == "unenumerated"
                            for row in report["boundaries"]))

    def test_source_addresses_do_not_promote_old_witness_or_option_correspondence(self):
        report = self.report()
        states = self.states(report)
        self.assertEqual(len(states), 28)
        self.assertEqual({key for key, value in states.items() if value == "represented"}, {
            PREFIX + "day:antiphon:communion",
            PREFIX + "vigil:antiphon:entrance",
            PREFIX + "vigil:antiphon:communion",
        })
        self.assertEqual(set(states.values()), {"represented", "unresolved"})
        forms = {row["id"]: row["state"] for row in report["targets"]
                 if row["id"] in {"pc2002-temporal-pentecost-day",
                                   "pc2002-temporal-pentecost-vigil"}}
        self.assertEqual(set(forms.values()), {"unresolved"})
        self.assertEqual(len(forms), 2)
        # The independently inventoried extended Vigil gets no base-form join.
        extended = next(row for row in report["targets"]
                        if row["id"] == "postconciliar:2008:pentecost-vigil-extended")
        self.assertEqual(extended["state"], "unresolved")
        self.assertIsNone(extended["mass"])

    def test_missing_day_communion_cannot_borrow_the_vigil_appointment(self):
        original = self.states(self.report())
        mass = copy.deepcopy(self.mass)
        day = next(form for form in mass["forms"] if form["id"] == "day")
        day["propers"] = [row for row in day["propers"]
                          if row["name"] != "Communion Antiphon"]
        changed = self.states(self.report(mass))
        target = PREFIX + "day:antiphon:communion"
        self.assertEqual((original[target], changed[target]),
                         ("represented", "not-represented"))
        self.assertEqual({key for key in original if original[key] != changed[key]}, {target})
        self.assertEqual(changed[PREFIX + "vigil:antiphon:communion"], "represented")


if __name__ == "__main__":
    unittest.main()
