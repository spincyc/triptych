"""Orientation rows retain exact subjects, locus reach, and every alternative."""
from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))
import _proper_chronology as chronology
import _proper_components as components
import _chronology as corpus
from tools.tests.test_content_preflight_study import StudyLeaf
from tools.tests.test_chronology import load_tool

TWENTIETH = "liturgy/roman-rite/1962/propers/temporal/60-twentieth-after-pentecost"
NEXT = "liturgy/roman-rite/1962/propers/temporal/61-twenty-first-after-pentecost"
PC54 = ("liturgy/roman-rite/postconciliar/roman-missal-third-edition-en-us-2011/"
        "propers/temporal/pc-s54-twenty-eighth-sunday-in-ordinary-time-year-a")


class OrientationProjectionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.found = chronology.dossier(TWENTIETH, provider="gpt")
        cls.projection = chronology.annotations(cls.found, presentation="orientation-v1")

    def test_legacy_projection_is_byte_identical(self):
        path = ROOT / "src/gpt" / TWENTIETH / chronology.ANNOTATIONS_RECORD
        self.assertEqual(chronology.render_annotations_tex(chronology.annotations(self.found)), path.read_text())
        self.assertEqual(chronology.render(self.found),
                         (ROOT / "src/gpt" / TWENTIETH / chronology.RECORD).read_text())

    def test_every_assertion_keeps_exact_locus_reach_and_alternatives(self):
        expected = {(element.key, reach.locus, claim.subject, claim.relation, claim.profile, claim.label)
                    for element in self.found.elements for claim in element.claims for reach in claim.reaches}
        actual = {(passage.element_key, locus, claim.subject, claim.relation, claim.profile, claim.label)
                  for row in self.projection.orientation_rows
                  if not row.group.requested_profile and not row.group.anchor_context
                  for passage in row.passages for locus in passage.loci for claim in row.group.claims}
        self.assertEqual(actual, expected)

    def test_mixed_introit_never_gives_daniels_answer_to_the_psalm(self):
        rows = [row for row in self.projection.orientation_rows
                if row.group.relation == "composition"
                and any(p.element_key == "introit" for p in row.passages)]
        self.assertEqual(len(rows), 2)
        for row in rows:
            passage = next(p for p in row.passages if p.element_key == "introit")
            if passage.loci == ("Ps.118.1",):
                self.assertEqual(chronology.orientation_date(row), "Before c. 165 B.C.")
                self.assertEqual(passage.refs, ("Ps 118:1",))
            else:
                self.assertTrue(all(locus.startswith("Dan.") for locus in passage.loci))
                self.assertEqual(chronology.orientation_date(row), "Most likely long after the Exile")

    def test_shared_psalm_date_has_one_row_and_full_coverage(self):
        rows = [row for row in self.projection.orientation_rows
                if chronology.orientation_date(row) == "Before c. 165 B.C."]
        self.assertEqual(len(rows), 1)
        self.assertEqual({p.element_key for p in rows[0].passages},
                         {"introit", "gradual", "alleluia", "offertory", "communion"})

    def test_named_comparison_follows_the_ordinary_answer(self):
        rows = [row for row in self.projection.orientation_rows
                if row.group.relation == "composition"
                and any(p.element_key == "epistle" for p in row.passages)]
        self.assertEqual(len(rows), 2)
        self.assertFalse(rows[0].group.requested_profile)
        self.assertTrue(rows[1].group.requested_profile)

    def test_scope_change_invalidates_the_authored_place_binding(self):
        extra = next(e for e in self.found.elements if e.key == "communion")._replace(
            key="additional-passage", name="Additional passage")
        changed = self.found._replace(elements=self.found.elements + (extra,))
        before = next(row for row in self.projection.orientation_rows
                      if chronology.orientation_date(row) == "Before c. 165 B.C.")
        after = next(row for row in chronology.orientation_rows(changed)
                     if chronology.orientation_date(row) == "Before c. 165 B.C.")
        self.assertNotEqual(before.key, after.key)

    def test_comparison_and_background_never_expand_partial_reach(self):
        comparison = self.found.profile_comparisons[0]
        element = next(e for e in self.found.elements if e.key == comparison.element_key)
        locus = element.loci[0]
        comparison = comparison._replace(claims=tuple(c._replace(
            reaches=tuple(r for r in c.reaches if r.locus == locus)) for c in comparison.claims))
        context = self.found.anchor_contexts[0]
        context_locus = context.parent.reaches[0].locus
        context = context._replace(parent=context.parent._replace(reaches=(context.parent.reaches[0],)))
        rows = chronology.orientation_rows(self.found._replace(
            profile_comparisons=(comparison,), anchor_contexts=(context,)))
        for row in rows:
            if row.group.requested_profile:
                self.assertEqual({l for p in row.passages for l in p.loci}, {locus})
            if row.group.anchor_context:
                self.assertEqual({l for p in row.passages for l in p.loci}, {context_locus})

    def test_context_is_not_promoted_to_the_psalm_or_stripped_of_uncertainty(self):
        row = next(row for row in self.projection.orientation_rows if row.group.anchor_context)
        self.assertIn("Historical background", chronology.orientation_subject(row))
        self.assertIn("possibly in the same year", chronology.orientation_subject(row))
        value = chronology.orientation_date(row)
        for part in ("A.M. 3416 (Haydock reporting Ussher)", "B.C. 586", "B.C. 587",
                     "B.C. 588 (Petavius via Sloet; transcription only)"):
            self.assertIn(part, value)
        self.assertNotIn("retained transcription", value)
        self.assertIn("retained transcription checked", chronology.render_annotations_tex(self.projection))

    def test_next_sunday_has_no_invented_job_era(self):
        found = chronology.dossier(NEXT, provider="gpt")
        rows = chronology.annotations(found, presentation="orientation-v1").orientation_rows
        job = [row for row in rows if any(locus.startswith("Job.")
               for p in row.passages for locus in p.loci)]
        self.assertTrue(job)
        self.assertTrue(all(row.group.relation in {claim.relation for element in found.elements
                            for claim in element.claims if any(reach.locus.startswith("Job.")
                            for reach in claim.reaches)} for row in job))

    def test_direct_reporting_exception_keeps_edition_attribution_or_refuses(self):
        found = chronology.dossier(PC54, provider="gpt")
        row = next(row for row in chronology.orientation_rows(found)
                   if row.group.relation == "superscription-setting")
        self.assertEqual(chronology.orientation_date(row),
                         "A.M. 2944 (Haydock edition reporting Ussher)")
        claim = next(c for e in found.elements for c in e.claims
                     if c.subject == "israel.monarchy.david-at-geth")
        with self.assertRaisesRegex(chronology.ChronologyWiringError, "reporting exception"):
            chronology._orientation_claim(claim._replace(orientation_qualification=""))
        self.assertNotIn("Haydock edition reporting Ussher", chronology.render(found))

    def test_esther_conjecture_keeps_its_qualified_force(self):
        found = chronology.dossier(NEXT, provider="gpt")
        row = next(row for row in chronology.orientation_rows(found)
                   if row.group.claims and row.group.claims[0].subject == "composition.book-of-esther")
        self.assertEqual(chronology.orientation_date(row),
                         "B.C. 465–425 (Conjectural early dating; later date possible)")

    def test_month_day_uses_source_calendar_words(self):
        claim = self.found.elements[0].claims[0]._replace(
            date="01-14", label="14 Nisan", precision="month-day")
        self.assertEqual(chronology._orientation_claim(claim).display_label, "14 Nisan")
        for precision in ("month-day", "day"):
            derived = claim._replace(derived=True, precision=precision)
            self.assertEqual(chronology._orientation_claim(derived).display_label, "14 Nisan (derived)")

    def test_pending_occasion_does_not_become_a_claim_of_undatability(self):
        row = next(row for row in self.projection.orientation_rows
                   if row.group.relation == "historical-setting" and not row.group.claims)
        self.assertEqual(row.group.status, "research-pending")
        self.assertEqual(chronology.orientation_date(row), "Occasion date unresolved")

    def test_exodus_relative_labels_name_the_anchor_and_preserve_ordinals(self):
        found = chronology.dossier(NEXT, provider="gpt")
        row = next(r for r in chronology.orientation_rows(found)
                   if r.group.relation == "retrospective-event")
        value = chronology.orientation_date(row)
        self.assertIn("Temple begun in the 480th year after the Exodus (Vulgate)", value)
        self.assertIn("Temple begun in the 440th year after the Exodus (Septuagint)", value)
        claim = next(c for e in found.elements for c in e.claims if c.orientation_label)
        fallback = chronology._orientation_claim(claim._replace(orientation_label=""))
        self.assertEqual(fallback.display_label, chronology.concise_display_label(claim))
        self.assertNotIn("Temple begun", chronology.render(found))

    def test_compact_labels_cannot_replace_absolute_dates(self):
        loaded = corpus.load()
        claim = loaded.events["israel.exile.third-captivity"].claims[0]
        raw = {"dates": [{"profile": claim.profile, "basis": claim.basis,
            "sources": list(claim.sources), "basis_class": claim.basis_class,
            "reporting_exception": claim.reporting_exception,
            "orientation_label": "Misleading replacement", "date": {
                "precision": "year", "from": {"year": 3416, "era": "am"}, "label": claim.date.label}}]}
        with self.assertRaisesRegex(corpus.ChronologyError, "only for relative"):
            corpus._claims(raw, "fixture", loaded.policies)


class OrientationGateTests(StudyLeaf, unittest.TestCase):
    document = TWENTIETH

    def setUp(self):
        super().setUp()
        self.shared_date_wrapper()
        with (self.leaf / "proper-components.toml").open("a") as stream:
            stream.write('presentation_contract = "interpretive-pagination-v1"\n'
                         'chronology_presentation = "orientation-v1"\n')
        self.found = self.corpus()
        self.projection = chronology.annotations(self.found)
        self.generated = self.leaf / chronology.ANNOTATIONS_RECORD
        self.generated.write_text(chronology.render_annotations_tex(self.projection))
        self.calls = [rf"\chronologyorientationrow{{{row.key}}}{{Place uncertain.}}"
                      for row in self.projection.orientation_rows]
        self.table = (r"\begin{chronologyorientationtable}" + "\n" + "\n".join(self.calls)
                      + "\n" + r"\end{chronologyorientationtable}")
        self.write("synthesis", self.table)

    def test_current_complete_rows_pass_and_generated_names_obey_shared_format(self):
        for check in ("chronology-record-current", "chronology-annotations-current", "chronology-claims-supported"):
            self.assertEqual(self.check(check, "synthesis")[0], [], check)
        text = components.tex_source(self.generated)
        components.audit_format_definitions(self.generated, self.leaf, text)
        components.audit_executable_tex(self.generated, self.leaf, text)

    def test_research_before_manifest_recomputes_orientation_and_refuses_edits(self):
        (self.leaf / "proper-components.toml").unlink()
        self.assertEqual(chronology.presentation_contract(self.leaf), "orientation-v1")
        self.assertEqual(self.check("chronology-annotations-current")[0], [])
        self.generated.write_text(self.generated.read_text().replace("B.C. 588", "B.C. 589"))
        self.assertTrue(self.check("chronology-annotations-current")[0])
        with self.assertRaisesRegex(chronology.ChronologyWiringError, "schema-2"):
            chronology.presentation_contract(self.leaf, required=True)

    def test_omitted_duplicate_unknown_or_outside_rows_refuse(self):
        for body in (self.table.replace(self.calls[0], ""),
                     self.table.replace(self.calls[0], self.calls[0] * 2),
                     self.table.replace(self.projection.orientation_rows[0].key, "row-forged"),
                     "\n".join(self.calls)):
            with self.subTest(body=body[:50]):
                self.write("synthesis", body)
                self.assertTrue(self.check("chronology-claims-supported", "synthesis")[0])

    def test_authored_dates_and_row_structure_cannot_replace_generated_cells(self):
        for body in (self.table.replace("Place uncertain.", "Rome, A.D. 1000."),
                     self.table.replace("Place uncertain.", r"Rome & A.D. 61\\"),
                     self.table.replace(self.calls[0], "Introit & Babylon & Unknown\\\\")):
            self.write("synthesis", body)
            self.assertTrue(self.check("chronology-claims-supported", "synthesis")[0])

    def test_changed_generated_row_or_shadowed_dispatcher_refuses(self):
        self.generated.write_text(self.generated.read_text().replace("B.C. 588", "B.C. 589"))
        self.assertTrue(self.check("chronology-annotations-current", "synthesis")[0])
        self.generated.write_text(chronology.render_annotations_tex(self.projection))
        self.write("synthesis", self.table + r"\renewcommand{\chronologyorientationrow}[2]{Forged}")
        self.assertTrue(self.check("chronology-annotations-current", "synthesis")[0])

    def test_web_expansion_keeps_three_cells_and_every_generated_value(self):
        web = load_tool("web-edition")
        expanded, payloads = web.expand_chronology_annotations(self.table, self.generated.read_text())
        self.assertEqual(len(payloads), 3 * len(self.calls))
        self.assertNotIn("triptychchronologyorientation@", expanded)
        self.assertNotIn("catholic-comprehensive-v1", expanded)
        self.assertIn("B.C. 588 (Petavius via Sloet; transcription only)", expanded)
        self.assertIn("Place uncertain.", expanded)
        with self.assertRaisesRegex(web.ConversionError, "no generated chronology orientation"):
            web.expand_chronology_annotations(r"\chronologyorientationrow{row-forged}{}", self.generated.read_text())


if __name__ == "__main__":
    unittest.main()
