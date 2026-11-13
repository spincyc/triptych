'use strict';

// Real producer data supplies both the appointments and wording. Negative
// controls alter private metadata copies; they never manufacture a prayer.
const fs = require('fs');
const path = require('path');
const assert = require('node:assert/strict');
const [root, dataRoot, testCase] = process.argv.slice(2);
const read = relative => JSON.parse(fs.readFileSync(path.join(dataRoot, relative), 'utf8'));
const fixture = name => JSON.parse(fs.readFileSync(path.join(root,
  'tools/tests/fixtures/liturgy-reader-state/v1', name), 'utf8')).requested;
const S = require(path.join(root, 'src/web/browser/liturgy/ordinary-seating.js'));
const A = require(path.join(root, 'src/web/browser/liturgy/reader-state-adapters.js'));
const M = require(path.join(root, 'src/web/browser/liturgy/assembly-model.js'));
const book = read('structure/ordinary/roman-1962.json');
const structure = read('structure/propers/roman-1962.json');
const clone = value => JSON.parse(JSON.stringify(value));
const rites = book.proper_rites || [];
const rite = rites.find(row => row.id === 'oratio-super-populum');
assert(rite, 'prepared Ordinary must hold the source-owned ferial rite');
assert(rite.appointments.length > 0);
const slot = book.slots.find(row => row.rite === rite.id);
const cue = book.sections.flatMap(section => section.elements).find(element =>
  (element.conditions || []).some(condition => condition.kind === 'include-when-proper-rite' && condition.rite === rite.id));
assert(slot && cue);
const cueId = 'ordinary-element/' + cue.key;
const finalGreetingId = 'ordinary-element/' + slot.anchor;
const shown = source => source.sections.flatMap(section => section.elements.map(element => ({section, element})));
const massOf = key => {
  const mass = structure.masses.find(row => row.key === key);
  assert(mass, 'held source Mass: ' + key);
  return mass;
};
const formOf = (mass, formId) => (mass.forms || []).find(form => form.id === formId) || null;
const frameOf = (mass, form) => (form && form.ordinary_frame) || mass.ordinary_frame || {applicability: 'full'};
function contextFor(appointment, data = structure) {
  const mass = data.masses.find(row => row.key === appointment.mass);
  assert(mass);
  const form = formOf(mass, appointment.form_id);
  return {calendar: data.calendar, mass: mass.key, formId: appointment.form_id,
    properRows: form ? form.propers : mass.propers};
}
function requestFor(appointment, language, missal = true) {
  const mass = massOf(appointment.mass);
  const request = {...fixture('propers-roman-1962-advent-1.json'),
    formulary: {id: mass.key, type: mass.kind},
    languages: {orations: language, ordinary: language},
    requestedMode: missal ? 'missal' : 'read',
    options: {ordinary: missal, legitimate: {}}};
  if (mass.forms && mass.forms.length) request.form = appointment.form_id;
  return request;
}
function adapt(appointment, language, missal = true, data = structure, ordinary = book) {
  return A.adaptPropers({request: requestFor(appointment, language, missal), structure: data, ordinary});
}
function riteEvent(result) {
  const found = result.events.filter(event => event.properRite && event.properRite.id === rite.id);
  assert.equal(found.length, 1, 'one independently appointed rite');
  return found[0];
}
function rejectsOrReports(operation, reason) {
  let result;
  try { result = operation(); }
  catch (error) { assert(error instanceof Error); return; }
  assert(result.coverage.some(row => ['unsupported', 'unresolved', 'partial'].includes(row.state)), reason);
  assert((result.ordinaryUnresolved || []).length || result.coverage.some(row =>
    row.scope === 'oration-execution' || row.scope === 'ordinary-placement:roman-1962' ||
    (row.reasons || []).some(item => item.kind === 'ordinary-element-unresolved' || item.kind === 'text-not-held')), reason);
}
let checks = 0;

if (testCase === 'exact-appointments') {
  const before = JSON.stringify(structure);
  for (const appointment of rite.appointments) {
    const context = contextFor(appointment);
    const projected = S.properRitesFor(book, context);
    assert.equal(projected.states[rite.id], true);
    assert.equal(projected.bindings.length, 1);
    const binding = projected.bindings[0];
    assert.deepEqual(binding.descriptor.appointment, {
      mass: appointment.mass, form_id: appointment.form_id,
      proper: appointment.proper, occurrence: appointment.occurrence});
    assert.equal(binding.descriptor.semanticRole, 'prayer-over-people');
    assert.equal(binding.descriptor.ownConclusion, true);
    assert.equal(context.properRows[binding.descriptor.sourceIndex], binding.proper);
    const seating = S.seats(book, shown(book), context);
    assert.equal(S.usableSlotOf(seating, binding.proper), book.slots.indexOf(slot));
    assert.equal(S.usableSlotOf(seating, appointment.proper), -1, 'a name alone cannot bind the rite');
    if (appointment.proper === 'Oratio') {
      for (const proper of context.properRows.filter(row => row.name === 'Oratio' && row !== binding.proper)) {
        assert.equal(S.usableSlotOf(seating, proper), -1, 'earlier Ember prayers stay unclaimed');
      }
    }
    checks++;
  }
  assert.equal(JSON.stringify(structure), before);
  assert.deepEqual(rite.appointments.filter(row => row.proper === 'Oratio')
    .map(row => [row.form_id, row.occurrence]), [['longer', 6], ['shorter', 2]]);
}

if (testCase === 'scope-refusals') {
  const target = rite.appointments.find(row => row.mass === 'passion-friday');
  assert(target);
  const context = contextFor(target);
  const alterations = [
    value => { value.calendar = 'postconciliar'; },
    value => { value.formId = null; },
    value => { value.properRows.pop(); },
    value => { value.properRows.at(-1).appointment_identity = {
      mass: 'unrelated', form_id: 'main', proper: target.proper, occurrence: 1}; },
    value => { value.properRows.at(-1).appointment_applicability = {source_edition: 'other'}; },
    value => { value.properRows = value.properRows.map((proper, sourceIndex) =>
      ({proper, sourceIndex, sourceMass: 'unrelated-source-owner'})); }
  ];
  for (const alter of alterations) {
    const changed = clone(context); alter(changed);
    assert.throws(() => S.properRitesFor(book, changed)); checks++;
  }
  const malformed = [
    value => { value.proper_rites[0].appointments.push(clone(value.proper_rites[0].appointments[0])); },
    value => { value.proper_rites[0].default = true; },
    value => { value.proper_rites[0].own_conclusion = false; },
    value => { value.proper_rites[0].appointments[0].occurrence = 0; },
    value => { value.proper_rites[0].appointments[0].locus = ''; }
  ];
  for (const alter of malformed) {
    const changed = clone(book); alter(changed);
    assert.throws(() => S.properRitesFor(changed, context)); checks++;
  }
}

if (testCase === 'unknown-and-unrelated') {
  assert.equal(S.properRitesFor(book).states[rite.id], null);
  const unknown = S.resolveElements(book, {}, {[rite.id]: true});
  assert(!unknown.shown.some(row => row.element.key === cue.key));
  assert(unknown.unresolved.some(row => row.element === cue.key)); checks++;
  for (const key of ['lent-1', 's-ioseph-sponsi-beatae-mariae-virginis',
    's-ioannis-damasceni-confessoris-ecclesiae-doctoris', 'good-friday']) {
    const context = {calendar: structure.calendar, mass: key, formId: 'main', properRows: massOf(key).propers};
    assert.equal(S.properRitesFor(book, context).states[rite.id], false);
    const result = S.resolveElements(book, {}, {'proper-rite-context': context, [rite.id]: true});
    assert(!result.shown.some(row => row.element.key === cue.key));
    assert(!result.unresolved.some(row => row.element === cue.key)); checks++;
  }
  const context = contextFor(rite.appointments.find(row => row.mass === 'passion-friday'));
  assert.throws(() => S.properRitesFor(book, {...context, formId: 'unheld'}));
  assert.equal(S.properRitesFor(book, {...context, mass: 'unrelated'}).states[rite.id], false); checks++;
}

if (testCase === 'bilingual-adapters') {
  const before = JSON.stringify(structure);
  for (const appointment of rite.appointments) for (const language of ['en', 'la']) {
    const result = adapt(appointment, language), quoted = adapt(appointment, language, false);
    assert.deepEqual(result.events.filter(row => row.kind === 'proper').map(row => row.id),
      quoted.events.filter(row => row.kind === 'proper').map(row => row.id));
    const prayer = riteEvent(result), original = riteEvent(quoted);
    assert.deepEqual(prayer.selected, original.selected);
    assert.equal(prayer.selected.availability, 'held');
    assert.equal(prayer.semanticSlot.identity.id, 'prayer-over-people');
    assert.equal(prayer.orationGroups, undefined);
    const mass = massOf(appointment.mass), frame = frameOf(mass, formOf(mass, appointment.form_id));
    const cues = result.events.filter(row => row.id === cueId);
    if (frame.applicability === 'full') {
      assert.equal(cues.length, 1);
      assert.equal(cues[0].selected.availability, 'held');
      const witness = cue.translations.find(row => row.lang === language && row.source_id === cues[0].selected.sourceId);
      assert(witness);
      assert.deepEqual(witness.turns.map(turn => turn.speaker), ['priest', 'deacon-or-priest']);
      assert(witness.turns.every(turn => !turn.dialogue_role && !turn.printed_marker));
      assert.equal(cues[0].selected.text, witness.text);
      const pc = result.events.findIndex(row => row.editionSlotLabel === 'Postcommunion');
      const cueIndex = result.events.indexOf(cues[0]), prayerIndex = result.events.indexOf(prayer);
      const final = result.events.findIndex(row => row.id === finalGreetingId);
      assert(pc >= 0 && pc < cueIndex && cueIndex < prayerIndex && prayerIndex < final);
      assert.equal(result.events.filter(row => row.id === finalGreetingId).length, 1);
      assert(!result.events.slice(pc + 1, prayerIndex).some(row =>
        row.kind === 'ordinary-element' && /dominus-vobiscum/.test(row.id)));
      assert.equal(prayer.seat.id, slot.key);
    } else {
      assert.equal(cues.length, 0);
      assert(!result.events.some(row => row.kind === 'ordinary-element'));
      assert(result.coverage.some(row => row.scope === 'ordinary-placement:roman-1962'));
    }
    checks++;
  }
  assert.equal(JSON.stringify(structure), before);
}

if (testCase === 'day-commemorations') {
  const year = read('structure/calendar/roman-1962/2026.json');
  const rubrics = read('structure/rubrics/roman-1962.json');
  const derived = M.derive({date: '2026-03-27', year, rubrics});
  for (const language of ['en', 'la']) {
    const request = {...fixture('day-roman-1962-2026-08-02.json'), civilDate: '2026-03-27',
      selectedReadableFormulary: {id: 'passion-friday'},
      requestedMode: 'missal', languages: {orations: language, ordinary: language},
      options: {ordinary: true, legitimate: {}}};
    const result = A.adaptDay({request, derived, structure, ordinary: book, rubrics});
    const prayer = riteEvent(result);
    const pc = result.events.find(row => row.editionSlotLabel === 'Postcommunion');
    assert(pc && pc.orationGroups.length >= 2, 'actual March 27 commemorations remain seated');
    assert(pc.orationGroups.every(group => group.members.every(member => !member.properRite)));
    assert.equal(prayer.orationGroups, undefined);
    assert.equal(result.events.filter(row => row.id === cueId).length, 1);
    assert(result.events.indexOf(pc) < result.events.findIndex(row => row.id === cueId));
    assert(result.events.findIndex(row => row.id === cueId) < result.events.indexOf(prayer));
    assert(result.events.indexOf(prayer) < result.events.findIndex(row => row.id === finalGreetingId));
    checks++;
  }
}

if (testCase === 'complete-conclusions') {
  for (const appointment of rite.appointments) for (const language of ['en', 'la']) {
    const result = adapt(appointment, language), prayer = riteEvent(result);
    const projected = prayer.properRiteExecution && prayer.properRiteExecution.languages[language];
    assert(projected, appointment.mass + '/' + appointment.form_id + '/' + language);
    assert.equal(projected.state, 'source-derived-complete',
      appointment.mass + '/' + appointment.form_id + '/' + language + ': ' + (projected.reasons || []).join(', '));
    assert.equal(projected.members.length, 1);
    const member = projected.members[0];
    assert.equal(member.id, prayer.id);
    assert.equal(member.source_text, prayer.selected.text);
    assert(member.priest_text && member.source_hooks.length > 0);
    assert(projected.response && projected.response.text);
    assert.equal(projected.response.provider_id, prayer.id);
    assert.deepEqual(prayer.conclusionExecution.languages[language].member, member);
    assert.deepEqual(prayer.conclusionExecution.languages[language].response, projected.response);
    assert.equal(prayer.orationGroups, undefined);
    for (const postcommunion of result.events.filter(row => row.editionSlotLabel === 'Postcommunion')) {
      assert(!(postcommunion.orationGroups || []).some(group => group.members.some(row => row.id === prayer.id)));
    }
    assert(!result.explicitAbsences.some(row => row.scope === 'oration-execution' && row.event === prayer.id));
    checks++;
  }
}

if (testCase === 'missing-conclusion') {
  const target = rite.appointments.find(row => row.mass === 'passion-friday');
  const changed = clone(structure);
  const context = contextFor(target, changed);
  const bound = S.properRitesFor(book, context).bindings[0].proper;
  delete bound.conclusion_execution;
  for (const language of ['en', 'la']) for (const missal of [false, true]) {
    const result = adapt(target, language, missal, changed);
    const prayer = riteEvent(result);
    assert.equal(prayer.properRiteExecution.languages[language].state, 'unresolved');
    assert(prayer.properRiteExecution.unresolved.length > 0);
    assert.equal(prayer.conclusionExecution.languages[language].member, null);
    assert.equal(prayer.conclusionExecution.languages[language].response, null);
    assert(result.coverage.some(row => row.scope === 'oration-execution' && row.state === 'unsupported'));
    assert(result.explicitAbsences.some(row => row.scope === 'oration-execution' && row.event === prayer.id));
    checks++;
  }
}

if (testCase === 'broken-frame') {
  const target = rite.appointments.find(row => row.mass === 'passion-friday');
  const context = contextFor(target);
  const malformed = [
    value => { value.slots = value.slots.filter(row => row.rite !== rite.id); },
    value => { value.slots.find(row => row.rite === rite.id).anchor = 'conclusio/unheld'; },
    value => { for (const section of value.sections) section.elements = section.elements.filter(row => row.key !== cue.key); },
    value => { const section = value.sections.find(row => row.elements.some(element => element.key === cue.key));
      section.elements.push(clone(section.elements.find(row => row.key === cue.key))); },
    value => { value.slots.find(row => row.rite === rite.id).propers = ['Oratio']; }
  ];
  for (const alter of malformed) {
    const changed = clone(book); alter(changed);
    assert.throws(() => S.properRitesFor(changed, context));
    assert.throws(() => adapt(target, 'la', true, structure, changed)); checks++;
  }
  const missingText = clone(book);
  const missingCue = missingText.sections.flatMap(row => row.elements).find(row => row.key === cue.key);
  missingCue.translations = [];
  rejectsOrReports(() => adapt(target, 'en', true, structure, missingText), 'missing cue text cannot be complete'); checks++;
  const unknown = clone(context.properRows);
  unknown.splice(unknown.length - 1, 0, {name: 'Oratio', form_id: 'main', source: 'composed'});
  assert.throws(() => S.validateProperSeating(book, unknown, {calendar: structure.calendar,
    mass: target.mass, form_id: target.form_id, full: true, facts: structure.proper_appointment_facts})); checks++;
  const backward = clone(context.properRows).reverse();
  assert.throws(() => S.validateProperSeating(book, backward, {calendar: structure.calendar,
    mass: target.mass, form_id: target.form_id, full: true, facts: structure.proper_appointment_facts})); checks++;
}

if (testCase === 'remaining-frames') {
  for (const key of ['lent-1-tuesday', 'lent-4-thursday', 'passion-wednesday']) {
    const mass = massOf(key), appointment = rite.appointments.find(row => row.mass === key && row.form_id === 'main');
    const held = mass.propers.filter(row => row.name === 'Oratio super populum');
    if (appointment) assert.equal(held.length, 1);
    else {
      assert.equal(held.length, 0);
      assert.equal(frameOf(mass).applicability, 'unavailable');
      assert(/whole source appointment|not yet held|not.*held/i.test(frameOf(mass).basis));
    }
    const result = adapt({mass: key, form_id: 'main'}, 'en');
    if (!appointment) {
      assert(!result.events.some(row => row.kind === 'ordinary-element'));
      assert(result.coverage.some(row => row.scope === 'ordinary-placement:roman-1962'));
    }
    checks++;
  }
  const sourceBefore = JSON.stringify(structure);
  for (const mass of structure.masses) for (const form of mass.forms || [{id: 'main'}]) {
    const frame = frameOf(mass, form);
    if (frame.applicability === 'full') continue;
    const result = adapt({mass: mass.key, form_id: form.id}, 'la');
    assert(!result.events.some(row => row.kind === 'ordinary-element'));
    assert(!result.events.some(row => row.id === cueId));
    assert(result.coverage.some(row => row.scope === 'ordinary-placement:roman-1962'));
    checks++;
  }
  assert.equal(JSON.stringify(structure), sourceBefore);
}

assert(checks > 0, 'unknown or empty test case: ' + testCase);
process.stdout.write(JSON.stringify({case: testCase, checks}) + '\n');
