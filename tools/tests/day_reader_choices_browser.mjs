#!/usr/bin/env node

/* Focused real-browser contract for first-class Day and Proper-form choices. */

import assert from 'node:assert/strict';
import { spawn } from 'node:child_process';
import { createServer } from 'node:http';
import { access, mkdir, mkdtemp, readFile, rm } from 'node:fs/promises';
import { extname, join, resolve, sep } from 'node:path';
import process from 'node:process';

const ROOT = resolve(import.meta.dirname, '../..');
const ROUTE = '/src/web/browser/liturgy/day.html';
const DATA = '/build/public-alpha/preview/browse';
const chromeBinary = process.env.TRIPTYCH_CHROME || '/usr/bin/chromium';

function mime(path) {
  return ({
    '.css': 'text/css; charset=utf-8', '.html': 'text/html; charset=utf-8',
    '.js': 'text/javascript; charset=utf-8', '.json': 'application/json'
  })[extname(path)] || 'application/octet-stream';
}

async function listen(server) {
  await new Promise((accept, reject) => {
    server.once('error', reject);
    server.listen(0, '127.0.0.1', accept);
  });
  return server.address().port;
}

async function exists(path) {
  try { await access(path); return true; } catch (_error) { return false; }
}

function withAuthoredForms(payload) {
  const structure = JSON.parse(payload);
  const mass = (structure.masses || []).find((row) => row.key === 'advent-1');
  if (!mass || mass.propers.length < 4) throw new Error('advent-1 fixture Mass is absent');
  const boundary = Math.floor(mass.propers.length / 2);
  const forms = [
    { id: 'night', name: 'At Night', ordinal: 1, propers: mass.propers.slice(0, boundary) },
    { id: 'day', name: 'During the Day', ordinal: 2, propers: mass.propers.slice(boundary) }
  ];
  forms.forEach((form) => form.propers.forEach((proper) => { proper.form_id = form.id; }));
  mass.forms = forms;
  return JSON.stringify(structure);
}

function withMultipleOrdinaryGroups(payload) {
  const structure = JSON.parse(payload);
  const groups = [
    ['reader-fixture-option', 'Focused reader option'],
    ['reader-fixture-second-option', 'Second focused reader option']
  ].map(([id, name]) => ({
    group: id, name,
    what: 'Synthetic browser-only proof that independent Ordinary choices remain exclusive.',
    options: [
      { id: id + '-a', name: 'Fixture A', default: true },
      { id: id + '-b', name: 'Fixture B', default: false }
    ]
  }));
  structure.variants = [...(structure.variants || []), ...groups];
  const anchors = new Set((structure.slots || []).map((slot) => slot.anchor));
  groups.forEach((group) => {
    const candidates = [];
    (structure.sections || []).forEach((section) => {
      (section.elements || []).forEach((element) => {
        if (!anchors.has(element.key) && !element.variant &&
            !(element.alternatives || []).length && !(element.conditions || []).length) {
          candidates.push(element);
        }
      });
    });
    if (candidates.length < 2) {
      throw new Error('ordinary fixture needs two unconditional non-anchor elements');
    }
    const first = candidates[0];
    const second = candidates[1];
    first.key += '-' + group.group + '-a';
    first.alternatives = [{ group: group.group, option: group.group + '-a' }];
    second.key += '-' + group.group + '-b';
    second.name = (second.name || second.key) + ' — Fixture B';
    second.alternatives = [{ group: group.group, option: group.group + '-b' }];
  });
  return JSON.stringify(structure);
}

function withMultipleOrdinaryIndexGroups(payload) {
  const index = JSON.parse(payload);
  const row = (index.calendars || []).find((entry) => entry.calendar === 'roman-1962');
  if (!row) throw new Error('Roman 1962 Ordinary index row is absent');
  row.variants = [...(row.variants || []),
    'reader-fixture-option', 'reader-fixture-second-option'];
  return JSON.stringify(index);
}

function withAuthorizedCalendarChoices(payload) {
  return payload + `
;(function (root) {
  const held = root.MassAssembly;
  const choices = {
    '2026-08-07': [
      ['saints-sixtus-ii-pope-companions-martyrs', 'Saints Sixtus II and Companions'],
      ['saint-cajetan-priest', 'Saint Cajetan'],
      ['ot-18-friday', 'Friday of the Eighteenth Week in Ordinary Time']
    ],
    '2027-06-05': [
      ['immaculate-heart-blessed-virgin-mary', 'The Immaculate Heart of Mary'],
      ['saint-boniface-bishop-martyr', 'Saint Boniface'],
      ['ot-9-saturday', 'Saturday of the Ninth Week in Ordinary Time']
    ]
  };
  root.MassAssembly = Object.freeze(Object.assign({}, held, {
    derive(input) {
      const result = held.derive(input);
      const rows = choices[result.date];
      if (!rows) return result;
      const branch = result.options[0];
      const locus = 'focused authorized-choice fixture';
      return Object.assign({}, result, {options: [Object.assign({}, branch, {
        winner: null, settled: true, unsettled: [],
        choice: {
          id: 'calendar-formulary', required: true, locus,
          what: 'the calendar source authorizes these coequal formularies',
          among: rows.map(([key, name]) => ({id: key, key, candidateId: key, name}))
        },
        readable: rows.map(([key, label]) => ({
          id: key, key, label, state: 'option', choice: 'calendar-formulary',
          locus, why: 'explicit choice required'
        }))
      })]});
    }
  }));
}(globalThis));
`;
}

function staticServer() {
  return createServer(async (request, response) => {
    try {
      const url = new URL(request.url, 'http://127.0.0.1');
      let relative = decodeURIComponent(url.pathname).replace(/^\/+/, '');
      if (relative === 'favicon.ico') {
        response.writeHead(204, { 'cache-control': 'no-store' });
        response.end();
        return;
      }
      const builtData = 'build/public-alpha/preview/browse/';
      if (relative.startsWith(builtData)) {
        const sourceRelative = 'src/web/data/' + relative.slice(builtData.length);
        if (await exists(resolve(ROOT, sourceRelative))) relative = sourceRelative;
      }
      const file = resolve(ROOT, relative || 'README.md');
      if (file !== ROOT && !file.startsWith(ROOT + sep)) throw new Error('outside root');
      let body = await readFile(file);
      if (relative === 'src/web/browser/liturgy/assembly-model.js') {
        body = Buffer.from(withAuthorizedCalendarChoices(body.toString('utf8')));
      }
      if (relative === 'src/web/data/structure/propers/postconciliar.json') {
        body = Buffer.from(withAuthoredForms(body.toString('utf8')));
      }
      if (relative === 'src/web/data/structure/ordinary/index.json') {
        body = Buffer.from(withMultipleOrdinaryIndexGroups(body.toString('utf8')));
      }
      if (relative === 'src/web/data/structure/ordinary/roman-1962.json') {
        body = Buffer.from(withMultipleOrdinaryGroups(body.toString('utf8')));
      }
      response.writeHead(200, {
        'content-type': mime(file), 'cache-control': 'no-store',
        'x-robots-tag': 'noindex, nofollow'
      });
      response.end(body);
    } catch (_error) {
      response.writeHead(404, { 'content-type': 'text/plain; charset=utf-8' });
      response.end('not found');
    }
  });
}

async function freePort() {
  const server = createServer();
  const port = await listen(server);
  await new Promise((accept) => server.close(accept));
  return port;
}

async function waitForJson(url) {
  for (let attempt = 0; attempt < 160; attempt += 1) {
    try {
      const response = await fetch(url);
      if (response.ok) return await response.json();
    } catch (_error) { /* Chromium is starting. */ }
    await new Promise((accept) => setTimeout(accept, 50));
  }
  throw new Error('Chromium debugging endpoint did not start');
}

class CDP {
  constructor(url) {
    this.socket = new WebSocket(url);
    this.next = 0;
    this.pending = new Map();
  }
  async ready() {
    await new Promise((accept, reject) => {
      this.socket.addEventListener('open', accept, { once: true });
      this.socket.addEventListener('error', reject, { once: true });
    });
    this.socket.addEventListener('message', (event) => {
      const message = JSON.parse(event.data);
      if (!message.id || !this.pending.has(message.id)) return;
      const pending = this.pending.get(message.id);
      this.pending.delete(message.id);
      if (message.error) pending.reject(new Error(message.error.message));
      else pending.accept(message.result);
    });
  }
  send(method, params = {}) {
    const id = ++this.next;
    return new Promise((accept, reject) => {
      this.pending.set(id, { accept, reject });
      this.socket.send(JSON.stringify({ id, method, params }));
    });
  }
  close() { this.socket.close(); }
}

async function evaluate(cdp, expression) {
  const result = await cdp.send('Runtime.evaluate', {
    expression, awaitPromise: true, returnByValue: true, userGesture: true
  });
  if (result.exceptionDetails) {
    throw new Error(result.exceptionDetails.exception?.description || result.exceptionDetails.text);
  }
  return result.result.value;
}

async function waitFor(cdp, expression, label) {
  for (let attempt = 0; attempt < 240; attempt += 1) {
    try {
      if (await evaluate(cdp, `Boolean(${expression})`)) return;
    } catch (_error) { /* a top-level navigation replaced the execution context */ }
    await new Promise((accept) => setTimeout(accept, 50));
  }
  throw new Error('Timed out waiting for ' + label);
}

function state(rows) {
  return '#' + new URLSearchParams({
    date: rows.date, missal: 'postconciliar', bible: 'douay-rheims',
    orations: 'la', mode: 'read', why: '0', rubrics: '1', ...rows
  }).toString();
}

async function navigate(cdp, base, hash) {
  const target = `${base}${ROUTE}?data=${DATA}${hash}`;
  await evaluate(cdp, `location.href = ${JSON.stringify(target)}; true`);
  await waitFor(cdp,
    `window.dayReaderReady === true && dayReaderDebug.committedRender && ` +
      `dayReaderDebug.committedRender.href === location.href`,
    'committed Day navigation');
}

async function snapshot(cdp) {
  return evaluate(cdp, `(() => ({
    path: location.pathname, hash: location.hash,
    outcome: dayReaderDebug.outcome,
    eventCount: (dayReaderDebug.semantic && dayReaderDebug.semantic.events || []).length,
    resolved: dayReaderDebug.semantic && dayReaderDebug.semantic.resolved,
    error: dayReaderDebug.error,
    choice: document.querySelector('[data-unresolved-choice]')?.dataset.unresolvedChoice || null,
    options: [...document.querySelectorAll('[data-choice-option]')].map((row) => row.value),
    contents: [...document.querySelectorAll('[data-reader-contents] button')]
      .map((row) => row.textContent.trim()),
    fallbackUnits: document.querySelectorAll('.proper, [data-semantic-event-id]').length,
    formularyControlHidden: document.querySelector('#reader-formulary-field').hidden,
    witnessChoices: [...document.querySelectorAll('[data-translation-witness-choice]')]
      .map((row) => row.dataset.translationWitnessChoice),
    witnessOptions: [...document.querySelectorAll('[data-translation-witness]')]
      .map((row) => row.value),
    witnessLimitations: [...document.querySelectorAll('[data-translation-witness-limitation]')]
      .map((row) => row.textContent.trim()),
    semanticLocations: [...document.querySelectorAll('[data-semantic-location]')]
      .map((row) => row.dataset.semanticLocation),
    stateLocation: dayReaderDebug.state?.semanticLocation || null,
    englishComposed: document.querySelectorAll('.composed[lang="en"]').length,
    ordinaryLoads: Object.keys(dayReaderDebug.loads).filter((path) =>
      path.includes('structure/ordinary/') && !path.endsWith('/index.json')),
    ordinaryPresentations: dayReaderDebug.ordinaryPresentations,
    ordinaryOptionGroups: [...document.querySelectorAll('[data-option-group]')]
      .map((row) => row.dataset.optionGroup),
    ordinaryChecked: [...document.querySelectorAll('[data-option-group] input:checked')]
      .map((row) => row.closest('[data-option-group]').dataset.optionGroup + ':' + row.value),
    ordinaryUnresolved: (dayReaderDebug.semantic?.ordinaryUnresolved || [])
      .map((row) => row.element),
    metadata: document.querySelector('#celebration-meta').textContent,
    ordinaryOptionFieldHidden: document.querySelector('#reader-ordinary-option-field').hidden
  }))()`);
}

async function click(cdp, selector) {
  await evaluate(cdp, `(() => {
    const node = document.querySelector(${JSON.stringify(selector)});
    if (!node) throw new Error('missing selector');
    node.click(); return true;
  })()`);
}

async function testCalendarChoices(cdp, base) {
  const cases = [
    ['2026-08-07', [
      'saints-sixtus-ii-pope-companions-martyrs', 'saint-cajetan-priest', 'ot-18-friday'
    ]],
    ['2027-06-05', [
      'immaculate-heart-blessed-virgin-mary', 'saint-boniface-bishop-martyr',
      'ot-9-saturday'
    ]]
  ];
  for (const [date, options] of cases) {
    await navigate(cdp, base, state({ date }));
    const held = await snapshot(cdp);
    assert.equal(held.path, '/src/web/browser/liturgy/day.html');
    assert.equal(held.outcome, 'unresolved', JSON.stringify(held.error));
    assert.equal(held.eventCount, 0);
    assert.equal(held.choice, 'calendar-formulary');
    assert.deepEqual(held.options, options);
    assert.deepEqual(held.contents, ['Choose a formulary']);
    assert.equal(held.fallbackUnits, 0);
    assert.equal(held.formularyControlHidden, true);
  }

  await click(cdp, '[data-reader-action="contents"]');
  await click(cdp, '[data-reader-contents] button');
  assert.equal(await evaluate(cdp,
    `document.activeElement.dataset.unresolvedChoice`), 'calendar-formulary');
  await click(cdp, '[data-choice-option="ot-9-saturday"]');
  await click(cdp, '.candidate-choice-apply');
  await waitFor(cdp,
    `dayReaderReady && dayReaderDebug.outcome === 'ready' && ` +
      `dayReaderDebug.semantic.resolved.formulary === 'ot-9-saturday'`,
    'explicit calendar formulary');
  const selected = await snapshot(cdp);
  assert.equal(new URLSearchParams(selected.hash.slice(1)).get('mass'), 'ot-9-saturday');
  assert.ok(selected.eventCount > 0);
  assert.match(await evaluate(cdp, 'document.activeElement.dataset.semanticEventId || ""'), /^proper\//);
  const beforeBack = await evaluate(cdp, 'dayReaderDebug.renders');
  await evaluate(cdp, 'history.back(); true');
  await waitFor(cdp,
    `dayReaderReady && dayReaderDebug.renders > ${beforeBack} && ` +
      `dayReaderDebug.outcome === 'unresolved'`, 'calendar choice history restoration');
  assert.equal((await snapshot(cdp)).eventCount, 0);
}

async function testProperForms(cdp, base) {
  const baseState = state({ date: '2026-11-29', mass: 'advent-1' });
  await navigate(cdp, base, baseState);
  const held = await snapshot(cdp);
  assert.equal(held.outcome, 'unresolved');
  assert.equal(held.choice, 'proper-form:postconciliar/advent-1');
  assert.deepEqual(held.options, ['night', 'day']);
  assert.equal(held.options.includes('main'), false);
  assert.equal(held.eventCount, 0);
  assert.equal(held.fallbackUnits, 0);
  assert.deepEqual(held.contents, ['Choose a Mass form']);

  const ax = await cdp.send('Accessibility.getFullAXTree');
  const radioNames = ax.nodes.filter((node) => node.role?.value === 'radio')
    .map((node) => node.name?.value).filter(Boolean);
  assert.deepEqual(radioNames, ['At Night', 'During the Day']);
  assert.equal(await evaluate(cdp, 'document.querySelector(".candidate-choice-apply").disabled'), true);
  await click(cdp, '[data-choice-option="day"]');
  assert.equal(await evaluate(cdp, 'document.querySelector(".candidate-choice-apply").disabled'), false);
  await click(cdp, '.candidate-choice-apply');
  await waitFor(cdp,
    `dayReaderReady && dayReaderDebug.outcome === 'ready' && ` +
      `dayReaderDebug.semantic.resolved.form === 'day'`, 'explicit Proper form');
  const selected = await snapshot(cdp);
  const selectedParams = new URLSearchParams(selected.hash.slice(1));
  assert.equal(selectedParams.get('mass'), 'advent-1');
  assert.equal(selectedParams.get('form'), 'day');
  assert.ok(selected.eventCount > 0);

  await navigate(cdp, base, baseState + '&form=foreign');
  const invalid = await snapshot(cdp);
  assert.equal(invalid.outcome, 'invalid');
  assert.equal(invalid.eventCount, 0);
  assert.equal(invalid.fallbackUnits, 0);
}

async function testColdRead(cdp, base) {
  await navigate(cdp, base, state({ date: '2026-08-02', mass: 'ot-18' }));
  const defaults = await snapshot(cdp);
  assert.equal(defaults.outcome, 'unresolved');
  assert.ok(defaults.contents.includes('Source Proper choice: Communion Antiphon'));
  assert.equal(new URLSearchParams(defaults.hash.slice(1)).get('ordinary-lang'), null);

  await navigate(cdp, base, state({
    date: '2026-08-02', mass: 'ot-18', 'ordinary-lang': 'en',
    'eucharistic-prayer': 'ep-ii'
  }));
  const held = await snapshot(cdp);
  assert.equal(held.outcome, 'unresolved');
  assert.ok(held.contents.includes('Source Proper choice: Communion Antiphon'));
  assert.deepEqual(held.ordinaryLoads, ['structure/ordinary/postconciliar.json']);
  assert.equal(held.ordinaryPresentations, 0);
  const params = new URLSearchParams(held.hash.slice(1));
  assert.equal(params.get('mode'), 'read');
  assert.equal(params.get('ordinary-lang'), 'en');
  assert.equal(params.get('eucharistic-prayer'), 'ep-ii');

  await navigate(cdp, base, state({
    date: '2026-08-02', mass: 'ot-18', 'eucharistic-prayer': 'foreign'
  }));
  const invalidOption = await snapshot(cdp);
  assert.equal(invalidOption.outcome, 'invalid');
  assert.equal(invalidOption.eventCount, 0);
  assert.equal(invalidOption.error[0].path, 'eucharistic-prayer');

  await navigate(cdp, base, state({
    date: '2026-08-02', mass: 'ot-18', 'ordinary-lang': 'fr'
  }));
  const invalidLanguage = await snapshot(cdp);
  assert.equal(invalidLanguage.outcome, 'invalid');
  assert.equal(invalidLanguage.eventCount, 0);
  assert.equal(invalidLanguage.error[0].path, 'ordinary-lang');
}

async function testMultipleOrdinaryGroups(cdp, base) {
  await navigate(cdp, base, state({
    date: '2026-08-02', missal: 'roman-1962', mass: 'pentecost-10',
    mode: 'missal', 'ordinary-lang': 'en'
  }));
  const held = await snapshot(cdp);
  assert.equal(held.outcome, 'ready', JSON.stringify(held.error));
  assert.ok(held.ordinaryOptionGroups.includes('reader-fixture-option'));
  assert.ok(held.ordinaryOptionGroups.includes('reader-fixture-second-option'));

  await click(cdp, '[data-reader-action="date"]');
  assert.equal((await snapshot(cdp)).ordinaryOptionFieldHidden, true);
  await click(cdp, '[data-reader-action="date"]');

  await click(cdp,
    '[data-option-group="reader-fixture-option"] input[value="reader-fixture-option-b"]');
  await waitFor(cdp,
    `dayReaderReady && dayReaderDebug.outcome === 'ready' && ` +
      `dayReaderDebug.state.options.legitimate['reader-fixture-option'] === ` +
        `'reader-fixture-option-b'`,
    'second independent Ordinary option');
  const selected = await snapshot(cdp);
  assert.equal(new URLSearchParams(selected.hash.slice(1)).get('reader-fixture-option'),
    'reader-fixture-option-b');
  assert.ok(selected.semanticLocations.some((id) =>
    id.endsWith('-reader-fixture-option-b')));
  assert.ok(!selected.semanticLocations.some((id) =>
    id.endsWith('-reader-fixture-option-a')));
  assert.ok(selected.semanticLocations.some((id) =>
    id.endsWith('-reader-fixture-second-option-a')));
  assert.ok(!selected.semanticLocations.some((id) =>
    id.endsWith('-reader-fixture-second-option-b')));
  assert.equal(await evaluate(cdp,
    `document.activeElement.closest('[data-option-group]')?.dataset.optionGroup || ''`),
  'reader-fixture-option');
}

async function testConditionedOrdinaryGroups(cdp, base) {
  await navigate(cdp, base, state({
    date: '2026-11-29', mass: 'advent-1', form: 'night', mode: 'missal',
    'ordinary-lang': 'en', 'eucharistic-prayer': 'ep-iv'
  }));
  const held = await snapshot(cdp);
  assert.equal(held.outcome, 'unresolved', JSON.stringify(held.error));
  assert.deepEqual(held.ordinaryOptionGroups,
    ['penitential-act', 'creed', 'eucharistic-prayer']);
  assert.ok(held.ordinaryChecked.includes('eucharistic-prayer:ep-iv'));
  assert.deepEqual(held.ordinaryUnresolved, [
    'ritus-initiales/gloria-in-excelsis',
    'prex-eucharistica/prex-eucharistica-iv'
  ]);
  assert.ok(!held.semanticLocations.some((id) =>
    id.endsWith('ordinary-element/prex-eucharistica/prex-eucharistica-iv')));
  assert.match(held.metadata, /Eucharistic Prayer: IV \(applicability unresolved\)/);

  await click(cdp, '[data-option-group="eucharistic-prayer"] input[value="ep-ii"]');
  await waitFor(cdp,
    `dayReaderReady && dayReaderDebug.outcome === 'unresolved' && ` +
      `dayReaderDebug.state.options.legitimate['eucharistic-prayer'] === 'ep-ii'`,
    'applicable Eucharistic Prayer');
  const selected = await snapshot(cdp);
  const params = new URLSearchParams(selected.hash.slice(1));
  assert.equal(params.get('eucharistic-prayer'), 'ep-ii');
  assert.ok(params.get('location').endsWith(
    'ordinary-element/prex-eucharistica/prex-eucharistica-ii'));
  assert.ok(selected.semanticLocations.some((id) =>
    id.endsWith('ordinary-element/prex-eucharistica/prex-eucharistica-ii')));
  assert.deepEqual(selected.ordinaryUnresolved,
    ['ritus-initiales/gloria-in-excelsis']);
  assert.equal(await evaluate(cdp,
    `document.activeElement.closest('[data-option-group]')?.dataset.optionGroup || ''`),
  'eucharistic-prayer');

  await click(cdp, '[data-option-group="eucharistic-prayer"] input[value="ep-iv"]');
  await waitFor(cdp,
    `dayReaderReady && dayReaderDebug.outcome === 'unresolved' && ` +
      `dayReaderDebug.state.options.legitimate['eucharistic-prayer'] === 'ep-iv'`,
    'unresolved-applicability Eucharistic Prayer');
  const unresolved = await snapshot(cdp);
  const unresolvedParams = new URLSearchParams(unresolved.hash.slice(1));
  assert.equal(unresolvedParams.get('location'), 'ordinary-section/prex-eucharistica');
  assert.ok(unresolved.ordinaryChecked.includes('eucharistic-prayer:ep-iv'));
  assert.deepEqual(unresolved.ordinaryUnresolved, [
    'ritus-initiales/gloria-in-excelsis',
    'prex-eucharistica/prex-eucharistica-iv'
  ]);
  assert.ok(!unresolved.semanticLocations.some((id) =>
    id.endsWith('ordinary-element/prex-eucharistica/prex-eucharistica-iv')));
  assert.equal(await evaluate(cdp,
    `document.activeElement.closest('[data-option-group]')?.dataset.optionGroup || ''`),
  'eucharistic-prayer');
}

async function testTranslationWitnesses(cdp, base) {
  const editionWitness =
    'edition.edward-caswall.lyra-catholica.london-1849';
  const artifactWitness =
    'artifact.edward-caswall.lyra-catholica.london-1849.missal-sequences-en';
  const baseState = state({
    date: '2026-09-15', missal: 'roman-1962',
    mass: 'septem-dolorum-beatae-mariae-virginis', orations: 'en'
  });
  await navigate(cdp, base, baseState);
  const held = await snapshot(cdp);
  assert.equal(held.outcome, 'unresolved', JSON.stringify(held.error));
  assert.equal(held.witnessChoices.length, 1);
  assert.deepEqual([...new Set(held.witnessOptions)], [artifactWitness, editionWitness].sort());
  const tree = await cdp.send('Accessibility.getFullAXTree');
  const witnessRadioNames = tree.nodes.filter((node) => node.role?.value === 'radio')
    .map((node) => node.name?.value).filter(Boolean);
  assert.equal(witnessRadioNames.length, 2);
  assert.ok(witnessRadioNames.some((name) => name.includes('Lyra Catholica')));
  assert.ok(witnessRadioNames.some((name) => name.includes(artifactWitness)));

  const focusedEvent = held.witnessChoices[0];
  await click(cdp, `[data-translation-witness="${editionWitness}"]`);
  await waitFor(cdp,
    `dayReaderReady && dayReaderDebug.outcome === 'ready' && ` +
      `dayReaderDebug.state.languages.translationWitness === ${JSON.stringify(editionWitness)}`,
    'explicit translation witness');
  const selected = await snapshot(cdp);
  assert.equal(new URLSearchParams(selected.hash.slice(1)).get('translation-witness'),
    editionWitness);
  assert.deepEqual(selected.witnessChoices, []);
  assert.equal(selected.englishComposed, 1);
  assert.equal(await evaluate(cdp,
    'document.activeElement.dataset.semanticEventId || ""'), focusedEvent);

  await navigate(cdp, base, baseState + '&translation-witness=foreign');
  const invalid = await snapshot(cdp);
  assert.equal(invalid.outcome, 'invalid');
  assert.equal(invalid.eventCount, 0);
  assert.equal(invalid.error[0].path, 'translation-witness');

  await navigate(cdp, base, state({
    date: '2026-11-02', missal: 'roman-1962',
    mass: 'commemoratione-omnium-fidelium-defunctorum', form: 'first', orations: 'en'
  }));
  const noCommonWitness = await snapshot(cdp);
  assert.equal(noCommonWitness.outcome, 'unresolved', JSON.stringify(noCommonWitness.error));
  assert.deepEqual(noCommonWitness.witnessChoices, []);
  assert.equal(noCommonWitness.witnessLimitations.length, 1);
  assert.ok(noCommonWitness.witnessLimitations.every((message) =>
    message.includes('No single held translation witness supplies every translated Proper')));
}

async function testSemanticLocations(cdp, base) {
  const baseState = state({ date: '2026-08-02', mass: 'ot-18' });
  await navigate(cdp, base, baseState);
  const initial = await snapshot(cdp);
  assert.equal(initial.outcome, 'unresolved');
  assert.ok(initial.contents.includes('Source Proper choice: Communion Antiphon'));
  assert.ok(initial.semanticLocations.length > 0);
  const location = initial.semanticLocations[0];

  await navigate(cdp, base, baseState + '&location=' + encodeURIComponent(location));
  const restored = await snapshot(cdp);
  assert.equal(restored.outcome, 'unresolved', JSON.stringify(restored.error));
  assert.deepEqual(restored.stateLocation, { eventId: location });
  assert.ok(restored.semanticLocations.includes(location));

  const invalidLocation = 'proper/postconciliar/ot-18/999';
  await navigate(cdp, base,
    baseState + '&location=' + encodeURIComponent(invalidLocation));
  const invalid = await snapshot(cdp);
  assert.equal(invalid.outcome, 'invalid');
  assert.equal(invalid.eventCount, 0);
  assert.equal(invalid.fallbackUnits, 0);
  assert.ok(invalid.error.some((row) =>
    row.path === 'location' && row.code === 'invalid-semantic-location'));
  assert.equal(new URLSearchParams(invalid.hash.slice(1)).get('location'), invalidLocation);
}

async function testDeferredModeContract(cdp, base) {
  await navigate(cdp, base, state({ date: '2026-08-02', mass: 'ot-18', mode: 'study' }));
  const study = await snapshot(cdp);
  assert.equal(study.outcome, 'deferred');
  const studyParams = new URLSearchParams(study.hash.slice(1));
  assert.equal(studyParams.get('mode'), 'study');
  assert.equal(studyParams.get('ordinary'), '0');
  assert.equal(studyParams.get('ordinary-lang'), null);
  await navigate(cdp, base, study.hash);
  assert.equal((await snapshot(cdp)).outcome, 'deferred');

  await navigate(cdp, base, state({
    date: '2026-08-02', mass: 'ot-18', mode: 'study', ordinary: '1'
  }));
  const studyOrdinary = await snapshot(cdp);
  assert.equal(studyOrdinary.outcome, 'deferred');
  const studyOrdinaryParams = new URLSearchParams(studyOrdinary.hash.slice(1));
  assert.equal(studyOrdinaryParams.get('ordinary'), '1');
  assert.equal(studyOrdinaryParams.get('ordinary-lang'), 'en');
  await navigate(cdp, base, studyOrdinary.hash);
  assert.equal((await snapshot(cdp)).outcome, 'deferred');

  await navigate(cdp, base, state({
    date: '2026-08-02', mass: 'ot-18', mode: 'study',
    location: 'proper/postconciliar/ot-18/001'
  }));
  const studyLocation = await snapshot(cdp);
  assert.equal(studyLocation.outcome, 'invalid');
  assert.ok(studyLocation.error.some((row) =>
    row.path === 'location' && row.code === 'invalid-semantic-location'));

  await navigate(cdp, base, state({ date: '2026-08-02', mass: 'ot-18', mode: 'compare' }));
  const compare = await snapshot(cdp);
  assert.equal(compare.outcome, 'invalid');
  assert.equal(compare.eventCount, 0);
  assert.equal(compare.error[0].code, 'compare-mode-state');
}

async function main() {
  const server = staticServer();
  const port = await listen(server);
  const base = `http://127.0.0.1:${port}`;
  const debugPort = await freePort();
  const scratch = join(ROOT, '.scratch');
  await mkdir(scratch, { recursive: true });
  const profile = await mkdtemp(join(scratch, 'day-choice-chrome-'));
  const chrome = spawn(chromeBinary, [
    '--headless=new', '--no-sandbox', '--disable-dev-shm-usage', '--disable-gpu',
    '--disable-extensions', '--disable-background-networking', '--disable-sync',
    `--remote-debugging-port=${debugPort}`, `--user-data-dir=${profile}`,
    '--no-first-run', '--no-default-browser-check', 'about:blank'
  ], { stdio: ['ignore', 'ignore', 'pipe'] });
  let cdp;
  try {
    await waitForJson(`http://127.0.0.1:${debugPort}/json/version`);
    const created = await fetch(`http://127.0.0.1:${debugPort}/json/new?about%3Ablank`, {
      method: 'PUT'
    }).then((response) => response.json());
    const target = (await waitForJson(`http://127.0.0.1:${debugPort}/json/list`))
      .find((row) => row.id === created.id);
    cdp = new CDP(target.webSocketDebuggerUrl);
    await cdp.ready();
    await Promise.all([
      cdp.send('Page.enable'), cdp.send('Runtime.enable'),
      cdp.send('Accessibility.enable')
    ]);
    await testCalendarChoices(cdp, base);
    await testProperForms(cdp, base);
    await testColdRead(cdp, base);
    await testMultipleOrdinaryGroups(cdp, base);
    await testConditionedOrdinaryGroups(cdp, base);
    await testTranslationWitnesses(cdp, base);
    await testSemanticLocations(cdp, base);
    await testDeferredModeContract(cdp, base);
    process.stdout.write(JSON.stringify({
      status: 'pass',
      assertions: [
        'calendar-formulary-choices', 'proper-form-choices', 'cold-read-validation',
        'multiple-ordinary-groups', 'conditioned-ordinary-groups', 'translation-witness-choices',
        'semantic-location-contract', 'deferred-mode-contract'
      ].map((name) => ({ name, status: 'pass' }))
    }) + '\n');
  } finally {
    if (cdp) cdp.close();
    const exited = new Promise((accept) => chrome.once('exit', accept));
    chrome.kill('SIGTERM');
    await Promise.race([
      exited, new Promise((accept) => setTimeout(accept, 2000))
    ]);
    await new Promise((accept) => server.close(accept));
    await rm(profile, { recursive: true, force: true, maxRetries: 5, retryDelay: 100 });
  }
}

await main();
