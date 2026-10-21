"""OLM1981 artifact86 / printed32 nn43-45 appoints distinct EasterII Psalms."""
from pathlib import Path
from importlib.machinery import SourceFileLoader
from importlib.util import module_from_spec,spec_from_loader
import sys,unittest,yaml
ROOT=Path(__file__).resolve().parents[2]
PROPERS=ROOT/'src/sources/calendars/postconciliar/propers.yaml'

def load_tool(name):
 loader=SourceFileLoader('_easter2_primary_'+name.replace('-','_'),str(ROOT/'tools'/name));spec=spec_from_loader(loader.name,loader);mod=module_from_spec(spec);sys.modules[loader.name]=mod;loader.exec_module(mod);return mod

class EasterTwoPrimaryPsalmsTest(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.doc=yaml.safe_load(PROPERS.read_text());cls.mass=next(m for s in cls.doc['sections'].values() for m in s['masses'] if m['key']=='easter-2');cls.owner=load_tool('mass-propers');cls.canon=load_tool('citations')
 def test_each_source_cycle_retains_its_distinct_passage(self):
  row=next(p for p in self.mass['propers'] if p['name']=='Responsorial Psalm')
  self.assertNotIn('verses',row);self.assertEqual(set(row['cycles']),set('ABC'))
  refs={'A':'Psalm 118:2-4, 13-15, 22-24','B':'Psalm 118:2-4, 16ab-18, 22-24','C':'Psalm 118:2-4, 22-24, 25-27a'}
  for c,ref in refs.items():
   entry=row['cycles'][c]['verses'][0];self.assertEqual(entry,self.canon.parse_citation(ref));view=self.owner.citation_structure(entry,'hebrew',self.owner.book_tokens());self.assertIsNone(view['unresolved']);self.assertEqual(view['loci']['vulgate'],[{'chapter':117,'first':r['begin']['verse'],'last':r['end']['verse']} for r in entry['ranges']])
 def test_common_gospel_and_acclamation_remain_unqualified(self):
  for name,ref in [('Gospel','John 20:19-31'),('Gospel Acclamation','John 20:29')]:
   row=next(p for p in self.mass['propers'] if p['name']==name);self.assertNotIn('cycles',row);self.assertEqual(row['verses'],[self.canon.parse_citation(ref)])
if __name__=='__main__':unittest.main()
