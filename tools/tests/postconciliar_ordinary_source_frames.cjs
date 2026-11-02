/* Production-code semantic/native-DOM checks over a freshly compiled Ordinary.
 * Calendar branch facts below are explicit test inputs, not observance claims.
 * This probe makes no Chromium or visual-layout acceptance claim.
 */
'use strict';

const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');

const [root, payloadPath, mode] = process.argv.slice(2);
const ordinary = JSON.parse(fs.readFileSync(payloadPath, 'utf8'));
const A = require(path.join(root, 'src/web/browser/liturgy/reader-state-adapters.js'));
const C = require(path.join(root, 'src/web/browser/liturgy/reader-state.js'));
const S = require(path.join(root, 'src/web/browser/liturgy/ordinary-seating.js'));
const dom = require(path.join(root, 'scripts/lectern/dom.js'));
const structure = JSON.parse(fs.readFileSync(path.join(root,
  'src/web/data/structure/propers/postconciliar.json'), 'utf8'));
const mass = structure.masses.find(row => row.key === 'most-holy-name-jesus');
assert(mass, 'the real source-held Mass used for seating must exist');
const form = mass.forms ? mass.forms.find(row => row.id === 'main') ||
  (mass.forms.length === 1 ? mass.forms[0] : null) : {id: 'main', propers: mass.propers};
assert(form, 'select one real Mass form without combining formularies');

const elements = new Map(ordinary.sections.flatMap(section =>
  section.elements.map(element => [element.key, element])));
const initial = key => 'ritus-initiales/' + key;
const communion = key => 'ritus-communionis/' + key;
const greetingIds = [
  'greeting-trinitarian', 'greeting-grace-peace', 'greeting-lord', 'greeting-bishop'
];
const greetingKeys = greetingIds.map(initial);
const bishopKey = initial('greeting-bishop');
const parents = [initial('introitus'), initial('salutatio'), communion('ecce-agnus-dei')];
const translation = (key, language) => {
  const element = elements.get(key);
  assert(element, key);
  const held = (element.translations || []).filter(row => row.lang === language);
  assert.equal(held.length, 1, key + ' has one source body in ' + language);
  return held[0];
};

globalThis.window = globalThis;
globalThis.document = dom.document;
globalThis.location = {search: '', hash: '', pathname: '/'};
globalThis.history = {replaceState() {}, pushState() {}};
globalThis.addEventListener = () => {};
vm.runInThisContext(fs.readFileSync(path.join(root,
  'src/web/browser/shared/browser-core.js'), 'utf8'));
globalThis.OrdinarySeating = S;
globalThis.LiturgyReaderStateAdapters = A;
vm.runInThisContext(fs.readFileSync(path.join(root,
  'src/web/browser/liturgy/day.js'), 'utf8'));
const R = TriptychOrdinaryRenderer;

function request(option, language, date, choices = {}) {
  const held = {
    schema: C.STATE_SCHEMA, entrance: 'day', civilDate: date,
    edition: {id: 'postconciliar'}, calendar: {id: 'postconciliar'},
    selectedReadableFormulary: {id: mass.key},
    bible: {id: 'vulgata-clementina', numbering: 'vulgate'},
    languages: {orations: 'la', ordinary: language}, requestedMode: 'missal',
    options: {ordinary: true, legitimate: Object.assign({}, choices,
      option ? {'salutatio-form': option} : {})},
    coverage: [], unresolvedChoices: [], sourceHooks: []
  };
  if (mass.forms) held.form = form.id;
  assert.equal(C.validateReaderState(held).ok, true);
  return held;
}

function adapt(option, language, date = '2027-01-06', nature = 'solemnity', choices = {}) {
  return A.adaptDay({
    request: request(option, language, date, choices), ordinary, structure,
    derived: {
      date, calendar: 'postconciliar', weekday: 'wednesday', season: 'nativity',
      liturgicalYear: {lectionary: {sunday: 'A', weekday: 'I'}},
      options: [{option: null, winner: {id: mass.key, nature}, settled: true,
        readable: [{key: mass.key, state: 'said'}], absent: []}]
    }
  });
}

function ordinaryEvent(events, key) {
  const found = events.filter(event => event.id === 'ordinary-element/' + key);
  assert.equal(found.length, 1, key + ' is one semantic event');
  return found[0];
}

function greetingEvents(events) {
  return events.filter(event => greetingKeys.some(key =>
    event.id === 'ordinary-element/' + key));
}

function render(option, language, display, choices = {}) {
  R.configure({ordinaryLang: language, textDisplay: display, why: false,
    variants: Object.assign({}, choices, option ? {'salutatio-form': option} : {})});
  return R.renderFrame(ordinary, form.propers, proper => {
    const node = document.createElement('p');
    node.textContent = proper.name;
    node.setAttribute('data-source-frame-test', proper.name);
    return node;
  }, (event, node) => {
    const key = event.kind === 'ordinary_element' ? event.element.key :
      event.kind === 'proper' ? event.proper.name : event.section.key;
    node.setAttribute('data-source-frame-test', key);
  }, {calendar: 'postconciliar', formulary: mass.key});
}

function nodes(frame, key) {
  // The repository native DOM supports attribute-presence selectors, not CSS
  // attribute-value selectors. Compare the actual value separately.
  return frame.querySelectorAll('[data-source-frame-test]').filter(node =>
    node.getAttribute('data-source-frame-test') === key);
}

function oneNode(frame, key) {
  const found = nodes(frame, key);
  assert.equal(found.length, 1, key + ' renders once');
  return found[0];
}

function sourceSides(node, language, display) {
  if (display === 'latin-and-selected' && language !== 'la') {
    const sides = node.querySelectorAll('.text-side');
    assert.equal(sides.length, 2);
    return ['la', language].map(lang => ({lang, node: sides.find(side =>
      side.getAttribute('data-text-language') === lang)}));
  }
  return [{lang: language, node}];
}

function assertIncreasing(events, wanted) {
  const indexes = wanted.map(key => events.indexOf(ordinaryEvent(events, key)));
  assert.deepEqual(indexes, indexes.slice().sort((left, right) => left - right));
}

let cases = 0;
if (mode === 'source') {
  for (const key of parents) {
    const parent = elements.get(key);
    assert(parent, 'the published semantic parent is retained: ' + key);
    assert.equal(parent.kind, 'rubric');
    assert.equal(parent.translations, null, 'no fragment claims the whole parent');
    assert.deepEqual(parent.absent, {english: 'not-a-text', latin: 'not-a-text'});
    cases++;
  }
  for (const key of [initial('signum-crucis'), ...greetingKeys,
    initial('greeting-response'), communion('offerte-vobis-pacem')]) {
    assert.equal(elements.get(key).kind, 'dialogue', key + ' is not a sacramental form');
    cases++;
  }
  const roles = new Map([
    [initial('signum-crucis'), ['priest', 'all']],
    ...greetingKeys.map(key => [key, [key === bishopKey ? 'bishop' : 'priest']]),
    [initial('greeting-response'), ['all']],
    [communion('ecce-agnus'), ['priest']],
    [communion('beati-ad-cenam'), ['priest']],
    [communion('domine-non-sum-dignus'), ['all']]
  ]);
  for (const [key, speakers] of roles) for (const lang of ['en', 'la']) {
    const held = translation(key, lang);
    assert.deepEqual(held.turns.map(turn => turn.speaker), speakers, key + ':' + lang);
    assert(held.turns.every(turn => turn.dialogue_role === null));
    assert.equal(held.reading_note.trim().length > 0, true, key + ' has default qualification');
    assert(!Object.hasOwn(held, 'target_wording'), 'no authenticated2008 identity is invented');
    if (lang === 'la') {
      assert.equal(held.relation, 'antecedent');
      assert.equal(held.collation, 'uncollated');
    }
    cases++;
  }
  const group = ordinary.variants.find(row => row.group === 'salutatio-form');
  assert.deepEqual(group.options.map(row => [row.id, row.default]),
    greetingIds.map((id, index) => [id, index === 0]));
  assert(group.options[3].name.startsWith('Bishop only'));
  assert.equal(elements.get(bishopKey).speaker, 'bishop');
  for (const lang of ['en', 'la']) {
    assert.match(translation(bishopKey, lang).reading_note, /John 20:19/);
    assert.match(translation(bishopKey, lang).reading_note, /Bishop-only/);
    assert.match(translation(communion('beati-ad-cenam'), lang).reading_note, /omit/i);
    assert.match(translation(communion('beati-ad-cenam'), lang).reading_note,
      /nuptiarum|of the wedding/);
    cases++;
  }
} else if (mode === 'selection') {
  for (const language of ['en', 'la']) for (const option of [null, ...greetingIds]) {
    const events = adapt(option, language).events;
    const expected = option || greetingIds[0];
    const selected = greetingEvents(events);
    assert.equal(selected.length, 1);
    assert.equal(selected[0].id, 'ordinary-element/' + initial(expected));
    assert.equal(selected[0].selected.availability, 'held');
    assert.equal(selected[0].selected.text, translation(initial(expected), language).text);
    assert.equal(selected[0].speaker, expected === 'greeting-bishop' ? 'bishop' : 'priest');
    ordinaryEvent(events, initial('greeting-response'));
    assert.equal(events.some(event => event.id === 'ordinary-element/' + bishopKey),
      option === 'greeting-bishop');
    cases++;
  }
  for (const date of ['2027-01-06', '2027-08-15']) {
    for (const nature of ['solemnity', 'weekday']) {
      assert(!greetingEvents(adapt(null, 'en', date, nature).events).some(event =>
        event.id === 'ordinary-element/' + bishopKey));
      assert.equal(greetingEvents(adapt('greeting-bishop', 'en', date, nature).events)[0].id,
        'ordinary-element/' + bishopKey);
      cases++;
    }
  }
  assert.throws(() => adapt('not-a-held-greeting', 'en'), /explicit Ordinary option is not held/);
} else if (mode === 'rendering') {
  for (const language of ['en', 'la']) for (const option of [null, ...greetingIds]) {
    for (const display of ['selected', 'latin-and-selected']) {
      const frame = render(option, language, display);
      const expected = initial(option || greetingIds[0]);
      assert.equal(greetingKeys.flatMap(key => nodes(frame, key)).length, 1);
      oneNode(frame, initial('greeting-response'));
      for (const key of [initial('signum-crucis'), expected, initial('greeting-response'),
        communion('ecce-agnus'), communion('beati-ad-cenam'), communion('domine-non-sum-dignus')]) {
        for (const side of sourceSides(oneNode(frame, key), language, display)) {
          assert(side.node, key + ':' + side.lang);
          const held = translation(key, side.lang);
          const notes = side.node.querySelectorAll('.ordinary-reading-note');
          assert.equal(notes.length, 1);
          assert.equal(notes[0].textContent, held.reading_note);
          assert.equal(notes[0].hasAttribute('hidden'), false);
          const source = side.node.querySelectorAll('.ordinary-reading-source');
          assert.equal(source.length, 1);
          const witness = ordinary.translations.find(row =>
            row.source_id === held.source_id && row.lang === side.lang);
          assert(witness);
          assert.equal(source[0].textContent, 'Source: ' + witness.label);
          const spoken = side.node.querySelectorAll('.ordinary-turn-text');
          assert.equal(spoken.length, held.turns.length);
          assert(spoken.every(span => !span.textContent.includes(held.reading_note)));
          assert.equal(side.node.querySelectorAll('details').length, 0,
            'source qualifications are not hidden in Study');
          if (key === communion('beati-ad-cenam') && side.lang === 'la') {
            assert.match(source[0].textContent, /Clementine Vulgate \(eBible latVUC\)/);
          }
        }
      }
      const sign = oneNode(frame, initial('signum-crucis'));
      for (const side of sourceSides(sign, language, display)) {
        assert.deepEqual(side.node.querySelectorAll('.ordinary-turn').map(turn =>
          turn.getAttribute('data-speaker')), ['priest', 'all']);
      }
      if (option === 'greeting-bishop') {
        for (const side of sourceSides(oneNode(frame, bishopKey), language, display)) {
          const turns = side.node.querySelectorAll('.ordinary-turn');
          assert.equal(turns.length, 1);
          assert.equal(turns[0].getAttribute('data-speaker'), 'bishop');
          const cue = side.node.querySelector('.ordinary-turn-cue');
          assert.equal(cue.querySelector('.visually-hidden').textContent, 'Bishop');
          const mark = cue.querySelector('.cue-mark');
          assert.equal(mark.getAttribute('data-cue'), 'B');
          assert.equal(mark.getAttribute('aria-hidden'), 'true');
          assert.equal(mark.hasAttribute('data-dialogue-mark'), false);
          if (side.lang === 'en') assert.match(side.node.textContent,
            /not approved for liturgical use or recitation\./);
        }
      } else assert.equal(nodes(frame, bishopKey).length, 0);
      cases++;
    }
  }
} else if (mode === 'conditions') {
  const kyrie = elements.get(initial('kyrie'));
  assert(kyrie.conditions.some(condition => condition.kind === 'omit-when-option' &&
    condition.group === 'penitential-act' && condition.options.includes('pa-iii') &&
    condition.basis.trim()));
  const english = translation(initial('kyrie'), 'en');
  assert.equal(english.turns.length, 6, 'the new study arrangement is sixfold, not ninefold');
  assert.deepEqual(english.turns.map(turn => turn.dialogue_role),
    ['versicle', 'response', 'versicle', 'response', 'versicle', 'response']);
  assert.match(english.reading_note, /sixfold/i);
  assert.match(english.reading_note, /not a verbatim.*1861|not.*approved/i);
  for (const language of ['en', 'la']) for (const option of ['pa-i', 'pa-ii', 'pa-iii']) {
    const choices = {'penitential-act': option};
    const events = adapt(null, language, '2027-01-06', 'solemnity', choices).events;
    const selected = events.filter(event => event.id === 'ordinary-element/' + initial('kyrie'));
    assert.equal(selected.length, option === 'pa-iii' ? 0 : 1);
    if (selected.length) {
      const held = (kyrie.translations || []).find(row => row.lang === language);
      assert.equal(selected[0].selected.text, held ? held.text : null,
        'an absent language never falls back to the held English');
    }
    for (const display of ['selected', 'latin-and-selected']) {
      const frame = render(null, language, display, choices);
      assert.equal(nodes(frame, initial('kyrie')).length, option === 'pa-iii' ? 0 : 1);
    }
    cases++;
  }
} else if (mode === 'order') {
  for (const language of ['en', 'la']) for (const option of [null, ...greetingIds]) {
    const events = adapt(option, language).events;
    const chosen = initial(option || greetingIds[0]);
    assertIncreasing(events, [initial('introitus'), initial('signum-crucis'),
      initial('salutatio'), chosen, initial('greeting-response')]);
    assertIncreasing(events, [communion('ecce-agnus-dei'), communion('ecce-agnus'),
      communion('beati-ad-cenam'), communion('domine-non-sum-dignus'), communion('communio')]);
    const entrance = events.find(event => event.kind === 'proper' &&
      event.editionSlotLabel === 'Entrance Antiphon');
    const communionAntiphon = events.find(event => event.kind === 'proper' &&
      event.editionSlotLabel === 'Communion Antiphon');
    assert(entrance && communionAntiphon, 'the real Mass supplies both proper seating controls');
    assert(events.indexOf(ordinaryEvent(events, initial('introitus'))) < events.indexOf(entrance));
    assert(events.indexOf(entrance) < events.indexOf(ordinaryEvent(events, initial('signum-crucis'))));
    assert(events.indexOf(ordinaryEvent(events, communion('communio'))) < events.indexOf(communionAntiphon));
    for (const key of parents) {
      const event = ordinaryEvent(events, key);
      assert.equal(event.action, true);
      assert.equal(event.selected.text, null);
      assert.equal(event.selected.absenceKey, 'not-a-text');
    }
    const frame = render(option, language, 'selected');
    const rendered = frame.querySelectorAll('[data-source-frame-test]');
    const index = key => rendered.indexOf(oneNode(frame, key));
    assert(index('Entrance Antiphon') < index(initial('signum-crucis')));
    const communionOrder = [communion('ecce-agnus-dei'), communion('ecce-agnus'),
      communion('beati-ad-cenam'), communion('domine-non-sum-dignus'), communion('communio')];
    const indexes = communionOrder.map(index);
    assert.deepEqual(indexes, indexes.slice().sort((left, right) => left - right));
    cases++;
  }
} else throw new Error('unknown source-frame probe mode: ' + mode);

console.log(JSON.stringify({mode, cases}));
