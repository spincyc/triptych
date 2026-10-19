#!/usr/bin/env python3
"""Typed coverage accounting and partial witness selection at both reader boundaries."""
from __future__ import annotations

import copy
import json
import os
from pathlib import Path
import subprocess
import sys
import unittest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))
import _missal_coverage as coverage

NODE = r"""
const fs = require('fs');
const input = JSON.parse(fs.readFileSync(0, 'utf8'));
global.window = {location: {search: ''}};
require('./src/web/browser/shared/browser-core.js');
const T = window.Triptych;
const A = require('./src/web/browser/liturgy/reader-state-adapters.js');
const C = require('./src/web/browser/liturgy/reader-state.js');
let out;
if (input.op === 'summary') out = T.summarizeCoverage(input.units);
if (input.op === 'labels') out = {
  languages: T.orationLanguagesOf(input.structure).map(T.orationLanguageLabel),
  witnesses: T.coverageWitnesses(input.structure.coverage, 'en'),
  notice: T.coverageSummaryText(input.structure.coverage, input.language || 'en', input.witness)
};
if (input.op === 'oration') out = T.orationFor(input.proper, 'en', input.witness);
if (input.op === 'adapt' || input.op === 'choices') {
  const request = {
    schema: C.STATE_SCHEMA, entrance: 'propers', civilDate: null,
    edition: {id: input.structure.calendar},
    formulary: {id: input.structure.masses[0].key, type: 'contract'},
    bible: {id: 'douay-rheims', numbering: 'vulgate'},
    languages: {orations: input.language || 'en'}, requestedMode: 'read',
    options: {ordinary: false, legitimate: {}}, coverage: [], unresolvedChoices: [], sourceHooks: []
  };
  if (input.witness) request.languages.translationWitness = input.witness;
  if (input.cycle) request.cycle = input.cycle;
  const result = A.adaptPropers({request, structure: input.structure});
  const units = T.selectedCoverageUnits(result, input.structure);
  out = {result, units, report: T.summarizeCoverage(units)};
  if (input.op === 'choices') {
    const runtime = {normalized: null};
    const Adapters = A;
    const day = fs.readFileSync('src/web/browser/liturgy/day-reader.js', 'utf8');
    const propers = fs.readFileSync('src/web/browser/liturgy/propers-reader.js', 'utf8');
    eval(day.slice(day.indexOf('  function translationWitnessState('), day.indexOf('  function validateExplicitTranslationWitness(')));
    eval(propers.slice(propers.indexOf('  function formularyWitnessState('), propers.indexOf('  function selectedBrowseMass(')));
    out = {day: translationWitnessState(result, input.structure, 'en'),
      propers: formularyWitnessState(input.structure, input.structure.masses[0], 'en', request)};
  }
}
if (input.op === 'ordinary') out = T.summarizeCoverage(T.selectedOrdinaryCoverageUnits(input.result, input.ordinary));
process.stdout.write(JSON.stringify(out));
"""


def node(**args):
    result = subprocess.run(["node", "-e", NODE], input=json.dumps(args), text=True,
                            capture_output=True, cwd=ROOT)
    if result.returncode:
        raise AssertionError(result.stderr)
    return json.loads(result.stdout)


def proper(target, occurrence, translations=(), *, cycle="all", rights=None):
    row = {"name": "Collect", "form_id": "main", "source": "composed",
           "citations": [], "translations": list(translations)}
    if rights:
        row["unavailable_translations"] = [{"lang": "en", "state": "rights-restricted"}]
    row["coverage"] = coverage.unit(row, target_id=target, occurrence_id=occurrence,
        cycle=cycle, cycle_family="cycles" if cycle != "all" else None,
        witnesses={"edition.a": {"source_id": "edition.a", "artifact_id": "artifact.a", "label": "Witness A"},
                   "artifact.a": {"source_id": "edition.a", "artifact_id": "artifact.a", "label": "Witness A"}})
    return row


def translation(source="edition.a", text="Public study fixture", rights="public-domain"):
    return {"lang": "en", "source_id": source, "text": text, "rights": rights}


def structure(propers):
    units = [unit for row in propers for unit in coverage.proper_units({"propers": [row]})]
    mass = {"key": "fixture", "kind": "contract", "propers": propers,
            "coverage": coverage.summarize(units, "mass")}
    return {"calendar": "fixture-edition", "masses": [mass], "translations": [],
            "coverage": coverage.summarize(units, "calendar")}


class ReaderCoverageTests(unittest.TestCase):
    def test_report_parity_deduplicates_targets_occurrences_and_witness_aliases(self):
        rows = [proper("shared", "one", [translation(), translation("artifact.a")]),
                proper("shared", "two", [translation()]),
                proper("other", "three", [translation("", rights="project-created")]),
                proper("missing", "four", rights=True)]
        scripture = coverage.unit({"source": "scripture"}, target_id="reading", occurrence_id="five")
        units = [row["coverage"] for row in rows] + [scripture, rows[0]["coverage"]]
        self.assertEqual(node(op="summary", units=units), coverage.summarize(units, "selection"))
        data = structure(rows)
        labels = node(op="labels", structure=data)
        self.assertIn("0 of 3 represented texts available", labels["languages"][0])
        self.assertIn("2 of 3 represented texts available", labels["languages"][1])
        self.assertEqual({row["id"] for row in labels["witnesses"]}, {"edition.a", "project-created"})
        self.assertNotIn("as printed", json.dumps(labels))

    def test_partial_explicit_witness_keeps_other_units_absent(self):
        data = structure([proper("one", "one", [translation()]),
                          proper("two", "two", [translation("edition.b", "Other witness")])])
        result = node(op="adapt", structure=data, witness="edition.a")
        selected = [event["selected"] for event in result["result"]["events"]]
        self.assertEqual(selected[0]["text"], "Public study fixture")
        self.assertIsNone(selected[1]["text"])
        self.assertEqual(selected[1]["reason"], "absent-in-witness")
        rendered = node(op="oration", proper=data["masses"][0]["propers"][1], witness="edition.a")
        self.assertIsNone(rendered["text"])
        self.assertEqual(rendered["reason"], "absent-in-witness")

    def test_project_witness_can_be_selected_without_a_source_id(self):
        row = proper("one", "one", [translation("", "Project study words", "project-created"), translation()])
        result = node(op="adapt", structure=structure([row]), witness="project-created")
        self.assertEqual(result["result"]["events"][0]["selected"]["text"], "Project study words")
        self.assertEqual(node(op="oration", proper=row, witness="project-created")["text"], "Project study words")

    def test_all_souls_witness_gap_does_not_deny_another_held_english_body(self):
        data = json.loads((ROOT / "src/web/data/structure/propers/roman-1962.json").read_text())
        mass = next(row for row in data["masses"]
                    if row["key"] == "commemoratione-omnium-fidelium-defunctorum")
        caswall = "edition.edward-caswall.lyra-catholica.london-1849"
        cummiskey = "edition.eugene-cummiskey.roman-missal-english-laity.philadelphia-1861"
        prayers = [row for row in mass["propers"] if row["form_id"] == "first"
                   and row["name"] in {"Collect", "Secret", "Postcommunion"}]
        self.assertEqual(len(prayers), 3)
        for row in prayers:
            with self.subTest(proper=row["name"]):
                self.assertEqual(row["text_status"]["state"], "unavailable")
                missing = node(op="oration", proper=row, witness=caswall)
                self.assertIsNone(missing["text"])
                self.assertEqual(missing["reason"], "absent-in-witness")
                held = node(op="oration", proper=row, witness=cummiskey)
                self.assertTrue(held["text"])
                self.assertFalse(held["missing"])
                self.assertEqual(held["lang"], "en")

    def test_aliases_collapse_only_identical_bodies(self):
        row = proper("one", "one", [translation(), translation("artifact.a")])
        result = node(op="adapt", structure=structure([row]))
        self.assertEqual(result["result"]["events"][0]["selected"]["availability"], "held")
        self.assertEqual(node(op="oration", proper=row)["text"], "Public study fixture")
        row["translations"][1]["text"] = "Conflicting public fixture"
        result = node(op="adapt", structure=structure([row]))
        self.assertEqual(result["result"]["events"][0]["selected"]["reason"], "conflicting-witness")
        self.assertEqual(node(op="oration", proper=row)["reason"], "conflicting-witness")

    def test_restricted_absence_is_not_relabelled_as_witness_gap(self):
        row = proper("one", "one", rights=True)
        self.assertEqual(node(op="oration", proper=row, witness="edition.a")["reason"], "rights-restricted")
        data = structure([proper("other", "other", [translation()]), row])
        result = node(op="adapt", structure=data, witness="edition.a")
        self.assertEqual(result["result"]["events"][1]["selected"]["reason"], "rights-restricted")

    def test_published_body_survives_a_distinct_restricted_alternative(self):
        row = proper("one", "one", [translation()], rights=True)
        # Private absence evidence must neither become a public witness choice
        # nor escape through the selected semantic result.
        row["unavailable_translations"][0].update({
            "source_id": "protected-private-witness", "note": "private permission evidence"})
        data = structure([row])
        choices = node(op="choices", structure=data)
        self.assertEqual(choices["propers"]["deterministic"], "edition.a")
        self.assertNotIn("protected-private-witness", json.dumps(choices))
        for witness in (None, "edition.a"):
            selected = node(op="adapt", structure=data, witness=witness)["result"]["events"][0]["selected"]
            rendered = node(op="oration", proper=row, witness=witness)
            self.assertEqual(selected["text"], rendered["text"])
            self.assertEqual(selected["availability"], "held")
            self.assertEqual(selected["rights"], "public-domain")
            self.assertNotIn("private", json.dumps(selected))
        with self.assertRaisesRegex(AssertionError, "selected no appointed text"):
            node(op="adapt", structure=data, witness="protected-private-witness")
        rendered = node(op="oration", proper=row, witness="protected-private-witness")
        self.assertIsNone(rendered["text"])
        self.assertEqual(rendered["reason"], "absent-in-witness")

    def test_selected_cycle_uses_only_its_report_units(self):
        cycles = {key: proper(key, key, [translation()], cycle=key) for key in ["A", "B", "C"]}
        parent = {"name": "Collect", "source": "composed", "form_id": "main", "cycles": cycles}
        result = node(op="adapt", structure=structure([parent]), cycle="B")
        self.assertEqual([row["occurrence_id"] for row in result["units"]], ["B"])
        self.assertEqual(result["report"], coverage.summarize([cycles["B"]["coverage"]], "selection"))

    def test_selected_ordinary_uses_event_identity_and_same_report(self):
        rows = [proper("one", "one", [translation()]), proper("two", "two")]
        for index, row in enumerate(rows):
            row["key"] = str(index)
            row["coverage"]["component"] = "ordinary-body"
        actual = node(op="ordinary", ordinary={"sections": [{"elements": rows}]},
                      result={"events": [{"kind": "ordinary-element", "id": "ordinary-element/0"}]})
        self.assertEqual(actual, coverage.summarize([rows[0]["coverage"]], "selection"))

    def test_both_entrances_offer_union_of_disjoint_partial_witnesses(self):
        data = structure([proper("one", "one", [translation()]),
                          proper("two", "two", [translation("", "Project", "project-created")])])
        result = node(op="choices", structure=data)
        for entrance in ("day", "propers"):
            self.assertEqual({row["id"] for row in result[entrance]["choices"]},
                             {"edition.a", "project-created"})
            self.assertTrue(all("1 of 2 uses" in row["label"] for row in result[entrance]["choices"]))

    def test_mixed_scripture_and_available_exact_witness_do_not_inflate_counts(self):
        first = translation()
        first["coverage_relationship"] = "exact-target"
        other = translation("edition.b")
        other["coverage_relationship"] = "historical-antecedent"
        unit = proper("mixed", "mixed", [first, other])["coverage"]
        unit["scripture_component"] = {"target_id": "mixed-scripture", "occurrence_id": "mixed-scripture",
            "relationship": "bible-reconstruction", "availability": "unresolved", "publication_basis": "unresolved"}
        actual = node(op="summary", units=[unit])
        self.assertEqual(actual, coverage.summarize([unit], "selection"))
        english = actual["languages"][1]
        self.assertEqual(english["exact_target"], 1)
        self.assertEqual(english["mixed_occurrences"], 1)
        self.assertEqual(actual["counts"]["occurrences"], 1)

    def test_generated_corpus_reports_match_browser_aggregation(self):
        data_root = Path(os.environ.get("TRIPTYCH_COVERAGE_DATA", ROOT / "src/web/data"))
        for family in ("propers", "ordinary"):
            for calendar in ("roman-1962", "postconciliar", "roman-pre-1955"):
                with self.subTest(family=family, calendar=calendar):
                    data = json.loads((data_root / "structure" / family / (calendar + ".json")).read_text())
                    self.assertEqual(data["coverage"]["schema"], coverage.SCHEMA)
                    units = ([unit for mass in data["masses"] for unit in coverage.proper_units(mass)]
                             if family == "propers" else
                             [element["coverage"] for section in data["sections"] for element in section["elements"]])
                    expected = coverage.summarize(units, "selection")
                    self.assertEqual(node(op="summary", units=units), expected)
                    published = {key: value for key, value in data["coverage"].items()
                                 if key != "expected_inventory"}
                    published["scope"] = "selection"
                    self.assertEqual(published, expected)

    def test_real_easter_sequence_aliases_leave_one_readable_witness(self):
        data_root = Path(os.environ.get("TRIPTYCH_COVERAGE_DATA", ROOT / "src/web/data"))
        data = json.loads((data_root / "structure/propers/roman-1962.json").read_text())
        data["masses"] = [mass for mass in data["masses"] if mass["key"] == "easter-sunday"]
        data["masses"][0]["kind"] = "contract"
        result = node(op="adapt", structure=data)
        sequence = next(event["selected"] for event in result["result"]["events"]
                        if event.get("editionSlotLabel") == "Sequence")
        self.assertEqual(sequence["availability"], "held")
        self.assertTrue(sequence["text"])

    def test_real_mixed_only_proper_accepts_its_body_witness(self):
        data_root = Path(os.environ.get("TRIPTYCH_COVERAGE_DATA", ROOT / "src/web/data"))
        data = json.loads((data_root / "structure/propers/roman-1962.json").read_text())
        mass = next(mass for mass in data["masses"] if mass["key"] == "pentecost-19")
        mixed = next(row for row in mass["propers"] if row["name"] == "Introit")
        self.assertIn("scripture_component", mixed["coverage"])
        english = next(row for row in mixed["coverage"]["languages"] if row["lang"] == "en")
        witness = english["witnesses"][0]["id"]
        data["masses"] = [{"key": mass["key"], "kind": "contract", "propers": [mixed]}]
        result = node(op="adapt", structure=data, witness=witness)
        self.assertEqual(result["result"]["events"][0]["selected"]["kind"], "scripture")
        self.assertTrue(node(op="oration", proper=mixed, witness=witness)["text"])
        self.assertEqual(result["report"]["languages"][1]["available"], 1)
        self.assertEqual(result["report"]["languages"][1]["scripture_occurrences"], 1)

    def test_missing_report_and_zero_units_make_no_completion_claim(self):
        labels = node(op="labels", structure={"translations": [{"lang": "en"}]})
        self.assertTrue(all("coverage not assessed" in row for row in labels["languages"]))
        empty = {"coverage": coverage.summarize([], "calendar")}
        self.assertIn("not been assessed", node(op="labels", structure=empty)["notice"])


if __name__ == "__main__":
    unittest.main()
