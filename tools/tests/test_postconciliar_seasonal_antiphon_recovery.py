"""Preserve source-backed antiphon seats, numbering, conditions and body gaps."""
from pathlib import Path
from importlib.machinery import SourceFileLoader
from importlib.util import module_from_spec,spec_from_loader
from collections import Counter
import copy,json,sys,tomllib,unittest,yaml
ROOT=Path(__file__).resolve().parents[2]
SOURCE=ROOT/'src/sources/calendars/postconciliar/propers.yaml'
EVIDENCE=ROOT/'src/sources/inventories/postconciliar-seasonal-collation-v1.toml'
ENGLISH=ROOT/'src/sources/inventories/postconciliar-proper-translations-v1.toml'
ART='artifact.catholic-church.missale-romanum.2010-english-icel-antiphonary.antiphonary-pdf'
TARGET='edition.catholic-church.missale-romanum.vatican-typica-tertia-reimpressio-emendata-2008'
def tool(name):
 loader=SourceFileLoader('_seasonal_recovery_test_'+name.replace('-','_'),str(ROOT/'tools'/name));m=module_from_spec(spec_from_loader(loader.name,loader));sys.modules[loader.name]=m;loader.exec_module(m);return m
class SeasonalAntiphonRecoveryTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.document=yaml.safe_load(SOURCE.read_text());cls.masses={m['key']:m for s in cls.document['sections'].values() for m in s['masses']};cls.evidence=tomllib.loads(EVIDENCE.read_text())['seasonal_antiphon_recovery_2026_10_21'];cls.english=tomllib.loads(ENGLISH.read_text())['untranslated'];cls.check=tool('check-calendar-masses');cls.canon=tool('citations');cls.owner=tool('mass-propers');cls.ordinary=tool('mass-ordinary');cls.frame=json.loads((ROOT/'src/web/data/structure/ordinary/postconciliar.json').read_text())
 def test_exact_source_cues_and_positions_bind_all_213_provisions(self):
  facts=self.evidence['rows'];self.assertEqual(len(facts),213);self.assertEqual(len({r['mass'] for r in facts}),106)
  self.assertEqual(Counter(r['proper'] for r in facts),Counter({'Entrance Antiphon':107,'Communion Antiphon':106}))
  for f in facts:
   with self.subTest(mass=f['mass'],proper=f['proper'],occurrence=f['occurrence']):
    mass=self.masses[f['mass']];rows=[p for p in mass['propers'] if p['name']==f['proper']];p=rows[f['occurrence']-1]
    self.assertEqual(self.owner.source_slot_identity(self.document,mass,'',p,None),(f['mass'],'main',f['proper'],f['occurrence']))
    self.assertIn(f"artifact page {f['artifact_page']} / printed page {f['printed_page']}",p['notes'])
    self.assertNotIn('text',p);self.assertNotIn('incipit',p);self.assertNotIn('translations',p)
    cue=f['source_citation_cue']
    if cue=='!uncited':
     self.assertEqual(p['source'],'composed');self.assertNotIn('verses',p)
     self.assertEqual(p['text_status'],{'state':'unavailable','scope':'proper-body','reasons':[{'kind':'witness-gap','source_id':TARGET}]})
    else:
     expected=[self.canon.parse_citation(c.strip()) for c in cue.removeprefix('Cf. ').split(';;')]
     self.assertEqual(p['source'],'scripture');self.assertEqual(p['verses'],expected)
     if any(e['book']=='Psalms' for e in expected):self.assertEqual(p['psalm_numbering'],'vulgate')
 def test_the_two_unconditional_alternative_groups_have_no_default(self):
  for key,role,group in [('easter-monday','Entrance Antiphon','entrance-antiphon'),('most-sacred-heart-jesus','Communion Antiphon','communion-antiphon')]:
   mass=self.masses[key];rows=[p for p in mass['propers'] if p['name']==role]
   self.assertEqual(len(rows),2);self.assertEqual([p['ordinary_disposition']['option'] for p in rows],['source-first','source-second'])
   self.assertEqual(rows[0]['ordinary_disposition']['basis'],rows[1]['ordinary_disposition']['basis'])
   for p in rows:
    self.assertEqual(p['ordinary_disposition']['kind'],'alternative');self.assertEqual(p['ordinary_disposition']['group'],group);self.assertNotIn('default',p['ordinary_disposition']);self.assertNotIn('cycles',p)
   self.ordinary.check_form_seating(self.frame,mass['propers'],key,full=True)
   singleton=copy.deepcopy(mass);singleton['propers'].remove(next(p for p in singleton['propers'] if p.get('ordinary_disposition',{}).get('option')=='source-second'))
   with self.assertRaisesRegex(self.ordinary.SourceError,'two distinct options|two options'):self.ordinary.check_form_seating(self.frame,singleton['propers'],'singleton',full=True)
   cross=copy.deepcopy(mass['propers']);member=next(p for p in cross if p.get('ordinary_disposition',{}).get('option')=='source-second');member['name']='Communion Antiphon' if role=='Entrance Antiphon' else 'Entrance Antiphon'
   with self.assertRaisesRegex(self.ordinary.SourceError,'spans Ordinary slots'):self.ordinary.check_form_seating(self.frame,cross,'cross-seat',full=True)
 def test_printed_order_and_source_conditions_remain_owned(self):
  self.assertEqual(self.check.order_problems([SOURCE]),[])
  self.assertIn('morning Mass of 24 December',self.masses['advent-december-24']['notes'])
  for week,days in [(1,['monday','tuesday','wednesday','thursday','friday','saturday']),(2,['monday','tuesday','wednesday','thursday','friday','saturday']),(3,['monday','tuesday','wednesday','thursday'])]:
   for day in days:
    for p in self.masses[f'advent-{week}-{day}']['propers']:
     if p['name'] in ('Entrance Antiphon','Communion Antiphon'):self.assertIn('before 17 December',p['notes'])
  self.assertIn('Holy Family fallback',next(p for p in self.masses['christmas-december-30']['propers'] if p['name']=='Entrance Antiphon')['notes'])
 def test_uncited_english_exemplars_are_held_but_no_body_is_published(self):
  facts=[f for f in self.evidence['rows'] if f['source_citation_cue']=='!uncited'];self.assertEqual(len(facts),11)
  for f in facts:
   key={k:f[k] for k in ('mass','form_id','proper','occurrence')};records=[r for r in self.english if all(r.get(k)==v for k,v in key.items()) and r.get('lang')=='en' and r.get('cycle')=='all' and r.get('extent')=='body'];self.assertEqual(len(records),1)
   r=records[0];self.assertEqual(r['availability'],'unavailable');self.assertEqual(r['reason']['kind'],'rights-withheld');self.assertEqual(r['witness_artifact_id'],ART);self.assertEqual(r['verified_artifact_page'],f['artifact_page']);self.assertEqual(self.check.untranslated_witness_problems('seasonal uncited',r),[])
   self.assertNotIn('text',r);self.assertNotIn('quarantined_text_sha256',r)
 def test_recovery_does_not_select_unproved_formularies_or_erase_existing_repairs(self):
  selected={r['mass'] for r in self.evidence['rows']}
  self.assertFalse(any(k.startswith('christmas-january-') for k in selected));self.assertTrue(selected.isdisjoint({'blessed-virgin-mary-mother-church','good-friday','lent-5','easter-6-wednesday','easter-6-thursday','easter-7-saturday'}))
  self.assertEqual([p['name'] for p in self.masses['lent-5-monday']['propers'] if p['name'].endswith('Antiphon')],['Entrance Antiphon'])
  for key,ref in [('easter-7','Psalm 26:7-9'),('corpus-christi','Psalm 80:17')]:
   p=next(p for p in self.masses[key]['propers'] if p['name']=='Entrance Antiphon');self.assertEqual(p['psalm_numbering'],'vulgate');self.assertEqual(p['verses'][0]['ref'],ref)
  self.assertTrue(any(v['ref']=='John 6:54' for p in self.masses['ot-21']['propers'] if p['name'].startswith('Communion Antiphon') for v in p.get('verses',[])))
  self.assertEqual(self.document['psalm_numbering'],'hebrew')
if __name__=='__main__':unittest.main()
