"""Held Propers lectionary-cycle comparison contract and real-browser controls."""

from __future__ import annotations

import json
import os
import subprocess
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


class ReaderCycleCompareTest(unittest.TestCase):
    def test_cycle_contract_and_source_selections(self) -> None:
        result = subprocess.run(
            ["node", "--test", str(ROOT / "tools/tests/liturgy_reader_cycle_compare.mjs")],
            cwd=ROOT, capture_output=True, text=True, timeout=30,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_browser_probe_parses(self) -> None:
        subprocess.run(
            ["node", "--check", str(ROOT / "tools/tests/reader_cycle_compare_chromium.mjs")],
            check=True, capture_output=True, text=True, timeout=15,
        )

    @unittest.skipUnless(os.environ.get("TRIPTYCH_CYCLE_COMPARE_CHROMIUM") == "1",
                         "set TRIPTYCH_CYCLE_COMPARE_CHROMIUM=1 for source-served Chromium")
    def test_cycle_controls_and_fail_closed_routes(self) -> None:
        result = subprocess.run(
            ["node", str(ROOT / "tools/tests/reader_cycle_compare_chromium.mjs")],
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
