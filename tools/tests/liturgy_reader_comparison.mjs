#!/usr/bin/env node

/* Real production-data checks for the pure two-side Proper comparison. */

import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { resolve } from 'node:path';
import { createRequire } from 'node:module';
import test from 'node:test';

const ROOT = resolve(import.meta.dirname, '../..');
const require = createRequire(import.meta.url);
const Assembly = require(resolve(ROOT, 'src/web/browser/liturgy/assembly-model.js'));
const Adapters = require(resolve(ROOT, 'src/web/browser/liturgy/reader-state-adapters.js'));
const Comparison = require(resolve(ROOT, 'src/web/browser/liturgy/reader-comparison.js'));
const DATA = 'src/web/data/structure/';
const FIXTURES = 'tools/tests/fixtures/liturgy-reader-comparison/v1/';

function json(path) { return JSON.parse(readFileSync(resolve(ROOT, path), 'utf8')); }
function fixture(id) { return json(FIXTURES + id + '.json'); }
function clone(value) { return structuredClone(value); }

function dayInput(spec) {
  const template = json('tools/tests/fixtures/liturgy-reader-state/v1/day-roman-1962-2026-08-02.json').requested;
  const comparison = spec.comparison;
  const date = comparison.anchor.civilDate;
  return {
    comparison,
    sides: comparison.sides.map((side) => {
      const id = side.edition.id;
      const request = clone(template);
      request.civilDate = date;
      request.edition = { id };
      request.calendar = { id: side.calendar.id };
      request.requestedMode = 'read';
      delete request.selectedReadableFormulary;
      const derived = Assembly.derive({
        date,
        year: json(DATA + 'calendar/' + side.calendar.id + '/2026.json'),
        rubrics: json(DATA + 'rubrics/' + side.calendar.id + '.json')
      });
      return {
        id: side.id,
        result: Adapters.adaptDay({
          request, derived, structure: json(DATA + 'propers/' + id + '.json')
        })
      };
    })
  };
}

function propersInput(spec) {
  const template = json('tools/tests/fixtures/liturgy-reader-state/v1/propers-roman-1962-advent-1.json').requested;
  const comparison = spec.comparison;
  return {
    comparison,
    sides: comparison.sides.map((side) => {
      const id = side.edition.id;
      const request = clone(template);
      request.edition = { id };
      request.formulary = { id: side.formulary.id, type: 'seasonal' };
      request.languages = { orations: side.languages.orations };
      request.requestedMode = 'read';
      return {
        id: side.id,
        result: Adapters.adaptPropers({
          request, structure: json(DATA + 'propers/' + id + '.json')
        })
      };
    })
  };
}

function checkFixture(spec, input, view) {
  assert.equal(spec.schema, 'triptych-liturgy-reader-comparison-fixture/v1');
  for (const path of spec.basis.paths) assert.ok(json(path));
  assert.equal(view.schema, 'triptych-liturgy-reader-comparison/v1');
  assert.deepEqual(view.anchor, spec.comparison.anchor);
  assert.equal(view.dimension, spec.comparison.dimension);
  assert.equal(view.units.length, spec.expected.unitCount);
  assert.deepEqual(view.calendarResults && view.calendarResults.map((row) => ({
    id: row.id, winner: row.calendarResult.winner, formulary: row.resolved.formulary
  })), spec.expected.calendar);
  assert.deepEqual(view.sides.map((side) => side.id), spec.comparison.sides.map((side) => side.id));
  for (const side of input.sides) {
    assert.strictEqual(view.sides.find((row) => row.id === side.id).result, side.result);
    const missing = view.units.filter((unit) => unit.sides.find((row) => row.id === side.id)
      .status === 'no-event-in-selected-formulary').map((unit) => unit.semanticSlot);
    const unavailable = view.units.filter((unit) => unit.sides.find((row) => row.id === side.id)
      .status === 'text-unavailable').map((unit) => unit.semanticSlot);
    assert.deepEqual(missing, spec.expected.oneSided[side.id]);
    assert.deepEqual(unavailable, spec.expected.textUnavailable[side.id]);
  }
  for (const unit of view.units) assert.equal(unit.relation, 'functional-slot-only');
}

test('Day resolves each calendar and shows one-sided Proper events separately from missing text', () => {
  const spec = fixture('day-2026-11-22');
  const input = dayInput(spec);
  const before = JSON.stringify(input);
  const view = Comparison.compare(input);
  checkFixture(spec, input, view);
  assert.equal(view.entrance, 'day');
  assert.notEqual(view.calendarResults[0].resolved.formulary,
    view.calendarResults[1].resolved.formulary);
  assert.equal(view.units.find((unit) => unit.semanticSlot === 'gradual').sides[1].event, null);
  assert.equal(view.units.find((unit) => unit.semanticSlot === 'collect').sides[1]
    .event.selected.availability, 'unavailable');
  for (const unit of view.units) {
    for (const cell of unit.sides) {
      if (cell.event) {
        assert.equal(cell.event.semanticSlot.identity.id, unit.semanticSlot);
        assert.ok(cell.event.sourceHooks.length > 0);
      }
    }
  }
  assert.equal(JSON.stringify(input), before, 'comparison does not mutate independently derived sides');
});

test('source order does not decide functional-slot pairing', () => {
  const input = dayInput(fixture('day-2026-11-22'));
  const expected = Comparison.compare(input).units.map((unit) => ({
    slot: unit.semanticSlot,
    ids: unit.sides.map((side) => side.event && side.event.id)
  }));
  input.sides[1].result.events.reverse();
  const actual = Comparison.compare(input).units.map((unit) => ({
    slot: unit.semanticSlot,
    ids: unit.sides.map((side) => side.event && side.event.id)
  }));
  assert.deepEqual(actual, expected);
});

test('Propers keeps its date-independent formulary and distinguishes untranslated orations', () => {
  const spec = fixture('propers-roman-1962-advent-1-orations');
  const input = propersInput(spec);
  const view = Comparison.compare(input);
  checkFixture(spec, input, view);
  assert.equal(view.entrance, 'propers');
  assert.equal(view.calendarResults, null);
  for (const slot of spec.expected.textUnavailable.en) {
    const unit = view.units.find((row) => row.semanticSlot === slot);
    assert.equal(unit.sides[0].status, 'text-held');
    assert.equal(unit.sides[1].event.selected.reason, spec.expected.unavailableReason);
  }
  assert.ok(view.units.every((unit) => unit.sides.every((side) => side.event)));
  assert.deepEqual(view.sides.map((side) => side.result.request.civilDate), [null, null]);
});

test('mismatched anchors and unsupported correspondence fail closed', () => {
  const day = dayInput(fixture('day-2026-11-22'));
  day.comparison.anchor.civilDate = '2026-11-29';
  assert.throws(() => Comparison.compare(day), /independently resolve the anchored calendar/);

  const propers = propersInput(fixture('propers-roman-1962-advent-1-orations'));
  propers.sides[1].result.resolved.edition = 'postconciliar';
  assert.throws(() => Comparison.compare(propers), /edition does not match/);

  const mixed = propersInput(fixture('propers-roman-1962-advent-1-orations'));
  mixed.sides[1].result.request.bible = { id: 'king-james-version' };
  assert.throws(() => Comparison.compare(mixed), /same edition, form, formulary, Bible/);
});

test('duplicate, unmapped, and unresolved Proper choices cannot be paired by position', () => {
  const spec = fixture('day-2026-11-22');
  const duplicate = dayInput(spec);
  duplicate.sides[0].result.events.push(clone(duplicate.sides[0].result.events[0]));
  assert.throws(() => Comparison.compare(duplicate), /duplicate Proper slot/);

  const unmapped = dayInput(spec);
  unmapped.sides[0].result.events[0].semanticSlot = { state: 'edition-local-unmapped' };
  assert.throws(() => Comparison.compare(unmapped), /unmapped or unsupported Proper slot/);

  const choice = dayInput(spec);
  choice.sides[0].result.events[0].kind = 'proper-choice';
  assert.throws(() => Comparison.compare(choice), /only resolved Proper events/);

  const open = dayInput(spec);
  open.sides[0].result.unresolvedChoices.push({ id: 'unresolved' });
  assert.throws(() => Comparison.compare(open), /choices that remain unresolved/);
});
