#!/usr/bin/env node

/* Source-served, real-browser checks for the shared reader preference boundary. */

import assert from 'node:assert/strict';
import { spawn } from 'node:child_process';
import { createServer } from 'node:http';
import { mkdir, mkdtemp, readFile, rm } from 'node:fs/promises';
import { extname, resolve, sep } from 'node:path';
import process from 'node:process';

const ROOT = resolve(import.meta.dirname, '../..');
const DATA = '/src/web/data';
const DAY = '/src/web/browser/liturgy/day.html';
const PROPERS = '/src/web/browser/liturgy/index.html';
const PREFERENCES_KEY = 'triptych:liturgy:preferences:v1';
const LEGACY_KEY = 'triptych:liturgy:propers';
const CHROME = process.env.TRIPTYCH_CHROME || '/usr/bin/chromium';
const SCRATCH = resolve(process.env.TRIPTYCH_BROWSER_SCRATCH ||
  resolve(ROOT, '.scratch/reader-preferences-browser'));

function mime(file) {
  return ({
    '.css': 'text/css; charset=utf-8', '.html': 'text/html; charset=utf-8',
    '.js': 'text/javascript; charset=utf-8', '.json': 'application/json'
  })[extname(file)] || 'application/octet-stream';
}

function server() {
  return createServer(async (request, response) => {
    try {
      let relative = decodeURIComponent(new URL(request.url, 'http://localhost').pathname)
        .replace(/^\/+/, '');
      if (relative === 'favicon.ico') {
        response.writeHead(204); response.end(); return;
      }
      if (/^src\/web\/data\/[^/]+\/chapters\//.test(relative)) {
        relative = relative.replace(/^src\/web\/data\//, 'src/sources/bibles/');
      }
      const file = resolve(ROOT, relative || 'README.md');
      if (!file.startsWith(ROOT + sep)) throw new Error('outside root');
      const body = await readFile(file);
      response.writeHead(200, { 'content-type': mime(file), 'cache-control': 'no-store' });
      response.end(body);
    } catch (_error) {
      response.writeHead(404); response.end('not found');
    }
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
  for (let index = 0; index < 120; index += 1) {
    try {
      const reply = await fetch(url);
      if (reply.ok) return await reply.json();
    } catch (_error) { /* Chromium is starting. */ }
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
  on(name, handler) {
    this.events.set(name, [...(this.events.get(name) || []), handler]);
  }
  async ready() {
    await new Promise((done, reject) => {
      this.socket.addEventListener('open', done, { once: true });
      this.socket.addEventListener('error', reject, { once: true });
    });
    this.socket.addEventListener('message', (event) => {
      const message = JSON.parse(event.data);
      if (!message.id) {
        for (const handler of this.events.get(message.method) || []) handler(message.params);
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
        this.pending.delete(id);
        reject(new Error('CDP timeout: ' + method));
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
  if (reply.exceptionDetails) {
    throw new Error(reply.exceptionDetails.exception?.description || reply.exceptionDetails.text);
  }
  return reply.result.value;
}

async function waitFor(cdp, expression, label) {
  for (let index = 0; index < 240; index += 1) {
    if (await evaluate(cdp, `Boolean(${expression})`)) return;
    await new Promise((done) => setTimeout(done, 50));
  }
  throw new Error('Timed out waiting for ' + label);
}

let sequence = 0;
async function visit(cdp, base, path, hash = '') {
  const url = `${base}${path}?data=${DATA}&pref-test=${++sequence}${hash}`;
  await cdp.send('Page.navigate', { url });
  const ready = path === DAY ? 'window.dayReaderReady === true' :
    'window.propersReaderReady === true';
  await waitFor(cdp, `performance.getEntriesByType('navigation')[0]?.name === ${JSON.stringify(url)} && ${ready}`,
    path + ' readiness');
  return evaluate(cdp, path === DAY ? 'dayReaderDebug' : 'propersReaderDebug');
}

async function state(cdp, name) {
  return evaluate(cdp, `${name}ReaderDebug.state`);
}

function hash(values) { return '#' + new URLSearchParams(values).toString(); }

const explicitDay = hash({
  date: '2026-08-08', missal: 'roman-1962', bible: 'douay-rheims', orations: 'la'
});
const explicitPropers = hash({
  missal: 'roman-1962', type: 'seasonal', mass: 'advent-1',
  bible: 'douay-rheims', orations: 'la'
});

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
let checks = 0;
const consoleProblems = [];
const failedRequests = [];
const httpProblems = [];
try {
  const pages = await waitJson(`http://127.0.0.1:${debugPort}/json`);
  cdp = new CDP(pages.find((row) => row.type === 'page').webSocketDebuggerUrl);
  await cdp.ready();
  cdp.on('Runtime.exceptionThrown', ({ exceptionDetails }) => {
    consoleProblems.push(exceptionDetails?.exception?.description ||
      exceptionDetails?.text || 'uncaught JavaScript exception');
  });
  cdp.on('Runtime.consoleAPICalled', ({ type, args }) => {
    if (type === 'error') consoleProblems.push(args.map((arg) => arg.value ||
      arg.description || '').join(' '));
  });
  cdp.on('Network.loadingFailed', ({ canceled, errorText }) => {
    if (!canceled) failedRequests.push(errorText || 'network request failed');
  });
  cdp.on('Network.responseReceived', ({ response }) => {
    if (response?.status >= 400) httpProblems.push(response.status + ' ' + response.url);
  });
  await Promise.all([
    cdp.send('Page.enable'), cdp.send('Runtime.enable'), cdp.send('Network.enable')
  ]);
  const clock = await cdp.send('Page.addScriptToEvaluateOnNewDocument', { source: `
    (() => {
      const OriginalDate = Date;
      const fixed = new OriginalDate(2026, 7, 8, 12).getTime();
      class FixedDate extends OriginalDate {
        constructor(...args) { super(...(args.length ? args : [fixed])); }
        static now() { return fixed; }
      }
      Object.setPrototypeOf(FixedDate, OriginalDate);
      globalThis.Date = FixedDate;
    })();
  ` });
  const base = `http://127.0.0.1:${port}`;

  await visit(cdp, base, DAY, explicitDay);
  await evaluate(cdp, 'localStorage.clear()');
  let row = await visit(cdp, base, DAY);
  assert.equal(row.outcome, 'ready');
  assert.equal(row.state.civilDate, '2026-08-08');
  assert.deepEqual([row.state.edition.id, row.state.bible.id, row.state.languages.orations,
    row.state.requestedMode], ['roman-1962', 'douay-rheims', 'la', 'read']);
  assert.equal(await evaluate(cdp, 'Object.keys(dayReaderDebug.loads).some(k => k.startsWith("structure/ordinary/") && !k.endsWith("/index.json"))'), false);
  checks += 1;

  await evaluate(cdp, `localStorage.setItem(${JSON.stringify(PREFERENCES_KEY)}, JSON.stringify({
    missal:'postconciliar', bible:'clementine-vulgate', orations:'en',
    date:'2026-11-29', locality:'invented', form:'day', mode:'missal'
  }))`);
  row = await visit(cdp, base, DAY);
  assert.equal(row.outcome, 'ready');
  assert.deepEqual([row.state.civilDate, row.state.edition.id, row.state.bible.id,
    row.state.languages.orations, row.state.requestedMode],
  ['2026-08-08', 'postconciliar', 'clementine-vulgate', 'en', 'read']);
  assert.equal(row.state.calendar.id, 'postconciliar');
  assert.equal(await evaluate(cdp, 'Object.keys(dayReaderDebug.loads).some(k => k.startsWith("structure/ordinary/") && !k.endsWith("/index.json"))'), false);
  checks += 1;

  row = await visit(cdp, base, PROPERS);
  assert.equal(row.outcome, 'browse');
  assert.deepEqual([row.state.edition.id, row.state.bible.id, row.state.languages.orations],
    ['postconciliar', 'clementine-vulgate', 'en']);
  checks += 1;

  row = await visit(cdp, base, DAY, explicitDay);
  assert.deepEqual([row.state.edition.id, row.state.bible.id, row.state.languages.orations],
    ['roman-1962', 'douay-rheims', 'la']);
  row = await visit(cdp, base, PROPERS, explicitPropers);
  assert.deepEqual([row.state.edition.id, row.state.bible.id, row.state.languages.orations],
    ['roman-1962', 'douay-rheims', 'la']);
  assert.equal(JSON.parse(await evaluate(cdp,
    `localStorage.getItem(${JSON.stringify(PREFERENCES_KEY)})`)).missal, 'postconciliar');
  checks += 1;

  row = await visit(cdp, base, DAY, '#date=2026-08-08&missal=not-held');
  assert.equal(row.outcome, 'invalid');
  row = await visit(cdp, base, PROPERS, '#missal=not-held&type=seasonal&mass=advent-1');
  assert.equal(row.outcome, 'invalid');
  checks += 1;

  await evaluate(cdp, `localStorage.setItem(${JSON.stringify(PREFERENCES_KEY)}, JSON.stringify({
    missal:'not-held', bible:'not-held', orations:'fr'
  }))`);
  row = await visit(cdp, base, DAY);
  assert.deepEqual([row.state.edition.id, row.state.bible.id, row.state.languages.orations],
    ['roman-1962', 'douay-rheims', 'la']);
  row = await visit(cdp, base, PROPERS);
  assert.deepEqual([row.state.edition.id, row.state.bible.id, row.state.languages.orations],
    ['roman-1962', 'douay-rheims', 'la']);
  checks += 1;

  await evaluate(cdp, `localStorage.removeItem(${JSON.stringify(PREFERENCES_KEY)});
    localStorage.setItem(${JSON.stringify(LEGACY_KEY)}, JSON.stringify({
      missal:'postconciliar', bible:'clementine-vulgate', orations:'en'
    }))`);
  row = await visit(cdp, base, DAY);
  assert.deepEqual([row.state.edition.id, row.state.bible.id, row.state.languages.orations],
    ['postconciliar', 'clementine-vulgate', 'en']);
  row = await visit(cdp, base, PROPERS);
  assert.deepEqual([row.state.edition.id, row.state.bible.id, row.state.languages.orations],
    ['postconciliar', 'clementine-vulgate', 'en']);
  checks += 1;

  await visit(cdp, base, DAY, explicitDay);
  await evaluate(cdp, `(() => {
    document.querySelector('#reader-date').value = '2026-11-29';
    document.querySelector('#reader-missal').value = 'postconciliar';
    document.querySelector('#reader-bible').value = 'clementine-vulgate';
    document.querySelector('#reader-orations').value = 'en';
    document.querySelector('#date-form').requestSubmit();
  })()`);
  await waitFor(cdp, `dayReaderDebug.ready && dayReaderDebug.state?.edition.id === 'postconciliar' &&
    dayReaderDebug.state?.civilDate === '2026-11-29'`, 'Day Apply');
  assert.equal(await evaluate(cdp, `localStorage.getItem(${JSON.stringify(PREFERENCES_KEY)})`),
    JSON.stringify({ missal:'postconciliar', bible:'clementine-vulgate', orations:'en' }));
  row = await visit(cdp, base, PROPERS);
  assert.deepEqual([row.state.edition.id, row.state.bible.id, row.state.languages.orations],
    ['postconciliar', 'clementine-vulgate', 'en']);
  checks += 1;

  await evaluate(cdp, `(() => {
    document.querySelector('#reader-formulary').value = 'advent-1';
    document.querySelector('#reader-bible').value = 'douay-rheims';
    document.querySelector('#reader-orations').value = 'la';
    document.querySelector('#browse-form').requestSubmit();
  })()`);
  await waitFor(cdp, `propersReaderDebug.ready && propersReaderDebug.outcome === 'ready' &&
    propersReaderDebug.state?.formulary?.id === 'advent-1'`, 'Propers Apply');
  assert.equal(await evaluate(cdp, `localStorage.getItem(${JSON.stringify(PREFERENCES_KEY)})`),
    JSON.stringify({ missal:'postconciliar', bible:'douay-rheims', orations:'la' }));
  row = await visit(cdp, base, DAY);
  assert.deepEqual([row.state.civilDate, row.state.edition.id, row.state.bible.id,
    row.state.languages.orations], ['2026-08-08', 'postconciliar', 'douay-rheims', 'la']);
  checks += 1;

  await evaluate(cdp, `localStorage.setItem(${JSON.stringify(PREFERENCES_KEY)}, '{')`);
  row = await visit(cdp, base, DAY);
  assert.deepEqual([row.state.edition.id, row.state.bible.id, row.state.languages.orations],
    ['roman-1962', 'douay-rheims', 'la']);
  checks += 1;

  const denied = await cdp.send('Page.addScriptToEvaluateOnNewDocument', { source: `
    Storage.prototype.getItem = () => { throw new Error('blocked'); };
    Storage.prototype.setItem = () => { throw new Error('blocked'); };
  ` });
  row = await visit(cdp, base, DAY);
  assert.deepEqual([row.state.edition.id, row.state.bible.id, row.state.languages.orations],
    ['roman-1962', 'douay-rheims', 'la']);
  row = await visit(cdp, base, PROPERS, explicitPropers);
  assert.equal(row.outcome, 'ready');
  row = await visit(cdp, base, DAY, explicitDay);
  const generation = await evaluate(cdp, 'dayReaderDebug.renders');
  await evaluate(cdp, `document.querySelector('#date-form').requestSubmit()`);
  await waitFor(cdp, `dayReaderDebug.ready && dayReaderDebug.renders > ${generation} &&
    dayReaderDebug.state?.edition.id === 'roman-1962'`,
    'Day Apply with blocked storage');
  await cdp.send('Page.removeScriptToEvaluateOnNewDocument', { identifier: denied.identifier });
  await cdp.send('Page.removeScriptToEvaluateOnNewDocument', { identifier: clock.identifier });
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
  await rm(profile, { recursive: true, force: true });
}
