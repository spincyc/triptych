/* ===========================================================================
 * The encyclicals list, as a model — what a choice selects, and in what order
 * ===========================================================================
 *
 * THE ONE THING THIS FILE OWNS: which encyclicals a set of choices leaves, the
 * order they come back in, and what an address may ask for.
 *
 * It is separate from encyclicals.js for the reason catalogue-model.js is
 * separate from texts.js: the derivation is the part worth checking, and a
 * rule that only ever runs in a browser is a rule nothing can run. The tests
 * replay THIS FILE under node against the generated catalogue, so there is one
 * derivation and a check that would fail if a second were written beside it.
 *
 * Three rules in here are the record rather than presentation:
 *
 *   THE POPE ORDER IS THE PONTIFICATE ORDER. `pontificate_index` is the
 *   chronological key the index states; a pope is never sorted by name, and
 *   his encyclicals keep their date order inside him.
 *
 *   AN UNDATED ROW STAYS UNDATED. It is never given a year to sort by. It goes
 *   after every dated row, in pontificate order, whichever way the dates run.
 *
 *   AN ADDRESS THAT ASKS FOR SOMETHING THIS LIST DOES NOT HOLD IS SAID TO. A
 *   pope, a text filter or an order no option carries is returned as invalid,
 *   with the value, and the page shows nothing under it rather than quietly
 *   showing everything under a control that names neither.
 *
 * It loads both as a browser global and as a node module, because the harness
 * needs the second and the page needs the first.
 * ======================================================================== */

'use strict';

(function (root, factory) {
  const api = factory();
  if (typeof module === 'object' && module.exports) module.exports = api;
  else root.EncyclicalsModel = api;
}(typeof self !== 'undefined' ? self : this, function () {

  const ANY = '';
  const LEADING_LANGUAGES = ['la', 'en'];

  const TEXT_FILTERS = [
    { value: '', label: 'Any, or none' },
    { value: 'la', label: 'Latin held here' },
    { value: 'en', label: 'English held here' },
    { value: 'la-or-en', label: 'Latin or English held here' },
    { value: 'none', label: 'No text held here' }
  ];

  const SORTS = [
    { value: 'date', label: 'Date, oldest first' },
    { value: '-date', label: 'Date, newest first' },
    { value: 'pope', label: 'Pope, earliest first' },
    { value: '-pope', label: 'Pope, latest first' },
    { value: 'title', label: 'Title, A to Z' },
    { value: '-title', label: 'Title, Z to A' }
  ];
  const DEFAULT_SORT = 'date';

  const MONTHS = ['January', 'February', 'March', 'April', 'May', 'June', 'July',
    'August', 'September', 'October', 'November', 'December'];

  /** Lower case, accents and leading punctuation removed: what a reader types. */
  function fold(text) {
    return String(text || '')
      .normalize('NFD')
      .replace(/[̀-ͯ]/g, '')
      .toLowerCase()
      .replace(/æ/g, 'ae')
      .replace(/œ/g, 'oe');
  }

  function titleKey(row) {
    return fold(row.title).replace(/^[^a-z0-9]+/, '');
  }

  function languagesOf(row) {
    const found = [];
    for (const reader of row.readers || []) {
      if (found.indexOf(reader.language) < 0) found.push(reader.language);
    }
    return found;
  }

  function hasLanguage(row, code) {
    return (row.readers || []).some(function (reader) { return reader.language === code; });
  }

  /** The language columns, Latin and English first and always present. */
  function languageColumns(catalogue) {
    const codes = LEADING_LANGUAGES.slice();
    for (const language of catalogue.languages || []) {
      if (codes.indexOf(language.code) < 0) codes.push(language.code);
    }
    return codes.map(function (code) {
      const known = (catalogue.languages || []).find(function (l) { return l.code === code; });
      return { code: code, label: known ? known.label : (code === 'la' ? 'Latin' : 'English') };
    });
  }

  function readersIn(row, code) {
    return (row.readers || []).filter(function (reader) { return reader.language === code; });
  }

  /** "15 May 1891", or null for an undated row. Written here, not by the locale. */
  function longDate(date) {
    const match = /^([0-9]{4})-([0-9]{2})-([0-9]{2})$/.exec(String(date || ''));
    if (!match) return null;
    return Number(match[3]) + ' ' + MONTHS[Number(match[2]) - 1] + ' ' + match[1];
  }

  function haystack(row, labels) {
    const parts = [row.title, row.subject, row.description, row.pope, row.year, row.date,
      longDate(row.date), row.no_local_text_reason];
    for (const reader of row.readers || []) {
      parts.push(reader.witness, reader.extent, labels[reader.language] || reader.language);
    }
    return fold(parts.filter(function (part) { return part !== null && part !== undefined; }).join('   '));
  }

  function matches(row, state, labels) {
    if (state.pope && row.pope_id !== state.pope) return false;
    switch (state.text) {
      case 'la': if (!hasLanguage(row, 'la')) return false; break;
      case 'en': if (!hasLanguage(row, 'en')) return false; break;
      case 'la-or-en':
        if (!hasLanguage(row, 'la') && !hasLanguage(row, 'en')) return false;
        break;
      case 'none': if ((row.readers || []).length) return false; break;
      default: break;
    }
    const words = fold(state.find).split(/\s+/).filter(Boolean);
    if (!words.length) return true;
    const text = haystack(row, labels || {});
    return words.every(function (word) { return text.indexOf(word) >= 0; });
  }

  function labelsOf(catalogue) {
    const labels = {};
    for (const language of catalogue.languages || []) labels[language.code] = language.label;
    return labels;
  }

  function narrow(catalogue, state) {
    const labels = labelsOf(catalogue);
    return (catalogue.encyclicals || []).filter(function (row) {
      return matches(row, state, labels);
    });
  }

  function compareText(a, b) {
    return a < b ? -1 : a > b ? 1 : 0;
  }

  /* Each order is a key and a direction, and undated rows are outside the
     direction: they come last whether the dates run up or down, in pontificate
     order, because a missing date is not an early or a late one. */
  function comparator(sort) {
    const descending = sort.charAt(0) === '-';
    const key = descending ? sort.slice(1) : sort;
    const sign = descending ? -1 : 1;
    function byDate(a, b) {
      const undated = (a.date ? 0 : 1) - (b.date ? 0 : 1);
      if (undated) return undated;
      if (!a.date) return a.pontificate_index - b.pontificate_index;
      return sign * compareText(a.date, b.date);
    }
    return function (a, b) {
      let result = 0;
      if (key === 'pope') {
        result = sign * (a.pontificate_index - b.pontificate_index);
        if (!result) {
          const undated = (a.date ? 0 : 1) - (b.date ? 0 : 1);
          result = undated || sign * compareText(a.date || '', b.date || '');
        }
      } else if (key === 'title') {
        result = sign * compareText(titleKey(a), titleKey(b));
        if (!result) result = byDate(a, b);
      } else {
        result = byDate(a, b);
      }
      return result || compareText(titleKey(a), titleKey(b)) || compareText(a.id, b.id);
    };
  }

  function order(rows, sort) {
    return rows.slice().sort(comparator(isSort(sort) ? sort : DEFAULT_SORT));
  }

  function isSort(value) {
    return SORTS.some(function (sort) { return sort.value === value; });
  }

  function isTextFilter(value) {
    return TEXT_FILTERS.some(function (filter) { return filter.value === value; });
  }

  /** What an address asks for, and what in it this list cannot honour. */
  function stateFrom(params, catalogue) {
    const get = function (key) {
      const value = params && typeof params.get === 'function' ? params.get(key) : null;
      return value === null || value === undefined ? '' : String(value);
    };
    const state = { pope: get('pope'), text: get('text'), sort: get('sort') || DEFAULT_SORT, find: get('find') };
    const invalid = [];
    if (state.pope && !(catalogue.popes || []).some(function (pope) { return pope.id === state.pope; })) {
      invalid.push({ key: 'pope', value: state.pope });
    }
    if (!isTextFilter(state.text)) invalid.push({ key: 'text', value: state.text });
    if (!isSort(state.sort)) invalid.push({ key: 'sort', value: state.sort });
    return { state: state, invalid: invalid };
  }

  /** The address for a state: defaults are left out, so the bare page is the whole list. */
  function hashPairs(state) {
    return [
      ['pope', state.pope || ''],
      ['text', state.text || ''],
      ['sort', state.sort === DEFAULT_SORT ? '' : (state.sort || '')],
      ['find', (state.find || '').trim()]
    ];
  }

  /** The next order when a column heading is pressed: same key flips, a new key starts ascending. */
  function toggled(current, key) {
    const bare = String(current || DEFAULT_SORT).replace(/^-/, '');
    if (bare !== key) return key;
    return current.charAt(0) === '-' ? key : '-' + key;
  }

  /** What the narrowed list amounts to. Counted, never assumed. */
  function tally(rows) {
    const counted = { encyclicals: rows.length, withText: 0, without: 0, readers: 0, byLanguage: {},
      first: null, last: null, undated: 0 };
    for (const row of rows) {
      if ((row.readers || []).length) counted.withText += 1;
      else counted.without += 1;
      for (const reader of row.readers || []) {
        counted.readers += 1;
        counted.byLanguage[reader.language] = (counted.byLanguage[reader.language] || 0) + 1;
      }
      if (row.year === null || row.year === undefined || !row.date) {
        counted.undated += 1;
        continue;
      }
      if (counted.first === null || row.year < counted.first) counted.first = row.year;
      if (counted.last === null || row.year > counted.last) counted.last = row.year;
    }
    return counted;
  }

  return {
    ANY: ANY,
    DEFAULT_SORT: DEFAULT_SORT,
    TEXT_FILTERS: TEXT_FILTERS,
    SORTS: SORTS,
    fold: fold,
    languagesOf: languagesOf,
    languageColumns: languageColumns,
    readersIn: readersIn,
    longDate: longDate,
    matches: matches,
    narrow: narrow,
    order: order,
    isSort: isSort,
    stateFrom: stateFrom,
    hashPairs: hashPairs,
    toggled: toggled,
    tally: tally
  };
}));
