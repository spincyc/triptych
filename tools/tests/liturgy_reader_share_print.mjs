#!/usr/bin/env node

/* Focused Share/Print contract checks without loading or copying liturgical text. */

import assert from 'node:assert/strict';
import { createRequire } from 'node:module';
import { resolve } from 'node:path';
import test from 'node:test';

const require = createRequire(import.meta.url);
const ROOT = resolve(import.meta.dirname, '../..');
const actions = require(resolve(ROOT, 'src/web/browser/liturgy/reader-share-print.js'));
const state = require(resolve(ROOT, 'src/web/browser/liturgy/reader-state.js'));

test('canonical Day and date-free Propers links retain semantic hashes without mutating location', () => {
  const day = { href: 'https://example.test/src/web/browser/liturgy/day-reader.html' +
    '#date=2026-08-02&missal=roman-1962&mode=compare&peer-missal=postconciliar-2008&territory=universal&location=compare%2Fproper%2Fintroit' };
  const original = day.href;
  const shared = actions.canonicalUrl('day', day, state);
  assert.equal(day.href, original);
  assert.equal(new URL(shared).pathname, '/src/web/browser/liturgy/day.html');
  assert.equal(new URL(shared).hash, new URL(original).hash);
  const proper = { href: 'https://example.test/src/web/browser/liturgy/propers-reader.html' +
    '#missal=roman-1962&type=seasonal&mass=pentecost-10&mode=study&location=proper%2Fintroit' };
  const properShared = actions.canonicalUrl('propers', proper, state);
  assert.equal(new URL(properShared).pathname, '/src/web/browser/liturgy/index.html');
  assert.equal(new URL(properShared).searchParams.has('date'), false);
  assert.equal(new URL(properShared).hash, new URL(proper.href).hash);
});

test('descriptive titles name the Day date and Compare territory, without inventing a Propers date', () => {
  const shell = { querySelector() { return { textContent: 'Tenth Sunday after Pentecost' }; } };
  const day = actions.shareTitle('day', shell, {
    civilDate: '2026-08-02', edition: { id: 'roman-1962' }, requestedMode: 'compare',
    comparison: { dimension: 'recension',
      sides: [{}, { edition: { id: 'postconciliar-2008' } }],
      anchor: { territorialContext: 'universal' } }
  });
  assert.match(day, /2026-08-02/);
  assert.match(day, /Compare recension with postconciliar-2008/);
  assert.match(day, /universal/);
  const proper = actions.shareTitle('propers', shell, {
    edition: { id: 'roman-1962' }, requestedMode: 'study'
  });
  assert.match(proper, /Propers.*roman-1962.*study/);
  assert.doesNotMatch(proper, /2026-08-02/);
  const language = actions.shareTitle('propers', shell, {
    edition: { id: 'roman-1962' }, requestedMode: 'compare',
    comparison: { dimension: 'oration-language', sides: [
      { edition: { id: 'roman-1962' }, languages: { orations: 'la' } },
      { edition: { id: 'roman-1962' }, languages: { orations: 'en' } }
    ] }
  });
  assert.match(language, /Compare oration-language with en/);
  assert.doesNotMatch(language, /with roman-1962/);
  const cycle = actions.shareTitle('propers', shell, {
    edition: { id: 'postconciliar' }, requestedMode: 'compare', cycle: 'A',
    comparison: { dimension: 'lectionary-cycle', sides: [
      { edition: { id: 'postconciliar' }, cycle: 'A' },
      { edition: { id: 'postconciliar' }, cycle: 'B' }
    ] }
  });
  assert.match(cycle, /Compare lectionary-cycle with Cycle B/);
  assert.doesNotMatch(cycle, /with postconciliar/);
  const alternative = actions.shareTitle('propers', shell, {
    edition: { id: 'postconciliar' }, requestedMode: 'compare',
    comparison: { dimension: 'reading-alternative', sides: [{}, {
      edition: { id: 'postconciliar' },
      alternative: { id: 'proper-choice/postconciliar/presentation-lord/main/gospel/shorter' }
    }] }
  });
  assert.match(alternative, /Compare reading-alternative with Option shorter/);
  assert.doesNotMatch(alternative, /with postconciliar/);
});

test('native share receives only title and URL; copy handles unavailability and native failure', async () => {
  const calls = [];
  const opts = { title: 'Propers · roman-1962', url: 'https://example.test/index.html#mass=pentecost-10',
    document: {}, focusTarget: {} };
  assert.equal(await actions.share({ ...opts, navigator: {
    share: async (value) => { calls.push(value); }
  } }), 'Shared this reader link.');
  assert.deepEqual(calls, [{ title: opts.title, url: opts.url }]);
  let copied = null;
  const navigator = { clipboard: { writeText: async (value) => { copied = value; } } };
  assert.equal(await actions.share({ ...opts, navigator }), 'Reader link copied to clipboard.');
  assert.equal(copied, opts.url);
  assert.equal(await actions.share({ ...opts, navigator: {
    ...navigator, share: async () => { throw new Error('unavailable'); }
  } }), 'Reader link copied to clipboard.');
  assert.equal(await actions.share({ ...opts, navigator: {
    ...navigator, share: async () => { throw { name: 'AbortError' }; }
  } }), 'Sharing cancelled.');
  assert.equal(await actions.share({ ...opts, navigator: {}, document: {} }),
    'Could not share or copy this reader link.');
});

test('local copy fallback reports the actual command result and restores button focus', async () => {
  let selected = false;
  let removed = false;
  let focused = false;
  const parent = { appendChild(field) { assert.equal(field.value, 'https://example.test/day.html'); } };
  const button = { parentElement: parent, isConnected: true,
    focus() { focused = true; } };
  const doc = { createElement() { return {
    style: {}, setAttribute() {}, select() { selected = true; },
    remove() { removed = true; }
  }; }, execCommand(command) { assert.equal(command, 'copy'); return true; } };
  assert.equal(await actions.copyUrl('https://example.test/day.html', {}, doc, button), true);
  assert.equal(selected && removed && focused, true);
  doc.execCommand = () => { throw new Error('denied'); };
  assert.equal(await actions.copyUrl('https://example.test/day.html', {}, doc, button), false);
});

class Element {
  constructor(tag) {
    this.tagName = tag.toUpperCase();
    this.children = [];
    this.dataset = {};
    this.style = {};
    this.listeners = {};
    this.textContent = '';
    this.attributes = {};
  }
  get firstChild() { return this.children[0] || null; }
  appendChild(child) { this.children.push(child); child.parentElement = this; return child; }
  append(...children) { children.forEach((child) => this.appendChild(child)); }
  insertBefore(child, before) {
    const old = this.children.indexOf(child);
    if (old >= 0) this.children.splice(old, 1);
    const at = this.children.indexOf(before);
    this.children.splice(at < 0 ? this.children.length : at, 0, child);
    child.parentElement = this;
    queueMicrotask(() => this.observer?.());
  }
  replaceChildren(...children) {
    this.children = [];
    this.append(...children);
    queueMicrotask(() => this.observer?.());
  }
  querySelector(selector) {
    if (selector === '[data-reader-share-print]') {
      return this.children.find((child) => 'readerSharePrint' in child.dataset) || null;
    }
    return null;
  }
  setAttribute(name, value) { this.attributes[name] = value; }
  getAttribute(name) { return this.attributes[name] ?? null; }
  addEventListener(name, callback) { this.listeners[name] = callback; }
}

test('Details retains native keyboard buttons after replacement; Share and Print leave URL unchanged', async () => {
  for (const entrance of ['day', 'propers']) {
    const body = new Element('div');
    const heading = new Element('h1');
    heading.textContent = 'Pentecost';
    const shell = {
      dataset: { entrance },
      querySelector(selector) {
        if (selector === '[data-reader-details]') return body;
        if (selector === '.reader-identity .celebration-title') return heading;
        return null;
      }
    };
    const reading = new Element('main');
    reading.setAttribute('aria-busy', 'false');
    const doc = {
      querySelector() { return shell; },
      getElementById() { return reading; },
      createElement(tag) { return new Element(tag); }
    };
    const path = entrance === 'day' ? 'day.html#date=2026-08-02&missal=roman-1962&mode=read' :
      'index.html#missal=roman-1962&type=seasonal&mass=pentecost&mode=read';
    const url = 'https://example.test/liturgy/' + path;
    let copied = null;
    let prints = 0;
    const win = {
      location: { href: url }, LiturgyReaderState: state,
      navigator: { clipboard: { writeText: async (value) => { copied = value; } } },
      print() { prints += 1; },
      MutationObserver: class {
        constructor(callback) { this.callback = callback; }
        observe(target) { target.observer = this.callback; }
        disconnect() { body.observer = null; }
      },
      [entrance === 'day' ? 'dayReaderDebug' : 'propersReaderDebug']: {
        ready: true, state: { civilDate: entrance === 'day' ? '2026-08-02' : null,
          edition: { id: 'roman-1962' }, requestedMode: 'read' }
      }
    };
    const mounted = actions.install({ document: doc, window: win });
    assert.ok(mounted);
    assert.equal(body.firstChild, mounted.section);
    assert.equal(actions.install({ document: doc, window: win }), null);
    const controls = mounted.section.children[1];
    const shareButton = controls.children[0];
    const printButton = controls.children[1];
    assert.equal(shareButton.tagName, 'BUTTON');
    assert.equal(printButton.tagName, 'BUTTON');
    assert.equal(shareButton.type, 'button');
    assert.equal(printButton.type, 'button');
    assert.equal(mounted.section.children[2].attributes.role, 'status');
    await shareButton.listeners.click();
    assert.equal(copied, url);
    printButton.listeners.click();
    assert.equal(prints, 1);
    assert.equal(win.location.href, url);
    body.replaceChildren(new Element('p'));
    await Promise.resolve();
    assert.equal(body.firstChild, mounted.section);
    mounted.disconnect();
  }
});
