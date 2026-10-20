/* Day Compare assembly. Each side is resolved against its own calendar. */
'use strict';

(function (root) {
  const Comparison = root.LiturgyReaderComparison;
  const View = root.LiturgyReaderCompareView;

  function requireCompare() {
    if (!Comparison || !View) throw new Error('Day Compare requires its semantic and view modules');
  }

  function sideRequest(state, descriptor, territory) {
    const request = Object.assign({}, state, {
      edition: { id: descriptor.edition.id },
      calendar: { id: descriptor.calendar.id },
      requestedMode: 'read',
      options: { ordinary: false, legitimate: {} },
      unresolvedChoices: [],
      sourceHooks: []
    });
    if (territory !== 'universal') request.calendar.territory = { id: territory };
    delete request.comparison;
    delete request.selectedReadableFormulary;
    delete request.form;
    delete request.semanticLocation;
    return request;
  }

  function preflight(parsed, missals) {
    const errors = [];
    const peer = parsed.recognized['peer-missal'];
    if (!peer || !missals.some(function (row) { return row.id === peer; })) {
      errors.push({ code: 'invalid-explicit-value', path: 'peer-missal',
        message: 'Compare requires another explicitly selected held edition' });
    }
    const unsupported = ['mass', 'form', 'translation-witness', 'ordinary-lang'];
    if (parsed.recognized.ordinary === '1') unsupported.push('ordinary');
    (parsed.variantKeys || []).forEach(function (key) { unsupported.push(key); });
    unsupported.forEach(function (key) {
      if (parsed.present.indexOf(key) >= 0) errors.push({
        code: 'unsupported-compare-selection', path: key,
        message: 'this selection needs its own source-backed comparison dimension'
      });
    });
    return errors;
  }

  function hasLocation(rendered, id) {
    const ids = rendered && rendered.semanticIds;
    return Boolean(ids && (typeof ids.has === 'function' ? ids.has(id) :
      Array.isArray(ids) && ids.indexOf(id) >= 0));
  }

  function territoryCodes(primary, peer) {
    function supports(derived, code) {
      const options = derived && derived.options || [];
      if (code === 'universal') return options.some(function (row) {
        return row.option === null;
      });
      return options.length === 1 && options[0].option === null ||
        options.some(function (row) { return row.option === code; });
    }
    const codes = new Set(['universal']);
    [primary, peer].forEach(function (derived) {
      (derived && derived.options || []).forEach(function (row) {
        if (row.option !== null) codes.add(row.option);
      });
    });
    return Array.from(codes).filter(function (code) {
      return supports(primary, code) && supports(peer, code);
    }).sort(function (left, right) {
      if (left === 'universal') return -1;
      if (right === 'universal') return 1;
      return left.localeCompare(right);
    });
  }

  async function derivePeer(input) {
    const peer = input.peer;
    const year = input.date.slice(0, 4);
    const rows = await Promise.all([
      input.load('structure/rubrics/' + peer + '.json'),
      input.load('structure/calendar/' + peer + '/' + year + '.json')
    ]);
    return input.Model.derive({ date: input.date, rubrics: rows[0], year: rows[1] });
  }

  async function build(input) {
    requireCompare();
    const comparison = input.state.comparison;
    if (!comparison || comparison.dimension !== 'recension' ||
        comparison.sides.length !== 2 || comparison.anchor.territorialContext === undefined) {
      throw new Error('Day Compare needs an explicit two-edition recension and territory');
    }
    const primary = comparison.sides[0];
    const peer = comparison.sides[1];
    if (primary.edition.id !== input.state.edition.id ||
        primary.calendar.id !== input.state.calendar.id ||
        primary.edition.id === peer.edition.id) {
      throw new Error('Day Compare side identities disagree with the selected state');
    }
    const peerDerived = await derivePeer({
      peer: peer.calendar.id, date: comparison.anchor.civilDate,
      load: input.load, Model: input.Model
    });
    if (!input.isCurrent()) return null;
    const heldTerritories = territoryCodes(input.derived, peerDerived);
    if (heldTerritories.indexOf(comparison.anchor.territorialContext) < 0) {
      throw new Error('the explicit territory has no comparable calendar branch on both sides');
    }
    const results = comparison.sides.map(function (descriptor, index) {
      const request = sideRequest(
        input.state, descriptor, comparison.anchor.territorialContext
      );
      const derived = index === 0 ? input.derived : peerDerived;
      const structure = input.structures[descriptor.edition.id];
      if (!structure) throw new Error('the comparison side has no held Proper structure');
      return {
        id: descriptor.id,
        result: input.Adapters.adaptDay({ request: request, derived: derived, structure: structure }),
        structure: structure,
        derived: derived
      };
    });
    const view = Comparison.compare({ comparison: comparison, sides: results.map(function (one) {
      return { id: one.id, result: one.result };
    }) });
    const renderedSides = await Promise.all(results.map(async function (side) {
      const mass = (side.structure.masses || []).find(function (one) {
        return one.key === side.result.resolved.formulary;
      });
      if (!mass) throw new Error('the selected comparison formulary is not held');
      const bible = input.bibles.find(function (one) {
        return one.id === side.result.request.bible.id;
      });
      if (!bible) throw new Error('the selected comparison Bible is not held');
      const loaded = await input.T.fetchFragments(bible, input.T.citationsOf(mass), side.result.request, input.bibles);
      const missal = input.missals.find(function (one) {
        return one.id === side.result.resolved.edition;
      });
      return {
        id: side.id,
        label: missal && (missal.edition || missal.label) || side.id,
        structure: side.structure,
        mass: mass,
        bible: bible,
        fragments: loaded.fragments, companion: loaded.companion
      };
    }));
    if (!input.isCurrent()) return null;
    const rendered = View.render({ view: view, sides: renderedSides });
    return { view: view, rendered: rendered, derived: results.map(function (row) {
      return row.derived;
    }) };
  }

  function compareLocation(location, result) {
    if (!location || location.kind !== 'event') return location;
    const event = result && (result.events || []).find(function (one) {
      return one.id === location.id;
    });
    const slot = event && event.semanticSlot;
    return slot && slot.state === 'mapped'
      ? { kind: 'event', id: 'compare/proper/' + slot.identity.id }
      : { kind: 'top', id: null };
  }

  function fromCompareLocation(location, result) {
    if (!location || location.kind !== 'event') return location;
    const match = /^compare\/proper\/(.+)$/.exec(location.id || '');
    if (!match) return { kind: 'top', id: null };
    const event = result && (result.events || []).find(function (one) {
      return one.semanticSlot && one.semanticSlot.state === 'mapped' &&
        one.semanticSlot.identity.id === match[1];
    });
    return event ? { kind: 'event', id: event.id } : { kind: 'top', id: null };
  }

  function summary(view) {
    return {
      dimension: view.dimension,
      anchor: view.anchor,
      calendarResults: view.calendarResults,
      sides: view.sides.map(function (side) {
        return { id: side.id, resolved: side.result.resolved,
          coverage: side.result.coverage, unresolvedChoices: side.result.unresolvedChoices };
      }),
      units: view.units.map(function (unit) {
        return { semanticSlot: unit.semanticSlot, relation: unit.relation,
          sides: unit.sides.map(function (cell) {
            return { id: cell.id, status: cell.status,
              eventId: cell.event && cell.event.id || null };
          }) };
      })
    };
  }

  function commit(input) {
    const view = input.built.view;
    const state = input.state;
    input.runtime.compareView = view;
    input.runtime.result = view.sides[0].result;
    input.runtime.branch = input.built.derived[0].options.find(function (one) {
      return (one.option || 'universal') === view.anchor.territorialContext;
    }) || null;
    input.reading.replaceChildren(input.built.rendered.fragment);
    input.reading.setAttribute('aria-busy', 'false');
    input.readerShell.setContents(input.built.rendered.contents);
    input.title.textContent = 'Compare calendar results';
    input.dateLine.textContent = input.longDate(
      input.built.derived[0].date, input.built.derived[0].weekday
    );
    const editions = view.sides.map(function (side) {
      const row = input.missals.find(function (one) {
        return one.id === side.result.resolved.edition;
      });
      return row && (row.edition || row.label) || side.id;
    });
    input.commitOutcomePresentation({
      mode: 'compare', outcome: 'ready', outcomeClass: 'ready',
      metadata: editions.join(' · ') + ' · ' + view.anchor.territorialContext +
        ' · ' + input.humanLanguage(state.languages.orations) + ' orations'
    });
    const unavailable = view.units.some(function (unit) {
      return unit.sides.some(function (cell) { return cell.status === 'text-unavailable'; });
    });
    input.coverageNotice.textContent = unavailable
      ? 'Some appointed text is unavailable on a compared side; each unavailable slot is identified below.' : '';
    input.coverageNotice.hidden = !unavailable;
    document.title = 'Calendar comparison — Day — Triptych';
    input.refreshDetailsAfterOutcome();
  }

  async function present(input) {
    const runtime = input.runtime;
    const T = root.Triptych;
    const built = await build({
      state: input.state, derived: input.assembled.derived,
      structures: input.assembled.structures, load: input.load,
      Model: root.MassAssembly, Adapters: root.LiturgyReaderStateAdapters,
      T: T, bibles: runtime.bibles, missals: runtime.missals,
      isCurrent: input.isCurrent
    });
    if (!built || !input.isCurrent()) return;
    const location = input.state.semanticLocation;
    if (location && !hasLocation(built.rendered, location.eventId)) {
      input.renderFailure([{ code: 'invalid-semantic-location', path: 'location',
        message: 'the explicit Compare location is not in these paired units' }],
      { mode: 'compare' });
      return;
    }
    commit({ built: built, state: input.state, runtime: runtime,
      reading: document.getElementById('reader-document'),
      title: document.getElementById('celebration-title'),
      dateLine: document.getElementById('celebration-date'),
      coverageNotice: document.getElementById('coverage-notice'),
      readerShell: input.readerShell, missals: runtime.missals,
      longDate: input.longDate, humanLanguage: T.languageName,
      commitOutcomePresentation: input.commitOutcomePresentation,
      refreshDetailsAfterOutcome: input.refreshDetailsAfterOutcome });
    input.populateDateSurface();
    root.dayReaderDebug.semantic = summary(built.view);
    input.restorePendingNavigation(input.pendingNavigation);
    if (input.pendingPreferences) input.savePreferences(input.state);
    if (input.modeStartedAt !== null) {
      root.dayReaderDebug.lastModeSwitchMs = performance.now() - input.modeStartedAt;
    }
  }

  function populateDetails(input) {
    const body = input.body;
    const view = input.view;
    body.replaceChildren();
    const selection = input.T.el('section', 'details-section');
    selection.appendChild(input.T.el('h3', null, 'Compare selection'));
    selection.appendChild(input.T.el('p', null,
      'One civil date and an explicit territory are held fixed. Each edition resolves its own calendar. Paired units share a functional slot; this does not assert identical text or a documented historical change.'));
    const list = input.T.el('dl');
    [['Date', view.anchor.civilDate], ['Territory', view.anchor.territorialContext]].forEach(function (row) {
      list.appendChild(input.T.el('dt', null, row[0]));
      list.appendChild(input.T.el('dd', null, row[1]));
    });
    view.calendarResults.forEach(function (row) {
      list.appendChild(input.T.el('dt', null, row.id));
      list.appendChild(input.T.el('dd', null,
        'Calendar winner: ' + row.calendarResult.winner + '; selected formulary: ' +
        row.resolved.formulary));
    });
    selection.appendChild(list);
    body.appendChild(selection);
  }

  function bindControls(input) {
    const setup = document.getElementById('compare-setup');
    const button = document.querySelector('[data-mode="compare"]');
    if (!setup || !button) return; // The protected visual prototype has no Compare controls.
    const peerSelect = document.getElementById('reader-compare-peer');
    const territorySelect = document.getElementById('reader-compare-territory');
    const note = document.getElementById('compare-setup-note');
    let serial = 0;

    function fill(select, rows, placeholder) {
      select.replaceChildren(new Option(placeholder, ''));
      rows.forEach(function (row) { select.appendChild(new Option(row.label, row.id)); });
    }

    async function selectPeer(wantedTerritory) {
      const sequence = ++serial;
      fill(territorySelect, [], 'Choose a territory');
      territorySelect.disabled = true;
      if (!peerSelect.value || !input.runtime.normalized) return;
      note.textContent = 'Loading the other calendar’s held territorial branches…';
      try {
        const derived = await derivePeer({
          peer: peerSelect.value,
          date: input.runtime.normalized.state.civilDate,
          load: input.load,
          Model: input.Model
        });
        if (sequence !== serial) return;
        const codes = territoryCodes(input.runtime.derived, derived);
        fill(territorySelect, codes.map(function (id) {
          return { id: id, label: id === 'universal' ? 'Universal' :
            input.T.titleCase(id.replace(/-/g, ' ')) };
        }), 'Choose a territory');
        territorySelect.disabled = !codes.length;
        territorySelect.value = codes.indexOf(wantedTerritory) >= 0 ? wantedTerritory : '';
        note.textContent = codes.length
          ? 'Choose a territory explicitly. The calendars will be resolved independently.'
          : 'These calendars have no comparable territorial branch for this date.';
      } catch (error) {
        if (sequence !== serial) return;
        note.textContent = 'The other calendar could not be loaded: ' + error.message;
      }
    }

    button.addEventListener('click', function () {
      setup.hidden = false;
      button.setAttribute('aria-expanded', 'true');
      const state = input.runtime.normalized && input.runtime.normalized.state;
      if (!state) {
        note.textContent = 'Choose a valid Day selection before comparing editions.';
        fill(peerSelect, [], 'Choose an edition');
        fill(territorySelect, [], 'Choose a territory');
        return;
      }
      fill(peerSelect, input.runtime.missals.filter(function (row) {
        return row.id !== state.edition.id;
      }).map(function (row) {
        return { id: row.id, label: row.edition || row.label || row.id };
      }), 'Choose an edition');
      const existing = state.comparison;
      peerSelect.value = existing && existing.sides[1].edition.id || '';
      selectPeer(existing && existing.anchor.territorialContext || '');
      peerSelect.focus({ preventScroll: true });
    });
    peerSelect.addEventListener('change', function () { selectPeer(''); });
    setup.addEventListener('submit', function (event) {
      event.preventDefault();
      if (!input.runtime.normalized || !peerSelect.value || !territorySelect.value) return;
      const location = compareLocation(
        input.readerShell.captureSemanticLocation(), input.runtime.result
      );
      input.readerShell.close({ restoreFocus: false, restoreScroll: false });
      setup.hidden = true;
      button.setAttribute('aria-expanded', 'false');
      input.onModeSwitch();
      input.navigate({
        mode: 'compare', compare: 'recension',
        'peer-missal': peerSelect.value, territory: territorySelect.value
      }, ['mass', 'form', 'translation-witness', 'ordinary-lang'].concat(
        input.variantKeys(input.runtime.manifests.ordinaryIndex)
      ), { location: location, modeFocus: true });
    });
  }

  root.TriptychDayCompare = Object.freeze({
    build: build,
    derivePeer: derivePeer,
    territoryCodes: territoryCodes,
    sideRequest: sideRequest,
    preflight: preflight,
    hasLocation: hasLocation,
    compareLocation: compareLocation,
    fromCompareLocation: fromCompareLocation,
    summary: summary,
    commit: commit,
    present: present,
    populateDetails: populateDetails,
    bindControls: bindControls
  });
}(typeof globalThis !== 'undefined' ? globalThis : this));
