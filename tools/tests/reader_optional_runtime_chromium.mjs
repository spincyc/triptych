#!/usr/bin/env node

/* Lazy Ordinary code preserves normalized state, eager oracles and render ownership. */

import assert from 'node:assert/strict';
import { spawn } from 'node:child_process';
import { createServer } from 'node:http';
import { mkdir, mkdtemp, readFile, rm } from 'node:fs/promises';
import { extname, resolve, sep } from 'node:path';

const ROOT = resolve(process.env.TRIPTYCH_REVIEW_ROOT || resolve(import.meta.dirname, '../..'));
const OVERLAY = process.env.TRIPTYCH_OPTIONAL_RUNTIME_MODULE_ROOT;
const CHROME = process.env.TRIPTYCH_CHROME || '/usr/bin/chromium';
const SCRATCH = resolve(process.env.TRIPTYCH_BROWSER_SCRATCH ||
  resolve(ROOT, '.scratch/reader-optional-runtime/browser'));
const policy = { behavior: 'normal', held: false, release: null };
const ordinaryPath = '/src/web/browser/liturgy/day.js';
const mime = (file) => ({ '.css': 'text/css', '.html': 'text/html',
  '.js': 'text/javascript', '.json': 'application/json' })[extname(file)] || 'application/octet-stream';

function server() {
  return createServer(async (request, response) => {
    try {
      const path = new URL(request.url, 'http://localhost').pathname;
      let relative = decodeURIComponent(path).replace(/^\/+/, '');
      if (relative === 'favicon.ico') { response.writeHead(204); response.end(); return; }
      if (path === ordinaryPath && policy.behavior === 'block') {
        response.writeHead(404, { 'x-triptych-test-blocked-ordinary': '1' });
        response.end('deliberately unavailable'); return;
      }
      if (path === ordinaryPath && policy.behavior === 'hold') {
        policy.held = true;
        await new Promise((done) => { policy.release = done; });
      }
      if (/^src\/web\/data\/[^/]+\/chapters\//.test(relative)) {
        relative = relative.replace(/^src\/web\/data\//, 'src/sources/bibles/');
      }
      const file = resolve(ROOT, relative || 'README.md');
      if (!file.startsWith(ROOT + sep)) throw new Error('outside repository');
      const body = OVERLAY ? await readFile(resolve(OVERLAY, relative)).catch(() => readFile(file))
        : await readFile(file);
      response.writeHead(200, { 'content-type': mime(file), 'cache-control': 'no-store' });
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
const expectedHttpProblems = [];
const expectedFailures = new Set();

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
  cdp.on('Network.responseReceived', ({ requestId, response }) => {
    if (response.status < 400) return;
    if (response.status === 404 && new URL(response.url).pathname === ordinaryPath &&
        response.headers['x-triptych-test-blocked-ordinary'] === '1') {
      expectedFailures.add(requestId);
      expectedHttpProblems.push({ status: response.status, path: ordinaryPath });
    } else httpProblems.push({ status: response.status, url: response.url });
  });
  cdp.on('Network.loadingFailed', ({ requestId, canceled, errorText }) => {
    if (!canceled && !expectedFailures.has(requestId)) failedRequests.push(errorText);
  });
  await Promise.all([cdp.send('Page.enable'), cdp.send('Runtime.enable'), cdp.send('Network.enable')]);
  await cdp.send('Page.addScriptToEvaluateOnNewDocument', { source: 'try { localStorage.clear(); } catch (_) {}' });
  const base = `http://127.0.0.1:${port}`;
  const snapshot = `(() => {
    const debug = window.dayReaderDebug || window.propersReaderDebug;
    const root = document.getElementById('reader-document');
    return { state: debug.state, outcome: debug.outcome, hash: location.hash,
      title: document.title, text: root.textContent,
      events: [...root.querySelectorAll('[data-semantic-event-id]')].map(node =>
        ({ id: node.dataset.semanticEventId, text: node.textContent })),
      ordinary: root.querySelectorAll('.ordinary-element').length };
  })()`;
  async function ready(generation = -1) {
    await waitFor(cdp, `(() => { const d = window.dayReaderDebug || window.propersReaderDebug;
      return d?.ready && d.renders > ${generation}; })()`, 'committed reader');
    return evaluate(cdp, snapshot);
  }
  async function visit(route, params) {
    await cdp.send('Page.navigate', { url: 'about:blank' });
    await cdp.send('Page.navigate', { url: `${base}/src/web/browser/liturgy/${route}?data=/src/web/data#${params}` });
    return ready();
  }
  async function change(params) {
    const generation = await evaluate(cdp, '(window.dayReaderDebug || window.propersReaderDebug).renders');
    await evaluate(cdp, `location.hash = ${JSON.stringify(params)}`);
    return ready(generation);
  }
  async function ordinaryRequests() {
    return evaluate(cdp, `performance.getEntriesByType('resource')
      .filter(entry => new URL(entry.name).pathname === ${JSON.stringify(ordinaryPath)}).length`);
  }
  for (const entrance of ['day', 'propers']) {
    const route = entrance === 'day' ? 'day.html' : 'index.html';
    const identity = entrance === 'day'
      ? 'date=2026-05-24&missal=roman-1962&bible=douay-rheims&orations=la'
      : 'missal=roman-1962&type=seasonal&mass=pentecost&bible=douay-rheims&orations=la';
    const read = identity + '&mode=read';
    const missal = identity + '&mode=missal&ordinary-lang=la';
    const plain = await visit(route, read);
    assert.equal(plain.outcome, 'ready');
    assert.equal(plain.state.options.ordinary, false);
    assert.ok(plain.events.length > 0);
    assert.equal(await ordinaryRequests(), 0);
    assert.equal(await evaluate(cdp, 'typeof TriptychOrdinaryRenderer'), 'undefined');
    assertions.push(entrance + ' Read displays its real Propers without requesting Ordinary code');

    const legacy = entrance === 'day' ? identity + '&ordinary=1&ordinary-lang=la' : missal;
    const framed = await visit(route, legacy);
    assert.equal(framed.outcome, 'ready');
    assert.equal(framed.state.options.ordinary, true);
    assert.ok(framed.ordinary > 0);
    assert.deepEqual(framed.events.filter(event => /^proper(?:-choice)?\//.test(event.id)), plain.events);
    assert.equal(await ordinaryRequests(), 1);
    assertions.push(entrance + ' requested Ordinary keeps the same Proper text and event order');

    if (entrance === 'day') {
      const studied = await visit(route, identity + '&mode=study&ordinary=1&ordinary-lang=la');
      assert.equal(studied.state.requestedMode, 'study');
      assert.equal(studied.state.options.ordinary, true);
      assert.ok(studied.ordinary > 0);
      assert.deepEqual(studied.events.map(event => event.id), framed.events.map(event => event.id));
      assert.equal(await ordinaryRequests(), 1);
      assertions.push('Day validated Study ordinary=1 loads its exact Ordinary event sequence');
    }

    const oracle = await visit(`reader-visual-reset-${entrance}.html`, legacy);
    assert.equal(await evaluate(cdp, 'typeof TriptychReaderOptionalRuntime'), 'undefined');
    assert.equal(oracle.state.options.ordinary, true);
    assert.deepEqual(oracle.events, framed.events);
    assert.equal(await ordinaryRequests(), 1);
    assertions.push(entrance + ' retained eager oracle works without the optional runtime');

    await visit(route, read);
    policy.behavior = 'hold'; policy.held = false;
    await evaluate(cdp, `location.hash = ${JSON.stringify(missal)}`);
    for (let attempt = 0; !policy.held && attempt < 120; attempt += 1) {
      await new Promise((done) => setTimeout(done, 25));
    }
    assert.equal(policy.held, true, 'Ordinary request reached the controlled response');
    const newer = await change(read);
    const generation = await evaluate(cdp, '(window.dayReaderDebug || window.propersReaderDebug).renders');
    policy.release(); policy.release = null; policy.behavior = 'normal';
    await waitFor(cdp, 'window.TriptychOrdinaryRenderer', 'released Ordinary presenter');
    await evaluate(cdp, 'new Promise(done => requestAnimationFrame(() => requestAnimationFrame(done)))');
    assert.deepEqual(await evaluate(cdp, snapshot), newer);
    assert.equal(await evaluate(cdp, '(window.dayReaderDebug || window.propersReaderDebug).renders'), generation);
    assert.ok((await change(missal)).ordinary > 0);
    assert.equal(await ordinaryRequests(), 1);
    assertions.push(entrance + ' old delayed code cannot replace newer Read and is reused by later Missal');

    policy.behavior = 'block';
    const failed = await visit(route, missal);
    assert.ok(!failed.state || (failed.state.requestedMode === 'missal' && failed.state.options.ordinary));
    assert.notEqual(failed.outcome, 'ready');
    assert.deepEqual(failed.events, []);
    assert.equal(new URLSearchParams(failed.hash.slice(1)).get('mode'), 'missal');
    const recovered = await change(read);
    assert.equal(recovered.outcome, 'ready');
    assert.equal(recovered.state.options.ordinary, false);
    assert.ok(recovered.events.length > 0);
    policy.behavior = 'normal';
    const retry = await change(missal);
    assert.equal(retry.outcome, 'ready');
    assert.ok(retry.ordinary > 0);
    assert.equal(await ordinaryRequests(), 2);
    assertions.push(entrance + ' failed Ordinary refuses Read fallback, allows Read recovery and retries Missal');
  }
  assert.equal(expectedHttpProblems.length, 2);
  assert.deepEqual(consoleProblems, []);
  assert.deepEqual(failedRequests, []);
  assert.deepEqual(httpProblems, []);
  process.stdout.write(JSON.stringify({ status: 'pass', checks: assertions.length, assertions,
    consoleProblems, failedRequests, httpProblems, expectedHttpProblems }) + '\n');
} catch (error) {
  process.stderr.write(JSON.stringify({ status: 'fail', error: error.stack, assertions,
    consoleProblems, failedRequests, httpProblems, expectedHttpProblems }) + '\n');
  process.exitCode = 1;
} finally {
  if (policy.release) policy.release();
  if (cdp) cdp.close();
  if (chrome.exitCode === null) {
    const stopped = new Promise((done) => chrome.once('exit', done));
    chrome.kill('SIGTERM'); await stopped;
  }
  await new Promise((done) => instance.close(done));
  await rm(profile, { recursive: true, force: true, maxRetries: 4, retryDelay: 100 });
}
