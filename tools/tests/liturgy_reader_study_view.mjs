#!/usr/bin/env node

/* Source-honest Study projection and browser element composition. */

import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { createRequire } from 'node:module';
import { resolve } from 'node:path';
import test from 'node:test';

const require = createRequire(import.meta.url);
const ROOT = resolve(import.meta.dirname, '../..');
const Study = require(resolve(ROOT, 'src/web/browser/liturgy/reader-study-view.js'));

class Node {
  constructor(tag, className, value) {
    this.tag = tag;
    this.tagName = tag.toUpperCase();
    this.parentNode = null;
    this.nodeType = tag === 'fragment' ? 11 : 1;
    this.className = className || '';
    this.textContent = value || '';
    this.children = [];
    this.dataset = {};
  }
  appendChild(child) { child.parentNode = this; this.children.push(child); return child; }
  after(node) {
    const parent = this.parentNode;
    node.parentNode = parent;
    parent.children.splice(parent.children.indexOf(this) + 1, 0, node);
  }
  contains(node) { return this === node || this.children.some((child) => child.contains(node)); }
  querySelectorAll(selector) {
    assert.equal(selector, '[data-semantic-event-id]');
    return this.children.flatMap(child => [
      ...(child.dataset.semanticEventId ? [child] : []), ...child.querySelectorAll(selector)
    ]);
  }
  get firstChild() { return this.children[0] || null; }
  insertBefore(child, before) {
    const index = this.children.indexOf(before);
    this.children.splice(index < 0 ? this.children.length : index, 0, child);
    return child;
  }
}

globalThis.document = {createDocumentFragment() { return new Node('fragment'); }};
globalThis.Triptych = {el(tag, className, value) {
  return new Node(tag, className, value);
}};

function fixture(name) {
  const data = JSON.parse(readFileSync(resolve(ROOT,
    `tools/tests/fixtures/liturgy-reader-state/v1/${name}.json`), 'utf8'));
  return {
    entrance: data.requested.entrance,
    request: data.requested,
    resolved: data.expected.resolved,
    calendarResult: data.expected.calendarResult,
    events: data.expected.events,
    coverage: data.expected.coverage,
    unresolvedChoices: data.expected.unresolvedChoices
  };
}

function textOf(node) {
  return node.textContent + node.children.map(textOf).join('');
}

function readingOf(result, prefix = '') {
  const fragment = document.createDocumentFragment();
  const contents = result.events.map((event) => {
    const element = Triptych.el('section', 'source-reading', 'HELD SOURCE BODY ' + event.id);
    element.dataset.semanticEventId = event.id;
    element.dataset.semanticLocation = prefix + event.id;
    fragment.appendChild(element);
    return {id: prefix + event.id, label: event.editionSlotLabel || event.id, element};
  });
  return {fragment, contents};
}

test('Day Study attaches calendar context before the unchanged source event sequence', () => {
  const result = fixture('day-roman-1962-2026-08-02');
  const projected = Study.project(result);
  assert.equal(projected.calendar.winner, 'pentecost-10');
  assert.equal(projected.calendar.date, '2026-08-02');
  assert.deepEqual(projected.events.map((one) => one.id), result.events.map((one) => one.id));
  const source = readingOf(result, 'branch/universal/');
  const first = source.contents[0].element;
  const originalText = textOf(first);
  const rendered = Study.attach({result, ...source, locationPrefix: 'branch/universal/'});
  assert.equal(rendered.fragment, source.fragment);
  assert.equal(rendered.contents, source.contents);
  assert.equal(rendered.fragment.children[1], first);
  assert.equal(rendered.semanticIds[0], 'branch/universal/' + result.events[0].id);
  assert.match(textOf(rendered.fragment.children[0]), /Calendar result/);
  assert.match(textOf(first), new RegExp(originalText));
  assert.equal(first.dataset.semanticLocation, 'branch/universal/' + result.events[0].id);
  assert.equal(first.children[0].tag, 'aside');
  assert.match(textOf(first.children[0]), /Source record/);
});

test('Propers Study names its date-independent boundary without a calendar result', () => {
  const result = fixture('propers-roman-1962-advent-1');
  const rendered = Study.attach({result, ...readingOf(result)});
  assert.deepEqual(rendered.semanticIds, result.events.map((one) => one.id));
  assert.match(textOf(rendered.fragment.children[0]), /date-independent/);
  assert.doesNotMatch(textOf(rendered.fragment.children[0]), /Calendar result/);
  assert.match(textOf(rendered.fragment), /HELD SOURCE BODY/);
});

test('unavailable bodies never enter Study while rights, absence, seat, and source remain', () => {
  const result = fixture('day-roman-1962-2026-08-02');
  result.events[1].selected = {
    kind: 'composed', availability: 'unavailable',
    language: 'en', rights: 'rights-restricted', reason: 'translation-missing',
    text: 'PROTECTED WORDS MUST NOT ESCAPE'
  };
  result.events[1].seat = {
    id: 'unplaced/source', placement: 'unseated',
    region: 'before-frame', basis: 'explicit source placement'
  };
  result.coverage.push({state: 'unavailable', scope: 'selected-translation',
    reasons: [{kind: 'text-withheld', basis: 'specific witness restriction'}]});
  result.unresolvedChoices.push({id: 'choice-1', reason: 'two source options',
    options: [{id: 'one'}, {id: 'two'}], sourceHooks: []});
  const projected = Study.project(result);
  assert.ok(!('text' in projected.events[1].selected));
  const rendered = Study.attach({result, ...readingOf(result)});
  const output = textOf(rendered.fragment);
  assert.doesNotMatch(output, /PROTECTED WORDS MUST NOT ESCAPE/);
  assert.match(output, /rights-restricted/);
  assert.match(output, /translation-missing/);
  assert.match(output, /explicit source placement/);
  assert.match(output, /specific witness restriction/);
  assert.match(output, /two source options/);
  assert.deepEqual(rendered.semanticIds, result.events.map((one) => one.id));
});

test('invalid identity and date claims fail closed', () => {
  const repeated = fixture('day-roman-1962-2026-08-02');
  repeated.events.push(structuredClone(repeated.events[0]));
  assert.throws(() => Study.project(repeated), /distinct stable identities/);

  const dated = fixture('propers-roman-1962-advent-1');
  dated.calendarResult = {date: '2026-08-02'};
  assert.throws(() => Study.project(dated), /date-independent/);

  const source = readingOf(dated);
  source.contents[0].element.dataset.semanticEventId = 'incorrect';
  assert.throws(() => Study.attach({result: fixture('propers-roman-1962-advent-1'),
    ...source}), /identities disagree/);
});

test('unrendered source placeholders and unresolved choice context do not invent bodies', () => {
  const result = fixture('day-roman-1962-2026-08-02');
  result.unresolvedChoices.push({id: 'held-choice', reason: 'source alternatives remain',
    options: [{id: 'first'}, {id: 'second'}], sourceHooks: []});
  const fragment = document.createDocumentFragment();
  const contents = [];
  const rendered = Study.attach({result, fragment, contents});
  assert.deepEqual(rendered.semanticIds, []);
  assert.deepEqual(rendered.contents, []);
  assert.match(textOf(fragment), /Unresolved choices/);
  assert.doesNotMatch(textOf(fragment), /HELD SOURCE BODY/);
});


test('Ordinary division Study apparatus follows its heading without nesting headings or duplicating IDs', () => {
  const result = fixture('day-roman-1962-2026-08-02');
  result.events[0].kind = 'ordinary-section';
  const source = readingOf(result);
  const heading = source.contents[0].element;
  heading.tag = 'h2';
  heading.tagName = 'H2';
  const original = textOf(heading);
  const ids = result.events.map(one => one.id);
  const rendered = Study.attach({result, ...source});
  assert.equal(textOf(heading), original);
  assert.deepEqual(heading.children, []);
  assert.equal(rendered.fragment.children[1], heading);
  const apparatus = rendered.fragment.children[2];
  assert.equal(apparatus.tag, 'aside');
  assert.equal(apparatus.dataset.studyEventId, ids[0]);
  assert.equal(apparatus.dataset.semanticEventId, undefined);
  assert.deepEqual(rendered.semanticIds, ids);
  assert.deepEqual(rendered.contents.map(one => one.element.dataset.semanticEventId), ids);
});


test('Ordinary source events receive Study facts without adding Contents destinations', () => {
  const result = fixture('day-roman-1962-2026-08-02');
  const source = readingOf(result);
  result.events[1].kind = 'ordinary-element';
  const ordinary = source.contents[1].element;
  source.contents.splice(1, 1);
  const ids = source.contents.map(one => one.id);
  const rendered = Study.attach({result, ...source});
  assert.deepEqual(rendered.contents.map(one => one.id), ids);
  assert.equal(ordinary.children[0].tag, 'aside');
  assert.equal(ordinary.children[0].dataset.studyEventId, result.events[1].id);
  assert.match(textOf(ordinary.children[0]), /ordinary-element/);
});
