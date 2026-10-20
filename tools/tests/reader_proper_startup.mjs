import test from 'node:test';
import assert from 'node:assert/strict';
import { createRequire } from 'node:module';

const require = createRequire(import.meta.url);
const { startupHints } = require('../../src/web/browser/liturgy/reader-proper-payload.js');
const DAY = '#date=2026-08-02&missal=roman-1962&bible=douay-rheims&orations=la&mode=read&ordinary=0';
const PROPERS = '#missal=roman-1962&type=sanctoral&mass=commemoratione-omnium-fidelium-defunctorum&form=first&bible=douay-rheims&orations=en';
function hints(entrance, rawHash, overrides = {}) {
  return startupHints({ entrance, rawHash, baseURI: 'https://reader.example/liturgy/day.html',
    origin: 'https://reader.example', dataPath: path => '../browse/' + path, ...overrides });
}

test('settled Read URLs hint only their bounded manifests and selected data', () => {
  const day = hints('day', DAY);
  assert.equal(day.length, 7);
  assert.ok(day.includes('https://reader.example/browse/structure/calendar/roman-1962/2026.json'));
  assert.ok(day.includes('https://reader.example/browse/structure/propers/catalog/roman-1962.json'));
  assert.ok(day.every(url => !url.includes('structure/ordinary/roman-1962.json')));
  const propers = hints('propers', PROPERS);
  assert.equal(propers.length, 5);
  assert.ok(propers.includes('https://reader.example/browse/structure/propers/mass/roman-1962/commemoratione-omnium-fidelium-defunctorum.json'));
  assert.ok(propers.every(url => !url.includes('/rubrics/') && !url.includes('/calendar/')));
});

test('other modes, dormant Ordinary, cross-edition and explicit branches do not speculate', () => {
  for (const value of ['missal','study','compare']) {
    assert.deepEqual(hints('day', DAY.replace('mode=read', 'mode='+value)), []);
    assert.deepEqual(hints('propers', PROPERS+'&mode='+value), []);
  }
  for (const suffix of ['&why=1','&ordinary-lang=la','&mass=pentecost-10','&territory=universal','&form=main','&unknown=1']) {
    assert.deepEqual(hints('day', DAY+suffix), []);
  }
  assert.deepEqual(hints('day', DAY.replace('ordinary=0','ordinary=1')), []);
  assert.deepEqual(hints('propers', PROPERS.replace('roman-1962','roman-pre-1955')), []);
  assert.deepEqual(hints('propers', PROPERS+'&ordinary-lang=en'), []);
});

test('duplicate keys, impossible dates and path-shaped Mass keys emit no hints', () => {
  for (const hash of [DAY+'&missal=roman-1962', DAY+'&date=2026-08-02',
                     DAY.replace('2026-08-02','2026-02-30'), DAY.replace('2026-08-02','2025-02-29')]) {
    assert.deepEqual(hints('day', hash), []);
  }
  assert.equal(hints('day', DAY.replace('2026-08-02','2028-02-29')).length, 7);
  for (const mass of ['..%2Fsecret','%2Fetc%2Fpasswd','Apostle','a%3Fb','a'.repeat(129),'']) {
    assert.deepEqual(hints('propers', PROPERS.replace('mass=commemoratione-omnium-fidelium-defunctorum','mass='+mass)), []);
  }
});

test('the shared dataPath owns custom roots and hints stay on the current origin', () => {
  const custom = hints('propers', PROPERS, {dataPath: path => '/custom-data/' + path});
  assert.equal(custom.length, 5);
  assert.ok(custom.every(url => url.startsWith('https://reader.example/custom-data/')));
  for (const dataPath of [path => 'https://other.example/'+path,
                          path => 'http://reader.example/'+path,
                          path => 'https://user:password@reader.example/'+path,
                          path => 'file:///tmp/'+path,
                          () => { throw new Error('root unavailable'); }]) {
    assert.deepEqual(hints('propers', PROPERS, {dataPath}), []);
  }
  assert.deepEqual(hints('day', DAY, {origin:'null',baseURI:'file:///reader/day.html',dataPath:path=>'../browse/'+path}), []);
});

test('hints neither invent defaults nor decide that a syntactically safe Mass exists', () => {
  assert.deepEqual(hints('day', '#date=2026-08-02'), []);
  assert.deepEqual(hints('day', '#missal=roman-1962'), []);
  assert.deepEqual(hints('propers', '#missal=roman-1962'), []);
  const missing = hints('propers', PROPERS.replace('mass=commemoratione-omnium-fidelium-defunctorum','mass=missing-mass'));
  assert.equal(missing.length, 5);
  assert.ok(missing.some(url => url.endsWith('/mass/roman-1962/missing-mass.json')));
  assert.deepEqual(startupHints(null), []);
});
