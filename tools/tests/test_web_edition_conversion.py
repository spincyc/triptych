from __future__ import annotations

import importlib.machinery
import importlib.util
from importlib.metadata import PackageNotFoundError
import re
import runpy
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
# A proper title block whose Latin line recurs in the opening prose, as it does
# in the leaves: a search of the whole edition cannot see that line dropped.
PROPER_TITLE = (
    r"\propertitle{The Eighteenth Sunday after Pentecost}" "\n"
    r"{Dominica decima octava post Pentecosten}" "\n"
    r"{Missale Romanum 1962 \quad\textperiodcentered\quad Proper of Time}" "\n"
    r"{Peace for the city:\\" "\n"
    r"a study of the proper in three readings}" "\n\n"
    r"The Eighteenth Sunday after Pentecost, \latin{Dominica decima octava post "
    r"Pentecosten}, is a Sunday of the second class."
)

# Pandoc pads narrow cells to align the columns; tests compare with runs of
# spaces collapsed, since the padding is not content.
DOSSIER_HEADER = "| **Proper** | **Citation** | **Location** | **Date** |\n|"


@unittest.skipUnless(HAS_PANDOC, "pandoc is not installed")
class WebEditionConversionTests(unittest.TestCase):
    def convert(
        self, body: str, metadata: str = CONTRIBUTION, preamble: str = "",
        *, files: dict[str, str] | None = None, proper: bool = False,
        element_keys: tuple[str, ...] = (),
        proper_schema: int | None = None,
        format_contract: str | None = None,
        title: str = "Subject",
    ) -> str:
        """Convert a synthetic single-section leaf and return its Markdown."""
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            leaf = root / "src" / "test" / "studies" / "subject"
            leaf.mkdir(parents=True)
            if proper:
                (leaf / "proper-components.toml").write_text(
                    (f"schema = {proper_schema}\n" if proper_schema is not None else "")
                    + (f"format_contract = {format_contract!r}\n" if format_contract else "")
                    + f"element_keys = {list(element_keys)!r}\n", encoding="utf-8"
                )
            for name, text in (files or {}).items():
                path = leaf / name
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(text, encoding="utf-8")
            (leaf / "generation-metadata.tex").write_text(
                rf"\AIDocumentRevisionTimestamp{{{TIMESTAMP}}}" + "\n" + metadata + "\n",
                encoding="utf-8",
            )
            (leaf / "main.tex").write_text(
                "\\input{common/preamble}\n"
                r"\hypersetup{pdftitle={" + title + r"},pdfsubject={A synthetic leaf}}"
                "\n" + preamble + "\n\\begin{document}\n"
                "\\begin{titlepage}\nDropped title page\n\\end{titlepage}\n"
                "\\section{Body}\n" + body + "\n"
                r"\input{studies/subject/generation-metadata}"
                "\n\\end{document}\n",
                encoding="utf-8",
            )
            with mock.patch.object(DRIVER, "SRC", root / "src"), mock.patch.object(
                DRIVER, "OUT", root / "build" / "web"
            ):
                destination = DRIVER.convert("test", "studies/subject", root / "build" / "web")
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

    def test_generated_markdown_has_no_trailing_whitespace(self) -> None:
        cleaned = DRIVER.clean_markdown_line_endings("Title  \nSubtitle \t\nPlain\n")
        self.assertEqual(cleaned, "Title<br>\nSubtitle<br>\nPlain\n")
        markdown = self.convert("First line.\n\nSecond line.")
        self.assertIsNone(re.search(r"[ \t]+$", markdown, re.MULTILINE))

    @unittest.skipUnless(importlib.util.find_spec("markdown"), "Python Markdown is not installed")
    def test_superscripts_survive_the_actual_site_renderer(self) -> None:
        # Pandoc's default ^137^ reached the site's reader as literal carets.
        # Exercise the owning renderer, including its locked Markdown version.
        markdown = self.convert(
            r"\textsuperscript{137}SADE. Ordinal\textsuperscript{er}. "
            r"Symbol\textsuperscript{*}. Escaped\textsuperscript{a\&b}. "
            r"Styled\textsuperscript{\textit{ab}}. Note.\footnote{Citation.}"
        )
        site = runpy.run_path(str(ROOT / "tools/public-alpha"))
        rendered = site["render_page"](
            "web/test/studies/subject.md", markdown, "subject.html", True, {}
        )
        for fragment in (
            "<sup>137</sup>SADE.", "Ordinal<sup>er</sup>",
            "Symbol<sup>*</sup>", "Escaped<sup>a&amp;b</sup>",
            "Styled<sup><em>ab</em></sup>",
        ):
            self.assertIn(fragment, rendered)
        self.assertEqual(rendered.count("<sup>"), 5)
        self.assertNotIn("^137^", rendered)
        self.assertIn('class="footnote-ref"', rendered)
        self.assertIn("Citation.", rendered)

    def test_braced_path_locators_survive_as_literal_unlinked_code(self) -> None:
        locators = (
            "propers/verified.md",
            "research/scope.md",
            "research/interpretations.md",
            "research/production-review.md",
            "research/source_record-v1&notes#locus.md",
        )
        markdown = self.convert("See " + ", ".join(
            rf"\path{{{locator}}}" for locator in locators
        ) + ".")
        for locator in locators:
            self.assertIn(f"`{locator}`", markdown)
            self.assertNotIn(f"]({locator})", markdown)
        self.assertNotIn(r"\path", markdown)

    def test_path_allows_whitespace_before_its_braced_locator(self) -> None:
        markdown = self.convert("See \\path \n {research/scope.md}.")
        self.assertIn("`research/scope.md`", markdown)

    def test_non_braced_path_syntax_is_refused_before_conversion(self) -> None:
        for body in (
            r"See \path|research/source_record-v1.md|.",
            r"See \path+research/source_record-v1.md+.",
            r"See \path[draw] (0,0) -- (1,1);.",
        ):
            with self.subTest(body=body), mock.patch.object(DRIVER.subprocess, "run") as pandoc:
                with self.assertRaises(DRIVER.ConversionError) as raised:
                    self.convert(
                        r"\input{studies/subject/sections/paths}",
                        files={"sections/paths.tex": body},
                    )
                self.assertIn(r"unsupported \path syntax", str(raised.exception))
                self.assertIn("sections/paths.tex", str(raised.exception))
                pandoc.assert_not_called()

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

    def test_inline_edition_branch_keeps_its_sentence_whole(self) -> None:
        # `\fi{}` is the inline form: the branch stands inside a sentence, and
        # the newlines around \ifdefined, \else and \fi are TeX's to gobble.
        markdown = self.convert(
            "The claim rests on a reading he sets out at length,\n"
            r"\ifdefined\TriptychSynthesisEdition" "\n"
            "as the fourth unit sets out%\n"
            r"\else" "\n"
            "as the Gospel subsection sets out%\n"
            r"\fi{} (Payne, p.~1); and the same subsection shows it" "\n"
            r"\ifdefined\TriptychSynthesisEdition" "\n"
            "there%\n"
            r"\else" "\n"
            "word by word%\n"
            r"\fi{}: at that place the reading is closer.",
            proper=True,
        )
        self.assertIn(
            "The claim rests on a reading he sets out at length, "
            "as the Gospel subsection sets out (Payne, p.\N{NO-BREAK SPACE}1); "
            "and the same subsection shows it word by word: "
            "at that place the reading is closer.",
            markdown,
        )
        self.assertNotIn("sets out\n\n", markdown)
        self.assertNotIn("word by word :", markdown)

    def test_capital_opening_cut_is_reported_by_the_run_check(self) -> None:
        # Both fragments open on a capital, so the case rule sees nothing; the
        # source keeps these words in one run, so the run check sees the cut.
        sources = (
            "\\item Council of Trent, Session~VI, cap.~X, cap.~XVI and can.~32, "
            "from the Tauchnitz 1887 printing of the Canones, page-verified in this repository.\n"
        )
        markdown = (
            "# Subject\n\n"
            "Council of Trent, Session VI, cap. X, cap. XVI and can. 32, from the\n\n"
            "Tauchnitz 1887 printing of the Canones, page-verified in this repository.\n"
        )
        failures = DRIVER.audit_output("Prose.", markdown, sources=sources)
        self.assertTrue(
            any("fell inside a run of words" in failure for failure in failures),
            failures,
        )
        self.assertFalse(
            any("lowercase" in failure for failure in failures), failures
        )

    def test_a_break_hint_does_not_eat_the_token_after_it(self) -> None:
        # Pandoc consumed the token after \allowbreak inside \texttt, so
        # `sections/50-resumed-sundays.tex` reached the reader as
        # `sections/-resumed-sundays.tex`, with no warning of any kind.
        markdown = self.convert(
            r"The file \texttt{sections/\allowbreak 50-resumed-sundays.tex} "
            r"carries it."
        )
        self.assertIn("sections/50-resumed-sundays.tex", markdown)
        self.assertNotIn("sections/-resumed", markdown)

    def test_a_bracketed_macro_is_not_read_as_an_optional_argument(self) -> None:
        # Pandoc expands \notread before \nopagebreak looks ahead, takes the
        # bracket it finds for an optional argument and drops the clause; TeX
        # sets it. The Acts verse of a postconciliar study lost half its words.
        preamble = (
            r"\newcommand{\notread}[1]{[\textit{#1}]}"
            "\n"
            r"\newenvironment{witness}[1]"
            r"{\begin{quote}\textsc{#1}\par\nopagebreak}{\end{quote}}"
        )
        markdown = self.convert(
            "\\begin{witness}{Douay--Rheims, Acts 16:14}\n"
            r"\notread{And a certain woman named Lydia did hear:} whose heart "
            "the Lord opened.\n\\end{witness}\n\n"
            r"Also \noindent\notread{a second clause} here.",
            preamble=preamble,
        )
        self.assertIn(r"\[*And a certain woman named Lydia did hear:*\] whose", markdown)
        self.assertIn(r"\[*a second clause*\] here", markdown)
        # A definition in the body is guarded too, and is not read as a call.
        markdown = self.convert(
            r"\newcommand{\gloss}[1]{[\textit{#1}]}"
            "\n\n"
            r"Text \noindent\gloss{a body-defined clause} ends."
        )
        self.assertIn(r"\[*a body-defined clause*\] ends", markdown)

    def test_a_middle_dot_separator_survives_and_keeps_its_spacing(self) -> None:
        # Pandoc drops \textperiodcentered silently. Braced, the space after it
        # is the author's; bare, TeX gobbles it, which is the Catalan geminate.
        markdown = self.convert(
            r"\textbf{Ident.} Dominica \textperiodcentered{} II classis "
            r"\textperiodcentered{} Green, in \emph{Miscel\textperiodcentered "
            r"lania}."
        )
        self.assertIn(
            "Dominica \N{MIDDLE DOT} II classis \N{MIDDLE DOT} Green", markdown)
        self.assertIn("Miscel\N{MIDDLE DOT}lania", markdown)

    def test_a_numbered_element_heading_carries_the_declared_anchor(self) -> None:
        """The anchor cannot depend on which macro a leaf heads an element with.

        `anchor_appointed_elements` keyed on \fulltextheading, which is defined
        only under src/gpt. A claude leaf heads the same element with a numbered
        subsection, matched nothing, and every claude edition shipped with no
        component anchors at all. The commentary heads the same element again
        and adds the incipit, so the appointed heading is the one that stops at
        its cue -- anchoring both mints the key twice and the edition is refused.
        """
        markdown = self.convert(
            r"\subsection*{1. Introit \cue{Int.}}" "\n"
            r"The appointed text stands here." "\n\n"
            r"\subsection*{1. Introit \cue{Int.} --- \emph{Miserere mihi}}" "\n"
            r"The commentary on it stands here." "\n\n"
            r"\subsection*{2. A Section That Is Not An Element}" "\n"
            r"Ordinary prose stands here.",
            preamble=r"\newcommand{\cue}[1]{\textit{#1}}",
            proper=True, element_keys=("introit",),
        )
        self.assertEqual(markdown.count("{#proper-introit}"), 1)
        self.assertIn("Introit", markdown)

    def test_line_ending_comment_before_a_guard_sets_no_space(self) -> None:
        # TeX lets `%` eat its own newline, so the page sets "on John," closed
        # up.  Pandoc keeps the newline and reads it as a space, which is how
        # the only space-before-a-comma in a 205 KB edition got there.
        markdown = self.convert(
            "Augustine's \\work{Tractatus} on John%\n"
            r"\ifdefined\TriptychSynthesisEdition{} and Chrysostom's Homily~7%"
            "\n"
            r"\else, Chrysostom's Homily~7, and Gregory's \work{Regula}%" "\n"
            r"\fi{} are read in the NPNF English.",
            proper=True,
        )
        self.assertIn("on John, Chrysostom", markdown)
        self.assertNotIn("John ,", markdown)

    def test_block_form_guard_mid_sentence_keeps_one_paragraph(self) -> None:
        # A block-form guard standing inside a sentence used to contribute a
        # blank line at each seam, cutting one reference into three paragraphs.
        markdown = self.convert(
            "Council of Trent,\n"
            r"\ifdefined\TriptychSynthesisEdition" "\n"
            "Session~VI, cap.~X and cap.~XVI, from the\n"
            r"\else" "\n"
            "Session~VI, cap.~X, cap.~XVI and can.~32, from the\n"
            r"\fi" "\n"
            "Tauchnitz 1887 printing of the Canones, page-verified in this repository.",
            proper=True,
        )
        self.assertIn(
            "Council of Trent, Session\N{NO-BREAK SPACE}VI, cap.\N{NO-BREAK SPACE}X, "
            "cap.\N{NO-BREAK SPACE}XVI and can.\N{NO-BREAK SPACE}32, from the "
            "Tauchnitz 1887 printing of the Canones, page-verified in this repository.",
            markdown,
        )

    def test_block_form_guard_between_blocks_keeps_its_paragraphs(self) -> None:
        markdown = self.convert(
            "Paragraph one ends here.\n\n"
            r"\ifdefined\TriptychSynthesisEdition" "\n"
            "Companion block.\n"
            r"\else" "\n"
            "Canonical block.\n"
            r"\fi" "\n\n"
            "Paragraph two.",
            proper=True,
        )
        self.assertIn("Paragraph one ends here.\n\nCanonical block.", markdown)
        self.assertIn("Canonical block.\n\nParagraph two.", markdown)

    def test_paragraph_opened_in_mid_sentence_is_reported(self) -> None:
        sources = (
            "Section.\n\n"
            "The claim rests on a reading he sets out at length, "
            "as the Gospel subsection sets out (Payne, p.~1).\n"
        )
        markdown = (
            "# Subject\n\n"
            "The claim rests on a reading he sets out at length,\n\n"
            "as the Gospel subsection sets out (Payne, p. 1).\n"
        )
        failures = DRIVER.audit_output("Prose.", markdown, sources=sources)
        self.assertTrue(
            any("opened on a lowercase word" in failure for failure in failures),
            failures,
        )
        whole = markdown.replace(",\n\n", ", ")
        self.assertEqual(
            [], [f for f in DRIVER.audit_output("Prose.", whole, sources=sources)
                 if "opened on a lowercase word" in f]
        )

    def test_paragraph_the_sources_open_the_same_way_is_not_reported(self) -> None:
        # A leaf may open a paragraph on a lowercase word of its own; only an
        # opening its own files never use is evidence of a reflowed sentence.
        sources = (
            "Section.\n\n"
            "\\item miserere mei, the psalm's own opening, is sung twice\n\n"
            "and a further line that does not close its sentence\n"
        )
        markdown = (
            "# Subject\n\n"
            "and a further line that does not close its sentence\n\n"
            "miserere mei, the psalm's own opening, is sung twice.\n"
        )
        self.assertEqual(
            [],
            [f for f in DRIVER.audit_output("Prose.", markdown, sources=sources)
             if "opened on a lowercase word" in f],
        )

    def test_proper_canonical_branch_survives_recursive_section_inputs(self) -> None:
        markdown = self.convert(
            r"\ifdefined\TriptychSynthesisEdition"
            r"\input{studies/subject/missing-companion}"
            r"\else\input{studies/subject/sections/outer}\fi",
            proper=True,
            files={
                "sections/outer.tex": r"\input{studies/subject/sections/references}",
                "sections/references.tex": (
                    r"\ifdefined\TriptychSynthesisEdition"
                    r"\unknowncompanion{Companion-only wording.}"
                    r"\input{studies/subject/missing-references}"
                    r"\else\clearpage\section*{References}\label{sec:references}"
                    r"Canonical witness at \sourceurl{https://example.invalid/witness}{its locus}."
                    r"\fi Shared terminal text."
                ),
            },
        )
        self.assertIn("## References {#sec:references}", markdown)
        self.assertIn("Canonical witness", markdown)
        self.assertIn("https://example.invalid/witness", markdown)
        self.assertIn("Shared terminal text.", markdown)
        self.assertNotIn("Companion-only", markdown)

    def test_proper_active_included_macro_is_still_refused(self) -> None:
        with self.assertRaises(DRIVER.ConversionError) as raised:
            self.convert(
                r"\input{studies/subject/sections/references}",
                proper=True,
                files={"sections/references.tex": (
                    r"\ifdefined\TriptychSynthesisEdition Companion."
                    r"\else\dubiousclaim{Canonical evidence.}\fi"
                )},
            )
        self.assertIn(r"unknown macro \dubiousclaim", str(raised.exception))
        self.assertIn("sections/references.tex", str(raised.exception))

    def test_synthesis_branch_requires_a_componentized_proper(self) -> None:
        with self.assertRaises(DRIVER.ConversionError) as raised:
            self.convert(
                r"\input{studies/subject/sections/references}",
                files={"sections/references.tex": (
                    r"\ifdefined\TriptychSynthesisEdition Companion."
                    r"\else Canonical.\fi"
                )},
            )
        self.assertIn(r"unknown macro \TriptychSynthesisEdition", str(raised.exception))

    def test_appointed_element_anchor_is_independent_of_heading_wording(self) -> None:
        for heading in ("Collect --- no. 1593", "Collect: grace before and after"):
            with self.subTest(heading=heading):
                markdown = self.convert(
                    r"\subsection*{Collect} Chronology context."
                    rf"\fulltextheading{{{heading}}} Appointed prayer.",
                    preamble=r"\newcommand{\fulltextheading}[1]{\subsection*{#1}}",
                    proper=True, element_keys=("collect",),
                )
                self.assertIn("{#proper-collect}", markdown)
                self.assertEqual(markdown.count("{#proper-collect}"), 1)
                self.assertRegex(markdown, r"\{#proper-collect\}\s+Appointed prayer\.")
                self.assertNotIn("### Collect {#proper-collect}", markdown)

    def test_appointed_element_preserves_an_explicit_source_anchor(self) -> None:
        markdown = self.convert(
            r"\fulltextheading{Collect}\label{appointed:collect} Appointed prayer.",
            preamble=r"\newcommand{\fulltextheading}[1]{\subsection*{#1}}",
            proper=True, element_keys=("collect",),
        )
        self.assertIn("{#appointed:collect}", markdown)
        self.assertNotIn("{#proper-collect}", markdown)

    def test_appointed_element_must_be_declared_in_manifest(self) -> None:
        with self.assertRaises(DRIVER.ConversionError) as raised:
            self.convert(
                r"\fulltextheading{Invented} Appointed prayer.",
                preamble=r"\newcommand{\fulltextheading}[1]{\subsection*{#1}}",
                proper=True, element_keys=("collect",),
            )
        self.assertIn("undeclared appointed element", str(raised.exception))

    @unittest.skipUnless(importlib.util.find_spec("markdown"), "Python Markdown is not installed")
    def test_schema_two_explicit_heading_and_paragraph_anchors_reach_the_site(self) -> None:
        keys = ("entrance", "collect", "first-reading", "responsorial-psalm", "second-reading",
                "acclamation", "gospel", "offerings", "communion-ps119", "communion-jn10", "after-communion")
        body = (
            r"\subsection{Entrance and Collect}\label{proper-entrance}" "\n"
            r"\textbf{Entrance:} Entrance locator." "\n\n"
            r"\label{proper-collect}\textbf{Collect:} Collect locator." "\n\n"
        )
        for key, heading in zip(keys[2:8], (
            "Isaiah 55:6--9", "Psalm 145", "Philippians 1", "Acts 16",
            "Matthew 20", "Prayer over the Offerings",
        )):
            body += rf"\subsection{{{heading}}}\label{{proper-{key}}} Text for {key}." + "\n\n"
        body += (
            r"\subsection{Communion alternatives}\label{proper-communion-ps119}" "\n"
            r"\textbf{First alternative:} Psalm text." "\n\n"
            r"\label{proper-communion-jn10}\textbf{Second alternative:} John text." "\n\n"
            r"\subsection{Prayer after Communion}\label{proper-after-communion} Prayer locator." "\n\n"
            r"\section{Appendix}\label{ordinary-label} Other labels remain allowed. "
            r"See \hyperref[proper-collect]{Collect} and \hyperref[proper-communion-jn10]{John}."
        )
        markdown = self.convert(body, proper=True, proper_schema=2, element_keys=keys)
        site = runpy.run_path(str(ROOT / "tools/public-alpha"))
        rendered = site["render_page"]("web/test/studies/subject.md", markdown, "subject.html", True, {})
        self.assertCountEqual(re.findall(r'id="(proper-[^"]+)"', rendered), [f"proper-{key}" for key in keys])
        self.assertIn('id="proper-collect" data-label="proper-collect"></span><strong>Collect:</strong>', rendered)
        self.assertIn('id="proper-communion-jn10" data-label="proper-communion-jn10"></span><strong>Second alternative:</strong>', rendered)
        self.assertIn('href="#proper-collect"', rendered)
        self.assertIn('href="#proper-communion-jn10"', rendered)
        self.assertIn('id="ordinary-label"', rendered)

    def test_schema_two_ten_1962_labels_do_not_depend_on_heading_names(self) -> None:
        keys = ("introit", "collect", "epistle", "gradual", "alleluia", "gospel",
                "offertory", "secret", "communion", "postcommunion")
        body = "\n\n".join(
            rf"\subsection{{Text {index}}}\label{{proper-{key}}} Appointed text."
            for index, key in enumerate(keys)
        )
        markdown = self.convert(body, proper=True, proper_schema=2, element_keys=keys)
        self.assertCountEqual(DRIVER.rendered_markdown_anchors(markdown), [
            "subject", "body", *(f"proper-{key}" for key in keys),
        ])

    def test_schema_two_adjacent_labels_survive_as_distinct_ids(self) -> None:
        markdown = self.convert(
            r"\subsection{Grouped}\label{proper-entrance}\label{proper-collect} Text.",
            proper=True, proper_schema=2, element_keys=("entrance", "collect"),
        )
        anchors = DRIVER.rendered_markdown_anchors(markdown)
        self.assertEqual(anchors.count("proper-entrance"), 1)
        self.assertEqual(anchors.count("proper-collect"), 1)

    def test_schema_two_rejects_title_and_site_normalized_heading_collisions(self) -> None:
        body = (r"\section{Appointed texts} Introduction." "\n\n"
                r"\label{proper-collect}\textbf{Collect:} Prayer.")
        for title, extra in (
            ("Proper collect", ""),
            ("Subject", "\n\n" + r"\subsection{Próper collect} Other text."),
        ):
            with self.subTest(title=title, extra=extra):
                with self.assertRaises(DRIVER.ConversionError) as raised:
                    self.convert(body + extra, title=title, proper=True, proper_schema=2, element_keys=("collect",))
                self.assertIn("duplicate schema-2 rendered proper anchor(s): proper-collect", str(raised.exception))

    def test_schema_two_rejects_unresolved_proper_links_with_styled_text(self) -> None:
        for text in ("the Collect", r"\textbf{the Collect}", r"\emph{the \textbf{Collect}}"):
            with self.subTest(text=text):
                with self.assertRaises(DRIVER.ConversionError) as raised:
                    self.convert(
                        r"\subsection{Collect}\label{proper-collect} Prayer. "
                        + rf"See \hyperref[proper-typo]{{{text}}}.",
                        proper=True, proper_schema=2, element_keys=("collect",),
                    )
                self.assertIn("unresolved schema-2 proper fragment(s): proper-typo", str(raised.exception))

    def test_schema_two_requires_the_site_renderer_dependency_lock(self) -> None:
        for behavior, message in (
            ({"return_value": "0.invalid"}, "does not match the bound dependency lock"),
            ({"side_effect": PackageNotFoundError("Markdown")}, "Python Markdown is required"),
        ):
            with self.subTest(behavior=behavior), mock.patch("_markdown_render.distribution_version", **behavior):
                with self.assertRaises(DRIVER.ConversionError) as raised:
                    self.convert(
                        r"\subsection{Collect}\label{proper-collect} Prayer.",
                        proper=True, proper_schema=2, element_keys=("collect",),
                    )
            self.assertIn("schema-2 site-rendered anchor audit failed", str(raised.exception))
            self.assertIn(message, str(raised.exception))

    def test_schema_two_requires_exact_active_source_label_coverage(self) -> None:
        for body, failure in (
            (r"\subsection{Collect} Prayer.", "missing"),
            ("% \\label{proper-collect}\nPrayer.", "missing"),
            (r"\subsection{Prayer}\label{proper-collect}\label{proper-collect} Prayer.", "duplicate"),
            (r"\subsection{Prayer}\label{proper-collect}\label{proper-other} Prayer.", "undeclared"),
        ):
            with self.subTest(body=body), self.assertRaises(DRIVER.ConversionError) as raised:
                self.convert(body, proper=True, proper_schema=2, element_keys=("collect",))
            self.assertIn(f"{failure} schema-2 source proper anchor", str(raised.exception))

    def test_schema_two_rejects_labels_dropped_by_a_macro_and_code_decoys(self) -> None:
        for decoy in ("", r'\texttt{<span id="proper-collect"></span>}'):
            with self.subTest(decoy=decoy), self.assertRaises(DRIVER.ConversionError) as raised:
                self.convert(
                    r"\discard{\label{proper-collect}} Prayer. " + decoy,
                    preamble=r"\newcommand{\discard}[1]{}", proper=True,
                    proper_schema=2, element_keys=("collect",),
                )
            self.assertIn("missing schema-2 rendered proper anchor", str(raised.exception))

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
        # The semantic definition-list dialect is deliberately limited to
        # schema-2 proper studies, so established non-proper output does not
        # change underneath already reviewed web editions.
        self.assertNotRegex(markdown, r"(?m)^:\s+Born at Corps\.$")

    def test_schema_two_proper_preserves_contents_at_its_source_position(self) -> None:
        markdown = self.convert(
            r"\label{proper-introit}" "\nOpening paragraph.\n\n"
            r"\tableofcontents"
            "\n\n"
            r"\section{Second part}"
            "\nSecond paragraph.\n",
            proper=True,
            proper_schema=2,
            element_keys=("introit",),
        )
        self.assertEqual(markdown.count("[TOC]"), 1)
        self.assertLess(markdown.index("Opening paragraph."), markdown.index("[TOC]"))
        self.assertLess(markdown.index("[TOC]"), markdown.index("## Second part"))

    def test_nonproper_contents_keeps_the_legacy_omission(self) -> None:
        markdown = self.convert(
            r"\tableofcontents" "\n\n" r"\section{Second part}" "\nText.\n"
        )
        self.assertNotIn("[TOC]", markdown)
        self.assertIn("## Second part", markdown)

    @unittest.skipUnless(importlib.util.find_spec("markdown"), "Python Markdown is not installed")
    def test_four_senses_render_as_definition_terms_after_site_rewriting(self) -> None:
        labels = ("Literal.", "Allegorical.", "Moral.", "Anagogical.")
        items = "\n\n".join(
            rf"\item[{label}] The {label[:-1].lower()} body." for label in labels
        )
        markdown = self.convert(
            "\\label{proper-introit}\n\\begin{fourSenses}\n"
            + items
            + "\n\\end{fourSenses}\n",
            preamble=(
                r"\newenvironment{fourSenses}"
                r"{\begin{description}[style=nextline,leftmargin=0pt]}"
                r"{\end{description}}"
            ),
            proper=True,
            proper_schema=2,
            element_keys=("introit",),
        )
        for label in labels:
            self.assertRegex(markdown, rf"(?m)^{re.escape(label)}$")
        self.assertEqual(len(re.findall(r"(?m)^:\s+The .* body\.$", markdown)), 4)

        site = runpy.run_path(str(ROOT / "tools/public-alpha"))
        rendered = site["render_page"](
            "web/test/studies/subject.md", markdown, "subject.html", True, {}
        )
        self.assertEqual(rendered.count("<dt>"), 4)
        self.assertEqual(rendered.count("<dd>"), 4)
        self.assertIn("<dt>Literal.</dt>", rendered)
        self.assertRegex(rendered, r"<dd>\s*<p>The literal body\.</p>\s*</dd>")
        self.assertNotIn("Literal.<br>", rendered)

    def test_generated_chronology_annotation_keeps_its_complete_payload(self) -> None:
        definitions = (
            r"\newcommand{\chronologyannotationclaim}[6]{#6}"
            "\n"
            r"\newcommand{\chronologyannotationcomparisonclaim}[8]{#8}"
            "\n"
            r"\newcommand{\chronologyannotationreach}[3]{}"
            "\n"
            r"\newcommand{\chronologyannotationgroup}[3]{#3}"
            "\n"
            r"\newcommand{\chronologyannotationcomparisongroup}[4]{#4}"
            "\n"
            r"\newcommand{\chronologyannotation}[1]{%"
            "\n"
            r"  \ifcsname triptychchronologyannotation@#1\endcsname"
            "\n"
            r"    \csname triptychchronologyannotation@#1\endcsname"
            "\n"
            r"  \fi}"
            "\n"
            r"\expandafter\def\csname triptychchronologyannotation@gospel\endcsname{%"
            "\n"
            r"\chronologyannotationgroup{composition}{disputed}{Composition -- disputed: "
            r"\chronologyannotationreach{Luke.7.11}{Luke}{true}"
            r"\chronologyannotationclaim{composition.gospel-of-luke}{composition}"
            r"{catholic-traditional-v1}{disputed}{About the year 70}{c. A.D. 70}; "
            r"\chronologyannotationclaim{composition.gospel-of-luke}{composition}"
            r"{catholic-traditional-v1}{disputed}{before Rome}{Before Rome}.}%"
            "\n"
            r"\space \chronologyannotationgroup{narrated-event}{preferred}{Event: "
            r"\chronologyannotationclaim{life-of-christ.naim}{narrated-event}"
            r"{catholic-traditional-v1}{preferred}{derived A.D. 27}{A.D. 27}.}%"
            "\n}"
        )
        for bold in (False, True):
            with self.subTest(bold_labels=bold):
                preamble = definitions
                if bold:
                    preamble = preamble.replace(
                        "{Composition --", r"{\textbf{Composition} --"
                    ).replace("{Event: ", r"{\textbf{Event}: ")
                markdown = self.convert(
                    r"\chronologyannotation{gospel}", preamble=preamble
                )
                marker = "**" if bold else ""
                self.assertIn(
                    f"{marker}Composition{marker} – disputed: c. A.D. 70; Before Rome.",
                    markdown,
                )
                self.assertIn(f"{marker}Event{marker}: A.D. 27.", markdown)
                self.assertNotIn("triptychchronologyannotation@", markdown)

    def test_generated_profile_comparison_keeps_display_and_hides_metadata(self) -> None:
        definitions = (
            r"\newcommand{\chronologyannotationcomparisonclaim}[8]{#8}"
            "\n"
            r"\newcommand{\chronologyannotationcomparisongroup}[4]{#4}"
            "\n"
            r"\newcommand{\chronologyannotation}[1]{%"
            "\n"
            r"  \ifcsname triptychchronologyannotation@#1\endcsname"
            "\n"
            r"    \csname triptychchronologyannotation@#1\endcsname"
            "\n"
            r"  \fi}"
            "\n"
            r"\expandafter\def\csname triptychchronologyannotation@gospel\endcsname{%"
            "\n"
            r"\chronologyannotationcomparisongroup{catholic-critical-v1}"
            r"{composition}{preferred}{Critical comparison: "
            r"\chronologyannotationcomparisonclaim{critical.gospel-of-matthew}"
            r"{composition}{catholic-critical-v1}{catholic-critical-v1}"
            r"{preferred}{passage.usccb.matthew}{post-A.D. 70 date}"
            r"{Post-A.D. 70 date}.}%"
            "\n}"
        )
        markdown = self.convert(
            r"\chronologyannotation{gospel}", preamble=definitions
        )
        self.assertIn("Critical comparison: Post-A.D. 70 date.", markdown)
        self.assertNotIn("critical.gospel-of-matthew", markdown)
        self.assertNotIn("passage.usccb.matthew", markdown)
        self.assertNotIn("chronologyannotationcomparison", markdown)

    def test_generated_chronology_annotation_without_definition_is_refused(self) -> None:
        with self.assertRaises(DRIVER.ConversionError) as raised:
            self.convert(r"\chronologyannotation{gospel}")
        self.assertIn(
            "no generated chronology annotation for: gospel", str(raised.exception)
        )

    def test_unknown_macro_names_its_file_and_writes_nothing(self) -> None:
        with self.assertRaises(DRIVER.ConversionError) as raised:
            self.convert(r"Prose \dubiousclaim{silently deleted evidence}.")
        message = str(raised.exception)
        self.assertIn(r"unknown macro \dubiousclaim", message)
        self.assertIn("main.tex", message)

    def convert_proper_title(self, body: str, *, shim: Path | None = None) -> str:
        """Convert under the real print \\propertitle, which the shim must override."""
        files = {"propers-format.tex": (ROOT / "src/common/propers-format.tex").read_text(
            encoding="utf-8")}
        preamble = r"\input{studies/subject/propers-format}"
        if shim is None:
            return self.convert(body, preamble=preamble, files=files)
        with mock.patch.object(DRIVER, "SHIM", shim):
            return self.convert(body, preamble=preamble, files=files)

    def test_proper_title_sets_all_four_fields_in_print_order(self) -> None:
        markdown = self.convert_proper_title(PROPER_TITLE)
        self.assertIn(
            "**The Eighteenth Sunday after Pentecost**\n\n"
            "Dominica decima octava post Pentecosten\n\n"
            "Missale Romanum 1962 · Proper of Time\n\n"
            "Peace for the city:<br>\na study of the proper in three readings\n\n"
            "The Eighteenth Sunday after Pentecost, ",
            markdown,
        )

    def test_proper_title_omits_an_empty_optional_field(self) -> None:
        for fields in (("Title", "Subtitle", "", "Occasion"),
                       ("Title", "Subtitle", "Edition", ""),
                       ("Title", "", "", "")):
            with self.subTest(fields=fields):
                markdown = self.convert_proper_title(
                    r"\propertitle" + "".join("{" + field + "}" for field in fields)
                    + "\n\nProse."
                )
                self.assertIn(
                    "\n\n".join(["**Title**", *filter(None, fields[1:]), "Prose."]) + "\n",
                    markdown,
                )

    def test_print_title_definition_pandoc_cannot_expand_is_refused(self) -> None:
        # Without the shim's definition, the print macro's empty-field tests
        # govern, and pandoc drops the second and third lines without a warning.
        shim_text, removed = re.subn(
            r"(?m)^\\newcommand\{\\propertitle\}.*\n", "",
            DRIVER.SHIM.read_text(encoding="utf-8"),
        )
        self.assertEqual(removed, 1)
        with tempfile.TemporaryDirectory() as temporary:
            shim = Path(temporary) / "web-shim.tex"
            shim.write_text(shim_text, encoding="utf-8")
            with self.assertRaises(DRIVER.ConversionError) as raised:
                self.convert_proper_title(PROPER_TITLE, shim=shim)
        self.assertIn(
            r"\propertitle title block not set as its 4 declared line(s) in order "
            "(expected 1, found 0): line(s) absent: "
            "Dominica decima octava post Pentecosten; "
            r"Missale Romanum 1962 \quad·\quad Proper of Time",
            str(raised.exception),
        )

    def convert_shared_dossier(self, body: str, *, shared: bool = True) -> str:
        """Convert a schema-2 leaf under the real shared proper format."""
        options = dict(
            preamble=r"\input{studies/subject/propers-format}",
            files={"propers-format.tex": (ROOT / "src/common/propers-format.tex").read_text(
                encoding="utf-8")},
            proper=True, proper_schema=2, element_keys=("collect",),
        )
        if not shared:
            return self.convert(body, **options)
        # The graph gate has its own tests; here it accepts the synthetic leaf.
        with mock.patch("_proper_components.include_graph",
                        side_effect=lambda main, leaf, root: {
                            path.resolve() for path in leaf.rglob("*.tex")}):
            return self.convert(body, format_contract="propers-format-v1", **options)

    @unittest.skipUnless(importlib.util.find_spec("markdown"), "Python Markdown is not installed")
    def test_shared_format_dossier_notes_are_set_full_width_beneath_their_row(self) -> None:
        body = (
            r"\subsection{Prayer}\label{proper-collect} Prayer." "\n\n"
            r"\begin{dossiertable}" "\n"
            r"Collect & Ps 1:1 & Nowhere named & Undated\\" "\n"
            r"\cmidrule(lr){1-4}" "\n"
            r"\dossierevent{Narrated event: none recorded.}" "\n"
            r"\cmidrule(lr){1-4}" "\n"
            r"\dossierprose{A note the print sets across all four columns.}" "\n"
            r"\midrule" "\n"
            r"Gospel & Mt 1:1 & Bethlehem & Dated\\" "\n"
            r"\cmidrule(lr){1-4}" "\n"
            r"\dossierprose{The last note, after which no table resumes.}" "\n"
            r"\end{dossiertable}"
        )
        markdown = self.convert_shared_dossier(body)
        flat = re.sub(r" {2,}", " ", markdown)
        header = DOSSIER_HEADER
        self.assertIn(
            "| Collect | Ps 1:1 | Nowhere named | Undated |\n\n"
            "*Narrated event: none recorded.*\n\n"
            "A note the print sets across all four columns.\n\n" + header,
            flat,
        )
        self.assertIn(
            "| Gospel | Mt 1:1 | Bethlehem | Dated |\n\n"
            "The last note, after which no table resumes.\n\n**Last revised",
            flat,
        )
        self.assertEqual(flat.count(header), 2)
        site = runpy.run_path(str(ROOT / "tools/public-alpha"))
        rendered = site["render_page"]("web/test/studies/subject.md", markdown, "subject.html", True, {})
        self.assertIn("</table>\n<p><em>Narrated event: none recorded.</em></p>", rendered)
        # A leaf that defines its own dossier keeps the padded-row handling.
        legacy = self.convert_shared_dossier(body, shared=False)
        self.assertRegex(
            legacy, r"(?m)^\| A note the print sets across all four columns\. +\|(?: +\|){3}$"
        )
        self.assertEqual(re.sub(r" {2,}", " ", legacy).count(header), 1)

    def test_commented_out_dossier_notes_never_reach_the_output(self) -> None:
        table = (
            r"\begin{dossiertable}" "\n"
            r"Collect & Ps 1:1 & Nowhere named & Undated\\ % a row's aside" "\n"
            r"% \dossierprose{A withdrawn note.}" "\n"
            r"  %\dossierevent{A withdrawn event.}" "\n"
            r"% \dossierprose{A withdrawn note" "\n"
            r"% across two lines.}" "\n"
            r"\dossierprose{A live note keeps its 50\% % and loses this aside" "\n"
            r"and every word after it.}" "\n"
            r"\midrule" "\n"
            r"Gospel & Mt 1:1 & Bethlehem & Dated\\" "\n"
            r"\end{dossiertable}"
        )
        # A commented-out opening must not pair with the live table's end.
        for opening in ("", "% \\begin{dossiertable} A withdrawn table opening.\n"):
            body = r"\subsection{Prayer}\label{proper-collect} Prayer." "\n\n" + opening + table
            with self.subTest(opening=opening):
                flat = re.sub(r" {2,}", " ", self.convert_shared_dossier(body))
                self.assertNotIn("withdrawn", flat)
                self.assertNotIn("aside", flat)
                self.assertIn(
                    "| Collect | Ps 1:1 | Nowhere named | Undated |\n\n"
                    "A live note keeps its 50% and every word after it.\n\n" + DOSSIER_HEADER,
                    flat,
                )
                self.assertIn("| Gospel | Mt 1:1 | Bethlehem | Dated |\n", flat)
                self.assertEqual(flat.count(DOSSIER_HEADER), 2)

    def test_dossier_segment_of_only_comments_or_page_control_is_not_published(self) -> None:
        for trailer in ("% A closing remark.", r"\newpage", "\\newpage\n% A closing remark.",
                        r"\clearpage", r"\Needspace{4\baselineskip}"):
            body = (
                r"\subsection{Prayer}\label{proper-collect} Prayer." "\n\n"
                r"\begin{dossiertable}" "\n"
                r"Collect & Ps 1:1 & Nowhere named & Undated\\" "\n"
                r"\dossierprose{The last note.}" "\n"
                + trailer + "\n"
                r"\end{dossiertable}"
            )
            with self.subTest(trailer=trailer):
                flat = re.sub(r" {2,}", " ", self.convert_shared_dossier(body))
                self.assertIn("The last note.\n\n**Last revised", flat)
                self.assertEqual(flat.count(DOSSIER_HEADER), 1)

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

    def test_dropped_or_changed_path_locator_is_reported(self) -> None:
        body = r"See \path{research/source_record-v1.md}."
        for output in ("", "`research/source_record-v2.md`"):
            with self.subTest(output=output):
                failures = DRIVER.audit_output(body, self.minimal_markdown() + output)
                self.assertIn(
                    r"\path payload dropped: research/source_record-v1.md", failures
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

    def test_raw_generated_chronology_token_is_reported(self) -> None:
        failures = DRIVER.audit_output(
            "Prose.",
            self.minimal_markdown()
            + "\ntriptychchronologyannotation@gospel "
            + "triptychchronologyannotation@gospel\n",
        )
        self.assertTrue(
            any(
                failure.startswith("raw generated chronology annotation token(s)")
                for failure in failures
            )
        )

    def test_missing_generated_chronology_payload_is_reported(self) -> None:
        failures = DRIVER.audit_output(
            "Prose.",
            self.minimal_markdown(),
            chronology_annotations=["Composition: Before c. 165 B.C."],
        )
        self.assertIn(
            "generated chronology annotation payload shortfall: expected 1, found 0: "
            "Composition: Before c. 165 B.C.",
            failures,
        )

    def test_bold_chronology_labels_do_not_hide_a_dropped_date(self) -> None:
        failures = DRIVER.audit_output(
            "Prose.",
            self.minimal_markdown() + "\n**Composition**: Before c. B.C.\n",
            chronology_annotations=[r"\textbf{Composition}: Before c. 165 B.C."],
        )
        self.assertIn(
            "generated chronology annotation payload shortfall: expected 1, found 0: "
            "Composition: Before c. 165 B.C.",
            failures,
        )

    def test_smart_apostrophe_does_not_hide_a_real_chronology_shortfall(self) -> None:
        annotation = (
            r"\textbf{Traditional attribution}: Isaias (ministry in Souvay's "
            r"traditional account), B.C. 740--701."
        )
        rendered_payload = (
            "\n**Traditional attribution**: Isaias (ministry in Souvay’s "
            "traditional account), B.C. 740–701.\n"
        )
        failures = DRIVER.audit_output(
            "Prose.",
            self.minimal_markdown() + rendered_payload,
            chronology_annotations=[annotation],
        )
        self.assertFalse(
            any("generated chronology annotation payload shortfall" in item for item in failures),
            failures,
        )

        failures = DRIVER.audit_output(
            "Prose.",
            self.minimal_markdown()
            + "\n**Traditional attribution**: Isaias (ministry in Souvay’s "
            "traditional account).\n",
            chronology_annotations=[annotation],
        )
        self.assertIn(
            "generated chronology annotation payload shortfall: expected 1, found 0: "
            "Traditional attribution: Isaias (ministry in Souvay's traditional "
            "account), B.C. 740-701.",
            failures,
        )

    def test_dropped_bracketed_macro_payload_is_reported(self) -> None:
        definitions, bracketed = DRIVER.guard_opening_brackets(
            r"\newcommand{\notread}[1]{[\textit{#1}]}"
            "\n"
            r"\newcommand\sic{[sic]}"
            "\n"
            r"\newcommand{\work}[1]{\textit{#1}}"
        )
        self.assertIn(r"\newcommand{\notread}[1]{{}[\textit{#1}]}", definitions)
        self.assertIn(r"\newcommand\sic{{}[sic]}", definitions)
        self.assertEqual(sorted(bracketed), ["notread", "sic"])
        body = (
            r"\notread{And a certain woman did hear:} whose heart. "
            r"\notread{And a certain woman did hear:} again. Writ\sic."
        )
        failures = DRIVER.audit_output(
            body,
            self.minimal_markdown() + "\n> whose heart. \\[*And a certain woman "
            "did hear:*\\] again. Writ.\n",
            bracketed=bracketed,
        )
        self.assertIn(
            "bracketed macro payload dropped (expected 2, found 1): "
            r"\notread{And a certain woman did hear:}",
            failures,
        )
        self.assertIn(
            r"bracketed macro payload dropped (expected 1, found 0): \sic", failures
        )
        failures = DRIVER.audit_output(
            body,
            self.minimal_markdown() + "\n> \\[*And a certain woman did hear:*\\] "
            "whose heart. \\[*And a certain woman did hear:*\\] again. "
            "Writ\\[sic\\].\n",
            bracketed=bracketed,
        )
        self.assertEqual(failures, [])

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

    def test_dropped_title_line_is_reported_though_its_words_recur_in_prose(self) -> None:
        body = (
            r"\propertitle{The Eighteenth Sunday after Pentecost}"
            r"{Dominica decima octava post Pentecosten}"
            r"{Missale Romanum 1962 · Proper of Time}{Peace for the city:\\ a study}"
            "\n\nThe Eighteenth Sunday after Pentecost, "
            r"\latin{Dominica decima octava post Pentecosten}, is a Sunday."
        )
        prose = (
            "\nThe Eighteenth Sunday after Pentecost, *Dominica decima octava "
            "post Pentecosten*, is a Sunday.\n"
        )
        failures = DRIVER.audit_output(
            body,
            self.minimal_markdown()
            + "\n**The Eighteenth Sunday after Pentecost**\n\n"
            "Peace for the city:<br>\na study\n" + prose,
        )
        self.assertIn(
            r"\propertitle title block not set as its 4 declared line(s) in order "
            "(expected 1, found 0): line(s) absent: "
            "Dominica decima octava post Pentecosten; "
            "Missale Romanum 1962 · Proper of Time",
            failures,
        )
        failures = DRIVER.audit_output(
            body,
            self.minimal_markdown()
            + "\n**The Eighteenth Sunday after Pentecost**\n\n"
            "Dominica decima octava post Pentecosten\n\n"
            "Missale Romanum 1962 · Proper of Time\n\n"
            "Peace for the city:<br>\na study\n" + prose,
        )
        self.assertEqual(failures, [])

    def test_reordered_or_merged_title_lines_are_reported(self) -> None:
        body = r"\weektitle{Ninth Sunday}{\latin{Dominica Nona} · II classis}{Missale, pp.~388--389}"
        for output in (
            "\n*Dominica Nona* · II classis\n\n**Ninth Sunday**\n\nMissale, pp. 388–389\n",
            "\n**Ninth Sunday** *Dominica Nona* · II classis\n\nMissale, pp. 388–389\n",
        ):
            with self.subTest(output=output):
                failures = DRIVER.audit_output(body, self.minimal_markdown() + output)
                self.assertTrue(any(
                    failure.startswith(r"\weektitle title block not set as its 3 declared")
                    for failure in failures
                ), failures)
        faithful = "\n**Ninth Sunday**\n\n*Dominica Nona* · II classis\n\nMissale, pp. 388–389\n"
        self.assertEqual(DRIVER.audit_output(body, self.minimal_markdown() + faithful), [])

    def test_empty_optional_title_field_expects_no_line(self) -> None:
        body = r"\propertitle{Title}{}{Edition}{}"
        self.assertEqual(
            DRIVER.audit_output(body, self.minimal_markdown() + "\n**Title**\n\nEdition\n"), []
        )

    def test_header_only_table_is_reported(self) -> None:
        for table in ("| **A** | **B** |\n|:--|:--|\n\nNext.\n",
                      "> | **A** | **B** |\n> |:--|:--|\n",
                      "| **A** | **B** |\n|:--|:--|\n"):
            with self.subTest(table=table):
                failures = DRIVER.audit_output("Prose.", self.minimal_markdown() + "\n" + table)
                self.assertIn("1 table(s) written with a header row and no body row", failures)

    def test_tex_comments_are_stripped_as_tex_and_pandoc_read_them(self) -> None:
        for text, expected in (
            ("50\\% kept", "50\\% kept"),
            ("row\\\\% gone", "row\\\\"),
            ("\\url{https://example.invalid/a%20b} % gone", "\\url{https://example.invalid/a%20b} "),
            ("a\n% whole line\nb", "a\nb"),
            ("a % trailing\nb", "a \nb"),
        ):
            with self.subTest(text=text):
                self.assertEqual(DRIVER.strip_tex_comments(text), expected)
                masked = DRIVER.mask_tex_comments(text)
                self.assertEqual(len(masked), len(text))
                self.assertNotIn("gone", masked)
                self.assertNotIn("whole", masked)

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
