from __future__ import annotations

import importlib.machinery
import importlib.util
import re
import shutil
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock


ROOT = Path(__file__).resolve().parents[2]
DRIVER_PATH = ROOT / "tools" / "web-edition"
LOADER = importlib.machinery.SourceFileLoader("triptych_web_edition", str(DRIVER_PATH))
SPEC = importlib.util.spec_from_loader(LOADER.name, LOADER)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError(f"cannot load {DRIVER_PATH}")
DRIVER = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = DRIVER
SPEC.loader.exec_module(DRIVER)

HAS_PANDOC = shutil.which("pandoc") is not None
TIMESTAMP = "2026-07-25T12:00:00Z"
CONTRIBUTION = (
    r"\AIModelContribution{test-model}{effort=high}{Test CLI 1.0; API workspace}"
)
REPEAT_CONTRIBUTION = (
    r"\AIModelContribution{test-model}{effort=high}{Test CLI 1.0; review role}"
)
OTHER_CONTRIBUTION = (
    r"\AIModelContribution{other-model}{effort=low}{Test CLI 1.1; API workspace}"
)


@unittest.skipUnless(HAS_PANDOC, "pandoc is not installed")
class WebEditionConversionTests(unittest.TestCase):
    def convert(
        self,
        body: str,
        metadata: str = CONTRIBUTION,
        *,
        nested_preamble: str | None = None,
        componentized: bool = False,
    ) -> str:
        """Convert a synthetic single-section leaf and return its Markdown."""
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            leaf = root / "src" / "test" / "studies" / "subject"
            leaf.mkdir(parents=True)
            nested_input = ""
            if nested_preamble is not None:
                (leaf / "format.tex").write_text(nested_preamble, encoding="utf-8")
                nested_input = "\\input{studies/subject/format}\n"
            if componentized:
                (leaf / "proper-components.toml").write_text(
                    'schema = 1\nrecord_type = "proper-components"\n',
                    encoding="utf-8",
                )
            (leaf / "generation-metadata.tex").write_text(
                rf"\AIDocumentRevisionTimestamp{{{TIMESTAMP}}}" + "\n" + metadata + "\n",
                encoding="utf-8",
            )
            (leaf / "main.tex").write_text(
                "\\input{common/preamble}\n"
                + nested_input
                + r"\hypersetup{pdftitle={Subject},pdfsubject={A synthetic leaf}}"
                "\n\\begin{document}\n"
                "\\begin{titlepage}\nDropped title page\n\\end{titlepage}\n"
                "\\section{Body}\n" + body + "\n"
                r"\input{studies/subject/generation-metadata}"
                "\n\\end{document}\n",
                encoding="utf-8",
            )
            with mock.patch.object(DRIVER, "SRC", root / "src"), mock.patch.object(
                DRIVER, "OUT", root / "build" / "web"
            ):
                destination = DRIVER.convert("test", "studies/subject")
            return destination.read_text(encoding="utf-8")

    def test_endnote_survives_as_a_footnote_with_its_body(self) -> None:
        markdown = self.convert(
            r"Claim.\endnote{Cited at \work{De Anima} 3, "
            r"\sourceurl{https://example.invalid/scan}{page image}.}"
        )
        self.assertIn("[^1]", markdown)
        self.assertIn("Cited at *De Anima* 3", markdown)
        self.assertIn("https://example.invalid/scan", markdown)

    def test_document_title_is_the_only_first_level_heading(self) -> None:
        markdown = self.convert("Prose.")
        self.assertTrue(markdown.startswith("# Subject\n"))
        self.assertIn("*A synthetic leaf*", markdown)
        self.assertIn("## Body", markdown)
        self.assertNotIn("Dropped title page", markdown)

    def test_print_only_branch_keeps_its_web_alternative(self) -> None:
        markdown = self.convert(
            "\\ifdefined\\TriptychPrintEdition\n"
            "Print-only wording.\n"
            "\\else\n"
            "Web alternative.\n"
            "\\fi\n"
        )
        self.assertIn("Web alternative.", markdown)
        self.assertNotIn("Print-only wording.", markdown)

    def test_componentized_web_selects_canonical_branch_in_nested_input(self) -> None:
        markdown = self.convert(
            r"\editionnote",
            nested_preamble=(
                "\\ifdefined\\TriptychSynthesisEdition\n"
                "\\newcommand{\\editionnote}{Synthesis companion.}\n"
                "\\else\n"
                "\\newcommand{\\editionnote}{Canonical research edition.}\n"
                "\\fi\n"
            ),
            componentized=True,
        )
        self.assertIn("Canonical research edition.", markdown)
        self.assertNotIn("Synthesis companion.", markdown)

    def test_named_table_environment_keeps_its_header_and_every_row(self) -> None:
        markdown = self.convert(
            "\\begin{lifetimeline}\n"
            r"\lifeevent{c. 155}{Born at Carthage}{Jerome}{Disputed}"
            "\n"
            r"\lifeevent{197}{Apologeticum}{Internal}{Secure}"
            "\n\\end{lifetimeline}\n"
        )
        for cell in ("Date", "Event", "Basis", "Status", "Born at Carthage",
                     "Apologeticum", "Jerome", "Disputed", "Secure"):
            self.assertIn(cell, markdown)

    def test_quoted_source_block_keeps_its_title(self) -> None:
        markdown = self.convert(
            "\\begin{massbox}{Operative text}\nThe quoted wording.\n\\end{massbox}\n"
        )
        self.assertIn("> **Operative text**", markdown)
        self.assertIn("> The quoted wording.", markdown)

    def test_model_and_qualifiers_remain_audit_only(self) -> None:
        markdown = self.convert(
            "Prose.",
            metadata="\n".join([CONTRIBUTION, REPEAT_CONTRIBUTION, OTHER_CONTRIBUTION]),
        )
        self.assertNotIn("**Model:**", markdown)
        self.assertNotIn("effort=", markdown)
        self.assertNotIn("**Agent/runtime:**", markdown)
        self.assertIn(f"**Last revised (UTC):** {TIMESTAMP}", markdown)
        self.assertNotIn("Test CLI 1.0; review role", markdown)

    def test_rights_colophon_is_appended_when_the_leaf_omits_it(self) -> None:
        markdown = self.convert("Prose.")
        self.assertIn("**Reuse and rights.**", markdown)
        self.assertIn("creativecommons.org/licenses/by/4.0/", markdown)
        self.assertIn("THIRD_PARTY.md", markdown)

    def test_table_becomes_a_pipe_table_the_site_renderer_can_read(self) -> None:
        markdown = self.convert(
            "\\begin{evidencekey}\n"
            r"\evidenceclass{A}{Contemporary record}"
            "\n\\end{evidencekey}\n"
        )
        self.assertRegex(markdown, r"(?m)^\| \*\*Class\*\* +\| \*\*Meaning\*\* +\|$")
        self.assertRegex(markdown, r"(?m)^\|(?:[ :]*-{2,}[ :]*\|)+\s*$")
        self.assertRegex(markdown, r"(?m)^\| A +\| Contemporary record +\|$")

    def test_labelled_heading_keeps_the_anchor_its_references_use(self) -> None:
        markdown = self.convert(
            "\\subsection{Method}\\label{sec:method}\n"
            r"See section~\ref{sec:method} and \ref{sec:missing}."
            "\n"
        )
        self.assertIn("### Method {#sec:method}", markdown)
        self.assertIn("[1.1](#sec:method)", markdown)
        # A reference no heading anchors keeps its text and loses its link.
        self.assertNotIn("(#sec:missing)", markdown)

    def test_starred_heading_drops_pandoc_only_attributes(self) -> None:
        markdown = self.convert("\\subsection*{Pastoral reply}\nProse.\n")
        self.assertIn("### Pastoral reply\n", markdown)
        self.assertNotIn(".unnumbered", markdown)

    def test_starred_heading_keeps_an_explicit_label(self) -> None:
        markdown = self.convert(
            "\\subsection*{Pastoral reply}\\label{sec:reply}\n"
            "See section~\\ref{sec:reply}.\n"
        )
        self.assertIn("### Pastoral reply {#sec:reply}\n", markdown)
        self.assertIn("(#sec:reply)", markdown)
        self.assertNotIn(".unnumbered", markdown)

    def test_description_labels_and_spacing_macros_survive(self) -> None:
        markdown = self.convert(
            "\\begin{description}[style=nextline,leftmargin=1.5em]\n"
            r"\item[7 November 1831] Born at Corps."
            "\n\\end{description}\n"
            r"Need\enspace\properrefs{Int.}"
            "\n"
        )
        self.assertIn("7 November 1831", markdown)
        self.assertIn("Born at Corps.", markdown)
        self.assertNotIn(":::", markdown)
        self.assertIn("Need (*Int.*)", markdown)

    def test_unknown_macro_names_its_file_and_writes_nothing(self) -> None:
        with self.assertRaises(DRIVER.ConversionError) as raised:
            self.convert(r"Prose \dubiousclaim{silently deleted evidence}.")
        message = str(raised.exception)
        self.assertIn(r"unknown macro \dubiousclaim", message)
        self.assertIn("main.tex", message)

    def test_long_form_heading_and_anchor_fidelity(self) -> None:
        count = 120
        body = "\n".join(
            rf"\subsection{{Part {number}}}\label{{sec:part-{number}}}"
            rf"See \ref{{sec:part-{number}}}."
            for number in range(1, count + 1)
        )
        markdown = self.convert(body)
        self.assertEqual(
            len(re.findall(r"^### Part \d+ \{#sec:part-\d+\}$", markdown, re.MULTILINE)),
            count,
        )
        self.assertEqual(
            len(re.findall(r"\]\(#sec:part-\d+\)", markdown)),
            count,
        )


class WebEditionAuditTests(unittest.TestCase):
    """The output audit is the last guard against silent scholarship loss."""

    def test_dropped_endnote_is_reported(self) -> None:
        failures = DRIVER.audit_output(
            r"Claim.\endnote{Lost body.}", self.minimal_markdown()
        )
        self.assertTrue(any("became 0 footnotes" in failure for failure in failures))

    def test_dropped_source_url_is_reported(self) -> None:
        failures = DRIVER.audit_output(
            r"\sourceurl{https://example.invalid/a}{text}", self.minimal_markdown()
        )
        self.assertIn(
            r"\sourceurl payload dropped: https://example.invalid/a", failures
        )

    def test_missing_colophon_and_timestamp_are_reported(self) -> None:
        failures = DRIVER.audit_output("Prose.", "# Subject\n\nProse.\n")
        self.assertIn("rights colophon missing from output", failures)
        self.assertIn("revision timestamp missing from output", failures)

    def test_residual_latex_is_reported(self) -> None:
        failures = DRIVER.audit_output("Prose.", self.minimal_markdown() + r"\rubric")
        self.assertTrue(
            any(failure.startswith("raw LaTeX left in output") for failure in failures)
        )

    def test_dropped_table_is_reported(self) -> None:
        failures = DRIVER.audit_output("Prose.", self.minimal_markdown(), tables=2)
        self.assertIn("2 table environments became 0 tables", failures)

    def test_split_table_is_not_a_loss(self) -> None:
        markdown = self.minimal_markdown() + "\n| a | b |\n|:--|:--|\n| 1 | 2 |\n"
        self.assertEqual(DRIVER.audit_output("Prose.", markdown, tables=1), [])

    def test_unconverted_block_is_reported(self) -> None:
        failures = DRIVER.audit_output(
            "Prose.", self.minimal_markdown() + "\n::: dossierframe\nText\n:::\n"
        )
        self.assertIn("2 unconverted fenced-div delimiter(s) left in output", failures)

    def test_blockquoted_fenced_div_is_reported(self) -> None:
        failures = DRIVER.audit_output(
            "Prose.",
            self.minimal_markdown()
            + "\n> ::: flushright\n> Attribution\n> :::\n",
        )
        self.assertIn("2 unconverted fenced-div delimiter(s) left in output", failures)

    def test_heading_shortfall_is_reported(self) -> None:
        failures = DRIVER.audit_output(
            r"\section{One}\subsection{Two}",
            self.minimal_markdown() + "\n## One\n",
        )
        self.assertIn("1 level-3 source heading(s) became 0 heading(s)", failures)

    def test_duplicate_heading_anchor_is_reported(self) -> None:
        failures = DRIVER.audit_output(
            "Prose.",
            self.minimal_markdown()
            + "\n## One {#sec:repeat}\n\n## Two {#sec:repeat}\n",
        )
        self.assertIn("duplicate heading anchor(s): sec:repeat", failures)

    def test_missing_internal_anchor_target_is_reported(self) -> None:
        failures = DRIVER.audit_output(
            "Prose.",
            self.minimal_markdown() + "\n[Missing](#sec:missing)\n",
        )
        self.assertIn("missing internal anchor target(s): sec:missing", failures)

    def test_named_table_wrapper_counts_as_a_table(self) -> None:
        definitions = (
            r"\newenvironment{historytimeline}{%"
            "\n  \\begingroup\\scriptsize\n  \\begin{longtable}{ll}}{\\end{longtable}}"
        )
        self.assertEqual(
            DRIVER.table_count(r"\begin{historytimeline}\end{historytimeline}", definitions),
            1,
        )

    def test_faithful_output_passes(self) -> None:
        self.assertEqual(DRIVER.audit_output("Prose.", self.minimal_markdown()), [])

    def minimal_markdown(self) -> str:
        return (
            "# Subject\n\nProse.\n\n"
            f"**Last revised (UTC):** {TIMESTAMP}\n\n"
            "**Reuse and rights.** Project-created content is licensed under CC BY 4.0.\n"
        )


if __name__ == "__main__":
    unittest.main()
