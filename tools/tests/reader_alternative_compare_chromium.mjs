#!/usr/bin/env node

/* Exact source reading alternatives through the production Propers adapter and renderer. */

import assert from 'node:assert/strict';
import { spawn, execFileSync } from 'node:child_process';
import { createServer } from 'node:http';
import { mkdir, mkdtemp, readFile, rm, writeFile } from 'node:fs/promises';
import { extname, resolve, sep } from 'node:path';

const ROOT = resolve(process.env.TRIPTYCH_REVIEW_ROOT || resolve(import.meta.dirname, '../..'));
const OVERLAY = process.env.TRIPTYCH_ALTERNATIVE_MODULE_ROOT;
const CHROME = process.env.TRIPTYCH_CHROME || '/usr/bin/chromium';
const SCRATCH = resolve(process.env.TRIPTYCH_BROWSER_SCRATCH ||
  resolve(ROOT, '.scratch/reader-alternative-compare/browser'));
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
  const identity = '#missal=postconciliar&type=christological&mass=presentation-lord&bible=douay-rheims&orations=la';
  const group = 'proper-choice/postconciliar/presentation-lord/main/gospel';
  const longer = group + '/longer', shorter = group + '/shorter';
  const comparison = '&mode=compare&compare=reading-alternative&alternative=' + encodeURIComponent(longer) + '&peer-alternative=' + encodeURIComponent(shorter);
  const ready = async () => waitFor(cdp, `window.propersReaderDebug?.ready && document.getElementById('reader-document').getAttribute('aria-busy') === 'false'`, 'settled Propers');
  const click = async (selector) => evaluate(cdp, `document.querySelector(${JSON.stringify(selector)}).click()`);
  const choose = async (selector, value) => evaluate(cdp, `(() => { const node = document.querySelector(${JSON.stringify(selector)}); node.value = ${JSON.stringify(value)}; node.dispatchEvent(new Event('change', { bubbles: true })); })()`);
  async function visit(suffix, path = PROPERS) { await cdp.send('Page.navigate', { url: base + path + '?data=/src/web/data' + identity + suffix }); await ready(); }
  const projections = [];
  for (const path of [PROPERS, '/src/web/browser/liturgy/propers-reader.html']) {
    await visit(comparison + '&location=compare%2Fproper%2Fgospel', path);
    const value = await evaluate(cdp, `({ outcome: propersReaderDebug.outcome, state: propersReaderDebug.state, semantic: propersReaderDebug.semantic,
      cells: [...document.querySelectorAll('[data-semantic-event-id="compare/proper/gospel"] .compare-side')].map(node => node.textContent),
      contents: [...document.querySelectorAll('[data-reader-location]')].map(node => node.dataset.readerLocation) })`);
    assert.equal(value.outcome, 'ready'); assert.equal(value.state.civilDate, null);
    assert.deepEqual(value.semantic.sides.map(side => side.id), ['longer', 'shorter']);
    assert.equal(value.semantic.units.length, 5); assert.equal(value.semantic.calendarResults, null);
    assert.match(value.cells[0], /Luke 2:22-40/); assert.match(value.cells[1], /Luke 2:22-32/);
    assert.ok(value.cells.every(text => /Bible reconstruction/.test(text)));
    assert.deepEqual(value.contents, value.semantic.units.map(unit => 'compare/proper/' + unit.semanticSlot));
    projections.push(value.semantic);
  }
  assert.deepEqual(projections[0], projections[1]); assertions.push('canonical and retained routes pair the exact longer and shorter source Gospel ordinals');

  await visit('&mode=read&location=' + encodeURIComponent(group));
  await waitFor(cdp, `document.querySelector('[data-semantic-event-id="${group}"]')?.getBoundingClientRect().top <= 280`, 'source choice location');
  await evaluate(cdp, `(async () => { for (let n = 0; n < 12; n += 1) await new Promise(requestAnimationFrame); })()`);
  await click('[data-reader-action="mode"]'); await click('[data-mode="compare"]'); await choose('#reader-compare-dimension', 'reading-alternative');
  assert.deepEqual(await evaluate(cdp, `[document.getElementById('reader-compare-alternative').value, document.getElementById('reader-compare-peer-alternative').value]`), ['', '']);
  await choose('#reader-compare-alternative', shorter); await choose('#reader-compare-peer-alternative', shorter); await click('#compare-setup .surface-apply');
  assert.equal(await evaluate(cdp, 'propersReaderDebug.state.requestedMode'), 'read');
  assert.match(await evaluate(cdp, 'document.getElementById("compare-setup-note").textContent'), /different source reading alternatives/);
  await choose('#reader-compare-peer-alternative', longer); await click('#compare-setup .surface-apply'); await ready();
  assert.equal(await evaluate(cdp, 'propersReaderDebug.state.comparison.dimension'), 'reading-alternative');
  assert.equal(await evaluate(cdp, 'propersReaderDebug.state.semanticLocation.eventId'), 'compare/proper/gospel');
  assert.equal(await evaluate(cdp, 'document.activeElement.dataset.readerAction'), 'mode');
  assertions.push('coequal controls require distinct explicit options and retain semantic Gospel place and Mode focus');

  await cdp.send('Emulation.setDeviceMetricsOverride', { width: 320, height: 852, deviceScaleFactor: 1, mobile: false });
  assert.equal(await evaluate(cdp, 'document.documentElement.scrollWidth > document.documentElement.clientWidth + 1'), false);
  assert.equal(await evaluate(cdp, `(() => { const sides = [...document.querySelectorAll('.compare-unit:last-child .compare-side')]; return sides[1].getBoundingClientRect().top >= sides[0].getBoundingClientRect().bottom; })()`), true);
  assertions.push('320-pixel alternative comparison stacks each corresponding pair without page overflow');

  await cdp.send('Emulation.setEmulatedMedia', { media: 'print' });
  const pdf = await cdp.send('Page.printToPDF', { printBackground: true, preferCSSPageSize: true });
  const pdfPath = resolve(SCRATCH, 'presentation-alternatives.pdf'); await writeFile(pdfPath, Buffer.from(pdf.data, 'base64'));
  const text = execFileSync('/usr/bin/pdftotext', [pdfPath, '-'], { encoding: 'utf8' });
  assert.match(text, /The Presentation of the Lord/); assert.match(text, /postconciliar/);
  assert.match(text, /Longer reading/); assert.match(text, /Shorter reading/);
  assert.match(text, /Luke 2:22-40/); assert.match(text, /Luke 2:22-32/); assert.match(text, /Bible reconstruction/);
  assert.match(text, /proper-choice-option|presentation-lord/);
  assert.doesNotMatch(text, /Share link|Compare this formulary|Primary reading alternative/);
  await cdp.send('Emulation.setEmulatedMedia', { media: 'screen' });
  assertions.push('print preserves independent source identities and Bible-reconstruction qualifications without interactive controls');

  await visit('&mode=compare&compare=reading-alternative&alternative=' + encodeURIComponent(shorter) + '&peer-alternative=' + encodeURIComponent(longer) + '&location=compare%2Fproper%2Fgospel');
  await waitFor(cdp, `document.querySelector('[data-semantic-event-id="compare/proper/gospel"]')?.getBoundingClientRect().top <= 280`, 'restored comparison Gospel');
  await evaluate(cdp, `(async () => { for (let n = 0; n < 12; n += 1) await new Promise(requestAnimationFrame); })()`);
  await click('[data-reader-action="mode"]'); await click('[data-mode="read"]'); await ready();
  const read = await evaluate(cdp, `({ outcome: propersReaderDebug.outcome, state: propersReaderDebug.state, hash: location.hash,
    first: document.querySelector('[data-proper-choice-option]')?.dataset.properChoiceOption,
    selection: document.querySelector('[data-proper-choice]')?.dataset.choiceSelection,
    unselected: document.querySelector('[data-choice-status="not-selected"]')?.tagName })`);
  assert.equal(read.outcome, 'ready'); assert.equal(read.state.alternative.id, shorter);
  assert.equal(read.state.semanticLocation.eventId, group); assert.equal(read.selection, 'shorter');
  assert.equal(read.first, 'shorter'); assert.equal(read.unselected, 'DETAILS');
  assert.doesNotMatch(read.hash, /(?:compare|peer-alternative)=/);
  assertions.push('return to Read retains the primary shorter option and its source choice location with other options collapsed');

  for (const invalid of [comparison.replace(encodeURIComponent(shorter), encodeURIComponent(group + '/unknown')),
    comparison.replace(encodeURIComponent(shorter), encodeURIComponent(longer)),
    comparison.replace('&peer-alternative=' + encodeURIComponent(shorter), ''),
    comparison + '&peer-cycle=A', comparison + '&peer-orations=en']) {
    await visit(invalid); assert.equal(await evaluate(cdp, 'propersReaderDebug.outcome'), 'invalid');
    assert.equal(await evaluate(cdp, 'document.querySelectorAll(".compare-unit").length'), 0);
  }
  assertions.push('unknown equal missing and wrong-dimension peers fail closed without fallback text');
  assert.deepEqual(consoleProblems, []); assert.deepEqual(failedRequests, []); assert.deepEqual(httpProblems, []);
  process.stdout.write(JSON.stringify({ status: 'pass', checks: assertions.length, assertions, consoleProblems, failedRequests, httpProblems }) + '\n');
} catch (error) {
  const state = cdp ? await evaluate(cdp, `({ hash: location.hash, debug: window.propersReaderDebug })`).catch(() => null) : null;
  process.stderr.write(JSON.stringify({ status: 'fail', error: error.stack, state, assertions, consoleProblems, failedRequests, httpProblems }) + '\n'); process.exitCode = 1;
} finally {
  if (cdp) cdp.close(); const stopped = new Promise((done) => chrome.once('exit', done)); chrome.kill('SIGTERM'); await stopped;
  await new Promise((done) => instance.close(done)); await rm(profile, { recursive: true, force: true, maxRetries: 4, retryDelay: 100 });
}
