'use strict';
/*
 * The Source Library, as `src/web/browser/sources/sources.js` assembles it.
 *
 * Three published layers, and the reader pays for what it opens (sources.js:9-23):
 *
 *   structure/sources/index.json   every work and edition, enough to search on;
 *   root + work.directory + file   one edition: its artifacts and every passage
 *                                  with its locus and its rights decision, no words;
 *   a passage's own text_path      one readable passage's words.
 *
 * Which editions a choice leaves, the order, the tally, an edition's file and
 * the edition a work opens on are `reader-model.js`'s answers, asked as
 * sources.js asks them. What may be shown is decided by the generator, never
 * here: a withheld passage arrives with its reason and without its words, and
 * nothing in this file reads an artifact from disk. The sentences marked
 * `page:` are the page's own prose, repeated with the line they come from.
 *
 * Works and editions are addressed by their position in the spine's arrays,
 * so the Python side holds the rows once and is told, per choice, which
 * survive and in what order. A citation from elsewhere (a passage id from
 * Catena Omnia, an edition id) is looked up exactly as the page looks it up,
 * and a miss is refused with the id quoted: it is never rounded to passage one.
 */
module.exports = function sources(realm) {
  realm.script('shared/browser-core.js');
  realm.script('sources/reader-model.js');
  const T = globalThis.Triptych;
  const M = globalThis.ReaderModel;
  const SPINE = 'structure/sources/index.json'; // sources.js:38

  let loading = null;
  function spine() {
    if (!loading) {
      loading = T.loadJSON(SPINE).then((file) => {
        const editions = new Map();
        (file.works || []).forEach((work, at) => (work.editions || []).forEach((edition, index) => {
          editions.set(edition.id, [at, index]);
        }));
        const position = new Map();
        (file.works || []).forEach((work, at) => position.set(work, at));
        return { file, editions, position };
      });
      loading.catch(() => { loading = null; });
    }
    return loading;
  }

  /* The page fetches an edition's file each time it is opened. Stepping from
   * passage to passage asks for the same one again, so the last few are kept
   * as fetched, unaltered. */
  const payloads = new Map();
  function payload(where) {
    if (payloads.has(where)) {
      const held = payloads.get(where);
      payloads.delete(where);
      payloads.set(where, held);
      return held;
    }
    const asked = T.loadJSON(where);
    payloads.set(where, asked);
    asked.catch(() => payloads.delete(where));
    while (payloads.size > 12) payloads.delete(payloads.keys().next().value);
    return asked;
  }

  function titleOf(work) { return work.title || work.id; } // sources.js:66-68
  function authorOf(work) { return work.author || 'No responsible creator recorded'; } // sources.js:70-72

  /* The page's one label (sources.js:74-86), kept in its two halves so a
   * narrow list can set the title on one line and the facts on the next. */
  function editionLabel(edition) {
    const parts = [];
    if (edition.date) parts.push(edition.date);
    if (edition.language) parts.push(T.languageName(edition.language));
    parts.push(edition.passages === 1 ? '1 passage' : edition.passages + ' passages');
    if (edition.readable > 0) parts.push(edition.readable + ' readable');
    return { title: edition.title || edition.id, facts: parts.join(' · ') };
  }

  function state(asked) { // sources.js:139-150
    asked = asked || {};
    return Object.assign(M.blank(), {
      author: asked.author || M.ANY,
      category: asked.category || M.ANY,
      language: asked.language || M.ANY,
      period: asked.period || M.ANY,
      rights: asked.rights || M.ANY,
      readable: Boolean(asked.readable),
      find: String(asked.find || '').trim().toLowerCase(),
      sort: asked.sort || 'author',
    });
  }

  async function opening() {
    const { file } = await spine();
    const facets = file.facets || {};
    return {
      schema: file.schema,
      advisory: file.advisory || '', // sources/index.html:122-126, written from the file
      counted: file.counted || {},
      controls: { // sources.js:92-137
        author: [{ value: '', label: 'Every author' }].concat((facets.authors || []).map(
          (one) => ({ value: one.id, label: one.id + ' (' + one.works + ')' }))),
        category: [{ value: '', label: 'Every kind' }].concat((facets.categories || []).map(
          (one) => ({ value: one.id, label: one.id + ' (' + one.works + ')' }))),
        language: [{ value: '', label: 'Every language' }].concat((facets.languages || []).map(
          (one) => ({ value: one.id, label: T.languageName(one.id) + ' (' + one.editions + ')' }))),
        period: [{ value: '', label: 'Every period' }].concat((facets.periods || []).map(
          (one) => ({ value: one.id, label: one.label + ' (' + one.editions + ')' }))),
        rights: [{ value: '', label: 'Any rights status' }].concat((facets.rights || []).map(
          (one) => ({ value: one.id, label: one.id + ' (' + one.artifacts + ' artifacts · ' + one.editions + ' editions)' }))),
        sort: [
          { value: 'author', label: 'Author' },
          { value: 'title', label: 'Title' },
          { value: 'date', label: 'Earliest edition' },
          { value: 'readable', label: 'Readable passage count' },
        ],
      },
      rights: (facets.rights || []).map((one) => ({ id: one.id, artifacts: one.artifacts, editions: one.editions })),
      // page: sources/index.html:101-121, the page's own account of what it lists
      glossary: [
        'A work is the intellectual thing — a treatise, a homily, a decree. An edition is one materially ' +
        'identified form of it whose wording or authority can differ from another\'s, so a Greek original, ' +
        'Migne\'s Latin and a public-domain English translation are three editions and never one work with ' +
        'three texts. An artifact is the exact bytes that were acquired, with their hash and their rights. ' +
        'A segment identifies a bounded part of a container artifact. A passage is an addressable place in an ' +
        'edition and names one controlling artifact; where it also names a segment, that segment narrows the ' +
        'artifact rather than replacing it. Nothing here flattens those five into one.',
        'Rights are read from the records, never from the disk. A passage is set here only where the artifact ' +
        'controlling it records an affirmative distribution basis and is stored in the repository. A passage ' +
        'that fails that test — because it is under copyright, its rights have never been settled, or the ' +
        'permitted bytes are not stored here — is listed with the reason rather than quietly dropped. A record ' +
        'you cannot read here is still a record you can find, cite and follow to its source.',
      ],
      works: (file.works || []).map((work) => ({
        id: work.id,
        title: titleOf(work),
        author: authorOf(work),
        authorRecorded: Boolean(work.author),
        category: work.category || '',
        also: (work.alternate_titles || []).length ? 'Also: ' + work.alternate_titles.join(' · ') : '', // sources.js:203-207
        editions: (work.editions || []).map((edition) => ({
          id: edition.id,
          title: editionLabel(edition).title,
          facts: editionLabel(edition).facts,
          passages: edition.passages || 0,
          readable: edition.readable || 0,
          withheld: edition.readable ? '' : 'no text readable here', // sources.js:218-222
        })),
      })),
    };
  }

  /* The finder (sources.js:167-191), as positions. */
  async function find(asked) {
    const { file, position } = await spine();
    const chosen = state(asked);
    const rows = M.order(M.narrow(file.works || [], chosen), chosen.sort);
    const counted = M.tally(rows);
    return {
      state: chosen,
      rows: rows.map((row) => [position.get(row.work), row.editions.map((one) => row.work.editions.indexOf(one))]),
      counted,
      tally: counted.works + ' works · ' + counted.editions + ' editions · ' + // page: sources.js:171-172
        counted.passages + ' passages · ' + counted.readable + ' readable here',
      zero: rows.length ? '' : 'No work in the corpus matches those choices. The corpus holds ' + // sources.js:178-179
        file.counted.works + ' works in all.',
    };
  }

  async function opened(workAt, editionAt) {
    const { file } = await spine();
    const work = (file.works || [])[workAt];
    const edition = work && (work.editions || [])[editionAt];
    if (!edition) throw new Error('no edition at ' + workAt + '/' + editionAt + ' in the spine');
    const where = M.editionPath(file, work, edition);
    if (!where) return { work, edition, problem: 'The index records no file for ' + edition.id + '.' }; // sources.js:239
    try {
      return { work, edition, where, payload: await payload(where) };
    } catch (error) {
      return { work, edition, where, problem: 'This edition could not be loaded: ' + (error.message || error) }; // sources.js:258
    }
  }

  /* The reader's head, selector and apparatus (sources.js:303-408, 581-631). */
  async function edition(workAt, editionAt) {
    const found = await opened(workAt, editionAt);
    const indexed = found.edition;
    const base = {
      at: [workAt, editionAt], id: indexed.id, where: found.where || '',
      passagesIndexed: indexed.passages || 0, readableIndexed: indexed.readable || 0,
    };
    if (found.problem) return Object.assign(base, { problem: found.problem });
    const data = found.payload;
    const work = data.work || {};
    const record = data.edition || {};
    const passages = data.passages || [];
    const facts = [];
    if (record.date) facts.push(record.date);
    if (record.language) facts.push(T.languageName(record.language));
    if ((record.translators || []).length) facts.push('tr. ' + record.translators.join(', '));
    if ((record.editors || []).length) facts.push('ed. ' + record.editors.join(', '));

    /* Why the passages not shown are not shown: the generator's own reason on
     * each, counted as written. The reasons are its words, not this file's. */
    const reasons = [];
    for (const one of passages) {
      if (one.readable) continue;
      const known = reasons.find((row) => row.code === one.withheld && row.reason === one.reason);
      if (known) known.count += 1;
      else reasons.push({ code: one.withheld || '', reason: one.reason || '', count: 1 });
    }
    const artifacts = data.artifacts || [];
    return Object.assign(base, {
      head: {
        title: work.title || work.id,
        author: authorOf(work),
        edition: record.title || record.id,
        facts: facts.join(' · '),
        publication: record.publication || '',
      },
      // page: sources.js:338-339
      empty: passages.length ? '' : 'This edition is identified, but no passage of it has been addressed ' +
        'yet. There is nothing to step through.',
      passages: passages.map((one, index) => ({ // sources.js:371-380, the label in its parts
        id: one.id,
        number: (index + 1) + '. ',
        locus: one.locus || one.id,
        mark: one.readable ? one.words + ' words' : 'not shown here',
        readable: Boolean(one.readable),
      })),
      reasons,
      artifactsSummary: artifacts.length === 1 ? 'The one source artifact for this edition' // sources.js:588-590
        : 'The ' + artifacts.length + ' source artifacts for this edition',
      artifacts: artifacts.map((one) => ({ // sources.js:593-618
        id: one.id || '',
        idSaid: one.id || 'No artifact id recorded',
        relationship: one.edition_owned ? 'Owned by this edition'
          : 'Controls a passage in this edition; owned by another edition',
        type: one.artifact_type || '',
        rights: one.rights || '',
        storage: 'stored ' + one.storage,
        basis: one.rights_basis || '',
      })),
      about: work.description || '',
      authority: record.authority || '',
      jurisdiction: record.jurisdiction || '',
    });
  }

  /* One passage, as renderPassage sets it (sources.js:448-579). */
  async function passage(workAt, editionAt, at) {
    const found = await opened(workAt, editionAt);
    if (found.problem) throw new Error(found.problem);
    const passages = found.payload.passages || [];
    const one = passages[at];
    if (!one) throw new Error('This edition holds no passage ' + (at + 1) + '; it holds ' + passages.length + '.');
    const facts = [];
    if (one.artifact_type) facts.push(one.artifact_type);
    if (one.rights) facts.push(one.rights);
    if (one.rights_jurisdiction) facts.push(one.rights_jurisdiction);
    if (one.storage) facts.push('stored ' + one.storage);
    const said = {
      at,
      id: one.id,
      count: 'Passage ' + (at + 1) + ' of ' + passages.length, // sources.js:403-405
      locus: one.locus || one.id,
      states: (one.states || []).join(' · '),
      context: one.context || '',
      readable: Boolean(one.readable),
      provenance: {
        controller: one.artifact_id || '',
        none: one.artifact_id ? '' : 'No controlling artifact is recorded.', // sources.js:553
        facts: facts.join(' · '),
        basis: one.rights_basis && !one.acknowledgement ? one.rights_basis : '', // sources.js:562-564
        segment: one.segment_id ? 'The passage is narrowed within that artifact through segment ' + // sources.js:565-571
          one.segment_id + '; the segment does not replace its controller.' : '',
        sourceUrl: one.source_url || '',
      },
      notes: one.notes || '',
    };
    if (!one.readable) { // sources.js:478-487: the reason in place of the words
      said.reason = one.reason || '';
      said.withheld = one.withheld || '';
      return said;
    }
    let text;
    try {
      text = await T.loadJSON(one.text_path);
    } catch (error) { // sources.js:494-502
      said.unloaded = 'the text of this passage could not be loaded: ' + (error.message || error);
      return said;
    }
    said.acknowledgement = one.acknowledgement || ''; // sources.js:511-516, above the words
    said.words = one.words;
    said.source = one.source || '';
    said.language = text.language || (found.payload.edition || {}).language || 'en';
    // sources.js:524-532: paragraph by paragraph on its own breaks, every physical line kept
    said.paragraphs = String(text.text || '').split(/\n\s*\n/).filter((block) => block.trim())
      .map((block) => block.split('\n'));
    return said;
  }

  function notHere(passageId) { // page: sources.js:740-743
    return 'No passage with the id “' + passageId + '” can be opened here. It may be a record whose text ' +
      'this repository may not serve, in which case it is findable in the corpus under its own work.';
  }

  /* An address another surface cites: an edition id, a passage id, or both
   * (sources.js:777-803). The passage alone is followed through its own text
   * file, never taken apart (sources.js:705-719). */
  async function follow(editionId, passageId) {
    const { file, editions } = await spine();
    let place = editionId ? editions.get(editionId) : undefined;
    if (!place && passageId) {
      let pointer = null;
      try {
        pointer = await T.loadJSON((file.texts || '') + passageId + '.json');
      } catch (error) {
        pointer = null;
      }
      if (pointer) {
        const work = (file.works || []).find((one) => one.id === pointer.work_id);
        const edition = work && (work.editions || []).find((one) => one.id === pointer.edition_id);
        if (edition) place = editions.get(edition.id);
      }
      if (!place) return { problem: notHere(passageId) };
    }
    if (!place) { // page: sources.js:756-760
      return { problem: 'No edition with the id “' + editionId + '” can be opened here. The address has been ' +
        'left unchanged so it cannot be mistaken for another edition.' };
    }
    const [workAt, editionAt] = place;
    if (!passageId) return { work: workAt, edition: editionAt, at: 0 };
    const found = await opened(workAt, editionAt);
    if (found.problem) return { problem: found.problem };
    const at = (found.payload.passages || []).findIndex((one) => one.id === passageId);
    if (at < 0) return { problem: notHere(passageId) }; // sources.js:264-277: never passage one
    return { work: workAt, edition: editionAt, at };
  }

  return { opening, find, edition, passage, follow };
};
