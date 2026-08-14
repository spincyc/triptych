/* Real-Chromium evidence for the V5 malformed-data correction.
 *
 * WHY THIS EXISTS, AND WHY IT IS NOT A SCREENSHOT TOOL.
 *
 * The V4.1 independent review proved its first blocker by replaying an
 * Everything-held page in real Chromium and reading `lang="[object Object]"`
 * off the fragment text. A PICTURE CANNOT SHOW THAT. A DOM language attribute
 * is invisible: it changes what a screen reader says, what font is chosen and
 * how the text hyphenates, and none of that appears in a PNG. Screenshots are
 * the wrong instrument for four of the five blocking classes, and offering
 * them as evidence would be offering evidence that cannot bear on the claim.
 *
 * So this reads the DOM instead, in the same browser, and prints what it read.
 * Run it against the V4.1 build and against the V5 build and the two reports
 * are a before/after of the exact facts the review named.
 *
 * IT SERVES A FIXTURE SITE ROOT, AND THAT IS THE POINT AND THE CAVEAT.
 * `capture-catena.mjs`, carried forward from V4.1, visits only real corpus
 * addresses and says so proudly: "Nothing is fabricated for the picture."
 * That is right for evidencing real holdings and useless for evidencing
 * malformed-data behaviour, because the corpus holds no malformed data. The
 * fixtures below ARE fabricated, deliberately, and the package says so in
 * those words. They are adversarial test data and represent no holding of
 * this project.
 *
 *   node probe-catena.mjs <site-root> <out.json> <label>
 *
 * <site-root> is a built site; this tool copies nothing and writes nothing
 * into it. The fixtures are injected in the response path of its own static
 * server, so the built artifact on disk is never modified.
 */

import { readFile, writeFile } from 'node:fs/promises';
import { createServer } from 'node:http';
import { spawn } from 'node:child_process';
import { join, normalize } from 'node:path';

const [ROOT, OUT, LABEL, SHOTS, PREFIX] = process.argv.slice(2);
if (!ROOT || !OUT || !LABEL) {
  console.error('usage: probe-catena.mjs <site-root> <out.json> <label> [shot-dir] [prefix]');
  process.exit(2);
}

/* The viewports a picture is taken at, when one is taken at all. A screenshot
 * is offered ONLY for the states whose rendering visibly differs; for the
 * rest the DOM report above is the evidence, because the difference is in an
 * attribute or a request and a picture cannot carry it. */
const VIEWPORTS = [[1440, 900], [393, 852]];

const CHROME = process.env.TRIPTYCH_CHROME || '/usr/bin/chromium';
const PORT = 9200 + (process.pid % 300);

/* ---------------------------------------------------------------- fixtures
 * Each one varies ONE class of the review's five, against an otherwise sound
 * chapter, so a difference in the report is attributable to that class.
 */

const source = (n, over) => Object.assign({
  author: 'Author ' + n, work: 'Work ' + n, work_id: 'probe.work' + n,
  date: 300 + n, language: 'la', voice: 'original', rights: 'public-domain',
  edition: 'Edition ' + n, edition_published: '1900', translators: [],
  container: ''
}, over || {});

const fragment = (n, over) => Object.assign({
  id: 'probe-' + n, locator: String(n), source: String(n), review: 'verified',
  text_words: 4,
  extent: { token: 'Gen', first_chapter: 1, first_verse: n,
            last_chapter: 1, last_verse: n }
}, over || {});

const CHAPTER = 'structure/catena/01-gen/001.json';
const INDEX = 'structure/catena/index.json';

// 1. Language metadata that is not a language, under Everything held — the
//    review's own replay condition.
const MALFORMED_LANGUAGE = {
  token: 'Gen', chapter: 1, text_prefix: 'structure/catena/text/',
  sources: {
    1: source(1, { language: 'la' }),
    2: source(2, { language: { code: 'la' } }),
    3: source(3, { language: ['la'] }),
    4: source(4, { language: 42 }),
    5: source(5, { language: true }),
    6: source(6, { language: '   ' }),
    7: source(7, { language: 'not a language code' })
  },
  fragments: [1, 2, 3, 4, 5, 6, 7].map((n) => fragment(n)),
  leads: [], blocked: [], refusals: {}
};

// 2. A valid member, a malformed record, a scalar, a null, a valid member —
//    in every collection at once, including the refusal list.
const MIXED_MEMBERS = {
  token: 'Gen', chapter: 1, text_prefix: 'structure/catena/text/',
  sources: { 1: source(1), 5: source(5) },
  fragments: [fragment(1, { id: 'probe-first' }), fragment(2, { source: '1' }),
              7, null, fragment(5, { id: 'probe-last' })],
  leads: [{ author: 'Lead One', title: 'Lead Work One', date: '500' },
          { author: { n: 1 }, title: ['x'], date: {} }, 13, null,
          { author: 'Lead Two', title: 'Lead Work Two', date: '600' }],
  blocked: [{ author: 'Blocked One', work: 'Blocked Work One', reason: 'rights' },
            { author: 5, work: [], reason: {} }, 21, null,
            { author: 'Blocked Two', work: 'Blocked Work Two', reason: 'rights' }],
  refusals: { 'douay-rheims': [null, 4, 'not a record'] }
};

// 3. Absence rows: a valid typed finding, a malformed finding, a valid
//    finding beside malformed siblings, `not-surveyed`, and a list mixing a
//    malformed member with a valid typed absence.
const TYPED_ABSENCE = {
  token: 'Gen', chapter: 1, text_prefix: 'structure/catena/text/',
  sources: { 1: source(1), 2: source(2), 3: source(3), 4: source(4), 5: source(5) },
  fragments: [1, 2, 3, 4, 5].map((n) => fragment(n)),
  leads: [], blocked: [], refusals: {}
};
const TYPED_ABSENCE_ROWS = {
  'probe.work1': [{ language: 'en', finding: 'none-published',
                    reason: 'No English translation has been published.' }],
  'probe.work2': [{ language: 'en', finding: { kind: 'in-copyright' },
                    reason: 'A reason that outlives its finding.' }],
  'probe.work3': [{ language: 'en', finding: 'in-copyright',
                    reason: ['not', 'text'], partial: 3 }],
  'probe.work4': [{ language: 'en', finding: 'not-surveyed', reason: '' }],
  'probe.work5': [null, 11, 'not a record',
                  { language: 'en', finding: 'partial-public-domain',
                    reason: 'Only part of it is out of copyright.',
                    partial: 'the 1893 selection' }]
};

// 4. Numbers that are not numbers, and a held path that is not text.
const MALFORMED_NUMBERS = {
  token: 'Gen', chapter: 1, text_prefix: 'structure/catena/text/',
  sources: { 1: source(1), 2: source(2), 3: source(3), 4: source(4) },
  fragments: [fragment(1, { text_words: 1200 }), fragment(2, { text_words: '1200' }),
              fragment(3, { text_words: true }), fragment(4, { text_words: 12.5 })],
  leads: [], blocked: [], refusals: {}
};

const BROKEN_HELD_INDEX = (real) => Object.assign({}, real, {
  held: [{ token: 'Gen', path: { at: 'somewhere' }, present: [1] }]
});

// 5. A canon whose members are not books — the bootstrap record, malformed.
const BROKEN_CANON_INDEX = (real) => Object.assign({}, real, {
  canon: [null, 7, 'Gen', { token: 'Gen' }]
});

const GEN1 = '#book=Gen&chapter=1&bible=douay-rheims';

const PROBES = [
  { name: 'malformed-language-everything-held', hash: GEN1,
    files: { [CHAPTER]: MALFORMED_LANGUAGE },
    shows: 'blocker 1 — a DOM lang attribute composed from a record',
    picture: 'the visible language chip: a value that is not a language code no longer names one' },
  { name: 'mixed-collection-members', hash: GEN1,
    files: { [CHAPTER]: MIXED_MEMBERS },
    shows: 'blocker 2 — counts, refusals and surviving siblings',
    picture: 'a null member replaced the whole page with a JavaScript error; the valid siblings now stand' },
  { name: 'typed-absence-findings', hash: GEN1 + '&voice=translation:en',
    files: { [CHAPTER]: TYPED_ABSENCE }, absences: TYPED_ABSENCE_ROWS,
    shows: 'blocker 3 — what each typed finding licenses the page to say',
    picture: 'the absence summary: a manufactured closed negative replaced by what each finding supports' },
  { name: 'malformed-word-tallies', hash: GEN1,
    files: { [CHAPTER]: MALFORMED_NUMBERS },
    shows: 'blocker 4 — a tally is a number the record wrote',
    picture: 'the word-count chips: "1 words" for a boolean and "12.5 words" for a fraction are gone' },
  { name: 'malformed-held-path', hash: GEN1, index: BROKEN_HELD_INDEX,
    shows: 'blocker 4 — a path that is not text is not fetched' },
  { name: 'malformed-canon-bootstrap', hash: '', index: BROKEN_CANON_INDEX,
    shows: 'blocker 4 — the bootstrap record, and the terminal state it owes',
    picture: 'the page stood at "Loading…" for ever; it now settles and says what failed' }
];

/* ------------------------------------------------------------------ server */

const MIME = { '.html': 'text/html; charset=utf-8', '.js': 'text/javascript',
               '.css': 'text/css', '.json': 'application/json',
               '.svg': 'image/svg+xml', '.png': 'image/png',
               '.woff2': 'font/woff2', '.ico': 'image/x-icon' };

let active = null;

function serve(root) {
  return createServer(async (request, response) => {
    let path = normalize(decodeURIComponent(
      String(request.url).split('#')[0].split('?')[0]));
    if (path.endsWith('/')) path += 'index.html';
    const relative = path.replace(/^\/+/, '');
    // THE FIXTURE IS INJECTED HERE, in the response, so the built artifact on
    // disk is never modified and the next probe sees it pristine.
    if (active) {
      const key = relative.replace(/^browse\//, '');
      if (active.files && Object.prototype.hasOwnProperty.call(active.files, key)) {
        response.writeHead(200, { 'content-type': 'application/json' });
        return response.end(JSON.stringify(active.files[key]));
      }
      if (active.index && key === INDEX) {
        try {
          const real = JSON.parse(
            await readFile(join(root, 'browse', INDEX), 'utf8'));
          response.writeHead(200, { 'content-type': 'application/json' });
          return response.end(JSON.stringify(active.index(real)));
        } catch (error) { /* fall through to the real file */ }
      }
      if (active.absences && key === INDEX) {
        try {
          const real = JSON.parse(
            await readFile(join(root, 'browse', INDEX), 'utf8'));
          real.absences = Object.assign({}, real.absences, active.absences);
          response.writeHead(200, { 'content-type': 'application/json' });
          return response.end(JSON.stringify(real));
        } catch (error) { /* fall through */ }
      }
    }
    try {
      const body = await readFile(join(root, relative));
      const dot = relative.lastIndexOf('.');
      response.writeHead(200, {
        'content-type': MIME[relative.slice(dot)] || 'application/octet-stream' });
      response.end(body);
    } catch (error) {
      response.writeHead(404, { 'content-type': 'text/plain' });
      response.end('not found');
    }
  });
}

/* --------------------------------------------------------------------- CDP */

let nextId = 1;
const pending = new Map();

/* The browser endpoint carries no `Page` domain: a target must be created and
 * attached to first, exactly as `capture-catena.mjs` does. Every call below
 * therefore rides a sessionId. */
function send(socket, method, params, sessionId) {
  const id = nextId += 1;
  socket.send(JSON.stringify({ id, method, params: params || {}, sessionId }));
  return new Promise((resolve, reject) => pending.set(id, { resolve, reject }));
}

async function main() {
  const server = serve(ROOT);
  await new Promise((resolve) => server.listen(0, '127.0.0.1', resolve));
  const origin = 'http://127.0.0.1:' + server.address().port;

  const chrome = spawn(CHROME, [
    '--headless=new', '--no-sandbox', '--disable-gpu', '--disable-dev-shm-usage',
    '--hide-scrollbars', '--force-device-scale-factor=1',
    '--remote-debugging-port=' + PORT, 'about:blank'
  ], { stdio: 'ignore' });

  let version = null;
  for (let tries = 0; tries < 100 && !version; tries += 1) {
    await new Promise((wait) => setTimeout(wait, 100));
    try {
      const answer = await fetch('http://127.0.0.1:' + PORT + '/json/version');
      version = await answer.json();
    } catch (error) { /* not up yet */ }
  }
  if (!version) throw new Error('Chromium did not expose a DevTools endpoint');

  const socket = new WebSocket(version.webSocketDebuggerUrl);
  await new Promise((resolve, reject) => {
    socket.addEventListener('open', resolve);
    socket.addEventListener('error', reject);
  });
  socket.addEventListener('message', (event) => {
    const message = JSON.parse(event.data);
    const waiting = pending.get(message.id);
    if (!waiting) return;
    pending.delete(message.id);
    if (message.error) waiting.reject(new Error(JSON.stringify(message.error)));
    else waiting.resolve(message.result);
  });

  const { targetId } = await send(socket, 'Target.createTarget', { url: 'about:blank' });
  const { sessionId } = await send(socket, 'Target.attachToTarget',
                                   { targetId, flatten: true });
  const call = (method, params) => send(socket, method, params, sessionId);

  await call('Page.enable');
  await call('Runtime.enable');
  await call('Emulation.setDeviceMetricsOverride',
             { width: 1440, height: 900, deviceScaleFactor: 1, mobile: false });

  // WHAT IS READ, AND WHY EACH ONE. Every field below is a fact the V4.1
  // review named, read off the live DOM rather than inferred from a picture.
  const READ = `(() => {
    const reading = document.getElementById('reading');
    const text = (node) => (node ? node.textContent.trim() : null);
    const all = (selector) => Array.from(document.querySelectorAll(selector));
    return {
      hash: location.hash,
      reference: text(document.getElementById('reference')),
      tally: text(document.getElementById('tally')),
      status: text(document.getElementById('reading-status')),
      ariaBusy: reading ? reading.getAttribute('aria-busy') : null,
      // THE BLOCKER-1 FACT. Read as the ATTRIBUTE, not the property.
      langAttributes: all('#reading [lang]').map(
        (one) => (one.className || one.localName) + '=' + one.getAttribute('lang')),
      languageChips: all('.fragment-language').map(text),
      fragmentCount: all('.fragment').length,
      wordChips: all('.fragment-length').map(text),
      extents: all('.fragment-extent').map(text),
      leads: all('.lead').map(text),
      blocked: all('.blocked').map(text),
      refusal: text(document.querySelector('.refusal')),
      absenceSummary: text(document.querySelector('.absence-note summary')),
      absenceReasons: all('.absence-reason').map(text),
      absencePartials: all('.absence-partial').map(text),
      asideNotes: all('.aside-note').map(text),
      errorHeadings: all('.catena-error .section-heading').map(text),
      bookOptions: all('#book-select option').slice(0, 3).map(text),
      dataStates: Array.from(new Set(all('#reading [data-state]').map(
        (one) => one.getAttribute('data-state')))).sort(),
      // EVERY REQUEST THE PAGE ACTUALLY MADE, so "a malformed path is never
      // fetched" is evidenced rather than asserted. Two pages can reach the
      // same visible state and differ entirely in what they asked the network
      // for, and a URL built by coercion is a request against nothing.
      // No regex literal here on purpose: this expression is carried inside a
      // template literal, and its backslash escapes are eaten before the page
      // ever sees them, which silently broke the whole probe once.
      requested: performance.getEntriesByType('resource')
        .map((one) => one.name.split('/').slice(3).join('/'))
        .filter((one) => one.endsWith('.json')).sort()
    };
  })()`;

  const report = { label: LABEL, browser: version.Browser, probes: {} };

  for (const probe of PROBES) {
    active = probe;
    await call('Page.navigate', { url: origin + '/catena/index.html' });
    await new Promise((wait) => setTimeout(wait, 300));
    // A fresh navigation per probe, then the address, so the cold-arrival
    // path is the one under test.
    await call('Runtime.evaluate', {
      expression: 'location.hash = ' + JSON.stringify(probe.hash) + ';' });
    await new Promise((wait) => setTimeout(wait, 1600));
    for (let tries = 0; tries < 40; tries += 1) {
      const settled = await call('Runtime.evaluate', {
        expression: "document.querySelector('#reading')?.getAttribute('aria-busy') !== 'true'",
        returnByValue: true });
      if (settled.result.value) break;
      await new Promise((wait) => setTimeout(wait, 100));
    }
    const seen = await call('Runtime.evaluate',
                            { expression: READ, returnByValue: true });
    report.probes[probe.name] = Object.assign(
      { shows: probe.shows, address: probe.hash || '(no address)' },
      seen.result.value);
  }

  if (SHOTS) {
    const shots = [];
    for (const probe of PROBES.filter((one) => one.picture)) {
      active = probe;
      for (const [width, height] of VIEWPORTS) {
        await call('Emulation.setDeviceMetricsOverride',
                   { width, height, deviceScaleFactor: 1, mobile: false });
        await call('Page.navigate', { url: origin + '/catena/index.html' });
        await new Promise((wait) => setTimeout(wait, 300));
        await call('Runtime.evaluate', {
          expression: 'location.hash = ' + JSON.stringify(probe.hash) + ';' });
        await new Promise((wait) => setTimeout(wait, 1600));
        for (let tries = 0; tries < 40; tries += 1) {
          const settled = await call('Runtime.evaluate', {
            expression: "document.querySelector('#reading')?.getAttribute('aria-busy') !== 'true'",
            returnByValue: true });
          if (settled.result.value) break;
          await new Promise((wait) => setTimeout(wait, 100));
        }
        const shot = await call('Page.captureScreenshot',
                                { format: 'png', captureBeyondViewport: false });
        const file = (PREFIX || 'after--') + 'catena--' + probe.name +
                     '--' + width + 'x' + height + '.png';
        const bytes = Buffer.from(shot.data, 'base64');
        await writeFile(join(SHOTS, file), bytes);
        shots.push({ file, state: probe.name, address: probe.hash || '(no address)',
                     viewport: width + 'x' + height, variant: 'default',
                     media: 'screen', shows: probe.picture, bytes: bytes.length });
      }
    }
    await writeFile(join(SHOTS, (PREFIX || 'after--') + 'probe-index.json'),
                    JSON.stringify(shots, null, 2) + '\n');
    report.screenshots = shots.length;
  }

  await writeFile(OUT, JSON.stringify(report, null, 2) + '\n');
  socket.close();
  chrome.kill();
  server.close();
  console.log('probed ' + PROBES.length + ' states at ' + LABEL + ' -> ' + OUT);
  process.exit(0);
}

main().catch((error) => {
  console.error('PROBE FAILED: ' + (error && error.stack || error));
  process.exit(1);
});
