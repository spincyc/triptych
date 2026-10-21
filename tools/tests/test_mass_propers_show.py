"""Human-readable Proper passages distinguish Bible text from Missal wording."""
from __future__ import annotations

import json
import subprocess
import sys

import yaml
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



class MassPropersBatchShowTests(unittest.TestCase):
    tool = ROOT / "tools/mass-propers"

    def show(self, masses: list[str], *, calendar: str = "roman-1962",
             lang: str = "la", bible: str | None = None, form: str = "text") -> subprocess.CompletedProcess[str]:
        command = [sys.executable, "-B", str(self.tool), "show",
                   "--root", str(ROOT / "src/sources/calendars"),
                   "--bible-root", str(ROOT / "src/sources/bibles"),
                   "--calendar", calendar, "--lang", lang]
        command += ["--json"] if form == "compact-json" else ["--format", form]
        if bible:
            command += ["--bible", bible]
        for mass in masses:
            command += ["--mass", mass]
        return subprocess.run(command, cwd=ROOT, capture_output=True, text=True, check=False)

    def test_batch_text_keeps_request_order_duplicates_and_each_bible_context(self) -> None:
        keys = ["epiphany-2", "advent-1", "epiphany-2"]
        singles = {}
        for key in dict.fromkeys(keys):
            result = self.show([key], bible="clementine-vulgate")
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("Bible reconstruction · Missal wording not established", result.stdout)
            singles[key] = result.stdout
        result = self.show(keys, bible="clementine-vulgate")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout, "\n".join(singles[key] for key in keys))
        self.assertEqual(result.stderr, "")

    def test_batch_text_keeps_typed_language_absences(self) -> None:
        keys = ["lent-3", "advent-1"]
        singles = [self.show([key], calendar="postconciliar", lang="en") for key in keys]
        for result in singles:
            self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("en translation unavailable: rights restricted", singles[0].stdout)
        result = self.show(keys, calendar="postconciliar", lang="en")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout, "\n".join(row.stdout for row in singles))

    def test_batch_machine_formats_keep_full_individual_records_and_source_choices(self) -> None:
        keys = ["easter-vigil", "lent-3"]
        singles = [self.show([key], calendar="postconciliar", lang="en", form="json") for key in keys]
        for result in singles:
            self.assertEqual(result.returncode, 0, result.stderr)
        records = [json.loads(row.stdout) for row in singles]
        # cli-v1 versions the response envelope, not every nested Mass.
        for record in records:
            self.assertEqual(record.pop("v"), 1)
        source_options = [row["proper"]["ordinary_disposition"] for row in records[0]["appointed"]
                          if row["proper"].get("ordinary_disposition", {}).get("kind") == "alternative"]
        self.assertGreaterEqual(len({row["group"] for row in source_options}), 2)
        for form in ("json", "yaml", "compact-json"):
            with self.subTest(form=form):
                result = self.show(keys, calendar="postconciliar", lang="en", form=form)
                self.assertEqual(result.returncode, 0, result.stderr)
                document = yaml.safe_load(result.stdout) if form == "yaml" else json.loads(result.stdout)
                expected = {"masses": records}
                if form != "yaml":
                    expected["v"] = 1
                self.assertEqual(document, expected)

    def test_unknown_later_mass_does_not_emit_partial_text(self) -> None:
        result = self.show(["advent-1", "not-a-held-mass"])
        self.assertEqual(result.returncode, 3)
        self.assertEqual(result.stdout, "")
        self.assertIn("not-a-held-mass", result.stderr)


if __name__ == "__main__":
    unittest.main()
