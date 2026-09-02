#!/usr/bin/env python3
"""Keep ICEL chant artifact metadata conservative and surface-specific."""

from __future__ import annotations

import collections
import importlib.machinery
import importlib.util
import json
import sys
import tomllib
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SOURCE_READER = ROOT / "tools" / "source-reader"
ARTIFACT_ROOT = (
    ROOT
    / "src/sources/works/international-commission-on-english-in-the-liturgy"
    / "music-for-the-roman-missal/editions/2010-chants-web-2026-08-21/artifacts"
)
MISSAL_ROOT = ROOT / "src/sources/works/catholic-church/missale-romanum/editions"
ANTIPHONARY_ROOT = MISSAL_ROOT / "2010-english-icel-antiphonary"
CBCEW_ROOT = MISSAL_ROOT / "2011-english-cbcew-excerpts"
ANTIPHONARY_PROJECTION = (
    ROOT
    / "src/web/data/structure/sources/editions/catholic-church/missale-romanum"
    / "2010-2010-english-icel-antiphonary.json"
)
CBCEW_PROJECTION = (
    ROOT
    / "src/web/data/structure/sources/editions/catholic-church/missale-romanum"
    / "2011-2011-english-cbcew-excerpts.json"
)
TRANSLATION_LEDGER = (
    ROOT / "src/sources/inventories/postconciliar-proper-translations-v1.toml"
)
EXPECTED_CBCEW_PDFS = {
    "compare-2-peoples-pdf",
    "compare-3-peoples-pdf",
    "ep1-a4-pdf",
    "ep2-a4-pdf",
    "ep3-a4-pdf",
    "ep4-a4-pdf",
    "epc-composers-guide-pdf",
    "exsultet-longer-pdf",
    "exsultet-shorter-pdf",
    "initiation-pdf",
    "lords-entrance-pdf",
    "ly-composers-guide-pdf",
    "mca-pdf",
    "mcal-pdf",
    "mcar-pdf",
    "mcf-pdf",
    "mcfl-pdf",
    "mcfr-pdf",
    "mcn-pdf",
    "mcnl-pdf",
    "mcnr-pdf",
    "mcw-pdf",
    "mcwl-pdf",
    "mcwr-pdf",
    "om-a6-pdf",
    "om-composers-guide-pdf",
    "vigil-beginning-pdf",
    "word-bookmark-pdf",
}
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


def load_source_reader():
    loader = importlib.machinery.SourceFileLoader(
        "icel_artifact_source_reader_under_test", str(SOURCE_READER)
    )
    spec = importlib.util.spec_from_loader(
        "icel_artifact_source_reader_under_test", loader
    )
    module = importlib.util.module_from_spec(spec)
    sys.modules["icel_artifact_source_reader_under_test"] = module
    loader.exec_module(module)
    return module


SOURCE_READER_MODULE = load_source_reader()


class FakeRecord:
    def __init__(self, data: dict) -> None:
        self.data = data
        self.path = Path("/remote/source.pdf")


class FakeLibrary:
    def __init__(self, artifact: dict) -> None:
        self.records = {artifact["id"]: FakeRecord(artifact)}
        self.root = ROOT


def load_toml(path: Path) -> dict:
    with path.open("rb") as handle:
        return tomllib.load(handle)


def pdf_artifacts() -> list[tuple[Path, dict]]:
    paths = [
        ANTIPHONARY_ROOT / "artifacts/antiphonary-pdf/artifact.toml",
        *sorted((CBCEW_ROOT / "artifacts").glob("*/artifact.toml")),
    ]
    return [
        (path, record)
        for path in paths
        if (record := load_toml(path)).get("media_type") == "application/pdf"
    ]


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


class IcelAndCbcewPdfRightsTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.pdf_records = pdf_artifacts()

    def test_all_twenty_nine_exact_pdf_records_are_restricted(self) -> None:
        self.assertEqual(len(self.pdf_records), 29)
        self.assertEqual(
            {
                path.parent.name
                for path, _ in self.pdf_records
                if path.is_relative_to(CBCEW_ROOT)
            },
            EXPECTED_CBCEW_PDFS,
        )
        self.assertEqual(
            sum(path.is_relative_to(ANTIPHONARY_ROOT) for path, _ in self.pdf_records),
            1,
        )

        hashes = set()
        for path, record in self.pdf_records:
            with self.subTest(artifact=record.get("id")):
                self.assertEqual(record.get("artifact_type"), "publisher-issued-pdf")
                self.assertEqual(record.get("storage"), "remote")
                self.assertEqual(record.get("rights_status"), "restricted")
                self.assertFalse(record.get("indexable"))
                self.assertNotIn("path", record)
                self.assertTrue(str(record.get("source_url") or "").startswith("https://"))
                digest = str(record.get("sha256") or "")
                self.assertRegex(digest, r"^[0-9a-f]{64}$")
                self.assertNotIn(digest, hashes)
                hashes.add(digest)
                self.assertGreater(record.get("byte_size", 0), 0)
                self.assertGreater(record.get("page_count", 0), 0)
                basis = " ".join(str(record.get("rights_basis") or "").split())
                self.assertIn("rights_status = restricted", basis)
                self.assertIn("non-bundled live-site display", basis)
                self.assertNotIn("withholds nothing of the ICEL text", basis)
                self.assertNotIn("That disposes of the file", basis)

    def test_remote_pdf_cannot_itself_authorize_an_adversarial_body(self) -> None:
        for path, artifact in self.pdf_records:
            passage = {
                "id": "passage.adversarial",
                "artifact_id": artifact["id"],
                "locus": "adversarial.body",
                "text": "This protected body must not be projected.",
            }
            with self.subTest(artifact=artifact["id"]):
                reading = SOURCE_READER_MODULE.reading_of(
                    FakeLibrary(artifact), passage
                )
                self.assertFalse(reading["readable"], path)
                self.assertEqual(reading["withheld"], "rights", path)
                self.assertEqual(reading["rights"], "restricted", path)
                self.assertNotIn("text", reading, path)

    def test_text_permission_survives_as_a_distinct_ledger_fact(self) -> None:
        ledger = load_toml(TRANSLATION_LEDGER)
        source = next(
            row
            for row in ledger["sources"]
            if row.get("id") == "icel-antiphonary-2010"
        )
        self.assertEqual(source["rights"], "permission")
        self.assertEqual(
            source["source_id"],
            "edition.catholic-church.missale-romanum.2010-english-icel-antiphonary",
        )
        self.assertEqual(
            source["acknowledgement"],
            "Excerpts from the English translation of The Roman Missal © 2010, "
            "International Commission on English in the Liturgy Corporation. "
            "All rights reserved.",
        )

        antiphonary_passages = sorted(
            (ANTIPHONARY_ROOT / "passages").glob("*.toml")
        )
        self.assertEqual(len(antiphonary_passages), 5)
        for path in antiphonary_passages:
            with self.subTest(passage=path.stem):
                passage = load_toml(path)
                self.assertEqual(
                    passage["artifact_id"],
                    "artifact.catholic-church.missale-romanum."
                    "2010-english-icel-antiphonary.antiphonary-pdf",
                )
                self.assertIn("verified", passage["states"])

    def test_source_reader_projection_preserves_the_file_layer(self) -> None:
        antiphonary = json.loads(ANTIPHONARY_PROJECTION.read_text(encoding="utf-8"))
        cbcew = json.loads(CBCEW_PROJECTION.read_text(encoding="utf-8"))

        self.assertEqual(
            collections.Counter(row["rights"] for row in antiphonary["artifacts"]),
            collections.Counter({"restricted": 1}),
        )
        self.assertEqual(
            collections.Counter(row["rights"] for row in cbcew["artifacts"]),
            collections.Counter({"restricted": 28, "unresolved": 1}),
        )
        self.assertEqual(len(antiphonary["passages"]), 5)
        for passage in antiphonary["passages"]:
            with self.subTest(passage=passage["id"]):
                self.assertFalse(passage["readable"])
                self.assertEqual(passage["withheld"], "rights")
                self.assertEqual(passage["rights"], "restricted")
                self.assertNotIn("text", passage)

        self.assertEqual(len(cbcew["passages"]), 1)
        local_grant = cbcew["passages"][0]
        self.assertFalse(local_grant["readable"])
        self.assertEqual(local_grant["rights"], "unresolved")
        self.assertEqual(local_grant["withheld"], "rights")


if __name__ == "__main__":
    unittest.main()
