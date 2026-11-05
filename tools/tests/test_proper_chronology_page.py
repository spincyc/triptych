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
import _chronology as corpus  # noqa: E402

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

    def test_a_proper_without_a_formulary_gets_its_record_and_no_rows(self):
        import _document_types as types
        from document_projections import scriptural_date_location as projection
        document = "liturgy/roman-rite/1962/propers/ritual/m01-nuptial-mass"
        context = types.LeafContext(ROOT, "gpt", document, ROOT / "src/gpt" / document,
                                    "proper-1962", "proper-guide-v1", ("main",), ("sheet", "evidence"))
        files = projection.render(context)
        self.assertEqual(sorted(files), [
            "generated/scriptural-date-location-evidence.tex",
            "generated/scriptural-date-location-sheet.tex",
            wiring.RECORD,
        ])
        self.assertIn(page.ABSENT[wiring.NO_CALENDAR_FORMULARY],
                      files["generated/scriptural-date-location-sheet.tex"])

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
        found, _, _ = page.projection(
            "liturgy/roman-rite/1962/propers/temporal/48-eighth-after-pentecost", provider="claude")
        # The real Maon setting now has its qualification. Remove it only in
        # this fixture to keep testing the refusal to publish a bare exception.
        without_qualification = lambda claim: (claim._replace(orientation_qualification="")
                                               if claim.reporting_exception else claim)
        found = found._replace(elements=tuple(element._replace(
            claims=tuple(without_qualification(claim) for claim in element.claims),
            publication_claims=tuple(without_qualification(claim) for claim in element.publication_claims))
            for element in found.elements))
        projected = wiring.annotations(found)
        pending = [row for row in projected.orientation_rows
                   if row.group.status == wiring.QUALIFICATION_PENDING]
        self.assertTrue(pending)
        for row in pending:
            self.assertEqual(row.group.claims, ())
            self.assertEqual(wiring.orientation_date(row), "Date pending its source qualification")

    def test_psalm_30_keeps_distinct_flights_before_and_during_davids_reign(self):
        _, projected, _ = page.projection(
            "liturgy/roman-rite/1962/propers/temporal/48-eighth-after-pentecost", provider="claude")
        rows = {row.group.claims[0].subject: row for row in wiring.compact_orientation_rows(projected)
                if row.group.claims and row.group.relation == "historical-setting"
                and any(locus.startswith("Ps.30.") for passage in row.passages for locus in passage.loci)}
        maon = wiring.orientation_date(rows["israel.monarchy.david-in-the-desert-of-maon"], compact=True)
        absalom = wiring.orientation_date(rows["israel.monarchy.david-flight-from-absalom"], compact=True)
        self.assertIn("1059", maon)
        self.assertIn("1025–1024", absalom)
        self.assertIn("Haydock", maon)
        self.assertIn("Ussher", maon)

    def test_source_labels_come_from_the_library(self):
        self.assertEqual(
            page.source_label("bible:douay-rheims:Matt.5.1"),
            "The Holy Bible, Douay-Rheims (Challoner revision), Project Gutenberg eBook 1581, Matt. 5:1")
        self.assertEqual(page.source_label("no.such.source"), "no.such.source")


class CompactOrientationTests(unittest.TestCase):
    @staticmethod
    def claim(date, precision="interval", label="", **changes):
        claim = wiring.AnnotationClaim(
            "composition.example", "Example", "composition", label or date, "",
            date, precision, "disputed", "catholic-traditional-v1", ("source.example",), ())
        claim = claim._replace(**changes)
        return claim._replace(display_label=wiring._concise_value(claim))

    @staticmethod
    def group(*claims):
        return wiring.AnnotationGroup("composition", "disputed", "", claims)

    def display(self, *claims):
        return wiring._orientation_candidate_display(self.group(*claims), lambda claim: claim.display_label)

    def test_disconnected_estimates_have_a_labelled_proposal_extent(self):
        value = self.display(
            self.claim("38 A.D. to 45 A.D.", label="about A.D. 38-45"),
            self.claim("40 A.D. to 42 A.D."), self.claim("40 A.D. to 45 A.D."),
            self.claim("60 A.D. to 68 A.D."), self.claim("64 A.D. to 67 A.D."),
            self.claim("about 50 A.D.", "approximate-year"))
        self.assertEqual(value, "Proposals span c. A.D. 38–68")

    def test_a_year_inside_an_interval_is_one_estimate_group(self):
        self.assertEqual(self.display(self.claim("61 A.D.", "year"),
                                      self.claim("61 A.D. to 63 A.D.")),
                         "Proposals span A.D. 61–63")

    def test_bc_envelopes_keep_chronological_endpoint_order(self):
        self.assertEqual(self.display(self.claim("650 B.C. to 630 B.C."),
                                      self.claim("640 B.C. to 620 B.C.")),
                         "Proposals span B.C. 650–620")

    def test_distinct_eras_do_not_merge(self):
        self.assertEqual(self.display(
            self.claim("40 A.D.", "year"), self.claim("41 A.D.", "year"),
            self.claim("40 A.M.", "year")), "Proposals span A.D. 40–41; A.M. 40")

    def test_disposition_profile_and_source_qualification_do_not_merge(self):
        first = self.claim("60 A.D. to 65 A.D.")
        for other in (
            self.claim("62 A.D. to 68 A.D.", disposition="preferred"),
            self.claim("62 A.D. to 68 A.D.", profile="catholic-critical-v1"),
            self.claim("62 A.D. to 68 A.D.")._replace(
                display_label="A.D. 62–68 (reported by an identified edition)"),
        ):
            with self.subTest(other=other):
                self.assertNotIn("Proposals span", self.display(first, other))

    def test_duration_spans_and_century_notation_stay_distinct(self):
        for other in (
            self.claim("60 A.D. to 68 A.D.", "range"),
            self.claim("1 A.D. to 100 A.D.", label="first century A.D."),
        ):
            with self.subTest(other=other):
                self.assertNotIn("Proposals span", self.display(
                    self.claim("61 A.D. to 63 A.D."), other))

    def test_hidden_gaps_keep_their_evidence_and_passage_heading(self):
        _, found, _ = page.projection(ALL_SAINTS, provider="claude")
        visible = wiring.compact_orientation_rows(found)
        hidden = {row.key for row in found.orientation_rows} - {row.key for row in visible}
        self.assertTrue(hidden)
        self.assertEqual({row.passages for row in visible},
                         {row.passages for row in found.orientation_rows})
        table = wiring.render_orientation_table(found)
        for key in hidden:
            self.assertNotIn(key, table)
        definitions = wiring.render_annotations_tex(found)
        for row in visible:
            if row.passage_start:
                marker = "triptychchronologyorientation@" + row.key
                definition = definitions[definitions.index(marker):].split("\n}", 1)[0]
                self.assertIn(wiring.tex_escape(wiring.orientation_passage(row)), definition)
        evidence = page.render(found, document=ALL_SAINTS, variant=page.EVIDENCE)
        self.assertIn("No date:", evidence)
        payload = wiring.annotation_payload(found)
        self.assertEqual({row["key"] for row in payload["orientation_rows"] if not row["displayed"]}, hidden)

    def test_compact_tex_keeps_each_contributing_claim_sealed(self):
        _, found, _ = page.projection(ALL_SAINTS, provider="claude")
        claims = (self.claim("61 A.D.", "year", "source first year"),
                  self.claim("61 A.D. to 63 A.D.", label="source second interval"))
        row = found.orientation_rows[0]._replace(group=self.group(*claims), calendar_estimate=None)
        projected = found._replace(orientation_rows=(row,))
        rendered = wiring.render_annotations_tex(projected)
        self.assertIn("Proposals span A.D.~61--63", rendered)
        self.assertIn(wiring._tex_claim(claims[1]._replace(display_label=""), date_typography=True), rendered)
        for claim in claims:
            self.assertIn(claim.label, rendered)
        self.assertEqual(projected.orientation_rows[0].group.claims, claims)

    def test_relative_alternative_stays_in_evidence_beside_a_numerical_overview(self):
        claims = (self.claim("38 A.D. to 40 A.D."), self.claim("60 A.D. to 70 A.D."),
                  self.claim("after the earlier work", "relative"))
        self.assertEqual(self.display(*claims), "Proposals span A.D. 38–70")
        groups = wiring._orientation_estimates(self.group(*claims))
        self.assertEqual(tuple(claim for _, members in groups for claim in members), claims)

    def test_a_relative_alternative_cannot_drop_a_different_era(self):
        claims = (self.claim("40 A.D.", "year"), self.claim("50 A.D.", "year"),
                  self.claim("40 A.M.", "year"), self.claim("after the earlier work", "relative"))
        groups = wiring._orientation_estimates(self.group(*claims))
        self.assertEqual(len(groups), 2)
        self.assertEqual(set(claim for _, members in groups for claim in members), set(claims))
        self.assertIn("A.M. 40", self.display(*claims))

    def test_calendar_orientation_preserves_its_own_qualification_and_original_evidence(self):
        _, found, _ = page.projection(ALL_SAINTS, provider="claude")
        claim = self.claim("after the deportation", "relative")
        date = corpus.Date("interval", corpus.Endpoint(598, "bc", None, None, None),
                           corpus.Endpoint(597, "bc", None, None, None), None,
                           "After the deportation of c. 598–597 B.C.", None)
        estimate = corpus.OrientationCalendarEstimate(
            claim.subject, claim.relation, claim.profile, date, "same year possible",
            ("source.calendar-orientation",), "Fixture source basis", ("event.deportation",),
            "anchor-context", "event.deportation")
        row = found.orientation_rows[0]._replace(group=self.group(claim), calendar_estimate=estimate)
        projected = found._replace(orientation_rows=(row,))
        compact = wiring.orientation_date(row, compact=True)
        self.assertEqual(compact, "After the deportation of c. 598–597 B.C. (same year possible)")
        self.assertIn("After the deportation", wiring.orientation_date(row))
        self.assertNotIn("598", wiring.orientation_date(row))
        rendered = wiring.render_annotations_tex(projected)
        self.assertIn(wiring._date_tex(compact), rendered)
        self.assertIn(wiring._tex_claim(claim._replace(display_label=""), date_typography=True), rendered)
        evidence = page.render(projected, document=ALL_SAINTS, variant=page.EVIDENCE)
        self.assertIn("after the deportation", evidence.casefold())
        self.assertIn("source.calendar-orientation", evidence)
        self.assertIn("same year possible", evidence)
        self.assertEqual(wiring.annotation_payload(projected)["orientation_rows"][0]
                         ["calendar_estimate"]["anchor"], "event.deportation")


if __name__ == "__main__":
    unittest.main()
