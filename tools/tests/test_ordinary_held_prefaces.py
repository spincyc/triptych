#!/usr/bin/env python3
"""Held-source collation must not turn a partial witness into a full Preface."""
import csv
import json
from pathlib import Path
import tomllib
import unittest

ROOT = Path(__file__).resolve().parents[2]


class HeldPrefaceExtents(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.file = json.loads((ROOT / 'src/web/data/structure/ordinary/roman-1962.json').read_text())
        cls.elements = {e['key']: e for s in cls.file['sections'] for e in s['elements']}
        cls.inventory = tomllib.loads((ROOT / 'src/sources/inventories/roman-1962-ordo-missae-v1.toml').read_text())
        cls.sources = {}
        for lang in ('en', 'la'):
            artifact = ROOT / ('src/sources/works/eugene-cummiskey/roman-missal-english-laity/'
                               f'editions/philadelphia-1861/artifacts/praefationes-{lang}/praefationes-{lang}.tsv')
            with artifact.open(newline='') as stream:
                cls.sources[lang] = {row['element_key']: row['english' if lang == 'en' else 'latin']
                                     for row in csv.DictReader(stream, delimiter='\t')}
        cls.complete_english = {}
        for group in ('a', 'b'):
            artifact = ROOT / ('src/sources/works/francis-xavier-lasance/the-new-roman-missal/'
                'editions/benziger-revised-1945/artifacts/'
                f'english-completion-20261029-ordinary-prefaces-complete-{group}-en/text.tsv')
            with artifact.open(newline='') as stream:
                for row in csv.DictReader(stream, delimiter='\t'):
                    cls.complete_english[row['element_key']] = row['english']

    def translation(self, key, lang):
        return next(row for row in self.elements['praefatio/' + key]['translations'] if row['lang'] == lang)

    def test_trinity_keeps_partial_latin_and_complete_historical_english(self):
        row = self.translation('praefatio-de-ss-trinitate', 'la')
        self.assertEqual(row['text'], self.sources['la']['praefatio-de-ss-trinitate'])
        self.assertNotIn('target_wording', row)
        self.assertEqual(row['collation'], 'collated')
        english_artifact = ROOT / ('src/sources/works/francis-xavier-lasance/the-new-roman-missal/'
            'editions/benziger-revised-1945/artifacts/'
            'english-completion-20261029-ordinary-prefaces-complete-a-en/text.tsv')
        with english_artifact.open(newline='') as stream:
            english_source = next(row['english'] for row in csv.DictReader(stream, delimiter='\t')
                                  if row['element_key'] == 'praefatio-de-ss-trinitate')
        english = self.translation('praefatio-de-ss-trinitate', 'en')
        self.assertEqual(english['text'], english_source)
        self.assertEqual((english['relation'], english['collation']), ('antecedent', 'uncollated'))
        self.assertNotIn('target_wording', english)
        self.assertNotIn('praefatio/praefatio-de-ss-trinitate-initium', self.elements)
        self.assertNotIn('junction', self.elements['praefatio/praefatio-de-ss-trinitate'])
        self.assertTrue(self.translation('praefatio-de-ss-trinitate', 'la')['text'].endswith(' Sanctus, &c.'))
        self.assertTrue(english['text'].endswith(':'))
        self.assertNotIn('&c.', english['text'])
        self.assertTrue(english['text'].startswith('IT IS'))

    def test_eight_partial_prefaces_keep_their_cues_variants_and_no_exact_grade(self):
        keys = ['praefatio-de-nativitate', 'praefatio-de-epiphania', 'praefatio-de-quadragesima',
                'praefatio-de-sancta-cruce', 'praefatio-paschalis', 'praefatio-de-ascensione',
                'praefatio-de-beata-maria-virgine', 'praefatio-de-apostolis']
        for key in keys:
            with self.subTest(key=key):
                row = self.translation(key, 'la')
                self.assertEqual(row['text'], self.sources['la'][key])
                self.assertEqual((row['relation'], row['collation']), ('antecedent', 'collated'))
                self.assertNotIn('target_wording', row)
                self.assertIn('&c.', row['text'])
        self.assertIn('infusit', self.translation('praefatio-de-nativitate', 'la')['text'])
        self.assertIn('humam', self.translation('praefatio-de-sancta-cruce', 'la')['text'])
        self.assertIn('[ in hoc potissimum nocte vel die, vel ] in hoc', self.translation('praefatio-paschalis', 'la')['text'])
        self.assertIn('colaudare', self.translation('praefatio-de-beata-maria-virgine', 'la')['text'])

    def test_nine_complete_historical_english_bodies_keep_their_source_extent_in_both_frames(self):
        self.assertEqual(len(self.complete_english), 9)
        for calendar in ('roman-1962', 'roman-pre-1955'):
            document = json.loads((ROOT / f'src/web/data/structure/ordinary/{calendar}.json').read_text())
            elements = {element['key']: element for section in document['sections']
                        for element in section['elements']}
            for key, source in self.complete_english.items():
                with self.subTest(calendar=calendar, key=key):
                    element = elements['praefatio/' + key]
                    english = next(row for row in element['translations'] if row['lang'] == 'en')
                    self.assertEqual(english['text'], source)
                    self.assertEqual(english['source_id'],
                        'edition.francis-xavier-lasance.the-new-roman-missal.benziger-revised-1945')
                    self.assertEqual((english['relation'], english['collation']),
                                     ('antecedent', 'uncollated'))
                    self.assertNotIn('target_wording', english)
                    self.assertTrue(source.startswith('IT IS'))
                    self.assertTrue(source.endswith(':'))
                    self.assertNotIn('&c.', source)
                    self.assertNotIn('junction', element)
                    self.assertIn('Historical', english['reading_note'])
            easter = next(row for row in elements['praefatio/praefatio-paschalis']['translations']
                          if row['lang'] == 'en')
            self.assertIn('day (in these days)', easter['text'])
            self.assertIn('night', easter['reading_note'])
            mary = next(row for row in elements['praefatio/praefatio-de-beata-maria-virgine']['translations']
                        if row['lang'] == 'en')
            self.assertIn('. . .', mary['text'])
            self.assertIn('blank', mary['reading_note'])

    def test_source_only_cases_stay_outside_new_target_wording_claims(self):
        uncollated = [element['key'] for element in self.elements.values()
                      for row in element['translations'] or []
                      if row['lang'] == 'la' and row.get('collation') == 'uncollated']
        self.assertEqual(uncollated, ['praeparatio/gloria-in-excelsis-heading',
                                     'conclusio/dominus-vobiscum-ante-postcommunionem'])
        greeting = self.elements[uncollated[-1]]
        for row in greeting['translations']:
            self.assertNotIn('target_wording', row)
            self.assertTrue(all(turn['dialogue_role'] is None for turn in row['turns']))

    def test_chrism_study_english_and_old_witness_latin_remain_distinct(self):
        stem = ROOT / 'src/sources/works/triptych/english-completion-20261029-ordinary-chrism/editions'
        payloads = {
            'la': stem / '2026-10-30-latin-projection/artifacts/ordinary-chrism-latin-babd71a3/text.tsv',
            'en': stem / '2026-10-30-study-english/artifacts/ordinary-chrism-study-en-3a4dbe81/text.tsv',
        }
        for lang, payload in payloads.items():
            with payload.open(newline='') as stream:
                source = next(csv.DictReader(stream, delimiter='\t'))
            row = self.translation('praefatio-missa-chrismatis', lang)
            self.assertEqual(row['text'], source['latin' if lang == 'la' else 'english'])
        latin = self.translation('praefatio-missa-chrismatis', 'la')
        self.assertEqual((latin['relation'], latin['collation'], latin['target_wording']),
                         ('antecedent', 'collated', 'word-exact'))
        english = self.translation('praefatio-missa-chrismatis', 'en')
        self.assertEqual(english['relation'], 'own')
        self.assertNotIn('target_wording', english)
        self.assertIn('Triptych study translation', english['reading_note'])
        self.assertIn('not for recitation', english['reading_note'])


if __name__ == '__main__':
    unittest.main()
