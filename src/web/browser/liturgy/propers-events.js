/* Production Proper event presenter and date-independent Missal composition. */
'use strict';

(function () {
  const T = window.Triptych;
  if (!T || !window.OrdinarySeating) {
    throw new Error('Propers events require the production browser and seating engine');
  }

  function create(dependencies) {
    const navigate = dependencies.navigate;
    const sourceIndex = dependencies.sourceIndex;
    const PUBLIC_KEYS = dependencies.publicKeys;
    const LEGACY_KEYS = dependencies.legacyKeys;
    const runtime = {
      get structure() { return dependencies.getStructure(); },
      get ordinary() { return dependencies.getOrdinary(); }
    };
  function renderFormChoice(result, mass) {
    const choice = (result.unresolvedChoices || []).find(function (row) {
      return row && typeof row.id === 'string' && row.id.indexOf('proper-form:') === 0;
    });
    if (!choice) return null;
    const section = T.el('section', 'candidate-entry proper-form-choice');
    section.appendChild(T.el('h2', null, mass.name || mass.key));
    section.appendChild(T.el('p', 'cycle-choice-note', choice.reason ||
      'Several source-appointed forms are held. Choose one explicitly.'));
    const controls = T.el('div', 'cycle-choice-controls');
    controls.setAttribute('role', 'group');
    controls.setAttribute('aria-label', 'Choose a source-appointed form');
    const labels = [];
    (choice.options || []).forEach(function (option) {
      const sourceForm = (mass.forms || []).find(function (row) { return row.id === option.id; });
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
    return section;
  }

  function nearestProperLocation(location, result) {
    const id = location && location.kind === 'event' && location.id;
    if (!id || /^(?:proper|proper-choice)\//.test(id)) return location;
    const events = result && result.events || [];
    const at = events.findIndex(function (row) { return row.id === id; });
    if (at < 0) return { kind: 'top', id: null };
    let best = null;
    events.forEach(function (row, index) {
      if (row.kind !== 'proper' && row.kind !== 'proper-choice') return;
      const distance = Math.abs(index - at);
      if (!best || distance < best.distance ||
          (distance === best.distance && index < best.index)) {
        best = { id: row.id, distance: distance, index: index };
      }
    });
    return best ? { kind: 'event', id: best.id } : { kind: 'top', id: null };
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
        orations: state.languages.orations, textDisplay: state.textDisplay,
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
      orations: translationChoice && state.textDisplay !== 'latin-and-selected'
        ? T.SOURCE_LANGUAGE : state.languages.orations,
      textDisplay: state.textDisplay,
      translationWitness: state.languages.translationWitness || null,
      heading: heading || 'h2', cycle: selectedCycle,
      orationGroups: event.orationGroups || null, orationContext: event.orationContext || null, eventId: event.id, structure: runtime.structure
    });
    if (translationChoice) {
      section.appendChild(T.el('p', 'composed-note',
        'More than one translation witness is held. Choose a witness in Browse & edition; missing portions will remain explicit.'));
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
    wrapper.tabIndex = -1;
    return window.TriptychReaderShell.renderProperChoice({
      T: T, event: event, selected: selected, wrapper: wrapper,
      titleId: 'proper-choice-title-' + event.id.replace(/[^a-z0-9]+/gi, '-'),
      heading: 'h2', optionHeading: 'h3', label: properChoiceLabel(event),
      state: state, navigate: navigate,
      location: { kind: 'event', id: event.id }, focus: 'event',
      adapt: function (request) {
        return window.LiturgyReaderStateAdapters.adaptPropers({ request: request,
          structure: runtime.structure, ordinary: runtime.ordinary });
      },
      renderMember: function (member) {
        const index = sourceIndex(member);
        const proper = index === null ? null : (mass.propers || [])[index];
        if (!proper || T.isPlaceholder(proper)) {
          throw new Error('Proper choice member has no production Proper at ' + member.id);
        }
        return renderProperMaterial(member, proper, bible, fragments, state, 'h4', event);
      }
    });
  }

  function semanticNode(node, event, ordinal) {
    node.dataset.semanticLocation = event.id;
    node.dataset.semanticEventId = event.id;
    node.id = 'reader-event-' + String(ordinal + 1).padStart(3, '0');
    node.tabIndex = -1;
    return node;
  }

  function ordinaryChoice(group, selected) {
    const fieldset = T.el('fieldset', 'ordinary-choice');
    fieldset.dataset.optionGroup = group.group;
    fieldset.appendChild(T.el('legend', null, group.name));
    fieldset.appendChild(T.el('p', 'ordinary-choice-note',
      'This source-defined choice belongs here in the liturgical sequence.'));
    const options = T.el('div', 'ordinary-choice-options');
    (group.options || []).forEach(function (option) {
      const label = T.el('label', 'ordinary-choice-option');
      const radio = document.createElement('input');
      radio.type = 'radio';
      radio.name = 'reader-' + group.group;
      radio.value = option.id;
      radio.checked = selected === option.id;
      radio.addEventListener('change', function () {
        if (!radio.checked) return;
        navigate({ mode: 'missal', [group.group]: option.id }, [], {
          location: null, focus: { kind: 'ordinary-option', group: group.group, option: option.id }
        });
      });
      label.appendChild(radio);
      label.appendChild(document.createTextNode(option.name));
      options.appendChild(label);
    });
    fieldset.appendChild(options);
    return fieldset;
  }

  function renderMissalEvents(fragment, contents, result, mass, bible, fragments, state) {
    const OrdinaryRenderer = window.TriptychOrdinaryRenderer;
    if (!OrdinaryRenderer) throw new Error('Missal needs its production Ordinary renderer');
    const ordinary = runtime.ordinary;
    if (!ordinary || ordinary.calendar !== state.edition.id) {
      throw new Error('the selected edition has no matching production Ordinary to render');
    }
    OrdinaryRenderer.configure({
      ordinaryLang: state.languages.ordinary, textDisplay: state.textDisplay || 'selected',
      variants: state.options.legitimate || {}, why: false
    });
    const sections = new Map();
    const elements = new Map();
    (ordinary.sections || []).forEach(function (section) {
      sections.set(section.key, section);
      (section.elements || []).forEach(function (element) { elements.set(element.key, element); });
    });
    const ordinals = new Map((result.events || []).map(function (event, index) {
      return [event.id, index];
    }));
    const frameEvents = (result.events || []).map(function (event) {
      return event.kind === 'proper-choice'
        ? Object.assign({}, event, { kind: 'proper', properChoiceEvent: event }) : event;
    });
    let division = ordinary.title || 'Order of Mass';
    const frame = OrdinaryRenderer.renderSemanticFrame(frameEvents, {
      section: function (event) {
        const raw = sections.get(event.id.replace(/^ordinary-section\//, ''));
        if (!raw) throw new Error('production Ordinary section is missing for ' + event.id);
        division = raw.name;
        const node = semanticNode(T.el('h2', 'mass-subheading ordinary-division', raw.name),
          event, ordinals.get(event.id));
        node.dataset.readerLocusMajor = raw.name;
        contents.push({ id: event.id, label: raw.name, element: node, group: 'Rites and divisions' });
        return node;
      },
      element: function (event) {
        const raw = elements.get(event.id.replace(/^ordinary-element\//, ''));
        if (!raw) throw new Error('production Ordinary element is missing for ' + event.id);
        const node = semanticNode(OrdinaryRenderer.renderElement(raw, ordinary),
          event, ordinals.get(event.id));
        node.dataset.readerLocusMajor = division;
        node.dataset.readerLocusUnit = raw.name || raw.locus || 'Ordinary';
        contents.push({ id: event.id, label: raw.name || raw.locus || 'Ordinary',
          element: node, group: division });
        return node;
      },
      proper: function (event) {
        const source = event.properChoiceEvent || event;
        if (source.kind === 'proper-choice') {
          if (!source.seat || source.seat.placement !== 'seated') {
            throw new Error('a Proper choice has no usable semantic Ordinary seat: ' + source.id);
          }
          const choice = semanticNode(renderProperChoiceEvent(
            source, mass, bible, fragments, state
          ), source, ordinals.get(source.id));
          choice.dataset.readerLocusMajor = division;
          choice.dataset.readerLocusUnit = properChoiceLabel(source);
          contents.push({ id: source.id, label: properChoiceLabel(source),
            element: choice, group: 'Proper choices' });
          return choice;
        }
        const index = sourceIndex(source);
        const proper = index === null ? null : (mass.propers || [])[index];
        if (!proper || T.isPlaceholder(proper)) {
          throw new Error('semantic Proper event has no production Proper at ' + source.id);
        }
        if ((!source.seat || source.seat.placement !== 'seated') &&
            !typedUnplacedSeat(source)) {
          throw new Error('appointed Proper has no usable semantic Ordinary seat: ' + source.id);
        }
        const node = semanticNode(renderEvent(source, proper, bible, fragments, state),
          source, ordinals.get(source.id));
        const unplaced = typedUnplacedSeat(source);
        node.dataset.readerLocusMajor = unplaced
          ? 'Exceptional source-order propers' : division;
        node.dataset.readerLocusUnit = source.editionSlotLabel || proper.name || 'Proper';
        contents.push({ id: source.id, label: source.editionSlotLabel || proper.name || 'Proper',
          element: node, group: unplaced ? 'Exceptional source-order propers' : 'Appointed propers' });
        return node;
      }
    });
    const selection = window.OrdinarySeating.selectionMap(ordinary, state.options.legitimate || {});
    window.OrdinarySeating.variantGroupsOf(ordinary).forEach(function (group) {
      const keys = new Set();
      let sectionKey = null;
      (ordinary.sections || []).forEach(function (section) {
        (section.elements || []).forEach(function (element) {
          if ((element.alternatives || []).some(function (row) { return row.group === group.group; }) ||
              (group.options || []).some(function (option) { return option.id === element.variant; })) {
            keys.add(element.key);
            if (!sectionKey) sectionKey = section.key;
          }
        });
      });
      const nodes = Array.from(frame.querySelectorAll('[data-semantic-event-id]'));
      const target = nodes.find(function (node) {
        return node.dataset.semanticEventId.startsWith('ordinary-element/') &&
          keys.has(node.dataset.semanticEventId.slice('ordinary-element/'.length));
      }) || nodes.find(function (node) {
        return node.dataset.semanticEventId === 'ordinary-section/' + sectionKey;
      });
      if (!target) {
        throw new Error('the production Ordinary has no semantic seat for option ' + group.group);
      }
      target.before(ordinaryChoice(group, selection[group.group]));
    });
    fragment.appendChild(frame);
    fragment.appendChild(OrdinaryRenderer.ordinaryPreamble(ordinary));
  }

    function renderMissal(input) {
      const { fragment, contents, result, mass, bible, fragments, state } = input;
      renderMissalEvents(fragment, contents, result, mass, bible, fragments, state);
    }
    return Object.freeze({
      renderFormChoice: renderFormChoice,
      renderEvent: renderEvent,
      renderProperChoiceEvent: renderProperChoiceEvent,
      typedUnplacedSeat: typedUnplacedSeat,
      properChoiceLabel: properChoiceLabel,
      nearestProperLocation: nearestProperLocation,
      renderMissal: renderMissal
    });
  }

  window.TriptychPropersEvents = Object.freeze({ create: create });
}());
