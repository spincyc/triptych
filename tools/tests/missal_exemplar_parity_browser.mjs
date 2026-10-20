#!/usr/bin/env node
/* Source-served Chromium observations for the 1962 Pentecost parity test. */

import { spawn } from 'node:child_process';
import { createServer } from 'node:http';
import { mkdir, mkdtemp, readFile, rm } from 'node:fs/promises';
import { extname, join, resolve, sep } from 'node:path';

const root = resolve(import.meta.dirname, '../..');
const chromeBinary = process.env.TRIPTYCH_CHROME || '/usr/bin/chromium';

function listen(server) {
  return new Promise((accept, reject) => {
    server.once('error', reject);
    server.listen(0, '127.0.0.1', () => accept(server.address().port));
  });
}

function server() {
  return createServer(async (request, response) => {
    try {
      let path = decodeURIComponent(new URL(request.url, 'http://localhost').pathname).replace(/^\/+/, '');
      if (path === 'favicon.ico') {
        response.writeHead(204).end();
        return;
      }
      if (/^src\/web\/data\/[^/]+\/chapters\//.test(path)) {
        path = path.replace(/^src\/web\/data\//, 'src/sources/bibles/');
      }
      const file = resolve(root, path);
      if (!file.startsWith(root + sep)) throw new Error('path outside root');
      const body = await readFile(file);
      const mime = {
        '.html': 'text/html; charset=utf-8', '.js': 'text/javascript; charset=utf-8',
        '.css': 'text/css; charset=utf-8', '.json': 'application/json'
      }[extname(file)] || 'application/octet-stream';
      response.writeHead(200, { 'content-type': mime, 'cache-control': 'no-store' }).end(body);
    } catch {
      response.writeHead(404).end('not found');
    }
  });
}

async function waitJson(url) {
  for (let attempt = 0; attempt < 100; attempt += 1) {
    try {
      const response = await fetch(url);
      if (response.ok) return response.json();
    } catch { /* Chromium is starting. */ }
    await new Promise((accept) => setTimeout(accept, 50));
  }
  throw new Error('Chromium debugging endpoint unavailable');
}

class CDP {
  constructor(url) {
    this.socket = new WebSocket(url);
    this.next = 0;
    this.pending = new Map();
    this.listeners = new Map();
  }
  async ready() {
    await new Promise((accept, reject) => {
      this.socket.addEventListener('open', accept, { once: true });
      this.socket.addEventListener('error', reject, { once: true });
    });
    this.socket.addEventListener('message', (event) => {
      const message = JSON.parse(event.data);
      const pending = this.pending.get(message.id);
      if (!pending) {
        for (const listener of this.listeners.get(message.method) || []) {
          listener(message.params || {});
        }
        return;
      }
      this.pending.delete(message.id);
      clearTimeout(pending.timer);
      if (message.error) pending.reject(new Error(message.error.message));
      else pending.accept(message.result);
    });
  }
  on(method, listener) {
    this.listeners.set(method, [...(this.listeners.get(method) || []), listener]);
  }
  send(method, params = {}) {
    const id = ++this.next;
    return new Promise((accept, reject) => {
      const timer = setTimeout(() => reject(new Error('CDP timeout: ' + method)), 20000);
      this.pending.set(id, { accept, reject, timer });
      this.socket.send(JSON.stringify({ id, method, params }));
    });
  }
  close() { this.socket.close(); }
}

async function evaluate(cdp, expression) {
  const result = await cdp.send('Runtime.evaluate', { expression, returnByValue: true });
  if (result.exceptionDetails) throw new Error(result.exceptionDetails.text);
  return result.result.value;
}

async function observe(cdp, url, debug) {
  await cdp.send('Page.navigate', { url });
  for (let attempt = 0; attempt < 240; attempt += 1) {
    const ready = await evaluate(cdp,
      `Boolean(performance.getEntriesByType('navigation')[0]?.name.split('#')[0] === ${JSON.stringify(url.split('#')[0])} && ` +
      `window.${debug}?.ready && document.querySelector('#reader-document')?.getAttribute('aria-busy') === 'false')`);
    if (ready) break;
    if (attempt === 239) throw new Error('Reader did not settle: ' + url);
    await new Promise((accept) => setTimeout(accept, 50));
  }
  return evaluate(cdp, `(() => {
    const debug = window.${debug};
    const ids = [...document.querySelectorAll('#reader-document [data-semantic-event-id]')]
      .map(node => node.dataset.semanticEventId);
    return {
      outcome: debug.outcome, resolved: debug.semantic.resolved,
      events: debug.semantic.events, domIds: ids,
      unresolvedChoices: debug.semantic.unresolvedChoices || [],
      ordinaryUnresolved: debug.semantic.ordinaryUnresolved || [],
      calendarResult: debug.semantic.calendarResult || null,
      title: document.querySelector('.celebration-title')?.textContent || '',
      lesson: document.querySelector('[data-semantic-event-id="proper/roman-1962/pentecost/003"]')?.innerText || '',
      variableNodes: [...document.querySelectorAll('#reader-document [data-semantic-event-id]')]
        .filter(node => /praefatio-de-spiritu-sancto|communicantes-pentecoste|hanc-igitur-pascha-pentecoste/.test(node.dataset.semanticEventId))
        .map(node => ({ id: node.dataset.semanticEventId, text: node.innerText })),
      literalLeaks: [...document.querySelectorAll('#reader-document [data-semantic-event-id]')]
        .filter(node => /\\bundefined\\b|\\bnull\\b|\\bNaN\\b|\\[object Object\\]/.test(node.innerText))
        .map(node => ({ id: node.dataset.semanticEventId, text: node.innerText.slice(0, 240) })),
      pageLeaks: document.body.innerText.match(/\\bundefined\\b|\\bnull\\b|\\bNaN\\b|\\[object Object\\]/g) || [],
      coverageNotice: document.querySelector('#coverage-notice')?.textContent || ''
    };
  })()`);
}

async function main() {
  const http = server();
  const port = await listen(http);
  const debugServer = createServer();
  const debugPort = await listen(debugServer);
  await new Promise((accept) => debugServer.close(accept));
  const scratch = join(root, '.scratch');
  await mkdir(scratch, { recursive: true });
  const profile = await mkdtemp(join(scratch, 'triptych-pentecost-parity-'));
  const chrome = spawn(chromeBinary, [
    '--headless=new', '--no-sandbox', '--disable-dev-shm-usage', '--disable-gpu',
    `--remote-debugging-port=${debugPort}`, `--user-data-dir=${profile}`,
    '--no-first-run', '--no-default-browser-check', 'about:blank'
  ], { stdio: ['ignore', 'ignore', 'pipe'] });
  let stderr = '';
  chrome.stderr.on('data', chunk => { stderr += chunk.toString(); });
  let cdp;
  try {
    await waitJson(`http://127.0.0.1:${debugPort}/json/version`);
    const pageResponse = await fetch(
      `http://127.0.0.1:${debugPort}/json/new?about:blank`, { method: 'PUT' });
    const page = await pageResponse.json();
    cdp = new CDP(page.webSocketDebuggerUrl);
    await cdp.ready();
    const problems = [];
    cdp.on('Runtime.exceptionThrown', ({ exceptionDetails }) => {
      problems.push(exceptionDetails?.text || 'JavaScript exception');
    });
    cdp.on('Network.loadingFailed', ({ canceled, errorText }) => {
      if (!canceled) problems.push(errorText || 'Network load failed');
    });
    cdp.on('Network.responseReceived', ({ response }) => {
      if (response?.status >= 400) problems.push(`${response.status} ${response.url}`);
    });
    await Promise.all([
      cdp.send('Page.enable'), cdp.send('Runtime.enable'), cdp.send('Network.enable')
    ]);
    const base = `http://127.0.0.1:${port}`;
    const day = `${base}/src/web/browser/liturgy/day.html?data=/src/web/data#` +
      'date=2026-05-24&missal=roman-1962&bible=douay-rheims&orations=la&mass=pentecost';
    const propers = `${base}/src/web/browser/liturgy/index.html?data=/src/web/data#` +
      'missal=roman-1962&type=seasonal&mass=pentecost&bible=douay-rheims&orations=la';
    const postDay = `${base}/src/web/browser/liturgy/day.html?data=/src/web/data#` +
      'date=2026-05-24&missal=postconciliar&bible=douay-rheims&orations=la&mass=pentecost&form=day';
    const preDay = `${base}/src/web/browser/liturgy/day.html?data=/src/web/data#` +
      'date=2026-05-24&missal=roman-pre-1955&bible=douay-rheims&orations=la&mass=pentecost';
    const postPropers = `${base}/src/web/browser/liturgy/index.html?data=/src/web/data#` +
      'missal=postconciliar&type=seasonal&mass=pentecost&form=day&bible=douay-rheims&orations=la';
    const prePropers = `${base}/src/web/browser/liturgy/index.html?data=/src/web/data#` +
      'missal=roman-pre-1955&type=seasonal&mass=pentecost&bible=douay-rheims&orations=la';
    const tagged = (url, tag) => url.replace('?data=/src/web/data#',
      `?data=/src/web/data&parity=${tag}#`);
    const result = {
      dayRead: await observe(cdp, tagged(day + '&ordinary=0', 'day-read'), 'dayReaderDebug'),
      dayMissal: await observe(cdp,
        tagged(day + '&ordinary=1&ordinary-lang=la', 'day-missal'), 'dayReaderDebug'),
      propersRead: await observe(cdp, tagged(propers, 'propers-read'), 'propersReaderDebug'),
      propersMissal: await observe(cdp,
        tagged(propers + '&mode=missal&ordinary-lang=la', 'propers-missal'),
        'propersReaderDebug'),
      dayEnglish: await observe(cdp,
        tagged(day.replace('orations=la', 'orations=en') + '&ordinary=0', 'day-english'),
        'dayReaderDebug'),
      postDayMissal: await observe(cdp,
        tagged(postDay + '&ordinary=1&ordinary-lang=en', 'post-day-missal'),
        'dayReaderDebug'),
      postPropersMissal: await observe(cdp,
        tagged(postPropers + '&mode=missal&ordinary-lang=en', 'post-propers-missal'),
        'propersReaderDebug'),
      preDayMissal: await observe(cdp,
        tagged(preDay + '&ordinary=1&ordinary-lang=en', 'pre-day-missal'),
        'dayReaderDebug'),
      prePropersMissal: await observe(cdp,
        tagged(prePropers + '&mode=missal&ordinary-lang=en', 'pre-propers-missal'),
        'propersReaderDebug')
    };
    result.problems = problems;
    process.stdout.write(JSON.stringify(result));
  } catch (error) {
    process.stderr.write((error.stack || String(error)) + '\n' + stderr.slice(-2000));
    process.exitCode = 1;
  } finally {
    cdp?.close();
    if (chrome.exitCode === null) {
      chrome.kill();
      await new Promise((accept) => chrome.once('exit', accept));
    }
    await new Promise((accept) => http.close(accept));
    await rm(profile, { recursive: true, force: true });
  }
}

await main();
