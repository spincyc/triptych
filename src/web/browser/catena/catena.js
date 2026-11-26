/* Chapter and chronological commentary. The model owns membership and
 * numbering; the generator owns rights. Fragment prose is fetched on demand. */

'use strict';

(function () {
  const T = window.Triptych;
  const M = window.CatenaModel;
  const textNode = (said) => document.createTextNode(said);
  const { sound, bag, voiceLabel } = M;
  M.useLanguageNames(T.languageName);

  const reference = document.getElementById('reference');
  const referenceBook = document.getElementById('reference-book');
  const tally = document.getElementById('tally');
  const reading = document.getElementById('reading');
  const bookSelect = document.getElementById('book-select');
  const chapterSelect = document.getElementById('chapter-select');
  const bibleSelect = document.getElementById('bible-select');
  // `#language-select` in markup; the hash key is `voice`.
  const voiceSelect = document.getElementById('language-select');
  const prevButton = document.getElementById('prev-button');
  const nextButton = document.getElementById('next-button');
  const controlsDisclosure = document.getElementById('controls-filter');
  const finderDisclosure = document.getElementById('commentary-finder');
  const verseInput = document.getElementById('verse-input');
  const verseError = document.getElementById('verse-error');
  const verseApply = document.getElementById('verse-apply');
  const verseClear = document.getElementById('verse-clear');
  const readCommentary = document.getElementById('read-commentary');
  let selectedVerses = '';
  let viewMode = 'author';

  let index = null;
  let bibles = [];
  let canon = { books: [], whole: false };
  let voices = { keys: [], whole: false };
  let editions = { bibles: [], whole: false };
  const chapterFiles = new Map();
  const scriptureFiles = new Map();
  const fragmentTexts = new Map();
  const paragraphFiles = new Map();
  const asking = new WeakMap();
  const substitutes = new Map();
  let paragraphs = null;
  const hiddenAuthors = new Set();
  let wantedVoice = '';
  let showingError = false;
  let arrival = false;
  const ABSENT = { absent: true };
  const seen = (file) => (file === ABSENT ? undefined : file);
  const textLoaders = new WeakMap();
  let printableChapter = false;
  const printing = T.bindPrint({
    root: reading,
    host: document.querySelector('.page-header'),
    label: 'Print chapter and selected commentary',
    identity: () => reference.textContent + ' — ' +
      bibleSelect.selectedOptions[0].textContent + ' — ' +
      voiceSelect.selectedOptions[0].textContent + (hiddenAuthors.size
        ? ' — Excluding authors: ' + [...hiddenAuthors].sort().join(', ') : ''),
    prepare: async () => {
      if (!printableChapter) return false;
      const selected = Array.from(reading.querySelectorAll('.fragment-body'))
        .filter((details) => !details.closest('[hidden]'));
      const results = await Promise.all(selected.map((details) => textLoaders.get(details)()));
      return results.every(Boolean);
    }
  });

  /* --------------------------------------------------------------- data */

  function canonEntry(token) {
    const wanted = sound(token);
    return canon.books.find((one) => one.token === wanted) || null;
  }

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

  function gone(path) {
    let one = substitutes.get(path);
    if (!one) substitutes.set(path, (one = { unfetched: path }));
    return one;
  }

  function chapterFile(token, chapter) {
    const path = M.chapterPath(index, token, chapter);
    if (!path) return Promise.resolve(path === null ? gone('the index record') : null);
    return cached(chapterFiles, path, gone(path))
      .then((file) => (M.spineUnreadable(file) ? gone(path) : file));
  }

  function chapterParagraphs(bible, token, chapter) {
    const path = M.paragraphPath(paragraphs, bible.id, bag(canonEntry(token)).path, chapter, token);
    return path === null ? Promise.resolve({ unfetched: true })
      : path ? cached(paragraphFiles, path, ABSENT)
        .then(seen, () => ({ unfetched: true }))
      : Promise.resolve(undefined);
  }

  function scriptureChapter(bible, token, chapter) {
    return M.readScripture(index, token, chapter, bible, {
      file: (path) => cached(scriptureFiles, path),
      chapter: (book, number) => T.loadChapter(bible.id, book, number),
      paragraphs: (book, number) => chapterParagraphs(bible, book, number),
      pick: (citation) => T.editionLoci(citation, bible),
      recast: (citation, picked) => T.recastLoci(citation, bible, index.numbering, picked),
      format: T.formatLoci
    });
  }

  function fragmentText(row) {
    const path = M.textAsked(row);
    const owner = M.rowTransport(row);
    if (!owner) return Promise.resolve(null);
    if (!path) return Promise.resolve(M.textCompleted(owner, M.NO_TEXT));
    const held = asking.get(owner);
    if (held) return held;
    const done = fragmentTexts.get(path);
    if (done) return Promise.resolve(M.textCompleted(owner, done));
    const asked = T.loadJSON(path).then(
      (file) => {
        const content = M.textPayload(file);
        if (!fragmentTexts.has(path)) fragmentTexts.set(path, content);
        return M.textCompleted(owner, content);
      },
      (error) => { asking.delete(owner); throw M.textFailed(owner, error); }
    );
    asking.set(owner, asked);
    return asked;
  }

  /* -------------------------------------------- scripture & verse linkage */

  function reducedMotion() {
    return typeof window.matchMedia === 'function' &&
      window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  }

  function scrollScriptureTo(container, target) {
    if (!container || !target || typeof container.scrollTo !== 'function' ||
        typeof container.getBoundingClientRect !== 'function') return false;
    if (container.scrollHeight <= container.clientHeight + 2) return false;
    const box = container.getBoundingClientRect();
    const rect = target.getBoundingClientRect();
    const top = container.scrollTop + (rect.top - box.top) -
      Math.max(24, (container.clientHeight - rect.height) * 0.3);
    container.scrollTo({ top: Math.max(0, top), behavior: reducedMotion() ? 'auto' : 'smooth' });
    return true;
  }

  function highlightVerses(linkCtx, span, scroll) {
    if (!linkCtx) return;
    for (const node of linkCtx.active) node.classList.remove('verse-active');
    linkCtx.active = [];
    if (!span) return;
    const lo = Math.max(1, span.start);
    const hi = span.end !== null ? Math.min(span.end, linkCtx.maxVerse) : linkCtx.maxVerse;
    for (let v = lo; v <= hi; v += 1) {
      const node = linkCtx.nodes.get(v);
      if (node) {
        node.classList.add('verse-active');
        linkCtx.active.push(node);
      }
    }
    if (scroll && linkCtx.active.length) {
      scrollScriptureTo(linkCtx.container, linkCtx.active[0]);
    }
  }

  function renderChapter(container, bible, book, chapter, result, marks, linkCtx) {
    const section = T.el('section', 'chapter');
    if (!result.ok) {
      section.appendChild(T.notice(M.humanRefusal(result.problem, bible.label)));
      container.appendChild(section);
      return;
    }
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

    const body = T.el('div', 'passage');
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
      const vKey = String(line.number);
      if (linkCtx) {
        verse.setAttribute('data-verse', vKey);
        linkCtx.nodes.set(line.number, verse);
        if (linkCtx.focus && linkCtx.focus.first !== null &&
            line.number >= linkCtx.focus.first && line.number <= linkCtx.focus.last) {
          verse.classList.add('verse-focused');
        }
      }
      const hit = linkCtx && linkCtx.map && linkCtx.map.byVerse[vKey];
      if (hit) {
        verse.classList.add('has-commentary');
        const num = T.el('button', 'verse-num verse-trigger', vKey);
        num.type = 'button';
        const active = selectedVerses === vKey;
        num.setAttribute('aria-pressed', String(active));
        const label = 'Verse ' + vKey + ' — ' + hit.count +
          (hit.count === 1 ? ' commentary fragment' : ' commentary fragments') +
          (active ? '; click to show whole chapter' : '; click to focus');
        num.setAttribute('aria-label', label);
        num.setAttribute('title', label);
        num.addEventListener('click', () => {
          if (selectedVerses === vKey) { resetVerses(); render(); }
          else {
            selectedVerses = verseInput.value = vKey;
            verseError.hidden = true;
            render('verse-click');
          }
        });
        verse.appendChild(num);
      } else {
        verse.appendChild(T.el('sup', 'verse-num', vKey));
      }
      verse.appendChild(textNode(line.text + ' '));
      passage.appendChild(verse);
    }

    const holder = T.el('details', 'chapter-body');
    holder.open = true;
    const head = T.el('summary', 'chapter-head');
    head.appendChild(T.el('span', 'chapter-name', result.label || book.name + ' ' + chapter));
    head.appendChild(T.el('span', 'chapter-count',
      lines.length + (lines.length === 1 ? ' verse' : ' verses')));
    if (printed + projected) {
      head.appendChild(T.el('span', 'chapter-count',
        opened + (opened === 1 ? ' paragraph' : ' paragraphs')));
    }
    holder.appendChild(head);
    holder.appendChild(body);
    holder.appendChild(T.el('p', 'paragraph-note', M.paragraphNote(read)));
    section.appendChild(holder);
    container.appendChild(section);
  }

  /* ----------------------------------------------- structured commentary */

  function appendInline(parent, raw, spans) {
    let at = 0;
    for (const [s, e, tag, cls] of spans) {
      if (s < at) continue;
      if (s > at) parent.appendChild(textNode(raw.slice(at, s)));
      parent.appendChild(T.el(tag, cls, raw.slice(s, e)));
      at = e;
    }
    if (at < raw.length) parent.appendChild(textNode(raw.slice(at)));
  }

  // Build structured blocks via createElement/textContent while preserving exact
  // whitespace text nodes between block boxes so `container.textContent === raw`.
  function renderBlocks(container, content, raw, range) {
    const blocks = M.textBlocks(content, range);
    if (!blocks.length) { container.textContent = raw; return; }
    const parts = [];
    let cursor = 0;
    for (const block of blocks) {
      const at = raw.indexOf(block.text, cursor);
      if (at < 0 || /\S/.test(raw.slice(cursor, at))) { container.textContent = raw; return; }
      parts.push({ gap: raw.slice(cursor, at), block });
      cursor = at + block.text.length;
    }
    const tail = raw.slice(cursor);
    if (/\S/.test(tail)) { container.textContent = raw; return; }
    T.clear(container);
    for (const { gap, block } of parts) {
      if (gap) container.appendChild(textNode(gap));
      const el = T.el(block.kind === 'lemma' ? 'blockquote' : 'p',
        block.kind === 'lemma' ? 'fragment-lemma' : 'fragment-para');
      const spans = [];
      if (block.speaker) spans.push([block.speaker[0], block.speaker[1], 'strong', 'speaker-name']);
      if (block.transition) spans.push([block.transition[0], block.transition[1], 'em', 'lemma-transition']);
      for (const note of block.notes) spans.push([note[0], note[1], 'span', 'ed-note']);
      spans.sort((a, b) => a[0] - b[0] || a[1] - b[1]);
      if (spans.length) appendInline(el, block.text, spans);
      else el.textContent = block.text;
      container.appendChild(el);
    }
    if (tail) container.appendChild(textNode(tail));
  }

  function shortLocator(locator, extentText) {
    let text = sound(locator).replace(/\s*\(Oxford English lemma numbering\)\s*$/i, '').trim();
    if (!text) return '';
    const semi = text.indexOf(';');
    if (semi > 0) text = text.slice(0, semi).trim();
    const norm = (s) => s.replace(/[\u2013\u2014]/g, '-').trim();
    const nExt = norm(extentText);
    const nText = norm(text);
    if (nText === nExt) return '';
    if (nExt && nText.startsWith(nExt) && /^[,;:\s]/.test(nText.slice(nExt.length))) {
      text = text.slice(nExt.length).replace(/^[,;:\s\u2013\u2014-]+/, '').trim();
    }
    return text.length > 72 ? text.slice(0, 71).trimEnd() + '…' : text;
  }

  function licence(note) {
    const block = T.el('p', 'fragment-acknowledgement');
    block.appendChild(T.el('strong', null, 'Licence: '));
    block.appendChild(textNode(note));
    return block;
  }

  function renderFragment(fragment, bookName, chapter, verses, versions, linkCtx) {
    const item = T.el('li', 'fragment');
    item.setAttribute('data-state', 'held');
    const details = fragmentDetails(fragment, bookName, chapter, verses, null, linkCtx, null);
    item.appendChild(details);
    if (versions.length) {
      const head = details.firstChild;
      head.appendChild(T.el('span', 'version-available', 'English available'));
      const versionsBox = T.el('div', 'paired-english');
      const apparatus = Array.from(details.children).find((c) => c.classList.contains('fragment-apparatus'));
      details.insertBefore(versionsBox, apparatus || null);
      const labels = M.englishVersionLabels(versions, bookName);
      for (const [n, version] of versions.entries()) {
        const option = T.el('div');
        const button = T.el('button', 'link-button version-title', labels[n]);
        button.type = 'button';
        button.setAttribute('aria-expanded', 'false');
        option.appendChild(button);
        versionsBox.appendChild(option);
        let edition;
        button.addEventListener('click', () => {
          const open = button.getAttribute('aria-expanded') === 'false';
          if (!edition) {
            edition = fragmentDetails(version.fragment, bookName, chapter, verses, version, null, fragment);
            option.appendChild(edition);
          }
          edition.hidden = !open;
          button.setAttribute('aria-expanded', String(open));
          if (open) textLoaders.get(edition)();
        });
      }
    }
    return item;
  }

  function fragmentDetails(fragment, bookName, chapter, verses, version, linkCtx, parent) {
    const details = version ? T.el('div', 'english-edition') : T.el('details', 'fragment-body');
    const sameWork = Boolean(version && parent &&
      fragment.author === parent.author && fragment.work === parent.work);
    const extentText = M.formatExtent(fragment.extent, bookName);
    if (!sameWork) {
      const head = T.el(version ? 'div' : 'summary', 'fragment-head');
      const extent = T.el('span', 'fragment-extent', extentText);
      if (M.spansChapters(fragment.extent)) {
        extent.appendChild(textNode(' '));
        extent.appendChild(T.el('span', 'spans', '— runs across the chapter boundary'));
      }
      head.appendChild(extent);
      const loc = !version ? shortLocator(fragment.locator, extentText) : '';
      if (loc) head.appendChild(T.el('span', 'fragment-locator', loc));
      head.appendChild(T.el('span', 'fragment-author', fragment.author));
      head.appendChild(T.el('span', 'fragment-work', fragment.work));
      const date = fragment.date || M.compositionDateLabel(fragment);
      if (date) head.appendChild(T.el('span', 'fragment-date', date));
      const named = M.languageChip(fragment);
      if (named) head.appendChild(T.el('span', 'fragment-language', named));
      const words = fragment.text_words;
      if (words) {
        head.appendChild(T.el('span', 'fragment-length',
          words.toLocaleString() + ' words'));
      }
      details.appendChild(head);
    }
    if (version) details.appendChild(T.el('p', 'fragment-basis', version.basis));

    const code = fragment.language;
    const text = T.el('div', 'fragment-text', 'Loading…');
    if (code) text.lang = code;
    details.appendChild(text);

    const span = !version && linkCtx ? M.fragmentChapterSpan(fragment, chapter) : null;
    if (span) {
      const label = 'See ' + (span.end === null ? 'vv. ' + span.start + 'ff.'
        : span.end !== span.start ? 'vv. ' + span.start + '–' + span.end : 'v. ' + span.start);
      const jump = T.el('button', 'link-button fragment-jump', label);
      jump.type = 'button';
      jump.addEventListener('click', () => {
        linkCtx.pinned = span;
        highlightVerses(linkCtx, span, true);
        if (linkCtx.container && linkCtx.container.scrollHeight <= linkCtx.container.clientHeight + 2 &&
            typeof linkCtx.container.scrollIntoView === 'function') {
          linkCtx.container.scrollIntoView({ behavior: reducedMotion() ? 'auto' : 'smooth', block: 'start' });
        }
      });
      details.appendChild(jump);
    }

    const apparatus = T.el('div', 'fragment-apparatus');
    details.appendChild(apparatus);
    let recordedNotes = [];
    let notesFold = null;
    const addNotes = (incoming) => {
      const merged = M.dedupeNotes(recordedNotes.concat(incoming));
      if (merged.length === recordedNotes.length) return;
      if (!notesFold) {
        notesFold = T.el('details', 'fragment-notes');
        notesFold.appendChild(T.el('summary', null, 'Editorial & dating notes'));
        apparatus.appendChild(notesFold);
      }
      for (let i = recordedNotes.length; i < merged.length; i += 1) {
        notesFold.appendChild(T.el('p', 'fragment-basis', merged[i]));
      }
      recordedNotes = merged;
    };
    if (fragment.composition_date_basis) {
      addNotes(['Date — ' + fragment.composition_date_basis]);
    }

    let acknowledged = 0;
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
    let pending = null;
    let printComplete = false;
    function ensureText() {
      if (asked) return pending || Promise.resolve(printComplete);
      asked = true;
      if (fragment.text_refused) {
        text.className = 'fragment-text missing';
        text.textContent = fragment.text_note;
        return Promise.resolve(false);
      }
      const wrote = (completed, write) => {
        let said = null;
        try { said = write(); } catch (problem) { said = null; }
        if (said === text.textContent) M.bodyApplied(fragment, completed, true);
        return said === text.textContent;
      };
      pending = fragmentText(fragment).then(
        (completed) => {
          if (!reading.contains(details) || !M.bodyAsked(fragment, completed)) return false;
          const body = completed.content;
          let complete = false;
          const applied = wrote(completed, () => {
            if (body.present) acknowledge(body.acknowledgement, body.acknowledgement_broken);
            const say = M.bodySaying(body);
            complete = !say.missing;
            text.className = say.missing ? 'fragment-text missing' : 'fragment-text';
            if (say.missing) {
              text.textContent = say.said;
            } else {
              renderBlocks(text, body, say.said);
              const extra = [];
              const snippets = M.matchingSnippets(body, fragment.extent.token, chapter, verses);
              if (snippets.length) {
                const excerpts = T.el('div', 'fragment-snippets');
                for (const snippet of snippets) {
                  excerpts.appendChild(T.el('p', 'fragment-basis',
                    'Excerpt — ' + M.formatExtent(snippet.extent, bookName) + ' · ' + snippet.locator));
                  const words = T.el('div', 'fragment-text snippet-text');
                  if (code) words.lang = code;
                  renderBlocks(words, body, snippet.text, snippet);
                  excerpts.appendChild(words);
                  extra.push('Excerpt — ' + snippet.basis);
                }
                const context = T.el('details', 'fragment-context');
                context.appendChild(T.el('summary', 'fragment-basis',
                  'Read full context — ' + extentText));
                details.insertBefore(excerpts, text);
                details.insertBefore(context, text);
                context.appendChild(text);
              }
              if (body.basis) extra.push('Extent — ' + body.basis);
              if (body.date_basis && !fragment.composition_date_basis) {
                extra.push('Date — ' + body.date_basis);
              }
              addNotes(extra);
            }
            return say.said;
          });
          printComplete = complete && applied;
          return printComplete;
        },
        (failed) => {
          if (!reading.contains(details) || !M.bodyAsked(fragment, failed)) return false;
          asked = false;
          const error = failed.error;
          wrote(failed, () => {
            const said = M.failureSaid(error instanceof T.NotFound, error);
            text.className = 'fragment-text missing';
            text.textContent = said;
            return said;
          });
          return false;
        }
      );
      return pending;
    }
    textLoaders.set(details, ensureText);
    if (!version) {
      details.addEventListener('toggle', () => {
        if (details.open) {
          ensureText();
          if (span) { linkCtx.pinned = span; highlightVerses(linkCtx, span, true); }
        } else if (span && linkCtx.pinned === span) {
          linkCtx.pinned = null;
          highlightVerses(linkCtx, null, false);
        }
      });
      if (span) {
        details.addEventListener('mouseenter', () => highlightVerses(linkCtx, span, false));
        details.addEventListener('mouseleave', () => highlightVerses(linkCtx, linkCtx.pinned, false));
        details.addEventListener('focusin', () => highlightVerses(linkCtx, span, false));
      }
    }

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
    fact(fragment.rights_basis);
    if (fragment.review && fragment.review !== 'verified') {
      source.appendChild(T.el('span', 'sep'));
      source.appendChild(T.el('span', 'state', fragment.review + ', not collated'));
    }
    if (fragment.id) {
      source.appendChild(T.el('span', 'sep'));
      const whole = T.el('a', 'fragment-whole', 'Open this passage in the Source Library');
      whole.href = '../sources/#passage=' + encodeURIComponent(fragment.id);
      source.appendChild(whole);
    }
    details.appendChild(source);
    return details;
  }

  function renderAbsences(container, file, wanted) {
    const asked = M.parseVoiceKey(wanted);
    if (!asked || asked.voice !== M.TRANSLATION) return;
    const rows = M.absenceRows(index, file, asked.language);
    if (!rows.length) {
      const unread = M.absencesUnread(index);
      if (unread) container.appendChild(T.el('p', 'aside-note', unread));
      return;
    }

    const note = T.el('details', 'absence-note');
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
      if (row.author && row.work) item.appendChild(textNode(' — '));
      item.appendChild(T.el('span', 'absence-work', row.work));
      if (row.reason) item.appendChild(T.el('p', 'absence-reason', row.reason));
      if (row.offer) item.appendChild(T.el('p', 'absence-partial', row.offer));
      items.appendChild(item);
    }
    note.appendChild(items);
    container.appendChild(note);
  }

  function renderChain(container, file, book, linkCtx, destination) {
    const wanted = voiceSelect.value;
    const chapter = Number(chapterSelect.value);
    const selection = M.passageSelection(file, chapter, selectedVerses, wanted, []);
    const held = selection.fragments;
    const heading = T.el('h2', 'section-heading', selection.heading);
    container.appendChild(heading);
    if (selectedVerses) {
      const chip = T.el('div', 'focus-chip');
      chip.appendChild(T.el('span', null, 'Focused on ' + book.name + ' ' + chapter + ':' + selectedVerses));
      const clearBtn = T.el('button', 'link-button focus-clear', 'Show whole chapter');
      clearBtn.type = 'button';
      clearBtn.addEventListener('click', () => { resetVerses(); render(); });
      chip.appendChild(clearBtn);
      container.appendChild(chip);
    }
    container.appendChild(T.el('p', 'english-availability', selection.availability));
    if (selection.contextNote) container.appendChild(T.el('p', 'aside-note', selection.contextNote));
    if (!held.length) {
      container.appendChild(T.el('p', 'aside-note', selection.empty));
      renderAbsences(container, file, wanted);
      return 0;
    }

    if (wanted) {
      const said = M.otherVoicesNote(wanted,
        M.chapterVoices(file).filter((one) => one.key !== wanted));
      if (said) container.appendChild(T.el('p', 'aside-note', said));
    }

    const chapterRows = M.chapterFragments(file);
    const allChapterGroups = M.commentaryGroups(chapterRows);
    const groups = M.commentaryGroups(held);
    const autoOpen = allChapterGroups.length === 1 ||
      (destination === 'verse-click' && groups.length <= 2);

    const toolbar = T.el('div', 'chain-toolbar');
    const views = T.el('div', 'chain-views');
    views.setAttribute('role', 'group');
    views.setAttribute('aria-label', 'Commentary order');
    const byAuthorBtn = T.el('button', 'chain-tool', 'By author');
    const byVerseBtn = T.el('button', 'chain-tool', 'By verse');
    byAuthorBtn.type = byVerseBtn.type = 'button';
    views.appendChild(byAuthorBtn);
    views.appendChild(byVerseBtn);
    toolbar.appendChild(views);
    const expandBtn = T.el('button', 'chain-tool chain-expand', 'Expand all');
    expandBtn.type = 'button';
    toolbar.appendChild(expandBtn);
    container.appendChild(toolbar);

    const authors = selection.authors;
    let filterHolder = null;
    const filterNote = T.el('p');
    filterNote.hidden = true;
    container.appendChild(filterNote);

    let chain = null;
    let undated = null;
    let rendered = [];
    let toggleTargets = [];

    function syncExpandLabel() {
      const visible = toggleTargets.filter((t) => !t.item.hidden);
      const anyClosed = visible.some((t) => !t.node.open);
      expandBtn.textContent = anyClosed ? 'Expand all' : 'Collapse all';
      expandBtn.disabled = !visible.length;
    }

    function applyFilter() {
      for (const row of rendered) {
        const on = !(row.author && hiddenAuthors.has(row.author));
        row.item.hidden = !on;
      }
      const filtered = M.passageSelection(file, chapter, selectedVerses, wanted, [...hiddenAuthors]);
      heading.textContent = filtered.heading;
      filterNote.textContent = filtered.empty;
      filterNote.hidden = !filtered.empty;
      filterNote.className = filtered.empty ? 'aside-note' : '';
      if (!filtered.visible.length && filterHolder) filterHolder.open = true;
      syncExpandLabel();
    }

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
          printing.invalidate();
          if (box.checked) hiddenAuthors.delete(name);
          else hiddenAuthors.add(name);
          applyFilter();
        });
        label.appendChild(box);
        label.appendChild(textNode(name));
        filter.appendChild(label);
      }
      filterHolder = T.el('details', 'author-filter-disclosure');
      filterHolder.appendChild(T.el('summary', null, 'Filter authors'));
      filterHolder.appendChild(filter);
      if (hiddenHere) filterHolder.open = true;
      container.appendChild(filterHolder);
    }

    // Anchor node keeps `<ul class="chain">` a direct child of `.chain-column`.
    const afterList = document.createTextNode('');
    container.appendChild(afterList);

    function buildList() {
      if (chain && chain.parentNode) chain.parentNode.removeChild(chain);
      if (undated && undated.parentNode) undated.parentNode.removeChild(undated);
      chain = T.el('ul', 'chain');
      undated = null;
      let undatedChain = null;
      rendered = [];
      toggleTargets = [];
      byAuthorBtn.setAttribute('aria-pressed', String(viewMode === 'author'));
      byVerseBtn.setAttribute('aria-pressed', String(viewMode === 'verse'));

      if (viewMode === 'verse') {
        for (const fragment of M.commentaryByVerse(held, chapter)) {
          const item = renderFragment(fragment, book.name, chapter, selectedVerses,
            M.englishVersions(fragment, chapterRows), linkCtx);
          chain.appendChild(item);
          rendered.push({ author: fragment.author, item });
          toggleTargets.push({ item, node: item.firstChild });
        }
      } else {
        for (const group of groups) {
          if (group.undated && !undated) {
            undated = T.el('section', 'aside');
            undated.setAttribute('data-date-state', 'unestablished');
            undated.appendChild(T.el('h3', 'section-heading', M.UNESTABLISHED_DATE));
            undatedChain = T.el('ul', 'chain');
            undated.appendChild(undatedChain);
          }
          const item = T.el('li', 'author');
          const works = new Set(group.fragments.map((f) => f.work).filter(Boolean));
          const singleWork = works.size === 1 && group.fragments.every((f) => f.work);
          if (singleWork) item.classList.add('author-single-work');
          if (group.undated) item.classList.add('author-undated');
          const node = T.el('details', 'author-body');
          if (autoOpen) node.open = true;

          const summary = T.el('summary', 'author-head');
          summary.appendChild(T.el('span', 'author-name', group.author));
          if (singleWork) summary.appendChild(T.el('span', 'author-work', [...works][0]));
          if (group.date !== null) {
            summary.appendChild(T.el('span', 'author-date', String(group.date)));
          }
          summary.appendChild(T.el('span', 'author-count',
            group.fragments.length === 1 ? '1 fragment' : group.fragments.length + ' fragments'));
          node.appendChild(summary);

          const inner = T.el('ul', 'author-fragments');
          for (const fragment of group.fragments) {
            const row = renderFragment(fragment, book.name, chapter, selectedVerses,
              M.englishVersions(fragment, chapterRows), linkCtx);
            inner.appendChild(row);
            if (groups.length === 1) toggleTargets.push({ item, node: row.firstChild });
          }
          node.appendChild(inner);
          item.appendChild(node);
          (group.undated ? undatedChain : chain).appendChild(item);
          rendered.push({ author: group.author, item });
          if (groups.length > 1) {
            toggleTargets.push({ item, node });
            node.addEventListener('toggle', syncExpandLabel);
          }
        }
      }
      if (chain.children.length) container.insertBefore(chain, afterList);
      if (undated) container.insertBefore(undated, afterList);
      applyFilter();
    }

    byAuthorBtn.addEventListener('click', () => {
      if (viewMode === 'author') return;
      viewMode = 'author';
      buildList();
    });
    byVerseBtn.addEventListener('click', () => {
      if (viewMode === 'verse') return;
      viewMode = 'verse';
      buildList();
    });
    expandBtn.addEventListener('click', () => {
      const visible = toggleTargets.filter((t) => !t.item.hidden);
      const shouldOpen = visible.some((t) => !t.node.open);
      for (const target of visible) {
        if (Boolean(target.node.open) !== shouldOpen) {
          target.node.open = shouldOpen;
          if (shouldOpen && textLoaders.has(target.node)) textLoaders.get(target.node)();
        }
      }
      syncExpandLabel();
    });

    buildList();
    renderAbsences(container, file, wanted);
    return held.length;
  }

  /* ----------------------------------- the things that are not fragments */

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

  function renderRefusal(container, file, bible, book, chapter) {
    const sentence = M.refusalNote(file, bible.id, chapter);
    if (!sentence) return false;
    const node = T.el('p', 'refusal');
    node.setAttribute('data-state', 'refusal');
    node.appendChild(T.el('strong', null, 'Boundary not established. '));
    node.appendChild(textNode(
      sentence + ' Commentary on ' + book.name + ' ' + chapter +
        ' is anchored in Vulgate numbering, and this page will not guess ' +
        'where the boundary moves to in ' + bible.label +
        '. The commentary keeps its canonical address.'));
    container.appendChild(node);
    return true;
  }

  /* ------------------------------------ the cited state, failing closed */

  function errorSection(title) {
    const section = T.el('section', 'catena-error');
    section.setAttribute('data-state', 'error');
    section.appendChild(T.el('h2', 'section-heading', title));
    return section;
  }

  function focusKeeper() {
    const lost = reading.contains(document.activeElement);
    return () => { if (lost) reading.focus(); };
  }

  function renderInvalid(bad) {
    readCommentary.disabled = true;
    printableChapter = false;
    printing.invalidate();
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

  async function render(destination) {
    readCommentary.disabled = true;
    printableChapter = false;
    printing.invalidate();
    const wasArrival = arrival;
    arrival = false;
    if (!wasArrival) wantedVoice = '';
    const token = bookSelect.value;
    const chapter = Number(chapterSelect.value);
    const bible = bibles.find((one) => one.id === bibleSelect.value);
    const book = canonEntry(token);
    if (!book || !bible || !Number.isFinite(chapter)) {
      startFailed('The catena index could not be read.');
      return;
    }

    const renderToken = T.beginRender();
    reading.setAttribute('aria-busy', 'true');

    reference.textContent = book.name + ' ' + chapter + (selectedVerses ? ':' + selectedVerses : '');
    referenceBook.textContent = book.testamentName;

    const refocus = focusKeeper();
    let file, scripture, focusProblem;
    try {
      [file, scripture, focusProblem] = await Promise.all([
        chapterFile(token, chapter),
        scriptureChapter(bible, token, chapter),
        M.passageProblem(index, token, chapter, selectedVerses, (path) => cached(scriptureFiles, path))
      ]);
      if (!T.isCurrentRender(renderToken)) return;
      if (focusProblem) {
        resetVerses();
        renderInvalid([focusProblem]);
        return;
      }

      const unfetched = M.chapterUnfetched(file);
      const blocked = M.chapterBlocked(file);
      const leads = M.chapterLeads(file);
      const total = M.chapterTally(file);
      fillVoices(file, unfetched || blocked.length);
      T.clear(reading);
      let count = 0;
      const refused = renderRefusal(reading, file, bible, book, chapter);
      const scriptureColumn = T.el('div', 'chapter');
      const focus = M.passageSelection(file, chapter, selectedVerses, voiceSelect.value, []);
      if (focus.focusNote) scriptureColumn.appendChild(T.el('p', 'focus-note', focus.focusNote));
      let linkCtx = null;
      if (scripture.ok) {
        if (scripture.note) {
          scriptureColumn.appendChild(T.el('p', 'citation-recast', M.humanRecast(scripture.note)));
        }
        const canonicalDirect = scripture.parts.length === 1 && !scripture.note && !refused;
        if (canonicalDirect) {
          const lines = M.chapterReading(scripture.parts[0].verses, scripture.parts[0].marks).lines;
          const maxVerse = lines.length ? lines[lines.length - 1].number : null;
          const voiceRows = M.passageSelection(file, chapter, '', voiceSelect.value, []).fragments;
          linkCtx = {
            nodes: new Map(),
            map: M.verseCommentaryMap(voiceRows, chapter, maxVerse),
            focus: M.parseVerses(selectedVerses),
            active: [],
            pinned: null,
            maxVerse: maxVerse || 0,
            container: scriptureColumn
          };
        }
        for (const part of scripture.parts) {
          renderChapter(scriptureColumn, bible, part, part.chapter,
            { ok: true, verses: part.verses, label: part.label }, part.marks, linkCtx);
        }
      } else renderChapter(scriptureColumn, bible, book, chapter, scripture);
      reading.appendChild(scriptureColumn);
      if (unfetched) {
        const section = errorSection('This chapter’s commentary record did not load');
        section.appendChild(T.el('p', 'error-detail',
          'The index records commentary on ' + book.name + ' ' + chapter +
            ', but its record (' + unfetched + ') could not be read — a ' +
            'data or connection fault, not an empty ' +
            'chapter. Reloading may recover it.'));
        reading.appendChild(section);
      } else {
        const column = T.el('div', 'chain-column');
        column.setAttribute('tabindex', '-1');
        column.setAttribute('role', 'region');
        column.setAttribute('aria-label', 'Commentary fragments');
        count = renderChain(column, file, book, linkCtx, destination);
        renderLeads(column, leads);
        renderBlocked(column, blocked);
        reading.appendChild(column);
        readCommentary.disabled = false;
      }
      reading.setAttribute('aria-busy', 'false');
      printableChapter = !unfetched && !blocked.length && scripture.ok &&
        scripture.parts.every((part) => {
          const checked = M.chapterReading(part.verses, part.marks);
          return !checked.versesUnread && checked.lines.length > 0;
        });
      refocus();
      if (destination === 'commentary') focusCommentary();
      if (linkCtx && linkCtx.focus && linkCtx.focus.first !== null) {
        const firstFocused = linkCtx.nodes.get(linkCtx.focus.first);
        if (firstFocused) scrollScriptureTo(scriptureColumn, firstFocused);
      }

      T.clear(tally);
      const said = M.chapterSummary({
        total: total,
        shown: M.chapterFragments(file).filter((row) => M.matchesVoice(row, voiceSelect.value)).length,
        blocked: blocked.length,
        leads: leads.length,
        unfetched: !!unfetched,
        voice: voiceSelect.value
      });
      if (said.bold) tally.appendChild(T.el('b', null, said.bold));
      tally.appendChild(textNode(said.tail));
      const matched = count + (count === 1 ? ' fragment matches' : ' fragments match') +
        ' the verse and voice filters';
      if (selectedVerses) tally.appendChild(textNode(' · ' + matched));
      T.statusLine(
        reference.textContent + ', ' + bible.label + ', ' + said.spoken +
          (selectedVerses ? ', ' + matched : '') + '.');
      writeRoute(wasArrival);
    } catch (error) {
      if (!T.isCurrentRender(renderToken)) return;
      fillVoices(null, true);
      T.clear(tally);
      T.fail('This chapter could not be loaded: ' + (error.message || error));
      refocus();
      writeRoute(wasArrival);
    }
  }

  function writeRoute(wasArrival) {
    showingError = false;
    updateSteps();
    const now = T.readHash();
    const identical =
      now.get('book') === bookSelect.value &&
      Number(now.get('chapter')) === Number(chapterSelect.value) &&
      now.get('bible') === bibleSelect.value &&
      (now.get('voice') || '') === voiceSelect.value &&
      (now.get('verses') || '') === selectedVerses;
    if (identical) return;
    if (wasArrival && window.history.replaceState) {
      window.history.replaceState(null, '', currentHashText());
    } else {
      selfWrote = currentHashText();
      T.writeHash([['book', bookSelect.value], ['chapter', chapterSelect.value],
                   ['bible', bibleSelect.value], ['voice', voiceSelect.value], ['verses', selectedVerses]]);
    }
  }

  function fillVoices(file, unknown) {
    const held = M.chapterVoices(file);
    const wanted = voiceSelect.value || wantedVoice;
    wantedVoice = '';
    const items = [{ value: '', label: 'Everything held' }];
    for (const entry of held) items.push({ value: entry.key, label: voiceLabel(entry) });
    if (wanted && !held.some((one) => one.key === wanted)) {
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
    chapterSelect.value = String(Number(wanted) || wanted);
    if (!chapterSelect.value) chapterSelect.value = '1';
  }

  function focusCommentary() {
    const column = reading.querySelector('.chain-column');
    if (column) { column.focus(); column.scrollIntoView({ block: 'start' }); }
  }

  function bindFinder() {
    const holdings = M.commentaryHoldings(index, canon.books);
    if (!holdings.length) return;
    const finder = finderDisclosure;
    const books = document.getElementById('finder-book');
    const chapters = document.getElementById('finder-chapter');
    const english = document.getElementById('finder-english');
    const submit = document.getElementById('finder-open');

    function fillResults(preferred) {
      const book = holdings.find((one) => one.token === books.value);
      const rows = book ? book.chapters.filter((row) => !english.checked || row.english) : [];
      T.fillSelect(chapters, rows.map((row) => ({ value: String(row.chapter),
        label: row.chapter + ' — ' + row.fragments + (row.fragments === 1 ? ' excerpt' : ' excerpts') +
          ' · ' + row.english + ' in English' })));
      if (rows.some((row) => String(row.chapter) === preferred)) chapters.value = preferred;
      submit.disabled = chapters.disabled = !rows.length;
    }

    function fillBooks(preferred, chapter) {
      const found = holdings.filter((book) => !english.checked || book.chapters.some((row) => row.english));
      const count = found.reduce((n, book) =>
        n + book.chapters.filter((row) => !english.checked || row.english).length, 0);
      document.getElementById('finder-count').textContent = count + (count === 1 ? ' chapter' : ' chapters') +
        (english.checked ? ' with English' : '');
      T.fillSelect(books, found.length ? found.map((book) => ({ value: book.token, label: book.name })) :
        [{ value: '', label: 'No chapters with English excerpts' }]);
      if (found.some((book) => book.token === preferred)) books.value = preferred;
      books.disabled = !found.length;
      fillResults(books.value === preferred ? chapter : '');
    }

    english.addEventListener('change', () => fillBooks(books.value, chapters.value));
    books.addEventListener('change', () => fillResults(''));
    finder.addEventListener('toggle', () => {
      if (finder.open) {
        controlsDisclosure.open = false;
        fillBooks(bookSelect.value, chapterSelect.value);
      }
    });
    document.getElementById('finder-form').addEventListener('submit', (event) => {
      event.preventDefault();
      if (!chapters.value) return;
      bookSelect.value = books.value;
      fillChapters(books.value, chapters.value);
      voiceSelect.value = '';
      resetVerses();
      finder.open = false;
      reading.focus();
      render('commentary');
    });
    fillBooks('', '');
    finder.hidden = false;
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
    resetVerses();
    render();
  }

  let selfWrote = null;

  function currentHashText() {
    const parts = [];
    for (const pair of [['book', bookSelect.value], ['chapter', chapterSelect.value],
                        ['bible', bibleSelect.value], ['voice', voiceSelect.value], ['verses', selectedVerses]]) {
      if (pair[1]) parts.push(pair[0] + '=' + encodeURIComponent(pair[1]));
    }
    return parts.length ? '#' + parts.join('&') : '';
  }

  function seedControls(hash, broken) {
    bookSelect.value = (!broken.has('book') && hash.get('book')) || 'Gen';
    if (!bookSelect.value) bookSelect.value = bag(canon.books[0]).token;
    fillChapters(bookSelect.value, broken.has('chapter') ? 1 : hash.get('chapter') || 1);
    bibleSelect.value =
      (!broken.has('bible') && hash.get('bible')) || (bibles[0] || {}).id || '';
    voiceSelect.value = '';
    wantedVoice = broken.has('voice') ? '' : hash.get('voice') || '';
    selectedVerses = broken.has('verses') ? '' : hash.get('verses') || '';
    verseInput.value = selectedVerses;
    verseError.hidden = true;
    updateSteps();
  }

  function onArrival(next) {
    try {
      const bad = M.addressProblems(next, canon, editions, voices);
      seedControls(next, new Set(bad.map((one) => one.key)));
      if (bad.length) { renderInvalid(bad); return; }
      arrival = true;
      render();
    } catch (error) {
      startFailed('The catena index could not be read: ' + (error.message || error));
    }
  }

  function labelSelects(label) {
    if (finderDisclosure) finderDisclosure.hidden = true;
    readCommentary.disabled = true;
    verseInput.disabled = verseApply.disabled = verseClear.disabled = true;
    for (const select of [bookSelect, chapterSelect, bibleSelect, voiceSelect]) {
      T.fillSelect(select, [{ value: '', label: label }]);
      select.disabled = true;
    }
  }

  function startFailed(message) {
    printableChapter = false;
    printing.invalidate();
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
    if (window.matchMedia('(max-width: 59.9375rem)').matches) {
      controlsDisclosure.open = false;
    }
    controlsDisclosure.addEventListener('toggle', () => {
      if (controlsDisclosure.open && finderDisclosure && finderDisclosure.open) {
        finderDisclosure.open = false;
      }
    });
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
        cached(paragraphFiles, 'structure/paragraphs/index.json', ABSENT)
          .then(seen, () => 'unreadable')
      ]);
    } catch (error) {
      startFailed('The catena index could not be loaded: ' + (error.message || error));
      return;
    }
    index = bag(index);
    if (!manifest.ok) { startFailed(manifest.message); return; }
    editions = M.bibleRoot(manifest.bibles);
    bibles = editions.bibles;
    canon = M.canonRoot(index.canon);
    voices = M.voiceRoot(index);

    if (!canon.books.length) return startFailed('The catena index could not be read.');
    if (!bibles.length) return startFailed('The published editions could not be read.');
    T.fillSelect(bookSelect,
      canon.books.map((book) => ({ value: book.token, label: book.name })));
    T.fillBibleSelect(bibleSelect, bibles);
    bookSelect.disabled = chapterSelect.disabled = bibleSelect.disabled = false;
    verseInput.disabled = verseApply.disabled = verseClear.disabled = false;
    bindFinder();

    document.getElementById('passage-focus').addEventListener('submit', async (event) => {
      event.preventDefault();
      const draft = verseInput.value;
      const address = currentHashText();
      const token = bookSelect.value, chapter = Number(chapterSelect.value);
      const focus = M.parseVerses(draft.trim());
      verseError.hidden = !!focus;
      if (!focus) {
        verseError.textContent = 'Enter one verse or an ascending range within this chapter, such as 3 or 3-8.';
        return;
      }
      const problem = await M.passageProblem(index, token, chapter, focus.key,
        (path) => cached(scriptureFiles, path));
      if (currentHashText() !== address || verseInput.value !== draft) return;
      if (problem) {
        verseError.textContent = 'Verse filter ' + problem.note + '.';
        verseError.hidden = false;
        return;
      }
      selectedVerses = verseInput.value = focus.key;
      render();
    });
    verseClear.addEventListener('click', () => { resetVerses(); render(); });
    readCommentary.addEventListener('click', focusCommentary);

    bookSelect.addEventListener('change', () => {
      fillChapters(bookSelect.value, 1);
      resetVerses();
      render();
    });
    chapterSelect.addEventListener('change', () => { resetVerses(); render(); });
    for (const one of [bibleSelect, voiceSelect]) {
      one.addEventListener('change', render);
    }
    prevButton.addEventListener('click', () => step(-1));
    nextButton.addEventListener('click', () => step(1));
    T.onArrowStep(step);
    window.addEventListener('hashchange', () => {
      if (window.location.hash === selfWrote) return void (selfWrote = null);
      selfWrote = null;
      if (!showingError && window.location.hash === currentHashText()) return;
      onArrival(T.readHash());
    });

    onArrival(T.readHash());
  }

  start();

  function resetVerses() {
    selectedVerses = verseInput.value = '';
    verseError.hidden = true;
  }
}());
