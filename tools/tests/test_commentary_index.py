"""The two checks that stand between the harvest and the catena.

Both defects they catch were live in tracked artifacts and both survived a
promotion, because promotion asserted nothing about what it wrote. Neither
check is expensive; their absence was the whole failure.

`Rule 8` — a group's canonical title must not name a book that the group's own
names do not share. Aquinas's Pauline commentary is one work over ten epistles
and was named `Super Epistolam ad Romanos lectura`, so the acquisition list
would have gone looking for one tenth of it.

`Rule 5` — one stored granularity, the rest derived. The index carried both
`Psalms 24` and `Psalms 24:4`, and the two answered the same question with
different corpora.
"""

from __future__ import annotations

import importlib.machinery
import importlib.util
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
ALIASES = ROOT / "src" / "sources" / "commentary" / "work-aliases.yaml"
LEDGER = ROOT / "src" / "sources" / "commentary" / "harvest-ledger.yaml"
INDEX = ROOT / "src" / "sources" / "commentary" / "passage-commentary-index.yaml"

sys.path.insert(0, str(ROOT / "scripts"))

from _commentary import key_extents, overlapping_keys  # noqa: E402


def load_harvest():
    loader = importlib.machinery.SourceFileLoader(
        "harvest_tool", str(ROOT / "tools" / "harvest")
    )
    spec = importlib.util.spec_from_loader(loader.name, loader)
    module = importlib.util.module_from_spec(spec)
    loader.exec_module(module)
    return module


harvest = load_harvest()


def tracked_runs() -> list[dict]:
    return harvest._ledger_runs(harvest._load(LEDGER))


class BookWordTests(unittest.TestCase):
    """The lexicon is derived from the ledger, so it must not be typed here.

    What these assert is the property the derivation is for: real book names
    are in, and genre words — which outnumber them and would fire on every
    group — are out.
    """

    def setUp(self) -> None:
        self.words = harvest._book_words(tracked_runs())

    def test_a_latin_book_name_is_recognized(self) -> None:
        for word, book in (
            ("romanos", "Romans"),
            ("galatas", "Galatians"),
            ("hebraeos", "Hebrews"),
            ("amos", "Amos"),
            ("psalmos", "Psalms"),
        ):
            with self.subTest(word=word):
                self.assertEqual(self.words.get(word), book)

    def test_a_genre_word_is_not_a_book_name(self) -> None:
        """`explanatio` heads 418 psalm attributions and is still not a book.

        A share test on volume alone would take it, and every group whose
        canonical title happened to carry a common word would then fail.
        """
        for word in ("explanatio", "commentarii", "expositio", "in", "super", "lectura"):
            with self.subTest(word=word):
                self.assertNotIn(word, self.words)


class RuleEightTests(unittest.TestCase):
    def test_the_tracked_table_names_every_work_by_its_whole(self) -> None:
        document = harvest._load(ALIASES)
        harvest._check_titles_cover_the_work(
            document.get("groups") or [], tracked_runs(), str(ALIASES)
        )

    def test_a_canonical_title_naming_one_book_of_many_is_refused(self) -> None:
        groups = [
            {
                "author": "Thomas Aquinas",
                "work": "Super Epistolam ad Romanos lectura",
                "titles": [
                    "super epistolam ad romanos lectura",
                    "super epistolam ad galatas lectura",
                ],
            }
        ]
        with self.assertRaises(ValueError) as caught:
            harvest._check_titles_cover_the_work(groups, tracked_runs(), "table")
        self.assertIn("Romans", str(caught.exception))
        self.assertIn("Galatians", str(caught.exception))

    def test_a_title_naming_the_whole_passes(self) -> None:
        groups = [
            {
                "author": "Thomas Aquinas",
                "work": "Super Epistolas S. Pauli lectura",
                "titles": [
                    "super epistolas s. pauli lectura",
                    "super epistolam ad romanos lectura",
                    "super epistolam ad galatas lectura",
                ],
            }
        ]
        harvest._check_titles_cover_the_work(groups, tracked_runs(), "table")

    def test_a_single_book_work_is_not_flagged(self) -> None:
        """Every name of a one-book work names that book. Nothing to catch."""
        groups = [
            {
                "author": "Thomas Aquinas",
                "work": "Postilla super Psalmos",
                "titles": ["postilla super psalmos", "lectura super psalmos"],
            }
        ]
        harvest._check_titles_cover_the_work(groups, tracked_runs(), "table")


class ReviewedNameTests(unittest.TestCase):
    """`review.canonical_titles` is the authored half; `groups` is derived."""

    def test_a_reviewed_name_replaces_the_derived_one(self) -> None:
        groups = [
            {
                "author": "Thomas Aquinas",
                "work": "Super Epistolam ad Romanos lectura",
                "titles": [
                    "super epistolam ad galatas lectura",
                    "super epistolam ad romanos lectura",
                ],
            }
        ]
        harvest._name_groups(
            groups,
            {
                "canonical_titles": [
                    {
                        "author": "Thomas Aquinas",
                        "instead_of": "Super Epistolam ad Romanos lectura",
                        "title": "Super Epistolas S. Pauli lectura",
                        "reason": "one work over ten epistles",
                    }
                ]
            },
        )
        self.assertEqual(groups[0]["work"], "Super Epistolas S. Pauli lectura")
        # The table will not load unless the canonical work is one of the
        # group's own titles, and a later run offering it must land here.
        self.assertIn("super epistolas s. pauli lectura", groups[0]["titles"])

    def test_an_entry_matching_no_group_is_refused(self) -> None:
        """Otherwise the override stops applying silently when grouping moves."""
        with self.assertRaises(ValueError) as caught:
            harvest._name_groups(
                [{"author": "Thomas Aquinas", "work": "x", "titles": ["x", "y"]}],
                {
                    "canonical_titles": [
                        {
                            "author": "Thomas Aquinas",
                            "instead_of": "a title no group holds",
                            "title": "Super Epistolas S. Pauli lectura",
                            "reason": "stale",
                        }
                    ]
                },
            )
        self.assertIn("no group holds", str(caught.exception))

    def test_every_tracked_entry_states_its_reason(self) -> None:
        """The idiom the review block keeps: no judgement without a reason."""
        review = (harvest._load(ALIASES).get("review") or {})
        for entry in review.get("canonical_titles") or []:
            with self.subTest(title=entry.get("title")):
                self.assertTrue(str(entry.get("reason") or "").strip())


class KeyExtentTests(unittest.TestCase):
    def test_a_chapter_key_covers_the_whole_chapter(self) -> None:
        self.assertEqual(key_extents("Psalms 24"), [("Psalms", 24, None, None)])

    def test_a_verse_key_covers_one_verse(self) -> None:
        self.assertEqual(key_extents("Psalms 24:4"), [("Psalms", 24, 4, 4)])

    def test_a_range_within_a_chapter_covers_its_verses(self) -> None:
        self.assertEqual(key_extents("Psalms 24:1-24:3"), [("Psalms", 24, 1, 3)])
        self.assertEqual(key_extents("Psalms 24:1-3"), [("Psalms", 24, 1, 3)])

    def test_a_range_across_chapters_is_open_at_the_seam(self) -> None:
        """Splitting at the boundary is not dropping what lies past it."""
        self.assertEqual(
            key_extents("Isaias 63:16-64:7"),
            [("Isaias", 63, 16, None), ("Isaias", 64, None, 7)],
        )

    def test_what_cannot_be_parsed_claims_no_extent(self) -> None:
        """A guessed extent would report an overlap that is not there."""
        self.assertEqual(key_extents("Baruch 3:9-15, 32-4:4"), [])


class OverlappingKeyTests(unittest.TestCase):
    """The detector whose absence let a two-granularity index be promoted."""

    def test_the_tracked_index_answers_each_passage_once(self) -> None:
        import yaml

        document = yaml.safe_load(INDEX.read_text(encoding="utf-8"))
        keys = [entry["passage"] for entry in document.get("passages") or []]
        self.assertEqual(overlapping_keys(keys), [])

    def test_a_chapter_and_a_verse_within_it_overlap(self) -> None:
        self.assertEqual(
            overlapping_keys(["Psalms 24", "Psalms 24:4"]),
            [("Psalms 24", "Psalms 24:4")],
        )

    def test_two_ranges_sharing_a_verse_overlap(self) -> None:
        self.assertEqual(
            overlapping_keys(["Psalms 24:1-24:3", "Psalms 24:3"]),
            [("Psalms 24:1-24:3", "Psalms 24:3")],
        )

    def test_a_range_crossing_a_chapter_meets_that_chapter(self) -> None:
        self.assertEqual(
            overlapping_keys(["Isaias 64", "Isaias 63:16-64:7"]),
            [("Isaias 63:16-64:7", "Isaias 64")],
        )

    def test_neighbours_that_do_not_touch_are_not_reported(self) -> None:
        for keys in (
            ["Psalms 24", "Psalms 25"],
            ["Psalms 24:1-24:3", "Psalms 24:4"],
            ["Psalms 24", "Luke 24"],
        ):
            with self.subTest(keys=keys):
                self.assertEqual(overlapping_keys(keys), [])


class PromotionTests(unittest.TestCase):
    def test_promotion_refuses_an_index_that_answers_twice(self) -> None:
        """A ledger keyed at two granularities must not reach the index at two."""
        works = [
            {
                "author": "Augustine of Hippo",
                "title": "Enarrationes in Psalmos",
                "role": "church-father",
                "death_year": 430,
            }
        ]
        runs = [
            {
                "run_id": "r",
                "passages": {"Psalms 24": works, "Psalms 24:4": works},
            }
        ]
        aliases: dict = {}
        answered = harvest._locus_answers(runs[0], aliases)
        # Both keys fold onto the one chapter, which is the whole point: the
        # run answered about Psalms 24 twice, not about two passages.
        self.assertEqual(sorted(answered), ["Psalms 24"])
        self.assertEqual(overlapping_keys(["Psalms 24", "Psalms 24:4"]),
                         [("Psalms 24", "Psalms 24:4")])

    def test_the_guard_would_have_refused_the_index_as_it_was_promoted(self) -> None:
        """With the fold removed, promotion emits both keys — and stops.

        The historical index held `Psalms 24` and `Psalms 24:4` at once. This
        pins the guard to that exact shape rather than to a shape the current
        derivation can no longer produce.
        """
        import argparse
        import tempfile

        import yaml

        work = {
            "author": "Augustine of Hippo",
            "title": "Enarrationes in Psalmos",
            "role": "church-father",
            "death_year": 430,
        }
        with tempfile.TemporaryDirectory() as scratch:
            ledger = Path(scratch) / "ledger.yaml"
            ledger.write_text(
                yaml.safe_dump(
                    {
                        "schema": "triptych-commentary-harvest/v1",
                        "runs": [
                            {
                                "run_id": "2026-07-30-model-0",
                                "passages": {
                                    "Psalms 24": [work],
                                    "Psalms 24:4": [work],
                                },
                            }
                        ],
                    }
                ),
                encoding="utf-8",
            )
            settings = argparse.Namespace(
                ledger=str(ledger),
                index=str(Path(scratch) / "index.yaml"),
                audited_on="2026-07-31",
                min_confidence=0.0,
                dry_run=True,
            )
            folded = harvest._chapter_loci
            harvest._chapter_loci = lambda passage: [passage]
            try:
                with self.assertRaises(ValueError) as caught:
                    harvest.run_promote(settings)
            finally:
                harvest._chapter_loci = folded
            self.assertIn("cover the same text", str(caught.exception))
            # And with the fold in place the same ledger promotes cleanly.
            self.assertEqual(harvest.run_promote(settings)["passages"], 1)

    def test_a_run_answering_one_chapter_twice_is_counted_once(self) -> None:
        """Confidence is appearances over runs, so it can never exceed one."""
        work = {
            "author": "Augustine of Hippo",
            "title": "Enarrationes in Psalmos",
            "role": "church-father",
            "death_year": 430,
        }
        answered = harvest._locus_answers(
            {"passages": {"Psalms 24:1-24:3": [work], "Psalms 24:4": [work]}}, {}
        )
        self.assertEqual(list(answered), ["Psalms 24"])
        self.assertEqual(len(answered["Psalms 24"]), 1)


if __name__ == "__main__":
    unittest.main()
