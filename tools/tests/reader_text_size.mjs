#!/usr/bin/env node

import assert from 'node:assert/strict';
import { createRequire } from 'node:module';
import test from 'node:test';

const require = createRequire(import.meta.url);
const preference = require('../../src/web/browser/liturgy/reader-text-size.js');

test('only supported exact enlargement preferences are accepted', () => {
  for (const size of [100, 125, 150, 175, 200]) {
    assert.equal(preference.validSize(size), size);
    assert.equal(preference.validSize(String(size)), size);
  }
  for (const invalid of [null, undefined, '', ' 150 ', '200%', '150.0', '1e2',
    0, 99, 101, 201, NaN, Infinity, {}, [150]]) {
    assert.equal(preference.validSize(invalid), null);
  }
});

test('storage failure and malformed memory leave a usable default', () => {
  for (const raw of [null, '', '200%', '999', '{}']) {
    assert.equal(preference.readPreference({ localStorage: { getItem: () => raw } }), 100);
  }
  assert.equal(preference.readPreference({ get localStorage() { throw new Error('denied'); } }), 100);
  assert.equal(preference.readPreference({ localStorage: { getItem: () => '175' } }), 175);
});

test('only valid explicit settings are persisted in the independent display preference', () => {
  const calls = [];
  const win = { localStorage: { setItem: (...args) => calls.push(args) } };
  assert.equal(preference.writePreference(win, 200), true);
  assert.deepEqual(calls, [['triptych:liturgy:text-size:v1', '200']]);
  assert.equal(preference.writePreference(win, '200%'), false);
  assert.equal(calls.length, 1);
  assert.equal(preference.writePreference({ get localStorage() { throw new Error('denied'); } }, 150), false);
});

// Model layout reads after root font sizing; focus or page-scrolling repairs
// would throw here. The existing semantic restorer has its one window scroll.
function reflowFixture(options = {}) {
  const events = node => Object.assign(node, {
    listeners: new Map(),
    addEventListener(type, callback) { this.listeners.set(type, callback); },
    dispatch(type) { this.listeners.get(type)?.(); }
  });
  const make = () => events({ dataset: {}, isConnected: true,
    append() {}, appendChild() {}, setAttribute() {},
    focus() { throw new Error('focus must stay owned by the reader'); },
    scrollIntoView() { throw new Error('ancestor scrolling is forbidden'); }
  });
  const frames = new Map(), canceled = [], scrolls = [];
  let nextFrame = 0;
  const header = make();
  header.getBoundingClientRect = () => ({ bottom: options.headerBottom ?? 110 });
  const surface = events({ open: true, isConnected: true, scrollTop: 0,
    clientTop: 1, clientHeight: options.portHeight ?? 500,
    querySelector: selector => selector === '.surface-head' ? header : null,
    insertBefore() {},
    getBoundingClientRect: () => ({ top: options.panelTop ?? 44 })
  });
  const doc = { createElement: make,
    documentElement: { dataset: {}, scrollHeight: 10000, style: { setProperty() {} } },
    body: { scrollHeight: 10000 },
    querySelector: () => ({ querySelector: () => surface }),
    getElementById: () => reading
  };
  const factor = () => Number(doc.documentElement.dataset.readerTextSize) / 100;
  const win = { innerHeight: 437, scrollY: 500,
    localStorage: { getItem: () => null, setItem() {} },
    MutationObserver: class { constructor(callback) { this.callback = callback; win.observer = this; } observe() {} },
    requestAnimationFrame(callback) { frames.set(++nextFrame, callback); return nextFrame; },
    cancelAnimationFrame(id) { canceled.push(id); frames.delete(id); },
    scrollTo(value) { scrolls.push(value); win.scrollY = value.top; },
    getComputedStyle(node) { return node === header ? { position: options.sticky ? 'sticky' : 'static' } : {
      outlineStyle: 'solid', outlineWidth: '2px', outlineOffset: options.outlineOffset ?? '2px'
    }; },
    location: { href: 'https://example.invalid/liturgy/day.html#mode=read&location=proper-3' }
  };
  const semantic = { dataset: { semanticLocation: 'proper-3' },
    getBoundingClientRect: () => ({ top: 400 * factor() - win.scrollY, height: 1000 * factor() }) };
  const reading = { ownerDocument: doc, querySelectorAll: () => [semantic] };
  const installed = preference.install({ document: doc, window: win });
  const select = installed.select;
  select.getBoundingClientRect = () => {
    const top = (factor() === 2 ? 774.9375 : 250) - surface.scrollTop;
    return { top, bottom: top + (factor() === 2 ? 69 : 44) };
  };
  doc.activeElement = select;
  return { win, doc, reading, surface, select, frames, canceled, scrolls,
    change(value) { select.value = String(value); select.dispatch('change'); },
    frame() { const queued = [...frames.values()]; frames.clear(); queued.forEach(callback => callback()); }
  };
}

test('reflow reveals the active full outline in the viewport-clipped Mode port in both directions', () => {
  const held = reflowFixture();
  const before = preference.captureLocation(held.win, held.reading);
  const url = held.win.location.href;
  held.change(200);
  assert.equal(held.surface.scrollTop, 0, 'the change waits for actual layout');
  held.frame();
  assert.equal(held.select.getBoundingClientRect().bottom + 4, 436,
    'the viewport clips the taller dialog port, with one CSS pixel for scroll rounding');
  assert.equal(held.scrolls.length, 1, 'only the existing semantic restore scrolls the window');
  assert.equal(preference.captureLocation(held.win, held.reading).id, before.id);
  assert.ok(Math.abs(preference.captureLocation(held.win, held.reading).fraction - before.fraction) < 1e-9);
  held.change(100);
  held.frame();
  assert.equal(held.select.getBoundingClientRect().top - 4, 46);
  assert.equal(held.doc.activeElement, held.select);
  assert.equal(held.win.location.href, url);
  assert.equal(held.scrolls.length, 2);
});

test('sticky headers and inset outlines use their computed visible boundaries; visible controls stay put', () => {
  const held = reflowFixture({ sticky: true, outlineOffset: '-1px' });
  held.change(200); held.frame();
  assert.equal(held.select.getBoundingClientRect().bottom + 1, 436);
  held.change(100); held.frame();
  assert.equal(held.select.getBoundingClientRect().top - 1, 111,
    'the sticky header and one CSS pixel for scroll rounding are excluded');
  const previous = held.surface.scrollTop;
  held.change(100); held.frame();
  assert.equal(held.surface.scrollTop, previous, 'no scroll when the full outline already fits');
});

test('closed, detached, moved-focus and reopened visits cannot claim a queued control reveal', () => {
  for (const boundary of ['closed', 'surface-detached', 'control-detached', 'moved-focus', 'reopened']) {
    const held = reflowFixture();
    held.change(200);
    if (boundary === 'closed') held.surface.open = false;
    if (boundary === 'surface-detached') held.surface.isConnected = false;
    if (boundary === 'control-detached') held.select.isConnected = false;
    if (boundary === 'moved-focus') held.doc.activeElement = {};
    if (boundary === 'reopened') {
      held.surface.open = false; held.win.observer.callback();
      held.surface.open = true; held.win.observer.callback();
    }
    held.frame();
    assert.equal(held.surface.scrollTop, 0, boundary);
  }
});

test('coalesced changes and close restoration cancel stale frames without revealing a closed visit', () => {
  const held = reflowFixture();
  held.win.scrollY = 0;
  held.change(200); held.change(100);
  assert.equal(held.frames.size, 1);
  assert.equal(held.canceled.length, 1);
  held.frame();
  assert.equal(held.scrolls.length, 1);
  assert.equal(held.surface.scrollTop, 0, 'only the final 100% layout is considered');
  held.change(200);
  held.surface.open = false;
  held.surface.dispatch('close');
  assert.equal(held.frames.size, 1);
  assert.equal(held.canceled.length, 2);
  held.frame();
  assert.equal(held.scrolls.length, 2, 'close retains the semantic restoration');
  assert.equal(held.surface.scrollTop, 0);
});
