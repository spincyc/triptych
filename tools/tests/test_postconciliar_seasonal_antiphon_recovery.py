"""Preserve source-backed antiphon seats, numbering, conditions and body gaps."""
from pathlib import Path
from importlib.machinery import SourceFileLoader
from importlib.util import module_from_spec,spec_from_loader
from collections import Counter
import copy,hashlib,json,sys,tomllib,unittest,yaml
sys.path.insert(0, str(Path(__file__).resolve().parent))
from _product_data import browser_data_root

ROOT=Path(__file__).resolve().parents[2]
SOURCE=ROOT/'src/sources/calendars/postconciliar/propers.yaml'
EVIDENCE=ROOT/'src/sources/inventories/postconciliar-seasonal-collation-v1.toml'
ENGLISH=ROOT/'src/sources/inventories/postconciliar-proper-translations-v1.toml'
ART='artifact.catholic-church.missale-romanum.2010-english-icel-antiphonary.antiphonary-pdf'
TARGET='edition.catholic-church.missale-romanum.vatican-typica-tertia-reimpressio-emendata-2008'
# Gap campaign 2026-11-14 admissions, read from their owning ledgers rather than retyped here.
_PROV=tomllib.loads((ROOT/'src/sources/inventories/postconciliar-proper-latin-provenance-v1.toml').read_text())['entries']
# Every later admission the Latin ledger permits (the 2026-11-14 Easter Thursday Communio projection and the gap campaign) holds a body.
GAP_LATIN={(r['mass'],r['proper']) for r in _PROV if r.get('publication_status')=='permitted'}
GAP_ENGLISH={(e['mass'],e['proper'],e.get('occurrence',1)) for e in tomllib.loads(ENGLISH.read_text())['entries'] if 'integrate lane' in str(e.get('witness_note',''))+str(e.get('divergence',''))}
def tool(name):
 loader=SourceFileLoader('_seasonal_recovery_test_'+name.replace('-','_'),str(ROOT/'tools'/name));m=module_from_spec(spec_from_loader(loader.name,loader));sys.modules[loader.name]=m;loader.exec_module(m);return m
class SeasonalAntiphonRecoveryTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.document=yaml.safe_load(SOURCE.read_text());cls.masses={m['key']:m for s in cls.document['sections'].values() for m in s['masses']};cls.evidence=tomllib.loads(EVIDENCE.read_text())['seasonal_antiphon_recovery_2026_10_21'];cls.english=tomllib.loads(ENGLISH.read_text())['untranslated'];cls.check=tool('check-calendar-masses');cls.canon=tool('citations');cls.owner=tool('mass-propers');cls.ordinary=tool('mass-ordinary');cls.frame=json.loads((browser_data_root(ROOT) / 'structure/ordinary/postconciliar.json').read_text())
 def test_exact_source_cues_and_positions_bind_all_213_provisions(self):
  facts=self.evidence['rows'];self.assertEqual(len(facts),213);self.assertEqual(len({r['mass'] for r in facts}),106)
  self.assertEqual(Counter(r['proper'] for r in facts),Counter({'Entrance Antiphon':107,'Communion Antiphon':106}))
  for f in facts:
   with self.subTest(mass=f['mass'],proper=f['proper'],occurrence=f['occurrence']):
    mass=self.masses[f['mass']];rows=[p for p in mass['propers'] if p['name']==f['proper']];p=rows[f['occurrence']-1]
    self.assertEqual(self.owner.source_slot_identity(self.document,mass,'',p,None),(f['mass'],'main',f['proper'],f['occurrence']))
    self.assertIn(f"artifact page {f['artifact_page']} / printed page {f['printed_page']}",p['notes'])
    self.assertNotIn('incipit',p);self.assertNotIn('translations',p)
    key=(f['mass'],f['proper']);latin=key in GAP_LATIN;english=(*key,f['occurrence']) in GAP_ENGLISH
    if latin:self.assertIsInstance(p['text'],str);self.assertNotIn('text_status',p)
    else:self.assertNotIn('text',p)
    cue=f['source_citation_cue']
    if cue=='!uncited':
     self.assertEqual(p['source'],'composed');self.assertNotIn('verses',p)
     if not latin:self.assertEqual(p['text_status'],{'state':'unavailable','scope':'proper-body','reasons':[{'kind':'witness-gap','source_id':TARGET}]})
    else:
     expected=[self.canon.parse_citation(c.strip()) for c in cue.removeprefix('Cf. ').split(';;')]
     # A gap-campaign admission gives the adapted antiphon its own body beside the retained citation.
     self.assertEqual(p['source'],'mixed' if (latin or english) else 'scripture');self.assertEqual(p['verses'],expected)
     if english and not latin:self.assertEqual(p['text_status'],{'state':'unavailable','scope':'proper-body','reasons':[{'kind':'witness-gap','source_id':TARGET}]})
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
 def test_uncited_english_exemplars_retain_their_original_restrictions_and_current_sources(self):
  key_fields = ('mass', 'form_id', 'proper', 'cycle', 'occurrence', 'lang', 'extent')
  def identity(row):
   return tuple(row[field] for field in key_fields)

  receipt = Path(__file__).parent / 'fixtures/postconciliar-seasonal-uncited-20261021.json'
  raw = receipt.read_bytes()
  self.assertEqual(hashlib.sha256(raw).hexdigest(), '9457848b559edaf973e4ac2c1ddfcfce118bc86e9ada32e041081f97885617a9')
  historical = {identity(r): r for r in json.loads(raw)['untranslated']}
  facts = [f for f in self.evidence['rows'] if f['source_citation_cue'] == '!uncited']
  facts = {(f['mass'], f['form_id'], f['proper'], 'all', f['occurrence'], 'en', 'body'): f for f in facts}
  self.assertEqual(set(historical), set(facts))
  self.assertEqual(len(facts), 11)
  english = tomllib.loads(ENGLISH.read_text())
  absences = {identity(r): r for r in english['untranslated']}
  positives = {(r['mass'], r.get('form_id', 'main'), r['proper'], r.get('cycle', 'all'),
                r.get('occurrence', 1), t['lang'], 'body'): (r, t)
               for r in english['entries'] for t in r.get('translations', [])}
  sources, problems = self.owner._source_library_records(ROOT / 'src/sources/calendars')
  self.assertEqual(problems, [])
  self.assertEqual((sources[ART]['rights_status'], sources[ART]['sha256']),
                   ('restricted', self.evidence['witness_sha256']))
  advent_december_18 = (
   'public-domain', 'antecedent-printing',
   'passage.catholic-church.breviarium-romanum.blackwood-bute-winter-1908.english-completion-20261029-postconciliar-phase2-otherseasonal-advent-december-18-main-entrance-antiphon-all-1-publication',
   'ec64c42d9e7813a54eab3ca00a4b3a8db47ae3ae736306ee541f237bec2d3c89',
  )
  advent_1_friday = (
   'project-created', 'abridged',
   'passage.catholic-church.breviarium-romanum.pustet-ratisbon-pars-hiemalis-1888.english-completion-20261029-postconciliar-phase2-otherseasonal-ecce-dominus-ninth-responsory-source',
   'aa4b07dfda8976668996210cdbb6b3021d621366bf2518f0b167001d33f7572f',
  )
  lent_3_thursday = (
   'public-domain', 'antecedent-printing',
   'passage.francis-xavier-lasance.the-new-roman-missal.benziger-revised-1945.english-completion-20261029-postconciliar-phase2-otherseasonal-lent-3-thursday-main-entrance-antiphon-all-1-publication',
   '5b168c961ec155c57ff09ecfacf3e9a35f19bb5d711954ae481ff9ca82102d2b',
  )
  easter_3_monday = (
   'project-created', 'abridged',
   'passage.catholic-church.breviarium-romanum.pustet-ratisbon-pars-verna-1888.gap-campaign-20261114-easter-pentecost-easter-3-monday-main-entrance-antiphon-1-study-source',
   '42a5f631b719930a54bbd6d299879cef16cfbccced3bee2b1a2241bb3901abfb',
  )
  easter_3_wednesday = (
   'project-created', 'variant',
   'passage.catholic-church.missale-romanum.pustet-ratisbon-1862.english-completion-20261029-postconciliar-phase2-late-easter-easter-5-wednesday-communion-historical-text',
   'ea518a19a0d2575defe641dde3d2929ff5e4df02e6ce7b8dee8de82b84b3dbea',
  )
  easter_3_friday = (
   'project-created', 'abridged',
   'passage.catholic-church.english-completion-20261029-postconciliar-phase2-late-easter-commemoratio-et-suffragia-sanctorum.mexico-1815.english-completion-20261029-postconciliar-phase2-late-easter-easter-5-friday-communion-historical-text',
   '3946e0fe404b1c217d46ce397e337ec69334c48a8aeb33a7627ea044eb81da94',
  )
  easter_5_monday = (
   'project-created', 'abridged',
   'passage.catholic-church.breviarium-romanum.pustet-ratisbon-pars-verna-1888.gap-campaign-20261114-easter-pentecost-easter-5-monday-main-entrance-antiphon-1-study-source',
   '42a5f631b719930a54bbd6d299879cef16cfbccced3bee2b1a2241bb3901abfb',
  )
  expected = {
   'advent-december-18': advent_december_18,
   'advent-1-friday': advent_1_friday,
   'advent-2-friday': advent_1_friday,
   'lent-3-thursday': lent_3_thursday,
   'easter-3-monday': easter_3_monday,
   'easter-3-wednesday': easter_3_wednesday,
   'easter-3-friday': easter_3_friday,
   'easter-5-monday': easter_5_monday,
   'easter-5-wednesday': easter_3_wednesday,
   'easter-5-friday': easter_3_friday,
  }
  self.assertEqual(set(expected), {k[0] for k in facts} - {'easter-monday'})
  for key, old in historical.items():
   with self.subTest(target=key):
    fact = facts[key]
    self.assertEqual((old['availability'], old['witness_artifact_id'], old['verified_artifact_page'],
                      old['verified_printed_page']), ('unavailable', ART, fact['artifact_page'], fact['printed_page']))
    self.assertEqual(old['reason'], {'kind': 'rights-withheld', 'source_id': ART,
                                     'surfaces': ['site-display', 'corpus-data', 'public-git', 'command-line', 'download']})
    self.assertEqual(self.check.untranslated_witness_problems('original uncited appointment', old), [])
    self.assertNotIn('text', old)
    self.assertNotIn('quarantined_text_sha256', old)
    if key[0] == 'easter-monday':
     self.assertEqual(key[2:5], ('Entrance Antiphon', 'all', 2))
     self.assertEqual(absences[key], old)
     self.assertNotIn(key, positives)
     continue
    self.assertNotIn(key, absences)
    record, translation = positives[key]
    rights, relation, passage, digest = expected[key[0]]
    self.assertEqual((translation['rights'], record['relation']), (rights, relation))
    self.assertEqual(hashlib.sha256(translation['text'].encode()).hexdigest(), digest)
    if rights == 'public-domain':
     self.assertEqual(record['publication_passage_id'], passage)
     artifact = record['publication_artifact_id']
     self.assertEqual(sources[passage]['edition_id'], translation['source_id'])
     self.assertEqual(sources[artifact]['sha256'], record['publication_artifact_sha256'])
    else:
     self.assertEqual(record['ancient_passage_id'], passage)
     self.assertNotIn('source_id', translation)
     artifact = record['witness_artifact_id']
     self.assertEqual(sources[passage]['edition_id'], record['witness_edition_id'])
    self.assertEqual(sources[passage]['artifact_id'], artifact)
    self.assertNotEqual(artifact, ART)
 def test_recovery_does_not_select_unproved_formularies_or_erase_existing_repairs(self):
  selected={r['mass'] for r in self.evidence['rows']}
  self.assertFalse(any(k.startswith('christmas-january-') for k in selected));self.assertTrue(selected.isdisjoint({'blessed-virgin-mary-mother-church','good-friday','lent-5','easter-6-wednesday','easter-6-thursday','easter-7-saturday'}))
  self.assertEqual([p['name'] for p in self.masses['lent-5-monday']['propers'] if p['name'].endswith('Antiphon')],['Entrance Antiphon'])
  for key,ref in [('easter-7','Psalm 26:7-9'),('corpus-christi','Psalm 80:17')]:
   p=next(p for p in self.masses[key]['propers'] if p['name']=='Entrance Antiphon');self.assertEqual(p['psalm_numbering'],'vulgate');self.assertEqual(p['verses'][0]['ref'],ref)
  self.assertTrue(any(v['ref']=='John 6:54' for p in self.masses['ot-21']['propers'] if p['name'].startswith('Communion Antiphon') for v in p.get('verses',[])))
  self.assertEqual(self.document['psalm_numbering'],'hebrew')
if __name__=='__main__':unittest.main()
