#!/usr/bin/env python3
"""Shared liturgy reader-state, URL, fixture, and consumer parity gates."""

from __future__ import annotations

import copy
import hashlib
import json
import shutil
import subprocess
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
FIXTURES = ROOT / "tools/tests/fixtures/liturgy-reader-state/v1"
DATA = ROOT / "src/web/data"
CONTRACT = ROOT / "src/web/browser/liturgy/reader-state.js"
ADAPTERS = ROOT / "src/web/browser/liturgy/reader-state-adapters.js"
ASSEMBLY = ROOT / "src/web/browser/liturgy/assembly-model.js"
SEATING = ROOT / "src/web/browser/liturgy/ordinary-seating.js"
MASS_TODAY = ROOT / "tools/mass-today"


NODE_BRIDGE = r"""
const fs = require('fs');
const C = require('./src/web/browser/liturgy/reader-state.js');
const A = require('./src/web/browser/liturgy/reader-state-adapters.js');
const M = require('./src/web/browser/liturgy/assembly-model.js');
const input = JSON.parse(fs.readFileSync(0, 'utf8'));
const reads = [];
const read = (path) => {
  reads.push(path);
  return JSON.parse(fs.readFileSync(path, 'utf8'));
};
const base = 'src/web/data/structure/';

function derive(id, date) {
  return M.derive({
    date,
    year: read(base + 'calendar/' + id + '/' + date.slice(0, 4) + '.json'),
    rubrics: read(base + 'rubrics/' + id + '.json')
  });
}

function context(entrance, id, date, includeOrdinary) {
  const held = date ? derive(id, date) : null;
  const structures = {};
  structures[id] = read(base + 'propers/' + id + '.json');
  const ordinaries = {};
  if (includeOrdinary) ordinaries[id] = read(base + 'ordinary/' + id + '.json');
  return A.validationContext({
    entrance,
    bibles: read('src/web/data/bibles.json'),
    properIndex: read(base + 'propers/index.json'),
    rubricsIndex: read(base + 'rubrics/index.json'),
    ordinaryIndex: includeOrdinary ? read(base + 'ordinary/index.json') : {calendars: []},
    structures,
    ordinaries,
    derived: held
  });
}

function selectedProjection(selected) {
  if (!selected) return null;
  return {
    kind: selected.kind || null,
    language: selected.language || null,
    cycle: selected.cycle || null,
    cycles: selected.cycles || [],
    references: selected.references || [],
    bible: selected.bible || null,
    numbering: selected.numbering || null,
    sourceId: selected.sourceId || null,
    rights: Object.prototype.hasOwnProperty.call(selected, 'rights') ? selected.rights : null,
    missing: Boolean(selected.missing),
    availability: selected.availability || null,
    absenceKey: selected.absenceKey || null,
    unresolvedWitnesses: selected.unresolvedWitnesses || [],
    text: Object.prototype.hasOwnProperty.call(selected, 'text') ? selected.text : null,
    alternatives: (selected.alternatives || []).map((alternative) => ({
      id: alternative.id,
      cycle: alternative.cycle,
      material: selectedProjection(alternative.material),
      sourceHooks: alternative.sourceHooks || []
    }))
  };
}

function eventProjection(event) {
  return {
    id: event.id,
    kind: event.kind,
    semanticSlot: event.semanticSlot || null,
    editionSlotLabel: event.editionSlotLabel || null,
    seat: event.seat ? {
      id: event.seat.id || null,
      placement: event.seat.placement || null,
      anchor: event.seat.anchor || null,
      where: event.seat.where || null
    } : null,
    selected: selectedProjection(event.selected),
    sourceHooks: event.sourceHooks || []
  };
}

function resultProjection(result) {
  return {
    resolved: result.resolved,
    calendarResult: result.calendarResult,
    events: (result.events || []).map(eventProjection),
    coverage: result.coverage || [],
    explicitAbsences: result.explicitAbsences || [],
    unresolvedChoices: result.unresolvedChoices || []
  };
}

let output;
if (input.op === 'fixture-validate') {
  output = input.fixtures.map((fixture) => C.validateFixture(fixture));
} else if (input.op === 'validate-states') {
  output = input.states.map((state) => C.validateReaderState(state));
} else if (input.op === 'source-hooks-presence') {
  const baseState = {
    schema: C.STATE_SCHEMA, entrance: 'day', civilDate: '2026-08-02',
    edition: {id: 'x'}, calendar: {id: 'x'}, requestedMode: 'read'
  };
  output = [undefined, null, false, '', {}, []].map((sourceHooks) => {
    const state = Object.assign({}, baseState, {sourceHooks});
    return C.validateReaderState(state);
  });
} else if (input.op === 'context') {
  output = context(input.entrance, input.id, input.date || null, Boolean(input.includeOrdinary));
} else if (input.op === 'context-trace') {
  const held = context(input.entrance, input.id, input.date || null, Boolean(input.includeOrdinary));
  output = {context: held, reads};
} else if (input.op === 'url') {
  const parsed = C.parseLegacy(input.entrance, input.hash, {variantKeys: input.variantKeys || []});
  const normalized = C.normalizeLegacy(parsed, {
    context: input.context,
    remembered: input.remembered || {},
    defaults: input.defaults || {}
  });
  output = {parsed, normalized};
  if (normalized.ok) {
    output.serialized = C.serializeLegacy(normalized);
    output.reparsed = C.parseLegacy(input.entrance, output.serialized, {
      variantKeys: input.variantKeys || []
    });
    output.renormalized = C.normalizeLegacy(output.reparsed, {
      context: input.context,
      remembered: input.reparseRemembered || input.remembered || {},
      defaults: input.defaults || {}
    });
    if (output.renormalized.ok) output.reserialized = C.serializeLegacy(output.renormalized);
  }
} else if (input.op === 'contract-probe') {
  const choice = C.unresolvedChoice('coequal', 'two options remain open', [
    {id: 'a', identity: {id: 'a'}}, {id: 'b', identity: {id: 'b'}}
  ]);
  const reversed = C.unresolvedChoice('coequal', 'two options remain open', [
    {id: 'b', identity: {id: 'b'}}, {id: 'a', identity: {id: 'a'}}
  ]);
  let forbiddenDefault = null;
  try {
    C.unresolvedChoice('bad', 'ordered default', [
      {id: 'a', identity: {id: 'a'}, default: true},
      {id: 'b', identity: {id: 'b'}}
    ]);
  } catch (error) { forbiddenDefault = error.message; }
  output = {
    malformedCoverage: C.validateReaderState({
      schema: C.STATE_SCHEMA, entrance: 'day', civilDate: '2026-08-02',
      edition: {id: 'x'}, calendar: {id: 'x'}, coverage: {}
    }),
    malformedChoices: C.validateReaderState({
      schema: C.STATE_SCHEMA, entrance: 'day', civilDate: '2026-08-02',
      edition: {id: 'x'}, calendar: {id: 'x'}, unresolvedChoices: {}
    }),
    unresolved: C.resolveAuthorizedChoice(choice),
    reversed: C.resolveAuthorizedChoice(reversed),
    explicit: C.resolveAuthorizedChoice(choice, 'b'),
    deterministic: C.resolveAuthorizedChoice(choice, null, 'a'),
    explicitInvalid: C.resolveAuthorizedChoice(choice, '', 'a'),
    forbiddenDefault,
    invalidCoverage: C.validateCoverage({
      state: 'supported', scope: 'x', completeness: 'complete',
      reasons: [{kind: 'unsupported-date'}]
    }),
    contradictoryCoverage: [
      {state: 'unavailable', scope: 'x', reasons: [{kind: 'unsupported-date'}]},
      {state: 'unsupported', scope: 'x', reasons: [{kind: 'translation-missing'}]},
      {state: 'supported', scope: 'x', completeness: 'partial', reasons: [{kind: 'semantic-absence'}]},
      {state: 'absent', scope: 'x', reasons: [{kind: 'text-not-held'}]}
    ].map((one) => C.validateCoverage(one)),
    dayMissing: C.validateReaderState({
      schema: C.STATE_SCHEMA, entrance: 'day', edition: {id: 'x'}
    }),
    propersValid: C.validateReaderState({
      schema: C.STATE_SCHEMA, entrance: 'propers', edition: {id: 'x'},
      formulary: {id: 'y'}, civilDate: null
    }),
    propersMissing: C.validateReaderState({
      schema: C.STATE_SCHEMA, entrance: 'propers', edition: {id: 'x'}
    }),
    browseValid: C.validateReaderState({
      schema: C.STATE_SCHEMA, entrance: 'propers', edition: {id: 'x'},
      browse: {kind: 'browse-entry'}
    }),
    browseInvalid: C.validateReaderState({
      schema: C.STATE_SCHEMA, entrance: 'propers', edition: {id: 'x'}, browse: 'yes'
    }),
    invalidConditional: [
      {schema: C.STATE_SCHEMA, entrance: 'day', civilDate: '2026-08-02',
       edition: {id: 'x'}, calendar: {id: 'x', territory: {label: 'bad'}}},
      {schema: C.STATE_SCHEMA, entrance: 'day', civilDate: '2026-08-02',
       edition: {id: 'x'}, calendar: {id: 'x'}, cycle: 42},
      {schema: C.STATE_SCHEMA, entrance: 'day', civilDate: '2026-08-02',
       edition: {id: 'x'}, calendar: {id: 'x'}, alternative: {name: 'bad'}},
      {schema: C.STATE_SCHEMA, entrance: 'day', civilDate: '2026-08-02',
       edition: {id: 'x'}, calendar: {id: 'x'}, languages: {invented: 'x'}},
      {schema: C.STATE_SCHEMA, entrance: 'day', civilDate: '2026-08-02',
       edition: {id: 'x'}, calendar: {id: 'x'},
       options: {ordinary: 'yes', legitimate: {group: ''}}}
    ].map((one) => C.validateReaderState(one)),
    storageFree: C.safeRemembered({getItem() { throw new Error('blocked'); }}, 'day'),
    inventory: C.URL_INVENTORY,
    strictRollover: C.strictDate('2026-02-30')
  };
} else if (input.op === 'adapt-fixture') {
  const fixture = input.fixture;
  const request = fixture.requested;
  if (request.entrance === 'day') {
    const id = request.edition.id;
    output = resultProjection(A.adaptDay({
      request,
      derived: derive(id, request.civilDate),
      structure: read(base + 'propers/' + id + '.json')
    }));
  } else {
    output = resultProjection(A.adaptPropers({
      request,
      structure: read(base + 'propers/' + request.edition.id + '.json')
    }));
  }
} else if (input.op === 'adapt-cycle-fixture') {
  const fixture = input.fixture;
  const request = JSON.parse(JSON.stringify(fixture.requested));
  if (Object.prototype.hasOwnProperty.call(input, 'cycle')) request.cycle = input.cycle;
  if (Object.prototype.hasOwnProperty.call(input, 'alternative')) {
    request.alternative = input.alternative;
  }
  const structure = read(base + 'propers/' + request.edition.id + '.json');
  if (input.reverseCycles || input.onlyCycles) {
    for (const mass of structure.masses || []) {
      if (mass.key !== request.formulary.id) continue;
      for (const proper of mass.propers || []) {
        let entries = Object.entries(proper.cycles || {});
        if (input.onlyCycles) {
          entries = entries.filter(([cycle]) => input.onlyCycles.includes(cycle));
        }
        if (input.reverseCycles) entries.reverse();
        proper.cycles = Object.fromEntries(entries);
      }
    }
  }
  output = resultProjection(A.adaptPropers({request, structure}));
} else if (input.op === 'synthetic-composed-cycles') {
  const request = {
    schema: C.STATE_SCHEMA, entrance: 'propers', civilDate: null,
    edition: {id: 'synthetic-cycle-edition'},
    formulary: {id: 'synthetic-cycle-formulary', type: 'contract'},
    languages: {orations: 'la'}, requestedMode: 'read',
    options: {ordinary: false, legitimate: {}}, coverage: [],
    unresolvedChoices: [], sourceHooks: []
  };
  if (Object.prototype.hasOwnProperty.call(input, 'cycle')) request.cycle = input.cycle;
  const order = input.reverseCycles ? ['C', 'B', 'A'] : ['A', 'B', 'C'];
  const cycles = {};
  for (const cycle of order) {
    cycles[cycle] = {citations: [], text: 'contract-material-' + cycle};
  }
  output = resultProjection(A.adaptPropers({
    request,
    structure: {
      calendar: 'synthetic-cycle-edition', translations: [],
      masses: [{
        key: 'synthetic-cycle-formulary', kind: 'contract',
        propers: [{name: 'Collect', source: 'composed', text: null, citations: [], cycles}]
      }]
    }
  }));
} else if (input.op === 'full-parity') {
  const request = input.request;
  const id = request.edition.id;
  const held = derive(id, request.civilDate);
  const structure = read(base + 'propers/' + id + '.json');
  const ordinary = read(base + 'ordinary/' + id + '.json');
  const day = A.adaptDay({request, derived: held, structure, ordinary});
  const cli = A.adaptCli({
    request, payload: input.payload, derived: held, structure
  });
  output = {day: resultProjection(day), cli: resultProjection(cli)};
} else if (input.op === 'compare-day') {
  const fixture = input.fixture;
  const checked = C.validateFixture(fixture);
  if (!checked.ok) throw new Error(JSON.stringify(checked.errors));
  const comparison = fixture.requested.comparison;
  const anchor = comparison.anchor;
  const wantedTerritory = anchor.territorialContext === 'universal'
    ? null : anchor.territorialContext;
  const sides = [];
  for (const side of comparison.sides) {
    const held = derive(side.calendar.id, anchor.civilDate);
    const branches = held.options.filter((one) => one.option === wantedTerritory);
    if (branches.length !== 1) throw new Error('comparison territory has no unique branch');
    const branch = branches[0];
    const said = branch.readable.filter((one) => one.state === 'said');
    if (said.length !== 1) throw new Error('comparison side has no unique said formulary');
    sides.push({
      id: side.id, edition: side.edition.id, calendar: side.calendar.id,
      date: held.date, territory: branch.option,
      calendarResult: branch.winner && branch.winner.id,
      formulary: said[0].key
    });
  }
  output = {
    dimension: comparison.dimension,
    anchor,
    calendarResult: {
      date: anchor.civilDate,
      territorialContext: anchor.territorialContext,
      resolveEachSideIndependently: true,
      showCalendarDifferencesFirst: true
    },
    sides
  };
} else if (input.op === 'compare-propers') {
  const fixture = input.fixture;
  const checked = C.validateFixture(fixture);
  if (!checked.ok) throw new Error(JSON.stringify(checked.errors));
  output = {
    anchor: fixture.requested.comparison.anchor,
    civilDate: fixture.requested.civilDate,
    sides: fixture.requested.comparison.sides,
    resolved: {
      correspondence: fixture.requested.comparison.anchor.correspondingFormulary,
      dateIndependent: true
    }
  };
} else if (input.op === 'resolve-choice') {
  output = input.choices.map((one) => C.resolveAuthorizedChoice(one));
} else if (input.op === 'source-preferred-choice') {
  const request = {
    schema: C.STATE_SCHEMA, entrance: 'day', civilDate: '2026-08-03',
    edition: {id: 'synthetic-test-edition'}, calendar: {id: 'synthetic-test-edition'},
    selectedReadableFormulary: {id: 'synthetic-formulary'},
    requestedMode: 'read', options: {ordinary: false, legitimate: {}},
    coverage: [], unresolvedChoices: [], sourceHooks: []
  };
  output = resultProjection(A.adaptDay({
    request,
    derived: {
      date: '2026-08-03', calendar: 'synthetic-test-edition',
      options: [{
        option: null, winner: {id: 'synthetic-celebration'}, settled: true,
        readable: [{key: 'synthetic-formulary', state: 'said'}],
        massChoices: [{
          id: 'synthetic-choice', preferred: 'source-option-id',
          among: [
            {id: 'source-option-id', key: 'synthetic-formulary'},
            {id: 'other-source-option', key: 'other-formulary'}
          ]
        }]
      }]
    },
    structure: {
      calendar: 'synthetic-test-edition', translations: [],
      masses: [{key: 'synthetic-formulary', kind: 'contract', propers: []}]
    }
  }));
} else if (input.op === 'synthetic-propers') {
  const request = {
    schema: C.STATE_SCHEMA, entrance: 'propers', civilDate: null,
    edition: {id: 'synthetic-test-edition'},
    formulary: {id: 'synthetic-test-formulary', type: 'contract'},
    bible: {id: 'douay-rheims', numbering: 'vulgate'},
    languages: {orations: input.language || 'la'}, requestedMode: 'read',
    options: {ordinary: false, legitimate: {}}, coverage: [],
    unresolvedChoices: [], sourceHooks: []
  };
  const translations = (input.translationOrder || ['witness-a', 'witness-b']).map((id) => ({
    lang: 'en', source_id: id, rights: 'public-domain', text: 'contract-only'
  }));
  const structure = {
    calendar: 'synthetic-test-edition', translations: [],
    masses: [{
      key: 'synthetic-test-formulary', kind: 'contract', propers: [
        {name: 'Placeholder', source: 'composed', text: 'not held', citations: [], cycles: {}},
        {name: 'Introit', source: 'scripture', citations: [{ref: 'Synthetic ref', unresolved: null}], cycles: {}},
        {name: 'Collect', source: 'composed', text: 'synthetic latin', citations: [], cycles: {}, translations}
      ]
    }]
  };
  output = resultProjection(A.adaptPropers({request, structure}));
} else if (input.op === 'ordinary-coverage') {
  const request = input.request;
  const id = request.edition.id;
  output = resultProjection(A.adaptDay({
    request, derived: derive(id, request.civilDate),
    structure: read(base + 'propers/' + id + '.json'),
    ordinary: read(base + 'ordinary/' + id + '.json')
  }));
} else {
  throw new Error('unknown operation');
}
process.stdout.write(JSON.stringify(output));
"""


def node_call(payload: dict) -> object:
    if shutil.which("node") is None:
        raise unittest.SkipTest("node is not installed")
    run = subprocess.run(
        ["node", "-e", NODE_BRIDGE],
        input=json.dumps(payload),
        capture_output=True,
        text=True,
        cwd=ROOT,
        check=False,
    )
    if run.returncode:
        raise AssertionError(run.stdout + run.stderr)
    return json.loads(run.stdout)


def load_fixtures() -> list[dict]:
    return [json.loads(path.read_text(encoding="utf-8")) for path in sorted(FIXTURES.glob("*.json"))]


def fixture_named(name: str) -> dict:
    return json.loads((FIXTURES / (name + ".json")).read_text(encoding="utf-8"))


def assert_subset(test: unittest.TestCase, expected: object, actual: object, path: str = "") -> None:
    if isinstance(expected, dict):
        test.assertIsInstance(actual, dict, path)
        for key, value in expected.items():
            test.assertIn(key, actual, f"{path}.{key}")
            assert_subset(test, value, actual[key], f"{path}.{key}")
    elif isinstance(expected, list):
        test.assertIsInstance(actual, list, path)
        test.assertEqual(len(expected), len(actual), path)
        for index, value in enumerate(expected):
            assert_subset(test, value, actual[index], f"{path}[{index}]")
    else:
        test.assertEqual(expected, actual, path)


class ContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.probe = node_call({"op": "contract-probe"})

    def test_entrance_requirements_are_intentionally_different(self) -> None:
        self.assertFalse(self.probe["dayMissing"]["ok"])
        self.assertTrue(self.probe["propersValid"]["ok"])
        self.assertFalse(self.probe["propersMissing"]["ok"])
        self.assertTrue(self.probe["browseValid"]["ok"])
        self.assertFalse(self.probe["browseInvalid"]["ok"])

    def test_malformed_typed_rows_fail_without_throwing(self) -> None:
        self.assertFalse(self.probe["malformedCoverage"]["ok"])
        self.assertFalse(self.probe["malformedChoices"]["ok"])
        self.assertTrue(self.probe["invalidCoverage"])
        self.assertTrue(all(self.probe["contradictoryCoverage"]))
        self.assertTrue(all(not one["ok"] for one in self.probe["invalidConditional"]))

    def test_every_explicitly_present_malformed_v1_field_fails_closed(self) -> None:
        day = {
            "schema": "triptych-liturgy-reader-state/v1",
            "entrance": "day",
            "civilDate": "2026-08-02",
            "edition": {"id": "x"},
            "calendar": {"id": "x"},
            "requestedMode": "read",
        }
        states = []
        for field, values in {
            "bible": [None, False, "", []],
            "selectedReadableFormulary": [None, False, "", []],
            "semanticLocation": [None, False, "", []],
            "apparatus": [None, False, "", []],
        }.items():
            for value in values:
                state = copy.deepcopy(day)
                state[field] = value
                states.append(state)
        for requested_mode in ("", False, [], "invented"):
            state = copy.deepcopy(day)
            state["requestedMode"] = requested_mode
            states.append(state)
        for apparatus in (
            {"why": "yes", "rubrics": 9},
            {"why": False, "rubrics": True, "invented": False},
        ):
            state = copy.deepcopy(day)
            state["apparatus"] = apparatus
            states.append(state)
        state = copy.deepcopy(day)
        state["madeUp"] = {"anything": True}
        states.append(state)
        state = copy.deepcopy(day)
        state["comparison"] = False
        states.append(state)
        results = node_call({"op": "validate-states", "states": states})
        self.assertTrue(all(not result["ok"] for result in results))

    def test_explicit_source_hooks_require_an_array_even_for_undefined(self) -> None:
        results = node_call({"op": "source-hooks-presence"})
        self.assertEqual([result["ok"] for result in results], [
            False, False, False, False, False, True,
        ])

    def test_entrance_fields_and_mode_comparison_are_mutually_consistent(self) -> None:
        day = {
            "schema": "triptych-liturgy-reader-state/v1",
            "entrance": "day",
            "civilDate": "2026-08-02",
            "edition": {"id": "roman-1962"},
            "calendar": {"id": "roman-1962"},
            "requestedMode": "read",
        }
        propers = {
            "schema": "triptych-liturgy-reader-state/v1",
            "entrance": "propers",
            "civilDate": None,
            "edition": {"id": "roman-1962"},
            "formulary": {"id": "advent-1"},
            "requestedMode": "read",
        }
        invalid = []
        for field, value in (
            ("formulary", {"id": "advent-1"}),
            ("browse", {"kind": "browse-entry"}),
        ):
            state = copy.deepcopy(day)
            state[field] = value
            invalid.append(state)
        for field, value in (
            ("calendar", {"id": "roman-1962"}),
            ("selectedReadableFormulary", {"id": "advent-1"}),
        ):
            state = copy.deepcopy(propers)
            state[field] = value
            invalid.append(state)
        state = copy.deepcopy(propers)
        state["browse"] = {"kind": "browse-entry"}
        invalid.append(state)
        comparison = fixture_named("compare-day-2026-08-02")["requested"]["comparison"]
        state = copy.deepcopy(day)
        state["requestedMode"] = "compare"
        invalid.append(state)
        state = copy.deepcopy(day)
        state["comparison"] = comparison
        invalid.append(state)
        results = node_call({"op": "validate-states", "states": invalid})
        self.assertTrue(all(not result["ok"] for result in results))

        nullable = copy.deepcopy(day)
        nullable["requestedMode"] = None
        nullable["cycle"] = None
        nullable["comparison"] = None
        self.assertTrue(node_call({"op": "validate-states", "states": [nullable]})[0]["ok"])

    def test_unresolved_choices_never_select_by_order(self) -> None:
        self.assertIsNone(self.probe["unresolved"]["selected"])
        self.assertIsNone(self.probe["reversed"]["selected"])
        self.assertEqual(self.probe["explicit"]["selected"]["id"], "b")
        self.assertEqual(self.probe["deterministic"]["selected"]["id"], "a")
        self.assertFalse(self.probe["explicitInvalid"]["ok"])
        self.assertIn("default", self.probe["forbiddenDefault"])

    def test_source_preferred_option_can_bind_source_id_or_formulary_key(self) -> None:
        projected = node_call({"op": "source-preferred-choice"})
        self.assertEqual(projected["resolved"]["formulary"], "synthetic-formulary")
        self.assertEqual(projected["unresolvedChoices"], [])

    def test_storage_failure_and_calendar_rollover_fail_safely(self) -> None:
        self.assertEqual(self.probe["storageFree"], {})
        self.assertFalse(self.probe["strictRollover"])

    def test_inventory_names_every_current_key(self) -> None:
        day = self.probe["inventory"]["day"]
        propers = self.probe["inventory"]["propers"]
        self.assertEqual(
            day["hash"],
            ["date", "missal", "bible", "orations", "why", "ordinary",
             "ordinary-lang", "rubrics", "mass", "eucharistic-prayer"],
        )
        self.assertEqual(propers["hash"], ["missal", "type", "mass", "bible", "orations"])
        self.assertEqual(day["query"], ["data"])
        self.assertEqual(propers["query"], ["data", "missals"])


class FixtureTests(unittest.TestCase):
    def test_all_versioned_fixtures_validate(self) -> None:
        fixtures = load_fixtures()
        results = node_call({"op": "fixture-validate", "fixtures": fixtures})
        self.assertEqual(len(results), 7)
        for fixture, result in zip(fixtures, results):
            self.assertTrue(result["ok"], f"{fixture['id']}: {result['errors']}")

    def test_fixture_validator_rejects_malformed_semantic_evidence(self) -> None:
        base = fixture_named("day-roman-1962-2026-08-02")
        mutations = []
        for mutate in ("slot", "selection", "hook", "absence", "url"):
            fixture = copy.deepcopy(base)
            if mutate == "slot":
                fixture["expected"]["events"][0]["semanticSlot"] = {"state": "mapped"}
            elif mutate == "selection":
                fixture["expected"]["events"][0]["selected"].pop("availability")
            elif mutate == "hook":
                fixture["expected"]["events"][0]["sourceHooks"] = [{"kind": "proper-structure"}]
            elif mutate == "absence":
                fixture["expected"]["explicitAbsences"][0].pop("kind")
            else:
                fixture["expected"]["url"] = {"legacy": "not-a-hash", "canonical": "#ok=1"}
            mutations.append(fixture)
        results = node_call({"op": "fixture-validate", "fixtures": mutations})
        self.assertTrue(all(not result["ok"] for result in results))

    def test_fixture_validator_rejects_malformed_cycle_alternatives(self) -> None:
        base = fixture_named("propers-postconciliar-transfiguration-cycles")
        mutations = []
        for mutate in ("duplicate", "mismatch", "material", "hooks", "default"):
            fixture = copy.deepcopy(base)
            selected = fixture["expected"]["events"][-1]["selected"]
            if mutate == "duplicate":
                selected["alternatives"][1]["id"] = "A"
                selected["alternatives"][1]["cycle"] = "A"
                selected["alternatives"][1]["material"]["cycle"] = "A"
            elif mutate == "mismatch":
                selected["alternatives"][0]["material"]["cycle"] = "B"
            elif mutate == "material":
                selected["alternatives"][0]["material"] = None
            elif mutate == "hooks":
                selected["alternatives"][0]["sourceHooks"] = None
            else:
                selected["alternatives"][0]["default"] = True
            mutations.append(fixture)
        results = node_call({"op": "fixture-validate", "fixtures": mutations})
        self.assertTrue(all(not result["ok"] for result in results))

    def test_fixture_validator_binds_comparison_results_and_synthetic_visibility(self) -> None:
        comparison = fixture_named("compare-day-2026-08-02")
        mutations = []
        changed = copy.deepcopy(comparison)
        changed["expected"]["calendarResult"]["date"] = "2026-08-03"
        mutations.append(changed)
        changed = copy.deepcopy(comparison)
        changed["expected"]["resolved"]["sides"].append(copy.deepcopy(
            changed["expected"]["resolved"]["sides"][0]
        ))
        mutations.append(changed)
        changed = copy.deepcopy(comparison)
        changed["expected"]["resolved"]["sides"][0]["edition"] = "postconciliar"
        mutations.append(changed)
        synthetic = fixture_named("compare-propers-synthetic-correspondence")
        synthetic["visibility"] = "public-data"
        mutations.append(synthetic)
        results = node_call({"op": "fixture-validate", "fixtures": mutations})
        self.assertTrue(all(not result["ok"] for result in results))

    def test_public_fixture_basis_paths_exist(self) -> None:
        for fixture in load_fixtures():
            if fixture["visibility"] == "public-data":
                for path in fixture["basis"]["paths"]:
                    self.assertTrue((ROOT / path).is_file(), f"{fixture['id']}: {path}")

    def test_synthetic_fixtures_are_explicitly_non_public_and_claim_free(self) -> None:
        synthetic = [one for one in load_fixtures() if one["visibility"] == "synthetic-non-public"]
        self.assertEqual({one["id"] for one in synthetic}, {
            "compare-propers-synthetic-correspondence", "choice-synthetic-coequal"
        })
        for fixture in synthetic:
            self.assertTrue(fixture["synthetic"]["contractOnly"])
            self.assertFalse(fixture["synthetic"]["liturgicalText"])
            self.assertFalse(fixture["synthetic"]["historicalClaims"])

    def test_semantic_hashes_cover_only_ordered_event_ids(self) -> None:
        for fixture in load_fixtures():
            ids = "\n".join(row["id"] for row in fixture["expected"]["events"])
            digest = hashlib.sha256(ids.encode()).hexdigest()
            self.assertEqual(digest, fixture["expected"]["semanticHash"], fixture["id"])

    def test_read_context_loads_only_the_selected_semantic_catalogs(self) -> None:
        traced = node_call({
            "op": "context-trace", "entrance": "day", "id": "roman-1962",
            "date": "2026-08-02", "includeOrdinary": False,
        })
        reads = traced["reads"]
        self.assertIn("src/web/data/structure/propers/roman-1962.json", reads)
        self.assertIn("src/web/data/structure/calendar/roman-1962/2026.json", reads)
        self.assertIn("src/web/data/structure/rubrics/roman-1962.json", reads)
        self.assertFalse(any("/ordinary/" in path for path in reads))
        self.assertFalse(any("propers/postconciliar.json" in path for path in reads))
        self.assertFalse(any("calendar/postconciliar/" in path for path in reads))


class UrlContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.day_context = node_call({
            "op": "context", "entrance": "day", "id": "roman-1962", "date": "2026-08-02"
        })
        cls.post_context = node_call({
            "op": "context", "entrance": "day", "id": "postconciliar", "date": "2026-11-29",
            "includeOrdinary": True,
        })
        cls.propers_context = node_call({"op": "context", "entrance": "propers", "id": "roman-1962"})

    @staticmethod
    def defaults(fixture: dict) -> dict:
        request = fixture["requested"]
        defaults = {
            "missal": request["edition"]["id"],
            "bible": request.get("bible", {}).get("id", "douay-rheims"),
            "orations": request.get("languages", {}).get("orations", "la"),
        }
        if request["entrance"] == "day":
            defaults.update({
                "date": request["civilDate"], "why": "0", "ordinary": "0", "rubrics": "1",
            })
        else:
            defaults.update({"type": request["formulary"]["type"], "mass": request["formulary"]["id"]})
        return defaults

    def test_every_real_legacy_fixture_round_trips_canonically(self) -> None:
        for name, context in (
            ("day-roman-1962-2026-08-02", self.day_context),
            ("day-postconciliar-2026-11-29", self.post_context),
            ("propers-roman-1962-advent-1", self.propers_context),
        ):
            fixture = fixture_named(name)
            url = fixture["expected"]["url"]
            result = node_call({
                "op": "url", "entrance": fixture["requested"]["entrance"],
                "hash": url["legacy"], "context": context,
                "defaults": self.defaults(fixture),
                "variantKeys": ["eucharistic-prayer"] if fixture["requested"]["entrance"] == "day" else [],
            })
            self.assertTrue(result["normalized"]["ok"], result["normalized"]["errors"])
            self.assertEqual(result["serialized"], url["canonical"])
            self.assertEqual(result["reparsed"]["entrance"], fixture["requested"]["entrance"])
            self.assertTrue(result["renormalized"]["ok"], result["renormalized"]["errors"])
            self.assertEqual(result["renormalized"]["state"], result["normalized"]["state"])
            self.assertEqual(result["reserialized"], result["serialized"])

    def test_every_meaningful_legacy_key_has_a_positive_semantic_mapping(self) -> None:
        day_hash = (
            "#date=2026-11-29&missal=postconciliar&bible=douay-rheims&orations=en&"
            "why=1&ordinary=1&ordinary-lang=en&rubrics=0&mass=advent-1&"
            "eucharistic-prayer=ep-ii"
        )
        day = node_call({
            "op": "url", "entrance": "day", "hash": day_hash,
            "context": self.post_context,
            "defaults": {"date": "2026-11-29", "missal": "postconciliar",
                         "bible": "douay-rheims", "orations": "la", "why": "0",
                         "ordinary": "0", "ordinary-lang": "en", "rubrics": "1"},
            "variantKeys": ["eucharistic-prayer"],
        })
        self.assertTrue(day["normalized"]["ok"], day["normalized"]["errors"])
        state = day["normalized"]["state"]
        self.assertEqual(state["civilDate"], "2026-11-29")
        self.assertEqual(state["edition"]["id"], "postconciliar")
        self.assertEqual(state["bible"]["id"], "douay-rheims")
        self.assertEqual(state["languages"], {"orations": "en", "ordinary": "en"})
        self.assertEqual(state["apparatus"], {"why": True, "rubrics": False})
        self.assertTrue(state["options"]["ordinary"])
        self.assertEqual(state["options"]["legitimate"]["eucharistic-prayer"], "ep-ii")
        self.assertEqual(state["selectedReadableFormulary"]["id"], "advent-1")
        self.assertEqual(day["serialized"], day_hash)
        self.assertEqual(day["renormalized"]["state"], state)

        propers_hash = (
            "#missal=roman-1962&type=seasonal&mass=advent-1&"
            "bible=douay-rheims&orations=en"
        )
        propers = node_call({
            "op": "url", "entrance": "propers", "hash": propers_hash,
            "context": self.propers_context,
            "defaults": {"missal": "roman-1962", "type": "seasonal", "mass": "advent-1",
                         "bible": "douay-rheims", "orations": "la"},
        })
        self.assertTrue(propers["normalized"]["ok"], propers["normalized"]["errors"])
        self.assertEqual(propers["normalized"]["state"]["formulary"],
                         {"id": "advent-1", "type": "seasonal"})
        self.assertEqual(propers["normalized"]["state"]["languages"]["orations"], "en")
        self.assertEqual(propers["serialized"], propers_hash)
        self.assertEqual(propers["renormalized"]["state"], propers["normalized"]["state"])

    def test_canonical_state_is_independent_of_remembered_opposites_and_storage(self) -> None:
        defaults = {"date": "2026-08-02", "missal": "roman-1962",
                    "bible": "douay-rheims", "orations": "la", "why": "0",
                    "ordinary": "0", "ordinary-lang": "en", "rubrics": "1"}
        explicit = (
            "#date=2026-08-02&missal=roman-1962&bible=douay-rheims&orations=la&"
            "why=0&ordinary=0&ordinary-lang=en&rubrics=1"
        )
        result = node_call({
            "op": "url", "entrance": "day", "hash": explicit,
            "context": node_call({"op": "context", "entrance": "day", "id": "roman-1962",
                                  "date": "2026-08-02", "includeOrdinary": True}),
            "defaults": defaults,
            "remembered": {"orations": "en", "why": "1", "ordinary": "1", "rubrics": "0"},
            "reparseRemembered": {"orations": "en", "why": "1", "ordinary": "1", "rubrics": "0"},
            "variantKeys": ["eucharistic-prayer"],
        })
        self.assertTrue(result["normalized"]["ok"])
        self.assertEqual(result["serialized"], explicit)
        self.assertEqual(result["renormalized"]["state"], result["normalized"]["state"])

        storage_defaults = node_call({
            "op": "url", "entrance": "day", "hash": "",
            "context": self.day_context,
            "defaults": {key: value for key, value in defaults.items() if key != "ordinary-lang"},
            "remembered": self.probe_storage_free(),
            "variantKeys": ["eucharistic-prayer"],
        })
        self.assertTrue(storage_defaults["normalized"]["ok"])
        self.assertEqual(storage_defaults["normalized"]["legacy"]["sources"]["missal"],
                         "repository-default")

    @staticmethod
    def probe_storage_free() -> dict:
        return node_call({"op": "contract-probe"})["storageFree"]

    def test_explicit_url_state_outranks_remembered_preferences(self) -> None:
        result = node_call({
            "op": "url", "entrance": "day",
            "hash": "#date=2026-08-02&missal=roman-1962&bible=douay-rheims",
            "context": self.day_context,
            "remembered": {"missal": "postconciliar", "bible": "clementine-vulgate"},
            "defaults": {"date": "2026-08-02", "missal": "postconciliar", "bible": "douay-rheims",
                         "orations": "la", "why": "0", "ordinary": "0", "rubrics": "1"},
            "variantKeys": ["eucharistic-prayer"],
        })
        self.assertTrue(result["normalized"]["ok"])
        self.assertEqual(result["normalized"]["state"]["edition"]["id"], "roman-1962")
        self.assertEqual(result["normalized"]["state"]["bible"]["id"], "douay-rheims")
        self.assertEqual(result["normalized"]["legacy"]["sources"]["missal"], "url")

    def test_invalid_explicit_values_fail_closed(self) -> None:
        day_cases = [
            "#date=2026-02-30&missal=roman-1962&bible=douay-rheims",
            "#date=2026-08-02&missal=roman-pre-1955&bible=douay-rheims",
            "#date=2026-08-02&missal=roman-1962&bible=not-held",
            "#date=2026-08-02&missal=roman-1962&bible=douay-rheims&orations=xx",
            "#date=2026-08-02&missal=roman-1962&bible=douay-rheims&ordinary-lang=xx",
            "#date=2026-08-02&missal=roman-1962&bible=douay-rheims&mass=not-held",
            "#date=2026-08-02&date=2026-08-03&missal=roman-1962&bible=douay-rheims",
            "#date=2026-08-02&missal=roman-1962&bible=douay-rheims&why=2",
            "#date=2026-08-02&missal=roman-1962&bible=douay-rheims&ordinary=yes",
            "#date=2026-08-02&missal=roman-1962&bible=douay-rheims&rubrics=",
        ]
        defaults = {"date": "2026-08-02", "missal": "roman-1962", "bible": "douay-rheims",
                    "orations": "la", "why": "0", "ordinary": "0", "rubrics": "1"}
        for url in day_cases:
            result = node_call({
                "op": "url", "entrance": "day", "hash": url,
                "context": self.day_context, "defaults": defaults,
                "variantKeys": ["eucharistic-prayer"],
            })
            self.assertFalse(result["normalized"]["ok"], url)

        propers_cases = [
            "#missal=not-held&type=seasonal&mass=advent-1&bible=douay-rheims",
            "#missal=roman-1962&type=not-held&mass=advent-1&bible=douay-rheims",
            "#missal=roman-1962&type=seasonal&mass=not-held&bible=douay-rheims",
        ]
        defaults = {"missal": "roman-1962", "type": "seasonal", "mass": "advent-1",
                    "bible": "douay-rheims", "orations": "la"}
        for url in propers_cases:
            result = node_call({
                "op": "url", "entrance": "propers", "hash": url,
                "context": self.propers_context, "defaults": defaults,
            })
            self.assertFalse(result["normalized"]["ok"], url)

        variant = node_call({
            "op": "url", "entrance": "day",
            "hash": "#date=2026-11-29&missal=postconciliar&bible=douay-rheims&eucharistic-prayer=not-held",
            "context": self.post_context,
            "defaults": {"date": "2026-11-29", "missal": "postconciliar",
                         "bible": "douay-rheims", "orations": "la", "why": "0",
                         "ordinary": "0", "rubrics": "1"},
            "variantKeys": ["eucharistic-prayer"],
        })
        self.assertFalse(variant["normalized"]["ok"])

    def test_unknown_and_inapplicable_legacy_keys_are_preserved_but_never_applied(self) -> None:
        url = (
            "#date=2026-08-02&missal=roman-1962&bible=douay-rheims&orations=en&"
            "rubrics=0&eucharistic-prayer=ep-ii&cycle=B&alternative=x&x%26y=z&future-empty="
        )
        result = node_call({
            "op": "url", "entrance": "day", "hash": url,
            "context": self.day_context,
            "defaults": {"date": "2026-08-02", "missal": "roman-1962",
                         "bible": "douay-rheims", "orations": "la", "why": "0",
                         "ordinary": "0", "rubrics": "1"},
            "variantKeys": ["eucharistic-prayer"],
        })
        self.assertTrue(result["normalized"]["ok"], result["normalized"]["errors"])
        self.assertEqual(result["normalized"]["legacy"]["inert"][0]["key"], "eucharistic-prayer")
        self.assertNotIn("cycle", result["normalized"]["state"])
        self.assertNotIn("alternative", result["normalized"]["state"])
        self.assertEqual(
            [(one["key"], one["value"]) for one in result["reparsed"]["unknown"]],
            [("cycle", "B"), ("alternative", "x"), ("x&y", "z"), ("future-empty", "")],
        )

    def test_no_geolocation_or_storage_dependency_is_present(self) -> None:
        source = CONTRACT.read_text(encoding="utf-8") + ADAPTERS.read_text(encoding="utf-8")
        self.assertNotIn("geolocation", source)
        self.assertNotIn("navigator", source)
        self.assertNotIn("localStorage", source)
        self.assertNotIn("sessionStorage", source)


class ParityTests(unittest.TestCase):
    def test_source_ordinals_slots_and_translation_choices_are_stable(self) -> None:
        latin = node_call({"op": "synthetic-propers", "language": "la"})
        proper_events = [one for one in latin["events"] if one["kind"] == "proper"]
        self.assertEqual([one["id"] for one in proper_events], [
            "proper/synthetic-test-edition/synthetic-test-formulary/002",
            "proper/synthetic-test-edition/synthetic-test-formulary/003",
        ])
        self.assertEqual(proper_events[0]["semanticSlot"]["identity"]["id"],
                         "entrance-antiphon")
        self.assertEqual(proper_events[0]["editionSlotLabel"], "Introit")

        forward = node_call({
            "op": "synthetic-propers", "language": "en",
            "translationOrder": ["witness-a", "witness-b"],
        })
        reverse = node_call({
            "op": "synthetic-propers", "language": "en",
            "translationOrder": ["witness-b", "witness-a"],
        })
        for result in (forward, reverse):
            collect = next(one for one in result["events"] if one["editionSlotLabel"] == "Collect")
            self.assertEqual(collect["selected"]["availability"], "choice-required")
            self.assertIsNone(collect["selected"]["sourceId"])
            self.assertEqual(len(result["unresolvedChoices"]), 1)
            self.assertEqual(
                [one["id"] for one in result["unresolvedChoices"][0]["options"]],
                ["witness-a", "witness-b"],
            )

    def test_missing_ordinary_language_is_explicitly_unavailable(self) -> None:
        request = copy.deepcopy(fixture_named("day-roman-1962-2026-08-02")["requested"])
        request["options"]["ordinary"] = True
        request["languages"]["ordinary"] = "zz-contract-unheld"
        result = node_call({"op": "ordinary-coverage", "request": request})
        row = next(one for one in result["coverage"] if one["scope"].startswith("ordinary:"))
        self.assertEqual(row["state"], "unavailable")
        self.assertEqual(row["reasons"][0]["kind"], "language-missing")

    def test_real_day_and_propers_fixtures_match_current_semantics(self) -> None:
        for name in (
            "day-roman-1962-2026-08-02",
            "day-postconciliar-2026-11-29",
            "propers-roman-1962-advent-1",
            "propers-postconciliar-transfiguration-cycles",
        ):
            fixture = fixture_named(name)
            actual = node_call({"op": "adapt-fixture", "fixture": fixture})
            expected = fixture["expected"]
            assert_subset(self, expected["resolved"], actual["resolved"], name + ".resolved")
            assert_subset(self, expected["calendarResult"], actual["calendarResult"], name + ".calendar")
            assert_subset(self, expected["events"], actual["events"], name + ".events")
            self.assertEqual(actual["coverage"], expected["coverage"], name)
            self.assertEqual(actual["explicitAbsences"], expected["explicitAbsences"], name)

    def test_propers_cycles_are_structured_not_merged_or_order_selected(self) -> None:
        fixture = fixture_named("propers-postconciliar-transfiguration-cycles")
        forward = node_call({"op": "adapt-cycle-fixture", "fixture": fixture})
        reversed_result = node_call({
            "op": "adapt-cycle-fixture", "fixture": fixture, "reverseCycles": True,
        })
        self.assertEqual(forward, reversed_result)
        gospel = next(one for one in forward["events"] if one["editionSlotLabel"] == "Gospel")
        self.assertEqual(gospel["selected"]["kind"], "cycle-alternatives")
        self.assertEqual(gospel["selected"]["availability"], "choice-required")
        alternatives = gospel["selected"]["alternatives"]
        self.assertEqual([one["id"] for one in alternatives], ["A", "B", "C"])
        self.assertEqual(
            [one["material"]["references"] for one in alternatives],
            [["Matthew 17:1-9"], ["Mark 9:2-10"], ["Luke 9:28b-36"]],
        )
        self.assertTrue(all(one["material"]["availability"] == "held" for one in alternatives))
        self.assertTrue(all(one["sourceHooks"] for one in alternatives))

    def test_explicit_and_sole_propers_cycles_are_deterministic_and_invalid_fails(self) -> None:
        fixture = fixture_named("propers-postconciliar-transfiguration-cycles")
        selected = node_call({"op": "adapt-cycle-fixture", "fixture": fixture, "cycle": "B"})
        gospel = next(one for one in selected["events"] if one["editionSlotLabel"] == "Gospel")
        self.assertEqual(gospel["selected"]["kind"], "scripture")
        self.assertEqual(gospel["selected"]["cycle"], "B")
        self.assertEqual(gospel["selected"]["cycles"], ["B"])
        self.assertEqual(gospel["selected"]["references"], ["Mark 9:2-10"])
        self.assertEqual(gospel["selected"]["alternatives"], [])

        sole = node_call({
            "op": "adapt-cycle-fixture", "fixture": fixture, "onlyCycles": ["C"],
        })
        gospel = next(one for one in sole["events"] if one["editionSlotLabel"] == "Gospel")
        self.assertEqual(gospel["selected"]["cycle"], "C")
        self.assertEqual(gospel["selected"]["references"], ["Luke 9:28b-36"])

        with self.assertRaises(AssertionError):
            node_call({"op": "adapt-cycle-fixture", "fixture": fixture, "cycle": "Z"})
        with self.assertRaises(AssertionError):
            node_call({
                "op": "adapt-cycle-fixture", "fixture": fixture,
                "alternative": {"id": "not-held"},
            })

    def test_composed_cycle_material_keeps_each_alternative_text(self) -> None:
        forward = node_call({"op": "synthetic-composed-cycles"})
        reversed_result = node_call({"op": "synthetic-composed-cycles", "reverseCycles": True})
        self.assertEqual(forward, reversed_result)
        selected = forward["events"][0]["selected"]
        self.assertEqual(selected["kind"], "cycle-alternatives")
        self.assertEqual(
            [(one["cycle"], one["material"]["text"]) for one in selected["alternatives"]],
            [("A", "contract-material-A"), ("B", "contract-material-B"),
             ("C", "contract-material-C")],
        )
        explicit = node_call({"op": "synthetic-composed-cycles", "cycle": "B"})
        self.assertEqual(explicit["events"][0]["selected"]["text"], "contract-material-B")

    def test_propers_adapter_rejects_a_mismatched_formulary_type(self) -> None:
        fixture = fixture_named("propers-roman-1962-advent-1")
        fixture["requested"]["formulary"]["type"] = "saints"
        with self.assertRaises(AssertionError):
            node_call({"op": "adapt-fixture", "fixture": fixture})

    def test_mass_today_expanded_matches_day_identity_order_seats_and_sources(self) -> None:
        for name in ("day-roman-1962-2026-08-02", "day-postconciliar-2026-11-29"):
            fixture = fixture_named(name)
            request = copy.deepcopy(fixture["requested"])
            request["options"]["ordinary"] = True
            run = subprocess.run(
                [str(MASS_TODAY), "show", "--date", request["civilDate"],
                 "--calendar", request["edition"]["id"], "--bible", request["bible"]["id"],
                 "--expanded", "--why", "--format", "json"],
                capture_output=True, text=True, cwd=ROOT, check=False,
            )
            self.assertEqual(run.returncode, 0, run.stdout + run.stderr)
            payload = json.loads(run.stdout)
            parity = node_call({"op": "full-parity", "request": request, "payload": payload})
            self.assertEqual(parity["day"]["resolved"], parity["cli"]["resolved"], name)
            self.assertEqual(parity["day"]["calendarResult"], parity["cli"]["calendarResult"], name)
            self.assertEqual(parity["day"]["events"], parity["cli"]["events"], name)
            self.assertEqual(parity["day"]["coverage"], parity["cli"]["coverage"], name)
            self.assertEqual(parity["day"]["explicitAbsences"],
                             parity["cli"]["explicitAbsences"], name)
            self.assertEqual(parity["day"]["unresolvedChoices"],
                             parity["cli"]["unresolvedChoices"], name)
            proper_events = [one for one in parity["day"]["events"] if one["kind"] == "proper"]
            self.assertEqual(len(proper_events), 10)
            self.assertTrue(all(one["seat"]["placement"] == "seated" for one in proper_events))

    def test_cli_parity_rejects_bible_lectionary_reference_and_text_drift(self) -> None:
        fixture = fixture_named("day-roman-1962-2026-08-02")
        request = copy.deepcopy(fixture["requested"])
        request["options"]["ordinary"] = True
        run = subprocess.run(
            [str(MASS_TODAY), "show", "--date", request["civilDate"],
             "--calendar", request["edition"]["id"], "--bible", request["bible"]["id"],
             "--expanded", "--why", "--format", "json"],
            capture_output=True, text=True, cwd=ROOT, check=False,
        )
        self.assertEqual(run.returncode, 0, run.stdout + run.stderr)
        payload = json.loads(run.stdout)
        mutations = []
        changed = copy.deepcopy(payload)
        changed["scripture"]["id"] = "not-requested"
        mutations.append(changed)
        changed = copy.deepcopy(payload)
        changed["days"][0]["why"]["lectionary"] = {"sunday": "X", "weekday": "Y"}
        mutations.append(changed)
        changed = copy.deepcopy(payload)
        scripture = next(one for one in changed["days"][0]["masses"][0]["propers"] if one["verses"])
        scripture["verses"][0]["ref"] = "invented drift"
        mutations.append(changed)
        changed = copy.deepcopy(payload)
        composed = next(
            one for one in changed["days"][0]["masses"][0]["propers"] if one.get("text")
        )
        composed["text"] += " drift"
        mutations.append(changed)
        for changed in mutations:
            with self.assertRaises(AssertionError):
                node_call({"op": "full-parity", "request": request, "payload": changed})

    def test_day_compare_holds_date_and_context_then_resolves_each_side(self) -> None:
        fixture = fixture_named("compare-day-2026-08-02")
        actual = node_call({"op": "compare-day", "fixture": fixture})
        self.assertEqual(actual["dimension"], fixture["expected"]["resolved"]["dimension"])
        self.assertEqual(actual["anchor"], fixture["requested"]["comparison"]["anchor"])
        self.assertEqual(actual["calendarResult"], fixture["expected"]["calendarResult"])
        expected = fixture["expected"]["resolved"]["sides"]
        projected = [
            {key: side[key] for key in (
                "id", "edition", "calendar", "calendarResult", "formulary"
            )}
            for side in actual["sides"]
        ]
        self.assertEqual(projected, expected)
        self.assertTrue(all(side["date"] == fixture["requested"]["civilDate"]
                            for side in actual["sides"]))
        self.assertTrue(all(side["territory"] is None for side in actual["sides"]))
        self.assertNotEqual(actual["sides"][0]["formulary"], actual["sides"][1]["formulary"])

    def test_propers_compare_is_date_independent_and_choice_fixture_stays_open(self) -> None:
        comparison = fixture_named("compare-propers-synthetic-correspondence")
        projected = node_call({"op": "compare-propers", "fixture": comparison})
        self.assertIsNone(projected["civilDate"])
        self.assertEqual(projected["anchor"], comparison["requested"]["comparison"]["anchor"])
        self.assertEqual(projected["sides"], comparison["requested"]["comparison"]["sides"])
        self.assertEqual(projected["resolved"], comparison["expected"]["resolved"])
        choice = fixture_named("choice-synthetic-coequal")["requested"]["unresolvedChoices"][0]
        reversed_choice = copy.deepcopy(choice)
        reversed_choice["options"].reverse()
        result = node_call({"op": "resolve-choice", "choices": [choice, reversed_choice]})
        self.assertIsNone(result[0]["selected"])
        self.assertIsNone(result[1]["selected"])
        self.assertEqual([one["id"] for one in result[0]["unresolved"]["options"]],
                         ["synthetic-option-a", "synthetic-option-b"])
        self.assertEqual([one["id"] for one in result[1]["unresolved"]["options"]],
                         ["synthetic-option-b", "synthetic-option-a"])


class PublicBoundaryTests(unittest.TestCase):
    def test_synthetic_fixture_ids_do_not_enter_generated_public_data(self) -> None:
        corpus = "\n".join(
            path.read_text(encoding="utf-8", errors="replace")
            for path in (DATA).rglob("*.json")
        )
        for fixture in load_fixtures():
            if fixture["visibility"] == "synthetic-non-public":
                sentinels = {fixture["id"]}

                def collect(value: object) -> None:
                    if isinstance(value, str) and value.startswith("synthetic-"):
                        sentinels.add(value)
                    elif isinstance(value, dict):
                        for nested in value.values():
                            collect(nested)
                    elif isinstance(value, list):
                        for nested in value:
                            collect(nested)

                collect(fixture)
                for sentinel in sentinels:
                    self.assertNotIn(sentinel, corpus, f"public data contains {sentinel}")

    def test_release_binding_contains_contract_modules_but_no_fixture(self) -> None:
        release = json.loads((ROOT / "release/public-alpha.json").read_text(encoding="utf-8"))
        authorization = release["authorizations"]["perpetual-public-repository-2026"]
        sources = authorization["site_sources"]
        self.assertIn("src/web/browser/liturgy/reader-state.js", sources)
        self.assertIn("src/web/browser/liturgy/reader-state-adapters.js", sources)
        self.assertFalse(any("liturgy-reader-state/v1" in path for path in sources))

    def test_contract_is_not_loaded_by_current_production_routes(self) -> None:
        for name in ("day.html", "index.html"):
            page = (ROOT / "src/web/browser/liturgy" / name).read_text(encoding="utf-8")
            self.assertNotIn("reader-state.js", page)
            self.assertNotIn("reader-state-adapters.js", page)


if __name__ == "__main__":
    unittest.main()
