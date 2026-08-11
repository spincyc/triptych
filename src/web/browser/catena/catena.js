/* ===========================================================================
 * The catena page — a chapter, and every fragment held on it
 * ===========================================================================
 * Book, chapter, translation; the chapter, and beside or beneath it the
 * commentary held on it, oldest first. Above 64rem chapter and chain are
 * two columns — a composition, not a reordering; facts first, prose in the
 * footer, per the maintainer's standing direction.
 *
 * WHAT THIS FILE DOES NOT DO, AND MUST NOT START DOING. It does not decide
 * what belongs to a chapter — that is `catena-model.js`, replayed by
 * `catena check`; one derivation. It does not resolve a numbering: the
 * projection's refusals arrive as data, because guessing where a displaced
 * psalm's boundary moved is what this apparatus exists to prevent. It does
 * not filter on rights or confidence — both guards live in the generator.
 *
 * WHAT A READER PAYS FOR. The book file is a SPINE — no prose; a
 * fragment's text is its own file, fetched when opened, so unfetched text
 * is beyond find-in-page. The page says so, and prints each length so the
 * reader chooses knowingly.
 * ======================================================================== */

'use strict';

(function () {
  const T = window.Triptych;
  const M = window.CatenaModel;

  const INDEX_PATH = 'structure/catena/index.json';
  const PARAGRAPH_INDEX_PATH = 'structure/paragraphs/index.json';

  // ISO 639 codes named for a reader; an unknown code prints as itself.
  const LANGUAGE_NAMES = {
    la: 'Latin', grc: 'Greek', el: 'Greek', en: 'English', de: 'German',
    fr: 'French', he: 'Hebrew', syr: 'Syriac', it: 'Italian', es: 'Spanish'
  };

  function languageName(code) {
    return LANGUAGE_NAMES[String(code || '')] || String(code || '');
  }

  /** "Latin, Greek and English". */
  function joinNames(names) {
    if (names.length <= 1) return names.join('');
    return names.slice(0, -1).join(', ') + ' and ' + names[names.length - 1];
  }

  // The original is named only by itself — "Latin" cannot tell Ambrose
  // writing from Eustathius translating; a translation, by the language
  // it translates INTO.
  function voiceLabel(entry) {
    if (!entry) return '';
    if (entry.voice === M.ORIGINAL) return 'The author’s own language';
    return languageName(entry.language) + ' translation';
  }

  /** The same, inside a sentence. */
  function voicePhrase(entry) {
    if (!entry) return '';
    if (entry.voice === M.ORIGINAL) return 'the author’s own language';
    return languageName(entry.language) + ' translation';
  }

  /** Every held voice as prose, for the empty-selection sentence. */
  function voiceList(file) {
    return joinNames(M.chapterVoices(file).map(voicePhrase));
  }

  // The voice a selection names, held here or not — read back from the
  // key itself.
  function chosen(file, wanted) {
    const held = M.chapterVoices(file).find((one) => one.key === wanted);
    return held || M.parseVoiceKey(wanted);
  }

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
  const previousButton = document.getElementById('prev-button');
  const nextButton = document.getElementById('next-button');
  const controlsDisclosure = document.getElementById('controls-filter');

  let index = null;
  let bibles = [];
  const chapterFiles = new Map();
  // One promise per file, so closing and reopening refetches nothing.
  const fragmentTexts = new Map();
  const paragraphFiles = new Map();
  let paragraphs = null;
  // Always on, not a control: where a chapter divides, that is how it reads.
  const paragraphsWanted = true;
  // Authors switched OFF — exclusions, so they persist across chapters.
  const hiddenAuthors = new Set();
  // A voice a link asked for, held until a control that can hold it
  // exists. THE DEFECT THIS REPLACES: assigning it while the select held
  // one option read back '' and rewrote the reader's URL without their
  // `voice`. It now seeds the first `fillVoices`.
  let wantedVoice = '';
  // True while an invalid-address notice is up; it matches no hash.
  let showingError = false;
  // True when the next render answers an ARRIVING address (cold load, Back,
  // Forward, a typed hash) rather than a reader action on the controls.
  let arrival = false;

  /* --------------------------------------------------------------- data */

  function heldEntry(token) {
    return (index.held || []).find((book) => book.token === token) || null;
  }

  // The spine for one chapter. A chapter with nothing has NO FILE, so
  // absence costs no request; the path is read from the index, never
  // composed. A 404 on a listed chapter is a broken record, not emptiness
  // — it comes back marked.
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
        if (error instanceof T.NotFound) return { unfetched: path };
        throw error;
      }
    );
    chapterFiles.set(path, pending);
    return pending;
  }

  function canonEntry(token) {
    return (index.canon || []).find((book) => book.token === token) || null;
  }

  // Where this edition opens a paragraph. The layer is the EDITION's —
  // a chapter that runs on has no file, so the 404 is the answer.
  function chapterParagraphs(bible, token, chapter) {
    if (!paragraphsWanted || !paragraphs) return Promise.resolve(null);
    const edition = (paragraphs.editions || {})[bible.id];
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

  // One fragment's prose, fetched once and kept — keyed by the path the
  // SPINE gave, never assembled from an id.
  function fragmentText(path) {
    if (!path) return Promise.resolve(null);
    if (fragmentTexts.has(path)) return fragmentTexts.get(path);
    const pending = T.loadJSON(path);
    fragmentTexts.set(path, pending);
    return pending;
  }


  /* ------------------------------------------------- the chapter */

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

    // Prose — a stack of verse-lines is a concordance.
    const breaks = (marks && marks.breaks) || {};
    const body = T.el('div', 'passage');
    body.lang = bible.language || 'en';
    let passage = null;
    let printed = 0;
    let projected = 0;
    let opened = 0;
    for (const number of numbers) {
      const kind = breaks[String(number)];
      if (!passage || kind) {
        passage = T.el('p', 'passage-paragraph');
        opened += 1;
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
    // OPEN. Closed dated from the stacked layout; the columns answer
    // that. Still a `details`.
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
    // The chip counts the PARAGRAPHS on the page, not the recorded
    // breaks: the first opens unmarked, so the break count was off by one.
    if (printed + projected) {
      head.appendChild(
        T.el(
          'span',
          'chapter-count',
          opened + (opened === 1 ? ' paragraph' : ' paragraphs')
        )
      );
    }
    holder.appendChild(head);
    holder.appendChild(body);
    // A printed mark and a projected one are different claims; the
    // note counts BREAKS, in those words.
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

  /* ------------------------------------------------- the chain
   * Rule 6 governs the label: a fragment shown under a chapter it only
   * reaches into still says where it actually runs. */

  function renderFragment(fragment, bookName) {
    const item = T.el('li', 'fragment');
    item.setAttribute('data-state', 'held');

    // `details`, not a scripted toggle: keyboard-reachable, and closed
    // rows read as a chronological index.
    const details = document.createElement('details');
    details.className = 'fragment-body';

    const head = document.createElement('summary');
    head.className = 'fragment-head';
    head.appendChild(T.el('span', 'fragment-author', fragment.author));
    head.appendChild(T.el('span', 'fragment-work', fragment.work));
    if (fragment.date !== null && fragment.date !== undefined) {
      head.appendChild(T.el('span', 'fragment-date', String(fragment.date)));
    }
    // The language, and WHOSE it is; an unestablished voice says only
    // the language.
    if (fragment.language) {
      const name = languageName(fragment.language);
      head.appendChild(
        T.el(
          'span',
          'fragment-language',
          fragment.voice === M.ORIGINAL
            ? name + ' — the author’s own'
            : fragment.voice === M.TRANSLATION
              ? name + ' translation'
              : name
        )
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

    // A licence travels ABOVE the words, so a copied selection carries
    // the condition. Rendered only when the record carries one; nothing is
    // invented for a bare `licensed`.
    const licence = (note) => {
      const block = T.el('p', 'fragment-acknowledgement');
      block.appendChild(T.el('strong', null, 'Licence: '));
      block.appendChild(document.createTextNode(note));
      return block;
    };
    if (fragment.acknowledgement) details.appendChild(licence(fragment.acknowledgement));

    // The prose arrives on first open; a failure is reported against
    // this fragment and nothing else.
    const text = T.el('p', 'fragment-text', 'Loading…');
    text.lang = fragment.language || 'en';
    details.appendChild(text);
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
          if (loaded.acknowledgement && !fragment.acknowledgement) {
            details.insertBefore(licence(loaded.acknowledgement), text);
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

    // Provenance, below the text, rendered whether or not the text loads.
    // Every rights, printing and attribution fact the spine carries is
    // printed; only `container` (a record id) stays unprinted.
    const source = T.el('p', 'fragment-source');
    source.appendChild(document.createTextNode(fragment.locator));
    const fact = (said) => {
      source.appendChild(T.el('span', 'sep'));
      source.appendChild(document.createTextNode(said));
    };
    if (fragment.edition) fact(fragment.edition);
    if (fragment.edition_published) fact(fragment.edition_published);
    if ((fragment.translators || []).length) fact('tr. ' + fragment.translators.join(', '));
    if (fragment.rights) fact(fragment.rights);
    if (fragment.attribution) fact(fragment.attribution);
    // A rights basis only where no acknowledgement already states the terms.
    if (fragment.rights_basis && !fragment.acknowledgement) fact(fragment.rights_basis);
    // The weaker review state gets the word — printing `inspected` and
    // `verified` alike would claim a collation nobody made.
    if (fragment.review && fragment.review !== 'verified') {
      source.appendChild(T.el('span', 'sep'));
      source.appendChild(T.el('span', 'state', fragment.review + ', not collated'));
    }
    // THE HREF IS PINNED by `test_browser_url_contract.py`.
    if (fragment.id) {
      source.appendChild(T.el('span', 'sep'));
      const whole = T.el(
        'a',
        'fragment-whole',
        'Open this passage in the Source Library'
      );
      whole.href = '../sources/#passage=' + encodeURIComponent(fragment.id);
      source.appendChild(whole);
    }
    details.appendChild(source);
    item.appendChild(details);
    return item;
  }

  // Why the works standing here miss the asked-for language; unsaid, the
  // page reads as a load failure. The findings are the generator's; this
  // prints them, counting the two apart — a partly public-domain English
  // is SOME, and filing it under "none" was false.
  function renderAbsences(container, file, wanted) {
    const asked = M.parseVoiceKey(wanted);
    if (!asked || asked.voice !== M.TRANSLATION || !asked.language) return;
    const recorded = (index && index.absences) || {};
    const sources = (file && file.sources) || {};
    const named = new Set();
    const rows = [];
    for (const key in sources) {
      if (!Object.hasOwn(sources, key)) continue;
      const source = sources[key];
      const workId = source.work_id || '';
      if (!workId || named.has(workId)) continue;
      const found = (recorded[workId] || []).find(
        (one) => one.language === asked.language
      );
      if (!found) continue;
      named.add(workId);
      rows.push({ author: source.author, work: source.work, absence: found });
    }
    if (!rows.length) return;

    const note = T.el('details', 'absence-note');
    note.setAttribute('data-state', 'absence');
    const untaken = rows.filter((row) => row.absence.partial).length;
    const closed = rows.length - untaken;
    const language = languageName(asked.language);
    const parts = [];
    if (closed) {
      parts.push(
        (closed === 1 ? 'One work standing here has' : closed + ' works standing here have') +
          ' no ' + language + ' this project may publish'
      );
    }
    if (untaken) {
      parts.push(
        (closed ? String(untaken) : untaken === 1 ? 'one work standing here' : untaken + ' works standing here') +
          (untaken === 1 ? ' has' : ' have') +
          ' only a partly public domain ' + language + ', not yet taken'
      );
    }
    const head = document.createElement('summary');
    head.textContent = parts.join('; ');
    note.appendChild(head);
    const list = T.el('ul', 'absence-list');
    for (const row of rows) {
      const item = T.el('li', 'absence');
      item.appendChild(T.el('span', 'absence-author', row.author));
      item.appendChild(T.el('span', 'absence-work', row.work));
      item.appendChild(T.el('p', 'absence-reason', row.absence.reason));
      // A partial not yet taken is an offer, not an excuse, and reads as
      // one only apart from the reason.
      if (row.absence.partial) {
        item.appendChild(
          T.el('p', 'absence-partial', 'Partly public domain — ' + row.absence.partial)
        );
      }
      list.appendChild(item);
    }
    note.appendChild(list);
    container.appendChild(note);
  }

  function renderChain(container, file, book) {
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
      // Rule 1: no fragments shows no fragments, said plainly.
      container.appendChild(
        T.el(
          'p',
          'aside-note',
          all.length
            ? 'No commentary on this chapter is held in ' +
                voicePhrase(chosen(file, wanted)) +
                '. ' +
                all.length +
                (all.length === 1 ? ' fragment is' : ' fragments are') +
                ' held here, in ' +
                voiceList(file) +
                '; choose “Everything held” to see ' +
                (all.length === 1 ? 'it' : 'them') +
                '.'
            : 'No commentary on this chapter is held yet.'
        )
      );
      renderAbsences(container, file, wanted);
      return 0;
    }

    // A father held only in his own Latin must not vanish under an
    // English selection: the unshown voices are named.
    if (wanted) {
      const others = M.chapterVoices(file).filter((one) => one.key !== wanted);
      if (others.length) {
        container.appendChild(
          T.el(
            'p',
            'aside-note',
            'Showing ' +
              voicePhrase(chosen(file, wanted)) +
              ' only. This chapter is also held in ' +
              joinNames(others.map(voicePhrase)) +
              '.'
          )
        );
      }
      renderAbsences(container, file, wanted);
    }

    // Grouped WITHOUT reordering: only a CONTIGUOUS author+date run
    // shares a heading. By-author grouping filed Augustine's 417 under a
    // 401 heading ahead of Severian's 401; the three stand as three.
    const groups = [];
    for (const fragment of held) {
      const date = fragment.date === undefined ? null : fragment.date;
      const last = groups[groups.length - 1];
      if (last && last.author === fragment.author && last.date === date) {
        last.fragments.push(fragment);
      } else {
        groups.push({ author: fragment.author, date: date, fragments: [fragment] });
      }
    }

    const list = T.el('ul', 'chain');
    const rendered = [];
    // The first group opens: all closed reads as nothing, all open as a
    // wall. No request either way.
    let first = true;
    for (const group of groups) {
      const item = T.el('li', 'author');
      const node = document.createElement('details');
      node.className = 'author-body';
      if (first) {
        node.open = true;
        first = false;
      }

      const summary = document.createElement('summary');
      summary.className = 'author-head';
      summary.appendChild(T.el('span', 'author-name', group.author));
      if (group.date !== null) {
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

    // One toggle per AUTHOR, though he may stand at several dates.
    const authors = [];
    for (const row of rendered) {
      if (!authors.includes(row.author)) authors.push(row.author);
    }

    let filterHolder = null;

    // DESELECTED authors; hiding rows, not rebuilding, keeps open nodes
    // open.
    function applyFilter() {
      let shown = 0;
      for (const row of rendered) {
        const on = !hiddenAuthors.has(row.author);
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

    // The filter exists when there is anyone to choose between AND when a
    // carried-over exclusion touches this chapter: a sole author switched
    // off elsewhere must still get his switch here.
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
        label.appendChild(document.createTextNode(name));
        filter.appendChild(label);
      }
      // Folded away — twenty checkboxes were the first screen.
      filterHolder = T.el('details', 'author-filter-disclosure');
      filterHolder.appendChild(T.el('summary', null, 'Filter authors'));
      filterHolder.appendChild(filter);
      if (hiddenHere) filterHolder.open = true;
      container.appendChild(filterHolder);
    }

    container.appendChild(list);
    applyFilter();
    return held.length;
  }

  /* ----------------------------------- the things that are not fragments */

  // The acquisition list, printed as recorded and no further: the record
  // is NOT reconciled against the held commentary (the two overlap), so
  // this copy claims neither absence above nor non-possession.
  // Reconciliation belongs to the record's generator.
  function renderLeads(container, leads) {
    if (!leads.length) return;
    const section = T.el('section', 'aside');
    section.setAttribute('data-state', 'lead');
    section.appendChild(
      T.el('h2', 'section-heading', 'Believed to comment here — the acquisition list')
    );
    section.appendChild(
      T.el(
        'p',
        'aside-note',
        leads.length +
          ' works the acquisition record lists for this chapter, printed as ' +
          'recorded. The list is kept separately from the commentary above ' +
          'and is not checked against it here.'
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
      node.setAttribute('data-state', 'blocked');
      const who = T.el('b', null, entry.author + ' — ' + entry.work);
      node.appendChild(who);
      node.appendChild(T.el('span', 'why', entry.reason));
      section.appendChild(node);
    }
    container.appendChild(section);
  }

  // Rule 4 — where the projection refuses, the page refuses, and does not
  // fall back to the same verse number: the wrong answer dressed right.
  function renderRefusal(container, file, bible, book, chapter) {
    const here = ((file && file.refusals) || {})[bible.id] || [];
    if (!here.length) return;
    const note = String(here[0].note || '').replace(/\s+$/, '');
    const sentence = note ? note.charAt(0).toUpperCase() + note.slice(1) + '.' : '';
    const node = T.el('p', 'refusal');
    node.setAttribute('data-state', 'refusal');
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

  /* ------------------------------------ the cited state, failing closed
   * A value this page cannot honour is never traded for a default: the
   * URL keeps the reader's text, the page names what it could not read,
   * and recovery is a link and the live controls. */

  function hashProblems(hash) {
    const bad = [];
    const token = hash.get('book') || '';
    const entry = token ? canonEntry(token) : null;
    if (token && !entry) {
      bad.push({ key: 'book', value: token, note: 'is not a book of this canon' });
    }
    const chapter = hash.get('chapter') || '';
    if (chapter) {
      const numeric = /^[0-9]+$/.test(chapter) ? Number(chapter) : NaN;
      // Ranged against the book the page would actually resolve: the cited
      // book when it is sound, else the current or default one.
      const anchor = entry || canonEntry(bookSelect.value) || canonEntry('Gen');
      const within = anchor
        ? numeric >= 1 && numeric <= anchor.chapters
        : numeric >= 1;
      if (!within) {
        bad.push({
          key: 'chapter',
          value: chapter,
          note: anchor
            ? 'is not a chapter of ' + anchor.name + ', which has ' + anchor.chapters
            : 'is not a chapter number'
        });
      }
    }
    const bible = hash.get('bible') || '';
    if (bible && !bibles.some((one) => one.id === bible)) {
      bad.push({ key: 'bible', value: bible, note: 'is not a published edition' });
    }
    const voice = hash.get('voice') || '';
    if (voice) {
      // The WHOLE key must be sound: `original:x` parses to an original
      // voice but is not the literal key, and would self-contradict.
      const parsed = M.parseVoiceKey(voice);
      const sound =
        parsed &&
        (parsed.key === M.ORIGINAL ||
          (parsed.voice === M.TRANSLATION && parsed.language));
      if (!sound) {
        bad.push({
          key: 'voice',
          value: voice,
          note: 'is not a voice — “original”, or “translation:” plus a language'
        });
      }
    }
    return bad;
  }

  // The nearest valid address: sound values kept, broken ones defaulted —
  // offered as a link, never imposed.
  function recoveryHash(hash, bad) {
    const broken = new Set(bad.map((one) => one.key));
    const token =
      !broken.has('book') && hash.get('book') ? hash.get('book') : 'Gen';
    const entry = canonEntry(token);
    let chapter =
      !broken.has('chapter') && hash.get('chapter') ? hash.get('chapter') : '1';
    if (entry && Number(chapter) > entry.chapters) chapter = '1';
    const bible =
      !broken.has('bible') && hash.get('bible')
        ? hash.get('bible')
        : (bibles[0] || {}).id || '';
    const voice = !broken.has('voice') ? hash.get('voice') || '' : '';
    const parts = [];
    for (const pair of [['book', token], ['chapter', chapter], ['bible', bible], ['voice', voice]]) {
      if (pair[1]) parts.push(pair[0] + '=' + encodeURIComponent(pair[1]));
    }
    return '#' + parts.join('&');
  }

  function errorSection(title) {
    const section = T.el('section', 'catena-error');
    section.setAttribute('data-state', 'error');
    section.appendChild(T.el('h2', 'section-heading', title));
    return section;
  }

  function renderInvalid(bad, recovery) {
    T.beginRender();
    showingError = true;
    reference.textContent = 'Address not recognised';
    referenceBook.textContent = '';
    T.clear(tally);
    T.clear(reading);
    const section = errorSection('This address names what the page does not have');
    for (const one of bad) {
      const row = T.el('p', 'error-detail');
      row.appendChild(T.el('code', null, one.key + '=' + one.value));
      row.appendChild(document.createTextNode(' ' + one.note + '.'));
      section.appendChild(row);
    }
    const recover = T.el('p', 'error-recovery');
    recover.appendChild(document.createTextNode('The address is left as written. '));
    const link = T.el('a', null, 'Open the nearest valid page');
    link.href = recovery;
    recover.appendChild(link);
    recover.appendChild(document.createTextNode(', or change a control above.'));
    section.appendChild(recover);
    reading.appendChild(section);
    reading.setAttribute('aria-busy', 'false');
    T.statusLine('The address could not be read; its invalid values are shown, unchanged.');
  }

  /* ----------------------------------------------------------- assembly */

  async function render() {
    const wasArrival = arrival;
    arrival = false;
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

    // An expected spine that would not come is an error, not an absence.
    const unfetched = file && file.unfetched ? file.unfetched : '';
    if (unfetched) file = null;

    fillVoices(file);
    const leads = (file && file.leads) || [];
    const total = M.chapterFragments(file).length;
    T.clear(reading);
    let count = 0;
    if (unfetched) {
      renderChapter(reading, bible, book, chapter, chapterResult, marks);
      const section = errorSection('This chapter’s commentary record did not load');
      section.appendChild(
        T.el(
          'p',
          'error-detail',
          'The index records commentary on ' + book.name + ' ' + chapter +
            ', but its record (' + unfetched + ') could not be fetched — a ' +
            'data or connection fault, not an empty ' +
            'chapter. Reloading may recover it.'
        )
      );
      reading.appendChild(section);
    } else {
      renderRefusal(reading, file, bible, book, chapter);
      renderChapter(reading, bible, book, chapter, chapterResult, marks);
      // One wrapper for all that is not the chapter, so the wide grid
      // seats the two side by side without counting children.
      const column = T.el('div', 'chain-column');
      count = renderChain(column, file, book);
      renderLeads(column, leads);
      renderBlocked(column, file);
      reading.appendChild(column);
    }
    reading.setAttribute('aria-busy', 'false');

    // The tally states the corpus, never the filter: an empty selection
    // must not read as an empty chapter.
    T.clear(tally);
    const wanted = voiceSelect.value;
    if (unfetched) {
      tally.appendChild(document.createTextNode('The commentary record did not load'));
    } else {
      tally.appendChild(T.el('b', null, total === 0 ? 'Nothing' : String(total)));
      let text =
        total === 0 ? ' held here' : total === 1 ? ' fragment held' : ' fragments held';
      if (total && wanted && count < total) {
        text += ' · ' + (count ? count + ' in ' : 'none in ') + voicePhrase(chosen(file, wanted));
      }
      if (leads.length) {
        text += ' · ' + leads.length + (leads.length === 1 ? ' work' : ' works') +
          ' on the acquisition list';
      }
      tally.appendChild(document.createTextNode(text));
    }

    T.statusLine(
      book.name + ' ' + chapter + ', ' + bible.label + ', ' +
        (unfetched
          ? 'commentary record unavailable.'
          : total + ' fragments held' +
            (wanted && count < total ? ', ' + count + ' shown' : '') + '.')
    );
    showingError = false;
    // History. A reader ACTION pushes an entry; an ARRIVAL never may. A
    // hash already parsing to these four values stays byte for byte as
    // written — rewriting `%3A`, a leading zero or an extra key would push
    // an entry Back can only bounce off — and a partial arrival is
    // completed with replaceState, not with a pushing write.
    const now = T.readHash();
    const identical =
      now.get('book') === token &&
      Number(now.get('chapter')) === chapter &&
      now.get('bible') === bible.id &&
      (now.get('voice') || '') === voiceSelect.value;
    if (!identical) {
      if (wasArrival && window.history && window.history.replaceState) {
        window.history.replaceState(null, '', currentHashText());
      } else {
        T.writeHash([
          ['book', token],
          ['chapter', String(chapter)],
          ['bible', bible.id],
          // `voice`, not `language`: an old `language=` link deliberately
          // opens on everything held rather than on a guess.
          ['voice', voiceSelect.value],
        ]);
      }
    }
    updateSteps();
  }

  // The voice control, COUNTED from what this chapter holds, never
  // assumed. An unheld selection is KEPT; the chain says so.
  function fillVoices(file) {
    const held = M.chapterVoices(file);
    // The reader's own selection first; a deep-linked voice only before
    // any selection.
    const wanted = voiceSelect.value || wantedVoice;
    wantedVoice = '';
    const items = [{ value: '', label: 'Everything held' }];
    for (const entry of held) items.push({ value: entry.key, label: voiceLabel(entry) });
    if (wanted && !held.some((one) => one.key === wanted)) {
      items.push({
        value: wanted,
        label: voiceLabel(chosen(file, wanted)) + ' — none here'
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

  /* ------------------------------ history, route-owned and deterministic
   * Not `T.onHashChange`: its remembered-write string goes stale after
   * Back and swallows Forward. This page compares the arriving hash with
   * what its CURRENT state would write — same keys, order and encoding as
   * the one `T.writeHash` call — so its own echoes are skipped and every
   * reader move renders. It yields while an error notice is up. */

  function currentHashText() {
    const parts = [];
    for (const pair of [
      ['book', bookSelect.value],
      ['chapter', chapterSelect.value],
      ['bible', bibleSelect.value],
      ['voice', voiceSelect.value]
    ]) {
      if (pair[1]) parts.push(pair[0] + '=' + encodeURIComponent(pair[1]));
    }
    return parts.length ? '#' + parts.join('&') : '';
  }

  function onArrival(next) {
    const bad = hashProblems(next);
    if (bad.length) {
      // Fail closed: the address stays as written and no stale chapter
      // stands under it.
      renderInvalid(bad, recoveryHash(next, bad));
      return;
    }
    if (next.get('book')) bookSelect.value = next.get('book');
    fillChapters(bookSelect.value, next.get('chapter') || 1);
    if (next.get('bible')) bibleSelect.value = next.get('bible');
    // The voice deferral again; cleared first, so a Back to a hash
    // without `voice` lands on everything held.
    voiceSelect.value = '';
    wantedVoice = next.get('voice') || '';
    arrival = true;
    render();
  }

  /* -------------------------------------------------------------- start */

  async function start() {
    // Narrow viewports fold the controls NOW, synchronously — after
    // three fetches, the fold shifted the page. Nothing re-closes them.
    if (
      controlsDisclosure &&
      window.matchMedia &&
      window.matchMedia('(max-width: 64rem)').matches
    ) {
      controlsDisclosure.open = false;
    }
    // The static document tells the truth without scripts; once this
    // script runs, "loading" becomes the truth instead.
    reference.textContent = 'Loading…';
    for (const select of [bookSelect, chapterSelect, bibleSelect, voiceSelect]) {
      T.clear(select);
      const option = T.el('option', null, 'Loading…');
      option.value = '';
      select.appendChild(option);
    }

    T.setInlineNotice(
      'No data root could be reached, so this page has nothing to show. Serve ' +
        'the pages over HTTP, or try ?data=fixture for the sample corpus.'
    );

    let manifest;
    try {
      [index, manifest, paragraphs] = await Promise.all([
        T.loadJSON(INDEX_PATH),
        T.loadBibles(),
        // Optional in the strongest sense: a data root without the
        // paragraph layer serves the page and the chapter runs on.
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
    const bad = hashProblems(hash);
    const broken = new Set(bad.map((one) => one.key));
    T.fillSelect(
      bookSelect,
      (index.canon || []).map((book) => ({ value: book.token, label: book.name }))
    );
    // The controls take every SOUND cited value and the default for the
    // rest; a broken value never becomes a selection.
    bookSelect.value =
      !broken.has('book') && hash.get('book') ? hash.get('book') : 'Gen';
    if (!bookSelect.value) bookSelect.value = (index.canon[0] || {}).token;
    fillChapters(
      bookSelect.value,
      broken.has('chapter') ? 1 : hash.get('chapter') || 1
    );
    T.fillBibleSelect(bibleSelect, bibles);
    if (
      !broken.has('bible') &&
      hash.get('bible') &&
      bibles.some((one) => one.id === hash.get('bible'))
    ) {
      bibleSelect.value = hash.get('bible');
    }
    // Not assigned to the control here: see `wantedVoice` above.
    wantedVoice = broken.has('voice') ? '' : hash.get('voice') || '';

    bookSelect.disabled = false;
    chapterSelect.disabled = false;
    bibleSelect.disabled = false;

    bookSelect.addEventListener('change', () => {
      fillChapters(bookSelect.value, 1);
      render();
    });
    chapterSelect.addEventListener('change', render);
    bibleSelect.addEventListener('change', render);
    voiceSelect.addEventListener('change', render);
    previousButton.addEventListener('click', () => step(-1));
    nextButton.addEventListener('click', () => step(1));
    T.onArrowStep(step);
    window.addEventListener('hashchange', () => {
      if (!showingError && window.location.hash === currentHashText()) return;
      onArrival(T.readHash());
    });

    if (bad.length) {
      // Cold load against a broken address: the notice, not a default page,
      // and a seeded voice control — never a control left "loading".
      fillVoices(null);
      renderInvalid(bad, recoveryHash(hash, bad));
      return;
    }
    arrival = true;
    await render();
  }

  start();
}());
