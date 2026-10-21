"""Source-located Common short forms remain explicit, qualified Gospel options."""
from pathlib import Path
from importlib.machinery import SourceFileLoader
from importlib.util import module_from_spec, spec_from_loader
import sys
import unittest
import yaml

ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / "src/sources/calendars/postconciliar/propers.yaml"
sys.path.insert(0, str(ROOT / "scripts"))
from _calendars import resolve_propers

# OLM 1981 n602/artifact351 -> n730.5/artifact390; n686/artifact371 -> n742.12/artifact397.
# The dated pages print the long reference only; Common alternatives are permitted by n83.
FACTS = {
    "saint-lawrence-brindisi-priest-doctor-church": ("Mark 4:1-10, 13-20", "Mark 4:1-9"),
    "saint-john-damascene-priest-doctor-church": ("Matthew 25:14-30", "Matthew 25:14-23"),
}

def load_tool(name):
    loader = SourceFileLoader("_common_short_" + name.replace("-", "_"), str(ROOT / "tools" / name))
    mod = module_from_spec(spec_from_loader(loader.name, loader))
    sys.modules[loader.name] = mod
    loader.exec_module(mod)
    return mod

class CommonShortFormsTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.document = yaml.safe_load(SOURCE.read_text())
        cls.masses = {m['key']: m for s in cls.document['sections'].values() for m in s['masses']}
        cls.citations = load_tool('citations')
        cls.owner = load_tool('check-calendar-masses')

    def test_preserved_long_and_common_short_have_exact_source_ranges(self):
        for key, (long_ref, short_ref) in FACTS.items():
            with self.subTest(mass=key):
                rows = self.masses[key]['propers']
                index = next(i for i, row in enumerate(rows) if row['name'] == 'Gospel')
                long, short = rows[index:index+2]
                self.assertEqual(short['name'], 'Gospel (shorter form)')
                self.assertEqual(long['verses'], [self.citations.parse_citation(long_ref)])
                self.assertEqual(short['verses'], [self.citations.parse_citation(short_ref)])
                self.assertNotIn('cycles', short)

    def test_owner_resolves_two_members_of_one_choice_in_the_same_seat(self):
        for key in FACTS:
            with self.subTest(mass=key):
                mass = self.masses[key]
                problems = []
                self.owner.check_entry(mass, 0, problems, section_kind='sanctoral', calendar='postconciliar')
                self.assertEqual(problems, [])
                entries, problems = resolve_propers(self.document, mass)
                self.assertEqual(problems, [])
                members = [row for _, row, _ in entries if row['name'] in ('Gospel', 'Gospel (shorter form)')]
                self.assertEqual([r['ordinary_disposition']['option'] for r in members], ['longer', 'shorter'])
                self.assertTrue(all(r['ordinary_disposition']['kind'] == 'alternative' and r['ordinary_disposition']['group'] == 'gospel' for r in members))
                self.assertEqual(members[0]['ordinary_disposition']['basis'], members[1]['ordinary_disposition']['basis'])

    def test_reading_citation_does_not_complete_the_missal_or_adopt_words(self):
        for key in FACTS:
            with self.subTest(mass=key):
                mass = self.masses[key]
                self.assertEqual((mass['text_status']['state'], mass['text_status']['scope']), ('partial', 'missal-formulary'))
                short, = [r for r in mass['propers'] if r['name'] == 'Gospel (shorter form)']
                self.assertEqual(short['source'], 'scripture')
                self.assertFalse({'text', 'latin', 'incipit', 'translations', 'cycles'} & set(short))

if __name__ == '__main__':
    unittest.main()
