"""Bounded Latin accompaniment for prayer and Missal bodies, with explicit gaps."""

from __future__ import annotations

import json
import os
import subprocess
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


class ReaderLatinAccompanimentTest(unittest.TestCase):
    def test_state_source_and_rendering_contract(self) -> None:
        result = subprocess.run(
            ["node", "--test", str(ROOT / "tools/tests/liturgy_reader_latin_accompaniment.mjs")],
            cwd=ROOT, capture_output=True, text=True, timeout=30,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_browser_probe_parses(self) -> None:
        subprocess.run(
            ["node", "--check", str(ROOT / "tools/tests/reader_latin_accompaniment_chromium.mjs")],
            check=True, capture_output=True, text=True, timeout=15,
        )

    @unittest.skipUnless(os.environ.get("TRIPTYCH_LATIN_ACCOMPANIMENT_CHROMIUM") == "1",
                         "set TRIPTYCH_LATIN_ACCOMPANIMENT_CHROMIUM=1 for source-served Chromium")
    def test_source_served_pairs_navigation_and_print(self) -> None:
        result = subprocess.run(
            ["node", str(ROOT / "tools/tests/reader_latin_accompaniment_chromium.mjs")],
            cwd=ROOT, capture_output=True, text=True, timeout=120,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        report = json.loads(result.stdout.strip().splitlines()[-1])
        self.assertEqual(report["status"], "pass")
        self.assertEqual(report["checks"], 8)
        for diagnostic in ("consoleProblems", "failedRequests", "httpProblems"):
            self.assertEqual(report[diagnostic], [])


if __name__ == "__main__":
    unittest.main()
