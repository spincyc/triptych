#!/usr/bin/env node

/* Source-served keyboard check for the shared Day/Propers mode radiogroup. */

import assert from 'node:assert/strict';
import { spawn } from 'node:child_process';
import { createServer } from 'node:http';
import { mkdtemp, mkdir, readFile, rm } from 'node:fs/promises';
import { extname, resolve, sep } from 'node:path';

const ROOT = resolve(import.meta.dirname, '../..');
const CHROME = process.env.TRIPTYCH_CHROME || '/usr/bin/chromium';
const SCRATCH = resolve(process.env.TRIPTYCH_BROWSER_SCRATCH ||
  resolve(ROOT, '.scratch/reader-mode-keyboard'));
const pages = [
  { path: '/src/web/browser/liturgy/day.html', ready: 'dayReaderReady',
    mode: 'dayReaderDebug.mode',
    state: '#date=2026-11-22&missal=roman-1962&bible=douay-rheims&orations=la&mode=read&ordinary=0' },
  { path: '/src/web/browser/liturgy/index.html', ready: 'propersReaderReady',
    mode: 'propersReaderDebug.state?.requestedMode',
    state: '#missal=roman-1962&type=seasonal&mass=pentecost&bible=douay-rheims&orations=la&mode=read' }
];

function server() {
  return createServer(async (request, response) => {
    try {
      let path = decodeURIComponent(new URL(request.url, 'http://localhost').pathname)
        .replace(/^\/+/, '');
      if (path === 'favicon.ico') { response.writeHead(204); response.end(); return; }
      if (/^src\/web\/data\/[^/]+\/chapters\//.test(path)) {
        path = path.replace(/^src\/web\/data\//, 'src/sources/bibles/');
      }
      const file = resolve(ROOT, path || 'README.md');
      if (!file.startsWith(ROOT + sep)) throw new Error('outside root');
      const mime = ({ '.css': 'text/css', '.html': 'text/html', '.js': 'text/javascript',
        '.json': 'application/json' })[extname(file)] || 'application/octet-stream';
      response.writeHead(200, { 'content-type': mime, 'cache-control': 'no-store' });
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

async function waitJson(url) {
  for (let i = 0; i < 120; i += 1) {
    try { const response = await fetch(url); if (response.ok) return response.json(); }
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
  }
  async ready() {
    await new Promise((done, reject) => {
      this.socket.addEventListener('open', done, { once: true });
      this.socket.addEventListener('error', reject, { once: true });
    });
    this.socket.addEventListener('message', (event) => {
      const message = JSON.parse(event.data);
      if (!message.id) return;
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
      const timer = setTimeout(() => reject(new Error('CDP timeout: ' + method)), 30000);
      this.pending.set(id, { resolve, reject, timer });
      this.socket.send(JSON.stringify({ id, method, params }));
    });
  }
  close() { this.socket.close(); }
}

async function evaluate(cdp, expression) {
  const result = await cdp.send('Runtime.evaluate', {
    expression, awaitPromise: true, returnByValue: true, userGesture: true
  });
  if (result.exceptionDetails) throw new Error(
    result.exceptionDetails.exception?.description || result.exceptionDetails.text
  );
  return result.result.value;
}

async function waitFor(cdp, expression, label) {
  for (let i = 0; i < 240; i += 1) {
    if (await evaluate(cdp, `Boolean(${expression})`)) return;
    await new Promise((done) => setTimeout(done, 50));
  }
  throw new Error('Timed out waiting for ' + label);
}

async function key(cdp, name, shift = false) {
  const details = { Tab: ['Tab', 9], ArrowRight: ['ArrowRight', 39],
    ArrowDown: ['ArrowDown', 40], End: ['End', 35], Home: ['Home', 36],
    Enter: ['Enter', 13], Space: ['Space', 32] }[name];
  const value = name === 'Space' ? ' ' : details[0];
  for (const type of ['keyDown', 'keyUp']) {
    await cdp.send('Input.dispatchKeyEvent', {
      type, key: value, code: details[0], windowsVirtualKeyCode: details[1],
      nativeVirtualKeyCode: details[1],
      modifiers: shift ? 8 : 0
    });
  }
}

function snapshot() {
  return `(() => ({ focus: document.activeElement.hasAttribute('data-reader-close') ? 'close' :
      document.activeElement.dataset.mode || document.activeElement.dataset.readerAction ||
      document.activeElement.id || null,
    checked: [...document.querySelectorAll('[role="radiogroup"] [role="radio"]')]
      .filter(node => node.getAttribute('aria-checked') === 'true').map(node => node.dataset.mode),
    tabs: [...document.querySelectorAll('[role="radiogroup"] [role="radio"]')]
      .filter(node => node.tabIndex === 0).map(node => node.dataset.mode),
    setup: !document.getElementById('compare-setup').hidden,
    open: document.getElementById('mode-surface').open }))()`;
}

const instance = server();
const port = await listen(instance);
const debugPort = await (async () => {
  const probe = server(); const free = await listen(probe);
  await new Promise((done) => probe.close(done)); return free;
})();
await mkdir(SCRATCH, { recursive: true });
const profile = await mkdtemp(resolve(SCRATCH, 'chromium-'));
const chrome = spawn(CHROME, [
  '--headless=new', '--disable-gpu', '--no-sandbox', '--disable-dev-shm-usage',
  `--remote-debugging-port=${debugPort}`, `--user-data-dir=${profile}`, 'about:blank'
], { stdio: 'ignore' });
let cdp;
let checks = 0;
try {
  const targets = await waitJson(`http://127.0.0.1:${debugPort}/json`);
  cdp = new CDP(targets.find((row) => row.type === 'page').webSocketDebuggerUrl);
  await cdp.ready();
  await Promise.all([cdp.send('Page.enable'), cdp.send('Runtime.enable')]);
  for (const page of pages) {
    const url = `http://127.0.0.1:${port}${page.path}?data=/src/web/data${page.state}`;
    await cdp.send('Page.navigate', { url });
    await waitFor(cdp, `window.${page.ready} === true &&
      window.TriptychReaderModeKeyboard && ${page.mode} === 'read'`, page.path + ' ready');
    await evaluate(cdp, `(() => { window.__modeClicks = 0;
      document.querySelector('[data-mode="read"]').addEventListener('click', () =>
        window.__modeClicks++); })()`);
    assert.deepEqual((await evaluate(cdp, snapshot())).tabs, ['read']);
    checks += 1;

    await evaluate(cdp, `document.querySelector('[data-reader-action="mode"]').click()`);
    await key(cdp, 'Tab'); // The checked radio is the only Tab stop in the group.
    assert.equal((await evaluate(cdp, snapshot())).focus, 'read');
    await key(cdp, 'Tab');
    assert.equal((await evaluate(cdp, snapshot())).focus, 'reader-text-size');
    await key(cdp, 'Tab');
    assert.equal((await evaluate(cdp, snapshot())).focus, 'details');
    await key(cdp, 'Tab');
    assert.equal((await evaluate(cdp, snapshot())).focus, 'close');
    await key(cdp, 'Tab', true);
    assert.equal((await evaluate(cdp, snapshot())).focus, 'details');
    await key(cdp, 'Tab', true);
    assert.equal((await evaluate(cdp, snapshot())).focus, 'reader-text-size');
    await key(cdp, 'Tab', true);
    assert.equal((await evaluate(cdp, snapshot())).focus, 'read');
    checks += 1;

    await key(cdp, 'ArrowRight');
    await waitFor(cdp, `${page.mode} === 'missal' &&
      document.querySelector('[data-mode="missal"]').getAttribute('aria-checked') === 'true'`,
    page.path + ' Missal');
    assert.deepEqual((await evaluate(cdp, snapshot())).tabs, ['missal']);
    checks += 1;

    await evaluate(cdp, `document.querySelector('[data-reader-action="mode"]').click()`);
    await key(cdp, 'Tab');
    assert.equal((await evaluate(cdp, snapshot())).focus, 'missal');
    await key(cdp, 'ArrowDown');
    await waitFor(cdp, `${page.mode} === 'study'`, page.path + ' Study');
    assert.deepEqual((await evaluate(cdp, snapshot())).tabs, ['study']);
    checks += 1;

    await evaluate(cdp, `document.querySelector('[data-reader-action="mode"]').click()`);
    await key(cdp, 'Tab');
    await key(cdp, 'End');
    const compare = await evaluate(cdp, snapshot());
    assert.equal(compare.setup, true);
    assert.deepEqual(compare.checked, ['study']); // Compare needs a completed setup.
    assert.match(compare.focus, /^reader-compare-/);
    assert.equal(await evaluate(cdp, page.mode), 'study');
    // Compare adds its own form fields between the roving group and the
    // preferences. Tab still reaches the shared secondary controls in order.
    for (let tabs = 0; tabs < 8; tabs += 1) {
      if ((await evaluate(cdp, snapshot())).focus === 'reader-text-size') break;
      await key(cdp, 'Tab');
    }
    assert.equal((await evaluate(cdp, snapshot())).focus, 'reader-text-size');
    await key(cdp, 'Tab');
    assert.equal((await evaluate(cdp, snapshot())).focus, 'details');
    await key(cdp, 'Tab');
    assert.equal((await evaluate(cdp, snapshot())).focus, 'close');
    checks += 1;

    await evaluate(cdp, `document.querySelector('#mode-surface [data-reader-close]').click()`);
    await evaluate(cdp, `document.querySelector('[data-reader-action="mode"]').click()`);
    assert.deepEqual((await evaluate(cdp, snapshot())).tabs, ['study']);
    await key(cdp, 'Tab');
    await key(cdp, 'Home');
    await waitFor(cdp, `${page.mode} === 'read'`, page.path + ' Read');
    assert.deepEqual((await evaluate(cdp, snapshot())).tabs, ['read']);
    checks += 1;

    for (const activation of ['Enter', 'Space']) {
      await evaluate(cdp, `document.querySelector('[data-reader-action="mode"]').click()`);
      await key(cdp, 'Tab');
      assert.equal((await evaluate(cdp, snapshot())).focus, 'read',
        page.path + ' before ' + activation);
      await evaluate(cdp, 'window.__modeClicks = 0');
      await key(cdp, activation);
      await waitFor(cdp, `!document.getElementById('mode-surface').open`,
        page.path + ' keyboard ' + activation);
      assert.equal(await evaluate(cdp, page.mode), 'read');
      assert.equal(await evaluate(cdp, 'window.__modeClicks'), 1);
      checks += 1;
    }

    await evaluate(cdp, `document.querySelector('[data-reader-action="mode"]').click()`);
    await key(cdp, 'Tab');
    await evaluate(cdp, `document.querySelector('[data-mode="missal"]')
      .setAttribute('aria-disabled', 'true')`);
    await key(cdp, 'ArrowRight');
    await waitFor(cdp, `${page.mode} === 'study'`, page.path + ' skip unavailable Missal');
    assert.deepEqual((await evaluate(cdp, snapshot())).tabs, ['study']);
    checks += 1;
  }
  process.stdout.write(JSON.stringify({ status: 'pass', checks }) + '\n');
} finally {
  if (cdp) cdp.close();
  chrome.kill('SIGTERM');
  await new Promise((done) => chrome.once('exit', done));
  await new Promise((done) => instance.close(done));
  await rm(profile, { recursive: true, force: true, maxRetries: 5, retryDelay: 100 });
}
