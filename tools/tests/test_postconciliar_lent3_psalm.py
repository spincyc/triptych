"""Keep OLM1981 n.237's second Psalm distinct from nearby provisions.

Held OLM artifact ed4bc14e, artifact p.188 / printed p.134, n.237:
the two Psalm cues are Ps41:2,3 and Ps42:2,3,4 (Vulgate). This test
uses appointment facts only; it supplies no protected liturgical wording.
"""
from importlib.machinery import SourceFileLoader
from importlib.util import module_from_spec, spec_from_loader
from pathlib import Path
import sys
import unittest


ROOT = Path(__file__).resolve().parents[2]


class PostconciliarLentThreePsalmTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        loader = SourceFileLoader("_lent3_psalm_mass_propers", str(ROOT / "tools/mass-propers"))
        spec = spec_from_loader(loader.name, loader)
        owner = module_from_spec(spec)
        sys.modules[loader.name] = owner
        loader.exec_module(owner)
        structure = owner.calendar_structure(ROOT / "src/sources/calendars", "postconciliar", owner.book_tokens())
        cls.masses = {mass["key"]: mass for mass in structure["masses"]}
        cls.source_masses = {mass["key"]: mass for _, mass in owner.masses_of(owner.load_calendar(ROOT / "src/sources/calendars", "postconciliar"))}

    def test_lent_three_monday_keeps_both_psalms_and_the_appointed_verse(self):
        units = self.masses["lent-3-monday"]["propers"]
        self.assertEqual([p["name"] for p in units], [
            "First Reading", "Responsorial Psalm", "Responsorial Psalm",
            "Verse Before the Gospel", "Gospel",
        ])
        self.assertEqual(units[1]["citations"][0]["loci"]["hebrew"], [
            {"chapter": 42, "first": 2, "last": 2},
            {"chapter": 42, "first": 3, "last": 3},
        ])
        second = units[2]["citations"][0]
        self.assertEqual(second["loci"]["vulgate"], [
            {"chapter": 42, "first": 2, "last": 2},
            {"chapter": 42, "first": 3, "last": 3},
            {"chapter": 42, "first": 4, "last": 4},
        ], "OLM n.237 appoints verse2 in the second Psalm")
        self.assertEqual(second["loci"]["hebrew"], [
            {"chapter": 43, "first": 2, "last": 2},
            {"chapter": 43, "first": 3, "last": 3},
            {"chapter": 43, "first": 4, "last": 4},
        ])
        self.assertEqual([p["citations"][0]["ref"] for p in (units[0], units[3], units[4])], [
            "2 Kings 5:1-15a", "Psalm 130:5, 7", "Luke 4:24-30",
        ])

    def test_other_source_provisions_do_not_inherit_the_correction(self):
        # OLM artifact205 / printed151 / n.279 actually appoints only
        # Vulgate42:3,4 in the second Psalm. Its omission of verse2 is correct.
        easter = next(p for p in self.masses["easter-4-monday"]["propers"] if p["name"] == "Responsorial Psalm")
        hebrew_43 = [locus for citation in easter["citations"] for locus in citation["loci"]["hebrew"] if locus["chapter"] == 43]
        self.assertEqual(hebrew_43, [
            {"chapter": 43, "first": 3, "last": 3},
            {"chapter": 43, "first": 4, "last": 4},
        ])
        # n.238's Vulgate24:4bc is the whole of Hebrew25:4, as the
        # existing 2026-10-01 source-specific colon relation records.
        tuesday = next(p for p in self.masses["lent-3-tuesday"]["propers"] if p["name"] == "Responsorial Psalm")
        first = tuesday["citations"][0]
        self.assertEqual(first["ref"], "Psalm 25:4-5ab, 6-7bc, 8-9")
        self.assertEqual(first["loci"]["hebrew"][0], {"chapter": 25, "first": 4, "last": 5})
        source_psalm = next(p for p in self.source_masses["lent-3-tuesday"]["propers"] if p["name"] == "Responsorial Psalm")
        self.assertEqual(source_psalm["verses"][0]["ranges"][0]["begin"], {"chapter": 25, "verse": 4})


if __name__ == "__main__":
    unittest.main()
