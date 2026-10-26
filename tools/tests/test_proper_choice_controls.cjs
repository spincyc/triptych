'use strict';
// Isolated DOM and exact production-function checks. Synthetic text is private
// contract evidence, and this file makes no browser or source-edition claim.
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');
const candidateRoot = path.resolve(process.argv[2] || path.join(__dirname, '../..'));
const uiRoot = path.resolve(process.argv[3] || candidateRoot);
const moduleRoot = path.join(candidateRoot, 'src/web/browser/liturgy');
const uiModuleRoot = path.join(uiRoot, 'src/web/browser/liturgy');
const C = require(path.join(moduleRoot, 'reader-state.js'));
const A = require(path.join(moduleRoot, 'reader-state-adapters.js'));
const S = require(path.join(moduleRoot, 'ordinary-seating.js'));
const Share = require(path.join(moduleRoot, 'reader-share-print.js'));
const source = (name) => fs.readFileSync(path.join(uiModuleRoot, name), 'utf8');
const daySource = source('day-reader.js');
const propersSource = source('propers-reader.js');
const results = [];
function test(name, run) { run(); results.push(name); }
const clone = (value) => JSON.parse(JSON.stringify(value));
function exactFunction(sourceText, name) {
  const match = new RegExp('^  (?:async )?function ' + name + '\\(', 'm').exec(sourceText);
  assert(match, 'missing production function ' + name);
  const end = sourceText.indexOf('\n  }\n', match.index);
  assert(end > match.index, 'missing function boundary ' + name);
  return sourceText.slice(match.index, end + 5);
}
class Element {
  constructor(tag) {
    this.tagName = tag.toUpperCase(); this.children = []; this.dataset = {};
    this.attributes = {}; this.listeners = {}; this.className = '';
    this.textContent = ''; this.checked = false; this.disabled = false;
    this.classList = {add: (...names) => {
      this.className = [...new Set(this.className.split(/\s+/).filter(Boolean).concat(names))].join(' ');
    }};
  }
  appendChild(node) { this.children.push(node); node.parentElement = this; return node; }
  get firstChild() { return this.children[0] || null; }
  insertBefore(node, before) {
    const at = before ? this.children.indexOf(before) : this.children.length;
    assert(at >= 0); this.children.splice(at, 0, node); node.parentElement = this; return node;
  }
  before(node) { this.parentElement.insertBefore(node, this); }
  closest(selector) {
    for (let node = this; node; node = node.parentElement)
      if (selector === '[data-option-group]' && node.dataset.optionGroup) return node;
    return null;
  }
  setAttribute(key, value) { this.attributes[key] = value; }
  addEventListener(name, fn) { (this.listeners[name] ||= []).push(fn); }
  dispatch(name) { (this.listeners[name] || []).forEach((fn) => fn({target: this})); }
  querySelectorAll(selector) { return descendants(this).filter((node) => selector === '[data-semantic-location]'
    ? node.dataset.semanticLocation : selector === '[data-semantic-event-id]' ? node.dataset.semanticEventId
    : selector === '[data-option-group]' ? node.dataset.optionGroup
    : selector === 'input[type="radio"]' ? node.tagName === 'INPUT' && node.type === 'radio'
    : selector === '[data-option-group] input[type="radio"]' ? node.tagName === 'INPUT' && node.type === 'radio' && node.closest('[data-option-group]') : false); }
  querySelector(selector) { return this.querySelectorAll(selector)[0] || null; }
  focus(options) { this.focused = options; }
  scrollIntoView(options) { this.scrolled = options; }
}
function descendants(node) { return node.children.flatMap((child) => [child, ...descendants(child)]); }
const radios = (node) => descendants(node).filter((child) => child.tagName === 'INPUT');
const members = (node) => descendants(node).filter((child) => child.dataset.properChoiceMemberEvent);
function environment() {
  const rendered = [];
  const T = {
    SOURCE_LANGUAGE: 'la',
    titleCase: (text) => text.replace(/\b\w/g, (char) => char.toUpperCase()),
    isPlaceholder: () => false,
    el(tag, cls, text) { const node = new Element(tag); node.className = cls || ''; node.textContent = text || ''; return node; },
    renderProper(proper, bible, fragments, options) {
      rendered.push({proper, bible, fragments, options});
      const node = new Element('section'); node.textContent = proper.text || '';
      return node;
    }
  };
  const context = {Triptych: T, OrdinarySeating: S, LiturgyReaderStateAdapters: A,
    document: {createElement: (tag) => new Element(tag), createTextNode: (text) => {
      const node = new Element('#text'); node.textContent = text; return node;
    }}, URLSearchParams, URL, console};
  context.window = context;
  vm.createContext(context);
  vm.runInContext(source('source-choice-controls.js'), context);
  vm.runInContext(source('reader-shell.js'), context);
  vm.runInContext(source('propers-events.js'), context);
  return {context, T, rendered, Shell: context.TriptychReaderShell};
}

const edition = 'roman-1962';
const massKey = 'contract-formulary';
const groupId = (group) => 'proper-choice/' + edition + '/' + massKey + '/main/' + group;
const acclamation = groupId('common-acclamation');
const gospel = groupId('gospel-reading');
function fixture() {
  const coordinate = (proper) => ({mass: 'contract-common', form_id: 'main', proper, occurrence: 1});
  const names = ['Introit', 'Collect', 'Epistle', 'Gradual', 'Alleluia', 'Tract',
    'Alleluia (Tempore paschali)', 'Alleluia (second constituent)', 'Gospel',
    'Offertory', 'Secret', 'Communion', 'Postcommunion', 'Gospel (additional reading)'];
  const propers = names.map((name) => ({name, form: '', form_id: 'main', source: 'composed',
    text: 'Synthetic contract member: ' + name, citations: [], cycles: {}, translations: [], taken_from: null}));
  propers[3].appointment_identity = coordinate('Gradual');
  propers[3].ordinary_disposition = {kind: 'conditional', group: 'common-gradual',
    basis: 'Synthetic source conditional rule.', when: {fact: 'contract-regime', in: ['regular', 'tract']}};
  [[4, 'regular', ['regular']], [5, 'tract', ['tract']], [6, 'paschal', ['paschal']],
    [7, 'paschal', ['paschal']]].forEach(([index, option, values]) => {
    propers[index].appointment_identity = coordinate(names[index]);
    propers[index].ordinary_disposition = {kind: 'alternative', group: 'common-acclamation', option,
      basis: 'Synthetic acclamation alternatives.', anchor: coordinate('Alleluia'),
      when: {fact: 'contract-regime', in: values}};
  });
  [[8, 'principal'], [13, 'additional']].forEach(([index, option]) => {
    propers[index].appointment_identity = coordinate(names[index]);
    propers[index].ordinary_disposition = {kind: 'alternative', group: 'gospel-reading', option,
      basis: 'Synthetic distant source alternatives.', anchor: coordinate('Gospel')};
  });
  return {calendar: edition, translations: [], masses: [{key: massKey, kind: 'common', propers}],
    proper_appointment_facts: {'contract-regime': {edition, values: ['regular', 'tract', 'paschal'],
      season_values: {epiphanytide: 'regular', lent: 'tract', paschaltide: 'paschal'},
      basis: 'Synthetic owner fact binding.'}}};
}
function request(entrance = 'propers') {
  const state = {schema: C.STATE_SCHEMA, entrance, edition: {id: edition},
    bible: {id: 'douay-rheims', numbering: 'vulgate'}, languages: {orations: 'la'},
    requestedMode: 'read', options: {ordinary: false, legitimate: {}},
    coverage: [], unresolvedChoices: [], sourceHooks: []};
  if (entrance === 'day') Object.assign(state, {civilDate: '2026-04-15', calendar: {id: edition},
    apparatus: {why: false, rubrics: true}});
  else Object.assign(state, {civilDate: null, formulary: {id: massKey, type: 'common'}});
  return state;
}
function derived() {
  return {calendar: edition, date: '2026-04-15', weekday: 'wednesday', season: 'paschaltide',
    liturgicalYear: {lectionary: null, anchors: {}}, options: [{option: null, settled: true,
      winner: {id: massKey, nature: 'feast'}, readable: [{key: massKey, state: 'said'}], absent: []}]};
}
const eventOf = (result, group) => result.events.find((event) => event.kind === 'proper-choice' && event.group === group);
function propersView(state, wanted = 'common-acclamation') {
  const structure = fixture(), env = environment(), navigation = [];
  const result = A.adaptPropers({request: state, structure});
  const renderer = env.context.TriptychPropersEvents.create({
    navigate: (...args) => navigation.push(clone(args)), sourceIndex: (event) => {
      const hook = event.sourceHooks.find((row) => row.kind === 'proper-structure');
      return Number(hook.id.slice(-3)) - 1;
    }, publicKeys: {cycle: 'cycle'}, legacyKeys: {cycle: '_candidate-cycle'},
    getStructure: () => structure, getOrdinary: () => null
  });
  const event = eventOf(result, wanted);
  const node = renderer.renderProperChoiceEvent(event, structure.masses[0], {}, {}, state);
  return {...env, node, event, result, structure, navigation};
}
function dayView(state, wanted = 'common-acclamation', prefix = '') {
  const structure = fixture(), env = environment(), navigation = [];
  const d = derived(), result = A.adaptDay({request: state, structure, derived: d});
  Object.assign(env.context, {T: env.T, Adapters: A, Shell: env.Shell,
    runtime: {derived: d, structure, ordinary: null},
    navigate: (...args) => navigation.push(clone(args)),
    renderTranslationWitnessChoice: () => null, resolvableTranslationWitnessState: () => ({})});
  ['sourceIndex', 'semanticNode', 'validateProperChoiceEvent', 'properChoiceLabel',
    'renderProperMaterial', 'renderProperChoiceEvent'].forEach((name) => {
    vm.runInContext(exactFunction(daySource, name), env.context);
  });
  const event = eventOf(result, wanted);
  const node = env.context.renderProperChoiceEvent(event, structure.masses[0], structure,
    {}, {}, state, 'h2', 'h4', prefix, result, 3, false);
  return {...env, node, event, result, structure, navigation};
}

test('Propers renders native unselected radios and every unchanged source body', () => {
  const view = propersView(request());
  const fields = descendants(view.node).filter((node) => node.tagName === 'FIELDSET');
  assert.equal(fields.length, 1);
  assert.equal(fields[0].children[0].tagName, 'LEGEND');
  assert.match(fields[0].className, /\bordinary-choice\b/);
  const inputs = radios(view.node);
  assert.deepEqual(inputs.map((input) => input.value), ['regular', 'tract', 'paschal']);
  assert(inputs.every((input) => input.type === 'radio' && !input.checked && !input.disabled));
  assert.equal(new Set(inputs.map((input) => input.name)).size, 1);
  assert(inputs.every((input) => input.parentElement.tagName === 'LABEL'));
  assert(inputs.every((input) => input.tabIndex === undefined && !input.listeners.keydown));
  assert.equal(members(view.node).length, 4);
  assert.deepEqual(view.rendered.map((row) => row.proper),
    [4, 5, 6, 7].map((index) => view.structure.masses[0].propers[index]));
  assert(view.rendered.every((row) => row.options.heading === 'h4'));
  assert.equal(view.node.dataset.semanticEventId, acclamation);
  assert.equal(view.node.tabIndex, -1);
  assert.equal(view.node.attributes['aria-labelledby'], view.node.children[0].id);
  inputs[0].dispatch('change');
  assert.equal(view.navigation.length, 0);
  Object.assign(view.context, {reading: {querySelectorAll: () => [view.node]}});
  ['eventLocation', 'focusCommittedResult'].forEach((name) =>
    vm.runInContext(exactFunction(propersSource, name), view.context));
  view.context.focusCommittedResult('event', {kind: 'event', id: acclamation});
  assert.equal(view.node.focused.preventScroll, true);
});
test('independent radio groups accumulate selections and migrate the legacy scalar', () => {
  const state = request(); state.alternative = {id: gospel + '/additional'};
  const before = JSON.stringify(state);
  const view = propersView(state);
  const paschal = radios(view.node).find((input) => input.value === 'paschal');
  paschal.checked = true; paschal.dispatch('change');
  assert.equal(view.navigation.length, 1);
  const [updates, removals, intent] = view.navigation[0];
  const choices = JSON.parse(updates['proper-choices']);
  assert.deepEqual(choices, {[gospel]: 'additional', [acclamation]: 'paschal'});
  assert.deepEqual(removals, ['alternative', '_candidate-alternative']);
  assert.deepEqual(intent, {location: {kind: 'event', id: acclamation}, focus: 'event'});
  assert.equal(JSON.stringify(state), before);
  const next = {...request(), properChoices: choices};
  const second = propersView(next, 'gospel-reading');
  const principal = radios(second.node).find((input) => input.value === 'principal');
  principal.checked = true; principal.dispatch('change');
  const changed = JSON.parse(second.navigation[0][0]['proper-choices']);
  assert.deepEqual(changed, {[gospel]: 'principal', [acclamation]: 'paschal'});
  assert.notEqual(radios(view.node)[0].name, principal.name);
  assert.equal(eventOf(A.adaptPropers({request: {...request(), properChoices: changed}, structure: fixture()}),
    'common-acclamation').selection.option, 'paschal');
});
test('selected option leads while all other source bodies remain collapsed with their identities', () => {
  const state = request(); state.properChoices = {[acclamation]: 'paschal'};
  for (const view of [propersView(state), dayView({...request('day'), properChoices: state.properChoices})]) {
    const options = descendants(view.node).filter((node) => node.dataset.properChoiceOption);
    assert.deepEqual(options.map((node) => node.dataset.properChoiceOption), ['paschal', 'regular', 'tract']);
    assert.equal(options[0].tagName, 'SECTION');
    assert.equal(options[0].attributes['aria-current'], 'true');
    assert(options.slice(1).every((node) => node.tagName === 'DETAILS' && node.children[0].tagName === 'SUMMARY'));
    assert.equal(members(view.node).length, 4);
    assert.equal(new Set(members(view.node).map((node) => node.dataset.properChoiceMemberEvent)).size, 4);
    assert.equal(radios(view.node).filter((input) => input.checked).length, 1);
  }
});
test('Day adapter disables incompatible source options and no disabled control navigates', () => {
  const view = dayView(request('day'));
  const inputs = radios(view.node);
  assert.deepEqual(inputs.map((input) => [input.value, input.disabled, input.checked]),
    [['regular', true, false], ['tract', true, false], ['paschal', false, true]]);
  assert.equal(members(view.node).length, 4);
  for (const input of inputs.filter((radio) => radio.disabled)) {
    assert.match(input.parentElement.children[1].textContent, /unavailable for this context/);
    input.checked = true; input.dispatch('change');
  }
  assert.equal(view.navigation.length, 0);
  const selected = inputs.find((input) => input.value === 'paschal');
  selected.dispatch('change');
  assert.equal(view.navigation.length, 1);
  assert.deepEqual(JSON.parse(view.navigation[0][0]['proper-choices']), {[acclamation]: 'paschal'});
});
test('Day choice preserves prefixed group location and the existing result-focus path', () => {
  const view = dayView(request('day'), 'gospel-reading', 'territory/contract/');
  const input = radios(view.node).find((radio) => radio.value === 'additional');
  input.checked = true; input.dispatch('change');
  const target = 'territory/contract/' + gospel;
  assert.deepEqual(view.navigation[0][2], {location: {kind: 'event', id: target},
    focus: {kind: 'proper-choice-result', event: target}});
  assert.equal(view.node.dataset.semanticLocation, target);
  assert(view.rendered.every((row) => row.options.heading === 'h4'));
  const restored = [];
  Object.assign(view.context, {reading: view.node.parentElement || {
    querySelectorAll: () => [view.node], querySelector: () => view.node
  }, readerShell: {restoreSemanticLocation: (value) => { restored.push(value); return true; }}});
  vm.runInContext(exactFunction(daySource, 'restorePendingNavigation'), view.context);
  view.context.restorePendingNavigation(view.navigation[0][2]);
  assert.equal(restored[0].id, target);
  assert.equal(view.node.focused.preventScroll, true);
});

function navContext(entrance, state, initialHash) {
  const env = environment(), pushes = [];
  const location = {pathname: '/liturgy/' + (entrance === 'day' ? 'day.html' : 'index.html'),
    search: '?contract=1', hash: initialHash, href: 'https://example.test/liturgy/' +
      (entrance === 'day' ? 'day.html' : 'index.html') + initialHash};
  const history = {state: {}, replaceState(value) { this.state = value; },
    pushState(value, _, url) { this.state = value; pushes.push(url); }};
  Object.assign(env.context, {Shell: env.Shell, Contract: C, runtime: {normalized: {state}, mode: 'read'},
    history, location, readerShell: {captureSemanticLocation: () => ({kind: 'event', id: gospel})},
    renderCandidate: () => {}, dayReaderDebug: {}});
  const text = entrance === 'day' ? daySource : propersSource;
  (entrance === 'day' ? ['hashWith', 'navigate'] : ['eventLocation', 'internalHash', 'navigate'])
    .forEach((name) => vm.runInContext(exactFunction(text, name), env.context));
  return {...env, pushes};
}
test('both actual navigation functions retain choices and clear them on every identity change', () => {
  for (const entrance of ['day', 'propers']) {
    const state = request(entrance); state.properChoices = {[acclamation]: 'paschal', [gospel]: 'additional'};
    const hash = '#proper-choices=' + encodeURIComponent(JSON.stringify(state.properChoices)) +
      '&alternative=old&_candidate-alternative=old';
    const same = navContext(entrance, state, hash);
    same.context.navigate({bible: 'vulgate'}, [], {location: {kind: 'event', id: gospel}, focus: 'event'});
    assert.deepEqual(JSON.parse(new URLSearchParams(same.pushes[0].split('#')[1]).get('proper-choices')), state.properChoices);
    const changes = entrance === 'day' ? [{date: '2026-04-16'}, {missal: 'postconciliar'}, {mass: 'other'}, {form: 'other'}, {cycle: 'C'}]
      : [{missal: 'postconciliar'}, {type: 'other'}, {mass: 'other'}, {form: 'other'}, {cycle: 'C'}];
    for (const update of changes) {
      const next = navContext(entrance, state, hash);
      next.context.navigate(update, [], {location: null});
      const params = new URLSearchParams(next.pushes[0].split('#')[1]);
      for (const key of ['proper-choices', 'alternative', '_candidate-alternative']) assert.equal(params.has(key), false, key);
    }
    const removedForm = navContext(entrance, state, hash);
    removedForm.context.navigate({}, ['form'], {location: null});
    assert.equal(new URLSearchParams(removedForm.pushes[0].split('#')[1]).has('proper-choices'), false);
    const choose = navContext(entrance, state, hash);
    choose.context.navigate({'proper-choices': JSON.stringify(state.properChoices)}, ['alternative', '_candidate-alternative'],
      {location: {kind: 'event', id: gospel}, focus: 'event'});
    const params = new URLSearchParams(choose.pushes[0].split('#')[1]);
    assert.deepEqual(JSON.parse(params.get('proper-choices')), state.properChoices);
    assert.equal(params.get('location'), gospel);
    assert.equal(params.has('alternative') || params.has('_candidate-alternative'), false);
  }
});
const validationContext = {missals: {[edition]: {calendar: edition, types: {common: [massKey]},
  formsByMass: {[massKey]: []}, orationLanguages: ['la'], ordinaryLanguages: [], variantGroups: {}}},
  bibles: {'douay-rheims': {numbering: 'vulgate'}}, dayReadableFormularies: [{id: massKey}]};
test('Propers controller manual legacy handling preserves the canonical multi-choice map', () => {
  const env = environment(), state = request(); state.properChoices = {[acclamation]: 'paschal', [gospel]: 'additional'};
  const hash = C.serializeLegacy({ok: true, state, legacy: {variants: {}, unknown: [], inert: []}});
  Object.assign(env.context, {Contract: C, T: env.T, location: {hash},
    PUBLIC_KEYS: {cycle: 'cycle', alternative: 'alternative', translationWitness: 'translation-witness'},
    LEGACY_KEYS: {cycle: '_candidate-cycle', alternative: '_candidate-alternative', translationWitness: '_candidate-translation-witness'},
    formularyWitnessState: () => ({held: [], deterministic: null})});
  ['explicitValues', 'explicitSemanticValue', 'normalizedState'].forEach((name) =>
    vm.runInContext(exactFunction(propersSource, name), env.context));
  const errors = [], normalized = env.context.normalizedState({parsed: C.parseLegacy('propers', hash),
    remembered: {}, defaults: {}, structure: fixture()}, validationContext, errors);
  assert.equal(normalized.ok, true, JSON.stringify(normalized.errors));
  assert.deepEqual(clone(normalized.state.properChoices), state.properChoices);
  assert.deepEqual(errors, []);
});
test('canonical Day and Propers selection maps survive share and presentation URLs', () => {
  for (const entrance of ['day', 'propers']) {
    const state = request(entrance); state.properChoices = {[gospel]: 'additional', [acclamation]: 'paschal'};
    const hash = C.serializeLegacy({ok: true, state, legacy: {variants: {}, unknown: [], inert: []}});
    const normalized = C.normalizeLegacy(C.parseLegacy(entrance, hash), {context: validationContext});
    assert.equal(normalized.ok, true, JSON.stringify(normalized.errors));
    const url = Share.canonicalUrl(entrance, {href: 'https://example.test/liturgy/' +
      (entrance === 'day' ? 'day-reader.html' : 'propers-reader.html') + hash}, C);
    assert.equal(new URL(url).hash, hash);
    assert.deepEqual(JSON.parse(new URLSearchParams(new URL(url).hash.slice(1)).get('proper-choices')), state.properChoices);
    assert.equal(C.serializeLegacy(normalized), hash);
    for (const changed of [Share.textDisplayUrl({href: url}, 'latin-and-selected'),
      Share.scriptureCompanionUrl({href: url}, 'clementine-vulgate')]) {
      assert.deepEqual(JSON.parse(new URLSearchParams(new URL(changed).hash.slice(1)).get('proper-choices')), state.properChoices);
    }
  }
});
test('browse-only explicit source choices fail before canonicalization', () => {
  const parsed = C.parseLegacy('propers', '#missal=roman-1962&proper-choices=' + encodeURIComponent(JSON.stringify({[gospel]: 'principal'})));
  const result = A.browseState({parsed, missal: edition}, validationContext);
  assert.equal(result.ok, false);
  assert.equal(result.errors[0].path, 'proper-choices');
  assert.match(propersSource, /normalized = browseState\(prepared, context\)/);
});
test('existing print rules hide native controls and the Day controller stays within its cap', () => {
  const css = fs.readFileSync(path.join(moduleRoot, 'reader-instrument.css'), 'utf8');
  assert.match(css.slice(css.indexOf('@media print')), /\.reader-instrument \.ordinary-choice/);
  assert(Buffer.byteLength(daySource) <= 126976);
  for (const name of ['source-choice-controls.js', 'reader-shell.js', 'propers-events.js', 'day-reader.js', 'propers-reader.js'])
    new vm.Script(source(name), {filename: name});
});

test('both entrances load the single control owner before the thin shell and match expected asset hashes', () => {
  const crypto = require('node:crypto');
  // Scratch candidates may supply a nonauthoritative local inventory fixture;
  // root owns regeneration of the actual publication bindings before landing.
  const inventory = JSON.parse(fs.readFileSync(path.join(uiRoot, 'release/public-alpha.json'), 'utf8'));
  function sourceHash(object, wanted) {
    if (!object || typeof object !== 'object') return [];
    return Object.entries(object).flatMap(([key, value]) =>
      key === wanted ? [value] : sourceHash(value, wanted));
  }
  const helperTag = '<script src="source-choice-controls.js"></script>';
  const shellTag = '<script src="reader-shell.js"></script>';
  for (const name of ['day.html', 'day-reader.html', 'index.html', 'propers-reader.html', 'reader-visual-reset-day.html', 'reader-visual-reset-propers.html']) {
    const page = source(name);
    assert.equal(page.split(helperTag).length - 1, 1);
    assert(page.indexOf(helperTag) < page.indexOf(shellTag));
  }
  for (const name of ['source-choice-controls.js', 'reader-shell.js', 'day.html', 'day-reader.html', 'index.html', 'propers-reader.html', 'reader-visual-reset-day.html', 'reader-visual-reset-propers.html']) {
    const key = 'src/web/browser/liturgy/' + name;
    assert.deepEqual(sourceHash(inventory, key), [crypto.createHash('sha256').update(source(name)).digest('hex')]);
  }
  for (const name of ['properChoiceRequest', 'properChoiceRemovals', 'renderProperChoice'])
    assert.equal(source('reader-shell.js').includes('function ' + name + '('), false);
});

test('only the retained Propers visual oracle may omit the production Mass form controls', () => {
  const declaration = propersSource.slice(propersSource.indexOf("  const massFormField ="),
    propersSource.indexOf("  const bibleSelect ="));
  function initialize(pathname, field, select) {
    return vm.runInNewContext(`(() => { ${declaration}; return Boolean(massFormField && massFormSelect); })()`, {
      window: {location: {pathname}}, document: {getElementById(id) {
        return id === 'reader-mass-form-field' ? field : select;
      }}
    });
  }
  for (const route of ['/liturgy/index.html', '/liturgy/propers-reader.html']) {
    assert.equal(initialize(route, {}, {}), true);
    for (const controls of [[null, null], [{}, null], [null, {}]])
      assert.throws(() => initialize(route, ...controls), /Mass form controls/);
  }
  const oracle = '/liturgy/reader-visual-reset-propers.html';
  assert.equal(initialize(oracle, null, null), false);
  assert.throws(() => initialize(oracle, {}, null), /Mass form controls/);
  assert.throws(() => initialize(oracle, null, {}), /Mass form controls/);
});

test('dedicated CommonJS controls retain browser DOM, legacy migration, and disabled Day negatives', () => {
  const commonJS = require(path.join(uiModuleRoot, 'source-choice-controls.js'));
  assert.deepEqual(Object.keys(commonJS).sort(), ['attachSourcePathChoices', 'createDayDateControls',
    'properChoiceRemovals', 'renderProperChoice']);
  function snapshot(node) {
    return {tag: node.tagName, className: node.className, dataset: {...node.dataset},
      attributes: {...node.attributes}, text: node.textContent, id: node.id || null,
      type: node.type || null, name: node.name || null, value: node.value || null,
      checked: node.checked, disabled: node.disabled, children: node.children.map(snapshot)};
  }
  for (const entrance of ['propers', 'day']) {
    const state = request(entrance);
    if (entrance === 'propers') state.alternative = {id: gospel + '/additional'};
    else state.properChoices = {[gospel]: 'additional'};
    const view = entrance === 'propers' ? propersView(state) : dayView(state);
    const wrapper = view.T.el('section', 'proper-choice');
    wrapper.dataset.semanticLocation = view.event.id;
    wrapper.dataset.semanticEventId = view.event.id;
    wrapper.tabIndex = -1;
    if (view.node.id) wrapper.id = view.node.id;
    const calls = [];
    const previous = globalThis.document;
    globalThis.document = view.context.document;
    try {
      commonJS.renderProperChoice({T: view.T, event: view.event, selected: view.event.selection.option,
        wrapper, titleId: view.node.children[0].id, heading: 'h2', optionHeading: 'h3',
        label: view.node.children[0].textContent, state,
        location: {kind: 'event', id: view.event.id}, focus: 'event',
        navigate: (...args) => calls.push(clone(args)), adapt: (next) => entrance === 'day'
          ? A.adaptDay({request: next, structure: view.structure, derived: derived()})
          : A.adaptPropers({request: next, structure: view.structure}),
        renderMember: (member) => {
          const hook = member.sourceHooks.find((row) => row.kind === 'proper-structure');
          const proper = view.structure.masses[0].propers[Number(hook.id.slice(-3)) - 1];
          return view.T.renderProper(proper, {}, {}, {heading: 'h4'});
        }});
      assert.deepEqual(snapshot(wrapper), snapshot(view.node));
      for (const input of radios(wrapper).filter((input) => input.disabled)) {
        input.checked = true; input.dispatch('change');
      }
      assert.equal(calls.length, 0);
      const paschal = radios(wrapper).find((input) => input.value === 'paschal');
      paschal.checked = true; paschal.dispatch('change');
      assert.equal(calls.length, 1);
      assert.deepEqual(JSON.parse(calls[0][0]['proper-choices']), {[gospel]: 'additional', [acclamation]: 'paschal'});
      assert.deepEqual(calls[0][1], ['alternative', '_candidate-alternative']);
      for (const updates of [{date: '2026-04-16'}, {missal: 'postconciliar'}, {form: 'other'}])
        assert.deepEqual(commonJS.properChoiceRemovals(state, updates, []),
          clone(view.Shell.properChoiceRemovals(state, updates, [])));
    } finally {
      if (previous === undefined) delete globalThis.document;
      else globalThis.document = previous;
    }
  }
});

const relationId = groupId('correlated-readings');
const owned = [groupId('coupled-first-reading'), groupId('coupled-gospel')];
const firstEvent = 'proper/roman-1962/contract-formulary/001';
const nextEvent = 'proper/roman-1962/contract-formulary/002';
function sourcePathView(options = {}) {
  const env = environment(), node = new Element('div'), navigation = [], probes = [];
  const prefix = options.prefix || '';
  for (const id of [firstEvent, nextEvent]) {
    const body = new Element('section'); body.textContent = 'Existing qualified source body ' + id;
    body.dataset.semanticEventId = id; body.dataset.semanticLocation = prefix + id; node.appendChild(body);
  }
  const independent = propersView({...request(), properChoices: {[gospel]: 'additional'}}, 'gospel-reading');
  node.appendChild(independent.node);
  const eventIds = node.querySelectorAll('[data-semantic-event-id]').map((row) => row.dataset.semanticEventId);
  const paths = ['common', 'optional-shorter', 'wrong', 'candidate-unknown', 'false', 'unknown'].map((id) => ({
    id, standing: id === 'common' ? 'principal' : 'optional',
    choices: {[owned[0]]: id === 'optional-shorter' ? 'shorter' : 'longer',
      [owned[1]]: id === 'optional-shorter' ? 'shorter' : 'longer'},
    condition: id === 'unknown' ? {fact: 'held-source-condition', in: ['transferred']} : null,
    applicability: {state: id === 'false' ? 'inapplicable' : id === 'unknown' ? 'unresolved' : 'applicable',
      reason: id === 'unknown' ? 'source-condition-unresolved' : null}}));
  const relation = {id: relationId, basis: 'Synthetic exact source heading and span.',
    selection: options.selectedUnknown ? {state: 'selected', option: 'unknown'} : {state: 'selected', option: 'optional-shorter'},
    ownedChoiceIds: owned, beforeEventId: options.start ? null : firstEvent,
    focusEventId: options.nullFocus ? null : firstEvent, paths};
  const state = request(options.entrance || 'propers');
  state.properChoices = {[relationId]: 'optional-shorter', [owned[1]]: 'shorter', [gospel]: 'additional'};
  state.alternative = {id: owned[0] + '/shorter'};
  const result = {events: eventIds.map((id) => ({id, kind: 'proper'})), sourcePathChoices: [relation]};
  function adapt(candidate) {
    probes.push(clone(candidate));
    const id = candidate.properChoices[relationId];
    const selected = paths.find((row) => row.id === id);
    assert.equal(candidate.alternative, undefined);
    for (const group of owned) assert.equal(candidate.properChoices[group], selected.choices[group]);
    assert.equal(candidate.properChoices[gospel], 'additional');
    if (id === 'wrong') throw new Error('Synthetic owning adapter refusal.');
    const held = clone(relation); held.selection = {state: 'selected', option: id};
    if (id === 'candidate-unknown') held.paths.find((row) => row.id === id).applicability.state = 'unresolved';
    return {...result, sourcePathChoices: [held]};
  }
  const beforeBodies = node.children.map((row) => row.textContent);
  const input = {T: env.T, root: node, result, state, prefix, adapt,
    navigate: (...args) => navigation.push(clone(args))};
  if (options.commonJS) {
    const previous = globalThis.document;
    globalThis.document = env.context.document;
    try { require(path.join(uiModuleRoot, 'source-choice-controls.js')).attachSourcePathChoices(input); }
    finally {
      if (previous === undefined) delete globalThis.document;
      else globalThis.document = previous;
    }
  } else env.Shell.attachSourcePathChoices(input);
  const wrapper = descendants(node).find((row) => row.dataset.sourcePathChoice);
  const controls = descendants(wrapper).find((row) => row.tagName === 'FIELDSET');
  return {...env, node, wrapper, controls, relation, state, result, probes, navigation,
    eventIds, beforeBodies, independent};
}

test('one cross-seat path control preserves normal event inventory, bodies, independent controls and print notes', () => {
  for (const commonJS of [false, true]) {
  const view = sourcePathView({commonJS});
  assert.equal(view.node.children[0], view.wrapper);
  assert.equal(view.wrapper.dataset.semanticEventId, undefined);
  assert.deepEqual(view.node.querySelectorAll('[data-semantic-event-id]').map((row) => row.dataset.semanticEventId), view.eventIds);
  assert.deepEqual(view.node.children.filter((row) => row !== view.wrapper).map((row) => row.textContent), view.beforeBodies);
  Object.assign(view.context, {reading: view.node});
  vm.runInContext(exactFunction(propersSource, 'renderedSemanticInventory'), view.context);
  assert.deepEqual(clone(view.context.renderedSemanticInventory(view.eventIds.map((id) => ({id})), view.node)), view.eventIds);
  assert.equal(radios(view.independent.node).filter((input) => !input.disabled).length, 2);
  const summary = view.wrapper.children[0];
  assert.match(summary.className, /source-path-note/);
  assert.equal(summary.parentElement, view.wrapper);
  assert.match(summary.textContent, /Source basis: Synthetic exact source heading and span/);
  assert.match(view.controls.className, /ordinary-choice/);
  assert.equal(radios(view.wrapper).length, 6);
  assert(radios(view.wrapper).every((radio) => radio.type === 'radio' && radio.parentElement.tagName === 'LABEL' && !radio.listeners.keydown));
  assert.equal(new Set(radios(view.wrapper).map((radio) => radio.name)).size, 1);
  assert.equal(radios(view.wrapper).filter((radio) => radio.checked).length, 1);
  assert.match(exactFunction(daySource, 'buildResultDocument'), /Shell.attachSourcePathChoices/);
  assert.match(exactFunction(propersSource, 'renderResult'), /Shell.attachSourcePathChoices/);
  }
});
test('source path selection replaces the whole tuple atomically, migrates scalar and preserves independent Gospel', () => {
  for (const entrance of ['day', 'propers']) {
  const prefix = entrance === 'day' ? 'territory/contract/' : '';
  const view = sourcePathView({entrance, prefix});
  const before = JSON.stringify(view.state);
  const radio = radios(view.wrapper).find((row) => row.value === 'common');
  radio.checked = true; radio.dispatch('change');
  assert.equal(view.navigation.length, 1);
  assert.deepEqual(JSON.parse(view.navigation[0][0]['proper-choices']), {
    [relationId]: 'common', [owned[0]]: 'longer', [owned[1]]: 'longer', [gospel]: 'additional'});
  assert.deepEqual(view.navigation[0][1], ['alternative', '_candidate-alternative']);
  const id = prefix + firstEvent;
  assert.deepEqual(view.navigation[0][2], {location: {kind: 'event', id}, focus: {kind: 'proper-choice-result', event: id}});
  assert.equal(JSON.stringify(view.state), before);
  assert(view.probes.every((candidate) => candidate.properChoices[owned[0]] === candidate.properChoices[owned[1]]));
  Object.assign(view.context, {reading: view.node, readerShell: {restoreSemanticLocation: () => true}});
  if (entrance === 'day') {
    vm.runInContext(exactFunction(daySource, 'restorePendingNavigation'), view.context);
    view.context.restorePendingNavigation(view.navigation[0][2]);
  } else {
    vm.runInContext(exactFunction(propersSource, 'eventLocation'), view.context);
    vm.runInContext(exactFunction(propersSource, 'focusCommittedResult'), view.context);
    view.context.focusCommittedResult(view.navigation[0][2].focus, view.navigation[0][2].location);
  }
  const body = view.node.querySelectorAll('[data-semantic-event-id]').find((row) => row.dataset.semanticEventId === firstEvent);
  assert.equal(body.focused.preventScroll, true);
  }
});
test('wrong and unknown candidate conditions stay disabled, with exact unresolved condition retained for print', () => {
  const view = sourcePathView({selectedUnknown: true});
  for (const id of ['wrong', 'candidate-unknown', 'false', 'unknown']) {
    const input = radios(view.wrapper).find((row) => row.value === id);
    assert.equal(input.disabled, true, id); input.checked = true; input.dispatch('change');
  }
  assert.equal(view.navigation.length, 0);
  const note = view.wrapper.children[0];
  assert.match(note.textContent, /Held Source Condition in Transferred/);
  assert.match(note.textContent, /Applicability unresolved/);
  assert.equal(note.closest('[data-option-group]'), null);
});
test('null placement starts the container and null event focus restores the checked path radio in both controllers', () => {
  for (const entrance of ['day', 'propers']) {
    const view = sourcePathView({entrance, start: true, nullFocus: true, prefix: entrance === 'day' ? 'territory/contract/' : ''});
    const radio = radios(view.wrapper).find((row) => row.value === 'common');
    radio.checked = true; radio.dispatch('change');
    const intent = view.navigation[0][2];
    assert.equal(view.node.children[0], view.wrapper); assert.equal(intent.location, null);
    assert.equal(intent.focus.kind, 'source-path-option');
    Object.assign(view.context, {reading: view.node, readerShell: {restoreSemanticLocation: () => true}});
    if (entrance === 'day') {
      vm.runInContext(exactFunction(daySource, 'restorePendingNavigation'), view.context);
      view.context.restorePendingNavigation(intent);
    } else {
      vm.runInContext(exactFunction(propersSource, 'focusCommittedResult'), view.context);
      view.context.focusCommittedResult(intent.focus, intent.location);
    }
    assert.equal(radio.focused.preventScroll, true);
    assert.equal(view.controls.scrolled.block, 'start');
  }
});
test('source path URL copy preserves relation plus tuple without claiming calendar-only Common A entitlement', () => {
  const view = sourcePathView();
  const radio = radios(view.wrapper).find((row) => row.value === 'common'); radio.checked = true; radio.dispatch('change');
  const choices = JSON.parse(view.navigation[0][0]['proper-choices']);
  const hash = C.serializeLegacy({ok: true, state: {...request(), cycle: 'B', properChoices: choices}, legacy: {variants: {}, unknown: [], inert: []}});
  const shared = Share.canonicalUrl('propers', {href: 'https://example.test/liturgy/propers-reader.html' + hash}, C);
  assert.deepEqual(JSON.parse(new URLSearchParams(new URL(shared).hash.slice(1)).get('proper-choices')), choices);
  const selected = clone(view.result); selected.sourcePathChoices[0].selection = {state: 'selected', option: 'common'};
  const root = new Element('div');
  const body = new Element('section'); body.dataset.semanticEventId = firstEvent; root.appendChild(body);
  view.Shell.attachSourcePathChoices({T: view.T, root, result: selected, state: view.state,
    navigate: () => {}, adapt: () => selected});
  const note = root.children[0].children[0].textContent;
  assert.match(note, /Common \(principal\)/); assert.doesNotMatch(note, /Year A|A.only|calendar.*A/i);
});

const actualSourceFixture = process.argv[4] && path.resolve(process.argv[4]);
if (actualSourceFixture) test('canonical Lent III source paths bridge adapters to atomic DOM controls with unchanged calendar B', () => {
  const structure = JSON.parse(fs.readFileSync(actualSourceFixture));
  const mass = structure.masses.find((row) => row.key === 'lent-3');
  const source = mass.proper_source_paths[0];
  const id = 'proper-choice/' + structure.calendar + '/lent-3/main/' + source.id;
  for (const entrance of ['day', 'propers']) {
    const env = environment(), node = new Element('div'), navigation = [];
    const state = {...request(entrance), edition: {id: structure.calendar}, cycle: 'B'};
    const d = {calendar: structure.calendar, date: '2027-02-28', weekday: 'sunday', season: 'lent',
      liturgicalYear: {lectionary: {sunday: 'B', weekday: 'I'}, anchors: {}}, options: [{option: null,
        winner: {id: mass.key, nature: 'sunday'}, settled: true, readable: [{key: mass.key, state: 'said'}], absent: []}]};
    if (entrance === 'day') { state.civilDate = d.date; state.calendar = {id: structure.calendar}; }
    else state.formulary = {id: mass.key, type: mass.kind};
    const adapt = (request) => entrance === 'day' ? A.adaptDay({request, derived: d, structure}) : A.adaptPropers({request, structure});
    const unresolved = adapt(state);
    for (const event of unresolved.events) {
      const body = new Element('section'); body.dataset.semanticEventId = event.id; node.appendChild(body);
    }
    const raw = JSON.stringify(structure);
    env.Shell.attachSourcePathChoices({T: env.T, root: node, result: unresolved, state, adapt,
      navigate: (...args) => navigation.push(clone(args))});
    const wrapper = descendants(node).find((row) => row.dataset.sourcePathChoice === id);
    const selectedId = 'optional-material-a-gospel-longer';
    const radio = radios(wrapper).find((row) => row.value === selectedId);
    assert(radio && !radio.disabled); radio.checked = true; radio.dispatch('change');
    assert.equal(navigation.length, 1);
    const choices = JSON.parse(navigation[0][0]['proper-choices']);
    const expected = unresolved.sourcePathChoices[0].paths.find((row) => row.id === selectedId).choices;
    assert.deepEqual(choices, {...expected, [id]: selectedId});
    const result = adapt({...state, properChoices: choices});
    if (entrance === 'day') assert.equal(result.calendarResult.lectionary.sunday, 'B');
    else assert.equal(result.calendarResult, null);
    const selectedEvents = result.events.filter((event) => ['004', '006', '007', '008', '009'].some((n) => event.id.endsWith('/' + n)));
    assert.equal(selectedEvents.length, 5); assert(selectedEvents.every((event) => event.selected.cycle === 'A'));
    assert(!result.events.some((event) => event.kind === 'proper-choice' && ['first-reading', 'gospel'].includes(event.group)));
    assert(result.events.some((event) => event.kind === 'proper-choice' && event.group === 'entrance-antiphon'));
    assert(result.events.some((event) => event.kind === 'proper-choice' && event.group === 'communion-antiphon'));
    assert.equal(navigation[0][2].location.id, result.sourcePathChoices[0].focusEventId);
    const selectedRoot = new Element('div');
    const renderer = env.context.TriptychPropersEvents.create({navigate: () => {},
      sourceIndex: (event) => Number(event.sourceHooks.find((row) => row.kind === 'proper-structure').id.slice(-3)) - 1,
      publicKeys: {cycle: 'cycle'}, legacyKeys: {cycle: '_candidate-cycle'},
      getStructure: () => structure, getOrdinary: () => null});
    const qualification = JSON.stringify(selectedEvents.map((event) => ({id: event.id, selected: event.selected, sourceHooks: event.sourceHooks})));
    for (const event of selectedEvents) {
      const index = Number(event.sourceHooks.find((row) => row.kind === 'proper-structure').id.slice(-3)) - 1;
      selectedRoot.appendChild(renderer.renderEvent(event, mass.propers[index], {}, {}, {...state, properChoices: choices}));
    }
    const rendered = env.rendered.slice(-5);
    assert(rendered.every((row) => row.options.cycle === 'A'));
    env.Shell.attachSourcePathChoices({T: env.T, root: selectedRoot, result, state: {...state, properChoices: choices}, adapt, navigate: () => {}});
    assert.deepEqual(selectedRoot.querySelectorAll('[data-semantic-event-id]').map((row) => row.dataset.semanticEventId), selectedEvents.map((event) => event.id));
    assert.equal(JSON.stringify(selectedEvents.map((event) => ({id: event.id, selected: event.selected, sourceHooks: event.sourceHooks}))), qualification);
    assert.equal(JSON.stringify(structure), raw);
    assert.deepEqual(node.querySelectorAll('[data-semantic-event-id]').map((row) => row.dataset.semanticEventId), unresolved.events.map((event) => event.id));
  }
});
process.stdout.write(JSON.stringify({status: 'pass', groups: results.length, checks: results,
  bytes: Object.fromEntries(['source-choice-controls.js', 'reader-shell.js', 'propers-events.js', 'day-reader.js', 'propers-reader.js']
    .map((name) => [name, Buffer.byteLength(source(name))]))}, null, 2) + '\n');
