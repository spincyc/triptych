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
    // The appointment inputs travel with the facts so one call site feeds
    // both: the formulary's printed appointments (null where the day borrows
    // its formulary), the civil date and the owning year's anchors.
    if (context && (context.appointments !== undefined || context.date !== undefined)) {
      facts['appointment-context'] = {
        appointments: context.appointments || null,
        date: typeof context.date === 'string' ? context.date : null,
        anchors: context.anchors || null
      };
    }
    if (context) Object.assign(facts, seasonalOrationFacts(context));
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

  const DAY_MS = 86400000;

  function isoDay(value) {
    return typeof value === 'string' && /^\d{4}-\d{2}-\d{2}$/.test(value)
      ? Date.UTC(Number(value.slice(0, 4)), Number(value.slice(5, 7)) - 1,
        Number(value.slice(8, 10)))
      : null;
  }

  function offsetFrom(anchors, name, date) {
    const anchor = isoDay(anchors && anchors[name]);
    const day = isoDay(date);
    return anchor === null || day === null ? null : Math.round((day - anchor) / DAY_MS);
  }

  /**
   * The pre-1955 seasonal orations, established FALSE only outside the dates
   * their rubrics name, and never established true (inside, the rank of the
   * day decides: Doubles take one oration, RG IX n. 1 of the Bonn witness).
   *
   *   a-cunctis-season - the 1861 witness's own rubrics (ordinarium-oblatio-en
   *     seq 1 and 54, ordinarium-conclusio-en seq 6) and the Bonn reimpressio's
   *     Additiones et Variationes tit. VI n. 1, 3) (artifact p. 56*) bound the
   *     second oration A cunctis, with its Secret and Postcommunion, to
   *     Candlemas through the day before Passion Sunday and Trinity Sunday
   *     through the day before Advent. The union of the two books' windows is
   *     used, so no day either book admits is excluded.
   *   concede-season - Bonn tit. VI n. 1 and 6) (pp. 56*-57*): from Passion
   *     Sunday to Saturday in albis and through the octave of Pentecost a
   *     single seasonal oration contra persecutores is said, not Concede; and
   *     the vigil of Pentecost omits them (n. 1; Proprium p. 399).
   *
   * Inputs are the civil date and the owning liturgical year's anchors; with
   * either missing nothing is established.
   */
  function seasonalOrationFacts(context) {
    const facts = {};
    const anchors = context && context.anchors;
    const date = context && context.date;
    const easter = offsetFrom(anchors, 'easter', date);
    const pentecost = offsetFrom(anchors, 'pentecost', date);
    const trinity = offsetFrom(anchors, 'trinity', date);
    const advent = offsetFrom(anchors, 'next_first_sunday_of_advent', date);
    if (easter === null || pentecost === null || trinity === null || advent === null) {
      return facts;
    }
    const candlemas = isoDay(date.slice(0, 4) + '-02-02');
    const day = isoDay(date);
    const inACunctis = (day >= candlemas && easter < -14) ||
      (trinity >= 0 && advent < 0);
    if (!inACunctis) facts['a-cunctis-season'] = false;
    if ((easter >= -14 && easter <= 6) || (pentecost >= -1 && pentecost <= 6)) {
      facts['concede-season'] = false;
    }
    return facts;
  }

  const WEEKDAYS = [
    'sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday'
  ];

  function spanCovers(span, context) {
    const date = context && context.date;
    if (typeof date !== 'string') return null;
    // A span narrowed to one weekday covers only that weekday of its dates.
    if (span.weekday) {
      const day = isoDay(date);
      if (day === null) return null;
      if (WEEKDAYS[new Date(day).getUTCDay()] !== span.weekday) return false;
    }
    if (span.anchor) {
      const offset = offsetFrom(context.anchors, span.anchor, date);
      if (offset === null) return null;
      return offset >= span.from && offset <= span.to;
    }
    const monthDay = date.slice(5);
    return span.from <= span.to
      ? monthDay >= span.from && monthDay <= span.to
      : monthDay >= span.from || monthDay <= span.to;
  }

  /**
   * The day's appointment of every Ordinary variable the file declares.
   *
   * In order: what the celebrated formulary itself prints (only when it is the
   * day's own Mass, never when a feria borrows it: RGMR 501 puts the proper
   * Communicantes "suo loco in propriis Missis", and the Epiphany and
   * Ascension forms are said "in festo tantum"); then a dated span the book's
   * own heading states; then the variable's sourced default. Where none
   * applies, or a span could not be evaluated, the variable is UNAPPOINTED
   * (null) and the frame shows the typed stand-in, never the common form.
   */
  function appointmentsFor(file, context) {
    const held = {};
    const formulary = context && context.appointments || {};
    for (const variable of (file && file.appointments) || []) {
      const key = variable.variable;
      if (Object.prototype.hasOwnProperty.call(formulary, key)) {
        held[key] = formulary[key];
        continue;
      }
      let decided = false;
      let unknown = false;
      for (const span of variable.spans || []) {
        const covers = spanCovers(span, context);
        if (covers === null) { unknown = true; break; }
        if (covers) {
          held[key] = span.withheld ? null : span.option;
          decided = true;
          break;
        }
      }
      if (decided) continue;
      held[key] = !unknown && variable.default && context && typeof context.date === 'string'
        ? variable.default : null;
    }
    return held;
  }

  function conditionsResolve(element, selected, predicates, appointed) {
    let unresolved = null;
    const appointments = appointed || {};
    for (const condition of element.conditions || []) {
      if (condition.kind === 'appointed' || condition.kind === 'unappointed') {
        const value = Object.prototype.hasOwnProperty.call(appointments, condition.variable)
          ? appointments[condition.variable] : null;
        if (condition.kind === 'unappointed') {
          if (value !== null) return { show: false, unresolved: null };
          continue;
        }
        if (value === null) {
          if (condition.or_unappointed === true) continue;
          // Where the file stands a typed "appointment not established"
          // element in the appointed place, that element carries the open
          // state once; every option's row is then simply not shown, rather
          // than reported again as a separate unresolved element.
          if (appointments.__standIns && appointments.__standIns.has(condition.variable)) {
            return { show: false, unresolved: null };
          }
          unresolved = unresolved || condition;
          continue;
        }
        if ((condition.options || []).indexOf(value) < 0) {
          return { show: false, unresolved: null };
        }
      } else if (condition.kind === 'include-when-any') {
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

  function conditionsShow(element, selected, predicates, appointed) {
    return conditionsResolve(element, selected, predicates, appointed).show;
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

  function elementResolution(element, file, selected, predicates, appointed) {
    if (!alternativeShows(element, file, selected)) {
      return { show: false, unresolved: null };
    }
    return conditionsResolve(element, selected, predicates, appointed);
  }

  function appointedIn(file, predicates) {
    const context = predicates && predicates['appointment-context'];
    const held = appointmentsFor(file, context && typeof context === 'object' ? context : null);
    const standIns = new Set();
    for (const section of (file && file.sections) || []) {
      for (const element of section.elements || []) {
        for (const condition of element.conditions || []) {
          if (condition.kind === 'unappointed') standIns.add(condition.variable);
        }
      }
    }
    Object.defineProperty(held, '__standIns', { value: standIns, enumerable: false });
    return held;
  }

  function elementShows(element, file, wanted, predicates) {
    return elementResolution(
      element, file, selectionMap(file, wanted), predicates,
      appointedIn(file, predicates)).show;
  }

  function resolveElements(file, wanted, predicates) {
    const selected = selectionMap(file, wanted);
    const appointed = appointedIn(file, predicates);
    const shown = [];
    const unresolved = [];
    for (const section of file.sections || []) {
      for (const element of section.elements || []) {
        const resolution = elementResolution(
          element, file, selected, predicates, appointed);
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
    return {
      selected: selected, shown: shown, unresolved: unresolved, appointed: appointed
    };
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
        ? ['basis', 'group', 'kind', 'region']
        : disposition.kind === 'conditional' ? ['basis', 'group', 'kind', 'when'] : [];
    if (disposition.kind === 'alternative') {
      if (Object.prototype.hasOwnProperty.call(disposition, 'anchor')) wanted.push('anchor');
      if (Object.prototype.hasOwnProperty.call(disposition, 'when')) wanted.push('when');
      if (Object.prototype.hasOwnProperty.call(disposition, 'seat')) wanted.push('seat');
      wanted.sort();
    }
    if (!wanted.length || keys.length !== wanted.length ||
        keys.some((key, index) => key !== wanted[index])) {
      throw new Error('Proper ordinary_disposition carries an unsupported shape');
    }
    for (const key of wanted.filter((one) => !['kind', 'anchor', 'when'].includes(one))) {
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
    if (Object.prototype.hasOwnProperty.call(disposition, 'anchor')) {
      appointmentCoordinate(disposition.anchor);
    }
    if (Object.prototype.hasOwnProperty.call(disposition, 'seat') &&
        (!disposition.anchor || disposition.seat !== 'reading-1')) {
      throw new Error('Proper explicit seat must be reading-1 on an anchored alternative group');
    }
    if (Object.prototype.hasOwnProperty.call(disposition, 'when')) {
      appointmentWhen(disposition.when);
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

  const SEMANTIC_SLOTS = Object.freeze({
    'Introit': 'entrance-antiphon',
    'Entrance Antiphon': 'entrance-antiphon',
    'Collect': 'collect',
    'Epistle': 'reading-1',
    'First Reading': 'reading-1',
    'Gradual': 'gradual',
    'Responsorial Psalm': 'responsorial-psalm',
    'Second Reading': 'reading-2',
    'Alleluia': 'gospel-acclamation',
    'Tract': 'gospel-acclamation',
    'Gospel Acclamation': 'gospel-acclamation',
    'Gospel': 'gospel',
    'Offertory': 'offertory-chant',
    'Secret': 'prayer-over-offerings',
    'Prayer over the Offerings': 'prayer-over-offerings',
    'Communion': 'communion-antiphon',
    'Communion Antiphon': 'communion-antiphon',
    'Postcommunion': 'prayer-after-communion',
    'Prayer after Communion': 'prayer-after-communion'
  });

  function semanticProperId(proper, qualified) {
    const name = proper && proper.name || '';
    if (SEMANTIC_SLOTS[name]) return SEMANTIC_SLOTS[name];
    if (!qualified) return null;
    const family = /^(.+?) \(.+\)$/.exec(name);
    return family && SEMANTIC_SLOTS[family[1]] || null;
  }

  function validateAppointmentReplacement(proper) {
    const replacement = proper && proper.appointment_replacement;
    if (replacement === null || replacement === undefined) return;
    const source = replacement && replacement.source_group;
    const anchor = replacement && replacement.anchor;
    if (!replacement || typeof replacement !== 'object' || Array.isArray(replacement) ||
        Object.keys(replacement).sort().join(',') !== 'anchor,basis,source_group' ||
        !source || typeof source !== 'object' || Array.isArray(source) ||
        Object.keys(source).sort().join(',') !== 'form_id,id,mass' ||
        !['mass', 'form_id', 'id'].every((key) => typeof source[key] === 'string' && source[key]) ||
        !anchor || anchor.mass !== source.mass || anchor.form_id !== source.form_id ||
        typeof replacement.basis !== 'string' || !replacement.basis.trim()) {
      throw new Error('Proper replacement must retain its exact derived source group and anchor');
    }
    appointmentCoordinate(anchor);
    appointmentCoordinate(proper.appointment_identity);
    const originalSeat = semanticProperId({name: anchor.proper}, true);
    const replacementSeat = semanticProperId(proper, true);
    if (!originalSeat || !replacementSeat || originalSeat !== replacementSeat) {
      throw new Error('explicit Proper replacement has no matching established semantic seat');
    }
  }

  function appointmentCoordinate(value) {
    const keys = value && typeof value === 'object' && !Array.isArray(value)
      ? Object.keys(value).sort() : [];
    if (keys.join(',') !== 'form_id,mass,occurrence,proper' ||
        !['mass', 'form_id', 'proper'].every((key) =>
          typeof value[key] === 'string' && value[key].trim()) ||
        !Number.isInteger(value.occurrence) || value.occurrence < 1) {
      throw new Error('Proper appointment coordinate must name exact mass, form_id, proper and occurrence');
    }
    return JSON.stringify([value.mass, value.form_id, value.proper, value.occurrence]);
  }

  function appointmentWhen(value) {
    if (!value || typeof value !== 'object' || Array.isArray(value) ||
        Object.keys(value).sort().join(',') !== 'fact,in' ||
        typeof value.fact !== 'string' || !value.fact ||
        !Array.isArray(value.in) || !value.in.length ||
        value.in.some((one) => typeof one !== 'string' || !one) ||
        new Set(value.in).size !== value.in.length) {
      throw new Error('Proper appointment when must name one source fact and unique allowed values');
    }
    return value;
  }

  // Producer-derived foreign applicability is independent of held body text.
  // Preserve the row for source inspection; refuse execution in this edition.
  function appointmentApplicabilityOf(proper, calendar) {
    if (!proper || !Object.prototype.hasOwnProperty.call(proper, 'appointment_applicability')) return null;
    const marker = proper.appointment_applicability;
    const edition = /^[a-z0-9]+(?:-[a-z0-9]+)*$/;
    if (!marker || typeof marker !== 'object' || Array.isArray(marker) ||
        Object.keys(marker).sort().join(',') !== 'basis,reason,source_edition,state,target_edition' ||
        marker.state !== 'unresolved' || marker.reason !== 'foreign-source-applicability' ||
        typeof marker.source_edition !== 'string' || !edition.test(marker.source_edition) ||
        typeof marker.target_edition !== 'string' || !edition.test(marker.target_edition) ||
        marker.source_edition === marker.target_edition ||
        (calendar !== undefined && marker.target_edition !== calendar) ||
        typeof marker.basis !== 'string' || !marker.basis.trim()) {
      throw new Error('Proper appointment_applicability must retain exact unresolved foreign editions and source basis');
    }
    return marker;
  }

  function assertSupportedAppointmentApplicability(proper, calendar) {
    const marker = appointmentApplicabilityOf(proper, calendar);
    if (!marker) return;
    throw new Error('unsupported foreign-source Proper applicability from ' + marker.source_edition +
      ' in ' + marker.target_edition + '; source condition remains unresolved: ' + marker.basis);
  }

  /** Project only positive canonical owner tuples; never resolve a calendar. */
  function projectProperUsage(context) {
    const owns = (record, keys) => record && typeof record === 'object' && !Array.isArray(record) &&
      keys.every((key) => Object.prototype.hasOwnProperty.call(record, key));
    if (!owns(context, ['calendar', 'entrance', 'branch', 'readable', 'mass', 'formId']) || !context || typeof context !== 'object' || Array.isArray(context) ||
        typeof context.calendar !== 'string' || !context.calendar || context.entrance !== 'day' ||
        !context.mass || typeof context.mass !== 'object' || Array.isArray(context.mass) ||
        !owns(context.mass, ['key']) || typeof context.mass.key !== 'string' || !context.mass.key ||
        typeof context.formId !== 'string' || !context.formId) return null;
    if ('forms' in context.mass && !Object.prototype.hasOwnProperty.call(context.mass, 'forms')) return null;
    const forms = context.mass.forms;
    if (forms !== undefined && !Array.isArray(forms)) return null;
    if (!forms || !forms.length) {
      if (context.formId !== 'main') return null;
    } else {
      const matchingForms = forms.filter((form) => form && form.id === context.formId);
      if (matchingForms.length !== 1 || !owns(matchingForms[0], ['id'])) return null;
    }
    const branch = context.branch;
    const readable = context.readable;
    if (!owns(branch, ['settled', 'choiceRequired', 'choice', 'massChoices', 'unsettled', 'readable', 'candidates', 'winner']) || branch.settled !== true || branch.choiceRequired !== false || branch.choice !== null ||
        !Array.isArray(branch.massChoices) || branch.massChoices.length ||
        !Array.isArray(branch.unsettled) || branch.unsettled.length ||
        !Array.isArray(branch.readable) || !Array.isArray(branch.candidates) ||
        !owns(readable, ['state', 'id', 'key']) || readable.state !== 'said' || readable.key !== context.mass.key ||
        typeof readable.id !== 'string' || !readable.id) return null;
    const said = branch.readable.filter((one) => one && (one.state === 'said' || one.id === readable.id));
    if (said.length !== 1 || !owns(said[0], ['state', 'id', 'key']) || said[0].state !== 'said' ||
        said[0].id !== readable.id || said[0].key !== readable.key) return null;
    const winner = branch.winner;
    if (!owns(winner, ['id', 'key', 'source', 'nature', 'optional', 'formulary']) || winner.id !== readable.id || winner.optional !== false) return null;
    const candidates = branch.candidates.filter((one) => one && one.id === winner.id);
    if (candidates.length !== 1) return null;
    const candidate = candidates[0];
    if (!owns(candidate, ['id', 'key', 'source', 'nature', 'competes', 'certain', 'formulary', 'rule']) || candidate.competes !== true || candidate.certain !== true ||
        candidate.key !== winner.key || candidate.source !== winner.source || candidate.nature !== winner.nature) return null;
    if (winner.nature === 'sunday' && winner.source === 'index' &&
        winner.id === context.mass.key && winner.key === context.mass.key &&
        Object.prototype.hasOwnProperty.call(winner, 'formulary') && winner.formulary === null &&
        Object.prototype.hasOwnProperty.call(candidate, 'formulary') && candidate.formulary === null &&
        owns(candidate.rule, ['origin', 'rule']) && candidate.rule.origin === 'temporal' &&
        typeof candidate.rule.rule === 'string' && candidate.rule.rule) return 'own-sunday';
    if (winner.nature !== 'feria' || winner.source !== 'implied' || winner.key !== null) return null;
    const own = winner.formulary; const held = candidate.formulary;
    if (!owns(own, ['kind', 'key', 'known', 'rule']) || !owns(held, ['kind', 'key', 'known', 'rule']) || own.kind !== 'borrowed' || held.kind !== 'borrowed' ||
        own.key !== context.mass.key || held.key !== own.key || own.known !== true || held.known !== true ||
        !owns(own.rule, ['origin', 'rule']) || !owns(held.rule, ['origin', 'rule']) || own.rule.origin !== 'ferial' || held.rule.origin !== 'ferial' ||
        typeof own.rule.rule !== 'string' || !own.rule.rule || held.rule.rule !== own.rule.rule) return null;
    return 'borrowed-feria';
  }

  /** Source predicates consume an existing owner's season; no date is derived. */
  function prepareProperAppointments(propers, context) {
    const rows = (propers || []).map(properRow);
    const supplied = context || {};
    const choices = supplied.choices || {};
    if (!choices || typeof choices !== 'object' || Array.isArray(choices)) {
      throw new Error('Proper appointment choices must be a mapping');
    }
    const groups = new Map();
    const coordinates = new Set();
    const conditions = [];
    const conditionalGroups = new Map();
    const domains = new Map();
    const facts = supplied.facts || {};
    let usesUsage = false;
    let usage = null;
    function domainFor(when) {
      appointmentWhen(when);
      if (domains.has(when.fact)) {
        const held = domains.get(when.fact);
        if (when.in.some((value) => !held.values.includes(value))) {
          throw new Error('Proper condition names an unheld source fact value');
        }
        return held;
      }
      const fact = Object.prototype.hasOwnProperty.call(facts, when.fact) ? facts[when.fact] : undefined;
      const selectors = fact && ['season_values', 'mass_values', 'usage_values'].filter((key) =>
        Object.prototype.hasOwnProperty.call(fact, key));
      const selector = selectors && selectors.length === 1 ? selectors[0] : null;
      if (!fact || typeof fact !== 'object' || Array.isArray(fact) || !selector ||
          Object.keys(fact).sort().join(',') !== ['basis', 'edition', selector, 'values'].sort().join(',') ||
          typeof fact.edition !== 'string' || !fact.edition || fact.edition !== supplied.calendar ||
          typeof fact.basis !== 'string' || !fact.basis.trim() ||
          !Array.isArray(fact.values) || !fact.values.length ||
          fact.values.some((value) => typeof value !== 'string' || !value) ||
          new Set(fact.values).size !== fact.values.length ||
          !fact[selector] || typeof fact[selector] !== 'object' || Array.isArray(fact[selector]) ||
          !Object.keys(fact[selector]).length || Object.keys(fact[selector]).some((key) => {
            if (!key || key.trim() !== key) return true;
            const entry = fact[selector][key];
            if (selector === 'season_values') return entry !== null && !fact.values.includes(entry);
            if (selector === 'usage_values') return !['own-sunday', 'borrowed-feria'].includes(key) || !fact.values.includes(entry);
            return !entry || typeof entry !== 'object' || Array.isArray(entry) ||
              Object.keys(entry).sort().join(',') !== 'basis,value' ||
              !fact.values.includes(entry.value) || typeof entry.basis !== 'string' || !entry.basis.trim();
          })) {
        throw new Error('Proper appointment fact is unheld, malformed or belongs to another edition');
      }
      if (selector === 'usage_values' && Object.keys(fact.usage_values).sort().join(',') !== 'borrowed-feria,own-sunday') {
        throw new Error('Proper usage selector requires exactly own-sunday and borrowed-feria source bindings');
      }
      if (when.in.some((value) => !fact.values.includes(value))) {
        throw new Error('Proper condition names an unheld source fact value');
      }
      if (!['day', 'propers'].includes(supplied.entrance)) {
        throw new Error('Proper applicability requires an explicit reader entrance');
      }
      if ((supplied.date != null && (typeof supplied.date !== 'string' || !/^\d{4}-\d{2}-\d{2}$/.test(supplied.date))) ||
          (supplied.season != null && (typeof supplied.season !== 'string' || !supplied.season))) {
        throw new Error('Proper applicability requires a held owner date and season or explicit absence');
      }
      if (supplied.entrance === 'propers' && (supplied.date || supplied.season)) {
        throw new Error('date-independent Propers cannot consume a calendar season');
      }
      let value = null;
      if (selector === 'usage_values') {
        usesUsage = true;
        const evidence = Object.prototype.hasOwnProperty.call(supplied, 'usageContext') ? supplied.usageContext : undefined;
        const formIds = new Set(rows.map((row) => formIdOf(row.proper)));
        if (evidence && evidence.calendar === supplied.calendar && evidence.entrance === supplied.entrance &&
            evidence.mass && evidence.mass.key === supplied.mass && formIds.size === 1 && formIds.has(evidence.formId)) {
          usage = projectProperUsage(evidence);
        }
        if (usage !== null) value = fact.usage_values[usage];
      } else if (selector === 'mass_values') {
        if (supplied.mass != null && (typeof supplied.mass !== 'string' || !supplied.mass || supplied.mass.trim() !== supplied.mass)) {
          throw new Error('Proper applicability requires an exact validated source Mass key or explicit unknown');
        }
        if (typeof supplied.mass === 'string' && Object.prototype.hasOwnProperty.call(fact.mass_values, supplied.mass)) value = fact.mass_values[supplied.mass].value;
      } else if (supplied.entrance === 'day' && supplied.date && supplied.season) {
        if (!Object.prototype.hasOwnProperty.call(fact.season_values, supplied.season)) {
          throw new Error('Proper applicability received an unheld owner season');
        }
        value = fact.season_values[supplied.season];
      }
      const held = {values: fact.values, domain: value === null ? fact.values.slice() : [value],
        selector: selector, known: value !== null};
      domains.set(when.fact, held);
      return held;
    }
    rows.forEach((row) => {
      const proper = row.proper;
      assertSupportedAppointmentApplicability(proper, supplied.calendar);
      validateAppointmentReplacement(proper);
      if (proper && Object.prototype.hasOwnProperty.call(proper, 'appointment_identity')) {
        const coordinate = appointmentCoordinate(proper.appointment_identity);
        if (coordinates.has(coordinate)) throw new Error('duplicate Proper appointment coordinate');
        coordinates.add(coordinate);
      }
      const disposition = dispositionOf(proper);
      if (!disposition) return;
      if (disposition.when || disposition.anchor || disposition.kind === 'conditional') {
        appointmentCoordinate(proper.appointment_identity);
      }
      if (disposition.when) domainFor(disposition.when);
      if (disposition.kind === 'conditional') {
        const id = proper.appointment_identity.mass + '/' + proper.appointment_identity.form_id + '/' + disposition.group;
        const definition = JSON.stringify([disposition.basis, disposition.when]);
        if (conditionalGroups.has(id) && conditionalGroups.get(id) !== definition) {
          throw new Error('conditional Proper group must retain one source basis and condition');
        }
        conditionalGroups.set(id, definition);
        conditions.push({row, disposition});
        return;
      }
      if (disposition.kind !== 'alternative') return;
      const id = formIdOf(proper) + '/' + disposition.group;
      if (!groups.has(id)) groups.set(id, new Map());
      const options = groups.get(id);
      const prior = options.get(disposition.option);
      if (options.has(disposition.option) && JSON.stringify(prior || null) !== JSON.stringify(disposition.when || null)) {
        throw new Error('Proper option members disagree about source applicability');
      }
      options.set(disposition.option, disposition.when || null);
    });
    Object.keys(choices).forEach((id) => {
      const options = groups.get(id);
      if (!options || typeof choices[id] !== 'string' || !options.has(choices[id])) {
        throw new Error('explicit Proper choice is not held by the exact formulary and form');
      }
      const when = options.get(choices[id]);
      if (!when) return;
      const held = domainFor(when);
      const narrowed = held.domain.filter((value) => when.in.includes(value));
      if (!narrowed.length) throw new Error('explicit Proper choice contradicts source applicability');
      if (held.selector !== 'season_values' && !held.known && narrowed.length !== held.domain.length) {
        throw new Error(held.selector === 'mass_values'
          ? 'explicit Proper choice cannot establish unknown source Mass eligibility'
          : 'explicit Proper choice cannot establish unknown source use applicability');
      }
      held.domain = narrowed;
    });
    function stateOf(when) {
      if (!when) return true;
      const domain = domainFor(when).domain;
      const included = domain.filter((value) => when.in.includes(value));
      return included.length === domain.length ? true : included.length === 0 ? false : null;
    }
    const selections = {};
    groups.forEach((options, id) => {
      const conditional = Array.from(options.values()).filter(Boolean).length;
      if (conditional && conditional !== options.size) {
        throw new Error('Proper group must disposition applicability for every option');
      }
      let option = choices[id] || null;
      if (!option && conditional) {
        const applicable = Array.from(options).filter((entry) => stateOf(entry[1]) !== false);
        if (!applicable.length) throw new Error('source applicability appoints no Proper option');
        if (applicable.length === 1 && stateOf(applicable[0][1]) === true) option = applicable[0][0];
      }
      selections[id] = {state: option ? 'selected' : 'required', option};
    });
    const unresolved = [];
    const inactive = [];
    const byIndex = new Map(conditions.map((condition) => [condition.row.sourceIndex, condition]));
    const active = rows.filter((row) => {
      const condition = byIndex.get(row.sourceIndex);
      if (!condition) return true;
      const disposition = condition.disposition;
      const state = stateOf(disposition.when);
      const record = {
        kind: 'conditional-proper-appointment', group: disposition.group,
        appointment: row.proper.appointment_identity, sourceIndex: row.sourceIndex,
        basis: disposition.basis, when: disposition.when
      };
      if (state === null) unresolved.push(record);
      if (state === false) inactive.push(Object.assign({reason: 'predicate-false'}, record));
      return state === true;
    }).map((row) => {
      if (!byIndex.has(row.sourceIndex)) return row;
      const proper = Object.assign({}, row.proper);
      delete proper.ordinary_disposition;
      return {proper, sourceIndex: row.sourceIndex};
    });
    return Object.assign({rows: active, selections, unresolved, inactive}, usesUsage ? {usage: usage} : {});
  }

  /**
   * Collapse only source-authored alternative annotations.  Every source row
   * survives inside exactly one unit with its original sourceIndex; a group is
   * atomic only after all of its members independently resolve to the same
   * Ordinary slot. An explicit reading-1 qualification belongs only to this
   * anchored source group and cannot override a known native semantic role.
   * No array position selects an option.
   */
  function properUnits(propers, seating, isPlaceholder, selections) {
    const rows = (propers || []).map(properRow).filter(function (row) {
      assertSupportedAppointmentApplicability(row.proper);
      return !(isPlaceholder && isPlaceholder(row.proper));
    });
    const units = [];
    const alternativeGroups = new Set();
    const unplacedGroups = new Map();
    const anchored = new Map();
    const coordinates = new Map();
    rows.forEach((row) => {
      if (row.proper && row.proper.appointment_identity) {
        const coordinate = appointmentCoordinate(row.proper.appointment_identity);
        if (coordinates.has(coordinate)) throw new Error('duplicate Proper appointment coordinate');
        coordinates.set(coordinate, row);
      }
      const disposition = dispositionOf(row.proper);
      if (!disposition || !disposition.anchor) return;
      const id = formIdOf(row.proper) + '/' + disposition.group;
      if (!anchored.has(id)) anchored.set(id, []);
      anchored.get(id).push({proper: row.proper, sourceIndex: row.sourceIndex, option: disposition.option});
    });
    anchored.forEach((members, id) => {
      const principal = dispositionOf(members[0].proper);
      const anchor = appointmentCoordinate(principal.anchor);
      members.forEach((member) => {
        const disposition = dispositionOf(member.proper);
        const identity = member.proper.appointment_identity;
        appointmentCoordinate(identity);
        if (identity.mass !== principal.anchor.mass || identity.form_id !== principal.anchor.form_id ||
            appointmentCoordinate(disposition.anchor) !== anchor || disposition.basis !== principal.basis ||
            disposition.seat !== principal.seat) {
          throw new Error('anchored Proper group must retain one exact owner, anchor, source basis and seat qualification');
        }
      });
      if (!members.some((member) => appointmentCoordinate(member.proper.appointment_identity) === anchor)) {
        throw new Error('Proper group anchor must be an exact member of the same source group');
      }
      rows.forEach((row) => {
        const disposition = dispositionOf(row.proper);
        if (disposition && disposition.kind === 'alternative' &&
            formIdOf(row.proper) + '/' + disposition.group === id && !disposition.anchor) {
          throw new Error('anchored Proper group cannot mix anchored and contiguous members');
        }
      });
    });

    function appendChoice(members, disposition, sourceIndex) {
      const byOption = new Map();
      const formIds = new Set(members.map((member) => formIdOf(member.proper)));
      if (formIds.size !== 1) throw new Error('alternative Proper group must belong to one stable Mass form');
      members.forEach((member) => {
        if (!byOption.has(member.option)) byOption.set(member.option, []);
        const bundle = byOption.get(member.option);
        if (bundle.length && bundle[bundle.length - 1].sourceIndex >= member.sourceIndex) {
          throw new Error('Proper option bundle must preserve original source order');
        }
        bundle.push({proper: member.proper, sourceIndex: member.sourceIndex});
      });
      if (byOption.size < 2) throw new Error('alternative Proper group must carry at least two distinct options');
      if (disposition.anchor) {
        const semanticIds = new Set(members.map((member) => semanticProperId(member.proper, true)));
        const explicitSeat = disposition.seat;
        if (explicitSeat
            ? Array.from(semanticIds).some((id) => id !== null && id !== explicitSeat)
            : semanticIds.size !== 1 || semanticIds.has(null)) {
          throw new Error('anchored Proper group must share one established semantic seat');
        }
      }
      let ordinal = null;
      if (seating) members.forEach((member) => {
        const found = usableSlotOf(seating, member.proper && member.proper.name);
        if (found < 0 || (ordinal !== null && found !== ordinal)) {
          throw new Error('alternative Proper group must share one usable semantic Ordinary seat');
        }
        ordinal = found;
      });
      const formId = Array.from(formIds)[0];
      const id = formId + '/' + disposition.group;
      const selection = selections && selections[id];
      if (members.some((member) => dispositionOf(member.proper).when) && !selection) {
        throw new Error('source applicability must be prepared before Proper seating');
      }
      if (selection && (Object.keys(selection).sort().join(',') !== 'option,state' ||
          !['selected', 'required'].includes(selection.state) ||
          (selection.state === 'selected' ? !byOption.has(selection.option) : selection.option !== null))) {
        throw new Error('Proper selection does not name one exact held source option');
      }
      units.push({
        kind: 'proper_choice', group: disposition.group, basis: disposition.basis,
        formId, sourceIndex, ordinal, seat: ordinal === null ? null : seating.slots[ordinal],
        options: Array.from(byOption, (entry) => ({id: entry[0], rows: entry[1]})),
        selection: selection || {state: 'required', option: null}
      });
    }

    for (let index = 0; index < rows.length;) {
      const row = rows[index];
      const disposition = dispositionOf(row.proper);
      if (!disposition) {
        units.push({ kind: 'proper', proper: row.proper, sourceIndex: row.sourceIndex, seat: null });
        index += 1;
        continue;
      }
      if (disposition.kind === 'conditional') {
        throw new Error('conditional Proper applicability must be prepared before seating');
      }
      if (disposition.anchor) {
        if (appointmentCoordinate(row.proper.appointment_identity) === appointmentCoordinate(disposition.anchor)) {
          if (alternativeGroups.has(disposition.group) || unplacedGroups.has(disposition.group)) {
            throw new Error('Proper group cannot repeat or mix alternative and unplaced rows');
          }
          alternativeGroups.add(disposition.group);
          appendChoice(anchored.get(formIdOf(row.proper) + '/' + disposition.group), disposition, row.sourceIndex);
        }
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
      appendChoice(members, disposition, members[0].sourceIndex);
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

  function seatPropers(propers, seating, isPlaceholder, selections) {
    const before = [];
    const buckets = new Map();
    const after = [];
    let reached = -1;
    let riding = null;
    let broke = false;
    const units = properUnits(propers, seating, isPlaceholder, selections);
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

  /**
   * Static producer gate, with every source candidate conserved. This never
   * appoints a season, selects an option, or produces reading events. Predicate
   * admission uses the same owner as execution, with an explicitly unknown
   * Propers context; conditional rows then lose only that validated annotation
   * on private copies so even an inactive candidate must have a sound seat.
   * Foreign markers remain a typed limitation, never permission to execute.
   */
  function validateProperSeating(file, propers, context) {
    const supplied = context || {};
    if (!file || supplied.calendar !== file.calendar ||
        typeof supplied.form_id !== 'string' || !supplied.form_id ||
        typeof supplied.mass !== 'string' || !supplied.mass ||
        typeof supplied.full !== 'boolean' || !Array.isArray(propers) ||
        propers.some((proper) => !proper || typeof proper !== 'object' ||
          Array.isArray(proper) || typeof proper.name !== 'string' || !proper.name)) {
      throw new Error('static Proper seating requires exact calendar, Mass, form, frame and candidate rows');
    }
    const foreign = new Set();
    const placeholders = new Set();
    const diagnostics = [];
    const copies = propers.map((proper, sourceIndex) => {
      const copy = Object.assign({}, proper);
      const marker = appointmentApplicabilityOf(proper, supplied.calendar);
      if (marker) {
        foreign.add(sourceIndex);
        diagnostics.push({kind: 'unsupported-foreign-source-applicability', sourceIndex,
          source_edition: marker.source_edition, target_edition: marker.target_edition});
        delete copy.appointment_applicability;
      }
      if (proper.name === 'Placeholder' && !marker && !proper.ordinary_disposition) placeholders.add(copy);
      return copy;
    });
    const prepared = prepareProperAppointments(copies, {
      calendar: supplied.calendar, entrance: 'propers', date: null, season: null,
      mass: supplied.mass,
      facts: supplied.facts || {}, choices: {}
    });
    let conditionalRows = 0;
    copies.forEach((proper) => {
      const disposition = dispositionOf(proper);
      if (disposition && disposition.kind === 'conditional') {
        conditionalRows += 1;
        delete proper.ordinary_disposition;
      }
    });
    const shown = (file.sections || []).flatMap((section) =>
      (section.elements || []).map((element) => ({section, element})));
    const seating = supplied.full ? seats(file, shown) : null;
    const units = properUnits(copies, seating, (proper) => placeholders.has(proper), prepared.selections);
    let reached = -1;
    let candidates = 0;
    let choices = 0;
    units.forEach((unit) => {
      const members = unit.kind === 'proper_choice'
        ? unit.options.flatMap((option) => option.rows) : [unit];
      candidates += members.length;
      if (unit.kind === 'proper_choice') choices += 1;
      if (!supplied.full || (unit.kind === 'proper' && unit.seat && unit.seat.region)) return;
      const ordinal = unit.kind === 'proper_choice'
        ? unit.ordinal : usableSlotOf(seating, unit.proper.name);
      if (ordinal < 0) {
        const name = unit.kind === 'proper' ? unit.proper.name : null;
        const qualifier = name && QUALIFIER.exec(name);
        const declared = name !== null && (file.slots || []).some((slot) =>
          (slot.propers || []).some((claim) => claim === name ||
            (slot.qualified && qualifier && claim === qualifier[1])));
        // Only an undeclared foreign standalone label has an unknown target
        // seat. A declared slot with a broken anchor still fails, and choice
        // groups retain the unchanged framed guard above.
        if (unit.kind === 'proper' && foreign.has(unit.sourceIndex) && !declared) {
          diagnostics.find((one) => one.sourceIndex === unit.sourceIndex).target_seat = {
            state: 'unknown', reason: 'not-declared-in-target-ordinary'
          };
          return;
        }
        throw new Error('static Proper candidate has no usable Ordinary seat');
      }
      // The foreign producer retains raw diagnostic order after stripping
      // target-inapplicable appointments. Its execution sequence is unknown.
      if (members.some((member) => foreign.has(member.sourceIndex))) return;
      if (ordinal < reached) throw new Error('static Proper candidate runs backward through Ordinary slots');
      reached = ordinal;
    });
    return {candidates, conditional_rows: conditionalRows, choice_groups: choices, diagnostics};
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
          selection: row.selection,
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
  function unframedEvents(propers, isPlaceholder, selections) {
    return properUnits(propers, null, isPlaceholder, selections).map(function (unit) {
      if (unit.kind === 'proper_choice') {
        return {
          kind: 'proper_choice', group: unit.group, basis: unit.basis,
          formId: unit.formId,
          sourceIndex: unit.sourceIndex, options: unit.options,
          selection: unit.selection,
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
    appointmentsFor: appointmentsFor,
    conditionsShow: conditionsShow,
    resolveElements: resolveElements,
    elementShows: elementShows,
    shownElements: shownElements,
    seats: seats,
    slotOf: slotOf,
    usableSlotOf: usableSlotOf,
    dispositionOf: dispositionOf,
    prepareProperAppointments: prepareProperAppointments,
    projectProperUsage: projectProperUsage,
    validateProperSeating: validateProperSeating,
    semanticProperId: semanticProperId,
    properUnits: properUnits,
    seatPropers: seatPropers,
    massEvents: massEvents,
    unframedEvents: unframedEvents
  };
}));
