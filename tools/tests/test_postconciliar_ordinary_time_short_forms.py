"""The bounded 1981 Ordo short readings remain explicit source alternatives."""

from __future__ import annotations

import sys
import tomllib
import unittest
from importlib.machinery import SourceFileLoader
from importlib.util import module_from_spec, spec_from_loader
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / 'src/sources/calendars/postconciliar/propers.yaml'
INVENTORY = ROOT / 'src/sources/inventories/postconciliar-seasonal-collation-v1.toml'
sys.path.insert(0, str(ROOT / 'scripts'))

APPOINTMENTS = [
    ('ot-3', 'Second Reading', 'C', '1 Corinthians 12:12-14, 27', 100, 69),
    ('ot-3', 'Gospel', 'A', 'Matthew 4:12-17', 100, 67),
    ('ot-4', 'Second Reading', 'C', '1 Corinthians 13:4-13', 102, 72),
    ('ot-5', 'Second Reading', 'C', '1 Corinthians 15:3-8, 11', 103, 75),
    ('ot-6', 'Gospel', 'A', 'Matthew 5:20-22a, 27-28, 33-34a, 37', 104, 76),
    ('ot-9', 'Gospel', 'B', 'Mark 2:23-28', 107, 86),
    ('ot-11', 'Gospel', 'C', 'Luke 7:36-50', 110, 93),
    ('ot-13', 'Gospel', 'B', 'Mark 5:21-24, 35b-43', 112, 98),
    ('ot-14', 'Gospel', 'C', 'Luke 10:1-9', 114, 102),
    ('ot-15', 'Second Reading', 'B', 'Ephesians 1:3-10', 115, 104),
    ('ot-15', 'Gospel', 'A', 'Matthew 13:1-9', 115, 103),
    ('ot-16', 'Gospel', 'A', 'Matthew 13:24-30', 116, 106),
    ('ot-17', 'Gospel', 'A', 'Matthew 13:44-46', 117, 109),
    ('ot-19', 'Second Reading', 'C', 'Hebrews 11:1-2, 8-12', 120, 117),
    ('ot-19', 'Gospel', 'C', 'Luke 12:35-40', 120, 117),
    ('ot-24', 'Gospel', 'C', 'Luke 15:1-10', 125, 132),
    ('ot-25', 'Gospel', 'C', 'Luke 16:10-13', 127, 135),
    ('ot-26', 'Second Reading', 'A', 'Philippians 2:1-5', 128, 136),
    ('ot-27', 'Gospel', 'B', 'Mark 10:2-12', 130, 140),
    ('ot-28', 'Gospel', 'A', 'Matthew 22:1-10', 131, 142),
    ('ot-28', 'Gospel', 'B', 'Mark 10:17-27', 131, 143),
    ('ot-29', 'Gospel', 'B', 'Mark 10:42-45', 133, 146),
    ('ot-32', 'Second Reading', 'A', '1 Thessalonians 4:13-14', 139, 154),
    ('ot-32', 'Gospel', 'B', 'Mark 12:41-44', 139, 155),
    ('ot-32', 'Gospel', 'C', 'Luke 20:27, 34-38', 140, 156),
    ('ot-33', 'Gospel', 'A', 'Matthew 25:14-15, 19-21', 141, 157),
]


def load_tool(name):
    loader = SourceFileLoader('_ot_short_' + name.replace('-', '_'), str(ROOT / 'tools' / name))
    module = module_from_spec(spec_from_loader(loader.name, loader))
    sys.modules[loader.name] = module
    loader.exec_module(module)
    return module


class OrdinaryTimeShortFormsTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.document = yaml.safe_load(SOURCE.read_text())
        cls.masses = {mass['key']: mass for section in cls.document['sections'].values()
                      for mass in section['masses']}
        cls.canon = load_tool('citations')
        cls.evidence = tomllib.loads(INVENTORY.read_text())['ordinary_time_short_forms_2026_10_20']

    def test_exact_short_references_and_parts_are_encoded_by_the_owner(self):
        for mass, slot, cycle, reference, _, _ in APPOINTMENTS:
            with self.subTest(mass=mass, slot=slot, cycle=cycle):
                short = next(row for row in self.masses[mass]['propers']
                             if row['name'] == slot + ' (shorter form)')
                self.assertEqual(short['cycles'][cycle]['verses'], [self.canon.parse_citation(reference)])

    def test_every_short_member_is_adjacent_to_its_preserved_primary(self):
        for mass, slot in {(row[0], row[1]) for row in APPOINTMENTS}:
            with self.subTest(mass=mass, slot=slot):
                propers = self.masses[mass]['propers']
                index = next(i for i, row in enumerate(propers) if row['name'] == slot)
                primary, short = propers[index:index + 2]
                self.assertEqual(short['name'], slot + ' (shorter form)')
                self.assertEqual(set(primary['cycles']), {'A', 'B', 'C'})
                self.assertEqual(primary['ordinary_disposition']['option'], 'longer')
                self.assertEqual(short['ordinary_disposition']['option'], 'shorter')
                for key in ('kind', 'group', 'basis'):
                    self.assertEqual(primary['ordinary_disposition'][key], short['ordinary_disposition'][key])

    def test_sparse_cycles_do_not_appoint_a_short_form_in_other_years(self):
        for mass, slot in {(row[0], row[1]) for row in APPOINTMENTS}:
            short = next(row for row in self.masses[mass]['propers']
                         if row['name'] == slot + ' (shorter form)')
            expected = {row[2] for row in APPOINTMENTS if row[:2] == (mass, slot)}
            self.assertEqual(set(short['cycles']), expected, (mass, slot))

    def test_new_options_hold_citations_and_no_liturgical_wording(self):
        for mass, slot in {(row[0], row[1]) for row in APPOINTMENTS}:
            short = next(row for row in self.masses[mass]['propers']
                         if row['name'] == slot + ' (shorter form)')
            self.assertEqual(short['source'], 'scripture')
            for owner in (short, *short['cycles'].values()):
                self.assertFalse({'text', 'latin', 'incipit', 'translations'} & set(owner), (mass, slot))

    def test_every_appointment_pins_the_inspected_page_and_cycle(self):
        rows = {(row['mass'], row['proper'], row['cycle']): row for row in self.evidence['rows']}
        self.assertEqual(set(rows), {(row[0], row[1], row[2]) for row in APPOINTMENTS})
        for mass, slot, cycle, reference, page, number in APPOINTMENTS:
            row = rows[(mass, slot, cycle)]
            self.assertEqual((row['short_reference'], row['artifact_page'], row['printed_page'], row['lectionary_number']),
                             (reference, page, page - 54, number))
            primary = next(proper for proper in self.masses[mass]['propers'] if proper['name'] == slot)
            self.assertEqual([verse['ref'] for verse in primary['cycles'][cycle]['verses']],
                             row['long_references'])
        self.assertEqual(self.evidence['recorded_on'], '2026-10-20')
        self.assertEqual(self.evidence['witness_sha256'], 'ed4bc14e6c5f885be9cb220f4edbdd23c1db749b53c1489058d6e54cfaf7fd0d')

    def test_ot21_lead_does_not_become_an_unsupported_1981_option(self):
        propers = self.masses['ot-21']['propers']
        primary = next(row for row in propers if row['name'] == 'Second Reading')
        self.assertNotIn('ordinary_disposition', primary)
        self.assertEqual(primary['cycles']['B']['verses'][0]['ref'], 'Ephesians 5:21-32')
        self.assertFalse(any(row['name'] == 'Second Reading (shorter form)' for row in propers))
        self.assertIn('Ephesians 5:2a, 25-32', primary['notes'])
        self.assertEqual(self.evidence['unconfirmed_leads'][0]['artifact_page'], 122)


if __name__ == '__main__':
    unittest.main()
