/* Shared, text-free Share and Print actions for the Day and Propers readers. */
'use strict';

(function (root, factory) {
  const api = factory(root);
  if (typeof module === 'object' && module && module.exports) module.exports = api;
  else {
    root.TriptychReaderSharePrint = api;
    if (root.document.readyState === 'loading') {
      root.document.addEventListener('DOMContentLoaded', function () { api.install(); }, { once: true });
    } else api.install();
  }
}(typeof globalThis !== 'undefined' ? globalThis : this, function (root) {
  function canonicalUrl(entrance, location, contract) {
    if (entrance !== 'day' && entrance !== 'propers') {
      throw new Error('Share requires a Day or Propers entrance');
    }
    if (!contract || typeof contract.canonicalRoute !== 'function') {
      throw new Error('Share requires the reader URL contract');
    }
    // The controllers have already serialized the validated semantic state
    // into this URL. Only the retained route basename can still differ.
    const url = new URL(location.href);
    url.pathname = contract.canonicalRoute(entrance, url.pathname);
    return url.href;
  }

  function shareTitle(entrance, shell, state) {
    const heading = shell.querySelector('.reader-identity .celebration-title');
    const parts = [entrance === 'day' ? 'Day' : 'Propers'];
    if (heading && heading.textContent.trim()) parts.push(heading.textContent.trim());
    if (entrance === 'day' && state.civilDate) parts.push(state.civilDate);
    if (state.edition && state.edition.id) parts.push(state.edition.id);
    if (state.requestedMode === 'compare' && state.comparison) {
      const peer = state.comparison.sides && state.comparison.sides[1];
      const peerEdition = peer && peer.edition && peer.edition.id;
      const peerLanguage = peer && peer.languages && peer.languages.orations;
      const peerLabel = state.comparison.dimension === 'reading-alternative'
        ? peer && peer.alternative && 'Option ' + peer.alternative.id.split('/').pop()
        : state.comparison.dimension === 'lectionary-cycle'
        ? peer && peer.cycle && 'Cycle ' + peer.cycle
        : state.comparison.dimension === 'oration-language'
          ? peerLanguage : peerEdition || peerLanguage;
      parts.push('Compare ' + state.comparison.dimension +
        (peerLabel ? ' with ' + peerLabel : ''));
      if (entrance === 'day' && state.comparison.anchor &&
          state.comparison.anchor.territorialContext) {
        parts.push(state.comparison.anchor.territorialContext);
      }
    } else if (state.requestedMode && state.requestedMode !== 'read') {
      parts.push(state.requestedMode);
    }
    return parts.join(' · ') + ' — Triptych';
  }

  async function copyUrl(url, navigator, document, focusTarget) {
    if (navigator.clipboard && typeof navigator.clipboard.writeText === 'function') {
      try {
        await navigator.clipboard.writeText(url);
        return true;
      } catch (_error) { /* Try the local copy command below. */ }
    }
    if (typeof document.execCommand !== 'function') return false;
    const field = document.createElement('textarea');
    field.value = url;
    field.readOnly = true;
    field.setAttribute('aria-hidden', 'true');
    field.style.position = 'fixed';
    field.style.opacity = '0';
    (focusTarget.parentElement || document.body).appendChild(field);
    let copied = false;
    try {
      field.select();
      copied = document.execCommand('copy') === true;
    } catch (_error) { /* A denied local copy is reported to the reader. */ }
    finally {
      field.remove();
      if (focusTarget.isConnected) focusTarget.focus({ preventScroll: true });
    }
    return copied;
  }

  async function share(options) {
    const held = options || {};
    const navigator = held.navigator;
    if (typeof navigator.share === 'function') {
      try {
        await navigator.share({ title: held.title, url: held.url });
        return 'Shared this reader link.';
      } catch (error) {
        // A cancelled native sheet is a decision, not permission to copy.
        if (error && error.name === 'AbortError') return 'Sharing cancelled.';
      }
    }
    return await copyUrl(held.url, navigator, held.document, held.focusTarget)
      ? 'Reader link copied to clipboard.'
      : 'Could not share or copy this reader link.';
  }

  function install(options) {
    const held = options || {};
    const doc = held.document || root.document;
    const win = held.window || root;
    const shell = doc.querySelector('[data-reader-shell]');
    const body = shell && shell.querySelector('[data-reader-details]');
    const entrance = shell && shell.dataset.entrance;
    if (!body || (entrance !== 'day' && entrance !== 'propers')) return null;
    if (body.querySelector('[data-reader-share-print]')) return null;

    const section = doc.createElement('section');
    section.className = 'reader-share-print';
    section.dataset.readerSharePrint = '';
    const title = doc.createElement('h3');
    title.textContent = 'Share & print';
    section.appendChild(title);
    const controls = doc.createElement('div');
    controls.className = 'reader-share-print-controls';
    const shareButton = doc.createElement('button');
    shareButton.type = 'button';
    shareButton.textContent = 'Share link';
    const printButton = doc.createElement('button');
    printButton.type = 'button';
    printButton.textContent = 'Print';
    controls.append(shareButton, printButton);
    section.appendChild(controls);
    const status = doc.createElement('p');
    status.className = 'reader-share-print-status';
    status.setAttribute('role', 'status');
    status.setAttribute('aria-live', 'polite');
    status.setAttribute('aria-atomic', 'true');
    section.appendChild(status);

    function currentState() {
      const debug = entrance === 'day' ? win.dayReaderDebug : win.propersReaderDebug;
      const reading = doc.getElementById('reader-document');
      return debug && debug.ready && debug.state &&
        reading && reading.getAttribute('aria-busy') === 'false' ? debug.state : null;
    }

    shareButton.addEventListener('click', async function () {
      const state = currentState();
      if (!state) {
        status.textContent = 'Wait for a valid reader selection before sharing.';
        return;
      }
      const url = canonicalUrl(entrance, win.location, win.LiturgyReaderState);
      status.textContent = await share({
        title: shareTitle(entrance, shell, state), url: url,
        navigator: win.navigator, document: doc, focusTarget: shareButton
      });
    });
    printButton.addEventListener('click', function () {
      if (!currentState()) {
        status.textContent = 'Wait for a valid reader selection before printing.';
        return;
      }
      try {
        win.print();
        status.textContent = 'Print dialog opened.';
      } catch (_error) {
        status.textContent = 'Could not open the print dialog.';
      }
    });

    function attach() {
      if (body.firstChild !== section) body.insertBefore(section, body.firstChild);
    }
    attach();
    // Both controllers replace Details contents on rerender and when opening
    // Compare. Keep the controls at the top without changing either owner.
    const observer = new win.MutationObserver(attach);
    observer.observe(body, { childList: true });
    return { section: section, disconnect: function () { observer.disconnect(); } };
  }

  return Object.freeze({ canonicalUrl: canonicalUrl, shareTitle: shareTitle,
    copyUrl: copyUrl, share: share, install: install });
}));
