"""Exact whole-verse carriers for two ICEL2010 seasonal source cues.

AP17/printed9: Cf. Haggai2:7. AP27/edition pagination19: Wisdom11:23,24,26.
No antiphon words, part cuts, exact2008 bodies or rights are certified.
"""
from __future__ import annotations

import copy
import hashlib
from importlib.machinery import SourceFileLoader
from importlib.util import module_from_spec, spec_from_loader
from pathlib import Path
import re
import sys
import unicodedata
import unittest

ROOT = Path(__file__).resolve().parents[2]
CALENDAR_ROOT = ROOT / 'src/sources/calendars'
sys.path.insert(0, str(ROOT / 'scripts'))


def load(name):
    loader = SourceFileLoader('_seasonal_exact_carrier_' + name.replace('-', '_'), str(ROOT / 'tools' / name))
    module = module_from_spec(spec_from_loader(loader.name, loader))
    sys.modules[loader.name] = module
    loader.exec_module(module)
    return module


propers = load('mass-propers')
index = load('index-bible')
canon = load('citations')

EXPECTED = {'Haggai 2:7': {'douay-rheims': 'e834935d8d525229446b4a172751856f8886fc9e53f7eb598bf3b854eae88fdb', 'douay-rheims-american-1899': 'e834935d8d525229446b4a172751856f8886fc9e53f7eb598bf3b854eae88fdb', 'clementine-vulgate': '06f570182958afc9453f3f2c63dc9faf9fcdc85a277809bbe056f932f2c09839', 'king-james-version': 'ff216cce7945318d29e7cd021036234a514cb1d0373598b76c627af9b2b8df8e', 'world-english-bible-catholic': '1858f2e3fda6ef64f427e089816e3c49104b7ddbafa41b69da2f6657692b5fa5', 'catholic-public-domain-version': '6af8bca9578d221d6fffcbd3681493cae262c670d18ff7a06fcbf99d76589c9f', 'revised-version-1895': '4ea23c1ee58840cb5b10e94c09cd2426bb1bb814978a99637d14008a59aef4d6'}, 'Wisdom 11:23, 24, 26': {'douay-rheims': '579011c0497394aaec1d113675354cc0eba5928d7742acc8af579934ba39c154', 'douay-rheims-american-1899': '579011c0497394aaec1d113675354cc0eba5928d7742acc8af579934ba39c154', 'clementine-vulgate': '1f29af98b3f8d1951c701d8ab831d9928408e592c5ce65d4431dbeddc0b819e5', 'king-james-version': 'e38ad015e61b47ca76a9f41efc095e8256fb52d187cab87a0ef9c65953b03219', 'world-english-bible-catholic': 'a33bf6820341ae5acf37997d0d128e44bebd5688d6ce56ed5cab02e8d3281781', 'catholic-public-domain-version': '746f42db5ee7e8e0b5e0b3ecec629f1faf3660c7b9f648d9feeb31254b6824de', 'revised-version-1895': 'cb51f88d8c64b5d42b76c5ac59b4de6a45f5d1eb3e0d2e9f2a91b6b363d32a7a'}}
SPECS = {
    'Haggai 2:7': ('advent-december-17', 'Communion Antiphon', 'Haggai 2:8'),
    'Wisdom 11:23, 24, 26': ('ash-wednesday', 'Entrance Antiphon', 'Wisdom 11:24-25, 27'),
}


def tables(doc, entries):
    return {n: index.Divergences('postconciliar', doc, entries, canon, n) for n in propers.SYSTEMS}


def words(text):
    text = unicodedata.normalize('NFKD', text.lower().replace('æ', 'ae').replace('œ', 'oe'))
    return ' '.join(re.findall('[a-z]+', text.encode('ascii', 'ignore').decode()))


class SeasonalExactCarrierTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.doc = propers.load_calendar(CALENDAR_ROOT, 'postconciliar')
        cls.masses = {m['key']: m for _, m in propers.masses_of(cls.doc)}
        cls.entries = [e for m in cls.masses.values() for e, _ in propers.numbered_entries(m, cls.doc['psalm_numbering'])]
        cls.tables = tables(cls.doc, cls.entries)
        cls.loci = {r['book']: r for r in cls.doc['citation_divergences']}
        cls.tokens = propers.book_tokens()

    def test_only_the_actual_source_refs_get_one_scalar_row_each(self):
        for ref, (mass, role, target) in SPECS.items():
            with self.subTest(ref=ref):
                book = canon.parse_citation(ref)['book']
                self.assertIn(ref, self.loci[book]['citations'])
                self.assertEqual(self.loci[book]['citations'][ref], target)
                appointed = [p for label, p in propers.propers_of(self.masses[mass]) if label == '' and p.get('name') == role]
                self.assertEqual(len(appointed), 1)
                self.assertIn(ref, {v['ref'] for v in appointed[0].get('verses', [])})

    def test_all_fourteen_exact_held_bible_carriers(self):
        checked = 0
        for ref, (_, _, vulgate) in SPECS.items():
            e = canon.parse_citation(ref)
            structured = propers.citation_structure(e, 'hebrew', self.tokens, self.tables)
            self.assertEqual(structured['ref'], ref)
            for edition, digest in EXPECTED[ref].items():
                with self.subTest(ref=ref, edition=edition):
                    cfg = index.EDITIONS[edition]
                    bible = index.Bible(ROOT / 'src/sources/works' / cfg['artifacts'])
                    ranges, error = self.tables[cfg['numbering']].apply(e, e['ranges'])
                    self.assertEqual(error, '')
                    expected = canon.parse_citation(vulgate if cfg['numbering'] == 'vulgate' else ref)['ranges']
                    self.assertEqual(ranges, expected)
                    text, error = bible.passage(bible.token(e['book']), ranges)
                    self.assertEqual(error, '')
                    self.assertEqual(hashlib.sha256(text.encode()).hexdigest(), digest)
                    self.assertEqual(structured['loci'][cfg['numbering']], [
                        {'chapter': s['begin']['chapter'], 'first': s['begin']['verse'], 'last': s['end']['verse']} for s in ranges])
                    for span in ranges:
                        self.assertNotIn('part', span['begin'])
                        self.assertNotIn('part', span['end'])
                    text_words = words(text)
                    if e['book'] == 'Haggai':
                        self.assertIn('domum' if cfg['language'] == 'la' else 'house', text_words)
                        self.assertIn('gloria' if cfg['language'] == 'la' else 'glory', text_words)
                    else:
                        self.assertIn('misereris' if cfg['language'] == 'la' else 'merci' if edition == 'catholic-public-domain-version' else 'mercy', text_words)
                        self.assertIn('diligis' if cfg['language'] == 'la' else 'love', text_words)
                        self.assertIn('parcis' if cfg['language'] == 'la' else 'spare', text_words)
                        self.assertEqual(ranges[-1]['end']['verse'], 27 if cfg['numbering'] == 'vulgate' else 26)
                    checked += 1
        self.assertEqual(checked, 14)

    def test_eight_raw_vulgate_as_cited_carriers_are_excluded(self):
        checked = 0
        for ref in SPECS:
            e = canon.parse_citation(ref)
            for edition in EXPECTED[ref]:
                cfg = index.EDITIONS[edition]
                if cfg['numbering'] != 'vulgate':
                    continue
                with self.subTest(ref=ref, edition=edition):
                    bible = index.Bible(ROOT / 'src/sources/works' / cfg['artifacts'])
                    token = bible.token(e['book'])
                    raw, error = bible.passage(token, e['ranges'])
                    self.assertEqual(error, '')
                    ranges, error = self.tables['vulgate'].apply(e, e['ranges'])
                    self.assertEqual(error, '')
                    selected, error = bible.passage(token, ranges)
                    self.assertEqual(error, '')
                    self.assertNotEqual(raw, selected)
                    if e['book'] == 'Haggai':
                        self.assertIn('caelum' if cfg['language'] == 'la' else 'heaven', words(raw))
                        self.assertNotIn('gloria' if cfg['language'] == 'la' else 'glory', words(raw))
                    else:
                        self.assertIn('roris' if cfg['language'] == 'la' else 'dew', words(raw))
                        self.assertNotIn('parcis' if cfg['language'] == 'la' else 'spare', words(raw))
                    checked += 1
        self.assertEqual(checked, 8)

    def test_the_baseline_safely_refuses_vulgate_and_keeps_correct_hebrew(self):
        before = copy.deepcopy(self.doc)
        for locus in before['citation_divergences']:
            for ref in SPECS:
                locus.get('citations', {}).pop(ref, None)
        baseline = tables(before, self.entries)
        for ref in SPECS:
            e = canon.parse_citation(ref)
            ranges, error = baseline['vulgate'].apply(e, e['ranges'])
            self.assertEqual(ranges, [])
            self.assertIn('records no resolution', error)
            self.assertEqual(baseline['hebrew'].apply(e, e['ranges']), (e['ranges'], ''))

    def test_both_existing_haggai_and_all_three_wisdom_rows_stay_exact(self):
        for ref, target in {'Haggai 1:1-8':'Haggai 1:1-8','Haggai 1:15b-2:9':'Haggai 2:1b-10'}.items():
            self.assertEqual(self.loci['Haggai']['citations'][ref], target)
        for ref, target in {'Wisdom 6:1-11':'Wisdom 6:2-12','Wisdom 6:12-16':'Wisdom 6:13-17','Wisdom 11:22-12:2':'Wisdom 11:23-12:2'}.items():
            self.assertEqual(self.loci['Wisdom']['citations'][ref], target)
        self.assertEqual(self.loci['Haggai']['chapters'], [1,2])
        self.assertEqual(self.loci['Wisdom']['chapters'], [6,11])
        for book in ['Haggai','Wisdom']:
            self.assertEqual(self.loci[book]['numbering'], {'hebrew':'as-cited'})

    def test_unlisted_ref_queries_keep_the_existing_refusal_and_fallback(self):
        for ref in ['Haggai 2:10','Haggai 2:8','Wisdom 11:25','Wisdom 11:24-25, 27']:
            e = canon.parse_citation(ref)
            ranges, error = self.tables['vulgate'].apply(e, e['ranges'])
            self.assertEqual(ranges, [])
            self.assertIn('records no resolution', error)
            self.assertEqual(self.tables['hebrew'].apply(e, e['ranges']), (e['ranges'], ''))

    def test_maps_without_the_new_appointments_fail_the_existing_stale_guard(self):
        for ref in SPECS:
            with self.subTest(ref=ref), self.assertRaisesRegex(ValueError, 'no longer cited'):
                tables(self.doc, [e for e in self.entries if e['ref'] != ref])

    def test_other_citation_results_and_explicit_alternate_set_are_unchanged(self):
        before = copy.deepcopy(self.doc)
        for locus in before['citation_divergences']:
            for ref in SPECS:
                locus.get('citations', {}).pop(ref, None)
        baseline = tables(before, self.entries)
        checked = 0
        for e in {e['ref']:e for e in self.entries}.values():
            if e['ref'] in SPECS:
                continue
            for numbering in propers.SYSTEMS:
                self.assertEqual(baseline[numbering].apply(e,e['ranges']), self.tables[numbering].apply(e,e['ranges']))
                checked += 1
        self.assertGreater(checked,1000)
        self.assertEqual(baseline['hebrew'].addressed, self.tables['hebrew'].addressed)


if __name__ == '__main__':
    unittest.main()
