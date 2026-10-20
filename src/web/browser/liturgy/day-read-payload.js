/* Day policy for the bounded, resolved 1962 Read payload. */
'use strict';

(function (root, factory) {
  const api = factory(root);
  if (typeof module === 'object' && module && module.exports) module.exports = api;
  else root.TriptychDayReadPayload = api;
}(typeof globalThis !== 'undefined' ? globalThis : this, function (root) {
  function eligibleKey(input) {
    const parsed = input.parsed;
    const derived = input.derived;
    if (input.missal !== 'roman-1962' || input.mode !== 'read' || input.needsOrdinary ||
        !parsed || !derived || parsed.recognized.why === '1' ||
        ['mass', 'form', 'territory', 'compare', 'peer-missal'].some(function (key) {
          return parsed.present.indexOf(key) >= 0;
        }) || derived.options.length !== 1) return null;
    const branch = derived.options[0];
    const said = (branch.readable || []).filter(function (one) { return one.state === 'said'; });
    if (branch.settled !== true || !branch.winner || said.length !== 1 ||
        !said[0].key || said[0].key !== branch.winner.key ||
        branch.winner.formulary && branch.winner.formulary.kind !== 'own') return null;
    return said[0].key;
  }

  function crossMassDependency(mass) {
    if (mass.takes_from || mass.common_from || mass.common_sets ||
        (mass.forms || []).length > 1) return true;
    const rows = (mass.propers || []).concat((mass.forms || []).flatMap(function (form) {
      return form.propers || [];
    }));
    return rows.some(function (proper) {
      return proper && (proper.taken_from || proper.common_from);
    });
  }

  async function loadStructure(input) {
    const monolith = 'structure/propers/' + input.missal + '.json';
    const key = eligibleKey(input);
    const row = ((input.index && input.index.missals) || []).find(function (one) {
      return one.id === input.missal;
    });
    const reader = root.LiturgyReaderProperPayload;
    if (!key || !row || !row.read_payload || !reader) return input.load(monolith);
    try {
      const structure = await reader.load({
        load: input.load, indexRow: row, calendar: input.missal, massKey: key
      });
      const mass = structure.masses.find(function (one) { return one.key === key; });
      if (!mass || crossMassDependency(mass)) {
        throw new Error('selected Day Mass needs the complete structure');
      }
      return structure;
    } catch (_error) {
      return input.load(monolith);
    }
  }

  return Object.freeze({ eligibleKey: eligibleKey, loadStructure: loadStructure });
}));
