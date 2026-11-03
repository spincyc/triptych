/* Progressive controls for the publication shell. Canonical body/print DOM stays untouched. */
(function () {
  'use strict';
  const installations = new WeakMap();

  function localDocument(value, base) {
    try {
      const current = new URL(base);
      const target = new URL(value, current);
      return /^https?:$/.test(target.protocol) && target.origin === current.origin &&
        !target.username && !target.password && target.pathname.endsWith('.html') ? target : null;
    } catch (_) { return null; }
  }

  function sectionAddress(base, id) {
    const address = new URL(base);
    // A shared reading address must not open somebody else's print dialog.
    address.searchParams.delete('print');
    address.hash = id ? encodeURIComponent(id) : '';
    return address.href;
  }

  function install(root) {
    if (installations.has(root)) return installations.get(root);
    const content = root.querySelector('[data-reader-content]');
    if (!content) return null;
    const toc = root.querySelector('[data-reader-toc]');
    const toolbar = root.querySelector('.publication-reader__toolbar');
    const selector = root.querySelector('[data-reader-document-select]');
    const copy = root.querySelector('[data-reader-copy-link]');
    const status = root.querySelector('[data-reader-status]');
    const progress = root.querySelector('[data-reader-progress]');
    const contents = root.querySelector('details[data-reader-contents]');
    const compact = window.matchMedia('(max-width: 64rem)');
    let desktopOpen = contents ? contents.open : true;
    let sections = [];
    let current = null;
    let scheduled = false;
    let shareField = null;

    function inset() {
      if (!toolbar) return 12;
      const box = toolbar.getBoundingClientRect();
      return box.top <= 12 && box.bottom > 0 ? box.bottom + 12 : 12;
    }

    function refresh() {
      sections = [];
      const seen = new Set();
      if (toc) toc.querySelectorAll('a[href]').forEach(function (link) {
        try {
          const address = new URL(link.href, location.href);
          if (address.origin !== location.origin || address.pathname !== location.pathname ||
              address.search !== location.search || !address.hash) return;
          const id = decodeURIComponent(address.hash.slice(1));
          const target = document.getElementById(id);
          if (!target || !(target === content || content.contains(target))) return;
          if (!seen.has(id)) sections.push({ id, target, links: [], margin: parseFloat(getComputedStyle(target).scrollMarginTop) || 0 });
          seen.add(id);
          sections.find(function (section) { return section.id === id; }).links.push(link);
        } catch (_) { /* A malformed fragment never selects a different section. */ }
      });
      schedule();
    }

    function update() {
      scheduled = false;
      const threshold = inset() + 12;
      // Opening prose belongs to the page until a named section is reached.
      let active = null;
      for (const section of sections) {
        if (section.target.getBoundingClientRect().top <= Math.max(threshold, section.margin + 2)) active = section;
      }
      if (active !== current) {
        sections.forEach(function (section) {
          section.links.forEach(function (link) {
            if (section === active) link.setAttribute('aria-current', 'location');
            else link.removeAttribute('aria-current');
          });
        });
        current = active;
      }
      if (progress) {
        const box = content.getBoundingClientRect();
        const span = Math.max(1, box.height - Math.max(1, innerHeight - threshold));
        progress.value = Math.round(Math.max(0, Math.min(1, (threshold - box.top) / span)) * 100);
      }
    }

    function schedule() {
      if (scheduled) return;
      scheduled = true;
      requestAnimationFrame(update);
    }

    function measure() {
      if (toolbar) root.style.setProperty('--reader-toolbar-height', toolbar.getBoundingClientRect().height + 'px');
      sections.forEach(function (section) { section.margin = parseFloat(getComputedStyle(section.target).scrollMarginTop) || 0; });
      schedule();
    }

    if (selector) {
      selector.addEventListener('change', function () {
        const option = selector.selectedOptions[0];
        const address = option && !option.disabled && option.value &&
          Array.from(selector.options).includes(option) && localDocument(option.value, location.href);
        if (address) location.assign(address.href);
        else if (status) status.textContent = 'That document is unavailable. Choose another document.';
      });
      const field = selector.closest('.publication-reader__document');
      if (field) field.hidden = false;
    }

    function showShareField(address) {
      if (!shareField) {
        const label = document.createElement('label');
        label.className = 'publication-reader__share-field';
        label.appendChild(document.createTextNode('Section link'));
        shareField = document.createElement('input');
        shareField.type = 'url';
        shareField.readOnly = true;
        label.appendChild(shareField);
        (toolbar || root).appendChild(label);
      }
      shareField.value = address;
      shareField.parentElement.hidden = false;
      shareField.focus({preventScroll: true});
      shareField.select();
      if (status) status.textContent = 'Select and copy the section link.';
    }

    if (copy) {
      copy.hidden = false;
      copy.addEventListener('click', async function () {
        update();
        const address = sectionAddress(location.href, current && current.id);
        try {
          if (!navigator.clipboard || !navigator.clipboard.writeText) throw new Error('Clipboard unavailable');
          await navigator.clipboard.writeText(address);
          if (shareField) shareField.parentElement.hidden = true;
          if (status) status.textContent = 'Section link copied.';
        } catch (_) { showShareField(address); }
      });
    }

    function resizeContents() {
      if (!contents) return;
      if (compact.matches) {
        if (!contents.contains(document.activeElement)) contents.open = false;
      } else contents.open = desktopOpen;
    }
    if (contents) {
      resizeContents();
      contents.addEventListener('toggle', function () {
        if (!compact.matches) desktopOpen = contents.open;
        schedule();
      });
      compact.addEventListener('change', resizeContents);
      contents.addEventListener('click', function (event) {
        const link = event.target.closest && event.target.closest('a[href]');
        if (compact.matches && link && event.button === 0 && !event.metaKey &&
            !event.ctrlKey && !event.altKey && !event.shiftKey) contents.open = false;
      });
    }

    root.addEventListener('focusin', function (event) {
      if (!content.contains(event.target)) return;
      // A sticky bar must not cover keyboard focus; leave already-visible focus still.
      const box = event.target.getBoundingClientRect();
      const clearance = inset();
      if (box.top < clearance && box.bottom > 0) scrollBy({top: box.top - clearance, behavior: 'instant'});
    });
    addEventListener('scroll', schedule, {passive: true});
    addEventListener('resize', measure, {passive: true});
    addEventListener('pageshow', schedule);
    addEventListener('hashchange', schedule);
    if ('ResizeObserver' in window) {
      const resize = new ResizeObserver(measure);
      if (toolbar) resize.observe(toolbar);
      resize.observe(content);
    }
    if ('MutationObserver' in window) {
      const changes = new MutationObserver(refresh);
      changes.observe(content, {childList: true, subtree: true});
      if (toc) changes.observe(toc, {childList: true, subtree: true});
    }
    measure();
    refresh();
    const controller = Object.freeze({refresh, update});
    installations.set(root, controller);
    return controller;
  }

  function bootstrap() { document.querySelectorAll('.publication-reader').forEach(install); }
  window.TriptychPublicationReader = Object.freeze({install, localDocument, sectionAddress});
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', bootstrap, {once: true});
  else bootstrap();
}());
