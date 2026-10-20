#!/usr/bin/env node

/* Source-served Chromium checks for the Day Study vertical slice. */

import assert from 'node:assert/strict';
import { spawn } from 'node:child_process';
import { createServer } from 'node:http';
import { mkdtemp, mkdir, readFile, rm } from 'node:fs/promises';
import { extname, resolve, sep } from 'node:path';

const ROOT = resolve(import.meta.dirname, '../..');
const CHROME = process.env.TRIPTYCH_CHROME || '/usr/bin/chromium';
const SCRATCH = resolve(process.env.TRIPTYCH_BROWSER_SCRATCH ||
  resolve(ROOT, '.scratch/day-study-browser'));
const DAY = '/src/web/browser/liturgy/day.html';
const CANDIDATE = '/src/web/browser/liturgy/day-reader.html';
const PROTOTYPE = '/src/web/browser/liturgy/reader-visual-reset-day.html';

function mime(file) {
  return ({ '.css': 'text/css', '.html': 'text/html', '.js': 'text/javascript',
    '.json': 'application/json' })[extname(file)] || 'application/octet-stream';
}

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
  const url = `${base}${path}?data=/src/web/data&study-test=${++sequence}${hash}`;
  await cdp.send('Page.navigate', { url });
  await waitFor(cdp, `performance.getEntriesByType('navigation')[0]?.name === ${JSON.stringify(url)} &&
    window.dayReaderReady === true`, path + ' ready');
  return evaluate(cdp, 'dayReaderDebug');
}

const baseState = '#date=2026-11-22&missal=roman-1962&bible=douay-rheims&orations=la';
const studyState = baseState + '&mode=study&ordinary=0';
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

  const read = await visit(cdp, base, DAY, baseState + '&mode=read&ordinary=0');
  assert.equal(read.outcome, 'ready', JSON.stringify(read.error));
  const readSource = await evaluate(cdp, `Array.from(document.querySelectorAll('#reader-document [data-semantic-event-id]'))
    .map((node) => [node.dataset.semanticLocation, node.textContent.trim()])`);
  for (const path of [DAY, CANDIDATE]) {
    const row = await visit(cdp, base, path, studyState);
    assert.equal(row.outcome, 'ready', JSON.stringify(row.error));
    assert.equal(row.mode, 'study');
    assert.equal(await evaluate(cdp, `document.querySelector('[data-mode="study"]').getAttribute('aria-checked')`), 'true');
    checks += 1;
  }
  const source = await evaluate(cdp, `Array.from(document.querySelectorAll('#reader-document [data-semantic-event-id]'))
    .map((node) => { const clone = node.cloneNode(true); clone.querySelectorAll('.study-event').forEach((one) => one.remove());
      return [node.dataset.semanticLocation, clone.textContent.trim()]; })`);
  assert.deepEqual(source, readSource);
  checks += 1;
  const apparatus = await evaluate(cdp, `({ calendar: document.querySelector('.study-overview .study-calendar')?.textContent,
    coverage: document.querySelector('.study-overview .study-coverage')?.textContent,
    events: document.querySelectorAll('.study-event').length,
    hosts: document.querySelectorAll('#reader-document [data-semantic-event-id]').length,
    duplicate: document.querySelectorAll('.study-event[data-semantic-event-id]').length,
    first: document.querySelector('.study-event')?.textContent })`);
  assert.match(apparatus.calendar, /2026-11-22/);
  assert.ok(apparatus.events > 0 && apparatus.events <= apparatus.hosts);
  assert.equal(apparatus.duplicate, 0);
  assert.match(apparatus.first, /Event|Witness|Source record/);
  checks += 1;

  const first = source[0][0];
  await evaluate(cdp, `(() => { document.querySelector('[data-reader-action="contents"]').click();
    document.querySelector('[data-reader-location="${first}"]').click(); })()`);
  assert.equal(await evaluate(cdp, 'document.activeElement.dataset.semanticLocation'), first);
  assert.equal(new URLSearchParams((await evaluate(cdp, 'location.hash')).slice(1)).get('location'), first);
  const located = await visit(cdp, base, DAY, studyState + '&location=' + encodeURIComponent(first));
  assert.equal(located.outcome, 'ready');
  assert.equal(located.state.semanticLocation.eventId, first);
  assert.ok(await evaluate(cdp, 'window.scrollY > 0'));
  checks += 1;

  await evaluate(cdp, `(() => { document.querySelector('[data-reader-action="mode"]').click();
    document.querySelector('[data-mode="read"]').click(); })()`);
  await waitFor(cdp, `dayReaderDebug.ready && dayReaderDebug.mode === 'read'`, 'Read switch');
  assert.equal(await evaluate(cdp, 'document.activeElement.dataset.readerAction'), 'mode');
  await evaluate(cdp, `(() => { document.querySelector('[data-reader-action="mode"]').click();
    document.querySelector('[data-mode="study"]').click(); })()`);
  await waitFor(cdp, `dayReaderDebug.ready && dayReaderDebug.mode === 'study'`, 'Study switch');
  assert.equal(await evaluate(cdp, 'document.activeElement.dataset.readerAction'), 'mode');
  checks += 1;

  const invalid = await visit(cdp, base, DAY,
    studyState + '&location=proper%2Froman-1962%2Fmissing');
  assert.equal(invalid.outcome, 'invalid');
  assert.ok(invalid.error.some((one) => one.code === 'invalid-semantic-location'));
  assert.equal(await evaluate(cdp, `document.querySelectorAll('.study-overview').length`), 0);
  checks += 1;

  const ordinary = await visit(cdp, base, DAY,
    baseState + '&mode=study&ordinary=1');
  assert.equal(ordinary.outcome, 'deferred');
  assert.equal(await evaluate(cdp, `document.querySelectorAll('.study-overview, .study-event').length`), 0);
  checks += 1;

  await visit(cdp, base, DAY, studyState);
  await cdp.send('Emulation.setDeviceMetricsOverride', {
    width: 320, height: 720, deviceScaleFactor: 1, mobile: true
  });
  const overflow = await evaluate(cdp, 'document.documentElement.scrollWidth - innerWidth');
  assert.ok(overflow <= 1, String(overflow));
  await cdp.send('Emulation.setEmulatedMedia', { media: 'print' });
  assert.notEqual(await evaluate(cdp, `getComputedStyle(document.querySelector('.study-overview')).display`), 'none');
  assert.equal(await evaluate(cdp, `getComputedStyle(document.querySelector('.reader-actions')).display`), 'none');
  const pdf = await cdp.send('Page.printToPDF', { printBackground: true });
  assert.ok(pdf.data.length > 1000);
  checks += 1;
  await cdp.send('Emulation.setEmulatedMedia', { media: 'screen' });
  await cdp.send('Emulation.clearDeviceMetricsOverride');

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
