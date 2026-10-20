/* Narrow 1962 Propers reading fast path; every split failure uses the full source projection. */
'use strict';

(function (root, factory) {
  const api = factory(root);
  if (typeof module === 'object' && module && module.exports) module.exports = api;
  else root.TriptychPropersReadPayload = api;
}(typeof globalThis !== 'undefined' ? globalThis : this, function (root) {
  function eligible(parsed, calendar) {
    const present = parsed.present || [];
    const framed = parsed.recognized.mode === 'missal';
    return calendar === 'roman-1962' &&
      (!present.includes('mode') || parsed.recognized.mode === 'read' || framed) &&
      present.includes('type') && present.includes('mass') &&
      (framed || !present.includes('ordinary-lang')) &&
      (!framed || root.LiturgyReaderProperPayload?.framedRequest?.(parsed)) &&
      !(parsed.variantKeys || []).some(function (key) { return present.includes(key); }) &&
      !(parsed.duplicates || []).length;
  }

  function resolvedForm(parsed, mass) {
    const forms = mass.forms || [];
    const explicit = (parsed.present || []).includes('form');
    if (!Array.isArray(forms)) return false;
    if (!explicit) return forms.length <= 1;
    return forms.some(function (form) { return form.id === parsed.recognized.form; });
  }

  async function load(input) {
    const monolith = function () { return input.load(input.monolith); };
    const indexRow = (input.index.missals || []).find(function (row) {
      return row.id === input.calendar;
    });
    if (!eligible(input.parsed, input.calendar) || !indexRow || !indexRow.read_payload ||
        !root.LiturgyReaderProperPayload) return monolith();
    try {
      const structure = await root.LiturgyReaderProperPayload.load({
        load: input.load, indexRow: indexRow, calendar: input.calendar,
        massKey: input.parsed.recognized.mass
      });
      const mass = (structure.masses || []).find(function (row) {
        return row.key === input.parsed.recognized.mass;
      });
      if (!mass || mass.kind !== input.parsed.recognized.type ||
          !resolvedForm(input.parsed, mass) ||
          (input.parsed.recognized.mode === 'missal' &&
            !root.LiturgyReaderProperPayload.framedMass(mass, input.parsed)) ||
          (mass.takes_from && mass.takes_from.common_sets != null)) {
        return monolith();
      }
      return structure;
    } catch (_error) {
      return monolith();
    }
  }

  return Object.freeze({ eligible: eligible, resolvedForm: resolvedForm, load: load });
}));
