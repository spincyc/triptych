"""Corrections preserve frozen witnesses and exclude only actual prior PDF bytes."""
from __future__ import annotations

import contextlib
import copy
import hashlib
import io
import json
import os
from pathlib import Path
import shlex
import subprocess
import sys
import tempfile
import tomllib
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))
import _bullarium as source
import _bullarium_corrections as corrections
from _typeset_papal import validate_document

REVISION = "2026-10-26T12:00:00Z"
PRIOR_REVISION = "2026-10-26T10:00:00Z"
CUMULATIVE_REVISION = "2026-10-26T11:00:00Z"


class CorrectionTests(unittest.TestCase):
    def setUp(self):
        scratch = ROOT / ".scratch/bullarium_reconstruction/correction_engine/per_row/tests"
        scratch.mkdir(parents=True, exist_ok=True)
        self.temp = tempfile.TemporaryDirectory(dir=scratch)
        self.root = Path(self.temp.name)
        (self.root / "src/gpt").mkdir(parents=True)
        self.payload = ("I.\r\nTitulus.\r\nLeo Papa I.\r\n\r\nVerba Latina integra.\r\n\r\n"
                        "Atto italiano inserito.\r\n\r\nDatum Romae.\r\nSubscriptionis finis.\r\n"
                        "Nota historica huius actus.\r\n").encode()
        self.container = self.root / "src/sources/works/fixture/container"
        self.container_edition = self.container / "editions/1871-test"
        self.payload_path = self.container_edition / "artifacts/ocr/ocr.txt"
        source.write(self.payload_path, self.payload)
        self.act = self.root / "src/sources/works/fixture/act"
        self.edition = self.act / "editions/1871-test-latin"
        self.segment_path = self.edition / "segments/source-ocr.toml"
        self.work = {"schema": 1, "record_type": "work", "id": "work.fixture.act",
                     "title": "Titulus", "responsible": "Fixture author", "languages": ["la"],
                     "work_type": "historical-papal-act", "description": "Synthetic test act."}
        source.record(self.act / "work.toml", self.work)
        source.record(self.container / "work.toml", {**self.work, "id": "work.fixture.container",
                      "work_type": "historical-document-container", "title": "Fixture container"})
        self.old_edition = {"schema": 1, "record_type": "edition", "id": "edition.fixture.act.1871-test-latin",
                            "work_id": self.work["id"], "title": "Historical printing — 1871-test-latin", "language": "la",
                            "date": "1871", "publication": "Synthetic historical publication facts.",
                            "notes": "Prior source-edition notes."}
        source.record(self.edition / "edition.toml", self.old_edition)
        source.record(self.container_edition / "edition.toml", {**self.old_edition,
                      "id": "edition.fixture.container.1871-test", "work_id": "work.fixture.container"})
        self.doc = {"id": "bullarium.fixture.unit-0001", "title": "Titulus", "pope": "Leo Papa I.",
                    "date": None, "document_type": "Historical papal act", "language": "la",
                    "source_url": "https://example.org/fixture.txt",
                    "text_path": self.payload_path.relative_to(self.root).as_posix(),
                    "sha256": hashlib.sha256(self.payload).hexdigest(), "artifact_id": "artifact.fixture.container.1871-test.ocr",
                    "rights_status": "public-domain", "rights_basis": "Synthetic test wording; no external source text.",
                    "rights_notice": "Synthetic fixture retains its stated rights.",
                    "segment_id": "segment.fixture.act.1871-test-latin.source-ocr",
                    "segment_path": self.segment_path.relative_to(self.root).as_posix(),
                    "physical_line_ranges": [[1, 10]], "source_note": "Prior project apparatus."}
        source.record(self.payload_path.parent / "artifact.toml", {
            "schema": 1, "record_type": "artifact", "id": self.doc["artifact_id"],
            "edition_id": "edition.fixture.container.1871-test", "artifact_type": "uncorrected-ocr",
            "media_type": "text/plain", "storage": "tracked", "rights_status": self.doc["rights_status"],
            "rights_basis": self.doc["rights_basis"], "rights_jurisdiction": "United States",
            "retrieved": "2026-10-26", "sha256": self.doc["sha256"], "byte_size": len(self.payload),
            "path": self.doc["text_path"], "source_url": self.doc["source_url"], "encoding": "utf-8", "indexable": True})
        source.record(self.segment_path, {"schema": 2, "record_type": "segment", "id": self.doc["segment_id"],
                      "edition_id": self.old_edition["id"], "artifact_id": self.doc["artifact_id"],
                      "artifact_sha256": self.doc["sha256"], "segment_type": "constituent-work",
                      "physical_line_ranges": self.doc["physical_line_ranges"],
                      "states": ["cataloged", "acquired", "inspected"], "context": "Original inspected selection.",
                      "notes": "Original segment notes."})
        self.initial = self.root / "initial.json"
        self.write_json(self.initial, {"schema": corrections.SCHEMA, "revision": PRIOR_REVISION, "documents": [self.doc]})
        self.receipt = self.add_receipt("prior-one", b"%PDF-1.4\nFirst reviewed fixture bytes.\n")
        self.plan_path, self.out = self.root / "plan.json", self.root / "corrections.json"
        self.plan = {"schema": corrections.PLAN_SCHEMA, "initial_manifests": ["initial.json"],
                     "prior_receipts": [self.receipt.relative_to(self.root).as_posix()],
                     "corrections": [{"prior_id": self.doc["id"], "replacement_id": self.doc["id"] + ".correction-2026-10-26",
                                      "reason": "Correct project apparatus without changing source wording.",
                                      "changes": {"source_note": "Corrected project apparatus.", "terminal_keep_blocks": 1,
                                                  "compact_layout": True}}]}

    def tearDown(self):
        self.temp.cleanup()

    @staticmethod
    def write_json(path, data):
        source.write(path, source.json_bytes(data))

    def add_receipt(self, name, pdf_bytes):
        folder = self.root / name
        pdf = folder / "edition/prior.pdf"
        source.write(pdf, pdf_bytes)
        row = {"id": self.doc["id"], "language": self.doc["language"], "status": "compiled",
               "artifact_id": self.doc["artifact_id"], "source_sha256": self.doc["sha256"],
               "segment_id": self.doc["segment_id"], "physical_line_ranges": self.doc["physical_line_ranges"],
               "pdf": "edition/prior.pdf", "pdf_sha256": hashlib.sha256(pdf_bytes).hexdigest(),
               "pages": 1, "text_fidelity": {"status": "pass"}}
        path = folder / "receipt.json"
        self.write_json(path, {"schema": corrections.RECEIPT_SCHEMA, "revision": PRIOR_REVISION, "documents": [row]})
        return path

    def build(self):
        self.write_json(self.plan_path, self.plan)
        return corrections.build_corrections(self.root, self.plan_path, self.out, REVISION)

    def frozen_files(self):
        return {path: path.read_bytes() for path in self.root.rglob("*") if path.is_file()
                and path not in {self.plan_path, self.out}}

    def new_segment(self, **updates):
        spec = {"key": "source-ocr-correction-2026-10-26", "physical_line_ranges": [[1, 11]],
                "context": "The newly included final source note belongs to this synthetic act.",
                "notes": "Exact source-selection correction; source bytes remain unchanged."}
        spec.update(updates)
        self.plan["corrections"][0]["new_segment"] = spec

    def new_edition(self):
        self.plan["corrections"][0]["new_edition"] = {
            "key": "1871-test-multilingual-correction-2026-10-26", "language": "mul",
            "notes": "Same historical printing; synthetic source includes Latin and Italian."}
        self.plan["corrections"][0]["changes"].update(language="mul", language_label="Latin and Italian")

    def cumulative_initial(self):
        self.doc["revision"] = PRIOR_REVISION
        appended = {**self.doc, "id": "bullarium.fixture.unit-0002", "revision": CUMULATIVE_REVISION}
        self.write_json(self.initial, {"schema": corrections.SCHEMA, "revision": CUMULATIVE_REVISION,
                                      "documents": [self.doc, appended]})

    def test_metadata_only_preserves_all_frozen_bytes_and_source_selection(self):
        before = self.frozen_files()
        checked_before = validate_document(self.doc, self.root)
        result = self.build()
        document = result["documents"][0]
        self.assertEqual(before, self.frozen_files())
        self.assertEqual(document["segment_id"], self.doc["segment_id"])
        self.assertEqual(document["physical_line_ranges"], self.doc["physical_line_ranges"])
        self.assertEqual(validate_document(document, self.root)["text"], checked_before["text"])
        self.assertEqual(self.payload_path.read_bytes(), self.payload)
        allowed = set(self.plan["corrections"][0]["changes"]) | {"id", "revision"}
        self.assertEqual({k: v for k, v in self.doc.items() if k not in allowed},
                         {k: v for k, v in document.items() if k not in allowed})
        self.assertEqual(document["revision"], REVISION)

    def test_legacy_frozen_receipt_survives_a_new_cumulative_header(self):
        self.cumulative_initial()
        before = self.frozen_files()
        document = self.build()["documents"][0]
        self.assertEqual(before, self.frozen_files())
        self.assertEqual(document["revision"], REVISION)
        self.assertNotEqual(document["revision"], self.doc["revision"])
        self.assertEqual(document["segment_id"], self.doc["segment_id"])

    def test_receipt_row_render_revision_overrides_its_cumulative_header(self):
        self.cumulative_initial()
        receipt = json.loads(self.receipt.read_text())
        receipt["revision"] = CUMULATIVE_REVISION
        receipt["documents"][0]["render_revision"] = PRIOR_REVISION
        self.write_json(self.receipt, receipt)
        result = self.build()
        self.assertEqual(result["supersessions"][0]["prior"]["pdf_sha256"],
                         hashlib.sha256((self.receipt.parent / "edition/prior.pdf").read_bytes()).hexdigest())

    def test_original_and_cumulative_manifests_accept_explicit_default_revision(self):
        original = self.root / "original.json"
        original.write_bytes(self.initial.read_bytes())
        self.cumulative_initial()
        self.plan["initial_manifests"].insert(0, "original.json")
        before = self.frozen_files()
        result = self.build()
        self.assertEqual(len(result["documents"]), 1)
        self.assertEqual(before, self.frozen_files())

    def test_new_header_cannot_authorize_a_wrong_receipt_row_revision(self):
        self.cumulative_initial()
        receipt = json.loads(self.receipt.read_text())
        receipt["revision"] = CUMULATIVE_REVISION
        receipt["documents"][0]["render_revision"] = CUMULATIVE_REVISION
        self.write_json(self.receipt, receipt)
        with self.assertRaisesRegex(ValueError, "document render revision disagree"):
            self.build()
        self.assertFalse(self.out.exists())

    def test_unknown_receipt_row_revision_is_refused_even_with_valid_header(self):
        receipt = json.loads(self.receipt.read_text())
        receipt["documents"][0]["render_revision"] = "2026-10-25T09:00:00Z"
        self.write_json(self.receipt, receipt)
        with self.assertRaisesRegex(ValueError, "document render revision disagree"):
            self.build()
        self.assertFalse(self.out.exists())

    def test_legacy_new_header_cannot_guess_the_older_row_render_revision(self):
        self.cumulative_initial()
        receipt = json.loads(self.receipt.read_text())
        receipt["revision"] = CUMULATIVE_REVISION
        self.write_json(self.receipt, receipt)
        with self.assertRaisesRegex(ValueError, "document render revision disagree"):
            self.build()
        self.assertFalse(self.out.exists())

    def test_invalid_manifest_row_and_receipt_revisions_are_refused(self):
        self.cumulative_initial()
        valid_initial, valid_receipt = self.initial.read_bytes(), self.receipt.read_bytes()
        cases = (("initial-row", None), ("receipt-row", "2026-02-30T10:00:00Z"),
                 ("receipt-header", "2026-10-26T10:00:00+00:00"))
        for owner, bad_revision in cases:
            with self.subTest(owner=owner):
                self.initial.write_bytes(valid_initial)
                self.receipt.write_bytes(valid_receipt)
                path = self.initial if owner == "initial-row" else self.receipt
                data = json.loads(path.read_text())
                if owner == "receipt-header":
                    data["revision"] = bad_revision
                else:
                    data["documents"][0]["revision" if owner == "initial-row" else "render_revision"] = bad_revision
                self.write_json(path, data)
                with self.assertRaisesRegex(ValueError, "explicit whole-second UTC"):
                    self.build()
                self.assertFalse(self.out.exists())

    def test_cumulative_revision_support_does_not_hide_changed_document_metadata(self):
        original = self.root / "original.json"
        original.write_bytes(self.initial.read_bytes())
        self.cumulative_initial()
        changed = json.loads(self.initial.read_text())
        changed["documents"][0]["source_note"] = "Different prior apparatus."
        self.write_json(self.initial, changed)
        self.plan["initial_manifests"].insert(0, "original.json")
        with self.assertRaisesRegex(ValueError, "disagree on a prior document"):
            self.build()
        self.assertFalse(self.out.exists())

    def test_legacy_and_new_receipts_keep_every_distinct_actual_pdf_hash(self):
        self.cumulative_initial()
        newer = self.add_receipt("prior-cumulative", b"%PDF-1.4\nA second exact prior layout.\n")
        data = json.loads(newer.read_text())
        data["revision"] = CUMULATIVE_REVISION
        data["documents"][0]["render_revision"] = PRIOR_REVISION
        self.write_json(newer, data)
        self.plan["prior_receipts"].append(newer.relative_to(self.root).as_posix())
        result = self.build()
        expected = {hashlib.sha256((path.parent / "edition/prior.pdf").read_bytes()).hexdigest()
                    for path in (self.receipt, newer)}
        self.assertEqual({row["prior"]["pdf_sha256"] for row in result["supersessions"]}, expected)

    def test_cumulative_prior_still_checks_actual_pdf_and_exact_source_selection(self):
        self.cumulative_initial()
        valid = self.receipt.read_bytes()
        for field, value, error in (("pdf_sha256", "0" * 64, "prior PDF SHA-256 mismatch"),
                                    ("physical_line_ranges", [[1, 11]], "frozen source on physical_line_ranges")):
            with self.subTest(field=field):
                receipt = json.loads(valid)
                receipt["documents"][0][field] = value
                self.write_json(self.receipt, receipt)
                with self.assertRaisesRegex(ValueError, error):
                    self.build()
                self.assertFalse(self.out.exists())

    def test_changed_bounds_mint_a_separate_segment_without_copying_artifact(self):
        self.new_segment()
        before = self.frozen_files()
        document = self.build()["documents"][0]
        self.assertNotEqual(document["segment_path"], self.doc["segment_path"])
        self.assertEqual(document["physical_line_ranges"], [[1, 11]])
        for path, data in before.items():
            self.assertEqual(path.read_bytes(), data)
        segment = tomllib.loads((self.root / document["segment_path"]).read_text())
        self.assertEqual(segment["schema"], 2)
        self.assertEqual(segment["artifact_id"], self.doc["artifact_id"])
        self.assertNotIn("verified", segment["states"])
        self.assertEqual(len(list(self.root.glob("src/sources/works/**/artifact.toml"))), 1)
        self.assertIn("Nota historica", validate_document(document, self.root)["text"])

    def test_mul_edition_keeps_old_work_edition_segment_and_controller(self):
        self.new_edition()
        before = self.frozen_files()
        document = self.build()["documents"][0]
        for path, data in before.items():
            self.assertEqual(path.read_bytes(), data)
        self.assertEqual(document["language"], "mul")
        self.assertEqual(document["text_path"], self.doc["text_path"])
        self.assertEqual(document["physical_line_ranges"], self.doc["physical_line_ranges"])
        edition_path = (self.root / document["segment_path"]).parents[1] / "edition.toml"
        new = tomllib.loads(edition_path.read_text())
        self.assertEqual(new["work_id"], self.old_edition["work_id"])
        self.assertEqual(new["date"], self.old_edition["date"])
        self.assertEqual(new["publication"], self.old_edition["publication"])
        self.assertEqual(new["language"], "mul")
        self.assertEqual(new["title"], "Historical printing — 1871-test-multilingual-correction-2026-10-26")
        self.assertEqual(validate_document(document, self.root)["text"], validate_document(self.doc, self.root)["text"])

    def test_new_source_records_pass_frozen_source_library_schema(self):
        self.new_edition()
        self.new_segment()
        self.build()
        run = subprocess.run([sys.executable, str(ROOT / "tools/source-library"), "--root", str(self.root), "validate"],
                             capture_output=True, text=True, check=False,
                             env={**os.environ, "TRIPTYCH_LIBRARY_CACHE": "0"})
        self.assertEqual(run.returncode, 0, run.stdout + run.stderr)

    def test_new_edition_cannot_introduce_a_different_historical_printing_year(self):
        self.new_edition()
        self.plan["corrections"][0]["new_edition"]["key"] = "2026-multilingual-correction"
        before = self.frozen_files()
        with self.assertRaisesRegex(ValueError, "must match the existing historical printing date"):
            self.build()
        self.assertEqual(before, self.frozen_files())
        self.assertFalse(self.out.exists())

    def test_all_distinct_actual_prior_pdf_hashes_are_superseded(self):
        second = self.add_receipt("prior-two", b"%PDF-1.4\nDifferent reviewed layout bytes.\n")
        same = self.add_receipt("prior-identical", b"%PDF-1.4\nFirst reviewed fixture bytes.\n")
        self.plan["prior_receipts"] += [p.relative_to(self.root).as_posix() for p in (second, same)]
        result = self.build()
        expected = {hashlib.sha256((path.parent / "edition/prior.pdf").read_bytes()).hexdigest()
                    for path in (self.receipt, second, same)}
        self.assertEqual({s["prior"]["pdf_sha256"] for s in result["supersessions"]}, expected)
        self.assertEqual(len(result["supersessions"]), 2)
        for row in result["supersessions"]:
            self.assertEqual(row["prior"]["segment_id"], self.doc["segment_id"])
            self.assertEqual(row["replacement"]["source_sha256"], self.doc["sha256"])

    def test_declared_prior_pdf_hash_must_match_actual_file(self):
        receipt = json.loads(self.receipt.read_text())
        receipt["documents"][0]["pdf_sha256"] = "0" * 64
        self.write_json(self.receipt, receipt)
        with self.assertRaisesRegex(ValueError, "prior PDF SHA-256 mismatch"):
            self.build()
        self.assertFalse(self.out.exists())

    def test_missing_hash_cannot_be_invented_from_a_pdf(self):
        receipt = json.loads(self.receipt.read_text())
        receipt["documents"][0].pop("pdf_sha256")
        self.write_json(self.receipt, receipt)
        with self.assertRaisesRegex(ValueError, "requires an exact PDF SHA-256"):
            self.build()

    def test_whole_artifact_prior_omits_optional_segment_evidence(self):
        for key in ("segment_id", "segment_path", "physical_line_ranges"):
            self.doc.pop(key)
        self.write_json(self.initial, {"schema": corrections.SCHEMA, "revision": PRIOR_REVISION, "documents": [self.doc]})
        receipt = json.loads(self.receipt.read_text())
        for key in ("segment_id", "physical_line_ranges"):
            receipt["documents"][0].pop(key)
        self.write_json(self.receipt, receipt)
        result = self.build()
        self.assertNotIn("segment_id", result["supersessions"][0]["prior"])
        self.assertNotIn("segment_id", result["supersessions"][0]["replacement"])
        self.assertEqual(validate_document(result["documents"][0], self.root)["text"], self.payload.decode())

    def test_receipt_cannot_fabricate_a_different_source_selection(self):
        receipt = json.loads(self.receipt.read_text())
        receipt["documents"][0]["physical_line_ranges"] = [[1, 11]]
        self.write_json(self.receipt, receipt)
        with self.assertRaisesRegex(ValueError, "frozen source on physical_line_ranges"):
            self.build()

    def test_missing_prior_pdf_and_unsuccessful_prior_are_refused(self):
        pdf = self.receipt.parent / "edition/prior.pdf"
        pdf.unlink()
        with self.assertRaisesRegex(ValueError, "prior PDF is absent"):
            self.build()
        receipt = json.loads(self.receipt.read_text())
        receipt["documents"][0]["status"] = "rendered"
        self.write_json(self.receipt, receipt)
        with self.assertRaisesRegex(ValueError, "lacks a successful prior PDF"):
            self.build()

    def test_changed_whole_source_is_refused_before_any_new_record(self):
        self.new_segment()
        self.payload_path.write_bytes(self.payload + b"Unregistered change.\n")
        with self.assertRaisesRegex(ValueError, "SHA-256 mismatch"):
            self.build()
        self.assertEqual(list(self.edition.glob("segments/*.toml")), [self.segment_path])
        self.assertFalse(self.out.exists())

    def test_null_selection_cannot_expand_an_act_to_the_whole_container(self):
        self.new_segment(physical_line_ranges=None)
        with self.assertRaisesRegex(ValueError, "explicit new_segment physical_line_ranges must be nonempty"):
            self.build()
        self.assertEqual(list(self.edition.glob("segments/*.toml")), [self.segment_path])
        self.assertFalse(self.out.exists())

    def test_body_source_hash_rights_and_direct_bounds_cannot_be_overridden(self):
        for key in ("blocks", "text", "body", "artifact_id", "sha256", "text_path", "source_url",
                    "rights_status", "rights_basis", "rights_notice", "segment_id", "segment_path", "physical_line_ranges"):
            with self.subTest(key=key):
                self.plan["corrections"][0]["changes"] = {key: "fabricated"}
                with self.assertRaisesRegex(ValueError, "never body, source, hashes or rights"):
                    self.build()
        self.assertFalse(self.out.exists())

    def test_failed_new_document_validation_rolls_back_new_records(self):
        self.new_edition()
        self.new_segment(physical_line_ranges=[[1, 200]])
        before = self.frozen_files()
        with self.assertRaisesRegex(ValueError, "escape the controlling artifact"):
            self.build()
        self.assertEqual(before, self.frozen_files())
        self.assertFalse(self.out.exists())

    def test_later_invalid_document_rolls_back_earlier_new_source_record(self):
        self.new_segment()
        other = {**self.doc, "id": "bullarium.fixture.unit-0002"}
        self.write_json(self.initial, {"schema": corrections.SCHEMA, "revision": PRIOR_REVISION,
                                      "documents": [self.doc, other]})
        receipt = json.loads(self.receipt.read_text())
        row = copy.deepcopy(receipt["documents"][0])
        row["id"] = other["id"]
        receipt["documents"].append(row)
        self.write_json(self.receipt, receipt)
        self.plan["corrections"].append({"prior_id": other["id"], "replacement_id": other["id"] + ".corrected",
                                         "reason": "Synthetic invalid later correction.",
                                         "changes": {"terminal_keep_blocks": 999}})
        before = self.frozen_files()
        with self.assertRaisesRegex(ValueError, "bounded source-block count"):
            self.build()
        self.assertEqual(before, self.frozen_files())
        self.assertFalse(self.out.exists())

    def test_existing_new_paths_are_absent_or_byte_identical(self):
        self.new_segment()
        result = self.build()
        new_path = self.root / result["documents"][0]["segment_path"]
        before = self.frozen_files()
        self.assertEqual(self.build(), result)
        self.assertEqual(before, self.frozen_files())
        new_path.write_text("conflicting bytes\n")
        with self.assertRaisesRegex(ValueError, "refusing to replace existing bytes"):
            self.build()
        self.assertEqual(new_path.read_text(), "conflicting bytes\n")

    def test_a_concurrently_appearing_new_path_is_never_overwritten(self):
        self.new_segment()
        target = self.edition / "segments/source-ocr-correction-2026-10-26.toml"
        real_link = os.link

        def race(staged, destination):
            if destination == target:
                destination.write_bytes(b"Concurrent owner bytes remain intact.\n")
            real_link(staged, destination)

        with patch.object(corrections.os, "link", side_effect=race):
            with self.assertRaisesRegex(ValueError, "refusing to replace existing bytes"):
                self.build()
        self.assertEqual(target.read_bytes(), b"Concurrent owner bytes remain intact.\n")
        self.assertFalse(self.out.exists())

    def test_reader_source_note_is_audit_metadata_not_a_source_note_substitute(self):
        self.plan["corrections"][0]["changes"] = {"reader_source_note": "Additional audit qualification."}
        document = self.build()["documents"][0]
        self.assertEqual(document["source_note"], self.doc["source_note"])
        self.assertEqual(document["reader_source_note"], "Additional audit qualification.")

    def test_replacement_identity_and_new_segment_path_must_be_distinct(self):
        row = self.plan["corrections"][0]
        row["replacement_id"] = row["prior_id"]
        with self.assertRaisesRegex(ValueError, "replacement_id must be distinct"):
            self.build()
        row["replacement_id"] += ".corrected"
        self.new_segment(key="source-ocr")
        with self.assertRaisesRegex(ValueError, "edit a frozen input"):
            self.build()

    def test_repository_and_source_ownership_paths_cannot_escape(self):
        self.plan["prior_receipts"] = ["../outside.json"]
        with self.assertRaisesRegex(ValueError, "without traversal"):
            self.build()
        self.plan["prior_receipts"] = [self.receipt.relative_to(self.root).as_posix()]
        self.new_edition()
        target = self.edition.parent / self.plan["corrections"][0]["new_edition"]["key"]
        foreign = self.root / "foreign-owner"
        foreign.mkdir()
        target.symlink_to(foreign, target_is_directory=True)
        with self.assertRaisesRegex(ValueError, "cannot pass through symlinks"):
            self.build()
        self.assertFalse(list(foreign.iterdir()))

    def test_language_change_needs_truthful_new_edition_and_explicit_utc_revision(self):
        self.plan["corrections"][0]["changes"]["language"] = "it"
        with self.assertRaisesRegex(ValueError, "language disagrees with the selected source edition"):
            self.build()
        self.new_edition()
        self.plan["corrections"][0]["new_edition"]["key"] = "multilingual-correction"
        with self.assertRaisesRegex(ValueError, "distinct dated key"):
            self.build()
        self.write_json(self.plan_path, self.plan)
        with self.assertRaisesRegex(ValueError, "explicit whole-second UTC"):
            corrections.build_corrections(self.root, self.plan_path, self.out, "2026-02-30T12:00:00Z")

    def test_cli_success_errors_and_both_safe_captured_examples(self):
        self.write_json(self.plan_path, self.plan)
        stdout, stderr = io.StringIO(), io.StringIO()
        with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
            status = corrections.main(["--root", str(self.root), "--plan", "plan.json", "--out", "corrections.json",
                                       "--revision", REVISION, "--json"])
        self.assertEqual(status, 0, stderr.getvalue())
        self.assertEqual(json.loads(stdout.getvalue()), {"v": 1, "status": "ok", "documents": 1,
                         "supersessions": 1, "manifest": "corrections.json"})
        for example in corrections.EXAMPLES:
            stdout, stderr = io.StringIO(), io.StringIO()
            with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
                status = corrections.main(shlex.split(example.command)[2:])
            self.assertEqual(status, 2)
            self.assertFalse(stdout.getvalue())
            self.assertEqual(tuple(stderr.getvalue().splitlines()), example.output)
        stderr = io.StringIO()
        with contextlib.redirect_stderr(stderr):
            self.assertEqual(corrections.main(["--json"]), 2)
        self.assertEqual(json.loads(stderr.getvalue())["code"], "input")


if __name__ == "__main__":
    unittest.main()
