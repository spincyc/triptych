"""The ferial insertion follows exact source appointments across reader surfaces."""

from pathlib import Path
from importlib.machinery import SourceFileLoader
from importlib.util import module_from_spec, spec_from_loader
import json
import subprocess
import sys
import unittest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(Path(__file__).resolve().parent))
from _product_data import browser_data_root


class FerialPrayerOverPeople(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = browser_data_root(ROOT)
        cls.runner = ROOT / "tools/tests/ferial_prayer_over_people.cjs"

    def check_case(self, name):
        result = subprocess.run(
            ["node", str(self.runner), str(ROOT), str(self.data), name],
            text=True, capture_output=True, check=False,
        )
        self.assertEqual(result.returncode, 0, result.stderr or result.stdout)
        report = json.loads(result.stdout)
        self.assertEqual(report["case"], name)
        self.assertGreater(report["checks"], 0)

    def test_exact_appointments_have_one_finite_seat_without_label_fallback(self):
        self.check_case("exact-appointments")

    def test_wrong_context_foreign_sources_and_malformed_declarations_refuse(self):
        self.check_case("scope-refusals")

    def test_unknown_context_and_unrelated_masses_never_appoint_the_cue(self):
        self.check_case("unknown-and-unrelated")

    def test_every_appointed_form_preserves_bilingual_source_events(self):
        self.check_case("bilingual-adapters")

    def test_every_appointed_prayer_has_independent_complete_conclusion(self):
        self.check_case("complete-conclusions")

    def test_day_rite_follows_all_commemorated_postcommunions_independently(self):
        self.check_case("day-commemorations")

    def test_missing_conclusion_has_visible_coverage_in_read_and_missal(self):
        self.check_case("missing-conclusion")

    def test_missing_cue_anchor_or_unrecognized_proper_cannot_pass(self):
        self.check_case("broken-frame")

    def test_missing_bodies_and_specialized_frames_remain_explicit(self):
        self.check_case("remaining-frames")


class FerialPrayerCliTransport(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        data = browser_data_root(ROOT)
        cls.ordinary = json.loads((data / "structure/ordinary/roman-1962.json").read_text())
        cls.structure = json.loads((data / "structure/propers/roman-1962.json").read_text())
        cls.mass = next(row for row in cls.structure["masses"] if row["key"] == "passion-friday")
        loader = SourceFileLoader("ferial_prayer_cli_transport", str(ROOT / "tools/mass-today"))
        spec = spec_from_loader(loader.name, loader)
        cls.tool = module_from_spec(spec)
        sys.modules[spec.name] = cls.tool
        loader.exec_module(cls.tool)

    def context(self, form="main"):
        return {"calendar": "roman-1962", "mass": self.mass["key"], "formId": form,
                "entrance": "propers", "date": None, "season": None,
                "facts": self.structure.get("proper_appointment_facts", {}), "choices": {}}

    def test_exact_context_transports_one_cue_and_seat_without_changing_source_rows(self):
        before = json.dumps(self.mass["propers"], sort_keys=True)
        result = self.tool.mass_events(self.ordinary, self.mass["propers"], None,
                                       proper_appointment_context=self.context())
        events = result["events"]
        cues = [row for row in events if row.get("element", {}).get("key") ==
                "conclusio/oratio-super-populum-cues"]
        prayers = [row for row in events if row.get("proper", {}).get("name") == "Oratio super populum"]
        finals = [row for row in events if row.get("element", {}).get("key") ==
                  "conclusio/dominus-vobiscum-ite-missa-est"]
        self.assertEqual((len(cues), len(prayers), len(finals)), (1, 1, 1))
        self.assertLess(events.index(cues[0]), events.index(prayers[0]))
        self.assertLess(events.index(prayers[0]), events.index(finals[0]))
        self.assertEqual(prayers[0]["seat"]["rite"], "oratio-super-populum")
        self.assertEqual(prayers[0]["placement"], "seated")
        self.assertEqual(json.dumps(self.mass["propers"], sort_keys=True), before)

    def test_wrong_explicit_form_cannot_emit_a_seated_prayer_without_a_seat(self):
        with self.assertRaises(self.tool.Refused):
            self.tool.mass_events(self.ordinary, self.mass["propers"], None,
                                  proper_appointment_context=self.context("unheld"))

    def test_context_free_ordinary_does_not_assert_a_mass_appointment(self):
        result = self.tool.mass_events(self.ordinary, [], None)
        self.assertFalse(any(row.get("element", {}).get("key") == "conclusio/oratio-super-populum-cues"
                             for row in result["events"]))
        self.assertTrue(any(row.get("element") == "conclusio/oratio-super-populum-cues"
                            for row in result["unresolved"]))


if __name__ == "__main__":
    unittest.main()
