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
    return JSON.parse(JSON.stringify(inlineFiles[path]));
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

    try {
      return await response.json();
    } catch (error) {
      throw new Error(url + ' — the response was not valid JSON');
    }
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

  function clear(node) {
    while (node.firstChild) node.removeChild(node.firstChild);
  }

  function showBanner(text) {
    const banner = document.getElementById('banner');
    if (!banner) return;
    banner.textContent = text;
    banner.hidden = false;
  }

  /**
   * The one-line spoken summary.
   *
   * The reading area is not itself a live region: replacing it would read a
   * whole Mass aloud on every change. This says what changed instead.
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

  function fail(text) {
    const reading = document.getElementById('reading');
    if (!reading) return;
    clear(reading);
    reading.appendChild(el('p', 'error', text));
    reading.setAttribute('aria-busy', 'false');
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

  function bibleMeta(bible) {
    const meta = [bible.label + ' — ' + bible.numbering + ' numbering'];
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
   * Pick the loci a given edition can actually read.
   *
   * Structure files key loci by numbering system because the psalter is
   * numbered differently in the Vulgate and Hebrew traditions and the same
   * citation lands on different chapters. No numbering logic ships to the
   * browser: the page reads the edition's `numbering` and takes the loci
   * already computed for it. An edition whose numbering has no entry is a gap
   * in the data, and is reported rather than silently guessed at — FAILURE 2.
   *
   * The book token may sit on the locus or on the citation that owns it: a
   * reading names its book once and lets its loci carry chapter and verses
   * only. The token is what the fragment path is built from, so it wins over
   * the display name.
   */
  function lociFor(citation, numbering) {
    const loci = (citation && citation.loci) || {};
    const chosen = loci[numbering];
    const owner = (citation && (citation.token || citation.book)) || null;

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

  /** Every distinct chapter a list of citations needs, in this numbering. */
  function chaptersNeeded(citations, numbering) {
    const wanted = new Map();
    for (const citation of citations) {
      if (!citation || citation.unresolved) continue;
      const picked = lociFor(citation, numbering);
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
  async function fetchFragments(bible, citations) {
    const chapters = chaptersNeeded(citations, bible.numbering);
    const results = await Promise.all(
      chapters.map((needed) => loadChapter(bible.id, needed.book, needed.chapter))
    );
    const fragments = new Map();
    chapters.forEach((needed, index) => {
      fragments.set(needed.book + '|' + needed.chapter, results[index]);
    });
    return { fragments: fragments, chapters: chapters };
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
      verse.appendChild(el('span', 'visually-hidden', 'Verse ' + number + '. '));
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
    if (!sourceNumbering || sourceNumbering === bible.numbering) return null;
    if (!picked.loci) return null;
    const source = lociFor(citation, sourceNumbering);
    if (!source.loci) return null;
    if (formatLoci(source.loci, options) === formatLoci(picked.loci, options)) {
      return null;
    }
    return formatLoci(picked.loci, options) + ' in this edition\'s ' +
      bible.numbering + ' numbering';
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

    const picked = lociFor(citation, bible.numbering);
    const label = citation.ref ||
      (picked.loci ? formatLoci(picked.loci, options) : null) ||
      (options && options.book) || citation.book || citation.token ||
      'Unlabelled citation';
    const recast = recastLoci(citation, bible, sourceNumbering, picked, options);
    if (showRef) {
      const line = el('p', 'citation-ref', label);
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

  function writeHash(pairs) {
    const parts = [];
    for (const [key, value] of pairs) {
      if (value === null || value === undefined || value === '') continue;
      parts.push(key + '=' + encodeURIComponent(value));
    }
    if (!parts.length) return;
    const next = '#' + parts.join('&');
    if (window.location.hash === next) return;
    lastWritten = next;
    window.location.hash = next;
  }

  function onHashChange(handler) {
    window.addEventListener('hashchange', () => {
      if (window.location.hash === lastWritten) return;
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
  function cycleOf(proper, key) {
    const held = (proper && proper.cycles && proper.cycles[key]) || null;
    if (!held) return { citations: [], text: null };
    return { citations: held.citations || [], text: held.text || null };
  }

  /** The years a proper actually varies over, in order, each carrying something. */
  function cycleKeysOf(proper) {
    return Object.keys((proper && proper.cycles) || {})
      .sort()
      .filter((key) => {
        const cycle = cycleOf(proper, key);
        return cycle.citations.length || cycle.text;
      });
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
    let composed = 0;
    const held = new Map();
    for (const mass of (structure && structure.masses) || []) {
      for (const proper of mass.propers || []) {
        if (!proper.text || isPlaceholder(proper)) continue;
        composed += 1;
        for (const translation of proper.translations || []) {
          if (!translation || !translation.lang || !translation.text) continue;
          held.set(translation.lang, (held.get(translation.lang) || 0) + 1);
        }
      }
    }
    const languages = [{ lang: SOURCE_LANGUAGE, held: composed, composed: composed }];
    for (const lang of Array.from(held.keys()).sort()) {
      languages.push({ lang: lang, held: held.get(lang), composed: composed });
    }
    return languages;
  }

  /** The label an orations control gives one of those languages. */
  function orationLanguageLabel(entry) {
    // The source language needs no coverage figure: it is what the missal
    // prints, so it is complete by definition. Every other entry states how far
    // it reaches, because none of them reaches everywhere.
    return entry.lang === SOURCE_LANGUAGE
      ? languageName(entry.lang) + ', as printed'
      : languageName(entry.lang) + ' — ' + entry.held + ' of ' + entry.composed;
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

  const VERSICLE_CANDIDATE = /([VR])\.(?=\s|$)/g;
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
    node.appendChild(el('span', 'visually-hidden', VERSICLE_NAMES[letter]));
    return node;
  }

  /** A text with its versicle and response marks set, as a fragment. */
  function versicled(text) {
    const fragment = document.createDocumentFragment();
    const source = text === null || text === undefined ? '' : String(text);
    let at = 0;
    let found;
    VERSICLE_CANDIDATE.lastIndex = 0;
    while ((found = VERSICLE_CANDIDATE.exec(source)) !== null) {
      const before = source.slice(0, found.index);
      if (!OPENS_A_CLAUSE.test(before) || AN_INITIAL_BEFORE.test(before)) continue;
      if (found.index > at) {
        fragment.appendChild(document.createTextNode(source.slice(at, found.index)));
      }
      fragment.appendChild(versicleMark(found[1]));
      at = found.index + found[0].length;
    }
    if (at < source.length) fragment.appendChild(document.createTextNode(source.slice(at)));
    return fragment;
  }

  /**
   * The composed text to show, and what to say about it.
   *
   * A proper with no translation in the chosen language is the ordinary case,
   * not an error — but it must not silently fall back to Latin and let the
   * reader believe they are looking at the English they asked for. The absence
   * is stated where the text would have been.
   */
  function orationFor(proper, wanted, witness) {
    const asked = wanted || SOURCE_LANGUAGE;
    if (asked === SOURCE_LANGUAGE) {
      return { text: proper.text, lang: SOURCE_LANGUAGE, missing: false, source: null };
    }
    const found = (proper.translations || []).find((translation) => {
      if (!translation || translation.lang !== asked || !translation.text) return false;
      if (!witness) return true;
      return (translation.source_id || translation.source || null) === witness;
    });
    if (found) {
      return {
        text: found.text,
        lang: asked,
        missing: false,
        source: found.source_id || found.source || null,
        notice: found.notice || null
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
    if (refs.length) heading.appendChild(el('span', 'proper-ref', refs.join('; ')));
    section.appendChild(heading);

    // The incipit is the passage's own opening words, so printing it above the
    // passage says the same thing twice. It earns its place only when the words
    // themselves are not shown.
    const showsWords = Boolean(proper.text) || refs.length > 0;
    if (proper.incipit && !showsWords) {
      section.appendChild(el('p', 'proper-incipit', proper.incipit));
    }

    // Composed propers — Collects, Secrets, Postcommunions — are not scripture
    // and have no citation to resolve. Where the structure file carries the
    // text, it is shown; where it carries only the incipit, that is said, once
    // and quietly. It is not a failure: the corpus indexes these propers by
    // their opening words and does not hold their bodies.
    if (proper.text) {
      const oration = orationFor(proper, held.orations, held.translationWitness || null);
      const composed = el('p', 'composed');
      const label = oration.missing
        ? 'Composed text — not scripture · ' + languageName(SOURCE_LANGUAGE)
        : 'Composed text — not scripture' +
          (oration.lang === SOURCE_LANGUAGE ? '' : ' · ' + languageName(oration.lang));
      composed.appendChild(el('span', 'composed-label', label));
      composed.appendChild(versicled(oration.text));
      composed.lang = oration.lang;
      section.appendChild(composed);

      // Said where the English would have been, not in a footnote: a reader who
      // asked for English and was handed Latin needs to know that at the text.
      if (oration.missing) {
        section.appendChild(
          el('p', 'composed-note',
            'No ' + languageName(oration.wanted) + ' translation is recorded for ' +
            'this proper. The Latin the missal prints is shown instead.')
        );
      }
      // Whose English it is. A translation is someone's expression, and the
      // reader is entitled to know whose before weighing it.
      if (oration.source) {
        section.appendChild(el('p', 'composed-note', 'Translation: ' + oration.source));
      }
      if (oration.notice) {
        section.appendChild(el('p', 'composed-note', oration.notice));
      }
    } else if (proper.incipit && proper.source === 'composed') {
      section.appendChild(
        el('p', 'composed-note',
          'Composed text — not scripture. The corpus carries its incipit only.')
      );
    }

    const citations = proper.citations || [];
    for (const citation of citations) {
      section.appendChild(
        renderCitation(citation, bible, fragments, numbering, { showRef: false })
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
      if (cycle.text) {
        const composed = el('p', 'composed');
        composed.appendChild(el('span', 'composed-label', 'Composed text — not scripture'));
        composed.appendChild(versicled(cycle.text));
        composed.lang = SOURCE_LANGUAGE;
        block.appendChild(composed);
      }
      for (const citation of cycle.citations) {
        block.appendChild(renderCitation(citation, bible, fragments, numbering));
      }
      section.appendChild(block);
    }

    if (!proper.text && !proper.incipit && !citations.length && !cycleKeys.length) {
      section.appendChild(notice('this proper carries neither a citation nor a text.'));
    }

    return section;
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

    // loci and fragments
    lociFor: lociFor,
    formatLoci: formatLoci,
    chaptersNeeded: chaptersNeeded,
    fetchFragments: fetchFragments,

    // propers, shared by both pages that show the text of a Mass
    SOURCE_LANGUAGE: SOURCE_LANGUAGE,
    languageName: languageName,
    cycleOf: cycleOf,
    cycleKeysOf: cycleKeysOf,
    cycleLabel: cycleLabel,
    citationsOf: citationsOf,
    isPlaceholder: isPlaceholder,
    massIsUncompiled: massIsUncompiled,
    massHasContent: massHasContent,
    orationLanguagesOf: orationLanguagesOf,
    orationLanguageLabel: orationLanguageLabel,
    orationFor: orationFor,
    versicled: versicled,
    renderProper: renderProper,
    uncompiledNote: uncompiledNote,

    // rendering
    el: el,
    clear: clear,
    notice: notice,
    renderLocus: renderLocus,
    renderCitation: renderCitation,
    showBanner: showBanner,
    statusLine: statusLine,
    fail: fail,
    titleCase: titleCase,
    fillSelect: fillSelect,

    // act-keyed records, shared by every page that draws one
    stationKind: stationKind,

    // sequencing
    beginRender: beginRender,
    isCurrentRender: isCurrentRender,
    readHash: readHash,
    writeHash: writeHash,
    onHashChange: onHashChange,
    onArrowStep: onArrowStep
  };
}());
