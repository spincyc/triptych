#!/usr/bin/env node

/* A partial Proper witness survives Read and Missal with independent Ordinary language. */

import assert from 'node:assert/strict';
import { spawn } from 'node:child_process';
import { createServer } from 'node:http';
import { mkdir, mkdtemp, readFile, rm } from 'node:fs/promises';
import { extname, resolve, sep } from 'node:path';

const ROOT = resolve(process.env.TRIPTYCH_REVIEW_ROOT || resolve(import.meta.dirname, '../..'));
const OVERLAY = process.env.TRIPTYCH_WITNESS_MODULE_ROOT;
const CHROME = process.env.TRIPTYCH_CHROME || '/usr/bin/chromium';
const SCRATCH = resolve(process.env.TRIPTYCH_BROWSER_SCRATCH ||
  resolve(ROOT, '.scratch/reader-witness-mode/browser'));
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
const chrome = spawn(CHROME, ['--headless=new', '--disable-gpu', '--no-sandbox', '--disable-dev-shm-usage',
  `--remote-debugging-port=${debugPort}`, `--user-data-dir=${profile}`, 'about:blank'], { stdio: 'ignore' });
let cdp;
const assertions = [], consoleProblems = [], failedRequests = [], httpProblems = [];
try {
  const pages = await waitJson(`http://127.0.0.1:${debugPort}/json`);
  cdp = new CDP(pages.find((page) => page.type === 'page').webSocketDebuggerUrl); await cdp.ready();
  cdp.on('Runtime.exceptionThrown', ({ exceptionDetails }) => consoleProblems.push(exceptionDetails?.exception?.description || exceptionDetails?.text));
  cdp.on('Runtime.consoleAPICalled', ({ type, args }) => { if (type === 'error' || type === 'warning') consoleProblems.push(args.map((one) => one.value || one.description || '').join(' ')); });
  cdp.on('Network.loadingFailed', ({ canceled, errorText }) => { if (!canceled) failedRequests.push(errorText); });
  cdp.on('Network.responseReceived', ({ response }) => { if (response?.status >= 400) httpProblems.push({ status: response.status, url: response.url }); });
  await Promise.all([cdp.send('Page.enable'), cdp.send('Runtime.enable'), cdp.send('Network.enable')]);
  await cdp.send('Page.addScriptToEvaluateOnNewDocument', { source: `Storage.prototype.getItem = function () { throw new Error('storage unavailable'); }; Storage.prototype.setItem = function () { throw new Error('storage unavailable'); };` });
  await cdp.send('Emulation.setDeviceMetricsOverride', { width: 393, height: 852, deviceScaleFactor: 1, mobile: false });
  const base = `http://127.0.0.1:${port}`;
  const key = 'commemoratione-omnium-fidelium-defunctorum';
  const caswall = 'edition.edward-caswall.lyra-catholica.london-1849';
  const identity = '#missal=roman-1962&type=sanctoral&mass=' + key + '&form=first&bible=douay-rheims&orations=en&translation-witness=' + caswall;
  const ready = async () => waitFor(cdp, `window.propersReaderDebug?.ready && document.getElementById('reader-document').getAttribute('aria-busy') === 'false'`, 'settled Propers');
  const click = async (selector) => evaluate(cdp, `document.querySelector(${JSON.stringify(selector)}).click()`);
  async function visit(suffix = '', hash = identity) { await cdp.send('Page.navigate', { url: base + PROPERS + '?data=/src/web/data' + hash + suffix }); await ready(); }
  async function capture() {
    return evaluate(cdp, `(() => { const events = propersReaderDebug.semantic?.events || [];
      const proper = name => events.find(event => event.kind === 'proper' && event.editionSlotLabel === name);
      return { outcome: propersReaderDebug.outcome, state: propersReaderDebug.state, hash: location.hash,
        error: propersReaderDebug.error, loads: propersReaderDebug.loads,
        sequence: proper('Sequence')?.selected, collect: proper('Collect')?.selected,
        collectAbsences: [...(document.querySelector('[data-semantic-event-id="proper/roman-1962/${key}/002"]')?.querySelectorAll('[data-unit-absence]') || [])].flatMap(node => node.dataset.unitAbsence.split(' ')),
        ordinary: events.filter(event => event.kind === 'ordinary-element').map(event => event.selected),
        focus: document.activeElement?.dataset.readerAction };
    })()`);
  }
  function partial(value) {
    assert.equal(value.outcome, 'ready', JSON.stringify(value.error));
    assert.equal(value.state.languages.translationWitness, caswall);
    assert.equal(value.sequence.availability, 'held'); assert.equal(value.sequence.sourceId, caswall); assert.ok(value.sequence.text);
    assert.equal(value.collect.availability, 'unavailable'); assert.equal(value.collect.text, null);
    assert.ok(value.collectAbsences.includes('en:absent-in-witness'), JSON.stringify({ absences: value.collectAbsences, collect: value.collect }));
  }
  await visit(); const read = await capture(); partial(read);
  assert.equal(read.loads['structure/propers/catalog/roman-1962.json'], 1);
  assert.equal(read.loads['structure/propers/mass/roman-1962/' + key + '.json'], 1);
  assert.equal(read.loads['structure/propers/roman-1962.json'] || 0, 0);
  assert.equal(read.loads['structure/ordinary/roman-1962.json'] || 0, 0);
  assertions.push('split All Souls first-form Read accepts partial Caswall and preserves the Collect absence');

  await click('[data-reader-action="mode"]'); await click('[data-mode="missal"]'); await ready();
  const missal = await capture(); partial(missal);
  assert.equal(missal.state.requestedMode, 'missal'); assert.equal(missal.state.languages.ordinary, 'en');
  assert.equal(missal.loads['structure/propers/roman-1962.json'], 1);
  assert.equal(missal.loads['structure/ordinary/roman-1962.json'], 1);
  assert.ok(missal.ordinary.some(selected => selected.availability === 'held'));
  assert.ok(missal.ordinary.every(selected => selected.sourceId !== caswall));
  assert.equal(missal.focus, 'mode');
  assert.deepEqual(missal.sequence, read.sequence); assert.deepEqual(missal.collect, read.collect);
  await click('[data-reader-action="mode"]'); await click('[data-mode="read"]'); await ready();
  const returned = await capture(); partial(returned); assert.equal(returned.state.requestedMode, 'read');
  assertions.push('first Missal transition and return to Read retain the same partial Proper witness independently of English Ordinary');

  await visit('&mode=missal&ordinary-lang=la'); const latinOrdinary = await capture(); partial(latinOrdinary);
  assert.equal(latinOrdinary.state.languages.ordinary, 'la');
  assert.ok(latinOrdinary.ordinary.some(selected => selected.availability === 'held' && selected.language === 'la'));
  assert.deepEqual(latinOrdinary.sequence, read.sequence); assert.deepEqual(latinOrdinary.collect, read.collect);
  assertions.push('direct Missal links keep English Caswall Propers while selecting Latin Ordinary separately');

  for (const hash of [identity.replace(caswall, 'not-held'), identity.replace('orations=en', 'orations=la')]) {
    await visit('&mode=missal', hash);
    assert.equal(await evaluate(cdp, 'propersReaderDebug.outcome'), 'invalid');
    assert.equal(await evaluate(cdp, 'document.querySelectorAll("#reader-document [data-semantic-event-id]").length'), 0);
  }
  assertions.push('unknown witnesses and translation-witness misuse on Latin source language still fail closed');
  assert.deepEqual(consoleProblems, []); assert.deepEqual(failedRequests, []); assert.deepEqual(httpProblems, []);
  process.stdout.write(JSON.stringify({ status: 'pass', checks: assertions.length, assertions, consoleProblems, failedRequests, httpProblems }) + '\n');
} catch (error) {
  const state = cdp ? await evaluate(cdp, `({ hash: location.hash, debug: window.propersReaderDebug })`).catch(() => null) : null;
  process.stderr.write(JSON.stringify({ status: 'fail', error: error.stack, state, assertions, consoleProblems, failedRequests, httpProblems }) + '\n'); process.exitCode = 1;
} finally {
  if (cdp) cdp.close(); const stopped = new Promise((done) => chrome.once('exit', done)); chrome.kill('SIGTERM'); await stopped;
  await new Promise((done) => instance.close(done)); await rm(profile, { recursive: true, force: true, maxRetries: 4, retryDelay: 100 });
}
