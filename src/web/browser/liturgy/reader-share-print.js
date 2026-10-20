/* Shared prayer presentation, Share and Print actions for both liturgy entrances. */
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
      const peerLabel = state.comparison.dimension === 'bible-edition'
        ? peer && peer.bible && peer.bible.id
        : state.comparison.dimension === 'translation-witness'
        ? peer && peer.languages && peer.languages.translationWitness
        : state.comparison.dimension === 'reading-alternative'
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
    if (state.textDisplay === 'latin-and-selected') parts.push('Latin alongside translated prayers');
    if (state.scriptureCompanion) parts.push('Latin Bible companion: ' + state.scriptureCompanion.id);
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

  function textDisplayUrl(location, value, semanticLocation) {
    if (!['selected', 'latin-and-selected'].includes(value)) throw new Error('Invalid prayer presentation');
    const url = new URL(location.href);
    const params = new URLSearchParams(url.hash.slice(1));
    params.set('text-display', value);
    if (semanticLocation && semanticLocation.kind === 'event') params.set('location', semanticLocation.id);
    else if (semanticLocation) params.delete('location');
    url.hash = params.toString();
    return url.href;
  }

  function scriptureCompanionUrl(location, id, semanticLocation) {
    if (id !== null && id !== 'clementine-vulgate') throw new Error('Invalid Latin Bible companion');
    const url = new URL(location.href);
    const params = new URLSearchParams(url.hash.slice(1));
    if (id) params.set('scripture-companion', id);
    else params.delete('scripture-companion');
    if (semanticLocation && semanticLocation.kind === 'event') params.set('location', semanticLocation.id);
    else if (semanticLocation) params.delete('location');
    url.hash = params.toString();
    return url.href;
  }

  // During printing, keep a source direction or heading with its next short
  // Ordinary event, and keep a Study note with the final short text of its
  // own Proper. Long readings remain free to continue across pages.
  function installPrintComposition(doc, win) {
    if (typeof win.addEventListener !== 'function') return function () {};
    let ties = [];
    let keptSides = [];
    const reading = function () { return doc.getElementById('reader-document'); };
    function clear() {
      const current = reading();
      ties.forEach(function (tie) {
        // A reader rerender may have detached the old frame while print was open.
        if (!tie.isConnected || !current || !current.contains(tie)) return;
        while (tie.firstChild) tie.parentNode.insertBefore(tie.firstChild, tie);
        tie.remove();
      });
      ties = [];
      keptSides.forEach(function (side) {
        if (side.isConnected && current && current.contains(side)) {
          side.classList.remove('print-keep-short-body');
        }
      });
      keptSides = [];
    }
    function wrap(parent, first, last, className) {
      const tie = doc.createElement('div');
      tie.className = className;
      parent.insertBefore(tie, first);
      let node = first;
      while (node) {
        const next = node.nextElementSibling;
        tie.appendChild(node);
        if (node === last) break;
        node = next;
      }
      ties.push(tie);
    }
    function prepare() {
      const current = reading();
      if (!current) return;
      // Repeated beforeprint is harmless; a new render replaces stale ties.
      if ((ties.length || keptSides.length) &&
          ties.every(function (tie) { return tie.isConnected && current.contains(tie); }) &&
          keptSides.every(function (side) { return side.isConnected && current.contains(side); })) return;
      clear();
      const shell = current.closest('.reader-instrument');
      if (!shell) return;
      // A short paired text and its own source qualifications travel as one
      // print unit. Long stanzas and readings remain free to paginate.
      current.querySelectorAll('.text-pair > .text-side').forEach(function (side) {
        if (side.closest('.scripture-pair')) return;
        const body = side.querySelector(':scope > .composed,:scope > .text-side-body');
        if (!body || !side.querySelector(':scope > .composed-note')) return;
        const bodyHeight = body.getBoundingClientRect().height;
        const sideHeight = side.getBoundingClientRect().height;
        if (!bodyHeight || bodyHeight > 240 || sideHeight > 560) return;
        side.classList.add('print-keep-short-body');
        keptSides.push(side);
      });
      if (shell.dataset.readerMode === 'study') {
        current.querySelectorAll('.proper:has(> .study-event)').forEach(function (proper) {
          const note = proper.lastElementChild;
          const tail = note && note.previousElementSibling;
          if (!note || !note.classList.contains('study-event') ||
              !tail || !tail.matches('.citation,.composed')) return;
          const tailHeight = tail.getBoundingClientRect().height;
          const noteHeight = note.getBoundingClientRect().height;
          if (!tailHeight || tailHeight > 240 || tailHeight + noteHeight > 560) return;
          wrap(proper, tail, note, 'study-print-tie');
        });
      } else if (shell.dataset.readerMode === 'missal') {
        current.querySelectorAll('.ordinary-frame').forEach(function (frame) {
          const children = Array.from(frame.children);
          for (let i = 0; i < children.length;) {
            const first = children[i];
            if (!first.classList.contains('ordinary-element') ||
                !first.matches('.is-heading,.is-rubric')) { i += 1; continue; }
            let j = i;
            while (j < children.length && children[j].classList.contains('ordinary-element') &&
                   children[j].matches('.is-heading,.is-rubric')) j += 1;
            const body = children[j];
            if (!body || !body.classList.contains('ordinary-element') ||
                !body.matches('.is-prayer,.is-dialogue,.is-form')) { i = j; continue; }
            const bodyHeight = body.getBoundingClientRect().height;
            const leadHeight = children.slice(i, j).reduce(function (height, node) {
              return height + node.getBoundingClientRect().height;
            }, 0);
            if (bodyHeight && bodyHeight <= 320 && leadHeight + bodyHeight <= 560) {
              wrap(frame, first, body, 'ordinary-print-tie');
            }
            i = j + 1;
          }
        });
      }
    }
    win.addEventListener('beforeprint', prepare);
    win.addEventListener('afterprint', clear);
    return function () {
      win.removeEventListener('beforeprint', prepare);
      win.removeEventListener('afterprint', clear);
      clear();
    };
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
    const presentation = doc.createElement('label');
    presentation.className = 'reader-text-display-control';
    const paired = doc.createElement('input');
    paired.type = 'checkbox';
    paired.dataset.readerTextDisplay = '';
    paired.setAttribute('aria-describedby', 'reader-text-display-note');
    presentation.append(paired, doc.createTextNode('Show Latin alongside translated prayers'));
    const scope = doc.createElement('p');
    scope.id = 'reader-text-display-note';
    scope.className = 'surface-note';
    scope.textContent = 'Pairs held prayer and Missal bodies. Bible pairing is controlled separately.';
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
    section.append(presentation, scope);
    const scriptureControl = doc.createElement('label');
    scriptureControl.className = 'reader-text-display-control';
    const scripturePaired = doc.createElement('input');
    scripturePaired.type = 'checkbox';
    scripturePaired.dataset.readerScriptureCompanion = '';
    scripturePaired.setAttribute('aria-describedby', 'reader-scripture-companion-note');
    scriptureControl.append(scripturePaired, doc.createTextNode('Show Latin alongside the selected Bible'));
    const scriptureNote = doc.createElement('p');
    scriptureNote.id = 'reader-scripture-companion-note';
    scriptureNote.className = 'surface-note';
    scriptureNote.textContent = 'Companion: Clementine Vulgate (Latin), Vulgate numbering, Gallican psalter. Each edition keeps its own numbering and explicit gaps. Bible text does not establish the Missal’s wording.';
    section.append(scriptureControl, scriptureNote);

    function currentState() {
      const debug = entrance === 'day' ? win.dayReaderDebug : win.propersReaderDebug;
      const reading = doc.getElementById('reader-document');
      return debug && debug.ready && debug.state &&
        reading && reading.getAttribute('aria-busy') === 'false' ? debug.state : null;
    }

    let presentationPending = false;
    const context = doc.createElement('p');
    context.className = 'reader-text-display-context';
    context.textContent = 'Latin alongside translated prayers · Scripture uses the selected Bible edition.';
    context.hidden = true;
    const reading = doc.getElementById('reader-document');
    if (reading) reading.before(context);
    function syncPresentation() {
      const state = currentState();
      paired.disabled = !state;
      paired.checked = Boolean(state && state.textDisplay === 'latin-and-selected');
      scripturePaired.disabled = !state;
      scripturePaired.checked = Boolean(state && state.scriptureCompanion);
      context.textContent = [paired.checked && 'Latin alongside translated prayers',
        scripturePaired.checked && 'Latin Bible companion: Clementine Vulgate (Latin) · Vulgate numbering · Gallican psalter · public domain · Bible text, not the Missal’s wording'].filter(Boolean).join(' · ');
      context.hidden = !paired.checked && !scripturePaired.checked;
      if (state && presentationPending) {
        presentationPending = false;
        const invoker = shell.querySelector('[data-reader-action="mode"]');
        if (invoker) invoker.focus({ preventScroll: true });
      }
    }
    paired.addEventListener('change', function () {
      const state = currentState();
      if (!state) { syncPresentation(); return; }
      const capture = win.TriptychReaderTextSize && win.TriptychReaderTextSize.captureLocation;
      const location = capture && reading ? capture(win, reading) : null;
      if (win.history) win.history.replaceState(win.history.state, '',
        textDisplayUrl(win.location, state.textDisplay || 'selected', location));
      presentationPending = true;
      win.location.href = textDisplayUrl(win.location,
        paired.checked ? 'latin-and-selected' : 'selected', location);
    });

    scripturePaired.addEventListener('change', function () {
      const state = currentState();
      if (!state) { syncPresentation(); return; }
      const capture = win.TriptychReaderTextSize && win.TriptychReaderTextSize.captureLocation;
      const location = capture && reading ? capture(win, reading) : null;
      if (win.history) win.history.replaceState(win.history.state, '',
        scriptureCompanionUrl(win.location, state.scriptureCompanion && state.scriptureCompanion.id || null, location));
      presentationPending = true;
      win.location.href = scriptureCompanionUrl(win.location,
        scripturePaired.checked ? 'clementine-vulgate' : null, location);
    });

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
    const displayObserver = new win.MutationObserver(function () {
      if (typeof win.requestAnimationFrame === 'function') win.requestAnimationFrame(syncPresentation);
      else syncPresentation();
    });
    if (reading) displayObserver.observe(reading, { attributes: true, attributeFilter: ['aria-busy'] });
    syncPresentation();
    const disconnectComposition = installPrintComposition(doc, win);
    return { section: section, disconnect: function () {
      observer.disconnect(); displayObserver.disconnect(); disconnectComposition();
    } };
  }

  return Object.freeze({ canonicalUrl: canonicalUrl, shareTitle: shareTitle,
    copyUrl: copyUrl, share: share, textDisplayUrl: textDisplayUrl, scriptureCompanionUrl: scriptureCompanionUrl, install: install });
}));
