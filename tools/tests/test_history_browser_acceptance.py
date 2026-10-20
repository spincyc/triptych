"""Input and evidence-preservation gates; these are not browser acceptance."""
import importlib.util
import json
from pathlib import Path
import subprocess
import tempfile
import unittest

ROOT=Path(__file__).resolve().parents[2]
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

if __name__=='__main__': unittest.main()
