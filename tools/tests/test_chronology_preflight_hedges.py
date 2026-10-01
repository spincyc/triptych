#!/usr/bin/env python3
"""The content preflight reads a date's hedge by the Date cells' own rule.

Until 2026-10-01 `_date_signature` in tools/check-content-preflight counted
only "about" and "c." as approximate, and "about" anywhere. Two consequences
reached published checks: a source label saying "around A.D. 80–100" was read
as the exact span, so it authorized "A.D. 80–100" in prose while the Date cell
printed "c. A.D. 80–100"; and "about Easter A.D. 57", which states its year
and hedges the season, authorized "c. A.D. 57". Both now follow
`_proper_chronology.hedges_the_year`, the one definition the generated Date
cells use.
"""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from test_content_preflight_study import (  # noqa: E402
    EIGHTEENTH,
    PREFLIGHT,
    StudyLeaf,
)

NINETEENTH = "liturgy/roman-rite/1962/propers/temporal/59-nineteenth-after-pentecost"


class DateSignatureTests(unittest.TestCase):
    def test_every_hedge_on_a_year_is_approximate(self) -> None:
        for printed, years in (
            ("around A.D. 80–100", (80, 100)),
            ("around A.D.~80--100", (80, 100)),
            ("circa A.D. 80", (80,)),
            ("ca. 80 A.D.", (80,)),
            ("c. A.D. 70", (70,)),
            ("about A.D. 38-45", (38, 45)),
            ("about the year 70 A.D.", (70,)),
            ("approximately A.D. 70", (70,)),
            ("from the year 90 to 100 A.D. (approximately)", (90, 100)),
        ):
            with self.subTest(printed=printed):
                self.assertEqual(PREFLIGHT._date_signature(printed),
                                 ("AD", "approximate", years))

    def test_a_hedge_on_something_else_leaves_the_year_exact(self) -> None:
        # The year is stated; "about" hedges Easter.
        self.assertEqual(PREFLIGHT._date_signature("about Easter A.D. 57"),
                         ("AD", "exact", (57,)))
        # "A. C." is ante Christum, an era, not "c." for circa.
        self.assertEqual(
            PREFLIGHT._date_signature("A. M. 2513, A. C. 1491")[1], "exact")
        # Both direction and the approximate bound survive.
        self.assertEqual(
            PREFLIGHT._date_signature(
                "before the Maccabean period, around 165 B.C.")[1],
            "before-approximate")
        self.assertNotEqual(
            PREFLIGHT._date_signature("before c. 165 B.C."),
            PREFLIGHT._date_signature("before 165 B.C."))
        self.assertEqual(
            PREFLIGHT._date_signature("after c. A.D. 70")[1],
            "after-approximate")

    def test_the_prose_scan_keeps_the_hedge_word_with_its_date(self) -> None:
        for printed in ("around A.D.~80--100", "circa A.D.~80",
                        "ca.~80~A.D.", "c.~A.D.~70",
                        "approximately A.D.~70", "about the year 70~A.D.",
                        "A.D.~70 (approximately)", "before 70~A.D.",
                        "before c.~165~B.C."):
            with self.subTest(printed=printed):
                match = PREFLIGHT.MANUAL_CHRONOLOGY_DATE.search(
                    f"The text gives {printed} here.")
                self.assertEqual(match.group(0), printed)


class EphesiansComparisonHedgeTests(StudyLeaf, unittest.TestCase):
    """The Nineteenth Sunday's Epistle comparison: "around A.D. 80–100"."""

    document = NINETEENTH

    def setUp(self):
        super().setUp()
        (self.leaf / "research/chronology-profile-comparisons.toml").write_text(
            'schema = 1\n'
            'record_type = "proper-chronology-profile-comparisons"\n'
            f'document = "{self.document}"\n\n'
            '[[comparisons]]\n'
            'key = "critical-ephesians-composition"\n'
            'element = "epistle"\n'
            'profile = "catholic-critical-v1"\n'
            'relation = "composition"\n'
            'subject = "critical.ephesians-later-disciple"\n')
        self.corpus()

    def prose(self, printed):
        self.write("research", f"The introduction dates it {printed}.\n")
        return self.check("chronology-claims-supported", "research")[0]

    def test_the_exact_span_is_not_authorized_by_a_hedged_label(self):
        problems = self.prose("A.D.~80--100")
        self.assertIn("manual chronology date", " ".join(problems))
        self.assertIn("A.D. 80-100", " ".join(problems))

    def test_the_hedged_span_is_authorized_in_either_spelling(self):
        for printed in ("around A.D.~80--100", "c.~A.D.~80--100",
                        "approximately A.D.~80--100",
                        "about the years 80--100~A.D.",
                        "A.D.~80--100 (approximately)"):
            with self.subTest(printed=printed):
                self.assertEqual(self.prose(printed), [])


class EasterHedgeTests(StudyLeaf, unittest.TestCase):
    """The Eighteenth Sunday's Epistle: "about Easter A.D. 57"."""

    document = EIGHTEENTH

    def setUp(self):
        super().setUp()
        self.write_provenance(version="6")
        self.corpus()

    def prose(self, printed):
        self.write("research", f"The article gives {printed}.\n")
        return self.check("chronology-claims-supported", "research")[0]

    def test_the_stated_year_is_authorized(self):
        self.assertEqual(self.prose("A.D.~57"), [])

    def test_a_hedge_the_source_put_on_easter_is_not_moved_to_the_year(self):
        for printed in ("c.~A.D.~57", "about A.D.~57", "around A.D.~57",
                        "approximately A.D.~57", "about the year 57~A.D.",
                        "A.D.~57 (approximately)", "before 57~A.D."):
            with self.subTest(printed=printed):
                self.assertIn("manual chronology date",
                              " ".join(self.prose(printed)))

    def test_prose_preserves_a_boundarys_hedge(self):
        self.assertEqual(self.prose("before c.~165~B.C."), [])
        self.assertIn("manual chronology date",
                      " ".join(self.prose("before 165~B.C.")))

    def test_qualified_year_without_its_era_is_still_refused(self):
        self.write("research", r"\dossierprose{The article gives about the year 57.}")
        problems = self.check("chronology-claims-supported", "research")[0]
        self.assertIn("omits its era", " ".join(problems))

    def test_per_passage_dates_preserve_the_same_qualification(self):
        wiring = PREFLIGHT._wiring()
        found = PREFLIGHT._corpus_answer(self.leaf, self.root)
        (self.leaf / "research/chronology-annotations.tex").write_text(
            wiring.render_annotations_tex(wiring.annotations(found)))
        for printed, accepted in (("before c.~165~B.C.", True),
                                  ("before 165~B.C.", False),
                                  ("about the year 57~A.D.", False)):
            with self.subTest(printed=printed):
                self.write("research",
                           r"\chronodate{introit}{\chronologyannotation{introit}}"
                           f"\n\\dossierprose{{Ps~121:1: {printed}}}\n")
                problems = self.check("chronology-claims-supported", "research")[0]
                if accepted:
                    self.assertEqual(problems, [])
                else:
                    self.assertIn("not the generated record's answer",
                                  " ".join(problems))


if __name__ == "__main__":
    unittest.main()
