/* Production Propers Read controller over production state and renderer paths. */
'use strict';

(function () {
  const T = window.Triptych;
  const Contract = window.LiturgyReaderState;
  const Adapters = window.LiturgyReaderStateAdapters;
  const Shell = window.TriptychReaderShell;

  if (!T || !Contract || !Adapters || !Shell) {
    throw new Error('Propers reader requires production browser, state, adapter, and shell modules');
  }

  const PROPERS_INDEX = 'structure/propers/index.json';
  const PUBLIC_KEYS = Object.freeze({
    cycle: 'cycle', alternative: 'alternative', translationWitness: 'translation-witness'
  });
  const LEGACY_KEYS = Object.freeze({
    cycle: '_candidate-cycle',
    alternative: '_candidate-alternative',
    translationWitness: '_candidate-translation-witness'
  });
  const KIND_SEQUENCE = ['seasonal', 'christological', 'marian', 'sanctoral'];
  const KIND_LABELS = {
    seasonal: 'Seasonal', christological: 'Christological',
    marian: 'Marian', sanctoral: 'Sanctoral'
  };
  const MONTHS = [
    'January', 'February', 'March', 'April', 'May', 'June',
    'July', 'August', 'September', 'October', 'November', 'December'
  ];

  const shellRoot = document.querySelector('[data-reader-shell]');
  const reading = document.getElementById('reader-document');
  const title = document.getElementById('formulary-title');
  const typeLine = document.getElementById('formulary-type');
  const metaLine = document.getElementById('formulary-meta');
  const sourceLine = document.getElementById('formulary-source');
  const coverageNotice = document.getElementById('coverage-notice');
  const detailsBody = document.querySelector('[data-reader-details]');
  const browseForm = document.getElementById('browse-form');
  const browseSurface = document.getElementById('browse-surface');
  const browseStatus = document.getElementById('browse-status');
  const contentsList = document.querySelector('[data-reader-contents]');
  const missalSelect = document.getElementById('reader-missal');
  const typeSelect = document.getElementById('reader-type');
  const formularySelect = document.getElementById('reader-formulary');
  const bibleSelect = document.getElementById('reader-bible');
  const orationsSelect = document.getElementById('reader-orations');
  const witnessField = document.getElementById('reader-witness-field');
  const witnessSelect = document.getElementById('reader-witness');

  const cache = new Map();
  const runtime = {
    manifests: null,
    missals: [],
    bibles: [],
    structure: null,
    groups: [],
    normalized: null,
    result: null,
    mass: null,
    detailsLoaded: false,
    outcome: 'loading',
    serial: 0,
    browseSerial: 0,
    pendingLocation: null,
    pendingLocationSet: false,
    pendingFocus: null,
    preferredType: null,
    draftStructure: null,
    draftGroups: []
  };

  window.propersReaderDebug = {
    candidate: true,
    shellBehavior: 'persistent',
    ready: false,
    renders: 0,
    detailsBuilds: 0,
    loads: {},
    state: null,
    semantic: null,
    legacy: null,
    outcome: 'loading',
    error: null,
    publicKeys: PUBLIC_KEYS,
    legacyInputAliases: LEGACY_KEYS
  };

  function load(path) {
    if (!cache.has(path)) {
      window.propersReaderDebug.loads[path] = (window.propersReaderDebug.loads[path] || 0) + 1;
      cache.set(path, T.loadJSON(path));
    }
    return cache.get(path);
  }

  function structurePath(id) {
    return 'structure/propers/' + id + '.json';
  }

  function described(entry) {
    if (typeof entry === 'string') return { id: entry, label: T.titleCase(entry), edition: null };
    return {
      id: entry.id,
      label: entry.edition_short || entry.label || entry.edition || T.titleCase(entry.id),
      edition: entry.edition || null
    };
  }

  function allowedMissals(index) {
    const rows = ((index && (index.missals || index.calendars)) || []).map(described);
    const override = T.params.get('missals');
    if (!override) return rows;
    return override.split(',').map(function (id) { return id.trim(); }).filter(Boolean).map(function (id) {
      return rows.find(function (row) { return row.id === id; }) || described(id);
    });
  }

  async function loadManifests() {
    if (runtime.manifests) return runtime.manifests;
    const loaded = await Promise.all([T.loadBibles(), load(PROPERS_INDEX)]);
    if (!loaded[0].ok) throw new Error(loaded[0].message);
    runtime.bibles = loaded[0].bibles;
    runtime.missals = allowedMissals(loaded[1]);
    if (!runtime.missals.length) throw new Error('the selected data root offers no Propers editions');
    const declared = loaded[1] && loaded[1].default;
    const landing = runtime.missals.some(function (row) { return row.id === declared; })
      ? declared : runtime.missals[0].id;
    runtime.manifests = {
      bibles: { bibles: runtime.bibles },
      properIndex: { default: landing, missals: runtime.missals.map(function (row) {
        return { id: row.id, edition: row.edition, edition_short: row.label };
      }) }
    };
    return runtime.manifests;
  }

  function massDate(mass) {
    const found = /^(\d{2})-(\d{2})$/.exec(String((mass && mass.date) || ''));
    if (!found) return null;
    const month = Number(found[1]);
    const day = Number(found[2]);
    return month >= 1 && month <= 12 && day >= 1 && day <= 31 ? [month, day] : null;
  }

  function massGroup(mass) {
    if (mass.season) return T.titleCase(mass.season);
    const date = massDate(mass);
    return date ? MONTHS[date[0] - 1] : null;
  }

  function groupByKind(masses) {
    const held = new Map();
    (masses || []).forEach(function (mass) {
      const kind = mass.kind || 'other';
      if (!held.has(kind)) held.set(kind, []);
      held.get(kind).push(mass);
    });
    const keys = KIND_SEQUENCE.filter(function (kind) { return held.has(kind); }).concat(
      Array.from(held.keys()).filter(function (kind) { return KIND_SEQUENCE.indexOf(kind) < 0; })
    );
    return keys.map(function (kind) {
      return { kind: kind, label: KIND_LABELS[kind] || T.titleCase(kind), masses: held.get(kind) };
    });
  }

  function missalRow(id) {
    return runtime.missals.find(function (row) { return row.id === id; }) || null;
  }

  function bibleRow(id) {
    return runtime.bibles.find(function (row) { return row.id === id; }) || null;
  }

  function groupRow(kind) {
    return runtime.groups.find(function (row) { return row.kind === kind; }) || null;
  }

  function editionName(id) {
    const row = missalRow(id);
    return row && (row.edition || row.label) || id;
  }

  function formRow(mass, id) {
    if (!mass || !id) return null;
    return (mass.forms || []).find(function (row) { return row && row.id === id; }) || null;
  }

  function translationWitnessRow(structure, id) {
    if (!structure || !id) return null;
    return (structure.translations || []).find(function (row) {
      return row && (row.source_id || row.source || null) === id;
    }) || null;
  }

  function rightsLabel(value) {
    return value ? T.titleCase(String(value).replace(/-/g, ' ')) : null;
  }

  function sourceStateLabel(value) {
    const held = typeof value === 'string' ? value.trim() : '';
    return held ? held.charAt(0).toUpperCase() + held.slice(1) : null;
  }

  function recensionContext(structure, mass) {
    const boundaries = structure && Array.isArray(structure.stands_before)
      ? structure.stands_before.filter(function (id) {
        return typeof id === 'string' && id;
      }) : [];
    const candidate = structure && structure.recension_coverage;
    const coverage = candidate && typeof candidate === 'object' && !Array.isArray(candidate)
      ? candidate : null;
    const domains = coverage && coverage.domains && typeof coverage.domains === 'object'
      ? coverage.domains : {};
    const properDomain = domains.propers && typeof domains.propers === 'object'
      ? domains.propers : {};
    const inheritance = coverage && coverage.inheritance &&
      typeof coverage.inheritance === 'object' ? coverage.inheritance : {};
    const stamp = mass && mass.recension && typeof mass.recension === 'object'
      ? mass.recension : null;
    if (!coverage && !stamp && !boundaries.length) return null;
    const sourceId = stamp && typeof stamp.text_from === 'string' && stamp.text_from
      ? stamp.text_from : null;
    const additional = stamp && Array.isArray(stamp.also) ? stamp.also.filter(function (row) {
      return row && typeof row === 'object' && typeof row.kind === 'string' && row.kind;
    }) : [];
    const coverageStatus = coverage && coverage.status || null;
    const properStatus = properDomain.state || null;
    const inheritanceStatus = inheritance.status || null;
    const inheritanceSource = inheritance.source_calendar || null;
    const coverageLabel = [
      coverageStatus && sourceStateLabel(coverageStatus) + ' finding aid',
      properStatus && 'Propers: ' + sourceStateLabel(properStatus),
      coverage && coverage.as_of && 'as of ' + coverage.as_of
    ].filter(Boolean).join(' · ') || null;
    const notice = [
      coverageStatus && 'This edition surface is a ' + coverageStatus +
        ' finding aid; recension coverage is dated ' + (coverage.as_of || 'without an as-of date') + '.',
      properStatus && 'Proper wording coverage is ' + properStatus + '.',
      inheritanceStatus && 'Inherited material' +
        (inheritanceSource ? ' from ' + editionName(inheritanceSource) : '') +
        ' remains ' + inheritanceStatus + '.'
    ].filter(Boolean).join(' ') || null;
    return {
      coverage: coverageLabel,
      coverageAsOf: coverage && coverage.as_of || null,
      coverageBasis: properDomain.basis || null,
      inheritanceBasis: inheritance.basis || null,
      notice: notice,
      textSource: sourceId
        ? editionName(sourceId) + ' · inherited ' + (inheritanceStatus || 'uncollated')
        : (stamp && stamp.stated === true
          ? 'Departure stated by this recension; no other calendar supplies this formulary'
          : null),
      departure: stamp && stamp.kind || null,
      departureAct: stamp && stamp.act || null,
      departureBasis: stamp && stamp.basis || null,
      additional: additional,
      boundaries: boundaries,
      boundaryLabel: boundaries.length ? boundaries.join('; ') : null,
      sourceId: sourceId
    };
  }

  function setSourceContext(parts) {
    const rows = (parts || []).filter(Boolean);
    sourceLine.textContent = rows.join(' · ');
    sourceLine.hidden = !rows.length;
  }

  function explicitValues(key) {
    const params = new URLSearchParams(window.location.hash.replace(/^#/, ''));
    return params.getAll(key);
  }

  function explicitSemanticValue(name, errors) {
    const publicKey = PUBLIC_KEYS[name];
    const legacyKey = LEGACY_KEYS[name];
    const publicValues = explicitValues(publicKey);
    const legacyValues = explicitValues(legacyKey);
    if (publicValues.length > 1 || legacyValues.length > 1 ||
        (publicValues.length && legacyValues.length)) {
      errors.push({
        code: 'duplicate-explicit-key', path: publicKey,
        message: 'the public state and its retained legacy alias may not occur together or repeat'
      });
      return null;
    }
    const values = publicValues.length ? publicValues : legacyValues;
    if (values.length === 1 && !values[0]) {
      errors.push({
        code: 'invalid-explicit-value', path: publicKey,
        message: 'the explicit selection must be a stable nonempty code'
      });
      return null;
    }
    return values.length ? values[0] : null;
  }

  function safePreferences() {
    const held = Contract.safeRemembered(window.localStorage, 'propers');
    return {
      missal: held.missal,
      bible: held.bible,
      orations: held.orations
    };
  }

  function choosePreference(parsed, remembered, defaults, key, valid, errors) {
    if (Object.prototype.hasOwnProperty.call(parsed.recognized, key)) {
      const explicit = parsed.recognized[key];
      if (valid(explicit)) return explicit;
      errors.push({
        code: 'invalid-explicit-value', path: key,
        message: 'the explicit ' + key + ' is not held by the selected production data'
      });
      return null;
    }
    if (remembered[key] && valid(remembered[key])) return remembered[key];
    return defaults[key] && valid(defaults[key]) ? defaults[key] : null;
  }

  async function prepare(parsed, manifests, serial) {
    const errors = [];
    if ((parsed.duplicates || []).length) {
      parsed.duplicates.forEach(function (row) {
        errors.push({
          code: 'duplicate-explicit-key', path: row.key,
          message: 'a semantic URL key may not occur more than once'
        });
      });
    }
    const remembered = safePreferences();
    const defaults = {
      missal: manifests.properIndex.default,
      bible: Contract.defaultBibleId(runtime.bibles),
      orations: T.SOURCE_LANGUAGE
    };
    const missal = choosePreference(
      parsed, remembered, defaults, 'missal',
      function (id) { return runtime.missals.some(function (row) { return row.id === id; }); },
      errors
    );
    const bible = choosePreference(
      parsed, remembered, defaults, 'bible',
      function (id) { return runtime.bibles.some(function (row) { return row.id === id; }); },
      errors
    );
    if (errors.length || !missal || !bible) return { ok: false, errors: errors };

    let structure;
    try {
      structure = await load(structurePath(missal));
    } catch (error) {
      return { ok: false, errors: [{
        code: 'candidate-load', path: 'missal', message: String(error.message || error)
      }] };
    }
    if (serial !== runtime.serial) return { superseded: true };
    if (!structure || structure.calendar !== missal || !(structure.masses || []).length) {
      return { ok: false, errors: [{
        code: 'unsupported-edition', path: 'missal',
        message: 'the requested edition has no matching production Proper structure'
      }] };
    }
    const languages = T.orationLanguagesOf(structure);
    const orations = choosePreference(
      parsed, remembered, defaults, 'orations',
      function (lang) { return languages.some(function (row) { return row.lang === lang; }); },
      errors
    );
    const groups = groupByKind(structure.masses || []);
    const hasType = parsed.present.indexOf('type') >= 0;
    const hasMass = parsed.present.indexOf('mass') >= 0;
    const hasForm = parsed.present.indexOf('form') >= 0;
    const hasLocation = parsed.present.indexOf('location') >= 0;
    let preferredType = null;
    if (hasType) {
      preferredType = parsed.recognized.type;
      if (!groups.some(function (row) { return row.kind === preferredType; })) {
        errors.push({
          code: 'invalid-explicit-value', path: 'type',
          message: 'the explicit formulary type is not held by the selected missal'
        });
      }
    }
    if (hasMass && hasType && !errors.length) {
      const group = groups.find(function (row) { return row.kind === preferredType; });
      if (!group.masses.some(function (row) { return row.key === parsed.recognized.mass; })) {
        errors.push({
          code: 'invalid-explicit-value', path: 'mass',
          message: 'the explicit formulary is not held in the requested missal and type'
        });
      }
    }
    if (hasMass && !hasType) {
      errors.push({
        code: 'incomplete-explicit-identity', path: 'type',
        message: 'the current Propers identity requires both type and mass'
      });
    }
    if (hasForm && (!hasMass || !hasType)) {
      errors.push({
        code: 'incomplete-explicit-identity', path: 'form',
        message: 'an explicit source-appointed form requires an exact formulary type and mass'
      });
    }
    if (hasLocation && (!hasMass || !hasType)) {
      errors.push({
        code: 'incomplete-explicit-identity', path: 'location',
        message: 'an explicit semantic location requires an exact formulary type and mass'
      });
    }
    if (errors.length || !orations) return { ok: false, errors: errors, structure: structure, groups: groups };
    return {
      ok: true, parsed: parsed, remembered: remembered, defaults: defaults,
      missal: missal, bible: bible, orations: orations, structure: structure,
      groups: groups, preferredType: preferredType,
      browse: !hasMass || !hasType
    };
  }

  function validationContext(prepared, manifests) {
    const structures = {};
    structures[prepared.missal] = prepared.structure;
    return Adapters.validationContext({
      entrance: 'propers', bibles: manifests.bibles,
      properIndex: manifests.properIndex, structures: structures, ordinaries: {}
    });
  }

  function browseState(prepared, context) {
    const requestedMode = Object.prototype.hasOwnProperty.call(prepared.parsed.recognized, 'mode')
      ? prepared.parsed.recognized.mode : 'read';
    const state = {
      schema: Contract.STATE_SCHEMA,
      entrance: 'propers',
      civilDate: null,
      edition: { id: prepared.missal },
      browse: { kind: 'browse-entry' },
      bible: {
        id: prepared.bible,
        numbering: context.bibles[prepared.bible] && context.bibles[prepared.bible].numbering || null
      },
      languages: { orations: prepared.orations },
      requestedMode: requestedMode,
      coverage: [],
      unresolvedChoices: [],
      sourceHooks: []
    };
    if (Object.prototype.hasOwnProperty.call(prepared.parsed.recognized, 'location')) {
      state.semanticLocation = { eventId: prepared.parsed.recognized.location };
    }
    return { ok: Contract.validateReaderState(state).ok, state: state, legacy: {
      sources: {}, unknown: (prepared.parsed.unknown || []).slice(), inert: [], variants: {}
    }, errors: Contract.validateReaderState(state).errors };
  }

  function normalizedState(prepared, context, errors) {
    const normalized = Contract.normalizeLegacy(prepared.parsed, {
      context: context,
      remembered: prepared.remembered,
      defaults: prepared.defaults
    });
    if (!normalized.ok) return normalized;
    const cycle = explicitSemanticValue('cycle', errors);
    const alternative = explicitSemanticValue('alternative', errors);
    const witness = explicitSemanticValue('translationWitness', errors);
    if (cycle) normalized.state.cycle = cycle;
    if (alternative) normalized.state.alternative = { id: alternative };
    normalized.legacy.unknown = (normalized.legacy.unknown || []).filter(function (row) {
      return Object.keys(LEGACY_KEYS).every(function (name) {
        return row.key !== LEGACY_KEYS[name];
      });
    });
    const mass = (prepared.structure.masses || []).find(function (row) {
      return row.key === normalized.state.formulary.id;
    });
    const witnessState = formularyWitnessState(
      prepared.structure, mass, normalized.state.languages.orations
    );
    if (witness) {
      const held = witnessState.deterministic === witness ||
        witnessState.choices.some(function (row) { return row.id === witness; });
      if (!held || normalized.state.languages.orations === T.SOURCE_LANGUAGE) {
        errors.push({
          code: 'invalid-explicit-value', path: PUBLIC_KEYS.translationWitness,
          message: 'the explicit translation witness cannot faithfully supply this formulary and language'
        });
      } else {
        normalized.state.languages.translationWitness = witness;
      }
    } else if (witnessState.deterministic) {
      normalized.state.languages.translationWitness = witnessState.deterministic;
    }
    const checked = Contract.validateReaderState(normalized.state);
    errors.push.apply(errors, checked.errors);
    if (errors.length) return { ok: false, errors: errors };
    return normalized;
  }

  function semanticProjection(result) {
    if (!result) return null;
    return {
      resolved: result.resolved,
      calendarResult: result.calendarResult,
      events: (result.events || []).map(function (event) {
        const projected = {
          id: event.id, kind: event.kind,
          semanticSlot: event.semanticSlot || null,
          editionSlotLabel: event.editionSlotLabel || null,
          selected: event.selected || null,
          seat: event.seat || null,
          sourceHooks: event.sourceHooks || []
        };
        if (event.kind === 'proper-choice') {
          projected.group = event.group;
          projected.selection = event.selection;
          projected.choiceBasis = event.choiceBasis;
          projected.options = (event.options || []).map(function (option) {
            return {
              id: option.id,
              events: (option.events || []).map(function (member) {
                return {
                  id: member.id,
                  kind: member.kind,
                  semanticSlot: member.semanticSlot || null,
                  editionSlotLabel: member.editionSlotLabel || null,
                  selected: member.selected || null,
                  seat: member.seat || null,
                  sourceHooks: member.sourceHooks || []
                };
              })
            };
          });
        }
        return projected;
      }),
      coverage: result.coverage || [],
      explicitAbsences: result.explicitAbsences || [],
      unresolvedChoices: result.unresolvedChoices || []
    };
  }

  function clearSelectionState(outcome) {
    runtime.normalized = null;
    runtime.result = null;
    runtime.mass = null;
    runtime.structure = null;
    runtime.groups = [];
    runtime.preferredType = null;
    runtime.draftStructure = null;
    runtime.draftGroups = [];
    runtime.outcome = outcome;
    runtime.detailsLoaded = false;
    setSourceContext([]);
    window.propersReaderDebug.state = null;
    window.propersReaderDebug.semantic = null;
    window.propersReaderDebug.legacy = null;
    window.propersReaderDebug.outcome = outcome;
  }

  function replaceReading(node) {
    reading.replaceChildren(node);
    reading.setAttribute('aria-busy', 'false');
    readerShell.setContents([]);
  }

  function failureNode(errors, heading) {
    const section = T.el('section', 'candidate-failure');
    section.appendChild(T.el('h2', null, heading || 'This explicit selection is invalid'));
    section.appendChild(T.el('p', null,
      'The reader did not substitute another missal, type, formulary, Bible, language, cycle, alternative, or witness.'));
    const list = T.el('ul');
    (errors || []).forEach(function (error) {
      list.appendChild(T.el('li', null, (error.path ? error.path + ': ' : '') +
        (error.message || String(error))));
    });
    section.appendChild(list);
    return section;
  }

  function renderFailure(errors, heading) {
    clearSelectionState(heading ? 'failed' : 'invalid');
    resetBrowseSurface();
    detailsBody.replaceChildren(T.el('p', 'surface-note', 'Details load when this surface is opened.'));
    replaceReading(failureNode(errors, heading));
    title.textContent = 'Selection unavailable';
    typeLine.textContent = '';
    metaLine.textContent = 'Propers · explicit state rejected';
    coverageNotice.hidden = true;
    document.title = 'Selection unavailable — Propers — Triptych';
    window.propersReaderDebug.error = (errors || []).map(function (row) {
      return { code: row.code || null, path: row.path || '', message: row.message || String(row) };
    });
    refreshDetailsAfterOutcome();
  }

  function renderBrowseEntry() {
    const section = T.el('section', 'candidate-entry');
    section.appendChild(T.el('h2', null, 'Select a formulary'));
    section.appendChild(T.el('p', null,
      'Browse by missal and formulary type, then choose the particular Mass or formulary to read. No liturgical text is selected by list order.'));
    replaceReading(section);
    title.textContent = 'Choose a formulary';
    typeLine.textContent = 'Propers are read independently of a civil date';
    const state = runtime.normalized.state;
    const missal = missalRow(state.edition.id);
    const bible = bibleRow(state.bible.id);
    metaLine.textContent = [
      missal && (missal.edition || missal.label), bible && bible.label,
      T.languageName(state.languages.orations) + ' orations'
    ].filter(Boolean).join(' · ');
    const recension = recensionContext(runtime.structure, null);
    setSourceContext(recension ? [
      recension.boundaryLabel && 'Historical boundary — stands before: ' + recension.boundaryLabel,
      recension.coverage && 'Recension coverage: ' + recension.coverage
    ] : []);
    coverageNotice.textContent = recension && recension.notice || '';
    coverageNotice.hidden = !(recension && recension.notice);
    document.title = 'Choose a formulary — Propers — Triptych';
  }

  function sourceIndex(event) {
    const hook = (event.sourceHooks || []).find(function (one) { return one.kind === 'proper-structure'; });
    const match = hook && /(\d{3})$/.exec(hook.id);
    return match ? Number(match[1]) - 1 : null;
  }

  function internalHash(updates, removals) {
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

  function eventLocation(location) {
    return location && location.kind === 'event' && location.id ? location.id : null;
  }

  function canonicalAddress(normalized) {
    return Contract.canonicalRoute('propers', window.location.pathname) +
      window.location.search + Contract.serializeLegacy(normalized);
  }

  function canonicalize(normalized, location, locationOverridesURL) {
    if (locationOverridesURL) {
      if (eventLocation(location)) {
        normalized.state.semanticLocation = { eventId: eventLocation(location) };
      } else {
        delete normalized.state.semanticLocation;
      }
    }
    const current = history.state && typeof history.state === 'object' ? history.state : {};
    const state = Object.assign({}, current, { propersReaderLocation: location || null });
    history.replaceState(state, '', canonicalAddress(normalized));
  }

  function focusCommittedResult(intent, location) {
    if (intent === 'event' && eventLocation(location)) {
      const target = Array.from(reading.querySelectorAll('[data-semantic-event-id]')).find(
        function (row) { return row.dataset.semanticEventId === eventLocation(location); }
      );
      if (target) target.focus({ preventScroll: true });
      return;
    }
    if (intent === 'title') title.focus();
  }

  function navigate(updates, removals) {
    const navigation = arguments.length > 2 && arguments[2] || {};
    const currentLocation = readerShell.captureSemanticLocation();
    const currentState = history.state && typeof history.state === 'object' ? history.state : {};
    history.replaceState(
      Object.assign({}, currentState, { propersReaderLocation: currentLocation }),
      '', window.location.href
    );
    runtime.pendingLocation = Object.prototype.hasOwnProperty.call(navigation, 'location')
      ? navigation.location : currentLocation;
    runtime.pendingLocationSet = true;
    runtime.pendingFocus = navigation.focus || null;
    const canonicalUpdates = Object.assign({}, updates || {}, {
      location: eventLocation(runtime.pendingLocation)
    });
    const canonicalHash = internalHash(canonicalUpdates, removals);
    history.pushState({ propersReaderLocation: runtime.pendingLocation }, '',
      Contract.canonicalRoute('propers', window.location.pathname) +
      window.location.search + canonicalHash);
    renderCandidate();
  }

  function cycleChoice(event, proper, bible, fragments, state, options) {
    const held = options || {};
    const wrapper = T.el('section', 'cycle-choice');
    wrapper.tabIndex = -1;
    wrapper.appendChild(T.el(held.heading || 'h2', null,
      event.editionSlotLabel || proper.name || 'Proper'));
    wrapper.appendChild(T.el('p', 'cycle-choice-note',
      'Several cycles are held. They remain separate below until one is chosen.'));
    const controls = T.el('div', 'cycle-choice-controls');
    controls.setAttribute('role', 'group');
    controls.setAttribute('aria-label', 'Choose a cycle for ' + (event.editionSlotLabel || proper.name || 'this Proper'));
    event.selected.alternatives.forEach(function (alternative) {
      const button = T.el('button', null, T.cycleLabel(alternative.cycle));
      button.type = 'button';
      button.addEventListener('click', function () {
        const target = held.locationEvent || event;
        navigate((function () {
          const row = {}; row[PUBLIC_KEYS.cycle] = alternative.cycle; return row;
        }()), [LEGACY_KEYS.cycle], {
          location: { kind: 'event', id: target.id }, focus: 'event'
        });
      });
      controls.appendChild(button);
    });
    wrapper.appendChild(controls);
    event.selected.alternatives.forEach(function (alternative) {
      const rendered = T.renderProper(proper, bible, fragments, {
        numbering: runtime.structure.numbering || null,
        orations: state.languages.orations,
        translationWitness: state.languages.translationWitness || null,
        heading: 'h2', cycle: alternative.cycle
      });
      const redundant = rendered.querySelector(':scope > .proper-name');
      if (redundant) redundant.remove();
      rendered.classList.add('cycle-alternative');
      rendered.dataset.cycle = alternative.cycle;
      wrapper.appendChild(rendered);
    });
    return wrapper;
  }

  function eventHasTranslationChoice(event) {
    if (!event || !event.selected) return false;
    if (event.selected.kind !== 'cycle-alternatives') {
      return event.selected.availability === 'choice-required' &&
        (event.selected.unresolvedWitnesses || []).length > 1;
    }
    return event.selected.alternatives.some(function (row) {
      return row.material.availability === 'choice-required' &&
        (row.material.unresolvedWitnesses || []).length > 1;
    });
  }

  function renderProperMaterial(event, proper, bible, fragments, state, heading, locationEvent) {
    if (event.selected && event.selected.kind === 'cycle-alternatives') {
      return cycleChoice(event, proper, bible, fragments, state, {
        heading: heading || 'h2', locationEvent: locationEvent || event
      });
    }
    const selectedCycle = event.selected && event.selected.cycle || null;
    const translationChoice = eventHasTranslationChoice(event);
    const section = T.renderProper(proper, bible, fragments, {
      numbering: runtime.structure.numbering || null,
      orations: translationChoice ? T.SOURCE_LANGUAGE : state.languages.orations,
      translationWitness: state.languages.translationWitness || null,
      heading: heading || 'h2', cycle: selectedCycle
    });
    if (translationChoice) {
      section.appendChild(T.el('p', 'composed-note',
        'More than one translation witness is held. Choose a witness in Browse & edition; the missal’s Latin is shown meanwhile.'));
    }
    return section;
  }

  function typedUnplacedSeat(event) {
    const seat = event && event.seat;
    return event && event.kind === 'proper' && seat &&
      seat.placement === 'unseated' && /^unplaced\//.test(seat.id || '') &&
      ['before-frame', 'after-frame'].indexOf(seat.region) >= 0 &&
      typeof seat.basis === 'string' && Boolean(seat.basis.trim());
  }

  function decorateUnplacedProper(section, event) {
    if (!typedUnplacedSeat(event)) return section;
    const region = event.seat.region;
    section.classList.add('proper-unplaced', 'proper-unplaced-' + region);
    section.dataset.unplacedRegion = region;
    section.dataset.unplacedBasis = event.seat.basis;
    const position = region === 'before-frame' ? 'before' : 'after';
    const note = T.el('p', 'composed-note proper-unplaced-note',
      'Exceptional source placement: the source assigns this Proper ' + position +
      ' the ordinary Mass frame. It remains here in source order; no Ordinary seat is invented.');
    note.setAttribute('role', 'note');
    const heading = section.querySelector(':scope > .proper-name');
    if (heading) heading.after(note);
    else section.prepend(note);
    return section;
  }

  function renderEvent(event, proper, bible, fragments, state) {
    if (event.seat && event.seat.placement === 'unseated' && !typedUnplacedSeat(event)) {
      throw new Error('a source Proper has an invalid unseated disposition: ' + event.id);
    }
    const section = renderProperMaterial(event, proper, bible, fragments, state, 'h2');
    decorateUnplacedProper(section, event);
    section.dataset.semanticLocation = event.id;
    section.dataset.semanticEventId = event.id;
    section.tabIndex = -1;
    return section;
  }

  function validateProperChoiceEvent(event) {
    if (!event || event.kind !== 'proper-choice' || typeof event.group !== 'string' ||
        !event.group || typeof event.choiceBasis !== 'string' || !event.choiceBasis.trim() ||
        !event.selection || !Array.isArray(event.options) ||
        event.options.length < 2) {
      throw new Error('a Proper choice needs a stable group, selection, and at least two options');
    }
    const selected = event.selection.option;
    if ((event.selection.state === 'required' && selected !== null) ||
        (event.selection.state === 'selected' &&
          (typeof selected !== 'string' || !selected)) ||
        ['required', 'selected'].indexOf(event.selection.state) < 0) {
      throw new Error('a Proper choice has an invalid explicit selection state: ' + event.id);
    }
    const optionIds = event.options.map(function (option) { return option && option.id; });
    if (optionIds.some(function (id) { return typeof id !== 'string' || !id; }) ||
        new Set(optionIds).size !== optionIds.length ||
        (selected !== null && optionIds.indexOf(selected) < 0)) {
      throw new Error('a Proper choice has invalid or duplicate option identities: ' + event.id);
    }
    const memberIds = [];
    event.options.forEach(function (option) {
      if (!Array.isArray(option.events) || !option.events.length ||
          option.events.some(function (member) {
            if (!member || member.kind !== 'proper' || typeof member.id !== 'string' || !member.id) {
              return true;
            }
            memberIds.push(member.id);
            return false;
          })) {
        throw new Error('every Proper choice option must retain its source Proper events: ' + event.id);
      }
    });
    if (new Set(memberIds).size !== memberIds.length) {
      throw new Error('a source Proper occurs in more than one choice option: ' + event.id);
    }
    return selected;
  }

  function properChoiceLabel(event) {
    return 'Source Proper choice: ' + T.titleCase(String(event.group).replace(/[-_]+/g, ' '));
  }

  function renderProperChoiceEvent(event, mass, bible, fragments, state) {
    const selected = validateProperChoiceEvent(event);
    const wrapper = T.el('section', 'proper-choice');
    wrapper.dataset.semanticLocation = event.id;
    wrapper.dataset.semanticEventId = event.id;
    wrapper.dataset.properChoice = event.group;
    wrapper.dataset.choiceState = event.selection.state;
    wrapper.tabIndex = -1;
    if (selected) wrapper.dataset.choiceSelection = selected;
    const heading = T.el('h2', 'proper-choice-title', properChoiceLabel(event));
    heading.id = 'proper-choice-title-' + event.id.replace(/[^a-z0-9]+/gi, '-');
    wrapper.setAttribute('aria-labelledby', heading.id);
    wrapper.appendChild(heading);
    wrapper.appendChild(T.el('p', 'proper-choice-note', selected
      ? 'The selected source option is shown first. Other source options remain collapsed and are not cumulative.'
      : 'The source appoints one of these alternatives here. None is selected; the option groups below are not cumulative.'));
    wrapper.appendChild(T.el('p', 'composed-note proper-choice-basis',
      'Source basis: ' + event.choiceBasis));
    const options = T.el('div', 'proper-choice-options');
    event.options.forEach(function (option) {
      const isSelected = selected === option.id;
      const optionName = T.titleCase(String(option.id).replace(/[-_]+/g, ' '));
      const optionNode = selected && !isSelected
        ? document.createElement('details') : T.el('section', 'proper-choice-option');
      optionNode.classList.add('proper-choice-option');
      optionNode.dataset.properChoiceOption = option.id;
      optionNode.dataset.choiceStatus = isSelected ? 'selected' :
        (selected ? 'not-selected' : 'available');
      if (isSelected) optionNode.setAttribute('aria-current', 'true');
      const label = (isSelected ? 'Selected option: ' :
        (selected ? 'Other source option: ' : 'Option: ')) + optionName;
      if (optionNode.tagName === 'DETAILS') {
        optionNode.appendChild(T.el('summary', 'proper-choice-option-title', label + ' (not selected)'));
      } else {
        optionNode.appendChild(T.el('h3', 'proper-choice-option-title', label));
      }
      (option.events || []).forEach(function (member) {
        const index = sourceIndex(member);
        const proper = index === null ? null : (mass.propers || [])[index];
        if (!proper || T.isPlaceholder(proper)) {
          throw new Error('Proper choice member has no production Proper at ' + member.id);
        }
        const node = renderProperMaterial(member, proper, bible, fragments, state, 'h4', event);
        node.classList.add('proper-choice-member');
        node.dataset.properChoiceMemberEvent = member.id;
        optionNode.appendChild(node);
      });
      options.appendChild(optionNode);
    });
    wrapper.appendChild(options);
    return wrapper;
  }

  function materialCoverageMessage(result) {
    const events = (result && result.events) || [];
    if (events.some(function (event) {
      return event.kind === 'proper-choice' && event.selection &&
        event.selection.state === 'required';
    })) {
      return 'A source-appointed Proper choice is shown inline. Its alternatives remain separate, and no option was selected by order.';
    }
    if (events.some(function (event) { return event.kind === 'proper-choice'; })) {
      return 'A source-appointed Proper choice is shown inline with its explicit selection; the other alternatives are not cumulative.';
    }
    if (events.some(function (event) {
      return event.selected && event.selected.kind === 'cycle-alternatives';
    })) {
      return 'Several cycles remain valid. Each is preserved separately at its Proper until a cycle is chosen.';
    }
    if ((result.unresolvedChoices || []).length) {
      return 'A translation or authorized option remains unresolved. No witness or option was selected by order.';
    }
    const rows = result.coverage || [];
    if (rows.every(function (row) {
      return row.state === 'supported' && row.completeness === 'complete';
    })) return null;
    if (rows.some(function (row) { return row.state === 'unavailable'; })) {
      return 'Some Proper text is unavailable in the selected edition or language; available material remains identified.';
    }
    if (rows.some(function (row) { return row.state === 'unsupported'; })) {
      return 'Part of this formulary is outside the supported Read boundary.';
    }
    if (rows.some(function (row) { return row.completeness === 'partial'; })) {
      if (rows.some(function (row) {
        return (row.reasons || []).some(function (reason) {
          return reason && reason.kind === 'partial-recension';
        });
      })) {
        return 'Some Proper material has not been collated against the selected recension; available portions remain identified.';
      }
      return 'Some Proper text is not held in this repository; the available portions are shown.';
    }
    return rows.length ? 'This formulary has a material coverage limitation.' : null;
  }

  function coverageMessage(result, mass, structure) {
    const recension = recensionContext(structure, mass);
    return [recension && recension.notice, materialCoverageMessage(result)]
      .filter(Boolean).join(' ') || null;
  }

  function unresolvedFormChoice(result, mass) {
    const choice = (result.unresolvedChoices || []).find(function (row) {
      return row && typeof row.id === 'string' && row.id.indexOf('proper-form:') === 0;
    });
    if (!choice) return false;
    const section = T.el('section', 'candidate-entry proper-form-choice');
    section.appendChild(T.el('h2', null, mass.name || mass.key));
    section.appendChild(T.el('p', 'cycle-choice-note', choice.reason ||
      'Several source-appointed forms are held. Choose one explicitly.'));
    const controls = T.el('div', 'cycle-choice-controls');
    controls.setAttribute('role', 'group');
    controls.setAttribute('aria-label', 'Choose a source-appointed form');
    const labels = [];
    (choice.options || []).forEach(function (option) {
      const sourceForm = formRow(mass, option.id);
      const label = sourceForm && sourceForm.name || T.titleCase(option.id);
      labels.push(label);
      const button = T.el('button', null, label);
      button.type = 'button';
      button.addEventListener('click', function () {
        navigate({ form: option.id }, [], { location: null, focus: 'title' });
      });
      controls.appendChild(button);
    });
    section.appendChild(T.el('p', 'proper-form-summary', 'Available forms: ' + labels.join('; ') + '.'));
    section.appendChild(controls);
    replaceReading(section);
    title.textContent = mass.name || mass.key;
    typeLine.textContent = 'Source-appointed form required';
    metaLine.textContent = 'Propers · choice unresolved';
    const recension = recensionContext(runtime.structure, mass);
    setSourceContext(recension ? [
      recension.boundaryLabel && 'Historical boundary — stands before: ' + recension.boundaryLabel,
      'Recension coverage: ' + recension.coverage,
      recension.textSource && 'Proper text source: ' + recension.textSource,
      recension.departureAct && 'Act-history station: ' + recension.departureAct
    ] : []);
    coverageNotice.textContent = [
      'No form was selected by manifest order.',
      recension && recension.notice
    ].filter(Boolean).join(' ');
    coverageNotice.hidden = false;
    document.title = (mass.name || mass.key) + ' — Choose a form — Triptych';
    return true;
  }

  function renderedSemanticInventory(contents, root) {
    const contentIds = (contents || []).map(function (row) { return row.id; });
    const domIds = Array.from(root.querySelectorAll('[data-semantic-event-id]')).map(
      function (node) { return node.dataset.semanticEventId; }
    );
    if (new Set(contentIds).size !== contentIds.length ||
        new Set(domIds).size !== domIds.length) {
      throw new Error('rendered semantic event identities must be globally unique');
    }
    if (contentIds.length !== domIds.length || contentIds.some(function (id, index) {
      return id !== domIds[index];
    })) {
      throw new Error('reader Contents must exactly match rendered semantic event order');
    }
    return domIds;
  }

  async function renderResult(result, mass, bible, serial, location) {
    const held = await T.fetchFragments(bible, T.citationsOf(mass));
    if (serial !== runtime.serial) return false;
    const fragment = document.createDocumentFragment();
    const contents = [];
    const uncompiled = T.massIsUncompiled(mass) ? T.uncompiledNote(mass) : null;
    (result.events || []).forEach(function (event, eventOrdinal) {
      if (event.kind === 'proper-choice') {
        const choice = renderProperChoiceEvent(
          event, mass, bible, held.fragments, runtime.normalized.state
        );
        choice.id = 'reader-event-' + String(eventOrdinal + 1).padStart(3, '0');
        choice.dataset.readerLocusMajor = 'Source alternatives';
        choice.dataset.readerLocusUnit = properChoiceLabel(event);
        fragment.appendChild(choice);
        contents.push({
          id: event.id,
          label: properChoiceLabel(event),
          element: choice
        });
        return;
      }
      if (event.kind !== 'proper') return;
      const index = sourceIndex(event);
      const proper = index === null ? null : (mass.propers || [])[index];
      if (!proper || T.isPlaceholder(proper)) return;
      const section = renderEvent(event, proper, bible, held.fragments, runtime.normalized.state);
      section.id = 'reader-event-' + String(index + 1).padStart(3, '0');
      section.dataset.readerLocusMajor = 'Propers';
      if (typedUnplacedSeat(event)) {
        section.dataset.readerLocusMajor = 'Exceptional source-order propers';
      }
      section.dataset.readerLocusUnit = event.editionSlotLabel || proper.name || 'Proper';
      fragment.appendChild(section);
      contents.push({
        id: event.id,
        label: event.editionSlotLabel || proper.name || 'Proper',
        element: section
      });
    });
    const semanticIds = renderedSemanticInventory(contents, fragment);
    if (eventLocation(location) && semanticIds.indexOf(eventLocation(location)) < 0) {
      return { invalidLocation: true, semanticIds: semanticIds };
    }
    reading.replaceChildren(fragment);
    reading.setAttribute('aria-busy', 'false');
    readerShell.setContents(contents);

    const state = runtime.normalized.state;
    const missal = missalRow(state.edition.id);
    const group = groupRow(state.formulary.type);
    const selectedForm = formRow(mass, result.resolved && result.resolved.form);
    const witnessId = state.languages.translationWitness || null;
    const witness = translationWitnessRow(runtime.structure, witnessId);
    const recension = recensionContext(runtime.structure, mass);
    title.textContent = mass.name || mass.key;
    typeLine.textContent = group && group.label || T.titleCase(state.formulary.type);
    const cycle = Object.prototype.hasOwnProperty.call(state, 'cycle') ? T.cycleLabel(state.cycle) : null;
    metaLine.textContent = [
      missal && (missal.edition || missal.label),
      bible.label,
      T.languageName(state.languages.orations) + ' orations',
      selectedForm && 'Form: ' + (selectedForm.name || selectedForm.id),
      cycle
    ].filter(Boolean).join(' · ');
    setSourceContext([
      witnessId && 'Translation witness: ' + (witness && witness.label || witnessId),
      witness && witness.rights && 'Rights: ' + rightsLabel(witness.rights),
      recension && recension.boundaryLabel &&
        'Historical boundary — stands before: ' + recension.boundaryLabel,
      recension && recension.coverage && 'Recension coverage: ' + recension.coverage,
      recension && recension.textSource && 'Proper text source: ' + recension.textSource,
      recension && recension.departure && 'Departure: ' + rightsLabel(recension.departure) +
        (recension.departureAct ? ' · Act-history station: ' + recension.departureAct : ''),
      recension && recension.additional.length && 'Also: ' + recension.additional.map(function (row) {
        return rightsLabel(row.kind) + (row.act ? ' · Act-history station: ' + row.act : '');
      }).join(', ')
    ]);
    const notice = coverageMessage(result, mass, runtime.structure);
    if (uncompiled) {
      coverageNotice.replaceChildren(...uncompiled.childNodes);
      if (notice) coverageNotice.appendChild(document.createTextNode(' ' + notice));
      coverageNotice.hidden = false;
    } else {
      coverageNotice.textContent = notice || '';
      coverageNotice.hidden = !notice;
    }
    document.title = [
      mass.name || mass.key,
      selectedForm && (selectedForm.name || selectedForm.id),
      'Propers', 'Triptych'
    ].filter(Boolean).join(' — ');
    return { semanticIds: semanticIds };
  }

  function placeholder(select, label) {
    const option = document.createElement('option');
    option.value = '';
    option.textContent = label;
    option.selected = true;
    select.insertBefore(option, select.firstChild);
  }

  function fillMissals(value) {
    T.fillSelect(missalSelect, runtime.missals.map(function (row) {
      return { value: row.id, label: row.label, title: row.edition || row.id };
    }));
    if (value) missalSelect.value = value;
  }

  function fillBibles(value) {
    T.fillBibleSelect(bibleSelect, runtime.bibles);
    if (value) bibleSelect.value = value;
  }

  function fillTypes(groups, value) {
    T.fillSelect(typeSelect, groups.map(function (row) {
      return { value: row.kind, label: row.label };
    }));
    if (value && groups.some(function (row) { return row.kind === value; })) typeSelect.value = value;
  }

  function fillFormularies(groups, kind, value) {
    const group = groups.find(function (row) { return row.kind === kind; });
    const masses = group ? group.masses : [];
    T.fillSelect(formularySelect, masses.map(function (mass) {
      return { value: mass.key, label: mass.name || mass.key, group: massGroup(mass) };
    }));
    placeholder(formularySelect, 'Choose a formulary…');
    if (value && masses.some(function (mass) { return mass.key === value; })) formularySelect.value = value;
  }

  function translationIdentity(row) {
    return row && (row.source_id || row.source || null);
  }

  function formularyWitnessState(structure, mass, language) {
    if (language === T.SOURCE_LANGUAGE || !mass) {
      return { deterministic: null, choices: [] };
    }
    const heldRows = (mass.propers || []).filter(function (proper) {
      return proper && !T.isPlaceholder(proper);
    }).map(function (proper) {
      return (proper.translations || []).filter(function (row) {
        return row && row.lang === language && row.text;
      });
    }).filter(function (rows) { return rows.length; });
    if (!heldRows.length || heldRows.some(function (rows) {
      return rows.some(function (row) { return !translationIdentity(row); });
    })) return { deterministic: null, choices: [] };
    const heldByProper = heldRows.map(function (rows) {
      return Array.from(new Set(rows.map(translationIdentity)));
    });

    const common = heldByProper.reduce(function (intersection, ids) {
      return intersection.filter(function (id) { return ids.indexOf(id) >= 0; });
    }, heldByProper[0].slice());
    const labels = new Map((structure.translations || []).map(function (row) {
      return [translationIdentity(row), row.label || translationIdentity(row)];
    }));
    const choices = common.map(function (id) {
      return { id: id, label: labels.get(id) || id };
    });
    return {
      deterministic: choices.length === 1 ? choices[0].id : null,
      choices: choices.length > 1 ? choices : []
    };
  }

  function selectedBrowseMass(groups) {
    const group = (groups || []).find(function (row) { return row.kind === typeSelect.value; });
    return group && group.masses.find(function (mass) {
      return mass.key === formularySelect.value;
    }) || null;
  }

  function fillOrations(structure, mass, language, witness) {
    const languages = T.orationLanguagesOf(structure);
    T.fillSelect(orationsSelect, languages.map(function (row) {
      return { value: row.lang, label: T.orationLanguageLabel(row), title: row.lang };
    }));
    orationsSelect.value = languages.some(function (row) { return row.lang === language; })
      ? language : T.SOURCE_LANGUAGE;
    witnessSelect.replaceChildren();
    witnessField.hidden = true;
    if (orationsSelect.value === T.SOURCE_LANGUAGE) return;

    const witnessState = formularyWitnessState(structure, mass, orationsSelect.value);
    if (witnessState.choices.length > 1) {
      T.fillSelect(witnessSelect, witnessState.choices.map(function (row) {
        return { value: row.id, label: row.label, title: row.id };
      }));
      placeholder(witnessSelect, 'Choose a translation witness…');
      if (witness && witnessState.choices.some(function (row) { return row.id === witness; })) {
        witnessSelect.value = witness;
      }
      witnessField.hidden = false;
    }
  }

  function setBrowseEnabled(enabled) {
    [missalSelect, typeSelect, formularySelect, bibleSelect, orationsSelect, witnessSelect]
      .forEach(function (control) { control.disabled = !enabled; });
    browseForm.querySelector('.surface-apply').disabled = !enabled;
  }

  function resetBrowseSurface() {
    [missalSelect, typeSelect, formularySelect, bibleSelect, orationsSelect, witnessSelect]
      .forEach(function (select) { select.replaceChildren(); });
    witnessField.hidden = true;
    browseStatus.textContent = 'Choose an edition to begin a new, explicit formulary selection.';
    setBrowseEnabled(false);
    if (runtime.manifests) {
      fillMissals(runtime.manifests.properIndex.default);
      fillBibles(Contract.defaultBibleId(runtime.bibles));
      missalSelect.disabled = false;
      bibleSelect.disabled = false;
    }
  }

  function populateBrowseSurface() {
    const state = runtime.normalized && runtime.normalized.state;
    if (!state || !runtime.structure) {
      resetBrowseSurface();
      return;
    }
    const currentMass = state.formulary && state.formulary.id || null;
    const currentType = state.formulary && state.formulary.type || runtime.preferredType ||
      (runtime.groups[0] && runtime.groups[0].kind);
    fillMissals(state.edition.id);
    fillBibles(state.bible.id);
    fillTypes(runtime.groups, currentType);
    fillFormularies(runtime.groups, typeSelect.value, currentMass);
    const mass = currentMass && (runtime.structure.masses || []).find(function (row) {
      return row.key === currentMass;
    });
    fillOrations(runtime.structure, mass, state.languages.orations,
      state.languages.translationWitness || null);
    browseStatus.textContent = currentMass
      ? 'Changing missal or type revalidates the formulary and requires another choice when it is not held.'
      : 'A formulary must be selected. Nothing is chosen by manifest order.';
    setBrowseEnabled(true);
  }

  async function draftMissal(id) {
    const serial = ++runtime.browseSerial;
    typeSelect.replaceChildren();
    formularySelect.replaceChildren();
    orationsSelect.replaceChildren();
    witnessSelect.replaceChildren();
    witnessField.hidden = true;
    browseStatus.textContent = 'Loading this edition’s formulary list…';
    setBrowseEnabled(false);
    missalSelect.disabled = false;
    let structure;
    try {
      structure = await load(structurePath(id));
    } catch (error) {
      if (serial !== runtime.browseSerial) return;
      browseStatus.textContent = 'This edition could not be loaded. Choose another missal.';
      setBrowseEnabled(false);
      missalSelect.disabled = false;
      return;
    }
    if (serial !== runtime.browseSerial) return;
    const groups = groupByKind(structure.masses || []);
    runtime.draftStructure = structure;
    runtime.draftGroups = groups;
    fillTypes(groups, groups[0] && groups[0].kind);
    fillFormularies(groups, typeSelect.value, null);
    fillOrations(structure, null, T.SOURCE_LANGUAGE, null);
    browseStatus.textContent = 'The prior formulary was cleared. Choose one held by this missal.';
    setBrowseEnabled(true);
  }

  function definitionList(rows) {
    const list = T.el('dl', 'details-list');
    rows.forEach(function (row) {
      if (row[1] === null || row[1] === undefined || row[1] === '') return;
      list.appendChild(T.el('dt', null, row[0]));
      list.appendChild(T.el('dd', null, String(row[1])));
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

  function cycleSummary(result, state) {
    if (Object.prototype.hasOwnProperty.call(state, 'cycle')) return T.cycleLabel(state.cycle);
    const cycles = [];
    (result.events || []).forEach(function (event) {
      if (event.selected && event.selected.kind === 'cycle-alternatives') {
        event.selected.alternatives.forEach(function (row) {
          if (cycles.indexOf(row.cycle) < 0) cycles.push(row.cycle);
        });
      }
    });
    return cycles.length ? 'Choice unresolved: ' + cycles.map(T.cycleLabel).join(', ') : 'Not applicable';
  }

  function coverageSummary(result, mass, structure) {
    if (!result) return null;
    const notice = coverageMessage(result, mass, structure);
    return notice || 'Complete for the selected production state';
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
      runtime.detailsLoaded = true;
      window.propersReaderDebug.detailsBuilds += 1;
      return;
    }
    const missal = missalRow(state.edition.id);
    const bible = bibleRow(state.bible.id);
    const selectedForm = formRow(
      runtime.mass, runtime.result && runtime.result.resolved && runtime.result.resolved.form
    );
    const witnessId = state.languages.translationWitness || null;
    const witness = translationWitnessRow(runtime.structure, witnessId);
    const recension = recensionContext(runtime.structure, runtime.mass);
    const additionalDepartures = recension && recension.additional.map(function (row) {
      return rightsLabel(row.kind) +
        (row.act ? ' · Act-history station: ' + row.act : '') +
        (row.basis ? ' — ' + row.basis : '');
    }).join(' | ');
    const selection = T.el('section', 'details-section');
    selection.appendChild(T.el('h3', null, 'Selection'));
    selection.appendChild(definitionList([
      ['Missal', missal && (missal.edition || missal.label) || state.edition.id],
      ['Formulary type', state.formulary && (groupRow(state.formulary.type) || {}).label],
      ['Formulary', runtime.mass && (runtime.mass.name || runtime.mass.key)],
      ['Form', selectedForm && (selectedForm.name || selectedForm.id) ||
        (runtime.mass && (runtime.mass.forms || []).length > 1 ? 'Choice required' : null)],
      ['Bible', bible && bible.label || state.bible.id],
      ['Orations', T.languageName(state.languages.orations)],
      ['Translation witness', witnessId && (witness && witness.label || witnessId)],
      ['Translation rights', witness && rightsLabel(witness.rights)],
      ['Translation caution', witness && witness.caution],
      ['Cycle', runtime.result ? cycleSummary(runtime.result, state) : 'Not selected'],
      ['Historical boundary — stands before', recension && recension.boundaryLabel],
      ['Recension coverage', recension && recension.coverage],
      ['Proper recension basis', recension && recension.coverageBasis],
      ['Proper text source', recension && recension.textSource],
      ['Inheritance basis', recension && recension.inheritanceBasis],
      ['Departure', recension && recension.departure &&
        (rightsLabel(recension.departure) +
          (recension.departureBasis ? ' — ' + recension.departureBasis : ''))],
      ['Departure act-history station', recension && recension.departureAct],
      ['Additional departures', additionalDepartures],
      ['Coverage', runtime.result
        ? coverageSummary(runtime.result, runtime.mass, runtime.structure)
        : (recension && recension.notice || 'No formulary selected')]
    ]));
    detailsBody.appendChild(selection);
    detailsBody.appendChild(detailsLinkSection('Related reader', [
      { label: 'Open the Day reader', href: 'day.html' }
    ]));
    detailsBody.appendChild(detailsLinkSection('Elsewhere in Triptych', [
      { label: 'The Story of Salvation', href: '../scripture/' },
      { label: 'How the Missal Changed', href: '../history/' },
      { label: 'Every Document', href: '../texts/' },
      { label: 'The Source Library', href: '../sources/' },
      { label: 'The Code, Canon by Canon', href: '../law/' }
    ]));
    runtime.detailsLoaded = true;
    window.propersReaderDebug.detailsBuilds += 1;
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
      if (name === 'browse') {
        populateBrowseSurface();
        if (!runtime.normalized && runtime.manifests && missalSelect.value) {
          draftMissal(missalSelect.value);
        }
      }
    },
    onClose: function (name) {
      if (name === 'browse') {
        runtime.browseSerial += 1;
        runtime.draftStructure = null;
        runtime.draftGroups = [];
      }
    }
  });

  async function renderCandidate() {
    const serial = ++runtime.serial;
    const pendingLocation = runtime.pendingLocation;
    const pendingLocationSet = runtime.pendingLocationSet;
    const pendingFocus = runtime.pendingFocus;
    runtime.pendingLocation = null;
    runtime.pendingLocationSet = false;
    runtime.pendingFocus = null;
    runtime.browseSerial += 1;
    if (readerShell.openSurface()) readerShell.close({ restoreFocus: false });
    clearSelectionState('loading');
    window.propersReaderReady = false;
    window.propersReaderDebug.ready = false;
    window.propersReaderDebug.error = null;
    reading.setAttribute('aria-busy', 'true');
    reading.replaceChildren(T.el('p', 'placeholder', 'Loading Propers selection…'));
    readerShell.setContents([]);
    title.textContent = 'Loading Propers selection';
    typeLine.textContent = '';
    metaLine.textContent = 'Propers · selection loading';
    document.title = 'Propers — Triptych';
    coverageNotice.textContent = '';
    coverageNotice.hidden = true;
    resetBrowseSurface();
    detailsBody.replaceChildren(T.el('p', 'surface-note', 'Details load when this surface is opened.'));

    try {
      const manifests = await loadManifests();
      if (serial !== runtime.serial) return;
      const parsed = Contract.parseLegacy('propers', window.location.hash);
      const prepared = await prepare(parsed, manifests, serial);
      if (prepared.superseded || serial !== runtime.serial) return;
      if (!prepared.ok) {
        if (prepared.structure) {
          runtime.structure = prepared.structure;
          runtime.groups = prepared.groups || [];
        }
        renderFailure(prepared.errors);
        return;
      }
      runtime.structure = prepared.structure;
      runtime.groups = prepared.groups;
      runtime.preferredType = prepared.preferredType;
      const context = validationContext(prepared, manifests);
      const internalErrors = [];
      let normalized;
      if (prepared.browse) {
        ['cycle', 'alternative', 'translationWitness'].forEach(function (name) {
          if (explicitSemanticValue(name, internalErrors)) {
            internalErrors.push({
              code: 'invalid-explicit-value', path: PUBLIC_KEYS[name],
              message: 'this selection requires an explicit formulary'
            });
          }
        });
        if (internalErrors.length) {
          renderFailure(internalErrors);
          return;
        }
        normalized = browseState(prepared, context);
      } else {
        normalized = normalizedState(prepared, context, internalErrors);
      }
      if (!normalized.ok) {
        renderFailure(normalized.errors);
        return;
      }
      const location = pendingLocationSet ? pendingLocation : (normalized.state.semanticLocation && {
        kind: 'event', id: normalized.state.semanticLocation.eventId
      }) || null;
      runtime.normalized = normalized;
      window.propersReaderDebug.state = normalized.state;
      window.propersReaderDebug.legacy = normalized.legacy;
      if (normalized.state.requestedMode !== 'read') {
        if (eventLocation(location)) {
          renderFailure([{
            code: 'invalid-semantic-location', path: 'location',
            message: 'the requested mode has no rendered semantic event inventory for this location'
          }]);
          return;
        }
        canonicalize(normalized, location, pendingLocationSet);
        renderFailure([{
          code: 'unsupported-mode', path: 'mode',
          message: 'this Propers surface currently renders Read mode only'
        }]);
        return;
      }
      if (prepared.browse) {
        canonicalize(normalized, location, pendingLocationSet);
        runtime.outcome = 'browse';
        window.propersReaderDebug.outcome = 'browse';
        renderBrowseEntry();
        populateBrowseSurface();
        refreshDetailsAfterOutcome();
        if (serial !== runtime.serial) return;
        readerShell.open('browse', shellRoot.querySelector('[data-reader-action="browse"]'));
        return;
      }

      let result;
      try {
        result = Adapters.adaptPropers({
          request: normalized.state,
          structure: prepared.structure
        });
      } catch (error) {
        renderFailure([{
          code: 'unsupported-selection', path: '', message: String(error.message || error)
        }]);
        return;
      }
      if (serial !== runtime.serial) return;
      const mass = (prepared.structure.masses || []).find(function (row) {
        return row.key === result.resolved.formulary;
      });
      if (!mass) throw new Error('the validated formulary is absent from production Proper data');
      runtime.result = result;
      runtime.mass = mass;
      const hasUnresolvedForm = (result.unresolvedChoices || []).some(function (row) {
        return row && typeof row.id === 'string' && row.id.indexOf('proper-form:') === 0;
      });
      if (hasUnresolvedForm) {
        if (eventLocation(location)) {
          renderFailure([{
            code: 'invalid-semantic-location', path: 'location',
            message: 'the explicit location is absent because this form choice is unresolved'
          }]);
          return;
        }
        canonicalize(normalized, location, pendingLocationSet);
        if (!unresolvedFormChoice(result, mass)) {
          throw new Error('the unresolved form choice could not be presented');
        }
        runtime.outcome = 'unresolved';
        window.propersReaderDebug.outcome = 'unresolved';
        window.propersReaderDebug.semantic = semanticProjection(result);
        populateBrowseSurface();
        refreshDetailsAfterOutcome();
        return;
      }
      runtime.outcome = 'ready';
      window.propersReaderDebug.outcome = 'ready';
      const rendered = await renderResult(
        result, mass, bibleRow(normalized.state.bible.id), serial, location
      );
      if (!rendered || serial !== runtime.serial) return;
      window.propersReaderDebug.semantic = semanticProjection(result);
      if (rendered.invalidLocation) {
        renderFailure([{
          code: 'invalid-semantic-location', path: 'location',
          message: 'the explicit location is not present in the rendered semantic event inventory'
        }]);
        return;
      }
      if (location && !readerShell.restoreSemanticLocation(location)) {
        renderFailure([{
          code: 'semantic-location-render', path: 'location',
          message: 'the validated semantic location could not be restored in the rendered document'
        }], 'The Propers reader could not restore this semantic location');
        return;
      }
      canonicalize(normalized, location, pendingLocationSet);
      focusCommittedResult(pendingFocus, location);
      refreshDetailsAfterOutcome();
    } catch (error) {
      if (serial !== runtime.serial) return;
      renderFailure([{
        code: 'candidate-load', path: '', message: String(error.message || error)
      }], 'The Propers reader could not load this selection');
    } finally {
      if (serial === runtime.serial) {
        window.propersReaderDebug.renders += 1;
        window.propersReaderDebug.ready = true;
        window.propersReaderReady = true;
      }
    }
  }

  missalSelect.addEventListener('change', function () { draftMissal(missalSelect.value); });
  typeSelect.addEventListener('change', function () {
    const available = runtime.draftStructure && runtime.draftStructure.calendar === missalSelect.value
      ? runtime.draftGroups : runtime.groups;
    fillFormularies(available, typeSelect.value, null);
    const structure = runtime.draftStructure && runtime.draftStructure.calendar === missalSelect.value
      ? runtime.draftStructure : runtime.structure;
    if (structure) fillOrations(structure, null, orationsSelect.value, null);
    browseStatus.textContent = 'Choose a formulary of this type; none was selected automatically.';
  });
  formularySelect.addEventListener('change', function () {
    const draft = runtime.draftStructure && runtime.draftStructure.calendar === missalSelect.value;
    const structure = draft ? runtime.draftStructure : runtime.structure;
    const groups = draft ? runtime.draftGroups : runtime.groups;
    if (structure) {
      fillOrations(structure, selectedBrowseMass(groups), orationsSelect.value, null);
    }
  });
  orationsSelect.addEventListener('change', function () {
    const draft = runtime.draftStructure && runtime.draftStructure.calendar === missalSelect.value;
    const structure = draft ? runtime.draftStructure
      : (runtime.structure && runtime.structure.calendar === missalSelect.value
        ? runtime.structure : null);
    const groups = draft ? runtime.draftGroups : runtime.groups;
    if (structure) {
      fillOrations(structure, selectedBrowseMass(groups), orationsSelect.value, null);
    }
  });

  function browseKeepsCurrentFormulary() {
    const state = runtime.normalized && runtime.normalized.state;
    return Boolean(state && state.formulary &&
      state.edition.id === missalSelect.value &&
      state.formulary.type === typeSelect.value &&
      state.formulary.id === formularySelect.value);
  }

  browseForm.addEventListener('submit', function (event) {
    event.preventDefault();
    if (!formularySelect.value) {
      browseStatus.textContent = 'Choose a formulary before applying this selection.';
      formularySelect.focus();
      return;
    }
    if (!witnessField.hidden && !witnessSelect.value) {
      browseStatus.textContent = 'Choose the translation witness, or choose the missal’s original oration language.';
      witnessSelect.focus();
      return;
    }
    try {
      window.localStorage.setItem('triptych:liturgy:propers', JSON.stringify({
        missal: missalSelect.value, bible: bibleSelect.value, orations: orationsSelect.value
      }));
    } catch (_error) {
      // Storage is optional; the explicit URL remains sufficient.
    }
    const updates = {
      missal: missalSelect.value,
      type: typeSelect.value,
      mass: formularySelect.value,
      bible: bibleSelect.value,
      orations: orationsSelect.value
    };
    updates[PUBLIC_KEYS.translationWitness] = witnessField.hidden ? null : witnessSelect.value;
    const removals = [
      'location', LEGACY_KEYS.cycle, LEGACY_KEYS.alternative,
      LEGACY_KEYS.translationWitness
    ];
    if (!browseKeepsCurrentFormulary()) {
      removals.push('form', PUBLIC_KEYS.cycle, PUBLIC_KEYS.alternative);
    }
    readerShell.close({ restoreFocus: false });
    navigate(updates, removals, { location: null, focus: 'title' });
  });

  contentsList.addEventListener('click', function (event) {
    const button = event.target.closest('[data-reader-location]');
    if (!button || !contentsList.contains(button) || !runtime.normalized ||
        runtime.outcome !== 'ready') return;
    canonicalize(runtime.normalized, {
      kind: 'event', id: button.dataset.readerLocation
    }, true);
  });

  document.querySelector('[data-mode="read"]').addEventListener('click', function () {
    readerShell.close();
  });

  let historyQueued = false;
  function historyRender(event) {
    if (event && event.type === 'popstate') {
      runtime.pendingLocation = event.state && event.state.propersReaderLocation || null;
      runtime.pendingLocationSet = true;
    } else if (!historyQueued) {
      runtime.pendingLocation = null;
      runtime.pendingLocationSet = false;
    }
    if (historyQueued) return;
    historyQueued = true;
    queueMicrotask(function () {
      historyQueued = false;
      renderCandidate();
    });
  }
  window.addEventListener('popstate', historyRender);
  window.addEventListener('hashchange', historyRender);

  T.setInlineNotice(
    'No data root could be reached at "' + T.dataRoot + '", so the Propers reader has nothing to render.'
  );
  renderCandidate();
}());
