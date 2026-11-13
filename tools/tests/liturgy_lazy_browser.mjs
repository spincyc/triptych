#!/usr/bin/env node

/* Actual generated Pages payloads preserve native Day/Propers across modes.
 * TRIPTYCH_TEST_BROWSER_DATA_ROOT supplies complete browser products. Optional
 * TRIPTYCH_TEST_PROPER_DATA_ROOT overlays a freshly generated mass-propers family.
 * The indexed branch serves those generated files without transformations. */

import assert from 'node:assert/strict';
import { spawn } from 'node:child_process';
import { createServer } from 'node:http';
import { mkdtemp, mkdir, readFile, rm } from 'node:fs/promises';
import { extname, resolve, sep } from 'node:path';

const ROOT = resolve(import.meta.dirname, '../..');
const DATA = resolve(process.env.TRIPTYCH_TEST_BROWSER_DATA_ROOT);
const PROPERS = resolve(process.env.TRIPTYCH_TEST_PROPER_DATA_ROOT || DATA);
let indexedMode = false;
async function served(where, file) {
  if (!where.startsWith('src/web/data/')) return readFile(file);
  const relative = where.slice('src/web/data/'.length);
  const body = await readFile(resolve(relative.startsWith('structure/propers/') ? PROPERS : DATA, relative));
  if (!indexedMode && relative === 'structure/propers/index.json') {
    // The independent oracle keeps every complete source owner. The deployed
    // branch receives the producer's manifest and every payload byte unchanged.
    const index = JSON.parse(body);
    index.missals.forEach(row => {
      delete row.reader_index; delete row.reader_file; delete row.read_payload;
    });
    return JSON.stringify(index);
  }
  return body;
}
const CHROME = process.env.TRIPTYCH_CHROME || '/usr/bin/chromium';
const SCRATCH = resolve(process.env.TRIPTYCH_BROWSER_SCRATCH ||
  resolve(ROOT, '.scratch/liturgy-lazy/browser'));

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
      const body = await served(path, file);
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
    (window.dayReaderReady === true || window.propersReaderReady === true)`, path + ' ready');
  return evaluate(cdp, 'window.dayReaderDebug || window.propersReaderDebug');
}


const instance = server();
const port = await listen(instance);
const probe = server(); const debugPort = await listen(probe);
await new Promise(done => probe.close(done));
await mkdir(SCRATCH, {recursive:true});
const profile = await mkdtemp(resolve(SCRATCH, 'chromium-'));
const chrome = spawn(CHROME, ['--headless=new','--disable-gpu','--no-sandbox','--disable-dev-shm-usage',
 `--remote-debugging-port=${debugPort}`,`--user-data-dir=${profile}`,'about:blank'], {stdio:'ignore'});
let cdp;
const diagnostics = [];
try {
 const pages = await waitJson(`http://127.0.0.1:${debugPort}/json`);
 cdp = new CDP(pages.find(row => row.type === 'page').webSocketDebuggerUrl); await cdp.ready();
 cdp.on('Runtime.exceptionThrown', row => diagnostics.push(row.exceptionDetails?.text));
 cdp.on('Runtime.consoleAPICalled', row => {
  if (row.type === 'error') diagnostics.push(row.args.map(arg => arg.value || arg.description).join(' '));
 });
 cdp.on('Network.loadingFailed', row => {if (!row.canceled) diagnostics.push(row.errorText)});
 cdp.on('Network.responseReceived', row => {if (row.response.status >= 400) diagnostics.push(row.response.status + ' ' + row.response.url)});
 await Promise.all([cdp.send('Page.enable'),cdp.send('Runtime.enable'),cdp.send('Network.enable')]);
 const base = `http://127.0.0.1:${port}`;
 const cases = [
  ['day.html','#date=2026-01-15&missal=roman-1962&orations=en&mode=read'],
  ['day.html','#date=2026-01-17&missal=roman-1962&orations=en&mode=missal&ordinary-lang=en'],
  ['day.html','#date=2026-05-24&missal=postconciliar&orations=en&mode=read'],
  ['day.html','#date=2026-06-04&missal=postconciliar&orations=la&mode=read'],
  ['day.html','#date=2026-11-22&missal=roman-1962&orations=la&mode=compare&compare=recension&peer-missal=postconciliar&territory=universal'],
  ['index.html','#missal=postconciliar&type=christological&mass=transfiguration-lord&orations=la&mode=compare&compare=lectionary-cycle&cycle=A&peer-cycle=B'],
  ['index.html','#missal=postconciliar&orations=en'],
  ['index.html','#missal=roman-1962&type=seasonal&mass=pentecost&orations=en&mode=missal&ordinary-lang=en'],
  ['index.html','#missal=postconciliar&type=seasonal&mass=advent-1&cycle=A&orations=en&mode=study'],
  ['index.html','#missal=roman-1962&type=sanctoral&mass=commemoratione-omnium-fidelium-defunctorum&form=first&orations=en'],
  ['day.html','#date=2026-08-02&missal=roman-pre-1955&orations=la'],
  ['index.html','#missal=roman-pre-1955&type=seasonal&mass=advent-1&orations=la'],
  ['reader-visual-reset-day.html','#date=2026-08-02&missal=roman-1962&orations=la'],
  ['reader-visual-reset-propers.html','#missal=postconciliar&type=seasonal&mass=advent-1&cycle=A&orations=la'],
 ];
 const resources = () => evaluate(cdp, `performance.getEntriesByType('resource')
   .filter(row => row.name.includes('/structure/propers/'))
   .map(row => ({path: new URL(row.name).pathname.split('/src/web/data/')[1], bytes: row.decodedBodySize}))`);
 const reports = [];
 for (const [page, hash] of cases) {
  indexedMode = false;
  const before = await visit(cdp, base, '/src/web/browser/liturgy/' + page, hash);
  const beforeResources = await resources();
  const text = await evaluate(cdp, "document.querySelector('#reader-document').textContent");
  indexedMode = true;
  const after = await visit(cdp, base, '/src/web/browser/liturgy/' + page, hash);
  const afterResources = await resources();
  const afterText = await evaluate(cdp, "document.querySelector('#reader-document').textContent");
  assert.deepEqual(after.state, before.state, page + hash + ' state');
  assert.equal(after.outcome, before.outcome, JSON.stringify({page, hash, before:before.error, after:after.error}));
  assert.equal(afterText, text, page + hash + ' text');
  assert.deepEqual(after.semantic, before.semantic, page + hash + ' semantic');
  assert.ok(afterResources.every(row => !/propers\/[^/]+\.json$/.test(row.path) || row.path.endsWith('/index.json')),
    'deployed reader never fetches a complete calendar: ' + JSON.stringify(afterResources));
  assert.ok(afterResources.some(row => row.path.includes('/reader/')), 'producer reader_file was requested');
  assert.ok(afterResources.every(row => !row.path.includes('/catalog/')), 'no duplicate catalog');
  const masses = Object.keys(after.loads).filter(p => p.includes('/propers/mass/'));
  assert.ok(masses.length < 15, JSON.stringify(masses));
  reports.push({page, hash, outcome:after.outcome, masses:masses.length,
    fullProperBytes:beforeResources.reduce((total, row) => total + row.bytes, 0),
    indexedProperBytes:afterResources.reduce((total, row) => total + row.bytes, 0)});
 }
 assert.deepEqual(diagnostics, []);
 console.log(JSON.stringify({status:'pass',cases:reports}));
} finally {
 if(cdp) cdp.close(); chrome.kill('SIGTERM'); await new Promise(done=>chrome.once('exit',done));
 await new Promise(done=>instance.close(done));
 await rm(profile,{recursive:true,force:true,maxRetries:5,retryDelay:100});
}
