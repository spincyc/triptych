/* Generate a native TeX PDF from source and runtime bytes admitted by the publisher. */
(function (global) {
  'use strict';

  const BUNDLE_SCHEMA = 'triptych-native-print-source-bundle/v1';
  const RUNTIME_SCHEMA = 'triptych-native-tex-runtime/v1';
  const MAX_RESOURCE = 256 * 1024 * 1024;
  const MAX_PROJECT = 256 * 1024 * 1024;
  const PACK_BYTES = 8 * 1024 * 1024;
  const HASH = /^[a-f0-9]{64}$/;
  const encoder = new TextEncoder();
  // Bump the implementation key when bridge,
  // convergence or output checks change without changing the admitted pins.
  const COMPILER_VERSION = 'triptych-native-tex-v4';
  const PDF_CACHE = 'triptych-native-pdf-v1';
  const CACHE_BYTES = 64 * 1024 * 1024;
  const CACHE_ENTRIES = 3;
  let cacheWrites = Promise.resolve();
  let cacheUnavailable = false;

  function stop(signal) {
    if (signal && signal.aborted) throw new DOMException('PDF generation cancelled.', 'AbortError');
  }

  function sameOrigin(value, base) {
    const url = new URL(value, base);
    const origin = new URL(document.baseURI).origin;
    if (url.origin !== origin || !/^https?:$/.test(url.protocol) || url.username || url.password || url.hash) {
      throw new Error('The print source and runtime must be served by this website.');
    }
    return url.href;
  }

  function relativePath(value) {
    if (typeof value !== 'string' || !value || value.length > 4096 ||
        value.startsWith('/') || /[\\\x00-\x1f\x7f]/.test(value) ||
        value.split('/').some(part => !part || part === '.' || part === '..')) {
      throw new Error('Invalid native print source path.');
    }
    return value;
  }

  async function sha256(bytes) {
    const hash = await crypto.subtle.digest('SHA-256', bytes);
    return Array.from(new Uint8Array(hash), n => n.toString(16).padStart(2, '0')).join('');
  }

  function resourcePin(value) {
    return value && HASH.test(value.sha256 || '') && Number.isSafeInteger(value.bytes) &&
      value.bytes > 0 && value.bytes <= MAX_RESOURCE;
  }

  function taskBudget(signal) {
    let resumed = Date.now();
    return async () => {
      stop(signal);
      if (Date.now() - resumed < 8) return;
      // Ready stream reads and digest promises can otherwise keep the page in
      // one microtask chain. A task boundary lets input and painting proceed.
      await new Promise(resolve => {
        const resume = () => {
          clearTimeout(timer);
          signal.removeEventListener('abort', resume);
          resolve();
        };
        const timer = setTimeout(resume, 0);
        signal.addEventListener('abort', resume, { once: true });
        if (signal.aborted) resume();
      });
      stop(signal);
      resumed = Date.now();
    };
  }

  function gzipStream(bytes, signal) {
    const cooperate = taskBudget(signal);
    let offset = 0;
    return new ReadableStream({
      async pull(controller) {
        await cooperate();
        if (offset === bytes.byteLength) { controller.close(); return; }
        // Blob streams can feed a large compressed resource in one transform.
        // Bound each input so the decompressor also gets task boundaries.
        const end = Math.min(offset + 128 * 1024, bytes.byteLength);
        controller.enqueue(bytes.subarray(offset, end));
        offset = end;
      }
    }).pipeThrough(new DecompressionStream('gzip'));
  }

  async function readExact(stream, size, signal, onBytes) {
    const reader = stream.getReader();
    const bytes = new Uint8Array(size);
    const cooperate = taskBudget(signal);
    let offset = 0;
    const abort = () => { reader.cancel().catch(() => {}); };
    signal.addEventListener('abort', abort, { once: true });
    try {
      stop(signal);
      while (true) {
        const { value, done } = await reader.read();
        stop(signal);
        if (done) break;
        if (offset + value.byteLength > size) throw new Error('A native print resource changed or exceeds its declared size.');
        bytes.set(value, offset);
        offset += value.byteLength;
        if (onBytes) onBytes(value.byteLength);
        await cooperate();
      }
      if (offset !== size) throw new Error('A native print resource changed: its body is incomplete.');
      return bytes;
    } finally {
      signal.removeEventListener('abort', abort);
      reader.cancel().catch(() => {});
    }
  }

  /* Storage is optional. A blocked browser storage backend must not hold a
     completed edition indefinitely; queued writes stop after such a timeout. */
  async function cacheAccess(action, signal) {
    if (cacheUnavailable || signal.aborted) return null;
    const controller = new AbortController();
    let timer;
    let finish;
    const expiry = new Promise(resolve => { finish = () => resolve(null); });
    const abort = () => { controller.abort(); finish(); };
    signal.addEventListener('abort', abort, { once: true });
    timer = setTimeout(() => { cacheUnavailable = true; abort(); }, 1000);
    const task = Promise.resolve().then(async () => {
      if (!global.caches) return null;
      const cache = await global.caches.open(PDF_CACHE);
      stop(controller.signal);
      return action(cache, controller.signal);
    }).catch(() => null);
    try { return await Promise.race([task, expiry]); }
    finally {
      clearTimeout(timer);
      signal.removeEventListener('abort', abort);
      controller.abort();
    }
  }

  async function cacheKey(options, bundleURL, runtimeURL, renderSHA256 = null) {
    const pins = [
      { url: bundleURL, sha256: options.bundleSHA256, bytes: options.bundleBytes },
      { url: runtimeURL, sha256: options.runtimeSHA256, bytes: options.runtimeBytes }
    ];
    if (!pins.every(resourcePin)) throw new Error('The native print download has no valid size and SHA-256 commitment.');
    const identity = renderSHA256 ? { renderSHA256, runtime: pins[1] } : { pins };
    const key = await sha256(encoder.encode(JSON.stringify({ implementation: COMPILER_VERSION, ...identity })));
    return new URL('pdf-cache/' + key + '.pdf', runtimeURL).href;
  }

  async function cachedPDF(key, signal) {
    return cacheAccess(async (cache, localSignal) => {
      const response = await cache.match(key);
      stop(localSignal);
      if (!response) return null;
      try {
        if (response.headers.get('X-Triptych-PDF-Key') !== key) throw new Error('Cached PDF belongs to another edition.');
        const size = Number(response.headers.get('Content-Length'));
        const sha = response.headers.get('X-Triptych-PDF-SHA256');
        if (!Number.isSafeInteger(size) || size < 5 || size > CACHE_BYTES || !HASH.test(sha || '')) throw new Error('Invalid cached PDF.');
        const bytes = await readExact(response.body, size, localSignal);
        if (new TextDecoder().decode(bytes.subarray(0, 5)) !== '%PDF-' || await sha256(bytes) !== sha) throw new Error('Changed cached PDF.');
        const metadata = JSON.parse(decodeURIComponent(response.headers.get('X-Triptych-PDF-Metadata') || ''));
        if (!metadata || !['document', 'output_id', 'source_revision', 'runtime'].every(name => typeof metadata[name] === 'string') ||
            !Number.isSafeInteger(metadata.passes) || metadata.passes < 2 || metadata.passes > 8) throw new Error('Invalid cached PDF metadata.');
        stop(localSignal);
        return { ...metadata, bytes, byteLength: size, sha256: sha, cached: true, log: 'Reused a verified PDF from this browser.' };
      } catch (error) {
        stop(localSignal);
        await cache.delete(key);
        return null;
      }
    }, signal);
  }

  async function prunePDFs(cache) {
    // Cache.put cannot be aborted. If it completes after display cancellation
    // or a storage timeout, its successful insertion still needs housekeeping.
    const controller = new AbortController();
    const localSignal = controller.signal;
    const timer = setTimeout(() => controller.abort(), 1000);
    try {
      // Prune after insertion so the final concurrent tab's completed write
      // also sees and bounds earlier writes. Page-local writes are serialized.
      const keys = await cache.keys();
      stop(localSignal);
      const held = [];
      let total = 0;
      for (const request of keys) {
        const response = await cache.match(request);
        stop(localSignal);
        const size = Number(response && response.headers.get('Content-Length'));
        if (!Number.isSafeInteger(size) || size < 5 || size > CACHE_BYTES) {
          await cache.delete(request);
        } else { held.push({ request, size }); total += size; }
        stop(localSignal);
      }
      while (held.length > CACHE_ENTRIES || total > CACHE_BYTES) {
        const oldest = held.shift();
        await cache.delete(oldest.request);
        total -= oldest.size;
        stop(localSignal);
      }
    } finally { clearTimeout(timer); }
  }

  async function rememberPDF(key, result, signal) {
    if (result.byteLength > CACHE_BYTES) return;
    const write = cacheWrites.then(() => cacheAccess(async (cache, localSignal) => {
      const metadata = Object.fromEntries(['document', 'output_id', 'source_revision', 'runtime', 'passes'].map(name => [name, result[name]]));
      stop(localSignal);
      await cache.put(key, new Response(result.bytes, { headers: {
        'Content-Type': 'application/pdf', 'Content-Length': String(result.byteLength),
        'X-Triptych-PDF-Key': key,
        'X-Triptych-PDF-SHA256': result.sha256,
        'X-Triptych-PDF-Metadata': encodeURIComponent(JSON.stringify(metadata))
      } }));
      await prunePDFs(cache);
    }, signal));
    cacheWrites = write.catch(() => {});
    await write;
  }

  async function verified(url, sha, size, signal, limit = MAX_RESOURCE, cacheMode = 'default', onBytes) {
    if (!HASH.test(sha || '') || !Number.isSafeInteger(size) || size < 1 || size > limit) {
      throw new Error('The native print download has no valid size and SHA-256 commitment.');
    }
    stop(signal);
    const response = await fetch(url, { signal, credentials: 'omit', redirect: 'error', cache: cacheMode });
    if (!response.ok) throw new Error('A required native print resource could not be loaded (' + response.status + ').');
    const length = response.headers.get('content-length');
    if (length && Number(length) > limit) throw new Error('A native print resource exceeds its permitted size.');
    const bytes = await readExact(response.body, size, signal, onBytes);
    stop(signal);
    if (bytes.byteLength !== size || await sha256(bytes) !== sha) {
      throw new Error('A native print resource changed. Reload the edition before printing.');
    }
    return bytes;
  }

  function downloadProgress(progress, stage, totalBytes) {
    let loadedBytes = 0;
    let last = -Infinity;
    const publish = () => {
      const now = Date.now();
      if (loadedBytes !== totalBytes && now - last < 500) return;
      last = now;
      const amount = value => (value / (1024 * 1024)).toFixed(1);
      progress(stage + ' (' + amount(loadedBytes) + ' of ' + amount(totalBytes) + ' MiB)…',
        { stage, loadedBytes, totalBytes });
    };
    publish();
    return amount => { loadedBytes += amount; publish(); };
  }

  function transportPin(pin, base) {
    if (!resourcePin(pin)) throw new Error('Invalid native engine resource.');
    sameOrigin(pin.url, base);
    if (pin.transport !== undefined) {
      if (!resourcePin(pin.transport) || pin.transport.compression !== 'gzip') throw new Error('Invalid compressed native engine resource.');
      sameOrigin(pin.transport.url, base);
    }
    return pin.transport && typeof DecompressionStream === 'function' ? pin.transport : pin;
  }

  async function engineResource(pin, base, signal, onBytes) {
    const delivered = transportPin(pin, base);
    const bytes = await verified(sameOrigin(delivered.url, base), delivered.sha256, delivered.bytes, signal,
      MAX_RESOURCE, 'default', onBytes);
    if (delivered === pin) return bytes;
    const stream = gzipStream(bytes, signal);
    const expanded = await readExact(stream, pin.bytes, signal);
    if (await sha256(expanded) !== pin.sha256) throw new Error('A decompressed native engine resource failed verification.');
    stop(signal);
    return expanded;
  }

  function json(bytes, name) {
    try { return JSON.parse(new TextDecoder('utf-8', { fatal: true }).decode(bytes)); }
    catch (_) { throw new Error('The ' + name + ' is not valid UTF-8 JSON.'); }
  }

  function canonical(value) {
    if (Array.isArray(value)) return '[' + value.map(canonical).join(',') + ']';
    if (value && typeof value === 'object') {
      return '{' + Object.keys(value).sort().map(key => JSON.stringify(key) + ':' + canonical(value[key])).join(',') + '}';
    }
    return JSON.stringify(value);
  }

  async function sourceRenderIdentity(bundle, bundleURL) {
    if (!bundle || bundle.schema !== BUNDLE_SCHEMA || !/^[a-f0-9]{40}$/.test(bundle.source_revision || '') ||
        !['pdftex', 'xetex'].includes(bundle.engine) || !Array.isArray(bundle.files) ||
        !bundle.files.length || bundle.files.length > 20000 ||
        !['document', 'output_id', 'edition'].every(key => typeof bundle[key] === 'string' && bundle[key]) ||
        bundle.format !== (bundle.engine === 'xetex' ? 'xelatex' : 'pdflatex')) {
      throw new Error('Unsupported or incomplete native print source bundle.');
    }
    const cwd = relativePath(bundle.cwd);
    const entrypoint = relativePath(bundle.entrypoint);
    if (!entrypoint.startsWith(cwd + '/')) throw new Error('The native print entrypoint is outside its working directory.');
    if (!bundle.options || bundle.options.shell_escape !== false ||
        bundle.options.max_passes !== 8 || bundle.options.minimum_passes !== 2 ||
        bundle.options.settle_auxiliary_files !== true) {
      throw new Error('Unsupported native print compilation policy.');
    }
    const texinputs = bundle.environment && bundle.environment.TEXINPUTS !== undefined ? bundle.environment.TEXINPUTS : '';
    if (typeof texinputs !== 'string' || texinputs.length > 4096 ||
        /[\x00-\x1f\x7f;\\$!{}]/.test(texinputs) || texinputs.split(':').some(part =>
          part && part !== '.' && part !== '..' && !/^[A-Za-z0-9_./-]+$/.test(part))) {
      throw new Error('Unsupported native TeX input search path.');
    }
    if (bundle.content_sha256) {
      const unsigned = Object.assign({}, bundle);
      delete unsigned.content_sha256;
      if (!HASH.test(bundle.content_sha256) || await sha256(encoder.encode(canonical(unsigned))) !== bundle.content_sha256) {
        throw new Error('The native source bundle identity does not match its contents.');
      }
    }
    const paths = new Set();
    const external = new Map();
    let total = 0;
    for (const file of bundle.files) {
      const path = relativePath(file.path);
      if (paths.has(path.toLowerCase()) || !Number.isSafeInteger(file.bytes) || file.bytes < 0 ||
          file.bytes > MAX_RESOURCE || !HASH.test(file.sha256 || '') ||
          (file.encoding !== 'url' && typeof file.content !== 'string')) throw new Error('Duplicate or incomplete native source file.');
      paths.add(path.toLowerCase());
      total += file.bytes;
      if (total > MAX_PROJECT) throw new Error('The canonical native source project exceeds its size limit.');
      let bytes;
      if (file.encoding === 'url') {
        if (!resourcePin(file) || typeof file.href !== 'string' || !file.href) throw new Error('Invalid native source URL.');
        sameOrigin(file.href, bundleURL);
        if (/\.(?:tex|sty|cls|bib|bst)$/i.test(path)) external.set(file.sha256, file.bytes);
        continue;
      } else if (file.encoding === 'utf8') bytes = encoder.encode(file.content);
      else if (file.encoding === 'base64' && /^[A-Za-z0-9+/]*={0,2}$/.test(file.content)) {
        let decoded;
        try { decoded = atob(file.content); } catch (_) { throw new Error('Invalid native source binary encoding.'); }
        bytes = Uint8Array.from(decoded, c => c.charCodeAt(0));
      } else throw new Error('Unsupported native source encoding.');
      if (bytes.byteLength !== file.bytes ||
          await sha256(bytes) !== file.sha256) throw new Error('A canonical TeX source or illustration failed verification.');
    }
    if (!bundle.files.some(file => file.path === entrypoint)) throw new Error('The native print entrypoint is missing.');
    if (bundle.sourcePacks !== undefined) {
      if (!Array.isArray(bundle.sourcePacks) || bundle.sourcePacks.length > external.size) throw new Error('Invalid native source packs.');
      const packed = new Set();
      for (const pack of bundle.sourcePacks) {
        if (!pack || Object.keys(pack).sort().join(',') !== 'bytes,compression,expanded_bytes,files,href,sha256' ||
            !resourcePin(pack) || pack.href !== '../source-packs/' + pack.sha256 + '.bin' || pack.compression !== 'gzip' ||
            !Number.isSafeInteger(pack.expanded_bytes) || pack.expanded_bytes < 1 || pack.expanded_bytes > PACK_BYTES ||
            !Array.isArray(pack.files) || !pack.files.length || pack.files.length > 32) throw new Error('Invalid native source pack.');
        sameOrigin(pack.href, bundleURL);
        let offset = 0;
        for (const member of pack.files) {
          if (!member || Object.keys(member).sort().join(',') !== 'bytes,offset,sha256' || !resourcePin(member) ||
              external.get(member.sha256) !== member.bytes || packed.has(member.sha256) || member.offset !== offset ||
              offset + member.bytes > pack.expanded_bytes) throw new Error('Invalid native source pack inventory.');
          packed.add(member.sha256);
          offset += member.bytes;
        }
        if (offset !== pack.expanded_bytes) throw new Error('Incomplete native source pack inventory.');
      }
    }
    if (bundle.render_sha256 === undefined) return null;
    const rendered = Object.fromEntries(['document', 'output_id', 'edition', 'engine', 'format', 'entrypoint', 'cwd',
      'environment', 'options'].map(key => [key, bundle[key]]));
    rendered.files = bundle.files.map(file => ({ path: file.path, bytes: file.bytes, sha256: file.sha256 }))
      .sort((left, right) => left.path < right.path ? -1 : left.path > right.path ? 1 : 0);
    if (!HASH.test(bundle.render_sha256) || await sha256(encoder.encode(canonical(rendered))) !== bundle.render_sha256) {
      throw new Error('The native source render identity does not match its exact inputs.');
    }
    return bundle.render_sha256;
  }

  async function sourceFiles(bundle, bundleURL, signal) {
    const renderSHA256 = await sourceRenderIdentity(bundle, bundleURL);
    stop(signal);
    const payloads = new Map();
    const external = new Map();
    for (const file of bundle.files) {
      if (file.encoding === 'url') {
        sameOrigin(file.href, bundleURL);
        external.set(file.sha256, file);
      }
    }
    const packs = typeof DecompressionStream === 'function' ? bundle.sourcePacks || [] : [];
    const packed = new Set(packs.flatMap(pack => pack.files.map(file => file.sha256)));
    const tasks = [...packs.map(pack => ({ pack })),
      ...Array.from(external.values()).filter(file => !packed.has(file.sha256)).map(file => ({ file }))];
    await pool(tasks, async ({ pack, file }, index, localSignal) => {
      if (file) {
        payloads.set(file.sha256, await verified(sameOrigin(file.href, bundleURL), file.sha256, file.bytes, localSignal));
        return;
      }
      const compressed = await verified(sameOrigin(pack.href, bundleURL), pack.sha256, pack.bytes, localSignal);
      const expanded = await readExact(gzipStream(compressed, localSignal), pack.expanded_bytes, localSignal);
      const cooperate = taskBudget(localSignal);
      for (const member of pack.files) {
        const bytes = expanded.subarray(member.offset, member.offset + member.bytes);
        if (await sha256(bytes) !== member.sha256) throw new Error('A canonical TeX source in a pack failed verification.');
        payloads.set(member.sha256, bytes);
        await cooperate();
      }
    }, signal);
    const files = [];
    for (const file of bundle.files) {
      stop(signal);
      const bytes = file.encoding === 'url' ? payloads.get(file.sha256) : file.encoding === 'utf8' ? encoder.encode(file.content) :
        Uint8Array.from(atob(file.content), char => char.charCodeAt(0));
      if (!bytes || bytes.byteLength !== file.bytes || await sha256(bytes) !== file.sha256) {
        throw new Error('A canonical TeX source or illustration failed verification.');
      }
      // Each mount gets its own buffer: worker transfer must not detach an alias
      // or another member's view into the same decompressed source pack.
      files.push({ path: file.path, bytes: bytes.slice() });
    }
    return { files, cwd: bundle.cwd, entrypoint: bundle.entrypoint.slice(bundle.cwd.length + 1),
      texinputs: bundle.environment && bundle.environment.TEXINPUTS || '', renderSHA256 };
  }

  async function pool(items, action, signal, count = 4) {
    const controller = new AbortController();
    const abort = () => controller.abort();
    signal.addEventListener('abort', abort, { once: true });
    if (signal.aborted) abort();
    let cursor = 0;
    let failure;
    const result = new Array(items.length);
    try {
      await Promise.allSettled(Array.from({ length: Math.min(count, items.length) }, async () => {
        try {
          while (cursor < items.length) {
            stop(controller.signal);
            const i = cursor++;
            result[i] = await action(items[i], i, controller.signal);
          }
        } catch (error) { if (!failure) failure = error; abort(); }
      }));
      if (failure) throw failure;
      stop(signal);
      return result;
    } finally { signal.removeEventListener('abort', abort); }
  }

  async function packageFiles(runtime, base, signal, progress, requested = null) {
    const keys = new Set();
    const expected = new Map();
    for (const file of runtime.texFiles) {
      if (!Number.isSafeInteger(file.format) || file.format < 0 || file.format > 100 ||
          typeof file.name !== 'string' || !file.name || /[\/\\\x00-\x1f]/.test(file.name) || !resourcePin(file)) {
        throw new Error('Invalid native TeX package lookup.');
      }
      const key = file.format + '/' + file.name;
      if (keys.has(key)) throw new Error('Duplicate native TeX package lookup.');
      keys.add(key);
      sameOrigin(file.url, base);
      expected.set(file.sha256 + ':' + file.bytes, file);
    }
    const payloads = new Map();
    if (runtime.texPacks !== undefined) {
      if (!Array.isArray(runtime.texPacks) || runtime.texPacks.length > expected.size) throw new Error('Invalid native TeX package packs.');
      const members = new Set();
      for (const pack of runtime.texPacks) {
        if (!resourcePin(pack) || pack.compression !== 'gzip' ||
            (pack.deferred !== undefined && typeof pack.deferred !== 'boolean') || !Number.isSafeInteger(pack.expanded_bytes) ||
            (pack.font_group !== undefined && (!pack.deferred || typeof pack.font_group !== 'string' ||
              !HASH.test(pack.font_group))) ||
            pack.expanded_bytes < 1 || pack.expanded_bytes > MAX_RESOURCE || !Array.isArray(pack.files) || !pack.files.length ||
            pack.expanded_bytes > PACK_BYTES && pack.files.length !== 1) {
          throw new Error('Invalid native TeX package pack.');
        }
        sameOrigin(pack.url, base);
        let offset = 0;
        for (const file of pack.files) {
          const id = file.sha256 + ':' + file.bytes;
          if (!resourcePin(file) || !expected.has(id) || members.has(id) || file.offset !== offset ||
              offset + file.bytes > pack.expanded_bytes) throw new Error('Invalid native TeX package pack inventory.');
          members.add(id);
          offset += file.bytes;
        }
        if (offset !== pack.expanded_bytes) throw new Error('Incomplete native TeX package pack inventory.');
      }
      if (members.size !== expected.size) throw new Error('Incomplete native TeX package pack inventory.');
    }
    if (runtime.texPacks !== undefined && typeof DecompressionStream === 'function') {
      const groups = new Set(runtime.texPacks.filter(pack => requested && pack.font_group &&
        pack.files.some(file => requested.has(file.sha256 + ':' + file.bytes))).map(pack => pack.font_group));
      const selected = runtime.texPacks.filter(pack => !requested || !pack.deferred ||
        groups.has(pack.font_group) || pack.files.some(file => requested.has(file.sha256 + ':' + file.bytes)));
      const downloaded = downloadProgress(progress, 'Downloading original fonts and packages',
        selected.reduce((total, pack) => total + pack.bytes, 0));
      await pool(selected, async (pack, index, localSignal) => {
        const compressed = await verified(sameOrigin(pack.url, base), pack.sha256, pack.bytes, localSignal,
          MAX_RESOURCE, 'default', downloaded);
        const stream = gzipStream(compressed, localSignal);
        const expanded = await readExact(stream, pack.expanded_bytes, localSignal);
        const cooperate = taskBudget(localSignal);
        for (const file of pack.files) {
          const bytes = expanded.subarray(file.offset, file.offset + file.bytes);
          if (await sha256(bytes) !== file.sha256) throw new Error('A native TeX package in a pack failed verification.');
          stop(localSignal);
          // Engine controllers consume whole ArrayBuffers, not subarray views.
          payloads.set(file.sha256 + ':' + file.bytes, bytes.slice().buffer);
          await cooperate();
        }
      }, signal);
    } else {
      const downloaded = downloadProgress(progress, 'Downloading original fonts and packages',
        Array.from(expected.values()).reduce((total, file) => total + file.bytes, 0));
      await pool(Array.from(expected), async ([id, file], index, localSignal) => {
        const bytes = await verified(sameOrigin(file.url, base), file.sha256, file.bytes, localSignal,
          MAX_RESOURCE, 'default', downloaded);
        payloads.set(id, bytes.buffer);
      }, signal);
    }
    return runtime.texFiles.map(file => ({ format: file.format, filename: file.name,
      data: payloads.get(file.sha256 + ':' + file.bytes), fileId: file.sha256 + ':' + file.bytes,
      deferred: !payloads.has(file.sha256 + ':' + file.bytes) }));
  }

  /* The bridge preserves the original project hierarchy, cwd and TEXINPUTS.
     TeX can read only verified files in this disposable worker's filesystem. */
  const WORKER_BRIDGE = String.raw`
;(function(){
  const originalMessage=self.onmessage;
  const originalCnf=typeof writeTexmfCnf==='function'?writeTexmfCnf:null;
  const originalRun=typeof runMain==='function'?runMain:null;
  let configured=false;
  const packageData=new Map();
  const deferredPaths=new Map();
  const placeholderNodes=new Map();
  const lookupPaths=new Map();
  const missingPackages=new Set();
  const metricNames=new Set();
  const mapPaths=new Set();
  let tracking=false;
  let trackingFailed=false;
  const originalPost=self.postMessage;
  self.postMessage=function(message,...rest){
    if(message.cmd==='compile')message={...message,nativeMissing:Array.from(missingPackages),
      nativeFontHints:missingPackages.size?fontHints():[],
      nativeInventory:deferredPaths.size===0||(tracking&&!trackingFailed)};
    return originalPost.call(self,message,...rest);
  };
  function fontHints(){
    // Only suggest additional bodies after a real missing-file access. The
    // native font map joins metrics already opened by TeX to their Type1
    // bodies, including aliases and reencodings. It never selects a font or
    // authorizes output: the fresh attempt still checks every body access.
    const hints=new Set();
    let remaining=16*1024*1024;
    for(const path of mapPaths){try{
      const size=FS.stat(path).size;
      if(!Number.isSafeInteger(size)||size<0||size>remaining)continue;
      remaining-=size;
      for(const line of FS.readFile(path,{encoding:'utf8'}).split(/\r?\n/)){
        const metric=line.match(/^\s*([^\s%]+)\s/);
        if(!metric||!metricNames.has(metric[1]))continue;
        for(const match of line.matchAll(/<{1,2}([^\s<>[\]]+\.pfb)(?=\s|$)/g)){
          const target=lookupPaths.get('32/'+match[1])||lookupPaths.get('32/'+match[1].slice(0,-4));
          const id=deferredPaths.get(target);
          if(id)hints.add(id);
        }
      }
    }catch(_){/* Missing or unusual maps leave native discovery in charge. */}}
    return Array.from(hints);
  }
  function track(path){
    if(typeof path==='string'){
      if(path.endsWith('.tfm'))metricNames.add(path.split('/').pop().slice(0,-4));
      if(path.endsWith('.map'))mapPaths.add(path);
    }
    const id=deferredPaths.get(path);if(id)missingPackages.add(id);
  }
  function trackDeferred(){
    if(!deferredPaths.size)return true;
    if(typeof FS.open!=='function'||typeof FS.getPath!=='function'||
       typeof PATH_FS==='undefined'||typeof PATH_FS.resolve!=='function'||
       typeof kpse_find_file_impl!=='function'||typeof UTF8ToString!=='function')return false;
    const open=FS.open;
    FS.open=function(path,...args){
      try{track(typeof path==='string'?PATH_FS.resolve(path):FS.getPath(path));}
      catch(_){trackingFailed=true;}
      const stream=open.call(FS,path,...args);
      try{track(FS.getPath(stream.node));}catch(_){trackingFailed=true;}
      return stream;
    };
    const resolve=kpse_find_file_impl;
    kpse_find_file_impl=function(pointer,format,mustexist){
      try{track(lookupPaths.get(format+'/'+UTF8ToString(pointer).replace(/^[*&]/,'')));}
      catch(_){trackingFailed=true;}
      return resolve(pointer,format,mustexist);
    };
    self.kpse_find_file_impl=kpse_find_file_impl;
    tracking=true;
    return true;
  }
  if(originalRun)runMain=function(program,args){return originalRun(program,['-no-shell-escape','-halt-on-error'].concat(args));};
  self.onmessage=function(event){
    const data=event.data;
    if(data.cmd==='triptych-mkdir'){
      try{FS.mkdirTree('/work/'+data.path);self.postMessage({cmd:data.cmd,result:'ok'});}
      catch(error){self.postMessage({cmd:data.cmd,result:'failed',error:String(error.message)});}
      return;
    }
    if(data.cmd==='triptych-preload'){
      const post=self.postMessage;
      try{
        for(const item of data.payloads){
          if(packageData.has(item.id))throw Error('A package payload was sent twice.');
          packageData.set(item.id,item.data);
        }
        self.postMessage=function(message,...rest){
          if(message.cmd==='preloadtexlive'&&message.result==='ok')return;
          return post.call(self,message,...rest);
        };
        for(const file of data.files){
          const bytes=packageData.get(file.fileId);
          if(!bytes&&!file.deferred)throw Error('A package payload is missing.');
          let path;
          if(typeof texlive200_cache!=='undefined'){
            if(typeof cacheFileName==='function')path=TEXCACHEROOT+'/'+cacheFileName(file.format,file.filename);
            else if(file.deferred)throw Error('The typesetter cannot track deferred packages.');
          }else{
            let name=file.filename;
            if(file.format===3&&!name.endsWith('.tfm'))name+='.tfm';
            if(file.format===33&&!name.endsWith('.vf'))name+='.vf';
            path='/tex/'+name;
          }
          if(path){
            lookupPaths.set(file.format+'/'+file.filename,path);
            const previous=placeholderNodes.get(path);
            if(previous){previous.node.node_ops=previous.ops;placeholderNodes.delete(path);}
            if(file.deferred)deferredPaths.set(path,file.fileId);else deferredPaths.delete(path);
          }
          // Preserve all original positive lookups and the complete directory
          // shape. A content access to an omitted body invalidates this attempt.
          if(typeof texlive200_cache!=='undefined'){
            originalMessage.call(self,{data:{cmd:'preloadtexlive',format:file.format,filename:file.filename,
              data:bytes||new ArrayBuffer(0)}});
          }else{
            FS.writeFile(path,new Uint8Array(bytes||new ArrayBuffer(0)));
            texlive200[file.format+'/'+file.filename]=path;
          }
          if(file.deferred){
            const node=FS.lookupPath(path).node;
            const ops=node.node_ops;
            const size=Number(file.fileId.split(':')[1]);
            // kpathsea scans and stats the whole directory. Its metadata is
            // fully known without font bytes; preserve it exactly. Opening
            // an omitted body still marks the entire attempt provisional.
            node.node_ops={...ops,getattr(value){const stat=ops.getattr(value);
              return {...stat,size,blocks:Math.ceil(size/stat.blksize)};}};
            placeholderNodes.set(path,{node,ops});
          }
        }
        if(data.final&&!data.retain)packageData.clear();
        post.call(self,{cmd:data.cmd,result:'ok'});
      }catch(error){post.call(self,{cmd:data.cmd,result:'failed',error:String(error.message)});}
      finally{self.postMessage=post;}
      return;
    }
    if(data.cmd==='triptych-take-packages'){
      const payloads=Array.from(packageData,([id,data])=>({id,data}));
      packageData.clear();
      self.postMessage({cmd:data.cmd,result:'ok',payloads},payloads.map(item=>item.data));
      return;
    }
    if(data.cmd==='triptych-configure'){
      try{
        WORKROOT='/work/'+data.cwd;
        FS.chdir(WORKROOT);
        const inputs='.;'+data.texinputs.split(':').filter(Boolean).join(';')+';/tex//';
        if(originalCnf)writeTexmfCnf=function(building){
          originalCnf(building);
          const path=WORKROOT+'/texmf.cnf';
          const value=FS.readFile(path,{encoding:'utf8'}).replace(/^TEXINPUTS\s*=.*$/m,'TEXINPUTS = '+inputs)
            +'\nshell_escape = f\nshell_escape_commands = ,\nfont_max = 9000\n';
          FS.writeFile(path,value);
          if(typeof texlive200_cache==='undefined')FS.writeFile('/work/texmf.cnf',value);
        };
        if(typeof texlive200_cache==='undefined'){
          FS.writeFile('/work/xetex','');
          FS.writeFile('/work/xdvipdfmx','');
          const config=texlive200['26/dvipdfmx.cfg'];
          if(config){
            const bytes=FS.readFile(config,{encoding:'binary'});
            FS.writeFile(WORKROOT+'/dvipdfmx.cfg',bytes);
            FS.writeFile('/work/dvipdfmx.cfg',bytes);
          }
        }
        configured=true;
        if(data.icu)self.icuData=new Uint8Array(data.icu);
        self.postMessage({cmd:data.cmd,result:'ok',nativeInventory:trackDeferred()});
      }catch(error){self.postMessage({cmd:data.cmd,result:'failed',error:String(error.message)});}
      return;
    }
    if(data.cmd==='triptych-state'){
      const files=[];let size=0;
      function visit(dir){for(const name of FS.readdir(dir)){
        if(name==='.'||name==='..')continue;
        const path=dir+'/'+name;const stat=FS.stat(path);
        if(FS.isDir(stat.mode)){visit(path);continue;}
        if(/\.(aux|toc|out|lof|lot|lol|ent|idx|ind|bbl|bcf|nav|snm)$/.test(name)){
          const bytes=FS.readFile(path,{encoding:'binary'});size+=bytes.byteLength;
          if(size>67108864)throw Error('Auxiliary files exceed the print limit.');
          files.push({path:path.slice(WORKROOT.length+1),bytes:bytes});
        }
      }}
      try{visit(WORKROOT);self.postMessage({cmd:data.cmd,result:'ok',files:files});}
      catch(error){self.postMessage({cmd:data.cmd,result:'failed',error:String(error.message)});}
      return;
    }
    if(data.cmd==='compilelatex'&&!configured){self.postMessage({cmd:'compile',result:'failed',error:'Native working directory was not configured.'});return;}
    return originalMessage.call(self,event);
  };
})();`;

  async function engineWorker(descriptor, runtimeBase, signal, progress, blobs) {
    if (!descriptor || !descriptor.worker || !descriptor.core || !descriptor.wasm) {
      throw new Error('The selected native TeX engine is not available.');
    }
    const assets = {};
    const listed = ['worker', 'core', 'wasm'].map(name => [name, descriptor[name]]);
    for (const item of descriptor.support || []) listed.push(['support', item]);
    const downloaded = downloadProgress(progress, 'Downloading the typesetter',
      listed.reduce((total, [name, item]) => total + transportPin(item, runtimeBase).bytes, 0));
    const values = await pool(listed, async (entry, index, localSignal) => {
      const [name, item] = entry;
      const url = sameOrigin(item.url, runtimeBase);
      const bytes = await engineResource(item, runtimeBase, localSignal, downloaded);
      const mime = name === 'wasm' ? 'application/wasm' : 'text/javascript';
      const blob = URL.createObjectURL(new Blob([bytes], { type: mime }));
      blobs.push(blob);
      assets[new URL(url).pathname.split('/').pop()] = blob;
      return [name, bytes];
    }, signal);
    const workerBytes = values.find(item => item[0] === 'worker')[1];
    const prelude = 'const __nativeAssets=' + JSON.stringify(assets) + ';\n' + String.raw`
const __nativeImport=self.importScripts.bind(self);
const __nativeFetch=self.fetch.bind(self);
self.fetch=function(url,options){
  if(!Object.values(__nativeAssets).includes(String(url)))return Promise.reject(Error('Unverified native engine resource.'));
  return __nativeFetch(url,options);
};
/* A missing optional package is a normal kpathsea miss. Report it locally;
   never make a network request and never unwind the native engine's stack. */
self.XMLHttpRequest=class{
  constructor(){this.status=404;this.response=new ArrayBuffer(0);}
  open(){}
  send(){}
  getResponseHeader(){return null;}
};
self.importScripts=function(...urls){
  for(const url of urls){
    const name=String(url).split('/').pop();
    if(!Object.hasOwn(__nativeAssets,name))throw Error('Unverified native engine script.');
    if(self.Module)self.Module.locateFile=function(file){
      const target=__nativeAssets[file.split('/').pop()];
      if(!target)throw Error('Unverified native engine binary.');
      return target;
    };
    __nativeImport(__nativeAssets[name]);
  }
};
`;
    let controller = new TextDecoder('utf-8', { fatal: true }).decode(workerBytes);
    /* The Unicode controllers declare a fixed cwd constant. Make only this
       binding configurable so the canonical project need not be rewritten. */
    if (controller.includes("const WORKROOT = '/work'")) {
      controller = controller.replace("const WORKROOT = '/work'", "var WORKROOT = '/work'");
    }
    const source = prelude + '\n' + controller + '\n' + WORKER_BRIDGE;
    const url = URL.createObjectURL(new Blob([source], { type: 'text/javascript' }));
    blobs.push(url);
    stop(signal);
    progress('Starting the typesetter…');
    const worker = new Worker(url);
    let active = null;
    let closed = false;
    let readyResolve;
    let readyReject;
    const ready = new Promise((resolve, reject) => { readyResolve = resolve; readyReject = reject; });
    function fail(error) {
      readyReject(error);
      if (active) { const pending = active; active = null; clearTimeout(pending.timer); pending.reject(error); }
    }
    function abort() { fail(new DOMException('PDF generation cancelled.', 'AbortError')); worker.terminate(); closed = true; }
    if (signal) signal.addEventListener('abort', abort, { once: true });
    worker.onerror = event => fail(new Error('The native TeX engine stopped: ' + (event.message || 'worker failure')));
    worker.onmessage = event => {
      const data = event.data;
      if (data.result === 'ok' && !data.cmd) { readyResolve(); return; }
      if (active && data.cmd === active.expected) {
        const pending = active; active = null; clearTimeout(pending.timer);
        // Compilation failures may be provisional missing-font attempts.
        // The caller checks their inventory before accepting status or output.
        if (data.result === 'failed' && data.cmd !== 'compile') {
          const error = new Error(data.error || 'Native TeX compilation failed.');
          error.log = data.log;
          pending.reject(error);
        }
        else pending.resolve(data);
      }
    };
    const startTimer = setTimeout(() => fail(new Error('The native TeX engine did not start in time.')), 60000);
    try { await ready; stop(signal); } catch (error) {
      worker.terminate();
      if (signal) signal.removeEventListener('abort', abort);
      throw error;
    }
    finally { clearTimeout(startTimer); }
    return {
      async ask(payload, expected = payload.cmd, timeout = 900000, transfer = []) {
        stop(signal);
        if (closed || active) throw new Error('The native TeX worker is unavailable.');
        return new Promise((resolve, reject) => {
          const timer = setTimeout(() => { fail(new Error('Native TeX compilation exceeded its time limit.')); worker.terminate(); closed = true; }, timeout);
          active = { resolve, reject, expected, timer };
          try { worker.postMessage(payload, transfer); }
          catch (error) { clearTimeout(timer); active = null; reject(error); }
        });
      },
      tell(payload) { stop(signal); worker.postMessage(payload); },
      close() {
        closed = true;
        fail(new DOMException('The native print worker was closed.', 'AbortError'));
        if (signal) signal.removeEventListener('abort', abort);
        worker.terminate();
      }
    };
  }

  async function auxiliaryState(worker) {
    const state = await worker.ask({ cmd: 'triptych-state' });
    if (!Array.isArray(state.files)) throw new Error('The native TeX auxiliary state could not be verified.');
    const identities = [];
    for (const file of state.files) identities.push([file.path, await sha256(new Uint8Array(file.bytes))]);
    identities.sort((a, b) => a[0].localeCompare(b[0], 'en'));
    return sha256(encoder.encode(JSON.stringify(identities)));
  }

  function compressedFormat(pin, base) {
    return pin.compression === 'gzip' || new URL(pin.url, base).pathname.endsWith('.gz');
  }

  async function formatBytes(pin, base, signal, progress) {
    const downloaded = downloadProgress(progress, 'Downloading the print format', transportPin(pin, base).bytes);
    const bytes = await engineResource(pin, base, signal, downloaded);
    if (!compressedFormat(pin, base)) return bytes;
    if (typeof DecompressionStream !== 'function') throw new Error('This browser cannot unpack the native TeX format.');
    const stream = gzipStream(bytes, signal);
    const expanded = new Uint8Array(await new Response(stream).arrayBuffer());
    if (!expanded.length || expanded.length > 64 * 1024 * 1024) throw new Error('The native TeX format exceeds its permitted size.');
    return expanded;
  }

  async function preloadPackages(worker, texFiles, retain) {
    const sent = new Set();
    let files = [];
    let payloads = [];
    let size = 0;
    async function flush(final) {
      await worker.ask({ cmd: 'triptych-preload', files, payloads, final, retain }, 'triptych-preload', 900000,
        Array.from(new Set(payloads.map(item => item.data))));
      files = []; payloads = []; size = 0;
    }
    // Keep every original lookup in order: different format keys can target
    // one filesystem name. Later aliases refer to worker-owned payload IDs.
    for (const file of texFiles) {
      const bytes = file.deferred || sent.has(file.fileId) ? 0 : file.data.byteLength;
      if (files.length && (files.length >= 128 || size + bytes > PACK_BYTES)) await flush(false);
      if (!file.deferred && !sent.has(file.fileId)) {
        payloads.push({ id: file.fileId, data: file.data });
        sent.add(file.fileId);
        size += bytes;
      }
      files.push({ format: file.format, filename: file.filename, fileId: file.fileId, deferred: file.deferred });
    }
    await flush(true);
  }

  async function recoverPackages(worker, texFiles, signal) {
    const returned = await worker.ask({ cmd: 'triptych-take-packages' });
    if (!Array.isArray(returned.payloads)) throw new Error('The typesetter did not return its original font data.');
    const expected = new Set(texFiles.filter(file => !file.deferred).map(file => file.fileId));
    const payloads = new Map();
    const cooperate = taskBudget(signal);
    for (const item of returned.payloads) {
      stop(signal);
      if (!expected.has(item.id) || payloads.has(item.id) || !(item.data instanceof ArrayBuffer) ||
          item.data.byteLength !== Number(item.id.split(':')[1])) throw new Error('The typesetter returned incomplete font data.');
      if (await sha256(new Uint8Array(item.data)) !== item.id.split(':')[0]) throw new Error('The typesetter changed the original font data.');
      payloads.set(item.id, item.data);
      await cooperate();
    }
    if (payloads.size !== expected.size) throw new Error('The typesetter returned incomplete font data.');
    for (const file of texFiles) if (!file.deferred) file.data = payloads.get(file.fileId);
  }

  async function mountProject(worker, project, texFiles, icu, retainPackages = false) {
    await preloadPackages(worker, texFiles, retainPackages);
    const directories = new Set();
    for (const file of project.files) {
      const directory = file.path.split('/').slice(0, -1).join('/');
      if (directory && !directories.has(directory)) {
        await worker.ask({ cmd: 'triptych-mkdir', path: directory });
        directories.add(directory);
      }
      await worker.ask({ cmd: 'writefile', url: file.path, src: file.bytes });
    }
    return worker.ask({ cmd: 'triptych-configure', cwd: project.cwd, texinputs: project.texinputs, icu: icu && icu.buffer },
      'triptych-configure', 900000, icu ? [icu.buffer] : []);
  }

  function checkLog(log, final) {
    if (typeof log !== 'string' || /(?:^|\n)!|Fatal error|Emergency stop|no output PDF file|Missing character:|Font .*not loadable|font .*not found|Font shape[\s\S]{0,300}?undefined|Some font shapes were not available,\s*defaults substituted/i.test(log)) {
      throw new Error('The native TeX edition could not be typeset completely. No substitute PDF was created.');
    }
    if (final && /undefined references|undefined citations|There were undefined|Rerun to get|Label\(s\) may have changed|Please (?:re)?run|Rerun .*get .*right/i.test(log)) {
      return false;
    }
    return true;
  }

  async function generate(options) {
    const outer = new AbortController();
    const signal = outer.signal;
    const upstream = options.signal;
    const relay = () => outer.abort();
    if (upstream) upstream.addEventListener('abort', relay, { once: true });
    if (upstream && upstream.aborted) outer.abort();
    const timer = setTimeout(() => outer.abort(), 20 * 60 * 1000);
    const progress = (message, detail = {}) => {
      if (!signal.aborted && typeof options.onProgress === 'function') options.onProgress({ ...detail,
        message: detail.stage === 'ready' ? message : message + ' Keep this page visible until it finishes.' });
    };
    const blobs = [];
    const releaseBlobs = () => { for (const url of blobs.splice(0)) URL.revokeObjectURL(url); };
    let worker;
    let converter;
    try {
      stop(signal);
      const bundleURL = sameOrigin(options.bundleURL, document.baseURI);
      const runtimeURL = sameOrigin(options.runtimeURL, document.baseURI);
      const sourceDownload = downloadProgress(progress, 'Checking the original sources and print runtime',
        options.bundleBytes + options.runtimeBytes);
      const bundleBody = await verified(bundleURL, options.bundleSHA256, options.bundleBytes, signal, MAX_RESOURCE, 'default', sourceDownload);
      const bundle = json(bundleBody, 'native source bundle');
      const renderSHA256 = await sourceRenderIdentity(bundle, bundleURL);
      const key = options.cache === false ? null : await cacheKey(options, bundleURL, runtimeURL, renderSHA256);
      if (key) {
        const cached = await cachedPDF(key, signal);
        stop(signal);
        if (cached) {
          progress('The typeset PDF is ready.', { stage: 'ready' });
          return { ...cached, document: bundle.document, output_id: bundle.output_id, source_revision: bundle.source_revision };
        }
      }
      if (typeof Worker !== 'function' || typeof WebAssembly !== 'object') {
        throw new Error('This browser cannot run the native typesetter. Use a browser with WebAssembly and worker support.');
      }
      // The content pin makes even the legacy stable route an immutable HTTP
      // cache key. A different release cannot reuse an earlier manifest body.
      const runtimeRequest = new URL(runtimeURL);
      runtimeRequest.searchParams.set('sha256', options.runtimeSHA256);
      const runtimeBody = await verified(runtimeRequest.href, options.runtimeSHA256, options.runtimeBytes, signal, MAX_RESOURCE, 'default', sourceDownload);
      const runtime = json(runtimeBody, 'native print runtime');
      if (runtime.schema !== RUNTIME_SCHEMA || !runtime.engines || !Array.isArray(runtime.texFiles) || runtime.texFiles.length > 50000) {
        throw new Error('Unsupported native TeX runtime manifest.');
      }
      const kind = bundle.engine === 'xetex' ? 'xelatex' : 'pdflatex';
      const descriptor = runtime.engines[kind];
      if (!descriptor || !descriptor.format) throw new Error('The selected native TeX format is unavailable.');
      /* Runtime payload routes are site-root relative, independent of the root's depth. */
      const assetBase = runtime.asset_base ? sameOrigin(runtime.asset_base, runtimeURL) : new URL('/', runtimeURL).href;
      if (compressedFormat(descriptor.format, assetBase) && typeof DecompressionStream !== 'function') {
        throw new Error('This browser cannot unpack the native TeX format. Use a browser with gzip decompression support.');
      }
      const engines = kind === 'xelatex' ? [descriptor, runtime.engines.dvipdfmx] : [descriptor];
      if (kind === 'xelatex' && !descriptor.icu) throw new Error('The native Unicode font data is unavailable.');
      for (const engine of engines) {
        if (!engine) throw new Error('The selected native TeX engine is not available.');
        for (const pin of [engine.worker, engine.core, engine.wasm, ...(engine.support || []),
          ...(engine.format ? [engine.format] : []), ...(engine.icu ? [engine.icu] : [])]) transportPin(pin, assetBase);
      }
      const project = await sourceFiles(bundle, bundleURL, signal);
      let requested = Array.isArray(runtime.texPacks) &&
        runtime.texPacks.some(pack => pack.deferred === true) && typeof DecompressionStream === 'function' ? new Set() : null;
      let texFiles;
      let result = null;
      let passes = 0;
      let settled = false;
      // Each provisional attempt is disposable. The fourth attempt uses the
      // complete original registry, bounding both restarts and discovery work.
      for (let attempt = 0; attempt < 4; attempt++) {
        if (attempt === 3) requested = null;
        texFiles = await packageFiles(runtime, assetBase, signal, progress, requested);
        const deferred = new Set(texFiles.filter(file => file.deferred).map(file => file.fileId));
        worker = await engineWorker(descriptor, assetBase, signal, progress, blobs);
        let icu = null;
        if (kind === 'xelatex') {
          const downloaded = downloadProgress(progress, 'Downloading original font support', transportPin(descriptor.icu, assetBase).bytes);
          icu = await engineResource(descriptor.icu, assetBase, signal, downloaded);
        } else {
          await worker.ask({ cmd: 'setpreamblesnapshot', enabled: false });
        }
        progress('Loading original fonts and sources into the typesetter…');
        const mounted = await mountProject(worker, project, texFiles, icu, kind === 'xelatex');
        icu = null;
        if (deferred.size && mounted.nativeInventory !== true) {
          worker.close(); worker = null; releaseBlobs(); requested = null;
          continue;
        }
        const format = await formatBytes(descriptor.format, assetBase, signal, progress);
        if (kind === 'xelatex') await worker.ask({ cmd: 'writefile', url: 'wasmtex-xetex.fmt', src: format }, 'writefile', 900000, [format.buffer]);
        else await worker.ask({ cmd: 'loadformat', data: format.buffer }, 'loadformat', 900000, [format.buffer]);
        worker.tell({ cmd: 'setmainfile', url: project.entrypoint });
        const needsPackages = response => {
          if (!deferred.size) return false;
          if (!Array.isArray(response.nativeMissing) || response.nativeMissing.length > deferred.size ||
              new Set(response.nativeMissing).size !== response.nativeMissing.length ||
              response.nativeMissing.some(id => !deferred.has(id))) {
            throw new Error('The typesetter did not verify its complete package inventory.');
          }
          // This check precedes status, fatal logs and PDF acceptance, including
          // successful optional probes in either native engine.
          if (response.nativeInventory !== true) { requested = null; return true; }
          if (!response.nativeMissing.length) return false;
          for (const id of response.nativeMissing) requested.add(id);
          // Hints only expand a required retry. Unknown or absent hints are
          // ignored; actual accesses and the complete-inventory fallback
          // retain authority when a map is unusual or discovery is partial.
          const hints = response.nativeFontHints;
          if (Array.isArray(hints) && hints.length <= deferred.size && hints.every(id => deferred.has(id))) {
            for (const id of hints) requested.add(id);
          }
          return true;
        };
        let previous = null;
        let retry = false;
        for (passes = 1; passes <= 8; passes++) {
          progress('Typesetting with the original TeX layout (pass ' + passes + ')…');
          result = await worker.ask({ cmd: 'compilelatex' }, 'compile');
          if (needsPackages(result)) { retry = true; break; }
          checkLog(result.log, false);
          if (result.status !== 0 || !result.pdf) throw new Error('The native TeX edition did not compile successfully.');
          const current = await auxiliaryState(worker);
          if (passes >= 2 && current === previous && checkLog(result.log, true)) break;
          previous = current;
        }
        if (retry) {
          worker.close(); worker = null; releaseBlobs();
          progress('Loading the original fonts selected by this document…');
          continue;
        }
        if (passes > 8) throw new Error('The TeX references or contents did not settle. No incomplete PDF was offered.');
        if (kind === 'xelatex') {
          progress('Embedding the original fonts in the typeset PDF…');
          await recoverPackages(worker, texFiles, signal);
          worker.close();
          worker = null;
          releaseBlobs();
          converter = await engineWorker(runtime.engines.dvipdfmx, assetBase, signal, progress, blobs);
          const conversionMount = await mountProject(converter, project, texFiles, null);
          if (deferred.size && conversionMount.nativeInventory !== true) {
            converter.close(); converter = null; releaseBlobs(); requested = null;
            continue;
          }
          const stem = project.entrypoint.split('/').pop().replace(/\.[^.]+$/, '');
          await converter.ask({ cmd: 'writefile', url: stem + '.xdv', src: new Uint8Array(result.pdf) }, 'writefile', 900000, [result.pdf]);
          converter.tell({ cmd: 'setmainfile', url: stem + '.xdv' });
          const converted = await converter.ask({ cmd: 'compilepdf' }, 'compile');
          if (needsPackages(converted)) {
            converter.close(); converter = null; releaseBlobs();
            progress('Loading the original fonts selected by this document…');
            continue;
          }
          if (converted.status !== 0 || !converted.pdf) throw new Error('The typeset Unicode edition could not be converted to PDF.');
          checkLog(converted.log, false);
          converted.log = result.log + '\n' + converted.log;
          result = converted;
        }
        settled = true;
        break;
      }
      if (!settled) throw new Error('The native TeX package inventory could not be completed.');
      const bytes = new Uint8Array(result.pdf);
      if (bytes.length < 5 || new TextDecoder().decode(bytes.slice(0, 5)) !== '%PDF-' || bytes.length > MAX_RESOURCE) {
        throw new Error('The native TeX engine did not produce a valid PDF.');
      }
      stop(signal);
      const output = { bytes, sha256: await sha256(bytes), byteLength: bytes.byteLength, passes, log: result.log,
        document: bundle.document, output_id: bundle.output_id, source_revision: bundle.source_revision, runtime: runtime.id, cached: false };
      stop(signal);
      if (key) await rememberPDF(key, output, signal);
      stop(signal);
      progress('The typeset PDF is ready.', { stage: 'ready' });
      return output;
    } finally {
      if (worker) worker.close();
      if (converter) converter.close();
      outer.abort();
      releaseBlobs();
      clearTimeout(timer);
      if (upstream) upstream.removeEventListener('abort', relay);
    }
  }

  global.TriptychNativeTeX = Object.freeze({ generate });
})(window);
