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

  // Hints only warm browser responses. The ordinary loaders remain responsible
  // for parsing, publication admission, selection validation and split fallback.
  function startupHints(input) {
    if (!object(input) || typeof input.rawHash !== 'string' ||
        typeof input.dataPath !== 'function' ||
        !['day', 'propers'].includes(input.entrance)) return [];
    const params = new URLSearchParams(input.rawHash.replace(/^#/, ''));
    const keys = Array.from(params.keys());
    const allowed = input.entrance === 'day'
      ? ['date', 'missal', 'bible', 'orations', 'mode', 'ordinary', 'location', 'translation-witness']
      : ['missal', 'type', 'mass', 'form', 'bible', 'orations', 'mode', 'cycle', 'alternative', 'translation-witness', 'location'];
    if (keys.some(function (key) { return !allowed.includes(key); }) ||
        new Set(keys).size !== keys.length || params.get('missal') !== 'roman-1962' ||
        (params.has('mode') && params.get('mode') !== 'read') ||
        (params.has('ordinary') && params.get('ordinary') !== '0')) return [];
    const paths = ['bibles.json', 'structure/propers/index.json', 'structure/ordinary/index.json',
      'structure/propers/catalog/roman-1962.json'];
    if (input.entrance === 'day') {
      const date = params.get('date') || '';
      if (!/^\d{4}-\d{2}-\d{2}$/.test(date)) return [];
      const stamp = Date.parse(date + 'T00:00:00Z');
      if (Number.isNaN(stamp) || new Date(stamp).toISOString().slice(0, 10) !== date) return [];
      paths.push('structure/rubrics/index.json', 'structure/rubrics/roman-1962.json',
        'structure/calendar/roman-1962/' + date.slice(0, 4) + '.json');
    } else {
      const mass = params.get('mass') || '';
      if (!['seasonal', 'christological', 'marian', 'sanctoral'].includes(params.get('type')) ||
          mass.length > 128 || !ID.test(mass)) return [];
      paths.push('structure/propers/mass/roman-1962/' + mass + '.json');
    }
    try {
      const urls = paths.map(function (path) { return new URL(input.dataPath(path), input.baseURI); });
      if (urls.some(function (url) {
        return !['http:', 'https:'].includes(url.protocol) ||
          url.origin !== input.origin || url.username || url.password;
      })) return [];
      return urls.map(function (url) { return url.href; });
    } catch (_error) { return []; }
  }

  // Explicit Latin avoids reimplementing effective language or witness choices.
  function framedRequest(parsed) {
    return object(parsed) && object(parsed.recognized) && parsed.recognized.orations === 'la' &&
      !(parsed.duplicates || []).length && !(parsed.unknown || []).length;
  }

  // A framed fast path needs one complete Mass and no second Mass's bodies.
  function selfContainedMass(mass) {
    if (!object(mass) || mass.takes_from || mass.common_from || mass.common_sets ||
        (mass.forms || []).length > 1) return false;
    const rows = (mass.propers || []).concat((mass.forms || []).flatMap(function (form) {
      return form.propers || [];
    }));
    return !rows.some(function (proper) {
      return proper && (proper.taken_from || proper.common_from);
    });
  }

  function framedMass(mass, parsed) {
    if (!selfContainedMass(mass) || !framedRequest(parsed)) return false;
    const forms = mass.forms || [];
    if ([mass].concat(forms).some(function (owner) {
      return owner.ordinary_frame && owner.ordinary_frame.applicability !== 'full';
    })) return false;
    return (mass.propers || []).every(function (proper) {
      return proper && proper.name !== 'Placeholder' && !proper.ordinary_disposition &&
        !Object.keys(proper.cycles || {}).length &&
        !Object.keys(proper.weekday_cycles || {}).length;
    });
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
    startupHints: startupHints, selfContainedMass: selfContainedMass, framedRequest: framedRequest, framedMass: framedMass,
    CATALOG_SCHEMA: CATALOG_SCHEMA, MASS_SCHEMA: MASS_SCHEMA });
}));

(function (root) {
  const doc = root.document;
  const browser = root.Triptych;
  if (!doc || !doc.head || typeof doc.querySelector !== 'function' || !browser ||
      typeof browser.dataPath !== 'function' || !root.LiturgyReaderProperPayload) return;
  const shell = doc.querySelector('[data-reader-shell][data-entrance]');
  if (!shell) return;
  const urls = root.LiturgyReaderProperPayload.startupHints({
    entrance: shell.getAttribute('data-entrance'), rawHash: root.location.hash,
    dataPath: browser.dataPath, baseURI: doc.baseURI, origin: root.location.origin
  });
  urls.forEach(function (url) {
    try {
      const present = Array.from(doc.head.querySelectorAll('link[rel="preload"][as="fetch"]'))
        .some(function (link) { return link.href === url && link.crossOrigin === 'anonymous'; });
      if (present) return;
      const link = doc.createElement('link');
      link.rel = 'preload';
      link.as = 'fetch';
      link.crossOrigin = 'anonymous';
      link.href = url;
      doc.head.append(link);
    } catch (_error) { /* An optional hint never replaces the normal load path. */ }
  });
}(typeof globalThis !== 'undefined' ? globalThis : this));
