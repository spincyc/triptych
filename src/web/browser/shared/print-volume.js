/* Load and verify every canonical period before printing a complete volume. */
(function () {
  'use strict';
  const normalize = (value) => value.replace(/\s+/gu, ' ').trim();
  const digest = async (value) => {
    if (!window.crypto || !window.crypto.subtle) throw new Error('Text verification is unavailable.');
    const bytes = await window.crypto.subtle.digest('SHA-256', new TextEncoder().encode(value));
    return Array.from(new Uint8Array(bytes), (byte) => byte.toString(16).padStart(2, '0')).join('');
  };

  for (const root of document.querySelectorAll('[data-print-volume]')) {
    const volume = root.dataset.printVolume;
    const sourceDigest = root.dataset.printVolumeDigest;
    const start = root.querySelector('[data-print-volume-start]');
    const cancel = root.querySelector('[data-print-volume-cancel]');
    const status = root.querySelector('[data-print-volume-status]');
    const destination = root.querySelector('[data-print-volume-periods]');
    const links = Array.from(root.querySelectorAll('a[data-print-volume-part]'));
    let generation = 0;
    let controller = null;
    let prepared = false;
    let preparedAddress = null;
    let texts = [];

    function invalidate(message) {
      generation += 1;
      if (controller) controller.abort();
      controller = null;
      prepared = false;
      preparedAddress = null;
      texts = [];
      root.dataset.printVolumeReady = 'false';
      destination.replaceChildren();
      start.disabled = false;
      cancel.hidden = true;
      status.textContent = message || '';
      root.setAttribute('aria-busy', 'false');
    }

    function manifest() {
      if (!volume || !/^[a-f0-9]{64}$/.test(sourceDigest || '') || !links.length) {
        throw new Error('The complete section list is missing.');
      }
      const base = new URL(window.location.href);
      const directory = base.pathname.replace(/\.html$/, '/');
      const keys = new Set();
      const ids = new Set();
      let previous = 0;
      return links.map((link) => {
        const key = link.dataset.printVolumePart;
        const url = new URL(link.getAttribute('href'), base);
        const readings = (link.dataset.readingIds || '').split(' ').filter(Boolean);
        const verses = Number(link.dataset.verseCount);
        if (!/^[a-z0-9]+(?:-[a-z0-9]+)*$/.test(key || '') || keys.has(key) ||
            url.origin !== base.origin || url.pathname !== directory + 'period-' + key + '.html' ||
            url.search || url.hash || !readings.length || !Number.isSafeInteger(verses) || verses < 0 ||
            !/^[a-f0-9]{64}$/.test(link.dataset.contentSha256 || '')) {
          throw new Error('The complete section list is inconsistent.');
        }
        keys.add(key);
        for (const id of readings) {
          const number = Number(id);
          if (!/^[1-9][0-9]*$/.test(id) || ids.has(id) || number <= previous) {
            throw new Error('The reading order is inconsistent.');
          }
          previous = number;
          ids.add(id);
        }
        return {key, url: url.href, readings, verses, sha256: link.dataset.contentSha256};
      });
    }

    function validatePart(part, expected) {
      if (part.tagName !== 'SECTION' || part.dataset.volumeId !== volume ||
          part.dataset.volumeDigest !== sourceDigest || part.dataset.volumePeriod !== expected.key) {
        throw new Error('A section does not belong to this volume.');
      }
      // Text hashes alone cannot establish visibility: hidden/style/classes or
      // closed disclosures can preserve every character while omitting print.
      // Accept only the exact vocabulary emitted by _period_html. This same
      // check runs again from ready() immediately before native browser print.
      for (const node of [part, ...part.querySelectorAll('*')]) {
        let attributes;
        let classes = null;
        let required = null;
        if (node === part) {
          attributes = ['data-volume-id', 'data-volume-period', 'data-volume-digest'];
        } else if (node.tagName === 'SECTION') {
          attributes = ['id'];
          required = 'id';
        } else if (['H2', 'H3', 'H4', 'STRONG'].includes(node.tagName)) {
          attributes = [];
        } else if (node.tagName === 'P') {
          attributes = ['class'];
          classes = ['scripture-reference', 'bible-paragraph'];
        } else if (node.tagName === 'ASIDE') {
          attributes = ['class'];
          classes = ['reading-refusal'];
          required = 'class';
        } else if (node.tagName === 'SPAN' || node.tagName === 'SUP') {
          attributes = ['class'];
          classes = [node.tagName === 'SPAN' ? 'verse' : 'verse-number'];
          required = 'class';
        } else {
          throw new Error('A section contains unexpected markup.');
        }
        if (Array.from(node.attributes).some((attribute) => !attributes.includes(attribute.name)) ||
            (required && !node.hasAttribute(required)) ||
            (classes && node.hasAttribute('class') && !classes.includes(node.getAttribute('class')))) {
          throw new Error('A section contains unexpected markup.');
        }
      }
      const ids = Array.from(part.querySelectorAll('[id]'), (node) => node.id);
      if (JSON.stringify(ids) !== JSON.stringify(expected.readings.map((id) => 'reading-' + id)) ||
          part.querySelectorAll('.verse-number').length !== expected.verses) {
        throw new Error('A section is incomplete or out of order.');
      }
    }

    function ready() {
      try {
        if (!prepared || !root.isConnected || preparedAddress !== window.location.href || controller) return false;
        const expected = manifest();
        const parts = Array.from(destination.children);
        if (parts.length !== expected.length || texts.length !== expected.length) return false;
        parts.forEach((part, index) => {
          validatePart(part, expected[index]);
          if (normalize(part.textContent) !== texts[index]) throw new Error('The prepared text changed.');
        });
        return true;
      } catch (_) {
        return false;
      }
    }

    start.hidden = false;
    root.dataset.printVolumeReady = 'false';
    cancel.addEventListener('click', () => invalidate('Preparation cancelled. No partial volume will print.'));
    for (const event of ['hashchange', 'popstate', 'pagehide']) {
      window.addEventListener(event, () => invalidate('The page changed. Prepare the complete volume again.'));
    }
    window.addEventListener('beforeprint', () => {
      const complete = ready();
      root.dataset.printVolumeReady = String(complete);
      if (!complete) status.textContent = 'Use Print complete volume to load and verify every section first.';
    });

    start.addEventListener('click', async () => {
      invalidate();
      const selected = generation;
      const address = window.location.href;
      const active = new AbortController();
      controller = active;
      start.disabled = true;
      cancel.hidden = false;
      root.setAttribute('aria-busy', 'true');
      const unchanged = () => {
        if (generation !== selected || address !== window.location.href || active.signal.aborted) {
          throw new Error('Preparation was cancelled or the page changed.');
        }
      };
      try {
        const expected = manifest();
        const verified = [];
        for (const [index, item] of expected.entries()) {
          unchanged();
          status.textContent = 'Loading section ' + (index + 1) + ' of ' + expected.length + '…';
          const response = await fetch(item.url, {signal: active.signal, credentials: 'same-origin', cache: 'no-store'});
          unchanged();
          if (!response.ok || (response.url && new URL(response.url).href !== item.url)) {
            throw new Error('A complete section could not be loaded.');
          }
          const source = new DOMParser().parseFromString(await response.text(), 'text/html');
          unchanged();
          const parts = source.querySelectorAll('[data-volume-period]');
          if (parts.length !== 1) throw new Error('A section response is incomplete or ambiguous.');
          const part = parts[0];
          validatePart(part, item);
          const text = normalize(part.textContent);
          if (await digest(text) !== item.sha256) throw new Error('A section’s text failed verification.');
          unchanged();
          destination.appendChild(document.importNode(part, true));
          verified.push(text);
        }
        if (document.fonts && document.fonts.ready) await document.fonts.ready;
        unchanged();
        texts = verified;
        preparedAddress = address;
        controller = null;
        prepared = true;
        if (!ready()) throw new Error('The complete volume could not be verified.');
        root.dataset.printVolumeReady = 'true';
        root.setAttribute('aria-busy', 'false');
        status.textContent = 'The complete volume is ready.';
        cancel.hidden = true;
        window.print();
      } catch (error) {
        if (generation === selected) invalidate('Print unavailable: ' + (error.message || error));
      } finally {
        if (generation === selected) start.disabled = false;
      }
    });
    if (new URLSearchParams(window.location.search).get('print') === '1') {
      queueMicrotask(() => start.click());
    }
  }
}());
