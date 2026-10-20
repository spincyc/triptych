/* Validated catalog + one-Mass Proper payload for the resolved Read path. */
'use strict';

(function (root, factory) {
  const api = factory();
  if (typeof module === 'object' && module && module.exports) module.exports = api;
  else root.LiturgyReaderProperPayload = api;
}(typeof globalThis !== 'undefined' ? globalThis : this, function () {
  const CATALOG_SCHEMA = 'triptych-propers-read-catalog/v1';
  const MASS_SCHEMA = 'triptych-propers-read-mass/v1';
  const ID = /^[a-z0-9]+(?:-[a-z0-9]+)*$/;
  const SHA = /^[a-f0-9]{64}$/;
  const DESCRIPTOR_KEYS = ['key', 'name', 'kind', 'season', 'date', 'coverage', 'forms'];

  function object(value) {
    return value !== null && typeof value === 'object' && !Array.isArray(value);
  }
  function fail(message) { throw new Error('Proper read payload: ' + message); }
  function same(left, right) {
    if (Array.isArray(left) || Array.isArray(right)) {
      return Array.isArray(left) && Array.isArray(right) &&
        left.length === right.length && left.every(function (one, index) {
          return same(one, right[index]);
        });
    }
    if (object(left) || object(right)) {
      if (!object(left) || !object(right)) return false;
      const keys = Object.keys(left).sort();
      const other = Object.keys(right).sort();
      return same(keys, other) && keys.every(function (key) {
        return same(left[key], right[key]);
      });
    }
    return left === right;
  }
  function descriptorOf(mass) {
    return {
      key: mass.key, name: mass.name, kind: mass.kind,
      season: mass.season ?? null, date: mass.date ?? null,
      coverage: mass.coverage,
      forms: (mass.forms || []).map(function (form) {
        return { id: form.id, name: form.name, ordinal: form.ordinal };
      })
    };
  }

  function warm(load, path) {
    try {
      const pending = load(path);
      // A speculative failure is handled by the ordinary validated load path.
      pending.catch(function () {});
      return pending;
    } catch (_error) { return null; }
  }

  function warmDay(input) {
    const parsed = input.parsed;
    const present = parsed && parsed.present || [];
    const rows = input.index && input.index.missals;
    const row = (Array.isArray(rows) ? rows : []).find(function (one) {
      return one.id === 'roman-1962';
    });
    if (input.missal !== 'roman-1962' || input.mode !== 'read' ||
        input.needsOrdinary || !row || !row.read_payload ||
        row.read_payload.catalog !== 'structure/propers/catalog/roman-1962.json' ||
        !parsed || !parsed.recognized || (parsed.duplicates || []).length ||
        parsed.recognized.why === '1' ||
        ['mass', 'form', 'territory', 'compare', 'peer-missal'].some(function (key) {
          return present.includes(key);
        })) return null;
    return warm(input.load, row.read_payload.catalog);
  }

  function warmPropers(load, rawHash) {
    const params = new URLSearchParams(String(rawHash || '').replace(/^#/, ''));
    const keys = Array.from(params.keys());
    const allowed = new Set([
      'missal', 'type', 'mass', 'form', 'bible', 'orations', 'mode',
      'cycle', 'alternative', 'translation-witness', 'location'
    ]);
    if (params.get('missal') !== 'roman-1962' ||
        !['seasonal', 'christological', 'marian', 'sanctoral'].includes(params.get('type')) ||
        !ID.test(params.get('mass') || '') ||
        (params.has('mode') && params.get('mode') !== 'read') ||
        keys.some(function (key) { return !allowed.has(key); }) ||
        new Set(keys).size !== keys.length) return null;
    return warm(load, 'structure/propers/catalog/roman-1962.json');
  }

  async function load(input) {
    if (!object(input) || typeof input.load !== 'function' ||
        !ID.test(input.calendar || '') || !ID.test(input.massKey || '')) {
      fail('calendar, Mass key, and load callback are required');
    }
    const calendar = input.calendar;
    const key = input.massKey;
    const row = input.indexRow;
    const paths = row && row.read_payload;
    if (!object(row) || row.id !== calendar || !object(paths) ||
        paths.catalog !== 'structure/propers/catalog/' + calendar + '.json' ||
        paths.mass_prefix !== 'structure/propers/mass/' + calendar + '/') {
      fail('the index row has no matching bounded payload paths');
    }
    const [catalog, envelope] = await Promise.all([
      input.load(paths.catalog), input.load(paths.mass_prefix + key + '.json')
    ]);
    if (!object(catalog) || catalog.schema !== CATALOG_SCHEMA ||
        catalog.calendar !== calendar || !SHA.test(catalog.generation || '') ||
        !object(catalog.structure) || catalog.structure.calendar !== calendar ||
        Object.prototype.hasOwnProperty.call(catalog.structure, 'masses') ||
        !Array.isArray(catalog.masses) || !catalog.masses.length) {
      fail('catalog schema, calendar, generation, or structure is invalid');
    }
    const seen = new Set();
    catalog.masses.forEach(function (descriptor) {
      if (!object(descriptor) || !same(Object.keys(descriptor).sort(), DESCRIPTOR_KEYS.slice().sort()) ||
          !ID.test(descriptor.key || '') || seen.has(descriptor.key) ||
          typeof descriptor.name !== 'string' || !descriptor.name ||
          typeof descriptor.kind !== 'string' || !descriptor.kind ||
          !object(descriptor.coverage) || !Array.isArray(descriptor.forms) ||
          descriptor.forms.some(function (form) {
            return !object(form) || !same(Object.keys(form).sort(), ['id', 'name', 'ordinal']) ||
              !ID.test(form.id || '') || typeof form.name !== 'string' || !form.name ||
              !Number.isInteger(form.ordinal) || form.ordinal < 1;
          })) {
        fail('catalog Mass descriptor is malformed or duplicated');
      }
      seen.add(descriptor.key);
    });
    if (!seen.has(key)) fail('requested Mass is absent from the catalog');
    if (!object(envelope) || envelope.schema !== MASS_SCHEMA ||
        envelope.calendar !== calendar || envelope.generation !== catalog.generation ||
        !object(envelope.mass) || envelope.mass.key !== key ||
        !same(catalog.masses.find(function (one) { return one.key === key; }),
          descriptorOf(envelope.mass))) {
      fail('Mass envelope disagrees with the selected catalog descriptor');
    }
    return Object.assign({}, catalog.structure, {
      masses: catalog.masses.map(function (descriptor) {
        return descriptor.key === key ? envelope.mass : descriptor;
      })
    });
  }

  return Object.freeze({ load: load, warmDay: warmDay, warmPropers: warmPropers,
    CATALOG_SCHEMA: CATALOG_SCHEMA, MASS_SCHEMA: MASS_SCHEMA });
}));
