/* ===========================================================================
 * The catena page — a chapter, and every fragment held on it
 * ===========================================================================
 *
 * The reader picks a book, a chapter and a translation. The page shows the
 * chapter in that translation and, beneath it, the commentary this project
 * holds on that chapter, oldest first.
 *
 * WHAT THIS FILE DOES NOT DO, AND MUST NOT START DOING:
 *
 *   It does not decide which fragments belong to a chapter. That is
 *   `catena-model.js`, which `catena check` replays under node against the
 *   solved cases in the source. One derivation.
 *
 *   It does not resolve a numbering. `guidance/web-data.md` keeps numbering
 *   logic out of the browser entirely: the refusals the projection made arrive
 *   as data in the book file, and this file reads them. Working out where a
 *   displaced psalm's boundary moved is exactly the guess the whole apparatus
 *   exists to prevent.
 *
 *   It does not filter on rights or on confidence. An unpublishable fragment
 *   never enters the structure file, and an L1 confidence is dropped at
 *   generation. Both guards live where a page cannot undo them, which is the
 *   same reason `bibles.json` excludes a licensed edition rather than the
 *   browser hiding it.
 *
 * WHAT A READER PAYS FOR. The book file is a SPINE: it carries every fragment's
 * author, work, date, extent, edition, rights and length, and no prose at all.
 * Each fragment's text is its own file, named by the spine, and is fetched when
 * the reader opens that fragment. So a chapter that holds nothing costs the
 * spine, a chapter that holds twenty costs the spine, and reading one of the
 * twenty costs that one. Genesis was 606 KB before this, all of it prose about
 * chapter 1, fetched in full by a reader on chapter 40.
 *
 * The cost is real and is stated on the page rather than hidden: text that has
 * not been fetched is not in the document, so the browser's own find-in-page
 * cannot reach it. That is the trade, and it is why the summary line carries a
 * word count — a reader chooses what to open knowing how long it is.
 *
 * THE ORDER OF THE PAGE IS THE MAINTAINER'S STANDING DIRECTION: the facts
 * first, everything else below. Reference, chapter, chain; then the works not
 * yet acquired; then the fragments held but not renderable; then, in the
 * footer, the prose.
 * ======================================================================== */

'use strict';

(function () {
  const T = window.Triptych;
  const M = window.CatenaModel;

  const INDEX_PATH = 'structure/catena/index.json';
  const PARAGRAPH_INDEX_PATH = 'structure/paragraphs/index.json';

  // The languages a fragment's edition can be in, named for a reader. The codes
  // are the source library's, which are ISO 639 and are what the `lang`
  // attribute needs; the words are what a selector can be read in. An unknown
  // code prints as itself rather than being dropped, because a language nobody
  // named is still a language the reader is looking at.
  const LANGUAGE_NAMES = {
    la: 'Latin',
    grc: 'Greek',
    el: 'Greek',
    en: 'English',
    de: 'German',
    fr: 'French',
    he: 'Hebrew',
    syr: 'Syriac',
    it: 'Italian',
    es: 'Spanish'
  };

  function languageName(code) {
    return LANGUAGE_NAMES[String(code || '')] || String(code || '');
  }

  /** "Latin and English", for a sentence rather than a control. */
  function languageList(file) {
    const names = ((file && file.languages) || []).map(languageName);
    if (names.length <= 1) return names.join('');
    return names.slice(0, -1).join(', ') + ' and ' + names[names.length - 1];
  }

  const reference = document.getElementById('reference');
  const referenceBook = document.getElementById('reference-book');
  const tally = document.getElementById('tally');
  const reading = document.getElementById('reading');
  const bookSelect = document.getElementById('book-select');
  const chapterSelect = document.getElementById('chapter-select');
  const bibleSelect = document.getElementById('bible-select');
  const languageSelect = document.getElementById('language-select');
  const previousButton = document.getElementById('prev-button');
  const nextButton = document.getElementById('next-button');

  let index = null;
  let bibles = [];
  const chapterFiles = new Map();
  // One promise per fragment text file, so a reader who closes a fragment and
  // opens it again, or pages away and back, refetches nothing.
  const fragmentTexts = new Map();
  const paragraphFiles = new Map();
  // The paragraph layer, and whether the reader wants it. On by default because
  // a whole chapter set as one block is the reason the layer exists; the switch
  // is what lets it be turned off, and turned off the chapter renders exactly as
  // it did before the layer existed.
  let paragraphs = null;
  // Always on, and not a control. Where a chapter divides, that is how the
  // chapter reads; offering it as a preference invited a reader to turn off
  // the edition's own paragraphing. The opt-out that does exist is the
  // typesetter's `--no-paragraphs`, which is for reviewing an edition
  // mechanically rather than reading it.
  const paragraphsWanted = true;
  // Authors the reader has switched OFF, held across chapters. Storing the
  // exclusions rather than the inclusions is what lets an author who does not
  // comment on the next chapter stay off rather than reappear checked.
  const hiddenAuthors = new Set();

  /* ------------------------------------------------------------------------
   * Data
   * --------------------------------------------------------------------- */

  function heldEntry(token) {
    return (index.held || []).find((book) => book.token === token) || null;
  }

  /**
   * The spine for one chapter: who comments here, what is led to, what is
   * refused. It carries no prose.
   *
   * A chapter with nothing at all has NO FILE, and the index says which chapters
   * have one — so a reader on Genesis 40 asks for nothing and is told plainly
   * that nothing is held there. The path and the padding both come from the
   * index rather than being composed here: `structure/catena/01-gen/040.json` is
   * a form the generator owns, and a page that assembled it out of a token and a
   * width would be the second place that convention lived.
   */
  function chapterFile(token, chapter) {
    const held = heldEntry(token);
    if (!held || !(held.present || []).includes(Number(chapter))) {
      return Promise.resolve(null);
    }
    const digits = Number(index.chapter_digits) || 1;
    const path =
      held.path + String(chapter).padStart(digits, '0') + '.json';
    if (chapterFiles.has(path)) return chapterFiles.get(path);
    const pending = T.loadJSON(path).then(
      (file) => file,
      (error) => {
        if (error instanceof T.NotFound) return null;
        throw error;
      }
    );
    chapterFiles.set(path, pending);
    return pending;
  }

  function canonEntry(token) {
    return (index.canon || []).find((book) => book.token === token) || null;
  }

  /**
   * Where this edition opens a paragraph in this chapter.
   *
   * The layer is the EDITION's, not the catena's — `scripts/_paragraphs.py`
   * owns the derivation and this page owns none of it. A chapter that runs on
   * has no file, so the 404 is the answer and costs one request; a chapter that
   * divides costs about 220 bytes.
   *
   * Switched off, this asks for nothing at all and the chapter renders exactly
   * as it did before the layer existed. That is the point of the switch: a
   * mechanical review of an edition must be able to see the edition and not
   * this project's reading of it.
   */
  function chapterParagraphs(bible, token, chapter) {
    if (!paragraphsWanted || !paragraphs) return Promise.resolve(null);
    const edition = (paragraphs.editions || {})[bible.id];
    // The book's path component is the one the canon index wrote down. It is
    // read, never composed: the convention lives in `scripts/_canon.py` and a
    // page that rebuilt it would be the second place it lived.
    const book = canonEntry(token);
    if (!edition || !book || !book.path) return Promise.resolve(null);
    const digits = Number(paragraphs.chapter_digits) || 1;
    const path =
      edition.path + book.path + '/' + String(chapter).padStart(digits, '0') + '.json';
    if (paragraphFiles.has(path)) return paragraphFiles.get(path);
    const pending = T.loadJSON(path).then(
      (file) => file,
      (error) => {
        if (error instanceof T.NotFound) return null;
        throw error;
      }
    );
    paragraphFiles.set(path, pending);
    return pending;
  }

  /**
   * One fragment's prose, fetched once and kept.
   *
   * Keyed by the path the SPINE gave, never by a path this file assembles from
   * an id: a page that builds its own URLs out of record identifiers is a page
   * that can be walked out of its data root by a bad identifier. The generator
   * checks the name and writes it down; this follows it.
   */
  function fragmentText(path) {
    if (!path) return Promise.resolve(null);
    if (fragmentTexts.has(path)) return fragmentTexts.get(path);
    const pending = T.loadJSON(path);
    fragmentTexts.set(path, pending);
    return pending;
  }


  /* ------------------------------------------------------------------------
   * Rendering — the chapter
   * --------------------------------------------------------------------- */

  function renderChapter(container, bible, book, chapter, result, marks) {
    const section = T.el('section', 'chapter');
    if (!result.ok) {
      section.appendChild(T.notice(result.problem));
      container.appendChild(section);
      return;
    }
    const numbers = Object.keys(result.verses)
      .map(Number)
      .filter((n) => Number.isFinite(n))
      .sort((a, b) => a - b);
    if (!numbers.length) {
      section.appendChild(T.notice(book.name + ' ' + chapter + ' carries no verses.'));
      container.appendChild(section);
      return;
    }

    // The chapter is set as prose, not as a stack of verse-lines, because a
    // stack of verse-lines is a concordance. Where paragraph structure is held
    // it divides that prose; where it is not, the chapter runs on as it always
    // has. `marks` is empty in both the "switched off" and the "none held"
    // cases, and the note below says which of the two a reader is looking at.
    const breaks = (marks && marks.breaks) || {};
    const body = T.el('div', 'passage');
    body.lang = bible.language || 'en';
    let passage = null;
    let printed = 0;
    let projected = 0;
    for (const number of numbers) {
      const kind = breaks[String(number)];
      if (!passage || kind) {
        passage = T.el('p', 'passage-paragraph');
        if (kind === 'projected') passage.classList.add('projected');
        if (kind === 'printed') printed += 1;
        if (kind === 'projected') projected += 1;
        body.appendChild(passage);
      }
      const verse = T.el('span', 'verse');
      verse.appendChild(T.el('sup', 'verse-num', String(number)));
      verse.appendChild(document.createTextNode(result.verses[String(number)] + ' '));
      passage.appendChild(verse);
    }
    // Closed like everything else. The maintainer's direction is that the page
    // opens as an index of what is here — the chapter, who comments on it, what
    // is not yet acquired — and a reader opens what they want. An earlier pass
    // kept this open on the theory that the chapter is the point; it made the
    // page open on a wall of text with the chain pushed below the fold.
    const holder = document.createElement('details');
    holder.className = 'chapter-body';
    const head = document.createElement('summary');
    head.className = 'chapter-head';
    head.appendChild(
      T.el('span', 'chapter-name', book.name + ' ' + chapter)
    );
    head.appendChild(
      T.el(
        'span',
        'chapter-count',
        numbers.length + (numbers.length === 1 ? ' verse' : ' verses')
      )
    );
    if (printed + projected) {
      head.appendChild(
        T.el(
          'span',
          'chapter-count',
          printed + projected + (printed + projected === 1 ? ' paragraph' : ' paragraphs')
        )
      );
    }
    holder.appendChild(head);
    holder.appendChild(body);
    // A printed mark and a projected one are not the same claim, so the page
    // says which it is showing rather than letting a division this project
    // inferred read as the edition's own printing.
    if (printed + projected) {
      const note = T.el('p', 'paragraph-note');
      const parts = [];
      if (printed) {
        parts.push(
          printed + (printed === 1 ? ' break is' : ' breaks are') +
            ' printed in this edition'
        );
      }
      if (projected) {
        parts.push(
          projected + (projected === 1 ? ' is' : ' are') +
            ' projected from the witnesses that concur, and marked'
        );
      }
      note.appendChild(document.createTextNode('Paragraphs: ' + parts.join('; ') + '.'));
      holder.appendChild(note);
    } else if (paragraphsWanted) {
      holder.appendChild(
        T.el(
          'p',
          'paragraph-note',
          'No paragraph division is held for this chapter in this edition, so it ' +
            'runs on. Another edition’s paragraphs are not borrowed for it.'
        )
      );
    }
    section.appendChild(holder);
    container.appendChild(section);
  }

  /* ------------------------------------------------------------------------
   * Rendering — the chain
   *
   * Rule 6 governs the label: a fragment shown under a chapter it only reaches
   * into still says where it actually runs from and to, because a fragment cut
   * at a boundary would attribute to one chapter words written about another.
   * --------------------------------------------------------------------- */

  function renderFragment(fragment, bookName) {
    const item = T.el('li', 'fragment');

    // Collapsed by default, and `details` rather than a scripted toggle so the
    // control is keyboard-reachable. The summary carries author, work, date,
    // extent and length, which is what makes a closed chain worth reading on
    // its own: it becomes a chronological index of who comments here, how far
    // each one reaches, and how much of him there is.
    const details = document.createElement('details');
    details.className = 'fragment-body';

    const head = document.createElement('summary');
    head.className = 'fragment-head';
    head.appendChild(T.el('span', 'fragment-author', fragment.author));
    head.appendChild(T.el('span', 'fragment-work', fragment.work));
    if (fragment.date !== null && fragment.date !== undefined) {
      head.appendChild(T.el('span', 'fragment-date', String(fragment.date)));
    }
    if (fragment.language) {
      head.appendChild(
        T.el('span', 'fragment-language', languageName(fragment.language))
      );
    }
    if (Number.isFinite(Number(fragment.text_words)) && fragment.text_words > 0) {
      head.appendChild(
        T.el(
          'span',
          'fragment-length',
          Number(fragment.text_words).toLocaleString() + ' words'
        )
      );
    }

    const extent = T.el('span', 'fragment-extent');
    extent.appendChild(
      document.createTextNode(M.formatExtent(fragment.extent, bookName))
    );
    if (M.spansChapters(fragment.extent)) {
      extent.appendChild(document.createTextNode(' '));
      extent.appendChild(
        T.el('span', 'spans', '— runs across the chapter boundary')
      );
    }
    head.appendChild(extent);
    details.appendChild(head);

    // The prose is not here yet, and is fetched the first time the reader opens
    // this fragment. A failure is reported against this fragment and nothing
    // else: one text that will not load must not take the chain down with it.
    const text = T.el('p', 'fragment-text', 'Loading…');
    text.lang = fragment.language || 'en';
    details.appendChild(text);
    // The apparatus that travels with the prose: why the extent was drawn where
    // it was, and on what ground the date rests. Both are about this one
    // fragment, so both are in its file rather than in the spine, and both are
    // shown below the text where a reader can weigh them against it.
    const apparatus = T.el('div', 'fragment-apparatus');
    details.appendChild(apparatus);
    let asked = false;
    details.addEventListener('toggle', () => {
      if (!details.open || asked) return;
      asked = true;
      fragmentText(fragment.text_path).then(
        (loaded) => {
          if (!loaded) {
            text.className = 'fragment-text missing';
            text.textContent =
              'This fragment carries no text file, so nothing of it can be shown.';
            return;
          }
          text.textContent = String(loaded.text || '');
          if (loaded.basis) {
            apparatus.appendChild(
              T.el('p', 'fragment-basis', 'Extent — ' + loaded.basis)
            );
          }
          if (loaded.date_basis) {
            apparatus.appendChild(
              T.el('p', 'fragment-basis', 'Date — ' + loaded.date_basis)
            );
          }
        },
        (error) => {
          asked = false;
          text.className = 'fragment-text missing';
          text.textContent =
            error instanceof T.NotFound
              ? 'The text of this fragment was not published beside the page.'
              : 'The text of this fragment could not be loaded: ' +
                (error.message || error);
        }
      );
    });

    // Where it came from and how to check it. Below the text, never above.
    const source = T.el('p', 'fragment-source');
    source.appendChild(document.createTextNode(fragment.locator));
    if (fragment.edition) {
      source.appendChild(T.el('span', 'sep'));
      source.appendChild(document.createTextNode(fragment.edition));
    }
    if ((fragment.translators || []).length) {
      source.appendChild(T.el('span', 'sep'));
      source.appendChild(
        document.createTextNode('tr. ' + fragment.translators.join(', '))
      );
    }
    // `fragment.container` is carried in the data and deliberately not printed:
    // it is a record id, and the edition line above already names the volume in
    // words. A reader is owed the volume, not the key it is filed under.
    if (fragment.rights) {
      source.appendChild(T.el('span', 'sep'));
      source.appendChild(document.createTextNode(fragment.rights));
    }
    // The review state, said truthfully or not at all. `inspected` means
    // someone read it; `verified` means it was collated against the
    // controlling witness. Printing them alike would claim a check nobody
    // performed, so the weaker state is the one that gets the word.
    if (fragment.review && fragment.review !== 'verified') {
      source.appendChild(T.el('span', 'sep'));
      source.appendChild(T.el('span', 'state', fragment.review + ', not collated'));
    }
    // An excerpt is worth more when its context is a click away. The source
    // library reads the whole edition this fragment was cut from, and the
    // passage id is the only thing needed to reach the right place in it: that
    // page looks the id up in what its own generator wrote, rather than being
    // handed a path this page would have to compose and keep in step.
    if (fragment.id) {
      source.appendChild(T.el('span', 'sep'));
      const whole = T.el('a', 'fragment-whole', 'Read the whole work');
      whole.href = '../sources/#passage=' + encodeURIComponent(fragment.id);
      source.appendChild(whole);
    }
    details.appendChild(source);
    item.appendChild(details);
    return item;
  }

  function renderChain(container, file, book) {
    // Already the chapter's own list: the spine is addressed by chapter, and the
    // derivation that decided which fragments stand here ran in the generator,
    // out of `catena-model.js` under node. One derivation, and it is that file's.
    // What each fragment shares with its edition is stored once per file and
    // rejoined here, which is the same file's `chapterFragments`.
    const all = M.chapterFragments(file);
    const wanted = languageSelect.value;
    const held = wanted ? all.filter((one) => one.language === wanted) : all;
    const headingText =
      held.length === 0
        ? 'Commentary held here'
        : held.length === 1
          ? 'One fragment held here'
          : held.length + ' fragments held here';
    const heading = T.el('h2', 'section-heading', headingText);
    container.appendChild(heading);
    if (!held.length) {
      // Rule 1: a chapter with no fragments shows no fragments, and says so
      // plainly rather than showing something else in their place.
      container.appendChild(
        T.el(
          'p',
          'aside-note',
          all.length
            ? 'No commentary on this chapter is held in ' +
                languageName(wanted) +
                '. ' +
                all.length +
                (all.length === 1 ? ' fragment is' : ' fragments are') +
                ' held here in ' +
                languageList(file) +
                '; choose “All languages” to see ' +
                (all.length === 1 ? 'it' : 'them') +
                '.'
            : 'No commentary on this chapter is held yet.'
        )
      );
      return 0;
    }

    // Which languages this chapter is held in, and which the reader is not
    // seeing. Said rather than hidden: a father held only in Latin must not
    // disappear from the page because the selector is set to English.
    if (wanted) {
      const others = (file.languages || []).filter((one) => one !== wanted);
      if (others.length) {
        container.appendChild(
          T.el(
            'p',
            'aside-note',
            'Showing ' +
              languageName(wanted) +
              ' only. This chapter is also held in ' +
              others.map(languageName).join(', ') +
              '.'
          )
        );
      }
    }

    // Grouped by author, in the order the chain already runs, which is oldest
    // first. Insertion order is the grouping order, so the tree inherits the
    // chronology rather than re-deriving it — and a second sort here could
    // silently disagree with the model's.
    const groups = [];
    const byAuthor = new Map();
    for (const fragment of held) {
      let group = byAuthor.get(fragment.author);
      if (!group) {
        group = { author: fragment.author, date: fragment.date, fragments: [] };
        byAuthor.set(fragment.author, group);
        groups.push(group);
      }
      group.fragments.push(fragment);
    }

    const list = T.el('ul', 'chain');
    const rendered = [];
    for (const group of groups) {
      const item = T.el('li', 'author');
      const node = document.createElement('details');
      node.className = 'author-body';

      const summary = document.createElement('summary');
      summary.className = 'author-head';
      summary.appendChild(T.el('span', 'author-name', group.author));
      if (group.date !== null && group.date !== undefined) {
        summary.appendChild(T.el('span', 'author-date', String(group.date)));
      }
      summary.appendChild(
        T.el(
          'span',
          'author-count',
          group.fragments.length === 1
            ? '1 fragment'
            : group.fragments.length + ' fragments'
        )
      );
      node.appendChild(summary);

      const inner = T.el('ul', 'author-fragments');
      for (const fragment of group.fragments) {
        inner.appendChild(renderFragment(fragment, book.name));
      }
      node.appendChild(inner);
      item.appendChild(node);
      list.appendChild(item);
      rendered.push({ author: group.author, item: item, count: group.fragments.length });
    }

    // Who may be read. The set holds the DESELECTED authors, so turning one off
    // keeps him off while paging through chapters, and an author who simply
    // does not comment on the next chapter does not come back switched on.
    // Hiding rows rather than rebuilding is what keeps an opened node open.
    function applyFilter() {
      let shown = 0;
      for (const row of rendered) {
        const on = !hiddenAuthors.has(row.author);
        row.item.hidden = !on;
        if (on) shown += row.count;
      }
      // The heading counts what is HELD; this says what is shown, and only when
      // the two differ. A filtered chain reporting a smaller total as the total
      // would misstate the corpus.
      heading.textContent =
        shown === held.length ? headingText : headingText + ' \u2014 ' + shown + ' shown';
    }

    if (rendered.length > 1) {
      const filter = T.el('div', 'author-filter');
      filter.setAttribute('role', 'group');
      filter.setAttribute('aria-label', 'Authors shown');
      for (const row of rendered) {
        const label = T.el('label', 'author-toggle');
        const box = document.createElement('input');
        box.type = 'checkbox';
        box.checked = !hiddenAuthors.has(row.author);
        box.addEventListener('change', () => {
          if (box.checked) hiddenAuthors.delete(row.author);
          else hiddenAuthors.add(row.author);
          applyFilter();
        });
        label.appendChild(box);
        label.appendChild(document.createTextNode(row.author));
        filter.appendChild(label);
      }
      container.appendChild(filter);
    }

    container.appendChild(list);
    applyFilter();
    return held.length;
  }

  /* ------------------------------------------------------------------------
   * Rendering — the things that are not fragments
   * --------------------------------------------------------------------- */

  function renderLeads(container, leads) {
    if (!leads.length) return;
    const section = T.el('section', 'aside');
    section.appendChild(
      T.el('h2', 'section-heading', 'Believed to comment here, not yet acquired')
    );
    section.appendChild(
      T.el(
        'p',
        'aside-note',
        leads.length +
          ' works. This is an acquisition list, not commentary: no text of any ' +
          'of them is held, and none of them is shown above.'
      )
    );
    const list = T.el('ul', 'lead-list');
    for (const lead of leads) {
      const item = T.el('li', 'lead');
      item.appendChild(document.createTextNode(lead.author));
      item.appendChild(document.createTextNode(' — '));
      item.appendChild(T.el('span', 'lead-work', lead.title));
      if (lead.date) item.appendChild(document.createTextNode(' (' + lead.date + ')'));
      list.appendChild(item);
    }
    section.appendChild(list);
    container.appendChild(section);
  }

  function renderBlocked(container, file) {
    const blocked = (file && file.blocked) || [];
    if (!blocked.length) return;
    const section = T.el('section', 'aside');
    section.appendChild(
      T.el('h2', 'section-heading', 'Held, and not renderable yet')
    );
    for (const entry of blocked) {
      const node = T.el('div', 'blocked');
      const who = T.el('b', null, entry.author + ' — ' + entry.work);
      node.appendChild(who);
      node.appendChild(T.el('span', 'why', entry.reason));
      section.appendChild(node);
    }
    container.appendChild(section);
  }

  /**
   * Rule 4 — where the projection refuses, the page refuses.
   *
   * It shows the fragment against its canonical address and states that the
   * boundary in the selected edition is not established. It does not fall back
   * to the same verse number, which is precisely the wrong answer dressed as
   * the right one.
   */
  function renderRefusal(container, file, bible, book, chapter) {
    const here = ((file && file.refusals) || {})[bible.id] || [];
    if (!here.length) return;
    // The projection's own note is a clause, not a sentence, so it is set into
    // one here rather than printed as though it were prose. Nothing is added
    // to what it says.
    const note = String(here[0].note || '').replace(/\s+$/, '');
    const sentence = note ? note.charAt(0).toUpperCase() + note.slice(1) + '.' : '';
    const node = T.el('p', 'refusal');
    node.appendChild(T.el('strong', null, 'Boundary not established. '));
    node.appendChild(
      document.createTextNode(
        sentence +
          ' Commentary on ' +
          book.name +
          ' ' +
          chapter +
          ' is anchored in Vulgate numbering, and this page will not guess ' +
          'where the boundary moves to in ' +
          bible.label +
          '. The verse numbers you are reading correspond; the divisions of ' +
          'the text may not.'
      )
    );
    container.appendChild(node);
  }

  /* ------------------------------------------------------------------------
   * Assembly
   * --------------------------------------------------------------------- */

  async function render() {
    const token = bookSelect.value;
    const chapter = Number(chapterSelect.value);
    const bible = bibles.find((one) => one.id === bibleSelect.value) || bibles[0];
    const book = canonEntry(token);
    if (!book || !bible || !Number.isFinite(chapter)) return;

    const renderToken = T.beginRender();
    reading.setAttribute('aria-busy', 'true');

    reference.textContent = book.name + ' ' + chapter;
    referenceBook.textContent =
      book.testament === 'old' ? 'Old Testament' : 'New Testament';

    let file;
    let chapterResult;
    let marks;
    try {
      [file, chapterResult, marks] = await Promise.all([
        chapterFile(token, chapter),
        T.loadChapter(bible.id, token, chapter),
        chapterParagraphs(bible, token, chapter)
      ]);
    } catch (error) {
      T.fail('This chapter could not be loaded: ' + (error.message || error));
      return;
    }
    if (!T.isCurrentRender(renderToken)) return;

    fillLanguages(file);
    const leads = (file && file.leads) || [];
    T.clear(reading);
    renderRefusal(reading, file, bible, book, chapter);
    renderChapter(reading, bible, book, chapter, chapterResult, marks);
    const count = renderChain(reading, file, book);
    renderLeads(reading, leads);
    renderBlocked(reading, file);
    reading.setAttribute('aria-busy', 'false');

    T.clear(tally);
    tally.appendChild(T.el('b', null, count === 0 ? 'Nothing' : String(count)));
    tally.appendChild(
      document.createTextNode(
        (count === 0
          ? ' held here'
          : count === 1
            ? ' fragment held'
            : ' fragments held') +
          (leads.length ? ' · ' + leads.length + ' works not yet acquired' : '')
      )
    );

    T.statusLine(
      book.name + ' ' + chapter + ', ' + bible.label + ', ' + count + ' fragments.'
    );
    T.writeHash([
      ['book', token],
      ['chapter', String(chapter)],
      ['bible', bible.id],
      ['language', languageSelect.value],
    ]);
    updateSteps();
  }

  /**
   * The commentary-language control, filled from what this chapter actually
   * holds.
   *
   * The list is COUNTED, never assumed. A chapter held in Latin alone offers
   * Latin, and a reader whose selection is not held here keeps it — the chain
   * then says so and names what is held instead, rather than silently widening
   * to a language the reader did not ask for or hiding the author who is only
   * in the other one.
   */
  function fillLanguages(file) {
    const held = (file && file.languages) || [];
    const wanted = languageSelect.value;
    const items = [{ value: '', label: 'All languages' }];
    for (const code of held) items.push({ value: code, label: languageName(code) });
    if (wanted && !held.includes(wanted)) {
      items.push({ value: wanted, label: languageName(wanted) + ' — none here' });
    }
    T.fillSelect(languageSelect, items);
    languageSelect.value = wanted;
    languageSelect.disabled = held.length < 2 && !wanted;
  }

  function fillChapters(token, wanted) {
    const book = canonEntry(token);
    const count = book ? book.chapters : 0;
    const items = [];
    for (let n = 1; n <= count; n += 1) items.push({ value: String(n), label: String(n) });
    T.fillSelect(chapterSelect, items);
    chapterSelect.value = items.some((item) => item.value === String(wanted))
      ? String(wanted)
      : '1';
  }

  function updateSteps() {
    const book = canonEntry(bookSelect.value);
    const chapter = Number(chapterSelect.value);
    previousButton.disabled = !(book && chapter > 1);
    nextButton.disabled = !(book && chapter < book.chapters);
  }

  function step(delta) {
    const next = Number(chapterSelect.value) + delta;
    const book = canonEntry(bookSelect.value);
    if (!book || next < 1 || next > book.chapters) return;
    chapterSelect.value = String(next);
    render();
  }

  /* ------------------------------------------------------------------------
   * Start
   * --------------------------------------------------------------------- */

  async function start() {
    T.setInlineNotice(
      'No data root could be reached, so this page has nothing to show. Serve ' +
        'the pages over HTTP, or try ?data=fixture for the sample corpus.'
    );

    let manifest;
    try {
      [index, manifest, paragraphs] = await Promise.all([
        T.loadJSON(INDEX_PATH),
        T.loadBibles(),
        // The paragraph layer is optional in the strongest sense: a data root
        // without it serves the page, and the chapter runs on as it always did.
        T.loadJSON(PARAGRAPH_INDEX_PATH).catch((error) => {
          if (error instanceof T.NotFound) return null;
          throw error;
        })
      ]);
    } catch (error) {
      T.fail('The catena index could not be loaded: ' + (error.message || error));
      return;
    }
    if (!manifest.ok) {
      T.fail(manifest.message);
      return;
    }
    bibles = manifest.bibles;

    const hash = T.readHash();
    T.fillSelect(
      bookSelect,
      (index.canon || []).map((book) => ({ value: book.token, label: book.name }))
    );
    bookSelect.value = hash.get('book') || 'Gen';
    if (!bookSelect.value) bookSelect.value = (index.canon[0] || {}).token;
    fillChapters(bookSelect.value, hash.get('chapter') || 1);
    T.fillBibleSelect(bibleSelect, bibles);
    if (hash.get('bible') && bibles.some((one) => one.id === hash.get('bible'))) {
      bibleSelect.value = hash.get('bible');
    }

    if (hash.get('language')) languageSelect.value = hash.get('language');

    bookSelect.disabled = false;
    chapterSelect.disabled = false;
    bibleSelect.disabled = false;

    bookSelect.addEventListener('change', () => {
      fillChapters(bookSelect.value, 1);
      render();
    });
    chapterSelect.addEventListener('change', render);
    bibleSelect.addEventListener('change', render);
    languageSelect.addEventListener('change', render);
    previousButton.addEventListener('click', () => step(-1));
    nextButton.addEventListener('click', () => step(1));
    T.onArrowStep(step);
    T.onHashChange((next) => {
      if (next.get('book')) bookSelect.value = next.get('book');
      fillChapters(bookSelect.value, next.get('chapter') || 1);
      if (next.get('bible')) bibleSelect.value = next.get('bible');
      languageSelect.value = next.get('language') || '';
      render();
    });

    await render();
  }

  start();
}());
