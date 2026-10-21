"""The Common's pro Vidua reading is eligible, optional and never cumulative."""
from __future__ import annotations
import copy
import os
from pathlib import Path
import sys
import unittest

ROOT=Path(os.environ.get('TRIPTYCH_REVIEW_ROOT',Path(__file__).resolve().parents[2]))
CLI=Path(os.environ.get('TRIPTYCH_MASS_VALUES_CLI',ROOT))
sys.path.insert(0,str(CLI/'tools/tests'))
import test_mass_today_source_mass_context as H
C,TODAY=H.C,H.TODAY
TODAY.SEATING_MODEL=Path(os.environ.get('TRIPTYCH_MASS_VALUES_SEATING',ROOT/'src/web/browser/liturgy/ordinary-seating.js'))
FACT='roman-1962-non-virginum-2-subject';GROUP='non-virginum-2-reading';COMMON='commune-non-virginum-2'
# Exact dated headings and referrals, physically read on the held source.
# These are source eligibility witnesses, not saint-name classification rules.
CONTROLS={
 's-franciscae-romanae-viduae':('2026-03-09','lent',567,486,'S. Franciscae Romanae Vid.'),
 's-margaritae-reginae-viduae':('2026-06-10','after-pentecost',629,548,'S. Margaritae Reginae, Vid.'),
 's-elisabeth-reginae-viduae':('2026-07-08','after-pentecost',663,582,'S. Elisabeth Reginae, Vid.'),
 's-ioannae-franciscae-fremiot-chantal-viduae':('2026-08-21','after-pentecost',713,632,'S. Ioannae Franciscae Fremiot de Chantal Vid.'),
 's-hedwigis-viduae':('2026-10-16','after-pentecost',768,687,'S. Hedwigis Viduae'),
 's-elisabeth-viduae':('2026-11-19','after-pentecost',802,721,'S. Elisabeth Vid.'),
}

class Roman1962WidowReadingTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.source=C.read_yaml(H.SOURCE_FILE);cls.index=C.mass_index(cls.source)

 def rows(self,key,source=None):
  source=source or self.source
  rows,errors=C.resolve_propers(source,C.mass_index(source)[key],appointments=True)
  self.assertEqual(errors,[])
  return [{'proper':{**proper,'form_id':'main'},'sourceIndex':i} for i,(_,proper,_) in enumerate(rows)]

 def execute(self,key,option=None,*,season='after-pentecost',date='2026-07-08',source=None):
  source=source or self.source;mass=C.mass_index(source)[key]
  held={**mass,C.PROPER_APPOINTMENT_FACTS:source.get(C.PROPER_APPOINTMENT_FACTS,{})}
  choices=None if option is None else [f'proper-choice/{source["calendar"]}/{key}/main/{GROUP}={option}']
  predicates={'date':date,'season':season}
  context=TODAY.proper_appointment_context_for(source['calendar'],held,predicates,choices)
  return TODAY.mass_events(None,self.rows(key,source),None,predicates,context)

 def test_exact_six_positive_bindings_have_individual_source_heading_evidence(self):
  fact=self.source[C.PROPER_APPOINTMENT_FACTS][FACT]
  self.assertEqual(fact['edition'],'roman-1962')
  self.assertEqual(fact['values'],['general','widow'])
  self.assertNotIn('season_values',fact)
  self.assertEqual(set(fact['mass_values']),set(CONTROLS))
  for key,(_,_,artifact,folio,heading) in CONTROLS.items():
   with self.subTest(key=key):
    binding=fact['mass_values'][key]
    self.assertEqual(set(binding),{'value','basis'});self.assertEqual(binding['value'],'widow')
    for witness in (str(artifact),str(folio),heading,'non Virginum II'):
     self.assertIn(witness,binding['basis'])
    self.assertEqual(self.index[key]['takes_from']['mass'],COMMON)

 def test_common_rows_keep_literal_citations_and_one_exact_qualified_reading_group(self):
  common=self.index[COMMON];members=[p for p in common['propers'] if p.get('ordinary_disposition',{}).get('group')==GROUP]
  self.assertEqual([p['name'] for p in members],['Lesson','Epistle'])
  self.assertEqual([p['verses'][0]['ref'] for p in members],['Proverbs 31:10-31','1 Timothy 5:3-10'])
  for proper,option,values in zip(members,['principal','pro-vidua'],[['general','widow'],['widow']]):
   disposition=proper['ordinary_disposition']
   self.assertEqual(disposition['option'],option);self.assertEqual(disposition['seat'],'reading-1')
   self.assertEqual(disposition['anchor'],{'mass':COMMON,'form_id':'main','proper':'Lesson','occurrence':1})
   self.assertEqual(disposition['when'],{'fact':FACT,'in':values})

 def test_six_source_formularies_require_a_choice_and_execute_exactly_one_reading(self):
  for key,(date,season,*_) in CONTROLS.items():
   with self.subTest(key=key):
    unresolved=self.execute(key,season=season,date=date)
    choice=next(e for e in unresolved['events'] if e.get('kind')=='proper_choice' and e['group']==GROUP)
    self.assertEqual(choice['selection'],{'state':'required','option':None})
    self.assertEqual([option['id'] for option in choice['options']],['principal','pro-vidua'])
    self.assertFalse(any(e.get('kind')=='proper' and e['proper'].get('name') in ('Lesson','Epistle') for e in unresolved['events']))
    for option,reference in [('principal','Proverbs 31:10-31'),('pro-vidua','1 Timothy 5:3-10')]:
     selected=self.execute(key,option,season=season,date=date)
     event=next(e for e in selected['events'] if e.get('kind')=='proper_choice' and e['group']==GROUP)
     self.assertEqual(event['selection'],{'state':'selected','option':option})
     active=next(o['rows'] for o in event['options'] if o['id']==option)
     self.assertEqual(len(active),1);self.assertEqual(active[0]['proper']['verses'][0]['ref'],reference)

 def test_generic_common_does_not_gain_widow_eligibility_from_a_choice(self):
  result=self.execute(COMMON)
  self.assertEqual(result['proper_appointment_selections']['main/'+GROUP],{'state':'required','option':None})
  with self.assertRaisesRegex(TODAY.Refused,'unknown|unresolved|eligib'):
   self.execute(COMMON,'pro-vidua')
  principal=self.execute(COMMON,'principal')
  self.assertEqual(principal['proper_appointment_selections']['main/'+GROUP],{'state':'selected','option':'principal'})
  # Selecting a held season does not attest the independent source subject.
  common={**self.index[COMMON],C.PROPER_APPOINTMENT_FACTS:self.source[C.PROPER_APPOINTMENT_FACTS]}
  choices=[f'proper-choice/roman-1962/{COMMON}/main/{GROUP}=pro-vidua',f'proper-choice/roman-1962/{COMMON}/main/non-virginum-2-post-epistle=regular']
  context=TODAY.proper_appointment_context_for('roman-1962',common,{},choices)
  with self.assertRaisesRegex(TODAY.Refused,'unknown|unresolved|eligib'):
   TODAY.mass_events(None,self.rows(COMMON),None,{},context)

 def test_widow_like_name_and_date_cannot_fill_a_missing_binding(self):
  source=copy.deepcopy(self.source);common=C.mass_index(source)[COMMON]
  common['name']='Technical Viduae heading restatement; not a source binding'
  with self.assertRaisesRegex(TODAY.Refused,'unknown|unresolved|eligib'):
   self.execute(COMMON,'pro-vidua',source=source,date='2026-11-19')

 def test_foreign_inheritance_retains_words_but_refuses_applicability(self):
  target=C._apply_departures({'calendar':'roman-pre-1955','sections':{}},self.source,'roman-1962')
  self.assertNotIn(C.PROPER_APPOINTMENT_FACTS,target)
  rows=self.rows(COMMON,target)
  readings=[r['proper'] for r in rows if r['proper'].get('name') in ('Lesson','Epistle')]
  self.assertEqual([p['verses'][0]['ref'] for p in readings],['Proverbs 31:10-31','1 Timothy 5:3-10'])
  self.assertTrue(all(p[C.APPOINTMENT_APPLICABILITY]['source_edition']=='roman-1962' for p in readings))
  with self.assertRaisesRegex(TODAY.Refused,'foreign-source'):
   self.execute(COMMON,'principal',source=target)

 def test_only_fact_and_two_common_annotations_change_against_source_baseline(self):
  if not os.environ.get('TRIPTYCH_MASS_VALUES_BASELINE'):return
  before=C.read_yaml(Path(os.environ['TRIPTYCH_MASS_VALUES_BASELINE']));normalized=copy.deepcopy(self.source)
  normalized[C.PROPER_APPOINTMENT_FACTS].pop(FACT)
  for proper in C.mass_index(normalized)[COMMON]['propers']:
   if proper.get('ordinary_disposition',{}).get('group')==GROUP:proper.pop('ordinary_disposition')
  self.assertEqual(normalized,before)
  for key in CONTROLS:self.assertEqual(self.index[key],C.mass_index(before)[key])

if __name__=='__main__':unittest.main()
