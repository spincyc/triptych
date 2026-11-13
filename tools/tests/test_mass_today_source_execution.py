"""Actual dated choices and atomic source-owned prayers reach the native CLI."""
import contextlib
import io
import json
from types import SimpleNamespace
from pathlib import Path
import sys
import unittest
sys.path.insert(0, str(Path(__file__).resolve().parent))
from _mass_today_native_fixture import NativeTodayFixture


class NativeSourceExecutionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.fixture = NativeTodayFixture()

    def data(self, *args, **kwargs):
        result = self.fixture.run(*args, **kwargs)
        self.assertEqual(result.returncode, 0, result.stderr)
        return json.loads(result.stdout)

    def test_source_mass_choice_precedes_any_reading_or_execution(self):
        for language in ("en", "la"):
            with self.subTest(language=language):
                day = self.data("2026-03-27", language)["days"][0]
                self.assertTrue(day["choice_required"])
                self.assertIsNone(day["selected_mass"])
                self.assertTrue(all(not mass.get("expanded_events") and not mass.get("derived_execution") for mass in day["masses"]))
                text = self.fixture.run("2026-03-27", language, text=True)
                self.assertEqual(text.returncode, 0, text.stderr)
                self.assertIn("Mass choice required", text.stdout)
                self.assertNotIn("Collect", text.stdout)
                for key in ("passion-friday", "comm-septem-dolorum-beatae-mariae-virginis"):
                    selected = self.data("2026-03-27", language, key)["days"][0]
                    self.assertFalse(selected["choice_required"])
                    self.assertEqual(selected["selected_mass"], key)
                for key in ("s-ioannis-damasceni-confessoris-ecclesiae-doctoris", "advent-2", "missa-feriae"):
                    self.assertNotEqual(self.fixture.run("2026-03-27", language, key).returncode, 0)
        joseph = self.data("2027-03-19")["days"][0]
        self.assertEqual(joseph["selected_mass"], "s-ioseph-sponsi-beatae-mariae-virginis")
        self.assertFalse(joseph["choice_required"])

    def test_christmas_prayer_owner_remains_private_with_exact_original_rows(self):
        for date in ("2026-12-26", "2027-12-27", "2026-12-28"):
            for language in ("en", "la"):
                with self.subTest(date=date, language=language):
                    day = self.data(date, language)["days"][0]
                    mass = next(row for row in day["masses"] if row["selected"])
                    self.assertEqual(len(day["masses"]), 1)
                    self.assertNotEqual(mass["key"], "fifth-day-within-octave")
                    source = mass["oration_sources"]
                    self.assertEqual(source["principal"], mass["key"])
                    self.assertEqual([(row["mass"], row["source_index"], row["proper"]["name"]) for row in source["rows"]],
                        [("fifth-day-within-octave", 1, "Collect"), ("fifth-day-within-octave", 7, "Secret"), ("fifth-day-within-octave", 9, "Postcommunion")])
                    self.assertTrue(all(row["proper"]["language_selection"]["requested"] == language for row in source["rows"]))
                    self.assertNotEqual(self.fixture.run(date, language, "fifth-day-within-octave").returncode, 0)
        def wrong_owner(kind, value):
            if kind == "proper" and value["mass"]["key"] == "fifth-day-within-octave":
                value["mass"]["key"] = "unappointed-owner"
        self.assertNotEqual(self.fixture.run("2026-12-26", fault=wrong_owner).returncode, 0)

    def test_shared_conclusion_is_atomic_and_response_belongs_to_its_final_member(self):
        normalize = lambda text: " ".join(text.split())
        for language in ("en", "la"):
            with self.subTest(language=language):
                day = self.data("2026-03-27", language, "passion-friday")["days"][0]
                mass = next(row for row in day["masses"] if row["selected"])
                projection = mass["derived_execution"]
                group = next(row["execution"] for row in projection["groups"] if row["slot"] == "Postcommunion" and row["conclusion_group"] == 2)
                self.assertEqual(group["state"], "source-derived-complete")
                self.assertEqual([row["role"] for row in group["members"]], ["petition", "conclusion-provider"])
                projected = {row["id"]: row["execution"] for row in projection["members"]}
                self.assertEqual(sum(bool(projected[row["id"]]["response"]) for row in group["members"]), 1)
                self.assertEqual(group["response"]["provider_id"], group["members"][-1]["id"])
                text = self.fixture.run("2026-03-27", language, "passion-friday", text=True)
                self.assertEqual(text.returncode, 0, text.stderr)
                for row in projection["members"]:
                    self.assertIn(normalize(row["execution"]["member"]["priest_text"]), normalize(text.stdout))
                    self.assertIn(normalize(row["execution"]["member"]["source_text"]), normalize(text.stdout))
                if language == "en":
                    self.assertIn("Source-derived English for study; not an approved liturgical translation.", text.stdout)
                negative = self.data("2026-01-19", language)["days"][0]
                negative = next(row for row in negative["masses"] if row["selected"])["derived_execution"]
                group = next(row["execution"] for row in negative["groups"] if row["slot"] == "Postcommunion" and row["conclusion_group"] == 2)
                self.assertEqual(group["state"], "unresolved")
                self.assertFalse(group.get("members"))
                self.assertFalse(any("/comm-" in row["id"] for row in negative["members"]))

    def test_execution_projection_cannot_be_replayed_under_another_selected_form(self):
        day = self.data("2026-03-27", "en", "passion-friday")["days"][0]
        mass = next(row for row in day["masses"] if row["selected"])
        mass["selected_form"] = "unappointed-form"
        arguments = SimpleNamespace(date="2026-03-27", lang="en")
        with contextlib.redirect_stdout(io.StringIO()), self.assertRaisesRegex(self.fixture.today.Refused, "display scope changed"):
            self.fixture.today.render_expanded_mass(mass, None, arguments, self.fixture.today.Style(), frame=True, calendar="roman-1962")

    def test_changed_intermediate_source_refuses_and_no_language_makes_no_execution(self):
        def changed(kind, value):
            if kind == "proper" and value["mass"]["key"] == "s-ioannis-damasceni-confessoris-ecclesiae-doctoris":
                wrapper = next(row for row in value["appointed"] if row["name"] == "Postcommunion")
                proper = wrapper.get("proper", wrapper)
                proper["text"] += " changed"
                for translation in proper.get("translations", []):
                    translation["text"] += " changed"
        for language in ("en", "la"):
            result = self.fixture.run("2026-03-27", language, "passion-friday", fault=changed)
            self.assertEqual(result.returncode, 2, result.stderr)
            self.assertIn("dated conclusion projection failed", result.stderr)
        day = self.data("2026-03-27", None, "passion-friday")["days"][0]
        self.assertTrue(all("derived_execution" not in mass for mass in day["masses"]))


if __name__ == "__main__":
    unittest.main()
