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
      form: held.form
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

  return Object.freeze({ renderProperChoice: renderProperChoice,
    properChoiceRemovals: properChoiceRemovals });
}));
