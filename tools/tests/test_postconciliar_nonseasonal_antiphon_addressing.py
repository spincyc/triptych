"""Three source-printed antiphon refs have exact whole-verse Bible carriers.

ICEL2010 artifact e6b82741: AP117/printed109, AP146/printed138,
AP150/printed142. This certifies no antiphon wording, cuts, 2008 body or rights.
"""
from __future__ import annotations

import copy
import hashlib
from importlib.machinery import SourceFileLoader
from importlib.util import module_from_spec, spec_from_loader
from pathlib import Path
import re
import sys
import tomllib
import unicodedata
import unittest

ROOT = Path(__file__).resolve().parents[2]
CALENDAR_ROOT = ROOT / 'src/sources/calendars'
EVIDENCE = ROOT / 'src/sources/inventories/postconciliar-nonseasonal-antiphon-addressing-v1.toml'
sys.path.insert(0, str(ROOT / 'scripts'))


def load(name):
    loader = SourceFileLoader('_nonseasonal_exact_' + name.replace('-', '_'), str(ROOT / 'tools' / name))
    module = module_from_spec(spec_from_loader(loader.name, loader))
    sys.modules[loader.name] = module
    loader.exec_module(module)
    return module


propers = load('mass-propers')
index = load('index-bible')
canon = load('citations')


def words(text):
    text = text.lower().replace('æ', 'ae').replace('œ', 'oe')
    text = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode()
    return ' '.join(re.findall(r'[a-z]+', text))


def tables(document, entries):
    return {n: index.Divergences('postconciliar', document, entries, canon, n) for n in propers.SYSTEMS}


class HeldNonseasonalAntiphonAddressingTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.evidence = tomllib.loads(EVIDENCE.read_text())
        cls.decisions = cls.evidence['decisions']
        cls.document = propers.load_calendar(CALENDAR_ROOT, 'postconciliar')
        cls.masses = {m['key']: m for _, m in propers.masses_of(cls.document)}
        cls.entries = [e for m in cls.masses.values()
                       for e, _ in propers.numbered_entries(m, cls.document['psalm_numbering'])]
        cls.tables = tables(cls.document, cls.entries)
        cls.tokens = propers.book_tokens()
        cls.loci = {r['book']: r for r in cls.document['citation_divergences']}

    def test_exact_maps_are_attached_to_the_actual_new_appointments(self):
        expected = {
            'Malachi 2:6': {'vulgate': 'Malachi 2:6', 'hebrew': 'Malachi 2:6'},
            'John 6:69, 70': {'vulgate': 'John 6:69, 70', 'hebrew': 'John 6:68, 69'},
            'Acts 7:58': {'vulgate': 'Acts 7:58', 'hebrew': 'Acts 7:59'},
        }
        self.assertEqual({d['source_ref']: d['targets'] for d in self.decisions}, expected)
        for d in self.decisions:
            with self.subTest(ref=d['source_ref']):
                e = canon.parse_citation(d['source_ref'])
                self.assertIn(d['source_ref'], self.loci[e['book']]['citations'])
                self.assertEqual(self.loci[e['book']]['citations'][d['source_ref']], expected[d['source_ref']])
                appointed = [p for label, p in propers.propers_of(self.masses[d['mass']])
                             if label == '' and p.get('name') == d['proper']]
                self.assertEqual(len(appointed), 1)
                self.assertIn(d['source_ref'], {v['ref'] for v in appointed[0].get('verses', [])})

    def test_all_twenty_one_held_whole_verse_carriers(self):
        self.assertEqual(sum(len(d['carriers']) for d in self.decisions), 21)
        for d in self.decisions:
            e = canon.parse_citation(d['source_ref'])
            structured = propers.citation_structure(e, 'hebrew', self.tokens, self.tables)
            self.assertEqual(structured['ref'], d['source_ref'])
            for held in d['carriers']:
                with self.subTest(ref=d['source_ref'], edition=held['edition']):
                    cfg = index.EDITIONS[held['edition']]
                    bible = index.Bible(ROOT / 'src/sources/works' / cfg['artifacts'])
                    ranges, problem = self.tables[cfg['numbering']].apply(e, e['ranges'])
                    self.assertEqual(problem, '')
                    self.assertEqual(ranges, canon.parse_citation(held['ref'])['ranges'])
                    self.assertEqual(structured['loci'][cfg['numbering']], [
                        {'chapter': s['begin']['chapter'], 'first': s['begin']['verse'], 'last': s['end']['verse']}
                        for s in ranges])
                    self.assertEqual(structured['loci']['hebrew'], structured['loci']['hebrew-unnumbered-titles'])
                    token = bible.token(e['book'])
                    text, problem = bible.passage(token, ranges)
                    self.assertEqual(problem, '')
                    self.assertEqual(hashlib.sha256(text.encode()).hexdigest(), held['text_sha256'])
                    whole = []
                    for s in ranges:
                        self.assertNotIn('part', s['begin'])
                        self.assertNotIn('part', s['end'])
                        self.assertEqual(s['begin']['chapter'], s['end']['chapter'])
                        whole.extend(bible.verses[bible.carrier(token, s['begin']['chapter'], v)]
                                     for v in range(s['begin']['verse'], s['end']['verse'] + 1))
                    self.assertEqual(text, ' '.join(whole))
                    cue = d['latin_bible_cue'] if cfg['language'] == 'la' else d['english_bible_cue']
                    self.assertIn(cue, words(text))

    def test_six_wrong_hebrew_as_cited_carriers_are_excluded(self):
        checked = 0
        for d in self.decisions:
            if d['source_ref'] == 'Malachi 2:6':
                continue
            e = canon.parse_citation(d['source_ref'])
            forbidden = 'devil' if e['book'] == 'John' else 'saul'
            for held in d['carriers']:
                cfg = index.EDITIONS[held['edition']]
                if cfg['numbering'] != 'hebrew':
                    continue
                with self.subTest(ref=d['source_ref'], edition=held['edition']):
                    bible = index.Bible(ROOT / 'src/sources/works' / cfg['artifacts'])
                    token = bible.token(e['book'])
                    raw, problem = bible.passage(token, e['ranges'])
                    self.assertEqual(problem, '')
                    self.assertIn(forbidden, words(raw))
                    ranges, problem = self.tables['hebrew'].apply(e, e['ranges'])
                    self.assertEqual(problem, '')
                    corrected, problem = bible.passage(token, ranges)
                    self.assertEqual(problem, '')
                    self.assertNotEqual(raw, corrected)
                    self.assertNotIn(forbidden, words(corrected))
                    self.assertIn(d['english_bible_cue'], words(corrected))
                    checked += 1
        self.assertEqual(checked, 6)

    def test_unlisted_refs_keep_the_existing_locus_policies(self):
        self.assertEqual(self.loci['Malachi']['numbering'], {'hebrew': 'resolved'})
        self.assertEqual(self.loci['John']['numbering'], {'hebrew': 'unrecorded'})
        self.assertEqual(self.loci['Acts']['numbering'], {'hebrew': 'as-cited'})
        for ref in ['Malachi 2:7', 'John 6:66']:
            e = canon.parse_citation(ref)
            for table in self.tables.values():
                with self.subTest(ref=ref, numbering=table.numbering):
                    ranges, problem = table.apply(e, e['ranges'])
                    self.assertEqual(ranges, [])
                    self.assertTrue(problem)
        e = canon.parse_citation('Acts 7:57')
        ranges, problem = self.tables['vulgate'].apply(e, e['ranges'])
        self.assertEqual(ranges, [])
        self.assertTrue(problem)
        self.assertEqual(self.tables['hebrew'].apply(e, e['ranges']), (e['ranges'], ''))

    def test_new_maps_do_not_change_any_other_citation_result(self):
        old = copy.deepcopy(self.document)
        for locus in old['citation_divergences']:
            for d in self.decisions:
                locus.get('citations', {}).pop(d['source_ref'], None)
        before = tables(old, self.entries)
        new_refs = {d['source_ref'] for d in self.decisions}
        checked = 0
        for e in {e['ref']: e for e in self.entries}.values():
            if e['ref'] in new_refs:
                continue
            for numbering in propers.SYSTEMS:
                self.assertEqual(before[numbering].apply(e, e['ranges']), self.tables[numbering].apply(e, e['ranges']))
                checked += 1
        self.assertGreater(checked, 1000)
        self.assertEqual(self.loci['John']['citations']['John 6:54'], 'John 6:55')
        self.assertEqual(self.loci['John']['citations']['John 6:64b, 69b'],
                         {'vulgate': 'John 6:64b, 69b', 'hebrew': 'John 6:63c, 68c'})

    def test_the_stale_ref_guard_requires_each_new_appointment(self):
        for d in self.decisions:
            with self.subTest(ref=d['source_ref']):
                entries = [e for e in self.entries if e['ref'] != d['source_ref']]
                with self.assertRaisesRegex(ValueError, 'no longer cited'):
                    tables(self.document, entries)

    def test_evidence_does_not_certify_antiphon_words_cuts_or_rights(self):
        self.assertEqual(self.evidence['source_artifact_sha256'], 'e6b82741acc77fb5e0d7c887813f6f2652b4ec088abc8526f5c77320e9762aca')
        self.assertEqual([(d['artifact_page'], d['printed_page']) for d in self.decisions], [(117,109),(146,138),(150,142)])
        for d in self.decisions:
            self.assertEqual(d['part_cuts'], 'unverified')
            self.assertEqual(d['exact_antiphon_wording'], 'unverified')
            self.assertEqual(d['exact_2008_body'], 'unverified')
            self.assertFalse(d['rights_promotion'])
            self.assertEqual(len(d['carriers']), 7)


if __name__ == '__main__':
    unittest.main()
