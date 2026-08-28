#!/usr/bin/env node

/* Real-Chromium interaction, race, reflow, parity, and review gates for W3. */

import assert from 'node:assert/strict';
import { spawn } from 'node:child_process';
import { createServer } from 'node:http';
import { mkdir, mkdtemp, readFile, writeFile } from 'node:fs/promises';
import { tmpdir } from 'node:os';
import { extname, resolve, sep } from 'node:path';
import process from 'node:process';

const ROOT = resolve(process.env.TRIPTYCH_REVIEW_ROOT || resolve(import.meta.dirname, '../..'));
const CANDIDATE = '/src/web/browser/liturgy/propers-reader.html';
const CURRENT = '/src/web/browser/liturgy/index.html';
const SOURCE_ONLY = process.env.TRIPTYCH_SOURCE_ONLY === '1';
const DATA = SOURCE_ONLY ? '/src/web/data' : '/build/public-alpha/preview/browse';
const SOURCE_PROPERS = (process.env.TRIPTYCH_SOURCE_PROPERS ||
  '.scratch/propers-source-structure/structure/propers').replace(/^\/+|\/+$/g, '');
const CYCLE_UNTRANSLATED_DATA = DATA + '-cycle-untranslated';
const NO_WITNESS_DATA = DATA + '-no-witness';
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
      const corrupt = relative.startsWith('build/public-alpha/preview/browse-failure/');
      if (corrupt) {
        relative = relative.replace('/browse-failure/', '/browse/');
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
        const payload = JSON.parse(body.toString('utf8'));
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
        body = Buffer.from(JSON.stringify(payload));
      }
      if (noWitness && relative.endsWith('/structure/propers/roman-1962.json')) {
        const payload = JSON.parse(body.toString('utf8'));
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
        body = Buffer.from(JSON.stringify(payload));
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
  post: hash({ missal: 'postconciliar', type: 'seasonal', mass: 'advent-1', bible: 'douay-rheims', orations: 'la' }),
  cycles: hash({ missal: 'postconciliar', type: 'christological', mass: 'transfiguration-lord', bible: 'douay-rheims', orations: 'la' }),
  cycleA: hash({ missal: 'postconciliar', type: 'christological', mass: 'transfiguration-lord', bible: 'douay-rheims', orations: 'la', cycle: 'A' }),
  cycleLegacyA: hash({ missal: 'postconciliar', type: 'christological', mass: 'transfiguration-lord', bible: 'douay-rheims', orations: 'la', '_candidate-cycle': 'A' }),
  cycleMixed: hash({ missal: 'postconciliar', type: 'christological', mass: 'transfiguration-lord', bible: 'douay-rheims', orations: 'la', cycle: 'A', '_candidate-cycle': 'A' }),
  cycleBad: hash({ missal: 'postconciliar', type: 'christological', mass: 'transfiguration-lord', bible: 'douay-rheims', orations: 'la', cycle: 'Z' }),
  alternativeUnsupported: hash({ missal: 'postconciliar', type: 'christological', mass: 'transfiguration-lord', bible: 'douay-rheims', orations: 'la', alternative: 'first-reading-alternative' }),
  alternative: hash({ missal: 'postconciliar', type: 'marian', mass: 'visitation-blessed-virgin-mary', bible: 'douay-rheims', orations: 'la' }),
  partial: hash({ missal: 'roman-1962', type: 'christological', mass: 'octava-nativitatis-domini', bible: 'douay-rheims', orations: 'la' }),
  missing: hash({ missal: 'roman-1962', bible: 'douay-rheims', orations: 'la' }),
  postMissing: hash({ missal: 'postconciliar', bible: 'douay-rheims', orations: 'la' }),
  invalid: hash({ missal: 'not-a-missal', type: 'seasonal', mass: 'advent-1', bible: 'douay-rheims', orations: 'la' }),
  invalidMass: hash({ missal: 'roman-1962', type: 'seasonal', mass: 'not-a-mass', bible: 'douay-rheims', orations: 'la' }),
  fast: hash({ missal: 'postconciliar', type: 'marian', mass: 'visitation-blessed-virgin-mary', bible: 'douay-rheims', orations: 'la' }),
  englishMultiple: hash({ missal: 'roman-1962', type: 'seasonal', mass: 'easter-sunday', bible: 'douay-rheims', orations: 'en' }),
  englishWitness: hash({ missal: 'roman-1962', type: 'seasonal', mass: 'easter-sunday', bible: 'douay-rheims', orations: 'en', 'translation-witness': MULTIPLE_TRANSLATION_WITNESS }),
  englishOne: hash({ missal: 'roman-1962', type: 'common', mass: 'commune-virginum-4', bible: 'douay-rheims', orations: 'en' }),
  englishNone: hash({ missal: 'roman-1962', type: 'sanctoral', mass: 's-hilarii-episcopi-confessoris-ecclesiae-doctoris', bible: 'douay-rheims', orations: 'en' }),
  romanChristmasForms: hash({ missal: 'roman-1962', type: 'christological', mass: 'nativitate-domini-octave', bible: 'douay-rheims', orations: 'la' }),
  romanChristmasNight: hash({ missal: 'roman-1962', type: 'christological', mass: 'nativitate-domini-octave', bible: 'douay-rheims', orations: 'la', form: 'night' }),
  postPentecostDay: hash({ missal: 'postconciliar', type: 'seasonal', mass: 'pentecost', bible: 'douay-rheims', orations: 'la', form: 'day' }),
  englishWithoutLatinBody: hash({ missal: 'roman-1962', type: 'common', mass: 'commune-virginum-4', bible: 'douay-rheims', orations: 'en' }),
  pre1955Advent: hash({ missal: 'roman-pre-1955', type: 'seasonal', mass: 'advent-1', bible: 'douay-rheims', orations: 'la' }),
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
    bible: document.querySelector('#reader-bible').value,
    orations: document.querySelector('#reader-orations').value,
    witnessHidden: document.querySelector('#reader-witness-field').hidden,
    witnessDisplay: getComputedStyle(document.querySelector('#reader-witness-field')).display,
    witnesses: [...document.querySelector('#reader-witness').options].map(row => row.value),
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
    assert.equal(value.title, 'First Sunday of Advent', JSON.stringify(value));
    assert.equal(value.outcome, 'ready');
    assert.equal(value.noticeHidden, false);
    assert.match(value.notice, /Proper text is unavailable/i);
    assert.equal(value.semantic.resolved.formulary, 'advent-1');
    assert.equal(value.semantic.events.length, 10);
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
    assert.deepEqual(await evaluate(cdp, `[...document.querySelectorAll('[data-reader-action]')].map(row => row.textContent.replace(/\\s+/g, ' ').trim())`),
      ['Browse', 'Contents', 'Mode Read', 'Details']);
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
      [STATES.cycleAUntranslated, 'rights-restricted', /rights restricted/i,
        'A Latin sibling sentinel', 'C Latin safe sibling'],
      [STATES.cycleCUntranslated, 'unavailable', /No English body is held.*cycle/i,
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
      if (unavailable === 'unavailable') assert.match(row.text, new RegExp(present));
      else assert.doesNotMatch(row.text, new RegExp(present));
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
      /Translation witness: (?:Antecedent English \(not the Missale Romanum 2002's text\): )?The Roman Missal translated into the English language/);
    assert.match(value.source, /Rights: Public Domain/);
    const row = await evaluate(cdp, `(() => {
      const event = propersReaderDebug.semantic.events.find(one =>
        one.kind === 'proper' && one.editionSlotLabel === 'Alleluia');
      if (!event) throw new Error('Alleluia semantic event is absent');
      const node = document.querySelector('[data-semantic-event-id="' + event.id + '"]');
      const composed = node && node.querySelector('.composed');
      return {
        text: node && node.textContent.replace(/\\s+/g, ' ').trim(),
        composed: composed && composed.textContent.replace(/\\s+/g, ' ').trim(),
        lang: composed && composed.lang
      };
    })()`);
    assert.match(row.composed, /This is a wise virgin, and one of the number of the prudent/);
    assert.equal(row.lang, 'en');
    assert.doesNotMatch(row.text, /Latin text unavailable|No English body is held/i);
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
      ...Array.from({ length: 10 }, (_row, index) =>
        'proper/postconciliar/pentecost/' + String(index + 17).padStart(3, '0'))
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
    assert.deepEqual(value.unresolved, [{
      id: value.choice.id, options: ['spiritus-domini', 'caritas-dei']
    }]);
    assert.deepEqual(value.domChoice, {
      group: 'entrance-antiphon', state: 'required',
      options: [['spiritus-domini', 'available'], ['caritas-dei', 'available']],
      members: ['proper/postconciliar/pentecost/015', 'proper/postconciliar/pentecost/016'],
      note: 'The source appoints one of these alternatives here. None is selected; the option groups below are not cumulative.'
    });
    assert.ok(value.semanticIds.indexOf('proper/postconciliar/pentecost/020') <
      value.semanticIds.indexOf('proper/postconciliar/pentecost/021'));
    assert.ok(value.semanticIds.indexOf('proper/postconciliar/pentecost/021') <
      value.semanticIds.indexOf('proper/postconciliar/pentecost/022'));

    const candidateProjection = await evaluate(cdp, 'propersReaderDebug.semantic');
    await current(cdp, base, STATES.postPentecostDay);
    assert.deepEqual(await evaluate(cdp, 'propersReaderDebug.semantic'), candidateProjection);
  });
  if (process.env.TRIPTYCH_P0_ONLY === '1') return;

  await check('explicit URL outranks remembered preferences', async () => {
    await evaluate(cdp, `localStorage.setItem('triptych:liturgy:propers', JSON.stringify({missal:'postconciliar',bible:'clementine-vulgate',orations:'en'}))`);
    await candidate(cdp, base, STATES.roman);
    const state = await evaluate(cdp, 'propersReaderDebug.state');
    assert.equal(state.edition.id, 'roman-1962'); assert.equal(state.bible.id, 'douay-rheims');
    assert.equal(state.languages.orations, 'la');
  });

  await check('current and candidate Roman texts, citations, and order match exactly', async () => {
    const wanted = await snapshot(cdp);
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
    assert.equal(form.witnesses.length, 3);
    assert.equal(form.witnesses[0], '');
    const witness = form.witnesses[1];
    await select(cdp, '#reader-witness', witness);
    await click(cdp, '#browse-form .surface-apply');
    await waitFor(cdp,
      `propersReaderDebug.ready && propersReaderDebug.state.languages.translationWitness === ${JSON.stringify(witness)}`,
      'explicit translation witness');
    assert.equal(await evaluate(cdp,
      `new URLSearchParams(location.hash.slice(1)).get('translation-witness')`), witness);
    assert.equal(await evaluate(cdp,
      `[...new URLSearchParams(location.hash.slice(1)).keys()].some(key => key.startsWith('_candidate-'))`), false);
  });

  await check('no held witness remains an explicit unavailable or partial result', async () => {
    await candidate(cdp, base, STATES.englishNone, NO_WITNESS_DATA);
    const value = await snapshot(cdp);
    assert.equal(value.outcome, 'ready', JSON.stringify(value.error)); assert.equal(value.noticeHidden, false);
    assert.ok(value.semantic.coverage.some(row =>
      row.state === 'unavailable' && row.scope === 'proper-translation:en'));
    assert.ok(value.texts.some(row => /No English (?:body is held|translation is recorded)/i.test(row)));
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
    const gate = armGate((path) => path.endsWith('/structure/propers/roman-1962.json'));
    await cdp.send('Page.navigate', { url: candidateUrl(base, STATES.roman) });
    await waitGate(gate);
    await waitFor(cdp, `window.propersReaderDebug && propersReaderDebug.outcome === 'loading'`,
      'Propers loading state');
    await click(cdp, '[data-reader-action="details"]');
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
    const gate = armGate((path) => path.endsWith('/browse-failure/structure/propers/roman-1962.json'));
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
      { mode: 'missal', disabled: true, checked: 'false' },
      { mode: 'study', disabled: true, checked: 'false' },
      { mode: 'compare', disabled: true, checked: 'false' }
    ]);
    await escape(cdp); await click(cdp, '[data-reader-action="details"]');
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
    assert.equal(await evaluate(cdp, `document.querySelectorAll('[data-reader-action]').length`), 4);
    assert.equal(await evaluate(cdp, 'propersReaderDebug.detailsBuilds'), 1);
    await escape(cdp);
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
      await click(cdp, `[data-reader-action="${action}"]`);
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
    assert.equal(await evaluate(cdp, `document.querySelectorAll('[data-reader-action]').length`), 4);
    assert.equal(await evaluate(cdp, `document.querySelectorAll('#reader-document .proper').length`), 10);
    await click(cdp, '[data-reader-action="details"]');
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
      actions: document.querySelectorAll('[data-reader-action]').length
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
      const gate = armGate((path) => path.endsWith('/structure/propers/roman-1962.json'));
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
    const gate = armGate((path) => path.endsWith('/browse-failure/structure/propers/roman-1962.json'));
    await cdp.send('Page.navigate', { url: candidateUrl(base, STATES.roman, DATA + '-failure') });
    await waitGate(gate); await evaluate(cdp, `location.hash=${JSON.stringify(STATES.fast.slice(1))}`);
    await waitFor(cdp, `propersReaderDebug.ready && propersReaderDebug.outcome === 'ready'`, 'fast valid after pending failure');
    gate.release(); await gate.served; await new Promise((done) => setTimeout(done, 120));
    assert.equal((await snapshot(cdp)).semantic.resolved.formulary, 'visitation-blessed-virgin-mary');
  });

  await check('Back and Forward cannot revive an older pending render', async () => {
    const gate = armGate((path) => path.endsWith('/structure/propers/roman-1962.json'));
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
    await click(cdp, `[data-reader-action="${action}"]`);
    await shot(cdp, resolve(captureDir, `propers-reader-${action}-open-393x852.png`)); await escape(cdp);
  }
  await viewport(cdp, 1440, 900); await candidate(cdp, base, STATES.roman);
  await click(cdp, '[data-reader-action="browse"]');
  await shot(cdp, resolve(captureDir, 'propers-reader-browse-open-1440x900.png')); await escape(cdp);
  await click(cdp, '[data-reader-action="details"]');
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
  await writeFile(resolve(captureDir, 'browser-results.json'), JSON.stringify({
    results, measurements, accessibility: accessibilityReport, performance: performanceReport
  }, null, 2) + '\n');
  return measurements;
}

const instance = server();
const port = await listen(instance);
const debugPort = await freePort();
const profile = await mkdtemp(resolve(tmpdir(), 'triptych-propers-reader-'));
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
  if (cdp) cdp.close(); chrome.kill('SIGTERM'); await new Promise((done) => instance.close(done));
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
