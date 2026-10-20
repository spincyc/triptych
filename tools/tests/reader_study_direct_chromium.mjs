#!/usr/bin/env node

/* Direct Study keeps the current Proper and returns focus to its dock command. */

import assert from 'node:assert/strict';
import { spawn } from 'node:child_process';
import { createServer } from 'node:http';
import { mkdir, mkdtemp, readFile, rm } from 'node:fs/promises';
import { extname, resolve, sep } from 'node:path';

const ROOT = resolve(import.meta.dirname, '../..');
const CHROME = process.env.TRIPTYCH_CHROME || '/usr/bin/chromium';
const SCRATCH = resolve(process.env.TRIPTYCH_BROWSER_SCRATCH ||
  resolve(ROOT, '.scratch/c7-study-direct/browser'));
const DAY = '/src/web/browser/liturgy/day.html';
const PROPERS = '/src/web/browser/liturgy/index.html';

const mime = (file) => ({ '.css': 'text/css', '.html': 'text/html',
  '.js': 'text/javascript', '.json': 'application/json' })[extname(file)] || 'application/octet-stream';

function server() {
  return createServer(async (request, response) => {
    try {
      let relative = decodeURIComponent(new URL(request.url, 'http://localhost').pathname)
        .replace(/^\/+/, '');
      if (relative === 'favicon.ico') { response.writeHead(204); response.end(); return; }
      if (/^src\/web\/data\/[^/]+\/chapters\//.test(relative)) {
        relative = relative.replace(/^src\/web\/data\//, 'src/sources/bibles/');
      }
      const file = resolve(ROOT, relative || 'README.md');
      if (!file.startsWith(ROOT + sep)) throw new Error('outside repository');
      response.writeHead(200, { 'content-type': mime(file), 'cache-control': 'no-store' });
      response.end(await readFile(file));
    } catch (_error) { response.writeHead(404); response.end('not found'); }
  });
}

async function listen(instance) {
  await new Promise((done, reject) => {
    instance.once('error', reject);
    instance.listen(0, '127.0.0.1', done);
  });
  return instance.address().port;
}

async function freePort() {
  const instance = server();
  const port = await listen(instance);
  await new Promise((done) => instance.close(done));
  return port;
}

async function waitJson(url) {
  for (let attempt = 0; attempt < 120; attempt += 1) {
    try { const reply = await fetch(url); if (reply.ok) return reply.json(); }
    catch (_error) { /* Chromium is starting. */ }
    await new Promise((done) => setTimeout(done, 50));
  }
  throw new Error('Chromium debugging endpoint did not start');
}

class CDP {
  constructor(url) {
    this.socket = new WebSocket(url);
    this.next = 0;
    this.pending = new Map();
    this.events = new Map();
  }
  on(name, callback) {
    this.events.set(name, [...(this.events.get(name) || []), callback]);
  }
  async ready() {
    await new Promise((done, reject) => {
      this.socket.addEventListener('open', done, { once: true });
      this.socket.addEventListener('error', reject, { once: true });
    });
    this.socket.addEventListener('message', (event) => {
      const message = JSON.parse(event.data);
      if (!message.id) {
        for (const callback of this.events.get(message.method) || []) callback(message.params);
        return;
      }
      const pending = this.pending.get(message.id);
      if (!pending) return;
      this.pending.delete(message.id);
      clearTimeout(pending.timer);
      if (message.error) pending.reject(new Error(message.error.message));
      else pending.resolve(message.result);
    });
  }
  send(method, params = {}) {
    const id = ++this.next;
    return new Promise((resolve, reject) => {
      const timer = setTimeout(() => {
        this.pending.delete(id); reject(new Error('CDP timeout: ' + method));
      }, 30000);
      this.pending.set(id, { resolve, reject, timer });
      this.socket.send(JSON.stringify({ id, method, params }));
    });
  }
  close() { this.socket.close(); }
}

async function evaluate(cdp, expression) {
  const reply = await cdp.send('Runtime.evaluate', {
    expression, awaitPromise: true, returnByValue: true, userGesture: true
  });
  if (reply.exceptionDetails) throw new Error(
    reply.exceptionDetails.exception?.description || reply.exceptionDetails.text);
  return reply.result.value;
}

async function waitFor(cdp, expression, label) {
  for (let attempt = 0; attempt < 240; attempt += 1) {
    if (await evaluate(cdp, `Boolean(${expression})`)) return;
    await new Promise((done) => setTimeout(done, 50));
  }
  throw new Error('Timed out waiting for ' + label);
}

async function key(cdp, name) {
  const codes = { Enter: 13, Escape: 27, ' ': 32 };
  for (const type of ['keyDown', 'keyUp']) await cdp.send('Input.dispatchKeyEvent', {
    type, key: name, code: name === ' ' ? 'Space' : name,
    windowsVirtualKeyCode: codes[name], nativeVirtualKeyCode: codes[name],
    ...(type === 'keyDown' && name !== 'Escape' ? { text: name === 'Enter' ? '\r' : name } : {})
  });
}

const instance = server();
const port = await listen(instance);
const debugPort = await freePort();
await mkdir(SCRATCH, { recursive: true });
const profile = await mkdtemp(resolve(SCRATCH, 'chromium-'));
const chrome = spawn(CHROME, [
  '--headless=new', '--disable-gpu', '--no-sandbox', '--disable-dev-shm-usage',
  `--remote-debugging-port=${debugPort}`, `--user-data-dir=${profile}`, 'about:blank'
], { stdio: 'ignore' });
let cdp;
const assertions = [];
const consoleProblems = [];
const failedRequests = [];
const httpProblems = [];
try {
  const pages = await waitJson(`http://127.0.0.1:${debugPort}/json`);
  cdp = new CDP(pages.find((page) => page.type === 'page').webSocketDebuggerUrl);
  await cdp.ready();
  cdp.on('Runtime.exceptionThrown', ({ exceptionDetails }) =>
    consoleProblems.push(exceptionDetails?.exception?.description || exceptionDetails?.text));
  cdp.on('Runtime.consoleAPICalled', ({ type, args }) => {
    if (type === 'error' || type === 'warning') consoleProblems.push(
      args.map((one) => one.value || one.description || '').join(' '));
  });
  cdp.on('Network.loadingFailed', ({ canceled, errorText }) => {
    if (!canceled) failedRequests.push(errorText);
  });
  cdp.on('Network.responseReceived', ({ response }) => {
    if (response?.status >= 400) httpProblems.push({ status: response.status, url: response.url });
  });
  await Promise.all([cdp.send('Page.enable'), cdp.send('Runtime.enable'), cdp.send('Network.enable')]);
  await cdp.send('Page.addScriptToEvaluateOnNewDocument', { source: `
    Storage.prototype.getItem = function () { throw new Error('storage unavailable'); };
    Storage.prototype.setItem = function () { throw new Error('storage unavailable'); };
  ` });
  await cdp.send('Emulation.setDeviceMetricsOverride', {
    width: 393, height: 852, deviceScaleFactor: 1, mobile: false
  });
  const base = `http://127.0.0.1:${port}`;
  for (const entrance of ['day', 'propers']) {
    await cdp.send('Emulation.setDeviceMetricsOverride', {
      width: 393, height: 852, deviceScaleFactor: 1, mobile: false
    });
    const path = entrance === 'day' ? DAY : PROPERS;
    const identity = entrance === 'day'
      ? '#date=2026-11-22&missal=roman-1962&bible=douay-rheims&orations=la'
      : '#missal=roman-1962&type=seasonal&mass=advent-1&bible=douay-rheims&orations=la';
    const debug = entrance + 'ReaderDebug';
    async function ready(mode) {
      await waitFor(cdp, `window.${debug}?.ready && ${debug}.outcome === 'ready' &&
        document.querySelector('[data-reader-shell]').dataset.readerMode === '${mode}' &&
        document.getElementById('reader-document').getAttribute('aria-busy') === 'false'`,
      entrance + ' ' + mode);
      assert.equal(await evaluate(cdp, `(async () => {
        let previous = null, stable = 0;
        for (let frame = 0; frame < 120; frame += 1) {
          await new Promise(requestAnimationFrame);
          const y = scrollY;
          stable = previous !== null && Math.abs(y - previous) < 0.5 ? stable + 1 : 0;
          if (stable >= 6) return true;
          previous = y;
        }
        return false;
      })()`), true, 'reader location visually settled');
    }
    async function visit(suffix) {
      await cdp.send('Page.navigate', { url: base + path + '?data=/src/web/data' + identity + suffix });
    }
    async function click(selector) {
      await evaluate(cdp, `document.querySelector(${JSON.stringify(selector)}).click()`);
    }
    async function jump(selector) {
      await click('[data-reader-action="contents"]');
      const id = await evaluate(cdp, `(() => {
        const buttons = [...document.querySelectorAll('[data-reader-location]')];
        const target = buttons.find(button => ${selector});
        if (!target) throw new Error('semantic Contents target not found');
        const id = target.dataset.readerLocation; target.click(); return id;
      })()`);
      await waitFor(cdp, `new URLSearchParams(location.hash.slice(1)).get('location') ===
        ${JSON.stringify(id)} && !document.getElementById('contents-surface').open`, 'Contents location');
      assert.equal(await evaluate(cdp, `(async () => {
        const target = [...document.querySelectorAll('[data-semantic-location]')]
          .find(node => node.dataset.semanticLocation === ${JSON.stringify(id)});
        let previous = null, stable = 0;
        for (let frame = 0; frame < 90; frame += 1) {
          await new Promise(requestAnimationFrame);
          const top = target.getBoundingClientRect().top;
          stable = top <= 280 && previous !== null && Math.abs(top - previous) < 0.5 ? stable + 1 : 0;
          if (stable >= 3) return true;
          previous = top;
        }
        return false;
      })()`), true, 'Contents target visually settled');
      return id;
    }
    await visit('&mode=read');
    await ready('read');
    assert.deepEqual(await evaluate(cdp, `[...document.querySelectorAll('.reader-actions button')]
      .map(button => button.dataset.readerAction)`),
    [entrance === 'day' ? 'date' : 'browse', 'contents', 'mode', 'study']);
    assert.equal(await evaluate(cdp, `document.querySelector('[data-reader-action="details"]')
      .closest('[data-reader-surface]').dataset.readerSurface`), 'mode');
    assertions.push(entrance + ' exposes four dock commands and secondary Details');

    const target = await jump("/gospel/i.test(button.textContent)");
    const before = await evaluate(cdp, `[...document.querySelectorAll('[data-semantic-event-id]')]
      .map(node => node.dataset.semanticEventId)`);
    await evaluate(cdp, `document.querySelector('[data-reader-action="study"]').focus({ preventScroll: true })`);
    await key(cdp, 'Enter');
    await ready('study');
    const studied = await evaluate(cdp, `({ mode: new URLSearchParams(location.hash.slice(1)).get('mode'),
      location: new URLSearchParams(location.hash.slice(1)).get('location'),
      focus: document.activeElement.dataset.readerAction,
      current: document.querySelector('[data-reader-action="study"]').getAttribute('aria-current'),
      open: [...document.querySelectorAll('[data-reader-surface]')].some(node => node.open),
      events: [...document.querySelectorAll('[data-semantic-event-id]')].map(node => node.dataset.semanticEventId) })`);
    assert.equal(studied.mode, 'study');
    assert.equal(studied.location, target);
    assert.equal(studied.focus, 'study');
    assert.equal(studied.current, 'true');
    assert.equal(studied.open, false);
    assert.deepEqual(studied.events, before);
    assertions.push(entrance + ' direct keyboard Study preserves deep Proper and focus');

    const prior = await evaluate(cdp, `({ hash: location.hash, renders: ${debug}.renders, y: scrollY })`);
    await key(cdp, ' ');
    const same = await evaluate(cdp, `({ hash: location.hash, renders: ${debug}.renders, y: scrollY,
      focus: document.activeElement.dataset.readerAction })`);
    assert.equal(same.hash, prior.hash);
    assert.equal(same.renders, prior.renders);
    assert.ok(Math.abs(same.y - prior.y) < 2);
    assert.equal(same.focus, 'study');
    assertions.push(entrance + ' current Study command does not restart or move reading');

    await click('[data-reader-action="mode"]');
    await click('[data-reader-action="details"]');
    await waitFor(cdp, `document.getElementById('details-surface').open &&
      document.querySelector('[data-reader-share-print]')`, 'secondary Details');
    assert.equal(await evaluate(cdp, `document.getElementById('mode-surface').open`), false);
    assert.deepEqual(await evaluate(cdp, `[...document.querySelectorAll('[data-reader-share-print] button')]
      .map(button => button.textContent)`), ['Share link', 'Print']);
    await key(cdp, 'Escape');
    assert.equal(await evaluate(cdp, 'document.activeElement.dataset.readerAction'), 'mode');
    assert.equal(await evaluate(cdp, 'location.hash'), prior.hash);
    assertions.push(entrance + ' secondary Details retains Share Print and returns focus to Mode');

    await click('[data-reader-action="mode"]');
    await click('[data-mode="missal"]');
    await ready('missal');
    await jump("/gospel/i.test(button.textContent)");
    await click('[data-reader-action="study"]');
    await ready('study');
    assert.equal(await evaluate(cdp, `new URLSearchParams(location.hash.slice(1)).get('location')`), target);
    assert.equal(await evaluate(cdp, 'document.activeElement.dataset.readerAction'), 'study');
    assertions.push(entrance + ' Missal direct Study retains matching Proper');

    await visit(entrance === 'day'
      ? '&mode=compare&compare=recension&peer-missal=postconciliar&territory=universal&ordinary=0'
      : '&mode=compare&compare=oration-language&peer-orations=en');
    await ready('compare');
    await jump("button.dataset.readerLocation.endsWith('/gospel')");
    await click('[data-reader-action="study"]');
    await ready('study');
    const compared = await evaluate(cdp, `({ location: new URLSearchParams(location.hash.slice(1)).get('location'),
      hash: location.hash, focus: document.activeElement.dataset.readerAction })`);
    assert.equal(compared.location, target);
    assert.equal(compared.focus, 'study');
    assert.doesNotMatch(compared.hash, /(?:compare|peer-missal|peer-orations|territory)=/);
    await cdp.send('Emulation.setDeviceMetricsOverride', {
      width: 320, height: 852, deviceScaleFactor: 1, mobile: false
    });
    assert.equal(await evaluate(cdp,
      'document.documentElement.scrollWidth > document.documentElement.clientWidth + 1'), false);
    assertions.push(entrance + ' Compare direct Study maps Proper and reflows at 320 pixels');
  }
  assert.deepEqual(consoleProblems, []);
  assert.deepEqual(failedRequests, []);
  assert.deepEqual(httpProblems, []);
  process.stdout.write(JSON.stringify({ status: 'pass', checks: assertions.length, assertions,
    consoleProblems, failedRequests, httpProblems }) + '\n');
} catch (error) {
  const state = cdp ? await evaluate(cdp, `(() => {
    const debug = window.dayReaderDebug || window.propersReaderDebug || {};
    return { hash: location.hash, title: document.title, ready: debug.ready,
      outcome: debug.outcome, error: debug.error, focus: document.activeElement?.outerHTML };
  })()`).catch(() => null) : null;
  process.stderr.write(JSON.stringify({ status: 'fail', error: error.stack, state,
    assertions, consoleProblems, failedRequests, httpProblems }) + '\n');
  process.exitCode = 1;
} finally {
  if (cdp) cdp.close();
  const stopped = new Promise((done) => chrome.once('exit', done));
  chrome.kill('SIGTERM');
  await stopped;
  await new Promise((done) => instance.close(done));
  await rm(profile, { recursive: true, force: true, maxRetries: 4, retryDelay: 100 });
}
