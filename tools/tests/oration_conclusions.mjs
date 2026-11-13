import assert from 'node:assert/strict';
import crypto from 'node:crypto';
import fs from 'node:fs';
import path from 'node:path';
import vm from 'node:vm';
const root = path.resolve(process.argv[2]);
const input = JSON.parse(fs.readFileSync(0, 'utf8'));
let code = fs.readFileSync(root + '/src/web/browser/liturgy/oration-conclusions.js', 'utf8');
// A review run can exercise the exact proposed pin while tracked activation
// remains empty. This substitution exists only in this test VM, never the app.
if (code.includes("const ACTIVE_AUTHORITY_SHA256 = '';")) {
  assert.ok(code.includes('const GENERATED_AUTHORITY_SHA256 = ' + JSON.stringify(input.authority_sha256) + ';'));
  code = code.replace("const ACTIVE_AUTHORITY_SHA256 = '';", 'const ACTIVE_AUTHORITY_SHA256 = ' + JSON.stringify(input.authority_sha256) + ';');
}
const sandbox = {module: {exports: {}}, console};
vm.runInNewContext(code, sandbox);
const C = sandbox.module.exports, plain = value => JSON.parse(JSON.stringify(value));
assert.equal(C.ACTIVE_AUTHORITY_SHA256, input.authority_sha256);
assert.deepEqual(plain(C.PUBLIC_PINS), input.pins);
for (const value of ['', 'abc', 'Æ😀 conclusion.']) assert.equal(C.sha(value), crypto.createHash('sha256').update(value).digest('hex'));
input.cases.forEach((context, index) => assert.deepEqual(plain(C.executeGroup(context)), input.expected[index]));
let refusals = 0;
for (const context of input.cases) {
  for (const change of [
    c => { c.calendar = 'postconciliar'; },
    c => { c.rule = 'unsourced'; },
    c => { c.massCategory = 'votive'; },
    c => { c.groups[0].members[0].text += ' '; },
    c => { c.groups[0].members[0].source.family = 'changed'; },
    c => { c.groups[0].members[0].target[0] = 'other'; },
    c => { c.groups[c.groups.length - 1].members[0].source = null; },
    c => { c.groups[c.groups.length - 1].conclusion_final = false; },
    c => { c.groups[0].members[0].source.languages.en.cue_start += 1; },
    c => { c.groups[0].members[0].source.languages.la.full_conclusion = 'invented'; }
  ]) {
    const candidate = plain(context); change(candidate);
    const result = plain(C.executeGroup(candidate));
    assert.equal(result.state, 'unresolved'); assert.deepEqual(result.members, []); refusals++;
  }
}
process.stdout.write(JSON.stringify({cases: input.cases.length, refusals}));
