"""Recovered appointments must not retain present-tense absence claims."""
from pathlib import Path
import unittest
import yaml

ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / 'src/sources/calendars/postconciliar/propers.yaml'


class PostconciliarSourceNoteCurrentnessTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        document = yaml.safe_load(SOURCE.read_text())
        cls.masses = {m['key']: m for s in document['sections'].values() for m in s['masses']}

    def test_recovered_antiphon_roles_are_not_still_described_as_absent(self):
        cases = {
            'transfiguration-lord': (125, 'Nothing else of this Mass has been read'),
            'saint-augustine-bishop-doctor-church': (130, 'Antiphons and the other two orations are printed in the Missal, not in the Ordo, and remain absent'),
            'saints-andrew-kim-tae-gon-priest': (134, 'no slot is written for it'),
        }
        for key, (page, obsolete) in cases.items():
            with self.subTest(mass=key):
                mass = self.masses[key]
                antiphons = [p for p in mass['propers'] if p['name'] in ('Entrance Antiphon', 'Communion Antiphon')]
                self.assertEqual([p['name'] for p in antiphons], ['Entrance Antiphon', 'Communion Antiphon'])
                self.assertTrue(any(f'artifact page {page}' in p.get('notes', '') for p in antiphons))
                self.assertNotIn(obsolete, mass['notes'])
                self.assertIn('now', mass['notes'])
                self.assertIn('English', mass['notes'])
                self.assertIn('restricted', mass['notes'])
                self.assertIn('unestablished', mass['notes'])

    def test_dated_antecedent_inspection_is_preserved_with_exact_edition_limits(self):
        for key in ('most-holy-name-jesus', 'most-holy-name-mary', 'saint-anthony-abbot'):
            with self.subTest(mass=key):
                note = self.masses[key]['notes']
                self.assertIn('ANTECEDENT, NOT THE CONTROLLING EDITION', note)
                self.assertIn('2026-08-20', note)
                self.assertIn('1862', note)
                self.assertIn('secondary digital reproduction identified as 2002 is now held', note)
                self.assertIn('no complete authenticated 2008 Missal artifact is held', note)
                self.assertIn('That antecedent Latin has not been collated against the target 2008 edition', note)
                self.assertNotIn('Nothing here has been collated', note)
                self.assertNotIn('2002/2008, which this file declares as its edition, which is in copyright and is not held here', note)

    def test_uncited_korean_entrance_is_not_claimed_to_have_no_slot_or_no_scriptural_content(self):
        mass = self.masses['saints-andrew-kim-tae-gon-priest']
        entrance = next(p for p in mass['propers'] if p['name'] == 'Entrance Antiphon')
        self.assertEqual(entrance['source'], 'composed')
        self.assertNotIn('verses', entrance)
        self.assertNotIn('text', entrance)
        self.assertEqual(entrance['text_status']['reasons'][0]['kind'], 'witness-gap')
        self.assertIn('2026-08-21 inspection initially carried only the Communion citation', mass['notes'])
        self.assertIn('absence of a citation does not classify its complete body as non-scriptural', mass['notes'])
        self.assertNotIn('THE ENTRANCE ANTIPHON IS PROPER AND NON-SCRIPTURAL', mass['notes'])

    def test_dated_common_directions_acknowledge_catalogue_without_resolving_a_form(self):
        for key in ('saint-catherine-siena-virgin-doctor-church', 'saint-justin-martyr',
                    'saints-charles-lwanga-companions-martyrs', 'saints-perpetua-felicity-martyrs'):
            with self.subTest(mass=key):
                mass = self.masses[key]
                self.assertIn('identity-only Common records that do not resolve a target-edition formulary', mass['notes'])
                self.assertNotIn('this repository carries no Common', mass['notes'])
                self.assertNotIn('takes_from', mass)


if __name__ == '__main__':
    unittest.main()
