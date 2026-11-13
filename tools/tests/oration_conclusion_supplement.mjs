import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';
import vm from 'node:vm';
const root = path.resolve(process.argv[2]);
const input = JSON.parse(fs.readFileSync(0, 'utf8'));
let code = fs.readFileSync(root + '/src/web/browser/liturgy/oration-conclusions.js', 'utf8');
// Review-only VM activation must match the generated finite authority exactly.
if (code.includes("const ACTIVE_AUTHORITY_SHA256 = '';")) {
  assert.ok(code.includes('const GENERATED_AUTHORITY_SHA256 = ' + JSON.stringify(input.authority_sha256) + ';'));
  code = code.replace("const ACTIVE_AUTHORITY_SHA256 = '';", 'const ACTIVE_AUTHORITY_SHA256 = ' + JSON.stringify(input.authority_sha256) + ';');
}
const sandbox = {module: {exports: {}}};
vm.runInNewContext(code, sandbox);
const conclusions = sandbox.module.exports;
assert.equal(conclusions.ACTIVE_AUTHORITY_SHA256, input.authority_sha256);
for (const {api, context, expected} of input.cases) {
  assert.deepEqual(JSON.parse(JSON.stringify(conclusions[api](context))), expected);
}
process.stdout.write(JSON.stringify({cases: input.cases.length}));
