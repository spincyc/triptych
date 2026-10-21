"""Preserve OLM1981 n58's principal and optional Day Second Readings."""
from pathlib import Path
from importlib.machinery import SourceFileLoader
from importlib.util import module_from_spec, spec_from_loader
import sys
import tomllib
import unittest
import yaml

ROOT = Path(__file__).resolve().parents[2]
PROPERS = ROOT / 'src/sources/calendars/postconciliar/propers.yaml'
INVENTORY = ROOT / 'src/sources/inventories/postconciliar-seasonal-collation-v1.toml'


class AscensionOptionsTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.document = yaml.safe_load(PROPERS.read_text())
        cls.mass = next(mass for section in cls.document['sections'].values()
                        for mass in section['masses'] if mass['key'] == 'ascension')
        cls.form = next(form for form in cls.mass['forms'] if form['id'] == 'day')
        cls.rows = [row for row in cls.form['propers']
                    if row.get('ordinary_disposition', {}).get('group') == 'second-reading']
        loader = SourceFileLoader('_ascension_citations', str(ROOT / 'tools/citations'))
        cls.citations = module_from_spec(spec_from_loader(loader.name, loader))
        sys.modules[loader.name] = cls.citations
        loader.exec_module(cls.citations)

    def test_principal_is_cycle_independent_and_optional_cycles_are_exact(self):
        self.assertEqual([row['ordinary_disposition']['option'] for row in self.rows],
                         ['common', 'longer', 'shorter', 'year-c'])
        common, longer, shorter, year_c = self.rows
        self.assertNotIn('cycles', common)
        self.assertNotIn('weekday_cycles', common)
        self.assertEqual(set(longer['cycles']), {'B'})
        self.assertEqual(set(shorter['cycles']), {'B'})
        self.assertEqual(set(year_c['cycles']), {'C'})
        self.assertEqual({row['ordinary_disposition']['kind'] for row in self.rows}, {'alternative'})
        self.assertEqual(len({row['ordinary_disposition']['basis'] for row in self.rows}), 1)

    def test_literal_source_references_and_queued_option_ids_survive(self):
        expected = [('common', None, 'Ephesians 1:17-23'),
                    ('longer', 'B', 'Ephesians 4:1-13'),
                    ('shorter', 'B', 'Ephesians 4:1-7, 11-13'),
                    ('year-c', 'C', 'Hebrews 9:24-28; 10:19-23')]
        for row, (option, cycle, reference) in zip(self.rows, expected):
            with self.subTest(option=option):
                self.assertEqual(row['ordinary_disposition']['option'], option)
                owner = row if cycle is None else row['cycles'][cycle]
                self.assertEqual(owner['verses'], [self.citations.parse_citation(reference)])
        names = [row['name'] for row in self.form['propers']]
        index = names.index('Second Reading')
        self.assertEqual(names[index + 1], 'Second Reading (shorter form)')

    def test_source_recovery_supplies_no_lectionary_wording_or_publication_grant(self):
        for row in self.rows:
            self.assertEqual(row['source'], 'scripture')
            for owner in (row, *row.get('cycles', {}).values()):
                self.assertFalse({'text', 'latin', 'translations', 'incipit'} & set(owner))
        self.assertEqual([form['id'] for form in self.mass['forms']], ['vigil', 'day'])

    def test_vigil_does_not_gain_an_unproved_second_reading_choice(self):
        vigil = next(form for form in self.mass['forms'] if form['id'] == 'vigil')
        second = [row for row in vigil['propers']
                  if row['name'] == 'Second Reading' or row['name'].startswith('Second Reading (')]
        self.assertEqual(len(second), 1)
        self.assertEqual(second[0]['name'], 'Second Reading')
        self.assertNotIn('ordinary_disposition', second[0])
        self.assertFalse(any(row.get('ordinary_disposition', {}).get('group') == 'second-reading'
                             for row in vigil['propers']))

    def test_dated_evidence_qualifies_target_and_vigil_correspondence(self):
        evidence = tomllib.loads(INVENTORY.read_text())['ascension_day_principal_optional_recovery_2026_10_20']
        self.assertEqual((evidence['mass'], evidence['form_id'], evidence['proper']),
                         ('ascension', 'day', 'Second Reading'))
        self.assertEqual((evidence['artifact_page'], evidence['printed_page'], evidence['marginal_number']), (93, 39, 58))
        self.assertEqual(evidence['witness_sha256'], 'ed4bc14e6c5f885be9cb220f4edbdd23c1db749b53c1489058d6e54cfaf7fd0d')
        self.assertIn('does not establish', evidence['boundary'])
        self.assertIn('Vigil', evidence['boundary'])
        self.assertIn('2008', evidence['boundary'])


if __name__ == '__main__':
    unittest.main()
