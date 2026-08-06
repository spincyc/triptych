#!/usr/bin/env node

/* Real-Chromium assertions and review captures for the W3 Day reader candidate. */

import assert from 'node:assert/strict';
import { spawn } from 'node:child_process';
import { createServer } from 'node:http';
import { mkdtemp, mkdir, readFile, rm, writeFile } from 'node:fs/promises';
import { extname, join, resolve, sep } from 'node:path';
import process from 'node:process';
import { gzipSync } from 'node:zlib';

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
let freshNavigationSequence = 0;
let currentDocumentToken = null;

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
    this.sessionId = null;
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
    return () => {
      const listeners = this.events.get(name) || [];
      this.events.set(name, listeners.filter((candidate) => candidate !== listener));
    };
  }
  send(method, params = {}) {
    const id = ++this.next;
    return new Promise((accept, reject) => {
      const timer = setTimeout(() => {
        this.pending.delete(id);
        reject(new Error('CDP command timed out: ' + method));
      }, 60000);
      this.pending.set(id, { accept, reject, timer });
      const message = { id, method, params };
      if (this.sessionId) message.sessionId = this.sessionId;
      this.socket.send(JSON.stringify(message));
    });
  }
  close() { this.socket.close(); }
}

async function evaluate(cdp, expression, awaitPromise = true) {
  let result;
  try {
    result = await cdp.send('Runtime.evaluate', {
      expression, awaitPromise, returnByValue: true, userGesture: true
    });
  } catch (error) {
    throw new Error(`${error.message}; expression: ${expression.slice(0, 180)}`);
  }
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
  romanMissal: hash({ date: '2026-08-02', missal: 'roman-1962', bible: 'douay-rheims', orations: 'la', mass: 'pentecost-10', ordinary: '1', 'ordinary-lang': 'en', rubrics: '1', why: '0' }),
  romanLatinMissal: hash({ date: '2026-08-02', missal: 'roman-1962', bible: 'douay-rheims', orations: 'la', mass: 'pentecost-10', ordinary: '1', 'ordinary-lang': 'la', rubrics: '1', why: '0' }),
  postconciliar: hash({ date: '2026-11-29', missal: 'postconciliar', bible: 'douay-rheims', orations: 'la', mass: 'advent-1' }),
  postReadLatent: hash({ date: '2026-11-29', missal: 'postconciliar', bible: 'douay-rheims', orations: 'la', mass: 'advent-1', ordinary: '0', 'ordinary-lang': 'en', rubrics: '0', why: '0', 'eucharistic-prayer': 'ep-ii' }),
  postMissal: hash({ date: '2026-11-29', missal: 'postconciliar', bible: 'douay-rheims', orations: 'la', mass: 'advent-1', ordinary: '1', 'ordinary-lang': 'en', rubrics: '1', why: '0', 'eucharistic-prayer': 'ep-ii' }),
  multiple: hash({ date: '2026-01-11', missal: 'roman-1962', bible: 'douay-rheims', orations: 'la', mass: 'comm-s-hygini-papae-martyris' }),
  partial: hash({ date: '2026-01-01', missal: 'roman-1962', bible: 'douay-rheims', orations: 'la', mass: 'octava-nativitatis-domini', ordinary: '1', 'ordinary-lang': 'en', rubrics: '1' }),
  missingSeat: hash({ date: '2026-02-18', missal: 'roman-1962', bible: 'douay-rheims', orations: 'la', mass: 'ash-wednesday', ordinary: '1', 'ordinary-lang': 'en', rubrics: '1' }),
  deferred: hash({ date: '2026-08-02', missal: 'roman-1962', bible: 'douay-rheims', orations: 'la', mass: 'pentecost-10', ordinary: '1', why: '1' }),
  invalid: hash({ date: '2026-08-02', missal: 'not-a-missal', bible: 'douay-rheims', orations: 'la' }),
  currentStyleLatent: hash({ date: '2026-11-29', missal: 'postconciliar', bible: 'douay-rheims', orations: 'la', mass: 'advent-1', ordinary: '0', 'ordinary-lang': 'en', rubrics: '0', 'eucharistic-prayer': 'ep-ii' }),
  ordinaryLatent: hash({ date: '2026-08-02', missal: 'roman-1962', bible: 'douay-rheims', orations: 'la', mass: 'pentecost-10', ordinary: '0', 'ordinary-lang': 'en', rubrics: '1' }),
  invalidPrayer: hash({ date: '2026-11-29', missal: 'postconciliar', bible: 'douay-rheims', orations: 'la', mass: 'advent-1', ordinary: '1', 'ordinary-lang': 'en', 'eucharistic-prayer': 'ep-99' }),
  inapplicablePrayer: hash({ date: '2026-08-02', missal: 'roman-1962', bible: 'douay-rheims', orations: 'la', mass: 'pentecost-10', ordinary: '1', 'ordinary-lang': 'en', 'eucharistic-prayer': 'ep-ii' }),
  invalidOrdinaryLanguage: hash({ date: '2026-08-02', missal: 'roman-1962', bible: 'douay-rheims', orations: 'la', mass: 'pentecost-10', ordinary: '1', 'ordinary-lang': 'fr' }),
  invalidOrdinary: hash({ date: '2026-08-02', missal: 'roman-1962', bible: 'douay-rheims', orations: 'la', mass: 'pentecost-10', ordinary: 'sometimes' }),
  territorial: hash({ date: '2026-01-04', missal: 'postconciliar', bible: 'douay-rheims', orations: 'la' }),
  loadFailure: hash({ date: '2121-08-02', missal: 'roman-1962', bible: 'douay-rheims', orations: 'la' }),
  fastValid: hash({ date: '2026-11-29', missal: 'postconciliar', bible: 'clementine-vulgate', orations: 'la', mass: 'advent-1' }),
  slowYear: hash({ date: '2027-08-01', missal: 'roman-1962', bible: 'douay-rheims', orations: 'la' })
});

const DUPLICATE_ORDINARY_STATES = Object.freeze({
  readThenMissal: STATES.roman + '&ordinary=0&ordinary=1',
  missalThenRead: STATES.roman + '&ordinary=1&ordinary=0'
});

function candidateUrl(base, state = STATES.roman, nonce = null) {
  const review = nonce === null ? '' : `&review-document=${encodeURIComponent(nonce)}`;
  return `${base}${ROUTE}?data=${DATA}${review}${state}`;
}

function currentUrl(base, state = STATES.roman, nonce = null) {
  const review = nonce === null ? '' : `&review-document=${encodeURIComponent(nonce)}`;
  return `${base}${CURRENT}?data=${DATA}${review}${state}`;
}

function builtCandidateUrl(base, state = STATES.roman, nonce = null) {
  const review = nonce === null ? '' : `?review-document=${encodeURIComponent(nonce)}`;
  return `${base}/build/public-alpha/preview/liturgy/day-reader.html${review}${state}`;
}

function builtCurrentUrl(base, state = STATES.roman, nonce = null) {
  const review = nonce === null ? '' : `?review-document=${encodeURIComponent(nonce)}`;
  return `${base}/build/public-alpha/preview/liturgy/day.html${review}${state}`;
}

async function waitForVisualSettlement(cdp, options = {}) {
  const config = {
    semanticEventId: options.semanticEventId || null,
    focus: options.focus || null,
    requireTargetInViewport: Boolean(options.semanticEventId),
    requireFocusInViewport: Boolean(options.focus),
    requiredStableFrames: options.requiredStableFrames || 5,
    tolerance: options.tolerance ?? 1,
    timeoutMs: options.timeoutMs || 8000
  };
  const result = await evaluate(cdp, `(async () => {
    const config = ${JSON.stringify(config)};
    const started = performance.now();
    let previous = null;
    let stableFrames = 0;
    let sampledFrames = 0;
    let last = null;
    function rectangle(element) {
      if (!element) return null;
      const box = element.getBoundingClientRect();
      return { top: box.top, right: box.right, bottom: box.bottom, left: box.left,
        width: box.width, height: box.height };
    }
    function intersects(rect) {
      if (!rect) return false;
      const width = Math.max(0, Math.min(rect.right, innerWidth) - Math.max(rect.left, 0));
      const height = Math.max(0, Math.min(rect.bottom, innerHeight) - Math.max(rect.top, 0));
      return width >= Math.min(12, Math.max(1, rect.width)) &&
        height >= Math.min(12, Math.max(1, rect.height));
    }
    function near(a, b) {
      if (a === null || b === null) return a === b;
      return ['top', 'right', 'bottom', 'left', 'width', 'height']
        .every(key => Math.abs(a[key] - b[key]) <= config.tolerance);
    }
    function sample() {
      const target = config.semanticEventId ?
        [...document.querySelectorAll('[data-semantic-event-id]')]
          .find(row => row.dataset.semanticEventId === config.semanticEventId) || null : null;
      const active = document.activeElement;
      const fieldset = active && active.closest ? active.closest('[data-option-group]') : null;
      const targetRect = rectangle(target);
      const activeRect = rectangle(active);
      const focusMatches = !config.focus || Boolean(active && active.type === 'radio' &&
        active.checked && active.value === config.focus.option && fieldset &&
        fieldset.dataset.optionGroup === config.focus.group &&
        fieldset.querySelector('legend')?.textContent.trim() === config.focus.legend);
      return {
        scrollY,
        targetFound: !config.semanticEventId || Boolean(target),
        targetRect,
        targetIntersectsViewport: !config.semanticEventId || intersects(targetRect),
        activeElement: {
          tag: active?.tagName || null,
          type: active?.type || null,
          value: active?.value || null,
          checked: typeof active?.checked === 'boolean' ? active.checked : null,
          optionGroup: fieldset?.dataset.optionGroup || null,
          legend: fieldset?.querySelector('legend')?.textContent.trim() || null
        },
        activeElementRect: activeRect,
        activeElementIntersectsViewport: !config.focus || intersects(activeRect),
        focusMatches,
        pendingNavigation: window.dayReaderDebug?.pendingNavigation ?? null
      };
    }
    while (performance.now() - started <= config.timeoutMs) {
      await new Promise(resolve => requestAnimationFrame(resolve));
      sampledFrames += 1;
      last = sample();
      const stable = previous && Math.abs(last.scrollY - previous.scrollY) <= config.tolerance &&
        near(last.targetRect, previous.targetRect) && near(last.activeElementRect, previous.activeElementRect);
      const valid = last.targetFound && last.focusMatches &&
        (!config.requireTargetInViewport || last.targetIntersectsViewport) &&
        (!config.requireFocusInViewport || last.activeElementIntersectsViewport) &&
        last.pendingNavigation === null;
      stableFrames = stable && valid ? stableFrames + 1 : (valid ? 1 : 0);
      if (stableFrames >= config.requiredStableFrames) {
        return { ...last, settled: true, stableFramesObserved: stableFrames,
          sampledFrames, tolerance: config.tolerance, requiredStableFrames: config.requiredStableFrames,
          elapsedMs: performance.now() - started, expectedSemanticEventId: config.semanticEventId };
      }
      previous = last;
    }
    return { ...last, settled: false, stableFramesObserved: stableFrames,
      sampledFrames, tolerance: config.tolerance, requiredStableFrames: config.requiredStableFrames,
      elapsedMs: performance.now() - started, expectedSemanticEventId: config.semanticEventId };
  })()`);
  if (!result.settled) {
    throw new Error('Visual settlement timed out: ' + JSON.stringify(result));
  }
  return result;
}

async function scheduleTopFrameNavigation(cdp, target, label) {
  let cancelContextListener = () => {};
  const newDocumentContext = new Promise((accept, reject) => {
    const timer = setTimeout(() => {
      cancelContextListener();
      reject(new Error('Timed out waiting for new document context: ' + label));
    }, 10000);
    cancelContextListener = cdp.on('Runtime.executionContextCreated', ({ context }) => {
      if (!context.auxData?.isDefault) return;
      clearTimeout(timer);
      cancelContextListener();
      accept(context.id);
    });
  });
  await evaluate(cdp,
    `setTimeout(() => { location.href = ${JSON.stringify(target)}; }, 0); true`);
  return newDocumentContext;
}

async function navigateFreshDocument(cdp, target, label) {
  const previousToken = currentDocumentToken;
  await scheduleTopFrameNavigation(cdp, target, label);
  await waitFor(cdp,
    `location.href === ${JSON.stringify(target)} && window.dayReaderReady === true && ` +
      `window.dayReaderDebug.documentToken !== ${JSON.stringify(previousToken)} && ` +
      `window.dayReaderDebug.committedRender !== null && ` +
      `window.dayReaderDebug.committedRender.documentToken === window.dayReaderDebug.documentToken && ` +
      `window.dayReaderDebug.committedRender.generation === window.dayReaderDebug.renders && ` +
      `window.dayReaderDebug.committedRender.href === ${JSON.stringify(target)}`,
    label + ' committed document render');
  const settlement = await waitForVisualSettlement(cdp);
  currentDocumentToken = await evaluate(cdp, 'dayReaderDebug.documentToken');
  return {
    path: 'fresh-document', target,
    documentToken: currentDocumentToken,
    generation: await evaluate(cdp, 'dayReaderDebug.committedRender.generation'),
    settlement
  };
}

async function navigateCandidate(cdp, base, state = STATES.roman) {
  freshNavigationSequence += 1;
  const target = candidateUrl(base, state, `source-${freshNavigationSequence}`);
  return navigateFreshDocument(cdp, target, 'Day reader candidate');
}

async function beginGatedCandidate(cdp, base, state, matches, label) {
  const gate = armResponseGate(matches);
  gatedNavigationSequence += 1;
  const target = `${base}${ROUTE}?data=${DATA}&race=${gatedNavigationSequence}${state}`;
  try {
    await scheduleTopFrameNavigation(cdp, target, label);
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

async function transitionHash(cdp, state, settlementOptions = {}) {
  const before = await evaluate(cdp, 'window.dayReaderDebug.renders');
  const documentToken = await evaluate(cdp, 'window.dayReaderDebug.documentToken');
  await evaluate(cdp, `location.hash = ${JSON.stringify(state.replace(/^#/, ''))}`);
  await waitFor(cdp,
    `location.hash === ${JSON.stringify(state)} && window.dayReaderReady === true && ` +
      `window.dayReaderDebug.renders > ${before} && ` +
      `window.dayReaderDebug.committedRender.generation === window.dayReaderDebug.renders && ` +
      `window.dayReaderDebug.committedRender.generation > ${before} && ` +
      `window.dayReaderDebug.committedRender.documentToken === ${JSON.stringify(documentToken)} && ` +
      `window.dayReaderDebug.committedRender.hash === ${JSON.stringify(state)} && ` +
      `window.dayReaderDebug.committedRender.href === location.href`,
    'candidate hash transition');
  const settlement = await waitForVisualSettlement(cdp, settlementOptions);
  return {
    path: 'same-document', target: await evaluate(cdp, 'location.href'),
    documentToken,
    generation: await evaluate(cdp, 'dayReaderDebug.committedRender.generation'),
    settlement
  };
}

async function historyMove(cdp, direction, expected, settlementOptions = {}) {
  const before = await evaluate(cdp, 'window.dayReaderDebug.renders');
  const documentToken = await evaluate(cdp, 'window.dayReaderDebug.documentToken');
  await evaluate(cdp, `history.${direction}()`);
  await waitFor(cdp,
    `location.hash === ${JSON.stringify(expected)} && window.dayReaderReady === true && ` +
      `window.dayReaderDebug.renders > ${before} && ` +
      `window.dayReaderDebug.committedRender.generation === window.dayReaderDebug.renders && ` +
      `window.dayReaderDebug.committedRender.generation > ${before} && ` +
      `window.dayReaderDebug.committedRender.documentToken === ${JSON.stringify(documentToken)} && ` +
      `window.dayReaderDebug.committedRender.hash === ${JSON.stringify(expected)} && ` +
      `window.dayReaderDebug.committedRender.href === location.href`,
    `history ${direction}`);
  return waitForVisualSettlement(cdp, settlementOptions);
}

async function settleResponseGate(cdp, gate) {
  gate.release();
  await gate.served;
  const suffix = '/' + gate.relative;
  await waitFor(cdp,
    `performance.getEntriesByType('resource').some(row => row.name.endsWith(${JSON.stringify(suffix)}))`,
    'released gated response');
  await waitForVisualSettlement(cdp);
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

async function modeOutcomeSnapshot(cdp) {
  return evaluate(cdp, `(() => ({
    href: location.href,
    hash: location.hash,
    context: document.querySelector('.reader-context').textContent,
    modeHeading: document.querySelector('#mode-surface-title').textContent,
    modeMetadata: document.querySelector('[data-reader-action="mode"] .action-state').textContent,
    modes: [...document.querySelectorAll('[data-mode]')].map(row => ({
      mode: row.dataset.mode, checked: row.getAttribute('aria-checked')
    })),
    title: document.querySelector('#celebration-title').textContent,
    date: document.querySelector('#celebration-date').textContent,
    metadata: document.querySelector('#celebration-meta').textContent,
    reading: document.querySelector('#reader-document').innerText,
    events: [...document.querySelectorAll('[data-semantic-event-id]')]
      .map(row => row.dataset.semanticEventId),
    contents: [...document.querySelectorAll('[data-reader-contents] button')]
      .map(row => row.dataset.readerLocation),
    outcome: dayReaderDebug.outcome,
    outcomeClass: dayReaderDebug.outcomeClass,
    mode: dayReaderDebug.mode,
    state: dayReaderDebug.state,
    semantic: dayReaderDebug.semantic,
    pending: dayReaderDebug.pendingNavigation,
    committed: dayReaderDebug.committedRender,
    active: {
      tag: document.activeElement.tagName,
      mode: document.activeElement.dataset.mode || null,
      option: document.activeElement.value || null
    }
  }))()`);
}

function convergentOutcome(snapshot) {
  const copy = structuredClone(snapshot);
  delete copy.href;
  delete copy.hash;
  delete copy.committed;
  return copy;
}

async function navigateCurrent(cdp, base, state = STATES.roman) {
  freshNavigationSequence += 1;
  const target = currentUrl(base, state, `current-${freshNavigationSequence}`);
  const targetUrl = new URL(target);
  await scheduleTopFrameNavigation(cdp, target, 'current Day route');
  try {
    await waitFor(cdp,
      `location.pathname === ${JSON.stringify(targetUrl.pathname)} && ` +
        `location.search === ${JSON.stringify(targetUrl.search)} && ` +
        `document.querySelector('#reading[aria-busy="false"]') && ` +
        `document.querySelector('#celebration-title').textContent !== 'Loading the Mass…'`,
      'current Day route');
  } catch (error) {
    const snapshot = await evaluate(cdp, `({ href: location.href, title: document.title,
      celebration: document.querySelector('#celebration-title')?.textContent || null,
      busy: document.querySelector('#reading')?.getAttribute('aria-busy') || null,
      reading: document.querySelector('#reading')?.innerText || null,
      banner: document.querySelector('#banner')?.innerText || null })`);
    throw new Error(`${error.message}; current-route snapshot: ${JSON.stringify(snapshot)}`);
  }
  const settlement = await waitForVisualSettlement(cdp);
  return { path: 'fresh-document', target, documentToken: null, generation: null, settlement };
}

async function navigateBuiltCandidate(cdp, base, state = STATES.roman) {
  freshNavigationSequence += 1;
  const target = builtCandidateUrl(base, state, `built-${freshNavigationSequence}`);
  return navigateFreshDocument(cdp, target, 'built Day reader candidate');
}

async function navigateBuiltCurrent(cdp, base, state = STATES.roman) {
  freshNavigationSequence += 1;
  const target = builtCurrentUrl(base, state, `built-current-${freshNavigationSequence}`);
  const targetUrl = new URL(target);
  await scheduleTopFrameNavigation(cdp, target, 'built current Day route');
  await waitFor(cdp,
    `location.pathname === ${JSON.stringify(targetUrl.pathname)} && ` +
      `location.search === ${JSON.stringify(targetUrl.search)} && ` +
      `document.querySelector('#reading[aria-busy="false"]') && ` +
      `document.querySelector('#celebration-title').textContent !== 'Loading the Mass…'`,
    'built current Day route');
  const settlement = await waitForVisualSettlement(cdp);
  return { path: 'fresh-document', target, documentToken: null, generation: null, settlement };
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

async function pressSpace(cdp) {
  await cdp.send('Input.dispatchKeyEvent', {
    type: 'keyDown', key: ' ', code: 'Space', windowsVirtualKeyCode: 32
  });
  await cdp.send('Input.dispatchKeyEvent', {
    type: 'keyUp', key: ' ', code: 'Space', windowsVirtualKeyCode: 32
  });
}

async function waitForCommittedRender(cdp, before, expectedHash, label, settlementOptions = {}) {
  const documentToken = await evaluate(cdp, 'window.dayReaderDebug.documentToken');
  await waitFor(cdp,
    `location.hash === ${JSON.stringify(expectedHash)} && window.dayReaderReady === true && ` +
      `window.dayReaderDebug.renders > ${before} && ` +
      `window.dayReaderDebug.committedRender.generation === window.dayReaderDebug.renders && ` +
      `window.dayReaderDebug.committedRender.generation > ${before} && ` +
      `window.dayReaderDebug.committedRender.documentToken === ${JSON.stringify(documentToken)} && ` +
      `window.dayReaderDebug.committedRender.hash === ${JSON.stringify(expectedHash)} && ` +
      `window.dayReaderDebug.committedRender.href === location.href`,
    label);
  return waitForVisualSettlement(cdp, settlementOptions);
}

function updatedHash(state, key, value) {
  const params = new URLSearchParams(state.replace(/^#/, ''));
  params.set(key, value);
  return '#' + params.toString();
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

async function captureEvidence(cdp, file, state, navigationPath, evidenceOptions = {}) {
  const expectedSemanticEventId = evidenceOptions.expectedSemanticEventId || null;
  const page = await evaluate(cdp, `(() => {
    const debug = window.dayReaderDebug || null;
    const active = document.activeElement;
    const activeFieldset = active?.closest?.('[data-option-group]') || null;
    const semanticTarget = ${JSON.stringify(expectedSemanticEventId)} ?
      [...document.querySelectorAll('[data-semantic-event-id]')].find(row =>
        row.dataset.semanticEventId === ${JSON.stringify(expectedSemanticEventId)}) || null : null;
    function rectangle(element) {
      if (!element) return null;
      const box = element.getBoundingClientRect();
      return { top: box.top, right: box.right, bottom: box.bottom, left: box.left,
        width: box.width, height: box.height };
    }
    function intersects(rect) {
      return Boolean(rect && rect.right > 0 && rect.bottom > 0 &&
        rect.left < innerWidth && rect.top < innerHeight);
    }
    const semanticTargetRect = rectangle(semanticTarget);
    const activeElementRect = rectangle(active);
    const pageOverflow = document.documentElement.scrollWidth - document.documentElement.clientWidth;
    return {
      file: ${JSON.stringify(file)},
      state: ${JSON.stringify(state)},
      targetUrl: location.href,
      targetHash: location.hash,
      navigationPath: ${JSON.stringify(navigationPath)},
      documentToken: debug && debug.documentToken || null,
      renderGeneration: debug && debug.committedRender && debug.committedRender.generation || null,
      committedRender: debug && debug.committedRender || null,
      expectedSemanticEventId: ${JSON.stringify(expectedSemanticEventId)},
      semanticTargetRect,
      semanticTargetIntersectsViewport: ${JSON.stringify(expectedSemanticEventId)} ?
        intersects(semanticTargetRect) : null,
      viewport: { width: innerWidth, height: innerHeight },
      outcome: debug && debug.outcome || null,
      outcomeClass: debug && debug.outcomeClass || null,
      mode: debug && debug.mode || null,
      modeChrome: {
        context: document.querySelector('.reader-context')?.textContent || null,
        action: document.querySelector('[data-reader-action="mode"] .action-state')?.textContent || null,
        checked: [...document.querySelectorAll('[data-mode][aria-checked="true"]')]
          .map(row => row.dataset.mode)
      },
      activeElement: {
        tag: active && active.tagName || null,
        type: active && active.type || null,
        value: active && active.value || null,
        checked: active && typeof active.checked === 'boolean' ? active.checked : null,
        optionGroup: activeFieldset?.dataset.optionGroup || null,
        legend: activeFieldset?.querySelector('legend')?.textContent.trim() || null,
        rect: activeElementRect,
        intersectsViewport: intersects(activeElementRect)
      },
      pendingNavigation: debug && debug.pendingNavigation || null,
      pageOverflow,
      surfaceOverflow: [...document.querySelectorAll('dialog[open]')].map(dialog => ({
        id: dialog.id, overflow: dialog.scrollWidth - dialog.clientWidth
      })),
      scrollY
    };
  })()`);
  return {
    ...page,
    visualSettlement: evidenceOptions.settlement || null,
    consoleErrors: structuredClone(consoleProblems),
    failedRequests: structuredClone(failedRequests),
    httpErrors: structuredClone(httpProblems)
  };
}

async function modePerformance(cdp, base) {
  await viewport(cdp, 1024, 768);
  await navigateBuiltCandidate(cdp, base, STATES.postReadLatent);
  const before = await evaluate(cdp, `({
    derivations: dayReaderDebug.derivations,
    detailsBuilds: dayReaderDebug.detailsBuilds,
    resources: performance.getEntriesByType('resource').map(row => row.name)
  })`);
  const missalGeneration = await evaluate(cdp, 'dayReaderDebug.renders');
  await click(cdp, '[data-reader-action="mode"]');
  await click(cdp, '[data-mode="missal"]');
  await waitForCommittedRender(cdp, missalGeneration,
    updatedHash(STATES.postReadLatent, 'ordinary', '1'), 'performance Missal switch');
  const missal = await evaluate(cdp, `({
    derivations: dayReaderDebug.derivations,
    detailsBuilds: dayReaderDebug.detailsBuilds,
    latency: dayReaderDebug.lastModeSwitchMs,
    loads: dayReaderDebug.loads,
    resources: performance.getEntriesByType('resource').map(row => row.name),
    layoutShift: performance.getEntriesByType('layout-shift').reduce((sum, entry) =>
      sum + (entry.hadRecentInput ? 0 : entry.value), 0)
  })`);
  const readGeneration = await evaluate(cdp, 'dayReaderDebug.renders');
  await click(cdp, '[data-reader-action="mode"]');
  await click(cdp, '[data-mode="read"]');
  await waitForCommittedRender(cdp, readGeneration,
    updatedHash(STATES.postReadLatent, 'ordinary', '0'), 'performance Read switch');
  const readLatency = await evaluate(cdp, 'dayReaderDebug.lastModeSwitchMs');
  const added = missal.resources.slice(before.resources.length);
  return {
    readToMissalMs: missal.latency,
    missalToReadMs: readLatency,
    derivationDelta: missal.derivations - before.derivations,
    detailsBuildDelta: missal.detailsBuilds - before.detailsBuilds,
    ordinaryManifestRequests: missal.resources.filter(row => /\/structure\/ordinary\/(index|postconciliar)\.json/.test(row)).length,
    ordinaryBodyRequestsAddedBySwitch: added.filter(row => /\/structure\/ordinary\/postconciliar\.json/.test(row)).length,
    fragmentRequestsAddedBySwitch: added.filter(row => /\/chapters\//.test(row)).length,
    optionDataRequestsAddedBySwitch: added.filter(row => /option|variant/.test(row)).length,
    duplicateResources: missal.resources.filter((url, index, all) => all.indexOf(url) !== index),
    layoutShift: missal.layoutShift,
    loads: missal.loads
  };
}

async function runAssertions(cdp, base) {
  await navigateCandidate(cdp, base);
  await viewport(cdp, 393, 852);
  await waitForVisualSettlement(cdp);

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
      ['Date', 'Contents', 'Mode Read', 'Details']);
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
    assert.match(value.notice, /not held|not yet transcribed/i);
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
    assert.match(value.href, /why=1/);
    assert.equal(value.events, 0);
  });

  await test('fresh and transitioned outcomes commit identical deterministic mode chrome', async () => {
    const cases = [
      ['invalid Eucharistic Prayer', STATES.invalidPrayer, 'missal', 'invalid', 'invalid', /explicit state rejected/i],
      ['missing semantic seat', STATES.missingSeat, 'missal', 'unrenderable', 'unrenderable', /valid selection unrenderable/i],
      ['Why deferred', STATES.deferred, 'missal', 'deferred', 'deferred', /valid state deferred/i],
      ['territorial choice', STATES.territorial, 'read', 'territorial-choice', 'unresolved', /valid state unresolved/i],
      ['invalid Ordinary value', STATES.invalidOrdinary, null, 'invalid', 'invalid', /Mode unavailable.*explicit state rejected/i],
      ['ready Read', STATES.roman, 'read', 'ready', 'ready', /1962/],
      ['ready Missal', STATES.romanMissal, 'missal', 'ready', 'ready', /1962/]
    ];
    for (const [label, targetState, mode, outcome, outcomeClass, metadata] of cases) {
      const noise = [consoleProblems.length, failedRequests.length, httpProblems.length];
      await navigateCandidate(cdp, base, targetState);
      const direct = await modeOutcomeSnapshot(cdp);
      assert.equal(direct.hash, targetState, label + ' direct hash');
      assert.equal(direct.href, direct.committed.href, label + ' committed href');
      assert.equal(direct.mode, mode, label + ' direct mode');
      assert.equal(direct.outcome, outcome, label + ' direct outcome');
      assert.equal(direct.outcomeClass, outcomeClass, label + ' direct class');
      assert.equal(direct.pending, null, label + ' direct pending state');
      assert.equal(direct.modeHeading, 'Mode');
      assert.match(direct.metadata, metadata, label + ' direct metadata');
      assert.deepEqual(direct.modes, [
        { mode: 'read', checked: String(mode === 'read') },
        { mode: 'missal', checked: String(mode === 'missal') }
      ]);
      assert.equal(direct.modeMetadata, mode === 'read' ? 'Read' : mode === 'missal' ? 'Missal' : 'Unavailable');
      assert.equal(direct.context, 'Day · ' + (mode === 'read' ? 'Read' : mode === 'missal' ? 'Missal' : 'Mode unavailable'));

      for (const origin of [STATES.postconciliar, STATES.postMissal]) {
        await navigateCandidate(cdp, base, origin);
        await transitionHash(cdp, targetState);
        const transitioned = await modeOutcomeSnapshot(cdp);
        assert.equal(transitioned.hash, targetState, label + ' transition hash');
        assert.equal(transitioned.href, transitioned.committed.href, label + ' transition committed href');
        assert.equal(transitioned.pending, null, label + ' transition pending state');
        assert.deepEqual(convergentOutcome(transitioned), convergentOutcome(direct),
          label + ' must converge from both modes');
      }
      assert.deepEqual([consoleProblems.length, failedRequests.length, httpProblems.length], noise,
        label + ' console/network state');
    }
  });

  await test('both duplicated Ordinary orderings are neutral and history-independent', async () => {
    const stale = /Tenth Sunday|First Sunday|pentecost-10|advent-1|Missale Romanum|Eucharistic Prayer|But I have cried/i;
    for (const [label, targetState] of Object.entries(DUPLICATE_ORDINARY_STATES)) {
      const noise = [consoleProblems.length, failedRequests.length, httpProblems.length];
      await navigateCandidate(cdp, base, targetState);
      const direct = await modeOutcomeSnapshot(cdp);
      assert.equal(direct.hash, targetState, label + ' direct hash');
      assert.equal(direct.href, direct.committed.href, label + ' committed href');
      assert.equal(direct.mode, null, label + ' neutral mode');
      assert.equal(direct.outcome, 'invalid', label + ' invalid outcome');
      assert.equal(direct.outcomeClass, 'invalid', label + ' invalid class');
      assert.equal(direct.pending, null, label + ' pending navigation');
      assert.equal(direct.context, 'Day · Mode unavailable');
      assert.equal(direct.modeMetadata, 'Unavailable');
      assert.deepEqual(direct.modes, [
        { mode: 'read', checked: 'false' },
        { mode: 'missal', checked: 'false' }
      ]);
      assert.equal(direct.title, 'Selection unavailable');
      assert.equal(direct.date, '');
      assert.match(direct.metadata, /Mode unavailable.*explicit state rejected/i);
      assert.deepEqual(direct.events, []);
      assert.deepEqual(direct.contents, []);
      assert.equal(direct.state, null);
      assert.equal(direct.semantic, null);
      assert.doesNotMatch(direct.reading, stale);

      for (const [originName, origin] of [
        ['Read', STATES.postconciliar], ['Missal', STATES.postMissal]
      ]) {
        await navigateCandidate(cdp, base, origin);
        await transitionHash(cdp, targetState);
        const transitioned = await modeOutcomeSnapshot(cdp);
        assert.equal(transitioned.hash, targetState, `${label} from ${originName} hash`);
        assert.equal(transitioned.pending, null, `${label} from ${originName} pending`);
        assert.equal(transitioned.active.tag, 'BODY', `${label} from ${originName} focus`);
        assert.deepEqual(convergentOutcome(transitioned), convergentOutcome(direct),
          `${label} must converge from ${originName}`);
      }
      assert.deepEqual([consoleProblems.length, failedRequests.length, httpProblems.length], noise,
        label + ' console/network state');
    }
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
      prayer: dayReaderDebug.state.options.legitimate['eucharistic-prayer'] || null,
      hash: location.hash
    })`);
    assert.deepEqual(latent, {
      ordinary: false, ordinaryLanguage: 'en', prayer: null, hash: STATES.ordinaryLatent
    });
  });

  await test('Missal and rubrics are active while Why remains exactly deferred', async () => {
    for (const state of [STATES.romanMissal, STATES.postMissal]) {
      await navigateCandidate(cdp, base, state);
      assert.equal(await evaluate(cdp, 'dayReaderDebug.outcome'), 'ready');
      assert.equal(await evaluate(cdp, 'dayReaderDebug.state.requestedMode'), 'missal');
      assert.ok((await evaluate(cdp, 'dayReaderDebug.semantic.events.length')) > 10);
      assert.deepEqual(await evaluate(cdp, 'dayReaderDebug.deferred'), []);
    }
    await navigateCandidate(cdp, base, STATES.deferred);
    assert.equal(await evaluate(cdp, 'dayReaderDebug.semantic'), null);
    assert.deepEqual(await evaluate(cdp, 'dayReaderDebug.deferred'),
      ['the current Day reasoning apparatus']);
    assert.equal(await evaluate(cdp, 'dayReaderDebug.outcome'), 'deferred');
    const invalid = [
      hash({ date: '2026-08-02', missal: 'roman-1962', bible: 'not-a-bible', orations: 'la' }),
      hash({ date: '2026-08-02', missal: 'roman-1962', bible: 'douay-rheims', orations: 'xx' }),
      hash({ date: '2026-08-02', missal: 'roman-1962', bible: 'douay-rheims', orations: 'la', mass: 'not-a-formulary' }),
      STATES.invalidPrayer, STATES.inapplicablePrayer, STATES.invalidOrdinaryLanguage
    ];
    for (const state of invalid) {
      await navigateCandidate(cdp, base, state);
      assert.equal(await evaluate(cdp, 'dayReaderDebug.semantic'), null);
      assert.ok((await evaluate(cdp, 'dayReaderDebug.error.length')) > 0);
      assert.equal(await evaluate(cdp, 'dayReaderDebug.outcome'), 'invalid');
    }
  });

  await test('both editions preserve production event order and seat every appointed Proper once', async () => {
    const cases = [
      [STATES.romanMissal, 211, 6, 195, 10, 'proper/roman-1962/pentecost-10/010'],
      [STATES.postMissal, 62, 7, 45, 10, 'proper/postconciliar/advent-1/010']
    ];
    for (const [state, total, sections, ordinary, propers, lastProper] of cases) {
      await navigateCandidate(cdp, base, state);
      const value = await evaluate(cdp, `(() => {
        const events = dayReaderDebug.semantic.events;
        const properEvents = events.filter(row => row.kind === 'proper');
        const dom = [...document.querySelectorAll('[data-semantic-event-id]')]
          .map(row => row.dataset.semanticEventId);
        return {
          total: events.length,
          sections: events.filter(row => row.kind === 'ordinary-section').length,
          ordinary: events.filter(row => row.kind === 'ordinary-element').length,
          propers: properEvents.length,
          properIds: properEvents.map(row => row.id),
          seats: properEvents.map(row => row.seat),
          dom,
          option: dayReaderDebug.state.options.legitimate['eucharistic-prayer'] || null,
          checked: document.querySelector('.ordinary-choice input:checked')?.value || null
        };
      })()`);
      assert.equal(value.total, total);
      assert.equal(value.sections, sections);
      assert.equal(value.ordinary, ordinary);
      assert.equal(value.propers, propers);
      assert.equal(new Set(value.properIds).size, propers);
      assert.equal(value.properIds.at(-1), lastProper);
      assert.ok(value.seats.every(row => row && row.id && row.placement === 'seated'));
      assert.deepEqual(value.dom, (await evaluate(cdp, 'dayReaderDebug.semantic.events.map(row => row.id)')));
      if (state === STATES.postMissal) {
        assert.equal(value.option, 'ep-ii');
        assert.equal(value.checked, 'ep-ii');
        assert.equal(value.dom.filter(id => /prex-eucharistica-(i|ii|iii|iv)$/.test(id)).length, 1);
        assert.ok(value.dom.includes('ordinary-element/prex-eucharistica/prex-eucharistica-ii'));
        assert.equal(await evaluate(cdp, 'document.querySelector("#coverage-notice").hidden'), false);
        await click(cdp, '[data-reader-action="contents"]');
        const contents = await evaluate(cdp,
          `[...document.querySelectorAll('[data-reader-contents]')][0].innerText`);
        assert.match(contents, /Rites and divisions/i);
        assert.match(contents, /Appointed propers/i);
        assert.match(contents, /Eucharistic Prayer: II/);
        await escape(cdp);
      } else {
        assert.equal(value.option, null);
        assert.equal(value.checked, null);
        assert.ok(value.dom.includes('ordinary-element/canon/canon-heading'));
        assert.equal(await evaluate(cdp, 'document.querySelector("#coverage-notice").hidden'), true);
      }
    }
  });

  await test('valid unavailable language, partial coverage, and missing seats remain honest', async () => {
    await navigateCandidate(cdp, base, STATES.romanLatinMissal);
    assert.equal(await evaluate(cdp, 'dayReaderDebug.state.languages.ordinary'), 'la');
    assert.match(await evaluate(cdp, 'document.querySelector("#reader-document").innerText'),
      /Withheld under “latin-not-transcribed”/);
    assert.equal(await evaluate(cdp, 'document.querySelector("#coverage-notice").hidden'), false);
    await navigateCandidate(cdp, base, STATES.partial);
    assert.equal(await evaluate(cdp, 'dayReaderDebug.outcome'), 'ready');
    assert.match(await evaluate(cdp, 'document.querySelector("#coverage-notice").textContent'), /not held|not yet transcribed/i);
    await navigateCandidate(cdp, base, STATES.missingSeat);
    assert.equal(await evaluate(cdp, 'dayReaderDebug.outcome'), 'unrenderable');
    assert.equal(await evaluate(cdp, 'dayReaderDebug.semantic'), null);
    assert.match(await evaluate(cdp, 'document.querySelector("#reader-document").innerText'),
      /no usable semantic seat/i);
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
        prayer: dayReaderDebug.state.options.legitimate['eucharistic-prayer']
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
    assert.equal(candidate.date, 'Sunday 29 November 2026');
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
    const active = STATES.postMissal;
    await navigateCandidate(cdp, base, STATES.currentStyleLatent);
    await transitionHash(cdp, active);
    assert.equal(await evaluate(cdp, 'dayReaderDebug.outcome'), 'ready');
    assert.equal(await evaluate(cdp, 'dayReaderDebug.state.requestedMode'), 'missal');
    await historyMove(cdp, 'back', STATES.currentStyleLatent);
    assert.equal(await evaluate(cdp, 'dayReaderDebug.outcome'), 'ready');
    assert.equal(await evaluate(cdp, 'dayReaderDebug.state.apparatus.rubrics'), false);
    assert.equal(await evaluate(cdp,
      `dayReaderDebug.state.options.legitimate['eucharistic-prayer']`), 'ep-ii');
    await historyMove(cdp, 'forward', active);
    assert.equal(await evaluate(cdp, 'dayReaderDebug.outcome'), 'ready');
    assert.equal(await evaluate(cdp, 'dayReaderDebug.state.requestedMode'), 'missal');
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
    assert.equal(await evaluate(cdp, 'dayReaderDebug.outcome'), 'unrenderable');
    assert.equal(await evaluate(cdp, 'dayReaderDebug.state'), null);
    await click(cdp, '[data-reader-action="details"]');
    const failedDetails = await evaluate(cdp, `document.querySelector('[data-reader-details]').innerText`);
    assert.match(failedDetails, /No validated selection.*unrenderable outcome/i);
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
      await transitionHash(cdp, STATES.postMissal);
      const before = await candidateOutcomeSnapshot(cdp);
      assert.equal(before.outcome, 'ready');
      assert.equal(before.title, 'First Sunday of Advent');
      assert.equal(before.state.edition.id, 'postconciliar');
      assert.equal(before.state.requestedMode, 'missal');
      assert.equal(before.semantic.resolved.formulary, 'advent-1');
      assert.equal(before.semantic.events.length, 62);
      await settleResponseGate(cdp, gate);
      const after = await candidateOutcomeSnapshot(cdp);
      assert.deepEqual(after, before);
    } finally {
      gate.release();
    }
  });

  await test('a superseded slow Missal cannot overwrite a newer Read result', async () => {
    const gate = await beginGatedCandidate(
      cdp, base, STATES.romanMissal,
      (relative) => relative.endsWith('/structure/ordinary/roman-1962.json'),
      'slow Roman Ordinary response'
    );
    try {
      await transitionHash(cdp, STATES.roman);
      const before = await candidateOutcomeSnapshot(cdp);
      assert.equal(before.outcome, 'ready');
      assert.equal(before.state.requestedMode, 'read');
      assert.equal(before.semantic.events.length, 10);
      await settleResponseGate(cdp, gate);
      const after = await candidateOutcomeSnapshot(cdp);
      assert.deepEqual(after, before);
      assert.equal(await evaluate(cdp, 'document.querySelectorAll(".ordinary-element").length'), 0);
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
    await waitForVisualSettlement(cdp, {
      semanticEventId: await evaluate(cdp,
        `document.querySelectorAll('[data-semantic-event-id]')[5].dataset.semanticEventId`)
    });
    await click(cdp, '[data-reader-action="contents"]');
    const current = await evaluate(cdp,
      `document.querySelector('[data-reader-contents] [aria-current="location"]').dataset.readerLocation`);
    assert.match(current, /^proper\/roman-1962\/pentecost-10\//);
    await click(cdp, '[data-reader-contents] button:last-child');
    assert.equal(await evaluate(cdp,
      'document.activeElement.dataset.semanticEventId'), 'proper/roman-1962/pentecost-10/010');
  });

  await test('Read and Missal are selectable while Details stays lazy and human-facing', async () => {
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
      { name: 'Missal', disabled: false, checked: 'false' },
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
    await escape(cdp);
    await navigateCandidate(cdp, base, STATES.postMissal);
    await click(cdp, '[data-reader-action="details"]');
    const missalDetails = await evaluate(cdp,
      `document.querySelector('[data-reader-details]').innerText`);
    assert.match(missalDetails, /Mode\s+Missal/i);
    assert.match(missalDetails, /Ordinary language\s+English/i);
    assert.match(missalDetails, /Eucharistic Prayer: II/);
    assert.doesNotMatch(missalDetails, /proper\/|ordinary-element\/|sourceHooks|ordinal|\{.*\}/i);
  });

  await test('mode switching preserves latent state, calendar derivation, semantic location, and history', async () => {
    await navigateCandidate(cdp, base, STATES.postReadLatent);
    const derivationsBefore = await evaluate(cdp, 'dayReaderDebug.derivations');
    const properId = 'proper/postconciliar/advent-1/007';
    await evaluate(cdp, `document.querySelector('[data-semantic-event-id="${properId}"]').scrollIntoView()`);
    await waitForVisualSettlement(cdp, { semanticEventId: properId });
    const missalGeneration = await evaluate(cdp, 'dayReaderDebug.renders');
    await click(cdp, '[data-reader-action="mode"]');
    await click(cdp, '[data-mode="missal"]');
    const missalHash = updatedHash(STATES.postReadLatent, 'ordinary', '1');
    await waitForCommittedRender(cdp, missalGeneration, missalHash, 'Missal switch',
      { semanticEventId: properId });
    const missal = await evaluate(cdp, `({
      hash: location.hash,
      derivations: dayReaderDebug.derivations,
      option: dayReaderDebug.state.options.legitimate['eucharistic-prayer'],
      language: dayReaderDebug.state.languages.ordinary,
      active: document.querySelector('[data-reader-action="mode"] .action-state').textContent,
      focus: document.activeElement.dataset.readerAction || null,
      location: document.querySelector('[data-semantic-event-id="${properId}"]').getBoundingClientRect().top,
      latency: dayReaderDebug.lastModeSwitchMs
    })`);
    assert.match(missal.hash, /ordinary=1/);
    assert.equal(missal.derivations, derivationsBefore);
    assert.equal(missal.option, 'ep-ii');
    assert.equal(missal.language, 'en');
    assert.equal(missal.active, 'Missal');
    assert.equal(missal.focus, 'mode');
    assert.ok(Math.abs(missal.location) < 852);
    assert.ok(missal.latency >= 0);
    const ordinaryLocation = 'ordinary-element/prex-eucharistica/prex-eucharistica-ii';
    await evaluate(cdp, `document.querySelector('[data-semantic-event-id="${ordinaryLocation}"]').scrollIntoView()`);
    await waitForVisualSettlement(cdp, { semanticEventId: ordinaryLocation });
    const readGeneration = await evaluate(cdp, 'dayReaderDebug.renders');
    await click(cdp, '[data-reader-action="mode"]');
    await click(cdp, '[data-mode="read"]');
    const readHash = updatedHash(STATES.postReadLatent, 'ordinary', '0');
    await waitForCommittedRender(cdp, readGeneration, readHash, 'Read switch');
    const read = await evaluate(cdp, `({
      hash: location.hash,
      derivations: dayReaderDebug.derivations,
      ordinaryNodes: document.querySelectorAll('.ordinary-element').length,
      option: dayReaderDebug.state.options.legitimate['eucharistic-prayer'],
      language: dayReaderDebug.state.languages.ordinary,
      visibleProper: [...document.querySelectorAll('[data-semantic-event-id]')]
        .some(row => Math.abs(row.getBoundingClientRect().top) < innerHeight)
    })`);
    assert.match(read.hash, /ordinary=0/);
    assert.equal(read.derivations, derivationsBefore);
    assert.equal(read.ordinaryNodes, 0);
    assert.equal(read.option, 'ep-ii');
    assert.equal(read.language, 'en');
    assert.equal(read.visibleProper, true);
    await historyMove(cdp, 'back', missal.hash);
    assert.equal(await evaluate(cdp, 'dayReaderDebug.state.requestedMode'), 'missal');
    await historyMove(cdp, 'forward', read.hash);
    assert.equal(await evaluate(cdp, 'dayReaderDebug.state.requestedMode'), 'read');
  });

  await test('keyboard Eucharistic Prayer changes restore the selected inline radio and location', async () => {
    await viewport(cdp, 393, 852);
    await navigateCandidate(cdp, base, STATES.postMissal);
    const semanticId = (option) => 'ordinary-element/prex-eucharistica/prex-eucharistica-' +
      option.replace(/^ep-/, '');
    const focusOf = (option) => ({
      group: 'eucharistic-prayer', option, legend: 'Eucharistic Prayer'
    });
    let currentOption = 'ep-ii';
    await evaluate(cdp, `document.querySelector('[data-semantic-event-id="${semanticId(currentOption)}"]').scrollIntoView({block: 'start'})`);
    await waitForVisualSettlement(cdp, { semanticEventId: semanticId(currentOption) });
    await evaluate(cdp, `(() => {
      const radio = document.querySelector('.ordinary-choice input:checked');
      radio.focus({preventScroll: true});
      radio.closest('[data-option-group]').scrollIntoView({block: 'start', behavior: 'auto'});
    })()`);
    let settled = await waitForVisualSettlement(cdp, {
      semanticEventId: semanticId(currentOption), focus: focusOf(currentOption)
    });
    assert.equal(settled.activeElement.value, 'ep-ii');
    assert.equal(settled.targetIntersectsViewport, true);
    assert.equal(settled.activeElementIntersectsViewport, true);
    let currentHash = STATES.postMissal;
    for (const option of ['ep-i', 'ep-iii', 'ep-iv', 'ep-ii']) {
      const before = await evaluate(cdp, 'dayReaderDebug.renders');
      const presentationsBefore = await evaluate(cdp, 'dayReaderDebug.ordinaryPresentations');
      const beforeTop = settled.targetRect.top;
      await evaluate(cdp,
        `document.querySelector('.ordinary-choice input[value="${option}"]').focus({preventScroll: true})`);
      await pressSpace(cdp);
      currentHash = updatedHash(currentHash, 'eucharistic-prayer', option);
      settled = await waitForCommittedRender(cdp, before, currentHash, 'keyboard EP ' + option, {
        semanticEventId: semanticId(option), focus: focusOf(option)
      });
      const restored = await evaluate(cdp, `(() => {
        const active = document.activeElement;
        const fieldset = active.closest('fieldset');
        const ids = [...document.querySelectorAll('[data-semantic-event-id]')]
          .map(row => row.dataset.semanticEventId);
        return {
          activeType: active.type,
          activeValue: active.value,
          checked: active.checked,
          legend: fieldset && fieldset.querySelector('legend').textContent,
          group: fieldset && fieldset.dataset.optionGroup,
          hash: location.hash,
          semanticTop: document.querySelector('[data-semantic-event-id="${semanticId(option)}"]').getBoundingClientRect().top,
          pending: dayReaderDebug.pendingNavigation,
          presentations: dayReaderDebug.ordinaryPresentations,
          uniqueEvents: new Set(ids).size === ids.length,
          epEvents: ids.filter(id => /prex-eucharistica-(i|ii|iii|iv)$/.test(id))
        };
      })()`);
      assert.equal(restored.activeType, 'radio');
      assert.equal(restored.activeValue, option);
      assert.equal(restored.checked, true);
      assert.equal(restored.legend, 'Eucharistic Prayer');
      assert.equal(restored.group, 'eucharistic-prayer');
      assert.equal(restored.hash, currentHash);
      assert.equal(settled.targetIntersectsViewport, true);
      assert.equal(settled.activeElementIntersectsViewport, true);
      assert.ok(settled.stableFramesObserved >= 5);
      assert.ok(Math.abs(restored.semanticTop - beforeTop) <= 4,
        `${option} semantic delta: ${restored.semanticTop - beforeTop}`);
      assert.equal(restored.pending, null);
      assert.equal(restored.presentations, presentationsBefore + 1);
      assert.equal(restored.uniqueEvents, true);
      assert.equal(restored.epEvents.length, 1);
      currentOption = option;
    }

    await cdp.send('Emulation.setEmulatedMedia', {
      media: 'screen', features: [{ name: 'prefers-reduced-motion', value: 'reduce' }]
    });
    const reducedBeforeTop = settled.targetRect.top;
    const reducedGeneration = await evaluate(cdp, 'dayReaderDebug.renders');
    await evaluate(cdp,
      `document.querySelector('.ordinary-choice input[value="ep-iii"]').focus({preventScroll: true})`);
    await pressSpace(cdp);
    const reducedHash = updatedHash(currentHash, 'eucharistic-prayer', 'ep-iii');
    const reduced = await waitForCommittedRender(cdp, reducedGeneration, reducedHash,
      'reduced-motion keyboard EP ep-iii', {
        semanticEventId: semanticId('ep-iii'), focus: focusOf('ep-iii')
      });
    assert.notEqual(await evaluate(cdp, 'getComputedStyle(document.documentElement).scrollBehavior'), 'smooth');
    assert.ok(Math.abs(reduced.targetRect.top - reducedBeforeTop) <= 4,
      `reduced-motion semantic delta: ${reduced.targetRect.top - reducedBeforeTop}`);
    assert.equal(reduced.activeElement.value, 'ep-iii');
    assert.equal(reduced.activeElement.checked, true);
    await cdp.send('Emulation.setEmulatedMedia', { media: 'screen' });

    await transitionHash(cdp, STATES.invalidPrayer);
    const invalid = await evaluate(cdp, `({
      outcome: dayReaderDebug.outcome,
      pending: dayReaderDebug.pendingNavigation,
      activeTag: document.activeElement.tagName,
      activeType: document.activeElement.type || null,
      checkedOptions: document.querySelectorAll('.ordinary-choice input:checked').length
    })`);
    assert.deepEqual(invalid, {
      outcome: 'invalid', pending: null, activeTag: 'BODY', activeType: null, checkedOptions: 0
    });
  });

  await test('top, reading, offertory, Canon, Communion, and end use semantic correspondence', async () => {
    async function choose(mode, semanticEventId = null) {
      const before = await evaluate(cdp, 'dayReaderDebug.renders');
      await click(cdp, '[data-reader-action="mode"]');
      await click(cdp, `[data-mode="${mode}"]`);
      const target = await evaluate(cdp, 'location.hash');
      await waitForCommittedRender(cdp, before, target, `${mode} correspondence`,
        semanticEventId ? { semanticEventId } : {});
    }
    await navigateCandidate(cdp, base, STATES.roman);
    await evaluate(cdp, 'window.scrollTo(0, 0)');
    await choose('missal');
    assert.ok(await evaluate(cdp, 'scrollY <= 8'));

    for (const id of [
      'proper/roman-1962/pentecost-10/006',
      'proper/roman-1962/pentecost-10/007'
    ]) {
      await transitionHash(cdp, STATES.roman);
      await evaluate(cdp, `document.querySelector('[data-semantic-event-id="${id}"]').scrollIntoView()`);
      await waitForVisualSettlement(cdp, { semanticEventId: id });
      await choose('missal', id);
      assert.ok(await evaluate(cdp,
        `Math.abs(document.querySelector('[data-semantic-event-id="${id}"]').getBoundingClientRect().top) < innerHeight`));
    }

    for (const id of [
      'ordinary-element/canon/canon-heading',
      'ordinary-element/communio/domine-non-sum-dignus'
    ]) {
      await transitionHash(cdp, STATES.romanMissal);
      await evaluate(cdp, `document.querySelector('[data-semantic-event-id="${id}"]').scrollIntoView()`);
      await waitForVisualSettlement(cdp, { semanticEventId: id });
      await choose('read');
      const visible = await evaluate(cdp, `[...document.querySelectorAll('[data-semantic-event-id^="proper/"]')]
        .filter(row => Math.abs(row.getBoundingClientRect().top) < innerHeight)
        .map(row => row.dataset.semanticEventId)`);
      assert.ok(visible.length > 0, `${id}: no corresponding Proper boundary`);
    }

    await transitionHash(cdp, STATES.roman);
    await evaluate(cdp, 'window.scrollTo(0, document.documentElement.scrollHeight)');
    await choose('missal');
    assert.ok(await evaluate(cdp,
      'scrollY + innerHeight >= document.documentElement.scrollHeight - 8'));
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
    const nextGeneration = await evaluate(cdp, 'dayReaderDebug.renders');
    await click(cdp, '#next-date');
    const nextHash = await evaluate(cdp, 'location.hash');
    await waitForCommittedRender(cdp, nextGeneration, nextHash, 'next date');
    assert.equal(await evaluate(cdp, 'dayReaderDebug.state.civilDate'), '2026-08-03');
    const backGeneration = await evaluate(cdp, 'dayReaderDebug.renders');
    await evaluate(cdp, 'history.back()');
    await waitForCommittedRender(cdp, backGeneration, STATES.roman, 'Back date');
    assert.equal(await evaluate(cdp, 'dayReaderDebug.state.civilDate'), '2026-08-02');
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

  await test('candidate Missal and current Day share Ordinary and Proper text for both editions', async () => {
    await viewport(cdp, 1024, 768);
    for (const state of [STATES.romanMissal, STATES.postMissal]) {
      await navigateCandidate(cdp, base, state);
      const candidate = await evaluate(cdp, `({
        title: document.querySelector('#celebration-title').textContent,
        ordinary: [...document.querySelectorAll('#reader-document .ordinary-element')]
          .map(row => row.textContent.replace(/\s+/g, ' ').trim()),
        propers: [...document.querySelectorAll('#reader-document .proper:not(.ordinary-element)')]
          .map(row => ({
            name: row.querySelector('.proper-name')?.childNodes[0]?.textContent.trim() || '',
            text: [...row.querySelectorAll('.passage, .composed')]
              .map(part => part.textContent.replace(/\s+/g, ' ').trim())
          }))
      })`);
      await navigateCurrent(cdp, base, state);
      const current = await evaluate(cdp, `({
        title: document.querySelector('#celebration-title').textContent,
        ordinary: [...document.querySelectorAll('#reading .ordinary-element')]
          .map(row => row.textContent.replace(/\s+/g, ' ').trim()),
        propers: [...document.querySelectorAll('#reading .proper:not(.ordinary-element)')]
          .map(row => ({
            name: row.querySelector('.proper-name')?.childNodes[0]?.textContent.trim() || '',
            text: [...row.querySelectorAll('.passage, .composed')]
              .map(part => part.textContent.replace(/\s+/g, ' ').trim())
          }))
      })`);
      assert.equal(candidate.title, current.title);
      assert.deepEqual(candidate.ordinary, current.ordinary);
      assert.deepEqual(candidate.propers, current.propers);
    }
  });

  await test('normal preview build contains a noindex candidate but no candidate navigation link', async () => {
    await navigateBuiltCandidate(cdp, base, STATES.roman);
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
    await navigateCandidate(cdp, base, STATES.postMissal);
    const missal = await evaluate(cdp, `({
      option: document.querySelector('#celebration-meta').textContent,
      ordinary: document.querySelectorAll('.ordinary-element').length,
      propers: document.querySelectorAll('#reader-document .proper[data-semantic-event-id^="proper/"]').length,
      choice: getComputedStyle(document.querySelector('.ordinary-choice')).display,
      actions: getComputedStyle(document.querySelector('.reader-actions')).display
    })`);
    assert.match(missal.option, /Eucharistic Prayer: II/);
    assert.equal(missal.ordinary, 45);
    assert.equal(missal.propers, 10);
    assert.equal(missal.choice, 'none');
    assert.equal(missal.actions, 'none');
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
  const navigation = await navigateBuiltCandidate(cdp, base, state);
  await evaluate(cdp, 'window.scrollTo(0, 0)');
  if (kind === 'deep') {
    await evaluate(cdp, 'window.scrollTo(0, document.documentElement.scrollHeight - innerHeight - 8)');
  } else if (['date', 'contents', 'mode', 'details'].includes(kind)) {
    await click(cdp, `[data-reader-action="${kind}"]`);
  }
  const settlement = await waitForVisualSettlement(cdp);
  return { ...navigation, settlement };
}

async function captureMatrix(cdp, base, directory) {
  await mkdir(directory, { recursive: true });
  const sizes = [[1440, 900], [1024, 768], [768, 1024], [393, 852], [320, 852]];
  const cases = [
    ['roman-read', STATES.roman, 'top'], ['roman-missal', STATES.romanMissal, 'top'],
    ['roman-missal-deep', STATES.romanMissal, 'deep'],
    ['roman-missal-contents', STATES.romanMissal, 'contents'],
    ['roman-missal-mode', STATES.romanMissal, 'mode'],
    ['roman-missal-details', STATES.romanMissal, 'details'],
    ['postconciliar-read', STATES.postconciliar, 'top'],
    ['postconciliar-missal-ep-ii', STATES.postMissal, 'top'],
    ['invalid-eucharistic-prayer', STATES.invalidPrayer, 'top'],
    ['partial-coverage', STATES.partial, 'top'], ['missing-seat', STATES.missingSeat, 'top'],
    ['why-deferred', STATES.deferred, 'top'],
    ['territorial-unresolved', STATES.territorial, 'top'],
    ['invalid-ordinary', STATES.invalidOrdinary, 'top']
  ];
  const measures = [];
  const evidence = [];
  for (const [width, height] of sizes) {
    await viewport(cdp, width, height);
    for (const [name, state, kind] of cases) {
      const navigation = await captureCandidate(cdp, base, state, kind);
      const file = `day-reader-missal-${name}-${width}x${height}.png`;
      await shot(cdp, join(directory, file));
      measures.push({ file, viewport: `${width}x${height}`, state: name, metrics: await metrics(cdp) });
      evidence.push(await captureEvidence(cdp, file, name, navigation.path,
        { settlement: navigation.settlement }));
      if (await evaluate(cdp, 'Boolean(document.querySelector("dialog[open]"))')) await escape(cdp);
    }
    for (const [name, state] of [['roman-missal', STATES.romanMissal], ['postconciliar-missal-ep-ii', STATES.postMissal]]) {
      const navigation = await navigateBuiltCurrent(cdp, base, state);
      const file = `day-current-${name}-${width}x${height}.png`;
      await shot(cdp, join(directory, file));
      evidence.push(await captureEvidence(cdp, file, 'current-' + name, navigation.path,
        { settlement: navigation.settlement }));
    }
  }

  await viewport(cdp, 393, 852);
  let navigation = await navigateBuiltCandidate(cdp, base, STATES.postMissal);
  await evaluate(cdp, 'window.scrollTo(0, 0)');
  await evaluate(cdp, `document.documentElement.style.fontSize = '200%'`);
  const enlargedFile = 'day-reader-missal-postconciliar-200-percent-393x852.png';
  await shot(cdp, join(directory, enlargedFile));
  measures.push({ file: enlargedFile, viewport: '393x852',
    state: 'postconciliar-missal-200-percent', metrics: await metrics(cdp) });
  const enlargedSettlement = await waitForVisualSettlement(cdp);
  evidence.push(await captureEvidence(cdp, enlargedFile, 'postconciliar-missal-200-percent', navigation.path,
    { settlement: enlargedSettlement }));
  await evaluate(cdp, `document.documentElement.style.fontSize = ''`);

  await viewport(cdp, 393, 852);
  navigation = await navigateBuiltCandidate(cdp, base, STATES.currentStyleLatent);
  const latentFile = 'day-reader-missal-latent-read-393x852.png';
  await shot(cdp, join(directory, latentFile));
  evidence.push(await captureEvidence(cdp, latentFile, 'latent-read', navigation.path,
    { settlement: navigation.settlement }));
  await navigateBuiltCandidate(cdp, base, STATES.roman);
  navigation = await transitionHash(cdp, STATES.invalid);
  await click(cdp, '[data-reader-action="date"]');
  const invalidDateFile = 'day-reader-missal-transition-invalid-date-393x852.png';
  await shot(cdp, join(directory, invalidDateFile));
  evidence.push(await captureEvidence(cdp, invalidDateFile, 'transition-invalid-date', navigation.path,
    { settlement: navigation.settlement }));
  await escape(cdp);
  await click(cdp, '[data-reader-action="details"]');
  const invalidDetailsFile = 'day-reader-missal-transition-invalid-details-393x852.png';
  await shot(cdp, join(directory, invalidDetailsFile));
  evidence.push(await captureEvidence(cdp, invalidDetailsFile, 'transition-invalid-details', navigation.path,
    { settlement: navigation.settlement }));
  await escape(cdp);

  navigation = await navigateBuiltCandidate(cdp, base, STATES.postReadLatent);
  const switchSemanticId = 'proper/postconciliar/advent-1/007';
  await evaluate(cdp, `document.querySelector('[data-semantic-event-id="${switchSemanticId}"]').scrollIntoView()`);
  let switchSettlement = await waitForVisualSettlement(cdp, { semanticEventId: switchSemanticId });
  const switchBeforeFile = 'day-reader-missal-mode-switch-before-393x852.png';
  await shot(cdp, join(directory, switchBeforeFile));
  evidence.push(await captureEvidence(cdp, switchBeforeFile, 'mode-switch-read-before', navigation.path,
    { expectedSemanticEventId: switchSemanticId, settlement: switchSettlement }));
  const captureGeneration = await evaluate(cdp, 'dayReaderDebug.renders');
  await click(cdp, '[data-reader-action="mode"]');
  await click(cdp, '[data-mode="missal"]');
  switchSettlement = await waitForCommittedRender(cdp, captureGeneration,
    updatedHash(STATES.postReadLatent, 'ordinary', '1'), 'captured Missal switch',
    { semanticEventId: switchSemanticId });
  const switchAfterFile = 'day-reader-missal-mode-switch-missal-after-393x852.png';
  await shot(cdp, join(directory, switchAfterFile));
  evidence.push(await captureEvidence(cdp, switchAfterFile, 'mode-switch-missal-after', 'same-document',
    { expectedSemanticEventId: switchSemanticId, settlement: switchSettlement }));
  const readGeneration = await evaluate(cdp, 'dayReaderDebug.renders');
  await click(cdp, '[data-reader-action="mode"]');
  await click(cdp, '[data-mode="read"]');
  const capturedReadHash = updatedHash(STATES.postReadLatent, 'ordinary', '0');
  switchSettlement = await waitForCommittedRender(cdp, readGeneration, capturedReadHash,
    'captured Read return', { semanticEventId: switchSemanticId });
  const switchReturnFile = 'day-reader-missal-mode-switch-read-return-393x852.png';
  await shot(cdp, join(directory, switchReturnFile));
  evidence.push(await captureEvidence(cdp, switchReturnFile, 'mode-switch-read-return', 'same-document',
    { expectedSemanticEventId: switchSemanticId, settlement: switchSettlement }));

  const correctionStates = [
    ['invalid-ep', STATES.invalidPrayer], ['missing-seat', STATES.missingSeat],
    ['why-deferred', STATES.deferred], ['territorial', STATES.territorial],
    ['invalid-ordinary', STATES.invalidOrdinary]
  ];
  for (const [name, target] of correctionStates) {
    for (const [originName, origin] of [['read', STATES.roman], ['missal', STATES.romanMissal]]) {
      await navigateBuiltCandidate(cdp, base, origin);
      navigation = await transitionHash(cdp, target);
      const file = `day-reader-missal-transition-${originName}-to-${name}-393x852.png`;
      await shot(cdp, join(directory, file));
      evidence.push(await captureEvidence(cdp, file, `${originName}-to-${name}`, navigation.path,
        { settlement: navigation.settlement }));
    }
  }

  for (const [width, height] of [[393, 852], [1440, 900]]) {
    await viewport(cdp, width, height);
    for (const [name, target] of Object.entries(DUPLICATE_ORDINARY_STATES)) {
      navigation = await navigateBuiltCandidate(cdp, base, target);
      const file = `day-reader-missal-duplicate-ordinary-${name}-${width}x${height}.png`;
      await shot(cdp, join(directory, file));
      evidence.push(await captureEvidence(cdp, file, `duplicate-ordinary-${name}`,
        navigation.path, { settlement: navigation.settlement }));
    }
  }
  await viewport(cdp, 393, 852);
  for (const [name, target] of Object.entries(DUPLICATE_ORDINARY_STATES)) {
    for (const [originName, origin] of [['read', STATES.roman], ['missal', STATES.romanMissal]]) {
      await navigateBuiltCandidate(cdp, base, origin);
      navigation = await transitionHash(cdp, target);
      const file = `day-reader-missal-transition-${originName}-to-duplicate-ordinary-${name}-393x852.png`;
      await shot(cdp, join(directory, file));
      evidence.push(await captureEvidence(cdp, file,
        `${originName}-to-duplicate-ordinary-${name}`, navigation.path,
        { settlement: navigation.settlement }));
    }
  }

  navigation = await navigateBuiltCandidate(cdp, base, STATES.postMissal);
  const initialEpId = 'ordinary-element/prex-eucharistica/prex-eucharistica-ii';
  await evaluate(cdp, `document.querySelector('[data-semantic-event-id="${initialEpId}"]').scrollIntoView({block: 'start'})`);
  await waitForVisualSettlement(cdp, { semanticEventId: initialEpId });
  await evaluate(cdp, `(() => {
    const radio = document.querySelector('.ordinary-choice input:checked');
    radio.focus({preventScroll: true});
    radio.closest('[data-option-group]').scrollIntoView({block: 'start', behavior: 'auto'});
  })()`);
  let epSettlement = await waitForVisualSettlement(cdp, {
    semanticEventId: initialEpId,
    focus: { group: 'eucharistic-prayer', option: 'ep-ii', legend: 'Eucharistic Prayer' }
  });
  const epBeforeFile = 'day-reader-missal-ep-focus-before-393x852.png';
  await shot(cdp, join(directory, epBeforeFile));
  evidence.push(await captureEvidence(cdp, epBeforeFile, 'ep-focus-before', navigation.path, {
    expectedSemanticEventId: initialEpId, settlement: epSettlement
  }));
  const epGeneration = await evaluate(cdp, 'dayReaderDebug.renders');
  await evaluate(cdp, `document.querySelector('.ordinary-choice input[value="ep-iii"]').focus({preventScroll: true})`);
  await pressSpace(cdp);
  const epHash = updatedHash(STATES.postMissal, 'eucharistic-prayer', 'ep-iii');
  const epAfterId = 'ordinary-element/prex-eucharistica/prex-eucharistica-iii';
  epSettlement = await waitForCommittedRender(cdp, epGeneration, epHash,
    'captured EP III focus restoration', {
      semanticEventId: epAfterId,
      focus: { group: 'eucharistic-prayer', option: 'ep-iii', legend: 'Eucharistic Prayer' }
    });
  const epAfterFile = 'day-reader-missal-ep-iii-focus-restored-393x852.png';
  await shot(cdp, join(directory, epAfterFile));
  evidence.push(await captureEvidence(cdp, epAfterFile, 'ep-iii-focus-restored', 'same-document', {
    expectedSemanticEventId: epAfterId, settlement: epSettlement
  }));

  await viewport(cdp, 1024, 768);
  navigation = await navigateBuiltCandidate(cdp, base, STATES.postMissal);
  await evaluate(cdp, 'window.scrollTo(0, 0)');
  await cdp.send('Emulation.setEmulatedMedia', { media: 'print' });
  const pdf = await cdp.send('Page.printToPDF', {
    printBackground: true, preferCSSPageSize: true, paperWidth: 8.5, paperHeight: 11,
    marginTop: 0.4, marginBottom: 0.4, marginLeft: 0.45, marginRight: 0.45
  });
  await writeFile(join(directory, 'day-reader-missal-postconciliar-print.pdf'), Buffer.from(pdf.data, 'base64'));
  const printMetadata = await captureEvidence(cdp,
    'day-reader-missal-postconciliar-print.pdf', 'postconciliar-missal-print', navigation.path,
    { settlement: navigation.settlement });
  await cdp.send('Emulation.setEmulatedMedia', { media: 'screen' });
  await writeFile(join(directory, 'measurements.json'), JSON.stringify(measures, null, 2) + '\n');
  await writeFile(join(directory, 'capture-metadata.json'), JSON.stringify(evidence, null, 2) + '\n');
  await writeFile(join(directory, 'print-metadata.json'), JSON.stringify(printMetadata, null, 2) + '\n');
  return measures;
}

async function main() {
  const server = staticServer();
  const serverPort = await listen(server);
  const base = `http://127.0.0.1:${serverPort}`;
  const debugPort = await freePort();
  freshNavigationSequence += 1;
  const bootstrapTarget = candidateUrl(base, STATES.roman,
    `bootstrap-${freshNavigationSequence}`);
  const profileRoot = join(ROOT, 'build');
  await mkdir(profileRoot, { recursive: true });
  const profile = await mkdtemp(join(profileRoot, 'triptych-day-reader-chrome-'));
  const chrome = spawn(chromeBinary, [
    '--headless=new', '--no-sandbox', '--disable-dev-shm-usage', '--disable-gpu',
    '--disable-extensions', '--disable-component-extensions-with-background-pages',
    '--disable-background-networking', '--disable-sync',
    `--remote-debugging-port=${debugPort}`, `--user-data-dir=${profile}`,
    '--no-first-run', '--no-default-browser-check', 'about:blank'
  ], { stdio: ['ignore', 'ignore', 'pipe'] });
  let chromeStderr = '';
  chrome.stderr.on('data', (chunk) => { chromeStderr += chunk.toString(); });
  let cdp;
  try {
    const browserVersion = await waitForJson(`http://127.0.0.1:${debugPort}/json/version`);
    const response = await fetch(
      `http://127.0.0.1:${debugPort}/json/new?${encodeURIComponent(bootstrapTarget)}`,
      { method: 'PUT' }
    );
    const createdPage = await response.json();
    let page = null;
    for (let attempt = 0; attempt < 180; attempt += 1) {
      const targets = await waitForJson(`http://127.0.0.1:${debugPort}/json/list`);
      page = targets.find((target) => target.id === createdPage.id &&
        target.type === 'page' && target.url === bootstrapTarget &&
        target.title === 'Day reader — internal candidate') || null;
      if (page && page.webSocketDebuggerUrl) break;
      if (attempt === 179) throw new Error('Chromium bootstrap page did not load');
      await new Promise((accept) => setTimeout(accept, 50));
    }
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

    await waitFor(cdp,
      `location.href === ${JSON.stringify(bootstrapTarget)} && window.dayReaderReady === true && ` +
        `window.dayReaderDebug.committedRender !== null && ` +
        `window.dayReaderDebug.committedRender.href === ${JSON.stringify(bootstrapTarget)}`,
      'bootstrap document render');
    await waitForVisualSettlement(cdp);
    currentDocumentToken = await evaluate(cdp, 'dayReaderDebug.documentToken');

    await runAssertions(cdp, base);
    const captures = captureDir ? await captureMatrix(cdp, base, captureDir) : [];
    await viewport(cdp, 393, 852);
    await navigateBuiltCandidate(cdp, base);
    await evaluate(cdp, 'window.scrollTo(0, 0)');
    const measured = await metrics(cdp);
    const modeMeasured = await modePerformance(cdp, base);
    const ax = await cdp.send('Accessibility.getFullAXTree');
    const measuredFiles = {};
    for (const [name, relative] of Object.entries({
      shellJavaScript: 'src/web/browser/liturgy/reader-shell.js',
      candidateJavaScript: 'src/web/browser/liturgy/day-reader.js',
      productionOrdinaryJavaScript: 'src/web/browser/liturgy/day.js',
      shellCss: 'src/web/browser/liturgy/reader-shell.css',
      candidateCss: 'src/web/browser/liturgy/day-reader.css',
      productionOrdinaryCss: 'src/web/browser/liturgy/day.css',
      productionMissalCss: 'src/web/browser/liturgy/day-missal.css'
    })) {
      const bytes = await readFile(join(ROOT, relative));
      measuredFiles[name] = { raw: bytes.length, gzip: gzipSync(bytes).length };
    }
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
        modeSwitch: modeMeasured,
        resourceCount: measured.resources.length,
        duplicateResources: measured.resources.filter((url, index, all) => all.indexOf(url) !== index)
      },
      captures: captures.length,
      files: measuredFiles
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
    if (chrome.exitCode === null && chrome.signalCode === null) {
      const exited = new Promise((accept) => chrome.once('exit', accept));
      chrome.kill('SIGTERM');
      await exited;
    }
    server.closeAllConnections();
    await new Promise((accept) => server.close(accept));
    await rm(profile, { recursive: true, force: true });
  }
}

await main();
