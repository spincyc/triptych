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


class VerseBoundTests(unittest.TestCase):
    """Every psalm is bounded, so a reference carried in the wrong system is
    caught by its verse number rather than passing as a plausible one."""

    def test_the_whole_psalter_is_bounded_in_both_systems(self) -> None:
        for system in _psalms.SYSTEMS:
            for chapter in range(1, _psalms.LAST_PSALM + 1):
                with self.subTest(system=system, chapter=chapter):
                    self.assertIsInstance(_psalms.psalm_ceiling(chapter, system), int)

    def test_the_vulgate_bounds_are_those_the_editions_print(self) -> None:
        # The two psalms the Vulgate prints under a pre-split numbering.
        self.assertEqual(_psalms.psalm_ceiling(115, "vulgate"), 19)
        self.assertEqual(_psalms.psalm_ceiling(147, "vulgate"), 20)
        self.assertEqual(_psalms.psalm_ceiling(118, "vulgate"), 176)
        self.assertIn("precedes", _psalms.validate_psalm(115, 9, "vulgate"))

    def test_a_hebrew_reference_beyond_its_psalm_is_reported(self) -> None:
        # Psalm 118 is the long one only in the Vulgate; Hebrew 118 ends at 29.
        problem = _psalms.validate_psalm(118, 137, "hebrew")
        self.assertIn("ends at verse 29", problem)
        self.assertEqual(_psalms.validate_psalm(118, 137, "vulgate"), "")

    def test_a_hebrew_psalm_ends_where_its_vulgate_host_divides(self) -> None:
        """Vulgate 9 runs to 39, but Hebrew 9 stops at 21 and Hebrew 10 at 18;
        a bound taken from the host would pass both of the references below."""
        self.assertEqual(_psalms.psalm_ceiling(9, "hebrew"), 21)
        self.assertEqual(_psalms.psalm_ceiling(10, "hebrew"), 18)
        self.assertEqual(_psalms.psalm_ceiling(9, "vulgate"), 39)
        self.assertNotEqual(_psalms.validate_psalm(9, 22, "hebrew"), "")
        self.assertNotEqual(_psalms.validate_psalm(10, 19, "hebrew"), "")

    def test_the_concordance_matches_the_tracked_verse_text(self) -> None:
        """The lookup table is numbering, and the verse text is scripture; if
        they ever disagree the table is describing a psalter no edition has."""
        import collections
        import csv

        artifacts = (
            ROOT / "src/sources/works/english-college-of-douay/douay-rheims-bible"
            "/editions/challoner-gutenberg-1581/artifacts"
        )
        found = sorted(artifacts.glob("verse-text-*-psalms-*/*.tsv"))
        self.assertEqual(len(found), 1)
        printed: dict[int, set[int]] = collections.defaultdict(set)
        with found[0].open(encoding="utf-8", newline="") as handle:
            for row in csv.DictReader(handle, delimiter="\t"):
                printed[int(row["chapter"])].add(int(row["verse"]))
        self.assertEqual(sum(len(verses) for verses in printed.values()), 2528)
        for chapter, verses in printed.items():
            with self.subTest(chapter=chapter):
                first, last = min(verses), max(verses)
                self.assertEqual(_psalms.psalm_ceiling(chapter, "vulgate"), last)
                self.assertEqual(_psalms.validate_psalm(chapter, first, "vulgate"), "")
                self.assertNotEqual(_psalms.validate_psalm(chapter, last + 1, "vulgate"), "")

    def test_every_verse_converts_and_returns(self) -> None:
        """The table is a bijection, so a round trip is the identity on all
        2528 verses; nothing is dropped at a join and nothing doubles up."""
        seen: set[tuple[int, int]] = set()
        for chapter in range(1, _psalms.LAST_PSALM + 1):
            first, last = _psalms.psalm_extent(chapter, "vulgate")
            for verse in range(first, last + 1):
                hebrew = _psalms.convert_point(chapter, verse, "vulgate", "hebrew")
                self.assertNotIn(hebrew[:2], seen)
                seen.add(hebrew[:2])
                back = _psalms.convert_point(hebrew[0], hebrew[1], "hebrew", "vulgate")
                self.assertEqual(back[:2], (chapter, verse))
        self.assertEqual(len(seen), 2528)

    def test_a_psalm_outside_the_psalter_is_reported(self) -> None:
        for chapter in (0, 151, "24", None):
            with self.subTest(chapter=chapter):
                self.assertIn("outside the psalter", _psalms.validate_psalm(chapter, 1, "vulgate"))

    def test_a_reference_without_a_verse_is_not_rejected(self) -> None:
        self.assertEqual(_psalms.validate_psalm(118, None, "hebrew"), "")

    def test_an_unknown_system_raises(self) -> None:
        with self.assertRaises(NumberingError):
            _psalms.validate_psalm(24, 1, "septuagint")


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


class EnglishTitleConventionTests(unittest.TestCase):
    """The offset an edition takes on by leaving a psalm's inscription unnumbered.

    The Hebrew numbering counts the inscription as a verse and the English
    convention does not, so an English bible's Psalm 51:1 is the *Miserere* a
    Hebrew-numbered calendar cites as 51:3. Nothing here converts a chapter:
    the two agree on which psalm, and differ only on where its verses start.
    """

    def test_the_miserere_is_two_verses_earlier_in_english(self) -> None:
        self.assertEqual(_psalms.english_verse(51, 3), (1, ""))

    def test_a_psalm_with_a_one_verse_inscription_shifts_by_one(self) -> None:
        self.assertEqual(_psalms.english_verse(3, 2), (1, ""))

    def test_a_psalm_with_no_inscription_does_not_shift(self) -> None:
        self.assertEqual(_psalms.english_verse(23, 1), (1, ""))
        self.assertEqual(_psalms.english_verse(119, 176), (176, ""))

    def test_an_inscription_has_no_english_verse_at_all(self) -> None:
        found, problem = _psalms.english_verse(51, 1)
        self.assertIsNone(found)
        self.assertIn("inscription", problem)

    def test_a_psalm_the_two_conventions_divide_differently_refuses(self) -> None:
        for chapter in (2, 4, 29, 100, 150):
            with self.subTest(chapter=chapter):
                found, problem = _psalms.english_verse(chapter, 1)
                self.assertIsNone(found)
                self.assertIn("divide", problem)

    def test_a_verse_outside_its_psalm_is_an_error_not_a_refusal(self) -> None:
        with self.assertRaises(NumberingError):
            _psalms.english_verse(23, 99)

    def test_every_convertible_psalm_lands_inside_the_english_psalm(self) -> None:
        """A converted verse must exist in an edition that prints the convention.

        The King James Version is that edition here, and reading its extents
        rather than restating them is what would catch a concordance whose
        English column had drifted from the text it describes.
        """
        import csv

        artifacts = (
            ROOT / "src/sources/works/church-of-england/king-james-version"
            / "editions/ebible-engkjv/artifacts"
        )
        found = sorted(artifacts.glob("verse-text-*-psalms-*/*.tsv"))
        self.assertEqual(len(found), 1)
        printed: dict[int, set[int]] = {}
        with found[0].open(encoding="utf-8", newline="") as handle:
            for row in csv.DictReader(handle, delimiter="\t"):
                printed.setdefault(int(row["chapter"]), set()).add(int(row["verse"]))
        converted = 0
        for chapter in range(1, 151):
            first, last = _psalms.psalm_extent(chapter, "hebrew")
            for verse in range(first, last + 1):
                English, problem = _psalms.english_verse(chapter, verse)
                if English is None:
                    continue
                converted += 1
                with self.subTest(chapter=chapter, verse=verse):
                    self.assertIn(English, printed[chapter])
        self.assertGreater(converted, 2000)


if __name__ == "__main__":
    unittest.main()
