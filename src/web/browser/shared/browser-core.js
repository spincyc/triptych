/* ===========================================================================
 * Triptych browser — the machinery both reading pages share
 * ===========================================================================
 *
 * THERE ARE TWO PAGES, AND THIS FILE IS NEITHER OF THEM.
 *
 *   liturgy/    Missal -> Type -> Mass -> Translation.   The propers of a Mass.
 *   scripture/  Tier -> Reading -> Translation.          An abridged reading plan.
 *
 * They are separate pages because they are separate tasks. What they share is
 * not the interface but the machinery, and the machinery lives here, once:
 *
 *   the chapter-fragment cache — one promise per bible/book/chapter, fetched
 *     once and re-used by every citation that lands in it, on either page
 *   verse-range slicing out of a fetched chapter
 *   the four failure renderings, each of which states its reason rather than
 *     rendering nothing:
 *       1. a citation the structure could not resolve
 *       2. loci absent for the numbering the chosen edition uses
 *       3. a chapter fragment this edition does not carry
 *       4. verses missing from a fragment that is present
 *   translation handling, including the `lang` each edition's text carries
 *   URL state, the render token that discards an overtaken selection, the data
 *     root, the fetch layer, and the select-filling that keeps order
 *
 * DUPLICATING ANY OF THAT INTO THE TWO PAGES IS HOW THEY WOULD DRIFT. A fix to
 * a failure rendering would land on one page and not the other; the cache would
 * be warm in one tab and cold in the other, and the same chapter would be
 * fetched twice by the same reader. Page-specific vocabulary — missals, kinds,
 * Masses, tiers, periods — belongs in the page. Anything the two pages must
 * agree about belongs here.
 *
 * WHY NOTHING IS PRE-RENDERED — READ THIS BEFORE "OPTIMISING"
 *
 * The obvious-looking improvement is to bake every Mass-and-translation pair
 * into a static page at build time. That is combinatorial, and it gets worse
 * with exactly the thing this project intends to do more of:
 *
 *   masses x translations = pages
 *
 * Two missals already carry some 600 Masses between them; the corpus tracks
 * more editions than two and means to add more. Every new translation would
 * multiply both calendars afresh, and the same chapter of the Psalter would be
 * copied into every page that cites it, in every edition, forever.
 *
 * Fragments make the cost additive instead:
 *
 *   masses + readings + (translations x chapters cited) = files
 *
 * So: do not turn this into static pages, do not inline verse text into the
 * structure files, and do not build a per-pair cache on disk. The join belongs
 * here, at read time.
 *
 * DEPLOYMENT
 *
 *   <site>/browse/      bibles.json, structure/, <edition>/chapters/...  (data)
 *   <site>/shared/      this file and browser-core.css
 *   <site>/liturgy/     the propers page
 *   <site>/scripture/   the reading-plan page
 *
 * The data lives once and both pages reach it at `../browse`, which is why the
 * default data root is a sibling directory rather than the page's own.
 *
 *   ?data=<root>   where the data lives (default: ../browse)
 *   ?data=fixture  the sample corpus in ../fixture, for demonstration
 *
 * No frameworks, no build step, no external requests of any kind. All output is
 * built with createElement/textContent, never innerHTML, so Latin orthography
 * and any other non-ASCII text passes through untouched.
 * ======================================================================== */

window.Triptych = (function () {
  'use strict';

  /* ------------------------------------------------------------------------
   * Where the data is
   * --------------------------------------------------------------------- */

  const PARAMS = new URLSearchParams(window.location.search);

  // A page sits in its own directory and the data sits in a sibling one, so
  // that one copy of the corpus serves both pages.
  const DEFAULT_DATA_ROOT = '../browse';
  const FIXTURE_DATA_ROOT = '../fixture';

  function resolveDataRoot(raw) {
    if (!raw) return DEFAULT_DATA_ROOT;
    if (raw === 'fixture') return FIXTURE_DATA_ROOT;
    return String(raw).replace(/\/+$/, '') || '.';
  }

  const DATA_ROOT = resolveDataRoot(PARAMS.get('data'));

  function dataPath(path) {
    return DATA_ROOT + '/' + path;
  }

  /* ------------------------------------------------------------------------
   * Fetch layer
   *
   * A 404 raises NotFound, which callers handle per file — a missing chapter is
   * a reportable gap, not a broken page. A transport failure at start-up — a
   * page opened straight off disk, where fetch is refused — switches to the
   * inline fallback once and says so. After start-up a transport failure is
   * reported against the citation that hit it, rather than silently replacing
   * the reader's corpus with a demonstration one.
   * --------------------------------------------------------------------- */

  class NotFound extends Error {}

  const inlineFiles = Object.create(null);
  let inlineMode = false;
  let bootstrapping = true;

  /** Each page adds its own structure file to the fallback; the shared parts
   *  (the manifest and a few chapters) are registered below. */
  function addInlineFiles(files) {
    for (const path of Object.keys(files)) inlineFiles[path] = files[path];
  }

  function hasInline(path) {
    return Object.prototype.hasOwnProperty.call(inlineFiles, path);
  }

  function fromInline(path) {
    if (!hasInline(path)) {
      throw new NotFound(path + ' is not in the built-in fallback');
    }
    return handedOn(JSON.parse(JSON.stringify(inlineFiles[path])), path);
  }

  /* A PARSED VALUE IS HANDED ON ONLY FROM A REALM THAT CANNOT TAKE IT FOR A
   * PROMISE. `loadJSON` is async, so what it returns resolves a promise, and
   * resolving a promise with an object asks the object for `then`. Nothing
   * JSON can encode is callable, so a parsed document can be taken for a
   * promise only through a `then` standing on one of the two prototypes
   * `JSON.parse` builds on — and one that answers `undefined` once and a
   * resolver the next time substitutes the whole document before any page
   * sees it (the Catena E1 hardening backlog: V16 finalized "HOSTILE
   * SECOND-THEN BODY" in place of the fragment's own words). So the body is
   * read as text — a string is never a thenable, where `response.json()`'s own
   * resolution was already one such ask — parsed here, and refused while either
   * prototype carries a `then`. The prototypes are asked by descriptor, so a
   * getter standing there is seen without being run, and the check and the
   * return have no `await` between them, so nothing can be installed in the
   * gap. Every page that loads through this file is covered: indexes,
   * spines, paragraphs, manifests and text alike. */
  function thenableRealm() {
    return Object.getOwnPropertyDescriptor(Object.prototype, 'then') !== undefined
      || Object.getOwnPropertyDescriptor(Array.prototype, 'then') !== undefined;
  }

  function handedOn(value, where) {
    if (thenableRealm()) {
      throw new Error(where + ' — refused: a "then" on a shared prototype could ' +
        'have replaced the document with another');
    }
    return value;
  }

  let inlineNotice =
    'No data root could be reached, so this page is showing its small built-in ' +
    'fallback rather than the corpus. Serve the pages over HTTP with the data ' +
    'at "' + DATA_ROOT + '", or try ?data=fixture.';

  function setInlineNotice(text) {
    inlineNotice = text;
  }

  function enterInlineMode() {
    if (inlineMode) return;
    inlineMode = true;
    showBanner(inlineNotice);
  }

  function doneBootstrapping() {
    bootstrapping = false;
  }

  async function loadJSON(path) {
    if (inlineMode) return fromInline(path);

    const url = dataPath(path);
    let response;
    try {
      response = await fetch(url, { credentials: 'same-origin' });
    } catch (error) {
      if (!bootstrapping) {
        throw new Error(url + ' could not be reached: ' + (error.message || error));
      }
      enterInlineMode();
      return fromInline(path);
    }

    if (response.status === 404) throw new NotFound(url + ' was not found (404)');
    if (!response.ok) throw new Error(url + ' — HTTP ' + response.status);

    let value;
    try {
      value = JSON.parse(await response.text());
    } catch (error) {
      throw new Error(url + ' — the response was not valid JSON');
    }
    return handedOn(value, url);
  }

  /**
   * Is a file there, without downloading it?
   *
   * The propers page asks this of each candidate missal, and a missal structure
   * runs to hundreds of kilobytes: discovering which ones exist must not fetch
   * any of them. A server that refuses HEAD, or answers something other than
   * 200 or 404, is given the benefit of the doubt — a missal wrongly offered
   * explains itself when it is chosen, whereas one wrongly withheld is invisible.
   */
  async function exists(path) {
    if (inlineMode) return hasInline(path);
    try {
      const response = await fetch(dataPath(path), {
        method: 'HEAD',
        credentials: 'same-origin'
      });
      return response.status !== 404;
    } catch (error) {
      if (bootstrapping) {
        enterInlineMode();
        return hasInline(path);
      }
      return true;
    }
  }

  /* ------------------------------------------------------------------------
   * Chapter cache — the point of the whole design. One promise per
   * bible/book/chapter, resolved once, re-used by every citation that lands in
   * it, on either page. The promise never rejects; it resolves to a result the
   * renderer can display either way.
   * --------------------------------------------------------------------- */

  const chapterCache = new Map();

  function loadChapter(bibleId, book, chapter) {
    const key = bibleId + '|' + book + '|' + chapter;
    const held = chapterCache.get(key);
    if (held) return held;

    const path = bibleId + '/chapters/' + book + '/' + chapter + '.json';
    const pending = loadJSON(path).then(
      (fragment) => {
        const verses = fragment && fragment.verses;
        if (!verses || typeof verses !== 'object') {
          return { ok: false, problem: path + ' carries no verses' };
        }
        return { ok: true, verses: verses };
      },
      (error) => {
        if (error instanceof NotFound) {
          return {
            ok: false,
            problem:
              'This edition has no fragment for ' + book + ' ' + chapter +
              ' (' + path + ').'
          };
        }
        return { ok: false, problem: String(error.message || error) };
      }
    );

    chapterCache.set(key, pending);
    return pending;
  }

  function cachedChapterCount() {
    return chapterCache.size;
  }

  /* ------------------------------------------------------------------------
   * Small DOM helpers — everything goes through textContent.
   * --------------------------------------------------------------------- */

  function el(tag, className, text) {
    const node = document.createElement(tag);
    if (className) node.className = className;
    if (text !== undefined && text !== null) node.textContent = text;
    return node;
  }

  // The label is English interface text inside a paragraph whose `lang` is
  // the oration's; it carries its own `lang` so it is not read as Latin.
  function composedLabel(text) {
    const label = el('span', 'composed-label', text);
    label.lang = 'en';
    return label;
  }

  function clear(node) {
    while (node.firstChild) node.removeChild(node.firstChild);
  }

  /* ------------------------------------------------------------------------
   * WHERE A MESSAGE LANDS
   *
   * There is no one document landmark. The instruments name their `<main>` four
   * different ways — `#reading` on catena, scripture, sources and texts, `#map`
   * on history, `#canon` on law, `#reader-document` on the liturgy reader — and
   * `fail` used to look up `#reading` alone and return silently when it was not
   * there. On the other three, `fail(text)` did NOTHING AT ALL: no error, no
   * spoken line, and the page's "Loading…" placeholder and `aria-busy="true"`
   * left standing, which is worse than an error, because it tells a reader the
   * corpus is arriving when it is not. History and law escaped that only by
   * open-coding their own failure rendering rather than calling `fail`, and the
   * liturgy reader by having its own; the trap was set for whoever called it
   * next.
   *
   * So a message is now aimed, in this order:
   *
   *   1. an element or an id passed by the caller, which always wins;
   *   2. the first of DOCUMENT_LANDMARKS the page actually carries.
   *
   * `#reading` is first in that list, so every caller that passed nothing
   * before still lands exactly where it did. The list is the contract: a new
   * instrument either names its `<main>` with one of these or passes its own
   * node, and `tools/tests/test_browser_collisions.py` fails if a published
   * page names it anything else.
   * --------------------------------------------------------------------- */

  const DOCUMENT_LANDMARKS = ['reading', 'map', 'canon', 'reader-document'];

  /** The element a page-level message belongs in, or null if there is none. */
  function documentRegion(target) {
    if (target && typeof target === 'object' && target.nodeType === 1) return target;
    if (typeof target === 'string' && target) return document.getElementById(target);
    for (const id of DOCUMENT_LANDMARKS) {
      const node = document.getElementById(id);
      if (node) return node;
    }
    return null;
  }

  /**
   * The strip above the reading area, for something true of the whole page.
   *
   * Aimed the same way as `fail`, but at one id rather than a list: `#banner`
   * is the only banner host in the tree. A page without one — the liturgy
   * reader is the live case — still shows nothing, including the inline-mode
   * notice, and fixing that means giving that page a banner host in its own
   * markup rather than inventing one from here.
   */
  function showBanner(text, target) {
    const banner = target && typeof target === 'object' && target.nodeType === 1
      ? target
      : document.getElementById(typeof target === 'string' && target ? target : 'banner');
    if (!banner) return;
    banner.textContent = text;
    banner.hidden = false;
  }

  /**
   * The one-line spoken summary.
   *
   * The reading area is not itself a live region: replacing it would read a
   * whole Mass aloud on every change. This says what changed instead.
   *
   * It needs no target and has never had the defect `fail` had: where the live
   * region is absent this MAKES one and appends it to the body, so the message
   * is spoken on every page in the tree, named or not.
   */
  function statusLine(text) {
    let status = document.getElementById('reading-status');
    if (!status) {
      status = el('p', 'visually-hidden');
      status.id = 'reading-status';
      status.setAttribute('role', 'status');
      status.setAttribute('aria-live', 'polite');
      document.body.appendChild(status);
    }
    status.textContent = text;
  }

  /** A stated reason, in place of the text that could not be shown. */
  function notice(text) {
    const node = el('p', 'notice');
    node.appendChild(el('strong', null, 'Not shown: '));
    node.appendChild(document.createTextNode(text));
    return node;
  }

  /**
   * The page could not be drawn, and this says why, in the page's own document
   * region. `target` is an element or an id; without one the region is found by
   * DOCUMENT_LANDMARKS above.
   *
   * The spoken line is said whether or not a region was found, because a reader
   * on a page with no landmark at all is still owed the reason.
   */
  function fail(text, target) {
    const region = documentRegion(target);
    if (region) {
      clear(region);
      region.appendChild(el('p', 'error', text));
      region.setAttribute('aria-busy', 'false');
    }
    statusLine(text);
  }

  /** "after-pentecost" -> "After Pentecost"; "roman-1962" -> "Roman 1962". */
  function titleCase(id) {
    return String(id)
      .split(/[-_\s]+/)
      .filter(Boolean)
      .map((word) => word.charAt(0).toUpperCase() + word.slice(1))
      .join(' ');
  }

  /* ------------------------------------------------------------------------
   * Two kinds of station, in every act-keyed record
   *
   *   promulgated  an act stands behind it and its instrument is cited
   *   printed      a witness survives and no act has been located
   *
   * The difference is one of EVIDENCE, not of importance, and it is READ, never
   * inferred. Working it out from whether an instrument string happens to be
   * present is the guess the whole apparatus exists to prevent: a station whose
   * act is merely unread would come out looking like a station whose act is not
   * claimed at all, and the two are different claims.
   *
   * One allowance, and it is about the schema rather than about any station. A
   * file written before the distinction existed carries the field nowhere, and
   * every station in such a file is an act by the generator's own rule —
   * `act-history check` refuses a station without one. So a file that names the
   * field NOWHERE is read as all-promulgated; a file that names it ANYWHERE is
   * read literally, and a station missing it there is `unstated` and says so.
   *
   * It lives here because more than one page now reads it, and a rule about
   * evidence that each page kept its own copy of would be free to drift into
   * two answers about the same station.
   * --------------------------------------------------------------------- */

  const PROMULGATED = 'promulgated';
  const PRINTED = 'printed';
  const UNSTATED = 'unstated';

  function statedKind(station) {
    const value = station && (station.station_kind || station.station);
    return typeof value === 'string' && value ? value : null;
  }

  const stationKind = {
    PROMULGATED: PROMULGATED,
    PRINTED: PRINTED,
    UNSTATED: UNSTATED,

    /** Does this file speak the two-kinds vocabulary at all? */
    stated: function (stations) {
      return (stations || []).some((station) => statedKind(station) !== null);
    },

    of: function (station, stated) {
      return statedKind(station) || (stated ? UNSTATED : PROMULGATED);
    }
  };

  /* ------------------------------------------------------------------------
   * Selects
   *
   * Options are emitted in the order given and never re-sorted here: the
   * meaningful order — the temporal cycle, the calendar date, the plan's own
   * sequence — is the caller's to decide, and alphabetical order would destroy
   * every one of them.
   *
   * Groups are run-length: a new optgroup opens whenever the group label
   * changes. That keeps a 250-entry sanctoral navigable without ever moving an
   * option out of the order the caller put it in.
   * --------------------------------------------------------------------- */

  function fillSelect(select, items) {
    clear(select);

    const labels = new Set();
    for (const item of items) if (item.group) labels.add(item.group);
    const grouped = labels.size > 1;

    let parent = select;
    let openLabel = null;
    for (const item of items) {
      if (grouped) {
        const group = item.group || 'Other';
        if (group !== openLabel) {
          parent = document.createElement('optgroup');
          parent.label = group;
          parent.setAttribute('label', group);
          select.appendChild(parent);
          openLabel = group;
        }
      }
      const option = el('option', null, item.label);
      option.value = item.value;
      if (item.title) option.setAttribute('title', item.title);
      parent.appendChild(option);
    }

    select.disabled = !items.length;
  }

  function fillBibleSelect(select, bibles) {
    fillSelect(
      select,
      bibles.map((bible) => ({
        value: bible.id,
        label: bible.language ? bible.label + ' (' + bible.language + ')' : bible.label
      }))
    );
  }

  /**
   * How an edition numbers its psalms, in words: its numbering system and,
   * where it leaves psalm titles unnumbered, that too -- the King James prints
   * the Miserere as 51:1 where the Hebrew numbering it follows says 51:3, and a
   * label naming the system alone would describe a numbering it does not print.
   */
  function numberingLabel(bible) {
    const label = bible.numbering + ' numbering';
    return bible.psalm_titles === 'unnumbered' ? label + ', psalm titles unnumbered' : label;
  }

  function bibleMeta(bible) {
    const meta = [bible.label + ' — ' + numberingLabel(bible)];
    if (bible.psalter) meta.push(bible.psalter + ' psalter');
    return meta;
  }

  async function loadBibles() {
    let file;
    try {
      file = await loadJSON('bibles.json');
    } catch (error) {
      doneBootstrapping();
      return {
        ok: false,
        message: 'The translation list could not be loaded: ' + (error.message || error)
      };
    }
    doneBootstrapping();
    const bibles = (file && file.bibles) || [];
    if (!bibles.length) {
      return { ok: false, message: 'bibles.json lists no translations.' };
    }
    return { ok: true, bibles: bibles };
  }

  /* ------------------------------------------------------------------------
   * Loci
   * --------------------------------------------------------------------- */

  /**
   * The loci key an edition reads, as the manifest states it.
   *
   * `bibles.json` names it per edition (`loci`): the numbering system, or the
   * Hebrew numbering as an edition that leaves psalm titles unnumbered prints
   * it. The page takes the key and computes nothing; a manifest written before
   * the key existed falls back to the edition's numbering, which is the key
   * every title-numbering edition reads anyway.
   */
  function lociKey(bible) {
    return (bible && (bible.loci || bible.numbering)) || null;
  }

  /**
   * Pick the loci a given edition can actually read.
   *
   * Structure files key loci by how an edition is addressed -- numbering
   * system and psalm-title convention -- because the psalter is numbered
   * differently in the Vulgate and Hebrew traditions and the same citation
   * lands on different chapters, and an edition that leaves psalm titles
   * unnumbered prints most psalms a verse or two lower. No numbering logic
   * ships to the browser: the page reads the key its edition's manifest entry
   * names (`lociKey`) and takes the loci already computed for it. An edition
   * whose key has no entry is a gap in the data, and is reported rather than
   * silently guessed at — FAILURE 2.
   *
   * `edition`, where given, is the edition's id. An edition whose own printing
   * departs from the addressing it reads -- the Clementine opens Vulgate Psalm
   * 115 at verse 1, not 10 -- has its loci under `edition_loci[edition]`,
   * written by the generator from that edition's verse-alias table, and they
   * win. A reason the generator recorded for refusing the edition or the
   * addressing (`refused`) is the answer when no loci stand for it.
   *
   * The book token may sit on the locus or on the citation that owns it: a
   * reading names its book once and lets its loci carry chapter and verses
   * only. The token is what the fragment path is built from, so it wins over
   * the display name.
   */
  function lociFor(citation, numbering, edition) {
    const loci = (citation && citation.loci) || {};
    const refused = (citation && citation.refused) || {};
    const departures = (citation && citation.edition_loci) || {};
    if (edition && typeof refused[edition] === 'string') {
      return { problem: refused[edition] };
    }
    const own = edition ? departures[edition] : undefined;
    const chosen = Array.isArray(own) ? own : loci[numbering];
    const owner = (citation && (citation.token || citation.book)) || null;

    if (!Array.isArray(chosen) && typeof refused[numbering] === 'string') {
      return { problem: refused[numbering] };
    }

    if (Array.isArray(chosen) && chosen.length) {
      const resolved = [];
      for (const locus of chosen) {
        const book = locus.book || owner;
        if (!book) {
          return {
            problem: 'the citation names no book, so there is no fragment to fetch'
          };
        }
        resolved.push({
          book: book,
          chapter: locus.chapter,
          first: locus.first,
          last: locus.last
        });
      }
      return { loci: resolved };
    }

    const offered = Object.keys(loci).filter((key) => {
      return Array.isArray(loci[key]) && loci[key].length;
    });
    if (!offered.length) {
      return {
        problem: 'the citation carries no loci at all, so there is nothing to fetch'
      };
    }
    return {
      problem:
        'this edition numbers by "' + numbering + '", and the citation carries ' +
        'loci only for ' + offered.map((key) => '"' + key + '"').join(', ') + '.'
    };
  }

  /** The loci one edition reads for a citation: its key, and its own departures. */
  function editionLoci(citation, bible) {
    return lociFor(citation, lociKey(bible), (bible && bible.id) || null);
  }

  /**
   * OPEN BOUNDS — `first` or `last` may be null, and null is not zero.
   *
   * A structure file spells "from the start of the chapter" as a null `first`
   * and "to the end of it" as a null `last`, because neither page may be made
   * to know how many verses a chapter has in an edition it has not fetched. So
   * a reading of Genesis 1:1-2:2 is stored as two loci — {1, 1, null} and
   * {2, null, 2} — and a whole chapter as {7, null, null}.
   *
   * `Number(null)` is 0, which is finite, so any arithmetic that forgets this
   * silently turns "to the end of the chapter" into "up to verse 0" and shows
   * an empty passage with a confident reason attached. Every bound therefore
   * goes through here, and an absent bound becomes an infinity rather than a
   * number.
   */
  function bound(value, whenAbsent) {
    if (value === null || value === undefined || value === '') return whenAbsent;
    const number = Number(value);
    return Number.isFinite(number) ? number : whenAbsent;
  }

  function openStart(locus) {
    return bound(locus.first, null) === null;
  }

  function openEnd(locus) {
    return bound(locus.last, null) === null;
  }

  /**
   * Loci that continue one another are one span, not two.
   *
   * A citation running from one chapter into the next arrives as a locus with
   * an open end followed by a locus with an open start, and printing them
   * separately ("Gen 1:1-, Gen 2:-2") describes a reading nobody asked for.
   * A run is joined when the previous locus runs to the end of its chapter,
   * the next begins at the start of the chapter after it, and both name the
   * same book.
   */
  function lociRuns(loci) {
    const runs = [];
    for (const locus of loci) {
      const held = runs.length ? runs[runs.length - 1] : null;
      const tail = held ? held[held.length - 1] : null;
      const continues = tail &&
        tail.book === locus.book &&
        openEnd(tail) && openStart(locus) &&
        Number(locus.chapter) === Number(tail.chapter) + 1;
      if (continues) held.push(locus);
      else runs.push([locus]);
    }
    return runs;
  }

  /**
   * One run, in the notation the plan's own prose uses: "Genesis 1:1-2:2",
   * "Genesis 3:1-24", "Psalm 46", "Daniel 1-6".
   *
   * A run left open at one end only — which this corpus does not produce, but
   * a hand-written structure file could — is printed with "ff." rather than
   * with a verse number nobody computed.
   */
  function formatRun(run, bookLabel) {
    const head = run[0];
    const tail = run[run.length - 1];
    const book = bookLabel || head.book;
    const from = Number(head.chapter);
    const to = Number(tail.chapter);

    if (openStart(head) && openEnd(tail)) {
      return book + ' ' + (from === to ? from : from + '-' + to);
    }

    if (from === to) {
      const lo = openStart(head) ? 1 : bound(head.first, 1);
      if (openEnd(tail)) return book + ' ' + from + ':' + lo + 'ff.';
      const hi = bound(tail.last, lo);
      return book + ' ' + from + ':' + (lo === hi ? String(lo) : lo + '-' + hi);
    }

    const opening = openStart(head) ? String(from) : from + ':' + bound(head.first, 1);
    const closing = openEnd(tail) ? to + 'ff.' : to + ':' + bound(tail.last, 1);
    return book + ' ' + opening + '-' + closing;
  }

  /**
   * "Ps 24:1-3, Ps 24:4" — used where the structure names no reference.
   *
   * `options.book` substitutes a display name for the fragment token, so a
   * page that knows the citation names one book can print "Genesis 1:1-2:2"
   * where the path needs "Gen". Pass it or omit it consistently: `recastLoci`
   * compares two formattings of the same citation, and comparing a formatting
   * that names the book differently would report a difference that is not one.
   */
  function formatLoci(loci, options) {
    const book = (options && options.book) || null;
    return lociRuns(loci).map((run) => formatRun(run, book)).join(', ');
  }

  /**
   * Every distinct chapter a list of citations needs, under this loci key --
   * and, where `edition` is given, as that edition's own departures place them.
   */
  function chaptersNeeded(citations, numbering, edition) {
    const wanted = new Map();
    for (const citation of citations) {
      if (!citation || citation.unresolved) continue;
      const picked = lociFor(citation, numbering, edition);
      if (!picked.loci) continue;
      for (const locus of picked.loci) {
        wanted.set(locus.book + '|' + locus.chapter, {
          book: locus.book,
          chapter: locus.chapter
        });
      }
    }
    return Array.from(wanted.values());
  }

  /**
   * Fetch every chapter a selection needs, in one pass, through the cache.
   * A chapter already held costs nothing; a chapter cited twice is fetched once.
   */
  async function fetchFragments(bible, citations, state, bibles) {
    if (state && state.scriptureCompanion) return fetchReaderFragments(bible, citations, state, bibles);
    const chapters = chaptersNeeded(citations, lociKey(bible), bible.id);
    const results = await Promise.all(
      chapters.map((needed) => loadChapter(bible.id, needed.book, needed.chapter))
    );
    const fragments = new Map();
    chapters.forEach((needed, index) => {
      fragments.set(needed.book + '|' + needed.chapter, results[index]);
    });
    return { fragments: fragments, chapters: chapters };
  }

  /**
   * Liturgy's optional named Latin companion. Each edition reads the citation's
   * own generated loci and refusals through the existing chapter loader. The
   * returned bundle is explicit; legacy two-argument fetchFragments consumers
   * retain their exact shape, requests and rendering.
   */
  async function fetchReaderFragments(bible, citations, state, bibles) {
    const descriptor = state && state.scriptureCompanion;
    if (!descriptor) return fetchFragments(bible, citations);
    const held = (bibles || []).filter(function (row) {
      return row.id === descriptor.id && row.language === SOURCE_LANGUAGE;
    });
    if (held.length !== 1 || (descriptor.numbering || null) !== (held[0].numbering || null)) {
      throw new Error('The named Latin Bible companion is not held with this numbering.');
    }
    const companion = held[0];
    const loaded = await Promise.all([
      fetchFragments(bible, citations),
      companion.id === bible.id ? null : fetchFragments(companion, citations)
    ]);
    return { fragments: loaded[0].fragments, chapters: loaded[0].chapters,
      companion: { bible: companion, fragments: (loaded[1] || loaded[0]).fragments } };
  }

  /* ------------------------------------------------------------------------
   * Rendering
   * --------------------------------------------------------------------- */

  /** The range a locus asks for, said in words, for a failure that must name it. */
  function locusRange(locus) {
    const where = locus.book + ' ' + locus.chapter;
    if (openStart(locus) && openEnd(locus)) return 'no verses at all in ' + where;
    if (openEnd(locus)) {
      return 'no verses from ' + bound(locus.first, 1) + ' onward in ' + where;
    }
    if (openStart(locus)) {
      return 'no verses up to ' + bound(locus.last, 1) + ' in ' + where;
    }
    const first = bound(locus.first, 1);
    const last = bound(locus.last, first);
    return 'no verse' + (first === last ? ' ' : 's ') +
      (first === last ? String(first) : first + '-' + last) + ' in ' + where;
  }

  /**
   * Render one locus out of an already-fetched chapter.
   *
   * Verses are emitted in ascending numeric order WITHIN the locus, but loci
   * are emitted in the order the citation lists them — a chant citation such as
   * "Psalm 138:18, 5-6" is deliberately out of sequence and must stay that way.
   *
   * `options.showChapter` prints the chapter before the text. A citation that
   * stays inside one chapter does not want it; one that runs across three does,
   * because the verse numbers restart at each boundary and a reader with no
   * marker cannot tell a new chapter from a repeated verse.
   *
   * Carries FAILURE 3 (the fragment is not there at all) and FAILURE 4 (the
   * fragment is there and the verses are not).
   */
  function renderLocus(locus, fragment, language, options) {
    const out = document.createDocumentFragment();
    out.passage = null;
    if (!fragment.ok) {
      out.appendChild(notice(fragment.problem));
      return out;
    }

    // Absent bounds are infinities, never zero: see `bound` above.
    const first = bound(locus.first, -Infinity);
    const last = bound(locus.last, Infinity);
    const numbers = Object.keys(fragment.verses)
      .map(Number)
      .filter((n) => Number.isFinite(n) && n >= first && n <= last)
      .sort((a, b) => a - b);

    if (!numbers.length) {
      out.appendChild(notice('this edition has ' + locusRange(locus) + '.'));
      return out;
    }

    if (options && options.showChapter) {
      const mark = el('p', 'chapter-mark');
      mark.appendChild(el('span', 'chapter-mark-word', 'Chapter '));
      mark.appendChild(el('span', 'chapter-mark-number', String(locus.chapter)));
      out.appendChild(mark);
    }

    // A segment after the first joins the passage already open, so a citation
    // cited in pieces reads as the one passage it is.
    const joining = options && options.into;
    const passage = joining || el('p', 'passage');
    // The edition's own language, so that Latin is spoken and hyphenated as
    // Latin and English as English.
    if (language) passage.lang = language;
    if (joining && options.elide) {
      passage.appendChild(el('span', 'elision', ' … '));
    }

    for (const number of numbers) {
      const verse = el('span', 'verse');
      const marker = el('sup', 'verse-num', String(number));
      marker.setAttribute('aria-hidden', 'true');
      verse.appendChild(marker);
      // The number is repeated for assistive technology, which does not get the
      // typographic cue that a superscript is a verse marker.
      const label = el('span', 'visually-hidden', 'Verse ' + number + '. ');
      label.lang = 'en';
      verse.appendChild(label);
      verse.appendChild(document.createTextNode(fragment.verses[number] + ' '));
      passage.appendChild(verse);
    }
    if (!joining) out.appendChild(passage);

    out.passage = passage;

    // Gaps are only reported between bounds that were actually asked for. An
    // open end has no expected last verse, so the scan stops at the last verse
    // the fragment holds rather than inventing verses that were never claimed;
    // a bounded locus still reports a missing tail, as it always did.
    const from = Number.isFinite(first) ? first : numbers[0];
    const to = Number.isFinite(last) ? last : numbers[numbers.length - 1];
    const gaps = [];
    for (let n = from; n <= to; n += 1) {
      if (!numbers.includes(n)) gaps.push(n);
    }
    if (gaps.length && gaps.length < to - from + 1) {
      out.appendChild(
        notice(
          'verse' + (gaps.length > 1 ? 's ' : ' ') + gaps.join(', ') +
          ' of ' + locus.book + ' ' + locus.chapter +
          ' — absent from this edition\'s fragment.'
        )
      );
    }

    return out;
  }

  /**
   * Where a structure file's own numbering differs from the edition's, say so.
   *
   * A postconciliar Mass cites "Psalm 25:1-3" because the missal numbers by the
   * Hebrew psalter; a Vulgate-numbered edition holds that text at Psalm 24. The
   * text shown is right and the reference shown is right, and a reader who
   * notices that they disagree is owed the reason rather than left to doubt one
   * of them.
   */
  function recastLoci(citation, bible, sourceNumbering, picked, options) {
    const written = citationNumbering(citation, sourceNumbering);
    if (!written || !picked.loci) return null;
    const source = lociFor(citation, written);
    if (!source.loci) return null;
    if (formatLoci(source.loci, options) === formatLoci(picked.loci, options)) {
      return null;
    }
    // An edition whose own printing departs from its numbering is not "in"
    // that numbering at this citation, so it is not said to be.
    const departs = Boolean(
      citation.edition_loci && Array.isArray(citation.edition_loci[bible.id])
    );
    return formatLoci(picked.loci, options) + (departs
      ? ' as this edition prints it'
      : ' in this edition\'s ' + numberingLabel(bible));
  }

  /**
   * The psalm numbering a citation is written in: its own, which the generator
   * states on every psalm citation, else the structure file's. A psalm number
   * names nothing until its system is said, and one Missal cites in both -- the
   * postconciliar antiphons keep the Missal's Vulgate numbers inside a
   * Hebrew-numbered file -- so a file-wide numbering cannot be trusted for one.
   */
  function citationNumbering(citation, sourceNumbering) {
    return (citation && citation.numbering) || sourceNumbering || null;
  }

  /** "Vulgate numbering", for a citation that states its psalm numbering; else null. */
  function psalmNumberingLabel(citation) {
    const numbering = citation && citation.numbering;
    if (!numbering) return null;
    return String(numbering).charAt(0).toUpperCase() + String(numbering).slice(1) +
      ' numbering';
  }

  /**
   * One citation, with its reference line and its text — or with the reason
   * there is no text. Carries FAILURE 1 (unresolved) and FAILURE 2 (numbering).
   *
   * `sourceNumbering` is the numbering the structure file's own references are
   * written in, where the caller knows it.
   *
   * `options.book`    a display name for the book, where the caller knows one
   *                   that reads better than the fragment token
   * `options.showRef` false where the caller has already given the reference a
   *                   better place than a line above the text. The recast note
   *                   survives either way: a reader who is shown one numbering
   *                   and given another edition's text is owed the reason.
   */
  function renderCitation(citation, bible, fragments, sourceNumbering, options) {
    const block = el('div', 'citation');
    const showRef = !(options && options.showRef === false);

    if (citation.unresolved) {
      block.appendChild(
        el('p', 'citation-ref',
          citation.ref || (options && options.book) || citation.book ||
          citation.token || 'Unlabelled citation')
      );
      block.appendChild(notice(String(citation.unresolved)));
      return block;
    }

    const picked = editionLoci(citation, bible);
    const label = citation.ref ||
      (picked.loci ? formatLoci(picked.loci, options) : null) ||
      (options && options.book) || citation.book || citation.token ||
      'Unlabelled citation';
    const recast = recastLoci(citation, bible, sourceNumbering, picked, options);
    if (showRef) {
      const line = el('p', 'citation-ref', label);
      // Which psalm numbering the reference above is written in; the recast
      // note, where there is one, says where this edition prints it.
      const written = psalmNumberingLabel(citation);
      if (written) line.appendChild(el('span', 'citation-numbering', written));
      if (recast) line.appendChild(el('span', 'citation-recast', recast));
      block.appendChild(line);
    } else if (recast) {
      block.appendChild(el('p', 'citation-ref citation-ref-recast-only', recast));
    }

    if (!picked.loci) {
      block.appendChild(notice(picked.problem));
      return block;
    }

    // Verse numbers restart at a chapter boundary, so a citation that crosses
    // one must say where the boundary is.
    const chapters = new Set(picked.loci.map((locus) => String(locus.chapter)));
    const showChapter = chapters.size > 1;

    // A citation is one passage even when it is cited in segments: the
    // reference line above already names them ("Psalm 24:16, 18"), so the words
    // run on as they are sung rather than breaking into a paragraph apiece. A
    // gap between segments is marked, because the omitted verses are not
    // silence — they are text the missal chose to pass over.
    let previous = null;
    let open = null;
    for (const locus of picked.loci) {
      const fragment = fragments.get(locus.book + '|' + locus.chapter) ||
        { ok: false, problem: locus.book + ' ' + locus.chapter + ' was not loaded.' };
      const abuts = previous !== null &&
        previous.chapter === locus.chapter &&
        previous.last !== null && previous.last !== undefined &&
        locus.first === previous.last + 1;
      // A new chapter opens a new passage, since its verse numbers restart and
      // the chapter mark has to sit between them; within one chapter the
      // segments join, with an ellipsis where verses were passed over.
      const sameChapter = previous !== null && previous.chapter === locus.chapter;
      const rendered = renderLocus(locus, fragment, bible.language, {
        showChapter: showChapter && !sameChapter,
        into: sameChapter ? open : null,
        elide: sameChapter && !abuts
      });
      block.appendChild(rendered);
      if (rendered.passage) open = rendered.passage;
      previous = locus;
    }

    return block;
  }

  /* ------------------------------------------------------------------------
   * The render token
   *
   * A selection made while fragments are in flight overtakes the one before it.
   * The newest render wins; an older one that comes back late throws its work
   * away rather than painting over the reader's current choice.
   * --------------------------------------------------------------------- */

  let renderToken = 0;

  function beginRender() {
    renderToken += 1;
    return renderToken;
  }

  function isCurrentRender(token) {
    return token === renderToken;
  }

  /* ------------------------------------------------------------------------
   * URL state
   *
   * The hash carries the whole selection, so a link is shareable and a reload
   * lands where the reader was. The keys differ per page and are the page's
   * business; the mechanics are not.
   *
   * A hash the page wrote itself is recognised by its text rather than by a
   * flag, so a flag can never be left set and swallow the reader's next Back.
   * --------------------------------------------------------------------- */

  let lastWritten = null;

  function readHash() {
    return new URLSearchParams(window.location.hash.replace(/^#/, ''));
  }

  function hashText(pairs) {
    const parts = [];
    for (const [key, value] of pairs) {
      if (value === null || value === undefined || value === '') continue;
      parts.push(key + '=' + encodeURIComponent(value));
    }
    return parts.length ? '#' + parts.join('&') : '';
  }

  function writeHash(pairs) {
    const next = hashText(pairs);
    if (window.location.hash === next) return;
    lastWritten = next;
    window.location.hash = next;
  }

  /** Canonicalize incremental state without filling the Back-button history. */
  function replaceHash(pairs) {
    const next = hashText(pairs);
    if (window.location.hash === next) return;
    window.history.replaceState(
      window.history.state,
      '',
      window.location.pathname + window.location.search + next
    );
  }

  function onHashChange(handler) {
    window.addEventListener('hashchange', () => {
      if (window.location.hash === lastWritten) {
        lastWritten = null;
        return;
      }
      handler(readHash());
    });
  }

  /* ------------------------------------------------------------------------
   * Keyboard stepping, shared because both pages step through a list
   * --------------------------------------------------------------------- */

  /**
   * Arrow keys step through whatever list the page is showing — but never
   * while a control has focus: left and right belong to the select the reader
   * is operating.
   */
  function onArrowStep(step) {
    document.addEventListener('keydown', (event) => {
      if (event.altKey || event.ctrlKey || event.metaKey || event.shiftKey) return;
      const target = event.target;
      if (target && target.closest && target.closest('select, input, textarea, button')) {
        return;
      }
      if (event.key === 'ArrowLeft') step(-1);
      if (event.key === 'ArrowRight') step(1);
    });
  }

  /* ------------------------------------------------------------------------
   * The shared part of the offline fallback
   *
   * This is not the data contract and it is not a corpus: it is what the pages
   * show when they are opened straight off disk, where fetch is refused, so
   * that neither page is ever blank. The manifest and a few chapters are shared;
   * each page registers its own structure file.
   * --------------------------------------------------------------------- */

  addInlineFiles({
    'bibles.json': {
      bibles: [
        {
          id: 'douay-rheims',
          label: 'Douay-Rheims (Challoner)',
          language: 'en',
          numbering: 'vulgate',
          psalter: 'gallican'
        },
        {
          id: 'clementine-vulgate',
          label: 'Clementine Vulgate',
          language: 'la',
          numbering: 'vulgate',
          psalter: 'gallican'
        }
      ]
    },

    'douay-rheims/chapters/Ps/24.json': {
      book: 'Ps',
      chapter: 24,
      verses: {
        1: 'Unto the end, a psalm for David. To thee, O Lord, have I lifted up my soul.',
        2: 'In thee, O my God, I put my trust; let me not be ashamed.',
        3: 'Neither let my enemies laugh at me: for none of them that wait on thee shall be confounded.',
        4: 'Let all them be confounded that act unjust things without cause. Shew, O Lord, thy ways to me, and teach me thy paths.'
      }
    },

    'douay-rheims/chapters/Rom/13.json': {
      book: 'Rom',
      chapter: 13,
      verses: {
        11: 'And that, knowing the season, that it is now the hour for us to rise from sleep. For now our salvation is nearer than when we believed.',
        12: 'The night is passed And the day is at hand. Let us, therefore cast off the works of darkness and put on the armour of light.'
      }
    },

    'douay-rheims/chapters/Gen/1.json': {
      book: 'Gen',
      chapter: 1,
      verses: {
        1: 'In the beginning God created heaven, and earth.',
        2: 'And the earth was void and empty, and darkness was upon the face of the deep; and the spirit of God moved over the waters.',
        3: 'And God said: Be light made. And light was made.'
      }
    },

    'clementine-vulgate/chapters/Ps/24.json': {
      book: 'Ps',
      chapter: 24,
      verses: {
        1: 'In finem. Psalmus David. Ad te, Domine, levavi animam meam:',
        2: 'Deus meus, in te confido; non erubescam.',
        3: 'Neque irrideant me inimici mei: etenim universi qui sustinent te, non confundentur.',
        4: 'Confundantur omnes iniqua agentes supervacue. Vias tuas, Domine, demonstra mihi, et semitas tuas edoce me.'
      }
    },

    'clementine-vulgate/chapters/Rom/13.json': {
      book: 'Rom',
      chapter: 13,
      verses: {
        11: 'Et hoc scientes tempus: quia hora est jam nos de somno surgere. Nunc enim propior est nostra salus, quam cum credidimus.',
        12: 'Nox præcessit, dies autem appropinquavit. Abjiciamus ergo opera tenebrarum, et induamur arma lucis.'
      }
    },

    'clementine-vulgate/chapters/Gen/1.json': {
      book: 'Gen',
      chapter: 1,
      verses: {
        1: 'In principio creavit Deus cælum et terram.',
        2: 'Terra autem erat inanis et vacua, et tenebræ erant super faciem abyssi: et spiritus Dei ferebatur super aquas.',
        3: 'Dixitque Deus: Fiat lux. Et facta est lux.'
      }
    }
  });

  /* ------------------------------------------------------------------------
   * Propers
   *
   * WHAT A PROPER IS, AND HOW IT READS, IS SHARED. Two pages now show the text
   * of a Mass: the propers browser, which reaches it by choosing a Mass, and the
   * assembly page, which reaches it by choosing a date. They must not disagree
   * about what a Collect looks like, when an incipit earns its place, which
   * translation is shown, or how an absent text is said — so none of that lives
   * in either page.
   *
   * Page-specific vocabulary stays in the page. A proper is not page-specific.
   * --------------------------------------------------------------------- */

  // The missals hold their orations in Latin; a translation is an addition to
  // that, never a replacement of it.
  const SOURCE_LANGUAGE = 'la';
  const LANGUAGE_NAMES = {
    la: 'Latin',
    en: 'English',
    fr: 'French',
    de: 'German',
    es: 'Spanish',
    it: 'Italian',
    pl: 'Polish'
  };

  function languageName(code) {
    return LANGUAGE_NAMES[code] || String(code || '').toUpperCase();
  }

  /**
   * One year of a cycle-varying proper: its citations and its own words.
   *
   * A cycle is an object and not a list of citations, because a proper may vary
   * in kind as well as in text — an acclamation composed one year and
   * scriptural the next — so each year carries both. Every reader of `cycles`
   * goes through here, so the shape is asserted in one place rather than
   * assumed in four; assuming it is what threw a TypeError on every
   * cycle-bearing Mass when the shape changed under the pages.
   */
  const SUNDAY_CYCLE_KEYS = Object.freeze(['A', 'B', 'C']);
  const WEEKDAY_CYCLE_KEYS = Object.freeze(['I', 'II']);

  function cycleFrom(proper, family, key) {
    const held = (proper && proper[family] && proper[family][key]) || null;
    if (!held) return { citations: [], text: null };
    return {
      citations: held.citations || [],
      text: held.text || null,
      translations: held.translations || [],
      unavailable_translations: held.unavailable_translations || [],
      untranslated: held.untranslated || [],
      latin: held.latin || null,
      coverage: held.coverage || null,
      text_status: held.text_status || null
    };
  }

  function cycleKeysFrom(proper, family, allowed) {
    const rows = (proper && proper[family]) || {};
    const keys = Object.keys(rows);
    const invalid = keys.filter((key) => allowed.indexOf(key) < 0);
    if (invalid.length) {
      throw new Error(family + ' carries unsupported Lectionary cycle keys: ' + invalid.join(', '));
    }
    return keys
      .sort()
      .filter((key) => {
        const cycle = cycleFrom(proper, family, key);
        return cycle.citations.length || cycle.text ||
          cycle.translations.some((translation) => translation && translation.text) ||
          cycle.unavailable_translations.length || cycle.untranslated.length ||
          (cycle.latin && cycle.latin.withheld);
      });
  }

  /** Sunday-cycle material is owned only by the generated `cycles` object. */
  function sundayCycleOf(proper, key) {
    return cycleFrom(proper, 'cycles', key);
  }

  function sundayCycleKeysOf(proper) {
    return cycleKeysFrom(proper, 'cycles', SUNDAY_CYCLE_KEYS);
  }

  /** Ferial I/II material is independent and owned only by `weekday_cycles`. */
  function weekdayCycleOf(proper, key) {
    return cycleFrom(proper, 'weekday_cycles', key);
  }

  function weekdayCycleKeysOf(proper) {
    return cycleKeysFrom(proper, 'weekday_cycles', WEEKDAY_CYCLE_KEYS);
  }

  /**
   * Backward-compatible generic access for renderers whose selected cycle key
   * already identifies its family. The source objects remain distinct.
   */
  function cycleOf(proper, key) {
    if (SUNDAY_CYCLE_KEYS.indexOf(key) >= 0) return sundayCycleOf(proper, key);
    if (WEEKDAY_CYCLE_KEYS.indexOf(key) >= 0) return weekdayCycleOf(proper, key);
    return { citations: [], text: null };
  }

  /** Every held Lectionary variant, without merging the two source objects. */
  function cycleKeysOf(proper) {
    return sundayCycleKeysOf(proper).concat(weekdayCycleKeysOf(proper));
  }

  /** A cycle's readable name: "Year A" for the Sunday cycles, else the key. */
  function cycleLabel(key) {
    return /^[A-C]$/.test(key) ? 'Year ' + key : 'Cycle ' + key;
  }

  /** Every citation a Mass carries, including each cycle's. */
  function citationsOf(mass) {
    const found = [];
    for (const proper of (mass && mass.propers) || []) {
      for (const citation of proper.citations || []) found.push(citation);
      for (const key of cycleKeysOf(proper)) {
        for (const citation of cycleOf(proper, key).citations) found.push(citation);
      }
    }
    return found;
  }

  /**
   * A stand-in for a formulary nobody has transcribed yet.
   *
   * The compiler writes one proper named "Placeholder", whose body is a sentence
   * about the corpus rather than a prayer. Rendering it as a proper prints an
   * oration that does not exist, under a slot name that is not a slot name, and
   * a reader counting the parts of the Mass off the page would count wrong. It
   * is recognised here, once, so that both pages say the same quiet thing about
   * it — one line for the Mass, never one line per slot.
   */
  function isPlaceholder(proper) {
    return Boolean(proper) && proper.name === 'Placeholder';
  }

  /** Is this Mass a day the calendar keeps whose propers are not compiled? */
  function massIsUncompiled(mass) {
    const propers = (mass && mass.propers) || [];
    return propers.length > 0 && propers.every(isPlaceholder);
  }

  /**
   * Does this Mass carry anything to read?
   *
   * A placeholder is not content. Most of the sanctoral is presently a registry
   * entry and a placeholder: the calendar knows the day, and the propers for it
   * have not been compiled. That is worth saying once, plainly, rather than
   * printing a sentence about the corpus where a prayer belongs.
   */
  function massHasContent(mass) {
    for (const proper of (mass && mass.propers) || []) {
      if (isPlaceholder(proper)) continue;
      if (proper.text || proper.incipit) return true;
      if ((proper.translations || []).some((translation) => translation && translation.text)) return true;
      if ((proper.citations || []).length) return true;
      if (cycleKeysOf(proper).length) return true;
    }
    return false;
  }

  /**
   * Every language a missal can render its composed propers in, with how much
   * of the missal each one actually reaches.
   *
   * The coverage is counted rather than assumed. A translation set that reaches
   * a tenth of the orations is a legitimate state — the rights position differs
   * sharply between the two missals and partial coverage is expected to be
   * permanent, not temporary — so the reader is owed the figure instead of a
   * dropdown that implies completeness.
   */
  function orationLanguagesOf(structure) {
    const report = structure && structure.coverage;
    return report && report.schema === 'triptych-missal-coverage/v1'
      ? report.languages : Array.from(new Set([SOURCE_LANGUAGE].concat(
        (structure && structure.translations || []).map(function (row) { return row.lang; }).filter(Boolean)
      ))).map(function (lang) { return { lang: lang }; });
  }

  /** The label an orations control gives one of those languages. */
  function orationLanguageLabel(entry) {
    // A zero denominator is not a ratio: "0 of 0" reads as a total absence.
    return languageName(entry.lang) + (!Number.isInteger(entry.targets)
      ? ' — coverage not assessed'
      : entry.targets === 0 ? ' — no composed texts represented'
        : ' — ' + entry.available_targets + ' of ' + entry.targets + ' represented texts available');
  }

  const COVERAGE_RELATIONSHIPS = Object.freeze({
    'exact-target': 'exact target wording',
    'historical-antecedent': 'historical antecedent',
    'study-translation': 'study translation',
    'bible-reconstruction': 'Bible reconstruction',
    'unresolved': 'target relationship unresolved'
  });

  function validateBodyLanguages(unit) {
    if (!unit || !Object.prototype.hasOwnProperty.call(unit, 'body_languages')) return;
    if (!Array.isArray(unit.body_languages) || unit.body_languages.length !== 1 ||
        unit.body_languages[0] !== 'en' || unit.component !== 'proper-body' ||
        !unit.scripture_component || typeof unit.scripture_component !== 'object' ||
        Array.isArray(unit.scripture_component)) {
      throw new Error('language-only body coverage requires English scope and a separate Scripture component');
    }
  }

  function languageBodyTargetMatches(proper, row) {
    if (!row || !row.target || row.target.extent !== 'body') return false;
    const unit = proper.coverage;
    validateBodyLanguages(unit);
    if (!unit || !unit.body_languages || !unit.body_languages.includes(row.lang)) return false;
    const target = row.target;
    function identity(parts) {
      return parts.map(function (one) {
        return encodeURIComponent(String(one)).replace(/[!'()*]/g, function (c) {
          return '%' + c.charCodeAt(0).toString(16).toUpperCase();
        });
      }).join(':');
    }
    const prefix = decodeURIComponent(unit.target_id.split(':')[0]).split(':').slice(0, 2);
    const source = identity(prefix.concat([target.mass, target.form_id,
      target.proper, target.occurrence]));
    return identity([source, unit.cycle_family || 'all', target.cycle]) === unit.target_id &&
      target.proper === proper.name;
  }

  function coverageUnitsOf(owner) {
    if (!owner) return [];
    validateBodyLanguages(owner.coverage);
    const units = owner.coverage && owner.coverage.schema === 'triptych-missal-unit-coverage/v1'
      ? [owner.coverage] : [];
    ['cycles', 'weekday_cycles'].forEach(function (family) {
      Object.values(owner[family] || {}).forEach(function (child) {
        units.push.apply(units, coverageUnitsOf(child));
      });
    });
    return units;
  }

  /** Select report units through existing resolved events, never re-resolve a Mass. */
  function selectedCoverageUnits(result, structure) {
    const units = [];
    function visit(event) {
      if (event.kind === 'proper-choice') {
        (event.options || []).forEach(function (option) { (option.events || []).forEach(visit); });
        return;
      }
      if (event.kind !== 'proper' || !event.selected || event.selected.kind === 'absent') return;
      (event.orationGroups || []).forEach(function (group) {
        (group.members || []).forEach(function (member) { if (member.id !== event.id) visit(member); });
      });
      const hook = (event.sourceHooks || []).find(function (row) { return row.kind === 'proper-structure'; });
      if (!hook) return;
      const mass = (structure.masses || []).find(function (row) {
        return hook.id.slice(0, hook.id.lastIndexOf('/')) === structure.calendar + '/' + row.key;
      });
      const proper = mass && mass.propers[Number(hook.id.slice(hook.id.lastIndexOf('/') + 1)) - 1];
      if (!proper) return;
      const selected = event.selected;
      const cycles = selected.kind === 'cycle-alternatives'
        ? selected.alternatives.map(function (row) { return row.cycle; })
        : selected.cycle ? [selected.cycle] : [];
      coverageUnitsOf(proper).forEach(function (unit) {
        if (!unit.cycle || unit.cycle === 'all' || cycles.indexOf(unit.cycle) >= 0) units.push(unit);
      });
    }
    (result && result.events || []).forEach(visit);
    return units;
  }

  function selectedOrdinaryCoverageUnits(result, ordinary) {
    const selected = new Set((result && result.events || []).filter(function (event) {
      return event.kind === 'ordinary-element';
    }).map(function (event) { return event.id.slice('ordinary-element/'.length); }));
    return (ordinary && ordinary.sections || []).flatMap(function (section) {
      return (section.elements || []).filter(function (element) {
        return selected.has(element.key) && element.coverage;
      }).map(function (element) { return element.coverage; });
    });
  }

  /** Only report identities and dispositions are aggregated; text rows are never counted. */
  function summarizeCoverage(units) {
    const unique = new Map(units.map(function (unit) {
      validateBodyLanguages(unit); return [unit.occurrence_id, unit];
    }));
    const languages = new Map();
    ['la', 'en'].forEach(function (lang) {
      languages.set(lang, {
        lang: lang, targets: new Set(), occurrences: 0, available: 0,
        available_targets: new Set(), exact_target: 0, exact_target_targets: new Set(),
        scripture_targets: new Set(), scripture_occurrences: 0,
        mixed_targets: new Set(), mixed_occurrences: 0,
        availability: Object.fromEntries(['available', 'not-publishable', 'not-sourced',
          'unresolved', 'inapplicable', 'absent-in-witness'].map(function (value) { return [value, 0]; })),
        relationships: Object.fromEntries(Object.keys(COVERAGE_RELATIONSHIPS).map(function (value) { return [value, 0]; })),
        collations: Object.fromEntries(['collated', 'uncollated', 'not-applicable', 'unresolved'].map(function (value) { return [value, 0]; })),
        witnesses: new Map()
      });
    });
    const targets = new Set();
    const witnesses = new Set();
    unique.forEach(function (unit) {
      targets.add(unit.target_id);
      (unit.languages || []).forEach(function (entry) {
        const row = languages.get(entry.lang);
        if (unit.scripture_component) {
          row.scripture_targets.add(unit.scripture_component.target_id);
          row.scripture_occurrences += 1;
          if (!unit.body_languages || unit.body_languages.includes(entry.lang)) {
            row.mixed_targets.add(unit.target_id); row.mixed_occurrences += 1;
          }
        }
        if (unit.component === 'scripture') {
          row.scripture_targets.add(unit.target_id); row.scripture_occurrences += 1; return;
        }
        if (unit.body_languages && !unit.body_languages.includes(entry.lang)) return;
        row.targets.add(unit.target_id); row.occurrences += 1;
        row.availability[entry.availability] = (row.availability[entry.availability] || 0) + 1;
        row.relationships[entry.relationship] = (row.relationships[entry.relationship] || 0) + 1;
        row.collations[entry.collation] = (row.collations[entry.collation] || 0) + 1;
        if (entry.availability === 'available') {
          row.available += 1; row.available_targets.add(unit.target_id);
          if (entry.relationship === 'exact-target' || (entry.witnesses || []).some(function (witness) {
            return witness.relationship === 'exact-target';
          })) {
            row.exact_target += 1; row.exact_target_targets.add(unit.target_id);
          }
        }
        (entry.witnesses || []).forEach(function (witness) {
          witnesses.add(JSON.stringify([unit.target_id, entry.lang, witness.id]));
          if (!row.witnesses.has(witness.id)) row.witnesses.set(witness.id, Object.assign({}, witness, {
            available: 0, available_targets: new Set(), relationships: new Set(), publication_bases: new Set(), aliases: new Set(), collations: new Set()
          }));
          const held = row.witnesses.get(witness.id);
          held.available += 1; held.available_targets.add(unit.target_id);
          held.relationships.add(witness.relationship); held.publication_bases.add(witness.publication_basis);
          held.collations.add(witness.collation);
          (witness.aliases || []).forEach(function (alias) { held.aliases.add(alias); });
        });
      });
    });
    return { schema: 'triptych-missal-coverage/v1', scope: 'selection', denominator: 'represented-units',
      count_basis: {
        canonical_targets: 'distinct source-owned targets within this recension',
        occurrences: 'appointed units, including distinct cycle owners',
        witness_alternatives: 'distinct published translation witnesses per target and language'
      }, counts: {
      canonical_targets: targets.size, occurrences: unique.size, witness_alternatives: witnesses.size
    }, languages: Array.from(languages.values()).map(function (row) {
      ['targets', 'available_targets', 'exact_target_targets', 'scripture_targets', 'mixed_targets'].forEach(function (key) {
        row[key] = row[key].size;
      });
      row.witnesses = Array.from(row.witnesses.values()).sort(function (a, b) { return a.id < b.id ? -1 : a.id > b.id ? 1 : 0; }).map(function (witness) {
        witness.available_targets = witness.available_targets.size;
        witness.targets = witness.available_targets; witness.occurrences = witness.available;
        witness.relationships = Array.from(witness.relationships).filter(Boolean).sort();
        witness.publication_bases = Array.from(witness.publication_bases).filter(Boolean).sort();
        witness.aliases = Array.from(witness.aliases).sort();
        witness.collations = Array.from(witness.collations).filter(Boolean).sort();
        delete witness.relationship;
        delete witness.collation;
        delete witness.publication_basis;
        return witness;
      });
      return row;
    }) };
  }

  function coverageWitnesses(report, language) {
    const row = report && (report.languages || []).find(function (entry) { return entry.lang === language; });
    return (row && row.witnesses || []).map(function (witness) {
      return Object.assign({}, witness, { label: witness.label + ' — ' + witness.available +
        ' of ' + row.occurrences + ' uses' +
        (witness.relationships && witness.relationships.length ? '; ' + witness.relationships.map(function (value) {
          return COVERAGE_RELATIONSHIPS[value] || value;
        }).join(', ') : '') });
    });
  }

  function coverageSummaryText(report, language, witnessId, component) {
    const row = report && (report.languages || []).find(function (entry) { return entry.lang === language; });
    const label = component || 'Proper';
    if (!row || !(report.counts && report.counts.occurrences)) {
      return label + ' text coverage has not been assessed for this selection.';
    }
    const witness = witnessId && (row.witnesses || []).find(function (entry) {
      return entry.id === witnessId || (entry.aliases || []).indexOf(witnessId) >= 0;
    });
    const parts = [label + ' coverage in ' + languageName(language) + ': ' + row.available_targets + ' of ' +
      row.targets + ' represented distinct texts available (' + row.available + ' of ' + row.occurrences + ' uses).'];
    if (!row.occurrences) parts.splice(0, 1, 'This represented selection has no composed ' + label.toLowerCase() + ' bodies.');
    if (witnessId) parts.push('Selected witness: ' + (witness ? witness.label : witnessId) + ' — ' +
      (witness ? witness.available : 0) + ' of ' + row.occurrences + ' uses; gaps remain explicit.');
    parts.push(row.exact_target + ' uses have verified target wording across available witnesses.');
    if (witness) parts.push('Witness relationship: ' + (witness.relationships || []).map(function (value) {
      return COVERAGE_RELATIONSHIPS[value] || value;
    }).join(', ') + '; publication basis: ' + (witness.publication_bases || []).join(', ') + '.');
    const relationships = Object.keys(row.relationships || {}).filter(function (value) {
      return value !== 'exact-target' && row.relationships[value] > 0;
    });
    if (relationships.length) parts.push(relationships.map(function (value) {
      return row.relationships[value] + ' ' + (COVERAGE_RELATIONSHIPS[value] || value);
    }).join('; ') + '.');
    const counts = bibleUseCounts(row);
    if (counts.reconstructions) parts.push(counts.reconstructions +
      ' Scripture uses are Bible reconstructions, which do not establish exact Missal wording.');
    if (counts.beside) parts.push(counts.beside +
      ' Missal texts also show their cited passages in the selected Bible, which are not the Missal’s wording.');
    return parts.join(' ');
  }

  function coverageNoticeText(report, language, witnessId, component) {
    const row = report && (report.languages || []).find(function (entry) { return entry.lang === language; });
    if (!row || !(report.counts && report.counts.occurrences)) {
      return (component || 'Proper') + ' coverage not assessed for this selection.';
    }
    const witness = witnessId && (row.witnesses || []).find(function (entry) {
      return entry.id === witnessId || (entry.aliases || []).indexOf(witnessId) >= 0;
    });
    const available = witnessId ? witness ? witness.available : 0 : row.available;
    const texts = witnessId ? witness ? witness.available_targets : 0 : row.available_targets;
    if (!row.occurrences) return row.scripture_occurrences +
      ' Bible reconstructions; exact Missal wording is not established.';
    const parts = [languageName(language) + ' ' + (component || 'Propers') + ': ' + texts + '/' + row.targets +
      ' represented texts, ' + available + '/' + row.occurrences + ' uses available' +
      (witnessId ? ' from the selected witness' : '') + '.'];
    if (witnessId ? !witness || available < row.occurrences ||
        (witness.relationships || []).some(function (value) { return value !== 'exact-target'; })
      : row.exact_target < row.occurrences) parts.push('Exact target wording remains incomplete.');
    const counts = bibleUseCounts(row);
    if (counts.reconstructions) parts.push(counts.reconstructions + ' Bible reconstructions.');
    if (counts.beside) parts.push(counts.beside + ' cited Bible passages beside Missal texts.');
    return parts.join(' ');
  }

  /**
   * A `mixed` unit's citation expansion stands beside the Missal's own text
   * and is not a reconstruction of it; only a Scripture-only unit is. The two
   * are counted apart so the notice agrees with each unit's own claim.
   */
  function bibleUseCounts(row) {
    const beside = Math.min(row.mixed_occurrences || 0, row.scripture_occurrences || 0);
    return { reconstructions: (row.scripture_occurrences || 0) - beside, beside: beside };
  }

  /**
   * The recension caveat both entrances state, from the structure's public
   * `recension_coverage`, `stands_before`, and the Mass's `recension` stamp.
   * `editionName` maps a calendar id to its edition label.
   */
  function recensionContext(structure, mass, editionName) {
    const name = typeof editionName === 'function' ? editionName : function (id) { return id; };
    const label = function (value) {
      const held = typeof value === 'string' ? value.trim() : '';
      return held ? held.charAt(0).toUpperCase() + held.slice(1) : null;
    };
    const boundaries = structure && Array.isArray(structure.stands_before)
      ? structure.stands_before.filter(function (id) {
        return typeof id === 'string' && id;
      }) : [];
    const candidate = structure && structure.recension_coverage;
    const coverage = candidate && typeof candidate === 'object' && !Array.isArray(candidate)
      ? candidate : null;
    const domains = coverage && coverage.domains && typeof coverage.domains === 'object'
      ? coverage.domains : {};
    const properDomain = domains.propers && typeof domains.propers === 'object'
      ? domains.propers : {};
    const inheritance = coverage && coverage.inheritance &&
      typeof coverage.inheritance === 'object' ? coverage.inheritance : {};
    const stamp = mass && mass.recension && typeof mass.recension === 'object'
      ? mass.recension : null;
    if (!coverage && !stamp && !boundaries.length) return null;
    const sourceId = stamp && typeof stamp.text_from === 'string' && stamp.text_from
      ? stamp.text_from : null;
    const additional = stamp && Array.isArray(stamp.also) ? stamp.also.filter(function (row) {
      return row && typeof row === 'object' && typeof row.kind === 'string' && row.kind;
    }) : [];
    const coverageStatus = coverage && coverage.status || null;
    const properStatus = properDomain.state || null;
    const inheritanceStatus = inheritance.status || null;
    const inheritanceSource = inheritance.source_calendar || null;
    const coverageLabel = [
      coverageStatus && label(coverageStatus) + ' finding aid',
      properStatus && 'Propers: ' + label(properStatus),
      coverage && coverage.as_of && 'as of ' + coverage.as_of
    ].filter(Boolean).join(' · ') || null;
    const notice = [
      coverageStatus && 'This edition surface is a ' + coverageStatus +
        ' finding aid; recension coverage is dated ' + (coverage.as_of || 'without an as-of date') + '.',
      properStatus && 'Proper wording coverage is ' + properStatus + '.',
      inheritanceStatus && 'Inherited material' +
        (inheritanceSource ? ' from ' + name(inheritanceSource) : '') +
        ' remains ' + inheritanceStatus + '.'
    ].filter(Boolean).join(' ') || null;
    return {
      coverage: coverageLabel,
      coverageAsOf: coverage && coverage.as_of || null,
      coverageBasis: properDomain.basis || null,
      inheritanceBasis: inheritance.basis || null,
      notice: notice,
      textSource: sourceId
        ? name(sourceId) + ' · inherited ' + (inheritanceStatus || 'uncollated')
        : (stamp && stamp.stated === true
          ? 'Departure stated by this recension; no other calendar supplies this formulary'
          : null),
      departure: stamp && stamp.kind || null,
      departureAct: stamp && stamp.act || null,
      departureBasis: stamp && stamp.basis || null,
      additional: additional,
      boundaries: boundaries,
      boundaryLabel: boundaries.length ? boundaries.join('; ') : null,
      sourceId: sourceId
    };
  }

  function coverageWitnessMatches(owner, language, requested, translation) {
    const actual = translation.source_id || translation.source || '';
    if (requested === actual || requested === 'project-created' && !actual) return true;
    const entry = owner.coverage && (owner.coverage.languages || []).find(function (row) { return row.lang === language; });
    return Boolean(entry && (entry.witnesses || []).some(function (row) {
      return (row.id === requested || (row.aliases || []).indexOf(requested) >= 0) &&
        (row.id === actual || (row.aliases || []).indexOf(actual) >= 0);
    }));
  }

  function coverageWitnessIdentity(owner, language, translation) {
    const actual = translation.source_id || translation.source || '';
    const entry = owner.coverage && (owner.coverage.languages || []).find(function (row) { return row.lang === language; });
    const witness = entry && (entry.witnesses || []).find(function (row) {
      return row.id === actual || (row.aliases || []).indexOf(actual) >= 0;
    });
    return witness ? witness.id : actual || 'project-created';
  }

  /* ------------------------------------------------------------------------
   * ℣ and ℟
   *
   * The versicle and the response have their own marks, and a book with no
   * sort for them prints "V." and "R." instead. The artifacts hold what the
   * book prints, and they are the things that carry the hashes, so THE
   * SUBSTITUTION IS MADE HERE, at the moment of setting, and never in the
   * record. Nothing upstream is edited to suit a stylesheet.
   *
   * THE RULE IS DELIBERATELY NARROW, BECAUSE THE WIDE ONE IS WRONG. Every
   * single "V." in the 1861 Ordinary — all four of them — is the V of
   * "the B. V. M.", the Blessed Virgin Mary, and not one is a versicle;
   * "P. Com." is a Post Communion. A blanket replacement would have set all
   * four as ℣, produced something that reads correctly, and been wrong every
   * time. So a letter is a mark only where it OPENS A CLAUSE — at the start of
   * the text, or after sentence or clause punctuation — and never where the
   * token in front of it is itself a single letter and a point, which is what
   * an initial in a name looks like.
   *
   * "P." IS LEFT EXACTLY AS THE BOOK PRINTS IT, and that is not an oversight
   * either. It marks the priest and not the versicle, and the two part company:
   * at the server's Misereatur the 1861 book prints "R. May Almighty God be
   * merciful to thee … P. Amen.", where the priest's line IS the response.
   * Setting every "P." as ℣ would have made the respondent the versicler at
   * that place and at every other place like it. There is no glyph for "the
   * priest", so there is nothing here to substitute, and the book stands.
   * --------------------------------------------------------------------- */

  const VERSICLE_MARKS = { V: '℣', R: '℟' };
  const VERSICLE_NAMES = { V: 'Versicle.', R: 'Response.' };

  const VERSICLE_CANDIDATE = /([VR])(?:\/\.?|\.)(?=\s|$)|([℣℟])\.?(?=\s|$)/g;
  const PRINTED_ROLE_LETTERS = { '℣': 'V', '℟': 'R' };
  // Start of text; after sentence or clause punctuation; at the head of a line,
  // whatever ended the one above — liturgical verse is set a colon to the line
  // and most lines end in no punctuation at all; and just inside a bracket,
  // which is how the Exsultet prints the dialogue a deacon may omit.
  const OPENS_A_CLAUSE = /(^|[.;:,!?)\]"'’”—-]\s+|\n\s*|[([]\s*)$/;
  const AN_INITIAL_BEFORE = /(^|[\s(])[A-Za-z]\.\s+$/;

  /** One mark, named for a reader who cannot see it. */
  function versicleMark(letter) {
    const node = el('span', 'vr-mark');
    // ℣ and ℟ are announced as nothing at all by most screen readers, and as
    // "V" and "R" by the rest, so the word is given beside the glyph and the
    // glyph is taken away from the reading.
    const glyph = el('span', 'vr-glyph', VERSICLE_MARKS[letter]);
    glyph.setAttribute('aria-hidden', 'true');
    node.appendChild(glyph);
    const label = el('span', 'visually-hidden', VERSICLE_NAMES[letter]);
    label.lang = 'en';
    node.appendChild(label);
    return node;
  }

  /** Where the versicle and response marks fall in a whole text. */
  function versicleMarksIn(source) {
    const marks = [];
    let found;
    VERSICLE_CANDIDATE.lastIndex = 0;
    while ((found = VERSICLE_CANDIDATE.exec(source)) !== null) {
      const before = source.slice(0, found.index);
      if (!OPENS_A_CLAUSE.test(before) || AN_INITIAL_BEFORE.test(before)) continue;
      marks.push({ start: found.index, end: found.index + found[0].length,
        letter: found[1] || PRINTED_ROLE_LETTERS[found[2]] });
    }
    return marks;
  }

  /** One stretch [from, to); `lineStart` survives inline rubric splits. */
  function appendVersicled(target, source, from, to, marks, lineStart) {
    const opening = lineStart === undefined ? from : lineStart;
    let at = from;
    marks.forEach(function (mark) {
      if (mark.start < from || mark.end > to) return;
      if (mark.start > at) target.appendChild(document.createTextNode(source.slice(at, mark.start)));
      // The source explicitly opens another versicle or response here. Give
      // it a line of its own even when the artifact stores the exchange in
      // one paragraph. Hard wraps and P./R. speaker letters create no turns.
      if (source.slice(opening, mark.start).trim()) target.appendChild(el('br'));
      target.appendChild(versicleMark(mark.letter));
      at = mark.end;
    });
    if (at < to) target.appendChild(document.createTextNode(source.slice(at, to)));
  }

  /** A text with its versicle and response marks set, as a fragment. */
  function versicled(text) {
    const fragment = document.createDocumentFragment();
    const source = text === null || text === undefined ? '' : String(text);
    appendVersicled(fragment, source, 0, source.length, versicleMarksIn(source));
    return fragment;
  }

  /* ------------------------------------------------------------------------
   * Who is speaking
   *
   * The 1861 book mixes two axes.
   * `P.` marks the PRIEST — a person. `R.` marks a RESPONSE — a position in a
   * dialogue, whoever makes it. They are not two values of one thing, and the
   * book prints them in one column as though they were:
   *
   *   priest   P. I confess to Almighty God, &c.
   *   server   R. May Almighty God be merciful to thee…
   *   server   R. I confess to Almighty God…
   *   priest   P. May Almighty God be merciful unto you…
   *
   * In the fourth row the priest's `P.` line IS the response to the server. So
   * setting every `P.` as ℣ would put "versicle" over a response — and in two
   * rubric elements `P.` is not a speaker mark at all but an abbreviation
   * inside running text ("is said the P. COMMUNION"). A printed R. names a
   * response; a printed P. must never be recast as a versicle.
   *
   * Where reviewed child rows exist their speaker and dialogue_role supply
   * each cue. Otherwise a marked element may hold a two-party dialogue inside one
   * element — "P. The Lord be with you. R. And with thy spirit." carries
   * `speaker: priest`, which names the first line only. Drop every mark and the
   * server's responses are printed as the priest's words. Only a leading P.
   * that repeats the declared priest is removed. Each existing marked change
   * starts its own line; source hard wraps create no additional turns.
   *
   * Nothing upstream is edited: the artifacts keep what the book prints.
   * --------------------------------------------------------------------- */

  const SPEAKER_WORDS = { priest: 'Priest', server: 'Server', all: 'All' };
  const SPEAKER_CUES = { priest: 'P', server: 'S', all: 'All' };
  const DIALOGUE_ROLE_WORDS = { versicle: 'Versicle', response: 'Response' };
  const DIALOGUE_ROLE_CUES = { versicle: '℣', response: '℟' };
  const MARK_WORDS = { 'P.': 'Priest', 'R.': 'Response' };
  // Only where a mark can be a speaker at all. A rubric is printed matter about
  // the Mass, not words said in it, and it is where both false positives live.
  const SPOKEN_KINDS = { dialogue: true, prayer: true, form: true };
  const A_MARK = /(^|[.;:,!?)\]"'’”]\s+|\n\s*)(P\.|R(?:\/\.?|\.)|℟\.?)(?=\s|$)/g;

  function speakerTag(word, speaker, opening) {
    const tag = el(
      'span',
      'speaker-tag' + (speaker ? ' is-' + speaker : '') + (opening ? ' is-opening-cue' : '')
    );
    if (!opening) {
      // The label is an English word set inside a text that may be Latin;
      // without its own language it is announced with Latin pronunciation.
      tag.lang = 'en';
      tag.textContent = word;
      return tag;
    }

    // This cue comes only from the element's structured `speaker` field. It is
    // presentation furniture, not another word of the Ordinary; keep the full
    // identity for assistive technology and the compact role mark for sighted
    // readers. Interior P./R. marks remain untouched because they are held in
    // opaque prose and are not trustworthy turn boundaries.
    tag.setAttribute('data-presentation-only', 'speaker-cue');
    tag.lang = 'en';
    tag.appendChild(el('span', 'visually-hidden', word));
    const mark = el('span', 'cue-mark');
    mark.setAttribute('data-cue', SPEAKER_CUES[speaker] || word);
    mark.setAttribute('aria-hidden', 'true');
    tag.appendChild(mark);
    return tag;
  }

  /** One explicit turn cue, with one accessible label and no spoken glyph. */
  function structuredTurnCue(turn) {
    if (turn.action === true || turn.gloss === true) return null;
    const speakerWord = SPEAKER_WORDS[turn.speaker] || null;
    // A checked printed R./V. is evidence for its own typographic sign even
    // when the target edition's dialogue_role has not been classified. This
    // normalizes only a declared, matching source marker; it assigns no role
    // to a speaker, and never turns the priest's P. into a versicle.
    const printed = turnBody(turn).marker;
    const letter = printed && /^(?:V|R)(?:\/\.?|\.)$/.test(printed)
      ? printed.charAt(0) : PRINTED_ROLE_LETTERS[printed && printed.replace(/\.$/, '')] || null;
    const roleWord = DIALOGUE_ROLE_WORDS[turn.dialogue_role] ||
      (letter ? VERSICLE_NAMES[letter].replace(/\.$/, '') : null);
    const visible = DIALOGUE_ROLE_CUES[turn.dialogue_role] ||
      (letter ? VERSICLE_MARKS[letter] : null) ||
      SPEAKER_CUES[turn.speaker] || null;
    if (!visible || (!speakerWord && !roleWord)) return null;

    // Dialogue role and speaker are independent axes. A priest may answer and
    // a server may initiate, so the explicit role chooses only the visible
    // ℣/℟ mark while the single accessible label retains both held facts.
    const fullLabel = roleWord && speakerWord
      ? roleWord + ' — ' + speakerWord
      : roleWord || speakerWord;
    const tag = el(
      'span',
      'speaker-tag is-opening-cue ordinary-turn-cue' +
        (turn.speaker ? ' is-' + turn.speaker : '')
    );
    tag.setAttribute('data-presentation-only', 'speaker-cue');
    tag.lang = 'en';
    tag.appendChild(el('span', 'visually-hidden', fullLabel));
    const mark = el('span', 'cue-mark');
    mark.setAttribute('data-cue', visible);
    if (DIALOGUE_ROLE_CUES[turn.dialogue_role] || letter) {
      mark.setAttribute('data-dialogue-mark', 'true');
    }
    mark.setAttribute('aria-hidden', 'true');
    tag.appendChild(mark);
    return tag;
  }

  /**
   * A turn's spoken matter, apart from the book's own printed head letter.
   *
   * `printed_marker` is a reviewed inventory declaration, validated by the
   * generator: the row is exactly that marker, one space, then spoken text. The
   * structured cue already says who speaks or which side of the dialogue this
   * is, so the printed letter would be a second visible cue on one turn. It is
   * kept on the row as data, never re-read as a speaker or a role, and if the
   * declaration does not fit the text the row is shown exactly as printed.
   */
  function turnBody(turn) {
    const text = String(turn.text === null || turn.text === undefined ? '' : turn.text);
    const marker = typeof turn.printed_marker === 'string' ? turn.printed_marker : '';
    if (!marker || !text.startsWith(marker + ' ') || text.length <= marker.length + 1) {
      return { marker: null, body: text };
    }
    return { marker: marker, body: text.slice(marker.length + 1) };
  }

  /** Exact source-owned turns inside one Ordinary element and semantic event. */
  function structuredTurns(held, locus) {
    const body = el('div', 'composed ordinary-dialogue');
    body.lang = held.lang;
    if (locus) body.appendChild(el('span', 'ordinary-locus', locus));

    for (const turn of held.turns) {
      const action = turn.action === true;
      const gloss = turn.gloss === true;
      const row = el('p', 'ordinary-turn' + (action ? ' is-action' : '') + (gloss ? ' is-gloss' : ''));
      if (gloss) {
        row.setAttribute('data-gloss', 'true');
        row.setAttribute('role', 'note');
        row.setAttribute('aria-label', 'Source translation');
      }
      if (turn.speaker) row.setAttribute('data-speaker', turn.speaker);
      if (turn.dialogue_role) {
        row.setAttribute('data-dialogue-role', turn.dialogue_role);
      }
      if (action) row.setAttribute('data-action', 'true');

      // One visible cue per turn. Only where the structured cue is set does the
      // printed letter step aside; a turn with no structured cue keeps it.
      const cue = structuredTurnCue(turn);
      const spokenPart = cue ? turnBody(turn) : { marker: null, body: turn.text };
      if (cue) row.appendChild(cue);
      if (spokenPart.marker) row.setAttribute('data-printed-marker', spokenPart.marker);
      const text = el('span', 'ordinary-turn-text', spokenPart.body);
      text.lang = held.lang;
      row.appendChild(text);
      body.appendChild(row);
    }
    return body;
  }

  /**
   * One element's words, with every change of speaker made plain.
   *
   * Returns a fragment. The element's own speaker opens it; a mark inside the
   * text opens each further turn.
   */
  function spoken(element, text) {
    const source = String(text === null || text === undefined ? '' : text);
    if (!SPOKEN_KINDS[element.kind]) return document.createTextNode(source);

    const fragment = document.createDocumentFragment();
    // `all` is frequently attached to a composite element whose first turn is
    // the priest (for example the postconciliar Greeting). Without structured
    // turns it is not an honest opening cue, so do not present it as one. And
    // because nothing then announces the opening speaker, a leading P./R. is
    // not furniture there: it is the only attribution the first line has, and
    // it is kept like an interior mark (the Preface dialogue, the Pax).
    const opening = element.speaker !== 'all'
      ? SPEAKER_WORDS[element.speaker] || null
      : null;
    if (opening) {
      fragment.appendChild(speakerTag(opening, element.speaker, true));
    }

    // Explicit V./R. marks already name their dialogue roles. Use the same
    // setting as a Proper; a hard wrap or an unmarked speaker creates no turn.
    if (versicleMarksIn(source).some(function (mark) { return mark.letter === 'V'; })) {
      fragment.appendChild(versicled(source));
      return fragment;
    }

    let at = 0;
    let found;
    let first = true;
    let droppedLast = false;
    A_MARK.lastIndex = 0;
    while ((found = A_MARK.exec(source)) !== null) {
      const response = /^[R℟]/.test(found[2]);
      const word = MARK_WORDS[response ? 'R.' : 'P.'];
      const start = found.index + found[1].length;
      if (AN_INITIAL_BEFORE.test(source.slice(0, start))) continue;
      // A priest's leading letter may repeat the declared speaker. A response
      // mark retains its independent role even when the speaker is known.
      const leading = first && source.slice(0, start).trim() === '';
      first = false;
      if (leading && opening && found[2] === 'P.') {
        at = start + found[2].length;
        droppedLast = true;
        continue;
      }
      // The source's R. explicitly names a response; P. names only the
      // priest. Keep those independent axes and the existing marked boundary.
      if (start > at) {
        fragment.appendChild(document.createTextNode(source.slice(at, start)));
      }
      if (source.slice(0, start).trim()) fragment.appendChild(el('br'));
      fragment.appendChild(response
        ? versicleMark('R') : speakerTag(word, 'priest'));
      at = start + found[2].length;
      droppedLast = false;
    }
    // The space after a DROPPED mark was that mark's own spacing, and left in
    // place it opened the turn with a double space. The space after a KEPT
    // word label separates the label from the words, exactly as it does for
    // every interior turn above; stripping it here glued the last label to its
    // text in copied and announced text ("ResponseEt cum spiritu tuo.").
    const rest = source.slice(at);
    const tail = droppedLast ? rest.replace(/^[ \t]+/, '') : rest;
    if (tail) fragment.appendChild(document.createTextNode(tail));
    return fragment;
  }

  /** The Ordinary's words, shared by the browser and terminal readers. */
  function ordinaryText(element, held, locus) {
    if (Array.isArray(held.turns) && held.turns.length) return structuredTurns(held, locus);
    const body = el('p', element.kind === 'heading' ? 'ordinary-head' : 'composed');
    if (locus) body.appendChild(el('span', 'ordinary-locus', locus));
    body.appendChild(spoken(element, held.text));
    body.lang = held.lang;
    return body;
  }

  /* ------------------------------------------------------------------------
   * Checked internal structure (C2 gap G14)
   *
   * `text_structure` is the generator's projection of a body's checked
   * stanza boundaries and typed inline actions, as offsets into the exact
   * published string (`guidance/web-data.md`). The words are never edited to
   * carry it: a stanza is a group of the text's own characters, and a rubric
   * printed inside a prayer -- the Pentecost genuflection -- is set as a rubric
   * span, not spoken text. A structure that does not fit its text is ignored
   * whole rather than half applied.
   * --------------------------------------------------------------------- */

  function usableStructure(text, structure) {
    if (!structure || typeof structure !== 'object') return null;
    const length = text.length;
    const stanzas = Array.isArray(structure.stanzas) ? structure.stanzas : [];
    const actions = Array.isArray(structure.actions) ? structure.actions : [];
    const ordered = stanzas.every(function (offset, index) {
      return Number.isInteger(offset) && offset >= 0 && offset < length &&
        (index === 0 ? offset === 0 : offset > stanzas[index - 1]);
    });
    let last = -1;
    const spans = actions.every(function (action) {
      const fits = action && action.kind === 'rubric' && Number.isInteger(action.start) &&
        Number.isInteger(action.end) && action.start > last && action.end > action.start &&
        action.end <= length;
      if (fits) last = action.end - 1;
      return fits;
    });
    if (!ordered || !spans || (!stanzas.length && !actions.length)) return null;
    return { stanzas: stanzas, actions: actions };
  }

  /** One rubric printed inside the text, set as a rubric and named once. */
  function inlineRubric(source, action, marks) {
    const node = el('span', 'inline-rubric');
    node.setAttribute('data-inline-action', action.kind);
    // Assistive technology is told what the italic and the red say; the
    // label is English interface text inside a paragraph of the text's own
    // language, so it carries its own `lang`.
    const label = el('span', 'visually-hidden', 'Rubric: ');
    label.lang = 'en';
    node.appendChild(label);
    appendVersicled(node, source, action.start, action.end, marks);
    return node;
  }

  /** Append [from, to) of the text, with its rubric spans, to `target`. */
  function appendStructured(target, source, from, to, actions, marks) {
    let at = from;
    actions.forEach(function (action) {
      if (action.start < from || action.end > to) return;
      appendVersicled(target, source, at, action.start, marks, from);
      target.appendChild(inlineRubric(source, action, marks));
      at = action.end;
    });
    appendVersicled(target, source, at, to, marks, from);
  }

  /**
   * The composed element for a body: a paragraph, or, where checked stanza
   * boundaries are recorded, a group whose stanzas are paragraphs of their
   * own. Either way the element carries the `composed` class, the language,
   * and the label as its first child, so every consumer reads one shape.
   */
  function composedBody(text, structure, label) {
    const source = String(text);
    const usable = usableStructure(source, structure);
    const marks = versicleMarksIn(source);
    const stanzas = usable && usable.stanzas.length > 1 ? usable.stanzas : null;
    const node = el(stanzas ? 'div' : 'p', stanzas ? 'composed composed-stanzas' : 'composed');
    if (label) node.appendChild(label);
    const actions = usable ? usable.actions : [];
    if (!stanzas) {
      appendStructured(node, source, 0, source.length, actions, marks);
      return node;
    }
    node.setAttribute('data-stanzas', String(stanzas.length));
    stanzas.forEach(function (start, index) {
      const end = index + 1 < stanzas.length ? stanzas[index + 1] : source.length;
      const stanza = el('p', 'stanza');
      appendStructured(stanza, source, start, end, actions, marks);
      // A boundary sits after whitespace; that whitespace is the gap the
      // stanza break already shows.
      const tail = stanza.lastChild;
      if (tail && tail.nodeType === 3) tail.nodeValue = tail.nodeValue.replace(/\s+$/, '');
      node.appendChild(stanza);
    });
    return node;
  }

  /* ------------------------------------------------------------------------
   * Copying from the reader
   *
   * What a reader copies is the text they see: the ℣ and ℟ glyphs, the words,
   * a rubric printed in the text, and a stanza or paragraph break where one is
   * shown. Not the labels written for assistive technology ("Verse 7.",
   * "Versicle."), and not the reader's apparatus lines about the text. The
   * browser's own serialisation gets both wrong -- the glyph sits in an
   * unselectable cue and the hidden words sit in selectable spans -- so the
   * plain-text flavour is written here from the selection itself.
   * --------------------------------------------------------------------- */

  const COPY_SKIP = '.visually-hidden, .verse-num, .composed-label, .unit-claim, ' +
    '.citation-numbering, [data-copy="skip"], button, select, input, textarea, ' +
    'script, style, template, svg';
  const PARAGRAPH_BLOCKS = new Set(['P', 'BLOCKQUOTE']);
  // The Ordinary's dialogue rows set their cue in generated content and copy
  // their accessible speaker label in its place; that is the Ordinary
  // renderer's own contract, so a selection reaching one is left to the
  // browser rather than serialised by these rules.
  const COPY_DEFERS = '.ordinary-dialogue, .ordinary-turn, .speaker-tag, .cue-mark';

  const DEFER = {};

  function copyText(range) {
    let text = '';
    function newlines(count) {
      if (!text) return;
      const trailing = /\n*$/.exec(text)[0].length;
      if (trailing < count) text = text.replace(/ +$/, '') + '\n'.repeat(count - trailing);
    }
    function walk(node) {
      if (!range.intersectsNode(node)) return;
      if (node.nodeType === 3) {
        let value = node.nodeValue;
        if (node === range.endContainer) value = value.slice(0, range.endOffset);
        if (node === range.startContainer) value = value.slice(range.startOffset);
        value = value.replace(/\s+/g, ' ');
        if (!text || /\s$/.test(text)) value = value.replace(/^ /, '');
        text += value;
        return;
      }
      if (node.nodeType !== 1) return;
      if (node.matches(COPY_DEFERS)) throw DEFER;
      if (node.matches(COPY_SKIP) || node.hidden) return;
      const style = getComputedStyle(node);
      if (style.display === 'none' || style.visibility === 'hidden') return;
      const parentStyle = node.parentElement ? getComputedStyle(node.parentElement) : null;
      const block = !/^inline/.test(style.display) || node.tagName === 'BR';
      const lines = PARAGRAPH_BLOCKS.has(node.tagName) ? 2 : 1;
      if (block) newlines(lines);
      else if (parentStyle && /flex|grid/.test(parentStyle.display) && text && !/\s$/.test(text)) {
        // Flex items -- a heading's name beside its reference -- are laid
        // out apart, so they are copied apart.
        text += ' ';
      }
      if (node.tagName === 'BR') return;
      node.childNodes.forEach(walk);
      if (block) newlines(lines);
    }
    try {
      const anchor = range.commonAncestorContainer;
      const element = anchor.nodeType === 1 ? anchor : anchor.parentElement;
      if (element && element.closest(COPY_DEFERS)) return null;
      walk(anchor);
    } catch (error) {
      if (error === DEFER) return null;
      throw error;
    }
    return text.replace(/[ \t]+\n/g, '\n').replace(/\n{3,}/g, '\n\n').trim();
  }

  function onReaderCopy(event) {
    const selection = document.getSelection && document.getSelection();
    if (!selection || selection.isCollapsed || !selection.rangeCount || !event.clipboardData) return;
    const range = selection.getRangeAt(0);
    const anchor = range.commonAncestorContainer;
    const element = anchor.nodeType === 1 ? anchor : anchor.parentElement;
    const inside = element && element.closest('.reader-document');
    const around = element && element.querySelector && element.querySelector('.reader-document');
    if (!inside && !around) return;
    const text = copyText(range);
    if (!text) return;
    event.clipboardData.setData('text/plain', text);
    event.preventDefault();
  }

  if (typeof document !== 'undefined' && document.addEventListener) {
    document.addEventListener('copy', onReaderCopy);
  }

  /**
   * The composed text to show, and what to say about it.
   *
   * A proper with no translation in the chosen language is the ordinary case,
   * not an error — but it must not silently fall back to Latin and let the
   * reader believe they are looking at the English they asked for. The absence
   * is stated where the text would have been.
   */
  function properBodyUnavailable(proper) {
    const status = proper && proper.text_status;
    return Boolean(status && status.state === 'unavailable' &&
      status.scope === 'proper-body');
  }

  function orationFor(proper, wanted, witness) {
    const asked = wanted || SOURCE_LANGUAGE;
    if (asked === SOURCE_LANGUAGE) {
      if (proper.latin && proper.latin.withheld) {
        return {
          text: null, lang: SOURCE_LANGUAGE, missing: true, wanted: asked,
          source: null, availability: 'unavailable', reason: 'latin-withheld',
          unavailableState: ['rights-restricted', 'unavailable'].includes(proper.latin.state)
            ? proper.latin.state : 'unavailable',
          held: false
        };
      }
      if (properBodyUnavailable(proper)) {
        return {
          text: null, lang: SOURCE_LANGUAGE, missing: true, wanted: asked,
          source: null, availability: 'unavailable', reason: 'latin-unavailable',
          unavailableState: 'unavailable', held: false
        };
      }
      return {
        text: proper.text, lang: SOURCE_LANGUAGE, missing: false, source: null,
        structure: proper.text_structure || null
      };
    }
    const rawCandidates = (proper.translations || []).filter((translation) => {
      return translation && translation.lang === asked && translation.text;
    });
    const grouped = new Map();
    const conflicts = new Set();
    rawCandidates.forEach(function (translation) {
      const id = coverageWitnessIdentity(proper, asked, translation);
      if (grouped.has(id) && grouped.get(id).text !== translation.text) conflicts.add(id);
      else grouped.set(id, translation);
    });
    const candidates = Array.from(grouped.values());
    if (candidates.some(function (translation) {
      return conflicts.has(coverageWitnessIdentity(proper, asked, translation)) &&
        (!witness || coverageWitnessMatches(proper, asked, witness, translation));
    })) return {
      text: null, lang: asked, missing: true, wanted: asked, source: null,
      availability: 'unavailable', reason: 'conflicting-witness', held: false
    };
    const found = witness
      ? candidates.find((translation) => {
          return coverageWitnessMatches(proper, asked, witness, translation);
        })
      : (candidates.length === 1 ? candidates[0] : null);
    if (found) {
      return {
        text: found.text,
        structure: found.text_structure || null,
        lang: asked,
        missing: false,
        source: found.source_id || found.source || null,
        sourceLabel: found.source_label || null,
        caution: found.caution || null,
        rights: found.rights || null,
        notice: found.notice || null
      };
    }
    if (!witness && candidates.length > 1) {
      return {
        text: null, lang: asked, missing: true, wanted: asked,
        source: null, availability: 'choice-required',
        reason: 'translation-choice-required', held: false
      };
    }
    const unavailable = (proper.unavailable_translations || []).concat(
      proper.untranslated || []
    ).find((translation) => {
      return translation && translation.lang === asked &&
        !(proper.source === 'scripture' && translation.target &&
          translation.target.extent === 'body' && !languageBodyTargetMatches(proper, translation));
    });
    if (unavailable && !(proper.translations || []).some((translation) => {
      return translation && translation.lang === asked && translation.text;
    })) {
      const state = unavailable.state || 'unavailable';
      const latinUnavailable = properBodyUnavailable(proper) && !proper.text;
      const blocksFallback = Boolean(witness) || state === 'rights-restricted' || latinUnavailable;
      return {
        text: blocksFallback ? null : (proper.text || null),
        lang: blocksFallback ? asked : SOURCE_LANGUAGE,
        missing: true,
        wanted: asked,
        source: null,
        availability: 'unavailable',
        reason: state === 'rights-restricted'
          ? state : (latinUnavailable ? 'text-unavailable' : state),
        unavailableState: state,
        held: false,
        extent: unavailable.target && unavailable.target.extent || null
      };
    }
    if (witness) return {
      text: null, lang: asked, missing: true, wanted: asked,
      source: null, availability: 'unavailable',
      reason: 'absent-in-witness', held: false
    };
    if (properBodyUnavailable(proper) && !proper.text) {
      return {
        text: null, lang: asked, missing: true, wanted: asked,
        source: null, availability: 'unavailable', reason: 'text-unavailable',
        unavailableState: 'unavailable', held: false
      };
    }
    return {
      text: proper.text,
      lang: SOURCE_LANGUAGE,
      missing: true,
      wanted: asked,
      source: null
    };
  }

  /* ------------------------------------------------------------------------
   * Claim-local truth
   *
   * Each displayed unit says locally what it is. The typed reasons are the
   * unit coverage record's own `availability` values, which are the vision's
   * five distinct absences; the page never parses prose to recover them, and a
   * unit without a coverage record falls back to the same public dispositions
   * `_missal_coverage.absence` derives that value from.
   * --------------------------------------------------------------------- */

  const ABSENCE_REASONS = Object.freeze({
    'inapplicable': 'not part of this rite or branch',
    'absent-in-witness': 'not present in this witness',
    'not-sourced': 'not yet sourced',
    'not-publishable': 'not publishable here',
    'unresolved': 'not resolved'
  });

  function unitCoverageOf(owner) {
    const unit = owner && owner.coverage;
    validateBodyLanguages(unit);
    return unit && unit.schema === 'triptych-missal-unit-coverage/v1' ? unit : null;
  }

  function typedAvailability(owner, lang) {
    const unit = unitCoverageOf(owner);
    const entry = unit && (unit.languages || []).find(function (row) { return row.lang === lang; });
    if (entry && Object.prototype.hasOwnProperty.call(ABSENCE_REASONS, entry.availability)) {
      return entry.availability;
    }
    if (lang === SOURCE_LANGUAGE) {
      return owner && owner.latin && owner.latin.state === 'rights-restricted'
        ? 'not-publishable' : 'unresolved';
    }
    const rows = [].concat(owner && owner.unavailable_translations || [],
      owner && owner.untranslated || []).filter(function (row) {
      return row && row.lang === lang;
    });
    if (rows.some(function (row) { return row.state === 'rights-restricted'; })) return 'not-publishable';
    return rows.length ? 'unresolved' : 'not-sourced';
  }

  /** "English translation unavailable: not publishable here (…)." */
  function absenceClause(owner, lang, scope) {
    const availability = typedAvailability(owner, lang);
    const subject = lang === SOURCE_LANGUAGE ? 'Latin text' : languageName(lang) + ' translation';
    return {
      lang: lang,
      availability: availability,
      text: subject + ' unavailable' + (scope ? ' ' + scope : '') + ': ' +
        ABSENCE_REASONS[availability] +
        (availability === 'not-publishable' ? ' (its use is rights restricted)' : '') + '.'
    };
  }

  /**
   * Whether the citation passages of this owner are Bible reconstructions.
   *
   * A citation is expanded from the selected Bible, which does not establish
   * the Missal's own wording (incipit, part-verse, adaptation, ending). The unit
   * coverage record says so as `bible-reconstruction`, on the unit itself or on
   * its `scripture_component`; only a unit with no record falls back to the
   * expansion itself.
   */
  function isBibleReconstruction(owner, fallbackOwner) {
    const unit = unitCoverageOf(owner) || unitCoverageOf(fallbackOwner);
    if (!unit) return true;
    if (unit.scripture_component) {
      return unit.scripture_component.relationship === 'bible-reconstruction';
    }
    return unit.component === 'scripture' && (unit.languages || []).some(function (row) {
      return row.relationship === 'bible-reconstruction';
    });
  }

  function reconstructionMarker() {
    const node = el('p', 'unit-claim', 'Bible reconstruction · Missal wording not established');
    node.setAttribute('data-unit-claim', 'bible-reconstruction');
    return node;
  }

  /**
   * The claim for citation passages set beneath the Missal's own text.
   *
   * A `mixed` unit prints the Missal's wording above and expands its citations
   * below. Those passages are then not a reconstruction standing in for the
   * Missal's words, which are shown; they are the cited text in the selected
   * Bible edition, and that is what the line says (C2 G9 follow-up).
   */
  function bibleTextMarker(bible) {
    const edition = bible && (bible.label || bible.id);
    const node = el('p', 'unit-claim',
      'Bible text' + (edition ? ' · ' + edition : '') + ' · not the Missal’s wording');
    node.setAttribute('data-unit-claim', 'bible-text');
    return node;
  }

  /** Which claim a unit's citation passages carry, given what was shown above. */
  function citationClaim(owner, fallbackOwner, source, missalTextShown, bible) {
    if (!isBibleReconstruction(owner, fallbackOwner)) return null;
    return source === 'mixed' && missalTextShown ? bibleTextMarker(bible) : reconstructionMarker();
  }

  /**
   * One owner's composed words and the claim-local account of what is absent.
   *
   * A requested translation that is missing never suppresses the held original:
   * the Latin stays visible, labelled as Latin, beside the exact typed absence of
   * the translation. No other witness of the translation is borrowed.
   */
  /** A readable petition, with its immutable historical ending in apparatus. */
  function renderExecutionSource(container, held) {
    const selected = held.executionSource;
    const source = selected.source;
    const range = source.ranges[0];
    const body = composedBody(source.source_text.slice(range.start, range.end), null,
      composedLabel('Historical English petition · dated RG110 execution source'));
    body.lang = 'en';
    body.setAttribute('data-execution-petition', source.record_sha256);
    container.appendChild(body);
    const apparatus = el('aside', 'execution-source-apparatus');
    apparatus.setAttribute('role', 'note');
    apparatus.setAttribute('data-copy', 'skip');
    apparatus.appendChild(el('p', 'composed-note', 'Historical human English; not approved for liturgical use. Only the petition is projected here; a translation of this whole prayer remains unavailable for this Missal.'));
    apparatus.appendChild(el('p', 'composed-note', 'Historical source: ' + source.source_label +
      '. Its printed ending belongs to the source witness; the appointed joint conclusion belongs to the companion. Any unbound English cue remains unresolved.'));
    const cue = source.ranges[2];
    apparatus.appendChild(el('p', 'composed-note historical-ending-cue',
      'Historical witness ending: ' + source.source_text.slice(cue.start, cue.end)));
    const details = el('details', 'execution-source-whole');
    details.appendChild(el('summary', 'composed-note', 'Complete historical English prayer'));
    details.appendChild(el('p', 'composed-note', source.source_text));
    apparatus.appendChild(details);
    container.appendChild(apparatus);
    if (selected.state === 'unresolved') {
      const note = el('p', 'composed-note unit-absence execution-source-unresolved',
        'Execution remains unresolved: ' + selected.unresolved.map(function (reason) {
          return {'companion-English-conclusion-unbound': 'the companion source prints no English ending cue',
            'source-name-placeholder-unbound': 'the source name placeholder is unbound',
            'companion-English-unavailable-in-selected-witness': 'the companion English is unavailable in the selected witness',
            'later-shared-conclusion-unbound': 'a later shared conclusion remains unbound'}[reason] || reason;
        }).join('; ') + '.');
      note.dataset.unitAbsence = 'unresolved:oration-execution';
      container.appendChild(note);
    }
    return {text: null, lang: 'en', shown: true, missing: false, source: source.source_id,
      sourceLabel: source.source_label, rights: 'public-domain', executionScoped: true};
  }

  /** Witness offers from selected, applied execution contexts, separate from body coverage. */
  function executionWitnesses(result, ordinaryChoices, language) {
    const choices = ordinaryChoices.slice();
    if (language !== 'en') return choices;
    const counts = new Map();
    const seen = new Set();
    function visit(event) {
      if (event.kind === 'proper-choice') {
        (event.options || []).filter(function (option) {
          return event.selection.state === 'selected' && option.id === event.selection.option;
        }).forEach(function (option) { (option.events || []).forEach(visit); });
      }
      if (event.executionSource && !seen.has(event.id)) {
        seen.add(event.id);
        const source = event.executionSource.source;
        if (!counts.has(source.source_id)) counts.set(source.source_id, {source: source, count: 0});
        counts.get(source.source_id).count++;
      }
      (event.orationGroups || []).forEach(function (group) { (group.members || []).forEach(visit); });
    }
    (result && result.events || []).forEach(visit);
    counts.forEach(function (row, id) {
      const existing = choices.find(function (choice) { return choice.id === id || (choice.aliases || []).indexOf(id) >= 0; });
      const label = row.count + ' execution-scoped source petitions';
      if (existing) existing.label += ' · ' + label;
      else choices.push({id: id, aliases: row.source.source_aliases, label: row.source.source_label + ' · ' + label,
        execution_sources: row.count, whole_body_translations_added: 0});
    });
    return choices;
  }

  function renderSingleOrationState(container, owner, held, scope, parentSource) {
    if (held.executionSource && held.orations === 'en') return renderExecutionSource(container, held);
    const asked = held.orations || SOURCE_LANGUAGE;
    const oration = orationFor(owner, asked, held.translationWitness || null);
    const latinHeld = Boolean(owner.text) && !(owner.latin && owner.latin.withheld);
    const original = !held.separateOriginal && !oration.text && oration.missing && asked !== SOURCE_LANGUAGE && latinHeld
      ? owner.text : null;
    const selectedText = held.separateOriginal && oration.missing ? null : oration.text;
    const shown = selectedText || original;
    const shownLang = selectedText ? oration.lang : SOURCE_LANGUAGE;
    // A Latin fallback is the owner's own text, and carries its structure;
    // a structure travels only with the exact words it was checked against.
    const structure = oration.text ? oration.structure : (owner.text_structure || null);
    if (shown) {
      // A `mixed` body is the Missal's own wording of a scriptural text, so it
      // is not labelled as a composition that is not scripture.
      const kind = (owner.source || parentSource) === 'mixed'
        ? 'Missal text' : 'Composed text — not scripture';
      const composed = composedBody(shown, structure, composedLabel(kind +
        (shownLang !== SOURCE_LANGUAGE ? ' · ' + languageName(shownLang)
          : (asked !== SOURCE_LANGUAGE ? ' · ' + languageName(SOURCE_LANGUAGE) : ''))));
      composed.lang = shownLang;
      if (shownLang === SOURCE_LANGUAGE && asked !== SOURCE_LANGUAGE) {
        composed.setAttribute('data-unit-original', SOURCE_LANGUAGE);
      }
      container.appendChild(composed);
      const context = shownLang === SOURCE_LANGUAGE && owner.latin && owner.latin.target_context;
      if (context && Object.keys(context).length === 3 &&
          context.scope === 'witness-state-only' && context.civil_date_authority === false &&
          typeof context.label === 'string' && context.label.trim() &&
          owner.latin.withheld === false &&
          owner.latin.publication && owner.latin.publication.status === 'permitted' &&
          ['public-domain', 'project-created', 'permission', 'licensed'].includes(owner.latin.publication.basis) &&
          owner.latin.provenance && owner.latin.provenance.status === 'collated' &&
          owner.latin.provenance.relationship === 'editorial-projection-exact-to-target') {
        const note = el('p', 'composed-note unit-witness-context',
          context.label + ' · checked witness wording; no date-specific pre-1955 attribution is established.');
        note.lang = 'en';
        note.setAttribute('data-target-witness-context', context.scope);
        container.appendChild(note);
      }
    }
    oration.shown = Boolean(shown);
    if (!oration.missing) return oration;

    // Said where the translation would have been, not in a footnote: a reader
    // who asked for English and is reading Latin needs to know that at the text.
    const sentences = [];
    const absences = [];
    function clause(lang) {
      const one = absenceClause(owner, lang, scope);
      sentences.push(one.text);
      absences.push(one.lang + ':' + one.availability);
    }
    const unit = scope ? 'cycle' : 'Proper';
    if (asked === SOURCE_LANGUAGE) {
      clause(SOURCE_LANGUAGE);
    } else if (oration.reason === 'conflicting-witness') {
      sentences.push('Conflicting readings of this witness remain unresolved; no translation was selected.');
    } else if (oration.reason === 'translation-choice-required') {
      sentences.push('Several ' + languageName(asked) +
        ' translations are held. Choose a witness before reading one.');
    } else if (oration.reason === 'absent-in-witness') {
      sentences.push('No ' + languageName(asked) +
        ' text is available from the selected witness for this ' + unit + '.');
      absences.push(asked + ':absent-in-witness');
    } else {
      clause(asked);
    }
    if (asked !== SOURCE_LANGUAGE && !held.separateOriginal) {
      if (shown && shownLang === SOURCE_LANGUAGE) sentences.push('The Latin original is shown.');
      else if (!latinHeld) clause(SOURCE_LANGUAGE);
    }
    const note = el('p', 'composed-note unit-absence', sentences.join(' '));
    if (absences.length) note.setAttribute('data-unit-absence', absences.join(' '));
    container.appendChild(note);
    return oration;
  }

  /** One labelled language side; metadata is passed from its source owner. */
  function textSide(language, metadata) {
    const facts = metadata || {};
    const side = el('section', 'text-side');
    side.setAttribute('data-text-language', language);
    ['sourceId', 'rights', 'relationship', 'availability'].forEach(function (key) {
      if (facts[key]) side.setAttribute('data-text-' + key.replace(/[A-Z]/g, function (one) {
        return '-' + one.toLowerCase();
      }), facts[key]);
    });
    const relation = COVERAGE_RELATIONSHIPS[facts.relationship] ||
      (facts.relationship === 'antecedent' ? 'historical antecedent' : facts.relationship);
    const label = el('p', 'text-side-label', [languageName(language), relation,
      facts.rights && String(facts.rights).replace(/-/g, ' '),
      facts.collation === 'uncollated' && 'uncollated'].filter(Boolean).join(' · '));
    label.lang = 'en';
    side.appendChild(label);
    return side;
  }

  // Presentation labels for the identified witnesses, not replacements for
  // their full source records. Unclassified witnesses retain every caution
  // inline; no sentence is shortened or discarded to meet a display budget.
  const TRANSLATION_PRESENTATIONS = {
    'edition.francis-xavier-lasance.the-new-roman-missal.benziger-revised-1945': {
      label: 'Lasance and Walsh, The New Roman Missal (1945 revision)',
      qualification: 'Historical lay translation; not approved for liturgical use. Its wording and recension may differ from the selected Missal.'
    },
    'edition.eugene-cummiskey.roman-missal-english-laity.philadelphia-1861': {
      label: 'The Roman Missal for the Laity (Cummiskey, 1861)',
      qualification: 'Historical lay translation; not approved for liturgical use. Its wording and recension may differ from the selected Missal.'
    },
    'edition.edward-caswall.lyra-catholica.london-1849': {
      label: 'Edward Caswall, Lyra Catholica (1849)',
      qualification: 'Metrical literary translation, not clause for clause. Stanza divisions may differ from the Latin; no Amen or Alleluia is rendered.'
    },
    'edition.hymns-ancient-and-modern-proprietors.hymns-ancient-and-modern.london-complete-edition-1890': {
      label: 'Hymns Ancient and Modern (1890), English attributed to W. J. Irons',
      qualification: 'Historical literary translation; this printing is not established as Irons’s own wording.'
    }
  };
  TRANSLATION_PRESENTATIONS['artifact.edward-caswall.lyra-catholica.london-1849.missal-sequences-en'] =
    TRANSLATION_PRESENTATIONS['edition.edward-caswall.lyra-catholica.london-1849'];
  TRANSLATION_PRESENTATIONS['artifact.hymns-ancient-and-modern-proprietors.hymns-ancient-and-modern.london-complete-edition-1890.dies-irae-irons-en'] =
    TRANSLATION_PRESENTATIONS['edition.hymns-ancient-and-modern-proprietors.hymns-ancient-and-modern.london-complete-edition-1890'];

  /** Exact source notes, available both beside the text and in terminal Study. */
  function translationCredits(oration, options) {
    const credits = el('div', 'translation-credits');
    const presentation = TRANSLATION_PRESENTATIONS[oration.source];
    if (oration.source) credits.appendChild(el('p', 'composed-note translation-credit',
      'Translation: ' + (presentation ? presentation.label : oration.sourceLabel || oration.source)));
    if (presentation && oration.caution) {
      credits.appendChild(el('p', 'composed-note translation-qualification', presentation.qualification));
      const details = el('details', 'translation-apparatus');
      if (options && options.expanded) details.setAttribute('open', '');
      details.appendChild(el('summary', 'composed-note', 'Translation source, differences and qualifications'));
      if (oration.sourceLabel) details.appendChild(el('p', 'composed-note', oration.sourceLabel));
      details.appendChild(el('p', 'composed-note', oration.caution));
      credits.appendChild(details);
    } else if (oration.caution) {
      credits.appendChild(el('p', 'composed-note translation-qualification', oration.caution));
    }
    // Required acknowledgements always travel verbatim with the words. They
    // never enter a closed disclosure, even for a classified public-domain source.
    if (oration.notice) credits.appendChild(el('p', 'composed-note translation-notice', oration.notice));
    return credits;
  }

  function orationCredits(container, oration) {
    if (oration.executionScoped) return;
    container.appendChild(translationCredits(oration));
  }

  function renderOrationState(container, owner, held, scope, parentSource) {
    const asked = held.orations || SOURCE_LANGUAGE;
    if (held.textDisplay !== 'latin-and-selected' || asked === SOURCE_LANGUAGE) {
      return renderSingleOrationState(container, owner, held, scope, parentSource);
    }
    const pair = el('div', 'text-pair');
    const coverage = unitCoverageOf(owner);
    const latin = orationFor(owner, SOURCE_LANGUAGE, null);
    const selected = orationFor(owner, asked, held.translationWitness || null);
    function metadata(lang, selection) {
      if (lang === 'en' && held.executionSource) return {sourceId: held.executionSource.source.source_id,
        rights: 'public-domain', relationship: 'execution-petition-only', availability: 'held'};
      const row = coverage && (coverage.languages || []).find(function (one) { return one.lang === lang; });
      const witness = row && (row.witnesses || []).find(function (one) {
        return one.id === selection.source || one.source_id === selection.source ||
          (one.aliases || []).includes(selection.source);
      });
      const original = lang === SOURCE_LANGUAGE && owner.latin || {};
      return {
        sourceId: selection.source || original.provenance && original.provenance.source_id,
        rights: selection.rights || original.publication && original.publication.basis,
        relationship: witness && witness.relationship || row && row.relationship,
        availability: selection.missing ? selection.availability || 'unavailable' :
          (selection.text ? 'held' : 'unavailable')
      };
    }
    const originalSide = textSide(SOURCE_LANGUAGE, metadata(SOURCE_LANGUAGE, latin));
    const originalResult = renderSingleOrationState(originalSide, owner,
      Object.assign({}, held, { orations: SOURCE_LANGUAGE, translationWitness: null }), scope, parentSource);
    if (!originalResult.shown && !originalResult.missing) {
      const absence = absenceClause(owner, SOURCE_LANGUAGE, scope);
      const note = el('p', 'composed-note unit-absence', absence.text);
      note.setAttribute('data-unit-absence', SOURCE_LANGUAGE + ':' + absence.availability);
      originalSide.appendChild(note);
    }
    const provenance = owner.latin && owner.latin.provenance;
    if (originalResult.shown && provenance && (provenance.source_date || provenance.source_id)) originalSide.appendChild(el('p', 'composed-note',
      'Latin source: ' + (provenance.source_date || provenance.source_id) +
      (provenance.verification_locator ? ' · ' + provenance.verification_locator : '')));
    const selectedSide = textSide(asked, metadata(asked, selected));
    const result = renderSingleOrationState(selectedSide, owner,
      Object.assign({}, held, { separateOriginal: true }), scope, parentSource);
    orationCredits(selectedSide, result);
    pair.appendChild(originalSide);
    pair.appendChild(selectedSide);
    container.appendChild(pair);
    result.creditsShown = true;
    result.shown = result.shown || originalResult.shown;
    return result;
  }

  function renderScriptureCitation(citation, bible, fragments, numbering, options, companion) {
    if (!companion) return renderCitation(citation, bible, fragments, numbering, options);
    const sameEdition = companion.bible.id === bible.id;
    const pair = el('div', sameEdition ? 'scripture-single' : 'text-pair scripture-pair');
    function side(edition, chapters) {
      const node = textSide(edition.language, { sourceId: edition.id, rights: edition.rights });
      node.classList.add('scripture-side');
      node.setAttribute('data-bible-edition', edition.id);
      node.setAttribute('data-bible-numbering', lociKey(edition));
      if (edition.edition) node.setAttribute('data-bible-witness', edition.edition);
      const label = el('p', 'text-side-label scripture-edition', bibleMeta(edition).join(' · '));
      node.appendChild(label);
      const body = el('div', 'text-side-body');
      body.appendChild(renderCitation(citation, edition, chapters, numbering, options));
      node.appendChild(body);
      return node;
    }
    // The citation is the common semantic fragment. Loci/verses inside each
    // side remain in that edition's own order and are never zipped together.
    pair.appendChild(side(companion.bible, companion.fragments));
    if (!sameEdition) pair.appendChild(side(bible, fragments));
    return pair;
  }

  /**
   * One proper, with its text.
   *
   *   options.numbering  the numbering the structure file's references are in
   *   options.orations   the language the composed propers are asked for
   *   options.heading    the level this proper's name sets at, default h3
   *
   * The level is an option because a proper is a top-level thing on the propers
   * page and a part of the Mass inside the Ordinary's frame, where the sections
   * of the rite stand above it. A page that set every heading at h3 whatever it
   * was nested in would tell a reader moving by headings that the Introit and
   * "The Priest at the Foot of the Altar" are peers, which they are not.
   */
  function renderProper(proper, bible, fragments, options) {
    const bundle = fragments && fragments.fragments ? fragments : null;
    const companion = bundle && bundle.companion;
    if (bundle) fragments = bundle.fragments;
    const held = options || {};
    const numbering = held.numbering || null;
    const level = held.heading || 'h3';
    const under = 'h' + Math.min(6, Number(String(level).slice(1) || 3) + 1);
    const section = el('section', 'proper');

    const heading = el(level, 'proper-name', proper.name || 'Proper');
    // "Vigil Mass", "Mass at Dawn" — the form this proper belongs to, where a
    // day carries more than one.
    if (proper.form) heading.appendChild(el('span', 'proper-form', proper.form));

    // The reference belongs beside the name, not on a line of its own: one
    // heading says what this proper is and where it comes from. Segments stay
    // together in that one reference, since they are one passage.
    const refs = (proper.citations || []).map((citation) => citation.ref).filter(Boolean);
    if (refs.length) {
      const reference = el('span', 'proper-ref', refs.join('; '));
      // The psalm numbering those references are written in, inside the
      // reference so it travels and is removed with it. One proper's citations
      // share one numbering (its own, else its Missal's), so it is said once;
      // the citations below print no reference line of their own.
      const written = (proper.citations || []).map(psalmNumberingLabel).find(Boolean);
      if (written) reference.appendChild(el('span', 'citation-numbering', written));
      heading.appendChild(reference);
    }
    section.appendChild(heading);

    // The incipit is the passage's own opening words, so printing it above the
    // passage says the same thing twice. It earns its place only when the words
    // themselves are not shown.
    const selectedCycle = held.cycle && (
      proper.cycles && proper.cycles[held.cycle] ||
      proper.weekday_cycles && proper.weekday_cycles[held.cycle]
    ) || null;
    const latinWithheld = Boolean(
      selectedCycle && selectedCycle.latin && selectedCycle.latin.withheld ||
      proper.latin && proper.latin.withheld
    );
    const showsWords = Boolean(proper.text) || refs.length > 0;
    if (proper.incipit && !showsWords && !latinWithheld) {
      section.appendChild(el('p', 'proper-incipit', proper.incipit));
    }

    // Composed propers — Collects, Secrets, Postcommunions — are not scripture
    // and have no citation to resolve. Where the structure file carries the
    // text, it is shown; where it carries only the incipit, that is said, once
    // and quietly. It is not a failure: the corpus indexes these propers by
    // their opening words and does not hold their bodies.
    const hasOrationState = Boolean(proper.text) ||
      (proper.translations || []).some((translation) => translation && translation.text) ||
      (proper.unavailable_translations || []).concat(proper.untranslated || []).some(function (row) {
        return proper.source !== 'scripture' || !row.target || row.target.extent !== 'body' ||
          languageBodyTargetMatches(proper, row);
      }) ||
      Boolean(proper.latin && proper.latin.withheld) ||
      properBodyUnavailable(proper);
    let missalTextShown = false;
    if (hasOrationState) {
      const oration = renderOrationState(section, proper, held, null);
      missalTextShown = Boolean(oration.shown);
      if (!oration.creditsShown) orationCredits(section, oration);
    } else if (proper.incipit && proper.source === 'composed') {
      section.appendChild(
        el('p', 'composed-note',
          'Composed text — not scripture. The corpus carries its incipit only.')
      );
    }

    const citations = proper.citations || [];
    // One quiet claim before the passages it qualifies, never a note per verse.
    const claim = citations.length
      ? citationClaim(proper, null, proper.source, missalTextShown, companion ? null : bible) : null;
    if (claim) section.appendChild(claim);
    for (const citation of citations) {
      section.appendChild(
        renderScriptureCitation(citation, bible, fragments, numbering, { showRef: false }, companion)
      );
    }

    // A cycle-varying proper reads differently in each year of the lectionary.
    // The structure file keeps the years apart, and so does this: merging them
    // would hand the reader three readings with no way to tell which is this
    // year's. A year may carry composed words instead of, or beside, a reading.
    //
    // `options.cycle` narrows it to the one year the caller is showing, which is
    // what a page that knows the date wants; without it every year is shown,
    // which is what a page that knows only the Mass wants.
    const cycleKeys = held.cycle
      ? cycleKeysOf(proper).filter((key) => key === held.cycle)
      : cycleKeysOf(proper);
    for (const key of cycleKeys) {
      const cycle = cycleOf(proper, key);
      const block = el('div', 'cycle');
      block.appendChild(el(under, 'cycle-name', cycleLabel(key)));
      let cycleTextShown = false;
      if (cycle.text || cycle.translations.some((translation) => translation && translation.text) ||
          cycle.unavailable_translations.length || cycle.untranslated.length ||
          (cycle.latin && cycle.latin.withheld) || properBodyUnavailable(cycle)) {
        cycleTextShown = Boolean(
          renderOrationState(block, cycle, held, 'for this cycle', proper.source).shown);
      }
      const cycleClaim = cycle.citations.length
        ? citationClaim(cycle, proper, cycle.source || proper.source, cycleTextShown, companion ? null : bible) : null;
      if (cycleClaim) block.appendChild(cycleClaim);
      for (const citation of cycle.citations) {
        block.appendChild(renderScriptureCitation(citation, bible, fragments, numbering, null, companion));
      }
      section.appendChild(block);
    }

    if (!hasOrationState && !proper.incipit && !citations.length && !cycleKeys.length) {
      section.appendChild(notice('this proper carries neither a citation nor a text.'));
    }

    if (held.orationGroups && held.orationGroups.length) {
      appendOrationGroups(section, held.orationGroups, held.eventId, held.structure,
        bible, fragments, held);
    }
    if (held.orationContext) {
      const context = el('p', 'composed-note unit-absence inseparable-oration-context',
        orationContextText(held.orationContext));
      context.setAttribute('role', 'note');
      context.dataset.unitAbsence = 'unresolved:inseparable-oration-assembly';
      section.appendChild(context);
    }
    return section;
  }

  function orationContextText(context) {
    if (!context || context.kind !== 'inseparable-use-context-unresolved') {
      throw new Error('invalid inseparable oration use context');
    }
    return 'RG 110 joins these prayers under one conclusion in the Mass of the Office. ' +
      'This date-independent formulary does not establish Office or votive use, and the paired assembly remains unresolved. ' +
      'Open Day to resolve the dated Mass of the Office.';
  }

  /** Render exact separately attributed bodies, never a synthesized prayer. */
  function appendOrationGroups(section, groups, eventId, structure, bible, fragments, options) {
    (groups || []).forEach(function (group) {
      if (group.count !== 1 || !Array.isArray(group.members) ||
          (group.kind === 'inseparable' ? group.members.length !== 2 :
            group.kind === 'commemoration' ? group.members.length !== 1 : true)) {
        throw new Error('invalid counted oration presentation');
      }
      const wrapper = el('div', group.kind === 'inseparable' ? 'inseparable-oration-group' : 'commemorated-oration');
      wrapper.dataset.orationCount = '1';
      wrapper.dataset.orationBasis = group.locus;
      if (group.conclusion_group) wrapper.dataset.conclusionGroup = String(group.conclusion_group);
      if (group.execution && (group.execution.unresolved || []).indexOf('intermediate-conclusion-spans-unbound') >= 0 && group.position === 2) {
        const absence = el('p', 'composed-note unit-absence oration-execution-absence',
          'These source prayers retain their printed ending cues. One second conclusion is appointed for this chain; an execution text separating the intermediate cues is not yet established.');
        absence.dataset.unitAbsence = 'unresolved:oration-execution-boundaries';
        wrapper.appendChild(absence);
      }
      if (group.execution && (group.execution.unresolved || []).indexOf('source-name-placeholder-unbound') >= 0) {
        const absence = el('p', 'composed-note unit-absence oration-execution-absence',
          'The appointed source retains a name placeholder. Occurrence-specific name wording is not established.');
        absence.dataset.unitAbsence = 'unresolved:oration-source-name';
        wrapper.appendChild(absence);
      }
      group.members.forEach(function (member) {
        if (member.id === eventId) return;
        const hook = (member.sourceHooks || []).find(function (one) { return one.kind === 'proper-structure'; });
        const owner = hook && structure && (structure.masses || []).find(function (one) {
          return hook.id.slice(0, hook.id.lastIndexOf('/')) === structure.calendar + '/' + one.key;
        });
        const proper = owner && owner.propers[Number(hook.id.slice(hook.id.lastIndexOf('/') + 1)) - 1];
        if (!proper) throw new Error('inseparable prayer has no exact production owner: ' + member.id);
        const level = Number(String(options.heading || 'h3').slice(1)) || 3;
        const rendered = renderProper(proper, bible, fragments, Object.assign({}, options, {
          orationGroups: null, executionSource: member.executionSource || null, heading: 'h' + Math.min(6, level + 1)
        }));
        const title = rendered.querySelector('.proper-name');
        if (title && member.of_name) title.textContent = proper.name + ' — ' + member.of_name;
        wrapper.appendChild(rendered);
      });
      wrapper.appendChild(el('p', group.kind === 'inseparable' ? 'composed-note inseparable-oration-note' : 'composed-note commemoration-conclusion-note',
        group.kind === 'inseparable' ? 'These two prayers count as one and are said under ' + group.conclusion + '.' :
          'This commemoration belongs to the second-conclusion group.'));
      section.appendChild(wrapper);
    });
  }

  /**
   * The one line a Mass gets when its formulary is not compiled.
   *
   * Small, quiet, and singular. It must not read as a failure — nothing failed —
   * and it must not let a reader conclude the Mass is short: the day is kept and
   * its propers are appointed, and what is missing is this repository's
   * transcription of them.
   */
  function uncompiledNote(mass) {
    const node = el('p', 'uncompiled');
    node.appendChild(el('span', 'uncompiled-mark', 'Not yet transcribed'));
    node.appendChild(document.createTextNode(
      'This missal keeps the day and appoints its Mass; the propers of it are not ' +
      'in this repository yet' +
      (mass && mass.registry ? ' (registry ' + mass.registry + ')' : '') + '.'));
    return node;
  }

  /* ------------------------------------------------------------------------
   * What the pages may use
   * --------------------------------------------------------------------- */

  return {
    // configuration
    params: PARAMS,
    dataRoot: DATA_ROOT,
    dataPath: dataPath,

    // fetching
    NotFound: NotFound,
    loadJSON: loadJSON,
    exists: exists,
    loadChapter: loadChapter,
    cachedChapterCount: cachedChapterCount,
    addInlineFiles: addInlineFiles,
    setInlineNotice: setInlineNotice,
    isInline: function () { return inlineMode; },
    doneBootstrapping: doneBootstrapping,

    // translations
    loadBibles: loadBibles,
    fillBibleSelect: fillBibleSelect,
    bibleMeta: bibleMeta,
    numberingLabel: numberingLabel,
    lociKey: lociKey,
    editionLoci: editionLoci,
    citationNumbering: citationNumbering,
    psalmNumberingLabel: psalmNumberingLabel,

    // loci and fragments
    lociFor: lociFor,
    formatLoci: formatLoci,
    chaptersNeeded: chaptersNeeded,
    fetchFragments: fetchFragments,
    fetchReaderFragments: fetchReaderFragments,

    // propers, shared by both pages that show the text of a Mass
    SOURCE_LANGUAGE: SOURCE_LANGUAGE,
    languageName: languageName,
    cycleOf: cycleOf,
    cycleKeysOf: cycleKeysOf,
    sundayCycleOf: sundayCycleOf,
    sundayCycleKeysOf: sundayCycleKeysOf,
    weekdayCycleOf: weekdayCycleOf,
    weekdayCycleKeysOf: weekdayCycleKeysOf,
    cycleLabel: cycleLabel,
    citationsOf: citationsOf,
    isPlaceholder: isPlaceholder,
    massIsUncompiled: massIsUncompiled,
    massHasContent: massHasContent,
    orationLanguagesOf: orationLanguagesOf,
    orationLanguageLabel: orationLanguageLabel,
    coverageUnitsOf: coverageUnitsOf,
    selectedCoverageUnits: selectedCoverageUnits,
    selectedOrdinaryCoverageUnits: selectedOrdinaryCoverageUnits,
    summarizeCoverage: summarizeCoverage,
    coverageWitnesses: coverageWitnesses,
    executionWitnesses: executionWitnesses,
    coverageSummaryText: coverageSummaryText,
    coverageNoticeText: coverageNoticeText,
    recensionContext: recensionContext,
    absenceReasons: ABSENCE_REASONS,
    orationFor: orationFor,
    versicled: versicled,
    ordinaryText: ordinaryText,
    translationCredits: translationCredits,
    composedBody: composedBody,
    textSide: textSide,
    renderProper: renderProper,
    orationContextText: orationContextText,
    uncompiledNote: uncompiledNote,

    // rendering
    el: el,
    clear: clear,
    notice: notice,
    renderLocus: renderLocus,
    renderCitation: renderCitation,
    recastLoci: recastLoci,
    showBanner: showBanner,
    statusLine: statusLine,
    fail: fail,
    documentLandmarks: DOCUMENT_LANDMARKS.slice(),
    documentRegion: documentRegion,
    titleCase: titleCase,
    fillSelect: fillSelect,

    // act-keyed records, shared by every page that draws one
    stationKind: stationKind,

    // sequencing
    beginRender: beginRender,
    isCurrentRender: isCurrentRender,
    readHash: readHash,
    writeHash: writeHash,
    replaceHash: replaceHash,
    onHashChange: onHashChange,
    onArrowStep: onArrowStep
  };
}());
