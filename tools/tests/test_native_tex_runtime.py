"""Execute native browser compiler transport and cache regressions under Node."""

import os
import shutil
import subprocess
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


class NativeTeXRuntimeTests(unittest.TestCase):
    def test_native_runtime(self):
        node = shutil.which("node")
        if node is None:
            candidate = Path.home() / ".local/bin/node"
            if os.access(candidate, os.X_OK):
                node = str(candidate)
        if node is None:
            self.skipTest("node is not installed")
        result = subprocess.run(
            [node, "--test", "tools/tests/native_tex_runtime.mjs"],
            cwd=ROOT, capture_output=True, text=True, timeout=30,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)


if __name__ == "__main__":
    unittest.main()
