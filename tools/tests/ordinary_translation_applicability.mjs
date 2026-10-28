#!/usr/bin/env node
/* A held day-form witness needs an appointed formulary before execution. */
import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';
import vm from 'node:vm';
import { createRequire } from 'node:module';
const require = createRequire(import.meta.url);
const ROOT = process.env.TRIPTYCH_REVIEW_ROOT || path.resolve(import.meta.dirname, '../..');
const CODE = process.env.TRIPTYCH_ORDINARY_MODULE_ROOT || ROOT;
const A = require(path.join(CODE, 'src/web/browser/liturgy/reader-state-adapters.js'));
const C = require(path.join(ROOT, 'src/web/browser/liturgy/reader-state.js'));
const ordinary = JSON.parse(fs.readFileSync(process.env.TRIPTYCH_ORDINARY_DATA ||
  path.join(ROOT, 'src/web/data/structure/ordinary/roman-1962.json'), 'utf8'));
const structure = JSON.parse(fs.readFileSync(path.join(ROOT, 'src/web/data/structure/propers/roman-1962.json'), 'utf8'));
const head = ordinary.sections.flatMap(s => s.elements).find(e => e.key === 'canon/communicantes-pascha');
const source = head.translations.find(t => t.lang === 'en');
assert.equal(source.applicability.kind, 'formulary');
assert.equal(source.applicability.calendar, 'roman-1962');
assert.deepEqual(source.applicability.formularies, ['easter-sunday', 'easter-monday', 'easter-tuesday',
  'easter-wednesday', 'easter-thursday', 'easter-friday', 'easter-saturday']);
for (const context of [undefined, null, {}, {calendar: 'roman-1962'},
  {calendar: 'roman-1962', formulary: 'unknown'}, {calendar: 'roman-1962', formulary: 'easter-vigil'},
  {calendar: 'postconciliar', formulary: 'easter-sunday'},
  {calendar: 'roman-1962', formulary: 'easter-sunday', time: 'day'}]) {
  for (const witness of [null, source.source_id]) {
    const selected = A.selectOrdinaryTranslation(head, ordinary, 'en', witness, context);
    assert.equal(selected.availability, 'unavailable');
    assert.equal(selected.text, null);
    assert.equal(selected.sourceId, null);
    assert.deepEqual(C.validateSelectedMaterial(selected), []);
  }
}
for (const formulary of source.applicability.formularies) {
  assert.equal(A.selectOrdinaryTranslation(head, ordinary, 'en', null,
    {calendar: 'roman-1962', formulary}).text, source.text);
}
for (const applicability of [null, {}, [], {...source.applicability, time: 'day'},
  {...source.applicability, formularies: []}, {...source.applicability, basis: ''}]) {
  const bad = structuredClone(head);
  bad.translations.find(t => t.lang === 'en').applicability = applicability;
  assert.throws(() => A.selectOrdinaryTranslation(bad, ordinary, 'en'), /malformed Ordinary/);
}
const latin = head.translations.find(t => t.lang === 'la');
assert.equal(A.selectOrdinaryTranslation(head, ordinary, 'la').text, latin.text);
function request(id) {
  return {schema: 'triptych-liturgy-reader-state/v1', entrance: 'propers', civilDate: null,
    edition: {id: 'roman-1962'}, formulary: {id}, bible: {id: 'douay-rheims', numbering: 'vulgate'},
    languages: {orations: 'la', ordinary: 'en'}, requestedMode: 'missal',
    options: {ordinary: true, legitimate: {}}, coverage: [], unresolvedChoices: [], sourceHooks: []};
}
for (const key of ['easter-sunday', 'easter-monday', 'easter-saturday', 'easter-vigil', 'ascension', 'pentecost']) {
  const result = A.adaptPropers({request: request(key), ordinary, structure});
  const events = result.events.filter(e => e.kind === 'ordinary-element');
  if (key === 'easter-vigil') assert.equal(events.length, 0);
  else {
    assert.ok(events.length > 0);
    assert.equal(events.find(e => e.id.endsWith('/communicantes-continuatio')).selected.text, null);
    const selected = events.find(e => e.id.endsWith('/communicantes-pascha'))?.selected;
    if (key.startsWith('easter-')) assert.equal(selected.text, source.text);
  }
}
// Use the actual production presenter for selected and paired output.
const dom = require(path.join(ROOT, 'scripts/lectern/dom.js'));
globalThis.window = globalThis; globalThis.document = dom.document;
globalThis.location = {search: '', hash: '', pathname: '/'};
globalThis.history = {replaceState() {}, pushState() {}}; globalThis.addEventListener = () => {};
for (const file of ['shared/browser-core.js', 'liturgy/ordinary-seating.js']) {
  vm.runInThisContext(fs.readFileSync(path.join(ROOT, 'src/web/browser', file), 'utf8'));
}
globalThis.LiturgyReaderStateAdapters = A;
vm.runInThisContext(fs.readFileSync(path.join(CODE, 'src/web/browser/liturgy/day.js'), 'utf8'));
for (const textDisplay of ['selected', 'latin-and-selected']) {
  TriptychOrdinaryRenderer.configure({ordinaryLang: 'en', textDisplay});
  for (const formulary of [null, 'easter-vigil', 'easter-sunday']) {
    const context = formulary && {calendar: 'roman-1962', formulary};
    const node = TriptychOrdinaryRenderer.renderElement(head, ordinary, undefined, context);
    assert.equal(node.textContent.includes(source.text), formulary === 'easter-sunday');
    const rawOptions = TriptychOrdinaryRenderer.renderElement(head, ordinary,
      {language: 'en', held: source}, context);
    assert.equal(rawOptions.textContent.includes(source.text), formulary === 'easter-sunday');
  }
}
console.log('Ordinary translation applicability: selector, appointed seating, and production DOM controls passed');
