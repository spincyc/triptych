"""Page-collated normal temporal appointments; no whole-rite completeness claim."""
import copy,importlib.machinery,importlib.util,json,re,subprocess,sys,tomllib,unittest
from pathlib import Path
import yaml
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'scripts'))
from _calendars import resolve_propers, _public_appointment_proper
from tools.tests._source_recovery_assertions import assert_current_latin_body_or_gap
DATA=ROOT/'src/sources/calendars/roman-1962/propers.yaml'
RECORD=ROOT/'src/sources/inventories/roman-1962-chant-appointment-collation-v1.toml'
# Independent physical source coordinates and source-order anchors.
EXPECTED=[
 ('holy-wednesday','Oratio',882,228,147,'Gradual','Second Lesson'),
 ('holy-wednesday','Oratio super populum',890,232,151,'Postcommunion',None),
 ('easter-tuesday','Alleluia',1166,414,333,'Gradual','Sequence'),
 ('easter-thursday','Alleluia',1188,418,337,'Gradual','Sequence'),
 ('pentecost-ember-wednesday','Oratio',1344,443,362,'First Alleluia','Second Lesson'),
 ('pentecost-ember-wednesday','Second Alleluia',1346,443,362,'Second Lesson','Sequence'),
]
MIXED=[('vigil-of-the-ascension',1276,431,350),('pentecost-monday',1323,439,358),('pentecost-tuesday',1333,441,360),('pentecost-thursday',1356,445,364),('pentecost-ember-friday',1366,446,365)]
def mass_index(d):return {m['key']:m for s in d['sections'].values() for m in s['masses']}
def source_problems(d):
 problems=[];ms=mass_index(d)
 for key,name,*_ in EXPECTED:
  ps=[p for p in ms[key]['propers'] if p['name']==name]
  if len(ps)!=1 or ps[0].get('source')!='composed':problems.append((key,name))
 for key,*_ in MIXED:
  p=next(p for p in ms[key]['propers'] if p['name']=='Alleluia')
  if p.get('source')!='mixed' or not p.get('verses'):problems.append((key,'Alleluia'))
 return problems
class EasterNormalAppointments(unittest.TestCase):
 @classmethod
 def setUpClass(c):
  c.doc=yaml.safe_load(DATA.read_text());c.ms=mass_index(c.doc);c.record=tomllib.loads(RECORD.read_text())
 def test_direct_units_keep_exact_source_order_and_reviewed_body_states(self):
  self.assertEqual(source_problems(self.doc),[])
  for key,name,_,_,_,prior,following in EXPECTED:
   ps=self.ms[key]['propers'];ix=next(i for i,p in enumerate(ps) if p['name']==name)
   self.assertEqual(ps[ix-1]['name'],prior)
   self.assertEqual(ps[ix+1]['name'] if ix+1<len(ps) else None,following)
   assert_current_latin_body_or_gap(self,key,name,ps[ix]);self.assertNotIn('verses',ps[ix])
  for key,*_ in MIXED:
   p=next(p for p in self.ms[key]['propers'] if p['name']=='Alleluia')
   assert_current_latin_body_or_gap(self,key,'Alleluia',p)
 def test_page_coordinates_and_raster_receipts_remain_source_specific(self):
  for key,name,number,page,folio,*_ in EXPECTED+[(k,'Alleluia',n,p,f) for k,n,p,f in MIXED]:
   rows=[r for r in self.record['appointments'] if r['mass']==key and r['proper']==name and r['marginal_number']==number]
   self.assertEqual(len(rows),1);r=rows[0]
   self.assertEqual((r['pdf_page'],r['printed_page']),(page,folio))
   self.assertTrue(all(re.fullmatch('[0-9a-f]{64}',h) for h in r['raster_sha256']))
 def test_schema_owner_accepts_exact_typed_nodes_and_rejects_reason_note(self):
  path=ROOT/'tools/check-calendar-masses';loader=importlib.machinery.SourceFileLoader('easter_normal_checker',str(path));spec=importlib.util.spec_from_loader(loader.name,loader);checker=importlib.util.module_from_spec(spec);sys.modules[spec.name]=checker;loader.exec_module(checker)
  p=next(p for p in self.ms['holy-wednesday']['propers'] if p['name']=='Oratio');problems=[]
  checker.check_proper('holy-wednesday',p,problems,calendar='roman-1962');self.assertEqual(problems,[])
  # This technical gap exercises the reason schema even if the source body is recovered.
  gap={k:v for k,v in p.items() if k!='text'};gap['text_status']={'state':'unavailable','scope':'proper-body','reasons':[{'kind':'no-exemplar'}]}
  problems=[];checker.check_proper('technical-gap',gap,problems,calendar='roman-1962');self.assertEqual(problems,[])
  bad=copy.deepcopy(gap);bad['text_status']['reasons'][0]['note']='not an allowed reason field';problems=[]
  checker.check_proper('negative',bad,problems,calendar='roman-1962');self.assertTrue(problems)
 def test_omitted_unit_and_lost_uncited_component_are_detected(self):
  bad=copy.deepcopy(self.doc);m=mass_index(bad)['easter-thursday'];m['propers']=[p for p in m['propers'] if p['name']!='Alleluia'];self.assertIn(('easter-thursday','Alleluia'),source_problems(bad))
  bad=copy.deepcopy(self.doc);p=next(p for p in mass_index(bad)['pentecost-monday']['propers'] if p['name']=='Alleluia');p['source']='scripture';p.pop('text_status',None);self.assertIn(('pentecost-monday','Alleluia'),source_problems(bad))
 def test_rogation_exact_source_courses_and_incompatible_choice(self):
  rows,errors=resolve_propers(self.doc,self.ms['rogation-mass']);self.assertEqual(errors,[])
  payload={'rows':[_public_appointment_proper(p) for _,p,_ in rows],'facts':self.doc['proper_appointment_facts']}
  js=r'''
const assert=require('node:assert/strict'),fs=require('node:fs');const owner=require(process.argv[1]);const d=JSON.parse(fs.readFileSync(0,'utf8'));
function course(season,choices={}){const p=owner.prepareProperAppointments(d.rows,{calendar:'roman-1962',entrance:'day',date:'2026-05-12',season,facts:d.facts,choices});const e=owner.unframedEvents(p.rows,null,p.selections);return {p,e,names:e.flatMap(x=>x.kind==='proper'?[x.proper.name]:(x.options.find(o=>o.id===x.selection.option)?.rows||[]).map(r=>r.proper.name))};}
for(const [s,yes,no] of [['paschaltide',['Alleluia (Tempore paschali)'],['Gradual','Alleluia','Tract']],['epiphanytide',['Gradual','Alleluia'],['Tract','Alleluia (Tempore paschali)']],['lent',['Gradual','Tract'],['Alleluia','Alleluia (Tempore paschali)']]]){const r=course(s);for(const n of yes)assert(r.names.includes(n));for(const n of no)assert(!r.names.includes(n));assert.equal(r.p.unresolved.length,0);}
assert.throws(()=>course('paschaltide',{'main/rogation-post-epistle':'regular'}),/contradicts source applicability/);
const unknown=owner.prepareProperAppointments(d.rows,{calendar:'roman-1962',entrance:'propers',facts:d.facts});assert(unknown.unresolved.length>0);assert.equal(unknown.selections['main/rogation-post-epistle'].state,'required');
const wrong=structuredClone(d.facts);wrong['roman-1962-common-chant-regime'].edition='roman-pre-1955';assert.throws(()=>owner.prepareProperAppointments(d.rows,{calendar:'roman-1962',entrance:'day',date:'2026-05-12',season:'paschaltide',facts:wrong}),/another edition/);
console.log('exact three seasonal courses; incompatible choice, unknown and foreign fact controls passed');
'''
  r=subprocess.run(['node','-e',js,str(ROOT/'src/web/browser/liturgy/ordinary-seating.js')],input=json.dumps(payload),capture_output=True,text=True);self.assertEqual(r.returncode,0,r.stdout+r.stderr)
 def test_holy_wednesday_keeps_explicit_unavailable_frame_and_unframed_order(self):
  self.assertEqual(self.ms['holy-wednesday']['ordinary_frame']['applicability'],'unavailable')
  rows,errors=resolve_propers(self.doc,self.ms['holy-wednesday']);self.assertEqual(errors,[])
  ps=[p for _,p,_ in rows];names=[p['name'] for p in ps];self.assertEqual(names[-2:],['Postcommunion','Oratio super populum'])
  state=assert_current_latin_body_or_gap(self,'holy-wednesday','Oratio super populum',ps[-1])
  self.assertLess(names.index('Oratio'),names.index('Second Lesson'))
  path=ROOT/'tools/mass-today';loader=importlib.machinery.SourceFileLoader('easter_normal_today',str(path));spec=importlib.util.spec_from_loader(loader.name,loader);today=importlib.util.module_from_spec(spec);sys.modules[spec.name]=today;loader.exec_module(today)
  self.assertEqual(today.validated_ordinary_frame(self.ms['holy-wednesday']['ordinary_frame'])['applicability'],'unavailable')
  projection=today.language_projection(ps[-1],'la',None)
  self.assertEqual(projection['available'],state=='present');self.assertEqual(projection['status'],'full-text' if state=='present' else 'unavailable')
  if state=='present':self.assertEqual(projection['texts'],[{'lang':'la','text':ps[-1]['text']}])
if __name__=='__main__':unittest.main()
