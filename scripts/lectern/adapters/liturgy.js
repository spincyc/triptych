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
      ], {
        params: ['T', 'Model', 'runtime'],
        args: [T, M, runtime],
        returns: ['longDate', 'coverageMessage', 'reasoningApparatus', 'branchHeading', 'resultHeading'],
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
      advisory: rubrics.advisory || null,
      calendarAdvisory: calendar.advisory || null,
      span: calendar.span || null,
      territorial: Object.fromEntries((calendar.calendars || []).map((one) =>
        [one.calendar, one.territorial && one.territorial.note || null])),
      default: propers.default || null,
      defaultBible: C.DEFAULT_BIBLE_ID,
      defaultOrations: T.SOURCE_LANGUAGE,
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
    const fragments = mass ? await T.fetchFragments(bible, T.citationsOf(mass)) : null;
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

  function ordinaryContext(ordinary) {
    if (!ordinary) return null;
    return {
      title: ordinary.title || null, edition: ordinary.edition || null, advisory: ordinary.advisory || null,
      languages: ordinary.languages || [],
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
      options: { ordinary: wantsOrdinary, legitimate: {} },
      coverage: [], unresolvedChoices: [], sourceHooks: [],
    };
    if (wantsOrdinary) base.languages.ordinary = state.ordinaryLang || state.orations;
    if (state.witness) base.languages.translationWitness = state.witness;
    if (state.properChoices && Object.keys(state.properChoices).length) base.properChoices = state.properChoices;
    return base;
  }

  function normal(options) {
    const state = Object.assign({ orations: T.SOURCE_LANGUAGE }, options || {});
    if (!['la', 'en'].includes(state.orations)) throw new Error('orations are la or en');
    return state;
  }

  function common(result, adapted) {
    return Object.assign(result, {
      resolved: adapted.resolved || null,
      calendarResult: adapted.calendarResult || null,
      coverage: adapted.coverage || [],
      explicitAbsences: adapted.explicitAbsences || [],
      unresolvedChoices: (adapted.unresolvedChoices || []).map((one) => ({ id: one.id, reason: one.reason,
        options: (one.options || []).map((option) => ({ id: option.id, identity: option.identity || null })) })),
      ordinaryUnresolved: adapted.ordinaryUnresolved || [],
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
      state, ordinary: ordinaryContext(ordinary), rows,
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
      state, mass: context, ordinary: ordinaryContext(ordinary),
      // the page's own notice, recension first (propers-reader.js:783-795)
      notice: propersReader(editionName).coverageMessage(adapted, mass, owner) || '',
    };
    common(result, adapted);
    const probe = (id, option) => A.adaptPropers({ request: Object.assign({}, asked, {
      properChoices: Object.assign({}, asked.properChoices || {}, { [id]: option }) }),
    structure: owner, ordinary });
    result.events = await events(adapted, calendar, mass, bible, state, ordinary, probe);
    return result;
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
      })),
    };
  }

  function search(calendar, query) {
    const index = data('structure/propers/search/' + calendar + '.json');
    return S.find(index, query).map((hit) => hit.ordinal);
  }

  return { opening, month, day, propers, catalogue, search };
};
