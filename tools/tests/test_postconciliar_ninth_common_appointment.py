"""Bounded 2008 Common appointment identity; no prayer bodies or applicability join."""
from collections import Counter
from pathlib import Path
import sys
import tomllib
import unittest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))
import _missal_coverage as coverage

TARGET = "postconciliar:2002:common-slot:martyrs-several-outside-easter-5:postcommunion:1"
WRONG_FORM = "postconciliar:2002:common-slot:martyr-one-outside-easter-1:postcommunion:1"
SLOTS = "postconciliar-2002-common-appointed-slots"
FORMS = "postconciliar-2002-common-formularies"


class NinthCommonAppointmentTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.path = ROOT / "src/sources/inventories/missal-expected-targets-v1.toml"
        cls.document = tomllib.loads(cls.path.read_text(encoding="utf-8"))
        cls.targets = {row["id"]: row for row in cls.document["targets"]}

    def test_official_correction_establishes_only_the_named_appointment(self):
        row = self.targets[TARGET]
        self.assertEqual(row["identity_state"], "established")
        self.assertEqual((row["slice_id"], row["kind"], row["source_form_key"]),
                         (SLOTS, "text-slot", "martyrs-several-outside-easter-5"))
        for locator in ("Notitiae 44", "printed p. 375 / artifact p. 57",
                        "entry p. 915, p.c.", "artifact pp. 553-554",
                        "before the following one-martyr form 1",
                        "no unchanged wording"):
            self.assertIn(locator, row["source_locus"])
        self.assertEqual(set(row), {"id", "slice_id", "kind", "label", "source_record",
                                    "source_locus", "identity_state", "source_form_key"})

    def test_common_source_denominators_keep_their_distinct_units(self):
        slots = [row for row in self.targets.values() if row["slice_id"] == SLOTS]
        self.assertEqual(len(slots), 403)
        self.assertEqual(Counter(row["identity_state"] for row in slots),
                         {"established": 9, "target-correspondence-unresolved": 394})
        forms = [row for row in self.targets.values() if row["slice_id"] == FORMS]
        self.assertEqual(len(forms), 60)
        self.assertEqual(Counter(row["identity_state"] for row in forms),
                         {"target-correspondence-unresolved": 60})
        slot_slice = next(row for row in self.document["slices"] if row["id"] == SLOTS)
        self.assertIn("positively names nine of these appointments", slot_slice["basis"])

    def test_following_form_and_generic_collect_are_not_promoted(self):
        wrong = self.targets[WRONG_FORM]
        self.assertEqual(wrong["identity_state"], "target-correspondence-unresolved")
        self.assertEqual(wrong["source_form_key"], "martyr-one-outside-easter-1")
        same_form_neighbours = [row for row in self.targets.values()
                                if row.get("source_form_key") == "martyrs-several-outside-easter-5"
                                and row["id"] != TARGET]
        self.assertTrue(same_form_neighbours)
        self.assertEqual({row["identity_state"] for row in same_form_neighbours},
                         {"target-correspondence-unresolved"})
        self.assertFalse(any("entry p. 961, c." in row.get("source_locus", "")
                             for row in self.targets.values()
                             if row["slice_id"] == SLOTS and row["identity_state"] == "established"))

    def test_existing_owner_does_not_turn_source_identity_into_a_calendar_join(self):
        # Even a held Mass with a source-local key cannot supply an absent explicit join.
        masses = [{"key": key} for key in ("martyrs-several-outside-easter-5",
                                           "martyr-one-outside-easter-1")]
        report = coverage.expectations(self.path, "postconciliar", masses)
        rows = {row["id"]: row for row in report["targets"]}
        for target in (TARGET, WRONG_FORM):
            self.assertEqual(rows[target]["state"], "unresolved")
            self.assertIsNone(rows[target]["mass"])
            self.assertNotIn("calendar_mass_key", rows[target])
        self.assertEqual(report["whole_inventory_state"], "unresolved")


if __name__ == "__main__":
    unittest.main()
