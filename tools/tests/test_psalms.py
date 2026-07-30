"""Tests for Vulgate/Hebrew psalm numbering conversion."""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))

import _psalms  # noqa: E402

convert_chapter = _psalms.convert_chapter
convert_reference = _psalms.convert_reference
vulgate_to_hebrew = _psalms.vulgate_to_hebrew
hebrew_to_vulgate = _psalms.hebrew_to_vulgate
NumberingError = _psalms.NumberingError


class LiturgicalAnchorTests(unittest.TestCase):
    """The Advent introit *Ad te levavi* is Psalm 24 in the 1962 missal and
    Psalm 25 in the postconciliar books; the module exists to reconcile them."""

    def test_ad_te_levavi_vulgate_twenty_four_is_hebrew_twenty_five(self) -> None:
        chapter, caveat = convert_chapter(24, "vulgate", "hebrew")
        self.assertEqual(chapter, 25)
        self.assertEqual(caveat, "")

    def test_ad_te_levavi_hebrew_twenty_five_is_vulgate_twenty_four(self) -> None:
        chapter, caveat = convert_chapter(25, "hebrew", "vulgate")
        self.assertEqual(chapter, 24)
        self.assertEqual(caveat, "")

    def test_ad_te_levavi_round_trips_through_a_reference(self) -> None:
        chapter, _ = convert_reference("Psalms", 24, "vulgate", "hebrew")
        self.assertEqual(chapter, 25)
        back, _ = convert_reference("Psalms", chapter, "hebrew", "vulgate")
        self.assertEqual(back, 24)


class IdentityRangeTests(unittest.TestCase):
    def test_first_eight_psalms_are_identical_in_both_systems(self) -> None:
        for chapter in range(1, 9):
            with self.subTest(chapter=chapter):
                self.assertEqual(vulgate_to_hebrew(chapter), (chapter, ""))
                self.assertEqual(hebrew_to_vulgate(chapter), (chapter, ""))

    def test_final_three_psalms_are_identical_in_both_systems(self) -> None:
        for chapter in range(148, 151):
            with self.subTest(chapter=chapter):
                self.assertEqual(vulgate_to_hebrew(chapter), (chapter, ""))
                self.assertEqual(hebrew_to_vulgate(chapter), (chapter, ""))


class OffsetRangeTests(unittest.TestCase):
    def test_vulgate_ten_to_one_hundred_twelve_gains_one(self) -> None:
        for chapter in range(10, 113):
            with self.subTest(chapter=chapter):
                self.assertEqual(vulgate_to_hebrew(chapter), (chapter + 1, ""))

    def test_vulgate_one_sixteen_to_one_forty_five_gains_one(self) -> None:
        for chapter in range(116, 146):
            with self.subTest(chapter=chapter):
                self.assertEqual(vulgate_to_hebrew(chapter), (chapter + 1, ""))

    def test_hebrew_eleven_to_one_thirteen_loses_one(self) -> None:
        for chapter in range(11, 114):
            with self.subTest(chapter=chapter):
                self.assertEqual(hebrew_to_vulgate(chapter), (chapter - 1, ""))

    def test_hebrew_one_seventeen_to_one_forty_six_loses_one(self) -> None:
        for chapter in range(117, 147):
            with self.subTest(chapter=chapter):
                self.assertEqual(hebrew_to_vulgate(chapter), (chapter - 1, ""))

    def test_offsets_are_reported_without_a_caveat(self) -> None:
        for chapter in (10, 112, 116, 145):
            with self.subTest(chapter=chapter):
                self.assertEqual(vulgate_to_hebrew(chapter)[1], "")


class SplitTests(unittest.TestCase):
    """Vulgate psalms that the Masoretic text divides."""

    def test_vulgate_nine_splits_by_verse(self) -> None:
        for verse, expected in ((1, 9), (21, 9), (22, 10), (39, 10)):
            with self.subTest(verse=verse):
                chapter, caveat = vulgate_to_hebrew(9, verse)
                self.assertEqual(chapter, expected)
                self.assertTrue(caveat)

    def test_vulgate_nine_rejects_a_verse_outside_both_halves(self) -> None:
        with self.assertRaises(NumberingError):
            vulgate_to_hebrew(9, 40)

    def test_vulgate_one_thirteen_splits_by_verse(self) -> None:
        for verse, expected in ((1, 114), (8, 114), (9, 115), (26, 115)):
            with self.subTest(verse=verse):
                chapter, caveat = vulgate_to_hebrew(113, verse)
                self.assertEqual(chapter, expected)
                self.assertTrue(caveat)

    def test_hebrew_one_sixteen_splits_by_verse(self) -> None:
        for verse, expected in ((1, 114), (9, 114), (10, 115), (19, 115)):
            with self.subTest(verse=verse):
                chapter, caveat = hebrew_to_vulgate(116, verse)
                self.assertEqual(chapter, expected)
                self.assertTrue(caveat)

    def test_hebrew_one_forty_seven_splits_by_verse(self) -> None:
        for verse, expected in ((1, 146), (11, 146), (12, 147), (20, 147)):
            with self.subTest(verse=verse):
                chapter, caveat = hebrew_to_vulgate(147, verse)
                self.assertEqual(chapter, expected)
                self.assertTrue(caveat)


class MergeTests(unittest.TestCase):
    """Chapters that correspond to only part of a chapter in the other system."""

    def test_vulgate_one_fourteen_and_one_fifteen_are_halves_of_hebrew_one_sixteen(
        self,
    ) -> None:
        for vulgate in (114, 115):
            with self.subTest(vulgate=vulgate):
                chapter, caveat = vulgate_to_hebrew(vulgate)
                self.assertEqual(chapter, 116)
                self.assertTrue(caveat)
        self.assertIn("116:1-9", vulgate_to_hebrew(114)[1])
        self.assertIn("116:10-19", vulgate_to_hebrew(115)[1])

    def test_vulgate_one_forty_six_and_one_forty_seven_are_halves_of_hebrew_one_forty_seven(
        self,
    ) -> None:
        for vulgate in (146, 147):
            with self.subTest(vulgate=vulgate):
                chapter, caveat = vulgate_to_hebrew(vulgate)
                self.assertEqual(chapter, 147)
                self.assertTrue(caveat)
        self.assertIn("147:1-11", vulgate_to_hebrew(146)[1])
        self.assertIn("147:12-20", vulgate_to_hebrew(147)[1])

    def test_hebrew_nine_and_ten_both_map_to_vulgate_nine(self) -> None:
        for hebrew in (9, 10):
            with self.subTest(hebrew=hebrew):
                chapter, caveat = hebrew_to_vulgate(hebrew)
                self.assertEqual(chapter, 9)
                self.assertTrue(caveat)

    def test_hebrew_one_fourteen_and_one_fifteen_both_map_to_vulgate_one_thirteen(
        self,
    ) -> None:
        for hebrew in (114, 115):
            with self.subTest(hebrew=hebrew):
                chapter, caveat = hebrew_to_vulgate(hebrew)
                self.assertEqual(chapter, 113)
                self.assertTrue(caveat)

    def test_merged_halves_ignore_a_supplied_verse(self) -> None:
        self.assertEqual(hebrew_to_vulgate(10, 1)[0], 9)
        self.assertEqual(hebrew_to_vulgate(115, 26)[0], 113)


class AmbiguityTests(unittest.TestCase):
    """A split with no verse is an error, never a guess."""

    def test_hebrew_one_sixteen_without_a_verse_raises(self) -> None:
        with self.assertRaises(NumberingError):
            hebrew_to_vulgate(116)
        with self.assertRaises(NumberingError):
            convert_chapter(116, "hebrew", "vulgate")

    def test_hebrew_one_forty_seven_without_a_verse_raises(self) -> None:
        with self.assertRaises(NumberingError):
            hebrew_to_vulgate(147)
        with self.assertRaises(NumberingError):
            convert_chapter(147, "hebrew", "vulgate")

    def test_vulgate_nine_without_a_verse_raises(self) -> None:
        with self.assertRaises(NumberingError):
            vulgate_to_hebrew(9)
        with self.assertRaises(NumberingError):
            convert_chapter(9, "vulgate", "hebrew")

    def test_numbering_error_is_a_value_error(self) -> None:
        self.assertTrue(issubclass(NumberingError, ValueError))


class SameSystemTests(unittest.TestCase):
    def test_every_chapter_is_unchanged_within_its_own_system(self) -> None:
        for system in _psalms.SYSTEMS:
            for chapter in range(1, 151):
                with self.subTest(system=system, chapter=chapter):
                    self.assertEqual(convert_chapter(chapter, system, system), (chapter, ""))

    def test_same_system_conversion_never_needs_a_verse(self) -> None:
        for chapter in (9, 113, 116, 147):
            with self.subTest(chapter=chapter):
                self.assertEqual(convert_chapter(chapter, "hebrew", "hebrew"), (chapter, ""))
                self.assertEqual(convert_chapter(chapter, "vulgate", "vulgate"), (chapter, ""))


class ReferenceTests(unittest.TestCase):
    def test_non_psalm_books_pass_through_unchanged(self) -> None:
        for source, target in (("vulgate", "hebrew"), ("hebrew", "vulgate")):
            with self.subTest(source=source):
                self.assertEqual(convert_reference("Isaiah", 7, source, target), (7, ""))
                self.assertEqual(convert_reference("Genesis", 9, source, target), (9, ""))
                self.assertEqual(convert_reference("Matthew", 116, source, target), (116, ""))

    def test_psalms_are_renumbered(self) -> None:
        self.assertEqual(convert_reference("Psalms", 51, "hebrew", "vulgate"), (50, ""))
        self.assertEqual(convert_reference("Psalms", 50, "vulgate", "hebrew"), (51, ""))

    def test_psalm_verse_is_forwarded_to_the_split_logic(self) -> None:
        self.assertEqual(convert_reference("Psalms", 116, "hebrew", "vulgate", 10)[0], 115)
        self.assertEqual(convert_reference("Psalms", 9, "vulgate", "hebrew", 25)[0], 10)


class InvalidInputTests(unittest.TestCase):
    def test_unknown_source_system_raises(self) -> None:
        with self.assertRaises(NumberingError):
            convert_chapter(24, "septuagint", "hebrew")

    def test_unknown_target_system_raises(self) -> None:
        with self.assertRaises(NumberingError):
            convert_chapter(24, "vulgate", "greek")

    def test_unknown_system_raises_even_when_source_and_target_agree(self) -> None:
        with self.assertRaises(NumberingError):
            convert_chapter(24, "coptic", "coptic")

    def test_chapters_outside_the_psalter_raise(self) -> None:
        for chapter in (0, 151, -1, 200):
            with self.subTest(chapter=chapter):
                with self.assertRaises(NumberingError):
                    vulgate_to_hebrew(chapter)
                with self.assertRaises(NumberingError):
                    hebrew_to_vulgate(chapter)
                with self.assertRaises(NumberingError):
                    convert_chapter(chapter, "vulgate", "hebrew")
                with self.assertRaises(NumberingError):
                    convert_chapter(chapter, "hebrew", "vulgate")


class RoundTripTests(unittest.TestCase):
    """Converting out and back returns the original chapter, except where the
    systems genuinely lose information at a merge boundary."""

    # Vulgate 115 and 147 are the SECOND halves of merged Hebrew psalms:
    # Vulgate 115:1 is Hebrew 116:10 and Vulgate 147:1 is Hebrew 147:12. A round
    # trip that carries verse 1 across therefore lands in the first half
    # (Vulgate 114 and 146). Those two are exercised in the tests below with a
    # verse taken inside the correct half.
    VULGATE_SECOND_HALVES = {115, 147}

    # Hebrew 10 and 115 are likewise the second halves of Vulgate 9 and 113.
    HEBREW_SECOND_HALVES = {10, 115}

    def test_vulgate_chapters_round_trip_at_verse_one(self) -> None:
        for chapter in range(1, 151):
            if chapter in self.VULGATE_SECOND_HALVES:
                continue
            with self.subTest(chapter=chapter):
                hebrew, _ = convert_chapter(chapter, "vulgate", "hebrew", 1)
                back, _ = convert_chapter(hebrew, "hebrew", "vulgate", 1)
                self.assertEqual(back, chapter)

    def test_vulgate_second_halves_round_trip_with_a_verse_in_that_half(self) -> None:
        for vulgate, hebrew, hebrew_verse in ((115, 116, 10), (147, 147, 12)):
            with self.subTest(vulgate=vulgate):
                converted, _ = convert_chapter(vulgate, "vulgate", "hebrew", 1)
                self.assertEqual(converted, hebrew)
                back, _ = convert_chapter(hebrew, "hebrew", "vulgate", hebrew_verse)
                self.assertEqual(back, vulgate)

    def test_hebrew_chapters_round_trip_at_verse_one(self) -> None:
        for chapter in range(1, 151):
            if chapter in self.HEBREW_SECOND_HALVES:
                continue
            with self.subTest(chapter=chapter):
                vulgate, _ = convert_chapter(chapter, "hebrew", "vulgate", 1)
                back, _ = convert_chapter(vulgate, "vulgate", "hebrew", 1)
                self.assertEqual(back, chapter)

    def test_hebrew_second_halves_round_trip_with_a_verse_in_that_half(self) -> None:
        for hebrew, vulgate, vulgate_verse in ((10, 9, 22), (115, 113, 9)):
            with self.subTest(hebrew=hebrew):
                converted, _ = convert_chapter(hebrew, "hebrew", "vulgate", 1)
                self.assertEqual(converted, vulgate)
                back, _ = convert_chapter(vulgate, "vulgate", "hebrew", vulgate_verse)
                self.assertEqual(back, hebrew)

    def test_every_vulgate_chapter_maps_into_the_psalter(self) -> None:
        for chapter in range(1, 151):
            with self.subTest(chapter=chapter):
                hebrew, _ = convert_chapter(chapter, "vulgate", "hebrew", 1)
                self.assertTrue(1 <= hebrew <= 150)

    def test_every_hebrew_chapter_maps_into_the_psalter(self) -> None:
        for chapter in range(1, 151):
            with self.subTest(chapter=chapter):
                vulgate, _ = convert_chapter(chapter, "hebrew", "vulgate", 1)
                self.assertTrue(1 <= vulgate <= 150)


if __name__ == "__main__":
    unittest.main()
