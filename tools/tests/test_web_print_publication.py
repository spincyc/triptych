"""Exact source selection and legal DOM bindings for browser-print products."""
from __future__ import annotations

from pathlib import Path
import hashlib
import re
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))
import _web_print_publication as printing
import _web_print_semantics as semantics

RIGHTS = r"\newcommand{\TriptychRightsNotice}{\begin{minipage}{\linewidth}\textbf{Reuse and rights.} Exact source notice.\end{minipage}}"
RIGHTS_HTML = "<p><strong>Reuse and rights.</strong> Exact source notice.</p>"


class PublicationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.library = printing.load_library(ROOT)

    def ledger(self, body):
        return semantics.expected_units({
            "head": RIGHTS, "body": body, "sources": {},
            "selection": {"entrypoint": "src/gpt/fixture/main.tex", "role": "main"},
            "chunks": [{"path": "src/gpt/fixture/main.tex", "occurrence": 1,
                        "selected_line": 1, "text": body}],
        }, self.library)

    def bind(self, source, fragment):
        ledger = self.ledger(source)
        fragment += RIGHTS_HTML
        proof = semantics.check_units(ledger, fragment)
        self.assertEqual(proof["status"], "pass", proof["failures"])
        bound, ids = printing.bind_print_units(ledger, fragment, proof)
        self.assertEqual(ids, printing.print_unit_ids(bound))
        provenance = printing.unit_expectations(ledger, ids)
        self.assertEqual([unit["id"] for unit in provenance], ids)
        self.assertTrue(all(unit["source"] and unit["occurrence"] for unit in provenance))
        self.assertEqual(len(ids), len(ledger["units"]))
        self.assertEqual(re.sub(r'<span data-print-unit="[^"]+"></span>', "", bound), fragment)
        return bound, ids

    def test_short_prayer_and_table_cells_keep_independent_ids(self):
        source = r"Amen.\par\begin{tabular}{ll}Cue & Reply\\Yes & Deo gratias.\\\end{tabular}"
        fragment = "<p>Amen.</p><table><tr><td>Cue</td><td>Reply</td></tr><tr><td>Yes</td><td>Deo gratias.</td></tr></table>"
        bound, ids = self.bind(source, fragment)
        self.assertEqual(len(ids), 6)
        self.assertNotRegex(bound, r"<(?:table|tr)[^>]*>\s*<span")

    def test_shared_br_host_binds_each_actual_run_in_order(self):
        bound, ids = self.bind(r"First.\newline Second.", "<p>First.<br>Second.</p>")
        self.assertIn(f'<span data-print-unit="{ids[0]}"></span>First.<br><span data-print-unit="{ids[1]}"></span>Second.', bound)

    def test_nested_list_tail_marker_follows_child(self):
        source = r"\begin{itemize}\item\begin{itemize}\item Child.\end{itemize}Tail.\end{itemize}"
        bound, ids = self.bind(source, "<ul><li><ul><li>Child.</li></ul>Tail.</li></ul>")
        self.assertLess(bound.index(ids[0]), bound.index("Child."))
        self.assertLess(bound.index("Child."), bound.index(ids[1]))

    def test_entity_bytes_are_not_rewritten(self):
        bound, _ = self.bind("A & B.", "<p>A &amp; B.</p>")
        self.assertIn("A &amp; B.", bound)

    def test_unowned_preexisting_marker_refuses(self):
        ledger = self.ledger("Amen.")
        fragment = '<p data-print-unit="invented">Amen.</p>' + RIGHTS_HTML
        proof = semantics.check_units(ledger, fragment)
        with self.assertRaisesRegex(printing.Refused, "canonical container"):
            printing.bind_print_units(ledger, fragment, proof)

    def test_incomplete_proof_cannot_bind(self):
        ledger = self.ledger("Amen.")
        with self.assertRaisesRegex(printing.Refused, "complete"):
            printing.bind_print_units(ledger, RIGHTS_HTML, {"status": "pass", "complete": False})

    def test_source_bound_container_is_added_without_changing_text(self):
        ledger = self.ledger(r"\begin{minipage}{\linewidth}Amen.\end{minipage}")
        fragment = '<div data-semantic-minipage="minipage-1"><p>Amen.</p></div>' + RIGHTS_HTML
        proof = semantics.check_units(ledger, fragment)
        self.assertEqual(proof["status"], "pass", proof["failures"])
        bound, ids = printing.bind_print_units(ledger, fragment, proof)
        self.assertEqual(ids[0], "minipage-1")
        self.assertIn('data-print-unit="minipage-1"', bound)
        self.assertEqual(len(ids), len(ledger["units"]) + 1)

    def test_balanced_selected_conditional_never_substitutes_research(self):
        source = r"\ifdefined\TriptychSynthesisEdition Concise \ifdefined\TriptychPrintEdition Print\else Browser\fi\else Research\fi"
        selected = printing.select_branches(source, "synthesis", self.library)
        self.assertIn("Concise", selected)
        self.assertIn("Browser", selected)
        self.assertNotIn("Research", selected)
        with self.assertRaises(printing.Refused):
            printing.select_branches(r"\ifdefined\UnknownFlag Amen.\fi", "main", self.library)

    def test_pdf_compression_guard_projects_only_its_literal_layout_setting(self):
        for level in (0, 1, 9):
            source = "Before.\n" + r"\ifdefined\pdfcompresslevel" + "\n" + \
                r"\pdfcompresslevel=" + str(level) + " % layout only\n" + r"\fi" + "\nAfter."
            self.assertEqual(printing.select_branches(source, "main", self.library, allow_pdf_compression=True), "Before.\n\nAfter.")
        for body in (r"\pdfcompresslevel=10", r"\pdfcompresslevel=-1", r"\pdfcompresslevel=\ChosenLevel",
                     r"\pdfcompresslevel=1 Visible content.", r"\pdfcompresslevel=1\else Other content.",
                     r"\pdfcompresslevel=1\else", r"\ifdefined\TriptychPrintEdition\pdfcompresslevel=1\fi",
                     r"\pdfcompresslevel=1\input{hidden}"):
            with self.subTest(body=body), self.assertRaisesRegex(printing.Refused, "PDF compression"):
                printing.select_branches(r"\ifdefined\pdfcompresslevel " + body + r"\fi", "main", self.library, allow_pdf_compression=True)

    def test_pdf_compression_guard_is_not_a_general_edition_flag(self):
        with self.assertRaisesRegex(printing.Refused, "unsupported conditional flag"):
            printing.select_branches(r"\ifdefined\pdfcompresslevel\pdfcompresslevel=1\fi", "main", self.library)
        with self.assertRaisesRegex(printing.Refused, "unsupported conditional flag"):
            printing.select_branches(r"\ifdefined\UnknownFlag Hidden rights.\fi", "main", self.library, allow_pdf_compression=True)

    def test_current_preamble_compression_remains_hashed_in_selected_source(self):
        from _print_document import publication_recipe
        recipe = publication_recipe("gpt", "articles/faith/catholic-doctrinal-authority", root=ROOT)
        selected = printing.selected_source(ROOT, recipe, self.library)
        source = ROOT / "src/common/preamble.tex"
        event = next(row for row in selected["selection"]["ordered_inputs"] if row["path"] == "src/common/preamble.tex")
        self.assertEqual(event["sha256"], hashlib.sha256(source.read_text().encode()).hexdigest())
        projected = printing.select_branches(source.read_text(), recipe["edition"], self.library, allow_pdf_compression=True)
        self.assertEqual(event["selected_sha256"], hashlib.sha256(projected.encode()).hexdigest())
        self.assertNotIn(r"\pdfcompresslevel", selected["source"])
        self.assertIn(r"\pdfcompresslevel=1", source.read_text())

    def test_source_walk_keeps_document_guards_and_unknown_preamble_guards_closed(self):
        from _print_document import publication_recipe
        recipe = publication_recipe("gpt", "articles/faith/catholic-doctrinal-authority", root=ROOT)
        read = Path.read_text
        for target, inserted in (
            (ROOT / recipe["entrypoint"], r"\def\pdfcompresslevel{Visible}\ifdefined\pdfcompresslevel\pdfcompresslevel=1\fi"),
            (ROOT / "src/common/preamble.tex", r"\ifdefined\UnknownFlag\newcommand{\HiddenRights}{Hidden notice.}\fi"),
        ):
            def changed(path, *args, **kwargs):
                return (inserted if path == target else "") + read(path, *args, **kwargs)
            with self.subTest(target=target), patch.object(Path, "read_text", changed):
                with self.assertRaisesRegex(printing.Refused, "unsupported conditional flag"):
                    printing.selected_source(ROOT, recipe, self.library)

    def test_scoped_heading_alias_does_not_escape_its_group(self):
        body = r"\begingroup\let\section\subsection\section{Inner}\endgroup\section{Outer}"
        selected = printing.project_heading_aliases({"head": "", "body": body}, self.library)
        self.assertIn(r"\subsection{Inner}", selected["body"])
        self.assertTrue(selected["body"].endswith(r"\section{Outer}"))
        self.assertEqual(selected["canonical_body"], body)

    def test_executed_reference_projection_preserves_custom_links(self):
        body = r"Appendix~\ref{app:record}; \hyperref[app:record]{custom title}."
        ledger = {"references": [{"command": "ref", "target": "app:record", "display": "A"}]}
        projected = printing.project_reference_displays({"head": "", "body": body}, ledger, self.library)
        self.assertIn(r"\hyperref[app:record]{A}", projected["body"])
        self.assertIn(r"\hyperref[app:record]{custom title}", projected["body"])

    def test_parts_are_balanced_and_bounded(self):
        fragment = "<p>First.</p><table><tr><td>Amen.</td></tr></table><p>Last.</p>"
        parts = printing.split_parts(fragment, limit=55)
        self.assertEqual("".join(part["html"] for part in parts), fragment)
        self.assertTrue(all(part["bytes"] < 55 for part in parts))
        with self.assertRaises(printing.PartError):
            printing.split_parts("<p>" + "x" * 100 + "</p>", limit=55)

    def test_actual_spanned_chronology_preserves_typed_source_column_widths(self):
        result = printing.render_publication(
            ROOT, "claude", "liturgy/roman-rite/1962/propers/temporal/48-eighth-after-pentecost")
        fragment = "".join(part["html"] for part in result["parts"])
        self.assertEqual(result["coverage_result"]["status"], "pass")
        self.assertTrue(result["coverage_result"]["complete"])
        for width in (14, 18, 35, 16):
            self.assertIn(f'class="print-column-width-{width}"', fragment)
        self.assertIn('colspan="4"', fragment)
        self.assertNotIn('style="width:', fragment)

    def test_actual_calendar_preserves_typed_source_table_widths(self):
        result = printing.render_publication(
            ROOT, "claude", "liturgy/roman-rite/1962/reference/liturgical-calendar")
        fragment = "".join(part["html"] for part in result["parts"])
        self.assertEqual(result["coverage_result"]["status"], "pass")
        self.assertTrue(result["coverage_result"]["complete"])
        for width in (70, 74, 86, 94):
            self.assertIn(f'class="print-table-width-{width}"', fragment)
        self.assertIn('colspan=', fragment)
        self.assertNotIn('style="width:', fragment)

    def test_actual_virtues_group_labels_keep_five_column_spans(self):
        result = printing.render_publication(ROOT, "gpt", "theology/virtues")
        fragment = "".join(part["html"] for part in result["parts"])
        self.assertTrue(result["coverage_result"]["complete"])
        labels = re.findall(r'<td\b[^>]*colspan="5"[^>]*>(.*?)</td>', fragment, re.S)
        self.assertEqual(len(labels), 7)
        self.assertTrue(all('<strong>' in label for label in labels))
        self.assertIn('Theological virtues', labels[0])
        self.assertIn('Remaining intellectual virtues', labels[-1])

    def test_actual_print_only_source_preserves_column_28(self):
        result = printing.render_publication(
            ROOT, "gpt", "articles/canon-law/clerical-celibacy-chastity-and-continence")
        fragment = "".join(part["html"] for part in result["parts"])
        self.assertTrue(result["coverage_result"]["complete"])
        self.assertIn('class="print-column-width-28"', fragment)

    def test_both_held_outputs_refuse_before_conversion(self):
        leaf = "liturgy/roman-rite/1962/propers/temporal/54-fourteenth-after-pentecost"
        with patch.object(printing, "require_print_toolchain", return_value={}):
            for output in (leaf, leaf + "-synthesis"):
                with self.subTest(output=output), self.assertRaisesRegex(printing.Refused, "held"):
                    printing.convert_output(ROOT, "claude", output, ROOT / ".scratch/web-print-held-test")

    def test_same_version_without_exact_pandoc_bytes_is_not_accepted(self):
        with patch.object(printing.shutil, "which", return_value=sys.executable):
            with self.assertRaisesRegex(printing.Refused, "verified official Pandoc binary"):
                printing.require_print_toolchain()

    def test_selected_entrypoint_cannot_escape_provider(self):
        with self.assertRaisesRegex(self.library.ConversionError, "escapes its provider"):
            self.library.convert("gpt", "fixture", selected={
                "edition": "main", "entrypoint": ROOT / "src/claude/fixture/main.tex",
            })

    def test_raw_span_target_preserved_only_for_selected_conversion(self):
        markdown = '[C](#app:table)\n\n<span id="app:table" data-label="app:table"></span>'
        targets = self.library.selected_markdown_anchors(markdown)
        self.assertEqual(targets, ["app:table"])
        self.assertIn("[C](#app:table)", self.library.resolve_anchors(markdown, targets))
        self.assertNotIn("[C](#app:table)", self.library.resolve_anchors(markdown))
        printing.validate_internal_targets(self.library.render_markdown(markdown, ROOT))

    def test_internal_target_absence_or_ambiguity_refuses(self):
        for fragment in ('<p><a href="#missing">A</a></p>',
                         '<span id="a"></span><span id="a"></span><p><a href="#a">A</a></p>'):
            with self.subTest(fragment=fragment), self.assertRaisesRegex(printing.Refused, "concrete target"):
                printing.validate_internal_targets(fragment)

    def test_compiler_requires_plaintext_lock_even_when_binary_is_available(self):
        scratch = ROOT / ".scratch/web-print-lock-tests"
        scratch.mkdir(parents=True, exist_ok=True)
        with tempfile.TemporaryDirectory(dir=scratch) as name:
            root = Path(name)
            with self.assertRaisesRegex(printing.Refused, "plaintext toolchain lock"):
                printing.require_print_toolchain(root)
            lock = root / "src/common/browser-print-toolchain.toml"
            lock.parent.mkdir(parents=True)
            lock.write_text('schema_version = true\nrecord_type = "browser-print-toolchain"\n[pandoc]\n')
            with self.assertRaisesRegex(printing.Refused, "unsupported"):
                printing.require_print_toolchain(root)


if __name__ == "__main__":
    unittest.main()
