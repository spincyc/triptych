"""Hold the selected Challoner words at the explicitly collated tail loci."""
from __future__ import annotations

import sys
import unittest
from importlib.machinery import SourceFileLoader
from importlib.util import module_from_spec, spec_from_loader
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'scripts'))
loader = SourceFileLoader('_thessalonian_index_bible', str(ROOT / 'tools/index-bible'))
index = module_from_spec(spec_from_loader(loader.name, loader))
loader.exec_module(index)
canon = index.sibling('citations')
import _loci


class ThessalonianAliases(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        artifacts = ROOT / 'src/sources/works' / index.EDITIONS['douay-rheims']['artifacts']
        cls.bible = index.Bible(artifacts)

    def reading(self, reference):
        entry = canon.parse_citation(reference)
        return self.bible.passage(self.bible.token(entry['book']), entry['ranges'])

    def test_ot_32_short_is_ignorance_and_resurrection(self):
        text, problem = self.reading('1 Thessalonians 4:13-14')
        self.assertEqual(problem, '')
        self.assertTrue(text.startswith('And we will not have you ignorant brethren'))
        self.assertTrue(text.endswith('will God bring with him.'))
        self.assertNotIn('For this we say unto you', text)

    def test_ot_32_long_keeps_the_final_comfort(self):
        text, problem = self.reading('1 Thessalonians 4:13-18')
        self.assertEqual(problem, '')
        self.assertTrue(text.startswith('And we will not have you ignorant brethren'))
        self.assertTrue(text.endswith('Wherefore, comfort ye one another with these words.'))

    def test_second_thessalonians_fourteen_is_glory(self):
        text, problem = self.reading('2 Thessalonians 2:14')
        self.assertEqual(problem, '')
        self.assertIn('purchasing of the glory', text)
        self.assertNotIn('hold the traditions', text)

    def test_cross_chapter_reading_keeps_both_consolation_and_exhortation(self):
        text, problem = self.reading('2 Thessalonians 2:16-3:5')
        self.assertEqual(problem, '')
        self.assertTrue(text.startswith('Now our Lord Jesus Christ himself'))
        self.assertIn('Exhort your hearts and confirm you in every good work and word.', text)
        self.assertTrue(text.endswith('the patience of Christ.'))

    def test_whole_chapters_conservatively_refuse_unisolatable_seams(self):
        for token, chapter in [('1Thess', 4), ('2Thess', 2)]:
            with self.subTest(token=token):
                text, problem = self.bible.passage(token, [{'begin': {'chapter': chapter},
                                                           'end': {'chapter': chapter}}])
                self.assertEqual(text, '')
                self.assertIn('joins Clementine', problem)
                self.assertIn('cannot isolate', problem)
                self.assertTrue(problem.endswith(index.NOT_CARRIED), problem)

    def test_exact_tail_loci_and_adjacent_defaults(self):
        pairs = [('1Thess', 4, 13, 12), ('1Thess', 4, 14, 13), ('1Thess', 4, 15, 14),
                 ('1Thess', 4, 16, 15), ('1Thess', 4, 17, 16), ('1Thess', 4, 18, 17),
                 ('2Thess', 2, 12, 11), ('2Thess', 2, 13, 12), ('2Thess', 2, 14, 13),
                 ('2Thess', 2, 15, 14), ('2Thess', 2, 16, 15), ('2Thess', 2, 17, 16)]
        for token, chapter, cited, printed in pairs:
            with self.subTest(locus=(token, chapter, cited)):
                self.assertEqual(self.bible.carrier(token, chapter, cited), (token, chapter, printed))
        for locus in [('1Thess', 3, 13), ('1Thess', 5, 1), ('2Thess', 2, 9), ('2Thess', 3, 1)]:
            self.assertEqual(self.bible.carrier(*locus), locus)

    def test_no_exact_alias_is_claimed_for_a_half_of_a_joined_verse(self):
        for locus in [('1Thess', 4, 11), ('1Thess', 4, 12), ('2Thess', 2, 10), ('2Thess', 2, 11)]:
            self.assertIn(locus, self.bible.aliases)
            self.assertIsNone(self.bible.aliases[locus])

    def test_unknown_tails_still_refuse(self):
        for reference in ['1 Thessalonians 4:19', '2 Thessalonians 2:18']:
            text, problem = self.reading(reference)
            self.assertEqual(text, '')
            self.assertIn('verse aliases', problem)

    def test_browser_departures_preserve_reference_parts_and_existing_api(self):
        propers = index.sibling('mass-propers')
        entry = canon.parse_citation('2 Thessalonians 2:1-3a, 14-17')
        structured = propers.citation_structure(entry, 'hebrew', propers.book_tokens())
        self.assertEqual(structured['ref'], '2 Thessalonians 2:1-3a, 14-17')
        self.assertEqual(structured['edition_loci']['douay-rheims'],
                         [{'chapter': 2, 'first': 1, 'last': 3},
                          {'chapter': 2, 'first': 13, 'last': 16}])
        self.assertEqual(entry['ranges'][0]['end']['part'], 'a')

    def test_all_four_isolated_seam_points_explain_held_joined_words(self):
        for reference in ['1 Thessalonians 4:11', '1 Thessalonians 4:12',
                          '2 Thessalonians 2:10', '2 Thessalonians 2:11']:
            text, problem = self.reading(reference)
            self.assertEqual(text, '')
            self.assertIn('joins Clementine', problem)
            self.assertIn('words are held', problem)
            self.assertIn('cannot isolate', problem)
            self.assertNotIn('not carried', problem)

    def test_actual_saturday_first_reading_refuses_only_affected_edition(self):
        propers = index.sibling('mass-propers')
        document = propers.load_calendar(ROOT / 'src/sources/calendars', 'postconciliar')
        mass = next(mass for _, mass in propers.masses_of(document) if mass['key'] == 'ot-21-saturday')
        proper = next(row for row in mass['propers'] if row['name'] == 'First Reading')
        entry, = proper['weekday_cycles']['I']['verses']
        self.assertEqual(entry['ref'], '1 Thessalonians 4:9-11')
        text, problem = self.bible.passage(self.bible.token(entry['book']), entry['ranges'])
        self.assertEqual(text, '')
        self.assertIn('cannot isolate', problem)
        structured = propers.citation_structure(entry, document['psalm_numbering'], propers.book_tokens())
        self.assertIn('cannot isolate', structured['refused']['douay-rheims'])
        self.assertNotIn('clementine-vulgate', structured.get('refused', {}))


if __name__ == '__main__':
    unittest.main()
