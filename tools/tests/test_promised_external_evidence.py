"""External historical print evidence must not invent completion or page counts."""
from __future__ import annotations

import hashlib
import importlib.machinery
import importlib.util
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[2]
LOADER = importlib.machinery.SourceFileLoader(
    "promised_external_evidence_checker", str(ROOT / "tools/check-promised-deliverables")
)
SPEC = importlib.util.spec_from_loader(LOADER.name, LOADER)
CHECKER = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = CHECKER
SPEC.loader.exec_module(CHECKER)

PDF_PATH = "pdf/gpt/history/demo.pdf"
PDF_SHA = "a" * 64


class PromisedExternalEvidenceTests(unittest.TestCase):
    def setUp(self):
        scratch = ROOT / ".scratch/source-resolver"
        scratch.mkdir(parents=True, exist_ok=True)
        self.temporary = tempfile.TemporaryDirectory(dir=scratch)
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.ledger = self.root / "candidate-ledger.toml"
        self.write("src/demo/main.tex", "Historical source owner.\n")

    def write(self, relative, text):
        path = self.root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text)
        return path

    def ledger_text(self, *, evidence=PDF_PATH, state="complete", status="pass", check="path_exists", minimum=20):
        text = (
            'schema_version = 1\n[[deliverables]]\nid = "demo"\nowner = "src/demo"\n'
            f'promise = "Preserve the historical publication."\nstate = "{state}"\n'
            '[[deliverables.requirements]]\nid = "artifact"\ncriterion = "Preserve the evidence."\n'
            f'status = "{status}"\nevidence = [{json.dumps(evidence)}]\ncheck = "{check}"\n'
        )
        if check == "pdf_min_pages":
            text += f'path = "{PDF_PATH}"\nminimum = {str(minimum).lower()}\n'
        if check == "contains":
            text += 'path = "src/demo/main.tex"\nneedle = "unmet required words"\n'
        self.ledger.write_text(text)

    def validate(self, required=()):
        with patch.object(CHECKER, "ROOT", self.root):
            return CHECKER.validate(self.ledger, set(required))

    def archive(self, *, pages=25):
        canonical_hash = hashlib.sha256(PDF_PATH.encode()).hexdigest()[:16]
        filename = f"demo-gpt-{canonical_hash}.pdf"
        snapshot = "1" * 40
        archive = {
            "schema": "triptych-print-archive/v1", "snapshot": snapshot,
            "source_manifest_url": "https://mystago.gy/PUBLICATION-MANIFEST.json",
            "source_manifest_sha256": "b" * 64,
            "publications": [{
                "id": "gpt/history/demo", "legacy_pdf": PDF_PATH, "filename": filename,
                "sha256": PDF_SHA, "bytes": 12345,
                "url": f"https://github.com/spincyc/triptych-artifacts/releases/download/prints-{snapshot[:7]}/{filename}",
            }],
        }
        self.write("release/print-archive.json", json.dumps(archive))
        self.page_receipt(pages)
        return archive

    def page_receipt(self, pages):
        receipt = {
            "schema": "triptych-print-archive-pages/v1",
            "archive_manifest_sha256": hashlib.sha256((self.root / CHECKER.PRINT_ARCHIVE).read_bytes()).hexdigest(),
            "method": CHECKER.PRINT_PAGE_METHOD,
            "publications": [{
                "id": "gpt/history/demo", "legacy_pdf": PDF_PATH, "pdf_sha256": PDF_SHA, "pages": pages,
            }],
        }
        self.write("release/print-archive-pages.json", json.dumps(receipt))
        return receipt

    def delivery(self):
        archive_sha = "c" * 64
        index = {
            "schema": CHECKER._artifact_store.SCHEMA,
            "archives": [{
                "id": archive_sha, "name": "historic.tar", "sha256": archive_sha,
                "bytes": 20000, "urls": ["https://example.org/historic.tar"],
            }],
            "artifacts": [{
                "path": PDF_PATH, "member": PDF_PATH, "sha256": PDF_SHA, "bytes": 12345,
                "media_type": "application/pdf", "kind": "historical-publication", "archive": archive_sha,
            }],
        }
        self.write(CHECKER._artifact_store.INDEX_PATH, json.dumps(index))
        return index

    def test_absent_archived_pdf_is_evidence_without_network_or_pdf_reads(self):
        self.archive()
        self.ledger_text(check="pdf_min_pages")
        original_open = Path.open

        def metadata_only(path, *args, **kwargs):
            self.assertNotEqual(".pdf", path.suffix.lower())
            return original_open(path, *args, **kwargs)

        with patch.object(Path, "open", metadata_only), \
                patch.object(CHECKER._artifact_store, "resolve", side_effect=AssertionError("no hydration")), \
                patch.object(CHECKER._artifact_store, "urlopen", side_effect=AssertionError("no network")):
            self.assertEqual([], self.validate())

    def test_absent_delivery_pdf_is_evidence_but_not_an_unmeasured_page_count(self):
        self.delivery()
        self.ledger_text()
        self.assertEqual([], self.validate())
        self.ledger_text(check="pdf_min_pages")
        self.assertIn("page-count receipt", "\n".join(self.validate()))

    def test_missing_undeclared_pdf_and_other_missing_evidence_fail(self):
        self.ledger_text()
        self.assertIn("missing evidence", "\n".join(self.validate()))
        self.archive()
        self.ledger_text(evidence="missing-proof.md")
        self.assertIn("missing evidence missing-proof.md", "\n".join(self.validate()))

    def test_archival_evidence_cannot_complete_open_or_candidate_work(self):
        self.archive()
        self.ledger_text(status="open")
        self.assertIn("complete state has unmet requirements", "\n".join(self.validate()))
        self.ledger_text(state="candidate")
        self.assertIn("completion required", "\n".join(self.validate(required=["demo"])))
        self.ledger_text(check="contains")
        self.assertIn("required literal is absent", "\n".join(self.validate()))

    def test_exact_historical_page_count_must_satisfy_the_minimum(self):
        self.archive(pages=19)
        self.ledger_text(check="pdf_min_pages", minimum=20)
        self.assertIn("does not meet minimum page count", "\n".join(self.validate()))
        self.ledger_text(check="pdf_min_pages", minimum=True)
        self.assertIn("does not meet minimum page count", "\n".join(self.validate()))

    def test_contains_never_opens_pdf_bytes_or_claims_the_literal_was_verified(self):
        self.archive()
        self.ledger_text(check="contains")
        self.ledger.write_text(self.ledger.read_text().replace(
            'path = "src/demo/main.tex"', f'path = "{PDF_PATH}"'
        ))
        original_open = Path.open

        def metadata_only(path, *args, **kwargs):
            self.assertNotEqual(".pdf", path.suffix.lower())
            return original_open(path, *args, **kwargs)

        with patch.object(Path, "open", metadata_only):
            self.assertIn("requires retained text evidence", "\n".join(self.validate()))

    def test_page_receipt_rejects_changed_archive_pdf_and_invalid_count(self):
        self.archive()
        self.ledger_text(check="pdf_min_pages")
        for field, value in (("pdf_sha256", "0" * 64), ("legacy_pdf", "pdf/gpt/other.pdf"), ("pages", True)):
            with self.subTest(field=field):
                receipt = self.page_receipt(25)
                receipt["publications"][0][field] = value
                self.write(str(CHECKER.PRINT_PAGES), json.dumps(receipt))
                self.assertIn("external PDF evidence", "\n".join(self.validate()))
        receipt = self.page_receipt(25)
        receipt["archive_manifest_sha256"] = "0" * 64
        self.write(str(CHECKER.PRINT_PAGES), json.dumps(receipt))
        self.assertIn("archive identity", "\n".join(self.validate()))

    def test_print_archive_rejects_unknown_fields_routes_ids_hashes_sizes_and_urls(self):
        self.ledger_text()
        for field, value in (("id", "gpt/../escape"), ("legacy_pdf", "pdf/gpt/other.pdf"),
                             ("sha256", "bad"), ("bytes", True), ("url", "http://example.org/demo.pdf")):
            with self.subTest(field=field):
                archive = self.archive()
                archive["publications"][0][field] = value
                self.write(str(CHECKER.PRINT_ARCHIVE), json.dumps(archive))
                self.assertIn("external PDF evidence", "\n".join(self.validate()))
        archive = self.archive()
        archive["unexpected"] = True
        self.write(str(CHECKER.PRINT_ARCHIVE), json.dumps(archive))
        self.assertIn("invalid print archive", "\n".join(self.validate()))

    def test_delivery_index_must_be_strict_and_agree_with_print_archive(self):
        self.archive()
        self.ledger_text()
        index = self.delivery()
        index["artifacts"][0]["sha256"] = "0" * 64
        self.write(CHECKER._artifact_store.INDEX_PATH, json.dumps(index))
        self.assertIn("disagree", "\n".join(self.validate()))
        index = self.delivery()
        index["unexpected"] = True
        self.write(CHECKER._artifact_store.INDEX_PATH, json.dumps(index))
        self.assertIn("external PDF evidence", "\n".join(self.validate()))


if __name__ == "__main__":
    unittest.main()
