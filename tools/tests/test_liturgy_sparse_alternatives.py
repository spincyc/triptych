#!/usr/bin/env python3
"""Source-owned regression gates for authored sparse Proper alternatives."""

from __future__ import annotations

import json
import shutil
import subprocess
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
ADAPTERS = ROOT / "src/web/browser/liturgy/reader-state-adapters.js"


NODE_BRIDGE = r"""
'use strict';
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const input = JSON.parse(fs.readFileSync(0, 'utf8'));
const C = require(path.resolve('src/web/browser/liturgy/reader-state.js'));
const A = require(input.adapters);
const M = require(path.resolve('src/web/browser/liturgy/assembly-model.js'));
const read = name => JSON.parse(fs.readFileSync('src/web/data/' + name, 'utf8'));
const structure = read('structure/propers/postconciliar.json');
const rubrics = read('structure/rubrics/postconciliar.json');
const bibles = read('bibles.json');
const original = JSON.stringify({structure, rubrics, bibles});
const clone = value => JSON.parse(JSON.stringify(value));
const sacred = 'most-sacred-heart-jesus';
const thursday = 'ot-12-thursday';
const massOf = (held, key) => held.masses.find(mass => mass.key === key);
const acclamationAlternative = mass => {
  const row = mass.propers.find(row => row.ordinary_disposition?.option === '1-john-4-10b');
  assert(row, 'the source retains the alternative Gospel Acclamation');
  return row;
};
const choiceId = (mass, group) => 'proper-choice/postconciliar/' + mass + '/main/' + group;
const properId = (mass, offset) => 'proper/postconciliar/' + mass + '/' + String(offset + 1).padStart(3, '0');
const members = result => result.events.flatMap(event => event.kind === 'proper-choice' ?
  event.options.flatMap(option => option.events) : [event]);

function dayCase(date, mass, language = 'en') {
  const derived = M.derive({date,
    year: read('structure/calendar/postconciliar/' + date.slice(0, 4) + '.json'), rubrics});
  assert(derived.options.some(branch => (branch.readable || []).some(row => row.key === mass)),
    date + ': exact source formulary is readable');
  const bible = bibles.bibles.find(row => row.id ===
    (language === 'la' ? 'clementine-vulgate' : 'douay-rheims'));
  assert(bible);
  const request = {
    schema: C.STATE_SCHEMA, entrance: 'day', civilDate: date,
    edition: {id: 'postconciliar'}, calendar: {id: 'postconciliar'},
    bible: {id: bible.id, numbering: bible.numbering || null},
    languages: {orations: language}, requestedMode: 'read',
    options: {ordinary: false, legitimate: {}}, selectedReadableFormulary: {id: mass},
    coverage: [], unresolvedChoices: [], sourceHooks: []
  };
  assert(C.validateReaderState(request).ok);
  return {request, derived, structure, ordinary: null};
}

function propersCase(mass, cycle, alternative) {
  const held = massOf(structure, mass);
  const context = A.validationContext({entrance: 'propers', bibles,
    properIndex: read('structure/propers/index.json'),
    rubricsIndex: read('structure/rubrics/index.json'),
    ordinaryIndex: {calendars: []}, structures: {postconciliar: structure}, ordinaries: {}});
  const fields = {missal: 'postconciliar', type: held.kind, mass,
    bible: 'douay-rheims', orations: 'en', cycle, mode: 'read'};
  if (alternative) fields.alternative = alternative;
  const hash = '#' + Object.entries(fields).map(([key, value]) =>
    key + '=' + encodeURIComponent(value)).join('&');
  const normalized = C.normalizeLegacy(C.parseLegacy('propers', hash), {
    context, defaults: {missal: 'postconciliar', bible: 'douay-rheims', orations: 'en'}});
  assert(normalized.ok, JSON.stringify(normalized.errors));
  assert.equal(normalized.state.cycle, cycle);
  if (alternative) assert.equal(normalized.state.alternative.id, alternative);
  return {request: normalized.state, structure, ordinary: null};
}

function mutateMass(held, mutate) {
  const key = held.request.selectedReadableFormulary.id;
  const selected = massOf(held.structure, key);
  const mass = clone(selected);
  mutate(mass);
  return {...held, structure: {...held.structure,
    masses: held.structure.masses.map(row => row === selected ? mass : row)}};
}

function checkResult(result, mass) {
  assert.equal(result.resolved.formulary, mass);
  const ids = members(result).map(member => member.id);
  assert.equal(new Set(ids).size, ids.length);
  for (const member of members(result)) {
    assert.deepEqual(C.validateSelectedMaterial(member.selected, 'selected'), []);
    assert.deepEqual(C.validateSemanticSlot(member.semanticSlot, 'semanticSlot'), []);
    assert(member.sourceHooks.some(hook => hook.kind === 'proper-structure'));
  }
  for (const choice of result.events.filter(event => event.kind === 'proper-choice')) {
    assert.equal(choice.selection.state, 'required');
    assert.equal(choice.selection.option, null);
    assert(choice.options.length >= 2);
  }
}

if (input.op === 'actual-days') {
  const cases = [['2026-06-12', sacred], ['2027-06-04', sacred], ['2028-06-23', sacred],
    ['2026-06-25', thursday], ['2027-06-24', thursday], ['2028-06-29', thursday]];
  for (const [date, mass] of cases) for (const language of ['en', 'la']) {
    const held = dayCase(date, mass, language);
    const result = A.adaptDay(held);
    checkResult(result, mass);
    if (date === '2028-06-29') assert.equal(result.resolved.standing, 'displaced');
    if (mass === sacred) {
      delete held.request.selectedReadableFormulary;
      const defaultResult = A.adaptDay(held);
      assert.equal(defaultResult.resolved.formulary, mass);
      assert.deepEqual(defaultResult.events, result.events);
    }
  }
} else if (input.op === 'source-identities') {
  for (const language of ['en', 'la']) {
    const a = A.adaptDay(dayCase('2026-06-12', sacred, language));
    const b = A.adaptDay(dayCase('2027-06-04', sacred, language));
    const c = A.adaptDay(dayCase('2028-06-23', sacred, language));
    const id = choiceId(sacred, 'gospel-acclamation');
    const authored = massOf(structure, sacred).propers;
    const offsets = authored.map((row, offset) => ({row, offset})).filter(one =>
      one.row.ordinary_disposition && one.row.ordinary_disposition.group === 'gospel-acclamation');
    for (const result of [b, c]) {
      const choice = result.events.find(event => event.id === id);
      assert.deepEqual(choice.options.map(option => option.id),
        offsets.map(one => one.row.ordinary_disposition.option));
      assert.deepEqual(choice.options.map(option => option.events[0].id),
        offsets.map(one => properId(sacred, one.offset)));
    }
    const primary = b.events.find(event => event.id === id).options[0].events[0];
    const held = a.events.find(event => event.id === primary.id);
    assert(held);
    assert.deepEqual(held.selected, primary.selected);
    assert.deepEqual(held.sourceHooks.filter(hook => hook.kind !== 'proper-choice-option'), primary.sourceHooks);
    assert(held.sourceHooks.some(hook => hook.kind === 'proper-choice-option' &&
      hook.id === id + '/' + offsets[0].row.ordinary_disposition.option));
    assert(!a.events.some(event => event.id === id));
    assert(!members(a).some(event => event.id === properId(sacred, offsets[1].offset)));
    const ii = A.adaptDay(dayCase('2026-06-25', thursday, language));
    const reading = ii.events.find(event => event.id === properId(thursday, 0));
    assert.equal(reading.selected.cycle, 'II');
    assert.equal(reading.selected.cycleDimension, 'weekday');
    assert.deepEqual(reading.selected.references,
      massOf(structure, thursday).propers[0].weekday_cycles.II.citations.map(row => row.ref));
    assert(reading.sourceHooks.some(hook => hook.kind === 'proper-choice-option' &&
      hook.id === choiceId(thursday, 'first-reading') + '/longer'));
    assert(ii.events.some(event => event.id === properId(thursday, 2)));
    const i = A.adaptDay(dayCase('2027-06-24', thursday, language));
    const choice = i.events.find(event => event.id === choiceId(thursday, 'first-reading'));
    assert.deepEqual(choice.options.map(option => option.id), ['longer', 'shorter']);
    assert.deepEqual(choice.options.map(option => option.events[0].id),
      [properId(thursday, 0), properId(thursday, 1)]);
  }
} else if (input.op === 'explicit-alternatives') {
  for (const [mass, cycle, group, held, excluded] of [
    [sacred, 'A', 'gospel-acclamation', 'matthew-11-29ab', '1-john-4-10b'],
    [thursday, 'II', 'first-reading', 'longer', 'shorter']]) {
    const id = choiceId(mass, group) + '/' + held;
    const result = A.adaptPropers(propersCase(mass, cycle, id));
    assert.equal(result.resolved.alternative, id);
    assert(result.events.some(event => event.sourceHooks.some(hook =>
      hook.kind === 'proper-choice-option' && hook.id === id)));
    const stale = propersCase(mass, cycle, choiceId(mass, group) + '/' + excluded);
    assert.throws(() => A.adaptPropers(stale), /explicit Propers alternative is not held/);
  }
  for (const [mass, cycle, group, option] of [
    [sacred, 'B', 'gospel-acclamation', '1-john-4-10b'],
    [sacred, 'C', 'gospel-acclamation', 'matthew-11-29ab'],
    [thursday, 'I', 'first-reading', 'shorter']]) {
    const id = choiceId(mass, group) + '/' + option;
    const result = A.adaptPropers(propersCase(mass, cycle, id));
    assert.equal(result.resolved.alternative, id);
    const choice = result.events.find(event => event.id === choiceId(mass, group));
    assert.deepEqual(choice.selection, {state: 'selected', option});
    assert(choice.options.find(one => one.id === option).events.some(event =>
      event.sourceHooks.some(hook => hook.kind === 'proper-choice-option' && hook.id === id)));
  }
} else if (input.op === 'strict-refusals') {
  const cases = [
    mutateMass(dayCase('2026-06-12', sacred), mass => {delete mass.propers.find(row => row.name === 'First Reading').cycles.A;}),
    mutateMass(dayCase('2026-06-12', sacred), mass => {
      acclamationAlternative(mass).cycles.Z = clone(acclamationAlternative(mass).cycles.B);}),
    mutateMass(dayCase('2026-06-12', sacred), mass => {
      acclamationAlternative(mass).weekday_cycles = {I: clone(acclamationAlternative(mass).cycles.B)};}),
    mutateMass(dayCase('2026-06-25', thursday), mass => {delete mass.propers.find(row => row.name === 'First Reading').weekday_cycles.II;})
  ];
  for (const held of cases) assert.throws(() => A.adaptDay(held),
    /not held|unsupported Lectionary cycle keys|both Sunday and weekday|no option for the selected cycle/);
  const invalid = dayCase('2026-06-12', sacred);
  invalid.derived = clone(invalid.derived);
  invalid.derived.liturgicalYear.lectionary.sunday = 'Z';
  assert.throws(() => A.adaptDay(invalid), /resolved Sunday Lectionary year is not held/);
  const missing = dayCase('2026-06-12', sacred);
  missing.derived = clone(missing.derived);
  missing.derived.liturgicalYear.lectionary = null;
  assert.throws(() => A.adaptDay(missing), /no resolved Lectionary year/);
} else if (input.op === 'whole-option-validation') {
  const held = mutateMass(dayCase('2026-06-12', sacred), mass => {
    const row = clone(acclamationAlternative(mass));
    row.cycles.Z = clone(row.cycles.B);
    mass.propers.splice(5, 0, row);
  });
  assert.throws(() => A.adaptDay(held), /unsupported Lectionary cycle keys/);
  const badStatus = mutateMass(dayCase('2026-06-12', sacred), mass => {
    acclamationAlternative(mass).cycles.B.text_status = {state: 'unavailable', scope: 'invented-scope'};
  });
  assert.throws(() => A.adaptDay(badStatus), /text_status/);
} else if (input.op === 'input-and-api-contract') {
  for (const held of [dayCase('2026-06-12', sacred), dayCase('2026-06-25', thursday),
    propersCase(sacred, 'A'), propersCase(thursday, 'II')]) {
    const before = JSON.stringify(held);
    if (held.request.entrance === 'day') A.adaptDay(held);
    else A.adaptPropers(held);
    assert.equal(JSON.stringify(held), before);
  }
  assert.deepEqual(Object.keys(A), ['properEventId', 'browseState', 'selectOrdinaryTranslation',
    'validationContext', 'adaptDay', 'adaptPropers', 'adaptCli']);
} else throw new Error('unknown regression operation');
assert.equal(JSON.stringify({structure, rubrics, bibles}), original);
process.stdout.write(JSON.stringify({ok: true}));
"""


class SparseAlternativeTests(unittest.TestCase):
    def check_node(self, operation: str) -> None:
        node = shutil.which("node")
        if node is None:
            self.skipTest("node is not installed")
        run = subprocess.run(
            [node, "-e", NODE_BRIDGE],
            input=json.dumps({"op": operation, "adapters": str(ADAPTERS)}),
            capture_output=True,
            text=True,
            cwd=ROOT,
            check=False,
        )
        self.assertEqual(run.returncode, 0, run.stdout + run.stderr)
        self.assertEqual(json.loads(run.stdout), {"ok": True})

    def test_actual_day_cycles_and_displaced_formulary_in_both_languages(self) -> None:
        self.check_node("actual-days")

    def test_original_event_option_and_current_cycle_identities(self) -> None:
        self.check_node("source-identities")

    def test_public_propers_url_accepts_applicable_and_refuses_stale_option(self) -> None:
        self.check_node("explicit-alternatives")

    def test_missing_primary_and_invalid_cycle_inputs_stay_refused(self) -> None:
        self.check_node("strict-refusals")

    def test_every_member_and_status_of_inapplicable_options_is_validated(self) -> None:
        self.check_node("whole-option-validation")

    def test_source_inputs_and_public_api_are_preserved(self) -> None:
        self.check_node("input-and-api-contract")


if __name__ == "__main__":
    unittest.main()
