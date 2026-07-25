from __future__ import annotations

import importlib.machinery
import importlib.util
import shutil
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock


ROOT = Path(__file__).resolve().parents[2]
DRIVER_PATH = ROOT / "scripts" / "web-edition"
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
    def convert(self, body: str, metadata: str = CONTRIBUTION) -> str:
        """Convert a synthetic single-section leaf and return its Markdown."""
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            leaf = root / "src" / "test" / "studies" / "subject"
            leaf.mkdir(parents=True)
            (leaf / "generation-metadata.tex").write_text(
                rf"\AIDocumentRevisionTimestamp{{{TIMESTAMP}}}" + "\n" + metadata + "\n",
                encoding="utf-8",
            )
            (leaf / "main.tex").write_text(
                "\\input{common/preamble}\n"
                r"\hypersetup{pdftitle={Subject},pdfsubject={A synthetic leaf}}"
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

    def test_repeated_model_and_qualifiers_suppress_the_model_line(self) -> None:
        markdown = self.convert(
            "Prose.",
            metadata="\n".join([CONTRIBUTION, REPEAT_CONTRIBUTION, OTHER_CONTRIBUTION]),
        )
        self.assertEqual(markdown.count("**Model:**"), 2)
        self.assertEqual(markdown.count("**Agent/runtime:**"), 3)
        self.assertIn(f"**Last revised (UTC):** {TIMESTAMP}", markdown)
        self.assertIn("Test CLI 1.0; review role", markdown)

    def test_rights_colophon_is_appended_when_the_leaf_omits_it(self) -> None:
        markdown = self.convert("Prose.")
        self.assertIn("**Reuse and rights.**", markdown)
        self.assertIn("creativecommons.org/licenses/by/4.0/", markdown)
        self.assertIn("THIRD_PARTY.md", markdown)

    def test_unknown_macro_names_its_file_and_writes_nothing(self) -> None:
        with self.assertRaises(DRIVER.ConversionError) as raised:
            self.convert(r"Prose \dubiousclaim{silently deleted evidence}.")
        message = str(raised.exception)
        self.assertIn(r"unknown macro \dubiousclaim", message)
        self.assertIn("main.tex", message)


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
