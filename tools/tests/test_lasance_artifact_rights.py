"""Fail closed if excluded Lasance insert pages return to tracked bytes."""

from __future__ import annotations

import hashlib
import tomllib
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
ARTIFACT_DIR = (
    ROOT
    / "src/sources/works/francis-xavier-lasance/the-new-roman-missal/editions"
    / "benziger-revised-1945/artifacts/new-roman-missal-text-80b34759"
)
MANIFEST = ARTIFACT_DIR / "artifact.toml"
PAYLOAD = ARTIFACT_DIR / "new-roman-missal-text.txt"
THIRD_PARTY = ROOT / "THIRD_PARTY.md"
MISSAL_GUIDANCE = ROOT / "guidance" / "missals.md"


class LasanceTrackedArtifactRightsTests(unittest.TestCase):
    def test_content_address_and_integrity_are_exact(self) -> None:
        artifact = tomllib.loads(MANIFEST.read_text(encoding="utf-8"))
        payload = PAYLOAD.read_bytes()
        digest = hashlib.sha256(payload).hexdigest()

        self.assertEqual(
            digest,
            "80b34759fb18ec60f6205460c2ac24dc9e4a861938a94ef1f8e04a08a398ac9a",
        )
        self.assertEqual(artifact["sha256"], digest)
        self.assertTrue(artifact["id"].endswith(digest[:8]))
        self.assertEqual(len(payload), 4_349_573)
        self.assertEqual(artifact["byte_size"], len(payload))
        self.assertEqual(payload.count(b"\n"), 197_573)

    def test_both_unestablished_insert_ranges_are_absent(self) -> None:
        artifact = tomllib.loads(MANIFEST.read_text(encoding="utf-8"))
        payload = PAYLOAD.read_text(encoding="utf-8")
        stripped_lines = {line.strip() for line in payload.splitlines()}

        # The OCR corrupts the printed 1302b page marker as 1802b. All four
        # exact page markers and the opening prose before 1302a must stay out.
        self.assertTrue(
            {"1302a", "1302b", "1802b", "1302c", "1302d"}.isdisjoint(
                stripped_lines
            )
        )
        self.assertNotIn("If a Commemoration is to be", payload)
        for pages in ("1298a-1298n", "1302a-1302d"):
            self.assertIn(pages, artifact["rights_basis"])
            self.assertIn(pages, artifact["transformation"])

    def test_superseded_content_address_is_gone(self) -> None:
        superseded = ARTIFACT_DIR.with_name("new-roman-missal-text-deb5d167")
        self.assertFalse((superseded / "artifact.toml").exists())
        self.assertFalse((superseded / "new-roman-missal-text.txt").exists())

    def test_repository_discloses_both_exclusions_and_residual_history(
        self,
    ) -> None:
        third_party = THIRD_PARTY.read_text(encoding="utf-8")
        guidance = MISSAL_GUIDANCE.read_text(encoding="utf-8")

        for pages in ("1298a--1298n", "1302a--1302d"):
            self.assertIn(pages, third_party)
        self.assertIn("Two exclusions and one trap", guidance)
        self.assertIn("pages 1302a–1302d", guidance)
        self.assertIn("thirty-two oration entries", third_party)
        self.assertIn("only the Collect on ordinary printed p.", guidance)
        self.assertIn("1302 is positive", guidance)
        self.assertIn("the five readings whose generic loci", guidance)
        self.assertIn("the witness translates `beatum`", guidance)
        self.assertIn(
            "6 admissible + 1 withdrawn + 14 excluded + 4 open",
            guidance,
        )
        for document in (third_party, guidance):
            self.assertIn("maintainer", document)
            self.assertIn("counsel", document)
            self.assertIn("history", document)


if __name__ == "__main__":
    unittest.main()
