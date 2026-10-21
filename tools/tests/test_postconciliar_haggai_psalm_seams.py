"""Bounded OLM source appointments resolve through the existing citation owner."""
from __future__ import annotations
from importlib.machinery import SourceFileLoader
from importlib.util import module_from_spec, spec_from_loader
from pathlib import Path
import sys
import unittest
import yaml

ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / 'src/sources/calendars/postconciliar/propers.yaml'
sys.path.insert(0, str(ROOT / 'scripts'))


def load_tool(name):
    loader = SourceFileLoader('_haggai_psalm_' + name.replace('-', '_'), str(ROOT / 'tools' / name))
    module = module_from_spec(spec_from_loader(loader.name, loader))
    sys.modules[loader.name] = module
    loader.exec_module(module)
    return module


class HaggaiPsalmSeamTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.propers = load_tool('mass-propers')
        cls.index = load_tool('index-bible')
        cls.canon = load_tool('citations')
        cls.doc = yaml.safe_load(SOURCE.read_text())
        cls.masses = {m['key']: m for s in cls.doc['sections'].values() for m in s['masses']}
        entries = [e for _, m in cls.propers.masses_of(cls.doc)
                   for e, _ in cls.propers.numbered_entries(m, cls.doc['psalm_numbering'])]
        cls.tables = {target: cls.index.Divergences('postconciliar', cls.doc, entries, cls.canon, target)
                      for target in cls.propers.SYSTEMS}
        cls.tokens = cls.propers.book_tokens()
        cls.haggai = next(p for p in cls.masses['ot-25-friday']['propers']
                          if p['name'] == 'First Reading')['weekday_cycles']['I']['verses'][0]
        cls.psalm = next(p for p in cls.masses['ot-24-saturday']['propers']
                         if p['name'] == 'Responsorial Psalm')['weekday_cycles']['II']['verses'][0]

    def test_source_citation_and_both_loci_keep_the_part_and_closing_verse(self):
        self.assertEqual(self.haggai, self.canon.parse_citation('Haggai 1:15b-2:9'))
        corrected, problem = self.tables['vulgate'].apply(self.haggai, self.haggai['ranges'])
        self.assertEqual(problem, '')
        self.assertEqual(corrected, self.canon.parse_citation('Haggai 2:1b-10')['ranges'])
        citation = self.propers.citation_structure(self.haggai, 'hebrew', self.tokens, self.tables)
        self.assertIsNone(citation['unresolved'])
        self.assertEqual(citation['ref'], 'Haggai 1:15b-2:9')
        self.assertEqual(citation['loci']['vulgate'], [{'chapter': 2, 'first': 1, 'last': 10}])
        for addressing in ('hebrew', 'hebrew-unnumbered-titles'):
            self.assertEqual(citation['loci'][addressing], [
                {'chapter': 1, 'first': 15, 'last': None},
                {'chapter': 2, 'first': None, 'last': 9}])

    def test_each_offered_bible_reaches_the_peace_clause_and_excludes_the_next_oracle(self):
        for name, edition in self.index.EDITIONS.items():
            if not edition['publishable']:
                continue
            with self.subTest(bible=name):
                bible = self.index.Bible(self.index.SOURCE_ROOT / str(edition['artifacts']))
                target = str(edition['numbering'])
                ranges, problem = self.tables[target].apply(self.haggai, self.haggai['ranges'])
                self.assertEqual(problem, '')
                text, problem = bible.passage(bible.token('Haggai'), ranges)
                self.assertEqual(problem, '')
                # Parts remain in the citation; existing Bible reconstruction shows
                # the whole opening verse, including its earlier dating clause.
                opening = 'anno secundo Darii' if edition['language'] == 'la' else 'second year'
                closing = 'dabo pacem' if edition['language'] == 'la' else 'peace'
                self.assertIn(opening, text)
                self.assertIn(closing, text)
                self.assertNotIn('noni mensis', text)
                self.assertNotIn('ninth month', text)
                self.assertNotIn('ninth', text)
                self.assertNotIn('Ask now the priests', text)

    def test_the_earlier_appointment_is_an_explicit_identity_and_no_offset_is_inferred(self):
        unchanged = self.canon.parse_citation('Haggai 1:1-8')
        self.assertEqual(self.tables['vulgate'].apply(unchanged, unchanged['ranges']),
                         (unchanged['ranges'], ''))
        unrecorded = self.canon.parse_citation('Haggai 2:10')
        ranges, problem = self.tables['vulgate'].apply(unrecorded, unrecorded['ranges'])
        self.assertEqual(ranges, [])
        self.assertIn('records no resolution', problem)

    def test_raw_haggai_range_is_not_a_success_in_the_selected_douay(self):
        edition = self.index.EDITIONS['douay-rheims']
        bible = self.index.Bible(self.index.SOURCE_ROOT / str(edition['artifacts']))
        text, problem = bible.passage(bible.token('Haggai'), self.haggai['ranges'])
        # This previously returned chapter 2:1-9 after an empty chapter tail.
        # The canonical source mapping must reach the positive peace assertion above.
        self.assertNotIn('I will give peace', text)

    def test_printed_psalm_endpoint_is_preserved_and_the_unmapped_unit_refuses_whole(self):
        self.assertEqual(self.psalm['ref'], 'Psalm 56:10, 11-12, 13-14')
        self.assertEqual(self.psalm['ranges'][-1]['end']['verse'], 14)
        citation = self.propers.citation_structure(self.psalm, 'hebrew', self.tokens, self.tables)
        self.assertEqual(citation['loci'], {})
        self.assertIn('would drop verse 14', citation['unresolved'])
        _, ranges, problem = self.index.citation(self.psalm, 'hebrew', 'vulgate', self.propers)
        self.assertEqual(ranges, [])
        self.assertIn('would drop verse 14', problem)

    def test_the_psalm_witnesses_confirm_a_division_gap_without_supplying_a_new_map(self):
        for name in ('douay-rheims', 'clementine-vulgate'):
            edition = self.index.EDITIONS[name]
            bible = self.index.Bible(self.index.SOURCE_ROOT / str(edition['artifacts']))
            self.assertEqual(bible.chapters[('Ps', 55)][1], 13)
            self.assertIsNone(bible.carrier('Ps', 55, 14))
            self.assertTrue(bible.verse('Ps', 55, 13))
        from _psalms import english_verse
        verse, problem = english_verse(56, 14)
        self.assertIsNone(verse)
        self.assertIn('divide', problem)


if __name__ == '__main__':
    unittest.main()
