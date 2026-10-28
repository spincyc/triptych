"""The CLI transports original Day evidence to the shared usage projector."""
from __future__ import annotations

import argparse
import contextlib
import copy
import importlib.machinery
import importlib.util
import io
import json
import os
from pathlib import Path
import subprocess
import sys
import unittest
from unittest.mock import patch

ROOT = Path(os.environ.get("TRIPTYCH_REVIEW_ROOT", Path(__file__).resolve().parents[2]))
CORE = Path(os.environ.get("TRIPTYCH_USAGE_CORE", ROOT))
CLI = Path(os.environ.get("TRIPTYCH_USAGE_CLI", ROOT))
PRODUCER = Path(os.environ.get("TRIPTYCH_USAGE_PRODUCER", ROOT))
SOURCE_FILE = Path(os.environ.get("TRIPTYCH_USAGE_SOURCE", ROOT / "src/sources/calendars/roman-1962/propers.yaml"))
SEATING = Path(os.environ.get("TRIPTYCH_USAGE_SEATING", ROOT / "src/web/browser/liturgy/ordinary-seating.js"))
sys.path.insert(0, str(ROOT / "scripts"))
sys.path.insert(0, str(CORE / "scripts"))
import _calendars as C


def load_tool(name, base):
    loader = importlib.machinery.SourceFileLoader("_proper_usage_" + name.replace("-", "_"), str(base / "tools" / name))
    spec = importlib.util.spec_from_loader(loader.name, loader)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    loader.exec_module(module)
    for key, value in list(vars(module).items()):
        if isinstance(value, Path) and value.is_relative_to(base):
            setattr(module, key, ROOT / value.relative_to(base))
    module.ROOT = ROOT
    return module


TODAY = load_tool("mass-today", CLI)
MP = load_tool("mass-propers", PRODUCER)
TODAY.SEATING_MODEL = SEATING
CASES = {
    "advent-1": ("2026-11-29", ["2026-12-01", "2026-12-05"]),
    "advent-2": ("2026-12-06", ["2026-12-09", "2026-12-10", "2026-12-12"]),
    "advent-3": ("2026-12-13", ["2026-12-14", "2026-12-15", "2026-12-17"]),
    "advent-4": ("2026-12-20", ["2026-12-22", "2026-12-23"]),
}


def arguments(date, machine=True):
    return argparse.Namespace(date=date, calendar="roman-1962", expanded=True,
                              ordinary=False, ordinary_variant=None, territory=None,
                              mass=None, form=None, proper_choice=None, lang="en",
                              bible="douay-rheims", witness=None, json=machine,
                              format="json" if machine else "text", rubrics=False, why=False)


def without_fields(value, fields):
    if isinstance(value, dict):
        return {key: without_fields(one, fields) for key, one in value.items() if key not in fields}
    if isinstance(value, (list, tuple)):
        return type(value)(without_fields(one, fields) for one in value)
    return value


class ProperUsageBridgeTests(unittest.TestCase):
    maxDiff = 2000

    @classmethod
    def setUpClass(cls):
        cls.source = C.read_yaml(SOURCE_FILE)
        cls.payloads = {}
        cls.load_payloads([*CASES, "pentecost-2"])
        dates = [date for sunday, ferias in CASES.values() for date in [sunday, *ferias]] + ["2026-06-08"]
        harness = r"""
const fs=require('node:fs'),path=require('node:path'),root=process.argv[1];
const M=require(path.join(root,'src/web/browser/liturgy/assembly-model.js'));
const year=JSON.parse(fs.readFileSync(path.join(root,'src/web/data/structure/calendar/roman-1962/2026.json')));
const rubrics=JSON.parse(fs.readFileSync(path.join(root,'src/web/data/structure/rubrics/roman-1962.json')));
let raw='';process.stdin.on('data',x=>raw+=x);process.stdin.on('end',()=>
 process.stdout.write(JSON.stringify(Object.fromEntries(JSON.parse(raw).map(date=>[date,M.derive({date,year,rubrics})])))));
"""
        result = subprocess.run(["node", "-e", harness, str(ROOT)], input=json.dumps(dates), capture_output=True, text=True, check=True)
        cls.derived = json.loads(result.stdout)
        cls.load_payloads({row["key"] for day in cls.derived.values() for branch in day["options"] for row in branch["readable"]})
        cls.ordinary = TODAY.invoke("mass-ordinary", ["show", "--calendar", "roman-1962", "--lang", "en"])

    @classmethod
    def load_payloads(cls, keys):
        for key in keys:
            if key in cls.payloads:
                continue
            args = argparse.Namespace(root=str(ROOT / "src/sources/calendars"), calendar="roman-1962", mass=key,
                                      lang="en", witness=None, bible="douay-rheims", bible_root=str(ROOT / "src/sources/bibles"), form=None)
            with patch.object(MP, "load_calendar", return_value=cls.source):
                cls.payloads[key] = MP.run_show_one(args)

    def show(self, date="2026-12-01", *, machine=True, derive=None, framed=False, expanded=True):
        derived = derive if derive is not None else self.derived[date]
        args = arguments(date, machine)
        args.expanded = expanded
        def invoke(tool, argv):
            if tool == "calendar-rubrics":
                return {"days": [derived]}
            if tool == "mass-ordinary":
                return self.ordinary if framed else {"ordinary": [None]}
            raise AssertionError((tool, argv))
        with patch.object(TODAY, "invoke", side_effect=invoke), patch.object(TODAY, "invoke_propers", side_effect=lambda calendar, keys, args: {key: copy.deepcopy(self.payloads[key]) for key in keys}):
            payload = TODAY.run_show(args)
        day = payload["days"][0]
        mass = next(one for one in day["masses"] if one["key"] == day["selected_mass"])
        return payload, day, mass, args

    def resolution(self, mass, context=None):
        predicates = {"date": "2026-12-01", "season": "advent"}
        context = context if context is not None else TODAY.proper_appointment_context_for("roman-1962", mass, predicates)
        return TODAY.mass_events(None, [{"proper": row, "sourceIndex": index} for index, row in enumerate(mass["propers"])], None, predicates, context)

    def structure(self):
        all_masses = list(MP.masses_of(self.source))
        selected = [(kind, mass) for kind, mass in all_masses if mass["key"] in {*CASES, "pentecost-2"}]
        original_masses_of = MP.masses_of
        original_translation_overlay = MP.translation_overlay

        def complete_translation_overlay(*args, **kwargs):
            with patch.object(MP, "masses_of", original_masses_of):
                return original_translation_overlay(*args, **kwargs)

        # The overlay validates its Scripture targets against the real catalog.
        # Keep the complete citation catalog, then project only the five Masses.
        # The finite dated execution sources own none of these Masses.
        with patch.object(MP, "load_calendar", return_value=self.source), patch.object(MP, "translation_overlay", side_effect=complete_translation_overlay), patch.object(MP, "masses_of", side_effect=[all_masses, selected]), patch.object(MP._oration_execution, "load_sources", return_value={}), patch.object(MP._name_execution, "load_name_sources", return_value={}):
            return MP.calendar_structure(ROOT / "src/sources/calendars", "roman-1962", MP.book_tokens())

    def test_original_branch_and_readable_survive_privately_before_public_projection(self):
        derived = copy.deepcopy(self.derived["2026-12-01"])
        snapshot = copy.deepcopy(derived)
        payload, day, mass, _ = self.show(derive=derived)
        context = TODAY.proper_appointment_context_for("roman-1962", mass, {})
        self.assertIs(context["usageContext"]["branch"], derived["options"][0])
        self.assertIs(context["usageContext"]["readable"], derived["options"][0]["readable"][0])
        self.assertIn("rule", context["usageContext"]["branch"]["candidates"][0])
        self.assertIn("id", context["usageContext"]["readable"])
        self.assertNotIn("candidates", day["branches"][0])
        public = json.loads(json.dumps(payload))
        self.assertNotIn("usageContext", json.dumps(public))
        self.assertNotIn("_source_branch", json.dumps(public))
        self.assertEqual(derived, snapshot)
        self.assertEqual(public["days"][0]["masses"][0]["proper_appointment_usage"], "borrowed-feria")

    def test_existing_producer_transports_actual_usage_map_and_exact_appointments(self):
        structure = self.structure()
        self.assertEqual(structure[C.PROPER_APPOINTMENT_FACTS], self.source[C.PROPER_APPOINTMENT_FACTS])
        self.assertEqual({mass["key"] for mass in structure["masses"]}, {*CASES, "pentecost-2"})
        for mass in structure["masses"]:
            guarded = [row for row in mass["propers"] if row.get("ordinary_disposition", {}).get("when", {}).get("fact") == "roman-1962-advent-sunday-alleluia-use"]
            self.assertEqual([row["name"] for row in guarded], ["Alleluia"] if mass["key"] in CASES else [])
            for row in guarded:
                self.assertEqual(row["appointment_identity"], {"mass": mass["key"], "form_id": "main", "proper": "Alleluia", "occurrence": 1})

    def test_actual_four_sundays_and_ten_ferias_change_only_the_held_alleluia(self):
        for key, (sunday, ferias) in CASES.items():
            for date in [sunday, *ferias]:
                with self.subTest(date=date, key=key):
                    _, _, mass, _ = self.show(date)
                    borrowed = date != sunday
                    self.assertEqual(mass["proper_appointment_usage"], "borrowed-feria" if borrowed else "own-sunday")
                    result = self.resolution(mass)
                    shown = [(event["sourceIndex"], event["proper"]) for event in result["events"] if event["kind"] == "proper"]
                    expected = [(index, row) for index, row in enumerate(mass["propers"]) if not (borrowed and row["name"] == "Alleluia")]
                    self.assertEqual(without_fields(shown, {"ordinary_disposition"}), without_fields(expected, {"ordinary_disposition"}))
                    self.assertTrue(any(row["name"] == "Gradual" for _, row in shown))
                    self.assertEqual(result["proper_appointment_unresolved"], [])

    def test_text_and_machine_share_exact_event_bodies_order_and_usage_framed_and_unframed(self):
        bridge = TODAY.mass_events
        for date in ("2026-11-29", "2026-12-01"):
            for framed in (False, True):
                calls = []
                def record(*args, **kwargs):
                    result = bridge(*args, **kwargs)
                    calls.append(copy.deepcopy(result))
                    return result
                with self.subTest(date=date, framed=framed), patch.object(TODAY, "mass_events", side_effect=record):
                    machine, _, mass, _ = self.show(date, framed=framed)
                    machine_events = calls[-1]
                    text, _, _, args = self.show(date, machine=False, framed=framed)
                    with contextlib.redirect_stdout(io.StringIO()) as output:
                        self.assertEqual(TODAY.render(text, args), 0)
                    # Text also resolves separately displayed commemorations.
                    # Compare the selected Mass, retaining every word while
                    # excluding its existing language/absence projections.
                    text_events = next(result for result in reversed(calls) if "proper_appointment_usage" in result)
                    projections = {"language_selection", "untranslated", "unavailable_translations"}
                    self.assertEqual(without_fields(text_events, projections), without_fields(machine_events, projections))
                    self.assertEqual(mass["proper_appointment_usage"], machine_events["proper_appointment_usage"])
                    self.assertIn("Gradual", output.getvalue())
                    self.assertTrue(machine["days"][0]["masses"][0]["expanded_events"])

    def test_yaml_serializes_only_the_public_mass_and_preserves_explicit_unknown(self):
        import yaml
        payload, _, mass, args = self.show()
        mass["proper_appointment_usage"] = None
        args.json = False
        args.format = "yaml"
        with contextlib.redirect_stdout(io.StringIO()) as output:
            self.assertEqual(TODAY.render(payload, args), 0)
        self.assertEqual(yaml.safe_load(output.getvalue()), json.loads(json.dumps(payload)))
        self.assertNotIn("usageContext", output.getvalue())

    def test_compact_machine_uses_one_existing_bridge_without_dropping_raw_propers(self):
        bridge = TODAY.mass_events
        for date in ("2026-11-29", "2026-12-01"):
            with self.subTest(date=date):
                _, _, expanded, _ = self.show(date)
                with patch.object(TODAY, "mass_events", wraps=bridge) as called:
                    _, _, compact, _ = self.show(date, expanded=False)
                self.assertEqual(called.call_count, 1)
                self.assertEqual(compact["propers"], expanded["propers"])
                self.assertNotIn("expanded_events", compact)
                for field in ("proper_appointment_usage", "proper_appointment_selections", "proper_appointment_unresolved", "proper_appointment_inactive"):
                    self.assertEqual(compact.get(field), expanded.get(field))
        with patch.object(TODAY, "mass_events", wraps=bridge) as called:
            _, _, control, _ = self.show("2026-06-08", expanded=False)
        self.assertEqual(called.call_count, 0)
        self.assertNotIn("proper_appointment_usage", control)

    def test_absent_original_evidence_is_explicit_unknown_and_not_restored_by_public_fields(self):
        _, _, original, _ = self.show()
        mass = dict(original)
        mass["proper_appointment_usage"] = "borrowed-feria"
        predicates = {"season": "advent", "usage": "borrowed-feria", "usageContext": {"forged": True}}
        context = TODAY.proper_appointment_context_for("roman-1962", mass, predicates)
        self.assertNotIn("usageContext", context)
        result = self.resolution(mass, context)
        self.assertIn("proper_appointment_usage", result)
        self.assertIsNone(result["proper_appointment_usage"])
        self.assertEqual(len(result["proper_appointment_unresolved"]), 1)
        self.assertFalse(any(event.get("proper", {}).get("name") == "Alleluia" for event in result["events"]))
        TODAY.expanded_event_projection("roman-1962", mass, None, list(range(len(mass["propers"]))), predicates)
        self.assertIsNone(mass["proper_appointment_usage"])

    def test_shared_helper_refuses_partial_or_wrong_original_coordinates(self):
        _, _, mass, _ = self.show()
        valid = TODAY.proper_appointment_context_for("roman-1962", mass, {})
        mutations = {
            "candidate absent": lambda c: c["branch"].update(candidates=[]),
            "readable id absent": lambda c: c["readable"].pop("id"),
            "unsettled": lambda c: c["branch"].update(settled=False),
            "not said": lambda c: c["readable"].update(state="commemorated"),
            "wrong current mass": lambda c: c["mass"].update(key="advent-2"),
            "wrong form": lambda c: c.update(formId="unheld-form"),
            "ambiguous form": lambda c: c.update(formId=None),
            "wrong calendar": lambda c: c.update(calendar="roman-pre-1955"),
            "wrong entrance": lambda c: c.update(entrance="propers"),
            "wrong original tuple": lambda c: c.update(branch=copy.deepcopy(self.derived["2026-12-06"]["options"][0])),
        }
        for label, mutate in mutations.items():
            context = copy.deepcopy(valid)
            mutate(context["usageContext"])
            with self.subTest(label=label):
                result = self.resolution(mass, context)
                self.assertIsNone(result["proper_appointment_usage"])
                self.assertEqual(len(result["proper_appointment_unresolved"]), 1)

    def test_unselected_mass_and_wrong_edition_do_not_receive_original_day_context(self):
        _, _, mass, _ = self.show()
        for update in ({"selected": False}, {"selected": None}):
            unselected = copy.deepcopy(mass)
            unselected.update(update)
            self.assertNotIn("usageContext", TODAY.proper_appointment_context_for("roman-1962", unselected, {}))
            self.assertIsNone(self.resolution(unselected)["proper_appointment_usage"])
        self.assertNotIn("usageContext", TODAY.proper_appointment_context_for("roman-pre-1955", mass, {}))

    def test_unused_usage_fact_does_not_change_existing_payload_or_post_pentecost_chant(self):
        _, _, mass, _ = self.show("2026-06-08")
        result = self.resolution(mass)
        self.assertNotIn("proper_appointment_usage", mass)
        self.assertNotIn("proper_appointment_usage", result)
        self.assertEqual([(event["sourceIndex"], event["proper"]) for event in result["events"] if event["kind"] == "proper"], list(enumerate(mass["propers"])))
        self.assertTrue(any(row["name"] == "Alleluia" for row in mass["propers"]))

    def test_malformed_source_selector_still_refuses_in_the_shared_validator(self):
        _, _, mass, _ = self.show()
        context = TODAY.proper_appointment_context_for("roman-1962", mass, {})
        context = copy.deepcopy(context)
        fact = next(fact for fact in context["facts"].values() if "usage_values" in fact)
        fact["usage_values"]["unknown"] = "chant-present"
        with self.assertRaises(TODAY.Refused):
            self.resolution(mass, context)


if __name__ == "__main__":
    unittest.main()
