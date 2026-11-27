"""Postconciliar same-place Row-3 Solemnity collisions settle under NUALC 60 and CDWDS 2020 Responsa."""

from importlib.machinery import SourceFileLoader
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[2]
rubrics = SourceFileLoader("pc_occurrence_rubrics", str(ROOT / "tools/calendar-rubrics")).load_module()
days = SourceFileLoader("pc_occurrence_days", str(ROOT / "tools/calendar-days")).load_module()


class PostconciliarOccurrenceLimitsTests(unittest.TestCase):
    def test_all_known_same_place_collisions_settle_with_source_bound_transfers(self):
        # Under NUALC 59 table 3, NUALC 60, and CDWDS Responsa ad dubia (11 May 2020),
        # Sacred Heart and Corpus Christi prevail over Saint Solemnities on the same row,
        # and the impeded Saint Solemnity transfers (or anticipates to 23 June for
        # Nativity of St. John the Baptist vs. Sacred Heart).
        cases_spec = [
            (f"{year}-06-24", None, "most-sacred-heart-jesus",
             "nativity-saint-john-baptist", f"{year}-06-23")
            for year in (2022, 2033, 2044, 2101, 2112)
        ]
        cases_spec += [
            ("2038-06-24", "corpus-christi-thursday", "corpus-christi",
             "nativity-saint-john-baptist", "2038-06-25")
        ]
        cases_spec += [
            (f"{year}-06-24", "corpus-christi-transferred-to-sunday", "corpus-christi",
             "nativity-saint-john-baptist", f"{year}-06-25")
            for year in (2057, 2068, 2114)
        ]
        cases_spec += [
            (f"{year}-06-29", None, "most-sacred-heart-jesus",
             "saints-peter-paul-apostles", f"{year}-06-30")
            for year in (2057, 2068, 2114)
        ]
        built, problems, _ = rubrics.build(rubrics.DEFAULT_ROOT, "postconciliar")
        self.assertFalse(problems)
        source = built[0]
        index = days.load_calendar(rubrics.DEFAULT_ROOT, "postconciliar")
        civil_years = sorted({int(date[:4]) for date, *_ in cases_spec})
        years = days.build_years(index, sorted(set(civil_years) | {year + 1 for year in civil_years}))
        days.with_fixed(index, civil_years)
        cases = [{"id": date, "date": date, "rubrics": source,
                  "year": days.year_document(index, int(date[:4]), years)} for date, *_ in cases_spec]
        results = rubrics.run_model({"cases": cases})["results"]
        for (date, territory, winner_key, loser_key, dest_date), result in zip(cases_spec, results):
            with self.subTest(date=date, territory=territory):
                self.assertTrue(result["ok"], result.get("error"))
                branch = next(row for row in result["result"]["options"] if row["option"] == territory)
                self.assertTrue(branch["settled"])
                self.assertEqual(branch["winner"]["id"], winner_key)
                self.assertFalse(branch["choiceRequired"])
                loser = next(row for row in branch["losers"] if row["id"] == loser_key)
                self.assertEqual(loser["disposition"], "transferred")
                self.assertEqual(loser["destination"], dest_date)

    def test_source_explanation_must_be_nonempty_prose(self):
        source = rubrics.load_source(rubrics.DEFAULT_ROOT, "postconciliar")
        for value in (False, 3, " "):
            source["precedence"]["unresolved_tie"] = value
            self.assertTrue(rubrics.check_precedence(source, "fixture"))


if __name__ == "__main__":
    unittest.main()
