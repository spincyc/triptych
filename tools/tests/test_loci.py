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
        """The defect that produced nothing on the page: first above last."""
        for begin, end in (
            ({"chapter": 14, "verse": 15}, {"chapter": 15, "verse": 1}),
            ({"chapter": 13, "verse": 17}, {"chapter": 14, "verse": 14}),
            ({"chapter": 63, "verse": 16}, {"chapter": 64, "verse": 7}),
        ):
            for locus in range_to_loci(begin, end):
                if locus["first"] is not None and locus["last"] is not None:
                    self.assertLessEqual(locus["first"], locus["last"], locus)


class RefusalTests(unittest.TestCase):
    def test_a_descending_chapter_range_raises(self) -> None:
        with self.assertRaises(ValueError):
            range_to_loci({"chapter": 15, "verse": 1}, {"chapter": 14, "verse": 15})

    def test_a_range_without_a_chapter_yields_nothing(self) -> None:
        self.assertEqual(range_to_loci({}, {}), [])
