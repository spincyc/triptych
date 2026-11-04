"""The generated Scriptural Date and Location page: whole, deterministic, honest."""

from __future__ import annotations

import re
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))

import _proper_chronology as wiring  # noqa: E402
import _proper_chronology_page as page  # noqa: E402

ALL_SAINTS = "liturgy/roman-rite/1962/propers/temporal/f02-all-saints"
ROW_POSITION = re.compile(r"(?i)\b(?:first|second|third|fourth|last|next|previous|above|below)\s+rows?\b"
                          r"|\brows?\s+(?:[0-9]+|one|two|three)\b")


class PageTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.found, cls.projected, cls.absent = page.projection(ALL_SAINTS, provider="claude")
        cls.section = page.render(cls.projected, document=ALL_SAINTS, variant=page.SECTION)
        cls.sheet = page.render(cls.projected, document=ALL_SAINTS, variant=page.PAGE)

    def test_rendering_is_byte_deterministic(self):
        again = page.projection(ALL_SAINTS, provider="claude")[1]
        self.assertEqual(page.render(again, document=ALL_SAINTS, variant=page.SECTION), self.section)
        self.assertEqual(page.render(again, document=ALL_SAINTS, variant=page.PAGE), self.sheet)

    def test_both_variants_import_the_shared_generated_table_once(self):
        for text in (self.section, self.sheet):
            self.assertTrue(text.startswith("% Generated. Do not edit."))
            self.assertEqual(text.count(f"\\input{{{ALL_SAINTS}/research/chronology-table}}"), 1)
            self.assertEqual(text.count(f"\\input{{{ALL_SAINTS}/research/chronology-annotations}}"), 1)
        self.assertIn("\\zlabel{triptych:concise:chronology:start}", self.sheet)
        self.assertIn("\\zlabel{triptych:concise:chronology:end}", self.sheet)
        self.assertNotIn("\\subsection", self.sheet)

    def test_page_two_closes_its_own_running_head(self):
        # A following starred section would otherwise inherit page 2's head.
        self.assertTrue(self.sheet.rstrip().endswith("\\closerunninghead"))
        self.assertNotIn("\\closerunninghead", self.section)

    def test_notes_are_headed_by_the_tables_own_passage_cells(self):
        heads = re.findall(r"\\textit\{([^{}]*)\}\\par", self.section)
        cells = [wiring._date_tex(wiring.orientation_passage(row))
                 for row in self.projected.orientation_rows if row.passage_start]
        self.assertEqual(heads, cells)

    def test_no_prose_refers_to_a_row_by_position(self):
        for text in (self.section, self.sheet):
            self.assertIsNone(ROW_POSITION.search(text))

    def test_one_book_is_named_one_way(self):
        # The table abbreviates the Apocalypse as "Apoc."; the corpus's
        # subjects call it the Apocalypse. "Revelation" is neither.
        self.assertIn("Apoc. 7:2--12", self.section)
        self.assertNotIn("Revelation", self.section)

    def test_every_dated_candidate_carries_its_raw_label_and_sources(self):
        for row in self.projected.orientation_rows:
            for claim in row.group.claims:
                self.assertIn(wiring.tex_escape(claim.label.strip()), self.section)
        self.assertIn("The Catholic Encyclopedia, Volume 4 (New York, 1908)", self.section)
        self.assertIn("Catholic critical chronology", self.section)
        self.assertIn("No date: the chronology corpus has not yet dated this (research pending).",
                      self.section)

    def test_absent_states_print_no_table_and_no_date(self):
        for reason in ("appointment-input-pending", wiring.NO_CALENDAR_FORMULARY):
            for variant in page.VARIANTS:
                with self.subTest(reason=reason, variant=variant):
                    text = page.render(None, document="x", variant=variant, absent=reason)
                    self.assertNotIn("\\input", text)
                    self.assertIsNone(re.search(r"\b(?:A\.D\.|B\.C\.|A\.M\.)", text))
                    if variant == page.EVIDENCE:
                        # Nothing is dated, so no appendix is printed at all.
                        self.assertNotIn("\\section", text)
                    else:
                        self.assertIn(page.ABSENT[reason], text)

    def test_a_ritual_mass_reports_its_missing_calendar_formulary(self):
        found, projected, absent = page.projection(
            "liturgy/roman-rite/1962/propers/ritual/m01-nuptial-mass", provider="gpt")
        self.assertEqual(page.absent_reason(projected, absent), wiring.NO_CALENDAR_FORMULARY)

    def test_a_postconciliar_leaf_without_its_appointment_input_is_pending(self):
        document = ("liturgy/roman-rite/postconciliar/roman-missal-third-edition-en-us-2011/"
                    "propers/temporal/pc-s26-most-holy-trinity-year-a")
        if (ROOT / "src/gpt" / document / "research/chronology-inputs.toml").is_file():
            self.skipTest("the leaf now has its reviewed appointment input")
        self.assertEqual(page.projection(document, provider="gpt"),
                         (None, None, "appointment-input-pending"))

    def test_a_guide_takes_a_one_page_sheet_and_a_terminal_evidence_appendix(self):
        sheet = page.render(self.projected, document=ALL_SAINTS, variant=page.SHEET)
        evidence = page.render(self.projected, document=ALL_SAINTS, variant=page.EVIDENCE)
        self.assertIn("\\section*{Scriptural Date and Location}", sheet)
        self.assertIn(f"\\input{{{ALL_SAINTS}/research/chronology-table}}", sheet)
        self.assertIn("Evidence for the Scriptural Dates", sheet)
        self.assertNotIn("\\begin{itemize}", sheet)
        self.assertNotRegex(sheet, r"\\(?:zlabel|runninghead)\b")
        self.assertIn("\\section*{" + page.EVIDENCE_HEADING + "}", evidence)
        self.assertNotIn("chronology-table", evidence)
        # The guide's appendix carries the same notes as the study's section.
        notes = lambda text: text[text.index("{\\small\n"):]
        self.assertEqual(notes(evidence), notes(self.section))

    def test_an_unqualified_reporting_exception_is_withheld_not_refused(self):
        found, projected, _ = page.projection(
            "liturgy/roman-rite/1962/propers/temporal/48-eighth-after-pentecost", provider="claude")
        pending = [row for row in projected.orientation_rows
                   if row.group.status == wiring.QUALIFICATION_PENDING]
        self.assertTrue(pending, "the Maon setting is no longer withheld; update this test")
        for row in pending:
            self.assertEqual(row.group.claims, ())
            self.assertEqual(wiring.orientation_date(row), "Date pending its source qualification")

    def test_source_labels_come_from_the_library(self):
        self.assertEqual(
            page.source_label("bible:douay-rheims:Matt.5.1"),
            "The Holy Bible, Douay-Rheims (Challoner revision), Project Gutenberg eBook 1581, Matt. 5:1")
        self.assertEqual(page.source_label("no.such.source"), "no.such.source")


if __name__ == "__main__":
    unittest.main()
