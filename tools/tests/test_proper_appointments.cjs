'use strict';
// Synthetic contract fixtures plus held source-body equality controls.
// No Missal wording is copied into this test.
const assert = require('assert');
const fs = require('fs');
const path = require('path');
const root = path.resolve(__dirname, '../..');
const moduleRoot = path.join(root, 'src/web/browser/liturgy');
const S = require(path.join(moduleRoot, 'ordinary-seating.js'));
const A = require(path.join(moduleRoot, 'reader-state-adapters.js'));
const C = require(path.join(moduleRoot, 'reader-state.js'));
const results = [];
function test(id, fn) { fn(); results.push(id); }
const copy = (x) => JSON.parse(JSON.stringify(x));
const edition = 'roman-1962';
const massKey = 'contract-formulary';
const owner = 'contract-common';
const factId = 'contract-chant-regime';
const facts = {[factId]: {edition, values: ['advent', 'regular', 'tract', 'paschal'],
  season_values: {advent: 'advent', epiphanytide: 'regular', septuagesima: 'tract',
    lent: 'tract', passiontide: 'tract', paschaltide: 'paschal',
    'after-pentecost': 'regular', christmastide: 'regular', triduum: null},
  basis: 'Synthetic source fact binding, not an historical source claim.'}};
const coordinate = (proper) => ({mass: owner, form_id: 'main', proper, occurrence: 1});
const anchor = coordinate('Alleluia');
const gospelAnchor = coordinate('Gospel');
const choiceId = (group) => 'proper-choice/' + edition + '/' + massKey + '/main/' + group;
function sourceRow(name) {
  return {name, form: '', form_id: 'main', source: 'composed', text: 'Contract-only fixture.',
    citations: [], cycles: {}, translations: [], taken_from: null};
}
function fixture(missingBody = false) {
  const names = ['Introit', 'Collect', 'Epistle', 'Gradual', 'Alleluia', 'Tract',
    'Alleluia (Tempore paschali)', 'Alleluia (second constituent)', 'Gospel',
    'Offertory', 'Secret', 'Communion', 'Postcommunion', 'Gospel (additional reading)'];
  const propers = names.map(sourceRow);
  propers[3].appointment_identity = coordinate('Gradual');
  propers[3].ordinary_disposition = {kind: 'conditional', group: 'common-gradual',
    basis: 'Synthetic conditional source rule.', when: {fact: factId, in: ['advent', 'regular', 'tract']}};
  [[4, 'regular', ['advent', 'regular']], [5, 'tract', ['tract']],
    [6, 'paschal', ['paschal']], [7, 'paschal', ['paschal']]].forEach(([index, option, values]) => {
    propers[index].appointment_identity = coordinate(names[index]);
    propers[index].ordinary_disposition = {kind: 'alternative', group: 'common-acclamation', option,
      basis: 'Synthetic acclamation alternatives.', anchor: copy(anchor), when: {fact: factId, in: values}};
  });
  [[8, 'principal'], [13, 'additional']].forEach(([index, option]) => {
    propers[index].appointment_identity = coordinate(names[index]);
    propers[index].ordinary_disposition = {kind: 'alternative', group: 'gospel-reading', option,
      basis: 'Synthetic distant Gospel alternatives.', anchor: copy(gospelAnchor)};
  });
  if (missingBody) {
    propers[6].text = null;
    propers[6].text_status = {state: 'unavailable', scope: 'proper-body'};
  }
  return {calendar: edition, translations: [], proper_appointment_facts: copy(facts), masses: [
    {key: massKey, kind: 'common', propers}
  ]};
}
function request(entrance = 'propers') {
  const result = {schema: C.STATE_SCHEMA, entrance, edition: {id: edition},
    bible: {id: 'douay-rheims', numbering: 'vulgate'}, languages: {orations: 'la'},
    requestedMode: 'read', options: {ordinary: false, legitimate: {}},
    coverage: [], unresolvedChoices: [], sourceHooks: []};
  if (entrance === 'day') {
    result.civilDate = '2026-04-15'; result.calendar = {id: edition};
    result.apparatus = {why: false, rubrics: true};
  } else { result.civilDate = null; result.formulary = {id: massKey, type: 'common'}; }
  return result;
}
function derived(season = 'paschaltide') {
  return {calendar: edition, date: '2026-04-15', weekday: 'wednesday', season,
    liturgicalYear: {lectionary: null, anchors: {}}, options: [{option: null,
      settled: true, winner: {id: massKey, nature: 'feast'},
      readable: [{key: massKey, state: 'said'}], absent: []}]};
}
function prepare(structure, context = {}) {
  return S.prepareProperAppointments(structure.masses[0].propers, {
    calendar: edition, entrance: 'propers', facts: structure.proper_appointment_facts, ...context});
}
const groupEvent = (result, group) => result.events.find((e) => e.kind === 'proper-choice' && e.group === group);
const performed = (events) => events.flatMap((event) => event.kind === 'proper-choice'
  ? event.selection.state === 'selected' ? event.options.find((o) => o.id === event.selection.option).events : []
  : [event]);
const allEvents = (events) => events.flatMap((event) => event.kind === 'proper-choice'
  ? event.options.flatMap((option) => allEvents(option.events)) : [event]);
function payloadFor(structure, req) {
  return {date: req.civilDate, scripture: {id: req.bible.id}, days: [{calendar: edition,
    selected_territory: null, settled: true, why: {lectionary: null}, masses: [{
      key: massKey, standing: 'said', bible: {id: req.bible.id}, selected_form: 'main',
      proper_appointment_facts: copy(structure.proper_appointment_facts),
      propers: structure.masses[0].propers.map((proper) => ({...copy(proper),
        verses: (proper.citations || []).map((citation) => ({ref: citation.ref, text: 'Synthetic Bible component.'}))}))
    }]}]};
}
const foreignEdition = 'roman-pre-1955';
function foreignFixture() {
  const proper = {...sourceRow('Gradual'), text: 'Synthetic held wording, not an applicability claim.',
    taken_from: {mass: owner, form: '', proper: 'Gradual'},
    appointment_applicability: {state: 'unresolved', reason: 'foreign-source-applicability',
      source_edition: edition, target_edition: foreignEdition,
      basis: 'Synthetic source-owned conditional appointment.'}};
  return {calendar: foreignEdition, proper_appointment_facts: {}, translations: [],
    masses: [{key: massKey, kind: 'common', propers: [proper]}]};
}
function foreignRequest(entrance = 'propers') {
  const req = request(entrance); req.edition.id = foreignEdition;
  if (req.calendar) req.calendar.id = foreignEdition;
  return req;
}

test('undated source applicability stays required with a separate conditional obligation', () => {
  const structure = fixture(); const before = JSON.stringify(structure);
  const prepared = prepare(structure);
  assert.equal(prepared.selections['main/common-acclamation'].state, 'required');
  assert.equal(prepared.unresolved.length, 1);
  assert(!prepared.rows.some((row) => row.proper.name === 'Gradual'));
  assert.equal(JSON.stringify(structure), before);
});
test('owned seasons select exact options and omit Gradual only in the source paschal regime', () => {
  for (const [season, option] of [['advent', 'regular'], ['epiphanytide', 'regular'],
    ['septuagesima', 'tract'], ['lent', 'tract'], ['passiontide', 'tract'], ['paschaltide', 'paschal']]) {
    const prepared = prepare(fixture(), {entrance: 'day', date: '2026-04-15', season});
    assert.equal(prepared.selections['main/common-acclamation'].option, option);
    assert.equal(prepared.rows.some((row) => row.proper.name === 'Gradual'), option !== 'paschal');
  }
});
test('a source-specific fourth Advent option selects independently of the regular option', () => {
  const structure = fixture();
  structure.masses[0].propers[4].ordinary_disposition.when.in = ['regular'];
  const advent = sourceRow('Alleluia (In Adventu)');
  advent.appointment_identity = coordinate(advent.name);
  advent.ordinary_disposition = {...copy(structure.masses[0].propers[4].ordinary_disposition),
    option: 'advent', when: {fact: factId, in: ['advent']}};
  structure.masses[0].propers.push(advent);
  const prepared = prepare(structure, {entrance: 'day', date: '2026-12-01', season: 'advent'});
  assert.equal(prepared.selections['main/common-acclamation'].option, 'advent');
  assert(prepared.rows.some((row) => row.proper.name === 'Gradual'));
});
test('mapped null and missing owner facts stay unresolved without a regular default', () => {
  for (const context of [{entrance: 'day'}, {entrance: 'day', date: '2026-04-15'},
    {entrance: 'day', date: '2026-04-15', season: 'triduum'}]) {
    assert.equal(prepare(fixture(), context).selections['main/common-acclamation'].state, 'required');
  }
});
test('explicit undated option qualifies the view without adding a date or calendar fact', () => {
  const req = request(); req.properChoices = {[choiceId('common-acclamation')]: 'paschal'};
  const result = A.adaptPropers({request: req, structure: fixture()});
  assert.equal(result.calendarResult, null); assert.equal(result.request.civilDate, null);
  assert.equal(groupEvent(result, 'common-acclamation').selection.option, 'paschal');
  assert(!performed(result.events).some((event) => event.editionSlotLabel === 'Gradual'));
  assert.equal(groupEvent(result, 'gospel-reading').selection.state, 'required');
});
test('independent explicit group choices coexist and preserve a distant source ordinal', () => {
  const req = request(); req.properChoices = {[choiceId('common-acclamation')]: 'tract',
    [choiceId('gospel-reading')]: 'additional'};
  const result = A.adaptPropers({request: req, structure: fixture()});
  assert.equal(groupEvent(result, 'common-acclamation').selection.option, 'tract');
  const selected = groupEvent(result, 'gospel-reading').options.find((o) => o.id === 'additional').events[0];
  assert.equal(selected.id, 'proper/' + edition + '/' + massKey + '/014');
  assert(result.events.indexOf(groupEvent(result, 'gospel-reading')) < result.events.findIndex((e) => e.editionSlotLabel === 'Offertory'));
});
test('legacy scalar alternative remains a single explicit authored choice', () => {
  const req = request(); req.alternative = {id: choiceId('gospel-reading') + '/additional'};
  assert.equal(groupEvent(A.adaptPropers({request: req, structure: fixture()}), 'gospel-reading').selection.option, 'additional');
});
test('duplicate scalar and mapping declarations refuse even when equal', () => {
  const req = request(); req.alternative = {id: choiceId('gospel-reading') + '/additional'};
  req.properChoices = {[choiceId('gospel-reading')]: 'additional'};
  assert.throws(() => A.adaptPropers({request: req, structure: fixture()}), /duplicate explicit/);
});
test('Day selects source-compatible season and rejects incompatible explicit options', () => {
  const req = request('day'); const result = A.adaptDay({request: req, derived: derived(), structure: fixture()});
  assert.equal(groupEvent(result, 'common-acclamation').selection.option, 'paschal');
  req.properChoices = {[choiceId('common-acclamation')]: 'tract'};
  assert.throws(() => A.adaptDay({request: req, derived: derived(), structure: fixture()}), /contradicts source applicability/);
});
test('multirow selected option retains distinct source events inside one semantic seat', () => {
  const req = request(); req.properChoices = {[choiceId('common-acclamation')]: 'paschal'};
  const event = groupEvent(A.adaptPropers({request: req, structure: fixture()}), 'common-acclamation');
  const bundle = event.options.find((option) => option.id === 'paschal').events;
  assert.equal(bundle.length, 2); assert.notEqual(bundle[0].id, bundle[1].id);
  assert(bundle.every((row) => row.semanticSlot.identity.id === 'gospel-acclamation'));
});
test('selected missing body remains unavailable and an inactive body is not counted as performed', () => {
  const structure = fixture(true); const req = request('day');
  const paschal = A.adaptDay({request: req, derived: derived(), structure});
  const selected = performed(paschal.events).find((event) => event.editionSlotLabel === 'Alleluia (Tempore paschali)');
  assert.equal(selected.selected.reason, 'proper-body-unavailable');
  const regular = A.adaptDay({request: req, derived: derived('epiphanytide'), structure});
  const claims = regular.coverage.flatMap((row) => row.reasons || []).filter((reason) => reason.repositoryTerm === 'proper-body');
  assert.equal(claims.length, 0);
});
test('mixed cited components cannot replace an unavailable composed chant body', () => {
  const structure = fixture(true); const proper = structure.masses[0].propers[6];
  // The shape models a mixed chant with a held citation and a missing composed
  // constituent; these synthetic words do not establish a Missal wording.
  proper.source = 'mixed'; proper.citations = [{ref: 'Psalms 109:4'}];
  const req = request('day');
  const day = A.adaptDay({request: req, derived: derived(), structure});
  const selected = performed(day.events).find((event) => event.editionSlotLabel === proper.name).selected;
  assert.equal(selected.kind, 'composed'); assert.equal(selected.availability, 'unavailable');
  assert.equal(selected.reason, 'proper-body-unavailable'); assert.equal(selected.text, null);
  assert.deepEqual(selected.scriptureComponents, {bible: 'douay-rheims', numbering: 'vulgate',
    references: ['Psalms 109:4'], unresolved: []});
  assert.deepEqual(C.validateSelectedMaterial(selected), []);
  const payload = payloadFor(structure, req);
  const cli = A.adaptCli({request: req, derived: derived(), structure, payload});
  assert.deepEqual(cli.events, day.events); assert.deepEqual(cli.coverage, day.coverage);
  payload.days[0].masses[0].propers[6].verses[0].ref = 'Psalms 1:1';
  assert.throws(() => A.adaptCli({request: req, derived: derived(), structure, payload}), /mixed scripture components disagree/);
  for (const change of [
    (one) => { one.scriptureComponents.text = 'No body is allowed in component metadata.'; },
    (one) => { one.scriptureComponents.unresolved = [{reference: 'wrong', reason: 'absent'}]; },
    (one) => { one.kind = 'scripture'; }
  ]) {
    const invalid = copy(selected); change(invalid);
    assert(C.validateSelectedMaterial(invalid).some((error) => error.code === 'selected-scripture-components'));
  }
});
test('mixed held bodies and translation witnesses retain their own availability with CLI parity', () => {
  const structure = fixture(); const proper = structure.masses[0].propers[6];
  proper.source = 'mixed'; proper.citations = [{ref: 'Psalms 109:4'}];
  proper.translations = [{lang: 'en', source: 'Synthetic public witness', source_id: 'contract-witness',
    rights: 'public-domain', text: 'Synthetic exact translated mixed body.'}];
  const req = request('day'); req.languages.orations = 'en';
  const day = A.adaptDay({request: req, derived: derived(), structure});
  const selected = performed(day.events).find((event) => event.editionSlotLabel === proper.name).selected;
  assert.equal(selected.kind, 'composed'); assert.equal(selected.availability, 'held');
  assert.equal(selected.text, proper.translations[0].text); assert.equal(selected.sourceId, 'contract-witness');
  const payload = payloadFor(structure, req);
  payload.days[0].masses[0].propers.forEach((row) => {
    row.language_selection = row === payload.days[0].masses[0].propers[6]
      ? {requested: 'en', status: 'full-text', available: true, held: true, complete: true, texts: copy(proper.translations)}
      : {requested: 'en', status: 'fallback-latin', available: false, held: false,
        texts: [], fallback: {lang: 'la', text: row.text}};
  });
  const cli = A.adaptCli({request: req, derived: derived(), structure, payload});
  assert.deepEqual(cli.events, day.events);
  proper.translations = []; proper.untranslated = [{lang: 'en', state: 'unavailable',
    target: {mass: owner, form_id: 'main', proper: proper.name, occurrence: 1, cycle: 'all', extent: 'body'}}];
  const absent = performed(A.adaptDay({request: req, derived: derived(), structure}).events)
    .find((event) => event.editionSlotLabel === proper.name).selected;
  assert.equal(absent.kind, 'composed'); assert.equal(absent.reason, 'ledgered-untranslated');
  assert.equal(absent.availability, 'unavailable'); assert.equal(absent.text, null);
  assert.equal(absent.scriptureComponents.references[0], 'Psalms 109:4');
});
test('real held Virgin IV mixed body remains exact and its English absence stays unavailable', () => {
  const held = JSON.parse(fs.readFileSync(path.join(root, 'src/web/data/structure/propers/roman-1962.json'), 'utf8'));
  const mass = held.masses.find((one) => one.key === 'commune-virginum-4');
  assert(mass, 'the actual Common Virgin IV is held');
  const proper = mass.propers.find((one) => one.name === 'Alleluia (Tempore paschali)');
  assert.equal(proper.source, 'mixed'); assert(proper.text);
  const req = request(); req.formulary = {id: mass.key, type: mass.kind};
  const before = JSON.stringify(mass);
  const latin = allEvents(A.adaptPropers({request: req, structure: held}).events)
    .find((event) => event.editionSlotLabel === proper.name).selected;
  assert.equal(latin.kind, 'composed'); assert.equal(latin.availability, 'held');
  assert.equal(latin.text, proper.text);
  assert.deepEqual(latin.scriptureComponents.references, proper.citations.map((one) => one.ref));
  req.languages.orations = 'en';
  const english = allEvents(A.adaptPropers({request: req, structure: held}).events)
    .find((event) => event.editionSlotLabel === proper.name).selected;
  assert.equal(english.kind, 'composed'); assert.equal(english.availability, 'unavailable');
  assert.equal(english.reason, 'ledgered-untranslated'); assert.equal(english.text, null);
  assert.equal(JSON.stringify(mass), before);
});
test('pure Scripture citation behavior remains unchanged', () => {
  const structure = fixture(); const proper = structure.masses[0].propers[2];
  proper.source = 'scripture'; proper.text = null; proper.citations = [{ref: 'Psalms 109:4'}];
  const req = request('day');
  const day = A.adaptDay({request: req, derived: derived(), structure});
  const selected = performed(day.events).find((event) => event.editionSlotLabel === proper.name).selected;
  assert.equal(selected.kind, 'scripture'); assert.equal(selected.availability, 'held');
  assert.equal(selected.scriptureComponents, undefined);
  const cli = A.adaptCli({request: req, derived: derived(), structure, payload: payloadFor(structure, req)});
  assert.deepEqual(cli.events, day.events);
});
test('anchors are exact members, preserve raw arrays, and reject duplicate/wrong coordinates', () => {
  const structure = fixture(); const before = JSON.stringify(structure);
  const prepared = prepare(structure, {choices: {'main/common-acclamation': 'regular'}});
  const events = S.unframedEvents(prepared.rows, null, prepared.selections);
  const reading = events.find((e) => e.group === 'gospel-reading');
  assert.equal(reading.sourceIndex, 8);
  assert.equal(reading.options.find((o) => o.id === 'additional').rows[0].sourceIndex, 13);
  assert.equal(JSON.stringify(structure), before);
  for (const mutation of [
    (s) => { s.masses[0].propers[4].ordinary_disposition.anchor = coordinate('Gradual'); },
    (s) => { s.masses[0].propers[4].appointment_identity.mass = 'another-owner'; },
    (s) => { s.masses[0].propers[5].appointment_identity = copy(s.masses[0].propers[4].appointment_identity); },
    (s) => { s.masses[0].propers[4].ordinary_disposition.anchor.occurrence = 2; }
  ]) {
    const altered = fixture(); mutation(altered);
    assert.throws(() => { const p = prepare(altered); S.unframedEvents(p.rows, null, p.selections); }, /coordinate|owner|anchor/);
  }
});
test('unknown fact, value, owner season, wrong edition and unsupported conditions refuse', () => {
  for (const mutate of [
    (s) => { delete s.proper_appointment_facts[factId]; },
    (s) => { s.proper_appointment_facts[factId].edition = 'postconciliar'; },
    (s) => { s.masses[0].propers[3].ordinary_disposition.when.in = ['unheld']; },
    (s) => { s.masses[0].propers[3].ordinary_disposition.when.equals = 'regular'; }
  ]) { const s = fixture(); mutate(s); assert.throws(() => prepare(s), /unheld|malformed|condition|when/); }
  assert.throws(() => prepare(fixture(), {entrance: 'day', date: '2026-04-15', season: 'unheld'}), /unheld owner season/);
  assert.throws(() => prepare(fixture(), {date: '2026-04-15', season: 'paschaltide'}), /date-independent/);
});
test('unsupported mixed-seat group refuses and no nested choice relation is invented', () => {
  const s = fixture(); s.masses[0].propers[13].name = 'Gradual';
  assert.throws(() => A.adaptPropers({request: request(), structure: s}), /one established semantic seat/);
});
test('shared unframed anchored choices refuse different or unknown semantic seats', () => {
  for (const names of [['Gospel', 'Epistle'], ['Gospel', 'Unmapped source reading'],
    ['Unmapped source reading', 'Another unmapped reading']]) {
    const principal = coordinate(names[0]);
    const rows = names.map((name, index) => ({...sourceRow(name),
      appointment_identity: coordinate(name), ordinary_disposition: {kind: 'alternative',
        group: 'semantic-seat-control', option: index ? 'second' : 'first',
        anchor: copy(principal), basis: 'Synthetic exact anchored source group.'}}));
    const before = JSON.stringify(rows);
    for (const choices of [{}, {'main/semantic-seat-control': 'second'}]) {
      const prepared = S.prepareProperAppointments(rows, {calendar: edition, entrance: 'propers', choices});
      assert.throws(() => S.unframedEvents(prepared.rows, null, prepared.selections),
        /anchored Proper group must share one established semantic seat/);
    }
    assert.equal(JSON.stringify(rows), before);
  }
});
test('shared semantic guard preserves distant valid groups and legacy unmapped behavior', () => {
  const structure = fixture();
  const before = JSON.stringify(structure);
  const prepared = prepare(structure, {choices: {'main/common-acclamation': 'paschal',
    'main/gospel-reading': 'additional'}});
  const events = S.unframedEvents(prepared.rows, null, prepared.selections);
  const gospel = events.find((event) => event.group === 'gospel-reading');
  assert.equal(gospel.sourceIndex, 8);
  assert.equal(gospel.options.find((option) => option.id === 'additional').rows[0].sourceIndex, 13);
  assert.equal(events.find((event) => event.group === 'common-acclamation')
    .options.find((option) => option.id === 'paschal').rows.length, 2);
  assert.equal(JSON.stringify(structure), before);
  for (const names of [['Unmapped legacy one', 'Unmapped legacy two'], ['Gospel', 'Epistle']]) {
    const legacy = names.map((name, index) => ({...sourceRow(name),
      ordinary_disposition: {kind: 'alternative', group: 'legacy-unmapped',
        option: index ? 'second' : 'first', basis: 'Synthetic legacy source unit.'}}));
    assert.equal(S.unframedEvents(legacy)[0].kind, 'proper_choice');
  }
  const shown = [{element: {key: 'anchor'}}];
  const unusable = S.seats({slots: [{key: 'gospel', anchor: 'missing', where: 'after',
    propers: ['Gospel'], qualified: true}]}, shown);
  assert.throws(() => S.seatPropers(prepared.rows, unusable, null, prepared.selections),
    /one usable semantic Ordinary seat/);
});
test('derived foreign applicability blocks execution without changing held wording or body state', () => {
  const structure = foreignFixture(); const rows = structure.masses[0].propers;
  const before = JSON.stringify(structure);
  for (const entrance of ['propers', 'day']) {
    assert.throws(() => S.prepareProperAppointments(rows, {calendar: foreignEdition, entrance,
      date: entrance === 'day' ? '2026-04-15' : undefined, season: 'paschaltide'}),
      /unsupported foreign-source Proper applicability from roman-1962 in roman-pre-1955; source condition remains unresolved/);
  }
  assert.throws(() => S.unframedEvents(rows), /unsupported foreign-source Proper applicability/);
  assert.throws(() => S.seatPropers(rows, S.seats({slots: []}, [])), /unsupported foreign-source Proper applicability/);
  assert.throws(() => A.adaptPropers({request: foreignRequest(), structure}), /unsupported foreign-source Proper applicability/);
  const d = {...derived(), calendar: foreignEdition}; const req = foreignRequest('day');
  assert.throws(() => A.adaptDay({request: req, derived: d, structure}), /unsupported foreign-source Proper applicability/);
  const payload = payloadFor(structure, req); payload.days[0].calendar = foreignEdition;
  assert.throws(() => A.adaptCli({request: req, derived: d, structure, payload}), /unsupported foreign-source Proper applicability/);
  assert.equal(JSON.stringify(structure), before);
  assert(rows[0].text); assert.equal(rows[0].text_status, undefined);
  assert.equal(rows[0].untranslated, undefined); assert.equal(rows[0].unavailable_translations, undefined);
});
test('foreign applicability marker has closed enums, exact edition context and source basis', () => {
  const mutations = [
    (p) => { p.appointment_applicability = null; },
    (p) => { p.appointment_applicability.extra = true; },
    (p) => { p.appointment_applicability.state = 'held'; },
    (p) => { p.appointment_applicability.reason = 'body-unavailable'; },
    (p) => { p.appointment_applicability.source_edition = ''; },
    (p) => { p.appointment_applicability.source_edition = 'Roman 1962'; },
    (p) => { p.appointment_applicability.source_edition = foreignEdition; },
    (p) => { p.appointment_applicability.target_edition = 'another-edition'; },
    (p) => { p.appointment_applicability.basis = ' '; }
  ];
  for (const field of ['state', 'reason', 'source_edition', 'target_edition', 'basis']) {
    mutations.push((p) => { delete p.appointment_applicability[field]; });
  }
  for (const mutate of mutations) {
    const rows = foreignFixture().masses[0].propers; mutate(rows[0]);
    assert.throws(() => S.prepareProperAppointments(rows, {calendar: foreignEdition, entrance: 'propers'}),
      /appointment_applicability must retain exact unresolved foreign editions and source basis/);
  }
});
test('foreign applicability marker refuses before raw placeholder filtering', () => {
  const placeholder = {...foreignFixture().masses[0].propers[0], name: 'Placeholder'};
  const rows = [placeholder, sourceRow('Gospel')]; const before = JSON.stringify(rows);
  const isPlaceholder = (proper) => proper.name === 'Placeholder';
  assert.throws(() => S.unframedEvents(rows, isPlaceholder), /unsupported foreign-source Proper applicability/);
  assert.throws(() => S.seatPropers(rows, S.seats({slots: []}, []), isPlaceholder),
    /unsupported foreign-source Proper applicability/);
  assert.equal(JSON.stringify(rows), before);
});
test('CLI cannot add, remove or alter foreign applicability metadata even on an inactive row', () => {
  const structure = foreignFixture(); const req = foreignRequest('day');
  const d = {...derived(), calendar: foreignEdition};
  for (const alter of [
    (p) => { delete p.appointment_applicability; },
    (p) => { p.appointment_applicability.basis = 'Different source basis'; }
  ]) {
    const payload = payloadFor(structure, req); payload.days[0].calendar = foreignEdition;
    alter(payload.days[0].masses[0].propers[0]);
    assert.throws(() => A.adaptCli({request: req, derived: d, structure, payload}), /applicability metadata disagrees/);
  }
  const regular = fixture(); const regularReq = request('day');
  for (const marker of [null, foreignFixture().masses[0].propers[0].appointment_applicability]) {
    const payload = payloadFor(regular, regularReq);
    payload.days[0].masses[0].propers[3].appointment_applicability = copy(marker);
    assert.throws(() => A.adaptCli({request: regularReq, derived: derived(), structure: regular, payload}),
      /applicability metadata disagrees/);
  }
});
test('pure legacy four-field alternatives remain exclusive unmarked source choices', () => {
  const rows = ['Gospel', 'Gospel (vel)'].map((name, index) => ({...sourceRow(name),
    ordinary_disposition: {kind: 'alternative', group: 'legacy-gospel', option: index ? 'second' : 'first',
      basis: 'Synthetic retained legacy source choice.'}}));
  const before = JSON.stringify(rows);
  const prepared = S.prepareProperAppointments(rows, {calendar: foreignEdition, entrance: 'propers'});
  const events = S.unframedEvents(prepared.rows, null, prepared.selections);
  assert.equal(events[0].kind, 'proper_choice'); assert.equal(events[0].options.length, 2);
  assert.equal(events[0].selection.state, 'required'); assert.equal(JSON.stringify(rows), before);
});
test('foreign new applicability stays blocked beside diagnostic legacy fields and terminal references', () => {
  const marker = foreignFixture().masses[0].propers[0].appointment_applicability;
  const rows = ['Gospel', 'Gospel (vel)'].map((name, index) => ({...sourceRow(name),
    taken_from: {mass: 'contract-terminal-wording', form: '', proper: 'Gospel'},
    appointment_applicability: copy(marker),
    ordinary_disposition: {kind: 'alternative', group: 'diagnostic-legacy-gospel',
      option: index ? 'second' : 'first', basis: 'Synthetic retained foreign diagnostic group.'}}));
  const before = JSON.stringify(rows);
  assert.throws(() => S.prepareProperAppointments(rows, {calendar: foreignEdition, entrance: 'propers',
    choices: {'main/diagnostic-legacy-gospel': 'second'}}), /from roman-1962 in roman-pre-1955/);
  assert.throws(() => S.unframedEvents(rows), /unsupported foreign-source Proper applicability/);
  assert.equal(JSON.stringify(rows), before);
  assert.equal(rows[0].taken_from.mass, 'contract-terminal-wording');
  assert.equal(rows[0].appointment_applicability.source_edition, edition);
});
test('explicit anchored reading seat qualifies only its source choice and never relabels known roles', () => {
  const principal = coordinate('Lesson');
  function readingRows(names = ['Lesson', 'Epistle (additional reading)']) {
    return names.map((name, index) => ({...sourceRow(name), appointment_identity: coordinate(name),
      ordinary_disposition: {kind: 'alternative', group: 'source-first-reading', option: index ? 'additional' : 'principal',
        basis: 'Synthetic source-owned first reading qualification.', anchor: copy(principal), seat: 'reading-1'}}));
  }
  const rows = readingRows(); const before = JSON.stringify(rows);
  assert.equal(S.semanticProperId(rows[0], true), null);
  const prepared = S.prepareProperAppointments(rows, {calendar: edition, entrance: 'propers'});
  assert.equal(S.unframedEvents(prepared.rows, null, prepared.selections)[0].kind, 'proper_choice');
  const result = A.adaptPropers({request: request(), structure: {calendar: edition,
    masses: [{key: massKey, kind: 'common', propers: rows}]}});
  assert(result.events[0].options.every((option) => option.events[0].semanticSlot.identity.id === 'reading-1'));
  const shown = [{element: {key: 'reading-anchor'}}];
  const seats = S.seats({slots: [{key: 'epistle', anchor: 'reading-anchor', where: 'after',
    propers: ['Lesson', 'Epistle'], qualified: true}]}, shown);
  assert.equal(S.seatPropers(prepared.rows, seats, null, prepared.selections).broke, false);
  assert.equal(JSON.stringify(rows), before); assert.equal(S.semanticProperId(rows[0], true), null);
  for (const mutation of [
    (r) => { delete r[0].ordinary_disposition.seat; },
    (r) => { r[1].ordinary_disposition.seat = 'gospel'; },
    (r) => { delete r[0].ordinary_disposition.anchor; },
    (r) => { r[1].name = 'Gospel'; },
    (r) => { r[1].name = 'Gradual'; }
  ]) {
    const changed = readingRows(); mutation(changed);
    assert.throws(() => { const appointed = S.prepareProperAppointments(changed, {calendar: edition, entrance: 'propers'});
      S.unframedEvents(appointed.rows, null, appointed.selections); }, /anchored|seat|source basis/);
  }
  const unqualified = readingRows(); unqualified.forEach((row) => { delete row.ordinary_disposition.seat; });
  const appointed = S.prepareProperAppointments(unqualified, {calendar: edition, entrance: 'propers'});
  assert.throws(() => S.unframedEvents(appointed.rows, null, appointed.selections), /one established semantic seat/);
});
test('unprepared conditional rows refuse instead of becoming cumulatively appointed', () => {
  assert.throws(() => S.unframedEvents(fixture().masses[0].propers), /must be prepared/);
});
test('framed seating conserves alternatives and uses the source principal anchor', () => {
  const prepared = prepare(fixture(), {entrance: 'day', date: '2026-04-15', season: 'paschaltide'});
  const slots = ['Introit', 'Collect', 'Epistle', 'Gradual', 'Alleluia', 'Gospel', 'Offertory', 'Secret', 'Communion', 'Postcommunion'];
  const file = {slots: slots.map((name) => ({key: name, anchor: name, where: 'after', propers: name === 'Alleluia' ? ['Alleluia', 'Tract'] : [name], qualified: true}))};
  const shown = slots.map((name) => ({element: {key: name}}));
  const placed = S.seatPropers(prepared.rows, S.seats(file, shown), null, prepared.selections);
  assert.equal(placed.broke, false);
  const events = S.massEvents(shown, placed);
  assert.equal(events.find((e) => e.group === 'gospel-reading').sourceIndex, 8);
  assert.equal(events.find((e) => e.group === 'common-acclamation').selection.option, 'paschal');
});
test('unknown exact selection targets and option ids refuse', () => {
  for (const choices of [
    {[choiceId('unknown')]: 'regular'}, {[choiceId('common-acclamation')]: 'unknown'},
    {[choiceId('common-acclamation').replace(edition, 'postconciliar')]: 'regular'},
    {[choiceId('common-acclamation').replace('/main/', '/other/')]: 'regular'}
  ]) { const req = request(); req.properChoices = choices; assert.throws(() => A.adaptPropers({request: req, structure: fixture()}), /not held|another edition/); }
});
test('derived replacements retain their own appointment and terminal wording with the original semantic seat', () => {
  const structure = fixture();
  const local = sourceRow('Alleluia');
  local.appointment_identity = {mass: massKey, form_id: 'main', proper: 'Alleluia', occurrence: 1};
  local.appointment_replacement = {source_group: {mass: owner, form_id: 'main', id: 'common-acclamation'},
    anchor: copy(anchor), basis: 'Synthetic exact source override.'};
  local.taken_from = {mass: 'contract-terminal-owner', form: '', proper: 'Alleluia'};
  structure.masses[0].propers = [local];
  const original = JSON.stringify(structure);
  const result = A.adaptPropers({request: request(), structure});
  assert.equal(result.events[0].semanticSlot.identity.id, 'gospel-acclamation');
  assert.equal(prepare(structure).rows.length, 1);
  assert.equal(JSON.stringify(structure), original);
  for (const mutate of [
    (p) => { p.name = 'Secret'; },
    (p) => { p.appointment_replacement.anchor.proper = 'Unmapped source text'; },
    (p) => { p.appointment_replacement.source_group.mass = 'wrong-owner'; },
    (p) => { p.appointment_replacement.inferred = true; }
  ]) {
    const altered = copy(structure); mutate(altered.masses[0].propers[0]);
    assert.throws(() => A.adaptPropers({request: request(), structure: altered}), /replacement|semantic seat/);
    assert.throws(() => prepare(altered), /replacement|semantic seat/);
  }
});
test('reader state validates exact multi-choice maps and rejects malformed maps', () => {
  const req = request(); req.properChoices = {[choiceId('common-acclamation')]: 'regular'};
  assert.equal(C.validateReaderState(req).ok, true);
  for (const value of [{}, [], null, {unknown: 'regular'}, {[choiceId('common-acclamation')]: undefined}, {[choiceId('common-acclamation')]: {id: 'regular'}}]) {
    req.properChoices = value; assert.equal(C.validateReaderState(req).ok, false);
  }
});
test('canonical Day and Propers URLs round-trip sorted multiple choices', () => {
  for (const entrance of ['day', 'propers']) {
    const req = request(entrance); req.properChoices = {[choiceId('gospel-reading')]: 'additional', [choiceId('common-acclamation')]: 'paschal'};
    const context = {missals: {[edition]: {calendar: edition, types: {common: [massKey]}, formsByMass: {[massKey]: []}, orationLanguages: ['la'], ordinaryLanguages: [], variantGroups: {}}},
      bibles: {'douay-rheims': {numbering: 'vulgate'}}, dayReadableFormularies: [{id: massKey}]};
    const hash = C.serializeLegacy({ok: true, state: req, legacy: {variants: {}, unknown: [], inert: []}});
    const normalized = C.normalizeLegacy(C.parseLegacy(entrance, hash), {context});
    assert.equal(normalized.ok, true, JSON.stringify(normalized.errors));
    assert.deepEqual(normalized.state.properChoices, req.properChoices);
    assert.equal(C.serializeLegacy(normalized), hash);
    const bad = C.normalizeLegacy(C.parseLegacy(entrance, hash.replace(/proper-choices=[^&]*/, 'proper-choices=not-json')), {context});
    assert.equal(bad.ok, false);
  }
});
test('CLI adapter and Day use identical original source indexes and source applicability', () => {
  const structure = fixture(); const req = request('day');
  req.properChoices = {[choiceId('gospel-reading')]: 'additional'};
  const d = derived(); const mass = structure.masses[0];
  const payload = {date: req.civilDate, scripture: {id: req.bible.id}, days: [{
    calendar: edition, selected_territory: null, settled: true, why: {lectionary: null},
    masses: [{key: massKey, standing: 'said', bible: {id: req.bible.id}, selected_form: 'main',
      proper_appointment_facts: copy(structure.proper_appointment_facts),
      propers: mass.propers.map((proper) => ({...copy(proper), form: '', verses: []}))}]
  }]};
  const day = A.adaptDay({request: req, derived: d, structure});
  const cli = A.adaptCli({request: req, derived: d, structure, payload});
  assert.deepEqual(cli.events, day.events); assert.deepEqual(cli.coverage, day.coverage);
  payload.days[0].masses[0].propers[4].appointment_identity.mass = 'wrong-owner';
  assert.throws(() => A.adaptCli({request: req, derived: d, structure, payload}), /order disagrees/);
});
test('CLI cannot supply a different source predicate map', () => {
  const structure = fixture(); const req = request('day');
  const payload = {date: req.civilDate, scripture: {id: req.bible.id}, days: [{calendar: edition,
    selected_territory: null, settled: true, why: {lectionary: null}, masses: [{
      key: massKey, standing: 'said', bible: {id: req.bible.id}, selected_form: 'main',
      propers: structure.masses[0].propers.map((proper) => ({...copy(proper), verses: []})),
      proper_appointment_facts: copy(facts)}]}]};
  payload.days[0].masses[0].proper_appointment_facts[factId].season_values.paschaltide = 'regular';
  assert.throws(() => A.adaptCli({request: req, derived: derived(), structure, payload}), /appointment facts disagree/);
});

process.stdout.write(JSON.stringify({status: 'pass', groups: results.length, checks: results}, null, 2) + '\n');
