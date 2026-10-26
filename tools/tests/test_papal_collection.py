"""Exact identity, supersession and layout-review evidence for local PDF links."""
from __future__ import annotations

import copy
import hashlib
import json
from pathlib import Path
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))
import _papal_collection as collection


class CollectionTests(unittest.TestCase):
    def setUp(self):
        scratch = ROOT / ".scratch/build_integration/tests"
        scratch.mkdir(parents=True, exist_ok=True)
        self.temp = tempfile.TemporaryDirectory(dir=scratch)
        self.root = Path(self.temp.name)
        self.out = self.root / "collection"

    def tearDown(self):
        self.temp.cleanup()

    def write(self, path, data):
        path.write_text(json.dumps(data), encoding="utf-8")

    def batch(self, name="base", identifier="papal.test.one", language="la", status="compiled", pages=2):
        folder = self.root / name
        folder.mkdir()
        (folder / 'title "&.tex').write_text("Synthetic TeX fixture.")
        (folder / "title.body.tex").write_text("Synthetic body fixture.")
        pdf = folder / 'title "&.pdf'
        pdf.write_bytes(("%PDF-1.7 synthetic fixture: " + name).encode())
        source_sha = hashlib.sha256((name + " source").encode()).hexdigest()
        doc = {"id": identifier, "language": language, "title": "Synthetic title " + name,
               "pope": "Synthetic issuer", "date": "1903-01-01", "artifact_id": "artifact.test." + name,
               "sha256": source_sha, "segment_id": "segment.test." + name,
               "physical_line_ranges": [[1, 2]], "text": "SOURCE BODY MUST NEVER BE COPIED"}
        item = {"id": identifier, "language": language, "artifact_id": doc["artifact_id"],
                "source_sha256": source_sha, "segment_id": doc["segment_id"],
                "physical_line_ranges": doc["physical_line_ranges"], "status": status,
                "tex": 'title "&.tex', "body_tex": "title.body.tex"}
        if status == "compiled":
            item.update(pdf=pdf.name, pdf_sha256=hashlib.sha256(pdf.read_bytes()).hexdigest(), pages=pages,
                        text_fidelity={"status": "pass"})
        manifest = {"schema": collection.MANIFEST_SCHEMA, "revision": "2026-10-26T05:10:28Z", "documents": [doc]}
        receipt = {"schema": collection.RECEIPT_SCHEMA, "revision": manifest["revision"], "documents": [item],
                   "summary": {"selected": 1, "compiled": int(status == "compiled"), "failed": int(status == "failed")}}
        spec = {"name": name, "receipt": folder / "receipt.json", "manifest": folder / "manifest.json"}
        self.write(spec["receipt"], receipt)
        self.write(spec["manifest"], manifest)
        return spec, manifest, receipt

    def corrections(self, prior, replacement, reason="Synthetic correction"):
        path = self.root / "corrections.json"
        data = {"schema": collection.MANIFEST_SCHEMA, "revision": "2026-10-26T06:00:00Z", "documents": [],
                "supersessions": [{"prior": {key: prior[key] for key in
                    ("id", "language", "pdf_sha256", "artifact_id", "source_sha256", "segment_id")},
                    "replacement": replacement, "reason": reason}]}
        self.write(path, data)
        return path, data

    def review(self, spec, receipt, status="PASS"):
        report = self.root / "review.md"
        report.write_text("Synthetic all-page layout inspection report.\n")
        row = receipt["documents"][0]
        record = {"id": row["id"], "language": row["language"], "pdf_sha256": row["pdf_sha256"],
                  "pages": row["pages"], "status": status, "report": report.relative_to(ROOT).as_posix(),
                  "report_sha256": hashlib.sha256(report.read_bytes()).hexdigest(),
                  "individually_inspected_pages": list(range(1, row["pages"] + 1)), "reused_pages": []}
        data = {"schema": collection.REVIEW_SCHEMA, "frozen_receipt_sha256": hashlib.sha256(spec["receipt"].read_bytes()).hexdigest(),
                "documents": [record]}
        path = self.root / "review.json"
        self.write(path, data)
        return path, data

    def test_merges_distinct_witnesses_without_copying_source_bodies(self):
        first, _, _ = self.batch("z-corpus")
        second, _, _ = self.batch("a-corpus", "bullarium.test.other", language="mul")
        result = collection.collect_batches([first, second], self.out)
        self.assertEqual(result["summary"]["compiled"], 2)
        self.assertEqual(result["summary"]["layout_reviewed"], 0)
        self.assertEqual([row["corpus"] for row in result["documents"]], ["a-corpus", "z-corpus"])
        self.assertEqual(result["documents"][0]["language_label"], "Multilingual")
        page = (self.out / "index.html").read_text()
        self.assertIn("PDF (review pending)", page)
        self.assertIn("Page review not recorded", page)
        self.assertNotIn("SOURCE BODY MUST NEVER BE COPIED", page + json.dumps(result))

    def test_metadata_and_local_links_are_escaped_and_encoded(self):
        spec, manifest, _ = self.batch()
        manifest["documents"][0]["title"] = '</script><img src=x onerror="bad()"> & title'
        spec["name"] = '<script>bad()</script>'
        self.write(spec["manifest"], manifest)
        result = collection.collect_batches([spec], self.out)
        page = (self.out / "index.html").read_text()
        self.assertNotIn('<img src=x', page)
        self.assertIn('&lt;/script&gt;&lt;img', page)
        self.assertNotIn('<script>bad()', page)
        self.assertIn('%22%26.pdf', result["documents"][0]["files"]["pdf"])

    def test_tampered_or_missing_successful_pdf_refuses_before_output(self):
        spec, _, receipt = self.batch()
        pdf = spec["receipt"].parent / receipt["documents"][0]["pdf"]
        for mutation in (lambda: pdf.write_bytes(b"changed"), lambda: pdf.unlink()):
            mutation()
            with self.assertRaises(collection.PapalCollectionError):
                collection.collect_batches([spec], self.out)
            self.assertFalse(self.out.exists())

    def test_pdf_and_tex_traversal_and_symlink_escape_refuse(self):
        spec, _, receipt = self.batch()
        for field in ("pdf", "tex", "body_tex"):
            for value in ("../escape" + (".pdf" if field == "pdf" else ".tex"), "/tmp/escape.tex", "null\x00.tex"):
                changed = copy.deepcopy(receipt)
                changed["documents"][0][field] = value
                self.write(spec["receipt"], changed)
                with self.subTest(field=field, value=value), self.assertRaises(collection.PapalCollectionError):
                    collection.collect_batches([spec], self.out)
        self.write(spec["receipt"], receipt)
        pdf = spec["receipt"].parent / receipt["documents"][0]["pdf"]
        outside = self.root / "outside.pdf"
        outside.write_bytes(pdf.read_bytes())
        pdf.unlink()
        pdf.symlink_to(outside)
        with self.assertRaisesRegex(collection.PapalCollectionError, "escapes"):
            collection.collect_batches([spec], self.out)

    def test_receipt_is_bound_to_frozen_revision_and_source_selection(self):
        spec, manifest, receipt = self.batch()
        for key, value in (("artifact_id", "artifact.wrong"), ("source_sha256", "0" * 64),
                           ("segment_id", "segment.wrong"), ("physical_line_ranges", [[1, 3]])):
            changed = copy.deepcopy(receipt)
            changed["documents"][0][key] = value
            self.write(spec["receipt"], changed)
            with self.subTest(key=key), self.assertRaisesRegex(collection.PapalCollectionError, "disagree"):
                collection.collect_batches([spec], self.out)
        self.write(spec["receipt"], receipt)
        manifest["revision"] = "2026-10-26T06:00:00Z"
        self.write(spec["manifest"], manifest)
        with self.assertRaisesRegex(collection.PapalCollectionError, "revisions"):
            collection.collect_batches([spec], self.out)

    def test_declared_frozen_manifest_pins_metadata_bytes_and_retained_file(self):
        spec, manifest, receipt = self.batch()
        frozen = spec["receipt"].parent / "frozen-manifest.json"
        frozen.write_bytes(spec["manifest"].read_bytes())
        receipt.update(input_manifest=frozen.name, input_manifest_sha256=hashlib.sha256(frozen.read_bytes()).hexdigest())
        self.write(spec["receipt"], receipt)
        self.assertEqual(collection.collect_batches([spec], self.out)["summary"]["compiled"], 1)
        manifest["documents"][0]["title"] = "Changed metadata with identical source artifact pins"
        self.write(spec["manifest"], manifest)
        with self.assertRaisesRegex(collection.PapalCollectionError, "frozen-manifest bytes"):
            collection.collect_batches([spec], self.out)
        spec["manifest"].write_bytes(frozen.read_bytes())
        frozen.write_text("changed retained bytes")
        with self.assertRaisesRegex(collection.PapalCollectionError, "frozen-manifest bytes"):
            collection.collect_batches([spec], self.out)

    def test_duplicate_active_identity_refuses_even_when_bytes_match(self):
        first, _, _ = self.batch("first")
        second, _, _ = self.batch("second")
        with self.assertRaisesRegex(collection.PapalCollectionError, "duplicate active"):
            collection.collect_batches([first, second], self.out)

    def test_exact_same_identity_supersession_removes_only_old_pdf(self):
        first, _, old = self.batch("old")
        second, _, new = self.batch("new")
        prior = old["documents"][0]
        replacement = {key: new["documents"][0][key] for key in ("id", "language", "artifact_id", "source_sha256", "segment_id")}
        path, _ = self.corrections(prior, replacement)
        result = collection.collect_batches([first, second], self.out, [path])
        self.assertEqual(result["summary"]["compiled"], 1)
        self.assertEqual(result["summary"]["excluded"], 1)
        self.assertEqual(result["documents"][0]["pdf_sha256"], new["documents"][0]["pdf_sha256"])
        self.assertNotIn('../old/', (self.out / "index.html").read_text())

    def test_distinct_replacement_and_explicit_withdrawal(self):
        first, _, old = self.batch("old")
        second, _, _ = self.batch("new", "papal.test.one.notes-v2")
        path, data = self.corrections(old["documents"][0], {"id": "papal.test.one.notes-v2", "language": "la"})
        result = collection.collect_batches([first, second], self.out, [path])
        self.assertEqual(result["documents"][0]["id"], "papal.test.one.notes-v2")
        data["supersessions"][0]["replacement"] = None
        self.write(path, data)
        result = collection.collect_batches([first], self.out, [path])
        self.assertEqual(result["summary"]["documents"], 0)
        self.assertEqual(result["summary"]["excluded"], 1)

    def test_supersession_missing_replacement_bad_hash_or_conflict_refuse(self):
        spec, _, receipt = self.batch()
        path, data = self.corrections(receipt["documents"][0], {"id": "missing", "language": "la"})
        for variant in (data,
                        {**data, "supersessions": [{**data["supersessions"][0], "replacement": None,
                            "prior": {**data["supersessions"][0]["prior"], "pdf_sha256": "0" * 64}}]},
                        {**data, "supersessions": [data["supersessions"][0]] * 2}):
            self.write(path, variant)
            with self.assertRaises(collection.PapalCollectionError):
                collection.collect_batches([spec], self.out, [path])
        data["supersessions"][0].pop("replacement")
        self.write(path, data)
        with self.assertRaisesRegex(collection.PapalCollectionError, "explicit null"):
            collection.collect_batches([spec], self.out, [path])

    def test_supersession_source_pins_cannot_match_another_witness(self):
        first, _, old = self.batch("old")
        second, _, _ = self.batch("new", "papal.test.new")
        path, data = self.corrections(old["documents"][0], {"id": "papal.test.new", "language": "la", "artifact_id": "wrong"})
        with self.assertRaisesRegex(collection.PapalCollectionError, "source pin"):
            collection.collect_batches([first, second], self.out, [path])
        data["supersessions"][0]["replacement"].pop("artifact_id")
        data["supersessions"][0]["prior"]["source_sha256"] = "f" * 64
        self.write(path, data)
        with self.assertRaisesRegex(collection.PapalCollectionError, "source pin"):
            collection.collect_batches([first, second], self.out, [path])

    def test_only_exact_all_page_layout_review_is_claimed(self):
        spec, _, receipt = self.batch()
        path, _ = self.review(spec, receipt)
        result = collection.collect_batches([spec], self.out, review_manifests=[path])
        self.assertEqual(result["summary"]["layout_reviewed"], 1)
        self.assertIn("Layout reviewed", (self.out / "index.html").read_text())

    def test_incomplete_duplicate_or_boolean_page_coverage_refuses(self):
        spec, _, receipt = self.batch()
        path, data = self.review(spec, receipt)
        for inspected, reused in (([1], []), ([1, 1, 2], []), ([True, 2], []), ([1, 2], [2])):
            changed = copy.deepcopy(data)
            changed["documents"][0].update(individually_inspected_pages=inspected, reused_pages=reused)
            self.write(path, changed)
            with self.subTest(inspected=inspected, reused=reused), self.assertRaises(collection.PapalCollectionError):
                collection.collect_batches([spec], self.out, review_manifests=[path])

    def test_stale_review_does_not_approve_new_pdf_and_bad_report_refuses(self):
        spec, _, receipt = self.batch()
        path, data = self.review(spec, receipt)
        data["documents"][0]["pdf_sha256"] = "f" * 64
        self.write(path, data)
        result = collection.collect_batches([spec], self.out, review_manifests=[path])
        self.assertEqual(result["summary"]["layout_reviewed"], 0)
        self.assertEqual(result["unmatched_review_entries"], 1)
        data["documents"][0]["pdf_sha256"] = receipt["documents"][0]["pdf_sha256"]
        data["documents"][0]["report_sha256"] = "f" * 64
        self.write(path, data)
        with self.assertRaisesRegex(collection.PapalCollectionError, "report SHA"):
            collection.collect_batches([spec], self.out, review_manifests=[path])

    def test_review_receipt_provenance_and_page_count_are_pinned(self):
        spec, _, receipt = self.batch()
        path, data = self.review(spec, receipt)
        for key, value in (("receipt_sha256", "invalid hash"), ("pages", 3)):
            changed = copy.deepcopy(data)
            changed["documents"][0][key] = value
            self.write(path, changed)
            with self.subTest(key=key), self.assertRaises(collection.PapalCollectionError):
                collection.collect_batches([spec], self.out, review_manifests=[path])

    def test_exact_pdf_review_survives_receipt_metadata_changes_with_both_hashes(self):
        spec, _, receipt = self.batch()
        path, data = self.review(spec, receipt)
        original = data["frozen_receipt_sha256"]
        receipt["input_note"] = "Receipt metadata changed; PDF bytes remain exact."
        self.write(spec["receipt"], receipt)
        result = collection.collect_batches([spec], self.out, review_manifests=[path])
        self.assertEqual(result["summary"]["layout_reviewed"], 1)
        evidence = result["documents"][0]["page_review"]
        self.assertEqual(evidence["review_receipt_sha256"], original)
        self.assertEqual(evidence["current_receipt_sha256"], hashlib.sha256(spec["receipt"].read_bytes()).hexdigest())
        self.assertNotEqual(evidence["review_receipt_sha256"], evidence["current_receipt_sha256"])
        self.assertEqual(evidence["receipt_binding"], "exact-pdf-bytes")

    def test_receipt_portability_requires_complete_exact_pdf_review_evidence(self):
        spec, _, receipt = self.batch()
        path, data = self.review(spec, receipt)
        receipt["input_note"] = "Receipt metadata changed."
        self.write(spec["receipt"], receipt)
        for changes in ({"individually_inspected_pages": [1]}, {"report_sha256": "f" * 64}, {"status": "PENDING"}):
            changed = copy.deepcopy(data)
            changed["documents"][0].update(changes)
            self.write(path, changed)
            with self.subTest(changes=changes), self.assertRaises(collection.PapalCollectionError):
                collection.collect_batches([spec], self.out, review_manifests=[path])
        changed = copy.deepcopy(data)
        changed["documents"][0]["pdf_sha256"] = "f" * 64
        self.write(path, changed)
        result = collection.collect_batches([spec], self.out, review_manifests=[path])
        self.assertEqual(result["summary"]["layout_reviewed"], 0)

    def test_pending_preview_is_labelled_and_rejected_layout_has_no_pdf_link(self):
        spec, _, receipt = self.batch()
        path, data = self.review(spec, receipt, "PENDING")
        pending = collection.collect_batches([spec], self.out, review_manifests=[path])
        self.assertIn("pdf", pending["documents"][0]["files"])
        data["documents"][0]["status"] = "CHANGES_REQUIRED"
        self.write(path, data)
        rejected = collection.collect_batches([spec], self.out, review_manifests=[path])
        self.assertNotIn("pdf", rejected["documents"][0]["files"])
        self.assertEqual(rejected["summary"]["changes_required"], 1)
        self.assertNotIn('title%20%22%26.pdf', (self.out / "index.html").read_text())

    def test_reuse_requires_one_equal_raster_proof_for_every_reused_page(self):
        spec, _, receipt = self.batch()
        path, data = self.review(spec, receipt)
        review = data["documents"][0]
        review.update(individually_inspected_pages=[1], reused_pages=[2], reuse_proofs=[{
            "page": 2, "current_raster_sha256": "a" * 64, "prior_raster_sha256": "a" * 64,
            "prior_report": review["report"], "prior_report_sha256": review["report_sha256"],
            "prior_pdf_sha256": "b" * 64}])
        self.write(path, data)
        self.assertEqual(collection.collect_batches([spec], self.out, review_manifests=[path])["summary"]["layout_reviewed"], 1)
        review["reuse_proofs"][0]["prior_raster_sha256"] = "c" * 64
        self.write(path, data)
        with self.assertRaisesRegex(collection.PapalCollectionError, "equal exact raster"):
            collection.collect_batches([spec], self.out, review_manifests=[path])

    def test_tampering_prior_review_breaks_the_reuse_approval_chain(self):
        spec, _, receipt = self.batch()
        path, data = self.review(spec, receipt)
        prior = self.root / "prior-review.md"
        prior.write_text("Synthetic prior individual inspection.\n")
        data["documents"][0].update(individually_inspected_pages=[1], reused_pages=[2], reuse_proofs=[{
            "page": 2, "current_raster_sha256": "a" * 64, "prior_raster_sha256": "a" * 64,
            "prior_report": prior.relative_to(ROOT).as_posix(),
            "prior_report_sha256": hashlib.sha256(prior.read_bytes()).hexdigest(),
            "prior_pdf_sha256": "b" * 64, "equality_method": "exact PNG bytes",
            "renderer_fingerprint": {"renderer": "synthetic fixture"}}])
        self.write(path, data)
        result = collection.collect_batches([spec], self.out, review_manifests=[path])
        proof = result["documents"][0]["page_review"]["reuse_proofs"][0]
        self.assertEqual(proof["equality_method"], "exact PNG bytes")
        self.assertEqual(proof["renderer_fingerprint"], {"renderer": "synthetic fixture"})
        prior.write_text("Prior report changed after its hash was recorded.\n")
        with self.assertRaisesRegex(collection.PapalCollectionError, "prior visual report SHA"):
            collection.collect_batches([spec], self.out, review_manifests=[path])

    def test_failed_and_render_only_results_never_link_a_pdf(self):
        failed, _, _ = self.batch("failed", status="failed")
        rendered, _, _ = self.batch("rendered", "papal.test.rendered", status="rendered")
        result = collection.collect_batches([failed, rendered], self.out)
        self.assertEqual(result["summary"]["compiled"], 0)
        self.assertTrue(all("pdf" not in row["files"] for row in result["documents"]))

    def test_duplicate_json_keys_and_nonfinite_values_refuse(self):
        spec, _, _ = self.batch()
        for body in ('{"schema":1,"schema":2}', '{"value":NaN}'):
            spec["receipt"].write_text(body)
            with self.assertRaises(collection.PapalCollectionError):
                collection.collect_batches([spec], self.out)

    def test_collection_cannot_replace_batch_index_or_follow_output_symlinks(self):
        spec, _, _ = self.batch()
        with self.assertRaisesRegex(collection.PapalCollectionError, "replace a batch"):
            collection.collect_batches([spec], spec["receipt"].parent)
        self.out.mkdir()
        target = self.root / "unrelated.html"
        target.write_text("untouched")
        (self.out / "index.html").symlink_to(target)
        with self.assertRaisesRegex(collection.PapalCollectionError, "symlink"):
            collection.collect_batches([spec], self.out)
        self.assertFalse((self.out / "collection.json").exists())
        self.assertEqual(target.read_text(), "untouched")


if __name__ == "__main__":
    unittest.main()
