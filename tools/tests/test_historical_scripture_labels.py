"""Historical Scripture bodies preserve their source grade and Bible distinction."""
import json
from pathlib import Path
import subprocess
import unittest

from tools.tests._product_data import browser_data_root

ROOT = Path(__file__).resolve().parents[2]


class HistoricalScriptureLabels(unittest.TestCase):
    def test_actual_admitted_bodies_and_source_grade_controls(self):
        done = subprocess.run(["node", str(ROOT / "tools/tests/historical_scripture_labels.mjs"),
                               str(ROOT), str(browser_data_root(ROOT))],
                              capture_output=True, text=True, timeout=60)
        self.assertEqual(done.returncode, 0, done.stdout + done.stderr)
        report = json.loads(done.stdout)
        self.assertEqual(report["status"], "pass")
        self.assertEqual(len(report["presentations"]), 4)
        self.assertEqual(report["latinNoBody"], 2)
        self.assertEqual(len(report["gradeControls"]), 8)
        # 2026-11-13: the canonical Christmas antiphon English stays withheld;
        # the presentations above use synthetic, never-published words.
        self.assertEqual(report["canonicalWithheld"],
                         ["christmas-december-30", "christmas-december-31"])
