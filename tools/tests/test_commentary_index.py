"""The two checks that stand between the harvest and the catena.

Both defects they catch were live in tracked artifacts and both survived a
promotion, because promotion asserted nothing about what it wrote. Neither
check is expensive; their absence was the whole failure.

`Rule 8` — a group's canonical title must not name a book that the group's own
names do not share. Aquinas's Pauline commentary is one work over ten epistles
and was named `Super Epistolam ad Romanos lectura`, so the acquisition list
would have gone looking for one tenth of it.
"""

from __future__ import annotations

import importlib.machinery
import importlib.util
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
ALIASES = ROOT / "src" / "sources" / "commentary" / "work-aliases.yaml"
LEDGER = ROOT / "src" / "sources" / "commentary" / "harvest-ledger.yaml"


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


if __name__ == "__main__":
    unittest.main()
