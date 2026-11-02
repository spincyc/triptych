"""The parallel runner preserves discovery's sibling imports and result reports."""

from __future__ import annotations

import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[2]


class TestRunnerTests(unittest.TestCase):
    def check_runner(self, jobs: int) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            scripts = root / "scripts"
            scripts.mkdir()
            shutil.copyfile(ROOT / "scripts/run_tests.py", scripts / "run_tests.py")
            tests = root / "tools/tests"
            tests.mkdir(parents=True)
            (tests / "_runner_sibling.py").write_text("VALUE = 'sibling helper'\n")
            (tests / "test_selected.py").write_text(
                "import unittest\n"
                "from _runner_sibling import VALUE\n"
                "class SelectedTests(unittest.TestCase):\n"
                "    def test_pass(self):\n"
                "        self.assertEqual(VALUE, 'sibling helper')\n"
                "    def test_failure(self):\n"
                "        self.fail('visible assertion failure')\n"
                "    def test_error(self):\n"
                "        raise ValueError('visible test error')\n"
            )
            (tests / "test_unselected.py").write_text(
                "raise AssertionError('unselected module was imported')\n"
            )
            env = dict(os.environ)
            env.pop("PYTHONPATH", None)
            # The runner changes cwd; preserve a relative caller TMPDIR's meaning.
            env["TMPDIR"] = tempfile.gettempdir()
            result = subprocess.run(
                [sys.executable, str(scripts / "run_tests.py"),
                 f"-j{jobs}", "-p", "test_selected.py"],
                cwd=root, env=env, capture_output=True, text=True, timeout=30,
            )
            output = result.stdout + result.stderr
            self.assertEqual(result.returncode, 1, output)
            self.assertIn("Ran 3 tests", output)
            self.assertIn(f"(1 units across {jobs} workers, 0 skipped)", output)
            self.assertIn("FAILED (failures=1, errors=1)", output)
            self.assertIn("FAIL: test_failure", output)
            self.assertIn("AssertionError: visible assertion failure", output)
            self.assertIn("ERROR: test_error", output)
            self.assertIn("ValueError: visible test error", output)
            self.assertNotIn("unselected module was imported", output)
            self.assertNotIn("ModuleNotFoundError", output)

    def test_sibling_imports_and_results_in_serial_mode(self):
        self.check_runner(1)

    def test_sibling_imports_and_results_in_parallel_mode(self):
        self.check_runner(2)


if __name__ == "__main__":
    unittest.main()
