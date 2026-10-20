#!/usr/bin/env node

/* Same-language translation witnesses over exact same-source Proper coordinates. */

import assert from 'node:assert/strict';
import { spawn, execFileSync } from 'node:child_process';
import { createServer } from 'node:http';
import { mkdir, mkdtemp, readFile, rm, writeFile } from 'node:fs/promises';
import { extname, resolve, sep } from 'node:path';

const ROOT = resolve(process.env.TRIPTYCH_REVIEW_ROOT || resolve(import.meta.dirname, '../..'));
const OVERLAY = process.env.TRIPTYCH_TRANSLATION_MODULE_ROOT;
const CHROME = process.env.TRIPTYCH_CHROME || '/usr/bin/chromium';
const SCRATCH = resolve(process.env.TRIPTYCH_BROWSER_SCRATCH ||
  resolve(ROOT, '.scratch/reader-translation-compare/browser'));
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

const instance = server(), port = await listen(instance), debugPort = await freePort();
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
  cdp.on('Runtime.consoleAPICalled', ({ type, args }) => { if (type === 'error' || type === 'warning') consoleProblems.push(args.map(one => one.value || one.description || '').join(' ')); });
  cdp.on('Network.loadingFailed', ({ canceled, errorText }) => { if (!canceled) failedRequests.push(errorText); });
  cdp.on('Network.responseReceived', ({ response }) => { if (response?.status >= 400) httpProblems.push({ status: response.status, url: response.url }); });
  await Promise.all([cdp.send('Page.enable'), cdp.send('Runtime.enable'), cdp.send('Network.enable')]);
  await cdp.send('Page.addScriptToEvaluateOnNewDocument', { source: `Storage.prototype.getItem = function () { throw new Error('storage unavailable'); }; Storage.prototype.setItem = function () { throw new Error('storage unavailable'); };` });
  await cdp.send('Emulation.setDeviceMetricsOverride', { width: 1440, height: 900, deviceScaleFactor: 1, mobile: false });
  const base = `http://127.0.0.1:${port}`, key = 'commemoratione-omnium-fidelium-defunctorum';
  const caswall = 'edition.edward-caswall.lyra-catholica.london-1849';
  const irons = 'edition.hymns-ancient-and-modern-proprietors.hymns-ancient-and-modern.london-complete-edition-1890';
  const cummiskey = 'edition.eugene-cummiskey.roman-missal-english-laity.philadelphia-1861';
  const sequence = 'proper/roman-1962/' + key + '/006', compareSequence = 'compare/source/' + sequence;
  const identity = '#missal=roman-1962&type=sanctoral&mass=' + key + '&form=first&bible=douay-rheims&orations=en&translation-witness=' + caswall;
  const axis = '&mode=compare&compare=translation-witness&peer-witness=';
  const ready = async () => waitFor(cdp, `window.propersReaderDebug?.ready && document.getElementById('reader-document').getAttribute('aria-busy') === 'false'`, 'settled Propers');
  const click = async selector => evaluate(cdp, `document.querySelector(${JSON.stringify(selector)}).click()`);
  const choose = async (selector, value) => evaluate(cdp, `(() => { const node = document.querySelector(${JSON.stringify(selector)}); node.value = ${JSON.stringify(value)}; node.dispatchEvent(new Event('change', { bubbles: true })); })()`);
  async function visit(suffix, path = PROPERS) { await cdp.send('Page.navigate', { url: base + path + '?data=/src/web/data' + identity + suffix }); await ready(); }
  async function capture() {
    return evaluate(cdp, `({ outcome: propersReaderDebug.outcome, error: propersReaderDebug.error, state: propersReaderDebug.state, semantic: propersReaderDebug.semantic,
      sequence: [...document.querySelectorAll('[data-semantic-event-id="${compareSequence}"] .compare-side')].map(side => ({ status: side.dataset.compareStatus, text: side.textContent })),
      contents: [...document.querySelectorAll('[data-reader-location]')].map(node => node.dataset.readerLocation), hash: location.hash })`);
  }
  const projections = [];
  for (const path of [PROPERS, '/src/web/browser/liturgy/propers-reader.html']) {
    await visit(axis + irons + '&location=' + encodeURIComponent(compareSequence), path);
    const value = await capture(); assert.equal(value.outcome, 'ready', JSON.stringify(value.error));
    assert.equal(value.state.civilDate, null); assert.equal(value.semantic.units.length, 11);
    assert.ok(value.semantic.units.every(unit => unit.relation === 'same-source-event'));
    assert.equal(value.semantic.units[5].sourceCoordinate.eventId, sequence);
    assert.deepEqual(value.sequence.map(side => side.status), ['text-held', 'text-held']);
    assert.match(value.sequence[0].text, /historical-antecedent/); assert.match(value.sequence[1].text, /Target relationship: unresolved/);
    assert.ok(value.sequence.every(side => /public-domain/.test(side.text) && /Target collation: unresolved/.test(side.text)));
    assert.deepEqual(value.contents, value.semantic.units.map(unit => unit.location));
    projections.push(value.semantic);
  }
  assert.deepEqual(projections[0], projections[1]); assertions.push('canonical and retained routes compare eleven source coordinates including two held qualified Sequence witnesses');

  await visit(axis + cummiskey); const partial = await capture(); assert.equal(partial.outcome, 'ready');
  const collect = partial.semantic.units.find(unit => unit.sourceCoordinate.ordinal === 2);
  const seq = partial.semantic.units.find(unit => unit.sourceCoordinate.ordinal === 6);
  assert.deepEqual(collect.sides.map(side => side.status), ['text-unavailable', 'text-held']);
  assert.deepEqual(seq.sides.map(side => side.status), ['text-held', 'text-unavailable']);
  assert.match(partial.sequence[1].text, /absent-in-witness/);
  assertions.push('partial witness union preserves opposite Cummiskey prayer and Caswall Sequence gaps without substitution');

  await visit('&mode=read&location=' + encodeURIComponent(sequence));
  await waitFor(cdp, `document.querySelector('[data-semantic-event-id="${sequence}"]')?.getBoundingClientRect().top <= 280`, 'Read Sequence location');
  await evaluate(cdp, `(async () => { for (let n = 0; n < 12; n += 1) await new Promise(requestAnimationFrame); })()`);
  await click('[data-reader-action="mode"]'); await click('[data-mode="compare"]'); await choose('#reader-compare-dimension', 'translation-witness');
  assert.equal(await evaluate(cdp, 'document.getElementById("reader-compare-witness").value'), caswall);
  assert.equal(await evaluate(cdp, 'document.getElementById("reader-compare-peer-witness").value'), '');
  await choose('#reader-compare-peer-witness', caswall); await click('#compare-setup .surface-apply');
  assert.equal(await evaluate(cdp, 'propersReaderDebug.state.requestedMode'), 'read');
  await choose('#reader-compare-peer-witness', irons); await click('#compare-setup .surface-apply'); await ready();
  const selected = await capture(); assert.equal(selected.outcome, 'ready', JSON.stringify(selected.error));
  assert.equal(selected.state.semanticLocation.eventId, compareSequence);
  assert.equal(await evaluate(cdp, 'document.activeElement.dataset.readerAction'), 'mode');
  await waitFor(cdp, `document.querySelector('[data-semantic-event-id="${compareSequence}"]')?.getBoundingClientRect().top <= 280`, 'Compare Sequence location');
  await evaluate(cdp, `(async () => { for (let n = 0; n < 12; n += 1) await new Promise(requestAnimationFrame); })()`);
  await click('[data-reader-action="mode"]'); await click('[data-mode="read"]'); await ready();
  assert.equal(await evaluate(cdp, 'propersReaderDebug.state.semanticLocation.eventId'), sequence);
  assert.equal(await evaluate(cdp, 'propersReaderDebug.state.languages.translationWitness'), caswall);
  assert.doesNotMatch(await evaluate(cdp, 'location.hash'), /peer-witness=|compare=translation-witness/);
  assertions.push('explicit witness controls preserve unmapped Sequence location and Mode focus through Compare and Read');

  await visit(axis + irons + '&text-display=latin-and-selected');
  assert.equal(await evaluate(cdp, 'propersReaderDebug.state.textDisplay'), 'latin-and-selected');
  await cdp.send('Emulation.setDeviceMetricsOverride', { width: 320, height: 852, deviceScaleFactor: 1, mobile: false });
  assert.equal(await evaluate(cdp, 'document.documentElement.scrollWidth > document.documentElement.clientWidth + 1'), false);
  assert.equal(await evaluate(cdp, `(() => { const sides = [...document.querySelectorAll('[data-semantic-event-id="${compareSequence}"] .compare-side')]; return sides[1].getBoundingClientRect().top >= sides[0].getBoundingClientRect().bottom; })()`), true);
  assertions.push('320-pixel comparison stacks source pairs while preserving Latin-accompaniment state');

  await cdp.send('Emulation.setEmulatedMedia', { media: 'print' });
  const pdf = await cdp.send('Page.printToPDF', { printBackground: true, preferCSSPageSize: true });
  const pdfPath = resolve(SCRATCH, 'allsouls-translation-witnesses.pdf'); await writeFile(pdfPath, Buffer.from(pdf.data, 'base64'));
  const text = execFileSync('/usr/bin/pdftotext', [pdfPath, '-'], { encoding: 'utf8' });
  assert.match(text, /roman-1962/); assert.match(text, /First Mass/); assert.match(text, /Sequence/);
  assert.match(text, /Lyra Catholica/); assert.match(text, /Hymns Ancient and Modern/);
  assert.match(text, /historical-antecedent/); assert.match(text, /Target relationship: unresolved/);
  assert.match(text, /Target collation: unresolved/); assert.match(text, /public-domain/);
  assert.doesNotMatch(text, /Share link|Compare this formulary|Primary translation witness/);
  await cdp.send('Emulation.setEmulatedMedia', { media: 'screen' });
  assertions.push('printed witness pairs retain form source rights and unresolved target qualifications without controls');

  for (const peer of ['not-held', caswall, 'artifact.edward-caswall.lyra-catholica.london-1849.missal-sequences-en']) {
    await visit(axis + peer); assert.equal((await capture()).outcome, 'invalid');
    assert.equal(await evaluate(cdp, 'document.querySelectorAll(".compare-unit").length'), 0);
  }
  await visit(axis + irons + '&peer-cycle=A'); assert.equal((await capture()).outcome, 'invalid');
  assertions.push('unknown equal alias-duplicate and wrong-axis witness peers fail closed');
  assert.deepEqual(consoleProblems, []); assert.deepEqual(failedRequests, []); assert.deepEqual(httpProblems, []);
  process.stdout.write(JSON.stringify({ status: 'pass', checks: assertions.length, assertions, consoleProblems, failedRequests, httpProblems }) + '\n');
} catch (error) {
  const state = cdp ? await evaluate(cdp, `({ hash: location.hash, debug: window.propersReaderDebug })`).catch(() => null) : null;
  process.stderr.write(JSON.stringify({ status: 'fail', error: error.stack, state, assertions, consoleProblems, failedRequests, httpProblems }) + '\n'); process.exitCode = 1;
} finally {
  if (cdp) cdp.close(); const stopped = new Promise(done => chrome.once('exit', done)); chrome.kill('SIGTERM'); await stopped;
  await new Promise(done => instance.close(done)); await rm(profile, { recursive: true, force: true, maxRetries: 4, retryDelay: 100 });
}
