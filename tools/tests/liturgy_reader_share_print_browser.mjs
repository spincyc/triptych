#!/usr/bin/env node

/* Source-served Chromium coverage for both reader Share/Print entrances. */

import assert from 'node:assert/strict';
import { execFile, spawn } from 'node:child_process';
import { createServer } from 'node:http';
import { mkdir, mkdtemp, readFile, rm, writeFile } from 'node:fs/promises';
import { extname, resolve, sep } from 'node:path';
import { promisify } from 'node:util';

const ROOT = resolve(import.meta.dirname, '../..');
const CHROME = process.env.TRIPTYCH_CHROME || '/usr/bin/chromium';
const SCRATCH = resolve(process.env.TRIPTYCH_BROWSER_SCRATCH ||
  resolve(ROOT, '.scratch/reader-share-print-browser'));
const DAY = '/src/web/browser/liturgy/day.html';
const PROPERS = '/src/web/browser/liturgy/index.html';
const execFileAsync = promisify(execFile);

// Physical PDF regressions follow source-owned reader text.
const SHORT_ORDINARY_PRINT = [
  ['psalmus-xlii-heading', null, 'Psalm xlii.'],
  ['judica-me-deus', 'dum affligit me inimicus?', 'whilst the enemy afflicteth me?'],
  ['emitte-lucem-tuam', 'ad Deum qui lætificat juventutem meam.', 'to God who giveth joy to my youth.'],
  ['confitebor-tibi-in-cithara', 'salutare vultus mei, et Deus meus.', 'the salvation of my countenance and my God.'],
  ['kyrie-eleison', 'Kyrie eleison.', 'Lord, have mercy upon us.'],
  ['christe-eleison', 'Christe eleison.', 'Christ, have mercy upon us.']
];
const compactPdfText = text => text.normalize('NFKC').replace(/[\s\u00ad]+/gu, '');

function pdfPages(text) {
  const pages = text.split('\f');
  if (!pages.at(-1).trim()) pages.pop();
  assert.ok(pages.length > 0 && pages.every(page => page.trim()),
    'printed reader must not acquire a blank page');
  return pages;
}

function pdfWordBottoms(bbox) {
  return [...bbox.matchAll(/<page\b[^>]*>(.*?)<\/page>/gs)].map(match => {
    const words = [...match[1].matchAll(/<word\b[^>]*yMax="([^"]+)"/g)];
    return words.length ? Math.max(...words.map(word => Number(word[1]))) : 0;
  });
}

function assertNoSparseInteriorPages(pages, bbox, label) {
  const bounds = pdfWordBottoms(bbox);
  assert.equal(bounds.length, pages.length, 'text and word bounds cover the same PDF pages');
  assert.ok(bounds.length >= 3, label + ' fixture spans interior pages');
  // Letter with 0.7in margins: an interior page ending before 400pt leaves
  // a large blank tail. Attachment fixes must also preserve this bound.
  for (const [index, bottom] of bounds.entries()) {
    if (index > 0 && index < bounds.length - 1) {
      assert.ok(bottom >= 400, 'interior ' + label + ' page ' + (index + 1) +
        ' ends at ' + bottom + 'pt, leaving excessive blank space');
    }
  }
  return bounds.slice(1,-1);
}

function assertAlternativePdf(pages, bbox) {
  const psalmPage = pages.findIndex(page => page.includes('Responsorial psalm'));
  assert.ok(psalmPage >= 0, 'Responsorial Psalm heading is printed');
  assert.ok((pages[psalmPage].match(/Psalm 24:7/g) || []).length >= 2 &&
    (pages[psalmPage].match(/Lift up your gates/g) || []).length >= 2,
    'Responsorial Psalm heading, both citations and first verses must share a page');
  const gospelPage = pages.findIndex(page => page.includes('Luke 2:22-40'));
  assert.ok(gospelPage >= 0, 'long Gospel citation is printed');
  assert.ok(pages[gospelPage].includes('Luke 2:22-32') &&
    (pages[gospelPage].match(/And after the days/g) || []).length >= 2,
    'both Gospel citations and first words must share a page');
  assert.ok(gospelPage < pages.length - 1, 'the long Gospel remains fragmentable');
  const interiorWordBottoms = assertNoSparseInteriorPages(pages, bbox, 'Compare');
  for (const id of ['001', '002', '003', '004', '005', '006']) {
    assert.ok(pages.join('\n').includes('postconciliar/presentation-lord/' + id),
      'printed alternative source ' + id + ' survives');
  }
  return {pages:pages.length, psalmPage:psalmPage + 1,
    gospelPage:gospelPage + 1, interiorWordBottoms};
}

function assertShortOrdinaryPdf(pages, bbox, owners) {
  const normalized = pages.map(page => page.replace(/\s+/g, ' '));
  const compactPages = normalized.map(compactPdfText), starts = [];
  let length = 0;
  for (const page of compactPages) { starts.push(length); length += page.length; }
  const text = compactPages.join('');
  const pageAt = offset => starts.findLastIndex(start => start <= offset);
  const joins = [];
  for (const [index, [key, latinTail, englishTail]] of SHORT_ORDINARY_PRINT.entries()) {
    const id = 'ordinary-element/praeparatio/' + key;
    const owner = owners[index];
    assert.equal(owner.id, id); assert.equal(owner.exists, true, id);
    assert.equal(owner.noteId, id, 'Study note belongs to its own Ordinary event');
    assert.equal(owner.noteLast, true, id);
    assert.deepEqual(owner.sides.map(side => side.lang), ['la','en']);
    assert.equal(owner.noteLanguage, 'en', 'this fixture selects the English Ordinary');
    assert.deepEqual({language:owner.noteLanguage,sourceId:owner.noteSourceId,
      relation:owner.noteRelation,collation:owner.noteCollation}, owner.selected,
      'own Study facts describe the actual selected source witness');
    const heading = new RegExp('Study notes for ' + id + '(?=\\s|$)');
    const matches = normalized.map((page, index) => heading.test(page) ? index : -1)
      .filter(index => index >= 0);
    assert.equal(matches.length, 1, 'exactly one own Study heading for ' + id);
    const page = normalized[matches[0]], at = page.search(heading);
    const noteAt = starts[matches[0]] + compactPdfText(page.slice(0, at)).length;
    // Bind repeated words to their authored language-label interval. The
    // English Kyrie/Christe body also repeats the Latin spoken words.
    const ranges = [], sideProof = [];
    let boundary = noteAt;
    for (let sideIndex = owner.sides.length - 1; sideIndex >= 0; sideIndex--) {
      const side = owner.sides[sideIndex];
      if (!side.held) continue;
      assert.ok(side.label, id + ' language label');
      const label = compactPdfText(side.label);
      const labelAt = text.lastIndexOf(label, boundary - 1);
      assert.ok(labelAt >= 0, id + ' own ' + side.lang + ' label precedes its body');
      ranges[sideIndex] = {start:labelAt + label.length,end:boundary,labelAt};
      boundary = labelAt;
    }
    for (const [sideIndex, expected] of [latinTail,englishTail].entries()) {
      const side = owner.sides[sideIndex];
      if (expected === null) {
        assert.equal(side.held, false, id + ' explicit Latin witness gap');
        continue;
      }
      assert.equal(side.held, true, id + ' ' + side.lang);
      assert.ok(side.sourceId && side.credit.startsWith('Source: '), id + ' source credit');
      assert.ok(compactPdfText(side.tail).endsWith(compactPdfText(expected)),
        id + ' substantive tail belongs to its actual language body');
      const range = ranges[sideIndex], tail = compactPdfText(expected), credit = compactPdfText(side.credit);
      const tailAt = text.lastIndexOf(tail, range.end - 1);
      assert.ok(tailAt >= range.start && tailAt + tail.length <= range.end,
        id + ' ' + side.lang + ' substantive tail remains inside its own language body');
      const creditAt = text.indexOf(credit, tailAt + tail.length);
      assert.ok(creditAt >= 0 && creditAt + credit.length <= range.end,
        id + ' ' + side.lang + ' source credit follows its own body tail');
      const tailPage = pageAt(tailAt), creditPage = pageAt(creditAt);
      assert.equal(pageAt(tailAt + tail.length - 1), tailPage);
      assert.equal(creditPage, tailPage, id + ' source credit stays on its body-tail page');
      assert.equal(pageAt(creditAt + credit.length - 1), tailPage);
      if (side.lang === owner.noteLanguage) {
        assert.equal(side.sourceId, owner.noteSourceId);
        assert.equal(tailPage, matches[0], id + ' selected-language tail and own Study note share a page');
      }
      sideProof.push({language:side.lang,labelPage:pageAt(range.labelAt) + 1,
        tailPage:tailPage + 1,creditPage:creditPage + 1});
    }
    assert.ok(compactPdfText(page.slice(at)).includes(
      compactPdfText('ordinary-structure: roman-1962/praeparatio/' + key)),
      id + ' own Study facts remain with their heading');
    assert.ok(compactPdfText(page.slice(at)).includes(compactPdfText('Language ' + owner.noteLanguage)) &&
      compactPdfText(page.slice(at)).includes(compactPdfText('Witness ' + owner.noteSourceId)),
      id + ' printed note identifies its selected language and witness');
    joins.push({id,page:matches[0] + 1,noteLanguage:owner.noteLanguage,sides:sideProof});
  }
  const interiorWordBottoms = assertNoSparseInteriorPages(pages, bbox, 'Study');
  return {pages:pages.length,joins,interiorWordBottoms};
}
// End physical PDF regression assertions.

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
const failures = [];
let activeCase = 'setup';
try {
  const pages = await waitJson(`http://127.0.0.1:${debugPort}/json`);
  cdp = new CDP(pages.find((page) => page.type === 'page').webSocketDebuggerUrl);
  await cdp.ready();
  cdp.on('Runtime.exceptionThrown', ({ exceptionDetails }) => {
    consoleProblems.push(exceptionDetails?.exception?.description ||
      exceptionDetails?.text || 'uncaught page exception');
  });
  cdp.on('Runtime.consoleAPICalled', ({ type, args }) => {
    if (type === 'error' || type === 'warning') {
      consoleProblems.push(args.map((one) => one.value || one.description || '').join(' '));
    }
  });
  cdp.on('Network.loadingFailed', ({ canceled, errorText, requestId }) => {
    failedRequests.push({ canceled: Boolean(canceled), errorText, requestId });
  });
  cdp.on('Network.responseReceived', ({ response }) => {
    if (response?.status >= 400) {
      httpProblems.push({ status: response.status, url: response.url });
    }
  });
  await Promise.all([cdp.send('Page.enable'), cdp.send('Runtime.enable'),
    cdp.send('Network.enable')]);
  await cdp.send('Page.addScriptToEvaluateOnNewDocument', { source: `
    Storage.prototype.getItem = function () { throw new Error('storage unavailable'); };
    Storage.prototype.setItem = function () { throw new Error('storage unavailable'); };
  ` });
  const base = `http://127.0.0.1:${port}`;

  async function check(entrance, hash) {
    const path = entrance === 'day' ? DAY : PROPERS;
    await cdp.send('Page.navigate', { url: base + path + '?data=/src/web/data' + hash });
    await waitFor(cdp, `window.${entrance}ReaderDebug?.ready &&
      document.querySelector('[data-reader-share-print]')`, entrance + ' reader');
    assert.equal(await evaluate(cdp, `${entrance}ReaderDebug.outcome`), 'ready',
      JSON.stringify(await evaluate(cdp, `${entrance}ReaderDebug.error`)));
    const before = await evaluate(cdp, 'location.href');
    const state = await evaluate(cdp, `${entrance}ReaderDebug.state`);
    assert.equal(state.entrance, entrance);
    await evaluate(cdp, `(() => {
      window.__shared = null;
      navigator.share = async (value) => { window.__shared = value; };
      window.__printed = 0;
      window.print = () => { window.__printed += 1; };
      document.querySelector('[data-reader-action="mode"]').click();
      document.querySelector('[data-reader-action="details"]').click();
    })()`);
    await waitFor(cdp, `document.querySelector('[data-reader-surface="details"]').open &&
      document.querySelector('[data-reader-share-print]')`, 'Details controls');
    const accessible = await evaluate(cdp, `(() => {
      const block = document.querySelector('[data-reader-share-print]');
      const buttons = [...block.querySelectorAll('button')];
      return { buttons: buttons.map((button) => ({ tag: button.tagName,
        type: button.type, tabIndex: button.tabIndex,
        visible: button.getClientRects().length > 0,
        label: button.textContent.trim() })),
        role: block.querySelector('[role="status"]')?.getAttribute('aria-live') };
    })()`);
    assert.deepEqual(accessible.buttons.map((button) => button.label), ['Share link', 'Print']);
    assert.ok(accessible.buttons.every((button) => button.tag === 'BUTTON' &&
      button.type === 'button' && button.tabIndex === 0 && button.visible));
    assert.equal(accessible.role, 'polite');
    await cdp.send('Input.dispatchKeyEvent', {
      type: 'keyDown', key: 'Tab', code: 'Tab', windowsVirtualKeyCode: 9
    });
    await cdp.send('Input.dispatchKeyEvent', {
      type: 'keyUp', key: 'Tab', code: 'Tab', windowsVirtualKeyCode: 9
    });
    assert.equal(await evaluate(cdp,
      `document.activeElement === document.querySelector('[data-reader-share-print] button')`), true);
    await cdp.send('Input.dispatchKeyEvent', {
      type: 'keyDown', key: ' ', code: 'Space', text: ' ', windowsVirtualKeyCode: 32
    });
    await cdp.send('Input.dispatchKeyEvent', {
      type: 'keyUp', key: ' ', code: 'Space', windowsVirtualKeyCode: 32
    });
    await waitFor(cdp, `window.__shared`, 'native share');
    const shared = await evaluate(cdp, 'window.__shared');
    assert.equal(shared.url, before);
    assert.deepEqual(Object.keys(shared).sort(), ['title', 'url']);
    assert.match(shared.title, new RegExp(state.edition.id));
    if (entrance === 'day') {
      assert.match(shared.title, /2026-11-22/);
      if (state.requestedMode === 'compare') {
        assert.match(shared.title, /Compare recension with postconciliar/);
        assert.match(shared.title, /universal/);
        assert.match(new URL(shared.url).hash, /territory=universal/);
      } else assert.match(shared.title, /study/);
    } else {
      assert.doesNotMatch(shared.title, /2026-11-22/);
      assert.equal(new URL(shared.url).hash.includes('date='), false);
      if (state.requestedMode === 'compare') {
        assert.match(shared.title, /Compare oration-language with en/);
      }
    }
    assert.equal(await evaluate(cdp, 'location.href'), before);
    assert.equal(await evaluate(cdp,
      `document.querySelector('[data-reader-share-print] [role="status"]').textContent`),
    'Shared this reader link.');

    await evaluate(cdp, `(() => {
      navigator.share = undefined;
      Object.defineProperty(navigator, 'clipboard', { configurable: true,
        value: { writeText: async (value) => { window.__copied = value; } } });
      window.__copied = null;
      document.querySelector('[data-reader-share-print] button').click();
    })()`);
    await waitFor(cdp, 'window.__copied', 'clipboard fallback');
    assert.equal(await evaluate(cdp, 'window.__copied'), before);
    assert.equal(await evaluate(cdp,
      `document.querySelector('[data-reader-share-print] [role="status"]').textContent`),
    'Reader link copied to clipboard.');
    assert.equal(await evaluate(cdp,
      `document.activeElement === document.querySelector('[data-reader-share-print] button')`), true);
    await evaluate(cdp, `document.querySelectorAll('[data-reader-share-print] button')[1].click()`);
    assert.equal(await evaluate(cdp, 'window.__printed'), 1);
    assert.equal(await evaluate(cdp, 'location.href'), before);
    const expectedPrint = await evaluate(cdp, `(() => ({
      mode: document.querySelector('.reader-instrument').dataset.readerMode,
      studyNotes: document.querySelectorAll('#reader-document .study-event').length,
      studySources: [...document.querySelectorAll('#reader-document .study-event dt')]
        .filter((node) => node.textContent.trim() === 'Source record').length,
      compareSources: [...document.querySelectorAll('#reader-document .compare-evidence')]
        .filter((node) => node.textContent.trim().startsWith('Source records:')).length
    }))()`);
    assert.equal(expectedPrint.mode, state.requestedMode);
    await cdp.send('Emulation.setEmulatedMedia', { media: 'print' });
    const printed = await evaluate(cdp, `(() => ({
      controls: getComputedStyle(document.querySelector('[data-reader-share-print]')).display,
      dialog: getComputedStyle(document.querySelector('[data-reader-surface="details"]')).display,
      title: getComputedStyle(document.querySelector('.reader-identity')).display,
      reading: getComputedStyle(document.querySelector('#reader-document')).display,
      compareColumns: document.querySelector('.compare-pair') &&
        getComputedStyle(document.querySelector('.compare-pair')).gridTemplateColumns
    }))()`);
    assert.equal(printed.controls, 'none');
    assert.equal(printed.dialog, 'none');
    assert.notEqual(printed.title, 'none');
    assert.notEqual(printed.reading, 'none');
    if (state.requestedMode === 'compare') {
      assert.equal(printed.compareColumns.split(' ').filter(Boolean).length, 2,
        'printed Compare keeps both semantic sides aligned');
    }
    const pdf = await cdp.send('Page.printToPDF', {
      printBackground: true, preferCSSPageSize: true
    });
    assert.ok(pdf.data.length > 10000, 'the selected reader generates a PDF');
    const pdfFile = resolve(profile, entrance + '-' + state.requestedMode + '.pdf');
    await writeFile(pdfFile, Buffer.from(pdf.data, 'base64'));
    const { stdout: pdfText } = await execFileAsync('pdftotext', ['-layout', pdfFile, '-'],
      { maxBuffer: 2 * 1024 * 1024 });
    const pages = pdfText.split('\f').filter((page) => page.trim());
    assert.ok(pages.length > 0 && pages.every((page) => page.trim().length > 80),
      'no detached or empty PDF page');
    if (state.requestedMode === 'compare') {
      assert.ok(pages.every((page) => !/^\s*Source records:/.test(page)),
        'a printed source credit cannot begin a page by itself');
    }
    assert.match(pages[0], new RegExp(entrance.toUpperCase() + ' · ' +
      state.requestedMode.toUpperCase()));
    assert.doesNotMatch(pdfText, /Share link|Print dialog opened/);
    if (entrance === 'day') {
      assert.match(pdfText, /Sunday 22 November 2026/);
      if (state.requestedMode === 'compare') {
        assert.match(pdfText, /Territorial context: universal/);
        assert.match(pdfText, /Calendar results on this date/);
      } else assert.match(pdfText, /Calendar result/);
    } else {
      assert.match(pdfText, /First Sunday of Advent/);
      assert.match(pdfText, /advent-1/);
    }
    if (state.requestedMode === 'study') {
      assert.ok(pages.every((page) => !/^Study notes for /.test(page.trimStart().split('\n')[0])),
        'a Study note cannot begin a page without its reading tail');
      assert.ok(expectedPrint.studyNotes > 0);
      assert.equal((pdfText.match(/Study notes for /g) || []).length,
        expectedPrint.studyNotes);
      assert.equal((pdfText.match(/Source record/g) || []).length,
        expectedPrint.studySources);
      assert.match(pdfText, /Coverage/);
    } else {
      assert.ok(expectedPrint.compareSources > 0);
      assert.equal((pdfText.match(/Source records:/g) || []).length,
        expectedPrint.compareSources);
      assert.match(pdfText, /Compare corresponding Propers/);
      assert.match(pdfText, /Entrance antiphon/);
      assert.match(pages.at(-1), /Prayer after Communion/);
    }
    await cdp.send('Emulation.setEmulatedMedia', { media: 'screen' });
    await evaluate(cdp, `document.querySelector('[data-reader-details]').replaceChildren(
      document.createElement('p'))`);
    await waitFor(cdp, `document.querySelector('[data-reader-details]').firstElementChild?.
      hasAttribute('data-reader-share-print')`, 'Details reinsertion');
  }

  async function checkMissalPagination() {
    const route = base + DAY + '?data=/src/web/data' +
      '#date=2026-05-24&missal=roman-1962&bible=douay-rheims&orations=la' +
      '&mass=pentecost&mode=missal&ordinary=1&ordinary-lang=en&rubrics=1&why=0';
    await cdp.send('Page.navigate', { url: route });
    await waitFor(cdp, 'window.dayReaderDebug?.ready && dayReaderDebug.outcome !== "loading"',
      'long Day Missal');
    assert.equal(await evaluate(cdp, 'dayReaderDebug.outcome'), 'ready');
    const before = await evaluate(cdp, `(() => ({
      ids: [...document.querySelectorAll('#reader-document [data-semantic-event-id]')]
        .map((node) => node.dataset.semanticEventId),
      html: document.querySelector('#reader-document').innerHTML
    }))()`);
    assert.ok(before.ids.length > 150);
    await cdp.send('Emulation.setEmulatedMedia', { media: 'print' });
    const lifecycle = await evaluate(cdp, `(() => {
      const reading = document.querySelector('#reader-document');
      window.dispatchEvent(new Event('beforeprint'));
      const first = reading.querySelectorAll('.ordinary-print-tie').length;
      window.dispatchEvent(new Event('beforeprint'));
      const repeated = reading.querySelectorAll('.ordinary-print-tie').length;
      window.dispatchEvent(new Event('afterprint'));
      return { first, repeated, restored: reading.innerHTML === ${JSON.stringify(before.html)} };
    })()`);
    assert.ok(lifecycle.first > 0);
    assert.equal(lifecycle.repeated, lifecycle.first);
    assert.equal(lifecycle.restored, true);
    const pdf = await cdp.send('Page.printToPDF', {
      printBackground: true, preferCSSPageSize: true
    });
    const pdfFile = resolve(profile, 'day-missal-composition.pdf');
    await writeFile(pdfFile, Buffer.from(pdf.data, 'base64'));
    const { stdout } = await execFileAsync('pdftotext', ['-layout', pdfFile, '-'],
      { maxBuffer: 2 * 1024 * 1024 });
    const pages = stdout.split('\f').filter((page) => page.trim());
    assert.ok(pages.length > 15 && pages.every((page) => page.trim().length > 80));
    for (const [direction, continuation] of [
      ['Turning towards the people, the Priest salutes them, saying,', 'Dominus vobiscum'],
      ['When the Priest puts the Wine and Water into the Chalice, he says,',
        'Deus qui humanae substantiae dignitatem'],
      ['Bowing before the middle of the Altar, he says,',
        'Suscipe sancta Trinitas hanc oblationem'],
      ['Taking the Host in his Hands, he says,', 'Panem cœlestem accipiam'],
      ['THE CANON OF THE MASS.', 'Te igitur, clementissime Pater']
    ]) {
      assert.ok(pages.some((page) => {
        const at = page.indexOf(direction);
        return at >= 0 && page.slice(at).includes(continuation);
      }), direction + ' must share a page with its following Ordinary text');
    }
    const after = await evaluate(cdp, `(() => ({
      ids: [...document.querySelectorAll('#reader-document [data-semantic-event-id]')]
        .map((node) => node.dataset.semanticEventId),
      html: document.querySelector('#reader-document').innerHTML,
      wrappers: document.querySelectorAll('#reader-document .ordinary-print-tie').length
    }))()`);
    assert.deepEqual(after.ids, before.ids);
    assert.equal(after.html, before.html);
    assert.equal(after.wrappers, 0);
    await cdp.send('Emulation.setEmulatedMedia', { media: 'screen' });
  }

  async function captureSemanticPrint(entrance, hash, label) {
    const path = entrance === 'day' ? DAY : PROPERS;
    await cdp.send('Page.navigate', { url: 'about:blank' });
    await cdp.send('Page.navigate', { url: base + path + '?data=/src/web/data' + hash });
    await waitFor(cdp, `window.${entrance}ReaderDebug?.ready &&
      window.${entrance}ReaderDebug.outcome !== 'loading' &&
      document.querySelector('#reader-document')?.getAttribute('aria-busy') === 'false'`, label);
    assert.equal(await evaluate(cdp, `${entrance}ReaderDebug.outcome`), 'ready');
    await cdp.send('Emulation.setDeviceMetricsOverride', {
      width:1440,height:900,deviceScaleFactor:1,mobile:false
    });
    try {
      await cdp.send('Emulation.setEmulatedMedia', { media: 'print' });
      await evaluate(cdp, `document.fonts.ready.then(() => new Promise(resolve =>
        requestAnimationFrame(() => requestAnimationFrame(resolve))))`);
      const marks = '.ordinary-print-tie,.study-print-tie,.print-keep-short-body,' +
        '.print-keep-short-psalm';
      const snapshot = () => evaluate(cdp, `(() => {
        const d=document.querySelector('#reader-document'),debug=window.${entrance}ReaderDebug;
        return {url:location.href,html:d.innerHTML,text:d.textContent,state:debug.state,
          ids:[...d.querySelectorAll('[data-semantic-event-id]')].map(n=>n.dataset.semanticEventId),
          semanticIds:(debug.semantic?.events||[]).map(event=>event.id),
          ordinary:${JSON.stringify(entrance === 'day' ? SHORT_ORDINARY_PRINT : [])}.map(([key])=>{
            const id='ordinary-element/praeparatio/'+key;
            const n=[...d.querySelectorAll('[data-semantic-event-id]')].find(n=>n.dataset.semanticEventId===id);
            const note=n?.querySelector(':scope > .study-event');
            const pair=n?.querySelector(':scope > .text-pair');
            const fact=label=>[...note?.querySelectorAll('.study-facts > dt')||[]]
              .find(dt=>dt.textContent===label)?.nextElementSibling?.textContent||null;
            const selected=debug.semantic?.events.find(event=>event.id===id)?.selected;
            return {id,exists:Boolean(n),noteId:note?.dataset.studyEventId||null,
              noteLast:Boolean(note&&n.lastElementChild===note),
              noteLanguage:fact('Language'),noteSourceId:fact('Witness'),
              noteRelation:fact('Witness relation'),noteCollation:fact('Collation'),
              selected:selected&&{language:selected.language,sourceId:selected.sourceId,
                relation:selected.relation,collation:selected.collation},
              sides:[...pair?.querySelectorAll(':scope > .text-side')||[]].map(side=>{
                const body=side.querySelector(':scope > .text-side-body');
                const spoken=[...body?.querySelectorAll('.ordinary-turn-text')||[]].at(-1)||
                  body?.querySelector(':scope > .composed,:scope > .ordinary-head');
                return {lang:side.dataset.textLanguage,held:side.dataset.textAvailability==='held',
                  sourceId:side.dataset.textSourceId||null,
                  label:side.querySelector(':scope > .text-side-label')?.textContent||'',
                  tail:(spoken?.textContent||'').trim().split(/\\s+/).slice(-12).join(' '),
                  credit:side.querySelector(':scope > .composed-note')?.textContent||''};
              })};
          })};
      })()`);
      const before = await snapshot();
      const lifecycle = await evaluate(cdp, `(() => {
        const d=document.querySelector('#reader-document'),before=d.innerHTML;
        const marked=()=>[...d.querySelectorAll(${JSON.stringify(marks)})].map(n=>({
          classes:n.className,id:n.dataset.semanticEventId||null}));
        dispatchEvent(new Event('beforeprint'));const first=marked();
        dispatchEvent(new Event('beforeprint'));const repeated=marked();
        dispatchEvent(new Event('afterprint'));
        return {first,repeated,restored:d.innerHTML===before,remaining:marked().length};
      })()`);
      assert.deepEqual(lifecycle.first, lifecycle.repeated, 'beforeprint is idempotent');
      assert.equal(lifecycle.restored, true, 'manual lifecycle restores exact reader DOM');
      assert.equal(lifecycle.remaining, 0);
      const pdf = await cdp.send('Page.printToPDF', {
        printBackground:true,preferCSSPageSize:true
      });
      const pdfFile = resolve(SCRATCH, label + '.pdf');
      await writeFile(pdfFile, Buffer.from(pdf.data, 'base64'));
      await waitFor(cdp, `!document.querySelector('#reader-document')?.querySelector(
        ${JSON.stringify(marks)})`, label + ' afterprint cleanup');
      assert.deepEqual(await snapshot(), before,
        'actual PDF printing restores exact DOM, ordered source events, text and selected state');
      const extract = async option => (await execFileAsync('pdftotext',
        [option,pdfFile,'-'], {maxBuffer:4 * 1024 * 1024})).stdout;
      const [layout,bbox] = await Promise.all(['-layout','-bbox'].map(extract));
      return {before,pages:pdfPages(layout),bbox};
    } finally {
      await cdp.send('Emulation.setEmulatedMedia', { media: 'screen' });
      await cdp.send('Emulation.clearDeviceMetricsOverride');
    }
  }

  activeCase = 'day-compare-share-print';
  await check('day', '#date=2026-11-22&missal=roman-1962&bible=douay-rheims&orations=la' +
    '&mode=compare&compare=recension&peer-missal=postconciliar&territory=universal&ordinary=0');
  assertions.push({ name: activeCase, status: 'pass' });
  activeCase = 'propers-study-share-print';
  await check('propers', '#missal=roman-1962&type=seasonal&mass=advent-1' +
    '&bible=douay-rheims&orations=la&mode=study');
  assertions.push({ name: activeCase, status: 'pass' });
  activeCase = 'day-study-print-composition';
  await check('day', '#date=2026-11-22&missal=roman-1962&bible=douay-rheims&orations=la' +
    '&mode=study&ordinary=0');
  assertions.push({ name: activeCase, status: 'pass' });
  activeCase = 'propers-compare-print-composition';
  await check('propers', '#missal=roman-1962&type=seasonal&mass=advent-1' +
    '&bible=douay-rheims&orations=la&mode=compare&compare=oration-language&peer-orations=en');
  assertions.push({ name: activeCase, status: 'pass' });
  activeCase = 'day-missal-print-pagination';
  await checkMissalPagination();
  assertions.push({ name: activeCase, status: 'pass' });
  activeCase = 'propers-reading-alternative-pdf-seams';
  const alternativePrint = await captureSemanticPrint('propers',
    '#missal=postconciliar&type=christological&mass=presentation-lord&bible=douay-rheims' +
    '&orations=la&mode=compare&compare=reading-alternative' +
    '&alternative=proper-choice%2Fpostconciliar%2Fpresentation-lord%2Fmain%2Fgospel%2Flonger' +
    '&peer-alternative=proper-choice%2Fpostconciliar%2Fpresentation-lord%2Fmain%2Fgospel%2Fshorter' +
    '&location=compare%2Fproper%2Fgospel', activeCase);
  assert.equal(alternativePrint.before.state.comparison.dimension, 'reading-alternative');
  assert.deepEqual(alternativePrint.before.ids, ['reading-1','responsorial-psalm','reading-2',
    'gospel-acclamation','gospel'].map(id => 'compare/proper/' + id));
  const alternativeProof = assertAlternativePdf(alternativePrint.pages, alternativePrint.bbox);
  assertions.push({ name: activeCase, status: 'pass', pdf:alternativeProof });

  activeCase = 'day-paired-study-ordinary-pdf-seams';
  const ordinaryPrint = await captureSemanticPrint('day',
    '#date=2026-05-24&missal=roman-1962&bible=douay-rheims&orations=en&mass=pentecost' +
    '&mode=study&ordinary=1&ordinary-lang=en&text-display=latin-and-selected', activeCase);
  assert.equal(ordinaryPrint.before.state.requestedMode, 'study');
  assert.equal(ordinaryPrint.before.state.textDisplay, 'latin-and-selected');
  assert.deepEqual(ordinaryPrint.before.ids, ordinaryPrint.before.semanticIds,
    'paired Study keeps the exact source event sequence');
  assert.ok(ordinaryPrint.before.ids.length > 150);
  const ordinaryProof = assertShortOrdinaryPdf(ordinaryPrint.pages,
    ordinaryPrint.bbox, ordinaryPrint.before.ordinary);
  assertions.push({ name: activeCase, status: 'pass', pdf:ordinaryProof });
} catch (error) {
  const detail = error && error.stack || String(error);
  assertions.push({ name: activeCase, status: 'fail', detail });
  failures.push({ name: activeCase, detail });
} finally {
  if (cdp) cdp.close();
  chrome.kill('SIGTERM');
  if (chrome.exitCode === null && chrome.signalCode === null) {
    await new Promise((done) => chrome.once('exit', done));
  }
  await instance.close();
  await rm(profile, { recursive: true, force: true });
}
const unexpectedFailedRequests = failedRequests.filter((one) => !one.canceled);
const clean = failures.length === 0 && consoleProblems.length === 0 &&
  unexpectedFailedRequests.length === 0 && httpProblems.length === 0;
process.stdout.write(JSON.stringify({ status: clean ? 'pass' : 'fail',
  checks: assertions.filter((one) => one.status === 'pass').length,
  assertions, failures, consoleProblems, failedRequests, httpProblems }) + '\n');
if (!clean) process.exitCode = 1;
