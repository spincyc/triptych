#!/usr/bin/env node

/* Real-Chromium proof that keyboard recovery on the Catena page lands on a
 * VISIBLE focus indicator, on both the success and the failure path.
 *
 * The integration review's second merge blocker was not a bug the replay
 * harness can see. The shim has no cascade and no computed style: it can say
 * that `document.activeElement` became `#reading`, which was already true and
 * already asserted, and it cannot say that the shared shell's
 * `.reading:focus { outline: none }` then out-ranked the universal
 * `:focus-visible` rule and drew nothing at all. A keyboard reader was moved
 * somewhere the page would not show them.
 *
 * So the assertion has to be made where the cascade is: in a browser, against
 * the BUILT artifact, reading `getComputedStyle` on the element the browser
 * itself reports as active. Every observation below is a computed or rendered
 * fact, compared with the same element's resting state, never a string found
 * in the stylesheet.
 *
 * The harness reports nothing rather than reporting a pass it did not observe:
 * with no Chromium, or no built site, it exits 3 and states which.
 *
 *   node tools/tests/catena_recovery_focus_gate.mjs [--json-out FILE]
 *
 * `TRIPTYCH_CHROME` names the browser; `TRIPTYCH_REVIEW_ROOT` names the built
 * site root, and defaults to `build/public-alpha/site`.
 */

import { spawn } from 'node:child_process';
import { createServer } from 'node:http';
import { access, mkdtemp, readFile, writeFile } from 'node:fs/promises';
import { tmpdir } from 'node:os';
import { extname, join, resolve, sep } from 'node:path';
import process from 'node:process';

const REPO = resolve(import.meta.dirname, '../..');
const ROOT = resolve(process.env.TRIPTYCH_REVIEW_ROOT || join(REPO, 'build/public-alpha/site'));
const CHROME_CANDIDATES = [
  '/usr/bin/chromium',
  '/usr/bin/chromium-browser',
  '/usr/bin/google-chrome-stable',
  '/usr/bin/google-chrome'
];
const EXIT_NO_BROWSER = 3;

/* The route with the eight recorded translation absences, and a route whose
 * book is not a book — the reviewed invalid address that offers recovery. */
const ABSENCE_ROUTE = '/catena/index.html#book=Gen&chapter=1&bible=douay-rheims&voice=translation:en';
const INVALID_ROUTE = '/catena/index.html#book=Zzz&chapter=1&bible=douay-rheims';
const RECOVERY_LABEL = 'Open the nearest valid page';

const jsonAt = process.argv.indexOf('--json-out');
const jsonOut = jsonAt >= 0 ? resolve(process.argv[jsonAt + 1]) : null;

const observations = [];
const failures = [];
const consoleProblems = [];

function mime(path) {
  return ({
    '.css': 'text/css; charset=utf-8',
    '.html': 'text/html; charset=utf-8',
    '.js': 'text/javascript; charset=utf-8',
    '.json': 'application/json; charset=utf-8',
    '.svg': 'image/svg+xml',
    '.txt': 'text/plain; charset=utf-8',
    '.png': 'image/png',
    '.woff2': 'font/woff2'
  })[extname(path)] || 'application/octet-stream';
}

async function exists(path) {
  try {
    await access(path);
    return true;
  } catch (_error) {
    return false;
  }
}

async function browserBinary() {
  const named = process.env.TRIPTYCH_CHROME;
  if (named) return (await exists(named)) ? named : null;
  for (const candidate of CHROME_CANDIDATES) {
    if (await exists(candidate)) return candidate;
  }
  return null;
}

async function listen(server) {
  await new Promise((accept, reject) => {
    server.once('error', reject);
    server.listen(0, '127.0.0.1', accept);
  });
  return server.address().port;
}

function staticServer() {
  return createServer(async (request, response) => {
    try {
      const url = new URL(request.url, 'http://127.0.0.1');
      const relative = decodeURIComponent(url.pathname).replace(/^\/+/, '');
      let file = resolve(ROOT, relative || 'index.html');
      if (file !== ROOT && !file.startsWith(ROOT + sep)) throw new Error('outside root');
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

async function waitForJson(url, attempts = 300) {
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
      (this.events.get(message.method) || []).forEach((one) => one(message.params || {}));
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
      }, 30000);
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
    expression, awaitPromise: true, returnByValue: true, userGesture: true
  });
  if (result.exceptionDetails) {
    throw new Error(result.exceptionDetails.exception?.description
      || result.exceptionDetails.text);
  }
  return result.result.value;
}

async function key(cdp, name, code) {
  for (const type of ['keyDown', 'keyUp']) {
    await cdp.send('Input.dispatchKeyEvent', {
      type, key: name, code: name,
      windowsVirtualKeyCode: code, nativeVirtualKeyCode: code
    });
  }
}

/* The page settles asynchronously — index, editions, paragraph index, chapter
 * spine, Scripture — and there is no readiness flag to wait on, so readiness
 * is a condition about the DOM rather than a fixed sleep. */
async function waitFor(cdp, expression, label, attempts = 200) {
  for (let attempt = 0; attempt < attempts; attempt += 1) {
    if (await evaluate(cdp, `Boolean(${expression})`)) return;
    await new Promise((accept) => setTimeout(accept, 50));
  }
  throw new Error('timed out waiting for ' + label);
}

const pause = (ms) => new Promise((accept) => setTimeout(accept, ms));

async function test(name, callback) {
  try {
    const detail = await callback();
    observations.push({ name, status: 'pass', detail: detail ?? null });
  } catch (error) {
    failures.push({ name, message: error.stack || String(error) });
    observations.push({ name, status: 'fail', detail: error.message });
  }
}

/* WHAT THE BROWSER DRAWS AROUND THE ACTIVE ELEMENT. Read from the element the
 * browser itself reports as active, so nothing here can be true of an element
 * a reader is not standing on. `outline-*` is the ring, `box-shadow` and
 * `border-*` are the other two ways a stylesheet can draw one, and the
 * bounding boxes are what tells a real ring from a zero-width declaration. */
const FOCUS_READING = `(() => {
  const one = document.activeElement;
  if (!one) return null;
  const style = getComputedStyle(one);
  const box = one.getBoundingClientRect();
  return {
    id: one.id,
    tag: one.tagName,
    isReading: one === document.getElementById('reading'),
    matchesFocus: one.matches(':focus'),
    matchesFocusVisible: one.matches(':focus-visible'),
    outlineStyle: style.outlineStyle,
    outlineWidth: style.outlineWidth,
    outlineColor: style.outlineColor,
    outlineOffset: style.outlineOffset,
    boxShadow: style.boxShadow,
    borderWidth: style.borderTopWidth,
    borderStyle: style.borderTopStyle,
    background: style.backgroundColor,
    width: Math.round(box.width),
    height: Math.round(box.height),
    tabIndex: one.tabIndex
  };
})()`;

/* THE SAME ELEMENT, NOT FOCUSED. A focus indicator is a DIFFERENCE, and a
 * page whose reading region always carried a ring would satisfy every
 * absolute assertion while telling a reader nothing. */
const RESTING_READING = `(() => {
  const one = document.getElementById('reading');
  const style = getComputedStyle(one);
  return {
    outlineStyle: style.outlineStyle,
    outlineWidth: style.outlineWidth,
    outlineColor: style.outlineColor,
    boxShadow: style.boxShadow
  };
})()`;

/* CONTRAST, COMPUTED FROM WHAT THE BROWSER RESOLVED. The ring's colour comes
 * back from `getComputedStyle` as an `rgb()` triple whatever the stylesheet
 * wrote, and the surface behind it is the region's own resolved background —
 * walked up to the first ancestor that paints one. WCAG relative luminance,
 * so "sufficient contrast" is a number and not an opinion about a hex code. */
const CONTRAST = `(() => {
  const parse = (value) => {
    const found = String(value).match(/-?[\\d.]+/g);
    return found ? found.slice(0, 3).map(Number) : null;
  };
  const luminance = (rgb) => {
    const channel = (eight) => {
      const part = eight / 255;
      return part <= 0.03928 ? part / 12.92 : Math.pow((part + 0.055) / 1.055, 2.4);
    };
    return 0.2126 * channel(rgb[0]) + 0.7152 * channel(rgb[1]) + 0.0722 * channel(rgb[2]);
  };
  const one = document.activeElement;
  const ring = parse(getComputedStyle(one).outlineColor);
  let behind = null;
  for (let node = one; node && node !== document.documentElement; node = node.parentElement) {
    const paint = getComputedStyle(node).backgroundColor;
    const rgba = String(paint).match(/-?[\\d.]+/g);
    if (rgba && (rgba.length < 4 || Number(rgba[3]) > 0)) { behind = parse(paint); break; }
  }
  if (!behind) behind = parse(getComputedStyle(document.documentElement).backgroundColor) || [255, 255, 255];
  if (!ring) return null;
  const lighter = Math.max(luminance(ring), luminance(behind));
  const darker = Math.min(luminance(ring), luminance(behind));
  return {
    ring: getComputedStyle(one).outlineColor,
    behind: behind,
    ratio: Math.round(((lighter + 0.05) / (darker + 0.05)) * 100) / 100
  };
})()`;

async function tabToRecovery(cdp, limit = 40) {
  const walk = [];
  for (let step = 0; step < limit; step += 1) {
    await key(cdp, 'Tab', 9);
    const where = await evaluate(cdp, `(() => {
      const one = document.activeElement;
      return { tag: one.tagName, id: one.id,
               text: (one.textContent || '').slice(0, 48).trim() };
    })()`);
    walk.push(where);
    if (where.tag === 'A' && where.text.startsWith(RECOVERY_LABEL)) {
      return { walk, reached: true };
    }
  }
  return { walk, reached: false };
}

/* A VISIBLE RING, ASSERTED THE SAME WAY EVERYWHERE. One shape of proof for
 * both paths: the browser says the element is focused, the ring is a painted
 * outline of real width, it differs from the same element at rest, and its
 * colour clears the contrast floor. */
function assertVisibleRing(where, resting, contrast, why) {
  if (!where) throw new Error(why + ': nothing is focused at all');
  if (!where.isReading) {
    throw new Error(`${why}: focus is on ${where.tag}#${where.id}, not #reading`);
  }
  if (!where.matchesFocus) throw new Error(why + ': #reading does not match :focus');
  if (!where.matchesFocusVisible) {
    throw new Error(why + ': #reading does not match :focus-visible, so a'
      + ' keyboard reader gets no ring');
  }
  if (where.outlineStyle === 'none') {
    throw new Error(why + ': outline-style is none — this is the reviewed defect');
  }
  const width = Number.parseFloat(where.outlineWidth);
  if (!(width >= 2)) {
    throw new Error(`${why}: outline-width is ${where.outlineWidth}, not a visible ring`);
  }
  if (where.outlineColor.includes('rgba(0, 0, 0, 0)') || where.outlineColor === 'transparent') {
    throw new Error(why + ': the ring is transparent');
  }
  if (!(where.width > 0 && where.height > 0)) {
    throw new Error(why + ': the focused region has no painted box');
  }
  if (resting.outlineStyle !== 'none' && resting.outlineWidth === where.outlineWidth) {
    throw new Error(why + ': the ring is indistinguishable from the resting state');
  }
  if (!contrast || !(contrast.ratio >= 3)) {
    throw new Error(`${why}: the ring contrast is ${contrast && contrast.ratio}:1`);
  }
  return { where, resting, contrast };
}

async function successPath(cdp, base) {
  await cdp.send('Page.navigate', { url: base + INVALID_ROUTE });
  await waitFor(cdp, `document.querySelector('.catena-error a')`, 'the recovery offer');

  const offer = await evaluate(cdp, `(() => {
    const link = document.querySelector('.catena-error a');
    return { text: link.textContent.trim(), href: link.getAttribute('href') };
  })()`);
  const resting = await evaluate(cdp, RESTING_READING);

  await test('recovery-offer-is-a-keyboard-reachable-link', async () => {
    const found = await tabToRecovery(cdp);
    if (!found.reached) {
      throw new Error('tabbing never reached the recovery link: '
        + JSON.stringify(found.walk));
    }
    return { steps: found.walk.length, offer };
  });

  await test('recovery-link-itself-shows-a-focus-ring', async () => {
    const ring = await evaluate(cdp, `(() => {
      const style = getComputedStyle(document.activeElement);
      return { outlineStyle: style.outlineStyle, outlineWidth: style.outlineWidth,
               focusVisible: document.activeElement.matches(':focus-visible') };
    })()`);
    if (ring.outlineStyle === 'none') throw new Error('the offer itself is unringed');
    return ring;
  });

  await key(cdp, 'Enter', 13);
  await waitFor(cdp, `document.activeElement === document.getElementById('reading')`,
    'recovery focus to land on the reading region');
  await pause(400);

  await test('recovery-focus-lands-on-the-reading-region', async () => {
    const where = await evaluate(cdp, FOCUS_READING);
    if (!where.isReading) throw new Error('focus is on ' + where.tag + '#' + where.id);
    return { hash: await evaluate(cdp, 'location.hash'), tabIndex: where.tabIndex };
  });

  await test('recovery-focus-is-visible-in-real-chromium', async () => {
    const where = await evaluate(cdp, FOCUS_READING);
    const contrast = await evaluate(cdp, CONTRAST);
    return assertVisibleRing(where, resting, contrast, 'the success path');
  });

  await test('the-page-really-recovered-behind-the-ring', async () => {
    const state = await evaluate(cdp, `(() => ({
      hash: location.hash,
      reference: (document.getElementById('reference') || {}).textContent || '',
      errors: document.querySelectorAll('.catena-error').length
    }))()`);
    if (state.errors) throw new Error('the error state survived recovery');
    if (!state.hash.includes('book=')) throw new Error('no route was written: ' + state.hash);
    return state;
  });

}

/* THE OTHER HALF OF `:focus-visible`: a mouse reader is owed NOTHING. Run on
 * its own fresh document, because Chromium keeps the focus-visible state of an
 * element that already had it — a press tested straight after a keyboard
 * recovery would be asking whether the ring goes away, which is not the
 * question. Here the region has never been focused at all. */
async function mousePath(cdp, base) {
  await cdp.send('Page.navigate', { url: 'about:blank' });
  await pause(150);
  await cdp.send('Page.navigate', { url: base + ABSENCE_ROUTE });
  await waitFor(cdp, `document.querySelector('.absence-list .absence')`, 'the absence rows');
  await pause(200);

  await test('a-mouse-press-on-the-region-draws-no-ring', async () => {
    const before = await evaluate(cdp, RESTING_READING);
    if (before.outlineStyle !== 'none') {
      throw new Error('the region carries a ring before anything touched it');
    }
    const box = await evaluate(cdp, `(() => {
      const one = document.getElementById('reading');
      const box = one.getBoundingClientRect();
      return { x: Math.round(box.left + 8), y: Math.round(box.top + 8) };
    })()`);
    for (const type of ['mousePressed', 'mouseReleased']) {
      await cdp.send('Input.dispatchMouseEvent', {
        type, x: box.x, y: box.y, button: 'left', buttons: 1, clickCount: 1
      });
    }
    await pause(150);
    const after = await evaluate(cdp, `(() => {
      const one = document.getElementById('reading');
      const style = getComputedStyle(one);
      return { focused: one.matches(':focus'),
               focusVisible: one.matches(':focus-visible'),
               outlineStyle: style.outlineStyle };
    })()`);
    if (after.focusVisible || after.outlineStyle !== 'none') {
      throw new Error('a mouse press drew a ring on the reading region: '
        + JSON.stringify(after));
    }
    return after;
  });

  await test('a-keyboard-arrival-after-the-press-still-draws-the-ring', async () => {
    // And the mouse press has not disabled the keyboard's own answer: the
    // very next Tab into the page produces a ring on whatever it lands on, so
    // the `:focus-visible` heuristic is being read, not suppressed.
    const found = await tabToRecovery(cdp, 6);
    const ring = await evaluate(cdp, `(() => {
      const one = document.activeElement;
      const style = getComputedStyle(one);
      return { tag: one.tagName, focusVisible: one.matches(':focus-visible'),
               outlineStyle: style.outlineStyle, outlineWidth: style.outlineWidth };
    })()`);
    if (ring.outlineStyle === 'none') {
      throw new Error('the first keyboard stop after a press is unringed: '
        + JSON.stringify(ring));
    }
    return { stops: found.walk.length, ring };
  });
}

async function failurePath(cdp, base) {
  /* THE REVIEWED RECOVERY PATH THAT FAILS. A hash-only navigation keeps the
   * page's caches, and a chapter already held cannot fail — so the document is
   * thrown away first, the invalid route is loaded fresh, and the chapter
   * spines are then made unfetchable BEFORE the recovery link is followed.
   * The rejection is installed in the page, not in the transport, so the built
   * artifact is exactly the one a reader would get. */
  await cdp.send('Page.navigate', { url: 'about:blank' });
  await pause(150);
  await cdp.send('Page.navigate', { url: base + INVALID_ROUTE });
  await waitFor(cdp, `document.querySelector('.catena-error a')`, 'the recovery offer');
  const resting = await evaluate(cdp, RESTING_READING);

  await evaluate(cdp, `(() => {
    const real = window.fetch;
    window.__refused = [];
    window.fetch = (url, init) => {
      if (/structure\\/catena\\/[0-9]/.test(String(url))) {
        window.__refused.push(String(url));
        return Promise.reject(new TypeError('failed to fetch'));
      }
      return real(url, init);
    };
    return true;
  })()`);

  const found = await tabToRecovery(cdp);
  await test('the-failing-recovery-offer-is-still-keyboard-reachable', async () => {
    if (!found.reached) {
      throw new Error('tabbing never reached the recovery link: '
        + JSON.stringify(found.walk));
    }
    return { steps: found.walk.length };
  });

  await key(cdp, 'Enter', 13);
  await waitFor(cdp, `document.activeElement === document.getElementById('reading')`,
    'recovery focus to land on the reading region');
  await pause(500);

  await test('the-recovery-really-failed', async () => {
    const state = await evaluate(cdp, `(() => ({
      refused: (window.__refused || []).length,
      classes: [...document.getElementById('reading').children].map((one) => one.className),
      said: (document.getElementById('reading').textContent || '').slice(0, 160)
    }))()`);
    if (!state.refused) throw new Error('no chapter request was refused at all');
    if (!state.classes.some((one) => String(one).includes('error'))) {
      throw new Error('the page did not fail: ' + JSON.stringify(state.classes));
    }
    return state;
  });

  await test('failed-recovery-focus-is-visible-in-real-chromium', async () => {
    const where = await evaluate(cdp, FOCUS_READING);
    const contrast = await evaluate(cdp, CONTRAST);
    return assertVisibleRing(where, resting, contrast, 'the failure path');
  });

  await test('the-failure-a-reader-is-standing-on-is-the-one-they-can-read', async () => {
    // The ring is worth nothing if it surrounds an empty region: the failure's
    // own words have to be inside the element that holds the focus.
    const said = await evaluate(cdp, `(() => {
      const one = document.getElementById('reading');
      return { active: document.activeElement === one,
               text: (one.textContent || '').trim().slice(0, 200) };
    })()`);
    if (!said.active) throw new Error('the reading region is not focused');
    if (!said.text) throw new Error('the focused region says nothing at all');
    return said;
  });
}

async function absenceRows(cdp, base) {
  /* THE FIRST BLOCKER, IN THE SAME BROWSER. The replay suite proves the
   * delimiter is a node; this proves the built artifact renders it, so a
   * build step that stripped text nodes could not pass one and fail the
   * other. */
  await cdp.send('Page.navigate', { url: base + ABSENCE_ROUTE });
  await waitFor(cdp, `document.querySelector('.absence-list .absence')`, 'the absence rows');
  await pause(200);

  await test('absence-rows-read-apart-when-flattened', async () => {
    const rows = await evaluate(cdp, `(() => [...document.querySelectorAll('.absence-list .absence')]
      .map((row) => ({
        author: (row.querySelector('.absence-author') || {}).textContent || '',
        work: (row.querySelector('.absence-work') || {}).textContent || '',
        flattened: row.textContent,
        rendered: row.innerText
      })))()`);
    if (!rows.length) throw new Error('no absence row rendered at all');
    for (const row of rows) {
      if (row.flattened.includes(row.author + row.work)) {
        throw new Error('flattened together: ' + row.flattened.slice(0, 80));
      }
      if (!row.flattened.startsWith(row.author + ' — ' + row.work)) {
        throw new Error('no delimiter: ' + row.flattened.slice(0, 80));
      }
      if (!row.rendered.includes('—')) {
        throw new Error('the rendered text carries no delimiter: '
          + row.rendered.slice(0, 80));
      }
    }
    return { rows: rows.length, first: rows[0].flattened.slice(0, 80) };
  });
}

async function main() {
  const chromeBinary = await browserBinary();
  if (!chromeBinary) {
    process.stderr.write(
      'catena_recovery_focus: no Chromium or Chrome executable was found.\n'
      + 'Set TRIPTYCH_CHROME to one, for example\n'
      + '  TRIPTYCH_CHROME=/usr/bin/chromium node tools/tests/catena_recovery_focus_gate.mjs\n'
      + `Tried: ${process.env.TRIPTYCH_CHROME || CHROME_CANDIDATES.join(', ')}\n`
      + 'This harness reports nothing rather than reporting a pass it did not observe.\n'
    );
    process.exitCode = EXIT_NO_BROWSER;
    return;
  }
  if (!(await exists(join(ROOT, 'catena/index.html')))) {
    process.stderr.write(
      `catena_recovery_focus: no built Catena page under ${ROOT}.\n`
      + 'Run `make public-site`, or set TRIPTYCH_REVIEW_ROOT to a built site root.\n'
    );
    process.exitCode = EXIT_NO_BROWSER;
    return;
  }

  const server = staticServer();
  const base = `http://127.0.0.1:${await listen(server)}`;
  const debugPort = await freePort();
  const profile = await mkdtemp(join(tmpdir(), 'triptych-catena-focus-chrome-'));
  const chrome = spawn(chromeBinary, [
    '--headless=new', '--no-sandbox', '--disable-dev-shm-usage', '--disable-gpu',
    '--disable-background-networking', '--disable-sync', '--mute-audio',
    '--no-first-run', '--no-default-browser-check',
    `--remote-debugging-port=${debugPort}`, `--user-data-dir=${profile}`, 'about:blank'
  ], { stdio: ['ignore', 'ignore', 'pipe'] });
  let chromeStderr = '';
  chrome.stderr.on('data', (chunk) => { chromeStderr += chunk.toString(); });

  let cdp = null;
  let chromium = '';
  try {
    chromium = (await waitForJson(`http://127.0.0.1:${debugPort}/json/version`)).Browser;
    const created = await (await fetch(
      `http://127.0.0.1:${debugPort}/json/new?${encodeURIComponent('about:blank')}`,
      { method: 'PUT' }
    )).json();
    cdp = new CDP(created.webSocketDebuggerUrl);
    await cdp.ready();
    for (const domain of ['Page', 'Runtime', 'DOM', 'Network']) {
      await cdp.send(`${domain}.enable`);
    }
    cdp.on('Runtime.consoleAPICalled', ({ type, args }) => {
      if (type === 'error') {
        consoleProblems.push({
          type, text: args.map((one) => one.value || one.description || '').join(' ')
        });
      }
    });
    await cdp.send('Emulation.setDeviceMetricsOverride', {
      width: 1440, height: 900, deviceScaleFactor: 1, mobile: false,
      screenWidth: 1440, screenHeight: 900
    });

    await absenceRows(cdp, base);
    await successPath(cdp, base);
    await mousePath(cdp, base);
    await failurePath(cdp, base);
  } catch (error) {
    failures.push({ name: 'harness', message: String(error.stack || error) });
    process.stderr.write(String(error.stack || error) + '\n'
      + chromeStderr.slice(-2000) + '\n');
  } finally {
    if (cdp) cdp.close();
    chrome.kill('SIGKILL');
    await new Promise((accept) => server.close(accept));
  }

  const report = {
    generatedAt: new Date().toISOString(),
    chromium,
    routes: { absence: ABSENCE_ROUTE, invalid: INVALID_ROUTE },
    assertions: observations,
    failures,
    consoleProblems
  };
  if (jsonOut) await writeFile(jsonOut, JSON.stringify(report, null, 2) + '\n');
  process.stdout.write(JSON.stringify(report, null, 2) + '\n');
  if (failures.length || consoleProblems.length) process.exitCode = 1;
}

await main();
