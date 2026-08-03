/* ===========================================================================
 * The Ordinary's seats — the derivation, and nothing else
 * ===========================================================================
 *
 * THIS FILE IS NOT A PAGE. It selects the elements shown for an Ordinary,
 * resolves the Ordinary's declared slots against those elements, and seats a
 * Mass's propers without reordering them, then walks the seated frame as
 * semantic events. It touches no DOM, emits no text, fetches nothing, and knows
 * nothing about either renderer. `day.js` uses it in the browser; `mass-today`
 * runs it under node. One implementation, so the two renderers cannot drift.
 * ======================================================================== */

'use strict';

(function (root, factory) {
  const api = factory();
  if (typeof module === 'object' && module && module.exports) module.exports = api;
  else root.OrdinarySeating = api;
}(typeof self !== 'undefined' ? self : this, function () {

  function variantGroupOf(file) {
    return (file.variants || [])[0] || null;
  }

  function chosenOption(group, wanted) {
    const found = (group.options || []).find((one) => one.id === wanted);
    return found || (group.options || []).find((one) => one.default) || null;
  }

  function elementShows(element, file, wanted) {
    if (!element.variant) return true;
    const group = variantGroupOf(file);
    const chosen = group && chosenOption(group, wanted);
    return Boolean(chosen && chosen.id === element.variant);
  }

  function shownElements(file, wanted) {
    const held = [];
    for (const section of file.sections || []) {
      for (const element of section.elements || []) {
        if (elementShows(element, file, wanted)) {
          held.push({ section: section, element: element });
        }
      }
    }
    return held;
  }

  function seats(file, shown) {
    const where = new Map();
    shown.forEach((row, index) => where.set(row.element.key, index));
    const slots = file.slots || [];
    const at = [];
    const byName = new Map();
    slots.forEach((slot, ordinal) => {
      const anchor = where.get(slot.anchor);
      // An unresolvable anchor loses the seat, never the proper.
      if (anchor === undefined) return;
      at[ordinal] = anchor + (slot.where === 'after' ? 1 : 0);
      for (const name of slot.propers || []) byName.set(name, ordinal);
    });
    return { slots: slots, at: at, byName: byName };
  }

  function seatPropers(propers, seating, isPlaceholder) {
    const before = [];
    const buckets = new Map();
    const after = [];
    let reached = -1;
    let riding = null;
    let broke = false;
    for (const proper of propers) {
      if (isPlaceholder && isPlaceholder(proper)) continue;
      if (broke) { after.push({ proper: proper, seat: null }); continue; }
      const ordinal = seating.byName.has(proper.name) ? seating.byName.get(proper.name) : -1;
      if (ordinal < 0) { (riding || before).push({ proper: proper, seat: null }); continue; }
      if (ordinal < reached) { broke = true; after.push({ proper: proper, seat: null }); continue; }
      reached = ordinal;
      const index = seating.at[ordinal];
      riding = buckets.get(index) || [];
      buckets.set(index, riding);
      riding.push({ proper: proper, seat: seating.slots[ordinal] });
    }
    return { before: before, buckets: buckets, after: after, broke: broke };
  }

  /** The seated frame in reading order, before either renderer presents it. */
  function massEvents(shown, placed) {
    const events = [];
    const proper = function (row, placement) {
      events.push({
        kind: 'proper', proper: row.proper, seat: row.seat, placement: placement
      });
    };

    for (const row of placed.before) proper(row, 'before');

    let current = null;
    for (let index = 0; index < shown.length; index += 1) {
      if (shown[index].section !== current) {
        current = shown[index].section;
        events.push({ kind: 'begin_section', section: current });
      }
      for (const row of placed.buckets.get(index) || []) proper(row, 'seated');
      events.push({ kind: 'ordinary_element', element: shown[index].element });
    }
    for (const row of placed.buckets.get(shown.length) || []) proper(row, 'seated');
    for (const row of placed.after) proper(row, 'after');
    return events;
  }

  return {
    variantGroupOf: variantGroupOf,
    chosenOption: chosenOption,
    elementShows: elementShows,
    shownElements: shownElements,
    seats: seats,
    seatPropers: seatPropers,
    massEvents: massEvents
  };
}));
