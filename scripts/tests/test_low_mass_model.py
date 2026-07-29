#!/usr/bin/env python3
"""Regression checks for the declared two-server Low-Mass model."""

from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[2]
OWNER = (
    ROOT
    / "src/gpt/liturgy/roman-rite/1962/reference/altar-server-guides"
)


class LowMassModelTests(unittest.TestCase):
    def setUp(self) -> None:
        self.ceremony = (OWNER / "shared/low-mass-ceremony.tex").read_text()
        self.diagrams = (OWNER / "shared/low-mass-diagrams.tex").read_text()
        self.inventory = (OWNER / "research/ceremonial-inventory.md").read_text()

    def test_gospel_wait_and_same_level_geometry_are_explicit(self) -> None:
        self.assertIn(r"\emph{In illo tempore}", self.ceremony)
        self.assertIn("same step level but laterally clear", self.ceremony)
        self.assertIn("First G/Step2; Second G/Step2 laterally clear", self.inventory)

    def test_offertory_formation_and_first_only_ablutions_are_explicit(self) -> None:
        self.assertIn("Side by side on the second step", self.ceremony)
        self.assertIn("First alone serves both ablutions", self.ceremony)
        self.assertIn("Pour wine first and then", self.ceremony)
        self.assertNotIn("First pours wine;\\nSecond pours water", self.ceremony)

    def test_coordinated_veil_and_book_exchange_has_no_cover_wait(self) -> None:
        self.assertIn("First takes the folded chalice veil", self.ceremony)
        self.assertIn("Second takes the Missal and stand", self.ceremony)
        self.assertIn("switch back to their normal", self.ceremony)
        self.assertIn("not an invented universal", self.ceremony)

    def test_corrected_low_mass_plates_replace_superseded_assets(self) -> None:
        for asset in (27, 28, 29, 31):
            self.assertIn(f"ASG-ART-0{asset}", self.diagrams)
        for asset in (
            "ASG-ART-012-lm-gospel-stations",
            "ASG-ART-013-lm-offertory-cruets",
            "ASG-ART-017-lm-mc-first-ablution",
            "ASG-ART-018-lm-mc-ablution",
            "ASG-ART-019-lm-book-and-veil-return",
        ):
            self.assertNotIn(asset, self.diagrams)


if __name__ == "__main__":
    unittest.main()
