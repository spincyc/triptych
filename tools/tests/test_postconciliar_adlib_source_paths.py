"""The three OLM provisions keep exact source roles, choices and material loci."""
from pathlib import Path
from importlib.machinery import SourceFileLoader
from importlib.util import module_from_spec, spec_from_loader
import sys
import unittest
import yaml

ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / 'src/sources/calendars/postconciliar/propers.yaml'
NEW_OPTIONS = [
    ('First Reading', 2, 'B', 'Genesis 15:1-6; 21:1-3'),
    ('First Reading', 3, 'C', '1 Samuel 1:20-22, 24-28'),
    ('Responsorial Psalm', 2, 'B', 'Psalm 104:1b-2, 3-4, 5-6, 8-9'),
    ('Responsorial Psalm', 3, 'C', 'Psalm 83:2-3, 5-6, 9-10'),
    ('Second Reading', 2, 'B', 'Hebrews 11:8, 11-12, 17-19'),
    ('Second Reading', 3, 'C', '1 John 3:1-2, 21-24'),
]


def tool(name):
    loader = SourceFileLoader('_adlib_source_' + name.replace('-', '_'), str(ROOT / 'tools' / name))
    module = module_from_spec(spec_from_loader(loader.name, loader))
    sys.modules[loader.name] = module
    loader.exec_module(module)
    return module


class AdLibitumSourcePathsTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.document = yaml.safe_load(SOURCE.read_text())
        cls.masses = {m['key']: m for s in cls.document['sections'].values() for m in s['masses']}
        cls.propers = tool('mass-propers')
        cls.canon = tool('citations')
        cls.check = tool('check-calendar-masses')
        from _calendars import ordinary_disposition_source_problems
        cls.group_problems = staticmethod(ordinary_disposition_source_problems)

    def test_six_holy_family_options_keep_exact_owner_occurrence_sparse_cycle_and_citation(self):
        mass = self.masses['holy-family']
        for role, occurrence, cycle, reference in NEW_OPTIONS:
            with self.subTest(role=role, occurrence=occurrence):
                proper = [p for p in mass['propers'] if p['name'] == role][occurrence - 1]
                self.assertEqual(self.propers.source_slot_identity(self.document, mass, '', proper, None),
                                 ('holy-family', 'main', role, occurrence))
                self.assertEqual(set(proper['cycles']), {cycle})
                self.assertEqual(proper['cycles'][cycle]['verses'], [self.canon.parse_citation(reference)])
                self.assertEqual(proper['ordinary_disposition']['option'], 'year-' + cycle.lower())
                self.assertEqual(proper['source'], 'scripture')
                for field in ('text', 'incipit', 'translations', 'latin', 'rights'):
                    self.assertNotIn(field, proper)
                problems = []
                self.check.check_proper('holy-family/' + role, proper, problems,
                                        calendar='postconciliar', season='christmas')
                self.assertEqual(problems, [])
        self.assertEqual(self.group_problems('holy-family', '', mass['propers']), [])
        duplicate_problems = []
        self.check.check_duplicate_proper_bodies('holy-family', mass, duplicate_problems)
        self.assertEqual(duplicate_problems, [])

    def test_printed_optional_psalm_numbers_reach_the_existing_citation_owner(self):
        rows = [p for p in self.masses['holy-family']['propers'] if p['name'] == 'Responsorial Psalm']
        expected = [
            (104, 105, [(1, 2), (3, 4), (5, 6), (8, 9)]),
            (83, 84, [(2, 3), (5, 6), (9, 10)]),
        ]
        for proper, (printed, hebrew, bounds) in zip(rows[1:], expected):
            self.assertEqual(proper['psalm_numbering'], 'vulgate')
            cycle = next(iter(proper['cycles'].values()))
            entry = cycle['verses'][0]
            citation = self.propers.citation_structure(entry, proper['psalm_numbering'], self.propers.book_tokens())
            self.assertIsNone(citation['unresolved'])
            for system, chapter in (('vulgate', printed), ('hebrew', hebrew)):
                self.assertEqual(citation['loci'][system], [
                    {'chapter': chapter, 'first': first, 'last': last} for first, last in bounds])

    def test_holy_family_common_and_actual_cycle_gospel_remain_separate(self):
        rows = self.masses['holy-family']['propers']
        controls = [('First Reading', 'Sirach 3:3-7, 14-17a'),
                    ('Responsorial Psalm', 'Psalm 128:1-2, 3, 4-5'),
                    ('Second Reading', 'Colossians 3:12-21')]
        for role, reference in controls:
            group = [p for p in rows if p['name'] == role]
            self.assertEqual(len(group), 3)
            self.assertEqual(group[0]['verses'][0]['ref'], reference)
            self.assertNotIn('cycles', group[0])
            self.assertEqual([p['ordinary_disposition']['option'] for p in group], ['common', 'year-b', 'year-c'])
        gospel = [p for p in rows if p['name'] in ('Gospel', 'Gospel (shorter form)')]
        self.assertEqual([p['ordinary_disposition']['option'] for p in gospel], ['longer', 'shorter'])
        self.assertEqual(set(gospel[0]['cycles']), {'A', 'B', 'C'})
        self.assertEqual(set(gospel[1]['cycles']), {'B'})
        relation = self.masses['holy-family']['proper_source_paths'][0]
        for path in relation['paths']:
            self.assertEqual(len(path['members']), 4)
            self.assertEqual(set(path['choices']), {'first-reading', 'responsorial-psalm', 'second-reading'})
            self.assertNotIn('Gospel', [m['appointment']['proper'] for m in path['members']])
            self.assertEqual(path['members'][-1]['appointment']['proper'], 'Gospel Acclamation')

    def test_principal_calendar_scope_and_optional_material_addresses_are_source_explicit(self):
        cases = [('holy-family', 'main', 'holy-family-reading-provisions', 4),
                 ('baptism-of-the-lord', 'main', 'baptism-reading-provisions', 4),
                 ('pentecost', 'day', 'pentecost-day-readings', 2)]
        for key, form, relation_id, count in cases:
            relation, = self.masses[key]['proper_source_paths']
            self.assertEqual((relation['id'], relation['form_id']), (relation_id, form))
            common, year_b, year_c = relation['paths']
            self.assertEqual(common['standing'], 'principal')
            self.assertEqual(common['calendar_cycles'], {'family': 'sunday', 'in': ['A', 'B', 'C']})
            for path, cycle in ((year_b, 'B'), (year_c, 'C')):
                self.assertEqual(path['standing'], 'optional')
                self.assertEqual(path['calendar_cycles'], {'family': 'sunday', 'in': [cycle]})
                self.assertEqual([member['material_cycle'] for member in path['members']],
                                 [{'family': 'cycles', 'cycle': cycle}] * count)
            if key == 'holy-family':
                self.assertEqual([member['material_cycle'] for member in common['members']],
                                 [{'family': None, 'cycle': 'all'}] * 3 + [{'family': 'cycles', 'cycle': 'A'}])
                for path, occurrence in ((common, 1), (year_b, 2), (year_c, 3)):
                    self.assertEqual([m['appointment']['occurrence'] for m in path['members']],
                                     [occurrence] * 3 + [1])
            else:
                for path in relation['paths']:
                    self.assertEqual(path['choices'], {})
                self.assertEqual([member['material_cycle'] for member in common['members']],
                                 [{'family': 'cycles', 'cycle': 'A'}] * count)


if __name__ == '__main__':
    unittest.main()
