"""Direct Study dock behavior through the real Day and Propers readers."""

from __future__ import annotations

import json
import os
import subprocess
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
PROBE = ROOT / "tools/tests/reader_study_direct_chromium.mjs"


class ReaderStudyDirectTest(unittest.TestCase):
    def test_browser_probe_parses(self) -> None:
        subprocess.run(["node", "--check", str(PROBE)], check=True,
                       capture_output=True, text=True, timeout=15)

    @unittest.skipUnless(os.environ.get("TRIPTYCH_STUDY_DIRECT_CHROMIUM") == "1",
                         "set TRIPTYCH_STUDY_DIRECT_CHROMIUM=1 for source-served Chromium")
    def test_direct_study_and_secondary_details_in_both_readers(self) -> None:
        result = subprocess.run(["node", str(PROBE)], cwd=ROOT, check=False,
                                capture_output=True, text=True, timeout=240)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        report = json.loads(result.stdout.strip().splitlines()[-1])
        self.assertEqual(report["status"], "pass")
        self.assertEqual(report["checks"], 12)
        self.assertEqual(report["consoleProblems"], [])
        self.assertEqual(report["failedRequests"], [])
        self.assertEqual(report["httpProblems"], [])


if __name__ == "__main__":
    unittest.main()
