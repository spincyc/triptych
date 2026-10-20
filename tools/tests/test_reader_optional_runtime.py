"""Ordinary code loads for authoritative state without regressing eager readers."""

from __future__ import annotations

import json
import os
import subprocess
import unittest
from pathlib import Path


ROOT = Path(os.environ.get("TRIPTYCH_REVIEW_ROOT", Path(__file__).resolve().parents[2]))
PROBE = Path(__file__).with_name("reader_optional_runtime_chromium.mjs")


class ReaderOptionalRuntimeTest(unittest.TestCase):
    def test_browser_probe_parses(self) -> None:
        subprocess.run(["node", "--check", str(PROBE)], check=True,
                       capture_output=True, text=True, timeout=15)

    @unittest.skipUnless(os.environ.get("TRIPTYCH_OPTIONAL_RUNTIME_CHROMIUM") == "1",
                         "set TRIPTYCH_OPTIONAL_RUNTIME_CHROMIUM=1 for source-served Chromium")
    def test_lazy_ordinary_preserves_selection_and_render_ownership(self) -> None:
        result = subprocess.run(["node", str(PROBE)], cwd=ROOT, check=False,
                                capture_output=True, text=True, timeout=120)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        report = json.loads(result.stdout.strip().splitlines()[-1])
        self.assertEqual(report["status"], "pass")
        self.assertEqual(report["checks"], 11)
        for diagnostic in ("consoleProblems", "failedRequests", "httpProblems"):
            self.assertEqual(report[diagnostic], [])
        self.assertEqual(report["expectedHttpProblems"], [
            {"status": 404, "path": "/src/web/browser/liturgy/day.js"},
            {"status": 404, "path": "/src/web/browser/liturgy/day.js"},
        ])


if __name__ == "__main__":
    unittest.main()
