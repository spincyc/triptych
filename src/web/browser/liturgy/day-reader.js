/* Production Day Read/Missal controller over production assembly, state, and renderers. */
'use strict';

(function () {
  const T = window.Triptych;
  const Model = window.MassAssembly;
  const Contract = window.LiturgyReaderState;
  const Adapters = window.LiturgyReaderStateAdapters;
  const Shell = window.TriptychReaderShell;
  const OrdinaryRenderer = window.TriptychOrdinaryRenderer;

  if (!T || !Model || !Contract || !Adapters || !Shell || !OrdinaryRenderer) {
    throw new Error('Day reader requires production browser, assembly, Ordinary renderer, state, adapter, and shell modules');
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
    branches: [],
    rubrics: null,
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

  function limitation(titleText, message) {
    const section = T.el('section', 'candidate-limitation');
    section.appendChild(T.el('h2', null, titleText));
    section.appendChild(T.el('p', null, message));
    return section;
  }

  function clearSelectionState(outcome) {
    runtime.normalized = null;
    runtime.result = null;
    runtime.derived = null;
    runtime.structure = null;
    runtime.ordinary = null;
    runtime.branch = null;
    runtime.branches = [];
    runtime.rubrics = null;
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
      'The reader rejected the explicit state and did not substitute another edition, date, Bible, language, locality, or formulary.'));
    const list = T.el('ul');
    (errors || []).forEach(function (error) {
      const label = error.path ? error.path + ': ' : '';
      list.appendChild(T.el('li', null, label + (error.message || String(error))));
    });
    section.appendChild(list);
    replaceReading(section);
    title.textContent = 'Selection unavailable';
    document.title = 'Selection unavailable — Day — Triptych';
    dateLine.textContent = '';
    coverageNotice.hidden = true;
    window.dayReaderDebug.error = (errors || []).map(function (one) {
      return { code: one.code || null, path: one.path || '', message: one.message || String(one) };
    });
    refreshDetailsAfterOutcome();
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
    const mode = requestedModeOf(parsed);
    // Study has a complete public spelling but no renderer in this slice.
    // Compare deliberately does not: the state contract requires an explicit
    // comparison request, for which v1 exposes no public URL spelling, so a
    // bare mode=compare is rejected instead of masquerading as deferred work.
    return mode === 'study' ? ['mode=' + mode] : [];
  }

  function requestedModeOf(parsed) {
    const duplicates = (parsed.duplicates || []).some(function (row) {
      return row.key === 'ordinary' || row.key === 'mode';
    });
    if (duplicates) return null;
    if (parsed.present.indexOf('mode') >= 0) {
      const mode = parsed.recognized.mode;
      if (Contract.MODES.indexOf(mode) < 0) return null;
      if (parsed.present.indexOf('ordinary') >= 0) {
        const legacy = parsed.recognized.ordinary === '1' ? 'missal' :
          (parsed.recognized.ordinary === '0' ? 'read' : null);
        if (legacy === null || mode !== legacy) return null;
      }
      return mode;
    }
    if (parsed.present.indexOf('ordinary') < 0) return 'read';
    if (parsed.recognized.ordinary === '0') return 'read';
    if (parsed.recognized.ordinary === '1') return 'missal';
    return null;
  }

  function modeLabel(mode) {
    if (mode === 'missal') return 'Missal';
    if (mode === 'read') return 'Read';
    if (mode === 'study') return 'Study';
    if (mode === 'compare') return 'Compare';
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
    return ['Day', modeLabel(mode), labels[outcomeClass] || outcomeClass]
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
    const variantPresent = (parsed.variantKeys || []).filter(function (key) {
      return parsed.present.indexOf(key) >= 0;
    });
    const languagePresent = parsed.present.indexOf('ordinary-lang') >= 0;
    if (!languagePresent && !variantPresent.length) return [];
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
    if (languagePresent && !structures.some(function (structure) {
      return (structure.languages || []).some(function (row) {
        return row.lang === parsed.recognized['ordinary-lang'];
      });
    })) {
      errors.push({
        code: 'invalid-explicit-value', path: 'ordinary-lang',
        message: 'the explicit Ordinary language is not applicable to the selected edition’s production Ordinary'
      });
    }
    variantPresent.forEach(function (key) {
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
    if (parsed.present.indexOf('mode') >= 0 &&
        parsed.present.indexOf('ordinary') >= 0 && requestedModeOf(parsed) === null) {
      errors.push({
        code: 'conflicting-explicit-mode', path: 'mode',
        message: 'explicit mode conflicts with the legacy ordinary state'
      });
    }
    return { ok: errors.length === 0, missal: wantedMissal, date: wantedDate, errors: errors };
  }

  async function assemble(parsed, manifests, preliminary) {
    const missal = preliminary.missal;
    const year = preliminary.date.slice(0, 4);
    const requestedMode = requestedModeOf(parsed);
    // Read does not present the Ordinary, but explicit dormant Ordinary state
    // is still source-validated. Remembered or default state remains cold.
    const explicitOrdinary = parsed.present.indexOf('ordinary-lang') >= 0 ||
      (parsed.variantKeys || []).some(function (key) {
        return parsed.present.indexOf(key) >= 0;
      });
    const needsOrdinary = requestedMode === 'missal' || explicitOrdinary;
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
    return {
      derived: derived,
      rubrics: rows[0],
      structure: rows[2],
      ordinary: rows[3] || null,
      context: context
    };
  }

  // The controls that DERIVE from a resolved day follow the outcome; the
  // controls that LEAVE a day do not.
  //
  // A failed outcome used to disable this surface entire, which is right about
  // stale state and wrong about escape: the date box, the missal select, Apply
  // and all three step buttons were the only things on the page that could
  // reach a different day, so a reader who stepped to a day that would not
  // render was left with a dead surface and no way out but the URL bar. That is
  // what "selecting a previous day makes the date box unresponsive" is.
  //
  // What the failure rule actually protects is that no PRIOR SELECTION shows
  // through a failure, and that is kept: `resetDateSurface` still empties the
  // date and every derived select, so these controls stay live holding nothing.
  // Previous and Next need a resolved day to step from and so follow `enabled`;
  // Today needs none, because today is a constant and not prior state, and it
  // is the guaranteed way back.
  function setDateSurfaceEnabled(enabled) {
    [bibleSelect, orationsSelect, formularySelect,
      ordinaryLangSelect, ordinaryOptionSelect].forEach(function (control) {
      control.disabled = !enabled;
    });
    // NEVER gated on runtime state. The first cut of this tied them to
    // `runtime.missals`, which `loadManifests()` fills, so any paint before that
    // landed disabled the date box, the missal select, Apply and Today at once —
    // the whole surface frozen, which is the opposite of the escape this exists
    // to guarantee. A control that can only ever navigate away is safe to leave
    // live: the step handlers already refuse when there is no resolved day, and
    // an empty missal select selects nothing.
    dateInput.disabled = false;
    missalSelect.disabled = false;
    dateForm.querySelector('.surface-apply').disabled = false;
    dateStepButtons.forEach(function (button) {
      button.disabled = button.id === 'today-date' ? false : !enabled;
    });
  }

  function resetDateSurface() {
    dateInput.value = '';
    [bibleSelect, orationsSelect, formularySelect,
      ordinaryLangSelect, ordinaryOptionSelect].forEach(function (select) {
      select.replaceChildren();
    });
    // The missal list is manifest data, not selection state: it is the same
    // list whatever day failed. Emptying it left an enabled select with nothing
    // in it, which is a second dead end wearing the first one's clothes. Nor is
    // its VALUE cleared now: that left a reader whose selection failed with no
    // missal named at all. It is read from the hash, so it is the request in
    // hand and not a prior selection showing through.
    T.fillSelect(missalSelect, (runtime.missals || []).map(function (row) {
      return { value: row.id, label: row.label, title: row.edition || row.code || row.id };
    }));
    const asked = new URLSearchParams(window.location.hash.replace(/^#/, '')).get('missal');
    missalSelect.value = (runtime.missals || []).some(function (row) {
      return row.id === asked;
    }) ? asked : '';
    formularyField.hidden = true;
    ordinaryLangField.hidden = true;
    ordinaryOptionField.hidden = true;
    dateStatus.textContent = 'No validated selection is available for the current reader outcome.';
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
    // The unresolved document is the only selector when the source appoints
    // coequal formularies.  A native select would visibly preselect its first
    // option and manufacture the very default the adapter refused to choose.
    if (readable.length > 1 && runtime.outcome !== 'unresolved') {
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
    if (runtime.outcome === 'unresolved') {
      dateStatus.textContent = 'These validated values are current, but the formulary outcome remains unresolved.';
    } else {
      dateStatus.textContent = runtime.branches.length > 1
        ? 'Every held territorial branch is shown; no locality or preferred branch is inferred.'
        : 'The resolved production result is shown without inferring a locality.';
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

  function detailsLinkSection(heading, links) {
    const section = T.el('section', 'details-section');
    section.appendChild(T.el('h3', null, heading));
    const list = T.el('ul');
    links.forEach(function (link) {
      const item = T.el('li');
      const anchor = T.el('a', null, link.label);
      anchor.href = link.href;
      item.appendChild(anchor);
      list.appendChild(item);
    });
    section.appendChild(list);
    return section;
  }

  function populateDetails() {
    if (runtime.detailsLoaded) return;
    detailsBody.replaceChildren();
    if (runtime.outcome === 'loading') {
      detailsBody.appendChild(T.el('p', 'surface-note',
        'The current selection is still loading. Details will follow the committed result.'));
      return;
    }
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
      ['Territorial result', runtime.branches.length > 1
        ? runtime.branches.map(function (row) { return row.branch.option; }).join('; ')
        : (runtime.branch && runtime.branch.option || 'Universal')],
      ['Bible', bible && bible.label || state.bible.id],
      ['Orations', humanLanguage(state.languages.orations)],
      ['Mode', modeLabel(runtime.mode)],
      ['Ordinary language', runtime.mode === 'missal'
        ? humanLanguage(state.languages.ordinary || 'en') : null],
      ['Ordinary option', runtime.mode === 'missal'
        ? selectedOrdinaryOptionLabel(state, runtime.ordinary) : null],
      ['Formulary', runtime.branches.length > 1
        ? runtime.branches.map(function (row) {
          return row.result && row.result.resolved && row.result.resolved.formulary;
        }).filter(Boolean).join('; ')
        : (runtime.result && runtime.result.resolved && runtime.result.resolved.formulary)],
      ['Mass form', state.form ||
        (runtime.result && runtime.result.resolved && runtime.result.resolved.form)]
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
      outcome.appendChild(T.el('h3', null, 'Reader outcome'));
      const messages = {
        deferred: 'An active request is valid and preserved, but is not yet rendered.',
        unresolved: runtime.branches.some(function (row) {
          return row.result && row.result.resolved && !(row.result.unresolvedChoices || []).length;
        })
          ? 'The current request has rendered territorial results alongside a branch-local formulary choice that remains unresolved.'
          : 'The current request is validated, but no formulary outcome has been selected.',
        unrenderable: 'The current request is valid, but its semantic document cannot be rendered from the available production resources.'
      };
      outcome.appendChild(T.el('p', 'surface-note', messages[runtime.outcome] || 'This selection is not resolved.'));
      detailsBody.appendChild(outcome);
    }
    detailsBody.appendChild(detailsLinkSection('Related reader', [
      { label: 'Browse the Propers', href: 'index.html' }
    ]));
    detailsBody.appendChild(detailsLinkSection('Elsewhere in Triptych', [
      { label: 'The Code, Canon by Canon', href: '../law/' },
      { label: 'Every Document', href: '../texts/' }
    ]));
    runtime.detailsLoaded = true;
    window.dayReaderDebug.detailsBuilds += 1;
  }

  function refreshDetailsAfterOutcome() {
    runtime.detailsLoaded = false;
    detailsBody.replaceChildren(T.el('p', 'surface-note',
      'Details load when this surface is opened.'));
    if (readerShell.openSurface() === 'details') populateDetails();
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
    const mode = Contract.MODES.indexOf(held.mode) >= 0 ? held.mode : null;
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
      return 'This Day result contains an unresolved choice. The reader has not selected one silently.';
    }
    if (rows.some(function (row) { return row.state === 'unavailable'; })) {
      return 'Some appointed text is unavailable in the selected edition or language; each held portion remains identified.';
    }
    if (rows.some(function (row) { return row.state === 'unsupported'; })) {
      return 'Part of this selection is outside the supported ' + modeLabel(runtime.mode) + ' boundary.';
    }
    if (rows.some(function (row) { return row.completeness === 'partial'; })) {
      return 'Some appointed text is not held in this repository; the available portions are shown.';
    }
    return 'This selection has a material coverage limitation.';
  }

  function reasoningParagraph(text, locus) {
    const paragraph = T.el('p', 'reasoning-note', text || '');
    if (locus) {
      paragraph.appendChild(document.createTextNode(' '));
      paragraph.appendChild(T.el('cite', 'reasoning-locus', locus));
    }
    return paragraph;
  }

  function reasoningLatin(text) {
    const paragraph = T.el('p', 'reasoning-latin', text);
    paragraph.lang = 'la';
    return paragraph;
  }

  const REASONING_SOURCE_WORDS = Object.freeze({
    index: 'in the calendar',
    implied: 'constituted from the season',
    arrived: 'transferred here'
  });

  const REASONING_ORDINALS = Object.freeze({ 2: 'Second', 3: 'Third' });

  function reasoningOrdinal(position) {
    return REASONING_ORDINALS[position] || 'Oration ' + position;
  }

  function appendOrationRuleReasoning(item, oration, branch) {
    if (oration.why) item.appendChild(reasoningParagraph(oration.why, oration.locus));
    if (oration.conclusion) {
      item.appendChild(reasoningParagraph('Said under ' + oration.conclusion + '.'));
    }
    if (oration.alternative) {
      item.appendChild(reasoningParagraph(
        'The collect of ' + oration.alternative.of_name +
        ' may be said in its place: ' + oration.alternative.what,
        oration.alternative.locus));
    }
    if (branch.sungDiffers) {
      item.appendChild(reasoningParagraph(
        'Not said at a sung Mass that is not the conventual Mass.'));
    }
  }

  function appendProperReasoning(body, branch, rubrics, structure, result) {
    const series = branch.orations && (branch.orations.all || branch.orations.low_mass) || [];
    const subordinate = series.filter(function (row) { return row.position > 1; });
    if (!subordinate.length) return;
    const slots = [];
    if (series[0] && series[0].label) {
      slots.push({ slot: series[0].label, what: null, locus: null });
    }
    ((rubrics.orations || {}).tracked_by || []).forEach(function (row) {
      if (row && row.slot) slots.push(row);
    });
    if (!slots.length) return;
    const mass = (structure.masses || []).find(function (row) {
      return result && result.resolved && row.key === result.resolved.formulary;
    });
    const heldNames = new Set(mass && !T.massIsUncompiled(mass)
      ? (mass.propers || []).filter(function (row) { return !T.isPlaceholder(row); })
        .map(function (row) { return row.name; }) : []);
    let applicableSlots = slots.filter(function (slot) { return heldNames.has(slot.slot); });
    const withoutHeldSlot = applicableSlots.length === 0;
    body.appendChild(T.el('h4', null, 'Appointed commemorations'));
    if (withoutHeldSlot) {
      body.appendChild(reasoningParagraph(
        'This corpus carries no oration slot for the day’s own Mass, so the reader ' +
        'cannot say which Proper each follows. They are appointed, not absent.'));
      const list = T.el('ul', 'reasoning-list');
      subordinate.forEach(function (oration) {
        const item = T.el('li');
        item.appendChild(T.el('strong', null,
          reasoningOrdinal(oration.position) + ' oration of ' + oration.of_name));
        if (oration.kind) item.appendChild(document.createTextNode(' — ' + oration.kind + '.'));
        const orationMass = (structure.masses || []).find(function (row) {
          return row.key === oration.of;
        });
        const namedSlot = String(oration.label || '').replace(
          /^(?:second|third|oration \d+)\s+/i, '');
        const sourceSlot = namedSlot || series[0] && series[0].label || 'Collect';
        const matching = orationMass && (orationMass.propers || []).find(function (row) {
          return String(row.name).toLowerCase() === String(sourceSlot).toLowerCase() ||
            String(row.name).toLowerCase() === 'collect';
        });
        if (matching && matching.incipit) item.appendChild(reasoningLatin(matching.incipit));
        appendOrationRuleReasoning(item, oration, branch);
        list.appendChild(item);
      });
      body.appendChild(list);
      return;
    }
    applicableSlots.forEach(function (slot) {
      body.appendChild(T.el('h5', null, 'What follows the ' + String(slot.slot).toLowerCase()));
      if (slot.what) body.appendChild(reasoningParagraph(slot.what, slot.locus));
      const list = T.el('ul', 'reasoning-list');
      subordinate.forEach(function (oration) {
        const item = T.el('li');
        item.appendChild(T.el('strong', null,
          reasoningOrdinal(oration.position) + ' ' + String(slot.slot).toLowerCase() +
          ' of ' + oration.of_name));
        if (oration.kind) item.appendChild(document.createTextNode(' — ' + oration.kind + '.'));
        const orationMass = (structure.masses || []).find(function (row) {
          return row.key === oration.of;
        });
        const matching = orationMass && (orationMass.propers || []).find(function (row) {
          return row.name === slot.slot;
        });
        if (matching && matching.incipit) {
          item.appendChild(reasoningLatin(matching.incipit));
        } else if (orationMass && !T.massIsUncompiled(orationMass)) {
          item.appendChild(reasoningParagraph(
            'Its ' + String(slot.slot).toLowerCase() + ' is appointed and is not transcribed here.'));
        }
        appendOrationRuleReasoning(item, oration, branch);
        list.appendChild(item);
      });
      body.appendChild(list);
    });
  }

  function appendOrdinaryReasoning(body, result, ordinary) {
    if (!ordinary || !result) return;
    const placements = (result.events || []).filter(function (event) {
      return event.kind === 'proper' && event.seat && event.seat.locus;
    });
    if (placements.length) {
      body.appendChild(T.el('h4', null, 'Placement in the Ordinary'));
      const list = T.el('ul', 'reasoning-list');
      placements.forEach(function (event) {
        const item = T.el('li');
        item.appendChild(T.el('strong', null, event.editionSlotLabel || event.id));
        item.appendChild(reasoningParagraph('Seated here by ' + event.seat.locus + '.'));
        list.appendChild(item);
      });
      body.appendChild(list);
    }
    if (ordinary.derived_from || ordinary.slots_derived_from) {
      body.appendChild(T.el('h4', null, 'Ordinary resolution'));
      if (ordinary.derived_from) body.appendChild(reasoningParagraph(ordinary.derived_from));
      if (ordinary.slots_derived_from) {
        body.appendChild(reasoningParagraph(ordinary.slots_derived_from));
      }
    }
    const shownElements = new Set((result.events || []).filter(function (event) {
      return event.kind === 'ordinary-element' || event.kind === 'ordinary_element';
    }).map(function (event) {
      return event.id.replace(/^ordinary-element\//, '');
    }));
    const notes = [];
    (ordinary.sections || []).forEach(function (section) {
      (section.elements || []).forEach(function (element) {
        if (element.note && shownElements.has(element.key)) notes.push(element);
      });
    });
    if (notes.length) {
      body.appendChild(T.el('h4', null, 'Ordinary source notes'));
      const list = T.el('ul', 'reasoning-list');
      notes.forEach(function (element) {
        const item = T.el('li');
        item.dataset.reasoningOrdinaryElement = element.key;
        item.appendChild(T.el('strong', null, element.name || element.key));
        item.appendChild(reasoningParagraph(element.note));
        list.appendChild(item);
      });
      body.appendChild(list);
    }
  }

  function reasoningApparatus(branch, rubrics, structure, result, ordinary) {
    const apparatus = document.createElement('details');
    apparatus.className = 'day-reasoning';
    apparatus.dataset.reasoningBranch = branch.option || 'universal';
    apparatus.appendChild(T.el('summary', null, 'Why this Mass'));
    const body = T.el('div', 'day-reasoning-body');
    const winner = branch.winner;
    if (winner) {
      const lead = T.el('p', 'reasoning-lead');
      lead.appendChild(T.el('strong', null, winner.name));
      lead.appendChild(document.createTextNode(winner.row !== null && winner.row !== undefined
        ? (winner.optional ? ' stands highest at ' : ' takes the day at ') +
          Model.placeWord(rubrics) + ' ' + winner.row +
          (winner.class ? ', class ' + winner.class : '') + '.'
        : ' takes the day.'));
      body.appendChild(lead);
      if (winner.rowLabel) body.appendChild(reasoningParagraph(winner.rowLabel, winner.locus));
      if (winner.why && winner.why !== winner.rowLabel) {
        body.appendChild(reasoningParagraph(winner.why, winner.locus));
      }
      if (winner.source) {
        body.appendChild(reasoningParagraph(
          REASONING_SOURCE_WORDS[winner.source] || winner.source));
      }
      if (winner.optional) {
        body.appendChild(reasoningParagraph(
          'It is optional; the day below it may be kept instead.', winner.locus));
      }
      if (winner.territorial) {
        body.appendChild(reasoningParagraph(
          'This result holds only under the source-defined territorial branch “' +
          winner.territorial + '”.'));
      }
      if (winner.formulary && winner.formulary.kind === 'own') {
        if (winner.formulary.why) {
          body.appendChild(reasoningParagraph(winner.formulary.why, winner.formulary.locus));
        }
        if (winner.formulary.latin) body.appendChild(reasoningLatin(winner.formulary.latin));
        if (winner.formulary.printed) {
          body.appendChild(reasoningParagraph(
            'The Missal prints it under the heading “' + winner.formulary.printed + '”.'));
        }
        if (winner.formulary.note) body.appendChild(reasoningParagraph(winner.formulary.note));
      } else if (winner.formulary && winner.formulary.kind === 'borrowed') {
        body.appendChild(reasoningParagraph(
          'This day takes ' + winner.formulary.name + '.',
          winner.formulary.rule && winner.formulary.rule.locus));
        if (winner.formulary.rule && winner.formulary.rule.rule) {
          body.appendChild(reasoningParagraph(winner.formulary.rule.rule));
        }
      }
    } else if (branch.choice) {
      body.appendChild(reasoningParagraph(
        branch.choice.what + ': ' + (branch.choice.among || []).map(function (row) {
          return row.name;
        }).join('; '), branch.choice.locus));
    }

    const others = (branch.candidates || []).filter(function (candidate) {
      return !winner || candidate.id !== winner.id;
    });
    if (others.length) {
      body.appendChild(T.el('h4', null, 'Also on this date'));
      const list = T.el('ul', 'reasoning-list');
      others.forEach(function (candidate) {
        const loser = (branch.losers || []).find(function (row) {
          return row.id === candidate.id;
        });
        const item = T.el('li');
        item.appendChild(T.el('strong', null, candidate.name));
        if (loser && loser.disposition) {
          item.appendChild(document.createTextNode(' — ' + loser.disposition + '.'));
        }
        item.appendChild(reasoningParagraph(
          loser && loser.why || candidate.why,
          loser && loser.locus || candidate.locus
        ));
        if (loser && loser.destination) {
          item.appendChild(reasoningParagraph(
            'Kept on ' + longDate(loser.destination, Model.weekdayOf(loser.destination)) + '.'));
        }
        if (loser && loser.destinationNotComputed) {
          item.appendChild(reasoningParagraph(
            'This reader does not compute where it goes. ' + loser.destinationNotComputed));
        }
        list.appendChild(item);
      });
      body.appendChild(list);
    }
    const ceiling = branch.ceilings && branch.ceilings.low_mass;
    if (ceiling) {
      body.appendChild(reasoningParagraph(ceiling.what ||
        ('This day admits ' + ceiling.max + ' commemoration' +
          (ceiling.max === 1 ? '' : 's') + '.'), ceiling.locus));
    }
    const category = rubrics.mass_category || {};
    if (category.assumed) {
      body.appendChild(reasoningParagraph(
        'This result assumes ' + category.assumed +
        '; it does not test whether a votive, ritual, requiem or festive Mass is admitted.',
        category.locus));
    }
    (branch.extras || []).forEach(function (extra) {
      body.appendChild(reasoningParagraph(extra.slot + ': ' + extra.what, extra.locus));
    });
    (branch.remarks || []).forEach(function (remark) {
      body.appendChild(reasoningParagraph(remark.what, remark.locus));
    });
    (branch.massChoices || []).forEach(function (choice) {
      body.appendChild(T.el('h4', null, choice.label || 'Source-defined Mass choice'));
      body.appendChild(reasoningParagraph(choice.why || choice.what, choice.locus));
      if (choice.latin) body.appendChild(reasoningLatin(choice.latin));
      if (choice.openBecause) body.appendChild(reasoningParagraph(choice.openBecause));
      if ((choice.among || []).length) {
        const options = T.el('ul', 'reasoning-list');
        choice.among.forEach(function (option) {
          const item = T.el('li');
          item.appendChild(T.el('strong', null, option.label || option.name || option.id));
          if (choice.preferred === option.id) {
            item.appendChild(document.createTextNode(' — ordinarily said.'));
          }
          item.appendChild(reasoningParagraph(option.why, option.locus));
          options.appendChild(item);
        });
        body.appendChild(options);
      }
    });
    appendProperReasoning(body, branch, rubrics, structure, result);
    appendOrdinaryReasoning(body, result, ordinary);
    apparatus.appendChild(body);
    return apparatus;
  }

  function locationPrefix(branch, multiple) {
    return multiple ? 'territory/' + branch.option + '/' : '';
  }

  function resultStateForBranch(state, branch, multiple) {
    if (!multiple) return state;
    return Object.assign({}, state, {
      calendar: Object.assign({}, state.calendar, { territory: { id: branch.option } })
    });
  }

  function failedBranchDocument(branch, prefix, error) {
    const fragment = document.createDocumentFragment();
    const section = T.el('section', 'candidate-failure');
    section.appendChild(T.el('h3', null, 'This territorial result cannot be rendered'));
    section.appendChild(T.el('p', null,
      String(error && error.message || error) +
      ' No locality, formulary, or liturgical text was substituted.'));
    fragment.appendChild(section);
    return {
      branch: branch,
      result: null,
      fragment: fragment,
      contents: [],
      bible: bibleRow(runtime.normalized.state.bible.id),
      uncompiled: null,
      notice: 'One held territorial result cannot be rendered from the available production resources.',
      prefix: prefix,
      error: String(error && error.message || error)
    };
  }

  function primaryDayChoice(result, branch) {
    const readable = new Set();
    (branch && branch.readable || []).forEach(function (one) {
      if (one.id) readable.add(one.id);
      if (one.key) readable.add(one.key);
    });
    return (result.unresolvedChoices || []).find(function (one) {
      return one.id === 'calendar-formulary' || /^proper-form:/.test(one.id) ||
        ((one.options || []).length > 1 && one.options.every(function (option) {
          return readable.has(option.id);
        }));
    }) || null;
  }

  function translationIdentity(row) {
    return row && (row.source_id || row.source || null);
  }

  /** Witnesses that can supply every translated Proper without suppressing one. */
  function translationWitnessState(result, structure, language) {
    if (!result || language === T.SOURCE_LANGUAGE) {
      return { requiresChoice: false, held: [], choices: [] };
    }
    const heldByProper = [];
    let requiresChoice = false;
    let anonymousHeldTranslation = false;
    (result.events || []).forEach(function (event) {
      if (event.kind !== 'proper' || !event.selected ||
          event.selected.kind !== 'composed' || event.selected.language !== language) return;
      const selected = event.selected;
      if (selected.availability === 'choice-required') {
        const ids = Array.from(new Set(selected.unresolvedWitnesses || [])).filter(Boolean);
        if (ids.length > 1) {
          requiresChoice = true;
          heldByProper.push(ids);
        } else anonymousHeldTranslation = true;
      } else if (selected.availability === 'held' && !selected.missing && selected.text) {
        if (selected.sourceId) heldByProper.push([selected.sourceId]);
        else anonymousHeldTranslation = true;
      }
    });
    if (!heldByProper.length || anonymousHeldTranslation) {
      return { requiresChoice: requiresChoice, held: [], choices: [] };
    }
    const common = heldByProper.reduce(function (intersection, ids) {
      return intersection.filter(function (id) { return ids.indexOf(id) >= 0; });
    }, heldByProper[0].slice());
    const labels = new Map((structure.translations || []).map(function (row) {
      return [translationIdentity(row), row.label || translationIdentity(row)];
    }));
    return {
      requiresChoice: requiresChoice,
      held: common,
      choices: requiresChoice ? common.map(function (id) {
        return { id: id, label: labels.get(id) || id };
      }) : []
    };
  }

  function validateExplicitTranslationWitness(state, derived, structure) {
    const wanted = state.languages && state.languages.translationWitness || null;
    if (!wanted) return [];
    const errors = [];
    (derived.options || []).forEach(function (branch) {
      const branchState = resultStateForBranch(state, branch, derived.options.length > 1);
      const languages = Object.assign({}, branchState.languages);
      delete languages.translationWitness;
      const witnessless = Object.assign({}, branchState, { languages: languages });
      const probe = Adapters.adaptDay({
        request: witnessless,
        derived: derived,
        structure: structure,
        ordinary: null
      });
      const witnessState = translationWitnessState(
        probe, structure, branchState.languages.orations
      );
      if (primaryDayChoice(probe, branch) || witnessState.held.indexOf(wanted) < 0) {
        errors.push({
          code: 'invalid-explicit-value', path: 'translation-witness',
          message: 'the explicit translation witness cannot faithfully supply this resolved Day formulary and language'
        });
      }
    });
    return errors.slice(0, 1);
  }

  function resolvableTranslationWitnessState(result, structure, state) {
    const witnessState = translationWitnessState(result, structure, state.languages.orations);
    if (!witnessState.choices.length || !runtime.derived) return witnessState;
    const choices = witnessState.choices.filter(function (option) {
      const languages = Object.assign({}, state.languages, {
        translationWitness: option.id
      });
      const candidate = Object.assign({}, state, { languages: languages });
      return !validateExplicitTranslationWitness(
        candidate, runtime.derived, structure
      ).length;
    });
    return Object.assign({}, witnessState, { choices: choices });
  }

  /** A valid Day whose source authorizes several identities and no default. */
  function unresolvedChoiceDocument(result, branch, structure, prefix) {
    const choice = primaryDayChoice(result, branch);
    if (!choice || !choice.options || choice.options.length < 2) {
      throw new Error('an unresolved Day needs its complete authorized formulary choice');
    }
    const properForm = /^proper-form:/.test(choice.id);
    const mass = properForm && (structure.masses || []).find(function (row) {
      return result.resolved && row.key === result.resolved.formulary;
    });
    if (properForm && !mass) {
      throw new Error('a Proper-form choice has no resolved source Mass');
    }
    const offered = properForm ? (mass.forms || []) : (branch.readable || []);
    const readable = new Map(offered.map(function (row) {
      return [row.id || row.key, row];
    }));
    const optionIds = choice.options.map(function (option) { return option.id; });
    if (optionIds.indexOf('main') >= 0) {
      throw new Error('the internal main form may not become a reader choice');
    }
    if (optionIds.some(function (id) { return !readable.has(id); }) ||
        optionIds.length !== readable.size) {
      throw new Error('source choice options do not match the readable identities');
    }

    const titleText = properForm ? 'Choose a Mass form' : 'Choose a formulary';
    const section = T.el('section', 'candidate-choice ' +
      (properForm ? 'proper-form-choice' : 'calendar-formulary-choice'));
    section.dataset.unresolvedChoice = choice.id;
    section.tabIndex = -1;
    const heading = T.el('h2', null, titleText);
    const baseId = properForm ? 'proper-form-choice' : 'calendar-formulary-choice';
    heading.id = prefix
      ? baseId + '-' + String(branch.option || 'universal').replace(/[^a-z0-9]+/gi, '-')
      : baseId;
    section.appendChild(heading);
    section.appendChild(T.el('p', 'candidate-choice-reason', choice.reason));
    const locus = (choice.sourceHooks || []).find(function (one) {
      return one.kind === 'locus';
    });
    if (locus) section.appendChild(T.el('p', 'candidate-choice-locus', locus.id));

    const form = T.el('form', 'candidate-choice-form');
    form.dataset.choice = choice.id;
    const fieldset = T.el('fieldset');
    fieldset.appendChild(T.el('legend', null,
      properForm ? 'Source-authored forms of this Mass' :
        'Authorized formularies for this date'));
    const options = T.el('div', 'candidate-choice-options');
    choice.options.forEach(function (option) {
      const row = readable.get(option.id);
      const label = T.el('label', 'candidate-choice-option');
      const input = document.createElement('input');
      input.type = 'radio';
      input.name = 'day-authorized-choice';
      input.value = option.id;
      input.dataset.choiceOption = option.id;
      label.appendChild(input);
      label.appendChild(document.createTextNode(row.label || row.name || option.id));
      options.appendChild(label);
    });
    fieldset.appendChild(options);
    const submit = T.el('button', 'candidate-choice-apply',
      properForm ? 'Read selected Mass form' : 'Read selected formulary');
    submit.type = 'submit';
    submit.disabled = true;
    fieldset.appendChild(submit);
    form.appendChild(fieldset);
    form.addEventListener('change', function () {
      submit.disabled = !form.querySelector('input[name="day-authorized-choice"]:checked');
    });
    form.addEventListener('submit', function (event) {
      event.preventDefault();
      const selected = form.querySelector('input[name="day-authorized-choice"]:checked');
      if (!selected) return;
      readerShell.close({ restoreFocus: false, restoreScroll: false });
      if (properForm) {
        navigate({
          mass: result.resolved.formulary, form: selected.value, location: null
        }, ['location'], {
          location: { kind: 'top', id: null }, focus: { kind: 'day-choice-result' }
        });
      } else {
        navigate({ mass: selected.value, form: null, location: null },
          ['form', 'location'], {
            location: { kind: 'top', id: null }, focus: { kind: 'day-choice-result' }
          });
      }
    });
    section.appendChild(form);
    return { node: section, choice: choice, title: titleText, id: heading.id };
  }

  function unresolvedBranchDocument(result, branch, structure, prefix) {
    const documentChoice = unresolvedChoiceDocument(result, branch, structure, prefix);
    const fragment = document.createDocumentFragment();
    fragment.appendChild(documentChoice.node);
    return {
      branch: branch,
      result: result,
      fragment: fragment,
      contents: [{
        id: documentChoice.id,
        label: documentChoice.title,
        element: documentChoice.node,
        group: 'Day selection'
      }],
      bible: bibleRow(runtime.normalized.state.bible.id),
      uncompiled: null,
      notice: coverageMessage(result),
      prefix: prefix,
      unresolved: true
    };
  }

  function commitUnresolvedChoice(result, branch, assembled, state) {
    const documentChoice = unresolvedChoiceDocument(
      result, branch, assembled.structure
    );
    reading.replaceChildren(documentChoice.node);
    reading.setAttribute('aria-busy', 'false');
    readerShell.setContents([{
      id: documentChoice.id,
      label: documentChoice.title,
      element: documentChoice.node,
      group: 'Day selection'
    }]);

    const missal = missalRow(state.edition.id);
    title.textContent = documentChoice.title;
    dateLine.textContent = longDate(assembled.derived.date, assembled.derived.weekday);
    commitOutcomePresentation({
      mode: runtime.mode,
      outcome: 'unresolved',
      outcomeClass: 'unresolved',
      metadata: [
        missal && (missal.edition || missal.label),
        documentChoice.choice.options.length + ' authorized options',
        'No default selected'
      ].filter(Boolean).join(' · ')
    });
    coverageNotice.textContent = coverageMessage(result);
    coverageNotice.hidden = false;
    document.title = documentChoice.title + ' — Day — Triptych';
    refreshDetailsAfterOutcome();
  }

  async function buildResultDocument(result, structure, branch, renderContext, isCurrent) {
    const state = renderContext.state;
    const mode = renderContext.mode;
    const ordinary = renderContext.ordinary;
    const prefix = renderContext.locationPrefix || '';
    const mass = (structure.masses || []).find(function (row) {
      return result.resolved && row.key === result.resolved.formulary;
    });
    if (!mass) throw new Error('the validated resolved formulary is absent from production Proper data');
    const bible = bibleRow(state.bible.id);
    const fragments = await T.fetchFragments(bible, T.citationsOf(mass));
    if (!isCurrent()) return false;
    const documentFragment = document.createDocumentFragment();
    const contents = [];
    const branchLocus = prefix && branch && branch.option
      ? T.titleCase(String(branch.option).replace(/-/g, ' ')) : null;

    const uncompiled = T.massIsUncompiled(mass) ? T.uncompiledNote(mass) : null;
    if (mode === 'missal') {
      renderMissalDocument(
        documentFragment, contents, result, mass, structure, bible,
        fragments.fragments, state, ordinary, prefix, branchLocus
      );
    } else {
      (result.events || []).forEach(function (event) {
        if (event.kind !== 'proper') return;
        const index = sourceIndex(event);
        const proper = index === null ? null : (mass.propers || [])[index];
        if (!proper || T.isPlaceholder(proper)) return;
        const section = renderProperEvent(event, proper, index, structure, bible,
          fragments.fragments, state, 'h2', prefix, result);
        exposeReaderLocus(section, branchLocus ? branchLocus + ' · Propers' : 'Propers',
          event.editionSlotLabel || proper.name || 'Proper');
        documentFragment.appendChild(section);
        contents.push({
          id: prefix + event.id,
          label: event.editionSlotLabel || proper.name || 'Proper',
          element: section,
          group: 'Proper of the Mass'
        });
      });
    }

    const notice = coverageMessage(result);
    return {
      branch: branch,
      result: result,
      fragment: documentFragment,
      contents: contents,
      bible: bible,
      uncompiled: uncompiled,
      notice: notice
    };
  }

  function branchHeading(branch, ordinal) {
    const heading = T.el('header', 'territorial-branch-heading');
    const identity = T.titleCase(String(branch.option || 'universal').replace(/-/g, ' '));
    heading.appendChild(T.el('p', 'territorial-branch-label', 'Territorial branch · ' + identity));
    const resultTitle = T.el('h2', null,
      branch.winner && branch.winner.name || 'Branch result unavailable');
    resultTitle.id = 'territorial-branch-' + String(ordinal + 1).padStart(2, '0');
    heading.appendChild(resultTitle);
    return { node: heading, titleId: resultTitle.id, identity: identity };
  }

  function commitResultDocuments(rows, assembled, state, showWhy) {
    const multiple = rows.length > 1;
    const hasUnresolved = rows.some(function (row) {
      return row.unresolved || Boolean(
        row.result && (row.result.unresolvedChoices || []).length
      );
    });
    const documentFragment = document.createDocumentFragment();
    const contents = [];
    rows.forEach(function (row, ordinal) {
      if (multiple) {
        const branch = document.createElement('section');
        branch.className = 'territorial-branch';
        branch.dataset.territorialBranch = row.branch.option;
        const heading = branchHeading(row.branch, ordinal);
        branch.setAttribute('aria-labelledby', heading.titleId);
        branch.appendChild(heading.node);
        branch.appendChild(row.fragment);
        if (showWhy) branch.appendChild(reasoningApparatus(
          row.branch, assembled.rubrics, assembled.structure, row.result, runtime.ordinary));
        documentFragment.appendChild(branch);
        row.contents.forEach(function (entry) {
          contents.push(Object.assign({}, entry, { group: heading.identity + ' · ' + entry.group }));
        });
      } else {
        documentFragment.appendChild(row.fragment);
        if (showWhy) documentFragment.appendChild(reasoningApparatus(
          row.branch, assembled.rubrics, assembled.structure, row.result, runtime.ordinary));
        row.contents.forEach(function (entry) { contents.push(entry); });
      }
    });
    reading.replaceChildren(documentFragment);
    reading.setAttribute('aria-busy', 'false');
    readerShell.setContents(contents);

    const missal = missalRow(state.edition.id);
    const bible = rows[0] && rows[0].bible;
    title.textContent = multiple
      ? 'Held territorial branches'
      : (rows[0].branch.winner && rows[0].branch.winner.name || 'No day is settled here');
    dateLine.textContent = longDate(assembled.derived.date, assembled.derived.weekday);
    const metadata = [
      missal && (missal.edition || missal.label),
      multiple ? rows.length + ' source-defined territorial results' : (rows[0].branch.option || 'Universal'),
      bible && bible.label,
      humanLanguage(state.languages.orations) + ' orations'
    ];
    if (runtime.mode === 'missal') {
      metadata.push(humanLanguage(state.languages.ordinary || 'en') + ' Ordinary');
      metadata.push(selectedOrdinaryOptionLabel(state, runtime.ordinary));
    }
    commitOutcomePresentation({
      mode: runtime.mode,
      outcome: hasUnresolved ? 'unresolved' : 'ready',
      outcomeClass: hasUnresolved ? 'unresolved' : 'ready',
      metadata: metadata.filter(Boolean).join(' · ')
    });
    document.title = multiple
      ? 'Territorial results — Day — Triptych'
      : title.textContent + ' — Day — Triptych';
    refreshDetailsAfterOutcome();

    const notices = rows.map(function (row) { return row.notice; }).filter(Boolean);
    const uncompiled = rows.map(function (row) { return row.uncompiled; }).filter(Boolean);
    if (uncompiled.length) {
      coverageNotice.textContent = multiple
        ? 'One or more held territorial results are not fully compiled; each available portion remains identified.'
        : uncompiled[0].textContent;
      coverageNotice.hidden = false;
    } else {
      coverageNotice.textContent = notices.length
        ? Array.from(new Set(notices)).join(' ') : '';
      coverageNotice.hidden = !notices.length;
    }
  }

  function semanticNode(node, event, ordinal, prefix) {
    const heldPrefix = prefix || '';
    node.dataset.semanticLocation = heldPrefix + event.id;
    node.dataset.semanticEventId = event.id;
    node.tabIndex = -1;
    node.id = 'reader-event-' + (heldPrefix ? heldPrefix.replace(/[^a-z0-9]+/gi, '-') : '') +
      String(ordinal + 1).padStart(3, '0');
    return node;
  }

  function exposeReaderLocus(node, major, unit) {
    if (!node || !major) return node;
    node.dataset.readerLocusMajor = major;
    if (unit) node.dataset.readerLocusUnit = unit;
    else delete node.dataset.readerLocusUnit;
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

  function renderTranslationWitnessChoice(event, witnessState, prefix) {
    if (!event.selected || event.selected.availability !== 'choice-required' ||
        !witnessState.choices.length) return null;
    const fieldset = T.el('fieldset', 'ordinary-choice translation-witness-choice');
    fieldset.dataset.translationWitnessChoice = event.id;
    fieldset.appendChild(T.el('legend', null,
      'Choose a translation witness for ' + (event.editionSlotLabel || 'this Proper')));
    fieldset.appendChild(T.el('p', 'ordinary-choice-note',
      'This witness will be used only when it faithfully supplies every translated Proper in this formulary.'));
    const options = T.el('div', 'ordinary-choice-options');
    witnessState.choices.forEach(function (option) {
      const label = T.el('label', 'ordinary-choice-option');
      const input = document.createElement('input');
      input.type = 'radio';
      input.name = 'reader-' + (prefix || '').replace(/[^a-z0-9]+/gi, '-') +
        event.id.replace(/[^a-z0-9]+/gi, '-') + '-translation-witness';
      input.value = option.id;
      input.dataset.translationWitness = option.id;
      input.addEventListener('change', function () {
        if (!input.checked) return;
        const location = { kind: 'event', id: (prefix || '') + event.id };
        navigate({ 'translation-witness': option.id }, [], {
          location: location,
          focus: { kind: 'translation-witness-result', event: location.id }
        });
      });
      label.appendChild(input);
      label.appendChild(document.createTextNode(option.label));
      options.appendChild(label);
    });
    fieldset.appendChild(options);
    return fieldset;
  }

  function renderProperEvent(event, proper, index, structure, bible, fragments, state, heading, prefix, result) {
    const section = T.renderProper(proper, bible, fragments, {
      numbering: structure.numbering || null,
      orations: state.languages.orations,
      translationWitness: state.languages.translationWitness || null,
      heading: heading,
      cycle: event.selected && event.selected.cycle || null
    });
    const choice = renderTranslationWitnessChoice(
      event, resolvableTranslationWitnessState(result, structure, state), prefix
    );
    if (choice) section.appendChild(choice);
    return semanticNode(section, event, index, prefix);
  }

  function renderMissalDocument(fragment, contents, result, mass, structure, bible, fragments, state, ordinary, prefix, branchLocus) {
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
    let currentDivision = null;
    function namedDivision(name) {
      return branchLocus ? branchLocus + ' · ' + name : name;
    }
    const frame = OrdinaryRenderer.renderSemanticFrame(result.events, {
      section: function (event) {
        const ordinal = ordinals.get(event.id);
        const raw = sections.get(event.id.replace(/^ordinary-section\//, ''));
        if (!raw) throw new Error('production Ordinary section is missing for ' + event.id);
        currentDivision = raw.name;
        const node = exposeReaderLocus(
          semanticNode(T.el('h2', 'mass-subheading ordinary-division', raw.name), event, ordinal, prefix),
          namedDivision(raw.name), null
        );
        contents.push({ id: prefix + event.id, label: raw.name, element: node, group: 'Rites and divisions' });
        return node;
      },
      element: function (event) {
        const ordinal = ordinals.get(event.id);
        const raw = elements.get(event.id.replace(/^ordinary-element\//, ''));
        if (!raw) throw new Error('production Ordinary element is missing for ' + event.id);
        const node = exposeReaderLocus(
          semanticNode(
            composeInstrumentAbsences(OrdinaryRenderer.renderElement(raw, ordinary)),
            event,
            ordinal,
            prefix
          ),
          namedDivision(currentDivision || ordinary.title || 'Order of Mass'),
          raw.name || null
        );
        if (!optionListed && group && raw.variant) {
          optionListed = true;
          const choice = renderOrdinaryChoice(group, selectedOption, event, prefix, ordinary);
          contents.push({
            id: prefix + event.id,
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
        const anchor = event.seat && event.seat.anchor || '';
        const seatedSection = sections.get(anchor.split('/')[0]);
        const node = exposeReaderLocus(
          renderProperEvent(event, proper, ordinal, structure, bible, fragments, state, 'h3', prefix, result),
          namedDivision(seatedSection && seatedSection.name || currentDivision || 'Appointed propers'),
          event.editionSlotLabel || proper.name || 'Proper'
        );
        contents.push({
          id: prefix + event.id,
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

  function renderOrdinaryChoice(group, selected, event, prefix, ordinary) {
    const fieldset = T.el('fieldset', 'ordinary-choice');
    fieldset.dataset.optionGroup = group.group;
    fieldset.dataset.optionBranch = prefix || '';
    fieldset.appendChild(T.el('legend', null, group.name));
    fieldset.appendChild(T.el('p', 'ordinary-choice-note',
      'This source-defined choice belongs here in the liturgical sequence.'));
    const options = T.el('div', 'ordinary-choice-options');
    (group.options || []).forEach(function (option) {
      const semanticKeys = [];
      (ordinary.sections || []).forEach(function (section) {
        (section.elements || []).forEach(function (element) {
          if (element.variant === option.id) semanticKeys.push(element.key);
        });
      });
      if (semanticKeys.length !== 1) {
        throw new Error('Ordinary option has no unique semantic element: ' + option.id);
      }
      const label = T.el('label', 'ordinary-choice-option');
      const input = document.createElement('input');
      input.type = 'radio';
      input.name = 'reader-' + (prefix || '').replace(/[^a-z0-9]+/gi, '-') + group.group;
      input.value = option.id;
      input.checked = Boolean(selected && selected.id === option.id);
      input.addEventListener('change', function () {
        if (!input.checked) return;
        const location = {
          kind: 'event',
          id: (prefix || '') + 'ordinary-element/' + semanticKeys[0]
        };
        navigate({ mode: 'missal', [group.group]: option.id }, ['ordinary'], {
          location: location,
          focus: {
            kind: 'ordinary-option', group: group.group, option: option.id,
            branch: prefix || ''
          }
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
    document.title = 'Day — Triptych';
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
      const variantErrors = await validateExplicitVariants(
        parsed, manifests, preliminary.missal
      );
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
          bible: Contract.defaultBibleId(runtime.bibles),
          orations: T.SOURCE_LANGUAGE
        }
      });
      if (!normalized.ok) {
        renderFailure(normalized.errors, { mode: requestedMode });
        return;
      }
      const validation = Contract.validateReaderState(normalized.state);
      if (!validation.ok) {
        renderFailure(validation.errors, { mode: requestedMode });
        return;
      }
      const witnessErrors = validateExplicitTranslationWitness(
        normalized.state, assembled.derived, assembled.structure
      );
      if (witnessErrors.length) {
        renderFailure(witnessErrors, { mode: requestedMode });
        return;
      }
      runtime.normalized = normalized;
      runtime.derived = assembled.derived;
      runtime.rubrics = assembled.rubrics;
      runtime.structure = assembled.structure;
      runtime.mode = normalized.state.requestedMode;
      runtime.ordinary = runtime.mode === 'missal' ? assembled.ordinary : null;
      runtime.branch = assembled.derived.options.length === 1 ? assembled.derived.options[0] : null;
      runtime.branches = [];
      runtime.deferred = deferredState(parsed);
      window.dayReaderDebug.state = normalized.state;
      window.dayReaderDebug.deferred = runtime.deferred.slice();
      window.dayReaderDebug.legacy = normalized.legacy;
      if (!pendingNavigation.location && normalized.state.semanticLocation) {
        pendingNavigation.location = {
          kind: 'event', id: normalized.state.semanticLocation.eventId
        };
      }
      const canonicalPath = Contract.canonicalRoute('day', window.location.pathname);
      const canonicalHash = Contract.serializeLegacy(normalized);
      if (window.location.pathname !== canonicalPath || window.location.hash !== canonicalHash) {
        history.replaceState(history.state, '',
          canonicalPath + window.location.search + canonicalHash);
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
          'The reader preserved ' + runtime.deferred.join(', ') +
            ' but did not partially render it.'
        ));
        title.textContent = runtime.branch && runtime.branch.winner
          ? runtime.branch.winner.name : 'Deferred Day selection';
        dateLine.textContent = longDate(assembled.derived.date, assembled.derived.weekday);
        return;
      }

      const multiple = assembled.derived.options.length > 1;
      const rendered = [];
      let branchFailures = 0;
      const branchErrors = [];
      try {
        for (let branchIndex = 0; branchIndex < assembled.derived.options.length; branchIndex += 1) {
          const branch = assembled.derived.options[branchIndex];
          const branchState = resultStateForBranch(normalized.state, branch, multiple);
          const prefix = locationPrefix(branch, multiple);
          try {
            const result = Adapters.adaptDay({
              request: branchState,
              derived: assembled.derived,
              structure: assembled.structure,
              ordinary: runtime.ordinary
            });
            if (primaryDayChoice(result, branch)) {
              const row = {
                branch: branch, result: result, prefix: prefix, state: branchState,
                unresolved: true
              };
              rendered.push(row);
              continue;
            }
            if (!result.resolved) {
              throw new Error('the production result leaves its formulary unresolved');
            }
            const row = await buildResultDocument(
              result, assembled.structure, branch,
              {
                state: branchState,
                mode: runtime.mode,
                ordinary: runtime.ordinary,
                locationPrefix: prefix
              },
              function () { return serial === runtime.serial; }
            );
            if (!row || serial !== runtime.serial) return;
            row.prefix = prefix;
            row.state = branchState;
            rendered.push(row);
          } catch (error) {
            branchFailures += 1;
            branchErrors.push(error);
            rendered.push(failedBranchDocument(branch, prefix, error));
          }
        }
      } catch (error) {
        if (serial !== runtime.serial) return;
        renderFailure([{ code: 'candidate-unrenderable', path: '', message: String(error.message || error) }], {
          mode: runtime.mode,
          outcome: 'unrenderable',
          outcomeClass: 'unrenderable',
          preserveSelection: true,
          heading: 'This valid Day selection cannot be rendered',
          explanation: 'The reader stopped rather than inventing a missing resource, semantic seat, option, or liturgical text.'
        });
        return;
      }
      if (!rendered.length || serial !== runtime.serial) return;
      if (branchFailures === rendered.length) {
        throw branchErrors[0];
      }
      const unresolved = rendered.filter(function (row) { return row.unresolved; });
      if (unresolved.length) {
        if (rendered.length === 1 && !branchFailures) {
          runtime.branches = [{
            branch: unresolved[0].branch,
            result: unresolved[0].result,
            prefix: unresolved[0].prefix
          }];
          runtime.branch = unresolved[0].branch;
          runtime.result = unresolved[0].result;
          commitUnresolvedChoice(
            unresolved[0].result, unresolved[0].branch, assembled, normalized.state
          );
          populateDateSurface();
          window.dayReaderDebug.semantic = semanticProjection(unresolved[0].result);
          restorePendingNavigation(pendingNavigation);
          if (modeStartedAt !== null) {
            window.dayReaderDebug.lastModeSwitchMs = performance.now() - modeStartedAt;
          }
          return;
        }
        unresolved.forEach(function (row) {
          Object.assign(row, unresolvedBranchDocument(
            row.result, row.branch, assembled.structure, row.prefix
          ));
        });
      }
      runtime.branches = rendered.map(function (row) {
        return { branch: row.branch, result: row.result, prefix: row.prefix };
      });
      runtime.branch = multiple ? null : rendered[0].branch;
      runtime.result = multiple ? null : rendered[0].result;
      commitResultDocuments(
        rendered, assembled, normalized.state,
        Boolean(normalized.state.apparatus && normalized.state.apparatus.why)
      );
      populateDateSurface();
      window.dayReaderDebug.semantic = multiple
        ? rendered.map(function (row) {
          return {
            territory: row.branch.option,
            prefix: row.prefix,
            document: semanticProjection(row.result)
          };
        })
        : semanticProjection(rendered[0].result);
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
        heading: 'The Day reader could not load this selection',
        explanation: 'The requested mode is valid, but the reader could not obtain a required production resource and did not substitute another one.'
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
    Object.keys(updates || {}).forEach(function (key) {
      const value = updates[key];
      if (value === null || value === undefined || value === '') params.delete(key);
      else params.set(key, value);
    });
    // Removals LAST, and they win. Applied first they died the moment an update
    // named the same key: Apply asks for `mass` to go whenever the day or the
    // missal changes, then wrote the outgoing missal's own formulary key back
    // from a select nothing had repopulated — and no missal holds another's.
    (removals || []).forEach(function (key) { params.delete(key); });
    const value = params.toString();
    return value ? '#' + value : '';
  }

  function navigate(updates, removals) {
    const navigation = arguments.length > 2 && arguments[2] || {};
    const currentLocation = readerShell.captureSemanticLocation();
    history.replaceState(
      Object.assign({}, history.state || {}, { dayReaderLocation: currentLocation }),
      '', window.location.href
    );
    if (Object.prototype.hasOwnProperty.call(navigation, 'location')) {
      runtime.pendingLocation = navigation.location;
      updates.location = navigation.location && navigation.location.kind === 'event'
        ? navigation.location.id : null;
    }
    runtime.pendingModeFocus = navigation.modeFocus === true;
    runtime.pendingFocus = navigation.focus || null;
    window.dayReaderDebug.pendingNavigation = {
      location: runtime.pendingLocation,
      modeFocus: runtime.pendingModeFocus,
      focus: runtime.pendingFocus
    };
    const hash = hashWith(updates, (removals || []).concat(['ordinary']));
    const route = Contract.canonicalRoute('day', window.location.pathname);
    history.pushState(Object.assign({}, history.state || {}, {
      dayReaderLocation: runtime.pendingLocation
    }), '',
      route + window.location.search + hash);
    renderCandidate();
  }

  function nearestProperLocation(location, events) {
    if (!location || location.kind !== 'event') return location;
    let prefix = '';
    let eventId = location.id || '';
    const territorial = /^territory\/[^/]+\//.exec(eventId);
    if (territorial) {
      prefix = territorial[0];
      eventId = eventId.slice(prefix.length);
    }
    if (/^proper\//.test(eventId)) return location;
    let rows = events || [];
    if (prefix) {
      const held = runtime.branches.find(function (row) { return row.prefix === prefix; });
      rows = held && held.result && held.result.events || [];
    }
    const at = rows.findIndex(function (event) { return event.id === eventId; });
    if (at < 0) return { kind: 'top', id: null };
    let best = null;
    rows.forEach(function (event, index) {
      if (event.kind !== 'proper') return;
      const distance = Math.abs(index - at);
      if (!best || distance < best.distance || (distance === best.distance && index < best.index)) {
        best = { id: event.id, distance: distance, index: index };
      }
    });
    return best ? { kind: 'event', id: prefix + best.id } : { kind: 'top', id: null };
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
          group.dataset.optionBranch === (held.focus.branch || '') &&
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
    } else if (held.focus && held.focus.kind === 'day-choice-result') {
      const target = reading.querySelector('[data-semantic-event-id]');
      if (target) target.focus({ preventScroll: true });
    } else if (held.focus && held.focus.kind === 'translation-witness-result') {
      const target = Array.from(reading.querySelectorAll('[data-semantic-location]')).find(
        function (node) { return node.dataset.semanticLocation === held.focus.event; }
      );
      if (target) target.focus({ preventScroll: true });
    } else if (held.modeFocus) {
      modeAction.focus({ preventScroll: true });
    }
  }

  dateForm.addEventListener('submit', function (event) {
    event.preventDefault();
    const previous = runtime.normalized && runtime.normalized.state;
    const nextFormulary = formularyField.hidden ? null : formularySelect.value;
    const changedDay = !previous || previous.civilDate !== dateInput.value ||
      previous.edition.id !== missalSelect.value;
    const previousFormulary = previous && previous.selectedReadableFormulary
      ? previous.selectedReadableFormulary.id : null;
    const changedFormulary = previousFormulary !== nextFormulary;
    const changedOrations = !previous || previous.languages.orations !== orationsSelect.value;
    const updates = {
      date: dateInput.value,
      missal: missalSelect.value,
      bible: bibleSelect.value,
      orations: orationsSelect.value,
      mass: nextFormulary
    };
    if (!ordinaryLangField.hidden) updates['ordinary-lang'] = ordinaryLangSelect.value;
    if (!ordinaryOptionField.hidden && runtime.ordinary) {
      const group = window.OrdinarySeating.variantGroupOf(runtime.ordinary);
      if (group) updates[group.group] = ordinaryOptionSelect.value;
    }
    readerShell.close({ restoreFocus: false });
    navigate(updates, changedDay ? ['mass', 'form', 'translation-witness', 'location'] :
      (changedFormulary ? ['form', 'translation-witness', 'location'] :
        (changedOrations ? ['translation-witness'] : [])));
  });

  document.getElementById('previous-date').addEventListener('click', function () {
    if (!runtime.normalized) return;
    readerShell.close({ restoreFocus: false });
    navigate({ date: Model.shift(runtime.normalized.state.civilDate, -1), mass: null,
      form: null, 'translation-witness': null, location: null },
      ['mass', 'form', 'translation-witness', 'location']);
  });
  document.getElementById('today-date').addEventListener('click', function () {
    readerShell.close({ restoreFocus: false });
    navigate({ date: todayISO(), mass: null, form: null, 'translation-witness': null,
      location: null }, ['mass', 'form', 'translation-witness', 'location']);
  });
  document.getElementById('next-date').addEventListener('click', function () {
    if (!runtime.normalized) return;
    readerShell.close({ restoreFocus: false });
    navigate({ date: Model.shift(runtime.normalized.state.civilDate, 1), mass: null,
      form: null, 'translation-witness': null, location: null },
      ['mass', 'form', 'translation-witness', 'location']);
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
    navigate({ mode: 'read' }, ['ordinary'], { location: location, modeFocus: true });
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
    navigate({ mode: 'missal' }, ['ordinary'], { location: location, modeFocus: true });
  });
  let historyRenderTimer = null;
  function scheduleHistoryRender() {
    if (historyRenderTimer !== null) return;
    historyRenderTimer = window.setTimeout(function () {
      historyRenderTimer = null;
      renderCandidate();
    }, 0);
  }
  window.addEventListener('popstate', function (event) {
    const hasLocation = event.state &&
      Object.prototype.hasOwnProperty.call(event.state, 'dayReaderLocation');
    runtime.pendingLocation = hasLocation
      ? event.state.dayReaderLocation : null;
    runtime.pendingModeFocus = false;
    runtime.pendingFocus = null;
    window.dayReaderDebug.pendingNavigation = {
      location: runtime.pendingLocation,
      modeFocus: false,
      focus: null
    };
    scheduleHistoryRender();
  });
  window.addEventListener('hashchange', function () {
    if (!window.dayReaderDebug.ready) return;
    scheduleHistoryRender();
  });

  T.setInlineNotice(
    'No data root could be reached at "' + T.dataRoot + '", so the Day reader has nothing to derive from.'
  );
  renderCandidate();
}());
