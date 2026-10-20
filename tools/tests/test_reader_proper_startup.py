"""Early bounded response hints, without a second reader data-root policy."""
from __future__ import annotations

import json
import os
import shutil
import subprocess
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TESTS = ROOT / "tools/tests"


class ReaderProperStartupTest(unittest.TestCase):
    def test_every_reader_starts_payload_hints_immediately_after_shared_core(self) -> None:
        core = '<script src="../shared/browser-core.js"></script>'
        payload = '<script src="reader-proper-payload.js"></script>'
        for name in ("day.html", "day-reader.html", "index.html", "propers-reader.html"):
            with self.subTest(page=name):
                html = (ROOT / "src/web/browser/liturgy" / name).read_text(encoding="utf-8")
                self.assertEqual(html.count(payload), 1)
                self.assertIn(core + "\n" + payload, html)
                self.assertIn('data-reader-shell data-entrance=', html)

    def test_guard_contract(self) -> None:
        result = subprocess.run(["node", "--test", str(TESTS / "reader_proper_startup.mjs")],
                                cwd=ROOT, capture_output=True, text=True, timeout=30)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    @unittest.skipUnless(os.environ.get("TRIPTYCH_PROPER_STARTUP_CHROMIUM") == "1" and
                         shutil.which("chromium") and shutil.which("chromedriver"),
                         "set TRIPTYCH_PROPER_STARTUP_CHROMIUM=1 with Chromium and ChromeDriver")
    def test_real_chromium_reuses_hints_and_preserves_split_fallback(self) -> None:
        result = subprocess.run(["node", str(TESTS / "reader_proper_startup_chromium.mjs")],
                                cwd=ROOT, capture_output=True, text=True, timeout=240)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        report = json.loads(result.stdout.strip().splitlines()[-1])
        self.assertEqual(report, {"status": "pass", "checks": 9})


if __name__ == "__main__":
    unittest.main()
