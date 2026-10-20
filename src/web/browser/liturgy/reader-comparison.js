/* Semantic Proper comparison over two independently adapted reader results.
 * Calendar resolution, text selection, and source claims belong to the
 * existing adapters. This module pairs only their mapped functional slots.
 */

'use strict';

(function (root, factory) {
  const api = factory(
    typeof module === 'object' && module && module.exports
      ? require('./reader-state.js') : root.LiturgyReaderState
  );
  if (typeof module === 'object' && module && module.exports) module.exports = api;
  else root.LiturgyReaderComparison = api;
}(typeof globalThis !== 'undefined' ? globalThis : this, function (Contract) {
  if (!Contract) throw new Error('reader comparison requires the reader-state contract');

  // This is a display order for known functional slots, not an assertion that
  // different editions appoint the same text or celebrate the same feast.
  const SLOT_ORDER = Object.freeze([
    'entrance-antiphon', 'collect', 'reading-1', 'gradual',
    'responsorial-psalm', 'reading-2', 'gospel-acclamation', 'gospel',
    'offertory-chant', 'prayer-over-offerings', 'communion-antiphon',
    'prayer-after-communion'
  ]);
  const SLOT_SET = new Set(SLOT_ORDER);

  function fail(message) { throw new Error('reader comparison: ' + message); }

  function ordered(value) {
    if (Array.isArray(value)) return value.map(ordered);
    if (value && typeof value === 'object') {
      const out = {};
      Object.keys(value).sort().forEach(function (key) { out[key] = ordered(value[key]); });
      return out;
    }
    return value;
  }

  function same(left, right) { return JSON.stringify(ordered(left)) === JSON.stringify(ordered(right)); }

  function withoutOrations(languages) {
    const rest = Object.assign({}, languages);
    delete rest.orations;
    return rest;
  }

  function compare(input) {
    if (!input || !input.comparison || !Array.isArray(input.sides)) {
      fail('comparison and independently adapted sides are required');
    }
    const first = input.sides[0] && input.sides[0].result;
    const entrance = first && first.entrance;
    const errors = Contract.validateComparison(input.comparison, entrance);
    if (errors.length) fail(errors.map(function (one) { return one.message; }).join('; '));
    if (input.sides.length !== 2 || input.comparison.sides.length !== 2) {
      fail('this comparison supports exactly two sides');
    }
    const dimension = input.comparison.dimension;
    if (entrance === 'day' && dimension !== 'recension') {
      fail('Day comparison currently supports recension only');
    }
    if (entrance === 'propers' &&
        ['oration-language', 'lectionary-cycle'].indexOf(dimension) < 0) {
      fail('Propers comparison supports oration language or held lectionary cycles');
    }

    const sides = input.comparison.sides.map(function (descriptor, index) {
      const supplied = input.sides[index];
      const result = supplied && supplied.result;
      if (!supplied || supplied.id !== descriptor.id || !result ||
          result.entrance !== entrance || !result.request || !result.resolved) {
        fail('side ' + descriptor.id + ' needs its matching resolved adapter result');
      }
      if (result.request.edition.id !== descriptor.edition.id ||
          result.resolved.edition !== descriptor.edition.id) {
        fail('side ' + descriptor.id + ' edition does not match its result');
      }
      if (!Array.isArray(result.events) || !Array.isArray(result.coverage) ||
          !Array.isArray(result.unresolvedChoices)) {
        fail('side ' + descriptor.id + ' is missing adapter evidence');
      }
      if (result.unresolvedChoices.length ||
          (result.ordinaryUnresolved || []).length) {
        fail('side ' + descriptor.id + ' has choices that remain unresolved');
      }
      if (entrance === 'day') {
        const anchor = input.comparison.anchor;
        const requestedTerritory = result.request.calendar &&
          result.request.calendar.territory && result.request.calendar.territory.id || 'universal';
        if (result.request.civilDate !== anchor.civilDate ||
            !result.calendarResult || result.calendarResult.date !== anchor.civilDate ||
            result.request.calendar.id !== descriptor.calendar.id ||
            result.calendarResult.calendar !== descriptor.calendar.id ||
            requestedTerritory !== anchor.territorialContext ||
            !result.calendarResult.winner || !result.resolved.formulary) {
          fail('side ' + descriptor.id + ' must independently resolve the anchored calendar');
        }
      } else {
        const anchor = input.comparison.anchor;
        if (!result.request.languages || (dimension === 'oration-language' &&
            (!descriptor.languages || !descriptor.languages.orations))) {
          fail('side ' + descriptor.id + ' needs an explicit oration language');
        }
        if (result.request.civilDate !== null || result.calendarResult !== null ||
            result.request.formulary.id !== descriptor.formulary.id ||
            result.resolved.formulary !== descriptor.formulary.id ||
            result.resolved.formulary !== anchor.correspondingFormulary ||
            (dimension === 'oration-language' &&
              result.request.languages.orations !== descriptor.languages.orations) ||
            (dimension === 'lectionary-cycle' &&
              (!descriptor.cycle || result.request.cycle !== descriptor.cycle))) {
          fail('side ' + descriptor.id + ' must use the anchored date-independent formulary and language');
        }
      }
      return { id: descriptor.id, result: result };
    });

    if (entrance === 'propers') {
      const left = sides[0].result;
      const right = sides[1].result;
      const cycleComparison = dimension === 'lectionary-cycle';
      if (left.resolved.edition !== right.resolved.edition ||
          left.resolved.formulary !== right.resolved.formulary ||
          left.resolved.form !== right.resolved.form ||
          !same(left.request.bible, right.request.bible) ||
          !(cycleComparison ? same(left.request.languages, right.request.languages) :
            same(withoutOrations(left.request.languages), withoutOrations(right.request.languages))) ||
          !same(left.request.options, right.request.options) ||
          (cycleComparison ? left.request.cycle === right.request.cycle :
            left.request.cycle !== right.request.cycle) ||
          left.request.form !== right.request.form ||
          left.request.alternative !== right.request.alternative ||
          (!cycleComparison && left.request.languages.orations === right.request.languages.orations)) {
        fail(dimension + ' requires the same edition, form, formulary, Bible, and other selections on distinct peers');
      }
    } else if (!same(sides[0].result.request.bible, sides[1].result.request.bible) ||
               !same(sides[0].result.request.languages, sides[1].result.request.languages)) {
      fail('recension comparison requires the same Bible and language selections');
    } else if (sides[0].result.resolved.edition === sides[1].result.resolved.edition) {
      fail('recension comparison requires distinct editions');
    }

    if (dimension === 'lectionary-cycle') {
      sides.forEach(function (side, index) {
        const cycle = input.comparison.sides[index].cycle;
        if (!side.result.events.some(function (event) {
          return event.selected && event.selected.cycle === cycle;
        })) fail('side ' + side.id + ' has no resolved material for its requested held cycle');
      });
    }

    const indexed = sides.map(function (side) {
      const bySlot = new Map();
      side.result.events.forEach(function (event) {
        if (!event || event.kind !== 'proper') {
          fail('only resolved Proper events can be aligned in this slice');
        }
        const slot = event.semanticSlot;
        const slotId = slot && slot.state === 'mapped' && slot.identity && slot.identity.id;
        if (!SLOT_SET.has(slotId)) {
          fail('unmapped or unsupported Proper slot on side ' + side.id);
        }
        if (bySlot.has(slotId)) {
          fail('duplicate Proper slot ' + slotId + ' on side ' + side.id);
        }
        if (!event.selected || typeof event.selected.availability !== 'string') {
          fail('Proper slot ' + slotId + ' lacks a selected-material state');
        }
        bySlot.set(slotId, event);
      });
      return bySlot;
    });

    function cell(side, event) {
      if (!event) return {
        id: side.id, status: 'no-event-in-selected-formulary', event: null
      };
      const availability = event.selected.availability;
      const statuses = {
        held: 'text-held', unavailable: 'text-unavailable',
        'choice-required': 'choice-required', absent: 'selected-material-absent'
      };
      if (!statuses[availability]) fail('unsupported selected-material state ' + availability);
      return { id: side.id, status: statuses[availability], event: event };
    }

    const units = SLOT_ORDER.filter(function (slot) {
      return indexed.some(function (bySlot) { return bySlot.has(slot); });
    }).map(function (slot) {
      return {
        semanticSlot: slot,
        relation: 'functional-slot-only',
        sides: sides.map(function (side, index) {
          return cell(side, indexed[index].get(slot));
        })
      };
    });
    const calendarResults = entrance === 'day' ? sides.map(function (side) {
      return {
        id: side.id,
        calendarResult: side.result.calendarResult,
        resolved: side.result.resolved
      };
    }) : null;

    return {
      schema: 'triptych-liturgy-reader-comparison/v1',
      entrance: entrance,
      dimension: dimension,
      anchor: input.comparison.anchor,
      calendarResults: calendarResults,
      sides: sides,
      units: units
    };
  }

  return Object.freeze({ SLOT_ORDER: SLOT_ORDER, compare: compare });
}));
