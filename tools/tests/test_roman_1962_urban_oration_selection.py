"""Urban's printed II loco selector is independent of his own Collect."""
from __future__ import annotations

import argparse
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

loader = importlib.machinery.SourceFileLoader('_urban_selection_propers', str(ROOT / 'tools/mass-propers'))
spec = importlib.util.spec_from_loader(loader.name, loader)
MP = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = MP
loader.exec_module(MP)

KEY = 'comm-s-urbani-i-papae-martyris'
COMMON = 'commune-summorum-pontificum'


class Roman1962UrbanOrationSelectionTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.source = yaml.safe_load((DATA_ROOT / 'src/sources/calendars/roman-1962/propers.yaml').read_text())
        cls.mass = mass_index(cls.source)[KEY]
        cls.evidence = tomllib.loads((DATA_ROOT / 'src/sources/inventories/roman-1962-urban-oration-selection-v1.toml').read_text())

    def test_source_selects_second_papal_option_and_keeps_distinct_own_collect(self):
        self.assertEqual(self.mass['takes_from']['common_sets']['orations'], {'state': 'selected', 'option': 'c2-singular'})
        rows, problems = resolve_propers(self.source, self.mass)
        self.assertEqual(problems, [])
        orations = [(p, origin) for _, p, origin in rows if p['name'].split(' (')[0] in ('Collect', 'Secret', 'Postcommunion')]
        self.assertEqual([p['name'] for p, _ in orations], ['Collect', 'Secret (Altera secreta)', 'Postcommunion (Altera postcommunio)'])
        self.assertEqual(orations[0], (self.mass['propers'][0], None))
        self.assertEqual([origin['mass'] for _, origin in orations[1:]], [COMMON, COMMON])
        self.assertEqual([origin['proper'] for _, origin in orations[1:]], ['Secret (Altera secreta)', 'Postcommunion (Altera postcommunio)'])

    def test_evidence_preserves_directive_and_the_collect_wording_distinction(self):
        self.assertEqual(self.evidence['mass'], KEY)
        self.assertEqual((self.evidence['pdf_page'], self.evidence['printed_page'], self.evidence['marginal_number']), (616, 535, '2643A'))
        self.assertEqual(self.mass['takes_from']['citation'], self.evidence['literal_directive'])
        self.assertEqual(self.evidence['own_collect_marginal_number'], 2639)
        self.assertEqual(self.evidence['own_collect_distinct_word'], 'virtute')
        self.assertEqual(self.evidence['common_c2_collect_distinct_word'], 'veritate')
        self.assertEqual(self.evidence['artifact_sha256'], '648fdb8fe830ed65a08aa4a95de6f94424c533ddf2398c8fc26b18735fd3518a')

    def test_cli_payload_uses_c2_secret_post_but_local_collect(self):
        args = argparse.Namespace(root=str(ROOT / 'src/sources/calendars'), calendar='roman-1962',
                                  mass=KEY, lang='la', witness=None, bible=None,
                                  bible_root=str(ROOT / 'src/sources/bibles'))
        with patch.object(MP, 'load_calendar', return_value=self.source):
            shown = MP.run_show_one(args)
        rows = {row['name']: row for row in shown['appointed']}
        self.assertIsNone(rows['Collect']['taken_from'])
        for name in ('Secret (Altera secreta)', 'Postcommunion (Altera postcommunio)'):
            self.assertEqual(rows[name]['taken_from']['mass'], COMMON)
            self.assertEqual(rows[name]['taken_from']['proper'], name)
        self.assertNotIn('Secret', rows)
        self.assertNotIn('Postcommunion', rows)


if __name__ == '__main__':
    unittest.main()
