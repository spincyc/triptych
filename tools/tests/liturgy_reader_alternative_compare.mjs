#!/usr/bin/env node
/* Existing source-recorded longer/shorter options over the same Propers identity. */
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { resolve } from 'node:path';
import { createRequire } from 'node:module';
import test from 'node:test';
const ROOT = resolve(process.env.TRIPTYCH_REVIEW_ROOT || resolve(import.meta.dirname, '../..'));
const CANDIDATE = process.env.TRIPTYCH_ALTERNATIVE_MODULE_ROOT || ROOT;
const MODULES = resolve(CANDIDATE, 'src/web/browser/liturgy');
const require = createRequire(import.meta.url);
const State = require(resolve(MODULES, 'reader-state.js'));
const Adapters = require(resolve(MODULES, 'reader-state-adapters.js'));
const Comparison = require(resolve(MODULES, 'reader-comparison.js'));
const PropersCompare = require(resolve(MODULES, 'propers-compare.js'));
const json = (path) => JSON.parse(readFileSync(resolve(ROOT, path), 'utf8'));
const structure = json('src/web/data/structure/propers/postconciliar.json');
const context = Adapters.validationContext({ entrance: 'propers',
  bibles: json('src/web/data/bibles.json'), properIndex: json('src/web/data/structure/propers/index.json'),
  ordinaryIndex: { calendars: [] }, structures: { postconciliar: structure } });
const group = 'proper-choice/postconciliar/presentation-lord/main/gospel';
const longer = group + '/longer';
const shorter = group + '/shorter';
const prefix = '#missal=postconciliar&type=christological&mass=presentation-lord&bible=douay-rheims&orations=la&mode=compare&compare=reading-alternative';
const normalize = (hash) => State.normalizeLegacy(State.parseLegacy('propers', hash), {
  context, defaults: { missal: 'postconciliar', bible: 'douay-rheims', orations: 'la' }
});
const hash = prefix + '&alternative=' + encodeURIComponent(longer) + '&peer-alternative=' + encodeURIComponent(shorter);
const normalized = normalize(hash);
const comparison = normalized.state.comparison;
const fixture = JSON.parse(readFileSync(resolve(CANDIDATE,
  'tools/tests/fixtures/liturgy-reader-comparison/v1/propers-postconciliar-presentation-alternatives.json'), 'utf8'));
function request() {
  return { schema: State.STATE_SCHEMA, entrance: 'propers', civilDate: null,
    edition: { id: 'postconciliar' }, formulary: { id: 'presentation-lord', type: 'christological' },
    bible: { id: 'douay-rheims', numbering: 'vulgate' }, languages: { orations: 'la' },
    requestedMode: 'read', options: { ordinary: false, legitimate: {} }, coverage: [],
    unresolvedChoices: [], sourceHooks: [] };
}
function adapt(id) {
  const selected = request();
  if (id !== undefined) selected.alternative = { id };
  return Adapters.adaptPropers({ request: selected, structure });
}
function input() {
  return { comparison: structuredClone(comparison), sides: comparison.sides.map((side) => ({
    id: side.id, result: adapt(side.alternative.id)
  })) };
}

test('the production Presentation retains a source-recorded unselected longer/shorter Gospel choice', () => {
  const result = adapt();
  const choice = result.events.find((event) => event.kind === 'proper-choice');
  assert.equal(choice.id, group);
  assert.deepEqual(choice.selection, { state: 'required', option: null });
  assert.deepEqual(choice.options.map((option) => option.id), ['longer', 'shorter']);
  assert.deepEqual(choice.options.map((option) => option.events[0].selected.references),
    [['Luke 2:22-40'], ['Luke 2:22-32']]);
  assert.equal(result.unresolvedChoices.length, 1);
  assert.deepEqual(PropersCompare.heldAlternatives(result).map((one) => one.id), [longer, shorter]);
});

test('both exact source option IDs survive canonical normalization without a date or inferred choice', () => {
  assert.equal(normalized.ok, true, JSON.stringify(normalized.errors));
  assert.deepEqual(comparison, fixture.comparison);
  assert.equal(normalized.state.alternative.id, longer);
  assert.equal(normalized.state.civilDate, null);
  assert.deepEqual(comparison.sides.map((side) => [side.id, side.alternative.id]),
    [['longer', longer], ['shorter', shorter]]);
  const serialized = State.serializeLegacy(normalized);
  assert.deepEqual(normalize(serialized).state, normalized.state);
  assert.equal(State.serializeLegacy(normalize(serialized)), serialized);
});

test('missing equal duplicate wrong-dimension and different-source-group peers fail normalization', () => {
  for (const bad of [prefix, prefix + '&peer-alternative=' + shorter,
    prefix + '&alternative=' + longer,
    hash.replace(encodeURIComponent(shorter), encodeURIComponent(longer)),
    hash + '&peer-alternative=' + shorter, hash + '&peer-orations=en', hash + '&peer-cycle=A',
    hash.replace(encodeURIComponent(shorter), encodeURIComponent(shorter.replace('/gospel/', '/another-group/'))),
    hash.replace('mode=compare', 'mode=read')]) assert.equal(normalize(bad).ok, false, bad);
  assert.equal(State.validateReaderState({ ...normalized.state,
    comparison: { ...comparison, sides: [null, null] } }).ok, false);
});

test('adapters select only the exact held source option without mutating production data or the request', () => {
  const source = JSON.stringify(structure);
  const state = request(); state.alternative = { id: shorter };
  const snapshot = JSON.stringify(state);
  const result = Adapters.adaptPropers({ request: state, structure });
  const choice = result.events.find((event) => event.kind === 'proper-choice');
  assert.deepEqual(choice.selection, { state: 'selected', option: 'shorter' });
  assert.equal(result.resolved.alternative, shorter);
  assert.deepEqual(result.unresolvedChoices, []);
  const selected = choice.options.find((option) => option.id === 'shorter').events[0];
  assert.equal(selected.id, 'proper/postconciliar/presentation-lord/006');
  assert.ok(selected.sourceHooks.some((hook) => hook.kind === 'proper-choice-option' && hook.id === shorter));
  assert.equal(JSON.stringify(structure), source);
  assert.equal(JSON.stringify(state), snapshot);
  for (const id of [group + '/unknown', shorter.replace('/presentation-lord/', '/transfiguration-lord/'),
    shorter.replace('/main/', '/not-held/'), 'shorter']) assert.throws(() => adapt(id), /alternative.*not held/);
});

test('Compare independently resolves source ordinals 005 and 006 into their one shared Gospel slot', () => {
  const prepared = input();
  const before = JSON.stringify(prepared);
  const view = Comparison.compare(prepared);
  assert.equal(view.calendarResults, null);
  assert.equal(view.dimension, 'reading-alternative');
  assert.equal(view.units.length, 5);
  const gospel = view.units.find((unit) => unit.semanticSlot === 'gospel');
  assert.deepEqual(gospel.sides.map((cell) => cell.status), ['text-held', 'text-held']);
  assert.deepEqual(gospel.sides.map((cell) => cell.event.id),
    ['proper/postconciliar/presentation-lord/005', 'proper/postconciliar/presentation-lord/006']);
  assert.deepEqual(gospel.sides.map((cell) => cell.event.selected.references),
    [['Luke 2:22-40'], ['Luke 2:22-32']]);
  assert.equal(JSON.stringify(prepared), before);
});

test('mixed edition form Bible language cycle options and unrelated source groups fail closed', () => {
  for (const mutate of [
    (p) => { p.sides[1].result.request.edition.id = 'roman-1962'; },
    (p) => { p.sides[1].result.request.form = 'not-held'; },
    (p) => { p.sides[1].result.request.bible.id = 'clementine-vulgate'; },
    (p) => { p.sides[1].result.request.languages.orations = 'en'; },
    (p) => { p.sides[1].result.request.cycle = 'B'; },
    (p) => { p.sides[1].result.request.options.legitimate = { creed: 'nicene' }; },
    (p) => { p.comparison.sides[1].alternative.id = group + '/not-held'; },
    (p) => { p.sides[1].result.events.find((event) => event.kind === 'proper-choice').selection.state = 'required'; }
  ]) { const prepared = input(); mutate(prepared); assert.throws(() => Comparison.compare(prepared)); }
  const unselected = input(); unselected.sides[1].result = adapt();
  assert.throws(() => Comparison.compare(unselected), /choices that remain unresolved/);
});

test('selected reading alternatives preserve unavailable absent and missing-event distinctions', () => {
  const prepared = input();
  const right = prepared.sides[1].result;
  right.events = right.events.filter((event) => event.semanticSlot?.identity.id !== 'reading-2').reverse();
  right.events.find((event) => event.semanticSlot?.identity.id === 'reading-1').selected.availability = 'unavailable';
  right.events.find((event) => event.semanticSlot?.identity.id === 'responsorial-psalm').selected.availability = 'absent';
  const view = Comparison.compare(prepared);
  assert.equal(view.units.find((unit) => unit.semanticSlot === 'reading-2').sides[1].status, 'no-event-in-selected-formulary');
  assert.equal(view.units.find((unit) => unit.semanticSlot === 'reading-1').sides[1].status, 'text-unavailable');
  assert.equal(view.units.find((unit) => unit.semanticSlot === 'responsorial-psalm').sides[1].status, 'selected-material-absent');
});

test('semantic locations map to the source choice wrapper and unrelated or multiple groups are not offered', () => {
  const result = adapt(shorter);
  assert.deepEqual(PropersCompare.compareLocation({ kind: 'event', id: group }, result),
    { kind: 'event', id: 'compare/proper/gospel' });
  assert.deepEqual(PropersCompare.fromCompareLocation({ kind: 'event', id: 'compare/proper/gospel' }, result),
    { kind: 'event', id: group });
  const unrelated = adapt();
  unrelated.events.find((event) => event.kind === 'proper-choice').options.forEach((option) => {
    option.events[0].semanticSlot.identity.id = 'collect';
  });
  assert.deepEqual(PropersCompare.heldAlternatives(unrelated), []);
  const multiple = adapt(); multiple.events.push(structuredClone(multiple.events.find((event) => event.kind === 'proper-choice')));
  assert.deepEqual(PropersCompare.heldAlternatives(multiple), []);
});
