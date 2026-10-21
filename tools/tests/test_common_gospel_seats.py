"""The three source-held Common Gospel alternatives have exact seats."""
import copy
from importlib.machinery import SourceFileLoader
from importlib.util import module_from_spec, spec_from_loader
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tomllib
import unittest

ROOT = Path(os.environ.get('TRIPTYCH_REVIEW_ROOT', Path(__file__).resolve().parents[2]))
SOURCE_ROOT = Path(os.environ.get('TRIPTYCH_COMMON_SOURCE_ROOT', ROOT))
ORDINARY_ROOT = Path(os.environ.get('TRIPTYCH_COMMON_ORDINARY_SOURCE_ROOT', ROOT))
SEATING = Path(os.environ.get('TRIPTYCH_APPOINTMENT_SEATING', ROOT / 'src/web/browser/liturgy/ordinary-seating.js'))
sys.path.insert(0, str(ROOT / 'scripts'))
import _calendars as C
loader = SourceFileLoader('_common_gospel_ordinary', str(ROOT / 'tools/mass-ordinary'))
spec = spec_from_loader(loader.name, loader)
O = module_from_spec(spec)
sys.modules[spec.name] = O
loader.exec_module(O)
LABELS = {
    'Gospel (alterum in Communi plurimorum Martyrum)',
    'Gospel (alterum in Communi Martyrum tempore paschali)',
    'Gospel (alterum)',
}


class CommonGospelSeats(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.source = C.read_yaml(SOURCE_ROOT / 'src/sources/calendars/roman-1962/propers.yaml')
        cls.inventory = tomllib.loads((ORDINARY_ROOT / 'src/sources/inventories/roman-1962-ordo-missae-v1.toml').read_text())
        cls.ordinary = json.loads((ROOT / 'src/web/data/structure/ordinary/roman-1962.json').read_text())
        cls.ordinary['slots'] = O.slot_table(cls.inventory, cls.ordinary['sections'], 'roman-1962')

    def test_each_exact_label_is_a_source_anchored_gospel_with_same_ordinary_seat(self):
        held = {p['name'] for m in self.source['sections']['common']['masses'] for p in m.get('propers', [])
            if p['name'] in LABELS and p.get('ordinary_disposition', {}).get('anchor', {}).get('proper') == 'Gospel'}
        self.assertEqual(held, LABELS)
        for name in LABELS:
            slot = self.ordinary['slots'][O.proper_slot(self.ordinary['slots'], name)]
            self.assertEqual(slot['key'], 'evangelium')
            self.assertFalse(slot['qualified'])
        self.assertEqual(O.proper_slot(self.ordinary['slots'], 'Gospel (unheld qualifier)'), -1)
        self.assertEqual(O.proper_slot(self.ordinary['slots'], 'Gospel (alterum in an unheld Common)'), -1)

    def test_runtime_alternatives_keep_exact_seats_and_cross_role_refusal(self):
        node = shutil.which('node')
        if node is None:
            self.skipTest('node is not installed')
        code = r"""const S=require(process.argv[1]);let t='';process.stdin.on('data',c=>t+=c);process.stdin.on('end',()=>{const x=JSON.parse(t),shown=x.ordinary.sections.flatMap(section=>section.elements.map(element=>({section,element}))),seating=S.seats(x.ordinary,shown),anchor={mass:'technical-common',form_id:'main',proper:'Gospel',occurrence:1};function check(name){const rows=['Gospel',name].map((name,index)=>({name,appointment_identity:{...anchor,proper:name},ordinary_disposition:{kind:'alternative',group:'technical-gospel',option:index?'other':'principal',basis:'Technical source seat fixture.',anchor}}));try{const u=S.properUnits(rows,seating);return{seat:u[0].seat.key,semantic:S.semanticProperId(rows[1],true)};}catch(e){return{error:e.message};}}process.stdout.write(JSON.stringify({held:x.labels.map(check),cross:check('Epistle'),unknown:check('Gospel (unheld qualifier)')}));});"""
        finished = subprocess.run([node, '-e', code, str(SEATING)], input=json.dumps({'ordinary': self.ordinary, 'labels': sorted(LABELS)}), text=True, capture_output=True, check=False, timeout=30)
        self.assertEqual(finished.returncode, 0, finished.stderr)
        result = json.loads(finished.stdout)
        self.assertEqual(result['held'], [{'seat': 'evangelium', 'semantic': 'gospel'}] * 3)
        self.assertIn('one established semantic seat', result['cross']['error'])
        self.assertIn('usable semantic Ordinary seat', result['unknown']['error'])


if __name__ == '__main__':
    unittest.main()
