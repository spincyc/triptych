#!/usr/bin/env python3
"""Day reader missal-switch gates: a formulary key never crosses a missal.

The maintainer reported that a reader on `/liturgy/day.html` could not leave the
1962 Missal for the Postconciliar one. Apply carried `mass`, a 1962 formulary
key, into a missal that does not hold it; the reader rejected the selection,
titled the page "Selection unavailable", and blanked the missal select, so there
was no way back either.

These are not string assertions. Each test lifts the shipped composition out of
`day-reader.js` -- `hashWith`, the Apply handler, `resetDateSurface` -- replays
it under node against stubs, and then puts the composed hash through the
production contract, adapters, and assembly over the tracked corpus. A test that
only read the source would pass on a reader that composed the right hash and
still resolved the wrong Mass.
"""

from __future__ import annotations

import json
import shutil
import subprocess
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
READER = ROOT / "src/web/browser/liturgy/day-reader.js"

# 2026-08-08 is the reported date: the two missals keep different days on it, and
# 1962 offers a second readable row, so Apply's formulary select is on screen
# holding a key the Postconciliar Missal has never heard of.
REPORTED_DATE = "2026-08-08"
VIANNEY = "s-ioannis-mariae-vianney-confessoris"
CYRIACUS = "comm-ss-cyriaci-largi-smaragdi-martyrum"
DOMINIC = "saint-dominic-priest"
OT_18_SATURDAY = "ot-18-saturday"
# 2026-05-03 is Easter 4 in 1962 and Easter 5 in the Postconciliar Missal: the
# target missal holds a formulary for the day, and it is a different one.
DIVERGENT_DATE = "2026-05-03"
EASTER_4 = "easter-4"
EASTER_5 = "easter-5"
PHILIP_JAMES = "saints-philip-james-apostles"
# 2026-03-08 is the trap: BOTH missals spell the day's own formulary `lent-3`.
# Equal spelling is not a correspondence, and nothing may be mapped across on
# the strength of it.
SHARED_SPELLING_DATE = "2026-03-08"
LENT_3 = "lent-3"
JOHN_OF_GOD = "s-ioannis-a-deo-confessoris"

# The frozen reader-state v1 Day inventory, from `guidance/liturgy-reader-state.md`.
DAY_HASH_KEYS = {
    "date", "missal", "bible", "orations", "why", "ordinary", "ordinary-lang",
    "rubrics", "mass", "form", "translation-witness", "mode", "location",
    "eucharistic-prayer",
}

NODE_PRELUDE = r"""
const fs = require('fs');
const C = require('./src/web/browser/liturgy/reader-state.js');
const A = require('./src/web/browser/liturgy/reader-state-adapters.js');
const M = require('./src/web/browser/liturgy/assembly-model.js');
const input = JSON.parse(fs.readFileSync(0, 'utf8'));
const base = 'src/web/data/structure/';
const read = (path) => JSON.parse(fs.readFileSync(path, 'utf8'));

function derive(id, date) {
  return M.derive({
    date,
    year: read(base + 'calendar/' + id + '/' + date.slice(0, 4) + '.json'),
    rubrics: read(base + 'rubrics/' + id + '.json')
  });
}

function context(id, date) {
  const structures = {};
  structures[id] = read(base + 'propers/' + id + '.json');
  return A.validationContext({
    entrance: 'day',
    bibles: read('src/web/data/bibles.json'),
    properIndex: read(base + 'propers/index.json'),
    rubricsIndex: read(base + 'rubrics/index.json'),
    ordinaryIndex: {calendars: []},
    structures,
    ordinaries: {},
    derived: derive(id, date)
  });
}

// What the reader does with a hash once it has one: normalize it against the
// selected missal, then resolve the day through the production adapter.
function resolve(hash, missal, date) {
  const parsed = C.parseLegacy('day', hash, {variantKeys: []});
  const normalized = C.normalizeLegacy(parsed, {
    context: context(missal, date),
    remembered: {},
    defaults: {date, missal, bible: 'douay-rheims', orations: 'la'}
  });
  if (!normalized.ok) {
    return {
      ok: false,
      errors: normalized.errors.map((one) => one.path + ':' + one.code)
    };
  }
  normalized.state.requestedMode = 'read';
  const derived = derive(missal, date);
  const result = A.adaptDay({
    request: normalized.state,
    derived,
    structure: read(base + 'propers/' + missal + '.json'),
    ordinary: null
  });
  return {
    ok: true,
    missal: normalized.state.edition.id,
    date: normalized.state.civilDate,
    asked: normalized.state.selectedReadableFormulary
      ? normalized.state.selectedReadableFormulary.id : null,
    resolved: result.resolved ? result.resolved.formulary : null,
    title: derived.options[0].winner ? derived.options[0].winner.name : null,
    readable: (derived.options[0].readable || []).map((one) => one.key)
  };
}

// A select that answers like an HTMLSelectElement: a value it holds no option
// for reads back empty. The blank-select symptom cannot hide behind a stub.
function selectStub() {
  let options = [];
  let held = '';
  return {
    disabled: false,
    setOptions(rows) {
      options = rows;
      if (options.indexOf(held) < 0) held = '';
    },
    replaceChildren() { options = []; held = ''; },
    get options() { return options.slice(); },
    get value() { return held; },
    set value(next) { held = options.indexOf(next) >= 0 ? next : ''; }
  };
}

function missalRows(ids) {
  return ids.map((id) => ({id, label: id, edition: id, code: id}));
}

// The Apply handler and `hashWith`, exactly as day-reader.js ships them.
function replayApply(scenario) {
  const window = {location: {hash: scenario.hash}};
  const runtime = {normalized: scenario.previous, ordinary: null};
  const dateInput = {value: scenario.date};
  const missalSelect = {value: scenario.missal};
  const bibleSelect = {value: scenario.bible};
  const orationsSelect = {value: scenario.orations};
  const formularyField = {hidden: !scenario.formulary};
  const formularySelect = {value: scenario.formulary || ''};
  const ordinaryLangField = {hidden: true};
  const ordinaryLangSelect = {value: ''};
  const ordinaryOptionField = {hidden: true};
  const ordinaryOptionSelect = {value: ''};
  const readerShell = {close() {}};
  let captured = null;
  function navigate(updates, removals) {
    captured = {updates, removals: removals || []};
  }
  __HASH_WITH__
  const apply = function (event) { __APPLY_BODY__ };
  apply({preventDefault() {}});
  return {
    hash: hashWith(captured.updates, captured.removals),
    updates: captured.updates,
    removals: captured.removals
  };
}

// `resetDateSurface`, exactly as day-reader.js ships it: the surface a reader is
// left holding when a selection does not resolve.
function replayReset(scenario) {
  const window = {location: {hash: scenario.hash}};
  const runtime = {missals: missalRows(scenario.missals)};
  const T = {
    fillSelect(select, rows) { select.setOptions(rows.map((row) => row.value)); }
  };
  const dateInput = {value: 'stale'};
  const missalSelect = selectStub();
  const bibleSelect = selectStub();
  const orationsSelect = selectStub();
  const formularySelect = selectStub();
  const ordinaryLangSelect = selectStub();
  const ordinaryOptionSelect = selectStub();
  const formularyField = {hidden: false};
  const ordinaryLangField = {hidden: false};
  const ordinaryOptionField = {hidden: false};
  const dateStatus = {textContent: ''};
  let enabled = null;
  function setDateSurfaceEnabled(value) { enabled = value; }
  __RESET_BODY__
  resetDateSurface();
  return {
    date: dateInput.value,
    missal: missalSelect.value,
    missalOptions: missalSelect.options,
    enabled,
    status: dateStatus.textContent
  };
}

const operations = {
  resolve: (payload) => resolve(payload.hash, payload.missal, payload.date),
  apply: (payload) => replayApply(payload),
  reset: (payload) => replayReset(payload),
  compose: (payload) => {
    const window = {location: {hash: payload.hash}};
    __HASH_WITH__
    return {hash: hashWith(payload.updates, payload.removals || [])};
  }
};

process.stdout.write(JSON.stringify(
  input.calls.map((call) => operations[call.op](call))
));
"""


def source() -> str:
    return READER.read_text(encoding="utf-8")


def block(text: str, opener: str) -> str:
    """Return `opener` and everything through its matching closing brace."""
    start = text.index(opener)
    at = text.index("{", start)
    depth = 0
    while at < len(text):
        if text[at] == "{":
            depth += 1
        elif text[at] == "}":
            depth -= 1
            if depth == 0:
                return text[start:at + 1]
        at += 1
    raise AssertionError("unbalanced braces after " + opener)


def body(text: str, opener: str) -> str:
    """Return only the statements inside `opener`'s braces."""
    held = block(text, opener)
    return held[held.index("{") + 1:-1]


def bridge() -> str:
    held = source()
    return (
        NODE_PRELUDE
        .replace("__HASH_WITH__", block(held, "function hashWith(updates, removals) {"))
        .replace("__APPLY_BODY__", body(
            held, "dateForm.addEventListener('submit', function (event) {"))
        .replace("__RESET_BODY__", block(held, "function resetDateSurface() {"))
    )


def node(calls: list[dict]) -> list[dict]:
    if shutil.which("node") is None:
        raise unittest.SkipTest("node is not installed")
    run = subprocess.run(
        ["node", "-e", bridge()], cwd=ROOT, check=True, text=True,
        capture_output=True, input=json.dumps({"calls": calls}),
    )
    return json.loads(run.stdout)


def hash_of(date: str, missal: str, mass: str | None = None) -> str:
    pairs = [
        "date=" + date, "missal=" + missal,
        "bible=douay-rheims", "orations=la",
    ]
    if mass:
        pairs.append("mass=" + mass)
    return "#" + "&".join(pairs)


def apply_call(hash_value: str, date: str, missal: str, formulary: str | None,
               previous_date: str, previous_missal: str) -> dict:
    """One press of Apply, with the surface holding what it holds."""
    return {
        "op": "apply",
        "hash": hash_value,
        "date": date,
        "missal": missal,
        "bible": "douay-rheims",
        "orations": "la",
        "formulary": formulary,
        "previous": {"state": {
            "civilDate": previous_date, "edition": {"id": previous_missal},
            "languages": {"orations": "la"},
        }},
    }


def pairs_of(hash_value: str) -> dict:
    held = {}
    for pair in hash_value.lstrip("#").split("&"):
        if not pair:
            continue
        key, _, value = pair.partition("=")
        held[key] = value
    return held


class DayMissalSwitchTests(unittest.TestCase):
    def test_the_corpus_gives_no_correspondence_to_map(self) -> None:
        """Dropping is the only honest option: the keys are different objects."""
        rows = node([
            {"op": "resolve", "hash": hash_of(REPORTED_DATE, "roman-1962"),
             "missal": "roman-1962", "date": REPORTED_DATE},
            {"op": "resolve", "hash": hash_of(REPORTED_DATE, "postconciliar"),
             "missal": "postconciliar", "date": REPORTED_DATE},
        ])
        self.assertEqual(rows[0]["readable"], [VIANNEY, CYRIACUS])
        self.assertEqual(rows[1]["readable"], [DOMINIC, OT_18_SATURDAY])
        self.assertEqual(set(rows[0]["readable"]) & set(rows[1]["readable"]), set())
        self.assertEqual(rows[0]["title"], "S. Ioannis Mariae Vianney Confessoris")
        self.assertEqual(rows[1]["title"], "Saint Dominic, Priest")

    def test_carrying_the_key_across_a_missal_is_what_broke(self) -> None:
        """The reported symptom, reproduced through the production contract."""
        rows = node([
            {"op": "resolve",
             "hash": hash_of(REPORTED_DATE, "postconciliar", VIANNEY),
             "missal": "postconciliar", "date": REPORTED_DATE},
        ])
        self.assertFalse(rows[0]["ok"])
        self.assertEqual(rows[0]["errors"], ["mass:invalid-explicit-value"])

    def test_apply_drops_the_key_leaving_1962_for_the_postconciliar_missal(self) -> None:
        rows = node([
            apply_call(hash_of(REPORTED_DATE, "roman-1962", VIANNEY),
                       REPORTED_DATE, "postconciliar", VIANNEY,
                       REPORTED_DATE, "roman-1962"),
        ])
        composed = rows[0]["hash"]
        self.assertNotIn("mass", pairs_of(composed))
        self.assertEqual(pairs_of(composed)["missal"], "postconciliar")
        resolved = node([{"op": "resolve", "hash": composed,
                          "missal": "postconciliar", "date": REPORTED_DATE}])[0]
        self.assertTrue(resolved["ok"], resolved)
        self.assertIsNone(resolved["asked"])
        self.assertEqual(resolved["resolved"], DOMINIC)
        self.assertEqual(resolved["title"], "Saint Dominic, Priest")

    def test_apply_drops_the_key_returning_to_1962(self) -> None:
        rows = node([
            apply_call(hash_of(DIVERGENT_DATE, "postconciliar", PHILIP_JAMES),
                       DIVERGENT_DATE, "roman-1962", PHILIP_JAMES,
                       DIVERGENT_DATE, "postconciliar"),
        ])
        composed = rows[0]["hash"]
        self.assertNotIn("mass", pairs_of(composed))
        resolved = node([{"op": "resolve", "hash": composed,
                          "missal": "roman-1962", "date": DIVERGENT_DATE}])[0]
        self.assertTrue(resolved["ok"], resolved)
        self.assertEqual(resolved["resolved"], EASTER_4)

    def test_a_target_missal_keeping_a_different_day_resolves_its_own(self) -> None:
        """2026-05-03 is Easter 4 in one missal and Easter 5 in the other."""
        rows = node([
            apply_call(hash_of(DIVERGENT_DATE, "roman-1962", EASTER_4),
                       DIVERGENT_DATE, "postconciliar", EASTER_4,
                       DIVERGENT_DATE, "roman-1962"),
        ])
        composed = rows[0]["hash"]
        self.assertNotIn("mass", pairs_of(composed))
        resolved = node([{"op": "resolve", "hash": composed,
                          "missal": "postconciliar", "date": DIVERGENT_DATE}])[0]
        self.assertTrue(resolved["ok"], resolved)
        self.assertEqual(resolved["resolved"], EASTER_5)
        self.assertIn(PHILIP_JAMES, resolved["readable"])

    def test_a_key_spelled_the_same_in_both_missals_is_still_dropped(self) -> None:
        """Equal spelling is not identity, so it is not carried, only re-derived."""
        rows = node([
            apply_call(hash_of(SHARED_SPELLING_DATE, "roman-1962", JOHN_OF_GOD),
                       SHARED_SPELLING_DATE, "postconciliar", JOHN_OF_GOD,
                       SHARED_SPELLING_DATE, "roman-1962"),
            apply_call(hash_of(SHARED_SPELLING_DATE, "roman-1962", LENT_3),
                       SHARED_SPELLING_DATE, "postconciliar", LENT_3,
                       SHARED_SPELLING_DATE, "roman-1962"),
        ])
        for row in rows:
            self.assertNotIn("mass", pairs_of(row["hash"]))
        resolved = node([{"op": "resolve", "hash": rows[1]["hash"],
                          "missal": "postconciliar",
                          "date": SHARED_SPELLING_DATE}])[0]
        self.assertTrue(resolved["ok"], resolved)
        # The Postconciliar day is `lent-3` because that missal says so, not
        # because the 1962 hash spelled it.
        self.assertIsNone(resolved["asked"])
        self.assertEqual(resolved["resolved"], LENT_3)

    def test_the_key_survives_when_the_missal_and_the_day_do_not_change(self) -> None:
        """Nothing is dropped unconditionally: a chosen commemoration holds."""
        rows = node([
            apply_call(hash_of(REPORTED_DATE, "roman-1962", VIANNEY),
                       REPORTED_DATE, "roman-1962", CYRIACUS,
                       REPORTED_DATE, "roman-1962"),
        ])
        composed = rows[0]["hash"]
        # The newly selected formulary survives. Its prior form and semantic
        # location do not: both are identities inside the formulary being left.
        self.assertEqual(
            rows[0]["removals"],
            ["form", "translation-witness", "location"],
        )
        self.assertEqual(pairs_of(composed)["mass"], CYRIACUS)
        resolved = node([{"op": "resolve", "hash": composed,
                          "missal": "roman-1962", "date": REPORTED_DATE}])[0]
        self.assertTrue(resolved["ok"], resolved)
        self.assertEqual(resolved["asked"], CYRIACUS)
        self.assertEqual(resolved["resolved"], CYRIACUS)

    def test_a_date_change_drops_the_key_the_same_way(self) -> None:
        """The key belongs to a day as much as to a missal."""
        rows = node([
            apply_call(hash_of(REPORTED_DATE, "roman-1962", CYRIACUS),
                       DIVERGENT_DATE, "roman-1962", CYRIACUS,
                       REPORTED_DATE, "roman-1962"),
        ])
        self.assertNotIn("mass", pairs_of(rows[0]["hash"]))
        resolved = node([{"op": "resolve", "hash": rows[0]["hash"],
                          "missal": "roman-1962", "date": DIVERGENT_DATE}])[0]
        self.assertTrue(resolved["ok"], resolved)
        self.assertEqual(resolved["resolved"], EASTER_4)

    def test_a_removal_outranks_an_update_that_names_the_same_key(self) -> None:
        """The composition rule the Apply handler was already relying on."""
        rows = node([
            {"op": "compose", "hash": hash_of(REPORTED_DATE, "roman-1962", VIANNEY),
             "updates": {"missal": "postconciliar", "mass": VIANNEY},
             "removals": ["mass"]},
            {"op": "compose", "hash": hash_of(REPORTED_DATE, "roman-1962", VIANNEY),
             "updates": {"missal": "postconciliar", "mass": VIANNEY},
             "removals": []},
        ])
        self.assertNotIn("mass", pairs_of(rows[0]["hash"]))
        self.assertEqual(pairs_of(rows[1]["hash"])["mass"], VIANNEY)

    def test_the_composed_hash_stays_inside_the_frozen_v1_day_inventory(self) -> None:
        rows = node([
            apply_call(hash_of(REPORTED_DATE, "roman-1962", VIANNEY),
                       REPORTED_DATE, "postconciliar", VIANNEY,
                       REPORTED_DATE, "roman-1962"),
            apply_call(hash_of(REPORTED_DATE, "roman-1962", VIANNEY),
                       REPORTED_DATE, "roman-1962", CYRIACUS,
                       REPORTED_DATE, "roman-1962"),
        ])
        for row in rows:
            self.assertLessEqual(set(pairs_of(row["hash"])), DAY_HASH_KEYS)
            for key in ("date", "missal", "bible", "orations"):
                self.assertIn(key, pairs_of(row["hash"]))

    def test_a_failed_selection_still_shows_the_missal_in_effect(self) -> None:
        """The stranding symptom: a blank select cannot be switched back."""
        rows = node([
            {"op": "reset",
             "hash": hash_of(REPORTED_DATE, "postconciliar", VIANNEY),
             "missals": ["roman-1962", "postconciliar"]},
            {"op": "reset",
             "hash": hash_of(REPORTED_DATE, "roman-1962", DOMINIC),
             "missals": ["roman-1962", "postconciliar"]},
        ])
        self.assertEqual(rows[0]["missal"], "postconciliar")
        self.assertEqual(rows[1]["missal"], "roman-1962")
        for row in rows:
            self.assertEqual(row["missalOptions"], ["roman-1962", "postconciliar"])
            # The rest of the surface is still emptied: only the missal in
            # effect survives a failure, and no prior day does.
            self.assertEqual(row["date"], "")
            self.assertFalse(row["enabled"])

    def test_a_missal_no_manifest_offers_is_not_invented_into_the_select(self) -> None:
        rows = node([
            {"op": "reset", "hash": hash_of(REPORTED_DATE, "sarum-nonesuch"),
             "missals": ["roman-1962", "postconciliar"]},
            {"op": "reset", "hash": "#date=" + REPORTED_DATE,
             "missals": ["roman-1962", "postconciliar"]},
            {"op": "reset", "hash": hash_of(REPORTED_DATE, "postconciliar"),
             "missals": []},
        ])
        self.assertEqual([row["missal"] for row in rows], ["", "", ""])


if __name__ == "__main__":
    unittest.main()
