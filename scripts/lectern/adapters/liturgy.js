'use strict';
/*
 * Today's Missal and the Propers, as the liturgy reader assembles them.
 *
 * The derivations are the browser's: `MassAssembly.derive` decides the day,
 * `LiturgyReaderStateAdapters.adaptDay` / `adaptPropers` decide what is read
 * and in what order, and `Triptych.renderProper` writes every proper with its
 * own sentences about what is absent, which witness speaks, and what a
 * passage of scripture is and is not. Nothing here ranks, seats, converts a
 * numbering or chooses among coequal options; a choice the adapter leaves
 * open is handed back open.
 */
const path = require('path');
const pages = require('./page-slice.js');

module.exports = function liturgy(realm) {
  realm.script('shared/browser-core.js');
  const T = globalThis.Triptych;
  const liturgyModel = (name) => require(path.join(realm.ROOT, 'src', 'web', 'browser', 'liturgy', name));
  const M = liturgyModel('assembly-model.js');
  const A = liturgyModel('reader-state-adapters.js');
  const S = liturgyModel('proper-search.js');
  const C = liturgyModel('reader-state.js');
  const Seating = liturgyModel('ordinary-seating.js');
  const PropersCompare = liturgyModel('propers-compare.js');
  const Study = liturgyModel('reader-study-view.js');

  /* The readers' own words, sliced out of the pages (page-slice.js): the Day
   * page's title, its coverage notice and its "Why this Mass", and the
   * Propers page's notice. `runtime` stands for the page state they read. */
  const runtime = { structure: null, ordinary: null, mode: 'read' };
  let dayPage = null;
  function dayReader() {
    if (!dayPage) {
      dayPage = pages.slicePage(realm, 'liturgy/day-reader.js', [
        ['  const MONTHS = [', '\n  ];'],
        ['  const WEEKDAY_NAMES = {', '\n  };'],
        ['  function longDate(iso, weekday) {', pages.FN],
        ['  function todayISO() {', pages.FN],
        ['  function modeLabel(mode) {', pages.FN],
        ['  function materialCoverageMessage(result) {', pages.FN],
        ['  function coverageMessage(result, detail) {', pages.FN],
        ['  function reasoningParagraph(text, locus) {', pages.FN],
        ['  function reasoningLatin(text) {', pages.FN],
        ['  const REASONING_SOURCE_WORDS = Object.freeze({', '\n  });'],
        ['  const REASONING_ORDINALS = Object.freeze(', pages.LINE],
        ['  function reasoningOrdinal(position) {', pages.FN],
        ['  function appendOrationRuleReasoning(item, oration, branch) {', pages.FN],
        ['  function appendProperReasoning(body, branch, rubrics, structure, result) {', pages.FN],
        ['  function appendOrdinaryReasoning(body, result, ordinary) {', pages.FN],
        ['  function reasoningApparatus(branch, rubrics, structure, result, ordinary) {', pages.FN],
        ['  function branchHeading(branch, ordinal) {', pages.FN],
        ['  function resultHeading(row, structure) {', pages.FN],
        ['  function locationPrefix(branch, multiple) {', pages.FN],
        ['  function nearestProperLocation(location, events) {', pages.FN],
      ], {
        params: ['T', 'Model', 'runtime'],
        args: [T, M, runtime],
        returns: ['longDate', 'todayISO', 'coverageMessage', 'reasoningApparatus', 'branchHeading', 'resultHeading', 'locationPrefix', 'nearestProperLocation'],
      });
    }
    return dayPage;
  }
  let propersPage = null;
  function propersReader(editionName) {
    if (!propersPage) {
      propersPage = pages.slicePage(realm, 'liturgy/propers-reader.js', [
        ['  function recensionContext(structure, mass) {', pages.FN],
        ['  function materialCoverageMessage(result) {', pages.FN],
        ['  function coverageMessage(result, mass, structure, detail) {', pages.FN],
      ], {
        params: ['T', 'runtime', 'editionName'],
        args: [T, runtime, editionName],
        returns: ['coverageMessage'],
      });
    }
    return propersPage;
  }

  const held = new Map();
  function data(relative) {
    if (!held.has(relative)) {
      const value = realm.read(relative);
      if (value === undefined) throw new Error(relative + ' is not published here');
      held.set(relative, value);
    }
    return held.get(relative);
  }
  const optional = (relative) => { try { return data(relative); } catch (error) { return null; } };

  function bibles() { return data('bibles.json').bibles; }
  function bibleFor(id) {
    const all = bibles();
    // The declared default, never manifest order (reader-state.js:1157-1165).
    const found = all.find((one) => one.id === (id || C.DEFAULT_BIBLE_ID));
    if (!found) throw new Error('the Bible ' + id + ' is not offered by bibles.json');
    return found;
  }
  const structure = (calendar) => data('structure/propers/' + calendar + '.json');
  const ordinaryOf = (calendar) => optional('structure/ordinary/' + calendar + '.json');

  function opening() {
    const rubrics = data('structure/rubrics/index.json');
    const calendar = data('structure/calendar/index.json');
    const propers = data('structure/propers/index.json');
    return {
      calendars: (rubrics.calendars || []).map((one) => ({
        id: one.id || one.calendar, edition: one.edition, short: one.edition_short, code: one.code,
      })),
      propersCalendars: (propers.missals || []).map((one) => ({
        id: one.id, edition: one.edition, short: one.edition_short,
      })),
      advisory: rubrics.advisory || null,
      calendarAdvisory: calendar.advisory || null,
      span: calendar.span || null,
      territorial: Object.fromEntries((calendar.calendars || []).map((one) =>
        [one.calendar, one.territorial && one.territorial.note || null])),
      default: propers.default || null,
      defaultBible: C.DEFAULT_BIBLE_ID,
      defaultOrations: T.SOURCE_LANGUAGE,
      defaultOrdinaryLanguage: 'en', // page: day-reader.js:2441; propers-reader.js:485
      bibles: bibles().map((one) => ({ id: one.id, label: one.label, language: one.language,
        numbering: one.numbering, loci: one.loci, rights: one.rights })),
    };
  }

  function year(calendar, iso) { return data('structure/calendar/' + calendar + '/' + iso.slice(0, 4) + '.json'); }
  function rubricsOf(calendar) { return data('structure/rubrics/' + calendar + '.json'); }

  function derive(calendar, iso) {
    return M.derive({ date: iso, year: year(calendar, iso), rubrics: rubricsOf(calendar) });
  }

  function branchSummary(option) {
    const winner = option.winner;
    return {
      option: option.option || null,
      settled: option.settled,
      choiceRequired: Boolean(option.choiceRequired),
      choice: option.choice || null,
      conditions: option.conditions || [],
      winner: winner ? {
        key: winner.key || null, name: winner.name, nature: winner.nature, class: winner.class || null,
        row: winner.row, rowLabel: winner.rowLabel, basisLabel: winner.basisLabel, locus: winner.locus,
        why: winner.why, optional: Boolean(winner.optional),
        formulary: winner.formulary ? { key: winner.formulary.key, kind: winner.formulary.kind,
          name: winner.formulary.name || null } : null,
      } : null,
      readable: (option.readable || []).map((one) => ({ key: one.key, label: one.label, state: one.state,
        why: one.why || null, locus: one.locus || null, disposition: one.disposition || null })),
      unsettled: (option.unsettled || []).map((one) => ({ what: one.what, why: one.why })),
      orations: option.orations || null,
      remarks: option.remarks || [],
    };
  }

  /* The month, one derive() a date: the same call the Day page makes. */
  function month(calendar, yearMonth) {
    if (!/^\d{4}-\d{2}$/.test(yearMonth)) throw new Error('a month is YYYY-MM');
    const days = [];
    for (let iso = yearMonth + '-01'; iso.slice(0, 7) === yearMonth; iso = M.shift(iso, 1)) {
      let result;
      try {
        result = derive(calendar, iso);
      } catch (error) {
        days.push({ date: iso, refused: String(error.message || error) });
        continue;
      }
      days.push({
        date: iso, season: result.season, week: result.week,
        branches: result.options.map((option) => ({
          option: option.option || null, settled: option.settled, choiceRequired: Boolean(option.choiceRequired),
          winner: option.winner ? { name: option.winner.name, nature: option.winner.nature,
            class: option.winner.class || null, rowLabel: option.winner.rowLabel } : null,
        })),
      });
    }
    return { calendar, month: yearMonth, days };
  }

  /* --- rendering one proper, as the reader renders it -------------------- */

  function sourceIndex(event) { // day-reader.js:200
    const hook = (event.sourceHooks || []).find((one) => one.kind === 'proper-structure');
    const match = hook && /\/(\d{3})$/.exec(hook.id);
    return match ? Number(match[1]) - 1 : null;
  }

  function renderedProper(event, mass, owner, bible, fragments, state) { // day-reader.js:1834
    const index = sourceIndex(event);
    const proper = index === null ? null : (mass.propers || [])[index];
    if (!proper) return { blocks: [], problem: 'no published proper stands at ' + event.id };
    if (T.isPlaceholder(proper)) return { blocks: [], placeholder: true };
    const section = T.renderProper(proper, bible, fragments, {
      numbering: owner.numbering || null,
      orations: state.orations,
      textDisplay: state.textDisplay || 'selected',
      translationWitness: state.witness || null,
      heading: 'h3',
      cycle: event.selected && event.selected.cycle || null,
      orationGroups: event.orationGroups || null, executionSource: event.executionSource || null, orationContext: event.orationContext || null, eventId: event.id, structure: owner,
    });
    return { blocks: realm.dom.read(section) };
  }

  function seat(event) {
    const one = event.seat;
    return one ? { id: one.id || null, anchor: one.anchor || null, where: one.where || null,
      locus: one.locus || null, placement: one.placement || null, region: one.region || null,
      basis: one.basis || null } : null;
  }

  function elementIndex(ordinary) {
    const found = new Map();
    for (const section of (ordinary && ordinary.sections) || []) {
      for (const element of section.elements || []) found.set(element.key, element);
    }
    return found;
  }

  /* The very selected Ordinary witness, set by the same owner as the page. */
  function renderedOrdinary(element, selected, ordinary, state) {
    if (!element) return [];
    realm.script('liturgy/ordinary-seating.js');
    globalThis.LiturgyReaderStateAdapters = A;
    // day.js exports its production presenter before its absent-control guard.
    realm.script('liturgy/day.js');
    const renderer = globalThis.TriptychOrdinaryRenderer;
    renderer.configure({ ordinaryLang: selected.language || state.ordinaryLang || state.orations,
      textDisplay: state.textDisplay || 'selected', variants: state.variants || {}, why: false });
    if (state.textDisplay === 'latin-and-selected') {
      return realm.dom.read(renderer.renderElement(element, ordinary));
    }
    const held = selected.availability === 'held' && (element.translations || []).find((row) =>
      row.lang === selected.language && row.text === selected.text &&
      (row.source_id || row.source || null) === (selected.sourceId || null));
    return realm.dom.read(renderer.renderElement(element, ordinary, {
      language: selected.language, held: held || null, selected: selected,
    }));
  }

  /* A proper choice as source-choice-controls.js presents it: its title, its
   * note, and each option by name, marked where adapting it fails. */
  function properChoice(event, probe) {
    const selected = event.selection && event.selection.option || null;
    return {
      title: 'Source Proper choice: ' + T.titleCase(String(event.group).replace(/[-_]+/g, ' ')),
      note: selected // source-choice-controls.js:54-56
        ? 'The selected source option is shown first. Other source options remain collapsed and are not cumulative.'
        : 'The source appoints one of these alternatives here. None is selected; the option groups below are not cumulative.',
      options: (event.options || []).map((option) => {
        let unavailable = false;
        try { if (probe) probe(event.id, option.id); } catch (error) { unavailable = true; }
        return { id: option.id, label: T.titleCase(String(option.id).replace(/[-_]+/g, ' ')), unavailable };
      }),
    };
  }

  async function events(result, calendar, mass, bible, state, ordinary, probe) {
    const owner = structure(calendar);
    const fragments = mass ? await T.fetchFragments(bible, T.citationsOf(mass), state, bibles()) : null;
    const elements = elementIndex(ordinary);
    const sections = new Map(((ordinary && ordinary.sections) || []).map((one) => [one.key, one]));
    const out = [];
    for (const event of result.events || []) {
      const base = { id: event.id, kind: event.kind, slot: event.editionSlotLabel || null, seat: seat(event),
        selected: event.selected ? { kind: event.selected.kind, availability: event.selected.availability || null,
          cycle: event.selected.cycle || null,
          cycles: (event.selected.alternatives || []).map((one) => one.cycle).filter(Boolean) } : null };
      if (event.kind === 'proper') {
        out.push(Object.assign(base, renderedProper(event, mass, owner, bible, fragments, state)));
      } else if (event.kind === 'proper-choice') {
        const presented = properChoice(event, probe);
        out.push(Object.assign(base, {
          group: event.group, basis: event.choiceBasis || null,
          selection: event.selection || null, title: presented.title, note: presented.note,
          options: (event.options || []).map((option, index) => Object.assign({}, presented.options[index], {
            members: (option.events || []).map((member) =>
              Object.assign({ id: member.id }, renderedProper(member, mass, owner, bible, fragments, state))),
          })),
        }));
      } else if (event.kind === 'ordinary-section') {
        const key = String(event.id).replace(/^ordinary-section\//, '');
        const section = sections.get(key);
        out.push(Object.assign(base, { name: section ? section.name : key }));
      } else if (event.kind === 'ordinary-element') {
        const key = String(event.id).replace(/^ordinary-element\//, '');
        const element = elements.get(key) || null;
        const selected = event.selected || {};
        out.push(Object.assign(base, {
          blocks: renderedOrdinary(element, selected, ordinary, state),
          element: element ? { key: element.key, kind: element.kind, name: element.name || null,
            speaker: element.speaker || null, latin_incipit: element.latin_incipit || null,
            locus: element.locus || null, variant: element.variant || null,
            absent: element.absent || null } : null,
          text: {
            language: selected.language || null, sourceId: selected.sourceId === undefined ? null : selected.sourceId,
            rights: selected.rights || null, relation: selected.relation || null,
            availability: selected.availability || null, absenceKey: selected.absenceKey || null,
            text: selected.text || null,
            turns: turnsOf(element, selected),
          },
        }));
      } else {
        out.push(base);
      }
    }
    return out;
  }

  /* The turns of the very translation the adapter selected, never another's. */
  function turnsOf(element, selected) {
    if (!element || !selected || !selected.language) return [];
    const match = (element.translations || []).find((one) => one.lang === selected.language &&
      (selected.sourceId === undefined || selected.sourceId === null || one.source_id === selected.sourceId));
    return match && Array.isArray(match.turns) ? match.turns : [];
  }

  function ordinaryContext(ordinary, state) {
    if (!ordinary) return null;
    return {
      title: ordinary.title || null, edition: ordinary.edition || null, advisory: ordinary.advisory || null,
      languages: ordinary.languages || [],
      variants: Seating.variantGroupsOf(ordinary),
      selection: Seating.selectionMap(ordinary, state && state.variants || {}),
      absences: (ordinary.absences || []).concat(ordinary.language_absences || []).map((one) => ({
        key: one.key, kind: one.kind || null, label: one.label || null, state: one.state || null,
        lang: one.lang || null })),
    };
  }

  function massContext(calendar, key, state) {
    const owner = structure(calendar);
    const mass = (owner.masses || []).find((one) => one.key === key) || null;
    if (!mass) return { mass: null, context: null };
    const recension = T.recensionContext(owner, mass, editionName);
    const witnesses = (owner.translations || []).map((one) => ({ lang: one.lang, source_id: one.source_id,
      label: one.label, rights: one.rights, caution: one.caution || null,
      acknowledgement: one.acknowledgement || null, held: one.held, composed: one.composed }));
    return {
      mass,
      context: {
        key: mass.key, name: mass.name, kind: mass.kind || null, season: mass.season || null,
        rank: mass.rank || null, registry: mass.registry || null,
        forms: (mass.forms || []).map((one) => ({ id: one.id, name: one.name, ordinal: one.ordinal })),
        textStatus: mass.text_status || null,
        uncompiled: T.massIsUncompiled ? Boolean(T.massIsUncompiled(mass)) : false,
        recension: recension && recension.notice || null,
        witnesses: witnesses.filter((one) => one.lang === state.orations),
        edition: owner.edition || null, editionShort: owner.edition_short || null,
        numbering: owner.numbering || null,
      },
    };
  }

  function request(entrance, calendar, state, bible) {
    const wantsOrdinary = Boolean(state.ordinary);
    const base = {
      schema: 'triptych-liturgy-reader-state/v1',
      entrance,
      edition: { id: calendar },
      bible: { id: bible.id, numbering: bible.numbering },
      languages: { orations: state.orations },
      requestedMode: wantsOrdinary ? 'missal' : 'read',
      textDisplay: state.textDisplay || 'selected',
      options: { ordinary: wantsOrdinary, legitimate: state.variants || {} },
      coverage: [], unresolvedChoices: [], sourceHooks: [],
    };
    if (wantsOrdinary) base.languages.ordinary = state.ordinaryLang || state.orations;
    if (state.witness) base.languages.translationWitness = state.witness;
    if (state.scriptureCompanion) base.scriptureCompanion = state.scriptureCompanion;
    if (state.alternative) base.alternative = { id: state.alternative };
    if (state.properChoices && Object.keys(state.properChoices).length) base.properChoices = state.properChoices;
    return base;
  }

  function normal(options) {
    const state = Object.assign({ orations: T.SOURCE_LANGUAGE }, options || {});
    if (!['la', 'en'].includes(state.orations)) throw new Error('orations are la or en');
    if (state.textDisplay && !['selected', 'latin-and-selected'].includes(state.textDisplay)) {
      throw new Error('text display is selected or latin-and-selected');
    }
    if (state.companion) {
      const companion = bibleFor(state.companion);
      if (companion.language !== T.SOURCE_LANGUAGE) throw new Error('the Scripture companion must be a held Latin Bible');
      state.scriptureCompanion = { id: companion.id, numbering: companion.numbering };
    }
    return state;
  }

  /* The same selected-Mass union the browser offers, including partial and
   * project-created witnesses. Corpus-wide manifests cannot answer this. */
  function witnessesFor(result, owner, state) {
    return T.executionWitnesses(result, T.coverageWitnesses(T.summarizeCoverage(T.selectedCoverageUnits(result, owner)), state.orations), state.orations);
  }

  /* Ask Study's production presenter to write its apparatus against semantic
   * event hosts. The terminal keeps this source-adjacent detail in a dialog;
   * no prose, coverage classification or source inference is recreated here. */
  function study(result) {
    const fragment = document.createDocumentFragment();
    // dom.js intentionally has no browser layout; these are only the event
    // identities the production Study presenter attaches its own notes to.
    const container = T.el('div');
    (result.events || []).forEach((event) => {
      const host = T.el('section');
      host.dataset.semanticEventId = event.id;
      host.dataset.semanticLocation = event.id;
      container.appendChild(host);
    });
    fragment.appendChild(container);
    return realm.dom.read(Study.attach({ result, fragment, contents: [] }).fragment);
  }

  /* Read the very source disclosure printed beside each selected Proper.
   * Study expands it; normal reading preserves the browser's closed state. */
  function translationApparatus(result, owner, state) {
    const mass = (owner.masses || []).find((one) => one.key === resolvedKey(result));
    if (!mass) return [];
    const fragment = document.createDocumentFragment();
    function append(event) {
      const index = sourceIndex(event);
      const proper = index === null ? null : (mass.propers || [])[index];
      if (!proper) return;
      const cycle = event.selected && event.selected.cycle;
      const owners = [proper].concat((cycle ? [cycle] : T.cycleKeysOf(proper)).map((key) => T.cycleOf(proper, key)));
      owners.forEach((textOwner) => {
        const selected = T.orationFor(textOwner, state.orations, state.witness || null);
        if (!selected.source && !selected.caution && !selected.notice) return;
        fragment.appendChild(T.el('h3', 'proper-name', proper.name || 'Proper'));
        fragment.appendChild(T.translationCredits(selected, { expanded: true }));
      });
    }
    (result.events || []).forEach((event) => {
      if (event.kind === 'proper') append(event);
      if (event.kind === 'proper-choice') (event.options || []).forEach((option) =>
        (option.events || []).forEach(append));
    });
    return realm.dom.read(fragment);
  }

  function studyDay(calendar, iso, options) {
    const state = normal(options);
    const bible = bibleFor(state.bible);
    const owner = structure(calendar);
    const derived = derive(calendar, iso);
    const branches = state.territory ? derived.options.filter((one) => one.option === state.territory) : derived.options;
    if (!branches.length) throw new Error('the requested territorial branch is not held');
    return branches.map((branch) => {
      const asked = Object.assign(request('day', calendar, state, bible), {
        civilDate: iso, calendar: { id: calendar },
      });
      if (branches.length > 1 || state.territory) asked.calendar.territory = { id: branch.option };
      if (state.mass) asked.selectedReadableFormulary = { id: state.mass };
      if (state.form) asked.form = state.form;
      const adapted = A.adaptDay({ request: asked, derived, structure: owner,
        ordinary: state.ordinary ? ordinaryOf(calendar) : null });
      return { option: branch.option || null,
        blocks: study(adapted).concat(translationApparatus(adapted, owner, state)) };
    });
  }

  function studyPropers(calendar, key, options) {
    const state = normal(options);
    const bible = bibleFor(state.bible);
    const asked = Object.assign(request('propers', calendar, state, bible), {
      civilDate: null, formulary: { id: key },
    });
    if (state.form) asked.form = state.form;
    if (state.cycle) asked.cycle = state.cycle;
    const owner = structure(calendar);
    const result = A.adaptPropers({ request: asked, structure: owner,
      ordinary: state.ordinary ? ordinaryOf(calendar) : null });
    return study(result).concat(translationApparatus(result, owner, state));
  }

  function common(result, adapted) {
    return Object.assign(result, {
      navigation: navigationFor(adapted),
      resolved: adapted.resolved || null,
      calendarResult: adapted.calendarResult || null,
      coverage: adapted.coverage || [],
      ...(adapted.executionSourceCoverage ? {executionSourceCoverage: adapted.executionSourceCoverage} : {}),
      explicitAbsences: adapted.explicitAbsences || [],
      unresolvedChoices: (adapted.unresolvedChoices || []).map((one) => ({ id: one.id, reason: one.reason,
        options: (one.options || []).map((option) => ({ id: option.id, identity: option.identity || null })) })),
      ordinaryUnresolved: adapted.ordinaryUnresolved || [],
    });
  }

  function navigationFor(result) {
    realm.script('liturgy/ordinary-seating.js');
    realm.script('liturgy/propers-events.js');
    realm.script('liturgy/day-compare.js');
    const events = globalThis.TriptychPropersEvents.create({
      getStructure: () => null, getOrdinary: () => null, navigate: () => {},
      sourceIndex, publicKeys: {}, legacyKeys: {},
    });
    const dayEntrance = result.entrance === 'day';
    const compare = dayEntrance ? globalThis.TriptychDayCompare : PropersCompare;
    const nearest = {};
    const maps = {};
    const backwards = {};
    const dimensions = dayEntrance ? ['recension'] : ['oration-language', 'lectionary-cycle',
      'reading-alternative', 'translation-witness', 'bible-edition'];
    for (const dimension of dimensions) {
      maps[dimension] = {};
      backwards[dimension] = {};
    }
    for (const event of result.events || []) {
      const location = { kind: 'event', id: event.id };
      nearest[event.id] = (dayEntrance ? dayReader().nearestProperLocation(location, result.events)
        : events.nearestProperLocation(location, result)).id || null;
      for (const dimension of dimensions) {
        const target = compare.compareLocation(location, result, dimension);
        maps[dimension][event.id] = target && target.id || null;
        if (target && target.id) backwards[dimension][target.id] = compare.fromCompareLocation(target, result).id || null;
      }
    }
    return { nearest, compare: maps, fromCompare: backwards };
  }

  /* The source-path control itself constructs and probes each candidate. Read
   * back its enabled choices and exact requests, rather than recreating the
   * relation's owned-choice tuple in a second consumer. */
  function sourcePathsFor(result, adapt) {
    if (!(result.sourcePathChoices || []).length) return [];
    realm.script('liturgy/source-choice-controls.js');
    const root = T.el('div');
    for (const event of result.events || []) {
      const host = T.el('section');
      host.dataset.semanticEventId = event.id;
      root.appendChild(host);
    }
    const candidates = new Map();
    globalThis.TriptychSourceChoiceControls.attachSourcePathChoices({
      T, root, result, state: result.request, prefix: '', navigate: () => {},
      adapt: (request) => {
        const next = adapt(request);
        for (const relation of result.sourcePathChoices) {
          const option = request.properChoices && request.properChoices[relation.id];
          if (option) candidates.set(relation.id + '/' + option, request.properChoices);
        }
        return next;
      },
    });
    return (result.sourcePathChoices || []).map((relation) => {
      const wrapper = root.querySelectorAll('.source-path-choice').find((node) => node.dataset.sourcePathChoice === relation.id);
      if (!wrapper) throw new Error('source reading path has no production control');
      return { id: relation.id, beforeEventId: relation.beforeEventId || null,
        selection: relation.selection, focusEventId: relation.focusEventId || null,
        blocks: realm.dom.read(wrapper), options: wrapper.querySelectorAll('input').map((radio) => ({
          id: radio.value, label: radio.parentNode.textContent, unavailable: Boolean(radio.disabled),
          properChoices: candidates.get(relation.id + '/' + radio.value) || null,
        })) };
    });
  }

  function editionName(id) {
    const row = (data('structure/rubrics/index.json').calendars || []).find((one) => (one.id || one.calendar) === id);
    return row && (row.edition || row.edition_short) || id;
  }

  function resolvedKey(adapted) {
    const formulary = adapted.resolved && adapted.resolved.formulary;
    return formulary && typeof formulary === 'object' ? formulary.id : formulary || null;
  }

  /* The page's branch heading, read back as its two lines. */
  function headingOf(page, branch, ordinal) {
    const lines = realm.dom.read(page.branchHeading(branch, ordinal).node)
      .map((block) => block.runs.map((run) => run.text).join(''));
    return { label: lines[0] || '', title: lines[1] || '' };
  }

  async function day(calendar, iso, options) {
    const state = normal(options);
    const bible = bibleFor(state.bible);
    const derived = derive(calendar, iso);
    const owner = structure(calendar);
    const ordinary = state.ordinary ? ordinaryOf(calendar) : null;
    const rubrics = rubricsOf(calendar);
    const page = dayReader();
    Object.assign(runtime, { structure: owner, ordinary, mode: state.ordinary ? 'missal' : 'read' });
    // Every held territorial branch, each read under its own territory, as the
    // page reads them (day-reader.js:1236-1243). A branch the reader names
    // narrows the reading to it.
    const named = state.territory
      ? derived.options.filter((one) => one.option === state.territory) : derived.options;
    if (state.territory && !named.length) throw new Error('no territorial branch ' + state.territory + ' holds on ' + iso);
    const multiple = named.length > 1;
    const rows = [];
    for (const [ordinal, branch] of named.entries()) {
      const asked = Object.assign(request('day', calendar, state, bible), {
        civilDate: iso, calendar: { id: calendar }, apparatus: { why: false, rubrics: true },
      });
      if (state.mass) asked.selectedReadableFormulary = { id: state.mass };
      if (state.form) asked.form = state.form;
      if (multiple || state.territory) asked.calendar.territory = { id: branch.option };
      const heading = multiple ? headingOf(page, branch, ordinal) : null;
      let adapted;
      try {
        adapted = A.adaptDay({ request: asked, derived, structure: owner, ordinary });
      } catch (error) {
        // page: day-reader.js:1251-1262
        rows.push({ option: branch.option || null, heading, branch: branchSummary(branch),
          failed: 'This territorial result cannot be rendered. ' + String(error && error.message || error) +
            ' No locality, formulary, or liturgical text was substituted.' });
        continue;
      }
      const key = resolvedKey(adapted);
      const { mass, context } = key ? massContext(calendar, key, state) : { mass: null, context: null };
      const row = {
        option: branch.option || null,
        prefix: page.locationPrefix(branch, multiple),
        heading,
        title: page.resultHeading({ branch, result: adapted }, owner),
        branch: branchSummary(branch),
        mass: context,
        // withRecensionNotice, day-reader.js:195-198
        notice: [context && context.recension, page.coverageMessage(adapted)].filter(Boolean).join(' '),
        // day-reader.js:1712-1716
        unsettled: adapted.resolved && adapted.resolved.standing === 'unresolved'
          ? (branch.unsettled || []).filter((one) => one.scope === 'oration-owner')
            .map((one) => [one.what, one.why].filter(Boolean).join(': ')) : [],
        reasoning: realm.dom.read(page.reasoningApparatus(branch, rubrics, owner, adapted, ordinary)),
      };
      common(row, adapted);
      if (context) context.witnesses = witnessesFor(adapted, owner, state);
      row.sourcePaths = sourcePathsFor(adapted, (next) => A.adaptDay({
        request: next, derived, structure: owner, ordinary,
      }));
      // properChoiceRequest, source-choice-controls.js: the same request with one choice made.
      const probe = (id, option) => A.adaptDay({ request: Object.assign({}, asked, {
        properChoices: Object.assign({}, asked.properChoices || {}, { [id]: option }) }),
      derived, structure: owner, ordinary });
      row.events = await events(adapted, calendar, mass, bible, state, ordinary, probe);
      rows.push(row);
    }
    return {
      entrance: 'day', calendar, date: iso, multiple,
      longDate: page.longDate(derived.date, derived.weekday),
      // day-reader.js:1679-1681
      title: multiple ? 'Held territorial branches' : (rows[0] && rows[0].title) || 'No day is settled here',
      day: {
        weekday: derived.weekday, season: derived.season, week: derived.week,
        edition: derived.edition, advisory: derived.advisory || null,
        dayAdvisory: derived.dayAdvisory || null, sourceAdvisory: derived.sourceAdvisory || null,
        year: derived.liturgicalYear ? { label: derived.liturgicalYear.label,
          lectionary: derived.liturgicalYear.lectionary || null,
          unresolved: derived.liturgicalYear.unresolved || [] } : null,
        branches: derived.options.map(branchSummary),
      },
      bible: { id: bible.id, label: bible.label, language: bible.language, numbering: bible.numbering },
      state, ordinary: ordinaryContext(ordinary, state), rows,
    };
  }

  async function propers(calendar, key, options) {
    const state = normal(options);
    const bible = bibleFor(state.bible);
    const owner = structure(calendar);
    const found = (owner.masses || []).find((one) => one.key === key);
    if (!found) throw new Error('no Mass ' + key + ' in ' + calendar);
    const ordinary = state.ordinary ? ordinaryOf(calendar) : null;
    const asked = Object.assign(request('propers', calendar, state, bible), {
      civilDate: null, formulary: { id: key, type: found.kind || null },
    });
    if (state.form) asked.form = state.form;
    if (state.cycle) asked.cycle = state.cycle;
    const adapted = A.adaptPropers({ request: asked, structure: owner, ordinary });
    const { mass, context } = massContext(calendar, key, state);
    Object.assign(runtime, { structure: owner, ordinary, mode: state.ordinary ? 'missal' : 'read' });
    const result = {
      entrance: 'propers', calendar, key,
      bible: { id: bible.id, label: bible.label, language: bible.language, numbering: bible.numbering },
      state, mass: context, ordinary: ordinaryContext(ordinary, state),
      // the page's own notice, recension first (propers-reader.js:783-795)
      notice: propersReader(editionName).coverageMessage(adapted, mass, owner) || '',
    };
    common(result, adapted);
    result.sourcePaths = sourcePathsFor(adapted, (next) => A.adaptPropers({ request: next, structure: owner, ordinary }));
    context.witnesses = witnessesFor(adapted, owner, state);
    result.cycles = PropersCompare.heldCycles(owner, asked);
    result.comparisonOffers = comparisonOffers(owner, asked, adapted);
    const probe = (id, option) => A.adaptPropers({ request: Object.assign({}, asked, {
      properChoices: Object.assign({}, asked.properChoices || {}, { [id]: option }) }),
    structure: owner, ordinary });
    result.events = await events(adapted, calendar, mass, bible, state, ordinary, probe);
    return result;
  }

  function comparisonOffers(owner, asked, adapted) {
    const languages = ['la'].concat((owner.coverage && owner.coverage.languages || []).map((row) => row.lang));
    return [
      { dimension: 'oration-language', label: 'Oration languages',
        options: [...new Set(languages)].map((id) => ({ id, label: T.languageName(id) })) },
      { dimension: 'lectionary-cycle', label: 'Lectionary cycles',
        options: PropersCompare.heldCycles(owner, asked).map((id) => ({ id, label: 'Cycle ' + id })) },
      { dimension: 'reading-alternative', label: 'Source reading alternatives',
        options: PropersCompare.heldAlternatives(adapted) },
      { dimension: 'translation-witness', label: 'Translation witnesses',
        options: PropersCompare.heldWitnesses(owner, asked, A, T) },
      { dimension: 'bible-edition', label: 'Bible editions',
        options: bibles().map((one) => ({ id: one.id, label: one.label })) },
    ].filter((one) => one.options.length > 1);
  }

  /* All five production Propers comparison dimensions, with both peers
   * explicitly supplied. The production builder owns selection and pairing. */
  async function comparePropers(calendar, key, options, selection) {
    const state = normal(options);
    const bible = bibleFor(state.bible);
    const owner = structure(calendar);
    const wanted = selection || {};
    const asked = Object.assign(request('propers', calendar, state, bible), {
      civilDate: null, formulary: { id: key, type: ((owner.masses || []).find((one) => one.key === key) || {}).kind || null }, requestedMode: 'compare',
      options: { ordinary: false, legitimate: {} },
    });
    delete asked.languages.ordinary;
    if (state.form) asked.form = state.form;
    if (state.cycle) asked.cycle = state.cycle;
    const initial = A.adaptPropers({ request: Object.assign({}, asked, { requestedMode: 'read' }), structure: owner });
    const offer = comparisonOffers(owner, asked, initial).find((one) => one.dimension === wanted.dimension);
    if (!offer || wanted.primary === wanted.peer ||
        ![wanted.primary, wanted.peer].every((id) => offer.options.some((one) => one.id === id))) {
      throw new Error('choose two distinct held peers for a supported Propers comparison');
    }
    const sides = [wanted.primary, wanted.peer].map((id) => ({ id, edition: { id: calendar }, formulary: { id: key } }));
    if (wanted.dimension === 'oration-language') {
      asked.languages.orations = wanted.primary;
      delete asked.languages.translationWitness;
      sides.forEach((side) => { side.languages = { orations: side.id }; });
    } else if (wanted.dimension === 'translation-witness') {
      asked.languages.translationWitness = wanted.primary;
      sides.forEach((side) => { side.languages = { orations: state.orations, translationWitness: side.id }; });
    } else if (wanted.dimension === 'lectionary-cycle') {
      asked.cycle = wanted.primary;
      delete asked.languages.translationWitness;
      sides.forEach((side) => { side.cycle = side.id; });
    } else if (wanted.dimension === 'reading-alternative') {
      asked.alternative = { id: wanted.primary };
      delete asked.languages.translationWitness;
      sides.forEach((side) => { side.alternative = { id: side.id }; });
    } else {
      asked.bible = { id: bibleFor(wanted.primary).id, numbering: bibleFor(wanted.primary).numbering };
      sides.forEach((side) => { const one = bibleFor(side.id); side.bible = { id: one.id, numbering: one.numbering }; });
    }
    asked.comparison = { dimension: wanted.dimension, anchor: { correspondingFormulary: key }, sides };
    ['liturgy/reader-state.js', 'liturgy/reader-comparison.js', 'liturgy/reader-compare-view.js'].forEach(realm.script);
    const built = await PropersCompare.build({ state: asked, structure: owner, Adapters: A,
      Comparison: globalThis.LiturgyReaderComparison, View: globalThis.LiturgyReaderCompareView,
      T, bibles: bibles(), isCurrent: () => true });
    return { title: offer.label, dimension: wanted.dimension, calendarResult: null, request: asked,
      lead: realm.dom.read(built.rendered.fragment.firstChild),
      sections: built.rendered.contents.map((one) => ({ id: one.id, label: one.label, blocks: realm.dom.read(one.element) })),
      selection: wanted, blocks: realm.dom.read(built.rendered.fragment), semantic: PropersCompare.summary(built.view) };
  }

  /* Day Compare, as day-compare.js builds it: each missal resolves the date
   * on its own calendar, and the page's comparison pairs their slots and its
   * view sets them; the terminal reads back what that view writes. */
  async function compare(primary, peer, iso, options) {
    const state = normal(options);
    ['liturgy/reader-state.js', 'liturgy/reader-comparison.js', 'liturgy/reader-compare-view.js',
      'liturgy/day-compare.js'].forEach(realm.script);
    const D = globalThis.TriptychDayCompare;
    const bible = bibleFor(state.bible);
    const missals = (data('structure/rubrics/index.json').calendars || []).map((one) =>
      ({ id: one.id || one.calendar, edition: one.edition, label: one.edition_short }));
    const derived = derive(primary, iso);
    const territories = D.territoryCodes(derived, derive(peer, iso));
    const asked = Object.assign(request('day', primary, state, bible), {
      civilDate: iso, calendar: { id: primary }, requestedMode: 'compare',
      apparatus: { why: false, rubrics: true },
      options: { ordinary: false, legitimate: {} },
      comparison: {
        dimension: 'recension',
        anchor: { civilDate: iso, territorialContext: state.territory || 'universal' },
        sides: [primary, peer].map((id) => ({ id, edition: { id }, calendar: { id } })),
      },
    });
    let built;
    try {
      built = await D.build({
        state: asked, derived, structures: { [primary]: structure(primary), [peer]: structure(peer) },
        load: (where) => Promise.resolve(data(where)), Model: M, Adapters: A, T,
        bibles: bibles(), missals, isCurrent: () => true,
      });
    } catch (error) {
      return { refused: String(error && error.message || error), territories };
    }
    const view = built.view;
    const editions = view.sides.map((side) => {
      const row = missals.find((one) => one.id === side.result.resolved.edition);
      return row && (row.edition || row.label) || side.id;
    });
    const unavailable = view.units.some((unit) => unit.sides.some((cell) => cell.status === 'text-unavailable'));
    return {
      title: 'Compare calendar results', // day-compare.js:209
      longDate: dayReader().longDate(built.derived[0].date, built.derived[0].weekday),
      // day-compare.js:219-222
      metadata: editions.join(' · ') + ' · ' + view.anchor.territorialContext + ' · ' +
        T.languageName(state.orations) + ' orations',
      // day-compare.js:224-226
      notice: unavailable
        ? 'Some appointed text is unavailable on a compared side; each unavailable slot is identified below.' : '',
      blocks: realm.dom.read(built.rendered.fragment),
      request: asked,
      lead: realm.dom.read(built.rendered.fragment.firstChild),
      sections: built.rendered.contents.map((one) => ({ id: one.id, label: one.label, blocks: realm.dom.read(one.element) })),
      territories,
    };
  }

  /* Canonical links use the same validator, URL vocabulary and serializer as
   * the website. No terminal-only query grammar is introduced. */
  async function readerUrl(entrance, calendar, anchor, options, comparison) {
    const state = normal(options);
    const bible = bibleFor(state.bible);
    let asked;
    if (comparison) {
      const built = entrance === 'day'
        ? await compare(calendar, comparison.peer, anchor, state)
        : await comparePropers(calendar, anchor, state, comparison);
      if (built.refused) throw new Error(built.refused);
      asked = built.request;
    } else {
      asked = request(entrance, calendar, state, bible);
      if (entrance === 'day') {
        if (state.territory) throw new Error('the browser Read route shows all territorial branches; this narrowed view has no equivalent URL');
        asked.civilDate = anchor;
        asked.calendar = { id: calendar };
        asked.apparatus = { why: false, rubrics: state.rubrics !== false };
        if (state.mass) asked.selectedReadableFormulary = { id: state.mass };
        if (state.form) asked.form = state.form;
        // Validation follows the same independent territorial adaptations as Day.
        const derived = derive(calendar, anchor);
        for (const branch of derived.options) {
          const branchRequest = Object.assign({}, asked, { calendar: { id: calendar } });
          if (derived.options.length > 1) branchRequest.calendar.territory = { id: branch.option };
          A.adaptDay({ request: branchRequest, derived, structure: structure(calendar),
            ordinary: state.ordinary ? ordinaryOf(calendar) : null });
        }
      } else {
        const mass = (structure(calendar).masses || []).find((one) => one.key === anchor);
        if (!mass) throw new Error('the requested formulary is not held');
        asked.civilDate = null;
        asked.formulary = { id: anchor, type: mass.kind || null };
        if (state.form) asked.form = state.form;
        if (state.cycle) asked.cycle = state.cycle;
        A.adaptPropers({ request: asked, structure: structure(calendar), ordinary: state.ordinary ? ordinaryOf(calendar) : null });
      }
    }
    if (state.location) asked.semanticLocation = { eventId: state.location };
    const checked = C.validateReaderState(asked);
    if (!checked.ok) throw new Error(checked.errors.map((one) => one.message).join('; '));
    const hash = C.serializeLegacy({ ok: true, state: asked,
      legacy: { variants: comparison ? {} : state.variants || {},
        unknown: state.urlLegacy && state.urlLegacy.unknown || [], inert: state.urlLegacy && state.urlLegacy.inert || [] } });
    return 'liturgy/' + C.CANONICAL_ROUTES[entrance].canonical + hash;
  }

  async function openReaderLink(value, currentEntrance) {
    const url = new URL(value, 'https://lectern.invalid/liturgy/' + C.CANONICAL_ROUTES[currentEntrance].canonical);
    if (url.searchParams.has('data') || url.searchParams.has('missals')) {
      throw new Error('this terminal reads the published checkout data; a custom browser data root cannot be substituted');
    }
    const basename = url.pathname.slice(url.pathname.lastIndexOf('/') + 1);
    const entrance = basename === '' && /\/liturgy\/$/.test(url.pathname) ? 'propers' : Object.keys(C.CANONICAL_ROUTES).find((key) =>
      [C.CANONICAL_ROUTES[key].canonical].concat(C.CANONICAL_ROUTES[key].legacy).includes(basename));
    if (!entrance) throw new Error('this is not a supported Day or Propers reader URL');
    const parsed = C.parseLegacy(entrance, url.hash, { variantKeys: C.URL_INVENTORY[entrance].dynamicHash });
    const calendar = parsed.recognized.missal || opening().default;
    const owner = structure(calendar);
    const ordinary = ordinaryOf(calendar);
    const derived = entrance === 'day' ? derive(calendar, parsed.recognized.date || dayReader().todayISO()) : null;
    const structures = Object.fromEntries(data('structure/propers/index.json').missals.map((one) => [one.id, structure(one.id)]));
    const context = A.validationContext({ entrance, bibles: data('bibles.json'),
      properIndex: data('structure/propers/index.json'), rubricsIndex: data('structure/rubrics/index.json'),
      ordinaryIndex: data('structure/ordinary/index.json'), structures,
      ordinaries: ordinary ? { [calendar]: ordinary } : {}, derived });
    if (entrance === 'propers' && !parsed.present.includes('mass') && !parsed.present.includes('type')) {
      if (parsed.duplicates.length || ['form', 'cycle', 'alternative', 'translation-witness', 'location']
        .some((key) => parsed.present.includes(key))) throw new Error('this explicit selection requires an exact formulary');
      const bible = bibleFor(parsed.recognized.bible);
      const orations = parsed.recognized.orations || T.SOURCE_LANGUAGE;
      if (!T.orationLanguagesOf(owner).some((one) => one.lang === orations)) throw new Error('this oration language is not held');
      const browsed = A.browseState({ parsed, missal: calendar, bible: bible.id, orations }, context);
      if (!browsed.ok) throw new Error(browsed.errors.map((one) => one.message).join('; '));
      return { entrance, intent: { calendar, bible: bible.id, orations, browse: true, replace: true,
        ordinary: browsed.state.options.ordinary, ordinaryLang: browsed.state.languages.ordinary || opening().defaultOrdinaryLanguage,
        textDisplay: browsed.state.textDisplay || 'selected', companion: browsed.state.scriptureCompanion && browsed.state.scriptureCompanion.id || '',
        urlLegacy: { unknown: browsed.legacy.unknown || [], inert: browsed.legacy.inert || [] } } };
    }
    const normalized = C.normalizeLegacy(parsed, { context, defaults: {
      missal: opening().default, bible: C.DEFAULT_BIBLE_ID, orations: T.SOURCE_LANGUAGE,
      date: derived && derived.date || null, 'ordinary-lang': opening().defaultOrdinaryLanguage,
    } });
    if (!normalized.ok) throw new Error(normalized.errors.map((one) => one.message).join('; '));
    const state = normalized.state;
    if (state.requestedMode === 'compare') {
      const preflight = entrance === 'propers' ? PropersCompare.preflight(parsed) : (function () {
        realm.script('liturgy/day-compare.js');
        return globalThis.TriptychDayCompare.preflight(parsed, opening().calendars);
      }());
      if (preflight.length) throw new Error(preflight.map((one) => one.message).join('; '));
    }
    const intent = {
      calendar: state.edition.id, bible: state.bible.id, orations: state.languages.orations,
      ordinary: state.options.ordinary, ordinaryLang: state.languages.ordinary || state.languages.orations,
      textDisplay: state.textDisplay || 'selected', companion: state.scriptureCompanion && state.scriptureCompanion.id || '',
      witness: state.languages.translationWitness || null, form: state.form || null,
      properChoices: state.properChoices || {}, variants: state.options.legitimate || {},
      cycle: state.cycle || null, alternative: state.alternative && state.alternative.id || null,
      location: state.semanticLocation && state.semanticLocation.eventId || null,
      study: state.requestedMode === 'study', replace: true,
      urlLegacy: { unknown: normalized.legacy.unknown || [], inert: normalized.legacy.inert || [] },
    };
    let locations = [];
    if (entrance === 'day') {
      intent.date = state.civilDate;
      intent.mass = state.selectedReadableFormulary && state.selectedReadableFormulary.id || null;
      intent.rubrics = state.apparatus.rubrics;
      if (state.comparison) {
        intent.comparing = true;
        intent.peer = state.comparison.sides[1].edition.id;
        intent.compare_territory = state.comparison.anchor.territorialContext;
        const compared = await compare(calendar, intent.peer, intent.date, {
          orations: intent.orations, bible: intent.bible, territory: intent.compare_territory === 'universal' ? '' : intent.compare_territory,
        });
        if (compared.refused) throw new Error(compared.refused);
        locations = compared.sections.map((one) => one.id);
      } else {
        intent.comparing = false;
        for (const branch of derived.options) {
          const branchRequest = Object.assign({}, state, { calendar: { id: calendar } });
          if (derived.options.length > 1) branchRequest.calendar.territory = { id: branch.option };
          const result = A.adaptDay({ request: branchRequest, derived, structure: owner, ordinary });
          const prefix = dayReader().locationPrefix(branch, derived.options.length > 1);
          locations.push(...result.events.map((one) => prefix + one.id));
        }
      }
    } else {
      intent.mass = state.formulary.id;
      if (state.comparison) {
        const dim = state.comparison.dimension;
        const idOf = (side) => dim === 'oration-language' ? side.languages.orations : dim === 'translation-witness'
          ? side.languages.translationWitness : dim === 'bible-edition' ? side.bible.id
            : dim === 'lectionary-cycle' ? side.cycle : side.alternative.id;
        intent.comparison = { dimension: dim, primary: idOf(state.comparison.sides[0]), peer: idOf(state.comparison.sides[1]) };
        const compared = await comparePropers(calendar, intent.mass, intent, intent.comparison);
        locations = compared.sections.map((one) => one.id);
      } else locations = A.adaptPropers({ request: state, structure: owner, ordinary }).events.map((one) => one.id);
    }
    if (intent.location && !locations.includes(intent.location)) throw new Error('the explicit semantic location is absent from this reading');
    return { entrance, intent };
  }

  /* Discovery: the published index, found and scored by the page's own search. */
  function catalogue(calendar) {
    const index = data('structure/propers/search/' + calendar + '.json');
    return {
      calendar, edition: index.edition || null, short: index.edition_short || null,
      rows: index.rows.map((row, ordinal) => ({
        ordinal, key: row.key, form_id: row.form_id, form_name: row.form_name || null, name: row.name,
        kind: row.kind, season: row.season || null, fixed_date: row.fixed_date || null,
        coverage: S.coverage(row),
        coverageCounts: (row.coverage && row.coverage.languages || []).map((one) => ({
          lang: one.lang, available: one.available, occurrences: one.occurrences,
          availability: one.availability || {},
        })),
      })),
    };
  }

  function search(calendar, query) {
    const index = data('structure/propers/search/' + calendar + '.json');
    return S.find(index, query).map((hit) => hit.ordinal);
  }

  return { opening, month, day, propers, compare, comparePropers, studyDay, studyPropers,
    readerUrl, openReaderLink, catalogue, search };
};
