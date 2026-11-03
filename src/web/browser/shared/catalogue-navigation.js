/* Table measurements and session return positions for opted-in catalogues/readers. */
(function () {
  'use strict';
  function measureHeading(head) {
    head.closest('table').style.setProperty('--catalogue-heading-height',
      head.getBoundingClientRect().height + 'px');
  }
  if ('ResizeObserver' in window) {
    const headings = new ResizeObserver(function (entries) {
      entries.forEach(function (entry) {
        measureHeading(entry.target);
      });
    });
    document.querySelectorAll('.catalogue-table thead').forEach(function (head) {
      headings.observe(head);
    });
  }
  addEventListener('focusin', function (event) {
    const table = event.target.closest && event.target.closest('.catalogue-table');
    if (table && table.tHead && !table.tHead.contains(event.target)) {
      measureHeading(table.tHead);
      event.target.scrollIntoView({ block: 'nearest', inline: 'nearest', behavior: 'instant' });
    }
  });
  const reader = document.querySelector('.publication-reader');
  if (!reader && !document.querySelector('.page-catalog, .page-home')) return;

  const stateKey = 'triptychCataloguePosition';
  const storageKey = 'triptych:catalogue:' +
    location.pathname.replace(/\/index\.html$/, '/') + location.search;
  const webRoot = new URL('../web/', document.currentScript.src);
  const printRoot = new URL('../print/', document.currentScript.src);
  const siteRoot = new URL('../', document.currentScript.src);
  const libraryRoot = new URL('library/', siteRoot);

  function position(value) {
    return value && Number.isFinite(value.x) && Number.isFinite(value.y) &&
      value.x >= 0 && value.y >= 0 ? value : null;
  }

  function savedPosition() {
    try { return position(JSON.parse(sessionStorage.getItem(storageKey))); }
    catch (_) { return null; }
  }

  function save() {
    const value = { x: scrollX, y: scrollY };
    try {
      history.replaceState(Object.assign({}, history.state, { [stateKey]: value }), '');
    } catch (_) { /* Native history restoration remains available. */ }
    try { sessionStorage.setItem(storageKey, JSON.stringify(value)); }
    catch (_) { /* Session storage is an optional enhancement. */ }
  }

  function fromCatalogueOrPublication() {
    try {
      const referrer = new URL(document.referrer);
      return referrer.origin === siteRoot.origin &&
        (referrer.pathname.startsWith(webRoot.pathname) ||
         referrer.pathname.startsWith(printRoot.pathname) ||
         referrer.pathname.startsWith(libraryRoot.pathname) ||
         referrer.pathname === siteRoot.pathname ||
         referrer.pathname === siteRoot.pathname + 'index.html');
    } catch (_) { return false; }
  }

  addEventListener('pagehide', save);
  let stopPending = function () {};
  addEventListener('pagehide', function () { stopPending(); });
  addEventListener('pageshow', function (event) {
    stopPending();
    const navigation = performance.getEntriesByType('navigation')[0];
    const traversal = event.persisted || (navigation && navigation.type === 'back_forward');
    // An explicit section link on a new visit always keeps its own destination.
    const value = traversal ? position(history.state && history.state[stateKey]) :
      (!location.hash && fromCatalogueOrPublication() ? savedPosition() : null);
    if (!value) return;
    if (!reader) {
      requestAnimationFrame(function () {
        requestAnimationFrame(function () {
          scrollTo({ left: value.x, top: value.y, behavior: 'instant' });
        });
      });
      return;
    }
    // Observe deliberate input immediately, including before the first frame.
    // Wait for delayed content/fonts only while the saved range is unavailable.
    let stopped = false;
    let observer;
    let timer;
    function stop() {
      stopped = true;
      if (observer) observer.disconnect();
      clearTimeout(timer);
      for (const name of ['wheel', 'pointerdown', 'keydown']) removeEventListener(name, stop);
    }
    stopPending = stop;
    function restore() {
      if (stopped) return;
      const height = Math.max(document.documentElement.scrollHeight, document.body.scrollHeight);
      if (height - innerHeight + 2 < value.y) return;
      scrollTo({ left: value.x, top: value.y, behavior: 'instant' });
      stop();
    }
    for (const name of ['wheel', 'pointerdown', 'keydown']) addEventListener(name, stop, {passive: true});
    timer = setTimeout(stop, 10000);
    requestAnimationFrame(function () {
      requestAnimationFrame(function () {
        if (stopped) return;
        if ('ResizeObserver' in window) {
          observer = new ResizeObserver(restore);
          observer.observe(document.body);
        }
        restore();
      });
    });
  });
}());
