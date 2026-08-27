#!/usr/bin/env python3
"""Keep ICEL chant artifact metadata conservative and surface-specific."""

from __future__ import annotations

import collections
import tomllib
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
ARTIFACT_ROOT = (
    ROOT
    / "src/sources/works/international-commission-on-english-in-the-liturgy"
    / "music-for-the-roman-missal/editions/2010-chants-web-2026-08-21/artifacts"
)
EXPECTED_CENSUS = collections.Counter(
    {
        ("remote", "restricted"): 187,
        ("restricted", "restricted"): 17,
        ("remote", "unresolved"): 1,
    }
)
EXPECTED_PUBLISHER_LEAF_PDFS = 170
EXPECTED_REGISTERED_PARENT_PDFS = 17
EXPECTED_RESTRICTED_DERIVATIVES = 17
EXPECTED_REMOTE_INDEXES = 1
REQUIRED_BASIS_STATEMENTS = (
    "does not clear any liturgical text or publisher file for publication from the current tree",
    "public Git repository, source browser, static data bundle, CLI, PDF, or download surface",
    "possible future qualifying non-bundled live-site display route only",
    "Every applicable fact and condition remains to be verified",
    "neither identity is a permission to republish those bytes",
)
OBSOLETE_OFFERS = (
    "publishable under the clause",
    "withholds nothing of the text",
    "That disposes of the file",
    "This project is such a site",
    "The grant therefore reaches",
)


class IcelArtifactRightsTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.records = [
            (path, tomllib.loads(path.read_text(encoding="utf-8")))
            for path in sorted(ARTIFACT_ROOT.glob("*/artifact.toml"))
        ]

    def test_artifact_census_and_non_distributable_storage_are_fixed(self) -> None:
        census = collections.Counter(
            (record.get("storage"), record.get("rights_status"))
            for _, record in self.records
        )
        self.assertEqual(census, EXPECTED_CENSUS)

        derivatives = [
            (path, record)
            for path, record in self.records
            if record.get("storage") == "restricted"
        ]
        parent_ids = {record.get("derived_from") for _, record in derivatives}
        parents = [
            (path, record)
            for path, record in self.records
            if record.get("id") in parent_ids
        ]
        publisher_leaf_pdfs = [
            (path, record)
            for path, record in self.records
            if record.get("artifact_type") == "publisher-issued-pdf"
            and record.get("id") not in parent_ids
        ]
        remote_indexes = [
            (path, record)
            for path, record in self.records
            if record.get("rights_status") == "unresolved"
        ]

        self.assertEqual(len(publisher_leaf_pdfs), EXPECTED_PUBLISHER_LEAF_PDFS)
        self.assertEqual(len(parents), EXPECTED_REGISTERED_PARENT_PDFS)
        self.assertEqual(len(derivatives), EXPECTED_RESTRICTED_DERIVATIVES)
        self.assertEqual(len(remote_indexes), EXPECTED_REMOTE_INDEXES)
        self.assertNotIn(None, parent_ids)
        self.assertEqual({record["id"] for _, record in parents}, parent_ids)

        classified_ids = collections.Counter(
            record["id"]
            for category in (
                publisher_leaf_pdfs,
                parents,
                derivatives,
                remote_indexes,
            )
            for _, record in category
        )
        all_ids = collections.Counter(record["id"] for _, record in self.records)
        self.assertEqual(
            classified_ids,
            all_ids,
            "every chant-edition artifact must belong to exactly one census category",
        )
        self.assertTrue(
            all(count == 1 for count in classified_ids.values()),
            "census categories must neither omit nor double-count artifacts",
        )

        for path, record in publisher_leaf_pdfs + parents + remote_indexes:
            with self.subTest(artifact=record.get("id")):
                self.assertFalse(record.get("indexable"), path)
                self.assertNotIn("path", record, path)
                self.assertTrue(record.get("id"), path)
                self.assertTrue(record.get("source_url"), path)
                self.assertRegex(str(record.get("sha256") or ""), r"^[0-9a-f]{64}$")
                self.assertGreater(record.get("byte_size", 0), 0, path)

        for path, record in derivatives:
            with self.subTest(derivative=record.get("id")):
                self.assertFalse(record.get("indexable"), path)
                self.assertNotIn("path", record, path)
                self.assertNotIn("source_url", record, path)
                self.assertNotIn("page_count", record, path)
                self.assertIn(record.get("derived_from"), parent_ids, path)
                self.assertTrue(record.get("transformation"), path)
                self.assertRegex(str(record.get("sha256") or ""), r"^[0-9a-f]{64}$")
                self.assertGreater(record.get("byte_size", 0), 0, path)

    def test_restricted_records_share_one_conditional_non_offer(self) -> None:
        restricted_records = [
            record
            for _, record in self.records
            if record.get("rights_status") == "restricted"
        ]
        self.assertEqual(len(restricted_records), 204)

        bases = {record.get("rights_basis") for record in restricted_records}
        self.assertEqual(len(bases), 1, "restricted artifacts must share one disposition")
        basis = " ".join((bases.pop() or "").split())
        for statement in REQUIRED_BASIS_STATEMENTS:
            self.assertIn(statement, basis)

        combined_metadata = " ".join(
            "\n".join(
                f"{record.get('rights_basis', '')}\n{record.get('notes', '')}"
                for _, record in self.records
            ).split()
        )
        for obsolete in OBSOLETE_OFFERS:
            self.assertNotIn(obsolete, combined_metadata)


if __name__ == "__main__":
    unittest.main()
