"""Conserve seven Common referrals, historical gaps and four admitted English uses."""
from pathlib import Path
from importlib.machinery import SourceFileLoader
from importlib.util import module_from_spec, spec_from_loader
import sys
import hashlib
import json
import tomllib
import unittest

ROOT = Path(__file__).resolve().parents[2]
CALENDARS = ROOT / 'src/sources/calendars'
LEDGER = ROOT / 'src/sources/inventories/postconciliar-proper-translations-v1.toml'
CASES = {
    'saint-polycarp-bishop-martyr': (536, 333, '717,6', 383),
    'saint-martin-i-pope-martyr': (551, 338, '717,6', 383),
    'saint-lawrence-brindisi-priest-doctor-church': (602, 351, '729,8', 390),
    'saints-pontian-pope-hippolytus-priest-martyrs': (620, 355, '717,6', 383),
    'saint-john-chrysostom-bishop-doctor-church': (637, 359, '729,8', 390),
    'saint-cecilia-virgin-martyr': (681, 370, '735,2', 391),
    'saint-lucy-virgin-martyr': (692, 372, '735,2', 391),
}
TARGET = 'edition.catholic-church.missale-romanum.vatican-typica-tertia-reimpressio-emendata-2008'

# All four admissions and complete positive dictionaries already exist at 702f650.
ADMITTED = {'saint-lawrence-brindisi-priest-doctor-church': {'entry_sha256': 'fe483d38fcaefbf7cf5ac5b8070e84418d22e4944377da2517a2a56eab4d2ff6',
                                                  'English_sha256': '7e025357311fc727eb8f27402ef09586cf13ac70b932b0aa1fcf4e7365544798',
                                                  'rights': 'public-domain',
                                                  'admission': 'phase1-admission.json'},
 'saint-john-chrysostom-bishop-doctor-church': {'entry_sha256': '617393fdedee2a0b0352cae324f38ec4f70081badddfa642b0f3dd9691c3a089',
                                                'English_sha256': '7e025357311fc727eb8f27402ef09586cf13ac70b932b0aa1fcf4e7365544798',
                                                'rights': 'public-domain',
                                                'admission': 'phase1-admission.json'},
 'saint-cecilia-virgin-martyr': {'entry_sha256': 'b2351e9a4f75f7d02802cd2fc208a1855c6f549111f87b877f1ea136f9d564f0',
                                 'English_sha256': '180c9c8a2fd059c019dc7a7747ed21220fb11d7d4771b8c7707b7cb030c0a722',
                                 'rights': 'project-created',
                                 'admission': 'phase2-virgo-admission.json'},
 'saint-lucy-virgin-martyr': {'entry_sha256': '4e9df70063a9933f7123f8ae50fe86311d8f0b98ff57102035902c7bee5ab64e',
                              'English_sha256': '180c9c8a2fd059c019dc7a7747ed21220fb11d7d4771b8c7707b7cb030c0a722',
                              'rights': 'project-created',
                              'admission': 'phase2-virgo-admission.json'}}
ADMISSION_HASHES = {'phase1-admission.json': '336c2eeb280f40fcf291e99a691c21bc0a1025b8b20751815ff8facaa10cc255',
 'phase2-virgo-admission.json': '32c337acd6aa77053b342e9da372cb7fd687a945647a9535bd7f8358e8cd4967'}

class CommonAcclamationEnglishTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        loader = SourceFileLoader('_common_acclamation_english_owner', str(ROOT / 'tools/mass-propers'))
        cls.owner = module_from_spec(spec_from_loader(loader.name, loader))
        sys.modules[loader.name] = cls.owner
        loader.exec_module(cls.owner)
        cls.document = cls.owner.load_calendar(CALENDARS, 'postconciliar')
        cls.masses = {m['key']: m for _, m in cls.owner.masses_of(cls.document)}
        cls.overlay, cls.absences, cls.stale, cls.witnesses = cls.owner.translation_overlay('postconciliar', CALENDARS)
        cls.positive_rows = {r['mass']: r for r in tomllib.loads(LEDGER.read_text())['entries']
                             if r['mass'] in ADMITTED and r['proper'] == 'Gospel Acclamation'}
        cls.archived_absences = {}
        for name, expected in ADMISSION_HASHES.items():
            raw = (ROOT / 'workflows/reviews/missal-english-completion-2026-10-29/postconciliar' / name).read_bytes()
            if hashlib.sha256(raw).hexdigest() != expected:
                raise AssertionError('exact previously accepted Common admission: ' + name)
            for row in json.loads(raw)['superseded_unavailable_dictionaries']:
                if row['mass'] in ADMITTED:
                    if row['mass'] in cls.archived_absences or ADMITTED[row['mass']]['admission'] != name:
                        raise AssertionError('unique historical Common absence source')
                    cls.archived_absences[row['mass']] = row
        if set(cls.archived_absences) != set(ADMITTED):
            raise AssertionError('all four historical Common absence dictionaries')

    def seats(self):
        for key in CASES:
            mass = self.masses[key]
            rows = [(form, proper, taken) for form, proper, taken
                    in self.owner.appointed_propers(self.document, mass)
                    if proper['name'] == 'Gospel Acclamation']
            self.assertEqual(len(rows), 1, key)
            form, proper, taken = rows[0]
            identity = self.owner.source_slot_identity(self.document, mass, form, proper, taken)
            self.assertEqual(identity, (key, 'main', 'Gospel Acclamation', 1))
            records = self.owner.matching_untranslated_records(
                proper, self.absences.get(identity[:3], []), identity[3], cycle='all', extent='body')
            yield key, proper, identity, records

    def test_seven_source_identified_historical_absences_remain_accounted(self):
        for key, proper, identity, records in self.seats():
            with self.subTest(mass=key):
                self.assertEqual(len(records), 0 if key in ADMITTED else 1)
                row = self.archived_absences[key] if key in ADMITTED else records[0]
                self.assertEqual({k: row[k] for k in ('form_id', 'cycle', 'occurrence', 'lang', 'extent', 'availability', 'reason')},
                                 {'form_id': 'main', 'cycle': 'all', 'occurrence': 1, 'lang': 'en', 'extent': 'body', 'availability': 'unavailable', 'reason': {'kind': 'no-exemplar'}})
                entry, page, common, common_page = CASES[key]
                for cue in (f'n. {entry}', f'page {page}', f'n. {common}', f'page {common_page}'):
                    self.assertIn(cue, row['note'])
                for field in ('text', 'translation', 'translations', 'source_id', 'witness_artifact_id', 'quarantined_text_sha256', 'verses'):
                    self.assertNotIn(field, row)
                entry = self.owner.translation_entry_for(self.overlay, identity[:3], (*identity[:3], 'all', 1))
                if key in ADMITTED:
                    self.assertIsNotNone(entry)
                else:
                    self.assertIsNone(entry)

    def test_joined_report_keeps_latin_gaps_independent_of_english_admissions(self):
        for key, proper, identity, records in self.seats():
            with self.subTest(mass=key):
                self.assertEqual(proper['source'], 'composed')
                self.assertEqual(proper['text_status'], {'state': 'unavailable', 'scope': 'proper-body', 'reasons': [{'kind': 'witness-gap', 'source_id': TARGET}]})
                carried = self.owner.carry_translations('postconciliar', identity[:3], proper, self.overlay, [], identity, self.witnesses)
                public = {**carried, 'untranslated': self.owner.public_untranslated_records(records)}
                states = {r['lang']: r for r in self.owner.proper_language_capabilities(public)}
                self.assertEqual(states['la']['status'], 'unavailable')
                self.assertFalse(states['la']['held'])
                self.assertFalse(states['la']['available'])
                self.assertEqual(public['text_status'], proper['text_status'])
                for field in ('text', 'verses', 'incipit'):
                    self.assertFalse(public.get(field))
                if key in ADMITTED:
                    self.assertEqual(states['en']['status'], 'full-text')
                    self.assertTrue(states['en']['held'])
                    self.assertTrue(states['en']['available'])
                    self.assertFalse(public['untranslated'])
                    english = [r for r in public['translations'] if r['lang'] == 'en']
                    self.assertEqual(len(english), 1)
                    self.assertEqual(english[0]['text'], self.positive_rows[key]['translations'][0]['text'])
                    self.assertEqual(english[0]['rights'], ADMITTED[key]['rights'])
                else:
                    self.assertEqual(states['en']['status'], 'unavailable')
                    self.assertFalse(states['en']['held'])
                    self.assertFalse(states['en']['available'])
                    self.assertFalse(public.get('translations'))
                    self.assertEqual(public['untranslated'][0]['target'], {'mass': key, 'form_id': 'main', 'proper': 'Gospel Acclamation', 'cycle': 'all', 'occurrence': 1, 'extent': 'body'})

    def test_four_prior_admissions_keep_exact_historical_and_study_routes(self):
        self.assertEqual(set(self.positive_rows), set(ADMITTED))
        self.assertEqual(set(ADMITTED), set(self.archived_absences))
        for key, spec in ADMITTED.items():
            with self.subTest(mass=key):
                row = self.positive_rows[key]
                raw = json.dumps(row, sort_keys=True, ensure_ascii=False, separators=(',', ':')).encode()
                self.assertEqual(hashlib.sha256(raw).hexdigest(), spec['entry_sha256'])
                self.assertEqual(len(row['translations']), 1)
                translation = row['translations'][0]
                self.assertEqual((translation['lang'], translation['rights']), ('en', spec['rights']))
                self.assertEqual(hashlib.sha256(translation['text'].encode()).hexdigest(), spec['English_sha256'])
                if spec['rights'] == 'public-domain':
                    self.assertEqual(row['relation'], 'antecedent-printing')
                    self.assertEqual(translation['source_id'], 'edition.catholic-church.breviarium-romanum.blackwood-bute-winter-1908')
                    self.assertTrue(row['publication_artifact_id'])
                    self.assertTrue(row['publication_passage_id'])
                else:
                    self.assertEqual(spec['rights'], 'project-created')
                    self.assertEqual(row['relation'], 'abridged')
                    self.assertNotIn('source_id', translation)
                    self.assertEqual(row['witness_edition_id'], 'edition.catholic-church.breviarium-romanum.pustet-ratisbon-pars-hiemalis-1888')
                    self.assertEqual(row['ancient_passage_id'], 'passage.catholic-church.breviarium-romanum.pustet-ratisbon-pars-hiemalis-1888.english-completion-20261029-postconciliar-virgo-initial-respond')

    def test_coverage_accounts_for_absences_without_silent_or_stale_seats(self):
        coverage = self.owner.english_coverage(CALENDARS, 'postconciliar')
        for field in ('unaccounted', 'outside_the_ledger', 'unmatched_records', 'stale_translation_records'):
            self.assertEqual(coverage[field], 0, (field, coverage))


if __name__ == '__main__':
    unittest.main()
