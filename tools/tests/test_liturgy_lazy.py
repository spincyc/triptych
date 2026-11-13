"""Selected-Mass transport preserves the existing shared liturgical derivations."""
from __future__ import annotations

import os
import json
from pathlib import Path
import shutil
import subprocess
import unittest


ROOT = Path(__file__).resolve().parents[2]
NODE = shutil.which("node")

SETUP = r"""
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const Payload = require('./src/web/browser/liturgy/reader-proper-payload.js');
globalThis.LiturgyReaderProperPayload = Payload;
const Day = require('./src/web/browser/liturgy/day-read-payload.js');
const Propers = require('./src/web/browser/liturgy/propers-read-payload.js');
const generation = '1'.repeat(64);
function indexed(full) {
  const masses = full.masses.map(mass => {
    const descriptor = {...mass};
    delete descriptor.propers;
    if (mass.forms) descriptor.forms = mass.forms.map(form => {
      const row = {...form}; delete row.propers; return row;
    });
    descriptor.payload = `structure/propers/mass/${full.calendar}/${mass.key}.json`;
    return descriptor;
  });
  return {...full, reader_index: true, generation, masses};
}
function fixture(full) {
  const structure = indexed(full), requests = [];
  const bodies = new Map(full.masses.map(mass => [mass.key, mass]));
  const load = where => {
    requests.push(where);
    if (where === `structure/propers/reader/${full.calendar}.json`) return structure;
    const key = where.split('/').at(-1).replace(/\.json$/, '');
    assert.equal(where, `structure/propers/mass/${full.calendar}/${key}.json`);
    assert.ok(bodies.has(key), where);
    return {schema: Payload.MASS_SCHEMA, calendar: full.calendar, generation,
      mass: bodies.get(key)};
  };
  return {structure, requests, load};
}
function outcome(fn) {
  try { return {result: fn()}; }
  catch (error) { return {error: error.message}; }
}
"""


@unittest.skipUnless(NODE, "the shared reader needs Node")
class LiturgyLazyTests(unittest.TestCase):
    def node(self, source: str, *, timeout: int = 90) -> None:
        result = subprocess.run([NODE, "-"], input=SETUP + source, cwd=ROOT,
                                capture_output=True, text=True, timeout=timeout)
        self.assertEqual(result.returncode, 0, result.stderr or result.stdout)

    def test_dependency_closure_preserves_choices_and_loads_each_body_once(self) -> None:
        self.node(r"""
const full = {schema: 'triptych-propers-structure/v1', calendar: 'roman-1962', masses: [
  {key: 'principal', name: 'Principal', kind: 'seasonal', season: 'unrelated',
   forms: [{id: 'main', name: 'Main', ordinal: 1, propers: []}],
   propers: [{taken_from: {mass: 'common'}, execution_sources: [
     {companion: {target: ['companion', 'main', 'Collect']}}]}]},
  {key: 'common', name: 'Common', kind: 'common', propers: [
    {name_execution_sources: [{terminal_common: ['terminal', 'main', 'Collect']}]}]},
  {key: 'companion', name: 'Companion', kind: 'sanctoral', propers: []},
  {key: 'terminal', name: 'Terminal', kind: 'common', takes_from: {mass: 'principal'}, propers: []},
  {key: 'alternative', name: 'Alternative', kind: 'sanctoral', propers: []},
  {key: 'unrelated', name: 'Unrelated', kind: 'seasonal', propers: []}
]};
const one = fixture(full);
const roots = {options: [{choiceRequired: true, readable: [
  {key: 'principal', state: 'optional'}, {key: 'alternative', state: 'optional'}]}]};
const result = Payload.hydrateSync({...one, roots});
assert.equal(result, one.structure);
assert.deepEqual(result.masses.filter(mass => !mass.payload).map(mass => mass.key),
  ['principal', 'common', 'companion', 'terminal', 'alternative']);
assert.equal(one.requests.length, 5);
assert.equal(new Set(one.requests).size, 5);
assert.ok(result.masses.find(mass => mass.key === 'unrelated').payload);
Payload.hydrateSync({...one, roots});
assert.equal(one.requests.length, 5);
assert.equal(roots.options[0].choiceRequired, true);
(async () => {
  const two = fixture(full);
  await Payload.hydrate({...two, roots, load: async where => two.load(where)});
  assert.deepEqual(two.structure, result);
})().catch(error => { console.error(error); process.exitCode = 1; });
""")

    def test_mismatched_or_missing_payload_is_refused_and_can_be_retried(self) -> None:
        self.node(r"""
const full = {schema: 'triptych-propers-structure/v1', calendar: 'postconciliar', masses: [
  {key: 'advent-1', name: 'Advent I', kind: 'seasonal', propers: []}
]};
for (const change of [
  envelope => ({...envelope, generation: '2'.repeat(64)}),
  envelope => ({...envelope, calendar: 'roman-1962'}),
  envelope => ({...envelope, mass: {...envelope.mass, name: 'Changed'}}),
  envelope => ({...envelope, mass: {...envelope.mass, propers: undefined}})
]) {
  const one = fixture(full);
  assert.throws(() => Payload.hydrateSync({...one, roots: 'advent-1',
    load: where => change(one.load(where))}), /disagrees/);
  assert.ok(one.structure.masses[0].payload);
  assert.deepEqual(Payload.hydrateSync({...one, roots: 'advent-1'}).masses[0], full.masses[0]);
}
const unsafe = fixture(full); unsafe.structure.masses[0].payload = '../foreign.json';
assert.throws(() => Payload.hydrateSync({...unsafe, roots: 'advent-1'}), /path/);
assert.equal(unsafe.requests.length, 0);
const missing = fixture(full);
assert.throws(() => Payload.hydrateSync({...missing, roots: 'advent-1',
  load: () => { throw new Error('missing payload'); }}), /missing payload/);
assert.ok(missing.structure.masses[0].payload);
for (const reader_file of ['../foreign.json', 'structure/propers/postconciliar.json',
  'structure/propers/reader/roman-1962.json', undefined]) {
  assert.throws(() => Payload.indexPath('postconciliar',
    {id: 'postconciliar', reader_index: true, reader_file}), /reader file/);
}
""")

    def test_all_mode_wrappers_use_indexed_loading_and_browse_fetches_no_mass(self) -> None:
        self.node(r"""
(async () => {
  for (const calendar of ['roman-1962', 'postconciliar', 'roman-pre-1955']) {
    const full = {schema: 'triptych-propers-structure/v1', calendar, masses: [
      {key: 'selected', name: 'Selected', kind: 'seasonal', propers: []},
      {key: 'unrelated', name: 'Unrelated', kind: 'seasonal', propers: []}
    ]};
    const index = {missals: [{id: calendar, reader_index: true,
      reader_file: `structure/propers/reader/${calendar}.json`}]};
    for (const mode of ['read', 'missal', 'study', 'compare']) {
      const one = fixture(full), parsed = {recognized: {mode, mass: 'selected'}, present: ['mode', 'mass']};
      const result = await Day.loadStructure({load: async where => one.load(where),
        index, missal: calendar, parsed, mode, needsOrdinary: mode === 'missal',
        derived: {options: [{readable: [{key: 'selected'}]}]}});
      assert.deepEqual(result.masses[0], full.masses[0]);
      assert.equal(one.requests.length, 2);
      const two = fixture(full);
      await Propers.load({load: async where => two.load(where), calendar, index, parsed});
      assert.equal(two.requests.length, 2);
    }
    const browse = fixture(full);
    await Propers.load({load: async where => browse.load(where), calendar, index,
      parsed: {recognized: {}, present: []}});
    assert.equal(browse.requests.length, 1);
    assert.ok(browse.structure.masses.every(mass => mass.payload));
  }
})().catch(error => { console.error(error); process.exitCode = 1; });
""")

    @unittest.skipUnless(os.environ.get("TRIPTYCH_TEST_PROPER_DATA_ROOT"),
                         "set TRIPTYCH_TEST_PROPER_DATA_ROOT for generated Pages payloads")
    def test_generated_pages_manifest_and_every_mass_use_the_reader_route(self) -> None:
        self.node(r"""
(async () => {
  const root = process.env.TRIPTYCH_TEST_PROPER_DATA_ROOT;
  const data = relative => JSON.parse(fs.readFileSync(path.join(root, relative), 'utf8'));
  const index = data('structure/propers/index.json');
  let checked = 0;
  for (const row of index.missals) {
    const calendar = row.id, full = data(`structure/propers/${calendar}.json`);
    assert.equal(row.reader_file, `structure/propers/reader/${calendar}.json`);
    assert.equal(row.reader_index, true);
    const requests = [], cache = new Map();
    const load = where => {
      assert.ok(where === row.reader_file || where.startsWith(`structure/propers/mass/${calendar}/`), where);
      if (!cache.has(where)) { requests.push(where); cache.set(where, data(where)); }
      return cache.get(where);
    };
    const structure = await Propers.load({calendar, index, load,
      parsed: {recognized: {}, present: []}});
    assert.deepEqual(requests, [row.reader_file], 'Browse fetches only the real thin product');
    assert.ok(structure.masses.every(mass => !Object.hasOwn(mass, 'propers') &&
      (mass.forms || []).every(form => !Object.hasOwn(form, 'propers'))));
    for (const mass of full.masses) {
      await Propers.load({calendar, index, load,
        parsed: {recognized: {mass: mass.key}, present: ['mass']}});
      assert.deepEqual(structure.masses.find(one => one.key === mass.key), mass);
      checked++;
    }
    assert.deepEqual(structure.masses, full.masses);
    assert.equal(requests.length, full.masses.length + 1, 'each source body is fetched once');
  }
  assert.equal(index.missals.length, 3);
  assert.ok(checked > 1500, `${checked} source Masses`);
})().catch(error => { console.error(error); process.exitCode = 1; });
""", timeout=180)

    @unittest.skipUnless(os.environ.get("TRIPTYCH_LITURGY_LAZY_CHROMIUM") == "1" and
                         os.environ.get("TRIPTYCH_TEST_BROWSER_DATA_ROOT") and
                         shutil.which("chromium"),
                         "set TRIPTYCH_LITURGY_LAZY_CHROMIUM=1 with Chromium and generated browser data")
    def test_generated_pages_native_readers_keep_full_calendar_semantics(self) -> None:
        result = subprocess.run([NODE, str(Path(__file__).with_name("liturgy_lazy_browser.mjs"))],
                                cwd=ROOT, capture_output=True, text=True, timeout=240)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        report = json.loads(result.stdout.strip().splitlines()[-1])
        self.assertEqual(report["status"], "pass")
        self.assertEqual(len(report["cases"]), 14)

    @unittest.skipUnless(os.environ.get("TRIPTYCH_TEST_BROWSER_DATA_ROOT"),
                         "set TRIPTYCH_TEST_BROWSER_DATA_ROOT for full-product parity")
    def test_real_calendars_keep_mass_and_day_adapter_results(self) -> None:
        self.node(r"""
const DATA = process.env.TRIPTYCH_TEST_BROWSER_DATA_ROOT;
const data = relative => JSON.parse(fs.readFileSync(path.join(DATA, relative), 'utf8'));
const Adapters = require('./src/web/browser/liturgy/reader-state-adapters.js');
const Model = require('./src/web/browser/liturgy/assembly-model.js');
let comparisons = 0, successes = 0;
function request(calendar, entrance, lang, framed) {
  return {schema: 'triptych-liturgy-reader-state/v1', entrance,
    edition: {id: calendar}, bible: {id: 'douay-rheims', numbering: 'vulgate'},
    languages: {orations: lang, ...(framed ? {ordinary: lang} : {})},
    requestedMode: framed ? 'missal' : 'read',
    options: {ordinary: framed, legitimate: {}}, coverage: [], unresolvedChoices: [], sourceHooks: []};
}
for (const calendar of ['roman-1962', 'postconciliar', 'roman-pre-1955']) {
  const full = data(`structure/propers/${calendar}.json`);
  assert.ok(!full.reader_index, 'parity oracle must be the complete audited product');
  const ordinary = data(`structure/ordinary/${calendar}.json`);
  for (const mass of full.masses) {
    const one = fixture(full);
    Payload.hydrateSync({...one, roots: mass.key});
    const asked = {...request(calendar, 'propers', 'la', false), civilDate: null,
      formulary: {id: mass.key, type: mass.kind}};
    const expected = outcome(() => Adapters.adaptPropers({request: asked, structure: full}));
    if (expected.result) successes++;
    assert.deepEqual(outcome(() => Adapters.adaptPropers({request: asked, structure: one.structure})),
      expected, `${calendar}/${mass.key}`);
    comparisons++;
  }
  const year = data(`structure/calendar/${calendar}/2026.json`);
  const rubrics = data(`structure/rubrics/${calendar}.json`);
  for (let date = '2026-01-01'; date.startsWith('2026-'); date = Model.shift(date, 1)) {
    const derived = Model.derive({date, year, rubrics});
    for (const lang of ['la', 'en']) for (const framed of [false, true]) {
      const one = fixture(full);
      Payload.hydrateSync({...one, roots: Payload.dayRoots(derived)});
      for (const branch of derived.options) {
        const asked = {...request(calendar, 'day', lang, framed), civilDate: date,
          calendar: {id: calendar, ...(branch.option ? {territory: {id: branch.option}} : {})},
          apparatus: {why: false, rubrics: true}};
        const context = {request: asked, derived, ordinary: framed ? ordinary : null};
        assert.deepEqual(outcome(() => Adapters.adaptDay({...context, structure: one.structure})),
          outcome(() => Adapters.adaptDay({...context, structure: full})),
          `${calendar}/${date}/${lang}/${framed}/${branch.option}`);
        comparisons++;
      }
    }
  }
}
assert.ok(successes > 1000, `${successes} successful adaptations`);
assert.ok(comparisons > 5900, `${comparisons} comparisons`);
console.log(`${comparisons} exact adapter comparisons (${successes} successful Propers adaptations)`);
""", timeout=180)


if __name__ == "__main__":
    unittest.main()
