/* Internal W3 Day Read/Missal candidate over production assembly, state, and renderers. */
'use strict';

(function () {
  // The normal artifact layout supplies the repository's stronger no-index
  // directive. This marker keeps the directly served review source no-index as
  // well without teaching the shared static renderer page-specific head markup.
  if (!document.querySelector('meta[name="robots"]')) {
    const robots = document.createElement('meta');
    robots.name = 'robots';
    robots.content = 'noindex, nofollow, noarchive';
    document.head.appendChild(robots);
  }

  const T = window.Triptych;
  const Model = window.MassAssembly;
  const Contract = window.LiturgyReaderState;
  const Adapters = window.LiturgyReaderStateAdapters;
  const Shell = window.TriptychReaderShell;
  const OrdinaryRenderer = window.TriptychOrdinaryRenderer;

  if (!T || !Model || !Contract || !Adapters || !Shell || !OrdinaryRenderer) {
    throw new Error('Day reader candidate requires production browser, assembly, Ordinary renderer, state, adapter, and shell modules');
  }

  const PATHS = Object.freeze({
    rubricsIndex: 'structure/rubrics/index.json',
    propersIndex: 'structure/propers/index.json',
    ordinaryIndex: 'structure/ordinary/index.json'
  });
  const MONTHS = [
    'January', 'February', 'March', 'April', 'May', 'June',
    'July', 'August', 'September', 'October', 'November', 'December'
  ];
  const WEEKDAY_NAMES = {
    sunday: 'Sunday', monday: 'Monday', tuesday: 'Tuesday', wednesday: 'Wednesday',
    thursday: 'Thursday', friday: 'Friday', saturday: 'Saturday'
  };

  const shellRoot = document.querySelector('[data-reader-shell]');
  const reading = document.getElementById('reader-document');
  const title = document.getElementById('celebration-title');
  const dateLine = document.getElementById('celebration-date');
  const metaLine = document.getElementById('celebration-meta');
  const coverageNotice = document.getElementById('coverage-notice');
  const detailsBody = document.querySelector('[data-reader-details]');
  const dateForm = document.getElementById('date-form');
  const dateInput = document.getElementById('reader-date');
  const missalSelect = document.getElementById('reader-missal');
  const bibleSelect = document.getElementById('reader-bible');
  const orationsSelect = document.getElementById('reader-orations');
  const formularyField = document.getElementById('reader-formulary-field');
  const formularySelect = document.getElementById('reader-formulary');
  const ordinaryLangField = document.getElementById('reader-ordinary-lang-field');
  const ordinaryLangSelect = document.getElementById('reader-ordinary-lang');
  const ordinaryOptionField = document.getElementById('reader-ordinary-option-field');
  const ordinaryOptionSelect = document.getElementById('reader-ordinary-option');
  const dateSurface = document.getElementById('date-surface');
  const dateStatus = dateSurface.querySelector('.surface-note');
  const dateStepButtons = Array.from(dateSurface.querySelectorAll('.date-steps button'));
  const contextLine = document.querySelector('.reader-context');
  const instrumentMode = document.querySelector('[data-instrument-mode]');
  const modeAction = document.querySelector('[data-reader-action="mode"]');
  const modeState = modeAction.querySelector('.action-state');
  const modeButtons = Array.from(document.querySelectorAll('[data-mode]'));
  const documentToken = typeof crypto !== 'undefined' && typeof crypto.randomUUID === 'function'
    ? crypto.randomUUID() : String(performance.timeOrigin) + '-' + Math.random().toString(36).slice(2);

  const cache = new Map();
  const derivations = new Map();
  const runtime = {
    manifests: null,
    normalized: null,
    result: null,
    derived: null,
    structure: null,
    ordinary: null,
    missals: [],
    bibles: [],
    branch: null,
    detailsLoaded: false,
    deferred: [],
    outcome: 'loading',
    serial: 0,
    mode: null,
    pendingLocation: null,
    pendingModeFocus: false,
    pendingFocus: null,
    modeStartedAt: null
  };

  window.dayReaderDebug = {
    candidate: true,
    shellBehavior: 'persistent',
    ready: false,
    renders: 0,
    detailsBuilds: 0,
    loads: {},
    state: null,
    semantic: null,
    deferred: [],
    legacy: null,
    outcome: 'loading',
    outcomeClass: 'loading',
    mode: null,
    error: null,
    derivations: 0,
    modeSwitches: 0,
    lastModeSwitchMs: null,
    ordinaryPresentations: 0,
    pendingNavigation: null,
    documentToken: documentToken,
    committedRender: null
  };

  function load(path) {
    if (!cache.has(path)) {
      window.dayReaderDebug.loads[path] = (window.dayReaderDebug.loads[path] || 0) + 1;
      cache.set(path, T.loadJSON(path));
    }
    return cache.get(path);
  }

  function todayISO() {
    const now = new Date();
    return [
      now.getFullYear(),
      String(now.getMonth() + 1).padStart(2, '0'),
      String(now.getDate()).padStart(2, '0')
    ].join('-');
  }

  function longDate(iso, weekday) {
    const parts = String(iso).split('-');
    return (WEEKDAY_NAMES[weekday] || '') + ' ' + Number(parts[2]) + ' ' +
      MONTHS[Number(parts[1]) - 1] + ' ' + parts[0];
  }

  function humanLanguage(code) {
    return T.languageName(code || 'la');
  }

  function missalRow(id) {
    return runtime.missals.find(function (row) { return row.id === id; }) || null;
  }

  function bibleRow(id) {
    return runtime.bibles.find(function (row) { return row.id === id; }) || null;
  }

  function sourceIndex(event) {
    const hook = (event.sourceHooks || []).find(function (one) {
      return one.kind === 'proper-structure';
    });
    const match = hook && /\/(\d{3})$/.exec(hook.id);
    return match ? Number(match[1]) - 1 : null;
  }

  function semanticProjection(result) {
    if (!result) return null;
    return {
      resolved: result.resolved,
      calendarResult: result.calendarResult,
      events: (result.events || []).map(function (event) {
        return {
          id: event.id,
          kind: event.kind,
          semanticSlot: event.semanticSlot || null,
          editionSlotLabel: event.editionSlotLabel || null,
          selected: event.selected || null,
          seat: event.seat || null,
          speaker: event.speaker || null,
          action: event.action === true,
          locus: event.locus || null,
          sourceHooks: event.sourceHooks || []
        };
      }),
      coverage: result.coverage || [],
      explicitAbsences: result.explicitAbsences || [],
      unresolvedChoices: result.unresolvedChoices || []
    };
  }

  function replaceReading(node) {
    reading.replaceChildren(node);
    reading.setAttribute('aria-busy', 'false');
    readerShell.setContents([]);
  }

  function currentDayLink() {
    const link = new URL('day.html', window.location.href);
    link.search = window.location.search;
    link.hash = window.location.hash;
    return link.href;
  }

  function limitation(titleText, message) {
    const section = T.el('section', 'candidate-limitation');
    section.appendChild(T.el('h2', null, titleText));
    section.appendChild(T.el('p', null, message));
    const paragraph = T.el('p');
    const link = T.el('a', null, 'Open this selection in the current Day reader');
    link.href = currentDayLink();
    paragraph.appendChild(link);
    section.appendChild(paragraph);
    return section;
  }

  function clearSelectionState(outcome) {
    runtime.normalized = null;
    runtime.result = null;
    runtime.derived = null;
    runtime.structure = null;
    runtime.ordinary = null;
    runtime.branch = null;
    runtime.deferred = [];
    runtime.outcome = outcome;
    runtime.mode = null;
    runtime.detailsLoaded = false;
    window.dayReaderDebug.state = null;
    window.dayReaderDebug.semantic = null;
    window.dayReaderDebug.deferred = [];
    window.dayReaderDebug.legacy = null;
    window.dayReaderDebug.outcome = outcome;
    window.dayReaderDebug.outcomeClass = outcome;
    window.dayReaderDebug.mode = null;
  }

  function renderFailure(errors, options) {
    const held = options || {};
    const outcome = held.outcome || 'invalid';
    const mode = Object.prototype.hasOwnProperty.call(held, 'mode') ? held.mode : runtime.mode;
    if (!held.preserveSelection) clearSelectionState(outcome);
    else {
      runtime.result = null;
      runtime.outcome = outcome;
      runtime.detailsLoaded = false;
      window.dayReaderDebug.semantic = null;
      window.dayReaderDebug.outcome = outcome;
    }
    commitOutcomePresentation({
      mode: mode,
      outcome: outcome,
      outcomeClass: held.outcomeClass || outcome,
      metadata: held.metadata || outcomeMetadata(mode, held.outcomeClass || outcome)
    });
    if (held.preserveSelection && runtime.normalized) populateDateSurface();
    else resetDateSurface();
    detailsBody.replaceChildren(T.el('p', 'surface-note', 'Details load when this surface is opened.'));
    const section = T.el('section', 'candidate-failure');
    section.appendChild(T.el('h2', null, held.heading || 'This explicit selection is invalid'));
    section.appendChild(T.el('p', null,
      held.explanation ||
      'The candidate rejected the explicit state and did not substitute another edition, date, Bible, language, locality, or formulary.'));
    const list = T.el('ul');
    (errors || []).forEach(function (error) {
      const label = error.path ? error.path + ': ' : '';
      list.appendChild(T.el('li', null, label + (error.message || String(error))));
    });
    section.appendChild(list);
    replaceReading(section);
    title.textContent = 'Selection unavailable';
    dateLine.textContent = '';
    coverageNotice.hidden = true;
    window.dayReaderDebug.error = (errors || []).map(function (one) {
      return { code: one.code || null, path: one.path || '', message: one.message || String(one) };
    });
  }

  function variantKeys(ordinaryIndex) {
    const keys = [];
    ((ordinaryIndex && ordinaryIndex.calendars) || []).forEach(function (row) {
      (row.variants || []).forEach(function (key) {
        if (keys.indexOf(key) < 0) keys.push(key);
      });
    });
    return keys;
  }

  function deferredState(parsed) {
    const reasons = [];
    const recognized = parsed.recognized || {};
    if (recognized.why === '1') reasons.push('the current Day reasoning apparatus');
    return reasons;
  }

  function requestedModeOf(parsed) {
    const duplicates = (parsed.duplicates || []).some(function (row) {
      return row.key === 'ordinary';
    });
    if (duplicates) return null;
    if (parsed.present.indexOf('ordinary') < 0) return 'read';
    if (parsed.recognized.ordinary === '0') return 'read';
    if (parsed.recognized.ordinary === '1') return 'missal';
    return null;
  }

  function modeLabel(mode) {
    if (mode === 'missal') return 'Missal';
    if (mode === 'read') return 'Read';
    return 'Mode unavailable';
  }

  function outcomeMetadata(mode, outcomeClass) {
    const labels = {
      loading: 'selection loading',
      invalid: 'explicit state rejected',
      deferred: 'valid state deferred',
      unresolved: 'valid state unresolved',
      unrenderable: 'valid selection unrenderable'
    };
    return ['Internal Day reader candidate', modeLabel(mode), labels[outcomeClass] || outcomeClass]
      .filter(Boolean).join(' · ');
  }

  async function loadManifests() {
    if (runtime.manifests) return runtime.manifests;
    const loaded = await Promise.all([
      T.loadBibles(),
      load(PATHS.rubricsIndex),
      load(PATHS.propersIndex),
      load(PATHS.ordinaryIndex)
    ]);
    if (!loaded[0].ok) throw new Error(loaded[0].message);
    runtime.bibles = loaded[0].bibles;
    runtime.missals = ((loaded[1] && loaded[1].calendars) || []).map(function (row) {
      return {
        id: row.calendar,
        label: row.edition_short || row.edition || T.titleCase(row.calendar),
        edition: row.edition || null,
        code: row.code || null
      };
    });
    runtime.manifests = {
      bibles: { bibles: runtime.bibles },
      rubricsIndex: loaded[1],
      propersIndex: loaded[2],
      ordinaryIndex: loaded[3]
    };
    return runtime.manifests;
  }

  async function validateExplicitVariants(parsed, manifests, selectedMissal) {
    const present = (parsed.variantKeys || []).filter(function (key) {
      return parsed.present.indexOf(key) >= 0;
    });
    if (!present.length) return [];
    const calendar = ((manifests.ordinaryIndex && manifests.ordinaryIndex.calendars) || [])
      .find(function (row) { return row.calendar === selectedMissal; });
    const structures = calendar
      ? [await load('structure/ordinary/' + selectedMissal + '.json')]
      : [];
    const allowed = {};
    structures.forEach(function (structure) {
      (structure.variants || []).forEach(function (group) {
        if (!allowed[group.group]) allowed[group.group] = [];
        (group.options || []).forEach(function (option) {
          if (allowed[group.group].indexOf(option.id) < 0) allowed[group.group].push(option.id);
        });
      });
    });
    const errors = [];
    present.forEach(function (key) {
      if (!allowed[key] || allowed[key].indexOf(parsed.recognized[key]) < 0) {
        errors.push({
          code: 'invalid-explicit-variant', path: key,
          message: 'the explicit option is not applicable to the selected edition’s production Ordinary'
        });
      }
    });
    return errors;
  }

  function preflightSelection(parsed, manifests) {
    const wantedMissal = Object.prototype.hasOwnProperty.call(parsed.recognized, 'missal')
      ? parsed.recognized.missal : manifests.propersIndex.default;
    const wantedDate = Object.prototype.hasOwnProperty.call(parsed.recognized, 'date')
      ? parsed.recognized.date : todayISO();
    const errors = [];
    if (!runtime.missals.some(function (row) { return row.id === wantedMissal; })) {
      errors.push({ code: 'invalid-explicit-value', path: 'missal', message: 'the requested missal is not offered by the production rules index' });
    }
    if (!Contract.strictDate(wantedDate)) {
      errors.push({ code: 'invalid-explicit-value', path: 'date', message: 'the requested date is not a real YYYY-MM-DD civil date' });
    }
    return { ok: errors.length === 0, missal: wantedMissal, date: wantedDate, errors: errors };
  }

  async function assemble(parsed, manifests, preliminary) {
    const missal = preliminary.missal;
    const year = preliminary.date.slice(0, 4);
    const needsOrdinary = parsed.present.indexOf('ordinary-lang') >= 0 ||
      parsed.recognized.ordinary === '1' ||
      (parsed.variantKeys || []).some(function (key) { return parsed.present.indexOf(key) >= 0; });
    const paths = [
      'structure/rubrics/' + missal + '.json',
      'structure/calendar/' + missal + '/' + year + '.json',
      'structure/propers/' + missal + '.json'
    ];
    if (needsOrdinary) paths.push('structure/ordinary/' + missal + '.json');
    const rows = await Promise.all(paths.map(load));
    const derivationKey = missal + '/' + preliminary.date;
    let derived = derivations.get(derivationKey);
    if (!derived) {
      derived = Model.derive({ date: preliminary.date, rubrics: rows[0], year: rows[1] });
      derivations.set(derivationKey, derived);
      window.dayReaderDebug.derivations += 1;
    }
    const structures = {};
    structures[missal] = rows[2];
    const ordinaries = {};
    if (rows[3]) ordinaries[missal] = rows[3];
    const context = Adapters.validationContext({
      entrance: 'day',
      bibles: manifests.bibles,
      rubricsIndex: manifests.rubricsIndex,
      properIndex: manifests.propersIndex,
      ordinaryIndex: manifests.ordinaryIndex,
      structures: structures,
      ordinaries: ordinaries,
      derived: derived
    });
    return { derived: derived, structure: rows[2], ordinary: rows[3] || null, context: context };
  }

  function setDateSurfaceEnabled(enabled) {
    [dateInput, missalSelect, bibleSelect, orationsSelect, formularySelect,
      ordinaryLangSelect, ordinaryOptionSelect].forEach(function (control) {
      control.disabled = !enabled;
    });
    dateForm.querySelector('.surface-apply').disabled = !enabled;
    dateStepButtons.forEach(function (button) { button.disabled = !enabled; });
  }

  function resetDateSurface() {
    dateInput.value = '';
    [missalSelect, bibleSelect, orationsSelect, formularySelect,
      ordinaryLangSelect, ordinaryOptionSelect].forEach(function (select) {
      select.replaceChildren();
    });
    formularyField.hidden = true;
    ordinaryLangField.hidden = true;
    ordinaryOptionField.hidden = true;
    dateStatus.textContent = 'No validated selection is available for the current candidate outcome.';
    setDateSurfaceEnabled(false);
  }

  function populateDateSurface() {
    const state = runtime.normalized && runtime.normalized.state;
    if (!state || !runtime.structure) {
      resetDateSurface();
      return;
    }
    T.fillSelect(missalSelect, runtime.missals.map(function (row) {
      return { value: row.id, label: row.label, title: row.edition || row.code || row.id };
    }));
    T.fillBibleSelect(bibleSelect, runtime.bibles);
    dateInput.value = state.civilDate;
    missalSelect.value = state.edition.id;
    bibleSelect.value = state.bible.id;
    const languages = T.orationLanguagesOf(runtime.structure);
    T.fillSelect(orationsSelect, languages.map(function (entry) {
      return { value: entry.lang, label: T.orationLanguageLabel(entry), title: entry.lang };
    }));
    orationsSelect.value = state.languages.orations;
    const readable = (runtime.branch && runtime.branch.readable) || [];
    if (readable.length > 1) {
      T.fillSelect(formularySelect, readable.map(function (row) {
        return { value: row.key, label: (row.label || row.key) + ' — ' + row.state };
      }));
      formularySelect.value = state.selectedReadableFormulary
        ? state.selectedReadableFormulary.id
        : (runtime.result && runtime.result.resolved && runtime.result.resolved.formulary) || '';
      formularyField.hidden = false;
    } else {
      formularyField.hidden = true;
      formularySelect.replaceChildren();
    }
    if (runtime.mode === 'missal' && runtime.ordinary) {
      const languages = runtime.ordinary.languages || [];
      T.fillSelect(ordinaryLangSelect, languages.map(function (row) {
        return {
          value: row.lang,
          label: humanLanguage(row.lang) + (row.held ? ' — ' + row.held + ' of ' + row.elements : ' — none held')
        };
      }));
      ordinaryLangSelect.value = state.languages.ordinary || 'en';
      ordinaryLangField.hidden = languages.length < 2;
      const group = window.OrdinarySeating.variantGroupOf(runtime.ordinary);
      if (group) {
        T.fillSelect(ordinaryOptionSelect, (group.options || []).map(function (option) {
          return { value: option.id, label: option.name };
        }));
        const wanted = state.options && state.options.legitimate && state.options.legitimate[group.group];
        const chosen = window.OrdinarySeating.chosenOption(group, wanted);
        if (chosen) ordinaryOptionSelect.value = chosen.id;
        ordinaryOptionField.hidden = false;
      } else {
        ordinaryOptionField.hidden = true;
      }
    } else {
      ordinaryLangField.hidden = true;
      ordinaryOptionField.hidden = true;
    }
    if (runtime.outcome === 'territorial-choice') {
      dateStatus.textContent = 'Locality is unresolved: a territorial choice is required and no branch has been selected.';
    } else if (runtime.outcome === 'deferred') {
      dateStatus.textContent = 'These validated values are preserved, but the active deferred request is not rendered in this candidate.';
    } else if (runtime.outcome === 'unresolved') {
      dateStatus.textContent = 'These validated values are current, but the formulary outcome remains unresolved.';
    } else {
      dateStatus.textContent = 'Locality is never inferred. Dates requiring an explicit territorial branch remain on the current Day page until that state is represented by the shared URL contract.';
    }
    setDateSurfaceEnabled(true);
  }

  function definitionList(rows) {
    const list = T.el('dl', 'details-list');
    rows.forEach(function (row) {
      if (row[1] === null || row[1] === undefined || row[1] === '') return;
      list.appendChild(T.el('dt', null, row[0]));
      list.appendChild(T.el('dd', row[2] || null, String(row[1])));
    });
    return list;
  }

  function populateDetails() {
    if (runtime.detailsLoaded) return;
    detailsBody.replaceChildren();
    const state = runtime.normalized && runtime.normalized.state;
    if (!state) {
      detailsBody.appendChild(T.el('p', 'surface-note',
        'No validated selection is available for the current ' + runtime.outcome + ' outcome.'));
      if (window.dayReaderDebug.error && window.dayReaderDebug.error.length) {
        const errors = T.el('ul');
        window.dayReaderDebug.error.forEach(function (error) {
          errors.appendChild(T.el('li', null, error.message));
        });
        detailsBody.appendChild(errors);
      }
      runtime.detailsLoaded = true;
      window.dayReaderDebug.detailsBuilds += 1;
      return;
    }
    const missal = missalRow(state.edition.id);
    const bible = bibleRow(state.bible.id);
    const selection = T.el('section', 'details-section');
    selection.appendChild(T.el('h3', null, 'Selection'));
    selection.appendChild(definitionList([
      ['Date', state.civilDate],
      ['Missal', missal && (missal.edition || missal.label) || state.edition.id],
      ['Locality', runtime.branch
        ? (runtime.branch.option || 'Universal')
        : (runtime.outcome === 'territorial-choice' ? 'Choice required' : 'Not selected')],
      ['Bible', bible && bible.label || state.bible.id],
      ['Orations', humanLanguage(state.languages.orations)],
      ['Mode', modeLabel(runtime.mode)],
      ['Ordinary language', runtime.mode === 'missal'
        ? humanLanguage(state.languages.ordinary || 'en') : null],
      ['Ordinary option', runtime.mode === 'missal'
        ? selectedOrdinaryOptionLabel(state, runtime.ordinary) : null],
      ['Formulary', runtime.result && runtime.result.resolved && runtime.result.resolved.formulary]
    ]));
    detailsBody.appendChild(selection);

    if (runtime.outcome === 'ready' && runtime.result && runtime.result.resolved) {
      const calendar = T.el('section', 'details-section');
      calendar.appendChild(T.el('h3', null, 'Resolved Day result'));
      const winner = runtime.branch && runtime.branch.winner;
      calendar.appendChild(definitionList([
        ['Celebration', winner && winner.name],
        ['Rank', winner && (winner.rank || winner.class || winner.grade)],
        ['Color', winner && winner.color],
        ['Season', runtime.derived && runtime.derived.season && T.titleCase(runtime.derived.season)],
        ['Standing', runtime.result.resolved && runtime.result.resolved.standing]
      ]));
      detailsBody.appendChild(calendar);
    } else if (runtime.outcome !== 'ready') {
      const outcome = T.el('section', 'details-section');
      outcome.appendChild(T.el('h3', null, 'Candidate outcome'));
      const messages = {
        deferred: 'An active request is valid and preserved, but remains deferred by this candidate.',
        'territorial-choice': 'A territorial choice is required; no locality has been selected.',
        unresolved: 'The current request is validated, but no formulary outcome has been selected.',
        unrenderable: 'The current request is valid, but its semantic document cannot be rendered from the available production resources.'
      };
      outcome.appendChild(T.el('p', 'surface-note', messages[runtime.outcome] || 'This selection is not resolved.'));
      detailsBody.appendChild(outcome);
    }
    runtime.detailsLoaded = true;
    window.dayReaderDebug.detailsBuilds += 1;
  }

  const readerShell = Shell.create({
    root: shellRoot,
    reading: reading,
    beforeOpen: function (name) {
      if (name === 'details') populateDetails();
      if (name === 'date') populateDateSurface();
    }
  });

  function selectedOrdinaryOptionLabel(state, ordinary) {
    const group = ordinary && window.OrdinarySeating.variantGroupOf(ordinary);
    if (!group) return state && state.edition && state.edition.id === 'roman-1962'
      ? 'Roman Canon' : null;
    const wanted = state.options && state.options.legitimate &&
      state.options.legitimate[group.group];
    const chosen = window.OrdinarySeating.chosenOption(group, wanted);
    return chosen ? group.name + ': ' + chosen.name : group.name + ': choice unresolved';
  }

  function commitOutcomePresentation(presentation) {
    const held = presentation || {};
    const mode = held.mode === 'read' || held.mode === 'missal' ? held.mode : null;
    runtime.mode = mode;
    runtime.outcome = held.outcome || runtime.outcome;
    window.dayReaderDebug.mode = mode;
    window.dayReaderDebug.outcome = runtime.outcome;
    window.dayReaderDebug.outcomeClass = held.outcomeClass || runtime.outcome;
    shellRoot.dataset.readerMode = mode || 'read';
    contextLine.textContent = 'Day · ' + modeLabel(mode);
    if (instrumentMode) instrumentMode.textContent = modeLabel(mode);
    modeState.textContent = mode ? modeLabel(mode) : 'Unavailable';
    modeButtons.forEach(function (button) {
      button.setAttribute('aria-checked', String(Boolean(mode) && button.dataset.mode === mode));
    });
    if (Object.prototype.hasOwnProperty.call(held, 'metadata')) {
      metaLine.textContent = held.metadata || '';
    }
    document.body.classList.toggle('hides-rubrics', Boolean(
      runtime.normalized && runtime.normalized.state.apparatus &&
      runtime.normalized.state.apparatus.rubrics === false
    ));
  }

  function coverageMessage(result) {
    const rows = (result && result.coverage) || [];
    if (rows.every(function (row) {
      return row.state === 'supported' && row.completeness === 'complete';
    }) && !(result.unresolvedChoices || []).length) return null;
    if ((result.unresolvedChoices || []).length) {
      return 'This Day result contains an unresolved choice. The candidate has not selected one silently.';
    }
    if (rows.some(function (row) { return row.state === 'unavailable'; })) {
      return 'Some appointed text is unavailable in the selected edition or language; each held portion remains identified.';
    }
    if (rows.some(function (row) { return row.state === 'unsupported'; })) {
      return 'Part of this selection is outside the candidate’s supported ' + modeLabel(runtime.mode) + ' boundary.';
    }
    if (rows.some(function (row) { return row.completeness === 'partial'; })) {
      return 'Some appointed text is not held in this repository; the available portions are shown.';
    }
    return 'This selection has a material coverage limitation.';
  }

  async function renderResult(result, structure, derived, branch, renderContext, isCurrent) {
    const state = renderContext.state;
    const mode = renderContext.mode;
    const ordinary = renderContext.ordinary;
    const mass = (structure.masses || []).find(function (row) {
      return result.resolved && row.key === result.resolved.formulary;
    });
    if (!mass) throw new Error('the validated resolved formulary is absent from production Proper data');
    const bible = bibleRow(state.bible.id);
    const fragments = await T.fetchFragments(bible, T.citationsOf(mass));
    if (!isCurrent()) return false;
    const documentFragment = document.createDocumentFragment();
    const contents = [];

    const uncompiled = T.massIsUncompiled(mass) ? T.uncompiledNote(mass) : null;
    if (mode === 'missal') {
      renderMissalDocument(
        documentFragment, contents, result, mass, structure, bible,
        fragments.fragments, state, ordinary
      );
    } else {
      (result.events || []).forEach(function (event) {
        if (event.kind !== 'proper') return;
        const index = sourceIndex(event);
        const proper = index === null ? null : (mass.propers || [])[index];
        if (!proper || T.isPlaceholder(proper)) return;
        const section = renderProperEvent(event, proper, index, structure, bible,
          fragments.fragments, state, 'h2');
        documentFragment.appendChild(section);
        contents.push({
          id: event.id,
          label: event.editionSlotLabel || proper.name || 'Proper',
          element: section,
          group: 'Proper of the Mass'
        });
      });
    }

    reading.replaceChildren(documentFragment);
    reading.setAttribute('aria-busy', 'false');
    readerShell.setContents(contents);

    const winner = branch && branch.winner;
    title.textContent = winner && winner.name || 'No day is settled here';
    dateLine.textContent = longDate(derived.date, derived.weekday);
    const missal = missalRow(state.edition.id);
    const metadata = [
      missal && (missal.edition || missal.label),
      branch && branch.option || 'Universal',
      bible && bible.label,
      humanLanguage(state.languages.orations) + ' orations'
    ];
    if (mode === 'missal') {
      metadata.push(humanLanguage(state.languages.ordinary || 'en') + ' Ordinary');
      metadata.push(selectedOrdinaryOptionLabel(state, ordinary));
    }
    commitOutcomePresentation({
      mode: mode,
      outcome: 'ready',
      outcomeClass: 'ready',
      metadata: metadata.filter(Boolean).join(' · ')
    });
    const notice = coverageMessage(result);
    if (uncompiled) {
      coverageNotice.replaceChildren(...uncompiled.childNodes);
      coverageNotice.hidden = false;
    } else {
      coverageNotice.textContent = notice || '';
      coverageNotice.hidden = !notice;
    }
    return true;
  }

  function semanticNode(node, event, ordinal) {
    node.dataset.semanticLocation = event.id;
    node.dataset.semanticEventId = event.id;
    node.tabIndex = -1;
    node.id = 'reader-event-' + String(ordinal + 1).padStart(3, '0');
    return node;
  }

  function composeInstrumentAbsences(node) {
    const notices = Array.from(node.children).filter(function (child) {
      return child.classList.contains('notice');
    });
    if (!notices.length) return node;
    const group = T.el('div', 'ordinary-absence-inline');
    node.insertBefore(group, notices[0]);
    notices.forEach(function (notice) { group.appendChild(notice); });
    return node;
  }

  function renderProperEvent(event, proper, index, structure, bible, fragments, state, heading) {
    const section = T.renderProper(proper, bible, fragments, {
      numbering: structure.numbering || null,
      orations: state.languages.orations,
      heading: heading,
      cycle: event.selected && event.selected.cycle || null
    });
    return semanticNode(section, event, index);
  }

  function renderMissalDocument(fragment, contents, result, mass, structure, bible, fragments, state, ordinary) {
    if (!ordinary) throw new Error('the selected edition has no production Ordinary to render');
    const unseated = (result.events || []).filter(function (event) {
      return event.kind === 'proper' && (!event.seat || !event.seat.id || event.seat.placement !== 'seated');
    });
    if (unseated.length) {
      throw new Error('appointed Proper has no usable semantic seat: ' +
        unseated.map(function (event) { return event.editionSlotLabel || event.id; }).join(', '));
    }
    window.dayReaderDebug.ordinaryPresentations += 1;

    OrdinaryRenderer.configure({
      ordinaryLang: state.languages.ordinary || null,
      variants: state.options && state.options.legitimate || {},
      why: false
    });

    const sections = new Map();
    const elements = new Map();
    (ordinary.sections || []).forEach(function (section) {
      sections.set(section.key, section);
      (section.elements || []).forEach(function (element) { elements.set(element.key, element); });
    });
    let optionListed = false;
    const group = window.OrdinarySeating.variantGroupOf(ordinary);
    const wantedOption = group && state.options && state.options.legitimate &&
      state.options.legitimate[group.group];
    const selectedOption = group && window.OrdinarySeating.chosenOption(group, wantedOption);
    if (group && !selectedOption) {
      throw new Error('the production Ordinary leaves ' + group.name + ' unresolved');
    }

    const ordinals = new Map((result.events || []).map(function (event, ordinal) {
      return [event.id, ordinal];
    }));
    const frame = OrdinaryRenderer.renderSemanticFrame(result.events, {
      section: function (event) {
        const ordinal = ordinals.get(event.id);
        const raw = sections.get(event.id.replace(/^ordinary-section\//, ''));
        if (!raw) throw new Error('production Ordinary section is missing for ' + event.id);
        const node = semanticNode(T.el('h2', 'mass-subheading ordinary-division', raw.name), event, ordinal);
        contents.push({ id: event.id, label: raw.name, element: node, group: 'Rites and divisions' });
        return node;
      },
      element: function (event) {
        const ordinal = ordinals.get(event.id);
        const raw = elements.get(event.id.replace(/^ordinary-element\//, ''));
        if (!raw) throw new Error('production Ordinary element is missing for ' + event.id);
        const node = semanticNode(
          composeInstrumentAbsences(OrdinaryRenderer.renderElement(raw, ordinary)),
          event,
          ordinal
        );
        if (!optionListed && group && raw.variant) {
          optionListed = true;
          const choice = renderOrdinaryChoice(group, selectedOption, event);
          contents.push({
            id: event.id,
            label: selectedOrdinaryOptionLabel(state, ordinary),
            element: node,
            group: 'Options'
          });
          const pair = document.createDocumentFragment();
          pair.appendChild(choice);
          pair.appendChild(node);
          return pair;
        }
        return node;
      },
      proper: function (event) {
        const ordinal = ordinals.get(event.id);
        const index = sourceIndex(event);
        const proper = index === null ? null : (mass.propers || [])[index];
        if (!proper || T.isPlaceholder(proper)) {
          throw new Error('semantic Proper event has no production Proper at ' + event.id);
        }
        const node = renderProperEvent(event, proper, ordinal, structure, bible, fragments, state, 'h3');
        contents.push({
          id: event.id,
          label: event.editionSlotLabel || proper.name || 'Proper',
          element: node,
          group: 'Appointed propers'
        });
        return node;
      }
    });

    const properIds = (result.events || []).filter(function (event) {
      return event.kind === 'proper';
    }).map(function (event) { return event.id; });
    if (new Set(properIds).size !== properIds.length) {
      throw new Error('the production semantic stream duplicated an appointed Proper');
    }
    fragment.appendChild(frame);
    fragment.appendChild(OrdinaryRenderer.ordinaryPreamble(ordinary));
  }

  function renderOrdinaryChoice(group, selected, event) {
    const fieldset = T.el('fieldset', 'ordinary-choice');
    fieldset.dataset.optionGroup = group.group;
    fieldset.appendChild(T.el('legend', null, group.name));
    fieldset.appendChild(T.el('p', 'ordinary-choice-note',
      'This source-defined choice belongs here in the liturgical sequence.'));
    const options = T.el('div', 'ordinary-choice-options');
    (group.options || []).forEach(function (option) {
      const label = T.el('label', 'ordinary-choice-option');
      const input = document.createElement('input');
      input.type = 'radio';
      input.name = 'reader-' + group.group;
      input.value = option.id;
      input.checked = Boolean(selected && selected.id === option.id);
      input.addEventListener('change', function () {
        if (!input.checked) return;
        const location = { kind: 'event', id: event.id };
        navigate({ ordinary: '1', [group.group]: option.id }, [], {
          location: location,
          focus: { kind: 'ordinary-option', group: group.group, option: option.id }
        });
      });
      label.appendChild(input);
      label.appendChild(document.createTextNode(option.name));
      options.appendChild(label);
    });
    fieldset.appendChild(options);
    return fieldset;
  }

  function takePendingNavigation() {
    const pending = {
      location: runtime.pendingLocation,
      modeFocus: runtime.pendingModeFocus,
      focus: runtime.pendingFocus
    };
    runtime.pendingLocation = null;
    runtime.pendingModeFocus = false;
    runtime.pendingFocus = null;
    window.dayReaderDebug.pendingNavigation = null;
    return pending;
  }

  async function renderCandidate() {
    const serial = ++runtime.serial;
    const pendingNavigation = takePendingNavigation();
    const modeStartedAt = runtime.modeStartedAt;
    runtime.modeStartedAt = null;
    const initialParsed = Contract.parseLegacy('day', window.location.hash, { variantKeys: [] });
    const requestedMode = requestedModeOf(initialParsed);
    if (readerShell.openSurface()) readerShell.close({ restoreFocus: false });
    clearSelectionState('loading');
    window.dayReaderReady = false;
    window.dayReaderDebug.ready = false;
    window.dayReaderDebug.error = null;
    window.dayReaderDebug.state = null;
    window.dayReaderDebug.semantic = null;
    window.dayReaderDebug.deferred = [];
    window.dayReaderDebug.committedRender = null;
    reading.setAttribute('aria-busy', 'true');
    reading.replaceChildren(T.el('p', 'placeholder', 'Loading Day selection…'));
    readerShell.setContents([]);
    title.textContent = 'Loading Day selection';
    dateLine.textContent = '';
    commitOutcomePresentation({
      mode: requestedMode,
      outcome: 'loading',
      outcomeClass: 'loading',
      metadata: outcomeMetadata(requestedMode, 'loading')
    });
    coverageNotice.textContent = '';
    coverageNotice.hidden = true;
    resetDateSurface();
    detailsBody.replaceChildren(T.el('p', 'surface-note', 'Details load when this surface is opened.'));

    try {
      const manifests = await loadManifests();
      if (serial !== runtime.serial) return;
      const keys = variantKeys(manifests.ordinaryIndex);
      const parsed = Contract.parseLegacy('day', window.location.hash, { variantKeys: keys });
      const preliminary = preflightSelection(parsed, manifests);
      if (!preliminary.ok) {
        renderFailure(preliminary.errors, { mode: requestedMode });
        return;
      }
      const variantErrors = await validateExplicitVariants(parsed, manifests, preliminary.missal);
      if (serial !== runtime.serial) return;
      if (variantErrors.length) {
        renderFailure(variantErrors, { mode: requestedMode });
        return;
      }
      const assembled = await assemble(parsed, manifests, preliminary);
      if (serial !== runtime.serial) return;

      const normalized = Contract.normalizeLegacy(parsed, {
        context: assembled.context,
        remembered: {},
        defaults: {
          date: preliminary.date,
          missal: preliminary.missal,
          bible: runtime.bibles[0].id,
          orations: T.SOURCE_LANGUAGE
        }
      });
      if (!normalized.ok) {
        renderFailure(normalized.errors, { mode: requestedMode });
        return;
      }
      normalized.state.requestedMode = normalized.state.options.ordinary ? 'missal' : 'read';
      const validation = Contract.validateReaderState(normalized.state);
      if (!validation.ok) {
        renderFailure(validation.errors, { mode: requestedMode });
        return;
      }
      runtime.normalized = normalized;
      runtime.derived = assembled.derived;
      runtime.structure = assembled.structure;
      runtime.ordinary = normalized.state.options.ordinary ? assembled.ordinary : null;
      runtime.mode = normalized.state.options.ordinary ? 'missal' : 'read';
      runtime.branch = assembled.derived.options.length === 1 ? assembled.derived.options[0] : null;
      runtime.deferred = deferredState(parsed);
      window.dayReaderDebug.state = normalized.state;
      window.dayReaderDebug.deferred = runtime.deferred.slice();
      window.dayReaderDebug.legacy = normalized.legacy;

      if (assembled.derived.options.length !== 1) {
        commitOutcomePresentation({
          mode: runtime.mode,
          outcome: 'territorial-choice',
          outcomeClass: 'unresolved',
          metadata: outcomeMetadata(runtime.mode, 'unresolved') + ' · locality required'
        });
        populateDateSurface();
        replaceReading(limitation(
          'Territorial branch requires the current Day reader',
          'This date resolves to more than one territorial branch, and the accepted Day legacy URL contract carries no locality key. The candidate did not choose by array order or geography.'
        ));
        title.textContent = 'Locality required';
        dateLine.textContent = longDate(assembled.derived.date, assembled.derived.weekday);
        return;
      }

      if (runtime.deferred.length) {
        commitOutcomePresentation({
          mode: runtime.mode,
          outcome: 'deferred',
          outcomeClass: 'deferred',
          metadata: outcomeMetadata(runtime.mode, 'deferred')
        });
        populateDateSurface();
        replaceReading(limitation(
          'This selection belongs to a later integration slice',
          'The candidate preserved ' + runtime.deferred.join(', ') +
            ' but did not partially render it. The unchanged current Day reader remains the faithful route for this request.'
        ));
        title.textContent = runtime.branch && runtime.branch.winner
          ? runtime.branch.winner.name : 'Deferred Day selection';
        dateLine.textContent = longDate(assembled.derived.date, assembled.derived.weekday);
        return;
      }

      let result;
      try {
        result = Adapters.adaptDay({
          request: normalized.state,
          derived: assembled.derived,
          structure: assembled.structure,
          ordinary: runtime.ordinary
        });
      } catch (error) {
        commitOutcomePresentation({
          mode: runtime.mode,
          outcome: 'unresolved',
          outcomeClass: 'unresolved',
          metadata: outcomeMetadata(runtime.mode, 'unresolved')
        });
        populateDateSurface();
        replaceReading(limitation(
          'This Day choice is not resolved by the candidate',
          String(error.message || error) + ' No formulary was selected implicitly.'
        ));
        title.textContent = runtime.branch && runtime.branch.winner
          ? runtime.branch.winner.name : 'Unresolved Day selection';
        dateLine.textContent = longDate(assembled.derived.date, assembled.derived.weekday);
        return;
      }
      runtime.result = result;
      if (!result.resolved) {
        commitOutcomePresentation({
          mode: runtime.mode,
          outcome: 'unresolved',
          outcomeClass: 'unresolved',
          metadata: outcomeMetadata(runtime.mode, 'unresolved') + ' · choice required'
        });
        populateDateSurface();
        replaceReading(limitation(
          'A formulary choice remains unresolved',
          'The production calendar result authorizes more than one choice. The candidate has preserved that state and selected none.'
        ));
        title.textContent = runtime.branch && runtime.branch.winner
          ? runtime.branch.winner.name : 'Unresolved Day selection';
        dateLine.textContent = longDate(assembled.derived.date, assembled.derived.weekday);
        return;
      }
      const renderContext = {
        state: normalized.state,
        mode: runtime.mode,
        ordinary: runtime.ordinary
      };
      let rendered;
      try {
        rendered = await renderResult(
          result, assembled.structure, assembled.derived, runtime.branch,
          renderContext,
          function () { return serial === runtime.serial; }
        );
      } catch (error) {
        if (serial !== runtime.serial) return;
        renderFailure([{ code: 'candidate-unrenderable', path: '', message: String(error.message || error) }], {
          mode: runtime.mode,
          outcome: 'unrenderable',
          outcomeClass: 'unrenderable',
          preserveSelection: true,
          heading: 'This valid Day selection cannot be rendered',
          explanation: 'The candidate stopped rather than inventing a missing resource, semantic seat, option, or liturgical text.'
        });
        return;
      }
      if (!rendered || serial !== runtime.serial) return;
      populateDateSurface();
      window.dayReaderDebug.semantic = semanticProjection(result);
      restorePendingNavigation(pendingNavigation);
      if (modeStartedAt !== null) {
        window.dayReaderDebug.lastModeSwitchMs = performance.now() - modeStartedAt;
      }
    } catch (error) {
      if (serial !== runtime.serial) return;
      renderFailure([{ code: 'candidate-load', path: '', message: String(error.message || error) }], {
        mode: requestedMode,
        outcome: 'unrenderable',
        outcomeClass: 'unrenderable',
        preserveSelection: Boolean(runtime.normalized),
        heading: 'The Day candidate could not load this selection',
        explanation: 'The requested mode is valid, but the candidate could not obtain a required production resource and did not substitute another one.'
      });
    } finally {
      if (serial === runtime.serial) {
        window.dayReaderDebug.renders += 1;
        window.dayReaderDebug.committedRender = {
          documentToken: documentToken,
          generation: window.dayReaderDebug.renders,
          serial: serial,
          href: window.location.href,
          hash: window.location.hash,
          mode: runtime.mode,
          outcome: runtime.outcome,
          outcomeClass: window.dayReaderDebug.outcomeClass
        };
        window.dayReaderDebug.ready = true;
        window.dayReaderReady = true;
      }
    }
  }

  function hashWith(updates, removals) {
    const params = new URLSearchParams(window.location.hash.replace(/^#/, ''));
    (removals || []).forEach(function (key) { params.delete(key); });
    Object.keys(updates || {}).forEach(function (key) {
      const value = updates[key];
      if (value === null || value === undefined || value === '') params.delete(key);
      else params.set(key, value);
    });
    const value = params.toString();
    return value ? '#' + value : '';
  }

  function navigate(updates, removals) {
    const navigation = arguments.length > 2 && arguments[2] || {};
    const currentLocation = readerShell.captureSemanticLocation();
    history.replaceState({ dayReaderLocation: currentLocation }, '', window.location.href);
    if (navigation.location) runtime.pendingLocation = navigation.location;
    runtime.pendingModeFocus = navigation.modeFocus === true;
    runtime.pendingFocus = navigation.focus || null;
    window.dayReaderDebug.pendingNavigation = {
      location: runtime.pendingLocation,
      modeFocus: runtime.pendingModeFocus,
      focus: runtime.pendingFocus
    };
    const hash = hashWith(updates, removals);
    history.pushState({ dayReaderLocation: runtime.pendingLocation }, '',
      window.location.pathname + window.location.search + hash);
    renderCandidate();
  }

  function nearestProperLocation(location, events) {
    if (!location || location.kind !== 'event') return location;
    if (/^proper\//.test(location.id || '')) return location;
    const rows = events || [];
    const at = rows.findIndex(function (event) { return event.id === location.id; });
    if (at < 0) return { kind: 'top', id: null };
    let best = null;
    rows.forEach(function (event, index) {
      if (event.kind !== 'proper') return;
      const distance = Math.abs(index - at);
      if (!best || distance < best.distance || (distance === best.distance && index < best.index)) {
        best = { id: event.id, distance: distance, index: index };
      }
    });
    return best ? { kind: 'event', id: best.id } : { kind: 'top', id: null };
  }

  function captureModeLocation(targetMode) {
    const location = readerShell.captureSemanticLocation();
    if (runtime.mode === 'missal' && targetMode === 'read') {
      return nearestProperLocation(location, runtime.result && runtime.result.events);
    }
    return location;
  }

  function restorePendingNavigation(pending) {
    const held = pending || {};
    let optionTarget = null;
    if (held.focus && held.focus.kind === 'ordinary-option') {
      optionTarget = Array.from(reading.querySelectorAll(
        '[data-option-group] input[type="radio"]'
      )).find(function (input) {
        const group = input.closest('[data-option-group]');
        return group && group.dataset.optionGroup === held.focus.group &&
          input.value === held.focus.option && input.checked;
      }) || null;
    }
    if (held.location) {
      const restored = readerShell.restoreSemanticLocation(held.location);
      if (!restored && optionTarget) {
        const fieldset = optionTarget.closest('[data-option-group]');
        const semantic = fieldset && fieldset.nextElementSibling;
        if (semantic && semantic.dataset.semanticLocation) {
          readerShell.restoreSemanticLocation({ kind: 'event', id: semantic.dataset.semanticLocation });
        } else readerShell.restoreSemanticLocation({ kind: 'top', id: null });
      } else if (!restored) readerShell.restoreSemanticLocation({ kind: 'top', id: null });
    }
    if (optionTarget) {
      optionTarget.focus({ preventScroll: true });
      const optionGroup = optionTarget.closest('[data-option-group]');
      (optionGroup || optionTarget).scrollIntoView({ block: 'start', behavior: 'auto' });
    } else if (held.modeFocus) {
      modeAction.focus({ preventScroll: true });
    }
  }

  dateForm.addEventListener('submit', function (event) {
    event.preventDefault();
    const previous = runtime.normalized && runtime.normalized.state;
    const changedDay = !previous || previous.civilDate !== dateInput.value ||
      previous.edition.id !== missalSelect.value;
    const updates = {
      date: dateInput.value,
      missal: missalSelect.value,
      bible: bibleSelect.value,
      orations: orationsSelect.value,
      mass: formularyField.hidden ? null : formularySelect.value
    };
    if (!ordinaryLangField.hidden) updates['ordinary-lang'] = ordinaryLangSelect.value;
    if (!ordinaryOptionField.hidden && runtime.ordinary) {
      const group = window.OrdinarySeating.variantGroupOf(runtime.ordinary);
      if (group) updates[group.group] = ordinaryOptionSelect.value;
    }
    readerShell.close({ restoreFocus: false });
    navigate(updates, changedDay ? ['mass'] : []);
  });

  document.getElementById('previous-date').addEventListener('click', function () {
    if (!runtime.normalized) return;
    readerShell.close({ restoreFocus: false });
    navigate({ date: Model.shift(runtime.normalized.state.civilDate, -1), mass: null }, ['mass']);
  });
  document.getElementById('today-date').addEventListener('click', function () {
    readerShell.close({ restoreFocus: false });
    navigate({ date: todayISO(), mass: null }, ['mass']);
  });
  document.getElementById('next-date').addEventListener('click', function () {
    if (!runtime.normalized) return;
    readerShell.close({ restoreFocus: false });
    navigate({ date: Model.shift(runtime.normalized.state.civilDate, 1), mass: null }, ['mass']);
  });

  document.querySelector('[data-mode="read"]').addEventListener('click', function () {
    if (runtime.mode === 'read') {
      readerShell.close();
      return;
    }
    const location = captureModeLocation('read');
    readerShell.close({ restoreFocus: false, restoreScroll: false });
    window.dayReaderDebug.modeSwitches += 1;
    runtime.modeStartedAt = performance.now();
    navigate({ ordinary: '0' }, [], { location: location, modeFocus: true });
  });
  document.querySelector('[data-mode="missal"]').addEventListener('click', function () {
    if (runtime.mode === 'missal') {
      readerShell.close();
      return;
    }
    const location = captureModeLocation('missal');
    readerShell.close({ restoreFocus: false, restoreScroll: false });
    window.dayReaderDebug.modeSwitches += 1;
    runtime.modeStartedAt = performance.now();
    navigate({ ordinary: '1' }, [], { location: location, modeFocus: true });
  });
  window.addEventListener('popstate', function (event) {
    runtime.pendingLocation = event.state && event.state.dayReaderLocation ||
      readerShell.captureSemanticLocation();
    runtime.pendingModeFocus = false;
    runtime.pendingFocus = null;
    window.dayReaderDebug.pendingNavigation = {
      location: runtime.pendingLocation,
      modeFocus: false,
      focus: null
    };
    renderCandidate();
  });
  window.addEventListener('hashchange', function () {
    if (!window.dayReaderDebug.ready) return;
    renderCandidate();
  });

  T.setInlineNotice(
    'No data root could be reached at "' + T.dataRoot + '", so the internal Day reader candidate has nothing to derive from.'
  );
  renderCandidate();
}());
