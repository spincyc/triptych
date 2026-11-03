/* Request the authored TeX PDF. Browser reflow is never a substitute. */
(function () {
  'use strict';
  const SCHEMA = 'triptych-native-print/v1';
  const installations = new WeakMap();
  const need = (condition, message) => { if (!condition) throw new Error(message); };
  const hex40 = (value) => typeof value === 'string' && /^[0-9a-f]{40}$/.test(value);
  const hex64 = (value) => typeof value === 'string' && /^[0-9a-f]{64}$/.test(value);
  const identity = (value) => typeof value === 'string' &&
    /^(?:publication:(?:gpt|claude)\/|bible:|reading-plan:|papal:)[a-z0-9][a-z0-9./-]*$/.test(value) &&
    !value.includes('..') && !value.includes('//') && !value.endsWith('/');

  function endpoint(value) {
    need(typeof value === 'string', 'The PDF service address is invalid.');
    if (!value) return null;
    need(!/[\s\\]/u.test(value), 'The PDF service address is invalid.');
    const url = new URL(value);
    need(url.protocol === 'https:' || url.protocol === 'http:' &&
      ['localhost', '127.0.0.1', '[::1]'].includes(url.hostname), 'The PDF service requires HTTPS.');
    need(!url.username && !url.password && !url.search && !url.hash &&
      !url.pathname.replace(/\/+$/, '').endsWith('/v1'), 'The PDF service address is invalid.');
    return url.href.replace(/\/+$/, '');
  }

  function selection(value) {
    need(value && typeof value === 'object' && value.schema === SCHEMA &&
      identity(value.id) && identity(value.document) &&
      ['main', 'synthesis', 'homily'].includes(value.edition) &&
      hex40(value.source_revision) && typeof value.title === 'string' && value.title.trim(),
    'The native PDF selection is incomplete.');
    endpoint(value.endpoint);
    if (value.wasm != null) {
      need(value.wasm && typeof value.wasm === 'object', 'The TeX compiler selection is invalid.');
      resourceURL(value.wasm.bundle);
      resourceURL(value.wasm.runtime);
      need(hex64(value.wasm.bundle_sha256) && hex64(value.wasm.runtime_sha256) &&
        Number.isSafeInteger(value.wasm.bundle_bytes) && value.wasm.bundle_bytes > 0 &&
        Number.isSafeInteger(value.wasm.runtime_bytes) && value.wasm.runtime_bytes > 0,
      'The TeX compiler resources have no exact identity.');
    }
    if (!value.id.startsWith('publication:')) {
      need(value.edition === 'main' && value.id === value.document, 'The native PDF edition is inconsistent.');
    } else {
      need(value.id === value.document + (value.edition === 'main' ? '' : '-' + value.edition),
        'The native PDF edition is inconsistent.');
    }
    return Object.freeze({...value});
  }

  function resourceURL(value) {
    need(typeof value === 'string' && value && !/[\s\\]/u.test(value), 'A TeX compiler resource address is invalid.');
    const url = new URL(value, location.href);
    need(url.origin === location.origin && !url.username && !url.password && !url.search && !url.hash,
      'A TeX compiler resource must belong to this site.');
    return url.href;
  }

  async function wasmTransport(chosen, options) {
    need(chosen.wasm && window.TriptychNativeTeX && typeof window.TriptychNativeTeX.generate === 'function',
      'The native TeX compiler could not be loaded. Please reload this page.');
    const generated = await window.TriptychNativeTeX.generate({
      bundleURL: resourceURL(chosen.wasm.bundle), runtimeURL: resourceURL(chosen.wasm.runtime),
      bundleSHA256: chosen.wasm.bundle_sha256, bundleBytes: chosen.wasm.bundle_bytes,
      runtimeSHA256: chosen.wasm.runtime_sha256, runtimeBytes: chosen.wasm.runtime_bytes,
      signal: options.signal, onProgress: (value) => {
        const message = typeof value === 'string' ? value : value && value.message;
        if (message && options.onStatus) options.onStatus(message);
      }
    });
    need(generated && generated.bytes instanceof Uint8Array && generated.byteLength === generated.bytes.byteLength &&
      generated.byteLength > 5 && new TextDecoder().decode(generated.bytes.subarray(0, 5)) === '%PDF-' &&
      hex64(generated.sha256), 'The TeX compiler did not produce a complete PDF.');
    need(window.crypto && window.crypto.subtle, 'PDF integrity verification is unavailable.');
    const hash = await window.crypto.subtle.digest('SHA-256', generated.bytes);
    const actual = Array.from(new Uint8Array(hash), (value) => value.toString(16).padStart(2, '0')).join('');
    need(actual === generated.sha256, 'The compiled PDF failed verification.');
    if (options.signal.aborted) throw new DOMException('Cancelled', 'AbortError');
    const blob = new Blob([generated.bytes], {type: 'application/pdf'});
    return {url: URL.createObjectURL(blob), sha256: actual, bytes: generated.byteLength};
  }

  function apiURL(base, path) {
    return base + path;
  }

  function job(value, chosen, base, previous) {
    need(value && typeof value === 'object' && hex64(value.key) &&
      value.source_revision === chosen.source_revision &&
      value.document === chosen.document && value.edition === chosen.edition &&
      (!value.output_id || value.output_id === chosen.id) &&
      ['queued', 'building', 'ready', 'failed'].includes(value.state),
    'The PDF service returned a different or invalid edition.');
    if (previous) need(value.key === previous, 'The PDF job changed while it was being prepared.');
    const statusPath = '/v1/jobs/' + value.key;
    // API paths are relative to the configured service, including any proxy
    // prefix. Validate before constructing a URL so a leading slash cannot
    // discard that prefix or redirect polling to another origin.
    need(value.status_url === statusPath || value.status_url === apiURL(base, statusPath),
      'The PDF service returned an invalid status address.');
    if (value.state === 'ready') {
      need(value.pdf_url === statusPath + '/pdf' || value.pdf_url === apiURL(base, statusPath + '/pdf'),
        'The PDF service returned an invalid download address.');
    } else {
      need(value.pdf_url == null, 'An unfinished PDF was offered for download.');
    }
    return value;
  }

  function delay(milliseconds, signal) {
    return new Promise((resolve, reject) => {
      const aborted = () => { clearTimeout(timer); reject(new DOMException('Cancelled', 'AbortError')); };
      const timer = setTimeout(() => { signal.removeEventListener('abort', aborted); resolve(); }, milliseconds);
      signal.addEventListener('abort', aborted, {once: true});
      if (signal.aborted) aborted();
    });
  }

  async function requestJSON(url, options, fetcher) {
    const response = await fetcher(url, {...options, credentials: 'omit', cache: 'no-store', redirect: 'error'});
    if (response.status === 409) throw new Error('The print service has a different text revision. Reload this page or try again after it updates.');
    if (response.status === 429 || response.status === 503) throw new Error('The PDF service is busy. Please try again shortly.');
    need(response.ok, 'The PDF service could not prepare this edition.');
    need((response.headers.get('Content-Type') || '').toLowerCase().includes('application/json'),
      'The PDF service returned an invalid response.');
    const text = await response.text();
    need(text.length <= 32768, 'The PDF service response is too large.');
    return JSON.parse(text);
  }

  async function serviceTransport(chosen, options) {
    const base = endpoint(chosen.endpoint);
    need(base, 'PDF generation is not connected to a typesetting service yet. An earlier TeX PDF may be available below.');
    const fetcher = options.fetch || window.fetch.bind(window);
    const onStatus = options.onStatus || (() => {});
    const signal = options.signal;
    const timeout = Date.now() + 30 * 60 * 1000;
    let current = job(await requestJSON(apiURL(base, '/v1/jobs'), {
      method: 'POST', signal, headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({document: chosen.document, edition: chosen.edition, source_revision: chosen.source_revision})
    }, fetcher), chosen, base);
    while (current.state !== 'ready') {
      if (current.state === 'failed') throw new Error(current.error || 'The original TeX edition could not be typeset.');
      onStatus(current.state === 'queued' ? 'Waiting for the typesetter…' : 'Typesetting the original TeX edition…');
      need(Date.now() < timeout, 'The PDF is taking longer than expected. Please try again.');
      await delay(options.pollMilliseconds == null ? 1500 : options.pollMilliseconds, signal);
      current = job(await requestJSON(apiURL(base, '/v1/jobs/' + current.key), {signal}, fetcher), chosen, base, current.key);
    }
    return {url: apiURL(base, '/v1/jobs/' + current.key + '/pdf'), job: current};
  }

  function install(root, descriptor, options) {
    if (installations.has(root)) return installations.get(root);
    options = options || {};
    const chosen = selection(descriptor);
    need(root.dataset.nativePrint === chosen.id, 'The PDF controls identify another edition.');
    const start = root.querySelector('[data-native-print-start]');
    const cancel = root.querySelector('[data-native-print-cancel]');
    const download = root.querySelector('[data-native-print-download]');
    const status = root.querySelector('[data-native-print-status]');
    need(start && cancel && download && status, 'The PDF controls are incomplete.');
    let generation = 0;
    let active = null;
    let currentURL = null;

    function reset(message) {
      generation += 1;
      if (active) active.abort();
      active = null;
      if (currentURL && currentURL.startsWith('blob:')) URL.revokeObjectURL(currentURL);
      currentURL = null;
      download.hidden = true;
      download.removeAttribute('href');
      start.disabled = false;
      cancel.hidden = true;
      root.removeAttribute('aria-busy');
      status.textContent = message || '';
    }

    async function generate() {
      reset();
      const ownGeneration = generation;
      const address = location.href;
      const controller = new AbortController();
      active = controller;
      start.disabled = true;
      cancel.hidden = false;
      root.setAttribute('aria-busy', 'true');
      status.textContent = 'Preparing the TeX PDF…';
      root.dataset.nativePrintState = 'preparing';
      try {
        const transport = options.transport || (chosen.wasm ? wasmTransport : serviceTransport);
        const result = await transport(chosen, {
          ...options, signal: controller.signal,
          onStatus: (message) => { if (generation === ownGeneration) status.textContent = message; }
        });
        if (generation !== ownGeneration || address !== location.href || controller.signal.aborted) return false;
        need(result && typeof result.url === 'string', 'The typesetter returned no PDF.');
        const target = new URL(result.url, location.href);
        need(target.protocol === 'blob:' || target.protocol === 'https:' ||
          target.protocol === 'http:' && ['localhost', '127.0.0.1', '[::1]'].includes(target.hostname),
        'The typesetter returned an invalid PDF address.');
        currentURL = target.href;
        download.href = currentURL;
        download.download = chosen.id.split('/').pop().replace(':', '-') + '.pdf';
        download.hidden = false;
        download.setAttribute('aria-label', 'Download PDF — ' + chosen.title);
        root.dataset.nativePrintState = 'ready';
        status.textContent = 'The TeX PDF is ready. Use Download PDF to open or save it.';
        // A plain link remains visible even where automatic downloads are blocked.
        // No window.print() or HTML-to-PDF renderer participates in this action.
        if (options.autoDownload !== false) download.click();
        return true;
      } catch (error) {
        if (generation === ownGeneration) {
          reset('PDF unavailable: ' + (error.message || error));
          root.dataset.nativePrintState = 'error';
        }
        return false;
      } finally {
        if (generation === ownGeneration) {
          active = null;
          start.disabled = false;
          cancel.hidden = true;
          root.removeAttribute('aria-busy');
        }
      }
    }
    const controls = {start: generate, cancel: () => {
      reset('PDF request cancelled.'); root.dataset.nativePrintState = 'cancelled';
    }};
    installations.set(root, controls);
    start.addEventListener('click', generate);
    cancel.addEventListener('click', controls.cancel);
    window.addEventListener('keydown', (event) => {
      if ((event.ctrlKey || event.metaKey) && !event.altKey && event.key.toLowerCase() === 'p') {
        event.preventDefault();
        if (!start.disabled) generate();
      }
    });
    window.addEventListener('beforeprint', () => {
      const refusal = document.querySelector('[data-print-volume-notice]');
      if (refusal) refusal.textContent = 'Use Generate PDF on this page for the complete edition in its original TeX layout.';
    });
    for (const event of ['hashchange', 'popstate', 'pagehide']) window.addEventListener(event, controls.cancel);
    root.dataset.nativePrintState = 'idle';
    if (options.auto || new URLSearchParams(location.search).get('print') === '1') queueMicrotask(generate);
    return controls;
  }

  function bootstrap() {
    for (const root of document.querySelectorAll('[data-native-print]')) {
      try {
        const manifest = root.querySelector('script[data-native-print-manifest]');
        need(manifest && manifest.type === 'application/json', 'The native PDF selection is missing.');
        install(root, JSON.parse(manifest.textContent));
      } catch (error) {
        const status = root.querySelector('[data-native-print-status]');
        if (status) status.textContent = 'PDF unavailable: ' + error.message;
        root.dataset.nativePrintState = 'error';
      }
    }
  }

  window.TriptychNativePrint = Object.freeze({install, selection, endpoint, job, serviceTransport, wasmTransport});
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', bootstrap, {once: true});
  else bootstrap();
}());
