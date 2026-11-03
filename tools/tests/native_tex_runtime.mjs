import assert from 'node:assert/strict';
import { readFile } from 'node:fs/promises';
import { createHash, webcrypto } from 'node:crypto';
import vm from 'node:vm';
import test from 'node:test';

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
  class FakeWorker {
    constructor() { this.passes = 0; this.terminated = false; workers.push(this); queueMicrotask(() => this.onmessage({ data: { result: 'ok' } })); }
    postMessage(payload) {
      if (change.postError && payload.cmd === 'writefile') throw new DOMException('Cannot clone the source payload', 'DataCloneError');
      messages.push(payload);
      if (payload.cmd === 'setmainfile') return;
      if (change.hang && payload.cmd === 'compilelatex') return;
      let data = { cmd: payload.cmd, result: 'ok' };
      if (payload.cmd === 'compilelatex') {
        this.passes++;
        data = { cmd: 'compile', result: 'ok', status: 0, log: change.log || 'Output written on main.pdf (1 page).', pdf: encode('%PDF-1.4\nNative test result').buffer };
      }
      if (payload.cmd === 'triptych-state') data.files = [{ path: 'main.aux', bytes: encode(change.unsettled ? String(this.passes) : 'settled').buffer }];
      queueMicrotask(() => { if (!this.terminated) this.onmessage({ data }); });
    }
    terminate() { this.terminated = true; }
  }
  const fetches = [];
  const context = vm.createContext({
    window: {}, document: { baseURI: 'https://example.test/' }, URL, Blob, Response, DecompressionStream,
    TextEncoder, TextDecoder, Uint8Array, ArrayBuffer, DOMException, AbortController,
    crypto: webcrypto, atob, setTimeout, clearTimeout, Worker: FakeWorker,
    fetch: async (url, options) => {
      fetches.push(String(url));
      if (options.signal.aborted) throw new DOMException('Cancelled', 'AbortError');
      const bytes = resources.get(new URL(url).pathname);
      return new Response(bytes || 'Not found', { status: bytes ? 200 : 404, headers: { 'content-length': String(bytes?.length || 9) } });
    }
  });
  vm.runInContext(source, context);
  const options = { bundleURL: bundlePin.url, bundleSHA256: bundlePin.sha256, bundleBytes: bundlePin.bytes,
    runtimeURL: runtimePin.url, runtimeSHA256: runtimePin.sha256, runtimeBytes: runtimePin.bytes };
  return { generate: context.window.TriptychNativeTeX.generate, options, resources, workers, messages, fetches };
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
