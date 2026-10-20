"""Source-owned Ordinary turns retain native copy and accessible note semantics."""

from __future__ import annotations

import json
import os
import subprocess
import unittest
from pathlib import Path


ROOT = Path(os.environ.get("TRIPTYCH_REVIEW_ROOT", Path(__file__).resolve().parents[2]))
PROBE = Path(__file__).with_name("reader_dialogue_chromium.mjs")


class ReaderDialogueBrowserTest(unittest.TestCase):
    def test_browser_probe_parses(self) -> None:
        subprocess.run(["node", "--check", str(PROBE)], check=True,
                       capture_output=True, text=True, timeout=15)

    @unittest.skipUnless(os.environ.get("TRIPTYCH_DIALOGUE_CHROMIUM") == "1",
                         "set TRIPTYCH_DIALOGUE_CHROMIUM=1 for source-served Chromium")
    def test_divided_turns_and_source_glosses_in_chromium(self) -> None:
        result = subprocess.run(["node", str(PROBE)], cwd=ROOT, check=False,
                                capture_output=True, text=True, timeout=360)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        report = json.loads(result.stdout.strip().splitlines()[-1])
        self.assertEqual(report["status"], "pass")
        self.assertEqual(report["checks"], 36)
        for diagnostic in ("failures", "consoleProblems", "failedRequests",
                           "httpProblems", "expectedHttpProblems"):
            self.assertEqual(report[diagnostic], [])


if __name__ == "__main__":
    unittest.main()
