"""Explicit published Bible comparison with exact source coordinates and refusals."""
from __future__ import annotations

import json
import os
import subprocess
import unittest
from pathlib import Path

ROOT = Path(os.environ.get("TRIPTYCH_REVIEW_ROOT", Path(__file__).resolve().parents[2]))
MODULE_ROOT = Path(os.environ.get("TRIPTYCH_BIBLE_COMPARE_MODULE_ROOT", ROOT))


class ReaderBibleCompareTest(unittest.TestCase):
    def test_published_bibles_fixed_axes_source_coordinates_and_real_refusal(self) -> None:
        result = subprocess.run(
            ["node", "--test", str(MODULE_ROOT / "tools/tests/liturgy_reader_bible_compare.mjs")],
            cwd=ROOT, capture_output=True, text=True, timeout=30,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_browser_probe_parses(self) -> None:
        subprocess.run(
            ["node", "--check", str(MODULE_ROOT / "tools/tests/reader_bible_compare_chromium.mjs")],
            check=True, capture_output=True, text=True, timeout=15,
        )

    @unittest.skipUnless(os.environ.get("TRIPTYCH_BIBLE_COMPARE_CHROMIUM") == "1",
                         "set TRIPTYCH_BIBLE_COMPARE_CHROMIUM=1 for source-served Chromium")
    def test_bible_controls_identity_refusal_print_and_fail_closed_routes(self) -> None:
        result = subprocess.run(
            ["node", str(MODULE_ROOT / "tools/tests/reader_bible_compare_chromium.mjs")],
            cwd=ROOT, capture_output=True, text=True, timeout=120,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        report = json.loads(result.stdout.strip().splitlines()[-1])
        self.assertEqual(report["status"], "pass")
        self.assertEqual(report["checks"], 7)
        for diagnostic in ("consoleProblems", "failedRequests", "httpProblems"):
            self.assertEqual(report[diagnostic], [])


if __name__ == "__main__":
    unittest.main()
