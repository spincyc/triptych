"""The browser structure must use the calendar's held citation decisions."""

from __future__ import annotations

import sys
import unittest
from importlib.machinery import SourceFileLoader
from importlib.util import module_from_spec, spec_from_loader
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'scripts'))


def load_tool(name):
    loader = SourceFileLoader('_citation_structure_' + name.replace('-', '_'), str(ROOT / 'tools' / name))
    module = module_from_spec(spec_from_loader(loader.name, loader))
    sys.modules[loader.name] = module
    loader.exec_module(module)
    return module


propers = load_tool('mass-propers')
index = load_tool('index-bible')
canon = load_tool('citations')
from _loci import Divergences as SharedDivergences


def citations(value):
    if isinstance(value, dict):
        if 'ref' in value and 'token' in value and 'loci' in value:
            yield value
        for child in value.values():
            yield from citations(child)
    elif isinstance(value, list):
        for child in value:
            yield from citations(child)


class CalendarCitationDivergenceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tokens = propers.book_tokens()
        cls.document = propers.load_calendar(propers.DEFAULT_ROOT, 'postconciliar')
        entries = [entry for _, mass in propers.masses_of(cls.document)
                   for entry, _ in propers.numbered_entries(mass, cls.document['psalm_numbering'])]
        cls.tables = {target: index.Divergences('postconciliar', cls.document, entries, canon, target)
                      for target in propers.SYSTEMS}
        structure = propers.calendar_structure(propers.DEFAULT_ROOT, 'postconciliar', cls.tokens)
        cls.by_ref = {}
        for citation in citations(structure):
            cls.by_ref.setdefault(citation['ref'], []).append(citation)

    def test_index_compatibility_inherits_the_single_resolver(self):
        for method in ('_declare', '_stances', '_chapters', '_resolve', 'locus_of', 'stance', 'apply', 'confirm'):
            self.assertIs(getattr(index.Divergences, method), getattr(SharedDivergences, method))
        self.assertEqual(index.Divergences('empty', {}, [], canon).numbering, index.RESOLVED_IN)
        self.assertEqual(index.Divergences('empty', {}, [], canon).numberings, index.other_numberings())
        self.assertEqual(tuple(system for system in propers.SYSTEMS if system != index.RESOLVED_IN),
                         index.other_numberings())

    def test_calendar_structure_carries_all_fourteen_held_targets(self):
        expected = {
            'Malachi 3:1-4, 23-24': [(3, 1, 4), (4, 5, 6)],
            'Isaiah 8:23b-9:3': [(9, 1, 4)],
            'Mark 4:35-41': [(4, 35, 40)],
            'Acts 14:19-28': [(14, 18, 27)],
            'Zechariah 2:14-17': [(2, 10, 13)],
            'Matthew 17:22-27': [(17, 21, 26)],
            'Mark 9:41-50': [(9, 40, 49)],
            'Genesis 49:29-32; 50:15-26a': [(49, 29, 31), (50, 15, 25)],
            'Exodus 40:16-21, 34-38': [(40, 14, 19), (40, 32, 36)],
            'Zechariah 2:5-9, 14-15a': [(2, 1, 5), (2, 10, 11)],
            'Malachi 3:13-20a': [(3, 13, 18), (4, 1, 2)],
            'Joel 4:12-21': [(3, 12, 21)],
            'Acts 7:55-60': [(7, 55, 59)],
            'Malachi 3:19-20a': [(4, 1, 2)],
        }
        for reference, loci in expected.items():
            with self.subTest(reference=reference):
                self.assertIn(reference, self.by_ref)
                for citation in self.by_ref[reference]:
                    self.assertEqual(citation['loci']['vulgate'], [
                        {'chapter': chapter, 'first': first, 'last': last}
                        for chapter, first, last in loci
                    ])

    def test_non_psalm_addressings_keep_the_recorded_stances(self):
        self.assertEqual(self.by_ref['Joel 4:12-21'][0]['loci']['hebrew'],
                         [{'chapter': 3, 'first': 12, 'last': 21}])
        self.assertEqual(self.by_ref['Mark 9:41-50'][0]['loci']['hebrew'],
                         [{'chapter': 9, 'first': 41, 'last': 50}])

    def test_unrecorded_citation_refuses_each_addressing(self):
        citation = propers.citation_structure(canon.parse_citation('Joel 4:18'), 'hebrew', self.tokens, self.tables)
        self.assertEqual(citation['loci'], {})
        self.assertEqual(set(citation['refused']), {'vulgate', 'hebrew', 'hebrew-unnumbered-titles'})
        self.assertTrue(all('records no resolution' in reason for reason in citation['refused'].values()))

    def test_unruled_numbering_refuses_without_hiding_other_numberings(self):
        citation = propers.citation_structure(canon.parse_citation('John 6:51'), 'hebrew', self.tokens, self.tables)
        self.assertEqual(citation['loci']['vulgate'], [{'chapter': 6, 'first': 51, 'last': 52}])
        self.assertNotIn('hebrew', citation['loci'])
        self.assertIn('unrecorded', citation['refused']['hebrew'])

    def test_three_argument_call_has_no_calendar_to_correct(self):
        citation = propers.citation_structure(canon.parse_citation('Joel 4:12-21'), 'hebrew', self.tokens)
        self.assertEqual(citation['loci']['vulgate'], [{'chapter': 4, 'first': 12, 'last': 21}])

    def test_psalm_edition_departure_still_runs_after_calendar_rules(self):
        citation = propers.citation_structure(canon.parse_citation('Psalm 116:10-19'), 'hebrew', self.tokens, self.tables)
        self.assertEqual(citation['loci']['vulgate'], [{'chapter': 115, 'first': 10, 'last': 19}])
        self.assertEqual(citation['edition_loci']['clementine-vulgate'],
                         [{'chapter': 115, 'first': 1, 'last': 10}])


if __name__ == '__main__':
    unittest.main()
