/* The catena page — a chapter, and every fragment held on it, oldest
 * first. NOT THIS FILE'S, AND MUST NOT BECOME IT: what belongs to a
 * chapter (`catena-model.js`), numbering (refusals arrive as data), rights
 * and confidence filtering (the generator's guards). The book file is a
 * SPINE: a fragment's text is its own file, fetched when opened, so
 * unfetched text is beyond find-in-page and the page says so. */

'use strict';

(function () {
  const T = window.Triptych;
  const M = window.CatenaModel;
  const textNode = (said) => document.createTextNode(said);
  // The typed boundary — asked, and explained, in `catena-model.js`.
  const { sound, bag } = M;

  const { voiceLabel } = M;
  M.useLanguageNames(T.languageName);

  const reference = document.getElementById('reference');
  const referenceBook = document.getElementById('reference-book');
  const tally = document.getElementById('tally');
  const reading = document.getElementById('reading');
  const bookSelect = document.getElementById('book-select');
  const chapterSelect = document.getElementById('chapter-select');
  const bibleSelect = document.getElementById('bible-select');
  // `#language-select` in the markup, and stays so: the id is older
  // than the axis; the hash key is `voice`.
  const voiceSelect = document.getElementById('language-select');
  const prevButton = document.getElementById('prev-button');
  const nextButton = document.getElementById('next-button');
  const controlsDisclosure = document.getElementById('controls-filter');

  let index = null;
  let bibles = [];
  // The three roots an address is judged against, read once; `whole` is
  // whether each could be read entire. `M.canonRoot` says why that matters.
  let canon = { books: [], whole: false };
  let voices = { keys: [], whole: false };
  let editions = { bibles: [], whole: false };
  const chapterFiles = new Map();
  const fragmentTexts = new Map();
  const paragraphFiles = new Map();
  let paragraphs = null;
  // Authors switched OFF — exclusions, so they persist across chapters.
  const hiddenAuthors = new Set();
  // A voice a link asked for, held until a control that can hold it exists.
  let wantedVoice = '';
  // True while an invalid-address notice is up; it matches no hash.
  let showingError = false;
  // The next render answers an ARRIVING address, not a reader action.
  let arrival = false;
  // THE 404, AS A VALUE, because `null` cannot be it: JSON `null` is a valid
  // document. Resolved to `undefined` before the model sees it: a sentinel a
  // payload could carry would be one a payload could forge.
  const ABSENT = { absent: true };
  const seen = (file) => (file === ABSENT ? undefined : file);

  /* --------------------------------------------------------------- data */

  // Off the root read at startup: one reading of the canon, one answer.
  function canonEntry(token) {
    const wanted = sound(token);
    return canon.books.find((one) => one.token === wanted) || null;
  }

  // One promise per path. A 404 is an ANSWER, kept as `absent`; any
  // other failure is EVICTED, so a retry — or a reload — really asks again.
  function cached(map, path, absent) {
    if (map.has(path)) return map.get(path);
    const pending = T.loadJSON(path).then(
      (file) => file,
      (error) => {
        if (error instanceof T.NotFound && absent !== undefined) return absent;
        map.delete(path);
        throw error;
      }
    );
    map.set(path, pending);
    return pending;
  }

  // The spine for one chapter: nothing held means NO FILE, no request.
  // A 404 on a LISTED chapter is a broken record, not emptiness — marked,
  // and so is an index this page cannot read.
  function chapterFile(token, chapter) {
    const path = M.chapterPath(index, token, chapter);
    if (!path) return Promise.resolve(path === null ? { unfetched: 'the index record' } : null);
    // A 200 CARRYING A DOCUMENT THAT IS NOT A SPINE IS NOT AN EMPTY CHAPTER.
    // `null`, a list and a string are all valid JSON, so the request succeeded
    // and every derivation off the payload then answered nothing — and the
    // page printed "No commentary on this chapter is held yet" over a chapter
    // its own index says holds commentary. The same manufactured negative the
    // index record already had a third answer for.
    return cached(chapterFiles, path, { unfetched: path })
      .then((file) => (M.spineUnreadable(file) ? { unfetched: path } : file));
  }

  // Where this edition opens a paragraph. The layer is the EDITION's —
  // a chapter that runs on has no file, so the 404 is the answer. An
  // unstatable path is not requested.
  function chapterParagraphs(bible, token, chapter) {
    const path = M.paragraphPath(paragraphs, bible.id, bag(canonEntry(token)).path, chapter);
    // `null` is the layer ROOT unreadable, not the 404 that means this
    // chapter runs on; carried in the route's own `unfetched`.
    // A layer that would not come is not a chapter that runs on, and the
    // fetch for an OPTIONAL record may not decide the page: a transport fault
    // on one paragraph file lost the Scripture and 107 fragments with it.
    return path === null ? Promise.resolve({ unfetched: true })
      : path ? cached(paragraphFiles, path, ABSENT)
        .then(seen, () => ({ unfetched: true }))
      : Promise.resolve(undefined);
  }

  // One fragment's prose — keyed by the path the SPINE gave, never
  // assembled from an id. Even its 404 is evicted: retry is real.
  function fragmentText(path) {
    if (!path) return Promise.resolve(ABSENT);
    return cached(fragmentTexts, path);
  }


  /* ------------------------------------------------- the chapter */

  function renderChapter(container, bible, book, chapter, result, marks) {
    const section = T.el('section', 'chapter');
    if (!result.ok) {
      section.appendChild(T.notice(result.problem));
      container.appendChild(section);
      return;
    }
    // Unreadable text is not a chapter with no verses, and an unreadable
    // paragraph record is not an edition that opens none here.
    const read = M.chapterReading(result.verses, marks);
    const lines = read.lines;
    if (!lines.length) {
      section.appendChild(T.notice(book.name + ' ' + chapter +
        (read.versesUnread
          ? ' arrived in a form this page cannot read.'
          : ' carries no verses.')));
      container.appendChild(section);
      return;
    }

    // Prose — a stack of verse-lines is a concordance.
    const body = T.el('div', 'passage');
    // OMITTED, NEVER GUESSED: `|| 'en'` made an unreadable language English.
    if (bible.language) body.lang = bible.language;
    let passage = null;
    let printed = 0;
    let projected = 0;
    let opened = 0;
    for (const line of lines) {
      if (!passage || line.kind) {
        passage = T.el('p', 'passage-paragraph');
        opened += 1;
        if (line.kind === 'printed') printed += 1;
        if (line.kind === 'projected') { passage.classList.add('projected'); projected += 1; }
        body.appendChild(passage);
      }
      const verse = T.el('span', 'verse');
      verse.appendChild(T.el('sup', 'verse-num', String(line.number)));
      verse.appendChild(textNode(line.text + ' '));
      passage.appendChild(verse);
    }
    // OPEN — closed dated from the stacked layout; still a `details`.
    const holder = T.el('details', 'chapter-body');
    holder.open = true;
    const head = T.el('summary', 'chapter-head');
    head.appendChild(T.el('span', 'chapter-name', book.name + ' ' + chapter));
    head.appendChild(T.el('span', 'chapter-count',
      lines.length + (lines.length === 1 ? ' verse' : ' verses')));
    // The chip counts the PARAGRAPHS on the page, not the recorded
    // breaks: the first opens unmarked.
    if (printed + projected) {
      head.appendChild(T.el('span', 'chapter-count',
        opened + (opened === 1 ? ' paragraph' : ' paragraphs')));
    }
    holder.appendChild(head);
    holder.appendChild(body);
    // Printed and projected marks are different claims; the note counts
    // BREAKS, in those words.
    if (printed + projected) {
      const parts = [];
      if (printed) {
        parts.push(printed + (printed === 1 ? ' break is' : ' breaks are') +
          ' printed in this edition');
      }
      if (projected) {
        parts.push(projected + (projected === 1 ? ' is' : ' are') +
          ' projected from the witnesses that concur, and marked');
      }
      holder.appendChild(
        T.el('p', 'paragraph-note', 'Paragraphs: ' + parts.join('; ') + '.'));
    } else {
      holder.appendChild(T.el('p', 'paragraph-note',
        read.marksUnread
          ? 'The paragraph record for this chapter in this edition could not be ' +
              'read, so whether it divides the chapter is not established here.'
          : 'No paragraph division is held for this chapter in this edition, so it ' +
              'runs on. Another edition’s paragraphs are not borrowed for it.'));
    }
    section.appendChild(holder);
    container.appendChild(section);
  }

  /* ---------------------------------------------------------- the chain
   * Rule 6: a fragment shown under a chapter it only reaches into still
   * says where it runs. */

  // A licence travels ABOVE the words, so a copied selection carries the
  // condition; nothing is invented for a bare `licensed`.
  function licence(note) {
    const block = T.el('p', 'fragment-acknowledgement');
    block.appendChild(T.el('strong', null, 'Licence: '));
    block.appendChild(textNode(note));
    return block;
  }

  function renderFragment(fragment, bookName) {
    const item = T.el('li', 'fragment');
    item.setAttribute('data-state', 'held');

    // `details`, not a scripted toggle: keyboard-reachable as served.
    const details = T.el('details', 'fragment-body');

    const head = T.el('summary', 'fragment-head');
    // EVERY FIELD HERE IS ALREADY TYPED: `M.chapterFragments` projects, and
    // carries no field this function does not render.
    head.appendChild(T.el('span', 'fragment-author', fragment.author));
    head.appendChild(T.el('span', 'fragment-work', fragment.work));
    if (fragment.date) head.appendChild(T.el('span', 'fragment-date', fragment.date));
    // The language, and WHOSE it is; an unestablished voice says only it.
    // Derived beside the other typed prose, so the two cannot drift.
    const code = fragment.language;
    const named = M.languageChip(fragment);
    if (named) head.appendChild(T.el('span', 'fragment-language', named));
    // A TALLY IS A NUMBER THE RECORD WROTE, not one `Number()` can make.
    const words = fragment.text_words;
    if (words) {
      head.appendChild(T.el('span', 'fragment-length',
        words.toLocaleString() + ' words'));
    }

    const extent = T.el('span', 'fragment-extent', M.formatExtent(fragment.extent, bookName));
    if (M.spansChapters(fragment.extent)) {
      extent.appendChild(textNode(' '));
      extent.appendChild(T.el('span', 'spans', '— runs across the chapter boundary'));
    }
    head.appendChild(extent);
    details.appendChild(head);

    // Prose arrives on first open; a failure reports against this fragment.
    const text = T.el('p', 'fragment-text', 'Loading…');
    // THE SINK THE V4.1 REVIEW REPLAYED — omitted where unstated, not guessed.
    if (code) text.lang = code;
    details.appendChild(text);
    const apparatus = T.el('div', 'fragment-apparatus');
    details.appendChild(apparatus);

    // ONE point-of-use acknowledgement channel: two VALID supplies render ONE
    // block, and a broken note — said to be broken once — cannot claim the
    // channel and erase a valid note the other supply carries.
    let acknowledged = 0;
    // `awry`: something was recorded and is not text — kept apart from the
    // note so a malformed supply still says so instead of reading as none.
    const acknowledge = (note, awry) => {
      if (acknowledged > 1 || !(note || awry)) return;
      if (!note && acknowledged) return;
      acknowledged = note ? 2 : 1;
      details.insertBefore(
        note
          ? licence(note)
          : T.el('p', 'fragment-acknowledgement',
              'The recorded acknowledgement is malformed and not shown.'),
        text);
    };
    acknowledge(fragment.acknowledgement, fragment.acknowledgement_broken);

    let asked = false;
    details.addEventListener('toggle', () => {
      if (!details.open || asked) return;
      asked = true;
      // THE REFUSAL IS TERMINAL, consumed before the sink: no path —
      // carried, cached or late — may answer a claim the page declined.
      if (fragment.text_refused) {
        text.className = 'fragment-text missing';
        text.textContent = fragment.text_note;
        return;
      }
      fragmentText(fragment.text_path).then(
        (loaded) => {
          // A completion for a rebuilt page mutates nothing here.
          if (!reading.contains(details)) return;
          // No file, or a file: a 200 answering `null` is the second.
          if (loaded === ABSENT) {
            text.className = 'fragment-text missing';
            text.textContent =
              'This fragment carries no text file, so nothing of it can be shown.';
            return;
          }
          // PROJECTED, not read field by field: an unreadable payload used
          // to render an empty paragraph and report nothing.
          const body = M.textPayload(loaded);
          acknowledge(body.acknowledgement, body.acknowledgement_broken);
          if (body.unreadable) {
            text.className = 'fragment-text missing';
            text.textContent =
              'The text of this fragment arrived in a form this page cannot read.';
            return;
          }
          text.className = 'fragment-text';
          text.textContent = body.text;
          if (body.basis) {
            apparatus.appendChild(T.el('p', 'fragment-basis', 'Extent — ' + body.basis));
          }
          if (body.date_basis) {
            apparatus.appendChild(T.el('p', 'fragment-basis', 'Date — ' + body.date_basis));
          }
        },
        (error) => {
          if (!reading.contains(details)) return;
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

    // Provenance, whether or not the text loads: every fact the spine carries.
    const source = T.el('p', 'fragment-source');
    source.appendChild(textNode(fragment.locator));
    const fact = (said) => {
      if (!said) return;
      source.appendChild(T.el('span', 'sep'));
      source.appendChild(textNode(said));
    };
    fact(fragment.edition);
    fact(fragment.edition_published);
    const hands = fragment.translators.join(', ');
    if (hands) fact('tr. ' + hands);
    fact(fragment.rights);
    fact(fragment.attribution);
    // EVERY supplied fact renders: an acknowledgement does not suppress a
    // recorded rights basis — that precedence hid supplied terms.
    fact(fragment.rights_basis);
    // The weaker review state gets the word — printing `inspected` and
    // `verified` alike would claim a collation nobody made.
    if (fragment.review && fragment.review !== 'verified') {
      source.appendChild(T.el('span', 'sep'));
      source.appendChild(T.el('span', 'state', fragment.review + ', not collated'));
    }
    // THE HREF IS PINNED by `test_browser_url_contract.py`.
    if (fragment.id) {
      source.appendChild(T.el('span', 'sep'));
      const whole = T.el('a', 'fragment-whole', 'Open this passage in the Source Library');
      whole.href = '../sources/#passage=' + encodeURIComponent(fragment.id);
      source.appendChild(whole);
    }
    details.appendChild(source);
    item.appendChild(details);
    return item;
  }

  // Why the works standing here miss the asked-for language; unsaid, the
  // page reads as a load failure. Partly public domain is SOME, counted
  // apart; the findings themselves are the generator's.
  function renderAbsences(container, file, wanted) {
    const asked = M.parseVoiceKey(wanted);
    if (!asked || asked.voice !== M.TRANSLATION) return;
    // THE TYPED FINDING DECIDES WHAT MAY BE SAID: dropped, it read
    // `not-surveyed` as a holdings negative.
    const rows = M.absenceRows(index, file, asked.language);
    // An unreadable absences root is not a corpus with nothing to say.
    if (!rows.length) {
      const unread = M.absencesUnread(index);
      if (unread) container.appendChild(T.el('p', 'aside-note', unread));
      return;
    }

    const note = T.el('details', 'absence-note');
    // The absence contract is not deferrable: the findings stand OPEN, and
    // the disclosure only lets a reader fold them away.
    note.open = true;
    note.setAttribute('data-state', 'absence');
    const language = M.sayLanguage(asked.language);
    const head = document.createElement('summary');
    head.textContent = M.absenceSummary(rows, language);
    note.appendChild(head);
    const items = T.el('ul', 'absence-list');
    for (const row of rows) {
      const item = T.el('li', 'absence');
      item.appendChild(T.el('span', 'absence-author', row.author));
      item.appendChild(T.el('span', 'absence-work', row.work));
      if (row.reason) item.appendChild(T.el('p', 'absence-reason', row.reason));
      // Only the finding that says so in its own name licenses the offer.
      if (row.offer) item.appendChild(T.el('p', 'absence-partial', row.offer));
      items.appendChild(item);
    }
    note.appendChild(items);
    container.appendChild(note);
  }

  function renderChain(container, file, book, blockedHeld) {
    // Already the chapter's own list: the derivation is the model's.
    const all = M.chapterFragments(file);
    const wanted = voiceSelect.value;
    const held = all.filter((one) => M.matchesVoice(one, wanted));
    const headingText =
      held.length === 0
        ? 'Commentary held here'
        : held.length === 1
          ? 'One fragment held here'
          : held.length + ' fragments held here';
    const heading = T.el('h2', 'section-heading', headingText);
    container.appendChild(heading);
    if (!held.length) {
      // Rule 1: no fragments shows no fragments, said plainly. The sentence
      // is the model's, beside the counts it is derived from.
      container.appendChild(T.el('p', 'aside-note',
        M.emptyChainNote(all.length, blockedHeld, wanted, M.chapterVoices(file))));
      renderAbsences(container, file, wanted);
      return 0;
    }

    if (wanted) {
      const said = M.otherVoicesNote(wanted,
        M.chapterVoices(file).filter((one) => one.key !== wanted));
      if (said) container.appendChild(T.el('p', 'aside-note', said));
      renderAbsences(container, file, wanted);
    }

    // Grouped WITHOUT reordering: only a CONTIGUOUS author+date run shares
    // a heading — by-author grouping misfiled Augustine's 417 before 401.
    const groups = [];
    for (const fragment of held) {
      const author = fragment.author;
      const date = fragment.date || null;
      const last = groups[groups.length - 1];
      // Unnamed is not a name to group by: two unnamed fragments are not one man.
      if (author && last && last.author === author && last.date === date) {
        last.fragments.push(fragment);
      } else {
        groups.push({ author: author, date: date, fragments: [fragment] });
      }
    }

    const chain = T.el('ul', 'chain');
    const rendered = [];
    // The first group opens: all closed reads as nothing, all open as
    // a wall. No request either way.
    let first = true;
    for (const group of groups) {
      const item = T.el('li', 'author');
      const node = T.el('details', 'author-body');
      if (first) {
        node.open = true;
        first = false;
      }

      const summary = T.el('summary', 'author-head');
      summary.appendChild(T.el('span', 'author-name', group.author));
      if (group.date !== null) {
        summary.appendChild(T.el('span', 'author-date', String(group.date)));
      }
      summary.appendChild(T.el('span', 'author-count',
        group.fragments.length === 1
          ? '1 fragment'
          : group.fragments.length + ' fragments'));
      node.appendChild(summary);

      const inner = T.el('ul', 'author-fragments');
      for (const fragment of group.fragments) {
        inner.appendChild(renderFragment(fragment, book.name));
      }
      node.appendChild(inner);
      item.appendChild(node);
      chain.appendChild(item);
      rendered.push({ author: group.author, item, count: group.fragments.length });
    }

    // One toggle per AUTHOR, though he may stand at several dates.
    // Only a NAMED author gets a switch: `hiddenAuthors` persists across
    // chapters, so a key of '' hid every author-less fragment in the corpus.
    const authors = [...new Set(rendered.map((row) => row.author).filter(Boolean))];

    let filterHolder = null;

    // DESELECTED authors; hiding, not rebuilding, keeps nodes open.
    function applyFilter() {
      let shown = 0;
      for (const row of rendered) {
        const on = !(row.author && hiddenAuthors.has(row.author));
        row.item.hidden = !on;
        if (on) shown += row.count;
      }
      // The heading counts what is HELD; when the filter hides everything
      // the page says so and opens the control that undoes it.
      heading.textContent =
        shown === held.length ? headingText : headingText + ' — ' + shown + ' shown';
      if (!shown && filterHolder) {
        heading.textContent =
          headingText + ' — none shown; every author is switched off below';
        filterHolder.open = true;
      }
    }

    // The filter exists when there is anyone to choose between AND when
    // a carried-over exclusion touches this chapter: a sole author
    // switched off elsewhere still gets his switch.
    const hiddenHere = authors.some((name) => hiddenAuthors.has(name));
    if (authors.length > 1 || hiddenHere) {
      const filter = T.el('div', 'author-filter');
      filter.setAttribute('role', 'group');
      filter.setAttribute('aria-label', 'Authors shown');
      for (const name of authors) {
        const label = T.el('label', 'author-toggle');
        const box = document.createElement('input');
        box.type = 'checkbox';
        box.checked = !hiddenAuthors.has(name);
        box.addEventListener('change', () => {
          if (box.checked) hiddenAuthors.delete(name);
          else hiddenAuthors.add(name);
          applyFilter();
        });
        label.appendChild(box);
        label.appendChild(textNode(name));
        filter.appendChild(label);
      }
      // Folded away — twenty checkboxes were the first screen.
      filterHolder = T.el('details', 'author-filter-disclosure');
      filterHolder.appendChild(T.el('summary', null, 'Filter authors'));
      filterHolder.appendChild(filter);
      if (hiddenHere) filterHolder.open = true;
      container.appendChild(filterHolder);
    }

    container.appendChild(chain);
    applyFilter();
    return held.length;
  }

  /* ----------------------------------- the things that are not fragments */

  // UNRECONCILED LEAD ENTRIES — what one is, and is not, is the model's.
  function renderLeads(container, leads) {
    if (!leads.length) return;
    const section = T.el('section', 'aside');
    section.setAttribute('data-state', 'lead');
    section.appendChild(
      T.el('h2', 'section-heading', 'Believed to comment here — the acquisition list'));
    section.appendChild(
      T.el('p', 'aside-note',
        leads.length +
          (leads.length === 1 ? ' unreconciled lead entry' : ' unreconciled lead entries') +
          ' on the acquisition record for this chapter, which omits its ' +
          'confidence. An entry establishes no distinct work, no possession ' +
          'and nothing renderable, and the list is not checked against the ' +
          'commentary above.'));
    const items = T.el('ul', 'lead-list');
    // The model's members: naming nothing is no entry, and enters no count.
    for (const lead of leads) {
      const item = T.el('li', 'lead');
      if (lead.who) item.appendChild(textNode(lead.who + ' — '));
      item.appendChild(T.el('span', 'lead-work', lead.title));
      if (lead.when) item.appendChild(textNode(' (' + lead.when + ')'));
      items.appendChild(item);
    }
    section.appendChild(items);
    container.appendChild(section);
  }

  function renderBlocked(container, blocked) {
    if (!blocked.length) return;
    const section = T.el('section', 'aside');
    section.appendChild(T.el('h2', 'section-heading', 'Held, and not renderable yet'));
    for (const entry of blocked) {
      const node = T.el('div', 'blocked');
      node.setAttribute('data-state', 'blocked');
      if (entry.named) node.appendChild(T.el('b', null, entry.named));
      if (entry.why) node.appendChild(T.el('span', 'why', entry.why));
      section.appendChild(node);
    }
    container.appendChild(section);
  }

  // Rule 4 — where the projection refuses, the page refuses; no
  // same-number fallback dressed right.
  function renderRefusal(container, file, bible, book, chapter) {
    // A REFUSAL IS A RECORD THAT STATES ONE: `{}` refuses nothing at all.
    const sentence = M.refusalNote(file, bible.id, chapter);
    if (!sentence) return;
    const node = T.el('p', 'refusal');
    node.setAttribute('data-state', 'refusal');
    node.appendChild(T.el('strong', null, 'Boundary not established. '));
    node.appendChild(textNode(
      sentence + ' Commentary on ' + book.name + ' ' + chapter +
        ' is anchored in Vulgate numbering, and this page will not guess ' +
        'where the boundary moves to in ' + bible.label +
        '. The verse numbers you are reading correspond; the divisions of ' +
        'the text may not.'));
    container.appendChild(node);
  }

  /* ------------------------------------ the cited state, failing closed
   * A value this page cannot honour is never traded for a default: the URL
   * keeps the reader's text; recovery is a link and the controls. */

  function errorSection(title) {
    const section = T.el('section', 'catena-error');
    section.setAttribute('data-state', 'error');
    section.appendChild(T.el('h2', 'section-heading', title));
    return section;
  }

  // Focus is never stranded on a removed node: a rebuild that swallows the
  // focused element (the recovery link, a failing load) hands focus to the
  // reading region; focus outside it stays the reader's.
  function focusKeeper() {
    const lost = reading.contains(document.activeElement);
    return () => { if (lost) reading.focus(); };
  }

  function renderInvalid(bad) {
    T.beginRender();
    showingError = true;
    const refocus = focusKeeper();
    fillVoices(null, true);
    reference.textContent = 'Address not used';
    referenceBook.textContent = '';
    T.clear(tally);
    T.clear(reading);
    const section = errorSection('This address cannot be used as written');
    for (const one of bad) {
      const row = T.el('p', 'error-detail');
      row.appendChild(T.el('code', null, one.key + '=' + one.value));
      row.appendChild(textNode(' ' + one.note + '.'));
      section.appendChild(row);
    }
    const recover = T.el('p', 'error-recovery');
    recover.appendChild(textNode('The address is left as written. '));
    const link = T.el('a', null, 'Open the nearest valid page');
    link.href = currentHashText();
    recover.appendChild(link);
    recover.appendChild(textNode(', or change a control above.'));
    section.appendChild(recover);
    reading.appendChild(section);
    reading.setAttribute('aria-busy', 'false');
    refocus();
    T.statusLine('The address is unchanged; the values not used are listed.');
  }

  /* ----------------------------------------------------------- assembly */

  async function render() {
    const wasArrival = arrival;
    arrival = false;
    // A reader action supersedes a parked arrival — and its deep-linked
    // voice, which may not ride the reader's own render into history.
    if (!wasArrival) wantedVoice = '';
    const token = bookSelect.value;
    const chapter = Number(chapterSelect.value);
    const bible = bibles.find((one) => one.id === bibleSelect.value);
    const book = canonEntry(token);
    // A SILENT RETURN IS NOT A TERMINAL STATE: reached from a malformed
    // index, this left "Loading…" standing and said nothing.
    if (!book || !bible || !Number.isFinite(chapter)) {
      startFailed('The catena index could not be read.');
      return;
    }

    const renderToken = T.beginRender();
    reading.setAttribute('aria-busy', 'true');

    reference.textContent = book.name + ' ' + chapter;
    // '' where the canon states no testament; an `else` printed "New".
    referenceBook.textContent = book.testamentName;

    // ONE FUNNEL after the address is claimed: outside it, a throw in the tail
    // stranded `aria-busy`, focus, the tally and the route. The keeper is taken
    // BEFORE the work, or it reads an emptied page and sees no loss.
    const refocus = focusKeeper();
    let file, chapterResult, marks;
    try {
      [file, chapterResult, marks] = await Promise.all([
        chapterFile(token, chapter),
        T.loadChapter(bible.id, token, chapter),
        chapterParagraphs(bible, token, chapter)
      ]);
      if (!T.isCurrentRender(renderToken)) return;

      // An expected spine that would not come is an error, not an absence.
      // `sound`: it reaches a reader inside a sentence, and a payload
      // carrying `unfetched: {…}` printed "[object Object]" there.
      const unfetched = sound(bag(file).unfetched);
      if (unfetched) file = null;

      // ONE typed truth beside the chapter: every tally, empty, blocked
      // and voice claim derives from these counts — held-but-unrenderable
      // is HELD, never "nothing".
      const blocked = M.chapterBlocked(file);
      const leads = M.chapterLeads(file);
      const total = M.chapterFragments(file).length;
      fillVoices(file, unfetched || blocked.length);
      T.clear(reading);
      let count = 0;
      renderRefusal(reading, file, bible, book, chapter);
      renderChapter(reading, bible, book, chapter, chapterResult, marks);
      if (unfetched) {
        const section = errorSection('This chapter’s commentary record did not load');
        section.appendChild(T.el('p', 'error-detail',
          'The index records commentary on ' + book.name + ' ' + chapter +
            ', but its record (' + unfetched + ') could not be read — a ' +
            'data or connection fault, not an empty ' +
            'chapter. Reloading may recover it.'));
        reading.appendChild(section);
      } else {
        // One wrapper for all that is not the chapter, for the wide grid.
        const column = T.el('div', 'chain-column');
        count = renderChain(column, file, book, blocked.length);
        renderLeads(column, leads);
        renderBlocked(column, blocked);
        reading.appendChild(column);
      }
      reading.setAttribute('aria-busy', 'false');
      refocus();

      // The tally states the corpus, never the filter, and the announcement
      // is the same clauses in the same order — one derivation, so the two
      // cannot disagree rather than being asserted not to.
      T.clear(tally);
      const said = M.chapterSummary({
        total: total, shown: count, blocked: blocked.length,
        leads: leads.length, unfetched: !!unfetched, voice: voiceSelect.value
      });
      if (said.bold) tally.appendChild(T.el('b', null, said.bold));
      tally.appendChild(textNode(said.tail));
      T.statusLine(
        book.name + ' ' + chapter + ', ' + bible.label + ', ' + said.spoken + '.');
      writeRoute(wasArrival);
    } catch (error) {
      // Stale proves nothing: only the owning render may show a failure.
      if (!T.isCurrentRender(renderToken)) return;
      fillVoices(null, true);
      T.clear(tally);
      T.fail('This chapter could not be loaded: ' + (error.message || error));
      refocus();
      writeRoute(wasArrival);
    }
  }

  // History. A reader ACTION pushes an entry; an ARRIVAL never may: a
  // partial one is completed in place, a value-identical one stays byte for
  // byte. Success and failure both come here; URL, controls, page agree.
  function writeRoute(wasArrival) {
    showingError = false;
    updateSteps();
    const now = T.readHash();
    const identical =
      now.get('book') === bookSelect.value &&
      Number(now.get('chapter')) === Number(chapterSelect.value) &&
      now.get('bible') === bibleSelect.value &&
      (now.get('voice') || '') === voiceSelect.value;
    if (identical) return;
    if (wasArrival && window.history.replaceState) {
      window.history.replaceState(null, '', currentHashText());
    } else {
      // The reader's step pushes through the shared writer — the published
      // grammar — and the text is remembered so its echo is consumed.
      selfWrote = currentHashText();
      T.writeHash([['book', bookSelect.value], ['chapter', chapterSelect.value],
                   ['bible', bibleSelect.value], ['voice', voiceSelect.value]]);
    }
  }

  // The voice control, COUNTED from what this chapter holds, never
  // assumed. An unheld selection is KEPT; the chain says so.
  function fillVoices(file, unknown) {
    const held = M.chapterVoices(file);
    // The reader's own selection first; a deep-linked voice only before it.
    const wanted = voiceSelect.value || wantedVoice;
    wantedVoice = '';
    const items = [{ value: '', label: 'Everything held' }];
    for (const entry of held) items.push({ value: entry.key, label: voiceLabel(entry) });
    if (wanted && !held.some((one) => one.key === wanted)) {
      // `unknown`: an invalid address, unloadable record, failed load or
      // a standing blocked row — none proves absence, so no "none here".
      items.push({
        value: wanted,
        label: voiceLabel(M.parseVoiceKey(wanted)) + (unknown ? '' : ' — none here')
      });
    }
    T.fillSelect(voiceSelect, items);
    voiceSelect.value = wanted;
    voiceSelect.disabled = held.length < 2 && !wanted;
  }

  function fillChapters(token, wanted) {
    const book = canonEntry(token);
    const count = book ? book.chapters : 0;
    const items = [];
    for (let n = 1; n <= count; n += 1) items.push({ value: String(n), label: String(n) });
    T.fillSelect(chapterSelect, items);
    // THE NUMBER IT DENOTES, not the spelling: `#chapter=007` carried no
    // option, so the page showed chapter 1 and rewrote the address to say so.
    chapterSelect.value = String(Number(wanted) || wanted);
    if (!chapterSelect.value) chapterSelect.value = '1';
  }

  function updateSteps() {
    const book = canonEntry(bookSelect.value);
    const chapter = Number(chapterSelect.value);
    prevButton.disabled = !(book && chapter > 1);
    nextButton.disabled = !(book && chapter < book.chapters);
  }

  function step(delta) {
    const next = Number(chapterSelect.value) + delta;
    const book = canonEntry(bookSelect.value);
    if (!book || next < 1 || next > book.chapters) return;
    chapterSelect.value = String(next);
    render();
  }

  /* ------------------------------ history, route-owned and deterministic
   * Not `T.onHashChange`: its remembered write goes stale after Back and
   * swallows Forward. `selfWrote` holds this route's own last write until its
   * echo consumes it: an echo judged against the CURRENT controls reverted a
   * reader who had already acted. All else arrives. */

  let selfWrote = null;

  // Exactly what `T.writeHash` writes for these controls, so a remembered
  // write matches its own echo. `voice`, not `language`: an old link opens
  // on everything held.
  function currentHashText() {
    const parts = [];
    for (const pair of [['book', bookSelect.value], ['chapter', chapterSelect.value],
                        ['bible', bibleSelect.value], ['voice', voiceSelect.value]]) {
      if (pair[1]) parts.push(pair[0] + '=' + encodeURIComponent(pair[1]));
    }
    return parts.length ? '#' + parts.join('&') : '';
  }

  // One seeding for EVERY arrival, cold or not: the controls take the
  // ADDRESS's route — sound values kept, the rest defaulted, nothing
  // borrowed from a leftover selection.
  function seedControls(hash, broken) {
    bookSelect.value = (!broken.has('book') && hash.get('book')) || 'Gen';
    if (!bookSelect.value) bookSelect.value = bag(canon.books[0]).token;
    fillChapters(bookSelect.value, broken.has('chapter') ? 1 : hash.get('chapter') || 1);
    bibleSelect.value =
      (!broken.has('bible') && hash.get('bible')) || (bibles[0] || {}).id || '';
    voiceSelect.value = '';
    wantedVoice = broken.has('voice') ? '' : hash.get('voice') || '';
    updateSteps();
  }

  function onArrival(next) {
    // EVERY ARRIVAL ENDS SOMEWHERE: the address work between the two
    // funnels had none, and threw here on every arrival alike.
    try {
      const bad = M.addressProblems(next, canon, editions, voices);
      seedControls(next, new Set(bad.map((one) => one.key)));
      if (bad.length) {
        // Fail closed: the address stays as written, no stale chapter under
        // it; the seeded controls hold the nearest valid route.
        renderInvalid(bad);
        return;
      }
      arrival = true;
      render();
    } catch (error) {
      startFailed('The catena index could not be read: ' + (error.message || error));
    }
  }

  /* -------------------------------------------------------------- start */

  // Never a permanent "Loading…" over a failed bootstrap.
  function labelSelects(label) {
    for (const select of [bookSelect, chapterSelect, bibleSelect, voiceSelect]) {
      T.fillSelect(select, [{ value: '', label: label }]);
      select.disabled = true;
    }
  }

  // A TERMINAL STATE IS A TRANSACTION: this left the tally standing and
  // invalidated nothing, so a render in flight repainted over the failure.
  function startFailed(message) {
    T.beginRender();
    const refocus = focusKeeper();
    reference.textContent = 'Unavailable';
    referenceBook.textContent = '';
    T.clear(tally);
    labelSelects('Unavailable');
    T.fail(message);
    refocus();
  }

  async function start() {
    // Narrow viewports fold the controls NOW: folded after the fetches,
    // the page shifted.
    if (window.matchMedia('(max-width: 64rem)').matches) {
      controlsDisclosure.open = false;
    }
    // The static document is true without scripts; from here on,
    // "loading" is the truth instead.
    reference.textContent = 'Loading…';
    labelSelects('Loading…');

    T.setInlineNotice(
      'No data root could be reached, so this page has nothing to show. Serve ' +
        'the pages over HTTP, or try ?data=fixture for the sample corpus.');

    let manifest;
    try {
      [index, manifest, paragraphs] = await Promise.all([
        T.loadJSON('structure/catena/index.json'),
        T.loadBibles(),
        // Optional: without the paragraph layer, the chapter runs on — and
        // OPTIONAL MEANS ITS FAILURE IS NOT THE PAGE'S. Unguarded, a transport
        // fault here took down the whole bootstrap and blamed the catena index.
        cached(paragraphFiles, 'structure/paragraphs/index.json', ABSENT)
          .then(seen, () => 'unreadable')
      ]);
    } catch (error) {
      startFailed('The catena index could not be loaded: ' + (error.message || error));
      return;
    }
    // JSON `null` is a valid document and NOT an index: read raw it threw
    // HERE, past the request catch, leaving "Loading…" standing for ever.
    index = bag(index);
    if (!manifest.ok) {
      startFailed(manifest.message);
      return;
    }
    // ONE READING OF EACH ROOT; everything judging an address consults these.
    editions = M.bibleRoot(manifest.bibles);
    bibles = editions.bibles;
    canon = M.canonRoot(index.canon);
    voices = M.voiceRoot(index);

    // AND AN UNREADABLE ROOT IS NOT A BAD ADDRESS: judged against an empty
    // canon, a null index answered "Gen is not a book of this canon".
    if (!canon.books.length) return startFailed('The catena index could not be read.');
    // An unreadable edition root is not a corpus published in no edition.
    if (!bibles.length) return startFailed('The published editions could not be read.');
    T.fillSelect(bookSelect,
      canon.books.map((book) => ({ value: book.token, label: book.name })));
    T.fillBibleSelect(bibleSelect, bibles);
    bookSelect.disabled = chapterSelect.disabled = bibleSelect.disabled = false;

    bookSelect.addEventListener('change', () => {
      fillChapters(bookSelect.value, 1);
      render();
    });
    for (const one of [chapterSelect, bibleSelect, voiceSelect]) {
      one.addEventListener('change', render);
    }
    prevButton.addEventListener('click', () => step(-1));
    nextButton.addEventListener('click', () => step(1));
    T.onArrowStep(step);
    window.addEventListener('hashchange', () => {
      // This route's own write echoes back first; consumed, never rendered.
      if (window.location.hash === selfWrote) return void (selfWrote = null);
      selfWrote = null;
      if (!showingError && window.location.hash === currentHashText()) return;
      onArrival(T.readHash());
    });

    // The cold load is an arrival like any other — ONE path, so a pasted
    // or restored address cannot resolve two ways.
    onArrival(T.readHash());
  }

  start();
}());
