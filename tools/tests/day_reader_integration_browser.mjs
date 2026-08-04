#!/usr/bin/env node

/* Real-Chromium assertions and review captures for the W3 Day reader candidate. */

import assert from 'node:assert/strict';
import { spawn } from 'node:child_process';
import { createServer } from 'node:http';
import { mkdtemp, mkdir, readFile, stat, writeFile } from 'node:fs/promises';
import { tmpdir } from 'node:os';
import { extname, join, resolve, sep } from 'node:path';
import process from 'node:process';

const ROOT = resolve(process.env.TRIPTYCH_REVIEW_ROOT || resolve(import.meta.dirname, '../..'));
const ROUTE = '/src/web/browser/liturgy/day-reader.html';
const CURRENT = '/src/web/browser/liturgy/day.html';
const DATA = '/build/public-alpha/preview/browse';
const captureAt = process.argv.indexOf('--capture-dir');
const captureDir = captureAt >= 0 ? resolve(process.argv[captureAt + 1]) : null;
const chromeBinary = process.env.TRIPTYCH_CHROME || '/usr/bin/google-chrome-stable';
const failures = [];
const assertions = [];
const consoleProblems = [];
const failedRequests = [];
const httpProblems = [];
let activeResponseGate = null;
let gatedNavigationSequence = 0;

function armResponseGate(matches) {
  assert.equal(activeResponseGate, null, 'a response gate is already armed');
  let markStarted;
  let releaseResponse;
  let markServed;
  const gate = {
    matches,
    relative: null,
    released: false,
    started: new Promise((accept) => { markStarted = accept; }),
    releasedSignal: new Promise((accept) => { releaseResponse = accept; }),
    served: new Promise((accept) => { markServed = accept; }),
    claim(relative) {
      this.relative = relative;
      activeResponseGate = null;
      markStarted(relative);
    },
    release() {
      if (this.released) return;
      this.released = true;
      releaseResponse();
    },
    finish() { markServed(); }
  };
  activeResponseGate = gate;
  return gate;
}

async function waitForGate(gate, label) {
  await Promise.race([
    gate.started,
    new Promise((_accept, reject) => setTimeout(
      () => reject(new Error('Timed out waiting for response gate: ' + label)), 8000
    ))
  ]);
}

function mime(path) {
  return ({
    '.css': 'text/css; charset=utf-8', '.html': 'text/html; charset=utf-8',
    '.js': 'text/javascript; charset=utf-8', '.json': 'application/json',
    '.png': 'image/png', '.svg': 'image/svg+xml'
  })[extname(path)] || 'application/octet-stream';
}

async function listen(server) {
  await new Promise((accept, reject) => {
    server.once('error', reject);
    server.listen(0, '127.0.0.1', accept);
  });
  return server.address().port;
}

function staticServer() {
  return createServer(async (request, response) => {
    let claimedGate = null;
    try {
      const url = new URL(request.url, 'http://127.0.0.1');
      const relative = decodeURIComponent(url.pathname).replace(/^\/+/, '');
      if (relative === 'favicon.ico') {
        response.writeHead(204, { 'cache-control': 'no-store' });
        response.end();
        return;
      }
      if (activeResponseGate && activeResponseGate.matches(relative)) {
        claimedGate = activeResponseGate;
        claimedGate.claim(relative);
        await claimedGate.releasedSignal;
      }
      if (relative.endsWith('/structure/calendar/roman-1962/2121.json')) {
        response.writeHead(200, {
          'content-type': 'application/json', 'cache-control': 'no-store'
        });
        response.end('{');
        return;
      }
      const file = resolve(ROOT, relative || 'README.md');
      if (file !== ROOT && !file.startsWith(ROOT + sep)) throw new Error('outside root');
      const body = await readFile(file);
      response.writeHead(200, {
        'content-type': mime(file), 'cache-control': 'no-store',
        'x-robots-tag': 'noindex, nofollow'
      });
      response.end(body);
    } catch (_error) {
      response.writeHead(404, { 'content-type': 'text/plain; charset=utf-8' });
      response.end('not found');
    } finally {
      if (claimedGate) claimedGate.finish();
    }
  });
}

async function freePort() {
  const server = createServer();
  const port = await listen(server);
  await new Promise((accept) => server.close(accept));
  return port;
}

async function waitForJson(url, attempts = 100) {
  for (let attempt = 0; attempt < attempts; attempt += 1) {
    try {
      const response = await fetch(url);
      if (response.ok) return await response.json();
    } catch (_error) {
      // Chromium is still starting.
    }
    await new Promise((accept) => setTimeout(accept, 50));
  }
  throw new Error('Chromium debugging endpoint did not become ready: ' + url);
}

class CDP {
  constructor(url) {
    this.socket = new WebSocket(url);
    this.next = 0;
    this.pending = new Map();
    this.events = new Map();
  }
  async ready() {
    await new Promise((accept, reject) => {
      this.socket.addEventListener('open', accept, { once: true });
      this.socket.addEventListener('error', reject, { once: true });
    });
    this.socket.addEventListener('message', (event) => {
      const message = JSON.parse(event.data);
      if (message.id) {
        const pending = this.pending.get(message.id);
        if (!pending) return;
        this.pending.delete(message.id);
        clearTimeout(pending.timer);
        if (message.error) pending.reject(new Error(message.error.message));
        else pending.accept(message.result);
        return;
      }
      (this.events.get(message.method) || []).forEach((listener) => listener(message.params || {}));
    });
  }
  on(name, listener) {
    if (!this.events.has(name)) this.events.set(name, []);
    this.events.get(name).push(listener);
  }
  send(method, params = {}) {
    const id = ++this.next;
    return new Promise((accept, reject) => {
      const timer = setTimeout(() => {
        this.pending.delete(id);
        reject(new Error('CDP command timed out: ' + method));
      }, 20000);
      this.pending.set(id, { accept, reject, timer });
      this.socket.send(JSON.stringify({ id, method, params }));
    });
  }
  close() { this.socket.close(); }
}

async function evaluate(cdp, expression, awaitPromise = true) {
  const result = await cdp.send('Runtime.evaluate', {
    expression, awaitPromise, returnByValue: true, userGesture: true
  });
  if (result.exceptionDetails) {
    throw new Error(result.exceptionDetails.exception?.description || result.exceptionDetails.text);
  }
  return result.result.value;
}

async function waitFor(cdp, expression, label, attempts = 180) {
  for (let attempt = 0; attempt < attempts; attempt += 1) {
    if (await evaluate(cdp, `Boolean(${expression})`)) return;
    await new Promise((accept) => setTimeout(accept, 50));
  }
  throw new Error('Timed out waiting for ' + label);
}

async function viewport(cdp, width, height) {
  await cdp.send('Emulation.setDeviceMetricsOverride', {
    width, height, deviceScaleFactor: 1, mobile: width <= 768,
    screenWidth: width, screenHeight: height
  });
}

function hash(rows) {
  return '#' + new URLSearchParams(rows).toString();
}

const STATES = Object.freeze({
  roman: hash({ date: '2026-08-02', missal: 'roman-1962', bible: 'douay-rheims', orations: 'la', mass: 'pentecost-10' }),
  postconciliar: hash({ date: '2026-11-29', missal: 'postconciliar', bible: 'douay-rheims', orations: 'la', mass: 'advent-1' }),
  multiple: hash({ date: '2026-01-11', missal: 'roman-1962', bible: 'douay-rheims', orations: 'la', mass: 'comm-s-hygini-papae-martyris' }),
  partial: hash({ date: '2026-01-01', missal: 'roman-1962', bible: 'douay-rheims', orations: 'la', mass: 'octava-nativitatis-domini' }),
  deferred: hash({ date: '2026-08-02', missal: 'roman-1962', bible: 'douay-rheims', orations: 'la', ordinary: '1', 'ordinary-lang': 'en' }),
  invalid: hash({ date: '2026-08-02', missal: 'not-a-missal', bible: 'douay-rheims', orations: 'la' }),
  currentStyleLatent: hash({ date: '2026-08-02', missal: 'roman-1962', bible: 'douay-rheims', orations: 'en', rubrics: '0', 'eucharistic-prayer': 'ep-ii' }),
  ordinaryLatent: hash({ date: '2026-08-02', missal: 'roman-1962', bible: 'douay-rheims', orations: 'la', ordinary: '0', 'ordinary-lang': 'en', 'eucharistic-prayer': 'ep-ii' }),
  territorial: hash({ date: '2026-01-04', missal: 'postconciliar', bible: 'douay-rheims', orations: 'la' }),
  loadFailure: hash({ date: '2121-08-02', missal: 'roman-1962', bible: 'douay-rheims', orations: 'la' }),
  fastValid: hash({ date: '2026-11-29', missal: 'postconciliar', bible: 'clementine-vulgate', orations: 'la', mass: 'advent-1' }),
  slowYear: hash({ date: '2027-08-01', missal: 'roman-1962', bible: 'douay-rheims', orations: 'la' })
});

function candidateUrl(base, state = STATES.roman) {
  return `${base}${ROUTE}?data=${DATA}${state}`;
}

function currentUrl(base, state = STATES.roman) {
  return `${base}${CURRENT}?data=${DATA}${state}`;
}

function builtCandidateUrl(base, state = STATES.roman) {
  return `${base}/build/public-alpha/preview/liturgy/day-reader.html${state}`;
}

function builtCurrentUrl(base, state = STATES.roman) {
  return `${base}/build/public-alpha/preview/liturgy/day.html${state}`;
}

async function navigateCandidate(cdp, base, state = STATES.roman) {
  const target = candidateUrl(base, state);
  await cdp.send('Page.navigate', { url: target });
  await waitFor(cdp,
    `location.href === ${JSON.stringify(target)} && window.dayReaderReady === true`,
    'Day reader candidate');
  await new Promise((accept) => setTimeout(accept, 80));
}

async function beginGatedCandidate(cdp, base, state, matches, label) {
  const gate = armResponseGate(matches);
  gatedNavigationSequence += 1;
  const target = `${base}${ROUTE}?data=${DATA}&race=${gatedNavigationSequence}${state}`;
  try {
    await cdp.send('Page.navigate', { url: target });
    await waitForGate(gate, label);
    await waitFor(cdp,
      `location.href === ${JSON.stringify(target)} && window.dayReaderReady === false`,
      label + ' loading state');
    return gate;
  } catch (error) {
    if (activeResponseGate === gate) activeResponseGate = null;
    gate.release();
    throw error;
  }
}

async function transitionHash(cdp, state) {
  const before = await evaluate(cdp, 'window.dayReaderDebug.renders');
  await evaluate(cdp, `location.hash = ${JSON.stringify(state.replace(/^#/, ''))}`);
  await waitFor(cdp,
    `location.hash === ${JSON.stringify(state)} && window.dayReaderReady === true && ` +
      `window.dayReaderDebug.renders > ${before}`,
    'candidate hash transition');
  await new Promise((accept) => setTimeout(accept, 80));
}

async function historyMove(cdp, direction, expected) {
  const before = await evaluate(cdp, 'window.dayReaderDebug.renders');
  await evaluate(cdp, `history.${direction}()`);
  await waitFor(cdp,
    `location.hash === ${JSON.stringify(expected)} && window.dayReaderReady === true && ` +
      `window.dayReaderDebug.renders > ${before}`,
    `history ${direction}`);
  await new Promise((accept) => setTimeout(accept, 80));
}

async function settleResponseGate(cdp, gate) {
  gate.release();
  await gate.served;
  const suffix = '/' + gate.relative;
  await waitFor(cdp,
    `performance.getEntriesByType('resource').some(row => row.name.endsWith(${JSON.stringify(suffix)}))`,
    'released gated response');
  await evaluate(cdp,
    'new Promise(resolve => requestAnimationFrame(() => requestAnimationFrame(resolve)))');
}

async function candidateOutcomeSnapshot(cdp) {
  const open = await evaluate(cdp, `document.querySelector('[data-reader-surface="details"]').open`);
  if (!open) await click(cdp, '[data-reader-action="details"]');
  const value = await evaluate(cdp, `(() => ({
    title: document.querySelector('#celebration-title').textContent,
    date: document.querySelector('#celebration-date').textContent,
    metadata: document.querySelector('#celebration-meta').textContent,
    notice: document.querySelector('#coverage-notice').textContent,
    noticeHidden: document.querySelector('#coverage-notice').hidden,
    reading: document.querySelector('#reader-document').innerText,
    properText: [...document.querySelectorAll('#reader-document .proper')].map(row =>
      row.textContent.replace(/\\s+/g, ' ').trim()),
    contents: [...document.querySelectorAll('[data-reader-contents] button')].map(row => ({
      location: row.dataset.readerLocation, text: row.textContent.trim()
    })),
    dateSurface: {
      date: document.querySelector('#reader-date').value,
      missal: document.querySelector('#reader-missal').value,
      bible: document.querySelector('#reader-bible').value,
      orations: document.querySelector('#reader-orations').value,
      formulary: document.querySelector('#reader-formulary').value,
      disabled: [...document.querySelectorAll('#date-form input, #date-form select, #date-form button, #date-surface .date-steps button')]
        .every(row => row.disabled)
    },
    details: document.querySelector('[data-reader-details]').innerText,
    state: dayReaderDebug.state,
    semantic: dayReaderDebug.semantic,
    legacy: dayReaderDebug.legacy,
    deferred: dayReaderDebug.deferred,
    outcome: dayReaderDebug.outcome,
    error: dayReaderDebug.error,
    ready: dayReaderDebug.ready,
    renders: dayReaderDebug.renders
  }))()`);
  if (!open) await escape(cdp);
  return value;
}

async function navigateCurrent(cdp, base, state = STATES.roman) {
  const target = currentUrl(base, state);
  await cdp.send('Page.navigate', { url: target });
  await waitFor(cdp,
    `document.querySelector('#reading[aria-busy="false"] .proper')`,
    'current Day route');
  await new Promise((accept) => setTimeout(accept, 80));
}

async function navigateBuiltCandidate(cdp, base, state = STATES.roman) {
  const target = builtCandidateUrl(base, state);
  await cdp.send('Page.navigate', { url: target });
  await waitFor(cdp, 'window.dayReaderReady === true', 'built Day reader candidate');
  await new Promise((accept) => setTimeout(accept, 80));
}

async function navigateBuiltCurrent(cdp, base, state = STATES.roman) {
  await cdp.send('Page.navigate', { url: builtCurrentUrl(base, state) });
  await waitFor(cdp,
    `document.querySelector('#reading[aria-busy="false"] .proper')`, 'built current Day route');
  await new Promise((accept) => setTimeout(accept, 80));
}

async function click(cdp, selector) {
  await evaluate(cdp, `(() => {
    const element = document.querySelector(${JSON.stringify(selector)});
    if (!element) throw new Error('missing selector: ' + ${JSON.stringify(selector)});
    element.click(); return true;
  })()`);
  await new Promise((accept) => setTimeout(accept, 40));
}

async function escape(cdp) {
  await cdp.send('Input.dispatchKeyEvent', {
    type: 'keyDown', key: 'Escape', code: 'Escape', windowsVirtualKeyCode: 27
  });
  await cdp.send('Input.dispatchKeyEvent', {
    type: 'keyUp', key: 'Escape', code: 'Escape', windowsVirtualKeyCode: 27
  });
  await new Promise((accept) => setTimeout(accept, 50));
}

async function shot(cdp, path) {
  const result = await cdp.send('Page.captureScreenshot', {
    format: 'png', captureBeyondViewport: false, fromSurface: true
  });
  await writeFile(path, Buffer.from(result.data, 'base64'));
}

async function test(name, callback) {
  try {
    await callback();
    assertions.push({ name, status: 'pass' });
  } catch (error) {
    failures.push({ name, message: error.stack || String(error) });
    assertions.push({ name, status: 'fail', detail: error.message });
  }
}

async function surfaceOverflow(cdp, name) {
  return evaluate(cdp, `(() => {
    const root = document.querySelector('[data-reader-surface="${name}"]');
    return [root, ...root.querySelectorAll('*')].map(element => ({
      name: element.id || element.className || element.tagName,
      scrollWidth: element.scrollWidth, clientWidth: element.clientWidth
    })).filter(row => row.clientWidth > 0 && row.scrollWidth > row.clientWidth + 1);
  })()`);
}

async function metrics(cdp) {
  return evaluate(cdp, `(() => {
    const action = document.querySelector('.reader-actions');
    const documentBox = document.querySelector('#reader-document').getBoundingClientRect();
    const first = document.querySelector('#reader-document .proper, #reader-document section');
    const firstBox = first && first.getBoundingClientRect();
    const targetBoxes = [...action.querySelectorAll('button')].map(button => {
      const box = button.getBoundingClientRect();
      return { width: box.width, height: box.height };
    });
    const paragraph = document.querySelector('#reader-document .passage, #reader-document .composed');
    const style = paragraph && getComputedStyle(paragraph);
    const canvas = document.createElement('canvas');
    const context = canvas.getContext('2d');
    if (style) context.font = style.font;
    const zeroWidth = context.measureText('0').width || 8;
    const readingWidth = firstBox ? firstBox.width : documentBox.width;
    return {
      shellHeight: action.getBoundingClientRect().height,
      readingWidth,
      approximateCharactersPerLine: Math.round(readingWidth / zeroWidth),
      firstContentPosition: firstBox ? firstBox.top + scrollY : null,
      pageOverflow: document.documentElement.scrollWidth - document.documentElement.clientWidth,
      surfaceOverflow: [...document.querySelectorAll('dialog[open]')].map(dialog => ({
        id: dialog.id, overflow: dialog.scrollWidth - dialog.clientWidth
      })),
      targets: targetBoxes,
      layoutShift: performance.getEntriesByType('layout-shift').reduce((sum, entry) =>
        sum + (entry.hadRecentInput ? 0 : entry.value), 0),
      resources: performance.getEntriesByType('resource').map(row => row.name),
      scrollY
    };
  })()`);
}

async function runAssertions(cdp, base) {
  await viewport(cdp, 393, 852);
  await navigateCandidate(cdp, base);

  await test('default candidate is calm Read with real content and four persistent actions', async () => {
    const value = await evaluate(cdp, `(() => ({
      title: document.querySelector('#celebration-title').textContent,
      meta: document.querySelector('#celebration-meta').textContent,
      noticeHidden: document.querySelector('#coverage-notice').hidden,
      events: [...document.querySelectorAll('[data-semantic-event-id]')].map(row => row.dataset.semanticEventId),
      actions: [...document.querySelectorAll('[data-reader-action]')].map(row => row.textContent.trim()),
      shell: getComputedStyle(document.querySelector('.reader-actions')).position,
      first: document.querySelector('#reader-document .proper').getBoundingClientRect().top,
      viewport: innerHeight
    }))()`);
    assert.equal(value.title, 'Tenth Sunday after Pentecost');
    assert.match(value.meta, /Missale Romanum, editio typica 1962/);
    assert.doesNotMatch(value.meta, /explicit|bound M1|fixture|contract/i);
    assert.equal(value.noticeHidden, true);
    assert.equal(value.events.length, 10);
    assert.deepEqual(value.actions.map(row => row.replace(/\s+/g, ' ')),
      ['▣ Date & edition', '≡ Contents', 'R Mode Read', 'i Details']);
    assert.equal(value.shell, 'fixed');
    assert.ok(value.first < value.viewport, JSON.stringify(value));
  });

  await test('candidate semantic projection matches accepted Roman and postconciliar fixtures', async () => {
    for (const [state, file] of [
      [STATES.roman, 'day-roman-1962-2026-08-02.json'],
      [STATES.postconciliar, 'day-postconciliar-2026-11-29.json']
    ]) {
      await navigateCandidate(cdp, base, state);
      const actual = await evaluate(cdp, 'window.dayReaderDebug.semantic');
      const fixture = JSON.parse(await readFile(join(
        ROOT, 'tools/tests/fixtures/liturgy-reader-state/v1', file), 'utf8'));
      const expected = fixture.expected;
      assert.deepEqual(actual.resolved, expected.resolved);
      assert.deepEqual({
        ...actual.calendarResult,
        lectionary: actual.calendarResult.lectionary ? {
          sunday: actual.calendarResult.lectionary.sunday,
          weekday: actual.calendarResult.lectionary.weekday
        } : null
      }, expected.calendarResult);
      assert.deepEqual(actual.events.map(row => row.id), expected.events.map(row => row.id));
      assert.deepEqual(actual.events.map(row => row.editionSlotLabel),
        expected.events.map(row => row.editionSlotLabel));
      assert.deepEqual(actual.events.map(row => row.selected.references || []),
        expected.events.map(row => row.selected.references || []));
      assert.deepEqual(actual.coverage, expected.coverage);
      assert.deepEqual(actual.explicitAbsences, expected.explicitAbsences);
    }
  });

  await test('explicit readable formulary and material coverage remain explicit', async () => {
    await navigateCandidate(cdp, base, STATES.multiple);
    assert.equal(await evaluate(cdp, 'dayReaderDebug.semantic.resolved.formulary'),
      'comm-s-hygini-papae-martyris');
    assert.match(await evaluate(cdp, 'document.querySelector("#celebration-meta").textContent'), /1962/);
    await navigateCandidate(cdp, base, STATES.partial);
    const value = await evaluate(cdp, `({
      notice: document.querySelector('#coverage-notice').textContent,
      hidden: document.querySelector('#coverage-notice').hidden,
      completeness: dayReaderDebug.semantic.coverage.map(row => row.completeness)
    })`);
    assert.equal(value.hidden, false);
    assert.match(value.notice, /not held/);
    assert.ok(value.completeness.includes('partial'));
  });

  await test('invalid and deferred explicit state fail closed without silent loss', async () => {
    await navigateCandidate(cdp, base, STATES.invalid);
    assert.match(await evaluate(cdp, 'document.querySelector("#reader-document").innerText'), /did not substitute/);
    assert.equal(await evaluate(cdp, 'dayReaderDebug.semantic'), null);
    await navigateCandidate(cdp, base, STATES.deferred);
    const value = await evaluate(cdp, `(() => {
      const link = document.querySelector('.candidate-limitation a');
      return { text: document.querySelector('#reader-document').innerText,
        href: link.href, deferred: dayReaderDebug.deferred, events: document.querySelectorAll('[data-semantic-event-id]').length };
    })()`);
    assert.match(value.text, /preserved/);
    assert.match(value.href, /day\.html/);
    assert.match(value.href, /ordinary=1/);
    assert.match(value.href, /ordinary-lang=en/);
    assert.equal(value.events, 0);
  });

  await test('inactive later-mode values remain validated latent Read state', async () => {
    const supported = [
      STATES.roman,
      hash({ date: '2026-08-02', missal: 'roman-1962', bible: 'clementine-vulgate', orations: 'la', mass: 'pentecost-10' }),
      hash({ date: '2026-11-29', missal: 'postconciliar', bible: 'douay-rheims', orations: 'la', mass: 'advent-1', ordinary: '0', why: '0' }),
      hash({ date: '2026-08-02', missal: 'roman-1962', bible: 'douay-rheims', orations: 'la', rubrics: '0', why: '0' }),
      STATES.currentStyleLatent,
      STATES.ordinaryLatent
    ];
    for (const state of supported) {
      await navigateCandidate(cdp, base, state);
      assert.ok(await evaluate(cdp, 'Boolean(dayReaderDebug.semantic && dayReaderDebug.semantic.resolved)'));
      assert.deepEqual(await evaluate(cdp, 'dayReaderDebug.deferred'), []);
      assert.equal(await evaluate(cdp, 'dayReaderDebug.outcome'), 'ready');
    }
    await navigateCandidate(cdp, base, STATES.ordinaryLatent);
    const latent = await evaluate(cdp, `({
      ordinary: dayReaderDebug.state.options.ordinary,
      ordinaryLanguage: dayReaderDebug.state.languages.ordinary,
      prayer: dayReaderDebug.legacy.inert.find(row => row.key === 'eucharistic-prayer').value,
      hash: location.hash
    })`);
    assert.deepEqual(latent, {
      ordinary: false, ordinaryLanguage: 'en', prayer: 'ep-ii', hash: STATES.ordinaryLatent
    });
  });

  await test('active later-mode state defers and invalid latent state still fails closed', async () => {
    const deferred = [
      hash({ date: '2026-08-02', missal: 'roman-1962', bible: 'douay-rheims', orations: 'la', why: '1' }),
      hash({ date: '2026-08-02', missal: 'roman-1962', bible: 'douay-rheims', orations: 'la', rubrics: '1' }),
      hash({ date: '2026-08-02', missal: 'roman-1962', bible: 'douay-rheims', orations: 'la', ordinary: '1' }),
      hash({ date: '2026-11-29', missal: 'postconciliar', bible: 'douay-rheims', orations: 'la', ordinary: '1', 'eucharistic-prayer': 'ep-ii' })
    ];
    for (const state of deferred) {
      await navigateCandidate(cdp, base, state);
      assert.equal(await evaluate(cdp, 'dayReaderDebug.semantic'), null);
      assert.ok((await evaluate(cdp, 'dayReaderDebug.deferred.length')) > 0);
      assert.equal(await evaluate(cdp, 'dayReaderDebug.outcome'), 'deferred');
      assert.match(await evaluate(cdp, 'document.querySelector(".candidate-limitation a").href'), /day\.html/);
    }
    const invalid = [
      hash({ date: '2026-08-02', missal: 'roman-1962', bible: 'not-a-bible', orations: 'la' }),
      hash({ date: '2026-08-02', missal: 'roman-1962', bible: 'douay-rheims', orations: 'xx' }),
      hash({ date: '2026-08-02', missal: 'roman-1962', bible: 'douay-rheims', orations: 'la', mass: 'not-a-formulary' }),
      hash({ date: '2026-11-29', missal: 'postconciliar', bible: 'douay-rheims', orations: 'la', 'eucharistic-prayer': 'ep-99' })
    ];
    for (const state of invalid) {
      await navigateCandidate(cdp, base, state);
      assert.equal(await evaluate(cdp, 'dayReaderDebug.semantic'), null);
      assert.ok((await evaluate(cdp, 'dayReaderDebug.error.length')) > 0);
      assert.equal(await evaluate(cdp, 'dayReaderDebug.outcome'), 'invalid');
    }
  });

  await test('current-style latent URL matches live Read text, citations, and weekday', async () => {
    await navigateCandidate(cdp, base, STATES.currentStyleLatent);
    const candidate = await evaluate(cdp, `({
      title: document.querySelector('#celebration-title').textContent,
      date: document.querySelector('#celebration-date').textContent,
      propers: [...document.querySelectorAll('#reader-document .proper')].map(row =>
        row.textContent.replace(/\\s+/g, ' ').trim()),
      state: {
        rubrics: dayReaderDebug.state.apparatus.rubrics,
        ordinary: dayReaderDebug.state.options.ordinary,
        prayer: dayReaderDebug.legacy.inert.find(row => row.key === 'eucharistic-prayer').value
      }
    })`);
    await navigateCurrent(cdp, base, STATES.currentStyleLatent);
    const current = await evaluate(cdp, `({
      title: document.querySelector('#celebration-title').textContent,
      date: document.querySelector('#celebration-date').textContent,
      propers: [...document.querySelectorAll('#reading .proper')].map(row =>
        row.textContent.replace(/\\s+/g, ' ').trim())
    })`);
    assert.equal(candidate.title, current.title);
    assert.equal(candidate.date, current.date);
    assert.equal(candidate.date, 'Sunday 2 August 2026');
    assert.deepEqual(candidate.propers, current.propers);
    assert.deepEqual(candidate.state, { rubrics: false, ordinary: false, prayer: 'ep-ii' });
  });

  await test('first visit uses repository defaults without remembered or geographic state', async () => {
    await navigateCandidate(cdp, base, '');
    const state = await evaluate(cdp, 'dayReaderDebug.state');
    assert.equal(state.edition.id, 'roman-1962');
    assert.equal(state.bible.id, 'douay-rheims');
    assert.equal(state.languages.orations, 'la');
    assert.equal(state.options.ordinary, false);
    assert.equal(state.requestedMode, 'read');
    assert.equal(await evaluate(cdp, 'document.querySelector("#coverage-notice").hidden'), true);
  });

  await test('URL state outranks storage and locality is never inferred', async () => {
    await evaluate(cdp, `localStorage.setItem('triptych:liturgy:day', JSON.stringify({
      missal: 'postconciliar', bible: 'king-james-version', date: '2026-11-29'
    }))`);
    await navigateCandidate(cdp, base, STATES.roman);
    const state = await evaluate(cdp, 'dayReaderDebug.state');
    assert.equal(state.edition.id, 'roman-1962');
    assert.equal(state.bible.id, 'douay-rheims');
    assert.equal(state.civilDate, '2026-08-02');
    assert.equal(await evaluate(cdp, `'geolocation' in dayReaderDebug`), false);
  });

  await test('active and latent state remain distinct through Back and Forward', async () => {
    const active = hash({
      date: '2026-08-02', missal: 'roman-1962', bible: 'douay-rheims',
      orations: 'en', rubrics: '1', 'eucharistic-prayer': 'ep-ii'
    });
    await navigateCandidate(cdp, base, STATES.currentStyleLatent);
    await transitionHash(cdp, active);
    assert.equal(await evaluate(cdp, 'dayReaderDebug.outcome'), 'deferred');
    await historyMove(cdp, 'back', STATES.currentStyleLatent);
    assert.equal(await evaluate(cdp, 'dayReaderDebug.outcome'), 'ready');
    assert.equal(await evaluate(cdp, 'dayReaderDebug.state.apparatus.rubrics'), false);
    assert.equal(await evaluate(cdp,
      `dayReaderDebug.legacy.inert.find(row => row.key === 'eucharistic-prayer').value`), 'ep-ii');
    await historyMove(cdp, 'forward', active);
    assert.equal(await evaluate(cdp, 'dayReaderDebug.outcome'), 'deferred');
  });

  await test('failed and unresolved transitions cannot expose prior selection state', async () => {
    const stalePattern = /Tenth Sunday|2026-08-02|Missale Romanum|pentecost-10|Universal|proper-structure|Resolved Day result/i;
    await navigateCandidate(cdp, base, STATES.roman);
    await transitionHash(cdp, STATES.invalid);
    assert.equal(await evaluate(cdp, 'dayReaderDebug.outcome'), 'invalid');
    assert.equal(await evaluate(cdp, 'dayReaderDebug.state'), null);
    await click(cdp, '[data-reader-action="date"]');
    const invalidDate = await evaluate(cdp, `({
      text: document.querySelector('#date-surface').innerText,
      values: [...document.querySelectorAll('#date-form input, #date-form select')].map(row => row.value),
      disabled: [...document.querySelectorAll('#date-form input, #date-form select, #date-form button, #date-surface .date-steps button')].every(row => row.disabled)
    })`);
    assert.doesNotMatch(invalidDate.text, stalePattern);
    assert.ok(invalidDate.values.every(value => value === ''), JSON.stringify(invalidDate));
    assert.equal(invalidDate.disabled, true);
    await escape(cdp);
    await click(cdp, '[data-reader-action="details"]');
    const invalidDetails = await evaluate(cdp, `document.querySelector('[data-reader-details]').innerText`);
    assert.match(invalidDetails, /No validated selection.*invalid outcome/i);
    assert.doesNotMatch(invalidDetails, stalePattern);
    await escape(cdp);

    await historyMove(cdp, 'back', STATES.roman);
    assert.equal(await evaluate(cdp, 'dayReaderDebug.outcome'), 'ready');
    assert.equal(await evaluate(cdp, `document.querySelector('#celebration-title').textContent`),
      'Tenth Sunday after Pentecost');

    await transitionHash(cdp, STATES.loadFailure);
    assert.equal(await evaluate(cdp, 'dayReaderDebug.outcome'), 'failed');
    assert.equal(await evaluate(cdp, 'dayReaderDebug.state'), null);
    await click(cdp, '[data-reader-action="details"]');
    const failedDetails = await evaluate(cdp, `document.querySelector('[data-reader-details]').innerText`);
    assert.match(failedDetails, /No validated selection.*failed outcome/i);
    assert.doesNotMatch(failedDetails, stalePattern);
    await escape(cdp);

    await historyMove(cdp, 'back', STATES.roman);
    await transitionHash(cdp, STATES.territorial);
    assert.equal(await evaluate(cdp, 'dayReaderDebug.outcome'), 'territorial-choice');
    assert.equal(await evaluate(cdp, 'dayReaderDebug.semantic'), null);
    await click(cdp, '[data-reader-action="details"]');
    const territorial = await evaluate(cdp, `document.querySelector('[data-reader-details]').innerText`);
    assert.match(territorial, /2026-01-04/);
    assert.match(territorial, /Choice required/);
    assert.doesNotMatch(territorial, /Universal|Tenth Sunday|pentecost-10|Resolved Day result|proper-structure/i);
    await escape(cdp);
  });

  await test('deferred state returns to valid Read and forward restores deferral', async () => {
    await navigateCandidate(cdp, base, STATES.roman);
    await transitionHash(cdp, STATES.deferred);
    assert.equal(await evaluate(cdp, 'dayReaderDebug.outcome'), 'deferred');
    await historyMove(cdp, 'back', STATES.roman);
    assert.equal(await evaluate(cdp, 'dayReaderDebug.outcome'), 'ready');
    assert.equal(await evaluate(cdp, 'dayReaderDebug.semantic.resolved.formulary'), 'pentecost-10');
    await historyMove(cdp, 'forward', STATES.deferred);
    assert.equal(await evaluate(cdp, 'dayReaderDebug.outcome'), 'deferred');
    assert.equal(await evaluate(cdp, 'dayReaderDebug.semantic'), null);
  });

  await test('a superseded slow valid render cannot overwrite a newer valid result', async () => {
    const gate = await beginGatedCandidate(
      cdp, base, STATES.roman,
      (relative) => relative.endsWith('/douay-rheims/chapters/Ps/54.json'),
      'slow valid scripture fragment'
    );
    try {
      await transitionHash(cdp, STATES.fastValid);
      const before = await candidateOutcomeSnapshot(cdp);
      assert.equal(before.outcome, 'ready');
      assert.equal(before.title, 'First Sunday of Advent');
      assert.equal(before.state.edition.id, 'postconciliar');
      assert.equal(before.semantic.resolved.formulary, 'advent-1');
      assert.ok(before.properText.length > 0);
      await settleResponseGate(cdp, gate);
      const after = await candidateOutcomeSnapshot(cdp);
      assert.deepEqual(after, before);
    } finally {
      gate.release();
    }
  });

  await test('a superseded slow failure cannot replace a newer valid result', async () => {
    const gate = await beginGatedCandidate(
      cdp, base, STATES.loadFailure,
      (relative) => relative.endsWith('/structure/calendar/roman-1962/2121.json'),
      'slow malformed calendar response'
    );
    try {
      await transitionHash(cdp, STATES.fastValid);
      const before = await candidateOutcomeSnapshot(cdp);
      assert.equal(before.outcome, 'ready');
      assert.equal(before.title, 'First Sunday of Advent');
      assert.equal(before.dateSurface.disabled, false);
      await settleResponseGate(cdp, gate);
      const after = await candidateOutcomeSnapshot(cdp);
      assert.deepEqual(after, before);
      assert.doesNotMatch(after.reading, /could not load|invalid JSON|Selection unavailable/i);
    } finally {
      gate.release();
    }
  });

  await test('a superseded slow valid render cannot overwrite a newer invalid result', async () => {
    const gate = await beginGatedCandidate(
      cdp, base, STATES.roman,
      (relative) => relative.endsWith('/douay-rheims/chapters/Ps/54.json'),
      'slow valid before invalid state'
    );
    try {
      await transitionHash(cdp, STATES.invalid);
      const before = await candidateOutcomeSnapshot(cdp);
      assert.equal(before.outcome, 'invalid');
      assert.equal(before.semantic, null);
      assert.equal(before.dateSurface.disabled, true);
      assert.deepEqual(before.contents, []);
      await settleResponseGate(cdp, gate);
      const after = await candidateOutcomeSnapshot(cdp);
      assert.deepEqual(after, before);
      assert.doesNotMatch(after.reading, /But I have cried to God|Tenth Sunday after Pentecost/i);
    } finally {
      gate.release();
    }
  });

  await test('history navigation owns the final state while an older render is loading', async () => {
    await navigateCandidate(cdp, base, STATES.roman);
    const gate = armResponseGate(
      (relative) => relative.endsWith('/structure/calendar/roman-1962/2027.json')
    );
    try {
      await evaluate(cdp, `location.hash = ${JSON.stringify(STATES.slowYear.replace(/^#/, ''))}`);
      await waitForGate(gate, 'slow history calendar response');
      await historyMove(cdp, 'back', STATES.roman);
      const before = await candidateOutcomeSnapshot(cdp);
      assert.equal(before.outcome, 'ready');
      assert.equal(before.state.civilDate, '2026-08-02');
      assert.equal(before.semantic.resolved.formulary, 'pentecost-10');
      await settleResponseGate(cdp, gate);
      const after = await candidateOutcomeSnapshot(cdp);
      assert.deepEqual(after, before);
      assert.equal(await evaluate(cdp, 'location.hash'), STATES.roman);
    } finally {
      if (activeResponseGate === gate) activeResponseGate = null;
      gate.release();
    }
  });

  await test('all actions preserve deep scroll, modal focus, Escape, and focus return', async () => {
    await navigateCandidate(cdp, base);
    await evaluate(cdp, 'window.scrollTo(0, document.documentElement.scrollHeight - innerHeight - 80)');
    const start = await evaluate(cdp, 'window.scrollY');
    assert.ok(start > 500);
    for (const name of ['date', 'contents', 'mode', 'details']) {
      await click(cdp, `[data-reader-action="${name}"]`);
      const open = await evaluate(cdp, `(() => ({
        modal: document.querySelector('[data-reader-surface="${name}"]').matches(':modal'),
        focus: document.activeElement.hasAttribute('data-reader-close'),
        expanded: document.querySelector('[data-reader-action="${name}"]').getAttribute('aria-expanded')
      }))()`);
      assert.deepEqual(open, { modal: true, focus: true, expanded: 'true' });
      await escape(cdp);
      const closed = await evaluate(cdp, `(() => ({
        focus: document.activeElement.dataset.readerAction,
        expanded: document.querySelector('[data-reader-action="${name}"]').getAttribute('aria-expanded'),
        scroll: window.scrollY
      }))()`);
      assert.equal(closed.focus, name);
      assert.equal(closed.expanded, 'false');
      assert.ok(Math.abs(closed.scroll - start) <= 2, JSON.stringify(closed));
    }
  });

  await test('Contents follows real semantic sections and moves focus to the selected text', async () => {
    await navigateCandidate(cdp, base);
    await evaluate(cdp, `document.querySelectorAll('[data-semantic-event-id]')[5].scrollIntoView()`);
    await new Promise((accept) => setTimeout(accept, 80));
    await click(cdp, '[data-reader-action="contents"]');
    const current = await evaluate(cdp,
      `document.querySelector('[data-reader-contents] [aria-current="location"]').dataset.readerLocation`);
    assert.match(current, /^proper\/roman-1962\/pentecost-10\//);
    await click(cdp, '[data-reader-contents] button:last-child');
    assert.equal(await evaluate(cdp,
      'document.activeElement.dataset.semanticEventId'), 'proper/roman-1962/pentecost-10/010');
  });

  await test('only Read is selectable and Details stays lazy and human-facing', async () => {
    await navigateCandidate(cdp, base);
    const buildsBefore = await evaluate(cdp, 'dayReaderDebug.detailsBuilds');
    assert.match(await evaluate(cdp, 'document.querySelector("[data-reader-details]").innerText'),
      /load when this surface is opened/i);
    await click(cdp, '[data-reader-action="mode"]');
    const before = await evaluate(cdp, 'JSON.stringify(dayReaderDebug.state)');
    const modes = await evaluate(cdp, `[...document.querySelectorAll('.mode-options button')].map(row => ({
      name: row.querySelector('strong').textContent, disabled: row.disabled, checked: row.getAttribute('aria-checked')
    }))`);
    assert.deepEqual(modes, [
      { name: 'Read', disabled: false, checked: 'true' },
      { name: 'Missal', disabled: true, checked: 'false' },
      { name: 'Study', disabled: true, checked: 'false' },
      { name: 'Compare', disabled: true, checked: 'false' }
    ]);
    await escape(cdp);
    await click(cdp, '[data-reader-action="details"]');
    const details = await evaluate(cdp, `({
      builds: dayReaderDebug.detailsBuilds,
      text: document.querySelector('[data-reader-details]').innerText,
      state: JSON.stringify(dayReaderDebug.state)
    })`);
    assert.equal(details.builds, buildsBefore + 1);
    assert.doesNotMatch(details.text, /triptych-liturgy-reader-state|\{|\}|bound M1|machine envelope/i);
    assert.doesNotMatch(details.text,
      /proper-structure|roman-1962\/pentecost-10|\/\d{3}\b|Available source identities/i);
    assert.equal(details.state, before);
  });

  await test('every auxiliary surface reflows at required widths and 200-percent text', async () => {
    const sizes = [[1440, 900], [1024, 768], [768, 1024], [393, 852], [320, 852]];
    for (const [width, height] of sizes) {
      await viewport(cdp, width, height);
      await navigateCandidate(cdp, base);
      for (const name of ['date', 'contents', 'mode', 'details']) {
        await click(cdp, `[data-reader-action="${name}"]`);
        assert.deepEqual(await surfaceOverflow(cdp, name), [], `${name} ${width}x${height}`);
        await escape(cdp);
      }
      const page = await evaluate(cdp,
        'document.documentElement.scrollWidth - document.documentElement.clientWidth');
      assert.ok(page <= 0, `${width}x${height} page overflow ${page}`);
    }
    await viewport(cdp, 393, 852);
    await navigateCandidate(cdp, base, STATES.multiple);
    await evaluate(cdp, `document.documentElement.style.fontSize = '200%'`);
    for (const name of ['date', 'contents', 'mode', 'details']) {
      await click(cdp, `[data-reader-action="${name}"]`);
      assert.deepEqual(await surfaceOverflow(cdp, name), [], `${name} at 200%`);
      await escape(cdp);
    }
    assert.ok(await evaluate(cdp,
      'document.documentElement.scrollWidth - document.documentElement.clientWidth') <= 0);
    await evaluate(cdp, `document.documentElement.style.fontSize = ''`);
  });

  await test('Back restores the prior semantic selection and data files load once', async () => {
    await viewport(cdp, 393, 852);
    await navigateCandidate(cdp, base);
    await click(cdp, '[data-reader-action="date"]');
    await click(cdp, '#next-date');
    await waitFor(cdp, 'dayReaderReady && dayReaderDebug.state.civilDate === "2026-08-03"', 'next date');
    await evaluate(cdp, 'history.back()');
    await waitFor(cdp, 'dayReaderReady && dayReaderDebug.state.civilDate === "2026-08-02"', 'Back date');
    const loads = await evaluate(cdp, 'dayReaderDebug.loads');
    assert.ok(Object.values(loads).every(count => count === 1), JSON.stringify(loads));
  });

  await test('candidate and current Day select the same visible identity and Proper order', async () => {
    await viewport(cdp, 1024, 768);
    await navigateCandidate(cdp, base);
    const candidate = await evaluate(cdp, `({
      title: document.querySelector('#celebration-title').textContent,
      names: [...document.querySelectorAll('#reader-document .proper-name')].map(row => row.childNodes[0].textContent.trim())
    })`);
    await navigateCurrent(cdp, base);
    const current = await evaluate(cdp, `({
      title: document.querySelector('#celebration-title').textContent,
      names: [...document.querySelectorAll('#reading .proper-name')].map(row => row.childNodes[0].textContent.trim())
    })`);
    assert.equal(candidate.title, current.title);
    assert.deepEqual(candidate.names, current.names);
    assert.equal(await evaluate(cdp, 'document.querySelectorAll("[data-reader-shell]").length'), 0);
  });

  await test('normal preview build contains a noindex candidate but no candidate navigation link', async () => {
    const target = `${base}/build/public-alpha/preview/liturgy/day-reader.html${STATES.roman}`;
    await cdp.send('Page.navigate', { url: target });
    await waitFor(cdp, 'window.dayReaderReady === true', 'built candidate route');
    const value = await evaluate(cdp, `({
      robots: document.querySelector('meta[name="robots"]').content,
      title: document.querySelector('#celebration-title').textContent,
      pageClass: document.querySelector('#main-content').className,
      navLinks: [...document.querySelectorAll('header a, footer a')].filter(row => /day-reader/.test(row.href)).length
    })`);
    assert.match(value.robots, /noindex/);
    assert.equal(value.title, 'Tenth Sunday after Pentecost');
    assert.match(value.pageClass, /day-reader-candidate/);
    assert.equal(value.navLinks, 0);
  });

  await test('print removes candidate and shell chrome while retaining identity and context', async () => {
    await navigateCandidate(cdp, base);
    await cdp.send('Emulation.setEmulatedMedia', { media: 'print' });
    const value = await evaluate(cdp, `({
      actions: getComputedStyle(document.querySelector('.reader-actions')).display,
      flag: getComputedStyle(document.querySelector('.candidate-flag')).display,
      title: document.querySelector('#celebration-title').textContent,
      meta: document.querySelector('#celebration-meta').textContent,
      properCount: document.querySelectorAll('#reader-document .proper').length
    })`);
    assert.equal(value.actions, 'none');
    assert.equal(value.flag, 'none');
    assert.equal(value.title, 'Tenth Sunday after Pentecost');
    assert.match(value.meta, /Universal/);
    assert.equal(value.properCount, 10);
    await cdp.send('Emulation.setEmulatedMedia', { media: 'screen' });
  });

  await test('reduced motion and final focused content retain accepted boundaries', async () => {
    await cdp.send('Emulation.setEmulatedMedia', {
      media: 'screen', features: [{ name: 'prefers-reduced-motion', value: 'reduce' }]
    });
    await navigateCandidate(cdp, base);
    const behavior = await evaluate(cdp, 'getComputedStyle(document.documentElement).scrollBehavior');
    assert.notEqual(behavior, 'smooth');
    await evaluate(cdp, `(() => {
      const last = document.querySelector('#reader-document .proper:last-child');
      last.scrollIntoView({block: 'end'}); last.focus({preventScroll: true});
    })()`);
    const boxes = await evaluate(cdp, `(() => ({
      last: document.querySelector('#reader-document .proper:last-child').getBoundingClientRect().bottom,
      shell: document.querySelector('.reader-actions').getBoundingClientRect().top
    }))()`);
    assert.ok(boxes.last <= boxes.shell + 1, JSON.stringify(boxes));
    await cdp.send('Emulation.setEmulatedMedia', { media: 'screen' });
  });
}

async function captureCandidate(cdp, base, state, kind) {
  await navigateBuiltCandidate(cdp, base, state);
  await evaluate(cdp, 'window.scrollTo(0, 0)');
  if (kind === 'deep') {
    await evaluate(cdp, 'window.scrollTo(0, document.documentElement.scrollHeight - innerHeight - 8)');
  } else if (['date', 'contents', 'mode', 'details'].includes(kind)) {
    await click(cdp, `[data-reader-action="${kind}"]`);
  }
  await new Promise((accept) => setTimeout(accept, 80));
}

async function captureMatrix(cdp, base, directory) {
  await mkdir(directory, { recursive: true });
  const sizes = [[1440, 900], [1024, 768], [768, 1024], [393, 852], [320, 852]];
  const cases = [
    ['default', STATES.roman, 'top'], ['deep', STATES.roman, 'deep'],
    ['date', STATES.roman, 'date'], ['contents', STATES.roman, 'contents'],
    ['mode', STATES.roman, 'mode'], ['details', STATES.roman, 'details'],
    ['deferred-ordinary', STATES.deferred, 'top'], ['partial', STATES.partial, 'top'],
    ['invalid', STATES.invalid, 'top']
  ];
  const measures = [];
  for (const [width, height] of sizes) {
    await viewport(cdp, width, height);
    for (const [name, state, kind] of cases) {
      await captureCandidate(cdp, base, state, kind);
      const file = `day-reader-${name}-${width}x${height}.png`;
      await shot(cdp, join(directory, file));
      measures.push({ file, viewport: `${width}x${height}`, state: name, metrics: await metrics(cdp) });
      if (await evaluate(cdp, 'Boolean(document.querySelector("dialog[open]"))')) await escape(cdp);
    }
    await navigateBuiltCurrent(cdp, base);
    const currentFile = `day-current-default-${width}x${height}.png`;
    await shot(cdp, join(directory, currentFile));
  }

  await viewport(cdp, 393, 852);
  await navigateBuiltCandidate(cdp, base, STATES.multiple);
  await evaluate(cdp, 'window.scrollTo(0, 0)');
  await evaluate(cdp, `document.documentElement.style.fontSize = '200%'`);
  await click(cdp, '[data-reader-action="date"]');
  await shot(cdp, join(directory, 'day-reader-date-200-percent-393x852.png'));
  measures.push({ file: 'day-reader-date-200-percent-393x852.png', viewport: '393x852',
    state: 'date-200-percent', metrics: await metrics(cdp) });
  await evaluate(cdp, `document.documentElement.style.fontSize = ''`);
  await escape(cdp);

  await viewport(cdp, 393, 852);
  await navigateBuiltCandidate(cdp, base, STATES.currentStyleLatent);
  await shot(cdp, join(directory, 'day-reader-latent-current-url-393x852.png'));
  await navigateBuiltCandidate(cdp, base, STATES.roman);
  await transitionHash(cdp, STATES.invalid);
  await click(cdp, '[data-reader-action="date"]');
  await shot(cdp, join(directory, 'day-reader-transition-invalid-date-393x852.png'));
  await escape(cdp);
  await click(cdp, '[data-reader-action="details"]');
  await shot(cdp, join(directory, 'day-reader-transition-invalid-details-393x852.png'));
  await escape(cdp);

  await viewport(cdp, 1024, 768);
  await navigateBuiltCandidate(cdp, base);
  await evaluate(cdp, 'window.scrollTo(0, 0)');
  await cdp.send('Emulation.setEmulatedMedia', { media: 'print' });
  const pdf = await cdp.send('Page.printToPDF', {
    printBackground: true, preferCSSPageSize: true, paperWidth: 8.5, paperHeight: 11,
    marginTop: 0.4, marginBottom: 0.4, marginLeft: 0.45, marginRight: 0.45
  });
  await writeFile(join(directory, 'day-reader-print.pdf'), Buffer.from(pdf.data, 'base64'));
  await cdp.send('Emulation.setEmulatedMedia', { media: 'screen' });
  await writeFile(join(directory, 'measurements.json'), JSON.stringify(measures, null, 2) + '\n');
  return measures;
}

async function main() {
  const server = staticServer();
  const serverPort = await listen(server);
  const base = `http://127.0.0.1:${serverPort}`;
  const debugPort = await freePort();
  const profile = await mkdtemp(join(tmpdir(), 'triptych-day-reader-chrome-'));
  const chrome = spawn(chromeBinary, [
    '--headless=new', '--no-sandbox', '--disable-dev-shm-usage', '--disable-gpu',
    `--remote-debugging-port=${debugPort}`, `--user-data-dir=${profile}`,
    '--no-first-run', '--no-default-browser-check', 'about:blank'
  ], { stdio: ['ignore', 'ignore', 'pipe'] });
  let chromeStderr = '';
  chrome.stderr.on('data', (chunk) => { chromeStderr += chunk.toString(); });
  let cdp;
  try {
    await waitForJson(`http://127.0.0.1:${debugPort}/json/version`);
    const response = await fetch(
      `http://127.0.0.1:${debugPort}/json/new?${encodeURIComponent('about:blank')}`,
      { method: 'PUT' }
    );
    const page = await response.json();
    cdp = new CDP(page.webSocketDebuggerUrl);
    await cdp.ready();
    await Promise.all([
      cdp.send('Page.enable'), cdp.send('Runtime.enable'), cdp.send('Network.enable'),
      cdp.send('Accessibility.enable'), cdp.send('Performance.enable')
    ]);
    cdp.on('Runtime.consoleAPICalled', ({ type, args }) => {
      if (type === 'error') consoleProblems.push({
        type, text: args.map((arg) => arg.value || arg.description || '').join(' ')
      });
    });
    cdp.on('Network.loadingFailed', (event) => failedRequests.push({
      requestId: event.requestId, error: event.errorText, canceled: Boolean(event.canceled)
    }));
    cdp.on('Network.responseReceived', ({ response: held }) => {
      if (held.status >= 400) httpProblems.push({ status: held.status, url: held.url });
    });

    await runAssertions(cdp, base);
    const captures = captureDir ? await captureMatrix(cdp, base, captureDir) : [];
    await viewport(cdp, 393, 852);
    await navigateBuiltCandidate(cdp, base);
    await evaluate(cdp, 'window.scrollTo(0, 0)');
    const measured = await metrics(cdp);
    const ax = await cdp.send('Accessibility.getFullAXTree');
    const report = {
      generatedAt: new Date().toISOString(),
      chrome: (await waitForJson(`http://127.0.0.1:${debugPort}/json/version`)).Browser,
      assertions, failures, consoleProblems, failedRequests, httpProblems,
      accessibility: {
        nodeCount: ax.nodes.length,
        unnamedInteractiveNodes: ax.nodes.filter((node) =>
          ['button', 'link', 'radio'].includes(node.role?.value) && !node.name?.value).length
      },
      performance: {
        metrics: measured,
        resourceCount: measured.resources.length,
        duplicateResources: measured.resources.filter((url, index, all) => all.indexOf(url) !== index)
      },
      captures: captures.length,
      files: {
        shellJavaScript: (await stat(join(ROOT, 'src/web/browser/liturgy/reader-shell.js'))).size,
        candidateJavaScript: (await stat(join(ROOT, 'src/web/browser/liturgy/day-reader.js'))).size,
        shellCss: (await stat(join(ROOT, 'src/web/browser/liturgy/reader-shell.css'))).size,
        candidateCss: (await stat(join(ROOT, 'src/web/browser/liturgy/day-reader.css'))).size
      }
    };
    if (captureDir) {
      await writeFile(join(captureDir, 'browser-results.json'), JSON.stringify(report, null, 2) + '\n');
    }
    process.stdout.write(JSON.stringify(report, null, 2) + '\n');
    if (failures.length || consoleProblems.length ||
        failedRequests.some(row => !row.canceled) || httpProblems.length ||
        report.accessibility.unnamedInteractiveNodes) process.exitCode = 1;
  } catch (error) {
    process.stderr.write((error.stack || String(error)) + '\n' + chromeStderr.slice(-4000));
    process.exitCode = 1;
  } finally {
    if (cdp) cdp.close();
    const exited = new Promise((accept) => chrome.once('exit', accept));
    chrome.kill('SIGTERM');
    await exited;
    await new Promise((accept) => server.close(accept));
  }
}

await main();
