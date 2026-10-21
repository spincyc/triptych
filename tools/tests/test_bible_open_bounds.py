"""Open passages include the endpoint proved by the edition's own aliases."""
from __future__ import annotations

import sys
import unittest
from importlib.machinery import SourceFileLoader
from importlib.util import module_from_spec, spec_from_loader
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'scripts'))
loader = SourceFileLoader('_open_bounds_index_bible', str(ROOT / 'tools/index-bible'))
index = module_from_spec(spec_from_loader(loader.name, loader))
loader.exec_module(index)


def whole(chapter, first=None, last=None):
    return {'begin': {'chapter': chapter, **({} if first is None else {'verse': first})},
            'end': {'chapter': chapter, **({} if last is None else {'verse': last})}}


def fixture(verses, aliases):
    with patch.multiple(index, load_books=lambda _: {}, load_verses=lambda _: verses,
                        load_aliases=lambda _: aliases):
        return index.Bible(Path('unused'))


class OpenBoundTests(unittest.TestCase):
    def test_recorded_final_carrier_extends_an_open_tail(self):
        bible = fixture({('X', 1, 1): 'one', ('X', 1, 2): 'joined', ('X', 1, 3): 'last'},
                        {('X', 1, 3): ('X', 1, 2), ('X', 1, 4): ('X', 1, 3)})
        self.assertEqual(bible.passage('X', [whole(1)]), ('one joined last', ''))
        self.assertEqual(bible.passage('X', [whole(1, 3)]), ('joined last', ''))
        self.assertEqual(bible.chapters[('X', 1)], (1, 3))

    def test_explicit_end_is_not_extended(self):
        bible = fixture({('X', 1, 1): 'one', ('X', 1, 2): 'joined', ('X', 1, 3): 'last'},
                        {('X', 1, 3): ('X', 1, 2), ('X', 1, 4): ('X', 1, 3)})
        self.assertEqual(bible.passage('X', [whole(1, 3, 3)]), ('joined', ''))

    def test_no_unrecorded_verse_is_inferred_between_known_endpoints(self):
        bible = fixture({('X', 1, 1): 'one', ('X', 1, 2): 'last'},
                        {('X', 1, 4): ('X', 1, 2)})
        text, problem = bible.passage('X', [whole(1)])
        self.assertEqual(text, '')
        self.assertIn('X 1:3 is past X 1:2', problem)

    def test_full_remapping_uses_recorded_first_and_last(self):
        bible = fixture({('X', 1, 1): 'one', ('X', 1, 2): 'two'},
                        {('X', 1, 10): ('X', 1, 1), ('X', 1, 11): ('X', 1, 2)})
        self.assertEqual(bible.passage('X', [whole(1)]), ('one two', ''))
        self.assertEqual(bible.passage('X', [whole(1, 10)]), ('one two', ''))

    def test_partial_alias_does_not_invent_a_new_first_number(self):
        bible = fixture({('X', 1, 1): 'one', ('X', 1, 2): 'two', ('X', 1, 3): 'three'},
                        {('X', 1, 5): ('X', 1, 1)})
        self.assertEqual(bible.passage('X', [whole(1)]), ('one two three', ''))

    def test_recorded_refusal_remains_final(self):
        bible = fixture({('X', 1, 1): 'one', ('X', 1, 2): 'two'},
                        {('X', 1, 2): None, ('X', 1, 3): ('X', 1, 2)})
        text, problem = bible.passage('X', [whole(1)])
        self.assertEqual(text, '')
        self.assertIn(index.NOT_CARRIED, problem)

    def test_missing_chapter_still_uses_only_recorded_loci(self):
        bible = fixture({('Y', 2, 1): 'one', ('Y', 2, 2): 'two'},
                        {('X', 1, 10): ('Y', 2, 1), ('X', 1, 11): ('Y', 2, 2)})
        self.assertEqual(bible.passage('X', [whole(1)]), ('one two', ''))

    def test_cross_chapter_aliases_do_not_claim_a_same_chapter_extent(self):
        bible = fixture({('X', 1, 1): 'one', ('X', 1, 2): 'two', ('Y', 2, 1): 'other'},
                        {('X', 1, 3): ('X', 1, 2), ('X', 1, 4): ('Y', 2, 1)})
        self.assertEqual(bible.passage('X', [whole(1)]), ('one two', ''))
        self.assertNotIn(('X', 1), bible.open_bounds)


class HeldPsalmControls(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        artifacts = ROOT / 'src/sources/works' / index.EDITIONS['clementine-vulgate']['artifacts']
        cls.bible = index.Bible(artifacts)

    def test_restarted_psalms_read_every_printed_verse_once(self):
        for edition in ['clementine-vulgate', 'catholic-public-domain-version', 'douay-rheims-american-1899']:
            bible = index.Bible(ROOT / 'src/sources/works' / index.EDITIONS[edition]['artifacts'])
            for chapter, first in [(115, 10), (147, 12)]:
                with self.subTest(edition=edition, chapter=chapter):
                    expected = ' '.join(text for (token, at, verse), text in sorted(bible.verses.items())
                                        if token == 'Ps' and at == chapter)
                    self.assertEqual(bible.passage('Ps', [whole(chapter)]), (expected, ''))
                    self.assertEqual(bible.passage('Ps', [whole(chapter, first)]), (expected, ''))

    def test_psalm_42_unmodeled_division_still_refuses(self):
        text, problem = self.bible.passage('Ps', [whole(42)])
        self.assertEqual(text, '')
        self.assertIn(index.NOT_CARRIED, problem)

    def test_an_explicit_unrecorded_psalm_tail_still_refuses(self):
        text, problem = self.bible.passage('Ps', [whole(147, 12, 21)])
        self.assertEqual(text, '')
        self.assertIn('Ps 147:21', problem)


if __name__ == '__main__':
    unittest.main()
