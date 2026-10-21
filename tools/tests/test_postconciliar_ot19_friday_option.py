"""OLM417's optional Ezekiel reading is available only in its source YearII."""
from pathlib import Path
from importlib.machinery import SourceFileLoader
from importlib.util import module_from_spec, spec_from_loader
import sys
import unittest
import yaml
ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / 'src/sources/calendars/postconciliar/propers.yaml'
sys.path.insert(0, str(ROOT / 'scripts'))
from _calendars import ordinary_disposition_group_problems

class OT19FridayOptionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        d = yaml.safe_load(SOURCE.read_text())
        cls.mass = next(m for s in d['sections'].values() for m in s['masses'] if m['key'] == 'ot-19-friday')
        loader = SourceFileLoader('_ot19_citations', str(ROOT / 'tools/citations'))
        cls.canon = module_from_spec(spec_from_loader(loader.name, loader)); loader.exec_module(cls.canon)

    def test_exact_principal_and_optional_appointments_and_source_cycles(self):
        rows = self.mass['propers'][:2]
        self.assertEqual([r['name'] for r in rows], ['First Reading', 'First Reading (ad libitum)'])
        self.assertEqual([r['ordinary_disposition']['option'] for r in rows], ['principal', 'ad-libitum'])
        self.assertEqual(set(rows[0]['weekday_cycles']), {'I', 'II'})
        self.assertEqual(set(rows[1]['weekday_cycles']), {'II'})
        self.assertEqual(rows[0]['weekday_cycles']['I']['verses'], [self.canon.parse_citation('Joshua 24:1-13')])
        self.assertEqual(rows[0]['weekday_cycles']['II']['verses'], [self.canon.parse_citation('Ezekiel 16:1-15, 60, 63')])
        self.assertEqual(rows[1]['weekday_cycles']['II']['verses'], [self.canon.parse_citation('Ezekiel 16:59-63')])
        self.assertEqual(ordinary_disposition_group_problems('ot-19-friday', [('', r, None) for r in rows]), [])
        self.assertTrue(ordinary_disposition_group_problems('ot-19-friday', [('', rows[0], None)]))

    def test_option_does_not_invent_year_i_or_liturgical_wording(self):
        row = self.mass['propers'][1]
        self.assertNotIn('I', row['weekday_cycles'])
        for owner in (row, row['weekday_cycles']['II']):
            self.assertFalse({'cycles', 'text', 'latin', 'translations', 'incipit'} & set(owner))

if __name__ == '__main__':
    unittest.main()
