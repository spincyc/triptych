#!/usr/bin/env node

/*
 * Bounded live verification for the Liturgical Instrument same-path cutover.
 *
 * This script intentionally has no package dependency. It drives the repository's
 * installed Chromium through the DevTools protocol, records original-pixel PNGs,
 * and writes one machine-readable result for either the immediate cache-bypassed
 * pass or the required post-freshness-window pass.
 */

import assert from 'node:assert/strict';
import { spawn } from 'node:child_process';
import { createHash } from 'node:crypto';
import { mkdtemp, mkdir, readFile, rm, writeFile } from 'node:fs/promises';
import { tmpdir } from 'node:os';
import { join, resolve } from 'node:path';
import process from 'node:process';

const ORIGIN = 'https://spincyc.github.io/triptych';
const CHROME = process.env.TRIPTYCH_CHROME || '/usr/bin/google-chrome-stable';
const REQUIRED_POST_WINDOW_SECONDS = 601;
const NOINDEX = 'noindex, nofollow, noarchive, nosnippet, noimageindex';

function parseOptions(argv) {
  const values = {};
  for (let index = 0; index < argv.length; index += 1) {
    const token = argv[index];
    if (!token.startsWith('--')) throw new Error(`unexpected argument: ${token}`);
    const name = token.slice(2);
    if (!['phase', 'cutover-sha', 'pages-run', 'output', 'immediate-result'].includes(name)) {
      throw new Error(`unknown option: ${token}`);
    }
    const value = argv[index + 1];
    if (!value || value.startsWith('--')) throw new Error(`missing value for ${token}`);
    values[name] = value;
    index += 1;
  }
  for (const required of ['phase', 'cutover-sha', 'pages-run', 'output']) {
    if (!values[required]) throw new Error(`missing --${required}`);
  }
  if (!['immediate-cache-bypassed', 'post-freshness-window'].includes(values.phase)) {
    throw new Error('--phase must be immediate-cache-bypassed or post-freshness-window');
  }
  if (!/^[0-9a-f]{7,40}$/.test(values['cutover-sha'])) {
    throw new Error('--cutover-sha must be a Git SHA');
  }
  if (!/^\d+$/.test(values['pages-run'])) throw new Error('--pages-run must be numeric');
  if (values.phase === 'post-freshness-window' && !values['immediate-result']) {
    throw new Error('--immediate-result is required for post-freshness-window');
  }
  return {
    phase: values.phase,
    cutoverSha: values['cutover-sha'],
    pagesRun: values['pages-run'],
    output: resolve(values.output),
    immediateResult: values['immediate-result'] ? resolve(values['immediate-result']) : null
  };
}

function sha256Bytes(bytes) {
  return createHash('sha256').update(bytes).digest('hex');
}

function hash(values) {
  return '#' + new URLSearchParams(values).toString();
}

const DAY = Object.freeze({
  read: hash({
    date: '2026-08-02', missal: 'roman-1962', bible: 'douay-rheims',
    orations: 'la', mass: 'pentecost-10', ordinary: '0'
  }),
  governing: hash({
    date: '2026-08-05', missal: 'roman-1962', bible: 'douay-rheims'
  }),
  missal: hash({
    date: '2026-08-02', missal: 'roman-1962', bible: 'douay-rheims',
    orations: 'la', mass: 'pentecost-10', ordinary: '1',
    'ordinary-lang': 'en', rubrics: '1', why: '0'
  }),
  partial: hash({
    date: '2026-01-01', missal: 'roman-1962', bible: 'douay-rheims',
    orations: 'la', mass: 'octava-nativitatis-domini', ordinary: '1',
    'ordinary-lang': 'en', rubrics: '1'
  }),
  post: hash({
    date: '2026-11-29', missal: 'postconciliar', bible: 'douay-rheims',
    orations: 'la', mass: 'advent-1', ordinary: '1', 'ordinary-lang': 'en',
    rubrics: '1', 'eucharistic-prayer': 'ep-ii'
  }),
  why: hash({
    date: '2026-08-02', missal: 'roman-1962', bible: 'douay-rheims',
    orations: 'la', mass: 'pentecost-10', ordinary: '0', why: '1'
  }),
  territorial: hash({
    date: '2026-01-04', missal: 'postconciliar', bible: 'douay-rheims',
    orations: 'la', ordinary: '0', why: '0'
  }),
  territorialWhy: hash({
    date: '2026-01-04', missal: 'postconciliar', bible: 'douay-rheims',
    orations: 'la', ordinary: '0', why: '1'
  })
});

const PROPERS = Object.freeze({
  read: hash({
    missal: 'roman-1962', type: 'seasonal', mass: 'advent-1',
    bible: 'douay-rheims', orations: 'la'
  }),
  browse: hash({ missal: 'roman-1962', bible: 'douay-rheims', orations: 'la' }),
  cycleBase: hash({
    missal: 'postconciliar', type: 'christological', mass: 'transfiguration-lord',
    bible: 'douay-rheims', orations: 'la'
  }),
  cycle: hash({
    missal: 'postconciliar', type: 'christological', mass: 'transfiguration-lord',
    bible: 'douay-rheims', orations: 'la', cycle: 'A'
  }),
  witnessBase: hash({
    missal: 'roman-1962', type: 'seasonal', mass: 'advent-1',
    bible: 'douay-rheims', orations: 'en'
  }),
  witness: hash({
    missal: 'roman-1962', type: 'seasonal', mass: 'advent-1',
    bible: 'douay-rheims', orations: 'en',
    'translation-witness': 'edition.eugene-cummiskey.roman-missal-english-laity.philadelphia-1861'
  }),
  alternative: hash({
    missal: 'postconciliar', type: 'christological', mass: 'transfiguration-lord',
    bible: 'douay-rheims', orations: 'la', alternative: 'first-reading-alternative'
  })
});

const IMMEDIATE_STATES = [
  { id: 'day-default-1440x900', entrance: 'day', hash: '', width: 1440, height: 900, defaultDay: true },
  { id: 'day-governing-deep-link-393x852', entrance: 'day', hash: DAY.governing, width: 393, height: 852 },
  { id: 'day-read-1440x900', entrance: 'day', hash: DAY.read, width: 1440, height: 900 },
  { id: 'day-read-1024x768', entrance: 'day', hash: DAY.read, width: 1024, height: 768 },
  { id: 'day-read-768x1024', entrance: 'day', hash: DAY.read, width: 768, height: 1024 },
  { id: 'day-read-393x852', entrance: 'day', hash: DAY.read, width: 393, height: 852 },
  { id: 'day-missal-1440x900', entrance: 'day', hash: DAY.missal, width: 1440, height: 900 },
  { id: 'day-missal-1024x768', entrance: 'day', hash: DAY.missal, width: 1024, height: 768 },
  { id: 'day-missal-393x852', entrance: 'day', hash: DAY.missal, width: 393, height: 852 },
  { id: 'day-missal-320x852', entrance: 'day', hash: DAY.missal, width: 320, height: 852 },
  { id: 'day-missal-deep-1440x900', entrance: 'day', hash: DAY.missal, width: 1440, height: 900, deep: true },
  { id: 'day-partial-393x852', entrance: 'day', hash: DAY.partial, width: 393, height: 852 },
  { id: 'day-postconciliar-1440x900', entrance: 'day', hash: DAY.post, width: 1440, height: 900 },
  { id: 'day-postconciliar-393x852', entrance: 'day', hash: DAY.post, width: 393, height: 852 },
  { id: 'day-why-1440x900', entrance: 'day', hash: DAY.why, width: 1440, height: 900, reasoning: true },
  { id: 'day-why-393x852', entrance: 'day', hash: DAY.why, width: 393, height: 852, reasoning: true },
  { id: 'day-territorial-1440x900', entrance: 'day', hash: DAY.territorial, width: 1440, height: 900 },
  { id: 'day-territorial-393x852', entrance: 'day', hash: DAY.territorial, width: 393, height: 852, secondBranch: true },
  { id: 'day-date-open-1024x768', entrance: 'day', hash: DAY.read, width: 1024, height: 768, action: 'date' },
  { id: 'day-contents-open-393x852', entrance: 'day', hash: DAY.missal, width: 393, height: 852, action: 'contents' },
  { id: 'day-mode-open-393x852', entrance: 'day', hash: DAY.read, width: 393, height: 852, action: 'mode' },
  { id: 'day-details-open-1440x900', entrance: 'day', hash: DAY.read, width: 1440, height: 900, action: 'details' },
  { id: 'day-details-open-393x852', entrance: 'day', hash: DAY.read, width: 393, height: 852, action: 'details', surfaceEnd: true },
  { id: 'day-text-200-percent-393x852', entrance: 'day', hash: DAY.missal, width: 393, height: 852, enlargement: true },
  { id: 'day-forced-colors-393x852', entrance: 'day', hash: DAY.read, width: 393, height: 852, media: [{ name: 'forced-colors', value: 'active' }] },
  { id: 'day-keyboard-focus-393x852', entrance: 'day', hash: DAY.read, width: 393, height: 852, keyboard: true },
  { id: 'day-reduced-motion-393x852', entrance: 'day', hash: DAY.missal, width: 393, height: 852, media: [{ name: 'prefers-reduced-motion', value: 'reduce' }] },
  { id: 'propers-read-1440x900', entrance: 'propers', hash: PROPERS.read, width: 1440, height: 900 },
  { id: 'propers-read-393x852', entrance: 'propers', hash: PROPERS.read, width: 393, height: 852 },
  { id: 'propers-browse-1440x900', entrance: 'propers', hash: PROPERS.browse, width: 1440, height: 900, browse: true },
  { id: 'propers-browse-393x852', entrance: 'propers', hash: PROPERS.browse, width: 393, height: 852, browse: true },
  { id: 'propers-details-open-1440x900', entrance: 'propers', hash: PROPERS.read, width: 1440, height: 900, action: 'details' },
  { id: 'propers-details-open-393x852', entrance: 'propers', hash: PROPERS.read, width: 393, height: 852, action: 'details', surfaceEnd: true },
  { id: 'propers-cycle-393x852', entrance: 'propers', hash: PROPERS.cycle, width: 393, height: 852, stableKey: 'cycle' },
  { id: 'propers-translation-witness-393x852', entrance: 'propers', hash: PROPERS.witness, width: 393, height: 852, stableKey: 'translation-witness' },
  { id: 'propers-alternative-fail-closed-393x852', entrance: 'propers', hash: PROPERS.alternative, width: 393, height: 852, stableKey: 'alternative', invalid: true }
];

const POST_WINDOW_STATES = [
  { id: 'day-default-1440x900', entrance: 'day', hash: '', width: 1440, height: 900, defaultDay: true },
  { id: 'day-governing-deep-link-393x852', entrance: 'day', hash: DAY.governing, width: 393, height: 852 },
  { id: 'day-missal-393x852', entrance: 'day', hash: DAY.missal, width: 393, height: 852 },
  { id: 'propers-governing-deep-link-393x852', entrance: 'propers', hash: PROPERS.read, width: 393, height: 852 },
  { id: 'day-details-open-393x852', entrance: 'day', hash: DAY.read, width: 393, height: 852, action: 'details' },
  { id: 'day-territorial-why-393x852', entrance: 'day', hash: DAY.territorialWhy, width: 393, height: 852, reasoning: true, secondBranch: true }
];

const STATIC_SURFACES = [
  { id: 'candidate-day', pathname: '/liturgy/day-reader.html', robots: NOINDEX, entrance: 'day' },
  { id: 'candidate-propers', pathname: '/liturgy/propers-reader.html', robots: NOINDEX, entrance: 'propers' },
  { id: 'oracle-day', pathname: '/liturgy/reader-visual-reset-day.html?design=instrument', robots: NOINDEX, entrance: 'day' },
  { id: 'oracle-propers', pathname: '/liturgy/reader-visual-reset-propers.html?design=instrument', robots: NOINDEX, entrance: 'propers' }
];

async function freePort() {
  const server = await import('node:net').then(({ createServer }) => createServer());
  await new Promise((accept, reject) => {
    server.once('error', reject);
    server.listen(0, '127.0.0.1', accept);
  });
  const port = server.address().port;
  await new Promise(accept => server.close(accept));
  return port;
}

async function waitForJson(url, attempts = 160) {
  for (let attempt = 0; attempt < attempts; attempt += 1) {
    try {
      const response = await fetch(url);
      if (response.ok) return response.json();
    } catch (_error) { /* Chromium is starting. */ }
    await new Promise(accept => setTimeout(accept, 50));
  }
  throw new Error(`Chromium debugging endpoint did not become ready: ${url}`);
}

class CDP {
  constructor(url) {
    this.socket = new WebSocket(url);
    this.serial = 0;
    this.pending = new Map();
    this.listeners = new Map();
    this.readyPromise = new Promise((accept, reject) => {
      this.socket.addEventListener('open', accept, { once: true });
      this.socket.addEventListener('error', reject, { once: true });
    });
    this.socket.addEventListener('message', event => {
      const message = JSON.parse(event.data);
      if (message.id) {
        const held = this.pending.get(message.id);
        if (!held) return;
        this.pending.delete(message.id);
        if (message.error) held.reject(new Error(message.error.message));
        else held.accept(message.result);
        return;
      }
      for (const listener of this.listeners.get(message.method) || []) listener(message.params || {});
    });
  }

  ready() { return this.readyPromise; }

  on(method, listener) {
    if (!this.listeners.has(method)) this.listeners.set(method, []);
    this.listeners.get(method).push(listener);
  }

  async send(method, params = {}) {
    await this.readyPromise;
    const id = ++this.serial;
    const promise = new Promise((accept, reject) => this.pending.set(id, { accept, reject }));
    this.socket.send(JSON.stringify({ id, method, params }));
    return promise;
  }

  close() { this.socket.close(); }
}

async function evaluate(cdp, expression) {
  const reply = await cdp.send('Runtime.evaluate', {
    expression, awaitPromise: true, returnByValue: true
  });
  if (reply.exceptionDetails) {
    throw new Error(reply.exceptionDetails.exception?.description || reply.exceptionDetails.text);
  }
  return reply.result.value;
}

async function waitFor(cdp, expression, label, attempts = 300) {
  for (let count = 0; count < attempts; count += 1) {
    if (await evaluate(cdp, `Boolean(${expression})`)) return;
    await new Promise(accept => setTimeout(accept, 50));
  }
  throw new Error(`timed out waiting for ${label}`);
}

async function settle(cdp) {
  await evaluate(cdp, `new Promise(resolve => requestAnimationFrame(() => requestAnimationFrame(resolve)))`);
  await new Promise(accept => setTimeout(accept, 80));
}

async function setViewport(cdp, width, height) {
  await cdp.send('Emulation.setDeviceMetricsOverride', {
    width, height, screenWidth: width, screenHeight: height,
    deviceScaleFactor: 1, mobile: width <= 768
  });
}

async function screenshot(cdp, pathname) {
  const result = await cdp.send('Page.captureScreenshot', {
    format: 'png', fromSurface: true, captureBeyondViewport: false
  });
  await writeFile(pathname, Buffer.from(result.data, 'base64'));
}

function pagePath(entrance) {
  return entrance === 'day' ? '/liturgy/day.html' : '/liturgy/index.html';
}

function publicUrl(entrance, state = '') {
  return ORIGIN + pagePath(entrance) + state;
}

function readyExpression(entrance) {
  return entrance === 'day' ? 'window.dayReaderReady === true' : 'window.propersReaderReady === true';
}

function debugName(entrance) {
  return entrance === 'day' ? 'dayReaderDebug' : 'propersReaderDebug';
}

async function openFresh(cdp, target, entrance) {
  await cdp.send('Page.navigate', { url: 'about:blank' });
  await waitFor(cdp, `location.href === 'about:blank'`, 'blank page');
  await cdp.send('Page.navigate', { url: target });
  await waitFor(cdp,
    `location.href === ${JSON.stringify(target)} && ${readyExpression(entrance)} && ` +
      `document.querySelector('#reader-document[aria-busy="false"]')`,
    `${entrance} reader readiness`);
  await settle(cdp);
}

function assertionsForSnapshot(row, snapshot) {
  const checks = [];
  function check(name, condition, detail = null) {
    checks.push({ name, status: condition ? 'pass' : 'fail', ...(condition ? {} : { detail }) });
  }

  check('document HTTP 200', snapshot.documentResponse?.status === 200, snapshot.documentResponse);
  check('no document redirect', snapshot.redirects.length === 0, snapshot.redirects);
  check('canonical pathname retained', snapshot.dom.pathname === `/triptych${pagePath(row.entrance)}`, snapshot.dom.pathname);
  check('exact requested hash retained', snapshot.dom.hash === row.hash, snapshot.dom.hash);
  check('reader ready', snapshot.dom.ready === true, snapshot.dom.ready);
  check('reader document settled', snapshot.dom.busy === 'false', snapshot.dom.busy);
  check('exactly one accepted shell', snapshot.dom.shellCount === 1, snapshot.dom.shellCount);
  check('shell entrance is correct', snapshot.dom.shellEntrance === row.entrance, snapshot.dom.shellEntrance);
  check('canonical page is indexable', snapshot.dom.robots === 'index, follow', snapshot.dom.robots);
  check('canonical Open Graph URL is route-correct',
    snapshot.dom.ogUrl === `${ORIGIN}${pagePath(row.entrance)}`, snapshot.dom.ogUrl);
  check('user-visible wording is route-neutral', !snapshot.dom.provisionalWording, snapshot.dom.provisionalSample);
  check('no duplicate IDs', snapshot.dom.duplicateIds.length === 0, snapshot.dom.duplicateIds);
  check('no unnamed interactive controls', snapshot.dom.unnamedDom.length === 0, snapshot.dom.unnamedDom);
  check('no unnamed AX controls', snapshot.axUnnamed.length === 0, snapshot.axUnnamed);
  check('no horizontal overflow', snapshot.dom.horizontalOverflow <= 1, snapshot.dom.horizontalOverflow);
  check('four primary actions remain', snapshot.dom.actions.length === 4, snapshot.dom.actions);
  const expectedActionLabels = row.entrance === 'day'
    ? ['Date', 'Contents', 'Mode', 'Details']
    : ['Browse', 'Contents', 'Mode', 'Details'];
  check('primary actions have the four complete expected labels',
    snapshot.dom.actions.map(action => action.label).join('|') === expectedActionLabels.join('|'),
    snapshot.dom.actions);
  check('primary labels remain on one unbroken line', snapshot.dom.actions.every(action =>
    action.labelLines === 1 && action.labelScrollWidth <= action.labelClientWidth + 1),
    snapshot.dom.actions);
  check('primary actions have adequate targets', snapshot.dom.actions.every(action =>
    action.width >= 44 && action.height >= 44), snapshot.dom.actions);
  check('no console problems', snapshot.consoleProblems.length === 0, snapshot.consoleProblems);
  check('no required failed requests', snapshot.failedRequests.length === 0, snapshot.failedRequests);
  check('no HTTP problems', snapshot.httpProblems.length === 0, snapshot.httpProblems);

  if (!row.browse && !row.invalid) {
    check('liturgical content rendered', snapshot.dom.properCount > 0, snapshot.dom.properCount);
  }
  if (row.defaultDay) {
    check('empty Day defaults to Roman 1962', snapshot.dom.state?.edition?.id === 'roman-1962', snapshot.dom.state);
    check('empty Day defaults to Read', snapshot.dom.state?.requestedMode === 'read', snapshot.dom.state);
    check('empty Day uses browser-local civil date', snapshot.dom.state?.civilDate === snapshot.dom.browserLocalDate,
      { state: snapshot.dom.state?.civilDate, browser: snapshot.dom.browserLocalDate });
  }
  if (row.reasoning) {
    check('why=1 remains in the URL', new URLSearchParams(row.hash.slice(1)).get('why') === '1');
    check('reasoning apparatus is present', snapshot.dom.reasoningCount > 0, snapshot.dom.reasoningCount);
    check('reasoning apparatus is reachable/open for evidence', snapshot.dom.openReasoningCount > 0,
      snapshot.dom.openReasoningCount);
  }
  if (row.hash === DAY.territorial || row.hash === DAY.territorialWhy) {
    check('all held territorial branches render', snapshot.dom.territorialBranches.length === 2,
      snapshot.dom.territorialBranches);
    check('territorial labels are explicit', snapshot.dom.territorialBranches.every(branch =>
      branch.id && branch.label), snapshot.dom.territorialBranches);
    check('no geography key is inferred', !new URLSearchParams(row.hash.slice(1)).has('territory') &&
      !snapshot.dom.state?.calendar?.territory, snapshot.dom.state?.calendar);
  }
  if (row.browse) {
    check('Browse surface is open', snapshot.dom.openSurface === 'browse', snapshot.dom.openSurface);
    check('Browse outcome is explicit', snapshot.dom.outcome === 'browse', snapshot.dom.outcome);
  }
  if (row.action) {
    check(`${row.action} surface is open`, snapshot.dom.openSurface === row.action, snapshot.dom.openSurface);
  }
  if (row.action === 'details') {
    const counterpart = row.entrance === 'day' ? 'Browse the Propers' : 'Open the Day reader';
    const counterpartPath = row.entrance === 'day' ? '/triptych/liturgy/index.html' : '/triptych/liturgy/day.html';
    const match = snapshot.dom.detailsLinks.find(link => link.label === counterpart);
    check('Details exposes canonical counterpart first', snapshot.dom.detailsLinks[0]?.label === counterpart,
      snapshot.dom.detailsLinks);
    check('Details counterpart targets canonical route', match?.pathname === counterpartPath, match);
    check('Details preserves counterpart plus the route-owned contextual destinations',
      snapshot.dom.detailsLinks.length >= 3,
      snapshot.dom.detailsLinks);
  }
  if (row.stableKey === 'cycle') {
    check('cycle uses stable public key', snapshot.dom.state?.cycle === 'A' &&
      !snapshot.dom.hash.includes('_candidate-'), snapshot.dom.state);
  }
  if (row.stableKey === 'translation-witness') {
    check('translation-witness uses stable public key',
      snapshot.dom.state?.languages?.translationWitness ===
        'edition.eugene-cummiskey.roman-missal-english-laity.philadelphia-1861' &&
        !snapshot.dom.hash.includes('_candidate-'), snapshot.dom.state);
  }
  if (row.stableKey === 'alternative') {
    check('unsupported alternative remains explicit', new URLSearchParams(snapshot.dom.hash.slice(1)).get('alternative') ===
      'first-reading-alternative', snapshot.dom.hash);
    check('unsupported alternative fails closed', snapshot.dom.outcome === 'invalid' && snapshot.dom.properCount === 0,
      { outcome: snapshot.dom.outcome, properCount: snapshot.dom.properCount });
  }
  return checks;
}

async function prepareState(cdp, row) {
  await setViewport(cdp, row.width, row.height);
  await cdp.send('Emulation.setEmulatedMedia', { media: 'screen', features: row.media || [] });
  await openFresh(cdp, publicUrl(row.entrance, row.hash), row.entrance);

  if (row.enlargement) {
    await evaluate(cdp, `document.documentElement.style.fontSize = '200%'`);
    await settle(cdp);
  }
  if (row.deep) {
    await evaluate(cdp, `document.querySelector('#reader-document .proper:last-of-type')?.scrollIntoView({block:'center'})`);
    await settle(cdp);
  }
  if (row.reasoning) {
    await evaluate(cdp, `(() => {
      const rows = [...document.querySelectorAll('.day-reasoning')];
      rows.forEach(node => { node.open = true; });
      (rows[0]?.querySelector('summary') || rows[0])?.scrollIntoView({block:'center'});
    })()`);
    await settle(cdp);
  }
  if (row.secondBranch) {
    await evaluate(cdp, `document.querySelectorAll('section.territorial-branch')[1]?.scrollIntoView({block:'start'})`);
    await settle(cdp);
  }
  if (row.action) {
    await evaluate(cdp, `document.querySelector('[data-reader-action=${JSON.stringify(row.action)}]')?.click()`);
    await waitFor(cdp,
      `document.querySelector('[data-reader-surface=${JSON.stringify(row.action)}]')?.open === true`,
      `${row.action} surface`);
    if (row.surfaceEnd) {
      await evaluate(cdp, `(() => {
        const surface = document.querySelector('[data-reader-surface=${JSON.stringify(row.action)}]');
        const scroller = surface?.querySelector('.surface-body') || surface;
        if (scroller) scroller.scrollTop = scroller.scrollHeight;
      })()`);
    }
    await settle(cdp);
  }
  if (row.keyboard) {
    await evaluate(cdp, `document.querySelector('[data-reader-action="contents"]')?.focus()`);
    await cdp.send('Input.dispatchKeyEvent', {
      type: 'keyDown', key: 'Tab', code: 'Tab', windowsVirtualKeyCode: 9
    });
    await cdp.send('Input.dispatchKeyEvent', {
      type: 'keyUp', key: 'Tab', code: 'Tab', windowsVirtualKeyCode: 9
    });
    await settle(cdp);
  }
}

async function domSnapshot(cdp, entrance) {
  const debug = debugName(entrance);
  return evaluate(cdp, `(() => {
    const interactive = [...document.querySelectorAll(
      'a[href], button, input, select, textarea, [role="button"], [tabindex]'
    )].filter(node => !node.disabled && node.getAttribute('aria-hidden') !== 'true' &&
      getComputedStyle(node).display !== 'none' && getComputedStyle(node).visibility !== 'hidden' &&
      node.getClientRects().length > 0);
    const ids = [...document.querySelectorAll('[id]')].map(node => node.id);
    const duplicates = [...new Set(ids.filter((id, index) => ids.indexOf(id) !== index))];
    const actions = [...document.querySelectorAll('[data-reader-action]')].map(node => {
      const box = node.getBoundingClientRect();
      const label = node.querySelector('.action-label');
      const labelBox = label?.getBoundingClientRect();
      const lineHeight = label ? parseFloat(getComputedStyle(label).lineHeight) || labelBox.height : 0;
      return {
        action: node.dataset.readerAction,
        name: node.getAttribute('aria-label') || node.innerText.trim(),
        label: label?.textContent.trim() || '',
        labelLines: labelBox && lineHeight ? Math.round(labelBox.height / lineHeight) : 0,
        labelScrollWidth: label?.scrollWidth || 0,
        labelClientWidth: label?.clientWidth || 0,
        width: box.width,
        height: box.height
      };
    });
    const details = document.querySelector('[data-reader-details]');
    const now = new Date();
    const browserLocalDate = [now.getFullYear(), String(now.getMonth() + 1).padStart(2, '0'),
      String(now.getDate()).padStart(2, '0')].join('-');
    const visible = document.body.innerText;
    const state = structuredClone(window.${debug}?.state || null);
    return {
      href: location.href,
      pathname: location.pathname,
      hash: location.hash,
      title: document.title,
      ready: ${readyExpression(entrance)},
      busy: document.querySelector('#reader-document')?.getAttribute('aria-busy') || null,
      shellCount: document.querySelectorAll('[data-reader-shell]').length,
      shellEntrance: document.querySelector('[data-reader-shell]')?.dataset.entrance || null,
      robots: document.querySelector('meta[name="robots"]')?.content || null,
      ogUrl: document.querySelector('meta[property="og:url"]')?.content || null,
      provisionalWording: /internal (?:reader )?candidate|W3 candidate|prototype reader/i.test(visible),
      provisionalSample: visible.match(/.{0,35}(?:internal (?:reader )?candidate|W3 candidate|prototype reader).{0,35}/i)?.[0] || null,
      duplicateIds: duplicates,
      unnamedDom: interactive.filter(node => !(
        node.getAttribute('aria-label') || node.getAttribute('aria-labelledby') ||
        node.innerText?.trim() || node.value || node.title
      )).map(node => node.id || node.dataset.readerAction || node.tagName),
      horizontalOverflow: document.documentElement.scrollWidth - document.documentElement.clientWidth,
      actions,
      properCount: document.querySelectorAll('#reader-document .proper').length,
      state,
      outcome: window.${debug}?.outcome || (window.${debug}?.ready ? 'ready' : null),
      browserLocalDate,
      reasoningCount: document.querySelectorAll('.day-reasoning').length,
      openReasoningCount: document.querySelectorAll('.day-reasoning[open]').length,
      territorialBranches: [...document.querySelectorAll('section.territorial-branch')].map(node => ({
        id: node.dataset.territorialBranch || '',
        label: node.querySelector('.territorial-branch-label, .territorial-branch-heading h2')?.textContent.trim() || ''
      })),
      openSurface: document.querySelector('dialog[open][data-reader-surface]')?.dataset.readerSurface || null,
      detailsLinks: details ? [...details.querySelectorAll('a')].map(node => ({
        label: node.textContent.trim(), pathname: new URL(node.href).pathname
      })) : [],
      scroll: {
        x: scrollX, y: scrollY,
        documentHeight: document.documentElement.scrollHeight,
        viewportWidth: innerWidth, viewportHeight: innerHeight
      },
      activeElement: {
        tag: document.activeElement?.tagName || null,
        id: document.activeElement?.id || null,
        name: document.activeElement?.getAttribute('aria-label') || document.activeElement?.innerText?.trim() || null
      }
    };
  })()`);
}

async function axUnnamed(cdp) {
  const tree = await cdp.send('Accessibility.getFullAXTree');
  return tree.nodes.filter(node => !node.ignored &&
    ['button', 'link', 'radio', 'textbox', 'combobox'].includes(node.role?.value) &&
    !node.name?.value).map(node => ({ role: node.role?.value, nodeId: node.nodeId }));
}

function stateNetwork(log, start) {
  const requests = log.requests.slice(start.requests);
  const responses = log.responses.slice(start.responses);
  const documentResponse = [...responses].reverse().find(row => row.type === 'Document') || null;
  const requested = new Set(requests.map(row => row.url));
  return {
    requests,
    responses,
    documentResponse,
    redirects: log.redirects.slice(start.redirects),
    failedRequests: log.failedRequests.slice(start.failedRequests).filter(row => !row.canceled),
    httpProblems: responses.filter(row => row.status >= 400 && requested.has(row.url)),
    consoleProblems: log.consoleProblems.slice(start.consoleProblems)
  };
}

async function verifyState(cdp, log, row, screenshotsDirectory) {
  const start = Object.fromEntries(Object.entries(log).map(([key, value]) => [key, value.length]));
  let preparationError = null;
  try {
    await prepareState(cdp, row);
  } catch (error) {
    preparationError = error.stack || String(error);
  }
  const filename = `${row.id}.png`;
  let dom = null;
  let unnamed = [];
  if (!preparationError) {
    dom = await domSnapshot(cdp, row.entrance);
    unnamed = await axUnnamed(cdp);
    await screenshot(cdp, join(screenshotsDirectory, filename));
  }
  const network = stateNetwork(log, start);
  const snapshot = {
    documentResponse: network.documentResponse,
    redirects: network.redirects,
    dom,
    axUnnamed: unnamed,
    consoleProblems: network.consoleProblems,
    failedRequests: network.failedRequests,
    httpProblems: network.httpProblems
  };
  const assertions = preparationError ? [
    { name: 'state preparation', status: 'fail', detail: preparationError }
  ] : assertionsForSnapshot(row, snapshot);
  return {
    id: row.id,
    entrance: row.entrance,
    url: publicUrl(row.entrance, row.hash),
    finalUrl: dom?.href || null,
    viewport: { width: row.width, height: row.height, deviceScaleFactor: 1 },
    screenshot: preparationError ? null : `screenshots/${filename}`,
    assertions,
    state: dom?.state || null,
    geometry: dom?.scroll || null,
    metadata: dom ? { title: dom.title, robots: dom.robots, ogUrl: dom.ogUrl } : null,
    network: {
      documentResponse: network.documentResponse,
      redirects: network.redirects,
      requests: network.requests,
      failedRequests: network.failedRequests,
      httpProblems: network.httpProblems
    },
    consoleProblems: network.consoleProblems
  };
}

async function verifyStaticSurfaces(cdp, log) {
  const results = [];
  for (const row of STATIC_SURFACES) {
    const hash = row.entrance === 'day' ? DAY.read : PROPERS.read;
    const target = ORIGIN + row.pathname + hash;
    const start = Object.fromEntries(Object.entries(log).map(([key, value]) => [key, value.length]));
    let error = null;
    let observed = null;
    try {
      await openFresh(cdp, target, row.entrance);
      observed = await evaluate(cdp, `({
        href: location.href,
        pathname: location.pathname,
        robots: document.querySelector('meta[name="robots"]')?.content || null,
        ogUrl: document.querySelector('meta[property="og:url"]')?.content || null
      })`);
    } catch (held) {
      error = held.stack || String(held);
    }
    const network = stateNetwork(log, start);
    const assertions = [];
    function add(name, condition, detail = null) {
      assertions.push({ name, status: condition ? 'pass' : 'fail', ...(condition ? {} : { detail }) });
    }
    add('surface loads without error', !error, error);
    add('surface HTTP 200', network.documentResponse?.status === 200, network.documentResponse);
    add('surface has static full noindex', observed?.robots === row.robots, observed?.robots);
    add('surface does not advertise an Open Graph public URL', observed?.ogUrl === null, observed?.ogUrl);
    add('surface does not redirect', network.redirects.length === 0, network.redirects);
    results.push({ id: row.id, url: target, observed, assertions });
  }
  return results;
}

async function lifecycle(cdp, entrance, originHash, targetHash, condition, label) {
  const result = { id: label, assertions: [], observations: [] };
  async function observe(step) {
    const value = await evaluate(cdp, `({
      step: ${JSON.stringify(step)},
      hash: location.hash,
      ready: ${readyExpression(entrance)},
      outcome: window.${debugName(entrance)}?.outcome || null,
      state: structuredClone(window.${debugName(entrance)}?.state || null)
    })`);
    result.observations.push(value);
    return value;
  }
  try {
    await openFresh(cdp, publicUrl(entrance, originHash), entrance);
    await observe('origin');
    await evaluate(cdp, `location.hash = ${JSON.stringify(targetHash.slice(1))}`);
    await waitFor(cdp, `${readyExpression(entrance)} && (${condition})`, `${label} direct state`);
    let value = await observe('direct');
    assert.equal(value.hash, targetHash);

    await cdp.send('Page.reload', { ignoreCache: true });
    await waitFor(cdp, `${readyExpression(entrance)} && (${condition})`, `${label} reload`);
    value = await observe('reload');
    assert.equal(value.hash, targetHash);

    await evaluate(cdp, 'history.back()');
    await waitFor(cdp, `${readyExpression(entrance)} && location.hash === ${JSON.stringify(originHash)}`,
      `${label} Back`);
    await observe('back');

    await evaluate(cdp, 'history.forward()');
    await waitFor(cdp, `${readyExpression(entrance)} && location.hash === ${JSON.stringify(targetHash)} && (${condition})`,
      `${label} Forward`);
    await observe('forward');
    result.assertions.push({ name: 'direct/reload/Back/Forward lifecycle', status: 'pass' });
  } catch (error) {
    result.assertions.push({
      name: 'direct/reload/Back/Forward lifecycle', status: 'fail', detail: error.stack || String(error)
    });
  }
  return result;
}

async function runLifecycles(cdp) {
  return [
    await lifecycle(cdp, 'day', DAY.read, DAY.why,
      `new URLSearchParams(location.hash.slice(1)).get('why') === '1' && ` +
      `document.querySelectorAll('.day-reasoning').length > 0`, 'day-why'),
    await lifecycle(cdp, 'propers', PROPERS.cycleBase, PROPERS.cycle,
      `propersReaderDebug.state.cycle === 'A'`, 'propers-cycle'),
    await lifecycle(cdp, 'propers', PROPERS.witnessBase, PROPERS.witness,
      `propersReaderDebug.state.languages.translationWitness === ` +
      `${JSON.stringify('edition.eugene-cummiskey.roman-missal-english-laity.philadelphia-1861')}`,
      'propers-translation-witness'),
    await lifecycle(cdp, 'propers', PROPERS.cycleBase, PROPERS.alternative,
      `propersReaderDebug.outcome === 'invalid' && ` +
      `new URLSearchParams(location.hash.slice(1)).get('alternative') === 'first-reading-alternative'`,
      'propers-unsupported-alternative')
  ];
}

async function fetchArtifact(pathname, cacheBypassed) {
  const headers = cacheBypassed ? {
    'cache-control': 'no-cache', pragma: 'no-cache'
  } : {};
  const suffix = cacheBypassed ? `?cutover=${encodeURIComponent(options.cutoverSha)}` : '';
  const response = await fetch(ORIGIN + pathname + suffix, { redirect: 'manual', headers });
  const bytes = Buffer.from(await response.arrayBuffer());
  return {
    path: pathname,
    url: ORIGIN + pathname + suffix,
    status: response.status,
    redirected: response.status >= 300 && response.status < 400,
    headers: Object.fromEntries([...response.headers.entries()].filter(([name]) =>
      ['age', 'cache-control', 'content-type', 'etag', 'last-modified', 'location'].includes(name))),
    bytes: bytes.length,
    sha256: sha256Bytes(bytes),
    body: bytes
  };
}

async function verifyArtifacts(cacheBypassed) {
  const paths = [
    '/liturgy/day.html', '/liturgy/index.html',
    '/liturgy/day-reader.html', '/liturgy/propers-reader.html',
    '/liturgy/reader-visual-reset-day.html', '/liturgy/reader-visual-reset-propers.html',
    '/liturgy/day-reader.js', '/liturgy/propers-reader.js',
    '/liturgy/day-reader.css', '/liturgy/propers-reader.css',
    '/liturgy/reader-state.js', '/liturgy/reader-state-adapters.js',
    '/liturgy/reader-shell.js', '/liturgy/reader-shell.css',
    '/liturgy/reader-instrument.css'
  ];
  const results = [];
  for (const pathname of paths) {
    const held = await fetchArtifact(pathname, cacheBypassed);
    const builtPath = resolve('build/public-alpha/site', pathname.replace(/^\//, ''));
    let built = null;
    try {
      const bytes = await readFile(builtPath);
      built = { bytes: bytes.length, sha256: sha256Bytes(bytes), matches: bytes.equals(held.body) };
    } catch (error) {
      built = { error: error.message };
    }
    results.push({
      path: held.path, url: held.url, status: held.status, redirected: held.redirected,
      headers: held.headers, bytes: held.bytes, sha256: held.sha256, built,
      assertions: [
        { name: 'HTTP 200', status: held.status === 200 ? 'pass' : 'fail', detail: held.status },
        { name: 'no redirect', status: !held.redirected ? 'pass' : 'fail', detail: held.headers.location || null },
        { name: 'deployed bytes match locked public-alpha build', status: built.matches ? 'pass' : 'fail', detail: built }
      ]
    });
  }
  return results;
}

function summarize(report) {
  const allAssertions = [
    ...report.states.flatMap(row => row.assertions),
    ...report.staticSurfaces.flatMap(row => row.assertions),
    ...report.lifecycle.flatMap(row => row.assertions),
    ...report.assets.flatMap(row => row.assertions)
  ];
  const globalProblems = {
    console: report.global.consoleProblems.length,
    failedRequests: report.global.failedRequests.filter(row => !row.canceled).length,
    http: report.global.httpProblems.length
  };
  return {
    assertions: allAssertions.length,
    passed: allAssertions.filter(row => row.status === 'pass').length,
    failed: allAssertions.filter(row => row.status === 'fail').length,
    screenshots: report.states.filter(row => row.screenshot).length,
    globalProblems,
    status: allAssertions.every(row => row.status === 'pass') &&
      Object.values(globalProblems).every(count => count === 0) ? 'pass' : 'fail'
  };
}

async function loadCacheBoundary(currentOptions) {
  if (currentOptions.phase === 'immediate-cache-bypassed') {
    return {
      strategy: 'CDP cache disabled; no-cache request headers; reloads ignore cache',
      requiredMinimumSeconds: REQUIRED_POST_WINDOW_SECONDS,
      immediateCompletedAt: null,
      elapsedSeconds: 0
    };
  }
  const immediate = JSON.parse(await readFile(currentOptions.immediateResult, 'utf8'));
  assert.equal(immediate.schema, 'triptych-public-cutover-live-verification/v1');
  assert.equal(immediate.phase, 'immediate-cache-bypassed');
  assert.equal(immediate.cutoverSha, currentOptions.cutoverSha);
  assert.equal(String(immediate.pagesRun), String(currentOptions.pagesRun));
  assert.equal(immediate.summary?.status, 'pass', 'immediate result is not green');
  const completed = Date.parse(immediate.completedAt);
  assert.ok(Number.isFinite(completed), 'immediate result lacks a valid completedAt');
  const elapsedSeconds = Math.floor((Date.now() - completed) / 1000);
  assert.ok(elapsedSeconds >= REQUIRED_POST_WINDOW_SECONDS,
    `post-window verification started after ${elapsedSeconds}s; require at least ${REQUIRED_POST_WINDOW_SECONDS}s`);
  return {
    strategy: 'fresh Chromium profile; normal cache; no cache-busting headers or query',
    requiredMinimumSeconds: REQUIRED_POST_WINDOW_SECONDS,
    immediateCompletedAt: immediate.completedAt,
    elapsedSeconds
  };
}

const options = parseOptions(process.argv.slice(2));

async function main() {
  const startedAt = new Date().toISOString();
  const cache = await loadCacheBoundary(options);
  const screenshotsDirectory = join(options.output, 'screenshots');
  await mkdir(screenshotsDirectory, { recursive: true });

  const debugPort = await freePort();
  const profile = await mkdtemp(join(tmpdir(), 'triptych-live-cutover-chrome-'));
  const chrome = spawn(CHROME, [
    '--headless=new', '--no-sandbox', '--disable-dev-shm-usage', '--disable-gpu',
    `--remote-debugging-port=${debugPort}`, `--user-data-dir=${profile}`,
    '--no-first-run', '--no-default-browser-check', 'about:blank'
  ], { stdio: ['ignore', 'ignore', 'pipe'] });
  let stderr = '';
  chrome.stderr.on('data', chunk => { stderr += chunk.toString(); });
  let cdp;
  let report;
  const log = {
    requests: [], responses: [], redirects: [], failedRequests: [],
    consoleProblems: [], httpProblems: []
  };

  try {
    const version = await waitForJson(`http://127.0.0.1:${debugPort}/json/version`);
    const response = await fetch(
      `http://127.0.0.1:${debugPort}/json/new?${encodeURIComponent('about:blank')}`,
      { method: 'PUT' }
    );
    const page = await response.json();
    cdp = new CDP(page.webSocketDebuggerUrl);
    await cdp.ready();
    await Promise.all([
      cdp.send('Page.enable'), cdp.send('Runtime.enable'), cdp.send('Network.enable'),
      cdp.send('Accessibility.enable')
    ]);
    const bypass = options.phase === 'immediate-cache-bypassed';
    await cdp.send('Network.setCacheDisabled', { cacheDisabled: bypass });
    await cdp.send('Network.setExtraHTTPHeaders', {
      headers: bypass ? { 'Cache-Control': 'no-cache', Pragma: 'no-cache' } : {}
    });

    cdp.on('Runtime.consoleAPICalled', ({ type, args }) => {
      if (['error', 'warning'].includes(type)) log.consoleProblems.push({
        type, text: args.map(argument => argument.value || argument.description || '').join(' '),
        url: null
      });
    });
    cdp.on('Runtime.exceptionThrown', ({ exceptionDetails }) => {
      log.consoleProblems.push({
        type: 'exception', text: exceptionDetails.exception?.description || exceptionDetails.text,
        url: exceptionDetails.url || null
      });
    });
    cdp.on('Network.requestWillBeSent', event => {
      log.requests.push({
        requestId: event.requestId, url: event.request.url, method: event.request.method,
        type: event.type, documentURL: event.documentURL
      });
      if (event.redirectResponse) log.redirects.push({
        from: event.redirectResponse.url, status: event.redirectResponse.status, to: event.request.url
      });
    });
    cdp.on('Network.loadingFailed', event => log.failedRequests.push({
      requestId: event.requestId, error: event.errorText, canceled: Boolean(event.canceled), type: event.type
    }));
    cdp.on('Network.responseReceived', ({ requestId, type, response: held }) => {
      const row = {
        requestId, type, url: held.url, status: held.status,
        fromDiskCache: Boolean(held.fromDiskCache),
        fromServiceWorker: Boolean(held.fromServiceWorker),
        protocol: held.protocol,
        headers: Object.fromEntries(Object.entries(held.headers || {}).filter(([name]) =>
          ['age', 'cache-control', 'content-type', 'etag', 'last-modified', 'location']
            .includes(name.toLowerCase())))
      };
      log.responses.push(row);
      if (held.status >= 400) log.httpProblems.push(row);
    });

    const rows = options.phase === 'immediate-cache-bypassed' ? IMMEDIATE_STATES : POST_WINDOW_STATES;
    const states = [];
    for (const row of rows) states.push(await verifyState(cdp, log, row, screenshotsDirectory));
    const staticSurfaces = await verifyStaticSurfaces(cdp, log);
    const lifecycleResults = options.phase === 'immediate-cache-bypassed' ? await runLifecycles(cdp) : [];
    const assets = await verifyArtifacts(bypass);
    const completedAt = new Date().toISOString();
    report = {
      schema: 'triptych-public-cutover-live-verification/v1',
      phase: options.phase,
      generatedAt: startedAt,
      completedAt,
      cutoverSha: options.cutoverSha,
      pagesRun: options.pagesRun,
      origin: ORIGIN,
      chrome: version.Browser,
      cache,
      states,
      staticSurfaces,
      lifecycle: lifecycleResults,
      assets,
      global: {
        consoleProblems: log.consoleProblems,
        failedRequests: log.failedRequests,
        httpProblems: log.httpProblems,
        responseCache: log.responses.map(row => ({
          url: row.url, status: row.status, fromDiskCache: row.fromDiskCache,
          fromServiceWorker: row.fromServiceWorker, headers: row.headers
        }))
      }
    };
    report.summary = summarize(report);
  } catch (error) {
    report = {
      schema: 'triptych-public-cutover-live-verification/v1',
      phase: options.phase,
      generatedAt: startedAt,
      completedAt: new Date().toISOString(),
      cutoverSha: options.cutoverSha,
      pagesRun: options.pagesRun,
      origin: ORIGIN,
      cache,
      fatal: error.stack || String(error),
      chromeStderr: stderr.slice(-4000),
      states: [], staticSurfaces: [], lifecycle: [], assets: [],
      global: {
        consoleProblems: log.consoleProblems,
        failedRequests: log.failedRequests,
        httpProblems: log.httpProblems
      },
      summary: { status: 'fail', assertions: 0, passed: 0, failed: 1, screenshots: 0 }
    };
  } finally {
    if (cdp) cdp.close();
    const exited = new Promise(accept => chrome.once('exit', accept));
    chrome.kill('SIGTERM');
    await Promise.race([exited, new Promise(accept => setTimeout(accept, 2000))]);
    await rm(profile, { recursive: true, force: true }).catch(() => {});
  }

  const resultPath = join(options.output, 'browser-results.json');
  await writeFile(resultPath, JSON.stringify(report, null, 2) + '\n');
  process.stdout.write(JSON.stringify({
    phase: report.phase,
    completedAt: report.completedAt,
    result: resultPath,
    summary: report.summary,
    fatal: report.fatal || null
  }, null, 2) + '\n');
  if (report.summary.status !== 'pass') process.exitCode = 1;
}

await main();
