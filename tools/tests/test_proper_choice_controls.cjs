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
  setAttribute(key, value) { this.attributes[key] = value; }
  addEventListener(name, fn) { (this.listeners[name] ||= []).push(fn); }
  dispatch(name) { (this.listeners[name] || []).forEach((fn) => fn({target: this})); }
  querySelectorAll(selector) { return descendants(this).filter((node) => selector === '[data-semantic-location]'
    ? node.dataset.semanticLocation : selector === '[data-semantic-event-id]' ? node.dataset.semanticEventId : false); }
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
    const changes = entrance === 'day' ? [{date: '2026-04-16'}, {missal: 'postconciliar'}, {mass: 'other'}, {form: 'other'}]
      : [{missal: 'postconciliar'}, {type: 'other'}, {mass: 'other'}, {form: 'other'}];
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

test('dedicated CommonJS controls retain browser DOM, legacy migration, and disabled Day negatives', () => {
  const commonJS = require(path.join(uiModuleRoot, 'source-choice-controls.js'));
  assert.deepEqual(Object.keys(commonJS).sort(), ['properChoiceRemovals', 'renderProperChoice']);
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
process.stdout.write(JSON.stringify({status: 'pass', groups: results.length, checks: results,
  bytes: Object.fromEntries(['source-choice-controls.js', 'reader-shell.js', 'propers-events.js', 'day-reader.js', 'propers-reader.js']
    .map((name) => [name, Buffer.byteLength(source(name))]))}, null, 2) + '\n');
