/* Shared screen text preference for the Day and Propers readers. */
'use strict';

(function (root, factory) {
  const api = factory(root);
  if (typeof module === 'object' && module && module.exports) module.exports = api;
  else {
    root.TriptychReaderTextSize = api;
    if (root.document.readyState === 'loading') {
      root.document.addEventListener('DOMContentLoaded', function () { api.install(); }, { once: true });
    } else api.install();
  }
}(typeof globalThis !== 'undefined' ? globalThis : this, function (root) {
  // Keep display size separate from the semantic preferences replaced by each
  // controller. It never changes the date, formulary, mode, or shared URL.
  const PREFERENCE_KEY = 'triptych:liturgy:text-size:v1';
  const SIZES = Object.freeze([100, 125, 150, 175, 200]);

  function validSize(value) {
    if (typeof value !== 'number' && typeof value !== 'string') return null;
    return SIZES.find(function (size) { return String(size) === String(value); }) || null;
  }

  function readPreference(window) {
    try { return validSize(window.localStorage.getItem(PREFERENCE_KEY)) || 100; }
    catch (_error) { return 100; }
  }

  function writePreference(window, size) {
    const valid = validSize(size);
    if (!valid) return false;
    try { window.localStorage.setItem(PREFERENCE_KEY, String(valid)); return true; }
    catch (_error) { return false; }
  }

  function captureLocation(window, reading) {
    if (window.scrollY <= 8) return { kind: 'top' };
    const document = reading.ownerDocument;
    const height = Math.max(document.documentElement.scrollHeight, document.body.scrollHeight);
    if (window.scrollY + window.innerHeight >= height - 8) return { kind: 'end' };
    const line = Math.max(80, Math.min(window.innerHeight * 0.38, 280));
    const candidates = Array.from(reading.querySelectorAll('[data-semantic-location]'));
    let target = candidates[0];
    for (const candidate of candidates) {
      if (candidate.getBoundingClientRect().top <= line) target = candidate;
      else break;
    }
    if (!target) return { kind: 'top' };
    const box = target.getBoundingClientRect();
    return { kind: 'event', id: target.dataset.semanticLocation,
      fraction: Math.max(0, Math.min(1, (line - box.top) / Math.max(1, box.height))) };
  }

  function restoreLocation(window, reading, location) {
    if (!location) return;
    if (location.kind === 'top') window.scrollTo({ top: 0, behavior: 'instant' });
    else if (location.kind === 'end') {
      window.scrollTo({ top: reading.ownerDocument.documentElement.scrollHeight, behavior: 'instant' });
    } else {
      const target = Array.from(reading.querySelectorAll('[data-semantic-location]'))
        .find(function (node) { return node.dataset.semanticLocation === location.id; });
      if (!target) return;
      const box = target.getBoundingClientRect();
      const line = Math.max(80, Math.min(window.innerHeight * 0.38, 280));
      window.scrollTo({ top: window.scrollY + box.top + location.fraction * box.height - line,
        behavior: 'instant' });
    }
  }

  function install(options) {
    const held = options || {};
    const doc = held.document || root.document;
    const win = held.window || root;
    const shell = doc.querySelector('[data-reader-shell]');
    const surface = shell && shell.querySelector('[data-reader-surface="mode"]');
    const reading = doc.getElementById('reader-document');
    if (!surface || !reading || surface.querySelector('[data-reader-text-size]')) return null;

    const section = doc.createElement('section');
    section.className = 'surface-body reader-text-size';
    section.dataset.readerTextSize = '';
    const label = doc.createElement('label');
    label.htmlFor = 'reader-text-size';
    label.textContent = 'Text size';
    const select = doc.createElement('select');
    select.id = 'reader-text-size';
    select.setAttribute('aria-describedby', 'reader-text-size-note');
    SIZES.forEach(function (size) {
      const option = doc.createElement('option');
      option.value = String(size);
      option.textContent = size + '%' + (size === 100 ? ' · Default' : '');
      select.appendChild(option);
    });
    const note = doc.createElement('p');
    note.id = 'reader-text-size-note';
    note.className = 'surface-note';
    note.textContent = 'Enlarge screen text up to 200%.';
    const status = doc.createElement('p');
    status.className = 'reader-text-size-status';
    status.setAttribute('role', 'status');
    status.setAttribute('aria-live', 'polite');
    status.setAttribute('aria-atomic', 'true');
    section.append(label, select, note, status);
    const secondary = surface.querySelector('[data-reader-secondary-actions]');
    surface.insertBefore(section, secondary);

    let size = readPreference(win);
    let location = null;
    let pending = null;
    let wasOpen = surface.open;
    function syncOpen() {
      if (surface.open && !wasOpen) location = null;
      wasOpen = surface.open;
    }
    // Observe the actual dialog state; beforetoggle is unavailable in some
    // engines. A new visit must never reuse a prior visit's held location.
    const observer = new win.MutationObserver(syncOpen);
    observer.observe(surface, { attributes: true, attributeFilter: ['open'] });
    function apply(value) {
      size = value;
      select.value = String(size);
      doc.documentElement.dataset.readerTextSize = String(size);
      doc.documentElement.style.setProperty('--reader-text-size', size + '%');
    }
    function restoreAfterLayout() {
      if (pending !== null) win.cancelAnimationFrame(pending);
      pending = win.requestAnimationFrame(function () {
        pending = null;
        restoreLocation(win, reading, location);
      });
    }
    apply(size);
    select.addEventListener('change', function () {
      syncOpen();
      const next = validSize(select.value);
      if (!next) { select.value = String(size); return; }
      location = captureLocation(win, reading);
      apply(next);
      const remembered = writePreference(win, next);
      status.textContent = 'Text size ' + next + '%.' +
        (remembered ? '' : ' This setting lasts for this visit.');
      // The selected control keeps focus. Only the document's semantic place
      // moves to account for the larger line boxes.
      restoreAfterLayout();
    });
    surface.addEventListener('close', function () {
      // The shell restores its opening scroll pixels synchronously. A size
      // change has changed those pixels, so restore the held semantic place
      // once that close has completed. Rerendered text keeps the root scale.
      if (location) restoreAfterLayout();
    });
    return Object.freeze({ section: section, select: select });
  }

  return Object.freeze({ SIZES: SIZES, PREFERENCE_KEY: PREFERENCE_KEY,
    validSize: validSize, readPreference: readPreference, writePreference: writePreference,
    install: install });
}));
