/* Dependency-free Chromium assertions and deterministic evidence for the five
 * Wave 1 corpus prototypes. The real public preview is always served below the
 * GitHub-Pages-style /triptych/ prefix. "Before" cases receive those bytes
 * unchanged; "after" cases receive only the isolated prototype CSS and JS.
 */

import { spawn, spawnSync } from 'node:child_process';
import { createHash } from 'node:crypto';
import { createServer } from 'node:http';
import {
  access, mkdir, mkdtemp, readFile, readdir, rm, stat, writeFile
} from 'node:fs/promises';
import { constants } from 'node:fs';
import { tmpdir } from 'node:os';
import { dirname, extname, join, relative, resolve, sep } from 'node:path';
import process from 'node:process';

const REPO = resolve(import.meta.dirname, '../..');
const PREVIEW = resolve(process.env.TRIPTYCH_REVIEW_ROOT || join(REPO, 'build/public-alpha/preview'));
const PROJECT_PREFIX = '/triptych';
const PROTOTYPE_ROOT = resolve(REPO, 'src/web/browser/prototypes/corpus-wave-1');
const PROTOTYPE_FIXTURE = join(PROTOTYPE_ROOT, 'index.html');
const PROTOTYPE_CSS = join(PROTOTYPE_ROOT, 'prototype.css');
const PROTOTYPE_JAVASCRIPT = join(PROTOTYPE_ROOT, 'prototype.js');
const DOCUMENT_CORPUS = join(PREVIEW, 'browse/structure/documents/corpus.json');
const DEFAULT_MATRIX = resolve(REPO, 'tools/tests/fixtures/corpus-wave1-prototype-matrix-v1.json');
const IPV4_LOOPBACK_OCTETS = [127, 0, 0, 1];
const LOOPBACK = IPV4_LOOPBACK_OCTETS.join('.');
const OVERFLOW_TOLERANCE_PX = 1;
const INHERITED_NESTED_MAIN_SURFACES = new Set(['publications', 'catena', 'sources']);
const CONTROL_ROLES = new Set([
  'button', 'checkbox', 'combobox', 'link', 'listbox', 'menuitem',
  'menuitemcheckbox', 'menuitemradio', 'option', 'radio', 'searchbox',
  'slider', 'spinbutton', 'switch', 'tab', 'textbox'
]);
const ALLOWED_EMULATIONS = new Set([
  'default', 'text-200', 'reflow-400', 'keyboard', 'forced-colors',
  'reduced-motion', 'no-js', 'print', 'zoom-400'
]);
const ALLOWED_VIEWPORTS = new Set([
  '1440x900', '1024x768', '768x1024', '393x852', '320x852'
]);
const CHROME_CANDIDATES = [
  'chromium', 'chromium-browser', 'google-chrome-stable', 'google-chrome'
];
const SETTLE_TIMEOUT_MS = 12000;
const REUSE_RIGHTS_TEXT = 'Reuse and rights. To the extent Triptych holds the rights, ' +
  'project-created content and design are licensed under CC BY 4.0. Scripture, liturgical or ' +
  'official texts, received prayers or hymns, quotations, fonts, and other third-party material ' +
  'retain their own status; public-domain material remains public domain. Identify changes. ' +
  'Attribution implies neither Triptych nor ecclesiastical approval. See LICENSE and ' +
  'THIRD_PARTY.md in the source.';

function usage() {
  return `usage: corpus_wave1_prototype_browser.mjs [options]\n\n` +
    `Serve build/public-alpha/preview beneath /triptych/, run the ordered Wave 1\n` +
    `before/after matrix in real Chromium, and optionally write deterministic\n` +
    `viewport captures and canonical JSON. After cases inject only the matrix's\n` +
    `isolated prototype CSS and JavaScript into the same preview route.\n\n` +
    `options:\n` +
    `  --matrix FILE       matrix JSON (default: tools/tests/fixtures/corpus-wave1-prototype-matrix-v1.json)\n` +
    `  --capture-dir DIR   write numbered PNG captures into an absent or empty directory\n` +
    `  --json-out FILE     write canonical scrubbed JSON in addition to stdout\n` +
    `  -h, --help          show this help\n\n` +
    `environment:\n` +
    `  TRIPTYCH_CHROME      Chromium/Chrome executable; auto-detected when unset\n` +
    `  TRIPTYCH_REVIEW_ROOT public-preview root (default: build/public-alpha/preview)\n\n` +
    `Print capture cases also require pdfinfo, pdftotext, and pdftoppm on PATH.\n`;
}

function parseArguments(argv) {
  const options = { matrix: DEFAULT_MATRIX, captureDir: null, jsonOut: null, help: false };
  const valued = new Map([
    ['--matrix', 'matrix'], ['--capture-dir', 'captureDir'], ['--json-out', 'jsonOut']
  ]);
  for (let at = 0; at < argv.length; at += 1) {
    const token = argv[at];
    if (token === '--help' || token === '-h') {
      options.help = true;
      continue;
    }
    const name = valued.get(token);
    if (!name) throw new Error(`unknown argument: ${token}`);
    if (at + 1 >= argv.length || argv[at + 1].startsWith('--')) {
      throw new Error(`${token} requires a value`);
    }
    options[name] = resolve(argv[++at]);
  }
  return options;
}

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
    '.xml': 'application/xml; charset=utf-8',
    '.pdf': 'application/pdf',
    '.woff': 'font/woff',
    '.woff2': 'font/woff2'
  })[extname(path).toLowerCase()] || 'application/octet-stream';
}

async function exists(path) {
  try {
    await access(path, constants.R_OK);
    return true;
  } catch (_error) {
    return false;
  }
}

function within(root, path) {
  return path === root || path.startsWith(root + sep);
}

function repoFile(path, label) {
  if (typeof path !== 'string' || !path || path.startsWith('/')) {
    throw new Error(`${label} must be a nonempty repository-relative path`);
  }
  const held = resolve(REPO, path);
  if (!within(REPO, held)) throw new Error(`${label} escapes the repository`);
  return held;
}

function cleanRoute(route) {
  if (typeof route !== 'string' || !route.startsWith('/') || route.startsWith('//')) {
    throw new Error('case route must be production-root-relative and begin with one slash');
  }
  const parsed = new URL(route, 'https://invalid.example');
  if (parsed.origin !== 'https://invalid.example' || parsed.pathname.split('/').includes('..')) {
    throw new Error(`unsafe case route: ${route}`);
  }
  if (parsed.pathname === PROJECT_PREFIX || parsed.pathname.startsWith(PROJECT_PREFIX + '/')) {
    throw new Error(`case route must omit the ${PROJECT_PREFIX} mount prefix: ${route}`);
  }
  return parsed.pathname + parsed.search + parsed.hash;
}

function selector(value, label, optional = true) {
  if ((value === null || value === undefined || value === '') && optional) return null;
  if (typeof value !== 'string' || !value.trim()) throw new Error(`${label} must be a CSS selector`);
  return value;
}

function validateAction(action, caseId, index) {
  if (!action || typeof action !== 'object' || Array.isArray(action)) {
    throw new Error(`${caseId} action ${index + 1} must be an object`);
  }
  const allowed = new Set(['click', 'focus', 'wait', 'wait-text', 'type', 'tab', 'key', 'scroll']);
  if (!allowed.has(action.op)) throw new Error(`${caseId} action ${index + 1} has unknown op ${action.op}`);
  if (['click', 'focus', 'wait', 'wait-text', 'type', 'scroll'].includes(action.op)) {
    selector(action.selector, `${caseId} action ${index + 1} selector`, false);
  }
  if (action.op === 'wait-text' &&
      typeof action.text !== 'string' && typeof action.absent !== 'string') {
    throw new Error(`${caseId} action ${index + 1} wait-text requires text or absent`);
  }
  if (action.op === 'type' && typeof action.value !== 'string') {
    throw new Error(`${caseId} action ${index + 1} type value must be a string`);
  }
  if (action.op === 'tab' && (!Number.isInteger(action.count ?? 1) || (action.count ?? 1) < 1)) {
    throw new Error(`${caseId} action ${index + 1} tab count must be a positive integer`);
  }
  if (action.op === 'key' && (typeof action.key !== 'string' || !action.key)) {
    throw new Error(`${caseId} action ${index + 1} key must be a nonempty string`);
  }
  if (action.op === 'scroll' && action.block !== undefined &&
      !['start', 'center', 'end', 'nearest'].includes(action.block)) {
    throw new Error(`${caseId} action ${index + 1} has invalid scroll block`);
  }
  return { ...action };
}

function validateMatrix(value) {
  if (!value || typeof value !== 'object' || Array.isArray(value)) throw new Error('matrix must be an object');
  if (value.version !== 1) throw new Error(`unsupported matrix version: ${value.version}`);
  const assets = value.prototype_assets;
  if (!assets || typeof assets !== 'object') throw new Error('matrix prototype_assets is required');
  const css = repoFile(assets.css, 'prototype_assets.css');
  const javascript = repoFile(assets.javascript, 'prototype_assets.javascript');
  if (css !== PROTOTYPE_CSS || javascript !== PROTOTYPE_JAVASCRIPT) {
    throw new Error('matrix prototype assets must name the isolated corpus-wave-1 CSS and JavaScript');
  }
  if (!Array.isArray(value.cases) || !value.cases.length) throw new Error('matrix cases must be a nonempty array');
  const ids = new Set();
  const seenViewports = new Set();
  const seenEmulations = new Set();
  const cases = value.cases.map((held, index) => {
    if (!held || typeof held !== 'object' || Array.isArray(held)) throw new Error(`case ${index + 1} must be an object`);
    if (typeof held.id !== 'string' || !/^[a-z0-9][a-z0-9-]*$/.test(held.id)) {
      throw new Error(`case ${index + 1} id must be a lowercase kebab-case slug`);
    }
    if (ids.has(held.id)) throw new Error(`duplicate case id: ${held.id}`);
    ids.add(held.id);
    if (typeof held.surface !== 'string' || !held.surface) throw new Error(`${held.id} surface is required`);
    if (!['before', 'after'].includes(held.phase)) throw new Error(`${held.id} phase must be before or after`);
    const route = cleanRoute(held.route);
    const viewport = held.viewport;
    if (!viewport || !Number.isInteger(viewport.width) || !Number.isInteger(viewport.height)) {
      throw new Error(`${held.id} viewport requires integer width and height`);
    }
    const viewportName = `${viewport.width}x${viewport.height}`;
    if (!ALLOWED_VIEWPORTS.has(viewportName)) {
      throw new Error(`${held.id} viewport ${viewportName} is outside the binding Wave 1 matrix`);
    }
    seenViewports.add(viewportName);
    const emulation = held.emulation || 'default';
    if (!ALLOWED_EMULATIONS.has(emulation)) throw new Error(`${held.id} has unknown emulation ${emulation}`);
    seenEmulations.add(emulation);
    if (emulation === 'reflow-400' && viewport.width !== 320) {
      throw new Error(`${held.id} reflow-400 must use the 320 CSS-pixel viewport`);
    }
    const expectation = held.expect || {};
    if (!expectation || typeof expectation !== 'object' || Array.isArray(expectation)) {
      throw new Error(`${held.id} expect must be an object`);
    }
    const strings = (name) => {
      const rows = expectation[name] ?? [];
      if (!Array.isArray(rows) || rows.some((one) => typeof one !== 'string')) {
        throw new Error(`${held.id} expect.${name} must be an array of strings`);
      }
      return rows.slice();
    };
    const allowedHttp = expectation.allowed_http ?? [];
    if (!Array.isArray(allowedHttp) || allowedHttp.some((one) =>
      !one || typeof one !== 'object' || Array.isArray(one) ||
      !Number.isInteger(one.status) || one.status < 400 || one.status > 599)) {
      throw new Error(`${held.id} expect.allowed_http must contain path/status objects for HTTP errors`);
    }
    const inheritedRoute = expectation.inherited_route ?? null;
    if (inheritedRoute !== null &&
        (!inheritedRoute || typeof inheritedRoute !== 'object' || Array.isArray(inheritedRoute) ||
         typeof inheritedRoute.reason !== 'string' || !inheritedRoute.reason.trim())) {
      throw new Error(`${held.id} expect.inherited_route must contain route and reason`);
    }
    const inheritedOverlay = expectation.inherited_overlay ?? null;
    const overlayAssertions = new Set([
      'reader-record-visible-provider', 'reader-record-visible-pdf'
    ]);
    if (inheritedOverlay !== null &&
        (!inheritedOverlay || typeof inheritedOverlay !== 'object' || Array.isArray(inheritedOverlay) ||
         !Array.isArray(inheritedOverlay.assertions) || !inheritedOverlay.assertions.length ||
         inheritedOverlay.assertions.some((one) => typeof one !== 'string' || !overlayAssertions.has(one)) ||
         new Set(inheritedOverlay.assertions).size !== inheritedOverlay.assertions.length ||
         typeof inheritedOverlay.reason !== 'string' || !inheritedOverlay.reason.trim())) {
      throw new Error(`${held.id} expect.inherited_overlay must contain unique supported assertions and reason`);
    }
    if (inheritedOverlay &&
        !(held.surface === 'reader' && held.phase === 'after' && emulation === 'no-js')) {
      throw new Error(`${held.id} expect.inherited_overlay is restricted to the after Reader no-js case`);
    }
    const links = expectation.links ?? [];
    if (!Array.isArray(links) || links.some((one) =>
      !one || typeof one !== 'object' || Array.isArray(one) ||
      typeof one.href !== 'string')) {
      throw new Error(`${held.id} expect.links must contain selector/href objects`);
    }
    const exactText = expectation.exact_text ?? [];
    if (!Array.isArray(exactText) || exactText.some((one) =>
      !one || typeof one !== 'object' || Array.isArray(one) ||
      typeof one.text !== 'string')) {
      throw new Error(`${held.id} expect.exact_text must contain selector/text objects`);
    }
    const closeAndRestore = expectation.close_and_restore ?? null;
    if (closeAndRestore !== null &&
        (!closeAndRestore || typeof closeAndRestore !== 'object' || Array.isArray(closeAndRestore))) {
      throw new Error(`${held.id} expect.close_and_restore must contain control, origin, and hidden selectors`);
    }
    if (closeAndRestore &&
        !(held.surface === 'publications' && held.phase === 'after' && emulation === 'keyboard')) {
      throw new Error(`${held.id} expect.close_and_restore is restricted to after Publications keyboard cases`);
    }
    const currentContents = expectation.current_contents ?? null;
    if (currentContents !== null &&
        (typeof currentContents !== 'string' || !currentContents || currentContents.startsWith('#'))) {
      throw new Error(`${held.id} expect.current_contents must be a heading id without #`);
    }
    if (currentContents && !(held.surface === 'reader' && held.phase === 'after')) {
      throw new Error(`${held.id} expect.current_contents is restricted to after Reader cases`);
    }
    return {
      id: held.id,
      surface: held.surface,
      phase: held.phase,
      route,
      viewport: { width: viewport.width, height: viewport.height },
      emulation,
      actions: (held.actions || []).map((action, actionIndex) => validateAction(action, held.id, actionIndex)),
      expect: {
        ready: selector(expectation.ready || 'main', `${held.id} expect.ready`, false),
        useful: selector(expectation.useful || 'main', `${held.id} expect.useful`, false),
        primaryTargets: strings('primary_targets'),
        focus: selector(expectation.focus, `${held.id} expect.focus`),
        focusWithin: selector(expectation.focus_within, `${held.id} expect.focus_within`),
        restoreFocusAfterEscape: selector(
          expectation.restore_focus_after_escape,
          `${held.id} expect.restore_focus_after_escape`
        ),
        text: strings('text'),
        absentText: strings('absent_text'),
        absentSelectors: strings('absent_selectors'),
        requests: strings('requests').map((one) => cleanRoute(one)),
        links: links.map((one, linkIndex) => ({
          selector: selector(one.selector, `${held.id} expect.links ${linkIndex + 1}`, false),
          href: cleanRoute(one.href)
        })),
        exactText: exactText.map((one, textIndex) => ({
          selector: selector(one.selector, `${held.id} expect.exact_text ${textIndex + 1}`, false),
          text: one.text
        })),
        closeAndRestore: closeAndRestore ? {
          control: selector(closeAndRestore.control, `${held.id} expect.close_and_restore control`, false),
          origin: selector(closeAndRestore.origin, `${held.id} expect.close_and_restore origin`, false),
          hidden: selector(closeAndRestore.hidden, `${held.id} expect.close_and_restore hidden`, false)
        } : null,
        currentContents,
        printText: strings('print_text'),
        allowedHttp: allowedHttp.map((one) => ({
          path: cleanRoute(one.path), status: one.status
        })),
        inheritedRoute: inheritedRoute ? {
          route: cleanRoute(inheritedRoute.route), reason: inheritedRoute.reason.trim()
        } : null,
        inheritedOverlay: inheritedOverlay ? {
          assertions: inheritedOverlay.assertions.slice(), reason: inheritedOverlay.reason.trim()
        } : null
      }
    };
  });
  const missingViewports = [...ALLOWED_VIEWPORTS].filter((held) => !seenViewports.has(held));
  if (missingViewports.length) {
    throw new Error(`matrix omits required viewports: ${missingViewports.join(', ')}`);
  }
  const missingEmulations = [...ALLOWED_EMULATIONS].filter((held) => !seenEmulations.has(held));
  if (missingEmulations.length) {
    throw new Error(`matrix omits required emulations: ${missingEmulations.join(', ')}`);
  }
  return { version: 1, assets: { css, javascript }, cases };
}

async function readMatrix(path) {
  let parsed;
  let source;
  try {
    source = await readFile(path);
    parsed = JSON.parse(source.toString('utf8'));
  } catch (error) {
    throw new Error(`cannot read matrix: ${error.message}`);
  }
  return { ...validateMatrix(parsed), sha256: createHash('sha256').update(source).digest('hex') };
}

async function sha256(path) {
  return createHash('sha256').update(await readFile(path)).digest('hex');
}

async function listen(server) {
  await new Promise((accept, reject) => {
    server.once('error', reject);
    server.listen(0, LOOPBACK, accept);
  });
  return server.address().port;
}

async function freePort() {
  const server = createServer();
  const port = await listen(server);
  await new Promise((accept) => server.close(accept));
  return port;
}

function mountedRecordHref(value, prefix, label) {
  if (typeof value !== 'string' || !value.startsWith(prefix) || value.includes('..')) {
    throw new Error(`${label} has an invalid generated public path`);
  }
  return `${PROJECT_PREFIX}/${value}`;
}

async function loadPublicationRecords() {
  const corpus = JSON.parse(await readFile(DOCUMENT_CORPUS, 'utf8'));
  if (corpus.schema !== 'triptych-document-catalogue/v1' || !Array.isArray(corpus.providers) ||
      !Array.isArray(corpus.works)) {
    throw new Error('generated document corpus has an unsupported shape');
  }
  const providers = new Map(corpus.providers.map((one) => [one.id, one.label]));
  const records = new Map();
  for (const work of corpus.works) {
    if (!Array.isArray(work.editions)) continue;
    for (const edition of work.editions) {
      if (typeof edition.web !== 'string') continue;
      const provider = { id: edition.provider, label: providers.get(edition.provider) };
      if (typeof provider.label !== 'string') throw new Error(`unknown corpus provider: ${provider.id}`);
      const route = mountedRecordHref(edition.web, `web/${provider.id}/`, 'edition.web')
        .slice(PROJECT_PREFIX.length);
      const pdfHref = mountedRecordHref(edition.pdf, `pdf/${provider.id}/`, 'edition.pdf');
      const sibling = work.editions.find((one) => one.provider !== provider.id && typeof one.web === 'string');
      let parallel = null;
      let parallelPath = null;
      if (sibling) {
        const siblingProvider = { id: sibling.provider, label: providers.get(sibling.provider) };
        if (typeof siblingProvider.label !== 'string') {
          throw new Error(`unknown sibling corpus provider: ${siblingProvider.id}`);
        }
        parallelPath = mountedRecordHref(
          sibling.web, `web/${siblingProvider.id}/`, 'sibling.web'
        );
        parallel = { provider: siblingProvider, webHref: parallelPath };
      }
      if (records.has(route)) throw new Error(`duplicate generated Reader record: ${route}`);
      records.set(route, {
        payload: { provider, pdfHref, parallel },
        routeProvider: provider.id,
        pdfPath: pdfHref,
        parallelPath
      });
    }
  }
  return records;
}

function htmlAttribute(value) {
  return String(value).replaceAll('&', '&amp;').replaceAll('"', '&quot;')
    .replaceAll('<', '&lt;').replaceAll('>', '&gt;');
}

function injectPrototype(html, publication) {
  if (!/<\/head\s*>/i.test(html) || !/<\/body\s*>/i.test(html)) {
    throw new Error('after-phase HTML lacks closing head or body');
  }
  const record = publication?.payload;
  const recordAttributes = record ? [
    ['data-wave-record-provider', record.provider.id],
    ['data-wave-record-provider-label', record.provider.label],
    ['data-wave-record-pdf', record.pdfHref],
    ['data-wave-record-parallel-provider', record.parallel?.provider.id || ''],
    ['data-wave-record-parallel-label', record.parallel?.provider.label || ''],
    ['data-wave-record-parallel-web', record.parallel?.webHref || '']
  ].map(([name, value]) => ` ${name}="${htmlAttribute(value)}"`).join('') : '';
  let output = html.replace(
    /<html\b/i,
    `<html data-wave1-prototype-phase="after"${recordAttributes}`
  );
  output = output.replace(
    /<\/head\s*>/i,
    `  <link rel="stylesheet" data-wave1-prototype-css href="${PROJECT_PREFIX}/__wave1/prototype.css">\n</head>`
  );
  return output.replace(
    /<\/body\s*>/i,
    `  <script defer data-wave1-prototype-js src="${PROJECT_PREFIX}/__wave1/prototype.js"></script>\n</body>`
  );
}

function governedPrototypeRoute(route, publications) {
  if (new Set(['/', '/texts/', '/catena/', '/sources/']).has(route)) return true;
  return /^\/web\/(?:gpt|claude)\/.+\.html$/.test(route) && publications.has(route);
}

function staticServer(state) {
  return createServer(async (request, response) => {
    try {
      const url = new URL(request.url, `http://${LOOPBACK}`);
      if (url.pathname === `${PROJECT_PREFIX}/__wave1/prototype.css`) {
        const body = await readFile(state.assets.css);
        response.writeHead(200, {
          'content-type': mime(state.assets.css), 'cache-control': 'no-store',
          'x-robots-tag': 'noindex, nofollow'
        });
        response.end(body);
        return;
      }
      if (url.pathname === `${PROJECT_PREFIX}/__wave1/prototype.js`) {
        const body = await readFile(state.assets.javascript);
        response.writeHead(200, {
          'content-type': mime(state.assets.javascript), 'cache-control': 'no-store',
          'x-robots-tag': 'noindex, nofollow'
        });
        response.end(body);
        return;
      }
      if (url.pathname !== PROJECT_PREFIX && !url.pathname.startsWith(PROJECT_PREFIX + '/')) {
        throw new Error('outside project prefix');
      }
      let relativePath = decodeURIComponent(url.pathname.slice(PROJECT_PREFIX.length)).replace(/^\/+/, '');
      if (!relativePath) relativePath = 'index.html';
      let file = resolve(PREVIEW, relativePath);
      if (!within(PREVIEW, file)) throw new Error('outside preview root');
      const held = await stat(file);
      if (held.isDirectory()) file = join(file, 'index.html');
      let body = await readFile(file);
      const route = url.pathname.slice(PROJECT_PREFIX.length) || '/';
      if (state.phase === 'after' && extname(file).toLowerCase() === '.html' &&
          governedPrototypeRoute(route, state.publications)) {
        body = Buffer.from(injectPrototype(
          body.toString('utf8'), state.publications.get(route) || null
        ), 'utf8');
      }
      response.writeHead(200, {
        'content-type': mime(file), 'cache-control': 'no-store',
        'x-robots-tag': 'noindex, nofollow'
      });
      response.end(body);
    } catch (_error) {
      response.writeHead(404, {
        'content-type': 'text/plain; charset=utf-8', 'cache-control': 'no-store',
        'x-robots-tag': 'noindex, nofollow'
      });
      response.end('not found');
    }
  });
}

async function protectedSurfaceAssertions(base, state) {
  const rows = [];
  const protectedRoutes = ['/liturgy/', '/liturgy/day.html'];
  state.phase = 'after';
  try {
    for (const route of protectedRoutes) {
      const relativePath = route.endsWith('/') ? `${route.slice(1)}index.html` : route.slice(1);
      const expected = await readFile(join(PREVIEW, relativePath));
      const response = await fetch(`${base}${PROJECT_PREFIX}${route}`);
      const actual = Buffer.from(await response.arrayBuffer());
      const injected = actual.includes(Buffer.from('data-wave1-prototype-'));
      rows.push(assertion(`protected-${route === '/liturgy/' ? 'liturgy-index' : 'liturgy-day'}-byte-identity`,
        response.status === 200 && actual.equals(expected) && !injected,
      `${route} status=${response.status} bytes=${actual.length} injected=${injected}`, true));
    }
  } finally {
    state.phase = 'before';
  }
  return rows;
}

async function waitForJson(url, attempts = 240) {
  for (let attempt = 0; attempt < attempts; attempt += 1) {
    try {
      const response = await fetch(url);
      if (response.ok) return await response.json();
    } catch (_error) {
      // Chromium has not opened its debugging endpoint yet.
    }
    await new Promise((accept) => setTimeout(accept, 50));
  }
  throw new Error(`Chromium debugging endpoint did not become ready: ${url}`);
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
      for (const listener of this.events.get(message.method) || []) listener(message.params || {});
    });
  }

  on(name, listener) {
    if (!this.events.has(name)) this.events.set(name, []);
    this.events.get(name).push(listener);
  }

  once(name, timeoutMs = SETTLE_TIMEOUT_MS) {
    return new Promise((accept, reject) => {
      const listener = (params) => {
        clearTimeout(timer);
        const held = this.events.get(name) || [];
        this.events.set(name, held.filter((one) => one !== listener));
        accept(params);
      };
      const timer = setTimeout(() => {
        const held = this.events.get(name) || [];
        this.events.set(name, held.filter((one) => one !== listener));
        reject(new Error(`timed out waiting for CDP event: ${name}`));
      }, timeoutMs);
      this.on(name, listener);
    });
  }

  send(method, params = {}) {
    const id = ++this.next;
    return new Promise((accept, reject) => {
      const timer = setTimeout(() => {
        this.pending.delete(id);
        reject(new Error(`CDP command timed out: ${method}`));
      }, 20000);
      this.pending.set(id, { accept, reject, timer });
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

async function waitFor(cdp, expression, label, attempts = 200) {
  for (let attempt = 0; attempt < attempts; attempt += 1) {
    if (await evaluate(cdp, `Boolean(${expression})`)) return;
    await new Promise((accept) => setTimeout(accept, 50));
  }
  throw new Error(`timed out waiting for ${label}`);
}

function newChannel() {
  return {
    console: [], exceptions: [], failed: [], badStatus: [], external: [],
    requests: new Map(), requested: new Set(), inflight: 0
  };
}

function clearChannel(channel) {
  channel.console.length = 0;
  channel.exceptions.length = 0;
  channel.failed.length = 0;
  channel.badStatus.length = 0;
  channel.external.length = 0;
  channel.requests.clear();
  channel.requested.clear();
  channel.inflight = 0;
}

async function settle(cdp, channel, readySelector) {
  const deadline = Date.now() + SETTLE_TIMEOUT_MS;
  let stable = 0;
  let previous = null;
  let lastFacts = null;
  while (Date.now() < deadline) {
    const facts = await evaluate(cdp, `(() => {
      const ready = document.querySelector(${JSON.stringify(readySelector)});
      const images = [...document.images].every(image => image.complete);
      return {
        complete: document.readyState === 'complete',
        ready: Boolean(ready && ready.getClientRects().length),
        images,
        width: document.documentElement.scrollWidth,
        height: document.documentElement.scrollHeight
      };
    })()`);
    lastFacts = facts;
    const signature = `${facts.width}x${facts.height}`;
    stable = facts.complete && facts.ready && facts.images && channel.inflight === 0 && signature === previous
      ? stable + 1 : 0;
    previous = signature;
    if (stable >= 3) {
      await evaluate(cdp, `document.fonts ? document.fonts.ready.then(() => true) : true`);
      await evaluate(cdp, `new Promise(resolve => requestAnimationFrame(() => requestAnimationFrame(resolve)))`);
      return;
    }
    await new Promise((accept) => setTimeout(accept, 80));
  }
  const pending = [...channel.requests.values()].slice(0, 8);
  throw new Error(`page did not settle within ${SETTLE_TIMEOUT_MS}ms: ` +
    `ready=${lastFacts?.ready} complete=${lastFacts?.complete} images=${lastFacts?.images} ` +
    `stable=${stable} inflight=${channel.inflight} size=${previous} pending=${JSON.stringify(pending)}`);
}

async function stabilizeInteraction(cdp, readySelector) {
  let ready = false;
  for (let attempt = 0; attempt < 40; attempt += 1) {
    ready = await evaluate(cdp,
      `document.querySelector(${JSON.stringify(readySelector)})?.getClientRects().length > 0`);
    if (ready) break;
    await new Promise((accept) => setTimeout(accept, 50));
  }
  await evaluate(cdp, `document.fonts ? document.fonts.ready.then(() => true) : true`);
  await evaluate(cdp, `new Promise(resolve => requestAnimationFrame(() => requestAnimationFrame(resolve)))`);
  return ready;
}

async function navigate(cdp, url) {
  const loaded = cdp.once('Page.loadEventFired');
  const result = await cdp.send('Page.navigate', { url });
  if (result.errorText) throw new Error(`navigation failed: ${result.errorText}`);
  await loaded;
}

async function dispatchKey(cdp, key) {
  const codes = {
    Tab: ['Tab', 9], Escape: ['Escape', 27], Enter: ['Enter', 13],
    ' ': ['Space', 32], Space: ['Space', 32], ArrowDown: ['ArrowDown', 40],
    ArrowUp: ['ArrowUp', 38], Home: ['Home', 36], End: ['End', 35]
  };
  const [code, number] = codes[key] || [key, key.length === 1 ? key.toUpperCase().charCodeAt(0) : 0];
  for (const type of ['keyDown', 'keyUp']) {
    await cdp.send('Input.dispatchKeyEvent', {
      type, key: key === 'Space' ? ' ' : key, code,
      windowsVirtualKeyCode: number, nativeVirtualKeyCode: number
    });
  }
}

async function performAction(cdp, action) {
  if (action.op === 'wait') {
    await waitFor(cdp,
      `document.querySelector(${JSON.stringify(action.selector)})?.getClientRects().length > 0`,
      `visible ${action.selector}`);
    return;
  }
  if (action.op === 'wait-text') {
    const conditions = [
      `document.querySelector(${JSON.stringify(action.selector)})?.getClientRects().length > 0`
    ];
    if (typeof action.text === 'string') {
      conditions.push(`document.querySelector(${JSON.stringify(action.selector)})?.textContent.includes(${JSON.stringify(action.text)})`);
    }
    if (typeof action.absent === 'string') {
      conditions.push(`!document.querySelector(${JSON.stringify(action.selector)})?.textContent.includes(${JSON.stringify(action.absent)})`);
    }
    await waitFor(cdp, conditions.join(' && '), `settled text in ${action.selector}`);
    return;
  }
  if (action.op === 'tab') {
    for (let step = 0; step < (action.count || 1); step += 1) await dispatchKey(cdp, 'Tab');
    return;
  }
  if (action.op === 'key') {
    await dispatchKey(cdp, action.key);
    return;
  }
  await evaluate(cdp, `(() => {
    const node = document.querySelector(${JSON.stringify(action.selector)});
    if (!node) throw new Error('missing action selector: ' + ${JSON.stringify(action.selector)});
    if (${JSON.stringify(action.op)} === 'click') { node.focus({preventScroll: true}); node.click(); }
    if (${JSON.stringify(action.op)} === 'focus') node.focus({preventScroll: true});
    if (${JSON.stringify(action.op)} === 'type') {
      node.focus({preventScroll: true});
      node.value = ${JSON.stringify(action.value || '')};
      node.dispatchEvent(new InputEvent('input', {bubbles: true, inputType: 'insertText', data: null}));
      node.dispatchEvent(new Event('change', {bubbles: true}));
    }
    if (${JSON.stringify(action.op)} === 'scroll') {
      document.documentElement.style.scrollBehavior = 'auto';
      const box = node.getBoundingClientRect();
      const block = ${JSON.stringify(action.block || 'center')};
      let top = window.scrollY + box.top;
      if (block === 'center') top -= (window.innerHeight - box.height) / 2;
      if (block === 'end') top -= window.innerHeight - box.height;
      window.scrollTo({top: Math.max(0, top), left: window.scrollX, behavior: 'instant'});
    }
    return true;
  })()`);
}

async function applyCaseState(cdp, held) {
  await cdp.send('Emulation.setScriptExecutionDisabled', { value: false });
  await cdp.send('Emulation.setPageScaleFactor', { pageScaleFactor: 1 });
  await cdp.send('Emulation.setDeviceMetricsOverride', {
    width: held.viewport.width, height: held.viewport.height,
    deviceScaleFactor: 1, mobile: false,
    screenWidth: held.viewport.width, screenHeight: held.viewport.height
  });
  const features = [];
  if (held.emulation === 'forced-colors') features.push({ name: 'forced-colors', value: 'active' });
  if (held.emulation === 'reduced-motion') {
    features.push({ name: 'prefers-reduced-motion', value: 'reduce' });
  }
  await cdp.send('Emulation.setEmulatedMedia', {
    media: held.emulation === 'print' ? 'print' : 'screen', features
  });
  await cdp.send('Emulation.setLocaleOverride', { locale: 'en-US' });
  await cdp.send('Emulation.setTimezoneOverride', { timezoneId: 'UTC' });
}

async function pageFacts(cdp, held) {
  return evaluate(cdp, `(() => {
    const useful = document.querySelector(${JSON.stringify(held.expect.useful)});
    const usefulBox = useful?.getBoundingClientRect();
    const active = document.activeElement;
    const activeBox = active?.getBoundingClientRect();
    const activeStyle = active ? getComputedStyle(active) : null;
    let unobscured = null;
    if (activeBox && activeBox.width > 0 && activeBox.height > 0) {
      const x = Math.max(0, Math.min(innerWidth - 1, activeBox.left + activeBox.width / 2));
      const y = Math.max(0, Math.min(innerHeight - 1, activeBox.top + activeBox.height / 2));
      const hit = document.elementFromPoint(x, y);
      unobscured = Boolean(hit && (hit === active || active.contains(hit) || hit.contains(active)));
    }
    const targets = ${JSON.stringify(held.expect.primaryTargets)}.flatMap(selector =>
      [...document.querySelectorAll(selector)].map(node => {
        const box = node.getBoundingClientRect();
        return {selector, visible: node.getClientRects().length > 0, width: box.width, height: box.height,
          text: (node.getAttribute('aria-label') || node.textContent || '').trim().slice(0, 80)};
      })
    );
    const links = ${JSON.stringify(held.expect.links)}.map(expected => {
      const node = document.querySelector(expected.selector);
      if (!node) return {...expected, actual: null};
      const url = new URL(node.href, location.href);
      const pathname = url.pathname === ${JSON.stringify(PROJECT_PREFIX)}
        ? '/' : url.pathname.slice(${PROJECT_PREFIX.length});
      return {...expected, actual: pathname + url.search + url.hash};
    });
    const exactText = ${JSON.stringify(held.expect.exactText)}.map(expected => {
      const node = document.querySelector(expected.selector);
      return {...expected, actual: node ? node.textContent.trim() : null};
    });
    const recordData = document.documentElement.dataset;
    const publicationRecord = recordData.waveRecordProvider ? {
      provider: {id: recordData.waveRecordProvider, label: recordData.waveRecordProviderLabel || ''},
      pdfHref: recordData.waveRecordPdf || '',
      parallel: recordData.waveRecordParallelWeb ? {
        provider: {id: recordData.waveRecordParallelProvider || '',
          label: recordData.waveRecordParallelLabel || ''},
        webHref: recordData.waveRecordParallelWeb
      } : null
    } : null;
    const outerMain = document.querySelector('main');
    const firstHeading = document.querySelector('h1');
    const skip = document.querySelector('a.skip-link[href^="#"]');
    let skipTarget = null;
    try { skipTarget = skip ? document.getElementById(decodeURIComponent(skip.hash.slice(1))) : null; }
    catch (_error) { skipTarget = null; }
    return {
      pathname: location.pathname, search: location.search, hash: location.hash,
      expectedReady: Boolean(document.querySelector(${JSON.stringify(held.expect.ready)})?.getClientRects().length),
      phaseMarker: document.documentElement.dataset.wave1PrototypePhase || null,
      injectedCss: Boolean(document.querySelector('[data-wave1-prototype-css]')),
      injectedJs: Boolean(document.querySelector('[data-wave1-prototype-js]')),
      prototypeRan: document.documentElement.hasAttribute('data-corpus-wave1') ||
        document.documentElement.hasAttribute('data-corpus-wave1-pending'),
      publicationRecord,
      readerRecordPresentation: (() => {
        const provider = document.querySelector('[data-wave-provider]');
        const routeHref = (selector) => {
          const node = document.querySelector(selector);
          if (!node) return null;
          const url = new URL(node.href, location.href);
          return url.pathname + url.search + url.hash;
        };
        return {
          providerText: provider?.textContent?.trim() || null,
          providerVisible: Boolean(provider?.getClientRects().length),
          pdfHref: routeHref('[data-wave-pdf]'),
          parallelHref: routeHref('[data-wave-parallel]')
        };
      })(),
      readerColophon: (() => {
        const action = document.querySelector('[data-wave-action="colophon"]');
        const target = document.getElementById('revision-and-rights');
        const article = target?.closest('[data-wave-reader-document]');
        const normalize = (node) => (node?.textContent || '').replace(/\\s+/gu, ' ').trim();
        const paragraphs = [...(target?.children || [])].filter((node) => node.matches('p'));
        const revision = paragraphs.find((node) => normalize(node).startsWith('Last revised (UTC):'));
        const rights = paragraphs.find((node) => normalize(node).startsWith('Reuse and rights.'));
        const noteBlocks = [...(article?.children || [])].filter((node) =>
          node.matches('.footnote, .footnotes, .endnotes, [role="doc-endnotes"]'));
        const lastNote = noteBlocks.at(-1) || null;
        const url = action ? new URL(action.href, location.href) : null;
        return {
          actionExists: Boolean(action),
          href: url ? url.pathname + url.search + url.hash : null,
          targetExists: Boolean(target?.matches('[data-wave-object="colophon"]')),
          resolves: Boolean(target && url && url.pathname === location.pathname &&
            url.search === location.search && url.hash === '#revision-and-rights'),
          targetLast: Boolean(article && article.lastElementChild === target),
          noteBlocks: noteBlocks.length,
          notesImmediatelyBefore: Boolean(!noteBlocks.length || (lastNote === target?.previousElementSibling &&
            noteBlocks.every((note) => note.compareDocumentPosition(target) & Node.DOCUMENT_POSITION_FOLLOWING))),
          revisionText: normalize(revision),
          revisionExact: /^Last revised \\(UTC\\): \\d{4}-\\d{2}-\\d{2}T\\d{2}:\\d{2}:\\d{2}Z$/.test(normalize(revision)),
          rightsExact: normalize(rights) === ${JSON.stringify(REUSE_RIGHTS_TEXT)},
          paragraphCount: paragraphs.length
        };
      })(),
      contentsCurrent: [...document.querySelectorAll(
        '[data-wave-contents-target][aria-current="location"]'
      )].map((node) => node.getAttribute('data-wave-contents-target')),
      printMedia: matchMedia('print').matches,
      visualViewport: window.visualViewport ? {
        width: window.visualViewport.width, height: window.visualViewport.height,
        scale: window.visualViewport.scale
      } : null,
      printChromeVisible: [...document.querySelectorAll(
        '[data-wave-shell-actions], dialog[data-wave-dialog-owner], [data-wave-open-dialog]'
      )].filter(node => node.getClientRects().length > 0).length,
      mainCount: document.querySelectorAll('main').length,
      h1Count: document.querySelectorAll('h1').length,
      h1InsideOuterMain: Boolean(outerMain && firstHeading && outerMain.contains(firstHeading)),
      skipTargetsOuterMain: Boolean(outerMain && skipTarget === outerMain),
      rootOverflow: document.documentElement.scrollWidth - document.documentElement.clientWidth,
      bodyOverflow: document.body.scrollWidth - document.body.clientWidth,
      layoutWidths: (() => {
        const metric = (node) => {
          if (!node) return null;
          const box = node.getBoundingClientRect();
          return {left: box.left, right: box.right, width: box.width,
            clientWidth: node.clientWidth, scrollWidth: node.scrollWidth,
            overflowX: getComputedStyle(node).overflowX};
        };
        const outsideOverflowNodes = [...document.querySelectorAll('body *')].filter((node) =>
          !node.closest('[data-wave-table-scroll]')
        ).map((node) => {
          const box = node.getBoundingClientRect();
          return {name: node.id ? '#' + node.id : node.tagName.toLowerCase() +
            ((node.classList && node.classList[0]) ? '.' + node.classList[0] : ''),
          left: box.left, right: box.right, width: box.width};
        }).filter((row) => row.left < -1 || row.right > document.documentElement.clientWidth + 1)
          .slice(0, 20);
        return {
          documentElement: metric(document.documentElement),
          body: metric(document.body),
          surfaceMain: metric(document.querySelector('[data-wave-surface-main]')),
          readerArticle: metric(document.querySelector('[data-wave-reader-document]')),
          tableWrappers: [...document.querySelectorAll('[data-wave-table-scroll]')]
            .slice(0, 12).map(metric),
          outsideOverflowNodes
        };
      })(),
      readerOverflowDiagnostics: (() => {
        if (!${held.surface === 'reader' && held.emulation === 'text-200'}) return null;
        const article = document.querySelector('[data-wave-reader-document]');
        if (!article) return null;
        const name = (node) => node.tagName.toLowerCase() + (node.id ? '#' + node.id : '') +
          [...node.classList].slice(0, 2).map((one) => '.' + one).join('');
        const metric = (node) => {
          const box = node.getBoundingClientRect();
          const style = getComputedStyle(node);
          return {name: name(node), parent: node.parentElement ? name(node.parentElement) : null,
            left: box.left, right: box.right, width: box.width,
            clientWidth: node.clientWidth, scrollWidth: node.scrollWidth,
            overflowWidth: node.scrollWidth - node.clientWidth,
            display: style.display, whiteSpace: style.whiteSpace,
            overflowWrap: style.overflowWrap, wordBreak: style.wordBreak,
            overflowX: style.overflowX};
        };
        const all = [article, ...article.querySelectorAll('*')];
        const included = new Set();
        for (const node of all) {
          if (node.scrollWidth - node.clientWidth <= 1) continue;
          let cursor = node;
          while (cursor && article.contains(cursor)) {
            included.add(cursor);
            if (cursor === article) break;
            cursor = cursor.parentElement;
          }
        }
        return {
          overflowingWithAncestors: all.filter((node) => included.has(node)).map(metric),
          topLevelChildren: [...article.children].map(metric)
        };
      })(),
      overflowNodes: [...document.querySelectorAll('body *')].map(node => {
        const box = node.getBoundingClientRect();
        return {name: node.id ? '#' + node.id : node.tagName.toLowerCase() +
          ((node.classList && node.classList[0]) ? '.' + node.classList[0] : ''), left: box.left, right: box.right};
      }).filter(row => row.left < -1 || row.right > document.documentElement.clientWidth + 1).slice(0, 20),
      useful: useful ? {text: (useful.textContent || '').trim().length, top: usefulBox.top,
        bottom: usefulBox.bottom, visible: useful.getClientRects().length > 0 && usefulBox.bottom > 0 &&
          usefulBox.top < innerHeight} : null,
      targets,
      links,
      exactText,
      active: active ? {tag: active.tagName.toLowerCase(), id: active.id || null,
        visible: Boolean(activeBox && active.getClientRects().length && activeBox.width && activeBox.height),
        inViewport: Boolean(activeBox && activeBox.bottom > 0 && activeBox.top < innerHeight &&
          activeBox.right > 0 && activeBox.left < innerWidth),
        outlineWidth: activeStyle ? parseFloat(activeStyle.outlineWidth) || 0 : 0,
        outlineStyle: activeStyle?.outlineStyle || '', boxShadow: activeStyle?.boxShadow || '',
        unobscured} : null,
      focusMatches: ${held.expect.focus ? `Boolean(active?.matches(${JSON.stringify(held.expect.focus)}))` : 'null'},
      focusWithin: ${held.expect.focusWithin ? `Boolean(document.querySelector(${JSON.stringify(held.expect.focusWithin)})?.contains(active))` : 'null'},
      text: document.body.innerText,
      absentSelectorsPresent: ${JSON.stringify(held.expect.absentSelectors)}.filter(selector =>
        document.querySelector(selector)
      )
    };
  })()`);
}

async function axFacts(cdp) {
  const { nodes } = await cdp.send('Accessibility.getFullAXTree');
  const unnamed = nodes.filter((node) => {
    if (node.ignored) return false;
    const role = node.role?.value || '';
    return CONTROL_ROLES.has(role) && !(node.name?.value || '').trim();
  }).map((node) => ({ role: node.role?.value || '' }));
  return { nodeCount: nodes.length, unnamed };
}

function assertion(name, pass, detail, gating) {
  return { name, status: pass ? 'pass' : 'fail', gating, detail: detail || '' };
}

function projectRequest(url) {
  try {
    const parsed = new URL(url);
    if (parsed.pathname !== PROJECT_PREFIX && !parsed.pathname.startsWith(PROJECT_PREFIX + '/')) {
      return { path: parsed.origin + parsed.pathname + parsed.search, status: null };
    }
    const pathname = parsed.pathname === PROJECT_PREFIX
      ? '/' : parsed.pathname.slice(PROJECT_PREFIX.length);
    return { path: pathname + parsed.search, status: null };
  } catch (_error) {
    return { path: url, status: null };
  }
}

async function probePublication(base, publication) {
  if (!publication) return null;
  const pdf = await fetch(`${base}${publication.pdfPath}`, { method: 'HEAD' });
  let parallelStatus = null;
  if (publication.parallelPath) {
    parallelStatus = (await fetch(`${base}${publication.parallelPath}`, { method: 'HEAD' })).status;
  }
  return { pdfStatus: pdf.status, parallelStatus };
}

function recordAssertions(
  held, facts, ax, channel, expectedRoute, rootFontRatio, publication, publicationProbe,
  baselineMainCount
) {
  const gating = held.phase === 'after';
  const rows = [];
  const expected = new URL(`${PROJECT_PREFIX}${expectedRoute}`, 'https://invalid.example');
  const routePass = facts.pathname === expected.pathname && facts.search === expected.search &&
    facts.hash === expected.hash;
  const inherited = held.expect.inheritedRoute
    ? new URL(`${PROJECT_PREFIX}${held.expect.inheritedRoute.route}`, 'https://invalid.example') : null;
  const inheritedPass = !routePass && inherited && facts.pathname === inherited.pathname &&
    facts.search === inherited.search && facts.hash === inherited.hash;
  rows.push(assertion('route-preserved', routePass,
    inheritedPass
      ? `inherited production normalization: ${held.expect.inheritedRoute.reason}; ` +
        `actual=${facts.pathname}${facts.search}${facts.hash}`
      : `${facts.pathname}${facts.search}${facts.hash}`,
    inheritedPass ? false : gating));
  rows.push(assertion('prototype-phase-correct', held.phase === 'after'
    ? facts.phaseMarker === 'after' && facts.injectedCss && facts.injectedJs
    : !facts.phaseMarker && !facts.injectedCss && !facts.injectedJs,
  `marker=${facts.phaseMarker || 'none'} css=${facts.injectedCss} js=${facts.injectedJs}`, true));
  if (held.surface === 'reader') {
    if (held.phase === 'before') {
      rows.push(assertion('reader-record-not-injected-before', facts.publicationRecord === null,
        JSON.stringify(facts.publicationRecord), true));
    } else {
      const routeProvider = held.route.match(/^\/web\/([^/]+)\//)?.[1] || null;
      const payloadExact = publication && JSON.stringify(facts.publicationRecord) ===
        JSON.stringify(publication.payload);
      rows.push(assertion('reader-record-injected-exactly', Boolean(payloadExact),
        JSON.stringify(facts.publicationRecord), true));
      rows.push(assertion('reader-record-provider-matches-route', Boolean(publication &&
        publication.routeProvider === routeProvider && facts.publicationRecord?.provider?.id === routeProvider),
      `route=${routeProvider} record=${facts.publicationRecord?.provider?.id || 'none'}`, true));
      rows.push(assertion('reader-record-pdf-same-provider', Boolean(publication &&
        facts.publicationRecord?.pdfHref?.startsWith(`${PROJECT_PREFIX}/pdf/${routeProvider}/`)),
      facts.publicationRecord?.pdfHref || 'none', true));
      rows.push(assertion('reader-record-pdf-http-200', publicationProbe?.pdfStatus === 200,
        `status=${publicationProbe?.pdfStatus ?? 'not-probed'}`, true));
      const providerVisible = facts.readerRecordPresentation.providerText ===
        `Provider · ${publication?.payload.provider.label}` &&
        facts.readerRecordPresentation.providerVisible === true;
      const providerOverlayLimitation = held.expect.inheritedOverlay?.assertions.includes(
        'reader-record-visible-provider'
      );
      rows.push(assertion('reader-record-visible-provider', providerVisible,
        providerOverlayLimitation && !providerVisible
          ? `inherited overlay limitation: ${held.expect.inheritedOverlay.reason} ` +
            JSON.stringify(facts.readerRecordPresentation)
          : JSON.stringify(facts.readerRecordPresentation),
      !providerOverlayLimitation));
      const pdfVisible = facts.readerRecordPresentation.pdfHref === publication?.payload.pdfHref;
      const pdfOverlayLimitation = held.expect.inheritedOverlay?.assertions.includes(
        'reader-record-visible-pdf'
      );
      rows.push(assertion('reader-record-visible-pdf', pdfVisible,
        pdfOverlayLimitation && !pdfVisible
          ? `inherited overlay limitation: ${held.expect.inheritedOverlay.reason} ` +
            (facts.readerRecordPresentation.pdfHref || 'none')
          : (facts.readerRecordPresentation.pdfHref || 'none'),
      !pdfOverlayLimitation));
      const parallel = facts.publicationRecord?.parallel;
      const parallelPass = !parallel || Boolean(publication &&
        parallel.webHref?.startsWith(`${PROJECT_PREFIX}/web/${parallel.provider?.id}/`) &&
        parallel.provider?.id !== routeProvider && publicationProbe?.parallelStatus === 200);
      rows.push(assertion('reader-record-parallel-verified', parallelPass,
        parallel ? `provider=${parallel.provider?.id} status=${publicationProbe?.parallelStatus}` : 'none recorded',
      true));
      if (held.emulation !== 'no-js') {
        rows.push(assertion('reader-colophon-action-target', facts.readerColophon.actionExists &&
          facts.readerColophon.targetExists && facts.readerColophon.resolves,
        JSON.stringify(facts.readerColophon), true));
        rows.push(assertion('reader-colophon-terminal-order', facts.readerColophon.targetLast &&
          facts.readerColophon.notesImmediatelyBefore,
        JSON.stringify(facts.readerColophon), true));
        rows.push(assertion('reader-colophon-exact-paragraphs', facts.readerColophon.revisionExact &&
          facts.readerColophon.rightsExact && facts.readerColophon.paragraphCount === 2,
        JSON.stringify(facts.readerColophon), true));
      }
      if (held.expect.currentContents) {
        rows.push(assertion('reader-current-contents-locus',
          facts.contentsCurrent.length === 1 && facts.contentsCurrent[0] === held.expect.currentContents,
        JSON.stringify(facts.contentsCurrent), true));
      }
    }
  }
  rows.push(assertion('console-clean', channel.console.length === 0,
    channel.console.slice(0, 8).join(' | '), true));
  rows.push(assertion('runtime-clean', channel.exceptions.length === 0,
    channel.exceptions.slice(0, 8).join(' | '), true));
  rows.push(assertion('request-clean', channel.failed.length === 0,
    channel.failed.slice(0, 8).map((row) => `${row.error}: ${row.url}`).join(' | '), true));
  const observedHttp = channel.badStatus.map((row) => ({
    ...projectRequest(row.url), status: row.status
  }));
  const allowedKeys = new Set(held.expect.allowedHttp.map((row) => `${row.status} ${row.path}`));
  const observedKeys = new Set(observedHttp.map((row) => `${row.status} ${row.path}`));
  const unexpectedHttp = observedHttp.filter((row) => !allowedKeys.has(`${row.status} ${row.path}`));
  const missingHttp = held.expect.allowedHttp.filter((row) => !observedKeys.has(`${row.status} ${row.path}`));
  rows.push(assertion('http-clean', unexpectedHttp.length === 0 && missingHttp.length === 0,
    JSON.stringify({ expectedObserved: observedHttp.filter((row) =>
      allowedKeys.has(`${row.status} ${row.path}`)), unexpected: unexpectedHttp, missing: missingHttp }), true));
  const requestedPaths = new Set([...channel.requested].map((url) => projectRequest(url).path));
  const missingRequests = held.expect.requests.filter((one) => !requestedPaths.has(one));
  rows.push(assertion('expected-requests-observed', missingRequests.length === 0,
    JSON.stringify(missingRequests), gating));
  rows.push(assertion('same-origin-triptych-only', channel.external.length === 0,
    channel.external.slice(0, 8).join(' | '), true));
  rows.push(assertion('expected-ready-visible', facts.expectedReady === true,
    held.expect.ready, gating));
  const inheritedNestedMain = INHERITED_NESTED_MAIN_SURFACES.has(held.surface);
  rows.push(assertion('one-main', facts.mainCount === 1, `found ${facts.mainCount}`,
    inheritedNestedMain ? false : gating));
  if (held.phase === 'after' && inheritedNestedMain) {
    rows.push(assertion('main-count-no-regression', Number.isInteger(baselineMainCount) &&
      facts.mainCount === baselineMainCount,
    `before=${baselineMainCount ?? 'missing'} after=${facts.mainCount}`, true));
  }
  rows.push(assertion('one-h1', facts.h1Count === 1, `found ${facts.h1Count}`, gating));
  rows.push(assertion('h1-inside-outer-main', facts.h1InsideOuterMain === true,
    `inside=${facts.h1InsideOuterMain}`, gating));
  rows.push(assertion('skip-target-is-outer-main', facts.skipTargetsOuterMain === true,
    `targetsOuter=${facts.skipTargetsOuterMain}`, gating));
  rows.push(assertion('interactive-ax-names', ax.unnamed.length === 0,
    ax.unnamed.slice(0, 8).map((row) => row.role).join(', '), gating));
  rows.push(assertion('no-page-overflow',
    facts.rootOverflow <= OVERFLOW_TOLERANCE_PX && facts.bodyOverflow <= OVERFLOW_TOLERANCE_PX,
    `root=${facts.rootOverflow}px body=${facts.bodyOverflow}px ` +
      `layout=${JSON.stringify(facts.layoutWidths)} ` +
      `reader=${JSON.stringify(facts.readerOverflowDiagnostics)} ` +
      `nodes=${JSON.stringify(facts.overflowNodes)}`, gating));
  rows.push(assertion('useful-content-visible', Boolean(facts.useful?.visible && facts.useful.text > 0),
    JSON.stringify(facts.useful), gating));
  const badTargets = facts.targets.filter((target) => target.visible &&
    (target.width < 43.5 || target.height < 43.5));
  const targetSelectorsFound = new Set(facts.targets.map((target) => target.selector));
  const missingTargets = held.expect.primaryTargets.filter((one) => !targetSelectorsFound.has(one));
  rows.push(assertion('primary-targets-44px', badTargets.length === 0 && missingTargets.length === 0,
    JSON.stringify({ badTargets, missingTargets }), gating));
  const badLinks = facts.links.filter((one) => one.actual !== one.href);
  rows.push(assertion('expected-links-resolve', badLinks.length === 0,
    JSON.stringify(badLinks), gating));
  const badExactText = facts.exactText.filter((one) => one.actual !== one.text);
  rows.push(assertion('expected-exact-text', badExactText.length === 0,
    JSON.stringify(badExactText), gating));
  if (held.emulation === 'text-200') {
    rows.push(assertion('text-enlarged-200-percent', rootFontRatio >= 1.99,
      `computed ratio=${rootFontRatio}`, gating));
  }
  if (held.emulation === 'reflow-400') {
    rows.push(assertion('reflow-400-equivalent', held.viewport.width === 320,
      '320 CSS pixels is the 1280px/400% reflow equivalent; no pageScaleFactor claim', gating));
  }
  if (held.emulation === 'forced-colors') {
    rows.push(assertion('forced-colors-active', facts.forcedColors === true,
      `matchMedia=${facts.forcedColors}`, gating));
  }
  if (held.emulation === 'reduced-motion') {
    rows.push(assertion('reduced-motion-active', facts.reducedMotion === true,
      `matchMedia=${facts.reducedMotion}`, gating));
  }
  if (held.emulation === 'print') {
    rows.push(assertion('print-media-active', facts.printMedia === true,
      `matchMedia=${facts.printMedia}`, gating));
    rows.push(assertion('print-interactive-chrome-hidden', facts.printChromeVisible === 0,
      `visible print chrome=${facts.printChromeVisible}`, gating));
  }
  if (held.emulation === 'zoom-400') {
    rows.push(assertion('page-scale-400-percent', facts.visualViewport?.scale >= 3.99,
      JSON.stringify(facts.visualViewport), gating));
  }
  if (held.emulation === 'no-js') {
    rows.push(assertion('prototype-javascript-disabled', facts.prototypeRan === false,
      `prototypeRan=${facts.prototypeRan}`, true));
  }
  if (held.expect.focus || held.expect.focusWithin || held.emulation === 'keyboard') {
    if (held.expect.focus) rows.push(assertion('expected-focus', facts.focusMatches === true,
      JSON.stringify(facts.active), gating));
    if (held.expect.focusWithin) rows.push(assertion('focus-within', facts.focusWithin === true,
      JSON.stringify(facts.active), gating));
    if (held.expect.focus || held.emulation === 'keyboard') {
      const visibleFocus = facts.active?.visible && facts.active?.inViewport && facts.active?.unobscured &&
        ((facts.active.outlineWidth >= 2 && facts.active.outlineStyle !== 'none') ||
         (facts.active.boxShadow && facts.active.boxShadow !== 'none'));
      rows.push(assertion('focus-visible-and-unobscured', Boolean(visibleFocus),
        JSON.stringify(facts.active), gating));
    }
  }
  for (const text of held.expect.text) {
    rows.push(assertion('expected-text-present', facts.text.includes(text), JSON.stringify(text), gating));
  }
  for (const text of held.expect.absentText) {
    rows.push(assertion('forbidden-text-absent', !facts.text.includes(text), JSON.stringify(text), gating));
  }
  rows.push(assertion('forbidden-selectors-absent', facts.absentSelectorsPresent.length === 0,
    JSON.stringify(facts.absentSelectorsPresent), gating));
  return rows;
}

async function runCase(
  cdp, base, held, serverState, channel, captureDir, number, baselineMainCount
) {
  await navigate(cdp, 'about:blank');
  await applyCaseState(cdp, held);
  serverState.phase = held.phase;
  const routePath = new URL(held.route, 'https://invalid.example').pathname;
  const publication = serverState.publications.get(routePath) || null;
  const publicationProbe = held.phase === 'after' && held.surface === 'reader'
    ? await probePublication(base, publication) : null;
  clearChannel(channel);
  const target = `${base}${PROJECT_PREFIX}${held.route}`;
  if (held.emulation === 'no-js') {
    await cdp.send('Emulation.setScriptExecutionDisabled', { value: true });
  }
  try {
    await navigate(cdp, target);
  } finally {
    if (held.emulation === 'no-js') {
      await cdp.send('Emulation.setScriptExecutionDisabled', { value: false });
    }
  }
  if (held.emulation === 'zoom-400') {
    await cdp.send('Emulation.setPageScaleFactor', { pageScaleFactor: 4 });
  }
  const initialReady = held.phase === 'after' && held.emulation !== 'no-js'
    ? 'body[data-wave-ready]' : 'main';
  await settle(cdp, channel, initialReady);

  let rootFontRatio = 1;
  if (held.emulation === 'text-200') {
    const before = await evaluate(cdp, `parseFloat(getComputedStyle(document.documentElement).fontSize)`);
    await evaluate(cdp, `document.documentElement.style.fontSize = ${JSON.stringify(`${before * 2}px`)}`);
    await settle(cdp, channel, initialReady);
    const after = await evaluate(cdp, `parseFloat(getComputedStyle(document.documentElement).fontSize)`);
    rootFontRatio = after / before;
  }

  if (held.emulation === 'keyboard' && !held.actions.some((action) => action.op === 'tab')) {
    await dispatchKey(cdp, 'Tab');
  }
  for (const action of held.actions) await performAction(cdp, action);
  await stabilizeInteraction(cdp, held.expect.ready);
  // Controllers may finish a final render after an action and restore their own
  // scroll position. Reapply only declarative evidence framing once the case is
  // settled so captures show the exact object the matrix names.
  for (const action of held.actions.filter((one) => one.op === 'scroll')) {
    await performAction(cdp, action);
  }

  const facts = await pageFacts(cdp, held);
  facts.forcedColors = await evaluate(cdp, `matchMedia('(forced-colors: active)').matches`);
  facts.reducedMotion = await evaluate(cdp, `matchMedia('(prefers-reduced-motion: reduce)').matches`);
  const ax = await axFacts(cdp);
  const assertions = recordAssertions(
    held, facts, ax, channel, held.route, rootFontRatio, publication, publicationProbe,
    baselineMainCount
  );

  let capture = null;
  let printEvidence = null;
  if (captureDir) {
    const captureStem = `${String(number).padStart(3, '0')}-${held.id}`;
    capture = `${captureStem}.png`;
    const image = await cdp.send('Page.captureScreenshot', {
      format: 'png', captureBeyondViewport: false, fromSurface: true
    });
    await writeFile(join(captureDir, capture), Buffer.from(image.data, 'base64'));
    if (held.emulation === 'print') {
      printEvidence = await renderPrintEvidence(
        cdp, captureDir, captureStem, held.expect.printText
      );
      assertions.push(...printEvidence.assertions);
      delete printEvidence.assertions;
    }
  }

  if (held.expect.restoreFocusAfterEscape) {
    await dispatchKey(cdp, 'Escape');
    await waitFor(cdp,
      `document.activeElement?.matches(${JSON.stringify(held.expect.restoreFocusAfterEscape)})`,
      `focus restoration to ${held.expect.restoreFocusAfterEscape}`);
    const restored = await evaluate(cdp,
      `document.activeElement?.matches(${JSON.stringify(held.expect.restoreFocusAfterEscape)}) === true`);
    assertions.push(assertion('focus-restored-after-escape', restored,
      held.expect.restoreFocusAfterEscape, held.phase === 'after'));
  }

  if (held.expect.closeAndRestore) {
    const close = held.expect.closeAndRestore;
    const closeReady = await evaluate(cdp,
      `document.activeElement?.matches(${JSON.stringify(close.control)}) === true`);
    assertions.push(assertion('publication-detail-close-focused', closeReady,
      close.control, held.phase === 'after'));
    await performAction(cdp, { op: 'click', selector: close.control });
    await waitFor(cdp, `(() => {
      const node = document.querySelector(${JSON.stringify(close.hidden)});
      return !node || node.hidden || node.getClientRects().length === 0;
    })()`, `closed ${close.hidden}`);
    const restored = await evaluate(cdp, `(() => {
      const origin = document.querySelector(${JSON.stringify(close.origin)});
      const active = document.activeElement;
      const box = active?.getBoundingClientRect();
      let unobscured = false;
      if (box && box.width > 0 && box.height > 0) {
        const x = Math.max(0, Math.min(innerWidth - 1, box.left + box.width / 2));
        const y = Math.max(0, Math.min(innerHeight - 1, box.top + box.height / 2));
        const hit = document.elementFromPoint(x, y);
        unobscured = Boolean(hit && (hit === active || active.contains(hit) || hit.contains(active)));
      }
      return {sameOrigin: Boolean(origin && active === origin), hidden: Boolean(
        !document.querySelector(${JSON.stringify(close.hidden)}) ||
        document.querySelector(${JSON.stringify(close.hidden)}).hidden ||
        document.querySelector(${JSON.stringify(close.hidden)}).getClientRects().length === 0
      ), visible: Boolean(active?.getClientRects().length), unobscured};
    })()`);
    assertions.push(assertion('publication-detail-close-activated', closeReady && restored.hidden,
      JSON.stringify(restored), held.phase === 'after'));
    assertions.push(assertion('publication-detail-focus-restored', restored.sameOrigin &&
      restored.visible && restored.unobscured,
    JSON.stringify(restored), held.phase === 'after'));
  }

  const requests = [...channel.requested].map((url) => {
    try {
      const parsed = new URL(url);
      return parsed.pathname + parsed.search;
    } catch (_error) {
      return url;
    }
  }).sort();
  const httpResponses = channel.badStatus.map((row) => ({
    ...projectRequest(row.url), status: row.status
  })).sort((left, right) => left.path.localeCompare(right.path) || left.status - right.status);
  return {
    id: held.id, surface: held.surface, phase: held.phase, route: held.route,
    viewport: `${held.viewport.width}x${held.viewport.height}`,
    emulation: held.emulation,
    capture,
    printEvidence,
    requests,
    httpResponses,
    measurements: {
      rootOverflowPx: facts.rootOverflow,
      bodyOverflowPx: facts.bodyOverflow,
      layoutWidths: facts.layoutWidths,
      readerOverflowDiagnostics: facts.readerOverflowDiagnostics,
      usefulTopPx: facts.useful?.top ?? null,
      usefulBottomPx: facts.useful?.bottom ?? null,
      axNodeCount: ax.nodeCount,
      mainCount: facts.mainCount,
      rootFontRatio,
      printMedia: facts.printMedia,
      visualViewport: facts.visualViewport
    },
    assertions
  };
}

function scrubString(value, base) {
  return String(value)
    .split(REPO).join('<repo>')
    .split(PREVIEW).join('<preview>')
    .split(base).join('');
}

function scrub(value, base) {
  if (typeof value === 'string') return scrubString(value, base);
  if (Array.isArray(value)) return value.map((one) => scrub(one, base));
  if (value && typeof value === 'object') {
    return Object.fromEntries(Object.entries(value).map(([key, held]) => [key, scrub(held, base)]));
  }
  return value;
}

async function command(commandName, args) {
  return new Promise((accept, reject) => {
    const child = spawn(commandName, args, { stdio: ['ignore', 'pipe', 'pipe'] });
    let stdout = '';
    let stderr = '';
    child.stdout.on('data', (chunk) => { stdout += chunk.toString(); });
    child.stderr.on('data', (chunk) => { stderr += chunk.toString(); });
    child.once('error', reject);
    child.once('exit', (code) => {
      if (code === 0) accept({ stdout, stderr });
      else reject(new Error(`${commandName} exited ${code}: ${stderr.trim()}`));
    });
  });
}

function normalizePrintText(value) {
  return value.normalize('NFKC').replace(/\s+/gu, ' ')
    .replace(/[\p{Dash_Punctuation}\u00ad\u2212]/gu, '').trim();
}

async function renderPrintEvidence(cdp, captureDir, captureStem, expectedText) {
  const pdfName = `${captureStem}.print.pdf`;
  const textName = `${captureStem}.print.txt`;
  const pagePrefix = `${captureStem}.print-page`;
  const pdfPath = join(captureDir, pdfName);
  const textPath = join(captureDir, textName);
  const printed = await cdp.send('Page.printToPDF', {
    printBackground: true, displayHeaderFooter: false, preferCSSPageSize: true,
    paperWidth: 8.27, paperHeight: 11.69,
    marginTop: 0.5, marginBottom: 0.5, marginLeft: 0.5, marginRight: 0.5
  });
  await writeFile(pdfPath, Buffer.from(printed.data, 'base64'));
  const info = await command('pdfinfo', [pdfPath]);
  const pageCount = Number(info.stdout.match(/^Pages:\s+(\d+)$/m)?.[1] || 0);
  if (!Number.isInteger(pageCount) || pageCount < 1) throw new Error('print PDF has no readable page count');
  await command('pdftotext', [pdfPath, textPath]);
  await command('pdftoppm', [
    '-png', '-scale-to', '320', '-f', '1', '-l', String(pageCount), pdfPath,
    join(captureDir, pagePrefix)
  ]);
  const pages = (await readdir(captureDir)).filter((name) =>
    name.startsWith(`${pagePrefix}-`) && name.endsWith('.png')
  ).sort((left, right) => left.localeCompare(right, undefined, { numeric: true }));
  const extracted = await readFile(textPath, 'utf8');
  const normalizedExtracted = normalizePrintText(extracted);
  const assertions = [
    assertion('print-pdf-generated', (await stat(pdfPath)).size > 0, pdfName, true),
    assertion('print-every-page-rastered', pages.length === pageCount,
      `pages=${pageCount} rasters=${pages.length}`, true)
  ];
  const orderedPositions = [];
  let orderedCursor = 0;
  for (const text of expectedText) {
    const normalizedExpected = normalizePrintText(text);
    const position = normalizedExtracted.indexOf(normalizedExpected, orderedCursor);
    orderedPositions.push({ text: normalizedExpected, position });
    if (position >= 0) orderedCursor = position + normalizedExpected.length;
    assertions.push(assertion('print-text-present', position >= 0,
      JSON.stringify(normalizedExpected), true));
  }
  assertions.push(assertion('print-text-order', orderedPositions.every((one) => one.position >= 0),
    JSON.stringify(orderedPositions), true));
  return { pdf: pdfName, extractedText: textName, pageCount, pages, assertions };
}

async function freshDirectory(path) {
  if (await exists(path)) {
    const entries = await readdir(path);
    if (entries.length) throw new Error(`capture directory is not empty: ${path}`);
  } else {
    await mkdir(path, { recursive: true });
  }
}

async function resolveChrome() {
  const named = process.env.TRIPTYCH_CHROME;
  const available = (command) => {
    const result = spawnSync(command, ['--version'], { stdio: 'ignore' });
    return !result.error && result.status === 0;
  };
  if (named) return available(named) ? named : null;
  for (const candidate of CHROME_CANDIDATES) if (available(candidate)) return candidate;
  return null;
}

async function stopChrome(chrome) {
  if (chrome.exitCode !== null || chrome.signalCode !== null) return;
  chrome.kill('SIGTERM');
  const exited = await Promise.race([
    new Promise((accept) => chrome.once('exit', () => accept(true))),
    new Promise((accept) => setTimeout(() => accept(false), 3000))
  ]);
  if (!exited && chrome.exitCode === null && chrome.signalCode === null) {
    chrome.kill('SIGKILL');
    await new Promise((accept) => chrome.once('exit', accept));
  }
}

async function main() {
  let options;
  try {
    options = parseArguments(process.argv.slice(2));
  } catch (error) {
    process.stderr.write(`${error.message}\n\n${usage()}`);
    process.exitCode = 2;
    return;
  }
  if (options.help) {
    process.stdout.write(usage());
    return;
  }

  let matrix;
  let publications;
  let inputHashes;
  try {
    matrix = await readMatrix(options.matrix);
    if (!(await exists(join(PREVIEW, 'index.html')))) {
      throw new Error('public preview is absent; run `make public-preview` first');
    }
    for (const path of [
      PROTOTYPE_FIXTURE, matrix.assets.css, matrix.assets.javascript, DOCUMENT_CORPUS
    ]) {
      const held = await stat(path);
      if (!held.isFile()) throw new Error(`prototype asset is not a file: ${relative(REPO, path)}`);
    }
    publications = await loadPublicationRecords();
    inputHashes = {
      matrixSha256: matrix.sha256,
      prototypeFixtureSha256: await sha256(PROTOTYPE_FIXTURE),
      prototypeCssSha256: await sha256(matrix.assets.css),
      prototypeJavascriptSha256: await sha256(matrix.assets.javascript),
      documentCorpusSha256: await sha256(DOCUMENT_CORPUS)
    };
    if (options.captureDir) await freshDirectory(options.captureDir);
  } catch (error) {
    process.stderr.write(scrubString(error.stack || String(error), '') + '\n');
    process.exitCode = 2;
    return;
  }

  const chromeBinary = await resolveChrome();
  if (!chromeBinary) {
    process.stderr.write('No Chromium binary found on PATH. Set TRIPTYCH_CHROME to a command or executable.\n');
    process.exitCode = 3;
    return;
  }

  const serverState = { phase: 'before', assets: matrix.assets, publications };
  const server = staticServer(serverState);
  const port = await listen(server);
  const base = `http://${LOOPBACK}:${port}`;
  const debugPort = await freePort();
  const profile = await mkdtemp(join(tmpdir(), 'triptych-corpus-wave1-chrome-'));
  const chrome = spawn(chromeBinary, [
    '--headless=new', '--no-sandbox', '--disable-dev-shm-usage', '--disable-gpu',
    '--disable-extensions', '--disable-component-extensions-with-background-pages',
    '--disable-background-networking', '--disable-component-update', '--disable-domain-reliability',
    '--disable-client-side-phishing-detection', '--disable-sync', '--no-pings',
    '--no-service-autorun', '--metrics-recording-only', '--password-store=basic',
    '--use-mock-keychain', '--mute-audio', '--force-color-profile=srgb', '--lang=en-US',
    '--disable-features=Translate,MediaRouter,OptimizationHints,InterestFeedContentSuggestions,PushMessaging',
    `--remote-debugging-port=${debugPort}`, `--user-data-dir=${profile}`,
    '--no-first-run', '--no-default-browser-check', 'about:blank'
  ], { stdio: ['ignore', 'ignore', 'pipe'] });
  let chromeStderr = '';
  chrome.stderr.on('data', (chunk) => { chromeStderr += chunk.toString(); });

  const channel = newChannel();
  const results = [];
  const serverAssertions = [];
  const baselineMainCounts = new Map();
  let cdp = null;
  try {
    const version = await waitForJson(`http://${LOOPBACK}:${debugPort}/json/version`);
    const page = await (await fetch(
      `http://${LOOPBACK}:${debugPort}/json/new?${encodeURIComponent('about:blank')}`,
      { method: 'PUT' }
    )).json();
    cdp = new CDP(page.webSocketDebuggerUrl);
    await cdp.ready();
    for (const domain of ['Page', 'Runtime', 'Network', 'Accessibility']) {
      await cdp.send(`${domain}.enable`);
    }
    await cdp.send('Network.setCacheDisabled', { cacheDisabled: true });
    await cdp.send('Network.setBypassServiceWorker', { bypass: true });
    serverAssertions.push(...await protectedSurfaceAssertions(base, serverState));
    cdp.on('Runtime.consoleAPICalled', ({ type, args }) => {
      if (!['warning', 'error', 'assert'].includes(type)) return;
      channel.console.push(`${type}: ` + args.map((arg) =>
        arg.value ?? arg.description ?? arg.unserializableValue ?? '').join(' '));
    });
    cdp.on('Runtime.exceptionThrown', ({ exceptionDetails }) => {
      channel.exceptions.push(exceptionDetails?.exception?.description || exceptionDetails?.text || 'exception');
    });
    cdp.on('Network.requestWillBeSent', ({ requestId, request }) => {
      if (!channel.requests.has(requestId)) channel.inflight += 1;
      channel.requests.set(requestId, request.url);
      channel.requested.add(request.url);
      try {
        const url = new URL(request.url);
        if (['http:', 'https:'].includes(url.protocol) &&
            (url.origin !== base || (url.pathname !== PROJECT_PREFIX &&
             !url.pathname.startsWith(PROJECT_PREFIX + '/')))) {
          channel.external.push(request.url);
        }
      } catch (_error) {
        // Non-network schemes cannot be external HTTP requests.
      }
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
      channel.failed.push({ url, error: event.errorText || 'load failed', canceled: Boolean(event.canceled) });
    });
    cdp.on('Network.responseReceived', ({ requestId, response }) => {
      if (response.status >= 400) {
        channel.badStatus.push({ status: response.status, url: response.url });
        finish(requestId);
      }
    });

    for (let index = 0; index < matrix.cases.length; index += 1) {
      const held = matrix.cases[index];
      try {
        const result = await runCase(
          cdp, base, held, serverState, channel, options.captureDir, index + 1,
          baselineMainCounts.get(held.surface)
        );
        results.push(result);
        if (held.phase === 'before' && Number.isInteger(result.measurements.mainCount) &&
            !baselineMainCounts.has(held.surface)) {
          baselineMainCounts.set(held.surface, result.measurements.mainCount);
        }
      } catch (error) {
        results.push({
          id: held.id, surface: held.surface, phase: held.phase, route: held.route,
          viewport: `${held.viewport.width}x${held.viewport.height}`, emulation: held.emulation,
          capture: null, printEvidence: null, requests: [], httpResponses: [], measurements: {}, assertions: [
            assertion('case-runs', false, error.message || String(error), true)
          ]
        });
      }
    }

    const flattened = [
      ...serverAssertions.map((one) => ({ case: 'server-boundary', phase: 'after', ...one })),
      ...results.flatMap((held) => held.assertions.map((one) => ({
        case: held.id, phase: held.phase, ...one
      })))
    ];
    const gatingFailures = flattened.filter((one) => one.status === 'fail' && one.gating);
    const baselineFindings = flattened.filter((one) => one.status === 'fail' && !one.gating);
    const report = scrub({
      schemaVersion: 1,
      matrixVersion: matrix.version,
      projectPrefix: PROJECT_PREFIX,
      inputHashes,
      requiredViewports: [...ALLOWED_VIEWPORTS],
      serverAssertions,
      cases: results,
      counts: {
        cases: results.length,
        captures: results.filter((one) => one.capture).length,
        assertions: flattened.length,
        passed: flattened.filter((one) => one.status === 'pass').length,
        gatingFailures: gatingFailures.length,
        baselineFindings: baselineFindings.length
      },
      gatingFailures,
      baselineFindings
    }, base);
    const text = JSON.stringify(report, null, 2) + '\n';
    if (options.jsonOut) {
      await mkdir(dirname(options.jsonOut), { recursive: true });
      await writeFile(options.jsonOut, text);
    }
    if (options.captureDir) {
      await writeFile(join(options.captureDir, 'browser-results.json'), text);
    }
    process.stdout.write(text);
    process.exitCode = gatingFailures.length ? 1 : 0;
    void version;
  } catch (error) {
    process.stderr.write(scrubString((error.stack || String(error)) + '\n' + chromeStderr.slice(-4000), base));
    process.exitCode = 1;
  } finally {
    if (cdp) cdp.close();
    await stopChrome(chrome);
    await new Promise((accept) => server.close(accept));
    await rm(profile, { recursive: true, force: true });
  }
}

await main();
