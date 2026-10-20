#!/usr/bin/env node

/* Source-served Chromium coverage for both reader Share/Print entrances. */

import assert from 'node:assert/strict';
import { spawn } from 'node:child_process';
import { createServer } from 'node:http';
import { mkdir, mkdtemp, readFile, rm } from 'node:fs/promises';
import { extname, resolve, sep } from 'node:path';

const ROOT = resolve(import.meta.dirname, '../..');
const CHROME = process.env.TRIPTYCH_CHROME || '/usr/bin/chromium';
const SCRATCH = resolve(process.env.TRIPTYCH_BROWSER_SCRATCH ||
  resolve(ROOT, '.scratch/reader-share-print-browser'));
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
const failures = [];
let activeCase = 'setup';
try {
  const pages = await waitJson(`http://127.0.0.1:${debugPort}/json`);
  cdp = new CDP(pages.find((page) => page.type === 'page').webSocketDebuggerUrl);
  await cdp.ready();
  cdp.on('Runtime.exceptionThrown', ({ exceptionDetails }) => {
    consoleProblems.push(exceptionDetails?.exception?.description ||
      exceptionDetails?.text || 'uncaught page exception');
  });
  cdp.on('Runtime.consoleAPICalled', ({ type, args }) => {
    if (type === 'error' || type === 'warning') {
      consoleProblems.push(args.map((one) => one.value || one.description || '').join(' '));
    }
  });
  cdp.on('Network.loadingFailed', ({ canceled, errorText, requestId }) => {
    failedRequests.push({ canceled: Boolean(canceled), errorText, requestId });
  });
  cdp.on('Network.responseReceived', ({ response }) => {
    if (response?.status >= 400) {
      httpProblems.push({ status: response.status, url: response.url });
    }
  });
  await Promise.all([cdp.send('Page.enable'), cdp.send('Runtime.enable'),
    cdp.send('Network.enable')]);
  await cdp.send('Page.addScriptToEvaluateOnNewDocument', { source: `
    Storage.prototype.getItem = function () { throw new Error('storage unavailable'); };
    Storage.prototype.setItem = function () { throw new Error('storage unavailable'); };
  ` });
  const base = `http://127.0.0.1:${port}`;

  async function check(entrance, hash) {
    const path = entrance === 'day' ? DAY : PROPERS;
    await cdp.send('Page.navigate', { url: base + path + '?data=/src/web/data' + hash });
    await waitFor(cdp, `window.${entrance}ReaderDebug?.ready &&
      document.querySelector('[data-reader-share-print]')`, entrance + ' reader');
    assert.equal(await evaluate(cdp, `${entrance}ReaderDebug.outcome`), 'ready',
      JSON.stringify(await evaluate(cdp, `${entrance}ReaderDebug.error`)));
    const before = await evaluate(cdp, 'location.href');
    const state = await evaluate(cdp, `${entrance}ReaderDebug.state`);
    assert.equal(state.entrance, entrance);
    await evaluate(cdp, `(() => {
      window.__shared = null;
      navigator.share = async (value) => { window.__shared = value; };
      window.__printed = 0;
      window.print = () => { window.__printed += 1; };
      document.querySelector('[data-reader-action="details"]').click();
    })()`);
    await waitFor(cdp, `document.querySelector('[data-reader-surface="details"]').open &&
      document.querySelector('[data-reader-share-print]')`, 'Details controls');
    const accessible = await evaluate(cdp, `(() => {
      const block = document.querySelector('[data-reader-share-print]');
      const buttons = [...block.querySelectorAll('button')];
      return { buttons: buttons.map((button) => ({ tag: button.tagName,
        type: button.type, tabIndex: button.tabIndex,
        visible: button.getClientRects().length > 0,
        label: button.textContent.trim() })),
        role: block.querySelector('[role="status"]')?.getAttribute('aria-live') };
    })()`);
    assert.deepEqual(accessible.buttons.map((button) => button.label), ['Share link', 'Print']);
    assert.ok(accessible.buttons.every((button) => button.tag === 'BUTTON' &&
      button.type === 'button' && button.tabIndex === 0 && button.visible));
    assert.equal(accessible.role, 'polite');
    await cdp.send('Input.dispatchKeyEvent', {
      type: 'keyDown', key: 'Tab', code: 'Tab', windowsVirtualKeyCode: 9
    });
    await cdp.send('Input.dispatchKeyEvent', {
      type: 'keyUp', key: 'Tab', code: 'Tab', windowsVirtualKeyCode: 9
    });
    assert.equal(await evaluate(cdp,
      `document.activeElement === document.querySelector('[data-reader-share-print] button')`), true);
    await cdp.send('Input.dispatchKeyEvent', {
      type: 'keyDown', key: ' ', code: 'Space', text: ' ', windowsVirtualKeyCode: 32
    });
    await cdp.send('Input.dispatchKeyEvent', {
      type: 'keyUp', key: ' ', code: 'Space', windowsVirtualKeyCode: 32
    });
    await waitFor(cdp, `window.__shared`, 'native share');
    const shared = await evaluate(cdp, 'window.__shared');
    assert.equal(shared.url, before);
    assert.deepEqual(Object.keys(shared).sort(), ['title', 'url']);
    assert.match(shared.title, new RegExp(state.edition.id));
    if (entrance === 'day') {
      assert.match(shared.title, /2026-11-22/);
      assert.match(shared.title, /Compare recension with postconciliar/);
      assert.match(shared.title, /universal/);
      assert.match(new URL(shared.url).hash, /territory=universal/);
    } else {
      assert.doesNotMatch(shared.title, /2026-11-22/);
      assert.equal(new URL(shared.url).hash.includes('date='), false);
    }
    assert.equal(await evaluate(cdp, 'location.href'), before);
    assert.equal(await evaluate(cdp,
      `document.querySelector('[data-reader-share-print] [role="status"]').textContent`),
    'Shared this reader link.');

    await evaluate(cdp, `(() => {
      navigator.share = undefined;
      Object.defineProperty(navigator, 'clipboard', { configurable: true,
        value: { writeText: async (value) => { window.__copied = value; } } });
      window.__copied = null;
      document.querySelector('[data-reader-share-print] button').click();
    })()`);
    await waitFor(cdp, 'window.__copied', 'clipboard fallback');
    assert.equal(await evaluate(cdp, 'window.__copied'), before);
    assert.equal(await evaluate(cdp,
      `document.querySelector('[data-reader-share-print] [role="status"]').textContent`),
    'Reader link copied to clipboard.');
    assert.equal(await evaluate(cdp,
      `document.activeElement === document.querySelector('[data-reader-share-print] button')`), true);
    await evaluate(cdp, `document.querySelectorAll('[data-reader-share-print] button')[1].click()`);
    assert.equal(await evaluate(cdp, 'window.__printed'), 1);
    assert.equal(await evaluate(cdp, 'location.href'), before);
    await cdp.send('Emulation.setEmulatedMedia', { media: 'print' });
    const printed = await evaluate(cdp, `(() => ({
      controls: getComputedStyle(document.querySelector('[data-reader-share-print]')).display,
      dialog: getComputedStyle(document.querySelector('[data-reader-surface="details"]')).display,
      title: getComputedStyle(document.querySelector('.reader-identity')).display,
      reading: getComputedStyle(document.querySelector('#reader-document')).display
    }))()`);
    assert.equal(printed.controls, 'none');
    assert.equal(printed.dialog, 'none');
    assert.notEqual(printed.title, 'none');
    assert.notEqual(printed.reading, 'none');
    const pdf = await cdp.send('Page.printToPDF', {
      printBackground: true, preferCSSPageSize: true
    });
    assert.ok(pdf.data.length > 10000, 'the selected reader generates a PDF');
    await cdp.send('Emulation.setEmulatedMedia', { media: 'screen' });
    await evaluate(cdp, `document.querySelector('[data-reader-details]').replaceChildren(
      document.createElement('p'))`);
    await waitFor(cdp, `document.querySelector('[data-reader-details]').firstElementChild?.
      hasAttribute('data-reader-share-print')`, 'Details reinsertion');
  }

  activeCase = 'day-compare-share-print';
  await check('day', '#date=2026-11-22&missal=roman-1962&bible=douay-rheims&orations=la' +
    '&mode=compare&compare=recension&peer-missal=postconciliar&territory=universal&ordinary=0');
  assertions.push({ name: activeCase, status: 'pass' });
  activeCase = 'propers-study-share-print';
  await check('propers', '#missal=roman-1962&type=seasonal&mass=advent-1' +
    '&bible=douay-rheims&orations=la&mode=study');
  assertions.push({ name: activeCase, status: 'pass' });
} catch (error) {
  const detail = error && error.stack || String(error);
  assertions.push({ name: activeCase, status: 'fail', detail });
  failures.push({ name: activeCase, detail });
} finally {
  if (cdp) cdp.close();
  chrome.kill('SIGTERM');
  if (chrome.exitCode === null && chrome.signalCode === null) {
    await new Promise((done) => chrome.once('exit', done));
  }
  await instance.close();
  await rm(profile, { recursive: true, force: true });
}
const unexpectedFailedRequests = failedRequests.filter((one) => !one.canceled);
const clean = failures.length === 0 && consoleProblems.length === 0 &&
  unexpectedFailedRequests.length === 0 && httpProblems.length === 0;
process.stdout.write(JSON.stringify({ status: clean ? 'pass' : 'fail',
  checks: assertions.filter((one) => one.status === 'pass').length,
  assertions, failures, consoleProblems, failedRequests, httpProblems }) + '\n');
if (!clean) process.exitCode = 1;
