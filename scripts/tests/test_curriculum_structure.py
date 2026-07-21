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


def generic_entries():
    return [
        part(1, "First Part", "1"),
        chapter(1, "First chapter", "chapter.1", "1"),
        section("1.1", "First section", "section.1.1", "1"),
        chapter(2, "Second chapter", "chapter.2", "2"),
        part(2, "Second Part", "3"),
        chapter(3, "Third chapter", "chapter.3", "3"),
        section("3.1", "Another section", "section.3.1", "3"),
    ]


def module_entries():
    entries = []
    next_chapter = 1
    practice_title = r"Unit 7: \Latin {Sum} and \Latin {Possum}"
    chapters_by_part = (
        ("Plan",),
        ("Lesson",),
        ("Connections",),
        (practice_title,),
        ("Mastery",),
        ("How to Use the Keys", "Enrichment models and rubrics", practice_title),
        ("Scope",),
    )
    for ordinal, (part_title, chapter_titles) in enumerate(
        zip(CHECKER.MODULE_PARTS, chapters_by_part), 1
    ):
        entries.append(part(ordinal, part_title))
        for title in chapter_titles:
            chapter_number = next_chapter
            chapter_page = "1"
            if part_title == "Selected Practice":
                chapter_page = "6"
            elif part_title == "Answer Key" and title == practice_title:
                chapter_page = "10"
            entries.append(
                chapter(
                    chapter_number,
                    title,
                    f"chapter.{chapter_number}",
                    chapter_page,
                )
            )
            next_chapter += 1
            if part_title == "Core Lesson":
                entries.append(
                    section(
                        f"{chapter_number}.1",
                        "Learner guidance",
                        f"section.{chapter_number}.1",
                    )
                )
            elif part_title == "Selected Practice":
                entries.extend(
                    (
                        section(
                            None,
                            "Worksheet I.26 — Variant B",
                            "section*.worksheet-b",
                            "6",
                        ),
                        section(
                            None,
                            "Worksheet I.27 — Variant C",
                            "section*.worksheet-c",
                            "7",
                        ),
                    )
                )
            elif part_title == "Answer Key" and title == practice_title:
                entries.extend(
                    (
                        section(
                            None,
                            "Solution I.26 — Variant B",
                            "section*.solution-b",
                            "10",
                        ),
                        section(
                            None,
                            "Solution I.27 — Variant C",
                            "section*.solution-c",
                            "11",
                        ),
                    )
                )
    return entries


def assessment_entries():
    entries = [
        part(1, "Assessment Protocol"),
        chapter(1, "Use, timing, and decision", "chapter.1"),
        chapter(2, "Common assessment protocol", "chapter.2"),
        chapter(3, "Scoring and remediation map", "chapter.3"),
        part(2, "Learner Forms"),
        chapter(4, "Gate I: Foundations", "chapter.4"),
        section(None, "F-A. Foundations mastery, Form A", "section*.fa.learner"),
        section(None, "F-B. Foundations mastery, Form B", "section*.fb.learner"),
        part(3, "Solutions and Rubrics"),
        chapter(5, "Gate I: Foundations", "chapter.5"),
        section(None, "F-A. Foundations mastery, Form A", "section*.fa.key"),
        section(None, "F-B. Foundations mastery, Form B", "section*.fb.key"),
        part(4, "Scope and Sources"),
        chapter(6, "Scope", "chapter.6"),
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
        self.assertEqual(parsed_bookmarks[1].parent, "part.1")

    def test_accepts_continuous_chapters_across_parts_and_nested_bookmarks(self) -> None:
        entries = generic_entries()
        CHECKER.validate_document(
            self.generic_document, entries, bookmarks(entries)
        )

    def test_rendered_contents_requires_distinct_dotted_chapter_lines(self) -> None:
        entries = generic_entries() + [
            section(None, "Worksheet sample", "section*.1", "3"),
            chapter(4, r"What ``complete'' means", "chapter.4", "4"),
        ]
        good = """TRIPTYCH / ECCLESIASTICAL LATIN                 Contents

Contents
I First Part                                                   1
1 First chapter . . . . . . . . . . . . . . . . . . . . .    1
  1.1 First section . . . . . . . . . . . . . . . . . . .    1
2 Second chapter . . . . . . . . . . . . . . . . . . . . .   2
II Second Part                                                 3
3 Third chapter . . . . . . . . . . . . . . . . . . . . .    3
  3.1 Another section . . . . . . . . . . . . . . . . . .    3
  Worksheet sample . . . . . . . . . . . . . . . . . . .    3
4 What “complete” means . . . . . . . . . . . . . . . . .    4

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
            "  3.1 Another section 3"
            if line.lstrip().startswith("3.1 Another section")
            else line
            for line in good.splitlines()
        )
        with self.assertRaisesRegex(CHECKER.StructureError, "Section 3.1 lacks"):
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

    def test_rejects_sparse_module_advance_when_pages(self) -> None:
        def page_with_words(marker: str, total: int) -> str:
            marker_count = len(marker.split())
            self.assertGreaterEqual(total, marker_count)
            return marker + " " + "evidence " * (total - marker_count)

        CHECKER.validate_fragmentary_pages(
            page_with_words("Advance when:", 90), is_module=True
        )
        with self.assertRaisesRegex(
            CHECKER.StructureError,
            "Advance when: but only 89 words; expected at least 90",
        ):
            CHECKER.validate_fragmentary_pages(
                page_with_words("Advance when:", 89), is_module=True
            )

        # The density floor belongs only to two-session learning modules.
        CHECKER.validate_fragmentary_pages(
            page_with_words("Advance when:", 20), is_module=False
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

        without_initialization = source.replace(
            r"\firstcourseworksheettrue", "", 1
        )
        with self.assertRaisesRegex(
            CHECKER.StructureError,
            "must initialize firstcourseworksheettrue",
        ):
            CHECKER.validate_course_format_layout(without_initialization, path)

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
        result = CHECKER.audit_sources(
            ROOT / "src/gpt/curriculums/ecclesiastical-latin"
        )
        self.assertEqual(
            result,
            CHECKER.SourceAudit(46, 46, 6, 9),
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

    def test_rejects_chapter_number_restart_at_a_new_part(self) -> None:
        entries = generic_entries()
        entries[5] = replace(entries[5], number="1")
        with self.assertRaisesRegex(
            CHECKER.StructureError, "continuous across Parts: expected 3, found 1"
        ):
            CHECKER.validate_document(
                self.generic_document, entries, bookmarks(entries)
            )

    def test_rejects_wrong_section_prefix_and_sequence(self) -> None:
        entries = generic_entries()
        entries[6] = replace(entries[6], number="2.2")
        with self.assertRaisesRegex(
            CHECKER.StructureError,
            "Section sequence is invalid: expected 3.1, found 2.2",
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

    def test_module_requires_practice_chapter_in_the_answer_key(self) -> None:
        document = (
            "curriculums/ecclesiastical-latin/01-foundations/"
            "01-grammar-bridge"
        )
        entries = module_entries()
        CHECKER.validate_document(document, entries, bookmarks(entries))

        broken = [
            replace(entry, title="Different worksheet")
            if entry.destination == "chapter.8"
            else entry
            for entry in entries
        ]
        with self.assertRaisesRegex(
            CHECKER.StructureError, "exactly one matching source-owned unit chapter"
        ):
            CHECKER.validate_document(document, broken, bookmarks(broken))

        wrapped = [
            replace(entry, title="Selected worksheet solutions")
            if entry.destination == "chapter.7"
            else entry
            for entry in entries
        ]
        with self.assertRaisesRegex(CHECKER.StructureError, "forbidden generic"):
            CHECKER.validate_document(document, wrapped, bookmarks(wrapped))

        unnumbered_wrapped = list(entries)
        answer_part_index = next(
            index
            for index, entry in enumerate(unnumbered_wrapped)
            if entry.kind == "part" and "Answer Key" in entry.title
        )
        unnumbered_wrapped.insert(
            answer_part_index + 1,
            chapter(
                None,
                "Selected worksheet solutions",
                "section*.generic-solution-wrapper",
            ),
        )
        with self.assertRaisesRegex(CHECKER.StructureError, "forbidden generic"):
            CHECKER.validate_document(
                document,
                unnumbered_wrapped,
                bookmarks(unnumbered_wrapped),
            )

        missing_solution = [
            entry
            for entry in entries
            if entry.destination != "section*.solution-c"
        ]
        with self.assertRaisesRegex(
            CHECKER.StructureError, "exactly two solution sections|section IDs differ"
        ):
            CHECKER.validate_document(
                document, missing_solution, bookmarks(missing_solution)
            )

    def test_module_navigation_stays_beneath_source_owned_units(self) -> None:
        document = (
            "curriculums/ecclesiastical-latin/01-foundations/"
            "01-grammar-bridge"
        )
        entries = module_entries()
        CHECKER.validate_document(document, entries, bookmarks(entries))
        for destination, wrapper_destination, expected in (
            ("chapter.4", "chapter*.worksheet-wrapper", "worksheet .*expected source-owned unit"),
            ("chapter.8", "chapter*.solution-wrapper", "solution .*expected source-owned unit"),
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

    def test_module_later_practice_and_solution_forms_start_new_pages(self) -> None:
        document = (
            "curriculums/ecclesiastical-latin/01-foundations/"
            "01-grammar-bridge"
        )
        entries = module_entries()
        CHECKER.validate_document(document, entries, bookmarks(entries))
        for destination, prior_destination, label in (
            ("section*.worksheet-c", "section*.worksheet-b", "learner worksheets"),
            ("section*.solution-c", "section*.solution-b", "keyed solutions"),
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

    def test_module_answer_unit_chapter_stays_with_first_solution(self) -> None:
        document = (
            "curriculums/ecclesiastical-latin/01-foundations/"
            "01-grammar-bridge"
        )
        entries = module_entries()
        CHECKER.validate_document(document, entries, bookmarks(entries))

        broken = [
            replace(entry, page="9")
            if entry.destination == "chapter.8"
            else entry
            for entry in entries
        ]
        with self.assertRaisesRegex(
            CHECKER.StructureError,
            "Answer Key source-owned unit chapter and first solution must "
            "share one logical page",
        ):
            CHECKER.validate_document(
                document,
                broken,
                bookmarks(broken),
            )

    def test_assessment_rejects_foreign_gate_and_form_headings(self) -> None:
        document = (
            "curriculums/ecclesiastical-latin/05-stage-assessments/"
            "01-foundations"
        )
        entries = assessment_entries()
        CHECKER.validate_document(document, entries, bookmarks(entries))

        broken = [
            replace(entry, title="Gate II: Complete Core Grammar")
            if entry.destination == "chapter.4"
            else replace(entry, title="C-A. Foreign form")
            if entry.destination == "section*.fa.learner"
            else entry
            for entry in entries
        ]
        with self.assertRaisesRegex(
            CHECKER.StructureError, "must render only|leaf selection"
        ):
            CHECKER.validate_document(document, broken, bookmarks(broken))

        peer_chapter = [
            replace(entry, kind="chapter")
            if entry.destination == "section*.fa.learner"
            else entry
            for entry in entries
        ]
        with self.assertRaisesRegex(
            CHECKER.StructureError, "forms must be unnumbered sections"
        ):
            CHECKER.validate_document(
                document, peer_chapter, bookmarks(peer_chapter)
            )

    def test_assessment_forms_remain_bookmarked_under_their_gate(self) -> None:
        document = (
            "curriculums/ecclesiastical-latin/05-stage-assessments/"
            "01-foundations"
        )
        entries = assessment_entries()
        CHECKER.validate_document(document, entries, bookmarks(entries))
        gate_index = next(
            index
            for index, entry in enumerate(entries)
            if entry.destination == "chapter.4"
        )
        broken = list(entries)
        broken.insert(
            gate_index + 1,
            chapter(None, "Generic forms wrapper", "chapter*.forms-wrapper"),
        )
        with self.assertRaisesRegex(
            CHECKER.StructureError, "Learner Forms form F-A .*expected gate"
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
            replace(entry, title="Common assessment protocol")
            if entry.destination == "chapter.6"
            else entry
            for entry in entries
        ]
        with self.assertRaisesRegex(
            CHECKER.StructureError, "must occur exactly once in the whole document"
        ):
            CHECKER.validate_document(document, repeated, bookmarks(repeated))


if __name__ == "__main__":
    unittest.main()
