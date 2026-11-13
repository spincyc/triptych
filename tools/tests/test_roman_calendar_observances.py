"""Primary-source regressions for the two annual 1962 calendar edge cases."""
from __future__ import annotations

import copy
from datetime import date, timedelta
from importlib.machinery import SourceFileLoader
from importlib.util import module_from_spec, spec_from_loader
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[2]
CALENDARS = ROOT / "src/sources/calendars"


def load_tool(name):
    loader = SourceFileLoader("_observance_" + name.replace("-", "_"), str(ROOT / "tools" / name))
    spec = spec_from_loader(loader.name, loader)
    module = module_from_spec(spec)
    sys.modules[spec.name] = module
    loader.exec_module(module)
    return module


days = load_tool("calendar-days")
rubrics = load_tool("calendar-rubrics")


class RomanCalendarObservances(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.index = days.load_calendar(CALENDARS, "roman-1962")
        cls.years = days.build_years(cls.index, list(range(2020, 2122)))
        days.with_fixed(cls.index, list(range(2020, 2121)))
        emitted, problems, sources = rubrics.build(CALENDARS, "roman-1962")
        if problems:
            raise AssertionError(problems)
        cls.rubrics = emitted[0]
        cls.source = sources["roman-1962"]
        dates = ["2021-04-25", "2026-04-25", "2025-04-25", "2038-04-25",
                 "2038-04-27", "2095-04-25", "2095-04-26", "2026-05-11",
                 "2026-05-12", "2026-05-13", "2038-11-21", "2095-11-20",
                 "2026-03-27", "2027-03-19"]
        cases = [{"id": stamp, "date": stamp, "rubrics": cls.rubrics,
                  "year": days.year_document(cls.index, int(stamp[:4]), cls.years)}
                 for stamp in dates]
        cls.inputs = {row["id"]: row for row in cases}
        result = rubrics.run_model({"cases": cases})
        cls.branches = {}
        for row in result["results"]:
            if not row["ok"]:
                raise AssertionError(row["error"])
            branch, = row["result"]["options"]
            cls.branches[row["id"]] = branch

    def test_greater_litanies_date_over_the_whole_supported_century(self):
        transferred = []
        for year in range(2020, 2121):
            anchors = self.years[year].anchors
            expected = date(year, 4, 25)
            if expected in (anchors.easter, anchors.easter + timedelta(days=1)):
                expected = anchors.easter + timedelta(days=2)
                transferred.append(year)
            self.assertEqual(expected, anchors.greater_litanies)
            self.assertIn("rogation-mass", [r["key"] for r in self.years[year].placements[expected]])
        self.assertEqual(transferred, [2038, 2095])

    def test_greater_litanies_is_a_privileged_commemoration_in_both_mass_types(self):
        for stamp in ("2021-04-25", "2026-04-25", "2025-04-25", "2038-04-27", "2095-04-26"):
            branch = self.branches[stamp]
            self.assertTrue(branch["settled"], stamp)
            for kind in ("low_mass", "sung_non_conventual"):
                self.assertEqual(len(branch["orations"][kind]), 2, (stamp, kind))
                row = branch["orations"][kind][1]
                self.assertEqual(row["of"], "commemoration:greater-litanies")
                self.assertEqual(row["source_key"], "rogation-mass")
                self.assertEqual(row["kind"], "privileged commemoration")

    def test_sunday_privilege_displaces_st_mark_without_turning_litanies_into_the_day(self):
        branch = self.branches["2021-04-25"]
        self.assertEqual(branch["winner"]["key"], "easter-3")
        mark = next(row for row in branch["losers"] if row["id"] == "litania-maior")
        self.assertEqual(mark["disposition"], "omitted")
        self.assertIn("privileged commemoration", mark["why"])
        self.assertEqual(next(row for row in branch["candidates"]
                              if row["id"] == "commemoration:greater-litanies")["row"], None)

    def test_easter_transfer_and_lesser_litanies_do_not_gain_the_april_commemoration(self):
        for stamp in ("2038-04-25", "2095-04-25", "2026-05-11", "2026-05-12", "2026-05-13"):
            branch = self.branches[stamp]
            self.assertTrue(branch["settled"], stamp)
            self.assertNotIn("commemoration:greater-litanies", [r["id"] for r in branch["candidates"]])
            for rows in branch["orations"].values():
                self.assertNotIn("rogation-mass", [r["source_key"] for r in rows])

    def test_short_year_uses_only_the_last_formulary_and_has_one_ferial_governor(self):
        for stamp in ("2038-11-21", "2095-11-20"):
            branch = self.branches[stamp]
            self.assertTrue(branch["settled"], stamp)
            self.assertEqual(branch["winner"]["key"], "last-sunday-after-pentecost")
            self.assertNotIn("pentecost-23", [r["key"] for r in branch["candidates"]])
            year = self.years[int(stamp[:4])]
            self.assertEqual(year.governors[date.fromisoformat(stamp)]["key"], "last-sunday-after-pentecost")
            self.assertNotIn(date.fromisoformat(stamp), year.contested)
            self.assertEqual(year.facts["sundays_after_pentecost"], 23)
            self.assertEqual(year.facts["unused_after_epiphany"], 0)
            self.assertEqual(year.facts["resumption_slots"], 0)
            self.assertEqual(year.facts["surplus"], 0)

    def test_missing_date_anchor_refuses_instead_of_silently_dropping_a_prayer(self):
        case = copy.deepcopy(self.inputs["2026-04-25"])
        for owner in case["year"]["liturgical_years"]:
            owner["anchors"].pop("greater_litanies", None)
        result, = rubrics.run_model({"cases": [case]})["results"]
        self.assertFalse(result["ok"])
        self.assertIn("missing calendar anchor", result["error"])

    def test_date_observance_validation_rejects_unknown_mass_and_ordinary_basis(self):
        assigned, errors = rubrics.assign(self.source, rubrics.load_masses(CALENDARS, "roman-1962"), "fixture")
        self.assertFalse(errors)
        for field, value in (("mass", "unknown-mass"), ("basis", "calendar-commemoration"),
                             ("on_anchor", "unknown_anchor")):
            fixture = copy.deepcopy(self.source)
            fixture["commemoration"]["date_observances"][0][field] = value
            self.assertTrue(rubrics.check_date_observances(fixture, assigned, "fixture"))

    def test_runtime_rejects_a_known_basis_that_would_change_the_observance(self):
        for basis in ("calendar-commemoration", "row-2-triduum"):
            case = copy.deepcopy(self.inputs["2026-04-25"])
            case["rubrics"]["commemoration"]["date_observances"][0]["basis"] = basis
            result, = rubrics.run_model({"cases": [case]})["results"]
            self.assertFalse(result["ok"])
            self.assertIn("unclassified dated commemoration", result["error"])

    def test_seven_sorrows_pair_requires_the_feria_to_win_occurrence(self):
        ordinary = self.branches["2026-03-27"]
        self.assertEqual(ordinary["winner"]["key"], "passion-friday")
        self.assertEqual([row["id"] for row in ordinary["massChoices"]],
                         ["seven-sorrows-where-devotions-are-held"])
        collision = self.branches["2027-03-19"]
        self.assertTrue(collision["settled"])
        self.assertEqual(collision["winner"]["key"], "s-ioseph-sponsi-beatae-mariae-virginis")
        self.assertEqual(collision["massChoices"], [])
        self.assertEqual([row["key"] for row in collision["readable"] if row["state"] == "said"],
                         ["s-ioseph-sponsi-beatae-mariae-virginis"])


if __name__ == "__main__":
    unittest.main()
