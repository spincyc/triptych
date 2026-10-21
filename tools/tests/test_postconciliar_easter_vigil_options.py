"""Retain the three independent Scripture options printed at OLM1981 n.41.

Held OLM artifact ed4bc14e, artifact page84 / printed page30. This records
appointment facts only; it grants no target-edition or body-publication claim.
"""
from pathlib import Path
from importlib.machinery import SourceFileLoader
from importlib.util import module_from_spec, spec_from_loader
import sys
import unittest

ROOT = Path(__file__).resolve().parents[2]
FACTS = [
    ("First Reading", "First Reading (shorter form)", "first-reading", "longer", "shorter",
     "Genesis 1:1-2:2", "Genesis 1:1, 26-31a"),
    ("Second Reading", "Second Reading (shorter form)", "second-reading", "longer", "shorter",
     "Genesis 22:1-18", "Genesis 22:1-2, 9a, 10-13, 15-18"),
    ("Responsorial Psalm", "Responsorial Psalm (alternative after the First Reading)",
     "responsorial-psalm-after-the-first-reading", "psalm-103", "psalm-32",
     "Psalm 104:1-2a, 5-6, 10, 12, 13-14, 24, 35c", "Psalm 33:4-5, 6-7, 12-13, 20, 22"),
]


def owner(name):
    loader = SourceFileLoader("_easter_vigil_options_" + name.replace("-", "_"), str(ROOT / "tools" / name))
    spec = spec_from_loader(loader.name, loader)
    module = module_from_spec(spec)
    sys.modules[loader.name] = module
    loader.exec_module(module)
    return module


class PostconciliarEasterVigilOptionsTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.owner = owner("mass-propers")
        cls.citations = owner("citations")
        document = cls.owner.load_calendar(ROOT / "src/sources/calendars", "postconciliar")
        cls.mass = next(m for _, m in cls.owner.masses_of(document) if m["key"] == "easter-vigil")
        structure = cls.owner.calendar_structure(ROOT / "src/sources/calendars", "postconciliar", cls.owner.book_tokens())
        cls.projected = next(m for m in structure["masses"] if m["key"] == "easter-vigil")

    def test_source_options_are_independent_adjacent_and_not_cumulative(self):
        rows = self.mass["propers"]
        names = [p["name"] for p in rows]
        for name, alternative, group, primary_option, secondary_option, primary_ref, secondary_ref in FACTS:
            with self.subTest(group=group):
                index = names.index(name)
                self.assertEqual(names[index + 1], alternative)
                pair = rows[index:index + 2]
                for row, option, ref in zip(pair, (primary_option, secondary_option), (primary_ref, secondary_ref)):
                    self.assertEqual(row["ordinary_disposition"]["kind"], "alternative")
                    self.assertEqual(row["ordinary_disposition"]["group"], group)
                    self.assertEqual(row["ordinary_disposition"]["option"], option)
                    self.assertEqual(row["source"], "scripture")
                    self.assertEqual(row["verses"], [self.citations.parse_citation(ref)])
                    self.assertNotIn("cycles", row)
                    self.assertNotIn("weekday_cycles", row)
                    self.assertNotIn("text", row)
                    self.assertNotIn("text_status", row)
                self.assertEqual(pair[0]["ordinary_disposition"]["basis"], pair[1]["ordinary_disposition"]["basis"])
                members = [p for p in rows if p.get("ordinary_disposition", {}).get("group") == group]
                self.assertEqual(members, pair)
        self.assertEqual(self.owner._calendars.ordinary_disposition_source_problems("easter-vigil", "", rows), [])

    def test_actual_citation_owner_retains_the_literal_boundaries_and_psalm(self):
        self.assertTrue(all(any(p.get("ordinary_disposition", {}).get("group") == fact[2] for p in self.projected["propers"]) for fact in FACTS))
        for name, alternative, group, primary_option, secondary_option, primary_ref, secondary_ref in FACTS:
            with self.subTest(group=group):
                rows = [p for p in self.projected["propers"] if p.get("ordinary_disposition", {}).get("group") == group]
                self.assertEqual(len(rows), 2)
                self.assertEqual([p["form_id"] for p in rows], ["main", "main"])
                self.assertEqual([p["citations"][0]["ref"] for p in rows], [primary_ref, secondary_ref])
                self.assertTrue(all(p["citations"][0]["unresolved"] is None for p in rows))
        psalm = next(p for p in self.projected["propers"] if p["name"] == FACTS[2][1])["citations"][0]
        self.assertEqual(psalm["loci"]["vulgate"], [
            {"chapter": 32, "first": 4, "last": 5},
            {"chapter": 32, "first": 6, "last": 7},
            {"chapter": 32, "first": 12, "last": 13},
            {"chapter": 32, "first": 20, "last": 20},
            {"chapter": 32, "first": 22, "last": 22},
        ])

    def test_other_vigil_modules_and_conditional_gaps_are_preserved(self):
        rows = self.mass["propers"]
        names = [p["name"] for p in rows]
        self.assertEqual(self.mass["ordinary_frame"]["applicability"], "unavailable")
        third = next(p for p in rows if p["name"] == "Third Reading")
        self.assertEqual(third["verses"], [self.citations.parse_citation("Exodus 14:15-15:1")])
        self.assertNotIn("ordinary_disposition", third)
        self.assertLess(names.index("First Reading"), names.index("Responsorial Psalm"))
        self.assertLess(names.index("Responsorial Psalm"), names.index("Prayer after the First Reading"))
        self.assertLess(names.index("Second Reading"), names.index("Third Reading"))
        self.assertEqual(len([p for p in rows if p["name"] == "Responsorial Psalm"]), 6)
        after_seventh = rows[names.index("Seventh Reading") + 1]
        self.assertEqual(after_seventh["name"], "Responsorial Psalm")
        self.assertNotIn("ordinary_disposition", after_seventh)
        self.assertEqual([v["ref"] for v in after_seventh["verses"]], ["Psalm 42:3, 5bcd", "Psalm 43:3, 4"])
        self.assertFalse(any(v["ref"] == "Psalm 51:12-13, 14-15, 18-19" for p in rows for v in p.get("verses", [])))


if __name__ == "__main__":
    unittest.main()
