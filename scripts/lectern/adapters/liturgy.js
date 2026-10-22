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

module.exports = function liturgy(realm) {
  realm.script('shared/browser-core.js');
  const T = globalThis.Triptych;
  const liturgyModel = (name) => require(path.join(realm.ROOT, 'src', 'web', 'browser', 'liturgy', name));
  const M = liturgyModel('assembly-model.js');
  const A = liturgyModel('reader-state-adapters.js');
  const S = liturgyModel('proper-search.js');

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
    const found = id ? all.find((one) => one.id === id) : all[0];
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

  async function events(result, calendar, mass, bible, state, ordinary) {
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
        out.push(Object.assign(base, {
          group: event.group, basis: event.choiceBasis || null,
          selection: event.selection || null,
          options: (event.options || []).map((option) => ({
            id: option.id,
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
    const editions = new Map((data('structure/rubrics/index.json').calendars || []).map((one) =>
      [one.id || one.calendar, one.edition_short || one.edition]));
    const recension = T.recensionContext(owner, mass, (id) => editions.get(id) || id);
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
        recension: recension ? (recension.notice || recension.text || recension) : null,
        coverage: mass.coverage ? T.coverageNoticeText(mass.coverage, state.orations,
          state.witness || null) : null,
        coverageSummary: mass.coverage ? T.coverageSummaryText(mass.coverage, state.orations,
          state.witness || null) : null,
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
    const state = Object.assign({ orations: 'la' }, options || {});
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

  async function day(calendar, iso, options) {
    const state = normal(options);
    const bible = bibleFor(state.bible);
    const derived = derive(calendar, iso);
    const ordinary = state.ordinary ? ordinaryOf(calendar) : null;
    const asked = Object.assign(request('day', calendar, state, bible), {
      civilDate: iso, calendar: { id: calendar }, apparatus: { why: false, rubrics: true },
    });
    if (state.mass) asked.selectedReadableFormulary = { id: state.mass };
    if (state.form) asked.form = state.form;
    if (state.territory) asked.calendar.territory = { id: state.territory };
    const adapted = A.adaptDay({ request: asked, derived, structure: structure(calendar), ordinary });
    const key = adapted.resolved && adapted.resolved.formulary && adapted.resolved.formulary.id ||
      (adapted.resolved && adapted.resolved.formulary) || null;
    const { mass, context } = key ? massContext(calendar, typeof key === 'string' ? key : key.id, state)
      : { mass: null, context: null };
    const result = {
      entrance: 'day', calendar, date: iso,
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
      state, mass: context, ordinary: ordinaryContext(ordinary),
    };
    common(result, adapted);
    result.events = await events(adapted, calendar, mass, bible, state, ordinary);
    return result;
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
    const result = {
      entrance: 'propers', calendar, key,
      bible: { id: bible.id, label: bible.label, language: bible.language, numbering: bible.numbering },
      state, mass: context, ordinary: ordinaryContext(ordinary),
    };
    common(result, adapted);
    result.events = await events(adapted, calendar, mass, bible, state, ordinary);
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
