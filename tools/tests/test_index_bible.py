"""Tests for the citation-divergence overrides `index-bible` resolves through.

The postconciliar calendar cites the Nova Vulgata; every bible tracked here
follows the Vulgate division. Where the two divide a book differently the
reference still resolves, so the failure has no error to report: `Joel 3:1-5`
returned the valley of Josaphat for as long as nobody read it. These tests hold
the corrected readings, and hold the validation that keeps the corrections from
rotting into the same silence.
"""

from __future__ import annotations

import sys
import unittest
import unittest.mock
from importlib.machinery import SourceFileLoader
from importlib.util import module_from_spec, spec_from_loader
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DOUAY = ROOT / "src/sources/bibles/douay-rheims/index.yaml"
KING_JAMES = ROOT / "src/sources/bibles/king-james-version/index.yaml"
CLEMENTINE = ROOT / "src/sources/bibles/clementine-vulgate/index.yaml"
ARTIFACTS = (
    ROOT / "src/sources/works/english-college-of-douay/douay-rheims-bible"
    / "editions/challoner-gutenberg-1581/artifacts"
)
ENGKJV = (
    ROOT / "src/sources/works/church-of-england/king-james-version"
    / "editions/ebible-engkjv/artifacts"
)


def load_tool(name: str):
    path = ROOT / "tools" / name
    loader = SourceFileLoader(f"_{name.replace('-', '_')}", str(path))
    spec = spec_from_loader(loader.name, loader)
    module = module_from_spec(spec)
    loader.exec_module(module)
    return module


sys.path.insert(0, str(ROOT / "scripts"))
index_bible = load_tool("index-bible")
canon = load_tool("citations")
Divergences = index_bible.Divergences


def entry(book: str, ref: str, ranges: list[dict]) -> dict:
    return {"book": book, "ref": ref, "ranges": ranges}


def span(chapter: int, first: int, last: int | None = None) -> dict:
    return {
        "begin": {"chapter": chapter, "verse": first},
        "end": {"chapter": chapter, "verse": first if last is None else last},
    }


JOEL = entry("Joel", "Joel 3:1-5", [span(3, 1, 5)])
# Every other numbering an indexed edition may be in has to be ruled on, so a
# fixture locus carries the ruling too.
STANCES = {numbering: index_bible.RESOLVED for numbering in index_bible.other_numberings()}
LOCUS = {
    "book": "Joel",
    "divergence": "the Nova Vulgata divides Joel into four chapters, the Vulgate three",
    "numbering": STANCES,
    "citations": {"Joel 3:1-5": "Joel 2:28-32"},
}


def divergences(
    locus: dict, entries: list[dict] | None = None, numbering: str = index_bible.RESOLVED_IN
) -> Divergences:
    document = {"citation_divergences": [locus]}
    return Divergences("postconciliar", document, entries or [JOEL], canon, numbering)


def passages(path: Path) -> dict:
    import yaml

    return yaml.safe_load(path.read_text(encoding="utf-8"))["passages"]


class TrackedIndexTests(unittest.TestCase):
    """The readings a wrong number quietly substituted, as they now resolve."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.douay = passages(DOUAY)
        cls.latin = passages(CLEMENTINE)

    def test_pentecost_vigil_joel_is_the_outpoured_spirit(self) -> None:
        text = self.douay["Joel 3:1-5"]
        self.assertIn("I will pour out my spirit upon all flesh", text)
        self.assertNotIn("valley of Josaphat", text)

    def test_pentecost_vigil_joel_is_the_outpoured_spirit_in_latin(self) -> None:
        self.assertIn(
            "effundam spiritum meum super omnem carnem", self.latin["Joel 3:1-5"]
        )

    def test_joel_two_is_untouched_where_the_two_numberings_agree(self) -> None:
        self.assertIn("rend your hearts", self.douay["Joel 2:12-13"])

    def test_the_last_sunday_malachi_resolves_at_all(self) -> None:
        # Vulgate Malachi 3 ends at verse 18, so this cited nothing before.
        self.assertIn("kindled as a furnace", self.douay["Malachi 3:19-20a"])
        self.assertIn("Sun of justice", self.douay["Malachi 3:19-20a"])

    def test_christmas_isaiah_is_the_child_born_to_us(self) -> None:
        self.assertIn("CHILD IS BORN", self.douay["Isaiah 9:5"])
        self.assertIn("Parvulus enim natus est nobis", self.latin["Isaiah 9:5"])

    def test_isaiah_nine_opens_at_the_people_in_darkness(self) -> None:
        self.assertTrue(self.douay["Isaiah 9:1"].startswith("The people that walked"))
        self.assertIn("The people that walked", self.douay["Isaiah 9:1-6"])
        self.assertIn("CHILD IS BORN", self.douay["Isaiah 9:1-6"])

    def test_isaiah_eight_twenty_three_crosses_into_the_vulgate_chapter(self) -> None:
        self.assertTrue(
            self.douay["Isaiah 8:23b-9:3"].startswith("At the first time the land of Zabulon")
        )

    def test_advent_isaiah_rends_the_heavens_and_ends_in_the_potters_hands(self) -> None:
        text = self.douay["Isaiah 63:16b-17, 19b; 64:2-7"]
        self.assertIn("rend the heavens", text)
        self.assertTrue(text.endswith("we all are the works of thy hands."))

    def test_micah_opens_at_bethlehem(self) -> None:
        text = self.douay["Micah 5:1-4a"]
        self.assertTrue(text.startswith("And thou Bethlehem Ephrata"))
        self.assertNotIn("daughter of the robber", text)


class ResolutionTests(unittest.TestCase):
    def test_a_recorded_citation_resolves_through_its_override(self) -> None:
        found, problem = divergences(LOCUS).apply(JOEL, [span(3, 1, 5)])
        self.assertEqual(problem, "")
        self.assertEqual(found, [{"begin": {"chapter": 2, "verse": 28},
                                  "end": {"chapter": 2, "verse": 32}}])

    def test_an_unrecorded_citation_in_a_divergent_book_refuses(self) -> None:
        other = entry("Joel", "Joel 4:18", [span(4, 18)])
        found, problem = divergences(LOCUS, [JOEL, other]).apply(other, [span(4, 18)])
        self.assertEqual(found, [])
        self.assertIn("records no resolution", problem)

    def test_a_citation_outside_every_divergent_book_passes_through(self) -> None:
        amos = entry("Amos", "Amos 8:4-7", [span(8, 4, 7)])
        ranges = [span(8, 4, 7)]
        found, problem = divergences(LOCUS, [JOEL, amos]).apply(amos, ranges)
        self.assertEqual(problem, "")
        self.assertEqual(found, ranges)

    def test_a_chapter_scoped_locus_leaves_the_rest_of_the_book_alone(self) -> None:
        far = entry("Isaiah", "Isaiah 2:1-5", [span(2, 1, 5)])
        near = entry("Isaiah", "Isaiah 9:5", [span(9, 5)])
        table = divergences(
            {
                "book": "Isaiah",
                "chapters": [9],
                "divergence": "the Vulgate opens chapter 9 one verse earlier",
                "numbering": STANCES,
                "citations": {"Isaiah 9:5": "Isaiah 9:6"},
            },
            [far, near],
        )
        self.assertEqual(table.apply(far, [span(2, 1, 5)])[1], "")
        self.assertEqual(table.apply(near, [span(9, 5)])[0], [{"begin": {"chapter": 9, "verse": 6},
                                                               "end": {"chapter": 9, "verse": 6}}])


class ValidationTests(unittest.TestCase):
    """A stale override must fail the build, not quietly stop overriding."""

    def refuses(self, locus: dict, entries: list[dict] | None = None) -> str:
        with self.assertRaises(ValueError) as caught:
            divergences(locus, entries)
        return str(caught.exception)

    def test_a_resolution_for_a_reference_no_longer_cited_is_refused(self) -> None:
        locus = {**LOCUS, "citations": {"Joel 3:1-5": "Joel 2:28-32",
                                        "Joel 3:6-8": "Joel 3:1-3"}}
        self.assertIn("no longer cited", self.refuses(locus))

    def test_a_resolution_into_another_book_is_refused(self) -> None:
        locus = {**LOCUS, "citations": {"Joel 3:1-5": "Amos 2:28-32"}}
        self.assertIn("outside Joel", self.refuses(locus))

    def test_an_unreadable_resolution_is_refused(self) -> None:
        locus = {**LOCUS, "citations": {"Joel 3:1-5": "not a citation"}}
        self.assertIn("unreadable reference", self.refuses(locus))

    def test_a_declared_chapter_nothing_reaches_is_refused(self) -> None:
        locus = {**LOCUS, "chapters": [3, 4]}
        self.assertIn("chapters [4]", self.refuses(locus))

    def test_a_reference_reaching_no_declared_chapter_is_refused(self) -> None:
        locus = {**LOCUS, "chapters": [4], "citations": {"Joel 3:1-5": "Joel 2:28-32"}}
        self.assertIn("reaches no divergent chapter", self.refuses(locus))

    def test_a_reference_cited_under_another_book_is_refused(self) -> None:
        moved = entry("Amos", "Joel 3:1-5", [span(3, 1, 5)])
        self.assertIn("cited under 'Amos'", self.refuses(LOCUS, [moved]))

    def test_the_psalter_may_not_be_declared_divergent(self) -> None:
        locus = {
            "book": "Psalms",
            "divergence": "the psalters number differently",
            "numbering": STANCES,
            "citations": {"Psalm 24:1-3": "Psalm 25:1-3"},
        }
        self.assertIn("owned by the psalm concordance", self.refuses(locus))

    def test_a_locus_without_a_stated_divergence_is_refused(self) -> None:
        locus = {"book": "Joel", "numbering": STANCES,
                 "citations": {"Joel 3:1-5": "Joel 2:28-32"}}
        self.assertIn("how the numbering diverges", self.refuses(locus))

    def test_a_locus_declaring_no_citations_is_refused(self) -> None:
        self.assertIn("declares no citations", self.refuses({**LOCUS, "citations": {}}))

    def test_a_locus_without_a_book_is_refused(self) -> None:
        self.assertIn("must name a book", self.refuses({**LOCUS, "book": ""}))

    def test_empty_chapters_are_refused_rather_than_read_as_the_whole_book(self) -> None:
        self.assertIn("non-empty list", self.refuses({**LOCUS, "chapters": []}))

    def test_a_chapter_that_is_not_a_number_is_refused(self) -> None:
        self.assertIn("not a chapter number", self.refuses({**LOCUS, "chapters": ["3"]}))

    def test_a_reference_resolved_twice_is_refused(self) -> None:
        document = {"citation_divergences": [LOCUS, LOCUS]}
        with self.assertRaises(ValueError) as caught:
            Divergences("postconciliar", document, [JOEL], canon)
        self.assertIn("resolved twice", str(caught.exception))

    def test_a_declaration_that_is_not_a_list_is_refused(self) -> None:
        with self.assertRaises(ValueError) as caught:
            Divergences("postconciliar", {"citation_divergences": {}}, [JOEL], canon)
        self.assertIn("must be a list", str(caught.exception))

    def test_a_calendar_declaring_nothing_resolves_everything_unchanged(self) -> None:
        table = Divergences("roman-1962", {}, [JOEL], canon)
        ranges = [span(3, 1, 5)]
        self.assertEqual(table.apply(JOEL, ranges), (ranges, ""))


class ConfirmationTests(unittest.TestCase):
    """An override must reach real text in every edition holding its book."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.bible = index_bible.Bible(ARTIFACTS)

    def test_the_tracked_resolutions_all_address_the_douay(self) -> None:
        import yaml

        calendar = ROOT / "src/sources/calendars/postconciliar/propers.yaml"
        document = yaml.safe_load(calendar.read_text(encoding="utf-8"))
        propers = load_tool("mass-propers")
        entries = [
            found
            for _, mass in propers.masses_of(document)
            for found in propers.scripture_entries(mass)
        ]
        table = Divergences("postconciliar", document, entries, canon)
        table.confirm(self.bible)
        self.assertIn("Joel 3:1-5", table.resolved)

    def test_a_resolution_the_edition_cannot_address_fails_the_build(self) -> None:
        # Vulgate Joel ends at chapter 3, so this override corrects nothing.
        locus = {**LOCUS, "citations": {"Joel 3:1-5": "Joel 9:1"}}
        table = divergences(locus)
        with self.assertRaises(ValueError) as caught:
            table.confirm(self.bible)
        self.assertIn("cannot address", str(caught.exception))

    def test_a_book_the_edition_lacks_is_not_held_against_the_override(self) -> None:
        esdras = entry("4 Esdras", "4 Esdras 2:36-37", [span(2, 36, 37)])
        locus = {
            "book": "4 Esdras",
            "divergence": "the editions that print it number it differently",
            "numbering": STANCES,
            "citations": {"4 Esdras 2:36-37": "4 Esdras 2:36-37"},
        }
        divergences(locus, [esdras]).confirm(self.bible)


def psalm(chapter: int, first: int, last: int | None = None) -> dict:
    return {"book": "Psalms", "ref": f"Psalm {chapter}:{first}", "ranges": [span(chapter, first, last)]}


class UnnumberedTitleTests(unittest.TestCase):
    """An edition that leaves a psalm's inscription unnumbered is a verse behind.

    The calendars all number the inscription. Addressing an edition that does
    not with their verse numbers returns real text one or two verses past the
    words cited, which is the failure this shift exists to stop.
    """

    def test_a_range_moves_onto_the_english_numbering(self) -> None:
        moved, problem = index_bible.unnumber_titles([span(51, 3, 4)])
        self.assertEqual(problem, "")
        self.assertEqual(moved[0]["begin"]["verse"], 1)
        self.assertEqual(moved[0]["end"]["verse"], 2)

    def test_a_range_on_the_inscription_refuses(self) -> None:
        moved, problem = index_bible.unnumber_titles([span(51, 1, 2)])
        self.assertEqual(moved, [])
        self.assertIn("inscription", problem)

    def test_a_psalm_without_a_recorded_correspondence_refuses(self) -> None:
        moved, problem = index_bible.unnumber_titles([span(29, 1, 2)])
        self.assertEqual(moved, [])
        self.assertIn("divide", problem)

    def test_a_whole_chapter_carries_no_verse_to_move(self) -> None:
        moved, problem = index_bible.unnumber_titles([{"begin": {"chapter": 51}}])
        self.assertEqual(problem, "")
        self.assertEqual(moved, [{"begin": {"chapter": 51}}])

    def test_the_shift_applies_when_calendar_and_edition_already_agree(self) -> None:
        """The case that reads as needing no work: both sides say `hebrew`."""
        propers = load_tool("mass-propers")
        _, ranges, problem = index_bible.citation(
            psalm(51, 3, 4), "hebrew", "hebrew", propers, index_bible.UNNUMBERED_TITLES
        )
        self.assertEqual(problem, "")
        self.assertEqual(ranges[0]["begin"]["verse"], 1)

    def test_a_title_numbering_edition_is_left_alone(self) -> None:
        propers = load_tool("mass-propers")
        _, ranges, problem = index_bible.citation(
            psalm(51, 3, 4), "hebrew", "hebrew", propers, "numbered"
        )
        self.assertEqual(problem, "")
        self.assertEqual(ranges[0]["begin"]["verse"], 3)

    def test_an_edition_declaring_it_must_be_numbered_from_the_hebrew(self) -> None:
        edition = dict(index_bible.EDITIONS["king-james-version"], numbering="vulgate")
        with unittest.mock.patch.dict(
            index_bible.EDITIONS, {"king-james-version": edition}
        ):
            with self.assertRaises(ValueError) as caught:
                index_bible.document_for("king-james-version", {"passages": {}})
        self.assertIn("hebrew numbering", str(caught.exception))


class WithheldLocusTests(unittest.TestCase):
    """A locus an edition prints text at, but not the text that was cited.

    The King James Version's Daniel 3:29 is Nabuchodonosor's decree; a Vulgate
    citation of Daniel 3:29 means the Prayer of Azarias, which this edition
    prints as a separate book. Returning what it prints would be wrong with
    nothing to report.

    Until 2026-07-31 the alias table answered that by refusing, because the
    correspondence with the separate book had not been established. It has been
    now, verse by verse, in the tracked deuterocanon numbering concordance, so
    these loci redirect rather than refuse. What still refuses is what the
    concordance says cannot be answered: Vulgate Daniel 3:52, which is two
    verses of the Greek book and cannot be selected by one reference without
    cutting it, and Vulgate Daniel 14:42, which the Greek Bel does not carry.
    """

    @classmethod
    def setUpClass(cls) -> None:
        cls.bible = index_bible.Bible(ENGKJV)

    def test_the_prayer_of_azarias_now_redirects_to_the_separate_book(self) -> None:
        text = self.bible.verse("Dan", 3, 29)
        self.assertIsNotNone(text)
        assert text is not None
        self.assertTrue(text.startswith("For we have sinned"), text)
        self.assertNotEqual(text, self.bible.verses[("Dan", 3, 29)])

    def test_a_locus_the_concordance_cannot_answer_still_refuses(self) -> None:
        # 3:52 carries both blessings the Greek numbers 29 and 30; 14:42 has no
        # counterpart in Bel at all.
        self.assertIsNone(self.bible.verse("Dan", 3, 52))
        self.assertIsNone(self.bible.verse("Dan", 14, 42))

    def test_the_edition_still_prints_those_verses(self) -> None:
        self.assertIn(("Dan", 3, 29), self.bible.verses)

    def test_an_unwithheld_neighbour_resolves(self) -> None:
        self.assertIsNotNone(self.bible.verse("Dan", 3, 23))

    def test_the_index_carries_no_passage_for_a_withheld_citation(self) -> None:
        import yaml

        found = yaml.safe_load(KING_JAMES.read_text(encoding="utf-8"))["passages"]
        for ref in ("Daniel 3:52", "Daniel 3:52-56", "Psalm 13:4-5", "Psalm 13:6"):
            with self.subTest(ref=ref):
                self.assertNotIn(ref, found)

    def test_the_index_now_carries_the_redirected_citations(self) -> None:
        import yaml

        found = yaml.safe_load(KING_JAMES.read_text(encoding="utf-8"))["passages"]
        self.assertTrue(found["Daniel 3:29"].startswith("For we have sinned"))
        self.assertTrue(
            found["Ecclesiasticus 36:18"].startswith("Reward them that wait for thee")
        )

    def test_the_miserere_resolves_to_the_verse_this_edition_prints_it_at(self) -> None:
        import yaml

        found = yaml.safe_load(KING_JAMES.read_text(encoding="utf-8"))["passages"]
        self.assertTrue(
            any(
                text.startswith("Have mercy upon me, O God")
                for ref, text in found.items()
                if ref.startswith("Psalm 51:")
            ),
            "no Psalm 51 passage opens at the Miserere",
        )


class NumberingStanceTests(unittest.TestCase):
    """A resolution is written in one numbering and is wrong in another.

    The correction that moves `Joel 3:1-5` onto the Vulgate's `Joel 2:28-32` is
    exactly what a Vulgate-numbered edition needs and exactly what a
    Greek-numbered New Testament must never be given, because a book the
    Lectionary and the Greek divide alike already stands where it belongs. Each
    locus therefore rules on every other numbering an edition may be in, and
    nothing is assumed for one it has not ruled on.
    """

    OTHER = index_bible.other_numberings()

    def test_every_indexed_numbering_but_the_resolutions_own_needs_a_ruling(self) -> None:
        self.assertTrue(self.OTHER, "no edition is in a numbering other than the resolutions'")
        self.assertNotIn(index_bible.RESOLVED_IN, self.OTHER)

    def test_a_locus_ruling_on_nothing_is_refused(self) -> None:
        locus = {key: value for key, value in LOCUS.items() if key != "numbering"}
        with self.assertRaises(ValueError) as caught:
            divergences(locus)
        self.assertIn("must say under numbering", str(caught.exception))

    def test_a_ruling_that_is_not_one_of_the_three_is_refused(self) -> None:
        locus = {**LOCUS, "numbering": {name: "maybe" for name in self.OTHER}}
        with self.assertRaises(ValueError) as caught:
            divergences(locus)
        self.assertIn("must be one of", str(caught.exception))

    def test_a_ruling_on_a_numbering_no_edition_is_in_is_refused(self) -> None:
        locus = {**LOCUS, "numbering": {**LOCUS["numbering"], "coptic": index_bible.RESOLVED}}
        with self.assertRaises(ValueError) as caught:
            divergences(locus)
        self.assertIn("which no indexed edition is in", str(caught.exception))

    def test_the_resolution_applies_in_the_numbering_it_was_written_in(self) -> None:
        found, problem = divergences(LOCUS, numbering=index_bible.RESOLVED_IN).apply(
            JOEL, [span(3, 1, 5)]
        )
        self.assertEqual(problem, "")
        self.assertEqual(found[0]["begin"]["chapter"], 2)

    def test_a_resolved_ruling_carries_the_correction_to_that_numbering_too(self) -> None:
        for name in self.OTHER:
            with self.subTest(numbering=name):
                found, problem = divergences(LOCUS, numbering=name).apply(JOEL, [span(3, 1, 5)])
                self.assertEqual(problem, "")
                self.assertEqual(found[0]["begin"]["chapter"], 2)

    def test_an_as_cited_ruling_leaves_the_citation_exactly_as_it_stands(self) -> None:
        locus = {**LOCUS, "numbering": {name: index_bible.AS_CITED for name in self.OTHER}}
        ranges = [span(3, 1, 5)]
        for name in self.OTHER:
            with self.subTest(numbering=name):
                found, problem = divergences(locus, numbering=name).apply(JOEL, ranges)
                self.assertEqual(problem, "")
                self.assertEqual(found, ranges)

    def test_an_unrecorded_ruling_refuses_rather_than_guessing(self) -> None:
        locus = {**LOCUS, "numbering": {name: index_bible.UNRECORDED for name in self.OTHER}}
        for name in self.OTHER:
            with self.subTest(numbering=name):
                found, problem = divergences(locus, numbering=name).apply(JOEL, [span(3, 1, 5)])
                self.assertEqual(found, [])
                self.assertIn(index_bible.UNRECORDED, problem)

    def test_a_resolution_is_not_confirmed_against_a_numbering_it_never_serves(self) -> None:
        """A correction meant for the Vulgate must not fail another edition's build."""
        locus = {
            **LOCUS,
            "numbering": {name: index_bible.AS_CITED for name in self.OTHER},
            "citations": {"Joel 3:1-5": "Joel 9:1"},
        }
        for name in self.OTHER:
            with self.subTest(numbering=name):
                divergences(locus, numbering=name).confirm(index_bible.Bible(ARTIFACTS))


class ChapterBoundTests(unittest.TestCase):
    """A citation running past a chapter's last verse is reported, not shortened.

    Clamping the range to what the edition prints returns the neighbouring
    verses under the cited numbers and counts as a success, and it also runs
    ahead of the edition's own verse aliases, so an edition that had recorded
    where it carries the merged verse could never be consulted.
    """

    @classmethod
    def setUpClass(cls) -> None:
        cls.bible = index_bible.Bible(ARTIFACTS)

    def test_a_verse_past_the_chapter_end_refuses(self) -> None:
        # The Vulgate joins Mark 4:40-41, so its chapter 4 stops at 40.
        text, problem = self.bible.passage("Mark", [span(4, 35, 41)])
        self.assertEqual(text, "")
        self.assertIn("Mark 4:41 is past Mark 4:40", problem)

    def test_the_refusal_says_where_to_record_the_answer(self) -> None:
        _, problem = self.bible.passage("Mark", [span(4, 35, 41)])
        self.assertIn("verse aliases", problem)

    def test_the_range_inside_the_chapter_still_resolves(self) -> None:
        text, problem = self.bible.passage("Mark", [span(4, 35, 40)])
        self.assertEqual(problem, "")
        self.assertIn("Let us pass over to the other side", text)

    def test_a_merged_verse_the_edition_recorded_resolves_through_the_alias(self) -> None:
        # This edition ends Amos 9 at 14 and records that its 15 stands there.
        self.assertIsNone(self.bible.verses.get(("Amos", 9, 15)))
        text, problem = self.bible.passage("Amos", [span(9, 13, 15)])
        self.assertEqual(problem, "")
        self.assertIn("the ploughman shall overtake the reaper", text)

    def test_a_range_over_a_merged_verse_reads_the_words_once(self) -> None:
        both, _ = self.bible.passage("Amos", [span(9, 13, 15)])
        upto, _ = self.bible.passage("Amos", [span(9, 13, 14)])
        self.assertEqual(both, upto)
        self.assertEqual(both.count("I will plant them upon their own land"), 1)

    def test_a_locus_the_edition_recorded_as_absent_says_so(self) -> None:
        # Vulgate Daniel 3:52 is verses 29 and 30 of this edition's separate
        # book, which one reference cannot select without cutting them.
        king_james = index_bible.Bible(ENGKJV)
        _, problem = king_james.passage("Dan", [span(3, 52)])
        self.assertTrue(problem.endswith(index_bible.NOT_CARRIED), problem)


class CorrectedReadingTests(unittest.TestCase):
    """The readings the second round of divergences settled, as they now stand."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.douay = passages(DOUAY)

    def test_the_fifth_sunday_of_easter_acts_opens_at_the_preaching(self) -> None:
        text = self.douay["Acts 14:21b-27"]
        self.assertTrue(text.startswith("And when they had preached the gospel"))

    def test_stephens_martyrdom_keeps_its_last_verse(self) -> None:
        text = self.douay["Acts 7:55-60"]
        self.assertIn("lay not this sin to their charge", text)

    def test_the_transfiguration_in_mark_opens_after_six_days(self) -> None:
        self.assertTrue(self.douay["Mark 9:2-10"].startswith("And after six days"))

    def test_the_cloud_acclamation_is_the_voice_from_it(self) -> None:
        self.assertIn("This is my most beloved Son", self.douay["Mark 9:6"])

    def test_the_bread_of_life_discourse_keeps_the_flesh_given_for_the_world(self) -> None:
        self.assertIn("for the life of the world", self.douay["John 6:41-51"])

    def test_a_vulgate_numbered_john_antiphon_is_left_where_it_stood(self) -> None:
        self.assertTrue(
            self.douay["John 6:55"].startswith("He that eateth my flesh")
        )

    def test_a_lectionary_numbered_john_acclamation_moves_one_verse_on(self) -> None:
        self.assertIn("words of eternal life", self.douay["John 6:68c"])

    def test_the_thirtieth_sunday_exodus_opens_at_the_stranger(self) -> None:
        self.assertTrue(
            self.douay["Exodus 22:20-26"].startswith("Thou shalt not molest a stranger")
        )

    def test_hosea_is_the_espousal_and_not_the_hearing_of_the_heavens(self) -> None:
        text = self.douay["Hosea 2:16b, 17b, 21-22"]
        self.assertIn("I will espouse thee to me for ever", text)
        self.assertNotIn("I will hear the heavens", text)

    def test_the_twenty_seventh_sunday_antiphon_is_mardochais_prayer(self) -> None:
        text = self.douay["Esther 4:17"]
        self.assertIn("there is none that can resist thy will", text)
        self.assertNotIn("Mardochai went", text)

    def test_wisdom_opens_at_the_grain_of_the_balance(self) -> None:
        self.assertTrue(
            self.douay["Wisdom 11:22-12:2"].startswith("For the whole world before thee")
        )

    def test_wisdom_six_opens_at_the_glory_of_wisdom(self) -> None:
        self.assertTrue(self.douay["Wisdom 6:12-16"].startswith("Wisdom is glorious"))

    def test_the_holy_family_sirach_opens_at_the_fathers_honour(self) -> None:
        self.assertTrue(
            self.douay["Sirach 3:3-7, 14-17a"].startswith("For God hath made the father")
        )

    def test_sirach_thirty_five_opens_at_the_judge_who_knows_no_favourites(self) -> None:
        self.assertIn(
            "there is not with him respect of person",
            self.douay["Sirach 35:15b-17, 20-22a"],
        )

    def test_a_sirach_citation_already_in_the_vulgates_numbering_is_untouched(self) -> None:
        self.assertTrue(
            self.douay["Sirach 27:5-8"].startswith("As when one sifteth with a sieve")
        )


if __name__ == "__main__":
    unittest.main()
