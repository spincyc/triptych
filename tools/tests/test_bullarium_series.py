"""Historical series keep physical sources, languages and review gates distinct."""
from __future__ import annotations

import copy
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import tomllib
import unittest
import xml.etree.ElementTree as ET
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))
import _bullarium_series as s


class HistoricalSeriesTests(unittest.TestCase):
    def setUp(self):
        scratch = ROOT / ".scratch/historical_series/tests"
        scratch.mkdir(parents=True, exist_ok=True)
        self.temp = tempfile.TemporaryDirectory(dir=scratch)
        self.root = Path(self.temp.name)
        (self.root / "src/gpt").mkdir(parents=True)
        self.cache = self.root / ".scratch/cache"
        self.when = "2026-10-26T05:00:00Z"
        self.text = ("TITLE PAGE\nI.\nPRIMUS TITULUS\nPius Papa VI\nVerba prima integra. Ex audientia SSmi. Sanctissimus benigne annuit pro gratia. Die 13 Iunii 1781.\nP. H. Massei, armorum praeses.\n"
                     "II.\nSECONDO TITOLO\nPius Papa VI\nParole italiane complete.\nFirmato.\nINDEX\n").encode()
        self.raw = s.legacy.lines(self.text)
        xml = '<DjVuXML><BODY><OBJECT usemap="book_0007.djvu" width="2000" height="3000">'
        for line in self.raw:
            xml += '<LINE>' + ''.join('<WORD coords="200,800,800,780">' + token + '</WORD>' for token in line.split()) + '</LINE>'
        xml = (xml + '</OBJECT></BODY></DjVuXML>').encode()
        payloads = {"ocr": self.text, "xml": xml, "labels": b'{"pages":[{"leafNum":7,"pageNumber":"1"}]}',
                    "imprint": b"Synthetic project-owned imprint evidence fixture"}
        inputs = {}
        for kind, payload in payloads.items():
            inputs[kind] = {"source_url": "https://example.org/" + kind, "filename": kind + ".txt",
                "sha256": s.sha(payload), "sha1": hashlib.sha1(payload).hexdigest(), "byte_size": len(payload),
                "retrieved_on": "2026-10-26", "media_type": {"xml": "application/xml", "labels": "application/json"}.get(kind, "text/plain")}
        self.config = {"schema": s.CONFIG_SCHEMA, "series_id": "bullarium-continuatio", "title": "Synthetic historical series",
            "revision": self.when, "volumes": [{"key": "volume-01", "title": "Synthetic volume I",
                "responsible": "Synthetic fixture editors", "publication": "Project-owned test fixture, synthetic1900label",
                "printing_basis": "Synthetic project-owned evidence; no external source claim.",
                "rights_basis": "Project-owned synthetic test source.", "publication_year": 1900,
                "place_slug": "rome", "language": "mul", "languages": ["la", "it"], "inputs": inputs,
                "body_line_ranges": [[2, 11]], "boundary_evidence": {"basis": "Synthetic fixture boundaries",
                    "contexts": [{"physical_lines": [1, 3], "text": "\n".join(self.raw[:3])},
                                 {"physical_lines": [10, 12], "text": "\n".join(self.raw[9:12])}]},
                "heading_patterns": [r"(?P<number>[IVXLCDM]+)\."] ,
                "protocol_patterns": [r"Pius Papa VI"], "heading_overrides": []}]}
        for kind, payload in payloads.items():
            s.legacy.write(s._input_path(self.root, self.cache, self.config["volumes"][0], kind), payload)

    def tearDown(self):
        self.temp.cleanup()

    def prepare(self):
        s.validate_config(self.config)
        s.prepare(self.root, self.config, self.cache, self.when)
        return s.read_json(self.root / s.paths_for(self.config["series_id"])["catalog"])

    def review(self, catalog, index=0, language="la"):
        unit = catalog["documents"][index]
        return {"document_id": unit["id"], "artifact_sha256": unit["artifact_sha256"],
            "decision": "admit", "title": "PRIMUS TITULUS" if index == 0 else "SECONDO TITOLO",
            "printed_attribution": "Pius Papa VI", "source_attribution_lines": [4, 4] if index == 0 else [9, 9],
            "physical_line_ranges": [[2, 6]] if index == 0 else [[7, 11]], "language": language,
            "genre": "Historical act (printed attribution)", "date": None,
            "review_note": "Complete synthetic fixture extent inspected with its neighbors.",
            "reviewed_extent": "All selected lines and surrounding context.",
            "boundary_review": "Independent heading and closing checked.",
            "reading_order_review": "Synthetic single column sequence read in full.",
            "source_extent_review": "No omitted substantive fixture text."}

    def packet(self, reviews):
        path = self.root / ".scratch/reviews.json"
        s.legacy.write(path, s.legacy.json_bytes({"schema": s.REVIEW_SCHEMA, "series_id": self.config["series_id"], "reviews": reviews}))
        return path

    def test_duplicate_json_keys_and_nonfinite_numbers_rejected(self):
        p = self.root / ".scratch/bad.json"
        for payload in ('{"a":1,"a":2}', '{"a":NaN}'):
            s.legacy.write(p, payload.encode())
            with self.assertRaises(ValueError):
                s.read_json(p)

    def test_revision_checks_calendar_and_explicit_utc(self):
        for value in ("2026-02-30T00:00:00Z", "2026-10-26", "2026-10-26T00:00:00+00:00"):
            with self.assertRaises(ValueError):
                s.revision(value)

    def test_config_requires_historical_printing_and_imprint(self):
        for field, value in (("publication_year", 1931), ("publication_year", True), ("printing_basis", "")):
            config = copy.deepcopy(self.config)
            config["volumes"][0][field] = value
            with self.assertRaises(ValueError):
                s.validate_config(config)
        config = copy.deepcopy(self.config)
        del config["volumes"][0]["inputs"]["imprint"]
        with self.assertRaisesRegex(ValueError, "imprint"):
            s.validate_config(config)

    def test_cache_paths_cannot_escape_repository_scratch(self):
        for path in (self.root / "outside", self.root / ".scratch/../../outside"):
            with self.assertRaisesRegex(ValueError, "scratch"):
                s.local(self.root, path, scratch=True)

    def test_whole_input_hashes_checked_before_import(self):
        source = self.config["volumes"][0]["inputs"]["ocr"]
        path = s._input_path(self.root, self.cache, self.config["volumes"][0], "ocr")
        path.write_bytes(self.text[:-1])
        with self.assertRaisesRegex(ValueError, "whole input"):
            s.exact_input(path, source)

    def test_cached_acquisition_does_not_fetch_and_verifies_all_bytes(self):
        with patch.object(s.urllib.request, "urlopen", side_effect=AssertionError("unexpected network")):
            result = s.acquire(self.root, self.config, self.cache)
        self.assertEqual(4, result["responses_reused"])
        self.assertEqual(0, result["responses_downloaded"])

    def test_remote_whole_pdf_imprint_is_not_an_image_or_a_full_wrapper_rights_claim(self):
        imprint = self.config["volumes"][0]["inputs"]["imprint"]
        imprint.update(media_type="application/pdf", storage="remote", rights_status="unresolved",
                       rights_basis="Historical body wording is public domain; complete provider wrapper rights are unresolved.")
        catalog = self.prepare()
        ref = catalog["volumes"][0]["container"]["artifacts"]["imprint"]
        record = tomllib.loads((self.root / ref["manifest"]).read_text())
        self.assertEqual("historical-printing-evidence-container", record["artifact_type"])
        self.assertEqual("remote", record["storage"])
        self.assertEqual("unresolved", record["rights_status"])
        self.assertNotIn("path", record)
        self.assertNotIn("verbose XML", record["notes"])
        imprint["storage"] = "tracked"
        with self.assertRaisesRegex(ValueError, "full-wrapper rights"):
            s.validate_config(self.config)

    def test_preparation_proposes_without_date_gate_or_automatic_admission(self):
        catalog = self.prepare()
        self.assertEqual(2, len(catalog["documents"]))
        self.assertTrue(all(item["date"] is None and not item["date_raw"] and item["status"] == "held" for item in catalog["documents"]))
        self.assertEqual(0, catalog["coverage"]["complete_printed_witnesses"])
        self.assertEqual([], s.read_json(self.root / s.paths_for(self.config["series_id"])["manifest"])["documents"])
        self.assertEqual("mul", catalog["volumes"][0]["language"])
        self.assertEqual([7], catalog["documents"][0]["scan_leaf_ids"])

    def test_boundary_context_must_be_literal(self):
        self.config["volumes"][0]["boundary_evidence"]["contexts"][0]["text"] = "model rewritten source"
        with self.assertRaisesRegex(ValueError, "literal source"):
            self.prepare()

    def test_formfeed_is_not_a_physical_line_boundary(self):
        text = b"title\nI.\nPius Papa VI\nprima\fsecunda\nsubscripsit\n"
        xml = self.root / ".scratch/formfeed.xml"
        xml.write_text('<DjVuXML><BODY><OBJECT usemap="x_0001.djvu" width="2000" height="3000">' +
                       ''.join('<LINE><WORD coords="200,800,800,780">' + token + '</WORD></LINE>' for token in text.decode().split()) +
                       '</OBJECT></BODY></DjVuXML>')
        mapping = s.legacy.page_map(text, xml, {"pages": []})
        volume = copy.deepcopy(self.config["volumes"][0])
        volume.update(body_line_ranges=[[2, 5]], boundary_evidence={"basis": "LF-only fixture extent",
            "contexts": [{"physical_lines": [4, 4], "text": "prima\fsecunda"}]})
        units = s.discover(text, volume, mapping, "bullarium-continuatio")
        self.assertEqual(5, mapping["physical_line_count"])
        self.assertEqual([[2, 5]], units[0]["physical_line_ranges"])
        self.assertEqual(5, mapping["pages"][0]["physical_line_end"])

    def test_heading_override_retains_unknown_number_and_preceding_own_lines(self):
        volume = self.config["volumes"][0]
        volume["heading_patterns"] = []
        volume["heading_overrides"] = [{"line": 3, "selection_start": 2, "act_number_raw": None,
                                       "reason": "Synthetic numeral unreadable; preceding own line retained."}]
        catalog = self.prepare()
        item = catalog["documents"][0]
        self.assertEqual(2, item["selection_start"])
        self.assertEqual(3, item["heading_line"])
        self.assertIsNone(item["act_number_raw"])
        self.assertIsNone(item["act_number"])
        self.assertEqual([[2, 11]], item["physical_line_ranges"])

    def test_explicit_heading_prefix_does_not_create_overlapping_discoveries(self):
        self.config["volumes"][0]["heading_overrides"] = [{"line": 3, "selection_start": 2, "act_number_raw": None,
                                                           "reason": "Include own prefix before actual first title."}]
        catalog = self.prepare()
        self.assertEqual(2, len(catalog["documents"]))
        self.assertEqual([2], catalog["documents"][0]["heading_exception"]["suppressed_prefix_heading_lines"])

    def test_whole_txt_xml_mismatch_refused(self):
        volume = self.config["volumes"][0]
        path = s._input_path(self.root, self.cache, volume, "xml")
        payload = path.read_bytes().replace(b"Verba", b"Alia")
        source = volume["inputs"]["xml"]
        source.update(sha256=s.sha(payload), sha1=hashlib.sha1(payload).hexdigest(), byte_size=len(payload))
        s.legacy.write(s._input_path(self.root, self.cache, volume, "xml"), payload)
        with self.assertRaisesRegex(ValueError, "token mismatch"):
            self.prepare()

    def test_xml_word_line_serialization_preserves_outside_line_words_and_lf_contract(self):
        xml = b'<DjVuXML><OBJECT><WORD>extra</WORD><PARAGRAPH><LINE><WORD>A\x0cB</WORD><WORD>C</WORD></LINE></PARAGRAPH><WORD>tail</WORD></OBJECT></DjVuXML>'
        # XML itself forbids FF; source controls are never repaired to parse it.
        with self.assertRaises(ET.ParseError):
            s.xml_word_line_text(xml)
        xml = xml.replace(b'A\x0cB', b'A B')
        self.assertEqual(b'extra\nA B C\n\ntail\n\n', s.xml_word_line_text(xml))

    def test_generated_xml_text_is_replayed_on_cold_cache_and_has_distinct_provenance(self):
        volume = self.config["volumes"][0]
        original = copy.deepcopy(volume["inputs"]["ocr"])
        original_path = s._input_path(self.root, self.cache, volume, "ocr")
        xml = s.exact_input(s._input_path(self.root, self.cache, volume, "xml"), volume["inputs"]["xml"])
        expected = s.xml_word_line_text(xml)
        volume["inputs"]["offered-ocr"] = original
        volume["inputs"]["ocr"] = {"source_url": volume["inputs"]["xml"]["source_url"], "filename": "xml-line-text.txt",
            "sha256": s.sha(expected), "byte_size": len(expected), "retrieved_on": "2026-10-26", "media_type": "text/plain",
            "generation": {"method": "xml-word-line-text-v1", "source_kind": "xml", "source_sha256": volume["inputs"]["xml"]["sha256"],
                "recipe_sha256": s.sha(s.xml_text_recipe())}}
        s.validate_config(self.config)
        with patch.object(s.urllib.request, "urlopen", side_effect=AssertionError("cold derived input must not fetch its XML URL as TXT")):
            acquisition = s.acquire(self.root, self.config, self.cache, {original["sha256"]: str(original_path.relative_to(self.root))})
        self.assertEqual(1, acquisition["representations_generated"])
        self.assertEqual(expected, s._input_path(self.root, self.cache, volume, "ocr").read_bytes())
        catalog = self.prepare()
        artifacts = catalog["volumes"][0]["container"]["artifacts"]
        derived = tomllib.loads((self.root / artifacts["ocr"]["manifest"]).read_text())
        self.assertEqual(artifacts["xml"]["id"], derived["derived_from"])
        self.assertNotEqual(artifacts["offered-ocr"]["id"], artifacts["ocr"]["id"])
        self.assertNotIn("Whole exact response", derived["provenance"])
        recipe = next(p for p in (self.root / "src/sources/works/triptych/historical-papal-line-mapping").rglob("rebuild-xml-line-text.py"))
        output = self.root / ".scratch/replayed-xml-text.txt"
        result = subprocess.run([sys.executable, str(recipe), "--xml", str(s._input_path(self.root, self.cache, volume, "xml")),
            "--xml-sha256", volume["inputs"]["xml"]["sha256"], "--out", str(output)], capture_output=True, text=True)
        self.assertEqual(0, result.returncode, result.stderr)
        self.assertEqual(expected, output.read_bytes())

    def test_replay_recipe_reproduces_complete_map(self):
        catalog = self.prepare()
        container = catalog["volumes"][0]["container"]
        matches = [p for p in (self.root / "src/sources/works").rglob("artifact.toml") if tomllib.loads(p.read_text())["id"] == container["line_map_recipe_id"]]
        recipe = self.root / tomllib.loads(matches[0].read_text())["path"]
        output = self.root / ".scratch/replayed.json"
        volume = self.config["volumes"][0]
        result = subprocess.run([sys.executable, str(recipe), "--ocr", str(s._input_path(self.root, self.cache, volume, "ocr")),
            "--xml", str(s._input_path(self.root, self.cache, volume, "xml")), "--labels", str(s._input_path(self.root, self.cache, volume, "labels")),
            "--recipe-id", container["line_map_recipe_id"], "--out", str(output)], capture_output=True, text=True)
        self.assertEqual(0, result.returncode, result.stderr)
        self.assertEqual((self.root / container["line_map_path"]).read_bytes(), output.read_bytes())

    def test_issuer_and_source_extent_findings_are_required(self):
        catalog = self.prepare()
        for mutate in (lambda item: item.update(printed_attribution="Leo Papa XIII"),
                       lambda item: item.update(source_extent_review="")):
            item = self.review(catalog)
            mutate(item)
            with self.assertRaises(ValueError):
                s.admit(self.root, self.config, [self.packet([item])], self.when)
        self.assertFalse(list((self.root / "src/sources/works/bullarium-continuatio").glob("volume-01-line-*/work.toml")))

    def test_independent_admitted_extents_cannot_overlap(self):
        catalog = self.prepare()
        first, second = self.review(catalog), self.review(catalog, 1, "it")
        second["physical_line_ranges"] = [[4, 11]]
        with self.assertRaisesRegex(ValueError, "overlap"):
            s.admit(self.root, self.config, [self.packet([first, second])], self.when)

    def test_distinct_constituent_languages_preserve_one_container(self):
        catalog = self.prepare()
        result = s.admit(self.root, self.config, [self.packet([self.review(catalog), self.review(catalog, 1, "it")])], self.when)
        self.assertEqual(2, result["complete_printed_witnesses"])
        manifest = s.read_json(self.root / s.paths_for(self.config["series_id"])["manifest"])
        self.assertEqual(["la", "it"], [item["language"] for item in manifest["documents"]])
        self.assertEqual(1, len({item["artifact_id"] for item in manifest["documents"]}))
        self.assertEqual(1, len(list((self.root / "src/sources/works").rglob("ocr.txt"))))
        for row in manifest["documents"]:
            segment = tomllib.loads((self.root / row["segment_path"]).read_text())
            edition = tomllib.loads((self.root / row["segment_path"]).parents[1].joinpath("edition.toml").read_text())
            self.assertEqual(row["language"], edition["language"])
            self.assertEqual(row["sha256"], segment["artifact_sha256"])
        self.assertEqual("ok", s.check(self.root, self.config)["status"])

    def test_internal_boundary_proof_is_not_reader_apparatus(self):
        catalog = self.prepare()
        item = self.review(catalog)
        item.update(review_note="Coordinator audit protocol4–6 and internal extent reconciliation.",
                    reader_source_note="A historical annex follows the signature.", language_label="Latin")
        s.admit(self.root, self.config, [self.packet([item])], self.when)
        manifest = s.read_json(self.root / s.paths_for(self.config["series_id"])["manifest"])
        source_note = manifest["documents"][0]["source_note"]
        self.assertIn("historical annex", source_note)
        self.assertNotIn("Coordinator", source_note)
        self.assertNotIn("protocol4", source_note)
        self.assertEqual("Latin", manifest["documents"][0]["language_label"])

    def test_editorial_caption_exception_has_exact_outside_body_proof_and_truthful_reader_notice(self):
        catalog = self.prepare()
        item = self.review(catalog)
        item.update(physical_line_ranges=[[4, 6]], reader_source_note="Complete papal body; editorial caption omitted.",
            editorial_omission_review={"finding": "non-substantive-publishing-furniture", "outside_papal_text": True,
                "not_substantive_historical_note": True, "basis": "Synthetic title furniture is separate from protocol, grant and subscription.",
                "omitted_loci": [{"physical_lines": [2, 3], "literal": "I.\nPRIMUS TITULUS", "basis": "Exact synthetic editorial caption."}]})
        s.admit(self.root, self.config, [self.packet([item])], self.when)
        row = s.read_json(self.root / s.paths_for(self.config["series_id"])["manifest"])["documents"][0]
        self.assertIn("Complete papal body; editorial caption", row["source_note"])
        self.assertNotIn("Historical synopsis, source notes, dating and subscriptions are retained", row["source_note"])

    def test_editorial_omission_cannot_cover_selected_body_or_unbounded_native_caption(self):
        raw = ["Editorial heading.", "Papal body."]
        item = {"reader_source_note": "Editorial heading omitted.", "editorial_omission_review": {
            "finding": "non-substantive-publishing-furniture", "outside_papal_text": True,
            "not_substantive_historical_note": True, "basis": "Synthetic review.",
            "omitted_loci": [{"physical_lines": [2, 2], "literal": raw[1], "basis": "Synthetic locus."}]}}
        with self.assertRaisesRegex(ValueError, "overlaps"):
            s._review_editorial_omission(raw, item, [[2, 2]])
        item["editorial_omission_review"]["omitted_loci"] = [{"source_url": "https://example.org/full-page.jpg",
            "sha256": "a" * 64, "byte_size": 100, "artifact_page": 1, "leaf": 0,
            "printed_caption": "Editorial heading.", "basis": "Synthetic native evidence."}]
        with self.assertRaisesRegex(ValueError, "bounded native image"):
            s._review_editorial_omission(raw, item, [[2, 2]])

    def test_fragment_requires_explicit_missing_content_and_title(self):
        catalog = self.prepare()
        item = self.review(catalog)
        item.update(decision="fragment", extent_kind="fragment")
        with self.assertRaisesRegex(ValueError, "visible title"):
            s.admit(self.root, self.config, [self.packet([item])], self.when)
        item.update(title="PRIMUS TITULUS — Fragment", missing_content="Synthetic fixture lacks its declared annex.")
        with self.assertRaisesRegex(ValueError, "protocol/incipit-only"):
            s.admit(self.root, self.config, [self.packet([item])], self.when)
        item["substantive_fragment_evidence"] = {"finding": "substantive-body-survives", "physical_line_ranges": [[5, 5]],
            "literal": "Sanctissimus benigne annuit pro gratia.",
            "basis": "The synthetic operative grant itself survives; this is more than its title, protocol or incipit."}
        s.admit(self.root, self.config, [self.packet([item])], self.when)
        full = s.read_json(self.root / s.paths_for(self.config["series_id"])["manifest"])
        fragments = s.read_json(self.root / s.paths_for(self.config["series_id"])["fragments"])
        self.assertFalse(full["documents"])
        self.assertEqual("fragment", fragments["documents"][0]["extent_kind"])

    def test_fragment_substantive_evidence_must_be_literal_inside_its_extent(self):
        raw = ["Pius Papa VI", "Verba substantialia supersunt.", "Aliud actum."]
        item = {"decision": "fragment", "extent_kind": "fragment", "title": "Fragment: synthetic act", "missing_content": "Closing absent.",
                "substantive_fragment_evidence": {"finding": "substantive-body-survives", "physical_line_ranges": [[3, 3]],
                    "literal": raw[2], "basis": "Synthetic extent proof."}}
        with self.assertRaisesRegex(ValueError, "escapes"):
            s._review_fragment(raw, item, [[1, 2]])
        item["substantive_fragment_evidence"].update(physical_line_ranges=[[2, 2]], literal="Invented words")
        with self.assertRaisesRegex(ValueError, "not literal"):
            s._review_fragment(raw, item, [[1, 2]])

    def test_normalized_date_requires_explicit_evidence(self):
        catalog = self.prepare()
        item = self.review(catalog)
        item["date"] = "1800-01-01"
        with self.assertRaisesRegex(ValueError, "date requires"):
            s.admit(self.root, self.config, [self.packet([item])], self.when)

    def test_canonical_join_cannot_rely_on_title_only(self):
        catalog = self.prepare()
        item = self.review(catalog)
        item.update(canonical_work_id="work.some.existing", identity_evidence={"existing_work_id": "work.some.existing", "basis": "Same title"})
        with self.assertRaisesRegex(ValueError, "issuer/date/incipit/body"):
            s.admit(self.root, self.config, [self.packet([item])], self.when)

    def test_existing_review_cannot_be_silently_replaced(self):
        catalog = self.prepare()
        item = self.review(catalog)
        packet = self.packet([item])
        s.admit(self.root, self.config, [packet], self.when)
        item["review_note"] = "Different unreviewed decision"
        with self.assertRaisesRegex(ValueError, "explicit supersession"):
            s.admit(self.root, self.config, [self.packet([item])], self.when)

    def test_prepare_refuses_disappearing_reviewed_base_before_registering_any_volume(self):
        catalog = self.prepare()
        item = self.review(catalog)
        s.admit(self.root, self.config, [self.packet([item])], self.when)
        before = {p: p.read_bytes() for p in (self.root / "src").rglob("*") if p.is_file()}
        original = self.config["volumes"][0]
        earlier = copy.deepcopy(original)
        earlier["key"] = "volume-00"
        for kind in earlier["inputs"]:
            payload = s._input_path(self.root, self.cache, original, kind).read_bytes()
            s.legacy.write(s._input_path(self.root, self.cache, earlier, kind), payload)
        original["body_line_ranges"] = [[7, 11]]
        self.config["volumes"].insert(0, earlier)
        with patch.object(s, "register_container", wraps=s.register_container) as register:
            with self.assertRaisesRegex(ValueError, "reviewed discovery would disappear"):
                self.prepare()
            register.assert_not_called()
        self.assertEqual(before, {p: p.read_bytes() for p in (self.root / "src").rglob("*") if p.is_file()})

    def test_prepare_refuses_reviewed_controller_rebinding_before_registration(self):
        catalog = self.prepare()
        s.admit(self.root, self.config, [self.packet([self.review(catalog)])], self.when)
        before = {p: p.read_bytes() for p in (self.root / "src").rglob("*") if p.is_file()}
        self.config["volumes"][0]["publication_year"] = 1901
        with patch.object(s, "register_container", wraps=s.register_container) as register:
            with self.assertRaisesRegex(ValueError, "reviewed discovery identity changed"):
                self.prepare()
            register.assert_not_called()
        self.assertEqual(before, {p: p.read_bytes() for p in (self.root / "src").rglob("*") if p.is_file()})

    def test_reprepare_preserves_reviewed_base_and_active_manifest_exactly(self):
        catalog = self.prepare()
        item = self.review(catalog)
        s.admit(self.root, self.config, [self.packet([item])], self.when)
        paths = s.paths_for(self.config["series_id"])
        reviewed = next(row for row in s.read_json(self.root / paths["catalog"])["documents"] if row["id"] == item["document_id"])
        manifest = (self.root / paths["manifest"]).read_bytes()
        again = self.prepare()
        self.assertEqual(reviewed, next(row for row in again["documents"] if row["id"] == reviewed["id"]))
        self.assertEqual(manifest, (self.root / paths["manifest"]).read_bytes())
        self.assertEqual("ok", s.check(self.root, self.config)["status"])

    def test_check_refuses_active_manifest_orphans_and_changed_source_selections(self):
        catalog = self.prepare()
        item = self.review(catalog)
        s.admit(self.root, self.config, [self.packet([item])], self.when)
        paths = s.paths_for(self.config["series_id"])
        catalog_path, manifest_path = (self.root / paths[key] for key in ("catalog", "manifest"))
        good_catalog = catalog_path.read_bytes()
        orphaned = s.read_json(catalog_path)
        orphaned["documents"] = [row for row in orphaned["documents"] if row["id"] != item["document_id"]]
        orphaned["coverage"] = s.coverage(orphaned)
        s.legacy.write(catalog_path, s.legacy.json_bytes(orphaned))
        with self.assertRaisesRegex(ValueError, "reader lacks one matching admitted catalog entry"):
            s.check(self.root, self.config)
        catalog_path.write_bytes(good_catalog)
        manifest = s.read_json(manifest_path)
        manifest["documents"][0]["physical_line_ranges"] = [[2, 5]]
        s.legacy.write(manifest_path, s.legacy.json_bytes(manifest))
        with self.assertRaisesRegex(ValueError, "reader disagrees with its admitted catalog source"):
            s.check(self.root, self.config)

    def test_compound_discovery_requires_separate_reviewed_constituents(self):
        self.config["volumes"][0]["heading_patterns"] = []
        catalog = self.prepare()
        first, second = self.review(catalog), self.review(catalog)
        second.update(title="SECONDO TITOLO", language="it", physical_line_ranges=[[7, 11]], source_attribution_lines=[9, 9])
        parent = {"document_id": catalog["documents"][0]["id"], "artifact_sha256": s.sha(self.text), "decision": "split",
                  "review_note": "Two independent complete acts occupy one machine proposal.", "constituents": [first, second]}
        s.admit(self.root, self.config, [self.packet([parent])], self.when)
        result = s.read_json(self.root / s.paths_for(self.config["series_id"])["catalog"])
        self.assertEqual(3, len(result["documents"]))
        self.assertEqual(2, result["coverage"]["complete_printed_witnesses"])
        self.assertEqual(1, result["coverage"]["raw_candidates"])
        self.assertEqual("split-into-constituents", result["documents"][0]["status"])
        # Re-preparing the immutable source keeps those independently reviewed children.
        self.prepare()
        result = s.read_json(self.root / s.paths_for(self.config["series_id"])["catalog"])
        self.assertEqual(3, len(result["documents"]))

    def test_one_shared_recipe_artifact_is_reused_across_containers(self):
        self.prepare()
        first = s.register_mapping_recipe(self.root, self.when)
        second = s.register_mapping_recipe(self.root, "2026-10-27T00:00:00Z")
        self.assertEqual(first, second)
        self.assertEqual(1, len(list((self.root / "src/sources/works/triptych/historical-papal-line-mapping").rglob("artifact.toml"))))

    def test_registered_vertical_passes_the_canonical_source_validator(self):
        catalog = self.prepare()
        s.admit(self.root, self.config, [self.packet([self.review(catalog), self.review(catalog, 1, "it")])], self.when)
        result = subprocess.run([str(ROOT / "tools/source-library"), "--root", str(self.root), "validate"],
                                cwd=ROOT, capture_output=True, text=True)
        self.assertEqual(0, result.returncode, result.stdout + result.stderr)

    def test_positive_container_work_reuse_keeps_established_records_unchanged(self):
        base = self.root / "src/sources/works/existing/volume"
        s.new_record(base / "work.toml", {"schema": 1, "record_type": "work", "id": "work.existing.volume",
                     "title": "Established historical volume", "responsible": "Historical editors", "work_type": "historical-document-container"})
        before = (base / "work.toml").read_bytes()
        self.config["volumes"][0]["canonical_container"] = {"work_id": "work.existing.volume",
            "identity_evidence": {"basis": "Synthetic independent volume/printing proof; artifact identity is distinct."}}
        catalog = self.prepare()
        container = catalog["volumes"][0]["container"]
        self.assertEqual("work.existing.volume", container["work_id"])
        self.assertTrue(container["edition_id"].startswith("edition.existing.volume."))
        self.assertEqual(before, (base / "work.toml").read_bytes())

    def contextual_review(self, catalog):
        item = self.review(catalog)
        item["physical_line_ranges"] = [[5, 6]]
        item["source_attribution_context"] = {"kind": "shared-running-header", "artifact_sha256": s.sha(self.text),
            "scope_line_ranges": [[2, 11]], "basis": "Synthetic common header applies to both independently closed fixture acts.",
            "page_evidence": [{"artifact_page": 1, "leaf": 7, "basis": "Synthetic page header and act scope directly checked."}],
            "protocol_and_closing_review": {"finding": "consistent", "protocol_lines": [5, 5], "closing_lines": [6, 6],
                "basis": "Both complete fixture clauses are consistent with the source header; no conflicting issuer."}}
        return item

    def test_bounded_shared_attribution_context_does_not_duplicate_header(self):
        catalog = self.prepare()
        item = self.contextual_review(catalog)
        s.admit(self.root, self.config, [self.packet([item])], self.when)
        manifest = s.read_json(self.root / s.paths_for(self.config["series_id"])["manifest"])
        self.assertEqual([[5, 6]], manifest["documents"][0]["physical_line_ranges"])
        self.assertNotIn([4, 4], manifest["documents"][0]["physical_line_ranges"])

    def test_out_of_scope_or_conflicting_context_does_not_establish_issuer(self):
        catalog = self.prepare()
        for field, value, message in (("scope_line_ranges", [[7, 11]], "scope"),
                                      ("protocol_and_closing_review", {"finding": "contradicted"}, "contradicted"),
                                      ("page_evidence", [{"artifact_page": 2, "leaf": 8, "basis": "Wrong page"}], "page/leaf")):
            item = self.contextual_review(catalog)
            item["source_attribution_context"][field] = value
            with self.assertRaisesRegex(ValueError, message):
                s.admit(self.root, self.config, [self.packet([item])], self.when)

    def test_incremental_admission_keeps_existing_render_revision(self):
        catalog = self.prepare()
        s.admit(self.root, self.config, [self.packet([self.review(catalog)])], self.when)
        later = "2026-10-26T06:00:00Z"
        s.admit(self.root, self.config, [self.packet([self.review(catalog, 1, "it")])], later)
        manifest = s.read_json(self.root / s.paths_for(self.config["series_id"])["manifest"])
        self.assertEqual(later, manifest["revision"])
        self.assertEqual([self.when, later], [row["revision"] for row in manifest["documents"]])

    def test_explicit_same_source_layout_correction_survives_later_admission(self):
        catalog = self.prepare()
        first, second = self.review(catalog), self.review(catalog, index=1, language="it")
        s.admit(self.root, self.config, [self.packet([first])], self.when)
        paths = s.paths_for(self.config["series_id"])
        catalog = s.read_json(self.root / paths["catalog"])
        unit = next(row for row in catalog["documents"] if row["id"] == first["document_id"])
        later = "2026-10-26T06:00:00Z"
        unit.update(render_revision=later, typeset_overrides={"allow_long_token_breaks": True,
            "source_note_append": "Literal long OCR runs may wrap without inserted characters."})
        s.legacy.write(self.root / paths["catalog"], s.legacy.json_bytes(catalog))
        s.admit(self.root, self.config, [self.packet([second])], later)
        row = next(row for row in s.read_json(self.root / paths["manifest"])["documents"] if row["id"] == unit["id"])
        self.assertEqual(later, row["revision"])
        self.assertTrue(row["allow_long_token_breaks"])
        self.assertTrue(row["source_note"].endswith(unit["typeset_overrides"]["source_note_append"]))
        self.assertEqual(unit["artifact_sha256"], row["sha256"])
        self.assertEqual(unit["review"]["physical_line_ranges"], row["physical_line_ranges"])
        self.assertEqual("ok", s.check(self.root, self.config)["status"])

    def test_invalid_layout_override_refuses_before_any_admission_write(self):
        catalog = self.prepare()
        catalog["documents"][0]["typeset_overrides"] = {"allow_long_token_breaks": "true"}
        s.legacy.write(self.root / s.paths_for(self.config["series_id"])["catalog"], s.legacy.json_bytes(catalog))
        packet = self.packet([self.review(catalog)])
        with patch.object(s.legacy, "write") as write:
            with self.assertRaisesRegex(ValueError, "literal boolean"):
                s.admit(self.root, self.config, [packet], self.when)
            write.assert_not_called()

    def test_unknown_publisher_new_rows_are_truthful_and_old_rows_remain_exact(self):
        self.config["volumes"][0]["publication"] = "Synthetic volume. Rome: None, 1900."
        catalog = self.prepare()
        with patch.object(s, "_reader_publication", side_effect=lambda value: value):
            s.admit(self.root, self.config, [self.packet([self.review(catalog)])], self.when)
        path = self.root / s.paths_for(self.config["series_id"])["manifest"]
        old = s.read_json(path)["documents"][0]
        old_bytes = s.legacy.json_bytes(old)
        # Existing immutable TOML may have a different harmless serialization.
        current = s.read_json(self.root / s.paths_for(self.config["series_id"])["catalog"])["documents"][0]
        segment = self.root / current["segment_path"]
        for source in (segment, segment.parents[1] / "edition.toml", segment.parents[3] / "work.toml"):
            source.write_bytes(b"# Existing immutable source record.\n" + source.read_bytes())
        source_bytes = {p: p.read_bytes() for p in (self.root / "src/sources/works").rglob("*") if p.is_file()}
        later = "2026-10-26T06:00:00Z"
        s.admit(self.root, self.config, [self.packet([self.review(catalog), self.review(catalog, 1, "it")])], later)
        rows = s.read_json(path)["documents"]
        self.assertEqual(old_bytes, s.legacy.json_bytes(rows[0]))
        self.assertIn("Rome: None,", rows[0]["source_note"])
        self.assertIn("Rome, 1900.", rows[1]["source_note"])
        self.assertNotIn("None", rows[1]["source_note"])
        self.assertEqual(self.when, rows[0]["revision"])
        self.assertEqual(later, rows[1]["revision"])
        self.assertTrue(all(p.read_bytes() == data for p, data in source_bytes.items()))
        current = s.read_json(self.root / s.paths_for(self.config["series_id"])["catalog"])["documents"]
        second_edition = (self.root / current[1]["segment_path"]).parents[1] / "edition.toml"
        self.assertEqual("Synthetic volume. Rome, 1900.", tomllib.loads(second_edition.read_text())["publication"])
        self.assertIn("Rome: None,", tomllib.loads((segment.parents[1] / "edition.toml").read_text())["publication"])

    def test_changed_constituent_printing_refuses_before_earlier_new_records_are_written(self):
        catalog = self.prepare()
        s.admit(self.root, self.config, [self.packet([self.review(catalog)])], self.when)
        self.config["volumes"][0]["publication"] = "A different printing cannot replace an existing edition."
        packet = self.packet([self.review(catalog, 1, "it"), self.review(catalog)])
        with patch.object(s.legacy, "write") as write, patch.object(s, "new_record") as record:
            with self.assertRaisesRegex(ValueError, "existing constituent printing metadata would change"):
                s.admit(self.root, self.config, [packet], "2026-10-26T06:00:00Z")
            write.assert_not_called()
            record.assert_not_called()

    def test_same_revision_source_change_refuses_before_any_write(self):
        catalog = self.prepare()
        s.admit(self.root, self.config, [self.packet([self.review(catalog)])], self.when)
        path = self.root / s.paths_for(self.config["series_id"])["catalog"]
        changed = s.read_json(path)
        changed["documents"][0]["review"]["physical_line_ranges"] = [[2, 5]]
        s.legacy.write(path, s.legacy.json_bytes(changed))
        packet = self.packet([])
        with patch.object(s.legacy, "write") as write, patch.object(s, "new_record") as record:
            with self.assertRaisesRegex(ValueError, "source changed without a newer render revision"):
                s.admit(self.root, self.config, [packet], "2026-10-26T06:00:00Z")
            write.assert_not_called()
            record.assert_not_called()

    def test_implicit_prior_row_revision_cannot_follow_a_new_manifest_header(self):
        catalog = self.prepare()
        s.admit(self.root, self.config, [self.packet([self.review(catalog)])], self.when)
        path = self.root / s.paths_for(self.config["series_id"])["manifest"]
        manifest = s.read_json(path)
        manifest["documents"][0].pop("revision")
        s.legacy.write(path, s.legacy.json_bytes(manifest))
        packet = self.packet([self.review(catalog, 1, "it")])
        with patch.object(s.legacy, "write") as write, patch.object(s, "new_record") as record:
            with self.assertRaisesRegex(ValueError, "pin its own render revision"):
                s.admit(self.root, self.config, [packet], "2026-10-26T06:00:00Z")
            write.assert_not_called()
            record.assert_not_called()

    def test_source_pinned_format_and_options_correction_requires_new_row_revision(self):
        self.config["volumes"][0]["publication"] = "Synthetic volume. Rome: None, 1900."
        catalog = self.prepare()
        with patch.object(s, "_reader_publication", side_effect=lambda value: value):
            s.admit(self.root, self.config, [self.packet([self.review(catalog)])], self.when)
        paths = s.paths_for(self.config["series_id"])
        manifest = self.root / paths["manifest"]
        old = s.read_json(manifest)["documents"][0]
        catalog = s.read_json(self.root / paths["catalog"])
        unit = catalog["documents"][0]
        unit["typeset_overrides"] = {"allow_long_token_breaks": True,
            "source_note_append": "Literal project-owned fixture runs may wrap without added characters."}
        s.legacy.write(self.root / paths["catalog"], s.legacy.json_bytes(catalog))
        packet = self.packet([])
        with patch.object(s.legacy, "write") as write, patch.object(s, "new_record") as record:
            with self.assertRaisesRegex(ValueError, "requires a newer render revision"):
                s.admit(self.root, self.config, [packet], "2026-10-26T06:00:00Z")
            write.assert_not_called()
            record.assert_not_called()
        unit["render_revision"] = "2026-10-26T06:00:00Z"
        s.legacy.write(self.root / paths["catalog"], s.legacy.json_bytes(catalog))
        s.admit(self.root, self.config, [packet], unit["render_revision"])
        row = s.read_json(manifest)["documents"][0]
        self.assertNotIn("None", row["source_note"])
        self.assertTrue(row["allow_long_token_breaks"])
        self.assertEqual(unit["render_revision"], row["revision"])
        for key in ("artifact_id", "sha256", "segment_id", "segment_path", "physical_line_ranges", "text_path"):
            self.assertEqual(old[key], row[key])

    def reader_variant_fixture(self):
        catalog = self.prepare()
        s.admit(self.root, self.config, [self.packet([self.review(catalog)])], self.when)
        paths = s.paths_for(self.config["series_id"])
        catalog = s.read_json(self.root / paths["catalog"])
        parent = catalog["documents"][0]
        variant = copy.deepcopy(parent)
        variant.update(id=parent["id"] + ".provider-marks-omitted-v2", parent_id=parent["id"],
            selection_variant_of=parent["id"], status="reader-selection-variant", render_revision="2026-10-26T06:00:00Z",
            segment_id=parent["segment_id"] + ".provider-marks-omitted-v2", physical_line_ranges=[[3, 6]])
        variant["review"].update(document_id=variant["id"], physical_line_ranges=[[3, 6]],
            review_note="Project-owned fixture: a separate project reader selection, not another historical act.")
        old_segment = self.root / parent["segment_path"]
        segment = tomllib.loads(old_segment.read_text())
        segment.update(id=variant["segment_id"], physical_line_ranges=[[3, 6]])
        new_segment = old_segment.with_name("provider-marks-omitted-v2.toml")
        s.new_record(new_segment, segment)
        variant["segment_path"] = str(new_segment.relative_to(self.root))
        catalog["documents"].append(variant)
        catalog["coverage"] = s.coverage(catalog)
        s.legacy.write(self.root / paths["catalog"], s.legacy.json_bytes(catalog))
        old_row = s.read_json(self.root / paths["manifest"])["documents"][0]
        row = {**old_row, "id": variant["id"], "revision": variant["render_revision"],
               "segment_id": variant["segment_id"], "segment_path": variant["segment_path"], "physical_line_ranges": [[3, 6]]}
        def pin(owner):
            return {"id": owner["id"], "language": owner["review"]["language"], "artifact_id": owner["artifact_id"],
                    "source_sha256": owner["artifact_sha256"], "segment_id": owner["segment_id"],
                    "physical_line_ranges": owner["review"]["physical_line_ranges"]}
        action = {"prior": {**pin(parent), "pdf_sha256": "1" * 64}, "replacement": pin(variant),
                  "reason": "A separate source-pinned project selection omits the synthetic caption."}
        shared = {"schema": s.TYPESET_SCHEMA, "revision": variant["render_revision"], "documents": [row], "supersessions": [action]}
        shared_path = self.root / "src/sources/papal-documents/historical-series-corrections-manifest.json"
        s.legacy.write(shared_path, s.legacy.json_bytes(shared))
        return catalog, parent, variant, shared_path, shared

    def test_reader_variants_keep_historical_identity_counts_and_base_rows(self):
        catalog, parent, variant, _, _ = self.reader_variant_fixture()
        paths = s.paths_for(self.config["series_id"])
        self.assertEqual(1, catalog["coverage"]["complete_printed_witnesses"])
        self.assertEqual("ok", s.check(self.root, self.config)["status"])
        old_row = s.read_json(self.root / paths["manifest"])["documents"][0]
        second = self.review({"documents": catalog["documents"]}, 1, "it")
        s.admit(self.root, self.config, [self.packet([second])], "2026-10-26T07:00:00Z")
        current = s.read_json(self.root / paths["catalog"])
        rows = s.read_json(self.root / paths["manifest"])["documents"]
        self.assertEqual(2, current["coverage"]["complete_printed_witnesses"])
        self.assertEqual(2, len(rows))
        self.assertNotIn(variant["id"], [row["id"] for row in rows])
        self.assertEqual(old_row, next(row for row in rows if row["id"] == parent["id"]))
        packet = self.packet([variant["review"]])
        with patch.object(s.legacy, "write") as write:
            with self.assertRaisesRegex(ValueError, "cannot be admitted as independent acts"):
                s.admit(self.root, self.config, [packet], "2026-10-26T08:00:00Z")
            write.assert_not_called()

    def test_reader_variant_segment_and_shared_correction_pins_are_checked(self):
        _, _, variant, shared_path, shared = self.reader_variant_fixture()
        segment_path = self.root / variant["segment_path"]
        segment = tomllib.loads(segment_path.read_text())
        bad = {**segment, "artifact_sha256": "0" * 64}
        segment_path.write_text("\n".join(f"{key} = {s._toml_value(value)}" for key, value in bad.items()) + "\n")
        with self.assertRaisesRegex(ValueError, "source pin"):
            s.check(self.root, self.config)
        segment_path.write_text("\n".join(f"{key} = {s._toml_value(value)}" for key, value in segment.items()) + "\n")
        mutations = [(lambda data: data["documents"][0].update(physical_line_ranges=[[2, 6]]), "catalog source"),
                     (lambda data: data["supersessions"][0]["prior"].pop("pdf_sha256"), "prior PDF"),
                     (lambda data: data.update(supersessions=[]), "exact prior PDF/source")]
        for mutate, message in mutations:
            with self.subTest(message=message):
                bad = copy.deepcopy(shared)
                mutate(bad)
                s.legacy.write(shared_path, s.legacy.json_bytes(bad))
                with self.assertRaisesRegex(ValueError, message):
                    s.check(self.root, self.config)

    def test_metadata_only_variant_still_uses_a_distinct_segment_without_another_act(self):
        catalog, parent, variant, shared_path, shared = self.reader_variant_fixture()
        variant["physical_line_ranges"] = copy.deepcopy(parent["review"]["physical_line_ranges"])
        variant["review"]["physical_line_ranges"] = copy.deepcopy(variant["physical_line_ranges"])
        path = self.root / variant["segment_path"]
        segment = tomllib.loads(path.read_text())
        segment["physical_line_ranges"] = variant["physical_line_ranges"]
        path.write_text("\n".join(f"{key} = {s._toml_value(value)}" for key, value in segment.items()) + "\n")
        shared["documents"][0]["physical_line_ranges"] = variant["physical_line_ranges"]
        shared["supersessions"][0]["replacement"]["physical_line_ranges"] = variant["physical_line_ranges"]
        s.legacy.write(shared_path, s.legacy.json_bytes(shared))
        s.legacy.write(self.root / s.paths_for(self.config["series_id"])["catalog"], s.legacy.json_bytes(catalog))
        self.assertEqual("ok", s.check(self.root, self.config)["status"])
        self.assertEqual(1, s.coverage(catalog)["complete_printed_witnesses"])
        variant["selection_variant_of"] = "unrelated.parent"
        s.legacy.write(self.root / s.paths_for(self.config["series_id"])["catalog"], s.legacy.json_bytes(catalog))
        with self.assertRaisesRegex(ValueError, "admitted historical parent"):
            s.check(self.root, self.config)

    def reader_withdrawal_fixture(self):
        catalog = self.prepare()
        s.admit(self.root, self.config, [self.packet([self.review(catalog)])], self.when)
        paths = s.paths_for(self.config["series_id"])
        catalog = s.read_json(self.root / paths["catalog"])
        unit = catalog["documents"][0]
        old_row = s.read_json(self.root / paths["manifest"])["documents"][0]
        action = {"prior": {"id": unit["id"], "language": old_row["language"], "artifact_id": unit["artifact_id"],
            "source_sha256": unit["artifact_sha256"], "segment_id": unit["segment_id"],
            "physical_line_ranges": old_row["physical_line_ranges"], "pdf_sha256": "1" * 64},
            "replacement": None, "reason": "Project-owned fixture: missing substantive body cells prevent a complete reader."}
        unit.update(status="specifically-held", reader_withdrawal=copy.deepcopy(action), review_history=[copy.deepcopy(unit["review"])],
            review={"document_id": unit["id"], "artifact_sha256": unit["artifact_sha256"], "decision": "hold", "review_note": action["reason"]})
        catalog["coverage"] = s.coverage(catalog)
        s.legacy.write(self.root / paths["catalog"], s.legacy.json_bytes(catalog))
        shared = {"schema": s.TYPESET_SCHEMA, "revision": "2026-10-26T06:00:00Z", "documents": [], "supersessions": [action]}
        shared_path = self.root / "src/sources/papal-documents/historical-series-corrections-manifest.json"
        s.legacy.write(shared_path, s.legacy.json_bytes(shared))
        return catalog, unit, old_row, shared_path, shared

    def test_explicit_withdrawal_retains_prior_row_and_generic_planner_excludes_it(self):
        catalog, unit, old_row, shared_path, _ = self.reader_withdrawal_fixture()
        self.assertEqual(0, catalog["coverage"]["complete_printed_witnesses"])
        self.assertEqual("ok", s.check(self.root, self.config)["status"])
        paths = s.paths_for(self.config["series_id"])
        source_bytes = {p: p.read_bytes() for p in (self.root / "src/sources/works").rglob("*") if p.is_file()}
        s.admit(self.root, self.config, [self.packet([self.review(catalog, 1, "it")])], "2026-10-26T07:00:00Z")
        manifest_path = self.root / paths["manifest"]
        rows = s.read_json(manifest_path)["documents"]
        self.assertEqual(s.legacy.json_bytes(old_row), s.legacy.json_bytes(next(row for row in rows if row["id"] == unit["id"])))
        self.assertTrue(all(p.read_bytes() == data for p, data in source_bytes.items()))
        import _papal_collection as collection
        result = collection.plan_sources([{"name": "series", "path": manifest_path}],
            [{"name": "corrections", "path": shared_path}], self.root / ".scratch/current.json")
        self.assertNotIn(unit["id"], [row["id"] for row in result["documents"]])
        self.assertEqual(1, len(result["documents"]))

    def test_withdrawal_requires_exact_shared_assertion_and_archived_review(self):
        catalog, unit, _, shared_path, shared = self.reader_withdrawal_fixture()
        bad = copy.deepcopy(shared)
        bad["supersessions"][0]["reason"] = "A different assertion does not authorize removal."
        s.legacy.write(shared_path, s.legacy.json_bytes(bad))
        with self.assertRaisesRegex(ValueError, "identical shared null"):
            s.check(self.root, self.config)
        s.legacy.write(shared_path, s.legacy.json_bytes(shared))
        unit["review_history"] = []
        s.legacy.write(self.root / s.paths_for(self.config["series_id"])["catalog"], s.legacy.json_bytes(catalog))
        with self.assertRaisesRegex(ValueError, "archived historical"):
            s.check(self.root, self.config)

    def test_withdrawn_base_row_cannot_disappear_or_be_readmitted(self):
        _, unit, _, _, _ = self.reader_withdrawal_fixture()
        packet = self.packet([unit["review_history"][0]])
        with patch.object(s.legacy, "write") as write, patch.object(s, "new_record") as record:
            with self.assertRaisesRegex(ValueError, "cannot be admitted as independent acts"):
                s.admit(self.root, self.config, [packet], "2026-10-26T07:00:00Z")
            write.assert_not_called()
            record.assert_not_called()
        path = self.root / s.paths_for(self.config["series_id"])["manifest"]
        manifest = s.read_json(path)
        manifest["documents"] = []
        s.legacy.write(path, s.legacy.json_bytes(manifest))
        with self.assertRaisesRegex(ValueError, "missing its pinned prior component"):
            s.check(self.root, self.config)

    def test_held_row_without_explicit_withdrawal_is_not_silently_retired(self):
        catalog, unit, _, _, _ = self.reader_withdrawal_fixture()
        unit.pop("reader_withdrawal")
        s.legacy.write(self.root / s.paths_for(self.config["series_id"])["catalog"], s.legacy.json_bytes(catalog))
        with self.assertRaisesRegex(ValueError, "matching admitted catalog entry"):
            s.check(self.root, self.config)
        packet = self.packet([])
        with patch.object(s.legacy, "write") as write, patch.object(s, "new_record") as record:
            with self.assertRaisesRegex(ValueError, "existing base reader would disappear"):
                s.admit(self.root, self.config, [packet], "2026-10-26T07:00:00Z")
            write.assert_not_called()
            record.assert_not_called()

    def test_recorded_rescript_requires_actual_audience_response_date_and_official(self):
        raw = ["Ex audientia SSmi.", "Sanctissimus benigne annuit pro gratia.", "Die 13 Iunii 1781.", "P. H. Massei, armorum praeses."]
        item = {"document_form": "recorded-audience-rescript", "recording_official": raw[3], "papal_context": "Pius VI",
            "recorded_rescript_evidence": {"audience_lines": [1, 1], "audience_formula": raw[0],
                "response_lines": [2, 2], "response_formula": raw[1], "date_lines": [3, 3], "date_raw": raw[2],
                "subscription_lines": [4, 4], "basis": "Project-owned synthetic formal audience response; no inference from a collection heading."}}
        s._review_recorded_rescript(raw, item, [[1, 4]])
        bad = copy.deepcopy(item)
        bad["recording_official"] = "Different official"
        with self.assertRaisesRegex(ValueError, "literal"):
            s._review_recorded_rescript(raw, bad, [[1, 4]])
        with self.assertRaisesRegex(ValueError, "extent"):
            s._review_recorded_rescript(raw, item, [[1, 3]])

    def test_recorded_rescript_metadata_names_recording_official_and_papal_context(self):
        catalog = self.prepare()
        item = self.review(catalog)
        item.update(document_form="recorded-audience-rescript", recording_official="P. H. Massei, armorum praeses.", papal_context="Pius VI",
            source_responsible="P. H. Massei, armorum praeses (recording official)", recorded_rescript_evidence={
                "audience_lines": [5, 5], "audience_formula": "Ex audientia SSmi.", "response_lines": [5, 5], "response_formula": "Sanctissimus benigne annuit pro gratia.",
                "date_lines": [5, 5], "date_raw": "Die 13 Iunii 1781.", "subscription_lines": [6, 6], "basis": "Synthetic formal response with distinct authority and recording roles."})
        s.admit(self.root, self.config, [self.packet([item])], self.when)
        manifest = s.read_json(self.root / s.paths_for(self.config["series_id"])["manifest"])
        self.assertEqual("P. H. Massei, armorum praeses (recording official)", manifest["documents"][0]["pope"])
        self.assertEqual("Pius VI", manifest["documents"][0]["pope_context"])
        self.assertIn("recorded by P. H. Massei", manifest["documents"][0]["source_note"])

    def test_ocr_audience_variant_needs_exact_registered_native_page_evidence(self):
        self.config["volumes"][0]["inputs"]["imprint"]["media_type"] = "image/png"
        catalog = self.prepare()
        volume = catalog["volumes"][0]
        image = volume["container"]["artifacts"]["imprint"]
        raw = ["Ex audieotia SSini.", "Sanctissimus benigne annuit pro gratia.", "Die 13 Iunii 1781.", "P. H. Massei, armorum praeses."]
        item = {"document_form": "recorded-audience-rescript", "recording_official": raw[3], "papal_context": "Pius VI",
            "recorded_rescript_evidence": {"audience_lines": [1, 1], "audience_formula": raw[0],
                "response_lines": [2, 2], "response_formula": raw[1], "date_lines": [3, 3], "date_raw": raw[2],
                "subscription_lines": [4, 4], "basis": "Synthetic OCR variant, never normalized in source wording."}}
        with self.assertRaisesRegex(ValueError, "native-image evidence"):
            s._review_recorded_rescript(raw, item, [[1, 4]], root=self.root, volume=volume)
        native = {"artifact_id": image["id"], "artifact_sha256": image["sha256"], "printed_formula": "Ex audientia SSmi.",
                  "artifact_page": 1, "leaf": 7, "basis": "Project-owned synthetic native-image evidence fixture."}
        item["recorded_rescript_evidence"]["native_audience_evidence"] = native
        s._review_recorded_rescript(raw, item, [[1, 4]], root=self.root, volume=volume)
        self.assertEqual("Ex audieotia SSini.", item["recorded_rescript_evidence"]["audience_formula"])
        native["leaf"] = 8
        with self.assertRaisesRegex(ValueError, "page/leaf"):
            s._review_recorded_rescript(raw, item, [[1, 4]], root=self.root, volume=volume)
        native.update(leaf=7, artifact_sha256="0" * 64)
        with self.assertRaisesRegex(ValueError, "whole image"):
            s._review_recorded_rescript(raw, item, [[1, 4]], root=self.root, volume=volume)


if __name__ == "__main__":
    unittest.main()
