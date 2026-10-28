#!/usr/bin/env node
/* Recorded lectionary-cycle selections over a single edition-qualified formulary. */
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { resolve } from 'node:path';
import { createRequire } from 'node:module';
import test from 'node:test';
const ROOT = resolve(process.env.TRIPTYCH_REVIEW_ROOT || resolve(import.meta.dirname, '../..'));
const MODULES = resolve(process.env.TRIPTYCH_CYCLE_MODULE_ROOT || ROOT, 'src/web/browser/liturgy');
const require = createRequire(import.meta.url);
const State = require(resolve(MODULES, 'reader-state.js'));
const Comparison = require(resolve(MODULES, 'reader-comparison.js'));
const PropersCompare = require(resolve(MODULES, 'propers-compare.js'));
const Adapters = require(resolve(ROOT, 'src/web/browser/liturgy/reader-state-adapters.js'));
const json = (path) => JSON.parse(readFileSync(resolve(ROOT, path), 'utf8'));
const structure = json('src/web/data/structure/propers/postconciliar.json');
const bibles = json('src/web/data/bibles.json');
const context = Adapters.validationContext({ entrance: 'propers', bibles,
  properIndex: json('src/web/data/structure/propers/index.json'),
  ordinaryIndex: { calendars: [] }, structures: { postconciliar: structure } });
const prefix = '#missal=postconciliar&type=christological&mass=transfiguration-lord&bible=douay-rheims&orations=la&mode=compare&compare=lectionary-cycle';
const normalize = (hash) => State.normalizeLegacy(State.parseLegacy('propers', hash), {
  context, defaults: { missal: 'postconciliar', bible: 'douay-rheims', orations: 'la' }
});
const fixtureRoot = process.env.TRIPTYCH_CYCLE_MODULE_ROOT || ROOT;
const fixture = JSON.parse(readFileSync(resolve(fixtureRoot,
  'tools/tests/fixtures/liturgy-reader-comparison/v1/propers-postconciliar-transfiguration-cycles.json'), 'utf8'));
const spec = fixture.comparison;
function input(comparison = structuredClone(spec)) {
  const template = json('tools/tests/fixtures/liturgy-reader-state/v1/propers-postconciliar-transfiguration-cycles.json').requested;
  return { comparison, sides: comparison.sides.map((side) => ({ id: side.id,
    result: Adapters.adaptPropers({ structure,
      request: { ...structuredClone(template), cycle: side.cycle } }) })) };
}

test('cycle Compare has explicit edition-qualified sides and canonical URL roundtrip', () => {
  const result = normalize(prefix + '&cycle=A&peer-cycle=B&location=compare%2Fproper%2Fgospel');
  assert.equal(result.ok, true, JSON.stringify(result.errors));
  assert.deepEqual(result.state.comparison, spec);
  assert.equal(result.state.civilDate, null);
  const hash = State.serializeLegacy(result);
  assert.match(hash, /cycle=A/);
  assert.match(hash, /peer-cycle=B/);
  assert.doesNotMatch(hash, /peer-orations/);
  const again = normalize(hash);
  assert.deepEqual(again.state, result.state);
  assert.equal(State.serializeLegacy(again), hash);
});

test('missing, equal, empty, duplicate, and wrong-dimension peers fail normalization', () => {
  for (const hash of [prefix + '&cycle=A', prefix + '&peer-cycle=B',
    prefix + '&cycle=A&peer-cycle=A', prefix + '&cycle=A&peer-cycle=',
    prefix + '&cycle=A&peer-cycle=B&peer-cycle=C',
    prefix + '&cycle=A&peer-cycle=B&peer-orations=en',
    prefix.replace('lectionary-cycle', 'oration-language') + '&peer-cycle=B&peer-orations=en']) {
    assert.equal(normalize(hash).ok, false, hash);
  }
  assert.equal(normalize(prefix.replace('&mode=compare', '&mode=read') + '&cycle=A&peer-cycle=B').ok, false);
});

test('held Transfiguration cycles independently resolve their source-qualified Gospel selections', () => {
  const prepared = input();
  const snapshot = JSON.stringify(prepared);
  const view = Comparison.compare(prepared);
  assert.equal(view.dimension, 'lectionary-cycle');
  assert.equal(view.calendarResults, null);
  assert.equal(view.units.length, fixture.expected.unitCount);
  assert.deepEqual(view.units.map((unit) => unit.semanticSlot),
    ['entrance-antiphon', 'reading-1', 'responsorial-psalm', 'reading-2', 'gospel-acclamation', 'gospel', 'communion-antiphon']);
  const gospel = view.units.find((unit) => unit.semanticSlot === 'gospel');
  assert.deepEqual(gospel.sides.map((cell) => cell.status), ['text-held', 'text-held']);
  assert.deepEqual(gospel.sides.map((cell) => cell.event.selected.cycle), ['A', 'B']);
  assert.deepEqual(gospel.sides.map((cell) => cell.event.selected.references),
    [['Matthew 17:1-9'], ['Mark 9:2-10']]);
  for (const cell of gospel.sides) {
    assert.equal(cell.event.selected.bible, 'douay-rheims');
    assert.equal(cell.event.sourceHooks[0].id, 'postconciliar/transfiguration-lord/006');
  }
  assert.equal(JSON.stringify(prepared), snapshot);
});

test('the third recorded cycle remains an explicit selectable peer', () => {
  const comparison = structuredClone(spec);
  comparison.sides[1] = { ...comparison.sides[1], id: 'C', cycle: 'C' };
  const view = Comparison.compare(input(comparison));
  assert.deepEqual(view.units.find((unit) => unit.semanticSlot === 'gospel').sides[1]
    .event.selected.references, ['Luke 9:28b-36']);
});

test('unknown primary or peer cycles cannot fall back to another held cycle', () => {
  for (const index of [0, 1]) {
    const comparison = structuredClone(spec);
    comparison.sides[index] = { ...comparison.sides[index], id: 'Z', cycle: 'Z' };
    assert.throws(() => input(comparison), /explicit cycle is not held/);
  }
});

test('mixed Bible, languages, forms, or cycle descriptors fail semantic pairing', () => {
  for (const mutate of [
    (p) => { p.sides[1].result.request.bible = { id: 'clementine-vulgate' }; },
    (p) => { p.sides[1].result.request.languages.orations = 'en'; },
    (p) => { p.sides[1].result.request.form = 'another-form'; },
    (p) => { p.comparison.sides[1].cycle = 'C'; },
    (p) => { p.sides[1].result.events.forEach((event) => { event.selected.cycle = null; }); }
  ]) {
    const prepared = input(); mutate(prepared);
    assert.throws(() => Comparison.compare(prepared));
  }
});

test('pairing remains semantic and distinguishes no event, unavailable text, and absent material', () => {
  const prepared = input();
  const right = prepared.sides[1].result;
  right.events = right.events.filter((event) => event.semanticSlot.identity.id !== 'reading-2').reverse();
  right.events.find((event) => event.semanticSlot.identity.id === 'reading-1').selected.availability = 'unavailable';
  right.events.find((event) => event.semanticSlot.identity.id === 'responsorial-psalm').selected.availability = 'absent';
  const view = Comparison.compare(prepared);
  assert.equal(view.units.find((unit) => unit.semanticSlot === 'reading-2').sides[1].status,
    'no-event-in-selected-formulary');
  assert.equal(view.units.find((unit) => unit.semanticSlot === 'reading-1').sides[1].status, 'text-unavailable');
  assert.equal(view.units.find((unit) => unit.semanticSlot === 'responsorial-psalm').sides[1].status,
    'selected-material-absent');
});

test('cycle choices derive from the exact held Mass and never set a primary or peer default', () => {
  const state = normalize(prefix + '&cycle=A&peer-cycle=B').state;
  assert.deepEqual(PropersCompare.heldCycles(structure, state), ['A', 'B', 'C']);
  assert.deepEqual(PropersCompare.heldCycles(structure, { ...state, formulary: { id: 'not-held' } }), []);
  const side = PropersCompare.sideRequest(state, spec.sides[1]);
  assert.equal(side.cycle, 'B');
  assert.equal(side.requestedMode, 'read');
  assert.equal(side.comparison, undefined);
  assert.deepEqual(side.languages, state.languages);
});
