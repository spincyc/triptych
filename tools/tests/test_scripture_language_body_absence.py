"""English whole-body scope cannot be satisfied by a Bible component."""
from pathlib import Path
from importlib.machinery import SourceFileLoader
from importlib.util import spec_from_loader,module_from_spec
import copy,json,sys,tomllib,unittest,subprocess
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'scripts'))
import _missal_coverage as V
loader=SourceFileLoader('_language_body_mass_propers',str(ROOT/'tools/mass-propers'));spec=spec_from_loader(loader.name,loader);M=module_from_spec(spec);sys.modules[loader.name]=M;loader.exec_module(M)
class ScriptureLanguageBodyTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.root=ROOT/'src/sources/calendars';cls.records,problems=M._source_library_records(cls.root);assert not problems,problems
  ledger=tomllib.loads((ROOT/'src/sources/inventories/postconciliar-proper-translations-v1.toml').read_text())
  expected={'saints-basil-great-gregory-nazianzen-bishops','saint-athanasius-bishop-doctor-church','saints-joachim-anne-parents-blessed-virgin','saint-dominic-priest','saint-augustine-bishop-doctor-church','saint-leo-great-pope-doctor-church','saint-ambrose-bishop-doctor-church'}
  cls.rows=[r for r in ledger['untranslated'] if r.get('mass') in expected and r.get('witness_passage_id') and str((cls.records.get(r['witness_passage_id']) or {}).get('locus') or '').startswith('proper-body:')]
  assert len(cls.rows)==7
 def test_registered_english_body_bindings_are_exact(self):
  self.assertGreaterEqual(len(self.rows),7)
  for row in self.rows:
   with self.subTest(mass=row['mass']):self.assertEqual(M.scripture_body_absence_problems(row,'postconciliar',self.records),[])
 def test_wrong_target_language_witness_page_or_hash_cannot_own_body(self):
  original=self.rows[0]
  for key,value in [('mass','wrong-target'),('lang','la'),('witness_artifact_id','unknown-artifact'),('witness_passage_id','unknown-passage'),('verified_artifact_page',999),('verified_on_page','1900-01-01')]:
   row=copy.deepcopy(original);row[key]=value
   with self.subTest(field=key):self.assertTrue(M.scripture_body_absence_problems(row,'postconciliar',self.records))
  records=copy.deepcopy(self.records);records[original['witness_passage_id']]['artifact_sha256']='0'*64
  self.assertTrue(M.scripture_body_absence_problems(original,'postconciliar',records))
  records=copy.deepcopy(self.records);artifact=records[original['witness_artifact_id']];records[artifact['edition_id']]['language']='la'
  self.assertTrue(M.scripture_body_absence_problems(original,'postconciliar',records))
 def test_only_explicit_exact_language_enters_body_coverage(self):
  row=self.rows[0];public=M.public_untranslated_record(row);source=V.identity('postconciliar','proper',row['mass'],row['form_id'],row['proper'],row['occurrence']);target=V.identity(source,'all','all')
  owner={'source':'scripture','citations':[{'ref':'Sirach 15:5'}],'untranslated':[public]}
  unit=V.unit(owner,target_id=target,occurrence_id=target,absence_kinds={'en':['rights-withheld']})
  self.assertEqual(unit['body_languages'],['en']);self.assertEqual(unit['component'],'proper-body');self.assertIn('scripture_component',unit)
  report=V.summarize([unit],'selection');V.validate_summary(report)
  la,en=report['languages'];self.assertEqual(la['targets'],0);self.assertEqual(en['targets'],1);self.assertEqual(en['availability']['not-publishable'],1)
  del owner['untranslated'];pure=V.unit(owner,target_id=target,occurrence_id=target,absence_kinds={'en':['rights-withheld']})
  self.assertEqual(pure['component'],'scripture');self.assertNotIn('body_languages',pure)
  public['target']['mass']='wrong-target';owner['untranslated']=[public]
  self.assertEqual(V.unit(owner,target_id=target,occurrence_id=target)['component'],'scripture')
 def test_scope_has_one_closed_public_shape(self):
  for scope in [[],['la'],['en','la'],['en','en'],'en',None]:
   with self.subTest(scope=scope):
    with self.assertRaises(ValueError):V.summarize([{'schema':V.UNIT_SCHEMA,'body_languages':scope,'component':'proper-body','scripture_component':{}}],'selection')
 def test_ordinary_scripture_denominator_and_mixed_units_keep_their_contract(self):
  identity=('synthetic','main','Entrance Antiphon',1)
  self.assertEqual(M.coverage_slot_units({'source':'scripture'},identity),[])
  self.assertEqual(len(M.coverage_slot_units({'source':'mixed'},identity)),1)
  owner={'source':'mixed','citations':[{'ref':'Sirach 15:5'}]}
  mixed=V.unit(owner,target_id='synthetic',occurrence_id='synthetic')
  self.assertNotIn('body_languages',mixed);self.assertIn('scripture_component',mixed)
  V.validate_summary(V.summarize([mixed],'selection'))
 def test_actual_shared_read_selection_and_dom_keep_bible_as_component(self):
  structure=M.calendar_structure(self.root,'postconciliar',M.book_tokens());cases=[]
  for row in self.rows:
   mass=next(m for m in structure['masses'] if m['key']==row['mass'])
   proper=next(p for p in mass['propers'] if p['name']==row['proper'])
   cases.append({'mass':mass,'proper':proper,'target':row})
  payload={'structure':structure,'cases':cases,'expectedCoverage':{mass['key']:V.summarize(V.proper_units(mass),'selection') for mass in (c['mass'] for c in cases)},'input':{'bibles':json.loads((ROOT/'src/web/data/bibles.json').read_text())}}
  result=subprocess.run(['node',str(ROOT/'tools/tests/scripture_language_body_read.mjs')],input=json.dumps(payload),text=True,capture_output=True,cwd=ROOT)
  self.assertEqual(result.returncode,0,result.stderr)
  proof=json.loads(result.stdout);self.assertEqual(proof['actualCases'],7);self.assertEqual(proof['actualCarrierRenders'],49)
if __name__=='__main__':unittest.main()
