/* Public, form-qualified Proper discovery. The index contains no body text. */
'use strict';

(function (root, factory) {
  const api = factory();
  if (typeof module === 'object' && module.exports) module.exports = api;
  if (root) root.TriptychProperSearch = api;
})(typeof window === 'object' ? window : null, function () {
  const LIMIT = 20;

  function normalized(value) {
    return String(value || '').toLowerCase().replace(/æ/g, 'ae').replace(/œ/g, 'oe')
      .normalize('NFD').replace(/[\u0300-\u036f]/g, '')
      .replace(/[^a-z0-9]+/g, ' ').trim().replace(/\s+/g, ' ');
  }

  const rowCache = new WeakMap();

  function prepared(row) {
    let entry = rowCache.get(row);
    if (entry) return entry;
    const name = normalized(row.name);
    const key = normalized(row.key);
    const incipits = (row.incipits || []).map(function (item) { return normalized(item.text); });
    const citations = (row.citations || []).map(function (item) { return normalized(item.ref); });
    const fields = [name, key, normalized(row.kind), normalized(row.season),
      normalized(row.fixed_date), normalized(row.form_name), normalized(row.form_id)]
      .concat(incipits)
      .concat(citations)
      // Public witness labels only, as the status line promises: a witness's
      // machine id can carry a date (an artifact made 2026-11-14), and a
      // civil-date query must never match a mass through it.
      .concat((row.witnesses || []).map(function (item) { return normalized(item.label); }))
      .join(' ');
    entry = { fields: fields, name: name, key: key, incipits: incipits, citations: citations };
    rowCache.set(row, entry);
    return entry;
  }

  function matchesPrepared(entry, tokens) {
    for (let i = 0; i < tokens.length; i += 1) {
      if (!entry.fields.includes(tokens[i])) return false;
    }
    return true;
  }

  function matches(row, query) {
    const tokens = normalized(query).split(' ').filter(Boolean);
    if (!tokens.length) return false;
    return matchesPrepared(prepared(row), tokens);
  }

  function scorePrepared(entry, wanted) {
    if (entry.name === wanted || entry.key === wanted) return 0;
    if (entry.name.startsWith(wanted)) return 1;
    if (entry.name.includes(wanted)) return 2;
    for (let i = 0; i < entry.incipits.length; i += 1) {
      if (entry.incipits[i].includes(wanted)) return 3;
    }
    for (let i = 0; i < entry.citations.length; i += 1) {
      if (entry.citations[i].includes(wanted)) return 4;
    }
    return 5;
  }

  function find(index, query) {
    if (!index || !Array.isArray(index.rows)) return [];
    const wanted = normalized(query);
    if (!wanted) return [];
    const tokens = wanted.split(' ');
    const results = [];
    for (let ordinal = 0; ordinal < index.rows.length; ordinal += 1) {
      const row = index.rows[ordinal];
      const entry = prepared(row);
      if (matchesPrepared(entry, tokens)) {
        results.push({ row: row, ordinal: ordinal, score: scorePrepared(entry, wanted) });
      }
    }
    return results.sort(function (left, right) {
      return left.score - right.score || left.ordinal - right.ordinal;
    });
  }

  function preview(row, query) {
    const wanted = normalized(query);
    const hits = [
      { value: row.fixed_date, label: 'Source fixed date' },
      ...(row.incipits || []).map(function (item) {
        return { value: item.text, label: item.slot + ' incipit' +
          (item.cycle ? ' · ' + item.cycle_family + ' ' + item.cycle : '') };
      }),
      ...(row.citations || []).map(function (item) {
        return { value: item.ref, label: item.slot + ' citation' +
          (item.cycle ? ' · ' + item.cycle_family + ' ' + item.cycle : '') };
      }),
      ...(row.witnesses || []).map(function (item) {
        return { value: item.label, label: item.lang + ' translation witness' };
      })
    ];
    return hits.find(function (hit) {
      return hit.value && normalized(hit.value).includes(wanted);
    }) || null;
  }

  function coverage(row) {
    const languages = row.coverage && row.coverage.languages || [];
    const language = function (code, label) {
      const item = languages.find(function (entry) { return entry.lang === code; });
      if (!item) return label + ': unassessed';
      const missing = Object.keys(item.availability || {}).filter(function (key) {
        return key !== 'available' && item.availability[key];
      }).map(function (key) { return item.availability[key] + ' ' + key.replace(/-/g, ' '); });
      return label + ': ' + item.available + '/' + item.occurrences + ' available' +
        (code === 'la' ? ' (' + item.exact_target + ' exact target)' : '') +
        (missing.length ? '; ' + missing.join(', ') : '');
    };
    const scripture = languages.find(function (entry) { return entry.lang === 'la'; });
    return 'Represented non-Scripture Proper units only. ' +
      language('la', 'Latin') + '. ' + language('en', 'English') +
      '. Scripture appointments: ' + (scripture && scripture.scripture_occurrences || 0) +
      ' (Bible text is separate from exact Missal wording).';
  }

  /* Formulary-list presentation. The order, the display season and each note
   * arrive with the data (`listing`, stamped by mass-propers; see
   * guidance/liturgy/roman-1962-propers.md § Reader list presentation). These
   * helpers only read them, so the web browse list, its search results and the
   * terminal reader show the same groups, marks and notes. */
  const LIST_MARKS = ['†', '‡', '§'];

  /** The season group a list shows an entry in: the stated list season, else its own. */
  function listSeason(entry) {
    return entry && (entry.listing && entry.listing.season || entry.season) || null;
  }

  /** The distinct notes a list's marked entries refer to, each with its mark, in list order. */
  function listNotes(entries) {
    const notes = [];
    (entries || []).forEach(function (entry) {
      const text = entry && entry.listing && entry.listing.note;
      if (!text || notes.some(function (note) { return note.text === text; })) return;
      notes.push({ mark: LIST_MARKS[notes.length] || '*'.repeat(notes.length + 1), text: text });
    });
    return notes;
  }

  /** The mark an entry carries among `notes`, or the empty string. */
  function listMark(entry, notes) {
    const text = entry && entry.listing && entry.listing.note;
    const note = text && (notes || []).find(function (one) { return one.text === text; });
    return note ? note.mark : '';
  }

  /** Write `notes` under a list and name them its description, or clear both. */
  function showListNotes(element, select, notes) {
    if (!element) return;
    element.textContent = (notes || []).map(function (note) {
      return note.mark + ' ' + note.text;
    }).join(' ');
    const empty = !(notes || []).length;
    element.hidden = empty;
    const wrap = element.parentElement && element.parentElement.classList.contains('formulary-notes-disclosure')
      ? element.parentElement : null;
    if (wrap) {
      wrap.hidden = empty;
      if (empty) wrap.open = false;
    }
    if (empty) select.removeAttribute('aria-describedby');
    else select.setAttribute('aria-describedby', element.id);
  }

  function mount(options) {
    const form = options.form;
    const input = options.input;
    const status = options.status;
    const results = options.results;
    const caveat = options.caveat;
    let serial = 0;

    function clear() {
      serial += 1;
      input.value = '';
      results.replaceChildren();
      caveat.textContent = '';
      caveat.hidden = true;
      status.textContent = 'Search the selected missal’s indexed titles, incipits, seasons, types, source fixed dates (MM-DD), Scripture citations, and public witness labels. Names are titles, not verified saint identities.';
    }

    async function run(event) {
      event.preventDefault();
      const edition = options.edition();
      const query = input.value.trim();
      const request = ++serial;
      results.replaceChildren();
      caveat.hidden = true;
      if (!query) {
        status.textContent = 'Enter a search term for the selected missal.';
        input.focus();
        return;
      }
      if (!edition || !options.structure(edition)) {
        status.textContent = 'Wait for the selected missal’s formulary list to load.';
        return;
      }
      status.textContent = 'Searching ' + options.editionLabel(edition) + '…';
      let index;
      try {
        index = await options.loadIndex(edition);
        if (!index || index.calendar !== edition || !Array.isArray(index.rows)) {
          throw new Error('the discovery index does not match the selected missal');
        }
      } catch (_error) {
        if (request !== serial || edition !== options.edition()) return;
        status.textContent = 'The selected missal’s discovery index could not be loaded. The browse list remains available.';
        return;
      }
      if (request !== serial || edition !== options.edition()) return;
      const context = options.recension(edition);
      if (context) {
        caveat.textContent = context;
        caveat.hidden = false;
      }
      const found = find(index, query);
      if (!found.length) {
        status.textContent = 'No results in ' + options.editionLabel(edition) +
          ' for “' + query + '”. Search covers indexed titles, incipits, seasons, types, source fixed dates, Scripture citations, and public witness labels; it does not resolve civil dates or saint identities.';
        return;
      }
      const shown = found.slice(0, LIMIT);
      status.textContent = 'Showing ' + shown.length + ' of ' + found.length +
        (found.length === 1 ? ' Mass in ' : ' Masses in ') + options.editionLabel(edition) +
        (found.length > LIMIT ? '. Refine your search to see more.' : '.');
      // Marks are the browse list's own: numbered over the whole edition.
      const notes = listNotes(index.rows);
      const list = document.createElement('ol');
      list.className = 'proper-search-results';
      shown.forEach(function (match) {
        const row = match.row;
        const item = document.createElement('li');
        const link = document.createElement('a');
        link.href = options.href(edition, row);
        link.textContent = row.name + (row.form_name ? ' · ' + row.form_name : '');
        link.addEventListener('click', function (click) {
          if (click.button !== 0 || click.metaKey || click.ctrlKey || click.altKey || click.shiftKey) return;
          click.preventDefault();
          options.select(edition, row);
        });
        const mark = listMark(row, notes);
        if (mark) link.textContent += ' ' + mark;
        item.appendChild(link);
        const identity = document.createElement('span');
        identity.className = 'proper-search-identity';
        const kindLabel = row.kind ? row.kind.charAt(0).toUpperCase() + row.kind.slice(1).replace(/-/g, ' ') : '';
        identity.textContent = [index.edition_short, kindLabel,
          row.fixed_date ? 'Fixed ' + row.fixed_date : null,
          row.form_name ? row.form_name : null].filter(Boolean).join(' · ');
        item.appendChild(identity);
        const hit = preview(row, query);
        if (hit) {
          const line = document.createElement('span');
          line.className = 'proper-search-hit';
          line.textContent = hit.label + ': ' + hit.value;
          item.appendChild(line);
        }
        const extent = document.createElement('span');
        extent.className = 'proper-search-coverage';
        extent.textContent = coverage(row);
        item.appendChild(extent);
        if (mark) {
          const note = document.createElement('span');
          note.className = 'proper-search-coverage proper-search-note';
          note.textContent = mark + ' ' + row.listing.note;
          item.appendChild(note);
        }
        list.appendChild(item);
      });
      results.appendChild(list);
    }

    form.addEventListener('submit', run);
    clear();
    return Object.freeze({ clear: clear });
  }

  return Object.freeze({ normalized: normalized, matches: matches, find: find,
    coverage: coverage, listSeason: listSeason, listNotes: listNotes, listMark: listMark,
    showListNotes: showListNotes, mount: mount });
});
