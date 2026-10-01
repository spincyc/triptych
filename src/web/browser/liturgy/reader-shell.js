/* Reusable persistent reader shell. It owns interaction, never liturgy. */
'use strict';

(function (root) {
  function focusable(surface) {
    return surface.querySelector(
      '[data-reader-close], button:not([disabled]), input:not([disabled]), ' +
      'select:not([disabled]), textarea:not([disabled]), a[href], [tabindex]:not([tabindex="-1"])'
    );
  }

  // What the browser gives a MODAL dialog by itself (`dialog:modal`: fixed to
  // the viewport and above every page layer, the highest of which here is 80),
  // lent to a non-modal surface while it is shown so that it stands where the
  // reader's own action would put it, and taken back when it closes. Margins,
  // sizes and the narrow bottom-sheet form stay with the stylesheets.
  const NON_MODAL_GEOMETRY = Object.freeze({ position: 'fixed', inset: '0', 'z-index': '90' });

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
    let openModal = false;
    let invoker = null;
    let preservedY = 0;
    let preservedLocation = null;
    let currentLocation = null;
    let sections = [];
    let loci = [];
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

    function currentLocus() {
      if (!loci.length) return null;
      const line = Math.max(80, Math.min(window.innerHeight * 0.38, 280));
      let winner = null;
      let nearestTop = -Infinity;
      for (const item of loci) {
        const top = item.element.getBoundingClientRect().top;
        if (top <= line && top > nearestTop) {
          winner = item;
          nearestTop = top;
        }
      }
      return winner || loci[0];
    }

    function locusHeading(item) {
      if (!item || !item.element) return null;
      if (item.element.matches('.ordinary-division')) return item.element;
      return item.element.querySelector(
        ':scope > .proper-name, :scope > .ordinary-head, :scope > h2, :scope > h3'
      );
    }

    function isReadingHeadingVisible(node) {
      if (!node) return false;
      const masthead = shell.querySelector('.reader-masthead');
      const topEdge = masthead && getComputedStyle(masthead).position === 'sticky'
        ? masthead.getBoundingClientRect().bottom : 0;
      const box = node.getBoundingClientRect();
      return box.bottom > topEdge && box.top < window.innerHeight;
    }

    function updateLocus() {
      const output = shell.querySelector('[data-reader-locus]');
      if (!output) return;
      const identity = shell.querySelector('.reader-identity');
      const masthead = shell.querySelector('.reader-masthead');
      const identityEdge = masthead && getComputedStyle(masthead).position === 'sticky'
        ? masthead.getBoundingClientRect().bottom : 0;
      const active = currentLocus();
      const identityVisible = identity && identity.getBoundingClientRect().bottom > identityEdge + 8;
      const headingVisible = isReadingHeadingVisible(locusHeading(active));
      const majorHeadingVisible = headingVisible && active && active.element.matches('.ordinary-division');
      if (!active || identityVisible || majorHeadingVisible) {
        output.hidden = true;
        output.classList.remove('has-unit');
        return;
      }
      const major = output.querySelector('[data-reader-locus-major]');
      const unit = output.querySelector('[data-reader-locus-unit]');
      const separator = output.querySelector('.reader-locus-separator');
      major.textContent = active.major;
      unit.textContent = active.unit || '';
      const hasUnit = Boolean(active.unit && active.unit !== active.major && !headingVisible);
      unit.hidden = !hasUnit;
      if (separator) separator.hidden = !hasUnit;
      output.classList.toggle('has-unit', hasUnit);
      output.hidden = false;
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
      updateLocus();
    }

    function centerCurrentContents(surface) {
      if (!surface || !surface.open || openName !== 'contents') return;
      const contents = surface.querySelector('[data-reader-contents]');
      const current = contents && contents.querySelector('[aria-current="location"]');
      const scroller = contents && contents.closest('.surface-body');
      if (!contents || !current || !scroller || !current.isConnected) return;
      const row = current.getBoundingClientRect();
      const viewport = scroller.getBoundingClientRect();
      const wanted = scroller.scrollTop + row.top - viewport.top -
        Math.max(0, (scroller.clientHeight - row.height) / 2);
      scroller.scrollTop = Math.max(0, Math.min(wanted,
        scroller.scrollHeight - scroller.clientHeight));
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
      // A non-modal surface left the page live, so where the reader is now is
      // the place to keep; only a modal one holds a place to return to.
      const restoreScroll = openModal && closeOptions.restoreScroll !== false;
      if (surface && !openModal) {
        Object.keys(NON_MODAL_GEOMETRY).forEach(function (property) {
          surface.style.removeProperty(property);
        });
      }
      openName = null;
      openModal = false;
      invoker = null;
      if (surface && surface.open) surface.close();
      if (button) button.setAttribute('aria-expanded', 'false');
      if (restoreScroll) {
        window.scrollTo({ top: restoreY, behavior: 'auto' });
        currentLocation = restoreLocation;
        markCurrent();
      }
      if (closeOptions.restoreFocus !== false && restoreTo) {
        restoreTo.focus({ preventScroll: true });
      }
      if (typeof held.onClose === 'function') held.onClose(name);
    }

    /*
     * A surface the reader opens is MODAL: the page behind it is inert, focus
     * is contained, and Escape returns focus to the invoker. A surface a route
     * foregrounds by itself, before the reader has done anything, is opened
     * with `{ modal: false }` instead. Opened modally on load, Propers Browse
     * made the whole document inert, so Tab never reached the site's skip
     * link and the first key a keyboard reader pressed landed inside a dialog
     * nobody had asked for. Shown non-modally it stands open just the same,
     * but takes no focus, closes the moment focus moves anywhere else in the
     * page — so it can never sit over a focused control — or on Escape, and
     * the action that names it still opens it modally.
     */
    function open(name, button, presentation) {
      const surface = surfaces.get(name);
      if (!surface) return;
      const modal = !(presentation && presentation.modal === false);
      if (openName) close({ restoreFocus: false });
      markCurrent();
      preservedY = window.scrollY;
      preservedLocation = currentLocation;
      invoker = button || actions.get(name) || null;
      if (typeof held.beforeOpen === 'function') held.beforeOpen(name);
      openName = name;
      openModal = modal;
      const action = actions.get(name);
      if (action) action.setAttribute('aria-expanded', 'true');
      // Not `show()`: it runs the dialog focusing steps, which would move focus
      // — and Tab's starting point — into the surface. The attribute presents
      // the same non-modal dialog and leaves focus where the reader has it.
      if (modal) {
        surface.showModal();
      } else {
        Object.keys(NON_MODAL_GEOMETRY).forEach(function (property) {
          surface.style.setProperty(property, NON_MODAL_GEOMETRY[property]);
        });
        surface.setAttribute('open', '');
      }
      const first = modal && focusable(surface);
      if (first) first.focus({ preventScroll: true });
      if (name === 'contents') centerCurrentContents(surface);
      if (typeof held.onOpen === 'function') held.onOpen(name);
    }

    function setContents(items) {
      sections = (items || []).filter(function (item) {
        return item && item.id && item.element;
      });
      loci = Array.from(reading.querySelectorAll('[data-reader-locus-major]')).map(function (element) {
        return {
          element: element,
          major: element.dataset.readerLocusMajor,
          unit: element.dataset.readerLocusUnit || null
        };
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
    // A non-modal surface receives no `cancel`, so its two dismissals are
    // listened for here; while a modal one is open neither listener acts.
    document.addEventListener('focusin', function (event) {
      if (!openName || openModal) return;
      const surface = surfaces.get(openName);
      if (surface && !surface.contains(event.target)) {
        close({ restoreFocus: false });
      }
    });
    document.addEventListener('keydown', function (event) {
      if (event.key !== 'Escape' || !openName || openModal) return;
      const surface = surfaces.get(openName);
      event.preventDefault();
      close({ restoreFocus: Boolean(surface && surface.contains(document.activeElement)) });
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
