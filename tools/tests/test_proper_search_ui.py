"""Run the dependency-free browser search matcher test in ordinary CI discovery."""
from __future__ import annotations

import subprocess
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


class ProperSearchUiTests(unittest.TestCase):
    def test_generated_indexes_match_the_browser_search_contract(self) -> None:
        result = subprocess.run(
            ["node", str(ROOT / "tools/tests/test_proper_search_ui.mjs")],
            cwd=ROOT, text=True, capture_output=True, check=False,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)


if __name__ == "__main__":
    unittest.main()
