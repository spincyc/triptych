"""Page-derived January-April source units and normal seasonal chant order."""
from pathlib import Path
import json
import subprocess
import sys
import tomllib
import unittest
import yaml

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'scripts'))
from _calendars import resolve_propers

POLYCARP = 's-polycarpi-episcopi-martyris'
TIMOTHY = 's-timothei-episcopi-martyris'
TITUS = 's-titi-episcopi-confessoris'
SORROWS = 'comm-septem-dolorum-beatae-mariae-virginis'
PAUL = 's-pauli-primi-eremitae-confessoris'


def bounds(proper):
    return [(v['book'], r['begin']['chapter'], r['begin']['verse'],
             r['end']['chapter'], r['end']['verse'])
            for v in proper.get('verses', []) for r in v['ranges']]


class JanuaryAprilAppointmentTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.document = yaml.safe_load((ROOT / 'src/sources/calendars/roman-1962/propers.yaml').read_text())
        cls.masses = {m['key']: m for s in cls.document['sections'].values() for m in s['masses']}
        cls.evidence = tomllib.loads((ROOT / 'src/sources/inventories/roman-1962-january-april-full-appointment-collation-v1.toml').read_text())
        cls.english = tomllib.loads((ROOT / 'src/sources/inventories/roman-1962-proper-translations-v1.toml').read_text())

    def proper(self, key, name):
        entries, problems = resolve_propers(self.document, self.masses[key], appointments=True)
        self.assertEqual(problems, [])
        found = [p for _, p, _ in entries if p['name'] == name]
        self.assertEqual(len(found), 1)
        return found[0]

    def test_every_printed_citation_constituent_retains_its_source_order(self):
        expected = {
            (PAUL, 'Gradual'): [('Psalms', 91, 13, 91, 13), ('Psalms', 91, 14, 91, 14), ('Psalms', 91, 3, 91, 3)],
            (POLYCARP, 'Introit'): [('Daniel', 3, 84, 3, 84), ('Daniel', 3, 87, 3, 87), ('Daniel', 3, 57, 3, 57)],
            (TITUS, 'Gradual'): [('Sirach', 44, 16, 44, 16), ('Sirach', 44, 20, 44, 20)],
        }
        for (key, name), wanted in expected.items():
            with self.subTest(mass=key, proper=name):
                self.assertEqual(bounds(self.proper(key, name)), wanted)

    def test_the_uncited_alleluia_is_a_real_own_appointment(self):
        proper = self.proper(POLYCARP, 'Alleluia')
        self.assertEqual(proper['source'], 'composed')
        self.assertNotIn('verses', proper)
        if not proper.get('text'):
            self.assertEqual(proper['text_status']['scope'], 'proper-body')
            self.assertEqual(proper['text_status']['state'], 'unavailable')
        source = [r for r in self.evidence['appointments'] if (r['mass'], r['proper']) == (POLYCARP, 'Alleluia')]
        self.assertEqual([(r['pdf_page'], r['printed_page'], r['column'], r['marginal_number']) for r in source], [(537, 456, 'right', 2030)])
        self.assertNotIn('printed_reference', source[0])

    def test_the_virgin_addressed_offertory_preserves_its_literal_body_identity(self):
        proper = self.proper(SORROWS, 'Offertory')
        self.assertEqual(proper['source'], 'mixed')
        self.assertEqual(bounds(proper), [('Jeremiah', 18, 20, 18, 20)])
        if not proper.get('text'):
            self.assertEqual(proper['text_status']['scope'], 'proper-body')
            self.assertEqual(proper['text_status']['state'], 'unavailable')

    def test_literal_targets_have_one_exact_whole_english_disposition(self):
        for key, name in [(POLYCARP, 'Alleluia'), (SORROWS, 'Offertory')]:
            with self.subTest(mass=key, proper=name):
                target = (key, 'main', name, 'all', 1)
                same = lambda r: (r.get('mass'), r.get('form_id', 'main'), r.get('proper'), r.get('cycle', 'all'), r.get('occurrence', 1)) == target
                positive = [r for r in self.english.get('entries', []) if same(r)]
                absent = [r for r in self.english.get('untranslated', []) if same(r) and r.get('lang') == 'en' and r.get('extent') == 'body']
                self.assertEqual(len(positive) + len(absent), 1)
                if absent:
                    self.assertEqual(absent[0]['reason'], {'kind': 'no-exemplar'})
                    self.assertEqual(absent[0]['availability'], 'unavailable')

    def test_normal_chant_choice_has_source_order_and_rejects_incompatible_context(self):
        payload = {'calendar': 'roman-1962', 'facts': self.document['proper_appointment_facts'], 'masses': {}}
        for key in [POLYCARP, TIMOTHY, TITUS]:
            rows, problems = resolve_propers(self.document, self.masses[key], appointments=True)
            self.assertEqual(problems, [])
            payload['masses'][key] = [p | {'form_id': form or 'main'} for form, p, _ in rows]
        script = r'''
const fs=require('fs'),assert=require('assert'),api=require(process.argv[1]);
const input=JSON.parse(fs.readFileSync(0,'utf8'));let checks=0;
const prepare=(rows,season,choices={})=>api.prepareProperAppointments(rows,{calendar:'roman-1962',entrance:season?'day':'propers',date:season?'2026-01-24':null,season:season||null,facts:input.facts,choices});
const flatten=p=>api.properUnits(p.rows,null,()=>false,p.selections).flatMap(u=>u.kind==='proper_choice'?u.options.filter(o=>u.selection.option===o.id).flatMap(o=>o.rows.map(r=>r.proper.name)):[u.proper.name]);
for(const [key,group,reading]of[["s-polycarpi-episcopi-martyris","polycarp-post-epistle","Epistle"],["s-timothei-episcopi-martyris","timothy-post-epistle","Epistle"],["s-titi-episcopi-confessoris","titus-post-epistle","Lesson"]]){
const rows=input.masses[key],id='main/'+group,expected=choice=>['Introit','Collect',reading,'Gradual',choice,'Gospel','Offertory','Secret','Communion','Postcommunion'];
assert.deepStrictEqual(flatten(prepare(rows,'epiphanytide')),expected('Alleluia'));checks++;
assert.deepStrictEqual(flatten(prepare(rows,'lent')),expected('Tract'));checks++;
assert.throws(()=>prepare(rows,'epiphanytide',{[id]:'tract'}),/contradicts source applicability/);checks++;
assert.deepStrictEqual(prepare(rows,null).selections[id],{state:'required',option:null});checks++;
assert.deepStrictEqual(flatten(prepare(rows,null,{[id]:'regular'})),expected('Alleluia'));checks++;
assert.throws(()=>prepare(rows,'paschaltide'),/appoints no Proper option/);checks++;
assert.throws(()=>prepare(rows,null,{[id]:'paschal-votive'}),/not held/);checks++;
}console.log(checks);
'''
        result = subprocess.run(['node', '-e', script, str(ROOT / 'src/web/browser/liturgy/ordinary-seating.js')], input=json.dumps(payload), text=True, capture_output=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout.strip(), '21')

    def test_the_source_denominator_counts_physical_units_and_referrals_separately(self):
        rows = self.evidence['appointments']
        self.assertEqual(len(rows), 139)
        self.assertEqual(len({(r['mass'], r['form_id'], r['proper'], r['occurrence']) for r in rows}), 139)
        self.assertEqual(len({r['mass'] for r in rows}), 24)
        self.assertEqual(sum(r['proper'] in ['Lesson', 'Epistle', 'Gospel'] for r in rows), 18)
        self.assertEqual(len(self.evidence['referrals']), 15)
        self.assertEqual(self.evidence['covered_source_addresses'], 154)
        self.assertEqual(self.evidence['unchecked_source_addresses'], 0)


if __name__ == '__main__':
    unittest.main()
