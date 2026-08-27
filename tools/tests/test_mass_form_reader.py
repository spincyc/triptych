#!/usr/bin/env python3
"""Focused fail-closed browser/CLI adapter contracts for Mass forms."""

from __future__ import annotations

import json
import subprocess
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]

NODE = r"""
const fs = require('fs');
const C = require('./src/web/browser/liturgy/reader-state.js');
const A = require('./src/web/browser/liturgy/reader-state-adapters.js');
const input = JSON.parse(fs.readFileSync(0, 'utf8'));

function proper(name, form, ordinal) {
  const scripture = name === 'Introit';
  return {
    name,
    form: 'Synthetic ' + form,
    form_id: form,
    source: scripture ? 'scripture' : 'composed',
    text: scripture ? null : 'synthetic-contract-' + form + '-' + ordinal,
    citations: scripture ? [{ref: 'Synthetic ' + form + ' ' + ordinal, unresolved: null}] : [],
    cycles: {}, translations: [], taken_from: null
  };
}

function mass(key, ids) {
  const forms = ids.map((id, index) => ({
    id, name: 'Synthetic ' + id, ordinal: index + 1,
    propers: [proper('Introit', id, 1), proper('Collect', id, 2)],
    placeholders: 0
  }));
  return {
    key, kind: 'synthetic-contract', forms,
    propers: forms.flatMap((form) => form.propers)
  };
}

function request(key, form, ordinary) {
  const held = {
    schema: C.STATE_SCHEMA, entrance: 'day', civilDate: '2026-12-25',
    edition: {id: 'synthetic-edition'}, calendar: {id: 'synthetic-edition'},
    selectedReadableFormulary: {id: key},
    bible: {id: 'synthetic-bible', numbering: 'vulgate'},
    languages: {orations: 'la', ordinary: 'en'}, requestedMode: 'read',
    options: {ordinary: Boolean(ordinary), legitimate: {}},
    coverage: [], unresolvedChoices: [], sourceHooks: []
  };
  if (form !== undefined && form !== null) held.form = form;
  return held;
}

function adapt(key, ids, selected, ordinary) {
  const heldMass = mass(key, ids);
  const heldRequest = request(key, selected, ordinary);
  const ordinaryFile = ordinary
    ? JSON.parse(fs.readFileSync('src/web/data/structure/ordinary/roman-1962.json', 'utf8'))
    : null;
  return A.adaptDay({
    request: heldRequest,
    derived: {
      date: heldRequest.civilDate, calendar: heldRequest.calendar.id,
      liturgicalYear: {lectionary: {sunday: 'A', weekday: 'II'}},
      options: [{
        option: null, winner: {id: key}, settled: true,
        readable: [{key, state: 'said'}], absent: []
      }]
    },
    structure: {calendar: 'synthetic-edition', translations: [], masses: [heldMass]},
    ordinary: ordinaryFile
  });
}

function projection(result) {
  return {
    resolved: result.resolved,
    proper: result.events.filter((event) => event.kind === 'proper').map((event) => ({
      id: event.id,
      label: event.editionSlotLabel,
      seat: event.seat && {id: event.seat.id, placement: event.seat.placement},
      references: event.selected.references || [],
      text: Object.prototype.hasOwnProperty.call(event.selected, 'text')
        ? event.selected.text : null
    })),
    ordinary: result.events.filter((event) => event.kind !== 'proper').map((event) => event.id),
    choices: (result.unresolvedChoices || []).map((choice) => ({
      id: choice.id, options: choice.options.map((option) => option.id)
    }))
  };
}

let output;
if (input.op === 'selected') {
  output = projection(adapt(input.key, input.ids, input.form, true));
} else if (input.op === 'unresolved') {
  output = projection(adapt(input.key, input.ids, null, true));
} else if (input.op === 'invalid') {
  try {
    adapt(input.key, input.ids, input.form, true);
    output = {threw: false};
  } catch (error) {
    output = {threw: true, message: error.message};
  }
} else if (input.op === 'no-form') {
  const key = 'synthetic-main';
  const heldMass = {
    key, kind: 'synthetic-contract', forms: [],
    propers: [proper('Introit', 'main', 1), proper('Collect', 'main', 2)].map((row) => {
      row.form = null;
      return row;
    })
  };
  const heldRequest = request(key, input.form, false);
  try {
    const result = A.adaptDay({
      request: heldRequest,
      derived: {
        date: heldRequest.civilDate, calendar: heldRequest.calendar.id,
        liturgicalYear: {lectionary: {sunday: 'A', weekday: 'II'}},
        options: [{option: null, winner: {id: key}, settled: true,
          readable: [{key, state: 'said'}], absent: []}]
      },
      structure: {calendar: 'synthetic-edition', translations: [], masses: [heldMass]}
    });
    output = {threw: false, result: projection(result)};
  } catch (error) {
    output = {threw: true, message: error.message};
  }
} else if (input.op === 'legacy-concatenation') {
  const key = 'synthetic-legacy';
  const heldMass = mass(key, ['first', 'second']);
  delete heldMass.forms;
  try {
    A.adaptDay({
      request: request(key, null, false),
      derived: {date: '2026-12-25', calendar: 'synthetic-edition',
        liturgicalYear: {lectionary: {sunday: 'A', weekday: 'II'}},
        options: [{option: null, winner: {id: key}, settled: true,
          readable: [{key, state: 'said'}], absent: []}]},
      structure: {calendar: 'synthetic-edition', translations: [], masses: [heldMass]}
    });
    output = {threw: false};
  } catch (error) {
    output = {threw: true, message: error.message};
  }
} else if (input.op === 'legacy-main') {
  const key = 'synthetic-legacy-main';
  const heldMass = {
    key, kind: 'synthetic-contract', propers: [
      proper('Introit', 'main', 1), proper('Collect', 'main', 2)
    ].map((row) => {
      delete row.form;
      delete row.form_id;
      return row;
    })
  };
  try {
    const result = A.adaptDay({
      request: request(key, null, false),
      derived: {date: '2026-12-25', calendar: 'synthetic-edition',
        liturgicalYear: {lectionary: {sunday: 'A', weekday: 'II'}},
        options: [{option: null, winner: {id: key}, settled: true,
          readable: [{key, state: 'said'}], absent: []}]},
      structure: {calendar: 'synthetic-edition', translations: [], masses: [heldMass]}
    });
    output = {threw: false, result: projection(result)};
  } catch (error) {
    output = {threw: true, message: error.message};
  }
} else if (input.op === 'url') {
  const parsed = C.parseLegacy(input.entrance, input.hash);
  const normalized = C.normalizeLegacy(parsed, {
    context: {
      bibles: {'synthetic-bible': {numbering: 'vulgate'}},
      missals: {'synthetic-edition': {
        calendar: 'synthetic-edition', orationLanguages: ['la'],
        ordinaryLanguages: ['en'], variantGroups: {},
        types: {'synthetic-contract': ['synthetic-christmas', 'synthetic-main']},
        formsByMass: {'synthetic-christmas': ['night', 'dawn', 'day'], 'synthetic-main': []}
      }},
      dayReadableFormularies: [{id: input.mass, state: 'said'}]
    },
    defaults: input.entrance === 'day'
      ? {date: '2026-12-25', missal: 'synthetic-edition', bible: 'synthetic-bible',
          orations: 'la', why: '0', ordinary: '0', rubrics: '1'}
      : {missal: 'synthetic-edition', type: 'synthetic-contract', mass: input.mass,
          bible: 'synthetic-bible', orations: 'la',
          ...(Object.prototype.hasOwnProperty.call(input, 'defaultMass')
            ? {mass: input.defaultMass} : {})}
  });
  output = {normalized};
  if (normalized.ok) output.serialized = C.serializeLegacy(normalized);
}
process.stdout.write(JSON.stringify(output));
"""


def node_call(payload: dict) -> dict:
    run = subprocess.run(
        ["node", "-e", NODE], input=json.dumps(payload), text=True,
        capture_output=True, cwd=ROOT, check=False,
    )
    if run.returncode:
        raise AssertionError(run.stdout + run.stderr)
    return json.loads(run.stdout)


class MassFormReaderTests(unittest.TestCase):
    CASES = (
        ("synthetic-christmas", ["night", "dawn", "day"]),
        ("synthetic-all-souls", ["first", "second", "third"]),
        ("synthetic-ember", ["longer", "shorter"]),
    )

    def test_explicit_form_is_an_exact_source_order_subsequence(self) -> None:
        for key, ids in self.CASES:
            selected = ids[1]
            result = node_call({"op": "selected", "key": key, "ids": ids, "form": selected})
            self.assertEqual(result["resolved"]["form"], selected)
            self.assertEqual([row["label"] for row in result["proper"]], ["Introit", "Collect"])
            self.assertEqual(len(result["proper"]), 2)
            # IDs retain their offsets in the source's full ordered inventory;
            # selecting a form does not renumber or concatenate its Proper rows.
            self.assertTrue(result["proper"][0]["id"].endswith("/003"), key)
            self.assertTrue(result["proper"][1]["id"].endswith("/004"), key)
            self.assertTrue(all(row["seat"]["placement"] == "seated"
                                for row in result["proper"]), key)

    def test_unselected_multi_form_mass_has_no_events_or_order_default(self) -> None:
        for key, ids in self.CASES:
            result = node_call({"op": "unresolved", "key": key, "ids": ids})
            self.assertEqual(result["proper"], [])
            self.assertEqual(result["ordinary"], [])
            self.assertNotIn("form", result["resolved"])
            self.assertEqual(result["choices"], [{
                "id": f"proper-form:synthetic-edition/{key}", "options": ids,
            }])

    def test_unsupported_and_legacy_multi_form_states_fail_closed(self) -> None:
        result = node_call({
            "op": "invalid", "key": "synthetic-christmas",
            "ids": ["night", "dawn", "day"], "form": "not-held",
        })
        self.assertTrue(result["threw"])
        self.assertIn("unsupported form", result["message"])
        legacy = node_call({"op": "legacy-concatenation"})
        self.assertTrue(legacy["threw"])
        self.assertIn("stable form identities", legacy["message"])

    def test_provably_single_form_v1_payload_normalizes_to_main(self) -> None:
        legacy = node_call({"op": "legacy-main"})
        self.assertFalse(legacy["threw"], legacy)
        self.assertEqual(len(legacy["result"]["proper"]), 2)
        self.assertNotIn("form", legacy["result"]["resolved"])

    def test_main_sentinel_is_internal_and_never_selectable(self) -> None:
        held = node_call({"op": "no-form"})
        self.assertFalse(held["threw"])
        self.assertNotIn("form", held["result"]["resolved"])
        self.assertEqual(len(held["result"]["proper"]), 2)
        explicit = node_call({"op": "no-form", "form": "main"})
        self.assertTrue(explicit["threw"])
        self.assertIn("unsupported", explicit["message"])

    def test_form_url_round_trip_and_invalid_explicit_refusal(self) -> None:
        for entrance, prefix in (
            ("day", "#date=2026-12-25&missal=synthetic-edition&bible=synthetic-bible"),
            ("propers", "#missal=synthetic-edition&type=synthetic-contract&mass=synthetic-christmas&bible=synthetic-bible"),
        ):
            if entrance == "day":
                prefix += "&mass=synthetic-christmas"
            valid = node_call({
                "op": "url", "entrance": entrance, "mass": "synthetic-christmas",
                "hash": prefix + "&form=night",
            })
            self.assertTrue(valid["normalized"]["ok"], valid["normalized"]["errors"])
            self.assertEqual(valid["normalized"]["state"]["form"], "night")
            self.assertIn("form=night", valid["serialized"])
            invalid = node_call({
                "op": "url", "entrance": entrance, "mass": "synthetic-christmas",
                "hash": prefix + "&form=not-held",
            })
            self.assertFalse(invalid["normalized"]["ok"])
            self.assertIn("invalid-explicit-value", {
                error["code"] for error in invalid["normalized"]["errors"]
            })

    def test_form_without_mass_and_internal_main_refuse_in_both_entrances(self) -> None:
        cases = (
            ("day", "#date=2026-12-25&missal=synthetic-edition&bible=synthetic-bible",
             {}),
            ("propers", "#missal=synthetic-edition&type=synthetic-contract&bible=synthetic-bible",
             {"defaultMass": None}),
        )
        for entrance, bare, extra in cases:
            without_mass = node_call({
                "op": "url", "entrance": entrance, "mass": "synthetic-christmas",
                "hash": bare + "&form=night", **extra,
            })
            self.assertFalse(without_mass["normalized"]["ok"], entrance)
            self.assertIn("invalid-explicit-value", {
                error["code"] for error in without_mass["normalized"]["errors"]
            })

            with_mass = bare + "&mass=synthetic-main&form=main"
            internal_main = node_call({
                "op": "url", "entrance": entrance, "mass": "synthetic-main",
                "hash": with_mass, **extra,
            })
            self.assertFalse(internal_main["normalized"]["ok"], entrance)
            self.assertIn("invalid-explicit-value", {
                error["code"] for error in internal_main["normalized"]["errors"]
            })


if __name__ == "__main__":
    unittest.main()
