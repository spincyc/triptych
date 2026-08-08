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

const STATES = [
  { name: 'desktop-1440x1000', width: 1440, height: 1000 },
  { name: 'laptop-1024x768', width: 1024, height: 768 },
  { name: 'tablet-768x1024', width: 768, height: 1024 },
  { name: 'handset-393x852', width: 393, height: 852 },
  { name: 'narrow-320x800', width: 320, height: 800 },
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

/* One CSS pixel. Sub-pixel rounding of a fractional layout width can report a
 * scrollWidth one larger than clientWidth on a page that does not in fact scroll,
 * so a single pixel is forgiven and anything beyond it is reported. */
const OVERFLOW_TOLERANCE_PX = 1;
const CONTROL_SELECTOR =
  'a[href], button, input, select, textarea, [tabindex]:not([tabindex="-1"])';
const TAB_DEPTH = 10;
const SETTLE_TIMEOUT_MS = 9000;
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
 * gate reports it, rather than being papered over with an index fallback. */
function staticServer() {
  return createServer(async (request, response) => {
    let file = null;
    try {
      const url = new URL(request.url, 'http://127.0.0.1');
      const relative = decodeURIComponent(url.pathname).replace(/^\/+/, '');
      file = resolve(ROOT, relative || 'index.html');
      if (file !== ROOT && !file.startsWith(ROOT + sep)) throw new Error('outside root');
      const body = await readFile(file);
      response.writeHead(200, {
        'content-type': mime(file),
        'cache-control': 'no-store',
        'x-robots-tag': 'noindex, nofollow'
      });
      response.end(body);
    } catch (_error) {
      response.writeHead(404, { 'content-type': 'text/plain; charset=utf-8' });
      response.end('not found');
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

/* Every recorded detail is scrubbed of the ephemeral port so two runs of the same
 * artifact produce byte-identical reports apart from `generatedAt`. */
function scrub(text, base) {
  return String(text ?? '').split(base).join('');
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

const VISIBLE_CONTROLS = `(() => {
  const nodes = [...document.querySelectorAll(${JSON.stringify(CONTROL_SELECTOR)})];
  return nodes.map((node) => {
    const box = node.getBoundingClientRect();
    const visible = node.getClientRects().length > 0 && node.checkVisibility();
    const identity = node.id ? '#' + node.id
      : (node.getAttribute('class') || '').trim().split(/\\s+/)[0]
        ? '.' + (node.getAttribute('class') || '').trim().split(/\\s+/)[0]
        : '';
    return {
      visible,
      descriptor: node.tagName.toLowerCase() + identity,
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

const ACTIVE_ELEMENT = `(() => {
  const node = document.activeElement;
  if (!node || node === document.body || node === document.documentElement) {
    return { none: true, descriptor: node ? node.tagName.toLowerCase() : 'null' };
  }
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
  const identity = node.id ? '#' + node.id
    : (node.getAttribute('class') || '').trim().split(/\\s+/)[0]
      ? '.' + (node.getAttribute('class') || '').trim().split(/\\s+/)[0]
      : '';
  return {
    none: false,
    tag: node.tagName.toLowerCase(),
    descriptor: node.tagName.toLowerCase() + identity,
    href,
    samePage: Boolean(href && href.startsWith('#')),
    targetExists,
    width: Math.round(box.width),
    height: Math.round(box.height),
    text: (node.textContent || '').trim().slice(0, 60)
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

async function runPage(cdp, base, route, state, channel) {
  const results = [];
  const record = (name, status, detail = '') =>
    results.push({ name, status, detail: scrub(detail, base) });

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
    sequence.push(await evaluate(cdp, ACTIVE_ELEMENT));
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
  const serverPort = await listen(server);
  const base = `http://127.0.0.1:${serverPort}`;
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

  const channel = {
    consoleErrors: [], exceptions: [], failed: [], badStatus: [], inflight: 0, requests: new Map()
  };
  const assertions = [];
  const pages = [];
  let cdp = null;
  let chromeVersion = 'unknown';

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
      if (url && !url.startsWith(base)) return;
      channel.failed.push({ url, error: event.errorText || 'load failed' });
    });
    cdp.on('Network.responseReceived', ({ response }) => {
      if (!response.url.startsWith(base)) return;
      if (response.status >= 200 && response.status < 400) return;
      channel.badStatus.push({ status: response.status, url: response.url });
    });

    if (captureDir) await mkdir(captureDir, { recursive: true });

    for (const route of routes) {
      for (const state of STATES) {
        await applyState(cdp, state);
        channel.consoleErrors.length = 0;
        channel.exceptions.length = 0;
        channel.failed.length = 0;
        channel.badStatus.length = 0;
        channel.requests.clear();
        channel.inflight = 0;

        const target = base + route;
        let settled = false;
        let results;
        try {
          await cdp.send('Page.navigate', { url: target });
          settled = await settle(cdp, channel);
          await cdp.send('Emulation.setPageScaleFactor', {
            pageScaleFactor: state.pageScale || 1
          });
          if (state.pageScale) await new Promise((accept) => setTimeout(accept, 120));
          results = await runPage(cdp, base, route, state, channel);
          if (!settled) {
            results.unshift({
              name: 'page-settles', status: 'fail',
              detail: `document did not reach a quiet complete state within ${SETTLE_TIMEOUT_MS}ms`
            });
          }
        } catch (error) {
          results = [{
            name: 'page-settles', status: 'fail',
            detail: scrub(error.stack || String(error), base)
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

        for (const one of results) {
          assertions.push({ name: one.name, route, state: state.name, status: one.status, detail: one.detail });
        }
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
  } catch (error) {
    assertions.push({
      name: 'gate-runs', route: '(harness)', state: '(harness)', status: 'fail',
      detail: scrub((error.stack || String(error)) + '\n' + chromeStderr.slice(-2000), base)
    });
  } finally {
    if (cdp) cdp.close();
    chrome.kill('SIGTERM');
    await new Promise((accept) => server.close(accept));
  }

  for (const family of discovered.missingFamilies) {
    if (routesArgument) break;
    assertions.push({
      name: 'gate-runs', route: `(${family})`, state: '(discovery)', status: 'fail',
      detail: `the built artifact holds no page under /${family}/`
    });
  }

  const failures = assertions.filter((one) => one.status === 'fail');
  const report = {
    generatedAt: new Date().toISOString(),
    chrome: chromeVersion,
    root: ROOT,
    routes,
    states: STATES.map((one) => ({ name: one.name, width: one.width, height: one.height })),
    overflowTolerancePx: OVERFLOW_TOLERANCE_PX,
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
