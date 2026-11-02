"""Finite source/execution metadata preserves whole prayers and existing holds."""
import copy
import importlib.machinery
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tomllib
import unittest
from unittest.mock import patch
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'scripts'))
import _oration_execution as execution

class OrationExecutionSources(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        loader = importlib.machinery.SourceFileLoader('_execution_source_owner', str(ROOT / 'tools/mass-propers'))
        spec = importlib.util.spec_from_loader(loader.name, loader)
        cls.owner = importlib.util.module_from_spec(spec); sys.modules[spec.name] = cls.owner; loader.exec_module(cls.owner)
        cls.calendar_root = ROOT / 'src/sources/calendars'
        cls.ledger_path = ROOT / 'src/sources/inventories/roman-1962-proper-translations-v1.toml'
        cls.ledger = tomllib.loads(cls.ledger_path.read_text())
        cls.sources = execution.load_sources(cls.calendar_root, 'roman-1962', cls.owner)

    def test_six_sources_keep_whole_body_holds(self):
        self.assertEqual(set(self.sources), execution.TARGETS)
        document = self.owner.load_calendar(self.calendar_root, 'roman-1962')
        entries = {self.owner.translation_record_identity(row, document): row for row in self.ledger['entries']}
        for native in self.ledger['execution_sources']:
            row = json.loads(native['record_json']); key = tuple(row['target'])
            self.assertNotIn(key, entries)
            self.assertTrue(any(a['mass'] == key[0] and a['proper'] == key[2] for a in self.ledger['untranslated']))
            self.assertEqual(row['source_binding']['translations'][0]['text'], self.sources[key]['source_text'])
            self.assertEqual(row['companion']['english_binding'], entries[tuple(row['companion']['target'])])
        self.assertEqual(execution.load_sources(self.calendar_root, 'roman-pre-1955', self.owner), {})

    def test_codepoint_utf8_utf16_are_distinct(self):
        text = 'Æ😀 petition. Cue.'; cuts = [0, len('Æ😀 petition.'), len('Æ😀 petition. '), len(text)]
        parts = [dict(kind=kind,start=cuts[i],end=cuts[i+1],utf8_start=len(text[:cuts[i]].encode()),utf8_end=len(text[:cuts[i+1]].encode())) for i,kind in enumerate(['petition','separator','printed-conclusion-cue'])]
        execution.validate_partition(text, parts, 'Cue.'); self.assertEqual(execution.utf16(text, 2), 3)
        for field,part in [('utf8_end',0),('start',1),('end',2),('kind',2)]:
            bad=copy.deepcopy(parts); bad[part][field] = 'rubric' if field=='kind' else bad[part][field]-1
            with self.assertRaises(ValueError): execution.validate_partition(text,bad,'Cue.')

    def test_closed_public_projection(self):
        original=next(iter(self.sources.values())); self.assertIs(execution.validate_public(original,ROOT),original)
        for field in ['source_text','source_id','source_sha256','target_proof_sha256','method_id','lang','private_locator']:
            bad=copy.deepcopy(original);bad[field]='CORRUPTED'
            with self.subTest(field=field),self.assertRaises(ValueError):execution.validate_public(bad,ROOT)
        for field in ['cue','family','proof_sha256','source_text']:
            bad=copy.deepcopy(original);bad['companion'][field]='CORRUPTED'
            with self.subTest(field=field),self.assertRaises(ValueError):execution.validate_public(bad,ROOT)

    def test_native_full_record_authority_is_closed(self):
        original_read=Path.read_text
        for change in ['drop','extra','empty','cue','source','host-proof','companion-proof','family','utf8','method','private']:
            rows=copy.deepcopy(self.ledger['execution_sources']);record=json.loads(rows[0]['record_json'])
            if change=='drop': rows.pop()
            elif change=='extra':rows.append(copy.deepcopy(rows[0]))
            elif change=='cue':record['source_binding']['translations'][0]['text']=record['source_binding']['translations'][0]['text'].removesuffix(record['source_english_cue'])
            elif change=='source':record['source_id']='edition.unproved'
            elif change=='host-proof':record['target_proof']['note']='DRIFT'
            elif change=='companion-proof':record['companion']['proof']['note']='DRIFT'
            elif change=='family':record['companion']['family']='wrong-person'
            elif change=='utf8':record['english_parts'][0]['utf8_end']-=1
            elif change=='method':rows[0]['method_id']='arbitrary-method'
            elif change=='private':record['private_field']='PRIVATE'
            if change not in ['drop','extra','empty','method']:rows[0]['record_json']=execution.canonical(record)
            payload=original_read(self.ledger_path).split('\n[[execution_sources]]',1)[0]+''.join('\n[[execution_sources]]\ntarget = '+json.dumps(r['target'])+'\nmethod_id = '+json.dumps(r['method_id'])+'\nrecord_json = '+json.dumps(r['record_json'],ensure_ascii=False)+'\n'for r in rows)
            if change=='empty':payload='execution_sources = []\n'+original_read(self.ledger_path).split('\n[[execution_sources]]',1)[0]
            def read(path,*args,**kwargs):return payload if path==self.ledger_path else original_read(path,*args,**kwargs)
            with self.subTest(change=change),patch.object(Path,'read_text',read),self.assertRaises(ValueError):execution.load_sources(self.calendar_root,'roman-1962',self.owner)

    def test_production_read_missal_renderer_and_refusals(self):
        done=subprocess.run(['node',str(ROOT/'tools/tests/oration_execution_source.mjs'),str(ROOT)],capture_output=True,text=True)
        self.assertEqual(done.returncode,0,done.stderr);self.assertGreaterEqual(json.loads(done.stdout)['rejected_controls'],28)

    def test_independent_public_release_gate(self):
        loader=importlib.machinery.SourceFileLoader('_execution_public_gate',str(ROOT/'tools/public-alpha'))
        spec=importlib.util.spec_from_loader(loader.name,loader);gate=importlib.util.module_from_spec(spec);sys.modules[spec.name]=gate;loader.exec_module(gate)
        payload=json.loads((ROOT/'src/web/data/structure/propers/roman-1962.json').read_text())
        virtual=ROOT/'src/web/data/structure/propers/execution-source-fixture.json'
        original_read=Path.read_text
        def check(value):
            def read(path,*args,**kwargs):return json.dumps(value,ensure_ascii=False)if path==virtual else original_read(path,*args,**kwargs)
            with patch.object(Path,'read_text',read):gate.validate_liturgical_public_data(virtual)
        check(payload)
        for change in ['private','wrong-owner','wrong-calendar','duplicate','source-text','coverage','private-coverage']:
            bad=copy.deepcopy(payload);mass=next(m for m in bad['masses']if any(p.get('execution_sources')for p in m['propers']));proper=next(p for p in mass['propers']if p.get('execution_sources'))
            if change=='private':proper['execution_sources'][0]['private_locator']='PRIVATE'
            elif change=='wrong-owner':mass['key']='unrelated-mass'
            elif change=='wrong-calendar':bad['calendar']='roman-pre-1955'
            elif change=='duplicate':mass['propers'].append(copy.deepcopy(proper))
            elif change=='source-text':proper['execution_sources'][0]['source_text']='CHANGED'
            elif change=='coverage':bad['execution_source_coverage']['whole_body_translations_added']=6
            elif change=='private-coverage':bad['execution_source_coverage']['private_field']='PRIVATE'
            with self.subTest(change=change),self.assertRaises(gate.ReleaseError):check(bad)
        catalog=json.loads((ROOT/'src/web/data/structure/propers/catalog/roman-1962.json').read_text())
        catalog_path=ROOT/'src/web/data/structure/propers/catalog/execution-source-fixture.json'
        def read_catalog(path,*args,**kwargs):return json.dumps(catalog,ensure_ascii=False)if path==catalog_path else original_read(path,*args,**kwargs)
        with patch.object(Path,'read_text',read_catalog):
            gate.validate_liturgical_public_data(catalog_path)
            catalog['structure']['execution_source_coverage']['private_locator']='PRIVATE'
            with self.assertRaises(gate.ReleaseError):gate.validate_liturgical_public_data(catalog_path)

if __name__=='__main__':unittest.main()
