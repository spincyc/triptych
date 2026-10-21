"""The Ordo's OT18 Tuesday Gospel option remains an actual selectable appointment."""
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

class OT18TuesdayOptionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        d = yaml.safe_load(SOURCE.read_text())
        cls.masses = {m['key']: m for s in d['sections'].values() for m in s['masses']}
        loader = SourceFileLoader('_ot18_citations', str(ROOT / 'tools/citations'))
        cls.canon = module_from_spec(spec_from_loader(loader.name, loader)); loader.exec_module(cls.canon)

    def test_exact_principal_and_optional_gospels_keep_one_source_group(self):
        rows = [r for r in self.masses['ot-18-tuesday']['propers'] if r['name'].startswith('Gospel') and r['name'] != 'Gospel Acclamation']
        self.assertEqual([r['name'] for r in rows], ['Gospel', 'Gospel (ad libitum)'])
        self.assertEqual([r['ordinary_disposition']['option'] for r in rows], ['principal', 'ad-libitum'])
        self.assertEqual([r['verses'] for r in rows], [[self.canon.parse_citation(ref)] for ref in ['Matthew 14:22-36', 'Matthew 15:1-2, 10-14']])
        self.assertEqual(ordinary_disposition_group_problems('ot-18-tuesday', [('', r, None) for r in rows]), [])
        self.assertTrue(ordinary_disposition_group_problems('ot-18-tuesday', [('', rows[0], None)]))

    def test_option_is_not_restricted_to_year_a_or_given_a_body(self):
        row = next(r for r in self.masses['ot-18-tuesday']['propers'] if r['name'] == 'Gospel (ad libitum)')
        self.assertFalse({'cycles', 'weekday_cycles', 'text', 'latin', 'translations', 'incipit'} & set(row))
        self.assertIn('preference, not a condition', row['notes'])

if __name__ == '__main__':
    unittest.main()
