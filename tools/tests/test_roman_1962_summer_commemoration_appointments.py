"""Page-derived own orations and the referrals needed by July–September commemorations."""
from __future__ import annotations

import copy
import os
from pathlib import Path
import sys
import tomllib
import unittest

import yaml

ROOT = Path(os.environ.get('TRIPTYCH_REVIEW_ROOT', Path(__file__).resolve().parents[2]))
DATA_ROOT = Path(os.environ.get('TRIPTYCH_REFERRAL_DATA_ROOT', ROOT))
MODULE_ROOT = Path(os.environ.get('TRIPTYCH_APPOINTMENT_MODULE_ROOT', ROOT))
sys.path.insert(0, str(ROOT/'scripts'))
sys.path.insert(0, str(MODULE_ROOT/'scripts'))
from _calendars import mass_index, proper_family, resolve_propers

ANNA = 's-annae-matris-beatae-mariae-virginis'
EUPHEMIA = 'comm-ss-euphemiae-virginis-luciae-geminiani'
FELIX = 'comm-ss-felicis-simplicii-faustini-beatricis'
NICOMEDES = 'comm-s-nicomedis-martyris'
SABINA = 'comm-s-sabinae-martyris'
EUSEBIUS = 'comm-s-eusebii-confessoris'
PAUL = 's-pauli-primi-eremitae-confessoris'
EXPECTED = [
    (ANNA, 'Collect', 683, 602, 3175, 'unmarked'),
    (ANNA, 'Secret', 684, 603, 3181, 'unmarked'),
    (ANNA, 'Postcommunion', 684, 603, 3183, 'unmarked'),
    (EUPHEMIA, 'Collect', 740, 659, 3641, 'P'),
    (EUPHEMIA, 'Secret', 741, 660, 3643, 'P'),
    (EUPHEMIA, 'Postcommunion', 741, 660, 3644, 'P'),
    (FELIX, 'Secret', 687, 606, 3212, 'P'),
    (FELIX, 'Postcommunion', 687, 606, 3213, 'P'),
    (NICOMEDES, 'Secret', 739, 658, 3633, 'P'),
    (NICOMEDES, 'Postcommunion', 739, 658, 3634, 'P'),
    (SABINA, 'Secret', 724, 643, 3508, 'P'),
    (SABINA, 'Postcommunion', 724, 643, 3509, 'P'),
]
NAMES = ['Collect','Secret','Postcommunion']


class Roman1962SummerCommemorationAppointmentsTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.source = yaml.safe_load((DATA_ROOT/'src/sources/calendars/roman-1962/propers.yaml').read_text())
        cls.masses = mass_index(cls.source)
        cls.evidence = tomllib.loads((DATA_ROOT/'src/sources/inventories/roman-1962-summer-commemoration-appointment-collation-v1.toml').read_text())
        cls.english = tomllib.loads((DATA_ROOT/'src/sources/inventories/roman-1962-proper-translations-v1.toml').read_text())

    def test_own_source_units_stay_local_in_collect_secret_postcommunion_order(self):
        for key in {row[0] for row in EXPECTED}:
            with self.subTest(mass=key):
                rows, problems = resolve_propers(self.source,self.masses[key])
                self.assertEqual(problems,[])
                prayers = [(p,origin) for _,p,origin in rows if proper_family(p['name']) in NAMES]
                self.assertEqual([p['name'] for p,_ in prayers],NAMES)
                for _,name,_,_,unit,_ in [r for r in EXPECTED if r[0]==key]:
                    raw = [p for p in self.masses[key]['propers'] if p['name']==name]
                    self.assertEqual(len(raw),1)
                    self.assertEqual(raw[0]['source'],'composed')
                    self.assertNotIn('takes_from',raw[0])
                    self.assertIn(str(unit),raw[0]['notes'])
                    self.assertEqual(next((p,origin) for p,origin in prayers if p['name']==name),(raw[0],None))
                    if not raw[0].get('text'):
                        self.assertEqual(raw[0]['text_status']['state'],'unavailable')
                        self.assertEqual(raw[0]['text_status']['scope'],'proper-body')

    def test_evidence_retains_exact_pages_numbers_and_source_classification(self):
        facts = {(r['mass'],r['proper']):r for r in self.evidence['appointments']}
        self.assertEqual(set(facts),{(r[0],r[1]) for r in EXPECTED})
        self.assertEqual(len(facts),len(EXPECTED))
        self.assertEqual(self.evidence['artifact_sha256'],'648fdb8fe830ed65a08aa4a95de6f94424c533ddf2398c8fc26b18735fd3518a')
        for key,name,pdf,printed,unit,classification in EXPECTED:
            with self.subTest(mass=key,proper=name):
                row=facts[(key,name)]
                self.assertEqual((row['pdf_page'],row['printed_page'],row['marginal_number']),(pdf,printed,unit))
                self.assertEqual(row['source_classification'],classification)
                self.assertEqual(len(row['raster_sha256']),64)

    def test_missing_own_oration_cannot_pass_as_inherited_common_wording(self):
        for key,name,*_ in EXPECTED:
            with self.subTest(mass=key,proper=name):
                broken=copy.deepcopy(self.source)
                mass=mass_index(broken)[key]
                mass['propers']=[p for p in mass['propers'] if p['name']!=name]
                rows,problems=resolve_propers(broken,mass)
                self.assertEqual(problems,[])
                self.assertFalse(any(p['name']==name and origin is None for _,p,origin in rows))

    def test_eusebius_takes_pauls_secret_and_postcommunion_and_keeps_own_collect(self):
        mass=self.masses[EUSEBIUS]
        self.assertEqual(mass['takes_from']['mass'],PAUL)
        rows,problems=resolve_propers(self.source,mass)
        self.assertEqual(problems,[])
        prayers=[(p,origin) for _,p,origin in rows if proper_family(p['name']) in NAMES]
        self.assertEqual([p['name'] for p,_ in prayers],NAMES)
        self.assertEqual(prayers[0],(mass['propers'][0],None))
        self.assertEqual([origin['mass'] for _,origin in prayers[1:]],[PAUL,PAUL])
        self.assertEqual([origin['proper'] for _,origin in prayers[1:]],['Secret','Postcommunion'])
        referral=self.evidence['eusebius_referral']
        self.assertEqual((referral['pdf_page'],referral['printed_page'],referral['own_collect_marginal_number']),(707,626,3377))
        self.assertEqual(referral['target_printed_page'],443)
        self.assertEqual(referral['terminal_oration_marginal_numbers'],[1932,1935])

    def test_sabina_uses_source_proved_singular_set_and_retains_three_local_orations(self):
        mass=self.masses[SABINA]
        self.assertEqual(mass['takes_from']['common_sets']['orations'],{'state':'selected','option':'c1-singular'})
        rows,problems=resolve_propers(self.source,mass)
        self.assertEqual(problems,[])
        prayers=[(p,origin) for _,p,origin in rows if proper_family(p['name']) in NAMES]
        self.assertEqual([p['name'] for p,_ in prayers],NAMES)
        self.assertTrue(all(origin is None for _,origin in prayers))
        self.assertEqual(self.evidence['sabina_selection']['local_collect_marginal_number'],3507)
        self.assertEqual(self.evidence['sabina_selection']['common_collect_marginal_number'],4433)
        broken=copy.deepcopy(self.source)
        mass=mass_index(broken)[SABINA]
        mass['takes_from']['common_sets']['orations']={'state':'selected','option':'foreign-source-set'}
        self.assertTrue(resolve_propers(broken,mass)[1])

    def test_each_new_local_oration_has_one_exact_english_disposition(self):
        for key,name,*_ in EXPECTED:
            with self.subTest(mass=key,proper=name):
                identity=(key,'main',name,'all',1,'en')
                def same(row):
                    return tuple(row.get(field) for field in ['mass','form_id','proper','cycle','occurrence','lang'])==identity
                rows=[r for r in self.english['untranslated'] if same(r)]
                self.assertEqual(len(rows),1)
                self.assertEqual(rows[0]['reason'],{'kind':'no-exemplar'})
                self.assertEqual(rows[0]['extent'],'body')
                self.assertFalse(any(same(row) for row in self.english.get('entries',[])))


if __name__=='__main__':
    unittest.main()
