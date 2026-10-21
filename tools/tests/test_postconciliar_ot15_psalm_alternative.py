"""OLM1981 artifact115 / printed61 n105 gives a YearC-only Psalm alternative."""
from pathlib import Path
from importlib.machinery import SourceFileLoader
from importlib.util import module_from_spec,spec_from_loader
import sys,unittest,yaml
ROOT=Path(__file__).resolve().parents[2]
PROPERS=ROOT/'src/sources/calendars/postconciliar/propers.yaml'

def load_tool(name):
 loader=SourceFileLoader('_ot15_psalm_'+name.replace('-','_'),str(ROOT/'tools'/name));spec=spec_from_loader(loader.name,loader);mod=module_from_spec(spec);sys.modules[loader.name]=mod;loader.exec_module(mod);return mod

class OrdinaryTimeFifteenPsalmAlternativeTest(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.doc=yaml.safe_load(PROPERS.read_text());cls.mass=next(m for s in cls.doc['sections'].values() for m in s['masses'] if m['key']=='ot-15');cls.owner=load_tool('mass-propers');cls.canon=load_tool('citations')
 def test_only_year_c_has_the_alternative_and_primary_is_preserved(self):
  rows=self.mass['propers'];i=next(i for i,p in enumerate(rows) if p['name']=='Responsorial Psalm');primary,alt=rows[i:i+2];self.assertEqual(alt['name'],'Responsorial Psalm (alternative)');self.assertEqual(set(primary['cycles']),set('ABC'));self.assertEqual(set(alt['cycles']),{'C'})
  refs={'A':'Psalm 65:10abcd, 10e-11, 12-13, 14','B':'Psalm 85:9ab-10, 11-12, 13-14','C':'Psalm 69:14, 17, 30-31, 33-34, 36ab, 37'}
  for c,ref in refs.items():self.assertEqual(primary['cycles'][c]['verses'],[self.canon.parse_citation(ref)])
  for p,option in [(primary,'principal'),(alt,'psalm-19')]:
   relation=self.owner.public_ordinary_disposition(p['ordinary_disposition']);self.assertEqual((relation['kind'],relation['group'],relation['option']),('alternative','responsorial-psalm',option))
 def test_canonical_projection_returns_the_four_printed_vulgate_verses(self):
  rows=[p for p in self.mass['propers'] if p['name']=='Responsorial Psalm (alternative)'];self.assertEqual(len(rows),1);entry=rows[0]['cycles']['C']['verses'][0];self.assertEqual(entry,self.canon.parse_citation('Psalm 19:8, 9, 10, 11'));view=self.owner.citation_structure(entry,'hebrew',self.owner.book_tokens());self.assertIsNone(view['unresolved']);self.assertEqual(view['loci']['vulgate'],[{'chapter':18,'first':n,'last':n} for n in (8,9,10,11)])
if __name__=='__main__':unittest.main()
