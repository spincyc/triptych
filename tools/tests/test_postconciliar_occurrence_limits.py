"""A coequal solemnity is not settled by the other recension's row rules."""

from importlib.machinery import SourceFileLoader
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[2]
rubrics = SourceFileLoader("pc_occurrence_rubrics", str(ROOT / "tools/calendar-rubrics")).load_module()
days = SourceFileLoader("pc_occurrence_days", str(ROOT / "tools/calendar-days")).load_module()


class PostconciliarOccurrenceLimitsTests(unittest.TestCase):
    def test_all_known_same_place_collisions_keep_source_bound_refusal(self):
        # The 2022 Responsum is not implemented here; its patronal exception
        # and June 23 transfer cannot be represented by merely picking June 24.
        dates = [(f"{year}-06-24", None) for year in (2022, 2033, 2044, 2101, 2112)]
        dates += [("2038-06-24", "corpus-christi-thursday")]
        dates += [(f"{year}-06-24", "corpus-christi-transferred-to-sunday") for year in (2057, 2068, 2114)]
        dates += [(f"{year}-06-29", None) for year in (2057, 2068, 2114)]
        built, problems, _ = rubrics.build(rubrics.DEFAULT_ROOT, "postconciliar")
        self.assertFalse(problems)
        source = built[0]
        index = days.load_calendar(rubrics.DEFAULT_ROOT, "postconciliar")
        civil_years = sorted({int(date[:4]) for date, _ in dates})
        years = days.build_years(index, sorted(set(civil_years) | {year + 1 for year in civil_years}))
        days.with_fixed(index, civil_years)
        cases = [{"id": date, "date": date, "rubrics": source,
                  "year": days.year_document(index, int(date[:4]), years)} for date, _ in dates]
        results = rubrics.run_model({"cases": cases})["results"]
        for (date, territory), result in zip(dates, results):
            with self.subTest(date=date, territory=territory):
                self.assertTrue(result["ok"], result.get("error"))
                branch = next(row for row in result["result"]["options"] if row["option"] == territory)
                self.assertFalse(branch["settled"])
                self.assertIsNone(branch["winner"])
                self.assertFalse(branch["choiceRequired"])
                why = " ".join(row["why"] for row in branch["unsettled"])
                self.assertIn(source["precedence"]["unresolved_tie"], why)
                self.assertNotIn("movable before fixed", why)
                self.assertNotIn("proper before indulted", why)

    def test_source_explanation_must_be_nonempty_prose(self):
        source = rubrics.load_source(rubrics.DEFAULT_ROOT, "postconciliar")
        for value in (False, 3, " "):
            source["precedence"]["unresolved_tie"] = value
            self.assertTrue(rubrics.check_precedence(source, "fixture"))


if __name__ == "__main__":
    unittest.main()
