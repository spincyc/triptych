"""Tests for turning a verse range into the loci a reading page fetches."""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))

from _loci import range_to_loci  # noqa: E402


class WithinOneChapterTests(unittest.TestCase):
    def test_a_plain_range_is_one_locus(self) -> None:
        self.assertEqual(
            range_to_loci({"chapter": 24, "verse": 1}, {"chapter": 24, "verse": 3}),
            [{"chapter": 24, "first": 1, "last": 3}],
        )

    def test_an_absent_end_chapter_means_the_same_chapter(self) -> None:
        self.assertEqual(
            range_to_loci({"chapter": 24, "verse": 1}, {"verse": 3}),
            [{"chapter": 24, "first": 1, "last": 3}],
        )

    def test_a_whole_chapter_is_open_at_both_ends(self) -> None:
        self.assertEqual(
            range_to_loci({"chapter": 24}, {"chapter": 24}),
            [{"chapter": 24, "first": None, "last": None}],
        )


class AcrossChaptersTests(unittest.TestCase):
    """A range that crosses a chapter used to be flattened onto its opening
    chapter, which turned Exodus 14:15-15:1 into verses 15 to 1 and rendered
    as nothing at all. 135 of 1975 citations and readings carried one."""

    def test_the_easter_vigil_crossing_spans_two_chapters(self) -> None:
        self.assertEqual(
            range_to_loci({"chapter": 14, "verse": 15}, {"chapter": 15, "verse": 1}),
            [
                {"chapter": 14, "first": 15, "last": None},
                {"chapter": 15, "first": None, "last": 1},
            ],
        )

    def test_an_epistle_crossing_a_chapter_spans_two(self) -> None:
        # 1 Corinthians 10:31-11:1, as the missal prints it.
        self.assertEqual(
            range_to_loci({"chapter": 10, "verse": 31}, {"chapter": 11, "verse": 1}),
            [
                {"chapter": 10, "first": 31, "last": None},
                {"chapter": 11, "first": None, "last": 1},
            ],
        )

    def test_chapters_between_the_ends_are_open_at_both(self) -> None:
        self.assertEqual(
            range_to_loci({"chapter": 3, "verse": 4}, {"chapter": 6, "verse": 2}),
            [
                {"chapter": 3, "first": 4, "last": None},
                {"chapter": 4, "first": None, "last": None},
                {"chapter": 5, "first": None, "last": None},
                {"chapter": 6, "first": None, "last": 2},
            ],
        )

    def test_no_locus_ever_runs_backwards(self) -> None:
        """The defect that produced nothing on the page: first above last.

        This test asserted nothing for as long as it existed. Every case it
        carried crossed a chapter, and a cross-chapter range gives every locus
        an open end, so `first is not None and last is not None` was false for
        all of them and the assertion never ran once. The same-chapter case it
        was named for was the one case it did not carry — and that branch had no
        ordering check, so it returned `first: 9, last: 3` without complaint.

        The guard stays, because an open end genuinely cannot be compared, but a
        same-chapter range is now among the cases and the count below fails if a
        future edit makes every case unassertable again.
        """
        compared = 0
        for begin, end in (
            ({"chapter": 24, "verse": 1}, {"chapter": 24, "verse": 3}),
            ({"chapter": 14, "verse": 15}, {"chapter": 15, "verse": 1}),
            ({"chapter": 13, "verse": 17}, {"chapter": 14, "verse": 14}),
            ({"chapter": 63, "verse": 16}, {"chapter": 64, "verse": 7}),
        ):
            for locus in range_to_loci(begin, end):
                if locus["first"] is not None and locus["last"] is not None:
                    self.assertLessEqual(locus["first"], locus["last"], locus)
                    compared += 1
        self.assertGreater(compared, 0, "every case was unassertable; the test proved nothing")


class RefusalTests(unittest.TestCase):
    def test_a_descending_chapter_range_raises(self) -> None:
        with self.assertRaises(ValueError):
            range_to_loci({"chapter": 15, "verse": 1}, {"chapter": 14, "verse": 15})

    def test_a_descending_verse_range_in_one_chapter_raises(self) -> None:
        """The same refusal the chapter above gets, which this branch lacked."""
        with self.assertRaises(ValueError):
            range_to_loci({"chapter": 24, "verse": 9}, {"chapter": 24, "verse": 3})

    def test_an_open_end_is_not_mistaken_for_a_descending_range(self) -> None:
        """A whole chapter has no verses to order, and must still resolve."""
        self.assertEqual(
            range_to_loci({"chapter": 24, "verse": None}, {"chapter": 24, "verse": None}),
            [{"chapter": 24, "first": None, "last": None}],
        )

    def test_a_range_without_a_chapter_yields_nothing(self) -> None:
        self.assertEqual(range_to_loci({}, {}), [])


class WholeChapterDepartureTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        from _loci import edition_departures

        cls.departures, cls.refused = edition_departures("Esth", {
            key: [{"chapter": 13, "first": None, "last": None}]
            for key in ("vulgate", "hebrew", "hebrew-unnumbered-titles")
        }, {})

    def test_whole_esther_redirects_to_held_separate_book(self) -> None:
        for edition in ("king-james-version", "revised-version-1895"):
            with self.subTest(edition=edition):
                self.assertEqual(self.departures.get(edition), [
                    {"book": "EsthGr", "chapter": 13, "first": 1, "last": 18},
                ])
                self.assertNotIn(edition, self.refused)

    def test_whole_esther_keeps_recorded_refusal(self) -> None:
        self.assertNotIn("catholic-public-domain-version", self.departures)
        self.assertIn("no exact selection recorded", self.refused.get(
            "catholic-public-domain-version", ""))

    def test_partial_alias_domain_does_not_become_a_whole_chapter(self) -> None:
        self.assertNotIn("world-english-bible-catholic", self.departures)
        self.assertIn("Esth 13:1", self.refused.get(
            "world-english-bible-catholic", ""))

    def test_whole_psalm_keeps_native_open_extent(self) -> None:
        from _loci import edition_readers, placed

        reader = next(row for row in edition_readers()
                      if row.id == "catholic-public-domain-version")
        self.assertIn(("Ps", 13), reader.chapters)
        locus = {"chapter": 13, "first": None, "last": None}
        self.assertEqual(placed(reader, "Ps", [locus]), ([locus], ""))

    def test_ordinary_whole_chapter_without_aliases_is_unchanged(self) -> None:
        from _loci import edition_readers, placed

        reader = next(row for row in edition_readers()
                      if row.id == "king-james-version")
        self.assertNotIn(("Gen", 1), reader.chapters)
        locus = {"chapter": 1, "first": None, "last": None}
        self.assertEqual(placed(reader, "Gen", [locus]), ([locus], ""))
