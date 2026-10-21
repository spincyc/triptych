"""The Ordinary gate transports source paths to its one shared semantic owner."""
from __future__ import annotations

import copy
from importlib.machinery import SourceFileLoader
from importlib.util import module_from_spec, spec_from_loader
import json
import os
from pathlib import Path
import sys
import unittest
from unittest.mock import patch

ROOT = Path(os.environ.get('TRIPTYCH_REVIEW_ROOT', Path(__file__).resolve().parents[2]))
CODE = Path(os.environ.get('TRIPTYCH_ORDINARY_GATE_ROOT', ROOT))
SEATING = Path(os.environ.get('TRIPTYCH_APPOINTMENT_SEATING', ROOT / 'src/web/browser/liturgy/ordinary-seating.js'))
STRUCTURE = Path(os.environ.get('TRIPTYCH_SOURCE_PATH_STRUCTURE', ROOT / 'src/web/data/structure/propers/postconciliar.json'))
sys.path.insert(0, str(ROOT / 'scripts'))
loader = SourceFileLoader('_source_path_ordinary_transport', str(CODE / 'tools/mass-ordinary'))
spec = spec_from_loader(loader.name, loader)
O = module_from_spec(spec)
sys.modules[spec.name] = O
loader.exec_module(O)
O.ROOT = ROOT
O.SEATING_MODEL = SEATING


class OrdinarySourcePathTransport(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.ordinary = json.loads((ROOT / 'src/web/data/structure/ordinary/postconciliar.json').read_text())
        cls.structure = json.loads(STRUCTURE.read_text())
        # Exercise all held source-path forms. The fixture is canonical producer
        # output, and root's normal generated file is the durable default.
        cls.structure['masses'] = [m for m in cls.structure['masses'] if 'proper_source_paths' in m]
        if not cls.structure['masses']:
            raise AssertionError('the canonical postconciliar structure holds no source paths')
        cls.lent = next(m for m in cls.structure['masses'] if m['key'] == 'lent-3')

    def check_mass(self, mass, *, ordinary=None):
        return O.check_calendar_seating(ordinary or self.ordinary, {
            **self.structure, 'masses': [mass],
        })

    def test_all_actual_source_forms_use_one_batch_and_exact_unelected_context(self):
        before = copy.deepcopy(self.structure)
        with patch.object(O.subprocess, 'run', wraps=O.subprocess.run) as run:
            result = O.check_calendar_seating(self.ordinary, self.structure)
        self.assertEqual(result['failures'], 0)
        self.assertEqual(run.call_count, 1)
        payload = json.loads(run.call_args.kwargs['input'])
        expected = []
        for mass in self.structure['masses']:
            for form in mass.get('forms') or [{'id': 'main', 'propers': mass['propers']}]:
                expected.append((mass, form))
        self.assertEqual(len(result['source_appointments']), len(expected))
        self.assertEqual(sum(s['candidates'] for s in result['source_appointments']), sum(
            len(form['propers']) for _, form in expected))
        self.assertEqual(len(payload['forms']), len(expected))
        for sent, (mass, form) in zip(payload['forms'], expected):
            self.assertEqual(sent['mass'], mass['key'])
            self.assertEqual(sent['form_id'], form['id'])
            self.assertEqual(sent['source_paths'], mass['proper_source_paths'])
            self.assertEqual(sent['propers'], form['propers'])
            self.assertEqual(set(sent), {'mass', 'form_id', 'where', 'full', 'propers', 'source_paths'})
        self.assertEqual(set(payload), {'ordinary', 'forms', 'facts'})
        self.assertTrue(all(set(s) == {'mass', 'form_id', 'candidates', 'conditional_rows',
            'choice_groups', 'diagnostics'} for s in result['source_appointments']))
        self.assertEqual(self.structure, before)

    def test_source_mass_field_or_raw_member_guard_triggers_the_owner(self):
        self.assertTrue(O.appointment_seating_required([{'name': 'Gospel', 'source_path_relation': 'held'}]))
        self.assertTrue(O.appointment_seating_required([{'name': 'Gospel', 'source_path_relation': None}]))
        for value in (None, {}, 'malformed', []):
            with self.subTest(value=value):
                self.assertTrue(O.appointment_seating_required([{'name': 'Gospel'}], {'proper_source_paths': value}))
        self.assertFalse(O.appointment_seating_required([{'name': 'Gospel'}], {'key': 'plain'}))
        # A raw guard cannot bypass the owner when its declaration was lost.
        rows = [copy.deepcopy(next(p for p in self.lent['propers'] if p.get('source_path_relation')))]
        with self.assertRaisesRegex(O.SourceError, 'membership|relation'):
            O.check_form_seating(self.ordinary, rows, 'postconciliar/technical/main', full=True,
                mass='technical', form_id='main')

    def test_malformed_mass_declarations_are_forwarded_without_default_stripping(self):
        for value in (None, {}, 'malformed'):
            mass = copy.deepcopy(self.lent)
            mass['proper_source_paths'] = value
            with self.subTest(value=value), patch.object(O.subprocess, 'run', wraps=O.subprocess.run) as run:
                with self.assertRaisesRegex(O.SourceError, 'source-owned relation list'):
                    self.check_mass(mass)
                sent = json.loads(run.call_args.kwargs['input'])['forms'][0]
                self.assertEqual(sent['source_paths'], value)
        mass = copy.deepcopy(self.lent)
        mass['proper_source_paths'] = []
        with self.assertRaisesRegex(O.SourceError, 'membership|relation'):
            self.check_mass(mass)

    def test_missing_guard_and_wrong_material_are_refused_by_shared_owner(self):
        mass = copy.deepcopy(self.lent)
        del next(p for p in mass['propers'] if p.get('source_path_relation'))['source_path_relation']
        with self.assertRaisesRegex(O.SourceError, 'guard|membership'):
            self.check_mass(mass)
        mass = copy.deepcopy(self.lent)
        mass['proper_source_paths'][0]['paths'][0]['members'][0]['material_cycle']['cycle'] = 'D'
        with self.assertRaisesRegex(O.SourceError, 'material cycle is not held'):
            self.check_mass(mass)

    def test_unselected_raw_candidate_cannot_hide_an_unknown_seat(self):
        mass = copy.deepcopy(self.lent)
        member = next(p for p in mass['propers'] if p.get('source_path_relation') and p['name'] == 'First Reading (shorter form)')
        old = member['name']; member['name'] = 'Unmapped source role'
        member['appointment_identity']['proper'] = member['name']
        for relation in mass['proper_source_paths']:
            for path in relation['paths']:
                for item in path['members']:
                    if item['appointment']['proper'] == old:
                        item['appointment']['proper'] = member['name']
        with self.assertRaisesRegex(O.SourceError, 'no usable|one.*seat|mapped|semantic|functional'):
            self.check_mass(mass)

    def test_foreign_path_members_require_every_original_marker(self):
        mass = copy.deepcopy(self.lent)
        target = 'technical-foreign-edition'
        ordinary = {**self.ordinary, 'calendar': target}
        for proper in mass['propers']:
            if proper.get('source_path_relation'):
                proper['appointment_applicability'] = {'state': 'unresolved',
                    'reason': 'foreign-source-applicability', 'source_edition': self.structure['calendar'],
                    'target_edition': target, 'basis': 'Technical foreign source contract fixture.'}
        result = self.check_mass(mass, ordinary=ordinary)
        diagnostics = result['source_appointments'][0]['diagnostics']
        self.assertEqual(len(diagnostics), sum(bool(p.get('source_path_relation')) for p in mass['propers']))
        del next(p for p in mass['propers'] if p.get('source_path_relation'))['appointment_applicability']
        with self.assertRaisesRegex(O.SourceError, 'every original unsupported applicability marker'):
            self.check_mass(mass, ordinary=ordinary)

    def test_palm_unavailable_frame_is_preserved_without_a_full_frame_claim(self):
        palm = next(m for m in self.structure['masses'] if m['key'] == 'palm-sunday')
        self.assertEqual(palm['ordinary_frame']['applicability'], 'unavailable')
        with patch.object(O.subprocess, 'run', wraps=O.subprocess.run) as run:
            result = self.check_mass(palm)
        self.assertEqual(result['full_forms'], 0)
        self.assertEqual(result['nonfull_forms'], 1)
        self.assertFalse(json.loads(run.call_args.kwargs['input'])['forms'][0]['full'])
        self.assertNotIn('events', result['source_appointments'][0])

    def test_legacy_path_is_unchanged_and_missing_node_fails_for_new_paths(self):
        with patch.object(O.shutil, 'which', return_value=None), patch.object(O.subprocess, 'run') as run:
            O.check_form_seating(self.ordinary, [{'name': 'First Reading'}, {'name': 'Gospel'}],
                'postconciliar/plain/main', full=True)
            self.assertEqual(run.call_count, 0)
            with self.assertRaisesRegex(O.SourceError, 'node is not installed'):
                self.check_mass(self.lent)
            self.assertEqual(run.call_count, 0)
        with patch.object(O.subprocess, 'run', wraps=O.subprocess.run) as run:
            O.check_form_seating(self.ordinary, self.lent['propers'], 'postconciliar/lent-3/main',
                full=True, mass='lent-3', form_id='main', source_mass=self.lent)
        self.assertEqual(run.call_count, 1)
        self.assertEqual(json.loads(run.call_args.kwargs['input'])['forms'][0]['source_paths'], self.lent['proper_source_paths'])


if __name__ == '__main__':
    unittest.main()
