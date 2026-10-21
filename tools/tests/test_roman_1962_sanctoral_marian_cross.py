"""Six complete normal feast forms collated to the held 1962 page images.

Source units are named below; explicit votive units are excluded from these
normal calendars until an owner proves whole-votive eligibility. Bible and
Common companions cannot answer an own literal Proper's whole-body English.
"""
from __future__ import annotations
import copy
import sys
import tomllib
import unittest
from pathlib import Path
import yaml

ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'scripts'))
from _calendars import resolve_propers
DATA=ROOT/'src/sources/calendars/roman-1962/propers.yaml'
TRANSLATIONS=ROOT/'src/sources/inventories/roman-1962-proper-translations-v1.toml'
K=['beatae-mariae-virginis-a-rosario','dedicatione-s-michaelis-archangeli','exaltatione-s-crucis','s-pii-x-papae-confessoris','sanctissimi-nominis-beatae-mariae-virginis','septem-dolorum-beatae-mariae-virginis']
# AP758R-760L/printed677-679; AP751L-752R/670-671;
# AP735R-736R/654-655; AP729R-730R/648-649;
# AP734L-735R/653-654; AP737L-739L/656-658.
EXPECTED={
 K[0]:[('Introit',3786),('Collect',3788),('Lesson',3790),('Gradual',3791),('Alleluia',3792),('Gospel',3795),('Offertory',3796),('Secret',3797),('Communion',3799),('Postcommunion',3800)],
 K[1]:[('Introit',3726),('Collect',3727),('Lesson',3728),('Gradual',3729),('Alleluia',3730),('Gospel',3731),('Offertory',3732),('Secret',3733),('Communion',3734),('Postcommunion',3735)],
 K[2]:[('Introit',3605),('Collect',3606),('Epistle',3607),('Gradual',3608),('Alleluia',3609),('Gospel',3610),('Offertory',3611),('Secret',3612),('Communion',3613),('Postcommunion',3614)],
 K[3]:[('Introit',3555),('Collect',3556),('Epistle',3557),('Gradual',3558),('Alleluia',3559),('Gospel',3562),('Offertory',3563),('Secret',3564),('Communion',3565),('Postcommunion',3566)],
 K[4]:[('Introit',3592),('Collect',3593),('Lesson',3594),('Gradual',3595),('Alleluia',3596),('Gospel',3600),('Offertory',3601),('Secret',3602),('Communion',3603),('Postcommunion',3604)],
 K[5]:[('Introit',3615),('Collect',3616),('Lesson',3619),('Gradual',3620),('Alleluia',3621),('Sequence',3624),('Gospel',3625),('Offertory',3626),('Secret',3627),('Communion',3629),('Postcommunion',3630)]}
# Each tuple is (book, chapter, first verse, last verse); all printed units
# here stay within one chapter. The tuple table is independent of the parser.
REFERENCES={
 (K[0],'Introit'):[('Psalms',44,2,2)],
 (K[0],'Lesson'):[('Proverbs',8,22,24),('Proverbs',8,32,35)],
 (K[0],'Gradual'):[('Psalms',44,5,5),('Psalms',44,11,11),('Psalms',44,12,12)],
 (K[0],'Gospel'):[('Luke',1,26,38)],
 (K[0],'Offertory'):[('Sirach',24,25,25),('Sirach',39,17,17)],
 (K[0],'Communion'):[('Sirach',39,19,19)],
 (K[1],'Introit'):[('Psalms',102,20,20),('Psalms',102,1,1)],
 (K[1],'Lesson'):[('Revelation',1,1,5)],
 (K[1],'Gradual'):[('Psalms',102,20,20),('Psalms',102,1,1)],
 (K[1],'Gospel'):[('Matthew',18,1,10)],
 (K[1],'Offertory'):[('Revelation',8,3,3),('Revelation',8,4,4)],
 (K[1],'Communion'):[('Daniel',3,58,58)],
 (K[2],'Introit'):[('Galatians',6,14,14),('Psalms',66,2,2)],
 (K[2],'Epistle'):[('Philippians',2,5,11)],
 (K[2],'Gradual'):[('Philippians',2,8,9)],
 (K[2],'Gospel'):[('John',12,31,36)],
 (K[3],'Introit'):[('Psalms',88,20,22),('Psalms',88,2,2)],
 (K[3],'Epistle'):[('1 Thessalonians',2,2,8)],
 (K[3],'Gradual'):[('Psalms',39,10,11)],
 (K[3],'Alleluia'):[('Psalms',22,5,6)],
 (K[3],'Gospel'):[('John',21,15,17)],
 (K[3],'Offertory'):[('Psalms',33,12,12)],
 (K[3],'Communion'):[('John',6,56,57)],
 (K[4],'Introit'):[('Psalms',44,13,13),('Psalms',44,15,15),('Psalms',44,16,16),('Psalms',44,2,2)],
 (K[4],'Lesson'):[('Sirach',24,23,31)],
 (K[4],'Gospel'):[('Luke',1,26,38)],
 (K[4],'Offertory'):[('Luke',1,28,28),('Luke',1,42,42)],
 (K[5],'Introit'):[('John',19,25,25),('John',19,26,27)],
 (K[5],'Lesson'):[('Judith',13,22,22),('Judith',13,23,25)],
 (K[5],'Gospel'):[('John',19,25,27)],
 (K[5],'Offertory'):[('Jeremiah',18,20,20)]}
LITERAL={(K[0],'Introit'),(K[0],'Alleluia'),(K[1],'Alleluia'),(K[2],'Introit'),(K[2],'Alleluia'),(K[2],'Offertory'),(K[2],'Communion'),(K[4],'Gradual'),(K[4],'Alleluia'),(K[4],'Communion'),(K[5],'Collect'),(K[5],'Gradual'),(K[5],'Alleluia'),(K[5],'Offertory'),(K[5],'Secret'),(K[5],'Communion'),(K[5],'Postcommunion')}
MIXED={(K[0],'Introit'),(K[2],'Introit'),(K[5],'Offertory')}
SOURCE='artifact.catholic-church.missale-romanum.vatican-typica-1962.cmaa-facsimile-pdf'
def masses(document):return{m['key']:m for section in document['sections'].values() for m in section['masses']}
def identity(row):return(row.get('mass'),row.get('form_id','main' if not row.get('form') else row['form']),row.get('proper'),row.get('cycle','all'),row.get('occurrence',1))
def english_problems(ledger):
 problems=[]
 for key,name in LITERAL:
  wanted=(key,'main',name,'all',1)
  bindings=[r for r in ledger.get('entries',[]) if identity(r)==wanted and any(t.get('lang')=='en' and isinstance(t.get('text'),str) and t['text'].strip() for t in r.get('translations',[]))]
  absent=[r for r in ledger.get('untranslated',[]) if identity(r)==wanted and r.get('lang')=='en' and r.get('extent')=='body']
  if bindings:
   if len(bindings)!=1 or absent:problems.append((wanted,'competing English coverage'))
  elif len(absent)!=1 or any(r.get('availability')!='unavailable' or r.get('reason')!={'kind':'no-exemplar'} for r in absent):problems.append((wanted,'missing or duplicate exact whole-body absence'))
 return problems
class SanctoralMarianCrossSourceTest(unittest.TestCase):
 @classmethod
 def setUpClass(cls):cls.document=yaml.safe_load(DATA.read_text());cls.by_key=masses(cls.document);cls.ledger=tomllib.loads(TRANSLATIONS.read_text())
 def test_complete_normal_source_order_and_no_votive_only_addition(self):
  count=0
  for key,units in EXPECTED.items():
   with self.subTest(mass=key):
    entries,errors=resolve_propers(self.document,self.by_key[key]);self.assertEqual(errors,[]);self.assertEqual([(form,p['name'],origin) for form,p,origin in entries],[('',name,None) for name,_ in units]);count+=len(entries)
    self.assertFalse(any(p.get('ordinary_disposition') for _,p,_ in entries));self.assertFalse(any('votive' in p['name'].lower() or p['name']=='Tract' for _,p,_ in entries))
  self.assertEqual(count,61)
 def test_every_printed_numeric_constituent_in_source_order(self):
  self.assertEqual(len(REFERENCES),31)
  for (key,name),expected in REFERENCES.items():
   with self.subTest(mass=key,proper=name):
    p=next(p for p in self.by_key[key]['propers'] if p['name']==name)
    actual=[(v['book'],r['begin']['chapter'],r['begin']['verse'],r['end']['chapter'],r['end']['verse']) for v in p['verses'] for r in v['ranges']]
    self.assertEqual(actual,[(book,ch,start,ch,end) for book,ch,start,end in expected])
 def test_literal_appointments_preserve_citations_and_have_body_or_typed_gap(self):
  self.assertEqual(len(LITERAL),17)
  for key,name in LITERAL:
   with self.subTest(mass=key,proper=name):
    p=next(p for p in self.by_key[key]['propers'] if p['name']==name);self.assertEqual(p['source'],'mixed' if (key,name) in MIXED else 'composed')
    if (key,name) in MIXED:self.assertTrue(p.get('verses'))
    else:self.assertNotIn('verses',p)
    if not p.get('text'):self.assertEqual(p.get('text_status'),{'state':'unavailable','scope':'proper-body','reasons':[{'kind':'witness-gap','source_id':SOURCE}]})
    else:self.assertNotIn('text_status',p)
 def test_exact_own_whole_body_english_accounting(self):
  self.assertEqual(english_problems(self.ledger),[])
  sample=next((r for r in self.ledger.get('untranslated',[]) if identity(r) in {(key,'main',name,'all',1) for key,name in LITERAL} and r.get('lang')=='en' and r.get('extent')=='body'),None)
  if sample is None:return
  duplicate=copy.deepcopy(self.ledger);duplicate['untranslated'].append(copy.deepcopy(sample));self.assertTrue(english_problems(duplicate))
  missing=copy.deepcopy(self.ledger);missing['untranslated']=[r for r in missing['untranslated'] if identity(r)!=identity(sample)];self.assertTrue(english_problems(missing))
if __name__=='__main__':unittest.main()
