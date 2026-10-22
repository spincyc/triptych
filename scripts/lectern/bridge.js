'use strict';
/*
 * The browser's own scripts, served to the terminal reader over stdin/stdout.
 *
 * The pages are assemblers: `browser-core.js` fetches, a page's model derives.
 * This process is one realm set up the way a page is — `window`, `location`,
 * and a `fetch` that answers from the checkout exactly as `tools/public-alpha`
 * lays the site's data root out — so each model runs unchanged, and nothing
 * here derives anything a model or the generator already decides.
 *
 * Requests, one per line: {"id", "adapter", "fn", "args"}. An adapter is a file
 * under adapters/ beside this one, which calls the page's model in the page's
 * order. Replies, one per line: {"id", "ok": true, "value"} or {"id", "ok":
 * false, "error"}.
 */
const fs = require('fs');
const path = require('path');
const readline = require('readline');
const vm = require('vm');

const ROOT = path.resolve(__dirname, '..', '..');
const DATA = path.join(ROOT, 'src', 'web', 'data');
const BIBLES = path.join(ROOT, 'src', 'sources', 'bibles');
const BROWSER = path.join(ROOT, 'src', 'web', 'browser');
const SITE = '../browse/';

function inside(base, file) {
  const relative = path.relative(base, file);
  return relative && !relative.startsWith('..') && !path.isAbsolute(relative);
}

let offered = null;
/* Only an edition the published manifest offers is served, as the deploy
 * copies only those (guidance/web-data.md, "Assembling the site"). */
function offeredEditions() {
  if (offered) return offered;
  try {
    const manifest = JSON.parse(fs.readFileSync(path.join(DATA, 'bibles.json'), 'utf8'));
    offered = new Set((manifest.bibles || []).map((one) => one && one.id).filter(Boolean));
  } catch (error) {
    offered = new Set();
  }
  return offered;
}

function onDisk(relative) {
  if (relative === 'bibles.json' || relative.startsWith('structure/')) {
    const file = path.resolve(DATA, relative);
    return inside(DATA, file) ? file : null;
  }
  const match = /^([a-z0-9][a-z0-9-]*)\/chapters\/(.+)$/.exec(relative);
  if (match && offeredEditions().has(match[1])) {
    const base = path.join(BIBLES, match[1], 'chapters');
    const file = path.resolve(base, match[2]);
    return inside(base, file) ? file : null;
  }
  return null;
}

function siteFetch(url, options) {
  const relative = String(url).replace(/^\.\.\/browse\//, '').split('#')[0].split('?')[0];
  const file = onDisk(relative);
  const reply = (status, text) => ({
    status: status,
    ok: status >= 200 && status < 300,
    text: () => Promise.resolve(text),
    json: () => Promise.resolve(JSON.parse(text)),
  });
  if (!file) return Promise.resolve(reply(404, ''));
  try {
    const head = options && options.method === 'HEAD';
    return Promise.resolve(reply(200, head ? '' : fs.readFileSync(file, 'utf8')));
  } catch (error) {
    if (error.code === 'ENOENT' || error.code === 'ENOTDIR') return Promise.resolve(reply(404, ''));
    return Promise.reject(error);
  }
}

/* The realm. `runInThisContext` leaves no `module` in scope, so each UMD
 * script takes its browser branch and sets its global, exactly as on a page;
 * a script run in a separate vm context would parse JSON whose prototypes the
 * models refuse. */
const dom = require('./dom.js');
globalThis.window = globalThis;
globalThis.self = globalThis;
globalThis.document = dom.document;
globalThis.location = { search: '', hash: '', pathname: '/' };
globalThis.history = { replaceState() {}, pushState() {} };
globalThis.addEventListener = () => {};
globalThis.fetch = siteFetch;

const loaded = new Set();
function script(relative) {
  if (loaded.has(relative)) return;
  const file = path.resolve(BROWSER, relative);
  if (!inside(BROWSER, file)) throw new Error(`outside src/web/browser: ${relative}`);
  vm.runInThisContext(fs.readFileSync(file, 'utf8'), { filename: file });
  loaded.add(relative);
}

function read(relative) {
  const file = onDisk(relative);
  if (!file || !fs.existsSync(file)) return undefined;
  return JSON.parse(fs.readFileSync(file, 'utf8'));
}

const realm = { ROOT, DATA, SITE, script, read, dom, fetch: siteFetch };
const adapters = new Map();
function adapter(name) {
  if (!/^[a-z][a-z-]*$/.test(name)) throw new Error(`no adapter named ${name}`);
  if (!adapters.has(name)) adapters.set(name, require(path.join(__dirname, 'adapters', name + '.js'))(realm));
  return adapters.get(name);
}

async function answer(request) {
  const api = adapter(request.adapter);
  // Only what the adapter itself exports: never an inherited name such as
  // `constructor`, which every object answers to.
  const fn = Object.prototype.hasOwnProperty.call(api, request.fn) ? api[request.fn] : undefined;
  if (typeof fn !== 'function') throw new Error(`the ${request.adapter} adapter has no ${request.fn}`);
  return fn.apply(api, request.args || []);
}

/* Requests are answered strictly in order, one at a time. */
let queue = Promise.resolve();
const lines = readline.createInterface({ input: process.stdin, terminal: false });
lines.on('line', (line) => {
  if (!line.trim()) return;
  queue = queue.then(async () => {
    let request;
    try {
      request = JSON.parse(line);
      const value = await answer(request);
      process.stdout.write(JSON.stringify({ id: request.id, ok: true, value: value === undefined ? null : value }) + '\n');
    } catch (error) {
      process.stdout.write(JSON.stringify({
        id: request && request.id, ok: false, error: String((error && error.message) || error),
      }) + '\n');
    }
  });
});
