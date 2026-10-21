"""Typed territorial requests must name a branch the canonical day holds."""
import json
import subprocess
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SCRIPT = r'''
const assert = require('node:assert/strict');
const fs = require('node:fs'), path = require('node:path');
const root = process.argv[1];
const C = require(path.join(root,'src/web/browser/liturgy/reader-state.js'));
const A = require(path.join(root,'src/web/browser/liturgy/reader-state-adapters.js'));
const M = require(path.join(root,'src/web/browser/liturgy/assembly-model.js'));
const read = p => JSON.parse(fs.readFileSync(path.join(root,'src/web/data/structure',p),'utf8'));
function sample(calendar,date) {
 const derived=M.derive({date,year:read('calendar/'+calendar+'/'+date.slice(0,4)+'.json'),rubrics:read('rubrics/'+calendar+'.json')});
 const request={schema:C.STATE_SCHEMA,entrance:'day',civilDate:date,
  edition:{id:calendar},calendar:{id:calendar},requestedMode:'read',
  bible:{id:'douay-rheims',numbering:'vulgate'},languages:{orations:'en'},
  options:{ordinary:false,legitimate:{}},coverage:[],unresolvedChoices:[],sourceHooks:[]};
 return {derived,request,structure:read('propers/'+calendar+'.json'),ordinary:null};
}
const tlm=sample('roman-1962','2026-08-02');
assert.equal(tlm.derived.options.length,1);assert.equal(tlm.derived.options[0].option,null);
const normal=A.adaptDay(tlm);assert(normal.resolved);
const explicitNull={...tlm,request:{...tlm.request,calendar:{...tlm.request.calendar,territory:null}}};
assert(C.validateReaderState(explicitNull.request).ok);
assert.deepEqual(A.adaptDay(explicitNull),{...normal,request:explicitNull.request});
for(const id of ['ascension-transferred-to-sunday','not-a-held-territory']) {
 const unsupported={...tlm,request:{...tlm.request,calendar:{...tlm.request.calendar,territory:{id}}}};
 assert(C.validateReaderState(unsupported.request).ok);
 assert.throws(()=>A.adaptDay(unsupported),/requested territorial Day branch is not held/);
}
const no=sample('postconciliar','2026-05-14');
const untouched=JSON.stringify(no.derived);
const open=A.adaptDay(no);assert.equal(open.resolved,null);
assert.deepEqual(open.unresolvedChoices.find(c=>c.id==='calendar-territory').options.map(o=>o.id),no.derived.options.map(b=>b.option));
for(const branch of no.derived.options) {
 const selected={...no,request:{...no.request,calendar:{...no.request.calendar,territory:{id:branch.option}}}};
 const result=A.adaptDay(selected);
 assert(result.resolved);assert.equal(result.calendarResult.territory,branch.option);
}
assert.equal(JSON.stringify(no.derived),untouched);
const bogus={...no,request:{...no.request,calendar:{...no.request.calendar,territory:{id:'not-a-held-territory'}}}};
assert.throws(()=>A.adaptDay(bogus),/requested territorial Day branch is not held/);
console.log(JSON.stringify({groups:5,unsupportedTypedRequestsRefused:3,supportedNobranches:no.derived.options.length,nullDefaultUnchanged:true,sourceUnchanged:true}));
'''

class TerritorialAdmissionTests(unittest.TestCase):
    def test_explicit_territory_cannot_fall_back_to_unqualified_branch(self):
        result = subprocess.run(['/usr/bin/node', '-e', SCRIPT, str(ROOT)],
                                cwd=ROOT, capture_output=True, text=True, check=False)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stderr, '')
        report = json.loads(result.stdout)
        self.assertEqual(report['unsupportedTypedRequestsRefused'], 3)
        self.assertEqual(report['supportedNobranches'], 2)
        self.assertTrue(report['nullDefaultUnchanged'])
        self.assertTrue(report['sourceUnchanged'])
