"""Bounded page-backed Common referral repairs; no completeness claim."""
from __future__ import annotations

import argparse
import copy
import importlib.machinery
import importlib.util
import os
from pathlib import Path
import sys
import tomllib
import unittest
from unittest.mock import patch

import yaml

ROOT = Path(os.environ.get('TRIPTYCH_REVIEW_ROOT', Path(__file__).resolve().parents[2]))
DATA_ROOT = Path(os.environ.get('TRIPTYCH_REFERRAL_DATA_ROOT', ROOT))
sys.path.insert(0, str(ROOT / 'scripts'))
from _calendars import mass_index, resolve_propers

loader = importlib.machinery.SourceFileLoader('_common_referral_propers', str(ROOT / 'tools/mass-propers'))
spec = importlib.util.spec_from_loader(loader.name, loader)
MP = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = MP
loader.exec_module(MP)

MASS = 's-thomae-villanova-episcopi-confessoris'
COMMON = 'commune-confessoris-pontificis-1'
DIRECTIVE = 'Missa Statuit, de Communi Confessoris Pontificis I loco [20], cum orationibus ut infra'


def spans(proper):
    return [(v['book'], r['begin']['chapter'], r['begin']['verse'],
             r['end']['chapter'], r['end']['verse'])
            for v in proper.get('verses', []) for r in v['ranges']]


class Roman1962CommonReferralFollowupTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.source = yaml.safe_load((DATA_ROOT / 'src/sources/calendars/roman-1962/propers.yaml').read_text())
        cls.mass = mass_index(cls.source)[MASS]
        cls.evidence = tomllib.loads((DATA_ROOT / 'src/sources/inventories/roman-1962-common-referral-collation-v1.toml').read_text())

    def test_thomas_keeps_the_printed_page_while_selecting_named_first_mass(self):
        self.assertEqual(self.mass['takes_from']['mass'], COMMON)
        self.assertEqual(self.mass['takes_from']['citation'], DIRECTIVE)
        rows = self.evidence['referrals']
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]['mass'], MASS)
        self.assertEqual(rows[0]['target_mass'], COMMON)
        self.assertEqual(rows[0]['literal_directive'], DIRECTIVE)
        self.assertEqual((rows[0]['pdf_page'], rows[0]['printed_page']), (746, 665))
        self.assertEqual(rows[0]['printed_common_page'], '[20]')
        self.assertEqual(self.evidence['artifact_sha256'], '648fdb8fe830ed65a08aa4a95de6f94424c533ddf2398c8fc26b18735fd3518a')

    def test_canonical_resolution_uses_statuit_and_preserves_own_collect(self):
        rows, problems = resolve_propers(self.source, self.mass)
        self.assertEqual(problems, [])
        by_name = {p['name']: (p, origin) for _, p, origin in rows}
        self.assertEqual(spans(by_name['Introit'][0]), [('Sirach', 45, 30, 45, 30), ('Psalms', 131, 1, 131, 1)])
        self.assertEqual(spans(by_name['Gospel'][0]), [('Matthew', 25, 14, 25, 23)])
        self.assertEqual(by_name['Gospel'][1]['mass'], COMMON)
        own = next(p for p in self.mass['propers'] if p['name'] == 'Collect')
        self.assertEqual(by_name['Collect'], (own, None))
        self.assertIn('no. 3690', own['notes'])

    def test_cli_show_carries_the_same_referral_without_changing_own_collect(self):
        args = argparse.Namespace(root=str(ROOT / 'src/sources/calendars'), calendar='roman-1962',
                                  mass=MASS, lang='la', witness=None, bible=None,
                                  bible_root=str(ROOT / 'src/sources/bibles'))
        # Exercise the actual CLI payload owner with real rights/translation
        # ledgers. Only the source load changes for scratch candidate review.
        with patch.object(MP, 'load_calendar', return_value=self.source):
            shown = MP.run_show_one(args)
        by_name = {p['name']: p for p in shown['appointed']}
        self.assertEqual(by_name['Gospel']['taken_from']['mass'], COMMON)
        self.assertEqual(spans(by_name['Gospel']['proper']), [('Matthew', 25, 14, 25, 23)])
        self.assertIsNone(by_name['Collect']['taken_from'])
        self.assertEqual(by_name['Collect']['proper']['text'], self.mass['propers'][0]['text'])

    def test_restoring_the_second_common_is_detected(self):
        broken = copy.deepcopy(self.source)
        mass = mass_index(broken)[MASS]
        mass['takes_from']['mass'] = 'commune-confessoris-pontificis-2'
        rows, problems = resolve_propers(broken, mass)
        self.assertEqual(problems, [])
        gospel = next(p for _, p, _ in rows if p['name'] == 'Gospel')
        self.assertNotEqual(spans(gospel), [('Matthew', 25, 14, 25, 23)])


if __name__ == '__main__':
    unittest.main()
