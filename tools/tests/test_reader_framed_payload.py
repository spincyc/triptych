"""The existing exact-Mass split preserves 1962 Ordinary seating and source claims."""
from __future__ import annotations

import os
import subprocess
import unittest
from pathlib import Path

ROOT = Path(os.environ.get("TRIPTYCH_REVIEW_ROOT", Path(__file__).resolve().parents[2]))
PROBE = Path(__file__).with_name("reader_framed_payload.mjs")


class ReaderFramedPayloadTest(unittest.TestCase):
    def test_framed_source_parity_and_fallbacks(self) -> None:
        result = subprocess.run(["node", "--test", str(PROBE)], cwd=ROOT,
                                capture_output=True, text=True, timeout=60)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)


if __name__ == "__main__":
    unittest.main()
