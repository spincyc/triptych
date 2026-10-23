"""Bounded OLM 1981 nn. 175, 197, 237, 251; appointment facts, no bodies.

--projection emits fresh canonical appointments for the paired Node test.
No generated repository data, actual-use attestation UI, or global writes.
"""
from __future__ import annotations

import argparse
import copy
from importlib.machinery import SourceFileLoader
from importlib.util import module_from_spec, spec_from_loader
import json
from pathlib import Path
import subprocess
import sys
import unittest

import yaml

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))
import _calendars as C

KEYS = ("advent-1-monday", "advent-december-21", "lent-3-monday", "lent-5-monday")
ADVENT_FACT = "advent-1-sunday-isaiah-2-1-5-actually-read"
LENT_FACT = "lent-5-sunday-john-8-1-11-actually-read"


def tool(name):
    loader = SourceFileLoader("_phase2_ferial_" + name.replace("-", "_"), str(ROOT / "tools" / name))
    spec = spec_from_loader(loader.name, loader)
    module = module_from_spec(spec)
    sys.modules[loader.name] = module
    loader.exec_module(module)
    return module


def document():
    return yaml.safe_load((ROOT / "src/sources/calendars/postconciliar/propers.yaml").read_text())


def payload(doc, mass):
    appointed, errors = C.resolve_propers(doc, mass, appointments=True)
    assert not errors, errors
    public = copy.deepcopy(mass)
    public["proper_source_paths"] = C.public_proper_source_paths(doc, mass)
    return {"mass": public, "appointed": [
        {"form": form, "form_id": "main", "proper": proper, "taken_from": taken_from}
        for form, proper, taken_from in appointed]}


def projection(doc):
    masses = C.mass_index(doc)
    projected = []
    for key in KEYS:
        one = payload(doc, masses[key])
        mass = one["mass"]
        mass["propers"] = [p["proper"] for p in one["appointed"]]
        projected.append(mass)
    return {"calendar": "postconciliar", "masses": projected}


class PhaseTwoFerialFidelityTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.doc = document()
        cls.masses = C.mass_index(cls.doc)
        cls.today = tool("mass-today")
        cls.citations = tool("citations")
        cls.propers = tool("mass-propers")

    def rows(self, key, role):
        return [p for p in self.masses[key]["propers"] if p["name"] == role]

    def prepare(self, key, cycle="C", choices=None, facts=None):
        args = argparse.Namespace(lang="en", bible=None, witness=None)
        mass = self.today.propers_of("postconciliar", key, args,
                                    {"sunday": cycle, "weekday": "II"},
                                    payload=payload(self.doc, self.masses[key]))
        mass.update(key=key)
        context = {"date": "2028-04-03", "season": self.masses[key]["season"],
                   "condition_facts": facts or {}}
        requested = ["proper-choice/postconciliar/" + key + "/main/" + k + "=" + v
                     for k, v in (choices or {}).items()]
        rows = [{"proper": p, "sourceIndex": i}
                for p, i in zip(mass["propers"], mass["_proper_source_indices"])]
        return self.today.mass_events(None, rows, None, context,
                                     self.today.proper_appointment_context_for(
                                         "postconciliar", mass, context, requested))

    @staticmethod
    def admitted(result, role):
        rows = []
        for event in result["events"]:
            if event["kind"] == "proper":
                rows.append(event)
            elif event["kind"] == "proper_choice":
                selected = (event.get("selection") or {}).get("option")
                rows.extend(row for option in event["options"] if option["id"] == selected
                            for row in option["rows"])
        return [row["proper"] for row in rows if row["proper"]["name"] == role]

    def test_exact_flat_citations_and_optional_subverses(self):
        for key, role, expected in [
            ("advent-1-monday", "First Reading", ["Isaiah 2:1-5", "Isaiah 4:2-6"]),
            ("advent-december-21", "First Reading", ["Song of Songs 2:8-14", "Zephaniah 3:14-18a"]),
            ("lent-3-monday", "Responsorial Psalm", ["Psalm 42:2, 3", "Psalm 43:3, 4"]),
            ("lent-5-monday", "Gospel", ["John 8:1-11", "John 8:12-20"]),
        ]:
            self.assertEqual([p["verses"] for p in self.rows(key, role)[:len(expected)]],
                             [[self.citations.parse_citation(ref)] for ref in expected])
        psalms = self.rows("advent-1-monday", "Responsorial Psalm")
        self.assertEqual([p["psalm_numbering"] for p in psalms], ["vulgate", "vulgate"])
        refs = ["Psalm 121:1-2, 3-4a, 8-9", "Psalm 121:1-2, 3-4a, 4b-5, 6-7, 8-9"]
        for proper, ref in zip(psalms, refs):
            self.assertEqual(proper["verses"], [self.citations.parse_citation(ref)])
            public = self.propers.citation_structure(proper["verses"][0], "vulgate",
                                                    self.propers.book_tokens())
            self.assertIsNone(public["unresolved"])
            self.assertEqual({r["chapter"] for r in public["loci"]["hebrew"]}, {122})
        ranges = psalms[1]["verses"][0]["ranges"]
        self.assertEqual(ranges[1]["end"], {"chapter": 121, "verse": 4, "part": "a"})
        self.assertEqual(ranges[2]["begin"], {"chapter": 121, "verse": 4, "part": "b"})
        self.assertEqual(ranges[2]["end"], {"chapter": 121, "verse": 5})
        self.assertEqual(ranges[3], {"begin": {"chapter": 121, "verse": 6},
                                     "end": {"chapter": 121, "verse": 7}})

    def test_source_owners_conserve_occurrences_without_authored_derived_guards(self):
        counts = {"advent-1-monday": 2, "lent-3-monday": 1, "lent-5-monday": 1}
        for key in KEYS:
            mass = self.masses[key]
            relations = C.public_proper_source_paths(self.doc, mass)
            self.assertEqual(len(relations), counts.get(key, 0))
            self.assertEqual(C.ordinary_disposition_source_problems(key, "", mass["propers"]), [])
            for row in mass["propers"]:
                for derived in ("appointment_identity", "source_path_relation", "source_edition"):
                    self.assertNotIn(derived, row)
            for relation in relations:
                self.assertEqual(relation["source_edition"], "postconciliar")
                for path in relation["paths"]:
                    expected = (5 if key == "lent-3-monday" and path["id"] == "ferial"
                                else 4 if key in ("lent-3-monday", "lent-5-monday") else 1)
                    self.assertEqual(len(path["members"]), expected)
                    if key in ("lent-3-monday", "lent-5-monday"):
                        self.assertEqual({m["appointment"]["proper"].replace(" (shorter form)", "")
                                          for m in path["members"]},
                                         {"First Reading", "Responsorial Psalm", "Verse Before the Gospel", "Gospel"})
                    self.assertEqual(path["members"][0]["material_cycle"], {"family": None, "cycle": "all"})
                    self.assertEqual(path["members"][0]["appointment"]["mass"], key)

    def test_lent_ab_refuse_replacement_even_with_actual_use_true(self):
        for cycle in "AB":
            for facts in ({}, {LENT_FACT: None}, {LENT_FACT: False}, {LENT_FACT: True}):
                with self.subTest(cycle=cycle, facts=facts):
                    result = self.prepare("lent-5-monday", cycle,
                                          {"lent-5-monday-reading-course": "john-8-1-11-ab-longer"}, facts)
                    self.assertEqual(self.admitted(result, "Gospel")[0]["verses"][0]["ref"], "John 8:1-11")
                    with self.assertRaises(self.today.Refused):
                        self.prepare("lent-5-monday", cycle,
                                     {"lent-5-monday-reading-course": "john-8-12-20-c-longer"}, facts)
                    with self.assertRaises(self.today.Refused):
                        self.prepare("lent-5-monday", cycle, {"gospel": "john-8-12-20"}, facts)

    def test_lent_c_principal_is_unrestricted_but_optional_requires_actual_true(self):
        for facts in ({}, {LENT_FACT: None}, {LENT_FACT: False}, {LENT_FACT: True}):
            result = self.prepare("lent-5-monday", facts=facts)
            self.assertEqual(result["source_path_selections"]["main/lent-5-monday-reading-course"],
                             {"state": "required", "option": None})
            self.assertEqual(self.admitted(result, "Gospel"), [])
            for daniel in ("longer", "shorter"):
                principal = self.prepare("lent-5-monday",
                    choices={"lent-5-monday-reading-course": "john-8-1-11-c-" + daniel}, facts=facts)
                self.assertEqual([p["verses"][0]["ref"] for p in self.admitted(principal, "Gospel")],
                                 ["John 8:1-11"])
                role = "First Reading" if daniel == "longer" else "First Reading (shorter form)"
                self.assertEqual(len(self.admitted(principal, role)), 1)
                alternate = {"lent-5-monday-reading-course": "john-8-12-20-c-" + daniel}
                if facts.get(LENT_FACT) is True:
                    selected = self.prepare("lent-5-monday", choices=alternate, facts=facts)
                    self.assertEqual([p["verses"][0]["ref"] for p in self.admitted(selected, "Gospel")],
                                     ["John 8:12-20"])
                    self.assertEqual(len(self.admitted(selected, role)), 1)
                else:
                    with self.assertRaises(self.today.Refused):
                        self.prepare("lent-5-monday", choices=alternate, facts=facts)
            with self.assertRaises(self.today.Refused):
                self.prepare("lent-5-monday", choices={"gospel": "john-8-12-20"}, facts=facts)
        for value in ("true", "false", 1, 0, {}, []):
            with self.assertRaises(self.today.Refused):
                self.prepare("lent-5-monday", facts={LENT_FACT: value})

    def test_old_exclusive_calendar_fails_the_repaired_admission_oracles(self):
        old = copy.deepcopy(self.doc)
        relation = C.mass_index(old)["lent-5-monday"]["proper_source_paths"][0]
        for path in relation["paths"]:
            if path["id"].startswith("john-8-1-11-c-"):
                path["when"] = {"fact": LENT_FACT, "is": False}
            elif path["id"].startswith("john-8-12-20-c-"):
                path["standing"] = "principal"
        # The actual former source semantics, not an altered runtime or fixture.
        courses = __import__("tools.tests.test_postconciliar_lenten_ferial_courses", fromlist=["projection"])
        old_case = type(self)()
        old_case.doc, old_case.masses, old_case.today = old, C.mass_index(old), self.today
        with self.assertRaises(self.today.Refused):
            old_case.test_lent_c_principal_is_unrestricted_but_optional_requires_actual_true()
        old_courses = courses.LentenFerialCourseTests()
        old_courses.masses, old_courses.citations = C.mass_index(old), self.citations
        with self.assertRaises(AssertionError):
            old_courses.test_monday_native_cross_product_and_shared_psalm_owners()
        for filename, projected in (
            ("test_postconciliar_phase2_ferial_fidelity.cjs", projection(old)),
            ("test_postconciliar_lenten_ferial_courses.cjs", courses.projection(old)),
        ):
            result = subprocess.run(["node", str(ROOT / "tools/tests" / filename)],
                                    input=json.dumps(projected), text=True, capture_output=True)
            self.assertNotEqual(result.returncode, 0, filename + " accepted the old exclusive calendar")
            self.assertIn("source-condition-unresolved" if "phase2" in filename else "564 !== 560",
                          result.stderr)

    def test_advent_optional_reading_requires_actual_use_and_year_a(self):
        for cycle in "ABC":
            for value in (None, False, True):
                with self.subTest(cycle=cycle, actual=value):
                    kwargs = dict(key="advent-1-monday", cycle=cycle,
                                  choices={"advent-first-reading": "isaiah-4"},
                                  facts={ADVENT_FACT: value})
                    if cycle == "A" and value is True:
                        selected = self.prepare(**kwargs)
                        self.assertEqual(self.admitted(selected, "First Reading")[0]["verses"][0]["ref"],
                                         "Isaiah 4:2-6")
                    else:
                        with self.assertRaises(self.today.Refused):
                            self.prepare(**kwargs)
        unknown = self.prepare("advent-1-monday", "A")
        self.assertEqual(unknown["source_path_selections"]["main/advent-first-reading"]["state"], "required")
        with self.assertRaises(self.today.Refused):
            self.prepare("advent-1-monday", "A", {"first-reading": "isaiah-4"})

    def test_advent_reading_and_entire_parenthesis_are_independent_choices(self):
        for reading in ("isaiah-2", "isaiah-4"):
            for psalm in ("without-parenthesized-block", "with-parenthesized-block"):
                result = self.prepare("advent-1-monday", "A",
                                      {"advent-first-reading": reading, "advent-psalm-strophes": psalm},
                                      {ADVENT_FACT: True})
                self.assertEqual(len(self.admitted(result, "First Reading")), 1)
                chosen = self.admitted(result, "Responsorial Psalm")
                self.assertEqual(len(chosen), 1)
                self.assertEqual(len(chosen[0]["verses"][0]["ranges"]), 5 if psalm.startswith("with-") else 3)
        for cycle in "ABC":
            result = self.prepare("advent-1-monday", cycle,
                                  {"advent-first-reading": "isaiah-2",
                                   "advent-psalm-strophes": "with-parenthesized-block"})
            self.assertEqual(len(self.admitted(result, "Responsorial Psalm")), 1)
        relation = self.masses["advent-1-monday"]["proper_source_paths"][1]
        self.assertEqual(len(relation["paths"]), 2)
        self.assertTrue(all(set(p["choices"]) == {"psalm-strophes"} and "when" not in p
                            for p in relation["paths"]))

    def test_december_alternative_is_cycle_independent_without_default(self):
        for cycle in "ABC":
            for option, ref in (("song-of-songs", "Song of Songs 2:8-14"),
                                ("zephaniah", "Zephaniah 3:14-18a")):
                result = self.prepare("advent-december-21", cycle, {"first-reading": option})
                self.assertEqual(self.admitted(result, "First Reading")[0]["verses"][0]["ref"], ref)
            self.assertEqual(self.admitted(self.prepare("advent-december-21", cycle), "First Reading"), [])

    def test_shared_browser_admission_from_fresh_projection(self):
        result = subprocess.run(["node", str(ROOT / "tools/tests/test_postconciliar_phase2_ferial_fidelity.cjs")],
                                input=json.dumps(projection(self.doc)), text=True, capture_output=True)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("phase2 ferial fidelity: 172 admission executions", result.stdout)

    def test_displaced_controls_use_native_calendar_rank_not_cycle_guess(self):
        days = tool("calendar-days")
        rubrics = tool("calendar-rubrics")
        calendar_root = ROOT / "src/sources/calendars"
        index = days.load_calendar(calendar_root, "postconciliar")
        built = days.build_years(index, list(range(2025, 2030)))
        days.with_fixed(index, list(range(2025, 2029)))
        years = {y: days.year_document(index, y, built) for y in (2025, 2026, 2028)}
        rb, problems, _ = rubrics.build(calendar_root, "postconciliar")
        self.assertEqual(problems, [])
        controls = [("2026-11-30", "advent-1-monday", False),
                    ("2028-03-20", "lent-3-monday", False),
                    ("2025-12-21", "advent-december-21", False),
                    ("2025-12-01", "advent-1-monday", True),
                    ("2026-03-09", "lent-3-monday", True),
                    ("2026-12-21", "advent-december-21", True),
                    ("2028-04-03", "lent-5-monday", True)]
        result = rubrics.run_model({"cases": [
            {"id": date, "date": date, "year": years[int(date[:4])], "rubrics": rb[0]}
            for date, _, _ in controls]})
        self.assertEqual(len(result["results"]), len(controls))
        for control, resolved in zip(controls, result["results"]):
            date, key, expected = control
            with self.subTest(date=date):
                self.assertEqual(resolved["id"], date)
                self.assertTrue(resolved["ok"], resolved)
                said = {p["key"] for option in resolved["result"]["options"] for p in option["readable"]
                        if p["state"] == "said"}
                self.assertEqual(key in said, expected)


if __name__ == "__main__":
    if sys.argv[1:] == ["--projection"]:
        print(json.dumps(projection(document())))
    else:
        unittest.main()
