"""New Communion appointments precede the existing Prayer after Communion."""
from pathlib import Path
from importlib.machinery import SourceFileLoader
from importlib.util import module_from_spec, spec_from_loader
from unittest.mock import patch
import copy
import sys
import unittest
import yaml

ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / 'src/sources/calendars/postconciliar/propers.yaml'
CASES = {
    'most-holy-name-jesus': (97, 89, 'Psalms', 8, 2),
    'saint-anthony-abbot': (98, 90, 'Matthew', 19, 21),
    'most-holy-name-mary': (132, 124, 'Luke', 1, 48),
}


class NonseasonalAntiphonOrderTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        loader = SourceFileLoader('_nonseasonal_order_owner', str(ROOT / 'tools/check-calendar-masses'))
        cls.check = module_from_spec(spec_from_loader(loader.name, loader))
        sys.modules[loader.name] = cls.check
        loader.exec_module(cls.check)
        cls.document = yaml.safe_load(SOURCE.read_text())
        cls.masses = {m['key']: m for s in cls.document['sections'].values() for m in s['masses']}

    def targeted(self, problems):
        return [message for message in problems if any(': ' + key + ':' in message for key in CASES)]

    def test_checked_communion_appointments_remain_between_offerings_and_after_communion(self):
        for key, (ap, pp, book, chapter, verse) in CASES.items():
            with self.subTest(mass=key):
                rows = self.masses[key]['propers']
                names = [r['name'] for r in rows]
                self.assertLess(names.index('Entrance Antiphon'), names.index('Communion Antiphon'))
                self.assertLess(names.index('Prayer over the Offerings'), names.index('Communion Antiphon'))
                self.assertLess(names.index('Communion Antiphon'), names.index('Prayer after Communion'))
                row, = [r for r in rows if r['name'] == 'Communion Antiphon']
                self.assertEqual(row['source'], 'scripture')
                entry, = row['verses']
                self.assertEqual(entry['book'], book)
                self.assertEqual(entry['ranges'], [{'begin': {'chapter': chapter, 'verse': verse},
                                                   'end': {'chapter': chapter, 'verse': verse}}])
                self.assertIn(f'artifact page {ap}, printed page {pp}', row['notes'])
                self.assertNotIn('text', row)
                self.assertNotIn('ordinary_disposition', row)

    def test_the_owning_printed_order_checker_accepts_source_order_and_refuses_append_regression(self):
        self.assertEqual(self.targeted(self.check.order_problems([SOURCE])), [])
        broken = copy.deepcopy(self.document)
        masses = {m['key']: m for s in broken['sections'].values() for m in s['masses']}
        for key in CASES:
            rows = masses[key]['propers']
            communion = next(r for r in rows if r['name'] == 'Communion Antiphon')
            rows.remove(communion)
            rows.append(communion)
        # Transplant only this fixture document. The actual canonical order owner,
        # Ordinary slot vocabulary and self-cleaning exception logic stay active.
        with patch.object(self.check, 'read_yaml', return_value=broken):
            errors = self.targeted(self.check.order_problems([SOURCE]))
        self.assertEqual(len(errors), 3)
        for key in CASES:
            self.assertTrue(any(': ' + key + ':' in e and 'Communion Antiphon stands behind' in e for e in errors))
        self.assertEqual(broken.get('proper_order_exceptions'), self.document.get('proper_order_exceptions'))


if __name__ == '__main__':
    unittest.main()
