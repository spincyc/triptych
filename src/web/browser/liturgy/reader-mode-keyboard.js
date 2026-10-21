/* Shared keyboard behavior for the Day and Propers mode radiogroup. */
'use strict';

(function (root, factory) {
  const api = factory();
  if (typeof module === 'object' && module && module.exports) module.exports = api;
  else {
    root.TriptychReaderModeKeyboard = api;
    if (root.document) api.create(root.document);
  }
}(typeof globalThis !== 'undefined' ? globalThis : this, function () {
  function create(documentRoot) {
    const surface = documentRoot.querySelector('[data-reader-surface="mode"]');
    const group = surface && surface.querySelector('[role="radiogroup"]');
    if (!group) return null;
    const radios = Array.from(group.querySelectorAll('[role="radio"][data-mode]'));
    if (!radios.length) return null;

    function available(radio) {
      return !radio.disabled && radio.getAttribute('aria-disabled') !== 'true' &&
        !radio.hidden && !radio.closest('[hidden]');
    }

    function sync() {
      // Closing the surface abandons an unsubmitted Compare draft. Leaving its
      // form expanded would make reopening skip the selected radio on Shift+Tab.
      if (!surface.open) {
        const setup = surface.querySelector('#compare-setup');
        if (setup) setup.hidden = true;
      }
      const choices = radios.filter(available);
      const focused = choices.find(function (radio) {
        return radio === documentRoot.activeElement;
      });
      const checked = choices.find(function (radio) {
        return radio.getAttribute('aria-checked') === 'true';
      });
      const tabStop = focused || checked || choices[0];
      radios.forEach(function (radio) {
        radio.tabIndex = radio === tabStop ? 0 : -1;
      });
    }

    group.addEventListener('focusin', sync);
    group.addEventListener('focusout', function () { queueMicrotask(sync); });
    group.addEventListener('click', function () { queueMicrotask(sync); });
    group.addEventListener('keydown', function (event) {
      const current = event.target.closest('[role="radio"][data-mode]');
      if (!current || !group.contains(current)) return;
      if (!available(current)) {
        if (event.key === 'Enter' || event.key === ' ' || event.key === 'Spacebar') {
          event.preventDefault();
        }
        return;
      }
      if (event.altKey || event.ctrlKey || event.metaKey) return;
      if (event.key === 'Enter' || event.key === ' ' || event.key === 'Spacebar') {
        // Explicit activation also works when a host dispatches trusted key
        // events without the button's native synthesized click.
        event.preventDefault();
        current.click();
        return;
      }
      const choices = radios.filter(available);
      let next = null;
      const index = choices.indexOf(current);
      if (event.key === 'ArrowRight' || event.key === 'ArrowDown') {
        next = choices[(index + 1) % choices.length];
      } else if (event.key === 'ArrowLeft' || event.key === 'ArrowUp') {
        next = choices[(index + choices.length - 1) % choices.length];
      } else if (event.key === 'Home') {
        next = choices[0];
      } else if (event.key === 'End') {
        next = choices[choices.length - 1];
      }
      if (!next) return;
      event.preventDefault();
      next.focus({ preventScroll: true });
      // A Compare click opens its setup; only the controller may check it after
      // a valid choice. Unsupported modes likewise keep the controller's state.
      next.click();
    });

    const observer = new MutationObserver(sync);
    radios.forEach(function (radio) {
      observer.observe(radio, {
        attributes: true,
        attributeFilter: ['aria-checked', 'aria-disabled', 'disabled', 'hidden']
      });
    });
    observer.observe(surface, { attributes: true, attributeFilter: ['open'] });
    sync();
    return Object.freeze({ sync: sync });
  }

  return Object.freeze({ create: create });
}));
