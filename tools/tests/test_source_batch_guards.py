"""Synthetic controls for exact source inputs and historical preservation replay."""
import copy,hashlib,json,tempfile,unittest
from pathlib import Path
from unittest import mock
import yaml
from tools.tests import _source_batch_guards as G
from tools.tests import test_roman_1962_octnov_commemoration_source_repair as L
class SourceBatchGuardTests(unittest.TestCase):
 def setUp(self):
  self.temp=tempfile.TemporaryDirectory();self.root=Path(self.temp.name);self.oldroot=G.ROOT;G.ROOT=self.root;G.fixture.cache_clear()
  self.before={G.YAML_PATH:b'value: before\n',G.LATIN_PATH:b'body = "before"\n'}
  self.after={G.YAML_PATH:b'value: after\n',G.LATIN_PATH:b'body = "after"\n'}
  files={};pins=[]
  for path,body in self.after.items():
   self.write(path,body);files[path]={'before_sha256':G.digest(self.before[path]),'after_sha256':G.digest(body),'hunks':[{'after_lines':[0,1],'after_slice_sha256':G.digest(body),'before_utf8':self.before[path].decode()}]};pins.append({'path':path,'post_sha256':G.digest(body)})
  self.manifest='tools/tests/fixtures/input-manifest.json';raw=json.dumps(pins).encode();self.write(self.manifest,raw)
  self.receipt='workflows/reviews/fixture/source-acceptance.json';receipt={'status':'accepted','scope':'missal-source-batch','source_input_manifest_sha256':G.digest(raw)};rr=json.dumps(receipt).encode();self.write(self.receipt,rr)
  self.data={'schema':'triptych-test-source-batch/v1','acceptance':{'status':'accepted','receipt_path':self.receipt,'receipt_sha256':G.digest(rr)},'source_input_manifest_path':self.manifest,'source_input_manifest_sha256':G.digest(raw),'files':files,'current_roman_document_sha256':G.digest(G.canonical({'value':'after'}))}
  self.save()
 def tearDown(self):G.ROOT=self.oldroot;G.fixture.cache_clear();self.temp.cleanup()
 def write(self,path,data):
  p=self.root/path;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(data)
 def save(self):
  self.write('tools/tests/fixtures/missal-source-batch-20261023.json',json.dumps(self.data).encode());G.fixture.cache_clear()
 def test_whole_current_inputs_replay_exact_historical_bytes(self):
  self.assertEqual(G.historical_bytes(G.YAML_PATH),self.before[G.YAML_PATH])
  self.assertEqual(G.historical_document({'value':'after'}),{'value':'before'})
 def test_pending_missing_and_valid_looking_wrong_receipts_refuse(self):
  original=copy.deepcopy(self.data)
  for change in ('pending','wrong-valid-hash','missing'):
   with self.subTest(change=change):
    self.data=copy.deepcopy(original)
    if change=='pending':self.data['acceptance']['status']='pending'
    elif change=='wrong-valid-hash':self.data['acceptance']['receipt_sha256']='a'*64
    else:self.data['acceptance']['receipt_path']='workflows/reviews/fixture/missing.json'
    self.save()
    with self.assertRaises(AssertionError):G.fixture()
 def test_valid_receipt_bytes_for_wrong_manifest_and_rejected_scope_refuse(self):
  for field,value in [('source_input_manifest_sha256','b'*64),('status','rejected'),('scope','other-source-batch')]:
   with self.subTest(field=field):
    receipt={'status':'accepted','scope':'missal-source-batch','source_input_manifest_sha256':self.data['source_input_manifest_sha256']};receipt[field]=value;raw=json.dumps(receipt).encode();self.write(self.receipt,raw);self.data['acceptance']['receipt_sha256']=G.digest(raw);self.save()
    with self.assertRaises(AssertionError):G.fixture()
 def test_wrong_manifest_bytes_and_replay_input_not_in_manifest_refuse(self):
  self.write(self.manifest,b'[]')
  with self.assertRaises(AssertionError):G.fixture()
  self.data['source_input_manifest_sha256']=G.digest(b'[]');receipt={'status':'accepted','scope':'missal-source-batch','source_input_manifest_sha256':G.digest(b'[]')};r=json.dumps(receipt).encode();self.write(self.receipt,r);self.data['acceptance']['receipt_sha256']=G.digest(r);self.save()
  with self.assertRaises(AssertionError):G.fixture()
 def test_non_source_replay_input_missing_from_manifest_refuses(self):
  path='tools/tests/legacy_guard.py';body=b'unchanged = True\n';self.write(path,body)
  self.data['files'][path]={'before_sha256':G.digest(body),'after_sha256':G.digest(body),'hunks':[]};self.save()
  with self.assertRaisesRegex(AssertionError,'every replay input belongs'):G.historical_bytes(path)
 def test_new_projection_edition_cannot_override_original_literal_oracle(self):
  self.data['new_projection_specs']={'original-edition':{'artifact_id':'new-artifact','publication_source_ids':[],'projected_from':[]}};self.save()
  original={'original-edition':{'artifact_id':'literal-old-artifact'}};prior=copy.deepcopy(original)
  with self.assertRaisesRegex(AssertionError,'cannot override historical literal'):G.add_projection_specs(original)
  self.assertEqual(original,prior)
 def test_projection_namespace_preserves_old_files_and_rejects_unlisted_paths(self):
  prefix='src/sources/works/triptych/roman-1962-latin-proper-editorial-projection/'
  old=prefix+'old.txt';new=prefix+'new.txt';self.write(old,b'old source\n');self.write(new,b'accepted new source\n')
  self.data['projection_baseline_source_files']={old:G.digest(b'old source\n')}
  pins=json.loads((self.root/self.manifest).read_bytes());pins.append({'path':new,'post_sha256':G.digest(b'accepted new source\n')})
  raw=json.dumps(pins).encode();self.write(self.manifest,raw);self.data['source_input_manifest_sha256']=G.digest(raw)
  receipt=json.dumps({'status':'accepted','scope':'missal-source-batch','source_input_manifest_sha256':G.digest(raw)}).encode();self.write(self.receipt,receipt);self.data['acceptance']['receipt_sha256']=G.digest(receipt);self.save()
  G.assert_current_projection_source_files()
  self.write(old,b'changed prior source\n')
  with self.assertRaisesRegex(AssertionError,'exact current project-projection source file'):G.assert_current_projection_source_files()
  self.write(old,b'old source\n');self.write(prefix+'unlisted.txt',b'unlisted\n')
  with self.assertRaisesRegex(AssertionError,'source-file identities'):G.assert_current_projection_source_files()
  (self.root/(prefix+'unlisted.txt')).unlink();(self.root/old).unlink()
  with self.assertRaisesRegex(AssertionError,'source-file identities'):G.assert_current_projection_source_files()
 def check_warm_and_cold_namespace_manifest_mutation(self,prefix,field,consumer):
  old=prefix+'historical.txt';new=prefix+'unreviewed.txt';body=b'prior historical source\n';self.write(old,body)
  self.data[field]={old:G.digest(body)}
  if field=='english_baseline_source_files':self.data['english_historical_source_files']={old:G.digest(body)}
  self.save();consumer()
  self.assertGreater(G.fixture.cache_info().currsize,0)
  original=(self.root/self.manifest).read_bytes();pins=json.loads(original)
  self.write(new,b'unreviewed source\n');pins.append({'path':new,'post_sha256':G.digest(b'unreviewed source\n')});self.write(self.manifest,json.dumps(pins).encode())
  with self.subTest(cache='warm'),self.assertRaisesRegex(AssertionError,'exact source input manifest bytes'):consumer()
  G.fixture.cache_clear()
  with self.subTest(cache='cold'),self.assertRaisesRegex(AssertionError,'exact source input manifest bytes'):consumer()
  self.write(self.manifest,original);(self.root/new).unlink();G.fixture.cache_clear();consumer()
 def test_projection_namespace_rejects_warm_and_cold_unreviewed_manifest_rows(self):
  self.check_warm_and_cold_namespace_manifest_mutation('src/sources/works/triptych/roman-1962-latin-proper-editorial-projection/','projection_baseline_source_files',G.assert_current_projection_source_files)
 def test_english_namespace_rejects_warm_and_cold_unreviewed_manifest_rows(self):
  self.check_warm_and_cold_namespace_manifest_mutation('src/sources/works/francis-xavier-lasance/','english_baseline_source_files',G.historical_english_source_files)
 def test_changed_or_missing_accepted_source_record_refuses_before_replay(self):
  self.write(G.LATIN_PATH,self.after[G.LATIN_PATH]+b'changed = true\n')
  with self.assertRaisesRegex(AssertionError,'entire accepted source input'):G.fixture()
  (self.root/G.LATIN_PATH).unlink();G.fixture.cache_clear()
  with self.assertRaisesRegex(AssertionError,'accepted source input missing'):G.fixture()
 def test_extra_whitespace_clause_and_in_memory_mutation_refuse_before_replay(self):
  for raw in (self.after[G.YAML_PATH]+b' ',self.after[G.YAML_PATH]+b'other: clause\n',self.before[G.YAML_PATH]):
   with self.subTest(raw=raw),self.assertRaises(AssertionError):G.historical_bytes(G.YAML_PATH,raw)
  with self.assertRaises(AssertionError):G.historical_document({'value':'changed'})
 def test_cross_supplement_is_exact_to_owner_source_array_and_editions(self):
  class Key:
   def __init__(self,mass):self.mass=mass
   def as_dict(self):return {'mass':self.mass,'proper':'Secret'}
  key=Key('one');extra='artifact.supplement';ids=['artifact.projection','artifact.primary',extra]
  self.data['cross_supplement_specs']={G.canonical([G.key_string(key),extra]):{'publication_source_ids':ids,'primary_artifact_id':'artifact.primary','primary_edition_id':'edition.first','supplement_artifact_id':extra,'supplement_edition_id':'edition.second'}};self.save()
  primary={'id':'artifact.primary','edition_id':'edition.first'};supplement={'id':extra,'edition_id':'edition.second'}
  self.assertTrue(G.explicit_cross_supplement(key,extra));self.assertFalse(G.explicit_cross_supplement(Key('other'),extra));self.assertFalse(G.explicit_cross_supplement(key,'artifact.other'))
  G.assert_explicit_cross_supplement(key,ids,extra,primary,supplement)
  with self.assertRaises(AssertionError):G.assert_explicit_cross_supplement(key,ids+['artifact.other'],extra,primary,supplement)
  with self.assertRaises(AssertionError):G.assert_explicit_cross_supplement(key,ids,extra,dict(primary,edition_id='edition.wrong'),supplement)
 def test_valid_stale_predecessors_refuse_before_private_legacy_steps(self):
  cases=[('phase5_predecessor_document','_phase5_predecessor_document_legacy',{'value':'before'}),('phase5_predecessor_yaml','_phase5_predecessor_yaml_legacy',self.before[G.YAML_PATH].decode()),('phase5_predecessor_ledger','_phase5_predecessor_ledger_legacy',self.before[G.LATIN_PATH].decode())]
  for public,private,value in cases:
   with self.subTest(public=public),mock.patch.object(L,private)as legacy:
    with self.assertRaises(AssertionError):getattr(L,public)(value)
    legacy.assert_not_called()
 def test_current_public_wrappers_enter_only_private_historical_steps(self):
  cases=[('phase5_predecessor_document','_phase5_predecessor_document_legacy',{'value':'after'},{'value':'before'}),('phase5_predecessor_yaml','_phase5_predecessor_yaml_legacy',self.after[G.YAML_PATH].decode(),self.before[G.YAML_PATH].decode()),('phase5_predecessor_ledger','_phase5_predecessor_ledger_legacy',self.after[G.LATIN_PATH].decode(),self.before[G.LATIN_PATH].decode())]
  for public,private,value,want in cases:
   with self.subTest(public=public),mock.patch.object(L,private,return_value='restored')as legacy:
    self.assertEqual(getattr(L,public)(value),'restored');legacy.assert_called_once_with(want)
if __name__=='__main__':unittest.main()
