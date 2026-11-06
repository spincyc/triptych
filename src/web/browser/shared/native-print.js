/* Request the authored TeX PDF. Browser reflow is never a substitute. */
(function () {
  'use strict';
  const SCHEMA = 'triptych-native-print/v1';
  const installations = new WeakMap();
  const need = (condition, message) => { if (!condition) throw new Error(message); };
  const hex40 = (value) => typeof value === 'string' && /^[0-9a-f]{40}$/.test(value);
  const hex64 = (value) => typeof value === 'string' && /^[0-9a-f]{64}$/.test(value);
  // One portable, lower-case file name per admitted edition, chosen at build time.
  const downloadName = (value) => typeof value === 'string' && /^[a-z0-9][a-z0-9-]{0,190}\.pdf$/.test(value);
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
    need(value.filename == null || downloadName(value.filename), 'The PDF file name is invalid.');
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

  // `base` is the page that carried the selection: this page, or the print
  // page whose selection a print link read in place.
  function resourceURL(value, base) {
    need(typeof value === 'string' && value && !/[\s\\]/u.test(value), 'A TeX compiler resource address is invalid.');
    const url = new URL(value, base || location.href);
    need(url.origin === location.origin && !url.username && !url.password && !url.search && !url.hash,
      'A TeX compiler resource must belong to this site.');
    return url.href;
  }

  async function wasmTransport(chosen, options) {
    need(chosen.wasm && window.TriptychNativeTeX && typeof window.TriptychNativeTeX.generate === 'function',
      'The native TeX compiler could not be loaded. Please reload this page.');
    const generated = await window.TriptychNativeTeX.generate({
      bundleURL: resourceURL(chosen.wasm.bundle, options.base), runtimeURL: resourceURL(chosen.wasm.runtime, options.base),
      bundleSHA256: chosen.wasm.bundle_sha256, bundleBytes: chosen.wasm.bundle_bytes,
      runtimeSHA256: chosen.wasm.runtime_sha256, runtimeBytes: chosen.wasm.runtime_bytes,
      signal: options.signal, onProgress: (value) => {
        const message = typeof value === 'string' ? value : value && value.message;
        if (message && options.onStatus) options.onStatus(message, value && typeof value === 'object' ? value : null);
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

  function fallbackName(id) {
    // Only reached for a manifest without a build-time name: the whole identity
    // is unique, unlike its final segment (".../la", ".../en").
    return id.replace(/^publication:/, '').replace(/[^a-z0-9]+/g, '-').replace(/^-+|-+$/g, '') + '.pdf';
  }

  function mebibytes(value) {
    return (value / (1024 * 1024)).toFixed(1);
  }

  async function produce(chosen, options) {
    const transport = options.transport || (chosen.wasm ? wasmTransport : serviceTransport);
    return transport(chosen, options);
  }

  // A typesetter result names its PDF; accept only an address this page may offer.
  function pdfAddress(result) {
    need(result && typeof result.url === 'string', 'The typesetter returned no PDF.');
    const target = new URL(result.url, location.href);
    need(target.protocol === 'blob:' || target.protocol === 'https:' ||
      target.protocol === 'http:' && ['localhost', '127.0.0.1', '[::1]'].includes(target.hostname),
    'The typesetter returned an invalid PDF address.');
    return target.href;
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
    // Byte counts change many times a second; they belong outside the polite
    // live region, which announces only stage changes.
    let progress = root.querySelector('[data-native-print-progress]');
    if (!progress) {
      progress = document.createElement('p');
      progress.className = 'native-print-progress';
      progress.setAttribute('data-native-print-progress', '');
      status.after(progress);
    }
    const filename = chosen.filename || fallbackName(chosen.id);
    let generation = 0;
    let active = null;
    let currentURL = null;
    let state = 'idle';

    function announce(message) {
      if (status.textContent !== message) status.textContent = message;
    }

    function render(next) {
      state = next;
      root.dataset.nativePrintState = next;
      const busy = next === 'preparing';
      start.disabled = busy;
      cancel.hidden = !busy;
      download.hidden = !currentURL;
      if (!currentURL) download.removeAttribute('href');
      if (!busy) progress.textContent = '';
    }

    // Move focus only when it is still with these controls (or was dropped to
    // the page by disabling a button): a reader who has gone on reading during
    // a build keeps their place.
    function focus(target) {
      const current = document.activeElement;
      if (!current || current === document.body || current === document.documentElement || root.contains(current)) {
        target.focus();
      }
    }

    function discard() {
      if (currentURL && currentURL.startsWith('blob:')) URL.revokeObjectURL(currentURL);
      currentURL = null;
    }

    function report(message, detail) {
      if (detail && detail.stage === 'ready') return;
      if (detail && typeof detail.stage === 'string' && Number.isFinite(detail.loadedBytes) &&
          Number.isFinite(detail.totalBytes) && detail.totalBytes > 0) {
        announce(detail.stage + '… Keep this page visible until it finishes.');
        progress.textContent = mebibytes(detail.loadedBytes) + ' of ' + mebibytes(detail.totalBytes) + ' MiB';
      } else {
        announce(message);
        progress.textContent = '';
      }
    }

    // Abort an in-flight build only. A finished PDF is left alone.
    function stop(message) {
      if (!active) return false;
      generation += 1;
      active.abort();
      active = null;
      render('cancelled');
      announce(message);
      return true;
    }

    async function generate() {
      generation += 1;
      const ownGeneration = generation;
      if (active) active.abort();
      discard();
      const controller = new AbortController();
      active = controller;
      render('preparing');
      announce('Preparing the TeX PDF…');
      focus(cancel);
      try {
        const result = await produce(chosen, {
          ...options, signal: controller.signal,
          onStatus: (message, detail) => { if (generation === ownGeneration) report(message, detail); }
        });
        if (generation !== ownGeneration || controller.signal.aborted) return false;
        const address = pdfAddress(result);
        active = null;
        currentURL = address;
        download.href = currentURL;
        download.download = filename;
        download.setAttribute('aria-label', 'Download PDF — ' + chosen.title);
        render('ready');
        announce('The TeX PDF is ready. Use Download PDF to open or save it.');
        focus(download);
        // A plain link remains visible even where automatic downloads are blocked.
        // No window.print() or HTML-to-PDF renderer participates in this action.
        if (options.autoDownload !== false) download.click();
        return true;
      } catch (error) {
        if (generation === ownGeneration) {
          active = null;
          discard();
          render('error');
          announce('PDF unavailable: ' + (error.message || error));
          focus(start);
        }
        return false;
      }
    }

    const controls = {start: generate, cancel: () => {
      if (stop('PDF request cancelled.')) focus(start);
    }};
    installations.set(root, controls);
    start.addEventListener('click', generate);
    cancel.addEventListener('click', controls.cancel);
    // In-page navigation (table-of-contents links, history within the page)
    // neither cancels a build nor discards a finished PDF. Leaving the page
    // stops an unfinished build; a finished one stays for a back/forward
    // restore, and the browser frees its blob when the document is destroyed.
    window.addEventListener('pagehide', () => {
      stop('PDF generation stopped when you left this page. Use Generate PDF to start again.');
    });
    window.addEventListener('pageshow', (event) => {
      if (event.persisted) render(state === 'preparing' && !active ? 'cancelled' : state);
    });
    render('idle');
    // A URL or installation option is not a request to run the typesetter.
    // Retained ?print=1 links stay readable until the reader invokes Generate PDF.
    // Browser print (Ctrl/Cmd+P) is left to the browser.
    return controls;
  }

  /* ------------------------------------------------------------------------
   * Print links generate in place
   *
   * A link to an edition's print page that carries `?print=1` asks for that
   * edition's PDF. A plain primary click typesets it here, under a small
   * progress popover beside the link, and the reader stays on this page. The
   * print page remains the link's target for a new tab, a modified click or a
   * page without this script. It alone carries the edition's selection, so
   * the click reads the selection from there rather than from a copy here.
   * --------------------------------------------------------------------- */
  const SCRIPT_URL = document.currentScript ? document.currentScript.src : '';
  const POPOVER_API = typeof HTMLElement === 'function' && 'showPopover' in HTMLElement.prototype;
  const EDGE = 8;
  const LINGER = 8000;
  let compiler = null;
  let inline = null;
  let parts = null;
  let placing = 0;

  function printLink(event) {
    if (event.defaultPrevented || event.button !== 0 || event.metaKey || event.ctrlKey ||
        event.shiftKey || event.altKey) return null;
    const link = event.target instanceof Element ? event.target.closest('a[href]') : null;
    // The popover's own "Open print page" means exactly that.
    if (!(link instanceof HTMLAnchorElement) || link.hasAttribute('download') ||
        link.target && link.target !== '_self' || link.closest('[data-native-print-popover]')) return null;
    let url;
    try { url = new URL(link.href, location.href); } catch (_) { return null; }
    if (url.origin !== location.origin || url.searchParams.get('print') !== '1' ||
        !/\/print\/(?:[^/]+\/)*[^/]+\.html$/.test(url.pathname)) return null;
    return {link, url};
  }

  async function linkedSelection(url, signal) {
    const page = new URL(url.href);
    page.search = '';
    page.hash = '';
    const response = await fetch(page.href, {signal});
    need(response.ok && new URL(response.url || page.href).origin === location.origin,
      'The print page for this edition could not be loaded.');
    const parsed = new DOMParser().parseFromString(await response.text(), 'text/html');
    const manifest = parsed.querySelector('[data-native-print] script[data-native-print-manifest]');
    need(manifest && manifest.type === 'application/json', 'The print page carries no PDF selection.');
    let value;
    try { value = JSON.parse(manifest.textContent); } catch (_) { value = null; }
    const chosen = selection(value);
    need(manifest.closest('[data-native-print]').dataset.nativePrint === chosen.id,
      'The PDF controls identify another edition.');
    return {chosen, base: response.url || page.href};
  }

  // Print pages load the compiler themselves; elsewhere it loads on first use.
  function loadCompiler() {
    if (window.TriptychNativeTeX) return Promise.resolve();
    if (!compiler) {
      compiler = new Promise((resolve, reject) => {
        const script = document.createElement('script');
        script.src = new URL('native-tex.js', SCRIPT_URL || location.href).href;
        script.addEventListener('load', () => resolve(), {once: true});
        script.addEventListener('error', () => {
          compiler = null;
          script.remove();
          reject(new Error('The native TeX compiler could not be loaded. Please reload this page.'));
        }, {once: true});
        document.head.appendChild(script);
      });
    }
    return compiler;
  }

  /* Where each stage the compiler reports sits in a whole run. These shares
     are a rough guide for the bar, not a measurement; the bar never moves
     back, so a retry that fetches more fonts keeps its place. A stage this
     table does not know keeps the bar where it is. */
  const STAGES = [
    [/^Checking the original sources/, 'Checking sources', 0, .1],
    [/^Downloading original fonts and packages/, 'Downloading fonts', .1, .35],
    [/^Downloading the typesetter/, 'Downloading typesetter', .35, .45],
    [/^Starting the typesetter/, 'Starting typesetter', .45, .45],
    [/^Downloading original font support/, 'Downloading font support', .45, .5],
    [/^Loading original fonts and sources/, 'Loading sources', .5, .5],
    [/^Downloading the print format/, 'Downloading print format', .5, .6],
    [/^Typesetting with the original TeX layout \(pass (\d+)\)/, 'Typesetting', .6, .9],
    [/^Loading the original fonts selected/, 'Loading fonts', null, null],
    [/^Embedding the original fonts/, 'Embedding fonts', .95, .95],
    [/^Waiting for the typesetter/, 'Waiting for typesetter', null, null],
    [/^Typesetting the original TeX edition/, 'Typesetting', null, null]
  ];

  function stage(message, detail) {
    const text = String(detail && typeof detail.stage === 'string' ? detail.stage : message || '');
    const bytes = detail && Number.isFinite(detail.loadedBytes) && Number.isFinite(detail.totalBytes) &&
      detail.totalBytes > 0 ? Math.min(1, Math.max(0, detail.loadedBytes / detail.totalBytes)) : null;
    const amount = bytes === null ? '' : mebibytes(detail.loadedBytes) + ' of ' + mebibytes(detail.totalBytes) + ' MiB';
    for (const [pattern, label, from, to] of STAGES) {
      const match = pattern.exec(text);
      if (!match) continue;
      if (from === null) return {label, share: null, amount};
      if (match[1]) {
        const pass = Number(match[1]);
        return {label: label + ' · pass ' + pass, share: from + (to - from) * (1 - Math.pow(.6, pass - 1)), amount};
      }
      return {label, share: from + (to - from) * (bytes === null ? 0 : bytes), amount};
    }
    return {label: text.replace(/\s*Keep this page visible until it finishes\.$/, ''), share: null, amount};
  }

  function popoverOpen() {
    return Boolean(parts) && parts.root.dataset.state !== 'closed';
  }

  function popover() {
    if (parts) return parts;
    const make = (tag, name) => {
      const node = document.createElement(tag);
      node.className = 'native-print-popover__' + name;
      return node;
    };
    const root = document.createElement('div');
    root.className = 'native-print-popover';
    root.setAttribute('data-native-print-popover', '');
    root.setAttribute('role', 'group');
    root.dataset.state = 'closed';
    if (POPOVER_API) root.setAttribute('popover', 'manual');
    else root.hidden = true;
    const head = make('div', 'head');
    // Stage changes are announced; byte counts change too often and are not.
    const status = make('p', 'status');
    status.setAttribute('role', 'status');
    const amount = make('span', 'amount');
    const action = make('a', 'action');
    action.hidden = true;
    const close = make('button', 'close');
    close.type = 'button';
    close.textContent = '×';
    const bar = make('div', 'bar');
    bar.setAttribute('role', 'progressbar');
    bar.setAttribute('aria-label', 'PDF generation progress');
    bar.setAttribute('aria-valuemin', '0');
    bar.setAttribute('aria-valuemax', '100');
    const fill = make('span', 'fill');
    bar.appendChild(fill);
    // Hidden tabs throttle the compiler's downloads and checks to a crawl.
    const hint = make('p', 'hint');
    hint.textContent = 'Keep this tab visible until it finishes.';
    head.append(status, amount, action, close);
    root.append(head, bar, hint);
    parts = {root, status, amount, action, close, bar, fill, timer: 0, announce: 0};
    close.addEventListener('click', () => closeInline());
    root.addEventListener('pointerenter', () => clearTimeout(parts.timer));
    root.addEventListener('focusin', () => clearTimeout(parts.timer));
    root.addEventListener('pointerleave', () => { if (!root.contains(document.activeElement)) linger(); });
    root.addEventListener('focusout', (event) => {
      if (!root.contains(event.relatedTarget) && !root.matches(':hover')) linger();
    });
    window.addEventListener('scroll', schedulePlace, {passive: true, capture: true});
    window.addEventListener('resize', schedulePlace, {passive: true});
    return parts;
  }

  // Beside the link, below it where there is room, and always within the
  // viewport, so a reader who scrolls on still sees the bar at the edge.
  function place() {
    if (!popoverOpen() || !inline) return;
    const view = document.documentElement;
    const width = view.clientWidth || window.innerWidth;
    const height = view.clientHeight || window.innerHeight;
    const box = parts.root.getBoundingClientRect();
    const anchor = inline.link.isConnected ? inline.link.getBoundingClientRect() : null;
    let top;
    let left;
    if (anchor && (anchor.width || anchor.height)) {
      top = anchor.bottom + 6;
      if (top + box.height > height - EDGE && anchor.top - 6 - box.height >= EDGE) top = anchor.top - 6 - box.height;
      left = anchor.left;
    } else {
      top = height - box.height - EDGE;
      left = width - box.width - EDGE;
    }
    parts.root.style.top = Math.round(Math.max(EDGE, Math.min(top, height - box.height - EDGE))) + 'px';
    parts.root.style.left = Math.round(Math.max(EDGE, Math.min(left, width - box.width - EDGE))) + 'px';
  }

  function schedulePlace() {
    if (!placing && popoverOpen()) placing = requestAnimationFrame(() => { placing = 0; place(); });
  }

  function showPopover(link) {
    popover();
    if (!parts.root.isConnected) document.body.appendChild(parts.root);
    if (POPOVER_API) {
      if (parts.root.matches(':popover-open')) parts.root.hidePopover();
      // `source` puts the popover next to its link in the focus order where supported.
      try { parts.root.showPopover({source: link}); } catch (_) { parts.root.showPopover(); }
    } else {
      parts.root.hidden = false;
    }
  }

  function hidePopover() {
    if (!parts) return;
    clearTimeout(parts.timer);
    clearTimeout(parts.announce);
    const focused = parts.root.contains(document.activeElement);
    if (POPOVER_API) { if (parts.root.matches(':popover-open')) parts.root.hidePopover(); }
    else parts.root.hidden = true;
    parts.root.dataset.state = 'closed';
    if (focused && inline && inline.link.isConnected) inline.link.focus({preventScroll: true});
  }

  function linger() {
    if (!parts || !inline || inline.state !== 'ready' || parts.root.dataset.state !== 'ready') return;
    clearTimeout(parts.timer);
    parts.timer = setTimeout(() => { if (inline && inline.state === 'ready') hidePopover(); }, LINGER);
  }

  function setShare(job, value) {
    if (value === null) {
      parts.root.dataset.progress = 'indeterminate';
      parts.bar.removeAttribute('aria-valuenow');
      parts.fill.style.removeProperty('width');
      return;
    }
    job.share = Math.max(job.share === null ? 0 : job.share, value);
    parts.root.dataset.progress = 'determinate';
    parts.bar.setAttribute('aria-valuenow', String(Math.round(job.share * 100)));
    parts.fill.style.width = (job.share * 100).toFixed(1) + '%';
  }

  function announce(text) {
    clearTimeout(parts.announce);
    if (parts.status.textContent !== text) parts.status.textContent = text;
  }

  function release(job) {
    if (job && job.address && job.address.startsWith('blob:')) URL.revokeObjectURL(job.address);
    if (job) job.address = null;
  }

  // Close the popover; a build still running is cancelled with it.
  function closeInline() {
    const job = inline;
    if (job && job.state === 'preparing') {
      job.state = 'cancelled';
      job.controller.abort();
    }
    hidePopover();
  }

  async function generateInline(link, url) {
    if (inline && inline.state === 'preparing' && inline.link === link && inline.url.href === url.href) {
      place();
      return;
    }
    if (inline && inline.state === 'preparing') {
      inline.state = 'cancelled';
      inline.controller.abort();
    }
    release(inline);
    const job = {link, url, controller: new AbortController(), state: 'preparing', share: null, address: null};
    const signal = job.controller.signal;
    inline = job;
    hidePopover();
    popover();
    parts.root.dataset.state = 'preparing';
    parts.root.setAttribute('aria-label', 'Generate PDF');
    parts.status.textContent = '';
    parts.amount.textContent = '';
    parts.action.hidden = true;
    parts.action.removeAttribute('href');
    for (const name of ['download', 'aria-label', 'target', 'rel']) parts.action.removeAttribute(name);
    parts.close.setAttribute('aria-label', 'Cancel PDF generation');
    setShare(job, null);
    showPopover(link);
    place();
    // A live region shown a moment ago may not be heard yet; speak after it is.
    parts.announce = setTimeout(() => {
      if (inline === job && job.state === 'preparing' && !parts.status.textContent) parts.status.textContent = 'Preparing PDF…';
    }, 100);
    const current = () => inline === job && job.state === 'preparing' && !signal.aborted;
    try {
      const {chosen, base} = await linkedSelection(url, signal);
      if (!current()) return;
      parts.root.setAttribute('aria-label', 'Generate PDF — ' + chosen.title);
      if (chosen.wasm) await loadCompiler();
      if (!current()) return;
      const result = await produce(chosen, {signal, base, onStatus: (message, detail) => {
        if (!current() || detail && detail.stage === 'ready') return;
        const next = stage(message, detail);
        announce(next.label);
        parts.amount.textContent = next.amount;
        if (next.share !== null) setShare(job, next.share);
        place();
      }});
      if (!current()) {
        if (result && typeof result.url === 'string' && result.url.startsWith('blob:')) URL.revokeObjectURL(result.url);
        return;
      }
      job.address = pdfAddress(result);
      job.state = 'ready';
      parts.root.dataset.state = 'ready';
      announce('PDF ready');
      parts.amount.textContent = '';
      setShare(job, 1);
      parts.action.href = job.address;
      parts.action.download = chosen.filename || fallbackName(chosen.id);
      parts.action.textContent = 'Save PDF';
      parts.action.setAttribute('aria-label', 'Save PDF — ' + chosen.title);
      // A service PDF is another origin, where `download` is ignored: open it
      // beside this page rather than in place of it.
      if (!job.address.startsWith('blob:')) {
        parts.action.target = '_blank';
        parts.action.rel = 'noopener';
      }
      parts.action.hidden = false;
      parts.close.setAttribute('aria-label', 'Close');
      place();
      // The visible link stays for a browser that blocks the automatic download.
      parts.action.click();
      if (!parts.root.matches(':hover') && !parts.root.contains(document.activeElement)) linger();
    } catch (error) {
      if (!current()) return;
      job.state = 'error';
      parts.root.dataset.state = 'error';
      announce('PDF unavailable: ' + (error && error.message || error));
      parts.amount.textContent = '';
      // The print page offers the same request, and any earlier printed edition.
      parts.action.href = url.href;
      parts.action.textContent = 'Open print page';
      parts.action.hidden = false;
      parts.close.setAttribute('aria-label', 'Close');
      place();
    }
  }

  function installLinks() {
    document.addEventListener('click', (event) => {
      const found = printLink(event);
      if (!found) return;
      event.preventDefault();
      generateInline(found.link, found.url);
    });
    document.addEventListener('keydown', (event) => {
      if (event.key !== 'Escape' || !inline || !popoverOpen()) return;
      const focused = document.activeElement;
      if (focused === inline.link || parts.root.contains(focused)) {
        event.preventDefault();
        closeInline();
      }
    });
    // Leaving the page stops an unfinished build, as on the print page.
    window.addEventListener('pagehide', () => { if (inline && inline.state === 'preparing') closeInline(); });
  }

  function bootstrap() {
    installLinks();
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

  window.TriptychNativePrint = Object.freeze({install, selection, endpoint, job, serviceTransport, wasmTransport, stage});
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', bootstrap, {once: true});
  else bootstrap();
}());
