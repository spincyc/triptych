#!/usr/bin/env node

/* Dependency-free Chromium gate and evidence capture for the A3/A4 prototype. */

import assert from 'node:assert/strict';
import { spawn } from 'node:child_process';
import { createServer } from 'node:http';
import { mkdtemp, mkdir, readFile, stat, writeFile } from 'node:fs/promises';
import { tmpdir } from 'node:os';
import { extname, join, resolve, sep } from 'node:path';
import process from 'node:process';

const ROOT = resolve(process.env.TRIPTYCH_REVIEW_ROOT || resolve(import.meta.dirname, '../..'));
const ROUTE = '/src/web/browser/prototypes/corpus-foundation/index.html';
const LOOPBACK = [127, 0, 0, 1].join('.');
const captureAt = process.argv.indexOf('--capture-dir');
const captureDir = captureAt >= 0 ? resolve(process.argv[captureAt + 1]) : null;
const chromeBinary = process.env.TRIPTYCH_CHROME || 'chromium';
const observations = [];
const failures = [];
const consoleProblems = [];
const failedRequests = [];
const httpProblems = [];

function mime(path) {
  return ({
    '.css': 'text/css; charset=utf-8',
    '.html': 'text/html; charset=utf-8',
    '.js': 'text/javascript; charset=utf-8'
  })[extname(path)] || 'application/octet-stream';
}

async function listen(server) {
  await new Promise((accept, reject) => {
    server.once('error', reject);
    server.listen(0, LOOPBACK, accept);
  });
  return server.address().port;
}

function staticServer() {
  return createServer(async (request, response) => {
    try {
      const url = new URL(request.url, `http://${LOOPBACK}`);
      const relative = decodeURIComponent(url.pathname).replace(/^\/+/, '');
      if (relative === 'favicon.ico') {
        response.writeHead(204, { 'cache-control': 'no-store' });
        response.end();
        return;
      }
      const file = resolve(ROOT, relative || 'README.md');
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

async function waitForJson(url, attempts = 120) {
  for (let attempt = 0; attempt < attempts; attempt += 1) {
    try {
      const response = await fetch(url);
      if (response.ok) return await response.json();
    } catch (_error) {
      // Chromium has not opened the debugging endpoint yet.
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
      }, 15000);
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

async function waitFor(cdp, expression, label, attempts = 120) {
  for (let attempt = 0; attempt < attempts; attempt += 1) {
    if (await evaluate(cdp, `Boolean(${expression})`)) return;
    await new Promise((accept) => setTimeout(accept, 50));
  }
  throw new Error('Timed out waiting for ' + label);
}

async function viewport(cdp, width, height, scale = 1) {
  await cdp.send('Emulation.setDeviceMetricsOverride', {
    width, height, deviceScaleFactor: scale, mobile: false,
    screenWidth: width, screenHeight: height
  });
}

function url(base, surface = 'reader', panel = 'none') {
  return `${base}${ROUTE}?surface=${surface}&panel=${panel}`;
}

async function navigate(cdp, target) {
  await cdp.send('Page.navigate', { url: target });
  await waitFor(cdp,
    `location.href === ${JSON.stringify(target)} && document.querySelectorAll('[data-archetype]').length === 3`,
    'prototype readiness');
  await new Promise((accept) => setTimeout(accept, 80));
}

async function click(cdp, selector) {
  await evaluate(cdp, `(() => {
    const element = document.querySelector(${JSON.stringify(selector)});
    if (!element) throw new Error('missing selector: ' + ${JSON.stringify(selector)});
    element.click();
    return true;
  })()`);
}

async function escape(cdp) {
  for (const type of ['keyDown', 'keyUp']) {
    await cdp.send('Input.dispatchKeyEvent', {
      type, key: 'Escape', code: 'Escape', windowsVirtualKeyCode: 27, nativeVirtualKeyCode: 27
    });
  }
  await new Promise((accept) => setTimeout(accept, 60));
}

async function shot(cdp, path) {
  const result = await cdp.send('Page.captureScreenshot', {
    format: 'png', captureBeyondViewport: false, fromSurface: true
  });
  await writeFile(path, Buffer.from(result.data, 'base64'));
}

async function test(name, callback) {
  try {
    await callback();
    observations.push({ name, status: 'pass' });
  } catch (error) {
    failures.push({ name, message: error.stack || String(error) });
    observations.push({ name, status: 'fail', detail: error.message });
  }
}

async function pageMetrics(cdp) {
  return evaluate(cdp, `(() => {
    const visible = document.querySelector('[data-archetype]:not([hidden])');
    const targets = [...document.querySelectorAll('button, .button')]
      .filter(node => node.getClientRects().length)
      .map(node => ({ text: node.textContent.trim(), width: node.getBoundingClientRect().width,
        height: node.getBoundingClientRect().height }));
    return {
      viewport: { width: innerWidth, height: innerHeight },
      archetype: visible?.dataset.archetype,
      documentOverflow: document.documentElement.scrollWidth - document.documentElement.clientWidth,
      bodyOverflow: document.body.scrollWidth - document.body.clientWidth,
      overflowNodes: [...document.querySelectorAll('body *')]
        .map(node => ({ name: node.id || node.className || node.tagName,
          left: node.getBoundingClientRect().left, right: node.getBoundingClientRect().right,
          width: node.getBoundingClientRect().width, scrollWidth: node.scrollWidth,
          clientWidth: node.clientWidth }))
        .filter(item => item.right > document.documentElement.clientWidth + 1 || item.left < -1)
        .slice(0, 12),
      openDialogs: document.querySelectorAll('dialog[open]').length,
      unnamedButtons: [...document.querySelectorAll('button')].filter(node =>
        !node.textContent.trim() && !node.getAttribute('aria-label')).length,
      undersizedControls: targets.filter(item => item.height < 43.5),
      usefulTop: visible?.getBoundingClientRect().top,
      primaryTop: (visible?.querySelector('.prose, .catalogue-row, .passage-plane'))?.getBoundingClientRect().top,
      targetCount: targets.length
    };
  })()`);
}

async function runAssertions(cdp, base) {
  await viewport(cdp, 1440, 900);
  await navigate(cdp, url(base));

  await test('one shell and exactly one visible archetype', async () => {
    const value = await evaluate(cdp, `(() => ({
      shells: document.querySelectorAll('[data-prototype-shell="single"]').length,
      visible: [...document.querySelectorAll('[data-archetype]')].filter(node => !node.hidden).map(node => node.dataset.archetype),
      fixture: document.querySelector('main').dataset.fixtureBoundary
    }))()`);
    assert.deepEqual(value, { shells: 1, visible: ['reader'], fixture: 'synthetic-review-v1' });
  });

  await test('surface switches preserve one visible surface', async () => {
    for (const name of ['catalogue', 'instrument', 'reader']) {
      await click(cdp, `[data-select-surface="${name}"]`);
      const value = await evaluate(cdp, `(() => ({
        visible: [...document.querySelectorAll('[data-archetype]')].filter(node => !node.hidden).map(node => node.dataset.archetype),
        pressed: document.querySelector('[data-select-surface="${name}"]').getAttribute('aria-pressed'),
        domain: document.querySelector('#current-domain').textContent
      }))()`);
      assert.deepEqual(value.visible, [name]);
      assert.equal(value.pressed, 'true');
      assert.equal(value.domain, name === 'instrument' ? 'Sources' : 'Publications');
    }
  });

  await test('dialogs have one owner and restore focus', async () => {
    await click(cdp, '[data-open-dialog="jump-dialog"]');
    assert.equal(await evaluate(cdp, 'document.querySelectorAll("dialog[open]").length'), 1);
    await escape(cdp);
    assert.equal(await evaluate(cdp, 'document.querySelectorAll("dialog[open]").length'), 0);
    assert.equal(await evaluate(cdp, 'document.activeElement.dataset.openDialog'), 'jump-dialog');
    await click(cdp, '[data-related-context="reader"]');
    assert.equal(await evaluate(cdp, 'document.querySelectorAll("dialog[open]").length'), 1);
    assert.equal(await evaluate(cdp, 'document.querySelector("dialog[open]").id'), 'related-dialog');
    await escape(cdp);
    assert.equal(await evaluate(cdp, 'document.activeElement.dataset.relatedContext'), 'reader');
  });

  await test('Jump filters and exposes a truthful no-result state', async () => {
    await click(cdp, '[data-open-dialog="jump-dialog"]');
    await evaluate(cdp, `(() => {
      const input = document.querySelector('#jump-query');
      input.value = 'no such synthetic object';
      input.dispatchEvent(new Event('input', { bubbles: true }));
    })()`);
    const value = await evaluate(cdp, `(() => ({
      status: document.querySelector('#jump-status').textContent,
      empty: !document.querySelector('#jump-empty').hidden,
      visible: [...document.querySelectorAll('#jump-results li')].filter(node => !node.hidden).length
    }))()`);
    assert.deepEqual(value, { status: '0 synthetic destinations', empty: true, visible: 0 });
    await escape(cdp);
  });

  await test('Catalogue filtering updates rows, count, and empty state', async () => {
    await click(cdp, '[data-select-surface="catalogue"]');
    await evaluate(cdp, `(() => {
      const input = document.querySelector('#catalogue-filter');
      input.value = 'no such work';
      input.dispatchEvent(new Event('input', { bubbles: true }));
    })()`);
    const value = await evaluate(cdp, `(() => ({
      count: document.querySelector('#catalogue-count').textContent,
      empty: !document.querySelector('#catalogue-empty').hidden,
      visible: [...document.querySelectorAll('[data-catalogue-terms]')].filter(node => !node.hidden).length
    }))()`);
    assert.deepEqual(value, { count: '0 works', empty: true, visible: 0 });
  });

  await test('Related edges change with source object and direction', async () => {
    await click(cdp, '[data-select-surface="reader"]');
    await click(cdp, '[data-related-context="reader"]');
    assert.equal(await evaluate(cdp, 'document.querySelector("[data-related-set=reader]").hidden'), false);
    assert.equal(await evaluate(cdp, 'document.querySelector("[data-related-set=instrument]").hidden'), true);
    await escape(cdp);
    await click(cdp, '[data-select-surface="instrument"]');
    await click(cdp, '[data-related-context="instrument"]');
    const value = await evaluate(cdp, `(() => ({
      reader: document.querySelector('[data-related-set="reader"]').hidden,
      instrument: document.querySelector('[data-related-set="instrument"]').hidden,
      text: document.querySelector('[data-related-set="instrument"]').textContent
    }))()`);
    assert.equal(value.reader, true);
    assert.equal(value.instrument, false);
    assert.match(value.text, /Is cited by publication/);
    assert.doesNotMatch(value.text, /Cites passage/);
    await escape(cdp);
    await navigate(cdp, url(base, 'catalogue', 'related'));
    const catalogue = await evaluate(cdp, `(() => ({
      visible: [...document.querySelectorAll('[data-related-set]')].filter(node => !node.hidden).map(node => node.dataset.relatedSet),
      text: document.querySelector('[data-related-set="catalogue"]').textContent
    }))()`);
    assert.deepEqual(catalogue.visible, ['catalogue']);
    assert.match(catalogue.text, /No structured Related fixture/);
    await escape(cdp);
  });

  await test('review query keys are bounded and do not mutate the URL', async () => {
    const target = `${base}${ROUTE}?surface=unknown&panel=unknown&private=1`;
    await navigate(cdp, target);
    const value = await evaluate(cdp, `(() => ({
      href: location.href,
      surface: document.querySelector('[data-archetype]:not([hidden])').dataset.archetype,
      dialogs: document.querySelectorAll('dialog[open]').length
    }))()`);
    assert.equal(value.href, target);
    assert.equal(value.surface, 'reader');
    assert.equal(value.dialogs, 0);
  });

  await test('320 CSS pixels has no document overflow and useful content appears', async () => {
    await viewport(cdp, 320, 852);
    for (const name of ['reader', 'catalogue', 'instrument']) {
      await navigate(cdp, url(base, name));
      const metrics = await pageMetrics(cdp);
      assert.ok(metrics.documentOverflow <= 1, JSON.stringify(metrics));
      assert.ok(metrics.bodyOverflow <= 1, JSON.stringify(metrics));
      assert.ok(metrics.primaryTop < metrics.viewport.height - 24, JSON.stringify(metrics));
      assert.equal(metrics.unnamedButtons, 0);
      assert.deepEqual(metrics.undersizedControls, []);
    }
  });

  await test('200 percent text preserves reflow and dialog access', async () => {
    await viewport(cdp, 393, 852);
    await navigate(cdp, url(base, 'catalogue', 'jump'));
    await evaluate(cdp, `document.documentElement.style.fontSize = '200%'`);
    await new Promise((accept) => setTimeout(accept, 100));
    const metrics = await pageMetrics(cdp);
    assert.ok(metrics.documentOverflow <= 1, JSON.stringify(metrics));
    assert.equal(metrics.openDialogs, 1);
    assert.deepEqual(metrics.undersizedControls, []);
    await escape(cdp);
  });

  await test('reduced motion contract is active when requested', async () => {
    await cdp.send('Emulation.setEmulatedMedia', {
      media: 'screen', features: [{ name: 'prefers-reduced-motion', value: 'reduce' }]
    });
    await navigate(cdp, url(base));
    const value = await evaluate(cdp,
      `getComputedStyle(document.documentElement).scrollBehavior`);
    assert.equal(value, 'auto');
    await cdp.send('Emulation.setEmulatedMedia', { media: 'screen' });
  });

  await test('keyboard focus is visible without changing layout', async () => {
    await viewport(cdp, 393, 852);
    await navigate(cdp, url(base, 'reader'));
    for (const type of ['keyDown', 'keyUp']) {
      await cdp.send('Input.dispatchKeyEvent', {
        type, key: 'Tab', code: 'Tab', windowsVirtualKeyCode: 9, nativeVirtualKeyCode: 9
      });
    }
    const value = await evaluate(cdp, `(() => {
      const style = getComputedStyle(document.activeElement);
      return { className: document.activeElement.className, outlineWidth: parseFloat(style.outlineWidth),
        transform: style.transform, overflow: document.documentElement.scrollWidth - document.documentElement.clientWidth };
    })()`);
    assert.match(value.className, /skip-link/);
    assert.ok(value.outlineWidth >= 3, JSON.stringify(value));
    assert.equal(value.transform, 'none');
    assert.ok(value.overflow <= 1, JSON.stringify(value));
  });
}

async function captureMatrix(cdp, base, directory) {
  await mkdir(directory, { recursive: true });
  const records = [];

  async function capture(file, width, height, surface, panel = 'none', options = {}) {
    await viewport(cdp, width, height);
    await cdp.send('Emulation.setEmulatedMedia', {
      media: 'screen', features: options.features || []
    });
    await navigate(cdp, url(base, surface, panel));
    if (options.text200) {
      await evaluate(cdp, `document.documentElement.style.fontSize = '200%'`);
      await new Promise((accept) => setTimeout(accept, 80));
    }
    if (options.noResult) {
      await evaluate(cdp, `(() => {
        const input = document.querySelector('#jump-query'); input.value = 'no result';
        input.dispatchEvent(new Event('input', { bubbles: true }));
      })()`);
    }
    if (options.catalogueNoResult) {
      await evaluate(cdp, `(() => {
        const input = document.querySelector('#catalogue-filter'); input.value = 'no result';
        input.dispatchEvent(new Event('input', { bubbles: true }));
      })()`);
    }
    if (options.keyboardTabs) {
      for (let step = 0; step < options.keyboardTabs; step += 1) {
        for (const type of ['keyDown', 'keyUp']) {
          await cdp.send('Input.dispatchKeyEvent', {
            type, key: 'Tab', code: 'Tab', windowsVirtualKeyCode: 9, nativeVirtualKeyCode: 9
          });
        }
      }
      await new Promise((accept) => setTimeout(accept, 50));
    }
    await shot(cdp, join(directory, file));
    records.push({ file, surface, panel, viewport: `${width}x${height}`,
      text: options.text200 ? '200%' : '100%', features: options.features || [],
      metrics: await pageMetrics(cdp) });
  }

  for (const surface of ['reader', 'catalogue', 'instrument']) {
    await capture(`after-${surface}-1440x900.png`, 1440, 900, surface);
    await capture(`after-${surface}-393x852.png`, 393, 852, surface);
  }
  await capture('after-reader-320x852.png', 320, 852, 'reader');
  await capture('after-catalogue-jump-1440x900.png', 1440, 900, 'catalogue', 'jump');
  await capture('after-catalogue-jump-no-result-393x852.png', 393, 852, 'catalogue', 'jump', { noResult: true });
  await capture('after-catalogue-filter-no-result-393x852.png', 393, 852, 'catalogue', 'none', { catalogueNoResult: true });
  await capture('after-reader-related-393x852.png', 393, 852, 'reader', 'related');
  await capture('after-reader-menu-393x852.png', 393, 852, 'reader', 'menu');
  await capture('after-reader-keyboard-focus-393x852.png', 393, 852, 'reader', 'none', { keyboardTabs: 1 });
  await capture('after-instrument-200-percent-393x852.png', 393, 852, 'instrument', 'none', { text200: true });
  await capture('after-catalogue-forced-colors-393x852.png', 393, 852, 'catalogue', 'none', {
    features: [{ name: 'forced-colors', value: 'active' }]
  });
  await capture('after-reader-reduced-motion-393x852.png', 393, 852, 'reader', 'none', {
    features: [{ name: 'prefers-reduced-motion', value: 'reduce' }]
  });
  await viewport(cdp, 320, 900);
  await navigate(cdp, url(base, 'reader'));
  await shot(cdp, join(directory, 'after-reader-400-percent-reflow-equivalent-320x900.png'));
  records.push({ file: 'after-reader-400-percent-reflow-equivalent-320x900.png', surface: 'reader', panel: 'none',
    viewport: '320x900', zoom: '400% reflow equivalent from a 1280 CSS-pixel baseline', metrics: await pageMetrics(cdp) });
  await cdp.send('Emulation.setEmulatedMedia', { media: 'screen' });

  await viewport(cdp, 1024, 768);
  await navigate(cdp, url(base, 'reader'));
  await cdp.send('Emulation.setEmulatedMedia', { media: 'print' });
  const pdf = await cdp.send('Page.printToPDF', {
    printBackground: true, preferCSSPageSize: true, paperWidth: 8.5, paperHeight: 11,
    marginTop: 0.45, marginBottom: 0.45, marginLeft: 0.5, marginRight: 0.5
  });
  await cdp.send('Emulation.setEmulatedMedia', { media: 'screen' });
  await writeFile(join(directory, 'after-reader-browser-print.pdf'), Buffer.from(pdf.data, 'base64'));
  await writeFile(join(directory, 'measurements.json'), JSON.stringify(records, null, 2) + '\n');
  return records;
}

async function main() {
  const server = staticServer();
  const serverPort = await listen(server);
  const base = `http://${LOOPBACK}:${serverPort}`;
  const debugPort = await freePort();
  const profile = await mkdtemp(join(tmpdir(), 'triptych-corpus-foundation-chrome-'));
  const chrome = spawn(chromeBinary, [
    '--headless=new', '--no-sandbox', '--disable-dev-shm-usage', '--disable-gpu',
    `--remote-debugging-port=${debugPort}`, `--user-data-dir=${profile}`,
    '--no-first-run', '--no-default-browser-check', 'about:blank'
  ], { stdio: ['ignore', 'ignore', 'pipe'] });
  let chromeStderr = '';
  chrome.stderr.on('data', (chunk) => { chromeStderr += chunk.toString(); });
  let cdp;
  try {
    await waitForJson(`http://${LOOPBACK}:${debugPort}/json/version`);
    const pageResponse = await fetch(
      `http://${LOOPBACK}:${debugPort}/json/new?${encodeURIComponent('about:blank')}`,
      { method: 'PUT' }
    );
    const page = await pageResponse.json();
    cdp = new CDP(page.webSocketDebuggerUrl);
    await cdp.ready();
    await Promise.all([
      cdp.send('Page.enable'), cdp.send('Runtime.enable'), cdp.send('Network.enable'),
      cdp.send('Accessibility.enable'), cdp.send('Performance.enable')
    ]);
    cdp.on('Runtime.consoleAPICalled', ({ type, args }) => {
      if (['error', 'warning'].includes(type)) consoleProblems.push({
        type, text: args.map((arg) => arg.value || arg.description || '').join(' ')
      });
    });
    cdp.on('Network.loadingFailed', (event) => failedRequests.push({
      requestId: event.requestId, error: event.errorText, canceled: Boolean(event.canceled)
    }));
    cdp.on('Network.responseReceived', ({ response }) => {
      if (response.status >= 400) httpProblems.push({ status: response.status, url: response.url });
    });

    await runAssertions(cdp, base);
    const captures = captureDir ? await captureMatrix(cdp, base, captureDir) : [];
    await viewport(cdp, 1440, 900);
    await navigate(cdp, url(base));
    const ax = await cdp.send('Accessibility.getFullAXTree');
    const unnamedInteractiveNodes = ax.nodes.filter((node) =>
      ['button', 'link', 'textbox'].includes(node.role?.value) && !node.name?.value).length;
    const version = await waitForJson(`http://${LOOPBACK}:${debugPort}/json/version`);
    const report = {
      generatedAt: new Date().toISOString(),
      chrome: version.Browser,
      assertions: observations,
      failures,
      consoleProblems,
      failedRequests,
      httpProblems,
      accessibility: { nodeCount: ax.nodes.length, unnamedInteractiveNodes },
      captures: captures.length,
      files: {
        html: (await stat(join(ROOT, 'src/web/browser/prototypes/corpus-foundation/index.html'))).size,
        css: (await stat(join(ROOT, 'src/web/browser/prototypes/corpus-foundation/prototype.css'))).size,
        javascript: (await stat(join(ROOT, 'src/web/browser/prototypes/corpus-foundation/prototype.js'))).size
      }
    };
    if (captureDir) await writeFile(join(captureDir, 'browser-results.json'), JSON.stringify(report, null, 2) + '\n');
    process.stdout.write(JSON.stringify(report, null, 2) + '\n');
    const unexpectedFailed = failedRequests.filter((one) => !one.canceled);
    if (failures.length || unnamedInteractiveNodes || consoleProblems.length ||
        unexpectedFailed.length || httpProblems.length) process.exitCode = 1;
  } catch (error) {
    process.stderr.write((error.stack || String(error)) + '\n' + chromeStderr.slice(-4000));
    process.exitCode = 1;
  } finally {
    if (cdp) cdp.close();
    chrome.kill('SIGTERM');
    await new Promise((accept) => server.close(accept));
  }
}

await main();
