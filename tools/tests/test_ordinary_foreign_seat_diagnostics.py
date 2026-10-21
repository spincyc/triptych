"""Closed static foreign-seat diagnostics cross the existing owner boundary."""
from __future__ import annotations

import copy
from importlib.machinery import SourceFileLoader
from importlib.util import module_from_spec, spec_from_loader
import json
import os
from pathlib import Path
import subprocess
import sys
import unittest
from unittest.mock import patch

ROOT = Path(os.environ.get('TRIPTYCH_REVIEW_ROOT', Path(__file__).resolve().parents[2]))
CODE = Path(os.environ.get('TRIPTYCH_FOREIGN_DIAGNOSTIC_ROOT', ROOT))
sys.path.insert(0, str(ROOT / 'scripts'))
loader = SourceFileLoader('_foreign_seat_diagnostic_ordinary', str(CODE / 'tools/mass-ordinary'))
spec = spec_from_loader(loader.name, loader)
O = module_from_spec(spec)
sys.modules[spec.name] = O
loader.exec_module(O)
O.SEATING_MODEL = ROOT / 'src/web/browser/liturgy/ordinary-seating.js'

BASE = {'kind': 'unsupported-foreign-source-applicability', 'sourceIndex': 0,
    'source_edition': 'roman-1962', 'target_edition': 'roman-pre-1955'}
TARGET = {'state': 'unknown', 'reason': 'not-declared-in-target-ordinary'}
FORMS = [{'mass': 'technical-foreign-form', 'form_id': 'main',
    'where': 'roman-pre-1955/technical-foreign-form/main', 'full': True,
    'propers': [{'name': 'Gospel (source-only qualifier)',
        'appointment_applicability': {'state': 'unresolved',
            'reason': 'foreign-source-applicability', 'source_edition': 'roman-1962',
            'target_edition': 'roman-pre-1955', 'basis': 'Technical owner transport fixture.'}}]}]


class ForeignSeatDiagnosticTransport(unittest.TestCase):
    def bridge(self, diagnostics):
        summary = {'candidates': 1, 'conditional_rows': 0, 'choice_groups': 0,
            'diagnostics': copy.deepcopy(diagnostics)}
        payload = [{'summary': summary}]
        result = subprocess.CompletedProcess(['node'], 0, json.dumps(payload), '')
        before = copy.deepcopy(FORMS)
        with patch.object(O.shutil, 'which', return_value='node'), patch.object(
            O.subprocess, 'run', return_value=result
        ) as run:
            accepted = O.check_appointment_seating({'calendar': 'roman-pre-1955'}, FORMS, {})
        self.assertEqual(run.call_count, 1)
        self.assertEqual(json.loads(run.call_args.kwargs['input'])['forms'], FORMS)
        self.assertEqual(FORMS, before)
        return accepted

    def test_existing_four_field_foreign_diagnostic_is_unchanged(self):
        result = self.bridge([BASE])
        self.assertEqual(result, [{'mass': 'technical-foreign-form', 'form_id': 'main',
            'candidates': 1, 'conditional_rows': 0, 'choice_groups': 0, 'diagnostics': [BASE]}])
        self.assertNotIn('target_seat', result[0]['diagnostics'][0])
        self.assertEqual(self.bridge([])[0]['diagnostics'], [])

    def test_exact_optional_unknown_target_seat_is_preserved(self):
        extended = {**BASE, 'target_seat': TARGET}
        result = self.bridge([extended, BASE])
        self.assertEqual(result[0]['diagnostics'], [extended, BASE])
        self.assertEqual(set(result[0]), {'mass', 'form_id', 'candidates',
            'conditional_rows', 'choice_groups', 'diagnostics'})
        self.assertNotIn('events', result[0])
        self.assertNotIn('seat', result[0])

    def test_optional_target_seat_rejects_malformed_shape_types_and_enums(self):
        malformed = [None, False, [], 'unknown', 0, {}, {'state': 'unknown'},
            {'reason': TARGET['reason']}, {**TARGET, 'ordinal': None},
            {**TARGET, 'state': 'known'}, {**TARGET, 'state': 'selected'},
            {**TARGET, 'state': None}, {**TARGET, 'reason': 'not-held'},
            {**TARGET, 'reason': None}, {**TARGET, 'reason': ['not-declared-in-target-ordinary']}]
        for target in malformed:
            with self.subTest(target=target), self.assertRaisesRegex(O.SourceError, 'malformed diagnostics'):
                self.bridge([{**BASE, 'target_seat': target}])

    def test_required_foreign_fields_and_existing_closed_enums_stay_required(self):
        malformed = []
        for field in BASE:
            item = {**BASE, 'target_seat': TARGET}; del item[field]; malformed.append(item)
        malformed += [{**BASE, 'target_seat': TARGET, 'extra': True},
            {**BASE, 'target_seat': TARGET, 'seat': None},
            {**BASE, 'target_seat': TARGET, 'kind': 'body-unavailable'},
            {**BASE, 'target_seat': TARGET, 'sourceIndex': -1},
            {**BASE, 'target_seat': TARGET, 'sourceIndex': True},
            {**BASE, 'target_seat': TARGET, 'sourceIndex': 0.5},
            {**BASE, 'target_seat': TARGET, 'source_edition': ''},
            {**BASE, 'target_seat': TARGET, 'target_edition': None},
            {'target_seat': TARGET}]
        for item in malformed:
            with self.subTest(item=item), self.assertRaisesRegex(O.SourceError, 'malformed diagnostics'):
                self.bridge([item])


if __name__ == '__main__':
    unittest.main()
