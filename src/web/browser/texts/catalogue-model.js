/* ===========================================================================
 * The catalogue, as a model — what a choice selects, and in what order
 * ===========================================================================
 *
 * THE ONE THING THIS FILE OWNS: which documents a set of choices leaves, what
 * each of them is called, and the order they come back in.
 *
 * It is separate from texts.js for the reason catena-model.js is separate from
 * catena.js: the page's own derivation is the part worth checking, and a rule
 * that only ever runs in a browser is a rule nothing here can run. `document-
 * library check` replays THIS FILE under node against the tracked catalogue, so
 * there is one derivation and a check that would fail if a second were written
 * beside it.
 *
 * Two rules in here are the record rather than presentation:
 *
 *   A WORK HAS NO SINGLE TITLE. Forty-five works are issued in both editions,
 *   and the two title them differently far more often than not — "The Debt of
 *   Nature" against "The Four Last Things: The Hour That Cannot Be Delegated".
 *   So `nameOf` is asked of an edition and never of a work, and `order` takes
 *   its key from every visible edition at once — the earliest title, the latest
 *   revision, the longest extent — so that no ordering silently prefers one
 *   edition's answer to the other's.
 *
 *   AN UNRECORDED TITLE STAYS UNRECORDED. `nameOf` returns the document's path
 *   and the generator's stated reason, flagged, and never composes a name out
 *   of the path. A composed name is indistinguishable from a real one at a
 *   glance, which is the whole failure this catalogue sits inside.
 *
 * It loads both as a browser global and as a node module, because the harness
 * needs the second and the page needs the first.
 * ======================================================================== */

'use strict';

(function (root, factory) {
  const api = factory();
  if (typeof module === 'object' && module.exports) module.exports = api;
  else root.CatalogueModel = api;
}(typeof self !== 'undefined' ? self : this, function () {

  const ANY = '';
  const READABLE = 'browser';
  const DOWNLOAD = 'pdf';

  /** A document's name, or its path and the reason there is none. */
  function nameOf(work, edition) {
    if (edition.title) return { text: edition.title, unrecorded: false, reason: null };
    return {
      text: work.leaf,
      unrecorded: true,
      reason: edition.title_absent || 'no title is recorded for this document'
    };
  }

  function pagesOf(edition) {
    return typeof edition.pages === 'number' ? edition.pages : null;
  }

  /** Everything a reader can see of one document, for the Find box to match. */
  function haystack(work, edition) {
    return [
      work.leaf,
      work.section,
      edition.title || '',
      edition.subject || '',
      edition.provider,
      (edition.models || []).join(' ')
    ].join(' ').toLowerCase();
  }

  /**
   * Does this edition survive the choices?
   *
   * Filters hide editions rather than works, so a work disappears only when
   * none of its editions survives. Asking by model otherwise leaves the other
   * edition standing beside the one that matched, and the count then says the
   * model wrote documents it did not.
   */
  function matches(work, edition, state) {
    if (state.edition && edition.provider !== state.edition) return false;
    if (state.author && (edition.models || []).indexOf(state.author) === -1) return false;
    if (state.reading === READABLE && !edition.web) return false;
    if (state.reading === DOWNLOAD && edition.web) return false;
    if (state.find && haystack(work, edition).indexOf(state.find) === -1) return false;
    return true;
  }

  function narrow(works, state) {
    const kept = [];
    for (const work of works || []) {
      if (state.section && work.section !== state.section) continue;
      const editions = (work.editions || []).filter(function (one) {
        return matches(work, one, state);
      });
      if (editions.length) kept.push({ work: work, editions: editions });
    }
    return kept;
  }

  function compare(a, b) {
    if (a < b) return -1;
    if (a > b) return 1;
    return 0;
  }

  /**
   * Order, taking each key from every visible edition of the work.
   *
   * Ties fall back to the path, which is unique, so the order is total and a
   * reload never reshuffles the list. A work with no titled edition sorts after
   * every titled one rather than to the top: an unrecorded title is a gap, and
   * a gap must not be promoted to the front of the reader's attention by an
   * accident of collation.
   */
  function order(rows, sort) {
    const keyed = rows.map(function (row) {
      const titles = row.editions
        .map(function (one) { return one.title; })
        .filter(Boolean)
        .map(function (one) { return one.toLowerCase(); })
        .sort();
      const pages = row.editions.map(pagesOf).filter(function (one) {
        return one !== null;
      });
      const revised = row.editions.map(function (one) {
        return one.revised || '';
      }).sort();
      return {
        row: row,
        // U+FFFF sorts after every assigned character, so an untitled work
        // lands at the end of a title ordering, in path order among its kind.
        title: titles.length ? titles[0] : '￿' + row.work.leaf,
        pages: pages.length ? Math.max.apply(null, pages) : -1,
        revised: revised.length ? revised[revised.length - 1] : ''
      };
    });
    keyed.sort(function (a, b) {
      const leaf = compare(a.row.work.leaf, b.row.work.leaf);
      if (sort === 'title') return compare(a.title, b.title) || leaf;
      if (sort === 'pages') return compare(b.pages, a.pages) || leaf;
      if (sort === 'revised') return compare(b.revised, a.revised) || leaf;
      return compare(a.row.work.section, b.row.work.section) || leaf;
    });
    return keyed.map(function (one) { return one.row; });
  }

  /** What the narrowed list amounts to. Counted, never assumed. */
  function tally(rows) {
    let documents = 0;
    let pages = 0;
    let unrecorded = 0;
    for (const row of rows) {
      documents += row.editions.length;
      for (const edition of row.editions) {
        pages += pagesOf(edition) || 0;
        if (!edition.title) unrecorded += 1;
      }
    }
    return { works: rows.length, documents: documents, pages: pages, unrecorded: unrecorded };
  }

  return {
    ANY: ANY,
    READABLE: READABLE,
    DOWNLOAD: DOWNLOAD,
    nameOf: nameOf,
    pagesOf: pagesOf,
    matches: matches,
    narrow: narrow,
    order: order,
    tally: tally
  };
}));
