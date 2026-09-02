"""Keep recovered OLM pointers and shorter Gospel forms source-exact."""

from pathlib import Path
import unittest

import yaml


ROOT = Path(__file__).resolve().parents[2]
PROPERS = (
    ROOT / "src" / "sources" / "calendars" / "postconciliar" / "propers.yaml"
)


class PostconciliarOlmPointerRecoveryTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        calendar = yaml.safe_load(PROPERS.read_text(encoding="utf-8"))
        cls.masses = {
            mass["key"]: mass
            for section in calendar["sections"].values()
            for mass in section["masses"]
        }

    def mass(self, key: str) -> dict:
        return self.masses[key]

    def form(self, mass: str, form_id: str) -> dict:
        return next(
            form for form in self.mass(mass)["forms"] if form["id"] == form_id
        )

    def proper(self, mass: str, name: str, form_id: str | None = None) -> dict:
        owner = self.form(mass, form_id) if form_id else self.mass(mass)
        return next(proper for proper in owner["propers"] if proper["name"] == name)

    def test_january_four_points_to_the_printed_january_two_acclamation(self) -> None:
        mass = self.mass("christmas-january-4")
        self.assertIn("artifact page 172", mass["notes"])
        self.assertIn("n. 207", mass["notes"])
        self.assertEqual(
            [proper["name"] for proper in mass["propers"]],
            ["First Reading", "Responsorial Psalm", "Gospel Acclamation", "Gospel"],
        )
        self.assertEqual(
            self.proper("christmas-january-4", "Gospel Acclamation")["takes_from"],
            {
                "mass": "christmas-january-2",
                "proper": "Gospel Acclamation",
                "citation": "Cf. n. 205",
            },
        )

    def test_easter_octave_points_to_monday_once_and_in_printed_order(self) -> None:
        monday = self.proper("easter-monday", "Gospel Acclamation")
        self.assertEqual(monday["verses"][0]["ref"], "Psalm 118:24")
        expected_pages = {
            "easter-tuesday": (199, 262),
            "easter-wednesday": (199, 263),
            "easter-thursday": (200, 264),
            "easter-friday": (200, 265),
            "easter-saturday": (200, 266),
        }
        for key, (page, number) in expected_pages.items():
            with self.subTest(mass=key):
                mass = self.mass(key)
                self.assertIn(f"artifact page {page}", mass["notes"])
                self.assertIn(f"n. {number}", mass["notes"])
                names = [proper["name"] for proper in mass["propers"]]
                self.assertEqual(names[2:4], ["Gospel Acclamation", "Gospel"])
                self.assertEqual(
                    self.proper(key, "Gospel Acclamation")["takes_from"],
                    {
                        "mass": "easter-monday",
                        "proper": "Gospel Acclamation",
                        "citation": "ut supra, n. 261",
                    },
                )

    def test_nativity_shorter_gospels_and_date_aliases_match(self) -> None:
        nativity = self.mass("nativity")
        self.assertIn("artifact pages 65-66", nativity["notes"])
        self.assertIn("nn. 13-16", nativity["notes"])
        expected = {
            "vigil": ("Matthew 1:18-25", [(1, 18, 1, 25)]),
            "day": ("John 1:1-5, 9-14", [(1, 1, 1, 5), (1, 9, 1, 14)]),
        }
        for form_id, (reference, ranges) in expected.items():
            with self.subTest(form=form_id):
                source_form = self.form("nativity", form_id)
                alias_form = self.form("nativity-lord", form_id)
                source_names = [proper["name"] for proper in source_form["propers"]]
                alias_names = [proper["name"] for proper in alias_form["propers"]]
                self.assertEqual(
                    source_names[source_names.index("Gospel") : source_names.index("Gospel") + 2],
                    ["Gospel", "Gospel (shorter form)"],
                )
                self.assertEqual(
                    alias_names[alias_names.index("Gospel") : alias_names.index("Gospel") + 2],
                    ["Gospel", "Gospel (shorter form)"],
                )
                shorter = self.proper("nativity", "Gospel (shorter form)", form_id)
                self.assertEqual(shorter["verses"][0]["ref"], reference)
                self.assertEqual(
                    [
                        (
                            row["begin"]["chapter"],
                            row["begin"]["verse"],
                            row["end"]["chapter"],
                            row["end"]["verse"],
                        )
                        for row in shorter["verses"][0]["ranges"]
                    ],
                    ranges,
                )
                self.assertEqual(
                    self.proper("nativity-lord", "Gospel (shorter form)", form_id)[
                        "takes_from"
                    ],
                    {
                        "mass": "nativity",
                        "form": source_form["name"],
                        "proper": "Gospel (shorter form)",
                    },
                )

    def test_holy_wednesday_retains_an_honest_two_target_absence(self) -> None:
        mass = self.mass("holy-wednesday")
        self.assertIn("artifact page 194", mass["notes"])
        self.assertIn("n. 259", mass["notes"])
        self.assertNotIn("Gospel Acclamation", [row["name"] for row in mass["propers"]])
        self.assertIn("choice-pointer to two targets", mass["notes"])
        self.assertIn("typed absence", mass["notes"])
        self.assertNotIn("prints a composed text", mass["notes"])


if __name__ == "__main__":
    unittest.main()
