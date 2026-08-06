/* Generated navigation for the reading-first liturgy pages.
 *
 * This module knows only about rendered DOM. Each page supplies the title,
 * reading surface, utility disclosure, navigation container, and the semantic
 * heading selector appropriate to that page. Liturgical names, missal rules,
 * URL state, and render sequencing remain with the page that owns them.
 */

'use strict';

(function () {
  const GENERATED_ID = 'data-reading-contents-generated-id';
  const GENERATED_TABINDEX = 'data-reading-contents-tabindex';
  const generatedTargets = new Set();

  function documentOf(options) {
    const node = options && (options.reading || options.beginning || options.nav);
    return (node && node.ownerDocument) || document;
  }

  function removeGeneratedAttributes(doc) {
    const marked = new Set(generatedTargets);
    for (const target of doc.querySelectorAll(
      '[' + GENERATED_ID + '], [' + GENERATED_TABINDEX + ']'
    )) marked.add(target);
    for (const target of marked) {
      if (target.id === target.getAttribute(GENERATED_ID)) target.removeAttribute('id');
      target.removeAttribute(GENERATED_ID);
      if (target.getAttribute('tabindex') === '-1') target.removeAttribute('tabindex');
      target.removeAttribute(GENERATED_TABINDEX);
    }
    generatedTargets.clear();
  }

  function clear(options) {
    const held = options || {};
    removeGeneratedAttributes(documentOf(held));
    if (held.nav) held.nav.replaceChildren();
    if (held.disclosure) held.disclosure.hidden = true;
  }

  function headingLabel(target) {
    const copy = target.cloneNode(true);
    for (const reference of copy.querySelectorAll('.proper-ref')) reference.remove();
    return copy.textContent.replace(/\s+/g, ' ').trim();
  }

  function generatedId(ordinal) {
    return 'reading-destination-' + String(ordinal).padStart(2, '0');
  }

  function makeFocusable(target) {
    if (target.hasAttribute('tabindex')) return;
    target.setAttribute('tabindex', '-1');
    target.setAttribute(GENERATED_TABINDEX, 'true');
    generatedTargets.add(target);
  }

  function assignId(target, ordinal, used) {
    if (target.id) return;
    let candidateOrdinal = ordinal;
    let candidate = generatedId(candidateOrdinal);
    while (used.has(candidate)) {
      candidateOrdinal += 1;
      candidate = generatedId(candidateOrdinal);
    }
    target.id = candidate;
    target.setAttribute(GENERATED_ID, candidate);
    generatedTargets.add(target);
    used.add(candidate);
  }

  function navigationButton(doc, label, target) {
    const button = doc.createElement('button');
    button.type = 'button';
    button.textContent = label;
    button.addEventListener('click', () => {
      target.scrollIntoView({ block: 'start' });
      target.focus({ preventScroll: true });
    });
    return button;
  }

  function rebuild(options) {
    const held = options || {};
    const beginning = held.beginning;
    const reading = held.reading;
    const disclosure = held.disclosure;
    const nav = held.nav;
    const selector = held.selector;
    const doc = documentOf(held);

    clear(held);
    if (!beginning || !reading || !disclosure || !nav || !selector) return [];

    const destinations = [beginning].concat(Array.from(reading.querySelectorAll(selector)));
    const used = new Set(Array.from(doc.querySelectorAll('[id]'), (node) => node.id));
    destinations.forEach((target, index) => {
      assignId(target, index + 1, used);
      makeFocusable(target);
      nav.appendChild(navigationButton(
        doc,
        index === 0 ? 'Beginning' : headingLabel(target),
        target
      ));
    });
    disclosure.hidden = destinations.length === 0;
    return destinations;
  }

  window.ReadingContents = Object.freeze({ clear, rebuild });
}());
