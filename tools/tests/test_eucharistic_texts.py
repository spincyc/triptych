"""Publication and witness boundaries of the original-language adapters."""
from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import sys
import tempfile
from types import SimpleNamespace
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))
import _eucharistic_texts as texts


def sha(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def native_fixture(test, identifier="fixture-book", wording="Exact native fixture."):
    """Synthetic full two-page witness; never evidence of a historical book."""
    edition_id = "edition." + identifier
    test.record(edition_id, "edition", date="1200", language="la")
    scan = test.artifact("artifact." + identifier + ".scan", "Synthetic facsimile bytes.\n",
                         artifact_type="scan", edition_id=edition_id, page_count=2,
                         rights_status="public-domain", rights_basis="Test only", rights_jurisdiction="United States")
    evidence_id = "passage." + identifier + ".extent"
    test.record(evidence_id, "passage", edition_id=edition_id, artifact_id=scan["id"],
                states=["inspected"], locus="Synthetic title and two-page extent")
    evidence = [{"source_id": evidence_id, "locus": "Synthetic pages 1–2"}]
    book = {"schema_version": 1, "record_type": "eucharistic-native-book", "id": identifier,
            "title": "Synthetic book fixture", "extent_kind": "whole-book", "excluded_book_divisions": [], "scope": "Both pages of one synthetic native book",
            "transcribed_by": "fixture-transcriber", "stage_ids": ["fixture.first"],
            "catalogue_witness_ids": ["research:first"], "components": ["rubrics"], "languages": ["la"],
            "date": {"kind": "attestation", "label": "1200", "start_year": 1200, "end_year": 1200,
                     "evidence": evidence},
            "witnesses": [{"id": "copy", "edition_id": edition_id, "artifact_id": scan["id"],
                           "completeness_evidence": evidence, "scope_pages": [[1, 2]]}],
            "extent_path": texts.NATIVE_BOOK_DIRECTORY + "/support/" + identifier + "-extent.json",
            "collation_path": texts.NATIVE_BOOK_DIRECTORY + "/support/" + identifier + "-review.json", "units": []}
    extent = {"schema_version": 1, "record_type": "eucharistic-book-extent", "book_id": identifier,
              "title": "Synthetic extent", "status": "complete", "unresolved": [], "omitted": [], "expected_unit_ids": [], "pages": []}
    for index, body in enumerate((wording, "Second native fixture."), 1):
        unit_id = "unit.fixture." + str(index)
        artifact = test.artifact("artifact." + identifier + ".unit" + str(index), body + "\n",
                                 artifact_type="normalized-text", edition_id=edition_id,
                                 derived_from=scan["id"], transformation="Synthetic fixture only",
                                 rights_status="public-domain", rights_basis="Test only", rights_jurisdiction="United States")
        passage_id = "passage." + identifier + ".unit" + str(index)
        test.record(passage_id, "passage", edition_id=edition_id, artifact_id=artifact["id"],
                    artifact_sha256=artifact["sha256"], physical_line_ranges=[[1, 1]],
                    states=["verified"], verified_on="2026-10-17", locus=f"Synthetic page {index}")
        book["units"].append({"unit_id": unit_id, "native_path": ["native-division", "unit-" + str(index)],
                              "source_order": index, "language": "la", "component": "rubrics", "kind": "rubric",
                              "witness_id": "copy", "witness_pages": [[index, index]],
                              "passage_id": passage_id, "text_sha256": sha(body)})
        extent["expected_unit_ids"].append(unit_id)
        extent["pages"].append({"witness_id": "copy", "ranges": [[index, index]], "role": "text", "unit_ids": [unit_id]})
    review = {"schema_version": 1, "record_type": "eucharistic-book-collation", "book_id": identifier,
              "title": "Synthetic independent review", "status": "verified", "independent": True, "complete_extent_verified": True,
              "reviewer": "fixture-independent-reviewer", "checked_on": "2026-10-17",
              "witness_sha256": {"copy": scan["sha256"]},
              "unit_sha256": {unit["unit_id"]: unit["text_sha256"] for unit in book["units"]}}

    def save():
        path = test.root / texts.NATIVE_BOOK_DIRECTORY / (identifier + ".json")
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(book), encoding="utf-8")
        extent_path = test.root / book["extent_path"]
        extent_path.parent.mkdir(parents=True, exist_ok=True)
        extent_path.write_text(json.dumps(extent), encoding="utf-8")
        review["binding_sha256"] = sha(path.read_text())
        review["extent_sha256"] = sha(extent_path.read_text())
        (test.root / book["collation_path"]).write_text(json.dumps(review), encoding="utf-8")
    save()
    return book, extent, review, save


def segmented_native_fixture(test):
    """A complete two-page work inside a separately owned four-page volume."""
    book, extent, review, save = native_fixture(test)
    edition_id = book["witnesses"][0]["edition_id"]
    container_id = "edition.fixture-container"
    test.record(container_id, "edition", date="1200", language="la")
    scan = test.records["artifact.fixture-book.scan"].data
    scan.update(schema=2, edition_id=container_id, page_count=4)
    facsimile_segment = test.record("segment.fixture-book.facsimile", "segment", schema=2,
                                    edition_id=edition_id, artifact_id=scan["id"], artifact_sha256=scan["sha256"],
                                    segment_type="constituent-work", artifact_page_ranges=[[2, 3]],
                                    states=["verified"], verified_on="2026-10-17")
    witness = book["witnesses"][0]
    witness.update(segment_id=facsimile_segment["id"], scope_pages=[[2, 3]])
    evidence = test.records["passage.fixture-book.extent"].data
    evidence.pop("artifact_id")
    evidence.update(schema=2, segment_id=facsimile_segment["id"], artifact_sha256=scan["sha256"],
                    artifact_page_ranges=[[2, 3]])
    literal = test.artifact("artifact.fixture-container.text", "Other work before.\nExact native fixture.\nSecond native fixture.\nOther work after.\n",
                            edition_id=container_id, artifact_type="normalized-text", derived_from=scan["id"],
                            transformation="Synthetic normalized volume transcription; not historical evidence",
                            rights_status="public-domain", rights_basis="Test only", rights_jurisdiction="United States")
    literal_segment = test.record("segment.fixture-book.text", "segment", schema=2, edition_id=edition_id,
                                 artifact_id=literal["id"], artifact_sha256=literal["sha256"],
                                 segment_type="constituent-work", physical_line_ranges=[[2, 3]],
                                 states=["verified"], verified_on="2026-10-17")
    for index, unit in enumerate(book["units"], 2):
        passage = test.records[unit["passage_id"]].data
        passage.pop("artifact_id")
        passage.update(schema=2, segment_id=literal_segment["id"], artifact_sha256=literal["sha256"],
                       physical_line_ranges=[[index, index]])
        unit["witness_pages"] = [[index, index]]
        extent["pages"][index - 2]["ranges"] = [[index, index]]
    save()
    return book, extent, review, save


class NativeBookTests(unittest.TestCase):
    setUp = lambda self: AdapterBoundaryTests.setUp(self)
    record = lambda self, *args, **kwargs: AdapterBoundaryTests.record(self, *args, **kwargs)
    artifact = lambda self, *args, **kwargs: AdapterBoundaryTests.artifact(self, *args, **kwargs)
    load = lambda self, adapter="native-book:fixture-book": AdapterBoundaryTests.load(self, adapter)

    def test_complete_native_book_is_literal_reviewed_and_deterministic(self):
        native_fixture(self)
        result = self.load()
        self.assertEqual(result, self.load())
        self.assertTrue(result["scope"]["whole_book_complete"])
        self.assertEqual(2, result["scope"]["known_extent_pages"])
        self.assertEqual("Exact native fixture.", result["units"][0]["text"])
        self.assertEqual(["native-division", "unit-1"], result["units"][0]["native_path"])
        self.assertEqual(1200, result["historical_date"]["start_year"])

    def test_complete_segment_book_keeps_constituent_identity_and_container_census(self):
        segmented_native_fixture(self)
        result = self.load()
        self.assertEqual(result, self.load())
        self.assertTrue(result["scope"]["whole_book_complete"])
        self.assertTrue(result["scope"]["complete_declared_extent"])
        self.assertEqual(2, result["scope"]["known_extent_pages"])
        self.assertEqual(["Exact native fixture.", "Second native fixture."], [unit["text"] for unit in result["units"]])
        self.assertNotIn("Other work", json.dumps(result["units"]))
        unit = result["units"][0]
        self.assertEqual("edition.fixture-book", unit["text_edition_id"])
        self.assertEqual("segment.fixture-book.text", unit["source_segment_id"])
        self.assertEqual("artifact.fixture-container.text", unit["source_artifact_id"])
        sources = {row["id"]: row for row in result["sources"]}
        self.assertEqual("edition.fixture-container", sources["artifact.fixture-container.text"]["edition_id"])
        self.assertEqual("edition.fixture-container", sources["artifact.fixture-book.scan"]["edition_id"])
        self.assertEqual([[2, 3]], result["book_binding"]["witness_extents"][0]["artifact_page_ranges"])
        self.assertEqual("segment-artifact-page-ranges", result["book_binding"]["witness_extents"][0]["census_boundary"])
        self.assertIn("segment.fixture-book.facsimile", sources)
        self.assertIn("segment.fixture-book.text", sources)

    def test_segment_book_can_keep_direct_constituent_literal_passages(self):
        book, extent, review, save = segmented_native_fixture(self)
        for index, unit in enumerate(book["units"], 1):
            passage = self.records[unit["passage_id"]].data
            passage.pop("segment_id")
            artifact = self.records[f"artifact.fixture-book.unit{index}"].data
            artifact.pop("derived_from")  # Cross-edition byte derivation would be false.
            passage.update(schema=1, artifact_id=artifact["id"], artifact_sha256=artifact["sha256"], physical_line_ranges=[[1, 1]])
            unit.update(verified_against_artifact_id="artifact.fixture-book.scan",
                        verified_against_artifact_sha256=review["witness_sha256"]["copy"])
        save()
        self.assertEqual("Exact native fixture.", self.load()["units"][0]["text"])
        self.assertNotIn("source_segment_id", self.load()["units"][0])

    def test_segment_witness_requires_exact_edition_container_hash_and_page_bounds(self):
        book, extent, review, save = segmented_native_fixture(self)
        segment = self.records["segment.fixture-book.facsimile"].data
        alternative = self.artifact("artifact.fixture-container.other-scan", "Other synthetic copy.\n",
                                    edition_id="edition.fixture-container", artifact_type="scan", page_count=4)
        for field, value, message in (
                ("edition_id", "edition.fixture-container", "exact-edition constituent"),
                ("artifact_sha256", "0" * 64, "container artifact hash"),
                ("artifact_id", alternative["id"], "container artifact hash"),
                ("artifact_page_ranges", [[2, 5]], "range outside witness"),
                ("artifact_page_ranges", [[3, 3]], "scope extends outside"),
                ("states", ["cataloged"], "inspected exact-edition"),
                ("schema", 1, "inspected exact-edition")):
            with self.subTest(field=field):
                original = segment[field]
                try:
                    segment[field] = value
                    with self.assertRaisesRegex(texts.AdapterError, message):
                        self.load()
                finally:
                    segment[field] = original
        segment.update(artifact_id=alternative["id"], artifact_sha256=alternative["sha256"])
        with self.assertRaisesRegex(texts.AdapterError, "different container artifact"):
            self.load()

    def test_segment_whole_book_requires_verified_complete_segment_boundary(self):
        book, extent, review, save = segmented_native_fixture(self)
        segment = self.records["segment.fixture-book.facsimile"].data
        for field, value in (("states", ["inspected"]), ("verified_on", ""), ("segment_type", "excerpt")):
            with self.subTest(field=field):
                original = segment[field]
                try:
                    segment[field] = value
                    with self.assertRaisesRegex(texts.AdapterError, "verified constituent-work segment boundary"):
                        self.load()
                finally:
                    segment[field] = original
        book["witnesses"][0]["scope_pages"] = [[2, 2]]
        save()
        with self.assertRaisesRegex(texts.AdapterError, "every witness page in scope"):
            self.load()

    def test_inspected_segment_supports_a_complete_declared_constituent(self):
        book, extent, review, save = segmented_native_fixture(self)
        book.update(extent_kind="constituent", excluded_book_divisions=["Second synthetic division"])
        book["witnesses"][0]["scope_pages"] = [[2, 2]]
        book["units"].pop()
        extent["expected_unit_ids"].pop()
        extent["pages"][1].update(role="outside-constituent", unit_ids=[], description="Excluded second division")
        review["unit_sha256"].pop("unit.fixture.2")
        segment = self.records["segment.fixture-book.facsimile"].data
        segment.update(states=["inspected"])
        segment.pop("verified_on")
        save()
        result = self.load()
        self.assertTrue(result["scope"]["complete_declared_extent"])
        self.assertFalse(result["scope"]["whole_book_complete"])
        self.assertEqual(1, result["scope"]["known_extent_pages"])

    def test_segment_census_excludes_container_pages_and_requires_all_segment_pages(self):
        book, extent, review, save = segmented_native_fixture(self)
        extent["pages"].pop()
        save()
        with self.assertRaisesRegex(texts.AdapterError, "pages unaccounted"):
            self.load()
        extent["pages"].append({"witness_id": "copy", "ranges": [[3, 3]], "role": "text", "unit_ids": ["unit.fixture.2"]})
        for role in ("non-text", "outside-constituent"):
            with self.subTest(role=role):
                extent["pages"].append({"witness_id": "copy", "ranges": [[1, 1]], "role": role,
                                        "unit_ids": [], "description": "Other work in the container"})
                save()
                with self.assertRaisesRegex(texts.AdapterError, "account extends outside its controlling segment"):
                    self.load()
                extent["pages"].pop()
        book["units"][0]["witness_pages"] = [[1, 2]]
        save()
        with self.assertRaisesRegex(texts.AdapterError, "unit loci extend outside"):
            self.load()

    def test_segment_literal_requires_exact_edition_hash_and_single_controller(self):
        segmented_native_fixture(self)
        segment = self.records["segment.fixture-book.text"].data
        passage = self.records["passage.fixture-book.unit1"].data
        for record, field, value, message in (
                (segment, "edition_id", "edition.fixture-container", "exact-edition constituent"),
                (segment, "artifact_sha256", "0" * 64, "container artifact hash"),
                (segment, "physical_line_ranges", [[3, 3]], "lines extend outside"),
                (passage, "edition_id", "edition.fixture-container", "verified exact-edition literal"),
                (passage, "artifact_sha256", "0" * 64, "verified exact-edition literal"),
                (passage, "schema", 1, "exactly one schema-2 segment controller")):
            with self.subTest(field=field):
                original = record[field]
                try:
                    record[field] = value
                    with self.assertRaisesRegex(texts.AdapterError, message):
                        self.load()
                finally:
                    record[field] = original
        passage["artifact_id"] = "artifact.fixture-container.text"
        with self.assertRaisesRegex(texts.AdapterError, "exactly one schema-2 segment controller"):
            self.load()
        passage.pop("artifact_id")
        passage.pop("segment_id")
        with self.assertRaisesRegex(texts.AdapterError, "Unregistered source"):
            self.load()

    def test_segment_literal_rechecks_container_lineage_rights_and_physical_bounds(self):
        segmented_native_fixture(self)
        literal = self.records["artifact.fixture-container.text"].data
        for field, value, message in (("derived_from", None, "does not derive from its exact witness"),
                                      ("rights_status", "unresolved", "public-git publication basis"),
                                      ("rights_jurisdiction", "Elsewhere", "public-git publication basis")):
            with self.subTest(field=field):
                original = literal[field]
                try:
                    literal[field] = value
                    with self.assertRaisesRegex(texts.AdapterError, message):
                        self.load()
                finally:
                    literal[field] = original
        segment = self.records["segment.fixture-book.text"].data
        passage = self.records["passage.fixture-book.unit1"].data
        literal["page_count"] = 4
        segment["artifact_page_ranges"] = [[2, 3]]
        passage["artifact_page_ranges"] = [[1, 2]]
        with self.assertRaisesRegex(texts.AdapterError, "pages extend outside its controlling segment"):
            self.load()
        passage["artifact_page_ranges"] = [[2, 2]]
        self.assertEqual("Exact native fixture.", self.load()["units"][0]["text"])

    def test_segment_manifest_and_container_dependencies_are_pinned(self):
        segmented_native_fixture(self)
        result = self.load()
        inputs = {row["path"]: row for row in result["inputs"]}
        identities = ("segment.fixture-book.facsimile", "segment.fixture-book.text",
                      "edition.fixture-book", "edition.fixture-container", "artifact.fixture-book.scan", "artifact.fixture-container.text")
        for identity in identities:
            record = self.records[identity]
            relative = record.path.relative_to(self.root).as_posix()
            self.assertEqual(sha(record.path.read_text()), inputs[relative]["sha256"])
        record = self.records["segment.fixture-book.text"]
        record.path.write_text(record.path.read_text() + "\n")
        changed = {row["path"]: row for row in self.load()["inputs"]}
        relative = record.path.relative_to(self.root).as_posix()
        self.assertNotEqual(inputs[relative]["sha256"], changed[relative]["sha256"])
        literal = self.records["artifact.fixture-container.text"].data
        (self.root / literal["path"]).write_text("Changed volume bytes.\n")
        with self.assertRaisesRegex(texts.AdapterError, "Artifact hash mismatch"):
            self.load()

    def test_segment_book_passes_the_real_source_library_gate(self):
        segmented_native_fixture(self)
        (self.root / "src/gpt").mkdir(parents=True)
        used = {row["id"] for row in self.load()["sources"]}
        owners = {"edition.fixture-book": "fixture-book", "edition.fixture-container": "fixture-container"}
        for slug in owners.values():
            self.record("work." + slug, "work", schema=1, title="Synthetic " + slug,
                        responsible="Synthetic fixture only", work_type="test-fixture", languages=["la"])
            used.add("work." + slug)
        for identity in sorted(used):
            data = dict(self.records[identity].data)
            kind = data["record_type"]
            if kind == "work":
                directory = "src/sources/works/test/" + identity.removeprefix("work.")
                relative = directory + "/work.toml"
            else:
                slug = owners[identity if kind == "edition" else data["edition_id"]]
                directory = "src/sources/works/test/" + slug + "/editions/1200-fixture"
                if kind == "edition":
                    data.update(schema=1, work_id="work." + slug, title="Synthetic " + slug, publication="Test only")
                    relative = directory + "/edition.toml"
                elif kind == "artifact":
                    directory += "/artifacts/" + identity.removeprefix("artifact.")
                    payload = (self.root / data["path"]).read_bytes()
                    data.update(schema=2 if "page_count" in data else 1, retrieved="2026-10-17",
                                provenance="Synthetic fixture bytes only", media_type="text/plain")
                    if data["artifact_type"] == "normalized-text":
                        data.update(indexable=True, encoding="utf-8")
                    else:
                        data["media_type"] = "application/pdf"
                    data["path"] = directory + "/payload.txt"
                    payload_path = self.root / data["path"]
                    payload_path.parent.mkdir(parents=True, exist_ok=True)
                    payload_path.write_bytes(payload)
                    relative = directory + "/artifact.toml"
                else:
                    data.setdefault("context", "Synthetic constituent extent only")
                    relative = directory + "/" + kind + "s/" + identity + ".toml"
            manifest = self.root / relative
            manifest.parent.mkdir(parents=True, exist_ok=True)
            manifest.write_text("\n".join(key + " = " + json.dumps(value) for key, value in data.items()) + "\n")
        result = texts.load_adapter("native-book:fixture-book", self.root)
        self.assertTrue(result["verification"]["source_library_valid"])
        self.assertEqual("Exact native fixture.", result["units"][0]["text"])
        self.assertEqual("edition.fixture-book", result["units"][0]["text_edition_id"])
        library = texts._load_library(self.root)
        source_library = sys.modules["_eucharistic_texts_source_library"]
        fingerprint = source_library.source_fingerprint(library, "passage.fixture-book.unit1")
        for identity in ("artifact.fixture-book.scan", "edition.fixture-book"):
            manifest = library.records[identity].path
            manifest.write_text(manifest.read_text() + '\nnotes = "Changed synthetic evidence metadata"\n')
            library = texts._load_library(self.root)
            changed = source_library.source_fingerprint(library, "passage.fixture-book.unit1")
            self.assertNotEqual(fingerprint, changed)
            fingerprint = changed

    def test_complete_constituent_cannot_claim_the_whole_book(self):
        book, extent, review, save = native_fixture(self)
        book["extent_kind"] = "constituent"
        book["excluded_book_divisions"] = ["Second native division"]
        book["witnesses"][0]["scope_pages"] = [[1, 1]]
        book["units"].pop()
        extent["expected_unit_ids"].pop()
        extent["pages"][1] = {"witness_id": "copy", "ranges": [[2, 2]], "role": "outside-constituent",
                               "unit_ids": [], "description": "Second native division outside this complete constituent"}
        review["unit_sha256"].pop("unit.fixture.2")
        save()
        result = self.load()
        self.assertFalse(result["scope"]["whole_book_complete"])
        self.assertTrue(result["scope"]["complete_declared_extent"])
        self.assertEqual(1, result["scope"]["known_extent_pages"])
        book["extent_kind"] = "whole-book"
        book["excluded_book_divisions"] = []
        save()
        with self.assertRaisesRegex(texts.AdapterError, "every witness page in scope"):
            self.load()

    def test_parallel_derivative_requires_exact_new_collation_witness(self):
        book, extent, review, save = native_fixture(self)
        self.records["artifact.fixture-book.unit1"].data.pop("derived_from")
        unit = book["units"][0]
        unit["verified_against_artifact_id"] = "artifact.fixture-book.scan"
        unit["verified_against_artifact_sha256"] = review["witness_sha256"]["copy"]
        save()
        self.assertEqual("Exact native fixture.", self.load()["units"][0]["text"])
        unit["verified_against_artifact_sha256"] = "0" * 64
        save()
        with self.assertRaisesRegex(texts.AdapterError, "does not derive"):
            self.load()

    def test_projection_or_companion_cannot_substitute_for_byte_derivation(self):
        book, extent, review, save = native_fixture(self)
        artifact = self.records["artifact.fixture-book.unit1"].data
        artifact.pop("derived_from")
        artifact.pop("transformation")
        unit = book["units"][0]
        witness_id = "artifact.fixture-book.scan"
        for field, value in (("projected_from", [witness_id]),
                             ("support_artifacts", [{"artifact_id": witness_id, "embedded_reference": "fixture"}])):
            with self.subTest(edge=field):
                artifact[field] = value
                save()
                with self.assertRaisesRegex(texts.AdapterError, "does not derive from its exact witness"):
                    self.load()
                unit["verified_against_artifact_id"] = witness_id
                unit["verified_against_artifact_sha256"] = review["witness_sha256"]["copy"]
                save()
                self.assertEqual("Exact native fixture.", self.load()["units"][0]["text"])
                unit["verified_against_artifact_sha256"] = "0" * 64
                save()
                with self.assertRaisesRegex(texts.AdapterError, "does not derive from its exact witness"):
                    self.load()
                artifact.pop(field)
                unit.pop("verified_against_artifact_id")
                unit.pop("verified_against_artifact_sha256")

    def test_native_literal_ranges_preserve_non_lf_line_characters(self):
        native_fixture(self, wording="First\rSecond\u2028Third.")
        result = self.load()
        self.assertEqual("First\rSecond\u2028Third.", result["units"][0]["text"])

    def test_scratch_or_unowned_support_cannot_authorize_complete_extent(self):
        book, extent, review, save = native_fixture(self)
        book["extent_path"] = ".scratch/unreviewed-extent.json"
        book["collation_path"] = ".scratch/unreviewed-review.json"
        save()
        with self.assertRaisesRegex(texts.AdapterError, "canonical inventory ownership"):
            self.load()

    def test_adapter_rejects_unit_identity_that_corpus_cannot_serialize(self):
        book, extent, review, save = native_fixture(self)
        old = book["units"][0]["unit_id"]
        book["units"][0]["unit_id"] = "invalid/unit"
        extent["expected_unit_ids"][0] = "invalid/unit"
        extent["pages"][0]["unit_ids"] = ["invalid/unit"]
        review["unit_sha256"]["invalid/unit"] = review["unit_sha256"].pop(old)
        save()
        with self.assertRaisesRegex(texts.AdapterError, "safe stable unit id"):
            self.load()

    def test_native_paths_cannot_replace_another_unit_with_a_git_directory(self):
        book, extent, review, save = native_fixture(self)
        book["units"][0]["native_path"] = ["canon"]
        book["units"][1]["native_path"] = ["canon.txt", "memento"]
        save()
        with self.assertRaisesRegex(texts.AdapterError, "file/directory collision"):
            self.load()
        book["units"][0]["native_path"], book["units"][1]["native_path"] = (
            book["units"][1]["native_path"], book["units"][0]["native_path"])
        save()
        with self.assertRaisesRegex(texts.AdapterError, "file/directory collision"):
            self.load()

    def test_native_gate_covers_provenance_paths_and_uses_real_escaping(self):
        book, extent, review, save = native_fixture(self)
        book["units"][0]["native_path"] = ["canon"]
        book["units"][1]["native_path"] = ["canon.json", "memento"]
        save()
        with self.assertRaisesRegex(texts.AdapterError, "file/directory collision"):
            self.load()
        book["units"][0]["native_path"] = ["."]
        book["units"][1]["native_path"] = ["..txt", "memento"]
        save()
        result = self.load()
        self.assertEqual("text/native/%2E.txt", texts.native_text_path(result["units"][0]["native_path"]))

    def test_approval_date_cannot_relabel_the_identified_witness(self):
        book, extent, review, save = native_fixture(self)
        book["date"].update(kind="approval", label="1250 approval", start_year=1250, end_year=1250)
        save()
        result = self.load()
        self.assertEqual("1250 approval", result["target_date"])
        self.assertEqual("approval", result["historical_date"]["kind"])
        self.assertEqual("1200", result["witness_date"])
        self.assertEqual("edition.fixture-book", result["witness_dates"][0]["edition_id"])

    def test_retained_page_image_can_bind_a_complete_constituent(self):
        book, extent, review, save = native_fixture(self)
        self.records["artifact.fixture-book.scan"].data.update(artifact_type="facsimile-image", page_count=1)
        book.update(extent_kind="constituent", excluded_book_divisions=["Other divisions outside the held image"])
        book["witnesses"][0]["scope_pages"] = [[1, 1]]
        book["units"].pop()
        extent["expected_unit_ids"].pop()
        extent["pages"].pop()
        review["unit_sha256"].pop("unit.fixture.2")
        save()
        result = self.load()
        self.assertTrue(result["scope"]["complete_declared_extent"])
        self.assertFalse(result["scope"]["whole_book_complete"])

    def test_image_preserving_pdf_derivative_remains_a_reviewed_facsimile(self):
        book, extent, review, save = native_fixture(self)
        images = self.artifact("artifact.fixture-book.images", "Synthetic exact page-image package.\n",
                               artifact_type="page-image-package", media_type="application/zip",
                               edition_id="edition.fixture-book")
        scan = self.records["artifact.fixture-book.scan"].data
        scan.update(artifact_type="facsimile-pdf-derivative", media_type="application/pdf",
                    derived_from=images["id"], transformation="Embed original JPEG byte streams in page order.")
        result = self.load()
        self.assertTrue(result["scope"]["whole_book_complete"])
        self.assertEqual("Exact native fixture.", result["units"][0]["text"])
        self.assertEqual("facsimile-pdf-derivative", next(source["artifact_type"] for source in result["sources"]
                                                         if source["id"] == scan["id"]))
        # Image provenance cannot substitute for full extent or independent review.
        review["independent"] = False
        save()
        with self.assertRaisesRegex(texts.AdapterError, "complete extent and independent collation"):
            self.load()
        review["independent"] = True
        extent["pages"].pop()
        save()
        with self.assertRaisesRegex(texts.AdapterError, "pages unaccounted"):
            self.load()

    def test_pdf_derivative_requires_image_provenance_not_ocr_or_text(self):
        native_fixture(self)
        images = self.artifact("artifact.fixture-book.images", "Synthetic page-image package.\n",
                               artifact_type="page-image-package", edition_id="edition.fixture-book")
        scan = self.records["artifact.fixture-book.scan"].data
        scan.update(artifact_type="facsimile-pdf-derivative", media_type="application/pdf",
                    derived_from=images["id"], transformation="Embed original image byte streams.")
        for field, value in (("artifact_type", "ocr"), ("artifact_type", "normalized-text"),
                             ("artifact_type", "pdf-derivative"), ("media_type", "text/plain"),
                             ("derived_from", None), ("transformation", "")):
            with self.subTest(field=field, value=value):
                original = scan[field]
                try:
                    scan[field] = value
                    with self.assertRaisesRegex(texts.AdapterError, "exact retained facsimile"):
                        self.load()
                finally:
                    scan[field] = original
        for kind in ("ocr", "normalized-text"):
            with self.subTest(parent_type=kind):
                images["artifact_type"] = kind
                with self.assertRaisesRegex(texts.AdapterError, "exact retained facsimile"):
                    self.load()

    def test_partial_selection_cannot_claim_complete(self):
        book, extent, review, save = native_fixture(self)
        book["units"].pop()
        save()
        with self.assertRaisesRegex(texts.AdapterError, "independent extent census"):
            self.load()

    def test_complete_census_requires_every_page_and_every_unit_locus(self):
        book, extent, review, save = native_fixture(self)
        extent["pages"].pop()
        save()
        with self.assertRaisesRegex(texts.AdapterError, "pages unaccounted"):
            self.load()
        extent["pages"].append({"witness_id": "copy", "ranges": [[2, 2]], "role": "non-text", "unit_ids": [], "description": "Blank"})
        save()
        with self.assertRaisesRegex(texts.AdapterError, "unit loci unaccounted"):
            self.load()

    def test_review_must_be_independent_complete_and_current(self):
        book, extent, review, save = native_fixture(self)
        review["reviewer"] = book["transcribed_by"]
        save()
        with self.assertRaisesRegex(texts.AdapterError, "independent of transcriber"):
            self.load()
        review["reviewer"] = "independent"
        extent["unresolved"] = ["unread rubric"]
        save()
        with self.assertRaisesRegex(texts.AdapterError, "complete extent"):
            self.load()
        extent["unresolved"] = []
        save()
        path = self.root / texts.NATIVE_BOOK_DIRECTORY / "fixture-book.json"
        path.write_text(path.read_text() + "\n")
        with self.assertRaisesRegex(texts.AdapterError, "collation is stale"):
            self.load()

    def test_unverified_or_rights_ineligible_literal_is_denied(self):
        native_fixture(self)
        passage = self.records["passage.fixture-book.unit1"].data
        passage["states"] = ["inspected"]
        with self.assertRaisesRegex(texts.AdapterError, "verified exact-edition"):
            self.load()
        passage["states"] = ["verified"]
        artifact = self.records["artifact.fixture-book.unit1"].data
        artifact["rights_status"] = "unresolved"
        with self.assertRaisesRegex(texts.AdapterError, "public-git publication"):
            self.load()
        artifact["rights_status"] = "public-domain"
        artifact.pop("derived_from")
        with self.assertRaisesRegex(texts.AdapterError, "exact witness"):
            self.load()


class AdapterBoundaryTests(unittest.TestCase):
    def setUp(self):
        scratch = Path(os.environ.get("TMPDIR", ROOT / ".scratch/text-reuse-expansion"))
        scratch.mkdir(parents=True, exist_ok=True)
        self.temp = tempfile.TemporaryDirectory(dir=scratch)
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.records = {}
        self.library = SimpleNamespace(records=self.records, errors=[])

    def record(self, identity, kind, **data):
        path = self.root / "records" / (identity + ".json")
        path.parent.mkdir(parents=True, exist_ok=True)
        fields = {"id": identity, "record_type": kind, **data}
        path.write_text(json.dumps(fields), encoding="utf-8")
        self.records[identity] = SimpleNamespace(path=path, record_type=kind, data=fields)
        return fields

    def artifact(self, identity, body, **metadata):
        path = self.root / "payloads" / (identity + ".txt")
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(body, encoding="utf-8")
        return self.record(identity, "artifact", storage="tracked", path=path.relative_to(self.root).as_posix(),
                           sha256=sha(body), byte_size=len(body.encode("utf-8")), **metadata)

    def proper_fixture(self):
        self.path = self.root / "src/sources/calendars/roman-1962/propers.yaml"
        self.path.parent.mkdir(parents=True)
        self.path.write_text('''schema: triptych-calendar-masses/v1
calendar: roman-1962
sections:
  seasonal:
    kind: seasonal
    masses:
      - key: synthetic
        name: Synthetic test only
        registry: '01'
        propers:
          - name: Collect
            source: composed
            text: "Idem textus."
          - name: Collect
            source: composed
            text: "Idem textus."
''')
        self.record("edition.projection", "edition", date="2026-09-03")
        target_edition = "edition.catholic-church.missale-romanum.vatican-typica-1962"
        self.record(target_edition, "edition", date="1962")
        projection = self.artifact("artifact.projection", "Idem textus.\nIdem textus.\n",
                                   edition_id="edition.projection", rights_status="project-created")
        self.artifact("artifact.public-domain", "Historical fixture.\n", rights_status="public-domain")
        self.record("artifact.target", "artifact", storage="remote", rights_status="unresolved", sha256="a" * 64)
        self.record("passage.target", "passage", edition_id=target_edition, artifact_id="artifact.target")
        self.entries = []
        for occurrence in (1, 2):
            passage = f"passage.projection.{occurrence}"
            self.record(passage, "passage", edition_id="edition.projection", artifact_id="artifact.projection",
                        artifact_sha256=projection["sha256"], physical_line_ranges=[[occurrence, occurrence]])
            self.entries.append({
                "mass": "synthetic", "form": "", "proper": "Collect", "course": "", "cycle": "", "occurrence": occurrence,
                "text_sha256": sha("Idem textus."), "provenance_status": "collated", "source_id": passage,
                "source_date": "2026-09-03", "locator": "fixture line", "relationship": "editorial-projection-exact-to-target",
                "verification_source_id": "passage.target", "verification_locator": "fixture target page",
                "transformations": [], "provenance_evidence": "Synthetic test evidence", "provenance_authority": "test",
                "provenance_confidence": "high", "publication_status": "permitted", "publication_basis": "public-domain",
                "surfaces": ["public-git", "corpus-data"], "publication_source_ids": ["artifact.public-domain"],
                "publication_locator": "fixture", "publication_evidence": "Synthetic test basis",
            })
        self.ledger = self.root / "src/sources/inventories/roman-1962-proper-latin-provenance-v1.toml"
        self.ledger.parent.mkdir(parents=True)
        self.write_ledger()

    def write_ledger(self):
        lines = ['schema = "triptych-proper-latin-provenance/v1"', 'calendar = "roman-1962"', 'language = "la"',
                 'policy = "guidance/liturgical-text-publication-policy.md"', '[defaults]',
                 'provenance_status = "unresolved"', 'publication_status = "unresolved"',
                 'publication_basis = "unresolved"', 'surfaces = []']
        for entry in self.entries:
            lines.append('[[entries]]')
            lines.extend(f"{key} = {json.dumps(value)}" for key, value in entry.items())
        self.ledger.write_text("\n".join(lines) + "\n")

    def load(self, adapter="roman-1962-propers"):
        with patch.object(texts, "_load_library", return_value=self.library):
            return texts.load_adapter(adapter, self.root)

    def test_occurrences_keep_distinct_identity_and_order_even_when_words_match(self):
        self.proper_fixture()
        first = self.load()
        self.assertEqual(first, self.load())
        units = first["units"]
        self.assertEqual([1, 2], [u["identity"]["occurrence"] for u in units])
        self.assertNotEqual(units[0]["unit_id"], units[1]["unit_id"])
        self.assertEqual(units[0]["content_id"], units[1]["content_id"])
        self.assertNotEqual(units[0]["text_edition_id"], units[0]["target_edition_id"])
        self.assertFalse(first["scope"]["whole_book_complete"])
        self.assertEqual([], first["historical_comparisons"])

    def test_changed_calendar_text_fails_even_with_plausible_words(self):
        self.proper_fixture()
        self.path.write_text(self.path.read_text().replace("Idem textus.", "Mutatus textus.", 1))
        with self.assertRaisesRegex(texts.AdapterError, "stale text hash"):
            self.load()

    def test_collated_selection_keeps_nonexact_target_qualification(self):
        self.proper_fixture()
        entry = self.entries[0]
        entry.update(relationship="collated-exact",
                     transformations=["Select feast wording; parenthetical target alternative not represented"],
                     provenance_evidence="Synthetic bounded selection, not exact to the complete target")
        self.write_ledger()
        result = self.load()
        unit = result["units"][0]
        self.assertEqual(2, len(result["units"]))
        self.assertEqual("Idem textus.", unit["text"])
        for field in ("relationship", "transformations", "provenance_evidence"):
            self.assertEqual(entry[field], unit["provenance"][field])
        self.assertFalse(unit["diplomatic"])
        self.assertFalse(result["scope"]["whole_book_complete"])
        self.assertEqual([], result["omitted_body_owners"])

    def test_collated_selection_still_checks_owning_projection(self):
        self.proper_fixture()
        self.entries[0]["relationship"] = "collated-exact"
        self.path.write_text(self.path.read_text().replace("Idem textus.", "Mutatus textus.", 1))
        self.entries[0]["text_sha256"] = sha("Mutatus textus.")
        self.write_ledger()
        with self.assertRaisesRegex(texts.AdapterError, "differs from owning projection"):
            self.load()

    def test_rehashed_calendar_cannot_drift_from_owning_projection(self):
        self.proper_fixture()
        self.path.write_text(self.path.read_text().replace("Idem textus.", "Mutatus textus.", 1))
        self.entries[0]["text_sha256"] = sha("Mutatus textus.")
        self.write_ledger()
        with self.assertRaisesRegex(texts.AdapterError, "differs from owning projection"):
            self.load()

    def test_web_permission_does_not_authorize_git_export(self):
        self.proper_fixture()
        self.entries[0]["surfaces"] = ["web"]
        self.write_ledger()
        with self.assertRaisesRegex(texts.AdapterError, "must cover corpus-data and public-git"):
            self.load()

    def test_changed_projection_payload_fails_hash_check(self):
        self.proper_fixture()
        artifact = self.records["artifact.projection"].data
        (self.root / artifact["path"]).write_text("Mutatus textus.\nIdem textus.\n")
        with self.assertRaisesRegex(texts.AdapterError, "Artifact hash mismatch"):
            self.load()

    def test_registered_other_edition_cannot_verify_a_1962_target(self):
        self.proper_fixture()
        self.record("edition.other-target", "edition", date="1861")
        self.record("passage.other-target", "passage", edition_id="edition.other-target",
                    artifact_id="artifact.target")
        self.entries[0]["verification_source_id"] = "passage.other-target"
        self.write_ledger()
        with self.assertRaisesRegex(texts.AdapterError, "Verification target edition mismatch"):
            self.load()

    def test_alternate_data_root_cannot_supply_or_hide_executed_tool_provenance(self):
        self.proper_fixture()
        # A sparse data root still pins every trusted implementation input.
        first = self.load()
        actual = {row["path"]: row for row in first["tool_inputs"]}
        self.assertEqual(set(texts.TOOL_INPUT_PATHS), set(actual))
        for path, record in actual.items():
            self.assertEqual(hashlib.sha256((ROOT / path).read_bytes()).hexdigest(), record["sha256"])
        fake = self.root / "scripts/_eucharistic_texts.py"
        fake.parent.mkdir(parents=True)
        fake.write_text("raise RuntimeError('untrusted data-root code')\n")
        second = self.load()
        self.assertEqual(first["tool_inputs"], second["tool_inputs"])
        self.assertNotIn("scripts/_eucharistic_texts.py", {row["path"] for row in second["inputs"]})

    def test_missing_trusted_tool_input_fails_closed(self):
        self.proper_fixture()
        with patch.object(texts, "TOOL_INPUT_PATHS", ("scripts/absent-eucharistic-tool.py",)):
            with self.assertRaisesRegex(texts.AdapterError, "Cannot export.*absent-eucharistic-tool"):
                self.load()

    def ordinary_fixture(self):
        self.record(texts.ORDINARY_EDITION, "edition", date="1861")
        stem = "artifact.eugene-cummiskey.roman-missal-english-laity.philadelphia-1861.canon-missae"
        self.artifact(stem + "-la", "seq\telement_key\tpart\tprinted_page\tia_leaf\tlatin\tnotes\n"
                      "2\tte-igitur\tcanon\txxxiii\t43\tTest fixture Latin.\tUnchanged wording\n",
                      rights_status="public-domain", rights_basis="Synthetic test basis", edition_id=texts.ORDINARY_EDITION)
        self.artifact(stem + "-en", "seq\telement_key\tpart\tkind\tspeaker\tprinted_page\tenglish\n"
                      "1\theading\tcanon\theading\t\txxxiii\tDo not export this\n"
                      "2\tte-igitur\tcanon\tprayer\tpriest\txxxiii\tDo not export this either\n"
                      "3\trubric\tcanon\trubric\t\txxxiii\tNor this\n",
                      rights_status="public-domain", rights_basis="Synthetic test basis", edition_id=texts.ORDINARY_EDITION)

    def test_ordinary_preserves_edition_and_explicit_non_latin_omissions(self):
        self.ordinary_fixture()
        with patch.object(texts, "ORDINARY_DIVISIONS", ("canon-missae",)):
            result = self.load("cummiskey-1861-latin-ordinary")
        self.assertEqual("Test fixture Latin.", result["units"][0]["text"])
        self.assertEqual(texts.ORDINARY_EDITION, result["units"][0]["target_edition_id"])
        self.assertEqual(["heading", "rubric"], [r["kind"] for r in result["divisions"][0]["omitted_non_latin_blocks"]])
        self.assertNotIn("Do not export", json.dumps(result))

    def test_ordinary_refuses_a_changed_rights_disposition(self):
        self.ordinary_fixture()
        key = "artifact.eugene-cummiskey.roman-missal-english-laity.philadelphia-1861.canon-missae-la"
        self.records[key].data["rights_status"] = "unresolved"
        with patch.object(texts, "ORDINARY_DIVISIONS", ("canon-missae",)):
            with self.assertRaisesRegex(texts.AdapterError, "lacks publication basis"):
                self.load("cummiskey-1861-latin-ordinary")

    def wilson_fixture(self):
        self.wilson_text = "Synthetic source. Exact fixture wording."
        self.record(texts.WILSON_EDITION, "edition", date="1915")
        artifact = self.artifact(texts.WILSON_MEMENTO_ARTIFACT, self.wilson_text + "\n",
                                 artifact_type="normalized-text", edition_id=texts.WILSON_EDITION,
                                 rights_status="public-domain", rights_basis="Synthetic test basis",
                                 rights_jurisdiction="United States", transformation="Synthetic test transformation")
        self.record(texts.WILSON_MEMENTO_PASSAGE, "passage", edition_id=texts.WILSON_EDITION,
                    artifact_id=texts.WILSON_MEMENTO_ARTIFACT, artifact_sha256=artifact["sha256"],
                    physical_line_ranges=[[1, 1]], states=["verified"], verified_on="2026-10-16", locus="Fixture page")

    def load_wilson(self):
        with patch.object(texts, "WILSON_MEMENTO_TEXT_SHA256", sha(self.wilson_text)):
            return self.load("wilson-1915-gregorian-canon-memento")

    def test_wilson_uses_only_the_checked_body_and_preserves_edition_scope(self):
        self.wilson_fixture()
        result = self.load_wilson()
        self.assertEqual(self.wilson_text, result["units"][0]["text"])
        self.assertEqual("1915", result["target_date"])
        self.assertEqual("2026-10-16", result["reviewed_on"])
        self.assertIn("ninth century", result["witness_date"])
        self.assertTrue(result["scope"]["not_direct_manuscript_transcription"])
        self.assertFalse(result["scope"]["whole_book_complete"])
        self.assertIn("critical apparatus, including the O variant", result["scope"]["omitted_book_divisions"])

    def test_wilson_rehashed_wording_cannot_override_the_reviewed_body(self):
        self.wilson_fixture()
        artifact = self.records[texts.WILSON_MEMENTO_ARTIFACT].data
        changed = "Unreviewed replacement.\n"
        (self.root / artifact["path"]).write_text(changed)
        artifact["sha256"] = sha(changed)
        self.records[texts.WILSON_MEMENTO_PASSAGE].data["artifact_sha256"] = sha(changed)
        with self.assertRaisesRegex(texts.AdapterError, "differs from its reviewed wording"):
            self.load_wilson()

    def test_wilson_requires_review_publication_and_exact_identity(self):
        self.wilson_fixture()
        passage = self.records[texts.WILSON_MEMENTO_PASSAGE].data
        artifact = self.records[texts.WILSON_MEMENTO_ARTIFACT].data
        for record, field, replacement, message in (
            (passage, "states", ["inspected"], "lacks a verified bounded transcription"),
            (artifact, "rights_status", "unresolved", "lacks its public-domain publication basis"),
            (artifact, "rights_jurisdiction", "unspecified", "lacks its public-domain publication basis"),
            (passage, "edition_id", texts.ORDINARY_EDITION, "identity mismatch"),
            (passage, "physical_line_ranges", [[1, 2]], "extent/hash mismatch"),
        ):
            with self.subTest(field=field):
                original = record[field]
                record[field] = replacement
                # An alternative registered edition must still be refused.
                self.record(texts.ORDINARY_EDITION, "edition", date="1861")
                try:
                    with self.assertRaisesRegex(texts.AdapterError, message):
                        self.load_wilson()
                finally:
                    record[field] = original

    def checked_selection(self):
        self.wilson_fixture()
        return {"title": "Synthetic selected prayer", "edition_id": texts.WILSON_EDITION,
                "scope": {"status": "one-complete-prayer", "omitted_book_divisions": ["all other text"]},
                "units": [{"unit_id": "unit.synthetic.prayer", "passage_id": texts.WILSON_MEMENTO_PASSAGE,
                           "artifact_id": texts.WILSON_MEMENTO_ARTIFACT, "text_sha256": sha(self.wilson_text),
                           "language": "la", "division": "canon", "element_key": "synthetic", "source_order": 1}]}

    def test_generic_checked_selection_keeps_native_text_and_deterministic_provenance(self):
        selection = self.checked_selection()
        with patch.dict(texts.CHECKED_PASSAGE_SETS, {"synthetic-checked-prayer": selection}):
            first = self.load("synthetic-checked-prayer")
            self.assertEqual(first, self.load("synthetic-checked-prayer"))
        self.assertEqual(self.wilson_text, first["units"][0]["text"])
        self.assertEqual("1915", first["target_date"])
        self.assertIsNone(first["witness_date"])
        self.assertEqual(["all other text"], first["scope"]["omitted_book_divisions"])
        self.assertEqual("Synthetic test transformation", first["units"][0]["provenance"]["normalization"])

    def test_generic_checked_selection_rejects_unreviewed_rehashed_text(self):
        selection = self.checked_selection()
        artifact = self.records[texts.WILSON_MEMENTO_ARTIFACT].data
        changed = "Different but well-formed text.\n"
        (self.root / artifact["path"]).write_text(changed)
        artifact["sha256"] = sha(changed)
        self.records[texts.WILSON_MEMENTO_PASSAGE].data["artifact_sha256"] = sha(changed)
        with patch.dict(texts.CHECKED_PASSAGE_SETS, {"synthetic-checked-prayer": selection}):
            with self.assertRaisesRegex(texts.AdapterError, "differs from reviewed wording"):
                self.load("synthetic-checked-prayer")

    def test_generic_checked_calendar_selection_keeps_blank_feast_cell_scope(self):
        selection = self.checked_selection()
        body = "5"
        artifact = self.records[texts.WILSON_MEMENTO_ARTIFACT].data
        passage = self.records[texts.WILSON_MEMENTO_PASSAGE].data
        (self.root / artifact["path"]).write_text(body + "\n", encoding="utf-8")
        artifact.update(sha256=sha(body + "\n"), byte_size=len((body + "\n").encode("utf-8")))
        passage.update(artifact_sha256=artifact["sha256"],
                       context="October 5 row: printed day retained; feast cell empty. Computistical columns omitted.")
        selection["scope"]["status"] = "one-calendar-row"
        selection["units"][0].update(text_sha256=sha(body), kind="calendar-entry", part="calendar",
                                     division="calendar", element_key="october-05")
        with patch.dict(texts.CHECKED_PASSAGE_SETS, {"synthetic-checked-calendar": selection}):
            result = self.load("synthetic-checked-calendar")
        unit = result["units"][0]
        self.assertEqual("5", unit["text"])
        self.assertEqual(("calendar-entry", "calendar"), (unit["kind"], unit["part"]))
        self.assertEqual(passage["context"], unit["provenance"]["scope"])
        self.assertFalse(result["scope"]["whole_book_complete"])

    def test_generic_checked_selection_preserves_greek_codepoints_and_speech_boundaries(self):
        selection = self.checked_selection()
        # Deliberately decomposed accent, lunate sigma and final sigma: neither
        # Unicode composition nor comparison-oriented letter folding is an export.
        body = "Α\u0301 Ϲ ϲ ς"
        artifact = self.records[texts.WILSON_MEMENTO_ARTIFACT].data
        passage = self.records[texts.WILSON_MEMENTO_PASSAGE].data
        (self.root / artifact["path"]).write_text(body + "\n", encoding="utf-8")
        artifact.update(sha256=sha(body + "\n"), byte_size=len((body + "\n").encode("utf-8")))
        passage.update(artifact_sha256=artifact["sha256"],
                       notes="Synthetic speech blocks [0, 4) and [5, 8); intervening response omitted.")
        selection["units"][0].update(language="grc", text_sha256=sha(body))
        with patch.dict(texts.CHECKED_PASSAGE_SETS, {"synthetic-checked-prayer": selection}):
            result = self.load("synthetic-checked-prayer")
        unit = result["units"][0]
        self.assertEqual(body.encode("utf-8"), unit["text"].encode("utf-8"))
        self.assertEqual(sha(body), unit["text_sha256"])
        self.assertEqual(passage["notes"], unit["provenance"]["review_limits"])
        self.assertEqual({"grc": 1}, result["counts"]["languages"])

    def test_checked_selection_pins_source_decoding_dependencies(self):
        selection = self.checked_selection()
        support_id = "artifact.synthetic.shared-annotation"
        support = self.artifact(support_id, "Synthetic decoding dependency.\n", rights_status="public-domain")
        dependency = {"artifact_id": support_id, "embedded_reference": "shared_anno.iff"}
        self.records[texts.WILSON_MEMENTO_ARTIFACT].data["support_artifacts"] = [dependency]
        with patch.dict(texts.CHECKED_PASSAGE_SETS, {"synthetic-checked-prayer": selection}):
            result = self.load("synthetic-checked-prayer")
            records = {record["id"]: record for record in result["sources"]}
            self.assertIn(support_id, records)
            self.assertEqual([dependency], records[texts.WILSON_MEMENTO_ARTIFACT]["support_artifacts"])
            self.assertIn(support["path"], {item["path"] for item in result["inputs"]})
            (self.root / support["path"]).write_text("Changed decoding dependency.\n")
            with self.assertRaisesRegex(texts.AdapterError, "Artifact hash mismatch"):
                self.load("synthetic-checked-prayer")

    def test_generic_checked_selection_requires_exact_controller_review_and_rights(self):
        selection = self.checked_selection()
        passage = self.records[texts.WILSON_MEMENTO_PASSAGE].data
        artifact = self.records[texts.WILSON_MEMENTO_ARTIFACT].data
        self.record(texts.ORDINARY_EDITION, "edition", date="1861")
        for record, field, replacement, message in (
            (passage, "edition_id", texts.ORDINARY_EDITION, "identity mismatch"),
            (passage, "artifact_id", "artifact.other", "identity mismatch"),
            (passage, "states", ["inspected"], "is not verified"),
            (artifact, "rights_status", "unresolved", "publication basis"),
            (passage, "physical_line_ranges", [[1, 2]], "extent/hash mismatch"),
        ):
            with self.subTest(field=field), patch.dict(texts.CHECKED_PASSAGE_SETS, {"synthetic-checked-prayer": selection}):
                self.artifact("artifact.other", self.wilson_text + "\n", edition_id=texts.WILSON_EDITION)
                original = record[field]
                record[field] = replacement
                try:
                    with self.assertRaisesRegex(texts.AdapterError, message):
                        self.load("synthetic-checked-prayer")
                finally:
                    record[field] = original


if __name__ == "__main__":
    unittest.main()
