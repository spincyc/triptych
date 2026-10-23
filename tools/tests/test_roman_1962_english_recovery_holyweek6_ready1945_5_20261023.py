"""Independent source-family/person and bounded publication checks for the next strict/table batch."""
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
ARTIFACT='artifact.francis-xavier-lasance.the-new-roman-missal.benziger-revised-1945.resume-orations-holyweek6-ready1945-5-2026-10-23-5c171982'
ARTIFACT_SHA='5c1719825da5899dce3c500d4947c6f7c4a23d33938ab1c7f1c3932b0f18256b'
TABLE='artifact.francis-xavier-lasance.the-new-roman-missal.benziger-revised-1945.resume-orations-conclusion-table-2026-10-23-7dbb4a25'
TABLE_SHA='7dbb4a258065ce0ba7d6d203be9e2593637b1e98dd2c123ffac10355e1bbb934'
PREVIOUS_ENTRIES_SHA='e906be2ca9d8da0d371307d45a6b15caa43e2e8944f0c9098356437692be55ad'
ORACLES={('easter-vigil', 'main', 'Secret', 'all', 1): ['3e997b7e2f1d23e55d7c24ec9a9c681f9006070532892968df42dbac3084dc8a',
                                                'c7c74e3316775d206cb470614af0864ef8daa6af0c9b3c4a2540811a90a057f1',
                                                '86e96ba8522b4b129b2ff3fe93be866e6aeaa7129b7ba4d2e314d09438017b20',
                                                'strict',
                                                None],
 ('good-friday', 'main', 'Collect', 'all', 1): ['0d05d364d14f27d7864d5027a3c1f4ce2bcec034e9d0f26cdcdb8a8b02ad1533',
                                                'e1a2910a1983b30abf48cebdb378859c31c4caa892be893981e9fe96253d5f69',
                                                'b41ca1dc5237f45a94d260f75c28d4c486bb3e217301ba4e5453c9ddf929f4dd',
                                                'same-witness-conclusion-table',
                                                'who-with-thee'],
 ('mass-of-the-lords-supper', 'main', 'Collect', 'all', 1): ['ac12f72f3bf62d862e41a1a9d23711f3f892ecca396277f8bd550b2421bfb7cf',
                                                             '5c48a69bc7d35a238b547eb8174833cf4e78569038cd97f86821ae2d8e1caa59',
                                                             '2f62b0ce4b69a799be461f372f4d495565f5467fbb12114787991529035537e3',
                                                             'same-witness-conclusion-table',
                                                             'who-with-thee'],
 ('mass-of-the-lords-supper', 'main', 'Postcommunion', 'all', 1): ['a839e55cfef53ab69098ea103cb8da3c57783c39f8fa2be0b63af70d70494550',
                                                                   'ea05b7eace5e2093f6054be6b04c198711f9672e0c9f748dfa6c5ac87ad75f68',
                                                                   '04c4a3cec9affb3d51a89c0eb2e0a3e4115f33d6833421a9ea243d82f4cae4bc',
                                                                   'strict',
                                                                   None],
 ('mass-of-the-lords-supper', 'main', 'Secret', 'all', 1): ['3fbbff4b8eacffc9473def04e4d43f8eae5550e8a7f70a90d2c533e958bfebad',
                                                            '118c974703a1cada50a9691eea21855bb105aaf95dac26853a784ef8c66c0e6e',
                                                            'c2ce84f64b1612372e7efb26f7c250de00f555af31601bf34f7071e59ad2fdcd',
                                                            'same-witness-conclusion-table',
                                                            'who-with-thee']}

OWN_CONTEXT_ORACLES={}

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
  audit=tomllib.loads((ROOT/'src/sources/inventories/roman-1962-english-recovery-2026-10-23.toml').read_text());later={tuple(r['target'])for r in audit['accepted']if r.get('batch')not in ['core193', 'core39', 'phase1', 'phase2', 'phase3', 'holyweek6-ready1945-5', None]}
  previous=[r for r in ledger['entries']if self.p.translation_record_identity(r,self.doc)not in ORACLES and self.p.translation_record_identity(r,self.doc)not in later]
  self.assertEqual(len(previous),780);self.assertEqual(sha(q(sorted(previous,key=q))),PREVIOUS_ENTRIES_SHA)
  missing={self.p.translation_record_identity(r,self.doc)for r in ledger['untranslated']};self.assertFalse(missing&set(ORACLES))
  for k,r in self.entries.items():self.assertEqual(sha(self.slots[k]['text']),ORACLES[k][0]);self.assertEqual(sha(r['translations'][0]['text']),ORACLES[k][1])
 def test_every_complete_petition_and_actual_conclusion_person(self):
  for k,entry in self.entries.items():
   with self.subTest(target=k):
    passage=self.records[entry['passage_id']];marker=next(m for m in ['Historical Latin comparison transcription: ','Historical Latin transcription, layout and stress accents normalized for comparison: ']if m in passage['notes']);historical=passage['notes'].split(marker,1)[1].split(' Complete checked English SHA256 ',1)[0]
    self.assertEqual(sha(historical),ORACLES[k][2]);target=self.slots[k]['text']
    if ORACLES[k][3]=='strict':self.assertEqual(words(historical),words(target));continue
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
 def test_source_verification_retains_exact_target_and_own_context(self):
  latin=tomllib.loads((ROOT/'src/sources/inventories/roman-1962-proper-latin-provenance-v1.toml').read_text())['entries']
  for k,r in self.entries.items():
   with self.subTest(target=k):
    source=self.records[r['passage_id']];self.assertIn('Complete seed canonical Latin SHA256 '+ORACLES[k][0],source['notes'])
    m=next(m for _,m in self.p.masses_of(self.doc)if m['key']==k[0]);matches=[v for v in latin if v['mass']==k[0]and v['proper']==k[2]and v['occurrence']==k[4]and(v['cycle']or'all')==k[3]and self.p.form_id_for_label(m,v['form'])==k[1]];self.assertEqual(len(matches),1)
    self.assertIn('Existing target Latin verification '+matches[0]['verification_source_id']+' retained',source['notes'])
    if k in OWN_CONTEXT_ORACLES:self.assertIn(OWN_CONTEXT_ORACLES[k],source['context'])

if __name__=='__main__':unittest.main()
