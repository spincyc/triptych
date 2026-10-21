"""Two source-ordered Entrance alternatives occupy one seat, without body promotion."""
from pathlib import Path
from importlib.machinery import SourceFileLoader
from importlib.util import module_from_spec, spec_from_loader
import copy
import json
import sys
import unittest
import yaml

ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / 'src/sources/calendars/postconciliar/propers.yaml'
CALENDARS = ROOT / 'src/sources/calendars'
TARGET = 'edition.catholic-church.missale-romanum.vatican-typica-tertia-reimpressio-emendata-2008'
ARTIFACT = 'artifact.catholic-church.missale-romanum.2010-english-icel-antiphonary.antiphonary-pdf'
CASES = {
    ('assumption-blessed-virgin-mary', 'day'): (127, 119, 'Revelation 12:1', None, 'Luke 1:48-49'),
    ('saint-john-apostle-evangelist', 'main'): (151, 143, None, 'Sirach 15:5', 'John 1:14, 16'),
}


def tool(name):
    loader = SourceFileLoader('_alternate_entrance_' + name.replace('-', '_'), str(ROOT / 'tools' / name))
    module = module_from_spec(spec_from_loader(loader.name, loader))
    sys.modules[loader.name] = module
    loader.exec_module(module)
    return module


class AlternateEntranceFormsTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.document = yaml.safe_load(SOURCE.read_text())
        cls.masses = {m['key']: m for s in cls.document['sections'].values() for m in s['masses']}
        cls.propers = tool('mass-propers')
        cls.check = tool('check-calendar-masses')
        cls.canon = tool('citations')
        cls.ordinary = tool('mass-ordinary')
        cls.frame = json.loads((ROOT / 'src/web/data/structure/ordinary/postconciliar.json').read_text())
        cls.overlay, cls.absences, cls.stale, cls.witnesses = cls.propers.translation_overlay('postconciliar', CALENDARS)

    def holder(self, key, form):
        mass = self.masses[key]
        return mass if form == 'main' else next(f for f in mass['forms'] if f['id'] == form)

    def test_all_six_appointments_preserve_literal_source_order_and_role_coordinates(self):
        for (key, form), (ap, pp, first, second, communion) in CASES.items():
            with self.subTest(mass=key, form=form):
                holder = self.holder(key, form)
                rows = holder['propers']
                self.assertEqual([r['name'] for r in rows[:2]], ['Entrance Antiphon'] * 2)
                self.assertEqual(rows[-1]['name'], 'Communion Antiphon')
                for row, reference in zip([*rows[:2], rows[-1]], (first, second, communion)):
                    self.assertIn(f'artifact page {ap} / printed page {pp}', row['notes'])
                    self.assertNotIn('text', row)
                    self.assertNotIn('incipit', row)
                    if reference:
                        self.assertEqual(row['source'], 'scripture')
                        self.assertEqual(row['verses'], [self.canon.parse_citation(reference)])
                    else:
                        self.assertEqual(row['source'], 'composed')
                        self.assertNotIn('verses', row)
                        self.assertEqual(row['text_status'], {'state': 'unavailable', 'scope': 'proper-body', 'reasons': [{'kind': 'witness-gap', 'source_id': TARGET}]})
                self.assertEqual([r['ordinary_disposition']['option'] for r in rows[:2]], ['source-first', 'source-second'])
                self.assertEqual(rows[0]['ordinary_disposition']['basis'], rows[1]['ordinary_disposition']['basis'])
                for row in rows[:2]:
                    self.assertEqual(row['ordinary_disposition']['group'], 'entrance-antiphon')
                    self.assertEqual(row['ordinary_disposition']['kind'], 'alternative')
                    self.assertNotIn('cycles', row)
                    self.assertNotIn('default', row['ordinary_disposition'])
                form_label = '' if form == 'main' else holder['name']
                for occurrence, row in enumerate(rows[:2], 1):
                    self.assertEqual(self.propers.source_slot_identity(self.document, self.masses[key], form_label, row, None),
                                     (key, form, 'Entrance Antiphon', occurrence))

    def test_existing_source_and_seating_owners_admit_options_and_refuse_singletons_or_cross_seat_groups(self):
        for key, form in CASES:
            mass = self.masses[key]
            problems = []
            self.check.check_entry(mass, 0, problems, section_kind=mass['kind'], calendar='postconciliar')
            self.assertEqual(problems, [])
            rows = self.holder(key, form)['propers']
            self.ordinary.check_form_seating(self.frame, rows, key + '/' + form, full=True)
            singleton = copy.deepcopy(rows)
            del singleton[1]
            with self.assertRaisesRegex(self.ordinary.SourceError, 'two distinct options|two options'):
                self.ordinary.check_form_seating(self.frame, singleton, 'singleton', full=True)
            cross = copy.deepcopy(rows)
            cross[1]['name'] = 'Communion Antiphon'
            with self.assertRaisesRegex(self.ordinary.SourceError, 'spans Ordinary slots'):
                self.ordinary.check_form_seating(self.frame, cross, 'cross-seat', full=True)

    def test_two_uncited_english_bodies_join_exact_held_restricted_absences(self):
        for (key, form), (ap, pp, first, second, _) in CASES.items():
            occurrence = 1 if first is None else 2
            proper = self.holder(key, form)['propers'][occurrence - 1]
            records = self.propers.matching_untranslated_records(
                proper, self.absences.get((key, form, 'Entrance Antiphon'), []), occurrence, cycle='all', extent='body')
            self.assertEqual(len(records), 1)
            row = records[0]
            self.assertEqual(row['reason']['kind'], 'rights-withheld')
            self.assertEqual(row['reason']['source_id'], ARTIFACT)
            self.assertEqual(row['witness_artifact_id'], ARTIFACT)
            self.assertEqual((row['verified_artifact_page'], row['verified_printed_page']), (ap, pp))
            for field in ('text', 'translations', 'quarantined_text_sha256'):
                self.assertNotIn(field, row)
            self.assertEqual(self.check.untranslated_witness_problems('alternate Entrance', row), [])
            public = {**proper, 'untranslated': self.propers.public_untranslated_records(records),
                      'unavailable_translations': self.propers.unavailable_states_from_records(records)}
            states = {x['lang']: x for x in self.propers.proper_language_capabilities(public)}
            self.assertEqual(states['la']['status'], 'unavailable')
            self.assertEqual(states['en']['status'], 'rights-withheld')
            for state in states.values():
                self.assertFalse(state['held'])
                self.assertFalse(state['available'])
            self.assertEqual(proper['text_status']['reasons'][0]['source_id'], TARGET)
            self.assertNotIn('verses', proper)

    def test_cited_john_component_does_not_claim_a_complete_adapted_english_body(self):
        alternative = self.holder('saint-john-apostle-evangelist', 'main')['propers'][1]
        self.assertEqual(alternative['verses'][0]['ref'], 'Sirach 15:5')
        self.assertEqual(alternative['source'], 'scripture')
        self.assertIn('not proof of the full adapted English antiphon body', alternative['notes'])
        self.assertIn('separate Sirach English body-scope companion', alternative['notes'])
        self.assertFalse(alternative.get('text'))
        self.assertFalse(alternative.get('translations'))


if __name__ == '__main__':
    unittest.main()
