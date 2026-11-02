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

    def test_collection_binds_original_row_revision_and_corpus(self):
        spec, manifest, receipt = self.batch()
        manifest["documents"][0].update(revision="2026-10-26T04:00:00Z", collection_corpus="original corpus")
        receipt["documents"][0]["render_revision"] = "2026-10-26T04:00:00Z"
        self.write(spec["manifest"], manifest)
        self.write(spec["receipt"], receipt)
        result = collection.collect_batches([spec], self.out)
        self.assertEqual(result["documents"][0]["render_revision"], "2026-10-26T04:00:00Z")
        self.assertEqual(result["documents"][0]["corpus"], "original corpus")
        receipt["documents"][0].pop("render_revision")
        self.write(spec["receipt"], receipt)
        with self.assertRaisesRegex(collection.PapalCollectionError, "render revisions"):
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


    def test_collection_preserves_metadata_inputs_aliased_by_output_endpoints(self):
        for kind in ("manifest", "receipt", "supersession", "review"):
            with self.subTest(kind=kind):
                spec, _, receipt = self.batch(kind)
                target = self.out / "collection.json"
                self.out.mkdir(exist_ok=True)
                navigation = self.out / "index.html"
                navigation.write_bytes(b"existing navigation must survive refusal")
                kwargs = {}
                if kind in {"manifest", "receipt"}:
                    target.write_bytes(spec[kind].read_bytes())
                    spec[kind] = target
                elif kind == "supersession":
                    path, _ = self.corrections(receipt["documents"][0], None)
                    target.write_bytes(path.read_bytes())
                    kwargs["supersession_manifests"] = [target]
                else:
                    path, _ = self.review(spec, receipt)
                    target.write_bytes(path.read_bytes())
                    kwargs["review_manifests"] = [target]
                before = {path: path.read_bytes() for path in (target, navigation)}
                with self.assertRaises(collection.PapalCollectionError):
                    collection.collect_batches([spec], self.out, **kwargs)
                self.assertEqual({path: path.read_bytes() for path in before}, before)

    def test_collection_preserves_current_and_reused_prior_report_output_aliases(self):
        spec, _, receipt = self.batch()
        path, audit = self.review(spec, receipt)
        self.out.mkdir()
        collection_path = self.out / "collection.json"
        report_path = self.out / "index.html"
        for prior in (False, True):
            with self.subTest(prior=prior):
                collection_path.write_bytes(b"previous metadata")
                report_path.write_bytes(b"exact hashed review report")
                row = copy.deepcopy(audit["documents"][0])
                if prior:
                    row["individually_inspected_pages"] = [1]
                    row["reused_pages"] = [2]
                    row["reuse_proofs"] = [{"page": 2, "current_raster_sha256": "a" * 64,
                        "prior_raster_sha256": "a" * 64, "prior_pdf_sha256": "b" * 64,
                        "prior_report": report_path.relative_to(ROOT).as_posix(),
                        "prior_report_sha256": hashlib.sha256(report_path.read_bytes()).hexdigest()}]
                else:
                    row["report"] = report_path.relative_to(ROOT).as_posix()
                    row["report_sha256"] = hashlib.sha256(report_path.read_bytes()).hexdigest()
                self.write(path, dict(audit, documents=[row]))
                before = {item: item.read_bytes() for item in (path, collection_path, report_path)}
                with self.assertRaisesRegex(collection.PapalCollectionError, "collides"):
                    collection.collect_batches([spec], self.out, review_manifests=[path])
                self.assertEqual({item: item.read_bytes() for item in before}, before)


class SourcePlanTests(unittest.TestCase):
    setUp = CollectionTests.setUp
    tearDown = CollectionTests.tearDown
    write = CollectionTests.write
    batch = CollectionTests.batch

    def component(self, name, identifier="papal.test.one", revision="2026-10-26T05:10:28Z"):
        spec, manifest, _ = self.batch(name, identifier)
        manifest["revision"] = revision
        manifest["documents"][0].pop("text")
        manifest["documents"][0]["text_path"] = "src/sources/synthetic/" + name + "/text.txt"
        self.write(spec["manifest"], manifest)
        return {"name": name, "path": spec["manifest"]}, manifest

    def correction(self, base, data, name="correction"):
        path = self.root / (name + ".json")
        changed = copy.deepcopy(data)
        changed["revision"] = "2026-10-26T06:00:00Z"
        changed["base_manifest_sha256"] = hashlib.sha256(base["path"].read_bytes()).hexdigest()
        changed["documents"][0]["title"] = "Explicit corrected display title"
        self.write(path, changed)
        return {"name": name, "path": path}, changed

    def plan(self, bases, corrections=()):
        return collection.plan_sources(bases, corrections, self.root / "current.json")

    def test_additive_rows_retain_revisions_and_distinct_witness_ids(self):
        base, _ = self.component("base")
        delta, _ = self.component("delta", "historical.test.same-act.other-witness", "2026-10-26T07:00:00Z")
        delta["role"] = "delta"
        result = self.plan([base, delta])
        rows = {row["id"]: row for row in result["documents"]}
        self.assertEqual(result["revision"], "2026-10-26T07:00:00Z")
        self.assertEqual(rows["papal.test.one"]["revision"], "2026-10-26T05:10:28Z")
        self.assertEqual(rows["historical.test.same-act.other-witness"]["revision"], "2026-10-26T07:00:00Z")
        self.assertEqual(result["selection_plan"]["inputs"][1]["role"], "delta")

    def test_explicit_row_revision_precedes_component_revision(self):
        base, data = self.component("base")
        data["documents"][0]["revision"] = "2026-10-26T03:00:00Z"
        self.write(base["path"], data)
        self.assertEqual(self.plan([base])["documents"][0]["revision"], "2026-10-26T03:00:00Z")

    def test_same_source_metadata_override_needs_no_fabricated_pdf_hash(self):
        base, data = self.component("base")
        correction, changed = self.correction(base, data)
        result = self.plan([base], [correction])
        self.assertEqual(result["documents"][0]["title"], changed["documents"][0]["title"])
        self.assertEqual(result["documents"][0]["collection_corpus"], "base")
        self.assertEqual(result["selection_plan"]["summary"]["metadata_overrides"], 1)
        prior = result["selection_plan"]["exclusions"][0]["prior"]
        self.assertEqual(prior["selection"]["manifest_sha256"], hashlib.sha256(base["path"].read_bytes()).hexdigest())
        self.assertNotIn("pdf_sha256", json.dumps(result))
        changed.pop("base_manifest_sha256")
        self.write(correction["path"], changed)
        self.assertEqual(self.plan([base], [correction])["selection_plan"]["summary"]["selected"], 1)

    def test_incorrect_declared_base_pin_refuses(self):
        base, data = self.component("base")
        correction, changed = self.correction(base, data)
        changed["base_manifest_sha256"] = "f" * 64
        self.write(correction["path"], changed)
        with self.assertRaisesRegex(collection.PapalCollectionError, "base manifest"):
            self.plan([base], [correction])

    def test_changed_bounds_without_exact_prior_supersession_refuse(self):
        base, data = self.component("base")
        correction, changed = self.correction(base, data)
        changed["documents"][0]["physical_line_ranges"] = [[1, 3]]
        self.write(correction["path"], changed)
        with self.assertRaisesRegex(collection.PapalCollectionError, "explicit source supersession"):
            self.plan([base], [correction])

    def test_source_identity_comparison_does_not_coerce_boolean_or_float_bounds(self):
        base, data = self.component("base")
        correction, changed = self.correction(base, data)
        for start in (True, 1.0):
            changed["documents"][0]["physical_line_ranges"] = [[start, 2]]
            self.write(correction["path"], changed)
            with self.subTest(start=start), self.assertRaisesRegex(collection.PapalCollectionError, "explicit source supersession"):
                self.plan([base], [correction])

    def test_explicit_source_supersession_and_withdrawal_preserve_provenance(self):
        base, data = self.component("base")
        other, other_data = self.component("other", "papal.test.withdraw")
        correction, changed = self.correction(base, data)
        old = data["documents"][0]
        new = changed["documents"][0]
        new["id"] = "papal.test.one.notes-v2"
        new["physical_line_ranges"] = [[1, 3]]
        prior = {"id": old["id"], "language": old["language"], "artifact_id": old["artifact_id"],
                 "source_sha256": old["sha256"], "segment_id": old["segment_id"]}
        withdrawn = other_data["documents"][0]
        changed.pop("base_manifest_sha256")
        changed["supersessions"] = [
            {"prior": prior, "replacement": {**prior, "id": new["id"]}, "reason": "Exact source-boundary correction."},
            {"prior": {"id": withdrawn["id"], "language": withdrawn["language"], "artifact_id": withdrawn["artifact_id"],
                       "source_sha256": withdrawn["sha256"], "segment_id": withdrawn["segment_id"]},
             "replacement": None, "reason": "Explicit withdrawal."}]
        self.write(correction["path"], changed)
        result = self.plan([base, other], [correction])
        self.assertEqual([row["id"] for row in result["documents"]], [new["id"]])
        self.assertEqual(result["selection_plan"]["summary"]["source_supersessions"], 1)
        self.assertEqual(result["selection_plan"]["summary"]["withdrawals"], 1)
        changed["supersessions"][0]["prior"].pop("segment_id")
        self.write(correction["path"], changed)
        with self.assertRaisesRegex(collection.PapalCollectionError, "segment pin"):
            self.plan([base, other], [correction])

    def test_unexplained_additive_collision_or_orphan_correction_refuses(self):
        first, data = self.component("first")
        second, _ = self.component("second")
        with self.assertRaisesRegex(collection.PapalCollectionError, "collision"):
            self.plan([first, second])
        correction, changed = self.correction(first, data)
        changed["documents"][0]["id"] = "unproven.new.identifier"
        self.write(correction["path"], changed)
        with self.assertRaisesRegex(collection.PapalCollectionError, "proven predecessor"):
            self.plan([first], [correction])

    def test_correction_cannot_collapse_distinct_witnesses_into_one_replacement(self):
        first, data = self.component("first")
        second, other = self.component("second", "papal.test.other-witness")
        correction, changed = self.correction(first, data)
        changed.pop("base_manifest_sha256")
        changed["documents"][0]["id"] = "papal.test.replacement"
        replacement = changed["documents"][0]
        target = {"id": replacement["id"], "language": replacement["language"],
                  "artifact_id": replacement["artifact_id"], "source_sha256": replacement["sha256"],
                  "segment_id": replacement["segment_id"]}
        changed["supersessions"] = [{"prior": {"id": row["id"], "language": row["language"],
            "artifact_id": row["artifact_id"], "source_sha256": row["sha256"], "segment_id": row["segment_id"]},
            "replacement": target, "reason": "Synthetic attempted convergence."}
            for row in (data["documents"][0], other["documents"][0])]
        self.write(correction["path"], changed)
        with self.assertRaisesRegex(collection.PapalCollectionError, "uniquely proven predecessor"):
            self.plan([first, second], [correction])

    def test_source_plan_is_deterministic_and_never_mutates_components(self):
        base, data = self.component("base")
        correction, _ = self.correction(base, data)
        pins = {item["path"]: item["path"].read_bytes() for item in (base, correction)}
        self.plan([base], [correction])
        first = (self.root / "current.json").read_bytes()
        self.plan([base], [correction])
        self.assertEqual(first, (self.root / "current.json").read_bytes())
        self.assertTrue(all(path.read_bytes() == payload for path, payload in pins.items()))

    def test_inline_source_body_is_refused_not_copied(self):
        base, data = self.component("base")
        data["documents"][0]["text"] = "Synthetic source body must remain under its own artifact."
        self.write(base["path"], data)
        with self.assertRaisesRegex(collection.PapalCollectionError, "never copied source bodies"):
            self.plan([base])

    def test_source_plan_cannot_overwrite_its_frozen_input(self):
        base, _ = self.component("base")
        before = base["path"].read_bytes()
        with self.assertRaisesRegex(collection.PapalCollectionError, "replace an input"):
            collection.plan_sources([base], [], base["path"])
        self.assertEqual(base["path"].read_bytes(), before)

    def test_source_plan_cannot_follow_an_output_symlink(self):
        base, _ = self.component("base")
        target = self.root / "unrelated.json"
        target.write_text("untouched")
        output = self.root / "current.json"
        output.symlink_to(target)
        with self.assertRaisesRegex(collection.PapalCollectionError, "symlink"):
            self.plan([base])
        self.assertEqual(target.read_text(), "untouched")

    def test_actual_confirmed_geometry_withdrawals_override_positive_source_selections(self):
        source = ROOT / "src/sources/papal-documents"
        geometry = source / "bullarium-geometry-manifest.json"
        negative = source / "bullarium-active-withdrawals.json"
        positive = json.loads(geometry.read_text())
        negative_bytes = negative.read_bytes()
        withdrawal = json.loads(negative_bytes)
        geometry_keys = {(row["id"], row["language"]) for row in positive["documents"]}
        self.assertTrue(geometry_keys)
        assertions = [row for row in withdrawal["supersessions"]
                      if (row["prior"]["id"], row["prior"]["language"]) in geometry_keys]
        withdrawn_keys = {(row["prior"]["id"], row["prior"]["language"]) for row in assertions}
        self.assertGreaterEqual(len(withdrawn_keys), 4)
        self.assertTrue(all(row["replacement"] is None for row in assertions))
        subset = self.root / "actual-geometry-withdrawals.json"
        self.write(subset, {"schema": collection.MANIFEST_SCHEMA, "revision": withdrawal["revision"],
                           "documents": [], "supersessions": assertions,
                           "source_inventory_sha256": hashlib.sha256(negative_bytes).hexdigest()})
        result = self.plan([{"name": "actual-geometry", "path": geometry}],
                           [{"name": "actual-withdrawals", "path": subset}])
        selected = {(row["id"], row["language"]) for row in result["documents"]}
        self.assertEqual(selected, geometry_keys - withdrawn_keys)
        self.assertEqual(result["selection_plan"]["summary"]["withdrawals"], len(withdrawn_keys))

    def test_last_reader_withdrawal_replaces_index_but_preserves_pdf_and_provenance(self):
        base, data = self.component("base")
        spec = {"name": "base", "manifest": base["path"], "receipt": base["path"].parent / "receipt.json"}
        before = collection.collect_batches([spec], self.out)
        old_pdf_url = before["documents"][0]["files"]["pdf"]
        pdf = base["path"].parent / 'title "&.pdf'
        original_pdf = pdf.read_bytes()
        old = data["documents"][0]
        negative = self.root / "withdrawals.json"
        self.write(negative, {"schema": collection.MANIFEST_SCHEMA, "revision": "2026-10-26T07:00:00Z", "documents": [],
            "supersessions": [{"prior": {"id": old["id"], "language": old["language"], "artifact_id": old["artifact_id"],
                "source_sha256": old["sha256"], "segment_id": old["segment_id"]}, "replacement": None,
                "reason": "Synthetic source-only withdrawal; no prior PDF hash is asserted."}]})
        plan = self.plan([base], [{"name": "withdrawals", "path": negative}])
        result = collection.collect_empty_plan(self.root / "current.json", self.out)
        self.assertEqual(result["documents"], [])
        self.assertEqual(result["summary"]["compiled"], 0)
        self.assertEqual(result["summary"]["source_exclusions"], 1)
        self.assertEqual(result["source_selection_plan"]["provenance"], plan["selection_plan"])
        self.assertNotIn(old_pdf_url, (self.out / "index.html").read_text())
        self.assertIn("0 current readers", (self.out / "index.html").read_text())
        self.assertEqual(pdf.read_bytes(), original_pdf)

    def test_empty_collection_refuses_a_plan_with_active_readers(self):
        base, _ = self.component("base")
        self.plan([base])
        self.out.mkdir()
        index = self.out / "index.html"
        index.write_text("Existing index remains untouched on invalid input.")
        with self.assertRaisesRegex(collection.PapalCollectionError, "no active readers"):
            collection.collect_empty_plan(self.root / "current.json", self.out)
        self.assertEqual(index.read_text(), "Existing index remains untouched on invalid input.")

    def test_empty_collection_refuses_source_plan_output_collision_without_changing_files(self):
        base, data = self.component("base")
        data["documents"] = []
        self.write(base["path"], data)
        plan = self.plan([base])
        self.out.mkdir()
        for name in ("collection.json", "index.html"):
            source = self.out / name
            other = self.out / ("index.html" if name == "collection.json" else "collection.json")
            self.write(source, plan)
            other.write_text("Existing navigation and metadata must remain exact.")
            before = {path: path.read_bytes() for path in (source, other)}
            with self.subTest(name=name), self.assertRaisesRegex(collection.PapalCollectionError, "collides"):
                collection.collect_empty_plan(source, self.out)
            self.assertTrue(all(path.read_bytes() == payload for path, payload in before.items()))


if __name__ == "__main__":
    unittest.main()
