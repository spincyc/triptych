#!/usr/bin/env node

/* Real-Chromium interaction, race, reflow, parity, and review gates for W3. */

import assert from 'node:assert/strict';
import { spawn } from 'node:child_process';
import { createServer } from 'node:http';
import { mkdir, mkdtemp, readFile, rm, writeFile } from 'node:fs/promises';
import { tmpdir } from 'node:os';
import { extname, resolve, sep } from 'node:path';
import process from 'node:process';
import { refreshCoverage, readerTools, fixtureRequest, verifyRealWitnesses } from './reader_coverage_fixture.mjs';

const ROOT = resolve(process.env.TRIPTYCH_REVIEW_ROOT || resolve(import.meta.dirname, '../..'));
const CANDIDATE = '/src/web/browser/liturgy/propers-reader.html';
const CURRENT = '/src/web/browser/liturgy/index.html';
const SOURCE_ONLY = process.env.TRIPTYCH_SOURCE_ONLY === '1';
const DATA = SOURCE_ONLY ? '/src/web/data' : '/build/public-alpha/preview/browse';
const SOURCE_PROPERS = (process.env.TRIPTYCH_SOURCE_PROPERS ||
  'src/web/data/structure/propers').replace(/^\/+|\/+$/g, '');
const CYCLE_UNTRANSLATED_DATA = DATA + '-cycle-untranslated';
const NO_WITNESS_DATA = DATA + '-no-witness';
const BAD_SPLIT_DATA = DATA + '-bad-split';
const captureAt = process.argv.indexOf('--capture-dir');
const captureDir = captureAt >= 0 ? resolve(process.argv[captureAt + 1]) : null;
const chromeBinary = process.env.TRIPTYCH_CHROME || '/usr/bin/google-chrome-stable';
const failures = [];
const results = [];
const consoleProblems = [];
const failedRequests = [];
let accessibilityReport = null;
let performanceReport = null;
let responseGate = null;
let navigationSerial = 0;

function mime(path) {
  return ({
    '.css': 'text/css; charset=utf-8', '.html': 'text/html; charset=utf-8',
    '.js': 'text/javascript; charset=utf-8', '.json': 'application/json',
    '.png': 'image/png', '.svg': 'image/svg+xml'
  })[extname(path)] || 'application/octet-stream';
}

function armGate(match) {
  let started;
  let release;
  let served;
  const gate = {
    match, seen: [], started: new Promise((done) => { started = done; }),
    releaseSignal: new Promise((done) => { release = done; }),
    served: new Promise((done) => { served = done; }),
    claim(path) { responseGate = null; started(path); },
    release() { release(); }, finish() { served(); }
  };
  responseGate = gate;
  return gate;
}

async function waitGate(gate) {
  await Promise.race([
    gate.started,
    new Promise((_done, reject) => setTimeout(() => reject(new Error(
      'response gate timeout; requests after arming: ' + gate.seen.join(', ')
    )), 8000))
  ]);
}

function withCycleUntranslated(body) {
  const payload = JSON.parse(body);
  const mass = payload.masses.find((row) => row.key === 'transfiguration-lord');
  const proper = mass && mass.propers[0];
  if (!proper) throw new Error('cycle-untranslated fixture target is absent');
  mass.propers.forEach((row) => { row.form_id = 'main'; });
  proper.name = 'Collect';
  proper.source = 'composed';
  const absence = (cycle, state) => ({
    target: {
      mass: mass.key, form_id: 'main', proper: proper.name,
      cycle, occurrence: 1, extent: 'body'
    },
    lang: 'en', state
  });
  proper.citations = [];
  proper.text = null;
  proper.translations = [];
  proper.unavailable_translations = null;
  proper.untranslated = null;
  proper.incipit = null;
  proper.cycles = {
    A: {
      citations: [], text: 'A Latin sibling sentinel',
      unavailable_translations: [absence('A', 'rights-restricted')]
    },
    B: {
      citations: [], text: null,
      latin: {
        target: absence('B', 'unavailable').target,
        state: 'unavailable', held: false, available: false, withheld: false
      },
      translations: [{
        lang: 'en', text: 'B held English without a Latin body',
        source_id: 'synthetic.cycle-b-held-english', rights: 'Public Domain'
      }]
    },
    C: {
      citations: [], text: 'C Latin safe sibling',
      untranslated: [absence('C', 'unavailable')]
    }
  };
  return refreshCoverage(payload, ROOT);
}

function withoutWitness(body) {
  const payload = JSON.parse(body);
  const mass = payload.masses.find((row) =>
    row.key === 's-hilarii-episcopi-confessoris-ecclesiae-doctoris');
  if (!mass) throw new Error('no-witness fixture target is absent');
  const occurrences = new Map();
  mass.propers.forEach((proper) => {
    proper.form_id = 'main';
    delete proper.form;
    if (!proper.text) return;
    const occurrence = (occurrences.get(proper.name) || 0) + 1;
    occurrences.set(proper.name, occurrence);
    proper.translations = [];
    proper.untranslated = [{
      target: {
        mass: mass.key, form_id: 'main', proper: proper.name,
        cycle: 'all', occurrence, extent: 'body'
      },
      lang: 'en', state: 'unavailable'
    }];
  });
  return refreshCoverage(payload, ROOT);
}

function server() {
  return createServer(async (request, response) => {
    let gate = null;
    try {
      const url = new URL(request.url, 'http://127.0.0.1');
      let relative = decodeURIComponent(url.pathname).replace(/^\/+/, '');
      if (relative === 'favicon.ico') {
        response.writeHead(204); response.end(); return;
      }
      if (responseGate) responseGate.seen.push(relative);
      if (responseGate && responseGate.match(relative)) {
        gate = responseGate; gate.claim(relative); await gate.releaseSignal;
      }
      const corrupt = relative.startsWith(DATA.slice(1) + '-failure/');
      if (corrupt) {
        relative = relative.replace(DATA.slice(1) + '-failure/', DATA.slice(1) + '/');
        if (relative.endsWith('/structure/propers/catalog/roman-1962.json')) {
          response.writeHead(200, { 'content-type': 'application/json', 'cache-control': 'no-store' });
          response.end('{"schema":"invalid"}'); return;
        }
        if (relative.endsWith('/structure/propers/roman-1962.json')) {
          response.writeHead(200, { 'content-type': 'application/json', 'cache-control': 'no-store' });
          response.end('{'); return;
        }
      }
      const cycleUntranslated = relative.startsWith(SOURCE_ONLY
        ? 'src/web/data-cycle-untranslated/'
        : 'build/public-alpha/preview/browse-cycle-untranslated/');
      if (cycleUntranslated) {
        relative = SOURCE_ONLY
          ? relative.replace('/data-cycle-untranslated/', '/data/')
          : relative.replace('/browse-cycle-untranslated/', '/browse/');
      }
      const noWitness = relative.startsWith(SOURCE_ONLY
        ? 'src/web/data-no-witness/' : 'build/public-alpha/preview/browse-no-witness/');
      if (noWitness) {
        relative = SOURCE_ONLY
          ? relative.replace('/data-no-witness/', '/data/')
          : relative.replace('/browse-no-witness/', '/browse/');
      }
      const badSplit = relative.startsWith(BAD_SPLIT_DATA.slice(1) + '/');
      if (badSplit) relative = relative.replace(BAD_SPLIT_DATA.slice(1) + '/', DATA.slice(1) + '/');
      if (SOURCE_ONLY && /^src\/web\/data\/[^/]+\/chapters\//.test(relative)) {
        relative = relative.replace(/^src\/web\/data\//, 'src/sources/bibles/');
      }
      if (SOURCE_ONLY && /^src\/web\/data\/structure\/propers\/[^/]+\.json$/.test(relative)) {
        relative = relative.replace('src/web/data/structure/propers', SOURCE_PROPERS);
      }
      const file = resolve(ROOT, relative || 'README.md');
      if (file !== ROOT && !file.startsWith(ROOT + sep)) throw new Error('outside root');
      let body = await readFile(file);
      if (cycleUntranslated && relative.endsWith('/structure/propers/postconciliar.json')) {
        body = Buffer.from(JSON.stringify(withCycleUntranslated(body.toString('utf8'))));
      }
      if (noWitness && relative.endsWith('/structure/propers/roman-1962.json')) {
        body = Buffer.from(JSON.stringify(withoutWitness(body.toString('utf8'))));
      }
      if (noWitness && relative.endsWith('/structure/propers/index.json')) {
        const index = JSON.parse(body);
        delete index.missals.find(row => row.id === 'roman-1962').read_payload;
        body = Buffer.from(JSON.stringify(index));
      }
      if (badSplit && /\/structure\/propers\/mass\/roman-1962\/[^/]+\.json$/.test(relative)) {
        const envelope = JSON.parse(body);
        envelope.generation = '0'.repeat(64);
        body = Buffer.from(JSON.stringify(envelope));
      }
      response.writeHead(200, {
        'content-type': mime(file), 'cache-control': 'no-store',
        'x-robots-tag': 'noindex, nofollow'
      });
      response.end(body);
    } catch (_error) {
      response.writeHead(404, { 'content-type': 'text/plain; charset=utf-8' });
      response.end('not found');
    } finally {
      if (gate) gate.finish();
    }
  });
}

async function listen(instance) {
  await new Promise((done, reject) => {
    instance.once('error', reject); instance.listen(0, '127.0.0.1', done);
  });
  return instance.address().port;
}

async function freePort() {
  const instance = createServer();
  const port = await listen(instance);
  await new Promise((done) => instance.close(done));
  return port;
}

async function waitJson(url) {
  for (let count = 0; count < 120; count += 1) {
    try { const reply = await fetch(url); if (reply.ok) return await reply.json(); } catch (_error) {}
    await new Promise((done) => setTimeout(done, 50));
  }
  throw new Error('Chromium debugging endpoint did not start');
}

class CDP {
  constructor(url) {
    this.socket = new WebSocket(url); this.next = 0; this.pending = new Map(); this.events = new Map();
  }
  async ready() {
    await new Promise((done, reject) => {
      this.socket.addEventListener('open', done, { once: true });
      this.socket.addEventListener('error', reject, { once: true });
    });
    this.socket.addEventListener('message', (event) => {
      const message = JSON.parse(event.data);
      if (message.id) {
        const held = this.pending.get(message.id); if (!held) return;
        this.pending.delete(message.id); clearTimeout(held.timer);
        if (message.error) held.reject(new Error(message.error.message)); else held.done(message.result);
      } else {
        (this.events.get(message.method) || []).forEach((handler) => handler(message.params || {}));
      }
    });
  }
  on(name, handler) {
    if (!this.events.has(name)) this.events.set(name, []);
    this.events.get(name).push(handler);
  }
  send(method, params = {}) {
    const id = ++this.next;
    return new Promise((done, reject) => {
      const timer = setTimeout(() => { this.pending.delete(id); reject(new Error('CDP timeout: ' + method)); }, 20000);
      this.pending.set(id, { done, reject, timer });
      this.socket.send(JSON.stringify({ id, method, params }));
    });
  }
  close() { this.socket.close(); }
}

async function evaluate(cdp, expression) {
  const reply = await cdp.send('Runtime.evaluate', {
    expression, awaitPromise: true, returnByValue: true, userGesture: true
  });
  if (reply.exceptionDetails) throw new Error(reply.exceptionDetails.exception?.description || reply.exceptionDetails.text);
  return reply.result.value;
}

async function waitFor(cdp, expression, label, attempts = 180) {
  for (let count = 0; count < attempts; count += 1) {
    if (await evaluate(cdp, `Boolean(${expression})`)) return;
    await new Promise((done) => setTimeout(done, 50));
  }
  throw new Error('Timed out waiting for ' + label);
}

function hash(values) { return '#' + new URLSearchParams(values).toString(); }
const MULTIPLE_TRANSLATION_WITNESS =
  'edition.edward-caswall.lyra-catholica.london-1849';
const STATES = Object.freeze({
  roman: hash({ missal: 'roman-1962', type: 'seasonal', mass: 'advent-1', bible: 'douay-rheims', orations: 'la' }),
  romanTrinity: hash({ missal: 'roman-1962', type: 'seasonal', mass: 'trinity', bible: 'douay-rheims', orations: 'la' }),
  post: hash({ missal: 'postconciliar', type: 'seasonal', mass: 'advent-1', bible: 'douay-rheims', orations: 'la' }),
  cycles: hash({ missal: 'postconciliar', type: 'christological', mass: 'transfiguration-lord', bible: 'douay-rheims', orations: 'la' }),
  cycleA: hash({ missal: 'postconciliar', type: 'christological', mass: 'transfiguration-lord', bible: 'douay-rheims', orations: 'la', cycle: 'A' }),
  cycleLegacyA: hash({ missal: 'postconciliar', type: 'christological', mass: 'transfiguration-lord', bible: 'douay-rheims', orations: 'la', '_candidate-cycle': 'A' }),
  cycleMixed: hash({ missal: 'postconciliar', type: 'christological', mass: 'transfiguration-lord', bible: 'douay-rheims', orations: 'la', cycle: 'A', '_candidate-cycle': 'A' }),
  cycleBad: hash({ missal: 'postconciliar', type: 'christological', mass: 'transfiguration-lord', bible: 'douay-rheims', orations: 'la', cycle: 'Z' }),
  alternativeUnsupported: hash({ missal: 'postconciliar', type: 'christological', mass: 'transfiguration-lord', bible: 'douay-rheims', orations: 'la', alternative: 'first-reading-alternative' }),
  alternative: hash({ missal: 'postconciliar', type: 'marian', mass: 'visitation-blessed-virgin-mary', bible: 'douay-rheims', orations: 'la' }),
  partial: hash({ missal: 'roman-1962', type: 'christological', mass: 'octava-nativitatis-domini', bible: 'douay-rheims', orations: 'la' }),
  withheld: hash({ missal: 'roman-1962', type: 'sanctoral', mass: 's-antonii-mariae-claret-episcopi-confessoris', bible: 'douay-rheims', orations: 'la' }),
  missing: hash({ missal: 'roman-1962', bible: 'douay-rheims', orations: 'la' }),
  postMissing: hash({ missal: 'postconciliar', bible: 'douay-rheims', orations: 'la' }),
  invalid: hash({ missal: 'not-a-missal', type: 'seasonal', mass: 'advent-1', bible: 'douay-rheims', orations: 'la' }),
  invalidMass: hash({ missal: 'roman-1962', type: 'seasonal', mass: 'not-a-mass', bible: 'douay-rheims', orations: 'la' }),
  fast: hash({ missal: 'postconciliar', type: 'marian', mass: 'visitation-blessed-virgin-mary', bible: 'douay-rheims', orations: 'la' }),
  englishMultiple: hash({ missal: 'roman-1962', type: 'sanctoral', mass: 'commemoratione-omnium-fidelium-defunctorum', form: 'first', bible: 'douay-rheims', orations: 'en' }),
  englishWitness: hash({ missal: 'roman-1962', type: 'sanctoral', mass: 'commemoratione-omnium-fidelium-defunctorum', form: 'first', bible: 'douay-rheims', orations: 'en', 'translation-witness': MULTIPLE_TRANSLATION_WITNESS }),
  englishOne: hash({ missal: 'roman-1962', type: 'sanctoral', mass: 'comm-s-saturnini-martyris', bible: 'douay-rheims', orations: 'en' }),
  englishNone: hash({ missal: 'roman-1962', type: 'sanctoral', mass: 's-hilarii-episcopi-confessoris-ecclesiae-doctoris', bible: 'douay-rheims', orations: 'en' }),
  romanChristmasForms: hash({ missal: 'roman-1962', type: 'christological', mass: 'nativitate-domini-octave', bible: 'douay-rheims', orations: 'la' }),
  romanChristmasNight: hash({ missal: 'roman-1962', type: 'christological', mass: 'nativitate-domini-octave', bible: 'douay-rheims', orations: 'la', form: 'night' }),
  postPentecostDay: hash({ missal: 'postconciliar', type: 'seasonal', mass: 'pentecost', bible: 'douay-rheims', orations: 'la', form: 'day' }),
  romanPentecost: hash({ missal: 'roman-1962', type: 'seasonal', mass: 'pentecost', bible: 'douay-rheims', orations: 'la' }),
  romanPentecostEnglish: hash({ missal: 'roman-1962', type: 'seasonal', mass: 'pentecost', bible: 'douay-rheims', orations: 'en' }),
  englishWithoutLatinBody: hash({ missal: 'roman-1962', type: 'sanctoral', mass: 's-alberti-magni-episcopi-confessoris-ecclesiae', bible: 'douay-rheims', orations: 'en' }),
  pre1955Advent: hash({ missal: 'roman-pre-1955', type: 'seasonal', mass: 'advent-1', bible: 'douay-rheims', orations: 'la' }),
  pre1955Trinity: hash({ missal: 'roman-pre-1955', type: 'seasonal', mass: 'trinity', bible: 'douay-rheims', orations: 'la' }),
  pre1955Palm: hash({ missal: 'roman-pre-1955', type: 'seasonal', mass: 'palm-sunday', bible: 'douay-rheims', orations: 'la' }),
  pre1955Supper: hash({ missal: 'roman-pre-1955', type: 'seasonal', mass: 'mass-of-the-lords-supper', bible: 'douay-rheims', orations: 'la' }),
  formWithoutMass: hash({ missal: 'postconciliar', bible: 'douay-rheims', orations: 'la', form: 'vigil' }),
  invalidLocation: hash({ missal: 'roman-1962', type: 'seasonal', mass: 'advent-1', bible: 'douay-rheims', orations: 'la', location: 'proper/roman-1962/advent-1/999' }),
  validLocation: hash({ missal: 'roman-1962', type: 'seasonal', mass: 'advent-1', bible: 'douay-rheims', orations: 'la', location: 'proper/roman-1962/advent-1/003' }),
  cycleAUntranslated: hash({ missal: 'postconciliar', type: 'christological', mass: 'transfiguration-lord', bible: 'douay-rheims', orations: 'en', cycle: 'A' }),
  cycleBHeldEnglish: hash({ missal: 'postconciliar', type: 'christological', mass: 'transfiguration-lord', bible: 'douay-rheims', orations: 'en', cycle: 'B' }),
  cycleCUntranslated: hash({ missal: 'postconciliar', type: 'christological', mass: 'transfiguration-lord', bible: 'douay-rheims', orations: 'en', cycle: 'C' })
});

function candidateUrl(base, state = STATES.roman, data = DATA) {
  return `${base}${CANDIDATE}?data=${data}${state}`;
}
function currentUrl(base, state = STATES.roman) { return `${base}${CURRENT}?data=${DATA}${state}`; }

async function navigate(cdp, url, ready = 'window.propersReaderReady === true') {
  await cdp.send('Page.navigate', { url });
  await waitFor(cdp, `location.href === ${JSON.stringify(url)} && ${ready}`, 'page readiness');
  await new Promise((done) => setTimeout(done, 70));
}

async function candidate(cdp, base, state = STATES.roman, data = DATA) {
  const url = `${base}${CANDIDATE}?data=${data}&test-nav=${++navigationSerial}${state}`;
  await cdp.send('Page.navigate', { url });
  await waitFor(cdp,
    `performance.getEntriesByType('navigation')[0]?.name === ${JSON.stringify(url)} && ` +
    'window.propersReaderReady === true', 'Propers readiness');
  await new Promise((done) => setTimeout(done, 70));
}

async function freshCandidate(cdp, base, state = STATES.roman, data = DATA) {
  const url = `${base}${CANDIDATE}?data=${data}&browse-race=${Math.random()}${state}`;
  await cdp.send('Page.navigate', { url });
  await waitFor(cdp,
    `performance.getEntriesByType('navigation')[0]?.name === ${JSON.stringify(url)} && ` +
    'window.propersReaderReady === true', 'fresh Propers readiness');
  await new Promise((done) => setTimeout(done, 70));
}

async function current(cdp, base, state = STATES.roman) {
  const url = currentUrl(base, state);
  await cdp.send('Page.navigate', { url });
  // The public route canonically omits the default Latin `orations` key.
  await waitFor(cdp,
    `location.pathname === ${JSON.stringify(CURRENT)} && window.propersReaderReady === true && (` +
    `document.querySelector('#reader-document[aria-busy="false"] .proper') || ` +
    `document.querySelector('#reader-document[aria-busy="false"] .error') || ` +
    `document.querySelector('#coverage-notice:not([hidden])'))`, 'current Propers readiness');
  await new Promise((done) => setTimeout(done, 70));
  const problem = await evaluate(cdp,
    `document.querySelector('#reader-document .proper') ? '' : ` +
    `(document.querySelector('#reader-document .error')?.textContent || document.querySelector('#coverage-notice')?.textContent)`);
  assert.equal(problem, '', 'current Propers route did not render: ' + problem);
}

async function click(cdp, selector) {
  await evaluate(cdp, `(() => { const node = document.querySelector(${JSON.stringify(selector)}); if (!node) throw new Error('missing ${selector}'); node.click(); })()`);
  await new Promise((done) => setTimeout(done, 50));
}

async function openSurface(cdp, name) {
  if (name === 'details' && !await evaluate(cdp,
    `document.querySelector('[data-reader-surface="mode"]').open`)) {
    await click(cdp, '[data-reader-action="mode"]');
  }
  await click(cdp, `[data-reader-action="${name}"]`);
}

async function select(cdp, selector, value) {
  await evaluate(cdp, `(() => {
    const node = document.querySelector(${JSON.stringify(selector)});
    if (!node) throw new Error('missing ${selector}');
    node.value = ${JSON.stringify(value)};
    node.dispatchEvent(new Event('change', {bubbles:true}));
  })()`);
  await new Promise((done) => setTimeout(done, 30));
}

async function browseSnapshot(cdp) {
  return evaluate(cdp, `(() => ({
    open: document.querySelector('#browse-surface').open,
    missal: document.querySelector('#reader-missal').value,
    types: [...document.querySelector('#reader-type').options].map(row => row.value),
    type: document.querySelector('#reader-type').value,
    formularies: [...document.querySelector('#reader-formulary').options].map(row => row.value),
    formulary: document.querySelector('#reader-formulary').value,
    formularyLabel: document.querySelector('#reader-formulary').selectedOptions[0]?.textContent || '',
    formularyLabels: [...document.querySelector('#reader-formulary').options].map(row => row.textContent),
    bible: document.querySelector('#reader-bible').value,
    orations: document.querySelector('#reader-orations').value,
    witnessHidden: document.querySelector('#reader-witness-field').hidden,
    witnessDisplay: getComputedStyle(document.querySelector('#reader-witness-field')).display,
    witnesses: [...document.querySelector('#reader-witness').options].map(row => row.value),
    witnessLabels: [...document.querySelector('#reader-witness').options].map(row => row.textContent),
    orationLabels: [...document.querySelector('#reader-orations').options].map(row => row.textContent),
    witness: document.querySelector('#reader-witness').value,
    status: document.querySelector('#browse-status').textContent,
    applyDisabled: document.querySelector('#browse-form .surface-apply').disabled,
    semantic: propersReaderDebug.semantic,
    outcome: propersReaderDebug.outcome
  }))()`);
}

async function escape(cdp) {
  for (const type of ['keyDown', 'keyUp']) {
    await cdp.send('Input.dispatchKeyEvent', { type, key: 'Escape', code: 'Escape', windowsVirtualKeyCode: 27 });
  }
  await new Promise((done) => setTimeout(done, 50));
}

async function viewport(cdp, width, height) {
  await cdp.send('Emulation.setDeviceMetricsOverride', {
    width, height, screenWidth: width, screenHeight: height,
    deviceScaleFactor: 1, mobile: width <= 768
  });
}

async function shot(cdp, path) {
  const image = await cdp.send('Page.captureScreenshot', { format: 'png', fromSurface: true });
  await writeFile(path, Buffer.from(image.data, 'base64'));
}

async function check(name, action) {
  try { await action(); results.push({ name, status: 'pass' }); }
  catch (error) {
    failures.push({ name, detail: error.stack || String(error) });
    results.push({ name, status: 'fail' });
    if (process.env.TRIPTYCH_FAIL_FAST === '1') throw error;
  }
}

async function snapshot(cdp) {
  return evaluate(cdp, `(() => ({
    title: document.querySelector('#formulary-title')?.textContent,
    documentTitle: document.title,
    meta: document.querySelector('#formulary-meta')?.textContent,
    source: document.querySelector('#formulary-source')?.textContent,
    sourceHidden: document.querySelector('#formulary-source')?.hidden,
    outcome: propersReaderDebug.outcome,
    notice: document.querySelector('#coverage-notice')?.textContent,
    noticeHidden: document.querySelector('#coverage-notice')?.hidden,
    names: [...document.querySelectorAll('#reader-document .proper-name')].map(row => row.textContent.trim()),
    texts: [...document.querySelectorAll('#reader-document .proper')].map(row => row.textContent.replace(/\\s+/g, ' ').trim()),
    state: propersReaderDebug.state,
    semantic: propersReaderDebug.semantic,
    error: propersReaderDebug.error
  }))()`);
}

// Whether the selected Latin Proper bodies fall short of exact target wording,
// computed from the same structure and unit coverage records the notice reads.
// The coverage lane regrades these records, so the notice is checked against the
// contract rather than against a fixed count (C2).
async function latinExactIncomplete(cdp, calendar, debug = 'propersReaderDebug') {
  return evaluate(cdp, `(async () => {
    const structure = await window.Triptych.loadJSON('structure/propers/${calendar}.json');
    const report = window.Triptych.summarizeCoverage(
      window.Triptych.selectedCoverageUnits(window[${JSON.stringify(debug)}].semantic, structure));
    const row = report.languages.find(one => one.lang === 'la');
    return row.exact_target < row.occurrences;
  })()`);
}

// Every rendered Proper unit against its own unit coverage record: a Bible
// reconstruction carries the claim immediately before its passages; a unit the
// record does not type as one carries none (C2 G9).
async function bibleClaimAudit(cdp, debug, calendar) {
  return evaluate(cdp, `(async () => {
    const T = window.Triptych;
    const structure = await T.loadJSON('structure/propers/${calendar}.json');
    const events = [];
    (window[${JSON.stringify(debug)}].semantic.events || []).forEach(row => {
      if (row.kind === 'proper') events.push(row);
      if (row.kind === 'proper-choice') (row.options || []).forEach(option =>
        (option.events || []).forEach(member => events.push(member)));
    });
    return events.map(event => {
      const expected = T.selectedCoverageUnits({ events: [event] }, structure).some(unit =>
        unit.scripture_component
          ? unit.scripture_component.relationship === 'bible-reconstruction'
          : unit.component === 'scripture' &&
            (unit.languages || []).some(row => row.relationship === 'bible-reconstruction'));
      const node = document.querySelector('[data-proper-choice-member-event="' + event.id + '"]') ||
        document.querySelector('[data-semantic-event-id="' + event.id + '"]');
      const claims = node ? [...node.querySelectorAll('[data-unit-claim]')] : [];
      // A mixed unit whose Missal text is shown labels its passages as the
      // cited text in the selected Bible; only a unit with no Missal text
      // shown carries the reconstruction claim (G9 follow-up).
      const mixed = T.selectedCoverageUnits({ events: [event] }, structure)
        .some(unit => Boolean(unit.scripture_component));
      const shown = Boolean(node && node.querySelector('.composed'));
      return {
        id: event.id, expected, found: Boolean(node), claims: claims.length,
        expectedKind: mixed && shown ? 'bible-text' : 'bible-reconstruction',
        kinds: claims.map(claim => claim.dataset.unitClaim),
        citations: node ? node.querySelectorAll('.citation').length : 0,
        ordered: claims.every(claim => claim.nextElementSibling &&
          claim.nextElementSibling.classList.contains('citation')),
        text: claims.map(claim => claim.textContent.trim())
      };
    });
  })()`);
}

function assertBibleClaims(rows, label) {
  assert.ok(rows.length > 0, label + ' rendered no Proper units');
  assert.ok(rows.some(row => row.expected) && rows.some(row => !row.expected),
    label + ' exemplar exercises both kinds: ' + JSON.stringify(rows));
  for (const row of rows) {
    assert.ok(row.found, label + ' unit missing from the page: ' + row.id);
    if (row.expected) {
      assert.ok(row.claims >= 1 && row.claims <= row.citations, label + ' ' + JSON.stringify(row));
      assert.ok(row.ordered, label + ' claim not set before its passage: ' + JSON.stringify(row));
      assert.ok(row.kinds.every(kind => kind === row.expectedKind), label + ' ' + JSON.stringify(row));
      assert.ok(row.text.every(text => row.expectedKind === 'bible-text'
        ? /^Bible text · .+ · not the Missal’s wording$/.test(text)
        : text === 'Bible reconstruction · Missal wording not established'),
        label + ' ' + JSON.stringify(row));
    } else {
      assert.equal(row.claims, 0, label + ' claim on a unit not typed as reconstruction: ' + row.id);
    }
  }
}

// C2 G14: every rendered Proper body against the structure's checked internal
// structure. Stanza groups and rubric spans are read from the DOM; what they
// must contain is read from the generated structure's own offsets.
async function textStructureAudit(cdp, calendar, massKey) {
  return evaluate(cdp, `(async () => {
    const T = window.Triptych;
    const structure = await T.loadJSON('structure/propers/${calendar}.json');
    const mass = structure.masses.find(row => row.key === ${JSON.stringify(massKey)});
    const clean = text => String(text || '').replace(/\\s+/g, ' ').trim();
    const shown = node => {
      const copy = node.cloneNode(true);
      copy.querySelectorAll('.visually-hidden, .composed-label').forEach(one => one.remove());
      return clean(copy.textContent).replace(/℣/g, 'V.').replace(/℟/g, 'R.')
        .replace(/V\\. (?=\\S)/g, 'V. ').replace(/R\\. (?=\\S)/g, 'R. ');
    };
    const sections = [...document.querySelectorAll('#reader-document section.proper')];
    return mass.propers.map(proper => {
      const section = sections.find(one => {
        const head = one.querySelector('.proper-name');
        return head && clean(head.childNodes[0] && head.childNodes[0].textContent) === proper.name;
      });
      const composed = section && section.querySelector(':scope > .composed');
      if (!composed) return { name: proper.name, found: Boolean(section), composed: false };
      const lang = composed.lang;
      const body = lang === 'la' ? proper : (proper.translations || []).find(row =>
        row.lang === lang && row.text_structure) || {};
      const held = body.text_structure || {};
      const text = body.text || '';
      const starts = held.stanzas || [];
      const rubrics = [...composed.querySelectorAll('.inline-rubric')];
      const principal = composed.cloneNode(true);
      principal.querySelectorAll('.inline-rubric').forEach(one => one.remove());
      return {
        name: proper.name, found: true, composed: true, lang,
        group: composed.classList.contains('composed-stanzas'),
        stanzaNodes: [...composed.querySelectorAll(':scope > .stanza')].map(shown),
        stanzas: starts.map((start, index) => clean(text.slice(start, starts[index + 1]))),
        actions: (held.actions || []).map(action => clean(text.slice(action.start, action.end))),
        rubrics: rubrics.map(node => ({
          text: shown(node), kind: node.dataset.inlineAction,
          italic: getComputedStyle(node).fontStyle, lang: node.closest('[lang]').lang,
          labelLang: node.querySelector('.visually-hidden')?.lang || null
        })),
        principal: shown(principal)
      };
    });
  })()`);
}

function assertTextStructure(rows, lang, label) {
  const bodies = rows.filter(row => row.composed && row.lang === lang);
  assert.ok(bodies.some(row => row.stanzas.length > 1), label + ' exercises stanzas: ' + JSON.stringify(rows));
  assert.ok(bodies.some(row => row.actions.length > 0), label + ' exercises an inline action: ' + JSON.stringify(rows));
  for (const row of rows.filter(one => one.composed)) {
    const where = label + ' ' + row.name;
    if (row.stanzas.length > 1) {
      assert.equal(row.group, true, where + ' is a stanza group');
      assert.deepEqual(row.stanzaNodes, row.stanzas, where + ' stanzas follow the checked offsets');
    } else {
      assert.equal(row.group, false, where + ' carries no unchecked stanzas');
      assert.deepEqual(row.stanzaNodes, [], where);
    }
    assert.deepEqual(row.rubrics.map(one => one.text), row.actions, where + ' rubric spans');
    for (const rubric of row.rubrics) {
      assert.equal(rubric.kind, 'rubric', where);
      assert.equal(rubric.italic, 'italic', where + ' rubric is set apart beyond colour');
      assert.equal(rubric.lang, row.lang, where + ' rubric keeps the text language');
      assert.equal(rubric.labelLang, 'en', where + ' rubric label is English interface text');
    }
    for (const action of row.actions) {
      assert.ok(!row.principal.includes(action), where + ' rubric is not principal text');
    }
  }
}

// Real clipboard text of one Proper section, copied through the browser.
async function copiedProper(cdp, name) {
  return evaluate(cdp, `(async () => {
    const section = [...document.querySelectorAll('#reader-document section.proper')].find(one => {
      const head = one.querySelector('.proper-name');
      return head && head.childNodes[0] && head.childNodes[0].textContent.trim() === ${JSON.stringify(name)};
    });
    if (!section) return null;
    const selection = getSelection();
    selection.removeAllRanges();
    const range = document.createRange();
    range.selectNodeContents(section);
    selection.addRange(range);
    const copied = document.execCommand('copy');
    selection.removeAllRanges();
    let text = null;
    try { text = await navigator.clipboard.readText(); } catch (error) { text = 'ERROR ' + error; }
    return {
      copied, text,
      glyphs: section.querySelectorAll('.vr-glyph').length,
      verses: section.querySelectorAll('.verse').length,
      rubrics: [...section.querySelectorAll('.inline-rubric')].map(node => {
        const copy = node.cloneNode(true);
        copy.querySelectorAll('.visually-hidden').forEach(one => one.remove());
        return copy.textContent.trim();
      }),
      stanzas: [...section.querySelectorAll('.stanza')].map(node => {
        const copy = node.cloneNode(true);
        copy.querySelectorAll('.visually-hidden').forEach(one => one.remove());
        return copy.textContent.replace(/\\s+/g, ' ').trim();
      })
    };
  })()`);
}

const HIDDEN_LABELS = /Verse \d|Versicle\.|Response\.|Rubric:|Composed text|Missal text|Bible text|Bible reconstruction/;

function assertCopied(row, label) {
  assert.ok(row && row.copied === true, label + ' copy command: ' + JSON.stringify(row));
  assert.doesNotMatch(row.text, /^ERROR /, label + ' clipboard read');
  assert.doesNotMatch(row.text, HIDDEN_LABELS, label + ' copies no hidden label: ' + row.text);
  assert.equal((row.text.match(/℣|℟/g) || []).length, row.glyphs, label + ' keeps every ℣/℟: ' + row.text);
  for (const rubric of row.rubrics) assert.ok(row.text.includes(rubric), label + ' keeps the printed rubric');
  if (row.stanzas.length) {
    const blocks = row.text.split(/\n\n/).map(block => block.replace(/\s+/g, ' ').trim());
    const first = blocks.indexOf(row.stanzas[0]);
    assert.ok(first >= 0, label + ' copies the first stanza as a block: ' + row.text);
    assert.deepEqual(blocks.slice(first, first + row.stanzas.length), row.stanzas, label + ' copies stanzas apart');
  }
}

// G9 follow-up: in a mixed unit the citation passages under the Missal's own
// text are the cited text in the selected Bible, and say so by name.
async function mixedClaimAudit(cdp, calendar, massKey) {
  return evaluate(cdp, `(async () => {
    const T = window.Triptych;
    const structure = await T.loadJSON('structure/propers/${calendar}.json');
    const bibles = await T.loadJSON('bibles.json');
    const wanted = new URLSearchParams(location.hash.slice(1)).get('bible');
    const bible = bibles.bibles.find(row => row.id === wanted);
    const mass = structure.masses.find(row => row.key === ${JSON.stringify(massKey)});
    const sections = [...document.querySelectorAll('#reader-document section.proper')];
    return {
      label: bible && bible.label,
      notice: document.querySelector('#coverage-notice')?.textContent || '',
      rows: mass.propers.map(proper => {
        const section = sections.find(one => {
          const head = one.querySelector('.proper-name');
          return head && head.childNodes[0] && head.childNodes[0].textContent.trim() === proper.name;
        });
        const claims = section ? [...section.querySelectorAll('[data-unit-claim]')] : [];
        return {
          name: proper.name, source: proper.source, found: Boolean(section),
          shown: Boolean(section && section.querySelector(':scope > .composed')),
          citations: section ? section.querySelectorAll('.citation').length : 0,
          claims: claims.map(claim => [claim.dataset.unitClaim, claim.textContent.trim()]),
          composedLabel: section?.querySelector(':scope > .composed > .composed-label')?.textContent || null
        };
      })
    };
  })()`);
}

function assertMixedClaims(value, label) {
  assert.ok(value.label, label + ' selected Bible label');
  const mixed = value.rows.filter(row => row.source === 'mixed');
  assert.ok(mixed.length > 0, label + ' exemplar has mixed units');
  for (const row of value.rows) {
    const where = label + ' ' + row.name + ' ' + JSON.stringify(row);
    assert.ok(row.found, where);
    if (row.source === 'mixed') {
      assert.equal(row.shown, true, where);
      assert.match(row.composedLabel, /^Missal text/, where);
      assert.deepEqual(row.claims, [['bible-text',
        'Bible text · ' + value.label + ' · not the Missal’s wording']], where);
      assert.ok(row.citations > 0, where);
    } else {
      assert.deepEqual(row.claims, [], where);
    }
  }
  assert.doesNotMatch(value.notice, /Bible reconstructions/, label + ' notice: ' + value.notice);
  assert.match(value.notice, new RegExp(mixed.length + ' cited Bible passages beside Missal texts'),
    label + ' notice: ' + value.notice);
}

async function claimsSurvivePrint(cdp) {
  await cdp.send('Emulation.setEmulatedMedia', { media: 'print' });
  try {
    return await evaluate(cdp, `[...document.querySelectorAll('[data-unit-claim]')].map(node => {
      const style = getComputedStyle(node);
      return style.display !== 'none' && style.visibility !== 'hidden' && node.getClientRects().length > 0;
    })`);
  } finally {
    await cdp.send('Emulation.setEmulatedMedia', { media: '' });
  }
}

async function metrics(cdp) {
  return evaluate(cdp, `(() => {
    const action = document.querySelector('.reader-actions');
    const reading = document.querySelector('#reader-document');
    const first = reading.querySelector('.proper, section');
    const box = (first || reading).getBoundingClientRect();
    const sample = reading.querySelector('.passage, .composed') || first || reading;
    const style = getComputedStyle(sample);
    const canvas = document.createElement('canvas'); const ctx = canvas.getContext('2d'); ctx.font = style.font;
    const unit = ctx.measureText('0').width || 8;
    const overflow = element => [element, ...element.querySelectorAll('*')].filter(row =>
      row.clientWidth > 0 && row.scrollWidth > row.clientWidth + 1).map(row => row.id || row.className || row.tagName);
    return {
      shellHeight: action.getBoundingClientRect().height,
      readingWidth: box.width,
      charactersPerLine: Math.round(box.width / unit),
      firstContentPosition: first ? first.getBoundingClientRect().top + scrollY : null,
      pageOverflow: document.documentElement.scrollWidth - document.documentElement.clientWidth,
      surfaceOverflow: [...document.querySelectorAll('dialog[open]')].flatMap(overflow),
      targets: [...action.querySelectorAll('button')].map(row => {
        const held = row.getBoundingClientRect(); return { width: held.width, height: held.height };
      }),
      resources: performance.getEntriesByType('resource').map(row => row.name),
      loadCounts: propersReaderDebug.loads,
      detailsBuilds: propersReaderDebug.detailsBuilds,
      layoutShift: (window.__triptychLayoutShifts || []).reduce((sum, row) => sum + row, 0),
      scrollY
    };
  })()`);
}

async function assertions(cdp, base) {
  await viewport(cdp, 393, 852);
  await candidate(cdp, base);

  await check('valid deep link uses the shared calm shell and reports typed material coverage', async () => {
    const value = await snapshot(cdp);
    const splitLoads = await evaluate(cdp, 'propersReaderDebug.loads');
    assert.equal(splitLoads['structure/propers/catalog/roman-1962.json'], 1);
    assert.equal(splitLoads['structure/propers/mass/roman-1962/advent-1.json'], 1);
    assert.equal(splitLoads['structure/propers/roman-1962.json'] || 0, 0);
    assert.equal(value.title, 'First Sunday of Advent', JSON.stringify(value));
    assert.equal(value.outcome, 'ready');
    // Held bodies do not establish target fidelity or exact Scripture wording.
    assert.equal(value.noticeHidden, false);
    assert.match(value.notice, /represented texts/);
    assert.equal(/Exact target wording remains incomplete/.test(value.notice),
      await latinExactIncomplete(cdp, 'roman-1962'), value.notice);
    assert.match(value.notice, /Bible reconstructions/);
    assert.deepEqual(value.semantic.coverage.map(row => [row.scope, row.completeness]),
      [['formulary:advent-1', 'partial']]);
    assert.equal(value.semantic.resolved.formulary, 'advent-1');
    // A date-free Advent formulary cannot resolve the Sunday/feria Alleluia.
    assert.equal(value.semantic.events.length, 9);
    assert.deepEqual(value.semantic.unresolvedChoices.map(row => row.id),
      ['proper-condition/roman-1962/advent-1/main/advent-1-alleluia-use']);
    assert.equal(await evaluate(cdp, 'location.pathname'), CURRENT);
    const semanticOrder = await evaluate(cdp, `(() => ({
      events: propersReaderDebug.semantic.events.filter(row => row.kind === 'proper').map(row => row.id),
      dom: [...document.querySelectorAll('#reader-document [data-semantic-event-id]')]
        .map(row => row.dataset.semanticEventId),
      contents: [...document.querySelectorAll('[data-reader-contents] [data-reader-location]')]
        .map(row => row.dataset.readerLocation)
    }))()`);
    assert.deepEqual(semanticOrder.dom, semanticOrder.events);
    assert.deepEqual(semanticOrder.contents, semanticOrder.dom);
    assert.equal(new Set(semanticOrder.dom).size, semanticOrder.dom.length);
    assert.deepEqual(await evaluate(cdp, `[...document.querySelectorAll('.reader-actions [data-reader-action]')].map(row => row.textContent.replace(/\\s+/g, ' ').trim())`),
      ['Browse', 'Contents', 'Mode Read', 'Study']);
    const measured = await metrics(cdp);
    const duplicateResources = measured.resources.filter((row, index, all) => all.indexOf(row) !== index);
    performanceReport = {
      candidateResourceCount: measured.resources.length,
      duplicateResources,
      manifestRequests: measured.resources.filter(row => /\/(bibles|index)\.json$/.test(row)).length,
      properStructureRequests: measured.resources.filter(row => /\/structure\/propers\/(?!index)[^/]+\.json$/.test(row)).length,
      properFragmentRequests: measured.resources.filter(row => /\/chapters\//.test(row)).length,
      initializationLayoutShift: measured.layoutShift,
      detailsLazy: measured.detailsBuilds === 0,
      selectedStructureLoadCount: measured.loadCounts['structure/propers/roman-1962.json']
    };

    // Typed material coverage, after the measurement above so that it counts
    // only the deep link: Claret's own Collect remains rights-withheld, so its
    // Latin is unavailable over a partial formulary. Vianney is now restored.
    await candidate(cdp, base, STATES.withheld);
    const withheld = await snapshot(cdp);
    assert.equal(withheld.outcome, 'ready');
    assert.equal(withheld.noticeHidden, false);
    assert.match(withheld.notice, /Latin Propers: 2\/3 represented texts/);
    assert.match(await evaluate(cdp, `[...document.querySelectorAll('#reader-document .proper')]
      .find(row => row.querySelector('.proper-name')?.textContent === 'Collect')?.textContent`),
      /Latin text unavailable/);
    assert.deepEqual(withheld.semantic.coverage.map(row => [row.scope, row.state]),
      [['formulary:s-antonii-mariae-claret-episcopi-confessoris', 'supported'],
        ['proper-original:la', 'unavailable']]);
  });

  await check('Proper search loads only on demand and links a titled incipit to its exact edition', async () => {
    await candidate(cdp, base, STATES.roman);
    assert.equal(await evaluate(cdp,
      `propersReaderDebug.loads['structure/propers/search/roman-1962.json'] || 0`), 0);
    await click(cdp, '[data-reader-action="browse"]');
    await evaluate(cdp, `(() => {
      document.querySelector('#proper-search-input').value = 'Spiritus Domini';
      document.querySelector('#proper-search-form').requestSubmit();
    })()`);
    await waitFor(cdp, `document.querySelectorAll('.proper-search-results li').length > 0`,
      '1962 search results');
    const found = await evaluate(cdp, `(() => ({
      status: document.querySelector('#proper-search-status').textContent,
      first: document.querySelector('.proper-search-results li').textContent,
      href: document.querySelector('.proper-search-results a').href,
      loads: propersReaderDebug.loads['structure/propers/search/roman-1962.json']
    }))()`);
    assert.match(found.status, /1962 Missal/);
    assert.match(found.first, /Spiritus Domini/);
    assert.match(found.first, /Represented non-Scripture Proper units only/);
    assert.match(found.href, /missal=roman-1962/);
    assert.match(found.href, /mass=pentecost/);
    assert.equal(found.loads, 1);
    assert.ok(!found.href.includes('Spiritus+Domini'));
  });

  await check('Proper search preserves all three All Souls forms and opens the chosen form', async () => {
    await candidate(cdp, base, STATES.missing);
    await evaluate(cdp, `(() => {
      document.querySelector('#proper-search-input').value = '11-02 Requiem';
      document.querySelector('#proper-search-form').requestSubmit();
    })()`);
    await waitFor(cdp, `document.querySelectorAll('.proper-search-results a').length >= 3`,
      'All Souls form results');
    const forms = await evaluate(cdp, `[...document.querySelectorAll('.proper-search-results a')]
      .filter(row => row.href.includes('commemoratione-omnium-fidelium-defunctorum'))
      .map(row => new URL(row.href).hash).map(hash => new URLSearchParams(hash.slice(1)).get('form'))`);
    assert.deepEqual(forms, ['first', 'second', 'third']);
    await evaluate(cdp, `[...document.querySelectorAll('.proper-search-results a')]
      .find(row => new URLSearchParams(new URL(row.href).hash.slice(1)).get('form') === 'second').click()`);
    await waitFor(cdp, `propersReaderDebug.ready && propersReaderDebug.semantic?.resolved?.form === 'second'`,
      'second All Souls Mass');
    assert.equal(await evaluate(cdp, 'location.pathname'), CURRENT);
    assert.equal(await evaluate(cdp,
      `new URLSearchParams(location.hash.slice(1)).get('form')`), 'second');
    assert.equal(await evaluate(cdp,
      `new URLSearchParams(location.hash.slice(1)).get('mode')`), 'read');
  });

  await check('Proper search states the inherited recension limit and rejects civil-date inference', async () => {
    await candidate(cdp, base, STATES.pre1955Trinity);
    await click(cdp, '[data-reader-action="browse"]');
    await evaluate(cdp, `(() => {
      document.querySelector('#proper-search-input').value = 'trinity';
      document.querySelector('#proper-search-form').requestSubmit();
    })()`);
    await waitFor(cdp, `document.querySelectorAll('.proper-search-results a').length > 0`,
      'pre-1955 search result');
    assert.match(await evaluate(cdp,
      `document.querySelector('#proper-search-caveat').textContent`), /Inherited material/);
    await evaluate(cdp, `(() => {
      document.querySelector('#proper-search-input').value = '2026-11-02';
      document.querySelector('#proper-search-form').requestSubmit();
    })()`);
    await waitFor(cdp, `document.querySelector('#proper-search-status').textContent.startsWith('No results')`,
      'scoped no-result message');
    assert.match(await evaluate(cdp,
      `document.querySelector('#proper-search-status').textContent`), /does not resolve civil dates/);
    assert.equal(await evaluate(cdp,
      `document.querySelectorAll('.proper-search-results a').length`), 0);
  });

  await check('Proper search re-scopes to a chosen missal and reflows at 320 pixels', async () => {
    await candidate(cdp, base, STATES.roman);
    await click(cdp, '[data-reader-action="browse"]');
    await select(cdp, '#reader-missal', 'postconciliar');
    await waitFor(cdp,
      `document.querySelector('#reader-formulary').disabled === false && ` +
      `document.querySelector('#reader-missal').value === 'postconciliar'`,
      'postconciliar Browse selection');
    await viewport(cdp, 320, 720);
    const width = await evaluate(cdp, `(() => ({
      page: document.documentElement.scrollWidth,
      viewport: innerWidth,
      input: document.querySelector('#proper-search-input').getBoundingClientRect().right
    }))()`);
    assert.ok(width.page <= width.viewport, JSON.stringify(width));
    assert.ok(width.input <= width.viewport, JSON.stringify(width));
    await evaluate(cdp, `(() => {
      document.querySelector('#proper-search-input').value = 'Transfiguration';
      document.querySelector('#proper-search-form').requestSubmit();
    })()`);
    await waitFor(cdp, `document.querySelectorAll('.proper-search-results a').length > 0`,
      'postconciliar search result');
    const href = await evaluate(cdp, `document.querySelector('.proper-search-results a').href`);
    assert.match(href, /missal=postconciliar/);
    assert.match(href, /mass=transfiguration-lord/);
    assert.ok(!href.includes('missal=roman-1962'));
    await viewport(cdp, 393, 852);
  });

  await check('form without exact formulary fails closed and is not canonicalized into Browse', async () => {
    await candidate(cdp, base, STATES.formWithoutMass);
    const value = await snapshot(cdp);
    assert.equal(value.outcome, 'invalid');
    assert.ok(value.error.some(row => row.path === 'form' && row.code === 'incomplete-explicit-identity'));
    assert.equal(await evaluate(cdp, 'location.pathname'), CANDIDATE);
    assert.equal(await evaluate(cdp,
      `new URLSearchParams(location.hash.slice(1)).get('form')`), 'vigil');
    assert.equal(await evaluate(cdp,
      `document.querySelector('#browse-surface').open`), false);
  });

  await check('source-authored form names survive choice, result identity, print, and focus', async () => {
    await candidate(cdp, base, STATES.romanChristmasForms);
    let value = await snapshot(cdp);
    assert.equal(value.outcome, 'unresolved');
    assert.deepEqual(await evaluate(cdp,
      `[...document.querySelectorAll('.proper-form-choice button')].map(row => row.textContent.trim())`),
    ['Ad primam Missam in nocte', 'Ad secundam Missam in aurora', 'Ad tertiam Missam in die']);
    await cdp.send('Emulation.setEmulatedMedia', { media: 'print' });
    assert.match(await evaluate(cdp, `document.querySelector('.proper-form-summary').textContent`),
      /Ad primam Missam in nocte.*Ad secundam Missam in aurora.*Ad tertiam Missam in die/);
    await cdp.send('Emulation.setEmulatedMedia', { media: 'screen' });
    await click(cdp, '.proper-form-choice button');
    await waitFor(cdp,
      `propersReaderDebug.ready && propersReaderDebug.state.form === 'night'`,
      'source-authored form navigation');
    value = await snapshot(cdp);
    assert.match(value.meta, /Form: Ad primam Missam in nocte/);
    assert.match(value.documentTitle, /Ad primam Missam in nocte/);
    assert.equal(await evaluate(cdp, `document.activeElement.id`), 'formulary-title');
    await cdp.send('Emulation.setEmulatedMedia', { media: 'print' });
    assert.match(await evaluate(cdp, `document.querySelector('#formulary-meta').textContent`),
      /Form: Ad primam Missam in nocte/);
    await cdp.send('Emulation.setEmulatedMedia', { media: 'screen' });
    await click(cdp, '[data-reader-action="browse"]');
    const alternateBible = await evaluate(cdp, `(() => {
      const select = document.querySelector('#reader-bible');
      return [...select.options].find(row => row.value && row.value !== select.value)?.value || '';
    })()`);
    assert.ok(alternateBible, 'Browse has no alternate Bible with which to test form retention');
    await select(cdp, '#reader-bible', alternateBible);
    await click(cdp, '#browse-form .surface-apply');
    await waitFor(cdp,
      `propersReaderDebug.ready && propersReaderDebug.state.form === 'night' && ` +
      `propersReaderDebug.state.bible.id === ${JSON.stringify(alternateBible)}`,
      'form retention after Bible change');
    assert.equal(await evaluate(cdp,
      `new URLSearchParams(location.hash.slice(1)).get('form')`), 'night');
    assert.match((await snapshot(cdp)).meta, /Form: Ad primam Missam in nocte/);
  });

  await check('pre-1955 coverage, inheritance, and departures remain visible and print-safe', async () => {
    await candidate(cdp, base, STATES.pre1955Advent);
    assert.equal((await snapshot(cdp)).outcome, 'invalid');
    assert.match(await evaluate(cdp, 'propersReaderDebug.error[0].message'),
      /foreign-source Proper applicability.*source condition remains unresolved/);
    await candidate(cdp, base, STATES.pre1955Trinity);
    let value = await snapshot(cdp);
    assert.equal(value.sourceHidden, false);
    assert.match(value.source, /Recension coverage: Structural-only finding aid/);
    assert.match(value.source, /Proper text source: .*1962.*inherited uncollated/i);
    assert.match(value.notice, /structural-only finding aid/i);
    assert.match(value.notice, /inherited material.*remains uncollated/i);

    await candidate(cdp, base, STATES.pre1955Palm);
    value = await snapshot(cdp);
    assert.match(value.source, /Departure: Replaced/);
    assert.match(value.source, /Also: Renamed/);
    assert.match(value.source, /Reslotted/);

    await candidate(cdp, base, STATES.pre1955Supper);
    value = await snapshot(cdp);
    assert.match(value.source, /inherited uncollated/i);
    assert.match(value.source, /Departure: Moved/);
    await cdp.send('Emulation.setEmulatedMedia', { media: 'print' });
    assert.notEqual(await evaluate(cdp,
      `getComputedStyle(document.querySelector('#formulary-source')).display`), 'none');
    await cdp.send('Emulation.setEmulatedMedia', { media: 'screen' });

    await candidate(cdp, base, STATES.roman);
    value = await snapshot(cdp);
    assert.equal(value.sourceHidden, true);
    assert.equal(value.source, '');
  });

  await check('semantic location must exist in rendered inventory and valid location restores exactly', async () => {
    await candidate(cdp, base, STATES.invalidLocation);
    let value = await snapshot(cdp);
    assert.equal(value.outcome, 'invalid');
    assert.ok(value.error.some(row => row.path === 'location' && row.code === 'invalid-semantic-location'));
    assert.equal(await evaluate(cdp, 'location.pathname'), CANDIDATE);
    assert.equal(await evaluate(cdp,
      `new URLSearchParams(location.hash.slice(1)).get('location')`),
    'proper/roman-1962/advent-1/999');

    await candidate(cdp, base, STATES.validLocation);
    value = await snapshot(cdp);
    assert.equal(value.outcome, 'ready');
    assert.deepEqual(value.state.semanticLocation,
      { eventId: 'proper/roman-1962/advent-1/003' });
    assert.equal(await evaluate(cdp, 'location.pathname'), CURRENT);
    assert.equal(await evaluate(cdp,
      `document.querySelector('[data-semantic-event-id="proper/roman-1962/advent-1/003"]') !== null`),
      true);
  });

  await check('Contents movement replaces canonical semantic location and focuses the result', async () => {
    await candidate(cdp, base, STATES.roman);
    await click(cdp, '[data-reader-action="contents"]');
    const wanted = await evaluate(cdp, `(() => {
      const row = document.querySelectorAll('[data-reader-contents] [data-reader-location]')[2];
      if (!row) throw new Error('third Contents location is absent');
      const id = row.dataset.readerLocation; row.click(); return id;
    })()`);
    assert.equal(await evaluate(cdp,
      `new URLSearchParams(location.hash.slice(1)).get('location')`), wanted);
    assert.equal(await evaluate(cdp,
      `document.activeElement.dataset.semanticEventId`), wanted);
    assert.deepEqual(await evaluate(cdp, `propersReaderDebug.state.semanticLocation`),
      { eventId: wanted });
  });

  await check('cycle branches keep typed absences isolated and held translations reachable', async () => {
    const cases = [
      [STATES.cycleAUntranslated, 'rights-restricted',
        /English translation unavailable for this cycle: not publishable here \(its use is rights restricted\)\. The Latin original is shown\./,
        'A Latin sibling sentinel', 'C Latin safe sibling'],
      [STATES.cycleCUntranslated, 'unavailable',
        /English translation unavailable for this cycle: [a-z ]+\. The Latin original is shown\./,
        'C Latin safe sibling', 'A Latin sibling sentinel']
    ];
    for (const [state, unavailable, notice, present, absent] of cases) {
      await candidate(cdp, base, state, CYCLE_UNTRANSLATED_DATA);
      const snapshotValue = await snapshot(cdp);
      assert.equal(snapshotValue.outcome, 'ready', JSON.stringify(snapshotValue));
      const row = await evaluate(cdp, `(() => {
        const event = propersReaderDebug.semantic.events.find(one => one.editionSlotLabel === 'Collect');
        const node = document.querySelector('[data-semantic-event-id="' + event.id + '"]');
        return { selected: event.selected, text: node.textContent.replace(/\\s+/g, ' ').trim() };
      })()`);
      assert.equal(row.selected.unavailableState, unavailable);
      assert.equal(row.selected.missing, true);
      assert.equal(row.selected.text, null);
      assert.match(row.text, notice);
      // The semantic selection stays the requested English absence; the held
      // Latin original of the same cycle remains visible beside it (C2 G10).
      assert.match(row.text, new RegExp(present));
      assert.doesNotMatch(row.text, new RegExp(absent));
    }

    await candidate(cdp, base, STATES.cycleBHeldEnglish, CYCLE_UNTRANSLATED_DATA);
    const held = await evaluate(cdp, `(() => {
      const event = propersReaderDebug.semantic.events.find(one => one.editionSlotLabel === 'Collect');
      const node = event && document.querySelector('[data-semantic-event-id="' + event.id + '"]');
      const composed = node && node.querySelector('.composed');
      return {
        outcome: propersReaderDebug.outcome,
        text: composed && composed.textContent.replace(/\\s+/g, ' ').trim(),
        lang: composed && composed.lang
      };
    })()`);
    assert.equal(held.outcome, 'ready');
    assert.match(held.text, /B held English without a Latin body/);
    assert.equal(held.lang, 'en');
  });

  await check('held English remains readable when the corresponding Latin body is unavailable', async () => {
    await candidate(cdp, base, STATES.englishWithoutLatinBody);
    const value = await snapshot(cdp);
    assert.equal(value.outcome, 'ready', JSON.stringify(value));
    assert.match(value.source,
      /Translation witness: .*The New Roman Missal/);
    assert.match(value.source, /Rights: Public Domain/);
    const row = await evaluate(cdp, `(async () => {
      const T = window.Triptych;
      const structure = await T.loadJSON('structure/propers/roman-1962.json');
      const event = propersReaderDebug.semantic.events.find(one =>
        one.kind === 'proper' && one.editionSlotLabel === 'Postcommunion');
      if (!event) throw new Error('Postcommunion semantic event is absent');
      const units = T.selectedCoverageUnits({ events: [event] }, structure)
        .filter(unit => unit.component !== 'scripture');
      if (units.length !== 1) throw new Error('Postcommunion body coverage is not unique');
      const state = lang => units[0].languages.find(row => row.lang === lang)?.availability;
      const node = document.querySelector('[data-semantic-event-id="' + event.id + '"]');
      const composed = node && node.querySelector('.composed');
      return {
        text: node && node.textContent.replace(/\\s+/g, ' ').trim(),
        composed: composed && composed.textContent.replace(/\\s+/g, ' ').trim(),
        lang: composed && composed.lang, source: event.selected.sourceId,
        latinAvailability: state('la'), englishAvailability: state('en')
      };
    })()`);
    assert.equal(row.latinAvailability, 'unresolved');
    assert.equal(row.englishAvailability, 'available');
    assert.equal(row.source, 'edition.francis-xavier-lasance.the-new-roman-missal.benziger-revised-1945');
    assert.match(row.composed, /Through this holy nourishment which we have consumed/);
    assert.equal(row.lang, 'en');
    assert.doesNotMatch(row.text, /Latin text unavailable|No English body is held/i);
  });

  await check('C2 G9: Bible-reconstructed units carry one quiet claim, in Read and print', async () => {
    await candidate(cdp, base, STATES.postPentecostDay);
    assert.equal((await snapshot(cdp)).outcome, 'ready');
    assertBibleClaims(await bibleClaimAudit(cdp, 'propersReaderDebug', 'postconciliar'),
      'Propers postconciliar Pentecost (day)');
    const printed = await claimsSurvivePrint(cdp);
    assert.ok(printed.length > 0 && printed.every(Boolean), JSON.stringify(printed));
  });

  await check('C2 G9 follow-up: Propers labels mixed units\' passages as Bible text, not a reconstruction', async () => {
    await candidate(cdp, base, STATES.romanPentecost);
    assert.equal((await snapshot(cdp)).outcome, 'ready');
    assertMixedClaims(await mixedClaimAudit(cdp, 'roman-1962', 'pentecost'), 'Propers 1962 Pentecost');
    const printed = await claimsSurvivePrint(cdp);
    assert.ok(printed.length > 0 && printed.every(Boolean), JSON.stringify(printed));
  });

  await check('C2 G14: Propers renders checked stanzas and the genuflection rubric in Latin, English and print', async () => {
    for (const [state, lang] of [[STATES.romanPentecost, 'la'], [STATES.romanPentecostEnglish, 'en']]) {
      await candidate(cdp, base, state);
      assert.equal((await snapshot(cdp)).outcome, 'ready');
      assertTextStructure(await textStructureAudit(cdp, 'roman-1962', 'pentecost'), lang, 'Propers 1962 Pentecost ' + lang);
    }
    await cdp.send('Emulation.setEmulatedMedia', { media: 'print' });
    try {
      const printed = await evaluate(cdp, `(() => {
        const group = document.querySelector('#reader-document .composed-stanzas');
        return {
          stanzas: [...group.querySelectorAll(':scope > .stanza')].map(node => node.getClientRects().length > 0),
          section: getComputedStyle(group.closest('section.proper')).breakInside
        };
      })()`);
      assert.ok(printed.stanzas.length > 1 && printed.stanzas.every(Boolean), JSON.stringify(printed));
      assert.equal(printed.section, 'auto');
    } finally {
      await cdp.send('Emulation.setEmulatedMedia', { media: '' });
    }
  });

  await check('C2 G14: copying from Propers keeps ℣, rubric and stanza breaks and drops hidden labels', async () => {
    const before = await evaluate(cdp, '({ width: innerWidth, height: innerHeight })');
    await viewport(cdp, 1440, 900);
    await cdp.send('Browser.grantPermissions', {
      origin: base, permissions: ['clipboardReadWrite', 'clipboardSanitizedWrite']
    });
    await cdp.send('Emulation.setFocusEmulationEnabled', { enabled: true });
    try {
      for (const state of [STATES.romanPentecost, STATES.romanPentecostEnglish]) {
        await candidate(cdp, base, state);
        await cdp.send('Page.bringToFront');
        for (const name of ['Introit', 'Alleluia', 'Sequence']) {
          const row = await copiedProper(cdp, name);
          assertCopied(row, 'Propers ' + state + ' ' + name);
          if (name === 'Alleluia') assert.ok(row.glyphs > 0 && row.rubrics.length === 1, JSON.stringify(row));
          if (name === 'Sequence') assert.ok(row.stanzas.length > 1, JSON.stringify(row));
        }
      }
    } finally {
      await cdp.send('Emulation.setFocusEmulationEnabled', { enabled: false });
      await cdp.send('Browser.resetPermissions', {});
      await viewport(cdp, before.width, before.height);
    }
  });

  await check('source alternatives remain one atomic form-exact choice in source order', async () => {
    await candidate(cdp, base, STATES.postPentecostDay);
    const value = await evaluate(cdp, `(() => {
      const semantic = propersReaderDebug.semantic;
      const events = semantic.events;
      const choice = events.find(row => row.kind === 'proper-choice');
      const semanticIds = events.map(row => row.id);
      return {
        outcome: propersReaderDebug.outcome,
        formulary: semantic.resolved.formulary,
        form: semantic.resolved.form,
        semanticIds,
        domIds: [...document.querySelectorAll('#reader-document [data-semantic-event-id]')]
          .map(row => row.dataset.semanticEventId),
        choice: choice && {
          id: choice.id, group: choice.group, selection: choice.selection,
          options: choice.options.map(option => ({
            id: option.id, events: option.events.map(row => row.id)
          }))
        },
        unresolved: semantic.unresolvedChoices.map(row => ({
          id: row.id, options: row.options.map(option => option.id)
        })),
        domChoice: {
          group: document.querySelector('.proper-choice')?.dataset.properChoice || null,
          state: document.querySelector('.proper-choice')?.dataset.choiceState || null,
          options: [...document.querySelectorAll('.proper-choice-option')]
            .map(row => [row.dataset.properChoiceOption, row.dataset.choiceStatus]),
          members: [...document.querySelectorAll('.proper-choice-member')]
            .map(row => row.dataset.properChoiceMemberEvent),
          note: document.querySelector('.proper-choice-note')?.textContent || ''
        }
      };
    })()`);
    const expectedIds = [
      'proper-choice/postconciliar/pentecost/day/entrance-antiphon',
      ...[17, 18, 19, 21, 22, 24, 25, 26].map(index =>
        'proper/postconciliar/pentecost/' + String(index).padStart(3, '0'))
    ];
    assert.equal(value.outcome, 'ready');
    assert.equal(value.formulary, 'pentecost');
    assert.equal(value.form, 'day');
    assert.deepEqual(value.semanticIds, expectedIds);
    assert.deepEqual(value.domIds, expectedIds);
    assert.deepEqual(value.choice, {
      id: 'proper-choice/postconciliar/pentecost/day/entrance-antiphon',
      group: 'entrance-antiphon',
      selection: { state: 'required', option: null },
      options: [
        { id: 'spiritus-domini', events: ['proper/postconciliar/pentecost/015'] },
        { id: 'caritas-dei', events: ['proper/postconciliar/pentecost/016'] }
      ]
    });
    assert.deepEqual(value.unresolved, [
      { id: 'proper-choice/postconciliar/pentecost/day/pentecost-day-readings',
        options: ['common', 'year-b-optional', 'year-c-optional'] },
      { id: value.choice.id, options: ['spiritus-domini', 'caritas-dei'] }
    ]);
    assert.deepEqual(value.domChoice, {
      group: 'entrance-antiphon', state: 'required',
      options: [['spiritus-domini', 'available'], ['caritas-dei', 'available']],
      members: ['proper/postconciliar/pentecost/015', 'proper/postconciliar/pentecost/016'],
      note: 'The source appoints one of these alternatives here. None is selected; the option groups below are not cumulative.'
    });
    assert.ok(!value.semanticIds.includes('proper/postconciliar/pentecost/020'));
    assert.ok(!value.semanticIds.includes('proper/postconciliar/pentecost/023'));
    assert.ok(value.semanticIds.indexOf('proper/postconciliar/pentecost/021') <
      value.semanticIds.indexOf('proper/postconciliar/pentecost/022'));

    const candidateProjection = await evaluate(cdp, 'propersReaderDebug.semantic');
    await current(cdp, base, STATES.postPentecostDay);
    assert.deepEqual(await evaluate(cdp, 'propersReaderDebug.semantic'), candidateProjection);
  });
  if (process.env.TRIPTYCH_P0_ONLY === '1') return;

  await check('C6 resolved 1962 Read uses one Mass payload with form and witness fidelity', async () => {
    for (const [route, mass, form] of [
      [STATES.romanChristmasNight, 'nativitate-domini-octave', 'night'],
      [STATES.englishWitness, 'commemoratione-omnium-fidelium-defunctorum', 'first']
    ]) {
      await candidate(cdp, base, route);
      const value = await evaluate(cdp, `({ outcome: propersReaderDebug.outcome,
        state: propersReaderDebug.state,
        semantic: propersReaderDebug.semantic,
        loads: propersReaderDebug.loads,
        dom: [...document.querySelectorAll('#reader-document [data-semantic-event-id]')]
          .map(row => row.dataset.semanticEventId) })`);
      assert.equal(value.outcome, 'ready');
      assert.equal(value.semantic.resolved.formulary, mass);
      assert.equal(value.semantic.resolved.form, form);
      assert.equal(value.loads['structure/propers/catalog/roman-1962.json'], 1);
      assert.equal(value.loads[`structure/propers/mass/roman-1962/${mass}.json`], 1);
      assert.equal(value.loads['structure/propers/roman-1962.json'] || 0, 0);
      assert.deepEqual(value.dom, value.semantic.events.map(row => row.id));
      if (route === STATES.englishWitness) {
        assert.equal(value.state.languages.translationWitness, MULTIPLE_TRANSLATION_WITNESS);
      }
    }
  });

  await check('C6 malformed split Mass falls back to the monolith with identical Read evidence', async () => {
    await candidate(cdp, base, STATES.roman);
    const baseline = await snapshot(cdp);
    await candidate(cdp, base, STATES.roman, BAD_SPLIT_DATA);
    const fallback = await snapshot(cdp);
    const loads = await evaluate(cdp, 'propersReaderDebug.loads');
    assert.equal(fallback.outcome, 'ready');
    assert.deepEqual(fallback.semantic, baseline.semantic);
    assert.deepEqual(fallback.texts, baseline.texts);
    assert.equal(fallback.notice, baseline.notice);
    assert.equal(loads['structure/propers/catalog/roman-1962.json'], 1);
    assert.equal(loads['structure/propers/mass/roman-1962/advent-1.json'], 1);
    assert.equal(loads['structure/propers/roman-1962.json'], 1);
  });

  await check('C6 bounded Missal uses one Mass while language, form, and source dependencies keep the monolith', async () => {
    await candidate(cdp, base, STATES.romanTrinity + '&mode=missal');
    const missal = await evaluate(cdp, `({ outcome: propersReaderDebug.outcome,
      state: propersReaderDebug.state, loads: propersReaderDebug.loads,
      ordinary: document.querySelectorAll('#reader-document .ordinary-element').length })`);
    assert.equal(missal.outcome, 'ready');
    assert.equal(missal.state.requestedMode, 'missal');
    assert.equal(missal.state.options.ordinary, true);
    assert.equal(missal.loads['structure/propers/catalog/roman-1962.json'], 1);
    assert.equal(missal.loads['structure/propers/mass/roman-1962/trinity.json'], 1);
    assert.equal(missal.loads['structure/propers/roman-1962.json'] || 0, 0);
    assert.equal(missal.loads['structure/ordinary/roman-1962.json'], 1);
    assert.ok(missal.ordinary > 0);
    const cases = [
      [STATES.missing, 'browse'],
      [STATES.romanPentecostEnglish + '&mode=missal', 'ready'],
      [STATES.roman + '&mode=study', 'ready'],
      [STATES.romanTrinity + '&mode=compare&compare=oration-language&peer-orations=en', 'ready'],
      [STATES.roman + '&mode=missal', 'ready'],
      [STATES.romanChristmasForms, 'unresolved'],
      [STATES.romanChristmasForms + '&mode=missal', 'unresolved'],
      [STATES.romanChristmasNight + '&mode=missal', 'ready'],
      [hash({ missal: 'roman-1962', type: 'sanctoral', mass: 'comm-s-telesphori-papae-martyris', bible: 'douay-rheims', orations: 'la' }), 'ready']
    ];
    for (const [route, outcome] of cases) {
      await candidate(cdp, base, route);
      const value = await evaluate(cdp, `({ outcome: propersReaderDebug.outcome,
        loads: propersReaderDebug.loads })`);
      assert.equal(value.outcome, outcome);
      assert.equal(value.loads['structure/propers/roman-1962.json'], 1);
    }
  });

  await check('C5 Propers Compare independently resolves two languages on one date-free formulary', async () => {
    const route = STATES.romanTrinity + '&mode=compare&compare=oration-language&peer-orations=en';
    await candidate(cdp, base, route);
    const value = await evaluate(cdp, `(() => ({
      outcome: propersReaderDebug.outcome,
      state: propersReaderDebug.state,
      semantic: propersReaderDebug.semantic,
      dom: [...document.querySelectorAll('#reader-document [data-semantic-event-id]')]
        .map(row => row.dataset.semanticEventId),
      contents: [...document.querySelectorAll('[data-reader-contents] [data-reader-location]')]
        .map(row => row.dataset.readerLocation),
      sides: [...document.querySelectorAll('#reader-document .compare-unit')]
        .map(row => [...row.querySelectorAll('.compare-side')]
          .map(side => [side.dataset.compareSide, side.dataset.compareStatus])),
      ordinaryLoads: propersReaderDebug.loads['structure/ordinary/roman-1962.json'] || 0,
      hash: location.hash
    }))()`);
    assert.equal(value.outcome, 'ready');
    assert.equal(value.state.requestedMode, 'compare');
    assert.equal(value.state.civilDate, null);
    assert.equal(value.semantic.anchor.correspondingFormulary, 'trinity');
    assert.equal(value.semantic.calendarResults, null);
    assert.equal(value.semantic.units.length, 10);
    assert.deepEqual(value.semantic.sides.map(row => row.id), ['la', 'en']);
    assert.deepEqual(value.dom, value.semantic.units.map(row => 'compare/proper/' + row.semanticSlot));
    assert.deepEqual(value.contents, value.dom);
    assert.ok(value.sides.every(row => row.length === 2));
    assert.deepEqual(value.semantic.units.find(row => row.semanticSlot === 'collect').sides
      .map(row => row.status), ['text-held', 'text-held']);
    assert.equal(value.ordinaryLoads, 0);
    assert.match(value.hash, /compare=oration-language/);
    assert.match(value.hash, /peer-orations=en/);
    const projection = value.semantic;
    await current(cdp, base, route);
    assert.deepEqual(await evaluate(cdp, 'propersReaderDebug.semantic'), projection);

    // Trinity and Ignatius hold checked English. Lent I's Collect retains its
    // exact Latin body and ledgered English gap, preserving the unavailable-side
    // contract alongside the complete Trinity parity checks above.
    const unavailableRoute = new URLSearchParams(STATES.englishNone.slice(1));
    unavailableRoute.set('mass', 'lent-1');
    unavailableRoute.set('type', 'seasonal');
    unavailableRoute.set('orations', 'la');
    unavailableRoute.set('mode', 'compare');
    unavailableRoute.set('compare', 'oration-language');
    unavailableRoute.set('peer-orations', 'en');
    await candidate(cdp, base, '#' + unavailableRoute);
    const unavailable = await evaluate(cdp, `({
      outcome: propersReaderDebug.outcome,
      state: propersReaderDebug.state,
      semantic: propersReaderDebug.semantic,
      sides: [...document.querySelectorAll('#reader-document [data-semantic-event-id="compare/proper/collect"] .compare-side')]
        .map(side => side.dataset.compareStatus)
    })`);
    assert.equal(unavailable.outcome, 'ready', JSON.stringify(unavailable));
    assert.equal(unavailable.state.civilDate, null);
    assert.equal(unavailable.semantic.anchor.correspondingFormulary,
      'lent-1');
    assert.deepEqual(unavailable.semantic.units.find(row => row.semanticSlot === 'collect').sides
      .map(row => row.status), ['text-held', 'text-unavailable']);
    assert.deepEqual(unavailable.sides, ['text-held', 'text-unavailable']);
  });

  await check('C5 Propers Compare controls retain the Proper location on return to Read', async () => {
    await candidate(cdp, base, STATES.romanTrinity + '&location=proper%2Froman-1962%2Ftrinity%2F002');
    await waitFor(cdp,
      `window.TriptychReaderShell && document.querySelector('#reader-document [data-semantic-location="proper/roman-1962/trinity/002"]')?.getBoundingClientRect().top <= 300`,
      'initial Proper location scroll');
    await click(cdp, '[data-reader-action="mode"]');
    await click(cdp, '[data-mode="compare"]');
    await select(cdp, '#reader-compare-orations', 'en');
    await click(cdp, '#compare-setup .surface-apply');
    await waitFor(cdp, `propersReaderDebug.ready && propersReaderDebug.state?.requestedMode === 'compare'`, 'Propers Compare mode');
    const compared = await evaluate(cdp, `({
      outcome: propersReaderDebug.outcome,
      location: propersReaderDebug.state.semanticLocation?.eventId,
      hash: location.hash,
      active: document.activeElement?.dataset.readerAction
    })`);
    assert.equal(compared.outcome, 'ready');
    assert.equal(compared.location, 'compare/proper/collect');
    assert.match(compared.hash, /location=compare%2Fproper%2Fcollect/);
    assert.equal(compared.active, 'mode');
    await waitFor(cdp,
      `document.querySelector('#reader-document [data-semantic-location="compare/proper/collect"]')?.getBoundingClientRect().top <= 300`,
      'Compare location scroll');
    await click(cdp, '[data-reader-action="mode"]');
    await click(cdp, '[data-mode="read"]');
    await waitFor(cdp, `propersReaderDebug.ready && propersReaderDebug.state?.requestedMode === 'read'`, 'Read return from Compare');
    const read = await evaluate(cdp, `({
      outcome: propersReaderDebug.outcome,
      location: propersReaderDebug.state.semanticLocation?.eventId,
      hash: location.hash,
      active: document.activeElement?.dataset.readerAction
    })`);
    assert.equal(read.outcome, 'ready');
    assert.equal(read.location, 'proper/roman-1962/trinity/002');
    assert.doesNotMatch(read.hash, /(?:compare|peer-orations)=/);
    assert.equal(read.active, 'mode');
  });

  await check('C5 Propers Compare rejects absent locations and unresolved source choices', async () => {
    await candidate(cdp, base, STATES.romanTrinity +
      '&mode=compare&compare=oration-language&peer-orations=en&location=compare%2Fproper%2Fnot-held');
    assert.equal(await evaluate(cdp, 'propersReaderDebug.outcome'), 'invalid');
    assert.equal(await evaluate(cdp, 'propersReaderDebug.error?.[0]?.code'), 'invalid-semantic-location');
    await candidate(cdp, base, STATES.postPentecostDay +
      '&mode=compare&compare=oration-language&peer-orations=en');
    assert.equal(await evaluate(cdp, 'propersReaderDebug.outcome'), 'invalid');
    assert.equal(await evaluate(cdp, 'propersReaderDebug.error?.[0]?.code'), 'unsupported-comparison');
    await candidate(cdp, base, STATES.roman +
      '&mode=compare&compare=oration-language&peer-orations=en');
    assert.equal(await evaluate(cdp, 'propersReaderDebug.error?.[0]?.code'), 'unsupported-comparison');
  });

  await check('C5 Propers Study keeps Read source text and event identities beside date-free apparatus', async () => {
    await candidate(cdp, base, STATES.roman);
    const readText = await evaluate(cdp,
      `[...document.querySelectorAll('#reader-document .proper')].map(row => row.textContent)`);
    const route = STATES.roman + '&mode=study&location=proper%2Froman-1962%2Fadvent-1%2F002';
    await candidate(cdp, base, route);
    const study = await evaluate(cdp, `(() => ({
      outcome: propersReaderDebug.outcome,
      state: propersReaderDebug.state,
      dom: [...document.querySelectorAll('#reader-document [data-semantic-event-id]')]
        .map(row => row.dataset.semanticEventId),
      contents: [...document.querySelectorAll('[data-reader-contents] [data-reader-location]')]
        .map(row => row.dataset.readerLocation),
      text: [...document.querySelectorAll('#reader-document .proper')].map(row => {
        const source = row.cloneNode(true);
        source.querySelectorAll('.study-event').forEach(note => note.remove());
        return source.textContent;
      }),
      notes: [...document.querySelectorAll('#reader-document .study-event')]
        .map(row => row.dataset.studyEventId),
      dateAbsence: document.querySelector('.study-date-absence')?.textContent || '',
      ordinaryNodes: document.querySelectorAll('#reader-document .ordinary-element').length,
      title: document.title,
      hash: location.hash
    }))()`);
    assert.equal(study.outcome, 'ready');
    assert.equal(study.state.requestedMode, 'study');
    assert.equal(study.state.civilDate, null);
    assert.equal(study.state.semanticLocation.eventId, 'proper/roman-1962/advent-1/002');
    assert.deepEqual(study.text, readText);
    assert.deepEqual(study.dom, study.contents);
    assert.deepEqual(study.notes, study.dom);
    assert.match(study.dateAbsence, /date-independent; no calendar result/);
    assert.equal(study.ordinaryNodes, 0);
    assert.match(study.title, /Study/);
    assert.match(study.hash, /mode=study/);
    await cdp.send('Emulation.setEmulatedMedia', { media: 'print' });
    const print = await evaluate(cdp, `({
      text: getComputedStyle(document.querySelector('#reader-document .proper')).display,
      apparatus: getComputedStyle(document.querySelector('#reader-document .study-event')).display
    })`);
    assert.notEqual(print.text, 'none');
    assert.notEqual(print.apparatus, 'none');
    const pdf = await cdp.send('Page.printToPDF', { printBackground: true });
    assert.ok(Buffer.from(pdf.data, 'base64').length > 1000);
    await cdp.send('Emulation.setEmulatedMedia', { media: 'screen' });
    await current(cdp, base, route);
    assert.deepEqual(await evaluate(cdp,
      `[...document.querySelectorAll('#reader-document [data-semantic-event-id]')].map(row => row.dataset.semanticEventId)`), study.dom);
  });

  await check('C5 Propers Study mode changes preserve locations and latent Ordinary language', async () => {
    const proper = 'proper/roman-1962/pentecost/001';
    await candidate(cdp, base, STATES.romanPentecost + '&mode=missal&ordinary-lang=la&location=' +
      encodeURIComponent(proper));
    await waitFor(cdp,
      `document.querySelector('#reader-document [data-semantic-location="${proper}"]')?.getBoundingClientRect().top <= 300`,
      'Missal Proper location scroll');
    await click(cdp, '[data-reader-action="study"]');
    await waitFor(cdp, `propersReaderDebug.ready && propersReaderDebug.state?.requestedMode === 'study'`, 'Study mode');
    const studied = await evaluate(cdp, `({ outcome: propersReaderDebug.outcome,
      location: propersReaderDebug.state.semanticLocation?.eventId,
      ordinaryLanguage: propersReaderDebug.state.languages.ordinary,
      ordinaryNodes: document.querySelectorAll('#reader-document .ordinary-element').length,
      active: document.activeElement?.dataset.readerAction, hash: location.hash })`);
    assert.equal(studied.outcome, 'ready');
    assert.equal(studied.location, proper);
    assert.equal(studied.ordinaryLanguage, 'la');
    assert.equal(studied.ordinaryNodes, 0);
    assert.equal(studied.active, 'study');
    assert.match(studied.hash, /ordinary-lang=la/);
    await waitFor(cdp,
      `document.querySelector('#reader-document [data-semantic-location="${proper}"]')?.getBoundingClientRect().top <= 300`,
      'Study Proper location scroll');
    await click(cdp, '[data-reader-action="mode"]');
    await click(cdp, '[data-mode="read"]');
    await waitFor(cdp, `propersReaderDebug.ready && propersReaderDebug.state?.requestedMode === 'read'`, 'Read return from Study');
    assert.equal(await evaluate(cdp, 'propersReaderDebug.state.semanticLocation?.eventId'), proper);
    await candidate(cdp, base, STATES.romanTrinity +
      '&mode=compare&compare=oration-language&peer-orations=en&location=compare%2Fproper%2Fcollect');
    await waitFor(cdp,
      `document.querySelector('#reader-document [data-semantic-location="compare/proper/collect"]')?.getBoundingClientRect().top <= 300`,
      'Compare Collect location scroll');
    await click(cdp, '[data-reader-action="mode"]');
    await click(cdp, '[data-mode="study"]');
    await waitFor(cdp, `propersReaderDebug.ready && propersReaderDebug.state?.requestedMode === 'study'`, 'Study from Compare');
    assert.equal(await evaluate(cdp, 'propersReaderDebug.state.semanticLocation?.eventId'),
      'proper/roman-1962/trinity/002');
  });

  await check('C5 Propers Study rejects absent locations and annotates unresolved source choices', async () => {
    await candidate(cdp, base, STATES.roman + '&mode=study&location=study%2Fevent%2Fnot-held');
    assert.equal(await evaluate(cdp, 'propersReaderDebug.outcome'), 'invalid');
    assert.equal(await evaluate(cdp, 'propersReaderDebug.error?.[0]?.code'), 'invalid-semantic-location');
    await candidate(cdp, base, STATES.postPentecostDay + '&mode=study');
    const value = await evaluate(cdp, `({ outcome: propersReaderDebug.outcome,
      choices: propersReaderDebug.semantic?.unresolvedChoices || [],
      choiceNodes: document.querySelectorAll('#reader-document .proper-choice').length,
      choiceNotes: document.querySelectorAll('#reader-document .proper-choice .study-event').length,
      ids: [...document.querySelectorAll('#reader-document [data-semantic-event-id]')]
        .map(row => row.dataset.semanticEventId) })`);
    assert.equal(value.outcome, 'ready');
    assert.ok(value.choices.length);
    assert.equal(value.choiceNodes, 1);
    assert.equal(value.choiceNotes, 1);
    assert.equal(new Set(value.ids).size, value.ids.length);
  });

  await check('C5 1962 Propers Missal seats the production Ordinary with exact event and Contents order', async () => {
    await candidate(cdp, base, STATES.romanPentecost + '&mode=missal');
    const value = await evaluate(cdp, `(() => ({
      outcome: propersReaderDebug.outcome,
      state: propersReaderDebug.state,
      events: propersReaderDebug.semantic?.events || [],
      calendarResult: propersReaderDebug.semantic?.calendarResult,
      dom: [...document.querySelectorAll('#reader-document [data-semantic-event-id]')]
        .map(row => row.dataset.semanticEventId),
      contents: [...document.querySelectorAll('[data-reader-contents] [data-reader-location]')]
        .map(row => row.dataset.readerLocation),
      ordinaryCount: document.querySelectorAll('#reader-document .ordinary-element').length,
      properCount: document.querySelectorAll('#reader-document > .ordinary-frame > .proper:not(.ordinary-element)').length,
      ordinaryLoads: propersReaderDebug.loads['structure/ordinary/roman-1962.json'] || 0,
      hash: location.hash
    }))()`);
    assert.equal(value.outcome, 'ready');
    assert.equal(value.state.requestedMode, 'missal');
    assert.equal(value.state.options.ordinary, true);
    assert.equal(value.state.languages.ordinary, 'en');
    assert.equal(value.calendarResult, null);
    assert.equal(value.events.length, 179);
    assert.equal(value.ordinaryCount, 163);
    assert.equal(value.properCount, 10);
    assert.deepEqual(value.dom, value.events.map(row => row.id));
    assert.deepEqual(value.contents, value.dom);
    assert.equal(value.ordinaryLoads, 1);
    assert.match(value.hash, /mode=missal/);
    assert.match(value.hash, /ordinary-lang=en/);
    assert.ok(value.events.every(row => (row.sourceHooks || []).length));
  });

  await check('C5 Propers mode changes preserve exact identity and latent Ordinary language', async () => {
    await candidate(cdp, base, STATES.romanPentecost + '&mode=missal&ordinary-lang=la');
    await click(cdp, '[data-reader-action="mode"]');
    await click(cdp, '[data-mode="read"]');
    await waitFor(cdp, `propersReaderDebug.ready && propersReaderDebug.state?.requestedMode === 'read'`, 'Propers Read mode');
    const read = await evaluate(cdp, `({
      state: propersReaderDebug.state,
      ordinaryLoads: propersReaderDebug.loads['structure/ordinary/roman-1962.json'] || 0,
      ordinaryNodes: document.querySelectorAll('#reader-document .ordinary-element').length,
      hash: location.hash
    })`);
    assert.equal(read.state.formulary.id, 'pentecost');
    assert.equal(read.state.languages.ordinary, 'la');
    assert.equal(read.state.options.ordinary, false);
    assert.equal(read.ordinaryNodes, 0);
    assert.equal(read.ordinaryLoads, 1);
    assert.match(read.hash, /ordinary-lang=la/);
    await click(cdp, '[data-reader-action="mode"]');
    await click(cdp, '[data-mode="missal"]');
    await waitFor(cdp, `propersReaderDebug.ready && propersReaderDebug.state?.requestedMode === 'missal'`, 'Propers Missal mode');
    assert.equal(await evaluate(cdp, `document.querySelectorAll('#reader-document .ordinary-element').length`), 163);
  });

  await check('C5 Ordinary location maps to the nearest Proper when leaving Missal mode', async () => {
    await candidate(cdp, base, STATES.romanPentecost + '&mode=missal&ordinary-lang=la');
    const ordinaryId = await evaluate(cdp,
      `document.querySelector('#reader-document .ordinary-element')?.dataset.semanticEventId`);
    assert.match(ordinaryId, /^ordinary-element\//);
    await candidate(cdp, base, STATES.romanPentecost + '&mode=missal&ordinary-lang=la&location=' +
      encodeURIComponent(ordinaryId));
    await click(cdp, '[data-reader-action="mode"]');
    await click(cdp, '[data-mode="read"]');
    await waitFor(cdp,
      `propersReaderDebug.ready && propersReaderDebug.state?.requestedMode === 'read'`,
      'Read mode from Ordinary location');
    const value = await evaluate(cdp, `({
      outcome: propersReaderDebug.outcome,
      location: propersReaderDebug.state?.semanticLocation?.eventId,
      hash: location.hash,
      ordinaryNodes: document.querySelectorAll('#reader-document .ordinary-element').length
    })`);
    assert.equal(value.outcome, 'ready');
    assert.match(value.location, /^(?:proper|proper-choice)\//);
    assert.ok(value.hash.includes('location=' + encodeURIComponent(value.location)));
    assert.match(value.hash, /ordinary-lang=la/);
    assert.equal(value.ordinaryNodes, 0);
  });

  await check('C5 same-document Ordinary deep link keeps explicit URL location', async () => {
    await candidate(cdp, base, STATES.romanPentecost + '&mode=missal&ordinary-lang=la');
    const ordinaryId = await evaluate(cdp,
      `document.querySelector('#reader-document .ordinary-element')?.dataset.semanticEventId`);
    assert.match(ordinaryId, /^ordinary-element\//);
    const target = STATES.romanPentecost + '&mode=missal&ordinary-lang=la&location=' +
      encodeURIComponent(ordinaryId);
    const before = await evaluate(cdp, 'propersReaderDebug.renders');
    await evaluate(cdp, `location.hash = ${JSON.stringify(target)}`);
    await waitFor(cdp,
      `propersReaderDebug.ready && propersReaderDebug.renders > ${before} && ` +
      `propersReaderDebug.state?.semanticLocation?.eventId === ${JSON.stringify(ordinaryId)}`,
      'same-document Ordinary deep link');
    assert.equal(await evaluate(cdp,
      `new URLSearchParams(location.hash.slice(1)).get('location')`), ordinaryId);
    assert.equal(await evaluate(cdp, 'propersReaderDebug.outcome'), 'ready');
  });

  await check('C5 postconciliar Propers Missal retains form, source options, and date-unknown applicability', async () => {
    await candidate(cdp, base, STATES.postPentecostDay + '&mode=missal');
    const value = await evaluate(cdp, `(() => ({
      outcome: propersReaderDebug.outcome,
      form: propersReaderDebug.semantic?.resolved?.form,
      ordinary: propersReaderDebug.semantic?.events.filter(row => row.kind === 'ordinary-element').length,
      choices: [...document.querySelectorAll('#reader-document .ordinary-choice')].map(row => row.dataset.optionGroup)
        .filter(id => id && !id.startsWith('proper-choice/')),
      unresolved: (propersReaderDebug.semantic?.ordinaryUnresolved || []).map(row => row.element),
      properChoice: propersReaderDebug.semantic?.events.some(row => row.kind === 'proper-choice'),
      calendarResult: propersReaderDebug.semantic?.calendarResult
    }))()`);
    assert.equal(value.outcome, 'ready');
    assert.equal(value.form, 'day');
    assert.ok(value.ordinary > 40);
    assert.equal(value.properChoice, true);
    assert.equal(value.calendarResult, null);
    assert.deepEqual(value.choices.sort(), ['creed', 'eucharistic-prayer', 'penitential-act']);
    assert.ok(value.unresolved.includes('ritus-initiales/gloria-in-excelsis'));
    assert.ok(value.unresolved.includes('symbolum/symbolum-nicaenum'));
  });

  await check('C5 Ordinary variant control commits a URL choice and restores radio focus', async () => {
    await candidate(cdp, base, STATES.postPentecostDay + '&mode=missal');
    await click(cdp, '#reader-document [data-option-group="eucharistic-prayer"] input[value="ep-ii"]');
    await waitFor(cdp,
      `propersReaderDebug.ready && propersReaderDebug.state?.options?.legitimate?.['eucharistic-prayer'] === 'ep-ii'`,
      'selected Eucharistic Prayer');
    const value = await evaluate(cdp, `({
      outcome: propersReaderDebug.outcome,
      hash: location.hash,
      checked: document.querySelector('#reader-document [data-option-group="eucharistic-prayer"] input[value="ep-ii"]')?.checked,
      focused: document.activeElement?.matches('#reader-document [data-option-group="eucharistic-prayer"] input[value="ep-ii"]'),
      calendarResult: propersReaderDebug.semantic?.calendarResult
    })`);
    assert.equal(value.outcome, 'ready');
    assert.match(value.hash, /eucharistic-prayer=ep-ii/);
    assert.equal(value.checked, true);
    assert.equal(value.focused, true);
    assert.equal(value.calendarResult, null);
  });

  await check('C5 invalid explicit Ordinary language and exceptional frame fail or disclose exactly', async () => {
    await candidate(cdp, base, STATES.roman + '&mode=missal&ordinary-lang=not-held');
    assert.equal((await snapshot(cdp)).outcome, 'invalid');
    await candidate(cdp, base, hash({ missal: 'postconciliar', type: 'seasonal',
      mass: 'good-friday', bible: 'douay-rheims', orations: 'la', mode: 'missal' }));
    const value = await evaluate(cdp, `({
      outcome: propersReaderDebug.outcome,
      text: document.querySelector('#reader-document')?.textContent || '',
      ordinary: document.querySelectorAll('#reader-document .ordinary-element').length,
      frame: propersReaderDebug.semantic?.coverage.find(row => row.scope === 'ordinary-frame:postconciliar')
    })`);
    assert.equal(value.outcome, 'ready');
    assert.equal(value.ordinary, 0);
    assert.match(value.text, /no ordinary Mass frame/i);
    assert.equal(value.frame.state, 'absent');
  });

  await check('explicit URL outranks remembered preferences', async () => {
    await evaluate(cdp, `localStorage.setItem('triptych:liturgy:propers', JSON.stringify({missal:'postconciliar',bible:'clementine-vulgate',orations:'en'}))`);
    await candidate(cdp, base, STATES.roman);
    const state = await evaluate(cdp, 'propersReaderDebug.state');
    assert.equal(state.edition.id, 'roman-1962'); assert.equal(state.bible.id, 'douay-rheims');
    assert.equal(state.languages.orations, 'la');
  });

  await check('current and candidate Roman texts, citations, and order match exactly', async () => {
    const wanted = await snapshot(cdp);
    // The candidate's resource count is measured by the deep-link check; when
    // that check failed early this read a null and threw a TypeError that hid
    // its cause.
    assert.ok(performanceReport,
      'the deep-link check did not record the candidate measurements compared here');
    await current(cdp, base, STATES.roman);
    performanceReport.currentRouteResourceCount = await evaluate(cdp,
      `performance.getEntriesByType('resource').length`);
    performanceReport.additionalCandidateRequests =
      performanceReport.candidateResourceCount - performanceReport.currentRouteResourceCount;
    const held = await evaluate(cdp, `[...document.querySelectorAll('#reader-document .proper')].map(row => row.textContent.replace(/\\s+/g, ' ').trim())`);
    assert.deepEqual(wanted.texts, held);
    await candidate(cdp, base, STATES.alternative);
    const alternative = await snapshot(cdp);
    assert.ok(alternative.semantic.events.some(row => row.kind === 'proper-choice' &&
      row.options.some(option => option.events.some(event =>
        event.editionSlotLabel === 'First Reading (alternative)'))));
    await current(cdp, base, STATES.alternative);
    assert.deepEqual(alternative.texts, await evaluate(cdp, `[...document.querySelectorAll('#reader-document .proper')].map(row => row.textContent.replace(/\\s+/g, ' ').trim())`));
  });

  await check('coequal cycles stay independent and explicit cycle selection is exact', async () => {
    await candidate(cdp, base, STATES.cycles);
    const unresolved = await evaluate(cdp, `({
      cycles:[...document.querySelectorAll('.cycle-alternative')].map(row=>row.dataset.cycle),
      buttons:[...document.querySelectorAll('.cycle-choice-controls button')].map(row=>row.textContent),
      kind:propersReaderDebug.semantic.events.find(row=>row.selected.kind==='cycle-alternatives').selected.kind,
      notice:document.querySelector('#coverage-notice').textContent
    })`);
    assert.deepEqual(unresolved.cycles, ['A', 'B', 'C']);
    assert.deepEqual(unresolved.buttons, ['Year A', 'Year B', 'Year C']);
    assert.equal(new Set(unresolved.cycles).size, 3); assert.match(unresolved.notice, /remain valid/);
    await click(cdp, '.cycle-choice-controls button');
    await waitFor(cdp, `propersReaderDebug.ready && propersReaderDebug.state.cycle === 'A'`,
      'public cycle writer');
    assert.equal(await evaluate(cdp,
      `new URLSearchParams(location.hash.slice(1)).get('cycle')`), 'A');
    assert.equal(await evaluate(cdp,
      `[...new URLSearchParams(location.hash.slice(1)).keys()].some(key => key.startsWith('_candidate-'))`), false);
    await candidate(cdp, base, STATES.cycleA);
    const exact = await snapshot(cdp);
    assert.equal(exact.state.cycle, 'A');
    assert.equal(await evaluate(cdp, `document.querySelectorAll('.cycle-choice').length`), 0);
    assert.equal(exact.semantic.events.find(row => row.editionSlotLabel === 'Gospel').selected.cycle, 'A');
    await click(cdp, '[data-reader-action="browse"]');
    await select(cdp, '#reader-orations', 'en');
    const form = await browseSnapshot(cdp);
    if (!form.witnessHidden) {
      assert.ok(form.witnesses[1], 'English cycle selection exposes no held witness');
      await select(cdp, '#reader-witness', form.witnesses[1]);
    }
    await click(cdp, '#browse-form .surface-apply');
    await waitFor(cdp,
      `propersReaderDebug.ready && propersReaderDebug.state.cycle === 'A' && ` +
      `propersReaderDebug.state.languages.orations === 'en'`,
      'cycle retention after language change');
    assert.equal(await evaluate(cdp,
      `new URLSearchParams(location.hash.slice(1)).get('cycle')`), 'A');
    await candidate(cdp, base, STATES.cycleBad);
    assert.equal((await snapshot(cdp)).outcome, 'invalid');
  });

  await check('public semantic keys are stable while retained aliases remain input-only and conflicts fail closed', async () => {
    assert.deepEqual(await evaluate(cdp, 'propersReaderDebug.publicKeys'), {
      cycle: 'cycle', alternative: 'alternative', translationWitness: 'translation-witness'
    });
    assert.deepEqual(await evaluate(cdp, 'propersReaderDebug.legacyInputAliases'), {
      cycle: '_candidate-cycle', alternative: '_candidate-alternative',
      translationWitness: '_candidate-translation-witness'
    });

    await candidate(cdp, base, STATES.cycleLegacyA);
    assert.equal((await snapshot(cdp)).outcome, 'ready');
    assert.equal(await evaluate(cdp, 'propersReaderDebug.state.cycle'), 'A');
    assert.equal(await evaluate(cdp,
      `new URLSearchParams(location.hash.slice(1)).get('cycle')`), 'A');
    assert.equal(await evaluate(cdp,
      `new URLSearchParams(location.hash.slice(1)).has('_candidate-cycle')`), false);

    await candidate(cdp, base, STATES.englishWitness);
    assert.equal((await snapshot(cdp)).outcome, 'ready');
    assert.equal(await evaluate(cdp, 'propersReaderDebug.state.languages.translationWitness'),
      MULTIPLE_TRANSLATION_WITNESS);

    const legacyWitness = STATES.englishMultiple +
      '&_candidate-translation-witness=' + encodeURIComponent(MULTIPLE_TRANSLATION_WITNESS);
    await candidate(cdp, base, legacyWitness);
    assert.equal((await snapshot(cdp)).outcome, 'ready');
    assert.equal(await evaluate(cdp, 'propersReaderDebug.state.languages.translationWitness'),
      MULTIPLE_TRANSLATION_WITNESS);

    for (const state of [
      STATES.cycleMixed,
      STATES.cycleA + '&cycle=A',
      STATES.cycles + '&cycle=',
      STATES.englishWitness + '&_candidate-translation-witness=' + encodeURIComponent(
        MULTIPLE_TRANSLATION_WITNESS),
      STATES.alternativeUnsupported
    ]) {
      await candidate(cdp, base, state);
      assert.equal((await snapshot(cdp)).outcome, 'invalid', state);
      assert.equal(await evaluate(cdp, `document.querySelectorAll('#reader-document .proper').length`), 0);
    }
  });

  await check('missing and malformed identity fail closed without liturgical text', async () => {
    await candidate(cdp, base, STATES.missing);
    assert.equal((await snapshot(cdp)).outcome, 'browse');
    assert.equal(await evaluate(cdp, `document.querySelector('[data-reader-surface="browse"]').open`), true);
    assert.equal(await evaluate(cdp, `document.querySelectorAll('#reader-document .proper').length`), 0);
    // Browse foregrounded by the route stands open but takes neither the page
    // nor focus: opened modally it made the document inert, and Tab never
    // reached the skip link. The first Tab must, and dismisses the surface.
    const surfaceState = `(() => ({
      open: document.querySelector('#browse-surface').open,
      modal: document.querySelector('#browse-surface').matches(':modal'),
      expanded: document.querySelector('[data-reader-action="browse"]').getAttribute('aria-expanded'),
      skipFocused: document.activeElement.classList.contains('skip-link'),
      bodyFocused: document.activeElement === document.body
    }))()`;
    assert.deepEqual(await evaluate(cdp, surfaceState),
      { open: true, modal: false, expanded: 'true', skipFocused: false, bodyFocused: true });
    for (const type of ['keyDown', 'keyUp']) {
      await cdp.send('Input.dispatchKeyEvent', { type, key: 'Tab', code: 'Tab', windowsVirtualKeyCode: 9 });
    }
    await new Promise((done) => setTimeout(done, 50));
    assert.deepEqual(await evaluate(cdp, surfaceState),
      { open: false, modal: false, expanded: 'false', skipFocused: true, bodyFocused: false });
    await candidate(cdp, base, STATES.missing); await escape(cdp);
    assert.deepEqual(await evaluate(cdp, surfaceState),
      { open: false, modal: false, expanded: 'false', skipFocused: false, bodyFocused: true });
    await click(cdp, '[data-reader-action="browse"]');
    assert.equal(await evaluate(cdp, `document.querySelector('#browse-surface').matches(':modal')`), true);
    await escape(cdp);
    await candidate(cdp, base, STATES.invalid);
    assert.equal((await snapshot(cdp)).outcome, 'invalid');
    await candidate(cdp, base, STATES.invalidMass);
    assert.equal((await snapshot(cdp)).outcome, 'invalid');
  });

  await check('source-declared partial formulary reports its typed coverage without suppressing material', async () => {
    await candidate(cdp, base, STATES.partial);
    const held = await snapshot(cdp);
    assert.equal(held.outcome, 'ready');
    assert.equal(held.noticeHidden, false);
    assert.match(held.notice, /not held|unavailable|coverage/i);
    assert.ok(held.texts.length > 0);
    assert.equal(await evaluate(cdp, `document.querySelectorAll('#coverage-notice').length`), 1);
  });

  await check('Latin Browse never asks for a translation witness in either missal', async () => {
    for (const state of [STATES.roman, STATES.post]) {
      await candidate(cdp, base, state); await click(cdp, '[data-reader-action="browse"]');
      const form = await browseSnapshot(cdp);
      assert.equal(form.orations, 'la'); assert.equal(form.witnessHidden, true);
      assert.equal(form.witnessDisplay, 'none');
      assert.deepEqual(form.witnesses, []); assert.equal(form.applyDisabled, false);
      await escape(cdp);
    }
  });

  await check('Browse formulary coverage follows the Orations language on open and on change', async () => {
    const allSouls = 'commemoratione-omnium-fidelium-defunctorum';
    const language = (form, name) => {
      assert.match(form.formularyLabel, new RegExp(' — ' + name + ' — '), JSON.stringify(form.formularyLabel));
      const other = name === 'English' ? 'Latin' : 'English';
      assert.ok(!form.formularyLabels.some(label => label.includes(' — ' + other + ' — ')),
        JSON.stringify(form.formularyLabels));
    };
    // A first open after a cold load once read the still-empty Orations control.
    await freshCandidate(cdp, base, STATES.englishWitness);
    await click(cdp, '[data-reader-action="browse"]');
    let form = await browseSnapshot(cdp);
    assert.equal(form.orations, 'en'); assert.equal(form.formulary, allSouls);
    language(form, 'English');
    await select(cdp, '#reader-orations', 'la');
    form = await browseSnapshot(cdp);
    assert.equal(form.formulary, allSouls); language(form, 'Latin');
    await select(cdp, '#reader-orations', 'en');
    form = await browseSnapshot(cdp);
    assert.equal(form.formulary, allSouls); language(form, 'English');
    await escape(cdp);
    // A reopen after a route change once read the previous route's language.
    await candidate(cdp, base, STATES.roman); await click(cdp, '[data-reader-action="browse"]');
    language(await browseSnapshot(cdp), 'Latin'); await escape(cdp);
    await candidate(cdp, base, STATES.englishWitness); await click(cdp, '[data-reader-action="browse"]');
    language(await browseSnapshot(cdp), 'English'); await escape(cdp);
  });

  await check('a zero coverage denominator is stated plainly, never as 0 of 0', async () => {
    await candidate(cdp, base, STATES.cycles); await click(cdp, '[data-reader-action="browse"]');
    const form = await browseSnapshot(cdp);
    const labels = form.formularyLabels.concat(form.orationLabels);
    assert.ok(!labels.some(label => /\b0 of 0\b/.test(label)), JSON.stringify(labels));
    // The served report decides whether this formulary exercises the zero case.
    const targets = await evaluate(cdp, `(async () => {
      const url = performance.getEntriesByType('resource').map(row => row.name)
        .find(name => /\\/structure\\/propers\\/postconciliar\\.json/.test(name));
      const structure = await (await fetch(url)).json();
      const mass = structure.masses.find(row => row.key === 'transfiguration-lord');
      return mass.coverage.languages.find(row => row.lang === 'la').targets;
    })()`);
    if (targets === 0) {
      assert.equal(form.formularyLabel, 'The Transfiguration of the Lord — Latin — no composed texts represented');
    } else {
      assert.match(form.formularyLabel, /— Latin — \d+ of [1-9]\d* represented texts available$/);
    }
    await escape(cdp);
  });

  await check('the loading placeholder does not shift the reading landmark when data arrives', async () => {
    await freshCandidate(cdp, base, STATES.post);
    await evaluate(cdp, `(() => {
      window.__readerDocumentShifts = [];
      new PerformanceObserver(list => list.getEntries().forEach(entry => {
        for (const source of entry.sources || []) {
          if (source.node && source.node.id === 'reader-document') window.__readerDocumentShifts.push(entry.value);
        }
      })).observe({ type: 'layout-shift' });
    })()`);
    // Hold the new missal so the placeholder-only document is painted, then
    // let the taller identity block and its coverage notice arrive above it.
    const gate = armGate((path) => path.endsWith('/structure/propers/catalog/roman-1962.json'));
    await cdp.send('Runtime.evaluate', {
      expression: `location.hash=${JSON.stringify(STATES.englishWitness.slice(1))}` });
    await waitGate(gate);
    // Past the 500 ms recent-input window, so no shift can be excused as input.
    await evaluate(cdp, 'new Promise(done => setTimeout(() => requestAnimationFrame(() => requestAnimationFrame(done)), 600))');
    const loading = await evaluate(cdp, `(() => {
      const main = document.querySelector('#reader-document');
      const placeholder = main.querySelector(':scope > .placeholder:only-child');
      return { busy: main.getAttribute('aria-busy'), placeholder: placeholder && getComputedStyle(placeholder).visibility };
    })()`);
    assert.deepEqual(loading, { busy: 'true', placeholder: 'visible' });
    gate.release(); await gate.served;
    await waitFor(cdp, `propersReaderDebug.ready && propersReaderDebug.state?.formulary?.id === 'commemoratione-omnium-fidelium-defunctorum'`, 'gated All Souls');
    await evaluate(cdp, 'new Promise(done => requestAnimationFrame(() => requestAnimationFrame(() => setTimeout(done, 100))))');
    assert.equal((await snapshot(cdp)).noticeHidden, false);
    assert.deepEqual(await evaluate(cdp, 'window.__readerDocumentShifts'), []);
  });

  await check('composed-text labels carry their own interface language', async () => {
    for (const state of [STATES.roman, STATES.englishWitness]) {
      await candidate(cdp, base, state);
      const rows = await evaluate(cdp, `[...document.querySelectorAll('#reader-document .composed')].map(node => ({
        lang: node.lang, label: node.querySelector(':scope > .composed-label')?.lang ?? null
      }))`);
      assert.ok(rows.length > 0, 'no composed text rendered');
      assert.ok(rows.every(row => row.label === 'en'), JSON.stringify(rows));
    }
    assert.ok(await evaluate(cdp, `document.querySelectorAll('#reader-document .composed[lang="la"], #reader-document .composed[lang="en"]').length > 0`));
  });

  await check('forced colors keep the Browse submit label visible against its backplate', async () => {
    await cdp.send('Emulation.setEmulatedMedia', { features: [{ name: 'forced-colors', value: 'active' }] });
    try {
      for (const scheme of ['light', 'dark']) {
        await cdp.send('Emulation.setEmulatedMedia', { features: [
          { name: 'forced-colors', value: 'active' }, { name: 'prefers-color-scheme', value: scheme }] });
        await candidate(cdp, base, STATES.roman); await click(cdp, '[data-reader-action="browse"]');
        const paint = await evaluate(cdp, `(() => {
          const probe = document.createElement('span');
          document.body.appendChild(probe);
          const system = name => { probe.style.color = name; return getComputedStyle(probe).color; };
          const canvas = system('Canvas'); const buttonText = system('ButtonText');
          probe.remove();
          const apply = getComputedStyle(document.querySelector('#browse-form .surface-apply'));
          return { forced: matchMedia('(forced-colors: active)').matches, canvas, buttonText,
            color: apply.color, background: apply.backgroundColor, border: apply.borderTopColor,
            borderWidth: apply.borderTopWidth };
        })()`);
        assert.equal(paint.forced, true);
        // Chromium paints a Canvas backplate behind forced text, so the label
        // must never be Canvas, and the button must keep a visible edge.
        assert.notEqual(paint.color, paint.canvas, JSON.stringify(paint));
        assert.notEqual(paint.color, paint.background, JSON.stringify(paint));
        assert.equal(paint.color, paint.buttonText, JSON.stringify(paint));
        assert.notEqual(paint.border, paint.background, JSON.stringify(paint));
        assert.notEqual(paint.borderWidth, '0px');
        await escape(cdp);
      }
    } finally {
      await cdp.send('Emulation.setEmulatedMedia', { features: [] });
    }
  });

  await check('one formulary-relevant witness resolves deterministically without a control', async () => {
    await candidate(cdp, base, STATES.englishOne);
    const state = await evaluate(cdp, 'propersReaderDebug.state');
    assert.equal(state.languages.translationWitness,
      'edition.eugene-cummiskey.roman-missal-english-laity.philadelphia-1861');
    await click(cdp, '[data-reader-action="browse"]');
    const form = await browseSnapshot(cdp);
    assert.equal(form.witnessHidden, true); assert.equal(form.witnessDisplay, 'none');
    assert.deepEqual(form.witnesses, []);
    await escape(cdp);
  });

  await check('multiple relevant witnesses require an explicit formulary-specific choice', async () => {
    await candidate(cdp, base, STATES.englishMultiple);
    assert.ok((await snapshot(cdp)).semantic.unresolvedChoices.some(row =>
      row.id.startsWith('translation-witness:')));
    await click(cdp, '[data-reader-action="browse"]');
    const form = await browseSnapshot(cdp);
    assert.equal(form.witnessHidden, false); assert.notEqual(form.witnessDisplay, 'none');
    assert.equal(form.witnesses.length, 5);
    assert.equal(form.witnesses[0], '');
    assert.ok(form.orationLabels.every(label => /represented texts available/.test(label)));
    assert.ok(form.witnessLabels.slice(1).every(label => /[123] of 6 uses/.test(label)));
    const witness = MULTIPLE_TRANSLATION_WITNESS;
    assert.ok(form.witnesses.includes(witness));
    await select(cdp, '#reader-witness', witness);
    await click(cdp, '#browse-form .surface-apply');
    await waitFor(cdp,
      `propersReaderDebug.ready && propersReaderDebug.state.languages.translationWitness === ${JSON.stringify(witness)}`,
      'explicit translation witness');
    assert.equal(await evaluate(cdp,
      `new URLSearchParams(location.hash.slice(1)).get('translation-witness')`), witness);
    assert.equal(await evaluate(cdp,
      `[...new URLSearchParams(location.hash.slice(1)).keys()].some(key => key.startsWith('_candidate-'))`), false);
    assert.equal(await evaluate(cdp, `document.querySelectorAll('.composed[lang="en"]').length`), 1);
    assert.equal((await snapshot(cdp)).semantic.events.filter(row =>
      row.selected?.reason === 'absent-in-witness').length, 5);
    const selectedNotes = await evaluate(cdp,
      `[...document.querySelectorAll('.composed-note')].map(node => node.textContent)`);
    assert.equal(selectedNotes.filter(text =>
      /No English text is available from the selected witness for this Proper/.test(text)).length, 5);
    assert.ok(!selectedNotes.some(text => /No English or Latin body is held here/.test(text)));
    assert.match((await snapshot(cdp)).notice, /from the selected witness/);
  });

  await check('no held witness remains an explicit unavailable or partial result', async () => {
    await candidate(cdp, base, STATES.englishNone, NO_WITNESS_DATA);
    const value = await snapshot(cdp);
    assert.equal(value.outcome, 'ready', JSON.stringify(value.error)); assert.equal(value.noticeHidden, false);
    assert.ok(value.semantic.coverage.some(row =>
      row.state === 'unavailable' && row.scope === 'proper-translation:en'));
    assert.ok(value.texts.some(row =>
      /English translation unavailable: (?:not resolved|not yet sourced|not publishable here|not present in this witness|not part of this rite or branch)/.test(row)));
    await click(cdp, '[data-reader-action="browse"]');
    const form = await browseSnapshot(cdp);
    assert.equal(form.witnessHidden, true); assert.equal(form.witnessDisplay, 'none');
    await escape(cdp);
  });

  await check('switching a chosen translation witness to Latin removes private witness state', async () => {
    await candidate(cdp, base, STATES.englishMultiple);
    await click(cdp, '[data-reader-action="browse"]');
    const witness = await evaluate(cdp,
      `document.querySelector('#reader-witness').options[1].value`);
    await select(cdp, '#reader-witness', witness);
    await select(cdp, '#reader-orations', 'la');
    const form = await browseSnapshot(cdp);
    assert.equal(form.witnessHidden, true); assert.equal(form.witnessDisplay, 'none');
    assert.deepEqual(form.witnesses, []);
    await click(cdp, '#browse-form .surface-apply');
    await waitFor(cdp, `propersReaderDebug.ready && propersReaderDebug.state.languages.orations === 'la'`,
      'Latin submission');
    assert.equal(await evaluate(cdp,
      `new URLSearchParams(location.hash.slice(1)).has('translation-witness')`), false);
    assert.equal(await evaluate(cdp,
      `'translationWitness' in propersReaderDebug.state.languages`), false);
  });

  await check('edition witnesses irrelevant to the formulary are neither required nor accepted', async () => {
    await candidate(cdp, base, STATES.englishOne);
    await click(cdp, '[data-reader-action="browse"]');
    const form = await browseSnapshot(cdp);
    assert.equal(form.witnessHidden, true); assert.equal(form.witnessDisplay, 'none');
    await escape(cdp);
    const invalidWitness = STATES.englishOne +
      '&translation-witness=' + encodeURIComponent(
        'artifact.eugene-cummiskey.roman-missal-english-laity.philadelphia-1861.temporal-orations-en');
    await candidate(cdp, base, invalidWitness);
    assert.equal((await snapshot(cdp)).outcome, 'invalid');
  });

  await check('changing missal clears formulary and requires a new choice', async () => {
    await candidate(cdp, base, STATES.roman); await click(cdp, '[data-reader-action="browse"]');
    await evaluate(cdp, `(() => { const row=document.querySelector('#reader-missal'); row.value='postconciliar'; row.dispatchEvent(new Event('change',{bubbles:true})); })()`);
    await waitFor(cdp, `document.querySelector('#reader-formulary').disabled === false`, 'draft missal');
    assert.equal(await evaluate(cdp, `document.querySelector('#reader-formulary').value`), '');
    assert.match(await evaluate(cdp, `document.querySelector('#browse-status').textContent`), /cleared/);
    await escape(cdp);
  });

  await check('superseded Browse missal load cannot overwrite a newer valid route form', async () => {
    await freshCandidate(cdp, base, STATES.post); await click(cdp, '[data-reader-action="browse"]');
    const gate = armGate((path) => path.endsWith('/structure/propers/roman-1962.json'));
    await select(cdp, '#reader-missal', 'roman-1962'); await waitGate(gate);
    await evaluate(cdp, `location.hash=${JSON.stringify(STATES.fast.slice(1))}`);
    await waitFor(cdp, `propersReaderDebug.ready && propersReaderDebug.state.formulary.id === 'visitation-blessed-virgin-mary'`, 'new valid route');
    await click(cdp, '[data-reader-action="browse"]');
    const before = await browseSnapshot(cdp); gate.release(); await gate.served;
    await new Promise((done) => setTimeout(done, 120));
    assert.deepEqual(await browseSnapshot(cdp), before);
    assert.equal(before.missal, 'postconciliar'); assert.equal(before.formulary, 'visitation-blessed-virgin-mary');
    await escape(cdp);
  });

  await check('Details opened during load refreshes only from the committed Propers result', async () => {
    const gate = armGate((path) => path.endsWith('/structure/propers/catalog/roman-1962.json'));
    await cdp.send('Page.navigate', { url: candidateUrl(base, STATES.roman) });
    await waitGate(gate);
    await waitFor(cdp, `window.propersReaderDebug && propersReaderDebug.outcome === 'loading'`,
      'Propers loading state');
    await openSurface(cdp, 'details');
    const loading = await evaluate(cdp,
      `document.querySelector('[data-reader-details]').textContent`);
    assert.match(loading, /still loading/);
    assert.doesNotMatch(loading, /Formulary\s+advent-1/);
    gate.release();
    await gate.served;
    await waitFor(cdp,
      `propersReaderDebug.ready && propersReaderDebug.outcome === 'ready'`,
      'Propers Details commit');
    const committed = await evaluate(cdp, `({
      open: document.querySelector('[data-reader-surface="details"]').open,
      text: document.querySelector('[data-reader-details]').innerText,
      headings: [...document.querySelectorAll('[data-reader-details] .details-section > h3')]
        .map(row => row.textContent.trim())
    })`);
    assert.equal(committed.open, true);
    assert.match(committed.text, /Formulary\s+First Sunday of Advent/i);
    assert.deepEqual(committed.headings,
      ['Selection', 'Related reader', 'Elsewhere in Triptych']);
    await escape(cdp);
  });

  await check('superseded Browse load cannot overwrite an invalid route form', async () => {
    await freshCandidate(cdp, base, STATES.post); await click(cdp, '[data-reader-action="browse"]');
    const gate = armGate((path) => path.endsWith('/structure/propers/roman-1962.json'));
    await select(cdp, '#reader-missal', 'roman-1962'); await waitGate(gate);
    await evaluate(cdp, `location.hash=${JSON.stringify(STATES.invalid.slice(1))}`);
    await waitFor(cdp, `propersReaderDebug.ready && propersReaderDebug.outcome === 'invalid'`, 'invalid route');
    await click(cdp, '[data-reader-action="browse"]');
    await select(cdp, '#reader-missal', 'postconciliar');
    await waitFor(cdp, `document.querySelector('#reader-type').disabled === false`, 'current invalid recovery form');
    const before = await browseSnapshot(cdp); gate.release(); await gate.served;
    await new Promise((done) => setTimeout(done, 120));
    assert.deepEqual(await browseSnapshot(cdp), before); assert.equal(before.missal, 'postconciliar');
    assert.equal(before.outcome, 'invalid'); await escape(cdp);
  });

  await check('superseded Browse load cannot overwrite missing-formulary Browse state', async () => {
    await freshCandidate(cdp, base, STATES.post); await click(cdp, '[data-reader-action="browse"]');
    const gate = armGate((path) => path.endsWith('/structure/propers/roman-1962.json'));
    await select(cdp, '#reader-missal', 'roman-1962'); await waitGate(gate);
    await evaluate(cdp, `location.hash=${JSON.stringify(STATES.postMissing.slice(1))}`);
    await waitFor(cdp, `propersReaderDebug.ready && propersReaderDebug.outcome === 'browse'`, 'missing formulary Browse state');
    const before = await browseSnapshot(cdp); gate.release(); await gate.served;
    await new Promise((done) => setTimeout(done, 120));
    assert.deepEqual(await browseSnapshot(cdp), before); assert.equal(before.missal, 'postconciliar');
    assert.equal(before.formulary, ''); assert.equal(before.outcome, 'browse'); await escape(cdp);
  });

  await check('superseded Browse failure cannot overwrite a current valid form', async () => {
    await freshCandidate(cdp, base, STATES.post, DATA + '-failure');
    await click(cdp, '[data-reader-action="browse"]');
    const gate = armGate((path) => path === DATA.slice(1) + '-failure/structure/propers/roman-1962.json');
    await select(cdp, '#reader-missal', 'roman-1962'); await waitGate(gate);
    await evaluate(cdp, `location.hash=${JSON.stringify(STATES.fast.slice(1))}`);
    await waitFor(cdp, `propersReaderDebug.ready && propersReaderDebug.outcome === 'ready'`, 'valid after Browse failure');
    await click(cdp, '[data-reader-action="browse"]');
    const before = await browseSnapshot(cdp); gate.release(); await gate.served;
    await new Promise((done) => setTimeout(done, 120));
    assert.deepEqual(await browseSnapshot(cdp), before); assert.equal(before.missal, 'postconciliar');
    await escape(cdp);
  });

  await check('rapid Browse Missal A to Missal B keeps the latest form', async () => {
    await freshCandidate(cdp, base, STATES.post); await click(cdp, '[data-reader-action="browse"]');
    const gate = armGate((path) => path.endsWith('/structure/propers/roman-1962.json'));
    await select(cdp, '#reader-missal', 'roman-1962'); await waitGate(gate);
    await select(cdp, '#reader-missal', 'postconciliar');
    await waitFor(cdp, `document.querySelector('#reader-type').disabled === false`, 'latest Browse missal');
    const before = await browseSnapshot(cdp); gate.release(); await gate.served;
    await new Promise((done) => setTimeout(done, 120));
    assert.deepEqual(await browseSnapshot(cdp), before); assert.equal(before.missal, 'postconciliar');
    await escape(cdp);
  });

  await check('Back and Forward invalidate an older pending Browse request', async () => {
    await freshCandidate(cdp, base, STATES.post); await click(cdp, '[data-reader-action="browse"]');
    const gate = armGate((path) => path.endsWith('/structure/propers/roman-1962.json'));
    await select(cdp, '#reader-missal', 'roman-1962'); await waitGate(gate);
    await evaluate(cdp, `location.hash=${JSON.stringify(STATES.fast.slice(1))}`);
    await waitFor(cdp, `propersReaderDebug.ready && propersReaderDebug.state.formulary.id === 'visitation-blessed-virgin-mary'`, 'forward Browse state');
    await evaluate(cdp, 'history.back()');
    await waitFor(cdp, `propersReaderDebug.ready && propersReaderDebug.state.formulary.id === 'advent-1'`, 'Browse history back');
    await evaluate(cdp, 'history.forward()');
    await waitFor(cdp, `propersReaderDebug.ready && propersReaderDebug.state.formulary.id === 'visitation-blessed-virgin-mary'`, 'Browse history forward');
    await click(cdp, '[data-reader-action="browse"]');
    const before = await browseSnapshot(cdp); gate.release(); await gate.served;
    await new Promise((done) => setTimeout(done, 120));
    assert.deepEqual(await browseSnapshot(cdp), before); assert.equal(before.missal, 'postconciliar');
    await escape(cdp);
  });

  await check('shared modal lifecycle, disabled modes, deep-scroll reachability, and restoration hold', async () => {
    await candidate(cdp, base, STATES.post);
    await evaluate(cdp, `(async () => {
      scrollTo({ top: document.documentElement.scrollHeight, behavior: 'instant' });
      await new Promise(resolve => requestAnimationFrame(() => requestAnimationFrame(resolve)));
    })()`);
    const before = await evaluate(cdp, 'scrollY');
    const locus = await evaluate(cdp, `({
      hidden: document.querySelector('[data-reader-locus]').hidden,
      text: document.querySelector('[data-reader-locus]').textContent.trim()
    })`);
    assert.equal(locus.hidden, false);
    assert.match(locus.text, /Propers/i);
    await click(cdp, '[data-reader-action="contents"]');
    assert.equal(await evaluate(cdp, `document.querySelector('[data-reader-surface="contents"]').open`), true);
    assert.equal(await evaluate(cdp, `document.querySelector('[data-reader-surface="contents"]').contains(document.activeElement)`), true);
    const mapped = await evaluate(cdp, `(() => {
      const row = document.querySelector('[data-reader-contents] [aria-current="location"]');
      const scroller = document.querySelector('[data-reader-contents]').closest('.surface-body');
      const r = row.getBoundingClientRect(); const s = scroller.getBoundingClientRect();
      return { visible: r.bottom > s.top && r.top < s.bottom,
        centered: Math.abs((r.top + r.bottom - s.top - s.bottom) / 2) <= 70,
        clamped: scroller.scrollTop >= scroller.scrollHeight - scroller.clientHeight - 1 };
    })()`);
    assert.equal(mapped.visible, true);
    assert.equal(mapped.centered || mapped.clamped, true);
    await escape(cdp);
    assert.equal(await evaluate(cdp, `document.activeElement.dataset.readerAction`), 'contents');
    assert.ok(Math.abs((await evaluate(cdp, 'scrollY')) - before) < 3);
    await click(cdp, '[data-reader-action="mode"]');
    const modes = await evaluate(cdp, `[...document.querySelectorAll('[data-mode]')].map(row=>({mode:row.dataset.mode,disabled:row.disabled,checked:row.getAttribute('aria-checked')}))`);
    assert.deepEqual(modes, [
      { mode: 'read', disabled: false, checked: 'true' },
      { mode: 'missal', disabled: false, checked: 'false' },
      { mode: 'study', disabled: false, checked: 'false' },
      { mode: 'compare', disabled: false, checked: 'false' }
    ]);
    await openSurface(cdp, 'details');
    const details = await evaluate(cdp, `({
      text: document.querySelector('[data-reader-details]').innerText,
      links: [...document.querySelectorAll('[data-reader-details] a')]
        .map(row => ({ label: row.textContent.trim(), pathname: new URL(row.href).pathname }))
    })`);
    assert.doesNotMatch(details.text, /sourceHooks|ordinal|hash|reader state|\{.*\}/i);
    assert.deepEqual(details.links.map(row => row.label), [
      'Open the Day reader', 'The Story of Salvation', 'How the Missal Changed',
      'Every Document', 'The Source Library', 'The Code, Canon by Canon'
    ]);
    assert.match(details.links[0].pathname, /\/liturgy\/day\.html$/);
    assert.match(details.links[1].pathname, /\/scripture\/$/);
    assert.match(details.links[2].pathname, /\/history\/$/);
    assert.match(details.links[3].pathname, /\/texts\/$/);
    assert.match(details.links[4].pathname, /\/sources\/$/);
    assert.match(details.links[5].pathname, /\/law\/$/);
    assert.deepEqual(await evaluate(cdp,
      `[...document.querySelectorAll('[data-reader-details] .details-section > h3')]
        .map(row => row.textContent.trim())`), [
      'Selection', 'Related reader', 'Elsewhere in Triptych'
    ]);
    assert.equal(await evaluate(cdp, `document.querySelectorAll('.reader-actions [data-reader-action]').length`), 4);
    assert.equal(await evaluate(cdp, 'propersReaderDebug.detailsBuilds'), 1);
    await escape(cdp);
    assert.equal(await evaluate(cdp, `document.activeElement.dataset.readerAction`), 'mode');
  });

  await check('Back and Forward restore candidate semantic choice', async () => {
    await candidate(cdp, base, STATES.cycles);
    await click(cdp, '.cycle-choice-controls button');
    await waitFor(cdp, `propersReaderDebug.ready && propersReaderDebug.state.cycle === 'A'`, 'cycle A navigation');
    await evaluate(cdp, 'history.back()');
    await waitFor(cdp, `propersReaderDebug.ready && !('cycle' in propersReaderDebug.state)`, 'history back');
    await evaluate(cdp, 'history.forward()');
    await waitFor(cdp, `propersReaderDebug.ready && propersReaderDebug.state.cycle === 'A'`, 'history forward');
    await cdp.send('Page.reload', { ignoreCache: true });
    await waitFor(cdp,
      `performance.getEntriesByType('navigation')[0]?.type === 'reload' && window.propersReaderDebug && ` +
      `window.propersReaderDebug && propersReaderDebug.ready && ` +
      `propersReaderDebug.state.cycle === 'A'`, 'cycle reload');
    assert.equal(await evaluate(cdp,
      `new URLSearchParams(location.hash.slice(1)).get('cycle')`), 'A');
  });

  await check('translation witness survives direct load, reload, Back, and Forward', async () => {
    await candidate(cdp, base, STATES.englishMultiple);
    await evaluate(cdp, `location.hash=${JSON.stringify(STATES.englishWitness.slice(1))}`);
    await waitFor(cdp,
      `propersReaderDebug.ready && propersReaderDebug.state.languages.translationWitness === ` +
      `${JSON.stringify(MULTIPLE_TRANSLATION_WITNESS)}`,
      'translation witness navigation');
    const source = await evaluate(cdp, `document.querySelector('#formulary-source').textContent`);
    assert.match(source, /Translation witness: Lyra Catholica/);
    assert.match(source, /Rights: Public Domain/);
    await cdp.send('Emulation.setEmulatedMedia', { media: 'print' });
    assert.notEqual(await evaluate(cdp,
      `getComputedStyle(document.querySelector('#formulary-source')).display`), 'none');
    await cdp.send('Emulation.setEmulatedMedia', { media: 'screen' });
    await cdp.send('Page.reload', { ignoreCache: true });
    await waitFor(cdp,
      `performance.getEntriesByType('navigation')[0]?.type === 'reload' && window.propersReaderDebug && ` +
      `window.propersReaderDebug && propersReaderDebug.ready && ` +
      `propersReaderDebug.state.languages.translationWitness === ` +
      `${JSON.stringify(MULTIPLE_TRANSLATION_WITNESS)}`,
      'translation witness reload');
    await evaluate(cdp, 'history.back()');
    await waitFor(cdp,
      `propersReaderDebug.ready && !('translationWitness' in propersReaderDebug.state.languages)`,
      'translation witness history back');
    await evaluate(cdp, 'history.forward()');
    await waitFor(cdp,
      `propersReaderDebug.ready && propersReaderDebug.state.languages.translationWitness === ` +
      `${JSON.stringify(MULTIPLE_TRANSLATION_WITNESS)}`,
      'translation witness history forward');
  });

  await check('unsupported public alternative survives URL lifecycle and stays fail-closed', async () => {
    await candidate(cdp, base, STATES.cycles);
    await evaluate(cdp, `location.hash=${JSON.stringify(STATES.alternativeUnsupported.slice(1))}`);
    await waitFor(cdp,
      `propersReaderDebug.ready && propersReaderDebug.outcome === 'invalid'`,
      'unsupported alternative navigation');
    assert.equal(await evaluate(cdp,
      `new URLSearchParams(location.hash.slice(1)).get('alternative')`),
      'first-reading-alternative');
    await cdp.send('Page.reload', { ignoreCache: true });
    await waitFor(cdp,
      `performance.getEntriesByType('navigation')[0]?.type === 'reload' && window.propersReaderDebug && ` +
      `window.propersReaderDebug && propersReaderDebug.ready && ` +
      `propersReaderDebug.outcome === 'invalid'`,
      'unsupported alternative reload');
    await evaluate(cdp, 'history.back()');
    await waitFor(cdp,
      `propersReaderDebug.ready && propersReaderDebug.outcome === 'ready' && ` +
      `!new URLSearchParams(location.hash.slice(1)).has('alternative')`,
      'unsupported alternative history back');
    await evaluate(cdp, 'history.forward()');
    await waitFor(cdp,
      `propersReaderDebug.ready && propersReaderDebug.outcome === 'invalid' && ` +
      `new URLSearchParams(location.hash.slice(1)).get('alternative') === 'first-reading-alternative'`,
      'unsupported alternative history forward');
  });

  await check('320 CSS pixels and 200 percent zoom preserve page and surface overflow contracts', async () => {
    await viewport(cdp, 320, 852); await candidate(cdp, base, STATES.cycles);
    for (const action of ['browse', 'contents', 'mode', 'details']) {
      await openSurface(cdp, action);
      const held = await metrics(cdp); assert.equal(held.pageOverflow, 0); assert.deepEqual(held.surfaceOverflow, []);
      await escape(cdp);
    }
    await cdp.send('Emulation.setPageScaleFactor', { pageScaleFactor: 2 });
    assert.equal((await metrics(cdp)).pageOverflow, 0);
    await cdp.send('Emulation.setPageScaleFactor', { pageScaleFactor: 1 });
  });

  await check('reduced motion retains content, controls, and explicit focus', async () => {
    await cdp.send('Emulation.setEmulatedMedia', {
      media: 'screen', features: [{ name: 'prefers-reduced-motion', value: 'reduce' }]
    });
    await candidate(cdp, base, STATES.roman);
    assert.equal(await evaluate(cdp, `document.querySelectorAll('.reader-actions [data-reader-action]').length`), 4);
    assert.equal(await evaluate(cdp, `document.querySelectorAll('#reader-document .proper').length`), 9);
    await openSurface(cdp, 'details');
    assert.equal(await evaluate(cdp, `document.querySelector('[data-reader-surface="details"]').contains(document.activeElement)`), true);
    await escape(cdp);
    await cdp.send('Emulation.setEmulatedMedia', { media: 'screen', features: [] });
  });

  await check('the retained Propers route is statically noindex and visible copy is route-neutral', async () => {
    const source = await readFile(resolve(ROOT, 'src/web/browser/liturgy/propers-reader.html'), 'utf8');
    assert.match(source,
      /<meta name="robots" content="noindex, nofollow, noarchive, nosnippet, noimageindex">/);
    assert.doesNotMatch(source, /<link[^>]+rel=["']canonical["']|property=["']og:url["']/i);
    await candidate(cdp, base, STATES.roman);
    const value = await evaluate(cdp, `({
      robots: document.querySelector('meta[name="robots"]').content,
      title: document.title,
      visible: document.body.innerText,
      actions: document.querySelectorAll('.reader-actions [data-reader-action]').length
    })`);
    assert.equal(value.robots, 'noindex, nofollow, noarchive, nosnippet, noimageindex');
    assert.equal(value.actions, 4);
    assert.doesNotMatch(value.title + '\n' + value.visible,
      /internal candidate|reader candidate|current reader|live reader/i);
  });

  await check('print removes shell chrome but retains identity and choice notice', async () => {
    await candidate(cdp, base, STATES.cycles); await cdp.send('Emulation.setEmulatedMedia', { media: 'print' });
    const value = await evaluate(cdp, `({
      shell:getComputedStyle(document.querySelector('.reader-actions')).display,
      routeMarker:document.querySelector('.candidate-flag'),
      title:document.querySelector('#formulary-title').textContent,
      notice:document.querySelector('#coverage-notice').textContent,
      choices:[...document.querySelectorAll('.cycle-alternative')].length
    })`);
    assert.equal(value.shell, 'none'); assert.equal(value.routeMarker, null);
    assert.equal(value.title, 'The Transfiguration of the Lord'); assert.match(value.notice, /cycles/); assert.equal(value.choices, 3);
    await cdp.send('Emulation.setEmulatedMedia', { media: 'screen' });
  });

  await check('superseded slow valid cannot overwrite fast valid or fast invalid', async () => {
    for (const [next, expected] of [[STATES.fast, 'visitation-blessed-virgin-mary'], [STATES.invalid, null]]) {
      const gate = armGate((path) => path.endsWith('/structure/propers/catalog/roman-1962.json'));
      const target = `${base}${CANDIDATE}?data=${DATA}&race=${Math.random()}${STATES.roman}`;
      await cdp.send('Page.navigate', { url: target }); await waitGate(gate);
      await evaluate(cdp, `location.hash=${JSON.stringify(next.slice(1))}`);
      await waitFor(cdp, 'window.propersReaderReady === true', 'fast render');
      gate.release(); await gate.served; await new Promise((done) => setTimeout(done, 120));
      const held = await snapshot(cdp);
      assert.equal(held.semantic?.resolved?.formulary || null, expected);
      assert.equal(held.outcome, expected ? 'ready' : 'invalid');
    }
  });

  await check('superseded slow failure cannot overwrite fast valid', async () => {
    const gate = armGate((path) => path === DATA.slice(1) + '-failure/structure/propers/roman-1962.json');
    await cdp.send('Page.navigate', { url: candidateUrl(base, STATES.roman, DATA + '-failure') });
    await waitGate(gate); await evaluate(cdp, `location.hash=${JSON.stringify(STATES.fast.slice(1))}`);
    await waitFor(cdp, `propersReaderDebug.ready && propersReaderDebug.outcome === 'ready'`, 'fast valid after pending failure');
    gate.release(); await gate.served; await new Promise((done) => setTimeout(done, 120));
    assert.equal((await snapshot(cdp)).semantic.resolved.formulary, 'visitation-blessed-virgin-mary');
  });

  await check('Back and Forward cannot revive an older pending render', async () => {
    const gate = armGate((path) => path.endsWith('/structure/propers/catalog/roman-1962.json'));
    const target = `${base}${CANDIDATE}?data=${DATA}&history-race=${Math.random()}${STATES.roman}`;
    await cdp.send('Page.navigate', { url: target }); await waitGate(gate);
    await evaluate(cdp, `location.hash=${JSON.stringify(STATES.fast.slice(1))}`);
    await waitFor(cdp, `propersReaderDebug.ready && propersReaderDebug.state.formulary.id === 'visitation-blessed-virgin-mary'`, 'fast history state');
    await evaluate(cdp, 'history.back()');
    await new Promise((done) => setTimeout(done, 60));
    await evaluate(cdp, 'history.forward()');
    await waitFor(cdp, `propersReaderDebug.ready && propersReaderDebug.state.formulary.id === 'visitation-blessed-virgin-mary'`, 'restored fast history state');
    gate.release(); await gate.served; await new Promise((done) => setTimeout(done, 120));
    const held = await snapshot(cdp);
    assert.equal(held.outcome, 'ready');
    assert.equal(held.semantic.resolved.formulary, 'visitation-blessed-virgin-mary');
  });
}

async function captures(cdp, base) {
  if (!captureDir) return null;
  await mkdir(captureDir, { recursive: true });
  const measurements = {};
  for (const [label, width, height] of [
    ['1440x900', 1440, 900], ['1024x768', 1024, 768], ['768x1024', 768, 1024],
    ['393x852', 393, 852], ['320x852', 320, 852]
  ]) {
    await viewport(cdp, width, height); await candidate(cdp, base, STATES.roman);
    await shot(cdp, resolve(captureDir, `propers-reader-valid-${label}.png`));
    measurements[label] = await metrics(cdp);
  }
  await viewport(cdp, 393, 852);
  const states = [['missing', STATES.missing], ['cycle-choice', STATES.cycles], ['invalid', STATES.invalid], ['partial-unavailable', STATES.partial]];
  for (const [label, state] of states) {
    await candidate(cdp, base, state); await shot(cdp, resolve(captureDir, `propers-reader-${label}-393x852.png`));
  }
  await candidate(cdp, base, STATES.cycleA);
  await shot(cdp, resolve(captureDir, 'propers-reader-public-cycle-a-393x852.png'));
  await candidate(cdp, base, STATES.englishWitness);
  await shot(cdp, resolve(captureDir, 'propers-reader-public-translation-witness-393x852.png'));
  await candidate(cdp, base, STATES.roman); await click(cdp, '[data-reader-action="browse"]');
  await shot(cdp, resolve(captureDir, 'propers-reader-roman-1962-latin-browse-393x852.png')); await escape(cdp);
  await candidate(cdp, base, STATES.post); await click(cdp, '[data-reader-action="browse"]');
  await shot(cdp, resolve(captureDir, 'propers-reader-postconciliar-latin-browse-393x852.png')); await escape(cdp);
  await candidate(cdp, base, STATES.englishMultiple); await click(cdp, '[data-reader-action="browse"]');
  await shot(cdp, resolve(captureDir, 'propers-reader-translation-multiple-witness-393x852.png')); await escape(cdp);
  await candidate(cdp, base, STATES.englishNone); await click(cdp, '[data-reader-action="browse"]');
  await shot(cdp, resolve(captureDir, 'propers-reader-translation-no-witness-393x852.png')); await escape(cdp);
  await freshCandidate(cdp, base, STATES.post); await click(cdp, '[data-reader-action="browse"]');
  const raceGate = armGate((path) => path.endsWith('/structure/propers/roman-1962.json'));
  await select(cdp, '#reader-missal', 'roman-1962'); await waitGate(raceGate);
  await evaluate(cdp, `location.hash=${JSON.stringify(STATES.fast.slice(1))}`);
  await waitFor(cdp, `propersReaderDebug.ready && propersReaderDebug.state.formulary.id === 'visitation-blessed-virgin-mary'`, 'capture race outcome');
  await click(cdp, '[data-reader-action="browse"]'); raceGate.release(); await raceGate.served;
  await new Promise((done) => setTimeout(done, 120));
  await shot(cdp, resolve(captureDir, 'propers-reader-browse-race-settled-393x852.png')); await escape(cdp);
  await candidate(cdp, base, STATES.roman);
  await shot(cdp, resolve(captureDir, 'propers-reader-route-neutral-393x852.png'));
  await candidate(cdp, base, STATES.post); await evaluate(cdp, 'scrollTo(0, document.documentElement.scrollHeight)');
  await shot(cdp, resolve(captureDir, 'propers-reader-deep-scroll-393x852.png'));
  for (const action of ['browse', 'contents', 'mode', 'details']) {
    await openSurface(cdp, action);
    await shot(cdp, resolve(captureDir, `propers-reader-${action}-open-393x852.png`)); await escape(cdp);
  }
  for (const scheme of ['light', 'dark']) {
    await cdp.send('Emulation.setEmulatedMedia', { features: [
      { name: 'forced-colors', value: 'active' }, { name: 'prefers-color-scheme', value: scheme }] });
    await candidate(cdp, base, STATES.englishWitness); await click(cdp, '[data-reader-action="browse"]');
    await shot(cdp, resolve(captureDir, `propers-reader-browse-forced-${scheme}-393x852.png`)); await escape(cdp);
  }
  await cdp.send('Emulation.setEmulatedMedia', { features: [] });
  await viewport(cdp, 1440, 900); await candidate(cdp, base, STATES.roman);
  await click(cdp, '[data-reader-action="browse"]');
  await shot(cdp, resolve(captureDir, 'propers-reader-browse-open-1440x900.png')); await escape(cdp);
  await openSurface(cdp, 'details');
  await shot(cdp, resolve(captureDir, 'propers-reader-details-open-1440x900.png')); await escape(cdp);
  await shot(cdp, resolve(captureDir, 'propers-reader-valid-1440x900-paired.png'));
  await current(cdp, base, STATES.roman); await shot(cdp, resolve(captureDir, 'propers-current-valid-1440x900.png'));
  await viewport(cdp, 393, 852); await candidate(cdp, base, STATES.cycles);
  await cdp.send('Emulation.setPageScaleFactor', { pageScaleFactor: 2 });
  await shot(cdp, resolve(captureDir, 'propers-reader-cycle-choice-200-percent.png'));
  await cdp.send('Emulation.setPageScaleFactor', { pageScaleFactor: 1 });
  await cdp.send('Emulation.setEmulatedMedia', { media: 'print' });
  const pdf = await cdp.send('Page.printToPDF', { printBackground: true, preferCSSPageSize: true });
  await writeFile(resolve(captureDir, 'propers-reader-cycle-choice-print.pdf'), Buffer.from(pdf.data, 'base64'));
  await cdp.send('Emulation.setEmulatedMedia', { media: 'screen' });
  for (const [label, width, height] of [
    ['1440x900', 1440, 900], ['393x852', 393, 852], ['320x852', 320, 852]
  ]) {
    await viewport(cdp, width, height);
    for (const [language, state] of [
      ['latin', STATES.romanPentecost], ['english', STATES.romanPentecostEnglish]
    ]) {
      await candidate(cdp, base, state);
      const overflow = await evaluate(cdp,
        'document.documentElement.scrollWidth - document.documentElement.clientWidth');
      assert.ok(overflow <= 1, `Pentecost ${language} ${label} overflows by ${overflow}px`);
      await shot(cdp, resolve(captureDir,
        `propers--pentecost-1962-read-${language}--${label}.png`));
    }
  }
  await viewport(cdp, 1024, 768);
  for (const [language, state] of [
    ['latin', STATES.romanPentecost], ['english', STATES.romanPentecostEnglish]
  ]) {
    await candidate(cdp, base, state);
    await cdp.send('Emulation.setEmulatedMedia', { media: 'print' });
    try {
      const printed = await cdp.send('Page.printToPDF', {
        printBackground: true, preferCSSPageSize: true
      });
      await writeFile(resolve(captureDir,
        `propers--pentecost-1962-read-${language}--print.pdf`),
      Buffer.from(printed.data, 'base64'));
    } finally {
      await cdp.send('Emulation.setEmulatedMedia', { media: 'screen' });
    }
  }
  await writeFile(resolve(captureDir, 'browser-results.json'), JSON.stringify({
    results, measurements, accessibility: accessibilityReport, performance: performanceReport
  }, null, 2) + '\n');
  return measurements;
}

if (process.argv.includes('--check-fixtures')) {
  const read = async (edition) => readFile(resolve(ROOT,
    'src/web/data/structure/propers', edition + '.json'), 'utf8');
  const { T, A } = readerTools(ROOT);
  const roman = await read('roman-1962');
  const empty = withoutWitness(roman);
  const emptyMass = empty.masses.find(row => row.key ===
    's-hilarii-episcopi-confessoris-ecclesiae-doctoris');
  assert.deepEqual(T.coverageWitnesses(emptyMass.coverage, 'en'), []);
  const emptyResult = A.adaptPropers({ structure: empty, request: fixtureRequest(empty, emptyMass) });
  const emptyBodies = emptyResult.events.filter(row => row.selected?.kind === 'composed');
  assert.ok(emptyBodies.length > 0);
  assert.ok(emptyBodies.every(row => row.selected.missing));
  const cycles = withCycleUntranslated(await read('postconciliar'));
  const mass = cycles.masses.find(row => row.key === 'transfiguration-lord');
  const proper = mass.propers[0];
  assert.equal(proper.coverage, null);
  assert.deepEqual(['A', 'B', 'C'].map(cycle =>
    proper.cycles[cycle].coverage.languages.find(row => row.lang === 'en').availability),
  ['not-publishable', 'available', 'unresolved']);
  for (const cycle of ['A', 'B', 'C']) {
    const request = fixtureRequest(cycles, mass, { cycle });
    const result = A.adaptPropers({ request, structure: cycles });
    const report = T.summarizeCoverage(T.selectedCoverageUnits(result, cycles));
    const offered = T.coverageWitnesses(report, 'en').map(row => row.id);
    assert.equal(offered.includes('synthetic.cycle-b-held-english'), cycle === 'B');
    assert.ok(T.selectedCoverageUnits(result, cycles).some(row => row.cycle === cycle));
  }
  assert.deepEqual(T.summarizeCoverage(mass.propers.flatMap(row => T.coverageUnitsOf(row))),
    { ...mass.coverage, scope: 'selection' });
  const checks = verifyRealWitnesses(JSON.parse(roman), ROOT);
  process.stdout.write(JSON.stringify({ status: 'pass', mode: 'fixtures-only',
    checks: ['untranslated-report', 'cycle-owned-reports', ...checks] }) + '\n');
  process.exit(0);
}

const instance = server();
const port = await listen(instance);
const debugPort = await freePort();
const profileRoot = resolve(process.env.TRIPTYCH_BROWSER_SCRATCH || tmpdir());
await mkdir(profileRoot, { recursive: true });
const profile = await mkdtemp(resolve(profileRoot, 'triptych-propers-reader-'));
const chrome = spawn(chromeBinary, [
  '--headless=new', '--disable-gpu', '--no-sandbox', '--disable-dev-shm-usage',
  `--remote-debugging-port=${debugPort}`, `--user-data-dir=${profile}`, 'about:blank'
], { stdio: ['ignore', 'ignore', 'pipe'] });
let chromeError = '';
chrome.stderr.on('data', (chunk) => { chromeError += chunk.toString(); });

let cdp;
try {
  const pages = await waitJson(`http://127.0.0.1:${debugPort}/json`);
  cdp = new CDP(pages.find((row) => row.type === 'page').webSocketDebuggerUrl); await cdp.ready();
  cdp.on('Runtime.consoleAPICalled', ({ type, args }) => {
    if (type === 'error' || type === 'warning') consoleProblems.push(args.map((row) => row.value || row.description).join(' '));
  });
  cdp.on('Network.loadingFailed', (row) => { if (!row.canceled) failedRequests.push(row.errorText); });
  await Promise.all([
    cdp.send('Page.enable'), cdp.send('Runtime.enable'), cdp.send('Network.enable'),
    cdp.send('Accessibility.enable')
  ]);
  await cdp.send('Page.addScriptToEvaluateOnNewDocument', { source: `
    window.__triptychLayoutShifts = [];
    new PerformanceObserver(list => list.getEntries().forEach(entry => {
      if (!entry.hadRecentInput) window.__triptychLayoutShifts.push(entry.value);
    })).observe({type: 'layout-shift', buffered: true});
  ` });
  const base = `http://127.0.0.1:${port}`;
  await assertions(cdp, base);
  if (process.env.TRIPTYCH_P0_ONLY !== '1') {
    await viewport(cdp, 393, 852); await candidate(cdp, base, STATES.roman);
    const tree = await cdp.send('Accessibility.getFullAXTree');
    const interactive = new Set(['button', 'link', 'radio', 'combobox', 'textbox']);
    const unnamed = tree.nodes.filter(row => interactive.has(row.role?.value) && !row.name?.value);
    accessibilityReport = {
      nodeCount: tree.nodes.length,
      unnamedInteractiveNodes: unnamed.length,
      roles: unnamed.map(row => row.role?.value)
    };
    assert.equal(unnamed.length, 0, 'unnamed interactive accessibility nodes');
    await captures(cdp, base);
  }
} catch (error) {
  failures.push({ name: 'harness', detail: error.stack || String(error) });
} finally {
  if (responseGate) responseGate.release();
  if (cdp) cdp.close();
  if (chrome.exitCode === null && chrome.signalCode === null) {
    const exited = new Promise((done) => chrome.once('exit', done));
    chrome.kill('SIGTERM');
    await exited;
  }
  instance.closeAllConnections();
  await new Promise((done) => instance.close(done));
  await rm(profile, { recursive: true, force: true, maxRetries: 5, retryDelay: 100 });
}

if (consoleProblems.length) failures.push({ name: 'console', detail: consoleProblems.join('\n') });
if (failedRequests.length) failures.push({ name: 'network', detail: failedRequests.join('\n') });
if (failures.length) {
  console.error(JSON.stringify({ status: 'fail', results, failures, chromeError: chromeError.slice(-2000) }, null, 2));
  process.exitCode = 1;
} else {
  console.log(JSON.stringify({
    status: 'pass', assertions: results.length, results,
    accessibility: accessibilityReport, performance: performanceReport
  }, null, 2));
}
