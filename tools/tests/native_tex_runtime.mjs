import assert from 'node:assert/strict';
import { readFile } from 'node:fs/promises';
import { createHash, webcrypto } from 'node:crypto';
import vm from 'node:vm';
import test from 'node:test';
import { gzipSync } from 'node:zlib';

const source = await readFile(new URL('../../src/web/browser/shared/native-tex.js', import.meta.url), 'utf8');
const encode = value => new TextEncoder().encode(value);
const hash = value => createHash('sha256').update(value).digest('hex');

function fixture(change = {}) {
  const tex = encode('\\documentclass{article}\\begin{document}Original TeX\\end{document}');
  const file = { path: 'src/gpt/example/main.tex', encoding: 'utf8', content: new TextDecoder().decode(tex), bytes: tex.length, sha256: hash(tex) };
  const bundle = {
    schema: 'triptych-native-print-source-bundle/v1', document: 'publication:gpt/example',
    output_id: 'gpt/example', edition: 'main', source_revision: 'a'.repeat(40), engine: 'pdftex', format: 'pdflatex',
    cwd: 'src/gpt', entrypoint: file.path, environment: { TEXINPUTS: '..:' },
    options: { shell_escape: false, max_passes: 8, minimum_passes: 2, settle_auxiliary_files: true }, files: [file]
  };
  if (change.bundle) change.bundle(bundle);
  const resources = new Map();
  function pin(name, value = name) {
    const bytes = typeof value === 'string' ? encode(value) : value;
    resources.set('/' + name, bytes);
    return { url: name, bytes: bytes.length, sha256: hash(bytes) };
  }
  const runtime = {
    schema: 'triptych-native-tex-runtime/v1', id: 'test-pinned-runtime', texFiles: [],
    engines: { pdflatex: { worker: pin('test.worker.js'), core: pin('test.js'), wasm: pin('test.wasm'), format: pin('test.fmt') } }
  };
  if (change.runtime) change.runtime(runtime, pin);
  const bundlePin = pin('bundle.json', JSON.stringify(bundle));
  const runtimePin = pin('runtime.json', JSON.stringify(runtime));
  const workers = [];
  const messages = [];
  const transfers = [];
  const liveBlobs = new Set();
  let peakBlobs = 0;
  class FixtureURL extends URL {
    static createObjectURL(blob) {
      const url = URL.createObjectURL(blob); liveBlobs.add(url); peakBlobs = Math.max(peakBlobs, liveBlobs.size); return url;
    }
    static revokeObjectURL(url) { liveBlobs.delete(url); URL.revokeObjectURL(url); }
  }
  class FakeWorker {
    constructor() {
      if (change.workerCreated) change.workerCreated(workers);
      this.index = workers.length; this.deferred = new Set();
      this.passes = 0; this.terminated = false; this.packageData = new Map(); workers.push(this);
      queueMicrotask(() => this.onmessage({ data: { result: 'ok' } }));
    }
    postMessage(payload, transfer = []) {
      if (change.postError && payload.cmd === 'writefile') throw new DOMException('Cannot clone the source payload', 'DataCloneError');
      const sizes = Array.from(transfer, buffer => buffer.byteLength);
      payload = structuredClone(payload, { transfer });
      transfers.push({ cmd: payload.cmd, sizes, detached: transfer.every(buffer => buffer.byteLength === 0) });
      let recorded = payload;
      if (payload.cmd === 'triptych-preload') {
        for (const item of payload.payloads) this.packageData.set(item.id, item.data);
        for (const file of payload.files) if (file.deferred) this.deferred.add(file.fileId);
        recorded = { ...payload, files: payload.files.map(file => ({ ...file, data: this.packageData.get(file.fileId) })) };
      }
      messages.push(structuredClone(recorded));
      if (payload.cmd === 'triptych-preload' && payload.final && !payload.retain) this.packageData.clear();
      if (payload.cmd === 'setmainfile') return;
      if (change.hang && payload.cmd === 'compilelatex') return;
      let data = { cmd: payload.cmd, result: 'ok' };
      if (payload.cmd === 'compilelatex' || payload.cmd === 'compilepdf') {
        this.passes++;
        data = { cmd: 'compile', result: 'ok', status: 0, log: change.log || 'Output written on main.pdf (1 page).',
          nativeInventory: true, nativeMissing: [], pdf: encode('%PDF-1.4\nNative test result').buffer };
        if (change.compile) change.compile(data, this);
      }
      if (payload.cmd === 'triptych-configure') data.nativeInventory = !change.noInventoryTracking;
      if (payload.cmd === 'triptych-state') data.files = [{ path: 'main.aux', bytes: encode(change.unsettled ? String(this.passes) : 'settled').buffer }];
      let returned = [];
      if (payload.cmd === 'triptych-take-packages') {
        data.payloads = Array.from(this.packageData, ([id, data]) => ({ id, data }));
        if (change.returnedPackages) change.returnedPackages(data.payloads);
        this.packageData.clear();
        returned = data.payloads.map(item => item.data);
      }
      queueMicrotask(() => { if (!this.terminated) this.onmessage({ data: structuredClone(data, { transfer: returned }) }); });
    }
    terminate() { this.terminated = true; }
  }
  const fetches = [];
  const context = vm.createContext({
    window: { caches: change.caches }, document: { baseURI: change.baseURI || 'https://example.test/' }, URL: FixtureURL, Blob, Response, ReadableStream,
    DecompressionStream: change.noDecompression ? undefined : change.DecompressionStream || DecompressionStream,
    TextEncoder, TextDecoder, Uint8Array, ArrayBuffer, DOMException, AbortController,
    crypto: change.crypto || webcrypto, Date: change.clock ? { now: change.clock } : Date,
    atob, setTimeout, clearTimeout, Worker: change.noWorker ? undefined : FakeWorker,
    WebAssembly: change.noWebAssembly ? undefined : WebAssembly,
    fetch: async (url, options) => {
      fetches.push(String(url));
      if (options.signal.aborted) throw new DOMException('Cancelled', 'AbortError');
      const bytes = resources.get(new URL(url).pathname);
      const respond = () => new Response(bytes || 'Not found', { status: bytes ? 200 : 404, headers: { 'content-length': String(bytes?.length || 9) } });
      return change.fetch ? change.fetch(url, options, respond) : respond();
    }
  });
  if (change.deniedCacheGetter) Object.defineProperty(context.window, 'caches', {
    get() { throw new DOMException('Storage denied', 'SecurityError'); }
  });
  vm.runInContext(source, context);
  const options = { bundleURL: bundlePin.url, bundleSHA256: bundlePin.sha256, bundleBytes: bundlePin.bytes,
    runtimeURL: runtimePin.url, runtimeSHA256: runtimePin.sha256, runtimeBytes: runtimePin.bytes };
  return { generate: context.window.TriptychNativeTeX.generate, options, resources, workers, messages, fetches, transfers,
    liveBlobs, peakBlobs: () => peakBlobs };
}

function packages(runtime, pin, packed = true) {
  const one = encode('First original package');
  const two = encode('Second original package, with a different length');
  const first = pin('first.sty', one);
  const second = pin('second.sty', two);
  runtime.texFiles = [
    { ...first, format: 26, name: 'first.sty' },
    { ...first, format: 26, name: 'first-alias.sty' },
    { ...second, format: 26, name: 'second.sty' }
  ];
  if (packed) runtime.texPacks = [{
    ...pin('packages.bin', gzipSync(Buffer.concat([one, two]))), compression: 'gzip', expanded_bytes: one.length + two.length,
    files: [{ sha256: first.sha256, bytes: one.length, offset: 0 },
      { sha256: second.sha256, bytes: two.length, offset: one.length }]
  }];
}

function unicodeRuntime(runtime, pin) {
  packages(runtime, pin);
  runtime.engines.xelatex = { ...runtime.engines.pdflatex, icu: pin('icu.dat'),
    format: pin('unicode.fmt.gz', gzipSync(encode('original Unicode format'))) };
  runtime.engines.dvipdfmx = { worker: pin('converter.worker.js'), core: pin('converter.js'), wasm: pin('converter.wasm') };
}

function deferredPackages(runtime, pin) {
  packages(runtime, pin);
  for (let index = 0; index < 4; index++) {
    const body = encode('Original font ' + index);
    const font = pin('font-' + index + '.pfb', body);
    runtime.texFiles.push({ ...font, format: 32, name: 'font-' + index + '.pfb' });
    runtime.texPacks.push({ ...pin('font-' + index + '.bin', gzipSync(body)), compression: 'gzip',
      expanded_bytes: body.length, deferred: true,
      files: [{ sha256: font.sha256, bytes: body.length, offset: 0 }] });
  }
}

function renderIdentity(bundle) {
  const rendered = Object.fromEntries(['document', 'output_id', 'edition', 'engine', 'format', 'entrypoint', 'cwd',
    'environment', 'options'].map(key => [key, bundle[key]]));
  rendered.files = bundle.files.map(({ path, bytes, sha256 }) => ({ path, bytes, sha256 }))
    .sort((a, b) => a.path < b.path ? -1 : a.path > b.path ? 1 : 0);
  const canonical = value => Array.isArray(value) ? '[' + value.map(canonical).join(',') + ']' :
    value && typeof value === 'object' ? '{' + Object.keys(value).sort().map(key => JSON.stringify(key) + ':' + canonical(value[key])).join(',') + '}' : JSON.stringify(value);
  bundle.render_sha256 = hash(encode(canonical(rendered)));
}

function addTransport(resource, pin, body = resource.url) {
  resource.transport = { ...pin(resource.url + '.transport.bin', gzipSync(encode(body))), compression: 'gzip' };
}

function memoryCaches(change = {}) {
  const entries = new Map();
  const key = value => typeof value === 'string' ? value : value.url;
  const cache = {
    async match(request) { return entries.get(key(request))?.clone(); },
    async keys() { return Array.from(entries.keys(), url => ({ url })); },
    async delete(request) { return entries.delete(key(request)); },
    async put(request, response) {
      if (change.put) await change.put();
      entries.set(key(request), response.clone());
    }
  };
  return { entries, async open() { if (change.open) await change.open(); return cache; } };
}

test('verified native generation preserves cwd and settles auxiliary files before offering PDF', async () => {
  const f = fixture();
  const result = await f.generate(f.options);
  assert.equal(result.passes, 2);
  assert.equal(result.sha256, hash(result.bytes));
  assert.equal(f.messages.find(v => v.cmd === 'triptych-configure').cwd, 'src/gpt');
  assert.equal(f.messages.find(v => v.cmd === 'triptych-configure').texinputs, '..:');
  assert.equal(f.messages.find(v => v.cmd === 'writefile').url, 'src/gpt/example/main.tex');
  assert.equal(f.messages.find(v => v.cmd === 'setmainfile').url, 'example/main.tex');
  assert.ok(f.workers.every(v => v.terminated));
});

test('provider-neutral bundles retain their empty native environment', async () => {
  const f = fixture({ bundle: value => { value.environment = {}; } });
  await f.generate(f.options);
  assert.equal(f.messages.find(v => v.cmd === 'triptych-configure').texinputs, '');
});

test('unused deferred font packs are not fetched and placeholders preserve the complete lookup inventory', async () => {
  const f = fixture({ runtime: deferredPackages });
  await f.generate(f.options);
  assert.equal(f.workers.length, 1);
  assert.ok(!f.fetches.some(url => /font-\d\.(?:bin|pfb)$/.test(url)));
  const mounted = f.messages.filter(message => message.cmd === 'triptych-preload').flatMap(message => message.files);
  assert.equal(mounted.filter(file => file.deferred).length, 4);
  assert.equal(mounted.length, 7);
});

test('both successful optional probes and fatal missing-font results restart before PDF or log acceptance', async () => {
  for (const fatal of [false, true]) {
    const caches = memoryCaches();
    const f = fixture({ caches, runtime: deferredPackages, compile: (data, worker) => {
      if (worker.index !== 0) return;
      data.nativeMissing = [Array.from(worker.deferred)[0]];
      data.pdf = encode('%PDF-1.4\nPROVISIONAL MUST NOT ESCAPE').buffer;
      if (fatal) { data.status = 1; data.result = 'failed'; data.log = '! Missing font'; }
    } });
    const result = await f.generate(f.options);
    assert.equal(f.workers.length, 2);
    assert.equal(f.workers[0].passes, 1);
    assert.equal(f.workers[1].passes, 2);
    assert.ok(f.workers.every(worker => worker.terminated));
    assert.ok(!new TextDecoder().decode(result.bytes).includes('PROVISIONAL'));
    assert.equal(f.messages.filter(message => message.cmd === 'writefile').length, 2, 'pristine sources are mounted in each worker');
    assert.equal(f.messages.filter(message => message.cmd === 'loadformat').length, 2, 'format transfers never reuse detached buffers');
    assert.equal(caches.entries.size, 1);
    assert.equal(f.fetches.filter(url => /font-\d\.bin$/.test(url)).length, 1);
  }
});

test('bounded discovery uses the complete registry on the fourth attempt', async () => {
  const f = fixture({ runtime: deferredPackages, compile: (data, worker) => {
    if (worker.deferred.size) data.nativeMissing = [Array.from(worker.deferred)[0]];
  } });
  await f.generate(f.options);
  assert.equal(f.workers.length, 4);
  assert.equal(f.workers.at(-1).deferred.size, 0);
  assert.ok(f.workers.every(worker => worker.terminated));
  assert.equal(f.liveBlobs.size, 0);
  assert.equal(f.peakBlobs(), 4, 'retired worker resources are released before every retry');
});

test('split font-group packs arrive together without fetching unrelated fonts', async () => {
  const f = fixture({ runtime: (runtime, pin) => {
    deferredPackages(runtime, pin);
    runtime.texPacks[1].font_group = runtime.texPacks[2].font_group = 'a'.repeat(64);
  }, compile: (data, worker) => {
    if (worker.index === 0) data.nativeMissing = [Array.from(worker.deferred)[0]];
  } });
  await f.generate(f.options);
  assert.equal(f.workers.length, 2);
  assert.equal(f.workers[1].deferred.size, 2);
  assert.equal(f.fetches.filter(url => /font-\d\.bin$/.test(url)).length, 2);
});

test('cancellation during discovery closes workers and cannot retain a provisional PDF', async () => {
  const controller = new AbortController();
  const caches = memoryCaches();
  const f = fixture({ caches, runtime: deferredPackages, compile: (data, worker) => {
    data.nativeMissing = [Array.from(worker.deferred)[0]];
  }, fetch: (url, options, respond) => {
    if (url.endsWith('/font-0.bin')) { controller.abort(); throw new DOMException('Cancelled', 'AbortError'); }
    return respond();
  } });
  await assert.rejects(f.generate({ ...f.options, signal: controller.signal }), error => error.name === 'AbortError');
  assert.ok(f.workers.every(worker => worker.terminated));
  assert.equal(f.liveBlobs.size, 0);
  assert.equal(caches.entries.size, 0);
});

test('Unicode converter discovery restarts original TeX and never reuses transferred provisional output', async () => {
  const f = fixture({ bundle: bundle => { bundle.engine = 'xetex'; bundle.format = 'xelatex'; },
    runtime: (runtime, pin) => { unicodeRuntime(runtime, pin); deferredPackages(runtime, pin); },
    compile: (data, worker) => {
      if (worker.index === 1) { data.nativeMissing = [Array.from(worker.deferred)[0]]; data.status = 1; data.result = 'failed'; }
    } });
  await f.generate(f.options);
  assert.deepEqual(f.workers.map(worker => worker.passes), [2, 1, 2, 1]);
  assert.ok(f.workers.every(worker => worker.terminated));
  assert.equal(f.liveBlobs.size, 0);
  assert.equal(f.messages.filter(message => message.cmd === 'triptych-take-packages').length, 2);
  assert.equal(f.messages.filter(message => message.cmd === 'writefile' && message.url === 'main.xdv').length, 2);
});

test('unsupported inventory tracking falls back before executing an incomplete worker', async () => {
  const f = fixture({ noInventoryTracking: true, runtime: deferredPackages });
  await f.generate(f.options);
  assert.equal(f.workers.length, 2);
  assert.equal(f.workers[0].passes, 0);
  assert.equal(f.workers[1].deferred.size, 0);
});

test('missing, duplicated or unknown discovery receipts cannot publish a successful PDF', async () => {
  for (const mutate of [(data) => { delete data.nativeMissing; },
    (data) => { data.nativeMissing = ['unowned']; },
    (data, worker) => { const id = Array.from(worker.deferred)[0]; data.nativeMissing = [id, id]; }]) {
    const caches = memoryCaches();
    const f = fixture({ caches, runtime: deferredPackages, compile: mutate });
    await assert.rejects(f.generate(f.options), /complete package inventory/);
    assert.equal(caches.entries.size, 0);
    assert.ok(f.workers.every(worker => worker.terminated));
  }
});

test('deferred font corruption never falls back to unverified raw bytes or a provisional PDF', async () => {
  const f = fixture({ runtime: deferredPackages, compile: (data, worker) => {
    data.nativeMissing = [Array.from(worker.deferred)[0]];
  } });
  f.resources.set('/font-0.bin', encode('changed compressed font'));
  await assert.rejects(f.generate(f.options), /changed/);
  assert.ok(!f.fetches.some(url => url.endsWith('/font-0.pfb')));
  assert.ok(f.workers.every(worker => worker.terminated));
});

test('render cache reuses exact content across provenance changes but invalidates shared style changes', async () => {
  const caches = memoryCaches();
  const first = fixture({ caches, bundle: renderIdentity });
  await first.generate(first.options);
  const revision = fixture({ caches, bundle: bundle => { bundle.source_revision = 'b'.repeat(40); renderIdentity(bundle); } });
  const result = await revision.generate(revision.options);
  assert.equal(result.cached, true);
  assert.equal(result.source_revision, 'b'.repeat(40));
  assert.equal(revision.workers.length, 0);
  const changed = fixture({ caches, bundle: bundle => {
    const file = bundle.files[0]; file.content += '\n% current shared style';
    file.bytes = encode(file.content).length; file.sha256 = hash(encode(file.content)); renderIdentity(bundle);
  } });
  assert.equal((await changed.generate(changed.options)).cached, false);
  assert.equal(changed.workers.length, 1);
});

test('changed source bundle is refused before worker execution', async () => {
  const f = fixture();
  f.resources.set('/bundle.json', encode('{}'));
  await assert.rejects(f.generate(f.options), /resource changed/);
  assert.equal(f.workers.length, 0);
});

test('source path traversal and duplicate files are refused', async () => {
  for (const change of [value => { value.files[0].path = '../outside.tex'; }, value => { value.files.push(value.files[0]); }]) {
    const f = fixture({ bundle: change });
    await assert.rejects(f.generate(f.options), /source path|Duplicate/);
    assert.equal(f.workers.length, 0);
  }
});

test('changed canonical TeX is refused despite a valid outer bundle hash', async () => {
  const f = fixture({ bundle: value => { value.files[0].content += 'changed'; } });
  await assert.rejects(f.generate(f.options), /source or illustration failed/);
  assert.equal(f.workers.length, 0);
});

test('external runtime or source resource is refused without requesting it', async () => {
  const f = fixture({ runtime: value => { value.engines.pdflatex.worker.url = 'https://elsewhere.test/worker.js'; } });
  await assert.rejects(f.generate(f.options), /served by this website/);
  assert.ok(f.fetches.every(url => new URL(url).origin === 'https://example.test'));
  assert.equal(f.workers.length, 0);
});

test('runtime engine bytes must match the publisher commitment', async () => {
  const f = fixture();
  f.resources.set('/test.wasm', encode('changed runtime'));
  await assert.rejects(f.generate(f.options), /resource changed/);
  assert.equal(f.workers.length, 0);
});

test('missing glyphs prevent an otherwise successful PDF from being offered', async () => {
  const f = fixture({ log: 'Missing character: There is no glyph in font.' });
  await assert.rejects(f.generate(f.options), /could not be typeset completely/);
  assert.ok(f.workers.every(v => v.terminated));
});

test('default font-family substitutions cannot silently replace native typography', async () => {
  const f = fixture({ log: 'LaTeX Font Warning: Some font shapes were not available,\n defaults substituted.' });
  await assert.rejects(f.generate(f.options), /could not be typeset completely/);
  assert.ok(f.workers.every(v => v.terminated));
});

test('a synchronous worker message failure closes the worker and clears pending timers', async () => {
  const f = fixture({ postError: true });
  await assert.rejects(f.generate(f.options), error => error.name === 'DataCloneError');
  assert.ok(f.workers.every(v => v.terminated));
});

test('unsettled references have a finite compile limit', async () => {
  const f = fixture({ unsettled: true });
  await assert.rejects(f.generate(f.options), /did not settle/);
  assert.equal(f.workers[0].passes, 8);
  assert.ok(f.workers.every(v => v.terminated));
});

test('cancellation terminates the native worker and rejects the pending operation', async () => {
  const f = fixture({ hang: true });
  const controller = new AbortController();
  const pending = f.generate({ ...f.options, signal: controller.signal });
  await new Promise(resolve => setTimeout(resolve, 30));
  controller.abort();
  await assert.rejects(pending, error => error.name === 'AbortError');
  assert.ok(f.workers.every(v => v.terminated));
});

test('externalized canonical illustrations retain byte commitments', async () => {
  const f = fixture({ bundle: value => { value.files.push({ path: 'art/figure.png', encoding: 'url', href: 'art.png', bytes: 3, sha256: hash(encode('art')) }); } });
  f.resources.set('/art.png', encode('art'));
  await f.generate(f.options);
  const art = f.messages.find(value => value.cmd === 'writefile' && value.url === 'art/figure.png');
  assert.equal(new TextDecoder().decode(art.src), 'art');
});

test('native cwd configuration keeps desktop font capacity and disables shell execution', () => {
  const match = source.match(/const WORKER_BRIDGE = String\.raw`([\s\S]*?)`;/);
  assert.ok(match, 'The reviewed worker bridge is present');
  for (const unicode of [false, true]) {
    const files = new Map();
    const calls = [];
    const context = {
      WORKROOT: '/work', self: { onmessage() {}, postMessage: value => calls.push(value) },
      FS: { chdir() {}, writeFile: (path, value) => files.set(path, value), readFile: path => files.get(path) },
      writeTexmfCnf() { files.set(context.WORKROOT + '/texmf.cnf', 'TEXINPUTS = .;/tex//\n'); },
      runMain: (program, args) => calls.push({ program, args })
    };
    if (unicode) context.texlive200 = {};
    else context.texlive200_cache = {};
    const isolated = vm.createContext(context);
    vm.runInContext(match[1], isolated);
    isolated.self.onmessage({ data: { cmd: 'triptych-configure', cwd: 'src/gpt', texinputs: '..:' } });
    isolated.writeTexmfCnf();
    const cnf = files.get('/work/src/gpt/texmf.cnf');
    assert.match(cnf, /font_max = 9000/);
    assert.match(cnf, /shell_escape = f/);
    assert.match(cnf, /shell_escape_commands = ,\n/);
    assert.match(cnf, /TEXINPUTS = \.;\.\.;\/tex\/\//);
    isolated.runMain('pdflatex', ['main.tex']);
    assert.ok(calls.at(-1).args.includes('-no-shell-escape'));
    if (unicode) {
      assert.equal(files.get('/work/texmf.cnf'), cnf);
      assert.equal(files.get('/work/xetex'), '');
      assert.equal(files.get('/work/xdvipdfmx'), '');
    }
  }
});

test('packed packages use one request and mount exact individual buffers for every alias', async () => {
  const f = fixture({ runtime: packages });
  await f.generate(f.options);
  assert.equal(f.fetches.length, 7, 'two manifests, one pack and four engine resources');
  assert.equal(f.fetches.filter(url => url.endsWith('/packages.bin')).length, 1);
  assert.ok(!f.fetches.some(url => /\/(first|second)\.sty$/.test(url)));
  const files = f.messages.find(value => value.cmd === 'triptych-preload').files;
  assert.deepEqual(Array.from(files, file => new TextDecoder().decode(file.data)), [
    'First original package', 'First original package', 'Second original package, with a different length'
  ]);
  assert.equal(files[0].data, files[1].data, 'aliases share one verified payload');
});

test('a runtime manifest uses its exact content pin as the HTTP cache key across releases', async () => {
  const oldRuntime = fixture().resources.get('/runtime.json');
  const requests = [];
  const f = fixture({ caches: memoryCaches(), runtime: packages,
    fetch: (url, options, respond) => {
      requests.push({ url, cache: options.cache });
      // The old stable route may still be fresh. A content-specific query
      // selects a distinct HTTP cache entry for the currently admitted bytes.
      if (url.endsWith('/runtime.json')) return new Response(oldRuntime);
      return respond();
    }
  });
  assert.equal((await f.generate(f.options)).cached, false);
  const request = requests.find(request => new URL(request.url).pathname === '/runtime.json');
  assert.equal(new URL(request.url).searchParams.get('sha256'), f.options.runtimeSHA256);
  assert.ok(requests.every(request => request.cache === 'default'));
  const before = requests.length;
  assert.equal((await f.generate(f.options)).cached, true);
  assert.equal(requests.length, before + 1, 'a completed PDF hit verifies only the current source bundle');
});

test('legacy and no-decompressor runtimes request each distinct original package once', async () => {
  for (const noDecompression of [false, true]) {
    const f = fixture({ noDecompression, runtime: (runtime, pin) => packages(runtime, pin, noDecompression) });
    await f.generate(f.options);
    assert.equal(f.fetches.length, 8);
    assert.equal(f.fetches.filter(url => url.endsWith('/first.sty')).length, 1);
    assert.equal(f.fetches.filter(url => url.endsWith('/second.sty')).length, 1);
    assert.ok(!f.fetches.some(url => url.endsWith('/packages.bin')));
  }
});

test('a present pack fails closed on invalid inventory or foreign addresses before any package fetch', async () => {
  const changes = [
    pack => { pack.files.pop(); },
    pack => { pack.files.push(pack.files[0]); },
    pack => { pack.files[1].offset--; },
    pack => { pack.files[1].offset++; },
    pack => { pack.expanded_bytes--; },
    pack => { pack.expanded_bytes++; },
    pack => { pack.files[0].sha256 = 'f'.repeat(64); },
    pack => { pack.url = 'https://elsewhere.test/pack.bin'; },
    pack => { pack.compression = 'unknown'; }
  ];
  for (const change of changes) {
    const f = fixture({ runtime: (runtime, pin) => { packages(runtime, pin); change(runtime.texPacks[0]); } });
    await assert.rejects(f.generate(f.options), /pack|served by this website/);
    assert.equal(f.workers.length, 0);
    assert.equal(f.fetches.length, 2);
  }
  const f = fixture({ runtime: (runtime, pin) => { packages(runtime, pin); runtime.texPacks = []; } });
  await assert.rejects(f.generate(f.options), /pack inventory/);
});

test('corrupt compressed bytes, member bytes and expansion overruns never fall back to original requests', async () => {
  for (const mode of ['compressed', 'member', 'expanded']) {
    const f = fixture({ runtime: (runtime, pin) => {
      packages(runtime, pin);
      if (mode !== 'compressed') {
        const bytes = Buffer.concat([encode('First original package'), encode('Second original package, with a different length')]);
        if (mode === 'member') bytes[0] ^= 1;
        const changed = mode === 'expanded' ? Buffer.concat([bytes, encode('extra')]) : bytes;
        Object.assign(runtime.texPacks[0], pin('packages.bin', gzipSync(changed)));
      }
    } });
    if (mode === 'compressed') f.resources.set('/packages.bin', encode('corrupt gzip'));
    await assert.rejects(f.generate(f.options), /changed|failed verification|exceeds its declared size/);
    assert.equal(f.workers.length, 0);
    assert.equal(f.fetches.length, 3);
  }
});

test('multi-member packs cannot exceed the eight MiB expansion limit', async () => {
  const f = fixture({ runtime: (runtime, pin) => {
    packages(runtime, pin);
    const size = 4 * 1024 * 1024 + 1;
    runtime.texFiles = [runtime.texFiles[0], runtime.texFiles[2]].map(file => ({ ...file, bytes: size }));
    runtime.texPacks[0].expanded_bytes = size * 2;
    runtime.texPacks[0].files = runtime.texFiles.map((file, index) => ({ sha256: file.sha256, bytes: size, offset: size * index }));
  } });
  await assert.rejects(f.generate(f.options), /Invalid native TeX package pack/);
  assert.equal(f.fetches.length, 2);
});

test('one failed package promptly aborts its active peers and leaves queued packages untouched', async () => {
  let aborted = 0;
  const f = fixture({
    runtime: (runtime, pin) => {
      runtime.texFiles = Array.from({ length: 12 }, (_, index) => ({ ...pin('package-' + index, 'unique package ' + index), format: 26, name: 'package-' + index }));
    },
    fetch: async (url, options, respond) => {
      if (url.endsWith('/package-0')) throw new Error('First package failed');
      if (/\/package-/.test(url)) return new Promise((resolve, reject) => {
        const abort = () => { aborted++; reject(new DOMException('Aborted', 'AbortError')); };
        options.signal.addEventListener('abort', abort, { once: true });
        if (options.signal.aborted) abort();
      });
      return respond();
    }
  });
  await assert.rejects(f.generate(f.options), /First package failed/);
  assert.equal(aborted, 3);
  assert.equal(f.fetches.filter(url => /\/package-/.test(url)).length, 4);
  assert.equal(f.workers.length, 0);
});

test('XeTeX is closed before the converter starts and both retain the original project', async () => {
  const f = fixture({
    bundle: value => { value.engine = 'xetex'; value.format = 'xelatex'; },
    runtime: (runtime, pin) => {
      runtime.engines.xelatex = { ...runtime.engines.pdflatex, icu: pin('icu.dat') };
      runtime.engines.dvipdfmx = { worker: pin('converter.worker.js'), core: pin('converter.js'), wasm: pin('converter.wasm') };
    },
    workerCreated: workers => { if (workers.length) assert.equal(workers[0].terminated, true); }
  });
  await f.generate(f.options);
  assert.equal(f.workers.length, 2);
  assert.equal(f.messages.filter(value => value.cmd === 'triptych-configure').length, 2);
  assert.ok(f.workers.every(worker => worker.terminated));
});

test('a verified completed PDF survives a reload, validates its current bundle and returns independent bytes', async () => {
  const caches = memoryCaches();
  const cold = fixture({ caches });
  const original = await cold.generate(cold.options);
  assert.equal(original.cached, false);
  original.bytes.fill(0);
  const warm = fixture({ caches });
  const reused = await warm.generate(warm.options);
  assert.equal(reused.cached, true);
  assert.equal(reused.sha256, hash(reused.bytes));
  assert.equal(reused.document, 'publication:gpt/example');
  assert.equal(warm.fetches.length, 1);
  assert.equal(warm.workers.length, 0);
  reused.bytes.fill(1);
  const again = await warm.generate(warm.options);
  assert.equal(again.sha256, hash(again.bytes));
});

test('cache identity includes both exact commitments, source URLs and deployment origin', async () => {
  const caches = memoryCaches();
  const first = fixture({ caches });
  await first.generate(first.options);
  for (const change of [
    { bundle: value => { value.source_revision = 'b'.repeat(40); } },
    { runtime: value => { value.id = 'new-runtime'; } },
    { baseURI: 'https://another.test/' }
  ]) {
    const next = fixture({ caches, ...change });
    assert.equal((await next.generate(next.options)).cached, false);
    assert.equal(next.workers.length, 1);
  }
  const relocated = fixture({ caches });
  relocated.resources.set('/project/runtime.json', relocated.resources.get('/runtime.json'));
  relocated.options.runtimeURL = '/project/runtime.json';
  assert.equal((await relocated.generate(relocated.options)).cached, false);
  const invalid = fixture({ caches });
  invalid.options.runtimeBytes++;
  await assert.rejects(invalid.generate(invalid.options), /resource changed/);
  const bypass = fixture({ caches });
  assert.equal((await bypass.generate({ ...bypass.options, cache: false })).cached, false);
  assert.equal(bypass.workers.length, 1);
});

test('corrupt cached PDF is discarded and generated again', async () => {
  const caches = memoryCaches();
  const f = fixture({ caches });
  await f.generate(f.options);
  const [key, response] = Array.from(caches.entries)[0];
  const changed = new Uint8Array(await response.arrayBuffer());
  changed[changed.length - 1] ^= 1;
  caches.entries.set(key, new Response(changed, { headers: response.headers }));
  const again = fixture({ caches });
  assert.equal((await again.generate(again.options)).cached, false);
  assert.equal(again.workers.length, 1);
  assert.equal(caches.entries.size, 1);
});

test('an intact cached response copied under another edition key is refused', async () => {
  const caches = memoryCaches();
  const first = fixture({ caches });
  await first.generate(first.options);
  const [[firstKey, firstResponse]] = Array.from(caches.entries);
  const second = fixture({ caches, bundle: value => { value.source_revision = 'b'.repeat(40); } });
  await second.generate(second.options);
  const secondKey = Array.from(caches.entries.keys()).find(key => key !== firstKey);
  caches.entries.set(secondKey, firstResponse.clone());
  const again = fixture({ caches, bundle: value => { value.source_revision = 'b'.repeat(40); } });
  const result = await again.generate(again.options);
  assert.equal(result.cached, false);
  assert.equal(result.source_revision, 'b'.repeat(40));
  assert.equal(again.workers.length, 1);
});

test('unavailable, denied and timed-out storage cannot fail native generation', async () => {
  for (const change of [
    { deniedCacheGetter: true },
    { caches: memoryCaches({ open: () => { throw new DOMException('Denied', 'SecurityError'); } }) },
    { caches: memoryCaches({ put: () => { throw new DOMException('Full', 'QuotaExceededError'); } }) },
    { caches: memoryCaches({ open: () => new Promise(() => {}) }) }
  ]) {
    const f = fixture(change);
    assert.equal((await f.generate(f.options)).cached, false);
    assert.equal(f.workers.length, 1);
  }
});

test('cancellation during cached lookup never returns or regenerates a PDF', async () => {
  const caches = memoryCaches();
  const first = fixture({ caches });
  await first.generate(first.options);
  const held = await caches.open();
  const controller = new AbortController();
  const cancelled = fixture({ caches: { async open() { return { ...held,
    async match(request) { controller.abort(); return held.match(request); }
  }; } } });
  await assert.rejects(cancelled.generate({ ...cancelled.options, signal: controller.signal }), error => error.name === 'AbortError');
  assert.equal(cancelled.fetches.length, 1);
  assert.equal(cancelled.workers.length, 0);
});

test('completed PDF cache remains bounded across independent concurrent page contexts', async () => {
  const caches = memoryCaches();
  const fixtures = Array.from({ length: 6 }, (_, index) => fixture({ caches,
    bundle: value => { value.source_revision = String(index).repeat(40); }
  }));
  await Promise.all(fixtures.map(f => f.generate(f.options)));
  assert.ok(caches.entries.size <= 3);
  assert.ok(caches.entries.size > 0);
});

test('a cache write completing after the storage deadline still prunes older PDFs', async () => {
  let slow = false;
  let finished;
  const completion = new Promise(resolve => { finished = resolve; });
  const caches = memoryCaches({ put: async () => {
    if (slow) { await new Promise(resolve => setTimeout(resolve, 1100)); finished(); }
  } });
  for (let index = 0; index < 3; index++) {
    const f = fixture({ caches, bundle: value => { value.source_revision = String(index).repeat(40); } });
    await f.generate(f.options);
  }
  assert.equal(caches.entries.size, 3);
  slow = true;
  const last = fixture({ caches, bundle: value => { value.source_revision = 'd'.repeat(40); } });
  assert.equal((await last.generate(last.options)).cached, false);
  await completion;
  await new Promise(resolve => setTimeout(resolve, 20));
  assert.equal(caches.entries.size, 3);
});

test('cache byte budget evicts older entries and cancellation during a write rejects the request', async () => {
  const caches = memoryCaches();
  const f = fixture({ caches });
  await f.generate(f.options);
  const [key, response] = Array.from(caches.entries)[0];
  const headers = new Headers(response.headers);
  headers.set('Content-Length', String(64 * 1024 * 1024));
  caches.entries.set(key, new Response('old cached body', { headers }));
  const next = fixture({ caches, bundle: value => { value.source_revision = 'b'.repeat(40); } });
  await next.generate(next.options);
  assert.equal(caches.entries.size, 1);
  assert.ok(!caches.entries.has(key));

  const controller = new AbortController();
  let release;
  const blocked = memoryCaches({ put: () => {
    controller.abort();
    return new Promise(resolve => { release = resolve; });
  } });
  const cancelled = fixture({ caches: blocked });
  await assert.rejects(cancelled.generate({ ...cancelled.options, signal: controller.signal }), error => error.name === 'AbortError');
  assert.ok(cancelled.workers.every(worker => worker.terminated));
  release();
});

test('bounded transferred preloads preserve separated aliases and conflicting filesystem write order', async () => {
  let expected;
  const f = fixture({ runtime: (runtime, pin) => {
    const first = pin('collision-first', 'first bytes');
    const other = pin('collision-other', 'other bytes');
    runtime.texFiles = [{ ...first, format: 3, name: 'collision' },
      ...Array.from({ length: 128 }, (_, index) => ({ ...pin('middle-' + index), format: 26, name: 'middle-' + index })),
      { ...other, format: 32, name: 'collision.tfm' }, { ...first, format: 26, name: 'collision.tfm' }];
    expected = runtime.texFiles.map(file => [file.format, file.name]);
  } });
  await f.generate(f.options);
  const batches = f.messages.filter(message => message.cmd === 'triptych-preload');
  assert.equal(batches.length, 2);
  assert.deepEqual(batches.flatMap(batch => batch.files.map(file => [file.format, file.filename])), expected);
  assert.ok(batches.every(batch => batch.files.length <= 128));
  assert.equal(batches.flatMap(batch => batch.payloads).length, 130, 'the separated alias is not transferred twice');
  assert.ok(f.transfers.every(transfer => transfer.detached));

  const stored = new Map();
  const messages = [];
  const context = vm.createContext({ self: { onmessage() {}, postMessage: value => messages.push(value) },
    texlive200: {}, FS: { writeFile: (path, data) => stored.set(path, new Uint8Array(data)) } });
  vm.runInContext(source.match(/const WORKER_BRIDGE = String\.raw`([\s\S]*?)`;/)[1], context);
  for (const batch of batches) context.self.onmessage({ data: batch });
  assert.equal(new TextDecoder().decode(stored.get('/tex/collision.tfm')), 'first bytes');
  assert.ok(messages.every(message => message.result === 'ok'));
});

test('bridge batches pdfTeX acknowledgments and restores postMessage after preload failure', () => {
  const messages = [];
  const context = { texlive200_cache: {}, self: {
    postMessage: value => messages.push(value),
    onmessage({ data }) {
      if (data.filename === 'broken') throw new Error('Cannot mount package');
      this.postMessage({ cmd: 'preloadtexlive', result: 'ok' });
      this.postMessage({ cmd: 'diagnostic', result: 'ok' });
    }
  } };
  const isolated = vm.createContext(context);
  vm.runInContext(source.match(/const WORKER_BRIDGE = String\.raw`([\s\S]*?)`;/)[1], isolated);
  const originalPost = isolated.self.postMessage;
  const send = (id, filename) => isolated.self.onmessage({ data: { cmd: 'triptych-preload', final: true, retain: false,
    payloads: [{ id, data: encode('package').buffer }], files: [{ format: 26, filename, fileId: id }] } });
  send('first', 'working');
  assert.deepEqual(messages.map(message => message.cmd), ['diagnostic', 'triptych-preload']);
  assert.equal(isolated.self.postMessage, originalPost);
  send('second', 'broken');
  assert.equal(messages.at(-1).result, 'failed');
  assert.equal(isolated.self.postMessage, originalPost);
});

test('XeTeX transfers and verifies package ownership before converter reuse, plus ICU and format handoffs', async () => {
  const f = fixture({ bundle: value => { value.engine = 'xetex'; value.format = 'xelatex'; }, runtime: unicodeRuntime });
  await f.generate(f.options);
  assert.equal(f.messages.filter(message => message.cmd === 'triptych-take-packages').length, 1);
  const preloads = f.messages.filter(message => message.cmd === 'triptych-preload');
  assert.equal(preloads.length, 2);
  assert.deepEqual(preloads.map(batch => batch.files.map(file => hash(new Uint8Array(file.data)))), [
    preloads[0].files.map(file => hash(new Uint8Array(file.data))), preloads[0].files.map(file => hash(new Uint8Array(file.data)))
  ]);
  assert.ok(f.transfers.every(transfer => transfer.detached));
  assert.deepEqual(f.transfers.find(transfer => transfer.cmd === 'triptych-configure').sizes, [encode('icu.dat').length]);
  assert.ok(f.transfers.some(transfer => transfer.cmd === 'writefile' && transfer.sizes[0] === encode('original Unicode format').length));
  assert.ok(f.workers.every(worker => worker.packageData.size === 0));
});

test('changed package bytes returned from XeTeX prevent converter startup', async () => {
  const f = fixture({ bundle: value => { value.engine = 'xetex'; value.format = 'xelatex'; }, runtime: unicodeRuntime,
    returnedPackages: payloads => { new Uint8Array(payloads[0].data)[0] ^= 1; } });
  await assert.rejects(f.generate(f.options), /changed the original font data/);
  assert.equal(f.workers.length, 1);
  assert.ok(f.workers[0].terminated);
});

test('required format decompression and compiler support are checked before large downloads', async () => {
  const noGzip = fixture({ noDecompression: true, bundle: value => { value.engine = 'xetex'; value.format = 'xelatex'; }, runtime: unicodeRuntime });
  await assert.rejects(noGzip.generate(noGzip.options), /cannot unpack/);
  assert.equal(noGzip.fetches.length, 2);
  assert.equal(noGzip.workers.length, 0);
  for (const change of [{ noWorker: true }, { noWebAssembly: true }]) {
    const f = fixture(change);
    await assert.rejects(f.generate(f.options), /cannot run the native typesetter/);
    assert.equal(f.fetches.length, 1);
  }
  const caches = memoryCaches();
  const warm = fixture({ caches });
  await warm.generate(warm.options);
  const disabled = fixture({ caches, noWorker: true, noWebAssembly: true, noDecompression: true });
  assert.equal((await disabled.generate(disabled.options)).cached, true);
  assert.equal(disabled.fetches.length, 1);
});

test('optional compressed engine transports preserve the exact WASM, ICU and format bytes', async () => {
  const unicode = fixture({ bundle: value => { value.engine = 'xetex'; value.format = 'xelatex'; }, runtime: (runtime, pin) => {
    unicodeRuntime(runtime, pin);
    addTransport(runtime.engines.xelatex.wasm, pin);
    addTransport(runtime.engines.xelatex.icu, pin);
    addTransport(runtime.engines.dvipdfmx.wasm, pin);
  } });
  await unicode.generate(unicode.options);
  assert.ok(unicode.fetches.some(url => url.endsWith('/icu.dat.transport.bin')));
  assert.ok(!unicode.fetches.some(url => /\/(icu\.dat|test\.wasm|converter\.wasm)$/.test(url)));
  const configured = unicode.messages.find(message => message.cmd === 'triptych-configure');
  assert.equal(new TextDecoder().decode(configured.icu), 'icu.dat');
  const format = unicode.messages.find(message => message.url === 'wasmtex-xetex.fmt');
  assert.equal(new TextDecoder().decode(format.src), 'original Unicode format');

  const pdftex = fixture({ runtime: (runtime, pin) => { addTransport(runtime.engines.pdflatex.format, pin); } });
  await pdftex.generate(pdftex.options);
  assert.ok(pdftex.fetches.some(url => url.endsWith('/test.fmt.transport.bin')));
  const loaded = pdftex.messages.find(message => message.cmd === 'loadformat');
  assert.equal(new TextDecoder().decode(loaded.data), 'test.fmt');
  assert.deepEqual(pdftex.transfers.find(transfer => transfer.cmd === 'loadformat').sizes, [encode('test.fmt').length]);
});

test('optional transport can use original bytes without decompression but never after transport corruption', async () => {
  const fallback = fixture({ noDecompression: true, runtime: (runtime, pin) => addTransport(runtime.engines.pdflatex.wasm, pin) });
  await fallback.generate(fallback.options);
  assert.ok(fallback.fetches.some(url => url.endsWith('/test.wasm')));
  assert.ok(!fallback.fetches.some(url => url.endsWith('.transport.bin')));
  for (const mode of ['compressed', 'expanded', 'hash']) {
    const f = fixture({ runtime: (runtime, pin) => addTransport(runtime.engines.pdflatex.wasm, pin,
      mode === 'expanded' ? 'too many expanded bytes' : mode === 'hash' ? 'bad.bytes' : 'test.wasm') });
    if (mode === 'compressed') f.resources.set('/test.wasm.transport.bin', encode('changed transport'));
    await assert.rejects(f.generate(f.options), /changed|failed verification|exceeds/);
    assert.ok(!f.fetches.some(url => url.endsWith('/test.wasm')));
    assert.equal(f.workers.length, 0);
  }
});

test('foreign or malformed optional transports fail preflight without downloading packages', async () => {
  for (const mutate of [pin => { pin.transport.url = 'https://elsewhere.test/engine.bin'; },
    pin => { pin.transport.compression = 'unknown'; }, pin => { pin.transport.bytes = -1; }]) {
    const f = fixture({ runtime: (runtime, pin) => {
      packages(runtime, pin);
      addTransport(runtime.engines.pdflatex.wasm, pin);
      mutate(runtime.engines.pdflatex.wasm);
    } });
    await assert.rejects(f.generate(f.options), /served by this website|Invalid compressed/);
    assert.equal(f.fetches.length, 2);
  }
});

test('download progress reports bounded byte totals, throttles chunks and preserves final readiness', async () => {
  const progress = [];
  const f = fixture({ runtime: packages, fetch: (url, options, respond) => {
    const response = respond();
    if (!url.endsWith('/packages.bin')) return response;
    return new Response(new ReadableStream({ async start(controller) {
      for (const byte of new Uint8Array(await response.arrayBuffer())) controller.enqueue(Uint8Array.of(byte));
      controller.close();
    } }));
  } });
  await f.generate({ ...f.options, onProgress: value => progress.push(value) });
  const packagesProgress = progress.filter(value => value.stage === 'Downloading original fonts and packages');
  assert.equal(packagesProgress.length, 2, 'rapid byte chunks emit only initial and completed progress');
  assert.equal(packagesProgress[0].loadedBytes, 0);
  assert.equal(packagesProgress.at(-1).loadedBytes, packagesProgress.at(-1).totalBytes);
  assert.ok(progress.slice(0, -1).every(value => value.message.includes('Keep this page visible')));
  assert.equal(progress.at(-1).stage, 'ready');
  assert.equal(progress.at(-1).message, 'The typeset PDF is ready.');
});

test('ready resource chunks yield to page tasks and cancellation before the body is complete', async () => {
  for (const cancel of [false, true]) {
    let clock = 0;
    let yielded = false;
    let pulled = 0;
    const controller = new AbortController();
    const f = fixture({ clock: () => clock, runtime: (runtime, pin) => {
      runtime.engines.pdflatex.wasm = pin('large.wasm', new Uint8Array(64));
    }, fetch: (url, options, respond) => {
      if (!url.endsWith('/large.wasm')) return respond();
      return new Response(new ReadableStream({ pull(stream) {
        clock += 9;
        if (pulled++ === 0) setTimeout(() => { yielded = true; if (cancel) controller.abort(); }, 0);
        if (pulled > 64) { stream.close(); return; }
        stream.enqueue(Uint8Array.of(0));
      } }));
    }, workerCreated: () => assert.ok(yielded, 'page task ran before typesetter startup') });
    const generation = f.generate({ ...f.options, signal: controller.signal });
    if (cancel) {
      await assert.rejects(generation, error => error.name === 'AbortError');
      assert.ok(pulled < 64, 'cancellation interrupts the ready body drain');
      assert.equal(f.workers.length, 0);
    } else await generation;
    assert.ok(yielded);
  }
});

test('compressed engine input is bounded and yields between ready decompression chunks', async () => {
  let clock = 0;
  let yielded = false;
  const chunks = [];
  class ReadyDecompressor {
    constructor() {
      // Identity decoding isolates stream scheduling from the native decoder's
      // own scheduling. Real gzip and both hash commitments are tested above.
      return new TransformStream({ transform(chunk, controller) {
        if (!chunks.length) setTimeout(() => { yielded = true; }, 0);
        chunks.push(chunk.byteLength);
        clock += 9;
        controller.enqueue(chunk);
      } });
    }
  }
  const f = fixture({ clock: () => clock, DecompressionStream: ReadyDecompressor,
    runtime: (runtime, pin) => {
      const bytes = new Uint8Array(512 * 1024 + 1);
      runtime.engines.pdflatex.wasm = { ...pin('large.wasm', bytes),
        transport: { ...pin('large.transport.bin', bytes), compression: 'gzip' } };
    }, workerCreated: () => assert.ok(yielded, 'page task ran before typesetter startup') });
  await f.generate(f.options);
  assert.deepEqual(chunks, [128 * 1024, 128 * 1024, 128 * 1024, 128 * 1024, 1]);
  assert.ok(!f.fetches.some(url => url.endsWith('/large.wasm')));
});

test('returned package verification yields to page tasks and aborts before converter startup', async () => {
  for (const cancel of [false, true]) {
    let clock = 0;
    let returning = false;
    let yielded = false;
    const controller = new AbortController();
    const f = fixture({ clock: () => clock, bundle: bundle => { bundle.engine = 'xetex'; bundle.format = 'xelatex'; },
      runtime: unicodeRuntime,
      crypto: { subtle: { digest(algorithm, bytes) {
        if (returning) clock += 9;
        return Promise.resolve(Uint8Array.from(createHash('sha256').update(bytes).digest()).buffer);
      } } },
      returnedPackages: () => {
        returning = true;
        setTimeout(() => { yielded = true; if (cancel) controller.abort(); }, 0);
      },
      workerCreated: workers => { if (workers.length) assert.ok(yielded, 'page task ran before converter startup'); }
    });
    const generation = f.generate({ ...f.options, signal: controller.signal });
    if (cancel) {
      await assert.rejects(generation, error => error.name === 'AbortError');
      assert.equal(f.workers.length, 1);
      assert.ok(f.workers[0].terminated);
    } else await generation;
    assert.ok(yielded);
  }
});
