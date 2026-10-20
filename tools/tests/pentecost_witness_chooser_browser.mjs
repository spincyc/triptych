#!/usr/bin/env node

/* Focused source-served C4/G16 regression: unit-local options and partial witnesses. */

import assert from 'node:assert/strict';
import { spawn } from 'node:child_process';
import { createServer } from 'node:http';
import { mkdir, mkdtemp, readFile, rm } from 'node:fs/promises';
import { extname, resolve, sep } from 'node:path';

const ROOT = resolve(import.meta.dirname, '../..');
const DATA = '/src/web/data';
const DAY = '/src/web/browser/liturgy/day.html';
const PROPERS = '/src/web/browser/liturgy/index.html';
const CALENDAR = 'roman-1962';
const MASS = 'pentecost';
const CASWALL = 'edition.edward-caswall.lyra-catholica.london-1849';
const INTROIT = 'proper/roman-1962/pentecost/001';
const SEQUENCE = 'proper/roman-1962/pentecost/005';
const chromeBinary = process.env.TRIPTYCH_CHROME || '/usr/bin/chromium';
const failures = [];
const structure = JSON.parse(await readFile(resolve(ROOT,
  'src/web/data/structure/propers/roman-1962.json')));
const pentecost = structure.masses.find((mass) => mass.key === MASS);
assert.ok(pentecost, 'source-served Pentecost formulary is absent');
const introit = pentecost.propers[0];
assert.equal(introit.name, 'Introit');
const introitEnglish = introit.coverage.languages.find((entry) => entry.lang === 'en');
const introitBodyWitnesses = new Set((introitEnglish?.witnesses || []).map((row) => row.id));
assert.ok(introitBodyWitnesses.size, 'source-served English Introit has no witness');

function mime(path) {
  return ({ '.css': 'text/css', '.html': 'text/html', '.js': 'text/javascript',
    '.json': 'application/json', '.svg': 'image/svg+xml' })[extname(path)] ||
    'application/octet-stream';
}

const server = createServer(async (request, response) => {
  try {
    const pathname = new URL(request.url, 'http://127.0.0.1').pathname;
    if (pathname === '/favicon.ico') { response.writeHead(204); response.end(); return; }
    let relative = decodeURIComponent(pathname).replace(/^\/+/, '');
    // Source-served Bible chapters live in the source library, as in the reader harnesses.
    if (/^src\/web\/data\/[^/]+\/chapters\//.test(relative)) {
      relative = relative.replace(/^src\/web\/data\//, 'src/sources/bibles/');
    }
    const file = resolve(ROOT, relative);
    if (!file.startsWith(ROOT + sep)) throw new Error('outside repository');
    const body = await readFile(file);
    response.writeHead(200, { 'content-type': mime(file), 'cache-control': 'no-store' });
    response.end(body);
  } catch (_error) {
    response.writeHead(404, { 'content-type': 'text/plain' }); response.end('not found');
  }
});

async function listen(instance) {
  await new Promise((done, reject) => {
    instance.once('error', reject); instance.listen(0, '127.0.0.1', done);
  });
  return instance.address().port;
}

async function freePort() {
  const instance = createServer();
  const port = await listen(instance);
  await new Promise((done) => instance.close(done));
  return port;
}

async function waitJson(url) {
  for (let count = 0; count < 120; count += 1) {
    try { const response = await fetch(url); if (response.ok) return await response.json(); }
    catch (_error) { /* Chromium has not started listening yet. */ }
    await new Promise((done) => setTimeout(done, 50));
  }
  throw new Error('Chromium debugging endpoint did not start');
}

class CDP {
  constructor(url) { this.socket = new WebSocket(url); this.next = 0; this.pending = new Map(); }
  async ready() {
    await new Promise((done, reject) => {
      this.socket.addEventListener('open', done, { once: true });
      this.socket.addEventListener('error', reject, { once: true });
    });
    this.socket.addEventListener('message', (event) => {
      const message = JSON.parse(event.data);
      if (!message.id) return;
      const held = this.pending.get(message.id);
      if (!held) return;
      this.pending.delete(message.id); clearTimeout(held.timer);
      if (message.error) held.reject(new Error(message.error.message));
      else held.done(message.result);
    });
  }
  send(method, params = {}) {
    const id = ++this.next;
    return new Promise((done, reject) => {
      const timer = setTimeout(() => {
        this.pending.delete(id); reject(new Error('CDP timeout: ' + method));
      }, 20000);
      this.pending.set(id, { done, reject, timer });
      this.socket.send(JSON.stringify({ id, method, params }));
    });
  }
  close() { this.socket.close(); }
}

async function evaluate(cdp, expression) {
  const result = await cdp.send('Runtime.evaluate', {
    expression, awaitPromise: true, returnByValue: true, userGesture: true
  });
  if (result.exceptionDetails) {
    throw new Error(result.exceptionDetails.exception?.description || result.exceptionDetails.text);
  }
  return result.result.value;
}

async function waitFor(cdp, expression, description) {
  for (let count = 0; count < 180; count += 1) {
    if (await evaluate(cdp, `Boolean(${expression})`)) return;
    await new Promise((done) => setTimeout(done, 50));
  }
  throw new Error('Timed out waiting for ' + description);
}

function hash(values) { return '#' + new URLSearchParams(values).toString(); }

async function navigate(cdp, url, debugName) {
  await cdp.send('Page.navigate', { url });
  try {
    await waitFor(cdp,
      `location.pathname === ${JSON.stringify(new URL(url).pathname)} && ` +
        `window.${debugName}Ready === true`,
      debugName + ' committed render');
  } catch (error) {
    const diagnostic = await evaluate(cdp, `(() => ({href: location.href,
      ready: window.${debugName}Ready, debug: window.${debugName}Debug?.error,
      body: document.body?.textContent?.slice(0, 350)}))()`);
    throw new Error(error.message + ': ' + JSON.stringify(diagnostic));
  }
  const outcome = await evaluate(cdp, `${debugName}Debug.outcome`);
  assert.ok(['ready', 'unresolved'].includes(outcome),
    `${debugName} outcome: ${outcome}; ` + JSON.stringify(await evaluate(cdp,
      `${debugName}Debug.error`)));
}

async function check(name, action) {
  try { await action(); process.stdout.write('PASS ' + name + '\n'); }
  catch (error) {
    failures.push({ name, message: error.stack || String(error) });
    process.stderr.write('FAIL ' + name + ': ' + error.message + '\n');
  }
}

const port = await listen(server);
const debugPort = await freePort();
const scratch = resolve(ROOT, '.scratch');
await mkdir(scratch, { recursive: true });
const profile = await mkdtemp(resolve(scratch, 'triptych-pentecost-witness-'));
const chrome = spawn(chromeBinary, [
  '--headless=new', '--disable-gpu', '--no-sandbox', '--disable-dev-shm-usage',
  `--remote-debugging-port=${debugPort}`, `--user-data-dir=${profile}`, 'about:blank'
], { stdio: ['ignore', 'ignore', 'pipe'] });
let chromeError = '';
chrome.stderr.on('data', (chunk) => { chromeError += chunk.toString(); });

let cdp;
try {
  const pages = await waitJson(`http://127.0.0.1:${debugPort}/json`);
  cdp = new CDP(pages.find((page) => page.type === 'page').webSocketDebuggerUrl);
  await cdp.ready();
  await Promise.all([cdp.send('Page.enable'), cdp.send('Runtime.enable')]);
  const base = `http://127.0.0.1:${port}`;
  const dayState = {
    date: '2026-05-24', missal: CALENDAR, mass: MASS,
    bible: 'douay-rheims', orations: 'en', mode: 'read', why: '0', rubrics: '1'
  };
  const propersState = {
    missal: CALENDAR, type: 'seasonal', mass: MASS,
    bible: 'douay-rheims', orations: 'en'
  };

  await check('Day presents a Mass-wide witness choice outside the Introit', async () => {
    await navigate(cdp, base + DAY + '?data=' + DATA + hash(dayState), 'dayReader');
    const choice = await evaluate(cdp, `(() => {
      const fieldset = document.querySelector('[data-translation-witness-choice]');
      return fieldset && {
        owner: fieldset.closest('[data-semantic-event-id]')?.dataset.semanticEventId || null,
        scope: fieldset.dataset.translationWitnessChoice,
        legend: fieldset.querySelector('legend')?.textContent || '',
        ids: [...fieldset.querySelectorAll('[data-translation-witness]')]
          .map((input) => input.value)
      };
    })()`);
    assert.ok(choice, 'Mass-level witness choice is absent');
    assert.equal(choice.owner, null, 'Mass-wide choice sits inside a single Proper');
    assert.equal(choice.scope, 'mass/roman-1962/pentecost');
    assert.match(choice.legend, /this Mass/);
    assert.ok(choice.ids.some((id) => !introitBodyWitnesses.has(id)),
      'partial witnesses should remain available at Mass scope');
    assert.ok(choice.ids.includes(CASWALL));
  });

  await check('All Souls first Mass has one Mass-wide witness choice in Read and Missal', async () => {
    for (const mode of ['read', 'missal']) {
      const state = {
        ...dayState, date: '2026-11-02', mass: 'commemoratione-omnium-fidelium-defunctorum',
        form: 'first', mode,
        ...(mode === 'missal' ? { ordinary: '1', 'ordinary-lang': 'la' } : {})
      };
      await navigate(cdp, base + DAY + '?data=' + DATA + hash(state), 'dayReader');
      const controls = await evaluate(cdp, `(() => [...document.querySelectorAll(
        '[data-translation-witness-choice]')].map((fieldset) => ({
          scope: fieldset.dataset.translationWitnessChoice,
          legend: fieldset.querySelector('legend')?.textContent || '',
          options: [...fieldset.querySelectorAll('[data-translation-witness]')]
            .map((input) => input.value)
        })))()`);
      assert.equal(controls.length, 1, `${mode}: duplicate Mass-wide controls`);
      assert.equal(controls[0].scope,
        'mass/roman-1962/commemoratione-omnium-fidelium-defunctorum');
      assert.match(controls[0].legend, /this Mass/);
      assert.equal(controls[0].options.length, 3);
    }
  });

  await check('Propers Mass-level chooser retains the partial Caswall witness', async () => {
    await navigate(cdp, base + PROPERS + '?data=' + DATA + hash(propersState), 'propersReader');
    await evaluate(cdp, `document.querySelector('[data-reader-action="browse"]').click()`);
    const choices = await evaluate(cdp, `(() => ({
      hidden: document.querySelector('#reader-witness-field').hidden,
      ids: [...document.querySelector('#reader-witness').options].map((option) => option.value)
    }))()`);
    assert.equal(choices.hidden, false);
    assert.ok(choices.ids.includes(CASWALL));
    await evaluate(cdp, `(() => {
      const witness = document.querySelector('#reader-witness');
      witness.value = ${JSON.stringify(CASWALL)};
      witness.dispatchEvent(new Event('change', { bubbles: true }));
      document.querySelector('#browse-form .surface-apply').click();
    })()`);
    await waitFor(cdp,
      `propersReaderDebug.state?.languages?.translationWitness === ${JSON.stringify(CASWALL)}`,
      'Caswall Browse selection');
    const selected = await evaluate(cdp,
      `new URLSearchParams(location.hash.slice(1)).get('translation-witness')`);
    assert.equal(selected, CASWALL);
  });

  await check('Caswall deep links keep the typed Introit gap and Sequence body in Day', async () => {
    const url = base + DAY + '?data=' + DATA + hash({
      ...dayState, 'translation-witness': CASWALL
    });
    await navigate(cdp, url, 'dayReader');
    const result = await evaluate(cdp, `(() => {
      const events = dayReaderDebug.semantic?.events || [];
      const proper = (id) => events.find((event) => event.id === id);
      const sequence = proper(${JSON.stringify(SEQUENCE)})?.selected;
      return {
        hash: location.hash,
        introitDom: (() => {
          const node = [...document.querySelectorAll('[data-semantic-event-id]')]
            .find((row) => row.dataset.semanticEventId === ${JSON.stringify(INTROIT)});
          return { absences: [...(node?.querySelectorAll('[data-unit-absence]') || [])]
              .map((note) => note.dataset.unitAbsence),
            latinPresent: Boolean(node?.querySelector('[lang="la"]')?.textContent?.trim()) };
        })(),
        sequenceAvailability: sequence?.availability,
        sequenceBody: Boolean(sequence?.text)
      };
    })()`);
    assert.equal(new URLSearchParams(result.hash.slice(1)).get('translation-witness'), CASWALL);
    assert.ok(result.introitDom.absences.includes('en:absent-in-witness'),
      JSON.stringify(result));
    assert.equal(result.sequenceAvailability, 'held');
    assert.ok(result.sequenceBody, 'Caswall Sequence body is absent');
    assert.ok(result.introitDom.latinPresent, 'Latin Introit should remain visible');
  });

  await check('Caswall deep links preserve the same unit outcomes in Propers', async () => {
    const url = base + PROPERS + '?data=' + DATA + hash({
      ...propersState, 'translation-witness': CASWALL
    });
    await navigate(cdp, url, 'propersReader');
    const result = await evaluate(cdp, `(() => {
      const events = propersReaderDebug.semantic?.events || [];
      const proper = (id) => events.find((event) => event.id === id);
      const sequence = proper(${JSON.stringify(SEQUENCE)})?.selected;
      return {
        hash: location.hash,
        sequenceAvailability: sequence?.availability,
        sequenceBody: Boolean(sequence?.text),
        introitAbsences: [...(document.querySelector('[data-semantic-event-id="${INTROIT}"]')?.querySelectorAll('[data-unit-absence]') || [])]
          .map((note) => note.dataset.unitAbsence)
      };
    })()`);
    assert.equal(new URLSearchParams(result.hash.slice(1)).get('translation-witness'), CASWALL);
    assert.ok(result.introitAbsences.includes('en:absent-in-witness'),
      JSON.stringify(result));
    assert.equal(result.sequenceAvailability, 'held');
    assert.ok(result.sequenceBody, 'Caswall Sequence body is absent');
  });
} catch (error) {
  failures.push({ name: 'harness', message: error.stack || String(error) });
} finally {
  if (cdp) cdp.close();
  if (chrome.exitCode === null && chrome.signalCode === null) {
    const exited = new Promise((done) => chrome.once('exit', done));
    chrome.kill('SIGTERM'); await exited;
  }
  server.closeAllConnections();
  await new Promise((done) => server.close(done));
  await rm(profile, { recursive: true, force: true, maxRetries: 5, retryDelay: 100 });
}

if (failures.length) {
  for (const failure of failures) process.stderr.write(failure.name + ': ' + failure.message + '\n');
  if (failures.some((failure) => failure.name === 'harness')) process.stderr.write(chromeError);
  process.exitCode = 1;
}
process.stdout.write(JSON.stringify({
  status: failures.length ? 'fail' : 'pass',
  assertions: [
    'Day presents a Mass-wide witness choice outside the Introit',
    'All Souls first Mass has one Mass-wide witness choice in Read and Missal',
    'Propers Mass-level chooser retains the partial Caswall witness',
    'Caswall deep links keep the typed Introit gap and Sequence body in Day',
    'Caswall deep links preserve the same unit outcomes in Propers'
  ].map((name) => ({
    name, status: failures.some((failure) => failure.name === name) ? 'fail' : 'pass'
  })),
  failures
}) + '\n');
