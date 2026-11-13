"""Annual Dedication Secrets require a location fact, never a default prayer."""
from pathlib import Path
import copy
import importlib.machinery
import importlib.util
import sys
import unittest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))
import _calendars as C

loader = importlib.machinery.SourceFileLoader("dedication_context_rubrics", str(ROOT / "tools/calendar-rubrics"))
spec = importlib.util.spec_from_loader(loader.name, loader)
R = importlib.util.module_from_spec(spec)
loader.exec_module(R)


class DedicationContextSourceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.rubrics = R.load_source(ROOT / "src/sources/calendars", "roman-1962")
        cls.document = C.load_document(ROOT / "src/sources/calendars", "roman-1962")
        cls.rule = cls.rubrics["dedication_anniversary_context"]

    def test_source_rule_binds_two_annual_feasts_without_public_evidence_payload(self):
        self.assertEqual([], R.check_dedication_anniversary_context(
            self.rubrics, self.document, "test"))
        built, problems, _ = R.build(ROOT / "src/sources/calendars", "roman-1962")
        self.assertEqual([], problems)
        self.assertEqual(self.rule, built[0]["dedication_anniversary_context"])
        self.assertNotIn("derived_from", built[0])
        self.assertNotIn("artifact_sha256", str(built[0]["dedication_anniversary_context"]))

    def test_missing_location_does_not_appoint_either_secret(self):
        for key in self.rule["keys"]:
            with self.subTest(mass=key):
                rows, errors = C.resolve_propers(self.document, C.mass_index(self.document)[key])
                self.assertEqual([], errors)
                prayers = [proper["name"] for _, proper, _ in rows
                           if C.proper_family(proper["name"]) in {"Collect", "Secret", "Postcommunion"}]
                self.assertEqual(["Collect", "Postcommunion"], prayers)

    def test_each_legitimate_context_resolves_one_exact_secret_and_anniversary_prayers(self):
        for key in self.rule["keys"]:
            for relation, condition in self.rule["conditions"].items():
                with self.subTest(mass=key, relation=relation):
                    document = copy.deepcopy(self.document)
                    mass = C.mass_index(document)[key]
                    mass["takes_from"]["common_sets"]["contextual-secret"] = {
                        "state": "selected", "option": condition["option"]}
                    rows, errors = C.resolve_propers(document, mass)
                    self.assertEqual([], errors)
                    prayers = [(proper["name"], origin["mass"]) for _, proper, origin in rows
                               if C.proper_family(proper["name"]) in {"Collect", "Secret", "Postcommunion"}]
                    self.assertEqual([(name, "commune-dedicationis-ecclesiae")
                                      for name in ("Collect", condition["proper"], "Postcommunion")], prayers)

    def test_invalid_scope_default_or_source_target_is_refused(self):
        changes = {
            "different-edition": lambda d: d.update(calendar="postconciliar"),
            "default": lambda d: d["dedication_anniversary_context"].update(default="outside-dedicated-church"),
            "known-without-context": lambda d: d["dedication_anniversary_context"].update(unknown="anniversary-outside-church"),
            "other-form": lambda d: d["dedication_anniversary_context"].update(form_id="other"),
            "duplicate-feast": lambda d: d["dedication_anniversary_context"].update(keys=[self.rule["keys"][0]] * 2),
            "consecration-day": lambda d: d["dedication_anniversary_context"]["required_selection"].update(option="dedication-day"),
            "source-order": lambda d: d["dedication_anniversary_context"]["conditions"]["outside-dedicated-church"].update(option="anniversary-in-church"),
            "wrong-prayer": lambda d: d["dedication_anniversary_context"]["conditions"]["in-dedicated-church"].update(proper="Secret (In ipso die Dedicationis)"),
            "missing-evidence": lambda d: d["derived_from"].pop("dedication_anniversary_context"),
        }
        for name, change in changes.items():
            with self.subTest(mutation=name):
                document = copy.deepcopy(self.rubrics)
                change(document)
                self.assertTrue(R.check_dedication_anniversary_context(document, self.document, "test"))
        changed = copy.deepcopy(self.document)
        C.mass_index(changed)[self.rule["keys"][0]]["takes_from"]["common_sets"]["contextual-secret"] = {
            "state": "selected", "option": "anniversary-outside-church"}
        self.assertTrue(R.check_dedication_anniversary_context(self.rubrics, changed, "test"))


if __name__ == "__main__":
    unittest.main()
