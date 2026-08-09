/* REVIEW ONLY, NOT PRODUCTION: preserves generated data, controllers, and
 * content targets; may add/relabel links and use ordinary Contents fragment
 * navigation; makes no requests or history/storage writes. Durable work
 * belongs at the owning generator and controller seams. */
(() => {
  'use strict';
  const html = document.documentElement;
  if (html.hasAttribute('data-corpus-wave1') || html.hasAttribute('data-corpus-wave1-pending'))
    return;
  html.setAttribute('data-corpus-wave1-pending', '');
  const DOMAINS = {
    home: 'Corpus',
    publications: 'Publications',
    reader: 'Publications',
    catena: 'Commentary',
    sources: 'Source Library'
  };
  const CORPUS_DESTINATIONS = [
    ['Publications', 'texts/', 'publications'], ['Sources', 'sources/', 'sources'],
    ['Scripture', 'scripture/', 'scripture'], ['Liturgy', 'liturgy/', 'liturgy'],
    ['History', 'history/', 'history'], ['Law', 'law/', 'law'], ['Commentary', 'catena/', 'catena']
  ];
  const READING_LABELS = {
    publications: 'Publication results',
    catena: 'Scripture and commentary',
    sources: 'Source Library results and passage'
  };
  const READING_PRIMARY = {publications: 'publication-results', sources: 'source-primary'};
  function normalizedPath(value) {
    return String(value || '').replace(/\/index\.html$/, '/');
  }
  function routeOf(anchor) {
    try {
      return normalizedPath(new URL(anchor.href, window.location.href).pathname);
    } catch (_error) {
      return '';
    }
  }
  function isPublicationsRoute(anchor) {
    return /\/texts\/$/.test(routeOf(anchor));
  }
  function detectSurface() {
    const main = document.querySelector('main#main-content');
    const scope = main || document.body;
    const path = normalizedPath(window.location.pathname);
    if (scope?.matches('.page-reader') || /\/web\/(?:gpt|claude)\/.+\.html$/.test(path)) {
      return 'reader';
    }
    if (scope?.matches('.texts-page') || document.body.matches('.texts-page') ||
        /\/texts\/$/.test(path))
      return 'publications';
    if (scope?.matches('.catena-page') || document.body.matches('.catena-page') ||
        /\/catena\/$/.test(path))
      return 'catena';
    if (scope?.matches('.sources-page') || document.body.matches('.sources-page') ||
        /\/sources\/$/.test(path))
      return 'sources';
    if (scope?.matches('.page-home')) return 'home';
    return null;
  }
  function element(tag, className, text) {
    const node = document.createElement(tag);
    if (className) node.className = className;
    if (text !== undefined) node.textContent = text;
    return node;
  }
  function technicalRecord(className, hook, value) {
    const disclosure = element('details', `wave-technical-record ${className || ''}`.trim());
    disclosure.setAttribute(hook, value || '');
    disclosure.appendChild(
        element('summary', 'wave-technical-record-summary', 'Technical publication record'));
    const body = element('div', 'wave-technical-record-body');
    disclosure.appendChild(body);
    return {disclosure, body};
  }
  function setOwnText(node, text) {
    if (!node) return;
    const held = [...node.childNodes].find(
        (child) => child.nodeType === Node.TEXT_NODE && child.nodeValue.trim());
    if (held)
      held.nodeValue = text;
    else
      node.appendChild(document.createTextNode(text));
  }
  function siteRoot() {
    const home = document.querySelector('.site-header .brand a[href]');
    if (home) return new URL('.', home.href);
    return new URL('.', window.location.href);
  }
  function localRoute(relative) {
    return new URL(relative, siteRoot()).href;
  }
  function copyLink(anchor) {
    const copy = element('a', 'wave-dialog-link', anchor.textContent.trim());
    copy.href = anchor.href;
    if (anchor.hasAttribute('aria-current')) {
      copy.setAttribute('aria-current', anchor.getAttribute('aria-current') || 'page');
    }
    return copy;
  }
  function destinationLinks(markCurrent = false) {
    const current = html.getAttribute('data-corpus-wave1') === 'reader' ?
        'publications' :
        html.getAttribute('data-corpus-wave1');
    return CORPUS_DESTINATIONS.map(([label, route, domain]) => {
      const anchor = element('a', '', label);
      anchor.href = localRoute(route);
      if (markCurrent && domain === current) anchor.setAttribute('aria-current', 'page');
      return anchor;
    });
  }
  function replacePublicationsLabels() {
    for (const anchor of document.querySelectorAll('a[href]')) {
      if (isPublicationsRoute(anchor) && anchor.textContent.trim() === 'Every Document') {
        anchor.textContent = 'Publications';
      }
    }
  }
  function markPrimary(node, kind) {
    if (!node) return;
    node.setAttribute('data-wave-primary', kind);
  }
  function objectLabel(parent, before, kind, tag = 'p') {
    if (!parent || !before || parent.querySelector(`:scope > [data-wave-object-label="${kind}"]`))
      return;
    const label = element(tag, 'wave-object-label', kind[0].toUpperCase() + kind.slice(1));
    label.setAttribute('data-wave-object-label', kind);
    parent.insertBefore(label, before);
  }
  function labelReadingMain(shell, surface) {
    const label = READING_LABELS[surface];
    if (!shell || !label) return;
    const reading = shell.querySelector(':scope > main#reading');
    if (!reading) return;
    reading.setAttribute('aria-label', label);
    if (READING_PRIMARY[surface]) markPrimary(reading, READING_PRIMARY[surface]);
    if (surface === 'catena') reading.setAttribute('data-wave-attached', 'commentary');
  }
  function wrapFilter(surface) {
    const form = document.querySelector('#controls');
    if (!form || form.closest('[data-wave-filter]')) return;
    const labels = {
      publications: 'Filter Publications',
      catena: 'Change chapter and commentary voice',
      sources: 'Filter Source Library'
    };
    if (!labels[surface]) return;
    const disclosure = element('details', 'wave-filter');
    disclosure.open = !window.matchMedia('(max-width: 64rem)').matches;
    disclosure.setAttribute('data-wave-filter', surface);
    const summary = element('summary', 'wave-filter-summary', labels[surface]);
    form.parentNode.insertBefore(disclosure, form);
    disclosure.append(summary, form);
    form.setAttribute('data-wave-filter-controls', '');
  }
  function makeList(anchors, className) {
    const list = element('ul', className);
    for (const anchor of anchors) {
      const item = element('li');
      item.appendChild(copyLink(anchor));
      list.appendChild(item);
    }
    return list;
  }
  function navigationList(anchors, label, className) {
    const nav = element('nav', 'wave-dialog-navigation');
    nav.setAttribute('aria-label', label);
    nav.appendChild(makeList(anchors, className));
    return nav;
  }
  function readerHeadings() {
    const reader = document.querySelector('[data-wave-reader-document]') ||
        document.querySelector('main.page-reader');
    if (!reader) return [];
    const seen = new Set();
    return [...reader.querySelectorAll('h2[id], h3[id], h4[id], h5[id], h6[id]')].filter(
        (heading) => {
          if (!heading.id || seen.has(heading.id)) return false;
          seen.add(heading.id);
          return true;
        });
  }
  function createDialog() {
    const existing = document.querySelector('dialog[data-wave-dialog-owner]');
    if (existing) return existing;
    const dialog = element('dialog', 'wave-dialog');
    dialog.id = 'corpus-wave1-dialog';
    dialog.setAttribute('data-wave-dialog-owner', '');
    dialog.setAttribute('data-wave-dialog', '');
    dialog.setAttribute('aria-labelledby', 'corpus-wave1-dialog-title');
    const frame = element('div', 'wave-dialog-frame');
    const header = element('header', 'wave-dialog-header');
    const title = element('h2', 'wave-dialog-title');
    title.id = 'corpus-wave1-dialog-title';
    const close = element('button', 'wave-dialog-close', 'Close');
    close.type = 'button';
    close.setAttribute('data-wave-close-dialog', '');
    const body = element('div', 'wave-dialog-body');
    body.setAttribute('data-wave-dialog-body', '');
    header.append(title, close);
    frame.append(header, body);
    dialog.appendChild(frame);
    document.body.appendChild(dialog);
    let session = null;
    let skipRestore = false;
    function closeDialog(restore = true) {
      if (!dialog.open) return;
      skipRestore = !restore;
      dialog.close();
    }
    function menuPanel() {
      return {
        title: 'Menu',
        node:
            navigationList(destinationLinks(true), 'Corpus menu', 'wave-dialog-list wave-menu-list')
      };
    }
    function jumpPanel() {
      const node = element('div', 'wave-jump');
      node.appendChild(element(
          'p', 'wave-dialog-note',
          'Quick destinations—not corpus search. This bounded list uses the corpus’s seven durable destinations.'));
      node.appendChild(navigationList(
          destinationLinks(true), 'Quick destinations', 'wave-dialog-list wave-jump-list'));
      return {title: 'Jump', node};
    }
    function contentsPanel() {
      const headings = readerHeadings();
      if (!headings.length) return null;
      let current = '';
      try {
        current = decodeURIComponent(window.location.hash.slice(1));
      } catch (_error) {
        current = '';
      }
      const list = element('ol', 'wave-dialog-list wave-contents-list');
      let section = null;
      let subsections = null;
      let branch = null;
      for (const heading of headings) {
        const item = element('li', 'wave-contents-item');
        const level = heading.tagName.slice(1);
        item.setAttribute('data-wave-heading-level', level);
        const anchor = element('a', 'wave-dialog-link', heading.textContent.trim());
        anchor.href = '#' + encodeURIComponent(heading.id);
        anchor.setAttribute('data-wave-contents-target', heading.id);
        if (heading.id === current) anchor.setAttribute('aria-current', 'location');
        item.appendChild(anchor);
        if (level === '2') {
          list.appendChild(item);
          section = item;
          subsections = null;
          branch = null;
          continue;
        }
        if (!subsections) {
          if (!section) {
            section = element('li', 'wave-contents-section');
            list.appendChild(section);
          }
          branch = element('details', 'wave-contents-branch');
          branch.appendChild(element('summary', 'wave-contents-summary', 'Subsections'));
          subsections = element('ol', 'wave-contents-subsections');
          branch.appendChild(subsections);
          section.appendChild(branch);
        }
        subsections.appendChild(item);
        if (heading.id === current) branch.open = true;
      }
      const nav = element('nav', 'wave-dialog-navigation');
      nav.setAttribute('aria-label', 'Publication contents');
      nav.appendChild(list);
      return {title: 'Contents', node: nav};
    }
    const panels = {menu: menuPanel, jump: jumpPanel, contents: contentsPanel};
    function openDialog(kind, invoker) {
      const panel = panels[kind]?.();
      if (!panel || typeof dialog.showModal !== 'function') return;
      if (!dialog.open) {
        session = {invoker, scrollX: window.scrollX, scrollY: window.scrollY};
      } else if (invoker && !dialog.contains(invoker)) {
        session.invoker?.setAttribute('aria-expanded', 'false');
        session.invoker = invoker;
      }
      skipRestore = false;
      dialog.dataset.waveDialogView = kind;
      title.textContent = panel.title;
      body.replaceChildren(panel.node);
      document.querySelectorAll('[data-wave-open-dialog][aria-expanded="true"]')
          .forEach((button) => button.setAttribute('aria-expanded', 'false'));
      invoker?.setAttribute('aria-expanded', 'true');
      if (!dialog.open) dialog.showModal();
      const target =
          body.querySelector('a[href], button:not([disabled]), input:not([disabled])') || close;
      target.focus({preventScroll: true});
    }
    dialog.addEventListener('click', (event) => {
      const opener = event.target.closest('[data-wave-contents-target]');
      if (opener) {
        const target = document.getElementById(opener.dataset.waveContentsTarget);
        closeDialog(false);
        if (target) {
          window.setTimeout(() => {
            if (!target.hasAttribute('tabindex')) target.setAttribute('tabindex', '-1');
            target.focus({preventScroll: true});
          }, 0);
        }
        return;
      }
      if (event.target.closest('[data-wave-dialog-body] a[href]')) {
        closeDialog(false);
        return;
      }
      if (event.target.closest('[data-wave-close-dialog]')) {
        closeDialog(true);
        return;
      }
      if (event.target === dialog) {
        const box = frame.getBoundingClientRect();
        const outside = event.clientX < box.left || event.clientX > box.right ||
            event.clientY < box.top || event.clientY > box.bottom;
        if (outside) closeDialog(true);
      }
    });
    dialog.addEventListener('cancel', () => {
      skipRestore = false;
    });
    dialog.addEventListener('close', () => {
      document.querySelectorAll('[data-wave-open-dialog][aria-expanded="true"]')
          .forEach((button) => button.setAttribute('aria-expanded', 'false'));
      const held = session;
      session = null;
      dialog.removeAttribute('data-wave-dialog-view');
      if (skipRestore || !held) {
        skipRestore = false;
        return;
      }
      const fallback = document.querySelector('[data-wave-primary] h1, h1[data-wave-title], h1');
      const target =
          held.invoker?.isConnected && !held.invoker.closest('[hidden]') ? held.invoker : fallback;
      window.setTimeout(() => {
        if (target) {
          if (!target.matches('a, button, input, select, textarea, [tabindex]')) {
            target.setAttribute('tabindex', '-1');
          }
          target.focus({preventScroll: true});
        }
        window.scrollTo(held.scrollX, held.scrollY);
      }, 0);
    });
    dialog.openWavePanel = openDialog;
    return dialog;
  }
  function actionButton(label, kind) {
    const button = element('button', 'wave-action', label);
    button.type = 'button';
    button.setAttribute('data-wave-open-dialog', kind);
    button.setAttribute('data-wave-action', kind);
    button.setAttribute('aria-controls', 'corpus-wave1-dialog');
    button.setAttribute('aria-haspopup', 'dialog');
    button.setAttribute('aria-expanded', 'false');
    return button;
  }
  function enhanceShell(surface, dialog) {
    const header = document.querySelector('.site-header');
    const nav = header?.querySelector('nav');
    if (!header || !nav) return;
    const feedback = [...nav.querySelectorAll('a[href]')].find(
        (anchor) => /\/contributing\.html$/.test(routeOf(anchor)));
    if (feedback) feedback.hidden = true;
    header.setAttribute('data-wave-shell', '');
    nav.setAttribute('data-wave-desktop-nav', '');
    let publications = [...nav.querySelectorAll('a[href]')].find(isPublicationsRoute);
    if (!publications) {
      publications = element('a', '', 'Publications');
      publications.href = localRoute('texts/');
      const home =
          [...nav.querySelectorAll('a[href]')].find((anchor) => /\/$/.test(routeOf(anchor)));
      if (home?.nextSibling)
        nav.insertBefore(publications, home.nextSibling);
      else
        nav.appendChild(publications);
    }
    publications.setAttribute('data-wave-publications-link', '');
    if (surface === 'publications' || surface === 'reader') {
      nav.querySelectorAll('[aria-current]')
          .forEach((node) => node.removeAttribute('aria-current'));
      publications.setAttribute('aria-current', 'page');
    }
    if (!header.querySelector('[data-wave-domain]')) {
      const domain = element('span', 'wave-domain', DOMAINS[surface]);
      domain.setAttribute('data-wave-domain', surface);
      const brand = header.querySelector('.brand');
      if (brand?.nextSibling)
        header.insertBefore(domain, brand.nextSibling);
      else
        header.appendChild(domain);
    }
    if (!header.querySelector('[data-wave-shell-actions]')) {
      const actions = element('div', 'wave-shell-actions');
      actions.setAttribute('data-wave-shell-actions', '');
      actions.setAttribute('data-wave-actions', 'shell');
      actions.append(actionButton('Menu', 'menu'), actionButton('Jump', 'jump'));
      header.appendChild(actions);
    }
    document.addEventListener('click', (event) => {
      const button = event.target.closest('[data-wave-open-dialog]');
      if (!button || !button.isConnected) return;
      dialog.openWavePanel(button.dataset.waveOpenDialog, button);
    });
  }
  function enhanceHome(main) {
    markPrimary(main, 'home');
    main.querySelector('h1')?.setAttribute('data-wave-title', '');
    const headings = [...main.querySelectorAll('h2')];
    const tables = main.querySelectorAll('table');
    const portalTable = tables[0];
    const taskTable = tables[1];
    const taskHeading = headings.find((node) => node.textContent.trim() === 'Read in the browser');
    let portalHeading = headings.find((node) => node.textContent.trim() === 'Library');
    if (!portalTable || !taskTable || !taskHeading) return;
    portalTable.setAttribute('data-wave-portals', '');
    portalTable.setAttribute(
        'data-wave-portal-count', String(portalTable.tBodies[0]?.rows.length || 0));
    taskHeading.setAttribute('data-wave-home-tasks', '');
    setOwnText(taskHeading, 'Begin with a task');
    taskTable.setAttribute('data-wave-task-entrances', '');
    const taskRows = [...(taskTable.tBodies[0]?.rows || [])];
    const taskDefinitions = [
      ['liturgy/day.html', 'Read today', 'read-today'],
      ['texts/', 'Find a publication', 'find-publication'],
      ['sources/', 'Trace a source', 'trace-source'],
      ['catena/', 'Follow commentary', 'follow-commentary'],
      ['history/', 'See what changed', 'see-changes'], ['law/', 'Look up a canon', 'look-up-canon']
    ];
    const secondaryDefinitions = [['liturgy/', 'propers'], ['scripture/', 'story-of-salvation']];
    function rowFor(relative) {
      const wanted = normalizedPath(new URL(relative, siteRoot()).pathname);
      return taskRows.find((row) => {
        const anchor = row.querySelector('a[href]');
        return anchor && routeOf(anchor) === wanted;
      });
    }
    const selected =
        taskDefinitions.map(([route, label, hook]) => ({row: rowFor(route), label, hook}));
    const secondaryRows = secondaryDefinitions.map(([route, hook]) => ({row: rowFor(route), hook}));
    if (selected.some(({row}) => !row) || secondaryRows.some(({row}) => !row)) return;
    const headingsCells = taskTable.querySelectorAll('thead th');
    setOwnText(headingsCells[0], 'Task');
    setOwnText(headingsCells[1], 'Destination');
    for (const {row, label, hook} of selected) {
      const anchor = row.querySelector('a[href]');
      setOwnText(anchor, label);
      row.setAttribute('data-wave-task', hook);
      anchor?.setAttribute('data-wave-task-destination', hook);
      taskTable.tBodies[0].appendChild(row);
    }
    taskTable.setAttribute('data-wave-task-count', String(selected.length));
    const parent = portalTable.parentNode;
    if (!parent || taskHeading.parentNode !== parent || taskTable.parentNode !== parent) return;
    if (!portalHeading || portalHeading.parentNode !== parent) {
      portalHeading = element('h2', 'wave-home-portals-title', 'Seven editorial portals');
      parent.insertBefore(portalHeading, portalTable);
    } else {
      setOwnText(portalHeading, 'Seven editorial portals');
      portalHeading.classList.add('wave-home-portals-title');
    }
    portalHeading.setAttribute('data-wave-portals-title', '');
    const tasks = element('section', 'wave-home-task-section');
    tasks.setAttribute('data-wave-home-task-section', '');
    tasks.setAttribute('data-wave-task-count', String(selected.length));
    markPrimary(tasks, 'task-entrances');
    parent.insertBefore(tasks, portalHeading);
    tasks.append(taskHeading, taskTable);
    const portals = element('section', 'wave-home-portals');
    portals.setAttribute('data-wave-home-portals', '');
    parent.insertBefore(portals, portalHeading);
    let cursor = portalHeading;
    while (cursor) {
      const next = cursor.nextSibling;
      portals.appendChild(cursor);
      if (cursor === portalTable) break;
      cursor = next;
    }
    const secondary = element('details', 'wave-home-secondary');
    secondary.setAttribute('data-wave-secondary-entrances', '');
    secondary.setAttribute('data-wave-secondary-count', String(secondaryRows.length));
    secondary.appendChild(element('summary', 'wave-home-secondary-summary', 'More ways to browse'));
    const secondaryList = element('ul', 'wave-home-secondary-list');
    for (const {row, hook} of secondaryRows) {
      const item = element('li', 'wave-home-secondary-item');
      item.setAttribute('data-wave-secondary-route', hook);
      const cells = [...row.cells];
      for (const cell of cells) {
        const part = element('span', 'wave-home-secondary-part');
        while (cell.firstChild) part.appendChild(cell.firstChild);
        item.appendChild(part);
      }
      row.remove();
      secondaryList.appendChild(item);
    }
    secondary.appendChild(secondaryList);
    portals.insertAdjacentElement('afterend', secondary);
  }
  function enhancePublications(main) {
    const heading = main.querySelector('.page-header h1');
    setOwnText(heading, 'Publications');
    heading?.setAttribute('data-wave-title', '');
    const lede = main.querySelector('.page-header .lede');
    if (lede) {
      lede.textContent =
          'Browse every publication in the corpus. Filter by provider, subject, ' +
          'availability, or title, then open the publication or its canonical PDF.';
    }
    if (/^Every Document\b/.test(document.title)) {
      document.title = document.title.replace(/^Every Document\b/, 'Publications');
    }
    wrapFilter('publications');
    enhancePublicationTerminology();
    markPrimary(document.getElementById('reading'), 'publication-results');
    document.getElementById('detail')?.setAttribute('data-wave-details', 'publication');
  }
  function enhancePublicationTerminology() {
    const author = document.getElementById('author-select');
    const authorLabel = document.querySelector('label[for="author-select"]');
    setOwnText(authorLabel, 'Model');
    const firstAuthor = author?.querySelector('option:first-child');
    if (firstAuthor?.textContent.trim() === 'Any author') {
      firstAuthor.textContent = 'Any model';
    }
    const authorField = author?.closest('.field');
    if (authorField && !authorField.closest('[data-wave-provenance-filter]')) {
      const provenance = element('details', 'wave-provenance-filter');
      provenance.setAttribute('data-wave-provenance-filter', 'model');
      provenance.open = Boolean(author.value);
      provenance.appendChild(
          element('summary', 'wave-provenance-summary', 'Model details'));
      authorField.parentNode.insertBefore(provenance, authorField);
      provenance.appendChild(authorField);
    }
    const provenance = authorField?.closest('[data-wave-provenance-filter]');
    if (provenance && !provenance.hasAttribute('data-wave-provenance-initialized') &&
        author.options.length > 1) {
      provenance.open = Boolean(author.value);
      provenance.setAttribute('data-wave-provenance-initialized', '');
    }
    const editionLabel = document.querySelector('label[for="edition-select"]');
    setOwnText(editionLabel, 'Provider');
    const firstEdition = document.querySelector('#edition-select option:first-child');
    if (firstEdition?.textContent.trim() === 'Both editions') {
      firstEdition.textContent = 'All providers';
    }
    const explanation = [...document.querySelectorAll('.page-footer p')].find(
        (node) => /^A work\b/.test(node.textContent.trim()) && /\bedition\b/i.test(node.textContent));
    if (explanation && !explanation.hasAttribute('data-wave-publication-terms')) {
      explanation.textContent =
          'A work is one subject. Each independently produced treatment remains a separate ' +
          'publication, and its available browser and PDF formats remain attached to that treatment.';
      explanation.setAttribute('data-wave-publication-terms', '');
    }
    const banner = document.querySelector('.release-banner[aria-label="Edition status"]');
    banner?.setAttribute('aria-label', 'Release status');
    const detailSub = document.querySelector('#detail .detail-sub');
    const detailIdentity = detailSub?.textContent.trim().match(/^(.+?) edition of (.+)$/);
    if (detailIdentity && !detailSub.hasAttribute('data-wave-treatment-kind')) {
      detailSub.textContent = 'Independent treatment';
      detailSub.setAttribute('data-wave-treatment-kind', 'independent');
      const provider = element(
          'p', 'detail-sub wave-detail-provider', 'Provider · ' + detailIdentity[1]);
      provider.setAttribute('data-wave-meta', 'provider');
      const work = element('p', 'detail-sub wave-detail-work', 'Work · ' + detailIdentity[2]);
      work.setAttribute('data-wave-meta', 'work');
      detailSub.insertAdjacentElement('afterend', work);
      detailSub.insertAdjacentElement('afterend', provider);
    }
    for (const heading of document.querySelectorAll('#detail .detail-heading')) {
      if (heading.textContent.trim() === 'Authorship') {
        heading.textContent = 'Provider and model';
        heading.setAttribute('data-wave-evidence', 'model-provenance');
      }
    }
    const detail = document.querySelector('#detail:not([hidden])');
    const issues = [...(detail?.querySelectorAll(':scope > .detail-heading') || [])].find(
        (node) => node.textContent.trim() === 'Issues');
    if (detail && issues && !detail.querySelector(':scope > [data-wave-technical-record]')) {
      const record = technicalRecord('', 'data-wave-technical-record', 'publication');
      const technical = record.disclosure;
      const body = record.body;
      body.setAttribute('data-wave-technical-record-body', 'publication');
      detail.insertBefore(technical, issues);
      let cursor = technical.nextSibling;
      while (cursor) {
        const next = cursor.nextSibling;
        body.appendChild(cursor);
        cursor = next;
      }
    }
    const detailRoot = document.getElementById('detail');
    if (detailRoot?.hidden) detailRoot.removeAttribute('data-wave-detail-focus');
    if (detail && !detail.hasAttribute('data-wave-detail-focus')) {
      const trigger = document.querySelector('.edition-title[aria-expanded="true"]');
      const close = detail.querySelector('.detail-close');
      const target = close || detail.querySelector('h2');
      detail.setAttribute('data-wave-detail-focus', 'moved');
      target?.setAttribute('data-wave-detail-focus-target', '');
      if (target && !target.matches('button, a, [tabindex]')) target.tabIndex = -1;
      target?.focus({preventScroll: true});
      if (close && trigger) {
        close.setAttribute('data-wave-detail-close', '');
        trigger.setAttribute('data-wave-detail-return', '');
        close.addEventListener('click', () => window.setTimeout(() => {
          if (trigger.isConnected) trigger.focus({preventScroll: true});
        }, 0), {once: true});
      }
    }
  }

  function decoratePublicationConstraints() {
    const filter = document.querySelector('[data-wave-filter="publications"]');
    const form = document.getElementById('controls');
    const find = document.getElementById('find-input');
    if (!filter || !form || !find) return;
    const active = [];
    if (find.value.trim()) active.push(`Find “${find.value.trim()}”`);
    for (const id of ['author-select', 'edition-select', 'section-select', 'reading-select']) {
      const control = document.getElementById(id);
      if (!control?.value) continue;
      const label = document.querySelector(`label[for="${id}"]`)?.textContent.trim() || id;
      const value = control.selectedOptions[0]?.textContent.trim() || control.value;
      active.push(`${label}: ${value}`);
    }
    const sort = document.getElementById('sort-select');
    if (sort?.value && sort.value !== 'section') {
      active.push(`Sort: ${sort.selectedOptions[0]?.textContent.trim() || sort.value}`);
    }
    let summary = document.querySelector('[data-wave-active-constraints]');
    if (!active.length) {
      summary?.remove();
      return;
    }
    if (!summary) {
      summary = element('div', 'wave-active-constraints');
      summary.setAttribute('data-wave-active-constraints', 'publications');
      summary.style.order = '4';
      const text = element('p');
      text.setAttribute('data-wave-active-constraints-text', '');
      const clear = element('button', 'wave-clear-constraints', 'Clear filters');
      clear.type = 'button';
      clear.setAttribute('data-wave-clear-constraints', '');
      clear.addEventListener('click', () => {
        form.reset();
        find.dispatchEvent(new InputEvent('input', {bubbles: true, inputType: 'deleteContent'}));
        find.focus({preventScroll: true});
      });
      summary.append(text, clear);
      filter.insertAdjacentElement('afterend', summary);
    }
    const text = summary.querySelector('[data-wave-active-constraints-text]');
    const value = 'Active filters · ' + active.join(' · ');
    if (text && text.textContent !== value) text.textContent = value;
  }
  function readerRecord() {
    return {
      provider: html.dataset.waveRecordProvider || '',
      providerLabel: html.dataset.waveRecordProviderLabel || '',
      pdf: html.dataset.waveRecordPdf || '',
      parallelWeb: html.dataset.waveRecordParallelWeb || '',
      parallelLabel: html.dataset.waveRecordParallelLabel || ''
    };
  }
  function recordedLocalHref(value, suffix) {
    if (!value) return '';
    try {
      const target = new URL(value, siteRoot());
      if (target.origin !== window.location.origin ||
          target.protocol !== window.location.protocol) {
        return '';
      }
      if (suffix && !target.pathname.endsWith(suffix)) return '';
      return target.href;
    } catch (_error) {
      return '';
    }
  }
  function wrapReaderTables(article) {
    for (const table of article.querySelectorAll('table')) {
      if (table.parentElement?.hasAttribute('data-wave-table-scroll')) continue;
      const caption = table.caption?.textContent.replace(/\s+/g, ' ').trim();
      let nearbyHeading = '';
      if (!caption) {
        for (const heading of article.querySelectorAll('h2, h3, h4, h5, h6')) {
          if (!(heading.compareDocumentPosition(table) & Node.DOCUMENT_POSITION_FOLLOWING)) {
            break;
          }
          nearbyHeading = heading.textContent.replace(/\s+/g, ' ').trim();
        }
      }
      const label = caption || nearbyHeading;
      const scroll = element('div', 'wave-reader-table-scroll');
      scroll.setAttribute('data-wave-table-scroll', '');
      scroll.tabIndex = 0;
      scroll.setAttribute('role', 'region');
      scroll.setAttribute('aria-label', label ? `Scrollable table: ${label}` : 'Scrollable table');
      table.parentNode.insertBefore(scroll, table);
      scroll.appendChild(table);
    }
  }
  function restoreReaderFragment() {
    const hash = window.location.hash;
    if (!hash || hash === '#' || html.dataset.waveReaderFragmentRestored === hash) return;
    let id;
    try {
      id = decodeURIComponent(hash.slice(1));
    } catch (_error) {
      id = hash.slice(1);
    }
    const target = document.getElementById(id);
    if (!target) return;
    html.dataset.waveReaderFragmentRestored = hash;
    const queueScroll = () => window.requestAnimationFrame(() => {
      window.requestAnimationFrame(() => {
        if (window.location.hash === hash && target.isConnected) {
          const scrollBehavior = html.style.scrollBehavior;
          html.style.scrollBehavior = 'auto';
          target.scrollIntoView({block: 'start', inline: 'nearest'});
          html.style.scrollBehavior = scrollBehavior;
        }
      });
    });
    if (document.readyState === 'complete')
      queueScroll();
    else
      window.addEventListener('load', queueScroll, {once: true});
  }
  function enhanceReader(main) {
    const library = [...main.querySelectorAll(':scope > .breadcrumb a[href]')].find(
        (anchor) => anchor.textContent.trim() === 'Library');
    if (library) {
      library.textContent = 'Publications';
      library.href = localRoute('texts/');
      library.setAttribute('data-wave-publications-link', '');
    }
    let article = main.querySelector(':scope > [data-wave-reader-document]');
    if (!article) {
      article = element('article', 'wave-reader-document reader-document');
      article.setAttribute('data-wave-reader-document', '');
      const breadcrumb = main.querySelector(':scope > .breadcrumb');
      const content = [...main.childNodes].filter((node) => node !== breadcrumb);
      if (breadcrumb?.nextSibling)
        main.insertBefore(article, breadcrumb.nextSibling);
      else
        main.appendChild(article);
      article.append(...content);
    }
    article.classList.add('reader-document');
    markPrimary(article, 'reader-prose');
    wrapReaderTables(article);
    const title = article.querySelector('h1');
    if (!title) return;
    title.setAttribute('data-wave-title', '');
    const record = readerRecord();
    let treatment = article.querySelector('[data-wave-treatment-kind]');
    let provider = article.querySelector('[data-wave-provider]');
    if (record.provider && record.providerLabel && !provider) {
      treatment = element('p', 'wave-reader-treatment', 'Independent treatment');
      treatment.setAttribute('data-wave-treatment-kind', 'independent');
      provider = element('p', 'wave-reader-provider', 'Provider · ' + record.providerLabel);
      provider.setAttribute('data-wave-provider', record.provider);
      provider.setAttribute('data-wave-meta', 'provider');
      article.insertBefore(treatment, title);
      article.insertBefore(provider, title);
    }
    const possibleSubtitle = title.nextElementSibling;
    if (possibleSubtitle?.matches('p') && possibleSubtitle.querySelector(':scope > em')) {
      possibleSubtitle.setAttribute('data-wave-subtitle', '');
    }
    let readerHeading = article.querySelector(':scope > [data-wave-reader-heading]');
    if (!readerHeading) {
      readerHeading = element('header', 'wave-reader-heading reader-heading');
      readerHeading.setAttribute('data-wave-reader-heading', '');
      const first = treatment || provider || title;
      article.insertBefore(readerHeading, first);
      if (treatment) readerHeading.appendChild(treatment);
      if (provider) readerHeading.appendChild(provider);
      readerHeading.appendChild(title);
      if (possibleSubtitle?.hasAttribute('data-wave-subtitle')) {
        readerHeading.appendChild(possibleSubtitle);
      }
    }
    let colophon = article.querySelector(':scope > [data-wave-object="colophon"]');
    if (!colophon) {
      const revised = [...article.querySelectorAll(':scope > p')].find(
          (node) => /^Last revised \(UTC\):/.test(node.textContent.trim()));
      const rights = revised?.nextElementSibling;
      if (revised && rights && /^Reuse and rights\./.test(rights.textContent.trim())) {
        colophon = element('section', 'wave-reader-colophon');
        colophon.id = 'revision-and-rights';
        colophon.setAttribute('data-wave-object', 'colophon');
        revised.parentNode.insertBefore(colophon, revised);
        colophon.append(revised, rights);
      }
    }
    if (colophon) {
      while (colophon.nextSibling) {
        article.insertBefore(colophon.nextSibling, colophon);
      }
      colophon.setAttribute('data-wave-terminal-colophon', '');
    }
    restoreReaderFragment();
    if (article.querySelector('[data-wave-reader-actions]')) return;
    const actions = element('div', 'wave-reader-actions');
    actions.setAttribute('data-wave-reader-actions', '');
    actions.setAttribute('data-wave-actions', 'reader');
    if (readerHeadings().length) actions.appendChild(actionButton('Contents', 'contents'));
    const pdfHref = recordedLocalHref(record.pdf, '.pdf');
    if (pdfHref) {
      const pdf = element('a', 'wave-action wave-action-primary', 'Canonical PDF');
      pdf.href = pdfHref;
      pdf.setAttribute('data-wave-pdf', 'recorded');
      pdf.setAttribute('data-wave-action', 'pdf');
      actions.appendChild(pdf);
    }
    const parallelHref = recordedLocalHref(record.parallelWeb, '.html');
    if (parallelHref && record.parallelLabel) {
      const parallel = element('a', 'wave-action wave-action-secondary', 'Parallel treatment');
      parallel.href = parallelHref;
      parallel.title = 'Provider · ' + record.parallelLabel;
      parallel.setAttribute('aria-label', 'Parallel treatment, provider ' + record.parallelLabel);
      parallel.setAttribute('data-wave-parallel', 'recorded-sibling');
      parallel.setAttribute('data-wave-action', 'parallel');
      actions.appendChild(parallel);
    }
    if (colophon) {
      const revision = element('a', 'wave-action wave-action-secondary', 'Revision and rights');
      revision.href = '#' + colophon.id;
      revision.setAttribute('data-wave-action', 'colophon');
      actions.appendChild(revision);
    }
    const after = readerHeading.querySelector('[data-wave-subtitle]') || title;
    after.insertAdjacentElement('afterend', actions);
  }
  function decoratePublications() {
    enhancePublicationTerminology();
    decoratePublicationConstraints();
    const works = [...document.querySelectorAll('#reading .work')];
    works[0]?.setAttribute('data-wave-primary', 'first-publication');
    for (const work of works) {
      work.setAttribute('data-wave-object', 'work');
      const providers = new Set();
      for (const edition of work.querySelectorAll(':scope .edition')) {
        edition.setAttribute('data-wave-object', 'treatment');
        const models = [...edition.querySelectorAll(':scope > .edition-meta .pill-model')];
        const absent = [...edition.querySelectorAll(':scope > .edition-meta .pill-absent')].find(
            (node) => node.textContent.trim() === 'authorship not stated');
        if (absent) absent.textContent = 'contribution provenance not stated';
        const provenance = absent ? [...models, absent] : models;
        if (provenance.length) {
          let technical = edition.querySelector(':scope > [data-wave-card-technical-record]');
          if (!technical) {
            technical =
                technicalRecord('wave-card-technical-record', 'data-wave-card-technical-record')
                    .disclosure;
            edition.querySelector(':scope > .edition-meta')
                ?.insertAdjacentElement('afterend', technical);
          }
          for (const model of provenance) {
            model.setAttribute('data-wave-provenance-deferred', '');
            technical.appendChild(model);
          }
        }
        const key = edition.getAttribute('data-key') || '';
        const providerId = key.includes('|') ? key.split('|').pop() : '';
        if (providerId) providers.add(providerId);
        const mark = edition.querySelector('.edition-mark');
        if (mark && !mark.hasAttribute('data-wave-treatment-kind')) {
          const raw = mark.textContent.trim();
          mark.textContent = 'Independent treatment';
          mark.setAttribute('data-wave-treatment-kind', 'independent');
          const provider = element('span', 'wave-treatment-provider', 'Provider · ' + raw);
          if (providerId) provider.setAttribute('data-wave-provider', providerId);
          mark.insertAdjacentElement('afterend', provider);
        }
        const title = edition.querySelector(':scope > .edition-head .edition-title');
        if (title && title.parentElement?.firstElementChild !== title) {
          title.parentElement.insertBefore(title, title.parentElement.firstElementChild);
        }
      }
      if (providers.size > 1 && !work.querySelector('[data-wave-parallel]')) {
        const label = element('p', 'wave-parallel-label', 'Parallel treatment');
        label.setAttribute('data-wave-parallel', 'same-work');
        const first = work.querySelector(':scope > .edition');
        if (first) work.insertBefore(label, first);
      }
    }
  }
  function enhanceCatena() {
    wrapFilter('catena');
    document.getElementById('reading')?.setAttribute('data-wave-attached', 'commentary');
    document.querySelector('.page-header h1')?.setAttribute('data-wave-title', '');
  }
  function decorateCatena() {
    const chapter = document.querySelector('.chapter');
    chapter?.setAttribute('data-wave-scripture', 'anchor');
    markPrimary(chapter, 'scripture-text');
    const chapterBody = chapter?.querySelector(':scope > details.chapter-body');
    if (chapterBody && !chapterBody.open) chapterBody.open = true;
    const chain = document.querySelector('#reading .chain');
    chain?.setAttribute('data-wave-attached', 'commentary');
    const firstAuthor = chain?.querySelector('details.author-body');
    if (firstAuthor && !firstAuthor.hasAttribute('data-wave-default-open')) {
      firstAuthor.open = true;
      firstAuthor.setAttribute('data-wave-default-open', '');
    }
    const authorFilter = document.querySelector('#reading .author-filter');
    if (authorFilter && !authorFilter.closest('[data-wave-author-filter]')) {
      const disclosure = element('details', 'wave-author-filter');
      disclosure.setAttribute('data-wave-author-filter', '');
      disclosure.appendChild(element('summary', 'wave-author-filter-summary', 'Filter authors'));
      authorFilter.parentNode.insertBefore(disclosure, authorFilter);
      disclosure.appendChild(authorFilter);
    }
    for (const fragment of document.querySelectorAll('.fragment')) {
      fragment.setAttribute('data-wave-object', 'commentary-passage');
      fragment.querySelector('.fragment-extent')?.setAttribute('data-wave-scripture-extent', '');
      fragment.querySelector('.fragment-body')?.setAttribute('data-wave-disclosure', 'commentary');
    }
    for (const link of document.querySelectorAll('a.fragment-whole')) {
      if (!link.hasAttribute('data-wave-relation')) {
        link.textContent = 'Open this passage in the Source Library';
        link.setAttribute('data-wave-relation', 'passage-in-source-library');
      }
    }
    const evidence = [
      ['.absence-note', 'translation-absence'],
      ['.aside:has(.lead-list)', 'acquisition-leads'],
      ['.aside:has(.blocked)', 'held-unrenderable'],
      ['.refusal', 'numbering-refusal']
    ];
    for (const [selector, kind] of evidence) {
      document.querySelectorAll(`#reading ${selector}`).forEach((node) =>
          node.setAttribute('data-wave-evidence', kind));
    }
  }
  function enhanceSources() {
    wrapFilter('sources');
    markPrimary(document.getElementById('reading'), 'source-primary');
    document.querySelector('.page-header h1')?.setAttribute('data-wave-title', '');
    document.getElementById('finder')?.setAttribute('data-wave-source-plane', 'finder');
    document.getElementById('reader')?.setAttribute('data-wave-source-plane', 'reader');
    const lede = document.querySelector('.page-header .lede');
    if (lede) {
      lede.textContent =
          'Browse each source as a Work, Edition, Artifact, and Passage. Read held text ' +
          'where rights permit; where it may not be served, keep the record and reason.';
    }
  }
  function decorateSourceConstraints() {
    const filter = document.querySelector('[data-wave-filter="sources"]');
    const form = document.getElementById('controls');
    const find = document.getElementById('find-input');
    let summary = document.querySelector('[data-wave-active-constraints="sources"]');
    if (!filter || !form || !find || form.hidden) {
      summary?.remove();
      return;
    }
    const active = [];
    if (find.value.trim()) active.push(`Find “${find.value.trim()}”`);
    for (const id of [
      'author-select', 'category-select', 'language-select', 'period-select', 'rights-select'
    ]) {
      const control = document.getElementById(id);
      if (!control?.value) continue;
      const label = document.querySelector(`label[for="${id}"]`)?.textContent.trim() || id;
      active.push(`${label}: ${control.selectedOptions[0]?.textContent.trim() || control.value}`);
    }
    const readable = document.getElementById('readable-input');
    if (readable?.checked) active.push('Readable here only');
    const sort = document.getElementById('sort-select');
    if (sort?.value && sort.value !== 'author') {
      active.push(`Order: ${sort.selectedOptions[0]?.textContent.trim() || sort.value}`);
    }
    if (!active.length) {
      summary?.remove();
      return;
    }
    if (!summary) {
      summary = element('div', 'wave-active-constraints');
      summary.setAttribute('data-wave-active-constraints', 'sources');
      summary.style.order = '4';
      const text = element('p');
      text.setAttribute('data-wave-active-constraints-text', '');
      const clear = element('button', 'wave-clear-constraints', 'Clear filters');
      clear.type = 'button';
      clear.setAttribute('data-wave-clear-constraints', '');
      clear.addEventListener('click', () => {
        form.reset();
        find.dispatchEvent(new InputEvent('input', {bubbles: true, inputType: 'deleteContent'}));
        find.focus({preventScroll: true});
      });
      summary.append(text, clear);
      filter.insertAdjacentElement('afterend', summary);
    }
    const text = summary.querySelector('[data-wave-active-constraints-text]');
    const value = 'Active filters · ' + active.join(' · ');
    if (text && text.textContent !== value) text.textContent = value;
  }
  function decorateSources() {
    const sourceFilter = document.querySelector('[data-wave-filter="sources"]');
    const sourceForm = document.getElementById('controls');
    if (sourceFilter && sourceForm && sourceFilter.hidden !== sourceForm.hidden) {
      sourceFilter.hidden = sourceForm.hidden;
    }
    decorateSourceConstraints();
    for (const work of document.querySelectorAll('#finder .work')) {
      work.setAttribute('data-wave-object', 'work');
      const title = work.querySelector(':scope > .work-title');
      objectLabel(work, title, 'work');
      work.querySelectorAll(':scope .edition').forEach((edition) => {
        edition.setAttribute('data-wave-object', 'edition');
        const button = edition.querySelector(':scope > .edition-open');
        objectLabel(edition, button, 'edition', 'span');
      });
    }
    const readerHead = document.querySelector('.reader-head');
    readerHead?.setAttribute('data-wave-identity', 'work-and-edition');
    const readerTitle = readerHead?.querySelector(':scope > .reader-title');
    objectLabel(readerHead, readerTitle, 'work');
    const readerEdition = readerHead?.querySelector(':scope > .reader-edition');
    objectLabel(readerHead, readerEdition, 'edition');
    const passage = document.querySelector('.passage-body');
    passage?.setAttribute('data-wave-object', 'passage');
    objectLabel(passage?.parentNode, passage, 'passage');
    const context = passage?.querySelector(':scope > .passage-context');
    if (context && !context.hasAttribute('data-wave-editorial-context')) {
      context.setAttribute('data-wave-editorial-context', 'inspection-scope');
      const label = element(
          'p', 'eyebrow wave-context-label', 'Inspection scope · editorial summary');
      label.setAttribute('data-wave-object-label', 'editorial-context');
      context.insertAdjacentElement('beforebegin', label);
    }
    const withheld = passage?.querySelector(':scope > .notice');
    const contextLabel = passage?.querySelector(
        ':scope > [data-wave-object-label="editorial-context"]');
    if (withheld && context && contextLabel && withheld.compareDocumentPosition(contextLabel) &
        Node.DOCUMENT_POSITION_PRECEDING) {
      passage.insertBefore(withheld, contextLabel);
    }
    document.querySelector('.passage-source')?.setAttribute('data-wave-evidence', 'provenance');
    for (const disclosure of document.querySelectorAll('.apparatus')) {
      const artifacts = disclosure.querySelector(':scope > .artifact-list');
      if (artifacts) {
        disclosure.setAttribute('data-wave-disclosure', 'edition-artifacts');
        artifacts.setAttribute('data-wave-object', 'artifact-list');
        artifacts.querySelectorAll(':scope > .artifact')
            .forEach((artifact) => artifact.setAttribute('data-wave-object', 'artifact'));
      } else {
        disclosure.setAttribute('data-wave-disclosure', 'work-description');
      }
    }
  }
  function start() {
    html.removeAttribute('data-corpus-wave1-pending');
    const surface = detectSurface();
    if (!surface) return;
    html.setAttribute('data-corpus-wave1', surface);
    const main = document.querySelector('main#main-content') || document.querySelector('main');
    if (!main) return;
    labelReadingMain(main, surface);
    main.setAttribute('data-wave-surface', surface);
    main.setAttribute('data-wave-surface-main', surface);
    replacePublicationsLabels();
    const dialog = createDialog();
    enhanceShell(surface, dialog);
    if (surface === 'home')
      enhanceHome(main);
    else if (surface === 'publications')
      enhancePublications(main);
    else if (surface === 'reader')
      enhanceReader(main);
    else if (surface === 'catena')
      enhanceCatena();
    else if (surface === 'sources')
      enhanceSources();
    function decorate() {
      labelReadingMain(main, surface);
      replacePublicationsLabels();
      if (surface === 'publications')
        decoratePublications();
      else if (surface === 'catena')
        decorateCatena();
      else if (surface === 'sources')
        decorateSources();
      document.body.setAttribute('data-wave-ready', '');
    }
    let pending = false;
    const observer = new MutationObserver(() => {
      if (pending) return;
      pending = true;
      window.queueMicrotask(() => {
        pending = false;
        decorate();
      });
    });
    observer.observe(main, {childList: true, subtree: true});
    decorate();
  }
  if (document.readyState === 'loading')
    document.addEventListener('DOMContentLoaded', start, {once: true});
  else
    start();
})();
