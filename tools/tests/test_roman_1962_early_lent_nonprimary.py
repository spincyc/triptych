"""Image-collated normal early-Lent appointments, not whole-Missal completeness.

The controlling CMAA 1962 PDF has SHA256
648fdb8fe830ed65a08aa4a95de6f94424c533ddf2398c8fc26b18735fd3518a.
The fixture records source unit/page facts independently of the calendar index.
The before-Mass ashes rite, eight separately collated Ember Saturday Oratio
nodes and selected-candidate Tract eligibility are outside these repair hunks.
"""
from __future__ import annotations
import collections,copy,importlib.machinery,importlib.util,sys,tomllib,unittest
from pathlib import Path
import yaml
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'scripts'))
from _calendars import resolve_propers
DATA=ROOT/'src/sources/calendars/roman-1962/propers.yaml'
ENGLISH=ROOT/'src/sources/inventories/roman-1962-proper-translations-v1.toml'

# mass, source-owned name, printed marginal unit, artifact page, printed page.
NEW_APPOINTMENTS=[('ash-wednesday', 'Oratio super populum', 396, 139, 58),
 ('thursday-after-ash-wednesday', 'Oratio super populum', 406, 141, 60),
 ('friday-after-ash-wednesday', 'Oratio super populum', 417, 143, 62),
 ('saturday-after-ash-wednesday', 'Oratio super populum', 427, 144, 63),
 ('lent-1-monday', 'Oratio super populum', 448, 147, 66),
 ('lent-1-ember-wednesday', 'Oratio', 463, 149, 68),
 ('lent-1-ember-wednesday', 'Oratio super populum', 471, 151, 70),
 ('lent-1-thursday', 'Oratio super populum', 481, 152, 71),
 ('lent-1-ember-friday', 'Oratio super populum', 492, 154, 73),
 ('lent-2-monday', 'Oratio super populum', 551, 163, 82),
 ('lent-2-tuesday', 'Oratio super populum', 561, 164, 83),
 ('lent-2-wednesday', 'Oratio super populum', 572, 166, 85),
 ('lent-2-thursday', 'Oratio super populum', 582, 167, 86),
 ('lent-2-friday', 'Oratio super populum', 593, 169, 88),
 ('lent-2-saturday', 'Oratio super populum', 603, 172, 91),
 ('lent-3-monday', 'Oratio super populum', 624, 175, 94),
 ('lent-3-tuesday', 'Oratio super populum', 634, 177, 96),
 ('lent-3-wednesday', 'Oratio super populum', 645, 179, 98),
 ('lent-3-thursday', 'Oratio super populum', 655, 180, 99),
 ('lent-3-friday', 'Oratio super populum', 666, 182, 101),
 ('lent-3-saturday', 'Oratio super populum', 676, 185, 104)]
# mass, form, proper, printed numerical appointments, marginal source unit.
CITATION_REPAIRS=[('quinquagesima', 'main', 'Tract', ['Psalm 99:2-3'], 370),
 ('lent-1-ember-wednesday', 'main', 'Introit', ['Psalm 24:6, 3, 22', 'Psalm 24:1-2'], 459),
 ('lent-1-thursday', 'main', 'Introit', ['Psalm 95:6', 'Psalm 95:1'], 472),
 ('lent-1-ember-saturday', 'longer', 'Third Gradual', ['Psalm 89:13, 1'], 502),
 ('lent-2-monday', 'main', 'Introit', ['Psalm 25:11-12', 'Psalm 25:1'], 541),
 ('lent-2-tuesday', 'main', 'Introit', ['Psalm 26:8-9', 'Psalm 26:1'], 552),
 ('lent-2-thursday', 'main', 'Introit', ['Psalm 69:2-3', 'Psalm 69:4'], 573),
 ('lent-2-saturday', 'main', 'Introit', ['Psalm 18:8', 'Psalm 18:2'], 594),
 ('lent-3-monday', 'main', 'Introit', ['Psalm 55:5', 'Psalm 55:2'], 614),
 ('lent-3-tuesday', 'main', 'Introit', ['Psalm 16:6, 8', 'Psalm 16:1'], 625),
 ('lent-3-wednesday', 'main', 'Introit', ['Psalm 30:7-8', 'Psalm 30:2'], 635),
 ('lent-3-friday', 'main', 'Introit', ['Psalm 85:17', 'Psalm 85:1'], 656),
 ('lent-3-saturday', 'main', 'Introit', ['Psalm 5:2-3', 'Psalm 5:4'], 667)]
FRAME_MASSES=['ash-wednesday',
 'friday-after-ash-wednesday',
 'lent-1-ember-friday',
 'lent-1-monday',
 'lent-1-thursday',
 'lent-2-friday',
 'lent-2-monday',
 'lent-2-saturday',
 'lent-2-thursday',
 'lent-2-tuesday',
 'lent-2-wednesday',
 'lent-3-friday',
 'lent-3-monday',
 'lent-3-saturday',
 'lent-3-thursday',
 'lent-3-tuesday',
 'lent-3-wednesday',
 'saturday-after-ash-wednesday',
 'thursday-after-ash-wednesday']
MIXED=[('lent-1-ember-saturday','longer','Hymn (Benedictus es)',508),
       ('lent-3-thursday','main','Introit',646)]
# Latin-body admissions rewrote these notes with the same unit/page facts: 1f1be432b (phase5-latin22) for the
# first eight, eeab39fef for the rest; see src/sources/inventories/roman-1962-proper-latin-provenance-v1.toml.
PHASE5_NOTES={(key,name) for key,name,*_ in NEW_APPOINTMENTS[:8]}
def locator_phrases(key,name,unit,pdf,printed):
 if (key,name) in PHASE5_NOTES:return (f'1962 target PDF {pdf} / printed {printed};',f'; unit {unit}')
 return (f'Proprium de tempore, printed p. {printed}, PDF p. {pdf}, unit {unit},',)
# Every NEW_APPOINTMENTS prayer's no-exemplar absence became one confirmed Lasance 1945 entry (c6c0fefcf, 290629ed5,
# eeab39fef, 3cd51e852; [[accepted]] in src/sources/inventories/roman-1962-english-recovery-2026-10-23.toml).

def owning_tool(name):
 loader=importlib.machinery.SourceFileLoader('early_lent_'+name,str(ROOT/'tools'/name))
 spec=importlib.util.spec_from_loader(loader.name,loader)
 module=importlib.util.module_from_spec(spec);loader.exec_module(module);return module

def masses(document):
 return {m['key']:m for section in document['sections'].values() for m in section['masses']}

def source_propers(document,key,fid='main'):
 mass=masses(document)[key]
 label='' if fid=='main' else next(f['name'] for f in mass['forms'] if f['id']==fid)
 rows,problems=resolve_propers(document,mass)
 if problems:raise AssertionError(problems)
 return [p for form,p,origin in rows if form==label]

def appointment_problems(document):
 problems=[];citations=owning_tool('citations')
 for key,name,unit,pdf,printed in NEW_APPOINTMENTS:
  rows=source_propers(document,key);matches=[p for p in rows if p['name']==name]
  if len(matches)!=1:problems.append((key,name,'source appointment'));continue
  proper=matches[0];names=[p['name'] for p in rows];at=names.index(name)
  wanted=['First Gradual','Oratio','Second Lesson'] if name=='Oratio' else ['Postcommunion','Oratio super populum']
  actual=names[at-1:at+2] if name=='Oratio' else names[-2:]
  if actual!=wanted:problems.append((key,name,'source order'))
  for phrase in locator_phrases(key,name,unit,pdf,printed):
   if phrase not in proper.get('notes',''):problems.append((key,name,'source locator'))
 for key,fid,name,refs,unit in CITATION_REPAIRS:
  proper=next(p for p in source_propers(document,key,fid) if p['name']==name)
  if proper.get('verses')!=[citations.parse_citation(ref) for ref in refs]:problems.append((key,name,'source citation'))
 return problems

class EarlyLentNonprimary(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.document=yaml.safe_load(DATA.read_text());cls.english=tomllib.loads(ENGLISH.read_text())
 def test_exact_source_appointments_positions_pages_and_citations(self):
  self.assertEqual(appointment_problems(self.document),[])
 def test_new_prayers_and_uncited_chant_constituents_have_real_body_dispositions(self):
  schema=owning_tool('check-calendar-masses')
  targets=[(key,'main',name) for key,name,*_ in NEW_APPOINTMENTS]+[(key,fid,name) for key,fid,name,_ in MIXED]
  for key,fid,name in targets:
   with self.subTest(mass=key,proper=name):
    proper=next(p for p in source_propers(self.document,key,fid) if p['name']==name)
    self.assertNotIn('takes_from',proper)
    problems=[];schema.check_proper(key,proper,problems,calendar='roman-1962',season='lent');self.assertEqual(problems,[])
    self.assertTrue(proper.get('text') or proper.get('text_status',{}).get('state')=='unavailable')
  for key,fid,name,unit in MIXED:
   self.assertEqual(next(p for p in source_propers(self.document,key,fid) if p['name']==name)['source'],'mixed')
 def test_exact_shared_english_whole_body_dispositions(self):
  received={(key,'main',name) for key,name,*_ in NEW_APPOINTMENTS};expected=received|{(key,fid,name) for key,fid,name,_ in MIXED}
  for key,fid,name in expected:
   matches=[r for r in self.english['untranslated'] if (r['mass'],r.get('form_id','main'),r['proper'],r.get('occurrence',1),r.get('cycle','all'),r['lang'],r['extent'])==(key,fid,name,1,'all','en','body')]
   entries=[r for r in self.english['entries'] if (r['mass'],r.get('form_id','main'),r['proper'],r.get('occurrence',1),r.get('cycle','all'))==(key,fid,name,1,'all')]
   if (key,fid,name) in received:
    self.assertEqual((matches,len(entries)),([],1),(key,fid,name))
    self.assertEqual(([t['lang'] for t in entries[0]['translations']],entries[0]['witness'],entries[0]['collation_result']),(['en'],'lasance-1945','confirmed'),(key,fid,name));continue
   self.assertEqual(entries,[],(key,fid,name))
   self.assertEqual(len(matches),1,(key,fid,name));self.assertEqual(matches[0]['reason'],{'kind':'no-exemplar'})
 def test_generic_frames_are_explicitly_unavailable_and_specialized_frames_remain(self):
  for key in FRAME_MASSES+['lent-1-ember-saturday','lent-1-ember-wednesday']:
   frame=masses(self.document)[key]['ordinary_frame'];self.assertEqual(frame['applicability'],'unavailable');self.assertTrue(frame['basis'])
 def test_omission_and_plausible_wrong_citation_are_detected(self):
  omitted=copy.deepcopy(self.document);mass=masses(omitted)['ash-wednesday'];mass['propers']=[p for p in mass['propers'] if p['name']!='Oratio super populum']
  self.assertIn(('ash-wednesday','Oratio super populum','source appointment'),appointment_problems(omitted))
  changed=copy.deepcopy(self.document);proper=next(p for p in masses(changed)['quinquagesima']['propers'] if p['name']=='Tract')
  proper['verses']=[owning_tool('citations').parse_citation('Psalm 99:1-2')]
  self.assertIn(('quinquagesima','Tract','source citation'),appointment_problems(changed))

if __name__=='__main__':unittest.main()
