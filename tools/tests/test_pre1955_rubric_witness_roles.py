"""Keep the misdated MissaleRomanum1920 OCR in its evidentiary lane."""

from __future__ import annotations

import tomllib
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
INVENTORY = (
    ROOT / "src" / "sources" / "inventories" / "pre-1955-rubrics-sources-v1.toml"
)
ARTIFACT = (
    ROOT
    / "src"
    / "sources"
    / "works"
    / "catholic-church"
    / "missale-romanum"
    / "editions"
    / "vatican-typica-1920"
    / "artifacts"
    / "missale-romanum-1920-text-aa646196"
    / "artifact.toml"
)
SOURCE_ID = "missale-romanum-1920"
ROLE = "structural-search-locating-only"


def load(path: Path) -> dict:
    return tomllib.loads(path.read_text(encoding="utf-8"))


class Pre1955RubricWitnessRoleTest(unittest.TestCase):
    def setUp(self) -> None:
        self.inventory = load(INVENTORY)
        self.artifact = load(ARTIFACT)
        self.held = next(
            row for row in self.inventory["held"] if row["id"] == SOURCE_ID
        )

    def test_composite_derivative_cannot_masquerade_as_a_1920_printing(self):
        self.assertEqual(self.held["source_role"], ROLE)
        self.assertEqual(
            self.held["printing_identity"], "later-composite-not-1920-impression"
        )
        self.assertEqual(self.held["artifact"], self.artifact["id"])
        self.assertEqual(self.held["canonical_artifact_sha256"], self.artifact["sha256"])
        self.assertNotEqual(self.held["sha256"], self.artifact["sha256"])
        self.assertFalse(self.held["bytes_match_the_registered_artifact"])
        self.assertEqual(self.artifact["storage"], "remote")
        self.assertEqual(self.artifact["rights_status"], "unresolved")
        self.assertEqual(self.held["rights"], "unresolved")
        self.assertEqual(self.held["may_publish_text"], "unresolved")

    def test_every_finding_using_the_composite_declares_its_limited_role(self):
        findings = [
            row
            for row in self.inventory["findings"]
            if any(SOURCE_ID in locus for locus in row.get("loci", []))
        ]
        self.assertGreater(len(findings), 0)
        for finding in findings:
            with self.subTest(finding=finding["id"]):
                self.assertEqual(finding.get("source_roles", {}).get(SOURCE_ID), ROLE)


if __name__ == "__main__":
    unittest.main()
