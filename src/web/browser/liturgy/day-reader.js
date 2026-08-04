/* Internal W3 Day Read candidate over production assembly, state, and renderer. */
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

  if (!T || !Model || !Contract || !Adapters || !Shell) {
    throw new Error('Day reader candidate requires production browser, assembly, state, adapter, and shell modules');
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
  const WEEKDAYS = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'];

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

  const cache = new Map();
  const runtime = {
    manifests: null,
    normalized: null,
    result: null,
    derived: null,
    structure: null,
    missals: [],
    bibles: [],
    branch: null,
    detailsLoaded: false,
    deferred: [],
    serial: 0
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
    error: null
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
    return (WEEKDAYS[weekday] || '') + ' ' + Number(parts[2]) + ' ' +
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

  function renderFailure(errors, heading) {
    const section = T.el('section', 'candidate-failure');
    section.appendChild(T.el('h2', null, heading || 'This explicit selection is invalid'));
    section.appendChild(T.el('p', null,
      'The candidate did not substitute another edition, date, Bible, language, locality, or formulary.'));
    const list = T.el('ul');
    (errors || []).forEach(function (error) {
      const label = error.path ? error.path + ': ' : '';
      list.appendChild(T.el('li', null, label + (error.message || String(error))));
    });
    section.appendChild(list);
    replaceReading(section);
    title.textContent = 'Selection unavailable';
    dateLine.textContent = '';
    metaLine.textContent = 'Internal Day Read candidate · explicit state rejected';
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
    if (recognized.ordinary === '1') reasons.push('the requested Ordinary');
    if (parsed.present.indexOf('ordinary-lang') >= 0) reasons.push('the requested Ordinary language');
    if (parsed.present.indexOf('rubrics') >= 0) reasons.push('the requested rubric presentation');
    if (recognized.why === '1') reasons.push('the current Day reasoning apparatus');
    (parsed.variantKeys || []).forEach(function (key) {
      if (parsed.present.indexOf(key) >= 0) reasons.push('the requested ' + key + ' option');
    });
    return reasons;
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
    const derived = Model.derive({ date: preliminary.date, rubrics: rows[0], year: rows[1] });
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

  function populateDateSurface() {
    const state = runtime.normalized && runtime.normalized.state;
    T.fillSelect(missalSelect, runtime.missals.map(function (row) {
      return { value: row.id, label: row.label, title: row.edition || row.code || row.id };
    }));
    T.fillBibleSelect(bibleSelect, runtime.bibles);
    if (!state || !runtime.structure) return;
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
      detailsBody.appendChild(T.el('p', 'surface-note', 'No validated selection is available.'));
      return;
    }
    const missal = missalRow(state.edition.id);
    const bible = bibleRow(state.bible.id);
    const selection = T.el('section', 'details-section');
    selection.appendChild(T.el('h3', null, 'Selection'));
    selection.appendChild(definitionList([
      ['Date', state.civilDate],
      ['Missal', missal && (missal.edition || missal.label) || state.edition.id],
      ['Locality', runtime.branch && runtime.branch.option || 'Universal'],
      ['Bible', bible && bible.label || state.bible.id],
      ['Orations', humanLanguage(state.languages.orations)],
      ['Formulary', runtime.result && runtime.result.resolved && runtime.result.resolved.formulary]
    ]));
    detailsBody.appendChild(selection);

    if (runtime.result) {
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

      const hooks = [];
      (runtime.result.events || []).forEach(function (event) {
        (event.sourceHooks || []).forEach(function (hook) {
          const value = hook.kind + ': ' + hook.id;
          if (hooks.indexOf(value) < 0) hooks.push(value);
        });
      });
      const source = T.el('section', 'details-section');
      source.appendChild(T.el('h3', null, 'Available source identities'));
      if (hooks.length) {
        const list = T.el('ul');
        hooks.forEach(function (hook) { list.appendChild(T.el('li', 'source-identifier', hook)); });
        source.appendChild(list);
      } else {
        source.appendChild(T.el('p', 'surface-note', 'No additional source identity is exposed for this selection.'));
      }
      detailsBody.appendChild(source);
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
      return 'Part of this selection is outside the candidate’s supported Read boundary.';
    }
    if (rows.some(function (row) { return row.completeness === 'partial'; })) {
      return 'Some appointed text is not held in this repository; the available portions are shown.';
    }
    return 'This selection has a material coverage limitation.';
  }

  async function renderResult(result, structure, derived, branch) {
    const state = runtime.normalized.state;
    const mass = (structure.masses || []).find(function (row) {
      return result.resolved && row.key === result.resolved.formulary;
    });
    if (!mass) throw new Error('the validated resolved formulary is absent from production Proper data');
    const bible = bibleRow(state.bible.id);
    const fragments = await T.fetchFragments(bible, T.citationsOf(mass));
    const documentFragment = document.createDocumentFragment();
    const contents = [];

    if (T.massIsUncompiled(mass)) documentFragment.appendChild(T.uncompiledNote(mass));
    (result.events || []).forEach(function (event) {
      if (event.kind !== 'proper') return;
      const index = sourceIndex(event);
      const proper = index === null ? null : (mass.propers || [])[index];
      if (!proper || T.isPlaceholder(proper)) return;
      const section = T.renderProper(proper, bible, fragments.fragments, {
        numbering: structure.numbering || null,
        orations: state.languages.orations,
        heading: 'h2',
        cycle: event.selected && event.selected.cycle || null
      });
      section.dataset.semanticLocation = event.id;
      section.dataset.semanticEventId = event.id;
      section.tabIndex = -1;
      const id = 'reader-event-' + String(index + 1).padStart(3, '0');
      section.id = id;
      documentFragment.appendChild(section);
      contents.push({ id: event.id, label: event.editionSlotLabel || proper.name || 'Proper', element: section });
    });

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
    metaLine.textContent = metadata.filter(Boolean).join(' · ');
    const notice = coverageMessage(result);
    coverageNotice.textContent = notice || '';
    coverageNotice.hidden = !notice;
  }

  async function renderCandidate() {
    const serial = ++runtime.serial;
    window.dayReaderReady = false;
    window.dayReaderDebug.ready = false;
    window.dayReaderDebug.error = null;
    window.dayReaderDebug.semantic = null;
    reading.setAttribute('aria-busy', 'true');
    coverageNotice.hidden = true;
    runtime.detailsLoaded = false;
    detailsBody.replaceChildren(T.el('p', 'surface-note', 'Details load when this surface is opened.'));
    if (readerShell.openSurface()) readerShell.close({ restoreFocus: false });

    try {
      const manifests = await loadManifests();
      if (serial !== runtime.serial) return;
      const keys = variantKeys(manifests.ordinaryIndex);
      const parsed = Contract.parseLegacy('day', window.location.hash, { variantKeys: keys });
      const preliminary = preflightSelection(parsed, manifests);
      if (!preliminary.ok) {
        renderFailure(preliminary.errors);
        populateDateSurface();
        return;
      }
      const assembled = await assemble(parsed, manifests, preliminary);
      if (serial !== runtime.serial) return;
      runtime.derived = assembled.derived;
      runtime.structure = assembled.structure;
      runtime.branch = assembled.derived.options.length === 1 ? assembled.derived.options[0] : null;

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
        runtime.normalized = null;
        renderFailure(normalized.errors);
        populateDateSurface();
        return;
      }
      normalized.state.requestedMode = 'read';
      const validation = Contract.validateReaderState(normalized.state);
      if (!validation.ok) {
        runtime.normalized = null;
        renderFailure(validation.errors);
        return;
      }
      runtime.normalized = normalized;
      runtime.result = null;
      runtime.deferred = deferredState(parsed);
      window.dayReaderDebug.state = normalized.state;
      window.dayReaderDebug.deferred = runtime.deferred.slice();
      populateDateSurface();

      if (assembled.derived.options.length !== 1) {
        replaceReading(limitation(
          'Territorial branch requires the current Day reader',
          'This date resolves to more than one territorial branch, and the accepted Day legacy URL contract carries no locality key. The candidate did not choose by array order or geography.'
        ));
        title.textContent = 'Locality required';
        dateLine.textContent = longDate(assembled.derived.date, assembled.derived.weekday);
        metaLine.textContent = missalRow(normalized.state.edition.id).edition;
        return;
      }

      if (runtime.deferred.length) {
        replaceReading(limitation(
          'This selection belongs to a later integration slice',
          'The candidate preserved ' + runtime.deferred.join(', ') +
            ' but did not partially render or map it to Read. The unchanged current Day reader remains the faithful route for this request.'
        ));
        title.textContent = runtime.branch && runtime.branch.winner
          ? runtime.branch.winner.name : 'Deferred Day selection';
        dateLine.textContent = longDate(assembled.derived.date, assembled.derived.weekday);
        metaLine.textContent = 'Read candidate limitation · explicit state preserved';
        return;
      }

      let result;
      try {
        result = Adapters.adaptDay({
          request: normalized.state,
          derived: assembled.derived,
          structure: assembled.structure,
          ordinary: null
        });
      } catch (error) {
        replaceReading(limitation(
          'This Day choice is not resolved by the candidate',
          String(error.message || error) + ' No formulary was selected implicitly.'
        ));
        title.textContent = runtime.branch && runtime.branch.winner
          ? runtime.branch.winner.name : 'Unresolved Day selection';
        dateLine.textContent = longDate(assembled.derived.date, assembled.derived.weekday);
        metaLine.textContent = 'Read candidate limitation · no silent fallback';
        return;
      }
      runtime.result = result;
      if (!result.resolved) {
        replaceReading(limitation(
          'A formulary choice remains unresolved',
          'The production calendar result authorizes more than one choice. The candidate has preserved that state and selected none.'
        ));
        title.textContent = runtime.branch && runtime.branch.winner
          ? runtime.branch.winner.name : 'Unresolved Day selection';
        dateLine.textContent = longDate(assembled.derived.date, assembled.derived.weekday);
        metaLine.textContent = 'Read candidate limitation · choice required';
        return;
      }
      await renderResult(result, assembled.structure, assembled.derived, runtime.branch);
      if (serial !== runtime.serial) return;
      window.dayReaderDebug.semantic = semanticProjection(result);
    } catch (error) {
      renderFailure([{ code: 'candidate-load', path: '', message: String(error.message || error) }],
        'The Day candidate could not load this selection');
    } finally {
      if (serial === runtime.serial) {
        window.dayReaderDebug.renders += 1;
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
    const hash = hashWith(updates, removals);
    history.pushState(null, '', window.location.pathname + window.location.search + hash);
    renderCandidate();
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
    readerShell.close();
  });
  window.addEventListener('popstate', renderCandidate);
  window.addEventListener('hashchange', function () {
    if (!window.dayReaderDebug.ready) return;
    renderCandidate();
  });

  T.setInlineNotice(
    'No data root could be reached at "' + T.dataRoot + '", so the internal Day reader candidate has nothing to derive from.'
  );
  renderCandidate();
}());
