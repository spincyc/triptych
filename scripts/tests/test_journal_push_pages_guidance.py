#!/usr/bin/env python3
"""Semantic regression checks for AI-guided push verification guidance."""

from pathlib import Path
import re
import unittest


ROOT = Path(__file__).resolve().parents[2]
JOURNAL_GUIDANCE = ROOT / ".journal" / "README.md"


class JournalPushPagesGuidanceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.guidance = " ".join(JOURNAL_GUIDANCE.read_text().split())

    def test_push_requires_exact_sha_pages_success_and_route_checks(self) -> None:
        self.assertRegex(
            self.guidance,
            re.compile(
                r"After every AI-guided push to `origin/main`.*?"
                r"head SHA exactly matches the pushed `main` tip.*?"
                r"terminal success state.*?"
                r"verify every affected production route",
            ),
        )

    def test_pending_or_failed_verification_remains_runnable_not_terminal(self) -> None:
        self.assertRegex(
            self.guidance,
            re.compile(
                r"pending or unsuccessful run, or a failed route check, "
                r"remains runnable work"
            ),
        )
        self.assertRegex(
            self.guidance,
            re.compile(
                r"Pages verification completes the push checkpoint; "
                r"it never supplies a stopping condition while any journal "
                r"task remains runnable"
            ),
        )


if __name__ == "__main__":
    unittest.main()
