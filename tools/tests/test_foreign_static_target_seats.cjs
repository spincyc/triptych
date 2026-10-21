'use strict';
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const root = process.env.TRIPTYCH_REVIEW_ROOT || path.resolve(__dirname, '../..');
const S = require(process.env.TRIPTYCH_FOREIGN_STATIC_SEATING || path.join(root, 'src/web/browser/liturgy/ordinary-seating.js'));
const ordinary = JSON.parse(fs.readFileSync(path.join(root, 'src/web/data/structure/ordinary/roman-pre-1955.json')));
const file = JSON.parse(fs.readFileSync(path.join(root, 'src/web/data/structure/propers/roman-pre-1955.json')));
const mass = file.masses.find((one) => one.key === 'commune-plurimorum-martyrum-1');
const ctx = {calendar: ordinary.calendar, mass: mass.key, form_id: 'main', full: true,
  facts: file.proper_appointment_facts || {}};
const copy = (one) => JSON.parse(JSON.stringify(one));
const checks = [];
function test(name, run) { run(); checks.push(name); }
const unknown = mass.propers[11];
assert.equal(unknown.name, 'Gospel (alterum in Communi plurimorum Martyrum)');
const marker = unknown.appointment_applicability;
const shown = ordinary.sections.flatMap((section) => section.elements.map((element) => ({section, element})));
const seating = S.seats(ordinary, shown);
test('actual marked standalone retains raw words and an unknown target seat without an alias', () => {
  const before = JSON.stringify(mass);
  const result = S.validateProperSeating(ordinary, mass.propers, ctx);
  assert.equal(result.candidates, mass.propers.length);
  const notice = result.diagnostics.find((one) => one.sourceIndex === 11);
  assert.deepEqual(notice.target_seat, {state: 'unknown', reason: 'not-declared-in-target-ordinary'});
  assert.equal(notice.source_edition, marker.source_edition);
  assert.equal(notice.target_edition, ordinary.calendar);
  assert.equal(S.usableSlotOf(seating, unknown.name), -1);
  assert.equal(JSON.stringify(mass), before);
});
test('missing, inherited, malformed or wrong-edition markers cannot authorize an unclaimed target row', () => {
  const variants = [
    (one) => {delete one.appointment_applicability;},
    (one) => {one.appointment_applicability = null;},
    (one) => {one.appointment_applicability.target_edition = 'roman-1962';},
    (one) => {one.appointment_applicability.source_edition = ordinary.calendar;},
    (one) => {one.appointment_applicability.source_edition = 'bad_edition';},
    (one) => {one.appointment_applicability.state = 'selected';},
    (one) => {one.appointment_applicability.extra = true;},
    (one) => {one.appointment_applicability.basis = '';}
  ];
  for (const mutate of variants) {
    const changed = copy(unknown); mutate(changed);
    assert.throws(() => S.validateProperSeating(ordinary, [changed], ctx), /no usable|applicability/);
  }
  const inherited = copy(unknown); delete inherited.appointment_applicability;
  Object.setPrototypeOf(inherited, {appointment_applicability: marker});
  assert.throws(() => S.validateProperSeating(ordinary, [inherited], ctx), /no usable/);
});
test('legacy groups keep all framed seat and mixed membership checks', () => {
  const alternatives = (names, marked) => names.map((name, index) => ({name, form_id: 'main',
    ...(marked[index] ? {appointment_applicability: copy(marker)} : {}),
    ordinary_disposition: {kind: 'alternative', group: 'technical-options', option: index ? 'second' : 'first', basis: 'Technical group control, no source appointment claim.'}}));
  assert.equal(S.validateProperSeating(ordinary, alternatives(['Gospel', 'Gospel (vel)'], [false, false]), ctx).choice_groups, 1);
  for (const [names, marked] of [
    [['Gospel', unknown.name], [false, true]],
    [[unknown.name, 'Gospel (another unknown)'], [true, true]],
    [['Gospel', 'Epistle'], [true, true]],
    [['Gospel', 'Epistle'], [false, true]]
  ]) assert.throws(() => S.validateProperSeating(ordinary, alternatives(names, marked), ctx), /share one usable semantic Ordinary seat/);
  const stale = {name: 'Gospel', appointment_applicability: copy(marker), ordinary_disposition: {
    kind: 'unplaced', group: 'technical-unplaced', region: 'after-frame', basis: 'Technical stale control.'}};
  assert.throws(() => S.validateProperSeating(ordinary, [stale], ctx), /stale/);
});
test('false and unknown conditions cannot hide an unmarked invalid source candidate', () => {
  const fact = {edition: ordinary.calendar, values: ['included', 'excluded'], basis: 'Technical source condition control.',
    season_values: {regular: 'excluded', advent: 'included', triduum: null}};
  const candidate = {name: unknown.name, form_id: 'main', appointment_identity: {
    mass: mass.key, form_id: 'main', proper: unknown.name, occurrence: 1}, ordinary_disposition: {
    kind: 'conditional', group: 'technical-conditional', basis: 'Technical source condition control.',
    when: {fact: 'technical-condition', in: ['included']}}};
  const facts = {'technical-condition': fact};
  const falseContext = {calendar: ordinary.calendar, mass: mass.key, entrance: 'day', date: '2026-10-21', season: 'regular', facts};
  assert.equal(S.prepareProperAppointments([candidate], falseContext).inactive.length, 1);
  assert.equal(S.prepareProperAppointments([candidate], {...falseContext, entrance: 'propers', date: null, season: null}).unresolved.length, 1);
  for (const supplied of [{...ctx, facts}, {...ctx, facts, ...falseContext}]) {
    assert.throws(() => S.validateProperSeating(ordinary, [candidate], supplied), /no usable/);
  }
  const broken = copy(candidate); broken.ordinary_disposition.when.fact = 'unheld';
  broken.appointment_applicability = copy(marker);
  assert.throws(() => S.validateProperSeating(ordinary, [broken], {...ctx, facts}), /unheld/);
});
test('known foreign rows keep their original diagnostics and all execution routes still refuse', () => {
  const mapped = {name: 'Gospel', appointment_applicability: copy(marker)};
  const result = S.validateProperSeating(ordinary, [mapped], ctx);
  assert(!Object.prototype.hasOwnProperty.call(result.diagnostics[0], 'target_seat'));
  for (const qualified of [false, true]) {
    const broken = copy(ordinary);
    const slot = broken.slots.find((one) => one.propers.includes('Gospel'));
    slot.anchor = 'technical-missing-anchor'; slot.qualified = qualified;
    const name = qualified ? 'Gospel (technical qualified control)' : 'Gospel';
    assert.throws(() => S.validateProperSeating(broken, [{...mapped, name}], ctx), /no usable/);
  }
  assert.throws(() => S.prepareProperAppointments([unknown], {calendar: ordinary.calendar, entrance: 'propers'}), /foreign-source/);
  assert.throws(() => S.unframedEvents([unknown]), /foreign-source/);
  const hidden = {...unknown, name: 'Placeholder'};
  assert.throws(() => S.unframedEvents([hidden], (one) => one.name === 'Placeholder'), /foreign-source/);
  assert.throws(() => S.properUnits([hidden], seating, (one) => one.name === 'Placeholder'), /foreign-source/);
});
process.stdout.write(JSON.stringify({status: 'pass', groups: checks.length, checks}) + '\n');
