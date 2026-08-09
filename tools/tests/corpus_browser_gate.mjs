#!/usr/bin/env node

/* Design-neutral page gate over the built public artifact, driven by real Chromium.
 *
 * Every other browser harness in this directory drives the repository copies under
 * `src/web/browser/`. The artifact a reader receives is not those files: the build
 * re-wraps each page in `release/public-alpha/layout.html`, so a defect introduced
 * at publication time — a second `<main>`, a stripped skip link, a doubled title
 * suffix — is invisible to every existing test. This gate serves
 * `build/public-alpha/site` and asserts only facts that are true or false
 * independently of how the site looks. There is no visual contract yet, so nothing
 * here measures colour, spacing, typography, layout or composition; inventing such
 * a measurement would freeze a design that has not been decided.
 *
 * The run has five phases. The first drives every route through the governing
 * viewport and emulation matrix. The other four are facts about a route rather
 * than about a screen size, and run once per route: the page with JavaScript
 * switched off, the hash contracts a shared link depends on, startup under the
 * `/<repository>/` prefix a project site is published at, and whether the page's
 * own links go anywhere.
 *
 * One assertion reads computed style, and only one: a focus indicator is invisible
 * unless something about the element changes when it takes focus, so the gate
 * compares an element with ITSELF unfocused and asserts only that the two differ.
 * It never asserts a value, so it fixes no appearance. See
 * FOCUS_INDICATOR_PROPERTIES.
 */

import { spawn } from 'node:child_process';
import { createServer } from 'node:http';
import { mkdtemp, mkdir, readdir, readFile, writeFile, access } from 'node:fs/promises';
import { constants } from 'node:fs';
import { tmpdir } from 'node:os';
import { extname, join, resolve, sep } from 'node:path';
import process from 'node:process';

const REPO = resolve(import.meta.dirname, '../..');
const ROOT = resolve(process.env.TRIPTYCH_REVIEW_ROOT || join(REPO, 'build/public-alpha/site'));

/* The thirteen pages the artifact serves from `src/web/browser/<entrance>/`. They
 * are listed rather than globbed so a page that stops being published is a visible
 * failure of this gate and not a silently shorter run. */
const INSTRUMENT_ROUTES = [
  '/catena/index.html',
  '/history/index.html',
  '/law/index.html',
  '/liturgy/day-reader.html',
  '/liturgy/day.html',
  '/liturgy/index.html',
  '/liturgy/propers-reader.html',
  '/liturgy/reader-visual-reset-day.html',
  '/liturgy/reader-visual-reset-propers.html',
  '/scripture/index.html',
  '/scripture/track.html',
  '/sources/index.html',
  '/texts/index.html'
];

/* Fixed non-instrument pages, plus one representative page drawn from each of the
 * three generated families. The representative is the lexicographically first page
 * that exists, so the sample is stable across runs without being pinned to a title
 * that may be renamed. */
const FIXED_SAMPLE_ROUTES = ['/404.html', '/about.html', '/index.html'];
const SAMPLED_FAMILIES = [
  { name: 'library', directory: 'library', recursive: false },
  { name: 'docs', directory: 'docs', recursive: false },
  { name: 'web', directory: 'web', recursive: true }
];

/* The governing screenshot/state matrix: five viewports, plus the four
 * accessibility derivatives of the handset. Changing a number here changes what
 * the project means by "supported", so the five base sizes are written out rather
 * than generated. */
const STATES = [
  { name: 'desktop-1440x900', width: 1440, height: 900 },
  { name: 'laptop-1024x768', width: 1024, height: 768 },
  { name: 'tablet-768x1024', width: 768, height: 1024 },
  { name: 'handset-393x852', width: 393, height: 852 },
  { name: 'narrow-320x852', width: 320, height: 852 },
  { name: 'handset-393x852-text-200', width: 393, height: 852, textScale: 2 },
  { name: 'handset-393x852-scale-400', width: 393, height: 852, pageScale: 4 },
  {
    name: 'handset-393x852-forced-colors',
    width: 393,
    height: 852,
    media: [{ name: 'forced-colors', value: 'active' }]
  },
  {
    name: 'handset-393x852-reduced-motion',
    width: 393,
    height: 852,
    media: [{ name: 'prefers-reduced-motion', value: 'reduce' }]
  }
];

/* ------------------------------------------------------------------ hash table
 *
 * THE ONE PLACE A ROUTER CHANGE HAS TO BE UPDATED.
 *
 * Each entry is a deep link a reader could have been sent, written in the keys the
 * page's own instrument reads. The keys were read off the built JavaScript:
 *
 *   /catena/index.html            catena.js writeHash: book, chapter, bible, voice
 *   /history/index.html           history.js writeHash: station, unit
 *   /law/index.html               law.js writeState: canon, par, line, act
 *   /liturgy/index.html           liturgy.js writeHash: missal, type, mass, bible,
 *                                 orations
 *   /liturgy/day.html             day.js writeHash: date, missal, bible, orations,
 *                                 why, ordinary, ordinary-lang, rubrics, mass, and
 *                                 one key per variant group
 *   /liturgy/day-reader.html      reader-state.js DAY_KEYS
 *   /liturgy/propers-reader.html  reader-state.js PROPERS_KEYS
 *   /scripture/track.html         track.js hashPairs: tier, reading|period, bible
 *   /sources/index.html           sources.js applyHash: edition, passage
 *   /texts/index.html             texts.js restore: author, edition, section,
 *                                 reading, sort, find
 *
 * `/scripture/index.html` is deliberately absent: plan.js forwards a legacy
 * `#tier=`/`#reading=`/`#period=` hash to `track.html` with `location.replace`, so
 * its hash contract is a redirect and asserting the hash survives would assert the
 * opposite of the intended behaviour.
 *
 * The assertion is that a stated selection survives arrival: every key and value
 * given here must still be in `location.hash` once the page has settled. A page
 * completing the hash with the rest of its state is normal and allowed; a page
 * dropping or rewriting what the reader asked for is the defect. */
const HASH_DEEP_LINKS = [
  /* `voice` is here because it was the key that did not survive. The page
   * assigned it to `#language-select` at startup, before the chapter file had
   * arrived and therefore before that control held any option but "Everything
   * held"; the assignment was dropped, the empty value was skipped by
   * `writeHash`, and the reader's own link was rewritten without it. Genesis 1
   * holds commentary in its authors' own languages, so `voice=original` is a
   * selection that chapter can honour, and this line fails if the deferral in
   * `catena.js` is ever undone. */
  {
    route: '/catena/index.html',
    hash: '#book=Gen&chapter=1&bible=douay-rheims&voice=original'
  },
  { route: '/history/index.html', hash: '#station=praedicatorum-venetiis-1484' },
  { route: '/law/index.html', hash: '#act=latin-missal' },
  { route: '/liturgy/day-reader.html', hash: '#missal=roman-1962&bible=douay-rheims' },
  { route: '/liturgy/day.html', hash: '#missal=roman-1962&bible=douay-rheims' },
  {
    route: '/liturgy/index.html',
    hash: '#missal=roman-1962&type=seasonal&mass=advent-1&bible=douay-rheims'
  },
  {
    route: '/liturgy/propers-reader.html',
    hash: '#missal=roman-1962&type=seasonal&mass=advent-1&bible=douay-rheims'
  },
  { route: '/scripture/track.html', hash: '#tier=landmarks&bible=douay-rheims' },
  {
    route: '/sources/index.html',
    hash: '#edition=edition.abraham-ibn-ezra.perush-al-ha-torah.piotrkow-1907'
  },
  { route: '/texts/index.html', hash: '#sort=title' }
];

/* One CSS pixel. Sub-pixel rounding of a fractional layout width can report a
 * scrollWidth one larger than clientWidth on a page that does not in fact scroll,
 * so a single pixel is forgiven and anything beyond it is reported. */
const OVERFLOW_TOLERANCE_PX = 1;
const CONTROL_SELECTOR =
  'a[href], button, input, select, textarea, [tabindex]:not([tabindex="-1"])';
const TAB_DEPTH = 10;
const SETTLE_TIMEOUT_MS = 9000;

/* GitHub Pages serves a project site under `/<repository>/`, and nothing above it
 * exists. A second server mounted here answers only under the prefix, so a
 * root-relative reference — the one mistake that works perfectly on a local root
 * and 404s on publication — cannot pass. */
const SUBPATH_PREFIX = '/triptych';

/* WCAG 2.2 target size (enhanced) is 44x44 CSS px, and 393px is the handset width
 * of the governing matrix. A link set inline in a sentence is exempt by the
 * standard's own inline exception, so those are counted and reported, never
 * failed. */
const TARGET_SIZE_MIN_PX = 44;
const TARGET_SIZE_WIDTH = 393;
const PROSE_ANCESTORS = 'p, blockquote, figcaption, dd, dt, td, th, li';
const CHROME_ANCESTORS = 'nav, [role="navigation"], header, footer, menu, form';

/* How many tab stops the focus-indicator check samples. The whole tab order would
 * multiply an already long run by the length of the longest page's navigation; the
 * first few stops are where a missing indicator is both most likely and most
 * damaging, and the bound is reported rather than assumed. */
const FOCUS_SAMPLE = 6;

/* The three properties a stylesheet can draw a focus ring with. The gate reads
 * them only to compare an element against ITSELF unfocused: it asserts that the
 * two differ, never that either has some value, so no appearance is fixed here and
 * no design decision is frozen. Pseudo-elements are read too, because a ring drawn
 * on `::after` is a real ring. */
const FOCUS_INDICATOR_PROPERTIES = [
  'outline-style', 'outline-width', 'outline-color', 'outline-offset',
  'box-shadow', 'border-style', 'border-width', 'border-color'
];

/* At most this many distinct link targets are resolved per route. Every route
 * shares one library index and one navigation, so the cap almost never bites; when
 * it does, the count not checked is recorded in the assertion detail AND in the
 * report's `bounds` block, so a truncated check can never be mistaken for a
 * complete one. */
const LINKS_PER_ROUTE_CAP = 40;
const BASE_FONT_SIZES = { standard: 16, fixed: 13 };
const CHROME_CANDIDATES = [
  '/usr/bin/chromium',
  '/usr/bin/chromium-browser',
  '/usr/bin/google-chrome-stable',
  '/usr/bin/google-chrome'
];
const EXIT_NO_BROWSER = 3;

/* AX roles that name a control a reader can operate. `[tabindex]` elements that
 * carry no such role are still checked, because the accessibility tree reports
 * them as focusable. */
const INTERACTIVE_ROLES = new Set([
  'button', 'checkbox', 'combobox', 'link', 'listbox', 'menuitem',
  'menuitemcheckbox', 'menuitemradio', 'option', 'radio', 'searchbox',
  'slider', 'spinbutton', 'switch', 'tab', 'textbox'
]);

function readArgument(flag) {
  const at = process.argv.indexOf(flag);
  return at >= 0 && at + 1 < process.argv.length ? process.argv[at + 1] : null;
}

const captureDirArgument = readArgument('--capture-dir');
const captureDir = captureDirArgument ? resolve(captureDirArgument) : null;
const jsonOutArgument = readArgument('--json-out');
const jsonOut = jsonOutArgument ? resolve(jsonOutArgument) : null;
const routesArgument = readArgument('--routes');

function mime(path) {
  return ({
    '.css': 'text/css; charset=utf-8',
    '.html': 'text/html; charset=utf-8',
    '.js': 'text/javascript; charset=utf-8',
    '.json': 'application/json; charset=utf-8',
    '.png': 'image/png',
    '.jpg': 'image/jpeg',
    '.jpeg': 'image/jpeg',
    '.svg': 'image/svg+xml',
    '.txt': 'text/plain; charset=utf-8',
    '.webp': 'image/webp',
    '.woff2': 'font/woff2',
    '.xml': 'application/xml; charset=utf-8'
  })[extname(path)] || 'application/octet-stream';
}

async function listen(server) {
  await new Promise((accept, reject) => {
    server.once('error', reject);
    server.listen(0, '127.0.0.1', accept);
  });
  return server.address().port;
}

/* The artifact is served exactly as published: a missing file answers 404 and the
 * gate reports it, rather than being papered over with an index fallback.
 *
 * `prefix` mounts the artifact the way GitHub Pages mounts a project site: under
 * `/<repository>/`, with nothing at all above it. Anything addressed outside the
 * prefix answers 404 exactly as the real host would, which is the whole point —
 * a root-relative reference must not be able to resolve.
 *
 * HEAD answers headers and no body, so resolving several hundred link targets does
 * not read several hundred megabytes of PDF off disk. */
function staticServer(prefix = '') {
  return createServer(async (request, response) => {
    try {
      const url = new URL(request.url, 'http://127.0.0.1');
      let pathname = decodeURIComponent(url.pathname);
      if (prefix) {
        if (pathname !== prefix && !pathname.startsWith(prefix + '/')) {
          throw new Error('outside the published prefix');
        }
        pathname = pathname.slice(prefix.length) || '/';
      }
      const relative = pathname.replace(/^\/+/, '');
      let file = resolve(ROOT, relative || 'index.html');
      if (file !== ROOT && !file.startsWith(ROOT + sep)) throw new Error('outside root');
      /* A directory answers with its own index.html, as the publishing host does.
       * That is not a fallback: a file that is simply absent still 404s, which is
       * what the gate exists to notice. */
      let body;
      try {
        body = await readFile(file);
      } catch (error) {
        if (error.code !== 'EISDIR') throw error;
        file = join(file, 'index.html');
        body = await readFile(file);
      }
      response.writeHead(200, {
        'content-type': mime(file),
        'content-length': body.length,
        'cache-control': 'no-store',
        'x-robots-tag': 'noindex, nofollow'
      });
      response.end(request.method === 'HEAD' ? undefined : body);
    } catch (_error) {
      response.writeHead(404, { 'content-type': 'text/plain; charset=utf-8' });
      response.end(request.method === 'HEAD' ? undefined : 'not found');
    }
  });
}

async function freePort() {
  const server = createServer();
  const port = await listen(server);
  await new Promise((accept) => server.close(accept));
  return port;
}

async function waitForJson(url, attempts = 200) {
  for (let attempt = 0; attempt < attempts; attempt += 1) {
    try {
      const response = await fetch(url);
      if (response.ok) return await response.json();
    } catch (_error) {
      // Chromium's debugging endpoint is not ready yet.
    }
    await new Promise((accept) => setTimeout(accept, 50));
  }
  throw new Error('Chromium debugging endpoint did not become ready: ' + url);
}

class CDP {
  constructor(url) {
    this.socket = new WebSocket(url);
    this.next = 0;
    this.pending = new Map();
    this.events = new Map();
  }

  async ready() {
    await new Promise((accept, reject) => {
      this.socket.addEventListener('open', accept, { once: true });
      this.socket.addEventListener('error', reject, { once: true });
    });
    this.socket.addEventListener('message', (event) => {
      const message = JSON.parse(event.data);
      if (message.id) {
        const pending = this.pending.get(message.id);
        if (!pending) return;
        this.pending.delete(message.id);
        clearTimeout(pending.timer);
        if (message.error) pending.reject(new Error(message.error.message));
        else pending.accept(message.result);
        return;
      }
      (this.events.get(message.method) || []).forEach((listener) => listener(message.params || {}));
    });
  }

  on(name, listener) {
    if (!this.events.has(name)) this.events.set(name, []);
    this.events.get(name).push(listener);
  }

  send(method, params = {}) {
    const id = ++this.next;
    return new Promise((accept, reject) => {
      const timer = setTimeout(() => {
        this.pending.delete(id);
        reject(new Error('CDP command timed out: ' + method));
      }, 20000);
      this.pending.set(id, { accept, reject, timer });
      this.socket.send(JSON.stringify({ id, method, params }));
    });
  }

  close() {
    this.socket.close();
  }
}

async function evaluate(cdp, expression) {
  const result = await cdp.send('Runtime.evaluate', {
    expression,
    awaitPromise: true,
    returnByValue: true,
    userGesture: true
  });
  if (result.exceptionDetails) {
    throw new Error(result.exceptionDetails.exception?.description || result.exceptionDetails.text);
  }
  return result.result.value;
}

async function key(cdp, name, code) {
  for (const type of ['keyDown', 'keyUp']) {
    await cdp.send('Input.dispatchKeyEvent', {
      type, key: name, code: name, windowsVirtualKeyCode: code, nativeVirtualKeyCode: code
    });
  }
}

function slug(route) {
  return route.replace(/^\/+/, '').replace(/\.html$/, '').replace(/[^A-Za-z0-9]+/g, '-') || 'root';
}

/* Every recorded detail is scrubbed of the ephemeral origins so two runs of the
 * same artifact produce byte-identical reports apart from `generatedAt`. Both the
 * root server and the subpath server are registered, longest first, so the subpath
 * origin is removed whole rather than leaving its prefix behind. */
const ephemeralOrigins = [];

function scrub(text) {
  let value = String(text ?? '');
  for (const origin of ephemeralOrigins) value = value.split(origin).join('');
  return value;
}

async function exists(path) {
  try {
    await access(path, constants.R_OK);
    return true;
  } catch (_error) {
    return false;
  }
}

async function firstPageUnder(directory, recursive) {
  const found = [];
  async function walk(relative) {
    let entries;
    try {
      entries = await readdir(join(ROOT, relative), { withFileTypes: true });
    } catch (_error) {
      return;
    }
    for (const entry of entries.sort((one, two) => one.name.localeCompare(two.name))) {
      const next = relative ? `${relative}/${entry.name}` : entry.name;
      if (entry.isDirectory() && recursive) await walk(next);
      else if (entry.isFile() && entry.name.endsWith('.html')) found.push('/' + next);
    }
  }
  await walk(directory);
  found.sort();
  return found[0] || null;
}

async function defaultRoutes() {
  const sampled = [];
  const missingFamilies = [];
  for (const family of SAMPLED_FAMILIES) {
    const route = await firstPageUnder(family.directory, family.recursive);
    if (route) sampled.push(route);
    else missingFamilies.push(family.name);
  }
  return {
    routes: [...INSTRUMENT_ROUTES, ...FIXED_SAMPLE_ROUTES, ...sampled].sort(),
    missingFamilies
  };
}

/* ---------------------------------------------------------------- page probes */

/* How a node is named in a failure detail: its tag, then its id or first class.
 * Enough to find it in the source, and stable between runs. */
const DESCRIPTOR = `((node) => {
  if (!node || !node.getAttribute) return String(node);
  const first = (node.getAttribute('class') || '').trim().split(/\\s+/)[0];
  return node.tagName.toLowerCase() +
    (node.id ? '#' + node.id : (first ? '.' + first : ''));
})`;

const SELECTOR = JSON.stringify(CONTROL_SELECTOR);

const VISIBLE_CONTROLS = `(() => {
  const describe = ${DESCRIPTOR};
  return [...document.querySelectorAll(${SELECTOR})].map((node) => {
    const box = node.getBoundingClientRect();
    return {
      visible: node.getClientRects().length > 0 && node.checkVisibility(),
      descriptor: describe(node),
      width: Math.round(box.width),
      height: Math.round(box.height)
    };
  });
})()`;

const DOCUMENT_FACTS = `(() => {
  const title = document.title || '';
  const roots = [document.documentElement, ...document.querySelectorAll('html')];
  const langs = [...new Set(roots)].map((root) => (root.getAttribute('lang') || '').trim());
  return {
    title,
    mainCount: document.querySelectorAll('main').length,
    h1Count: document.querySelectorAll('h1').length,
    langs,
    scrollWidth: document.documentElement.scrollWidth,
    clientWidth: document.documentElement.clientWidth
  };
})()`;

/* What a focus ring is made of, read off one element. Only ever compared with
 * another reading of the same element, never with a literal. */
const FINGERPRINT = `((node) => [null, '::before', '::after']
  .map((part) => {
    const style = window.getComputedStyle(node, part);
    return ${JSON.stringify(FOCUS_INDICATOR_PROPERTIES)}
      .map((name) => style.getPropertyValue(name)).join(',');
  })
  .join(' / '))`;

/* The active element after a Tab press. `stash` records the element and its
 * indicator while it genuinely holds keyboard focus, because that is the only
 * moment `:focus-visible` is in effect — a programmatic `focus()` does not
 * reliably reproduce it, and a check built on one is a check that flickers. The
 * matching unfocused readings are taken afterwards by FOCUS_RESTING. */
function activeElementProbe(stash) {
  return `(() => {
  const node = document.activeElement;
  if (!node || node === document.body || node === document.documentElement) {
    return { none: true, descriptor: node ? node.tagName.toLowerCase() : 'null' };
  }
  ${stash ? `(() => {
    const store = window.__triptychGateFocusSample || (window.__triptychGateFocusSample = []);
    if (store.length < ${FOCUS_SAMPLE} && !store.some((one) => one.node === node)) {
      store.push({ node, focused: (${FINGERPRINT})(node), descriptor: (${DESCRIPTOR})(node) });
    }
  })();` : ''}
  const box = node.getBoundingClientRect();
  const href = node.getAttribute ? node.getAttribute('href') : null;
  let targetExists = null;
  if (href && href.startsWith('#')) {
    const raw = href.slice(1);
    let id = raw;
    try { id = decodeURIComponent(raw); } catch (_error) { id = raw; }
    targetExists = Boolean(
      (id && document.getElementById(id)) ||
      (id && document.getElementsByName(id).length) ||
      raw === 'top'
    );
  }
  return {
    none: false,
    tag: node.tagName.toLowerCase(),
    descriptor: (${DESCRIPTOR})(node),
    href,
    samePage: Boolean(href && href.startsWith('#')),
    targetExists,
    width: Math.round(box.width),
    height: Math.round(box.height),
    text: (node.textContent || '').trim().slice(0, 60)
  };
})()`;
}

const ACTIVE_ELEMENT = activeElementProbe(false);
const ACTIVE_ELEMENT_SAMPLING = activeElementProbe(true);

/* The other half of the focus-indicator check: focus is released, and each element
 * the traversal stashed is read again with nothing focused. Each element is
 * therefore compared with ITSELF, and the assertion is that the two readings
 * differ. Nothing here says what a focus ring should look like — only that a
 * reader can tell focus apart from its absence.
 *
 * `::before` and `::after` are read too, so a ring drawn on a pseudo-element
 * counts. A ring drawn only by changing that pseudo-element's `content` would not
 * be seen; widening the fingerprint further would start to read the page's
 * appearance rather than its behaviour. */
const FOCUS_RESTING = `(() => {
  const store = window.__triptychGateFocusSample || [];
  const holder = document.activeElement;
  if (holder && holder.blur) holder.blur();
  return store.map((one) => ({
    descriptor: one.descriptor,
    differs: one.focused !== (${FINGERPRINT})(one.node)
  }));
})()`;

/* Target size. Only controls a reader can actually see are measured; a control
 * smaller than the minimum in either dimension is returned, marked with whether
 * the standard's inline exception covers it — a link inside a sentence, as opposed
 * to a link in navigation, a header, a footer or a form, which are chrome and are
 * not exempt however they are marked up. */
const UNDERSIZED_TARGETS = `((minimum) => {
  const describe = ${DESCRIPTOR};
  const rows = [];
  for (const node of document.querySelectorAll(${SELECTOR})) {
    if (!(node.getClientRects().length > 0 && node.checkVisibility())) continue;
    const box = node.getBoundingClientRect();
    const width = Math.round(box.width);
    const height = Math.round(box.height);
    if (width >= minimum && height >= minimum) continue;
    rows.push({
      descriptor: describe(node),
      /* An anchor often carries neither id nor class, so the descriptor alone
       * would not say which one. Its own text does. */
      text: (node.textContent || '').replace(/\\s+/g, ' ').trim().slice(0, 32),
      width,
      height,
      exempt: node.tagName === 'A' &&
        Boolean(node.closest(${JSON.stringify(PROSE_ANCESTORS)})) &&
        !node.closest(${JSON.stringify(CHROME_ANCESTORS)})
    });
  }
  return rows;
})(${TARGET_SIZE_MIN_PX})`;

/* Same-origin link targets, de-duplicated within the page and reported as
 * path+query so the ephemeral origin never enters the report. A `javascript:` or
 * `mailto:` href has a null origin and is dropped by the same-origin filter. */
const SAME_ORIGIN_LINKS = `(() => {
  const seen = new Set();
  for (const node of document.querySelectorAll('a[href]')) {
    const raw = node.getAttribute('href') || '';
    if (!raw || raw.startsWith('#')) continue;
    let url = null;
    try { url = new URL(node.href, document.baseURI); } catch (_error) { continue; }
    if (url.origin !== window.location.origin) continue;
    seen.add(url.pathname + url.search);
  }
  return [...seen].sort();
})()`;

/* What a reader has before a single line of the page's JavaScript has run. */
const STATIC_TRUTH = `(() => {
  const here = window.location.pathname;
  const links = new Set();
  for (const node of document.querySelectorAll('a[href]')) {
    const raw = node.getAttribute('href') || '';
    if (!raw || raw.startsWith('#')) continue;
    let url = null;
    try { url = new URL(node.href, document.baseURI); } catch (_error) { continue; }
    if (url.origin !== window.location.origin) continue;
    if (url.pathname === here && !url.search) continue;
    links.add(url.pathname + url.search);
  }
  return {
    title: (document.title || '').trim(),
    h1Count: document.querySelectorAll('h1').length,
    mainCount: document.querySelectorAll('main').length,
    links: [...links].sort()
  };
})()`;

/* A doubled site suffix is what a page picks up when it is wrapped in the release
 * layout after already carrying the layout's own title. Two adjacent separated
 * segments that are equal, or a final segment that occurs more than once, are both
 * that defect. */
function duplicatedTitleSegment(title) {
  const segments = title.split(/\s*[·|—]\s*/).map((one) => one.trim()).filter(Boolean);
  for (let index = 1; index < segments.length; index += 1) {
    if (segments[index] === segments[index - 1]) return segments[index];
  }
  if (segments.length > 1) {
    const last = segments[segments.length - 1];
    if (segments.filter((one) => one === last).length > 1) return last;
  }
  return null;
}

function collectNodeIds(node, into) {
  into.set(node.nodeId, node.backendNodeId);
  for (const child of node.children || []) collectNodeIds(child, into);
  for (const child of node.pseudoElements || []) collectNodeIds(child, into);
  if (node.contentDocument) collectNodeIds(node.contentDocument, into);
}

async function accessibleNames(cdp) {
  const { root } = await cdp.send('DOM.getDocument', { depth: -1 });
  const backendOf = new Map();
  collectNodeIds(root, backendOf);
  const { nodeIds } = await cdp.send('DOM.querySelectorAll', {
    nodeId: root.nodeId, selector: CONTROL_SELECTOR
  });
  const { nodes } = await cdp.send('Accessibility.getFullAXTree');
  const axOf = new Map();
  for (const node of nodes) {
    if (node.backendDOMNodeId === undefined) continue;
    axOf.set(node.backendDOMNodeId, {
      ignored: Boolean(node.ignored),
      role: node.role?.value || '',
      name: (node.name?.value || '').trim(),
      focusable: (node.properties || []).some(
        (property) => property.name === 'focusable' && property.value?.value === true
      )
    });
  }
  return { nodeIds, backendOf, axOf };
}

/* -------------------------------------------------------------- the assertions */

async function runPage(cdp, route, state, channel) {
  const results = [];
  const record = (name, status, detail = '') =>
    results.push({ name, status, detail: scrub(detail) });

  const facts = await evaluate(cdp, DOCUMENT_FACTS);

  /* 1 — nothing the page ran reported an error, and nothing it ran threw. */
  const consoleErrors = channel.consoleErrors.slice();
  const exceptions = channel.exceptions.slice();
  if (consoleErrors.length || exceptions.length) {
    record('no-console-errors', 'fail',
      [...consoleErrors, ...exceptions].slice(0, 6).join(' | '));
  } else {
    record('no-console-errors', 'pass');
  }

  /* 2 — every same-origin subresource the page asked for arrived. */
  const networkProblems = [
    ...channel.failed.map((one) => `${one.error}: ${one.url}`),
    ...channel.badStatus.map((one) => `HTTP ${one.status}: ${one.url}`)
  ];
  if (networkProblems.length) {
    record('no-failed-requests', 'fail', networkProblems.slice(0, 8).join(' | '));
  } else {
    record('no-failed-requests', 'pass');
  }

  /* 3 — one main region. Two is the publish-time wrapping defect. */
  record('single-main-element', facts.mainCount === 1 ? 'pass' : 'fail',
    `found ${facts.mainCount} <main> elements`);

  /* 4 — one first-level heading. */
  record('single-h1-element', facts.h1Count === 1 ? 'pass' : 'fail',
    `found ${facts.h1Count} <h1> elements`);

  /* 10 and 5 — walk the tab order from the top of a freshly loaded document. Where
   * the page has already taken focus for itself the first Tab does not start at the
   * top, and the detail says so rather than blaming a skip link that is present. */
  const resting = await evaluate(cdp, ACTIVE_ELEMENT);
  const stolenFocus = resting && !resting.none ? ` (the page had already moved focus to ${resting.descriptor})` : '';
  const sequence = [];
  for (let step = 0; step < TAB_DEPTH; step += 1) {
    await key(cdp, 'Tab', 9);
    /* The first stops are sampled for the focus-indicator check as they go past,
     * because the reading has to be taken while the element really holds keyboard
     * focus. */
    sequence.push(await evaluate(cdp,
      step < FOCUS_SAMPLE ? ACTIVE_ELEMENT_SAMPLING : ACTIVE_ELEMENT));
  }
  const first = sequence[0];
  if (!first || first.none) {
    record('skip-link-targets-existing-element', 'fail',
      `first Tab reached no control (${first ? first.descriptor : 'nothing'})`);
  } else if (first.tag !== 'a' || !first.samePage) {
    record('skip-link-targets-existing-element', 'fail',
      `first focusable element is ${first.descriptor}` +
      (first.href ? ` href="${first.href}"` : ' with no same-page href') +
      (first.text ? ` text "${first.text.slice(0, 40)}"` : '') + stolenFocus);
  } else if (first.targetExists !== true) {
    record('skip-link-targets-existing-element', 'fail',
      `skip link ${first.descriptor} points at "${first.href}" which no element answers`);
  } else {
    record('skip-link-targets-existing-element', 'pass',
      `${first.descriptor} -> ${first.href}`);
  }

  const reached = sequence.filter((one) => one && !one.none);
  const invisibleStops = sequence
    .slice(1)
    .filter((one) => one && !one.none && one.width === 0 && one.height === 0);
  if (!reached.length) {
    record('tab-traversal-reaches-visible-controls', 'fail',
      `${TAB_DEPTH} presses of Tab reached no control`);
  } else if (invisibleStops.length) {
    record('tab-traversal-reaches-visible-controls', 'fail',
      'tab order stops on zero-sized elements: ' +
      invisibleStops.map((one) => one.descriptor).slice(0, 6).join(', '));
  } else {
    record('tab-traversal-reaches-visible-controls', 'pass',
      `${reached.length} of ${TAB_DEPTH} presses reached a control`);
  }

  /* 6 — a page has a name, and it says the site's name once. */
  const duplicated = duplicatedTitleSegment(facts.title);
  if (!facts.title.trim()) {
    record('title-present-and-unduplicated', 'fail', 'document.title is empty');
  } else if (duplicated) {
    record('title-present-and-unduplicated', 'fail',
      `title "${facts.title}" repeats the segment "${duplicated}"`);
  } else {
    record('title-present-and-unduplicated', 'pass', facts.title);
  }

  /* 7 — the document declares its language. */
  const missingLang = facts.langs.filter((one) => !one);
  record('html-element-has-lang', missingLang.length ? 'fail' : 'pass',
    missingLang.length
      ? `${missingLang.length} of ${facts.langs.length} <html> elements carry no lang`
      : facts.langs.join(', '));

  /* 8 — the narrowest supported viewport does not scroll sideways. */
  if (state.width === 320) {
    const overflow = facts.scrollWidth - facts.clientWidth;
    record('no-horizontal-overflow-at-320',
      overflow <= OVERFLOW_TOLERANCE_PX ? 'pass' : 'fail',
      `scrollWidth ${facts.scrollWidth} exceeds clientWidth ${facts.clientWidth} ` +
      `by ${overflow}px (tolerance ${OVERFLOW_TOLERANCE_PX}px)`);
  } else {
    record('no-horizontal-overflow-at-320', 'skip',
      `not applicable at ${state.width}px`);
  }

  /* 9 — every control a reader can see can be named by assistive technology. */
  const controls = await evaluate(cdp, VISIBLE_CONTROLS);
  const { nodeIds, backendOf, axOf } = await accessibleNames(cdp);
  const unnamed = [];
  const limit = Math.min(controls.length, nodeIds.length);
  for (let index = 0; index < limit; index += 1) {
    if (!controls[index].visible) continue;
    const backend = backendOf.get(nodeIds[index]);
    const ax = backend === undefined ? null : axOf.get(backend);
    if (!ax || ax.ignored) continue;
    if (!INTERACTIVE_ROLES.has(ax.role) && !ax.focusable) continue;
    if (!ax.name) unnamed.push(`${controls[index].descriptor} [${ax.role || 'no role'}]`);
  }
  if (controls.length !== nodeIds.length) {
    record('interactive-controls-have-accessible-names', 'fail',
      `control enumeration disagreed: ${controls.length} in page, ${nodeIds.length} over CDP`);
  } else {
    record('interactive-controls-have-accessible-names', unnamed.length ? 'fail' : 'pass',
      unnamed.length
        ? `${unnamed.length} unnamed: ${unnamed.slice(0, 8).join(', ')}`
        : `${controls.filter((one) => one.visible).length} visible controls named`);
  }

  /* 12 — focus is visible. Each sampled control is compared with itself, so this
   * fails only when focus changes nothing a reader could see. */
  const focused = await evaluate(cdp, FOCUS_RESTING);
  const invisible = focused.filter((one) => !one.differs);
  if (!focused.length) {
    /* Tab reached nothing to sample. That is a real problem, but it is not this
     * assertion's problem: skip-link and tab-traversal own whether a control can
     * be reached at all, and reporting it twice would say the artifact has two
     * defects where it has one. The reason is recorded so the skip cannot be read
     * as coverage. */
    record('focus-indicator-differs-from-resting', 'skip',
      `${TAB_DEPTH} presses of Tab reached no control to sample`);
  } else {
    record('focus-indicator-differs-from-resting', invisible.length ? 'fail' : 'pass',
      invisible.length
        ? `${invisible.length} of ${focused.length} tab stops look identical focused ` +
          `and unfocused: ${invisible.map((one) => one.descriptor).slice(0, 6).join(', ')}`
        : `${focused.length} of the first ${FOCUS_SAMPLE} tab stops change visibly on focus`);
  }

  /* 13 — a control is big enough to hit with a thumb. Only at the handset width,
   * because that is where the standard's 44px is about a finger. */
  if (state.width === TARGET_SIZE_WIDTH) {
    const undersized = await evaluate(cdp, UNDERSIZED_TARGETS);
    const failing = undersized.filter((one) => !one.exempt);
    const exempt = undersized.filter((one) => one.exempt);
    const exemptNote = exempt.length
      ? `; ${exempt.length} inline prose links are exempt and reported only`
      : '';
    record('primary-controls-meet-target-size', failing.length ? 'fail' : 'pass',
      (failing.length
        ? `${failing.length} controls under ${TARGET_SIZE_MIN_PX}x${TARGET_SIZE_MIN_PX}: ` +
          failing.map((one) =>
            `${one.descriptor}${one.text ? ` "${one.text}"` : ''} ${one.width}x${one.height}`)
            .slice(0, 6).join(', ')
        : `every visible control is at least ${TARGET_SIZE_MIN_PX}x${TARGET_SIZE_MIN_PX}`) +
      exemptNote);
  } else {
    record('primary-controls-meet-target-size', 'skip',
      `measured only at the ${TARGET_SIZE_WIDTH}px handset width, not at ${state.width}px`);
  }

  /* 11 — the universal dismissal key is safe to press anywhere. */
  const beforeConsole = channel.consoleErrors.length;
  const beforeExceptions = channel.exceptions.length;
  await key(cdp, 'Escape', 27);
  await new Promise((accept) => setTimeout(accept, 60));
  const raised = [
    ...channel.consoleErrors.slice(beforeConsole),
    ...channel.exceptions.slice(beforeExceptions)
  ];
  record('escape-key-does-not-throw', raised.length ? 'fail' : 'pass',
    raised.slice(0, 4).join(' | '));

  return results;
}

/* ------------------------------------------------------------------- the drive */

async function applyState(cdp, state) {
  await cdp.send('Emulation.setDeviceMetricsOverride', {
    width: state.width,
    height: state.height,
    deviceScaleFactor: 1,
    mobile: state.width <= 768,
    screenWidth: state.width,
    screenHeight: state.height
  });
  await cdp.send('Emulation.setEmulatedMedia',
    state.media ? { media: 'screen', features: state.media } : { media: 'screen', features: [] });
  const scale = state.textScale || 1;
  await cdp.send('Page.setFontSizes', {
    fontSizes: {
      standard: BASE_FONT_SIZES.standard * scale,
      fixed: BASE_FONT_SIZES.fixed * scale
    }
  });
}

async function settle(cdp, channel) {
  const deadline = Date.now() + SETTLE_TIMEOUT_MS;
  let quiet = 0;
  while (Date.now() < deadline) {
    const complete = await evaluate(cdp, 'document.readyState === "complete"');
    quiet = complete && channel.inflight === 0 ? quiet + 1 : 0;
    if (quiet >= 3) return true;
    await new Promise((accept) => setTimeout(accept, 80));
  }
  return false;
}

async function main() {
  const chromeBinary = process.env.TRIPTYCH_CHROME
    || (await Promise.all(CHROME_CANDIDATES.map(exists)))
      .map((present, index) => (present ? CHROME_CANDIDATES[index] : null))
      .find(Boolean)
    || null;
  if (!chromeBinary || !(await exists(chromeBinary))) {
    process.stderr.write(
      'corpus_browser_gate: no Chromium binary is available.\n' +
      'Set TRIPTYCH_CHROME to a Chromium or Chrome executable, for example\n' +
      '  TRIPTYCH_CHROME=/usr/bin/chromium node tools/tests/corpus_browser_gate.mjs\n' +
      `Tried: ${(process.env.TRIPTYCH_CHROME || CHROME_CANDIDATES.join(', '))}\n` +
      'This gate reports nothing rather than reporting a pass it did not observe.\n'
    );
    process.exitCode = EXIT_NO_BROWSER;
    return;
  }
  if (!(await exists(join(ROOT, 'index.html')))) {
    process.stderr.write(
      `corpus_browser_gate: no built artifact at ${ROOT}.\n` +
      'Run `make public-site`, or set TRIPTYCH_REVIEW_ROOT to a built site root.\n'
    );
    process.exitCode = EXIT_NO_BROWSER;
    return;
  }

  const discovered = await defaultRoutes();
  const routes = routesArgument
    ? routesArgument.split(',').map((one) => one.trim()).filter(Boolean)
    : discovered.routes;

  const server = staticServer();
  const base = `http://127.0.0.1:${await listen(server)}`;
  const subpathServer = staticServer(SUBPATH_PREFIX);
  const subpathOrigin = `http://127.0.0.1:${await listen(subpathServer)}`;
  const subpathBase = subpathOrigin + SUBPATH_PREFIX;
  ephemeralOrigins.push(base, subpathOrigin);
  const debugPort = await freePort();
  const profile = await mkdtemp(join(tmpdir(), 'triptych-corpus-gate-chrome-'));

  /* Chromium on a workstation tries to register with Google's push service and to
   * talk to the desktop power daemon; neither is available here and both write to
   * stderr. They are switched off where a switch exists, and stderr is captured
   * rather than inherited so nothing Chromium prints can reach this gate's stdout. */
  const chrome = spawn(chromeBinary, [
    '--headless=new', '--no-sandbox', '--disable-dev-shm-usage', '--disable-gpu',
    '--disable-extensions', '--disable-component-extensions-with-background-pages',
    '--disable-background-networking', '--disable-component-update',
    '--disable-domain-reliability', '--disable-client-side-phishing-detection',
    '--disable-sync', '--no-pings', '--no-service-autorun', '--metrics-recording-only',
    '--password-store=basic', '--use-mock-keychain', '--mute-audio',
    '--disable-features=Translate,MediaRouter,OptimizationHints,InterestFeedContentSuggestions,CalculateNativeWinOcclusion,PushMessaging',
    `--remote-debugging-port=${debugPort}`, `--user-data-dir=${profile}`,
    '--no-first-run', '--no-default-browser-check', 'about:blank'
  ], { stdio: ['ignore', 'ignore', 'pipe'] });
  let chromeStderr = '';
  chrome.stderr.on('data', (chunk) => { chromeStderr += chunk.toString(); });

  /* `origin` is the origin the run currently treats as same-origin. It moves to the
   * subpath server for that phase, so a request the subpath mount cannot answer is
   * recorded as this artifact's failure and not dismissed as third-party. */
  const channel = {
    origin: base,
    consoleErrors: [], exceptions: [], failed: [], badStatus: [], inflight: 0, requests: new Map()
  };
  const assertions = [];
  const pages = [];
  const cappedRoutes = [];
  let cdp = null;
  let chromeVersion = 'unknown';

  const resetChannel = () => {
    channel.consoleErrors.length = 0;
    channel.exceptions.length = 0;
    channel.failed.length = 0;
    channel.badStatus.length = 0;
    channel.requests.clear();
    channel.inflight = 0;
  };

  /* Every phase adds rows the same way, so route/state/name ordering is a property
   * of the loops rather than of each call site. */
  const add = (name, route, state, status, detail = '') =>
    assertions.push({ name, route, state, status, detail: scrub(detail) });

  /* One HEAD per distinct target for the whole run: the navigation is shared by
   * every page, so without this the link check would resolve the same few hundred
   * targets nineteen times. */
  const statusCache = new Map();
  const statusOf = async (origin, target) => {
    const memo = origin + target;
    if (statusCache.has(memo)) return statusCache.get(memo);
    let status;
    try {
      status = (await fetch(origin + target, { method: 'HEAD' })).status;
    } catch (error) {
      status = `unreachable (${error.message})`;
    }
    statusCache.set(memo, status);
    return status;
  };
  const resolves = (status) => typeof status === 'number' && status >= 200 && status < 300;

  try {
    const version = await waitForJson(`http://127.0.0.1:${debugPort}/json/version`);
    chromeVersion = version.Browser || 'unknown';
    const created = await (await fetch(
      `http://127.0.0.1:${debugPort}/json/new?${encodeURIComponent('about:blank')}`,
      { method: 'PUT' }
    )).json();
    cdp = new CDP(created.webSocketDebuggerUrl);
    await cdp.ready();
    for (const domain of ['Page', 'Runtime', 'Network', 'DOM', 'Accessibility']) {
      await cdp.send(`${domain}.enable`);
    }

    cdp.on('Runtime.consoleAPICalled', ({ type, args }) => {
      if (type !== 'error' && type !== 'assert') return;
      channel.consoleErrors.push(
        args.map((arg) => arg.value ?? arg.description ?? arg.unserializableValue ?? '').join(' ')
      );
    });
    cdp.on('Runtime.exceptionThrown', ({ exceptionDetails }) => {
      channel.exceptions.push(
        exceptionDetails?.exception?.description || exceptionDetails?.text || 'exception'
      );
    });
    cdp.on('Network.requestWillBeSent', ({ requestId, request }) => {
      channel.inflight += 1;
      channel.requests.set(requestId, request.url);
    });
    const finish = (requestId) => {
      if (!channel.requests.has(requestId)) return;
      channel.requests.delete(requestId);
      channel.inflight = Math.max(0, channel.inflight - 1);
    };
    cdp.on('Network.loadingFinished', ({ requestId }) => finish(requestId));
    cdp.on('Network.loadingFailed', (event) => {
      const url = channel.requests.get(event.requestId) || '';
      finish(event.requestId);
      if (event.canceled) return;
      if (url && !url.startsWith(channel.origin)) return;
      channel.failed.push({ url, error: event.errorText || 'load failed' });
    });
    cdp.on('Network.responseReceived', ({ response }) => {
      if (!response.url.startsWith(channel.origin)) return;
      if (response.status >= 200 && response.status < 400) return;
      channel.badStatus.push({ status: response.status, url: response.url });
    });

    if (captureDir) await mkdir(captureDir, { recursive: true });

    /* ---------------------------------------------------- phase 1: the matrix */
    for (const route of routes) {
      for (const state of STATES) {
        await applyState(cdp, state);
        resetChannel();

        let settled = false;
        let results;
        try {
          await cdp.send('Page.navigate', { url: base + route });
          settled = await settle(cdp, channel);
          await cdp.send('Emulation.setPageScaleFactor', {
            pageScaleFactor: state.pageScale || 1
          });
          if (state.pageScale) await new Promise((accept) => setTimeout(accept, 120));
          results = await runPage(cdp, route, state, channel);
          if (!settled) {
            results.unshift({
              name: 'page-settles', status: 'fail',
              detail: `document did not reach a quiet complete state within ${SETTLE_TIMEOUT_MS}ms`
            });
          }
        } catch (error) {
          results = [{
            name: 'page-settles', status: 'fail',
            detail: scrub(error.stack || String(error))
          }];
        }

        if (captureDir) {
          try {
            const shot = await cdp.send('Page.captureScreenshot', {
              format: 'png', captureBeyondViewport: false, fromSurface: true
            });
            await writeFile(
              join(captureDir, `${slug(route)}--${state.name}--${state.width}x${state.height}.png`),
              Buffer.from(shot.data, 'base64')
            );
          } catch (_error) {
            // A capture that fails is evidence lost, not an assertion about the page.
          }
        }

        for (const one of results) add(one.name, route, state.name, one.status, one.detail);
        pages.push({
          route,
          state: state.name,
          viewport: `${state.width}x${state.height}`,
          passed: results.filter((one) => one.status === 'pass').length,
          failed: results.filter((one) => one.status === 'fail').length,
          skipped: results.filter((one) => one.status === 'skip').length
        });
      }
    }

    /* The remaining phases are facts about a route rather than about a viewport,
     * so each runs once per route at the widest supported state. Their rows carry
     * the phase name where a viewport name would be, which keeps one flat
     * assertion table without pretending a phase is a screen size. */
    await applyState(cdp, STATES[0]);
    await cdp.send('Emulation.setPageScaleFactor', { pageScaleFactor: 1 });

    /* ------------------------------------------- phase 2: the page without JS */
    await cdp.send('Emulation.setScriptExecutionDisabled', { value: true });
    for (const route of routes) {
      resetChannel();
      await cdp.send('Page.navigate', { url: base + route });
      await settle(cdp, channel);
      const truth = await evaluate(cdp, STATIC_TRUTH);
      const missing = [];
      if (!truth.title) missing.push('no <title>');
      if (truth.h1Count < 1) missing.push('no <h1>');
      if (truth.mainCount < 1) missing.push('no main landmark');
      let working = null;
      for (const target of truth.links.slice(0, LINKS_PER_ROUTE_CAP)) {
        if (resolves(await statusOf(base, target))) { working = target; break; }
      }
      if (!working) {
        missing.push(truth.links.length
          ? `none of its ${truth.links.length} same-origin links resolve`
          : 'no same-origin link to anywhere else');
      }
      add('no-script-static-truth', route, '(no-script)',
        missing.length ? 'fail' : 'pass',
        missing.length
          ? missing.join('; ')
          : `title "${truth.title}", ${truth.h1Count} h1, ${truth.mainCount} main, ` +
            `link to ${working} resolves`);
    }
    await cdp.send('Emulation.setScriptExecutionDisabled', { value: false });

    /* --------------------------------------- phase 3: hash deep-link contracts */
    for (const entry of HASH_DEEP_LINKS) {
      if (!routes.includes(entry.route)) continue;
      resetChannel();
      await cdp.send('Page.navigate', { url: base + entry.route + entry.hash });
      const settled = await settle(cdp, channel);
      const arrived = await evaluate(cdp, 'window.location.hash');
      const asked = new URLSearchParams(entry.hash.replace(/^#/, ''));
      const got = new URLSearchParams(String(arrived).replace(/^#/, ''));
      const lost = [];
      for (const [name, value] of asked) {
        if (got.get(name) !== value) lost.push(`${name}=${value} became ${got.get(name)}`);
      }
      const noise = [...channel.consoleErrors, ...channel.exceptions];
      const problems = [];
      if (!settled) problems.push(`did not settle within ${SETTLE_TIMEOUT_MS}ms`);
      if (noise.length) problems.push('console: ' + noise.slice(0, 3).join(' | '));
      if (lost.length) problems.push('the hash was rewritten: ' + lost.join(', '));
      add('hash-deep-link-is-honoured', entry.route, '(hash-deep-link)',
        problems.length ? 'fail' : 'pass',
        problems.length
          ? `${entry.hash} -> ${arrived}: ${problems.join('; ')}`
          : `${entry.hash} survived as ${arrived}`);
    }

    /* -------------------------------- phase 4: startup under a published prefix */
    channel.origin = subpathOrigin;
    for (const route of routes) {
      resetChannel();
      await cdp.send('Page.navigate', { url: subpathBase + route });
      const settled = await settle(cdp, channel);
      const problems = [
        ...channel.failed.map((one) => `${one.error}: ${one.url}`),
        ...channel.badStatus.map((one) => `HTTP ${one.status}: ${one.url}`)
      ];
      if (!settled) problems.unshift(`did not settle within ${SETTLE_TIMEOUT_MS}ms`);
      add('subpath-deep-link-startup', route, '(subpath)',
        problems.length ? 'fail' : 'pass',
        problems.length
          ? `under ${SUBPATH_PREFIX}/: ` + problems.slice(0, 8).join(' | ')
          : `loads under ${SUBPATH_PREFIX}/ with every same-origin request answered`);
    }
    channel.origin = base;

    /* -------------------------------------- phase 5: internal links go anywhere */
    for (const route of routes) {
      resetChannel();
      await cdp.send('Page.navigate', { url: base + route });
      await settle(cdp, channel);
      const collected = await evaluate(cdp, SAME_ORIGIN_LINKS);
      const considered = collected.slice(0, LINKS_PER_ROUTE_CAP);
      const notChecked = collected.length - considered.length;
      if (notChecked) {
        cappedRoutes.push({ route, collected: collected.length, checked: considered.length, notChecked });
      }
      const broken = [];
      for (const target of considered) {
        const status = await statusOf(base, target);
        if (!resolves(status)) broken.push(`${status}: ${target}`);
      }
      const capNote = notChecked
        ? ` (capped at ${LINKS_PER_ROUTE_CAP}; ${notChecked} of ${collected.length} NOT CHECKED)`
        : '';
      add('internal-links-resolve', route, '(links)', broken.length ? 'fail' : 'pass',
        (broken.length
          ? `${broken.length} of ${considered.length} checked links do not resolve: ` +
            broken.slice(0, 8).join(' | ')
          : `${considered.length} distinct same-origin links resolve`) + capNote);
    }
  } catch (error) {
    assertions.push({
      name: 'gate-runs', route: '(harness)', state: '(harness)', status: 'fail',
      detail: scrub((error.stack || String(error)) + '\n' + chromeStderr.slice(-2000))
    });
  } finally {
    if (cdp) cdp.close();
    chrome.kill('SIGTERM');
    await new Promise((accept) => server.close(accept));
    await new Promise((accept) => subpathServer.close(accept));
  }

  for (const family of discovered.missingFamilies) {
    if (routesArgument) break;
    assertions.push({
      name: 'gate-runs', route: `(${family})`, state: '(discovery)', status: 'fail',
      detail: `the built artifact holds no page under /${family}/`
    });
  }

  /* The phases append in phase order, which scatters a route's rows. Sorting by
   * route, then state, then assertion name puts the table in one order that does
   * not depend on how the run was scheduled, so two runs of the same artifact
   * differ only in `generatedAt`. */
  const order = (one, two) =>
    one.route.localeCompare(two.route) ||
    one.state.localeCompare(two.state) ||
    one.name.localeCompare(two.name);
  assertions.sort(order);

  const failures = assertions.filter((one) => one.status === 'fail');

  /* Counts per assertion kind, so the shape of a failing run is readable without
   * reading two thousand rows. `routesFailing` is what says whether a failure is
   * one bad page or a defect the whole artifact shares. */
  const summary = [...new Set(assertions.map((one) => one.name))].sort().map((name) => {
    const rows = assertions.filter((one) => one.name === name);
    const failing = rows.filter((one) => one.status === 'fail');
    return {
      name,
      total: rows.length,
      passed: rows.filter((one) => one.status === 'pass').length,
      failed: failing.length,
      skipped: rows.filter((one) => one.status === 'skip').length,
      routesFailing: new Set(failing.map((one) => one.route)).size
    };
  });

  const report = {
    generatedAt: new Date().toISOString(),
    chrome: chromeVersion,
    root: ROOT,
    routes,
    states: STATES.map((one) => ({ name: one.name, width: one.width, height: one.height })),
    phases: ['(no-script)', '(hash-deep-link)', '(subpath)', '(links)'],
    overflowTolerancePx: OVERFLOW_TOLERANCE_PX,
    /* Everything the run deliberately did not do, stated where a reader of the
     * report will see it. A bound recorded here is coverage this gate does not
     * claim. */
    bounds: {
      tabDepth: TAB_DEPTH,
      focusSample: FOCUS_SAMPLE,
      targetSizeMinPx: TARGET_SIZE_MIN_PX,
      targetSizeMeasuredAtWidth: TARGET_SIZE_WIDTH,
      linksPerRouteCap: LINKS_PER_ROUTE_CAP,
      cappedRoutes: cappedRoutes.sort((one, two) => one.route.localeCompare(two.route)),
      hashDeepLinksCovered: HASH_DEEP_LINKS.map((one) => one.route).sort(),
      subpathPrefix: SUBPATH_PREFIX + '/'
    },
    summary,
    pages,
    assertions,
    failures,
    counts: {
      routes: routes.length,
      states: STATES.length,
      pages: pages.length,
      assertions: assertions.length,
      passed: assertions.filter((one) => one.status === 'pass').length,
      failed: failures.length,
      skipped: assertions.filter((one) => one.status === 'skip').length
    }
  };

  const text = JSON.stringify(report, null, 2) + '\n';
  if (jsonOut) {
    await mkdir(resolve(jsonOut, '..'), { recursive: true });
    await writeFile(jsonOut, text);
  }
  if (captureDir) await writeFile(join(captureDir, 'corpus-browser-gate.json'), text);
  process.stdout.write(text);
  process.exitCode = failures.length ? 1 : 0;
}

await main();
