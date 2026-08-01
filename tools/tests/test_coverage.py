"""Coverage: what a held work is not held on, and whether that is a defect.

The whole value of this report is one distinction, so most of what is tested
here is that it refuses to collapse: a work that ENDS where the fragments end
is complete, a work that reaches further is a gap, a work whose reach nobody
has established is neither, and the three must not be reported alike. The rest
is the guard that makes the subtraction trustworthy at all — an extent a held
fragment already reaches past is a contradiction, and a report standing on it
would say the corpus is clean whichever of the two is wrong.
"""
from __future__ import annotations

import json
import sys
import tempfile
import textwrap
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))

import _coverage  # noqa: E402

BOOK_INDEX = (
    "ordinal\ttoken\tfile\ttestament\tdouay_title\tmodern_name\t"
    "missal_latin_abbreviation\talternate_names\n"
    "1\tGen\t01-genesis.tsv\told\tThe Book of Genesis\tGenesis\tGen.\tGen.;Gn\n"
    "2\tRom\t52-romans.tsv\tnew\tThe Epistle to the Romans\tRomans\tRom.\tRom.\n"
)

WORK = "work.augustine.de-civitate-dei"
PASSAGE = "passage.augustine.de-civitate-dei.dods-1871.11.7"


class CoverageFixture(unittest.TestCase):
    """One work, one book, and whichever extent the test is about."""

    def setUp(self) -> None:
        self.temporary_directory = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary_directory.name)
        self.write(
            "src/sources/works/catholic-church/vulgata-clementina/editions/"
            "ebible-latvuc/artifacts/book-index-fcad78c2/book-index.tsv",
            BOOK_INDEX,
        )
        for token, sizes in (("Gen", (31, 25, 24)), ("Rom", (32, 29, 31))):
            for chapter, verses in enumerate(sizes, start=1):
                self.write(
                    f"src/sources/bibles/clementine-vulgate/chapters/{token}/{chapter}.json",
                    json.dumps(
                        {
                            "book": token,
                            "chapter": chapter,
                            "verses": {str(n): "text" for n in range(1, verses + 1)},
                        }
                    ),
                )
        self.write(
            "src/sources/works/augustine/de-civitate-dei/work.toml",
            """
            schema = 1
            record_type = "work"
            id = "work.augustine.de-civitate-dei"
            title = "De civitate Dei"
            responsible = "Augustine of Hippo"
            work_type = "patristic-treatise"
            languages = ["lat"]
            """,
        )
        self.write_aliases()
        self.write_index()
        self.write_edges()
        self.write_extents()

    def tearDown(self) -> None:
        self.temporary_directory.cleanup()

    def write(self, relative: str, content: str) -> Path:
        path = self.root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(textwrap.dedent(content).lstrip(), encoding="utf-8")
        return path

    def write_aliases(self) -> None:
        self.write(
            "src/sources/commentary/work-aliases.yaml",
            """
            schema: triptych-commentary-work-aliases/v1
            groups:
            - author: Augustine of Hippo
              work: De civitate Dei
              titles:
              - de civitate dei
              - the city of god
            """,
        )

    def write_index(self, chapters: tuple[int, ...] = (1, 2, 3)) -> None:
        rows = "\n".join(
            textwrap.dedent(
                f"""
                - passage: Genesis {chapter}
                  works:
                  - author: Augustine of Hippo
                    title: De civitate Dei
                    date: 417
                    confidence: 1.0
                """
            ).strip()
            for chapter in chapters
        )
        self.write(
            "src/sources/commentary/passage-commentary-index.yaml",
            "schema: triptych-commentary-work-index/v1\npassages:\n" + rows + "\n",
        )

    def write_edges(self, last_chapter: int = 1, last_verse: int = 5) -> None:
        import yaml

        (self.root / "src/sources/commentary").mkdir(parents=True, exist_ok=True)
        (self.root / "src/sources/commentary/fragment-loci.yaml").write_text(
            yaml.safe_dump(
                {
                    "schema": "triptych-commentary-fragment-loci/v1",
                    "numbering": "vulgate",
                    "fragments": [
                        {
                            "passage_id": PASSAGE,
                            "work_id": WORK,
                            "work_alias": {
                                "author": "Augustine of Hippo",
                                "work": "De civitate Dei",
                            },
                            "numbering": "vulgate",
                            "extent": {
                                "token": "Gen",
                                "first_chapter": 1,
                                "first_verse": 3,
                                "last_chapter": last_chapter,
                                "last_verse": last_verse,
                            },
                            "basis": "The excerpt expounds the making of light.",
                        }
                    ],
                },
                sort_keys=False,
            ),
            encoding="utf-8",
        )

    def write_extents(self, *rows: dict[str, object], numbering: str = "vulgate") -> None:
        import yaml

        (self.root / "src/sources/commentary").mkdir(parents=True, exist_ok=True)
        (self.root / "src/sources/commentary/work-extents.yaml").write_text(
            yaml.safe_dump(
                {
                    "schema": _coverage.SCHEMA,
                    "updated": "2026-08-01",
                    "numbering": numbering,
                    "extents": list(rows),
                },
                sort_keys=False,
            ),
            encoding="utf-8",
        )

    def extent(self, **overrides: object) -> dict[str, object]:
        row: dict[str, object] = {
            "work_id": WORK,
            "token": "Gen",
            "first_chapter": 1,
            "first_verse": 1,
            "last_chapter": 3,
            "last_verse": 24,
            "within": "continuous",
            "basis": "The eleventh to fourteenth books expound the first three chapters.",
        }
        row.update(overrides)
        return row

    def rows(self) -> list[dict[str, object]]:
        return _coverage.coverage(self.root)["rows"]

    def only(self) -> dict[str, object]:
        rows = self.rows()
        self.assertEqual(len(rows), 1, rows)
        return rows[0]


class ExtentRecordTests(CoverageFixture):
    """The record has to be usable before anything is subtracted from it."""

    def test_a_well_formed_extent_validates(self) -> None:
        self.write_extents(self.extent())
        self.assertEqual(_coverage.validate(self.root), [])

    def test_an_extent_a_held_fragment_reaches_past_is_refused(self) -> None:
        """The one contradiction worth failing a build over.

        If the fragment is right the extent is short and every gap it hides is
        invisible; if the extent is right the fragment is misplaced. Either way
        the subtraction reports a clean corpus, which is this repository's named
        worst failure wearing a coverage report's clothes.
        """
        self.write_edges(last_chapter=3, last_verse=24)
        self.write_extents(self.extent(last_chapter=2, last_verse=25))
        errors = _coverage.validate(self.root)
        self.assertTrue(
            any("but a held fragment of it ends at 3:24" in error for error in errors),
            errors,
        )

    def test_an_extent_beginning_after_a_held_fragment_is_refused(self) -> None:
        self.write_extents(self.extent(first_chapter=2, first_verse=1))
        errors = _coverage.validate(self.root)
        self.assertTrue(
            any("but a held fragment of it begins at 1:3" in error for error in errors),
            errors,
        )

    def test_an_unknown_within_is_refused(self) -> None:
        """`within` decides whether a number is a work item, so it is a closed set."""
        self.write_extents(self.extent(within="mostly"))
        errors = _coverage.validate(self.root)
        self.assertTrue(any("within='mostly'" in error for error in errors), errors)

    def test_an_extent_without_a_basis_is_refused(self) -> None:
        self.write_extents(self.extent(basis="   "))
        errors = _coverage.validate(self.root)
        self.assertTrue(any("states no basis" in error for error in errors), errors)

    def test_an_extent_naming_no_work_record_is_refused(self) -> None:
        self.write_extents(self.extent(work_id="work.nobody.nothing"))
        errors = _coverage.validate(self.root)
        self.assertTrue(any("names no work record" in error for error in errors), errors)

    def test_an_extent_past_the_end_of_the_book_is_refused(self) -> None:
        self.write_extents(self.extent(last_chapter=99, last_verse=1))
        errors = _coverage.validate(self.root)
        self.assertTrue(any("past the canonical last chapter" in error for error in errors), errors)

    def test_an_extent_past_the_end_of_a_chapter_is_refused(self) -> None:
        self.write_extents(self.extent(last_chapter=3, last_verse=99))
        errors = _coverage.validate(self.root)
        self.assertTrue(any("past the canonical last verse" in error for error in errors), errors)

    def test_one_work_and_book_cannot_be_recorded_twice(self) -> None:
        self.write_extents(self.extent(), self.extent(last_chapter=2, last_verse=25))
        errors = _coverage.validate(self.root)
        self.assertTrue(any("is recorded twice" in error for error in errors), errors)

    def test_a_non_canonical_numbering_is_refused(self) -> None:
        """Rule 3: an extent is a canonical address or it is anchored to nothing."""
        self.write_extents(self.extent(), numbering="hebrew")
        errors = _coverage.validate(self.root)
        self.assertTrue(any("numbering is 'hebrew'" in error for error in errors), errors)


class CoverageReportTests(CoverageFixture):
    """The four readings, and that they stay four."""

    def test_a_continuous_work_short_of_its_extent_is_a_gap(self) -> None:
        self.write_extents(self.extent())
        row = self.only()
        self.assertEqual(row["status"], "gap")
        self.assertEqual(row["missing"], [2, 3])
        self.assertEqual(row["held"], [1])

    def test_a_selective_work_short_of_its_extent_is_not_established(self) -> None:
        """The work may simply say nothing there, and the report must not guess."""
        self.write_extents(self.extent(within="selective"))
        row = self.only()
        self.assertEqual(row["status"], "not-established")
        self.assertEqual(row["missing"], [2, 3])

    def test_a_work_whose_extent_ends_where_the_holding_ends_is_complete(self) -> None:
        """De Genesi ad litteram's case: the work ends, so nothing is missing."""
        self.write_extents(self.extent(last_chapter=1, last_verse=31))
        row = self.only()
        self.assertEqual(row["status"], "complete")
        self.assertEqual(row["missing"], [])
        # The index still names it further on, and that disagreement is carried
        # rather than resolved: one of the two claims is wrong.
        self.assertEqual(row["named_beyond_extent"], [2, 3])

    def test_a_work_with_no_recorded_extent_is_unexamined(self) -> None:
        """De civitate Dei's case: the difference is real and its reading is not."""
        self.write_extents()
        row = self.only()
        self.assertEqual(row["status"], "unexamined")
        self.assertIsNone(row["extent"])
        self.assertEqual(row["missing"], [2, 3])
        self.assertIn("no extent recorded", row["note"])

    def test_the_index_is_a_second_witness_and_is_reported_separately(self) -> None:
        """`missing` comes from the extent; `named_not_held` from the index."""
        self.write_index(chapters=(1,))
        self.write_extents(self.extent())
        row = self.only()
        self.assertEqual(row["missing"], [2, 3])
        self.assertEqual(row["named_not_held"], [])

    def test_a_book_named_but_never_held_still_gets_a_row(self) -> None:
        """The cheapest win: a work already acquired, named on a second book."""
        self.write(
            "src/sources/commentary/passage-commentary-index.yaml",
            """
            schema: triptych-commentary-work-index/v1
            passages:
            - passage: Genesis 1
              works:
              - author: Augustine of Hippo
                title: De civitate Dei
                date: 417
                confidence: 1.0
            - passage: Romans 3
              works:
              - author: Augustine of Hippo
                title: The City of God
                date: 417
                confidence: 1.0
            """,
        )
        self.write_extents(self.extent())
        rows = {row["token"]: row for row in self.rows()}
        self.assertEqual(sorted(rows), ["Gen", "Rom"])
        self.assertEqual(rows["Rom"]["held"], [])
        self.assertEqual(rows["Rom"]["status"], "unexamined")

    def test_a_work_held_nowhere_is_not_reported(self) -> None:
        """The acquisition list is `discover`'s answer and is not restated here."""
        self.write(
            "src/sources/commentary/work-aliases.yaml",
            """
            schema: triptych-commentary-work-aliases/v1
            groups:
            - author: Augustine of Hippo
              work: De civitate Dei
              titles:
              - de civitate dei
            - author: Basil the Great
              work: Homiliae in Hexaemeron
              titles:
              - homiliae in hexaemeron
            """,
        )
        self.write(
            "src/sources/commentary/passage-commentary-index.yaml",
            """
            schema: triptych-commentary-work-index/v1
            passages:
            - passage: Genesis 1
              works:
              - author: Basil the Great
                title: Homiliae in Hexaemeron
                date: 379
                confidence: 1.0
            """,
        )
        self.write_extents(self.extent())
        self.assertEqual([row["work_id"] for row in self.rows()], [WORK])

    def test_a_row_declaring_its_own_numbering_is_not_counted_as_coverage(self) -> None:
        """Such a row means a different chapter, so naming it here would misattribute."""
        self.write(
            "src/sources/commentary/passage-commentary-index.yaml",
            """
            schema: triptych-commentary-work-index/v1
            passages:
            - passage: Genesis 3
              numbering: septuagint
              works:
              - author: Augustine of Hippo
                title: De civitate Dei
                date: 417
                confidence: 1.0
            """,
        )
        self.write_extents()
        row = self.only()
        self.assertEqual(row["named"], [])

    def test_rows_are_ranked_by_how_much_is_missing(self) -> None:
        self.write_extents(self.extent())
        report = _coverage.coverage(self.root)
        sizes = [len(row["missing"]) for row in report["rows"]]
        self.assertEqual(sizes, sorted(sizes, reverse=True))

    def test_a_gap_is_reported_and_never_raised(self) -> None:
        """An unacquired work is not a defect; the summary states it and returns."""
        self.write_extents(self.extent())
        self.assertEqual(_coverage.validate(self.root), [])
        self.assertIn("2 chapters not held", _coverage.summary_line(self.root))

    def test_the_report_is_byte_stable_for_unchanged_inputs(self) -> None:
        self.write_extents(self.extent())
        first = json.dumps(_coverage.coverage(self.root), sort_keys=True)
        second = json.dumps(_coverage.coverage(self.root), sort_keys=True)
        self.assertEqual(first, second)


if __name__ == "__main__":
    unittest.main()
