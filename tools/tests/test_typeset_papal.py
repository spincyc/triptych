"""Papal extraction preserves whole bodies; rendering requires exact lawful bytes."""
from __future__ import annotations

import hashlib
import io
import json
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))
import _typeset_papal as papal


class ExtractionTests(unittest.TestCase):
    def test_body_headings_signature_notes_and_inline_boundaries_survive(self):
        html = b'''<html><title>Witness</title><nav>Discard navigation</nav>
        <div class="documento"><div class="testo"><div class="translation-field">EN LA</div>
        <div class="abstract vaticanrichtext"><p>ORIGINAL TITLE</p></div>
        <div class="vaticanrichtext"><h2>Original heading</h2>
        <p>1. Preserve <i>these words</i>, and punctuation.<br>Second line joins.</p>
        <p>2. Original numbered text<a href="#note">[1]</a>.</p>
        <script>Discard executable text</script><p>Datum Romae. LEO PP. XIII.</p>
        <div><p>[1] The original endnote, retained to the final word.</p></div></div>
        </div></div><footer>Discard footer</footer></html>'''
        result = papal.extract_document(html, "https://example.org/witness")
        self.assertEqual(result["title"], "Witness")
        self.assertEqual(result["blocks"][1], {"kind": "heading", "text": "Original heading"})
        self.assertIn("1. Preserve these words, and punctuation. Second line joins.", result["text"])
        self.assertIn("text[1].", result["text"])
        self.assertTrue(result["text"].endswith("retained to the final word.\n"))
        for absent in ("Discard", "EN LA"):
            self.assertNotIn(absent, result["text"])
        self.assertEqual(result["text"], "\n\n".join(block["text"] for block in result["blocks"]) + "\n")

    def test_no_fallback_to_arbitrary_page_text(self):
        for html in (b"<p>" + b"Long page " * 80 + b"</p>",
                     b'<div class="documento"><div class="testo"><div class="vaticanrichtext"><p>Short</p></div></div></div>'):
            with self.assertRaises(papal.PapalTypesetError):
                papal.extract_document(html)

    def test_html_entities_and_inline_styling_do_not_change_wording(self):
        html = ('<div class="documento"><div class="testo"><div class="vaticanrichtext">'
                '<p>' + 'A&amp;B: <b>de</b> fide; &aelig; &nbsp; Christus. ' * 6 + '</p>'
                '</div></div></div>').encode()
        self.assertIn("A&B: de fide; æ Christus.", papal.extract_document(html)["text"])

    def test_nested_paragraphs_and_displayed_list_numbering_survive(self):
        html = ("<div class='documento'><div class='testo'><div class='vaticanrichtext'>"
                "<blockquote><p>First paragraph.</p><p>Second paragraph.</p></blockquote>"
                "<ol start='4'><li>Fourth list item.</li><li value='8'>Eighth list item.</li></ol>"
                "<ol reversed type='I'><li>Second roman item.</li><li>First roman item.</li></ol>"
                "</div></div></div>").encode()
        text = papal.extract_document(html)["text"]
        self.assertIn("First paragraph.\n\nSecond paragraph.", text)
        self.assertIn("4. Fourth list item.\n\n8. Eighth list item.", text)
        self.assertIn("II. Second roman item.\n\nI. First roman item.", text)


class ManifestTests(unittest.TestCase):
    def setUp(self):
        scratch = ROOT / ".scratch/typeset_pipeline/tests"
        scratch.mkdir(parents=True, exist_ok=True)
        self.temp = tempfile.TemporaryDirectory(dir=scratch)
        self.root = Path(self.temp.name)
        self.payload_path = self.root / "src/sources/works/test/editions/1903-test/artifacts/text/text.txt"
        self.payload_path.parent.mkdir(parents=True)
        self.payload = "1. Test source words with æ, %, &, #, _ and {braces}.\n\n2. Final paragraph.\n"
        self.payload_path.write_text(self.payload, encoding="utf-8")
        self.doc = {"id": "papal.test.fixture", "title": "Fixture", "pope": "Test author",
                    "date": "1903-01-01", "language": "en", "source_url": "https://example.org/source",
                    "text_path": self.payload_path.relative_to(self.root).as_posix(),
                    "sha256": hashlib.sha256(self.payload.encode()).hexdigest(),
                    "artifact_id": "artifact.test.fixture.text", "rights_status": "public-domain",
                    "rights_basis": "Synthetic test fixture; no external source wording."}
        self.artifact = {"schema": 1, "record_type": "artifact", "id": self.doc["artifact_id"],
                         "edition_id": "edition.test.fixture", "source_url": self.doc["source_url"],
                         "storage": "tracked", "rights_status": self.doc["rights_status"],
                         "rights_basis": self.doc["rights_basis"], "sha256": self.doc["sha256"],
                         "byte_size": len(self.payload.encode()), "path": self.doc["text_path"],
                         "media_type": "text/plain; charset=utf-8"}
        self.write_artifact()
        (self.payload_path.parents[2] / "edition.toml").write_text(
            'schema = 1\nrecord_type = "edition"\nid = "edition.test.fixture"\nlanguage = "en"\n')
        self.manifest = {"schema": papal.SCHEMA, "revision": "2026-10-25T21:00:00Z", "documents": [self.doc]}

    def tearDown(self):
        self.temp.cleanup()

    def write_artifact(self):
        self.payload_path.with_name("artifact.toml").write_text(
            "\n".join(f"{key} = {json.dumps(value)}" for key, value in self.artifact.items()) + "\n", encoding="utf-8")

    def test_source_manifest_and_payload_must_agree(self):
        checked = papal.validate_document(self.doc, self.root)
        self.assertEqual(checked["text"], self.payload)
        self.artifact["rights_status"] = "restricted"
        self.write_artifact()
        with self.assertRaisesRegex(papal.PapalTypesetError, "rights_status"):
            papal.validate_document(self.doc, self.root)

    def test_installer_cli_dispatch_is_explicit_and_preparation_stdout_is_bounded(self):
        import _papal_install as installer
        summary = {"current": 3, "ready": 1, "pages": 2, "bytes": 100,
                   "review_pending": 2, "changes_required": 0, "failed": 0, "missing": 0}
        out = self.root / "prepared.json"
        def prepare(plan, pairs, target, reviews):
            self.assertEqual((plan, pairs, reviews), (Path("plan.json"), Path("pairs.json"), [Path("review.json")]))
            target.write_text('{"synthetic":true}\n')
            return {"schema": installer.PREPARED_SCHEMA, "summary": summary,
                    "documents": [{"source": "Do not copy candidate details to stdout"}]}
        stdout = io.StringIO()
        with patch.object(installer, "prepare_install", side_effect=prepare) as prepared, redirect_stdout(stdout), \
                patch.object(papal, "render_documents") as render:
            code = papal.main(["prepare-install", "--plan", "plan.json", "--batch-pairs", "pairs.json",
                               "--review", "review.json", "--out", str(out), "--json"])
        self.assertEqual(code, 0)
        self.assertEqual(json.loads(stdout.getvalue())["sha256"], hashlib.sha256(out.read_bytes()).hexdigest())
        self.assertNotIn("documents", json.loads(stdout.getvalue()))
        prepared.assert_called_once()
        render.assert_not_called()
        for verb, arguments, function, returned in (
            ("install", ["--prepared", "prepared.json"], "install_prepared", {"schema": installer.RELEASE_SCHEMA, "summary": summary}),
            ("check-install", ["--plan", "plan.json"], "check_install", {"schema": installer.RELEASE_SCHEMA,
                "status": "valid", "installed": 1, "current": 3, "not_installed": 2})):
            stdout = io.StringIO()
            with self.subTest(verb=verb), patch.object(installer, function, return_value=returned) as called, \
                    redirect_stdout(stdout), patch.object(papal, "render_documents") as render:
                self.assertEqual(papal.main([verb, *arguments, "--json"]), 0)
            called.assert_called_once_with(Path(arguments[1]))
            self.assertEqual(json.loads(stdout.getvalue())["schema"], installer.RELEASE_SCHEMA)
            render.assert_not_called()

    def test_installer_cli_refusal_is_visible_without_rendering_or_installing(self):
        import _papal_install as installer
        stderr = io.StringIO()
        with patch.object(installer, "prepare_install", side_effect=installer.PapalInstallError("source plan is stale")), \
                patch.object(installer, "install_prepared") as install, patch.object(papal, "render_documents") as render, \
                redirect_stderr(stderr):
            code = papal.main(["prepare-install", "--plan", "plan.json", "--batch-pairs", "pairs.json", "--json"])
        self.assertEqual(code, 2)
        self.assertEqual(json.loads(stderr.getvalue())["error"], "source plan is stale")
        install.assert_not_called()
        render.assert_not_called()

    def test_installer_help_never_dispatches_an_install(self):
        import _papal_install as installer
        with patch.object(installer, "install_prepared") as install, redirect_stdout(io.StringIO()):
            with self.assertRaises(SystemExit) as result:
                papal.main(["install", "--help"])
        self.assertEqual(result.exception.code, 0)
        install.assert_not_called()

    def test_missing_rights_and_payload_tampering_refuse(self):
        for key, value in (("rights_status", "unresolved"), ("rights_basis", ""), ("language", "xx")):
            changed = {**self.doc, key: value}
            with self.subTest(key=key), self.assertRaises(papal.PapalTypesetError):
                papal.validate_document(changed, self.root)
        self.payload_path.write_text(self.payload + "Changed", encoding="utf-8")
        with self.assertRaisesRegex(papal.PapalTypesetError, "SHA-256"):
            papal.validate_document(self.doc, self.root)

    def test_url_control_characters_cannot_reach_tex(self):
        for ending in (" space", "\nline", "\x00control"):
            with self.assertRaisesRegex(papal.PapalTypesetError, "HTTP"):
                papal.validate_document({**self.doc, "source_url": "https://example.org/" + ending}, self.root)

    def test_selection_language_and_declared_source_url_are_bound_to_source_records(self):
        with self.assertRaisesRegex(papal.PapalTypesetError, "document language"):
            papal.validate_document({**self.doc, "language": "la"}, self.root)
        with self.assertRaisesRegex(papal.PapalTypesetError, "source_url disagrees"):
            papal.validate_document({**self.doc, "source_url": "https://example.org/unrelated"}, self.root)
        del self.artifact["source_url"]
        self.write_artifact()
        self.assertEqual(papal.validate_document(self.doc, self.root)["language"], "en")

    def test_mixed_edition_uses_truthful_escaped_language_label(self):
        edition = self.payload_path.parents[2] / "edition.toml"
        edition.write_text('schema = 1\nrecord_type = "edition"\nid = "edition.test.fixture"\nlanguage = "mul"\n')
        doc = papal.validate_document({**self.doc, "language": "mul", "language_label": "Latin & Italian"}, self.root)
        self.assertIn(r"Latin \& Italian", papal.render_tex(doc, self.manifest["revision"]))
        generic = {key: value for key, value in doc.items() if key != "language_label"}
        self.assertIn("Multilingual", papal.render_tex(generic, self.manifest["revision"]))
        self.assertEqual(doc["text"], self.payload)
        index = papal.render_index(self.root, [doc], {"summary":{"compiled":0,"failed":0}, "documents":[{"id":doc["id"],"language":"mul","status":"rendered","tex":"no-file.tex"}]})
        self.assertIn("Latin &amp; Italian", index)
        self.assertNotIn("Single-language", index)
        for bad in ("", "A\nB", " Latin", 12):
            with self.assertRaisesRegex(papal.PapalTypesetError, "language_label"):
                papal.validate_document({**doc, "language_label": bad}, self.root)
        edition.write_text('schema = 1\nrecord_type = "edition"\nid = "edition.test.fixture"\nlanguage = "en"\n')
        primary = papal.validate_document({**self.doc, "language_label": "English, with Latin quotations"}, self.root)
        self.assertIn("English, with Latin quotations", papal.render_tex(primary, self.manifest["revision"]))

    def test_hashed_text_cannot_be_replaced_by_unchecked_blocks(self):
        doc = {**self.doc, "blocks": [{"kind": "paragraph", "text": "A different text"}]}
        with self.assertRaisesRegex(papal.PapalTypesetError, "block wording"):
            papal.validate_document(doc, self.root)

    def test_truthful_segment_uses_pinned_container_lines_without_a_copy(self):
        segment = self.root / "src/sources/works/constituent/editions/1903/segments/part.toml"
        segment.parent.mkdir(parents=True)
        segment.write_text('schema = 2\nrecord_type = "segment"\nid = "segment.test.part"\n'
                           'edition_id = "edition.test.constituent"\n'
                           f'artifact_id = "{self.doc["artifact_id"]}"\n'
                           f'artifact_sha256 = "{self.doc["sha256"]}"\n'
                           'physical_line_ranges = [[3, 3]]\n', encoding="utf-8")
        (segment.parents[1] / "edition.toml").write_text(
            'schema = 1\nrecord_type = "edition"\nid = "edition.test.constituent"\nlanguage = "la"\n')
        doc = {**self.doc, "language": "la", "segment_id": "segment.test.part", "segment_path": segment.relative_to(self.root).as_posix(),
               "physical_line_ranges": [[3, 3]]}
        checked = papal.validate_document(doc, self.root)
        self.assertEqual(checked["text"], "2. Final paragraph.")
        with self.assertRaisesRegex(papal.PapalTypesetError, "document language"):
            papal.validate_document({**doc, "language": "en"}, self.root)
        bad = {**doc, "physical_line_ranges": [[1, 1]]}
        with self.assertRaisesRegex(papal.PapalTypesetError, "segment manifest disagrees"):
            papal.validate_document(bad, self.root)

    @unittest.skipUnless(shutil.which("xelatex") and shutil.which("pdfinfo") and shutil.which("pdftotext"), "PDF toolchain unavailable")
    def test_declared_range_continuation_joins_only_selected_boundary_and_preserves_pdf_words(self):
        self.payload = "Source words remain perpe-\nExcluded journal footer\ntua without dehyphenation.\n\nOwn historical note.\n"
        self.payload_path.write_text(self.payload, encoding="utf-8")
        self.doc["sha256"] = hashlib.sha256(self.payload.encode()).hexdigest()
        self.artifact.update(sha256=self.doc["sha256"], byte_size=len(self.payload.encode()))
        self.write_artifact()
        segment = self.root / "src/sources/works/constituent/editions/1903/segments/continued.toml"
        segment.parent.mkdir(parents=True)
        segment.write_text('schema = 2\nrecord_type = "segment"\nid = "segment.test.continued"\n'
                           'edition_id = "edition.test.continued"\n'
                           f'artifact_id = "{self.doc["artifact_id"]}"\n'
                           f'artifact_sha256 = "{self.doc["sha256"]}"\n'
                           'physical_line_ranges = [[1, 1], [3, 3], [5, 5]]\n', encoding="utf-8")
        (segment.parents[1] / "edition.toml").write_text(
            'schema = 1\nrecord_type = "edition"\nid = "edition.test.continued"\nlanguage = "en"\n')
        row = {**self.doc, "segment_id": "segment.test.continued",
               "segment_path": segment.relative_to(self.root).as_posix(),
               "physical_line_ranges": [[1, 1], [3, 3], [5, 5]], "range_continuations": [0]}
        document = papal.validate_document(row, self.root)
        self.assertEqual([block["text"] for block in document["blocks"]],
                         ["Source words remain perpe- tua without dehyphenation.", "Own historical note."])
        unjoined = papal.validate_document({key: value for key, value in row.items()
                                           if key != "range_continuations"}, self.root)
        self.assertEqual(re.sub(r"\s", "", document["text"]), re.sub(r"\s", "", unjoined["text"]))
        self.assertEqual(self.payload_path.read_text(), self.payload)
        receipt = papal.render_documents({**self.manifest, "documents": [row]}, [document],
                                         self.root / "range-continuation", True)
        self.assertEqual(receipt["errors"], [])
        self.assertEqual(receipt["documents"][0]["range_continuations"], [0])
        self.assertEqual(receipt["documents"][0]["text_fidelity"]["status"], "pass")
        pdf = self.root / "range-continuation" / receipt["documents"][0]["pdf"]
        extracted = subprocess.check_output(["pdftotext", "-raw", str(pdf), "-"], text=True)
        self.assertIn("perpe- tua", extracted)
        self.assertNotIn("Excluded journal footer", extracted)
        for bad in ([2], [-1], [0, 0], [1, 0], [True], "0", None):
            with self.subTest(bad=bad), self.assertRaisesRegex(papal.PapalTypesetError, "range_continuations"):
                papal.validate_document({**row, "range_continuations": bad}, self.root)
        with self.assertRaisesRegex(papal.PapalTypesetError, "registered segment"):
            papal.validate_document({**self.doc, "range_continuations": [0]}, self.root)

    def test_escape_preserves_printed_metacharacters_and_blocks_input(self):
        self.assertEqual(papal.tex_escape(r"a\b {x} $ & # % _ ^ ~"),
                         r"a\textbackslash{}b \{x\} \$ \& \# \% \_ \textasciicircum{} \textasciitilde{}")
        with self.assertRaises(papal.PapalTypesetError):
            papal.tex_escape("bad\x00text")

    @unittest.skipUnless(shutil.which("xelatex") and shutil.which("pdfinfo") and shutil.which("pdftotext"), "PDF toolchain unavailable")
    def test_explicit_long_ocr_wrap_preserves_every_character_and_pdf_fidelity(self):
        token = "RRRALLLLLICCCCÉCCCÓÉOCÓÉÓÉÉÓÉÓÉÓÉÓÉÓÉÓÉÓÉÓÉÓÓÉÓÉÓÉÓÓRÓRÓRÓROOÓ—————M"
        self.payload = "Ordinary short source words.\n\n" + token + "\n\nFinal source note.\n"
        self.payload_path.write_text(self.payload, encoding="utf-8")
        self.doc["sha256"] = hashlib.sha256(self.payload.encode()).hexdigest()
        self.artifact.update(sha256=self.doc["sha256"], byte_size=len(self.payload.encode()))
        self.write_artifact()
        row = {**self.doc, "allow_long_token_breaks": True}
        document = papal.validate_document(row, self.root)
        body = papal.render_body(document)
        self.assertIn(r"\allowbreak{}", body)
        self.assertIn("Ordinary short source words.", body)
        self.assertEqual(papal.body_tex_escape("ordinary words", True), papal.source_tex_escape("ordinary words"))
        self.assertEqual(papal.body_tex_escape("x" * 47, True), "x" * 47)
        self.assertNotIn("m" + r"\allowbreak{}" + "\u0305", papal.body_tex_escape("m\u0305" * 30, True))
        receipt = papal.render_documents({**self.manifest, "documents": [row]}, [document],
                                         self.root / "long-ocr-wrap", True)
        self.assertEqual(receipt["errors"], [])
        self.assertEqual(receipt["documents"][0]["allow_long_token_breaks"], True)
        self.assertEqual(receipt["documents"][0]["text_fidelity"]["status"], "pass")
        self.assertEqual(document["text"], self.payload)
        self.assertEqual(self.payload_path.read_text(), self.payload)
        for bad in (None, 1, "true", []):
            with self.subTest(bad=bad), self.assertRaisesRegex(papal.PapalTypesetError, "allow_long_token_breaks"):
                papal.validate_document({**row, "allow_long_token_breaks": bad}, self.root)

    def test_render_is_byte_stable_and_single_language_two_columns(self):
        doc = papal.validate_document(self.doc, self.root)
        first = papal.render_tex(doc, self.manifest["revision"])
        self.assertEqual(first, papal.render_tex(doc, self.manifest["revision"]))
        self.assertIn(r"\documentclass[10pt,twocolumn]{article}", first)
        self.assertIn(r"\input{" + papal.output_stem(doc) + ".body.tex}", first)
        body = papal.render_body(doc)
        self.assertIn(r"2. Final paragraph.", body)
        self.assertIn(r"\%", body)
        self.assertNotEqual(papal.output_stem(doc), papal.output_stem({**doc, "language": "la"}))
        self.assertNotEqual(papal.safe_id("a.b"), papal.safe_id("a-b"))

    def test_render_retains_the_exact_manifest_read_before_the_input_file_changes(self):
        path = self.root / "input.json"
        original = (json.dumps(self.manifest, indent=4) + "\n").encode()
        path.write_bytes(original)
        manifest, documents = papal.read_manifest(path, self.root)
        changed = {**self.manifest, "revision": "2026-10-26T00:00:00Z"}
        path.write_text(json.dumps(changed))
        out = self.root / "snapshot-output"
        receipt = papal.render_documents(manifest, documents, out)
        self.assertEqual((out / "frozen-manifest.json").read_bytes(), original)
        self.assertEqual(receipt["input_manifest_sha256"], hashlib.sha256(original).hexdigest())
        self.assertEqual(receipt["revision"], self.manifest["revision"])
        manifest["revision"] = changed["revision"]
        with self.assertRaisesRegex(papal.PapalTypesetError, "changed after validation"):
            papal.render_documents(manifest, documents, out)

    def test_snapshot_cannot_claim_different_rendered_identification(self):
        document = papal.validate_document({**self.doc, "title": "Changed title"}, self.root)
        with self.assertRaisesRegex(papal.PapalTypesetError, "input manifest on title"):
            papal.render_documents(self.manifest, [document], self.root / "mismatched-input")

    def test_document_revision_requires_a_real_whole_second_utc_timestamp(self):
        for bad in (None, False, "2026-02-30T00:00:00Z", "2026-10-26T25:00:00Z",
                    "2026-10-26T00:00:00.1Z", "2026-10-26T00:00:00+00:00"):
            with self.assertRaisesRegex(papal.PapalTypesetError, "document revision"):
                papal.validate_document({**self.doc, "revision": bad}, self.root)

    @unittest.skipUnless(shutil.which("xelatex") and shutil.which("pdfinfo") and shutil.which("pdftotext"), "PDF toolchain unavailable")
    def test_row_revision_keeps_pdf_identity_when_only_inventory_revision_changes(self):
        row = {**self.doc, "revision": "2020-01-01T00:00:00Z"}
        checked = papal.validate_document(row, self.root)
        first_manifest = {**self.manifest, "documents": [row]}
        second_manifest = {**first_manifest, "revision": "2026-10-26T22:00:00Z"}
        first_out, second_out = self.root / "first-inventory", self.root / "second-inventory"
        first = papal.render_documents(first_manifest, [checked], first_out, True)
        second = papal.render_documents(second_manifest, [checked], second_out, True)
        self.assertFalse(first["errors"] or second["errors"])
        self.assertNotEqual(first["input_manifest_sha256"], second["input_manifest_sha256"])
        self.assertNotEqual(first["revision"], second["revision"])
        self.assertEqual(first["documents"][0]["render_revision"], row["revision"])
        self.assertEqual(first["documents"][0]["pdf_sha256"], second["documents"][0]["pdf_sha256"])
        self.assertEqual((first_out / first["documents"][0]["tex"]).read_bytes(),
                         (second_out / second["documents"][0]["tex"]).read_bytes())
        unpinned = papal.validate_document(self.doc, self.root)
        self.assertNotEqual(papal.render_tex(unpinned, first_manifest["revision"]),
                            papal.render_tex(unpinned, second_manifest["revision"]))

    def test_missing_normalized_date_is_omitted_without_changing_source_text(self):
        known = papal.validate_document(self.doc, self.root)
        unknown = papal.validate_document({**self.doc, "date": None}, self.root)
        rendered = papal.render_tex(unknown, self.manifest["revision"])
        self.assertNotIn("Date unrecorded", rendered)
        self.assertIn("Test author · English", rendered)
        self.assertEqual(papal.render_body(known), papal.render_body(unknown))

    def test_ocr_metadata_blank_lines_do_not_create_tex_paragraph_arguments(self):
        doc = papal.validate_document({**self.doc, "pope": "Printed issuer\n \nsecond line"}, self.root)
        rendered = papal.render_tex(doc, self.manifest["revision"])
        setup = next(line for line in rendered.splitlines() if line.startswith(r"\hypersetup"))
        self.assertIn("pdfauthor={Printed issuer second line}", setup)
        self.assertIn("Printed issuer\n \nsecond line · 1903-01-01 · English", rendered)
        self.assertEqual(doc["text"], self.payload)

    def test_heading_keep_controls_are_bounded_without_changing_source_words(self):
        doc = papal.validate_document({**self.doc, "keep_with_next": [0]}, self.root)
        self.assertIn(r"\nopagebreak[4]", papal.render_body(doc))
        self.assertEqual(doc["text"], self.payload)
        for value in ([99], [True], [1, 0], [0, 0]):
            with self.assertRaisesRegex(papal.PapalTypesetError, "keep_with_next"):
                papal.validate_document({**self.doc, "keep_with_next": value}, self.root)

    @unittest.skipUnless(shutil.which("xelatex") and shutil.which("pdfinfo") and shutil.which("pdftotext"), "PDF toolchain unavailable")
    def test_heading_can_keep_first_body_line_while_long_paragraph_flows(self):
        self.payload = "CHAPTER I.\n\n" + "Long source paragraph preserves every printed word. " * 190 + "\n\nClosing source.\n"
        self.payload_path.write_text(self.payload, encoding="utf-8")
        self.doc["sha256"] = hashlib.sha256(self.payload.encode()).hexdigest()
        self.artifact.update(sha256=self.doc["sha256"], byte_size=len(self.payload.encode()))
        self.write_artifact()
        row = {**self.doc, "keep_with_next": [0], "keep_with_next_mode": "first-line"}
        document = papal.validate_document(row, self.root)
        receipt = papal.render_documents({**self.manifest, "documents": [row]}, [document], self.root / "heading-long-body", True)
        self.assertEqual(receipt["errors"], [])
        self.assertGreater(receipt["documents"][0]["pages"], 1)
        self.assertEqual(receipt["documents"][0]["text_fidelity"]["status"], "pass")
        self.assertEqual(document["text"], self.payload)
        with self.assertRaisesRegex(papal.PapalTypesetError, "keep_with_next_mode"):
            papal.validate_document({**row, "keep_with_next_mode": "unknown"}, self.root)

    def test_explicit_compact_layout_preserves_body_size_and_fragment(self):
        normal = papal.validate_document(self.doc, self.root)
        compact = papal.validate_document({**self.doc, "compact_layout": True}, self.root)
        rendered = papal.render_tex(compact, self.manifest["revision"])
        self.assertIn(r"\documentclass[10pt,twocolumn]{article}", rendered)
        self.assertIn("margin=0.65in,columnsep=0.24in", rendered)
        self.assertIn(r"\setlength{\parskip}{1pt}", rendered)
        self.assertEqual(papal.render_body(normal), papal.render_body(compact))
        for bad in ("true", 1, None):
            with self.assertRaisesRegex(papal.PapalTypesetError, "compact_layout"):
                papal.validate_document({**self.doc, "compact_layout": bad}, self.root)

    def test_selected_compact_margin_is_bounded_without_changing_source(self):
        doc = papal.validate_document({**self.doc, "compact_layout": True, "compact_margin": 0.5}, self.root)
        rendered = papal.render_tex(doc, self.manifest["revision"])
        self.assertIn("margin=0.5in,columnsep=0.24in", rendered)
        self.assertIn(r"\documentclass[10pt,twocolumn]{article}", rendered)
        self.assertEqual(papal.render_body(doc), papal.render_body(papal.validate_document(self.doc, self.root)))
        for bad in (0.4, 0.8, "0.5", True):
            with self.assertRaisesRegex(papal.PapalTypesetError, "compact_margin"):
                papal.validate_document({**doc, "compact_margin": bad}, self.root)
        with self.assertRaisesRegex(papal.PapalTypesetError, "compact_margin"):
            papal.validate_document({**doc, "compact_layout": False}, self.root)

    def test_local_index_escapes_metadata_and_never_invents_a_pdf_link(self):
        source = {**self.doc, "title": "<script>unsafe</script>"}
        doc = papal.validate_document(source, self.root)
        out = self.root / "index-output"
        receipt = papal.render_documents({**self.manifest, "documents": [source]}, [doc], out)
        index = (out / receipt["index"]).read_text(encoding="utf-8")
        self.assertIn("&lt;script&gt;unsafe&lt;/script&gt;", index)
        self.assertNotIn("<script>", index)
        self.assertNotIn('>PDF</a>', index)
        self.assertIn('>TeX</a>', index)
        self.assertNotIn("1. Test source words", index)

    def test_failed_index_row_cannot_link_a_stale_pdf(self):
        doc = papal.validate_document(self.doc, self.root)
        out = self.root / "failed-index-output"
        receipt = papal.render_documents(self.manifest, [doc], out)
        (out / "stale.pdf").write_bytes(b"old output")
        receipt["documents"][0].update(status="failed", pdf="stale.pdf", error="Failure <detail>")
        receipt["summary"].update(failed=1)
        index = papal.render_index(out, [doc], receipt)
        self.assertIn("failed: Failure &lt;detail&gt;", index)
        self.assertNotIn('href="stale.pdf"', index)

    def test_index_metadata_follows_receipt_identity_not_list_position(self):
        first = papal.validate_document(self.doc, self.root)
        second_source = {**self.doc, "id": "papal.test.second", "title": "Second witness"}
        second = papal.validate_document(second_source, self.root)
        out = self.root / "ordered-index-output"
        receipt = papal.render_documents({**self.manifest, "documents": [self.doc, second_source]}, [first, second], out)
        index = papal.render_index(out, [second, first], receipt)
        self.assertLess(index.index("<td>Fixture</td>"), index.index("<td>Second witness</td>"))

    @unittest.skipUnless(shutil.which("xelatex") and shutil.which("pdfinfo") and shutil.which("pdftotext"), "PDF toolchain unavailable")
    def test_compiled_source_preserves_literal_quotes_backticks_and_dashes(self):
        self.payload = 'Original "double quotes", apostrophe \' and backtick `; dashes -- and ---; æ.\n'
        self.payload_path.write_text(self.payload, encoding="utf-8")
        self.doc["sha256"] = hashlib.sha256(self.payload.encode()).hexdigest()
        self.artifact.update(sha256=self.doc["sha256"], byte_size=len(self.payload.encode()))
        self.write_artifact()
        checked = papal.validate_document(self.doc, self.root)
        output = self.root / "output"
        receipt = papal.render_documents(self.manifest, [checked], output, True)
        self.assertEqual(receipt["errors"], [])
        pdf = output / receipt["documents"][0]["pdf"]
        extracted = subprocess.run(["pdftotext", str(pdf), "-"], capture_output=True, text=True, check=True).stdout
        self.assertIn(self.payload.strip(), re.sub(r"\s+", " ", extracted))
        second = {**checked, "id": "papal.test.same-container-different-segment"}
        second_manifest = {**self.manifest, "documents": [{**self.doc, "id": second["id"]}]}
        other = papal.render_documents(second_manifest, [second], self.root / "other-output", True)
        other_pdf = self.root / "other-output" / other["documents"][0]["pdf"]
        identity = lambda data: re.search(rb"/ID\s*\[\s*<([a-fA-F0-9]+)>", data).group(1)
        self.assertNotEqual(identity(pdf.read_bytes()), identity(other_pdf.read_bytes()))

    @unittest.skipUnless(shutil.which("xelatex") and shutil.which("pdfinfo") and shutil.which("pdftotext"), "PDF toolchain unavailable")
    def test_compiled_greek_combining_mark_and_soft_hyphen_keep_logical_text(self):
        self.payload = "Greek πάτερ and ἡμῶν, combining x̶ and Ssm̅um, retained Cyrillic aс, symbol ►, and prae\u00adpositi.\fContinuation after a page delimiter.\n"
        self.payload_path.write_text(self.payload, encoding="utf-8")
        self.doc["sha256"] = hashlib.sha256(self.payload.encode()).hexdigest()
        self.artifact.update(sha256=self.doc["sha256"], byte_size=len(self.payload.encode()))
        self.write_artifact()
        checked = papal.validate_document(self.doc, self.root)
        receipt = papal.render_documents(self.manifest, [checked], self.root / "unicode-output", True)
        self.assertEqual(receipt["errors"], [])
        self.assertEqual(receipt["documents"][0]["warnings"], [])

    def test_form_feed_is_rendering_whitespace_without_mutating_input(self):
        self.assertEqual(papal.tex_escape("word\fcontinuation"), "word continuation")
        self.assertEqual(papal.tex_escape("word\ncontinuation"), "word\ncontinuation")

    def test_unknown_document_refuses_before_output(self):
        path = self.root / "manifest.json"
        path.write_text(json.dumps(self.manifest), encoding="utf-8")
        with self.assertRaisesRegex(papal.PapalTypesetError, "unknown document"):
            papal.read_manifest(path, self.root, ["no-such-document"])
        with self.assertRaises(papal.PapalTypesetError):
            papal.safe_output(ROOT / "pdf/papal-documents")

    def test_apparatus_only_final_page_cannot_pass_publication_check(self):
        run = subprocess.CompletedProcess([], 0, stdout="Original body.\n1\n\fSource apparatus only.\n2\n\f")
        with patch.object(papal.subprocess, "run", return_value=run):
            with self.assertRaisesRegex(papal.PapalTypesetError, "terminal apparatus"):
                papal.pdf_body_fidelity(self.root / "unused.pdf", {"text": "Original body."}, 2)

    def test_title_only_first_page_cannot_pass_source_edition_check(self):
        run = subprocess.CompletedProcess([], 0, stdout="Title only.\n1\n\fOriginal body. Source note.\n2\n\f")
        with patch.object(papal.subprocess, "run", return_value=run):
            with self.assertRaisesRegex(papal.PapalTypesetError, "typeset title"):
                papal.pdf_body_fidelity(self.root / "unused.pdf", {"text": "Original body."}, 2)

    def test_closing_layout_retry_preserves_complete_source_and_full_fragment(self):
        doc = papal.validate_document(self.doc, self.root)
        folder = self.root / "closing-layout" / papal.output_stem(doc)
        folder.mkdir(parents=True)
        tex = folder / (papal.output_stem(doc) + ".tex")
        original = papal.render_body(doc)
        failure = papal.PapalTypesetError("terminal apparatus creates a page after the complete source body")
        with patch.object(papal, "_compile", side_effect=[failure, {"pages": 1}]) as compile_pdf:
            result = papal._compile_with_layout(tex, self.manifest["revision"], doc)
        self.assertEqual(result["layout"], "closing-source-with-apparatus")
        self.assertEqual(compile_pdf.call_args_list[1].args[2]["text"], self.payload)
        self.assertEqual(tex.with_name(tex.stem + ".body.tex").read_text(), original)
        self.assertIn(r"\begin{samepage}", tex.read_text())


if __name__ == "__main__":
    unittest.main()
