"""Source print readers preserve exact selections without PDF inputs."""
from __future__ import annotations

import hashlib
import html
import json
from pathlib import Path
import re
import sys
import tempfile
from types import SimpleNamespace
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))
import _print_catalog as catalog


def digest(payload):
    return hashlib.sha256(payload).hexdigest()


class SourceFixture(unittest.TestCase):
    def setUp(self):
        scratch = ROOT / ".scratch/source-html/tests"
        scratch.mkdir(parents=True, exist_ok=True)
        self.temp = tempfile.TemporaryDirectory(dir=scratch)
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.revision = "2026-10-30T00:00:00Z"
        self.text_path = "src/sources/works/test/container/editions/1903/artifacts/text/source.txt"
        self.segment_path = "src/sources/works/test/act/editions/1903/segments/body.toml"
        self.text = "UNSELECTED BEFORE\nSource heading <literal>\n\n1. Body & body [1].\n\n[1] Historical note; τέλος.\nUNSELECTED AFTER\n"
        self.write(self.text_path, self.text)
        self.source = {
            "id": "papal.fixture", "language": "en", "pope": "Fixture author", "title": "Source <title>",
            "date": "1903-01-01", "revision": self.revision,
            "text_path": self.text_path, "sha256": digest(self.text.encode()),
            "source_url": "https://example.org/source", "artifact_id": "artifact.test.text",
            "segment_id": "segment.test.act", "segment_path": self.segment_path,
            "physical_line_ranges": [[2, 6]], "rights_status": "public-domain",
            "rights_basis": "Synthetic fixture; not external wording.",
            "rights_notice": "Historical wording remains outside the project licence.",
            "source_note": "A historical fragment, preserving the ending note; OCR is not collation."}
        self.toml(str(Path(self.text_path).parent / "artifact.toml"), {
            "record_type": "artifact", "id": "artifact.test.text", "edition_id": "edition.test.container",
            "storage": "tracked", "rights_status": "public-domain", "rights_basis": self.source["rights_basis"],
            "sha256": self.source["sha256"], "byte_size": len(self.text.encode()),
            "path": self.text_path, "media_type": "text/plain; charset=utf-8"})
        self.toml(self.segment_path, {
            "schema": 2, "record_type": "segment", "id": "segment.test.act",
            "edition_id": "edition.test.act", "artifact_id": "artifact.test.text",
            "artifact_sha256": self.source["sha256"], "physical_line_ranges": [[2, 6]]})
        self.toml("src/sources/works/test/act/editions/1903/edition.toml", {
            "record_type": "edition", "id": "edition.test.act", "language": "en"})
        self.pdf = "pdf/papal-documents/1903-01-01--fixture--en--1234567890123456.pdf"
        self.reader = {"release_id": "papal.fixture", "language": "en", "pdf": self.pdf,
                       "pdf_sha256": "a" * 64, "pages": 1, "extent": "fragment", "witness": "Fixture 1903"}
        self.manifest = {"schema": catalog.papal.SCHEMA, "revision": self.revision, "documents": [self.source]}
        base = self.freeze("src/sources/papal-documents/base-manifest.json", self.manifest)
        self.plan = {**self.manifest, "selection_plan": {"schema": "triptych-papal-source-plan/v1", "inputs": [base]}}
        plan = self.freeze("release/papal-documents/inputs/plan.json", self.plan)
        manifest = self.freeze("release/papal-documents/inputs/manifest.json", self.manifest)
        rendered = {"id": "papal.fixture", "language": "en", "status": "compiled",
                    "pdf_sha256": "a" * 64, "pages": 1, "render_revision": self.revision,
                    "artifact_id": self.source["artifact_id"], "source_sha256": self.source["sha256"],
                    "segment_id": self.source["segment_id"], "physical_line_ranges": [[2, 6]],
                    "text_fidelity": {"status": "pass"}}
        receipt = self.freeze("release/papal-documents/inputs/receipt.json", {
            "revision": self.revision, "documents": [rendered], "input_manifest_sha256": manifest["sha256"]})
        report = self.freeze_text("release/papal-documents/reports/review.md", "All synthetic pages reviewed.\n")
        audit = self.freeze("release/papal-documents/inputs/audit.json", {
            "frozen_receipt_sha256": receipt["sha256"], "documents": [{
                "id": "papal.fixture", "language": "en", "status": "PASS", "pdf_sha256": "a" * 64,
                "pages": 1, "individually_inspected_pages": [1], "reused_pages": [], "reuse_proofs": [],
                "report": "review.md", "report_sha256": report["sha256"]}]})
        self.release = {"documents": [{"id": "papal.fixture", "language": "en", "pdf": self.pdf,
            "pdf_sha256": "a" * 64, "pages": 1, "source": self.source, "render_revision": self.revision,
            "manifest": {**manifest, "row_index": 0}, "receipt": {**receipt, "row_index": 0},
            "review": {"status": "PASS", "audit": {**audit, "row_index": 0}, "reports": {"review.md": report},
                       "original_receipt_sha256": receipt["sha256"], "current_receipt_sha256": receipt["sha256"]}}],
            "source_plan": plan}
        self.save_release()
        self.save_index()

    def write(self, path, text):
        target = self.root / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(text, encoding="utf-8")

    def toml(self, path, data):
        self.write(path, "\n".join(key + " = " + json.dumps(value) for key, value in data.items()) + "\n")

    def freeze_text(self, path, text):
        self.write(path, text)
        payload = text.encode()
        return {"path": path, "sha256": digest(payload), "bytes": len(payload)}

    def freeze(self, path, data):
        return self.freeze_text(path, json.dumps(data, ensure_ascii=False, sort_keys=True) + "\n")

    def save_release(self):
        self.freeze("release/papal-documents.json", self.release)

    def save_index(self):
        self.freeze("src/web/data/encyclicals/index.json", {
            "counts": {"readers": 1}, "encyclicals": [{"readers": [self.reader]}]})

    def test_bounded_fragment_notes_escape_and_no_pdf_presence(self):
        self.assertFalse((self.root / self.pdf).exists())
        pages = catalog._papal_pages(self.root)
        self.assertEqual(list(pages), ["papal-documents/1903-01-01--fixture--en--1234567890123456.html"])
        page = next(iter(pages.values()))
        body = page["html"]
        self.assertIn("Source &lt;title&gt;", body)
        self.assertIn("Source heading &lt;literal&gt;", body)
        self.assertIn("1. Body &amp; body [1].", body)
        self.assertIn("[1] Historical note; τέλος.", body)
        self.assertIn("Historical fragment", body)
        self.assertIn("OCR is not collation", body)
        self.assertIn("outside the project licence", body)
        self.assertNotIn("UNSELECTED", body)
        self.assertNotIn(self.revision, body)
        self.assertEqual(page["legacy_pdf"], self.pdf)
        self.assertIn(self.segment_path, page["source_paths"])
        self.assertFalse(any(path.endswith(".pdf") for path in page["source_paths"]))

    def test_sparse_artifact_without_family_declarations_has_no_source_pages(self):
        (self.root / "src/web/data/encyclicals/index.json").unlink()
        self.assertEqual(catalog.source_pages(self.root), {})
        self.assertEqual(catalog.legacy_pdf_routes(self.root), {})

    def test_missing_source_fails_instead_of_omitting_reader(self):
        (self.root / self.text_path).unlink()
        with self.assertRaises(catalog.papal.PapalTypesetError):
            catalog._papal_pages(self.root)

    def test_changed_plan_input_and_new_withdrawal_both_refuse(self):
        path = self.root / "src/sources/papal-documents/base-manifest.json"
        original = path.read_bytes()
        path.write_bytes(original + b" ")
        with self.assertRaisesRegex(catalog.PrintCatalogError, "SHA-256"):
            catalog._papal_pages(self.root)
        path.write_bytes(original)
        self.freeze("src/sources/papal-documents/new-withdrawals.json", {
            "schema": catalog.papal.SCHEMA, "supersessions": [{
                "prior": {"id": "papal.fixture", "language": "en"}, "replacement": None}]})
        with self.assertRaisesRegex(catalog.PrintCatalogError, "supersession"):
            catalog._papal_pages(self.root)

    def test_stale_source_bounds_cannot_expand_to_whole_parent(self):
        self.release["documents"][0]["source"]["physical_line_ranges"] = [[1, 7]]
        self.save_release()
        with self.assertRaisesRegex(catalog.PrintCatalogError, "source bounds"):
            catalog._papal_pages(self.root)

    def test_missing_review_page_refuses(self):
        row = self.release["documents"][0]
        audit = json.loads((self.root / row["review"]["audit"]["path"]).read_text())
        audit["documents"][0]["individually_inspected_pages"] = []
        row["review"]["audit"] = {**self.freeze(row["review"]["audit"]["path"], audit), "row_index": 0}
        self.save_release()
        with self.assertRaisesRegex(catalog.PrintCatalogError, "every page"):
            catalog._papal_pages(self.root)

    def test_only_browser_admitted_release_rows_are_published(self):
        self.release["documents"].append({"id": "papal.not-admitted", "language": "la"})
        self.save_release()
        self.assertEqual(len(catalog._papal_pages(self.root)), 1)

    def test_structured_headings_and_signature_remain_literal(self):
        document = {**self.source, "blocks": [{"kind": "heading", "text": "Source section <I>"},
            {"kind": "paragraph", "text": "Datum Romae. LEO PP. XIII. [1]"},
            {"kind": "paragraph", "text": "[1] Historical endnote."}]}
        body = catalog._papal_body(document, self.reader)
        self.assertIn("<h2>Source section &lt;I&gt;</h2>", body)
        self.assertIn("<p>Datum Romae. LEO PP. XIII. [1]</p>", body)
        self.assertIn("<p>[1] Historical endnote.</p>", body)

    def test_changed_bible_verse_bytes_cannot_publish_under_old_artifact(self):
        path = self.root / self.text_path
        path.write_text(self.text + "Changed verse words", encoding="utf-8")
        edition = SimpleNamespace(artifacts=path.parents[1], books=[SimpleNamespace(path=path)])
        module = SimpleNamespace(registry=lambda: {"douay-rheims": {"artifacts": "unused"}})
        with self.assertRaisesRegex(catalog.PrintCatalogError, "Bible verse artifact"):
            catalog._bible_sources(self.root, module, edition)

    def test_bible_printed_paragraph_mark_stays_distinct_from_projection(self):
        edition = SimpleNamespace(name_of=lambda token: "Genesis")
        body = catalog._verse_html(edition, [("Gen", 1, 1, "First & verse."),
            ("Gen", 1, 2, "Printed paragraph."), ("Gen", 1, 3, "Projected paragraph.")],
            {("Gen", 1, 2): "printed", ("Gen", 1, 3): "projected"})
        self.assertEqual(body.count('<p class="bible-paragraph">'), 3)
        self.assertIn('</sup> ¶ Printed paragraph.', body)
        self.assertIn('</sup> Projected paragraph.', body)
        self.assertEqual(body.count('¶'), 1)
        self.assertIn('First &amp; verse.', body)


class CorpusTests(unittest.TestCase):
    def test_all_admitted_papal_and_six_full_tracks_without_pdf_reads(self):
        original_read = Path.read_bytes
        original_open = Path.open
        original_validate = catalog.papal.validate_document
        checked = {}

        def retain_selection(source, root):
            document = original_validate(source, root)
            checked[(document["id"], document["language"])] = document
            return document

        def no_pdf_read(path, *args, **kwargs):
            if path.suffix.lower() == ".pdf":
                raise AssertionError("source HTML attempted to read a PDF")
            return original_read(path, *args, **kwargs)

        def no_pdf_open(path, *args, **kwargs):
            if path.suffix.lower() == ".pdf":
                raise AssertionError("source HTML attempted to open a PDF")
            return original_open(path, *args, **kwargs)

        with patch.object(Path, "read_bytes", no_pdf_read), patch.object(Path, "open", no_pdf_open), \
                patch.object(catalog.papal, "validate_document", retain_selection):
            pages = catalog.source_pages(ROOT)
        papal_pages = {k: v for k, v in pages.items() if k.startswith("papal-documents/")}
        plans = {k: v for k, v in pages.items() if k.startswith("reading-plans/") and v.get("legacy_pdf")}
        parts = {k: v for k, v in pages.items() if k.startswith("reading-plans/") and not v.get("legacy_pdf")}
        self.assertEqual(len(papal_pages), 350)
        self.assertEqual(len(plans), 6)
        self.assertEqual(len(parts), 24)
        released = {row["pdf"]: row for row in json.loads((ROOT / "release/papal-documents.json").read_text())["documents"]}
        for page in papal_pages.values():
            row = released[page["legacy_pdf"]]
            document = checked[(row["id"], row["language"])]
            rendered = re.search(r'<div class="source-text">(.*?)</div>', page["html"], re.S).group(1)
            words = html.unescape(re.sub(r"<[^>]*>", " ", rendered))
            self.assertEqual(" ".join(words.split()), " ".join(document["text"].split()), row["id"])
        for tier, expected_readings, expected_verses in (("landmarks", 36, 1210), ("story", 111, 3675),
                                                        ("full-account", 357, 13867)):
            page = plans[f"reading-plans/narrative-spine-{tier}-douay-rheims.html"]
            body = "\n".join(parts[route]["html"] for route in page["part_routes"]) if page.get("part_routes") else page["html"]
            self.assertEqual(body.count('<section id="reading-'), expected_readings)
            self.assertEqual(body.count('class="verse-number"'), expected_verses)
            self.assertNotIn('class="reading-refusal"', body)
        for page in plans.values():
            self.assertIn("Source text retains its own rights", page["html"])
            if "king-james" in page["legacy_pdf"]:
                self.assertIn("United Kingdom", page["html"])
                body = "\n".join(parts[route]["html"] for route in page["part_routes"]) if page.get("part_routes") else page["html"]
                self.assertIn('class="reading-refusal"', body)
        # Frozen before this partition: all twelve canonical period bodies,
        # including every heading, note, reference, verse label and refusal.
        historical_text_hashes = {
            "douay-rheims": "b503c7be2489baf0d58295b02130a0711a2f773ac36ec0063966356b74eebd5d",
            "king-james-version": "ddfbb04a7beff7b5ac663286e778cf299f331468eb692f6b613c40ffa0037ea8"}
        for edition, expected_sha in historical_text_hashes.items():
            page = plans[f"reading-plans/narrative-spine-full-account-{edition}.html"]
            self.assertEqual(len(page["part_routes"]), 12)
            self.assertIn("src/web/browser/shared/print-volume.js", page["source_paths"])
            self.assertIn('data-print-volume-ready="false"', page["html"])
            self.assertIn('data-print-volume-notice', page["html"])
            self.assertNotIn('class="verse-number"', page["html"])
            text, keys = [], []
            for route in page["part_routes"]:
                part = parts[route]
                self.assertLess(len(part["html"].encode("utf-8")), 800_000)
                parser = catalog.papal.DocumentParser()
                parser.feed(part["html"])
                selected = [node for node in catalog.papal.walk(parser.root) if node.attrs.get("data-volume-period")]
                self.assertEqual(len(selected), 1)
                node = selected[0]
                keys.append(node.attrs["data-volume-period"])
                text.append(" ".join(catalog.papal._visible(node).split()))
            self.assertEqual(len(set(keys)), 12)
            self.assertEqual(digest(" ".join(text).encode("utf-8")), expected_sha)
        for route, page in pages.items():
            self.assertTrue(route.endswith(".html"))
            self.assertIn("<h1>", page["html"])
            self.assertTrue(page["title"])
            if route.startswith("reading-plans/"):
                self.assertLess(len(page["html"].encode("utf-8")), 800_000)
            self.assertTrue(all((ROOT / path).is_file() for path in page["source_paths"]))


if __name__ == "__main__":
    unittest.main()
