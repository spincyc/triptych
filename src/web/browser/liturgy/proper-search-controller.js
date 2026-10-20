/* Production Propers search binding, kept off the reader controller's hot path. */
'use strict';

(function (root) {
  function mount(input) {
    const Search = root.TriptychProperSearch;
    const form = root.document.getElementById('proper-search-form');
    if (!Search || !form) return null;
    const T = root.Triptych;
    const runtime = input.runtime;
    const bible = root.document.getElementById('reader-bible');
    const orations = root.document.getElementById('reader-orations');
    const missal = root.document.getElementById('reader-missal');
    const aliases = input.legacyKeys;

    function structure(id) {
      return [runtime.draftStructure, runtime.structure].find(function (value) {
        return value && value.calendar === id;
      }) || null;
    }

    function target(edition, row) {
      const held = structure(edition);
      const mass = held && (held.masses || []).find(function (one) {
        return one.key === row.key && one.kind === row.kind;
      });
      if (!mass) throw new Error('the search result is absent from this missal');
      const form = (mass.forms || []).some(function (one) {
        return one.id === row.form_id;
      }) ? row.form_id : null;
      const updates = {
        missal: edition, type: row.kind, mass: row.key, form: form,
        bible: bible.value, orations: orations.value,
        mode: 'read', location: null, 'ordinary-lang': null
      };
      const removals = [
        'cycle', 'alternative', 'translation-witness', 'compare', 'peer-orations', 'peer-cycle',
        aliases.cycle, aliases.alternative, aliases.translationWitness
      ];
      ((runtime.manifests && runtime.manifests.ordinaryIndex.calendars) || [])
        .forEach(function (one) { removals.push.apply(removals, one.variants || []); });
      return { updates: updates, removals: removals };
    }

    return Search.mount({
      form: form,
      input: root.document.getElementById('proper-search-input'),
      status: root.document.getElementById('proper-search-status'),
      caveat: root.document.getElementById('proper-search-caveat'),
      results: root.document.getElementById('proper-search-results'),
      edition: function () { return missal.value; },
      editionLabel: function (id) {
        const row = input.missalRow(id); return row && row.label || id;
      },
      structure: structure,
      recension: function (id) {
        const context = T.recensionContext(structure(id), null, input.editionName);
        return context && context.notice || null;
      },
      loadIndex: function (id) {
        return input.load('structure/propers/search/' + id + '.json');
      },
      href: function (id, row) {
        const selected = target(id, row);
        return input.Contract.canonicalRoute('propers', root.location.pathname) +
          root.location.search + input.internalHash(selected.updates, selected.removals);
      },
      select: function (id, row) {
        const selected = target(id, row);
        input.readerShell.close({ restoreFocus: false });
        input.navigate(selected.updates, selected.removals, {
          location: null, focus: 'title', rememberPreferences: true
        });
      }
    });
  }

  root.TriptychProperSearchController = Object.freeze({ mount: mount });
}(typeof globalThis !== 'undefined' ? globalThis : this));
