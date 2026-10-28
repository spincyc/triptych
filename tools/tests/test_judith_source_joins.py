"""Judith source joins preserve native verses and refuse inexact selections.

The source comparison establishes one whole-verse join, Vulgate 15:10 to
native 15:9, in the three Greek-division editions. Their native 13:18 combines
Vulgate 13:23 and 13:24; it is not an exact singleton carrier for either.
The adjacent differences are textual readings, not a chapter-wide offset.
"""
from __future__ import annotations

import sys
import unittest
from importlib.machinery import SourceFileLoader
from importlib.util import module_from_spec, spec_from_loader
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))

import _loci  # noqa: E402

loader = SourceFileLoader("_judith_source_joins_index_bible", str(ROOT / "tools/index-bible"))
index = module_from_spec(spec_from_loader(loader.name, loader))
loader.exec_module(index)

GREEK_DIVISION = (
    "world-english-bible-catholic",
    "king-james-version",
    "revised-version-1895",
)
LATIN_CONTROLS = (
    "douay-rheims",
    "douay-rheims-american-1899",
    "clementine-vulgate",
    "catholic-public-domain-version",
)
# These distinguish source findings from a generic out-of-bounds failure. They
# assert the material reasons without freezing the full editorial prose.
REFUSAL_DETAILS = {
    22: ("13:22", "13:17", "Judith", "God", "addressee", "no exact"),
    23: ("13:23", "13:24", "13:18", "following blessing", "no exact"),
    24: ("13:23", "13:24", "13:18", "preceding blessing", "no exact"),
    25: ("13:25", "13:19-20", "praise/name", "hope/heart", "13:26", "no exact"),
}


def span(chapter: int, first: int, last: int | None = None) -> dict:
    return {
        "begin": {"chapter": chapter, "verse": first},
        "end": {"chapter": chapter, "verse": first if last is None else last},
    }


def locus(chapter: int, first: int, last: int | None = None) -> dict:
    return {"chapter": chapter, "first": first, "last": first if last is None else last}


class JudithSourceJoins(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        # Registry and parsers select the active edition-owned artifacts. No
        # artifact basename, directory count, historical ID or text is copied.
        cls.bibles = {
            name: index.Bible(index.SOURCE_ROOT / str(index.EDITIONS[name]["artifacts"]))
            for name in (*GREEK_DIVISION, *LATIN_CONTROLS)
        }
        cls.readers = {reader.id: reader for reader in _loci.edition_readers()}

    def assert_precise_refusal(self, problem: str, verse: int) -> None:
        for detail in REFUSAL_DETAILS[verse]:
            self.assertIn(detail, problem)

    def test_15_10_reads_the_exact_complete_native_15_9_body(self) -> None:
        for edition in GREEK_DIVISION:
            with self.subTest(edition=edition):
                bible = self.bibles[edition]
                expected = bible.verses[("Jdt", 15, 9)]
                self.assertNotEqual(expected, bible.verses[("Jdt", 15, 10)])
                self.assertEqual(bible.carrier("Jdt", 15, 10), ("Jdt", 15, 9))
                self.assertEqual(bible.verse("Jdt", 15, 10), expected)
                text, problem, _opened, _closed = bible.span("Jdt", span(15, 10))
                self.assertEqual((text, problem), ([expected], ""))

    def test_13_22_through_25_refuse_with_their_checked_source_reasons(self) -> None:
        for edition in GREEK_DIVISION:
            for verse in REFUSAL_DETAILS:
                with self.subTest(edition=edition, verse=verse):
                    bible = self.bibles[edition]
                    self.assertIsNone(bible.carrier("Jdt", 13, verse))
                    self.assertIsNone(bible.verse("Jdt", 13, verse))
                    text, problem, _opened, _closed = bible.span("Jdt", span(13, verse))
                    self.assertEqual(text, [])
                    self.assert_precise_refusal(problem, verse)

    def test_public_singleton_refusals_retain_the_same_source_reasons(self) -> None:
        for edition in GREEK_DIVISION:
            for verse in REFUSAL_DETAILS:
                with self.subTest(edition=edition, verse=verse):
                    moved, problem = _loci.placed(self.readers[edition], "Jdt", [locus(13, verse)])
                    self.assertEqual(moved, [])
                    self.assert_precise_refusal(problem, verse)

    def test_public_15_10_selects_one_native_verse_without_interpolation(self) -> None:
        native = [locus(15, 9)]
        for edition in GREEK_DIVISION:
            with self.subTest(edition=edition):
                self.assertEqual(
                    _loci.placed(self.readers[edition], "Jdt", [locus(15, 10)]),
                    (native, ""),
                )
                # Read exactly the projected native range from the edition's
                # native verse dictionary. No whole chapter or synthesized text.
                moved, _problem = _loci.placed(self.readers[edition], "Jdt", [locus(15, 10)])
                selected = [
                    self.bibles[edition].verses[("Jdt", row["chapter"], verse)]
                    for row in moved
                    for verse in range(row["first"], row["last"] + 1)
                ]
                self.assertEqual(selected, [self.bibles[edition].verses[("Jdt", 15, 9)]])

    def test_singleton_13_23_never_widens_to_the_held_combined_carrier(self) -> None:
        addressings = {reader.addressing for reader in self.readers.values()}
        singleton = {addressing: [locus(13, 23)] for addressing in addressings}
        departures, refused = _loci.edition_departures("Jdt", singleton, {})
        for edition in GREEK_DIVISION:
            with self.subTest(edition=edition):
                # Native 13:18 really is held. That cannot justify returning its
                # following blessing as if it belonged to a 13:23-only query.
                self.assertTrue(self.bibles[edition].verses[("Jdt", 13, 18)])
                self.assertNotIn(edition, departures)
                self.assertIn(edition, refused)
                self.assert_precise_refusal(refused[edition], 23)
                self.assertEqual(
                    self.bibles[edition].passage("Jdt", [span(13, 23)])[0], ""
                )

    def test_appointed_13_selections_do_not_return_plausible_partial_passages(self) -> None:
        selections = {
            "comm-septem-dolorum": [locus(13, 22), locus(13, 23, 25)],
            "assumptione": [locus(13, 22, 25), locus(15, 10)],
            "septem-dolorum": [locus(13, 22), locus(13, 23, 25)],
            "conceptione-immaculata-gradual": [locus(13, 23)],
        }
        for edition in GREEK_DIVISION:
            for name, selection in selections.items():
                with self.subTest(edition=edition, selection=name):
                    moved, problem = _loci.placed(self.readers[edition], "Jdt", selection)
                    self.assertEqual(moved, [])
                    self.assertIn("no exact", problem)
                    spans = [span(row["chapter"], row["first"], row["last"]) for row in selection]
                    text, problem = self.bibles[edition].passage("Jdt", spans)
                    self.assertEqual(text, "")
                    self.assertIn("no exact", problem)

    def test_four_latin_controls_keep_native_addresses_and_complete_bodies(self) -> None:
        points = [(13, verse) for verse in REFUSAL_DETAILS] + [(15, 10)]
        for edition in LATIN_CONTROLS:
            for chapter, verse in points:
                with self.subTest(edition=edition, chapter=chapter, verse=verse):
                    bible = self.bibles[edition]
                    expected = bible.verses[("Jdt", chapter, verse)]
                    self.assertEqual(bible.carrier("Jdt", chapter, verse), ("Jdt", chapter, verse))
                    text, problem, _opened, _closed = bible.span("Jdt", span(chapter, verse))
                    self.assertEqual((text, problem), ([expected], ""))
                    unchanged = [locus(chapter, verse)]
                    self.assertEqual(
                        _loci.placed(self.readers[edition], "Jdt", unchanged), (unchanged, "")
                    )


if __name__ == "__main__":
    unittest.main()
