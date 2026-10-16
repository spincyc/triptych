from __future__ import annotations

import importlib.machinery
import importlib.util
from pathlib import Path
import shutil
import sys
import tempfile
import unittest
from unittest import mock


ROOT = Path(__file__).resolve().parents[2]
LOADER = importlib.machinery.SourceFileLoader(
    "triptych_web_pageref", str(ROOT / "tools" / "web-edition")
)
SPEC = importlib.util.spec_from_loader(LOADER.name, LOADER)
DRIVER = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = DRIVER
SPEC.loader.exec_module(DRIVER)


class PageReferenceTests(unittest.TestCase):
    def test_comments_escaped_commands_and_print_prefixes(self) -> None:
        source = (
            r"\section{Esther}\label{hist-esther}" "\n"
            r"% p.~\pageref{missing}" "\n"
            r"Literal \\pageref{missing}; 50\% kept. "
            r"Esther, p.~\pageref{hist-esther}; pp. \pageref{hist-esther}; "
            "\\pageref% command comment\n{hist-esther}."
        )
        prepared, references = DRIVER.prepare_page_references(source)
        self.assertEqual([target for _, target in references], ["hist-esther"] * 3)
        self.assertIn(r"% p.~\pageref{missing}", prepared)
        self.assertIn(r"Literal \\pageref{missing}; 50\% kept.", prepared)
        for marker, _ in references:
            self.assertEqual(prepared.count(marker), 1)
        self.assertNotIn("Esther, p.", prepared)
        self.assertNotIn("; pp.", prepared)

    def test_missing_and_duplicate_source_labels_fail(self) -> None:
        for labels, count in (("", 0), (r"\label{x}\label{x}", 2)):
            with self.subTest(count=count), self.assertRaisesRegex(
                DRIVER.ConversionError, f"exactly one source label; found {count}"
            ):
                DRIVER.prepare_page_references(labels + r"p.~\pageref{x}")

    def test_missing_nonheading_and_duplicate_rendered_targets_fail(self) -> None:
        for destination in (
            "No heading.", '<span id="x">Inline target</span>',
            "## First {#x}\n\n## Second {#x}",
        ):
            with self.subTest(destination=destination), self.assertRaisesRegex(
                DRIVER.ConversionError, "one rendered heading target"
            ):
                DRIVER.resolve_page_references(destination + "\n\nMARK", [("MARK", "x")], "# T")

    def test_missing_and_repeated_markers_fail(self) -> None:
        for markers in ("", "MARK MARK"):
            with self.subTest(markers=markers), self.assertRaisesRegex(
                DRIVER.ConversionError, "lost or repeated in conversion"
            ):
                DRIVER.resolve_page_references("## Target {#x}\n\n" + markers, [("MARK", "x")], "# T")

    def test_rendered_link_loss_fails(self) -> None:
        render = DRIVER.render_markdown

        def drop_link(text: str, root: Path) -> str:
            return render(text, root).replace('href="#x"', 'href="#wrong"')

        with mock.patch.object(DRIVER, "render_markdown", side_effect=drop_link):
            with self.assertRaisesRegex(DRIVER.ConversionError, "lost in site rendering"):
                DRIVER.resolve_page_references("## Target {#x}\n\nMARK", [("MARK", "x")], "# T")

    def test_heading_formatting_and_punctuation_are_plain_link_text(self) -> None:
        markdown = (
            "## *Esther* &amp; [Job](https://example.invalid): [text] | &lt;angle&gt; {#x}\n\n"
            "| Source | Reference |\n| --- | --- |\n| Kept | MARK |\n"
        )
        result = DRIVER.resolve_page_references(markdown, [("MARK", "x")], "# T")
        self.assertIn(
            '<a href="#x">Esther &amp; Job: &#91;text&#93; &#124; &lt;angle&gt;</a>', result
        )
        rendered = DRIVER.render_markdown(result, ROOT)
        self.assertIn('<td><a href="#x">Esther &amp; Job: &#91;text&#93; &#124; &lt;angle&gt;</a></td>', rendered)
        self.assertEqual(rendered.count("<td>"), 2)

    def test_literal_markdown_in_a_heading_cannot_become_a_nested_link(self) -> None:
        markdown = "## Code `[click](#wrong) *literal*` {#x}\n\nMARK"
        result = DRIVER.resolve_page_references(markdown, [("MARK", "x")], "# T")
        self.assertIn('Code &#91;click&#93;(#wrong) &#42;literal&#42;</a>', result)
        rendered = DRIVER.render_markdown(result, ROOT)
        self.assertEqual(rendered.count("<a "), 1)
        self.assertNotIn("<em>", rendered)


@unittest.skipUnless(shutil.which("pandoc"), "pandoc is not installed")
class PageReferenceConversionTests(unittest.TestCase):
    def convert(
        self, *, schema: int = 2, orientation: bool = True,
        preamble: str = "", extra_body: str = "", presentation: str = "orientation-v1",
    ) -> str:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            leaf = root / "src" / "test" / "doc"
            leaf.mkdir(parents=True)
            (leaf / "proper-components.toml").write_text(
                f'schema = {schema}\nelement_keys = ["introit"]\n'
                + (f'chronology_presentation = "{presentation}"\n' if orientation else "")
            )
            (leaf / "main.tex").write_text(
                r"\input{common/preamble}" "\n"
                r"\hypersetup{pdftitle={Page references}}" "\n"
                + preamble + "\n"
                + r"\begin{document}" "\n"
                r"\section{Introit}\label{proper-introit}" "\n"
                "Preserved appointed text.\n\n"
                r"Sources: Esther, p.~\pageref{hist-esther}; "
                r"Job, pp.~\pageref{hist-job}. "
                r"See also \pageref{hist-esther}." "\n\n"
                r"\subsection{Esther: a threatened people}\label{hist-esther}" "\n"
                "Esther's source qualification.\n\n"
                r"\subsection{Job: the land of the story}\label{hist-job}" "\n"
                "Job's source qualification.\n\n"
                + extra_body + "\n"
                + r"\AIDocumentRevisionTimestamp{2026-10-13T00:00:00Z}" "\n"
                r"\end{document}" "\n"
            )
            with mock.patch.object(DRIVER, "SRC", root / "src"):
                output = DRIVER.convert("test", "doc", root / "output")
            return output.read_text()

    def test_orientation_conversion_retains_each_reference_and_passage(self) -> None:
        markdown = self.convert()
        self.assertIn('Sources: Esther, <a href="#hist-esther">Esther: a threatened people</a>;', markdown)
        self.assertIn('Job, <a href="#hist-job">Job: the land of the story</a>.', markdown)
        self.assertIn('See also <a href="#hist-esther">Esther: a threatened people</a>.', markdown)
        self.assertIn("Preserved appointed text.", markdown)
        self.assertIn("Esther’s source qualification.", markdown)
        self.assertIn("Job’s source qualification.", markdown)
        self.assertNotIn(DRIVER.WEB_PAGE_REFERENCE_MARK, markdown)
        self.assertNotIn("p.", markdown)
        self.assertIn("hist-esther", DRIVER.rendered_markdown_anchors(markdown))

    def test_orientation_v2_leaves_take_the_same_page_reference_path(self) -> None:
        markdown = self.convert(presentation="orientation-v2")
        self.assertIn('Sources: Esther, <a href="#hist-esther">Esther: a threatened people</a>;', markdown)
        self.assertNotIn(DRIVER.WEB_PAGE_REFERENCE_MARK, markdown)

    def test_legacy_and_nonorientation_schema_two_do_not_enter_new_path(self) -> None:
        for schema, orientation in ((1, True), (2, False)):
            with self.subTest(schema=schema, orientation=orientation):
                with mock.patch.object(DRIVER, "prepare_page_references", side_effect=AssertionError("legacy changed")):
                    markdown = self.convert(schema=schema, orientation=orientation)
                self.assertIn("Sources: Esther, p.", markdown)
                self.assertNotIn('<a href="#hist-esther">', markdown)

    def test_macro_hidden_references_fail_closed(self) -> None:
        for definition, call in (
            (r"\newcommand{\where}[1]{p.~\pageref{#1}}", r"\where{hist-esther}"),
            (r"\newcommand{\where}{p.~\pageref{hist-esther}}", r"\where{}"),
            (r"\let\where\pageref", r"\where{hist-esther}"),
        ):
            for location in ("preamble", "body"):
                with self.subTest(definition=definition, location=location):
                    with self.assertRaisesRegex(DRIVER.ConversionError, "page references in macro definitions are unsupported"):
                        self.convert(
                            preamble=definition if location == "preamble" else "",
                            extra_body=(definition if location == "body" else "") + "\nSee " + call + ".",
                        )

    def test_commented_macro_reference_is_not_refused(self) -> None:
        markdown = self.convert(preamble="% " + r"\newcommand{\where}[1]{p.~\pageref{#1}}")
        self.assertIn('<a href="#hist-esther">', markdown)

    def test_current_orientation_leaf_changes_only_the_five_print_references(self) -> None:
        leaf = "liturgy/roman-rite/1962/propers/temporal/61-twenty-first-after-pentecost"
        with tempfile.TemporaryDirectory() as temporary:
            output = Path(temporary)
            current = DRIVER.convert("gpt", leaf, output / "current").read_text()
            with mock.patch.object(DRIVER, "prepare_page_references", side_effect=lambda body: (body, [])):
                previous = DRIVER.convert("gpt", leaf, output / "previous").read_text()
        before = next(line for line in previous.splitlines() if line.startswith("Sources and fuller qualifications:"))
        after = next(line for line in current.splitlines() if line.startswith("Sources and fuller qualifications:"))
        for target in ("esther", "job", "psalms", "matthew", "ephesians"):
            self.assertEqual(after.count(f'<a href="#hist-{target}">'), 1)
        self.assertNotIn("p.", after)
        self.assertEqual(current, previous.replace(before, after))


if __name__ == "__main__":
    unittest.main()
