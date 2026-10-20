"""Human-readable Proper passages distinguish Bible text from Missal wording."""
from __future__ import annotations

import subprocess
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


class MassPropersShowTests(unittest.TestCase):
    def test_bible_passages_carry_local_wording_claims(self) -> None:
        result = subprocess.run(
            [
                str(ROOT / "tools/mass-propers"), "show", "--calendar", "roman-1962",
                "--mass", "s-luciae-virginis-martyris", "--bible", "clementine-vulgate",
                "--lang", "la", "--format", "text",
            ],
            cwd=ROOT, capture_output=True, text=True, check=True,
        )
        def section(name: str, following: str) -> str:
            return result.stdout.split(f"\n{name}\n", 1)[1].split(f"\n{following}\n", 1)[0]

        alleluia = section("Alleluia", "Gospel")
        communion = section("Communion", "Postcommunion")
        collect = section("Collect", "Epistle")

        self.assertIn("Bible reconstruction · Missal wording not established", alleluia)
        self.assertLess(alleluia.index("Bible reconstruction"), alleluia.index("Speciosus forma"))
        self.assertIn("Bible text · clementine-vulgate · shown separately from the Missal text", communion)
        self.assertLess(communion.index("Bible text"), communion.index("Sin* Principes"))
        self.assertLess(communion.index("Sin* Principes"), communion.index("quasi qui invenit spolia multa"))
        self.assertNotIn("Bible reconstruction", communion)
        self.assertNotIn("Bible reconstruction", collect)
        self.assertNotIn("Bible text", collect)


if __name__ == "__main__":
    unittest.main()
