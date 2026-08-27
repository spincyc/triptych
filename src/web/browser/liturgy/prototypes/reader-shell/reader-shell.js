/* Shared W2 reader-shell prototype over the existing Triptych Proper renderer. */

'use strict';

(function () {
  const T = window.Triptych;
  const Contract = window.LiturgyReaderState;
  const MODES = ['read', 'missal', 'study', 'compare'];
  const SHELLS = ['persistent', 'reveal'];
  const M1_FIXTURE_ROOT = '/tools/tests/fixtures/liturgy-reader-state/v1/';
  const DEFAULT_STATE = 'day-read';
  const INITIATED_AT = performance.now();

  const STATES = Object.freeze({
    'day-read': {
      entrance: 'day', mode: 'read', edition: 'roman-1962', mass: 'pentecost-10',
      date: '2026-08-02', bible: 'douay-rheims', orations: 'la', ordinaryLanguage: 'en',
      display: 'translation', ordinary: false,
      fixture: 'day-roman-1962-2026-08-02.json',
      meta: '1962 Roman Missal · Universal · Douay–Rheims · Latin orations'
    },
    'day-postconciliar': {
      entrance: 'day', mode: 'read', edition: 'postconciliar', mass: 'advent-1',
      date: '2026-11-29', bible: 'douay-rheims', orations: 'la', ordinaryLanguage: 'en',
      display: 'translation', ordinary: false, ordinaryOption: 'ep-i',
      fixture: 'day-postconciliar-2026-11-29.json',
      meta: 'Postconciliar Roman Missal · Universal · Douay–Rheims · Latin orations'
    },
    'day-missal': {
      entrance: 'day', mode: 'missal', edition: 'roman-1962', mass: 'pentecost-10',
      date: '2026-08-02', bible: 'douay-rheims', orations: 'la', ordinaryLanguage: 'en',
      display: 'translation', ordinary: true,
      fixture: 'day-roman-1962-2026-08-02.json', long: true,
      meta: '1962 Missal · long shell exercise · Ordinary outline is prototype-only'
    },
    'day-study': {
      entrance: 'day', mode: 'study', edition: 'roman-1962', mass: 'pentecost-10',
      date: '2026-08-02', bible: 'douay-rheims', orations: 'la', ordinaryLanguage: 'en',
      display: 'translation', ordinary: false,
      fixture: 'day-roman-1962-2026-08-02.json', initialSurface: 'study',
      meta: '1962 Missal · Study shell · production-backed M1 Day fixture'
    },
    'propers-formulary': {
      entrance: 'propers', mode: 'read', edition: 'roman-1962', mass: 'advent-1',
      date: null, bible: 'douay-rheims', orations: 'la', ordinaryLanguage: 'en',
      display: 'translation', ordinary: false,
      fixture: 'propers-roman-1962-advent-1.json',
      meta: '1962 Missal · formulary-first · calendar-independent'
    },
    'propers-browse': {
      entrance: 'propers', mode: 'read', edition: 'roman-1962', mass: 'advent-1',
      date: null, bible: 'douay-rheims', orations: 'la', ordinaryLanguage: 'en',
      display: 'translation', ordinary: false,
      fixture: 'propers-roman-1962-advent-1.json', initialSurface: 'entrance',
      meta: 'Browse shell · no search index in W2 · current valid formulary shown behind the surface'
    },
    'propers-postconciliar': {
      entrance: 'propers', mode: 'read', edition: 'postconciliar', mass: 'transfiguration-lord',
      date: null, bible: 'douay-rheims', orations: 'la', ordinaryLanguage: 'en',
      display: 'translation', ordinary: false, ordinaryOption: 'ep-i',
      fixture: 'propers-postconciliar-transfiguration-cycles.json',
      meta: 'Postconciliar Missal · formulary-first · cycle-bearing fixture'
    },
    unavailable: {
      entrance: 'day', mode: 'read', edition: 'roman-1962', mass: 'fixture-diagnostics',
      date: '2026-08-03', bible: 'douay-rheims', orations: 'la', ordinaryLanguage: 'en',
      display: 'translation', ordinary: false, partial: true,
      meta: 'Prototype-only diagnostic state · unavailable fragments remain explicit'
    },
    compare: {
      entrance: 'propers', mode: 'compare', edition: 'synthetic-edition-a', mass: null,
      date: null, fixture: 'compare-propers-synthetic-correspondence.json', synthetic: true,
      returnState: 'propers-formulary', display: 'translation', ordinary: false,
      meta: 'Synthetic non-public M1 correspondence contract · layout only · no semantic comparison engine'
    },
    'compare-day': {
      entrance: 'day', mode: 'compare', edition: 'roman-1962', mass: null,
      date: '2026-08-02', fixture: 'compare-day-2026-08-02.json', synthetic: true,
      returnState: 'day-read', display: 'translation', ordinary: false,
      meta: 'Production-backed M1 date-side contract · layout only · no semantic comparison engine'
    },
    unresolved: {
      entrance: 'day', mode: 'read', edition: 'synthetic-edition', mass: null,
      date: '2000-01-01', fixture: 'choice-synthetic-coequal.json', synthetic: true,
      returnState: 'day-read', display: 'translation', ordinary: false,
      meta: 'Synthetic non-public M1 choice contract · no option selected by order'
    },
    bilingual: {
      entrance: 'propers', mode: 'read', edition: 'roman-1962', mass: 'advent-1',
      date: null, bible: 'douay-rheims', secondaryBible: 'clementine-vulgate', orations: 'la',
      ordinaryLanguage: 'en', display: 'bilingual', ordinary: false,
      fixture: 'propers-roman-1962-advent-1.json', bilingual: true,
      meta: '1962 Missal · Douay-Rheims and Clementine Vulgate · paired by the same Proper'
    }
  });

  const shell = document.getElementById('reader-shell');
  const reading = document.getElementById('reader-document');
  const title = document.getElementById('reader-title');
  const dateLine = document.getElementById('reader-date');
  const meta = document.getElementById('reader-meta');
  const context = document.getElementById('reader-context');
  const coverage = document.getElementById('reader-coverage');
  const error = document.getElementById('prototype-error');
  const actions = document.getElementById('global-actions');
  const entranceActionLabel = document.getElementById('entrance-action-label');
  const activeModeShort = document.getElementById('active-mode-short');
  const revealButton = document.getElementById('shell-reveal');
  const contents = document.getElementById('semantic-contents');
  const entranceContent = document.getElementById('entrance-panel-content');
  const studyContent = document.getElementById('study-panel-content');
  const status = document.getElementById('reader-status');
  const surfaces = Object.freeze({
    entrance: document.getElementById('entrance-surface'),
    contents: document.getElementById('contents-surface'),
    mode: document.getElementById('mode-surface'),
    study: document.getElementById('study-surface')
  });

  const runtime = {
    stateName: null,
    config: null,
    shell: 'persistent',
    mode: 'read',
    bible: null,
    secondaryBible: null,
    structure: null,
    mass: null,
    fixture: null,
    fixtureTrusted: false,
    fixtureMismatch: [],
    currentLocation: null,
    locations: [],
    openSurface: null,
    invoker: null,
    preservedY: 0,
    preservedLocation: null,
    surfacePresentation: null,
    pendingModeFocus: false,
    renderToken: 0,
    lastScrollY: 0,
    scrollTick: false,
    studyLoaded: false,
    requestBaseline: 0
  };

  function node(tag, className, text) {
    return T.el(tag, className, text);
  }

  function own(object, key) {
    return Object.prototype.hasOwnProperty.call(object, key);
  }

  function query() {
    return new URLSearchParams(window.location.search);
  }

  function replaceQuery(update, push) {
    const params = query();
    Object.keys(update).forEach((key) => {
      const value = update[key];
      if (value === null || value === undefined || value === '') params.delete(key);
      else params.set(key, value);
    });
    const next = window.location.pathname + '?' + params.toString() + window.location.hash;
    const semanticLocation = runtime && runtime.currentLocation ? runtime.currentLocation : null;
    if (push) {
      window.history.replaceState(Object.assign({}, window.history.state || {}, {
        semanticLocation: semanticLocation
      }), '');
      window.history.pushState({ semanticLocation: semanticLocation }, '', next);
    } else {
      window.history.replaceState(Object.assign({}, window.history.state || {}, {
        semanticLocation: semanticLocation
      }), '', next);
    }
  }

  function closedConfig(params) {
    const stateName = params.get('state') || DEFAULT_STATE;
    if (!own(STATES, stateName)) {
      return { ok: false, message: 'Unsupported prototype state “' + stateName + '”. No fallback was selected.' };
    }
    const shellName = params.get('shell') || 'persistent';
    if (!SHELLS.includes(shellName)) {
      return { ok: false, message: 'Unsupported shell variant “' + shellName + '”. No fallback was selected.' };
    }
    const base = STATES[stateName];
    const askedMode = params.get('mode') || base.mode;
    if (!MODES.includes(askedMode)) {
      return { ok: false, message: 'Unsupported prototype mode “' + askedMode + '”. No fallback was selected.' };
    }
    if (base.synthetic && askedMode !== base.mode) {
      return { ok: false, message: 'This synthetic fixture may be shown only in its declared layout mode.' };
    }
    const config = Object.assign({}, base);
    const bible = params.get('bible');
    const orations = params.get('orations');
    const display = params.get('display');
    const ordinaryLanguage = params.get('ordinaryLanguage');
    const ordinaryOption = params.get('ordinaryOption');
    const locality = params.get('locality');
    const ordinary = params.get('ordinary');
    if (bible && !['douay-rheims', 'clementine-vulgate'].includes(bible)) {
      return { ok: false, message: 'Unsupported Bible selection. No fallback was selected.' };
    }
    if (orations && !['la', 'en'].includes(orations)) {
      return { ok: false, message: 'Unsupported oration language. No fallback was selected.' };
    }
    if (display && !['translation', 'original', 'bilingual'].includes(display)) {
      return { ok: false, message: 'Unsupported text display. No fallback was selected.' };
    }
    if (ordinaryLanguage && !['en', 'la'].includes(ordinaryLanguage)) {
      return { ok: false, message: 'Unsupported Ordinary language. No fallback was selected.' };
    }
    if (ordinaryOption && !['ep-i', 'ep-ii', 'ep-iii', 'ep-iv'].includes(ordinaryOption)) {
      return { ok: false, message: 'Unsupported legitimate option. No fallback was selected.' };
    }
    if (locality && locality !== 'universal') {
      return { ok: false, message: 'Unsupported locality. No locality was inferred or substituted.' };
    }
    if (ordinary && !['on', 'off'].includes(ordinary)) {
      return { ok: false, message: 'Unsupported Ordinary state. No fallback was selected.' };
    }
    if (params.has('cycle') || params.has('alternative')) {
      return { ok: false, message: 'This W2 prototype does not resolve cycle or alternative URL selections.' };
    }
    config.bible = bible || config.bible;
    config.orations = orations || config.orations;
    config.display = display || config.display;
    config.ordinaryLanguage = ordinaryLanguage || config.ordinaryLanguage;
    config.ordinaryOption = ordinaryOption || config.ordinaryOption;
    config.locality = locality || 'universal';
    if (ordinary) config.ordinary = ordinary === 'on';
    if (config.display === 'original') config.bible = 'clementine-vulgate';
    if (config.display === 'translation') config.bible = 'douay-rheims';
    if (config.display === 'bilingual') {
      config.bible = 'douay-rheims';
      config.secondaryBible = 'clementine-vulgate';
    }
    if (stateName === 'unavailable' && params.get('requestedDate')) {
      if (!/^\d{4}-\d{2}-\d{2}$/.test(params.get('requestedDate'))) {
        return { ok: false, message: 'The requested unavailable date is invalid.' };
      }
      config.date = params.get('requestedDate');
    }
    if (stateName === 'unavailable' && params.get('edition')) {
      if (!['roman-1962', 'postconciliar'].includes(params.get('edition'))) {
        return { ok: false, message: 'The unavailable state names an unsupported edition.' };
      }
      config.edition = params.get('edition');
      config.mass = config.edition === 'roman-1962' ? 'fixture-diagnostics' : null;
    }
    if (base.entrance === 'propers' && params.get('mass')) config.mass = params.get('mass');
    return { ok: true, stateName: stateName, shell: shellName, mode: askedMode, config: config };
  }

  function showFailure(message) {
    error.textContent = message;
    error.hidden = false;
    shell.hidden = true;
    document.title = 'Unsupported prototype state · Triptych';
    window.readerShellReady = true;
  }

  function titleDate(value) {
    if (!/^\d{4}-\d{2}-\d{2}$/.test(value || '')) return value || '';
    const stamp = new Date(value + 'T12:00:00Z');
    return new Intl.DateTimeFormat('en', {
      weekday: 'long', year: 'numeric', month: 'long', day: 'numeric', timeZone: 'UTC'
    }).format(stamp);
  }

  function structurePath(edition) {
    return 'structure/propers/' + edition + '.json';
  }

  function massFrom(structure, key) {
    return ((structure && structure.masses) || []).find((one) => one.key === key) || null;
  }

  function bibleFrom(bibles, id) {
    return (bibles || []).find((one) => one.id === id) || null;
  }

  async function loadFixture(name) {
    if (!name) return null;
    const response = await fetch(M1_FIXTURE_ROOT + name, { credentials: 'same-origin' });
    if (!response.ok) throw new Error('Required M1 fixture “' + name + '” could not be loaded.');
    const fixture = await response.json();
    const validation = Contract.validateFixture(fixture);
    if (!validation.ok) throw new Error('Required M1 fixture “' + name + '” failed contract validation.');
    return fixture;
  }

  function fixtureIdentity(config, fixture) {
    if (!fixture || !fixture.requested) return { trusted: false, mismatch: ['no M1 fixture is bound'] };
    const requested = fixture.requested;
    const formulary = requested.formulary || requested.selectedReadableFormulary || {};
    const mismatch = [];
    if (requested.entrance !== config.entrance) mismatch.push('entrance');
    if ((requested.edition || {}).id !== config.edition) mismatch.push('edition');
    if (config.entrance === 'day' && requested.civilDate !== config.date) mismatch.push('civil date');
    if (formulary.id !== config.mass) mismatch.push('formulary');
    if (requested.bible && requested.bible.id !== config.bible) mismatch.push('Bible edition');
    if (requested.languages && requested.languages.orations && requested.languages.orations !== config.orations) {
      mismatch.push('oration language');
    }
    return { trusted: mismatch.length === 0, mismatch: mismatch };
  }

  function selectedCoverage(fixture) {
    return fixture && fixture.expected && Array.isArray(fixture.expected.coverage)
      ? fixture.expected.coverage : [];
  }

  function selectionMeta(config) {
    if (config.synthetic) return config.meta;
    const edition = config.edition === 'roman-1962' ? '1962 Roman Missal' : 'Postconciliar Roman Missal';
    const bible = config.display === 'bilingual'
      ? 'Douay–Rheims + Clementine Vulgate'
      : config.bible === 'clementine-vulgate' ? 'Clementine Vulgate' : 'Douay–Rheims';
    const parts = [edition, 'Universal', bible,
      (config.orations === 'en' ? 'English where available' : 'Latin') + ' orations'];
    if (config.ordinary) parts.push('Ordinary enabled · ' + (config.ordinaryLanguage === 'la' ? 'Latin' : 'English'));
    if (config.edition === 'postconciliar' && config.ordinaryOption) {
      parts.push('representative ' + config.ordinaryOption.toUpperCase().replace('-', ' '));
    }
    return parts.join(' · ');
  }

  function setIdentity(config, mass, fixture) {
    const entranceWord = config.entrance === 'day' ? 'Day' : 'Propers';
    context.textContent = entranceWord + ' · ' + runtime.mode.charAt(0).toUpperCase() + runtime.mode.slice(1);
    entranceActionLabel.textContent = config.entrance === 'day' ? 'Date & edition' : 'Browse & edition';
    activeModeShort.textContent = runtime.mode.charAt(0).toUpperCase() + runtime.mode.slice(1);
    title.textContent = mass ? mass.name : (
      runtime.stateName === 'compare' ? 'Compare shell layout' :
      runtime.stateName === 'compare-day' ? 'Compare shell layout' :
      runtime.stateName === 'unresolved' ? 'A choice remains unresolved' :
      runtime.stateName === 'unavailable' ? 'Requested text unavailable' : 'Reader shell prototype'
    );
    dateLine.textContent = config.entrance === 'day' ? titleDate(config.date) : 'Calendar-independent formulary';
    meta.textContent = selectionMeta(config);
    const rows = selectedCoverage(fixture);
    const partial = config.partial || rows.some((row) => row.state !== 'supported' || row.completeness === 'partial');
    coverage.hidden = true;
    coverage.textContent = '';
    if (config.synthetic) {
      coverage.hidden = false;
      coverage.textContent = 'Prototype-only layout material: no liturgical text or historical claim is supplied by this state.';
    } else if (runtime.fixture && !runtime.fixtureTrusted) {
      coverage.hidden = false;
      coverage.textContent = 'Selection details are unavailable because the contextual record does not match the current ' +
        runtime.fixtureMismatch.join(', ') + '. The displayed text remains identified; mismatched provenance is not shown.';
    } else if (partial) {
      coverage.hidden = false;
      coverage.textContent = 'Coverage is partial or unavailable for this selection. Missing text remains identified below.';
    }
    document.title = title.textContent + ' · Reader shell prototype · Triptych';
  }

  function modeBoundary(config) {
    if (runtime.mode === 'read') return null;
    const messages = {
      missal: 'Missal shell preview: the current real Propers are retained. The prototype-only outline tests depth and reachability; W3 owns continuous Ordinary integration.',
      compare: 'Compare shell preview: W2 tests layout only. No unit is semantically matched and no historical change is inferred.'
    };
    return messages[runtime.mode] ? node('p', 'mode-boundary', messages[runtime.mode]) : null;
  }

  function ordinaryOutline() {
    const wrap = node('section', 'ordinary-outline');
    wrap.setAttribute('data-prototype-only', 'true');
    wrap.appendChild(node('h2', null, 'Continuous-rite depth marker · prototype only'));
    const list = node('ol');
    ['Beginning', 'Liturgy of the Word', 'Offertory', 'Canon', 'Communion', 'Conclusion'].forEach((label) => {
      list.appendChild(node('li', null, label));
    });
    wrap.appendChild(list);
    return wrap;
  }

  function divisionMarker(id, label) {
    const section = node('section', 'major-division');
    section.id = 'division-' + id;
    section.dataset.semanticLocation = section.id;
    section.dataset.prototypeOnly = 'true';
    const heading = node('h2', null, label + ' · prototype division');
    heading.tabIndex = -1;
    heading.dataset.semanticFocus = 'true';
    section.appendChild(heading);
    return section;
  }

  function semanticId(proper, index) {
    const label = (proper && proper.name) || 'proper';
    return 'unit-' + String(index + 1).padStart(2, '0') + '-' + label
      .toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/^-|-$/g, '');
  }

  function markSemantic(section, proper, index) {
    const id = semanticId(proper, index);
    section.id = id;
    section.dataset.semanticLocation = id;
    section.dataset.fixtureIndex = String(index);
    const heading = section.querySelector('.proper-name');
    if (heading) {
      heading.tabIndex = -1;
      heading.dataset.semanticFocus = 'true';
    }
    return section;
  }

  async function renderActual(config, token) {
    const bibleResult = await T.loadBibles();
    if (!bibleResult.ok) throw new Error(bibleResult.message);
    const structure = await T.loadJSON(structurePath(config.edition));
    const mass = massFrom(structure, config.mass);
    if (!mass) throw new Error(
      'The requested formulary “' + config.mass + '” is not held by the selected prototype data. No nearby formulary was substituted.'
    );
    const bible = bibleFrom(bibleResult.bibles, config.bible);
    if (!bible) throw new Error(
      'The requested Bible “' + config.bible + '” is not held by the selected prototype data. No other Bible was substituted.'
    );
    const citations = T.citationsOf(mass);
    const held = await T.fetchFragments(bible, citations);
    if (token !== runtime.renderToken) return;

    runtime.structure = structure;
    runtime.mass = mass;
    runtime.bible = bible;
    runtime.secondaryBible = null;
    setIdentity(config, mass, runtime.fixtureTrusted ? runtime.fixture : null);
    T.clear(reading);
    const boundary = modeBoundary(config);
    if (boundary) reading.appendChild(boundary);
    if (runtime.mode === 'missal' || config.ordinary) reading.appendChild(ordinaryOutline());

    if (config.bilingual) {
      const second = bibleFrom(bibleResult.bibles, config.secondaryBible);
      if (!second) throw new Error('The requested second Bible is unavailable; bilingual mode did not fall back.');
      const secondHeld = await T.fetchFragments(second, citations);
      if (token !== runtime.renderToken) return;
      runtime.secondaryBible = second;
      mass.propers.forEach((proper, index) => {
        const pair = node('section', 'dual-text');
        pair.dataset.semanticLocation = semanticId(proper, index);
        pair.id = pair.dataset.semanticLocation;
        pair.dataset.fixtureIndex = String(index);
        const left = node('div', 'dual-fragment');
        left.appendChild(node('p', 'dual-language', bible.label + ' · ' + bible.numbering));
        left.appendChild(T.renderProper(proper, bible, held.fragments, {
          numbering: structure.numbering, orations: config.orations, heading: 'h2'
        }));
        const right = node('div', 'dual-fragment');
        right.appendChild(node('p', 'dual-language', second.label + ' · ' + second.numbering));
        right.appendChild(T.renderProper(proper, second, secondHeld.fragments, {
          numbering: structure.numbering, orations: config.orations, heading: 'h2'
        }));
        const focus = left.querySelector('.proper-name');
        if (focus) { focus.tabIndex = -1; focus.dataset.semanticFocus = 'true'; }
        pair.append(left, right);
        reading.appendChild(pair);
      });
    } else if (T.massIsUncompiled(mass)) {
      reading.appendChild(T.uncompiledNote(mass));
    } else {
      mass.propers.forEach((proper, index) => {
        if (runtime.mode === 'missal' || config.ordinary) {
          const divisions = {
            0: ['beginning', 'Beginning'],
            2: ['word', 'Liturgy of the Word'],
            6: ['offertory-canon', 'Offertory and Canon'],
            8: ['communion-conclusion', 'Communion and conclusion']
          };
          if (divisions[index]) reading.appendChild(divisionMarker(...divisions[index]));
        }
        const section = T.renderProper(proper, bible, held.fragments, {
          numbering: structure.numbering, orations: config.orations, heading: 'h2'
        });
        reading.appendChild(markSemantic(section, proper, index));
      });
    }
    if (config.long) {
      const marker = ordinaryOutline();
      marker.querySelector('h2').textContent = 'Depth continuation · prototype-only Ordinary outline';
      reading.appendChild(marker);
    }
  }

  function fixtureNotice(text) {
    const notice = node('p', 'fixture-boundary', text);
    notice.setAttribute('role', 'note');
    return notice;
  }

  function renderUnavailable(config) {
    setIdentity(config, null, null);
    T.clear(reading);
    const wrap = node('section', 'choice-shell');
    wrap.id = 'unavailable-text';
    wrap.dataset.semanticLocation = wrap.id;
    const heading = node('h2', null, 'Text unavailable for this bounded prototype state');
    heading.tabIndex = -1;
    heading.dataset.semanticFocus = 'true';
    wrap.appendChild(heading);
    wrap.appendChild(node('p', null,
      'The requested date or edition is not represented by the prototype fixture set. The shell has preserved the explicit request and has not substituted a nearby day, formulary, locality, cycle, or alternative.'));
    wrap.appendChild(fixtureNotice(
      'Prototype-only typed coverage: unavailable · scope requested-day · reason unsupported-date.'));
    reading.appendChild(wrap);
  }

  function renderCompare(config) {
    setIdentity(config, null, runtime.fixture);
    T.clear(reading);
    const wrap = node('div', 'compare-shell');
    wrap.appendChild(fixtureNotice(
      'Synthetic non-public M1 fixture “compare-propers-synthetic-correspondence”. This tests parallel and stacked shell composition only; it supplies no liturgical text and makes no historical claim.'
    ));
    const fixture = runtime.fixture;
    const sides = fixture.requested.comparison.sides;
    ['Calendar or formulary result', 'Entrance antiphon slot', 'Reading slot', 'Oration slot'].forEach((label, index) => {
      const unit = node('section', 'compare-unit');
      unit.id = 'compare-unit-' + String(index + 1).padStart(2, '0');
      unit.dataset.semanticLocation = unit.id;
      unit.dataset.semanticIndex = String(index);
      sides.forEach((side) => {
        const column = node('div', 'compare-side');
        const heading = node('h2', null, side.edition.id);
        heading.tabIndex = -1;
        if (side === sides[0]) heading.dataset.semanticFocus = 'true';
        column.appendChild(heading);
        column.appendChild(node('p', 'compare-placeholder', label + ' · representative placeholder; semantic engine deferred.'));
        unit.appendChild(column);
      });
      wrap.appendChild(unit);
    });
    reading.appendChild(wrap);
  }

  function renderUnresolved(config) {
    setIdentity(config, null, runtime.fixture);
    T.clear(reading);
    const wrap = node('section', 'choice-shell');
    wrap.id = 'unresolved-choice';
    wrap.dataset.semanticLocation = wrap.id;
    wrap.dataset.semanticIndex = '0';
    wrap.appendChild(fixtureNotice(
      'Synthetic non-public M1 fixture “choice-synthetic-coequal”. It exists only to prove that the shell can present a required choice without selecting the first option.'
    ));
    const heading = node('h2', null, 'A reader decision is required');
    heading.tabIndex = -1;
    heading.dataset.semanticFocus = 'true';
    wrap.appendChild(heading);
    wrap.appendChild(node('p', null, 'The contract declares coequal authorized options and no selected or default option. W2 does not resolve it.'));
    const fieldset = node('fieldset');
    fieldset.appendChild(node('legend', 'surface-legend', 'Prototype-only options'));
    const choices = runtime.fixture.requested.unresolvedChoices[0].options;
    choices.forEach((choice) => {
      const label = node('label');
      const input = node('input');
      input.type = 'radio';
      input.name = 'synthetic-choice';
      input.value = choice.id;
      label.append(input, document.createTextNode(choice.id + ' · no liturgical claim'));
      fieldset.appendChild(label);
    });
    wrap.appendChild(fieldset);
    reading.appendChild(wrap);
  }

  function labelFromLocation(element) {
    const heading = element.querySelector('.proper-name, h2, h3');
    if (!heading) return 'Reading beginning';
    const copy = heading.cloneNode(true);
    copy.querySelectorAll('.proper-ref').forEach((reference) => reference.remove());
    return copy.textContent.replace(/\s+/g, ' ').trim() || 'Liturgical section';
  }

  function rebuildContents() {
    T.clear(contents);
    runtime.locations = Array.from(reading.querySelectorAll('[data-semantic-location]'));
    runtime.locations.forEach((location, index) => {
      const button = node('button', null, labelFromLocation(location));
      button.type = 'button';
      button.dataset.ordinal = String(index + 1).padStart(2, '0');
      button.dataset.location = location.dataset.semanticLocation;
      if (runtime.currentLocation === button.dataset.location || (!runtime.currentLocation && index === 0)) {
        button.setAttribute('aria-current', 'location');
      }
      button.addEventListener('click', () => selectLocation(location));
      contents.appendChild(button);
    });
    updateCurrentLocation();
  }

  function focusFor(location) {
    return location.querySelector('[data-semantic-focus]') || location;
  }

  function selectLocation(location) {
    closeSurface({ restoreScroll: false, restoreFocus: false });
    runtime.currentLocation = location.dataset.semanticLocation;
    location.scrollIntoView({ block: 'start', behavior: 'auto' });
    const focus = focusFor(location);
    if (!focus.hasAttribute('tabindex')) focus.tabIndex = -1;
    focus.focus({ preventScroll: true });
    markCurrentButton();
    announce('Moved to ' + labelFromLocation(location) + '.');
  }

  function locationAtViewport() {
    if (!runtime.locations.length) return null;
    const threshold = Math.min(window.innerHeight * 0.34, 220);
    let current = runtime.locations[0];
    runtime.locations.forEach((location) => {
      if (location.getBoundingClientRect().top <= threshold) current = location;
    });
    return current;
  }

  function markCurrentButton() {
    contents.querySelectorAll('button').forEach((button) => {
      if (button.dataset.location === runtime.currentLocation) button.setAttribute('aria-current', 'location');
      else button.removeAttribute('aria-current');
    });
  }

  function updateCurrentLocation() {
    const current = locationAtViewport();
    if (!current) return;
    const changed = runtime.currentLocation !== current.dataset.semanticLocation;
    runtime.currentLocation = current.dataset.semanticLocation;
    markCurrentButton();
    if (changed && runtime.openSurface === 'study' && runtime.surfacePresentation === 'pinned') populateStudy();
  }

  function announce(message) {
    status.textContent = '';
    window.setTimeout(() => { status.textContent = message; }, 10);
  }

  function addOption(select, value, label) {
    const option = node('option', null, label);
    option.value = value;
    select.appendChild(option);
    return option;
  }

  function field(labelText, control, wide) {
    const wrap = node('div', 'surface-field' + (wide ? ' is-wide' : ''));
    const id = 'prototype-field-' + labelText.toLowerCase().replace(/[^a-z0-9]+/g, '-');
    control.id = id;
    const label = node('label', null, labelText);
    label.htmlFor = id;
    wrap.append(label, control);
    return wrap;
  }

  function setState(name, additions) {
    closeSurface({ restoreScroll: false, restoreFocus: false });
    replaceQuery(Object.assign({
      state: name, mode: null, mass: null, requestedDate: null, edition: null
    }, additions || {}), true);
    renderFromUrl({ fromHistory: true });
  }

  function shiftDate(date, days) {
    const stamp = new Date(date + 'T12:00:00Z');
    stamp.setUTCDate(stamp.getUTCDate() + days);
    return stamp.toISOString().slice(0, 10);
  }

  function unsupportedDate(date, config) {
    replaceQuery({
      state: 'unavailable', requestedDate: date, edition: config.edition,
      bible: config.bible, orations: config.orations, display: config.display,
      ordinaryLanguage: config.ordinaryLanguage,
      ordinaryOption: config.ordinaryOption || null,
      ordinary: config.ordinary ? 'on' : 'off', mode: null, mass: null
    }, true);
    renderFromUrl({ fromHistory: true });
  }

  function openHeldDay(date, edition) {
    if (edition === 'roman-1962' && date === '2026-08-02') setState('day-read');
    else if (edition === 'postconciliar' && date === '2026-11-29') setState('day-postconciliar');
    else unsupportedDate(date, Object.assign({}, runtime.config, { edition: edition }));
  }

  function dayPanel(config) {
    const fragment = document.createDocumentFragment();
    const steps = node('div', 'date-steps');
    const previous = node('button', null, 'Previous');
    const today = node('button', null, 'Today');
    const next = node('button', null, 'Next');
    [previous, today, next].forEach((button) => { button.type = 'button'; });
    previous.addEventListener('click', () => openHeldDay(shiftDate(config.date, -1), config.edition));
    today.addEventListener('click', () => openHeldDay(new Date().toISOString().slice(0, 10), config.edition));
    next.addEventListener('click', () => openHeldDay(shiftDate(config.date, 1), config.edition));
    steps.append(previous, today, next);
    fragment.appendChild(steps);

    const fields = node('div', 'surface-fields');
    const dateInput = node('input');
    dateInput.type = 'date';
    dateInput.value = /^\d{4}-/.test(config.date || '') ? config.date : '';
    dateInput.addEventListener('change', () => openHeldDay(dateInput.value, config.edition));
    fields.appendChild(field('Direct date', dateInput));

    const edition = node('select');
    addOption(edition, 'roman-1962', '1962 Missal');
    addOption(edition, 'postconciliar', 'Postconciliar Missal');
    edition.value = config.edition;
    edition.addEventListener('change', () => openHeldDay(config.date, edition.value));
    fields.appendChild(field('Edition', edition));
    fields.appendChild(configurationFields(config));
    fragment.appendChild(fields);
    fragment.appendChild(node('p', 'surface-note',
      'Date navigation is intentionally outside a large Settings form. Dates not represented by this bounded fixture prototype fail closed instead of retaining the current formulary silently.'));
    return fragment;
  }

  function configurationFields(config) {
    const fragment = document.createDocumentFragment();
    const locality = node('select');
    addOption(locality, 'universal', 'Universal');
    locality.disabled = true;
    fragment.appendChild(field('Locality', locality));

    const bible = node('select');
    addOption(bible, 'douay-rheims', 'Douay–Rheims');
    addOption(bible, 'clementine-vulgate', 'Clementine Vulgate');
    bible.value = config.bible || 'douay-rheims';
    bible.addEventListener('change', () => {
      replaceQuery({
        bible: bible.value,
        display: bible.value === 'clementine-vulgate' ? 'original' : 'translation'
      }, true);
      renderFromUrl({ preserveLocation: true });
    });
    fragment.appendChild(field('Bible edition', bible));

    const display = node('select');
    addOption(display, 'translation', 'Translation');
    addOption(display, 'original', 'Original');
    addOption(display, 'bilingual', 'Bilingual');
    display.value = config.display || 'translation';
    display.addEventListener('change', () => {
      replaceQuery({
        display: display.value,
        bible: display.value === 'original' ? 'clementine-vulgate' : 'douay-rheims'
      }, true);
      renderFromUrl({ preserveLocation: true });
    });
    fragment.appendChild(field('Text display', display));

    const orations = node('select');
    addOption(orations, 'la', 'Latin');
    addOption(orations, 'en', 'English where held');
    orations.value = config.orations || 'la';
    orations.addEventListener('change', () => {
      replaceQuery({ orations: orations.value }, true);
      renderFromUrl({ preserveLocation: true });
    });
    fragment.appendChild(field('Oration language', orations));

    const ordinary = node('select');
    addOption(ordinary, 'off', 'Closed');
    addOption(ordinary, 'on', 'Open');
    ordinary.value = config.ordinary ? 'on' : 'off';
    ordinary.addEventListener('change', () => {
      replaceQuery({ ordinary: ordinary.value }, true);
      renderFromUrl({ preserveLocation: true });
    });
    fragment.appendChild(field('Ordinary', ordinary));

    const ordinaryLanguage = node('select');
    addOption(ordinaryLanguage, 'en', 'English');
    addOption(ordinaryLanguage, 'la', 'Latin if available');
    ordinaryLanguage.value = config.ordinaryLanguage || 'en';
    ordinaryLanguage.addEventListener('change', () => {
      replaceQuery({ ordinaryLanguage: ordinaryLanguage.value }, true);
      renderFromUrl({ preserveLocation: true });
    });
    fragment.appendChild(field('Ordinary language', ordinaryLanguage));

    if (config.edition === 'postconciliar') {
      const option = node('select');
      ['ep-i', 'ep-ii', 'ep-iii', 'ep-iv'].forEach((value, index) => addOption(option, value, ['I', 'II', 'III', 'IV'][index]));
      option.value = config.ordinaryOption || 'ep-i';
      option.addEventListener('change', () => {
        replaceQuery({ ordinaryOption: option.value }, true);
        renderFromUrl({ preserveLocation: true });
      });
      fragment.appendChild(field('Eucharistic Prayer', option));
    }
    return fragment;
  }

  function propersPanel(config) {
    const fragment = document.createDocumentFragment();
    const fields = node('div', 'surface-fields');
    const edition = node('select');
    addOption(edition, 'roman-1962', '1962 Missal');
    addOption(edition, 'postconciliar', 'Postconciliar Missal');
    edition.value = config.edition.startsWith('synthetic') ? 'roman-1962' : config.edition;
    edition.addEventListener('change', () => {
      setState(edition.value === 'postconciliar' ? 'propers-postconciliar' : 'propers-formulary');
    });
    fields.appendChild(field('Edition', edition, true));
    fields.appendChild(configurationFields(config));
    fragment.appendChild(fields);
    const browse = node('div', 'browse-list');
    browse.appendChild(node('p', 'surface-legend', 'Browse held formularies'));
    const held = runtime.structure && runtime.structure.masses ? runtime.structure.masses : [];
    held.filter((mass) => mass.key !== 'fixture-diagnostics').slice(0, 16).forEach((mass) => {
      const button = node('button', null, mass.name);
      button.type = 'button';
      button.addEventListener('click', () => {
        replaceQuery({ state: 'propers-formulary', mass: mass.key, mode: null }, true);
        renderFromUrl({ fromHistory: true });
      });
      browse.appendChild(button);
    });
    fragment.appendChild(browse);
    fragment.appendChild(node('p', 'surface-note',
      'This is bounded browse over the existing fixture structure. W2 adds no Propers search index and does not imply one exists.'));
    return fragment;
  }

  function populateEntrance() {
    T.clear(entranceContent);
    const config = runtime.config;
    document.getElementById('entrance-surface-kicker').textContent = config.entrance === 'day' ? 'Day entrance' : 'Propers entrance';
    document.getElementById('entrance-surface-title').textContent = config.entrance === 'day' ? 'Date & edition' : 'Browse & edition';
    entranceContent.appendChild(config.entrance === 'day' ? dayPanel(config) : propersPanel(config));
  }

  function fixtureEventForLocation() {
    if (!runtime.fixtureTrusted || !runtime.fixture || !runtime.fixture.expected ||
        !Array.isArray(runtime.fixture.expected.events)) return null;
    const current = runtime.locations.find((one) => one.dataset.semanticLocation === runtime.currentLocation);
    const index = current && current.dataset.fixtureIndex !== undefined
      ? Number(current.dataset.fixtureIndex) : null;
    return index === null ? null : runtime.fixture.expected.events[index] || null;
  }

  function apparatusSection(titleText, body) {
    const section = node('section');
    section.appendChild(node('h3', null, titleText));
    if (body instanceof Node) section.appendChild(body);
    else section.appendChild(node('p', null, body));
    return section;
  }

  function readableValue(value) {
    if (value === null || value === undefined || value === '') return 'Not supplied';
    if (value === 'roman-1962') return '1962 Roman';
    return String(value).replace(/:/g, ': ').replace(/[-_]+/g, ' ')
      .replace(/\s+/g, ' ').replace(/^./, (letter) => letter.toUpperCase());
  }

  function definitionList(pairs, className) {
    const list = node('dl', className || null);
    pairs.forEach((pair) => {
      const term = node('dt', null, pair[0]);
      const description = node('dd');
      if (pair[1] instanceof Node) description.appendChild(pair[1]);
      else description.textContent = pair[1];
      if (pair[2]) Object.keys(pair[2]).forEach((key) => { description.dataset[key] = pair[2][key]; });
      list.append(term, description);
    });
    return list;
  }

  function calendarOutcome(outcome) {
    if (!outcome) return 'Not applicable or not supplied by this fixture.';
    return definitionList([
      ['Calendar', readableValue(outcome.calendar), { value: outcome.calendar }],
      ['Date', titleDate(outcome.date), { value: outcome.date }],
      ['Outcome', readableValue(outcome.winner), { value: outcome.winner }],
      ['Season', readableValue(outcome.season), { value: outcome.season }],
      ['Locality', outcome.territory ? readableValue(outcome.territory) : 'Universal', { value: outcome.territory || 'universal' }],
      ['Status', outcome.settled ? 'Settled' : 'Unresolved', { value: String(outcome.settled) }]
    ], 'apparatus-fields');
  }

  function coverageList(rows) {
    if (!rows.length) return node('p', null, 'No coverage record is supplied for this state.');
    const list = node('ul', 'coverage-list');
    rows.forEach((row) => {
      const item = node('li');
      item.dataset.state = row.state;
      item.dataset.scope = row.scope;
      item.dataset.completeness = row.completeness;
      item.appendChild(node('strong', null, readableValue(row.completeness)));
      item.appendChild(document.createTextNode(' · ' + readableValue(row.state) + ' · ' + readableValue(row.scope)));
      if (row.reasons && row.reasons.length) {
        item.appendChild(document.createTextNode(' · ' + row.reasons.map(readableValue).join('; ')));
      }
      list.appendChild(item);
    });
    return list;
  }

  function populateStudy() {
    T.clear(studyContent);
    const event = fixtureEventForLocation();
    const fixture = runtime.fixtureTrusted ? runtime.fixture : null;
    const selected = event && event.selected;
    const hookList = node('ul');
    const hooks = event && event.sourceHooks ? event.sourceHooks : [];
    if (hooks.length) hooks.forEach((hook) => {
      const item = node('li');
      item.dataset.kind = hook.kind;
      item.dataset.sourceId = hook.id;
      item.append(node('strong', null, readableValue(hook.kind) + ': '), node('span', 'source-identifier', hook.id));
      hookList.appendChild(item);
    });
    else hookList.appendChild(node('li', null, 'No claim-local source hook is present in this prototype fixture.'));

    const outcome = fixture && fixture.expected ? fixture.expected.calendarResult : null;
    if (!runtime.fixtureTrusted) {
      studyContent.appendChild(apparatusSection('Apparatus boundary',
        runtime.config.partial
          ? 'Prototype-only typed coverage: unavailable · requested-day · unsupported-date. No M1 source hook is attached.'
          : 'The contextual apparatus is not applied because the current shell selection differs in ' +
            runtime.fixtureMismatch.join(', ') + '. The displayed text remains available, but no mismatched provenance is shown.'));
    }
    studyContent.appendChild(apparatusSection('Why here?',
      runtime.config.entrance === 'day' && runtime.fixtureTrusted
        ? 'The prototype uses the selected production-backed calendar state where one exists. Full calendar reasoning remains in the production Day apparatus and is not re-derived here.'
        : runtime.config.entrance === 'propers'
          ? 'This formulary was opened directly and remains calendar-independent; no civil date was invented.'
          : 'No fixture-backed “Why here?” claim is available for this requested state.'));
    studyContent.appendChild(apparatusSection('Rubrics',
      'Rubric access is represented as one part of Study. W2 does not copy or expand the current rubric record into a second apparatus.'));
    studyContent.appendChild(apparatusSection('Calendar outcome', calendarOutcome(outcome)));
    studyContent.appendChild(apparatusSection('Rank and precedence',
      'Not supplied by the selected fixture at this semantic location; the prototype leaves the field explicit instead of inventing a value.'));
    studyContent.appendChild(apparatusSection('Commemorations and displaced celebrations',
      'None is asserted by this shell prototype. A later shared Study model must carry any actual dispositions from the calendar result.'));
    studyContent.appendChild(apparatusSection('Sources and provenance', hookList));

    const availability = definitionList([
      ['Selection', selected ? readableValue(selected.kind) + ' · ' + readableValue(selected.availability) : 'No selected material in this layout fixture'],
      ['Rights', selected && selected.rights ? readableValue(selected.rights) : 'No additional rights value supplied here']
    ], 'apparatus-fields');
    const coverageValues = coverageList(selectedCoverage(fixture));
    studyContent.appendChild(apparatusSection('Rights, availability, and typed coverage', availability));
    studyContent.lastElementChild.appendChild(coverageValues);

    const history = node('p');
    history.appendChild(document.createTextNode('Historical-change links remain in '));
    const link = node('a', null, 'How the Missal Changed');
    link.href = '../../../history/';
    history.append(link, document.createTextNode('; W2 does not infer a change from layout or witness difference.'));
    studyContent.appendChild(apparatusSection('Historical change', history));
    runtime.studyLoaded = true;
  }

  function updateModes() {
    document.querySelectorAll('#mode-options [data-mode]').forEach((button) => {
      button.setAttribute('aria-checked', button.dataset.mode === runtime.mode ? 'true' : 'false');
      button.tabIndex = button.dataset.mode === runtime.mode ? 0 : -1;
    });
  }

  function surfaceButton(name) {
    return actions.querySelector('[data-surface="' + name + '"]');
  }

  function closeOtherSurface() {
    if (!runtime.openSurface) return;
    const held = surfaces[runtime.openSurface];
    if (held.open) held.close();
    held.classList.remove('is-pinned-study');
    const button = surfaceButton(runtime.openSurface);
    if (button) button.setAttribute('aria-expanded', 'false');
    runtime.openSurface = null;
    runtime.surfacePresentation = null;
  }

  function pinnedStudyAvailable() {
    return runtime.mode === 'study' && window.matchMedia('(min-width: 72rem)').matches;
  }

  function syncStudyPresentation() {
    if (runtime.openSurface !== 'study' || runtime.mode !== 'study') return;
    const expected = pinnedStudyAvailable() ? 'pinned' : 'modal';
    if (runtime.surfacePresentation === expected) return;
    const invoker = runtime.invoker || surfaceButton('study');
    const location = runtime.currentLocation;
    closeSurface({ restoreScroll: false, restoreFocus: false });
    runtime.currentLocation = location;
    openSurface('study', invoker);
  }

  function openSurface(name, invoker) {
    if (!own(surfaces, name)) return;
    if (runtime.openSurface === name && runtime.surfacePresentation === 'pinned') {
      const first = surfaces[name].querySelector('[data-close], button, input, select, a[href]');
      if (first) first.focus({ preventScroll: true });
      return;
    }
    closeOtherSurface();
    runtime.preservedY = window.scrollY;
    runtime.preservedLocation = runtime.currentLocation;
    runtime.invoker = invoker || surfaceButton(name);
    if (name === 'entrance') populateEntrance();
    if (name === 'study') populateStudy();
    if (name === 'contents') updateCurrentLocation();
    const dialog = surfaces[name];
    const pinned = name === 'study' && pinnedStudyAvailable();
    runtime.openSurface = name;
    runtime.surfacePresentation = pinned ? 'pinned' : 'modal';
    const button = surfaceButton(name);
    if (button) button.setAttribute('aria-expanded', 'true');
    dialog.classList.toggle('is-pinned-study', pinned);
    const studyTitle = document.getElementById('study-surface-title');
    if (name === 'study') studyTitle.textContent = pinned ? 'Study apparatus' : 'Details';
    if (pinned) dialog.show();
    else dialog.showModal();
    const first = dialog.querySelector('[data-close], button, input, select, a[href]');
    if (first) first.focus({ preventScroll: true });
  }

  function closeSurface(options) {
    if (!runtime.openSurface) return;
    const held = options || {};
    const name = runtime.openSurface;
    const dialog = surfaces[name];
    const invoker = runtime.invoker;
    const y = runtime.preservedY;
    const semantic = runtime.preservedLocation;
    const presentation = runtime.surfacePresentation;
    runtime.openSurface = null;
    runtime.invoker = null;
    runtime.surfacePresentation = null;
    if (dialog.open) dialog.close();
    dialog.classList.remove('is-pinned-study');
    const button = surfaceButton(name);
    if (button) button.setAttribute('aria-expanded', 'false');
    if (held.restoreScroll !== false && presentation !== 'pinned') {
      window.scrollTo({ top: y, behavior: 'auto' });
      runtime.currentLocation = semantic;
      markCurrentButton();
    }
    if (held.restoreFocus !== false && invoker) invoker.focus({ preventScroll: true });
  }

  function handleMode(mode) {
    const location = runtime.currentLocation;
    closeSurface({ restoreScroll: false, restoreFocus: false });
    runtime.pendingModeFocus = true;
    if (mode === 'compare') {
      setState(runtime.config.entrance === 'day' ? 'compare-day' : 'compare');
      return;
    }
    if (runtime.config.synthetic) {
      setState(runtime.config.returnState || (runtime.config.entrance === 'day' ? 'day-read' : 'propers-formulary'), {
        mode: mode
      });
      return;
    }
    replaceQuery({ mode: mode }, true);
    renderFromUrl({ preserveLocation: true, location: location });
  }

  function revealShell(focusFirst) {
    shell.classList.remove('shell-hidden');
    revealButton.hidden = true;
    if (focusFirst) {
      const first = actions.querySelector('button');
      if (first) first.focus({ preventScroll: true });
    }
  }

  function updateRevealOnScroll() {
    updateCurrentLocation();
    if (runtime.shell !== 'reveal' || runtime.openSurface) {
      runtime.lastScrollY = window.scrollY;
      return;
    }
    const delta = window.scrollY - runtime.lastScrollY;
    if (window.scrollY > 180 && delta > 12 && !actions.contains(document.activeElement)) {
      shell.classList.add('shell-hidden');
      revealButton.hidden = false;
    } else if (delta < -8 || window.scrollY < 120) {
      revealShell(false);
    }
    runtime.lastScrollY = window.scrollY;
  }

  function scheduleScrollUpdate() {
    if (runtime.scrollTick) return;
    runtime.scrollTick = true;
    requestAnimationFrame(() => {
      runtime.scrollTick = false;
      updateRevealOnScroll();
    });
  }

  function restoreLocation(id) {
    if (!id) return;
    const location = document.querySelector('[data-semantic-location="' + CSS.escape(id) + '"]');
    if (!location) return;
    location.scrollIntoView({ block: 'start', behavior: 'auto' });
    runtime.currentLocation = id;
    markCurrentButton();
  }

  async function renderFromUrl(options) {
    const held = options || {};
    window.readerShellReady = false;
    const parsed = closedConfig(query());
    if (!parsed.ok) {
      showFailure(parsed.message);
      return;
    }
    error.hidden = true;
    const previousLocation = held.location || (held.preserveLocation ? runtime.currentLocation : null);
    closeOtherSurface();
    runtime.stateName = parsed.stateName;
    runtime.config = parsed.config;
    runtime.shell = parsed.shell;
    runtime.mode = parsed.mode;
    runtime.studyLoaded = false;
    runtime.structure = null;
    runtime.mass = null;
    runtime.renderToken += 1;
    const token = runtime.renderToken;
    runtime.fixture = null;
    runtime.fixtureTrusted = false;
    runtime.fixtureMismatch = [];
    shell.dataset.shell = runtime.shell;
    shell.classList.remove('shell-hidden');
    revealButton.hidden = true;
    reading.setAttribute('aria-busy', 'true');
    T.clear(reading);
    reading.appendChild(node('p', 'placeholder', 'Loading real Triptych content…'));
    runtime.requestBaseline = performance.getEntriesByType('resource').length;

    try {
      runtime.fixture = await loadFixture(parsed.config.fixture);
      if (token !== runtime.renderToken) return;
      const identity = fixtureIdentity(parsed.config, runtime.fixture);
      runtime.fixtureTrusted = identity.trusted;
      runtime.fixtureMismatch = identity.mismatch;
      if (runtime.stateName.startsWith('compare')) renderCompare(parsed.config);
      else if (runtime.stateName === 'unresolved') renderUnresolved(parsed.config);
      else if (runtime.stateName === 'unavailable') renderUnavailable(parsed.config);
      else await renderActual(parsed.config, token);
      if (token !== runtime.renderToken) return;
      reading.setAttribute('aria-busy', 'false');
      rebuildContents();
      updateModes();
      shell.hidden = false;
      if (previousLocation) requestAnimationFrame(() => restoreLocation(previousLocation));
      announce(title.textContent + ' loaded in ' + runtime.mode + ' mode.');
      performance.mark('reader-shell-ready');
      window.readerShellReady = true;
      window.readerShellMetrics = collectMetrics();
      const initialSurface = runtime.mode === 'study' ? 'study' : parsed.config.initialSurface;
      if (initialSurface && !runtime.openSurface) {
        requestAnimationFrame(() => openSurface(initialSurface, surfaceButton(initialSurface)));
      } else if (runtime.pendingModeFocus) {
        const modeAction = surfaceButton('mode');
        if (modeAction) modeAction.focus({ preventScroll: true });
      }
      runtime.pendingModeFocus = false;
    } catch (caught) {
      if (token !== runtime.renderToken) return;
      reading.setAttribute('aria-busy', 'false');
      T.clear(reading);
      reading.appendChild(node('p', 'error', caught.message || String(caught)));
      setIdentity(parsed.config, null, runtime.fixture);
      shell.hidden = false;
      coverage.hidden = false;
      coverage.textContent = 'The requested prototype state failed closed. No neighboring edition, formulary, Bible, or option was substituted.';
      announce('Prototype state unavailable.');
      window.readerShellReady = true;
      window.readerShellMetrics = collectMetrics();
    }
  }

  function collectMetrics() {
    const actionBox = actions.getBoundingClientRect();
    const documentBox = reading.getBoundingClientRect();
    const firstContent = reading.querySelector('.proper, [data-semantic-location]');
    const firstBox = firstContent ? firstContent.getBoundingClientRect() : null;
    const firstPassage = reading.querySelector('.passage, .composed');
    const style = firstPassage ? getComputedStyle(firstPassage) : null;
    const fontSize = style ? parseFloat(style.fontSize) : 16;
    const approximateCharacters = firstPassage
      ? Math.round(firstPassage.getBoundingClientRect().width / (fontSize * 0.52)) : 0;
    const targets = Array.from(actions.querySelectorAll('button')).map((button) => {
      const box = button.getBoundingClientRect();
      return { label: button.innerText.replace(/\s+/g, ' ').trim(), width: box.width, height: box.height };
    });
    return {
      state: runtime.stateName,
      entrance: runtime.config && runtime.config.entrance,
      mode: runtime.mode,
      shell: runtime.shell,
      initializationMs: Math.round((performance.now() - INITIATED_AT) * 100) / 100,
      firstContentfulPaintMs: Math.round(
        ((performance.getEntriesByName('first-contentful-paint')[0] || {}).startTime || 0) * 100
      ) / 100,
      largestContentfulPaintMs: Math.round((window.readerShellLargestContentfulPaint || 0) * 100) / 100,
      shellHeight: Math.round(actionBox.height * 100) / 100,
      readingWidth: Math.round(documentBox.width * 100) / 100,
      approximateCharactersPerLine: approximateCharacters,
      firstContentTop: firstBox ? Math.round((firstBox.top + window.scrollY) * 100) / 100 : null,
      horizontalOverflow: document.documentElement.scrollWidth - document.documentElement.clientWidth,
      targets: targets,
      resourceCount: performance.getEntriesByType('resource').length,
      addedRequestsForState: performance.getEntriesByType('resource').length - runtime.requestBaseline,
      studyLoaded: runtime.studyLoaded,
      layoutShift: Math.round((window.readerShellLayoutShift || 0) * 100000) / 100000
    };
  }

  function updateViewportScrollbar() {
    const scrollbar = Math.max(0, window.innerWidth - document.documentElement.clientWidth);
    const value = scrollbar + 'px';
    if (document.documentElement.style.getPropertyValue('--viewport-scrollbar') !== value) {
      document.documentElement.style.setProperty('--viewport-scrollbar', value);
    }
  }

  actions.querySelectorAll('[data-surface]').forEach((button) => {
    button.setAttribute('aria-expanded', 'false');
    button.addEventListener('click', () => openSurface(button.dataset.surface, button));
  });
  document.querySelectorAll('[data-close]').forEach((button) => {
    button.addEventListener('click', () => closeSurface());
  });
  Object.values(surfaces).forEach((dialog) => {
    dialog.addEventListener('cancel', (event) => {
      event.preventDefault();
      closeSurface();
    });
  });
  document.querySelectorAll('#mode-options [data-mode]').forEach((button) => {
    button.addEventListener('click', () => handleMode(button.dataset.mode));
    button.addEventListener('keydown', (event) => {
      if (!['ArrowDown', 'ArrowRight', 'ArrowUp', 'ArrowLeft', 'Home', 'End'].includes(event.key)) return;
      event.preventDefault();
      const buttons = Array.from(document.querySelectorAll('#mode-options [data-mode]'));
      const current = buttons.indexOf(button);
      const next = event.key === 'Home' ? 0 : event.key === 'End' ? buttons.length - 1
        : (current + (['ArrowDown', 'ArrowRight'].includes(event.key) ? 1 : -1) + buttons.length) % buttons.length;
      handleMode(buttons[next].dataset.mode);
    });
  });
  revealButton.addEventListener('click', () => revealShell(true));
  updateViewportScrollbar();
  window.addEventListener('resize', updateViewportScrollbar);
  window.addEventListener('resize', syncStudyPresentation);
  if ('ResizeObserver' in window) new ResizeObserver(updateViewportScrollbar).observe(document.documentElement);
  document.addEventListener('focusin', (event) => {
    const location = event.target instanceof Element
      ? event.target.closest('[data-semantic-location]') : null;
    if (location && reading.contains(location)) {
      const changed = runtime.currentLocation !== location.dataset.semanticLocation;
      runtime.currentLocation = location.dataset.semanticLocation;
      markCurrentButton();
      if (changed && runtime.openSurface === 'study' &&
          runtime.surfacePresentation === 'pinned') populateStudy();
    }
    if (runtime.shell === 'reveal' && (actions.contains(document.activeElement) || revealButton === document.activeElement)) {
      revealShell(false);
    }
  });
  window.addEventListener('scroll', scheduleScrollUpdate, { passive: true });
  window.addEventListener('popstate', (event) => renderFromUrl({
    fromHistory: true,
    preserveLocation: true,
    location: event.state && event.state.semanticLocation
  }));

  window.ReaderShellPrototype = Object.freeze({
    states: Object.keys(STATES),
    open: openSurface,
    close: closeSurface,
    metrics: collectMetrics,
    current: function () {
      return {
        state: runtime.stateName,
        entrance: runtime.config && runtime.config.entrance,
        mode: runtime.mode,
        shell: runtime.shell,
        location: runtime.currentLocation,
        surface: runtime.openSurface,
        surfacePresentation: runtime.surfacePresentation,
        fixtureTrusted: runtime.fixtureTrusted,
        fixtureMismatch: runtime.fixtureMismatch.slice(),
        selections: runtime.config ? {
          edition: runtime.config.edition,
          mass: runtime.config.mass,
          bible: runtime.config.bible,
          orations: runtime.config.orations,
          locality: runtime.config.locality,
          display: runtime.config.display,
          ordinary: runtime.config.ordinary,
          ordinaryLanguage: runtime.config.ordinaryLanguage,
          ordinaryOption: runtime.config.ordinaryOption || null
        } : null
      };
    }
  });

  renderFromUrl({ fromHistory: false });
}());
