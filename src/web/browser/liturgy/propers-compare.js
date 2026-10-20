/* Date-independent, same-formulary Propers Compare orchestration. */
'use strict';

(function (root, factory) {
  const api = factory(root);
  if (typeof module === 'object' && module && module.exports) module.exports = api;
  else root.TriptychPropersCompare = api;
}(typeof globalThis !== 'undefined' ? globalThis : this, function (root) {
  const URL_KEYS = Object.freeze(['compare', 'peer-orations', 'peer-cycle', 'peer-alternative']);

  function sideRequest(state, descriptor) {
    const request = Object.assign({}, state, {
      languages: Object.assign({}, state.languages, descriptor.languages || {}),
      requestedMode: 'read',
      options: { ordinary: false, legitimate: {} },
      unresolvedChoices: [],
      sourceHooks: []
    });
    if (descriptor.cycle) request.cycle = descriptor.cycle;
    if (descriptor.alternative) request.alternative = Object.assign({}, descriptor.alternative);
    delete request.comparison;
    delete request.semanticLocation;
    return request;
  }

  function preflight(parsed) {
    const unsupported = ['translation-witness'];
    (parsed.variantKeys || []).forEach(function (key) { unsupported.push(key); });
    return unsupported.filter(function (key) {
      return parsed.present.indexOf(key) >= 0;
    }).map(function (key) {
      return { code: 'unsupported-compare-selection', path: key,
        message: 'this selection needs its own source-backed comparison dimension' };
    });
  }

  function mappedSlot(event) {
    if (event && event.semanticSlot && event.semanticSlot.state === 'mapped') return event.semanticSlot.identity.id;
    const slots = new Set();
    (event && event.kind === 'proper-choice' && event.options || []).forEach(function (option) {
      option.events.forEach(function (member) {
        const slot = member.semanticSlot;
        if (slot && slot.state === 'mapped') slots.add(slot.identity.id);
      });
    });
    return slots.size === 1 ? Array.from(slots)[0] : null;
  }

  function compareLocation(location, result) {
    if (!location || location.kind !== 'event') return location;
    const event = result && (result.events || []).find(function (one) {
      return one.id === location.id;
    });
    const slot = mappedSlot(event);
    return slot
      ? { kind: 'event', id: 'compare/proper/' + slot }
      : { kind: 'top', id: null };
  }

  function fromCompareLocation(location, result) {
    if (!location || location.kind !== 'event') return location;
    const match = /^compare\/proper\/(.+)$/.exec(location.id || '');
    if (!match) return { kind: 'top', id: null };
    const event = result && (result.events || []).find(function (one) {
      return mappedSlot(one) === match[1];
    });
    return event ? { kind: 'event', id: event.id } : { kind: 'top', id: null };
  }

  async function build(input) {
    const state = input.state;
    const comparison = state && state.comparison;
    if (!comparison || ['oration-language', 'lectionary-cycle', 'reading-alternative'].indexOf(comparison.dimension) < 0 ||
        comparison.sides.length !== 2 || state.options.ordinary) {
      throw new Error('Propers Compare needs two explicit supported peers without the Ordinary');
    }
    if (comparison.anchor.correspondingFormulary !== state.formulary.id ||
        (comparison.dimension === 'oration-language' &&
          comparison.sides[0].languages.orations !== state.languages.orations) ||
        (comparison.dimension === 'lectionary-cycle' && comparison.sides[0].cycle !== state.cycle) ||
        (comparison.dimension === 'reading-alternative' && (!state.alternative ||
          comparison.sides[0].alternative.id !== state.alternative.id)) ||
        comparison.sides[0].edition.id !== state.edition.id) {
      throw new Error('Propers Compare anchor or primary side disagrees with the selection');
    }
    const mass = (input.structure.masses || []).find(function (one) {
      return one.key === state.formulary.id;
    });
    const bible = input.bibles.find(function (one) { return one.id === state.bible.id; });
    if (!mass || !bible) throw new Error('the exact comparison Mass or Bible is not held');
    const results = comparison.sides.map(function (descriptor) {
      const request = sideRequest(state, descriptor);
      return { id: descriptor.id, result: input.Adapters.adaptPropers({
        request: request, structure: input.structure, ordinary: null
      }) };
    });
    const view = input.Comparison.compare({ comparison: comparison, sides: results });
    const loaded = await input.T.fetchFragments(bible, input.T.citationsOf(mass));
    if (!input.isCurrent()) return null;
    const sides = results.map(function (side) {
      return {
        id: side.id, label: comparison.dimension === 'reading-alternative'
          ? state.edition.id + ' · ' + input.T.titleCase(side.id) + ' reading'
          : comparison.dimension === 'lectionary-cycle'
          ? state.edition.id + ' · Cycle ' + side.id
          : input.T.languageName(side.id) + ' orations',
        structure: input.structure, mass: mass, bible: bible,
        fragments: loaded.fragments
      };
    });
    const rendered = input.View.render({ view: view, sides: sides });
    return { view: view, rendered: rendered, mass: mass, bible: bible };
  }

  function summary(view) {
    return {
      dimension: view.dimension, anchor: view.anchor,
      calendarResults: view.calendarResults,
      sides: view.sides.map(function (side) {
        return { id: side.id, resolved: side.result.resolved,
          coverage: side.result.coverage,
          unresolvedChoices: side.result.unresolvedChoices };
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

  async function present(input) {
    const built = await build({
      state: input.state, structure: input.structure,
      bibles: input.runtime.bibles, Adapters: root.LiturgyReaderStateAdapters,
      Comparison: root.LiturgyReaderComparison, View: root.LiturgyReaderCompareView,
      T: root.Triptych, isCurrent: input.isCurrent
    });
    if (!built || !input.isCurrent()) return null;
    const location = input.location;
    if (location && location.kind === 'event' &&
        built.rendered.semanticIds.indexOf(location.id) < 0) {
      return { invalidLocation: true };
    }
    input.runtime.compareView = built.view;
    input.runtime.result = built.view.sides[0].result;
    input.runtime.mass = built.mass;
    input.reading.replaceChildren(built.rendered.fragment);
    input.reading.setAttribute('aria-busy', 'false');
    input.readerShell.setContents(built.rendered.contents);
    input.title.textContent = built.mass.name || built.mass.key;
    const cycles = built.view.dimension === 'lectionary-cycle';
    const alternatives = built.view.dimension === 'reading-alternative';
    input.typeLine.textContent = alternatives ? 'Date-independent reading alternatives' :
      cycles ? 'Date-independent lectionary cycles' : 'Date-independent oration languages';
    input.metaLine.textContent = input.state.edition.id + ' · ' +
      built.view.sides.map(function (side) {
        return alternatives ? root.Triptych.titleCase(side.id) + ' reading' :
          cycles ? 'Cycle ' + side.id : root.Triptych.languageName(side.id);
      }).join(' / ') + (cycles || alternatives ? ' · Compare' : ' orations · Compare');
    const incomplete = built.view.units.some(function (unit) {
      return unit.sides.some(function (cell) { return cell.status !== 'text-held'; });
    });
    input.coverageNotice.textContent = incomplete
      ? 'Some compared slots have unavailable text or are absent; each side is identified below.' : '';
    input.coverageNotice.hidden = !incomplete;
    root.document.title = (built.mass.name || built.mass.key) + ' — Compare — Triptych';
    return { view: built.view, semantic: summary(built.view), semanticIds: built.rendered.semanticIds };
  }

  function populateDetails(input) {
    const T = root.Triptych;
    input.body.replaceChildren();
    const section = T.el('section', 'details-section');
    section.appendChild(T.el('h3', null, 'Compare selection'));
    section.appendChild(T.el('p', null,
      'One date-independent formulary and Bible are held fixed. Each side resolves its explicit language, cycle or source reading alternative. Shared functional slots do not assert identical wording or a historical change.'));
    section.appendChild(T.el('p', null,
      'Formulary: ' + input.view.anchor.correspondingFormulary +
      (input.view.dimension === 'reading-alternative' ? ' · Reading alternatives: ' :
        input.view.dimension === 'lectionary-cycle' ? ' · Cycles: ' : ' · Orations: ') +
      input.view.sides.map(function (side) { return side.id; }).join(' / ')));
    input.body.appendChild(section);
  }

  function heldCycles(structure, state) {
    const mass = (structure && structure.masses || []).find(function (row) {
      return state && state.formulary && row.key === state.formulary.id;
    });
    const values = new Set();
    (mass && mass.propers || []).forEach(function (proper) {
      if (state.form && proper.form_id && proper.form_id !== state.form) return;
      ['cycles', 'weekday_cycles'].forEach(function (family) {
        Object.keys(proper[family] || {}).forEach(function (cycle) { values.add(cycle); });
      });
    });
    return Array.from(values).sort();
  }

  function heldAlternatives(result) {
    const groups = (result && result.events || []).filter(function (event) { return event.kind === 'proper-choice'; });
    if (groups.length !== 1) return [];
    const group = groups[0];
    if (!(group.options || []).every(function (option) {
      return option.events.length === 1 && option.events.every(function (event) {
        const slot = mappedSlot(event);
        return ['reading-1', 'reading-2', 'gospel'].includes(slot);
      });
    })) return [];
    return group.options.map(function (option) {
      return { id: group.id + '/' + option.id, label: group.group + ': ' + option.id };
    });
  }

  function bindControls(input) {
    const button = root.document.querySelector('[data-mode="compare"]');
    const setup = root.document.getElementById('compare-setup');
    const select = root.document.getElementById('reader-compare-orations');
    const dimension = root.document.getElementById('reader-compare-dimension');
    const primary = root.document.getElementById('reader-compare-cycle');
    const peer = root.document.getElementById('reader-compare-peer-cycle');
    const alternative = root.document.getElementById('reader-compare-alternative');
    const peerAlternative = root.document.getElementById('reader-compare-peer-alternative');
    const note = root.document.getElementById('compare-setup-note');
    if (!button || !setup || !select || !dimension || !primary || !peer || !alternative || !peerAlternative || !note) return;
    function fields() {
      const cycles = dimension.value === 'lectionary-cycle';
      const alternatives = dimension.value === 'reading-alternative';
      select.closest('.surface-field').hidden = cycles || alternatives;
      select.required = !cycles && !alternatives;
      [alternative, peerAlternative].forEach(function (control) {
        control.closest('.surface-field').hidden = !alternatives;
        control.required = alternatives;
      });
      [primary, peer].forEach(function (control) {
        control.closest('.surface-field').hidden = !cycles;
        control.required = cycles;
      });
      note.textContent = alternatives
        ? 'Choose both source reading alternatives explicitly. This comparison appoints neither for a date.'
        : cycles
        ? 'Choose both held cycles explicitly. Bible passages keep their edition and coverage qualifications.'
        : 'The selected formulary will be resolved independently in each language.';
    }
    dimension.addEventListener('change', fields);
    button.addEventListener('click', function () {
      setup.hidden = false;
      button.setAttribute('aria-expanded', 'true');
      const state = input.runtime.normalized && input.runtime.normalized.state;
      select.replaceChildren(new Option('Choose another oration language', ''));
      if (!state || !state.formulary) {
        note.textContent = 'Choose an exact formulary before comparing.';
        return;
      }
      const languages = ['la'].concat((input.runtime.structure.coverage &&
        input.runtime.structure.coverage.languages || []).map(function (row) {
        return row.lang;
      })).filter(function (value, index, all) {
        return value && all.indexOf(value) === index && value !== state.languages.orations;
      });
      languages.forEach(function (lang) { select.appendChild(new Option(input.T.languageName(lang), lang)); });
      const cycles = heldCycles(input.runtime.structure, state);
      const cycleOption = dimension.querySelector('[value="lectionary-cycle"]');
      cycleOption.disabled = cycles.length < 2;
      [primary, peer].forEach(function (control) {
        control.replaceChildren(new Option('Choose a held cycle', ''));
        cycles.forEach(function (cycle) { control.appendChild(new Option('Cycle ' + cycle, cycle)); });
      });
      const alternatives = heldAlternatives(input.runtime.result);
      dimension.querySelector('[value="reading-alternative"]').disabled = alternatives.length < 2;
      [alternative, peerAlternative].forEach(function (control) {
        control.replaceChildren(new Option('Choose a source reading alternative', ''));
        alternatives.forEach(function (row) { control.appendChild(new Option(input.T.titleCase(row.label), row.id)); });
      });
      alternative.value = state.alternative && state.alternative.id || '';
      peerAlternative.value = state.comparison && state.comparison.dimension === 'reading-alternative'
        ? state.comparison.sides[1].alternative.id : '';
      dimension.value = state.comparison && state.comparison.dimension || 'oration-language';
      select.value = state.comparison && state.comparison.dimension === 'oration-language'
        ? state.comparison.sides[1].languages.orations : '';
      primary.value = state.cycle || '';
      peer.value = state.comparison && state.comparison.dimension === 'lectionary-cycle'
        ? state.comparison.sides[1].cycle : '';
      fields();
      dimension.focus({ preventScroll: true });
    });
    setup.addEventListener('submit', function (event) {
      event.preventDefault();
      if (!input.runtime.normalized) return;
      const cycles = dimension.value === 'lectionary-cycle';
      const alternatives = dimension.value === 'reading-alternative';
      if (alternatives && (!alternative.value || !peerAlternative.value || alternative.value === peerAlternative.value)) {
        note.textContent = 'Choose two different source reading alternatives.';
        return;
      }
      if (!alternatives && (cycles ? !primary.value || !peer.value || primary.value === peer.value : !select.value)) {
        note.textContent = cycles ? 'Choose two different held cycles.' : 'Choose another oration language.';
        return;
      }
      const captured = input.readerShell.captureSemanticLocation();
      const location = input.runtime.normalized.state.requestedMode === 'compare'
        ? captured : compareLocation(captured, input.runtime.result);
      input.readerShell.close({ restoreFocus: false, restoreScroll: false });
      setup.hidden = true;
      button.setAttribute('aria-expanded', 'false');
      input.navigate(alternatives ? { mode: 'compare', compare: 'reading-alternative',
        alternative: alternative.value, 'peer-alternative': peerAlternative.value } :
      cycles ? { mode: 'compare', compare: 'lectionary-cycle',
        cycle: primary.value, 'peer-cycle': peer.value } :
      { mode: 'compare', compare: 'oration-language', 'peer-orations': select.value },
      ['translation-witness', 'ordinary-lang'].concat(URL_KEYS.filter(function (key) {
        return key !== 'compare' && key !== (alternatives ? 'peer-alternative' : cycles ? 'peer-cycle' : 'peer-orations');
      }), input.variantKeys()), { location: location, focus: 'mode' });
    });
  }

  return Object.freeze({
    URL_KEYS: URL_KEYS, sideRequest: sideRequest, preflight: preflight, build: build, heldCycles: heldCycles, heldAlternatives: heldAlternatives,
    compareLocation: compareLocation, fromCompareLocation: fromCompareLocation,
    summary: summary, present: present, populateDetails: populateDetails,
    bindControls: bindControls
  });
}));
