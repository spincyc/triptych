#!/usr/bin/env python3
"""Bonn-witness boundaries, without claims about an actual local Ordo."""
from __future__ import annotations

import copy
import sys
import unittest
from importlib.machinery import SourceFileLoader
from importlib.util import module_from_spec, spec_from_loader
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))
CALENDARS = ROOT / "src/sources/calendars"


def load_tool(name):
    loader = SourceFileLoader("pre55_boundary_" + name.replace("-", "_"), str(ROOT / "tools" / name))
    spec = spec_from_loader(loader.name, loader)
    module = module_from_spec(spec)
    sys.modules[loader.name] = module
    loader.exec_module(module)
    return module


days = load_tool("calendar-days")
rubrics = load_tool("calendar-rubrics")


def year_for(calendar, civil_year=2026):
    index = days.load_calendar(CALENDARS, calendar)
    built = days.build_years(index, [civil_year, civil_year + 1])
    days.with_fixed(index, [civil_year])
    return days.year_document(index, civil_year, built)


class Pre1955CalendarSourceBoundaries(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.older = year_for("roman-pre-1955")
        cls.roman = year_for("roman-1962")

    def test_older_assignments_have_no_postconciliar_sunday_alternative(self):
        dates = self.older["days"]
        self.assertIn("ascension", [r["key"] for r in dates["2026-05-14"]])
        self.assertNotIn("ascension", [r["key"] for r in dates["2026-05-17"]])
        self.assertIn("sunday-after-ascension", [r["key"] for r in dates["2026-05-17"]])
        self.assertIn("corpus-christi", [r["key"] for r in dates["2026-06-04"]])
        self.assertNotIn("corpus-christi", [r["key"] for r in dates["2026-06-07"]])
        for family in ("days", "ferial_formulary"):
            self.assertTrue(all("territorial" not in r for rows in self.older.get(family, {}).values() for r in rows))
        for family in ("epiphany", "ascension", "body_and_blood_of_christ"):
            self.assertNotIn("options", self.older["territorial"][family])
            self.assertIn("not computed", self.older["territorial"][family]["transferred_sunday_form"])

    def test_friday_after_older_ascension_octave_uses_its_sunday(self):
        # Bonn486/382 and 1962's checked352 deliberately appoint different Masses.
        self.assertEqual([r["key"] for r in self.older["ferial_formulary"]["2026-05-22"]], ["sunday-after-ascension"])
        self.assertEqual([r["key"] for r in self.roman["ferial_formulary"]["2026-05-22"]], ["ascension"])
        for calendar in (self.older, self.roman):
            self.assertEqual([r["key"] for r in calendar["ferial_formulary"]["2026-05-21"]], ["ascension"])

    def test_older_model_has_one_branch_without_new_territorial_law(self):
        built, problems, _ = rubrics.build(CALENDARS, "roman-pre-1955")
        self.assertEqual(problems, [])
        answered = rubrics.run_model({"cases": [
            {"id": date, "date": date, "year": self.older, "rubrics": built[0]}
            for date in ("2026-05-14", "2026-05-17", "2026-06-04", "2026-06-07")]})
        for row in answered["results"]:
            with self.subTest(date=row["id"]):
                self.assertTrue(row["ok"], row)
                self.assertEqual(len(row["result"]["options"]), 1)
                branch, = row["result"]["options"]
                self.assertIsNone(branch["option"])


class Pre1955AdmittedPrayerConservation(unittest.TestCase):
    def test_no_1960_cap_truncates_older_admitted_series(self):
        # AdditionsV.1 requires the admitted Lauds series. This anonymous
        # read/simplex source-contract fixture stipulates four such units;
        # it establishes no date, local calendar, or missing historical grade.
        built, problems, _ = rubrics.build(CALENDARS, "roman-pre-1955")
        self.assertEqual(problems, [])
        source = copy.deepcopy(built[0])
        indices = {r["id"]: i for i, r in enumerate(source["bases"])}
        source["keys"] = {
            "fixture-office": {"basis": indices["row-24-simplex-feria"], "name": "Source-fixture Office", "forms": []},
            **{"fixture-commemoration-" + str(i): {
                "basis": indices["calendar-commemoration"], "name": "Admitted Lauds commemoration " + str(i), "forms": []}
                for i in range(1, 5)},
        }
        for rule in source["commemoration"]["ceilings"]["rules"]:
            if rule.get("clause") == "d":
                rule["max"] = 4  # Exact admission supplied by this fixture.
                rule["what"] = "the source-fixture's four admitted Lauds commemorations"
        date = "2026-07-09"
        year = {"days": {date: [{"key": key} for key in source["keys"]]}, "rules": [],
                "liturgical_years": [{"begins": "2025-11-30", "ends": "2026-11-28",
                "seasons": [{"from": "2026-05-31", "to": "2026-11-28", "season": "after-pentecost"}],
                "unresolved": []}]}
        result, = rubrics.run_model({"cases": [{"id": "admitted-series", "date": date,
                                               "year": year, "rubrics": source}]})["results"]
        self.assertTrue(result["ok"], result)
        branch, = result["result"]["options"]
        admitted = [r for r in branch["losers"] if r["disposition"] == "commemorated"]
        self.assertEqual(len(admitted), 4)
        self.assertEqual(len(branch["orations"]["low_mass"]), 5)
        self.assertEqual([r["of"] for r in branch["orations"]["low_mass"]], list(source["keys"]))


if __name__ == "__main__":
    unittest.main()
