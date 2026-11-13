"""Structural Ordinary markers do not claim that nonexistent words are missing."""
import os
from pathlib import Path
import subprocess
import unittest


ROOT = Path(os.environ.get("TRIPTYCH_REVIEW_ROOT", Path(__file__).resolve().parents[2]))


class OrdinaryStructuralAbsence(unittest.TestCase):
    def test_generated_structural_markers_and_real_absence_controls(self):
        result = subprocess.run(
            ["/usr/bin/node", str(Path(__file__).with_name("ordinary_structural_absence.mjs"))],
            cwd=ROOT, text=True, capture_output=True, check=False,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)


if __name__ == "__main__":
    unittest.main()
