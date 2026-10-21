"""OLM 1981 p. 5, nn. 2-3: retain source boundaries across projections.

These assertions concern citation metadata. Bible reconstructions still show
whole verses; no subverse textual correspondence is asserted here.
"""
from pathlib import Path
from importlib.machinery import SourceFileLoader
from importlib.util import module_from_spec, spec_from_loader
import sys
import unittest
import yaml

ROOT = Path(__file__).resolve().parents[2]
PROPERS = ROOT / "src/sources/calendars/postconciliar/propers.yaml"


def load_tool(name):
    loader = SourceFileLoader("_advent_primary_" + name.replace("-", "_"), str(ROOT / "tools" / name))
    spec = spec_from_loader(loader.name, loader)
    module = module_from_spec(spec)
    sys.modules[loader.name] = module
    loader.exec_module(module)
    return module


class PostconciliarAdventPrimaryBoundariesTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.document = yaml.safe_load(PROPERS.read_text())
        cls.mass = next(m for s in cls.document["sections"].values() for m in s["masses"] if m["key"] == "advent-1")
        cls.canon = load_tool("citations")
        cls.owner = load_tool("mass-propers")

    def test_year_b_first_reading_keeps_printed_begin_part(self):
        proper = next(p for p in self.mass["propers"] if p["name"] == "First Reading")
        ref = "Isaiah 63:16b-17, 19b; 64:2b-7"
        self.assertEqual(proper["cycles"]["B"]["verses"], [self.canon.parse_citation(ref)])
        self.assertEqual(proper["cycles"]["A"]["verses"], [self.canon.parse_citation("Isaiah 2:1-5")])
        self.assertEqual(proper["cycles"]["C"]["verses"], [self.canon.parse_citation("Jeremiah 33:14-16")])

    def test_existing_whole_verse_divergence_remains_bound_to_corrected_source(self):
        proper = next(p for p in self.mass["propers"] if p["name"] == "First Reading")
        entry = proper["cycles"]["B"]["verses"][0]
        entries = [citation for _, mass in self.owner.masses_of(self.document) for citation, _ in self.owner.numbered_entries(mass, self.document["psalm_numbering"])]
        resolvers = {target: self.owner.Divergences("postconciliar", self.document, entries, self.canon, target, numberings=("hebrew",)) for target in self.owner.SYSTEMS}
        projected = self.owner.citation_structure(entry, "hebrew", self.owner.book_tokens(), resolvers)
        self.assertIsNone(projected["unresolved"])
        self.assertNotIn("refused", projected)
        self.assertEqual(projected["loci"]["vulgate"], [{"chapter":63,"first":16,"last":17},{"chapter":64,"first":1,"last":1},{"chapter":64,"first":3,"last":8}])

    def test_psalm_source_part_conversion_is_not_blindly_reversed(self):
        proper = next(p for p in self.mass["propers"] if p["name"] == "Responsorial Psalm")
        entry = proper["cycles"]["C"]["verses"][0]
        self.assertEqual(entry, self.canon.parse_citation("Psalm 25:4-5ab, 8-9, 10, 14"))
        self.assertNotIn("part", entry["ranges"][0]["begin"])
        self.assertIn("Its Vulgate 4bc names the whole", self.mass["notes"])


if __name__ == "__main__":
    unittest.main()
