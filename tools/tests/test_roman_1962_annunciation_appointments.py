"""Annunciation source course, CMAA 576/495, numbered units 2326-2328."""
from __future__ import annotations

import copy
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tomllib
import unittest

import yaml

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'scripts'))
from _calendars import resolve_propers

DATA = ROOT / 'src/sources/calendars/roman-1962/propers.yaml'
TRANSLATIONS = ROOT / 'src/sources/inventories/roman-1962-proper-translations-v1.toml'
SEATING = ROOT / 'src/web/browser/liturgy/ordinary-seating.js'
MASS = 'annuntiatio-beatae-mariae-virginis'
FACT = 'roman-1962-common-chant-regime'
NAMES = ['Introit','Collect','Lesson','Gradual','Tract','Alleluia','Gospel',
         'Offertory','Secret','Communion','Postcommunion']


class Roman1962AnnunciationAppointmentTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.document = yaml.safe_load(DATA.read_text())
        cls.mass = next(m for s in cls.document['sections'].values() for m in s['masses']
                        if m['key']==MASS)
        cls.entries, cls.problems = resolve_propers(cls.document, cls.mass, appointments=True)
        cls.propers = {p['name']:p for _,p,_ in cls.entries}
        cls.translations = tomllib.loads(TRANSLATIONS.read_text())

    def test_direct_source_order_and_unchanged_reading_neighbors(self):
        self.assertEqual(self.problems, [])
        self.assertEqual([p['name'] for _,p,_ in self.entries], NAMES)
        self.assertTrue(all(origin is None for _,_,origin in self.entries))
        self.assertEqual(self.propers['Lesson']['verses'][0]['ref'], 'Isaiah 7:10-15')
        self.assertEqual(self.propers['Gospel']['verses'][0]['ref'], 'Luke 1:26-38')
        self.assertNotIn('takes_from',self.mass)

    def test_printed_tract_reference_is_13_then_10_not_3(self):
        ranges = self.propers['Tract']['verses'][0]
        self.assertEqual(ranges['book'],'Psalms')
        self.assertEqual([(r['begin']['chapter'],r['begin']['verse'],
                           r['end']['chapter'],r['end']['verse']) for r in ranges['ranges']],
                         [(44,11,44,12),(44,13,44,13),(44,10,44,10),(44,15,44,16)])
        self.assertEqual(self.propers['Gradual']['verses'][0]['ref'],'Psalms 44:3, 5')
        self.assertEqual(self.propers['Alleluia']['verses'][0]['ref'],'Luke 1:28')
        self.assertEqual(len(self.propers['Alleluia']['verses']),1)

    def test_exact_own_anchor_and_source_qualified_conditions(self):
        gradual = self.propers['Gradual']['ordinary_disposition']
        tract = self.propers['Tract']['ordinary_disposition']
        alleluia = self.propers['Alleluia']['ordinary_disposition']
        self.assertEqual(gradual['kind'],'conditional')
        self.assertEqual(gradual['when'],{'fact':FACT,'in':['advent','regular','tract']})
        self.assertEqual(tract['when'],gradual['when'])
        self.assertEqual(alleluia['when'],{'fact':FACT,'in':['paschal']})
        self.assertEqual((tract['kind'],tract['option']),('alternative','outside-paschal'))
        self.assertEqual((alleluia['kind'],alleluia['option']),('alternative','paschal'))
        self.assertEqual(tract['group'],alleluia['group'])
        anchor = {'mass':MASS,'form_id':'main','proper':'Tract','occurrence':1}
        self.assertEqual(tract['anchor'],anchor)
        self.assertEqual(alleluia['anchor'],anchor)
        self.assertEqual(gradual['basis'],tract['basis'])
        self.assertEqual(tract['basis'],alleluia['basis'])
        for locator in ('576','495','2326','2328'):
            self.assertIn(locator,tract['basis'])

    def test_mixed_alleluia_has_no_invented_whole_body_or_english_binding(self):
        proper = self.propers['Alleluia']
        self.assertEqual(proper['source'],'mixed')
        self.assertNotIn('text',proper)
        self.assertEqual(proper['text_status'],{
            'state':'unavailable','scope':'proper-body','reasons':[{'kind':'no-exemplar'}]})
        identity = {'mass':MASS,'form_id':'main','proper':'Alleluia','cycle':'all',
                    'occurrence':1,'lang':'en','extent':'body'}
        matches = [(section,row) for section in ('entries','untranslated')
                   for row in self.translations.get(section,[])
                   if all(row.get(k)==v for k,v in identity.items())]
        self.assertEqual(len(matches),1)
        section,row = matches[0]
        self.assertEqual(section,'untranslated')
        self.assertEqual(row['availability'],'unavailable')
        self.assertEqual(row['reason'],{'kind':'no-exemplar'})

    def test_exact_positive_binding_and_absence_cannot_coexist(self):
        identity = {'mass':MASS,'form_id':'main','proper':'Alleluia','cycle':'all',
                    'occurrence':1,'lang':'en','extent':'body'}
        mutated = copy.deepcopy(self.translations)
        positive = copy.deepcopy(mutated['entries'][0])
        positive.update(identity)
        mutated['entries'].append(positive)
        matches = [(section,row) for section in ('entries','untranslated')
                   for row in mutated.get(section,[])
                   if all(row.get(k)==v for k,v in identity.items())]
        self.assertEqual(len(matches),2)
        self.assertEqual({section for section,_ in matches},{'entries','untranslated'})
        # Run the actual real-ledger guard against the injected exact positive
        # binding plus absence; this must fail rather than ignoring entries.
        original = self.translations
        self.translations = mutated
        try:
            with self.assertRaises(AssertionError):
                self.test_mixed_alleluia_has_no_invented_whole_body_or_english_binding()
        finally:
            self.translations = original

    def test_owned_day_season_selects_one_course_and_refuses_incompatible_choice(self):
        node = shutil.which('node')
        if node is None:
            self.skipTest('node is not installed')
        public = []
        for _,proper,_ in self.entries:
            row = {k:v for k,v in proper.items() if k!='text'}
            identity = getattr(proper,'appointment_identity',None)
            if identity is not None:
                row['appointment_identity'] = identity
            public.append(row)
        probe = r'''
const fs=require('node:fs'),assert=require('node:assert/strict');
const S=require(process.argv[1]);const f=JSON.parse(fs.readFileSync(0,'utf8'));
const context={calendar:'roman-1962',facts:f.facts,entrance:'day'};
function execute(season,choices={}) {
 const p=S.prepareProperAppointments(f.propers,{...context,season,date:'2026-03-25',choices});
 const events=S.unframedEvents(p.rows,null,p.selections);
 const names=events.flatMap(e=>e.kind==='proper'?[e.proper.name]:
   e.selection.state==='selected'?e.options.find(o=>o.id===e.selection.option).rows.map(r=>r.proper.name):[]);
 return {p,names};
}
assert.deepEqual(execute('passiontide').names,
 ['Introit','Collect','Lesson','Gradual','Tract','Gospel','Offertory','Secret','Communion','Postcommunion']);
assert.deepEqual(execute('paschaltide').names,
 ['Introit','Collect','Lesson','Alleluia','Gospel','Offertory','Secret','Communion','Postcommunion']);
const unknown=S.prepareProperAppointments(f.propers,{calendar:'roman-1962',facts:f.facts,entrance:'propers'});
const group='main/'+f.propers.find(p=>p.name==='Tract').ordinary_disposition.group;
assert.equal(unknown.selections[group].state,'required');assert.equal(unknown.unresolved.length,1);
assert.throws(()=>execute('passiontide',{[group]:'paschal'}),/contradicts source applicability/);
assert.throws(()=>execute('paschaltide',{[group]:'outside-paschal'}),/contradicts source applicability/);
assert.throws(()=>S.prepareProperAppointments(f.propers,{...context,facts:{}}),/unheld/);
console.log(JSON.stringify({status:'pass'}));
'''
        completed = subprocess.run([node,'-e',probe,str(SEATING)],cwd=ROOT,
            input=json.dumps({'propers':public,'facts':self.document['proper_appointment_facts']}),
            capture_output=True,text=True,check=False)
        self.assertEqual(completed.returncode,0,completed.stdout+completed.stderr)
        self.assertEqual(json.loads(completed.stdout),{'status':'pass'})


if __name__=='__main__':
    unittest.main()
