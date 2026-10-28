"""1962 page-image appointments: units1532 and1612–1617; no votive leakage."""
import sys
import tomllib
import unittest
from pathlib import Path
from importlib.machinery import SourceFileLoader
from importlib.util import module_from_spec, spec_from_loader
import yaml
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'scripts'))
from _calendars import resolve_propers

def load_checker():
    loader = SourceFileLoader('after_pentecost_source_checker', str(ROOT / 'tools/check-calendar-masses'))
    module = module_from_spec(spec_from_loader(loader.name, loader))
    sys.modules[loader.name] = module
    loader.exec_module(module)
    return module

class AfterPentecostSourceAppointmentTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.document = yaml.safe_load((ROOT / 'src/sources/calendars/roman-1962/propers.yaml').read_text())
        cls.masses = {m['key']: m for section in cls.document['sections'].values() for m in section['masses']}
        cls.checker = load_checker()

    def resolved(self, key):
        entries, errors = resolve_propers(self.document, self.masses[key], appointments=True)
        self.assertEqual(errors, [])
        return [p for form, p, origin in entries]

    def test_tenth_sunday_introit_1532_uses_discrete_printed_verses(self):
        # MR1962 physical470/printed389, rightcolumn:17,18,20,23; Psalmverse2.
        proper = next(p for p in self.resolved('pentecost-10') if p['name'] == 'Introit')
        ranges = [r for citation in proper['verses'] for r in citation['ranges']]
        self.assertEqual([(r['begin']['chapter'], r['begin']['verse'], r['end']['verse']) for r in ranges],
                         [(54, 17, 18), (54, 20, 20), (54, 23, 23), (54, 2, 2)])

    def test_ember_wednesday_1612_includes_the_printed_psalm_verse(self):
        # MR1962 physical481/printed400, leftcolumn:antiphon2–5; Psalmverse6.
        proper = next(p for p in self.resolved('september-ember-wednesday') if p['name'] == 'Introit')
        self.assertEqual([(r['begin']['chapter'], r['begin']['verse'], r['end']['verse'])
                          for c in proper['verses'] for r in c['ranges']], [(80, 2, 5), (80, 6, 6)])

    def test_ember_wednesday_oratio_1616_remains_between_gradual_and_lesson(self):
        # MR1962 physical481/printed400, rightcolumn:1615,1616,1617.
        propers = self.resolved('september-ember-wednesday')
        names = [p['name'] for p in propers]
        self.assertEqual(names, ['Introit', 'Collect', 'First Lesson', 'First Gradual', 'Oratio',
                                 'Second Lesson', 'Second Gradual', 'Gospel', 'Offertory', 'Secret',
                                 'Communion', 'Postcommunion'])
        proper = propers[4]
        problems = []
        self.checker.check_proper('september-ember-wednesday', proper, problems,
                                  calendar='roman-1962', season='after-pentecost')
        self.assertEqual(problems, [])
        self.assertTrue(proper.get('text') or proper.get('text_status', {}).get('scope') == 'proper-body')
        inventory = tomllib.loads((ROOT / 'src/sources/inventories/missal-expected-targets-v1.toml').read_text())
        target = next(r for r in inventory['targets'] if r['id'] == 'roman-1962.temporal.september-ember-wed:collect:2')
        self.assertEqual((target['calendar_proper_name'], target['calendar_proper_occurrence']), ('Oratio', 1))
        english = tomllib.loads((ROOT / 'src/sources/inventories/roman-1962-proper-translations-v1.toml').read_text())
        identity = ('september-ember-wednesday', 'main', 'Oratio', 'all', 1)
        same = lambda r: (r.get('mass'), r.get('form_id'), r.get('proper'), r.get('cycle'), r.get('occurrence')) == identity
        rows = [r for r in english['untranslated'] if same(r) and r.get('lang') == 'en']
        rows += [r for r in english['entries'] if same(r) and 'en' in [t['lang'] for t in r['translations']]]
        self.assertEqual(len(rows), 1)
        # da270a039: the no-exemplar absence became one confirmed Lefebvre entry (english22-latin3-source-adoption.json
        # under workflows/reviews/missal-reader-completion-2026-10-26; [[accepted]] existing-forward-five).
        self.assertEqual((rows[0].get('witness'), rows[0].get('collation_result')), ('lefebvre-1925', 'confirmed'))

    def test_christ_king_3943_3944_votive_alternatives_do_not_enter_normal_form(self):
        # MR1962 physical779/printed698,L: the preceding clause expressly says In Missis votivis.
        names = [p['name'] for p in self.resolved('christ-the-king')]
        self.assertEqual(names, ['Introit', 'Collect', 'Epistle', 'Gradual', 'Alleluia', 'Gospel',
                                 'Offertory', 'Secret', 'Communion', 'Postcommunion'])
        self.assertNotIn('Tract', names)
        self.assertEqual(names.count('Alleluia'), 1)

if __name__ == '__main__':
    unittest.main()
