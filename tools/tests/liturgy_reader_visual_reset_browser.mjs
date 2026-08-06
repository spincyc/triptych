#!/usr/bin/env node

/* Real-Chromium assertions and visual evidence for the shared reader reset. */

import assert from 'node:assert/strict';
import { spawn } from 'node:child_process';
import { createServer } from 'node:http';
import { mkdtemp, mkdir, readFile, stat, writeFile } from 'node:fs/promises';
import { tmpdir } from 'node:os';
import { extname, join, resolve, sep } from 'node:path';
import process from 'node:process';

const ROOT = resolve(process.env.TRIPTYCH_REVIEW_ROOT || resolve(import.meta.dirname, '../..'));
const PREVIEW = '/build/public-alpha/preview/liturgy/';
const DATA = '/build/public-alpha/preview/browse';
const captureAt = process.argv.indexOf('--capture-dir');
const captureDir = captureAt >= 0 ? resolve(process.argv[captureAt + 1]) : null;
const chromeBinary = process.env.TRIPTYCH_CHROME || '/usr/bin/google-chrome-stable';
const failures = [];
const assertions = [];
const consoleProblems = [];
const failedRequests = [];
const httpProblems = [];
const requests = [];

const STATES = Object.freeze({
  romanRead: '#date=2026-08-02&missal=roman-1962&bible=douay-rheims&orations=la&mass=pentecost-10&ordinary=0',
  romanMissal: '#date=2026-08-02&missal=roman-1962&bible=douay-rheims&orations=la&mass=pentecost-10&ordinary=1&ordinary-lang=en&rubrics=1&why=0',
  postRead: '#date=2026-11-29&missal=postconciliar&bible=douay-rheims&orations=la&mass=advent-1&ordinary=0&ordinary-lang=en&eucharistic-prayer=ep-ii',
  postMissal: '#date=2026-11-29&missal=postconciliar&bible=douay-rheims&orations=la&mass=advent-1&ordinary=1&ordinary-lang=en&rubrics=1&eucharistic-prayer=ep-ii',
  partial: '#date=2026-01-01&missal=roman-1962&bible=douay-rheims&orations=la&mass=octava-nativitatis-domini&ordinary=1&ordinary-lang=en&rubrics=1',
  propers: '#missal=roman-1962&type=seasonal&mass=advent-1&bible=douay-rheims&orations=la',
  browse: '#missal=roman-1962&bible=douay-rheims&orations=la'
});

function mime(path) {
  return ({
    '.css': 'text/css; charset=utf-8', '.html': 'text/html; charset=utf-8',
    '.js': 'text/javascript; charset=utf-8', '.json': 'application/json; charset=utf-8',
    '.png': 'image/png', '.svg': 'image/svg+xml', '.pdf': 'application/pdf'
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
    try {
      const url = new URL(request.url, 'http://127.0.0.1');
      const relative = decodeURIComponent(url.pathname).replace(/^\/+/, '');
      if (relative === 'favicon.ico') {
        response.writeHead(204, { 'cache-control': 'no-store' });
        response.end();
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
    }
  });
}

async function freePort() {
  const server = createServer();
  const port = await listen(server);
  await new Promise((accept) => server.close(accept));
  return port;
}

async function waitForJson(url, attempts = 120) {
  for (let attempt = 0; attempt < attempts; attempt += 1) {
    try {
      const response = await fetch(url);
      if (response.ok) return response.json();
    } catch (_error) { /* Chromium is still starting. */ }
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

async function stableFrames(cdp, selector = null) {
  return evaluate(cdp, `(async () => {
    const selector = ${JSON.stringify(selector)};
    let prior = null;
    let stable = 0;
    let frames = 0;
    while (frames < 180) {
      await new Promise(resolve => requestAnimationFrame(resolve));
      frames += 1;
      const node = selector ? document.querySelector(selector) : null;
      const rect = node ? node.getBoundingClientRect() : null;
      const sample = { scrollY, top: rect && rect.top, bottom: rect && rect.bottom };
      if (prior && Math.abs(sample.scrollY - prior.scrollY) <= 0.5 &&
          (!rect || (Math.abs(sample.top - prior.top) <= 0.5 && Math.abs(sample.bottom - prior.bottom) <= 0.5))) {
        stable += 1;
      } else stable = 0;
      prior = sample;
      if (stable >= 5) return { settled: true, stableFrames: stable, frames, sample };
    }
    throw new Error('visual settlement timed out: ' + JSON.stringify({ selector, prior, stable, frames }));
  })()`);
}

async function viewport(cdp, width, height) {
  await cdp.send('Emulation.setDeviceMetricsOverride', {
    width, height, deviceScaleFactor: 1, mobile: width <= 768,
    screenWidth: width, screenHeight: height
  });
}

function prototypeUrl(base, entrance, design, state) {
  const page = entrance === 'day' ? 'reader-visual-reset-day.html' : 'reader-visual-reset-propers.html';
  return `${base}${PREVIEW}${page}?design=${design}&data=${encodeURIComponent(DATA)}${state}`;
}

async function fresh(cdp, target, entrance, selector = null) {
  await cdp.send('Page.navigate', { url: 'about:blank' });
  await waitFor(cdp, `location.href === 'about:blank'`, 'blank document');
  await cdp.send('Page.navigate', { url: target });
  const ready = entrance === 'day' ? 'window.dayReaderReady === true' : 'window.propersReaderReady === true';
  await waitFor(cdp,
    `location.href === ${JSON.stringify(target)} && ${ready} && window.readerVisualResetDebug`,
    `${entrance} visual-reset readiness`);
  return stableFrames(cdp, selector);
}

async function genericFresh(cdp, target, readyExpression) {
  await cdp.send('Page.navigate', { url: 'about:blank' });
  await waitFor(cdp, `location.href === 'about:blank'`, 'blank baseline document');
  await cdp.send('Page.navigate', { url: target });
  const pathname = new URL(target).pathname;
  await waitFor(cdp,
    `location.pathname === ${JSON.stringify(pathname)} && document.readyState === 'complete' && (${readyExpression})`,
    'baseline page readiness');
  return stableFrames(cdp);
}

async function click(cdp, selector) {
  await evaluate(cdp, `(() => {
    const node = document.querySelector(${JSON.stringify(selector)});
    if (!node) throw new Error('missing selector: ' + ${JSON.stringify(selector)});
    node.click();
  })()`);
}

async function escape(cdp) {
  for (const type of ['keyDown', 'keyUp']) {
    await cdp.send('Input.dispatchKeyEvent', {
      type, key: 'Escape', code: 'Escape', windowsVirtualKeyCode: 27, nativeVirtualKeyCode: 27
    });
  }
  await waitFor(cdp, 'document.querySelectorAll("dialog[open]").length === 0', 'surface close');
}

async function shot(cdp, path) {
  const result = await cdp.send('Page.captureScreenshot', {
    format: 'png', captureBeyondViewport: false, fromSurface: true
  });
  await writeFile(path, Buffer.from(result.data, 'base64'));
}

async function check(name, callback) {
  try {
    await callback();
    assertions.push({ name, status: 'pass' });
  } catch (error) {
    failures.push({ name, message: error.stack || String(error) });
    assertions.push({ name, status: 'fail', detail: error.message });
  }
}

async function metrics(cdp) {
  return evaluate(cdp, `(() => {
    const root = document.querySelector('[data-visual-reset]');
    const reading = document.querySelector('#reader-document');
    const identity = document.querySelector('.reader-identity');
    const actions = document.querySelector('.reader-actions');
    const coverage = document.querySelector('#coverage-notice');
    const text = reading.querySelector('.passage, .composed');
    const liturgical = reading.querySelector('.proper, .ordinary-element, .candidate-entry, .candidate-limitation');
    const division = reading.querySelector('.ordinary-division');
    const rect = node => node ? (() => { const r = node.getBoundingClientRect(); return {
      x: Math.round(r.x * 100) / 100, y: Math.round(r.y * 100) / 100,
      width: Math.round(r.width * 100) / 100, height: Math.round(r.height * 100) / 100,
      top: Math.round(r.top * 100) / 100, bottom: Math.round(r.bottom * 100) / 100
    }; })() : null;
    const width = text ? text.getBoundingClientRect().width : reading.getBoundingClientRect().width;
    const font = text ? parseFloat(getComputedStyle(text).fontSize) : 0;
    const approximateCharacters = font ? Math.round(width / (font * 0.49)) : 0;
    const interactive = [...document.querySelectorAll('button, a, input, select, summary')]
      .filter(node => !node.closest('[hidden]') && getComputedStyle(node).display !== 'none' &&
        node.getBoundingClientRect().width > 0 && node.getBoundingClientRect().height > 0)
      .map(node => ({ name: node.getAttribute('aria-label') || node.textContent.trim(), ...rect(node) }));
    const duplicateIds = [...document.querySelectorAll('[id]')].map(node => node.id)
      .filter((id, index, ids) => ids.indexOf(id) !== index);
    const actionStyle = actions ? getComputedStyle(actions) : null;
    const divisionStyle = division ? getComputedStyle(division) : null;
    const divisionLineHeight = divisionStyle ? parseFloat(divisionStyle.lineHeight) : 0;
    const divisionContentHeight = division ? division.getBoundingClientRect().height -
      parseFloat(divisionStyle.paddingTop) - parseFloat(divisionStyle.paddingBottom) -
      parseFloat(divisionStyle.borderTopWidth) - parseFloat(divisionStyle.borderBottomWidth) : 0;
    return {
      href: location.href, hash: location.hash, design: root.dataset.design,
      entrance: root.dataset.entrance, semanticProgress: root.dataset.semanticProgress,
      viewport: { width: innerWidth, height: innerHeight }, scrollY,
      document: { scrollWidth: document.documentElement.scrollWidth,
        clientWidth: document.documentElement.clientWidth,
        scrollHeight: document.documentElement.scrollHeight },
      reading: rect(reading), identity: rect(identity), actions: rect(actions),
      firstLiturgical: rect(liturgical), firstText: rect(text),
      coverage: { hidden: coverage ? coverage.hidden : true, box: rect(coverage),
        text: coverage ? coverage.textContent.trim() : '' },
      absences: {
        directNotices: reading.querySelectorAll('.ordinary-element > .notice').length,
        inlineGroups: reading.querySelectorAll('.ordinary-absence-inline').length,
        inlineNotices: reading.querySelectorAll('.ordinary-absence-inline > .notice').length
      },
      firstDivision: { box: rect(division), text: division ? division.textContent.trim() : '',
        approximateLines: divisionLineHeight ? Math.max(1, Math.round(divisionContentHeight / divisionLineHeight)) : 0 },
      shell: actionStyle ? { background: actionStyle.backgroundColor, borderRadius: actionStyle.borderRadius,
        boxShadow: actionStyle.boxShadow, borderTopWidth: actionStyle.borderTopWidth,
        borderLeftWidth: actionStyle.borderLeftWidth } : null,
      firstTextSample: text ? text.textContent.trim().slice(0, 180) : '',
      text: { fontSize: font, width: Math.round(width * 100) / 100, approximateCharacters },
      interactive, duplicateIds,
      dialogs: [...document.querySelectorAll('dialog[open]')].map(node => node.id),
      activeElement: { tag: document.activeElement.tagName, id: document.activeElement.id,
        label: document.activeElement.getAttribute('aria-label') || document.activeElement.textContent.trim() },
      robots: document.querySelector('meta[name=robots]')?.content || null,
      ready: root.dataset.entrance === 'day' ? dayReaderDebug : propersReaderDebug
    };
  })()`);
}

async function runAssertions(cdp, base) {
  await viewport(cdp, 1440, 900);

  await check('three directions preserve one Roman Day semantic document', async () => {
    const projections = [];
    for (const design of ['folio', 'instrument', 'reader']) {
      const target = prototypeUrl(base, 'day', design, STATES.romanRead);
      await fresh(cdp, target, 'day');
      projections.push(await evaluate(cdp, `({
        design: readerVisualResetDebug.design,
        semantic: dayReaderDebug.semantic.events.map(row => row.id),
        title: document.querySelector('#celebration-title').textContent,
        properCount: document.querySelectorAll('#reader-document .proper').length,
        robots: document.querySelector('meta[name=robots]').content
      })`));
    }
    assert.deepEqual(projections[0].semantic, projections[1].semantic);
    assert.deepEqual(projections[0].semantic, projections[2].semantic);
    assert.equal(new Set(projections.map(row => row.title)).size, 1);
    assert.equal(new Set(projections.map(row => row.properCount)).size, 1);
    projections.forEach(row => assert.match(row.robots, /noindex/));
  });

  await check('directions are materially distinct compositions, not palette aliases', async () => {
    const layouts = [];
    for (const design of ['folio', 'instrument', 'reader']) {
      await fresh(cdp, prototypeUrl(base, 'day', design, STATES.romanMissal), 'day');
      layouts.push(await evaluate(cdp, `(() => {
        const root = document.querySelector('[data-visual-reset]');
        const title = document.querySelector('.celebration-title');
        const action = document.querySelector('.reader-actions');
        const element = document.querySelector('.ordinary-element');
        return { design: root.dataset.design, background: getComputedStyle(root).backgroundColor,
          titleFamily: getComputedStyle(title).fontFamily,
          action: getComputedStyle(action).gridTemplateColumns,
          element: getComputedStyle(element).display };
      })()`));
    }
    assert.equal(new Set(layouts.map(row => row.background)).size, 3);
    assert.notEqual(layouts[0].titleFamily, layouts[1].titleFamily);
    assert.notEqual(layouts[0].element, layouts[1].element);
    assert.notEqual(layouts[1].action, layouts[2].action);
  });

  await check('Day Read and Missal retain real production state and event identity', async () => {
    for (const [state, mode] of [[STATES.romanRead, 'read'], [STATES.romanMissal, 'missal'],
      [STATES.postRead, 'read'], [STATES.postMissal, 'missal']]) {
      await fresh(cdp, prototypeUrl(base, 'day', 'instrument', state), 'day');
      const value = await evaluate(cdp, `({ mode: dayReaderDebug.mode,
        events: dayReaderDebug.semantic.events.length,
        properCount: document.querySelectorAll('#reader-document .proper').length,
        ordinaryCount: document.querySelectorAll('#reader-document .ordinary-element').length,
        outcome: dayReaderDebug.outcome })`);
      assert.equal(value.mode, mode);
      assert.equal(value.outcome, 'ready');
      assert.ok(value.events > 5);
      assert.ok(value.properCount > 0);
      if (mode === 'missal') assert.ok(value.ordinaryCount > 10);
      else assert.equal(value.ordinaryCount, 0);
    }
  });

  await check('Propers ready and Browse states share the visual foundation without defaults', async () => {
    await fresh(cdp, prototypeUrl(base, 'propers', 'reader', STATES.propers), 'propers');
    let value = await evaluate(cdp, `({ outcome: propersReaderDebug.outcome,
      properCount: document.querySelectorAll('#reader-document .proper').length,
      modes: [...document.querySelectorAll('[data-mode]')].map(node => node.dataset.mode) })`);
    assert.equal(value.outcome, 'ready');
    assert.ok(value.properCount > 5);
    assert.deepEqual(value.modes, ['read']);
    await fresh(cdp, prototypeUrl(base, 'propers', 'reader', STATES.browse), 'propers');
    value = await evaluate(cdp, `({ outcome: propersReaderDebug.outcome,
      selected: document.querySelector('#reader-formulary').value,
      dialog: document.querySelector('#browse-surface').open,
      results: document.querySelectorAll('.browse-result').length })`);
    assert.equal(value.outcome, 'browse');
    assert.equal(value.selected, '');
    assert.equal(value.dialog, true);
    assert.ok(value.results > 2);
  });

  await check('persistent shell stays one action away and restores focus at deep scroll', async () => {
    await fresh(cdp, prototypeUrl(base, 'day', 'folio', STATES.romanMissal), 'day');
    await evaluate(cdp, `document.querySelector('#reader-document .proper:last-of-type').scrollIntoView({block:'center'})`);
    await stableFrames(cdp, '#reader-document .proper:last-of-type');
    const before = await evaluate(cdp, 'scrollY');
    await click(cdp, '[data-reader-action="contents"]');
    await waitFor(cdp, 'document.querySelector("#contents-surface").open', 'Contents surface');
    assert.equal(await evaluate(cdp, 'document.activeElement.getAttribute("aria-label")'), 'Close Contents');
    await escape(cdp);
    const after = await evaluate(cdp, 'scrollY');
    assert.ok(Math.abs(after - before) <= 2, `${before} -> ${after}`);
    assert.equal(await evaluate(cdp, 'document.activeElement.dataset.readerAction'), 'contents');
  });

  await check('Read and Missal mode switching keeps semantic location and focus behavior', async () => {
    await fresh(cdp, prototypeUrl(base, 'day', 'reader', STATES.postRead), 'day');
    const selector = '[data-semantic-event-id="proper/postconciliar/advent-1/007"]';
    await evaluate(cdp, `document.querySelector(${JSON.stringify(selector)}).scrollIntoView({block:'center'})`);
    await stableFrames(cdp, selector);
    const generation = await evaluate(cdp, 'dayReaderDebug.committedRender.generation');
    await click(cdp, '[data-reader-action="mode"]');
    await click(cdp, '[data-mode="missal"]');
    await waitFor(cdp, `dayReaderDebug.ready && dayReaderDebug.mode === 'missal' &&
      dayReaderDebug.committedRender.generation > ${generation}`, 'Missal transition');
    await stableFrames(cdp, selector);
    const value = await evaluate(cdp, `(() => {
      const rect = document.querySelector(${JSON.stringify(selector)}).getBoundingClientRect();
      return { top: rect.top, bottom: rect.bottom, viewportHeight: innerHeight, mode: dayReaderDebug.mode,
        focus: document.activeElement.dataset.readerAction };
    })()`);
    assert.equal(value.mode, 'missal');
    assert.ok(value.bottom > 0 && value.top < value.viewportHeight);
    assert.equal(value.focus, 'mode');
  });

  await check('partial coverage stays explicit and subordinate to held text', async () => {
    await fresh(cdp, prototypeUrl(base, 'day', 'folio', STATES.partial), 'day');
    const value = await evaluate(cdp, `({ notice: document.querySelector('#coverage-notice').textContent,
      hidden: document.querySelector('#coverage-notice').hidden,
      text: document.querySelectorAll('#reader-document .composed, #reader-document .passage').length,
      noticeTop: document.querySelector('#coverage-notice').getBoundingClientRect().top,
      firstTextTop: document.querySelector('#reader-document .composed, #reader-document .passage').getBoundingClientRect().top })`);
    assert.equal(value.hidden, false);
    assert.match(value.notice, /partial|unavailable|not held/i);
    assert.ok(value.text > 3);
    assert.ok(value.noticeTop < value.firstTextTop);
  });

  await check('Instrument consolidates exact partial and postconciliar absences', async () => {
    await viewport(cdp, 393, 852);
    await fresh(cdp, prototypeUrl(base, 'day', 'instrument', STATES.partial), 'day');
    let value = await evaluate(cdp, `({
      coverage: document.querySelector('#coverage-notice').textContent.trim(),
      uncompiled: document.querySelectorAll('#reader-document > .uncompiled').length,
      held: document.querySelectorAll('#reader-document .composed, #reader-document .passage').length
    })`);
    assert.match(value.coverage, /not yet transcribed/i);
    assert.equal(value.uncompiled, 0);
    assert.ok(value.held > 3);

    await fresh(cdp, prototypeUrl(base, 'day', 'instrument', STATES.postMissal), 'day');
    value = await evaluate(cdp, `({
      direct: document.querySelectorAll('.ordinary-element > .notice').length,
      groups: document.querySelectorAll('.ordinary-absence-inline').length,
      notices: document.querySelectorAll('.ordinary-absence-inline > .notice').length,
      held: document.querySelectorAll('#reader-document .composed, #reader-document .passage').length
    })`);
    assert.equal(value.direct, 0);
    assert.ok(value.groups > 3);
    assert.ok(value.notices >= value.groups);
    assert.ok(value.held > 3);
  });

  await check('320px reflow has no horizontal overflow or undersized dock targets', async () => {
    await viewport(cdp, 320, 852);
    for (const design of ['folio', 'instrument', 'reader']) {
      await fresh(cdp, prototypeUrl(base, 'day', design, STATES.romanMissal), 'day');
      const value = await metrics(cdp);
      assert.ok(value.document.scrollWidth <= value.document.clientWidth + 1);
      value.interactive.filter(node => ['Date', 'Contents', 'ModeRead', 'Details'].some(label => node.name.replace(/\s/g, '').includes(label)))
        .forEach(node => assert.ok(node.height >= 44, `${node.name}: ${node.height}`));
      assert.deepEqual(value.duplicateIds, []);
    }
  });

  await check('200% text enlargement retains one readable plane and usable surfaces', async () => {
    await viewport(cdp, 393, 852);
    await fresh(cdp, prototypeUrl(base, 'day', 'instrument', STATES.postMissal), 'day');
    await evaluate(cdp, `document.documentElement.style.fontSize = '200%'`);
    await stableFrames(cdp);
    await click(cdp, '[data-reader-action="details"]');
    await waitFor(cdp, 'document.querySelector("#details-surface").open', 'enlarged Details');
    const value = await evaluate(cdp, `({ page: document.documentElement.scrollWidth - document.documentElement.clientWidth,
      surface: document.querySelector('#details-surface').scrollWidth - document.querySelector('#details-surface').clientWidth,
      close: document.querySelector('#details-surface [data-reader-close]').getBoundingClientRect().width })`);
    assert.ok(value.page <= 1);
    assert.ok(value.surface <= 1);
    assert.ok(value.close >= 44);
    await escape(cdp);
    await evaluate(cdp, `document.documentElement.style.fontSize = ''`);
  });

  await check('400% browser scale keeps the compact reader operable', async () => {
    await viewport(cdp, 393, 852);
    await fresh(cdp, prototypeUrl(base, 'day', 'reader', STATES.romanRead), 'day');
    await cdp.send('Emulation.setPageScaleFactor', { pageScaleFactor: 4 });
    await stableFrames(cdp);
    const value = await evaluate(cdp, `({
      overflow: document.documentElement.scrollWidth - document.documentElement.clientWidth,
      actions: [...document.querySelectorAll('.reader-actions button')].map(node => ({
        label: node.getAttribute('aria-label') || node.textContent.trim(),
        width: node.getBoundingClientRect().width, height: node.getBoundingClientRect().height
      }))
    })`);
    assert.ok(value.overflow <= 1);
    assert.equal(value.actions.length, 4);
    value.actions.forEach(node => assert.ok(node.width > 0 && node.height > 0, node.label));
    await cdp.send('Emulation.setPageScaleFactor', { pageScaleFactor: 1 });
  });

  await check('forced colors, reduced motion, and keyboard focus remain explicit', async () => {
    await cdp.send('Emulation.setEmulatedMedia', { media: 'screen', features: [
      { name: 'forced-colors', value: 'active' },
      { name: 'prefers-reduced-motion', value: 'reduce' }
    ] });
    await viewport(cdp, 393, 852);
    await fresh(cdp, prototypeUrl(base, 'propers', 'reader', STATES.propers), 'propers');
    await click(cdp, '[data-reader-action="details"]');
    await waitFor(cdp, 'document.querySelector("#details-surface").open', 'forced-color Details');
    const value = await evaluate(cdp, `({ close: document.querySelector('#details-surface [data-reader-close]').getBoundingClientRect().width,
      reduced: matchMedia('(prefers-reduced-motion: reduce)').matches,
      forced: matchMedia('(forced-colors: active)').matches,
      focus: document.activeElement.getAttribute('aria-label') })`);
    assert.equal(value.reduced, true);
    assert.equal(value.forced, true);
    assert.ok(value.close >= 44);
    assert.equal(value.focus, 'Close Details');
    await escape(cdp);
    await cdp.send('Emulation.setEmulatedMedia', { media: 'screen' });
  });

  await check('prototype resources remain local and network-clean', async () => {
    const external = requests.filter(url => !url.startsWith(base) && !url.startsWith('about:'));
    assert.deepEqual(external, []);
    assert.deepEqual(consoleProblems, []);
    assert.deepEqual(failedRequests.filter(row => !row.canceled), []);
    assert.deepEqual(httpProblems, []);
  });
}

async function captureOne(cdp, base, directory, row) {
  const { file, entrance, design, state, width, height, action = null, deep = false,
    enlargement = false, media = null, keyboard = false } = row;
  await viewport(cdp, width, height);
  if (media) await cdp.send('Emulation.setEmulatedMedia', { media: 'screen', features: media });
  const target = prototypeUrl(base, entrance, design, STATES[state]);
  await fresh(cdp, target, entrance);
  if (enlargement) {
    await evaluate(cdp, `document.documentElement.style.fontSize = '200%'`);
    await stableFrames(cdp);
  }
  if (deep) {
    const selector = entrance === 'day' ? '#reader-document .proper:last-of-type' : '#reader-document .proper:last-of-type';
    await evaluate(cdp, `document.querySelector(${JSON.stringify(selector)}).scrollIntoView({block:'center'})`);
    await stableFrames(cdp, selector);
  }
  if (action) {
    await click(cdp, `[data-reader-action="${action}"]`);
    await waitFor(cdp, `document.querySelector('[data-reader-surface="${action}"]').open`, `${action} surface`);
    await stableFrames(cdp);
  }
  if (keyboard) {
    if (!action) {
      await click(cdp, '[data-reader-action="contents"]');
      await waitFor(cdp, 'document.querySelector("#contents-surface").open', 'keyboard Contents');
    }
    await cdp.send('Input.dispatchKeyEvent', { type: 'keyDown', key: 'Tab', code: 'Tab', windowsVirtualKeyCode: 9 });
    await cdp.send('Input.dispatchKeyEvent', { type: 'keyUp', key: 'Tab', code: 'Tab', windowsVirtualKeyCode: 9 });
  }
  await stableFrames(cdp);
  await shot(cdp, join(directory, file));
  const measured = await metrics(cdp);
  if (action || keyboard) await escape(cdp);
  if (enlargement) await evaluate(cdp, `document.documentElement.style.fontSize = ''`);
  if (media) await cdp.send('Emulation.setEmulatedMedia', { media: 'screen' });
  return { ...row, target, measured,
    consoleErrors: consoleProblems.length, failedRequests: failedRequests.filter(one => !one.canceled).length,
    httpErrors: httpProblems.length };
}

async function captureMatrix(cdp, base, directory) {
  await mkdir(directory, { recursive: true });
  const rows = [];
  for (const design of ['folio', 'instrument', 'reader']) {
    const prefix = `visual-reset-${design}`;
    rows.push(
      { file: `${prefix}-day-roman-read-1440x900.png`, entrance: 'day', design, state: 'romanRead', width: 1440, height: 900 },
      { file: `${prefix}-day-roman-read-393x852.png`, entrance: 'day', design, state: 'romanRead', width: 393, height: 852 },
      { file: `${prefix}-day-roman-missal-1440x900.png`, entrance: 'day', design, state: 'romanMissal', width: 1440, height: 900 },
      { file: `${prefix}-day-roman-missal-393x852.png`, entrance: 'day', design, state: 'romanMissal', width: 393, height: 852 },
      { file: `${prefix}-propers-advent-1-1440x900.png`, entrance: 'propers', design, state: 'propers', width: 1440, height: 900 },
      { file: `${prefix}-propers-advent-1-393x852.png`, entrance: 'propers', design, state: 'propers', width: 393, height: 852 },
      { file: `${prefix}-day-missal-deep-1440x900.png`, entrance: 'day', design, state: 'romanMissal', width: 1440, height: 900, deep: true },
      { file: `${prefix}-propers-browse-1440x900.png`, entrance: 'propers', design, state: 'browse', width: 1440, height: 900 },
      { file: `${prefix}-day-contents-393x852.png`, entrance: 'day', design, state: 'romanMissal', width: 393, height: 852, action: 'contents' },
      { file: `${prefix}-day-partial-393x852.png`, entrance: 'day', design, state: 'partial', width: 393, height: 852 }
    );
  }

  const detailed = [
    ['instrument-day-read-1024x768.png', 'day', 'romanRead', 1024, 768, {}],
    ['instrument-day-read-768x1024.png', 'day', 'romanRead', 768, 1024, {}],
    ['instrument-day-missal-320x852.png', 'day', 'romanMissal', 320, 852, {}],
    ['instrument-day-missal-200-percent-393x852.png', 'day', 'romanMissal', 393, 852, { enlargement: true }],
    ['instrument-day-forced-colors-393x852.png', 'day', 'romanRead', 393, 852, { media: [{ name: 'forced-colors', value: 'active' }] }],
    ['instrument-day-reduced-motion-393x852.png', 'day', 'romanMissal', 393, 852, { media: [{ name: 'prefers-reduced-motion', value: 'reduce' }] }],
    ['instrument-day-keyboard-focus-393x852.png', 'day', 'romanRead', 393, 852, { keyboard: true }],
    ['instrument-day-long-missal-deep-1440x900.png', 'day', 'romanMissal', 1440, 900, { deep: true }],
    ['instrument-day-postconciliar-read-1440x900.png', 'day', 'postRead', 1440, 900, {}],
    ['instrument-day-postconciliar-missal-1440x900.png', 'day', 'postMissal', 1440, 900, {}],
    ['instrument-day-postconciliar-missal-393x852.png', 'day', 'postMissal', 393, 852, {}],
    ['instrument-day-date-open-1024x768.png', 'day', 'romanRead', 1024, 768, { action: 'date' }],
    ['instrument-day-mode-open-393x852.png', 'day', 'romanRead', 393, 852, { action: 'mode' }],
    ['instrument-day-details-open-1440x900.png', 'day', 'postMissal', 1440, 900, { action: 'details' }],
    ['instrument-propers-browse-393x852.png', 'propers', 'browse', 393, 852, {}]
  ];
  detailed.forEach(([file, entrance, state, width, height, extras]) => rows.push({
    file, entrance, design: 'instrument', state, width, height, ...extras
  }));

  const evidence = [];
  for (const row of rows) evidence.push(await captureOne(cdp, base, directory, row));

  const deployed = 'https://spincyc.github.io/triptych/liturgy/';
  const baselines = [
    ['current-day', deployed + 'day.html', STATES.romanRead,
      '!document.querySelector("#celebration-title").textContent.includes("Loading") && document.querySelector("#reading").textContent.length > 100'],
    ['current-propers', deployed + 'index.html', STATES.propers,
      '!document.querySelector("#formulary-title").textContent.includes("Loading") && document.querySelector("#reading").textContent.length > 100'],
    ['accepted-day', deployed + 'day-reader.html', STATES.romanRead, 'window.dayReaderReady === true'],
    ['accepted-propers', deployed + 'propers-reader.html', STATES.propers, 'window.propersReaderReady === true']
  ];
  for (const [name, page, state, ready] of baselines) {
    for (const [width, height] of [[1440, 900], [393, 852]]) {
      await viewport(cdp, width, height);
      const target = `${page}${state}`;
      await genericFresh(cdp, target, ready);
      const file = `before-${name}-${width}x${height}.png`;
      await shot(cdp, join(directory, file));
      evidence.push({ file, baseline: name, target, width, height,
        measured: await evaluate(cdp, `({ href: location.href, viewport: {width: innerWidth, height: innerHeight},
          scrollWidth: document.documentElement.scrollWidth, clientWidth: document.documentElement.clientWidth })`) });
    }
  }

  await viewport(cdp, 1024, 768);
  await fresh(cdp, prototypeUrl(base, 'day', 'instrument', STATES.romanMissal), 'day');
  await cdp.send('Emulation.setEmulatedMedia', { media: 'print' });
  const pdf = await cdp.send('Page.printToPDF', {
    printBackground: true, preferCSSPageSize: true, paperWidth: 8.5, paperHeight: 11,
    marginTop: 0.4, marginBottom: 0.4, marginLeft: 0.45, marginRight: 0.45
  });
  await cdp.send('Emulation.setEmulatedMedia', { media: 'screen' });
  await writeFile(join(directory, 'visual-reset-instrument-print-smoke.pdf'), Buffer.from(pdf.data, 'base64'));
  await writeFile(join(directory, 'capture-metadata.json'), JSON.stringify(evidence, null, 2) + '\n');
  return evidence;
}

async function main() {
  const server = staticServer();
  const serverPort = await listen(server);
  const base = `http://127.0.0.1:${serverPort}`;
  const debugPort = await freePort();
  const profile = await mkdtemp(join(tmpdir(), 'triptych-visual-reset-chrome-'));
  const chrome = spawn(chromeBinary, [
    '--headless=new', '--no-sandbox', '--disable-dev-shm-usage', '--disable-gpu',
    `--remote-debugging-port=${debugPort}`, `--user-data-dir=${profile}`,
    '--no-first-run', '--no-default-browser-check', 'about:blank'
  ], { stdio: ['ignore', 'ignore', 'pipe'] });
  let chromeStderr = '';
  chrome.stderr.on('data', chunk => { chromeStderr += chunk.toString(); });
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
      if (['error', 'warning'].includes(type)) consoleProblems.push({
        type, text: args.map(arg => arg.value || arg.description || '').join(' ')
      });
    });
    cdp.on('Network.requestWillBeSent', ({ request }) => requests.push(request.url));
    cdp.on('Network.loadingFailed', event => failedRequests.push({
      error: event.errorText, canceled: Boolean(event.canceled), requestId: event.requestId
    }));
    cdp.on('Network.responseReceived', ({ response: held }) => {
      if (held.status >= 400) httpProblems.push({ status: held.status, url: held.url });
    });

    await runAssertions(cdp, base);
    const captures = captureDir ? await captureMatrix(cdp, base, captureDir) : [];
    const ax = await cdp.send('Accessibility.getFullAXTree');
    const unnamed = ax.nodes.filter(node =>
      ['button', 'link', 'radio', 'textbox'].includes(node.role?.value) && !node.name?.value
    );
    const report = {
      generatedAt: new Date().toISOString(),
      chrome: (await waitForJson(`http://127.0.0.1:${debugPort}/json/version`)).Browser,
      assertions, failures, consoleProblems, failedRequests, httpProblems,
      accessibility: { nodeCount: ax.nodes.length, unnamedInteractiveNodes: unnamed.length },
      captures: captures.length,
      sizes: {
        javascript: (await stat(join(ROOT, 'src/web/browser/liturgy/reader-visual-reset.js'))).size,
        css: (await stat(join(ROOT, 'src/web/browser/liturgy/reader-visual-reset.css'))).size,
        dayHtml: (await stat(join(ROOT, 'src/web/browser/liturgy/reader-visual-reset-day.html'))).size,
        propersHtml: (await stat(join(ROOT, 'src/web/browser/liturgy/reader-visual-reset-propers.html'))).size
      }
    };
    if (captureDir) await writeFile(join(captureDir, 'browser-results.json'), JSON.stringify(report, null, 2) + '\n');
    process.stdout.write(JSON.stringify(report, null, 2) + '\n');
    if (failures.length || consoleProblems.length || failedRequests.filter(one => !one.canceled).length ||
        httpProblems.length || unnamed.length) process.exitCode = 1;
  } catch (error) {
    process.stderr.write((error.stack || String(error)) + '\n' + chromeStderr.slice(-4000));
    process.exitCode = 1;
  } finally {
    if (cdp) cdp.close();
    chrome.kill('SIGTERM');
    await new Promise(accept => server.close(accept));
  }
}

await main();
