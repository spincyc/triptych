#!/usr/bin/env node

/* Real-Chromium interaction and measured-review harness for the W2 prototype. */

import assert from 'node:assert/strict';
import { spawn } from 'node:child_process';
import { createServer } from 'node:http';
import { mkdtemp, mkdir, readFile, stat, writeFile } from 'node:fs/promises';
import { tmpdir } from 'node:os';
import { extname, join, resolve, sep } from 'node:path';
import process from 'node:process';

const ROOT = resolve(process.env.TRIPTYCH_REVIEW_ROOT || resolve(import.meta.dirname, '../..'));
const ROUTE = '/src/web/browser/liturgy/prototypes/reader-shell/index.html';
const captureAt = process.argv.indexOf('--capture-dir');
const captureDir = captureAt >= 0 ? resolve(process.argv[captureAt + 1]) : null;
const correctionAt = process.argv.indexOf('--correction-dir');
const correctionDir = correctionAt >= 0 ? resolve(process.argv[correctionAt + 1]) : null;
const beforeAt = process.argv.indexOf('--before-dir');
const beforeDir = beforeAt >= 0 ? resolve(process.argv[beforeAt + 1]) : null;
const chromeBinary = process.env.TRIPTYCH_CHROME || '/usr/bin/google-chrome-stable';
const failures = [];
const observations = [];
const consoleProblems = [];
const failedRequests = [];
const httpProblems = [];

function mime(path) {
  return ({
    '.css': 'text/css; charset=utf-8',
    '.html': 'text/html; charset=utf-8',
    '.js': 'text/javascript; charset=utf-8',
    '.json': 'application/json; charset=utf-8',
    '.svg': 'image/svg+xml'
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
        'content-type': mime(file),
        'cache-control': 'no-store',
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

async function waitForJson(url, attempts = 80) {
  for (let attempt = 0; attempt < attempts; attempt += 1) {
    try {
      const response = await fetch(url);
      if (response.ok) return await response.json();
    } catch (_error) {
      // Chromium's debugging endpoint is not ready yet.
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
      }, 15000);
      this.pending.set(id, { accept, reject, timer });
      this.socket.send(JSON.stringify({ id, method, params }));
    });
  }

  close() {
    this.socket.close();
  }
}

async function evaluate(cdp, expression, awaitPromise = true) {
  const result = await cdp.send('Runtime.evaluate', {
    expression,
    awaitPromise,
    returnByValue: true,
    userGesture: true
  });
  if (result.exceptionDetails) {
    throw new Error(result.exceptionDetails.exception?.description || result.exceptionDetails.text);
  }
  return result.result.value;
}

async function waitFor(cdp, expression, label, attempts = 120) {
  for (let attempt = 0; attempt < attempts; attempt += 1) {
    if (await evaluate(cdp, `Boolean(${expression})`)) return;
    await new Promise((accept) => setTimeout(accept, 50));
  }
  throw new Error('Timed out waiting for ' + label);
}

async function viewport(cdp, width, height, scale = 1) {
  await cdp.send('Emulation.setDeviceMetricsOverride', {
    width, height, deviceScaleFactor: scale, mobile: width <= 768,
    screenWidth: width, screenHeight: height
  });
}

function url(base, state, shell, extras = '') {
  return `${base}${ROUTE}?state=${state}&shell=${shell}&data=/build/public-alpha/preview/browse${extras}`;
}

async function navigate(cdp, target) {
  await cdp.send('Page.navigate', { url: target });
  await waitFor(cdp,
    `location.href === ${JSON.stringify(target)} && window.readerShellReady === true`,
    'reader shell readiness');
  await new Promise((accept) => setTimeout(accept, 80));
}

async function click(cdp, selector) {
  return evaluate(cdp, `(() => {
    const element = document.querySelector(${JSON.stringify(selector)});
    if (!element) throw new Error('missing selector: ' + ${JSON.stringify(selector)});
    element.click();
    return true;
  })()`);
}

async function escape(cdp) {
  await cdp.send('Input.dispatchKeyEvent', {
    type: 'keyDown', key: 'Escape', code: 'Escape', windowsVirtualKeyCode: 27,
    nativeVirtualKeyCode: 27
  });
  await cdp.send('Input.dispatchKeyEvent', {
    type: 'keyUp', key: 'Escape', code: 'Escape', windowsVirtualKeyCode: 27,
    nativeVirtualKeyCode: 27
  });
  await new Promise((accept) => setTimeout(accept, 40));
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
    observations.push({ name, status: 'pass' });
  } catch (error) {
    failures.push({ name, message: error.stack || String(error) });
    observations.push({ name, status: 'fail', detail: error.message });
  }
}

async function surfaceOverflow(cdp, surface) {
  return evaluate(cdp, `(() => {
    const root = document.querySelector('#${surface}-surface');
    const nodes = [root, ...root.querySelectorAll(
      '.surface-head, .surface-body, .surface-fields, .surface-field, .date-steps, .browse-list, ' +
      '.mode-options, .study-panel section, input, select, button, dl, dd, li'
    )];
    return nodes.map((element) => ({
      name: element.id || element.className || element.tagName,
      scrollWidth: element.scrollWidth,
      clientWidth: element.clientWidth
    })).filter((entry) => entry.scrollWidth > entry.clientWidth + 1);
  })()`);
}

async function runAssertions(cdp, base) {
  await viewport(cdp, 393, 852);
  await navigate(cdp, url(base, 'day-read', 'persistent'));

  await test('default is shared Day Read shell with four labelled actions', async () => {
    const value = await evaluate(cdp, `(() => ({
      current: ReaderShellPrototype.current(),
      labels: [...document.querySelectorAll('#global-actions button')].map(b =>
        [...b.querySelectorAll('span:not(.action-mark):not(.action-state)')]
          .map(span => span.textContent.trim()).join(' ')),
      properCount: document.querySelectorAll('#reader-document .proper').length,
      contentsCount: document.querySelectorAll('#semantic-contents button').length,
      robots: document.querySelector('meta[name=robots]').content
    }))()`);
    assert.equal(value.current.entrance, 'day');
    assert.equal(value.current.mode, 'read');
    assert.equal(value.current.selections.edition, 'roman-1962');
    assert.deepEqual(value.labels, ['Date & edition', 'Contents', 'Mode', 'Details']);
    assert.ok(value.properCount >= 8, 'real Proper renderer did not produce enough sections');
    assert.equal(value.properCount, value.contentsCount);
    assert.match(value.robots, /noindex/);
  });

  await test('complete Read states omit diagnostic notices while reliance states retain them', async () => {
    let value = await evaluate(cdp, `(() => ({
      hidden: document.querySelector('#reader-coverage').hidden,
      text: document.querySelector('#reader-coverage').textContent,
      meta: document.querySelector('#reader-meta').textContent,
      firstTop: document.querySelector('#reader-document .proper').getBoundingClientRect().top
    }))()`);
    assert.equal(value.hidden, true);
    assert.equal(value.text, '');
    assert.equal(/bound M1|explicitly selected|No blocking notices|contract/i.test(value.meta), false);
    assert.match(value.meta, /1962 Roman Missal · Universal · Douay–Rheims · Latin orations/);
    assert.ok(value.firstTop < 255, `first content remains at ${value.firstTop}px`);

    await navigate(cdp, url(base, 'unavailable', 'persistent'));
    value = await evaluate(cdp, `({
      hidden: document.querySelector('#reader-coverage').hidden,
      text: document.querySelector('#reader-coverage').textContent
    })`);
    assert.equal(value.hidden, false);
    assert.match(value.text, /partial or unavailable/i);

    await navigate(cdp, url(base, 'day-read', 'persistent', '&display=original&bible=clementine-vulgate'));
    value = await evaluate(cdp, `({
      hidden: document.querySelector('#reader-coverage').hidden,
      text: document.querySelector('#reader-coverage').textContent
    })`);
    assert.equal(value.hidden, false);
    assert.match(value.text, /does not match.*Bible edition/i);
  });

  await test('Propers uses the same shell and changes only the entrance action', async () => {
    await navigate(cdp, url(base, 'propers-formulary', 'persistent'));
    const value = await evaluate(cdp, `(() => ({
      current: ReaderShellPrototype.current(),
      shellCount: document.querySelectorAll('#reader-shell').length,
      label: document.querySelector('#entrance-action-label').textContent,
      properCount: document.querySelectorAll('#reader-document .proper').length
    }))()`);
    assert.equal(value.current.entrance, 'propers');
    assert.equal(value.shellCount, 1);
    assert.equal(value.label, 'Browse & edition');
    assert.ok(value.properCount >= 8);
  });

  await test('every auxiliary surface preserves scroll and focus; Escape closes it', async () => {
    await navigate(cdp, url(base, 'day-read', 'persistent'));
    for (const surface of ['entrance', 'contents', 'mode', 'study']) {
      await evaluate(cdp, `window.scrollTo(0, document.querySelectorAll('[data-semantic-location]')[5].offsetTop)`);
      await new Promise((accept) => setTimeout(accept, 50));
      const before = await evaluate(cdp, 'window.scrollY');
      await click(cdp, `[data-surface="${surface}"]`);
      const opened = await evaluate(cdp, `(() => ({
        surface: ReaderShellPrototype.current().surface,
        activeInside: document.querySelector('#${surface}-surface').contains(document.activeElement),
        y: window.scrollY,
        modalCount: document.querySelectorAll('dialog[open]').length
      }))()`);
      assert.equal(opened.surface, surface);
      assert.equal(opened.activeInside, true);
      assert.equal(opened.modalCount, 1);
      assert.ok(Math.abs(opened.y - before) <= 1, `${surface} moved the reading position while opening`);
      await escape(cdp);
      const closed = await evaluate(cdp, `(() => ({
        open: document.querySelectorAll('dialog[open]').length,
        focused: document.activeElement === document.querySelector('[data-surface="${surface}"]'),
        y: window.scrollY
      }))()`);
      assert.equal(closed.open, 0);
      assert.equal(closed.focused, true);
      assert.ok(Math.abs(closed.y - before) <= 1, `${surface} did not restore scroll`);
    }
  });

  await test('only one auxiliary surface can be open', async () => {
    await evaluate(cdp, `ReaderShellPrototype.open('contents', document.querySelector('[data-surface="contents"]'))`);
    await evaluate(cdp, `ReaderShellPrototype.open('study', document.querySelector('[data-surface="study"]'))`);
    const value = await evaluate(cdp, `({
      count: document.querySelectorAll('dialog[open]').length,
      id: document.querySelector('dialog[open]')?.id,
      current: ReaderShellPrototype.current().surface
    })`);
    assert.deepEqual(value, { count: 1, id: 'study-surface', current: 'study' });
    await escape(cdp);
  });

  await test('Contents follows and moves to the active semantic location', async () => {
    await evaluate(cdp, `window.scrollTo(0, document.querySelectorAll('[data-semantic-location]')[5].offsetTop + 20)`);
    await new Promise((accept) => setTimeout(accept, 100));
    await click(cdp, '[data-surface="contents"]');
    const current = await evaluate(cdp, `document.querySelector('#semantic-contents [aria-current="location"]')?.dataset.location`);
    assert.match(current, /^unit-0[5-7]-/);
    await click(cdp, '#semantic-contents button:last-child');
    const moved = await evaluate(cdp, `(() => ({
      location: ReaderShellPrototype.current().location,
      focused: document.activeElement.closest('[data-semantic-location]')?.dataset.semanticLocation,
      open: document.querySelectorAll('dialog[open]').length,
      selectedVisible: document.querySelector('#unit-10-postcommunion').getBoundingClientRect().top < innerHeight
    }))()`);
    assert.equal(moved.focused, 'unit-10-postcommunion');
    assert.equal(moved.selectedVisible, true);
    assert.equal(moved.open, 0);
  });

  await test('persistent and reveal variants remain reachable at deep scroll', async () => {
    for (const variant of ['persistent', 'reveal']) {
      await navigate(cdp, url(base, 'day-missal', variant));
      await evaluate(cdp, 'window.scrollTo(0, document.documentElement.scrollHeight)');
      await new Promise((accept) => setTimeout(accept, 120));
      const state = await evaluate(cdp, `(() => {
        const actions = document.querySelector('#global-actions');
        const reveal = document.querySelector('#shell-reveal');
        const visible = e => !e.hidden && getComputedStyle(e).display !== 'none' && e.getBoundingClientRect().height > 0;
        return { actions: visible(actions), reveal: visible(reveal), shell: ReaderShellPrototype.current().shell };
      })()`);
      assert.equal(state.shell, variant);
      assert.equal(state.actions || state.reveal, true, `${variant} has no deep-scroll affordance`);
      if (variant === 'reveal' && state.reveal) {
        await click(cdp, '#shell-reveal');
        assert.equal(await evaluate(cdp, '!document.querySelector("#global-actions").closest("#reader-shell").classList.contains("shell-hidden")'), true);
      }
    }
  });

  await test('URL mode preserves semantic location and Back restores state', async () => {
    await navigate(cdp, url(base, 'day-read', 'persistent'));
    await evaluate(cdp, `window.scrollTo(0, document.querySelectorAll('[data-semantic-location]')[4].offsetTop)`);
    await new Promise((accept) => setTimeout(accept, 80));
    const location = await evaluate(cdp, 'ReaderShellPrototype.current().location');
    await click(cdp, '[data-surface="mode"]');
    await click(cdp, '[data-mode="study"]');
    await waitFor(cdp, `ReaderShellPrototype.current().mode === "study" && ReaderShellPrototype.current().location === ${JSON.stringify(location)}`, 'Study mode and location');
    await evaluate(cdp, 'history.back()');
    await waitFor(cdp, `ReaderShellPrototype.current().mode === "read" && ReaderShellPrototype.current().location === ${JSON.stringify(location)}`, 'Back to Read and location');
    await evaluate(cdp, 'history.forward()');
    await waitFor(cdp, `ReaderShellPrototype.current().mode === "study" && ReaderShellPrototype.current().location === ${JSON.stringify(location)}`, 'Forward to Study and location');
  });

  await test('Details and Study mode have distinct temporary, pinned, and mobile behavior', async () => {
    await viewport(cdp, 1440, 900);
    await navigate(cdp, url(base, 'day-read', 'persistent'));
    const readWidth = await evaluate(cdp, `document.querySelector('#reader-document').getBoundingClientRect().width`);
    await click(cdp, '[data-surface="study"]');
    let value = await evaluate(cdp, `(() => ({
      mode: ReaderShellPrototype.current().mode,
      presentation: ReaderShellPrototype.current().surfacePresentation,
      modal: document.querySelector('#study-surface').matches(':modal'),
      action: document.querySelector('[data-surface="study"] span:last-child').textContent
    }))()`);
    assert.deepEqual(value, { mode: 'read', presentation: 'modal', modal: true, action: 'Details' });
    await escape(cdp);

    await evaluate(cdp, `window.scrollTo(0, document.querySelectorAll('[data-semantic-location]')[4].offsetTop)`);
    await new Promise((accept) => setTimeout(accept, 80));
    const location = await evaluate(cdp, 'ReaderShellPrototype.current().location');
    await click(cdp, '[data-surface="mode"]');
    await click(cdp, '[data-mode="study"]');
    await waitFor(cdp, 'ReaderShellPrototype.current().surfacePresentation === "pinned"', 'pinned Study rail');
    value = await evaluate(cdp, `(() => ({
      location: ReaderShellPrototype.current().location,
      modal: document.querySelector('#study-surface').matches(':modal'),
      presentation: ReaderShellPrototype.current().surfacePresentation,
      readingInert: document.querySelector('#reader-document').inert,
      title: document.querySelector('#study-surface-title').textContent,
      action: document.querySelector('[data-surface="study"] span:last-child').textContent,
      readingWidth: document.querySelector('#reader-document').getBoundingClientRect().width
    }))()`);
    assert.equal(value.location, location);
    assert.equal(value.modal, false);
    assert.equal(value.presentation, 'pinned');
    assert.equal(value.readingInert, false);
    assert.equal(value.title, 'Study apparatus');
    assert.equal(value.action, 'Details');
    assert.ok(Math.abs(value.readingWidth - readWidth) <= 1, `${readWidth} became ${value.readingWidth}`);
    const sourceBefore = await evaluate(cdp, `document.querySelector('.source-identifier')?.textContent`);
    const laterLocation = await evaluate(cdp, `(() => {
      const target = document.querySelectorAll('[data-semantic-location]')[7];
      target.scrollIntoView({ block: 'start' });
      target.querySelector('[data-semantic-focus]').focus({ preventScroll: true });
      return target.dataset.semanticLocation;
    })()`);
    await waitFor(cdp,
      `ReaderShellPrototype.current().location === ${JSON.stringify(laterLocation)}`,
      'pinned Study semantic update');
    await new Promise((accept) => setTimeout(accept, 100));
    value = await evaluate(cdp, `({
      railOpen: document.querySelector('#study-surface').open,
      readingFocused: document.querySelector('#reader-document').contains(document.activeElement),
      scrolled: window.scrollY > 0,
      source: document.querySelector('.source-identifier')?.textContent
    })`);
    assert.equal(value.railOpen, true);
    assert.equal(value.readingFocused, true);
    assert.equal(value.scrolled, true);
    assert.notEqual(value.source, sourceBefore);

    await viewport(cdp, 768, 1024);
    await waitFor(cdp, 'ReaderShellPrototype.current().surfacePresentation === "modal"', 'resized Study sheet');
    assert.equal(await evaluate(cdp, `document.querySelector('#study-surface').matches(':modal')`), true);
    await viewport(cdp, 1440, 900);
    await waitFor(cdp, 'ReaderShellPrototype.current().surfacePresentation === "pinned"', 'restored pinned Study rail');

    await viewport(cdp, 393, 852);
    await navigate(cdp, url(base, 'day-read', 'persistent'));
    await evaluate(cdp, `window.scrollTo(0, document.querySelectorAll('[data-semantic-location]')[4].offsetTop)`);
    await new Promise((accept) => setTimeout(accept, 80));
    const mobileLocation = await evaluate(cdp, 'ReaderShellPrototype.current().location');
    await click(cdp, '[data-surface="mode"]');
    await click(cdp, '[data-mode="study"]');
    await waitFor(cdp, 'ReaderShellPrototype.current().surfacePresentation === "modal"', 'mobile Study sheet');
    assert.equal(await evaluate(cdp, `document.querySelector('#study-surface').matches(':modal')`), true);
    await escape(cdp);
    value = await evaluate(cdp, `({
      mode: ReaderShellPrototype.current().mode,
      location: ReaderShellPrototype.current().location,
      focused: document.activeElement === document.querySelector('[data-surface="study"]')
    })`);
    assert.deepEqual(value, { mode: 'study', location: mobileLocation, focused: true });
    await click(cdp, '[data-surface="mode"]');
    await click(cdp, '[data-mode="read"]');
    await waitFor(cdp,
      `ReaderShellPrototype.current().mode === "read" && ReaderShellPrototype.current().location === ${JSON.stringify(mobileLocation)} && ` +
      `document.activeElement === document.querySelector('[data-surface="mode"]')`,
      'return to Read location and focus');
    value = await evaluate(cdp, `({
      location: ReaderShellPrototype.current().location,
      focused: document.activeElement === document.querySelector('[data-surface="mode"]'),
      active: document.activeElement.outerHTML
    })`);
    assert.equal(value.location, mobileLocation);
    assert.equal(value.focused, true, value.active);
  });

  await test('every open auxiliary surface reflows without internal horizontal overflow', async () => {
    const sizes = [[1440, 900], [1024, 768], [768, 1024], [393, 852], [320, 852]];
    for (const [width, height] of sizes) {
      await viewport(cdp, width, height);
      for (const surface of ['entrance', 'contents', 'mode', 'study']) {
        await navigate(cdp, url(base, 'day-read', 'persistent'));
        await click(cdp, `[data-surface="${surface}"]`);
        assert.deepEqual(await surfaceOverflow(cdp, surface), [], `${surface} overflow at ${width}x${height}`);
        await escape(cdp);
      }
      await navigate(cdp, url(base, 'propers-browse', 'persistent'));
      await waitFor(cdp, 'ReaderShellPrototype.current().surface === "entrance"', 'Browse surface');
      assert.deepEqual(await surfaceOverflow(cdp, 'entrance'), [], `Browse overflow at ${width}x${height}`);
      await escape(cdp);
    }

    await viewport(cdp, 393, 852);
    for (const [state, surface] of [
      ['day-read', 'entrance'], ['day-read', 'contents'], ['day-read', 'mode'],
      ['day-read', 'study'], ['propers-browse', 'entrance']
    ]) {
      await navigate(cdp, url(base, state, 'persistent'));
      await evaluate(cdp, `document.documentElement.style.fontSize = '200%'`);
      if (await evaluate(cdp, 'ReaderShellPrototype.current().surface === null')) {
        await click(cdp, `[data-surface="${surface}"]`);
      }
      assert.deepEqual(await surfaceOverflow(cdp, surface), [], `${state}/${surface} overflow at 200%`);
      await escape(cdp);
    }
  });

  await test('state selection is explicit and invalid prototype input fails closed', async () => {
    const expected = {
      'day-read': ['roman-1962', 'pentecost-10', 'douay-rheims', 'la'],
      'day-postconciliar': ['postconciliar', 'advent-1', 'douay-rheims', 'la'],
      'day-missal': ['roman-1962', 'pentecost-10', 'douay-rheims', 'la'],
      'propers-formulary': ['roman-1962', 'advent-1', 'douay-rheims', 'la'],
      'bilingual': ['roman-1962', 'advent-1', 'douay-rheims', 'la']
    };
    for (const [name, selections] of Object.entries(expected)) {
      await navigate(cdp, url(base, name, 'persistent'));
      const current = await evaluate(cdp, 'ReaderShellPrototype.current()');
      assert.deepEqual([
        current.selections.edition, current.selections.mass,
        current.selections.bible, current.selections.orations
      ], selections, `${name} silently changed a selection`);
    }
    for (const suffix of [
      'state=not-held&shell=persistent',
      'state=day-read&shell=vanishing',
      'state=day-read&shell=persistent&mode=dashboard',
      'state=day-read&shell=persistent&orations=invented'
    ]) {
      await navigate(cdp, `${base}${ROUTE}?${suffix}&data=/build/public-alpha/preview/browse`);
      const failed = await evaluate(cdp, `(() => ({
        error: !document.querySelector('#prototype-error').hidden,
        shell: document.querySelector('#reader-shell').hidden,
        text: document.querySelector('#prototype-error').textContent,
        propers: document.querySelectorAll('.proper').length
      }))()`);
      assert.equal(failed.error, true, suffix);
      assert.equal(failed.shell, true, suffix);
      assert.equal(failed.propers, 0, suffix);
      assert.match(failed.text, /Unsupported|No fallback|invalid/, suffix);
    }
  });

  await test('Study uses only identity-matched M1 apparatus', async () => {
    await navigate(cdp, url(base, 'day-study', 'persistent'));
    await waitFor(cdp, 'ReaderShellPrototype.current().surface === "study"', 'Study surface');
    let value = await evaluate(cdp, `(() => ({
      trusted: ReaderShellPrototype.current().fixtureTrusted,
      text: document.querySelector('#study-panel-content').innerText
    }))()`);
    assert.equal(value.trusted, true);
    assert.match(value.text, /pentecost-10/);
    assert.match(value.text, /After pentecost/);
    assert.doesNotMatch(value.text, /[\[{]\s*"/);
    await escape(cdp);

    await navigate(cdp, url(base, 'day-read', 'persistent', '&display=original&bible=clementine-vulgate'));
    await click(cdp, '[data-surface="study"]');
    value = await evaluate(cdp, `(() => ({
      trusted: ReaderShellPrototype.current().fixtureTrusted,
      mismatch: ReaderShellPrototype.current().fixtureMismatch,
      text: document.querySelector('#study-panel-content').innerText
    }))()`);
    assert.equal(value.trusted, false);
    assert.ok(value.mismatch.includes('Bible edition'));
    assert.match(value.text, /not applied/);
    assert.doesNotMatch(value.text, /proper\/roman-1962\/pentecost-10/);
    await escape(cdp);
  });

  await test('date failure preserves the explicit edition and requested date', async () => {
    await navigate(cdp, url(base, 'day-postconciliar', 'persistent'));
    await click(cdp, '[data-surface="entrance"]');
    await click(cdp, '.date-steps button:last-child');
    await waitFor(cdp, 'ReaderShellPrototype.current().state === "unavailable"', 'unavailable date');
    const value = await evaluate(cdp, `(() => ({
      current: ReaderShellPrototype.current(),
      date: document.querySelector('#reader-date').textContent,
      message: document.querySelector('#reader-document').innerText,
      query: location.search
    }))()`);
    assert.equal(value.current.selections.edition, 'postconciliar');
    assert.match(value.date, /November 30, 2026/);
    assert.match(value.message, /has not substituted/);
    assert.match(value.query, /requestedDate=2026-11-30/);
  });

  await test('Mode radiogroup supports arrow keys and Compare has a return path', async () => {
    await navigate(cdp, url(base, 'day-read', 'persistent'));
    await click(cdp, '[data-surface="mode"]');
    await evaluate(cdp, `document.querySelector('[data-mode="read"]').focus()`);
    await cdp.send('Input.dispatchKeyEvent', {
      type: 'keyDown', key: 'ArrowRight', code: 'ArrowRight', windowsVirtualKeyCode: 39
    });
    await cdp.send('Input.dispatchKeyEvent', {
      type: 'keyUp', key: 'ArrowRight', code: 'ArrowRight', windowsVirtualKeyCode: 39
    });
    await waitFor(cdp, 'ReaderShellPrototype.current().mode === "missal"', 'arrow-selected Missal');
    await click(cdp, '[data-surface="mode"]');
    await click(cdp, '[data-mode="compare"]');
    await waitFor(cdp, 'ReaderShellPrototype.current().mode === "compare"', 'Compare');
    assert.equal(await evaluate(cdp, 'ReaderShellPrototype.current().entrance'), 'day');
    await click(cdp, '[data-surface="mode"]');
    await click(cdp, '[data-mode="read"]');
    await waitFor(cdp, 'ReaderShellPrototype.current().mode === "read"', 'return from Compare');
    assert.equal(await evaluate(cdp, 'ReaderShellPrototype.current().entrance'), 'day');
  });

  await test('production Day and Propers routes still render in Chromium', async () => {
    await viewport(cdp, 1024, 768);
    await cdp.send('Page.navigate', {
      url: `${base}/src/web/browser/liturgy/day.html?data=/build/public-alpha/preview/browse#date=2026-08-02&missal=roman-1962`
    });
    await waitFor(cdp, 'document.querySelectorAll("#reading .proper, .reading .proper").length > 0', 'production Day Proper');
    assert.equal(await evaluate(cdp, 'document.querySelectorAll("#reader-shell").length'), 0);
    await cdp.send('Page.navigate', {
      url: `${base}/src/web/browser/liturgy/index.html?data=/build/public-alpha/preview/browse#missal=roman-1962&type=temporal&mass=advent-1`
    });
    await waitFor(cdp, 'document.querySelectorAll("#reading .proper, .reading .proper").length > 0', 'production Propers Proper');
    assert.equal(await evaluate(cdp, 'document.querySelectorAll("#reader-shell").length'), 0);
  });

  await test('320-pixel reflow has no page overflow and keeps practical targets', async () => {
    await viewport(cdp, 320, 852);
    await navigate(cdp, url(base, 'bilingual', 'persistent'));
    const value = await evaluate(cdp, `(() => ({
      overflow: document.documentElement.scrollWidth - document.documentElement.clientWidth,
      columns: getComputedStyle(document.querySelector('.dual-text')).gridTemplateColumns,
      actionOverflow: document.querySelector('#global-actions').scrollWidth - document.querySelector('#global-actions').clientWidth,
      targets: [...document.querySelectorAll('#global-actions button')].map(b => {
        const r = b.getBoundingClientRect();
        return { width: r.width, height: r.height, left: r.left, right: r.right };
      })
    }))()`);
    assert.ok(value.overflow <= 0, `horizontal overflow is ${value.overflow}px`);
    assert.ok(value.actionOverflow <= 0, `action overflow is ${value.actionOverflow}px`);
    assert.ok(value.targets.every((one) => one.height >= 44), JSON.stringify(value.targets));
    assert.ok(value.targets.every((one) => one.left >= 0 && one.right <= 320), JSON.stringify(value.targets));
  });

  await test('200-percent text enlargement and forced colors retain all actions', async () => {
    await viewport(cdp, 320, 852);
    await navigate(cdp, url(base, 'day-read', 'persistent'));
    await evaluate(cdp, `document.documentElement.style.fontSize = '200%'`);
    await new Promise((accept) => setTimeout(accept, 100));
    const value = await evaluate(cdp, `(() => ({
      overflow: document.documentElement.scrollWidth - document.documentElement.clientWidth,
      actions: [...document.querySelectorAll('#global-actions button')].map(button => {
        const box = button.getBoundingClientRect();
        return { left: box.left, right: box.right, height: box.height };
      }),
      clientWidth: document.documentElement.clientWidth
    }))()`);
    assert.ok(value.actions.every((one) => one.left >= 0 && one.right <= value.clientWidth && one.height >= 44), JSON.stringify(value));
    await evaluate(cdp, 'window.scrollTo(9999, 0)');
    assert.equal(await evaluate(cdp, 'window.scrollX'), 0, JSON.stringify(value));
    await evaluate(cdp, `document.documentElement.style.fontSize = ''`);
    await cdp.send('Emulation.setEmulatedMedia', {
      media: 'screen', features: [{ name: 'forced-colors', value: 'active' }]
    });
    const forced = await evaluate(cdp, `(() => ({
      border: getComputedStyle(document.querySelector('#global-actions')).borderTopWidth,
      currentBorder: getComputedStyle(document.querySelector('#semantic-contents button')).borderLeftWidth
    }))()`);
    assert.notEqual(forced.border, '0px');
    await cdp.send('Emulation.setEmulatedMedia', { media: 'screen' });
  });

  await test('print omits interactive chrome and retains contextual identity', async () => {
    await viewport(cdp, 1024, 768);
    await navigate(cdp, url(base, 'day-read', 'persistent'));
    await cdp.send('Emulation.setEmulatedMedia', { media: 'print' });
    const value = await evaluate(cdp, `(() => ({
      actions: getComputedStyle(document.querySelector('#global-actions')).display,
      flag: getComputedStyle(document.querySelector('.prototype-flag')).display,
      title: getComputedStyle(document.querySelector('#reader-title')).display,
      meta: document.querySelector('#reader-meta').textContent,
      content: document.querySelectorAll('#reader-document .proper').length
    }))()`);
    assert.equal(value.actions, 'none');
    assert.equal(value.flag, 'none');
    assert.notEqual(value.title, 'none');
    assert.match(value.meta, /1962 Roman Missal/);
    assert.ok(value.content >= 8);
    await cdp.send('Emulation.setEmulatedMedia', { media: 'screen' });
  });
}

async function prepareCapture(cdp, base, state, variant, kind) {
  await navigate(cdp, url(base, state, variant));
  if (kind === 'deep') {
    await evaluate(cdp, 'window.scrollTo(0, Math.max(0, document.documentElement.scrollHeight - innerHeight - 8))');
    await new Promise((accept) => setTimeout(accept, 100));
  } else if (['contents', 'mode', 'study'].includes(kind)) {
    await click(cdp, `[data-surface="${kind}"]`);
    await new Promise((accept) => setTimeout(accept, 50));
  }
}

async function captureMatrix(cdp, base, directory) {
  await mkdir(directory, { recursive: true });
  const sizes = [[1440, 900], [1024, 768], [768, 1024], [393, 852], [320, 852]];
  const cases = [
    ['day-read', 'read'],
    ['day-missal', 'deep'],
    ['day-read', 'contents'],
    ['day-read', 'mode'],
    ['day-read', 'study'],
    ['propers-formulary', 'default'],
    ['unavailable', 'partial']
  ];
  const measures = [];
  for (const [width, height] of sizes) {
    await viewport(cdp, width, height);
    for (const variant of ['persistent', 'reveal']) {
      for (const [state, kind] of cases) {
        await prepareCapture(cdp, base, state, variant, kind);
        const entrance = state.startsWith('propers') ? 'propers' : 'day';
        const fileState = kind === 'default' ? 'read' : kind;
        const name = `${entrance}-${fileState}-${variant}-${width}x${height}.png`;
        await shot(cdp, join(directory, name));
        measures.push({ viewport: `${width}x${height}`, state, kind, variant,
          metrics: await evaluate(cdp, 'ReaderShellPrototype.metrics()') });
        if (await evaluate(cdp, 'document.querySelectorAll("dialog[open]").length > 0')) await escape(cdp);
      }
    }
  }

  const extended = [
    ['day-postconciliar', 'day-postconciliar-read'],
    ['day-study', 'day-study-shell'],
    ['propers-browse', 'propers-browse'],
    ['compare-day', 'day-compare'],
    ['unresolved', 'day-unresolved'],
    ['bilingual', 'propers-bilingual']
  ];
  for (const [width, height] of [[1440, 900], [393, 852]]) {
    await viewport(cdp, width, height);
    for (const variant of ['persistent', 'reveal']) {
      for (const [state, name] of extended) {
        await navigate(cdp, url(base, state, variant));
        await new Promise((accept) => setTimeout(accept, 50));
        await shot(cdp, join(directory, `${name}-${variant}-${width}x${height}.png`));
        measures.push({ viewport: `${width}x${height}`, state, kind: 'representative', variant,
          metrics: await evaluate(cdp, 'ReaderShellPrototype.metrics()') });
        if (await evaluate(cdp, 'document.querySelectorAll("dialog[open]").length > 0')) await escape(cdp);
      }
    }
  }

  await viewport(cdp, 393, 852);
  await navigate(cdp, url(base, 'day-read', 'persistent'));
  await click(cdp, '[data-surface="contents"]');
  await cdp.send('Input.dispatchKeyEvent', { type: 'keyDown', key: 'Tab', code: 'Tab', windowsVirtualKeyCode: 9 });
  await cdp.send('Input.dispatchKeyEvent', { type: 'keyUp', key: 'Tab', code: 'Tab', windowsVirtualKeyCode: 9 });
  await shot(cdp, join(directory, 'day-keyboard-focus-persistent-393x852.png'));
  await escape(cdp);

  await cdp.send('Emulation.setEmulatedMedia', {
    media: 'screen', features: [{ name: 'prefers-reduced-motion', value: 'reduce' }]
  });
  await navigate(cdp, url(base, 'day-read', 'reveal'));
  await shot(cdp, join(directory, 'day-reduced-motion-reveal-393x852.png'));
  await cdp.send('Emulation.setEmulatedMedia', { media: 'screen' });

  await navigate(cdp, url(base, 'day-read', 'persistent'));
  await evaluate(cdp, `document.documentElement.style.setProperty('--safe-bottom', '34px')`);
  await shot(cdp, join(directory, 'day-safe-area-persistent-393x852.png'));

  await viewport(cdp, 1024, 768);
  await navigate(cdp, url(base, 'day-read', 'persistent'));
  await cdp.send('Emulation.setEmulatedMedia', { media: 'print' });
  const pdf = await cdp.send('Page.printToPDF', {
    printBackground: true, preferCSSPageSize: true, paperWidth: 8.27, paperHeight: 11.69,
    marginTop: 0.4, marginBottom: 0.4, marginLeft: 0.45, marginRight: 0.45
  });
  await cdp.send('Emulation.setEmulatedMedia', { media: 'screen' });
  await writeFile(join(directory, 'day-read-print.pdf'), Buffer.from(pdf.data, 'base64'));
  await writeFile(join(directory, 'measurements.json'), JSON.stringify(measures, null, 2) + '\n');
  return measures;
}

async function captureCorrectionEvidence(cdp, base, directory) {
  await mkdir(directory, { recursive: true });
  const measures = [];

  async function capture(name, width, height, state, surface = null, enlargement = false) {
    await viewport(cdp, width, height);
    await navigate(cdp, url(base, state, 'persistent'));
    if (surface && await evaluate(cdp, 'ReaderShellPrototype.current().surface === null')) {
      await click(cdp, `[data-surface="${surface}"]`);
    }
    if (surface) await waitFor(cdp,
      `ReaderShellPrototype.current().surface === ${JSON.stringify(surface)}`, `${name} surface`);
    if (enlargement) {
      await evaluate(cdp, `document.documentElement.style.fontSize = '200%'`);
      await new Promise((accept) => setTimeout(accept, 100));
    }
    await shot(cdp, join(directory, name + '.png'));
    const currentSurface = await evaluate(cdp, 'ReaderShellPrototype.current().surface');
    measures.push({
      file: name + '.png', viewport: `${width}x${height}`,
      state, surface: currentSurface, enlargement: enlargement ? '200%' : '100%',
      surfaceOverflow: currentSurface ? await surfaceOverflow(cdp, currentSurface) : [],
      metrics: await evaluate(cdp, 'ReaderShellPrototype.metrics()')
    });
    if (currentSurface) await escape(cdp);
  }

  await capture('day-read-persistent-393x852', 393, 852, 'day-read');
  await capture('day-read-persistent-320x852', 320, 852, 'day-read');
  await capture('propers-read-persistent-393x852', 393, 852, 'propers-formulary');
  await capture('day-date-persistent-1440x900', 1440, 900, 'day-read', 'entrance');
  await capture('day-date-persistent-393x852', 393, 852, 'day-read', 'entrance');
  await capture('propers-browse-persistent-1440x900', 1440, 900, 'propers-browse', 'entrance');
  await capture('propers-browse-persistent-393x852', 393, 852, 'propers-browse', 'entrance');
  await capture('day-details-persistent-1440x900', 1440, 900, 'day-read', 'study');
  await capture('day-details-persistent-393x852', 393, 852, 'day-read', 'study');
  await capture('day-study-mode-persistent-1440x900', 1440, 900, 'day-study', 'study');
  await capture('day-study-mode-persistent-393x852', 393, 852, 'day-study', 'study');
  await capture('propers-browse-persistent-393x852-200-percent', 393, 852, 'propers-browse', 'entrance', true);

  for (const [width, height] of [[1440, 900], [1024, 768], [768, 1024]]) {
    await viewport(cdp, width, height);
    await navigate(cdp, url(base, 'day-read', 'persistent'));
    measures.push({
      file: null, viewport: `${width}x${height}`, state: 'day-read', surface: null,
      enlargement: '100%', surfaceOverflow: [],
      metrics: await evaluate(cdp, 'ReaderShellPrototype.metrics()')
    });
  }

  await viewport(cdp, 1024, 768);
  await navigate(cdp, url(base, 'day-read', 'persistent'));
  await cdp.send('Emulation.setEmulatedMedia', { media: 'print' });
  const pdf = await cdp.send('Page.printToPDF', {
    printBackground: true, preferCSSPageSize: true, paperWidth: 8.5, paperHeight: 11,
    marginTop: 0.4, marginBottom: 0.4, marginLeft: 0.45, marginRight: 0.45
  });
  await cdp.send('Emulation.setEmulatedMedia', { media: 'screen' });
  await writeFile(join(directory, 'day-read-print.pdf'), Buffer.from(pdf.data, 'base64'));
  await writeFile(join(directory, 'measurements.json'), JSON.stringify(measures, null, 2) + '\n');
  return measures;
}

async function main() {
  const server = staticServer();
  const serverPort = await listen(server);
  const base = `http://127.0.0.1:${serverPort}`;
  const debugPort = await freePort();
  const profile = await mkdtemp(join(tmpdir(), 'triptych-reader-shell-chrome-'));
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
    const pageResponse = await fetch(
      `http://127.0.0.1:${debugPort}/json/new?${encodeURIComponent('about:blank')}`,
      { method: 'PUT' }
    );
    const page = await pageResponse.json();
    cdp = new CDP(page.webSocketDebuggerUrl);
    await cdp.ready();
    await Promise.all([
      cdp.send('Page.enable'), cdp.send('Runtime.enable'), cdp.send('Network.enable'),
      cdp.send('Accessibility.enable'), cdp.send('Performance.enable')
    ]);
    cdp.on('Runtime.consoleAPICalled', ({ type, args }) => {
      if (['error', 'warning'].includes(type)) consoleProblems.push({
        type, text: args.map((arg) => arg.value || arg.description || '').join(' ')
      });
    });
    cdp.on('Network.loadingFailed', (event) => failedRequests.push({
      url: event.requestId, error: event.errorText, canceled: Boolean(event.canceled)
    }));
    cdp.on('Network.responseReceived', ({ response }) => {
      if (response.status >= 400) httpProblems.push({
        status: response.status, url: response.url, type: response.mimeType
      });
    });
    if (!beforeDir) await runAssertions(cdp, base);
    let measures = [];
    if (captureDir) measures = await captureMatrix(cdp, base, captureDir);
    if (correctionDir) measures = await captureCorrectionEvidence(cdp, base, correctionDir);
    if (beforeDir) measures = await captureCorrectionEvidence(cdp, base, beforeDir);
    await navigate(cdp, url(base, 'day-read', 'persistent'));
    const defaultMetrics = await evaluate(cdp, 'ReaderShellPrototype.metrics()');
    const interactionLatencyMs = await evaluate(cdp, `(async () => {
      await new Promise(resolve => requestAnimationFrame(resolve));
      const started = performance.now();
      document.querySelector('[data-surface="contents"]').click();
      await new Promise(resolve => requestAnimationFrame(() => requestAnimationFrame(resolve)));
      const elapsed = performance.now() - started;
      ReaderShellPrototype.close();
      return Math.round(elapsed * 100) / 100;
    })()`);
    const ax = await cdp.send('Accessibility.getFullAXTree');
    const report = {
      generatedAt: new Date().toISOString(),
      chrome: (await waitForJson(`http://127.0.0.1:${debugPort}/json/version`)).Browser,
      assertions: observations,
      failures,
      consoleProblems,
      failedRequests,
      httpProblems,
      accessibility: {
        nodeCount: ax.nodes.length,
        unnamedInteractiveNodes: ax.nodes.filter((node) =>
          ['button', 'link', 'radio'].includes(node.role?.value) && !node.name?.value).length
      },
      performance: { defaultMetrics, interactionLatencyMs },
      captures: measures.length,
      files: {
        javascript: (await stat(join(ROOT, 'src/web/browser/liturgy/prototypes/reader-shell/reader-shell.js'))).size,
        css: (await stat(join(ROOT, 'src/web/browser/liturgy/prototypes/reader-shell/reader-shell.css'))).size,
        html: (await stat(join(ROOT, 'src/web/browser/liturgy/prototypes/reader-shell/index.html'))).size
      }
    };
    const reportDir = captureDir || correctionDir || beforeDir;
    if (reportDir) await writeFile(join(reportDir, 'browser-results.json'), JSON.stringify(report, null, 2) + '\n');
    process.stdout.write(JSON.stringify(report, null, 2) + '\n');
    const unexpectedFailed = failedRequests.filter((one) => !one.canceled);
    if (failures.length || report.accessibility.unnamedInteractiveNodes || consoleProblems.length ||
        unexpectedFailed.length || httpProblems.length) process.exitCode = 1;
  } catch (error) {
    process.stderr.write((error.stack || String(error)) + '\n' + chromeStderr.slice(-4000));
    process.exitCode = 1;
  } finally {
    if (cdp) cdp.close();
    chrome.kill('SIGTERM');
    await new Promise((accept) => server.close(accept));
  }
}

await main();
