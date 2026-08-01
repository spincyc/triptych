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

  const reference = document.getElementById('reference');
  const referenceBook = document.getElementById('reference-book');
  const tally = document.getElementById('tally');
  const reading = document.getElementById('reading');
  const bookSelect = document.getElementById('book-select');
  const chapterSelect = document.getElementById('chapter-select');
  const bibleSelect = document.getElementById('bible-select');
  const previousButton = document.getElementById('prev-button');
  const nextButton = document.getElementById('next-button');

  let index = null;
  let bibles = [];
  const bookFiles = new Map();
  // Authors the reader has switched OFF, held across chapters. Storing the
  // exclusions rather than the inclusions is what lets an author who does not
  // comment on the next chapter stay off rather than reappear checked.
  const hiddenAuthors = new Set();

  /* ------------------------------------------------------------------------
   * Data
   * --------------------------------------------------------------------- */

  function bookFile(token) {
    if (bookFiles.has(token)) return bookFiles.get(token);
    const pending = T.loadJSON('structure/catena/' + token + '.json').then(
      (file) => file,
      (error) => {
        // A book with neither a fragment nor a lead has no file at all. That is
        // an empty chapter, not a broken page.
        if (error instanceof T.NotFound) return null;
        throw error;
      }
    );
    bookFiles.set(token, pending);
    return pending;
  }

  function canonEntry(token) {
    return (index.canon || []).find((book) => book.token === token) || null;
  }

  /* ------------------------------------------------------------------------
   * Rendering — the chapter
   * --------------------------------------------------------------------- */

  function renderChapter(container, bible, book, chapter, result) {
    const section = T.el('section', 'chapter');
    if (!result.ok) {
      section.appendChild(T.notice(result.problem));
      container.appendChild(section);
      return;
    }
    const passage = T.el('p', 'passage');
    passage.lang = bible.language || 'en';
    const numbers = Object.keys(result.verses)
      .map(Number)
      .filter((n) => Number.isFinite(n))
      .sort((a, b) => a - b);
    if (!numbers.length) {
      section.appendChild(T.notice(book.name + ' ' + chapter + ' carries no verses.'));
      container.appendChild(section);
      return;
    }
    for (const number of numbers) {
      const verse = T.el('span', 'verse');
      verse.appendChild(T.el('sup', 'verse-num', String(number)));
      verse.appendChild(document.createTextNode(result.verses[String(number)] + ' '));
      passage.appendChild(verse);
    }
    // Collapsible like the fragments, but OPEN by default: the chapter is what
    // the page is about, and the commentary is what is read against it. A
    // reader closes it to compare several fathers without the text between.
    const holder = document.createElement('details');
    holder.className = 'chapter-body';
    holder.open = true;
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
    holder.appendChild(head);
    holder.appendChild(passage);
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
    // control is keyboard-reachable and the text is still findable by the
    // browser's own search. The summary carries author, work, date and extent,
    // which is what makes a closed chain worth reading on its own: it becomes a
    // chronological index of who comments here and how far each one reaches.
    const details = document.createElement('details');
    details.className = 'fragment-body';

    const head = document.createElement('summary');
    head.className = 'fragment-head';
    head.appendChild(T.el('span', 'fragment-author', fragment.author));
    head.appendChild(T.el('span', 'fragment-work', fragment.work));
    if (fragment.date !== null && fragment.date !== undefined) {
      head.appendChild(T.el('span', 'fragment-date', String(fragment.date)));
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

    const text = T.el('p', 'fragment-text', fragment.text);
    text.lang = fragment.language || 'en';
    details.appendChild(text);

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
    details.appendChild(source);
    item.appendChild(details);
    return item;
  }

  function renderChain(container, file, book, chapter) {
    const held = file ? M.fragmentsOnChapter(file.fragments || [], chapter) : [];
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
        T.el('p', 'aside-note', 'No commentary on this chapter is held yet.')
      );
      return 0;
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

  function renderLeads(container, file, chapter) {
    const leads = ((file && file.leads) || {})[String(chapter)] || [];
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

  function renderBlocked(container, file, chapter) {
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
    const forEdition = ((file && file.refusals) || {})[bible.id] || [];
    const here = forEdition.filter((row) => Number(row.chapter) === Number(chapter));
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
    try {
      [file, chapterResult] = await Promise.all([
        bookFile(token),
        T.loadChapter(bible.id, token, chapter)
      ]);
    } catch (error) {
      T.fail('This chapter could not be loaded: ' + (error.message || error));
      return;
    }
    if (!T.isCurrentRender(renderToken)) return;

    T.clear(reading);
    renderRefusal(reading, file, bible, book, chapter);
    renderChapter(reading, bible, book, chapter, chapterResult);
    const count = renderChain(reading, file, book, chapter);
    renderLeads(reading, file, chapter);
    renderBlocked(reading, file, chapter);
    reading.setAttribute('aria-busy', 'false');

    const leads = ((file && file.leads) || {})[String(chapter)] || [];
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
      ['bible', bible.id]
    ]);
    updateSteps();
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
      [index, manifest] = await Promise.all([T.loadJSON(INDEX_PATH), T.loadBibles()]);
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

    bookSelect.disabled = false;
    chapterSelect.disabled = false;
    bibleSelect.disabled = false;

    bookSelect.addEventListener('change', () => {
      fillChapters(bookSelect.value, 1);
      render();
    });
    chapterSelect.addEventListener('change', render);
    bibleSelect.addEventListener('change', render);
    previousButton.addEventListener('click', () => step(-1));
    nextButton.addEventListener('click', () => step(1));
    T.onArrowStep(step);
    T.onHashChange((next) => {
      if (next.get('book')) bookSelect.value = next.get('book');
      fillChapters(bookSelect.value, next.get('chapter') || 1);
      if (next.get('bible')) bibleSelect.value = next.get('bible');
      render();
    });

    await render();
  }

  start();
}());
