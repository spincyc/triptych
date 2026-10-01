"""Preserve the 2026-10-01 Ordo collation, including its two negative findings.

The source is the registered ed4bc14e scan of the 1981 Ordo, read at 200 dpi.
Exact artifact pages and marginal numbers are kept beside the cases below and
in each Mass's notes. No protected source text is needed for these checks.
"""

from pathlib import Path
import unittest

import yaml


ROOT = Path(__file__).resolve().parents[2]


class PostconciliarPsalmCollationTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        document = yaml.safe_load(
            (ROOT / "src/sources/calendars/postconciliar/propers.yaml").read_text()
        )
        cls.masses = {
            mass["key"]: mass
            for section in document["sections"].values()
            for mass in section["masses"]
        }

    def citation(self, mass, proper, cycle_key=None, cycle=None):
        slot = next(p for p in self.masses[mass]["propers"] if p["name"] == proper)
        if cycle_key:
            slot = slot[cycle_key][cycle]
        return slot["verses"][0]

    def test_responsorial_4bc_addresses_the_whole_hebrew_verse(self):
        cases = (
            ("advent-1", "cycles", "C", 59, 3),
            ("advent-3-monday", None, None, 161, 187),
            ("advent-december-23", None, None, 166, 199),
            ("lent-1", "cycles", "B", 73, 23),
            ("lent-3-tuesday", None, None, 188, 238),
            ("ot-3", "cycles", "B", 100, 68),
            ("ot-9-thursday", "weekday_cycles", "II", 244, 356),
        )
        for mass, cycle_key, cycle, page, number in cases:
            with self.subTest(mass=mass, cycle=cycle, page=page, number=number):
                citation = self.citation(mass, "Responsorial Psalm", cycle_key, cycle)
                self.assertEqual(citation["book"], "Psalms")
                self.assertEqual(
                    citation["ranges"][0]["begin"], {"chapter": 25, "verse": 4}
                )
                self.assertEqual(
                    citation["ranges"][0]["end"],
                    {"chapter": 25, "verse": 5, "part": "ab"},
                )
                self.assertTrue(citation["ref"].startswith("Psalm 25:4-5ab,"))

    def test_responsorial_range_does_not_extend_3b_into_hebrew_4a(self):
        # Ordo artifact p. 244, n. 355: its Vulgate 4a ends Hebrew verse 3.
        citation = self.citation(
            "ot-9-wednesday", "Responsorial Psalm", "weekday_cycles", "I"
        )
        self.assertEqual(
            citation["ranges"][:2],
            [
                {"begin": {"chapter": 25, "verse": 2},
                 "end": {"chapter": 25, "verse": 3}},
                {"begin": {"chapter": 25, "verse": 4},
                 "end": {"chapter": 25, "verse": 5, "part": "ab"}},
            ],
        )
        self.assertEqual(citation["ref"], "Psalm 25:2-3, 4-5ab, 6-7bc, 8-9")

    def test_acclamation_words_keep_the_second_hebrew_colon(self):
        # Unlike the responsorial selections, these printed acclamations use
        # 4b for the request to be taught the paths: already Hebrew 25:4b.
        for mass, page, number in (
            ("ot-10-wednesday", 247, 361),
            ("ot-20-friday", 278, 423),
        ):
            with self.subTest(mass=mass, page=page, number=number):
                citation = self.citation(mass, "Gospel Acclamation")
                self.assertEqual(citation["ref"], "Psalm 25:4b, 5a")
                self.assertEqual(
                    citation["ranges"][0],
                    {"begin": {"chapter": 25, "verse": 4, "part": "b"},
                     "end": {"chapter": 25, "verse": 4, "part": "b"}},
                )


if __name__ == "__main__":
    unittest.main()
