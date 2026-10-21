"""Keep six printed named orations distinct from Common wording origins."""
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

loader = importlib.machinery.SourceFileLoader('_named_orations_propers', str(ROOT / 'tools/mass-propers'))
spec = importlib.util.spec_from_loader(loader.name, loader)
MP = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = MP
loader.exec_module(MP)

ANTHONY = 's-antonii-padua-confessoris-ecclesiae-doctoris'
BIBIANA = 's-bibianae-virginis-martyris'
SABBAS = 'comm-s-sabbae-abbatis'
# Facts independently read from the actual held page images. C/P describe the
# source classification; neither is a claim about the speaker or body rights.
EXPECTED = [
    (ANTHONY, 'Secret', 633, 552, 2777, 'P'),
    (ANTHONY, 'Postcommunion', 633, 552, 2778, 'P'),
    (BIBIANA, 'Secret', 511, 430, 1824, 'C'),
    (BIBIANA, 'Postcommunion', 511, 430, 1825, 'C'),
    (SABBAS, 'Secret', 514, 433, 1850, 'P'),
    (SABBAS, 'Postcommunion', 515, 434, 1851, 'P'),
]


class Roman1962NamedOrationAppointmentTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.source = yaml.safe_load((DATA_ROOT / 'src/sources/calendars/roman-1962/propers.yaml').read_text())
        cls.index = mass_index(cls.source)
        cls.evidence = tomllib.loads((DATA_ROOT / 'src/sources/inventories/roman-1962-named-oration-appointment-collation-v1.toml').read_text())

    def test_exact_named_orations_override_unspecialized_common_bodies(self):
        for key, name, _, _, number, _ in EXPECTED:
            with self.subTest(mass=key, proper=name):
                raw = [p for p in self.index[key]['propers'] if p['name'] == name]
                self.assertEqual(len(raw), 1)
                self.assertEqual(raw[0]['source'], 'composed')
                self.assertNotIn('takes_from', raw[0])
                self.assertIn(str(number), raw[0]['notes'])
                # Body collation may add words later without changing this
                # independent source appointment identity.
                if not raw[0].get('text'):
                    self.assertEqual(raw[0]['text_status']['state'], 'unavailable')
                    self.assertEqual(raw[0]['text_status']['scope'], 'proper-body')
                rows, problems = resolve_propers(self.source, self.index[key])
                self.assertEqual(problems, [])
                appointed = [(proper, origin) for _, proper, origin in rows if proper['name'] == name]
                self.assertEqual(len(appointed), 1)
                self.assertEqual(appointed[0], (raw[0], None))

    def test_appointment_evidence_keeps_the_exact_page_and_classification(self):
        rows = {(r['mass'], r['proper']): r for r in self.evidence['appointments']}
        self.assertEqual(len(rows), len(EXPECTED))
        self.assertEqual(self.evidence['artifact_sha256'], '648fdb8fe830ed65a08aa4a95de6f94424c533ddf2398c8fc26b18735fd3518a')
        for key, name, pdf, printed, number, marker in EXPECTED:
            with self.subTest(mass=key, proper=name):
                row = rows[(key, name)]
                self.assertEqual((row['pdf_page'], row['printed_page'], row['marginal_number']), (pdf, printed, number))
                self.assertEqual(row['source_classification'], marker)
                self.assertEqual(row['origin'], 'direct-named-appointment')
                self.assertEqual(len(row['raster_sha256']), 64)

    def test_anthony_routes_to_the_nonbishop_doctor_form_without_changing_collect(self):
        mass = self.index[ANTHONY]
        self.assertEqual(mass['takes_from']['mass'], 'commune-doctorum-non-pontificis')
        self.assertEqual(mass['takes_from']['citation'], 'Missa In medio, de Communi Doctorum [22], cum orationibus ut infra')
        rows, problems = resolve_propers(self.source, mass)
        self.assertEqual(problems, [])
        collect = next((p, origin) for _, p, origin in rows if p['name'] == 'Collect')
        self.assertEqual(collect, (mass['propers'][0], None))

    def test_cli_show_exposes_named_appointments_without_common_body_fallback(self):
        for key in (ANTHONY, BIBIANA, SABBAS):
            with self.subTest(mass=key):
                args = argparse.Namespace(root=str(ROOT / 'src/sources/calendars'), calendar='roman-1962',
                                          mass=key, lang='la', witness=None, bible=None,
                                          bible_root=str(ROOT / 'src/sources/bibles'))
                with patch.object(MP, 'load_calendar', return_value=self.source):
                    shown = MP.run_show_one(args)
                for name in ('Secret', 'Postcommunion'):
                    row = next(p for p in shown['appointed'] if p['name'] == name)
                    self.assertIsNone(row['taken_from'])
                    raw = next(p for p in self.index[key]['propers'] if p['name'] == name)
                    if not raw.get('text'):
                        self.assertFalse(row['proper'].get('text'))
                        self.assertEqual(row['proper']['text_status']['state'], 'unavailable')

    def test_removing_an_own_appointment_exposes_the_regression(self):
        for key, name, *_ in EXPECTED:
            with self.subTest(mass=key, proper=name):
                broken = copy.deepcopy(self.source)
                mass = mass_index(broken)[key]
                mass['propers'] = [p for p in mass['propers'] if p['name'] != name]
                rows, problems = resolve_propers(broken, mass)
                self.assertEqual(problems, [])
                fallback = next(origin for _, proper, origin in rows if proper['name'] == name)
                self.assertIsNotNone(fallback)


if __name__ == '__main__':
    unittest.main()
