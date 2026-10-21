"""Page-collated 1962 reading continuations and complete local primary families.

Bounds below are independent printed-page facts from CMAA1962 AP629–806, not
expectations derived from generated Bible payloads. Exact liturgical wording,
including Gregory's cento, has a separate source-body proof obligation.
"""
from pathlib import Path
import copy
import os
import sys
import unittest
import yaml
ROOT=next(p for p in Path(__file__).resolve().parents if (p/'tools/citations').is_file())
sys.path.insert(0,str(ROOT/'scripts'))
from _calendars import resolve_propers
DATA=Path(os.environ.get('TRIPTYCH_1962_PRIMARY_DATA',str(ROOT/'src/sources/calendars/roman-1962/propers.yaml')))
EXPECTED={
 ('assumptione-beatae-mariae-virginis','Lesson'):[('Judith',[(13,22,13,25),(15,10,15,10)])], # AP708/p627 n3380
 ('s-barnabae-apostoli','Epistle'):[('Acts',[(11,21,11,26),(13,1,13,3)])], # AP629–630 n2752
 ('s-irenaei-episcopi-martyris','Epistle'):[('2 Timothy',[(3,14,3,17),(4,1,4,5)])], # AP658–659 n2974
 ('s-mariae-magdalenae-paenitentis','Lesson'):[('Song of Songs',[(3,2,3,5),(8,6,8,7)])], # AP678 n3135
 ('s-marthae-virginis','Epistle'):[('2 Corinthians',[(10,17,10,18),(11,1,11,2)])], # AP686 n3201
 ('s-ignatii-confessoris','Epistle'):[('2 Timothy',[(2,8,2,10),(3,10,3,12)])], # AP689 n3226
 ('s-gregorii-thaumaturgi-episcopi-confessoris','Lesson'):[('Sirach',[(44,16,44,27),(45,3,45,20)])], # AP801 n4114
 ('s-clementis-i-papae-martyris','Epistle'):[('Philippians',[(3,17,3,21),(4,1,4,3)])], # AP805–806 n4147
}
MANDATORY={('s-nicolai-episcopi-confessoris','Epistle'):[('Hebrews',[(13,7,13,17)])]} # AP515/p434 n1854
FAMILIES={
 's-raphaelis-archangeli':[('Lesson',[('Tobit',[(12,7,12,15)])]),('Gospel',[('John',[(5,1,5,4)])])], # complete AP776–777
 'ss-simonis-iudae-apostolorum':[('Epistle',[('Ephesians',[(4,7,4,13)])]),('Gospel',[('John',[(15,17,15,25)])])], # complete AP781–783
}
def masses(doc):return {m['key']:m for section in doc['sections'].values() for m in section['masses']}
def bounds(proper):
 out=[]
 for v in proper.get('verses',[]):
  spans=[(r['begin']['chapter'],r['begin']['verse'],r['end']['chapter'],r['end']['verse']) for r in v['ranges']]
  if out and out[-1][0]==v['book']:out[-1][1].extend(spans)
  else:out.append((v['book'],spans))
 return out
def resolved(doc,key):
 entries,errors=resolve_propers(doc,masses(doc)[key])
 if errors:raise AssertionError(errors)
 return [(p['name'],bounds(p)) for form,p,origin in entries if p['name'] in {'Lesson','Epistle','Gospel'}]
def defects(doc):
 found=[]
 for (key,name),want in (EXPECTED | MANDATORY).items():
  held=[b for n,b in resolved(doc,key) if n==name]
  if held!=[want]:found.append((key,name))
 for key,want in FAMILIES.items():
  if resolved(doc,key)!=want:found.append((key,'whole-primary-family'))
 return found
class AnnualPrimaryReadings(unittest.TestCase):
 @classmethod
 def setUpClass(cls):cls.doc=yaml.safe_load(DATA.read_text())
 def test_printed_continuations_and_full_local_families(self):self.assertEqual(defects(self.doc),[])
 def test_nicholas_source_epistle_once_before_gradual(self):
  entries,errors=resolve_propers(self.doc,masses(self.doc)['s-nicolai-episcopi-confessoris'])
  self.assertEqual(errors,[])
  names=[p['name'] for _,p,_ in entries]
  self.assertEqual(names.count('Epistle'),1)
  self.assertEqual(names[names.index('Epistle')+1],'Gradual')
 def test_each_lost_continuation_is_detected(self):
  self.assertEqual(defects(self.doc),[])
  for key,name in EXPECTED:
   with self.subTest(mass=key):
    damaged=copy.deepcopy(self.doc);p=next(p for p in masses(damaged)[key]['propers'] if p['name']==name)
    p['verses']=p['verses'][:1];p['verses'][0]['ranges']=p['verses'][0]['ranges'][:1]
    self.assertIn((key,name),defects(damaged))
 def test_reading_borrowed_from_other_formulary_is_detected(self):
  self.assertEqual(defects(self.doc),[])
  for key in FAMILIES:
   with self.subTest(mass=key):
    damaged=copy.deepcopy(self.doc)
    masses(damaged)[key]['propers'].insert(3,{'name':'Epistle','source':'scripture','verses':[{'book':'Colossians','ref':'Colossians 1:12-20','ranges':[{'begin':{'chapter':1,'verse':12},'end':{'chapter':1,'verse':20}}]}]})
    self.assertIn((key,'whole-primary-family'),defects(damaged))
if __name__=='__main__':unittest.main()
