/* Native source choice controls shared by both reader entrances. */
'use strict';

(function (root, factory) {
  const api = factory(root);
  if (typeof module === 'object' && module && module.exports) module.exports = api;
  else root.TriptychSourceChoiceControls = api;
}(typeof globalThis !== 'undefined' ? globalThis : this, function (root) {
  // Preserve independent source choices and retire the input-only scalar alias.
  // The owning adapter validates group identities and source applicability.
  function properChoiceRequest(state, group, option) {
    const choices = Object.assign({}, state.properChoices || {});
    if (state.alternative) {
      const id = state.alternative.id;
      const at = id.lastIndexOf('/');
      choices[id.slice(0, at)] = id.slice(at + 1);
    }
    choices[group] = option;
    const request = Object.assign({}, state, { properChoices: choices });
    delete request.alternative;
    return request;
  }

  function adaptProperChoiceRequest(state, group, option, adapt) {
    const request = properChoiceRequest(state, group, option);
    try {
      adapt(request);
    } catch (error) {
      // A witness can belong solely to the prayer the reader just omitted.
      if (!request.languages || !request.languages.translationWitness ||
          error.message !== 'explicit translation witness selected no appointed text') throw error;
      request.languages = Object.assign({}, request.languages);
      delete request.languages.translationWitness;
      adapt(request);
    }
    return request;
  }

  function properChoiceRemovals(state, updates, removals) {
    const held = state || {};
    const identity = {
      date: held.civilDate, missal: held.edition && held.edition.id,
      type: held.formulary && held.formulary.type,
      mass: held.formulary && held.formulary.id ||
        held.selectedReadableFormulary && held.selectedReadableFormulary.id,
      form: held.form, cycle: held.cycle
    };
    const removed = removals || [];
    const changed = Object.keys(identity).some(function (key) {
      return removed.indexOf(key) >= 0 ||
        Object.prototype.hasOwnProperty.call(updates || {}, key) &&
        (updates[key] || null) !== (identity[key] || null);
    });
    return changed ? removed.concat(['proper-choices', 'alternative', '_candidate-alternative']) : removed;
  }

  function renderProperChoice(input) {
    const T = input.T;
    const event = input.event;
    const selected = input.selected;
    const missal = input.state && input.state.requestedMode === 'missal';
    const wrapper = input.wrapper;
    wrapper.dataset.properChoice = event.group;
    wrapper.dataset.choiceState = event.selection.state;
    if (selected) wrapper.dataset.choiceSelection = selected;
    const title = T.el(input.heading, 'proper-choice-title', input.label);
    title.id = input.titleId;
    wrapper.setAttribute('aria-labelledby', title.id);
    wrapper.appendChild(title);
    let settings = wrapper;
    if (missal && selected) {
      settings = T.el('details', 'proper-choice-settings');
      settings.appendChild(T.el('summary', null, 'Change source option'));
      wrapper.appendChild(settings);
    }
    if (!missal) {
      wrapper.appendChild(T.el('p', 'proper-choice-note', selected
        ? 'The selected source option is shown first. Other source options remain collapsed and are not cumulative.'
        : 'The source appoints one of these alternatives here. None is selected; the option groups below are not cumulative.'));
    }
    const basis = T.el('p', 'composed-note proper-choice-basis', event.choiceBasis);
    if (missal && !selected) {
      const detail = T.el('details', 'proper-choice-settings');
      detail.appendChild(T.el('summary', null, 'Source of these alternatives'));
      detail.appendChild(basis);
      wrapper.appendChild(detail);
    } else settings.appendChild(basis);
    const controls = T.el('fieldset', 'ordinary-choice proper-choice-controls');
    controls.appendChild(T.el('legend', null, 'Choose a source option'));
    const choices = T.el('div', 'ordinary-choice-options');
    event.options.forEach(function (option) {
      const label = T.el('label', 'ordinary-choice-option');
      const radio = root.document.createElement('input');
      radio.type = 'radio';
      radio.name = 'reader-' + input.titleId;
      radio.value = option.id;
      radio.checked = selected === option.id;
      const optionName = T.titleCase(String(option.id).replace(/[-_]+/g, ' '));
      function candidate() {
        return adaptProperChoiceRequest(input.state, event.id, option.id, input.adapt);
      }
      try { candidate(); } catch (_error) { radio.disabled = true; }
      radio.addEventListener('change', function () {
        if (!radio.checked || radio.disabled) return;
        let request;
        try { request = candidate(); } catch (_error) { return; }
        const removals = ['alternative', '_candidate-alternative'];
        if (input.state.languages && input.state.languages.translationWitness &&
            !request.languages.translationWitness) removals.push('translation-witness', '_candidate-translation-witness');
        input.navigate({ 'proper-choices': JSON.stringify(request.properChoices) }, removals, {
            location: input.location, focus: input.focus
          });
      });
      label.appendChild(radio);
      label.appendChild(root.document.createTextNode(optionName +
        (radio.disabled ? ' — unavailable for this context' : '')));
      choices.appendChild(label);
    });
    controls.appendChild(choices);
    settings.appendChild(controls);
    const options = T.el('div', 'proper-choice-options');
    const displayed = selected ? event.options.filter(option => option.id === selected)
      .concat(missal ? [] : event.options.filter(option => option.id !== selected)) : event.options;
    displayed.forEach(function (option) {
      const isSelected = selected === option.id;
      const optionName = T.titleCase(String(option.id).replace(/[-_]+/g, ' '));
      const optionNode = (selected || missal) && !isSelected
        ? root.document.createElement('details') : T.el('section', 'proper-choice-option');
      optionNode.classList.add('proper-choice-option');
      optionNode.dataset.properChoiceOption = option.id;
      optionNode.dataset.choiceStatus = isSelected ? 'selected' :
        (selected ? 'not-selected' : 'available');
      if (isSelected) optionNode.setAttribute('aria-current', 'true');
      const label = (isSelected ? 'Selected option: ' :
        (selected ? 'Other source option: ' : 'Option: ')) + optionName;
      optionNode.appendChild(T.el(optionNode.tagName === 'DETAILS' ? 'summary' : input.optionHeading,
        'proper-choice-option-title', label));
      (option.events || []).forEach(function (member) {
        const node = input.renderMember(member);
        node.classList.add('proper-choice-member');
        node.dataset.properChoiceMemberEvent = member.id;
        optionNode.appendChild(node);
      });
      options.appendChild(optionNode);
    });
    wrapper.appendChild(options);
    return wrapper;
  }

  function attachSourcePathChoices(input) {
    const T = input.T;
    const first = input.root.firstChild;
    const prefix = input.prefix || '';
    function label(id) { return T.titleCase(String(id).replace(/[-_]+/g, ' ')); }
    function condition(path) {
      const when = path && path.condition;
      const status = path && path.applicability;
      const text = when ? ' Source condition: ' + label(when.fact) +
        ' in ' + (when.in || []).map(label).join(', ') + '.' : '';
      return text + (status && status.state !== 'applicable'
        ? ' Applicability ' + status.state + ': ' + label(status.reason || status.state) + '.' : '');
    }
    (input.result.sourcePathChoices || []).forEach(function (relation) {
      const wrapper = T.el('section', 'source-path-choice');
      wrapper.dataset.sourcePathChoice = relation.id;
      const selected = relation.paths.find(function (path) { return path.id === relation.selection.option; });
      wrapper.appendChild(T.el('p', 'composed-note source-path-note',
        (selected ? 'Source reading path: ' + label(selected.id) + ' (' + selected.standing + ').'
          : 'Choose one source reading path; none is selected.') +
        ' Source basis: ' + relation.basis + condition(selected)));
      const controls = T.el('fieldset', 'ordinary-choice source-path-controls');
      controls.dataset.optionGroup = relation.id;
      controls.dataset.optionBranch = prefix;
      controls.appendChild(T.el('legend', null, 'Source reading path: ' + label(relation.id.split('/').pop())));
      const options = T.el('div', 'ordinary-choice-options');
      relation.paths.forEach(function (path) {
        const option = T.el('label', 'ordinary-choice-option');
        const radio = root.document.createElement('input');
        radio.type = 'radio';
        radio.name = 'reader-source-path-' + prefix + relation.id;
        radio.value = path.id;
        radio.checked = relation.selection.state === 'selected' && relation.selection.option === path.id;
        function candidate() {
          const request = properChoiceRequest(input.state, relation.id, path.id);
          relation.ownedChoiceIds.forEach(function (id) { delete request.properChoices[id]; });
          Object.assign(request.properChoices, path.choices, { [relation.id]: path.id });
          const result = input.adapt(request);
          const choice = (result.sourcePathChoices || []).find(function (row) { return row.id === relation.id; });
          const actual = choice && choice.paths.find(function (row) { return row.id === path.id; });
          if (!choice || choice.selection.state !== 'selected' || choice.selection.option !== path.id ||
              !actual || actual.applicability.state !== 'applicable') {
            throw new Error('source path is not admitted by the owning adapter');
          }
          if (choice.focusEventId && !(result.events || []).some(function (event) { return event.id === choice.focusEventId; })) {
            throw new Error('source path focus is absent from its admitted semantic events');
          }
          return { request: request, choice: choice };
        }
        radio.disabled = path.applicability.state !== 'applicable';
        if (!radio.disabled) {
          try { candidate(); } catch (_error) { radio.disabled = true; }
        }
        radio.addEventListener('change', function () {
          if (!radio.checked || radio.disabled) return;
          let next;
          try { next = candidate(); } catch (_error) { return; }
          const event = next.choice.focusEventId && prefix + next.choice.focusEventId;
          input.navigate({ 'proper-choices': JSON.stringify(next.request.properChoices) },
            ['alternative', '_candidate-alternative'], {
              location: event ? { kind: 'event', id: event } : null,
              focus: event ? { kind: 'proper-choice-result', event: event } : {
                kind: 'source-path-option', group: relation.id, option: path.id, branch: prefix
              }
            });
        });
        option.appendChild(radio);
        option.appendChild(root.document.createTextNode(label(path.id) + ' (' + path.standing + ')' +
          (radio.disabled ? ' — unavailable for this context' + condition(path) : '')));
        options.appendChild(option);
      });
      controls.appendChild(options);
      wrapper.appendChild(controls);
      if (relation.beforeEventId) {
        const target = Array.from(input.root.querySelectorAll('[data-semantic-event-id]')).find(
          function (node) { return node.dataset.semanticEventId === relation.beforeEventId; }
        );
        if (!target) throw new Error('source path has no existing rendering placement');
        target.before(wrapper);
      } else input.root.insertBefore(wrapper, first);
    });
  }

  function sourcePrayerWitness(input, rows) {
    const id = input.state.languages.translationWitness;
    if (!id || !rows.length) return null;
    const report = input.T.summarizeCoverage(rows.flatMap(row => input.T.coverageUnitsOf(row.proper)));
    return input.T.coverageWitnesses(report, input.state.languages.orations).some(row =>
      row.id === id || (row.aliases || []).includes(id)) ? id : null;
  }

  function prayerSourceHref(input, mass, formId, index, witness) {
    const url = new URL('index.html', root.location.href);
    url.search = root.location.search;
    const state = input.state;
    const params = new URLSearchParams({missal: input.structure.calendar, type: mass.kind,
      mass: mass.key, bible: state.bible.id, orations: state.languages.orations, mode: 'read'});
    if (formId !== 'main') params.set('form', formId);
    if (state.textDisplay) params.set('text-display', state.textDisplay);
    if (state.scriptureCompanion) params.set('scripture-companion', state.scriptureCompanion.id);
    if (witness) params.set('translation-witness', witness);
    if (index >= 0) {
      const disposition = mass.propers[index].ordinary_disposition;
      const location = disposition && disposition.kind === 'alternative'
        ? ['proper-choice', input.structure.calendar, mass.key, formId, disposition.group].join('/')
        : ['proper', input.structure.calendar, mass.key, String(index + 1).padStart(3, '0')].join('/');
      params.set('location', location);
    }
    url.hash = params.toString();
    return url.href;
  }

  function memorialPrayerControl(input, role, sources, feria) {
    const T = input.T;
    const control = T.el('details', 'memorial-prayer-source');
    control.dataset.memorialPrayer = role;
    const summary = T.el('summary', null, role + ' · Choose a source');
    control.appendChild(summary);
    const picker = T.el('select');
    const label = T.el('label', null, 'Prayer source ');
    label.appendChild(picker);
    control.appendChild(label);
    const content = T.el('div', 'memorial-prayer-preview');
    content.setAttribute('aria-live', 'polite');
    control.appendChild(content);
    const source = T.el('a', 'composed-note', 'Memorial in the 2002 Missal');
    source.href = sources.url;
    control.appendChild(source);

    const options = new Map();
    function appendOption(parent, text, value) {
      const option = T.el('option', null, text);
      option.value = value;
      parent.appendChild(option);
    }
    function addSource(parent, mass, form, qualification, groupId) {
      const value = [groupId, mass.key, form.id].join('/');
      if (options.has(value)) return;
      options.set(value, {mass: mass.key, form: form.id, label: form.name, qualification: qualification});
      appendOption(parent, form.name, value);
    }
    function initialize() {
      if (!control.open || picker.options.length) return;
      appendOption(picker, 'Choose a source', '');
      for (const group of sources.groups) {
        if (group.season && input.season && (group.season === 'outside-easter'
          ? input.season === 'easter' : group.season !== input.season)) continue;
        const mass = input.structure.masses.find(function (one) { return one.key === group.mass; });
        const optgroup = T.el('optgroup');
        optgroup.label = group.label;
        for (const formId of group.form_ids) {
          const form = mass.forms.find(function (one) { return one.id === formId; });
          addSource(optgroup, mass, form, group.qualification, group.id);
        }
        if (optgroup.childElementCount) picker.appendChild(optgroup);
      }
      if (feria) {
        const weekday = input.structure.masses.find(function (one) { return one.key === feria.mass; });
        if (feria.options.length) {
          const weekdays = T.el('optgroup');
          weekdays.label = weekday.name + ' · permitted prayer sources';
          feria.options.forEach(function (owner) {
            addSource(weekdays, {key: owner.id}, {id: 'main', name: owner.label},
              weekday.name + ' · ' + feria.locus, 'feria');
          });
          picker.appendChild(weekdays);
        } else addSource(picker, weekday, {id: 'main', name: weekday.name}, null, 'feria');
      }
      if (!feria && sources.current_feria) {
        const note = T.el('p', 'composed-note', 'For a memorial celebrated on a weekday, GIRM 363 also permits that weekday’s prayer.');
        control.insertBefore(note, source);
      }
    }
    control.addEventListener('toggle', initialize);
    picker.addEventListener('change', async function () {
      const key = picker.value;
      const choice = options.get(key);
      content.replaceChildren();
      summary.textContent = role + (choice ? ' · ' + choice.label : ' · Choose a source');
      if (!choice) return;
      try {
        await root.LiturgyReaderProperPayload.hydrate({
          structure: input.structure, roots: [choice.mass], load: input.load
        });
        if (picker.value !== key) return;
        const mass = input.structure.masses.find(function (one) { return one.key === choice.mass; });
        const rows = mass.propers.map(function (proper, index) { return {proper: proper, index: index}; })
          .filter(function (row) { return row.proper.form_id === choice.form && row.proper.name === role; });
        const january = feria && feria.mass === mass.key && root.MassAssembly.januaryWeekdayPrayers({
          mass: mass, derived: input.derived, branch: input.branch});
        if (january) {
          const prayer = january.prayers.find(one => one.role === role);
          if (prayer) {
            content.appendChild(T.renderJanuaryPrayer(prayer, january, input.state, 'h4'));
            return;
          }
        }
        if (choice.qualification) content.appendChild(T.el('p', 'composed-note', choice.qualification));
        if (!rows.length) content.appendChild(T.el('p', 'composed-note',
          'This weekday has no fixed prayer here. Consult its appointed prayer choices.'));
        const link = T.el('a', null, rows.length ? 'Open this prayer in the formulary' : 'Open the weekday formulary');
        const witness = sourcePrayerWitness(input, rows);
        link.href = prayerSourceHref(input, mass, choice.form, rows.length ? rows[0].index : -1, witness);
        content.appendChild(link);
        const english = T.prayerWitness(mass, choice.form, role);
        if (english && input.state.languages.orations === 'en') content.appendChild(T.publishedPrayerLink(english));
        for (const witness of T.missalWitnessLinks(mass, choice.form)) {
          if (witness.language !== 'la' || witness.scope !== 'form') continue;
          const anchor = T.el('a', null, witness.edition_label + ' · ' + witness.locus);
          anchor.href = witness.url;
          content.appendChild(anchor);
        }
        if (!rows.length) return;
        const preview = T.el('div');
        let revision = 0;
        async function show(row) {
          const serial = ++revision;
          preview.replaceChildren();
          if (!row) return;
          const citations = T.citationsOf({propers: [row.proper]});
          let fragments = input.fragments;
          if (citations.length) {
            try { fragments = await T.fetchFragments(input.bible, citations, input.state, input.bibles); }
            catch (_error) {
              if (serial === revision) preview.textContent = 'The selected Scripture text could not be loaded.';
              return;
            }
          }
          if (serial !== revision || picker.value !== key) return;
          preview.replaceChildren(T.renderProper(row.proper, input.bible, fragments, {
            numbering: input.structure.numbering, orations: input.state.languages.orations,
            textDisplay: input.state.textDisplay, translationWitness: witness,
            structure: input.structure, heading: 'h4'
          }));
        }
        if (rows.length === 1) await show(rows[0]);
        else {
          const variants = T.el('select');
          const field = T.el('label', null, 'Prayer variant ');
          field.appendChild(variants);
          appendOption(variants, 'Choose a variant', '');
          rows.forEach(function (row, ordinal) {
            appendOption(variants, 'Option ' + (ordinal + 1), String(ordinal));
          });
          variants.addEventListener('change', function () {
            show(variants.value ? rows[Number(variants.value)] : null);
          });
          content.appendChild(field);
        }
        content.appendChild(preview);
      } catch (_error) {
        if (picker.value === key) content.replaceChildren(T.el('p', 'composed-note',
          'This prayer source could not be loaded. The memorial source is available below.'));
      }
    });
    return control;
  }

  function votiveChantChooser(input) {
    const chants = input.mass.off_date_chants;
    if (!chants || !chants.length) return null;
    const T = input.T;
    const control = T.el('details', 'memorial-prayer-source votive-chant-chooser');
    control.dataset.votiveMass = input.mass.key;
    control.appendChild(T.el('summary', null, 'Seasonal and votive chants'));
    const select = T.el('select');
    const label = T.el('label', null, 'Off-date provision ');
    label.appendChild(select);
    control.appendChild(label);
    select.appendChild(T.el('option', null, 'Choose a chant'));
    chants.forEach(chant => {
      const option = T.el('option', null, chant.label);
      option.value = chant.id;
      select.appendChild(option);
    });
    const preview = T.el('div', 'votive-chant-preview');
    preview.setAttribute('aria-live', 'polite');
    control.appendChild(preview);
    select.addEventListener('change', async () => {
      const chant = chants.find(one => one.id === select.value);
      preview.replaceChildren();
      if (!chant) return;
      const witness = T.el('a', null, chant.source.edition_label + ' · ' + chant.source.locus);
      witness.href = chant.source.url;
      preview.appendChild(witness);
      const common = chant.common;
      if (!common) {
        preview.appendChild(T.el('p', 'composed-note', 'Consult the 1962 facsimile for the chant wording.'));
        return;
      }
      try {
        await root.LiturgyReaderProperPayload.hydrate({
          structure: input.structure, load: input.load, roots: [common.mass]});
        const mass = input.structure.masses.find(one => one.key === common.mass);
        const proper = mass && mass.propers[common.index];
        if (!proper || proper.name !== chant.role) throw new Error('Missing Common chant');
        const fragments = await T.fetchFragments(input.bible, T.citationsOf({propers: [proper]}), input.state, input.bibles);
        if (select.value !== chant.id) return;
        preview.appendChild(T.el('p', 'composed-note', common.label + ' · ' + common.qualification));
        preview.appendChild(T.renderProper(proper, input.bible, fragments, {structure: input.structure,
          numbering: input.structure.numbering, orations: input.state.languages.orations,
          textDisplay: input.state.textDisplay, heading: 'h4'}));
      } catch (_error) {
        if (select.value === chant.id) preview.appendChild(T.el('p', 'composed-note', 'The Common chant could not be loaded.'));
      }
    });
    return control;
  }

  function januaryPrayerChooser(input) {
    const source = input.mass.january_prayer_sources;
    if (!source) return null;
    const T = input.T;
    const chooser = T.el('details', 'memorial-prayer-source january-prayer-chooser');
    chooser.appendChild(T.el('summary', null, 'Prayers for the weekday of Christmas Time'));
    function select(label, entries) {
      const field = T.el('label', null, label + ' ');
      const picker = T.el('select');
      for (const [value, text] of entries) {
        const opt = T.el('option', null, text);
        opt.value = value;
        picker.appendChild(opt);
      }
      field.appendChild(picker);
      chooser.appendChild(field);
      return picker;
    }
    const weekday = select('Weekday', [['','Choose a weekday']].concat(source.weekdays.map(row => [row.weekday, row.label])));
    const phase = select('Local observance', [['','Choose an observance'],
      ['before-epiphany','Before Epiphany'], ['after-epiphany','After Epiphany']]);
    const preview = T.el('div', 'january-prayer-preview');
    preview.setAttribute('aria-live', 'polite');
    chooser.appendChild(preview);
    chooser.addEventListener('change', async function () {
      preview.replaceChildren();
      if (!weekday.value || !phase.value) return;
      try {
        if (!root.MassAssembly) await import('./assembly-model.js');
        const selection = root.MassAssembly.januaryPrayerSelection(source, Number(weekday.value), phase.value);
        if (!selection) return;
        preview.replaceChildren(...selection.prayers.map(prayer => T.renderJanuaryPrayer(prayer, selection, input.state, 'h3')));
        const antiphons = T.el('a', null, selection.label + ' · English Entrance and Communion antiphons');
        antiphons.href = selection.english_url;
        preview.appendChild(antiphons);
      } catch (_error) {
        preview.textContent = 'The weekday prayers could not be loaded.';
      }
    });
    const link = T.el('a', 'composed-note', 'Weekday rubric in the 2002 Missal');
    link.href = source.rule_url;
    chooser.appendChild(link);
    return chooser;
  }

  function attachMemorialPrayers(input) {
    const sources = input.mass.memorial_prayer_sources;
    if (!sources) return;
    const feria = input.branch && root.MassAssembly.memorialFeriaPrayerSources(input);
    const slots = {'Prayer over the Offerings': 'praeparatio-donorum/super-oblata',
      'Prayer after Communion': 'ritus-communionis/post-communionem'};
    sources.roles.forEach(function (role) {
      const control = memorialPrayerControl(input, role, sources, feria);
      const seat = input.root.querySelector('[data-semantic-event-id="ordinary-element/' + slots[role] + '"]');
      if (seat) seat.after(control);
      else {
        const communion = role === 'Prayer over the Offerings' &&
          Array.from(input.root.querySelectorAll('[data-reader-locus-unit]')).find(function (one) {
            return one.dataset.readerLocusUnit === 'Communion Antiphon';
          });
        if (communion) communion.before(control);
        else input.root.appendChild(control);
      }
    });
  }

  /** Date-surface presentation over the Day controller's validated result. */
  function createDayDateControls(input) {
    const T = input.T;
    const runtime = input.runtime;
    const resultMass = input.resultMass;
    const ordinaryVariantGroups = input.ordinaryVariantGroups;
    const ordinarySelectionMap = input.ordinarySelectionMap;
    const dateForm = root.document.getElementById('date-form');
    const dateInput = root.document.getElementById('reader-date');
    const missalSelect = root.document.getElementById('reader-missal');
    const bibleSelect = root.document.getElementById('reader-bible');
    const orationsSelect = root.document.getElementById('reader-orations');
    const formularyField = root.document.getElementById('reader-formulary-field');
    const formularySelect = root.document.getElementById('reader-formulary');
    const massFormField = root.document.getElementById('reader-mass-form-field');
    const massFormSelect = root.document.getElementById('reader-mass-form');
    const ordinaryLangField = root.document.getElementById('reader-ordinary-lang-field');
    const ordinaryLangSelect = root.document.getElementById('reader-ordinary-lang');
    const ordinaryOptionField = root.document.getElementById('reader-ordinary-option-field');
    const ordinaryOptionSelect = root.document.getElementById('reader-ordinary-option');
    const dateSurface = root.document.getElementById('date-surface');
    const dateStatus = dateSurface.querySelector('.surface-note');
    const dateStepButtons = Array.from(dateSurface.querySelectorAll('.date-steps button'));

    // Keep Date, missal, Apply, and Today live after an invalid day.
    function setDateSurfaceEnabled(enabled) {
      [bibleSelect, orationsSelect, formularySelect,
        ordinaryLangSelect, ordinaryOptionSelect].forEach(function (control) {
        control.disabled = !enabled;
      });
      if (massFormSelect) massFormSelect.disabled = !enabled;
      // These escape controls also stay live before manifests finish loading.
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
      // Keep manifest choices and the explicit missal visible after failure.
      T.fillSelect(missalSelect, (runtime.missals || []).map(function (row) {
        return { value: row.id, label: row.label, title: row.edition || row.code || row.id };
      }));
      const asked = new URLSearchParams(root.location.hash.replace(/^#/, '')).get('missal');
      missalSelect.value = (runtime.missals || []).some(function (row) {
        return row.id === asked;
      }) ? asked : '';
      formularyField.hidden = true;
      if (massFormField) {
        massFormField.hidden = true;
        massFormSelect.replaceChildren();
      }
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
      // Do not let a native select preselect a coequal formulary.
      if (readable.length > 1 && runtime.result && runtime.result.resolved &&
          runtime.mode !== 'compare') {
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
      if (massFormField) {
        const mass = resultMass(runtime.result);
        const forms = mass && mass.forms || [];
        const selected = runtime.result && runtime.result.resolved && runtime.result.resolved.form;
        // The first choice stays in the reading, with no native-select default.
        // Only an already selected form exposes its Mass's source-authored peers.
        if (forms.length > 1 && forms.some(function (form) { return form.id === selected; }) &&
            runtime.mode !== 'compare') {
          T.fillSelect(massFormSelect, forms.map(function (form) {
            return { value: form.id, label: form.name };
          }));
          massFormSelect.value = selected;
          massFormField.hidden = false;
        } else {
          massFormField.hidden = true;
          massFormSelect.replaceChildren();
        }
      }
      if (state.options.ordinary && runtime.ordinary) {
        const languages = T.orationLanguagesOf(runtime.ordinary);
        T.fillSelect(ordinaryLangSelect, languages.map(function (row) {
          return {
            value: row.lang,
            label: T.orationLanguageLabel(row)
          };
        }));
        ordinaryLangSelect.value = state.languages.ordinary || 'en';
        ordinaryLangField.hidden = languages.length < 2;
        const groups = ordinaryVariantGroups(runtime.ordinary);
        if (groups.length === 1) {
          const group = groups[0];
          T.fillSelect(ordinaryOptionSelect, (group.options || []).map(function (option) {
            return { value: option.id, label: option.name };
          }));
          const chosen = ordinarySelectionMap(state, runtime.ordinary)[group.group];
          if (chosen) ordinaryOptionSelect.value = chosen;
          ordinaryOptionField.hidden = false;
        } else {
          ordinaryOptionField.hidden = true;
          ordinaryOptionSelect.replaceChildren();
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

    return Object.freeze({ setEnabled: setDateSurfaceEnabled,
      reset: resetDateSurface, populate: populateDateSurface });
  }

  return Object.freeze({ adaptProperChoiceRequest: adaptProperChoiceRequest, renderProperChoice: renderProperChoice,
    attachSourcePathChoices: attachSourcePathChoices, attachMemorialPrayers: attachMemorialPrayers,
    januaryPrayerChooser: januaryPrayerChooser, votiveChantChooser: votiveChantChooser,
    properChoiceRemovals: properChoiceRemovals, createDayDateControls: createDayDateControls });
}));
