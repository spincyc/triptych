"""The Ecclesiastical Latin curriculum's web selection, constructs and coverage."""
from __future__ import annotations

from collections import Counter
import html
import importlib.machinery
import importlib.util
import os
import re
import shutil
import subprocess
import sys
import tempfile
import time
import tomllib
import unicodedata
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))
LOADER = importlib.machinery.SourceFileLoader(
    "triptych_web_edition_for_curriculum", str(ROOT / "tools" / "web-edition"))
SPEC = importlib.util.spec_from_loader(LOADER.name, LOADER)
DRIVER = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = DRIVER
SPEC.loader.exec_module(DRIVER)

import _web_edition_curriculum as curriculum  # noqa: E402
from _markdown_render import MarkdownRenderError, render_markdown  # noqa: E402

HAS_PANDOC = shutil.which("pandoc") is not None
HAS_TEX = all(shutil.which(tool) for tool in ("pdflatex", "pdftotext"))
COURSE_ROOT = ROOT / "src" / "gpt" / curriculum.COURSE
GROUP = r"\{(?:[^{}]|\{(?:[^{}]|\{[^{}]*\})*\})*\}"


def site_renderer_available() -> bool:
    try:
        render_markdown("x", ROOT)
    except MarkdownRenderError:
        return False
    return True


def curriculum_leaves() -> list[str]:
    """Every curriculum leaf the selection serves: a curriculum kind, not ineligible."""
    leaves = []
    for manifest in sorted(COURSE_ROOT.rglob("publication.toml")):
        declaration = manifest.with_name("web-edition.toml")
        kind = tomllib.loads(manifest.read_text(encoding="utf-8")).get("kind", "")
        if not curriculum.applies(kind) or not declaration.is_file():
            continue
        record = tomllib.loads(declaration.read_text(encoding="utf-8"))
        if record.get("eligibility") != "ineligible" and not record.get("withdrawn"):
            leaves.append(manifest.parent.relative_to(ROOT / "src" / "gpt").as_posix())
    return leaves


def words(text: str) -> list[str]:
    return [word.casefold() for word in re.findall(r"[^\W\d_]+", unicodedata.normalize("NFKC", text))]


def selected_words(body: str) -> list[str]:
    """The words the selected TeX sets, without commands, layout or audit-only metadata."""
    body = curriculum.TOKEN_RE.sub(" ", body)
    body = re.sub(r"\\AIModelContribution(?:Repeat)?" + GROUP * 3
                  + r"|\\AIGenerationProvenance" + GROUP * 6, " ", body)
    body = re.sub(r"\\\\\*?(?:\[[^\]]*\])?", " ", body)
    body = re.sub(r"\\begin\{(?:longtable|tabular)\}" + GROUP, " ", body)
    body = re.sub(r"\\multicolumn" + GROUP * 2, " ", body)
    body = re.sub(r"\\(?:begin|end)\s*\{[^{}]*\}(?:\[[^\]]*\])?", " ", body)
    body = re.sub(r"\\[A-Za-z@]+\*?", " ", body)
    return words(re.sub(r"\$[^$]*\$", " ", body))


def page_words(markdown: str) -> list[str]:
    return words(html.unescape(re.sub(r"<[^>]+>", " ", render_markdown(markdown, ROOT))))


class FixtureCourse(unittest.TestCase):
    """A small course in a sandbox repository, read exactly as the real one is."""

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        (self.root / "src/common").mkdir(parents=True)
        (self.root / "src/common/preamble.tex").write_text("% shared preamble\n")
        self.leaf = curriculum.COURSE + "/fixture"
        (self.root / "src/gpt" / self.leaf).mkdir(parents=True)

    def tearDown(self):
        self.tmp.cleanup()

    def select(self, document: str) -> dict:
        (self.root / "src/gpt" / self.leaf / "main.tex").write_text(document)
        return curriculum.selection(self.root, "gpt", self.leaf, DRIVER)


PROGRAM = r"""\input{common/preamble}
\newcommand{\SelectedUnits}{all}
\newcommand{\SelectUnits}[1]{\renewcommand{\SelectedUnits}{#1}}
\NewEnviron{unit}[1]{\IfStrEq{\SelectedUnits}{all}{\BODY}{%
  \IfSubStr{,\SelectedUnits,}{,#1,}{\BODY}{}}}
\newif\ifsolutions
\newcommand{\Exercise}[3][0.38in]{\item #2%
  \ifsolutions\par\textbf{Answer:} #3\else\par\vspace{#1}\hrulefill\fi}
\newcommand{\Key}{U1}
\hypersetup{pdftitle={Fixture Packet},pdfsubject={A sandbox}}
\begin{document}
\SelectUnits{\Key,U3}
\part{Practice}
\chapter{Forms}
\begin{unit}{U1}\begin{enumerate}\Exercise[0.9in]{Alpha prompt}{alpha answer}\end{enumerate}\end{unit}
\begin{unit}{U2}Beta never set.\end{unit}
\begin{unit}{U3}Gamma set.\end{unit}
\part{Answers}
\solutionstrue
\chapter{Unit keys}
\section*{Solution U1}
\begin{unit}{U1}\begin{enumerate}\Exercise[0.9in]{Alpha prompt}{alpha answer}\end{enumerate}\end{unit}
\solutionsfalse
\end{document}
"""


class SelectionTests(FixtureCourse):
    def test_units_solutions_and_responses_follow_the_tex_program(self):
        selected = self.select(PROGRAM)
        body = selected["body"]
        self.assertIn("Alpha prompt", body)
        self.assertIn("Gamma set.", body)
        self.assertNotIn("Beta never", body)
        # The learner form leaves a response space; the key alone sets the answer.
        self.assertEqual(body.count("alpha answer"), 1)
        self.assertEqual(len(curriculum.RESPONSE_RE.findall(body)), 1)
        self.assertLess(body.index(curriculum.KEY_ON), body.index("alpha answer"))
        self.assertLess(body.index("alpha answer"), body.index(curriculum.KEY_OFF))
        # Print levels shift one down: Part, Chapter, Section become H2..H4.
        self.assertIn(r"\section{Practice}", body)
        self.assertIn(r"\subsection{Forms}", body)
        self.assertIn(r"\subsubsection*{Solution U1}", body)
        self.assertIn(r"pdftitle={Fixture Packet}", selected["source"])
        self.assertNotIn("\\input", selected["source"])

    def test_tokens_keep_control_word_boundaries_and_registries_expand(self):
        selected = self.select(r"""\input{common/preamble}
\newcommand{\SetKey}{M01}
\csdef{set@M01@new}{\Item{L1}\Item{L2}}
\newcommand{\Item}[1]{[#1]}
\newcommand{\UseSet}[1]{\csuse{set@#1@new}}
\newcounter{Count}
\newcommand{\Declare}[1]{\stepcounter{Count}\gappto{\All}{#1;}}
\newcommand{\All}{}
\Declare{a}\Declare{b}
\hypersetup{pdftitle={Registry}}
\begin{document}
\UseSet{\SetKey} \All{} \arabic{Count}
\forcsvlist{\Item}{x, y}
\end{document}
""")
        self.assertIn("[L1][L2]", selected["body"])
        self.assertIn("a;b;", selected["body"])
        self.assertIn(" 2", selected["body"])
        self.assertIn("[x][y]", selected["body"])

    def test_unmodelled_constructs_are_refused(self):
        for construct, message in (
            (r"\ifx\a\b yes\fi", "unmodelled conditional"),
            (r"\PackageError{course}{Duplicate}{}", "Duplicate"),
            (r"\begin{tikzpicture}\end{tikzpicture}", "unmodelled environment"),
            (r"\edef\x{y}", "expands at definition time"),
        ):
            with self.subTest(construct=construct), self.assertRaisesRegex(
                    curriculum.CurriculumError, message):
                self.select("\\hypersetup{pdftitle={T}}\\begin{document}" + construct
                            + "\\end{document}\n")

    def test_layout_is_dropped_and_wrappers_unwrapped(self):
        selected = self.select(r"""\hypersetup{pdftitle={T}}
\begin{document}
\Needspace{9\baselineskip}\clearpage\markboth{a}{b}\hbadness=10000
\fcolorbox{black}{gray}{\begin{minipage}{0.9\linewidth}\textbf{Boxed.} text\end{minipage}}
\begin{center}Centred\end{center}\rule{\linewidth}{1pt}\rule{0pt}{2em}
Name: \rule{1.3in}{0.4pt} and \rule{2.6in}{0.4pt}.
\end{document}
""")
        body = selected["body"]
        for gone in ("Needspace", "clearpage", "markboth", "hbadness", "minipage",
                     "fcolorbox", "center", "rule"):
            self.assertNotIn(gone, body)
        self.assertIn(r"\textbf{Boxed.} text", body)
        self.assertEqual(len(curriculum.RESPONSE_RE.findall(body)), 2)


class ProjectionTests(unittest.TestCase):
    def test_response_spaces_blanks_and_write_in_rows(self):
        responses = [{"kind": "line", "lines": 1, "size": "fill"},
                     {"kind": "line", "lines": 2, "size": "fill"},
                     {"kind": "blank", "lines": 1, "size": "long"},
                     {"kind": "line", "lines": 1, "size": "fill"}]
        token = lambda number: f"{curriculum.RESPONSE}{number}-END"  # noqa: E731
        markdown = "\n".join([
            "1.  Prompt", "", f"    {token(1)}", "", f"    {token(2)}", "",
            f"Name: {token(3)} here.", "",
            "| Form | Lemma |", "|:-----|:------|", f"| x | {token(4)} |", "|   |   |", "",
        ])
        projected = curriculum.project(markdown, responses, [])
        self.assertIn('    <span class="web-response" data-lines="3"', projected)
        self.assertEqual(projected.count('class="web-response"'), 1)
        self.assertIn('Name: <span class="web-blank" data-size="long"', projected)
        self.assertIn('| x | <span class="web-blank" data-size="fill"', projected)
        empty_row = projected.splitlines()[-1] if projected.splitlines()[-1] else projected.splitlines()[-2]
        self.assertEqual(empty_row.count('data-size="fill"'), 2)

    def test_lost_response_is_refused(self):
        with self.assertRaisesRegex(curriculum.CurriculumError, "lost"):
            curriculum.project("no token here", [{"kind": "line", "lines": 1, "size": "fill"}], [])

    def test_answer_keys_wrap_a_chapter_with_text_or_each_section_of_a_grouping_chapter(self):
        markdown = "\n".join([
            "## Answers", "", curriculum.KEY_ON, "",
            "### Memory answers", "", "#### Lexemes", "", "x", "", "#### Grammar", "", "y", "",
            "### Reader", "", "Note.", "", "#### Model", "", "z", "",
            curriculum.KEY_OFF, "", "## Scope", "",
        ])
        projected = curriculum.project(markdown, [], [])
        comments = re.findall(r"<!-- (/?)triptych:answer-key ?([^>]*?) ?-->", projected)
        self.assertEqual([summary for opening, summary in comments if not opening],
                         ["Lexemes", "Grammar", "Reader"])
        self.assertEqual(sum(1 for opening, _ in comments if opening), 3)
        self.assertLess(projected.index("### Memory answers"), projected.index("answer-key Lexemes"))
        self.assertLess(projected.index("answer-key Reader"), projected.index("#### Model"))

    def test_scansion_display_is_mathml(self):
        mathml = curriculum.scansion_mathml(
            r"\underbrace{\text{--}\;\text{--}}_{\text{opening base}}\mid\smile\,\times .")
        self.assertTrue(mathml.startswith('<math display="block">'))
        for part in ("<munder>", "⏟", "<mtext>opening base</mtext>", "∣", "⌣", "×"):
            self.assertIn(part, mathml)
        with self.assertRaises(curriculum.CurriculumError):
            curriculum.scansion_mathml(r"\frac{1}{2}")


@unittest.skipUnless(HAS_PANDOC, "pandoc is required for conversion")
@unittest.skipUnless(site_renderer_available(), "the pinned site Markdown renderer is required")
class RealCourseTests(unittest.TestCase):
    """Every served curriculum leaf converts and loses no selected word."""

    def test_the_curriculum_leaf_set(self):
        self.assertEqual(len(curriculum_leaves()), 36)

    def test_every_leaf_converts_with_complete_ordered_coverage(self):
        report = []
        with tempfile.TemporaryDirectory() as directory:
            for leaf in curriculum_leaves():
                with self.subTest(leaf=leaf):
                    started = time.monotonic()
                    selected = curriculum.selection(ROOT, "gpt", leaf, DRIVER)
                    path = DRIVER.convert("gpt", leaf, Path(directory), selected=selected)
                    markdown = path.read_text(encoding="utf-8")
                    elapsed = time.monotonic() - started
                    report.append((leaf, len(markdown.encode()), elapsed))
                    self.assertNotIn("TRIPTYCHCURRICULUM", markdown)
                    page = page_words(markdown)
                    wanted = selected_words(selected["body"])
                    missing = Counter(wanted) - Counter(page)
                    self.assertFalse(missing, f"selected words missing from the page: {missing.most_common(10)}")
                    cursor = 0
                    for word in page:
                        if cursor < len(wanted) and wanted[cursor] == word:
                            cursor += 1
                    self.assertEqual(cursor, len(wanted),
                                     "selected words out of order near: " + " ".join(wanted[cursor:cursor + 12]))
                    if selected["body"].count(curriculum.KEY_ON):
                        self.assertIn("<!-- triptych:answer-key ", markdown)
                    self.assertEqual(markdown.count("<!-- triptych:answer-key "),
                                     markdown.count("<!-- /triptych:answer-key -->"))
        if os.environ.get("TRIPTYCH_CURRICULUM_REPORT"):
            for leaf, size, elapsed in report:
                print(f"{leaf}\t{size}\t{elapsed:.2f}s", file=sys.stderr)


@unittest.skipUnless(HAS_TEX, "pdflatex and pdftotext are required to typeset the reference")
class TypesetAgreementTests(unittest.TestCase):
    """What the selection sets is what TeX sets, apart from print furniture."""

    LEAVES = (curriculum.COURSE + "/01-foundations/01-form-case-and-agreement",
              curriculum.COURSE + "/05-stage-assessments/04-advanced",
              curriculum.COURSE + "/00-course-guide")
    # Printed Part numerals, the contents heading, and repeated longtable heads.
    FURNITURE = frozenset("part contents i ii iii iv v vi id event sense latin project gloss "
                          "citation morphology use form fact prompt response model".split())

    def test_selected_words_are_the_typeset_words(self):
        for leaf in self.LEAVES:
            with self.subTest(leaf=leaf), tempfile.TemporaryDirectory() as directory:
                finished = subprocess.run(
                    ["pdflatex", "-no-shell-escape", "-interaction=nonstopmode", "-halt-on-error",
                     "-jobname=reference", f"-output-directory={directory}", f"{leaf}/main.tex"],
                    cwd=ROOT / "src/gpt", env={**os.environ, "TEXINPUTS": "..:"},
                    capture_output=True, text=True, check=False)
                self.assertEqual(finished.returncode, 0, finished.stdout[-2000:])
                text = subprocess.run(["pdftotext", "-layout", f"{directory}/reference.pdf", "-"],
                                      capture_output=True, text=True, check=True).stdout
                pages = [page for page in text.split("\f")
                         if not (re.search(r"^\s*Contents\s*$", page, re.M) and ". . ." in page)]
                lines = [line for page in pages for line in page.split("\n")
                         if not re.match(r"\s*(?:TRIPTYCH / ECCLESIASTICAL LATIN|Disce legendo"
                                         r"|CHAPTER \d+\s*$)", line)]
                # The closing timestamp and rights notice are the shared
                # preamble's; the converter appends the web's own.
                text = "\n".join(lines).split("Last revised (UTC)")[0]
                typeset = Counter(words(re.sub(r"(\w)-\n\s*(\w)", r"\1\2", text)))
                selected = Counter(selected_words(curriculum.selection(ROOT, "gpt", leaf, DRIVER)["body"]))
                # Hyphenation rejoining leaves a few compounds unsplit.
                missing = {word: count for word, count in (typeset - selected).items()
                           if word not in self.FURNITURE and not word.endswith(("order", "paced"))}
                self.assertLessEqual(sum(missing.values()), 6, missing)
                extra = selected - typeset
                self.assertLessEqual(sum(extra.values()), 6, dict(extra))


if __name__ == "__main__":
    unittest.main()
