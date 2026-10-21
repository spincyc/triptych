"""Keep two source-checked seasonal antiphons on their printed Vulgate Psalms."""
from pathlib import Path
from importlib.machinery import SourceFileLoader
from importlib.util import module_from_spec, spec_from_loader
import sys
import unittest
import yaml

ROOT = Path(__file__).resolve().parents[2]
PROPERS = ROOT / "src/sources/calendars/postconciliar/propers.yaml"

class SeasonalAntiphonNumberingTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        loader = SourceFileLoader("_seasonal_antiphon_numbering_owner", str(ROOT / "tools/mass-propers"))
        cls.owner = module_from_spec(spec_from_loader(loader.name, loader))
        sys.modules[loader.name] = cls.owner
        loader.exec_module(cls.owner)
        cls.calendar = yaml.safe_load(PROPERS.read_text())
        cls.masses = {m["key"]: m for _, m in cls.owner.masses_of(cls.calendar)}

    def citation(self, key, name):
        proper = next(p for p in self.masses[key]["propers"] if p["name"] == name)
        entries = list(self.owner.numbered_proper_entries(proper, self.calendar["psalm_numbering"]))
        self.assertEqual(len(entries), 1)
        entry, numbering = entries[0]
        row = self.owner.citation_structure(entry, numbering, self.owner.book_tokens())
        self.assertIsNone(row["unresolved"])
        return row

    def test_seasonal_entrances_address_the_source_psalms(self):
        # Literal source cues and the source's printed Hebrew bracket, not
        # expectations derived by the conversion owner under test.
        for key, vulgate, hebrew, first, last in [
            ("easter-7", 26, 27, 7, 9),
            ("corpus-christi", 80, 81, 17, 17),
        ]:
            with self.subTest(mass=key):
                row = self.citation(key, "Entrance Antiphon")
                self.assertEqual(row["numbering"], "vulgate")
                self.assertEqual(row["loci"]["vulgate"], [{"chapter": vulgate, "first": first, "last": last}])
                self.assertEqual(row["loci"]["hebrew"], [{"chapter": hebrew, "first": first, "last": last}])

    def test_existing_owners_are_preserved(self):
        self.assertEqual(self.calendar["psalm_numbering"], "hebrew")
        advent = self.citation("advent-1", "Entrance Antiphon")
        self.assertEqual(advent["numbering"], "hebrew")
        self.assertEqual(advent["loci"]["vulgate"], [{"chapter":24,"first":1,"last":3}])
        king = self.citation("christ-the-king", "Communion Antiphon")
        self.assertEqual(king["numbering"], "vulgate")
        self.assertEqual(king["loci"]["vulgate"], [{"chapter":28,"first":10,"last":11}])
        self.assertEqual(self.citation("easter-7", "Communion Antiphon")["ref"], "John 17:22")
        self.assertEqual(self.citation("corpus-christi", "Communion Antiphon")["ref"], "John 6:57")

if __name__ == "__main__":
    unittest.main()
