#!/usr/bin/python3
"""Admitted 1962 Office-Mass orations project once from exact source owners."""
import copy
from importlib.machinery import SourceFileLoader
from importlib.util import module_from_spec, spec_from_loader
import json
import os
from pathlib import Path
import subprocess
import unittest

import yaml

ROOT = Path(os.environ.get('TRIPTYCH_ORATION_TEST_ROOT', Path(__file__).resolve().parents[2]))
loader = SourceFileLoader('_oration_calendar_rubrics', str(ROOT / 'tools/calendar-rubrics'))
spec = spec_from_loader(loader.name, loader)
owner = module_from_spec(spec)
loader.exec_module(owner)


class CommemoratedOrations(unittest.TestCase):
    def test_reviewed_source_contract_is_exact_and_calendar_bounded(self):
        source = yaml.safe_load((ROOT / 'src/sources/calendars/roman-1962/rubrics.yaml').read_text())
        self.assertEqual(owner.check_oration_execution(source, 'fixture'), [])
        for mutate in [lambda s: s.update(calendar='roman-pre-1955'),
                       lambda s: s['orations']['execution'].update(scope='votive'),
                       lambda s: s['orations']['execution'].update(unknown=True),
                       lambda s: s['orations'].update(execution=None),
                       lambda s: s['orations']['execution']['conclusions'].update(principal=True),
                       lambda s: s['orations']['execution']['multiple_lessons'].update(commemorated_source='last-prayer')]:
            changed=copy.deepcopy(source);mutate(changed)
            self.assertTrue(owner.check_oration_execution(changed, 'fixture'))
        source['orations'].pop('execution')
        self.assertEqual(owner.check_oration_execution(source, 'fixture'), [])

    def test_source_projection_and_meaningful_negative_controls(self):
        done=subprocess.run(['node', str(ROOT / 'tools/tests/commemorated_orations.mjs'), str(ROOT)], capture_output=True, text=True)
        self.assertEqual(done.returncode, 0, done.stderr)
        self.assertGreaterEqual(json.loads(done.stdout)['checks'],20)

    def test_cli_retains_typed_shared_planner_refusal(self):
        loader=SourceFileLoader('_oration_mass_today', str(ROOT / 'tools/mass-today'))
        spec=spec_from_loader(loader.name,loader);today=module_from_spec(spec);loader.exec_module(today)
        source=json.loads((ROOT / 'src/web/data/structure/rubrics/roman-1962.json').read_text())
        execution={**source['orations']['execution'], 'slots': [{'slot':'Collect'},{'slot':'Secret'},{'slot':'Postcommunion'}]}
        with self.assertRaisesRegex(today.Refused, 'unsupported-oration-context'):
            today.mass_events(None, [], None, oration_context={'active':True,'calendar':'roman-pre-1955','execution':execution})

    def test_pre1955_does_not_inherit_1962_execution(self):
        source=yaml.safe_load((ROOT / 'src/sources/calendars/roman-pre-1955/rubrics.yaml').read_text())
        self.assertNotIn('execution', source['orations'])
        self.assertEqual(owner.check_oration_execution(source, 'fixture'), [])


if __name__ == '__main__':
    unittest.main()
