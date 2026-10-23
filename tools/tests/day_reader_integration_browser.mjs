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
const SOURCE_ONLY = process.env.TRIPTYCH_SOURCE_ONLY === '1';
const DATA = SOURCE_ONLY ? '/src/web/data' : '/build/public-alpha/preview/browse';
const SOURCE_PROPERS = (process.env.TRIPTYCH_SOURCE_PROPERS ||
  '.scratch/day-source-structure/structure/propers').replace(/^\/+|\/+$/g, '');
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
      let relative = decodeURIComponent(url.pathname).replace(/^\/+/, '');
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
      if (/^src\/web\/data\/[^/]+\/chapters\//.test(relative)) {
        relative = relative.replace(/^src\/web\/data\//, 'src/sources/bibles/');
      }
      if (SOURCE_ONLY && /^src\/web\/data\/structure\/propers\/[^/]+\.json$/.test(relative)) {
        relative = relative.replace('src/web/data/structure/propers', SOURCE_PROPERS);
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

const DAY_STATE_KEYS = new Set([
  'date', 'missal', 'bible', 'orations', 'why', 'ordinary', 'ordinary-lang',
  'rubrics', 'mass', 'form', 'mode', 'location', 'eucharistic-prayer'
]);

// The candidate route accepts the retained `ordinary` input but immediately
// publishes the v1 canonical state.  Browser waits must follow that committed
// state instead of waiting forever for the pre-canonical URL to reappear.
function canonicalDayHash(state) {
  const parsed = new URLSearchParams(state.replace(/^#/, ''));
  const pairs = [];
  const add = (key, value) => {
    if (value !== null && value !== undefined) pairs.push([key, value]);
  };
  add('date', parsed.get('date'));
  add('missal', parsed.get('missal'));
  add('bible', parsed.get('bible'));
  add('orations', parsed.get('orations'));
  add('mode', parsed.get('mode') || (parsed.get('ordinary') === '1' ? 'missal' : 'read'));
  add('location', parsed.get('location'));
  add('why', parsed.get('why') === '1' ? '1' : '0');
  add('ordinary-lang', parsed.get('ordinary-lang'));
  add('rubrics', parsed.get('rubrics') === '0' ? '0' : '1');
  add('mass', parsed.get('mass'));
  add('form', parsed.get('form'));
  add('eucharistic-prayer', parsed.get('eucharistic-prayer'));
  for (const [key, value] of parsed.entries()) {
    if (!DAY_STATE_KEYS.has(key)) add(key, value);
  }
  return '#' + new URLSearchParams(pairs).toString();
}

const STATES = Object.freeze({
  roman: hash({ date: '2026-08-02', missal: 'roman-1962', bible: 'douay-rheims', orations: 'la', mass: 'pentecost-10' }),
  augustineRomanLatin: hash({ date: '2026-08-28', missal: 'roman-1962', bible: 'douay-rheims', orations: 'la' }),
  augustineRomanEnglish: hash({ date: '2026-08-28', missal: 'roman-1962', bible: 'douay-rheims', orations: 'en' }),
  augustinePostconciliarLatin: hash({ date: '2026-08-28', missal: 'postconciliar', bible: 'douay-rheims', orations: 'la' }),
  romanMissal: hash({ date: '2026-08-02', missal: 'roman-1962', bible: 'douay-rheims', orations: 'la', mass: 'pentecost-10', ordinary: '1', 'ordinary-lang': 'en', rubrics: '1', why: '0' }),
  romanLatinMissal: hash({ date: '2026-08-02', missal: 'roman-1962', bible: 'douay-rheims', orations: 'la', mass: 'pentecost-10', ordinary: '1', 'ordinary-lang': 'la', rubrics: '1', why: '0' }),
  postconciliar: hash({ date: '2026-11-29', missal: 'postconciliar', bible: 'douay-rheims', orations: 'la', mass: 'advent-1' }),
  postReadLatent: hash({ date: '2026-11-29', missal: 'postconciliar', bible: 'douay-rheims', orations: 'la', mass: 'advent-1', ordinary: '0', 'ordinary-lang': 'en', rubrics: '0', why: '0', 'eucharistic-prayer': 'ep-ii' }),
  postMissal: hash({ date: '2026-11-29', missal: 'postconciliar', bible: 'douay-rheims', orations: 'la', mass: 'advent-1', ordinary: '1', 'ordinary-lang': 'en', rubrics: '1', why: '0', 'eucharistic-prayer': 'ep-ii' }),
  postLatinMissal: hash({ date: '2026-11-29', missal: 'postconciliar', bible: 'douay-rheims', orations: 'la', mass: 'advent-1', ordinary: '1', 'ordinary-lang': 'la', rubrics: '1', why: '0', 'eucharistic-prayer': 'ep-ii' }),
  postPentecostDayMissal: hash({ date: '2026-05-24', missal: 'postconciliar', bible: 'douay-rheims', orations: 'la', mass: 'pentecost', form: 'day', ordinary: '1', 'ordinary-lang': 'en', rubrics: '1', why: '0' }),
  romanEmberLongerMissal: hash({ date: '2026-12-19', missal: 'roman-1962', bible: 'douay-rheims', orations: 'la', mass: 'advent-ember-saturday', form: 'longer', ordinary: '1', 'ordinary-lang': 'en', rubrics: '1', why: '0' }),
  multiple: hash({ date: '2026-01-11', missal: 'roman-1962', bible: 'douay-rheims', orations: 'la', mass: 'comm-s-hygini-papae-martyris' }),
  // Claret's own Collect remains rights-withheld; the Common supplies the
  // Secret and Postcommunion. Vianney's former gap was restored in Phase 5.
  partial: hash({ date: '2026-10-23', missal: 'roman-1962', bible: 'douay-rheims', orations: 'la', mass: 's-antonii-mariae-claret-episcopi-confessoris', ordinary: '1', 'ordinary-lang': 'en', rubrics: '1' }),
  ashBeforeFrame: hash({ date: '2026-02-18', missal: 'roman-1962', bible: 'douay-rheims', orations: 'la', mass: 'ash-wednesday', ordinary: '1', 'ordinary-lang': 'en', rubrics: '1' }),
  why: hash({ date: '2026-08-02', missal: 'roman-1962', bible: 'douay-rheims', orations: 'la', mass: 'pentecost-10', ordinary: '1', 'ordinary-lang': 'en', why: '1' }),
  whyTransferred: hash({ date: '2024-03-25', missal: 'roman-1962', bible: 'douay-rheims', orations: 'la', why: '1' }),
  whyLatin: hash({ date: '2020-01-04', missal: 'roman-1962', bible: 'douay-rheims', orations: 'la', why: '1' }),
  whyCommemoration: hash({ date: '2026-01-11', missal: 'roman-1962', bible: 'douay-rheims', orations: 'la', why: '1' }),
  whyCompleteOrationSlots: hash({ date: '2026-01-15', missal: 'roman-1962', bible: 'douay-rheims', orations: 'la', why: '1' }),
  postWhy: hash({ date: '2026-11-29', missal: 'postconciliar', bible: 'douay-rheims', orations: 'la', mass: 'advent-1', ordinary: '1', 'ordinary-lang': 'en', rubrics: '1', why: '1', 'eucharistic-prayer': 'ep-ii' }),
  invalid: hash({ date: '2026-08-02', missal: 'not-a-missal', bible: 'douay-rheims', orations: 'la' }),
  currentStyleLatent: hash({ date: '2026-11-29', missal: 'postconciliar', bible: 'douay-rheims', orations: 'la', mass: 'advent-1', ordinary: '0', 'ordinary-lang': 'en', rubrics: '0', 'eucharistic-prayer': 'ep-ii' }),
  ordinaryLatent: hash({ date: '2026-08-02', missal: 'roman-1962', bible: 'douay-rheims', orations: 'la', mass: 'pentecost-10', ordinary: '0', 'ordinary-lang': 'en', rubrics: '1' }),
  invalidPrayer: hash({ date: '2026-11-29', missal: 'postconciliar', bible: 'douay-rheims', orations: 'la', mass: 'advent-1', ordinary: '1', 'ordinary-lang': 'en', 'eucharistic-prayer': 'ep-99' }),
  inapplicablePrayer: hash({ date: '2026-08-02', missal: 'roman-1962', bible: 'douay-rheims', orations: 'la', mass: 'pentecost-10', ordinary: '1', 'ordinary-lang': 'en', 'eucharistic-prayer': 'ep-ii' }),
  invalidOrdinaryLanguage: hash({ date: '2026-08-02', missal: 'roman-1962', bible: 'douay-rheims', orations: 'la', mass: 'pentecost-10', ordinary: '1', 'ordinary-lang': 'fr' }),
  invalidOrdinary: hash({ date: '2026-08-02', missal: 'roman-1962', bible: 'douay-rheims', orations: 'la', mass: 'pentecost-10', ordinary: 'sometimes' }),
  territorialEpiphany: hash({ date: '2026-01-04', missal: 'postconciliar', bible: 'douay-rheims', orations: 'la' }),
  territorialEpiphanyWhy: hash({ date: '2026-01-04', missal: 'postconciliar', bible: 'douay-rheims', orations: 'la', why: '1' }),
  territorialAscension: hash({ date: '2026-05-17', missal: 'postconciliar', bible: 'douay-rheims', orations: 'la' }),
  territorialCorpus: hash({ date: '2026-06-07', missal: 'postconciliar', bible: 'douay-rheims', orations: 'la' }),
  loadFailure: hash({ date: '2121-08-02', missal: 'roman-1962', bible: 'douay-rheims', orations: 'la' }),
  fastValid: hash({ date: '2026-11-29', missal: 'postconciliar', bible: 'clementine-vulgate', orations: 'la', mass: 'advent-1' }),
  slowYear: hash({ date: '2027-08-01', missal: 'roman-1962', bible: 'douay-rheims', orations: 'la' }),
  // C2 representative-Mass exemplars: Pentecost Sunday in the three principal missals.
  pentecost1962: hash({ date: '2026-05-24', missal: 'roman-1962', bible: 'douay-rheims', orations: 'la', mass: 'pentecost' }),
  pentecost1962English: hash({ date: '2026-05-24', missal: 'roman-1962', bible: 'douay-rheims', orations: 'en', mass: 'pentecost' }),
  pentecost1962Missal: hash({ date: '2026-05-24', missal: 'roman-1962', bible: 'douay-rheims', orations: 'la', mass: 'pentecost', ordinary: '1', 'ordinary-lang': 'en', rubrics: '1', why: '0' }),
  pentecostPostDayEnglish: hash({ date: '2026-05-24', missal: 'postconciliar', bible: 'douay-rheims', orations: 'en', mass: 'pentecost', form: 'day' }),
  pentecostPre1955: hash({ date: '2026-05-24', missal: 'roman-pre-1955', bible: 'douay-rheims', orations: 'la', mass: 'pentecost' }),
  pentecostPre1955Missal: hash({ date: '2026-05-24', missal: 'roman-pre-1955', bible: 'douay-rheims', orations: 'la', mass: 'pentecost', ordinary: '1', 'ordinary-lang': 'en', rubrics: '1', why: '0' }),
  pentecostPostDefaultMissal: hash({ date: '2026-05-24', missal: 'postconciliar', bible: 'douay-rheims', orations: 'la', ordinary: '1', 'ordinary-lang': 'en', rubrics: '1', why: '0' })
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
  return awaitFreshDocumentCommit(cdp, target, previousToken, label);
}

async function reloadFreshDocument(cdp, label) {
  const target = await evaluate(cdp, 'location.href');
  const previousToken = currentDocumentToken;
  const contextCreated = new Promise((accept, reject) => {
    let cancelContextListener = () => {};
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
  await cdp.send('Page.reload', { ignoreCache: true });
  await contextCreated;
  return awaitFreshDocumentCommit(cdp, target, previousToken, label);
}

async function awaitFreshDocumentCommit(cdp, target, previousToken, label) {
  await waitFor(cdp,
    `performance.getEntriesByType('navigation')[0]?.name === ${JSON.stringify(target)} && ` +
      `window.dayReaderReady === true && ` +
      `window.dayReaderDebug.documentToken !== ${JSON.stringify(previousToken)} && ` +
      `window.dayReaderDebug.committedRender !== null && ` +
      `window.dayReaderDebug.committedRender.documentToken === window.dayReaderDebug.documentToken && ` +
      `window.dayReaderDebug.committedRender.generation === window.dayReaderDebug.renders && ` +
      `window.dayReaderDebug.committedRender.href === location.href`,
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
      `performance.getEntriesByType('navigation')[0]?.name === ${JSON.stringify(target)} && ` +
        `window.dayReaderReady !== true`,
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
    `window.dayReaderReady === true && window.dayReaderDebug.renders > ${before} && ` +
      `window.dayReaderDebug.committedRender.generation === window.dayReaderDebug.renders && ` +
      `window.dayReaderDebug.committedRender.generation > ${before} && ` +
      `window.dayReaderDebug.committedRender.documentToken === ${JSON.stringify(documentToken)} && ` +
      `window.dayReaderDebug.committedRender.hash === location.hash && ` +
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
  const expectedHash = canonicalDayHash(expected);
  await evaluate(cdp, `history.${direction}()`);
  await waitFor(cdp,
    `location.hash === ${JSON.stringify(expectedHash)} && window.dayReaderReady === true && ` +
      `window.dayReaderDebug.renders > ${before} && ` +
      `window.dayReaderDebug.committedRender.generation === window.dayReaderDebug.renders && ` +
      `window.dayReaderDebug.committedRender.generation > ${before} && ` +
      `window.dayReaderDebug.committedRender.documentToken === ${JSON.stringify(documentToken)} && ` +
      `window.dayReaderDebug.committedRender.hash === ${JSON.stringify(expectedHash)} && ` +
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
  if (!open) await openSurface(cdp, 'details');
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
      // The DERIVED controls follow the outcome; the controls that leave a day
      // do not. Disabling the whole surface hid no stale value that clearing
      // does not already hide, and it stranded the reader on the failure with
      // nothing that could reach another day. See setDateSurfaceEnabled.
      disabled: [...document.querySelectorAll('#reader-bible, #reader-orations, #reader-formulary, #reader-ordinary-lang, #reader-ordinary-option, #previous-date, #next-date')]
        .every(row => row.disabled),
      escapable: [...document.querySelectorAll('#reader-date, #reader-missal, #date-form .surface-apply, #today-date')]
        .every(row => !row.disabled)
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
        `window.dayReaderReady === true && ` +
        `document.querySelector('#reader-document[aria-busy="false"]') && ` +
        `document.querySelector('#celebration-title').textContent !== 'Loading the Mass…'`,
      'current Day route');
  } catch (error) {
    const snapshot = await evaluate(cdp, `({ href: location.href, title: document.title,
      celebration: document.querySelector('#celebration-title')?.textContent || null,
      busy: document.querySelector('#reader-document')?.getAttribute('aria-busy') || null,
      reading: document.querySelector('#reader-document')?.innerText || null,
      banner: document.querySelector('#coverage-notice')?.innerText || null })`);
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
      `window.dayReaderReady === true && ` +
      `document.querySelector('#reader-document[aria-busy="false"]') && ` +
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

async function openSurface(cdp, name) {
  if (name === 'details') {
    const open = await evaluate(cdp,
      `document.querySelector('[data-reader-surface="mode"]').open`);
    if (!open) await click(cdp, '[data-reader-action="mode"]');
  }
  await click(cdp, `[data-reader-action="${name}"]`);
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
  const canonicalHash = canonicalDayHash(expectedHash);
  try {
    await waitFor(cdp,
      `location.hash === ${JSON.stringify(canonicalHash)} && window.dayReaderReady === true && ` +
        `window.dayReaderDebug.renders > ${before} && ` +
        `window.dayReaderDebug.committedRender.generation === window.dayReaderDebug.renders && ` +
        `window.dayReaderDebug.committedRender.generation > ${before} && ` +
        `window.dayReaderDebug.committedRender.documentToken === ${JSON.stringify(documentToken)} && ` +
        `window.dayReaderDebug.committedRender.hash === ${JSON.stringify(canonicalHash)} && ` +
        `window.dayReaderDebug.committedRender.href === location.href`,
      label);
  } catch (error) {
    const actual = await evaluate(cdp, `({
      hash: location.hash,
      href: location.href,
      ready: window.dayReaderReady,
      renders: window.dayReaderDebug && window.dayReaderDebug.renders,
      committed: window.dayReaderDebug && window.dayReaderDebug.committedRender
    })`);
    throw new Error(`${error.message}; expected ${canonicalHash}; actual ${JSON.stringify(actual)}`);
  }
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

// Whether the selected Latin Proper bodies fall short of exact target wording,
// computed from the same structure and unit coverage records the notice reads.
// The coverage lane regrades these records, so the notice is checked against the
// contract rather than against a fixed count (C2).
async function latinExactIncomplete(cdp, calendar) {
  return evaluate(cdp, `(async () => {
    const structure = await window.Triptych.loadJSON('structure/propers/${calendar}.json');
    const report = window.Triptych.summarizeCoverage(
      window.Triptych.selectedCoverageUnits(dayReaderDebug.semantic, structure));
    const row = report.languages.find(one => one.lang === 'la');
    return row.exact_target < row.occurrences;
  })()`);
}

// Each composed Proper body against its unit coverage record: what is shown,
// and which typed absences its note states (C2 G10, G12).
async function unitAbsenceAudit(cdp, calendar) {
  return evaluate(cdp, `(async () => {
    const T = window.Triptych;
    const structure = await T.loadJSON('structure/propers/${calendar}.json');
    const asked = dayReaderDebug.state.languages.orations;
    const events = [];
    (dayReaderDebug.semantic.events || []).forEach(row => {
      if (row.kind === 'proper') events.push(row);
      if (row.kind === 'proper-choice') (row.options || []).forEach(option =>
        (option.events || []).forEach(member => events.push(member)));
    });
    return events.map(event => {
      const units = T.selectedCoverageUnits({ events: [event] }, structure)
        .filter(unit => unit.component !== 'scripture');
      if (units.length !== 1) return null;
      const state = lang => ((units[0].languages || []).find(row => row.lang === lang) || {}).availability || null;
      const node = document.querySelector('[data-proper-choice-member-event="' + event.id + '"]') ||
        document.querySelector('[data-semantic-event-id="' + event.id + '"]');
      const notes = node ? [...node.querySelectorAll('.unit-absence')] : [];
      return {
        id: event.id, asked, la: state('la'), requested: state(asked),
        composed: node ? [...node.querySelectorAll('.composed')].map(row => ({
          lang: row.lang, original: row.dataset.unitOriginal || null })) : [],
        absences: notes.map(row => row.dataset.unitAbsence || null),
        notes: notes.map(row => row.textContent.trim())
      };
    }).filter(Boolean);
  })()`);
}

const ABSENCE_WORDS = Object.freeze({
  'inapplicable': 'not part of this rite or branch',
  'absent-in-witness': 'not present in this witness',
  'not-sourced': 'not yet sourced',
  'not-publishable': 'not publishable here',
  'unresolved': 'not resolved'
});

async function detailsText(cdp) {
  await openSurface(cdp, 'details');
  const text = await evaluate(cdp, `document.querySelector('[data-reader-details]').innerText`);
  await escape(cdp);
  return text;
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

/**
 * C4 step 2 (2026-10-19): the dialogues held as reviewed per-turn child rows.
 *
 * Self-contained: the expected spoken words are read from the generated
 * Ordinary data (each turn's row less its declared printed marker), so no
 * liturgical text is restated here; the cue glyph and its accessible label
 * come from the reviewed speakers and roles. Measures the visible generated
 * cue, the accessibility tree, the selection and the real clipboard, and that
 * element headings no longer print a cue letter.
 */
async function c4Step2DialogueTurns(cdp, base) {
  await test('C4 step 2 divided dialogues expose one visible, announced and copied cue per turn', async () => {
    const P = ['P', 'Priest'];
    const V = ['℣', 'Versicle — Priest'];
    const R = ['℟', 'Response — Server'];
    const spec = {
      'roman-1962': {
        'praeparatio/introibo-ad-altare-dei': [P, R],
        'praeparatio/judica-me-deus': [P, R],
        'praeparatio/emitte-lucem-tuam': [P, R],
        'praeparatio/confitebor-tibi-in-cithara': [P, R],
        'praeparatio/gloria-patri': [P, R],
        'praeparatio/introibo-ad-altare-dei-repetitio': [P, R],
        'praeparatio/adjutorium-nostrum': [V, R],
        'oblatio/per-omnia-saecula': [V, R],
        'oblatio/sursum-corda': [V, R, V, R, V, R],
        'communio/pax-domini': [P, R],
        'conclusio/dominus-vobiscum-ite-missa-est': [V, R, P, R]
      },
      postconciliar: {
        'prex-eucharistica/praefationis-dialogus': [
          ['℣', 'Versicle — Priest'], ['℟', 'Response — All'],
          ['℣', 'Versicle — Priest'], ['℟', 'Response — All'],
          ['℣', 'Versicle — Priest'], ['℟', 'Response — All']
        ],
        'ritus-communionis/pax-domini': [P, ['℟', 'Response — All']]
      }
    };
    const headed = [
      'oblatio/dominus-vobiscum-ante-evangelium', 'oblatio/laus-tibi-christe',
      'oblatio/dominus-vobiscum-ante-offertorium', 'oblatio/suscipiat-dominus',
      'oblatio/per-omnia-saecula', 'oblatio/sursum-corda',
      'communio/per-omnia-saecula-post-libera-nos', 'communio/pax-domini'
    ];
    // Lasance's held English does not name an actor for the Preface responses.
    // Its Pax retains a printed R. without declaring a target dialogue role.
    const englishSpec = {
      ...spec['roman-1962'],
      'oblatio/per-omnia-saecula': [V, ['℟', 'Response']],
      'oblatio/sursum-corda': [V, ['℟', 'Response'], V, ['℟', 'Response'], V, ['℟', 'Response']],
      'communio/pax-domini': [P, R]
    };
    const data = {};
    for (const calendar of Object.keys(spec)) {
      const file = JSON.parse(await readFile(
        resolve(ROOT, 'src/web/data/structure/ordinary', calendar + '.json'), 'utf8'));
      data[calendar] = new Map(file.sections.flatMap((section) =>
        section.elements.map((element) => [element.key, element])));
    }
    const sourceTurns = (calendar, key, lang) => {
      const held = (data[calendar].get(key).translations || []).find((one) => one.lang === lang);
      assert.ok(held && Array.isArray(held.turns), `${calendar} ${key} ${lang} has turns`);
      return held.turns.map((turn) => ({
        speaker: turn.speaker || null,
        role: turn.dialogue_role || null,
        marker: turn.printed_marker || null,
        words: turn.printed_marker ? turn.text.slice(turn.printed_marker.length + 1) : turn.text
      }));
    };

    await viewport(cdp, 1440, 900);
    await cdp.send('Browser.grantPermissions', {
      origin: base, permissions: ['clipboardReadWrite', 'clipboardSanitizedWrite']
    });
    await cdp.send('Emulation.setFocusEmulationEnabled', { enabled: true });
    try {
      for (const [state, calendar, lang] of [
        [STATES.romanMissal, 'roman-1962', 'en'],
        [STATES.romanLatinMissal, 'roman-1962', 'la'],
        [STATES.postLatinMissal, 'postconciliar', 'la']
      ]) {
        await navigateCandidate(cdp, base, state);
        if (calendar === 'roman-1962') {
          const headings = await evaluate(cdp, `(() => ${JSON.stringify(headed)}.map((key) => {
            const event = [...document.querySelectorAll('[data-semantic-event-id]')]
              .find((node) => node.dataset.semanticEventId === 'ordinary-element/' + key);
            const heading = event && event.querySelector('.proper-name');
            return heading && heading.firstChild ? heading.firstChild.textContent : null;
          }))()`);
          headings.forEach((text, index) => {
            assert.ok(text, headed[index] + ' heading rendered');
            assert.doesNotMatch(text, /^(?:[PRVS]\.|[℣℟])/, headed[index] + ' heading prints no cue');
          });
        }
        for (const [key, cues] of Object.entries(lang === 'en' ? englishSpec : spec[calendar])) {
          const eventId = 'ordinary-element/' + key;
          const expected = sourceTurns(calendar, key, lang);
          assert.equal(expected.length, cues.length, eventId + ' reviewed turn count');
          const observed = await evaluate(cdp, `(async () => {
            const event = [...document.querySelectorAll('[data-semantic-event-id]')]
              .find((node) => node.dataset.semanticEventId === ${JSON.stringify(eventId)});
            if (!event) return null;
            event.scrollIntoView({ block: 'center' });
            const turns = [...event.querySelectorAll('.ordinary-turn')].map((row, index) => {
              row.setAttribute('data-c4s2-probe', String(index));
              const words = row.querySelector('.ordinary-turn-text');
              const label = row.querySelector('.speaker-tag .visually-hidden');
              const selection = getSelection();
              selection.removeAllRanges();
              const range = document.createRange();
              range.selectNodeContents(row);
              selection.addRange(range);
              const selected = selection.toString();
              selection.removeAllRanges();
              return {
                generated: [...row.querySelectorAll('.cue-mark')]
                  .map((mark) => getComputedStyle(mark, '::before').content)
                  .filter((content) => content && content !== 'none' && content !== 'normal')
                  .map((content) => content.replace(/^"|"$/g, '')),
                cueHidden: [...row.querySelectorAll('.cue-mark')].map((mark) => mark.getAttribute('aria-hidden')),
                cueLang: row.querySelector('.speaker-tag')?.lang || null,
                label: label ? label.textContent : null,
                printedMarker: row.dataset.printedMarker || null,
                speaker: row.dataset.speaker || null,
                dialogueRole: row.dataset.dialogueRole || null,
                wordsLang: words ? words.lang : null,
                words: words ? words.textContent : null,
                selected
              };
            });
            const body = event.querySelector('.ordinary-dialogue');
            const selection = getSelection();
            selection.removeAllRanges();
            const range = document.createRange();
            range.selectNodeContents(body);
            selection.addRange(range);
            const copiedOk = document.execCommand('copy');
            selection.removeAllRanges();
            let copied = null;
            try { copied = await navigator.clipboard.readText(); } catch (error) { copied = 'ERROR ' + error; }
            return { turns, copiedOk, copied };
          })()`);
          assert.ok(observed, 'rendered ' + eventId);
          assert.equal(observed.turns.length, cues.length, eventId + ' turn rows');

          const { nodes } = await cdp.send('Accessibility.getFullAXTree');
          const byId = new Map(nodes.map((node) => [node.nodeId, node]));
          const { root } = await cdp.send('DOM.getDocument', { depth: 0 });
          const announced = [];
          for (let index = 0; index < cues.length; index += 1) {
            const { nodeId } = await cdp.send('DOM.querySelector', {
              nodeId: root.nodeId,
              selector: `[data-semantic-event-id="${eventId}"] [data-c4s2-probe="${index}"]`
            });
            const { node } = await cdp.send('DOM.describeNode', { nodeId });
            const start = nodes.find((one) => one.backendDOMNodeId === node.backendNodeId);
            assert.ok(start, eventId + ' turn ' + index + ' is in the accessibility tree');
            const names = [];
            (function walk(one) {
              if (!one.ignored && one.role?.value === 'StaticText') {
                names.push(one.name?.value || '');
                return;
              }
              for (const child of one.childIds || []) {
                const next = byId.get(child);
                if (next) walk(next);
              }
            })(start);
            announced.push(names);
          }

          observed.turns.forEach((turn, index) => {
            const [glyph, label] = cues[index];
            const where = `${calendar} ${eventId} ${lang} turn ${index}`;
            assert.deepEqual(turn.generated, [glyph], where + ' sets exactly one visible cue');
            assert.deepEqual(turn.cueHidden, ['true'], where + ' hides the decorative glyph');
            assert.equal(turn.label, label, where + ' accessible cue');
            assert.equal(turn.cueLang, 'en', where + ' cue language');
            assert.equal(turn.wordsLang, lang, where + ' spoken language');
            assert.equal(turn.printedMarker, expected[index].marker, where + ' separated printed marker');
            assert.equal(turn.speaker, expected[index].speaker, where + ' source actor remains independent of printed sign');
            assert.equal(turn.dialogueRole, expected[index].role, where + ' printed sign adds no target role');
            assert.equal(turn.words, expected[index].words, where + ' spoken words are the source row');
            assert.doesNotMatch(turn.words, /^(?:[PRVS]\.|[℣℟])/, where + ' no printed cue');
            assert.deepEqual(announced[index], [label, turn.words], where + ' announcement');
            assert.equal(announced[index].join(' ').match(/[℣℟]/g), null, where + ' glyph silent');
            assert.equal(turn.selected.replace(/\s+/g, ' ').trim(), label + ' ' + turn.words,
              where + ' selected text');
          });
          if (key === 'praeparatio/introibo-ad-altare-dei' && lang === 'la') {
            // The antiphon label is printed matter, not a cue: it stays.
            assert.match(observed.turns[0].words, /^Anth?\. /, eventId + ' keeps its antiphon label');
          }
          assert.equal(observed.copiedOk, true, eventId + ' copy command');
          assert.equal(
            observed.copied.replace(/\s+/g, ' ').trim(),
            observed.turns.map((turn) => turn.label + ' ' + turn.words).join(' '),
            eventId + ' copied text holds one cue per turn'
          );
        }
      }
    } finally {
      await cdp.send('Emulation.setFocusEmulationEnabled', { enabled: false });
      await cdp.send('Browser.resetPermissions', {});
      await viewport(cdp, 1024, 768);
    }
  });
}

async function runAssertions(cdp, base) {
  await navigateCandidate(cdp, base);
  await viewport(cdp, 393, 852);
  await waitForVisualSettlement(cdp);

  await test('default candidate is calm Read with real content and four persistent actions', async () => {
    const value = await evaluate(cdp, `(() => ({
      path: location.pathname,
      hash: location.hash,
      title: document.querySelector('#celebration-title').textContent,
      meta: document.querySelector('#celebration-meta').textContent,
      noticeHidden: document.querySelector('#coverage-notice').hidden,
      notice: document.querySelector('#coverage-notice').textContent,
      events: [...document.querySelectorAll('[data-semantic-event-id]')].map(row => row.dataset.semanticEventId),
      actions: [...document.querySelectorAll('.reader-actions [data-reader-action]')].map(row => row.textContent.trim()),
      shell: getComputedStyle(document.querySelector('.reader-actions')).position,
      first: document.querySelector('#reader-document .proper').getBoundingClientRect().top,
      viewport: innerHeight
    }))()`);
    assert.equal(value.path, CURRENT);
    assert.equal(value.hash, canonicalDayHash(STATES.roman));
    assert.equal(new URLSearchParams(value.hash.slice(1)).get('mode'), 'read');
    assert.equal(new URLSearchParams(value.hash.slice(1)).has('ordinary'), false);
    assert.equal(value.title, 'Tenth Sunday after Pentecost');
    assert.match(value.meta, /Missale Romanum, editio typica 1962/);
    assert.doesNotMatch(value.meta, /explicit|bound M1|fixture|contract/i);
    // Availability does not establish exact target wording or liturgical
    // Scripture fragments; C1 keeps that qualification visible.
    assert.equal(value.noticeHidden, false);
    assert.match(value.notice, /represented texts/);
    assert.equal(/Exact target wording remains incomplete/.test(value.notice),
      await latinExactIncomplete(cdp, 'roman-1962'), value.notice);
    assert.match(value.notice, /Bible reconstructions/);
    assert.equal(value.events.length, 10);
    assert.deepEqual(value.actions.map(row => row.replace(/\s+/g, ' ')),
      ['Date', 'Contents', 'Mode Read', 'Study']);
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

  await test('St Augustine default day routes render the historical Collect or its explicit absence', async () => {
    for (const [state, language, opening] of [
      [STATES.augustineRomanLatin, 'la', 'Adesto supplicationibus nostris, omnipotens Deus'],
      [STATES.augustineRomanEnglish, 'en', 'Give ear, O Lord, to our prayers']
    ]) {
      await navigateCandidate(cdp, base, state);
      const value = await evaluate(cdp, `(() => {
        const collect = [...document.querySelectorAll('#reader-document .proper')]
          .find(row => row.querySelector('.proper-name')?.childNodes[0]?.textContent.trim() === 'Collect');
        const composed = collect?.querySelector('.composed') || null;
        return {
          formulary: dayReaderDebug.semantic?.resolved?.formulary || null,
          collectCount: [...document.querySelectorAll('#reader-document .proper .proper-name')]
            .filter(row => row.childNodes[0]?.textContent.trim() === 'Collect').length,
          text: composed?.textContent.replace(/\\s+/g, ' ').trim() || '',
          language: composed?.lang || '',
          note: collect?.querySelector('.composed-note')?.textContent.trim() || ''
        };
      })()`);
      assert.equal(value.formulary, 's-augustini-episcopi-confessoris-ecclesiae-doctoris');
      assert.equal(value.collectCount, 1);
      assert.equal(value.language, language);
      assert.match(value.text, new RegExp(opening));
      assert.doesNotMatch(value.note, /unavailable|not recorded|incipit only/i);
    }

    await navigateCandidate(cdp, base, STATES.augustinePostconciliarLatin);
    const unavailable = await evaluate(cdp, `(() => {
      const collect = [...document.querySelectorAll('#reader-document .proper')]
        .find(row => row.querySelector('.proper-name')?.childNodes[0]?.textContent.trim() === 'Collect');
      return {
        formulary: dayReaderDebug.semantic?.resolved?.formulary || null,
        collectCount: [...document.querySelectorAll('#reader-document .proper .proper-name')]
          .filter(row => row.childNodes[0]?.textContent.trim() === 'Collect').length,
        composedCount: collect?.querySelectorAll('.composed').length ?? -1,
        note: collect?.querySelector('.composed-note')?.textContent.trim() || '',
        absence: collect?.querySelector('.unit-absence')?.dataset.unitAbsence || '',
        sectionText: collect?.innerText.replace(/\\s+/g, ' ').trim() || ''
      };
    })()`);
    assert.equal(unavailable.formulary, 'saint-augustine-bishop-doctor-church');
    assert.equal(unavailable.collectCount, 1);
    assert.equal(unavailable.composedCount, 0);
    const typed = /^la:([a-z-]+)$/.exec(unavailable.absence);
    assert.ok(typed && ABSENCE_WORDS[typed[1]], JSON.stringify(unavailable));
    assert.equal(unavailable.note, 'Latin text unavailable: ' + ABSENCE_WORDS[typed[1]] +
      (typed[1] === 'not-publishable' ? ' (its use is rights restricted)' : '') + '.');
    assert.equal(unavailable.sectionText, 'Collect ' + unavailable.note);
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
    assert.match(value.notice, /unavailable in the selected edition or language/i);
    assert.ok(value.completeness.includes('partial'));
  });

  await test('invalid state fails closed while Why preserves the rendered Mass and adds subordinate reasoning', async () => {
    await navigateCandidate(cdp, base, STATES.invalid);
    assert.match(await evaluate(cdp, 'document.querySelector("#reader-document").innerText'), /did not substitute/);
    assert.equal(await evaluate(cdp, 'dayReaderDebug.semantic'), null);
    await navigateCandidate(cdp, base, STATES.why);
    const value = await evaluate(cdp, `(() => {
      const apparatus = document.querySelector('details.day-reasoning[data-reasoning-branch]');
      const reading = document.querySelector('#reader-document');
      return {
        hash: location.hash,
        outcome: dayReaderDebug.outcome,
        why: dayReaderDebug.state.apparatus.why,
        title: document.querySelector('#celebration-title').textContent,
        text: reading.innerText,
        apparatusText: apparatus && apparatus.textContent,
        branch: apparatus && apparatus.dataset.reasoningBranch,
        summary: apparatus && apparatus.querySelector('summary').textContent,
        open: apparatus && apparatus.open,
        followsContent: Boolean(apparatus && apparatus.previousElementSibling &&
          reading.querySelector('[data-semantic-event-id]') && reading.lastElementChild === apparatus),
        links: apparatus ? apparatus.querySelectorAll('a').length : -1,
        deferred: dayReaderDebug.deferred,
        events: document.querySelectorAll('[data-semantic-event-id]').length
      };
    })()`);
    assert.equal(value.hash, canonicalDayHash(STATES.why));
    assert.equal(value.outcome, 'ready');
    assert.equal(value.why, true);
    assert.equal(value.summary, 'Why this Mass');
    assert.equal(value.branch, 'universal');
    assert.equal(value.open, false);
    assert.equal(value.followsContent, true);
    assert.equal(value.links, 0);
    assert.deepEqual(value.deferred, []);
    assert.ok(value.events > 10, JSON.stringify(value));
    assert.equal(value.title, 'Tenth Sunday after Pentecost');
    assert.match(value.apparatusText, /in the calendar/);
    assert.doesNotMatch(value.apparatusText, /Source:\s*index/);
    assert.match(value.apparatusText, /RG 12; RG 91 row 15/);
    assert.match(value.apparatusText, /RG 111; RGMR 434 b/);
    assert.match(value.apparatusText, /RGMR 270/);
    assert.match(value.apparatusText, /Placement in the Ordinary/);
    assert.match(value.apparatusText, /Ordinary resolution/);
    assert.match(value.apparatusText, /Ordinary source notes/);

    await reloadFreshDocument(cdp, 'Why reload');
    assert.equal(await evaluate(cdp, 'location.hash'), canonicalDayHash(STATES.why));
    assert.equal(await evaluate(cdp,
      `document.querySelectorAll('details.day-reasoning').length`), 1);
  });

  await test('Why preserves transferred dates, Latin source text, and complete Proper oration apparatus', async () => {
    await navigateCandidate(cdp, base, STATES.whyTransferred);
    assert.match(await evaluate(cdp,
      `document.querySelector('details.day-reasoning').textContent`),
      /Kept on Monday 8 April 2024\./);

    await navigateCandidate(cdp, base, STATES.whyLatin);
    const latin = await evaluate(cdp, `[...document.querySelectorAll(
      'details.day-reasoning .reasoning-latin[lang="la"]')].map(row => row.textContent.trim())`);
    assert.deepEqual(latin, []);

    await navigateCandidate(cdp, base, STATES.whyCommemoration);
    const proper = await evaluate(cdp,
      `document.querySelector('details.day-reasoning').textContent`);
    assert.match(proper, /Appointed commemorations/);
    assert.match(proper, /What follows the collect/i);
    assert.match(proper, /RG|RGMR/);

    await navigateCandidate(cdp, base, STATES.whyCompleteOrationSlots);
    const completeSlots = await evaluate(cdp,
      `document.querySelector('details.day-reasoning').textContent`);
    assert.doesNotMatch(completeSlots, /carries no oration slot/i);
    assert.match(completeSlots, /What follows the collect/i);
    assert.match(completeSlots, /What follows the secret/i);
    assert.match(completeSlots, /What follows the postcommunion/i);
    const slotLatin = await evaluate(cdp, `[...document.querySelectorAll(
      'details.day-reasoning .reasoning-latin[lang="la"]')].map(row => row.textContent.trim())`);
    assert.ok(slotLatin.some(row => /Intercessio nos, quaesumus/.test(row)), JSON.stringify(slotLatin));

    await navigateCandidate(cdp, base, STATES.postWhy);
    const ordinaryNotes = await evaluate(cdp, `[...document.querySelectorAll(
      'details.day-reasoning [data-reasoning-ordinary-element]')].map(row => row.dataset.reasoningOrdinaryElement)`);
    assert.deepEqual(ordinaryNotes.filter(key => /prex-eucharistica\/(?:prex-eucharistica-)?(?:i|ii|iii|iv)$/.test(key)),
      ['prex-eucharistica/prex-eucharistica-ii']);
  });

  await test('fresh and transitioned outcomes commit identical deterministic mode chrome', async () => {
    const cases = [
      ['invalid Eucharistic Prayer', STATES.invalidPrayer, 'missal', 'invalid', 'invalid', /explicit state rejected/i],
      ['typed before-frame rite', STATES.ashBeforeFrame, 'missal', 'ready', 'ready', /1962/],
      ['Why apparatus', STATES.why, 'missal', 'ready', 'ready', /1962/],
      ['territorial branches', STATES.territorialCorpus, 'read', 'unresolved', 'unresolved', /territorial results/i],
      ['invalid Ordinary value', STATES.invalidOrdinary, null, 'invalid', 'invalid', /Mode unavailable.*explicit state rejected/i],
      ['ready Read', STATES.roman, 'read', 'ready', 'ready', /1962/],
      ['ready Missal', STATES.romanMissal, 'missal', 'ready', 'ready', /1962/]
    ];
    for (const [label, targetState, mode, outcome, outcomeClass, metadata] of cases) {
      const noise = [consoleProblems.length, failedRequests.length, httpProblems.length];
      await navigateCandidate(cdp, base, targetState);
      const direct = await modeOutcomeSnapshot(cdp);
      const expectedHash = direct.state ? canonicalDayHash(targetState) : targetState;
      assert.equal(direct.hash, expectedHash, label + ' direct hash');
      assert.equal(direct.href, direct.committed.href, label + ' committed href');
      assert.equal(direct.mode, mode, label + ' direct mode');
      assert.equal(direct.outcome, outcome, label + ' direct outcome');
      assert.equal(direct.outcomeClass, outcomeClass, label + ' direct class');
      assert.equal(direct.pending, null, label + ' direct pending state');
      assert.equal(direct.modeHeading, 'Mode');
      assert.match(direct.metadata, metadata, label + ' direct metadata');
      assert.deepEqual(direct.modes, [
        { mode: 'read', checked: String(mode === 'read') },
        { mode: 'missal', checked: String(mode === 'missal') },
        { mode: 'study', checked: 'false' },
        { mode: 'compare', checked: 'false' }
      ]);
      assert.equal(direct.modeMetadata, mode === 'read' ? 'Read' : mode === 'missal' ? 'Missal' : 'Unavailable');
      assert.equal(direct.context, 'Day · ' + (mode === 'read' ? 'Read' : mode === 'missal' ? 'Missal' : 'Mode unavailable'));

      for (const origin of [STATES.postconciliar, STATES.postMissal]) {
        await navigateCandidate(cdp, base, origin);
        await transitionHash(cdp, targetState);
        const transitioned = await modeOutcomeSnapshot(cdp);
        assert.equal(transitioned.hash, expectedHash, label + ' transition hash');
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
        { mode: 'missal', checked: 'false' },
        { mode: 'study', checked: 'false' },
        { mode: 'compare', checked: 'false' }
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
      ordinary: false, ordinaryLanguage: 'en', prayer: null,
      hash: canonicalDayHash(STATES.ordinaryLatent)
    });
  });

  await test('Missal, rubrics, and Why are active together without changing the semantic stream', async () => {
    for (const state of [STATES.romanMissal, STATES.postMissal]) {
      await navigateCandidate(cdp, base, state);
      assert.equal(await evaluate(cdp, 'dayReaderDebug.outcome'),
        state === STATES.postMissal ? 'unresolved' : 'ready');
      assert.deepEqual(await evaluate(cdp,
        'dayReaderDebug.semantic.ordinaryUnresolved.map(row => row.element)'),
      state === STATES.postMissal ? ['ritus-initiales/gloria-in-excelsis'] : []);
      assert.equal(await evaluate(cdp, 'dayReaderDebug.state.requestedMode'), 'missal');
      assert.ok((await evaluate(cdp, 'dayReaderDebug.semantic.events.length')) > 10);
      assert.deepEqual(await evaluate(cdp, 'dayReaderDebug.deferred'), []);
    }
    await navigateCandidate(cdp, base, STATES.romanMissal);
    const withoutWhy = await evaluate(cdp,
      `dayReaderDebug.semantic.events.map(row => row.id)`);
    await navigateCandidate(cdp, base, STATES.why);
    assert.deepEqual(await evaluate(cdp,
      `dayReaderDebug.semantic.events.map(row => row.id)`), withoutWhy);
    assert.deepEqual(await evaluate(cdp, 'dayReaderDebug.deferred'), []);
    assert.equal(await evaluate(cdp, 'dayReaderDebug.outcome'), 'ready');
    assert.equal(await evaluate(cdp, 'dayReaderDebug.state.apparatus.why'), true);
    assert.equal(await evaluate(cdp,
      `document.querySelectorAll('details.day-reasoning[data-reasoning-branch]').length`), 1);
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
      // 2026-10-19 (C2 G5/G6): Pentecost X shows one Preface stand-in for
      // the 25 unappointed Preface rows and loses the six excluded
      // second-Postcommunion and Et famulos rows.
      // 2026-10-19 (C2 Preface directions): Pentecost X seats its printed
      // Trinity Preface (with the 1861 asterisk note and heading) in place of
      // the one typed stand-in, so two more Ordinary events.
      // 2026-10-19 (C3 Ordinary variables): the 1962 Canon continues the
      // common Communicantes with canon/communicantes-continuatio, one more
      // Ordinary event.
      [STATES.romanMissal, 178, 6, 162, 10, 'proper/roman-1962/pentecost-10/010'],
      [STATES.postMissal, 58, 7, 41, 10, 'proper/postconciliar/advent-1/010']
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
          checked: document.querySelector(
            '[data-option-group="eucharistic-prayer"] input:checked')?.value || null
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
        // Pentecost X's own texts are all held since 3f86eed68; what the Missal
        // mode still lacks is the uncollated antecedent Ordinary, which is a
        // text not held here rather than one withheld.
        assert.equal(await evaluate(cdp, 'document.querySelector("#coverage-notice").hidden'), false);
        assert.match(await evaluate(cdp,
          'document.querySelector("#coverage-notice").textContent'), /not held in this repository/i);
      }
    }
  });

  await test('source-choice and non-full forms render in exact source order without borrowing an Ordinary', async () => {
    await navigateCandidate(cdp, base, STATES.postPentecostDayMissal);
    const pentecost = await evaluate(cdp, `(() => {
      const semantic = dayReaderDebug.semantic;
      const events = semantic.events;
      const choice = events.find(row => row.kind === 'proper-choice');
      return {
        outcome: dayReaderDebug.outcome,
        mode: dayReaderDebug.state.requestedMode,
        formulary: semantic.resolved.formulary,
        form: semantic.resolved.form,
        eventIds: events.map(row => row.id),
        eventKinds: events.map(row => row.kind),
        seats: events.filter(row => row.kind === 'proper' || row.kind === 'proper-choice')
          .map(row => row.seat),
        ordinaryEvents: events.filter(row => row.kind.startsWith('ordinary-')).length,
        domIds: [...document.querySelectorAll('#reader-document [data-semantic-event-id]')]
          .map(row => row.dataset.semanticEventId),
        ordinaryDom: document.querySelectorAll(
          '#reader-document .ordinary-element, #reader-document .ordinary-division').length,
        frameLimitation: document.querySelector('.missal-frame-limitation')?.textContent
          .replace(/\\s+/g, ' ').trim() || '',
        frame: semantic.coverage.find(row =>
          row.scope === 'ordinary-frame:postconciliar') || null,
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
    const pentecostIds = [
      'proper-choice/postconciliar/pentecost/day/entrance-antiphon',
      ...Array.from({ length: 10 }, (_row, index) =>
        'proper/postconciliar/pentecost/' + String(index + 17).padStart(3, '0'))
    ];
    // 2026-10-19 (C2 G7): IGMR 64 seats the Sequence before the Alleluia, so
    // the Day form takes the full frame and every Proper is seated in order.
    const properIds = pentecost.eventIds.filter(id => id.startsWith('proper'));
    assert.equal(pentecost.outcome, 'unresolved');
    assert.equal(pentecost.mode, 'missal');
    assert.equal(pentecost.formulary, 'pentecost');
    assert.equal(pentecost.form, 'day');
    assert.deepEqual(properIds, pentecostIds);
    assert.deepEqual(pentecost.domIds, pentecost.eventIds);
    assert.ok(pentecost.seats.every(row => row && row.id && row.placement === 'seated'));
    assert.ok(pentecost.ordinaryEvents > 0);
    assert.ok(pentecost.ordinaryDom > 0);
    assert.equal(pentecost.frameLimitation, '');
    assert.ok(!pentecost.frame || pentecost.frame.state !== 'unavailable');
    const at = (id) => pentecost.eventIds.indexOf(id);
    assert.ok(at('proper/postconciliar/pentecost/020') < at('proper/postconciliar/pentecost/021'));
    assert.ok(at('proper/postconciliar/pentecost/021') <
      at('ordinary-element/liturgia-verbi/acclamatio-ante-evangelium'));
    assert.ok(at('ordinary-element/liturgia-verbi/acclamatio-ante-evangelium') <
      at('proper/postconciliar/pentecost/022'));
    assert.ok(at('ordinary-element/prex-eucharistica/praefatio-appointed') > 0);
    assert.equal(at('ordinary-element/prex-eucharistica/praefatio'), -1);
    assert.ok(at('ordinary-element/ritus-conclusionis/dimissio-appointed') > 0);
    assert.equal(at('ordinary-element/ritus-conclusionis/dimissio'), -1);
    assert.deepEqual(pentecost.choice, {
      id: 'proper-choice/postconciliar/pentecost/day/entrance-antiphon',
      group: 'entrance-antiphon',
      selection: { state: 'required', option: null },
      options: [
        { id: 'spiritus-domini', events: ['proper/postconciliar/pentecost/015'] },
        { id: 'caritas-dei', events: ['proper/postconciliar/pentecost/016'] }
      ]
    });
    assert.deepEqual(pentecost.unresolved, [{
      id: pentecost.choice.id, options: ['spiritus-domini', 'caritas-dei']
    }]);
    assert.deepEqual(pentecost.domChoice, {
      group: 'entrance-antiphon', state: 'required',
      options: [['spiritus-domini', 'available'], ['caritas-dei', 'available']],
      members: ['proper/postconciliar/pentecost/015', 'proper/postconciliar/pentecost/016'],
      note: 'The source appoints one of these alternatives here. None is selected; the option groups below are not cumulative.'
    });

    await navigateCandidate(cdp, base, STATES.romanEmberLongerMissal);
    const ember = await evaluate(cdp, `(() => {
      const semantic = dayReaderDebug.semantic;
      const events = semantic.events;
      return {
        outcome: dayReaderDebug.outcome,
        mode: dayReaderDebug.state.requestedMode,
        formulary: semantic.resolved.formulary,
        form: semantic.resolved.form,
        eventIds: events.map(row => row.id),
        seats: events.filter(row => row.kind === 'proper').map(row => row.seat),
        ordinaryEvents: events.filter(row => row.kind.startsWith('ordinary-')).length,
        domIds: [...document.querySelectorAll('#reader-document [data-semantic-event-id]')]
          .map(row => row.dataset.semanticEventId),
        frame: semantic.coverage.find(row =>
          row.scope === 'ordinary-frame:roman-1962') || null,
        frameLimitation: document.querySelector('.missal-frame-limitation')?.textContent
          .replace(/\\s+/g, ' ').trim() || '',
        visibleNames: [...document.querySelectorAll('#reader-document .proper-name')]
          .map(row => [...row.childNodes].find(node => node.nodeType === Node.TEXT_NODE)
            ?.textContent.trim() || '')
      };
    })()`);
    const emberIds = Array.from({ length: 24 }, (_row, index) =>
      'proper/roman-1962/advent-ember-saturday/' + String(index + 1).padStart(3, '0'));
    assert.equal(ember.outcome, 'ready');
    assert.equal(ember.mode, 'missal');
    assert.equal(ember.formulary, 'advent-ember-saturday');
    assert.equal(ember.form, 'longer');
    assert.deepEqual(ember.eventIds, emberIds);
    assert.deepEqual(ember.domIds, emberIds);
    assert.ok(ember.seats.every(row => row === null));
    assert.equal(ember.ordinaryEvents, 0);
    assert.match(ember.frameLimitation, /Ordinary frame is unavailable/i);
    assert.match(ember.frameLimitation, /source order.*not invented/is);
    assert.equal(ember.frame.state, 'unavailable');
    assert.equal(ember.frame.scope, 'ordinary-frame:roman-1962');
    assert.deepEqual(ember.frame.reasons.map(row => [row.kind, row.applicability]),
      [['text-not-held', 'unavailable']]);
    assert.ok(ember.frame.reasons[0].basis.trim().length > 0);
    assert.deepEqual(ember.visibleNames.slice(2, 20), [
      'First Lesson', 'First Gradual', 'Oratio', 'Second Lesson', 'Second Gradual',
      'Oratio', 'Third Lesson', 'Third Gradual', 'Oratio', 'Fourth Lesson', 'Fourth Gradual',
      'Oratio', 'Fifth Lesson', 'Hymn (Benedictus es)', 'Oratio', 'Epistle', 'Tract', 'Gospel'
    ]);
  });

  await test('C2 G5-G8: Pentecost seats exactly its appointed Ordinary variables in all three missals', async () => {
    const read = () => evaluate(cdp, `(() => ({
      outcome: dayReaderDebug.outcome,
      form: dayReaderDebug.semantic && dayReaderDebug.semantic.resolved.form || null,
      ids: dayReaderDebug.semantic ? dayReaderDebug.semantic.events.map(row => row.id) : [],
      text: document.querySelector('#reader-document').innerText
    }))()`);
    for (const state of [STATES.pentecost1962Missal, STATES.pentecostPre1955Missal]) {
      await navigateCandidate(cdp, base, state);
      const day = await read();
      const is1962 = state === STATES.pentecost1962Missal;
      const prefaces = day.ids.filter(id => /^ordinary-element\/praefatio\/praefatio/.test(id));
      // C3, 2026-10-19: the 1962 Holy Spirit Preface carries the common
      // opening up to its printed junction; pre-1955 is unchanged.
      assert.deepEqual(prefaces, [
        'ordinary-element/praefatio/praefatio-de-spiritu-sancto-heading',
        ...(is1962 ? ['ordinary-element/praefatio/praefatio-de-spiritu-sancto-initium'] : []),
        'ordinary-element/praefatio/praefatio-de-spiritu-sancto'
      ]);
      assert.ok(day.ids.includes('ordinary-element/canon/communicantes-pentecoste'));
      assert.ok(day.ids.includes('ordinary-element/canon/hanc-igitur-pascha-pentecoste'));
      assert.ok(!day.ids.includes('ordinary-element/canon/communicantes'));
      assert.ok(!day.ids.includes('ordinary-element/canon/hanc-igitur'));
      assert.ok(!day.ids.includes('ordinary-element/oblatio/a-cunctis'));
      assert.ok(!day.ids.includes('ordinary-element/conclusio/postcommunio-mundet'));
      if (is1962) {
        assert.equal(day.ids.indexOf('ordinary-element/canon/communicantes-pentecoste') + 1,
          day.ids.indexOf('ordinary-element/canon/communicantes-continuatio'));
        assert.doesNotMatch(day.text, /The appointed proper Canon form is not held here \(witness gap\)/);
        assert.match(day.text, /Held English lacks the 1962 Saint Joseph clause \(witness gap\)/);
        const preface = await evaluate(cdp, `(() => {
          const node = document.querySelector('[data-semantic-event-id="ordinary-element/praefatio/praefatio-de-spiritu-sancto"]');
          const mark = node && node.querySelector('.ordinary-conditional');
          const opening = document.querySelector('[data-semantic-event-id="ordinary-element/praefatio/praefatio-de-spiritu-sancto-initium"]');
          return {
            marked: mark ? mark.textContent : null,
            note: node ? Array.from(node.querySelectorAll('.ordinary-conditional-note')).map(one => one.textContent) : [],
            opening: opening ? opening.innerText.length : 0
          };
        })()`);
        assert.ok(preface.marked && preface.marked.startsWith('['), JSON.stringify(preface));
        assert.equal(preface.note.length, 1, JSON.stringify(preface));
        assert.match(preface.note[0], /vigil of Pentecost/);
        assert.ok(preface.opening > 40, JSON.stringify(preface));
      } else {
        assert.match(day.text, /The appointed proper Canon form is not held here \(witness gap\)/);
      }
    }
    await navigateCandidate(cdp, base, STATES.pentecostPostDefaultMissal);
    const post = await read();
    assert.equal(post.form, 'day');
    assert.ok(post.ids.includes('ordinary-element/prex-eucharistica/praefatio-appointed'));
    assert.ok(post.ids.indexOf('proper/postconciliar/pentecost/021') <
      post.ids.indexOf('ordinary-element/liturgia-verbi/acclamatio-ante-evangelium'));
  });

  await test('valid unavailable language, partial coverage, and typed before-frame rites remain honest', async () => {
    await navigateCandidate(cdp, base, STATES.romanLatinMissal);
    assert.equal(await evaluate(cdp, 'dayReaderDebug.state.languages.ordinary'), 'la');
    const unavailableLatin = await evaluate(cdp,
      'document.querySelector("#reader-document").innerText');
    assert.match(unavailableLatin, /The 1861 witness prints this block only in English \(witness gap\)/);
    // 2026-10-19 (C2 G6): both not-in-the-1962-ordo orations are excluded,
    // so that reason no longer stands at any emitted element.
    assert.doesNotMatch(unavailableLatin, /This older oration is outside the 1962 Ordinary \(witness gap\)/);
    // 2026-10-19 (C2 Preface directions): the Sunday's printed Trinity
    // Preface is appointed, so no typed "appointment not established" stands.
    assert.doesNotMatch(unavailableLatin, /This day’s Ordinary appointment is not established \(model gap\)/);
    assert.match(unavailableLatin, /Qui cum unigenito Filio tuo/);
    assert.match(unavailableLatin, /The 1861 lay witness supplies its own English heading or rubric \(witness gap\)/);
    assert.equal(await evaluate(cdp, 'document.querySelector("#coverage-notice").hidden'), false);
    await navigateCandidate(cdp, base, STATES.partial);
    assert.equal(await evaluate(cdp, 'dayReaderDebug.outcome'), 'ready');
    assert.match(await evaluate(cdp,
      'document.querySelector("#coverage-notice").textContent'),
      /unavailable in the selected edition or language/i);
    await navigateCandidate(cdp, base, STATES.ashBeforeFrame);
    const ash = await evaluate(cdp, `(() => {
      const events = dayReaderDebug.semantic.events;
      const prefix = events.slice(0, 5);
      return {
        outcome: dayReaderDebug.outcome,
        ids: prefix.map(row => row.id),
        seats: prefix.map(row => row.seat),
        notes: [...document.querySelectorAll(
          '.proper-unplaced-before-frame .proper-unplaced-note')].map(row =>
            row.textContent.replace(/\\s+/g, ' ').trim()),
        ordinary: events.filter(row => row.kind.startsWith('ordinary-')).length,
        frame: dayReaderDebug.semantic.coverage.find(row => row.scope === 'ordinary-frame:roman-1962'),
        limitation: document.querySelector('.missal-frame-limitation')?.textContent || '',
        domIds: [...document.querySelectorAll('#reader-document [data-semantic-event-id]')]
          .map(row => row.dataset.semanticEventId)
      };
    })()`);
    assert.equal(ash.outcome, 'ready');
    assert.deepEqual(ash.ids, Array.from({ length: 5 }, (_row, index) =>
      'proper/roman-1962/ash-wednesday/' + String(index + 1).padStart(3, '0')));
    assert.ok(ash.seats.every(row => row && row.placement === 'unseated' &&
      row.region === 'before-frame' && row.id ===
        'unplaced/roman-1962/ash-wednesday/main/blessing-and-imposition-of-ashes' &&
      row.basis.trim().length > 0));
    assert.equal(ash.notes.length, 5);
    assert.ok(ash.notes.every(row => /before the ordinary Mass frame.*no Ordinary seat is invented/i.test(row)));
    assert.equal(ash.ordinary, 0);
    assert.equal(ash.frame.state, 'unavailable');
    assert.match(ash.frame.reasons[0].basis, /Oratio super populum/i);
    assert.match(ash.limitation, /Ordinary frame is unavailable/i);
    assert.deepEqual(ash.domIds,
      await evaluate(cdp, 'dayReaderDebug.semantic.events.map(row => row.id)'));
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
      propers: [...document.querySelectorAll('#reader-document .proper')].map(row =>
        row.textContent.replace(/\\s+/g, ' ').trim())
    })`);
    assert.equal(candidate.title, current.title);
    assert.equal(candidate.date, current.date);
    assert.equal(candidate.date, 'Sunday 29 November 2026');
    assert.deepEqual(candidate.propers, current.propers);
    assert.deepEqual(candidate.state, { rubrics: false, ordinary: false, prayer: 'ep-ii' });
  });

  await test('first visit uses repository defaults without remembered or geographic state', async () => {
    const fixedClock = await cdp.send('Page.addScriptToEvaluateOnNewDocument', { source: `
      (() => {
        const OriginalDate = Date;
        // 23 October: Claret's own Collect is still withheld, so the first
        // visit has a limitation to disclose even without the Ordinary.
        const fixed = new OriginalDate(2026, 9, 23, 12, 0, 0, 0).getTime();
        class FixedDate extends OriginalDate {
          constructor(...args) { super(...(args.length ? args : [fixed])); }
          static now() { return fixed; }
        }
        Object.setPrototypeOf(FixedDate, OriginalDate);
        globalThis.Date = FixedDate;
      })();
    ` });
    try {
      await navigateCandidate(cdp, base, '');
      const state = await evaluate(cdp, 'dayReaderDebug.state');
      assert.equal(state.civilDate, '2026-10-23');
      assert.equal(state.edition.id, 'roman-1962');
      assert.equal(state.bible.id, 'douay-rheims');
      assert.equal(state.languages.orations, 'la');
      assert.equal(state.options.ordinary, false);
      assert.equal(state.requestedMode, 'read');
      assert.equal(await evaluate(cdp, 'document.querySelector("#coverage-notice").hidden'), false);
      assert.match(await evaluate(cdp,
        'document.querySelector("#coverage-notice").textContent'), /unavailable/i);
    } finally {
      await cdp.send('Page.removeScriptToEvaluateOnNewDocument', {
        identifier: fixedClock.identifier
      });
    }
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

  await test('territorial branches preserve resolved documents and branch-local form choices', async () => {
    const cases = [
      [STATES.territorialEpiphany, 'unresolved', [
        ['epiphany-january-6', 'Second Sunday after the Nativity', false],
        ['epiphany-transferred-to-sunday', 'The Epiphany of the Lord', true]
      ]],
      [STATES.territorialAscension, 'unresolved', [
        ['ascension-thursday', 'Seventh Sunday of Easter', false],
        ['ascension-transferred-to-sunday', 'The Ascension of the Lord', true]
      ]],
      [STATES.territorialCorpus, 'unresolved', [
        ['corpus-christi-thursday', 'Tenth Sunday in Ordinary Time', false],
        ['corpus-christi-transferred-to-sunday', 'The Most Holy Body and Blood of Christ', false]
      ]]
    ];
    for (const [state, outcome, expected] of cases) {
      await navigateCandidate(cdp, base, state);
      const value = await evaluate(cdp, `(() => ({
        hash: location.hash,
        outcome: dayReaderDebug.outcome,
        stateTerritory: dayReaderDebug.state.calendar.territory || null,
        publicTerritory: new URLSearchParams(location.hash.slice(1)).has('territory'),
        semantic: dayReaderDebug.semantic.map(row => ({
          territory: row.territory,
          prefix: row.prefix,
          eventIds: row.document.events.map(event => event.id)
        })),
        branches: [...document.querySelectorAll('section.territorial-branch[data-territorial-branch]')]
          .map(row => ({
            option: row.dataset.territorialBranch,
            label: row.querySelector('.territorial-branch-label').textContent.trim(),
            title: row.querySelector('h2').textContent.trim(),
            formChoice: Boolean(row.querySelector('.proper-form-choice')),
            formOptions: [...row.querySelectorAll('.proper-form-choice [data-choice-option]')]
              .map(option => option.value),
            locations: [...row.querySelectorAll('[data-semantic-location]')]
              .map(event => event.dataset.semanticLocation),
            eventIds: [...row.querySelectorAll('[data-semantic-event-id]')]
              .map(event => event.dataset.semanticEventId)
          })),
        overflow: document.documentElement.scrollWidth - document.documentElement.clientWidth
      }))()`);
      assert.equal(value.hash, canonicalDayHash(state));
      assert.equal(value.outcome, outcome);
      assert.equal(value.stateTerritory, null);
      assert.equal(value.publicTerritory, false);
      assert.equal(value.overflow, 0);
      assert.deepEqual(value.branches.map(row => [row.option, row.title, row.formChoice]), expected);
      assert.deepEqual(value.semantic.map(row => row.territory), expected.map(row => row[0]));
      value.branches.forEach((branch, index) => {
        const option = expected[index][0];
        assert.match(branch.label, new RegExp(option.replace(/-/g, ' '), 'i'));
        assert.equal(branch.locations.length > 0, !expected[index][2], JSON.stringify(branch));
        assert.ok(branch.locations.every(location => location.startsWith(`territory/${option}/`)),
          JSON.stringify(branch));
        assert.deepEqual(branch.eventIds, value.semantic[index].eventIds);
        assert.equal(value.semantic[index].prefix, `territory/${option}/`);
        if (expected[index][2]) assert.deepEqual(branch.formOptions, ['vigil', 'day']);
      });
    }

    await navigateCandidate(cdp, base, STATES.territorialEpiphanyWhy);
    const why = await evaluate(cdp, `(() => ({
      hash: location.hash,
      branches: [...document.querySelectorAll('section.territorial-branch')].map(row => ({
        option: row.dataset.territorialBranch,
        apparatus: row.querySelectorAll('details.day-reasoning').length,
        loci: row.querySelectorAll('.reasoning-locus').length,
        links: row.querySelectorAll('details.day-reasoning a').length
      }))
    }))()`);
    assert.equal(why.hash, canonicalDayHash(STATES.territorialEpiphanyWhy));
    assert.deepEqual(why.branches.map(row => row.option),
      ['epiphany-january-6', 'epiphany-transferred-to-sunday']);
    assert.ok(why.branches.every(row => row.apparatus === 1 && row.loci > 0 && row.links === 0),
      JSON.stringify(why));
    await reloadFreshDocument(cdp, 'territorial Why reload');
    assert.equal(await evaluate(cdp, 'location.hash'),
      canonicalDayHash(STATES.territorialEpiphanyWhy));
    assert.equal(await evaluate(cdp,
      `document.querySelectorAll('section.territorial-branch details.day-reasoning').length`), 2);
  });

  await test('Apply clears outgoing edition variants while same-edition dates and history preserve them', async () => {
    for (const origin of [STATES.postReadLatent,
      updatedHash(STATES.postMissal, 'eucharistic-prayer', 'ep-iii')]) {
      await navigateCandidate(cdp, base, origin + '&future-option=preserve-me');
      const mode = await evaluate(cdp, 'dayReaderDebug.state.requestedMode');
      const prayer = await evaluate(cdp,
        `dayReaderDebug.state.options.legitimate['eucharistic-prayer']`);
      await click(cdp, '[data-reader-action="date"]');
      await evaluate(cdp, `document.querySelector('#reader-date').value = '2026-12-06'`);
      const sameEdition = hash({
        date: '2026-12-06', missal: 'postconciliar', bible: 'douay-rheims',
        orations: 'la', mode, 'ordinary-lang': 'en',
        rubrics: mode === 'missal' ? '1' : '0',
        'eucharistic-prayer': prayer, 'future-option': 'preserve-me'
      });
      let before = await evaluate(cdp, 'dayReaderDebug.renders');
      await click(cdp, '#date-form .surface-apply');
      await waitForCommittedRender(cdp, before, sameEdition, 'same-edition Apply');
      assert.equal(await evaluate(cdp,
        `dayReaderDebug.state.options.legitimate['eucharistic-prayer']`), prayer);

      await click(cdp, '[data-reader-action="date"]');
      await evaluate(cdp, `document.querySelector('#reader-missal').value = 'roman-1962'`);
      const params = new URLSearchParams(sameEdition.slice(1));
      params.set('missal', 'roman-1962');
      params.delete('eucharistic-prayer');
      const changedEdition = '#' + params.toString();
      before = await evaluate(cdp, 'dayReaderDebug.renders');
      await click(cdp, '#date-form .surface-apply');
      await waitForCommittedRender(cdp, before, changedEdition, 'changed-edition Apply');
      const selected = await evaluate(cdp, `({
        edition: dayReaderDebug.state.edition.id,
        mode: dayReaderDebug.state.requestedMode,
        outcome: dayReaderDebug.outcome,
        options: dayReaderDebug.state.options.legitimate,
        properCount: document.querySelectorAll('#reader-document .proper').length
      })`);
      assert.equal(selected.edition, 'roman-1962');
      assert.equal(selected.mode, mode);
      assert.equal(selected.outcome, 'ready');
      assert.deepEqual(selected.options, {});
      assert.ok(selected.properCount > 0);

      await historyMove(cdp, 'back', sameEdition);
      assert.equal(await evaluate(cdp, 'dayReaderDebug.state.edition.id'), 'postconciliar');
      assert.equal(await evaluate(cdp,
        `dayReaderDebug.state.options.legitimate['eucharistic-prayer']`), prayer);
      await historyMove(cdp, 'forward', changedEdition);
      assert.equal(await evaluate(cdp, 'dayReaderDebug.state.edition.id'), 'roman-1962');
      assert.equal(await evaluate(cdp, 'dayReaderDebug.outcome'), 'ready');
    }
  });

  await test('active and latent state remain distinct through Back and Forward', async () => {
    const active = STATES.postMissal;
    await navigateCandidate(cdp, base, STATES.currentStyleLatent);
    await transitionHash(cdp, active);
    assert.equal(await evaluate(cdp, 'dayReaderDebug.outcome'), 'unresolved');
    assert.equal(await evaluate(cdp, 'dayReaderDebug.state.requestedMode'), 'missal');
    await historyMove(cdp, 'back', STATES.currentStyleLatent);
    assert.equal(await evaluate(cdp, 'dayReaderDebug.outcome'), 'ready');
    assert.equal(await evaluate(cdp, 'dayReaderDebug.state.apparatus.rubrics'), false);
    assert.equal(await evaluate(cdp,
      `dayReaderDebug.state.options.legitimate['eucharistic-prayer']`), 'ep-ii');
    await historyMove(cdp, 'forward', active);
    assert.equal(await evaluate(cdp, 'dayReaderDebug.outcome'), 'unresolved');
    assert.equal(await evaluate(cdp, 'dayReaderDebug.state.requestedMode'), 'missal');
  });

  await test('failed transitions cannot expose prior selection state', async () => {
    const stalePattern = /Tenth Sunday|2026-08-02|Missale Romanum|pentecost-10|Universal|proper-structure|Resolved Day result/i;
    await navigateCandidate(cdp, base, STATES.roman);
    await transitionHash(cdp, STATES.invalid);
    assert.equal(await evaluate(cdp, 'dayReaderDebug.outcome'), 'invalid');
    assert.equal(await evaluate(cdp, 'dayReaderDebug.state'), null);
    await click(cdp, '[data-reader-action="date"]');
    const invalidDate = await evaluate(cdp, `({
      text: document.querySelector('#date-surface').innerText,
      values: [...document.querySelectorAll('#date-form input, #date-form select')].map(row => row.value),
      disabled: [...document.querySelectorAll('#reader-bible, #reader-orations, #reader-formulary, #reader-ordinary-lang, #reader-ordinary-option, #previous-date, #next-date')].every(row => row.disabled),
      escapable: [...document.querySelectorAll('#reader-date, #reader-missal, #date-form .surface-apply, #today-date')].every(row => !row.disabled)
    })`);
    assert.doesNotMatch(invalidDate.text, stalePattern);
    assert.ok(invalidDate.values.every(value => value === ''), JSON.stringify(invalidDate));
    assert.equal(invalidDate.disabled, true);
    // ...and the way out of the failure is still live. A cleared control shows
    // no prior selection; a disabled one shows no way back.
    assert.equal(invalidDate.escapable, true);
    await escape(cdp);
    await openSurface(cdp, 'details');
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
    await openSurface(cdp, 'details');
    const failedDetails = await evaluate(cdp, `document.querySelector('[data-reader-details]').innerText`);
    assert.match(failedDetails, /No validated selection.*unrenderable outcome/i);
    assert.doesNotMatch(failedDetails, stalePattern);
    await escape(cdp);

  });

  await test('Why state returns to plain Read and Forward restores the ready apparatus', async () => {
    await navigateCandidate(cdp, base, STATES.roman);
    await transitionHash(cdp, STATES.why);
    assert.equal(await evaluate(cdp, 'dayReaderDebug.outcome'), 'ready');
    assert.equal(await evaluate(cdp, `document.querySelectorAll('details.day-reasoning').length`), 1);
    await historyMove(cdp, 'back', STATES.roman);
    assert.equal(await evaluate(cdp, 'dayReaderDebug.outcome'), 'ready');
    assert.equal(await evaluate(cdp, 'dayReaderDebug.semantic.resolved.formulary'), 'pentecost-10');
    assert.equal(await evaluate(cdp, `document.querySelectorAll('details.day-reasoning').length`), 0);
    await historyMove(cdp, 'forward', STATES.why);
    assert.equal(await evaluate(cdp, 'dayReaderDebug.outcome'), 'ready');
    assert.equal(await evaluate(cdp, `document.querySelectorAll('details.day-reasoning').length`), 1);
    assert.equal(await evaluate(cdp, 'dayReaderDebug.semantic.resolved.formulary'), 'pentecost-10');
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
      assert.equal(before.outcome, 'unresolved');
      assert.equal(before.title, 'First Sunday of Advent');
      assert.equal(before.state.edition.id, 'postconciliar');
      assert.equal(before.state.requestedMode, 'missal');
      assert.equal(before.semantic.resolved.formulary, 'advent-1');
      assert.equal(before.semantic.events.length, 58);
      await settleResponseGate(cdp, gate);
      const after = await candidateOutcomeSnapshot(cdp);
      assert.deepEqual(after, before);
    } finally {
      gate.release();
    }
  });

  await test('Details opened during a territorial load refreshes only from the committed result', async () => {
    const gate = await beginGatedCandidate(
      cdp, base, STATES.territorialEpiphany,
      (relative) => relative.endsWith('/douay-rheims/chapters/Wis/18.json'),
      'slow territorial scripture fragment'
    );
    try {
      await openSurface(cdp, 'details');
      const loading = await evaluate(cdp,
        `document.querySelector('[data-reader-details]').textContent`);
      assert.match(loading, /still loading/);
      assert.doesNotMatch(loading, /Territorial result\s+Universal/);
      gate.release();
      await gate.served;
      await waitFor(cdp,
        `window.dayReaderReady === true && dayReaderDebug.outcome === 'unresolved' && ` +
        `dayReaderDebug.semantic.length === 2`, 'territorial Details commit');
      const committed = await evaluate(cdp, `({
        open: document.querySelector('[data-reader-surface="details"]').open,
        text: document.querySelector('[data-reader-details]').innerText,
        headings: [...document.querySelectorAll('[data-reader-details] .details-section > h3')]
          .map(row => row.textContent.trim())
      })`);
      assert.equal(committed.open, true);
      assert.match(committed.text, /epiphany-january-6; epiphany-transferred-to-sunday/);
      assert.match(committed.text, /current request is validated, but no formulary outcome has been selected/i);
      assert.deepEqual(committed.headings,
        ['Selection', 'Reader outcome', 'Related reader', 'Elsewhere in Triptych']);
      await escape(cdp);
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
      assert.equal(await evaluate(cdp, 'location.hash'), canonicalDayHash(STATES.roman));
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
      await openSurface(cdp, name);
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
      assert.equal(closed.focus, name === 'details' ? 'mode' : name);
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


  await test('C2 G9: Bible-reconstructed units carry one quiet claim in Read, Missal and print', async () => {
    await navigateCandidate(cdp, base, STATES.pentecost1962);
    assertBibleClaims(await bibleClaimAudit(cdp, 'dayReaderDebug', 'roman-1962'), 'Day 1962 Pentecost Read');
    const printed = await claimsSurvivePrint(cdp);
    assert.ok(printed.length > 0 && printed.every(Boolean), JSON.stringify(printed));
    await navigateCandidate(cdp, base, STATES.pentecost1962Missal);
    assert.equal(await evaluate(cdp, 'dayReaderDebug.mode'), 'missal');
    assertBibleClaims(await bibleClaimAudit(cdp, 'dayReaderDebug', 'roman-1962'), 'Day 1962 Pentecost Missal');
  });

  await test('C2 G9 follow-up: mixed units label their passages as Bible text, not a reconstruction', async () => {
    for (const state of [STATES.pentecost1962, STATES.pentecost1962Missal]) {
      await navigateCandidate(cdp, base, state);
      assertMixedClaims(await mixedClaimAudit(cdp, 'roman-1962', 'pentecost'),
        'Day 1962 Pentecost ' + await evaluate(cdp, 'dayReaderDebug.mode'));
    }
    const printed = await claimsSurvivePrint(cdp);
    assert.ok(printed.length > 0 && printed.every(Boolean), JSON.stringify(printed));
  });

  await test('C2 G14: checked stanzas and the genuflection rubric render from the structure in Read, Missal and print', async () => {
    for (const [state, lang] of [[STATES.pentecost1962, 'la'], [STATES.pentecost1962English, 'en'],
      [STATES.pentecost1962Missal, 'la']]) {
      await navigateCandidate(cdp, base, state);
      const label = 'Day 1962 Pentecost ' + await evaluate(cdp, 'dayReaderDebug.mode') + ' ' + lang;
      assertTextStructure(await textStructureAudit(cdp, 'roman-1962', 'pentecost'), lang, label);
    }
    await cdp.send('Emulation.setEmulatedMedia', { media: 'print' });
    try {
      const printed = await evaluate(cdp, `(() => {
        const group = document.querySelector('#reader-document .composed-stanzas');
        return {
          stanzas: [...group.querySelectorAll(':scope > .stanza')].map(node =>
            node.getClientRects().length > 0 && getComputedStyle(node).breakInside === 'avoid'),
          section: getComputedStyle(group.closest('section.proper')).breakInside,
          rubric: getComputedStyle(document.querySelector('#reader-document .inline-rubric')).fontStyle
        };
      })()`);
      assert.ok(printed.stanzas.length > 1 && printed.stanzas.every(Boolean), JSON.stringify(printed));
      assert.equal(printed.section, 'auto', 'a Sequence paginates by strophe');
      assert.equal(printed.rubric, 'italic');
    } finally {
      await cdp.send('Emulation.setEmulatedMedia', { media: '' });
    }
  });

  await test('C2 G14: copying a Proper keeps its ℣ and words, a printed rubric and stanza breaks, and no hidden label', async () => {
    const before = await evaluate(cdp, '({ width: innerWidth, height: innerHeight })');
    await viewport(cdp, 1440, 900);
    await cdp.send('Browser.grantPermissions', {
      origin: base, permissions: ['clipboardReadWrite', 'clipboardSanitizedWrite']
    });
    await cdp.send('Emulation.setFocusEmulationEnabled', { enabled: true });
    try {
      for (const state of [STATES.pentecost1962, STATES.pentecost1962English]) {
        await navigateCandidate(cdp, base, state);
        await cdp.send('Page.bringToFront');
        for (const name of ['Introit', 'Alleluia', 'Sequence']) {
          const row = await copiedProper(cdp, name);
          assertCopied(row, 'Day ' + state + ' ' + name);
          if (name === 'Introit') assert.ok(row.verses > 0, 'Introit copy exercises verse numbers');
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

  await test('C2 G10: a missing translation leaves the held Latin original visible with its typed absence', async () => {
    await navigateCandidate(cdp, base, STATES.pentecost1962English);
    const rows = await unitAbsenceAudit(cdp, 'roman-1962');
    const missing = rows.filter(row => row.requested !== 'available');
    assert.ok(missing.some(row => row.la === 'available'), 'exemplar has a held Latin body without English: ' +
      JSON.stringify(rows));
    for (const row of rows) {
      if (row.requested === 'available') {
        assert.deepEqual(row.composed.map(one => one.lang), ['en'], JSON.stringify(row));
        assert.deepEqual(row.absences, [], JSON.stringify(row));
        continue;
      }
      assert.equal(row.absences.length, 1, JSON.stringify(row));
      assert.ok(row.absences[0].startsWith('en:' + row.requested), JSON.stringify(row));
      assert.match(row.notes[0], new RegExp('^English translation unavailable: ' + ABSENCE_WORDS[row.requested]));
      if (row.la === 'available') {
        assert.deepEqual(row.composed, [{ lang: 'la', original: 'la' }], JSON.stringify(row));
        assert.match(row.notes[0], /The Latin original is shown\.$/);
      } else {
        assert.deepEqual(row.composed, [], JSON.stringify(row));
        assert.ok(row.absences[0].endsWith(' la:' + row.la), JSON.stringify(row));
      }
    }
  });

  await test('C2 G11: pre-1955 Day states the inherited, uncollated recension caveat on screen, in Details and in print', async () => {
    await navigateCandidate(cdp, base, STATES.pentecostPre1955);
    const value = await evaluate(cdp, `(async () => {
      const structure = await window.Triptych.loadJSON('structure/propers/roman-pre-1955.json');
      const notice = document.querySelector('#coverage-notice');
      return {
        coverage: structure.recension_coverage,
        notice: notice.textContent, hidden: notice.hidden,
        notes: [...document.querySelectorAll('#reader-document .composed-note')].map(row => ({
          text: row.textContent.trim(), typed: row.dataset.unitAbsence || null }))
      };
    })()`);
    assert.ok(value.coverage && value.coverage.inheritance, 'pre-1955 structure carries recension coverage');
    assert.equal(value.hidden, false);
    assert.ok(value.notice.startsWith('This edition surface is a ' + value.coverage.status + ' finding aid'),
      value.notice);
    assert.match(value.notice, new RegExp('Proper wording coverage is ' + value.coverage.domains.propers.state + '\\.'));
    assert.match(value.notice, new RegExp('Inherited material from Missale Romanum, editio typica 1962 remains ' +
      value.coverage.inheritance.status + '\\.'));
    assert.ok(value.notes.length > 0);
    assert.ok(value.notes.every(row => row.text !== 'Latin text unavailable'), JSON.stringify(value.notes));
    assert.ok(value.notes.filter(row => /unavailable/.test(row.text)).every(row => row.typed), JSON.stringify(value.notes));
    await cdp.send('Emulation.setEmulatedMedia', { media: 'print' });
    try {
      assert.equal(await evaluate(cdp, `(() => {
        const notice = document.querySelector('#coverage-notice');
        return getComputedStyle(notice).display !== 'none' && notice.getClientRects().length > 0;
      })()`), true);
    } finally {
      await cdp.send('Emulation.setEmulatedMedia', { media: '' });
    }
    const details = await detailsText(cdp);
    assert.match(details, /RECENSION COVERAGE|Recension coverage/);
    assert.match(details, /Proper text source[\s\S]*Missale Romanum, editio typica 1962 · inherited/i);
    assert.match(details, /Inheritance basis/i);
    assert.match(details, /remains uncollated|remains inherited/);
  });

  await test('C2 G12: every absent Proper body states each typed reason', async () => {
    await navigateCandidate(cdp, base, STATES.pentecostPostDayEnglish);
    const rows = await unitAbsenceAudit(cdp, 'postconciliar');
    const empty = rows.filter(row => row.requested !== 'available' && row.la !== 'available');
    assert.ok(empty.length > 0, 'exemplar has a body held in neither language: ' + JSON.stringify(rows));
    for (const row of empty) {
      assert.deepEqual(row.absences, ['en:' + row.requested + ' la:' + row.la], JSON.stringify(row));
      assert.equal(row.notes[0], 'English translation unavailable: ' + ABSENCE_WORDS[row.requested] +
        (row.requested === 'not-publishable' ? ' (its use is rights restricted)' : '') +
        '. Latin text unavailable: ' + ABSENCE_WORDS[row.la] +
        (row.la === 'not-publishable' ? ' (its use is rights restricted)' : '') + '.');
    }
    assert.doesNotMatch(await evaluate(cdp, `document.querySelector('#reader-document').innerText`),
      /No English or Latin body is held here/);
  });

  await test('C2 G13: Details reports the explicitly selected formulary and form, and only what remains open', async () => {
    await navigateCandidate(cdp, base, STATES.pentecostPostDayEnglish);
    const value = await evaluate(cdp, `(async () => {
      const structure = await window.Triptych.loadJSON('structure/propers/postconciliar.json');
      const mass = structure.masses.find(row => row.key === 'pentecost');
      return { outcome: dayReaderDebug.outcome, name: mass.name,
        form: (mass.forms || []).find(row => row.id === 'day').name,
        choices: dayReaderDebug.semantic.unresolvedChoices.map(row => row.id) };
    })()`);
    assert.equal(value.outcome, 'unresolved');
    assert.deepEqual(value.choices, ['proper-choice/postconciliar/pentecost/day/entrance-antiphon']);
    const details = await detailsText(cdp);
    assert.doesNotMatch(details, /no formulary outcome has been selected/i);
    assert.ok(details.includes('Selected formulary: ' + value.name + '; form: ' + value.form + '.'), details);
    assert.match(details, /Still to be chosen: Source Proper choice: Entrance Antiphon \(Spiritus Domini or Caritas Dei\)\. No option is selected silently\./);
    assert.match(details, /Pentecost Sunday/);
  });

  await test('C2 G17: Read and Missal Contents jumps write a stable semantic location that a fresh load restores', async () => {
    for (const [state, mode] of [[STATES.pentecost1962, 'read'], [STATES.pentecost1962Missal, 'missal']]) {
      await navigateCandidate(cdp, base, state);
      const before = await evaluate(cdp, '({ hash: location.hash, length: history.length })');
      assert.equal(new URLSearchParams(before.hash.slice(1)).has('location'), false);
      await click(cdp, '[data-reader-action="contents"]');
      const target = await evaluate(cdp, `(() => {
        const rows = [...document.querySelectorAll('[data-reader-contents] [data-reader-location]')]
          .filter(row => /^proper\\//.test(row.dataset.readerLocation));
        const row = rows[Math.min(4, rows.length - 1)];
        row.click();
        return row.dataset.readerLocation;
      })()`);
      await waitForVisualSettlement(cdp, { semanticEventId: target });
      const after = await evaluate(cdp, `({ hash: location.hash, length: history.length,
        state: history.state && history.state.dayReaderLocation,
        debug: dayReaderDebug.state.semanticLocation,
        focus: document.activeElement.dataset.semanticEventId || null })`);
      const params = new URLSearchParams(after.hash.slice(1));
      assert.equal(params.get('location'), target, mode + ' ' + after.hash);
      assert.equal(params.get('mode'), mode);
      assert.equal(after.length, before.length, mode + ' jump replaces rather than adds history');
      assert.deepEqual(after.state, { kind: 'event', id: target });
      assert.deepEqual(after.debug, { eventId: target });
      assert.equal(after.focus, target);
      await navigateCandidate(cdp, base, after.hash);
      const restored = await evaluate(cdp, `(() => {
        const node = document.querySelector('[data-semantic-event-id="${target}"]');
        const box = node.getBoundingClientRect();
        return { outcome: dayReaderDebug.outcome, error: dayReaderDebug.error,
          location: new URLSearchParams(location.hash.slice(1)).get('location'),
          visible: box.bottom > 0 && box.top < innerHeight };
      })()`);
      assert.equal(restored.outcome, 'ready', JSON.stringify(restored));
      assert.equal(restored.location, target);
      assert.equal(restored.visible, true, JSON.stringify(restored));
    }
  });

  await test('deep Missal locus and Contents map share current semantic ownership', async () => {
    await navigateCandidate(cdp, base, STATES.romanMissal);
    await evaluate(cdp, `(async () => {
      const nodes = [...document.querySelectorAll('[data-reader-locus-major]')];
      const canon = nodes.filter(node => /Canon/i.test(node.dataset.readerLocusMajor));
      const start = Math.min(...canon.map(node => node.getBoundingClientRect().top + scrollY));
      const end = Math.max(...canon.map(node => node.getBoundingClientRect().bottom + scrollY));
      for (let y = start + 120; y < end - 120; y += 80) {
        scrollTo({ top: y, behavior: 'instant' });
        await new Promise(resolve => requestAnimationFrame(() => requestAnimationFrame(resolve)));
        const locus = document.querySelector('[data-reader-locus]');
        if (locus && !locus.hidden && /Canon/i.test(locus.textContent)) return y;
      }
      throw new Error('no stable visible Canon locus inside the Canon range');
    })()`);
    await waitFor(cdp,
      `/Canon/i.test(document.querySelector('[data-reader-locus]')?.textContent || '') && document.querySelector('[data-reader-locus]')?.hidden === false`,
      'persistent Canon locus');
    const locus = await evaluate(cdp, `({
      text: document.querySelector('[data-reader-locus]').textContent.trim(),
      current: document.querySelector('[data-reader-contents] [aria-current="location"]')?.dataset.readerLocation,
      count: document.querySelectorAll('[data-reader-locus]').length
    })`);
    assert.equal(locus.count, 1);
    assert.match(locus.text, /Canon/i);
    assert.equal(locus.current, 'ordinary-section/canon');

    await click(cdp, '[data-reader-action="contents"]');
    const map = await evaluate(cdp, `(() => {
      const row = document.querySelector('[data-reader-contents] [aria-current="location"]');
      const surface = document.querySelector('[data-reader-contents]').closest('.surface-body');
      const r = row.getBoundingClientRect();
      const s = surface.getBoundingClientRect();
      return { current: row.dataset.readerLocation, rowCenter: (r.top + r.bottom) / 2,
        surfaceCenter: (s.top + s.bottom) / 2, visible: r.bottom > s.top && r.top < s.bottom,
        scrollTop: surface.scrollTop, scrollMax: surface.scrollHeight - surface.clientHeight,
        focus: document.activeElement.getAttribute('aria-label') };
    })()`);
    assert.equal(map.current, 'ordinary-section/canon');
    assert.equal(map.visible, true);
    assert.ok(Math.abs(map.rowCenter - map.surfaceCenter) <= 70 ||
      map.scrollTop >= map.scrollMax - 1, JSON.stringify(map));
    assert.equal(map.focus, 'Close Contents');
    await escape(cdp);
    assert.match(await evaluate(cdp,
      `document.querySelector('[data-reader-locus]').textContent.trim()`), /Canon/i);
  });

  await test('Read, Missal, Study and Compare controls keep Details lazy and human-facing', async () => {
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
      { name: 'Study', disabled: false, checked: 'false' },
      { name: 'Compare', disabled: false, checked: 'false' }
    ]);
    await escape(cdp);
    await openSurface(cdp, 'details');
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
    await openSurface(cdp, 'details');
    const missalDetails = await evaluate(cdp,
      `document.querySelector('[data-reader-details]').innerText`);
    assert.match(missalDetails, /Mode\s+Missal/i);
    assert.match(missalDetails, /Ordinary language\s+English/i);
    assert.match(missalDetails, /Eucharistic Prayer: II/);
    assert.match(missalDetails, /Ordinary elements have unresolved applicability/i);
    assert.doesNotMatch(missalDetails, /territorial results|branch-local formulary choice/i);
    assert.doesNotMatch(missalDetails, /proper\/|ordinary-element\/|sourceHooks|ordinal|\{.*\}/i);
  });

  await test('Details presents the counterpart first and preserves the accepted legacy destinations', async () => {
    await navigateCandidate(cdp, base, STATES.roman);
    await openSurface(cdp, 'details');
    const links = await evaluate(cdp, `[...document.querySelectorAll('[data-reader-details] a')]
      .map(row => ({ label: row.textContent.trim(), pathname: new URL(row.href).pathname }))`);
    assert.deepEqual(links.map(row => row.label), [
      'Browse the Propers', 'The Code, Canon by Canon', 'Every Document'
    ]);
    assert.match(links[0].pathname, /\/liturgy\/index\.html$/);
    assert.match(links[1].pathname, /\/law\/$/);
    assert.match(links[2].pathname, /\/texts\/$/);
    assert.deepEqual(await evaluate(cdp,
      `[...document.querySelectorAll('[data-reader-details] .details-section > h3')]
        .map(row => row.textContent.trim())`), [
      'Selection', 'Resolved Day result', 'Related reader', 'Elsewhere in Triptych'
    ]);
    assert.equal(await evaluate(cdp, `document.querySelectorAll('.reader-actions [data-reader-action]').length`), 4);
    await escape(cdp);
  });

  await test('territorial history selects an Epiphany form without substituting the other branch', async () => {
    await viewport(cdp, 393, 852);
    await navigateCandidate(cdp, base, STATES.territorialEpiphany);
    const semanticLocation = await evaluate(cdp,
      `document.querySelectorAll('section.territorial-branch')[0]
        .querySelector('[data-semantic-location]').dataset.semanticLocation`);
    assert.match(semanticLocation, /^territory\/epiphany-january-6\//);
    await evaluate(cdp,
      `document.querySelector('[data-semantic-location="${semanticLocation}"]').scrollIntoView({block:'start'})`);
    await waitForVisualSettlement(cdp);
    const before = await evaluate(cdp, 'dayReaderDebug.renders');
    await evaluate(cdp, `(() => {
      const form = document.querySelector(
        'section[data-territorial-branch="epiphany-transferred-to-sunday"] .proper-form-choice form');
      const day = form.querySelector('input[value="day"]');
      day.click();
      form.requestSubmit();
    })()`);
    let selectedHash = updatedHash(STATES.territorialEpiphany, 'mass', 'epiphany');
    selectedHash = updatedHash(selectedHash, 'form', 'day');
    await waitForCommittedRender(cdp, before, selectedHash, 'territorial Epiphany day selection');
    assert.equal(await evaluate(cdp, 'dayReaderDebug.outcome'), 'ready');
    assert.equal(await evaluate(cdp,
      `document.querySelectorAll('section.territorial-branch').length`), 2);
    const selected = await evaluate(cdp, `(() => {
      const row = document.querySelector(
        'section[data-territorial-branch="epiphany-january-6"]');
      const held = document.querySelector(
        'section[data-territorial-branch="epiphany-transferred-to-sunday"]');
      return {
        rejectedLocations: row.querySelectorAll('[data-semantic-location]').length,
        failure: row.querySelector('.candidate-failure')?.textContent || '',
        heldLocations: held.querySelectorAll('[data-semantic-location]').length,
        heldChoices: held.querySelectorAll('.proper-form-choice').length
      };
    })()`);
    assert.equal(selected.rejectedLocations, 0);
    assert.match(selected.failure, /requested readable formulary is not held on this Day branch/);
    assert.match(selected.failure, /No locality, formulary, or liturgical text was substituted/);
    assert.ok(selected.heldLocations > 0);
    assert.equal(selected.heldChoices, 0);
    await historyMove(cdp, 'back', STATES.territorialEpiphany);
    assert.equal(await evaluate(cdp, 'dayReaderDebug.state.requestedMode'), 'read');
    assert.equal(await evaluate(cdp,
      `document.querySelector('[data-semantic-location="${semanticLocation}"]') !== null`), true);
    assert.equal(await evaluate(cdp,
      `document.querySelectorAll('.proper-form-choice').length`), 1);
    await historyMove(cdp, 'forward', selectedHash);
    assert.equal(await evaluate(cdp, 'dayReaderDebug.state.form'), 'day');
    assert.match(await evaluate(cdp, `document.querySelector(
      'section[data-territorial-branch="epiphany-january-6"] .candidate-failure').textContent`),
      /requested readable formulary is not held on this Day branch.*No locality, formulary, or liturgical text was substituted/s);
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
    let missalHash = updatedHash(canonicalDayHash(STATES.postReadLatent), 'mode', 'missal');
    missalHash = updatedHash(missalHash, 'location', properId);
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
    assert.match(missal.hash, /mode=missal/);
    assert.doesNotMatch(missal.hash, /(?:^|&)ordinary=/);
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
    const readProperId = 'proper/postconciliar/advent-1/008';
    let readHash = updatedHash(canonicalDayHash(STATES.postReadLatent), 'mode', 'read');
    readHash = updatedHash(readHash, 'location', readProperId);
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
    assert.match(read.hash, /mode=read/);
    assert.doesNotMatch(read.hash, /(?:^|&)ordinary=/);
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
    const semanticId = (option) => option === 'ep-i'
      ? 'ordinary-element/prex-eucharistica/te-igitur'
      : 'ordinary-element/prex-eucharistica/prex-eucharistica-' + option.replace(/^ep-/, '');
    const focusOf = (option) => ({
      group: 'eucharistic-prayer', option, legend: 'Eucharistic Prayer'
    });
    let currentOption = 'ep-ii';
    await evaluate(cdp, `document.querySelector('[data-semantic-event-id="${semanticId(currentOption)}"]').scrollIntoView({block: 'start'})`);
    await waitForVisualSettlement(cdp, { semanticEventId: semanticId(currentOption) });
    await evaluate(cdp, `(() => {
      const radio = document.querySelector(
        '[data-option-group="eucharistic-prayer"] input:checked');
      radio.focus({preventScroll: true});
      radio.closest('[data-option-group]').scrollIntoView({block: 'start', behavior: 'auto'});
    })()`);
    let settled = await waitForVisualSettlement(cdp, {
      semanticEventId: semanticId(currentOption), focus: focusOf(currentOption)
    });
    assert.equal(settled.activeElement.value, 'ep-ii');
    assert.equal(settled.targetIntersectsViewport, true);
    assert.equal(settled.activeElementIntersectsViewport, true);
    let currentHash = canonicalDayHash(STATES.postMissal);
    for (const option of ['ep-i', 'ep-iii', 'ep-iv', 'ep-ii']) {
      const previousOption = currentOption;
      const targetId = option === 'ep-iv'
        ? 'ordinary-section/prex-eucharistica' : semanticId(option);
      const before = await evaluate(cdp, 'dayReaderDebug.renders');
      const presentationsBefore = await evaluate(cdp, 'dayReaderDebug.ordinaryPresentations');
      const beforeTop = settled.targetRect.top;
      await evaluate(cdp,
        `document.querySelector('[data-option-group="eucharistic-prayer"] input[value="${option}"]').focus({preventScroll: true})`);
      await pressSpace(cdp);
      currentHash = updatedHash(currentHash, 'eucharistic-prayer', option);
      currentHash = updatedHash(currentHash, 'location', targetId);
      settled = await waitForCommittedRender(cdp, before, currentHash, 'keyboard EP ' + option, {
        semanticEventId: targetId, focus: focusOf(option)
      });
      const restored = await evaluate(cdp, `(() => {
        const active = document.activeElement;
        const fieldset = active.closest('fieldset');
        const ids = [...document.querySelectorAll('[data-semantic-event-id]')]
          .map(row => row.dataset.semanticEventId);
        const epOneKeys = new Set([
          'te-igitur', 'memento-domine', 'communicantes', 'hanc-igitur',
          'quam-oblationem', 'qui-pridie', 'unde-et-memores', 'supra-quae',
          'supplices', 'memento-etiam', 'nobis-quoque', 'per-quem'
        ]);
        return {
          activeType: active.type,
          activeValue: active.value,
          checked: active.checked,
          legend: fieldset && fieldset.querySelector('legend').textContent,
          group: fieldset && fieldset.dataset.optionGroup,
          hash: location.hash,
          semanticTop: document.querySelector('[data-semantic-event-id="${targetId}"]').getBoundingClientRect().top,
          pending: dayReaderDebug.pendingNavigation,
          presentations: dayReaderDebug.ordinaryPresentations,
          uniqueEvents: new Set(ids).size === ids.length,
          epEvents: ids.filter(id => /prex-eucharistica-(i|ii|iii|iv)$/.test(id) ||
            epOneKeys.has(id.split('/').at(-1))),
          canonEvents: ids.filter(id => {
            if (!id.startsWith('ordinary-element/prex-eucharistica/')) return false;
            const key = id.split('/').at(-1);
            return epOneKeys.has(key) || key === 'mysterium-fidei' || key === 'doxologia' ||
              /prex-eucharistica-(i|ii|iii|iv)$/.test(key);
          })
        };
      })()`);
      assert.equal(restored.activeType, 'radio');
      assert.equal(restored.activeValue, option);
      assert.equal(restored.checked, true);
      assert.equal(restored.legend, 'Eucharistic Prayer');
      assert.equal(restored.group, 'eucharistic-prayer');
      assert.equal(restored.hash, canonicalDayHash(currentHash));
      assert.equal(settled.targetIntersectsViewport, true);
      assert.equal(settled.activeElementIntersectsViewport, true);
      assert.ok(settled.stableFramesObserved >= 5);
      if (option !== 'ep-iv' && previousOption !== 'ep-iv') assert.ok(
        Math.abs(restored.semanticTop - beforeTop) <= 4,
        `${option} semantic delta: ${restored.semanticTop - beforeTop}`);
      assert.equal(restored.pending, null);
      assert.equal(restored.presentations, presentationsBefore + 1);
      assert.equal(restored.uniqueEvents, true);
      assert.equal(restored.epEvents.length, option === 'ep-i' ? 12 : option === 'ep-iv' ? 0 : 1);
      if (option === 'ep-i') assert.deepEqual(restored.canonEvents, [
        'ordinary-element/prex-eucharistica/te-igitur',
        'ordinary-element/prex-eucharistica/memento-domine',
        'ordinary-element/prex-eucharistica/communicantes',
        'ordinary-element/prex-eucharistica/hanc-igitur',
        'ordinary-element/prex-eucharistica/quam-oblationem',
        'ordinary-element/prex-eucharistica/qui-pridie',
        'ordinary-element/prex-eucharistica/mysterium-fidei',
        'ordinary-element/prex-eucharistica/unde-et-memores',
        'ordinary-element/prex-eucharistica/supra-quae',
        'ordinary-element/prex-eucharistica/supplices',
        'ordinary-element/prex-eucharistica/memento-etiam',
        'ordinary-element/prex-eucharistica/nobis-quoque',
        'ordinary-element/prex-eucharistica/per-quem',
        'ordinary-element/prex-eucharistica/doxologia'
      ]);
      else if (option === 'ep-iv') assert.deepEqual(restored.canonEvents, [
        'ordinary-element/prex-eucharistica/mysterium-fidei',
        'ordinary-element/prex-eucharistica/doxologia'
      ]);
      else assert.deepEqual(restored.canonEvents, [
        semanticId(option),
        'ordinary-element/prex-eucharistica/mysterium-fidei',
        'ordinary-element/prex-eucharistica/doxologia'
      ]);
      currentOption = option;
    }

    await cdp.send('Emulation.setEmulatedMedia', {
      media: 'screen', features: [{ name: 'prefers-reduced-motion', value: 'reduce' }]
    });
    const reducedBeforeTop = settled.targetRect.top;
    const reducedGeneration = await evaluate(cdp, 'dayReaderDebug.renders');
    await evaluate(cdp,
      `document.querySelector('[data-option-group="eucharistic-prayer"] input[value="ep-iii"]').focus({preventScroll: true})`);
    await pressSpace(cdp);
    let reducedHash = updatedHash(currentHash, 'eucharistic-prayer', 'ep-iii');
    reducedHash = updatedHash(reducedHash, 'location', semanticId('ep-iii'));
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
        await openSurface(cdp, name);
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
      await openSurface(cdp, name);
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
      names: [...document.querySelectorAll('#reader-document .proper-name')].map(row => row.childNodes[0].textContent.trim())
    })`);
    assert.equal(candidate.title, current.title);
    assert.deepEqual(candidate.names, current.names);
    assert.equal(await evaluate(cdp, 'document.querySelectorAll("[data-reader-shell]").length'), 1);
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
        ordinary: [...document.querySelectorAll('#reader-document .ordinary-element')]
          .map(row => row.textContent.replace(/\s+/g, ' ').trim()),
        propers: [...document.querySelectorAll('#reader-document .proper:not(.ordinary-element)')]
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

  await test('each verified dialogue turn exposes one visible, announced, and copied cue', async () => {
    // C4, first step: the 1962 Confiteor and Suscipiat and the postconciliar
    // Orate fratres. Structured turns once set a generated cue beside the
    // book's printed P./R., and Orate fratres needed an event-specific rule
    // to hide its response glyph. Visible cues, the accessibility tree and the
    // real clipboard are measured here because CSS-generated content and
    // fake-DOM parity cannot prove any of the three.
    await viewport(cdp, 1440, 900);
    await cdp.send('Browser.grantPermissions', {
      origin: base, permissions: ['clipboardReadWrite', 'clipboardSanitizedWrite']
    });
    await cdp.send('Emulation.setFocusEmulationEnabled', { enabled: true });
    try {
      const cases = [
        [STATES.romanMissal, 'en', [
          ['praeparatio/confiteor-sacerdotis', [['P', 'Priest', null, 'I CONFESS to almighty God, to blessed Mary']]],
          ['praeparatio/confiteor-ministrorum', [['S', 'Server', null, 'I CONFESS to almighty God, to blessed Mary']]],
          // The checked printed R. supplies its sign, without supplying an
          // actor or a structured target role.
          ['oblatio/suscipiat-dominus', [['℟', 'Response', 'R.', 'MAY the Lord receive this sacrifice']]],
          ['conclusio/deo-gratias', [['℟', 'Response — Server', 'R.', 'Thanks be to God.']]]
        ]],
        [STATES.romanLatinMissal, 'la', [
          ['praeparatio/confiteor-sacerdotis', [['P', 'Priest', 'P.', 'Confiteor Deo omnipotenti, &c.']]],
          ['praeparatio/confiteor-ministrorum', [['℟', 'Response — Server', 'R.', 'Confiteor Deo omnipotenti, beatæ Mariæ']]],
          ['oblatio/suscipiat-dominus', [['℟', 'Response — Server', 'R.', 'Suscipiat Dominus sacrificium']]],
          ['conclusio/deo-gratias', [['℟', 'Response — Server', 'R.', 'Deo gratias.']]]
        ]],
        // Speakers only since 2026-10-19 (C4): the 2002 Ordo n. 29 (artifact
        // p. 310) prints rubrics naming the priest and the people and no
        // versicle or response mark, so the unsupported target roles were
        // withdrawn. The antecedent's checked printed R. still sets as ℟.
        [STATES.postLatinMissal, 'la', [
          ['praeparatio-donorum/orate-fratres', [
            ['P', 'Priest', null, 'Orate Fratres: ut meum ac vestrum'],
            ['℟', 'Response — All', 'R.', 'Suscipiat Dominus sacrificium de manibus tuis']
          ]]
        ]]
      ];
      for (const [state, lang, events] of cases) {
        const calendar = new URLSearchParams(state.slice(1)).get('missal');
        const file = JSON.parse(await readFile(
          resolve(ROOT, 'src/web/data/structure/ordinary', calendar + '.json'), 'utf8'));
        const sourceElements = new Map(file.sections.flatMap(section =>
          section.elements.map(element => [element.key, element])));
        await navigateCandidate(cdp, base, state);
        for (const [key, expected] of events) {
          const eventId = 'ordinary-element/' + key;
          const sourceRows = sourceElements.get(key).translations.find(row => row.lang === lang).turns;
          assert.equal(sourceRows.length, expected.length, eventId + ' exact selected-source turn extent');
          const observed = await evaluate(cdp, `(async () => {
            const event = [...document.querySelectorAll('[data-semantic-event-id]')]
              .find((node) => node.dataset.semanticEventId === ${JSON.stringify(eventId)});
            if (!event) return null;
            event.scrollIntoView({ block: 'center' });
            const rows = [...event.querySelectorAll('.ordinary-turn')];
            const turns = rows.map((row, index) => {
              row.setAttribute('data-cue-probe', String(index));
              const generated = [...row.querySelectorAll('.cue-mark')]
                .map((mark) => getComputedStyle(mark, '::before').content)
                .filter((content) => content && content !== 'none' && content !== 'normal');
              const words = row.querySelector('.ordinary-turn-text');
              const label = row.querySelector('.speaker-tag .visually-hidden');
              const selection = getSelection();
              selection.removeAllRanges();
              const range = document.createRange();
              range.selectNodeContents(row);
              selection.addRange(range);
              const selected = selection.toString();
              selection.removeAllRanges();
              return {
                generated: generated.map((content) => content.replace(/^"|"$/g, '')),
                cueLang: row.querySelector('.speaker-tag')?.lang || null,
                cueHidden: [...row.querySelectorAll('.cue-mark')]
                  .map((mark) => mark.getAttribute('aria-hidden')),
                label: label ? label.textContent : null,
                printedMarker: row.dataset.printedMarker || null,
                speaker: row.dataset.speaker || null,
                dialogueRole: row.dataset.dialogueRole || null,
                wordsLang: words ? words.lang : null,
                words: words ? words.textContent : null,
                selected
              };
            });
            const body = event.querySelector('.ordinary-dialogue');
            const selection = getSelection();
            selection.removeAllRanges();
            const range = document.createRange();
            range.selectNodeContents(body);
            selection.addRange(range);
            const copiedOk = document.execCommand('copy');
            selection.removeAllRanges();
            let copied = null;
            try { copied = await navigator.clipboard.readText(); } catch (error) { copied = 'ERROR ' + error; }
            return { turns, copiedOk, copied };
          })()`);
          assert.ok(observed, 'rendered ' + eventId);
          assert.equal(observed.turns.length, expected.length, eventId + ' turn count');

          // The accessibility tree: one cue name per row and spoken words
          // without a printed letter or a decorative glyph beside them.
          const { nodes } = await cdp.send('Accessibility.getFullAXTree');
          const byId = new Map(nodes.map((node) => [node.nodeId, node]));
          const { root } = await cdp.send('DOM.getDocument', { depth: 0 });
          const announced = [];
          for (let index = 0; index < expected.length; index += 1) {
            const { nodeId } = await cdp.send('DOM.querySelector', {
              nodeId: root.nodeId,
              selector: `[data-semantic-event-id="${eventId}"] [data-cue-probe="${index}"]`
            });
            const { node } = await cdp.send('DOM.describeNode', { nodeId });
            const start = nodes.find((one) => one.backendDOMNodeId === node.backendNodeId);
            assert.ok(start, eventId + ' turn ' + index + ' is in the accessibility tree');
            const names = [];
            (function walk(one) {
              if (!one.ignored && one.role?.value === 'StaticText') {
                names.push(one.name?.value || '');
                return;
              }
              for (const child of one.childIds || []) {
                const next = byId.get(child);
                if (next) walk(next);
              }
            })(start);
            announced.push(names);
          }

          observed.turns.forEach((turn, index) => {
            const [glyph, label, marker, opening] = expected[index];
            const where = `${eventId} ${lang} turn ${index}`;
            assert.deepEqual(turn.generated, glyph ? [glyph] : [], where + ' source-qualified cue');
            assert.deepEqual(turn.cueHidden, glyph ? ['true'] : [], where + ' hides the decorative glyph');
            assert.equal(turn.label, label, where + ' accessible cue');
            assert.equal(turn.cueLang, glyph ? 'en' : null, where + ' cue language');
            assert.equal(turn.wordsLang, lang, where + ' spoken language');
            assert.equal(turn.printedMarker, marker, where + ' separated printed marker');
            assert.equal(turn.speaker, sourceRows[index].speaker || null, where + ' source actor is preserved');
            assert.equal(turn.dialogueRole, sourceRows[index].dialogue_role || null, where + ' printed sign adds no target role');
            assert.equal((marker ? marker + ' ' : '') + turn.words, sourceRows[index].text,
              where + ' reconstructs the exact selected-source row');
            assert.ok(turn.words.startsWith(opening), where + ' spoken words: ' + turn.words);
            if (glyph) assert.doesNotMatch(turn.words, /^(?:[PRVS]\.|[℣℟])/, where + ' no duplicate printed cue');
            assert.deepEqual(announced[index], label ? [label, turn.words] : [turn.words], where + ' announcement');
            assert.equal(announced[index].join(' ').match(/[℣℟]/g), null, where + ' glyph silent');
            assert.equal(turn.selected.replace(/\s+/g, ' ').trim(), (label ? label + ' ' : '') + turn.words,
              where + ' selected text');
          });
          assert.equal(observed.copiedOk, true, eventId + ' copy command');
          assert.equal(
            observed.copied.replace(/\s+/g, ' ').trim(),
            observed.turns.map((turn) => (turn.label ? turn.label + ' ' : '') + turn.words).join(' '),
            eventId + ' copied text holds one cue per turn'
          );
        }
      }

      // The opening-cue regression for an opaque `all` element ran here on the
      // postconciliar Preface dialogue and Pax. Since C4 step 2 (2026-10-19)
      // both are reviewed per-turn rows, checked in c4Step2DialogueTurns; the
      // opaque path itself stays covered by test_mass_ordinary's fixture.
    } finally {
      await cdp.send('Emulation.setFocusEmulationEnabled', { enabled: false });
      await cdp.send('Browser.resetPermissions', {});
      // Later assertions inherit the viewport the preceding test set.
      await viewport(cdp, 1024, 768);
    }
  });

  await c4Step2DialogueTurns(cdp, base);

  await test('C4 dialogue glyphs keep readable red structure at 320px, 400-percent text and in print', async () => {
    // This short, source-divided exchange carries both printed roles. The
    // earlier C4 checks cover its accessible names and real clipboard copy;
    // here the actual CSS boxes and generated glyphs must also survive reflow.
    try {
      for (const [name, width, height, textSize, media] of [
        ['320px', 320, 852, '', 'screen'],
        ['400-percent', 1280, 900, '400%', 'screen'],
        ['print', 1024, 768, '', 'print']
      ]) {
        await viewport(cdp, width, height);
        await navigateCandidate(cdp, base, STATES.romanMissal);
        if (textSize) await evaluate(cdp,
          `document.documentElement.style.fontSize = ${JSON.stringify(textSize)}`);
        await cdp.send('Emulation.setEmulatedMedia', { media });
        const measured = await evaluate(cdp, `(() => {
          const event = document.querySelector(
            '[data-semantic-event-id="ordinary-element/praeparatio/adjutorium-nostrum"]');
          event.scrollIntoView({ behavior: 'instant', block: 'center' });
          const eventBox = event.getBoundingClientRect();
          const colorProbe = document.createElement('span');
          colorProbe.style.color = 'var(--instrument-accent)';
          event.appendChild(colorProbe);
          const accent = getComputedStyle(colorProbe).color;
          colorProbe.remove();
          return {
            accent,
            overflow: document.documentElement.scrollWidth - document.documentElement.clientWidth,
            eventBox: { top: eventBox.top, bottom: eventBox.bottom },
            viewportHeight: innerHeight,
            rows: [...event.querySelectorAll('.ordinary-turn[data-dialogue-role]')].map((row) => {
              const cue = row.querySelector('.ordinary-turn-cue');
              const mark = cue.querySelector('.cue-mark');
              const words = row.querySelector('.ordinary-turn-text');
              const cueBox = cue.getBoundingClientRect();
              const wordsBox = words.getBoundingClientRect();
              const rowBox = row.getBoundingClientRect();
              const style = getComputedStyle(mark);
              return {
                role: row.dataset.dialogueRole,
                markCount: row.querySelectorAll('.cue-mark').length,
                glyph: getComputedStyle(mark, '::before').content.replace(/^"|"$/g, ''),
                hidden: mark.getAttribute('aria-hidden'),
                markText: mark.textContent,
                color: style.color,
                fontFamily: style.fontFamily,
                fontSize: parseFloat(style.fontSize),
                wordsSize: parseFloat(getComputedStyle(words).fontSize),
                cueBox: { left: cueBox.left, right: cueBox.right, bottom: cueBox.bottom },
                wordsBox: { left: wordsBox.left, right: wordsBox.right },
                rowBox: { left: rowBox.left, right: rowBox.right, bottom: rowBox.bottom }
              };
            })
          };
        })()`);
        assert.equal(measured.overflow <= 1, true, `${name} page overflow ${measured.overflow}px`);
        assert.ok(measured.eventBox.bottom > 0 && measured.eventBox.top < measured.viewportHeight,
          `${name} dialogue visible in viewport`);
        assert.deepEqual(measured.rows.map((row) => row.role), ['versicle', 'response'],
          `${name} source roles`);
        measured.rows.forEach((row, index) => {
          const where = `${name} turn ${index}`;
          assert.equal(row.markCount, 1, where + ' one visible mark');
          assert.equal(row.glyph, index ? '℟' : '℣', where + ' role glyph');
          assert.equal(row.hidden, 'true', where + ' decorative mark silent');
          assert.equal(row.markText, '', where + ' generated mark stays out of copy');
          assert.equal(row.color, measured.accent, where + ' rubric red');
          assert.match(row.fontFamily, /Noto Sans Symbols 2.*Segoe UI Symbol.*DejaVu Sans/,
            where + ' symbol font fallback');
          assert.ok(row.fontSize >= row.wordsSize * 0.9, where + ' near body size');
          assert.ok(row.cueBox.left >= row.rowBox.left - 1, where + ' cue inside row');
          assert.ok(row.cueBox.right <= row.wordsBox.left + 1, where + ' cue clear of words');
          assert.ok(row.cueBox.bottom <= row.rowBox.bottom + 1, where + ' cue fits row');
          assert.ok(row.wordsBox.right <= row.rowBox.right + 1, where + ' words fit row');
        });
        if (captureDir && media === 'screen') {
          await mkdir(captureDir, { recursive: true });
          await shot(cdp, join(captureDir, `c4-dialogue-glyph-${name}.png`));
        }
      }
    } finally {
      await cdp.send('Emulation.setEmulatedMedia', { media: 'screen' });
      await evaluate(cdp, `document.documentElement.style.fontSize = ''`);
      await viewport(cdp, 1024, 768);
    }
  });

  if (!SOURCE_ONLY) await test(
    'normal preview build contains a noindex candidate but no candidate navigation link', async () => {
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
    }
  );

  await test('the retained Day route is statically noindex and visible copy is route-neutral', async () => {
    const source = await readFile(join(ROOT, 'src/web/browser/liturgy/day-reader.html'), 'utf8');
    assert.match(source,
      /<meta name="robots" content="noindex, nofollow, noarchive, nosnippet, noimageindex">/);
    assert.doesNotMatch(source, /<link[^>]+rel=["']canonical["']|property=["']og:url["']/i);
    await navigateCandidate(cdp, base, STATES.roman);
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

  await test('print removes shell chrome while retaining identity and context', async () => {
    await navigateCandidate(cdp, base);
    await cdp.send('Emulation.setEmulatedMedia', { media: 'print' });
    const value = await evaluate(cdp, `({
      actions: getComputedStyle(document.querySelector('.reader-actions')).display,
      routeMarker: document.querySelector('.candidate-flag'),
      title: document.querySelector('#celebration-title').textContent,
      meta: document.querySelector('#celebration-meta').textContent,
      properCount: document.querySelectorAll('#reader-document .proper').length
    })`);
    assert.equal(value.actions, 'none');
    assert.equal(value.routeMarker, null);
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
    assert.equal(missal.ordinary, 41);
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
  } else if (kind === 'why') {
    await click(cdp, 'details.day-reasoning summary');
  } else if (['date', 'contents', 'mode', 'details'].includes(kind)) {
    await openSurface(cdp, kind);
  }
  const settlement = await waitForVisualSettlement(cdp);
  return { ...navigation, settlement };
}

async function captureC2Exemplar(cdp, base, directory) {
  await mkdir(directory, { recursive: true });
  const evidence = [];
  const states = [
    ['read-latin', STATES.pentecost1962],
    ['read-english', STATES.pentecost1962English],
    ['missal-latin', STATES.pentecost1962Missal]
  ];
  for (const [width, height] of [[1440, 900], [393, 852], [320, 852]]) {
    await viewport(cdp, width, height);
    for (const [name, state] of states) {
      const navigation = await navigateCandidate(cdp, base, state);
      const overflow = await evaluate(cdp,
        'document.documentElement.scrollWidth - document.documentElement.clientWidth');
      assert.ok(overflow <= 1, `Pentecost ${name} ${width}x${height} overflows by ${overflow}px`);
      const file = `day--pentecost-1962-${name}--${width}x${height}.png`;
      await shot(cdp, join(directory, file));
      evidence.push(await captureEvidence(cdp, file, name, navigation.path,
        { settlement: navigation.settlement }));
    }
  }
  await viewport(cdp, 1024, 768);
  for (const [name, state] of [states[1], states[2]]) {
    const navigation = await navigateCandidate(cdp, base, state);
    await cdp.send('Emulation.setEmulatedMedia', { media: 'print' });
    try {
      const pdf = await cdp.send('Page.printToPDF', {
        printBackground: true, preferCSSPageSize: true,
        paperWidth: 8.5, paperHeight: 11,
        marginTop: 0.4, marginBottom: 0.4, marginLeft: 0.45, marginRight: 0.45
      });
      const file = `day--pentecost-1962-${name}--print.pdf`;
      await writeFile(join(directory, file), Buffer.from(pdf.data, 'base64'));
      evidence.push(await captureEvidence(cdp, file, name + '-print', navigation.path,
        { settlement: navigation.settlement }));
    } finally {
      await cdp.send('Emulation.setEmulatedMedia', { media: 'screen' });
    }
  }
  await writeFile(join(directory, 'c2-exemplar-evidence.json'),
    JSON.stringify(evidence, null, 2) + '\n');
  return evidence;
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
    ['partial-coverage', STATES.partial, 'top'], ['ash-before-frame', STATES.ashBeforeFrame, 'top'],
    ['why-apparatus', STATES.why, 'top'],
    ['territorial-epiphany', STATES.territorialEpiphany, 'top'],
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

  for (const [width, height] of [[1440, 900], [393, 852]]) {
    await viewport(cdp, width, height);
    for (const [name, state, kind] of [
      ['why-apparatus-open', STATES.why, 'why'],
      ['territorial-ascension', STATES.territorialAscension, 'top'],
      ['territorial-corpus-christi', STATES.territorialCorpus, 'top']
    ]) {
      const navigation = await captureCandidate(cdp, base, state, kind);
      const file = `day-reader-missal-${name}-${width}x${height}.png`;
      await shot(cdp, join(directory, file));
      measures.push({ file, viewport: `${width}x${height}`, state: name, metrics: await metrics(cdp) });
      evidence.push(await captureEvidence(cdp, file, name, navigation.path,
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
  await openSurface(cdp, 'details');
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
    ['invalid-ep', STATES.invalidPrayer], ['ash-before-frame', STATES.ashBeforeFrame],
    ['why-apparatus', STATES.why], ['territorial', STATES.territorialEpiphany],
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
    const radio = document.querySelector(
      '[data-option-group="eucharistic-prayer"] input:checked');
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
  await evaluate(cdp, `document.querySelector('[data-option-group="eucharistic-prayer"] input[value="ep-iii"]').focus({preventScroll: true})`);
  await pressSpace(cdp);
  const epAfterId = 'ordinary-element/prex-eucharistica/prex-eucharistica-iii';
  let epHash = updatedHash(STATES.postMissal, 'eucharistic-prayer', 'ep-iii');
  epHash = updatedHash(epHash, 'location', epAfterId);
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
  const profileRoot = resolve(process.env.TRIPTYCH_BROWSER_SCRATCH || join(ROOT, 'build'));
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
        target.type === 'page') || null;
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
      `performance.getEntriesByType('navigation')[0]?.name === ${JSON.stringify(bootstrapTarget)} && ` +
        `location.pathname === ${JSON.stringify(CURRENT)} && ` +
        `location.hash === ${JSON.stringify(canonicalDayHash(STATES.roman))} && ` +
        `window.dayReaderReady === true && ` +
        `window.dayReaderDebug.committedRender !== null && ` +
        `window.dayReaderDebug.committedRender.href === location.href`,
      'bootstrap document render');
    await waitForVisualSettlement(cdp);
    currentDocumentToken = await evaluate(cdp, 'dayReaderDebug.documentToken');

    await runAssertions(cdp, base);
    const sourceOnly = SOURCE_ONLY;
    const captures = captureDir ? (sourceOnly ?
      await captureC2Exemplar(cdp, base, captureDir) :
      await captureMatrix(cdp, base, captureDir)) : [];
    await viewport(cdp, 393, 852);
    if (sourceOnly) await navigateCandidate(cdp, base);
    else await navigateBuiltCandidate(cdp, base);
    await evaluate(cdp, 'window.scrollTo(0, 0)');
    const measured = await metrics(cdp);
    const modeMeasured = sourceOnly ? null : await modePerformance(cdp, base);
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
      sourceOnly,
      captures: captures.length,
      files: measuredFiles
    };
    if (captureDir) {
      await mkdir(captureDir, { recursive: true });
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
    await rm(profile, { recursive: true, force: true, maxRetries: 5, retryDelay: 100 });
  }
}

await main();
