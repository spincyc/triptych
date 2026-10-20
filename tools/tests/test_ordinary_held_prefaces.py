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

    def translation(self, key, lang):
        return next(row for row in self.elements['praefatio/' + key]['translations'] if row['lang'] == lang)

    def test_trinity_keeps_the_partial_source_row_and_no_new_occurrence(self):
        for lang in ('en', 'la'):
            row = self.translation('praefatio-de-ss-trinitate', lang)
            self.assertEqual(row['text'], self.sources[lang]['praefatio-de-ss-trinitate'])
            self.assertNotIn('target_wording', row)
            self.assertEqual(row['collation'], 'collated' if lang == 'la' else 'uncollated')
        self.assertNotIn('praefatio/praefatio-de-ss-trinitate-initium', self.elements)
        self.assertNotIn('junction', self.elements['praefatio/praefatio-de-ss-trinitate'])
        self.assertTrue(self.translation('praefatio-de-ss-trinitate', 'la')['text'].endswith(' Sanctus, &c.'))
        self.assertTrue(self.translation('praefatio-de-ss-trinitate', 'en')['text'].endswith(' Holy, &c.'))

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


if __name__ == '__main__':
    unittest.main()
