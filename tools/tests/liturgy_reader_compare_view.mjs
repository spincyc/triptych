#!/usr/bin/env node

/* Focused Compare presentation checks, including unavailable-text isolation. */

import assert from 'node:assert/strict';
import { createRequire } from 'node:module';
import { resolve } from 'node:path';
import test from 'node:test';

const require = createRequire(import.meta.url);
const View = require(resolve(import.meta.dirname,
  '../../src/web/browser/liturgy/reader-compare-view.js'));

class Node {
  constructor(tag, className, value) {
    this.tag = tag;
    this.className = className || '';
    this.textContent = value || '';
    this.children = [];
    this.dataset = {};
  }
  appendChild(child) { this.children.push(child); return child; }
}

const rendered = [];
globalThis.document = { createDocumentFragment() { return new Node('fragment'); } };
globalThis.Triptych = {
  el(tag, className, value) { return new Node(tag, className, value); },
  renderProper(proper, _bible, _fragments, options) {
    rendered.push({proper, options});
    return new Node('section', 'proper', proper.text);
  }
};

function event(id, slot, availability, reason = null) {
  return {
    id: `proper/${id}/mass/001`, kind: 'proper',
    semanticSlot: {state: 'mapped', identity: {id: slot}},
    editionSlotLabel: 'Collect',
    selected: {availability, language: 'la', reason},
    sourceHooks: [{kind: 'proper-structure', id: `${id}/mass/001`}]
  };
}

function input(entrance = 'day') {
  const latin = event('roman-1962', 'collect', 'held');
  const absent = event('postconciliar', 'collect', 'unavailable', 'latin-withheld');
  const left = {id: 'roman-1962', result: {request: {languages: {orations: 'la'}}}};
  const right = {id: 'postconciliar', result: {request: {languages: {orations: 'la'}}}};
  const units = [
    {semanticSlot: 'collect', relation: 'functional-slot-only', sides: [
      {id: left.id, status: 'text-held', event: latin},
      {id: right.id, status: 'text-unavailable', event: absent}
    ]},
    {semanticSlot: 'gradual', relation: 'functional-slot-only', sides: [
      {id: left.id, status: 'text-held', event: event('roman-1962', 'gradual', 'held')},
      {id: right.id, status: 'no-event-in-selected-formulary', event: null}
    ]}
  ];
  const view = {
    schema: 'triptych-liturgy-reader-comparison/v1', entrance,
    dimension: entrance === 'day' ? 'recension' : 'oration-language',
    anchor: entrance === 'day'
      ? {civilDate: '2026-11-22', territorialContext: 'universal'}
      : {correspondingFormulary: 'mass'},
    sides: [left, right],
    calendarResults: entrance === 'day' ? [
      {id: left.id,
        calendarResult: {calendar: left.id, winner: 'last-sunday-after-pentecost'},
        resolved: {formulary: 'mass'}},
      {id: right.id,
        calendarResult: {calendar: right.id, winner: 'christ-the-king'},
        resolved: {formulary: 'mass'}}
    ] : null,
    units
  };
  const sides = [left, right].map((side) => ({
    id: side.id, label: side.id === left.id ? 'Roman 1962' : 'Postconciliar',
    structure: {calendar: side.id, numbering: 'vulgate'},
    mass: {key: 'mass', name: 'Named Mass', propers: [{name: 'Collect', text: 'held'}]},
    bible: {id: 'douay-rheims'}, fragments: new Map()
  }));
  return {view, sides};
}

function textOf(node) {
  return node.textContent + node.children.map(textOf).join('');
}

test('Day presents calendar differences before slot pairs and separates absent events from unavailable text', () => {
  rendered.length = 0;
  const result = View.render(input());
  assert.deepEqual(result.semanticIds, [
    'compare/calendar-result', 'compare/proper/collect', 'compare/proper/gradual'
  ]);
  assert.deepEqual(result.contents.map((one) => one.element.dataset.semanticLocation),
    result.semanticIds);
  assert.equal(result.fragment.children[1].className, 'compare-calendar-results');
  assert.match(textOf(result.fragment.children[1]), /different results/);
  assert.match(textOf(result.fragment), /selected text is unavailable/);
  assert.match(textOf(result.fragment), /No corresponding mapped Proper event/);
  assert.equal(rendered.length, 2, 'only held cells reach the production text renderer');
  assert.ok(rendered.every((one) => one.options.orations === 'la'));
});

test('Propers comparison remains date-independent and its Contents contain only Proper pairs', () => {
  const props = input('propers');
  const projection = View.project(props.view);
  assert.equal(projection.calendars, null);
  const result = View.render(props);
  assert.deepEqual(result.semanticIds, ['compare/proper/collect', 'compare/proper/gradual']);
  assert.doesNotMatch(textOf(result.fragment), /Calendar results on this date/);
});

test('view refuses mismatched side evidence, duplicate slots, and a held text without a source hook', () => {
  const wrong = input();
  wrong.view.units[0].sides[1].status = 'no-event-in-selected-formulary';
  assert.throws(() => View.project(wrong.view), /inconsistent side, event, or status/);

  const duplicate = input();
  duplicate.view.units.push(structuredClone(duplicate.view.units[0]));
  assert.throws(() => View.project(duplicate.view), /distinct mapped functional/);

  const missingSource = input();
  missingSource.view.units[0].sides[0].event.sourceHooks = [];
  assert.throws(() => View.render(missingSource), /source structure hook/);
});
