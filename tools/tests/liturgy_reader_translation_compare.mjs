#!/usr/bin/env node
/* Same-language witness comparisons retain exact same-source Proper coordinates. */
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { resolve } from 'node:path';
import { createRequire } from 'node:module';
import vm from 'node:vm';
import test from 'node:test';
const ROOT = resolve(process.env.TRIPTYCH_REVIEW_ROOT || resolve(import.meta.dirname, '../..'));
const CANDIDATE = process.env.TRIPTYCH_TRANSLATION_MODULE_ROOT || ROOT;
const MODULES = resolve(CANDIDATE, 'src/web/browser/liturgy');
const require = createRequire(import.meta.url);
const State = require(resolve(MODULES, 'reader-state.js'));
const Adapters = require(resolve(MODULES, 'reader-state-adapters.js'));
const Comparison = require(resolve(MODULES, 'reader-comparison.js'));
const View = require(resolve(MODULES, 'reader-compare-view.js'));
const PropersCompare = require(resolve(MODULES, 'propers-compare.js'));
const json = (path) => JSON.parse(readFileSync(resolve(ROOT, path), 'utf8'));
const structure = json('src/web/data/structure/propers/roman-1962.json');
const fixture = JSON.parse(readFileSync(resolve(CANDIDATE,
  'tools/tests/fixtures/liturgy-reader-comparison/v1/propers-roman-1962-allsouls-translation-witnesses.json'), 'utf8'));
const bibles = json('src/web/data/bibles.json').bibles;
const key = 'commemoratione-omnium-fidelium-defunctorum';
const caswall = 'edition.edward-caswall.lyra-catholica.london-1849';
const irons = 'edition.hymns-ancient-and-modern-proprietors.hymns-ancient-and-modern.london-complete-edition-1890';
const cummiskey = 'edition.eugene-cummiskey.roman-missal-english-laity.philadelphia-1861';
const context = Adapters.validationContext({ entrance: 'propers', bibles: { bibles },
  properIndex: json('src/web/data/structure/propers/index.json'), ordinaryIndex: { calendars: [] },
  structures: { 'roman-1962': structure } });
const prefix = '#missal=roman-1962&type=sanctoral&mass=' + key + '&form=first&bible=douay-rheims&orations=en&mode=compare&compare=translation-witness';
const normalize = (hash) => State.normalizeLegacy(State.parseLegacy('propers', hash), { context,
  defaults: { missal: 'roman-1962', bible: 'douay-rheims', orations: 'la' } });
const hash = prefix + '&translation-witness=' + caswall + '&peer-witness=' + irons;
const normalized = normalize(hash);
const realm = vm.createContext({ window: { location: { search: '' }, addEventListener() {} },
  document: { addEventListener() {} }, URLSearchParams, URL });
vm.runInContext(readFileSync(resolve(CANDIDATE, 'src/web/browser/shared/browser-core.js'), 'utf8'), realm);
const T = realm.window.Triptych;
function input(peer = irons) {
  const state = normalize(prefix + '&translation-witness=' + caswall + '&peer-witness=' + peer).state;
  return { comparison: state.comparison, sides: state.comparison.sides.map((descriptor) => ({
    id: descriptor.id, structure,
    result: Adapters.adaptPropers({ request: PropersCompare.sideRequest(state, descriptor), structure })
  })) };
}
function build(state = normalized.state) {
  let presentation;
  return PropersCompare.build({ state, structure, bibles, Adapters, Comparison,
    View: { render(value) { presentation = value; return { projected: View.project(value.view), semanticIds: [] }; } },
    T: Object.assign({}, T, { fetchFragments: async () => ({ fragments: new Map() }) }),
    isCurrent: () => true }).then((result) => ({ result, presentation }));
}

test('explicit same-language witness identities and Latin-accompaniment state roundtrip without a date', () => {
  assert.equal(fixture.schema, 'triptych-liturgy-reader-comparison-fixture/v1');
  fixture.basis.paths.forEach(path => assert.ok(readFileSync(resolve(ROOT, path)).length));
  assert.equal(normalized.ok, true, JSON.stringify(normalized.errors));
  assert.deepEqual(normalized.state.comparison, fixture.comparison);
  assert.equal(normalized.state.form, fixture.selection.form);
  assert.equal(normalized.state.bible.id, fixture.selection.bible);
  assert.deepEqual(normalized.state.comparison.sides.map(side => side.languages.orations), ['en', 'en']);
  assert.equal(normalized.state.civilDate, null);
  for (const suffix of ['', '&text-display=latin-and-selected&location=compare%2Fsource%2Fproper%2Froman-1962%2F' + key + '%2F006']) {
    const state = normalize(hash + suffix);
    assert.equal(state.ok, true, JSON.stringify(state.errors));
    const serialized = State.serializeLegacy(state);
    assert.deepEqual(normalize(serialized).state, state.state);
    assert.equal(State.serializeLegacy(normalize(serialized)), serialized);
  }
});

test('missing equal duplicate Latin-source and wrong-axis peers fail normalization', () => {
  for (const bad of [prefix, prefix + '&peer-witness=' + irons, prefix + '&translation-witness=' + caswall,
    hash.replace(irons, caswall), hash + '&peer-witness=' + irons, hash.replace('orations=en', 'orations=la'),
    hash + '&peer-orations=la', hash + '&peer-cycle=A', hash + '&peer-alternative=shorter', hash.replace('mode=compare', 'mode=read')]) {
    assert.equal(normalize(bad).ok, false, bad);
  }
  assert.deepEqual(PropersCompare.preflight(State.parseLegacy('propers', hash)), []);
  assert.ok(PropersCompare.preflight(State.parseLegacy('propers', hash.replace('compare=translation-witness', 'compare=oration-language')))
    .some(error => error.path === 'translation-witness'));
});

test('eleven exact source coordinates include the unmapped Sequence without cross-edition slot claims', () => {
  const prepared = input(), before = JSON.stringify(prepared);
  const view = Comparison.compare(prepared);
  assert.equal(view.units.length, fixture.expected.unitCount); assert.equal(view.calendarResults, fixture.expected.calendar);
  assert.ok(view.units.every(unit => unit.relation === fixture.expected.relation));
  const sequence = view.units.find(unit => unit.sourceCoordinate.ordinal === 6);
  assert.equal(sequence.label, 'Sequence'); assert.equal(sequence.semanticSlot, fixture.expected.sequence.semanticSlot);
  assert.equal(sequence.sourceCoordinate.eventId, fixture.expected.sequence.eventId);
  assert.deepEqual(sequence.sides.map(cell => cell.status), fixture.expected.sequence.statuses);
  assert.deepEqual(sequence.sides.map(cell => cell.event.selected.sourceId), [caswall, irons]);
  assert.equal(sequence.sides[0].event.id, sequence.sides[1].event.id);
  const projection = View.project(view);
  assert.equal(projection.units[5].location, 'compare/source/proper/roman-1962/' + key + '/006');
  prepared.sides[1].result.events.reverse();
  assert.deepEqual(Comparison.compare(prepared).units, view.units);
  prepared.sides[1].result.events.reverse(); assert.equal(JSON.stringify(prepared), before);
});

test('partial witness union keeps Cummiskey prayers and Caswall Sequence as explicit opposite gaps', () => {
  const view = Comparison.compare(input(cummiskey));
  const sequence = view.units.find(unit => unit.sourceCoordinate.ordinal === 6);
  const collect = view.units.find(unit => unit.sourceCoordinate.ordinal === 2);
  assert.equal(cummiskey, fixture.expected.partialPeer.id);
  assert.deepEqual(sequence.sides.map(cell => cell.status), fixture.expected.partialPeer.sequenceStatuses);
  assert.deepEqual(collect.sides.map(cell => cell.status), fixture.expected.partialPeer.collectStatuses);
  assert.equal(sequence.sides[1].event.selected.reason, fixture.expected.partialPeer.unavailableReason);
  assert.equal(collect.sides[0].event.selected.text, null);
  assert.ok(view.units.every(unit => unit.sides.every(cell => cell.event !== null)));
});

test('different source revision, wrong or duplicate coordinates, owner form and source hooks refuse', () => {
  for (const mutate of [
    p => { p.sides[1].structure = structuredClone(structure); },
    p => { const invalid = { ...structure, schema: 'unverified' }; p.sides.forEach(side => { side.structure = invalid; }); },
    p => { p.sides[1].result.events[5].id = p.sides[1].result.events[4].id; },
    p => { p.sides[1].result.events[5].sourceHooks[0].id = 'roman-1962/' + key + '/005'; },
    p => { p.sides[1].result.events[5].sourceHooks.push(structuredClone(p.sides[1].result.events[5].sourceHooks[0])); },
    p => { p.sides[1].result.events[5].sourceKind = 'not-held'; },
    p => { p.sides[1].result.events[5].form = 'wrong-form'; },
    p => { p.sides[1].result.events.push(structuredClone(p.sides[1].result.events[5])); },
    p => { p.sides[1].result.events.pop(); }
  ]) { const prepared = input(); mutate(prepared); assert.throws(() => Comparison.compare(prepared), undefined, mutate.toString()); }
});

test('edition formulary form Bible language cycle alternative options and text presentation remain fixed', () => {
  for (const mutate of [
    p => { p.sides[1].result.request.edition.id = 'roman-pre-1955'; },
    p => { p.sides[1].result.resolved.formulary = 'pentecost'; },
    p => { p.sides[1].result.resolved.form = 'second'; },
    p => { p.sides[1].result.request.bible = { id: 'clementine-vulgate' }; },
    p => { p.sides[1].result.request.languages.orations = 'la'; },
    p => { p.sides[1].result.request.cycle = 'B'; },
    p => { p.sides[1].result.request.alternative = { id: 'not-held' }; },
    p => { p.sides[1].result.request.options.legitimate = { creed: 'nicene' }; },
    p => { p.sides[1].result.request.textDisplay = 'latin-and-selected'; }
  ]) { const prepared = input(); mutate(prepared); assert.throws(() => Comparison.compare(prepared), undefined, mutate.toString()); }
  const crossEdition = input(); crossEdition.comparison.dimension = 'oration-language';
  crossEdition.sides[1].result.request.languages.orations = 'la';
  crossEdition.sides[1].result.request.languages.translationWitness = caswall;
  crossEdition.comparison.sides[1].languages.orations = 'la';
  assert.throws(() => Comparison.compare(crossEdition), /unmapped or unsupported/);
});

test('orchestration preserves source qualification and rejects unknown or canonically duplicate witness aliases', async () => {
  const { result, presentation } = await build(); assert.equal(result.view.units.length, 11);
  assert.deepEqual(presentation.sides.map(side => Array.from(side.witness.relationships)), fixture.expected.sequence.relationships);
  assert.deepEqual(presentation.sides.map(side => Array.from(side.witness.publication_bases)), fixture.expected.sequence.publicationBases);
  assert.deepEqual(presentation.sides.map(side => Array.from(side.witness.collations)), fixture.expected.sequence.collations);
  const unknown = normalize(prefix + '&translation-witness=' + caswall + '&peer-witness=not-held').state;
  await assert.rejects(build(unknown), /distinct held translation witnesses/);
  const alias = normalize(prefix + '&translation-witness=' + caswall + '&peer-witness=artifact.edward-caswall.lyra-catholica.london-1849.missal-sequences-en').state;
  await assert.rejects(build(alias), /distinct held translation witnesses/);
});

test('Sequence coordinates preserve Read place and malformed presentation cells refuse', () => {
  const prepared = input(), result = prepared.sides[0].result;
  const id = 'proper/roman-1962/' + key + '/006';
  assert.deepEqual(PropersCompare.compareLocation({ kind: 'event', id }, result, 'translation-witness'), { kind: 'event', id: 'compare/source/' + id });
  assert.deepEqual(PropersCompare.fromCompareLocation({ kind: 'event', id: 'compare/source/' + id }, result), { kind: 'event', id });
  const view = Comparison.compare(prepared); view.units[5].sides[1].event.id = 'proper/roman-1962/' + key + '/007';
  assert.throws(() => View.project(view), /source coordinate/);
});
