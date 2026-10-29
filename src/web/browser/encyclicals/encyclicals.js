/* Every encyclical, one row each, from one generated file.
 *
 * The file is encyclicals/index.json under the data root, written by
 * `scripts/_encyclicals.py structure` from the tracked index. This page reads it
 * and nothing else: it opens no PDF, walks no tree, and derives no fact the
 * generator did not state. What a choice selects and what order the rows come
 * back in are in encyclicals-model.js beside this file, which node can run and
 * the tests do run. Everything here is markup.
 *
 * Two things on this page are not the popes' and must never read as theirs:
 * the one-line descriptions, which an AI model wrote, and the reasons a row
 * carries no text. Both are labelled where they stand, in words, so the label
 * survives a stylesheet that never loads and a narrow screen that drops the
 * column headings.
 *
 * All output is built with createElement/textContent, never innerHTML.
 */
(function () {
  'use strict';

  const T = window.Triptych;
  const M = window.EncyclicalsModel;
  const CATALOGUE = 'encyclicals/index.json';
  /* The page sits one directory below the site root, and the PDFs hang off it. */
  const SITE = '..';

  const table = document.getElementById('enc-table');
  const head = document.getElementById('enc-head');
  const body = document.getElementById('enc-body');
  const region = document.getElementById('reading');
  const placeholder = document.getElementById('enc-placeholder');
  const scroller = document.getElementById('enc-scroll');
  const scrollHint = document.getElementById('enc-scroll-hint');
  const tally = document.getElementById('tally');
  const banner = document.getElementById('banner');
  const provenance = document.getElementById('enc-provenance');
  const popeSelect = document.getElementById('pope-select');
  const textSelect = document.getElementById('text-select');
  const sortSelect = document.getElementById('sort-select');
  const findInput = document.getElementById('find-input');
  const controls = [popeSelect, textSelect, sortSelect];

  let catalogue = null;
  let columns = [];
  let invalid = [];
  const sortButtons = {};

  function count(number, noun, plural) {
    return number.toLocaleString('en') + ' ' + (number === 1 ? noun : (plural || noun + 's'));
  }

  function labelOf(code) {
    const column = columns.find(function (one) { return one.code === code; });
    return column ? column.label : code;
  }

  function readState() {
    return {
      pope: popeSelect.value || M.ANY,
      text: textSelect.value || M.ANY,
      sort: sortSelect.value || M.DEFAULT_SORT,
      find: (findInput.value || '').trim()
    };
  }

  /* ------------------------------------------------------------------------
   * The head: built once, so a pressed heading keeps its focus
   * --------------------------------------------------------------------- */

  function headCell(text, key) {
    const cell = T.el('th');
    cell.scope = 'col';
    cell.setAttribute('role', 'columnheader');
    if (!key) {
      cell.textContent = text;
      return cell;
    }
    const button = T.el('button', 'enc-sort');
    button.type = 'button';
    button.appendChild(document.createTextNode(text));
    const mark = T.el('span', 'enc-sort-mark');
    mark.setAttribute('aria-hidden', 'true');
    button.appendChild(mark);
    button.addEventListener('click', function () {
      sortSelect.value = M.toggled(sortSelect.value, key);
      render();
    });
    cell.appendChild(button);
    sortButtons[key] = { cell: cell, mark: mark };
    return cell;
  }

  function buildHead() {
    T.clear(head);
    head.setAttribute('role', 'row');
    head.appendChild(headCell('Year', 'date'));
    head.appendChild(headCell('Pope', 'pope'));
    head.appendChild(headCell('Encyclical', 'title'));
    head.appendChild(headCell('Summary (AI-written)'));
    for (const column of columns) head.appendChild(headCell(column.label));
    head.appendChild(headCell('Vatican'));
  }

  function markSort(sort) {
    const descending = sort.charAt(0) === '-';
    const key = descending ? sort.slice(1) : sort;
    for (const name of Object.keys(sortButtons)) {
      const entry = sortButtons[name];
      if (name === key) {
        entry.cell.setAttribute('aria-sort', descending ? 'descending' : 'ascending');
        entry.mark.textContent = descending ? ' ▼' : ' ▲';
        entry.mark.classList.remove('enc-sort-idle');
      } else {
        entry.cell.setAttribute('aria-sort', 'none');
        entry.mark.textContent = ' ↕';
        entry.mark.classList.add('enc-sort-idle');
      }
    }
  }

  /* ------------------------------------------------------------------------
   * One row
   * --------------------------------------------------------------------- */

  function cell(label, className) {
    const node = T.el('td', className);
    node.setAttribute('role', 'cell');
    /* On a narrow screen the headings are not on screen, so each cell carries
       its own; the stylesheet prints it before the content. */
    node.setAttribute('data-label', label);
    return node;
  }

  function readerItem(row, reader) {
    const item = T.el('li', 'enc-reader');
    item.setAttribute('data-extent', reader.extent);
    const link = T.el('a', 'enc-pdf');
    link.href = SITE + '/' + reader.pdf;
    link.type = 'application/pdf';
    link.hreflang = reader.language;
    link.appendChild(T.el('span', 'visually-hidden', labelOf(reader.language) + ' reading edition of ' + row.title + ', '));
    link.appendChild(document.createTextNode(
      'PDF, ' + reader.pages + (reader.pages === 1 ? ' page' : ' pp')));
    item.appendChild(link);
    if (reader.extent !== 'complete') {
      /* In words, not only a colour: a fragment or a damaged printing is a
         fact about what the reader will find, and it must survive a
         stylesheet that never loads. */
      const mark = T.el('span', 'enc-extent', reader.extent === 'fragment' ? 'Fragment' : 'Damaged printing');
      mark.setAttribute('data-extent', reader.extent);
      item.appendChild(document.createTextNode(' '));
      item.appendChild(mark);
    }
    item.appendChild(T.el('span', 'enc-witness', reader.witness));
    return item;
  }

  function languageCell(row, column) {
    const node = cell(column.label, 'enc-language');
    node.setAttribute('data-language', column.code);
    const readers = M.readersIn(row, column.code);
    if (!readers.length) {
      node.classList.add('enc-empty');
      node.appendChild(T.el('span', 'enc-none', '—'));
      node.appendChild(T.el('span', 'visually-hidden', 'No ' + column.label + ' text here'));
      return node;
    }
    const list = T.el('ul', 'enc-readers');
    for (const reader of readers) list.appendChild(readerItem(row, reader));
    node.appendChild(list);
    return node;
  }

  function rowFor(row) {
    const tr = T.el('tr', 'enc-row');
    tr.setAttribute('role', 'row');
    tr.setAttribute('data-id', row.id);

    const year = cell('Year', 'enc-year');
    if (row.date) {
      const time = T.el('time', 'enc-year-figure', String(row.year));
      time.dateTime = row.date;
      year.appendChild(time);
      year.appendChild(T.el('span', 'enc-date', M.longDate(row.date)));
    } else {
      year.appendChild(T.el('span', 'enc-undated', row.year ? row.year + ', day undated' : 'Undated'));
    }
    tr.appendChild(year);

    const pope = cell('Pope', 'enc-pope');
    pope.textContent = row.pope;
    tr.appendChild(pope);

    const title = T.el('th', 'enc-title');
    title.scope = 'row';
    title.setAttribute('role', 'rowheader');
    title.appendChild(T.el('span', 'enc-incipit', row.title));
    if (row.subject) title.appendChild(T.el('span', 'enc-subject', row.subject));
    tr.appendChild(title);

    /* A summary not yet written is null in the data and a blank cell here:
       nothing is put in its place that could be read as one. */
    const summary = cell('AI-written summary', 'enc-summary');
    if (row.description) summary.textContent = row.description;
    else summary.classList.add('enc-empty');
    tr.appendChild(summary);

    if ((row.readers || []).length) {
      for (const column of columns) tr.appendChild(languageCell(row, column));
    } else {
      const absent = cell('Text here', 'enc-absent');
      absent.colSpan = columns.length;
      absent.appendChild(T.el('span', 'enc-absent-label', 'No text here: '));
      absent.appendChild(document.createTextNode(row.no_local_text_reason));
      tr.appendChild(absent);
    }

    const vatican = cell('Vatican', 'enc-vatican');
    if (row.links && row.links.vatican) {
      const link = T.el('a', 'enc-vatican-link');
      link.href = row.links.vatican;
      link.rel = 'noopener';
      link.appendChild(document.createTextNode('Vatican page'));
      link.appendChild(T.el('span', 'visually-hidden', ' for ' + row.title + ' (external site)'));
      vatican.appendChild(link);
    } else {
      vatican.classList.add('enc-empty');
      vatican.appendChild(T.el('span', 'enc-none', '—'));
      vatican.appendChild(T.el('span', 'visually-hidden', 'No Vatican page recorded'));
    }
    tr.appendChild(vatican);
    return tr;
  }

  function messageRow(text, withReset) {
    const tr = T.el('tr', 'enc-message');
    tr.setAttribute('role', 'row');
    const td = T.el('td');
    td.setAttribute('role', 'cell');
    td.colSpan = 5 + columns.length;
    td.appendChild(T.el('p', 'placeholder', text));
    if (withReset) {
      const reset = T.el('button', 'enc-reset', 'Show every encyclical');
      reset.type = 'button';
      reset.addEventListener('click', clearAll);
      td.appendChild(reset);
    }
    tr.appendChild(td);
    return tr;
  }

  /* ------------------------------------------------------------------------
   * The pass
   * --------------------------------------------------------------------- */

  function describeState(state) {
    const parts = [];
    if (state.pope) {
      const pope = (catalogue.popes || []).find(function (one) { return one.id === state.pope; });
      parts.push(pope ? pope.name : state.pope);
    }
    const text = M.TEXT_FILTERS.find(function (one) { return one.value === state.text; });
    if (state.text && text) parts.push(text.label.toLowerCase());
    if (state.find) parts.push('matching “' + state.find + '”');
    return parts.join(', ');
  }

  function tallyText(rows) {
    const whole = catalogue.counts || {};
    const counted = M.tally(rows);
    const all = M.tally(catalogue.encyclicals || []);
    const range = all.first !== null ? ', ' + all.first + '–' + all.last : '';
    let text = count(whole.encyclicals || 0, 'encyclical') + range + ' · ' +
      count(whole.with_local_text || 0, 'with a text here', 'with a text here') + ' · ' +
      columns.map(function (column) {
        return (all.byLanguage[column.code] || 0) + ' ' + column.label;
      }).join(', ') + ' reading editions';
    if (counted.encyclicals !== (whole.encyclicals || 0)) {
      text += ' · showing ' + count(counted.encyclicals, 'row');
    }
    return text;
  }

  function render() {
    const state = readState();
    T.clear(body);
    markSort(state.sort);
    if (invalid.length) {
      body.appendChild(messageRow(
        'This address asks for ' + invalid.map(function (one) {
          return one.key + ' “' + one.value + '”';
        }).join(' and ') + ', which this list does not hold, so nothing is shown under it.',
        true
      ));
      tally.textContent = tallyText([]);
      region.setAttribute('aria-busy', 'false');
      T.statusLine('Nothing shown: the address names a choice this list does not hold.');
      return;
    }
    const rows = M.order(M.narrow(catalogue, state), state.sort);
    const fragment = document.createDocumentFragment();
    for (const row of rows) fragment.appendChild(rowFor(row));
    body.appendChild(fragment);
    if (!rows.length) {
      body.appendChild(messageRow(
        'No encyclical matches ' + (describeState(state) || 'these choices') + '.', true
      ));
    }
    tally.textContent = tallyText(rows);
    region.setAttribute('aria-busy', 'false');
    updateScrollHint();
    T.statusLine(count(rows.length, 'encyclical') + ' shown' +
      (describeState(state) ? ', ' + describeState(state) : '') + '.');
    writeAddress(state);
  }

  /* Said in words when the table is wider than its box, because the only
     other cue is a scrollbar under the last row. */
  function updateScrollHint() {
    if (!scroller || !scrollHint) return;
    scrollHint.hidden = table.hidden || scroller.scrollWidth <= scroller.clientWidth + 1;
  }

  function writeAddress(state) {
    const pairs = M.hashPairs(state);
    if (pairs.some(function (pair) { return pair[1]; })) {
      T.replaceHash(pairs);
    } else if (window.location.hash) {
      try {
        window.history.replaceState(null, '', window.location.pathname + window.location.search);
      } catch (error) {
        window.location.hash = '';
      }
    }
  }

  function clearAll() {
    invalid = [];
    banner.hidden = true;
    restoreOptions();
    popeSelect.value = M.ANY;
    textSelect.value = M.ANY;
    sortSelect.value = M.DEFAULT_SORT;
    findInput.value = '';
    render();
    findInput.focus();
  }

  /* ------------------------------------------------------------------------
   * Start
   * --------------------------------------------------------------------- */

  function fill() {
    T.fillSelect(popeSelect, [{ value: M.ANY, label: 'Every pope (' + (catalogue.counts || {}).encyclicals + ')' }]
      .concat((catalogue.popes || []).map(function (pope) {
        return { value: pope.id, label: pope.name + ' (' + pope.encyclicals + ')' };
      })));
    T.fillSelect(textSelect, M.TEXT_FILTERS);
    T.fillSelect(sortSelect, M.SORTS);
  }

  /* A value no option carries is shown as what it is, selected, so the control
     names the state the page is actually in rather than falling to its first
     option while the list says something else. */
  function holdUnknown(select, value) {
    const option = T.el('option', 'enc-unknown', 'Not in this list: ' + value);
    option.value = value;
    select.appendChild(option);
    select.value = value;
  }

  function restoreOptions() {
    for (const select of controls) {
      for (const stale of Array.from(select.querySelectorAll('option.enc-unknown'))) stale.remove();
    }
  }

  function restore() {
    restoreOptions();
    const parsed = M.stateFrom(T.readHash(), catalogue);
    invalid = parsed.invalid;
    const bad = {};
    for (const one of invalid) bad[one.key] = one.value;
    const pairs = [[popeSelect, 'pope', M.ANY], [textSelect, 'text', M.ANY], [sortSelect, 'sort', M.DEFAULT_SORT]];
    for (const pair of pairs) {
      const value = parsed.state[pair[1]];
      if (pair[1] in bad) holdUnknown(pair[0], value);
      else pair[0].value = value || pair[2];
    }
    findInput.value = parsed.state.find;
    if (invalid.length) {
      T.showBanner('This link asks for ' + invalid.map(function (one) {
        return one.key + ' “' + one.value + '”';
      }).join(' and ') + ', which this list does not hold. Choose again, or show every encyclical.');
    } else {
      banner.hidden = true;
    }
  }

  function changed() {
    if (invalid.length) {
      invalid = [];
      banner.hidden = true;
      restoreOptions();
      for (const select of controls) if (select.selectedIndex < 0) select.selectedIndex = 0;
    }
    render();
  }

  async function start() {
    T.setInlineNotice(
      'No data root could be reached, so this page has nothing to list. Serve ' +
        'the pages over HTTP with the data at "' + T.dataRoot + '".'
    );
    try {
      catalogue = await T.loadJSON(CATALOGUE);
    } catch (error) {
      T.doneBootstrapping();
      for (const control of controls) {
        T.fillSelect(control, [{ value: '', label: 'Unavailable — the list could not be read' }]);
        control.disabled = true;
      }
      findInput.placeholder = 'The list could not be read';
      if (placeholder) placeholder.remove();
      T.fail('The list of encyclicals could not be loaded: ' + (error.message || error), region);
      return;
    }
    T.doneBootstrapping();
    if (!catalogue || catalogue.schema !== 'triptych-encyclicals-browser/v1' ||
        !Array.isArray(catalogue.encyclicals)) {
      if (placeholder) placeholder.remove();
      T.fail('The list of encyclicals is not in the form this page reads.', region);
      return;
    }

    columns = M.languageColumns(catalogue);
    const provenanceRecord = catalogue.description_provenance || {};
    if (provenance && provenanceRecord.author) {
      provenance.textContent = 'Written by ' + provenanceRecord.author +
        (provenanceRecord.written_on ? ', ' + provenanceRecord.written_on : '') +
        (provenanceRecord.method ? '. ' + provenanceRecord.method : '.');
    }
    buildHead();
    fill();
    restore();
    for (const control of controls) {
      control.disabled = false;
      control.addEventListener('change', changed);
    }
    findInput.disabled = false;
    let pending = null;
    findInput.addEventListener('input', function () {
      window.clearTimeout(pending);
      pending = window.setTimeout(changed, 120);
    });
    document.getElementById('controls').addEventListener('submit', function (event) {
      event.preventDefault();
      changed();
    });
    T.onHashChange(function () {
      restore();
      render();
    });
    if (placeholder) placeholder.remove();
    table.hidden = false;
    window.addEventListener('resize', updateScrollHint);
    render();
  }

  start();
}());
