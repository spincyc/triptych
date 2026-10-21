#!/usr/bin/env python3
"""Source-backed Q4 commemoration prayer appointments and Common origins."""
import copy
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))
from _calendars import mass_index, proper_family, read_yaml, resolve_propers

SOURCE = ROOT / "src/sources/calendars/roman-1962/propers.yaml"
OWN = (
    "comm-s-chrysogoni-martyris", "comm-s-felicitatis-martyris",
    "comm-s-mennae-martyris", "comm-ss-sergii-bacchi-marcelli-apuleii",
    "comm-ss-ursulae-ac-sociarum-virginum", "comm-s-thomae-episcopi-martyris",
    "comm-ss-tryphonis-respicii-nymphae-virginis",
    "comm-ss-vitalis-agricolae-martyrum", "third-day-within-octave-s-ioannis",
)
INHERITED = (
    "comm-s-barbarae-virginis-martyris", "comm-s-evaristi-papae-martyris",
    "comm-s-hilarionis-abbatis", "comm-s-marci-papae-confessoris",
    "comm-s-melchiadis-papae-martyris",
    "comm-s-petri-alexandrini-episcopi-martyris", "comm-s-pontiani-papae-martyris",
    "comm-s-remigii-episcopi-confessoris", "s-eusebii-episcopi-martyris",
)
OTHER = (
    "comm-s-sabbae-abbatis", "comm-s-silvestri-i-papae-confessoris",
    "comm-s-theodori-martyris", "comm-ss-dionysii-episcopi-rustici-eleutherii",
    "comm-ss-placidi-sociorum-martyrum", "maternitatis-beatae-mariae-virginis",
    "s-lucae-evangelistae",
)
FAMILIES = ["Collect", "Secret", "Postcommunion"]


class CommemorationOrations(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.document = read_yaml(SOURCE)
        cls.masses = mass_index(cls.document)

    def orations(self, key):
        entries, errors = resolve_propers(self.document, self.masses[key])
        self.assertEqual(errors, [], key)
        return [(proper, provenance) for _, proper, provenance in entries
                if proper_family(proper["name"]) in FAMILIES]

    def test_all_commemorated_beneficiaries_have_the_three_prayers_in_order(self):
        for key in OWN + INHERITED + OTHER:
            with self.subTest(mass=key):
                self.assertEqual([p["name"] for p, _ in self.orations(key)], FAMILIES)

    def test_own_prayers_do_not_fall_back_to_common_formulas(self):
        for key in OWN:
            with self.subTest(mass=key):
                self.assertEqual([origin for _, origin in self.orations(key)], [None] * 3)
        for key in INHERITED:
            with self.subTest(mass=key):
                self.assertTrue(all(origin is not None for _, origin in self.orations(key)))

    def test_felicity_requires_all_own_families_to_omit_common_choice(self):
        own = self.masses["comm-s-felicitatis-martyris"]
        self.assertNotIn("common_sets", own["takes_from"])
        for family in FAMILIES:
            with self.subTest(missing=family):
                incomplete = copy.deepcopy(own)
                incomplete["propers"] = [p for p in incomplete["propers"] if p["name"] != family]
                _, problems = resolve_propers(self.document, incomplete)
                self.assertTrue(problems)


if __name__ == "__main__":
    unittest.main()
