"""Conditional constructs in web readers, and the reader marks the site expands.

guidance/web-editions.md "Conditional constructs" owns the decisions; the
curriculum and figure adapters have their own test modules.
"""
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
sys.path.insert(0, str(ROOT / "scripts"))
LOADER = importlib.machinery.SourceFileLoader("triptych_web_edition_constructs", str(ROOT / "tools/web-edition"))
SPEC = importlib.util.spec_from_loader(LOADER.name, LOADER)
DRIVER = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = DRIVER
SPEC.loader.exec_module(DRIVER)

import _web_reader_markup as markup  # noqa: E402

HAS_PANDOC = shutil.which("pandoc") is not None
METADATA = (r"\AIDocumentRevisionTimestamp{2026-11-04T12:00:00Z}" "\n"
            r"\AIModelContribution{Example Model 9}{effort=high}{Test CLI; API workspace}" "\n")


def site_renderer_available() -> bool:
    try:
        from _markdown_render import require_locked_markdown_dependency
        require_locked_markdown_dependency(ROOT)
    except Exception:
        return False
    return True


class ConstructTests(unittest.TestCase):
    def test_landscape_and_minipage_divs_become_reader_marks_as_blocks(self):
        markdown = ("::: landscape\n# Wide\n:::\n\n> ::: minipage\n> **Latin**\n> :::\n>\n"
                    "> ::: minipage\n> English.\n> :::\n")
        projected = DRIVER.project_construct_divs(markdown)
        self.assertNotIn(":::", projected)
        self.assertIn("<!-- triptych:wide -->\n\n# Wide\n\n<!-- /triptych:wide -->", projected)
        self.assertIn("> <!-- triptych:column -->\n>\n> **Latin**\n>\n> <!-- /triptych:column -->",
                      projected)

    def test_a_box_inside_a_box_is_content_not_a_nested_column(self):
        markdown = ("::: minipage\n<figure></figure>\n\n:::: minipage\n**Drawing 1.** Caption.\n::::\n:::\n")
        projected = DRIVER.project_construct_divs(markdown)
        self.assertEqual(projected.count("<!-- triptych:column -->"), 1)
        self.assertEqual(projected.count("<!-- /triptych:column -->"), 1)
        self.assertNotIn(":::", projected)
        page = markup.expand("<!-- triptych:column -->\n<figure></figure>\n<p>Caption.</p>\n"
                             "<!-- /triptych:column -->\n", "web/gpt/x.html")
        self.assertNotIn("web-column", page)

    def test_each_call_of_a_counter_stepping_macro_gets_its_number(self):
        preamble = ("\\newcounter{sketchfigure}\n\\newcommand{\\sketchcaption}[1]{%\n"
                    "  \\refstepcounter{sketchfigure}\\textbf{Drawing \\thesketchfigure.} #1}\n")
        body = "A.\\sketchcaption{One} B.\\sketchcaption{Two} % \\sketchcaption{commented}\n"
        numbered = DRIVER.number_counter_macros(body, preamble)
        self.assertEqual(numbered.count("\\def\\thesketchfigure{1}\\sketchcaption{One}"), 1)
        self.assertEqual(numbered.count("\\def\\thesketchfigure{2}\\sketchcaption{Two}"), 1)
        self.assertNotIn("{3}", numbered)
        self.assertEqual(DRIVER.number_counter_macros(body, "\\newcommand{\\x}{y}"), body)
        with self.assertRaisesRegex(DRIVER.ConversionError, "not modelled"):
            DRIVER.number_counter_macros("\\setcounter{sketchfigure}{4}" + body, preamble)

    def test_any_other_div_is_left_for_the_audit_to_refuse(self):
        self.assertIn("::: center", DRIVER.project_construct_divs("::: center\nText.\n:::\n"))

    def test_a_scoped_heading_alias_demotes_only_its_group(self):
        body = ("\\section{Before}\n\\begingroup\n\\let\\section\\subsection\n"
                "\\section{Inside}\n{\\section{Nested}}\n\\endgroup\n\\section{After}\n")
        projected = DRIVER.project_heading_aliases(body)
        self.assertNotIn("\\let", projected)
        self.assertIn("\\section{Before}", projected)
        self.assertIn("\\subsection{Inside}", projected)
        self.assertIn("\\subsection{Nested}", projected)
        self.assertIn("\\section{After}", projected)
        self.assertEqual(DRIVER.project_heading_aliases("\\section{Plain}\n"), "\\section{Plain}\n")

    def test_multicols_is_one_column_and_publishes_no_column_count(self):
        shim = (ROOT / "scripts/web-shim.tex").read_text(encoding="utf-8")
        self.assertIn("\\renewenvironment{multicols}[1]{}{}", shim)
        self.assertIn("\\newenvironment{multicols*}[1]{}{}", shim)


@unittest.skipUnless(HAS_PANDOC, "pandoc is not installed")
@unittest.skipUnless(site_renderer_available(), "the pinned site Markdown renderer is required")
class ConversionTests(unittest.TestCase):
    def convert(self, body: str) -> str:
        with tempfile.TemporaryDirectory() as temporary:
            src = Path(temporary) / "src"
            leaf = src / "test/studies/subject"
            leaf.mkdir(parents=True)
            (leaf / "generation-metadata.tex").write_text(METADATA)
            (leaf / "main.tex").write_text(
                "\\input{common/preamble}\n\\hypersetup{pdftitle={Subject}}\n\\begin{document}\n"
                "\\section{Body}\n" + body + "\n\\input{studies/subject/generation-metadata}\n"
                "\\end{document}\n")
            with mock.patch.object(DRIVER, "SRC", src):
                return DRIVER.convert_markdown("test", "studies/subject")

    def test_paired_minipages_and_landscape_tables_reach_the_reader(self):
        markdown = self.convert(
            "\\begin{quote}\n\\begin{minipage}[t]{0.48\\linewidth}\\textbf{Latin}\\par Ave.\\end{minipage}\\hfill\n"
            "\\begin{minipage}[t]{0.48\\linewidth}\\textbf{English}\\par Hail.\\end{minipage}\n\\end{quote}\n"
            "\\begin{landscape}\n\\begin{tabular}{ll}\nA & B\\\\\nC & D\\\\\n\\end{tabular}\n\\end{landscape}\n")
        self.assertEqual(markdown.count("<!-- triptych:column -->"), 2)
        self.assertEqual(markdown.count("<!-- triptych:wide -->"), 1)
        from _markdown_render import render_markdown
        page = markup.expand(render_markdown(markdown, ROOT), "web/test/studies/subject.html")
        self.assertIn('<div class="web-columns"><div class="web-column">', page)
        self.assertIn('<table class="web-wide-table"', page)
        self.assertNotIn("triptych:", page)

    def test_a_contributed_model_name_or_model_field_is_refused_but_a_model_answer_is_not(self):
        markdown = self.convert("\\textbf{Answer / model:} \\textit{Ave.} Model: \\textit{Vale.}")
        self.assertIn("Answer / model:", markdown)
        with self.assertRaisesRegex(DRIVER.ConversionError, "model metadata"):
            self.convert("Written by Example Model 9.")
        with self.assertRaisesRegex(DRIVER.ConversionError, "model metadata"):
            self.convert("\\textbf{Model:} anything")

    def test_a_table_inside_a_quotation_counts_as_written(self):
        markdown = self.convert("\\begin{quote}\n\\begin{tabular}{ll}\nA & B\\\\\nC & D\\\\\n"
                                "\\end{tabular}\n\\end{quote}\n")
        self.assertIn("> |", markdown)


class ReaderMarkupTests(unittest.TestCase):
    def test_an_answer_key_is_collapsed_under_its_summary(self):
        page = ("<p>Before.</p>\n<!-- triptych:answer-key Solution M01-A &amp; notes -->\n"
                "<h4>Solution</h4>\n<p>Amo.</p>\n<!-- /triptych:answer-key -->\n")
        expanded = markup.expand(page, "web/gpt/x.html")
        self.assertIn('<details class="web-answer-key"><summary>Solution M01-A &amp; notes</summary>',
                      expanded)
        self.assertIn("<p>Amo.</p>\n</details>", expanded)

    def test_a_lone_column_is_plain_content(self):
        page = "<!-- triptych:column -->\n<p>Boxed.</p>\n<!-- /triptych:column -->\n"
        self.assertEqual(markup.expand(page, "web/gpt/x.html").strip(), "<p>Boxed.</p>")

    def test_unbalanced_nested_or_unknown_marks_are_refused(self):
        for page in ("<!-- triptych:column -->", "<!-- /triptych:wide -->",
                     "<!-- triptych:wide --><!-- triptych:wide --><!-- /triptych:wide --><!-- /triptych:wide -->",
                     "<!-- triptych:answer-key  --><!-- /triptych:answer-key -->",
                     "<!-- triptych:other -->"):
            with self.subTest(page=page), self.assertRaises(markup.ReaderMarkupError):
                markup.expand(page, "web/gpt/x.html")

    def test_figure_sources_are_relative_to_the_page(self):
        figure = "a" * 64
        page = f'<figure class="web-figure"><img src="web-figures/{figure}.svg" alt="x"></figure>'
        self.assertIn(f'src="../../../web-figures/{figure}.svg"',
                      markup.expand(page, "web/gpt/articles/x.html"))
        self.assertEqual(markup.figure_ids(page), [figure])


if __name__ == "__main__":
    unittest.main()
