"""Shared mode radiogroup loading and optional real-keyboard behavior."""

from __future__ import annotations

import json
import os
import subprocess
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
LITURGY = ROOT / "src/web/browser/liturgy"
PROBE = ROOT / "tools/tests/reader_mode_keyboard_chromium.mjs"


class ReaderModeKeyboardTest(unittest.TestCase):
    def test_both_readers_load_the_shared_keyboard_before_the_controller(self) -> None:
        for page, controller in (("day.html", "day-reader.js"),
                                 ("index.html", "propers-reader.js")):
            with self.subTest(page=page):
                html = (LITURGY / page).read_text(encoding="utf-8")
                self.assertEqual(html.count('src="reader-mode-keyboard.js"'), 1)
                self.assertLess(html.index('src="reader-shell.js"'),
                                html.index('src="reader-mode-keyboard.js"'))
                self.assertLess(html.index('src="reader-mode-keyboard.js"'),
                                html.index(f'src="{controller}"'))
                self.assertEqual(html.count('role="radiogroup"'), 1)
                self.assertEqual(html.count('role="radio"'), 4)

    def test_shared_module_and_probe_parse(self) -> None:
        for path in (LITURGY / "reader-mode-keyboard.js", PROBE):
            with self.subTest(path=path.name):
                subprocess.run(["node", "--check", str(path)], check=True,
                               capture_output=True, text=True, timeout=15)

    @unittest.skipUnless(os.environ.get("TRIPTYCH_MODE_KEYBOARD_CHROMIUM") == "1",
                         "set TRIPTYCH_MODE_KEYBOARD_CHROMIUM=1 for source-served Chromium")
    def test_both_readers_in_real_chromium(self) -> None:
        result = subprocess.run(["node", str(PROBE)], cwd=ROOT, check=False,
                                capture_output=True, text=True, timeout=240)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        report = json.loads(result.stdout.strip().splitlines()[-1])
        self.assertEqual(report["status"], "pass")
        self.assertEqual(report["checks"], 18)


if __name__ == "__main__":
    unittest.main()
