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

function withAuthorizedCalendarChoices(payload) {
  return payload + `
;(function (root) {
  const held = root.MassAssembly;
  const choices = {
    '2026-08-07': [
      ['saints-sixtus-ii-pope-companions-martyrs', 'Saints Sixtus II and Companions'],
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
    englishComposed: document.querySelectorAll('.composed[lang="en"]').length,
    ordinaryLoads: Object.keys(dayReaderDebug.loads).filter((path) =>
      path.includes('structure/ordinary/') && !path.endsWith('/index.json')),
    ordinaryPresentations: dayReaderDebug.ordinaryPresentations
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
    ['2026-08-07', ['saints-sixtus-ii-pope-companions-martyrs', 'ot-18-friday']],
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
  await navigate(cdp, base, state({
    date: '2026-08-02', mass: 'ot-18', 'ordinary-lang': 'en',
    'eucharistic-prayer': 'ep-ii'
  }));
  const held = await snapshot(cdp);
  assert.equal(held.outcome, 'ready');
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
}

async function testDeferredModeContract(cdp, base) {
  await navigate(cdp, base, state({ date: '2026-08-02', mass: 'ot-18', mode: 'study' }));
  assert.equal((await snapshot(cdp)).outcome, 'deferred');

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
    await testTranslationWitnesses(cdp, base);
    await testDeferredModeContract(cdp, base);
    process.stdout.write(JSON.stringify({
      status: 'pass',
      assertions: [
        'calendar-formulary-choices', 'proper-form-choices', 'cold-read-validation',
        'translation-witness-choices', 'deferred-mode-contract'
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
