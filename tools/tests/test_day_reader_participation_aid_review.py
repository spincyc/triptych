#!/usr/bin/env python3
"""Invariants for the dated, fail-closed Day-reader rights review."""

from __future__ import annotations

import datetime as dt
import re
import tomllib
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
RECORD = (
    ROOT
    / "src"
    / "sources"
    / "inventories"
    / "day-reader-participation-aid-review-v1.toml"
)
POLICY = ROOT / "guidance" / "liturgical-text-publication-policy.md"
GUIDELINES_ROOT = (
    ROOT
    / "src"
    / "sources"
    / "works"
    / "united-states-conference-of-catholic-bishops"
    / "guidelines-publication-liturgical-books"
)
GUIDELINES_EDITION = GUIDELINES_ROOT / "editions" / "2025-first-printing"
GUIDELINES_ARTIFACT = (
    GUIDELINES_EDITION / "artifacts" / "usccb-pdf-daab2999" / "artifact.toml"
)
GUIDELINES_SHA256 = (
    "daab29993c7764b9f5a8972629a9ee87e45a6fa0b62c9fe0318e85eca8ee4512"
)


class DayReaderParticipationAidReview(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.record = tomllib.loads(RECORD.read_text(encoding="utf-8"))

    def test_review_precedes_effective_date_and_remains_fail_closed(self) -> None:
        record = self.record
        recorded = dt.date.fromisoformat(record["recorded_on"])
        review = dt.date.fromisoformat(record["mandatory_review_on"])
        effective = dt.date.fromisoformat(record["guidelines_effective_on"])
        contingency = dt.date.fromisoformat(record["contingency_deadline"])

        self.assertLess(recorded, review)
        self.assertLess(review, effective)
        self.assertLess(contingency, effective)
        self.assertEqual(record["decision"]["state"], "fail-closed")
        self.assertTrue(
            record["decision"]["continues_after_guidelines_effective_date"]
        )
        self.assertIn("fail-closed", record["review"]["if_not_complete"])
        self.assertFalse(record["authorizes_release"])
        self.assertFalse(record["legal_advice"])

    def test_record_names_exact_surface_and_separate_authorities(self) -> None:
        surface = self.record["surface"]
        self.assertEqual(
            surface["entrypoints"],
            [
                "src/web/browser/liturgy/day.html",
                "src/web/browser/liturgy/day-reader.html",
            ],
        )
        self.assertEqual(surface["release_boundary"], "tools/public-alpha")
        self.assertIn("public Git object", surface["scope"])
        self.assertIn("participation aid", self.record["classification"]["status"])
        self.assertIn("not a legal", self.record["classification"]["decision_kind"])

        review = self.record["review"]
        self.assertIn("repository maintainer", review["repository_decision_authority"])
        for authority in ("USCCB Secretariat", "local Ordinary", "copyright holder"):
            self.assertIn(authority, review["external_authority"])

    def test_evidence_is_dated_and_non_assertions_reject_blanket_clearance(self) -> None:
        evidence = self.record["evidence"]
        self.assertGreaterEqual(len(evidence), 4)
        for item in evidence:
            self.assertEqual(item.get("retrieved_on", item.get("reviewed_on")), "2026-08-26")
            if "url" in item:
                self.assertRegex(item["sha256"], re.compile(r"^[0-9a-f]{64}$"))

        assertions = " ".join(self.record["non_assertions"]["statements"]).lower()
        self.assertIn("legally or canonically", assertions)
        self.assertIn("copyright license", assertions)
        self.assertIn("git payloads", assertions)
        decision_text = self.record["decision"]["holding"].lower()
        self.assertIn("not proof", decision_text)
        self.assertIn("blanket clearance", decision_text)

    def test_publication_policy_links_the_dated_action_record(self) -> None:
        policy = POLICY.read_text(encoding="utf-8")
        self.assertIn("day-reader-participation-aid-review-v1.toml", policy)
        self.assertIn("15 November", policy)
        self.assertIn("29 November 2026", policy)
        self.assertIn("gate stays\nclosed", policy)

    def test_pdf_evidence_is_bound_to_exact_restricted_source_records(self) -> None:
        evidence = next(
            item
            for item in self.record["evidence"]
            if item.get("sha256") == GUIDELINES_SHA256
        )
        self.assertEqual(
            evidence["work_id"],
            "work.united-states-conference-of-catholic-bishops."
            "guidelines-publication-liturgical-books",
        )
        self.assertEqual(
            evidence["edition_id"],
            "edition.united-states-conference-of-catholic-bishops."
            "guidelines-publication-liturgical-books.2025-first-printing",
        )

        artifact = tomllib.loads(GUIDELINES_ARTIFACT.read_text(encoding="utf-8"))
        self.assertEqual(evidence["artifact_id"], artifact["id"])
        self.assertEqual(artifact["sha256"], GUIDELINES_SHA256)
        self.assertEqual(artifact["storage"], "restricted")
        self.assertEqual(artifact["rights_status"], "restricted")
        self.assertEqual(artifact["page_count"], 51)
        self.assertNotIn("path", artifact)
        self.assertEqual(
            [path.name for path in GUIDELINES_ARTIFACT.parent.iterdir()],
            ["artifact.toml"],
        )

        passages = {}
        for path in sorted((GUIDELINES_EDITION / "passages").glob("*.toml")):
            passage = tomllib.loads(path.read_text(encoding="utf-8"))
            passages[passage["id"]] = passage
        self.assertEqual(set(evidence["passage_ids"]), set(passages))
        for passage_id in evidence["passage_ids"]:
            passage = passages[passage_id]
            self.assertEqual(passage["artifact_id"], artifact["id"])
            self.assertEqual(passage["artifact_sha256"], GUIDELINES_SHA256)
            self.assertEqual(
                passage["states"],
                ["cataloged", "acquired", "inspected", "verified"],
            )
            self.assertEqual(passage["verified_on"], "2026-08-26")


if __name__ == "__main__":
    unittest.main()
