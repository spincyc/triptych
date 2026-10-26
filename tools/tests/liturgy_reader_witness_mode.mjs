#!/usr/bin/env node
/* Partial Proper witness admission must preserve the selected Ordinary inputs. */
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { createRequire } from 'node:module';
import { resolve } from 'node:path';
import vm from 'node:vm';
import test from 'node:test';
const ROOT = resolve(process.env.TRIPTYCH_REVIEW_ROOT || resolve(import.meta.dirname, '../..'));
const CANDIDATE = process.env.TRIPTYCH_WITNESS_MODULE_ROOT || ROOT;
const require = createRequire(import.meta.url);
const Adapters = require(resolve(CANDIDATE, 'src/web/browser/liturgy/reader-state-adapters.js'));
const json = (path) => JSON.parse(readFileSync(resolve(ROOT, path), 'utf8'));
const structure = json('src/web/data/structure/propers/roman-1962.json');
const ordinary = json('src/web/data/structure/ordinary/roman-1962.json');
const key = 'commemoratione-omnium-fidelium-defunctorum';
const mass = structure.masses.find((one) => one.key === key);
const caswall = 'edition.edward-caswall.lyra-catholica.london-1849';
const cummiskey = 'edition.eugene-cummiskey.roman-missal-english-laity.philadelphia-1861';
const realm = vm.createContext({ window: { location: { search: '' }, addEventListener() {} },
  document: { addEventListener() {} }, URLSearchParams, URL, Map, Set });
vm.runInContext(readFileSync(resolve(ROOT, 'src/web/browser/shared/browser-core.js'), 'utf8'), realm);
const T = realm.window.Triptych;
const controller = readFileSync(resolve(CANDIDATE, 'src/web/browser/liturgy/propers-reader.js'), 'utf8');
const start = controller.indexOf('  function formularyWitnessState(');
const end = controller.indexOf('  function selectedBrowseMass(', start);
assert.ok(start >= 0 && end > start);
realm.T = T; realm.Adapters = Adapters; realm.runtime = { ordinary, normalized: null };
vm.runInContext(controller.slice(start, end), realm);
const witnessState = realm.formularyWitnessState;
function request(mode = 'read', witness = caswall) {
  const state = { schema: 'triptych-liturgy-reader-state/v1', entrance: 'propers', civilDate: null,
    edition: { id: 'roman-1962' }, formulary: { id: key, type: 'sanctoral' }, form: 'first',
    bible: { id: 'douay-rheims', numbering: 'vulgate' }, languages: { orations: 'en' },
    requestedMode: mode, options: { ordinary: mode === 'missal', legitimate: {} },
    coverage: [], unresolvedChoices: [], sourceHooks: [] };
  if (witness) state.languages.translationWitness = witness;
  if (mode === 'missal') state.languages.ordinary = 'en';
  return state;
}

test('All Souls selected Mass and source witness metadata agree between split and monolith', () => {
  const envelope = json('src/web/data/structure/propers/mass/roman-1962/' + key + '.json');
  assert.deepEqual(envelope.mass, mass);
  const sequences = mass.propers.filter((proper) => proper.name === 'Sequence');
  assert.equal(sequences.length, 3);
  assert.ok(sequences.every((proper) => proper.translations.some((row) => row.source_id === caswall)));
});

test('Missal witness admission preserves the partial Proper union from Read', () => {
  const read = request(), missal = request('missal');
  const readHeld = Array.from(witnessState(structure, mass, 'en', read).held).sort();
  const missalHeld = Array.from(witnessState(structure, mass, 'en', missal).held).sort();
  assert.ok(readHeld.includes(caswall)); assert.ok(readHeld.includes(cummiskey));
  assert.deepEqual(missalHeld, readHeld);
  assert.ok(!missalHeld.includes('not-held'));
});

test('omitting the loaded Ordinary is the false-refusal trigger, not a missing Proper witness', () => {
  const state = request('missal', null);
  assert.throws(() => Adapters.adaptPropers({ request: state, structure }), /no production Ordinary/);
  assert.doesNotThrow(() => Adapters.adaptPropers({ request: state, structure, ordinary }));
});

test('Caswall holds only its Sequence while another witness is never silently substituted', () => {
  for (const mode of ['read', 'missal']) {
    const result = Adapters.adaptPropers({ request: request(mode), structure, ordinary: mode === 'missal' ? ordinary : null });
    const sequence = result.events.find((event) => event.editionSlotLabel === 'Sequence');
    const collect = result.events.find((event) => event.editionSlotLabel === 'Collect');
    assert.equal(sequence.selected.availability, 'held'); assert.equal(sequence.selected.sourceId, caswall);
    assert.ok(sequence.selected.text);
    assert.equal(collect.selected.availability, 'unavailable'); assert.equal(collect.selected.text, null);
    assert.notEqual(collect.selected.sourceId, cummiskey);
    if (mode === 'missal') {
      const ordinaryText = result.events.filter((event) => event.kind === 'ordinary-element' && event.selected.availability === 'held');
      assert.ok(ordinaryText.length > 0);
      assert.ok(ordinaryText.every((event) => event.selected.sourceId !== caswall));
    }
  }
});

test('unknown witnesses Latin witness misuse and unresolved Mass forms still fail closed', () => {
  assert.throws(() => Adapters.adaptPropers({ request: request('missal', 'not-held'), structure, ordinary }), /selected no appointed text/);
  const latin = request('missal'); latin.languages.orations = 'la';
  assert.throws(() => Adapters.adaptPropers({ request: latin, structure, ordinary }), /cannot select the Latin source/);
  const unselected = request('missal'); delete unselected.form;
  assert.deepEqual(Array.from(witnessState(structure, mass, 'en', unselected).held), []);
});

function pendingWitnessRequest(calendar, massKey, witness, mode = 'read') {
  return { schema: 'triptych-liturgy-reader-state/v1', entrance: 'propers', civilDate: null,
    edition: { id: calendar }, formulary: { id: massKey },
    bible: { id: 'douay-rheims', numbering: 'vulgate' },
    languages: { orations: 'en', ordinary: 'en', translationWitness: witness },
    requestedMode: mode, options: { ordinary: mode === 'missal', legitimate: {} },
    coverage: [], unresolvedChoices: [], sourceHooks: [] };
}

const pendingWitnessCases = [
  ...['commune-virginum-2', 'commune-virginum-4', 'comm-s-priscae-virginis-martyris',
    'comm-s-emerentianae-virginis-martyris', 'comm-s-dorotheae-virginis-martyris',
    'comm-s-petronillae-virginis', 'comm-s-margaritae-virginis-martyris',
    'comm-s-christinae-virginis-martyris', 's-bibianae-virginis-martyris']
    .map(id => ['roman-1962', id, cummiskey]),
  ['roman-1962', 'comm-ss-placidi-sociorum-martyrum',
    'edition.francis-xavier-lasance.the-new-roman-missal.benziger-revised-1945'],
  ['postconciliar', 'easter-vigil', cummiskey]
];

test('every actual offered witness confined to pending source options preserves an honest unresolved state', () => {
  for (const [calendar, massKey, witness] of pendingWitnessCases) {
    const heldStructure = json('src/web/data/structure/propers/' + calendar + '.json');
    const heldMass = heldStructure.masses.find(one => one.key === massKey);
    const state = pendingWitnessRequest(calendar, massKey, witness);
    realm.runtime.ordinary = json('src/web/data/structure/ordinary/' + calendar + '.json');
    const before = JSON.stringify({ heldStructure, state });
    assert.ok(witnessState(heldStructure, heldMass, 'en', state).held.includes(witness), massKey);
    const view = Adapters.adaptPropers({ request: state, structure: heldStructure });
    assert.equal(view.request.languages.translationWitness, witness);
    const pending = view.events.filter(event => event.kind === 'proper-choice' && event.selection.state === 'required');
    assert.ok(pending.length > 0, massKey);
    const held = pending.flatMap(event => event.options.flatMap(option => option.events))
      .filter(event => event.selected.sourceId === witness && event.selected.availability === 'held');
    assert.ok(held.length > 0, massKey);
    // No pending member becomes an active event or silently selects its option.
    const active = view.events.filter(event => event.kind === 'proper');
    assert.ok(held.every(event => !active.some(one => one.id === event.id)), massKey);
    assert.ok(pending.every(event => event.selection.option === null &&
      view.unresolvedChoices.some(choice => choice.id === event.id)), massKey);
    assert.equal(JSON.stringify({ heldStructure, state }), before);
  }
});

test('choosing the exact source option admits only that witness body in Read and Missal', () => {
  const massKey = 'commune-virginum-2';
  const heldMass = structure.masses.find(one => one.key === massKey);
  const group = 'proper-choice/roman-1962/' + massKey + '/main/virginum-2-post-epistle';
  const source = heldMass.propers.find(one => one.name === 'Alleluia');
  const literal = source.translations.find(one => one.source_id === cummiskey).text;
  for (const mode of ['read', 'missal']) {
    const state = pendingWitnessRequest('roman-1962', massKey, cummiskey, mode);
    state.properChoices = { [group]: 'regular' };
    const view = Adapters.adaptPropers({ request: state, structure, ordinary: mode === 'missal' ? ordinary : null });
    const choice = view.events.find(event => event.id === group);
    assert.deepEqual(choice.selection, { state: 'selected', option: 'regular' });
    assert.equal(choice.options.find(option => option.id === 'regular').events[0].selected.text, literal);
    assert.equal(choice.options.find(option => option.id === 'regular').events[0].selected.sourceId, cummiskey);
    assert.ok(!view.unresolvedChoices.some(one => one.id === group));
    for (const option of ['tract', 'paschal']) {
      const wrong = structuredClone(state); wrong.properChoices[group] = option;
      assert.throws(() => Adapters.adaptPropers({ request: wrong, structure,
        ordinary: mode === 'missal' ? ordinary : null }), /selected no appointed text/);
    }
  }
});

test('pending options do not admit unknown witnesses empty bodies foreign applicability or foreign choices', () => {
  const state = pendingWitnessRequest('roman-1962', 'commune-virginum-2', cummiskey);
  const unknown = structuredClone(state); unknown.languages.translationWitness = 'not-held';
  assert.throws(() => Adapters.adaptPropers({ request: unknown, structure }), /selected no appointed text/);
  const empty = structuredClone(structure);
  empty.masses.find(one => one.key === state.formulary.id).propers.forEach(proper => {
    proper.translations = (proper.translations || []).filter(one => one.source_id !== cummiskey);
  });
  assert.throws(() => Adapters.adaptPropers({ request: state, structure: empty }), /selected no appointed text/);
  const foreignChoice = structuredClone(state);
  foreignChoice.properChoices = { 'proper-choice/roman-1962/another-mass/main/virginum-2-post-epistle': 'regular' };
  assert.throws(() => Adapters.adaptPropers({ request: foreignChoice, structure }), /another edition, formulary or form/);
  const inherited = json('src/web/data/structure/propers/roman-pre-1955.json');
  const foreign = pendingWitnessRequest('roman-pre-1955', 'commune-virginum-2', cummiskey);
  assert.throws(() => Adapters.adaptPropers({ request: foreign, structure: inherited }), /foreign-source Proper applicability/);
});
