#!/usr/bin/env node
/* A typed structural parent has no missing words; real gaps remain explicit. */
import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';
import vm from 'node:vm';
import {createRequire} from 'node:module';
const require = createRequire(import.meta.url);
const ROOT = process.env.TRIPTYCH_REVIEW_ROOT || path.resolve(import.meta.dirname, '../..');
const CODE = process.env.TRIPTYCH_ORDINARY_MODULE_ROOT || ROOT;
const {repositoryPath} = require(path.join(ROOT, 'tools/tests/_product_data.cjs'));
const dataPath = process.env.TRIPTYCH_ORDINARY_DATA || repositoryPath(ROOT,
  'src/web/data/structure/ordinary/postconciliar.json');
const ordinary = JSON.parse(fs.readFileSync(dataPath, 'utf8'));
const elements = ordinary.sections.flatMap(section => section.elements);
const invitation = elements.find(element => element.key === 'ritus-communionis/ecce-agnus-dei');
const unavailable = elements.find(element => element.key === 'ritus-communionis/perceptio-corporis-et-sanguinis');
const reading = elements.find(element => element.key === 'liturgia-verbi/lectio-prima');
assert.ok(invitation && unavailable && reading);
const dom = require(path.join(ROOT, 'scripts/lectern/dom.js'));
globalThis.window = globalThis; globalThis.document = dom.document;
globalThis.location = {search: '', hash: '', pathname: '/'};
globalThis.history = {replaceState() {}, pushState() {}};
globalThis.addEventListener = () => {};
for (const file of ['shared/browser-core.js', 'liturgy/ordinary-seating.js', 'liturgy/reader-state.js', 'liturgy/reader-state-adapters.js']) {
  vm.runInThisContext(fs.readFileSync(path.join(ROOT, 'src/web/browser', file), 'utf8'));
}
vm.runInThisContext(fs.readFileSync(path.join(CODE, 'src/web/browser/liturgy/day.js'), 'utf8'));
const renderer = TriptychOrdinaryRenderer;
const results = [];
function render(element, file, lang, display, why = false) {
  renderer.configure({ordinaryLang: lang, textDisplay: display, why});
  return renderer.renderElement(element, file);
}
function check(name, run) {run(); results.push(name);}
for (const lang of ['en', 'la']) for (const display of ['selected', 'latin-and-selected']) {
  const state = lang + '/' + display;
  check('actual structural invitation ' + state, () => {
    const node = render(invitation, ordinary, lang, display);
    assert.equal(node.querySelectorAll('.notice').length, 0);
    assert.equal(node.querySelectorAll('.proper-name').length, 1);
    assert.ok(node.textContent.includes(invitation.name));
    assert.equal(node.querySelector('.proper-incipit').textContent, invitation.latin_incipit);
    assert.equal(node.querySelector('.proper-incipit').lang, 'la');
    assert.equal(node.querySelectorAll('.text-side').length, 0);
    assert.ok(render(invitation, ordinary, lang, display, true).textContent.includes(invitation.note));
  });
  check('actual unavailable prayer ' + state, () => {
    const node = render(unavailable, ordinary, lang, display);
    assert.equal(node.querySelectorAll('.notice').length, 2);
    assert.ok(node.textContent.includes('No exact exemplar of this quiet prayer is held here'));
    assert.ok(node.textContent.includes('The older witness differs at the target words'));
    assert.ok(node.textContent.includes(unavailable.latin_incipit));
  });
  check('actual language-specific rights gap ' + state, () => {
    const node = render(reading, ordinary, lang, display);
    assert.equal(node.querySelectorAll('.notice').length, 1);
    assert.ok(node.textContent.includes('Approved English text is not published here'));
    assert.equal(node.textContent.includes('its Latin.'), false);
  });
}
const mutations = [
  ['missing absence binding', (e) => {delete e.absent.english;}],
  ['different not-applicable reason', (e) => {e.absent.english = 'no-fixed-text';}],
  ['missing absence definition', (_e, f) => {f.absences = f.absences.filter(a => a.key !== 'not-a-text');}],
  ['duplicate absence definition', (_e, f) => {f.absences.push({...f.absences.find(a => a.key === 'not-a-text')});}],
  ['missing absence kind', (_e, f) => {delete f.absences.find(a => a.key === 'not-a-text').kind;}],
  ['rights absence kind', (_e, f) => {f.absences.find(a => a.key === 'not-a-text').kind = 'rights-withheld';}],
  ['unresolved absence state', (_e, f) => {f.absences.find(a => a.key === 'not-a-text').state = 'unresolved';}],
  ['scoped rights contradiction', (_e, f) => {f.language_absences.find(a => a.key === 'not-a-text' && a.lang === 'en').kind = 'rights-withheld';}],
  ['missing scoped definition', (_e, f) => {f.language_absences = f.language_absences.filter(a => a.key !== 'not-a-text' || a.lang !== 'en');}],
  ['missing coverage', (e) => {delete e.coverage;}],
  ['unversioned coverage', (e) => {delete e.coverage.schema;}],
  ['missing language coverage', (e) => {e.coverage.languages = e.coverage.languages.filter(a => a.lang !== 'en');}],
  ['malformed language coverage', (e) => {e.coverage.languages = {};}],
  ['duplicate language coverage', (e) => {e.coverage.languages.push({...e.coverage.languages.find(a => a.lang === 'en')});}],
  ['unavailable coverage', (e) => {e.coverage.languages.find(a => a.lang === 'en').availability = 'not-sourced';}],
  ['duplicate language descriptor', (_e, f) => {f.languages.push({...f.languages.find(a => a.lang === 'en')});}]
];
for (const [name, mutate] of mutations) for (const display of ['selected', 'latin-and-selected']) {
  check(name + '/' + display, () => {
    const element = structuredClone(invitation), file = structuredClone(ordinary);
    mutate(element, file);
    const node = render(element, file, 'en', display);
    assert.ok(node.querySelectorAll('.notice').length > 0);
    assert.ok(node.textContent.includes('its English.'));
    assert.ok(node.textContent.includes(invitation.name));
  });
}
for (const display of ['selected', 'latin-and-selected']) {
  check('contradictory held text survives/' + display, () => {
    const element = structuredClone(invitation);
    element.translations = [{lang: 'en', text: 'Synthetic held words.', rights: 'public-domain'}];
    const node = render(element, ordinary, 'en', display);
    assert.ok(node.textContent.includes('Synthetic held words.'));
  });
  check('language-specific structural side retains cue/' + display, () => {
    const element = structuredClone(invitation);
    element.absent.english = 'approved-english-publication-restriction';
    element.coverage.languages.find(a => a.lang === 'en').availability = 'not-publishable';
    const node = render(element, ordinary, 'en', display);
    assert.equal(node.querySelectorAll('.notice').length, 1);
    assert.ok(node.textContent.includes('Approved English text is not published here'));
    assert.equal(node.querySelector('.proper-incipit').textContent, invitation.latin_incipit);
  });
}
console.log(JSON.stringify({state: 'pass', checks: results.length, results}, null, 2));
