"""Papal source acquisition keeps identity, rights and exact bytes separate."""
from __future__ import annotations

import copy
import json
from pathlib import Path
import sys
import tempfile
import tomllib
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))
import _papal_sources as sources


def document():
    return {"id": "papal.leo-xiii.sample-18910515", "title": "A source test", "pope": "Leo XIII", "pope_id": "leo-xiii", "date": "1891-05-15", "document_type": "encyclical", "languages": {"la": "https://www.vatican.va/content/leo-xiii/la/sample.html"}, "source_index_urls": ["https://www.vatican.va/content/leo-xiii/en/encyclicals.index.html"]}


class SourceTests(unittest.TestCase):
    def setUp(self):
        scratch = ROOT / ".scratch/source_records/tests"
        scratch.mkdir(parents=True, exist_ok=True)
        self.tmp = tempfile.TemporaryDirectory(dir=scratch)
        self.root = Path(self.tmp.name)
        self.doc = document()
        self.index = {"works": {}, "urls": {}}

    def tearDown(self):
        self.tmp.cleanup()

    def test_old_date_is_only_a_candidate_filter(self):
        self.assertIsNone(sources.candidate_reason(self.doc))
        with self.assertRaisesRegex(ValueError, "does not pin"):
            sources.validate_approval(self.doc, {}, "a" * 64, "b" * 64)
        self.doc["date"] = None
        self.assertEqual(sources.candidate_reason(self.doc), "unresolved-act-date")
        sources.validate_approval(self.doc, self.approval("a" * 64, "b" * 64), "a" * 64, "b" * 64)
        self.doc["date"] = "1935-01-01"
        self.assertEqual(sources.candidate_reason(self.doc), "later-act-date")
        sources.validate_approval(self.doc, self.approval("a" * 64, "b" * 64), "a" * 64, "b" * 64)

    def test_registration_retains_no_body_or_acquisition_claim(self):
        links = sources.register_document(self.root, self.doc, self.index, "2026-10-26")
        art = tomllib.loads((self.root / links["editions"]["la"]["artifact_path"]).read_text())
        self.assertEqual(art["storage"], "restricted")
        self.assertNotIn("path", art)
        self.assertNotIn("sha256", art)
        self.assertEqual(len(list((self.root / "src/sources").rglob("*.txt"))), 0)

    def test_existing_delivery_reuses_work(self):
        work_dir = self.root / "src/sources/works/leo-xiii/existing-work"
        sources.write_record(work_dir / "work.toml", {"id": "work.leo-xiii.existing", "title": "Historical title"})
        self.index["works"]["work.leo-xiii.existing"] = {"path": work_dir / "work.toml"}
        self.index["urls"][self.doc["languages"]["la"]] = {"work.leo-xiii.existing"}
        links = sources.register_document(self.root, self.doc, self.index, "2026-10-26")
        self.assertEqual(links["work_id"], "work.leo-xiii.existing")
        self.assertTrue(links["reused_work"])
        self.assertEqual(tomllib.loads((work_dir / "work.toml").read_text())["title"], "Historical title")

    def test_ambiguous_delivery_does_not_merge(self):
        self.index["urls"][self.doc["languages"]["la"]] = {"work.first", "work.second"}
        with self.assertRaisesRegex(ValueError, "multiple existing works"):
            sources.work_owner(self.root, self.doc, self.index)

    def test_transformations_are_exact_and_explicit(self):
        extracted = {"blocks": [{"kind": "paragraph", "text": "TITLE*"}, {"kind": "paragraph", "text": "Original words 1."}, {"kind": "paragraph", "text": "*Modern citation."}]}
        approved = {"strip_asterisk_after": ["TITLE"], "omit_exact_blocks": ["*Modern citation."]}
        self.assertEqual(sources.normalized_candidate(extracted, approved), "TITLE\n\nOriginal words 1.\n")
        with self.assertRaisesRegex(ValueError, "exactly one"):
            sources.normalized_candidate(extracted, {"omit_exact_blocks": ["unmatched"]})
        with self.assertRaisesRegex(ValueError, "exactly once"):
            sources.normalized_candidate(extracted, {"strip_asterisk_after": ["unmatched"]})

    def test_approval_pins_wording_and_publication(self):
        approval = self.approval("a" * 64, "b" * 64)
        sources.validate_approval(self.doc, approval, "a" * 64, "b" * 64)
        with self.assertRaisesRegex(ValueError, "does not pin"):
            sources.validate_approval(self.doc, approval, "a" * 64, "c" * 64)
        approval["publication_year"] = 1931
        with self.assertRaisesRegex(ValueError, "no later than 1930"):
            sources.validate_approval(self.doc, approval, "a" * 64, "b" * 64)

    def test_suffix_exclusion_keeps_preceding_signature(self):
        extracted = {"blocks": [{"kind": "paragraph", "text": "PONTIFEX. *Modern bibliography."}]}
        self.assertEqual(sources.normalized_candidate(extracted, {"omit_exact_suffixes": ["*Modern bibliography."]}), "PONTIFEX.\n")
        with self.assertRaisesRegex(ValueError, "one block end"):
            sources.normalized_candidate(extracted, {"omit_exact_suffixes": ["PONTIFEX."]})

    def test_reviewed_exact_join_repairs_only_the_identified_boundary(self):
        blocks = [{"kind": "paragraph", "text": "quae a C"}, {"kind": "paragraph", "text": "hristo constituta sit"}]
        approval = {"join_exact_blocks": [{"left": "quae a C", "right": "hristo constituta sit", "separator": ""}]}
        self.assertEqual(sources.normalized_candidate({"blocks": blocks}, approval), "quae a Christo constituta sit\n")
        with self.assertRaisesRegex(ValueError, "unique adjacent blocks"):
            sources.normalized_candidate({"blocks": [blocks[0], {"kind": "paragraph", "text": "another paragraph"}, blocks[1]]}, approval)
        with self.assertRaisesRegex(ValueError, "unique adjacent blocks"):
            sources.normalized_candidate({"blocks": blocks + [blocks[0]]}, approval)

    def test_retained_constituent_range_requires_exact_boundaries(self):
        source = {"blocks": [{"kind": "paragraph", "text": t} for t in ["Latin beginning", "Latin ending", "Italian translation"]]}
        selector = {"start": 0, "end": 2, "first": "Latin beginning", "last": "Latin ending"}
        self.assertEqual(sources.normalized_candidate(source, {"retain_exact_block_range": selector}), "Latin beginning\n\nLatin ending\n")
        for bad in ({**selector, "end": 4}, {**selector, "start": True}, {**selector, "last": "wrong boundary"}):
            with self.assertRaises(ValueError):
                sources.normalized_candidate(source, {"retain_exact_block_range": bad})

    def test_disjoint_ranges_preserve_title_and_body_without_navigation(self):
        source = {"blocks": [{"kind": "paragraph", "text": t} for t in ["Historical title", "Modern navigation", "Latin beginning", "Latin ending", "Italian translation"]]}
        ranges = [{"start": 0, "end": 1, "first": "Historical title", "last": "Historical title"}, {"start": 2, "end": 4, "first": "Latin beginning", "last": "Latin ending"}]
        self.assertEqual(sources.normalized_candidate(source, {"retain_exact_block_ranges": ranges}), "Historical title\n\nLatin beginning\n\nLatin ending\n")
        with self.assertRaisesRegex(ValueError, "ordered and nonoverlapping"):
            sources.normalized_candidate(source, {"retain_exact_block_ranges": ranges[::-1]})

    def test_reviewed_correction_requires_witness_and_unique_whole_block(self):
        correction = {"before": "PIUS PP. XI", "after": "PIVS PP. X.", "publication_citation": "Synthetic project-owned source, page 1", "source_witness_sha256": "a" * 64, "locus": "signature"}
        source = {"blocks": [{"kind": "paragraph", "text": "PIUS PP. XI"}]}
        self.assertEqual(sources.normalized_candidate(source, {"replace_exact_blocks": [correction]}), "PIVS PP. X.\n")
        with self.assertRaisesRegex(ValueError, "one unique whole source block"):
            sources.normalized_candidate({"blocks": source["blocks"] * 2}, {"replace_exact_blocks": [correction]})
        incomplete = {k: v for k, v in correction.items() if k != "source_witness_sha256"}
        with self.assertRaisesRegex(ValueError, "missing source_witness_sha256"):
            sources.normalized_candidate(source, {"replace_exact_blocks": [incomplete]})

    def test_latin_translation_requires_identified_historical_expression(self):
        approval = self.approval("a" * 64, "b" * 64)
        approval["original_language"] = False
        with self.assertRaisesRegex(ValueError, "historical expression kind"):
            sources.validate_approval(self.doc, approval, "a" * 64, "b" * 64)
        approval["expression_kind"] = "historical-latin-translation"
        with self.assertRaisesRegex(ValueError, "expression_note"):
            sources.validate_approval(self.doc, approval, "a" * 64, "b" * 64)
        approval["expression_note"] = "Identified human Latin translation in " + approval["publication_citation"] + "."
        sources.validate_approval(self.doc, approval, "a" * 64, "b" * 64)
        prefix, note = sources.expression_provenance(approval)
        self.assertEqual(prefix, "Historical Latin translation publication: ")
        self.assertIn("Identified human Latin translation", note)
        approval["original_language"] = True
        with self.assertRaisesRegex(ValueError, "cannot identify a translation"):
            sources.validate_approval(self.doc, approval, "a" * 64, "b" * 64)

    def approval(self, raw_hash, text_hash):
        return {"source_sha256": raw_hash, "text_sha256": text_hash, "language": "la", "original_language": True, "publication_year": 1891, "publication_citation": "Synthetic project-owned fixture, 1891 label", "rights_status": "public-domain", "rights_jurisdiction": "United States", "rights_basis": "Synthetic project-owned text used only to test a rights decision", "apparatus_review": "No excluded apparatus in fixture.", "reviewed_on": "2026-10-26"}

    def test_stage_does_not_retain_unapproved_wording(self):
        links = sources.register_document(self.root, self.doc, self.index, "2026-10-26")
        raw = b"project-owned synthetic raw HTML fixture"
        text = "Project-owned fixture paragraph preserved without alteration. " * 3
        extracted = {"text": text + "\n", "blocks": [{"kind": "paragraph", "text": text}], "extractor": "synthetic-fixture"}
        class Fetch:
            def fetch(self, url):
                return raw, {"source_url": url, "sha256": sources.sha(raw), "byte_size": len(raw), "retrieved": "2026-10-26"}
        stage = self.root / ".scratch/source_records/candidates"
        with patch.object(sources, "extract_candidate", return_value=extracted):
            row = sources.acquire_one(self.root, self.doc, links, Fetch(), stage, None)
            self.assertEqual(row["status"], "staged")
            self.assertFalse(list((self.root / "src/sources").rglob("*.txt")))
            approval = self.approval(sources.sha(raw), sources.sha((text + "\n").encode()))
            approval.update({"original_language": False, "expression_kind": "historical-latin-translation", "expression_note": "Identified historical Latin translation in the synthetic publication fixture."})
            row = sources.acquire_one(self.root, self.doc, links, Fetch(), stage, approval)
        self.assertEqual(row["status"], "retained")
        payload = self.root / row["text_path"]
        self.assertEqual(payload.read_text(), text + "\n")
        record = tomllib.loads((payload.parent / "artifact.toml").read_text())
        self.assertEqual(record["path"], row["text_path"])
        self.assertEqual(record["sha256"], sources.sha(payload.read_bytes()))
        self.assertEqual(record["derived_from"], links["editions"]["la"]["artifact_id"])
        self.assertTrue(record["provenance"].startswith("Historical Latin translation publication:"))
        self.assertNotIn("Original Latin publication:", record["provenance"])
        self.assertIn("Historical Latin translation:", row["source_note"])

    def test_rights_withdrawal_preserves_exact_research_bytes_and_excludes_manifest(self):
        links = sources.register_document(self.root, self.doc, self.index, "2026-10-26")
        raw = b"project-owned synthetic raw fixture"
        text = "Project-owned test wording.\n"
        class Fetch:
            def fetch(self, url):
                return raw, {"source_url": url, "sha256": sources.sha(raw), "byte_size": len(raw), "retrieved": "2026-10-26"}
        stage = self.root / ".scratch/source_records"
        approval = self.approval(sources.sha(raw), sources.sha(text.encode()))
        with patch.object(sources, "extract_candidate", return_value={"blocks": [{"kind": "paragraph", "text": text.strip()}]}):
            retained = sources.acquire_one(self.root, self.doc, links, Fetch(), stage / "candidates", approval)
        decision = approval | {"withdrawal_reason": "The fixture's prior publication-date inference is withdrawn.", "withdrawal_evidence": "Project-owned test evidence"}
        with self.assertRaisesRegex(ValueError, "does not pin"):
            sources.withdraw_retained(self.root, retained, decision | {"text_sha256": "f" * 64}, stage)
        payload = self.root / retained["text_path"]
        self.assertTrue(payload.exists())
        withdrawn = sources.withdraw_retained(self.root, retained, decision, stage)
        self.assertEqual(withdrawn["status"], "withdrawn")
        self.assertFalse(payload.exists())
        self.assertEqual((self.root / withdrawn["research_text_path"]).read_bytes(), text.encode())
        record = tomllib.loads((payload.parent / "artifact.toml").read_text())
        self.assertEqual(record["sha256"], sources.sha(text.encode()))
        self.assertEqual(record["storage"], "restricted")
        self.assertEqual(record["rights_status"], "restricted")
        self.assertFalse(record["indexable"])
        self.assertNotIn("path", record)
        self.assertEqual(sources.manifest({"documents": [self.doc]}, [withdrawn], "2026-10-26T00:00:00Z")["documents"], [])
        self.assertEqual(sources.withdraw_retained(self.root, withdrawn, decision, stage), withdrawn)

    def test_fragment_extent_survives_acquisition_and_manifest_replay(self):
        links = sources.register_document(self.root, self.doc, self.index, "2026-10-26")
        raw = b"project-owned synthetic raw fixture"
        text = "Project-owned fragment fixture with the supplied closing.\n"
        approval = self.approval(sources.sha(raw), sources.sha(text.encode()))
        approval["extent_kind"] = "fragment"
        with self.assertRaisesRegex(ValueError, "missing_content"):
            sources.validate_approval(self.doc, approval, sources.sha(raw), sources.sha(text.encode()))
        approval["missing_content"] = "The source replaces its announced annex with an ellipsis."
        class Fetch:
            def fetch(self, url):
                return raw, {"source_url": url, "sha256": sources.sha(raw), "retrieved": "2026-10-26"}
        with patch.object(sources, "extract_candidate", return_value={"blocks": [{"kind": "paragraph", "text": text.strip()}]}):
            receipt = sources.acquire_one(self.root, self.doc, links, Fetch(), self.root / ".scratch/source_records/candidates", approval)
        self.assertEqual("fragment", receipt["extent_kind"])
        self.assertIn(approval["missing_content"], receipt["source_note"])
        artifact = tomllib.loads((self.root / receipt["text_path"]).with_name("artifact.toml").read_text())
        self.assertIn(approval["missing_content"], artifact["notes"])
        row = sources.manifest({"documents": [self.doc]}, [receipt], "2026-10-26T00:00:00Z")["documents"][0]
        self.assertEqual("fragment", row["extent_kind"])
        self.assertEqual(approval["missing_content"], row["missing_content"])
        self.assertEqual(self.doc["title"] + " — Fragment", row["title"])
        self.doc["title"] = row["title"]
        replay = sources.manifest({"documents": [self.doc]}, [receipt], "2026-10-26T00:00:00Z")["documents"][0]
        self.assertEqual(row["title"], replay["title"])
        with self.assertRaisesRegex(ValueError, "extent_kind"):
            sources.manifest({"documents": [self.doc]}, [receipt | {"extent_kind": "unverified-whole"}], "2026-10-26T00:00:00Z")

    def test_unlinked_catalog_work_has_no_invented_edition(self):
        self.doc["languages"] = {}
        links = sources.register_document(self.root, self.doc, self.index, "2026-10-26")
        self.assertEqual(links["editions"], {})

    def test_composite_is_not_registered_as_a_fictional_single_act(self):
        self.doc["record_role"] = "composite"
        links = sources.register_document(self.root, self.doc, self.index, "2026-10-26")
        self.assertNotIn("work_id", links)
        self.assertEqual(links["status"], "not-registered-as-whole-work")
        self.assertFalse(list(self.root.rglob("work.toml")))

    def test_resolved_mislink_registers_actual_body_title(self):
        self.doc.update({"record_role": "index-mislink", "resolved_title": "Actual body title", "resolved_date": "1891-05-14", "date_resolution": {"source_url": "https://www.vatican.va/archive/printed.pdf", "locus": "p. 1"}, "title_resolution": {"basis": "Primary printed body"}, "index_title_raw": "Wrong index heading"})
        links = sources.register_document(self.root, self.doc, self.index, "2026-10-26")
        self.assertEqual(links["status"], "resolved-body-identity")
        work = tomllib.loads((self.root / links["work_path"]).read_text())
        self.assertEqual(work["title"], "Actual body title")
        self.assertEqual(links["index_title_raw"], "Wrong index heading")
        edition = tomllib.loads((self.root / links["editions"]["la"]["edition_path"]).read_text())
        self.assertEqual(edition["title"], "Actual body title — Holy See la web delivery")
        self.assertIn("Original index label: Wrong index heading", edition["notes"])

    def test_related_curial_unit_keeps_its_responsible_and_papal_context(self):
        responsible = "Cardinal Merry del Val, Secretary of State, by special mandate of Pius X"
        self.doc.update({"record_role": "constituent", "pope": "Pius X", "source_responsible": responsible, "display_responsible": responsible, "source_work_type": "curial-regulation", "source_unit_identity": {"kind": "related-regulation", "source_url": "https://www.vatican.va/archive/printed.pdf", "source_sha256": "a" * 64, "reviewed_on": "2026-10-26", "locus": "pp. 1-2", "basis": "Identified regulatory work in the historical printing."}})
        links = sources.register_document(self.root, self.doc, self.index, "2026-10-26")
        self.assertEqual(links["status"], "related-regulation-identity")
        work = tomllib.loads((self.root / links["work_path"]).read_text())
        self.assertEqual(work["responsible"], responsible)
        self.assertEqual(work["work_type"], "curial-regulation")
        receipt = {"id": self.doc["id"], "status": "retained", "language": "la", "source_url": self.doc["languages"]["la"], "text_path": "src/sources/example.txt", "artifact_id": "artifact.example", "rights_status": "public-domain", "rights_basis": "Synthetic fixture", "text_sha256": "a" * 64}
        row = sources.manifest({"documents": [self.doc]}, [receipt], "2026-10-26T00:00:00Z")["documents"][0]
        self.assertEqual(row["pope"], responsible)
        self.assertEqual(row["pope_context"], "Pius X")
        self.assertEqual(row["document_type"], "curial-regulation")

    def test_qualifications_preserve_extent_notes_and_reviewed_date(self):
        self.doc.update({"date": None, "date_conflicts": [{"date": "1891-05-15"}], "resolved_date": "1891-05-14", "date_resolution": {"source_url": "https://www.vatican.va/archive/printed.pdf", "locus": "p. 1"}})
        self.assertIsNone(sources.candidate_reason(self.doc))
        note = sources.source_qualifications(self.doc, {"source_notes": "The annex is abbreviated.", "extent": "The original act alone is complete.", "textual_limitations": "Normalized web transcription."})
        self.assertIn("annex is abbreviated", note)
        self.assertIn("original act alone is complete", note)
        self.assertIn("1891-05-14", note)

    def test_qualifications_cite_the_print_and_do_not_deny_declared_corrections(self):
        approval = self.approval("a" * 64, "b" * 64)
        approval["textual_limitations"] = "Normalized Vatican web transcription; spelling, punctuation, erroneous words, and reference numbering retained except declared modern apparatus. Not a facsimile, corrected text, or diplomatic edition. A material annex is absent."
        approval["replace_exact_blocks"] = [{"before": "PIUS PP. XI", "after": "PIVS PP. X.", "publication_citation": "Historical source", "source_witness_sha256": "a" * 64, "locus": "signature"}]
        note = sources.source_qualifications(self.doc, approval)
        self.assertIn("Historical witness: " + approval["publication_citation"], note)
        self.assertIn("A material annex is absent.", note)
        self.assertIn("PIVS PP. X.", note)
        self.assertNotIn("Not a facsimile, corrected text", note)

    def test_reviewed_work_alias_merge_preserves_exact_artifact_identity(self):
        prior_doc = copy.deepcopy(self.doc)
        prior_doc["id"] += "-alias"
        prior_doc["languages"]["la"] = "https://www.vatican.va/content/leo-xiii/la/alias.html"
        prior = sources.register_document(self.root, prior_doc, self.index, "2026-10-26")
        canonical = sources.register_document(self.root, self.doc, self.index, "2026-10-26")
        old_artifact_path = self.root / prior["editions"]["la"]["artifact_path"]
        artifact = tomllib.loads(old_artifact_path.read_text())
        artifact.update({"sha256": "a" * 64, "byte_size": 50, "retrieved": "2026-10-26"})
        sources.write_record(old_artifact_path, artifact)
        self.doc.update({"url_aliases": [self.doc["languages"]["la"], prior_doc["languages"]["la"]], "identity_aliases": [prior_doc["id"]], "reviewed_aliases": [{"canonical_id": self.doc["id"], "evidence": "Exact source comparison"}]})
        changes = sources.reconcile_catalog_owners(self.root, [self.doc], self.root / ".scratch/source_records")
        self.assertEqual(changes[0]["action"], "merged-reviewed-alias")
        index = sources.canonical_work_index(self.root)
        self.assertNotIn(prior["work_id"], index["works"])
        self.assertEqual(index["urls"][prior_doc["languages"]["la"]], {canonical["work_id"]})
        moved = next(p for p in (self.root / canonical["work_path"]).parent.rglob("artifact.toml") if tomllib.loads(p.read_text())["id"] == artifact["id"])
        self.assertEqual(tomllib.loads(moved.read_text())["sha256"], "a" * 64)

    def test_compound_delivery_has_one_container_owner_and_cannot_be_recreated_under_constituent(self):
        child = sources.register_document(self.root, self.doc, self.index, "2026-10-26")
        child_artifact_path = self.root / child["editions"]["la"]["artifact_path"]
        old = tomllib.loads(child_artifact_path.read_text())
        old.update({"sha256": "a" * 64, "byte_size": 50, "retrieved": "2026-10-26"})
        sources.write_record(child_artifact_path, old)
        container = self.root / "src/sources/works/papal-collections/compound"
        sources.write_record(container / "work.toml", {"schema": 1, "record_type": "work", "id": "work.collection", "title": "Compound delivery", "responsible": "Historical publisher", "work_type": "collection"})
        edition = container / "editions/2026-10-26-web"
        sources.write_record(edition / "edition.toml", {"schema": 1, "record_type": "edition", "id": "edition.collection", "work_id": "work.collection", "title": "Compound delivery", "language": "la", "publication": "Synthetic fixture"})
        art = {**old, "id": "artifact.collection.html", "edition_id": "edition.collection"}
        sources.write_record(edition / "artifacts/html/artifact.toml", art)
        self.doc.update({"record_role": "composite", "source_work_id": child["work_id"], "delivery_ownership": {"la": {"container_work_id": "work.collection", "artifact_id": "artifact.collection.html", "source_url": self.doc["languages"]["la"], "source_sha256": "a" * 64, "reason": "Exact compound response belongs to the collected delivery."}}})
        sources.reconcile_catalog_owners(self.root, [self.doc], self.root / ".scratch/source_records")
        links = sources.register_document(self.root, self.doc, sources.canonical_work_index(self.root), "2026-10-26")
        self.assertEqual(links["work_id"], child["work_id"])
        self.assertEqual(links["status"], "identified-constituent-in-composite")
        self.assertTrue((self.root / links["work_path"]).exists())
        self.assertEqual(links["editions"]["la"]["status"], "container-owned-delivery")
        self.assertFalse(child_artifact_path.exists())
        class NoFetch:
            def fetch(self, url):
                raise AssertionError("a compound response must not be re-promoted under its constituent")
        receipt = sources.acquire_one(self.root, self.doc, links, NoFetch(), self.root / ".scratch/source_records/candidates", None)
        self.assertEqual(receipt["status"], "segmented")

    def test_cache_and_network_url_guards(self):
        with self.assertRaisesRegex(ValueError, "repository .scratch"):
            sources.scratch_path(self.root, self.root / "build/cache")
        with self.assertRaisesRegex(ValueError, "public Vatican"):
            sources.canonical_url("http://127.0.0.1/private")
        self.assertEqual(sources.canonical_url("http://vatican.va/content/page.html#note"), "https://www.vatican.va/content/page.html")

    def test_subset_acquisition_preserves_other_retained_witnesses(self):
        from argparse import Namespace
        catalog = self.root / "catalog.json"
        sources.write_json(catalog, {"schema": "triptych-papal-documents/v1", "documents": [self.doc]})
        stage = self.root / ".scratch/source_records"
        links = sources.register_document(self.root, self.doc, self.index, "2026-10-26")
        sources.write_json(stage / "source-links.json", {"documents": [links]})
        retained = {"id": "papal.another.retained", "status": "retained", "artifact_id": "artifact.example"}
        sources.write_json(stage / "acquisition.json", {"documents": [retained]})
        args = Namespace(root=self.root, catalog=catalog, document=[self.doc["id"]], verb="acquire", stage=stage, approvals=None, limit=None, workers=1, pace=0.4, manifest=None)
        with patch.object(sources, "acquire_one", return_value={"id": self.doc["id"], "status": "staged"}):
            result = sources.command(args)
        report = json.loads((stage / "acquisition.json").read_text())
        self.assertEqual(result["retained"], 1)
        self.assertEqual(result["staged"], 1)
        self.assertIn(retained, report["documents"])

    def test_subset_registration_preserves_canonical_mapping_and_syncs_new_stage(self):
        from argparse import Namespace
        other = copy.deepcopy(self.doc)
        other["id"] += "-second"
        other["languages"]["la"] += "?second=1"
        catalog = self.root / ".scratch/catalog.json"
        sources.write_json(catalog, {"schema": "triptych-papal-documents/v1", "retrieved_on": "2026-10-26", "documents": [self.doc, other]})
        stage = self.root / ".scratch/source_records"
        args = Namespace(root=self.root, catalog=catalog, document=[], verb="register", stage=stage)
        sources.command(args)
        canonical = self.root / "src/sources/papal-documents/source-links.json"
        before = json.loads(canonical.read_text())
        unselected = next(row for row in before["documents"] if row["id"] == other["id"])
        args.document = [self.doc["id"]]
        args.stage = self.root / ".scratch/new-stage"
        result = sources.command(args)
        after = json.loads(canonical.read_text())
        self.assertEqual(2, result["mapping_documents"])
        self.assertEqual(1, result["documents"])
        self.assertEqual({self.doc["id"], other["id"]}, {row["id"] for row in after["documents"]})
        self.assertIn(unselected, after["documents"])
        self.assertEqual(after, json.loads((args.stage / "source-links.json").read_text()))


if __name__ == "__main__":
    unittest.main()
