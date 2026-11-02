/* Synthetic source coordinates test book facts; these words claim no liturgical coverage. */
import assert from 'node:assert/strict';
import {createRequire} from 'node:module';
import test from 'node:test';

const require = createRequire(import.meta.url);
const S = require('../../src/web/browser/liturgy/ordinary-seating.js');
const A = require('../../src/web/browser/liturgy/reader-state-adapters.js');
const C = require('../../src/web/browser/liturgy/reader-state.js');
const names = ['Matthew', 'Mark', 'Luke', 'John'];
const keys = names.map(name => 'gospel-book-' + name.toLowerCase());
const unknown = Object.fromEntries(keys.map(key => [key, null]));
const clone = value => JSON.parse(JSON.stringify(value));
const gospel = book => ({name: 'Gospel', form_id: 'main', source: 'scripture',
  citations: [{book, ref: book + ' 1:1', unresolved: null}], cycles: {}, translations: []});
function prepare(rows, options = {}) {
  const context = {calendar: 'synthetic-edition', entrance: 'propers', mass: 'synthetic',
    formId: 'main', choices: {}, ...options};
  return S.prepareProperAppointments(rows, context);
}
function facts(rows, options = {}, cycles = {}) {
  const prepared = prepare(rows, options);
  return S.predicateFacts({properAppointments: prepared, properRows: rows, calendarCycles: cycles});
}
function selected(book) {
  return Object.fromEntries(keys.map(key => [key, key === 'gospel-book-' + book.toLowerCase()]));
}
function bookFacts(value) {
  return Object.fromEntries(keys.map(key => [key, value[key]]));
}
function alternative(book, option) {
  return {...gospel(book), ordinary_disposition: {kind: 'alternative', group: 'gospel',
    option, basis: 'Synthetic exact source alternatives.'}};
}

export function ordinary() {
  const element = key => ({key, kind: 'dialogue', speaker: 'deacon-or-priest',
    translations: ['en', 'la'].map(lang => ({lang, source_id: 'synthetic-' + lang,
      rights: 'project-created', relation: 'own', text: 'Synthetic source marker ' + key,
      collation: 'not-applicable'})), absent: {english: null, latin: null}});
  const heads = names.map(name => ({...element('word/heading-' + name.toLowerCase()),
    conditions: [{kind: 'include-when-any', predicates: ['gospel-book-' + name.toLowerCase()],
      unknown: 'unresolved', basis: 'Synthetic source-owned named heading.'}]}));
  const elements = [element('word/greeting'), ...heads, element('word/gloria'),
    {...element('word/proclamation'), kind: 'rubric', speaker: null}, element('word/closing')];
  return {calendar: 'synthetic-edition', sections: [{key: 'word', name: 'Synthetic Word', elements}],
    slots: [{key: 'gospel', propers: ['Gospel'], anchor: 'word/proclamation', where: 'after', locus: 'synthetic'}],
    variants: [], absences: [],
    languages: ['en', 'la'].map(lang => ({lang, held: elements.length, elements: elements.length})),
    language_coverage: ['en', 'la'].map(lang => ({lang, held: elements.length,
      elements: elements.length, missing: 0, absent: 0})),
    relation_coverage: ['en', 'la'].map(lang => ({lang, relation: 'own', collation: 'not-applicable', count: elements.length})),
    translations: ['en', 'la'].map(lang => ({lang, source_id: 'synthetic-' + lang, label: 'Synthetic source'}))};
}

test('each closed canonical Gospel book supplies one true fact and three false facts', () => {
  for (const name of names) assert.deepEqual(bookFacts(facts([gospel(name)])), selected(name));
});

test('no context, no Gospel, non-Gospel citations and qualified non-Gospel labels stay unknown', () => {
  assert.deepEqual(bookFacts(S.predicateFacts()), unknown);
  for (const name of ['Gospel Acclamation', 'First Reading', 'Not Gospel', 'Gospel Acclamation (longer)',
    'Passion of the Lord', 'Passion of the Lord (shorter form)']) {
    assert.deepEqual(bookFacts(facts([{...gospel('Luke'), name}])), unknown);
  }
  assert.deepEqual(bookFacts(facts([])), unknown);
});

test('all applicable Gospel citations must agree; invalid or unresolved books cannot borrow another citation', () => {
  for (const book of [null, false, 1, 'Acts', 'Luke ', 'luke', '__proto__']) {
    assert.deepEqual(bookFacts(facts([gospel(book)])), unknown);
  }
  for (const citations of [[], [null], [{ref: 'Luke 1:1'}],
    [{book: 'Luke', unresolved: 'unresolved-source'}],
    [{book: 'Luke'}, {book: 'John'}], [{book: 'Luke'}, {}]]) {
    assert.deepEqual(bookFacts(facts([{...gospel('Luke'), citations}])), unknown);
  }
  assert.deepEqual(bookFacts(facts([gospel('Luke'), gospel('John')])), unknown);
  assert.deepEqual(bookFacts(facts([{...gospel('Luke'), citations: [{book: 'Luke'}, {book: 'Luke'}]}])), selected('Luke'));
  assert.deepEqual(bookFacts(facts([{...gospel('Luke'), citations: [{book: 'Luke', token: 'John', ref: 'John 1:1'}]}])), selected('Luke'));
});

test('unresolved alternatives stay unknown even when their books agree; explicit options are order independent', () => {
  for (const books of [['Luke', 'John'], ['Luke', 'Luke']]) {
    const rows = books.map((book, index) => alternative(book, index ? 'shorter' : 'longer'));
    assert.deepEqual(bookFacts(facts(rows)), unknown);
    for (const reversed of [false, true]) {
      const source = reversed ? rows.slice().reverse() : rows;
      assert.deepEqual(bookFacts(facts(source, {choices: {'main/gospel': 'shorter'}})), selected(books[1]));
      assert.deepEqual(bookFacts(facts(source, {choices: {'main/gospel': 'longer'}})), selected(books[0]));
    }
  }
});

test('only the held selected cycle supplies a book; no cycle or contradictory cycle stays unknown', () => {
  const row = {...gospel('John'), citations: [], cycles: {
    A: {citations: [{book: 'Matthew'}]}, B: {citations: [{book: 'Mark'}]},
    C: {citations: [{book: 'Luke'}]}}};
  assert.deepEqual(bookFacts(facts([row])), unknown);
  for (const [sunday, book] of [['A', 'Matthew'], ['B', 'Mark'], ['C', 'Luke']]) {
    assert.deepEqual(bookFacts(facts([row], {}, {sunday})), selected(book));
  }
  assert.deepEqual(bookFacts(facts([row], {}, {sunday: 'X'})), unknown);
  const single = {...row, cycles: {A: row.cycles.A}};
  assert.deepEqual(bookFacts(facts([single])), selected('Matthew'));
  assert.deepEqual(bookFacts(facts([single], {}, {sunday: 'B'})), unknown);
  const weekday = {...gospel('John'), citations: [], weekday_cycles: {
    I: {citations: [{book: 'Luke'}]}, II: {citations: [{book: 'John'}]}}};
  assert.deepEqual(bookFacts(facts([weekday], {}, {weekday: 'II'})), selected('John'));
  assert.deepEqual(bookFacts(facts([{...row, weekday_cycles: weekday.weekday_cycles}], {}, {sunday: 'A', weekday: 'I'})), unknown);
});

test('base and selected-cycle citations are the same unanimous set used by the material selector', () => {
  const cycle = {A: {citations: [{book: 'Luke', ref: 'Luke 1:1'}]}};
  for (const citation of [{book: 'John'}, {book: 'Acts'}, {book: 'Luke', unresolved: 'unresolved-parent'}]) {
    const proper = {...gospel('Luke'), citations: [citation], cycles: cycle};
    assert.deepEqual(bookFacts(facts([proper], {}, {sunday: 'A'})), unknown);
  }
  const baseOnly = {...gospel('Luke'), cycles: {A: {text: 'Synthetic selected child wording.'}}};
  assert.deepEqual(bookFacts(facts([baseOnly], {}, {sunday: 'A'})), selected('Luke'));
  const unanimous = {...gospel('Luke'), cycles: cycle};
  assert.deepEqual(bookFacts(facts([unanimous], {}, {sunday: 'A'})), selected('Luke'));
});

test('conditional Gospel use must be known; unrelated unresolved readings do not hide a closed Gospel', () => {
  function conditional(name, book) {
    return {...gospel(book), name, appointment_identity: {mass: 'synthetic', form_id: 'main', proper: name, occurrence: 1},
      ordinary_disposition: {kind: 'conditional', group: 'source-condition', basis: 'Synthetic source condition.',
        when: {fact: 'season', in: ['used']}}};
  }
  const source = {season: {edition: 'synthetic-edition', basis: 'Synthetic source condition.',
    values: ['used', 'unused'], season_values: {ordinary: 'used', advent: 'unused'}}};
  const options = {facts: source};
  assert.deepEqual(bookFacts(facts([conditional('Gospel', 'John')], options)), unknown);
  assert.deepEqual(bookFacts(facts([gospel('Luke'), conditional('First Reading', 'John')], options)), selected('Luke'));
  assert.deepEqual(bookFacts(facts([gospel('Luke'), conditional('Gospel', 'John')], {
    ...options, entrance: 'day', date: '2026-12-01', season: 'advent'})), selected('Luke'));
});

test('source-path material selection outranks the calendar cycle and unresolved Gospel paths stay unknown', () => {
  const identity = {mass: 'synthetic', form_id: 'main', proper: 'Gospel', occurrence: 1};
  const row = {...gospel('John'), citations: [], appointment_identity: identity, source_path_relation: 'readings',
    cycles: {A: {citations: [{book: 'Luke'}]}, B: {citations: [{book: 'Mark'}]}}};
  const path = (id, cycle) => ({id, standing: id === 'principal' ? 'principal' : 'optional',
    calendar_cycles: {family: 'sunday', in: ['B']}, choices: {},
    members: [{appointment: identity, material_cycle: {family: 'cycles', cycle}}]});
  const options = {calendarCycles: {sunday: 'B', weekday: null}, sourcePaths: [{
    id: 'readings', form_id: 'main', basis: 'Synthetic exact source paths.', source_edition: 'synthetic-edition',
    paths: [path('principal', 'A'), path('optional', 'B')]}]};
  assert.deepEqual(bookFacts(facts([row], options, {sunday: 'B'})), unknown);
  assert.deepEqual(bookFacts(facts([row], {...options, choices: {'main/readings': 'principal'}}, {sunday: 'B'})), selected('Luke'));
  assert.deepEqual(bookFacts(facts([row], {...options, choices: {'main/readings': 'optional'}}, {sunday: 'B'})), selected('Mark'));
});

test('derivation preserves source rows, choices and every existing calendar/appointment fact', () => {
  const rows = [alternative('Luke', 'longer'), alternative('John', 'shorter')];
  const options = {choices: {'main/gospel': 'longer'}};
  const prepared = prepare(rows, options);
  const context = {settled: true, weekday: 'sunday', season: 'ordinary', nature: 'sunday',
    date: '2026-10-04', anchors: {easter: '2026-04-05'}, appointments: {preface: 'synthetic'}};
  const before = clone({rows, options, prepared, context});
  const old = S.predicateFacts(context);
  const result = S.predicateFacts({...context, properAppointments: prepared, properRows: rows});
  for (const [key, value] of Object.entries(old)) if (!keys.includes(key)) assert.deepEqual(result[key], value);
  assert.deepEqual(bookFacts(result), selected('Luke'));
  assert.deepEqual({rows, options, prepared, context}, before);
});

test('a known heading stays before the appointed Gospel and its source closing stays after it', () => {
  const file = ordinary();
  for (const name of names) {
    const rows = [gospel(name)];
    const prepared = prepare(rows);
    const resolution = S.resolveElements(file, {}, facts(rows));
    const events = S.massEvents(resolution.shown,
      S.seatPropers(prepared.rows, S.seats(file, resolution.shown), null, prepared.selections));
    const ids = events.map(event => event.kind === 'ordinary_element' ? event.element.key : event.kind === 'proper' ? 'Gospel' : event.kind);
    assert.equal(ids.filter(id => id.startsWith('word/heading-')).length, 1);
    assert(ids.indexOf('word/heading-' + name.toLowerCase()) < ids.indexOf('Gospel'));
    assert(ids.indexOf('word/proclamation') < ids.indexOf('Gospel'));
    assert(ids.indexOf('Gospel') < ids.indexOf('word/closing'));
    assert.equal(resolution.unresolved.length, 0);
  }
  const resolution = S.resolveElements(file, {}, S.predicateFacts());
  assert.equal(resolution.shown.filter(row => row.element.key.startsWith('word/heading-')).length, 0);
  assert.equal(resolution.unresolved.length, 4);
});

test('Day and date-independent Propers adapters consume the same selected source book', () => {
  const file = ordinary();
  const row = {...gospel('Luke'), citations: [], cycles: {
    A: {citations: [{book: 'Matthew', ref: 'Matthew 1:1', unresolved: null}]},
    B: {citations: [{book: 'Mark', ref: 'Mark 1:1', unresolved: null}]}}};
  const mass = {key: 'synthetic', name: 'Synthetic source Mass', kind: 'synthetic', propers: [row]};
  const structure = {calendar: 'synthetic-edition', translations: [], masses: [mass]};
  const common = {schema: C.STATE_SCHEMA, edition: {id: 'synthetic-edition'},
    bible: {id: 'synthetic-bible', numbering: 'vulgate'}, languages: {orations: 'la', ordinary: 'en'},
    options: {ordinary: true, legitimate: {}}, requestedMode: 'missal',
    coverage: [], unresolvedChoices: [], sourceHooks: []};
  const day = A.adaptDay({structure, ordinary: file, request: {...common, entrance: 'day',
    civilDate: '2026-10-04', calendar: {id: 'synthetic-edition'}, selectedReadableFormulary: {id: 'synthetic'}},
    derived: {date: '2026-10-04', calendar: 'synthetic-edition', weekday: 'sunday', season: 'ordinary',
      liturgicalYear: {lectionary: {sunday: 'B', weekday: 'II'}}, options: [{
        option: null, winner: {id: 'synthetic', nature: 'sunday'}, settled: true,
        readable: [{key: 'synthetic', state: 'said'}], absent: []}]}});
  const propers = A.adaptPropers({structure, ordinary: file, request: {...common, entrance: 'propers',
    formulary: {id: 'synthetic'}, cycle: 'B'}});
  const headings = result => result.events.filter(event => event.id.includes('/heading-')).map(event => event.id);
  assert.deepEqual(headings(day), ['ordinary-element/word/heading-mark']);
  assert.deepEqual(headings(propers), headings(day));
  const unresolved = A.adaptPropers({structure, ordinary: file, request: {...common, entrance: 'propers', formulary: {id: 'synthetic'}}});
  assert.deepEqual(headings(unresolved), []);
  assert.equal(unresolved.ordinaryUnresolved.filter(row => row.element.includes('/heading-')).length, 4);
  row.citations = [{book: 'John', ref: 'John 1:1', unresolved: null}];
  const conflict = A.adaptPropers({structure, ordinary: file, request: {...common, entrance: 'propers',
    formulary: {id: 'synthetic'}, cycle: 'B'}});
  assert.deepEqual(headings(conflict), []);
  assert.deepEqual(conflict.events.find(event => event.kind === 'proper').selected.references, ['John 1:1', 'Mark 1:1']);
});
