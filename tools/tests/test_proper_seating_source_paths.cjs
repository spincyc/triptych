'use strict';
// The static gate validates every original candidate and every authored tuple;
// it does not choose a calendar course or an actual-use path.
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const root = path.resolve(__dirname, '../..');
const S = require(path.join(root, 'src/web/browser/liturgy/ordinary-seating.js'));
const structurePath = process.env.TRIPTYCH_SOURCE_PATH_STRUCTURE || path.join(root, 'src/web/data/structure/propers/postconciliar.json');
const structure = JSON.parse(fs.readFileSync(structurePath));
const ordinary = JSON.parse(fs.readFileSync(path.join(root, 'src/web/data/structure/ordinary/postconciliar.json')));
const copy = (value) => JSON.parse(JSON.stringify(value));
const masses = structure.masses.filter((mass) => (mass.proper_source_paths || []).length);
const records = [];
assert.equal(masses.length, 29);
assert.equal(masses.reduce((n, mass) => n + mass.proper_source_paths.length, 0), 31);
assert.deepEqual(masses.flatMap((mass) => mass.proper_source_paths.map((relation) =>
  mass.key + '/' + relation.form_id + '/' + relation.id)).sort(), [
  'advent-1-monday/main/advent-first-reading',
  'advent-1-monday/main/advent-psalm-strophes',
  'baptism-of-the-lord/main/baptism-reading-provisions',
  'easter-4-monday/main/easter-4-monday-gospel',
  'easter-6/main/easter-6-readings',
  'easter-sunday/main/easter-day-gospel',
  'easter-sunday/main/easter-day-second-reading',
  'holy-family/main/holy-family-reading-provisions',
  'lent-3/main/lent-3-readings',
  'lent-4/main/lent-4-readings',
  'lent-5/main/lent-5-readings',
  ...[3, 4, 5].flatMap(week => ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday'].map(day =>
    `lent-${week}-${day}/main/lent-${week}-${day}-reading-course`)),
  'palm-sunday/main/palm-procession-gospel',
  'pentecost/day/pentecost-day-readings'
].sort(), 'a count cannot replace an exact source-owned relation inventory');
const ferialExtents = {
  'easter-4-monday/main/easter-4-monday-gospel': [
    ['john-10-1-10', 'Gospel', 1], ['john-10-11-18-a', 'Gospel', 2]
  ],
  'advent-1-monday/main/advent-first-reading': [
    ['isaiah-2', 'First Reading', 1], ['isaiah-4', 'First Reading', 2]
  ],
  'advent-1-monday/main/advent-psalm-strophes': [
    ['without-parenthesized-block', 'Responsorial Psalm', 1],
    ['with-parenthesized-block', 'Responsorial Psalm', 2]
  ]
};
for (const week of [3, 4, 5]) for (const day of ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday']) {
  const key = `lent-${week}-${day}`, number = {3: 236, 4: 243, 5: 250}[week];
  const shared = key === 'lent-3-thursday', monday = key === 'lent-5-monday';
  const psalms = [['Responsorial Psalm', 1], ...(key === 'lent-3-monday' ? [['Responsorial Psalm', 2]] : [])];
  const extent = [];
  if (monday) {
    for (const [id, occurrence] of [['john-8-1-11-ab', 1], ['john-8-1-11-c', 1], ['john-8-12-20-c', 2]]) {
      for (const daniel of ['longer', 'shorter']) extent.push(...[
        [daniel === 'longer' ? 'First Reading' : 'First Reading (shorter form)', 1],
        ...psalms, ['Verse Before the Gospel', 1], ['Gospel', occurrence]
      ].map(([role, ordinal]) => [id + '-' + daniel, role, ordinal]));
    }
  } else extent.push(...[['First Reading', 1], ...psalms, ['Verse Before the Gospel', 1], ['Gospel', 1]]
    .map(([role, ordinal]) => ['ferial', role, ordinal]));
  extent.push(...[['First Reading', 2], ['Responsorial Psalm', shared ? 1 : key === 'lent-3-monday' ? 3 : 2],
    ['Verse Before the Gospel', 2], ['Gospel', monday ? 3 : 2]]
    .map(([role, ordinal]) => ['course-' + number, role, ordinal]));
  ferialExtents[key + '/main/' + key + '-reading-course'] = extent;
}
const monday = masses.find(mass => mass.key === 'lent-5-monday');
for (const sourcePath of monday.proper_source_paths[0].paths) {
  if (sourcePath.id.startsWith('john-8-1-11-')) {
    assert.equal(sourcePath.standing, 'principal');
    assert.equal(Object.hasOwn(sourcePath, 'when'), false);
  } else if (sourcePath.id.startsWith('john-8-12-20-c-')) {
    assert.equal(sourcePath.standing, 'optional');
    assert.deepEqual(sourcePath.when, {fact: 'lent-5-sunday-john-8-1-11-actually-read', is: true});
  }
}
for (const mass of masses) for (const relation of mass.proper_source_paths) {
  const id = mass.key + '/' + relation.form_id + '/' + relation.id;
  if (!Object.prototype.hasOwnProperty.call(ferialExtents, id)) continue;
  assert.deepEqual(relation.paths.flatMap((one) => one.members.map((member) =>
    [one.id, member.appointment.proper, member.appointment.occurrence])), ferialExtents[id],
  id + ' must retain every exact source path and its original semantic role');
}
function context(mass, form) {
  return {calendar: structure.calendar, mass: mass.key, form_id: form.id,
    full: ((form.ordinary_frame || mass.ordinary_frame || {}).applicability || 'full') === 'full',
    facts: structure.proper_appointment_facts || {}, sourcePaths: mass.proper_source_paths};
}
for (const mass of masses) for (const form of mass.forms || [{id: 'main', propers: mass.propers}]) {
  const original = JSON.stringify(form.propers);
  const result = S.validateProperSeating(ordinary, form.propers, context(mass, form));
  assert.equal(result.candidates, form.propers.filter((proper) => proper.name !== 'Placeholder').length);
  assert.equal(JSON.stringify(form.propers), original);
  records.push({mass: mass.key, form: form.id, candidates: result.candidates,
    paths: mass.proper_source_paths.filter((relation) => relation.form_id === form.id)
      .reduce((n, relation) => n + relation.paths.length, 0)});
}
const mass = masses.find((one) => one.key === 'lent-3');
const propers = mass.propers;
const ctx = context(mass, {id: 'main'});
const malformed = copy(propers);
const inactive = malformed.find((proper) => proper.source_path_relation && proper.name === 'First Reading (shorter form)');
assert(inactive);
inactive.name = 'Unmapped source role';
inactive.appointment_identity.proper = inactive.name;
const changedRelations = copy(mass.proper_source_paths);
changedRelations.forEach((relation) => relation.paths.forEach((one) => one.members.forEach((member) => {
  if (member.appointment.proper === 'First Reading (shorter form)') member.appointment.proper = inactive.name;
})));
assert.throws(() => S.validateProperSeating(ordinary, malformed, {...ctx, sourcePaths: changedRelations}),
  /no usable|one.*seat|mapped|semantic|functional/);
const missing = copy(propers);
delete missing.find((proper) => proper.source_path_relation).source_path_relation;
assert.throws(() => S.validateProperSeating(ordinary, missing, ctx), /guard|membership/);
const wrong = copy(mass.proper_source_paths);
wrong[0].paths[0].members[0].material_cycle.cycle = 'D';
assert.throws(() => S.validateProperSeating(ordinary, propers, {...ctx, sourcePaths: wrong}), /not held/);
assert.throws(() => S.validateProperSeating(ordinary, propers, {...ctx, sourcePaths: null}), /must be a source-owned relation list/);
const foreignProps = copy(propers);
const target = 'contract-target';
foreignProps.forEach((proper) => {
  if (proper.source_path_relation) proper.appointment_applicability = {
    state: 'unresolved', reason: 'foreign-source-applicability', source_edition: structure.calendar,
    target_edition: target, basis: 'Technical original foreign extent control; no target rule claim.'
  };
});
const foreign = S.validateProperSeating({...ordinary, calendar: target}, foreignProps, {...ctx, calendar: target});
assert.equal(foreign.diagnostics.length, foreignProps.filter((proper) => proper.source_path_relation).length);
assert.throws(() => S.prepareProperAppointments(foreignProps, {
  calendar: target, entrance: 'propers', mass: mass.key, formId: 'main', sourcePaths: mass.proper_source_paths
}), /foreign-source/);
const purePath = foreignProps.find((proper) => proper.source_path_relation && !proper.ordinary_disposition);
assert(purePath, 'a foreign path row without a disposition must retain its guard');
const placeholder = {...purePath, name: 'Placeholder'};
assert.throws(() => S.unframedEvents([placeholder], (proper) => proper.name === 'Placeholder'), /foreign-source/);
const unmarked = copy(foreignProps);
delete unmarked.find((proper) => proper.source_path_relation).appointment_applicability;
assert.throws(() => S.validateProperSeating({...ordinary, calendar: target}, unmarked, {...ctx, calendar: target}),
  /every original unsupported/);
const report = {status: 'pass', actualForms: records.length,
  actualCandidates: records.reduce((n, one) => n + one.candidates, 0),
  authoredPaths: records.reduce((n, one) => n + one.paths, 0), records,
  negatives: ['inactive unmapped candidate', 'missing exact guard', 'wrong material selector',
    'explicit malformed relation map', 'foreign marker missing', 'raw foreign pure-path placeholder bypass'],
  foreignDiagnostics: foreign.diagnostics.length};
process.stdout.write(JSON.stringify(report) + '\n');
