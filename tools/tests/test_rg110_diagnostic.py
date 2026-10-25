#!/usr/bin/python3
"""Do not publish ordinary-commemoration results for an unapplied RG110 pair."""
import copy
from importlib.machinery import SourceFileLoader
from importlib.util import module_from_spec, spec_from_loader
import json
import os
from pathlib import Path
import subprocess
import sys
import unittest

import yaml

ROOT = Path(os.environ.get("TRIPTYCH_RG110_TEST_REPOSITORY", Path(__file__).resolve().parents[2]))
SOURCE = Path(os.environ.get("TRIPTYCH_RG110_TEST_SOURCE", ROOT / "src/sources/calendars/roman-1962/rubrics.yaml"))
MODEL = Path(os.environ.get("TRIPTYCH_RG110_TEST_MODEL", ROOT / "src/web/browser/liturgy/assembly-model.js"))
TOOL = Path(os.environ.get("TRIPTYCH_RG110_TEST_TOOL", ROOT / "tools/calendar-rubrics"))
sys.path.insert(0, str(ROOT / "scripts"))
loader = SourceFileLoader("_rg110_calendar_rubrics", str(TOOL))
spec = spec_from_loader(loader.name, loader)
tool = module_from_spec(spec)
loader.exec_module(tool)

HARNESS = """
const model = require(process.argv[1]);
let raw = '';
process.stdin.on('data', one => raw += one);
process.stdin.on('end', () => {
  const results = JSON.parse(raw).map(one => {
    try { return { id: one.id, result: model.derive(one) }; }
    catch (error) { return { id: one.id, error: String(error) }; }
  });
  process.stdout.write(JSON.stringify(results));
});
"""


def run_model(cases):
    result = subprocess.run(["node", "-e", HARNESS, str(MODEL.resolve())],
                            input=json.dumps(cases), capture_output=True, text=True, check=True)
    return {one["id"]: one for one in json.loads(result.stdout)}


class Rg110Diagnostic(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.source = yaml.safe_load(SOURCE.read_text())
        # Exercise the retained refusal contract independently of whether the
        # installed source has since enabled its bounded execution path.
        rule = cls.source["commemoration"]["inseparable"]
        if rule.get("applied") is True:
            pairs = rule.pop("pairs")
            rule.pop("execution")
            rule["applied"] = False
            rule["unapplied"] = {
                "scope": "oration-owner", "what": "unapplied inseparable fixture",
                "why": "this fixture does not implement the source-identified RG 110 group",
                "pairs": pairs,
            }
        cls.masses = tool.load_masses(ROOT / "src/sources/calendars", "roman-1962")
        cls.rubrics = json.loads((ROOT / "src/web/data/structure/rubrics/roman-1962.json").read_text())
        cls.rubrics["commemoration"] = copy.deepcopy(cls.source["commemoration"])
        cls.dates = ["2027-02-22", "2028-02-22", "2060-02-22", "2027-01-25", "2026-06-30",
                     "2026-02-22", "2026-01-25", "2030-06-30", "2026-06-29", "2027-02-23"]
        cls.inputs = {}
        for date in cls.dates:
            cls.inputs[date] = cls.case(date)
        cls.results = run_model(list(cls.inputs.values()))

    @classmethod
    def case(cls, date, identifier=None):
        year = json.loads((ROOT / f"src/web/data/structure/calendar/roman-1962/{date[:4]}.json").read_text())
        return {"id": identifier or date, "date": date, "year": year, "rubrics": copy.deepcopy(cls.rubrics)}

    def branch(self, date):
        row = self.results[date]
        self.assertNotIn("error", row)
        branch, = row["result"]["options"]
        return branch

    def assert_refused(self, date):
        branch = self.branch(date)
        self.assertFalse(branch["settled"])
        self.assertIsNone(branch["winner"])
        self.assertEqual(branch["losers"], [])
        self.assertFalse(branch["choiceRequired"])
        self.assertIsNone(branch["choice"])
        self.assertEqual(branch["orations"], {"low_mass": [], "sung_non_conventual": []})
        self.assertEqual(branch["remarks"], [])
        reason, = branch["unsettled"]
        self.assertEqual(reason["scope"], "oration-owner")
        self.assertIn("RG 110", reason["locus"])
        self.assertIn("does not implement", reason["why"])
        self.assertNotIn("pairs", reason)
        self.assertNotIn("unapplied", reason)
        self.assertEqual({row["id"] for row in branch["readable"]},
                         {row["id"] for row in branch["candidates"] if row.get("key")})
        self.assertTrue(all(row["state"] == "unresolved" for row in branch["readable"]))
        return branch

    def test_chair_in_lent_cannot_drop_paul_as_surplus(self):
        self.assert_refused("2027-02-22")

    def test_chair_in_septuagesima_cannot_give_paul_a_second_conclusion_or_drop_him_sung(self):
        self.assert_refused("2028-02-22")

    def test_chair_commemorated_on_a_second_class_sunday_requires_the_group_too(self):
        baseline = copy.deepcopy(self.inputs["2060-02-22"])
        del baseline["rubrics"]["commemoration"]["inseparable"]["unapplied"]
        old = run_model([baseline])[baseline["id"]]["result"]["options"][0]
        self.assertEqual(old["winner"]["nature"], "sunday")
        self.assertTrue(any(one["id"] == "cathedrae-s-petri-apostoli" and
                            one["disposition"] == "commemorated" for one in old["losers"]))
        self.assert_refused("2060-02-22")

    def test_conversion_of_paul_requires_the_reverse_peter_group(self):
        self.assert_refused("2027-01-25")

    def test_june_paul_formulary_requires_its_own_peter_group(self):
        self.assert_refused("2026-06-30")

    def test_both_omitted_dates_are_not_newly_refused(self):
        dates = ["2026-02-22", "2026-01-25", "2030-06-30"]
        controls = [copy.deepcopy(self.inputs[date]) for date in dates]
        for case in controls:
            del case["rubrics"]["commemoration"]["inseparable"]["unapplied"]
        unchanged = run_model(controls)
        for date in dates:
            with self.subTest(date=date):
                branch = self.branch(date)
                self.assertTrue(branch["settled"])
                self.assertEqual(branch["unsettled"], [])
                self.assertEqual({one["disposition"] for one in branch["losers"]}, {"omitted"})
                self.assertEqual(self.results[date], unchanged[date])

    def test_joint_feast_and_neighbouring_unrelated_date_are_unchanged(self):
        dates = ["2026-06-29", "2027-02-23"]
        controls = [copy.deepcopy(self.inputs[date]) for date in dates]
        for case in controls:
            del case["rubrics"]["commemoration"]["inseparable"]["unapplied"]
        unchanged = run_model(controls)
        for date in dates:
            with self.subTest(date=date):
                self.assertTrue(self.branch(date)["settled"])
                self.assertEqual(self.branch(date)["unsettled"], [])
                self.assertEqual(self.results[date], unchanged[date])

    def test_companion_admitted_without_host_is_also_refused(self):
        case = self.case("2027-01-25", "orphan-companion")
        case["year"]["days"][case["date"]] = [row for row in case["year"]["days"][case["date"]]
                                                   if row["key"] != "conversione-s-pauli-apostoli"]
        got = run_model([case])[case["id"]]
        self.assertNotIn("error", got)
        branch = got["result"]["options"][0]
        self.assertFalse(branch["settled"])
        self.assertEqual(branch["orations"], {"low_mass": [], "sung_non_conventual": []})
        self.assertEqual(branch["unsettled"][0]["scope"], "oration-owner")

    def test_existing_source_refusal_is_preserved_without_a_provisional_rg110_claim(self):
        case = self.case("2027-02-22", "earlier-refusal")
        prior = {"what": "preexisting source limit", "why": "independent unresolved occurrence",
                 "scope": "occurrence", "when": {"candidate_key": "cathedrae-s-petri-apostoli"}}
        case["rubrics"]["unsettled"].append(prior)
        got = run_model([case])[case["id"]]["result"]["options"][0]
        self.assertFalse(got["settled"])
        self.assertIsNone(got["winner"])
        self.assertEqual([row["what"] for row in got["unsettled"]], [prior["what"]])
        self.assertEqual(got["losers"], [])

    def test_reader_requires_explicit_raw_selection_and_preserves_each_prayer_body(self):
        harness = r"""
const fs = require('fs');
const crypto = require('crypto');
const A = require(process.argv[1] + '/src/web/browser/liturgy/reader-state-adapters.js');
let raw = '';
process.stdin.on('data', one => raw += one);
process.stdin.on('end', () => {
  const derived = JSON.parse(raw);
  const structure = JSON.parse(fs.readFileSync(process.argv[1] + '/src/web/data/structure/propers/roman-1962.json'));
  const fixture = JSON.parse(fs.readFileSync(process.argv[1] + '/tools/tests/fixtures/liturgy-reader-state/v1/day-roman-1962-2026-08-02.json'));
  const request = fixture.requested;
  request.civilDate = derived.date;
  delete request.selectedReadableFormulary;
  let implicitError = null;
  try { A.adaptDay({request, derived, structure}); } catch (error) { implicitError = String(error); }
  const sha = text => crypto.createHash('sha256').update(text).digest('hex');
  const explicit = ['cathedrae-s-petri-apostoli', 'comm-s-pauli-apostoli'].map(key => {
    const selected = Object.assign({}, request, {selectedReadableFormulary: {id: key}});
    const result = A.adaptDay({request: selected, derived, structure});
    const target = structure.masses.find(mass => mass.key === key);
    const held = target.propers.filter(one => ['Collect', 'Secret', 'Postcommunion'].includes(one.name));
    const bodies = result.events.filter(one => one.kind === 'proper' && held.some(p => p.name === one.editionSlotLabel));
    return {key, resolved: result.resolved, settled: result.calendarResult.settled,
      exactBodies: bodies.length === held.length && bodies.every(event =>
        sha(event.selected.text) === sha(held.find(one => one.name === event.editionSlotLabel).text)),
      ownEventsOnly: result.events.every(event => event.kind !== 'proper' || event.id.startsWith('proper/roman-1962/' + key + '/'))};
  });
  process.stdout.write(JSON.stringify({implicitError, explicit}));
});
"""
        result = subprocess.run(["node", "-e", harness, str(ROOT.resolve())],
                                input=json.dumps(self.results["2027-02-22"]["result"]),
                                capture_output=True, text=True, check=True)
        report = json.loads(result.stdout)
        self.assertIn("no deterministic or explicitly selected formulary", report["implicitError"] or "")
        for row in report["explicit"]:
            with self.subTest(key=row["key"]):
                self.assertFalse(row["settled"])
                self.assertEqual(row["resolved"]["standing"], "unresolved")
                self.assertTrue(row["exactBodies"])
                self.assertTrue(row["ownEventsOnly"])

    def test_source_pairs_validate_without_saint_name_inference(self):
        self.assertEqual(tool.check_inseparable(self.source, self.masses, "fixture"), [])
        pairs = self.source["commemoration"]["inseparable"]["unapplied"]["pairs"]
        self.assertEqual([(p["host"], p["companion"]) for p in pairs], [
            ("conversione-s-pauli-apostoli", "comm-s-petri-apostoli"),
            ("cathedrae-s-petri-apostoli", "comm-s-pauli-apostoli"),
            ("commemoratione-s-pauli-apostoli", "comm-s-petri-apostoli-2")])

    def test_malformed_unknown_repeated_or_noncommemoration_source_pairs_are_rejected(self):
        mutations = [
            lambda r: r.update(applied=True),
            lambda r: r.update(unapplied=None),
            lambda r: r["unapplied"].update(extra=True),
            lambda r: r["unapplied"].update(scope="unsupported"),
            lambda r: r["unapplied"].update(why=""),
            lambda r: r["unapplied"].update(pairs=[]),
            lambda r: r["unapplied"]["pairs"][0].update(extra=True),
            lambda r: r["unapplied"]["pairs"][0].update(host="unknown-source-key"),
            lambda r: r["unapplied"]["pairs"][0].update(companion="conversione-s-pauli-apostoli"),
            lambda r: r["unapplied"]["pairs"][1].update(companion="comm-s-petri-apostoli"),
            lambda r: r["unapplied"]["pairs"][0].update(companion="cathedrae-s-petri-apostoli"),
        ]
        for position, mutate in enumerate(mutations):
            with self.subTest(position=position):
                source = copy.deepcopy(self.source)
                mutate(source["commemoration"]["inseparable"])
                self.assertTrue(tool.check_inseparable(source, self.masses, "fixture"))

    def test_runtime_rejects_malformed_or_unknown_source_selectors(self):
        cases = []
        for identifier in ["unknown-key", "unknown-field", "duplicate", "wrong-scope", "null-limit", "false-limit"]:
            case = self.case("2027-02-22", identifier)
            limit = case["rubrics"]["commemoration"]["inseparable"]["unapplied"]
            if identifier == "unknown-key": limit["pairs"][0]["host"] = "not-a-key"
            if identifier == "unknown-field": limit["pairs"][0]["saint"] = "Peter"
            if identifier == "duplicate": limit["pairs"].append(copy.deepcopy(limit["pairs"][0]))
            if identifier == "wrong-scope": limit["scope"] = "unrecognised"
            if identifier == "null-limit": case["rubrics"]["commemoration"]["inseparable"]["unapplied"] = None
            if identifier == "false-limit": case["rubrics"]["commemoration"]["inseparable"]["unapplied"] = False
            cases.append(case)
        for identifier, result in run_model(cases).items():
            with self.subTest(identifier=identifier):
                self.assertTrue("error" in result, identifier + " must reject a malformed selector")
                self.assertIn("inseparable", result["error"])


if __name__ == "__main__":
    unittest.main()
