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

`Rule 3` — the third element of a locus is the system it is numbered in, and
the index declared none. `Psalms 24` is Ad te levavi in the Vulgate and a
different psalm in the Hebrew; both resolve, and a lookup on the wrong one
returns real commentary attached to the wrong text with nothing counting it a
failure. The declaration is derived here and asserted against a fresh
derivation, in both directions, so a row cannot go on claiming a system after
the calendars stop saying so.
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
GENESIS_ALIASES = ROOT / "src" / "sources" / "commentary" / "genesis-work-aliases.yaml"
CALENDARS = ROOT / "src" / "sources" / "calendars"

sys.path.insert(0, str(ROOT / "scripts"))

from _commentary import (  # noqa: E402
    CANONICAL,
    NUMBERING_SYSTEMS,
    UNRECORDED,
    declared_numbering,
    impossible_key,
    key_extents,
    moved_citations,
    overlapping_keys,
)


def load_harvest():
    loader = importlib.machinery.SourceFileLoader(
        "harvest_tool", str(ROOT / "tools" / "harvest")
    )
    spec = importlib.util.spec_from_loader(loader.name, loader)
    module = importlib.util.module_from_spec(spec)
    loader.exec_module(module)
    return module


harvest = load_harvest()
# Loaded through the harvest's own helper, so the test exercises the same
# import path promotion uses rather than a second one that could diverge.
work_index = harvest._work_index_tool()


def tracked_index() -> dict:
    import yaml

    return yaml.safe_load(INDEX.read_text(encoding="utf-8"))


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
        """`amos` used to be here and is deliberately gone.

        Harvesting Hosea 14 and Amos 9 put Julian of Eclanum's *Tractatus in
        Osee, Ioel et Amos* in the ledger under both books, so the word now
        carries two and the derivation can no longer prove it names one. That
        is the sound direction — a word it cannot prove is never read as a book
        name — and it is why the list below is not a fixed vocabulary: which
        words are provable is a fact about the corpus, and a combined
        commentary takes one out.
        """
        for word, book in (
            ("romanos", "Romans"),
            ("galatas", "Galatians"),
            ("hebraeos", "Hebrews"),
            ("isaiam", "Isaiah"),
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
        for field in ("canonical_titles", "same_authors"):
            for entry in review.get(field) or []:
                with self.subTest(field=field, entry=entry.get("title") or entry.get("also")):
                    self.assertTrue(str(entry.get("reason") or "").strip())


def _run(run_id: str, author: str, title: str, aliases: list[str]) -> dict:
    return {
        "run_id": run_id,
        "passages": {
            "Matthew 9": [
                {"author": author, "title": title, "role": "doctor",
                 "death_year": 1280, "aliases": aliases}
            ]
        },
    }


class SameAuthorTests(unittest.TestCase):
    """`review.same_authors`: one person under two spellings is one author.

    Grouping is per author, so Albertus Magnus and Albert the Great were two
    authors, and the one commentary took two places in the Matthew 9 row.
    """

    REVIEW = {
        "same_authors": [
            {"author": "Albert the Great", "also": "Albertus Magnus", "reason": "one person"}
        ]
    }
    RUNS = [
        _run("r1", "Albert the Great", "Super Matthaeum", ["Commentary on Matthew"]),
        _run("r2", "Albertus Magnus", "Super Matthaeum", ["Enarrationes in Matthaeum"]),
    ]

    def test_a_declared_spelling_joins_its_person(self) -> None:
        groups, _ = harvest._derive_groups(self.RUNS, self.REVIEW)
        self.assertEqual(len(groups), 1)
        self.assertEqual(groups[0]["author"], "Albert the Great")
        self.assertEqual(
            groups[0]["titles"],
            ["commentary on matthew", "enarrationes in matthaeum", "super matthaeum"],
        )

    def test_without_the_entry_they_stay_two(self) -> None:
        groups, _ = harvest._derive_groups(self.RUNS, {})
        self.assertEqual(sorted(g["author"] for g in groups), ["Albert the Great", "Albertus Magnus"])

    def test_the_digest_covers_the_claims_not_the_review(self) -> None:
        """A review entry must not age the table; only a new claim does."""
        self.assertEqual(
            harvest._derive_groups(self.RUNS, self.REVIEW)[1],
            harvest._derive_groups(self.RUNS, {})[1],
        )

    def test_key_and_answers_read_the_spelling_as_its_person(self) -> None:
        registry = harvest._Registry(authors=harvest._same_authors(self.REVIEW))
        work = {"author": "Albertus Magnus", "title": "Lectura nova", "role": "doctor"}
        self.assertEqual(harvest._key(dict(work), registry), ("albert the great", "lectura nova"))
        answered = harvest._locus_answers(
            {"passages": {"Matthew 9": [work]}}, harvest._Registry(authors=registry.authors)
        )
        (found,) = answered["Matthew 9"].values()
        self.assertEqual(found["work"]["author"], "Albert the Great")

    def test_an_entry_without_a_reason_is_refused(self) -> None:
        with self.assertRaises(ValueError):
            harvest._same_authors(
                {"same_authors": [{"author": "A", "also": "B", "reason": ""}]}
            )

    def test_a_chain_is_refused(self) -> None:
        with self.assertRaises(ValueError) as caught:
            harvest._same_authors(
                {"same_authors": [
                    {"author": "A", "also": "B", "reason": "x"},
                    {"author": "B", "also": "C", "reason": "x"},
                ]}
            )
        self.assertIn("both kept and folded", str(caught.exception))

    def test_an_entry_no_run_reaches_is_refused(self) -> None:
        review = {"same_authors": [{"author": "Albert the Great", "also": "Albertus", "reason": "x"}]}
        with self.assertRaises(ValueError) as caught:
            harvest._derive_groups(self.RUNS, review)
        self.assertIn("no run names", str(caught.exception))


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


class NumberingDeclarationTests(unittest.TestCase):
    """The declaration itself: present, known, and honoured by the loader."""

    def test_the_tracked_index_declares_its_numbering(self) -> None:
        self.assertEqual(declared_numbering(tracked_index(), str(INDEX)), CANONICAL)

    def test_an_index_with_no_declaration_is_refused(self) -> None:
        """Both readings of `Psalms 24` resolve, so silence is the worst answer."""
        with self.assertRaises(ValueError) as caught:
            declared_numbering({"passages": []}, "somewhere")
        self.assertIn("no `numbering` declared", str(caught.exception))

    def test_a_declaration_outside_the_vocabulary_is_refused(self) -> None:
        with self.assertRaises(ValueError):
            declared_numbering({"numbering": "latin"}, "somewhere")

    def test_the_vocabulary_separates_the_greek_from_the_hebrew(self) -> None:
        """A two-way flag cannot say what TVTMS says.

        `guidance/versification.md` §3.3 records Vulgate Psalm 9:22-39 against
        Greek 9:21-38 for the same words: the Vulgate and the Greek disagree
        with each other, not merely with the Hebrew. The catena's Genesis pilot
        already holds Basil and Brenton's Septuagint is tracked, so a
        vocabulary that could not tell them apart would have to call one of
        them the other.
        """
        for system in ("vulgate", "hebrew", "greek", "septuagint", "nova-vulgata"):
            with self.subTest(system=system):
                self.assertIn(system, NUMBERING_SYSTEMS)

    def test_the_loader_refuses_an_undeclared_index(self) -> None:
        import tempfile

        import yaml

        with tempfile.TemporaryDirectory() as scratch:
            path = Path(scratch) / "index.yaml"
            path.write_text(
                yaml.safe_dump({"passages": [{"passage": "Psalms 24", "works": []}]}),
                encoding="utf-8",
            )
            with self.assertRaises(ValueError):
                work_index._load_discovery(path)

    def test_the_loader_refuses_a_row_keyed_in_another_system(self) -> None:
        """The row is kept and the answer is not: refusal is the result."""
        import tempfile

        import yaml

        work = {"author": "Jerome", "title": "In Ioelem", "confidence": 1.0}
        with tempfile.TemporaryDirectory() as scratch:
            path = Path(scratch) / "index.yaml"
            path.write_text(
                yaml.safe_dump(
                    {
                        "numbering": CANONICAL,
                        "passages": [
                            {"passage": "Joel 2", "works": [work]},
                            {
                                "passage": "Joel 3",
                                "numbering": UNRECORDED,
                                "numbering_basis": "the Lectionary's Joel 3",
                                "works": [work],
                            },
                        ],
                    }
                ),
                encoding="utf-8",
            )
            discovery = work_index._load_discovery(path)
        self.assertEqual(discovery.numbering, CANONICAL)
        self.assertEqual(sorted(discovery.works), ["Joel 2"])
        self.assertEqual(discovery.refusals, {"Joel 3": "the Lectionary's Joel 3"})


class KeyBoundsTests(unittest.TestCase):
    """A key must be able to exist in the system its file claims."""

    def setUp(self) -> None:
        self.ceilings = dict(harvest._canonical_chapters())

    def test_every_tracked_key_can_exist_in_the_declared_system(self) -> None:
        document = tracked_index()
        system = declared_numbering(document, str(INDEX))
        for entry in document.get("passages") or []:
            if entry.get("numbering"):
                # `unrecorded` claims nothing about this system, so measuring
                # it against this system's bounds would refuse the honest row.
                continue
            with self.subTest(passage=entry["passage"]):
                self.assertEqual(
                    impossible_key(entry["passage"], system, self.ceilings), ""
                )

    def test_a_chapter_past_the_canon_is_refused(self) -> None:
        """Nova Vulgata Joel runs to four chapters; the Vulgate's stops at three."""
        problem = impossible_key("Joel 4", CANONICAL, self.ceilings)
        self.assertIn("ends at chapter 3", problem)

    def test_a_psalm_verse_outside_its_system_is_refused(self) -> None:
        """Hebrew 118 ends at 29 and only the Vulgate's runs to 176."""
        self.assertNotEqual(impossible_key("Psalms 118:137", "hebrew", self.ceilings), "")
        self.assertEqual(impossible_key("Psalms 118:137", "vulgate", self.ceilings), "")

    def test_a_book_the_canon_does_not_carry_is_refused(self) -> None:
        self.assertIn(
            "not a book of the canon", impossible_key("Enoch 1", CANONICAL, self.ceilings)
        )


class NumberingSurveyTests(unittest.TestCase):
    """The overrides are derived from the calendars, and both ways.

    A hand-typed exception list is the thing this repository has been bitten by
    twice: the copies disagree, and the stale one goes on looking honoured. So
    the tracked rows are asserted equal to a fresh derivation — an override the
    calendars no longer support fails, and a divergence with no override fails.
    """

    @classmethod
    def setUpClass(cls) -> None:
        import yaml

        citations = work_index._load_citations_tool()
        documents = {
            calendar: yaml.safe_load(
                (CALENDARS / calendar / "propers.yaml").read_text(encoding="utf-8")
            )
            for calendar in work_index.DEFAULT_CALENDARS
        }
        cls.documents = documents
        cls.survey = work_index.numbering_survey(citations, documents)
        cls.misrouted = work_index.misrouted_citations(citations, documents)

    def test_the_tracked_overrides_are_exactly_the_derived_ones(self) -> None:
        tracked = {
            entry["passage"]: {
                "numbering": entry["numbering"],
                "numbering_basis": entry["numbering_basis"],
            }
            for entry in tracked_index().get("passages") or []
            if entry.get("numbering")
        }
        self.assertEqual(tracked, self.survey)

    def test_the_count_in_the_header_matches_the_rows(self) -> None:
        document = tracked_index()
        self.assertEqual(
            document["numbering_unrecorded_count"],
            len([e for e in document["passages"] if e.get("numbering")]),
        )

    def test_the_lectionary_chapters_are_the_ones_found(self) -> None:
        """Pinned to the loci, not to a count, so a fix has to say which moved.

        Vulgate Joel 3 is the valley of Josaphat and Nova Vulgata Joel 3 is the
        outpoured spirit; Vulgate Esther 4 is Mardochai going away to do as
        Esther asked and Nova Vulgata Esther 4:17 is his prayer. Both are real
        chapters of both books, which is exactly why nothing caught them.

        `Isaiah 8` left this list on 2026-08-02, and saying which moved is the
        point of pinning the loci. It was here because the one citation reaching
        it, `Isaiah 8:23b-9:3`, is resolved to `Isaiah 9:1b-4` by the
        postconciliar calendar's own register, so nothing asked about Vulgate
        Isaiah 8 at all. Reading the Annunciation out of the Ordo added
        `Isaiah 7:10-14; 8:10`, which reaches that chapter and means it. The key
        is sound now, on the same "every, not any" rule that keeps `Malachi 3`.
        """
        self.assertEqual(sorted(self.survey), ["Esther 4", "Joel 3"])
        for locus in self.survey:
            with self.subTest(locus=locus):
                self.assertEqual(self.survey[locus]["numbering"], UNRECORDED)
                self.assertIn("citation_divergences", self.survey[locus]["numbering_basis"])

    def test_a_key_some_citation_means_is_not_condemned(self) -> None:
        """`Malachi 3` is reached by two citations and only one of them moves.

        `Malachi 3:1` means Vulgate Malachi 3. The key is therefore sound and
        it is `Malachi 3:19-20a`, which means Vulgate Malachi 4, that is
        misrouted — a fact about resolution, not about the key.
        """
        self.assertNotIn("Malachi 3", self.survey)
        self.assertIn(
            {
                "calendar": "postconciliar",
                "cited": "Malachi 3:19-20a",
                "reaches": "Malachi 3",
                "means": "Malachi 4:1-2a",
            },
            self.misrouted,
        )

    def test_only_chapter_moving_divergences_count(self) -> None:
        """Most corrections move a verse inside its chapter and change no key."""
        moved = moved_citations(self.documents["postconciliar"])
        self.assertNotIn("Isaiah 9:1-6", moved)
        self.assertIn("Joel 3:1-5", moved)

    def test_the_roman_missal_declares_no_divergences_and_produces_none(self) -> None:
        self.assertEqual(moved_citations(self.documents["roman-1962"]), {})


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


class GenesisAliasCoverageTests(unittest.TestCase):
    """The alias table must account for every name the index holds, exactly once.

    `guidance/sources.md` requires that a retrieval record the names it searched
    under, "because that is the only way to tell a work that is genuinely
    unreachable from one that was looked for under the wrong name". That promise
    is only kept if the table covers the index: a name the table omits is a work
    nobody searched for, and it would read afterwards as an absence.

    The three counts the table states about itself are checked against a fresh
    derivation rather than trusted. One of them was typed wrongly on the first
    write — 62 groups declared against 66 present — which is this repository's
    named defect in its smallest form, and is why they are derived here.
    """

    def setUp(self) -> None:
        import yaml

        self.table = yaml.safe_load(GENESIS_ALIASES.read_text(encoding="utf-8"))
        self.groups = self.table["groups"]

    def index_names(self) -> set[tuple[str, str]]:
        rows = tracked_index()["passages"]
        names: set[tuple[str, str]] = set()
        for row in rows:
            if not row["passage"].startswith("Genesis "):
                continue
            for work in row["works"]:
                names.add((work["author"], work["title"]))
        return names

    def test_declared_counts_are_derivable(self) -> None:
        declared = self.table["distinct_works"]
        self.assertEqual(declared, len(self.groups))
        covered = sum(len(group["index_names"]) for group in self.groups)
        self.assertEqual(self.table["index_names_total"], covered)

    def test_every_indexed_genesis_work_was_searched_for(self) -> None:
        indexed = self.index_names()
        declared = [
            (name["author"], name["title"])
            for group in self.groups
            for name in group["index_names"]
        ]
        missing = indexed - set(declared)
        self.assertEqual(
            missing,
            set(),
            "the index names these Genesis works and the alias table does not, "
            "so nothing searched for them: " + repr(sorted(missing)),
        )
        self.assertEqual(
            len(declared),
            len(set(declared)),
            "a name reaches two groups, so one work would be surveyed twice "
            "under two identities",
        )
        self.assertEqual(len(indexed), self.table["index_names_total"])

    def test_every_group_carries_names_to_search_under(self) -> None:
        for group in self.groups:
            with self.subTest(group=group["id"]):
                self.assertTrue(group.get("author_aliases"), "no author alias")
                self.assertTrue(group.get("title_aliases"), "no title alias")
                self.assertIn("migne", group, "no Migne determination, not even 'none'")



class TruncationTests(unittest.TestCase):
    """A capped list says it was capped (guidance/catena.md Rule 13).

    `discover` caps each passage at twenty leads by default. A sweep that read
    a capped list as the passage's whole list reported the leads below the cap
    as absent, and at Matthew 9 the cap hid the Glossa ordinaria without a word.
    """

    def setUp(self) -> None:
        self.citations = work_index._load_citations_tool()
        works = [
            work_index._coerce_work_record(
                {"author": f"Author {n}", "title": f"Work {n}", "confidence": 1 - n / 10}
            )
            for n in range(3)
        ]
        self.discovery = work_index.Discovery(CANONICAL, {"Joel 2": works}, {})

    def test_a_capped_lookup_reports_the_whole_count(self) -> None:
        _, shown, _, total = work_index._lookup_works(
            self.discovery, self.citations, "Joel 2", 2
        )
        self.assertEqual((len(shown), total), (2, 3))

    def test_an_uncapped_lookup_shows_every_lead(self) -> None:
        _, shown, _, total = work_index._lookup_works(
            self.discovery, self.citations, "Joel 2", 0
        )
        self.assertEqual((len(shown), total), (3, 3))

    def test_discover_marks_a_capped_passage_and_not_an_uncapped_one(self) -> None:
        import json
        import subprocess

        def run(*extra: str) -> dict:
            result = subprocess.run(
                [str(ROOT / "tools" / "commentary-work-index"), "discover",
                 "--passage", "Matthew 9:1-8", "--json", *extra],
                capture_output=True, text=True, check=True, cwd=ROOT,
            )
            return json.loads(result.stdout)["discoveries"][0]

        capped = run("--max-results", "1")
        self.assertEqual(capped["truncated"]["shown"], 1)
        self.assertGreater(capped["truncated"]["total"], 1)
        self.assertNotIn("truncated", run("--max-results", "0"))


SERMO_50 = "passage.peter-chrysologus.sermones.1894-garnier-migne-pl-52.sermo-50"
BASIL_1 = (
    "passage.nicene-and-post-nicene-fathers.series-2-volume-8.new-york-1895."
    "basil-hexaemeron-1"
)
AD_LITTERAM_4 = "passage.augustine.de-genesi-ad-litteram.migne-pl-34.liber-4"


_DISCOVERED: dict[tuple[str, ...], str] = {}


def discover(*arguments: str) -> str:
    """The tool's own output, run once per argument list."""
    import subprocess

    if arguments not in _DISCOVERED:
        _DISCOVERED[arguments] = subprocess.run(
            [str(ROOT / "tools" / "commentary-work-index"), "discover", *arguments],
            capture_output=True, text=True, check=True, cwd=ROOT,
        ).stdout
    return _DISCOVERED[arguments]


def discovered(passage: str, *extra: str) -> dict:
    import json

    return json.loads(
        discover("--passage", passage, "--max-results", "0", "--json", *extra)
    )["discoveries"][0]


def lead(entry: dict, author: str, title: str) -> dict:
    found = [w for w in entry["works"] if (w["author"], w["title"]) == (author, title)]
    if len(found) != 1:
        raise AssertionError(f"{author} -- {title}: {len(found)} leads, expected one")
    return found[0]


class HeldFragmentTests(unittest.TestCase):
    """A held fragment answers at the verse; the harvest stays on the chapter.

    guidance/catena.md §11. The index stores chapters and must never gain a
    verse key (Rule 5, §3), so a lead reached through its chapter says so. A
    sweep of Matthew 9:1-8 was told only that Chrysologus's *Sermones* matched
    on the chapter, while the library held Sermo 50 on 9:1-7, printed and
    collated; the fragment showed only as a `fragment-edge` join.
    """

    def test_sermo_50_is_reported_on_the_verses_it_expounds(self) -> None:
        chrysologus = lead(discovered("Matthew 9:1-8"), "Peter Chrysologus", "Sermones")
        # The harvest's claim is left as it was: it learned the chapter only.
        self.assertEqual(chrysologus["matched"], "chapter")
        self.assertEqual(chrysologus["matched_loci"], ["Matthew 9"])
        self.assertEqual(
            chrysologus["held_fragments"],
            [{
                "passage_id": SERMO_50,
                "work_id": "work.peter-chrysologus.sermones",
                "extent": "Matthew 9:1-9:7",
                "numbering": "vulgate",
                "matched": "verses",
                # 9:8 is the crowds' glorifying of God, which the sermon never
                # reaches; the fragment covers some of the verses cited.
                "passage": "partial",
            }],
        )

    def test_the_text_and_yaml_carry_the_same_verse_match(self) -> None:
        import re

        import yaml

        text = discover("--passage", "Matthew 9:1-8", "--max-results", "0", "--plain")
        # The lead's own lines: from its heading to the next numbered lead.
        block = re.split(r"\n +\d+\. ", text.split("Peter Chrysologus -- Sermones", 1)[1])[0]
        self.assertIn("matched on the chapter, not the verses cited: Matthew 9\n", block)
        self.assertIn(
            "held fragment overlapping the verses cited: Matthew 9:1-9:7, "
            f"covering some of them; {SERMO_50}\n",
            block,
        )
        document = yaml.safe_load(
            discover("--passage", "Matthew 9:1-8", "--max-results", "0", "--yaml")
        )
        chrysologus = lead(document["discoveries"][0], "Peter Chrysologus", "Sermones")
        self.assertEqual(
            [(row["passage_id"], row["extent"], row["matched"]) for row in chrysologus["held_fragments"]],
            [(SERMO_50, "Matthew 9:1-9:7", "verses")],
        )

    def test_basils_first_homily_is_reported_at_genesis_1_1(self) -> None:
        """Both of the harvest's names for the Hexaemeron join the one library work."""
        entry = discovered("Genesis 1:1")
        for author in ("Basil the Great", "Basil of Caesarea"):
            basil = lead(entry, author, "Homiliae in Hexaemeron")
            self.assertEqual(basil["matched"], "chapter")
            rows = {row["passage_id"]: row for row in basil["held_fragments"]}
            self.assertEqual(rows[BASIL_1]["extent"], "Genesis 1:1")
            self.assertEqual(rows[BASIL_1]["passage"], "inside")
            # Homily II begins at 1:2 and must not ride along on the chapter.
            self.assertTrue(all(row["extent"] == "Genesis 1:1" for row in rows.values()))
        self.assertIn(
            f"held fragment overlapping the verses cited: Genesis 1:1, covering all of them; {BASIL_1}",
            discover("--passage", "Genesis 1:1", "--max-results", "0", "--plain"),
        )

    def test_a_range_the_fragment_stops_short_of_claims_no_verse_match(self) -> None:
        """Sermo 50 ends at 9:7. The verse after it shares its chapter, not its extent."""
        short = discovered("Matthew 9:8-13")
        chrysologus = lead(short, "Peter Chrysologus", "Sermones")
        self.assertEqual(chrysologus["matched"], "chapter")
        self.assertNotIn("held_fragments", chrysologus)
        self.assertNotIn(
            SERMO_50, [row["passage_id"] for row in short.get("fragments_without_lead", [])]
        )
        # One verse back, the boundary is inside the extent and is claimed.
        seam = lead(discovered("Matthew 9:7-8"), "Peter Chrysologus", "Sermones")
        self.assertEqual([row["passage_id"] for row in seam["held_fragments"]], [SERMO_50])

    def test_an_extent_across_a_chapter_is_found_from_either_side_and_shown_whole(self) -> None:
        """Rule 6: De Genesi ad litteram IV runs 1:5-2:3 and is never cut at the seam."""
        for passage, reach in (("Genesis 2:1-3", "inside"), ("Genesis 1:5", "inside"),
                               ("Genesis 1:31-2:1", "inside"), ("Genesis 2:3-4", "partial")):
            entry = discovered(passage)
            rows = [
                row
                for work in entry["works"]
                for row in work.get("held_fragments", [])
            ] + entry.get("fragments_without_lead", [])
            found = {row["passage_id"]: row for row in rows}
            self.assertIn(AD_LITTERAM_4, found, passage)
            self.assertEqual(found[AD_LITTERAM_4]["extent"], "Genesis 1:5-2:3", passage)
            self.assertEqual(found[AD_LITTERAM_4]["passage"], reach, passage)
        self.assertNotIn(
            AD_LITTERAM_4,
            [row["passage_id"] for work in discovered("Genesis 2:4")["works"]
             for row in work.get("held_fragments", [])],
        )

    def test_a_held_fragment_no_lead_joins_is_still_listed(self) -> None:
        """The harvest names no Angelomus on Genesis 1; the library holds him at 1:1."""
        entry = discovered("Genesis 1:1")
        self.assertNotIn(
            "Angelomus of Luxeuil", [work["author"] for work in entry["works"]]
        )
        unplaced = {row["passage_id"]: row for row in entry["fragments_without_lead"]}
        angelomus = unplaced["passage.angelomus-of-luxeuil.commentarius-in-genesim.latin-migne-pl-115.1-1"]
        self.assertEqual(
            (angelomus["extent"], angelomus["matched"], angelomus["lead"]),
            ("Genesis 1:1", "verses", "none"),
        )

    def test_a_fragment_whose_lead_is_cut_says_so(self) -> None:
        import json

        entry = json.loads(discover(
            "--passage", "Matthew 9:1-8", "--max-results", "1", "--json"
        ))["discoveries"][0]
        self.assertNotIn("Peter Chrysologus", [work["author"] for work in entry["works"]])
        self.assertEqual(
            [(row["passage_id"], row["lead"]) for row in entry["fragments_without_lead"]],
            [(SERMO_50, "below-cap")],
        )


class FragmentNumberingTests(unittest.TestCase):
    """Rule 3: a fragment's extent is Vulgate, and a Hebrew citation is converted to meet it."""

    def setUp(self) -> None:
        import json
        import tempfile
        import types

        import _containment

        directory = tempfile.TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        root = Path(directory.name)
        index = (
            root / "src/sources/works/catholic-church/vulgata-clementina/editions/"
            "ebible-latvuc/artifacts/book-index-fcad78c2/book-index.tsv"
        )
        index.parent.mkdir(parents=True)
        index.write_text(
            "ordinal\ttoken\tfile\ttestament\tdouay_title\tmodern_name\t"
            "missal_latin_abbreviation\talternate_names\n"
            "19\tPs\t19-psalms.tsv\told\tThe Book of Psalms\tPsalms\tPs.\tPs.\n",
            encoding="utf-8",
        )
        for chapter, verses in ((49, 23), (50, 21)):
            path = root / f"src/sources/bibles/clementine-vulgate/chapters/Ps/{chapter}.json"
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(json.dumps(
                {"verses": {str(n): "text" for n in range(1, verses + 1)}}
            ), encoding="utf-8")
        edges = root / "src/sources/commentary/fragment-loci.yaml"
        edges.parent.mkdir(parents=True)
        edges.write_text(
            "schema: triptych-commentary-fragment-loci/v1\n"
            "numbering: vulgate\n"
            "fragments:\n"
            "- passage_id: passage.miserere\n"
            "  work_id: work.someone.expositio\n"
            "  numbering: vulgate\n"
            "  extent: {token: Ps, first_chapter: 50, first_verse: 3,"
            " last_chapter: 50, last_verse: 4}\n",
            encoding="utf-8",
        )
        self.fragments = work_index.HeldFragments(
            types.SimpleNamespace(root=root, books=_containment.Canon(root))
        )
        self.citations = work_index._load_citations_tool()

    def found(self, citation: str, numbering: str) -> list[str]:
        record = work_index._parse_passage_value(self.citations, citation)[0]
        return [row["passage_id"] for row in self.fragments.overlapping(record, numbering)]

    def test_the_hebrew_miserere_meets_the_vulgate_extent(self) -> None:
        self.assertEqual(self.found("Psalm 51:3", "hebrew"), ["passage.miserere"])
        self.assertEqual(self.found("Psalm 50:3", "vulgate"), ["passage.miserere"])

    def test_the_same_number_in_the_other_system_is_another_psalm(self) -> None:
        self.assertEqual(self.found("Psalm 50:3", "hebrew"), [])


if __name__ == "__main__":
    unittest.main()
