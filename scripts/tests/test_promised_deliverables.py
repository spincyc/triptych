#!/usr/bin/env python3
"""Regression tests for the promised-deliverable completion gate."""

from __future__ import annotations

import subprocess
import tempfile
import textwrap
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
CHECKER = ROOT / "tools/lib/check-promised-deliverables"


class PromisedDeliverableTests(unittest.TestCase):
    def run_checker(self, text: str, *arguments: str) -> subprocess.CompletedProcess[str]:
        with tempfile.NamedTemporaryFile("w", suffix=".toml", delete=False) as stream:
            stream.write(textwrap.dedent(text))
            ledger = Path(stream.name)
        try:
            return subprocess.run(
                [str(CHECKER), "--ledger", str(ledger), *arguments],
                cwd=ROOT,
                capture_output=True,
                text=True,
            )
        finally:
            ledger.unlink()

    def test_repository_ledger_is_valid(self) -> None:
        result = subprocess.run(
            [str(CHECKER)], cwd=ROOT, capture_output=True, text=True
        )
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_complete_rejects_open_requirement(self) -> None:
        result = self.run_checker(
            """
            schema_version = 1
            [[deliverables]]
            id = "demo"
            owner = "guidance"
            promise = "Finish the demo."
            state = "complete"
              [[deliverables.requirements]]
              id = "review"
              criterion = "Review it."
              status = "open"
              evidence = ["guidance/editorial.md"]
            """
        )
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("complete state has unmet requirements", result.stderr)

    def test_pass_rejects_missing_evidence(self) -> None:
        result = self.run_checker(
            """
            schema_version = 1
            [[deliverables]]
            id = "demo"
            owner = "guidance"
            promise = "Finish the demo."
            state = "candidate"
              [[deliverables.requirements]]
              id = "review"
              criterion = "Review it."
              status = "pass"
              check = "path_exists"
              evidence = ["does-not-exist"]
            """
        )
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("missing evidence", result.stderr)

    def test_require_complete_rejects_candidate(self) -> None:
        result = self.run_checker(
            """
            schema_version = 1
            [[deliverables]]
            id = "demo"
            owner = "guidance"
            promise = "Finish the demo."
            state = "candidate"
              [[deliverables.requirements]]
              id = "review"
              criterion = "Review it."
              status = "pass"
              check = "path_exists"
              evidence = ["guidance/editorial.md"]
            """,
            "--require-complete",
            "demo",
        )
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("completion required", result.stderr)


if __name__ == "__main__":
    unittest.main()
