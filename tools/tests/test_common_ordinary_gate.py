"""The static Ordinary gate retains every source-owned Common candidate."""
from __future__ import annotations

import copy
import importlib.machinery
import importlib.util
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tomllib
import unittest
from unittest.mock import patch

ROOT = Path(os.environ.get('TRIPTYCH_REVIEW_ROOT', Path(__file__).resolve().parents[2]))
CODE = Path(os.environ.get('TRIPTYCH_ORDINARY_GATE_ROOT', ROOT))
PYTHON = Path(os.environ.get('TRIPTYCH_APPOINTMENT_MODULE_ROOT', ROOT))
SOURCE = Path(os.environ.get('TRIPTYCH_COMMON_SOURCE_ROOT', ROOT))
ORDINARY_SOURCE = Path(os.environ.get('TRIPTYCH_COMMON_ORDINARY_SOURCE_ROOT', ROOT))
sys.path.insert(0, str(ROOT / 'scripts'))
sys.path.insert(0, str(PYTHON / 'scripts'))
import _calendars as C


def tool(name, directory):
    loader = importlib.machinery.SourceFileLoader('_common_gate_' + name.replace('-', '_'), str(directory / 'tools' / name))
    spec = importlib.util.spec_from_loader(loader.name, loader)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    loader.exec_module(module)
    for key, value in list(vars(module).items()):
        if isinstance(value, Path) and value.is_relative_to(directory):
            setattr(module, key, ROOT / value.relative_to(directory))
    module.ROOT = ROOT
    return module


O = tool('mass-ordinary', CODE)
O.SEATING_MODEL = CODE / 'src/web/browser/liturgy/ordinary-seating.js'
MP = tool('mass-propers', PYTHON)
FACTS = {'fixture-season': {'edition': 'roman-1962', 'values': ['inside', 'outside'],
    'season_values': {'inside': 'inside', 'outside': 'outside'}, 'basis': 'Technical source condition fixture.'}}


def coordinate(name, occurrence=1):
    return {'mass': 'technical-common', 'form_id': 'main', 'proper': name, 'occurrence': occurrence}


def row(name, occurrence=1):
    return {'name': name, 'appointment_identity': coordinate(name, occurrence)}


def choice_rows():
    rows = [row('Introit'), row('Epistle'), row('Gospel'), row('Offertory'), row('Gospel (vel)')]
    for index, option in [(2, 'principal'), (4, 'other')]:
        rows[index]['ordinary_disposition'] = {'kind': 'alternative', 'group': 'technical-gospel',
            'option': option, 'basis': 'Technical nonadjacent source alternative.', 'anchor': coordinate('Gospel')}
    return rows


def conditioned(name='Gradual'):
    proper = row(name)
    proper['ordinary_disposition'] = {'kind': 'conditional', 'group': 'technical-conditional',
        'basis': 'Technical source condition fixture.', 'when': {'fact': 'fixture-season', 'in': ['inside']}}
    return proper


class CommonOrdinaryGate(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.ordinary = json.loads((ROOT / 'src/web/data/structure/ordinary/roman-1962.json').read_text())
        inventory = tomllib.loads((ORDINARY_SOURCE / 'src/sources/inventories/roman-1962-ordo-missae-v1.toml').read_text())
        cls.ordinary['slots'] = O.slot_table(inventory, cls.ordinary['sections'], 'roman-1962')
        cls.source = C.read_yaml(SOURCE / 'src/sources/calendars/roman-1962/propers.yaml')
        # A bounded in-memory projection of the actual Common source, using
        # the canonical producer and all its referenced terminal owners.
        cls.source.pop('citation_divergences', None)
        # The finite dated execution sources validate non-Common hosts outside
        # this projection; their own tests own them.
        with patch.object(MP, 'load_calendar', return_value=cls.source), patch.object(
            MP, 'masses_of', return_value=[('common', mass) for mass in cls.source['sections']['common']['masses']]
        ), patch.object(MP._oration_execution, 'load_sources', return_value={}), patch.object(
            MP._name_execution, 'load_name_sources', return_value={}
        ):
            cls.structure = MP.calendar_structure(ROOT / 'src/sources/calendars', 'roman-1962', MP.book_tokens())

    def check(self, rows, *, full=True, facts=None, ordinary=None):
        O.check_form_seating(ordinary or self.ordinary, rows, 'roman-1962/technical-common/main',
            full=full, mass='technical-common', form_id='main', facts=FACTS if facts is None else facts)

    def node(self, code, data):
        node = shutil.which('node')
        if node is None:
            self.skipTest('node is not installed')
        result = subprocess.run([node, '-e', code, str(O.SEATING_MODEL)], input=json.dumps(data),
            text=True, capture_output=True, check=False, timeout=30)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        return json.loads(result.stdout)

    def test_actual_thirty_commons_are_checked_once_in_one_batch(self):
        before = copy.deepcopy(self.structure)
        with patch.object(O.subprocess, 'run', wraps=O.subprocess.run) as run:
            result = O.check_calendar_seating(self.ordinary, self.structure)
        self.assertEqual(result['full_forms'], 30)
        self.assertEqual(result['failures'], 0)
        self.assertEqual(run.call_count, 1)
        summaries = result['source_appointments']
        self.assertGreater(len(summaries), 0)
        expected = [m for m in self.structure['masses'] if O.appointment_seating_required(m['propers'])]
        self.assertEqual({s['mass'] for s in summaries}, {m['key'] for m in expected})
        self.assertEqual(sum(s['candidates'] for s in summaries), sum(len(m['propers']) for m in expected))
        self.assertEqual(sum(s['conditional_rows'] for s in summaries), sum(
            p.get('ordinary_disposition', {}).get('kind') == 'conditional' for m in expected for p in m['propers']))
        self.assertGreater(sum(s['choice_groups'] for s in summaries), 0)
        self.assertTrue(all(s['diagnostics'] == [] for s in summaries))
        self.assertEqual(self.structure, before)

    def test_anchored_choice_uses_principal_position_without_losing_candidates(self):
        rows = choice_rows()
        before = copy.deepcopy(rows)
        self.check(rows)
        self.assertEqual(rows, before)
        moved = rows[1:] + rows[:1]
        with self.assertRaisesRegex(O.SourceError, 'runs backward'):
            self.check(moved)

    def test_hidden_conditional_bad_seat_is_checked_when_false_or_unknown(self):
        rows = [row('Epistle'), conditioned('Unclaimed conditional'), row('Gospel')]
        code = r"""const S=require(process.argv[1]);let t='';process.stdin.on('data',c=>t+=c);process.stdin.on('end',()=>{const p=JSON.parse(t);const out=['propers','day'].map(entrance=>{const x=S.prepareProperAppointments(p.rows,{calendar:'roman-1962',entrance,date:entrance==='day'?'2026-01-02':null,season:entrance==='day'?'outside':null,facts:p.facts});return{unresolved:x.unresolved.length,inactive:x.inactive.length};});process.stdout.write(JSON.stringify(out));});"""
        self.assertEqual(self.node(code, {'rows': rows, 'facts': FACTS}), [
            {'unresolved': 1, 'inactive': 0}, {'unresolved': 0, 'inactive': 1}])
        with self.assertRaisesRegex(O.SourceError, 'no usable Ordinary seat'):
            self.check(rows)
        self.check([row('Epistle'), conditioned(), row('Gospel')])

    def test_all_metadata_is_checked_before_placeholder_or_condition_filtering(self):
        cases = []
        bad = choice_rows(); bad[2]['ordinary_disposition']['anchor']['occurrence'] = 99; cases.append((bad, 'anchor'))
        bad = choice_rows(); bad[4]['appointment_identity'] = copy.deepcopy(bad[2]['appointment_identity']); cases.append((bad, 'duplicate'))
        bad = choice_rows(); bad[4]['ordinary_disposition']['anchor']['mass'] = 'wrong-mass'; cases.append((bad, 'owner, anchor'))
        bad = [conditioned()]; bad[0]['ordinary_disposition']['when']['in'] = ['unheld']; cases.append((bad, 'unheld source fact value'))
        bad = [conditioned()]; bad[0]['ordinary_disposition']['extra'] = True; cases.append((bad, 'unsupported shape'))
        bad = [conditioned('Placeholder')]; cases.append((bad, 'no usable Ordinary seat'))
        for rows, message in cases:
            with self.subTest(message=message), self.assertRaisesRegex(O.SourceError, message):
                self.check(rows)
        with self.assertRaisesRegex(O.SourceError, 'fact is unheld'):
            self.check([conditioned()], facts={})

    def test_cross_seat_and_gospel_forged_as_reading_one_refuse(self):
        rows = choice_rows(); rows[4]['name'] = 'Epistle'
        with self.assertRaisesRegex(O.SourceError, 'share one established semantic seat'):
            self.check(rows)
        rows = choice_rows()
        for proper in [rows[2], rows[4]]:
            proper['ordinary_disposition']['seat'] = 'reading-1'
        with self.assertRaisesRegex(O.SourceError, 'share one established semantic seat'):
            self.check(rows)
        rows = choice_rows(); rows[4]['name'] = 'Gospel (unheld qualifier)'
        with self.assertRaisesRegex(O.SourceError, 'usable semantic Ordinary seat'):
            self.check(rows)
        self.assertIsNone(self.node(r"""const S=require(process.argv[1]);process.stdout.write(JSON.stringify(S.semanticProperId({name:'Lesson'},true)));""", {}))

    def test_foreign_rows_keep_typed_diagnostics_and_execution_still_refuses(self):
        source = copy.deepcopy(self.source)
        target = C.read_yaml(ROOT / 'src/sources/calendars/roman-pre-1955/propers.yaml')
        target['sections'] = {}
        target.pop('citation_divergences', None)
        base = C._apply_departures(target, source, 'roman-1962')
        with patch.object(MP, 'load_calendar', return_value=base), patch.object(
            MP, 'masses_of', return_value=[('common', mass) for mass in base['sections']['common']['masses']]
        ):
            structure = MP.calendar_structure(ROOT / 'src/sources/calendars', 'roman-pre-1955', MP.book_tokens())
        ordinary = copy.deepcopy(self.ordinary); ordinary['calendar'] = 'roman-pre-1955'
        result = O.check_calendar_seating(ordinary, structure)
        diagnostics = [d for s in result['source_appointments'] for d in s['diagnostics']]
        self.assertGreater(len(diagnostics), 0)
        self.assertTrue(all(d['source_edition'] == 'roman-1962' and d['target_edition'] == 'roman-pre-1955' for d in diagnostics))
        selected = next(p for m in structure['masses'] for p in m['propers'] if p.get('appointment_applicability'))
        code = r"""const S=require(process.argv[1]);let t='';process.stdin.on('data',c=>t+=c);process.stdin.on('end',()=>{const p=JSON.parse(t);const errors=[];for(const f of [()=>S.prepareProperAppointments([p],{calendar:'roman-pre-1955',entrance:'propers'}),()=>S.unframedEvents([p]),()=>S.unframedEvents([{...p,name:'Placeholder'}],()=>true)]){try{f();errors.push(null);}catch(e){errors.push(e.message);}}process.stdout.write(JSON.stringify(errors));});"""
        errors = self.node(code, selected)
        self.assertTrue(all('unsupported foreign-source Proper applicability' in error for error in errors))
        bad = copy.deepcopy(selected); bad['appointment_applicability']['target_edition'] = 'another-edition'
        with self.assertRaisesRegex(O.SourceError, 'exact unresolved foreign editions'):
            self.check([bad], ordinary=ordinary, facts={})
        bad = copy.deepcopy(selected); bad['ordinary_disposition'] = copy.deepcopy(conditioned()['ordinary_disposition'])
        bad['appointment_identity'] = coordinate(bad['name'])
        with self.assertRaisesRegex(O.SourceError, 'fact is unheld'):
            self.check([bad], ordinary=ordinary, facts={})

    def test_foreign_marker_does_not_excuse_a_malformed_legacy_group(self):
        rows = choice_rows()
        marker = {'state': 'unresolved', 'reason': 'foreign-source-applicability',
            'source_edition': 'roman-1962', 'target_edition': 'roman-pre-1955', 'basis': 'Technical unsupported source condition.'}
        for proper in [rows[2], rows[4]]:
            del proper['ordinary_disposition']['anchor']
            proper['appointment_applicability'] = marker
        ordinary = copy.deepcopy(self.ordinary); ordinary['calendar'] = 'roman-pre-1955'
        with self.assertRaisesRegex(O.SourceError, 'contiguous|at least two distinct options'):
            self.check(rows, ordinary=ordinary, facts={})

    def test_pure_legacy_path_keeps_its_existing_controls_without_node(self):
        with patch.object(O.shutil, 'which', return_value=None):
            self.check([{'name': 'Epistle'}, {'name': 'Gospel'}])
            with self.assertRaisesRegex(O.SourceError, 'runs backward'):
                self.check([{'name': 'Gospel'}, {'name': 'Epistle'}])
            with self.assertRaisesRegex(O.SourceError, 'has no Ordinary seat'):
                self.check([{'name': 'Unknown'}])
            with self.assertRaisesRegex(O.SourceError, 'node is not installed'):
                self.check(choice_rows())
        rows = choice_rows()
        for proper in [rows[2], rows[4]]:
            del proper['ordinary_disposition']['anchor']
        with self.assertRaisesRegex(O.SourceError, 'contiguous'):
            self.check(rows)
        rows = [{'name': 'Epistle', 'ordinary_disposition': {'kind': 'unplaced',
            'group': 'stale', 'region': 'before-frame', 'basis': 'Technical stale placement.'}}]
        with self.assertRaisesRegex(O.SourceError, 'stale because'):
            self.check(rows)


if __name__ == '__main__':
    unittest.main()
