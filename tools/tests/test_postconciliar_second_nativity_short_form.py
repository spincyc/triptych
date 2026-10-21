"""OLM1981 artifact69 / printed15 n19 Gospel lengths share one semantic seat."""
from pathlib import Path
from importlib.machinery import SourceFileLoader
from importlib.util import module_from_spec,spec_from_loader
import sys,unittest,yaml
ROOT=Path(__file__).resolve().parents[2]
PROPERS=ROOT/'src/sources/calendars/postconciliar/propers.yaml'

def load_tool(name):
 loader=SourceFileLoader('_second_nativity_'+name.replace('-','_'),str(ROOT/'tools'/name));spec=spec_from_loader(loader.name,loader);mod=module_from_spec(spec);sys.modules[loader.name]=mod;loader.exec_module(mod);return mod

class SecondNativityShortFormTest(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.doc=yaml.safe_load(PROPERS.read_text());cls.mass=next(m for s in cls.doc['sections'].values() for m in s['masses'] if m['key']=='second-sunday-after-nativity');cls.owner=load_tool('mass-propers');cls.canon=load_tool('citations')
 def test_source_lengths_are_adjacent_exclusive_options(self):
  rows=self.mass['propers'];i=next(i for i,p in enumerate(rows) if p['name']=='Gospel');full,short=rows[i:i+2]
  self.assertEqual(short['name'],'Gospel (shorter form)');self.assertEqual(full['verses'],[self.canon.parse_citation('John 1:1-18')]);self.assertEqual(short['verses'],[self.canon.parse_citation('John 1:1-5, 9-14')])
  for p,option in [(full,'longer'),(short,'shorter')]:
   relation=self.owner.public_ordinary_disposition(p['ordinary_disposition']);self.assertEqual((relation['kind'],relation['group'],relation['option']),('alternative','gospel',option));self.assertNotIn('cycles',p);self.assertEqual(p['source'],'scripture')
  self.assertEqual(full['ordinary_disposition']['basis'],short['ordinary_disposition']['basis'])
 def test_short_projection_keeps_both_disjoint_runs(self):
  short=next(p for p in self.mass['propers'] if p['name']=='Gospel (shorter form)');view=self.owner.citation_structure(short['verses'][0],'hebrew',self.owner.book_tokens());self.assertIsNone(view['unresolved']);self.assertEqual(view['loci']['vulgate'],[{'chapter':1,'first':1,'last':5},{'chapter':1,'first':9,'last':14}])
if __name__=='__main__':unittest.main()
