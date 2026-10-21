"""Keep source-checked OT antiphons on their actual psalms.

The exact ICEL Antiphonary e6b82741 artifact pages 75-91 were read as page
images on 2026-10-20. The literal Vulgate loci below are the antiphon cues,
not the parenthesized Graduale suggestions. The existing seasonal-collation
inventory carries each row's printed/artifact page and the numbering caveats.
Public-domain Bible reconstruction remains distinct from liturgical wording.
"""
from pathlib import Path
from importlib.machinery import SourceFileLoader
from importlib.util import module_from_spec, spec_from_loader
import sys
import unittest
import yaml

ROOT = Path(__file__).resolve().parents[2]
PROPERS = ROOT / "src/sources/calendars/postconciliar/propers.yaml"

# Literal source loci; secondary Hebrew addresses follow the existing
# concordance. None of these expectations is calculated by the tested owner.
CORRECTED = [('ot-6',
  'Entrance Antiphon',
  1,
  {'vulgate': [{'chapter': 30, 'first': 3, 'last': 4}],
   'hebrew': [{'chapter': 31, 'first': 3, 'last': 4}]}),
 ('ot-7',
  'Entrance Antiphon',
  1,
  {'vulgate': [{'chapter': 12, 'first': 6, 'last': 6}],
   'hebrew': [{'chapter': 13, 'first': 6, 'last': 6}]}),
 ('ot-8',
  'Communion Antiphon',
  1,
  {'vulgate': [{'chapter': 12, 'first': 6, 'last': 6}],
   'hebrew': [{'chapter': 13, 'first': 6, 'last': 6}]}),
 ('ot-9',
  'Communion Antiphon',
  1,
  {'vulgate': [{'chapter': 16, 'first': 6, 'last': 6}],
   'hebrew': [{'chapter': 17, 'first': 6, 'last': 6}]}),
 ('ot-10',
  'Entrance Antiphon',
  1,
  {'vulgate': [{'chapter': 26, 'first': 1, 'last': 2}],
   'hebrew': [{'chapter': 27, 'first': 1, 'last': 2}]}),
 ('ot-10',
  'Communion Antiphon',
  1,
  {'vulgate': [{'chapter': 17, 'first': 3, 'last': 3}],
   'hebrew': [{'chapter': 18, 'first': 3, 'last': 3}]}),
 ('ot-11',
  'Entrance Antiphon',
  1,
  {'vulgate': [{'chapter': 26, 'first': 7, 'last': 7}, {'chapter': 26, 'first': 9, 'last': 9}],
   'hebrew': [{'chapter': 27, 'first': 7, 'last': 7}, {'chapter': 27, 'first': 9, 'last': 9}]}),
 ('ot-11',
  'Communion Antiphon',
  1,
  {'vulgate': [{'chapter': 26, 'first': 4, 'last': 4}],
   'hebrew': [{'chapter': 27, 'first': 4, 'last': 4}]}),
 ('ot-12',
  'Entrance Antiphon',
  1,
  {'vulgate': [{'chapter': 27, 'first': 8, 'last': 9}],
   'hebrew': [{'chapter': 28, 'first': 8, 'last': 9}]}),
 ('ot-12',
  'Communion Antiphon',
  1,
  {'vulgate': [{'chapter': 144, 'first': 15, 'last': 15}],
   'hebrew': [{'chapter': 145, 'first': 15, 'last': 15}]}),
 ('ot-13',
  'Entrance Antiphon',
  1,
  {'vulgate': [{'chapter': 46, 'first': 2, 'last': 2}],
   'hebrew': [{'chapter': 47, 'first': 2, 'last': 2}]}),
 ('ot-13',
  'Communion Antiphon',
  1,
  {'vulgate': [{'chapter': 102, 'first': 1, 'last': 1}],
   'hebrew': [{'chapter': 103, 'first': 1, 'last': 1}]}),
 ('ot-18',
  'Entrance Antiphon',
  1,
  {'vulgate': [{'chapter': 69, 'first': 2, 'last': 2}, {'chapter': 69, 'first': 6, 'last': 6}],
   'hebrew': [{'chapter': 70, 'first': 2, 'last': 2}, {'chapter': 70, 'first': 6, 'last': 6}]}),
 ('ot-19',
  'Entrance Antiphon',
  1,
  {'vulgate': [{'chapter': 73, 'first': 20, 'last': 20},
               {'chapter': 73, 'first': 19, 'last': 19},
               {'chapter': 73, 'first': 22, 'last': 22},
               {'chapter': 73, 'first': 23, 'last': 23}],
   'hebrew': [{'chapter': 74, 'first': 20, 'last': 20},
              {'chapter': 74, 'first': 19, 'last': 19},
              {'chapter': 74, 'first': 22, 'last': 22},
              {'chapter': 74, 'first': 23, 'last': 23}]}),
 ('ot-20',
  'Entrance Antiphon',
  1,
  {'vulgate': [{'chapter': 83, 'first': 10, 'last': 11}],
   'hebrew': [{'chapter': 84, 'first': 10, 'last': 11}]}),
 ('ot-20',
  'Communion Antiphon',
  1,
  {'vulgate': [{'chapter': 129, 'first': 7, 'last': 7}],
   'hebrew': [{'chapter': 130, 'first': 7, 'last': 7}]}),
 ('ot-21',
  'Entrance Antiphon',
  1,
  {'vulgate': [{'chapter': 85, 'first': 1, 'last': 3}],
   'hebrew': [{'chapter': 86, 'first': 1, 'last': 3}]}),
 ('ot-21',
  'Communion Antiphon',
  1,
  {'vulgate': [{'chapter': 103, 'first': 13, 'last': 15}],
   'hebrew': [{'chapter': 104, 'first': 13, 'last': 15}]}),
 ('ot-22',
  'Entrance Antiphon',
  1,
  {'vulgate': [{'chapter': 85, 'first': 3, 'last': 3}, {'chapter': 85, 'first': 5, 'last': 5}],
   'hebrew': [{'chapter': 86, 'first': 3, 'last': 3}, {'chapter': 86, 'first': 5, 'last': 5}]}),
 ('ot-23',
  'Communion Antiphon',
  1,
  {'vulgate': [{'chapter': 41, 'first': 2, 'last': 3}],
   'hebrew': [{'chapter': 42, 'first': 2, 'last': 3}]}),
 ('ot-24',
  'Communion Antiphon',
  1,
  {'vulgate': [{'chapter': 35, 'first': 8, 'last': 8}],
   'hebrew': [{'chapter': 36, 'first': 8, 'last': 8}]}),
 ('ot-28',
  'Entrance Antiphon',
  1,
  {'vulgate': [{'chapter': 129, 'first': 3, 'last': 4}],
   'hebrew': [{'chapter': 130, 'first': 3, 'last': 4}]}),
 ('ot-28',
  'Communion Antiphon',
  1,
  {'vulgate': [{'chapter': 33, 'first': 11, 'last': 11}],
   'hebrew': [{'chapter': 34, 'first': 11, 'last': 11}]}),
 ('ot-29',
  'Entrance Antiphon',
  1,
  {'vulgate': [{'chapter': 16, 'first': 6, 'last': 6}, {'chapter': 16, 'first': 8, 'last': 8}],
   'hebrew': [{'chapter': 17, 'first': 6, 'last': 6}, {'chapter': 17, 'first': 8, 'last': 8}]}),
 ('ot-30',
  'Entrance Antiphon',
  1,
  {'vulgate': [{'chapter': 104, 'first': 3, 'last': 4}],
   'hebrew': [{'chapter': 105, 'first': 3, 'last': 4}]}),
 ('ot-30',
  'Communion Antiphon',
  1,
  {'vulgate': [{'chapter': 19, 'first': 6, 'last': 6}],
   'hebrew': [{'chapter': 20, 'first': 6, 'last': 6}]}),
 ('ot-31',
  'Entrance Antiphon',
  1,
  {'vulgate': [{'chapter': 37, 'first': 22, 'last': 23}],
   'hebrew': [{'chapter': 38, 'first': 22, 'last': 23}]}),
 ('ot-32',
  'Entrance Antiphon',
  1,
  {'vulgate': [{'chapter': 87, 'first': 3, 'last': 3}],
   'hebrew': [{'chapter': 88, 'first': 3, 'last': 3}]}),
 ('ot-32',
  'Communion Antiphon',
  1,
  {'vulgate': [{'chapter': 22, 'first': 1, 'last': 2}],
   'hebrew': [{'chapter': 23, 'first': 1, 'last': 2}]})]

PRESERVED = [('ot-2',
  'Entrance Antiphon',
  1,
  'hebrew',
  {'vulgate': [{'chapter': 65, 'first': 4, 'last': 4}],
   'hebrew': [{'chapter': 66, 'first': 4, 'last': 4}]}),
 ('ot-3',
  'Entrance Antiphon',
  1,
  'hebrew',
  {'vulgate': [{'chapter': 95, 'first': 1, 'last': 1}, {'chapter': 95, 'first': 6, 'last': 6}],
   'hebrew': [{'chapter': 96, 'first': 1, 'last': 1}, {'chapter': 96, 'first': 6, 'last': 6}]}),
 ('ot-4',
  'Communion Antiphon',
  1,
  'hebrew',
  {'vulgate': [{'chapter': 30, 'first': 17, 'last': 18}],
   'hebrew': [{'chapter': 31, 'first': 17, 'last': 18}]}),
 ('ot-5',
  'Entrance Antiphon',
  1,
  'hebrew',
  {'vulgate': [{'chapter': 94, 'first': 6, 'last': 7}],
   'hebrew': [{'chapter': 95, 'first': 6, 'last': 7}]}),
 ('ot-7',
  'Communion Antiphon',
  1,
  'hebrew',
  {'vulgate': [{'chapter': 9, 'first': 2, 'last': 3}],
   'hebrew': [{'chapter': 9, 'first': 2, 'last': 3}]}),
 ('ot-14',
  'Entrance Antiphon',
  1,
  'hebrew',
  {'vulgate': [{'chapter': 47, 'first': 10, 'last': 11}],
   'hebrew': [{'chapter': 48, 'first': 10, 'last': 11}]}),
 ('ot-15',
  'Communion Antiphon',
  1,
  'hebrew',
  {'vulgate': [{'chapter': 83, 'first': 4, 'last': 5}],
   'hebrew': [{'chapter': 84, 'first': 4, 'last': 5}]}),
 ('ot-16',
  'Entrance Antiphon',
  1,
  'hebrew',
  {'vulgate': [{'chapter': 53, 'first': 6, 'last': 6}, {'chapter': 53, 'first': 8, 'last': 8}],
   'hebrew': [{'chapter': 54, 'first': 6, 'last': 6}, {'chapter': 54, 'first': 8, 'last': 8}]}),
 ('ot-17',
  'Entrance Antiphon',
  1,
  'hebrew',
  {'vulgate': [{'chapter': 67, 'first': 6, 'last': 7}, {'chapter': 67, 'first': 36, 'last': 36}],
   'hebrew': [{'chapter': 68, 'first': 6, 'last': 7}, {'chapter': 68, 'first': 36, 'last': 36}]}),
 ('ot-19',
  'Communion Antiphon',
  1,
  'hebrew',
  {'vulgate': [{'chapter': 147, 'first': 12, 'last': 12},
               {'chapter': 147, 'first': 14, 'last': 14}],
   'hebrew': [{'chapter': 147, 'first': 12, 'last': 12},
              {'chapter': 147, 'first': 14, 'last': 14}]}),
 ('ot-25',
  'Communion Antiphon',
  1,
  'vulgate',
  {'vulgate': [{'chapter': 118, 'first': 4, 'last': 5}],
   'hebrew': [{'chapter': 119, 'first': 4, 'last': 5}]}),
 ('ot-33',
  'Communion Antiphon',
  1,
  'vulgate',
  {'vulgate': [{'chapter': 72, 'first': 28, 'last': 28}],
   'hebrew': [{'chapter': 73, 'first': 28, 'last': 28}]})]


class PostconciliarAntiphonNumberingTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        loader = SourceFileLoader("_antiphon_numbering_mass_propers", str(ROOT / "tools/mass-propers"))
        spec = spec_from_loader(loader.name, loader)
        cls.owner = module_from_spec(spec)
        sys.modules[loader.name] = cls.owner
        loader.exec_module(cls.owner)
        cls.calendar = yaml.safe_load(PROPERS.read_text())
        cls.masses = {m["key"]: m for s in cls.calendar["sections"].values() for m in s["masses"]}

    def projection(self, key, name, occurrence):
        slot = [p for p in self.masses[key]["propers"] if p["name"] == name][occurrence - 1]
        rows = [self.owner.citation_structure(entry, numbering, self.owner.book_tokens())
                for entry, numbering in self.owner.numbered_proper_entries(slot, self.calendar["psalm_numbering"])]
        for row in rows:
            self.assertIsNone(row["unresolved"], (key, name, row))
        return rows

    def assert_source_loci(self, key, name, occurrence, numbering, expected):
        rows = self.projection(key, name, occurrence)
        for system, spans in expected.items():
            self.assertEqual([span for row in rows for span in row["loci"][system]], spans,
                             (key, name, occurrence, system))
        self.assertTrue(all(row["numbering"] == numbering for row in rows), (key, name))

    def test_reconstructed_antiphons_address_the_source_psalms(self):
        for key, name, occurrence, expected in CORRECTED:
            with self.subTest(mass=key, proper=name, occurrence=occurrence):
                self.assert_source_loci(key, name, occurrence, "vulgate", expected)

    def test_existing_hebrew_and_vulgate_owners_keep_their_source_loci(self):
        for key, name, occurrence, numbering, expected in PRESERVED:
            with self.subTest(mass=key, proper=name, occurrence=occurrence):
                self.assert_source_loci(key, name, occurrence, numbering, expected)


if __name__ == "__main__":
    unittest.main()
