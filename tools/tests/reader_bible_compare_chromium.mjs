#!/usr/bin/env node

/* Explicit published Bible renderings over exact source occurrences. */

import assert from 'node:assert/strict';
import { spawn, execFileSync } from 'node:child_process';
import { createServer } from 'node:http';
import { mkdir, mkdtemp, readFile, rm, writeFile } from 'node:fs/promises';
import { extname, resolve, sep } from 'node:path';

const ROOT = resolve(process.env.TRIPTYCH_REVIEW_ROOT || resolve(import.meta.dirname, '../..'));
const OVERLAY = process.env.TRIPTYCH_BIBLE_COMPARE_MODULE_ROOT;
const CHROME = process.env.TRIPTYCH_CHROME || '/usr/bin/chromium';
const SCRATCH = resolve(process.env.TRIPTYCH_BROWSER_SCRATCH ||
  resolve(ROOT, '.scratch/c18-bible-compare/browser'));
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
  const identity = '#missal=roman-1962&type=seasonal&mass=advent-1&bible=douay-rheims&orations=la';
  const source = 'proper/roman-1962/advent-1/006', location = 'compare/source/' + source;
  const comparison = '&mode=compare&compare=bible-edition&peer-bible=king-james-version';
  const ready = async () => waitFor(cdp, `window.propersReaderDebug?.ready && document.getElementById('reader-document').getAttribute('aria-busy') === 'false'`, 'settled Propers');
  const click = async (selector) => evaluate(cdp, `document.querySelector(${JSON.stringify(selector)}).click()`);
  const choose = async (selector, value) => evaluate(cdp, `(() => { const node = document.querySelector(${JSON.stringify(selector)}); node.value = ${JSON.stringify(value)}; node.dispatchEvent(new Event('change', { bubbles: true })); })()`);
  const settle = async () => evaluate(cdp, `(async () => { let previous = NaN, stable = 0; for (let n = 0; n < 240 && stable < 8; n += 1) { await new Promise(requestAnimationFrame); stable = Math.abs(scrollY - previous) < 0.5 ? stable + 1 : 0; previous = scrollY; } })()`);
  const screenshot = async (name) => { const shot = await cdp.send('Page.captureScreenshot', { format: 'png' }); await writeFile(resolve(SCRATCH, name), Buffer.from(shot.data, 'base64')); };
  async function visit(suffix, path = PROPERS, selection = identity) { await cdp.send('Page.navigate', { url: base + path + '?data=/src/web/data' + selection + suffix }); await ready(); }
  const projections = [];
  for (const path of [PROPERS, '/src/web/browser/liturgy/propers-reader.html']) {
    await visit(comparison + '&location=' + encodeURIComponent(location), path);
    const value = await evaluate(cdp, `({ outcome: propersReaderDebug.outcome, state: propersReaderDebug.state, semantic: propersReaderDebug.semantic,
      cells: [...document.querySelectorAll('[data-semantic-event-id="${location}"] .compare-side')].map(node => ({text:node.textContent,bible:node.dataset.bibleEdition,citations:node.dataset.bibleCitations})),
      contents: [...document.querySelectorAll('[data-reader-location]')].map(node => node.dataset.readerLocation),
      text: document.getElementById('reader-document').textContent })`);
    assert.equal(value.outcome, 'ready'); assert.equal(value.state.civilDate, null);
    assert.deepEqual(value.semantic.sides.map(side => side.id), ['douay-rheims', 'king-james-version']);
    assert.equal(value.semantic.units.length, 10); assert.equal(value.semantic.calendarResults, null);
    assert.ok(value.semantic.units.every(unit => unit.relation === 'same-source-event'));
    assert.deepEqual(value.cells.map(cell => cell.bible), ['douay-rheims', 'king-james-version']);
    assert.ok(value.cells.every(cell => /Bible reconstruction/.test(cell.text) && cell.citations === 'resolved'));
    assert.match(value.text, /Vulgate numbering/); assert.match(value.text, /hebrew numbering/i);
    assert.match(value.text, /exact Missal or Lectionary wording is not established/);
    assert.deepEqual(value.contents, value.semantic.units.map(unit => 'compare/source/' + unit.sourceCoordinate.eventId));
    projections.push(value.semantic);
  }
  assert.deepEqual(projections[0], projections[1]); assertions.push('canonical and retained routes render exact same-source occurrences with two distinct Bible identities numbering and qualifications');

  await visit('&mode=read&location=' + encodeURIComponent(source)); await settle();
  await click('[data-reader-action="mode"]'); await click('[data-mode="compare"]'); await choose('#reader-compare-dimension', 'bible-edition');
  const select = await evaluate(cdp, `({value:document.getElementById('reader-compare-peer-bible').value,options:[...document.getElementById('reader-compare-peer-bible').options].map(node=>node.value)})`);
  assert.equal(select.value, ''); assert.equal(select.options.length, 7); assert.ok(!select.options.includes('douay-rheims'));
  await click('#compare-setup .surface-apply');
  assert.equal(await evaluate(cdp, 'propersReaderDebug.state.requestedMode'), 'read');
  assert.equal(await evaluate(cdp, 'document.getElementById("reader-compare-peer-bible").validity.valueMissing'), true);
  await choose('#reader-compare-peer-bible', 'king-james-version');
  await screenshot('mode-explicit-bible-393x852.png');
  await evaluate(cdp, `document.querySelector('#compare-setup .surface-apply').focus()`); await key(cdp, 'Enter'); await ready(); await settle();
  assert.equal(await evaluate(cdp, 'propersReaderDebug.state.comparison.dimension'), 'bible-edition');
  assert.equal(await evaluate(cdp, 'propersReaderDebug.state.semanticLocation.eventId'), location);
  assert.equal(await evaluate(cdp, 'document.activeElement.dataset.readerAction'), 'mode');
  assert.equal(await evaluate(cdp, 'propersReaderDebug.state.languages.orations'), 'la');
  assertions.push('Mode requires an explicit published peer and keyboard application preserves source Gospel selection and Mode focus');
  assert.ok(await evaluate(cdp, `(() => {const top = document.querySelector('[data-semantic-event-id="${location}"]').getBoundingClientRect().top; return top >= 0 && top <= 280;})()`));
  await screenshot('bible-gospel-pair-393x852.png');

  await cdp.send('Emulation.setDeviceMetricsOverride', { width: 320, height: 852, deviceScaleFactor: 1, mobile: false });
  assert.equal(await evaluate(cdp, 'document.documentElement.scrollWidth > document.documentElement.clientWidth + 1'), false);
  assert.equal(await evaluate(cdp, `(() => { const sides = [...document.querySelectorAll('.compare-unit:last-child .compare-side')]; return sides[1].getBoundingClientRect().top >= sides[0].getBoundingClientRect().bottom; })()`), true);
  assertions.push('320-pixel Bible comparison stacks pairs without page overflow');
  await cdp.send('Emulation.setDeviceMetricsOverride', { width: 393, height: 852, deviceScaleFactor: 1, mobile: false });
  await visit(comparison + '&location=' + encodeURIComponent(location)); await settle();
  await click('[data-reader-action="mode"]'); await click('[data-mode="read"]'); await ready();
  const read = await evaluate(cdp, `({outcome:propersReaderDebug.outcome,state:propersReaderDebug.state,hash:location.hash,focus:document.activeElement.dataset.readerAction})`);
  assert.equal(read.outcome, 'ready'); assert.equal(read.state.semanticLocation.eventId, source); assert.equal(read.state.bible.id, 'douay-rheims');
  assert.equal(read.focus, 'mode'); assert.doesNotMatch(read.hash, /(?:compare|peer-bible)=/);
  assertions.push('return to Read keeps primary Bible and original source Gospel while clearing peer comparison');

  const epiphany = '#missal=roman-1962&type=christological&mass=epiphania-domini&bible=douay-rheims&orations=la';
  const refusedLocation = 'compare/source/proper/roman-1962/epiphania-domini/007';
  await visit(comparison + '&location=' + encodeURIComponent(refusedLocation), PROPERS, epiphany); await settle();
  const refusal = await evaluate(cdp, `({units:propersReaderDebug.semantic.units,
    cells:[...document.querySelectorAll('[data-semantic-event-id="${refusedLocation}"] .compare-side')].map(node=>({id:node.dataset.bibleEdition,state:node.dataset.bibleCitations,text:node.textContent,passages:node.querySelectorAll('.passage').length})),
    primary:propersReaderDebug.state.bible.id})`);
  const reason = 'English Bibles divide Psalm 72 differently from the Hebrew numbering, and no verse-for-verse correspondence is recorded for it';
  assert.equal(refusal.primary, 'douay-rheims'); assert.equal(refusal.cells[0].state, 'resolved'); assert.ok(refusal.cells[0].passages > 0);
  assert.equal(refusal.cells[1].state, 'refused'); assert.equal(refusal.cells[1].passages, 0); assert.ok(refusal.cells[1].text.includes(reason));
  const negative = refusal.units.find(unit=>unit.sourceCoordinate.eventId.endsWith('/007'));
  assert.deepEqual(negative.sides[1].bibleCitations, [{reference:'Psalms 71:10-11',state:'refused',reason}]);
  await screenshot('epiphany-offertory-refusal-393x852.png');
  assertions.push('real Epiphany Offertory keeps the KJV Psalm72 numbering refusal without another Bible fallback');

  await cdp.send('Emulation.setEmulatedMedia', { media: 'print' });
  const pdf = await cdp.send('Page.printToPDF', { printBackground: true, preferCSSPageSize: true });
  const pdfPath = resolve(SCRATCH, 'epiphany-bible-comparison.pdf'); await writeFile(pdfPath, Buffer.from(pdf.data, 'base64'));
  const text = execFileSync('/usr/bin/pdftotext', [pdfPath, '-'], { encoding: 'utf8' }).replace(/\s+/g, ' ');
  await writeFile(resolve(SCRATCH, 'epiphany-bible-comparison.txt'), text);
  assert.match(text, /In Epiphania Domini/); assert.match(text, /roman-1962/); assert.match(text, /epiphania-domini/);
  assert.match(text, /douay-rheims/); assert.match(text, /king-james-version/); assert.match(text, /Vulgate numbering/); assert.match(text, /hebrew numbering/i);
  assert.match(text, /Bible reconstruction/); assert.match(text, /public-domain/); assert.match(text, /English Bibles divide Psalm 72/);
  assert.match(text, /exact Missal or Lectionary wording is not established/); assert.match(text, /roman-1962\/epiphania-domini\/007/);
  assert.doesNotMatch(text, /Share link|Compare this formulary|Choose another Bible edition/);
  await cdp.send('Emulation.setEmulatedMedia', { media: 'screen' });
  assertions.push('print retains both Bible identities numbering rights source coordinates qualifications and precise refusal');

  for (const invalid of [comparison.replace('king-james-version', 'unknown'), comparison.replace('king-james-version', 'douay-rheims'),
    comparison.replace('&peer-bible=king-james-version', ''), comparison + '&peer-bible=clementine-vulgate', comparison + '&peer-cycle=A']) {
    await visit(invalid); assert.equal(await evaluate(cdp, 'propersReaderDebug.outcome'), 'invalid');
    assert.equal(await evaluate(cdp, 'document.querySelectorAll(".compare-unit").length'), 0);
  }
  assertions.push('unknown equal missing duplicate and wrong-dimension peers fail closed without fallback Bible text');
  assert.deepEqual(consoleProblems, []); assert.deepEqual(failedRequests, []); assert.deepEqual(httpProblems, []);
  const report = { status: 'pass', checks: assertions.length, assertions, consoleProblems, failedRequests, httpProblems };
  await writeFile(resolve(SCRATCH, 'report.json'), JSON.stringify(report, null, 2) + '\n');
  process.stdout.write(JSON.stringify(report) + '\n');
} catch (error) {
  const state = cdp ? await evaluate(cdp, `({ hash: location.hash, debug: window.propersReaderDebug })`).catch(() => null) : null;
  process.stderr.write(JSON.stringify({ status: 'fail', error: error.stack, state, assertions, consoleProblems, failedRequests, httpProblems }) + '\n'); process.exitCode = 1;
} finally {
  if (cdp) cdp.close(); const stopped = new Promise((done) => chrome.once('exit', done)); chrome.kill('SIGTERM'); await stopped;
  await new Promise((done) => instance.close(done)); await rm(profile, { recursive: true, force: true, maxRetries: 4, retryDelay: 100 });
}
