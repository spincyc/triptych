/* Every document this project holds, listed from one generated file.
 *
 * The file is structure/documents/corpus.json, written by `document-library
 * structure`. This page reads it and nothing else. It does not walk the source
 * tree, it does not open a PDF, and it derives no fact the generator did not
 * already state — which is the point: the corpus is read once, by a tool a
 * check can run, and the browser only arranges what that tool wrote.
 *
 * What a choice selects, what a document is called, and what order the list
 * comes back in are in catalogue-model.js beside this file, which node can run
 * and `document-library check` does run. Everything here is markup.
 *
 * All output is built with createElement/textContent, never innerHTML.
 */
(function () {
  'use strict';

  const T = window.Triptych;
  const M = window.CatalogueModel;
  const CATALOGUE = 'structure/documents/corpus.json';
  /* The page sits one directory below the site root, and the PDFs, the web
     editions and the collection pages all hang off that root. */
  const SITE = '..';

  const SORTS = [
    { value: 'section', label: 'Section, then path' },
    { value: 'title', label: 'Title' },
    { value: 'revised', label: 'Last revised' },
    { value: 'pages', label: 'Extent' }
  ];

  const list = document.getElementById('reading');
  const detail = document.getElementById('detail');
  const tally = document.getElementById('tally');
  const authorSelect = document.getElementById('author-select');
  const editionSelect = document.getElementById('edition-select');
  const sectionSelect = document.getElementById('section-select');
  const readingSelect = document.getElementById('reading-select');
  const sortSelect = document.getElementById('sort-select');
  const findInput = document.getElementById('find-input');
  const advisory = document.getElementById('advisory');

  let catalogue = null;
  let opened = null;

  /* ------------------------------------------------------------------------
   * Reading the record
   *
   * Every accessor below answers from the generated file or says it cannot.
   * None of them fills anything in.
   * --------------------------------------------------------------------- */

  function editionLabel(provider) {
    const known = (catalogue.providers || []).find((row) => row.id === provider);
    return known ? known.label : provider;
  }

  function extent(edition) {
    const pages = M.pagesOf(edition);
    return pages === null ? null : pages + (pages === 1 ? ' page' : ' pages');
  }

  function day(stamp) {
    return String(stamp || '').slice(0, 10);
  }

  function readState() {
    return {
      author: authorSelect.value || M.ANY,
      edition: editionSelect.value || M.ANY,
      section: sectionSelect.value || M.ANY,
      reading: readingSelect.value || M.ANY,
      sort: sortSelect.value || 'section',
      find: (findInput.value || '').trim().toLowerCase()
    };
  }

  /* ------------------------------------------------------------------------
   * Rendering
   * --------------------------------------------------------------------- */

  function link(className, href, text) {
    const node = T.el('a', className, text);
    node.href = href;
    return node;
  }

  function pill(text, className) {
    return T.el('span', 'pill' + (className ? ' ' + className : ''), text);
  }

  function editionRow(work, edition) {
    const row = T.el('div', 'edition');
    row.setAttribute('data-key', work.leaf + '|' + edition.provider);

    const head = T.el('p', 'edition-head');
    head.appendChild(T.el('span', 'edition-mark', editionLabel(edition.provider)));

    const name = M.nameOf(work, edition);
    const button = T.el('button', 'edition-title', name.text);
    button.type = 'button';
    button.setAttribute('aria-expanded', 'false');
    if (name.unrecorded) button.classList.add('unrecorded');
    button.addEventListener('click', function () {
      open(work, edition, button);
    });
    head.appendChild(button);
    row.appendChild(head);

    if (name.unrecorded) {
      row.appendChild(T.notice('this document states no title of its own — ' + name.reason));
    }

    if (edition.subject) row.appendChild(T.el('p', 'edition-subject', edition.subject));

    const meta = T.el('p', 'edition-meta');
    const measure = extent(edition);
    meta.appendChild(pill(measure || 'extent unrecorded', measure ? '' : 'pill-absent'));
    if (edition.revised) meta.appendChild(pill('revised ' + day(edition.revised)));
    for (const model of edition.models || []) meta.appendChild(pill(model, 'pill-model'));
    if (!(edition.models || []).length) {
      meta.appendChild(pill('authorship not stated', 'pill-absent'));
    }
    row.appendChild(meta);

    const where = T.el('p', 'edition-links');
    if (edition.web) {
      where.appendChild(link('read', SITE + '/' + edition.web, 'Read here'));
    }
    if (edition.pdf) {
      where.appendChild(link('download', SITE + '/' + edition.pdf, 'PDF'));
    } else if (edition.pdf_absent) {
      where.appendChild(T.el('span', 'absent', edition.pdf_absent));
    }
    for (const issue of edition.also || []) {
      if (!issue.pdf) continue;
      const measured = typeof issue.pages === 'number' ? ', ' + issue.pages + 'pp' : '';
      where.appendChild(
        link('download', SITE + '/' + issue.pdf, T.titleCase(issue.kind) + ' PDF' + measured)
      );
    }
    row.appendChild(where);
    return row;
  }

  function workCard(row) {
    const card = T.el('article', 'work');
    const head = T.el('p', 'work-head');
    head.appendChild(T.el('span', 'work-section', row.work.section));
    head.appendChild(T.el('code', 'work-leaf', row.work.leaf));
    if (row.work.catalog_page) {
      head.appendChild(
        link('work-catalog', SITE + '/' + row.work.catalog_page, 'in the catalogue')
      );
    }
    card.appendChild(head);
    for (const edition of row.editions) card.appendChild(editionRow(row.work, edition));
    return card;
  }

  /* ------------------------------------------------------------------------
   * The detail panel: everything recorded about one document
   * --------------------------------------------------------------------- */

  function line(label, value) {
    const node = T.el('p', 'detail-line');
    node.appendChild(T.el('span', 'detail-label', label));
    node.appendChild(document.createTextNode(value));
    return node;
  }

  function open(work, edition, button) {
    const key = work.leaf + '|' + edition.provider;
    if (opened === key) {
      close();
      return;
    }
    opened = key;
    for (const other of document.querySelectorAll('.edition-title[aria-expanded="true"]')) {
      other.setAttribute('aria-expanded', 'false');
    }
    button.setAttribute('aria-expanded', 'true');

    T.clear(detail);
    detail.hidden = false;

    const name = M.nameOf(work, edition);
    const heading = T.el('h2', 'detail-title', name.text);
    if (name.unrecorded) heading.classList.add('unrecorded');
    detail.appendChild(heading);
    detail.appendChild(
      T.el('p', 'detail-sub', editionLabel(edition.provider) + ' edition of ' + work.leaf)
    );

    const dismiss = T.el('button', 'detail-close', 'Close');
    dismiss.type = 'button';
    dismiss.addEventListener('click', close);
    detail.appendChild(dismiss);

    if (name.unrecorded) {
      detail.appendChild(T.notice(name.reason));
    } else {
      detail.appendChild(line('Title declared in', edition.title_source || 'not recorded'));
      if (edition.title_template) {
        detail.appendChild(line('Composed as', edition.title_template));
      }
    }
    if (edition.subject) detail.appendChild(line('Subject', edition.subject));

    const measure = extent(edition);
    detail.appendChild(line('Extent', measure || 'not recorded'));
    detail.appendChild(line('Last revised', edition.revised || 'not recorded'));
    detail.appendChild(line('Section', work.section));
    if (work.catalog) detail.appendChild(line('Catalogued in', work.catalog));

    detail.appendChild(T.el('h3', 'detail-heading', 'In the browser'));
    if (edition.web) {
      detail.appendChild(
        line('Rendered', 'eligible, reviewed ' + day(edition.reviewed))
      );
    } else {
      detail.appendChild(
        line('Not rendered', edition.eligibility + ', reviewed ' + day(edition.reviewed))
      );
      if (edition.basis) {
        detail.appendChild(line(edition.basis, edition.rationale || ''));
      }
      if ((edition.blocking_constructs || []).length) {
        detail.appendChild(
          line('Blocked by', (edition.blocking_constructs || []).join(', '))
        );
      }
    }

    detail.appendChild(T.el('h3', 'detail-heading', 'Issues'));
    detail.appendChild(issueLine('full', edition.pages, edition.pdf, edition.pdf_absent,
      edition.status, edition.authorization, null));
    for (const issue of edition.also || []) {
      detail.appendChild(issueLine(
        issue.kind,
        issue.pages,
        issue.pdf,
        issue.pdf_absent,
        'status' in issue ? issue.status : edition.status,
        'authorization' in issue ? issue.authorization : edition.authorization,
        issue.title || null
      ));
    }

    detail.appendChild(T.el('h3', 'detail-heading', 'Authorship'));
    if (edition.inherits) {
      detail.appendChild(
        line('Inherited from', edition.inherits)
      );
      detail.appendChild(T.notice(
        'this document is set from that one’s sources and records a pointer to ' +
        'its ledger rather than a copy of it. The models listed for it are that ' +
        'document’s; open that document for the roles they took.'
      ));
    } else if ((edition.contributions || []).length) {
      for (const contribution of edition.contributions) {
        const block = T.el('div', 'contribution');
        block.appendChild(T.el('p', 'contribution-model', contribution.model));
        block.appendChild(line('Configuration', contribution.qualifiers));
        block.appendChild(line('Agent and runtime', contribution.runtime));
        detail.appendChild(block);
      }
    } else {
      detail.appendChild(T.notice('this document records no contribution at all.'));
    }

    detail.scrollIntoView({ block: 'nearest' });
    T.statusLine('Showing the full record of ' + name.text + '.');
  }

  function issueLine(kind, pages, pdf, absent, status, authorization, title) {
    const node = T.el('p', 'detail-line');
    node.appendChild(T.el('span', 'detail-label', T.titleCase(kind)));
    const measured = typeof pages === 'number' ? pages + 'pp' : 'extent unrecorded';
    node.appendChild(document.createTextNode(
      measured + ' · ' + (status || 'no release status') +
      ' · ' + (authorization || 'no authorization recorded')
    ));
    if (title) {
      node.appendChild(T.el('span', 'detail-aside', 'titled ' + title));
    }
    if (pdf) {
      node.appendChild(document.createTextNode(' '));
      node.appendChild(link('download', SITE + '/' + pdf, pdf));
    } else if (absent) {
      node.appendChild(T.el('span', 'absent', absent));
    }
    return node;
  }

  function close() {
    opened = null;
    detail.hidden = true;
    T.clear(detail);
    for (const other of document.querySelectorAll('.edition-title[aria-expanded="true"]')) {
      other.setAttribute('aria-expanded', 'false');
    }
  }

  /* ------------------------------------------------------------------------
   * The pass
   * --------------------------------------------------------------------- */

  function render() {
    const state = readState();
    const rows = M.order(M.narrow(catalogue.works, state), state.sort);
    const counted = M.tally(rows);

    close();
    T.clear(list);
    if (!rows.length) {
      list.appendChild(T.el('p', 'placeholder',
        'Nothing in the corpus matches those choices. Widen one of them.'));
    }
    for (const row of rows) list.appendChild(workCard(row));
    list.setAttribute('aria-busy', 'false');

    // "of 178" appears only while the list is narrowed. Printing it against the
    // unnarrowed corpus would restate a total the next line already gives.
    const whole = (catalogue.counted || {}).documents || 0;
    const summary =
      count(counted.works, 'work') + ' · ' + count(counted.documents, 'document') +
      ' · ' + count(counted.pages, 'page') +
      (counted.documents === whole ? '' : ' of ' + whole);
    tally.textContent = summary +
      (counted.unrecorded ? ' · ' + count(counted.unrecorded, 'title') + ' unrecorded' : '');
    T.statusLine(summary + '.');

    T.writeHash([
      ['author', state.author],
      ['edition', state.edition],
      ['section', state.section],
      ['reading', state.reading],
      ['sort', state.sort === 'section' ? '' : state.sort],
      ['find', state.find]
    ]);
  }

  function count(number, noun) {
    return number.toLocaleString('en') + ' ' + noun + (number === 1 ? '' : 's');
  }

  /* ------------------------------------------------------------------------
   * Start
   * --------------------------------------------------------------------- */

  function fill() {
    const models = catalogue.models || [];
    T.fillSelect(authorSelect, [{ value: M.ANY, label: 'Any author' }].concat(
      models.map(function (model) {
        return { value: model.id, label: model.id + ' (' + model.documents + ')' };
      })
    ));
    T.fillSelect(editionSelect, [{ value: M.ANY, label: 'Both editions' }].concat(
      (catalogue.providers || []).map(function (provider) {
        return { value: provider.id, label: provider.label + ' (' + provider.documents + ')' };
      })
    ));
    T.fillSelect(sectionSelect, [{ value: M.ANY, label: 'Every section' }].concat(
      (catalogue.sections || []).map(function (section) {
        return {
          value: section.id,
          label: T.titleCase(section.id) + ' (' + section.works + ')'
        };
      })
    ));
    T.fillSelect(readingSelect, [
      { value: M.ANY, label: 'However held' },
      { value: M.READABLE, label: 'Readable here' },
      { value: M.DOWNLOAD, label: 'PDF only' }
    ]);
    T.fillSelect(sortSelect, SORTS);
  }

  function restore() {
    const hash = T.readHash();
    if (hash.get('author')) authorSelect.value = hash.get('author');
    if (hash.get('edition')) editionSelect.value = hash.get('edition');
    if (hash.get('section')) sectionSelect.value = hash.get('section');
    if (hash.get('reading')) readingSelect.value = hash.get('reading');
    sortSelect.value = hash.get('sort') || 'section';
    findInput.value = hash.get('find') || '';
  }

  async function start() {
    T.setInlineNotice(
      'No data root could be reached, so this page has nothing to list. Serve ' +
        'the pages over HTTP with the data at "' + T.dataRoot + '".'
    );
    try {
      catalogue = await T.loadJSON(CATALOGUE);
    } catch (error) {
      T.fail('The catalogue could not be loaded: ' + (error.message || error));
      return;
    }
    T.doneBootstrapping();

    fill();
    restore();
    for (const control of [authorSelect, editionSelect, sectionSelect, readingSelect, sortSelect]) {
      control.disabled = false;
      control.addEventListener('change', render);
    }
    findInput.disabled = false;
    findInput.addEventListener('input', render);
    T.onHashChange(function () {
      restore();
      render();
    });

    // The file says what it is; the page prints that rather than its own copy.
    if (catalogue.advisory) advisory.textContent = catalogue.advisory;
    render();
  }

  start();
}());
