#!/usr/bin/env node

/* Propers compares explicitly selected held cycles without calendar or text fallback. */

import assert from 'node:assert/strict';
import { spawn } from 'node:child_process';
import { createServer } from 'node:http';
import { mkdir, mkdtemp, readFile, rm } from 'node:fs/promises';
import { extname, resolve, sep } from 'node:path';

const ROOT = resolve(process.env.TRIPTYCH_REVIEW_ROOT || resolve(import.meta.dirname, '../..'));
const OVERLAY = process.env.TRIPTYCH_CYCLE_MODULE_ROOT;
const CHROME = process.env.TRIPTYCH_CHROME || '/usr/bin/chromium';
const SCRATCH = resolve(process.env.TRIPTYCH_BROWSER_SCRATCH ||
  resolve(ROOT, '.scratch/reader-cycle-compare/browser'));
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
      const body = OVERLAY ? await readFile(resolve(OVERLAY, relative)).catch(() => readFile(file))
        : await readFile(file);
      response.end(body);
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
  const identity = '#missal=postconciliar&type=christological&mass=transfiguration-lord&bible=douay-rheims&orations=la';
  const comparison = '&mode=compare&compare=lectionary-cycle&cycle=A&peer-cycle=B';
  async function ready(outcome = 'ready') {
    await waitFor(cdp, `window.propersReaderDebug?.ready && propersReaderDebug.outcome === '${outcome}' &&
      document.getElementById('reader-document').getAttribute('aria-busy') === 'false'`, 'Propers ' + outcome);
  }
  async function visit(suffix, path = PROPERS) {
    await cdp.send('Page.navigate', { url: base + path + '?data=/src/web/data' + identity + suffix });
  }
  async function click(selector) {
    await evaluate(cdp, `document.querySelector(${JSON.stringify(selector)}).click()`);
  }
  async function select(selector, value) {
    await evaluate(cdp, `(() => { const node = document.querySelector(${JSON.stringify(selector)});
      node.value = ${JSON.stringify(value)}; node.dispatchEvent(new Event('change', { bubbles: true })); })()`);
  }
  const projections = [];
  for (const path of [PROPERS, '/src/web/browser/liturgy/propers-reader.html']) {
    await visit(comparison + '&location=compare%2Fproper%2Fgospel', path);
    await ready();
    const value = await evaluate(cdp, `({ state: propersReaderDebug.state, semantic: propersReaderDebug.semantic,
      hash: location.hash, title: document.title,
      refs: [...document.querySelectorAll('[data-semantic-event-id="compare/proper/gospel"] .compare-side')]
        .map(side => ({ id: side.dataset.compareSide, text: side.textContent })),
      contents: [...document.querySelectorAll('[data-reader-location]')].map(row => row.dataset.readerLocation),
      ordinary: Object.keys(propersReaderDebug.loads).filter(path => path.includes('structure/ordinary/') && !path.endsWith('/index.json')) })`);
    assert.equal(value.state.requestedMode, 'compare');
    assert.equal(value.state.civilDate, null);
    assert.equal(value.state.cycle, 'A');
    assert.deepEqual(value.semantic.sides.map(side => side.id), ['A', 'B']);
    assert.equal(value.semantic.calendarResults, null);
    assert.equal(value.semantic.units.length, 5);
    assert.match(value.refs[0].text, /Cycle A/);
    assert.match(value.refs[0].text, /Matthew 17:1/);
    assert.match(value.refs[1].text, /Cycle B/);
    assert.match(value.refs[1].text, /Mark 9:2/);
    assert.deepEqual(value.contents, value.semantic.units.map(unit => 'compare/proper/' + unit.semanticSlot));
    assert.equal(value.ordinary.length, 0);
    assert.match(value.hash, /peer-cycle=B/);
    assert.doesNotMatch(value.hash, /peer-orations/);
    projections.push(value.semantic);
  }
  assert.deepEqual(projections[0], projections[1]);
  assertions.push('canonical and retained Propers routes resolve the same explicit date-free cycle comparison');

  await visit('&mode=read'); await ready();
  await click('[data-reader-action="mode"]'); await click('[data-mode="compare"]');
  await select('#reader-compare-dimension', 'lectionary-cycle');
  const choices = await evaluate(cdp, `({ primary: document.getElementById('reader-compare-cycle').value,
    peer: document.getElementById('reader-compare-peer-cycle').value,
    values: [...document.getElementById('reader-compare-cycle').options].map(option => option.value),
    languageHidden: document.getElementById('reader-compare-orations').closest('.surface-field').hidden })`);
  assert.equal(choices.primary, ''); assert.equal(choices.peer, '');
  assert.deepEqual(choices.values, ['', 'A', 'B', 'C']); assert.equal(choices.languageHidden, true);
  await select('#reader-compare-cycle', 'A'); await select('#reader-compare-peer-cycle', 'A');
  await click('#compare-setup .surface-apply');
  assert.equal(await evaluate(cdp, 'propersReaderDebug.state.requestedMode'), 'read');
  assert.match(await evaluate(cdp, 'document.getElementById("compare-setup-note").textContent'), /different held cycles/);
  await select('#reader-compare-peer-cycle', 'C'); await click('#compare-setup .surface-apply');
  await ready();
  assert.equal(await evaluate(cdp, 'propersReaderDebug.state.comparison.sides[1].cycle'), 'C');
  assert.match(await evaluate(cdp,
    `document.querySelector('[data-semantic-event-id="compare/proper/gospel"] .compare-side:last-child').textContent`), /Luke 9:28/);
  assertions.push('cycle controls leave coequal choices blank and require distinct explicit selections');

  await cdp.send('Emulation.setDeviceMetricsOverride', {
    width: 320, height: 852, deviceScaleFactor: 1, mobile: false
  });
  assert.equal(await evaluate(cdp, 'document.documentElement.scrollWidth > document.documentElement.clientWidth + 1'), false);
  assert.equal(await evaluate(cdp, `(() => { const sides = [...document.querySelectorAll('.compare-unit:last-child .compare-side')];
    return sides[1].getBoundingClientRect().top >= sides[0].getBoundingClientRect().bottom; })()`), true);
  assertions.push('320-pixel cycle comparison stacks each semantic pair without page overflow');

  await visit(comparison + '&location=compare%2Fproper%2Fgospel'); await ready();
  await waitFor(cdp, `document.querySelector('[data-semantic-event-id="compare/proper/gospel"]')
    ?.getBoundingClientRect().top <= 280`, 'restored Gospel comparison');
  await evaluate(cdp, `(async () => { for (let frame = 0; frame < 12; frame += 1)
    await new Promise(requestAnimationFrame); })()`);
  await click('[data-reader-action="study"]'); await ready();
  const studied = await evaluate(cdp, `({ mode: propersReaderDebug.state.requestedMode,
    location: propersReaderDebug.state.semanticLocation?.eventId, hash: location.hash })`);
  assert.equal(studied.mode, 'study'); assert.match(studied.location, /transfiguration-lord\/005$/);
  assert.doesNotMatch(studied.hash, /(?:compare|peer-cycle|peer-orations)=/);
  assert.match(studied.hash, /cycle=A/);
  assertions.push('return to Study preserves the primary cycle and corresponding Gospel location');

  for (const suffix of [comparison.replace('peer-cycle=B', 'peer-cycle=Z'),
    comparison.replace('peer-cycle=B', 'peer-cycle=A'), comparison.replace('&peer-cycle=B', ''),
    comparison + '&peer-orations=en']) {
    await visit(suffix); await ready('invalid');
    assert.equal(await evaluate(cdp, 'document.querySelectorAll(".compare-unit").length'), 0);
  }
  assertions.push('unknown equal missing and wrong-dimension peers fail closed without compared text');

  await cdp.send('Page.navigate', { url: base + PROPERS + '?data=/src/web/data' +
    '#missal=roman-1962&type=seasonal&mass=advent-1&bible=douay-rheims&orations=la&mode=compare&compare=oration-language&peer-orations=en' });
  await ready();
  assert.equal(await evaluate(cdp, 'propersReaderDebug.state.comparison.dimension'), 'oration-language');
  assert.deepEqual(await evaluate(cdp, 'propersReaderDebug.semantic.sides.map(side => side.id)'), ['la', 'en']);
  await click('[data-reader-action="mode"]'); await click('[data-mode="read"]'); await ready();
  assert.doesNotMatch(await evaluate(cdp, 'location.hash'), /(?:compare|peer-cycle|peer-orations)=/);
  assertions.push('existing oration-language comparison and return to Read remain available');

  await visit(comparison); await ready();
  await click('[data-reader-action="mode"]'); await click('[data-mode="read"]'); await ready();
  assert.equal(await evaluate(cdp, 'propersReaderDebug.state.requestedMode'), 'read');
  assert.equal(await evaluate(cdp, 'propersReaderDebug.state.cycle'), 'A');
  assert.doesNotMatch(await evaluate(cdp, 'location.hash'), /(?:compare|peer-cycle|peer-orations)=/);
  await click('[data-reader-action="mode"]'); await click('[data-mode="missal"]'); await ready();
  assert.equal(await evaluate(cdp, 'propersReaderDebug.state.requestedMode'), 'missal');
  assert.equal(await evaluate(cdp, 'propersReaderDebug.state.cycle'), 'A');
  await click('[data-reader-action="mode"]'); await click('[data-mode="read"]'); await ready();
  assert.equal(await evaluate(cdp, 'propersReaderDebug.state.requestedMode'), 'read');
  assert.doesNotMatch(await evaluate(cdp, 'location.hash'), /(?:compare|peer-cycle|peer-orations)=/);
  assertions.push('canonical cycle Compare clears peer state through Read and Missal transitions');

  await cdp.send('Page.navigate', { url: base +
    '/src/web/browser/liturgy/reader-visual-reset-propers.html?design=instrument&data=/src/web/data' +
    '#missal=roman-1962&type=seasonal&mass=advent-1&bible=douay-rheims&orations=la&mode=missal' });
  await ready();
  assert.equal(await evaluate(cdp, 'typeof window.TriptychPropersCompare'), 'undefined');
  assert.equal(await evaluate(cdp, 'propersReaderDebug.state.requestedMode'), 'missal');
  assert.equal(await evaluate(cdp, 'document.querySelectorAll(".ordinary-element").length > 0'), true);
  await click('[data-reader-action="mode"]'); await click('[data-mode="read"]'); await ready();
  assert.equal(await evaluate(cdp, 'propersReaderDebug.state.requestedMode'), 'read');
  assert.equal(await evaluate(cdp, 'document.querySelectorAll(".ordinary-element").length'), 0);
  assert.match(await evaluate(cdp, 'location.hash'), /mode=read/);
  assertions.push('retained visual oracle without Compare returns from an explicit Missal link to Read');

  assert.deepEqual(consoleProblems, []); assert.deepEqual(failedRequests, []); assert.deepEqual(httpProblems, []);
  process.stdout.write(JSON.stringify({ status: 'pass', checks: assertions.length, assertions,
    consoleProblems, failedRequests, httpProblems }) + '\n');
} catch (error) {
  const state = cdp ? await evaluate(cdp, `({ hash: location.hash, title: document.title,
    debug: window.propersReaderDebug, text: document.getElementById('reader-document')?.textContent })`).catch(() => null) : null;
  process.stderr.write(JSON.stringify({ status: 'fail', error: error.stack, state,
    assertions, consoleProblems, failedRequests, httpProblems }) + '\n');
  process.exitCode = 1;
} finally {
  if (cdp) cdp.close();
  const stopped = new Promise((done) => chrome.once('exit', done));
  chrome.kill('SIGTERM'); await stopped;
  await new Promise((done) => instance.close(done));
  await rm(profile, { recursive: true, force: true, maxRetries: 4, retryDelay: 100 });
}
