"""Exact finite2 source relationships; no owner generator or canonical mutation."""
import copy
import ast
import hashlib
import importlib.machinery
import importlib.util
import json
from pathlib import Path
import re
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch
sys.dont_write_bytecode=True
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'scripts'))
import _name_execution as names

class FiniteNameExecution(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Installed use reads the appended namespace; the small fixture carries
        # only the two exact records and selected source/proof dictionaries.
        if (ROOT/'fixture-source-bindings.json').exists():
            data=json.loads((ROOT/'fixture-source-bindings.json').read_text());cls.records=json.loads((ROOT.parent/'records.json').read_text());cls.targets={tuple(r['target']):{k:v for k,v in r.items()if k!='target'}for r in data['targets']};cls.entries={tuple(r[k]for k in ['mass','form_id','proper','cycle','occurrence']):r for r in data['entries']};cls.proofs={(r['mass'],r['proper']):r for r in data['proofs']}
        else:
            import tomllib
            ledger=tomllib.loads((ROOT/'src/sources/inventories/roman-1962-proper-translations-v1.toml').read_text());cls.records=[json.loads(r['record_json'])for r in ledger['name_execution_sources']]
            loader=importlib.machinery.SourceFileLoader('_finite_name_owner',str(ROOT/'tools/mass-propers'));spec=importlib.util.spec_from_loader(loader.name,loader);owner=importlib.util.module_from_spec(spec);sys.modules[spec.name]=owner;loader.exec_module(owner);document=owner.load_calendar(ROOT/'src/sources/calendars','roman-1962');cls.entries={owner.translation_record_identity(r,document):r for r in ledger['entries']};cls.targets={}
            for _,mass in owner.masses_of(document):
                if mass['key']not in {r['target'][0]for r in cls.records}|{r['terminal_common'][0]for r in cls.records}:continue
                seen={}
                for form,proper,taken in owner.appointed_propers(document,mass):
                    form_id=owner.form_id_for_label(mass,form);identity=(form_id,proper['name']);seen[identity]=seen.get(identity,0)+1;cls.targets[(mass['key'],form_id,proper['name'],'all',seen[identity])]={'text':proper.get('text'),'taken_from':taken or None}
            proof=tomllib.loads((ROOT/'src/sources/inventories/roman-1962-proper-latin-provenance-v1.toml').read_text())['entries'];cls.proofs={(r['mass'],r['proper']):r for r in proof if r['occurrence']==1 and not r['form']and not r['cycle']}

    def test_exact_native_sources_and_distinct_Patrick_controller(self):
        self.assertEqual({tuple(r['target'])for r in self.records},names.TARGETS)
        for r in self.records:
            public=names.validate_native(r,self.targets,self.entries,self.proofs,ROOT)
            self.assertEqual(public['inference']['ordinary_admissions'],0)
            self.assertFalse(public['inference']['historically_named_English'])
            self.assertEqual(public['template']['text'],r['template_binding']['translations'][0]['text'])
            self.assertNotIn('actual_named_normative_Latin_private_transcription',public)
            if r['target'][0].startswith('s-patricii'):
                self.assertNotEqual(r['canonical_latin_sha256'],r['normative_named_controller']['whole_named_latin_sha256']);self.assertEqual(r['canonical_proof_owner'],'commune-confessoris-pontificis-1');self.assertIn('N.',self.targets[tuple(r['target'])]['text'])

    def test_closed_public_and_complete_record_authority(self):
        for r in self.records:
            original=names.public_projection(r)
            for field in ['private_normative_body','method_id','accepted_date','source_id','required_role','canonical_latin_sha256','named_normative_latin_sha256']:
                changed=copy.deepcopy(original);changed[field]='CHANGED'
                with self.subTest(field=field),self.assertRaises(ValueError):names.validate_public(changed,ROOT)
            for change in ['name','template','conclusion','normative','proof']:
                value=copy.deepcopy(r)
                if change=='name':value['name_controller']['text']+=' CHANGED'
                elif change=='template':value['template_text']=value['template_text'].replace('N.','Name')
                elif change=='conclusion':value['conclusion']['literal_english_cue']='Amen.'
                elif change=='normative':value['normative_named_controller']['whole_named_latin_sha256']='0'*64
                else:value['canonical_proof']['note']='DRIFT'
                with self.subTest(change=change),self.assertRaises(ValueError):names.validate_native(value,self.targets,self.entries,self.proofs,ROOT)

    def test_current_source_and_complete_proof_drift_refused(self):
        r=self.records[0]
        for kind in ['recipient','common','proof','binding']:
            targets=copy.deepcopy(self.targets);proofs=copy.deepcopy(self.proofs);entries=copy.deepcopy(self.entries)
            if kind=='recipient':targets[tuple(r['target'])]['text']+=' DRIFT'
            elif kind=='common':targets[tuple(r['terminal_common'])]['text']+=' DRIFT'
            elif kind=='proof':proofs[(r['canonical_proof_owner'],r['target'][2])]['note']='DRIFT'
            else:entries[tuple(r['terminal_common'])]['translations'][0]['text']+=' DRIFT'
            with self.subTest(kind=kind),self.assertRaises(ValueError):names.validate_native(r,targets,entries,proofs,ROOT)

    def test_placeholder_dot_and_non_ascii_controller_offsets(self):
        for r in self.records:
            text=r['template_text'];p=r['placeholder'];part=names.span(text,p,'N.');self.assertEqual(text[p['codepoint_range'][0]:p['codepoint_range'][1]],'N.');self.assertEqual(part['end']-part['start'],2)
            n=r['name_controller'];span=names.span(n['text'],n['span'],n['span']['literal']);self.assertEqual(n['text'].encode('utf-16-le')[span['start']*2:span['end']*2].decode('utf-16-le'),n['span']['literal'])
            bad=copy.deepcopy(p);bad['codepoint_range'][1]-=1
            with self.assertRaises(ValueError):names.span(text,bad,'N.')
        anth=next(r for r in self.records if r['target'][0]=='s-antonii-abbatis');text=anth['name_controller']['text'];a,b=anth['name_controller']['span']['codepoint_range'];self.assertNotEqual(len(text[:a].encode()),a);self.assertEqual(text[a:b],'Anthony')

    def test_actual_adapter_renderer_and_Study_without_generators(self):
        done=subprocess.run(['node',str(ROOT/'tools/tests/finite_name_execution.mjs'),str(ROOT)],capture_output=True,text=True);self.assertEqual(done.returncode,0,done.stderr);self.assertGreaterEqual(json.loads(done.stdout)['negative_controls'],28)

    def test_closed_read_transport_binds_both_separate_execution_coverages(self):
        # Execute the production transport function alone: no owner CLI or
        # release build, and no mocks of its exact source/catalog comparison.
        module=ast.parse((ROOT/'tools/public-alpha').read_bytes())
        function=next(n for n in module.body if isinstance(n,ast.FunctionDef) and n.name=='validate_propers_read_payload_sources')
        class ReleaseError(Exception): pass
        namespace={'Path':Path,'json':json,'hashlib':hashlib,'re':re,'ReleaseError':ReleaseError}
        exec(compile(ast.Module(body=[function],type_ignores=[]),'<actual public transport>','exec'),namespace)
        validate=namespace[function.name]
        scratch=ROOT/'.scratch';scratch.mkdir(exist_ok=True)
        with tempfile.TemporaryDirectory(prefix='finite-name-transport-',dir=scratch) as temporary:
            data=Path(temporary);proper=data/'structure/propers'
            def write(relative,value):
                p=proper/relative;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(value,sort_keys=True)+'\n');return p
            structure={'schema':'triptych-propers-structure/v1','calendar':'roman-1962','edition':'1962','edition_short':'1962','numbering':{},'translations':[],'languages':[],'coverage':{},'masses':[],
                'execution_source_coverage':{'schema':'triptych-execution-source-coverage/v1','language':'en','sources':6,'count_basis':'distinct-source-targets','whole_body_translations_added':0,'group_completeness':'context-dependent'},
                'name_execution_source_coverage':{'schema':'triptych-name-source-coverage/v1','sources':2,'historical_named_translations_added':0,'count_basis':'distinct-exact-recipient-occurrences'}}
            write('index.json',{'default':'roman-1962','missals':[{'id':'roman-1962','edition':'1962','edition_short':'1962','read_payload':{'catalog':'structure/propers/catalog/roman-1962.json','mass_prefix':'structure/propers/mass/roman-1962/'}}]})
            def bind(value):
                source=write('roman-1962.json',value)
                catalog={'schema':'triptych-propers-read-catalog/v1','calendar':'roman-1962','generation':hashlib.sha256(source.read_bytes()).hexdigest(),'structure':{k:v for k,v in value.items()if k!='masses'},'masses':[]}
                write('catalog/roman-1962.json',catalog);return catalog
            catalog=bind(structure);validate(data)
            for field in ['name_execution_source_coverage','execution_source_coverage']:
                bad=copy.deepcopy(catalog);bad['structure'][field]['sources']+=1;write('catalog/roman-1962.json',bad)
                with self.subTest(field=field),self.assertRaises(ReleaseError):validate(data)
            bad=copy.deepcopy(catalog);bad['structure'].pop('name_execution_source_coverage');write('catalog/roman-1962.json',bad)
            with self.assertRaises(ReleaseError):validate(data)
            bad=copy.deepcopy(structure);bad['unbound_execution_metadata']={};bind(bad)
            with self.assertRaises(ReleaseError):validate(data)

if __name__=='__main__':unittest.main()
