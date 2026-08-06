(function () {
  'use strict';

  const root = document.querySelector('[data-visual-reset]');
  if (!root) return;

  const DIRECTIONS = new Set(['folio', 'instrument', 'reader']);
  const requested = new URL(window.location.href).searchParams.get('design');
  const design = DIRECTIONS.has(requested) ? requested : 'folio';
  root.dataset.design = design;
  document.documentElement.dataset.readerDesign = design;

  const ICONS = {
    calendar: '<rect x="3.5" y="5" width="17" height="15" rx="2"/><path d="M7.5 3v4M16.5 3v4M3.5 9.5h17"/><path d="M8 13h.01M12 13h.01M16 13h.01M8 16.5h.01M12 16.5h.01"/>',
    browse: '<circle cx="10.5" cy="10.5" r="6.5"/><path d="m15.5 15.5 5 5M8 8.5h5M8 11.5h4"/>',
    contents: '<path d="M9 6h11M9 12h11M9 18h11"/><circle cx="4.5" cy="6" r="1"/><circle cx="4.5" cy="12" r="1"/><circle cx="4.5" cy="18" r="1"/>',
    mode: '<rect x="3" y="4" width="18" height="16" rx="3"/><path d="M8 8h8M8 12h8M8 16h5"/>',
    details: '<circle cx="12" cy="12" r="9"/><path d="M12 10.5V17M12 7.2h.01"/>',
    close: '<path d="m6 6 12 12M18 6 6 18"/>',
    previous: '<path d="m15 18-6-6 6-6"/>',
    next: '<path d="m9 18 6-6-6-6"/>',
    search: '<circle cx="10.5" cy="10.5" r="6.5"/><path d="m15.5 15.5 5 5"/>'
  };

  function icon(name) {
    const svg = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
    svg.setAttribute('viewBox', '0 0 24 24');
    svg.setAttribute('focusable', 'false');
    svg.setAttribute('aria-hidden', 'true');
    svg.classList.add('reader-icon');
    svg.innerHTML = ICONS[name] || ICONS.details;
    return svg;
  }

  root.querySelectorAll('[data-icon]').forEach(function (control) {
    const host = control.querySelector('.action-mark, [aria-hidden="true"]');
    if (host) host.replaceChildren(icon(control.dataset.icon));
  });
  root.querySelectorAll('[data-icon-host]').forEach(function (host) {
    host.replaceChildren(icon(host.dataset.iconHost));
  });

  const context = root.querySelector('.reader-context');
  const visualMode = root.querySelector('[data-visual-mode]');
  if (context) {
    const syncMode = function () {
      const parts = context.textContent.split('·');
      const mode = (parts[1] || 'Read').trim();
      root.dataset.readerMode = mode.toLocaleLowerCase();
      if (visualMode) visualMode.textContent = mode;
    };
    new MutationObserver(syncMode).observe(context, { childList: true, characterData: true, subtree: true });
    syncMode();
  }

  const progress = root.querySelector('[data-visual-progress]');
  const reading = root.querySelector('#reader-document');
  const coverageNotice = root.querySelector('#coverage-notice');
  let semanticCurrent = null;
  let semanticCount = 0;
  let progressQueued = false;

  function semanticNodes() {
    return Array.from(reading.querySelectorAll(
      '[data-reader-event], [data-semantic-id], .proper-name, .ordinary-division'
    )).filter(function (node, index, nodes) {
      return index === 0 || node !== nodes[index - 1];
    });
  }

  function updateProgress() {
    progressQueued = false;
    const nodes = semanticNodes();
    semanticCount = nodes.length;
    let active = 0;
    const masthead = root.querySelector('.reader-masthead');
    const threshold = (masthead ? masthead.getBoundingClientRect().bottom : 0) + 24;
    nodes.forEach(function (node, index) {
      if (node.getBoundingClientRect().top <= threshold) active = index;
    });
    semanticCurrent = nodes[active] || null;
    if (progress) progress.style.inlineSize = nodes.length
      ? String(((active + 1) / nodes.length) * 100) + '%'
      : '0%';
    root.dataset.semanticProgress = nodes.length ? String(active + 1) + '/' + String(nodes.length) : '0/0';
  }

  function queueProgress() {
    if (progressQueued) return;
    progressQueued = true;
    requestAnimationFrame(updateProgress);
  }

  /*
   * The production renderers own every word and every absence. Instrument only
   * composes those existing nodes so one truthful status leads into the held
   * rite instead of repeating visually dominant warning bars. The guards make
   * this idempotent across renderer-owned replacement and render races.
   */
  function normalizeInstrumentCoverage() {
    if (design !== 'instrument') return;

    const uncompiled = reading.querySelector(':scope > .uncompiled');
    if (uncompiled && coverageNotice) {
      coverageNotice.replaceChildren(...uncompiled.childNodes);
      coverageNotice.hidden = false;
      uncompiled.remove();
    }

    reading.querySelectorAll('.ordinary-element').forEach(function (element) {
      const notices = Array.from(element.children).filter(function (child) {
        return child.classList.contains('notice');
      });
      if (!notices.length || element.querySelector(':scope > .ordinary-absence-inline')) return;
      const group = document.createElement('div');
      group.className = 'ordinary-absence-inline';
      element.insertBefore(group, notices[0]);
      notices.forEach(function (notice) { group.appendChild(notice); });
    });
  }

  window.addEventListener('scroll', queueProgress, { passive: true });
  window.addEventListener('resize', queueProgress);
  new MutationObserver(function () {
    normalizeInstrumentCoverage();
    queueProgress();
  }).observe(reading, { childList: true, subtree: true });
  normalizeInstrumentCoverage();
  queueProgress();

  const formulary = document.getElementById('reader-formulary');
  const filter = document.getElementById('formulary-filter');
  const results = root.querySelector('[data-browse-results]');
  let browseQueued = false;

  function updateBrowseResults() {
    browseQueued = false;
    if (!formulary || !filter || !results) return;
    const query = filter.value.trim().toLocaleLowerCase();
    const options = Array.from(formulary.options).filter(function (option) {
      return option.value && (!query || option.textContent.toLocaleLowerCase().includes(query));
    });
    results.replaceChildren();
    if (!options.length) {
      const empty = document.createElement('p');
      empty.className = 'browse-empty';
      empty.textContent = query ? 'No held title matches this filter.' : 'Choose an edition and collection to see its held titles.';
      results.appendChild(empty);
      return;
    }
    const list = document.createElement('div');
    list.className = 'browse-result-list';
    options.slice(0, 14).forEach(function (option) {
      const button = document.createElement('button');
      button.type = 'button';
      button.className = 'browse-result';
      button.dataset.value = option.value;
      button.setAttribute('aria-pressed', String(option.value === formulary.value));
      const title = document.createElement('span');
      title.textContent = option.textContent;
      const cue = document.createElement('span');
      cue.textContent = option.value === formulary.value ? 'Selected' : 'Choose';
      button.append(title, cue);
      button.addEventListener('click', function () {
        formulary.value = option.value;
        formulary.dispatchEvent(new Event('change', { bubbles: true }));
        updateBrowseResults();
      });
      list.appendChild(button);
    });
    results.appendChild(list);
    if (options.length > 14) {
      const count = document.createElement('p');
      count.className = 'browse-count';
      count.textContent = String(options.length - 14) + ' more titles — refine the filter to narrow the list.';
      results.appendChild(count);
    }
  }

  function queueBrowseResults() {
    if (browseQueued) return;
    browseQueued = true;
    queueMicrotask(updateBrowseResults);
  }
  if (formulary && filter && results) {
    filter.addEventListener('input', queueBrowseResults);
    formulary.addEventListener('change', queueBrowseResults);
    new MutationObserver(queueBrowseResults).observe(formulary, { childList: true });
    queueBrowseResults();
  }

  window.readerVisualResetDebug = {
    design: design,
    requestedDesign: requested,
    entrance: root.dataset.entrance,
    get semanticCurrent() {
      return semanticCurrent && (semanticCurrent.dataset.readerEvent ||
        semanticCurrent.dataset.semanticId || semanticCurrent.id || semanticCurrent.textContent.trim());
    },
    get semanticCount() { return semanticCount; }
  };
}());
