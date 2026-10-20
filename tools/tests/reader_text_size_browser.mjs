#!/usr/bin/env node

/* Source-served Chromium coverage for reader text size and semantic reflow. */

import assert from 'node:assert/strict';
import { spawn } from 'node:child_process';
import { createServer } from 'node:http';
import { mkdir, mkdtemp, readFile, rm, writeFile } from 'node:fs/promises';
import { extname, resolve, sep } from 'node:path';

const ROOT = resolve(import.meta.dirname, '../..');
const CHROME = process.env.TRIPTYCH_CHROME || '/usr/bin/chromium';
const SCRATCH = resolve(process.env.TRIPTYCH_BROWSER_SCRATCH ||
  resolve(ROOT, '.scratch/c7-text-size'));
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
      let body = await readFile(file);
      if (process.env.TRIPTYCH_TEXT_SIZE_INJECT === '1' && extname(file) === '.html') {
        const text = body.toString();
        if (!text.includes('src="reader-text-size.js"')) {
          body = text.replace('</head>', '<link rel="stylesheet" href="reader-text-size.css"></head>')
            .replace('</body>', '<script src="reader-text-size.js"></script></body>');
        }
      }
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

const instance = server();
const port = await listen(instance);
const debugPort = await freePort();
await mkdir(SCRATCH, { recursive: true });
const profile = await mkdtemp(resolve(SCRATCH, 'chromium-'));
const chrome = spawn(CHROME, ['--headless=new', '--disable-gpu', '--no-sandbox',
  '--disable-dev-shm-usage', `--remote-debugging-port=${debugPort}`,
  `--user-data-dir=${profile}`, 'about:blank'], { stdio: 'ignore' });
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
    consoleProblems.push(exceptionDetails?.exception?.description || exceptionDetails?.text);
  });
  cdp.on('Network.loadingFailed', ({ canceled, errorText }) => {
    if (!canceled) failedRequests.push(errorText);
  });
  cdp.on('Network.responseReceived', ({ response }) => {
    if (response?.status >= 400) httpProblems.push({ status: response.status, url: response.url });
  });
  await Promise.all([cdp.send('Page.enable'), cdp.send('Runtime.enable'),
    cdp.send('Network.enable'), cdp.send('Accessibility.enable')]);
  const base = `http://127.0.0.1:${port}`;
  let navigation = 0;

  async function navigate(entrance) {
    const hash = entrance === 'day'
      ? '#date=2026-08-02&missal=roman-1962&bible=douay-rheims&orations=la&mode=read&ordinary=0'
      : '#missal=roman-1962&type=seasonal&mass=pentecost-10&bible=douay-rheims&orations=la&mode=read';
    // A new query forces a document load even after the controller has
    // canonicalized the hash; a hash-only navigation would reuse old readiness.
    const url = base + (entrance === 'day' ? DAY : PROPERS) +
      '?data=/src/web/data&text-size-probe=' + (++navigation) + hash;
    await evaluate(cdp, 'window.__textSizeNavigating = true');
    await cdp.send('Page.navigate', {url});
    await waitFor(cdp, `!window.__textSizeNavigating && window.${entrance}ReaderDebug?.ready &&
      document.getElementById('reader-text-size')`, entrance + ' ready with text-size control');
    assert.equal(await evaluate(cdp, `${entrance}ReaderDebug.outcome`), 'ready');
  }

  async function settled() {
    await evaluate(cdp, 'new Promise(resolve => requestAnimationFrame(() => requestAnimationFrame(resolve)))');
  }

  async function viewport(width, height, scale = 1) {
    await cdp.send('Emulation.setDeviceMetricsOverride', {
      width, height, deviceScaleFactor: scale, mobile: false
    });
    await settled();
  }

  async function change(size) {
    await evaluate(cdp, `(() => { const select = document.getElementById('reader-text-size');
      select.focus({preventScroll:true}); select.value = '${size}';
      select.dispatchEvent(new Event('change', {bubbles:true})); })()`);
    await settled();
  }

  const currentLocation = `(() => {
    const line = Math.max(80, Math.min(innerHeight * .38, 280));
    const nodes = [...document.querySelectorAll('#reader-document [data-semantic-location]')];
    let target = nodes[0];
    for (const node of nodes) { if(node.getBoundingClientRect().top <= line) target=node; else break; }
    return target?.dataset.semanticLocation;
  })()`;

  for (const entrance of ['day', 'propers']) {
    activeCase = entrance + '-text-size-place-focus-and-reflow';
    await viewport(393, 852);
    await navigate(entrance);
    await evaluate(cdp, `localStorage.removeItem(TriptychReaderTextSize.PREFERENCE_KEY)`);
    await navigate(entrance);
    const originalUrl = await evaluate(cdp, 'location.href');
    const baseline = await evaluate(cdp,
      `parseFloat(getComputedStyle(document.querySelector('.reader-document .passage, .reader-document .composed')).fontSize)`);
    await evaluate(cdp, `(() => {
      const units = document.querySelectorAll('#reader-document [data-semantic-location]');
      units[Math.floor(units.length/2)].scrollIntoView({block:'start',behavior:'instant'});
    })()`);
    const before = await evaluate(cdp, currentLocation);
    await evaluate(cdp, `document.getElementById('mode-surface').addEventListener(
      'beforetoggle', event => event.stopImmediatePropagation(), true)`);
    await evaluate(cdp, `document.querySelector('[data-reader-action="mode"]').click()`);
    await change(175);
    for (const type of ['keyDown', 'keyUp']) {
      await cdp.send('Input.dispatchKeyEvent', {type, key:'ArrowDown', code:'ArrowDown',
        windowsVirtualKeyCode:40, nativeVirtualKeyCode:40});
    }
    await settled();
    assert.equal(await evaluate(cdp, `document.getElementById('reader-text-size').value`), '200');
    assert.equal(await evaluate(cdp, `document.activeElement.id`), 'reader-text-size');
    assert.equal(await evaluate(cdp, `getComputedStyle(document.documentElement).fontSize`), '32px');
    const enlarged = await evaluate(cdp,
      `parseFloat(getComputedStyle(document.querySelector('.reader-document .passage, .reader-document .composed')).fontSize)`);
    assert.ok(Math.abs(enlarged / baseline - 2) < .01,
      'spoken text doubles: ' + JSON.stringify({entrance, baseline, enlarged}));
    const ax = await cdp.send('Accessibility.getFullAXTree');
    assert.ok(ax.nodes.some((node) => node.role?.value === 'combobox' &&
      node.name?.value === 'Text size' && node.value?.value === '200%'));
    await evaluate(cdp, `document.querySelector('#mode-surface [data-reader-close]').click()`);
    await settled();
    assert.equal(await evaluate(cdp, currentLocation), before, 'same semantic unit after enlargement and modal close');
    assert.equal(await evaluate(cdp, `document.activeElement.dataset.readerAction`), 'mode');
    assert.equal(await evaluate(cdp, 'location.href'), originalUrl);
    await evaluate(cdp, `document.querySelectorAll('#reader-document [data-semantic-location]')[1]
      .scrollIntoView({block:'start',behavior:'instant'})`);
    const reopenedPlace = await evaluate(cdp, currentLocation);
    assert.notEqual(reopenedPlace, before, 'the next visit starts from a different unit');
    await evaluate(cdp, `document.querySelector('[data-reader-action="mode"]').click()`);
    await evaluate(cdp, `document.querySelector('#mode-surface [data-reader-close]').click()`);
    await settled();
    assert.equal(await evaluate(cdp, currentLocation), reopenedPlace,
      'reopening without a size change keeps the new place when beforetoggle is unavailable');

    await cdp.send('Emulation.setEmulatedMedia', {media:'print'});
    assert.equal(await evaluate(cdp, `getComputedStyle(document.documentElement).fontSize`), '16px');
    assert.equal(await evaluate(cdp, `getComputedStyle(document.querySelector('.reader-text-size')).display`), 'none');
    await cdp.send('Emulation.setEmulatedMedia', {media:'screen'});
    assert.equal(await evaluate(cdp, `getComputedStyle(document.documentElement).fontSize`), '32px');

    for (const [width,height,scale] of [[320,852,1], [320,225,4]]) {
      await viewport(width,height,scale);
      assert.equal(await evaluate(cdp, `document.documentElement.scrollWidth <= innerWidth + 1`), true);
      await evaluate(cdp, `document.querySelector('[data-reader-action="mode"]').click()`);
      await evaluate(cdp, `document.getElementById('reader-text-size').focus()`);
      await settled();
      const overflow = await evaluate(cdp, `(() => {
        const surface=document.getElementById('mode-surface');
        const select=document.getElementById('reader-text-size');
        const box=select.getBoundingClientRect(), panel=surface.getBoundingClientRect();
        const header=surface.querySelector('.surface-head').getBoundingClientRect();
        return {horizontal:surface.scrollWidth <= surface.clientWidth+1,
          control:box.left >= panel.left && box.right <= panel.right+1,
          focus:document.activeElement===select,
          height:box.height, visible:box.bottom>0 && box.top<innerHeight,
          unobscured:box.top >= header.bottom-1 && box.bottom <= panel.bottom+1};
      })()`);
      const screenshot = await cdp.send('Page.captureScreenshot', {format:'png'});
      await writeFile(resolve(SCRATCH, entrance + '-text-200-' + width + 'x' + height + '.png'),
        Buffer.from(screenshot.data, 'base64'));
      assert.deepEqual(overflow, {horizontal:true,control:true,focus:true,height:overflow.height,
        visible:true,unobscured:true}, entrance + ' ' + width + 'x' + height);
      assert.ok(overflow.height >= 44);
      await evaluate(cdp, `document.querySelector('#mode-surface [data-reader-close]').click()`);
    }
    await viewport(393,852);
    await navigate(entrance);
    assert.equal(await evaluate(cdp, `document.getElementById('reader-text-size').value`), '200');
    await evaluate(cdp, `document.querySelector('[data-reader-action="mode"]').click()`);
    await evaluate(cdp, `document.querySelector('[data-mode="study"]').click()`);
    await waitFor(cdp, `${entrance}ReaderDebug.ready && ${entrance}ReaderDebug.state.requestedMode === 'study'`, 'Study rerender');
    assert.equal(await evaluate(cdp, `getComputedStyle(document.documentElement).fontSize`), '32px');
    assert.equal(await evaluate(cdp, `document.querySelectorAll('section[data-reader-text-size]').length`), 1);
    assertions.push({name:activeCase,status:'pass'});
  }

  activeCase = 'invalid-and-unavailable-storage';
  await evaluate(cdp, `localStorage.setItem(TriptychReaderTextSize.PREFERENCE_KEY, '999')`);
  await navigate('day');
  assert.equal(await evaluate(cdp, `document.getElementById('reader-text-size').value`), '100');
  assert.equal(await evaluate(cdp, `localStorage.getItem(TriptychReaderTextSize.PREFERENCE_KEY)`), '999');
  await cdp.send('Page.addScriptToEvaluateOnNewDocument', {source:
    `Object.defineProperty(window,'localStorage',{get(){throw new Error('storage unavailable')}});`});
  await navigate('propers');
  assert.equal(await evaluate(cdp, `document.getElementById('reader-text-size').value`), '100');
  await evaluate(cdp, `document.querySelector('[data-reader-action="mode"]').click()`);
  const before = await evaluate(cdp, 'location.href');
  await change(150);
  assert.equal(await evaluate(cdp, `getComputedStyle(document.documentElement).fontSize`), '24px');
  assert.match(await evaluate(cdp, `document.querySelector('.reader-text-size-status').textContent`), /lasts for this visit/);
  assert.equal(await evaluate(cdp, 'location.href'), before);
  assertions.push({name:activeCase,status:'pass'});
} catch (error) {
  const detail = error?.stack || String(error);
  failures.push({name:activeCase,detail});
} finally {
  if(cdp) cdp.close();
  chrome.kill('SIGTERM');
  if(chrome.exitCode===null && chrome.signalCode===null) await new Promise(done=>chrome.once('exit',done));
  await instance.close();
  await rm(profile,{recursive:true,force:true});
}
const clean = failures.length===0 && consoleProblems.length===0 && failedRequests.length===0 && httpProblems.length===0;
process.stdout.write(JSON.stringify({status:clean?'pass':'fail',checks:assertions.length,
  assertions,failures,consoleProblems,failedRequests,httpProblems})+'\n');
if(!clean) process.exitCode=1;
