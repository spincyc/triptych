"""Correlated membership composes with current selector and Common contracts."""
from __future__ import annotations
import argparse
import copy
import importlib.machinery
import importlib.util
import os
from pathlib import Path
import sys
import unittest
from unittest.mock import patch

ROOT=Path(os.environ.get('TRIPTYCH_REVIEW_ROOT',Path(__file__).resolve().parents[2]))
MODULE_ROOT=Path(os.environ.get('TRIPTYCH_SOURCE_PATH_CORE',ROOT))
PRODUCER_ROOT=Path(os.environ.get('TRIPTYCH_SOURCE_PATH_PRODUCER',MODULE_ROOT))
sys.path.insert(0,str(ROOT/'scripts'))
sys.path.insert(0,str(MODULE_ROOT/'scripts'))
import _calendars as C

def tool(name):
    loader=importlib.machinery.SourceFileLoader('_paths_after_usage_'+name.replace('-','_'),str(PRODUCER_ROOT/'tools'/name))
    spec=importlib.util.spec_from_loader(loader.name,loader)
    mod=importlib.util.module_from_spec(spec);sys.modules[spec.name]=mod;loader.exec_module(mod)
    for key,value in list(vars(mod).items()):
        if isinstance(value,Path) and value.is_relative_to(PRODUCER_ROOT):
            setattr(mod,key,ROOT/value.relative_to(PRODUCER_ROOT))
    mod.ROOT=ROOT
    return mod

MP=tool('mass-propers')
BASIS='Technical composition fixture; no historical or actual-use permission is asserted.'
CALENDAR='postconciliar'

def facts():
    return {
        'fixture-season':{'edition':CALENDAR,'values':['outside','paschal'],'basis':BASIS,'season_values':{'lent':'outside','triduum':None}},
        'fixture-mass':{'edition':CALENDAR,'values':['general','widow'],'basis':BASIS,'mass_values':{'fixture':{'value':'widow','basis':BASIS}}},
        'fixture-usage':{'edition':CALENDAR,'values':['chant-present','chant-omitted'],'basis':BASIS,'usage_values':{'own-sunday':'chant-present','borrowed-feria':'chant-omitted'}}}

def scripture():
    return {'name':'Gospel','source':'scripture','cycles':{cycle:{'verses':[{'book':'Matthew','ranges':[{'begin':{'chapter':1,'verse':1},'end':{'chapter':1,'verse':1}}],'ref':'Matthew 1:1'}]} for cycle in ['A','B','C']}}

def relation():
    return {'id':'fixture-course','form_id':'main','basis':BASIS,'paths':[
        {'id':'held-a','standing':'principal','calendar_cycles':{'family':'sunday','in':['A','B','C']},'choices':{},
         'when':{'fact':'fixture-actual-use','is':True},
         'members':[{'appointment':{'mass':'fixture','form_id':'main','proper':'Gospel','occurrence':1},'material_cycle':{'family':'cycles','cycle':'A'}}]}]}

def fixture():
    mass={'key':'fixture','name':'Technical composed source model','registry':'fixture','season':'lent','propers':[scripture()],'proper_source_paths':[relation()]}
    return {'calendar':CALENDAR,'edition':'Technical fixture','psalm_numbering':'hebrew','proper_appointment_facts':facts(),'sections':{'seasonal':{'kind':'seasonal','masses':[mass]}}},mass

def show(document,mass):
    args=argparse.Namespace(root=str(ROOT/'src/sources/calendars'),calendar=CALENDAR,mass=mass['key'],lang='la',witness=None,bible=None,bible_root=str(ROOT/'src/sources/bibles'),form=None)
    with patch.object(MP,'load_calendar',return_value=document),patch.object(MP,'translation_overlay',return_value=({}, {}, [], {})),patch.object(MP,'publication_records',return_value=({}, [])):
        return MP.run_show_one(args)

class ProperSourcePathsAfterUsageTests(unittest.TestCase):
    def test_three_fact_selectors_and_boolean_path_condition_transport_unchanged(self):
        document,mass=fixture();before=copy.deepcopy(document)
        self.assertIs(C.validate_proper_appointment_facts(document['proper_appointment_facts'],CALENDAR,document=document),document['proper_appointment_facts'])
        rows,problems=C.resolve_propers(document,mass,appointments=True)
        self.assertEqual(problems,[])
        public=C.public_proper_source_paths(document,mass)
        self.assertEqual(public[0]['paths'][0]['when'],{'fact':'fixture-actual-use','is':True})
        self.assertNotIn('fixture-actual-use',document['proper_appointment_facts'])
        payload=show(document,mass)
        self.assertEqual(payload['proper_appointment_facts'],document['proper_appointment_facts'])
        self.assertEqual(payload['mass']['proper_source_paths'],public)
        self.assertEqual(payload['appointed'][0]['proper']['source_path_relation'],'fixture-course')
        self.assertEqual(set(payload['appointed'][0]['proper']['cycles']),{'A','B','C'})
        self.assertEqual(rows[0][1]['appointment_identity'],{'mass':'fixture','form_id':'main','proper':'Gospel','occurrence':1})
        self.assertEqual(document,before)

    def test_bad_current_fact_selectors_refuse_before_path_publication(self):
        mutations=[lambda f:f['fixture-mass']['mass_values'].update(unheld={'value':'widow','basis':BASIS}),
            lambda f:f['fixture-usage']['usage_values'].update(default='chant-present'),
            lambda f:f['fixture-season']['season_values'].update(lent='unheld'),
            lambda f:f['fixture-mass'].update(usage_values={'own-sunday':'widow','borrowed-feria':'general'})]
        for mutate in mutations:
            document,mass=fixture();mutate(document['proper_appointment_facts'])
            with self.subTest(facts=document['proper_appointment_facts']):
                self.assertTrue(C.resolve_propers(document,mass)[1])
                with self.assertRaises(ValueError):C.public_proper_source_paths(document,mass)
                with patch.object(MP,'sanitize_mass',side_effect=AssertionError('publication reached malformed source facts')),self.assertRaises(ValueError):show(document,mass)

    def test_inactive_material_and_path_conditions_are_admitted_before_projection(self):
        for invalid in ['inactive-cycle','path-boolean']:
            document,mass=fixture()
            if invalid=='inactive-cycle':mass['propers'][0]['cycles']['C']['verses']=[]
            else:mass['proper_source_paths'][0]['paths'][0]['when']['is']='true'
            with self.subTest(invalid=invalid):
                self.assertTrue(C.resolve_propers(document,mass)[1])
                with self.assertRaises(ValueError):C.public_proper_source_paths(document,mass)
        document,mass=fixture()
        mass['proper_source_paths'][0]['paths'][0]['when']['is']=False
        rows,problems=C.resolve_propers(document,mass,appointments=True)
        self.assertEqual(problems,[])
        self.assertEqual(len(rows),1)
        self.assertEqual(C.public_proper_source_paths(document,mass)[0]['paths'][0]['when']['is'],False)

    def test_foreign_pure_path_multihop_keeps_origin_marker_and_raw_material_without_source_facts(self):
        document,mass=fixture();before=copy.deepcopy(document)
        middle=C._apply_departures({'calendar':'foreign-middle','sections':{}},document,CALENDAR)
        target=C._apply_departures({'calendar':'foreign-target','sections':{}},middle,'foreign-middle')
        self.assertNotIn('proper_appointment_facts',middle)
        self.assertNotIn('proper_appointment_facts',target)
        inherited=C.mass_index(target)['fixture']
        rows,problems=C.resolve_propers(target,inherited,appointments=True)
        self.assertEqual(problems,[])
        self.assertEqual(len(rows),1)
        proper=rows[0][1]
        self.assertNotIn('ordinary_disposition',proper)
        self.assertEqual(proper['cycles'],mass['propers'][0]['cycles'])
        self.assertEqual(proper['source_path_relation'],'fixture-course')
        self.assertEqual(proper['appointment_applicability']['source_edition'],CALENDAR)
        self.assertEqual(proper['appointment_applicability']['target_edition'],'foreign-target')
        self.assertEqual(C.public_proper_source_paths(target,inherited)[0]['source_edition'],CALENDAR)
        self.assertEqual(document,before)

    def test_complete_common_oration_override_still_allows_local_path_without_selecting_common_set(self):
        document,mass=fixture()
        families=['Collect','Secret','Postcommunion']
        common={'key':'fixture-common','name':'Technical Common','registry':'fixture-common','common_sets':{'orations':{'families':families,'options':{'first':families,'second':[name+' (altera)' for name in families]}}},
            'propers':[{'name':name+suffix,'source':'composed','text':'Technical inherited '+name+suffix} for name in families for suffix in ['', ' (altera)']]}
        document['sections']['common']={'kind':'common','masses':[common]}
        mass['takes_from']={'mass':'fixture-common'}
        mass['propers']=[{'name':name,'source':'composed','text':'Technical local '+name} for name in families]+mass['propers']
        rows,problems=C.resolve_propers(document,mass,appointments=True)
        self.assertEqual(problems,[])
        self.assertEqual([p['name'] for _,p,_ in rows],families+['Gospel'])
        self.assertEqual(C.public_proper_source_paths(document,mass)[0]['source_edition'],CALENDAR)
        self.assertTrue(all(owner is None for _,_,owner in rows))
        mass['takes_from']['common_sets']={}
        self.assertTrue(C.resolve_propers(document,mass)[1])

if __name__=='__main__':unittest.main()
