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

  const SOURCE_COORDINATE_DIMENSIONS = Object.freeze(['translation-witness', 'bible-edition']);

  function withoutWitness(languages) {
    const rest = Object.assign({}, languages); delete rest.translationWitness; return rest;
  }

  function withoutOrations(languages) {
    const rest = Object.assign({}, languages);
    delete rest.orations;
    return rest;
  }

  function selectedPropers(result) {
    return result.events.reduce(function (events, event) {
      if (event && event.kind === 'proper') return events.concat([event]);
      const selected = event && event.kind === 'proper-choice' && event.selection &&
        event.selection.state === 'selected' && event.options.find(function (option) {
          return option.id === event.selection.option;
        });
      if (!selected) fail('only resolved Proper events can be aligned in this slice');
      return events.concat(selected.events);
    }, []);
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
        ['oration-language', 'lectionary-cycle', 'reading-alternative', 'translation-witness', 'bible-edition'].indexOf(dimension) < 0) {
      fail('Propers comparison supports translation witnesses, Bible editions, oration languages, held cycles and reading alternatives');
    }

    const bibleComparison = dimension === 'bible-edition';
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
        if (bibleComparison) {
          const bible = descriptor.bible;
          const held = (input.bibles || []).filter(function (row) { return bible && row.id === bible.id; });
          if (!bible || descriptor.id !== bible.id || held.length !== 1 ||
              !same(result.request.bible, bible) || (held[0].numbering || null) !== bible.numbering) {
            fail('Bible comparison side must match one published Bible and its declared numbering');
          }
        }
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
              (!descriptor.cycle || result.request.cycle !== descriptor.cycle)) ||
            (dimension === 'translation-witness' && (!descriptor.languages ||
              result.request.languages.orations !== descriptor.languages.orations ||
              result.request.languages.translationWitness !== descriptor.languages.translationWitness)) ||
            (dimension === 'reading-alternative' && (!descriptor.alternative ||
              !same(result.request.alternative, descriptor.alternative) ||
              result.resolved.alternative !== descriptor.alternative.id))) {
          fail('side ' + descriptor.id + ' must use the anchored date-independent formulary and language');
        }
      }
      return { id: descriptor.id, result: result };
    });

    if (entrance === 'propers') {
      const left = sides[0].result;
      const right = sides[1].result;
      const cycleComparison = dimension === 'lectionary-cycle';
      const alternativeComparison = dimension === 'reading-alternative';
      const languageComparison = dimension === 'oration-language';
      const witnessComparison = dimension === 'translation-witness';
      if (!same(left.request.scriptureCompanion, right.request.scriptureCompanion) ||
          (left.request.textDisplay || 'selected') !== (right.request.textDisplay || 'selected') ||
          left.resolved.edition !== right.resolved.edition ||
          left.resolved.formulary !== right.resolved.formulary ||
          left.resolved.form !== right.resolved.form ||
          (bibleComparison ? left.request.bible.id === right.request.bible.id :
            !same(left.request.bible, right.request.bible)) ||
          !(languageComparison ?
            same(withoutOrations(left.request.languages), withoutOrations(right.request.languages)) :
            witnessComparison ? same(withoutWitness(left.request.languages), withoutWitness(right.request.languages)) :
            same(left.request.languages, right.request.languages)) ||
          !same(left.request.options, right.request.options) ||
          (cycleComparison ? left.request.cycle === right.request.cycle :
            left.request.cycle !== right.request.cycle) ||
          left.request.form !== right.request.form ||
          (alternativeComparison ? same(left.request.alternative, right.request.alternative) :
            !same(left.request.alternative, right.request.alternative)) ||
          (languageComparison && left.request.languages.orations === right.request.languages.orations) ||
          (witnessComparison && left.request.languages.translationWitness === right.request.languages.translationWitness)) {
        fail(dimension + ' requires the same edition, form, formulary, Bible, and other selections on distinct peers');
      }
    } else if (!same(sides[0].result.request.scriptureCompanion, sides[1].result.request.scriptureCompanion) ||
               (sides[0].result.request.textDisplay || 'selected') !==
               (sides[1].result.request.textDisplay || 'selected') ||
               !same(sides[0].result.request.bible, sides[1].result.request.bible) ||
               !same(sides[0].result.request.languages, sides[1].result.request.languages)) {
      fail('recension comparison requires the same Bible and language selections');
    } else if (sides[0].result.resolved.edition === sides[1].result.resolved.edition) {
      fail('recension comparison requires distinct editions');
    }

    if (dimension === 'lectionary-cycle') {
      sides.forEach(function (side, index) {
        const cycle = input.comparison.sides[index].cycle;
        if (!selectedPropers(side.result).some(function (event) {
          return event.selected && event.selected.cycle === cycle;
        })) fail('side ' + side.id + ' has no resolved material for its requested held cycle');
      });
    }

    if (dimension === 'reading-alternative') {
      const groups = sides.map(function (side, index) {
        const identity = input.comparison.sides[index].alternative.id;
        const group = side.result.events.find(function (event) {
          return event.kind === 'proper-choice' && event.selection.state === 'selected' &&
            event.id + '/' + event.selection.option === identity;
        });
        const selected = group && group.options.find(function (option) { return option.id === group.selection.option; });
        if (!selected || selected.events.length !== 1 || !selected.events.every(function (event) {
          return event.semanticSlot && event.semanticSlot.state === 'mapped' &&
            ['reading-1', 'reading-2', 'gospel'].includes(event.semanticSlot.identity.id);
        })) fail('reading-alternative requires one exact source reading option per side');
        return group.id;
      });
      if (groups[0] !== groups[1]) fail('reading alternatives must belong to the same held source group');
    }

    const coordinateAxis = SOURCE_COORDINATE_DIMENSIONS.includes(dimension);
    let coordinateOwners;
    if (coordinateAxis) {
      const structure = input.sides[0].structure;
      if (!structure || structure.schema !== 'triptych-propers-structure/v1' || !input.sides.every(function (side) { return side.structure === structure; }) ||
          structure.calendar !== sides[0].result.resolved.edition) {
        fail('same-source comparison requires one identical source structure revision on both sides');
      }
      const mass = (structure.masses || []).find(function (one) {
        return one.key === input.comparison.anchor.correspondingFormulary;
      });
      if (!mass) fail('same-source comparison has no exact source formulary');
      coordinateOwners = new Map();
      sides.forEach(function (side) {
        selectedPropers(side.result).forEach(function (event) {
          const prefix = 'proper/' + structure.calendar + '/' + mass.key + '/';
          const ordinal = event && event.id && event.id.startsWith(prefix) ? event.id.slice(prefix.length) : '';
          const hooks = event && (event.sourceHooks || []).filter(function (hook) { return hook.kind === 'proper-structure'; });
          const sourceId = structure.calendar + '/' + mass.key + '/' + ordinal;
          const owner = /^\d{3}$/.test(ordinal) && (mass.propers || [])[Number(ordinal) - 1];
          const form = side.result.resolved.form || 'main';
          if (!owner || !hooks || hooks.length !== 1 || hooks[0].id !== sourceId ||
              (owner.form_id || 'main') !== form || (event.form || null) !== (owner.form || null) ||
              event.sourceKind !== (owner.source || null) || event.editionSlotLabel !== (owner.name || null)) {
            fail('Proper event has no exact edition/formulary/form/source coordinate');
          }
          coordinateOwners.set(event.id, { label: owner.name, semanticSlot: event.semanticSlot &&
            event.semanticSlot.state === 'mapped' ? event.semanticSlot.identity.id : null,
            sourceCoordinate: { edition: structure.calendar, formulary: mass.key, form: form,
              eventId: event.id, properStructureId: sourceId, ordinal: Number(ordinal) } });
        });
      });
    }

    const indexed = sides.map(function (side) {
      const bySlot = new Map();
      selectedPropers(side.result).forEach(function (event) {
        if (!event || event.kind !== 'proper') {
          fail('only resolved Proper events can be aligned in this slice');
        }
        const slot = event.semanticSlot;
        const slotId = coordinateAxis ? event.id : slot && slot.state === 'mapped' && slot.identity && slot.identity.id;
        if (!coordinateAxis && !SLOT_SET.has(slotId)) {
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

    if (coordinateAxis && !same(Array.from(indexed[0].keys()).sort(), Array.from(indexed[1].keys()).sort())) {
      fail('same-source comparison sides require identical source coordinates');
    }
    const orderedUnits = coordinateAxis ? Array.from(coordinateOwners.keys()).sort(function (left, right) {
      return coordinateOwners.get(left).sourceCoordinate.ordinal - coordinateOwners.get(right).sourceCoordinate.ordinal;
    }) : SLOT_ORDER;
    const units = orderedUnits.filter(function (slot) {
      return indexed.some(function (bySlot) { return bySlot.has(slot); });
    }).map(function (slot) {
      return Object.assign(coordinateAxis ? {
        semanticSlot: coordinateOwners.get(slot).semanticSlot, relation: 'same-source-event',
        sourceCoordinate: coordinateOwners.get(slot).sourceCoordinate, label: coordinateOwners.get(slot).label
      } : { semanticSlot: slot, relation: 'functional-slot-only' }, {
        sides: sides.map(function (side, index) {
          return cell(side, indexed[index].get(slot));
        })
      });
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

  return Object.freeze({ SLOT_ORDER: SLOT_ORDER, SOURCE_COORDINATE_DIMENSIONS: SOURCE_COORDINATE_DIMENSIONS, compare: compare });
}));
