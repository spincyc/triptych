/* Reusable persistent reader shell. It owns interaction, never liturgy. */
'use strict';

(function (root) {
  function focusable(surface) {
    return surface.querySelector(
      '[data-reader-close], button:not([disabled]), input:not([disabled]), ' +
      'select:not([disabled]), textarea:not([disabled]), a[href], [tabindex]:not([tabindex="-1"])'
    );
  }

  function create(options) {
    const held = options || {};
    const shell = held.root;
    const reading = held.reading;
    if (!shell || !reading) throw new Error('reader shell needs a root and reading document');

    const actions = new Map();
    shell.querySelectorAll('[data-reader-action]').forEach(function (button) {
      actions.set(button.dataset.readerAction, button);
    });
    const surfaces = new Map();
    shell.querySelectorAll('[data-reader-surface]').forEach(function (surface) {
      surfaces.set(surface.dataset.readerSurface, surface);
    });

    let openName = null;
    let invoker = null;
    let preservedY = 0;
    let preservedLocation = null;
    let currentLocation = null;
    let sections = [];
    let updateQueued = false;

    function currentSection() {
      if (!sections.length) return null;
      const line = Math.max(80, Math.min(window.innerHeight * 0.38, 280));
      let winner = sections[0];
      for (const section of sections) {
        if (section.element.getBoundingClientRect().top <= line) winner = section;
        else break;
      }
      return winner;
    }

    function captureSemanticLocation() {
      if (window.scrollY <= 8) return { kind: 'top', id: null };
      const documentHeight = Math.max(document.documentElement.scrollHeight, document.body.scrollHeight);
      if (window.scrollY + window.innerHeight >= documentHeight - 8) {
        return { kind: 'end', id: null };
      }
      const candidates = Array.from(reading.querySelectorAll('[data-semantic-location]'));
      if (!candidates.length) return { kind: 'top', id: null };
      const line = Math.max(80, Math.min(window.innerHeight * 0.38, 280));
      let winner = candidates[0];
      for (const candidate of candidates) {
        if (candidate.getBoundingClientRect().top <= line) winner = candidate;
        else break;
      }
      return { kind: 'event', id: winner.dataset.semanticLocation || null };
    }

    function restoreSemanticLocation(location) {
      const held = location || { kind: 'top', id: null };
      if (held.kind === 'end') {
        window.scrollTo({ top: Math.max(0, document.documentElement.scrollHeight), behavior: 'auto' });
        markCurrent();
        return true;
      }
      if (held.kind === 'top') {
        window.scrollTo({ top: 0, behavior: 'auto' });
        markCurrent();
        return true;
      }
      const target = Array.from(reading.querySelectorAll('[data-semantic-location]')).find(function (node) {
        return node.dataset.semanticLocation === held.id;
      });
      if (!target) return false;
      target.scrollIntoView({ block: 'start', behavior: 'auto' });
      currentLocation = held.id;
      markCurrent();
      return true;
    }

    function markCurrent() {
      const active = currentSection();
      currentLocation = active ? active.id : null;
      const contents = shell.querySelector('[data-reader-contents]');
      if (!contents) return;
      contents.querySelectorAll('[data-reader-location]').forEach(function (button) {
        if (button.dataset.readerLocation === currentLocation) {
          button.setAttribute('aria-current', 'location');
        } else {
          button.removeAttribute('aria-current');
        }
      });
    }

    function scheduleMark() {
      if (updateQueued) return;
      updateQueued = true;
      requestAnimationFrame(function () {
        updateQueued = false;
        markCurrent();
      });
    }

    function close(options) {
      if (!openName) return;
      const closeOptions = options || {};
      const name = openName;
      const surface = surfaces.get(name);
      const button = actions.get(name);
      const restoreTo = invoker;
      const restoreY = preservedY;
      const restoreLocation = preservedLocation;
      openName = null;
      invoker = null;
      if (surface && surface.open) surface.close();
      if (button) button.setAttribute('aria-expanded', 'false');
      if (closeOptions.restoreScroll !== false) {
        window.scrollTo({ top: restoreY, behavior: 'auto' });
        currentLocation = restoreLocation;
        markCurrent();
      }
      if (closeOptions.restoreFocus !== false && restoreTo) {
        restoreTo.focus({ preventScroll: true });
      }
      if (typeof held.onClose === 'function') held.onClose(name);
    }

    function open(name, button) {
      const surface = surfaces.get(name);
      if (!surface) return;
      if (openName) close({ restoreFocus: false });
      preservedY = window.scrollY;
      preservedLocation = currentLocation;
      invoker = button || actions.get(name) || null;
      if (typeof held.beforeOpen === 'function') held.beforeOpen(name);
      openName = name;
      const action = actions.get(name);
      if (action) action.setAttribute('aria-expanded', 'true');
      surface.showModal();
      const first = focusable(surface);
      if (first) first.focus({ preventScroll: true });
      if (typeof held.onOpen === 'function') held.onOpen(name);
    }

    function setContents(items) {
      sections = (items || []).filter(function (item) {
        return item && item.id && item.element;
      });
      const contents = shell.querySelector('[data-reader-contents]');
      if (!contents) return;
      contents.replaceChildren();
      let currentGroup = null;
      sections.forEach(function (item, index) {
        const group = item.group || 'Proper of the Mass';
        if (group !== currentGroup) {
          currentGroup = group;
          const division = document.createElement('p');
          division.className = 'contents-division';
          division.textContent = group;
          contents.appendChild(division);
        }
        const button = document.createElement('button');
        button.type = 'button';
        button.dataset.readerLocation = item.id;
        button.dataset.ordinal = String(index + 1).padStart(2, '0');
        button.textContent = item.label;
        button.addEventListener('click', function () {
          close({ restoreScroll: false, restoreFocus: false });
          item.element.scrollIntoView({ block: 'start', behavior: 'auto' });
          item.element.focus({ preventScroll: true });
          currentLocation = item.id;
          markCurrent();
        });
        contents.appendChild(button);
      });
      markCurrent();
    }

    actions.forEach(function (button, name) {
      button.addEventListener('click', function () { open(name, button); });
    });
    surfaces.forEach(function (surface) {
      surface.querySelectorAll('[data-reader-close]').forEach(function (button) {
        button.addEventListener('click', function () { close(); });
      });
      surface.addEventListener('cancel', function (event) {
        event.preventDefault();
        close();
      });
    });
    window.addEventListener('scroll', scheduleMark, { passive: true });
    window.addEventListener('resize', scheduleMark);

    return Object.freeze({
      open: open,
      close: close,
      setContents: setContents,
      currentLocation: function () { return currentLocation; },
      captureSemanticLocation: captureSemanticLocation,
      restoreSemanticLocation: restoreSemanticLocation,
      openSurface: function () { return openName; },
      refreshLocation: markCurrent
    });
  }

  root.TriptychReaderShell = Object.freeze({ create: create });
}(typeof globalThis !== 'undefined' ? globalThis : window));
