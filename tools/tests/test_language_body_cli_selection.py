"""The actual CLI plaintext body notice follows eligible language/witness selection."""
from pathlib import Path
from importlib.machinery import SourceFileLoader
from importlib.util import spec_from_loader,module_from_spec
import copy,sys,tomllib,unittest
ROOT=Path(__file__).resolve().parents[2]
def tool(name):
 loader=SourceFileLoader('_body_cli_'+name.replace('-','_'),str(ROOT/'tools'/name));spec=spec_from_loader(loader.name,loader);m=module_from_spec(spec);sys.modules[loader.name]=m;loader.exec_module(m);return m
TODAY=tool('mass-today');MASS=tool('mass-propers')
class LanguageBodyCliSelectionTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  ledger=tomllib.loads((ROOT/'src/sources/inventories/postconciliar-proper-translations-v1.toml').read_text())
  row=next(r for r in ledger['untranslated'] if r.get('mass')=='saints-basil-great-gregory-nazianzen-bishops' and r.get('proper')=='Entrance Antiphon' and r.get('extent')=='body')
  cls.absence=MASS.public_untranslated_record(row)
 def proper(self):
  return {'name':'Entrance Antiphon','source':'scripture','verses':[{'ref':'Sirach 15:5','text':'Synthetic Bible component.'}],'untranslated':[copy.deepcopy(self.absence)],'unavailable_translations':[copy.deepcopy(self.absence)]}
 def plain(self,p,witness=None,lang='en'):
  return '\n'.join(TODAY.proper_lines(p,TODAY.Style('plain'),'x',lang=lang,witness=witness,seat=None,why=False))
 def test_actual_plaintext_and_machine_positive_body_selection_agree(self):
  p=self.proper();p['translations']=[{'lang':'en','text':'Synthetic eligible English body.','source_id':'project-created-test','rights':'project-created'}]
  projection=TODAY.language_projection(p,'en',{'id':'synthetic','language':'en'})
  self.assertEqual(projection['status'],'full-text');self.assertTrue(projection['available'])
  for witness in [None,'project-created-test']:
   with self.subTest(witness=witness):
    rendered=self.plain(p,witness);self.assertIn('Synthetic eligible English body.',rendered);self.assertIn('shown separately from the selected antiphon body',rendered)
    self.assertNotIn('whole requested-language antiphon body is unavailable',rendered);self.assertNotIn('en antiphon body unavailable',rendered);self.assertNotIn('en unavailable',rendered)
 def test_other_held_witness_does_not_fill_selected_absent_witness(self):
  p=self.proper();p['translations']=[{'lang':'en','text':'Synthetic other witness body.','source_id':'other-witness','rights':'project-created'}]
  self.assertEqual(TODAY.language_projection(p,'en',None)['status'],'full-text')
  rendered=self.plain(p,'absent-witness');self.assertNotIn('Synthetic other witness body.',rendered);self.assertIn('whole requested-language antiphon body is unavailable',rendered);self.assertIn('rights restricted',rendered)
 def test_bible_component_and_latin_fallback_cannot_supply_english_body(self):
  for latin in [None,'Synthetic Latin fallback.']:
   p=self.proper()
   if latin:p['text']=latin
   projection=TODAY.language_projection(p,'en',{'id':'synthetic','language':'en'});self.assertEqual(projection['status'],'withheld');self.assertFalse(projection['available'])
   for witness in [None,'absent-witness']:
    rendered=self.plain(p,witness);self.assertIn('Synthetic Bible component.',rendered);self.assertIn('whole requested-language antiphon body is unavailable',rendered);self.assertIn('rights restricted',rendered)
 def test_unmarked_scripture_and_other_languages_keep_existing_behavior(self):
  p=self.proper();self.assertNotIn('whole requested-language',self.plain(p,lang='la'))
  p.pop('untranslated');p.pop('unavailable_translations');rendered=self.plain(p);self.assertNotIn('antiphon body unavailable',rendered);self.assertNotIn('Bible component only',rendered)
  self.assertEqual(TODAY.language_projection(p,'en',{'id':'synthetic','language':'en'})['status'],'scripture-delegated')
if __name__=='__main__':unittest.main()
