/* Shared two-side Proper Compare presentation over independently resolved results.
 * Calendar resolution and semantic pairing belong to the adapters and
 * reader-comparison.js. This module only presents their typed result.
 */
'use strict';

(function (root, factory) {
  const api = factory(root);
  if (typeof module === 'object' && module && module.exports) module.exports = api;
  else root.LiturgyReaderCompareView = api;
}(typeof globalThis !== 'undefined' ? globalThis : this, function (root) {
  const SLOT_LABELS = Object.freeze({
    'entrance-antiphon': 'Entrance antiphon',
    collect: 'Collect',
    'reading-1': 'First reading',
    gradual: 'Gradual',
    'responsorial-psalm': 'Responsorial psalm',
    'reading-2': 'Second reading',
    'gospel-acclamation': 'Gospel acclamation',
    gospel: 'Gospel',
    'offertory-chant': 'Offertory chant',
    'prayer-over-offerings': 'Prayer over the offerings',
    'communion-antiphon': 'Communion antiphon',
    'prayer-after-communion': 'Prayer after Communion'
  });
  const STATUS_NOTES = Object.freeze({
    'no-event-in-selected-formulary':
      'No corresponding mapped Proper event belongs to this selected formulary.',
    'text-unavailable':
      'A Proper event is modeled here, but its selected text is unavailable.',
    'selected-material-absent':
      'This modeled Proper has an explicitly absent selected material state.',
    'choice-required':
      'A source choice is required here. No text has been selected.'
  });

  function fail(message) { throw new Error('reader Compare view: ' + message); }

  function project(view) {
    if (!view || view.schema !== 'triptych-liturgy-reader-comparison/v1' ||
        ['day', 'propers'].indexOf(view.entrance) < 0 ||
        !Array.isArray(view.sides) || view.sides.length !== 2 ||
        !Array.isArray(view.units)) fail('a resolved two-side comparison is required');
    if (view.entrance === 'day' &&
        (!Array.isArray(view.calendarResults) || view.calendarResults.length !== 2)) {
      fail('Day needs both independently resolved calendar results');
    }
    if (view.entrance === 'propers' && view.calendarResults !== null) {
      fail('Propers has no civil-date calendar result');
    }
    const ids = view.sides.map(function (side) { return side.id; });
    if (!ids[0] || !ids[1] || ids[0] === ids[1]) fail('side identities must be distinct');
    const calendars = view.entrance === 'day' ? view.calendarResults.map(function (row, index) {
      if (!row || row.id !== ids[index] || !row.calendarResult || !row.resolved) {
        fail('calendar result does not match its comparison side');
      }
      return {
        id: row.id,
        winner: row.calendarResult.winner || null,
        formulary: row.resolved.formulary || null,
        calendar: row.calendarResult.calendar,
        territory: row.calendarResult.territory || 'universal'
      };
    }) : null;
    const seen = new Set();
    const units = view.units.map(function (unit) {
      const slot = unit && unit.semanticSlot;
      if (!SLOT_LABELS[slot] || seen.has(slot) ||
          unit.relation !== 'functional-slot-only' ||
          !Array.isArray(unit.sides) || unit.sides.length !== 2) {
        fail('units must be distinct mapped functional Proper slots');
      }
      seen.add(slot);
      const cells = unit.sides.map(function (cell, index) {
        if (!cell || cell.id !== ids[index] ||
            ['text-held', 'no-event-in-selected-formulary', 'text-unavailable',
              'selected-material-absent', 'choice-required'].indexOf(cell.status) < 0 ||
            (cell.status === 'no-event-in-selected-formulary') !== (cell.event === null)) {
          fail('a unit cell has an inconsistent side, event, or status');
        }
        return { id: cell.id, status: cell.status, event: cell.event };
      });
      return {
        slot: slot, label: SLOT_LABELS[slot],
        location: 'compare/proper/' + slot, sides: cells
      };
    });
    return {
      entrance: view.entrance, dimension: view.dimension,
      anchor: view.anchor, sideIds: ids, calendars: calendars, units: units
    };
  }

  function properFor(side, event) {
    const hook = (event.sourceHooks || []).find(function (one) {
      return one && one.kind === 'proper-structure';
    });
    const prefix = side.structure.calendar + '/' + side.mass.key + '/';
    if (!hook || typeof hook.id !== 'string' || !hook.id.startsWith(prefix)) {
      fail('held Proper event has no matching source structure hook');
    }
    const ordinal = hook.id.slice(prefix.length);
    if (!/^\d{3}$/.test(ordinal)) fail('Proper source hook has no stable ordinal');
    const proper = (side.mass.propers || [])[Number(ordinal) - 1];
    if (!proper) fail('held Proper source hook does not resolve');
    return proper;
  }

  function render(input) {
    const T = root.Triptych;
    if (!T || typeof T.el !== 'function' || typeof T.renderProper !== 'function' ||
        !root.document || typeof root.document.createDocumentFragment !== 'function') {
      fail('production Proper renderer and DOM are required');
    }
    const projected = project(input && input.view);
    const sides = input && input.sides;
    if (!Array.isArray(sides) || sides.length !== 2 || sides.some(function (side, index) {
      return !side || side.id !== projected.sideIds[index] || !side.structure ||
        !side.mass || !side.bible || !(side.fragments instanceof Map);
    })) fail('each side needs its matching structure, Mass, Bible, and fragments');

    const fragment = root.document.createDocumentFragment();
    const contents = [];
    const intro = T.el('section', 'compare-intro');
    intro.appendChild(T.el('h2', null, 'Compare corresponding Propers'));
    intro.appendChild(T.el('p', null,
      'Pairs follow functional liturgical slots. A shared slot does not by itself establish identical wording or a historical change.'));
    if (projected.entrance === 'day') {
      intro.appendChild(T.el('p', 'compare-anchor',
        'Fixed date: ' + projected.anchor.civilDate +
        ' · Territorial context: ' + projected.anchor.territorialContext));
    } else {
      intro.appendChild(T.el('p', 'compare-anchor',
        'Date-independent formulary: ' + projected.anchor.correspondingFormulary));
    }
    fragment.appendChild(intro);

    if (projected.calendars) {
      const calendar = T.el('section', 'compare-calendar-results');
      calendar.dataset.semanticLocation = 'compare/calendar-result';
      calendar.dataset.semanticEventId = 'compare/calendar-result';
      calendar.tabIndex = -1;
      calendar.appendChild(T.el('h2', null, 'Calendar results on this date'));
      const different = projected.calendars[0].winner !== projected.calendars[1].winner ||
        projected.calendars[0].formulary !== projected.calendars[1].formulary;
      calendar.appendChild(T.el('p', 'compare-calendar-relation', different
        ? 'The two calendars appoint different results on this date.'
        : 'The two calendars appoint the same identified result on this date.'));
      const list = T.el('div', 'compare-calendar-pair');
      projected.calendars.forEach(function (row, index) {
        const side = sides[index];
        const item = T.el('div', 'compare-calendar-side');
        item.appendChild(T.el('h3', null, side.label || side.id));
        item.appendChild(T.el('p', null,
          'Calendar: ' + row.calendar + ' · Winner: ' + (row.winner || 'unresolved') +
          ' · Formulary: ' + (row.formulary || 'unresolved')));
        if (side.mass.name) item.appendChild(T.el('p', 'compare-calendar-name', side.mass.name));
        list.appendChild(item);
      });
      calendar.appendChild(list);
      fragment.appendChild(calendar);
      contents.push({
        id: 'compare/calendar-result', label: 'Calendar results', element: calendar
      });
    }

    projected.units.forEach(function (unit) {
      const section = T.el('section', 'compare-unit');
      section.dataset.semanticLocation = unit.location;
      section.dataset.semanticEventId = unit.location;
      section.dataset.readerLocusMajor = 'Compare';
      section.dataset.readerLocusUnit = unit.label;
      section.tabIndex = -1;
      section.appendChild(T.el('h2', 'compare-unit-title', unit.label));
      const pair = T.el('div', 'compare-pair');
      unit.sides.forEach(function (cell, index) {
        const side = sides[index];
        const column = T.el('div', 'compare-side');
        column.dataset.compareSide = cell.id;
        column.dataset.compareStatus = cell.status;
        column.appendChild(T.el('h3', 'compare-side-title', side.label || side.id));
        if (cell.status === 'text-held') {
          const proper = properFor(side, cell.event);
          const selected = cell.event.selected;
          column.appendChild(T.renderProper(proper, side.bible, side.fragments, {
            numbering: side.structure.numbering || null,
            orations: input.view.sides[index].result.request.languages.orations,
            translationWitness: input.view.sides[index].result.request.languages.translationWitness || null,
            heading: 'h4', cycle: selected.cycle || null
          }));
        } else {
          column.appendChild(T.el('p', 'compare-status', STATUS_NOTES[cell.status]));
        }
        if (cell.event) {
          const selected = cell.event.selected;
          const facts = [
            cell.event.editionSlotLabel && 'Edition slot: ' + cell.event.editionSlotLabel,
            selected && selected.language && 'Language: ' + selected.language,
            selected && selected.reason && 'Availability reason: ' + selected.reason,
            selected && typeof selected.rights === 'string' && 'Rights: ' + selected.rights,
            (cell.event.sourceHooks || []).length && 'Source records: ' +
              cell.event.sourceHooks.map(function (one) { return one.id; }).filter(Boolean).join('; ')
          ].filter(Boolean);
          facts.forEach(function (fact) {
            column.appendChild(T.el('p', 'compare-evidence', fact));
          });
        }
        pair.appendChild(column);
      });
      section.appendChild(pair);
      fragment.appendChild(section);
      contents.push({ id: unit.location, label: unit.label, element: section });
    });
    if (!projected.units.length) {
      fragment.appendChild(T.el('p', 'compare-status',
        'No mapped Proper slots are available for this comparison.'));
    }
    return {
      fragment: fragment, contents: contents,
      semanticIds: contents.map(function (one) { return one.id; })
    };
  }

  return Object.freeze({ project: project, render: render });
}));
