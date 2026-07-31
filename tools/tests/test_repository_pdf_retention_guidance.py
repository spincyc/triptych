#!/usr/bin/env python3
"""Guard the installed-PDF retention boundary in canonical guidance."""

from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[2]


class RepositoryPdfRetentionGuidanceTests(unittest.TestCase):
  def test_installed_pdfs_are_historical_release_artifacts(self) -> None:
    guidance = (ROOT / "guidance/repository.md").read_text(encoding="utf-8")

    self.assertIn(
        "Installed PDFs under `pdf/` are tracked release artifacts retained through\n"
        "ordinary Git history.",
        guidance,
    )
    self.assertIn(
        "Their reproducibility does not make them disposable\n"
        "intermediates or authorize rewriting history to remove prior releases.",
        guidance,
    )
    self.assertIn(
        "Moving\n"
        "release artifacts to external storage requires a separately designed and\n"
        "authorized migration",
        guidance,
    )


if __name__ == "__main__":
  unittest.main()
