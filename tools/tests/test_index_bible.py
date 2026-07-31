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
from importlib.machinery import SourceFileLoader
from importlib.util import module_from_spec, spec_from_loader
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DOUAY = ROOT / "src/sources/bibles/douay-rheims/index.yaml"
CLEMENTINE = ROOT / "src/sources/bibles/clementine-vulgate/index.yaml"
ARTIFACTS = (
    ROOT / "src/sources/works/english-college-of-douay/douay-rheims-bible"
    / "editions/challoner-gutenberg-1581/artifacts"
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
LOCUS = {
    "book": "Joel",
    "divergence": "the Nova Vulgata divides Joel into four chapters, the Vulgate three",
    "citations": {"Joel 3:1-5": "Joel 2:28-32"},
}


def divergences(locus: dict, entries: list[dict] | None = None) -> Divergences:
    document = {"citation_divergences": [locus]}
    return Divergences("postconciliar", document, entries or [JOEL], canon)


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
            self.douay["Isaiah 8:23-9:3"].startswith("At the first time the land of Zabulon")
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
            "citations": {"Psalm 24:1-3": "Psalm 25:1-3"},
        }
        self.assertIn("owned by the psalm concordance", self.refuses(locus))

    def test_a_locus_without_a_stated_divergence_is_refused(self) -> None:
        locus = {"book": "Joel", "citations": {"Joel 3:1-5": "Joel 2:28-32"}}
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
            "citations": {"4 Esdras 2:36-37": "4 Esdras 2:36-37"},
        }
        divergences(locus, [esdras]).confirm(self.bible)


if __name__ == "__main__":
    unittest.main()
