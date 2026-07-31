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

  /** "Ps 24:1-3, Ps 24:4" — used where the structure names no reference. */
  function formatLoci(loci) {
    return loci
      .map((locus) => {
        const range = Number(locus.first) === Number(locus.last)
          ? String(locus.first)
          : locus.first + '-' + locus.last;
        return locus.book + ' ' + locus.chapter + ':' + range;
      })
      .join(', ');
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

  /**
   * Render one locus out of an already-fetched chapter.
   *
   * Verses are emitted in ascending numeric order WITHIN the locus, but loci
   * are emitted in the order the citation lists them — a chant citation such as
   * "Psalm 138:18, 5-6" is deliberately out of sequence and must stay that way.
   *
   * Carries FAILURE 3 (the fragment is not there at all) and FAILURE 4 (the
   * fragment is there and the verses are not).
   */
  function renderLocus(locus, fragment, language) {
    if (!fragment.ok) return notice(fragment.problem);

    const first = Number(locus.first);
    const last = Number(locus.last);
    const numbers = Object.keys(fragment.verses)
      .map(Number)
      .filter((n) => Number.isFinite(n) && n >= first && n <= last)
      .sort((a, b) => a - b);

    if (!numbers.length) {
      return notice(
        'this edition\'s ' + locus.book + ' ' + locus.chapter + ' has no verses ' +
        first + '-' + last + '.'
      );
    }

    const passage = el('p', 'passage');
    // The edition's own language, so that Latin is spoken and hyphenated as
    // Latin and English as English.
    if (language) passage.lang = language;

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

    const gaps = [];
    for (let n = first; n <= last; n += 1) {
      if (!numbers.includes(n)) gaps.push(n);
    }
    if (gaps.length && gaps.length < last - first + 1) {
      const wrapper = document.createDocumentFragment();
      wrapper.appendChild(passage);
      wrapper.appendChild(
        notice(
          'verse' + (gaps.length > 1 ? 's ' : ' ') + gaps.join(', ') +
          ' of ' + locus.book + ' ' + locus.chapter +
          ' — absent from this edition\'s fragment.'
        )
      );
      return wrapper;
    }

    return passage;
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
  function recastLoci(citation, bible, sourceNumbering, picked) {
    if (!sourceNumbering || sourceNumbering === bible.numbering) return null;
    if (!picked.loci) return null;
    const source = lociFor(citation, sourceNumbering);
    if (!source.loci) return null;
    if (formatLoci(source.loci) === formatLoci(picked.loci)) return null;
    return formatLoci(picked.loci) + ' in this edition\'s ' + bible.numbering +
      ' numbering';
  }

  /**
   * One citation, with its reference line and its text — or with the reason
   * there is no text. Carries FAILURE 1 (unresolved) and FAILURE 2 (numbering).
   *
   * `sourceNumbering` is the numbering the structure file's own references are
   * written in, where the caller knows it.
   */
  function renderCitation(citation, bible, fragments, sourceNumbering) {
    const block = el('div', 'citation');

    if (citation.unresolved) {
      block.appendChild(
        el('p', 'citation-ref',
          citation.ref || citation.book || citation.token || 'Unlabelled citation')
      );
      block.appendChild(notice(String(citation.unresolved)));
      return block;
    }

    const picked = lociFor(citation, bible.numbering);
    const label = citation.ref ||
      (picked.loci ? formatLoci(picked.loci) : null) ||
      citation.book || citation.token || 'Unlabelled citation';
    const line = el('p', 'citation-ref', label);
    const recast = recastLoci(citation, bible, sourceNumbering, picked);
    if (recast) line.appendChild(el('span', 'citation-recast', recast));
    block.appendChild(line);

    if (!picked.loci) {
      block.appendChild(notice(picked.problem));
      return block;
    }

    for (const locus of picked.loci) {
      const fragment = fragments.get(locus.book + '|' + locus.chapter) ||
        { ok: false, problem: locus.book + ' ' + locus.chapter + ' was not loaded.' };
      block.appendChild(renderLocus(locus, fragment, bible.language));
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

    // sequencing
    beginRender: beginRender,
    isCurrentRender: isCurrentRender,
    readHash: readHash,
    writeHash: writeHash,
    onHashChange: onHashChange,
    onArrowStep: onArrowStep
  };
}());
