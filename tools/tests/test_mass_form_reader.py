#!/usr/bin/env python3
"""Focused fail-closed browser/CLI adapter contracts for Mass forms."""

from __future__ import annotations

import json
import os
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
    languages: {orations: 'la', ordinary: 'en'},
    requestedMode: ordinary ? 'missal' : 'read',
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
  if (ordinaryFile) ordinaryFile.calendar = 'synthetic-edition';
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
if (input.op === 'appointment-boundary') {
  const Seating = require('./src/web/browser/liturgy/ordinary-seating.js');
  const structure = JSON.parse(fs.readFileSync(
    'src/web/data/structure/propers/roman-1962.json', 'utf8'));
  const ordinary = JSON.parse(fs.readFileSync(
    'src/web/data/structure/ordinary/roman-1962.json', 'utf8'));
  const heldMass = structure.masses.find((one) => one.key === 'commune-summorum-pontificum');
  const conditional = heldMass.propers.find((proper) =>
    proper.ordinary_disposition && proper.ordinary_disposition.kind === 'conditional');
  let rawError = null;
  try { Seating.unframedEvents([conditional]); }
  catch (error) { rawError = error.message; }
  const before = JSON.stringify(heldMass);
  const result = A.adaptPropers({
    request: {
      schema: C.STATE_SCHEMA, entrance: 'propers', edition: {id: 'roman-1962'},
      formulary: {id: heldMass.key}, bible: {id: 'douay-rheims', numbering: 'vulgate'},
      languages: {orations: 'la', ordinary: 'la'}, requestedMode: 'missal',
      options: {ordinary: true, legitimate: {}},
      coverage: [], unresolvedChoices: [], sourceHooks: []
    }, structure, ordinary
  });
  output = {
    rawError, sourceUnchanged: JSON.stringify(heldMass) === before,
    prepared: projection(result),
    conditionalChoice: result.unresolvedChoices.some((choice) =>
      choice.id.startsWith('proper-condition/roman-1962/' + heldMass.key + '/'))
  };
} else if (input.op === 'selected') {
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
          orations: 'la', why: '0', ordinary: '0', rubrics: '1',
          ...(Object.prototype.hasOwnProperty.call(input, 'defaultMass')
            ? {mass: input.defaultMass} : {})}
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


# This is intentionally a production-data walk, rather than a fixture census.
# It crosses the same appointment owner as the reader before seating and keeps
# the static candidate census separate from the admitted event sequence. Global
# Proper offsets remain the IDs the adapters expose.
PRODUCTION_SEATING_NODE = r"""
const fs = require('fs');
const Seating = require('./src/web/browser/liturgy/ordinary-seating.js');

const calendars = (process.env.TRIPTYCH_SEATING_CALENDARS ||
  'roman-1962,roman-pre-1955,postconciliar').split(',').filter(Boolean);
const structureRoot = process.env.TRIPTYCH_STRUCTURE_ROOT || 'src/web/data';
const failures = [];
const report = {calendars: {}, failures};

function failure(calendar, mass, form, message) {
  failures.push({calendar, mass, form, message});
}

function effectiveFrame(mass, form) {
  return form.ordinary_frame || mass.ordinary_frame || {
    applicability: 'full', basis: null
  };
}

function formsOf(mass) {
  const forms = mass.forms || [];
  if (!forms.length) {
    return [{
      id: 'main', ordinary_frame: null,
      rows: (mass.propers || []).map((proper, sourceIndex) => ({proper, sourceIndex}))
    }];
  }
  let offset = 0;
  return forms.map((form) => {
    const rows = (form.propers || []).map((proper, localIndex) => ({
      proper, sourceIndex: offset + localIndex
    }));
    offset += rows.length;
    return {id: form.id, ordinary_frame: form.ordinary_frame || null, rows};
  });
}

function hasSelectionMarker(value) {
  return value && typeof value === 'object' &&
    (Object.prototype.hasOwnProperty.call(value, 'selected') ||
     Object.prototype.hasOwnProperty.call(value, 'default'));
}

function ordinarySelections(ordinary) {
  let selections = [{}];
  for (const group of ordinary.variants || []) {
    selections = selections.flatMap((held) => (group.options || []).map((option) =>
      Object.assign({}, held, {[group.group]: option.id})));
  }
  return selections;
}

function placedRows(placed) {
  const rows = (placed.before || []).concat(placed.after || []);
  for (const bucket of placed.buckets.values()) rows.push(...bucket);
  return rows;
}

for (const calendar of calendars) {
  const structure = JSON.parse(fs.readFileSync(
    structureRoot + '/structure/propers/' + calendar + '.json', 'utf8'));
  const ordinary = JSON.parse(fs.readFileSync(
    structureRoot + '/structure/ordinary/' + calendar + '.json', 'utf8'));
  const stats = report.calendars[calendar] = {
    masses: 0, forms: 0, full: 0, nonfull: 0, sourceOccurrences: 0,
    plainOccurrences: 0, alternativeOccurrences: 0, unplacedOccurrences: 0,
    choiceEvents: 0, candidates: 0, conditionalCandidates: 0,
    candidateChoiceGroups: 0, unadmittedPathCandidates: 0,
    unresolvedConditions: 0, inactiveConditions: 0, unresolvedPaths: 0,
    unsupportedForms: 0, unsupportedCandidates: 0
  };

  for (const mass of structure.masses || []) {
    stats.masses += 1;
    const manifest = mass.forms || [];
    if (manifest.length) {
      const ids = manifest.map((form) => form.id);
      if (new Set(ids).size !== ids.length || manifest.some((form, index) =>
          !form || form.ordinal !== index + 1 ||
          typeof form.id !== 'string' || !form.id)) {
        failure(calendar, mass.key, '*',
          'production form manifest lacks unique stable source-order identities');
      }
      const nested = manifest.flatMap((form) => form.propers || []);
      const flat = mass.propers || [];
      if (flat.length !== nested.length || flat.some((proper, index) =>
          JSON.stringify(proper) !== JSON.stringify(nested[index]))) {
        failure(calendar, mass.key, '*',
          'production form manifest does not partition the flat Proper inventory');
      }
    }
    for (const form of formsOf(mass)) {
      stats.forms += 1;
      const frame = effectiveFrame(mass, form);
      const application = frame && frame.applicability;
      const context = [calendar, mass.key, form.id];
      if (['full', 'none', 'unavailable'].indexOf(application) < 0) {
        failure(...context, 'effective Ordinary frame has invalid applicability');
        continue;
      }
      if (application !== 'full' &&
          (typeof frame.basis !== 'string' || !frame.basis.trim())) {
        failure(...context, 'non-full Ordinary frame has no source basis');
        continue;
      }

      const candidates = form.rows.filter((row) =>
        row.proper && row.proper.name !== 'Placeholder');
      const byIndex = new Map();
      candidates.forEach((row) => {
        if (row.proper.form_id !== form.id) {
          failure(...context,
            'source candidate does not retain form identity at ' + row.sourceIndex);
        }
        if (byIndex.has(row.sourceIndex)) {
          failure(...context, 'selected form repeats global sourceIndex ' + row.sourceIndex);
        }
        byIndex.set(row.sourceIndex, row);
      });
      let prepared;
      const before = JSON.stringify(form.rows);
      try {
        const checked = Seating.validateProperSeating(
          ordinary, form.rows.map((row) => row.proper), {
            calendar, mass: mass.key, form_id: form.id,
            full: application === 'full',
            facts: structure.proper_appointment_facts || {},
            sourcePaths: mass.proper_source_paths || []
          });
        if (checked.candidates !== candidates.length) {
          throw new Error('static seating did not conserve every source candidate');
        }
        stats.candidates += checked.candidates;
        stats.conditionalCandidates += checked.conditional_rows;
        stats.candidateChoiceGroups += checked.choice_groups;
        try {
          prepared = Seating.prepareProperAppointments(form.rows, {
            calendar, entrance: 'propers', mass: mass.key, formId: form.id,
            sourcePaths: mass.proper_source_paths || [], calendarCycles: {},
            date: null, season: null,
            facts: structure.proper_appointment_facts || {}, choices: {}
          });
        } catch (error) {
          if (!checked.diagnostics.length ||
              !/^unsupported foreign-source (Proper|path) applicability/.test(error.message)) {
            throw error;
          }
          stats.unsupportedForms += 1;
          stats.unsupportedCandidates += candidates.length;
          continue;
        }
        if (checked.diagnostics.length) {
          throw new Error('foreign source candidates escaped their runtime refusal');
        }
        stats.unresolvedConditions += prepared.unresolved.length;
        stats.inactiveConditions += prepared.inactive.length;
        stats.unresolvedPaths += prepared.sourcePathUnresolved.length;
      } catch (error) {
        failure(...context, 'appointment preparation refused: ' + error.message);
        continue;
      } finally {
        if (JSON.stringify(form.rows) !== before) {
          failure(...context, 'appointment validation mutated authored source rows');
        }
      }
      const selected = prepared.rows.filter((row) =>
        row.proper && row.proper.name !== 'Placeholder');
      const accounted = new Set(selected.map((row) => row.sourceIndex));
      prepared.unresolved.concat(prepared.inactive).forEach((row) => {
        if (accounted.has(row.sourceIndex)) {
          failure(...context, 'one source candidate has multiple applicability states');
        }
        accounted.add(row.sourceIndex);
      });
      for (const row of candidates) {
        if (accounted.has(row.sourceIndex)) continue;
        const relation = (mass.proper_source_paths || []).find((one) =>
          one.id === row.proper.source_path_relation && one.form_id === form.id);
        if (!relation) {
          failure(...context,
            'source candidate disappeared without a conditional or source-path disposition');
        } else {
          stats.unadmittedPathCandidates += 1;
        }
      }
      stats.sourceOccurrences += selected.length;

      let events;
      let placed = null;
      try {
        if (application === 'full') {
          stats.full += 1;
          const predicates = {};
          if (selected.some((row) => row.proper.name === 'Second Reading')) {
            predicates['second-reading-appointed'] = true;
          }
          const shown = Seating.shownElements(ordinary, null, predicates);
          placed = Seating.seatPropers(
            prepared.rows,
            Seating.seats(ordinary, shown),
            (proper) => proper && proper.name === 'Placeholder',
            prepared.selections
          );
          events = Seating.massEvents(shown, placed);
          for (const selection of ordinarySelections(ordinary)) {
            try {
              const branchShown = Seating.shownElements(ordinary, selection, predicates);
              const branchPlaced = Seating.seatPropers(
                prepared.rows,
                Seating.seats(ordinary, branchShown),
                (proper) => proper && proper.name === 'Placeholder',
                prepared.selections
              );
              if (branchPlaced.broke || branchPlaced.sourceCount !== selected.length ||
                  placedRows(branchPlaced).some((row) => !row || !row.seat)) {
                throw new Error('branch has an unexplained or backwards Proper row');
              }
            } catch (error) {
              failure(...context,
                'Ordinary option branch refused ' + JSON.stringify(selection) +
                ': ' + error.message);
              break;
            }
          }
        } else {
          stats.nonfull += 1;
          events = Seating.unframedEvents(
            prepared.rows, (proper) => proper && proper.name === 'Placeholder',
            prepared.selections);
        }
      } catch (error) {
        failure(...context, 'seating refused: ' + error.message);
        continue;
      }

      if (placed && placed.broke) {
        failure(...context, 'full-frame seating walked backwards');
      }
      if (placed && placed.sourceCount !== selected.length) {
        failure(...context, 'seating sourceCount did not conserve selected rows');
      }

      const appearances = new Map();
      const unitOrder = [];
      const choiceGroups = new Map();
      function appearance(row, owner, option) {
        if (!appearances.has(row.sourceIndex)) appearances.set(row.sourceIndex, []);
        appearances.get(row.sourceIndex).push({row, owner, option});
      }

      for (const event of events || []) {
        if (event.kind === 'proper') {
          unitOrder.push(event.sourceIndex);
          appearance(event, event, null);
          const disposition = Seating.dispositionOf(event.proper);
          if (disposition && disposition.kind === 'alternative') {
            failure(...context,
              'alternative source row escaped its atomic choice at ' + event.sourceIndex);
          } else if (disposition && disposition.kind === 'unplaced') {
            stats.unplacedOccurrences += 1;
            if (!event.seat || event.seat.key !== 'unplaced/' + disposition.group ||
                event.seat.placement !== 'unseated' ||
                event.seat.region !== disposition.region ||
                event.seat.basis !== disposition.basis ||
                event.seat.formId !== form.id ||
                event.placement !== 'unseated') {
              failure(...context,
                'unplaced source row lacks its exact synthetic seat at ' + event.sourceIndex);
            }
          } else {
            stats.plainOccurrences += 1;
            if (application === 'full') {
              if (!event.seat || String(event.seat.key || '').startsWith('unplaced/') ||
                  event.placement !== 'seated') {
                failure(...context,
                  'plain full-frame row has no usable semantic seat at ' + event.sourceIndex);
              }
            } else if (event.seat !== null || event.placement !== null) {
              failure(...context,
                'plain non-full row borrowed an Ordinary seat at ' + event.sourceIndex);
            }
          }
          continue;
        }
        if (event.kind !== 'proper_choice') continue;
        unitOrder.push(event.sourceIndex);

        stats.choiceEvents += 1;
        if (event.formId !== form.id) {
          failure(...context, 'alternative choice lost its form identity: ' + event.group);
        }
        if (choiceGroups.has(event.group)) {
          failure(...context, 'alternative group emitted more than one choice: ' + event.group);
        }
        choiceGroups.set(event.group, event);
        if (hasSelectionMarker(event)) {
          failure(...context, 'alternative choice carries an incidental selection: ' + event.group);
        }
        const ids = (event.options || []).map((option) => option.id);
        if (new Set(ids).size < 2 || new Set(ids).size !== ids.length) {
          failure(...context, 'alternative choice lacks distinct options: ' + event.group);
        }
        const members = (event.options || []).flatMap((option) => option.rows || []);
        const firstDisposition = members.length && Seating.dispositionOf(members[0].proper);
        const anchor = firstDisposition && firstDisposition.anchor;
        const anchored = anchor && selected.find((row) =>
          row.proper.appointment_identity && ['mass', 'form_id', 'proper', 'occurrence']
            .every((key) => row.proper.appointment_identity[key] === anchor[key]));
        const expectedAnchor = anchor ? anchored && anchored.sourceIndex
          : Math.min(...members.map((row) => row.sourceIndex));
        if (event.sourceIndex !== expectedAnchor) {
          failure(...context, 'alternative choice moved from its exact source anchor');
        }
        if (application === 'full') {
          if (!event.seat || String(event.seat.key || '').startsWith('unplaced/') ||
              event.placement !== 'seated') {
            failure(...context, 'full-frame choice has no shared semantic seat: ' + event.group);
          }
        } else if (event.seat !== null || event.placement !== null) {
          failure(...context, 'non-full choice borrowed an Ordinary seat: ' + event.group);
        }
        for (const option of event.options || []) {
          if (hasSelectionMarker(option)) {
            failure(...context,
              'alternative option carries an incidental selection: ' + event.group);
          }
          for (const row of option.rows || []) {
            stats.alternativeOccurrences += 1;
            appearance(row, event, option);
            const disposition = Seating.dispositionOf(row.proper);
            if (!disposition || disposition.kind !== 'alternative' ||
                disposition.group !== event.group || disposition.option !== option.id ||
                disposition.basis !== event.basis) {
              failure(...context,
                'choice member disagrees with its source annotation at ' + row.sourceIndex);
            }
          }
          const offsets = option.rows.map((row) => row.sourceIndex);
          if (offsets.some((offset, index) => index && offset <= offsets[index - 1])) {
            failure(...context, 'source option bundle changed its internal order');
          }
        }
      }

      for (const source of selected) {
        const found = appearances.get(source.sourceIndex) || [];
        if (found.length !== 1) {
          failure(...context,
            'source occurrence ' + source.sourceIndex + ' appeared ' + found.length + ' times');
          continue;
        }
        if (found[0].row.proper !== source.proper) {
          failure(...context,
            'source occurrence ' + source.sourceIndex + ' was replaced by another row');
        }
        const disposition = Seating.dispositionOf(source.proper);
        if (disposition && disposition.kind === 'alternative' &&
            found[0].owner.kind !== 'proper_choice') {
          failure(...context,
            'alternative occurrence is cumulative, not a choice member: ' + source.sourceIndex);
        }
        if ((!disposition || disposition.kind === 'unplaced') &&
            found[0].owner.kind !== 'proper') {
          failure(...context,
            'plain or unplaced occurrence changed event kind: ' + source.sourceIndex);
        }
      }
      if (unitOrder.some((offset, index) => index && offset <= unitOrder[index - 1])) {
        failure(...context, 'Proper units do not retain their source anchor order');
      }
    }
  }
}

process.stdout.write(JSON.stringify(report));
"""


def node_call(payload: dict) -> dict:
    run = subprocess.run(
        ["node", "-e", NODE], input=json.dumps(payload), text=True,
        capture_output=True, cwd=ROOT, check=False,
    )
    if run.returncode:
        raise AssertionError(run.stdout + run.stderr)
    return json.loads(run.stdout)


def production_seating_report() -> dict:
    run = subprocess.run(
        ["node", "-e", PRODUCTION_SEATING_NODE], text=True,
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

    def test_conditional_source_candidates_cross_the_reader_appointment_owner(self) -> None:
        result = node_call({"op": "appointment-boundary"})
        self.assertEqual(
            result["rawError"],
            "conditional Proper applicability must be prepared before seating",
        )
        self.assertTrue(result["sourceUnchanged"])
        self.assertTrue(result["conditionalChoice"])
        self.assertGreater(len(result["prepared"]["proper"]), 0)
        self.assertGreater(len(result["prepared"]["ordinary"]), 0)
        self.assertNotIn("Gradual", {
            row["label"] for row in result["prepared"]["proper"]
        })

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

    def test_explicit_form_never_borrows_ambient_formulary_identity(self) -> None:
        cases = (
            (
                "day",
                "#date=2026-12-25&missal=synthetic-edition&bible=synthetic-bible&form=night",
                "form-requires-explicit-mass",
            ),
            (
                "propers",
                "#missal=synthetic-edition&type=synthetic-contract&bible=synthetic-bible&form=night",
                "form-requires-explicit-formulary",
            ),
            (
                "propers",
                "#missal=synthetic-edition&mass=synthetic-christmas&bible=synthetic-bible&form=night",
                "form-requires-explicit-formulary",
            ),
        )
        for entrance, hash_value, error_code in cases:
            with self.subTest(entrance=entrance, hash=hash_value):
                result = node_call({
                    "op": "url",
                    "entrance": entrance,
                    "mass": "synthetic-christmas",
                    "defaultMass": "synthetic-christmas",
                    "hash": hash_value,
                })
                self.assertFalse(result["normalized"]["ok"])
                self.assertIn(
                    error_code,
                    {error["code"] for error in result["normalized"]["errors"]},
                )

    def test_every_production_form_has_one_typed_source_honest_event_path(self) -> None:
        report = production_seating_report()
        self.assertEqual(
            report["failures"], [],
            json.dumps(report["failures"][:30], indent=2),
        )
        selected_calendars = os.environ.get(
            "TRIPTYCH_SEATING_CALENDARS",
            "roman-1962,roman-pre-1955,postconciliar",
        )
        self.assertEqual(
            set(report["calendars"]),
            {calendar for calendar in selected_calendars.split(",") if calendar},
        )
        for calendar, stats in report["calendars"].items():
            with self.subTest(calendar=calendar):
                self.assertGreater(stats["full"], 0)
                self.assertGreater(stats["nonfull"], 0)
                self.assertGreater(stats["candidateChoiceGroups"], 0)
                self.assertEqual(
                    stats["sourceOccurrences"],
                    stats["plainOccurrences"] +
                    stats["alternativeOccurrences"] +
                    stats["unplacedOccurrences"],
                )
                self.assertEqual(
                    stats["candidates"],
                    stats["sourceOccurrences"] + stats["unresolvedConditions"] +
                    stats["inactiveConditions"] + stats["unadmittedPathCandidates"] +
                    stats["unsupportedCandidates"],
                )
                self.assertEqual(
                    stats["forms"],
                    stats["full"] + stats["nonfull"] + stats["unsupportedForms"],
                )
        self.assertGreater(
            sum(stats["alternativeOccurrences"] for stats in report["calendars"].values()),
            0,
        )
        self.assertGreater(
            sum(stats["unplacedOccurrences"] for stats in report["calendars"].values()),
            0,
        )


if __name__ == "__main__":
    unittest.main()
