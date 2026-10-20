"""Named Latin Bible accompaniment over independently addressed citation fragments."""
from __future__ import annotations

import json
import os
import subprocess
import unittest
from pathlib import Path

ROOT = Path(os.environ.get("TRIPTYCH_REVIEW_ROOT", Path(__file__).resolve().parents[2]))
MODULE_ROOT = Path(os.environ.get("TRIPTYCH_SCRIPTURE_MODULE_ROOT", ROOT))


class ReaderScriptureCompanionTest(unittest.TestCase):
    def test_named_companion_state_fragments_refusals_and_default_parity(self) -> None:
        result = subprocess.run(
            ["node", "--test", str(MODULE_ROOT / "tools/tests/liturgy_reader_scripture_companion.mjs")],
            cwd=ROOT, capture_output=True, text=True, timeout=30,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_browser_probe_parses(self) -> None:
        subprocess.run(
            ["node", "--check", str(MODULE_ROOT / "tools/tests/reader_scripture_companion_chromium.mjs")],
            check=True, capture_output=True, text=True, timeout=15,
        )

    @unittest.skipUnless(os.environ.get("TRIPTYCH_SCRIPTURE_COMPANION_CHROMIUM") == "1",
                         "set TRIPTYCH_SCRIPTURE_COMPANION_CHROMIUM=1 for source-served Chromium")
    def test_both_entrances_pairs_compare_shared_scripture_and_print(self) -> None:
        result = subprocess.run(
            ["node", str(MODULE_ROOT / "tools/tests/reader_scripture_companion_chromium.mjs")],
            cwd=ROOT, capture_output=True, text=True, timeout=120,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        report = json.loads(result.stdout.strip().splitlines()[-1])
        self.assertEqual(report["status"], "pass")
        self.assertEqual(report["checks"], 10)
        for diagnostic in ("consoleProblems", "failedRequests", "httpProblems"):
            self.assertEqual(report[diagnostic], [])


if __name__ == "__main__":
    unittest.main()
