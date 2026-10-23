'use strict';
// stdin is the fresh canonical projection from the paired Python test.
// No tracked generated fixture, source words, or URL actual-use attestation.
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const S = require(path.resolve(__dirname, '../../src/web/browser/liturgy/ordinary-seating.js'));
const ordinary = JSON.parse(fs.readFileSync(path.resolve(__dirname,
  '../../src/web/data/structure/ordinary/postconciliar.json'), 'utf8'));
const source = JSON.parse(fs.readFileSync(0, 'utf8'));
const before = JSON.stringify(source);
const masses = Object.fromEntries(source.masses.map((mass) => [mass.key, mass]));
const lentFact = 'lent-5-sunday-john-8-1-11-actually-read';
const adventFact = 'advent-1-sunday-isaiah-2-1-5-actually-read';
for (const mass of source.masses) {
  const result = S.validateProperSeating(ordinary, mass.propers, {
    calendar: 'postconciliar', mass: mass.key, form_id: 'main', full: true,
    facts: {}, sourcePaths: mass.proper_source_paths
  });
  assert.equal(result.candidates, mass.propers.length);
}
let executions = 0;
function prepare(key, cycle, choices = {}, conditionFacts = {}, entrance = 'day') {
  const mass = masses[key];
  executions++;
  return S.prepareProperAppointments(mass.propers.map((proper, sourceIndex) => ({proper, sourceIndex})), {
    calendar: 'postconciliar', mass: key, formId: 'main', entrance,
    sourcePaths: mass.proper_source_paths, calendarCycles: {sunday: cycle, weekday: 'II'},
    choices, conditionFacts
  });
}
function references(result, role) {
  return S.unframedEvents(result.rows, null, result.selections).flatMap((event) =>
    event.kind === 'proper' ? [event] : event.options
      .filter((option) => option.id === (event.selection || {}).option)
      .flatMap((option) => option.rows)).filter((row) => row.proper.name === role)
    .flatMap((row) => row.proper.verses.map((verse) => verse.ref));
}
for (const entrance of ['day', 'propers']) {
  for (const cycle of ['A', 'B']) {
    for (const value of [true, false, null, undefined]) {
      const result = prepare('lent-5-monday', cycle,
        {'main/lent-5-monday-reading-course': 'john-8-1-11-ab-longer'}, value === undefined ? {} : {[lentFact]: value}, entrance);
      assert.deepEqual(references(result, 'Gospel'), ['John 8:1-11']);
      assert.throws(() => prepare('lent-5-monday', cycle,
        {'main/lent-5-monday-reading-course': 'john-8-12-20-c-longer'}, value === undefined ? {} : {[lentFact]: value}, entrance));
      assert.throws(() => prepare('lent-5-monday', cycle,
        {'main/gospel': 'john-8-12-20'}, value === undefined ? {} : {[lentFact]: value}, entrance));
    }
  }
  for (const facts of [{}, {[lentFact]: null}, {[lentFact]: false}, {[lentFact]: true},
    Object.create({[lentFact]: true}), Object.create({[lentFact]: false})]) {
    const result = prepare('lent-5-monday', 'C', {}, facts, entrance);
    assert.deepEqual(result.sourcePathSelections['main/lent-5-monday-reading-course'],
      {state: 'required', option: null});
    assert.deepEqual(references(result, 'Gospel'), []);
    for (const daniel of ['longer', 'shorter']) {
      const principal = prepare('lent-5-monday', 'C',
        {'main/lent-5-monday-reading-course': 'john-8-1-11-c-' + daniel}, facts, entrance);
      assert.deepEqual(references(principal, 'Gospel'), ['John 8:1-11']);
      const role = daniel === 'longer' ? 'First Reading' : 'First Reading (shorter form)';
      assert.equal(references(principal, role).length, 1);
      const alternate = {'main/lent-5-monday-reading-course': 'john-8-12-20-c-' + daniel};
      if (Object.hasOwn(facts, lentFact) && facts[lentFact] === true) {
        const result = prepare('lent-5-monday', 'C', alternate, facts, entrance);
        assert.deepEqual(references(result, 'Gospel'), ['John 8:12-20']);
        assert.equal(references(result, role).length, 1);
      } else {
        assert.throws(() => prepare('lent-5-monday', 'C', alternate, facts, entrance),
          /source-condition-unresolved|inapplicable/);
      }
    }
  }
  for (const value of ['true', 'false', 1, 0, {}, [], undefined]) {
    assert.throws(() => prepare('lent-5-monday', 'C', {}, {[lentFact]: value}, entrance), /boolean/);
  }
  for (const cycle of ['A', 'B', 'C']) {
    for (const value of [true, false, null]) {
      if (cycle === 'A' && value === true) continue;
      assert.throws(() => prepare('advent-1-monday', cycle,
        {'main/advent-first-reading': 'isaiah-4'}, {[adventFact]: value}, entrance));
    }
    for (const psalm of ['without-parenthesized-block', 'with-parenthesized-block']) {
      const result = prepare('advent-1-monday', cycle,
        {'main/advent-first-reading': 'isaiah-2', 'main/advent-psalm-strophes': psalm}, {}, entrance);
      assert.equal(references(result, 'Responsorial Psalm').length, 1);
      assert.equal(result.sourcePathSelections['main/advent-psalm-strophes'].option, psalm);
    }
    for (const option of ['song-of-songs', 'zephaniah']) {
      const result = prepare('advent-december-21', cycle, {'main/first-reading': option}, {}, entrance);
      assert.deepEqual(references(result, 'First Reading'),
        [option === 'zephaniah' ? 'Zephaniah 3:14-18a' : 'Song of Songs 2:8-14']);
    }
  }
  for (const reading of ['isaiah-2', 'isaiah-4']) {
    for (const psalm of ['without-parenthesized-block', 'with-parenthesized-block']) {
      const result = prepare('advent-1-monday', 'A',
        {'main/advent-first-reading': reading, 'main/advent-psalm-strophes': psalm},
        {[adventFact]: true}, entrance);
      assert.deepEqual(references(result, 'First Reading'),
        [reading === 'isaiah-2' ? 'Isaiah 2:1-5' : 'Isaiah 4:2-6']);
      assert.equal(references(result, 'Responsorial Psalm').length, 1);
    }
  }
  assert.throws(() => prepare('advent-1-monday', 'A',
    {'main/first-reading': 'isaiah-4'}, {}, entrance), /complete selected source path/);
}
assert.equal(executions, 172);
assert.equal(JSON.stringify(source), before, 'admission must not mutate canonical source appointments');
console.log(`phase2 ferial fidelity: ${executions} admission executions; both entrances; no bodies`);
