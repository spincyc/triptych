#!/usr/bin/env node

/* Real-Chromium proof that the generated public site works at any mount.
 *
 * The generated artifact is served at "/<repo>" today (GitHub Pages project
 * site) and at "/" once the didach.ai custom domain is active. Every page
 * links document-relatively, so the same artifact must work at both mounts;
 * this harness serves build/public-alpha/site at the mount named by
 * TRIPTYCH_TEST_MOUNT (default "", i.e. the root) and proves the properties
 * the migration rests on:
 *
 *   - every entrance page cold-loads with no console errors, no failed
 *     requests, and no HTTP status >= 400;
 *   - every request the pages make stays inside the mount — the assertion
 *     that catches "//", duplicated segments, and absolute-origin leaks;
 *   - the browser data root resolves relatively (no ?data= is passed, so
 *     shared/browser-core.js's default "../browse" is what is exercised);
 *   - a hash deep link on the Day reader cold-loads;
 *   - a PDF and the site assets are reachable under the mount; and
 *   - a missed deep URL serves 404.html, whose links are anchored to the
 *     artifact's built base path (asset resolution is asserted when the
 *     mount equals that base path — the deployed combination).
 *
 * Run it twice to cover both deployment shapes:
 *   TRIPTYCH_TEST_MOUNT=          node tools/tests/public_site_mount_browser.mjs
 *   TRIPTYCH_TEST_MOUNT=/triptych node tools/tests/public_site_mount_browser.mjs
 *
 * Prerequisite: make public-site (the artifact must exist).
 */

import assert from 'node:assert/strict';
import { spawn } from 'node:child_process';
import { mkdtemp, readFile, readdir, rm, stat } from 'node:fs/promises';
import { tmpdir } from 'node:os';
import { join, resolve } from 'node:path';
import process from 'node:process';

import { serveTree, listen, freePort, mountFromEnv } from './harness/static-site-server.mjs';

const ROOT = resolve(process.env.TRIPTYCH_REVIEW_ROOT || resolve(import.meta.dirname, '../..'));
const SITE = join(ROOT, 'build', 'public-alpha', 'site');
const MOUNT = mountFromEnv();
const chromeBinary = process.env.TRIPTYCH_CHROME || '/usr/bin/google-chrome-stable';

const ENTRANCES = ['liturgy', 'scripture', 'catena', 'history', 'texts', 'sources', 'law'];
const DAY_DEEP_LINK = '#date=2026-08-02&missal=roman-1962&bible=douay-rheims&orations=la';

const failures = [];
const assertions = [];

function record(label, run) {
  return run().then(
    () => assertions.push(label),
    (error) => failures.push({ label, error: String(error && error.message || error) })
  );
}

async function siteBasePath() {
  const source = await readFile(join(ROOT, 'tools', 'public-alpha'), 'utf8');
  const match = source.match(/^SITE_BASE_PATH = "([^"]*)"$/m);
  if (!match) throw new Error('SITE_BASE_PATH not found in tools/public-alpha');
  return match[1];
}

async function waitForJson(url, attempts = 120) {
  for (let attempt = 0; attempt < attempts; attempt += 1) {
    try {
      const response = await fetch(url);
      if (response.ok) return response.json();
    } catch (_error) { /* Chromium is still starting. */ }
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
  close() { this.socket.close(); }
}

async function evaluate(cdp, expression, awaitPromise = true) {
  const result = await cdp.send('Runtime.evaluate', {
    expression, awaitPromise, returnByValue: true
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
  throw new Error('Timed out waiting for ' + label);
}

async function firstPdfRelative() {
  const providers = await readdir(join(SITE, 'pdf'));
  for (const provider of providers.sort()) {
    const stack = [join(SITE, 'pdf', provider)];
    while (stack.length) {
      const directory = stack.shift();
      const entries = (await readdir(directory, { withFileTypes: true }))
        .sort((left, right) => left.name.localeCompare(right.name));
      for (const entry of entries) {
        const path = join(directory, entry.name);
        if (entry.isDirectory()) stack.push(path);
        else if (entry.name.endsWith('.pdf')) return path.slice(SITE.length + 1);
      }
    }
  }
  throw new Error('no PDF found under the artifact');
}

async function main() {
  await stat(SITE).catch(() => {
    throw new Error(`missing generated artifact at ${SITE} — run: make public-site`);
  });
  await stat(chromeBinary).catch(() => {
    throw new Error(`missing Chromium binary at ${chromeBinary} — set TRIPTYCH_CHROME`);
  });
  const builtBasePath = await siteBasePath();

  const server = serveTree({ root: SITE, mountPath: MOUNT });
  const serverPort = await listen(server);
  const origin = `http://127.0.0.1:${serverPort}`;
  const base = origin + MOUNT;

  const debugPort = await freePort();
  const profile = await mkdtemp(join(tmpdir(), 'triptych-site-mount-chrome-'));
  const chrome = spawn(chromeBinary, [
    '--headless=new', '--no-sandbox', '--disable-dev-shm-usage', '--disable-gpu',
    `--remote-debugging-port=${debugPort}`, `--user-data-dir=${profile}`,
    '--no-first-run', '--no-default-browser-check', 'about:blank'
  ], { stdio: ['ignore', 'ignore', 'pipe'] });
  let chromeStderr = '';
  chrome.stderr.on('data', (chunk) => { chromeStderr += chunk.toString(); });

  let cdp;
  const consoleProblems = [];
  const failedRequests = [];
  const httpProblems = [];
  const requests = [];
  try {
    await waitForJson(`http://127.0.0.1:${debugPort}/json/version`);
    const response = await fetch(
      `http://127.0.0.1:${debugPort}/json/new?${encodeURIComponent('about:blank')}`,
      { method: 'PUT' }
    );
    const page = await response.json();
    cdp = new CDP(page.webSocketDebuggerUrl);
    await cdp.ready();
    await Promise.all([
      cdp.send('Page.enable'), cdp.send('Runtime.enable'), cdp.send('Network.enable')
    ]);
    cdp.on('Runtime.consoleAPICalled', ({ type, args }) => {
      if (['error', 'warning'].includes(type)) consoleProblems.push({
        type, text: args.map((arg) => arg.value || arg.description || '').join(' ')
      });
    });
    cdp.on('Network.requestWillBeSent', ({ request }) => requests.push(request.url));
    cdp.on('Network.loadingFailed', (event) => {
      if (!event.canceled) failedRequests.push({ error: event.errorText, requestId: event.requestId });
    });
    cdp.on('Network.responseReceived', ({ response: held }) => {
      if (held.status >= 400) httpProblems.push({ status: held.status, url: held.url });
    });

    const navigate = async (url, readyExpression, label) => {
      await cdp.send('Page.navigate', { url });
      await waitFor(cdp, "document.readyState === 'complete'", label + ' load');
      if (readyExpression) await waitFor(cdp, readyExpression, label + ' readiness');
    };

    // The home page, cold.
    await record('home cold-loads under the mount', async () => {
      await navigate(`${base}/`, "document.querySelector('main')", 'home');
      const title = await evaluate(cdp, 'document.title');
      assert.match(title, /Triptych/);
    });

    // Every entrance page, cold and direct, with the default relative data
    // root actually exercised: no ?data= anywhere in this harness. The
    // scripture front door deliberately fetches nothing (plan.js: "This page
    // reads no scripture and fetches no chapter"), so it is held to the
    // clean-load assertions but not to a data fetch.
    const FETCHING_ENTRANCES = ENTRANCES.filter((entrance) => entrance !== 'scripture');
    for (const entrance of ENTRANCES) {
      await record(`${entrance}/ cold-loads and fetches its data relatively`, async () => {
        const before = requests.length;
        await navigate(`${base}/${entrance}/`, "document.querySelector('main')", entrance);
        if (!FETCHING_ENTRANCES.includes(entrance)) return;
        // The page must ask for corpus data under the mount's browse sibling;
        // the request log fills from CDP events, so poll the Node side.
        const sawBrowse = () =>
          requests.slice(before).some((url) => url.startsWith(`${origin}${MOUNT}/browse/`));
        for (let attempt = 0; attempt < 200 && !sawBrowse(); attempt += 1) {
          await new Promise((accept) => setTimeout(accept, 50));
        }
        assert.ok(
          sawBrowse(),
          `no ${MOUNT}/browse/ request observed from ${entrance}/ — got: ` +
            requests.slice(before).slice(0, 8).join(', ')
        );
      });
    }

    // A hash deep link on the Day reader, cold.
    await record('liturgy/day.html hash deep link cold-loads', async () => {
      await navigate(`${base}/liturgy/day.html${DAY_DEEP_LINK}`, "document.querySelector('main')", 'day deep link');
      const hash = await evaluate(cdp, 'window.location.hash');
      assert.ok(hash.includes('missal=roman-1962'), 'hash survived navigation: ' + hash);
    });

    // Every request either left for the debugging endpoint or stayed inside
    // the mount: this one assertion catches //, /triptych/triptych/,
    // dropped mounts, and absolute-origin leaks.
    await record('every page request stays inside the mount', async () => {
      const external = requests.filter((url) => {
        if (!/^https?:/.test(url)) return false;
        if (!url.startsWith(origin + '/')) return true;
        return MOUNT ? !(url === origin + MOUNT || url.startsWith(origin + MOUNT + '/')) : false;
      });
      assert.deepEqual(external, []);
    });

    await record('no failed requests', async () => assert.deepEqual(failedRequests, []));
    await record('no HTTP responses of 400 or above', async () => assert.deepEqual(httpProblems, []));
    await record('no console errors or warnings', async () => assert.deepEqual(consoleProblems, []));

    // Assets and one PDF answer directly under the mount.
    await record('site assets and a PDF are reachable under the mount', async () => {
      for (const path of ['assets/site.css', 'assets/icon.png', 'robots.txt', await firstPdfRelative()]) {
        const reply = await fetch(`${base}/${path}`);
        assert.equal(reply.status, 200, `${path}: ${reply.status}`);
      }
    });

    // A missed deep URL serves the error page with its base-anchored links.
    await record('a missed deep URL serves 404.html', async () => {
      const reply = await fetch(`${base}/liturgy/this-page-does-not-exist.html`);
      assert.equal(reply.status, 404);
      const body = await reply.text();
      assert.match(body, /Page not found/);
      const links = [...body.matchAll(/(?:href|src)="([^"#][^"]*)"/g)]
        .map((match) => match[1])
        .filter((href) => !/^[a-z][a-z0-9+.-]*:/i.test(href) && !href.startsWith('//'));
      assert.ok(links.length > 0, 'the error page names no local links at all');
      for (const href of links) {
        assert.ok(
          href.startsWith(builtBasePath + '/'),
          `error-page link is not anchored to the built base path ${builtBasePath}: ${href}`
        );
      }
      if (MOUNT === builtBasePath) {
        // The deployed combination: the mount the artifact was built for.
        // Every error-page link must actually resolve.
        for (const href of links) {
          const resolved = await fetch(origin + href);
          assert.equal(resolved.status, 200, `${href}: ${resolved.status}`);
        }
      }
    });
  } finally {
    if (cdp) cdp.close();
    chrome.kill('SIGTERM');
    await new Promise((accept) => chrome.once('exit', accept));
    await new Promise((accept) => server.close(accept));
    await rm(profile, { recursive: true, force: true });
  }

  const report = {
    mount: MOUNT || '/',
    builtBasePath: builtBasePath || '/',
    assertions,
    failures,
    consoleProblems,
    failedRequests,
    httpProblems
  };
  console.log(JSON.stringify(report, null, 2));
  if (failures.length) {
    console.error(`${failures.length} failure(s) at mount '${MOUNT || '/'}'`);
    if (chromeStderr && failures.length) console.error(chromeStderr.slice(0, 2000));
    process.exit(1);
  }
  console.log(`public site verified at mount '${MOUNT || '/'}': ${assertions.length} assertion group(s)`);
}

main().catch((error) => {
  console.error(String(error && error.stack || error));
  process.exit(1);
});
