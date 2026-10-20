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

  function fieldText(row) {
    return [row.name, row.key, row.kind, row.season, row.fixed_date,
      row.form_name, row.form_id]
      .concat((row.incipits || []).map(function (item) { return item.text; }))
      .concat((row.citations || []).map(function (item) { return item.ref; }))
      .concat((row.witnesses || []).flatMap(function (item) { return [item.label, item.id]; }))
      .map(normalized).join(' ');
  }

  function matches(row, query) {
    const tokens = normalized(query).split(' ').filter(Boolean);
    if (!tokens.length) return false;
    const fields = fieldText(row);
    return tokens.every(function (token) { return fields.includes(token); });
  }

  function score(row, query) {
    const wanted = normalized(query);
    const name = normalized(row.name);
    if (name === wanted || normalized(row.key) === wanted) return 0;
    if (name.startsWith(wanted)) return 1;
    if (name.includes(wanted)) return 2;
    if ((row.incipits || []).some(function (item) { return normalized(item.text).includes(wanted); })) return 3;
    if ((row.citations || []).some(function (item) { return normalized(item.ref).includes(wanted); })) return 4;
    return 5;
  }

  function find(index, query) {
    if (!index || !Array.isArray(index.rows) || !normalized(query)) return [];
    return index.rows.map(function (row, ordinal) {
      return { row: row, ordinal: ordinal, score: score(row, query) };
    }).filter(function (result) { return matches(result.row, query); })
      .sort(function (left, right) {
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
        ' form-qualified results in ' + options.editionLabel(edition) +
        (found.length > LIMIT ? '. Refine the search to see other results.' : '.');
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
        item.appendChild(link);
        const identity = document.createElement('span');
        identity.className = 'proper-search-identity';
        identity.textContent = [index.edition_short, row.kind, row.key,
          'form ' + row.form_id].join(' · ');
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
        list.appendChild(item);
      });
      results.appendChild(list);
    }

    form.addEventListener('submit', run);
    clear();
    return Object.freeze({ clear: clear });
  }

  return Object.freeze({ normalized: normalized, matches: matches, find: find,
    coverage: coverage, mount: mount });
});
