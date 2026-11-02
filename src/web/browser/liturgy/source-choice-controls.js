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
    const wrapper = input.wrapper;
    wrapper.dataset.properChoice = event.group;
    wrapper.dataset.choiceState = event.selection.state;
    if (selected) wrapper.dataset.choiceSelection = selected;
    const title = T.el(input.heading, 'proper-choice-title', input.label);
    title.id = input.titleId;
    wrapper.setAttribute('aria-labelledby', title.id);
    wrapper.appendChild(title);
    wrapper.appendChild(T.el('p', 'proper-choice-note', selected
      ? 'The selected source option is shown first. Other source options remain collapsed and are not cumulative.'
      : 'The source appoints one of these alternatives here. None is selected; the option groups below are not cumulative.'));
    wrapper.appendChild(T.el('p', 'composed-note proper-choice-basis',
      'Source basis: ' + event.choiceBasis));
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
        const request = properChoiceRequest(input.state, event.id, option.id);
        input.adapt(request);
        return request;
      }
      try { candidate(); } catch (_error) { radio.disabled = true; }
      radio.addEventListener('change', function () {
        if (!radio.checked || radio.disabled) return;
        let request;
        try { request = candidate(); } catch (_error) { return; }
        input.navigate({ 'proper-choices': JSON.stringify(request.properChoices) },
          ['alternative', '_candidate-alternative'], {
            location: input.location, focus: input.focus
          });
      });
      label.appendChild(radio);
      label.appendChild(root.document.createTextNode(optionName +
        (radio.disabled ? ' — unavailable for this context' : '')));
      choices.appendChild(label);
    });
    controls.appendChild(choices);
    wrapper.appendChild(controls);
    const options = T.el('div', 'proper-choice-options');
    const displayed = selected ? event.options.filter(function (option) { return option.id === selected; })
      .concat(event.options.filter(function (option) { return option.id !== selected; })) : event.options;
    displayed.forEach(function (option) {
      const isSelected = selected === option.id;
      const optionName = T.titleCase(String(option.id).replace(/[-_]+/g, ' '));
      const optionNode = selected && !isSelected
        ? root.document.createElement('details') : T.el('section', 'proper-choice-option');
      optionNode.classList.add('proper-choice-option');
      optionNode.dataset.properChoiceOption = option.id;
      optionNode.dataset.choiceStatus = isSelected ? 'selected' :
        (selected ? 'not-selected' : 'available');
      if (isSelected) optionNode.setAttribute('aria-current', 'true');
      const label = (isSelected ? 'Selected option: ' :
        (selected ? 'Other source option: ' : 'Option: ')) + optionName;
      optionNode.appendChild(T.el(optionNode.tagName === 'DETAILS' ? 'summary' : input.optionHeading,
        'proper-choice-option-title', label + (optionNode.tagName === 'DETAILS' ? ' (not selected)' : '')));
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
      if (readable.length > 1 && runtime.outcome !== 'unresolved' && runtime.mode !== 'compare') {
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

  return Object.freeze({ renderProperChoice: renderProperChoice,
    attachSourcePathChoices: attachSourcePathChoices,
    properChoiceRemovals: properChoiceRemovals, createDayDateControls: createDayDateControls });
}));
