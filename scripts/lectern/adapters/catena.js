'use strict';
/*
 * Catena Omnia, as `src/web/browser/catena/catena.js` assembles it.
 *
 * Every value below is a return of `catena-model.js` or `browser-core.js`,
 * called in the order catena.js calls them, except the few sentences marked
 * `page:` — prose that lives in catena.js itself and is repeated here with its
 * line so the terminal says what the page says. The model keeps the dated
 * chain's order and sets explicitly undated commentary apart in both readers.
 */
module.exports = function catena(realm) {
  realm.script('shared/browser-core.js');
  realm.script('catena/catena-model.js');
  const T = globalThis.Triptych;
  const M = globalThis.CatenaModel;
  M.useLanguageNames(T.languageName); // catena.js:18

  /* The page's per-path cache (catena.js:70): the model keys its projections
   * on the file object, so a chapter must be the same object each time it is
   * asked about, or a fragment's text could not be matched to its row. */
  const files = new Map();
  const ABSENT = { absent: true };
  function cached(where, absent) {
    if (!files.has(where)) {
      files.set(where, T.loadJSON(where).then((file) => file, (error) => {
        if (error instanceof T.NotFound && absent !== undefined) return absent;
        files.delete(where);
        throw error;
      }));
    }
    return files.get(where);
  }
  const gone = new Map();
  function unfetched(where) { // catena.js:86
    if (!gone.has(where)) gone.set(where, { unfetched: where });
    return gone.get(where);
  }

  let started = null;
  function start() { // catena.js:920
    if (!started) {
      started = Promise.all([
        T.loadJSON('structure/catena/index.json'),
        T.loadBibles(),
        cached('structure/paragraphs/index.json', ABSENT).then(
          (file) => (file === ABSENT ? undefined : file), () => 'unreadable'),
      ]).then(([index, manifest, paragraphs]) => {
        index = M.bag(index);
        if (!manifest.ok) throw new Error(manifest.message);
        const editions = M.bibleRoot(manifest.bibles);
        const canon = M.canonRoot(index.canon);
        const voices = M.voiceRoot(index);
        if (!canon.books.length) throw new Error('The catena index could not be read.');
        if (!editions.bibles.length) throw new Error('The published editions could not be read.');
        return { index, editions, canon, voices, paragraphs };
      });
      started.catch(() => { started = null; });
    }
    return started;
  }

  async function opening() {
    const { index, editions, canon, voices } = await start();
    const held = new Map(M.records(index.held).map((one) => [one.token, one]));
    return {
      numbering: index.numbering,
      books: canon.books.map((book) => {
        const record = held.get(book.token) || {};
        return {
          token: book.token, name: book.name, chapters: book.chapters,
          testament: book.testamentName, fragments: record.fragments || 0,
          present: (record.present || []).length,
        };
      }),
      bibles: editions.bibles.map((one) => ({
        id: one.id, label: one.label, language: one.language, numbering: one.numbering,
      })),
      voices: voices.keys,
    };
  }

  async function chapterFile(token, chapter) {
    const { index } = await start();
    const where = M.chapterPath(index, token, chapter);
    if (!where) return { where, file: where === null ? unfetched('the index record') : null };
    const file = await cached(where, unfetched(where));
    return { where, file: M.spineUnreadable(file) ? unfetched(where) : file };
  }

  async function address(token, chapter, bible, voice) {
    const state = await start();
    const hash = new URLSearchParams();
    hash.set('book', token);
    hash.set('chapter', String(chapter));
    if (bible) hash.set('bible', bible);
    if (voice) hash.set('voice', voice);
    return { state, problems: M.addressProblems(hash, state.canon, state.editions, state.voices) };
  }

  async function view(token, chapter, bibleId, voice) {
    const { state, problems } = await address(token, chapter, bibleId, voice);
    if (problems.length) {
      return { problems, heading: 'This address cannot be used as written' }; // catena.js:626
    }
    const { canon, editions, paragraphs } = state;
    const bibles = editions.bibles;
    const bible = bibles.find((one) => one.id === (bibleId || bibles[0].id));
    const book = canon.books.find((one) => one.token === M.sound(token));
    voice = voice || '';

    const [{ where, file }, reading] = await Promise.all([
      chapterFile(token, chapter),
      M.readScripture(state.index, token, chapter, bible, {
        file: (path) => cached(path),
        chapter: (nativeBook, number) => T.loadChapter(bible.id, nativeBook, number),
        paragraphs: (nativeBook, number) => {
          const native = canon.books.find((one) => one.token === nativeBook);
          const path = M.paragraphPath(paragraphs, bible.id, M.bag(native).path, number);
          return path === null ? Promise.resolve({ unfetched: true })
            : path ? cached(path, ABSENT).then(
              (file) => (file === ABSENT ? undefined : file), () => ({ unfetched: true }))
              : Promise.resolve(undefined);
        },
        pick: (citation) => T.editionLoci(citation, bible),
        recast: (citation, picked) => T.recastLoci(citation, bible, state.index.numbering, picked),
        format: T.formatLoci,
      })]);

    const missing = M.chapterUnfetched(file);
    const blocked = M.chapterBlocked(file);
    const leads = M.chapterLeads(file);
    const total = M.chapterTally(file);
    const held = M.chapterVoices(file);

    const voiceOptions = [{ value: '', label: 'Everything held' }] // catena.js:797
      .concat(held.map((entry) => ({ value: entry.key, label: M.voiceLabel(entry) })));
    if (voice && !held.some((one) => one.key === voice)) {
      voiceOptions.push({ value: voice,
        label: M.voiceLabel(M.parseVoiceKey(voice)) + ((missing || blocked.length) ? '' : ' — none here') });
    }

    const refused = M.refusalNote(file, bible.id, chapter);
    const refusal = refused ? ( // page: catena.js:610-624
      'Boundary not established. ' + refused + ' Commentary on ' + book.name + ' ' + chapter +
      ' is anchored in Vulgate numbering, and this page will not guess where the boundary moves to in ' +
      bible.label + '. The commentary keeps its canonical address.'
    ) : '';

    let scripture;
    if (!reading.ok) {
      scripture = { ok: false, problem: reading.problem };
    } else {
      const sections = reading.parts.map((part) => {
        const read = M.chapterReading(part.verses, part.marks);
        let current = null;
        const paragraphsOut = [];
        for (const line of read.lines) {
          if (!current || line.kind) {
            current = { kind: line.kind || '', verses: [] };
            paragraphsOut.push(current);
          }
          current.verses.push({ number: line.number, text: line.text });
        }
        return { label: part.label, verseCount: read.lines.length,
          paragraphs: paragraphsOut, note: M.paragraphNote(read) };
      });
      scripture = {
        ok: true, verseCount: sections.reduce((sum, part) => sum + part.verseCount, 0),
        sections, note: reading.note,
      };
    }

    let chain = null;
    if (!missing) { // catena.js:425
      const all = M.chapterFragments(file);
      const shown = all.filter((one) => M.matchesVoice(one, voice));
      const heading = shown.length === 0 ? 'Commentary held here'
        : shown.length === 1 ? 'One fragment held here' : shown.length + ' fragments held here';
      const notes = [];
      if (!shown.length) notes.push(M.emptyChainNote(all.length, blocked.length, voice, held));
      else if (voice) {
        const said = M.otherVoicesNote(voice, held.filter((one) => one.key !== voice));
        if (said) notes.push(said);
      }
      let absences = null; // catena.js:389, only under a translation voice
      const asked = M.parseVoiceKey(voice);
      if (asked && asked.voice === M.TRANSLATION) {
        const rows = M.absenceRows(index(state), file, asked.language);
        absences = rows.length
          ? { summary: M.absenceSummary(rows, M.sayLanguage(asked.language)), rows }
          : { unread: M.absencesUnread(index(state)), rows: [] };
      }
      const fragments = M.commentaryGroups(shown).flatMap((group) => group.fragments).map((row) => ({
        id: row.id, author: row.author, work: row.work, date: row.date,
        ...M.compositionDateMetadata(row),
        language: row.language, voice: row.voice, text_words: row.text_words,
        locator: row.locator, edition: row.edition, edition_published: row.edition_published,
        translators: row.translators, rights: row.rights, attribution: row.attribution,
        rights_basis: row.rights_basis, review: row.review, text_refused: row.text_refused,
        text_note: row.text_note,
        extent: M.formatExtent(row.extent, book.name),
        spans: M.spansChapters(row.extent),
        chip: M.languageChip(row),
        reviewNote: row.review && row.review !== 'verified' ? row.review + ', not collated' : '', // catena.js:369
      }));
      chain = { heading, notes, total: all.length, shown: shown.length, absences, fragments };
    }

    const summary = M.chapterSummary({ total, shown: chain ? chain.shown : 0,
      blocked: blocked.length, leads: leads.length, unfetched: !!missing, voice });

    return {
      problems: [],
      reference: book.name + ' ' + chapter,
      testament: book.testamentName,
      book: { token: book.token, name: book.name, chapters: book.chapters },
      chapter,
      bible: { id: bible.id, label: bible.label, language: bible.language, numbering: bible.numbering },
      voice,
      voices: voiceOptions,
      held: !!where,
      tally: summary,
      refusal,
      scripture,
      chain,
      leads,
      blocked,
      unfetched: missing ? 'The index records commentary on ' + book.name + ' ' + chapter + // catena.js:713
        ', but its record (' + missing + ') could not be read — a data or connection fault, not an empty chapter.' : '',
    };
  }

  function index(state) { return state.index; }

  async function body(token, chapter, voice, id) { // catena.js:119, :298
    const { file } = await chapterFile(token, chapter);
    const row = M.chapterFragments(file).find((one) => one.id === id);
    if (!row) throw new Error('no fragment ' + id + ' stands under this chapter');
    if (row.text_refused) return { missing: true, said: row.text_note };
    const where = M.textAsked(row);
    const owner = M.rowTransport(row);
    if (!owner) return { missing: true, said: 'This fragment cannot be opened.' };
    let completed;
    if (!where) completed = M.textCompleted(owner, M.NO_TEXT);
    else {
      try {
        completed = M.textCompleted(owner, M.textPayload(await T.loadJSON(where)));
      } catch (error) {
        completed = M.textFailed(owner, error);
      }
    }
    if (!M.bodyAsked(row, completed)) return { missing: true, said: 'This fragment cannot be opened.' };
    if (completed.failed) {
      return { missing: true, said: M.failureSaid(completed.error instanceof T.NotFound, completed.error) };
    }
    const content = completed.content;
    const say = M.bodySaying(content);
    return {
      missing: say.missing,
      said: say.said,
      basis: say.missing ? '' : content.basis,
      date_basis: say.missing ? '' : content.date_basis,
      acknowledgement: content.present ? content.acknowledgement : '',
      acknowledgement_broken: content.present ? content.acknowledgement_broken : false,
    };
  }

  /* Per-chapter counts for a book: the model's tally of each chapter's own
   * file. A fragment spanning two chapters counts in both (guidance/catena.md
   * Rule 6), so these do not sum to the book's total. */
  async function density(token) {
    const { canon, editions } = await start();
    const book = canon.books.find((one) => one.token === M.sound(token));
    if (!book) throw new Error('no book ' + token);
    const ids = editions.bibles.map((one) => one.id);
    const rows = [];
    for (let chapter = 1; chapter <= book.chapters; chapter += 1) {
      const { where, file } = await chapterFile(book.token, chapter);
      const row = { chapter, held: !!where, fragments: 0, leads: 0, blocked: 0, refused: 0, unreadable: false };
      if (where === null) row.unreadable = true;
      if (where) {
        row.unreadable = !!M.chapterUnfetched(file);
        row.fragments = M.chapterTally(file);
        row.leads = M.chapterLeads(file).length;
        row.blocked = M.chapterBlocked(file).length;
        row.refused = ids.filter((id) => M.refusalNote(file, id, chapter)).length;
      }
      rows.push(row);
    }
    return rows;
  }

  return { opening, view, body, density };
};
