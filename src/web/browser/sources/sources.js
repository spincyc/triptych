/* ===========================================================================
 * The Source Library — search the corpus, then read a work passage by passage
 * ===========================================================================
 *
 * Two views on one page, because they are one task interrupted rather than two
 * tasks: FIND a work, then READ it. The hash carries whichever you are in, so a
 * passage is linkable and Catena Omnia can send a reader straight to one.
 *
 * THREE LAYERS, AND YOU PAY FOR WHAT YOU OPEN. The generator writes them and
 * this file follows what it wrote:
 *
 *   index.json                 every work and edition, enough to search on.
 *                              No prose, no apparatus, no passages.
 *   <work-dir>/<edition>.json  one edition: its record, its artifacts, and
 *                              every passage with its locus and its rights
 *                              decision. STILL NO WORDS.
 *   text/<passage-id>.json     one passage's words. Fetched when opened.
 *
 * A reader searching the corpus fetches the first and nothing else. A reader
 * who opens an edition pays a median 3.4 KB for it. A reader who opens a
 * passage pays for that passage. Shipping 1,241 passages as one document would
 * have made every one of them pay for all of it — the failure the catena
 * measured at 605,923 bytes to render a chapter that held nothing.
 *
 * WHAT MAY BE SHOWN IS NOT DECIDED HERE. The generator applies the rights rule
 * and writes, per passage, either the text's location or the reason there is
 * none. This page renders whichever it is given and has no rule of its own — so
 * a page bug cannot publish a withheld text, because the words were never sent
 * to the browser in the first place.
 * ======================================================================== */

(function () {
  'use strict';

  const T = window.Triptych;
  const M = window.ReaderModel;

  const SPINE = 'structure/sources/index.json';

  const elements = {
    tally: document.getElementById('tally'),
    advisory: document.getElementById('advisory'),
    reading: document.getElementById('reading'),
    controls: document.getElementById('controls'),
    author: document.getElementById('author-select'),
    category: document.getElementById('category-select'),
    language: document.getElementById('language-select'),
    period: document.getElementById('period-select'),
    rights: document.getElementById('rights-select'),
    sort: document.getElementById('sort-select'),
    readable: document.getElementById('readable-input'),
    find: document.getElementById('find-input'),
    finder: document.getElementById('finder'),
    reader: document.getElementById('reader')
  };

  let spine = null;
  let state = M.blank();
  // The edition currently open, its fetched payload, and where in it we are.
  let open = null;

  /* ---------------------------------------------------------------------
   * Labels. Every one of them says what the record says, or says nothing.
   * ------------------------------------------------------------------ */

  function titleOf(work) {
    return work.title || work.id;
  }

  function authorOf(work) {
    return work.author || 'No responsible creator recorded';
  }

  function editionLabel(edition) {
    const parts = [];
    if (edition.date) parts.push(edition.date);
    if (edition.language) parts.push(T.languageName(edition.language));
    parts.push(
      edition.passages === 1 ? '1 passage' : edition.passages + ' passages'
    );
    if (edition.readable > 0) parts.push(edition.readable + ' readable');
    return parts.join(' · ');
  }

  /* ---------------------------------------------------------------------
   * The controls, filled from the facets the generator counted
   * ------------------------------------------------------------------ */

  function fillControls() {
    const facets = spine.facets || {};
    T.fillSelect(elements.author, [{ value: '', label: 'Every author' }].concat(
      (facets.authors || []).map(function (one) {
        return { value: one.id, label: one.id + ' (' + one.works + ')' };
      })
    ));
    T.fillSelect(elements.category, [{ value: '', label: 'Every kind' }].concat(
      (facets.categories || []).map(function (one) {
        return { value: one.id, label: one.id + ' (' + one.works + ')' };
      })
    ));
    T.fillSelect(elements.language, [{ value: '', label: 'Every language' }].concat(
      (facets.languages || []).map(function (one) {
        return {
          value: one.id,
          label: T.languageName(one.id) + ' (' + one.editions + ')'
        };
      })
    ));
    T.fillSelect(elements.period, [{ value: '', label: 'Every period' }].concat(
      (facets.periods || []).map(function (one) {
        return { value: one.id, label: one.label + ' (' + one.editions + ')' };
      })
    ));
    // The rights control is not a curiosity. It is how a reader asks the one
    // question this corpus answers differently from a library catalogue: what
    // may I actually read, and what is only identified for me.
    T.fillSelect(elements.rights, [{ value: '', label: 'Any rights status' }].concat(
      (facets.rights || []).map(function (one) {
        return { value: one.id, label: one.id + ' (' + one.artifacts + ')' };
      })
    ));
    T.fillSelect(elements.sort, [
      { value: 'author', label: 'Author' },
      { value: 'title', label: 'Title' },
      { value: 'date', label: 'Earliest edition' },
      { value: 'readable', label: 'Most readable here' }
    ]);
    elements.readable.disabled = false;
    elements.find.disabled = false;
  }

  function readControls() {
    state = {
      author: elements.author.value,
      category: elements.category.value,
      language: elements.language.value,
      period: elements.period.value,
      rights: elements.rights.value,
      readable: elements.readable.checked,
      find: elements.find.value.trim().toLowerCase(),
      sort: elements.sort.value || 'author'
    };
  }

  function writeControls() {
    elements.author.value = state.author;
    elements.category.value = state.category;
    elements.language.value = state.language;
    elements.period.value = state.period;
    elements.rights.value = state.rights;
    elements.readable.checked = Boolean(state.readable);
    elements.find.value = state.find;
    elements.sort.value = state.sort;
  }

  /* ---------------------------------------------------------------------
   * The finder
   * ------------------------------------------------------------------ */

  function renderFinder() {
    const rows = M.order(M.narrow(spine.works || [], state), state.sort);
    const counted = M.tally(rows);
    elements.tally.textContent =
      counted.works + ' works · ' + counted.editions + ' editions · ' +
      counted.passages + ' passages · ' + counted.readable + ' readable here';

    T.clear(elements.finder);
    if (!rows.length) {
      elements.finder.appendChild(
        T.el('p', 'placeholder',
          'No work in the corpus matches those choices. The corpus holds ' +
          spine.counted.works + ' works in all.')
      );
      T.statusLine('No works match.');
      return;
    }

    for (const row of rows) {
      elements.finder.appendChild(renderWorkCard(row));
    }
    T.statusLine(
      counted.works + ' works, ' + counted.readable + ' passages readable here.'
    );
  }

  function renderWorkCard(row) {
    const work = row.work;
    const card = T.el('article', 'work');
    card.appendChild(T.el('h3', 'work-title', titleOf(work)));
    card.appendChild(T.el('p', 'work-author', authorOf(work)));
    if (work.category) card.appendChild(T.el('p', 'work-kind', work.category));

    // The aliases, shown rather than merely searchable. A reader who knows this
    // work as the City of God should see that name on the card that calls it
    // De civitate Dei, instead of doubting they have found the right thing.
    if ((work.alternate_titles || []).length) {
      card.appendChild(
        T.el('p', 'work-aliases', 'Also: ' + work.alternate_titles.join(' · '))
      );
    }

    const list = T.el('ul', 'edition-list');
    for (const edition of row.editions) {
      const item = T.el('li', 'edition');
      const button = T.el('button', 'edition-open', editionLabel(edition));
      button.type = 'button';
      button.addEventListener('click', function () {
        openEdition(work, edition, null);
      });
      item.appendChild(button);
      if (!edition.readable) {
        item.appendChild(
          T.el('span', 'edition-withheld', 'no text readable here')
        );
      }
      list.appendChild(item);
    }
    card.appendChild(list);
    return card;
  }

  /* ---------------------------------------------------------------------
   * The reader
   * ------------------------------------------------------------------ */

  async function openEdition(work, edition, wantedPassage) {
    const path = M.editionPath(spine, work, edition);
    if (!path) {
      T.fail('The index records no file for ' + edition.id + '.');
      return;
    }
    const token = T.beginRender();
    showReader();
    T.clear(elements.reader);
    elements.reader.appendChild(T.el('p', 'placeholder', 'Loading the edition…'));

    let payload;
    try {
      payload = await T.loadJSON(path);
    } catch (error) {
      if (!T.isCurrentRender(token)) return;
      T.clear(elements.reader);
      elements.reader.appendChild(
        T.el('p', 'error',
          'This edition could not be loaded: ' + (error.message || error))
      );
      return;
    }
    if (!T.isCurrentRender(token)) return;

    const at = wantedPassage
      ? Math.max(0, (payload.passages || []).findIndex(function (one) {
          return one.id === wantedPassage;
        }))
      : 0;
    open = { work: work, edition: edition, payload: payload, at: at };
    renderReader();
  }

  function showReader() {
    elements.finder.hidden = true;
    elements.controls.hidden = true;
    elements.reader.hidden = false;
  }

  function showFinder() {
    open = null;
    elements.reader.hidden = true;
    elements.controls.hidden = false;
    elements.finder.hidden = false;
    writeHash();
    renderFinder();
  }

  function renderReader() {
    const payload = open.payload;
    const work = payload.work || {};
    const edition = payload.edition || {};
    const passages = payload.passages || [];

    T.clear(elements.reader);

    const back = T.el('button', 'back', '← Back to the corpus');
    back.type = 'button';
    back.addEventListener('click', showFinder);
    elements.reader.appendChild(back);

    const head = T.el('header', 'reader-head');
    head.appendChild(T.el('h2', 'reader-title', work.title || work.id));
    head.appendChild(T.el('p', 'reader-author', authorOf(work)));
    head.appendChild(T.el('p', 'reader-edition', edition.title || edition.id));
    const facts = [];
    if (edition.date) facts.push(edition.date);
    if (edition.language) facts.push(T.languageName(edition.language));
    if ((edition.translators || []).length) {
      facts.push('tr. ' + edition.translators.join(', '));
    }
    if ((edition.editors || []).length) {
      facts.push('ed. ' + edition.editors.join(', '));
    }
    if (facts.length) head.appendChild(T.el('p', 'reader-facts', facts.join(' · ')));
    if (edition.publication) {
      head.appendChild(T.el('p', 'reader-publication', edition.publication));
    }
    elements.reader.appendChild(head);

    if (!passages.length) {
      elements.reader.appendChild(
        T.el('p', 'placeholder',
          'This edition is identified and its artifacts are recorded, but no ' +
          'passage of it has been addressed yet. There is nothing to step ' +
          'through.')
      );
      renderApparatus();
      return;
    }

    elements.reader.appendChild(renderNavigation(passages));
    const body = T.el('div', 'passage-body');
    body.id = 'passage-body';
    elements.reader.appendChild(body);
    renderPassage();
    renderApparatus();
  }

  function renderNavigation(passages) {
    const bar = T.el('nav', 'passage-nav');
    bar.setAttribute('aria-label', 'Passages of this edition');

    const previous = T.el('button', 'step', '‹ Previous');
    previous.type = 'button';
    previous.disabled = open.at <= 0;
    previous.addEventListener('click', function () { step(-1); });
    bar.appendChild(previous);

    const field = T.el('div', 'field');
    const label = T.el('label', null, 'Passage');
    label.setAttribute('for', 'passage-select');
    const select = T.el('select');
    select.id = 'passage-select';
    T.fillSelect(select, passages.map(function (one, index) {
      // The dropdown states, on every row, whether that passage can be read.
      // A reader choosing where to go next is owed that before they go, not
      // after — otherwise the control promises text it will not deliver.
      const mark = one.readable ? one.words + ' words' : 'not shown here';
      return {
        value: String(index),
        label: (index + 1) + '. ' + (one.locus || one.id) + ' — ' + mark
      };
    }));
    select.value = String(open.at);
    select.addEventListener('change', function () {
      open.at = Number(select.value) || 0;
      writeHash();
      renderPassage();
      refreshNavigation();
    });
    field.appendChild(label);
    field.appendChild(select);
    bar.appendChild(field);

    const next = T.el('button', 'step', 'Next ›');
    next.type = 'button';
    next.disabled = open.at >= passages.length - 1;
    next.addEventListener('click', function () { step(1); });
    bar.appendChild(next);

    bar.appendChild(
      T.el('p', 'passage-count',
        'Passage ' + (open.at + 1) + ' of ' + passages.length)
    );
    return bar;
  }

  function refreshNavigation() {
    const bar = elements.reader.querySelector('.passage-nav');
    if (!bar) return;
    const replacement = renderNavigation(open.payload.passages || []);
    bar.parentNode.replaceChild(replacement, bar);
  }

  function step(by) {
    const passages = open.payload.passages || [];
    const next = open.at + by;
    if (next < 0 || next >= passages.length) return;
    open.at = next;
    writeHash();
    renderPassage();
    refreshNavigation();
  }

  async function renderPassage() {
    const body = document.getElementById('passage-body');
    if (!body) return;
    const passage = (open.payload.passages || [])[open.at];
    if (!passage) return;

    T.clear(body);
    const head = T.el('div', 'passage-head');
    head.appendChild(T.el('h3', 'passage-locus', passage.locus || passage.id));
    if ((passage.states || []).length) {
      head.appendChild(
        T.el('span', 'passage-states', passage.states.join(' · '))
      );
    }
    body.appendChild(head);

    // The editorial note on this passage: what was read, and how far the
    // reading went. It belongs above the text because it bounds it.
    if (passage.context) {
      body.appendChild(T.el('p', 'passage-context', passage.context));
    }

    if (!passage.readable) {
      // ABSENCE WITH ITS REASON. Never a blank, never a quiet omission. The
      // record is here, named, dated and bounded; what is missing is the
      // permission or the bytes, and the reader is told which.
      body.appendChild(T.notice(passage.reason));
      body.appendChild(renderProvenance(passage));
      if (passage.notes) body.appendChild(T.el('p', 'passage-notes', passage.notes));
      T.statusLine((passage.locus || 'This passage') + ' is not shown here.');
      return;
    }

    const token = T.beginRender();
    body.appendChild(T.el('p', 'placeholder', 'Loading ' + passage.words + ' words…'));
    let text;
    try {
      text = await T.loadJSON(passage.text_path);
    } catch (error) {
      if (!T.isCurrentRender(token)) return;
      body.removeChild(body.lastChild);
      body.appendChild(
        T.notice('the text of this passage could not be loaded: ' +
          (error.message || error))
      );
      return;
    }
    if (!T.isCurrentRender(token)) return;
    body.removeChild(body.lastChild);

    // A licensed text carries its licence at the point of use, ABOVE the words
    // and not in a page footer, because a reader who copies the passage out has
    // to carry the condition with it. A footer does not travel with a
    // selection; this does.
    if (passage.acknowledgement) {
      const note = T.el('p', 'acknowledgement');
      note.appendChild(T.el('strong', null, 'Licence: '));
      note.appendChild(document.createTextNode(passage.acknowledgement));
      body.appendChild(note);
    }

    const prose = T.el('div', 'passage-text');
    prose.lang = text.language || open.payload.edition.language || 'en';
    // The transcription is set paragraph by paragraph on its own line breaks.
    // Raw physical lines from an OCR artifact keep their line structure,
    // hyphenation and all, because normalising them here would present a
    // corrected text as though the artifact carried it.
    for (const paragraph of String(text.text || '').split(/\n\s*\n/)) {
      if (!paragraph.trim()) continue;
      const block = T.el('p', 'passage-paragraph');
      for (const [index, line] of paragraph.split('\n').entries()) {
        if (index) block.appendChild(T.el('br'));
        block.appendChild(document.createTextNode(line));
      }
      prose.appendChild(block);
    }
    body.appendChild(prose);

    body.appendChild(renderProvenance(passage));
    if (passage.notes) body.appendChild(T.el('p', 'passage-notes', passage.notes));
    T.statusLine(
      (passage.locus || 'Passage') + ', ' + passage.words + ' words, now shown.'
    );
  }

  /** Whose bytes these are, and under what. Shown for a text and for a refusal
   *  alike: the reader weighing a refusal needs the same facts as the reader
   *  weighing a text. */
  function renderProvenance(passage) {
    const source = T.el('p', 'passage-source');
    const parts = [];
    if (passage.artifact_type) parts.push(passage.artifact_type);
    if (passage.rights) parts.push(passage.rights);
    if (passage.rights_jurisdiction) parts.push(passage.rights_jurisdiction);
    if (passage.storage) parts.push('stored ' + passage.storage);
    source.appendChild(T.el('span', 'source-facts', parts.join(' · ')));
    if (passage.rights_basis && !passage.acknowledgement) {
      source.appendChild(T.el('span', 'source-basis', passage.rights_basis));
    }
    if (passage.segment_id) {
      source.appendChild(
        T.el('span', 'source-segment',
          'Witnessed inside a container artifact, through segment ' +
          passage.segment_id + '.')
      );
    }
    if (passage.source_url) {
      const link = T.el('a', 'source-url', passage.source_url);
      link.href = passage.source_url;
      link.rel = 'noreferrer';
      source.appendChild(link);
    }
    return source;
  }

  /** The edition's artifacts, under the reading, where they explain it. */
  function renderApparatus() {
    const artifacts = open.payload.artifacts || [];
    if (!artifacts.length) return;
    const section = T.el('details', 'apparatus');
    section.appendChild(
      T.el('summary', null,
        artifacts.length === 1
          ? 'The one artifact behind this edition'
          : 'The ' + artifacts.length + ' artifacts behind this edition')
    );
    const list = T.el('ul', 'artifact-list');
    for (const artifact of artifacts) {
      const item = T.el('li', 'artifact');
      item.appendChild(T.el('span', 'artifact-type', artifact.artifact_type || ''));
      item.appendChild(T.el('span', 'artifact-rights', artifact.rights || ''));
      item.appendChild(T.el('span', 'artifact-storage', 'stored ' + artifact.storage));
      if (artifact.rights_basis) {
        item.appendChild(T.el('span', 'artifact-basis', artifact.rights_basis));
      }
      list.appendChild(item);
    }
    section.appendChild(list);
    elements.reader.appendChild(section);

    const work = open.payload.work || {};
    if (work.description) {
      const about = T.el('details', 'apparatus');
      about.appendChild(T.el('summary', null, 'About this work'));
      about.appendChild(T.el('p', null, work.description));
      elements.reader.appendChild(about);
    }
  }

  /* ---------------------------------------------------------------------
   * URL state, and the link that arrives from Catena Omnia
   * ------------------------------------------------------------------ */

  function writeHash() {
    if (open) {
      const passage = (open.payload.passages || [])[open.at];
      T.writeHash([
        ['edition', open.edition.id],
        ['passage', passage ? passage.id : '']
      ]);
      return;
    }
    T.writeHash([
      ['author', state.author],
      ['category', state.category],
      ['language', state.language],
      ['period', state.period],
      ['rights', state.rights],
      ['readable', state.readable ? '1' : ''],
      ['find', state.find],
      ['sort', state.sort === 'author' ? '' : state.sort]
    ]);
  }

  /**
   * Follow a link that names a passage and nothing else.
   *
   * This is the edge Catena Omnia links across: a fragment there knows its
   * passage id and nothing about this page's layout. The route is written by
   * the generator into the passage's own text file — the edition it belongs to
   * and where that edition's file is — so the id is LOOKED UP rather than taken
   * apart. Deriving an edition from the shape of a passage id would make a
   * renamed record a broken link that nothing notices.
   */
  async function followPassage(passageId) {
    let pointer;
    try {
      pointer = await T.loadJSON((spine.texts || '') + passageId + '.json');
    } catch (error) {
      return null;
    }
    for (const work of spine.works || []) {
      if (work.id !== pointer.work_id) continue;
      for (const edition of work.editions || []) {
        if (edition.id === pointer.edition_id) return { work: work, edition: edition };
      }
    }
    return null;
  }

  async function applyHash(hash) {
    const editionId = hash.get('edition');
    const passageId = hash.get('passage');

    if (editionId) {
      for (const work of spine.works || []) {
        for (const edition of work.editions || []) {
          if (edition.id === editionId) {
            await openEdition(work, edition, passageId);
            return;
          }
        }
      }
    }
    if (passageId) {
      const found = await followPassage(passageId);
      if (found) {
        await openEdition(found.work, found.edition, passageId);
        return;
      }
      // A passage the corpus does not offer here. Said plainly, with the
      // corpus still reachable, rather than dropping the reader on a list with
      // no explanation of why the link did not work.
      showReader();
      T.clear(elements.reader);
      const back = T.el('button', 'back', '← Back to the corpus');
      back.type = 'button';
      back.addEventListener('click', showFinder);
      elements.reader.appendChild(back);
      elements.reader.appendChild(
        T.el('p', 'error',
          'No passage with the id “' + passageId + '” can be opened here. It may ' +
          'be a record whose text this repository may not serve, in which case ' +
          'it is findable in the corpus below under its own work.')
      );
      return;
    }

    state = {
      author: hash.get('author') || '',
      category: hash.get('category') || '',
      language: hash.get('language') || '',
      period: hash.get('period') || '',
      rights: hash.get('rights') || '',
      readable: hash.get('readable') === '1',
      find: (hash.get('find') || '').toLowerCase(),
      sort: hash.get('sort') || 'author'
    };
    writeControls();
    elements.reader.hidden = true;
    elements.controls.hidden = false;
    elements.finder.hidden = false;
    renderFinder();
  }

  /* ---------------------------------------------------------------------
   * Start
   * ------------------------------------------------------------------ */

  async function start() {
    T.setInlineNotice(
      'The source corpus could not be reached, so this page has nothing to ' +
      'show. Serve the pages over HTTP with the data at "' + T.dataRoot + '".'
    );
    try {
      spine = await T.loadJSON(SPINE);
    } catch (error) {
      T.doneBootstrapping();
      T.fail('The source corpus could not be loaded: ' + (error.message || error));
      return;
    }
    T.doneBootstrapping();

    elements.advisory.textContent = spine.advisory || '';
    fillControls();
    writeControls();

    for (const control of [
      elements.author, elements.category, elements.language,
      elements.period, elements.rights, elements.sort
    ]) {
      control.addEventListener('change', function () {
        readControls();
        writeHash();
        renderFinder();
      });
    }
    elements.readable.addEventListener('change', function () {
      readControls();
      writeHash();
      renderFinder();
    });
    elements.find.addEventListener('input', function () {
      readControls();
      writeHash();
      renderFinder();
    });

    // Arrow keys step through the passages of an open edition, and do nothing
    // in the finder, where there is no sequence to step through.
    T.onArrowStep(function (by) {
      if (open) step(by);
    });
    T.onHashChange(function (hash) { applyHash(hash); });

    elements.reading.setAttribute('aria-busy', 'false');
    await applyHash(T.readHash());
  }

  start();
}());
