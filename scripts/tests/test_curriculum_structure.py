#!/usr/bin/env python3
"""Regression tests for rendered Ecclesiastical Latin hierarchy checks."""

from __future__ import annotations

import importlib.machinery
import importlib.util
import sys
import tempfile
import unittest
from dataclasses import replace
from pathlib import Path
from xml.sax.saxutils import escape


ROOT = Path(__file__).resolve().parents[2]
CHECKER_PATH = ROOT / "scripts" / "check-curriculum-structure"
LOADER = importlib.machinery.SourceFileLoader(
    "triptych_curriculum_structure_checker", str(CHECKER_PATH)
)
SPEC = importlib.util.spec_from_loader(LOADER.name, LOADER)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError(f"cannot load {CHECKER_PATH}")
CHECKER = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = CHECKER
SPEC.loader.exec_module(CHECKER)


def part(ordinal: int, title: str, page: str = "1"):
    return CHECKER.TocEntry(
        "part",
        f"{CHECKER._roman(ordinal)}\\hspace {{1em}}{title}",
        f"part.{ordinal}",
        None,
        page,
    )


def chapter(
    number: int | None, title: str, destination: str, page: str = "1"
):
    return CHECKER.TocEntry(
        "chapter", title, destination, None if number is None else str(number), page
    )


def section(
    number: str | None, title: str, destination: str, page: str = "1"
):
    return CHECKER.TocEntry("section", title, destination, number, page)


def bookmarks(entries):
    current = {}
    result = []
    for entry in entries:
        if entry.kind == "part":
            parent = ""
            current = {"part": entry.destination}
        else:
            parent_kind = CHECKER.PARENT_KIND[entry.kind]
            parent = current[parent_kind]
            current[entry.kind] = entry.destination
        result.append(
            CHECKER.Bookmark(
                CHECKER.BOOKMARK_LEVEL[entry.kind], entry.destination, parent
            )
        )
    return result


def contents_bbox(
    positioned_entries,
    *,
    new_page_destinations=(),
    wrapped_destinations=(),
    wrapped_first_line_words=None,
    wrapped_continuation_x=None,
):
    """Build small Poppler-like bbox XHTML for rendered Contents rows."""
    page_rows = [[]]
    part_ordinal = 0
    new_pages = set(new_page_destinations)
    wrapped = set(wrapped_destinations)
    first_line_words = dict(wrapped_first_line_words or {})
    continuation_x = dict(wrapped_continuation_x or {})
    for entry, gutter_x, title_x in positioned_entries:
        if entry.destination in new_pages and page_rows[-1]:
            page_rows.append([])
        if entry.kind == "part":
            part_ordinal += 1
            number = CHECKER._roman(part_ordinal)
            title = CHECKER._part_title(entry, part_ordinal, [])
        else:
            number = entry.number
            title = CHECKER._plain_title(entry.title)
        page_rows[-1].append(
            (entry.destination, number, title, gutter_x, title_x)
        )

    pages = []
    for rows in page_rows:
        lines = [
            '<line><word xMin="520" yMin="20">Contents</word></line>'
        ]
        y_min = 100.0
        for destination, number, title, gutter_x, title_x in rows:
            words = title.split()
            wrap_after = first_line_words.get(destination, 4)
            first_line = words[:wrap_after] if destination in wrapped else words
            later_line = words[wrap_after:] if destination in wrapped else []
            rendered = []
            if number is not None:
                rendered.append((number, gutter_x))
            next_x = title_x
            for word in first_line:
                rendered.append((word, next_x))
                next_x += max(8.0, len(word) * 5.0 + 3.0)
            lines.append(
                "<line>"
                + "".join(
                    f'<word xMin="{x_min:.3f}" yMin="{y_min:.3f}">'
                    f"{escape(word)}</word>"
                    for word, x_min in rendered
                )
                + "</line>"
            )
            if later_line:
                next_x = continuation_x.get(destination, title_x)
                lines.append(
                    "<line>"
                    + "".join(
                        f'<word xMin="{next_x + offset * 30.0:.3f}" '
                        f'yMin="{y_min + 9.0:.3f}">{escape(word)}</word>'
                        for offset, word in enumerate(later_line)
                    )
                    + "</line>"
                )
                y_min += 9.0
            y_min += 12.0
        pages.append("<page><flow><block>" + "".join(lines) + "</block></flow></page>")
    return "<html><body><doc>" + "".join(pages) + "</doc></body></html>"


def generic_entries():
    return [
        part(1, "First Part", "1"),
        chapter(1, "First chapter", "chapter.1.1", "1"),
        section("1.1", "First section", "section.1.1.1", "1"),
        chapter(2, "Second chapter", "chapter.1.2", "2"),
        part(2, "Second Part", "3"),
        chapter(1, "Third chapter", "chapter.2.1", "3"),
        section("1.1", "Another section", "section.2.1.1", "3"),
    ]


def module_entries():
    unit_one = r"Unit I.1: Form, function, and \Latin {sum}"
    unit_two = r"Unit I.2: Case, agreement, and a first reading"
    entries = [
        part(1, "Teaching"),
        chapter(1, unit_one, "chapter.1.1", "1"),
        section("1.1", r"The indicative of \Latin {sum}", "section.1.1.1", "1"),
        chapter(2, unit_two, "chapter.1.2", "3"),
        section("2.1", "Case and agreement", "section.1.2.1", "3"),
        part(2, "Memory Work", "5"),
        chapter(1, "Vocabulary and forms for M01", "chapter.2.1", "5"),
        part(3, "Reading and Composition", "7"),
        chapter(1, "Connected Latin and controlled composition", "chapter.3.1", "7"),
        part(4, "Cumulative Practice", "10"),
        chapter(1, unit_one, "chapter.4.1", "10"),
    ]
    for offset, variant in enumerate("ABCD", 11):
        entries.append(
            section(
                None,
                f"Worksheet I.1 — Variant {variant}",
                f"section*.worksheet-i1-{variant.lower()}",
                str(offset),
            )
        )
    entries.append(chapter(2, unit_two, "chapter.4.2", "15"))
    for offset, variant in enumerate("ABCD", 16):
        entries.append(
            section(
                None,
                f"Worksheet I.2 — Variant {variant}",
                f"section*.worksheet-i2-{variant.lower()}",
                str(offset),
            )
        )
    entries.extend(
        (
            chapter(3, "Before continuing", "chapter.4.3", "20"),
            part(5, "Answers and Models", "21"),
            chapter(1, "Memory-work answers", "chapter.5.1", "21"),
            chapter(2, "Reading and composition models", "chapter.5.2", "22"),
            chapter(3, unit_one, "chapter.5.3", "23"),
        )
    )
    for offset, variant in enumerate("ABCD", 24):
        entries.append(
            section(
                None,
                f"Solution I.1 — Variant {variant}",
                f"section*.solution-i1-{variant.lower()}",
                str(offset),
            )
        )
    entries.append(chapter(4, unit_two, "chapter.5.4", "28"))
    for offset, variant in enumerate("ABCD", 29):
        entries.append(
            section(
                None,
                f"Solution I.2 — Variant {variant}",
                f"section*.solution-i2-{variant.lower()}",
                str(offset),
            )
        )
    entries.extend(
        (
            part(6, "Scope and Sources", "33"),
            chapter(1, "Scope and Qualifications", "chapter.6.1", "33"),
            chapter(2, "References", "chapter.6.2", "34"),
            chapter(3, "Generation Metadata", "chapter.6.3", "35"),
        )
    )
    return entries


def assessment_entries():
    entries = [
        part(1, "Using This Review"),
        chapter(1, "Purpose and method", "chapter.1.1"),
        chapter(2, "Common self-review method", "chapter.1.2"),
        chapter(3, "Reading the result qualitatively", "chapter.1.3"),
        part(2, "Review Forms"),
        chapter(1, "Foundations Cumulative Review", "chapter.2.1"),
        section(None, "F-A. Foundations, first review", "section*.fa.review"),
        section(None, "F-B. Foundations, later review", "section*.fb.review"),
        part(3, "Answers and Models"),
        chapter(1, "Foundations Cumulative Review", "chapter.3.1"),
        section(None, "F-A. Foundations, first review", "section*.fa.model"),
        section(None, "F-B. Foundations, later review", "section*.fb.model"),
        part(4, "Scope and Sources"),
        chapter(1, "Scope", "chapter.4.1"),
    ]
    return entries


class CurriculumStructureTests(unittest.TestCase):
    generic_document = (
        "curriculums/ecclesiastical-latin/00-reference-grammar"
    )

    def test_parses_balanced_toc_titles_and_bookmarks(self) -> None:
        toc = r"""
\contentsline {part}{I\hspace {1em}First Part}{1}{part.1}%
\contentsline {chapter}{\numberline {1}A \Latin {nested {title}}}{1}{chapter.1}%
\contentsline {section}{\numberline {}Worksheet I.1}{2}{section*.worksheet}%
"""
        out = r"""
\BOOKMARK [0][-]{part.1}{First Part}{}%
\BOOKMARK [1][-]{chapter.1}{A nested title}{part.1}%
"""
        entries = CHECKER.parse_toc(toc)
        parsed_bookmarks = CHECKER.parse_bookmarks(out)
        self.assertEqual(entries[1].number, "1")
        self.assertEqual(entries[1].page, "1")
        self.assertEqual(entries[1].title, r"A \Latin {nested {title}}")
        self.assertIsNone(entries[2].number)
        self.assertEqual(entries[2].title, "Worksheet I.1")
        self.assertEqual(parsed_bookmarks[1].parent, "part.1")

    def test_accepts_chapters_restarting_with_each_part_and_nested_bookmarks(self) -> None:
        entries = generic_entries()
        CHECKER.validate_document(
            self.generic_document, entries, bookmarks(entries)
        )

    def test_rendered_contents_requires_distinct_dotted_chapter_lines(self) -> None:
        entries = generic_entries() + [
            section(None, "Worksheet sample", "section*.1", "3"),
            chapter(2, r"What ``complete'' means", "chapter.2.2", "4"),
        ]
        good = """TRIPTYCH / ECCLESIASTICAL LATIN                 Contents

Contents
I First Part                                                   1
1 First chapter . . . . . . . . . . . . . . . . . . . . .    1
  1.1 First section . . . . . . . . . . . . . . . . . . .    1
2 Second chapter . . . . . . . . . . . . . . . . . . . . .   2
II Second Part                                                 3
1 Third chapter . . . . . . . . . . . . . . . . . . . . .    3
  1.1 Another section . . . . . . . . . . . . . . . . . .    3
  Worksheet sample . . . . . . . . . . . . . . . . . . .    3
2 What “complete” means . . . . . . . . . . . . . . . . .    4

Disce legendo et scribendo                                    i
\fBODY
"""
        CHECKER.validate_toc_rendering(good, entries)
        broken = good.replace(
            "2 Second chapter . . . . . . . . . . . . . . . . . . . . .   2",
            "2 Second chapter2",
        )
        with self.assertRaisesRegex(
            CHECKER.StructureError, "Chapter 2 lacks a dotted leader"
        ):
            CHECKER.validate_toc_rendering(broken, entries)

        broken_section = "\n".join(
            "  1.1 Another section 3"
            if line.lstrip().startswith("1.1 Another section")
            else line
            for line in good.splitlines()
        )
        with self.assertRaisesRegex(CHECKER.StructureError, "Section 1.1 lacks"):
            CHECKER.validate_toc_rendering(broken_section, entries)

        broken_unnumbered = "\n".join(
            "  Worksheet sample 3"
            if line.lstrip().startswith("Worksheet sample")
            else line
            for line in good.splitlines()
        )
        with self.assertRaisesRegex(
            CHECKER.StructureError, "unnumbered section 'Worksheet sample' lacks"
        ):
            CHECKER.validate_toc_rendering(broken_unnumbered, entries)

    def test_learning_module_contents_must_fit_one_physical_page(self) -> None:
        entries = [
            part(1, "First Part", "1"),
            chapter(1, "First chapter", "chapter.1", "1"),
        ]
        one_page = """Contents
I First Part                                                   1
1 First chapter . . . . . . . . . . . . . . . . . . . . .    1
"""
        CHECKER.validate_toc_rendering(
            one_page, entries, require_single_page=True
        )
        spilled = one_page + "\fTRIPTYCH / ECCLESIASTICAL LATIN Contents\n"
        with self.assertRaisesRegex(
            CHECKER.StructureError, "Contents must occupy exactly one physical page"
        ):
            CHECKER.validate_toc_rendering(
                spilled, entries, require_single_page=True
            )

    def test_toc_geometry_accepts_nested_wrapped_and_continued_rows(self) -> None:
        entries = generic_entries()
        entries[1] = replace(
            entries[1], title="First chapter with deliberately wrapped words"
        )
        entries.append(
            section(None, "Worksheet sample", "section*.worksheet", "3")
        )
        chapter_count = 0
        section_count = 0
        positioned = []
        for entry in entries:
            if entry.kind == "part":
                positioned.append((entry, 54.0, 72.0))
            elif entry.kind == "chapter":
                chapter_count += 1
                positioned.append(
                    (entry, 68.0 + chapter_count * 0.2, 93.0 + chapter_count * 0.2)
                )
            elif entry.number is None:
                positioned.append((entry, 111.4, 111.4))
            else:
                section_count += 1
                positioned.append(
                    (entry, 82.0 + section_count * 0.2, 111.0 + section_count * 0.2)
                )
        bbox = contents_bbox(
            positioned,
            new_page_destinations={"part.2"},
            wrapped_destinations={"chapter.1.1"},
        )
        CHECKER.validate_toc_geometry(bbox, entries)

    def test_toc_rows_keep_mixed_style_words_with_their_poppler_line(self) -> None:
        bbox = """<doc><page>
<line yMin="20"><word xMin="520" yMin="20">Contents</word></line>
<line yMin="100"><word xMin="82" yMin="100">4.2</word></line>
<line yMin="100">
  <word xMin="111" yMin="100">First</word>
  <word xMin="140" yMin="100">declension:</word>
  <word xMin="191" yMin="102.6">gratia,</word>
</line>
<line yMin="103">
  <word xMin="82" yMin="103">4.3</word>
  <word xMin="111" yMin="103">Second</word>
</line>
</page></doc>"""
        rows = CHECKER._toc_bbox_rows(bbox)
        self.assertEqual(
            [[word.text for word in row] for row in rows],
            [
                ["Contents"],
                ["4.2", "First", "declension:", "gratia,"],
                ["4.3", "Second"],
            ],
        )

    def test_toc_geometry_accepts_title_wrapped_before_four_word_prefix(self) -> None:
        entries = generic_entries()
        entries[1] = replace(
            entries[1], title="First chapter with deliberately wrapped words"
        )
        positioned = [
            (
                entry,
                54.0
                if entry.kind == "part"
                else 68.0
                if entry.kind == "chapter"
                else 82.0,
                72.0
                if entry.kind == "part"
                else 93.0
                if entry.kind == "chapter"
                else 111.0,
            )
            for entry in entries
        ]
        CHECKER.validate_toc_geometry(
            contents_bbox(
                positioned,
                wrapped_destinations={"chapter.1.1"},
                wrapped_first_line_words={"chapter.1.1": 2},
            ),
            entries,
        )

    def test_toc_geometry_rejects_flush_left_wrapped_continuation(self) -> None:
        entries = generic_entries()
        entries[1] = replace(
            entries[1], title="First chapter with deliberately wrapped words"
        )
        positioned = [
            (
                entry,
                54.0
                if entry.kind == "part"
                else 68.0
                if entry.kind == "chapter"
                else 82.0,
                72.0
                if entry.kind == "part"
                else 93.0
                if entry.kind == "chapter"
                else 111.0,
            )
            for entry in entries
        ]
        with self.assertRaisesRegex(
            CHECKER.StructureError,
            "Chapter 1 wrapped continuation is not aligned with its title column",
        ):
            CHECKER.validate_toc_geometry(
                contents_bbox(
                    positioned,
                    wrapped_destinations={"chapter.1.1"},
                    wrapped_first_line_words={"chapter.1.1": 2},
                    wrapped_continuation_x={"chapter.1.1": 54.0},
                ),
                entries,
            )

    def test_toc_geometry_rejects_flat_chapters(self) -> None:
        entries = generic_entries()
        positioned = [
            (
                entry,
                54.0 if entry.kind in {"part", "chapter"} else 68.0,
                72.0
                if entry.kind == "part"
                else 79.0
                if entry.kind == "chapter"
                else 97.0,
            )
            for entry in entries
        ]
        with self.assertRaisesRegex(
            CHECKER.StructureError,
            "Chapter 1 gutter is not visibly indented beneath Part I",
        ):
            CHECKER.validate_toc_geometry(contents_bbox(positioned), entries)

    def test_toc_geometry_rejects_flat_sections(self) -> None:
        entries = generic_entries()
        positioned = [
            (
                entry,
                54.0
                if entry.kind == "part"
                else 68.0,
                72.0
                if entry.kind == "part"
                else 93.0
                if entry.kind == "chapter"
                else 100.0,
            )
            for entry in entries
        ]
        with self.assertRaisesRegex(
            CHECKER.StructureError,
            "Section 1.1 gutter is not visibly indented beneath Chapter 1",
        ):
            CHECKER.validate_toc_geometry(contents_bbox(positioned), entries)

    def test_toc_geometry_aligns_numbered_and_unnumbered_section_titles(self) -> None:
        entries = generic_entries() + [
            section(None, "Worksheet sample", "section*.worksheet", "3")
        ]
        positioned = []
        for entry in entries:
            if entry.kind == "part":
                positioned.append((entry, 54.0, 72.0))
            elif entry.kind == "chapter":
                positioned.append((entry, 68.0, 93.0))
            elif entry.number is None:
                positioned.append((entry, 82.0, 82.0))
            else:
                positioned.append((entry, 82.0, 111.0))
        with self.assertRaisesRegex(
            CHECKER.StructureError,
            "unnumbered section 'Worksheet sample' title column is not aligned",
        ):
            CHECKER.validate_toc_geometry(contents_bbox(positioned), entries)

    def test_chapter_labels_cannot_be_orphaned_at_the_page_foot(self) -> None:
        entries = [part(1, "First Part"), chapter(1, "First", "chapter.1")]
        template = """<?xml version="1.0" encoding="UTF-8"?>
<doc><page width="612" height="792"><flow><block>
<line xMin="470" yMin="{top}" xMax="558" yMax="{bottom}">
<word xMin="470" yMin="{top}" xMax="540" yMax="{bottom}">CHAPTER</word>
<word xMin="545" yMin="{top}" xMax="558" yMax="{bottom}">1</word>
</line></block></flow></page></doc>
"""
        CHECKER.validate_chapter_positions(
            template.format(top="124", bottom="137"), entries
        )
        with self.assertRaisesRegex(
            CHECKER.StructureError, "too near the page foot"
        ):
            CHECKER.validate_chapter_positions(
                template.format(top="700", bottom="713"), entries
            )

        wrong_number = template.format(top="124", bottom="137").replace(
            ">1</word>", ">2</word>"
        )
        with self.assertRaisesRegex(
            CHECKER.StructureError, "chapter-label sequence differs"
        ):
            CHECKER.validate_chapter_positions(wrong_number, entries)

    def test_rejects_pages_with_only_header_footer_or_rules(self) -> None:
        body_page = """<?xml version="1.0" encoding="UTF-8"?>
<doc><page width="612" height="792"><flow><block>
<line><word yMin="32" yMax="44">HEADER</word></line>
<line><word yMin="110" yMax="122">Body</word></line>
<line><word yMin="748" yMax="760">FOOTER</word></line>
</block></flow></page></doc>
"""
        CHECKER.validate_body_word_pages(body_page)

        header_footer_only = body_page.replace(
            '<line><word yMin="110" yMax="122">Body</word></line>',
            "<line><span /></line>",
        )
        with self.assertRaisesRegex(
            CHECKER.StructureError,
            "physical page 1 has no body words",
        ):
            CHECKER.validate_body_word_pages(header_footer_only)

    def test_rejects_sparse_module_before_continuing_pages(self) -> None:
        def page_with_words(marker: str, total: int) -> str:
            marker_count = len(marker.split())
            self.assertGreaterEqual(total, marker_count)
            return marker + " " + "evidence " * (total - marker_count)

        CHECKER.validate_fragmentary_pages(
            page_with_words("Before continuing", 90), is_module=True
        )
        with self.assertRaisesRegex(
            CHECKER.StructureError,
            "Before continuing but only 89 words; expected at least 90",
        ):
            CHECKER.validate_fragmentary_pages(
                page_with_words("Before continuing", 89), is_module=True
            )

        # The density floor belongs only to learning packets.
        CHECKER.validate_fragmentary_pages(
            page_with_words("Before continuing", 20), is_module=False
        )

    def test_rejects_sparse_worksheet_and_solution_continuations(self) -> None:
        def page_with_words(marker: str, total: int) -> str:
            marker_count = len(marker.split())
            self.assertGreaterEqual(total, marker_count)
            return marker + "\n" + "answer " * (total - marker_count)

        for marker in (
            "TRIPTYCH / ECCLESIASTICAL LATIN Worksheet II.53 — Compression A",
            "TRIPTYCH / ECCLESIASTICAL LATIN Solution III.41 — Requiem A",
        ):
            with self.subTest(marker=marker):
                CHECKER.validate_fragmentary_pages(page_with_words(marker, 80))
                with self.assertRaisesRegex(
                    CHECKER.StructureError,
                    "sparse worksheet/solution continuation with only 79 words",
                ):
                    CHECKER.validate_fragmentary_pages(
                        page_with_words(marker, 79)
                    )

                first_page = marker + "\nWorksheet ID: III.41\nshort form"
                CHECKER.validate_fragmentary_pages(first_page)

        # A body cross-reference is not a continuation-page running head.
        body_reference = "\n".join(
            (
                "Short reference note",
                "First point",
                "Second point",
                "Third point",
                "Fourth point",
                "Fifth point",
                "See Worksheet II.53 for delayed practice.",
            )
        )
        CHECKER.validate_fragmentary_pages(body_reference)

    def test_rejects_the_obsolete_definition_footer_anywhere(self) -> None:
        CHECKER.validate_fragmentary_pages(
            "Worksheet I.1 " + "substantive learner content " * 40
        )
        for page in (
            "Worksheet I.1 " + "substantive learner content " * 40
            + "Definition/error check: record the rule.",
            "TRIPTYCH / ECCLESIASTICAL LATIN\n"
            "Definition / error check: record the rule.\n"
            "Disce legendo et scribendo\n",
        ):
            with self.subTest(page=page), self.assertRaisesRegex(
                CHECKER.StructureError,
                "contains obsolete Definition/error check footer",
            ):
                CHECKER.validate_fragmentary_pages(page)

    def test_course_format_layout_contract_rejects_each_missing_guard(self) -> None:
        path = (
            ROOT
            / "src/gpt/curriculums/ecclesiastical-latin/shared/course-format.sty"
        )
        source = path.read_text(encoding="utf-8")
        CHECKER.validate_course_format_layout(source, path)

        worksheet_start = source.index(r"\NewEnviron{worksheet}")
        worksheet_end = source.index(r"\newcommand{\Exercise}", worksheet_start)
        worksheet_source = source[worksheet_start:worksheet_end]

        def remove_occurrence(token: str, ordinal: int) -> str:
            positions = []
            cursor = 0
            while True:
                position = worksheet_source.find(token, cursor)
                if position < 0:
                    break
                positions.append(position)
                cursor = position + len(token)
            self.assertEqual(len(positions), 2)
            position = positions[ordinal]
            mutated_worksheet = (
                worksheet_source[:position]
                + worksheet_source[position + len(token) :]
            )
            return (
                source[:worksheet_start]
                + mutated_worksheet
                + source[worksheet_end:]
            )

        for token, diagnostic in (
            (
                r"\global\firstcourseworksheetfalse",
                "must globally transition firstcourseworksheetfalse",
            ),
            (
                r"\removelastskip",
                r"must contain \\removelastskip followed by \\clearpage",
            ),
            (
                r"\clearpage",
                r"must contain \\removelastskip followed by \\clearpage",
            ),
        ):
            for ordinal in range(2):
                with (
                    self.subTest(token=token, ordinal=ordinal),
                    self.assertRaisesRegex(CHECKER.StructureError, diagnostic),
                ):
                    CHECKER.validate_course_format_layout(
                        remove_occurrence(token, ordinal), path
                    )

        begin_bank_start = source.index(r"\newcommand{\BeginExerciseBank}")
        begin_bank_end = source.index(
            r"\newcommand{\SelectedWorksheetVariants}", begin_bank_start
        )
        begin_bank_source = source[begin_bank_start:begin_bank_end]
        without_initialization = source.replace(
            begin_bank_source,
            begin_bank_source.replace(r"\firstcourseworksheettrue", "", 1),
            1,
        )
        with self.assertRaisesRegex(
            CHECKER.StructureError,
            "must initialize firstcourseworksheettrue",
        ):
            CHECKER.validate_course_format_layout(without_initialization, path)

        unit_guard_start = source.index(r"\newcommand{\CourseUnitOpeningGuard}")
        unit_guard_end = source.index(r"\NewEnviron{courseunit}", unit_guard_start)
        unit_guard_source = source[unit_guard_start:unit_guard_end]
        without_unit_reset = source.replace(
            unit_guard_source,
            unit_guard_source.replace(
                r"\global\firstcourseworksheettrue", "", 1
            ),
            1,
        )
        with self.assertRaisesRegex(
            CHECKER.StructureError,
            "must reset firstcourseworksheettrue for every selected unit",
        ):
            CHECKER.validate_course_format_layout(without_unit_reset, path)

        courseunit_start = source.index(r"\NewEnviron{courseunit}")
        courseunit_end = source.index(
            r"\newcommand{\Definition}", courseunit_start
        )
        courseunit_source = source[courseunit_start:courseunit_end]
        without_guard_use = source.replace(
            courseunit_source,
            courseunit_source.replace(r"\CourseUnitOpeningGuard", ""),
            1,
        )
        with self.assertRaisesRegex(
            CHECKER.StructureError,
            "must invoke CourseUnitOpeningGuard in both selection branches",
        ):
            CHECKER.validate_course_format_layout(without_guard_use, path)

    def test_course_format_requires_part_qualified_hypertext_destinations(self) -> None:
        path = (
            ROOT
            / "src/gpt/curriculums/ecclesiastical-latin/shared/course-format.sty"
        )
        source = path.read_text(encoding="utf-8")
        CHECKER.validate_course_format_layout(source, path)

        symbolic_part = source.replace(
            r"\def\theHchapter{\arabic{part}.\arabic{chapter}}",
            r"\def\theHchapter{curriculum.\theHpart.\thechapter}",
            1,
        )
        self.assertNotEqual(symbolic_part, source)
        CHECKER.validate_course_format_layout(symbolic_part, path)

        without_part = source.replace(
            r"\def\theHchapter{\arabic{part}.\arabic{chapter}}",
            r"\def\theHchapter{\arabic{chapter}}",
            1,
        )
        with self.assertRaisesRegex(
            CHECKER.StructureError,
            "theHchapter must combine a Part-qualified component",
        ):
            CHECKER.validate_course_format_layout(without_part, path)

        without_chapter_scope = source.replace(
            r"\def\theHsection{\theHchapter.\arabic{section}}",
            r"\def\theHsection{\arabic{part}.\arabic{section}}",
            1,
        )
        with self.assertRaisesRegex(
            CHECKER.StructureError,
            "theHsection must derive from the Part-qualified theHchapter",
        ):
            CHECKER.validate_course_format_layout(without_chapter_scope, path)

    def test_course_format_assessment_contract_rejects_each_missing_guard(self) -> None:
        path = (
            ROOT
            / "src/gpt/curriculums/ecclesiastical-latin/shared/course-format.sty"
        )
        source = path.read_text(encoding="utf-8")
        CHECKER.validate_course_format_layout(source, path)

        without_initialization = source.replace(
            r"\firstcourseassessmenttrue", "", 1
        )
        with self.assertRaisesRegex(
            CHECKER.StructureError,
            "SelectAssessments must initialize firstcourseassessmenttrue",
        ):
            CHECKER.validate_course_format_layout(without_initialization, path)

        assessment_start = source.index(r"\NewEnviron{assessment}")
        assessment_end = source.index(
            r"\newcommand{\AssessmentItem}", assessment_start
        )

        def remove_assessment_token(token: str) -> str:
            region = source[assessment_start:assessment_end]
            self.assertEqual(region.count(token), 1)
            return (
                source[:assessment_start]
                + region.replace(token, "", 1)
                + source[assessment_end:]
            )

        for token, diagnostic in (
            (
                r"\global\firstcourseassessmentfalse",
                "must globally transition firstcourseassessmentfalse",
            ),
            (
                r"\removelastskip",
                r"later assessment path must contain \\removelastskip",
            ),
            (
                r"\clearpage",
                r"later assessment path must contain \\removelastskip",
            ),
        ):
            with (
                self.subTest(token=token),
                self.assertRaisesRegex(CHECKER.StructureError, diagnostic),
            ):
                CHECKER.validate_course_format_layout(
                    remove_assessment_token(token), path
                )

        item_start = source.index(r"\newcommand{\AssessmentItem}")
        item_end = source.index(r"\newcolumntype", item_start)
        item_region = source[item_start:item_end]
        for token in (r"\begin{minipage}[t]{\linewidth}", "#3"):
            with self.subTest(token=token):
                self.assertIn(token, item_region)
                mutated = (
                    source[:item_start]
                    + item_region.replace(token, "", 1)
                    + source[item_end:]
                )
                with self.assertRaisesRegex(
                    CHECKER.StructureError,
                    "AssessmentItem must keep its ID, prompt, response, and answer",
                ):
                    CHECKER.validate_course_format_layout(mutated, path)

    def test_obsolete_definition_footer_is_rejected_in_any_source_record(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "lesson.tex").write_text("Current lesson.\n", encoding="utf-8")
            (root / "research.md").write_text("Current audit.\n", encoding="utf-8")
            CHECKER.validate_obsolete_definition_checks(root)

            (root / "research.md").write_text(
                "Retired label: Definition/error check: do this.\n",
                encoding="utf-8",
            )
            with self.assertRaisesRegex(
                CHECKER.StructureError,
                "research.md: contains obsolete Definition/error check footer",
            ):
                CHECKER.validate_obsolete_definition_checks(root)

    def test_authoritative_source_registry_reconciles_all_publications(self) -> None:
        curriculum_root = ROOT / "src/gpt/curriculums/ecclesiastical-latin"
        result = CHECKER.audit_sources(curriculum_root)
        self.assertEqual(
            result,
            CHECKER.SourceAudit(30, 30, 7, 9),
        )

        rows = CHECKER._registry_rows(curriculum_root)
        CHECKER._validate_registry_shape(rows)
        short_trunk = list(rows)
        module_id, _, worksheets, leaf = short_trunk[0]
        short_trunk[0] = (module_id, "I.1", worksheets, leaf)
        with self.assertRaisesRegex(
            CHECKER.StructureError,
            "must contain two or three common-trunk units|46 stable lessons",
        ):
            CHECKER._validate_registry_shape(short_trunk)

        misplaced_poetry = list(rows)
        module_id, units, worksheets, _ = misplaced_poetry[-1]
        misplaced_poetry[-1] = (
            module_id,
            units,
            worksheets,
            "04-advanced/08-verse-composition",
        )
        with self.assertRaisesRegex(
            CHECKER.StructureError, "non-poetry canonical leaf"
        ):
            CHECKER._validate_registry_shape(misplaced_poetry)

    def test_module_packet_keys_control_memory_reader_and_practice(self) -> None:
        path = (
            ROOT
            / "src/gpt/curriculums/ecclesiastical-latin/01-foundations/"
            "01-form-case-and-agreement/module-data.tex"
        )
        source = CHECKER._strip_tex_comments(path.read_text(encoding="utf-8"))
        CHECKER._validate_module_key_alignment(source, path, "EL-M01")

        for old, new, diagnostic in (
            (
                r"\newcommand{\ModuleIDKey}{M01}",
                r"\newcommand{\ModuleIDKey}{M02}",
                "ModuleIDKey 'M02' != packet key 'M01'",
            ),
            (
                r"\newcommand{\ModuleMemorySet}{M01}",
                r"\newcommand{\ModuleMemorySet}{M02}",
                "ModuleMemorySet 'M02' != packet key 'M01'",
            ),
            (
                r"\newcommand{\ModuleReaderSet}{M01}",
                r"\newcommand{\ModuleReaderSet}{M02}",
                "ModuleReaderSet 'M02' != packet key 'M01'",
            ),
            (
                r"\SelectCourseUnits{M01}",
                r"\SelectCourseUnits{M02}",
                "ModulePractice must select only packet key 'M01'",
            ),
        ):
            with self.subTest(old=old):
                mutated = source.replace(old, new, 1)
                self.assertNotEqual(mutated, source)
                with self.assertRaisesRegex(CHECKER.StructureError, diagnostic):
                    CHECKER._validate_module_key_alignment(
                        mutated, path, "EL-M01"
                    )

    def test_publication_inventory_rejects_every_unregistered_main(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            expected = root / "01-stage/01-module"
            expected.mkdir(parents=True)
            (expected / "main.tex").touch()
            self.assertEqual(
                CHECKER._publication_leaves(root, {"01-stage/01-module"}),
                {"01-stage/01-module"},
            )
            rogue = root / "shared/rogue"
            rogue.mkdir(parents=True)
            (rogue / "main.tex").touch()
            with self.assertRaisesRegex(
                CHECKER.StructureError,
                "unregistered curriculum publication leaf: shared/rogue",
            ):
                CHECKER._publication_leaves(root, {"01-stage/01-module"})

    def test_shared_source_paths_cannot_escape_curriculum_root(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory)
            root = base / "curriculum"
            shared = root / "shared"
            shared.mkdir(parents=True)
            good = shared / "good.tex"
            good.touch()
            diagnostic = root / "module-data.tex"
            self.assertEqual(
                CHECKER._source_path(
                    root, r"\CourseRoot/shared/good", diagnostic
                ),
                good.resolve(),
            )
            for escaped in (
                r"\CourseRoot//etc/passwd",
                r"\CourseRoot/shared/../outside",
            ):
                with self.subTest(escaped=escaped), self.assertRaisesRegex(
                    CHECKER.StructureError, "escapes curriculum root"
                ):
                    CHECKER._source_path(root, escaped, diagnostic)

            outside = base / "outside.tex"
            outside.touch()
            (shared / "escape.tex").symlink_to(outside)
            with self.assertRaisesRegex(
                CHECKER.StructureError, "resolves outside curriculum root"
            ):
                CHECKER._source_path(
                    root, r"\CourseRoot/shared/escape", diagnostic
                )

    def test_pdf_destinations_match_declared_logical_pages(self) -> None:
        entries = [
            part(1, "Front Part", "i"),
            chapter(1, "First chapter", "chapter.1", "1"),
        ]
        destinations = """
Page  Destination                 Name
   2 [ XYZ 0 0 null ] "page.i"
   2 [ XYZ 0 0 null ] "part.1"
   3 [ XYZ 0 0 null ] "page.1"
   3 [ XYZ 0 0 null ] "chapter.1"
"""
        CHECKER.validate_pdf_destinations(destinations, entries)
        broken = destinations.replace(
            '   3 [ XYZ 0 0 null ] "chapter.1"',
            '   4 [ XYZ 0 0 null ] "chapter.1"',
        )
        with self.assertRaisesRegex(
            CHECKER.StructureError, "declared ToC page '1' maps to physical page 3"
        ):
            CHECKER.validate_pdf_destinations(broken, entries)

    def test_worksheet_definition_rejects_duplicate_stable_ids(self) -> None:
        block = r"""
\begin{worksheet}{I.1}{A}{Title}{Variant A}{Focus}{Use}
\end{worksheet}
\begin{worksheet}{I.1}{B}{Title}{Variant B}{Focus}{Use}
\end{worksheet}
\begin{worksheet}{I.3}{C}{Title}{Variant C}{Focus}{Use}
\end{worksheet}
\begin{worksheet}{I.4}{D}{Title}{Variant D}{Focus}{Use}
\end{worksheet}
"""
        with self.assertRaisesRegex(CHECKER.StructureError, "repeats worksheet ID I.1"):
            CHECKER._worksheet_definitions(block, Path("exercise.tex"), "I.1")

    def test_rejects_chapter_number_that_does_not_restart_at_a_new_part(self) -> None:
        entries = generic_entries()
        entries[5] = replace(entries[5], number="3")
        with self.assertRaisesRegex(
            CHECKER.StructureError,
            "within Part II is invalid: expected 1, found 3",
        ):
            CHECKER.validate_document(
                self.generic_document, entries, bookmarks(entries)
            )

    def test_rejects_duplicate_destinations_after_chapter_number_restart(self) -> None:
        entries = generic_entries()
        entries[5] = replace(entries[5], destination="chapter.1.1")
        with self.assertRaisesRegex(
            CHECKER.StructureError, "table of contents contains duplicate destinations"
        ):
            CHECKER.validate_document(
                self.generic_document, entries, bookmarks(entries)
            )

    def test_rejects_unnumbered_toc_chapters(self) -> None:
        entries = generic_entries()
        entries[1] = replace(entries[1], number=None)
        with self.assertRaisesRegex(
            CHECKER.StructureError,
            "Unnumbered chapter is not permitted in Part I: First chapter",
        ):
            CHECKER.validate_document(
                self.generic_document, entries, bookmarks(entries)
            )

    def test_rejects_wrong_section_prefix_and_sequence(self) -> None:
        entries = generic_entries()
        entries[6] = replace(entries[6], number="2.2")
        with self.assertRaisesRegex(
            CHECKER.StructureError,
            "Section sequence is invalid: expected 1.1, found 2.2",
        ):
            CHECKER.validate_document(
                self.generic_document, entries, bookmarks(entries)
            )

    def test_rejects_an_empty_part(self) -> None:
        entries = generic_entries() + [part(3, "Empty")]
        with self.assertRaisesRegex(CHECKER.StructureError, "Part 3 contains no chapter"):
            CHECKER.validate_document(
                self.generic_document, entries, bookmarks(entries)
            )

    def test_rejects_flat_or_duplicate_bookmarks(self) -> None:
        entries = generic_entries()
        rendered_bookmarks = bookmarks(entries)
        rendered_bookmarks[1] = replace(
            rendered_bookmarks[1], level=0, parent=""
        )
        rendered_bookmarks[5] = replace(
            rendered_bookmarks[5], destination=rendered_bookmarks[1].destination
        )
        with self.assertRaisesRegex(
            CHECKER.StructureError, "duplicate destinations|expected 1 for chapter"
        ):
            CHECKER.validate_document(
                self.generic_document, entries, rendered_bookmarks
            )

    def test_module_requires_matching_solution_unit_chapters(self) -> None:
        document = (
            "curriculums/ecclesiastical-latin/01-foundations/"
            "01-form-case-and-agreement"
        )
        entries = module_entries()
        CHECKER.validate_document(document, entries, bookmarks(entries))

        broken_title = [
            replace(entry, title="Different source unit")
            if entry.destination == "chapter.5.4"
            else entry
            for entry in entries
        ]
        with self.assertRaisesRegex(
            CHECKER.StructureError,
            "source-owned worksheet and solution unit chapters differ",
        ):
            CHECKER.validate_document(
                document, broken_title, bookmarks(broken_title)
            )

        missing_solution = [
            entry
            for entry in entries
            if entry.destination != "section*.solution-i2-d"
        ]
        with self.assertRaisesRegex(
            CHECKER.StructureError,
            "one solution for every worksheet|IDs/titles differ",
        ):
            CHECKER.validate_document(
                document, missing_solution, bookmarks(missing_solution)
            )

    def test_common_trunk_requires_every_declared_teaching_unit(self) -> None:
        document = (
            "curriculums/ecclesiastical-latin/01-foundations/"
            "01-form-case-and-agreement"
        )
        entries = module_entries()

        without_second_teaching = [
            entry
            for entry in entries
            if entry.destination not in {"chapter.1.2", "section.1.2.1"}
        ]
        with self.assertRaisesRegex(
            CHECKER.StructureError,
            "Teaching and Cumulative Practice must render the same number",
        ):
            CHECKER.validate_document(
                document,
                without_second_teaching,
                bookmarks(without_second_teaching),
            )

        one_unit = []
        for entry in entries:
            if (
                entry.destination in {"chapter.1.2", "section.1.2.1", "chapter.4.2", "chapter.5.4"}
                or entry.destination.startswith("section*.worksheet-i2-")
                or entry.destination.startswith("section*.solution-i2-")
            ):
                continue
            if entry.destination == "chapter.4.3":
                entry = replace(entry, number="2")
            one_unit.append(entry)
        with self.assertRaisesRegex(
            CHECKER.StructureError,
            "common-trunk packet must render two or three teaching units",
        ):
            CHECKER.validate_document(document, one_unit, bookmarks(one_unit))

        fixture_expectation = (
            ("I.1", "I.2"),
            ("I.1", "I.1", "I.1", "I.1", "I.2", "I.2", "I.2", "I.2"),
        )
        CHECKER.validate_document(
            document,
            entries,
            bookmarks(entries),
            expected_module=fixture_expectation,
        )
        wrong_ids = (
            fixture_expectation[0],
            fixture_expectation[1][:-1] + ("I.99",),
        )
        with self.assertRaisesRegex(
            CHECKER.StructureError,
            "rendered worksheet IDs differ from the canonical registry",
        ):
            CHECKER.validate_document(
                document,
                entries,
                bookmarks(entries),
                expected_module=wrong_ids,
            )

    def test_module_requires_declared_packet_parts(self) -> None:
        document = (
            "curriculums/ecclesiastical-latin/01-foundations/"
            "01-form-case-and-agreement"
        )
        self.assertEqual(
            CHECKER.MODULE_PARTS,
            (
                "Teaching",
                "Memory Work",
                "Reading and Composition",
                "Cumulative Practice",
                "Answers and Models",
                "Scope and Sources",
            ),
        )
        entries = module_entries()
        CHECKER.validate_document(document, entries, bookmarks(entries))

        broken = [
            replace(entry, title=part(3, "Cumulative Practice").title)
            if entry.destination == "part.3"
            else replace(entry, title=part(4, "Reading and Composition").title)
            if entry.destination == "part.4"
            else entry
            for entry in entries
        ]
        with self.assertRaisesRegex(
            CHECKER.StructureError,
            "learning packet Parts differ from the declared sequence",
        ):
            CHECKER.validate_document(document, broken, bookmarks(broken))

    def test_module_navigation_stays_beneath_source_owned_units(self) -> None:
        document = (
            "curriculums/ecclesiastical-latin/01-foundations/"
            "01-form-case-and-agreement"
        )
        entries = module_entries()
        CHECKER.validate_document(document, entries, bookmarks(entries))
        for destination, wrapper_destination, expected in (
            (
                "chapter.4.1",
                "chapter*.worksheet-wrapper",
                "worksheet .*has no numbered unit-chapter parent",
            ),
            (
                "chapter.5.3",
                "chapter*.solution-wrapper",
                "solution .*has no numbered unit-chapter parent",
            ),
        ):
            with self.subTest(destination=destination):
                index = next(
                    index
                    for index, entry in enumerate(entries)
                    if entry.destination == destination
                )
                broken = list(entries)
                broken.insert(
                    index + 1,
                    chapter(None, "Generic wrapper", wrapper_destination),
                )
                with self.assertRaisesRegex(CHECKER.StructureError, expected):
                    CHECKER.validate_document(
                        document, broken, bookmarks(broken)
                    )

    def test_module_later_worksheet_and_solution_forms_start_new_pages(self) -> None:
        document = (
            "curriculums/ecclesiastical-latin/01-foundations/"
            "01-form-case-and-agreement"
        )
        entries = module_entries()
        CHECKER.validate_document(document, entries, bookmarks(entries))
        for destination, prior_destination, label in (
            (
                "section*.worksheet-i1-c",
                "section*.worksheet-i1-b",
                "learner worksheets",
            ),
            (
                "section*.solution-i1-c",
                "section*.solution-i1-b",
                "keyed solutions",
            ),
        ):
            with self.subTest(label=label):
                prior_page = next(
                    entry.page
                    for entry in entries
                    if entry.destination == prior_destination
                )
                broken = [
                    replace(entry, page=prior_page)
                    if entry.destination == destination
                    else entry
                    for entry in entries
                ]
                with self.assertRaisesRegex(
                    CHECKER.StructureError,
                    rf"later {label} must start on a strictly later logical page",
                ):
                    CHECKER.validate_document(
                        document, broken, bookmarks(broken)
                    )

                reversed_pages = [
                    replace(entry, page="5")
                    if entry.destination == destination
                    else replace(entry, page="6")
                    if entry.destination == prior_destination
                    else entry
                    for entry in entries
                ]
                with self.assertRaisesRegex(
                    CHECKER.StructureError,
                    rf"later {label} must start on a strictly later logical page",
                ):
                    CHECKER.validate_document(
                        document,
                        reversed_pages,
                        bookmarks(reversed_pages),
                    )

    def test_module_requires_four_variants_per_source_unit(self) -> None:
        document = (
            "curriculums/ecclesiastical-latin/01-foundations/"
            "01-form-case-and-agreement"
        )
        entries = module_entries()
        CHECKER.validate_document(document, entries, bookmarks(entries))

        broken = [
            entry
            for entry in entries
            if entry.destination
            not in {
                "section*.worksheet-i1-d",
                "section*.solution-i1-d",
            }
        ]
        with self.assertRaisesRegex(
            CHECKER.StructureError,
            "must contain four A–D forms",
        ):
            CHECKER.validate_document(
                document,
                broken,
                bookmarks(broken),
            )

    def test_assessment_rejects_foreign_review_group_and_forms(self) -> None:
        document = (
            "curriculums/ecclesiastical-latin/05-stage-assessments/"
            "01-foundations"
        )
        entries = assessment_entries()
        CHECKER.validate_document(document, entries, bookmarks(entries))

        broken = [
            replace(entry, title="Core Grammar Cumulative Review")
            if entry.destination == "chapter.2.1"
            else replace(entry, title="C-A. Foreign form")
            if entry.destination == "section*.fa.review"
            else entry
            for entry in entries
        ]
        with self.assertRaisesRegex(
            CHECKER.StructureError, "must render only|leaf selection"
        ):
            CHECKER.validate_document(document, broken, bookmarks(broken))

        peer_chapter = [
            replace(entry, kind="chapter")
            if entry.destination == "section*.fa.review"
            else entry
            for entry in entries
        ]
        with self.assertRaisesRegex(
            CHECKER.StructureError, "forms must be unnumbered sections"
        ):
            CHECKER.validate_document(
                document, peer_chapter, bookmarks(peer_chapter)
            )

    def test_assessment_forms_remain_bookmarked_under_their_review_group(self) -> None:
        document = (
            "curriculums/ecclesiastical-latin/05-stage-assessments/"
            "01-foundations"
        )
        entries = assessment_entries()
        CHECKER.validate_document(document, entries, bookmarks(entries))
        group_index = next(
            index
            for index, entry in enumerate(entries)
            if entry.destination == "chapter.2.1"
        )
        broken = list(entries)
        broken.insert(
            group_index + 1,
            chapter(None, "Generic forms wrapper", "chapter*.forms-wrapper"),
        )
        with self.assertRaisesRegex(
            CHECKER.StructureError,
            "Review Forms form F-A .*expected review group",
        ):
            CHECKER.validate_document(document, broken, bookmarks(broken))

    def test_assessment_protocol_chapters_are_globally_unique(self) -> None:
        document = (
            "curriculums/ecclesiastical-latin/05-stage-assessments/"
            "01-foundations"
        )
        entries = assessment_entries()
        CHECKER.validate_document(document, entries, bookmarks(entries))

        repeated = [
            replace(entry, title="Common self-review method")
            if entry.destination == "chapter.4.1"
            else entry
            for entry in entries
        ]
        with self.assertRaisesRegex(
            CHECKER.StructureError, "must occur exactly once in the whole document"
        ):
            CHECKER.validate_document(document, repeated, bookmarks(repeated))


if __name__ == "__main__":
    unittest.main()
