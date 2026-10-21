"""Source appointment boundaries for the November 1962 Common repairs."""
from __future__ import annotations

from pathlib import Path
import sys
import tomllib
import unittest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))
import _calendars as C
import _proper_latin as L

CALENDAR = ROOT / "src/sources/calendars/roman-1962/propers.yaml"
POINTERS = ROOT / "src/sources/inventories/roman-1962-sanctoral-commons-v1.toml"
LATIN = ROOT / "src/sources/inventories/roman-1962-proper-latin-provenance-v1.toml"


class Roman1962CommonRepairs(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.document = C.read_yaml(CALENDAR)
        cls.masses = C.mass_index(cls.document)

    def resolved(self, key):
        rows, problems = C.resolve_propers(self.document, self.masses[key])
        self.assertEqual(problems, [])
        return {proper["name"]: (proper, provenance) for _, proper, provenance in rows}

    def test_theodore_has_three_own_commemoration_orations(self):
        # AP794/printed713:4054P/4055P/4056P. Common chants are not performed
        # by a commemoration; its source-owned prayer identity still matters.
        mass = self.masses["comm-s-theodori-martyris"]
        own = {p["name"]: p for p in mass["propers"]}
        resolved = self.resolved(mass["key"])
        for name in ("Collect", "Secret", "Postcommunion"):
            with self.subTest(proper=name):
                self.assertIn(name, own)
                proper, provenance = resolved[name]
                self.assertIsNone(provenance, "an own prayer must not be substituted from the Common")
                self.assertEqual(proper, own[name])
                if not isinstance(proper.get("text"), str):
                    self.assertEqual(proper.get("text_status", {}).get("state"), "unavailable")
                    self.assertEqual(proper["text_status"]["scope"], "proper-body")

    def test_andrew_uses_confessor_common_not_neighboring_martyrs(self):
        # AP794/[713] appoints Os iusti [24]. The erroneous direct rows came
        # from the distinct AP795-796 commemoration, including Romans8:18-23.
        mass = self.masses["s-andreae-avellini-confessoris"]
        target = "commune-confessoris-non-pontificis-1"
        self.assertEqual(mass.get("takes_from", {}).get("mass"), target)
        own = {p["name"]: p for p in mass["propers"]}
        self.assertEqual(set(own), {"Collect", "Secret", "Postcommunion"})
        resolved = self.resolved(mass["key"])
        for name in ("Introit", "Lesson", "Gradual", "Gospel", "Offertory", "Communion"):
            with self.subTest(proper=name):
                self.assertEqual(resolved[name][1]["mass"], target)
        self.assertEqual([v["ref"] for v in resolved["Lesson"][0]["verses"]], ["Sirach 31:8-11"])
        self.assertEqual([v["ref"] for v in resolved["Gospel"][0]["verses"]], ["Luke 12:35-40"])
        self.assertNotIn("Romans 8:18-23", [v["ref"] for proper, _ in resolved.values() for v in proper.get("verses", [])])
        records, problems = L.read_sidecar(LATIN)
        self.assertEqual(problems, [])
        for name, proper in own.items():
            with self.subTest(prayer=name):
                self.assertIsNone(resolved[name][1])
                decision = L.decision_for(L.LatinKey(mass["key"], "", name), proper["text"], records)
                self.assertEqual(decision.provenance_status, "collated")
                self.assertTrue(decision.permits(L.STRUCTURE_SURFACES))

    def test_november_pointer_keys_distinguish_feast_and_commemoration(self):
        rows = tomllib.loads(POINTERS.read_text())["pointers"]
        expected = {
            (791, "11-04", 19): "s-caroli-episcopi-confessoris",
            (794, "11-09", 39): "dedicatione-archibasilicae-mi-salvatoris",
            (794, "11-09", 8): "comm-s-theodori-martyris",
        }
        for address, mass in expected.items():
            with self.subTest(source=address):
                matches = [r for r in rows if (r["digital_page"], r["date"], r["printed_bracket"]) == address]
                self.assertEqual(len(matches), 1)
                self.assertEqual(matches[0]["mass"], mass)
                self.assertIn(mass, self.masses)


if __name__ == "__main__":
    unittest.main()
