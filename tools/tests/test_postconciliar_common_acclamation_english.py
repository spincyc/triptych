"""Account for seven unavailable Common-referral roles without inventing English."""
from pathlib import Path
from importlib.machinery import SourceFileLoader
from importlib.util import module_from_spec, spec_from_loader
import sys
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

    def test_exact_joined_seats_have_one_source_identified_english_absence(self):
        for key, proper, identity, records in self.seats():
            with self.subTest(mass=key):
                self.assertEqual(len(records), 1)
                row = records[0]
                self.assertEqual({k: row[k] for k in ('form_id', 'cycle', 'occurrence', 'lang', 'extent', 'availability', 'reason')},
                                 {'form_id': 'main', 'cycle': 'all', 'occurrence': 1, 'lang': 'en', 'extent': 'body', 'availability': 'unavailable', 'reason': {'kind': 'no-exemplar'}})
                entry, page, common, common_page = CASES[key]
                for cue in (f'n. {entry}', f'page {page}', f'n. {common}', f'page {common_page}'):
                    self.assertIn(cue, row['note'])
                for field in ('text', 'translation', 'translations', 'source_id', 'witness_artifact_id', 'quarantined_text_sha256', 'verses'):
                    self.assertNotIn(field, row)
                self.assertIsNone(self.owner.translation_entry_for(self.overlay, identity[:3], (*identity[:3], 'all', 1)))

    def test_joined_report_keeps_both_languages_unavailable_and_latin_state_independent(self):
        for key, proper, identity, records in self.seats():
            with self.subTest(mass=key):
                self.assertEqual(proper['source'], 'composed')
                self.assertEqual(proper['text_status'], {'state': 'unavailable', 'scope': 'proper-body', 'reasons': [{'kind': 'witness-gap', 'source_id': TARGET}]})
                carried = self.owner.carry_translations('postconciliar', identity[:3], proper, self.overlay, [], identity, self.witnesses)
                public = {**carried, 'untranslated': self.owner.public_untranslated_records(records)}
                states = {r['lang']: r for r in self.owner.proper_language_capabilities(public)}
                for lang in ('la', 'en'):
                    self.assertEqual(states[lang]['status'], 'unavailable')
                    self.assertFalse(states[lang]['held'])
                    self.assertFalse(states[lang]['available'])
                self.assertEqual(public['text_status'], proper['text_status'])
                self.assertEqual(public['untranslated'][0]['target'], {'mass': key, 'form_id': 'main', 'proper': 'Gospel Acclamation', 'cycle': 'all', 'occurrence': 1, 'extent': 'body'})
                for field in ('text', 'translations', 'verses', 'incipit'):
                    self.assertFalse(public.get(field))

    def test_coverage_accounts_for_absences_without_silent_or_stale_seats(self):
        coverage = self.owner.english_coverage(CALENDARS, 'postconciliar')
        for field in ('unaccounted', 'outside_the_ledger', 'unmatched_records', 'stale_translation_records'):
            self.assertEqual(coverage[field], 0, (field, coverage))


if __name__ == '__main__':
    unittest.main()
