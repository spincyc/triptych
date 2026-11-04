from __future__ import annotations

import json
from pathlib import Path
import shutil
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))

import _web_edition_figures as figures  # noqa: E402

PREAMBLE = r"""\documentclass{article}
\usepackage{tikz}
\usetikzlibrary{arrows.meta,positioning}
\usepackage{hyperref}
\tikzset{
  guide node/.style={draw=black, align=center, inner sep=5pt, font=\small},
  guide arrow/.style={-{Stealth[length=2mm]}, thick, draw=black}
}
"""
HEAD = "\\input{common/preamble}\n\\hypersetup{pdftitle={Fixture}}\n"
FLOWCHART = r"""\begin{tikzpicture}[node distance=5mm]
\node[guide node, text width=.18\linewidth] (gift) {God first loves\\and gives the Spirit};
\node[guide node, right=of gift, text width=.18\linewidth] (root) {charity becomes\\the inward root; it bears fruit};
\draw[guide arrow] (gift) -- (root);
\end{tikzpicture}"""
BODY = (
    "Before the figure.\n\n\\begin{center}\n" + FLOWCHART + "\n\\end{center}\n\nAfter the figure.\n"
)
SKETCH = r"""\begin{sketchfig}
\begin{tikzpicture}[scale=0.8]
\draw (0,0) -- (1,1);
\node[slabel] at (2,0) {the staves, always in the rings};
\end{tikzpicture}
\sketchcaption{The ark as commanded. The measures are Scripture's (Exodus
25:10--22); the forms are not.}
\end{sketchfig}
"""


class FixtureTree:
    def __init__(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary.name)
        (self.root / "src/common").mkdir(parents=True)
        (self.root / "src/common/preamble.tex").write_text(PREAMBLE, encoding="utf-8")
        self.leaf = self.root / "src/gpt/articles/faith/fixture"
        self.leaf.mkdir(parents=True)
        self.entry = self.leaf / "main.tex"
        self.entry.write_text(HEAD + "\\begin{document}\n" + BODY + "\\end{document}\n", encoding="utf-8")

    def cleanup(self):
        self.temporary.cleanup()


class ExtractionTests(unittest.TestCase):
    def setUp(self):
        self.tree = FixtureTree()
        self.addCleanup(self.tree.cleanup)

    def extract(self, body=BODY, head=HEAD):
        return figures.extract(body, head, root=self.tree.root, provider="gpt", entrypoint=self.tree.entry)

    def test_picture_becomes_a_token_paragraph_with_a_source_identity(self):
        body, records = self.extract()
        self.assertEqual(len(records), 1)
        record = records[0]
        self.assertRegex(record["id"], r"\A[0-9a-f]{64}\Z")
        self.assertIn("\n\n\\TriptychWebFigure{" + record["id"] + "}\n\n", body)
        self.assertNotIn("tikzpicture", body)
        self.assertIn("Before the figure.", body)
        self.assertIn("After the figure.", body)
        self.assertEqual(record["inputs"], [{"path": "src/common/preamble.tex",
                                             "sha256": figures._sha(PREAMBLE)}])
        self.assertIn(FLOWCHART, record["tex"])
        self.assertIn("\\PreviewEnvironment{tikzpicture}", record["tex"])
        self.assertTrue(record["tex"].startswith(HEAD.rstrip("\n")))
        self.assertEqual(record["id"], figures.identity(record["tex"], record["inputs"]))

    def test_identity_is_stable_and_follows_the_preamble_bytes(self):
        first = self.extract()[1][0]["id"]
        self.assertEqual(first, self.extract()[1][0]["id"])
        (self.tree.root / "src/common/preamble.tex").write_text(PREAMBLE + "% changed\n", encoding="utf-8")
        self.assertNotEqual(first, self.extract()[1][0]["id"])

    def test_uncaptioned_alternative_numbers_node_texts_in_source_order(self):
        record = self.extract()[1][0]
        self.assertFalse(record["captioned"])
        self.assertEqual(
            record["alt"],
            "Diagram: (1) God first loves \u2014 and gives the Spirit; "
            "(2) charity becomes \u2014 the inward root; it bears fruit",
        )

    def test_caption_supplies_the_alternative_and_stays_in_the_body(self):
        body, records = self.extract(body="Intro.\n\n" + SKETCH)
        self.assertTrue(records[0]["captioned"])
        self.assertEqual(records[0]["alt"],
                         "The ark as commanded. The measures are Scripture\u2019s (Exodus "
                         "25:10\u201322); the forms are not. Labels in the figure: "
                         "the staves, always in the rings")
        self.assertEqual(records[0]["labels"], ["the staves, always in the rings"])
        self.assertIn("\\sketchcaption{The ark as commanded.", body)

    def test_commented_and_nested_pictures(self):
        body, records = self.extract(body="% \\begin{tikzpicture}\nText.\n")
        self.assertEqual(records, [])
        with self.assertRaises(figures.FigureError):
            self.extract(body="\\begin{tikzpicture}\\begin{tikzpicture}\\end{tikzpicture}\\end{tikzpicture}")
        with self.assertRaises(figures.FigureError):
            self.extract(body="\\begin{tikzpicture}\\node {x};")

    def test_unresolvable_preamble_input_is_refused(self):
        with self.assertRaises(figures.FigureError):
            self.extract(head="\\input{common/missing}\n")

    def test_strip_figures_removes_only_pictures(self):
        stripped = figures.strip_figures(BODY)
        self.assertNotIn("God first loves", stripped)
        self.assertIn("After the figure.", stripped)


class PlainTextTests(unittest.TestCase):
    def test_tex_markup_becomes_reader_text(self):
        self.assertEqual(
            figures.plain_text(r"\textbf{Linear inquiry}\\earlier $\longrightarrow$ later $\longrightarrow \cdots$"),
            "Linear inquiry \u2014 earlier \u2192 later \u2192 \u2026",
        )
        self.assertEqual(figures.plain_text(r"1738--1869 ``Freemasonry'' \& caf\'e~bar"),
                         "1738\u20131869 \"Freemasonry\" & cafe bar")


class ProjectionTests(unittest.TestCase):
    RECORD = {"id": "a" * 64, "alt": 'Diagram: "x" < y'}

    def token(self, figure="a" * 64):
        return figures.TOKEN_PREFIX + figure + figures.TOKEN_SUFFIX

    def test_token_paragraph_becomes_a_figure(self):
        markdown = f"Before.\n\n{self.token()}\n\nAfter.\n"
        projected = figures.project(markdown, [self.RECORD])
        self.assertIn(
            '<figure class="web-figure" data-figure="' + "a" * 64 + '"><img src="web-figures/'
            + "a" * 64 + '.svg" alt="Diagram: &quot;x&quot; &lt; y" loading="lazy" decoding="async"></figure>',
            projected,
        )
        self.assertNotIn(figures.TOKEN_PREFIX, projected)

    def test_quoted_token_keeps_its_quotation_prefix(self):
        projected = figures.project(f"> Lead.\n>\n> {self.token()}\n", [self.RECORD])
        self.assertIn("> <figure class=\"web-figure\"", projected)

    def test_missing_duplicate_extra_and_inline_tokens_are_refused(self):
        for markdown, records in (
            ("No figure.\n", [self.RECORD]),
            (f"{self.token()}\n\n{self.token()}\n", [self.RECORD]),
            (f"{self.token()}\n\n{self.token('b' * 64)}\n", [self.RECORD]),
            (f"Text {self.token()} text.\n", [self.RECORD]),
        ):
            with self.subTest(markdown=markdown), self.assertRaises(figures.FigureError):
                figures.project(markdown, records)

    def test_shim_macro_writes_the_token(self):
        self.assertIn("\\newcommand{\\TriptychWebFigure}[1]{" + figures.TOKEN_PREFIX + "#1"
                      + figures.TOKEN_SUFFIX + "}", figures.SHIM_ADDITIONS)


class CheckTests(unittest.TestCase):
    def test_check_reports_missing_extra_and_changed_figures(self):
        with tempfile.TemporaryDirectory() as temporary:
            out = Path(temporary)
            svg = b"<svg xmlns='http://www.w3.org/2000/svg'/>"
            (out / ("a" * 64 + ".svg")).write_bytes(svg)
            manifest = {"schema": figures.SCHEMA, "generator": figures.FIGURE_GENERATOR_VERSION,
                        "figures": {"a" * 64: {"sha256": figures._sha(svg), "bytes": len(svg)}},
                        "toolchain": {}}
            (out / "manifest.json").write_text(json.dumps(manifest))
            self.assertEqual(figures.check(out, ["a" * 64]), [])
            self.assertEqual(figures.check(out, ["a" * 64, "b" * 64]), ["figure not compiled: " + "b" * 64])
            self.assertEqual(figures.check(out, []), ["figure compiled for no edition: " + "a" * 64])
            (out / ("a" * 64 + ".svg")).write_bytes(svg + b" ")
            self.assertEqual(figures.check(out, ["a" * 64]), ["figure SVG differs from its manifest: " + "a" * 64])

    def test_runner_must_be_known(self):
        with self.assertRaises(figures.FigureError):
            figures._runner_command("ssh:elsewhere", ROOT, ROOT / "x.sh")
        command = figures._runner_command("docker:ghcr.io/example/tex@sha256:" + "0" * 64, ROOT, ROOT / "x.sh")
        self.assertEqual(command[:4], ["docker", "run", "--rm", "--network"])
        self.assertIn("none", command)


@unittest.skipUnless(all(shutil.which(tool) for tool in ("pdflatex", "pdftocairo", "pdfinfo")),
                     "pdflatex, pdftocairo and pdfinfo are required to compile figures")
class CompileTests(unittest.TestCase):
    def test_flowchart_compiles_twice_to_identical_svg(self):
        tree = FixtureTree()
        self.addCleanup(tree.cleanup)
        _, records = figures.extract(BODY, HEAD, root=tree.root, provider="gpt", entrypoint=tree.entry)
        out = tree.root / "build/web-figures"
        manifest = figures.compile_figures(records, out, root=tree.root)
        figure = records[0]["id"]
        svg = (out / f"{figure}.svg").read_bytes()
        self.assertIn(b"<svg", svg)
        self.assertEqual(manifest["figures"][figure], {"sha256": figures._sha(svg), "bytes": len(svg)})
        self.assertTrue(manifest["toolchain"]["pdflatex"].startswith("pdfTeX"))
        self.assertEqual(figures.check(out, [figure]), [])
        again = figures.compile_figures(records, out, root=tree.root)
        self.assertEqual(again["figures"], manifest["figures"])

    def test_a_preamble_that_demands_a_revision_stamp_still_compiles(self):
        # The shared preamble errors without \jobname.revision.tex; a figure job
        # supplies a fixed stamp rather than deriving one from git.
        tree = FixtureTree()
        self.addCleanup(tree.cleanup)
        (tree.root / "src/common/preamble.tex").write_text(PREAMBLE + (
            "\\newcommand{\\AIDocumentRevisionTimestamp}[1]{}\n"
            "\\InputIfFileExists{\\jobname.revision}{}{\\errmessage{No edition revision stamp}}\n"),
            encoding="utf-8")
        _, records = figures.extract(BODY, HEAD, root=tree.root, provider="gpt", entrypoint=tree.entry)
        out = tree.root / "build/web-figures"
        manifest = figures.compile_figures(records, out, root=tree.root)
        self.assertEqual(figures.check(out, [records[0]["id"]]), [])
        self.assertIn(records[0]["id"], manifest["figures"])

    def test_changed_source_no_longer_matches_its_identity(self):
        tree = FixtureTree()
        self.addCleanup(tree.cleanup)
        _, records = figures.extract(BODY, HEAD, root=tree.root, provider="gpt", entrypoint=tree.entry)
        tampered = [{**records[0], "tex": records[0]["tex"] + "% edit\n"}]
        with self.assertRaises(figures.FigureError):
            figures.compile_figures(tampered, tree.root / "out", root=tree.root)


if __name__ == "__main__":
    unittest.main()
