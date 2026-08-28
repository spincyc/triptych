#!/usr/bin/env python3
"""Shared liturgy reader-state, URL, fixture, and consumer parity gates."""

from __future__ import annotations

import copy
import hashlib
import importlib.machinery
import importlib.util
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
BROWSER_CORE = ROOT / "src/web/browser/shared/browser-core.js"


def load_tool_module(name: str, path: Path):
    loader = importlib.machinery.SourceFileLoader(name, str(path))
    spec = importlib.util.spec_from_loader(name, loader)
    if spec is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    loader.exec_module(module)
    return module


MASS_TODAY_MODULE = load_tool_module("reader_state_mass_today", MASS_TODAY)
MASS_PROPERS_MODULE = load_tool_module(
    "reader_state_mass_propers", ROOT / "tools/mass-propers"
)


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
    weekdayCycles: selected.weekdayCycles || [],
    cycleDimension: selected.cycleDimension || null,
    references: selected.references || [],
    bible: selected.bible || null,
    numbering: selected.numbering || null,
    sourceId: selected.sourceId || null,
    rights: Object.prototype.hasOwnProperty.call(selected, 'rights') ? selected.rights : null,
    missing: Boolean(selected.missing),
    availability: selected.availability || null,
    reason: selected.reason || null,
    unavailableState: selected.unavailableState || null,
    extent: selected.extent || null,
    held: selected.held === true,
    absenceKey: selected.absenceKey || null,
    relation: selected.relation || null,
    collation: selected.collation || null,
    unresolvedWitnesses: selected.unresolvedWitnesses || [],
    text: Object.prototype.hasOwnProperty.call(selected, 'text') ? selected.text : null,
    alternatives: (selected.alternatives || []).map((alternative) => ({
      id: alternative.id,
      cycle: alternative.cycle,
      cycleDimension: alternative.cycleDimension || null,
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
    unresolvedChoices: result.unresolvedChoices || [],
    ordinaryUnresolved: result.ordinaryUnresolved || []
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
    languages: {orations: input.translationOnly ? 'en' : 'la'}, requestedMode: 'read',
    options: {ordinary: false, legitimate: {}}, coverage: [],
    unresolvedChoices: [], sourceHooks: []
  };
  if (Object.prototype.hasOwnProperty.call(input, 'cycle')) request.cycle = input.cycle;
  const order = input.reverseCycles ? ['C', 'B', 'A'] : ['A', 'B', 'C'];
  const cycles = {};
  for (const cycle of order) {
    cycles[cycle] = input.translationOnly
      ? {citations: [], translations: [{lang: 'en', source_id: 'witness-cycle-' + cycle,
          rights: 'public-domain', text: 'translated-cycle-' + cycle}]}
      : {citations: [], text: 'contract-material-' + cycle};
  }
  output = resultProjection(A.adaptPropers({
    request,
    structure: {
      calendar: 'synthetic-cycle-edition', translations: [],
      masses: [{
        key: 'synthetic-cycle-formulary', kind: 'contract',
        propers: [{
          name: 'Collect', form_id: 'main', source: 'composed',
          text: null, citations: [], cycles
        }]
      }]
    }
  }));
} else if (input.op === 'synthetic-day-cycle') {
  const request = {
    schema: C.STATE_SCHEMA, entrance: 'day', civilDate: '2026-08-26',
    edition: {id: 'synthetic-cycle-edition'}, calendar: {id: 'synthetic-cycle-edition'},
    selectedReadableFormulary: {id: 'synthetic-cycle-formulary'},
    bible: {id: 'douay-rheims', numbering: 'vulgate'},
    languages: {orations: 'la'}, requestedMode: 'read',
    options: {ordinary: false, legitimate: {}}, coverage: [],
    unresolvedChoices: [], sourceHooks: []
  };
  const sunday = input.reverse ? ['C', 'B', 'A'] : ['A', 'B', 'C'];
  const weekday = input.reverse ? ['II', 'I'] : ['I', 'II'];
  const cycleRows = Object.fromEntries(sunday.map((key) => [key, {
    citations: [{ref: 'Sunday ' + key, unresolved: null}], text: null
  }]));
  const weekdayRows = Object.fromEntries(weekday.map((key) => [key, {
    citations: [{ref: 'Weekday ' + key, unresolved: null}], text: null
  }]));
  const proper = {
    name: 'First Reading', form_id: 'main', source: 'scripture', citations: []
  };
  if (input.family === 'sunday' || input.family === 'both') proper.cycles = cycleRows;
  if (input.family === 'weekday' || input.family === 'both') proper.weekday_cycles = weekdayRows;
  output = resultProjection(A.adaptDay({
    request,
    derived: {
      date: request.civilDate, calendar: request.calendar.id,
      liturgicalYear: {lectionary: input.lectionary || {sunday: 'B', weekday: 'II'}},
      options: [{
        option: null, winner: {id: 'synthetic-day'}, settled: true,
        readable: [{key: 'synthetic-cycle-formulary', state: 'said'}]
      }]
    },
    structure: {
      calendar: request.edition.id, translations: [],
      masses: [{key: 'synthetic-cycle-formulary', kind: 'contract', propers: [proper]}]
    }
  }));
} else if (input.op === 'synthetic-cycle-untranslated') {
  const request = {
    schema: C.STATE_SCHEMA, entrance: 'day', civilDate: '2026-08-30',
    edition: {id: 'synthetic-cycle-edition'}, calendar: {id: 'synthetic-cycle-edition'},
    selectedReadableFormulary: {id: 'synthetic-cycle-formulary'},
    bible: {id: 'douay-rheims', numbering: 'vulgate'},
    languages: {orations: 'en'}, requestedMode: 'read',
    options: {ordinary: false, legitimate: {}}, coverage: [],
    unresolvedChoices: [], sourceHooks: []
  };
  const absence = (cycle, state) => ({
    target: {mass: 'synthetic-cycle-formulary', form_id: 'main', proper: 'Collect',
      cycle, occurrence: 1, extent: 'body'},
    lang: 'en', state
  });
  const proper = {
    name: 'Collect', form_id: 'main', source: 'composed', citations: [],
    cycles: {
      A: {citations: [], unavailable_translations: [absence('A', 'rights-restricted')]},
      C: {citations: [], untranslated: [absence('C', 'unavailable')]}
    }
  };
  if (input.variant === 'cycle-owned-translation') {
    proper.text = 'Parent Latin body';
    proper.translations = [{
      lang: 'en', source_id: 'edition.synthetic.parent',
      rights: 'public-domain', text: 'Parent English must not win.'
    }];
    proper.cycles.A = {
      citations: [], text: 'Cycle A Latin body', translations: [{
        lang: 'en', source_id: 'edition.synthetic.cycle-a',
        rights: 'public-domain', text: 'Cycle A held English.'
      }]
    };
  } else if (input.variant === 'cycle-owned-restriction') {
    proper.text = 'Parent Latin body';
    proper.translations = [{
      lang: 'en', source_id: 'edition.synthetic.parent-protected',
      rights: 'public-domain', text: 'Parent English must not escape.'
    }];
    proper.cycles.A = {
      citations: [], text: 'Cycle A Latin body',
      unavailable_translations: [absence('A', 'rights-restricted')]
    };
  }
  output = resultProjection(A.adaptDay({
    request,
    derived: {
      date: request.civilDate, calendar: request.calendar.id,
      liturgicalYear: {lectionary: {sunday: input.cycle, weekday: 'II'}},
      options: [{option: null, winner: {id: 'synthetic-day'}, settled: true,
        readable: [{key: 'synthetic-cycle-formulary', state: 'said'}]}]
    },
    structure: {calendar: request.edition.id, translations: [], masses: [{
      key: 'synthetic-cycle-formulary', kind: 'contract', propers: [proper]
    }]}
  }));
} else if (input.op === 'synthetic-cli-language') {
  const withheldLatin = input.kind === 'withheld-latin';
  const language = withheldLatin ? 'la' : 'en';
  const request = {
    schema: C.STATE_SCHEMA, entrance: 'day', civilDate: '2026-08-30',
    edition: {id: 'synthetic-language-edition'}, calendar: {id: 'synthetic-language-edition'},
    selectedReadableFormulary: {id: 'synthetic-language-formulary'},
    bible: {id: 'douay-rheims', numbering: 'vulgate'},
    languages: {orations: language}, requestedMode: 'read',
    options: {ordinary: false, legitimate: {}}, coverage: [],
    unresolvedChoices: [], sourceHooks: []
  };
  const translations = withheldLatin ? [] : [{
    lang: 'en', source_id: 'edition.synthetic.safe-english',
    rights: 'public-domain', text: 'Held English text.'
  }];
  const generatedProper = {
    name: 'Collect', form_id: 'main', source: 'composed', citations: [], cycles: {},
    text: withheldLatin ? null : 'Retained Latin text.', translations,
    latin: withheldLatin ? {
      withheld: true, held: false, available: false, state: 'unavailable',
      target: 'Collect'
    } : null
  };
  const payloadProper = {
    name: 'Collect', form: null, form_id: 'main', source: 'composed',
    text: withheldLatin ? null : 'Retained Latin text.', translations,
    taken_from: null, verses: []
  };
  if (withheldLatin) {
    payloadProper.latin = {
      target: 'Collect', state: 'unavailable', withheld: true,
      held: false, available: false
    };
    payloadProper.language_selection = {
      requested: 'la', status: 'unavailable', held: false,
      available: false, complete: false,
      reason: {state: 'text-withheld', lang: 'la'}
    };
  } else {
    payloadProper.language_selection = {
      requested: 'en', status: 'full-text', held: true,
      available: true, complete: true, texts: translations
    };
  }
  const derived = {
    date: request.civilDate, calendar: request.calendar.id,
    liturgicalYear: {lectionary: {sunday: 'A', weekday: 'II'}},
    options: [{option: null, winner: {id: 'synthetic-day'}, settled: true,
      readable: [{key: 'synthetic-language-formulary', state: 'said'}], absent: []}]
  };
  const structure = {calendar: request.edition.id, translations: [], masses: [{
    key: 'synthetic-language-formulary', kind: 'contract',
    ordinary_frame: {applicability: 'full', basis: 'synthetic full-frame basis'},
    propers: [generatedProper]
  }]};
  const payload = {
    date: request.civilDate, scripture: {id: request.bible.id},
    days: [{
      calendar: request.calendar.id, selected_territory: null,
      territory_choice_required: false, settled: true,
      why: {lectionary: {sunday: 'A', weekday: 'II'}},
      masses: [{
        key: 'synthetic-language-formulary', standing: 'said',
        bible: {id: request.bible.id}, selected_form: 'main',
        form_choice_required: false,
        ordinary_frame: {applicability: 'full', basis: 'synthetic full-frame basis'},
        propers: [payloadProper]
      }]
    }]
  };
  const day = A.adaptDay({request, derived, structure});
  const cli = A.adaptCli({request, payload, derived, structure});
  output = {day: resultProjection(day), cli: resultProjection(cli)};
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
  if (input.translationWitness) {
    request.languages.translationWitness = input.translationWitness;
  }
  const translations = input.rightsRestricted ? [] :
    (input.translationOrder || ['witness-a', 'witness-b']).map((id) => ({
      lang: 'en', source_id: id, rights: 'public-domain', text: 'contract-only'
    }));
  const unavailableTranslations = input.rightsRestricted ? [{
    lang: 'en', state: 'rights-restricted',
    target: {
      mass: 'synthetic-test-formulary', form_id: 'main', proper: 'Collect',
      cycle: 'all', occurrence: 1, extent: 'body'
    },
    source_id: 'protected-witness-must-not-escape',
    text: 'protected exact wording must not escape'
  }] : [];
  const structure = {
    calendar: 'synthetic-test-edition', translations: [],
    masses: [{
      key: 'synthetic-test-formulary', kind: 'contract', propers: [
        {name: 'Placeholder', form_id: 'main', source: 'composed', text: 'not held', citations: [], cycles: {}},
        {name: 'Introit', form_id: 'main', source: 'scripture', citations: [{ref: 'Synthetic ref', unresolved: null}], cycles: {}},
        {
          name: 'Collect', form_id: 'main', source: 'composed',
          text: input.latinWithheld ? null : 'synthetic latin',
          citations: [], cycles: {}, translations,
          latin: input.latinWithheld ? Object.assign({
            withheld: true, held: false, available: false, state: 'unavailable',
            target: 'Collect'
          }, input.malformedLatin || {}) : null,
          unavailable_translations: unavailableTranslations
        }
      ]
    }]
  };
  output = resultProjection(A.adaptPropers({request, structure}));
} else if (input.op === 'synthetic-ordinary-frame') {
  const request = {
    schema: C.STATE_SCHEMA, entrance: 'day', civilDate: '2027-03-26',
    edition: {id: 'synthetic-frame-edition'}, calendar: {id: 'synthetic-frame-edition'},
    selectedReadableFormulary: {id: 'exceptional-rite'},
    languages: {orations: 'la', ordinary: 'la'}, requestedMode: 'study',
    options: {ordinary: true, legitimate: {}}, coverage: [],
    unresolvedChoices: [], sourceHooks: []
  };
  const frame = Object.prototype.hasOwnProperty.call(input, 'frame') ? input.frame : {
    applicability: input.applicability, basis: 'source-owned frame basis'
  };
  const proper = input.properName ? {
    name: input.properName, form_id: 'main', source: 'composed',
    text: 'synthetic proper body', citations: [], cycles: {}
  } : {
    name: 'Placeholder', form_id: 'main', source: 'composed',
    text: 'repository status, not liturgy', citations: [], cycles: {}
  };
  const mass = {
    key: 'exceptional-rite', kind: 'contract',
    propers: [proper]
  };
  if (!input.omitFrame) mass.ordinary_frame = frame;
  const adaptFrame = () => resultProjection(A.adaptDay({
    request,
    derived: {
      date: request.civilDate, calendar: request.calendar.id,
      options: [{
        option: null, winner: {id: 'exceptional-rite'}, settled: true,
        readable: [{key: 'exceptional-rite', state: 'said'}]
      }]
    },
    structure: {
      calendar: request.edition.id, translations: [],
      masses: [mass]
    },
    ordinary: {
      calendar: request.edition.id, languages: [], sections: [], slots: [], variants: []
    }
  }));
  if (input.captureError) {
    try { output = adaptFrame(); }
    catch (error) { output = {error: String(error && error.message || error)}; }
  } else output = adaptFrame();
} else if (input.op === 'cross-recension') {
  const request = {
    schema: C.STATE_SCHEMA, entrance: 'day', civilDate: '2027-03-26',
    edition: {id: 'requested-edition'}, calendar: {id: 'requested-edition'},
    selectedReadableFormulary: {id: 'synthetic-mass'},
    bible: {id: 'douay-rheims', numbering: 'vulgate'},
    languages: {orations: 'la', ordinary: 'en'}, requestedMode: 'study',
    options: {ordinary: true, legitimate: {}}, coverage: [],
    unresolvedChoices: [], sourceHooks: []
  };
  const derived = {
    date: request.civilDate, calendar: request.calendar.id,
    options: [{option: null, winner: {id: 'synthetic-mass'}, settled: true,
      readable: [{key: 'synthetic-mass', state: 'said'}]}]
  };
  const structure = {
    calendar: 'requested-edition', translations: [],
    masses: [{key: 'synthetic-mass', kind: 'contract', propers: []}]
  };
  const payload = {
    date: request.civilDate, scripture: {id: request.bible.id},
    days: [{calendar: request.calendar.id, ordinary: {calendar: 'foreign-edition'},
      masses: []}]
  };
  const message = (call) => {
    try { call(); return null; }
    catch (error) { return String(error && error.message || error); }
  };
  output = {
    dayStructure: message(() => A.adaptDay({
      request, derived, structure: Object.assign({}, structure, {calendar: 'foreign-edition'})
    })),
    dayOrdinary: message(() => A.adaptDay({
      request, derived, structure, ordinary: {calendar: 'foreign-edition'}
    })),
    cliStructure: message(() => A.adaptCli({
      request, derived, payload,
      structure: Object.assign({}, structure, {calendar: 'foreign-edition'})
    })),
    cliOrdinary: message(() => A.adaptCli({request, derived, payload, structure}))
  };
} else if (input.op === 'synthetic-ordinary-condition') {
  const request = {
    schema: C.STATE_SCHEMA, entrance: 'day', civilDate: '2027-03-26',
    edition: {id: 'synthetic-condition'}, calendar: {id: 'synthetic-condition'},
    selectedReadableFormulary: {id: 'synthetic-mass'},
    bible: {id: 'douay-rheims', numbering: 'vulgate'},
    languages: {orations: 'la', ordinary: 'en'}, requestedMode: 'study',
    options: {ordinary: true, legitimate: {}}, coverage: [],
    unresolvedChoices: [], sourceHooks: []
  };
  const ordinary = {
    calendar: 'synthetic-condition',
    languages: [{lang: 'en', absent: 'english', elements: 1, held: 1}],
    language_coverage: [{lang: 'en', elements: 1, held: 1, missing: 0, absent: 0}],
    relation_coverage: [{lang: 'en', relation: 'own', collation: 'not-applicable', count: 1}],
    language_absences: [], absences: [], exclusions: [], variants: [], slots: [],
    translations: [{lang: 'en', source_id: 'edition.synthetic.ordinary'}],
    sections: [{key: 'conditional', elements: [{
      key: 'conditional/element', kind: 'prayer', speaker: 'priest',
      absent: {english: null},
      conditions: [{kind: 'include-when-any', predicates: ['source-fact'], basis: 'source basis'}],
      translations: [{lang: 'en', source_id: 'edition.synthetic.ordinary',
        rights: 'public-domain', relation: 'own', collation: 'not-applicable', text: 'Held.'}]
    }]}]
  };
  output = resultProjection(A.adaptDay({
    request,
    derived: {date: request.civilDate, calendar: request.calendar.id,
      options: [{option: null, winner: {id: 'synthetic-mass'}, settled: true,
        readable: [{key: 'synthetic-mass', state: 'said'}]}]},
    structure: {calendar: request.edition.id, translations: [],
      masses: [{key: 'synthetic-mass', kind: 'contract', propers: []}]},
    ordinary
  }));
} else if (input.op === 'synthetic-ordinary-variants') {
  const request = {
    schema: C.STATE_SCHEMA, entrance: 'day', civilDate: '2027-03-26',
    edition: {id: 'synthetic-variants'}, calendar: {id: 'synthetic-variants'},
    selectedReadableFormulary: {id: 'synthetic-mass'},
    bible: {id: 'douay-rheims', numbering: 'vulgate'},
    languages: {orations: 'la', ordinary: 'en'}, requestedMode: 'study',
    options: {ordinary: true, legitimate: {first: 'b', second: 'y'}},
    coverage: [], unresolvedChoices: [], sourceHooks: []
  };
  const combinations = [['a', 'x'], ['a', 'y'], ['b', 'x'], ['b', 'y']];
  const elements = combinations.map(([first, second]) => ({
    key: 'variants/' + first + second, kind: 'prayer', speaker: 'priest',
    absent: {english: null}, conditions: [],
    alternatives: [{group: 'first', option: first}, {group: 'second', option: second}],
    translations: [{lang: 'en', source_id: 'edition.synthetic.ordinary',
      rights: 'public-domain', relation: 'own', collation: 'not-applicable',
      text: first + second}]
  }));
  const ordinary = {
    calendar: request.edition.id,
    languages: [{lang: 'en', absent: 'english', elements: 4, held: 4}],
    language_coverage: [{lang: 'en', elements: 4, held: 4, missing: 0, absent: 0}],
    relation_coverage: [{lang: 'en', relation: 'own', collation: 'not-applicable', count: 4}],
    language_absences: [], absences: [], exclusions: [], slots: [],
    translations: [{lang: 'en', source_id: 'edition.synthetic.ordinary'}],
    variants: [
      {group: 'first', mode: 'one-of', options: [{id: 'a', default: true}, {id: 'b'}]},
      {group: 'second', mode: 'one-of', options: [{id: 'x', default: true}, {id: 'y'}]}
    ],
    sections: [{key: 'variants', elements}]
  };
  output = resultProjection(A.adaptDay({
    request,
    derived: {date: request.civilDate, calendar: request.calendar.id,
      options: [{option: null, winner: {id: 'synthetic-mass'}, settled: true,
        readable: [{key: 'synthetic-mass', state: 'said'}]}]},
    structure: {calendar: request.edition.id, translations: [],
      masses: [{key: 'synthetic-mass', kind: 'contract', propers: []}]},
    ordinary
  }));
} else if (input.op === 'browser-oration') {
  global.window = {location: {search: ''}};
  require('./src/web/browser/shared/browser-core.js');
  output = global.window.Triptych.orationFor(input.proper, input.language, input.witness || null);
} else if (input.op === 'browser-cycles') {
  global.window = {location: {search: ''}};
  require('./src/web/browser/shared/browser-core.js');
  const T = global.window.Triptych;
  output = {
    all: T.cycleKeysOf(input.proper),
    sunday: T.sundayCycleKeysOf(input.proper),
    weekday: T.weekdayCycleKeysOf(input.proper),
    selected: T.cycleOf(input.proper, input.cycle),
    citations: T.citationsOf({propers: [input.proper]}).map((row) => row.ref)
  };
} else if (input.op === 'url-foundation') {
  output = {
    bible: C.defaultBibleId(input.bibles, input.preferred || null),
    dayRoute: C.canonicalRoute('day', input.dayPath),
    propersRoute: C.canonicalRoute('propers', input.propersPath)
  };
} else if (input.op === 'ordinary-coverage') {
  const request = input.request;
  const id = request.edition.id;
  output = resultProjection(A.adaptDay({
    request, derived: derive(id, request.civilDate),
    structure: read(base + 'propers/' + id + '.json'),
    ordinary: read(base + 'ordinary/' + id + '.json')
  }));
} else if (input.op === 'source-ordinary-frame') {
  const request = {
    schema: C.STATE_SCHEMA, entrance: 'day', civilDate: input.date,
    edition: {id: input.id}, calendar: {id: input.id},
    selectedReadableFormulary: {id: input.mass},
    bible: {id: 'douay-rheims', numbering: 'vulgate'},
    languages: {orations: 'la', ordinary: 'en'}, requestedMode: 'study',
    options: {ordinary: true, legitimate: {}}, coverage: [],
    unresolvedChoices: [], sourceHooks: []
  };
  if (input.form) request.form = input.form;
  output = resultProjection(A.adaptDay({
    request, derived: derive(input.id, input.date),
    structure: read(base + 'propers/' + input.id + '.json'),
    ordinary: read(base + 'ordinary/' + input.id + '.json')
  }));
} else if (input.op === 'source-claim-coverage') {
  const structure = read(base + 'propers/' + input.id + '.json');
  const mass = structure.masses.find((one) => one.key === input.mass);
  if (input.malformed === 'mass-status') mass.text_status.extra = true;
  if (input.malformed === 'proper-status') {
    mass.propers.find((proper) => proper.text_status).text_status.scope = 'whole-proper';
  }
  if (input.malformed === 'common-set') {
    mass.takes_from.common_sets.orations.candidates = ['c3'];
  }
  const request = {
    schema: C.STATE_SCHEMA, entrance: 'propers', civilDate: null,
    edition: {id: input.id},
    formulary: {id: input.mass, type: mass.kind},
    bible: {id: 'douay-rheims', numbering: 'vulgate'},
    languages: {orations: input.language || 'la'}, requestedMode: 'read',
    options: {ordinary: false, legitimate: {}}, coverage: [],
    unresolvedChoices: [], sourceHooks: []
  };
  output = resultProjection(A.adaptPropers({request, structure}));
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
        state = copy.deepcopy(day)
        state["form"] = "night"
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
        state = copy.deepcopy(propers)
        state["form"] = "night"
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
             "ordinary-lang", "rubrics", "mass", "form", "translation-witness",
             "mode", "location", "eucharistic-prayer"],
        )
        self.assertEqual(
            propers["hash"],
            ["missal", "type", "mass", "bible", "orations", "form", "cycle",
             "alternative", "translation-witness", "mode", "location"],
        )
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

        unavailable = fixture_named("propers-roman-1962-advent-1")
        unavailable_mutations = []
        for mutation in (
            {"held": True},
            {"missing": False},
            {"text": "protected text must not escape"},
            {"sourceId": "private-source"},
            {"source": "private-source"},
        ):
            fixture = copy.deepcopy(unavailable)
            fixture["expected"]["events"][1]["selected"].update(mutation)
            unavailable_mutations.append(fixture)
        fixture = copy.deepcopy(unavailable)
        fixture["expected"]["events"][1]["selected"].pop("reason")
        unavailable_mutations.append(fixture)
        results = node_call({
            "op": "fixture-validate", "fixtures": unavailable_mutations,
        })
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
            "op": "context", "entrance": "day", "id": "roman-1962",
            "date": "2026-08-02", "includeOrdinary": True,
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

    def test_mode_location_routes_and_bible_default_are_canonical_and_order_free(self) -> None:
        rows = [{"id": "world-english-bible-catholic"}, {"id": "douay-rheims"}]
        forward = node_call({
            "op": "url-foundation", "bibles": rows,
            "dayPath": "/prefix/liturgy/day-reader.html",
            "propersPath": "/prefix/liturgy/propers-reader.html",
        })
        reverse = node_call({
            "op": "url-foundation", "bibles": list(reversed(rows)),
            "dayPath": "/prefix/liturgy/day-reader.html",
            "propersPath": "/prefix/liturgy/propers-reader.html",
        })
        self.assertEqual(forward, reverse)
        self.assertEqual(forward["bible"], "douay-rheims")
        self.assertEqual(forward["dayRoute"], "/prefix/liturgy/day.html")
        self.assertEqual(forward["propersRoute"], "/prefix/liturgy/index.html")

        fallback = node_call({
            "op": "url-foundation", "bibles": [{"id": "z"}, {"id": "a"}],
            "dayPath": "/unrelated", "propersPath": "/unrelated",
        })
        self.assertEqual(fallback["bible"], "a")
        self.assertEqual(fallback["dayRoute"], "/unrelated")
        self.assertEqual(fallback["propersRoute"], "/unrelated")

    def test_mode_and_semantic_location_round_trip_and_legacy_ordinary_canonicalizes(self) -> None:
        legacy = node_call({
            "op": "url", "entrance": "day",
            "hash": (
                "#date=2026-08-02&missal=roman-1962&bible=douay-rheims&"
                "orations=la&ordinary=1&location=proper%2Froman-1962%2Fadvent-1%2F001"
            ),
            "context": self.day_context,
            "defaults": {"date": "2026-08-02", "missal": "roman-1962",
                         "bible": "douay-rheims", "orations": "la",
                         "why": "0", "ordinary": "0", "ordinary-lang": "en",
                         "rubrics": "1"},
        })
        self.assertTrue(legacy["normalized"]["ok"], legacy["normalized"]["errors"])
        state = legacy["normalized"]["state"]
        self.assertEqual(state["requestedMode"], "missal")
        self.assertTrue(state["options"]["ordinary"])
        self.assertEqual(
            state["semanticLocation"],
            {"eventId": "proper/roman-1962/advent-1/001"},
        )
        self.assertIn("mode=missal", legacy["serialized"])
        self.assertIn("ordinary-lang=en", legacy["serialized"])
        self.assertIn("location=proper%2Froman-1962%2Fadvent-1%2F001", legacy["serialized"])
        self.assertNotIn("ordinary=", legacy["serialized"])
        self.assertEqual(legacy["renormalized"]["state"], state)

        propers = node_call({
            "op": "url", "entrance": "propers",
            "hash": (
                "#missal=roman-1962&type=seasonal&mass=advent-1&"
                "bible=douay-rheims&orations=la&mode=read&"
                "location=proper%2Froman-1962%2Fadvent-1%2F003"
            ),
            "context": self.propers_context,
            "defaults": {"missal": "roman-1962", "type": "seasonal",
                         "mass": "advent-1", "bible": "douay-rheims", "orations": "la"},
        })
        self.assertTrue(propers["normalized"]["ok"], propers["normalized"]["errors"])
        self.assertEqual(propers["normalized"]["state"]["requestedMode"], "read")
        self.assertEqual(
            propers["normalized"]["state"]["semanticLocation"]["eventId"],
            "proper/roman-1962/advent-1/003",
        )
        self.assertEqual(propers["reserialized"], propers["serialized"])

        conflict = node_call({
            "op": "url", "entrance": "day",
            "hash": (
                "#date=2026-08-02&missal=roman-1962&bible=douay-rheims&"
                "orations=la&mode=read&ordinary=1"
            ),
            "context": self.day_context,
            "defaults": {"date": "2026-08-02", "missal": "roman-1962",
                         "bible": "douay-rheims", "orations": "la"},
        })
        self.assertFalse(conflict["normalized"]["ok"])
        self.assertIn(
            "conflicting-explicit-mode",
            [one["code"] for one in conflict["normalized"]["errors"]],
        )

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
            "translation-witness=witness-english&eucharistic-prayer=ep-ii"
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
        self.assertEqual(state["languages"], {
            "orations": "en", "ordinary": "en",
            "translationWitness": "witness-english",
        })
        self.assertEqual(state["apparatus"], {"why": True, "rubrics": False})
        self.assertTrue(state["options"]["ordinary"])
        self.assertEqual(state["options"]["legitimate"]["eucharistic-prayer"], "ep-ii")
        self.assertEqual(state["selectedReadableFormulary"]["id"], "advent-1")
        self.assertEqual(day["serialized"], (
            "#date=2026-11-29&missal=postconciliar&bible=douay-rheims&orations=en&"
            "mode=missal&why=1&ordinary-lang=en&rubrics=0&mass=advent-1&"
            "translation-witness=witness-english&eucharistic-prayer=ep-ii"
        ))
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
        self.assertEqual(propers["serialized"], propers_hash + "&mode=read")
        self.assertEqual(propers["renormalized"]["state"], propers["normalized"]["state"])

    def test_propers_public_choice_keys_round_trip_canonically(self) -> None:
        url = (
            "#missal=roman-1962&type=seasonal&mass=advent-1&"
            "bible=douay-rheims&orations=en&cycle=B&alternative=option-b&"
            "translation-witness=witness-english"
        )
        result = node_call({
            "op": "url", "entrance": "propers", "hash": url,
            "context": self.propers_context,
            "defaults": {"missal": "roman-1962", "type": "seasonal",
                         "mass": "advent-1", "bible": "douay-rheims",
                         "orations": "la"},
        })
        self.assertTrue(result["normalized"]["ok"], result["normalized"]["errors"])
        self.assertEqual(result["parsed"]["unknown"], [])
        self.assertEqual(result["parsed"]["recognized"]["cycle"], "B")
        self.assertEqual(result["parsed"]["recognized"]["alternative"], "option-b")
        self.assertEqual(
            result["parsed"]["recognized"]["translation-witness"],
            "witness-english",
        )
        state = result["normalized"]["state"]
        self.assertEqual(state["cycle"], "B")
        self.assertEqual(state["alternative"], {"id": "option-b"})
        self.assertEqual(state["languages"]["translationWitness"], "witness-english")
        canonical = (
            "#missal=roman-1962&type=seasonal&mass=advent-1&"
            "bible=douay-rheims&orations=en&mode=read&cycle=B&alternative=option-b&"
            "translation-witness=witness-english"
        )
        self.assertEqual(result["serialized"], canonical)
        self.assertEqual(result["reserialized"], canonical)
        self.assertEqual(result["renormalized"]["state"], state)
        self.assertNotIn("_", result["serialized"])
        self.assertNotIn("_candidate", CONTRACT.read_text(encoding="utf-8"))

    def test_propers_public_choice_keys_reject_empty_and_duplicate_values(self) -> None:
        base = (
            "#missal=roman-1962&type=seasonal&mass=advent-1&"
            "bible=douay-rheims&orations=en"
        )
        defaults = {"missal": "roman-1962", "type": "seasonal",
                    "mass": "advent-1", "bible": "douay-rheims",
                    "orations": "la"}
        for key in ("cycle", "alternative", "translation-witness"):
            for suffix in (f"&{key}=", f"&{key}=one&{key}=two"):
                result = node_call({
                    "op": "url", "entrance": "propers", "hash": base + suffix,
                    "context": self.propers_context, "defaults": defaults,
                })
                self.assertFalse(result["normalized"]["ok"], key + suffix)
                codes = [error["code"] for error in result["normalized"]["errors"]]
                expected = "invalid-explicit-value" if suffix.endswith("=") \
                    else "duplicate-explicit-key"
                self.assertIn(expected, codes, key + suffix)

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
        self.assertEqual(result["serialized"], (
            "#date=2026-08-02&missal=roman-1962&bible=douay-rheims&orations=la&"
            "mode=read&why=0&ordinary-lang=en&rubrics=1"
        ))
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

        selected_without_language = node_call({
            "op": "url", "entrance": "day",
            "hash": (
                "#date=2026-08-02&missal=roman-1962&bible=douay-rheims&"
                "ordinary=1"
            ),
            "context": self.day_context,
            "defaults": {
                key: value for key, value in defaults.items()
                if key != "ordinary-lang"
            },
        })
        self.assertFalse(selected_without_language["normalized"]["ok"])
        self.assertIn(
            "required-url-value",
            {error["code"] for error in selected_without_language["normalized"]["errors"]},
        )

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
    def optional_day_request(self, date: str, selected: str | None = None) -> dict:
        request = copy.deepcopy(fixture_named("day-postconciliar-2026-11-29")["requested"])
        request["civilDate"] = date
        request["options"]["ordinary"] = False
        if selected is None:
            request.pop("selectedReadableFormulary", None)
        else:
            request["selectedReadableFormulary"] = {"id": selected}
        return request

    def optional_day_payload(self, date: str) -> dict:
        run = subprocess.run(
            [
                str(MASS_TODAY), "show", "--date", date,
                "--calendar", "postconciliar", "--bible", "douay-rheims",
                "--expanded", "--why", "--format", "json",
            ],
            capture_output=True,
            text=True,
            cwd=ROOT,
            check=False,
        )
        self.assertEqual(run.returncode, 0, run.stdout + run.stderr)
        return json.loads(run.stdout)

    def territory_payload(self, date: str, territory: str | None = None) -> dict:
        command = [
            str(MASS_TODAY), "show", "--date", date,
            "--calendar", "postconciliar", "--bible", "douay-rheims",
            "--expanded", "--why", "--format", "json",
        ]
        if territory is not None:
            command.extend(["--territory", territory])
        run = subprocess.run(
            command, capture_output=True, text=True, cwd=ROOT, check=False,
        )
        self.assertEqual(run.returncode, 0, run.stdout + run.stderr)
        return json.loads(run.stdout)

    def form_payload(self, date: str, form: str) -> dict:
        run = subprocess.run(
            [
                str(MASS_TODAY), "show", "--date", date,
                "--calendar", "roman-1962", "--bible", "douay-rheims",
                "--ordinary", "--expanded", "--why", "--form", form,
                "--format", "json",
            ],
            capture_output=True, text=True, cwd=ROOT, check=False,
        )
        self.assertEqual(run.returncode, 0, run.stdout + run.stderr)
        return json.loads(run.stdout)

    def historical_payload(self, date: str) -> dict:
        run = subprocess.run(
            [
                str(MASS_TODAY), "show", "--date", date,
                "--calendar", "roman-pre-1955", "--bible", "douay-rheims",
                "--ordinary", "--expanded", "--why", "--format", "json",
            ],
            capture_output=True, text=True, cwd=ROOT, check=False,
        )
        self.assertEqual(run.returncode, 0, run.stdout + run.stderr)
        return json.loads(run.stdout)

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

        direct = node_call({
            "op": "browser-oration", "language": "en", "proper": {
                "text": "Latin body",
                "translations": [
                    {"lang": "en", "source_id": "witness-b", "text": "B"},
                    {"lang": "en", "source_id": "witness-a", "text": "A"},
                ],
            },
        })
        self.assertEqual(direct["availability"], "choice-required")
        self.assertEqual(direct["reason"], "translation-choice-required")
        self.assertIsNone(direct["text"])
        self.assertIsNone(direct["source"])

        explicit = node_call({
            "op": "synthetic-propers", "language": "en",
            "translationWitness": "witness-a",
        })
        selected = next(
            one for one in explicit["events"] if one["editionSlotLabel"] == "Collect"
        )["selected"]
        self.assertEqual(selected["availability"], "held")
        self.assertEqual(selected["sourceId"], "witness-a")
        with self.assertRaisesRegex(AssertionError, "translation witness"):
            node_call({
                "op": "synthetic-propers", "language": "en",
                "translationWitness": "not-held",
            })
        with self.assertRaisesRegex(AssertionError, "Latin source language"):
            node_call({
                "op": "synthetic-propers", "language": "la",
                "translationWitness": "witness-a",
            })

    def test_explicit_ordinary_witness_must_be_held_by_selected_elements(self) -> None:
        request = copy.deepcopy(
            fixture_named("day-roman-1962-2026-08-02")["requested"]
        )
        request["requestedMode"] = "study"
        request["options"]["ordinary"] = True
        request["languages"]["ordinary"] = "en"
        ordinary = json.loads(
            (DATA / "structure/ordinary/roman-1962.json").read_text(encoding="utf-8")
        )
        witness = ordinary["translations"][0]["source_id"]
        request["languages"]["ordinaryWitness"] = witness
        result = node_call({"op": "ordinary-coverage", "request": request})
        ordinary_events = [
            event for event in result["events"] if event["kind"] == "ordinary-element"
        ]
        self.assertTrue(ordinary_events)
        self.assertTrue(any(event["selected"]["sourceId"] == witness
                            for event in ordinary_events))

        request["languages"]["ordinaryWitness"] = "not-held"
        with self.assertRaisesRegex(AssertionError, "Ordinary witness"):
            node_call({"op": "ordinary-coverage", "request": request})

    def test_ordinary_antecedent_witness_is_never_reported_complete(self) -> None:
        request = copy.deepcopy(
            fixture_named("day-roman-1962-2026-08-02")["requested"]
        )
        request["requestedMode"] = "study"
        request["options"]["ordinary"] = True
        request["languages"]["ordinary"] = "en"
        result = node_call({"op": "ordinary-coverage", "request": request})
        coverage = next(
            row for row in result["coverage"]
            if row["scope"] == "ordinary:roman-1962:en"
        )
        self.assertEqual(coverage["state"], "supported")
        self.assertEqual(coverage["completeness"], "partial")
        relation = next(
            reason for reason in coverage["reasons"]
            if reason["kind"] == "partial-recension" and
            reason.get("domain") == "ordinary"
        )
        self.assertEqual(relation["relation"], "antecedent")
        self.assertEqual(relation["collation"], "uncollated")
        self.assertTrue(coverage["exclusions"])
        for exclusion in coverage["exclusions"]:
            self.assertEqual(exclusion["state"], "not-in-target-recension")
            self.assertTrue(exclusion["basis"])
            self.assertTrue(exclusion["sources"])
            self.assertTrue(all(isinstance(source, str) and source
                                for source in exclusion["sources"]))
            self.assertTrue(exclusion["evidence"])
            self.assertNotIn('"text"', json.dumps(exclusion["evidence"]))
        event = next(
            event for event in result["events"]
            if event["kind"] == "ordinary-element" and
            event["selected"]["availability"] == "held"
        )
        self.assertEqual(event["selected"]["relation"], "antecedent")
        self.assertEqual(event["selected"]["collation"], "uncollated")

    def test_ordinary_unavailable_language_preserves_typed_absence_states(self) -> None:
        request = copy.deepcopy(
            fixture_named("day-postconciliar-2026-11-29")["requested"]
        )
        request["requestedMode"] = "study"
        request["options"]["ordinary"] = True
        request["languages"]["ordinary"] = "en"
        result = node_call({"op": "ordinary-coverage", "request": request})
        coverage = next(
            row for row in result["coverage"]
            if row["scope"] == "ordinary:postconciliar:en"
        )
        self.assertEqual(coverage["state"], "unavailable")
        self.assertNotIn("language-missing", {
            reason["kind"] for reason in coverage["reasons"]
        })
        restricted = next(
            reason for reason in coverage["reasons"]
            if reason.get("sourceState") == "rights-restricted"
        )
        self.assertEqual(restricted["kind"], "text-withheld")
        self.assertEqual(restricted["sourceKind"], "rights-withheld")
        self.assertGreater(restricted["count"], 0)
        unavailable = next(
            reason for reason in coverage["reasons"]
            if reason.get("sourceState") == "unavailable"
        )
        self.assertEqual(unavailable["kind"], "text-not-held")
        applicability = next(
            reason for reason in coverage["reasons"]
            if reason.get("sourceKind") == "applicability-unresolved"
        )
        self.assertEqual(applicability["sourceState"], "unresolved")
        self.assertEqual(
            [row["element"] for row in result["ordinaryUnresolved"]],
            ["ritus-initiales/gloria-in-excelsis"],
        )
        self.assertIn(
            "ordinary-element/symbolum/symbolum-nicaenum",
            {event["id"] for event in result["events"]},
        )

        event = next(
            event for event in result["events"]
            if event["kind"] == "ordinary-element" and
            event["selected"]["absenceKey"] ==
            "approved-english-publication-restriction"
        )
        selected = event["selected"]
        self.assertEqual(selected["availability"], "unavailable")
        self.assertFalse(selected["held"])
        self.assertEqual(selected["reason"], "rights-restricted")
        self.assertEqual(selected["unavailableState"], "rights-restricted")
        self.assertIsNone(selected["sourceId"])
        self.assertIsNone(selected["text"])

    def test_unmodelled_preface_and_local_solemnity_facts_stay_unresolved(self) -> None:
        request = copy.deepcopy(
            fixture_named("day-postconciliar-2026-11-29")["requested"]
        )
        request["requestedMode"] = "study"
        request["options"]["ordinary"] = True
        request["options"]["legitimate"]["eucharistic-prayer"] = "ep-iv"
        request["languages"]["ordinary"] = "en"
        result = node_call({"op": "ordinary-coverage", "request": request})
        unresolved = {
            row["element"]: row["condition"]
            for row in result["ordinaryUnresolved"]
        }
        self.assertIn("ritus-initiales/gloria-in-excelsis", unresolved)
        self.assertIn("particular-celebration-of-more-solemn-character",
                      unresolved["ritus-initiales/gloria-in-excelsis"]["predicates"])
        self.assertEqual(
            unresolved["prex-eucharistica/prex-eucharistica-iv"]["predicates"],
            ["mass-has-no-proper-preface"],
        )
        event_ids = {event["id"] for event in result["events"]}
        self.assertNotIn(
            "ordinary-element/prex-eucharistica/prex-eucharistica-iv",
            event_ids,
        )

    def test_day_and_cli_reject_cross_recension_structure_and_ordinary(self) -> None:
        result = node_call({"op": "cross-recension"})
        self.assertRegex(result["dayStructure"], r"structure.*requested edition")
        self.assertRegex(result["dayOrdinary"], r"Ordinary.*requested edition")
        self.assertRegex(result["cliStructure"], r"structure.*requested edition")
        self.assertRegex(result["cliOrdinary"], r"Ordinary.*requested edition")

    def test_unknown_ordinary_applicability_is_suppressed_and_typed(self) -> None:
        result = node_call({"op": "synthetic-ordinary-condition"})
        self.assertEqual(result["events"], [])
        self.assertEqual(len(result["ordinaryUnresolved"]), 1)
        unresolved = result["ordinaryUnresolved"][0]
        self.assertEqual(unresolved["kind"], "ordinary-unresolved")
        self.assertEqual(unresolved["state"], "unresolved")
        self.assertEqual(unresolved["element"], "conditional/element")
        self.assertEqual(unresolved["condition"]["kind"], "include-when-any")
        coverage = next(
            row for row in result["coverage"] if row["scope"].startswith("ordinary:")
        )
        self.assertEqual(coverage["state"], "supported")
        self.assertEqual(coverage["completeness"], "partial")
        reason = next(
            row for row in coverage["reasons"]
            if row.get("sourceKind") == "applicability-unresolved"
        )
        self.assertEqual(reason["sourceState"], "unresolved")
        self.assertEqual(reason["elements"], ["conditional/element"])

    def test_all_ordinary_variant_groups_are_selected_without_concatenation(self) -> None:
        result = node_call({"op": "synthetic-ordinary-variants"})
        elements = [
            event for event in result["events"] if event["kind"] == "ordinary-element"
        ]
        self.assertEqual([event["id"] for event in elements], [
            "ordinary-element/variants/by",
        ])
        self.assertEqual(elements[0]["selected"]["text"], "by")
        self.assertEqual(result["ordinaryUnresolved"], [])

    def test_rights_restricted_translation_is_typed_and_never_leaks(self) -> None:
        result = node_call({
            "op": "synthetic-propers", "language": "en", "rightsRestricted": True,
        })
        collect = next(one for one in result["events"] if one["editionSlotLabel"] == "Collect")
        selected = collect["selected"]
        self.assertEqual(selected["availability"], "unavailable")
        self.assertEqual(selected["reason"], "rights-restricted")
        self.assertEqual(selected["unavailableState"], "rights-restricted")
        self.assertFalse(selected["held"])
        self.assertTrue(selected["missing"])
        self.assertIsNone(selected["text"])
        self.assertIsNone(selected["sourceId"])
        self.assertIsNone(selected["rights"])
        serialized = json.dumps(result)
        self.assertNotIn("protected-witness-must-not-escape", serialized)
        self.assertNotIn("protected exact wording must not escape", serialized)
        reasons = [reason["kind"] for row in result["coverage"] for reason in row["reasons"]]
        self.assertIn("text-withheld", reasons)
        self.assertNotIn("translation-missing", reasons)

        proper = {
            "text": "safe source Latin",
            "translations": [],
            "unavailable_translations": [{
                "lang": "en", "state": "rights-restricted",
                "source_id": "protected-witness-must-not-escape",
                "text": "protected exact wording must not escape",
            }],
        }
        direct = node_call({"op": "browser-oration", "proper": proper, "language": "en"})
        self.assertEqual(direct["availability"], "unavailable")
        self.assertEqual(direct["reason"], "rights-restricted")
        self.assertIsNone(direct["text"])
        self.assertIsNone(direct["source"])
        self.assertNotIn("protected", json.dumps(direct))

        corpus_gap = node_call({
            "op": "browser-oration",
            "proper": {"text": "safe source Latin", "translations": []},
            "language": "en",
        })
        self.assertNotEqual(corpus_gap.get("reason"), "rights-restricted")

        latin = node_call({
            "op": "synthetic-propers", "language": "la", "latinWithheld": True,
        })
        selected_latin = next(
            one for one in latin["events"] if one["editionSlotLabel"] == "Collect"
        )["selected"]
        self.assertEqual(selected_latin["availability"], "unavailable")
        self.assertEqual(selected_latin["reason"], "latin-withheld")
        self.assertEqual(selected_latin["unavailableState"], "unavailable")
        self.assertFalse(selected_latin["held"])
        self.assertTrue(selected_latin["missing"])
        self.assertIsNone(selected_latin["text"])
        self.assertNotIn("protected-latin", json.dumps(latin))
        latin_coverage = next(
            row for row in latin["coverage"] if row["scope"] == "proper-original:la"
        )
        self.assertEqual(latin_coverage, {
            "state": "unavailable",
            "scope": "proper-original:la",
            "reasons": [{"kind": "text-withheld", "count": 1}],
        })
        self.assertNotIn(
            "proper-translation:la", [row["scope"] for row in latin["coverage"]]
        )
        with self.assertRaises(AssertionError):
            node_call({
                "op": "synthetic-propers",
                "language": "la",
                "latinWithheld": True,
                "malformedLatin": {"held": True},
            })

        browser_latin = node_call({
            "op": "browser-oration",
            "proper": {
                "text": "protected Latin words must not escape",
                "latin": {
                    "withheld": True,
                    "retained": True,
                    "state": "rights-restricted",
                },
            },
            "language": "la",
        })
        self.assertEqual(browser_latin["availability"], "unavailable")
        self.assertFalse(browser_latin["held"])
        self.assertIsNone(browser_latin["text"])
        self.assertNotIn("protected Latin words", json.dumps(browser_latin))
        browser_source = BROWSER_CORE.read_text(encoding="utf-8")
        self.assertEqual(browser_source.count("'Latin text unavailable'"), 2)
        self.assertNotIn("Latin body is unavailable for public display", browser_source)

    def test_browser_typed_proper_body_absence_never_becomes_empty_text(self) -> None:
        proper = {
            "name": "Collect",
            "text": None,
            "text_status": {
                "state": "unavailable",
                "scope": "proper-body",
                "reasons": [{"kind": "witness-gap"}],
            },
            "translations": [],
        }

        latin = node_call({
            "op": "browser-oration", "proper": proper, "language": "la",
        })
        self.assertEqual(latin["availability"], "unavailable")
        self.assertEqual(latin["reason"], "latin-unavailable")
        self.assertEqual(latin["lang"], "la")
        self.assertTrue(latin["missing"])
        self.assertFalse(latin["held"])
        self.assertIsNone(latin["text"])
        self.assertIsNone(latin["source"])

        english_proper = copy.deepcopy(proper)
        english_proper["untranslated"] = [{
            "lang": "en",
            "state": "unavailable",
            "target": {"extent": "body"},
        }]
        english = node_call({
            "op": "browser-oration", "proper": english_proper, "language": "en",
        })
        self.assertEqual(english.get("availability"), "unavailable")
        self.assertEqual(english.get("reason"), "text-unavailable")
        self.assertEqual(english.get("lang"), "en")
        self.assertTrue(english.get("missing"))
        self.assertFalse(english.get("held"))
        self.assertIsNone(english.get("text"))
        self.assertIsNone(english.get("source"))
        self.assertNotEqual(english.get("lang"), "la")

    def test_browser_typed_body_absence_preserves_english_rights_reason(self) -> None:
        proper = {
            "name": "Collect",
            "text": None,
            "text_status": {
                "state": "unavailable",
                "scope": "proper-body",
                "reasons": [{"kind": "witness-gap"}],
            },
            "translations": [],
            "unavailable_translations": [{
                "lang": "en",
                "state": "rights-restricted",
                "target": {"extent": "body"},
            }],
        }

        english = node_call({
            "op": "browser-oration", "proper": proper, "language": "en",
        })
        self.assertEqual(english["availability"], "unavailable")
        self.assertEqual(english["reason"], "rights-restricted")
        self.assertEqual(english["unavailableState"], "rights-restricted")
        self.assertEqual(english["lang"], "en")
        self.assertTrue(english["missing"])
        self.assertFalse(english["held"])
        self.assertIsNone(english["text"])
        self.assertIsNone(english["source"])

    def test_browser_typed_body_absence_without_english_ledger_is_unavailable(self) -> None:
        proper = {
            "name": "Collect",
            "text": None,
            "text_status": {
                "state": "unavailable",
                "scope": "proper-body",
                "reasons": [{"kind": "witness-gap"}],
            },
            "translations": [],
        }

        english = node_call({
            "op": "browser-oration", "proper": proper, "language": "en",
        })
        self.assertEqual(english["availability"], "unavailable")
        self.assertEqual(english["reason"], "text-unavailable")
        self.assertEqual(english["lang"], "en")
        self.assertTrue(english["missing"])
        self.assertFalse(english["held"])
        self.assertIsNone(english["text"])
        self.assertIsNone(english["source"])
        self.assertNotEqual(english["lang"], "la")

    def test_missing_ordinary_language_is_explicitly_unavailable(self) -> None:
        request = copy.deepcopy(fixture_named("day-roman-1962-2026-08-02")["requested"])
        request["requestedMode"] = "missal"
        request["options"]["ordinary"] = True
        request["languages"]["ordinary"] = "zz-contract-unheld"
        result = node_call({"op": "ordinary-coverage", "request": request})
        row = next(one for one in result["coverage"] if one["scope"].startswith("ordinary:"))
        self.assertEqual(row["state"], "unavailable")
        self.assertEqual(row["reasons"][0]["kind"], "language-missing")

    def test_ordinary_frame_producers_share_the_fail_closed_contract(self) -> None:
        self.assertEqual(
            MASS_TODAY_MODULE.validated_ordinary_frame(),
            {"applicability": "full"},
        )
        accepted = (
            {"applicability": "full"},
            {"applicability": "full", "basis": "source basis"},
            {"applicability": "none", "basis": "source basis"},
            {"applicability": "unavailable", "basis": "source basis"},
        )
        validators = (
            MASS_TODAY_MODULE.validated_ordinary_frame,
            MASS_PROPERS_MODULE.public_ordinary_frame,
        )
        for validator in validators:
            for frame in accepted:
                with self.subTest(validator=validator.__module__, accepted=frame):
                    self.assertEqual(validator(frame), frame)

        malformed = (
            None,
            False,
            [],
            "full",
            {},
            {"basis": "source"},
            {1: "source"},
            {"applicability": "invented"},
            {"applicability": "none"},
            {"applicability": "none", "basis": ""},
            {"applicability": "none", "basis": "   "},
            {"applicability": "none", "basis": 123},
            {"applicability": "unavailable"},
            {"applicability": "full", "basis": ""},
            {"applicability": "full", "basis": "   "},
            {"applicability": "full", "basis": 123},
            {"applicability": "full", "basis": "source", "extra": True},
        )
        for validator in validators:
            for frame in malformed:
                with self.subTest(validator=validator.__module__, malformed=frame):
                    with self.assertRaises((ValueError, MASS_TODAY_MODULE.Refused)):
                        validator(frame)

    def test_mass_today_withheld_latin_capability_uses_public_unavailable_state(self) -> None:
        proper = {
            "name": "Collect",
            "text": None,
            "latin": {
                "withheld": True,
                "held": False,
                "available": False,
                "state": "unavailable",
                "target": "Collect",
            },
        }
        self.assertEqual(
            MASS_TODAY_MODULE.language_projection(proper, "la", None),
            {
                "requested": "la",
                "status": "unavailable",
                "held": False,
                "available": False,
                "complete": False,
                "reason": {"state": "text-withheld", "lang": "la"},
            },
        )
        for mutation in ({"held": True}, {"available": True}, {"state": "private"}):
            malformed = copy.deepcopy(proper)
            malformed["latin"].update(mutation)
            with self.subTest(mutation=mutation), self.assertRaises(
                MASS_TODAY_MODULE.Refused
            ):
                MASS_TODAY_MODULE.language_projection(malformed, "la", None)
        malformed = copy.deepcopy(proper)
        malformed["text"] = "private Latin body"
        with self.assertRaises(MASS_TODAY_MODULE.Refused):
            MASS_TODAY_MODULE.language_projection(malformed, "la", None)

    def test_exceptional_rites_never_borrow_or_seat_the_ordinary_frame(self) -> None:
        expected = {
            "none": ("absent", "semantic-absence"),
            "unavailable": ("unavailable", "text-not-held"),
        }
        for applicability, (state, reason) in expected.items():
            with self.subTest(applicability=applicability):
                result = node_call({
                    "op": "synthetic-ordinary-frame",
                    "applicability": applicability,
                })
                self.assertEqual(result["events"], [])
                frame = next(
                    row for row in result["coverage"]
                    if row["scope"].startswith("ordinary-frame:")
                )
                self.assertEqual(frame["state"], state)
                self.assertEqual(frame["reasons"], [{
                    "kind": reason,
                    "basis": "source-owned frame basis",
                    "applicability": applicability,
                }])

        with self.assertRaisesRegex(AssertionError, "no usable semantic Ordinary seat"):
            node_call({
                "op": "synthetic-ordinary-frame", "applicability": "full",
                "properName": "Collect",
            })

        accepted = (
            {"frame": {"applicability": "none", "basis": "source basis"}},
            {"frame": {"applicability": "unavailable", "basis": "source basis"}},
        )
        for case in accepted:
            with self.subTest(accepted=case):
                result = node_call({
                    "op": "synthetic-ordinary-frame", "properName": "Collect", **case,
                })
                self.assertNotIn("error", result)

        malformed = (
            None,
            False,
            [],
            "full",
            {},
            {"basis": "source"},
            {"applicability": "invented"},
            {"applicability": "none"},
            {"applicability": "none", "basis": ""},
            {"applicability": "none", "basis": "   "},
            {"applicability": "none", "basis": 123},
            {"applicability": "unavailable"},
            {"applicability": "full", "basis": ""},
            {"applicability": "full", "basis": "   "},
            {"applicability": "full", "basis": 123},
            {"applicability": "full", "basis": "source", "extra": True},
        )
        for frame in malformed:
            with self.subTest(frame=frame):
                refused = node_call({
                    "op": "synthetic-ordinary-frame", "frame": frame,
                    "captureError": True,
                })
                self.assertRegex(refused["error"], r"Ordinary.frame|Ordinary-frame|source basis")

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

    def test_inherited_pre_1955_propers_are_partial_not_complete(self) -> None:
        request = copy.deepcopy(
            fixture_named("propers-roman-1962-advent-1")["requested"]
        )
        request["edition"] = {"id": "roman-pre-1955"}

        result = node_call({
            "op": "adapt-fixture",
            "fixture": {"requested": request},
        })
        formulary = next(
            row for row in result["coverage"]
            if row["scope"] == "formulary:advent-1"
        )
        self.assertEqual(formulary, {
            "state": "supported",
            "scope": "formulary:advent-1",
            "completeness": "partial",
            "reasons": [{
                "kind": "partial-recension",
                "recensionStatus": "structural-only",
                "domain": "propers",
                "domainState": "none",
                "sourceCalendar": "roman-1962",
                "inheritanceStatus": "uncollated",
            }, {
                "kind": "text-not-held",
                "count": 3,
                "repositoryTerm": "proper-body",
                "claims": [
                    {"proper": "Collect", "cycle": None},
                    {"proper": "Secret", "cycle": None},
                    {"proper": "Postcommunion", "cycle": None},
                ],
            }],
        })
        self.assertFalse(any(
            row.get("scope") == "formulary:advent-1"
            and row.get("completeness") == "complete"
            for row in result["coverage"]
        ))

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

        translated = node_call({
            "op": "synthetic-composed-cycles", "translationOnly": True, "cycle": "B",
        })
        selected = translated["events"][0]["selected"]
        self.assertEqual(selected["availability"], "held")
        self.assertEqual(selected["sourceId"], "witness-cycle-B")
        self.assertEqual(selected["text"], "translated-cycle-B")

    def test_day_cycle_families_are_independent_order_free_and_mixed_fails_closed(self) -> None:
        for family, lectionary, cycle, dimension, references in (
            ("sunday", {"sunday": "A", "weekday": "II"}, "A", "sunday", ["Sunday A"]),
            ("sunday", {"sunday": "B", "weekday": "I"}, "B", "sunday", ["Sunday B"]),
            ("weekday", {"sunday": "A", "weekday": "II"}, "II", "weekday", ["Weekday II"]),
            ("weekday", {"sunday": "B", "weekday": "I"}, "I", "weekday", ["Weekday I"]),
        ):
            forward = node_call({
                "op": "synthetic-day-cycle", "family": family, "lectionary": lectionary,
            })
            reverse = node_call({
                "op": "synthetic-day-cycle", "family": family,
                "lectionary": lectionary, "reverse": True,
            })
            self.assertEqual(forward, reverse)
            selected = forward["events"][0]["selected"]
            self.assertEqual(selected["cycle"], cycle)
            self.assertEqual(selected["cycleDimension"], dimension)
            self.assertEqual(selected["references"], references)
            self.assertEqual(selected["cycles"], [cycle] if dimension == "sunday" else [])
            self.assertEqual(
                selected["weekdayCycles"], [cycle] if dimension == "weekday" else [],
            )
        # The source contract defines no composition rule for two axes on one
        # Proper; selecting both would merge appointed material by invention.
        with self.assertRaises(AssertionError):
            node_call({"op": "synthetic-day-cycle", "family": "both"})

        core = node_call({
            "op": "browser-cycles", "cycle": "II", "proper": {
                "citations": [{"ref": "annual"}],
                "cycles": {"B": {"citations": [{"ref": "Sunday B"}]}},
                "weekday_cycles": {"II": {"citations": [{"ref": "Weekday II"}]}},
            },
        })
        self.assertEqual(core["all"], ["B", "II"])
        self.assertEqual(core["sunday"], ["B"])
        self.assertEqual(core["weekday"], ["II"])
        self.assertEqual([one["ref"] for one in core["selected"]["citations"]], ["Weekday II"])
        self.assertEqual(core["citations"], ["annual", "Sunday B", "Weekday II"])

    def test_selected_cycle_uses_only_its_typed_untranslated_state(self) -> None:
        cases = (
            ("A", "rights-restricted"),
            ("C", "unavailable"),
        )
        for cycle, state in cases:
            with self.subTest(cycle=cycle):
                result = node_call({"op": "synthetic-cycle-untranslated", "cycle": cycle})
                selected = result["events"][0]["selected"]
                self.assertEqual(selected["cycle"], cycle)
                self.assertEqual(selected["cycles"], [cycle])
                self.assertEqual(selected["unavailableState"], state)
                self.assertFalse(selected["held"])
                self.assertTrue(selected["missing"])
                self.assertIsNone(selected["text"])

        held = node_call({
            "op": "synthetic-cycle-untranslated", "cycle": "A",
            "variant": "cycle-owned-translation",
        })["events"][0]["selected"]
        self.assertEqual(held["availability"], "held")
        self.assertEqual(held["text"], "Cycle A held English.")
        self.assertEqual(held["sourceId"], "edition.synthetic.cycle-a")
        self.assertNotIn("Parent English", json.dumps(held))

        restricted = node_call({
            "op": "synthetic-cycle-untranslated", "cycle": "A",
            "variant": "cycle-owned-restriction",
        })["events"][0]["selected"]
        self.assertEqual(restricted["availability"], "unavailable")
        self.assertEqual(restricted["unavailableState"], "rights-restricted")
        self.assertFalse(restricted["held"])
        self.assertIsNone(restricted["text"])
        self.assertNotIn("Parent English", json.dumps(restricted))

    def test_cli_and_day_match_held_english_and_withheld_latin(self) -> None:
        held = node_call({"op": "synthetic-cli-language", "kind": "held-english"})
        self.assertEqual(held["day"], held["cli"])
        selected = held["day"]["events"][0]["selected"]
        self.assertEqual(selected["language"], "en")
        self.assertEqual(selected["availability"], "held")
        self.assertEqual(selected["text"], "Held English text.")

        withheld = node_call({"op": "synthetic-cli-language", "kind": "withheld-latin"})
        self.assertEqual(withheld["day"], withheld["cli"])
        selected = withheld["day"]["events"][0]["selected"]
        self.assertEqual(selected["reason"], "latin-withheld")
        self.assertEqual(selected["unavailableState"], "unavailable")
        self.assertFalse(selected["held"])
        self.assertIsNone(selected["text"])
        self.assertNotIn("protected-latin", json.dumps(withheld))

    def test_propers_adapter_rejects_a_mismatched_formulary_type(self) -> None:
        fixture = fixture_named("propers-roman-1962-advent-1")
        fixture["requested"]["formulary"]["type"] = "saints"
        with self.assertRaises(AssertionError):
            node_call({"op": "adapt-fixture", "fixture": fixture})

    def test_optional_day_choices_match_cli_and_require_explicit_formulary(self) -> None:
        cases = {
            "2026-08-07": [
                "saints-sixtus-ii-pope-companions-martyrs",
                "saint-cajetan-priest",
                "ot-18-friday",
            ],
            "2027-06-05": [
                "immaculate-heart-blessed-virgin-mary",
                "saint-boniface-bishop-martyr",
                "ot-9-saturday",
            ],
        }
        for date, keys in cases.items():
            with self.subTest(date=date):
                parity = node_call({
                    "op": "full-parity",
                    "request": self.optional_day_request(date),
                    "payload": self.optional_day_payload(date),
                })
                self.assertEqual(parity["day"], parity["cli"])
                outcome = parity["day"]
                self.assertIsNone(outcome["resolved"])
                self.assertEqual(outcome["events"], [])
                self.assertEqual(len(outcome["unresolvedChoices"]), 1)
                choice = outcome["unresolvedChoices"][0]
                self.assertEqual(choice["id"], "calendar-formulary")
                self.assertEqual([one["id"] for one in choice["options"]], keys)
                self.assertTrue(all(one.get("selected") is not True for one in choice["options"]))
                self.assertEqual(outcome["coverage"][0]["state"], "absent")

    def test_every_optional_day_arm_is_selectable_and_invalid_never_falls_back(self) -> None:
        cases = {
            "2026-08-07": [
                "saints-sixtus-ii-pope-companions-martyrs",
                "saint-cajetan-priest",
                "ot-18-friday",
            ],
            "2027-06-05": [
                "immaculate-heart-blessed-virgin-mary",
                "saint-boniface-bishop-martyr",
                "ot-9-saturday",
            ],
        }
        for date, keys in cases.items():
            payload = self.optional_day_payload(date)
            for key in keys:
                with self.subTest(date=date, key=key):
                    parity = node_call({
                        "op": "full-parity",
                        "request": self.optional_day_request(date, key),
                        "payload": payload,
                    })
                    self.assertEqual(parity["day"]["resolved"], parity["cli"]["resolved"])
                    self.assertEqual(
                        parity["day"]["calendarResult"], parity["cli"]["calendarResult"]
                    )
                    expected = {
                        "edition": "postconciliar", "formulary": key, "standing": "option",
                    }
                    for outcome in (parity["day"], parity["cli"]):
                        self.assertEqual(outcome["resolved"], expected)
                        self.assertTrue(outcome["events"])
                        self.assertNotIn(
                            "calendar-formulary",
                            [one["id"] for one in outcome["unresolvedChoices"]],
                        )
            with self.subTest(date=date, key="not-authorized"):
                with self.assertRaises(AssertionError):
                    node_call({
                        "op": "full-parity",
                        "request": self.optional_day_request(date, "not-authorized"),
                        "payload": payload,
                    })

    def test_territory_choice_and_each_explicit_branch_match_without_default(self) -> None:
        date = "2026-05-14"
        template = copy.deepcopy(
            fixture_named("day-postconciliar-2026-11-29")["requested"]
        )
        template["civilDate"] = date
        template["options"]["ordinary"] = False
        template.pop("selectedReadableFormulary", None)

        unresolved = node_call({
            "op": "full-parity",
            "request": template,
            "payload": self.territory_payload(date),
        })
        self.assertIsNone(unresolved["day"]["resolved"])
        self.assertEqual(unresolved["day"], unresolved["cli"])
        self.assertEqual(
            unresolved["day"]["unresolvedChoices"][0]["id"],
            "calendar-territory",
        )
        self.assertEqual(
            [
                row["id"]
                for row in unresolved["day"]["unresolvedChoices"][0]["options"]
            ],
            ["ascension-thursday", "ascension-transferred-to-sunday"],
        )

        cases = (
            ("ascension-thursday", "ascension"),
            ("ascension-transferred-to-sunday", "saint-matthias-apostle"),
        )
        for territory, mass in cases:
            with self.subTest(territory=territory):
                request = copy.deepcopy(template)
                request["calendar"]["territory"] = {"id": territory}
                request["selectedReadableFormulary"] = {"id": mass}
                parity = node_call({
                    "op": "full-parity",
                    "request": request,
                    "payload": self.territory_payload(date, territory),
                })
                self.assertEqual(parity["day"]["resolved"], parity["cli"]["resolved"])
                self.assertEqual(
                    parity["day"]["calendarResult"], parity["cli"]["calendarResult"]
                )
                self.assertEqual(
                    parity["day"]["calendarResult"]["selectedBranch"], territory
                )
                self.assertEqual(parity["day"]["resolved"]["formulary"], mass)

        invalid = copy.deepcopy(template)
        invalid["calendar"]["territory"] = {"id": "not-held"}
        with self.assertRaisesRegex(AssertionError, "territorial Day branch is not held"):
            node_call({
                "op": "full-parity", "request": invalid,
                "payload": self.territory_payload(date),
            })

    def test_real_multiform_subsequences_keep_exact_seating_and_event_ids(self) -> None:
        cases = (
            ("2026-12-25", "nativitate-domini-octave", "night", 10),
            ("2026-12-25", "nativitate-domini-octave", "dawn", 10),
            ("2026-12-25", "nativitate-domini-octave", "day", 9),
            ("2026-11-02", "commemoratione-omnium-fidelium-defunctorum", "first", 11),
            ("2026-11-02", "commemoratione-omnium-fidelium-defunctorum", "second", 11),
            ("2026-11-02", "commemoratione-omnium-fidelium-defunctorum", "third", 11),
        )
        template = fixture_named("day-roman-1962-2026-08-02")["requested"]
        for date, mass, form, proper_count in cases:
            with self.subTest(date=date, mass=mass, form=form):
                request = copy.deepcopy(template)
                request["civilDate"] = date
                request["selectedReadableFormulary"] = {"id": mass}
                request["form"] = form
                request["requestedMode"] = "missal"
                request["options"]["ordinary"] = True
                parity = node_call({
                    "op": "full-parity", "request": request,
                    "payload": self.form_payload(date, form),
                })
                self.assertEqual(parity["day"], parity["cli"])
                self.assertEqual(parity["day"]["resolved"]["form"], form)
                proper_events = [
                    event for event in parity["day"]["events"]
                    if event["kind"] == "proper"
                ]
                self.assertEqual(len(proper_events), proper_count)
                if mass == "commemoratione-omnium-fidelium-defunctorum":
                    labels = [event["editionSlotLabel"] for event in proper_events]
                    self.assertLess(labels.index("Tract"), labels.index("Sequence"))
                    self.assertLess(labels.index("Sequence"), labels.index("Gospel"))
                self.assertEqual(
                    len({event["id"] for event in parity["day"]["events"]}),
                    len(parity["day"]["events"]),
                )
                self.assertTrue(all(
                    event["seat"] and event["seat"]["placement"] == "seated" and
                    event["seat"]["id"]
                    for event in proper_events
                ))

        for form, proper_count, first_index in (
            ("longer", 19, 1),
            ("shorter", 11, 20),
        ):
            with self.subTest(date="2026-12-19", mass="advent-ember-saturday", form=form):
                result = node_call({
                    "op": "source-ordinary-frame", "id": "roman-1962",
                    "date": "2026-12-19", "mass": "advent-ember-saturday",
                    "form": form,
                })
                self.assertEqual(result["resolved"]["form"], form)
                self.assertEqual(len(result["events"]), proper_count)
                self.assertEqual(
                    [event["id"] for event in result["events"]],
                    [
                        f"proper/roman-1962/advent-ember-saturday/{index:03d}"
                        for index in range(first_index, first_index + proper_count)
                    ],
                )
                self.assertTrue(all(
                    event["kind"] == "proper" and event["seat"] is None
                    for event in result["events"]
                ))
                placement = next(
                    row for row in result["coverage"]
                    if row["scope"] == "ordinary-placement:roman-1962"
                )
                frame = next(
                    row for row in result["coverage"]
                    if row["scope"] == "ordinary-frame:roman-1962"
                )
                self.assertEqual(placement["state"], "unsupported")
                self.assertEqual(
                    placement["reasons"][0]["kind"],
                    "ordinary-placement-unavailable",
                )
                self.assertEqual(frame["state"], "unavailable")
                self.assertEqual(
                    frame["reasons"][0]["applicability"], "unavailable"
                )

    def test_real_exceptional_rites_never_borrow_the_ordinary(self) -> None:
        cases = (
            ("2027-03-21", "palm-sunday", "unavailable", "unavailable", "text-not-held"),
            ("2027-03-26", "good-friday", "none", "absent", "semantic-absence"),
            ("2027-03-27", "easter-vigil", "unavailable", "unavailable", "text-not-held"),
        )
        template = fixture_named("day-roman-1962-2026-08-02")["requested"]
        for date, mass, applicability, state, reason in cases:
            with self.subTest(date=date, mass=mass):
                request = copy.deepcopy(template)
                request["civilDate"] = date
                request["edition"] = {"id": "roman-pre-1955"}
                request["calendar"] = {"id": "roman-pre-1955"}
                request["selectedReadableFormulary"] = {"id": mass}
                request["requestedMode"] = "missal"
                request["options"]["ordinary"] = True
                parity = node_call({
                    "op": "full-parity", "request": request,
                    "payload": self.historical_payload(date),
                })
                self.assertEqual(parity["day"], parity["cli"])
                self.assertFalse(any(
                    event["kind"].startswith("ordinary-")
                    for event in parity["day"]["events"]
                ))
                frame = next(
                    row for row in parity["day"]["coverage"]
                    if row["scope"] == "ordinary-frame:roman-pre-1955"
                )
                self.assertEqual(frame["state"], state)
                self.assertEqual(frame["reasons"][0]["kind"], reason)
                self.assertEqual(
                    frame["reasons"][0]["applicability"], applicability
                )
                self.assertTrue(frame["reasons"][0]["basis"])

    def test_source_owned_postconciliar_exceptional_frames_reach_adapter(self) -> None:
        cases = (
            ("2027-03-26", "good-friday", "none", "absent", "semantic-absence"),
            ("2027-03-27", "easter-vigil", "unavailable", "unavailable", "text-not-held"),
        )
        for date, mass, applicability, state, reason in cases:
            with self.subTest(date=date, mass=mass):
                result = node_call({
                    "op": "source-ordinary-frame", "id": "postconciliar",
                    "date": date, "mass": mass,
                })
                self.assertFalse(any(
                    event["kind"].startswith("ordinary-") for event in result["events"]
                ))
                frame = next(
                    row for row in result["coverage"]
                    if row["scope"] == "ordinary-frame:postconciliar"
                )
                self.assertEqual(frame["state"], state)
                self.assertEqual(frame["reasons"][0]["kind"], reason)
                self.assertEqual(frame["reasons"][0]["applicability"], applicability)
                self.assertTrue(frame["reasons"][0]["basis"])

    def test_source_claim_absences_and_common_sets_block_complete_coverage(self) -> None:
        fatima = node_call({
            "op": "source-claim-coverage", "id": "postconciliar",
            "mass": "our-lady-fatima",
        })
        self.assertEqual(fatima["events"], [])
        self.assertEqual(fatima["coverage"][0]["state"], "unavailable")
        self.assertNotEqual(fatima["coverage"][0].get("completeness"), "complete")

        lawrence_key = "s-laurentii-brundusio-confessoris-ecclesiae-doctoris"
        lawrence = node_call({
            "op": "source-claim-coverage", "id": "roman-1962",
            "mass": lawrence_key,
        })
        formulary = next(row for row in lawrence["coverage"]
                         if row["scope"] == f"formulary:{lawrence_key}")
        self.assertEqual((formulary["state"], formulary["completeness"]),
                         ("supported", "partial"))
        self.assertTrue(any(
            row["scope"].endswith("/main/collect")
            and row["repositoryTerm"] == "proper-collect"
            for row in lawrence["explicitAbsences"]
        ))
        self.assertFalse(any(
            event.get("editionSlotLabel") == "Collect"
            for event in lawrence["events"]
        ))

        stanislaus = node_call({
            "op": "source-claim-coverage", "id": "roman-1962",
            "mass": "s-stanislai-episcopi-martyris",
        })
        common_choice = next(
            row for row in stanislaus["unresolvedChoices"]
            if row["id"].startswith("common-set:")
        )
        self.assertEqual([option["id"] for option in common_choice["options"]],
                         ["c3", "c4"])
        self.assertEqual(stanislaus["coverage"][0]["completeness"], "partial")
        self.assertIn("unresolved-choice", {
            reason["kind"] for reason in stanislaus["coverage"][0]["reasons"]
        })

    def test_source_claim_statuses_and_common_set_dispositions_fail_closed(self) -> None:
        malformed = (
            ("postconciliar", "our-lady-fatima", "mass-status"),
            ("roman-1962", "s-laurentii-brundusio-confessoris-ecclesiae-doctoris",
             "proper-status"),
            ("roman-1962", "s-stanislai-episcopi-martyris", "common-set"),
        )
        for edition, mass, mutation in malformed:
            with self.subTest(mutation=mutation), self.assertRaises(AssertionError):
                node_call({
                    "op": "source-claim-coverage", "id": edition,
                    "mass": mass, "malformed": mutation,
                })

    def test_mass_today_expanded_matches_day_identity_order_seats_and_sources(self) -> None:
        for name in ("day-roman-1962-2026-08-02", "day-postconciliar-2026-11-29"):
            fixture = fixture_named(name)
            request = copy.deepcopy(fixture["requested"])
            request["requestedMode"] = "missal"
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
            self.assertEqual(parity["day"]["ordinaryUnresolved"],
                             parity["cli"]["ordinaryUnresolved"], name)
            proper_events = [one for one in parity["day"]["events"] if one["kind"] == "proper"]
            self.assertEqual(len(proper_events), 10)
            self.assertTrue(all(one["seat"]["placement"] == "seated" for one in proper_events))

    def test_postconciliar_2026_2027_weekday_and_sunday_cli_browser_cycle_parity(self) -> None:
        cases = (
            ("2027-08-26", "weekday", "I", "1 Thessalonians 3:7-13"),
            ("2026-08-26", "weekday", "II", "2 Thessalonians 3:6-10, 16-18"),
            ("2026-08-30", "sunday", "A", "Jeremiah 20:7-9"),
        )
        template = fixture_named("day-postconciliar-2026-11-29")["requested"]
        for date, dimension, cycle, first_reading in cases:
            run = subprocess.run(
                [str(MASS_TODAY), "show", "--date", date,
                 "--calendar", "postconciliar", "--bible", "douay-rheims",
                 "--expanded", "--why", "--format", "json"],
                capture_output=True, text=True, cwd=ROOT, check=False,
            )
            self.assertEqual(run.returncode, 0, run.stdout + run.stderr)
            payload = json.loads(run.stdout)
            day = payload["days"][0]
            said = [one for one in day["masses"] if one["standing"] == "said"]
            if said:
                self.assertEqual(len(said), 1)
                mass = said[0]
            else:
                # Ordinary-Time weekdays hold a deterministic ferial reading
                # course but no source-selected oration owner.  Select that
                # sole readable formulary explicitly without upgrading its
                # fail-closed standing to "said".
                self.assertEqual(len(day["masses"]), 1)
                mass = day["masses"][0]
                self.assertEqual(mass["standing"], "unresolved")
            request = copy.deepcopy(template)
            request["civilDate"] = date
            request["selectedReadableFormulary"] = {"id": mass["key"]}
            request["options"]["ordinary"] = False
            parity = node_call({"op": "full-parity", "request": request, "payload": payload})
            self.assertEqual(parity["day"]["resolved"], parity["cli"]["resolved"], date)
            self.assertEqual(parity["day"]["calendarResult"], parity["cli"]["calendarResult"], date)
            self.assertEqual(parity["day"]["events"], parity["cli"]["events"], date)
            event = next(
                one for one in parity["day"]["events"]
                if one["editionSlotLabel"] == "First Reading"
            )
            self.assertEqual(event["selected"]["references"], [first_reading])
            self.assertEqual(event["selected"]["cycle"], cycle)
            self.assertEqual(event["selected"]["cycleDimension"], dimension)
            self.assertEqual(
                event["selected"]["cycles"], [cycle] if dimension == "sunday" else [],
            )
            self.assertEqual(
                event["selected"]["weekdayCycles"],
                [cycle] if dimension == "weekday" else [],
            )
            payload_proper = next(
                one for one in mass["propers"] if one["name"] == "First Reading"
            )
            self.assertEqual(
                sorted((payload_proper.get("cycles") or {}).keys()),
                ["A", "B", "C"] if dimension == "sunday" else [],
            )
            self.assertEqual(
                sorted((payload_proper.get("weekday_cycles") or {}).keys()),
                ["I", "II"] if dimension == "weekday" else [],
            )

    def test_cli_parity_rejects_bible_lectionary_reference_and_text_drift(self) -> None:
        fixture = fixture_named("day-roman-1962-2026-08-02")
        request = copy.deepcopy(fixture["requested"])
        request["requestedMode"] = "missal"
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
        mutations.append((changed, "payload Bible does not match"))
        changed = copy.deepcopy(payload)
        changed["days"][0]["why"]["lectionary"] = {"sunday": "X", "weekday": "Y"}
        mutations.append((changed, "lectionary result disagrees"))
        changed = copy.deepcopy(payload)
        scripture = next(one for one in changed["days"][0]["masses"][0]["propers"] if one["verses"])
        scripture["verses"][0]["ref"] = "invented drift"
        mutations.append((changed, "scripture references disagree"))
        changed = copy.deepcopy(payload)
        withheld = next(
            one
            for mass in changed["days"][0]["masses"]
            for one in mass["propers"]
            if (one.get("latin") or {}).get("withheld")
        )
        withheld["latin"]["state"] = (
            "rights-restricted"
            if withheld["latin"]["state"] == "unavailable"
            else "unavailable"
        )
        mutations.append((changed, "withheld Latin state disagrees"))
        for changed, expected in mutations:
            with self.subTest(expected=expected), self.assertRaisesRegex(
                AssertionError, expected
            ):
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

    def test_promoted_production_routes_load_the_shared_reader_contract(self) -> None:
        controllers = {
            "day.html": "day-reader.js",
            "index.html": "propers-reader.js",
        }
        state_tag = '<script src="reader-state.js"></script>'
        adapters_tag = '<script src="reader-state-adapters.js"></script>'
        for name, controller in controllers.items():
            with self.subTest(route=name):
                page = (ROOT / "src/web/browser/liturgy" / name).read_text(
                    encoding="utf-8"
                )
                controller_tag = f'<script src="{controller}"></script>'
                self.assertEqual(page.count(state_tag), 1)
                self.assertEqual(page.count(adapters_tag), 1)
                self.assertEqual(page.count(controller_tag), 1)
                self.assertLess(page.index(state_tag), page.index(adapters_tag))
                self.assertLess(page.index(adapters_tag), page.index(controller_tag))


if __name__ == "__main__":
    unittest.main()
