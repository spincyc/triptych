"""An enacted Mass's explicit Proper choice never selects another formulary."""
from __future__ import annotations

import argparse
import contextlib
import copy
import importlib.machinery
import importlib.util
import io
import os
from pathlib import Path
import sys
import unittest
from unittest.mock import patch

ROOT = Path(os.environ.get("TRIPTYCH_REVIEW_ROOT", Path(__file__).resolve().parents[2]))
MODULE_ROOT = Path(os.environ.get("TRIPTYCH_APPOINTMENT_MODULE_ROOT", ROOT))
CALENDARS_ROOT = Path(os.environ.get("TRIPTYCH_APPOINTMENT_CALENDARS_ROOT", MODULE_ROOT))
sys.path.insert(0, str(ROOT / "scripts"))
sys.path.insert(0, str(CALENDARS_ROOT / "scripts"))
loader = importlib.machinery.SourceFileLoader("_proper_choice_cli_scope_today", str(MODULE_ROOT / "tools/mass-today"))
spec = importlib.util.spec_from_loader(loader.name, loader)
TODAY = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = TODAY
loader.exec_module(TODAY)
TODAY.SEATING_MODEL = Path(os.environ.get("TRIPTYCH_APPOINTMENT_SEATING", ROOT / "src/web/browser/liturgy/ordinary-seating.js"))

CHOICE = "proper-choice/roman-1962/fixture-selected/main/gospel=principal"
ORDINARY = {"sections": [{"key": "fixture-section", "name": "Technical Ordinary fixture", "elements": [{"key": "fixture-element", "kind": "prayer", "name": "Technical frame", "translations": [{"lang": "la", "text": "Technical frame body."}]}]}], "slots": [{"id": "fixture-gospel", "anchor": "fixture-element", "where": "before", "propers": ["Gospel", "Gospel (vel)"]}]}


def formulary(key):
    anchor = {"mass": key, "form_id": "main", "proper": "Gospel", "occurrence": 1}
    propers = []
    for name, option in (("Gospel", "principal"), ("Gospel (vel)", "other")):
        propers.append({
            "name": name, "form_id": "main", "source": "composed",
            "text": f"Technical {key} {option} body.",
            "appointment_identity": {**anchor, "proper": name},
            "ordinary_disposition": {"kind": "alternative", "group": "gospel", "option": option, "anchor": dict(anchor), "basis": "Technical exact choice-scope fixture; no historical rule is asserted."},
        })
    return {"propers": propers, "_proper_source_indices": [4, 8], "placeholders": 0, "forms": [], "ordinary_frame": {"applicability": "full"}}


def arguments(machine=False, choices=None):
    return argparse.Namespace(
        date="2026-10-20", calendar="roman-1962", expanded=True,
        ordinary=False, ordinary_variant=None, territory=None, mass=None,
        form=None, proper_choice=[CHOICE] if choices is None else choices,
        lang="la", bible="fixture-bible", witness=None, why=False,
        rubrics=True, json=False, format="json" if machine else "text",
        style_resolved=TODAY.Style(),
    )


class ProperChoiceCliScopeTests(unittest.TestCase):
    def run_day(self, args, *, ordinary="held", selected=True, standing="commemorated"):
        branch = {
            "settled": True, "winner": {"key": "fixture-selected", "nature": "feast"} if selected else None,
            "readable": [{"key": "fixture-selected", "state": "said"}, {"key": "fixture-other", "state": standing}],
        }
        if not selected:
            branch.update(choiceRequired=True, choice={"required": True, "among": [{"key": "fixture-selected"}, {"key": "fixture-other"}]})
        ranked = {"days": [{"calendar": "roman-1962", "season": "regular", "weekday": "tuesday", "options": [branch]}]}

        def invoke(tool, argv):
            if tool == "calendar-rubrics":
                return copy.deepcopy(ranked)
            if tool == "mass-ordinary":
                if ordinary == "unavailable":
                    raise TODAY.Refused("Technical unavailable Ordinary fixture")
                return {"ordinary": [copy.deepcopy(ORDINARY)]}
            raise AssertionError(f"unexpected tool call {tool}")

        def propers(calendar, key, *unused, **kwargs):
            mass = formulary(key)
            if ordinary == "suppressed":
                mass["ordinary_frame"] = {"applicability": "none", "basis": "Technical source frame suppression fixture"}
            return mass

        with patch.object(TODAY, "invoke", side_effect=invoke), patch.object(TODAY, "invoke_propers", return_value={}), patch.object(TODAY, "propers_of", side_effect=propers), patch.object(TODAY, "indexed_bible", return_value={"id": "fixture-bible", "language": "la"}):
            return TODAY.run_show(args)

    def test_expanded_text_and_machine_scope_only_the_enacted_mass(self):
        # The real render() loop calls render_expanded_mass for both rows.
        # Exercise its framed, absent-Ordinary and source-suppressed paths.
        for ordinary in ("held", "unavailable", "suppressed"):
            for standing in ("commemorated", "displaced", "option"):
                with self.subTest(ordinary=ordinary, standing=standing):
                    args = arguments()
                    payload = self.run_day(args, ordinary=ordinary, standing=standing)
                    raw_propers = copy.deepcopy([mass["propers"] for mass in payload["days"][0]["masses"]])
                    output = io.StringIO()
                    with contextlib.redirect_stdout(output):
                        TODAY.render(payload, args)
                    text = output.getvalue()
                    self.assertIn("Technical fixture-selected principal body.", text)
                    self.assertNotIn("Technical fixture-selected other body.", text)
                    self.assertNotIn("Technical fixture-other principal body.", text)
                    self.assertNotIn("Technical fixture-other other body.", text)
                    self.assertEqual(text.count("Proper choice required: gospel"), 1)
                    self.assertEqual([mass["propers"] for mass in payload["days"][0]["masses"]], raw_propers)

                    machine = self.run_day(arguments(machine=True), ordinary=ordinary, standing=standing)
                    enacted, other = machine["days"][0]["masses"]
                    choice = next(event for event in enacted["expanded_events"] if event["kind"] == "proper-choice")
                    self.assertEqual(choice["id"], CHOICE.partition("=")[0])
                    self.assertEqual(choice["source_index"], 4)
                    self.assertEqual(choice["selection"], {"state": "selected", "option": "principal"})
                    self.assertEqual(enacted["proper_appointment_selections"]["main/gospel"], choice["selection"])
                    self.assertEqual(choice["options"][0]["events"], ["proper/roman-1962/fixture-selected/005"])
                    self.assertNotIn("expanded_events", other)
                    self.assertNotIn("proper_appointment_selections", other)
                    self.assertEqual([mass["propers"] for mass in machine["days"][0]["masses"]], raw_propers)

    def test_stale_or_malformed_explicit_requests_are_still_refused(self):
        cases = ([CHOICE.replace("roman-1962", "postconciliar")],
                 [CHOICE.replace("fixture-selected", "fixture-other")],
                 [CHOICE, CHOICE], ["gospel=principal"],
                 [CHOICE.replace("/main/", "/missing/")],
                 [CHOICE.replace("/gospel=", "/missing=")],
                 [CHOICE.replace("=principal", "=missing")])
        for machine in (False, True):
            for choices in cases:
                with self.subTest(machine=machine, choices=choices), self.assertRaises(TODAY.Refused):
                    args = arguments(machine=machine, choices=choices)
                    payload = self.run_day(args, ordinary="suppressed")
                    with contextlib.redirect_stdout(io.StringIO()):
                        TODAY.render(payload, args)

    def test_explicit_choice_requires_an_enacted_mass_in_both_formats(self):
        for machine in (False, True):
            with self.subTest(machine=machine), self.assertRaisesRegex(TODAY.Refused, "one selected Mass"):
                self.run_day(arguments(machine=machine), selected=False)


if __name__ == "__main__":
    unittest.main()
