"""Tests for the deuterocanonical numbering concordance.

Esther, Ecclesiasticus and Daniel are divided differently by the Latin and the
Greek traditions, and both calendars cite the divergences. Until this table
existed a citation of `Ecclesiasticus 36:18` against the King James returned
"the belly devoureth all meats" — real text, at the right numbers, entirely the
wrong words, and nothing counted it a failure.

Two things are held here. The readings themselves, so a correction cannot be
undone silently; and the load-time validation, because a concordance nothing
checks is a hand-typed lookup table with a better name.
"""

from __future__ import annotations

import csv
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))

import _deuterocanon as deuterocanon  # noqa: E402

VULGATE = "vulgate"
GREEK = "greek"
WEB = "world-english-catholic"


def reset() -> None:
    for cached in (
        deuterocanon._rows,
        deuterocanon._index,
        deuterocanon._printed,
        deuterocanon._edition_text,
        deuterocanon._departures,
    ):
        cached.cache_clear()


class Reading(unittest.TestCase):
    """What the concordance says, read against the verses it was compiled from."""

    def setUp(self) -> None:
        reset()

    def where(self, book, chapter, verse, source=VULGATE, target=GREEK):
        found, problem = deuterocanon.convert_verse(book, chapter, verse, source, target)
        self.assertEqual(problem, "", f"{book} {chapter}:{verse} refused: {problem}")
        assert found is not None
        return f"{found.book} {found.chapter}:{found.first}"

    def test_susanna_and_bel_are_not_verse_for_verse(self):
        """Daniel 13:65 is Bel 1, so Bel runs one ahead of Vulgate Daniel 14.

        `guidance/versification.md` section 7.2 says these two are pure chapter
        relabelling, verse for verse. The tracked text says otherwise, and the
        difference reaches a citation the 1962 calendar makes.
        """
        self.assertEqual(self.where("Dan", 13, 1), "Sus 1:1")
        self.assertEqual(self.where("Dan", 13, 64), "Sus 1:64")
        self.assertEqual(self.where("Dan", 13, 65), "Bel 1:1")
        self.assertEqual(self.where("Dan", 14, 1), "Bel 1:2")
        self.assertEqual(self.where("Dan", 14, 27), "Bel 1:28")
        self.assertEqual(self.where("Dan", 14, 41), "Bel 1:42")

    def test_the_last_verse_of_daniel_has_no_greek_counterpart(self):
        found, problem = deuterocanon.convert_verse("Dan", 14, 42, VULGATE, GREEK)
        self.assertIsNone(found)
        self.assertIn("no counterpart", problem)

    def test_the_benedicite_is_reordered_and_not_offset(self):
        """Between 3:53 and 3:78 the two traditions order the canticle differently."""
        self.assertEqual(self.where("Dan", 3, 51), "SgThree 1:28")
        self.assertEqual(self.where("Dan", 3, 53), "SgThree 1:31")
        self.assertEqual(self.where("Dan", 3, 54), "SgThree 1:33")
        self.assertEqual(self.where("Dan", 3, 55), "SgThree 1:32")
        self.assertEqual(self.where("Dan", 3, 58), "SgThree 1:37")
        self.assertEqual(self.where("Dan", 3, 59), "SgThree 1:36")
        self.assertEqual(self.where("Dan", 3, 77), "SgThree 1:56")
        self.assertEqual(self.where("Dan", 3, 78), "SgThree 1:55")
        self.assertEqual(self.where("Dan", 3, 79), "SgThree 1:57")

    def test_one_vulgate_verse_becomes_two_greek_ones(self):
        """Daniel 3:52 carries both blessings the Greek numbers 29 and 30."""
        found, problem = deuterocanon.convert_verse("Dan", 3, 52, VULGATE, GREEK)
        self.assertIsNone(found)
        self.assertIn("SgThree 1:29-30", problem)

    def test_the_chapter_three_and_four_boundary_moves(self):
        self.assertEqual(self.where("Dan", 3, 91), "Dan 3:24")
        self.assertEqual(self.where("Dan", 3, 98), "Dan 4:1")
        self.assertEqual(self.where("Dan", 4, 1), "Dan 4:4")
        self.assertEqual(self.where("Dan", 4, 34), "Dan 4:37")

    def test_esther_fifteen_needs_three_relations_at_once(self):
        """Absent, merged and split, in one chapter of one book."""
        absent, why = deuterocanon.convert_verse("Esth", 15, 1, VULGATE, GREEK)
        self.assertIsNone(absent)
        self.assertIn("no counterpart", why)

        self.assertEqual(self.where("Esth", 15, 4), "EsthGr 15:1")

        merged, note = deuterocanon.convert_verse("Esth", 15, 13, VULGATE, GREEK)
        assert merged is not None
        self.assertEqual((merged.book, merged.chapter, merged.first), ("EsthGr", 15, 10))
        self.assertIn("superset", note)

        split, why = deuterocanon.convert_verse("Esth", 15, 15, VULGATE, GREEK)
        self.assertIsNone(split)
        self.assertIn("EsthGr 15:11-12", why)

    def test_the_esther_additions_keep_their_numbers_outside_chapter_fifteen(self):
        self.assertEqual(self.where("Esth", 13, 9), "EsthGr 13:9")
        self.assertEqual(self.where("Esth", 14, 12), "EsthGr 14:12")
        self.assertEqual(self.where("Esth", 16, 24), "EsthGr 16:24")

    def test_ecclesiasticus_refuses_and_says_why(self):
        found, problem = deuterocanon.convert_verse("Ecclus", 24, 1, VULGATE, GREEK)
        self.assertIsNone(found)
        self.assertIn("all fifty-one chapters", problem)

    def test_the_one_ecclesiasticus_locus_that_was_read(self):
        """Da pacem Domine is the Vulgate's 36:18 and the Greek's 36:16."""
        self.assertEqual(self.where("Ecclus", 36, 18), "Ecclus 36:16")

    def test_the_world_english_edition_is_two_hops_away(self):
        hops = (VULGATE, GREEK, WEB)
        for book, chapter, verse, expected in (
            ("Dan", 13, 65, "Dan 14:1"),
            ("Dan", 14, 27, "Dan 14:28"),
            ("Dan", 3, 77, "Dan 3:78"),
            ("Esth", 13, 9, "Esth 4:19"),
            ("Ecclus", 36, 18, "Ecclus 36:16"),
        ):
            found, problem = deuterocanon.convert_through(book, chapter, verse, hops)
            self.assertEqual(problem, "", f"{book} {chapter}:{verse}: {problem}")
            assert found is not None
            self.assertEqual(f"{found.book} {found.chapter}:{found.first}", expected)


class Validation(unittest.TestCase):
    """A concordance that has stopped describing the library must not load."""

    def setUp(self) -> None:
        reset()
        self.addCleanup(reset)
        found = sorted(deuterocanon.CONCORDANCE_ROOT.glob(deuterocanon.CONCORDANCE_GLOB))
        self.assertEqual(len(found), 1)
        with found[0].open(encoding="utf-8", newline="") as handle:
            reader = csv.DictReader(handle, delimiter="\t")
            self.columns = list(reader.fieldnames or ())
            self.rows = list(reader)

    def load(self, rows):
        """Load a doctored copy of the table and return the complaint."""
        directory = Path(tempfile.mkdtemp())
        self.addCleanup(lambda: None)
        inside = directory / "deuterocanon-numbering-0000dead"
        inside.mkdir()
        with (inside / "deuterocanon-numbering.tsv").open(
            "w", encoding="utf-8", newline=""
        ) as handle:
            writer = csv.DictWriter(
                handle, fieldnames=self.columns, delimiter="\t", lineterminator="\n"
            )
            writer.writeheader()
            writer.writerows(rows)
        deuterocanon.CONCORDANCE_ROOT = directory
        reset()
        with self.assertRaises(deuterocanon.ConcordanceUnavailable) as caught:
            deuterocanon._rows()
        return str(caught.exception)

    def tearDown(self) -> None:
        deuterocanon.CONCORDANCE_ROOT = (
            deuterocanon.WORKS / "english-college-of-douay" / "douay-rheims-bible"
            / "editions" / "challoner-gutenberg-1581" / "artifacts"
        )
        reset()

    def find(self, **fields):
        for index, row in enumerate(self.rows):
            if all(row[key] == value for key, value in fields.items()):
                return index
        raise AssertionError(f"no row matching {fields}")

    def test_an_opening_the_witness_does_not_print_is_refused(self):
        rows = [dict(row) for row in self.rows]
        where = self.find(left_book="Sus", right_book="Dan")
        rows[where]["left_opening"] = "and there dwelt a man in babylon"
        self.assertIn("is recorded as opening", self.load(rows))

    def test_a_one_to_one_row_of_unequal_runs_is_refused(self):
        rows = [dict(row) for row in self.rows]
        rows[self.find(left_book="Sus", right_book="Dan")]["right_verses"] = "1-63"
        self.assertIn("runs of equal length", self.load(rows))

    def test_a_row_that_overruns_its_chapter_is_refused(self):
        """The ceiling comes from the text, so no ceiling can be wrong on its own."""
        rows = [dict(row) for row in self.rows]
        where = self.find(left_book="Dan", left_chapter="14", left_verses="42")
        rows[where]["left_verses"] = "42-43"
        self.assertIn("but the witness prints only", self.load(rows))

    def test_a_chapter_left_uncovered_is_refused(self):
        rows = [row for row in self.rows if not (
            row["left_book"] == "Ecclus" and row["left_chapter"] == "40"
        )]
        self.assertIn("is in the witness and in no", self.load(rows))

    def test_two_rows_claiming_one_verse_are_refused(self):
        rows = [dict(row) for row in self.rows]
        rows.append(dict(rows[self.find(left_book="Sus", right_book="Dan")]))
        self.assertIn("claimed twice", self.load(rows))

    def test_a_refusal_without_a_reason_is_refused(self):
        rows = [dict(row) for row in self.rows]
        rows[self.find(left_book="Ecclus", left_chapter="40")]["note"] = ""
        self.assertIn("must say what was looked at", self.load(rows))


class DerivedAliases(unittest.TestCase):
    """The editions' alias tables must be what the concordance derives.

    The rule the psalter learned the hard way: one table, and nothing beside it
    restating what it says. The alias rows are a mechanical expansion of the
    concordance against each edition's own verse text, and a hand edit to either
    end has to fail here rather than quietly disagree.
    """

    def setUp(self) -> None:
        reset()

    def test_every_aliased_edition_matches_its_derivation(self):
        for edition, (_, where) in sorted(deuterocanon.ALIASED.items()):
            with self.subTest(edition=edition):
                found = sorted(
                    (ROOT / "src/sources/works" / where).glob(
                        "verse-aliases-*/verse-aliases.tsv"
                    )
                )
                self.assertEqual(len(found), 1)
                with found[0].open(encoding="utf-8", newline="") as handle:
                    tracked = [
                        row
                        for row in csv.DictReader(handle, delimiter="\t")
                        if row["cited_locus"].split(".")[0] in deuterocanon.CITED_BOOKS
                    ]
                derived = deuterocanon.derive_aliases(edition)
                self.assertEqual(
                    [dict(row) for row in tracked],
                    derived,
                    f"{edition}: run `python3 scripts/_deuterocanon.py {edition}`",
                )

    def test_the_king_james_song_of_the_three_defect_is_still_there(self):
        """Its verse 55 repeats the mountains of 53; the Revised Version does not.

        The departure is declared with both openings and both are checked, so
        this is a statement about the tracked bytes, not an assertion.
        """
        departures = deuterocanon._departures("king-james-version")
        self.assertIn(("SgThree", 1, 55), departures)
        self.assertIn(("SgThree", 1, 56), departures)
        self.assertEqual(deuterocanon._departures("revised-version-1895"), {})


if __name__ == "__main__":
    unittest.main()
