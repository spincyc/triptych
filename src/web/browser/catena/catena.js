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
  // A typed value is a fact only as nonempty text; anything else is
  // withheld, never coerced into words or a legal status.
  const sound = (value) => typeof value === 'string' && value.trim();

  // ISO 639 codes the shared table lacks; the shared fallback names the rest.
  function languageName(code) {
    return { grc: 'Greek', el: 'Greek', he: 'Hebrew', syr: 'Syriac' }[code] || T.languageName(code);
  }

  /** "Latin, Greek and English". */
  function joinNames(names) {
    const last = names.pop();
    return names.length ? names.join(', ') + ' and ' + last : last || '';
  }

  // The original is named only by itself; a translation, by language.
  function voicePhrase(entry) {
    if (!entry) return '';
    if (entry.voice === M.ORIGINAL) return 'the author’s own language';
    return languageName(entry.language) + ' translation';
  }

  /** The same, opening a label. */
  function voiceLabel(entry) {
    const phrase = voicePhrase(entry);
    return phrase.charAt(0).toUpperCase() + phrase.slice(1);
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
  const prevButton = document.getElementById('prev-button');
  const nextButton = document.getElementById('next-button');
  const controlsDisclosure = document.getElementById('controls-filter');

  let index = null;
  let bibles = [];
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

  /* --------------------------------------------------------------- data */

  function entryOf(list, token) {
    return (list || []).find((book) => book.token === token) || null;
  }

  function canonEntry(token) { return entryOf(index.canon, token); }

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
  // A 404 on a LISTED chapter is a broken record, not emptiness — marked.
  function chapterFile(token, chapter) {
    const held = entryOf(index.held, token);
    if (!held || !(held.present || []).includes(Number(chapter))) {
      return Promise.resolve(null);
    }
    const path = held.path +
      String(chapter).padStart(Number(index.chapter_digits) || 1, '0') + '.json';
    return cached(chapterFiles, path, { unfetched: path });
  }

  // Where this edition opens a paragraph. The layer is the EDITION's —
  // a chapter that runs on has no file, so the 404 is the answer.
  function chapterParagraphs(bible, token, chapter) {
    if (!paragraphs) return Promise.resolve(null);
    const edition = (paragraphs.editions || {})[bible.id];
    const book = canonEntry(token);
    if (!edition || !book || !book.path) return Promise.resolve(null);
    const path = edition.path + book.path + '/' +
      String(chapter).padStart(Number(paragraphs.chapter_digits) || 1, '0') + '.json';
    return cached(paragraphFiles, path, null);
  }

  // One fragment's prose — keyed by the path the SPINE gave, never
  // assembled from an id. Even its 404 is evicted: retry is real.
  function fragmentText(path) {
    if (!path) return Promise.resolve(null);
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
    const numbers = Object.keys(result.verses)
      .map(Number)
      .filter(Number.isFinite)
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
        if (kind === 'printed') printed += 1;
        if (kind === 'projected') { passage.classList.add('projected'); projected += 1; }
        body.appendChild(passage);
      }
      const verse = T.el('span', 'verse');
      verse.appendChild(T.el('sup', 'verse-num', String(number)));
      verse.appendChild(textNode(result.verses[String(number)] + ' '));
      passage.appendChild(verse);
    }
    // OPEN — closed dated from the stacked layout; still a `details`.
    const holder = T.el('details', 'chapter-body');
    holder.open = true;
    const head = T.el('summary', 'chapter-head');
    head.appendChild(T.el('span', 'chapter-name', book.name + ' ' + chapter));
    head.appendChild(T.el('span', 'chapter-count',
      numbers.length + (numbers.length === 1 ? ' verse' : ' verses')));
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
        'No paragraph division is held for this chapter in this edition, so it ' +
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
    head.appendChild(T.el('span', 'fragment-author', sound(fragment.author) || ''));
    head.appendChild(T.el('span', 'fragment-work', sound(fragment.work) || ''));
    if (sound(fragment.date) || Number.isFinite(fragment.date)) {
      head.appendChild(T.el('span', 'fragment-date', String(fragment.date)));
    }
    // The language, and WHOSE it is; an unestablished voice says only it.
    if (sound(fragment.language)) {
      const name = languageName(fragment.language);
      head.appendChild(T.el('span', 'fragment-language',
        fragment.voice === M.ORIGINAL
          ? name + ' — the author’s own'
          : fragment.voice === M.TRANSLATION ? name + ' translation' : name));
    }
    if (Number(fragment.text_words) > 0) {
      head.appendChild(T.el('span', 'fragment-length',
        Number(fragment.text_words).toLocaleString() + ' words'));
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
    text.lang = fragment.language || 'en';
    details.appendChild(text);
    const apparatus = T.el('div', 'fragment-apparatus');
    details.appendChild(apparatus);

    // ONE point-of-use acknowledgement channel: two VALID supplies render ONE
    // block, and a broken note — said to be broken once — cannot claim the
    // channel and erase a valid note the other supply carries.
    let acknowledged = 0;
    const acknowledge = (note) => {
      if (acknowledged > 1 || note == null || note === '') return;
      if (!sound(note) && acknowledged) return;
      acknowledged = sound(note) ? 2 : 1;
      details.insertBefore(
        sound(note)
          ? licence(note)
          : T.el('p', 'fragment-acknowledgement',
              'The recorded acknowledgement is malformed and not shown.'),
        text);
    };
    acknowledge(fragment.acknowledgement);

    let asked = false;
    details.addEventListener('toggle', () => {
      if (!details.open || asked) return;
      asked = true;
      fragmentText(fragment.text_path).then(
        (loaded) => {
          // A completion for a rebuilt page mutates nothing here.
          if (!reading.contains(details)) return;
          if (!loaded) {
            text.className = 'fragment-text missing';
            text.textContent =
              'This fragment carries no text file, so nothing of it can be shown.';
            return;
          }
          acknowledge(loaded.acknowledgement);
          text.className = 'fragment-text';
          // The payload's body fields are typed too: broken renders nothing.
          text.textContent = sound(loaded.text) ? loaded.text : '';
          if (sound(loaded.basis)) {
            apparatus.appendChild(T.el('p', 'fragment-basis', 'Extent — ' + loaded.basis));
          }
          if (sound(loaded.date_basis)) {
            apparatus.appendChild(T.el('p', 'fragment-basis', 'Date — ' + loaded.date_basis));
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
    source.appendChild(textNode(sound(fragment.locator) || ''));
    const fact = (said) => {
      if (!sound(said)) return;
      source.appendChild(T.el('span', 'sep'));
      source.appendChild(textNode(said));
    };
    fact(fragment.edition);
    fact(fragment.edition_published);
    const hands = [].concat(fragment.translators).filter(sound).join(', ');
    if (hands) fact('tr. ' + hands);
    fact(fragment.rights);
    fact(fragment.attribution);
    // EVERY supplied fact renders: an acknowledgement does not suppress a
    // recorded rights basis — that precedence hid supplied terms.
    fact(fragment.rights_basis);
    // The weaker review state gets the word — printing `inspected` and
    // `verified` alike would claim a collation nobody made.
    if (sound(fragment.review) && fragment.review !== 'verified') {
      source.appendChild(T.el('span', 'sep'));
      source.appendChild(T.el('span', 'state', fragment.review + ', not collated'));
    }
    // THE HREF IS PINNED by `test_browser_url_contract.py`.
    if (sound(fragment.id)) {
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
    if (!asked || asked.voice !== M.TRANSLATION || !asked.language) return;
    const recorded = (index && index.absences) || {};
    const sources = (file && file.sources) || {};
    const named = new Set();
    const rows = [];
    for (const key in sources) {
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
    // The absence contract is not deferrable: the findings stand OPEN, and
    // the disclosure only lets a reader fold them away.
    note.open = true;
    note.setAttribute('data-state', 'absence');
    const untaken = rows.filter((row) => row.absence.partial).length;
    const closed = rows.length - untaken;
    const language = languageName(asked.language);
    const parts = [];
    if (closed) {
      parts.push(
        (closed === 1 ? 'One work standing here has' : closed + ' works standing here have') +
          ' no ' + language + ' this project may publish');
    }
    if (untaken) {
      parts.push(
        (closed ? String(untaken) : untaken === 1 ? 'one work standing here' : untaken + ' works standing here') +
          (untaken === 1 ? ' has' : ' have') +
          ' only a partly public domain ' + language + ', not yet taken');
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
      // A partial not yet taken is an offer, not an excuse.
      if (row.absence.partial) {
        item.appendChild(
          T.el('p', 'absence-partial', 'Partly public domain — ' + row.absence.partial));
      }
      list.appendChild(item);
    }
    note.appendChild(list);
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
      // Rule 1: no fragments shows no fragments, said plainly — but a
      // held row that cannot be rendered is NOT absence; beside one, an
      // absence claim covers the RENDERABLE rows alone.
      container.appendChild(
        T.el('p', 'aside-note',
          all.length
            ? 'No ' + (blockedHeld ? 'renderable ' : '') +
                'commentary on this chapter is held in ' +
                voicePhrase(M.parseVoiceKey(wanted)) + '. ' + all.length +
                (all.length === 1 ? ' fragment is' : ' fragments are') +
                ' held here, in ' +
                joinNames(M.chapterVoices(file).map(voicePhrase)) +
                '; choose “Everything held” to see ' +
                (all.length === 1 ? 'it' : 'them') + '.'
            : blockedHeld
              ? 'Nothing held on this chapter is renderable yet; what is ' +
                'held, and why it cannot be shown, stands below.'
              : 'No commentary on this chapter is held yet.'));
      renderAbsences(container, file, wanted);
      return 0;
    }

    // A father held only in his own Latin must not vanish under an
    // English selection: the unshown voices are named.
    if (wanted) {
      const others = M.chapterVoices(file).filter((one) => one.key !== wanted);
      if (others.length) {
        container.appendChild(
          T.el('p', 'aside-note',
            'Showing ' + voicePhrase(M.parseVoiceKey(wanted)) +
              ' only. This chapter is also held in ' +
              joinNames(others.map(voicePhrase)) + '.'));
      }
      renderAbsences(container, file, wanted);
    }

    // Grouped WITHOUT reordering: only a CONTIGUOUS author+date run shares
    // a heading — by-author grouping misfiled Augustine's 417 before 401.
    const groups = [];
    for (const fragment of held) {
      const author = sound(fragment.author) || '';
      const date = sound(fragment.date) || Number.isFinite(fragment.date) ? fragment.date : null;
      const last = groups[groups.length - 1];
      if (last && last.author === author && last.date === date) {
        last.fragments.push(fragment);
      } else {
        groups.push({ author: author, date: date, fragments: [fragment] });
      }
    }

    const list = T.el('ul', 'chain');
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
      list.appendChild(item);
      rendered.push({ author: group.author, item, count: group.fragments.length });
    }

    // One toggle per AUTHOR, though he may stand at several dates.
    const authors = [...new Set(rendered.map((row) => row.author))];

    let filterHolder = null;

    // DESELECTED authors; hiding, not rebuilding, keeps nodes open.
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

    container.appendChild(list);
    applyFilter();
    return held.length;
  }

  /* ----------------------------------- the things that are not fragments */

  // The acquisition record's rows are UNRECONCILED LEAD ENTRIES: the record
  // omits its confidence and overlaps held commentary, so a row asserts no
  // distinct work, no possession, nothing renderable.
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
    const list = T.el('ul', 'lead-list');
    // Typed fields only: the count is the record's, the words must be.
    for (const lead of leads) {
      const item = T.el('li', 'lead');
      if (sound(lead.author)) item.appendChild(textNode(lead.author + ' — '));
      item.appendChild(T.el('span', 'lead-work', sound(lead.title) ? lead.title : ''));
      if (sound(lead.date) || Number.isFinite(lead.date) && lead.date) item.appendChild(textNode(' (' + lead.date + ')'));
      list.appendChild(item);
    }
    section.appendChild(list);
    container.appendChild(section);
  }

  function renderBlocked(container, blocked) {
    if (!blocked.length) return;
    const section = T.el('section', 'aside');
    section.appendChild(T.el('h2', 'section-heading', 'Held, and not renderable yet'));
    for (const entry of blocked) {
      const node = T.el('div', 'blocked');
      node.setAttribute('data-state', 'blocked');
      if (sound(entry.author) && sound(entry.work)) node.appendChild(T.el('b', null, entry.author + ' — ' + entry.work));
      if (sound(entry.reason)) node.appendChild(T.el('span', 'why', entry.reason));
      section.appendChild(node);
    }
    container.appendChild(section);
  }

  // Rule 4 — where the projection refuses, the page refuses; no
  // same-number fallback dressed right.
  function renderRefusal(container, file, bible, book, chapter) {
    const here = ((file && file.refusals) || {})[bible.id] || [];
    if (!here.length) return;
    const note = sound(here[0].note) || '';
    const sentence = note ? note.charAt(0).toUpperCase() + note.slice(1) + '.' : '';
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

  function hashProblems(hash) {
    const bad = [];
    const flag = (key, value, note) => bad.push({ key, value, note });
    // Multiplicity first: a recognized key cited twice is refused even when
    // the citations agree; a stranger's key is not judged, and no write keeps
    // one. (An undecodable percent-value stays literal, and fails.)
    for (const key of ['book', 'chapter', 'bible', 'voice']) {
      const all = hash.getAll(key);
      if (all.length > 1) flag(key, all.join(', '), 'is cited more than once');
    }
    const token = hash.get('book') || '';
    const entry = token ? canonEntry(token) : null;
    if (token && !entry) flag('book', token, 'is not a book of this canon');
    const chapter = hash.get('chapter') || '';
    if (chapter) {
      const numeric = /^[0-9]+$/.test(chapter) ? Number(chapter) : NaN;
      // Ranged against the book the ADDRESS resolves to — never a
      // leftover control — so every arrival judges alike.
      const anchor = entry || canonEntry('Gen');
      if (!(anchor ? numeric >= 1 && numeric <= anchor.chapters : numeric >= 1)) {
        flag('chapter', chapter, anchor
          ? 'is not a chapter of ' + anchor.name + ', which has ' + anchor.chapters
          : 'is not a chapter number');
      }
    }
    const bible = hash.get('bible') || '';
    if (bible && !bibles.some((one) => one.id === bible)) {
      flag('bible', bible, 'is not a published edition');
    }
    const voice = hash.get('voice') || '';
    if (voice) {
      // The WHOLE key, as a closed grammar: `original` alone, or
      // `translation:` plus one lowercase code — no second colon, no
      // whitespace, no suffix. `original:x` would self-contradict.
      const parsed = M.parseVoiceKey(voice);
      if (voice !== M.ORIGINAL &&
          !(parsed && parsed.voice === M.TRANSLATION &&
            /^[a-z]{2,3}$/.test(parsed.language))) {
        flag('voice', voice, 'is not a voice — “original”, or “translation:” plus a language');
      } else if (parsed.language &&
                 !(index.held || []).some((one) => (one.languages || []).includes(parsed.language))) {
        flag('voice', voice, 'is not a voice this corpus holds');
      }
    }
    return bad;
  }

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
    reference.textContent = 'Address not recognised';
    referenceBook.textContent = '';
    T.clear(tally);
    T.clear(reading);
    const section = errorSection('This address names what the page does not have');
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
    T.statusLine('The address could not be read; its invalid values are shown, unchanged.');
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
    if (!book || !bible || !Number.isFinite(chapter)) return;

    const renderToken = T.beginRender();
    reading.setAttribute('aria-busy', 'true');

    reference.textContent = book.name + ' ' + chapter;
    referenceBook.textContent =
      book.testament === 'old' ? 'Old Testament' : 'New Testament';

    let file, chapterResult, marks;
    try {
      [file, chapterResult, marks] = await Promise.all([
        chapterFile(token, chapter),
        T.loadChapter(bible.id, token, chapter),
        chapterParagraphs(bible, token, chapter)
      ]);
    } catch (error) {
      // A STALE failure proves nothing: only the render still owning the
      // route may show one — completing the address (URL, controls and
      // error agree), claiming no voice absence, keeping the reader's focus.
      if (!T.isCurrentRender(renderToken)) return;
      const refocus = focusKeeper();
      fillVoices(null, true);
      T.clear(tally);
      T.fail('This chapter could not be loaded: ' + (error.message || error));
      refocus();
      writeRoute(wasArrival);
      return;
    }
    if (!T.isCurrentRender(renderToken)) return;

    // An expected spine that would not come is an error, not an absence.
    const unfetched = (file && file.unfetched) || '';
    if (unfetched) file = null;

    // ONE typed truth beside the chapter: every tally, empty, blocked
    // and voice claim derives from these counts — held-but-unrenderable
    // is HELD, never "nothing".
    const blocked = (file && file.blocked) || [];
    const leads = (file && file.leads) || [];
    const total = M.chapterFragments(file).length;
    fillVoices(file, unfetched || blocked.length);
    const refocus = focusKeeper();
    T.clear(reading);
    let count = 0;
    renderRefusal(reading, file, bible, book, chapter);
    renderChapter(reading, bible, book, chapter, chapterResult, marks);
    if (unfetched) {
      const section = errorSection('This chapter’s commentary record did not load');
      section.appendChild(T.el('p', 'error-detail',
        'The index records commentary on ' + book.name + ' ' + chapter +
          ', but its record (' + unfetched + ') could not be fetched — a ' +
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

    // The tally states the corpus, never the filter — and the announcement
    // is the same clauses in the same order, so the two cannot disagree.
    T.clear(tally);
    const wanted = voiceSelect.value;
    const blockedClause = blocked.length +
      (blocked.length === 1 ? ' work' : ' works') + ' held, not renderable yet';
    let head;
    const extras = [];
    if (unfetched) {
      head = 'The commentary record did not load';
    } else {
      head = total
        ? total + (total === 1 ? ' fragment held' : ' fragments held')
        : blocked.length ? blockedClause : 'Nothing held here';
      // "none in X" is provable only with no blocked row standing.
      if (total && wanted && count < total && (count || !blocked.length)) {
        extras.push((count ? count + ' in ' : 'none in ') + voicePhrase(M.parseVoiceKey(wanted)));
      }
      if (total && blocked.length) extras.push(blockedClause);
      if (leads.length) {
        extras.push(leads.length +
          (leads.length === 1 ? ' lead entry' : ' lead entries') +
          ' on the acquisition list');
      }
    }
    const bold = unfetched ? '' : String(total || blocked.length || 'Nothing');
    if (bold) tally.appendChild(T.el('b', null, bold));
    tally.appendChild(textNode(
      head.slice(bold.length) + extras.map((one) => ' · ' + one).join('')));

    T.statusLine(
      book.name + ' ' + chapter + ', ' + bible.label + ', ' +
        (unfetched
          ? 'commentary record unavailable'
          : [head].concat(extras).join(', ')) + '.'
    );
    writeRoute(wasArrival);
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
    chapterSelect.value = String(wanted);
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
    if (!bookSelect.value) bookSelect.value = (index.canon[0] || {}).token;
    fillChapters(bookSelect.value, broken.has('chapter') ? 1 : hash.get('chapter') || 1);
    bibleSelect.value =
      (!broken.has('bible') && hash.get('bible')) || (bibles[0] || {}).id || '';
    voiceSelect.value = '';
    wantedVoice = broken.has('voice') ? '' : hash.get('voice') || '';
    updateSteps();
  }

  function onArrival(next) {
    const bad = hashProblems(next);
    seedControls(next, new Set(bad.map((one) => one.key)));
    if (bad.length) {
      // Fail closed: the address stays as written, no stale chapter under
      // it; the seeded controls hold the nearest valid route.
      renderInvalid(bad);
      return;
    }
    arrival = true;
    render();
  }

  /* -------------------------------------------------------------- start */

  // Never a permanent "Loading…" over a failed bootstrap.
  function labelSelects(label) {
    for (const select of [bookSelect, chapterSelect, bibleSelect, voiceSelect]) {
      T.fillSelect(select, [{ value: '', label: label }]);
      select.disabled = true;
    }
  }

  function startFailed(message) {
    reference.textContent = 'Unavailable';
    labelSelects('Unavailable');
    T.fail(message);
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
        // Optional: without the paragraph layer, the chapter runs on.
        cached(paragraphFiles, 'structure/paragraphs/index.json', null)
      ]);
    } catch (error) {
      startFailed('The catena index could not be loaded: ' + (error.message || error));
      return;
    }
    if (!manifest.ok) {
      startFailed(manifest.message);
      return;
    }
    bibles = manifest.bibles;

    T.fillSelect(bookSelect,
      (index.canon || []).map((book) => ({ value: book.token, label: book.name })));
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
