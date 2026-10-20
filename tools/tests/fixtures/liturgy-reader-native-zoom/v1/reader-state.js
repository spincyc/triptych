'use strict';
return (() => {
  const rect = node => {
    if (!node) return null;
    const box = node.getBoundingClientRect();
    return { left: box.left, top: box.top, right: box.right, bottom: box.bottom,
      width: box.width, height: box.height };
  };
  const reading = document.getElementById('reader-document');
  const shell = document.querySelector('[data-reader-shell]');
  const entrance = shell?.dataset.entrance;
  const debug = window[entrance === 'day' ? 'dayReaderDebug' : 'propersReaderDebug'];
  const line = Math.max(80, Math.min(innerHeight * .38, 280));
  const units = [...(reading?.querySelectorAll('[data-semantic-location]') || [])];
  let current = units[0];
  for (const node of units) {
    if (node.getBoundingClientRect().top <= line) current = node;
    else break;
  }
  const focused = document.activeElement;
  const heading = focused?.querySelector?.(':scope > .proper-name, :scope > .ordinary-head, :scope > h2, :scope > h3') || focused;
  const viewport = window.visualViewport;
  return {
    href: location.href, entrance: entrance,
    ready: debug?.ready, outcome: debug?.outcome,
    busy: reading?.getAttribute('aria-busy'), mode: debug?.state?.requestedMode,
    edition: debug?.state?.edition?.id, date: debug?.state?.civilDate,
    mass: debug?.state?.selectedReadableFormulary?.id || debug?.state?.formulary?.id,
    currentUnit: current?.dataset.semanticLocation || null,
    focus: { id: focused?.id, tag: focused?.tagName,
      action: focused?.dataset.readerAction,
      semanticLocation: focused?.dataset.semanticLocation,
      close: focused?.hasAttribute?.('data-reader-close') || false,
      outline: focused ? getComputedStyle(focused).outlineStyle : null,
      rect: rect(focused), heading: rect(heading) },
    scroll: { x: scrollX, y: scrollY, height: document.documentElement.scrollHeight },
    cssViewport: { width: innerWidth, height: innerHeight,
      clientWidth: document.documentElement.clientWidth,
      clientHeight: document.documentElement.clientHeight,
      scrollWidth: document.documentElement.scrollWidth },
    outer: { width: outerWidth, height: outerHeight },
    screen: { width: screen.width, height: screen.height,
      availableWidth: screen.availWidth, availableHeight: screen.availHeight },
    devicePixelRatio: devicePixelRatio,
    visualViewport: viewport ? { width: viewport.width, height: viewport.height,
      scale: viewport.scale, offsetTop: viewport.offsetTop, offsetLeft: viewport.offsetLeft } : null,
    root: { fontSize: getComputedStyle(document.documentElement).fontSize,
      zoom: getComputedStyle(document.documentElement).zoom,
      bodyZoom: getComputedStyle(document.body).zoom },
    reading: rect(reading), masthead: rect(document.querySelector('.reader-masthead')),
    actions: rect(document.querySelector('.reader-actions')),
    openSurfaces: [...document.querySelectorAll('[data-reader-surface][open]')]
      .map(node => ({ name: node.dataset.readerSurface, rect: rect(node),
        scrollWidth: node.scrollWidth, clientWidth: node.clientWidth })),
    comparePairColumns: [...document.querySelectorAll('.compare-pair')].slice(0, 2)
      .map(node => getComputedStyle(node).gridTemplateColumns)
  };
})();
