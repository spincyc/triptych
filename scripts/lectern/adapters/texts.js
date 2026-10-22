'use strict';
/*
 * Every Document, as `src/web/browser/texts/texts.js` assembles it.
 *
 * The catalogue is the one generated file the page reads
 * (structure/documents/corpus.json, texts.js:20). Which treatments a set of
 * choices leaves, what each is called, the order they come back in, what the
 * list amounts to and whether a production record has drifted are
 * `catalogue-model.js`'s answers, asked as texts.js asks them. The sentences
 * marked `page:` are texts.js's own prose, repeated with the line they come
 * from; nothing else here is written by hand.
 *
 * One word differs, deliberately. The page calls a provider's document an
 * "edition". The accepted vision (guidance/corpus-browser-vision.md:129-141)
 * keeps that word for bibliographic Source Editions and names a provider's
 * document an independent treatment, with the provider kept explicit; the
 * terminal uses the vision's word. Every count noun the page uses (works,
 * documents, pages) is kept as the page has it.
 *
 * Works and treatments are addressed by their position in the catalogue's own
 * arrays, so the Python side can hold the rows once and be told, per choice,
 * which survive and in what order.
 */
const fs = require('fs');
const path = require('path');

module.exports = function texts(realm) {
  realm.script('shared/browser-core.js');
  realm.script('texts/catalogue-model.js');
  const T = globalThis.Triptych;
  const M = globalThis.CatalogueModel;
  const CATALOGUE = 'structure/documents/corpus.json'; // texts.js:20

  const SORTS = [ // texts.js:25-30
    { value: 'section', label: 'Section, then path' },
    { value: 'title', label: 'Title' },
    { value: 'revised', label: 'Last revised' },
    { value: 'pages', label: 'Extent' },
  ];
  const PRODUCTION_FIELDS = [ // texts.js:225-232
    ['Workflow', 'workflow_id'],
    ['Workflow version', 'workflow_version'],
    ['Workflow digest', 'workflow_digest'],
    ['Run', 'run_id'],
    ['Seed commit', 'seed_commit'],
    ['Install commit', 'install_commit'],
  ];

  let loading = null;
  function catalogue() {
    if (!loading) {
      loading = T.loadJSON(CATALOGUE).then((file) => {
        const position = new Map();
        (file.works || []).forEach((one, index) => position.set(one, index));
        return { file, position };
      });
      loading.catch(() => { loading = null; });
    }
    return loading;
  }

  /* Whether a path the catalogue records is present in this checkout. The
   * installed PDFs stopped being tracked on 2026-09-04 and are built at deploy
   * (guidance/repository.md:24-41), so a recorded PDF is usually not here; the
   * reader says so rather than offering a path that leads nowhere. */
  function here(relative) {
    if (!relative) return false;
    const file = path.resolve(realm.ROOT, relative);
    const inside = path.relative(realm.ROOT, file);
    return !inside.startsWith('..') && !path.isAbsolute(inside) && fs.existsSync(file);
  }

  function providerLabel(file, provider) { // texts.js:53-56
    const known = (file.providers || []).find((row) => row.id === provider);
    return known ? known.label : provider;
  }

  function extent(edition) { // texts.js:58-61
    const pages = M.pagesOf(edition);
    return pages === null ? null : pages + (pages === 1 ? ' page' : ' pages');
  }

  function day(stamp) { // texts.js:63-65
    return String(stamp || '').slice(0, 10);
  }

  function drift(file, edition) { // texts.js:102-134
    const found = M.driftOf(edition, file.workflows || []);
    if (!found) return null;
    let words = null;
    let state = null;
    if (found.behind) {
      words = 'produced under ' + found.workflow + ' v' + found.recorded + ', now v' + found.current;
      state = 'produced-under-an-earlier-workflow';
    } else if (found.ahead) {
      words = 'produced under ' + found.workflow + ' v' + found.recorded + ', declared v' + found.current;
      state = 'produced-under-a-later-workflow';
    } else if (found.revised) {
      words = 'produced under ' + found.workflow + ' v' + found.recorded + ', guidance revised since';
      state = 'produced-under-revised-workflow-guidance';
    }
    if (words === null) return null;
    return {
      words, state,
      title: 'Advisory only. The workflow that produced this document is not the ' + // page: texts.js:129-132
        'workflow this repository declares today. It is not a statement that ' +
        'the document is wrong, and nothing in the project gates on it.',
    };
  }

  function treatment(file, work, edition) { // texts.js:136-190, the card's row
    const name = M.nameOf(work, edition);
    return {
      provider: edition.provider,
      providerLabel: providerLabel(file, edition.provider),
      title: name.text,
      unrecorded: name.unrecorded,
      // page: texts.js:155 (T.notice prefixes "Not shown: ")
      unrecordedNote: name.unrecorded ? 'this document states no title of its own — ' + name.reason : '',
      subject: edition.subject || '',
      extent: extent(edition),
      revised: edition.revised ? day(edition.revised) : '',
      drift: drift(file, edition),
      models: edition.models || [],
      status: edition.status || '',
      web: edition.web || '',
      pdf: edition.pdf || '',
      pdfHere: here(edition.pdf),
      pdfAbsent: edition.pdf_absent || '',
      also: (edition.also || []).map((issue) => ({ // texts.js:181-187
        label: T.titleCase(issue.kind) + ' PDF',
        pages: typeof issue.pages === 'number' ? issue.pages : null,
        pdf: issue.pdf || '',
        pdfHere: here(issue.pdf),
        pdfAbsent: issue.pdf_absent || '',
        title: issue.title || '',
      })),
    };
  }

  function count(number, noun) { // texts.js:461-463
    return number.toLocaleString('en') + ' ' + noun + (number === 1 ? '' : 's');
  }

  function state(asked) { // texts.js:67-76
    asked = asked || {};
    return {
      author: asked.author || M.ANY,
      edition: asked.edition || M.ANY,
      section: asked.section || M.ANY,
      reading: asked.reading || M.ANY,
      sort: asked.sort || 'section',
      find: String(asked.find || '').trim().toLowerCase(),
    };
  }

  async function opening() {
    const { file } = await catalogue();
    const models = file.models || [];
    return {
      schema: file.schema,
      advisory: file.advisory || '', // texts.js:556-557: printed from the file
      counted: file.counted || {},
      controls: { // texts.js:469-495
        author: [{ value: M.ANY, label: 'Any author' }].concat(
          models.map((model) => ({ value: model.id, label: model.id + ' (' + model.documents + ')' }))),
        edition: [{ value: M.ANY, label: 'Both treatments' }].concat( // page: 'Both editions'
          (file.providers || []).map((one) => ({ value: one.id, label: one.label + ' (' + one.documents + ')' }))),
        section: [{ value: M.ANY, label: 'Every section' }].concat(
          (file.sections || []).map((one) => ({ value: one.id, label: T.titleCase(one.id) + ' (' + one.works + ')' }))),
        reading: [
          { value: M.ANY, label: 'However held' },
          { value: M.READABLE, label: 'Readable here' },
          { value: M.DOWNLOAD, label: 'PDF only' },
        ],
        sort: SORTS,
      },
      providers: (file.providers || []).map((one) => ({ id: one.id, label: one.label })),
      works: (file.works || []).map((work) => ({
        leaf: work.leaf,
        section: work.section,
        sectionLabel: T.titleCase(work.section),
        catalog: work.catalog || '',
        treatments: (work.editions || []).map((edition) => treatment(file, work, edition)),
      })),
    };
  }

  function tallyOf(file, asked) {
    return M.tally(M.narrow(file.works, asked));
  }

  /* The list a set of choices leaves (texts.js:400-442), as positions. */
  async function find(asked) {
    const { file, position } = await catalogue();
    const chosen = state(asked);
    const rows = M.order(M.narrow(file.works, chosen), chosen.sort);
    const counted = M.tally(rows);
    const whole = (file.counted || {}).documents || 0;
    // page: texts.js:414-422 — "of N" only while the list is narrowed
    const summary = count(counted.works, 'work') + ' · ' + count(counted.documents, 'document') +
      ' · ' + count(counted.pages, 'page') + (counted.documents === whole ? '' : ' of ' + whole);
    const tally = summary + (counted.unrecorded ? ' · ' + count(counted.unrecorded, 'title') + ' unrecorded' : '');

    /* How the chosen documents are held, each figure the model's own tally of
     * the same choices with one control set otherwise: the reading control for
     * the split between readable here and PDF only, the treatment control for
     * the split by provider. Nothing is counted here that the model does not
     * count. */
    const anyReading = Object.assign({}, chosen, { reading: M.ANY });
    const anyProvider = Object.assign({}, chosen, { edition: M.ANY });
    const holdings = {
      held: tallyOf(file, anyReading).documents,
      readable: tallyOf(file, Object.assign({}, anyReading, { reading: M.READABLE })).documents,
      pdfOnly: tallyOf(file, Object.assign({}, anyReading, { reading: M.DOWNLOAD })).documents,
      providersOf: tallyOf(file, anyProvider).documents,
      providers: (file.providers || []).map((one) => ({
        id: one.id, label: one.label,
        documents: tallyOf(file, Object.assign({}, anyProvider, { edition: one.id })).documents,
      })),
    };
    return {
      state: chosen,
      rows: rows.map((row) => [position.get(row.work), row.editions.map((one) => row.work.editions.indexOf(one))]),
      tally,
      counted,
      whole,
      zero: rows.length ? '' : 'Nothing in the corpus matches those choices. Widen one of them.', // texts.js:408-409
      holdings,
    };
  }

  function issue(kind, pages, pdf, absent, status, authorization, title) { // texts.js:367-385
    const measured = typeof pages === 'number' ? pages + 'pp' : 'extent unrecorded';
    return {
      kind: T.titleCase(kind),
      said: measured + ' · ' + (status || 'no release status') + ' · ' + (authorization || 'no authorization recorded'),
      title: title ? 'titled ' + title : '',
      pdf: pdf || '',
      pdfHere: here(pdf),
      absent: absent || '',
    };
  }

  /* The record panel (texts.js:260-365), line for line. */
  async function record(workAt, editionAt) {
    const { file } = await catalogue();
    const work = (file.works || [])[workAt];
    const edition = work && (work.editions || [])[editionAt];
    if (!edition) throw new Error('no treatment at ' + workAt + '/' + editionAt + ' in the catalogue');
    const name = M.nameOf(work, edition);
    const lines = [];
    let notice = '';
    if (name.unrecorded) notice = name.reason;
    else {
      lines.push(['Title declared in', edition.title_source || 'not recorded']);
      if (edition.title_template) lines.push(['Composed as', edition.title_template]);
    }
    if (edition.subject) lines.push(['Subject', edition.subject]);
    lines.push(['Extent', extent(edition) || 'not recorded']);
    lines.push(['Last revised', edition.revised || 'not recorded']);
    lines.push(['Section', work.section]);
    if (work.catalog) lines.push(['Catalogued in', work.catalog]);

    const produced = edition.produced || {}; // texts.js:234-258
    const known = PRODUCTION_FIELDS.filter((pair) => produced[pair[1]]);
    const production = known.length
      ? PRODUCTION_FIELDS.map((pair) => [pair[0], produced[pair[1]] || 'not recorded', !!produced[pair[1]]])
      : [['Production record', 'nothing recorded, and no origin was invented for it', false]];

    const browser = edition.web // texts.js:307-324
      ? { label: 'Rendered', value: 'eligible, reviewed ' + day(edition.reviewed) }
      : {
        label: 'Not rendered', value: edition.eligibility + ', reviewed ' + day(edition.reviewed),
        basis: edition.basis || '', rationale: edition.rationale || '',
        blockedBy: (edition.blocking_constructs || []).join(', '),
      };

    const issues = [issue('full', edition.pages, edition.pdf, edition.pdf_absent,
      edition.status, edition.authorization, null)];
    for (const one of edition.also || []) { // texts.js:329-339
      issues.push(issue(one.kind, one.pages, one.pdf, one.pdf_absent,
        'status' in one ? one.status : edition.status,
        'authorization' in one ? one.authorization : edition.authorization,
        one.title || null));
    }

    let authorship; // texts.js:341-361
    if (edition.inherits) {
      authorship = {
        inherited: edition.inherits,
        notice: 'this document is set from that one’s sources and records a pointer to ' +
          'its ledger rather than a copy of it. The models listed for it are that ' +
          'document’s; open that document for the roles they took.',
      };
    } else if ((edition.contributions || []).length) {
      authorship = { contributions: edition.contributions.map((one) => ({
        model: one.model, qualifiers: one.qualifiers, runtime: one.runtime })) };
    } else {
      authorship = { notice: 'this document records no contribution at all.' };
    }

    return {
      heading: name.text,
      unrecorded: name.unrecorded,
      // page: texts.js:280 reads "<Provider> edition of <leaf>"; see the note above
      sub: providerLabel(file, edition.provider) + ' · independent treatment of ' + work.leaf,
      notice,
      lines,
      production,
      browser,
      issues,
      authorship,
      treatment: treatment(file, work, edition),
    };
  }

  /* A treatment named by its work's path and its provider, as another surface
   * would cite it. A miss is said, never rounded to a neighbour. */
  async function locate(leaf, provider) {
    const { file } = await catalogue();
    const workAt = (file.works || []).findIndex((one) => one.leaf === leaf);
    if (workAt < 0) return { problem: 'No work with the path “' + leaf + '” is in the catalogue.' };
    const editions = file.works[workAt].editions || [];
    if (!provider) return { work: workAt, edition: null }; // the work, with no treatment preferred
    const editionAt = editions.findIndex((one) => one.provider === provider);
    if (editionAt < 0) {
      return { problem: 'The catalogue holds no ' + providerLabel(file, provider) + ' treatment of “' + leaf + '”.' };
    }
    return { work: workAt, edition: editionAt };
  }

  return { opening, find, record, locate };
};
