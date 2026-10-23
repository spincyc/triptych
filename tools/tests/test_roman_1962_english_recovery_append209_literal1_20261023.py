"""Independent source-family/person and bounded publication checks for separately reviewed complete-canonical-Latin donor reuse."""
from pathlib import Path
from importlib.machinery import SourceFileLoader
from importlib.util import spec_from_loader, module_from_spec
import copy,hashlib,json,re,sys,tomllib,unicodedata,unittest
ROOT=Path(__file__).resolve().parents[2]
CAL=ROOT/"src/sources/calendars"
LEDGER=ROOT/"src/sources/inventories/roman-1962-proper-translations-v1.toml"
def sha(v):return hashlib.sha256(v.encode()if isinstance(v,str)else v).hexdigest()
def q(v):return json.dumps(v,ensure_ascii=False)
def words(v):
 v=v.casefold().replace('æ','ae').replace('œ','oe')
 return re.findall('[a-z]+|[0-9]+',''.join(c for c in unicodedata.normalize('NFKD',v)if not unicodedata.combining(c)))
ARTIFACT='artifact.francis-xavier-lasance.the-new-roman-missal.benziger-revised-1945.resume-orations-append209-literal1-2026-10-23-3a887a70'
ARTIFACT_SHA='3a887a7080bea779031cf4b3cdcfa1c821723c5cd3947a2054fe073af7a6e26a'
TABLE='artifact.francis-xavier-lasance.the-new-roman-missal.benziger-revised-1945.resume-orations-conclusion-table-2026-10-23-7dbb4a25'
TABLE_SHA='7dbb4a258065ce0ba7d6d203be9e2593637b1e98dd2c123ffac10355e1bbb934'
PREVIOUS_ENTRIES_SHA='f9d48fd89cf9f4309a4cb4bd52a7b03e2f9016507e6bccc0a305a2dd35f5859d'
ORACLES={('lent-4', 'main', 'Secret', 'all', 1): ['89916ae5b717e6e8714e403b139644ada06913f7a75cac818e3072e593a39465',
                                          'b0397ec803867f0dbfc0584ced59f74fb0eb577503f480efa499dd8096968d2f',
                                          'fc903f1f242e93c738d5aa810b16bd1e679fdfdf2e60dead64d4dd716c8d8524',
                                          'complete-canonical-latin-literal-reuse',
                                          'through-our-lord']}

LITERAL_REUSE={('lent-4', 'main', 'Secret', 'all', 1): {'donor': ['thursday-after-ash-wednesday', 'main', 'Secret', 'all', 1],
                                          'subroute': 'same-witness-conclusion-table'}}

class EnglishRecoveryNextStrictTableTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  l=SourceFileLoader('english_next_strict_table_propers',str(ROOT/'tools/mass-propers'));s=spec_from_loader(l.name,l);cls.p=module_from_spec(s);sys.modules[s.name]=cls.p;l.exec_module(cls.p)
  cls.doc=cls.p.load_calendar(CAL,'roman-1962');cls.overlay,cls.absent,cls.stale,cls.witnesses=cls.p.translation_overlay('roman-1962',CAL);cls.records,cls.trouble=cls.p._source_library_records(CAL)
  cls.entries={k:r for k,r in cls.overlay.items()if r.get('publication_artifact_id')==ARTIFACT};cls.slots={}
  for _,m in cls.p.masses_of(cls.doc):
   for f,b,taken in cls.p.appointed_propers(cls.doc,m):
    owner=cls.p.source_slot_identity(cls.doc,m,f,b,taken)
    for k,body in cls.p.coverage_slot_units(b,owner):cls.slots[k]=body
  cls.table=json.loads((ROOT/cls.records[TABLE]['path']).read_text());cls.families={r['key']:r for r in cls.table['formulas']}
 def split(self,text):
  tokens=words(text);found=[]
  for family,r in self.families.items():
   full=words(r['full_latin'])
   for n in range(len(tokens)-1):
    tail=tokens[n:]
    if(len(tail)>=2 and tail==full[:len(tail)])or tail==full+['r','amen']:found.append((n,family,tokens[:n],tail))
  if not found:return None
  first=min(x[0]for x in found);best=[r for r in found if r[0]==first];self.assertEqual(len(best),1);return best[0]
 def test_exact_new_owner_set_and_preserved_previous_entries(self):
  self.assertFalse(self.stale);self.assertFalse(self.trouble);self.assertEqual(set(self.entries),set(ORACLES));ledger=tomllib.loads(LEDGER.read_text())
  audit=tomllib.loads((ROOT/'src/sources/inventories/roman-1962-english-recovery-2026-10-23.toml').read_text());later={tuple(r['target'])for r in audit['accepted']if r.get('batch')not in ['append209-strict165', 'phase1', 'phase2', 'phase3', 'append209-literal1', None]}
  previous=[r for r in ledger['entries']if self.p.translation_record_identity(r,self.doc)not in ORACLES and self.p.translation_record_identity(r,self.doc)not in later]
  self.assertEqual(len(previous),713);self.assertEqual(sha(q(sorted(previous,key=q))),PREVIOUS_ENTRIES_SHA)
  missing={self.p.translation_record_identity(r,self.doc)for r in ledger['untranslated']};self.assertFalse(missing&set(ORACLES))
  for k,r in self.entries.items():self.assertEqual(sha(self.slots[k]['text']),ORACLES[k][0]);self.assertEqual(sha(r['translations'][0]['text']),ORACLES[k][1])
 def test_every_complete_petition_and_actual_conclusion_person(self):
  for k,entry in self.entries.items():
   with self.subTest(target=k):
    passage=self.records[entry['passage_id']];marker=next(m for m in ['Historical Latin comparison transcription: ','Historical Latin transcription, layout and stress accents normalized for comparison: ']if m in passage['notes']);historical=passage['notes'].split(marker,1)[1].split(' Complete checked English SHA256 ',1)[0]
    self.assertEqual(sha(historical),ORACLES[k][2]);target=self.slots[k]['text']
    donor=tuple(LITERAL_REUSE[k]['donor']);self.assertEqual(self.slots[donor]['text'],target);self.assertEqual(self.overlay[donor]['translations'][0]['text'],self.overlay[k]['translations'][0]['text'])
    if LITERAL_REUSE[k]['subroute']=='strict':self.assertEqual(words(historical),words(target));continue
    h=self.split(historical);t=self.split(target);self.assertIsNotNone(h);self.assertIsNotNone(t);self.assertEqual((h[1],h[2]),(t[1],t[2]));self.assertEqual(h[1],ORACLES[k][4]);self.assertIn('resume-orations-conclusion-table-2026-10-23-transcription',entry['witness_note'])
    self.assertNotEqual(h[2],words('est ')+t[2]);wrong=self.split(re.sub(r'\bper dominum\b','per eumdem dominum',' '.join(words(target)),count=1))
    if t[1]=='through-our-lord':self.assertTrue(wrong is None or wrong[1]!='through-our-lord')
    family=self.families[h[1]];actual=words(entry['translations'][0]['text']);short=words(family['short_english']);full=words(family['full_english'])
    self.assertTrue(any(actual[-n:]==full[:n]for n in range(2,len(full)+1))or actual[-len(short):]==short)
 def test_exact_table_source_and_five_distinct_families(self):
  record=self.records[TABLE];self.assertEqual(record['sha256'],TABLE_SHA);self.assertEqual(sha((ROOT/record['path']).read_bytes()),TABLE_SHA);self.assertEqual(record['derived_from'],self.table['source_artifact_id'])
  self.assertEqual((self.table['pdf_page'],self.table['printed_page']),(818,'819'));self.assertEqual(len(self.families),5)
  self.assertIn('eumdem',words(self.families['through-the-same']['full_latin']));self.assertNotIn('eundem',words(self.families['through-the-same']['full_latin']))
  self.assertEqual(self.split('Petition. Qui tecum.')[1],'who-with-thee');self.assertEqual(self.split('Petition. Qui vivis.')[1],'who-livest')
  self.assertEqual(self.split('Petition. Per eumdem Dominum.')[1],'through-the-same');self.assertEqual(self.split('Petition. Per Dominum.')[1],'through-our-lord')
 def test_every_new_latin_body_keeps_its_independent_public_proof(self):
  latin=tomllib.loads((ROOT/'src/sources/inventories/roman-1962-proper-latin-provenance-v1.toml').read_text())['entries']
  for k,r in self.entries.items():
   m=next(m for _,m in self.p.masses_of(self.doc)if m['key']==k[0]);matches=[v for v in latin if v['mass']==k[0]and v['proper']==k[2]and v['occurrence']==k[4]and(v['cycle']or'all')==k[3]and self.p.form_id_for_label(m,v['form'])==k[1]]
   self.assertEqual(len(matches),1);proof=matches[0];self.assertEqual(proof['text_sha256'],ORACLES[k][0]);self.assertEqual((proof['provenance_status'],proof['publication_status'],proof['publication_basis']),('collated','permitted','public-domain'));self.assertIn(proof['verification_source_id'],r['witness_note'])
 def test_exact_publication_bytes_and_negative_english_control(self):
  art=self.records[ARTIFACT];self.assertEqual(art['sha256'],ARTIFACT_SHA);self.assertEqual(sha((ROOT/art['path']).read_bytes()),ARTIFACT_SHA)
  for k,r in self.entries.items():
   self.p.validate_translation_publication_binding(r,CAL,LEDGER,self.witnesses);changed=copy.deepcopy(r);changed['translations'][0]['text']+=' Amen.'
   with self.assertRaisesRegex(ValueError,'translation body differs from its exact publication passage'):self.p.validate_translation_publication_binding(changed,CAL,LEDGER,self.witnesses)
if __name__=='__main__':unittest.main()
