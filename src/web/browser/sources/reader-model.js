/* ===========================================================================
 * The source corpus, as a model — what a choice selects, and in what order
 * ===========================================================================
 *
 * THE ONE THING THIS FILE OWNS: which editions a set of choices leaves, what
 * each record is called, and the order they come back in.
 *
 * It is separate from sources.js for the reason catalogue-model.js is separate
 * from texts.js: the page's own derivation is the part worth checking, and a
 * rule that only ever runs in a browser is a rule nothing here can run.
 * `source-reader check` replays THIS FILE under node against the tracked spine,
 * so there is one derivation and a check that would fail if a second were
 * written beside it.
 *
 * Three rules in here are the record rather than presentation:
 *
 *   FILTERS HIDE EDITIONS, NOT WORKS. A work disappears only when none of its
 *   editions survives. The same work held in Greek, in Migne's Latin and in a
 *   public-domain English is three editions and not one thing with three texts,
 *   so asking for Greek must leave the Greek standing alone — not the work with
 *   all three still under it, which would report Greek the corpus has not got.
 *
 *   A WORK IS NOT AN EDITION AND NEITHER IS A PASSAGE. `nameOf` is asked of a
 *   work for its title and of an edition for its date and language, and the two
 *   are never merged into one label. The counts follow the same split: `works`
 *   counts works, `editions` counts editions, and `readable` counts passages.
 *
 *   AN UNRECORDED FIELD STAYS UNRECORDED. Nothing here composes a title out of
 *   an id or a date out of a filename. A composed name is indistinguishable
 *   from a recorded one at a glance, and this corpus's whole value is that its
 *   identities were established rather than guessed.
 *
 * It loads both as a browser global and as a node module, because the harness
 * needs the second and the page needs the first.
 * ======================================================================== */

'use strict';

(function (root, factory) {
  const api = factory();
  if (typeof module === 'object' && module.exports) module.exports = api;
  else root.ReaderModel = api;
}(typeof self !== 'undefined' ? self : this, function () {

  const ANY = '';

  /** Decode the compact discovery metadata; edition apparatus stays lazy. */
  function catalogue(input) {
    if (input.schema !== 'triptych-source-catalogue/v2') return input;
    const labels = input.labels;
    function label(at) {
      if (at === null) return null;
      if (!Number.isInteger(at) || at < 0 || at >= labels.length) throw new Error('Invalid Sources label');
      return labels[at];
    }
    if (!Array.isArray(labels) || !Array.isArray(input.rows)) throw new Error('Invalid Sources catalogue');
    const works = input.rows.map(function (row) {
      if (!Array.isArray(row) || row.length !== 7 || !Array.isArray(row[6])) throw new Error('Invalid Sources work');
      return { id: row[0], title: row[1], author: label(row[2]), category: label(row[3]),
        alternate_titles: row[4], directory: row[5], editions: row[6].map(function (ed) {
          if (!Array.isArray(ed) || ed.length !== 9) throw new Error('Invalid Sources edition');
          return { id: ed[0], title: ed[1] === 0 ? row[1] : ed[1], language: label(ed[2]),
            date: label(ed[3]), year: ed[4], file: label(ed[5]), passages: ed[6], readable: ed[7],
            rights: ed[8].map(label) };
        }) };
    });
    const result = Object.assign({}, input, { works: works });
    delete result.rows;
    delete result.labels;
    return result;
  }

  /** A complete finder remains available without loading it before the first page.
   * Calls share in-flight shard requests; a failed shard remains retryable.
   */
  function discovery(input, load) {
    if (input.schema !== 'triptych-source-discovery/v3') {
      if (input.schema && !['triptych-source-reader/v1', 'triptych-source-catalogue/v2'].includes(input.schema)) {
        throw new Error('Unknown Sources discovery schema');
      }
      const file = catalogue(input);
      if (!Array.isArray(file.works)) throw new Error('Invalid Sources catalogue');
      return { file: file, ensure: async function () { return file; },
        all: async function () { return file; }, total: (file.works || []).length };
    }
    if (!Array.isArray(input.shards) || !input.counted ||
        !Number.isInteger(input.counted.works) || input.counted.works < 0 ||
        input.shards.some(function (shard, at) {
          return !shard || shard.path !== 'structure/sources/catalogue/' + String(at).padStart(4, '0') + '.json' ||
            !Number.isInteger(shard.works) || shard.works < 1 || shard.works > 128;
        }) || input.shards.reduce(function (sum, shard) { return sum + shard.works; }, 0) !== input.counted.works) {
      throw new Error('Invalid Sources discovery');
    }
    const file = Object.assign({}, input, { works: [] });
    let loaded = 0;
    let pending = null;
    async function ensure(count) {
      const wanted = Math.min(count, input.counted.works);
      while (file.works.length < wanted) {
        if (!pending) {
          const shard = input.shards[loaded];
          if (!shard) throw new Error('Sources discovery is incomplete');
          pending = load(shard.path).then(function (body) {
            const works = catalogue(body).works;
            if (!Array.isArray(works) || works.length !== shard.works) throw new Error('Sources shard count differs');
            file.works.push.apply(file.works, works);
            loaded += 1;
          }).finally(function () { pending = null; });
        }
        await pending;
      }
      return file;
    }
    return { file: file, ensure: ensure, all: function () { return ensure(input.counted.works); },
      total: input.counted.works };
  }

  function unfiltered(state) {
    return !(state.author || state.category || state.language || state.period || state.rights ||
      state.readable || state.find || (state.sort && state.sort !== 'author'));
  }

  // Records are immutable discovery data. Normalise each searched identity once,
  // and let the old catalogue be collected when a new one replaces it.
  const searchText = new WeakMap();
  const emptyEdition = {};

  /** Every control at rest. One object, so a caller cannot forget a key. */
  function blank() {
    return {
      author: ANY,
      category: ANY,
      language: ANY,
      period: ANY,
      rights: ANY,
      readable: false,
      find: ANY,
      sort: 'author'
    };
  }

  /** The century an edition falls in, as the spine writes it, or null. */
  function periodOf(edition) {
    if (typeof edition.year !== 'number') return null;
    return String(Math.floor(edition.year / 100) * 100);
  }

  /**
   * Everything a reader can see of one record, for the Find box to match.
   *
   * The alternate titles are in here and they matter more than the rest.
   * `guidance/sources.md` is blunt about it: a work is rarely catalogued once,
   * and a search that knows only the canonical title produces a FALSE ABSENCE —
   * the work is held under a name nobody searched, and the reader concludes the
   * corpus does not have it. So every alias the record carries is searchable.
   */
  function haystack(work, edition) {
    let held = searchText.get(work);
    if (!held) { held = new WeakMap(); searchText.set(work, held); }
    if (held.has(edition)) return held.get(edition);
    const result = [
      work.title || '',
      work.author || '',
      work.category || '',
      (work.alternate_titles || []).join(' '),
      work.id,
      edition.id || '',
      edition.title || '',
      edition.date || '',
      edition.language || ''
    ].join(' ').toLowerCase();
    held.set(edition, result);
    return result;
  }

  /** Does this edition survive the choices? */
  function matches(work, edition, state) {
    if (state.language && edition.language !== state.language) return false;
    if (state.period && periodOf(edition) !== state.period) return false;
    if (state.rights && (edition.rights || []).indexOf(state.rights) === -1) return false;
    if (state.readable && !(edition.readable > 0)) return false;
    if (state.find && haystack(work, edition).indexOf(state.find) === -1) return false;
    return true;
  }

  /**
   * Is any control asking a question only an edition can answer?
   *
   * It matters because eight works in this corpus have no edition record at
   * all — Basil's Hexaemeron and Gregory's De hominis opificio among them,
   * whose translations are witnessed inside an anthology owned by someone else.
   * Their identity is established and nothing hangs beneath it, which is a real
   * and recorded state.
   *
   * So a work with no editions survives the work-level controls and is dropped
   * only by an edition-level one. Dropping it always would be a FALSE ABSENCE
   * for exactly the works Catena Omnia publishes; keeping it always would have
   * a search for Greek editions return a work with no edition in any language.
   */
  function asksAboutEditions(state) {
    return Boolean(state.language || state.period || state.rights || state.readable);
  }

  function narrow(works, state) {
    const kept = [];
    for (const work of works || []) {
      if (state.author && work.author !== state.author) continue;
      if (state.category && work.category !== state.category) continue;
      const editions = (work.editions || []).filter(function (one) {
        return matches(work, one, state);
      });
      if (editions.length) {
        kept.push({ work: work, editions: editions });
        continue;
      }
      if (!(work.editions || []).length && !asksAboutEditions(state) &&
          (!state.find || haystack(work, emptyEdition).indexOf(state.find) !== -1)) {
        kept.push({ work: work, editions: [] });
      }
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
   * Ties fall back to the work id, which is unique, so the order is total and a
   * reload never reshuffles the list. Two gaps are deliberately sent to the
   * back rather than the front: a work with no recorded author, and an edition
   * with no recorded date. An absent field is a gap in the record, and a gap
   * must not be promoted to the head of a reader's attention by an accident of
   * collation.
   */
  function order(rows, sort) {
    const keyed = rows.map(function (row) {
      const years = row.editions
        .map(function (one) { return one.year; })
        .filter(function (one) { return typeof one === 'number'; });
      return {
        row: row,
        // U+FFFF sorts after every assigned character.
        author: row.work.author ? row.work.author.toLowerCase() : '￿',
        title: row.work.title ? row.work.title.toLowerCase() : '￿' + row.work.id,
        year: years.length ? Math.min.apply(null, years) : Infinity,
        readable: row.editions.reduce(function (sum, one) {
          return sum + (one.readable || 0);
        }, 0)
      };
    });
    keyed.sort(function (a, b) {
      const id = compare(a.row.work.id, b.row.work.id);
      if (sort === 'title') return compare(a.title, b.title) || id;
      if (sort === 'date') return compare(a.year, b.year) || id;
      if (sort === 'readable') return compare(b.readable, a.readable) || id;
      return compare(a.author, b.author) || compare(a.title, b.title) || id;
    });
    return keyed.map(function (one) { return one.row; });
  }

  /** What the narrowed list amounts to. Counted, never assumed. */
  function tally(rows) {
    let editions = 0;
    let passages = 0;
    let readable = 0;
    for (const row of rows) {
      editions += row.editions.length;
      for (const edition of row.editions) {
        passages += edition.passages || 0;
        readable += edition.readable || 0;
      }
    }
    return {
      works: rows.length,
      editions: editions,
      passages: passages,
      readable: readable
    };
  }

  /**
   * Where an edition's own file is: the work's directory and the edition's name.
   *
   * Joined here and composed nowhere. The generator writes both halves down —
   * the directory on the work, the file on the edition — precisely so that the
   * page follows what was written instead of knowing the layout by heart.
   */
  function editionPath(spine, work, edition) {
    const directory = work.directory || '';
    if (!directory || !edition.file) return null;
    return (spine.root || '') + directory + edition.file;
  }

  /**
   * The one edition a work should open on.
   *
   * The one that can actually be read, if any can; otherwise the earliest. A
   * reader who opens a work and lands on the edition whose text is withheld,
   * while a readable one sits beneath it, has been told the wrong thing about
   * the corpus.
   */
  function openingEdition(editions) {
    const readable = (editions || []).filter(function (one) {
      return one.readable > 0;
    });
    return (readable.length ? readable : editions || [])[0] || null;
  }

  /** An explicit source edition joins exactly one declared full Bible offer.
   * Rights and product completeness are established by the producer/publisher;
   * the reader accepts their typed route, with no default or label matching.
   */
  function biblePrintForEdition(bibles, editionId) {
    if (!Array.isArray(bibles) || typeof editionId !== 'string' || !editionId) return null;
    const matches = bibles.filter(function (one) {
      return one && one.source_id === editionId;
    });
    if (matches.length !== 1) return null;
    const bible = matches[0];
    const offer = bible.print;
    if (typeof bible.id !== 'string' || !/^[a-z0-9]+(?:-[a-z0-9]+)*$/.test(bible.id) ||
        typeof bible.label !== 'string' || !bible.label.trim() || !offer ||
        offer.id !== 'bible:' + bible.id || offer.kind !== 'bible' ||
        offer.format !== 'browser' ||
        offer.href !== 'print/bibles/' + bible.id + '.html?print=1') return null;
    return { id: bible.id, label: bible.label, href: offer.href };
  }

  return {
    ANY: ANY,
    catalogue: catalogue,
    discovery: discovery,
    unfiltered: unfiltered,
    blank: blank,
    periodOf: periodOf,
    haystack: haystack,
    matches: matches,
    narrow: narrow,
    order: order,
    tally: tally,
    editionPath: editionPath,
    openingEdition: openingEdition,
    biblePrintForEdition: biblePrintForEdition
  };
}));
