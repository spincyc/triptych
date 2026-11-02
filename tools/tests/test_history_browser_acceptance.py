"""Input and evidence-preservation gates; these are not browser acceptance."""
import importlib.util
from contextlib import contextmanager, redirect_stderr, redirect_stdout
import io
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from types import SimpleNamespace
from unittest.mock import patch

ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'scripts'))
spec=importlib.util.spec_from_file_location('history_acceptance',ROOT/'scripts/_history_browser_acceptance.py')
owner=importlib.util.module_from_spec(spec)
spec.loader.exec_module(owner)

class InputGates(unittest.TestCase):
    def fixture(self):
        catalogue={'entries':[{'id':'book'}],'presentation_groups':[],'native_texts':[],'comparisons':[],
                   'stage_history':{'stages':[],'transitions':[]}}
        raw=json.dumps(catalogue).encode()
        plan={'schema':owner.SCHEMA,'catalogue_sha256':owner.digest(raw),'entries':['book']}
        return catalogue,raw,plan

    def test_stale_catalogue_plan_rejected(self):
        catalogue,raw,plan=self.fixture()
        with self.assertRaisesRegex(ValueError,'digest'):
            owner.validate_plan(plan,catalogue,raw+b' ')

    def test_unknown_and_duplicate_targets_rejected(self):
        catalogue,raw,plan=self.fixture()
        for values in [['missing'],['book','book']]:
            with self.subTest(values=values),self.assertRaises(ValueError):
                owner.validate_plan(dict(plan,entries=values),catalogue,raw)

    def test_empty_plan_is_not_acceptance(self):
        catalogue,raw,plan=self.fixture()
        with self.assertRaisesRegex(ValueError,'select actual'):
            owner.validate_plan(dict(plan,entries=[]),catalogue,raw)

    def test_loopback_only_no_credentials(self):
        for url in ['https://example.test/history/','http://example.test/history/',
                    'http://user:secret@127.0.0.1/history/','http://127.0.0.1/other/']:
            with self.subTest(url=url),self.assertRaises(ValueError): owner.local_url(url)
        self.assertEqual(owner.local_url('http://127.0.0.1:0/history/').port,0)

    def test_existing_evidence_never_overwritten(self):
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory)
            out=root/'.scratch/review'
            out.mkdir(parents=True)
            evidence=out/'summary.json'
            evidence.write_text('prior evidence')
            with self.assertRaisesRegex(ValueError,'never overwritten'): owner.owned_output(root,out)
            self.assertEqual(evidence.read_text(),'prior evidence')

    def test_output_escape_and_symlink_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory)
            (root/'.scratch').mkdir()
            (root/'.scratch/alias').symlink_to(root/'.scratch',target_is_directory=True)
            for value in ['tracked-output','.scratch/../tracked-output','.scratch/alias/new']:
                with self.subTest(value=value),self.assertRaises(ValueError): owner.owned_output(root,value)

    def test_new_dedicated_scratch_output_allowed(self):
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory)
            self.assertEqual(owner.owned_output(root,'.scratch/review'),root/'.scratch/review')
            self.assertFalse((root/'.scratch/review').exists())

    def test_opening_one_native_preserves_existing_sibling_state(self):
        canon={'binding':'native-book:canon','open':True,'units':35}
        closed={'binding':'native-book:offertory','open':False,'units':0}
        opened={'binding':'native-book:offertory','open':True,'units':7}
        cases=[([canon,opened],True),
               ([dict(canon,open=False),opened],False),
               ([dict(canon,units=0),opened],False),
               ([canon,opened,{'binding':'native-book:extra','open':True,'units':1}],False)]
        for after,expected in cases:
            with self.subTest(after=after):
                self.assertEqual(owner.siblings_preserved([canon,closed],after,'native-book:offertory'),expected)

    def test_legacy_and_multi_descriptor_order(self):
        legacy={'text_binding':'native-book:old','text_projection_path':'native-texts/old.json'}
        self.assertEqual(owner.descriptors(legacy),[legacy])
        items=[{'text_binding':'native-book:offertory'},{'text_binding':'native-book:canon'}]
        self.assertEqual(owner.descriptors({'text_projections':items}),items)

    def test_cli_bad_url_does_not_create_output(self):
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory)
            process=subprocess.run([str(ROOT/'tools/history-browser-acceptance'),'--root',str(root),
                '--url','http://example.test/history/','--catalogue','missing.json','--plan','missing.json',
                '--out','.scratch/review','--json'],text=True,capture_output=True)
            self.assertEqual(process.returncode,2)
            self.assertEqual(json.loads(process.stderr)['code'],'invalid-input')
            self.assertEqual(process.stdout,'')
            self.assertFalse((root/'.scratch/review').exists())


class ProductSnapshotGates(unittest.TestCase):
    fixture=InputGates.fixture
    def setUp(self):
        scratch=ROOT/'.scratch/next-product-consumers'
        scratch.mkdir(parents=True,exist_ok=True)
        self.temporary=tempfile.TemporaryDirectory(dir=scratch)
        self.addCleanup(self.temporary.cleanup)
        self.root=Path(self.temporary.name)
        self.data=self.root/'private'
        target=self.data/'structure/act-history/catalogue.json'
        target.parent.mkdir(parents=True)
        self.catalogue,self.raw,plan=self.fixture()
        target.write_bytes(self.raw)
        (self.root/'plan.json').write_text(json.dumps(plan))
        self.events=[]
        self.active=False

    @contextmanager
    def products(self,root,*,product_ids):
        self.assertEqual(root,self.root)
        self.assertEqual(product_ids,['act-history'])
        self.active=True
        self.events.append('verify')
        try:
            yield SimpleNamespace(data_root=self.data)
        finally:
            self.assertEqual(self.events[-1],'close')
            self.active=False
            self.events.append('verified-exit')

    def browser(self,root,out,url,site,*,data_root):
        self.assertTrue(self.active)
        self.assertEqual(data_root,self.data)
        return SimpleNamespace(checks=[],
            start=lambda:self.events.append('start'),
            close=lambda:self.events.append('close'),
            save=lambda name,value:self.events.append('save:'+name))

    def exercise(self,browser,catalogue,raw,plan,source):
        self.assertTrue(self.active)
        self.assertEqual(source,self.data/'structure/act-history/catalogue.json')
        self.assertEqual(raw,self.raw)
        self.events.append('exercise')

    def run_main(self,*extra):
        stdout,stderr=io.StringIO(),io.StringIO()
        with redirect_stdout(stdout),redirect_stderr(stderr):
            status=owner.main(['--root',str(self.root),'--url','http://127.0.0.1:0/history/',
                '--plan','plan.json','--out','.scratch/review',*extra])
        return status,stdout.getvalue(),stderr.getvalue()

    def test_verified_snapshot_is_held_until_browser_shutdown(self):
        with (patch.object(owner,'verified_products',self.products),
              patch.object(owner,'Browser',side_effect=self.browser),
              patch.object(owner,'exercise',side_effect=self.exercise)):
            status,stdout,stderr=self.run_main()
        self.assertEqual(status,0,stderr)
        self.assertEqual(json.loads(stdout)['status'],'pass')
        self.assertEqual(self.events,['verify','start','exercise','close','verified-exit','save:summary'])
        self.assertFalse(self.active)

    def test_frozen_catalogue_must_match_verified_current_bytes(self):
        stale=self.root/'src/web/data/structure/act-history/catalogue.json'
        stale.parent.mkdir(parents=True)
        stale.write_bytes(self.raw+b' ')
        @contextmanager
        def products(*args,**kwargs):
            yield SimpleNamespace(data_root=self.data)
        with (patch.object(owner,'verified_products',products),patch.object(owner,'Browser') as browser):
            status,stdout,stderr=self.run_main('--catalogue',str(stale))
        self.assertEqual(status,2)
        self.assertEqual(stdout,'')
        self.assertIn('does not match verified current',json.loads(stderr)['error'])
        browser.assert_not_called()
        self.assertFalse((self.root/'.scratch/review').exists())

    def test_failed_verification_never_starts_a_browser(self):
        with (patch.object(owner,'verified_products',side_effect=ValueError('stale descriptor')),
              patch.object(owner,'Browser') as browser):
            status,stdout,stderr=self.run_main()
        self.assertEqual(status,2)
        self.assertEqual(stdout,'')
        self.assertIn('stale descriptor',json.loads(stderr)['error'])
        browser.assert_not_called()

    def test_final_verification_failure_cannot_emit_a_passing_summary(self):
        @contextmanager
        def changed(*args,**kwargs):
            with self.products(*args,**kwargs) as products:
                yield products
            raise ValueError('current inputs changed')
        with (patch.object(owner,'verified_products',changed),
              patch.object(owner,'Browser',side_effect=self.browser),
              patch.object(owner,'exercise',side_effect=self.exercise)):
            status,stdout,stderr=self.run_main()
        self.assertEqual(status,2)
        self.assertEqual(stdout,'')
        self.assertIn('current inputs changed',json.loads(stderr)['error'])
        self.assertNotIn('save:summary',self.events)
        self.assertEqual(self.events[-1],'save:failure')


class SourceOwnerPins(unittest.TestCase):
    def setUp(self):
        scratch=ROOT/'.scratch/next-product-consumers'
        scratch.mkdir(parents=True,exist_ok=True)
        self.temporary=tempfile.TemporaryDirectory(dir=scratch)
        self.addCleanup(self.temporary.cleanup)
        self.root=Path(self.temporary.name)
        self.path='src/sources/works/owner/book/editions/old/artifacts/page/page.jpg'
        self.raw=b'archived JPEG bytes'
        self.declaration={'path':self.path,'sha256':owner.digest(self.raw),'byte_size':len(self.raw)}
        archive='a'*64
        self.delivery={'schema':owner._artifact_store.SCHEMA,
            'archives':[{'id':archive,'name':'evidence.tar','sha256':archive,'bytes':1024,
                         'urls':['https://example.org/evidence.tar']}],
            'artifacts':[{'path':self.path,'sha256':self.declaration['sha256'],'bytes':len(self.raw),
                          'kind':'source-evidence','media_type':'image/jpeg','archive':archive,'member':self.path}]}
        self.index=self.root/owner._artifact_store.INDEX_PATH
        self.index.parent.mkdir(parents=True)
        self.index.write_text(json.dumps(self.delivery))

    def test_absent_archived_jpeg_uses_exact_declaration_without_reading_or_fetching_bytes(self):
        with (patch.object(owner._artifact_store,'resolve',side_effect=AssertionError('payload resolution forbidden')),
              patch.object(owner._artifact_store,'hydrate',side_effect=AssertionError('hydration forbidden'))):
            pin,=owner.source_owner_pins(self.root,[self.declaration])
        self.assertEqual(pin['sha256'],self.declaration['sha256'])
        self.assertEqual(pin['verification'],'external-declaration')
        self.assertIs(pin['witness_bytes_audited'],False)
        self.assertFalse((self.root/self.path).exists())

    def test_unknown_missing_owner_is_refused(self):
        declaration=dict(self.declaration,path=self.path.replace('page.jpg','unknown.jpg'))
        with self.assertRaisesRegex(ValueError,'not a known external artifact'):
            owner.source_owner_pins(self.root,[declaration])

    def test_wrong_declared_hash_or_size_is_refused(self):
        for changes in ({'sha256':'b'*64},{'byte_size':len(self.raw)+1}):
            with self.subTest(changes=changes),self.assertRaisesRegex(ValueError,'identity differs'):
                owner.source_owner_pins(self.root,[dict(self.declaration,**changes)])

    def test_metadata_changed_mid_run_is_refused_even_when_entry_and_mtime_stay_the_same(self):
        pins=owner.source_owner_pins(self.root,[self.declaration])
        before=self.index.stat()
        self.index.write_text(json.dumps(self.delivery)+' ')
        os.utime(self.index,ns=(before.st_atime_ns,before.st_mtime_ns))
        with self.assertRaisesRegex(ValueError,'metadata changed'):
            owner.source_owner_pins(self.root,[self.declaration],expected=pins)

    def test_plaintext_is_checked_from_actual_bytes_and_cannot_use_delivery_fallback(self):
        relative='src/owner.txt'
        target=self.root/relative
        target.write_bytes(b'canonical text')
        declaration={'path':relative,'sha256':owner.digest(target.read_bytes()),'byte_size':target.stat().st_size}
        pins=owner.source_owner_pins(self.root,[declaration])
        self.assertEqual(pins[0]['verification'],'file-bytes')
        target.write_bytes(b'changed text')
        with self.assertRaisesRegex(ValueError,'bytes or external delivery metadata changed'):
            owner.source_owner_pins(self.root,[declaration],expected=pins)
        target.unlink()
        with self.assertRaisesRegex(ValueError,'not a known external artifact'):
            owner.source_owner_pins(self.root,[declaration])

if __name__=='__main__': unittest.main()
