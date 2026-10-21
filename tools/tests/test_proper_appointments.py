#!/usr/bin/env python3
"""Source-owned Proper applicability, identity and reader/CLI regressions."""
import json
import shutil
import subprocess
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

class ProperAppointmentTests(unittest.TestCase):
    def run_node(self, name):
        node = shutil.which("node")
        if node is None:
            self.skipTest("node is not installed")
        result = subprocess.run(
            [node, str(ROOT / "tools/tests" / name)],
            cwd=ROOT, capture_output=True, text=True, check=False)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        record = json.loads(result.stdout)
        self.assertEqual(record["status"], "pass")
        self.assertEqual(record["groups"], len(record["checks"]))

    def test_source_owned_appointments_and_choices(self):
        self.run_node("test_proper_appointments.cjs")

    def test_native_proper_choice_controls_and_navigation(self):
        self.run_node("test_proper_choice_controls.cjs")

if __name__ == "__main__":
    unittest.main()
