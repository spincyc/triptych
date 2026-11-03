import assert from 'node:assert/strict';
import { readFile } from 'node:fs/promises';
import { createHash, webcrypto } from 'node:crypto';
import vm from 'node:vm';
import test from 'node:test';
import { gzipSync } from 'node:zlib';

const source = await readFile(new URL('../../src/web/browser/shared/native-tex.js', import.meta.url), 'utf8');
const hash = value => createHash('sha256').update(value).digest('hex');
const encode = value => new TextEncoder().encode(value);
const canonical = value => JSON.stringify(value, (_, item) => item && !Array.isArray(item) && typeof item === 'object'
  ? Object.fromEntries(Object.entries(item).sort(([a], [b]) => a < b ? -1 : a > b ? 1 : 0)) : item);
function sign(bundle) {
  const rendered = Object.fromEntries(['document', 'output_id', 'edition', 'engine', 'format', 'entrypoint', 'cwd',
    'environment', 'options'].map(key => [key, bundle[key]]));
  rendered.files = bundle.files.map(({ path, bytes, sha256 }) => ({ path, bytes, sha256 })).sort((a, b) => a.path < b.path ? -1 : 1);
  bundle.render_sha256 = hash(canonical(rendered));
  delete bundle.content_sha256;
  bundle.content_sha256 = hash(canonical(bundle));
  return bundle;
}

function fixture() {
  const resources = {};
  const text = ['\\documentclass{article}\r\n' + '% shared style\r\n'.repeat(100), 'Exact æ, œ, †.\r\n'.repeat(100)];
  const paths = ['src/common/preamble.tex', 'src/gpt/body.tex'];
  const files = text.map((content, i) => {
    const bytes = encode(content), sha256 = hash(bytes);
    resources['native-tex/assets/' + sha256 + '.bin'] = bytes;
    return { path: paths[i], encoding: 'url', href: '../assets/' + sha256 + '.bin', bytes: bytes.length, sha256 };
  });
  const inline = '\\input{common/preamble}\r\n\\input{body}\r\n';
  files.push({ path: 'src/gpt/main.tex', encoding: 'utf8', content: inline, bytes: encode(inline).length, sha256: hash(inline) });
  // Two mounted paths may share bytes but must receive independent buffers.
  files.push({ ...files[1], path: 'src/gpt/z-alias.tex' });
  const expanded = Buffer.concat(text.map(value => Buffer.from(value)));
  const packed = gzipSync(expanded, { mtime: 0 });
  const sha256 = hash(packed);
  resources['native-tex/source-packs/' + sha256 + '.bin'] = packed;
  const bundle = sign({ schema: 'triptych-native-print-source-bundle/v1', document: 'publication:gpt/example',
    output_id: 'publication:gpt/example', edition: 'main', source_revision: 'a'.repeat(40), engine: 'pdftex', format: 'pdflatex',
    cwd: 'src/gpt', entrypoint: 'src/gpt/main.tex', environment: { TEXINPUTS: '..:' },
    options: { shell_escape: false, minimum_passes: 2, max_passes: 8, settle_auxiliary_files: true }, files,
    sourcePacks: [{ href: '../source-packs/' + sha256 + '.bin', sha256, bytes: packed.length, compression: 'gzip',
      expanded_bytes: expanded.length, files: files.slice(0, 2).map((file, i) => ({ sha256: file.sha256,
        bytes: file.bytes, offset: i ? files[0].bytes : 0 })) }] });
  return { bundle, resources };
}

function controller(resources, options = {}) {
  const fetches = [];
  const context = vm.createContext({ window: {}, document: { baseURI: 'https://example.test/project/' },
    URL, Blob, Response, ReadableStream, TextEncoder, TextDecoder, Uint8Array, ArrayBuffer,
    DOMException, AbortController, crypto: webcrypto, atob, setTimeout, clearTimeout,
    DecompressionStream: options.raw ? undefined : DecompressionStream,
    fetch: async (url, request) => {
      fetches.push(String(url));
      const body = resources[new URL(url).pathname.replace('/project/', '')];
      if (options.fetch) await options.fetch(request);
      return new Response(body || 'missing', { status: body ? 200 : 404,
        headers: { 'content-length': String(body?.length || 7) } });
    } });
  vm.runInContext(source.replace('  async function pool(', '  global.sourceTransport = { sourceFiles, sourceRenderIdentity };\n  async function pool('), context);
  return { ...context.window.sourceTransport, fetches };
}
const base = 'https://example.test/project/native-tex/sources/source.json';
const run = (api, bundle) => api.sourceFiles(bundle, base, new AbortController().signal);

if (process.argv.includes('--fixture')) {
  const { bundle, assets } = JSON.parse(await readFile(process.argv[process.argv.indexOf('--fixture') + 1], 'utf8'));
  const resources = Object.fromEntries(Object.entries(assets).map(([key, value]) => [key, Uint8Array.from(value)]));
  for (const raw of [false, true]) {
    const api = controller(resources, { raw });
    assert.equal(await api.sourceRenderIdentity(bundle, base), bundle.render_sha256);
    const project = await run(api, bundle);
    assert.equal(project.files.length, bundle.files.length);
    for (const file of project.files) {
      const declared = bundle.files.find(row => row.path === file.path);
      assert.equal(hash(file.bytes), declared.sha256);
      assert.equal(file.bytes.length, declared.bytes);
    }
  }
} else {
  test('compressed and raw source transports preserve all virtual bytes and independent transfer buffers', async () => {
    const { bundle, resources } = fixture();
    for (const raw of [false, true]) {
      const api = controller(resources, { raw }), result = await run(api, bundle);
      assert.equal(result.renderSHA256, bundle.render_sha256);
      for (const file of result.files) assert.equal(hash(file.bytes), bundle.files.find(row => row.path === file.path).sha256);
      assert.equal(new Set(result.files.map(file => file.bytes.buffer)).size, result.files.length);
      assert.equal(api.fetches.length, raw ? 2 : 1);
      const buffers = result.files.map(file => file.bytes.buffer);
      const clone = structuredClone(result.files, { transfer: buffers });
      assert.ok(buffers.every(buffer => !buffer.byteLength));
      assert.ok(clone.every(file => file.bytes.byteLength));
    }
  });
  test('revision-only provenance keeps identity; changed style bytes cannot claim old identity', async () => {
    const { bundle, resources } = fixture(), api = controller(resources);
    const identity = bundle.render_sha256;
    bundle.source_revision = 'b'.repeat(40); sign(bundle);
    assert.equal(await api.sourceRenderIdentity(bundle, base), identity);
    bundle.files[0].sha256 = 'c'.repeat(64);
    delete bundle.content_sha256;
    await assert.rejects(api.sourceRenderIdentity(bundle, base));
    assert.equal(api.fetches.length, 0);
  });
  test('invalid pack inventory or external origin fails before fetch even with raw fallback', async () => {
    const mutations = [p => p.files[0].offset++, p => p.files[0].bytes++, p => p.files.push({ ...p.files[0] }),
      p => p.files[0].sha256 = 'f'.repeat(64), p => p.expanded_bytes++, p => p.expanded_bytes = 8 * 1024 * 1024 + 1,
      p => p.href = '../source-packs/unknown.bin', p => p.extra = true];
    for (const raw of [false, true]) {
      for (const mutate of mutations) {
        const { bundle, resources } = fixture(), api = controller(resources, { raw });
        mutate(bundle.sourcePacks[0]); delete bundle.content_sha256;
        await assert.rejects(run(api, bundle)); assert.equal(api.fetches.length, 0);
      }
      const { bundle, resources } = fixture(), api = controller(resources, { raw });
      bundle.files[0].href = 'https://elsewhere.test/private.bin'; delete bundle.content_sha256;
      await assert.rejects(api.sourceRenderIdentity(bundle, base), /this website/); assert.equal(api.fetches.length, 0);
    }
  });
  test('compressed and raw byte substitution, missing data and wrong expansion fail closed', async () => {
    for (const mode of ['compressed', 'raw', 'missing', 'expansion', 'member']) {
      const { bundle, resources } = fixture(), pack = bundle.sourcePacks[0];
      const route = 'native-tex/' + pack.href.slice(3);
      if (mode === 'compressed') resources[route] = Uint8Array.from(resources[route], byte => byte ^ 1);
      if (mode === 'raw') resources['native-tex/' + bundle.files[0].href.slice(3)] = encode('wrong bytes');
      if (mode === 'missing') delete resources[route];
      if (mode === 'expansion' || mode === 'member') {
        const body = gzipSync(Buffer.alloc(pack.expanded_bytes + (mode === 'expansion' ? 1 : 0), 65));
        pack.sha256 = hash(body); pack.href = '../source-packs/' + pack.sha256 + '.bin'; pack.bytes = body.length;
        resources['native-tex/' + pack.href.slice(3)] = body; sign(bundle);
      }
      await assert.rejects(run(controller(resources, { raw: mode === 'raw' }), bundle));
    }
  });
  test('legacy inline v1 sources remain accepted', async () => {
    const { bundle, resources } = fixture();
    for (const file of bundle.files) if (file.encoding === 'url') {
      file.content = new TextDecoder().decode(resources['native-tex/' + file.href.slice(3)]);
      file.encoding = 'utf8'; delete file.href;
    }
    delete bundle.sourcePacks; delete bundle.render_sha256; delete bundle.content_sha256;
    const api = controller({});
    assert.equal(await api.sourceRenderIdentity(bundle, base), null);
    assert.equal((await run(api, bundle)).files.length, 4);
    assert.equal(api.fetches.length, 0);
  });
  test('raw source requests have bounded concurrency and abort propagation', async () => {
    const { bundle, resources } = fixture();
    delete bundle.sourcePacks;
    for (let i = 0; i < 9; i++) {
      const bytes = encode('Unique source ' + i), sha256 = hash(bytes), href = '../assets/' + sha256 + '.bin';
      resources['native-tex/' + href.slice(3)] = bytes;
      bundle.files.push({ path: 'src/gpt/extra' + i + '.tex', encoding: 'url', href, sha256, bytes: bytes.length });
    }
    sign(bundle);
    let active = 0, maximum = 0;
    const api = controller(resources, { fetch: async () => {
      active++; maximum = Math.max(maximum, active); await new Promise(resolve => setTimeout(resolve, 5)); active--;
    } });
    await run(api, bundle); assert.equal(maximum, 4);
    const abort = new AbortController();
    const waiting = controller(resources, { fetch: request => new Promise((resolve, reject) => {
      request.signal.addEventListener('abort', () => reject(new DOMException('Cancelled', 'AbortError')), { once: true });
      abort.abort();
      if (request.signal.aborted) reject(new DOMException('Cancelled', 'AbortError'));
    }) });
    await assert.rejects(waiting.sourceFiles(bundle, base, abort.signal), { name: 'AbortError' });
  });
}
