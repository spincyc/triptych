"""Current accepted body/permission partitions, separate from historical replay."""
import json,sys,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];sys.path[:0]=[str(ROOT),str(ROOT/'scripts')]
import _calendars as C
from _proper_latin import LatinKey,SURFACES,body_owners,decision_for,publication_records,read_sidecar
from tools.tests import _source_batch_guards as G
class CurrentSourceBatchLatinTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.frozen=G.fixture();cls.document=C.load_document(ROOT/'src/sources/calendars','roman-1962')
  cls.records,problems=read_sidecar(ROOT/G.LATIN_PATH)
  if problems:raise AssertionError(problems)
  cls.validated,problems=publication_records(ROOT/'src/sources/calendars','roman-1962')
  if problems:raise AssertionError(problems)
  cls.bodies={G.key_string(k):(k,b,state)for k,b,state in body_owners(cls.document)}
 def test_every_prior_body_and_disposition_is_exact_except_declared_repairs(self):
  G.assert_current_latin(self.records);G.assert_live_baseline_bodies(self.document)
  baseline=self.frozen['latin_baseline_bodies'];corrected=set(self.frozen['corrected_latin_keys'])
  self.assertEqual(set(self.bodies)-set(baseline),set(self.frozen['new_latin_keys']))
  for identity,want in baseline.items():
   if identity in corrected:continue
   with self.subTest(identity=identity):
    _,body,state=self.bodies[identity];self.assertEqual({'state':state,'body_sha256':G.digest(body)if body is not None else None},want)
  removed={identity for identity,v in baseline.items()if v['state']=='removed'}
  self.assertEqual(len(removed),20)
  # The accepted successor restores Anthony's previously removed Collect.
  # All other removed owners retain their original refusal contract.
  restored=removed & corrected
  self.assertEqual({json.loads(identity)['mass'] for identity in restored},
                   {'s-antonii-padua-confessoris-ecclesiae-doctoris'})
  for identity in removed-restored:
   key,body,state=self.bodies[identity];self.assertEqual(state,'removed');self.assertFalse(decision_for(key,'Invented body.',self.validated).permits(SURFACES))
 def test_every_explicit_new_or_corrected_body_has_current_six_surface_proof(self):
  for identity in self.frozen['new_latin_keys']+self.frozen['corrected_latin_keys']:
   with self.subTest(identity=identity):
    key,body,state=self.bodies[identity];self.assertEqual(state,'present')
    self.assertEqual(G.digest(body),self.frozen['latin_current_bodies'][identity]['body_sha256'])
    row=self.validated[key]
    self.assertEqual((row['provenance_status'],row['publication_status'],row['publication_basis']),('collated','permitted','public-domain'))
    self.assertEqual(set(row['surfaces']),set(SURFACES));self.assertTrue(decision_for(key,body,self.validated).permits(SURFACES))
    self.assertFalse(decision_for(key,body+'Amen.\n',self.validated).permits(SURFACES))
 def test_superseded_corrected_bodies_are_refused_by_actual_current_permissions(self):
  # Historical text is used only as the explicit negative control; all positive
  # bodies and publication records above come from the actual current corpus.
  historical=G.historical_document(self.document)
  prior={G.key_string(k):body for k,body,state in body_owners(historical)if state=='present'}
  proof_only=set();restored=set()
  for identity in self.frozen['corrected_latin_keys']:
   with self.subTest(identity=identity):
    key,current,state=self.bodies[identity]
    baseline=self.frozen['latin_baseline_bodies'][identity]
    if baseline['state']=='removed':
     self.assertNotIn(identity,prior);restored.add(json.loads(identity)['mass']);continue
    before=prior[identity]
    self.assertEqual(G.digest(before),baseline['body_sha256'])
    if before==current:
     # Joseph Calasanctius is an accepted evidence-chain repair. It leaves
     # the complete historical body exact and cannot make that body stale.
     proof_only.add(json.loads(identity)['mass'])
     self.assertNotEqual(self.frozen['latin_baseline_rows']['roman-1962'][identity],
                         self.frozen['latin_current_rows']['roman-1962'][identity])
     self.assertTrue(decision_for(key,before,self.validated).permits(SURFACES))
    else:
     denial=decision_for(key,before,self.validated);self.assertFalse(denial.permits(SURFACES));self.assertIn('stale text hash',denial.reason)
  self.assertEqual(proof_only,{'s-iosephi-calasanctii-confessoris'})
  self.assertEqual(restored,{'s-antonii-padua-confessoris-ecclesiae-doctoris'})
if __name__=='__main__':unittest.main()
