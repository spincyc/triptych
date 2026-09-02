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

  function variantGroupsOf(file) {
    return file.variants || [];
  }

  function variantGroupOf(file) {
    return variantGroupsOf(file)[0] || null;
  }

  function chosenOption(group, wanted) {
    const found = (group.options || []).find((one) => one.id === wanted);
    return found || (group.options || []).find((one) => one.default) || null;
  }

  /**
   * Resolve every independent choice group. A scalar is retained for the old
   * CLI contract: it selects the one group that owns that option, while every
   * other group takes its declared display default. A map is the canonical
   * form. Invalid values do not create a new branch; they fall back to the
   * source-declared default and are rejected at the reader boundary.
   */
  function selectionMap(file, wanted) {
    const supplied = wanted && typeof wanted === 'object' && !Array.isArray(wanted)
      ? wanted : {};
    const listed = Array.isArray(wanted)
      ? wanted.filter((one) => typeof one === 'string') : [];
    const scalar = typeof wanted === 'string' ? wanted : null;
    const selected = {};
    for (const group of variantGroupsOf(file)) {
      const listedForGroup = listed.filter((wantedOption) =>
        (group.options || []).some((one) => one.id === wantedOption));
      if (new Set(listedForGroup).size > 1) {
        throw new Error(
          'conflicting Ordinary options for group ' + String(group.group || ''));
      }
      const scalarHere = scalar && (group.options || []).some((one) => one.id === scalar);
      const listedHere = listedForGroup[0];
      const choice = chosenOption(
        group, supplied[group.group] || listedHere || (scalarHere ? scalar : null));
      if (choice) selected[group.group] = choice.id;
    }
    return selected;
  }

  function predicateState(predicates, key) {
    if (!predicates) return null;
    if (typeof predicates.has === 'function') {
      return predicates.has(key) ? true : null;
    }
    if (Array.isArray(predicates)) return predicates.includes(key) ? true : null;
    if (!Object.prototype.hasOwnProperty.call(predicates, key)) return null;
    return predicates[key] === true ? true : predicates[key] === false ? false : null;
  }

  /**
   * Derive only applicability facts the settled calendar result states. The
   * input is deliberately small so browser and terminal cannot grow separate
   * rank/name heuristics. Local solemnity and proper-Preface facts are not in
   * this calendar context and therefore remain unknown.
   */
  function predicateFacts(context) {
    const facts = {};
    if (!context || context.settled !== true ||
        typeof context.nature !== 'string' || !context.nature) return facts;
    const weekday = context.weekday;
    const season = context.season;
    const weekdays = [
      'sunday', 'monday', 'tuesday', 'wednesday',
      'thursday', 'friday', 'saturday'
    ];
    const sunday = weekdays.includes(weekday) ? weekday === 'sunday' : null;
    const exactNatures = [
      'additional-mass', 'feast', 'memorial', 'optional-memorial',
      'solemnity', 'sunday', 'triduum', 'weekday'
    ];
    const exactNature = exactNatures.includes(context.nature);

    if (sunday !== null) {
      if (!sunday) {
        facts['sunday-outside-advent-and-lent'] = false;
      } else if (season === 'advent' || season === 'lent') {
        facts['sunday-outside-advent-and-lent'] = false;
      } else if (typeof season === 'string' && season) {
        facts['sunday-outside-advent-and-lent'] = true;
      }
    }
    if (exactNature) {
      facts['solemnity-or-feast'] =
        context.nature === 'solemnity' || context.nature === 'feast';
    }
    if (sunday === true || context.nature === 'solemnity') {
      facts['sunday-or-solemnity'] = true;
    } else if (sunday === false && exactNature) {
      facts['sunday-or-solemnity'] = false;
    }
    return facts;
  }

  function conditionsResolve(element, selected, predicates) {
    let unresolved = null;
    for (const condition of element.conditions || []) {
      if (condition.kind === 'include-when-any') {
        const states = (condition.predicates || []).map(
          (key) => predicateState(predicates, key));
        if (states.some((state) => state === true)) continue;
        if (states.length && states.every((state) => state === false)) {
          return { show: false, unresolved: null };
        }
        unresolved = unresolved || condition;
      } else if (condition.kind === 'omit-when-option') {
        if ((condition.options || []).includes(selected[condition.group])) {
          return { show: false, unresolved: null };
        }
      } else {
        // Unknown applicability is never permission to print the element.
        unresolved = unresolved || condition;
      }
    }
    return unresolved
      ? { show: false, unresolved: unresolved }
      : { show: true, unresolved: null };
  }

  function conditionsShow(element, selected, predicates) {
    return conditionsResolve(element, selected, predicates).show;
  }

  function alternativeShows(element, file, selected) {
    const alternatives = element.alternatives || [];
    if (alternatives.length) {
      for (const alternative of alternatives) {
        if (selected[alternative.group] !== alternative.option) return false;
      }
    } else if (element.variant) {
      // Compatibility with the original single-group generated structures.
      const group = variantGroupsOf(file).find((one) =>
        (one.options || []).some((option) => option.id === element.variant));
      if (!group || selected[group.group] !== element.variant) return false;
    }
    return true;
  }

  function elementResolution(element, file, selected, predicates) {
    if (!alternativeShows(element, file, selected)) {
      return { show: false, unresolved: null };
    }
    return conditionsResolve(element, selected, predicates);
  }

  function elementShows(element, file, wanted, predicates) {
    return elementResolution(
      element, file, selectionMap(file, wanted), predicates).show;
  }

  function resolveElements(file, wanted, predicates) {
    const selected = selectionMap(file, wanted);
    const shown = [];
    const unresolved = [];
    for (const section of file.sections || []) {
      for (const element of section.elements || []) {
        const resolution = elementResolution(element, file, selected, predicates);
        if (resolution.show) {
          shown.push({ section: section, element: element });
        } else if (resolution.unresolved) {
          unresolved.push({
            section: section.key,
            element: element.key,
            condition: resolution.unresolved
          });
        }
      }
    }
    return { selected: selected, shown: shown, unresolved: unresolved };
  }

  function shownElements(file, wanted, predicates) {
    return resolveElements(file, wanted, predicates).shown;
  }

  function seats(file, shown) {
    const where = new Map();
    shown.forEach((row, index) => where.set(row.element.key, index));
    const slots = file.slots || [];
    const at = [];
    const byName = new Map();
    // The names a slot claims through a qualifier, and only for a slot whose
    // inventory entry asks for them. `Collect (Altera oratio)` is this
    // project's way of writing a further oration of the Collect's kind, and
    // that it stands in the Collect's place is the inventory's claim, made on
    // its own locus. The parenthesis is a naming convention and no rubric
    // authorises it, so nothing here may claim a name the data did not ask
    // for: a calendar whose inventory sets no flag is unaffected.
    const qualified = new Map();
    slots.forEach((slot, ordinal) => {
      const anchor = where.get(slot.anchor);
      // An unresolvable anchor loses the seat, never the proper.
      if (anchor === undefined) return;
      at[ordinal] = anchor + (slot.where === 'after' ? 1 : 0);
      for (const name of slot.propers || []) {
        byName.set(name, ordinal);
        if (slot.qualified) qualified.set(name, ordinal);
      }
    });
    return { slots: slots, at: at, byName: byName, qualified: qualified };
  }

  const QUALIFIER = /^(.+?) \(.+\)$/;

  /** The slot a proper name resolves to, or -1 for a name no slot claims. */
  function slotOf(seating, name) {
    if (seating.byName.has(name)) return seating.byName.get(name);
    const held = seating.qualified || new Map();
    const family = QUALIFIER.exec(name);
    if (family && held.has(family[1])) return held.get(family[1]);
    return -1;
  }

  function usableSlotOf(seating, name) {
    const ordinal = slotOf(seating, name);
    return ordinal >= 0 && Number.isInteger(seating.at[ordinal]) ? ordinal : -1;
  }

  function properRow(row, index) {
    if (row && Object.prototype.hasOwnProperty.call(row, 'proper') &&
        Number.isInteger(row.sourceIndex) && row.sourceIndex >= 0) {
      return { proper: row.proper, sourceIndex: row.sourceIndex };
    }
    return { proper: row, sourceIndex: index };
  }

  function dispositionOf(proper) {
    if (!proper || !Object.prototype.hasOwnProperty.call(proper, 'ordinary_disposition')) {
      return null;
    }
    const disposition = proper.ordinary_disposition;
    if (!disposition || typeof disposition !== 'object' || Array.isArray(disposition)) {
      throw new Error('Proper ordinary_disposition must be an exact mapping');
    }
    const keys = Object.keys(disposition).sort();
    const wanted = disposition.kind === 'alternative'
      ? ['basis', 'group', 'kind', 'option']
      : disposition.kind === 'unplaced'
        ? ['basis', 'group', 'kind', 'region'] : [];
    if (!wanted.length || keys.length !== wanted.length ||
        keys.some((key, index) => key !== wanted[index])) {
      throw new Error('Proper ordinary_disposition carries an unsupported shape');
    }
    for (const key of wanted.filter((one) => one !== 'kind')) {
      if (typeof disposition[key] !== 'string' || !disposition[key].trim()) {
        throw new Error('Proper ordinary_disposition fields must be nonempty strings');
      }
    }
    const stableId = /^[a-z0-9]+(?:-[a-z0-9]+)*$/;
    if (!stableId.test(disposition.group) ||
        (disposition.kind === 'alternative' && !stableId.test(disposition.option))) {
      throw new Error('Proper ordinary_disposition group and option must be kebab-case ids');
    }
    if (disposition.kind === 'unplaced' &&
        ['before-frame', 'after-frame'].indexOf(disposition.region) < 0) {
      throw new Error('unplaced Proper must name the before-frame or after-frame region');
    }
    return disposition;
  }

  function formIdOf(proper) {
    if (proper && Object.prototype.hasOwnProperty.call(proper, 'form_id') &&
        (typeof proper.form_id !== 'string' || !proper.form_id)) {
      throw new Error('Proper form_id must be a nonempty stable identity');
    }
    return proper && proper.form_id || 'main';
  }

  /**
   * Collapse only source-authored alternative annotations.  Every source row
   * survives inside exactly one unit with its original sourceIndex; a group is
   * atomic only after all of its members independently resolve to the same
   * Ordinary slot.  No array position selects an option.
   */
  function properUnits(propers, seating, isPlaceholder) {
    const rows = (propers || []).map(properRow).filter(function (row) {
      return !(isPlaceholder && isPlaceholder(row.proper));
    });
    const units = [];
    const alternativeGroups = new Set();
    const unplacedGroups = new Map();

    for (let index = 0; index < rows.length;) {
      const row = rows[index];
      const disposition = dispositionOf(row.proper);
      if (!disposition) {
        units.push({ kind: 'proper', proper: row.proper, sourceIndex: row.sourceIndex, seat: null });
        index += 1;
        continue;
      }
      if (disposition.kind === 'unplaced') {
        if (seating && usableSlotOf(seating, row.proper && row.proper.name) >= 0) {
          throw new Error('unplaced Proper annotation is stale because a usable slot now claims it');
        }
        if (alternativeGroups.has(disposition.group)) {
          throw new Error('ordinary_disposition group cannot be both alternative and unplaced');
        }
        const held = unplacedGroups.get(disposition.group);
        if (held && (held.region !== disposition.region || held.basis !== disposition.basis)) {
          throw new Error('unplaced Proper group must retain one region and source basis');
        }
        unplacedGroups.set(disposition.group, disposition);
        units.push({
          kind: 'proper', proper: row.proper, sourceIndex: row.sourceIndex,
          seat: {
            key: 'unplaced/' + disposition.group,
            placement: 'unseated', region: disposition.region,
            basis: disposition.basis, group: disposition.group,
            formId: formIdOf(row.proper)
          }
        });
        index += 1;
        continue;
      }

      if (alternativeGroups.has(disposition.group) || unplacedGroups.has(disposition.group)) {
        throw new Error('alternative Proper group must be one contiguous source unit');
      }
      alternativeGroups.add(disposition.group);
      const members = [];
      while (index < rows.length) {
        const memberDisposition = dispositionOf(rows[index].proper);
        if (!memberDisposition || memberDisposition.kind !== 'alternative' ||
            memberDisposition.group !== disposition.group) break;
        if (memberDisposition.basis !== disposition.basis) {
          throw new Error('alternative Proper group must retain one source basis');
        }
        members.push({
          proper: rows[index].proper,
          sourceIndex: rows[index].sourceIndex,
          option: memberDisposition.option
        });
        index += 1;
      }
      const byOption = new Map();
      const formIds = new Set(members.map(function (member) {
        return formIdOf(member.proper);
      }));
      if (formIds.size !== 1) {
        throw new Error('alternative Proper group must belong to one stable Mass form');
      }
      members.forEach(function (member) {
        if (!byOption.has(member.option)) byOption.set(member.option, []);
        byOption.get(member.option).push({
          proper: member.proper, sourceIndex: member.sourceIndex
        });
      });
      if (byOption.size < 2) {
        throw new Error('alternative Proper group must carry at least two distinct options');
      }
      let ordinal = null;
      if (seating) {
        members.forEach(function (member) {
          const found = usableSlotOf(seating, member.proper && member.proper.name);
          if (found < 0 || (ordinal !== null && found !== ordinal)) {
            throw new Error('alternative Proper group must share one usable semantic Ordinary seat');
          }
          ordinal = found;
        });
      }
      units.push({
        kind: 'proper_choice', group: disposition.group, basis: disposition.basis,
        formId: Array.from(formIds)[0],
        sourceIndex: members[0].sourceIndex,
        ordinal: ordinal,
        seat: ordinal === null ? null : seating.slots[ordinal],
        options: Array.from(byOption, function (entry) {
          return { id: entry[0], rows: entry[1] };
        })
      });
    }

    // "before" and "after" are source prefix/suffix claims, not permission
    // to move a middle row around the frame.
    let phase = 'before';
    units.forEach(function (unit) {
      const region = unit.kind === 'proper' && unit.seat && unit.seat.region;
      if (region === 'before-frame') {
        if (phase !== 'before') throw new Error('before-frame Proper must be a source prefix');
      } else if (region === 'after-frame') {
        phase = 'after';
      } else {
        if (phase === 'after') throw new Error('after-frame Proper must be a source suffix');
        phase = 'frame';
      }
    });
    return units;
  }

  function seatPropers(propers, seating, isPlaceholder) {
    const before = [];
    const buckets = new Map();
    const after = [];
    let reached = -1;
    let riding = null;
    let broke = false;
    const units = properUnits(propers, seating, isPlaceholder);
    for (const unit of units) {
      if (unit.kind === 'proper' && unit.seat && unit.seat.region) {
        (unit.seat.region === 'before-frame' ? before : after).push(unit);
        continue;
      }
      if (broke) {
        unit.seat = null;
        after.push(unit);
        continue;
      }
      const ordinal = unit.kind === 'proper_choice'
        ? unit.ordinal : usableSlotOf(seating, unit.proper && unit.proper.name);
      if (ordinal < 0) {
        unit.seat = null;
        (riding || before).push(unit);
        continue;
      }
      if (ordinal < reached) {
        broke = true;
        unit.seat = null;
        after.push(unit);
        continue;
      }
      reached = ordinal;
      const index = seating.at[ordinal];
      riding = buckets.get(index) || [];
      buckets.set(index, riding);
      unit.seat = seating.slots[ordinal];
      riding.push(unit);
    }
    return {
      before: before, buckets: buckets, after: after, broke: broke,
      sourceCount: units.reduce(function (count, unit) {
        return count + (unit.kind === 'proper_choice'
          ? unit.options.reduce(function (held, option) { return held + option.rows.length; }, 0)
          : 1);
      }, 0)
    };
  }

  /** The seated frame in reading order, before either renderer presents it. */
  function massEvents(shown, placed) {
    const events = [];
    const proper = function (row, placement) {
      if (row.kind === 'proper_choice') {
        events.push({
          kind: 'proper_choice', group: row.group, basis: row.basis,
          formId: row.formId,
          sourceIndex: row.sourceIndex, options: row.options,
          seat: row.seat, placement: placement
        });
        return;
      }
      events.push({
        kind: 'proper', proper: row.proper, sourceIndex: row.sourceIndex,
        seat: row.seat,
        placement: row.seat && row.seat.placement || placement
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

  /** Source-order Proper events when no Ordinary frame is being rendered. */
  function unframedEvents(propers, isPlaceholder) {
    return properUnits(propers, null, isPlaceholder).map(function (unit) {
      if (unit.kind === 'proper_choice') {
        return {
          kind: 'proper_choice', group: unit.group, basis: unit.basis,
          formId: unit.formId,
          sourceIndex: unit.sourceIndex, options: unit.options,
          seat: null, placement: null
        };
      }
      return {
        kind: 'proper', proper: unit.proper, sourceIndex: unit.sourceIndex,
        seat: unit.seat,
        placement: unit.seat && unit.seat.placement || null
      };
    });
  }

  return {
    variantGroupsOf: variantGroupsOf,
    variantGroupOf: variantGroupOf,
    chosenOption: chosenOption,
    selectionMap: selectionMap,
    predicateFacts: predicateFacts,
    conditionsShow: conditionsShow,
    resolveElements: resolveElements,
    elementShows: elementShows,
    shownElements: shownElements,
    seats: seats,
    slotOf: slotOf,
    usableSlotOf: usableSlotOf,
    dispositionOf: dispositionOf,
    properUnits: properUnits,
    seatPropers: seatPropers,
    massEvents: massEvents,
    unframedEvents: unframedEvents
  };
}));
