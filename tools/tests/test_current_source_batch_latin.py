"""Current accepted body/permission partitions, separate from historical replay."""
import hashlib,json,sys,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];sys.path[:0]=[str(ROOT),str(ROOT/'scripts')]
import _calendars as C
from _proper_latin import LatinKey,SURFACES,body_owners,decision_for,publication_records,read_sidecar
from tools.tests import _source_batch_guards as G
# The finite qualified-rights adoption names the only bodies whose basis is not
# public-domain; every other new or corrected body keeps the public-domain basis.
QUALIFIED=json.loads((ROOT/'workflows/reviews/missal-reader-completion-2026-10-26/gregem-damasus-qualified-rights-adoption.json').read_text())
QUALIFIED_IDENTITIES={G.canonical({'course':'','cycle':'','form':'','mass':m,'occurrence':o,'proper':p})
 for m,f,p,c,o in(s['target']for s in QUALIFIED['exact_scopes'])if f=='main'and c=='all'}
HISTORICAL_FINITE_RAW=(ROOT/'workflows/reviews/missal-english-completion-2026-10-29/roman-1962/finite-latin-authority-v1.json').read_bytes()
if hashlib.sha256(HISTORICAL_FINITE_RAW).hexdigest()!='920299972ab84575183de8c84adcd3f7418bdc46304fbe1d6a4435fad1103ee3':raise AssertionError('exact original sixteen-scope authority')
HISTORICAL_FINITE=json.loads(HISTORICAL_FINITE_RAW)
FINITE_RAW=(ROOT/'workflows/reviews/missal-english-completion-2026-10-29/roman-1962/finite-latin-authority-v2.json').read_bytes()
if hashlib.sha256(FINITE_RAW).hexdigest()!='495e5b3672cccb8f2c3ea07398104c4b72026ffb7139de21d25087edcab1f48e':raise AssertionError('exact adopted twenty-two-scope authority')
FINITE_QUALIFIED=json.loads(FINITE_RAW)
QUALIFIED_IDENTITIES.update(G.key_string(LatinKey(*scope['key']))
 for scope in FINITE_QUALIFIED['scopes'])
RESTORED_IDENTITIES={G.key_string(LatinKey(m,'',p,'','',o)) for m,p,o in (
 ('s-antonii-padua-confessoris-ecclesiae-doctoris','Collect',1),
 ('comm-s-silvestri-i-papae-confessoris','Collect',1),
 ('palm-sunday','Procession Antiphon',5),
 ('palm-sunday','Procession Antiphon',6),
 ('easter-vigil','Blessing of the Lighted Candle',1),
 ('palm-sunday','Blessing of the Palms',1),
 ('good-friday','Improperia',1),
 ('good-friday','Antiphons at the Translation of the Blessed Sacrament',1))}
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
  # Anthony's prior restoration remains. The finite-sixteen adoption adds
  # Silvester; the two accepted Palm source reviews restore direct-Latin
  # ordinals5/6 (English target ordinals6/7 include an earlier Scripture node).
  # The separately adopted next seven restore four further removed
  # bundles above. Every other original removed owner keeps its refusal.
  restored=removed & corrected
  self.assertEqual(restored,RESTORED_IDENTITIES)
  for identity in removed-restored:
   key,body,state=self.bodies[identity];self.assertEqual(state,'removed');self.assertFalse(decision_for(key,'Invented body.',self.validated).permits(SURFACES))
 def test_every_explicit_new_or_corrected_body_has_current_six_surface_proof(self):
  self.assertEqual(len(HISTORICAL_FINITE['scopes']),16)
  current={tuple(s['key']):s for s in FINITE_QUALIFIED['scopes']}
  for scope in HISTORICAL_FINITE['scopes']:self.assertEqual(scope,current[tuple(scope['key'])])
  self.assertEqual(len(FINITE_QUALIFIED['scopes']),22)
  self.assertEqual(len(QUALIFIED_IDENTITIES),24)
  for identity in self.frozen['new_latin_keys']+self.frozen['corrected_latin_keys']:
   with self.subTest(identity=identity):
    key,body,state=self.bodies[identity];self.assertEqual(state,'present')
    self.assertEqual(G.digest(body),self.frozen['latin_current_bodies'][identity]['body_sha256'])
    row=self.validated[key]
    basis='qualified-nonoriginal-adaptation'if identity in QUALIFIED_IDENTITIES else'public-domain'
    self.assertEqual((row['provenance_status'],row['publication_status'],row['publication_basis']),('collated','permitted',basis))
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
     self.assertNotIn(identity,prior);restored.add(identity);continue
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
  # Each keeps its exact historical body under an accepted proof-only repair:
  # Calasanctius (latin-three-repair-adoption), the Seven Founders
  # (two-primary-source-method-adoption), Philip Neri, Josaphat and Cosmas and
  # Damian (their finite-source-methods records), Ignatius
  # (francis-one-ignatius-proof-adoption) and Damasus
  # (gregem-damasus-qualified-rights-adoption).
  self.assertEqual(proof_only,{'s-iosephi-calasanctii-confessoris','ss-septem-fundatorum-ordinis-servorum-beatae',
   's-philippi-nerii-confessoris','s-ignatii-episcopi-martyris','s-iosaphat-episcopi-martyris',
   's-damasi-i-papae-confessoris','ss-cosmae-damiani-martyrum'})
  self.assertEqual(restored,RESTORED_IDENTITIES)
if __name__=='__main__':unittest.main()
