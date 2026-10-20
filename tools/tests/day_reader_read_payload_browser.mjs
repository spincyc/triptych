#!/usr/bin/env node

/* Source-served Chromium checks for the Day resolved Read payload. */

import assert from 'node:assert/strict';
import { spawn } from 'node:child_process';
import { createServer } from 'node:http';
import { mkdtemp, mkdir, readFile, rm } from 'node:fs/promises';
import { extname, resolve, sep } from 'node:path';

const ROOT = resolve(import.meta.dirname, '../..');
const CHROME = process.env.TRIPTYCH_CHROME || '/usr/bin/chromium';
const SCRATCH = resolve(process.env.TRIPTYCH_BROWSER_SCRATCH ||
  resolve(ROOT, '.scratch/day-read-payload-browser'));
const DAY = '/src/web/browser/liturgy/day.html';
const CANDIDATE = '/src/web/browser/liturgy/day-reader.html';
const PROTOTYPE = '/src/web/browser/liturgy/reader-visual-reset-day.html';

function mime(file) {
  return ({ '.css': 'text/css', '.html': 'text/html', '.js': 'text/javascript',
    '.json': 'application/json' })[extname(file)] || 'application/octet-stream';
}

let fault = null;
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
      let body = await readFile(file);
      if (fault === 'catalog-generation' && path.endsWith('/catalog/roman-1962.json')) {
        const changed = JSON.parse(body); changed.generation = '0'.repeat(64);
        body = JSON.stringify(changed);
      }
      if (fault === 'mass-descriptor' && path.endsWith('/mass/roman-1962/last-sunday-after-pentecost.json')) {
        const changed = JSON.parse(body); changed.mass.name = 'Mismatched source identity';
        body = JSON.stringify(changed);
      }
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
    this.events = new Map();
  }
  on(name, fn) { this.events.set(name, [...(this.events.get(name) || []), fn]); }
  async ready() {
    await new Promise((done, reject) => {
      this.socket.addEventListener('open', done, { once: true });
      this.socket.addEventListener('error', reject, { once: true });
    });
    this.socket.addEventListener('message', (event) => {
      const message = JSON.parse(event.data);
      if (!message.id) {
        for (const fn of this.events.get(message.method) || []) fn(message.params);
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

let sequence = 0;
async function visit(cdp, base, path, hash) {
  const url = `${base}${path}?data=/src/web/data&payload-test=${++sequence}${hash}`;
  await cdp.send('Page.navigate', { url });
  await waitFor(cdp, `performance.getEntriesByType('navigation')[0]?.name === ${JSON.stringify(url)} &&
    window.dayReaderReady === true`, path + ' ready');
  return evaluate(cdp, 'dayReaderDebug');
}

const baseState = '#date=2026-11-22&missal=roman-1962&bible=douay-rheims&orations=la';
const readState = baseState + '&mode=read&ordinary=0';
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
const consoleProblems = [];
const failedRequests = [];
const httpProblems = [];
try {
  const pages = await waitJson(`http://127.0.0.1:${debugPort}/json`);
  cdp = new CDP(pages.find((row) => row.type === 'page').webSocketDebuggerUrl);
  await cdp.ready();
  cdp.on('Runtime.exceptionThrown', ({ exceptionDetails }) => {
    consoleProblems.push(exceptionDetails?.exception?.description || exceptionDetails?.text);
  });
  cdp.on('Runtime.consoleAPICalled', ({ type, args }) => {
    if (type === 'error') consoleProblems.push(args.map((arg) => arg.value || arg.description).join(' '));
  });
  cdp.on('Network.loadingFailed', ({ canceled, errorText }) => {
    if (!canceled) failedRequests.push(errorText);
  });
  cdp.on('Network.responseReceived', ({ response }) => {
    if (response?.status >= 400) httpProblems.push(response.status + ' ' + response.url);
  });
  await Promise.all([cdp.send('Page.enable'), cdp.send('Runtime.enable'),
    cdp.send('Network.enable')]);
  const base = `http://127.0.0.1:${port}`;
  let fastText = null;
  let fastSemantic = null;
  for (const path of [DAY, CANDIDATE]) {
    const row = await visit(cdp, base, path, readState);
    assert.equal(row.outcome, 'ready', JSON.stringify(row.error));
    assert.equal(row.mode, 'read');
    assert.ok(row.loads['structure/propers/catalog/roman-1962.json']);
    assert.ok(row.loads['structure/propers/mass/roman-1962/last-sunday-after-pentecost.json']);
    assert.equal(row.loads['structure/propers/roman-1962.json'], undefined);
    const text = await evaluate(cdp, `Array.from(document.querySelectorAll('#reader-document [data-semantic-event-id]'))
      .map((node) => [node.dataset.semanticLocation, node.textContent.trim()])`);
    assert.ok(text.length > 0);
    if (fastText) assert.deepEqual(text, fastText);
    else { fastText = text; fastSemantic = row.semantic; }
    checks += 1;
  }

  const august = await visit(cdp, base, DAY,
    '#date=2026-08-02&missal=roman-1962&bible=douay-rheims&orations=la&mode=read&ordinary=0');
  assert.equal(august.outcome, 'ready', JSON.stringify(august.error));
  assert.ok(august.loads['structure/propers/mass/roman-1962/pentecost-10.json']);
  assert.equal(august.loads['structure/propers/roman-1962.json'], undefined);
  checks += 1;

  fault = 'catalog-generation';
  let fallback = await visit(cdp, base, DAY, readState);
  assert.equal(fallback.outcome, 'ready', JSON.stringify(fallback.error));
  assert.ok(fallback.loads['structure/propers/roman-1962.json']);
  assert.deepEqual(fallback.semantic, fastSemantic);
  assert.deepEqual(await evaluate(cdp, `Array.from(document.querySelectorAll('#reader-document [data-semantic-event-id]'))
    .map((node) => [node.dataset.semanticLocation, node.textContent.trim()])`), fastText);
  checks += 1;

  fault = 'mass-descriptor';
  fallback = await visit(cdp, base, DAY, readState);
  assert.equal(fallback.outcome, 'ready', JSON.stringify(fallback.error));
  assert.ok(fallback.loads['structure/propers/roman-1962.json']);
  assert.deepEqual(fallback.semantic, fastSemantic);
  checks += 1;
  fault = null;

  const why = await visit(cdp, base, DAY, readState + '&why=1');
  assert.equal(why.outcome, 'ready', JSON.stringify(why.error));
  assert.ok(why.loads['structure/propers/roman-1962.json']);
  assert.equal(why.loads['structure/propers/catalog/roman-1962.json'], undefined);
  checks += 1;

  const explicit = await visit(cdp, base, DAY,
    readState + '&mass=last-sunday-after-pentecost');
  assert.equal(explicit.outcome, 'ready', JSON.stringify(explicit.error));
  assert.ok(explicit.loads['structure/propers/roman-1962.json']);
  assert.equal(explicit.loads['structure/propers/catalog/roman-1962.json'], undefined);
  checks += 1;

  const missal = await visit(cdp, base, DAY,
    baseState + '&mode=missal&ordinary=1&ordinary-lang=en');
  assert.equal(missal.outcome, 'ready', JSON.stringify(missal.error));
  assert.equal(missal.mode, 'missal');
  assert.equal(missal.state.options.ordinary, true);
  assert.equal(missal.loads['structure/propers/catalog/roman-1962.json'], 1);
  assert.equal(missal.loads['structure/propers/mass/roman-1962/last-sunday-after-pentecost.json'], 1);
  assert.equal(missal.loads['structure/propers/roman-1962.json'], undefined);
  assert.equal(missal.loads['structure/ordinary/roman-1962.json'], 1);
  assert.ok(await evaluate(cdp, `document.querySelectorAll('#reader-document .ordinary-element').length > 0`));

  // The Visitation has commemorated Propers and keeps the full source structure.
  const complex = await visit(cdp, base, DAY,
    '#date=2026-07-02&missal=roman-1962&bible=douay-rheims&orations=la&mode=missal&ordinary=1&ordinary-lang=en');
  assert.equal(complex.outcome, 'ready', JSON.stringify(complex.error));
  assert.equal(complex.mode, 'missal');
  assert.equal(complex.loads['structure/propers/roman-1962.json'], 1);
  assert.equal(complex.loads['structure/propers/catalog/roman-1962.json'], undefined);
  checks += 1;

  const visual = await visit(cdp, base, PROTOTYPE,
    '#date=2026-08-02&missal=roman-1962&bible=douay-rheims&orations=la');
  assert.equal(visual.outcome, 'ready', JSON.stringify(visual.error));
  assert.equal(visual.mode, 'read');
  checks += 1;

  assert.deepEqual({ consoleProblems, failedRequests, httpProblems },
    { consoleProblems: [], failedRequests: [], httpProblems: [] });
  process.stdout.write(JSON.stringify({ status: 'pass', checks,
    consoleProblems, failedRequests, httpProblems }) + '\n');
} finally {
  if (cdp) cdp.close();
  chrome.kill('SIGTERM');
  await new Promise((done) => chrome.once('exit', done));
  await new Promise((done) => instance.close(done));
  await rm(profile, { recursive: true, force: true, maxRetries: 5, retryDelay: 100 });
}
