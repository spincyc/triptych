#!/usr/bin/env node

/* Source-served Chromium checks for the Day Compare vertical slice. */

import assert from 'node:assert/strict';
import { spawn } from 'node:child_process';
import { createServer } from 'node:http';
import { mkdtemp, mkdir, readFile, rm } from 'node:fs/promises';
import { extname, resolve, sep } from 'node:path';

const ROOT = resolve(import.meta.dirname, '../..');
const CHROME = process.env.TRIPTYCH_CHROME || '/usr/bin/chromium';
const SCRATCH = resolve(process.env.TRIPTYCH_BROWSER_SCRATCH ||
  resolve(ROOT, '.scratch/day-compare-browser'));
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
  const url = `${base}${path}?data=/src/web/data&compare-test=${++sequence}${hash}`;
  await cdp.send('Page.navigate', { url });
  await waitFor(cdp, `performance.getEntriesByType('navigation')[0]?.name === ${JSON.stringify(url)} &&
    window.dayReaderReady === true`, path + ' ready');
  return evaluate(cdp, 'dayReaderDebug');
}

const baseState = '#date=2026-11-22&missal=roman-1962&bible=douay-rheims&orations=la';
const compareState = baseState + '&mode=compare&compare=recension&peer-missal=postconciliar&territory=universal&ordinary=0';
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

  for (const path of [DAY, CANDIDATE]) {
    const row = await visit(cdp, base, path, compareState);
    assert.equal(row.outcome, 'ready', JSON.stringify(row.error));
    assert.equal(row.mode, 'compare');
    assert.equal(row.semantic.units.length, 12);
    assert.deepEqual(row.semantic.calendarResults.map((one) => one.resolved.formulary),
      ['last-sunday-after-pentecost', 'christ-the-king']);
    const order = await evaluate(cdp, `Array.from(document.querySelector('#reader-document').children)
      .map((node) => node.className)`);
    assert.equal(order[1], 'compare-calendar-results');
    assert.equal(order[2], 'compare-unit');
    checks += 1;
  }

  const statuses = await evaluate(cdp, `({
    gradual: document.querySelector('[data-semantic-location="compare/proper/gradual"] [data-compare-side="postconciliar"]')?.dataset.compareStatus,
    psalm: document.querySelector('[data-semantic-location="compare/proper/responsorial-psalm"] [data-compare-side="roman-1962"]')?.dataset.compareStatus,
    collect: document.querySelector('[data-semantic-location="compare/proper/collect"] [data-compare-side="postconciliar"]')?.dataset.compareStatus,
    text: document.querySelector('[data-semantic-location="compare/proper/collect"] [data-compare-side="postconciliar"]')?.textContent
  })`);
  assert.deepEqual([statuses.gradual, statuses.psalm, statuses.collect],
    ['no-event-in-selected-formulary', 'no-event-in-selected-formulary', 'text-unavailable']);
  assert.match(statuses.text, /text is unavailable/i);
  checks += 1;

  const source = await evaluate(cdp, `({
    hash: location.hash, loads: dayReaderDebug.loads,
    comparison: dayReaderDebug.state.comparison,
    ordinary: Object.keys(dayReaderDebug.loads).filter((key) => key.startsWith('structure/ordinary/') && !key.endsWith('/index.json'))
  })`);
  assert.match(source.hash, /compare=recension&peer-missal=postconciliar&territory=universal/);
  assert.equal(source.comparison.anchor.territorialContext, 'universal');
  assert.ok(source.loads['structure/calendar/roman-1962/2026.json']);
  assert.ok(source.loads['structure/calendar/postconciliar/2026.json']);
  assert.deepEqual(source.ordinary, []);
  checks += 1;

  await evaluate(cdp, `(() => {
    document.querySelector('[data-reader-action="contents"]').click();
    document.querySelector('[data-reader-location="compare/proper/collect"]').click();
  })()`);
  assert.match(await evaluate(cdp, 'location.hash'), /location=compare%2Fproper%2Fcollect/);
  assert.equal(await evaluate(cdp, 'document.activeElement.dataset.semanticLocation'),
    'compare/proper/collect');
  const located = await visit(cdp, base, DAY, compareState + '&location=compare%2Fproper%2Fcollect');
  assert.equal(located.outcome, 'ready');
  assert.equal(located.state.semanticLocation.eventId, 'compare/proper/collect');
  checks += 1;

  await evaluate(cdp, `(() => {
    document.querySelector('[data-reader-action="mode"]').click();
    document.querySelector('[data-mode="read"]').click();
  })()`);
  await waitFor(cdp, `dayReaderDebug.ready && dayReaderDebug.mode === 'read'`, 'Read switch');
  assert.doesNotMatch(await evaluate(cdp, 'location.hash'), /compare=|peer-missal=|territory=/);
  assert.equal(await evaluate(cdp, 'document.activeElement.dataset.readerAction'), 'mode');
  checks += 1;

  await visit(cdp, base, DAY, baseState);
  await evaluate(cdp, `(() => {
    document.querySelector('[data-reader-action="mode"]').click();
    document.querySelector('[data-mode="compare"]').click();
  })()`);
  let setup = await evaluate(cdp, `({ hidden: document.querySelector('#compare-setup').hidden,
    peer: document.querySelector('#reader-compare-peer').value,
    territory: document.querySelector('#reader-compare-territory').value })`);
  assert.deepEqual(setup, { hidden: false, peer: '', territory: '' });
  await evaluate(cdp, `(() => {
    const peer = document.querySelector('#reader-compare-peer');
    peer.value = 'postconciliar'; peer.dispatchEvent(new Event('change', { bubbles:true }));
  })()`);
  await waitFor(cdp, `!document.querySelector('#reader-compare-territory').disabled`,
    'territory choices');
  setup = await evaluate(cdp, `({ peer: document.querySelector('#reader-compare-peer').value,
    territory: document.querySelector('#reader-compare-territory').value })`);
  assert.deepEqual(setup, { peer: 'postconciliar', territory: '' });
  await evaluate(cdp, `(() => {
    document.querySelector('#reader-compare-territory').value = 'universal';
    document.querySelector('#compare-setup').requestSubmit();
  })()`);
  await waitFor(cdp, `dayReaderDebug.ready && dayReaderDebug.mode === 'compare'`,
    'explicit Compare setup');
  assert.match(await evaluate(cdp, 'location.hash'), /peer-missal=postconciliar&territory=universal/);
  checks += 1;

  for (const hash of [
    baseState + '&mode=compare&compare=recension&territory=universal',
    baseState + '&mode=compare&compare=recension&peer-missal=postconciliar',
    baseState + '&mode=compare&compare=recension&peer-missal=postconciliar&territory=invented'
  ]) {
    const row = await visit(cdp, base, DAY, hash);
    assert.notEqual(row.outcome, 'ready', hash);
    assert.equal(await evaluate(cdp, `document.querySelectorAll('.compare-unit').length`), 0);
  }
  checks += 1;

  await visit(cdp, base, DAY, compareState);
  await cdp.send('Emulation.setDeviceMetricsOverride', {
    width: 320, height: 720, deviceScaleFactor: 1, mobile: true
  });
  const mobile = await evaluate(cdp, `({ overflow: document.documentElement.scrollWidth - innerWidth,
    columns: getComputedStyle(document.querySelector('.compare-pair')).gridTemplateColumns })`);
  assert.ok(mobile.overflow <= 1, JSON.stringify(mobile));
  assert.equal(mobile.columns.split(' ').length, 1);
  await cdp.send('Emulation.setEmulatedMedia', { media: 'print' });
  const printed = await evaluate(cdp, `({
    title: document.querySelector('#celebration-title').textContent,
    calendar: getComputedStyle(document.querySelector('.compare-calendar-results')).display,
    units: document.querySelectorAll('.compare-unit').length,
    actions: getComputedStyle(document.querySelector('.reader-actions')).display
  })`);
  assert.equal(printed.units, 12);
  assert.notEqual(printed.calendar, 'none');
  assert.equal(printed.actions, 'none');
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
  await rm(profile, { recursive: true, force: true });
}
