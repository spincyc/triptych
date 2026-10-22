"""The terminal reader holds the page's rules, not a copy of them.

`tools/lectern` reads the published structure and asks the browser's own
models and renderers for every derivation, through one node process. These
tests pin the properties that make that true and that a reader would be misled
by losing:

- the chain is the generator's order, never re-sorted;
- a choice the rubrics leave open comes back open, with no Mass read;
- an absence is said where the text would have been, in the page's words;
- a date-independent reading carries no calendar result;
- the bridge serves nothing from outside the browser tree or the data root.

The adapter tests need node, which `make check` already requires for the
rubric and catena checks. The drawing tests need Textual, which only the
reader needs; without it they are skipped by name, never passed silently.
"""
from __future__ import annotations

import importlib.metadata
import importlib.util
import json
import shutil
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))

from lectern import bridge, refs, webedition  # noqa: E402
from lectern.repo import STRUCTURE, Refused  # noqa: E402

NODE = shutil.which("node")
TEXTUAL = importlib.util.find_spec("textual") is not None


@unittest.skipUnless(NODE, "node is not installed; the reader's derivations run the browser's models under node")
class CatenaAdapterTests(unittest.TestCase):
    def test_the_chain_is_the_spines_own_order(self) -> None:
        view = bridge.call("catena", "view", "Gen", 1, "", "")
        spine = json.loads((STRUCTURE / "catena" / "01-gen" / "001.json").read_text(encoding="utf-8"))
        self.assertEqual(
            [row["id"] for row in view["chain"]["fragments"]],
            [row["id"] for row in spine["fragments"]],
        )

    def test_leads_are_never_fragments(self) -> None:
        view = bridge.call("catena", "view", "Gen", 1, "", "")
        fragments = {row["id"] for row in view["chain"]["fragments"]}
        self.assertTrue(view["leads"])
        for lead in view["leads"]:
            self.assertNotIn("id", lead)
        self.assertTrue(fragments)

    def test_a_chapter_with_no_record_is_said_to_hold_nothing(self) -> None:
        opening = bridge.call("catena", "opening")
        book = next(one for one in opening["books"] if not one["present"])
        view = bridge.call("catena", "view", book["token"], 1, "", "")
        self.assertFalse(view["held"])
        self.assertEqual(view["chain"]["fragments"], [])
        self.assertEqual(view["unfetched"], "")

    def test_an_address_the_canon_does_not_hold_is_refused_not_moved(self) -> None:
        view = bridge.call("catena", "view", "Gen", 999, "", "")
        self.assertTrue(view["problems"])
        self.assertNotIn("chain", view)

    def test_a_fragment_opens_with_its_bases(self) -> None:
        view = bridge.call("catena", "view", "Gen", 1, "", "")
        first = view["chain"]["fragments"][0]
        body = bridge.call("catena", "body", "Gen", 1, "", first["id"])
        self.assertFalse(body["missing"])
        self.assertTrue(body["said"].strip())
        self.assertTrue(body["date_basis"].strip())


@unittest.skipUnless(NODE, "node is not installed; the reader's derivations run the browser's models under node")
class LiturgyAdapterTests(unittest.TestCase):
    def test_an_optional_memorial_is_left_to_the_reader(self) -> None:
        view = bridge.call("liturgy", "day", "postconciliar", "2026-10-22", {"orations": "en"})
        (row,) = view["rows"]
        self.assertTrue(row["unresolvedChoices"])
        self.assertEqual(row["events"], [])
        self.assertIsNone(row["mass"])
        self.assertEqual(view["title"], "No day is settled here")
        self.assertIn("has not selected one silently", row["notice"])

    def test_the_choice_once_made_is_read(self) -> None:
        options = {"orations": "en", "mass": "ot-29-thursday"}
        (row,) = bridge.call("liturgy", "day", "postconciliar", "2026-10-22", options)["rows"]
        self.assertEqual(row["unresolvedChoices"], [])
        self.assertEqual(row["mass"]["key"], options["mass"])
        self.assertTrue(any(event["kind"] == "proper" for event in row["events"]))

    def test_every_held_territorial_branch_is_read_and_none_is_inferred(self) -> None:
        view = bridge.call("liturgy", "day", "postconciliar", "2026-05-14", {"orations": "en"})
        self.assertTrue(view["multiple"])
        self.assertEqual(view["title"], "Held territorial branches")
        self.assertEqual([row["option"] for row in view["rows"]],
                         ["ascension-thursday", "ascension-transferred-to-sunday"])

    def test_a_borrowing_feria_is_titled_by_the_day_and_says_whose_mass_it_takes(self) -> None:
        view = bridge.call("liturgy", "day", "roman-1962", "2026-10-22", {})
        self.assertEqual(view["title"], "a feria after Pentecost")
        said = " ".join(run["text"] for block in view["rows"][0]["reasoning"] for run in block["runs"])
        self.assertIn("This day takes Twenty-first Sunday after Pentecost.", said)

    def test_compare_is_the_pages_and_refuses_as_the_page_refuses(self) -> None:
        built = bridge.call("liturgy", "compare", "roman-1962", "roman-pre-1955", "2026-10-25", {})
        said = [" ".join(run["text"] for run in block["runs"]) for block in built["blocks"]]
        self.assertEqual(built["title"], "Compare calendar results")
        self.assertIn("Calendar results on this date", said)
        self.assertIn("Compare corresponding Propers", said)
        refused = bridge.call("liturgy", "compare", "roman-1962", "postconciliar", "2026-08-02", {})
        self.assertIn("remain unresolved", refused["refused"])
        self.assertNotIn("blocks", refused)

    def test_the_defaults_are_the_pages(self) -> None:
        opening = bridge.call("liturgy", "opening")
        self.assertEqual((opening["defaultBible"], opening["defaultOrations"]), ("douay-rheims", "la"))

    def test_a_missing_translation_is_said_at_the_text_and_the_latin_kept(self) -> None:
        view = bridge.call("liturgy", "day", "roman-1962", "2026-10-22", {"orations": "en"})
        collect = next(event for event in view["rows"][0]["events"] if event.get("slot") == "Collect")
        said = [" ".join(run["text"] for run in block["runs"]) for block in collect["blocks"]]
        self.assertTrue(any("English translation unavailable" in line for line in said), said)
        self.assertTrue(any("The Latin original is shown." in line for line in said), said)
        self.assertTrue(any("Familiam tuam" in line for line in said), said)

    def test_a_formulary_read_without_a_date_has_no_calendar_result(self) -> None:
        view = bridge.call("liturgy", "propers", "roman-1962", "advent-1", {"orations": "en"})
        self.assertIsNone(view["calendarResult"])
        self.assertTrue(view["events"])

    def test_lectionary_cycles_stay_apart_until_one_is_chosen(self) -> None:
        view = bridge.call("liturgy", "propers", "postconciliar", "transfiguration-lord", {"orations": "en"})
        open_cycles = [event for event in view["events"]
                       if (event.get("selected") or {}).get("kind") == "cycle-alternatives"]
        self.assertTrue(open_cycles)
        self.assertEqual(open_cycles[0]["selected"]["availability"], "choice-required")
        self.assertGreater(len(open_cycles[0]["selected"]["cycles"]), 1)

    def test_a_month_is_every_date_of_it(self) -> None:
        month = bridge.call("liturgy", "month", "roman-1962", "2026-02")
        self.assertEqual([row["date"] for row in month["days"]][-1], "2026-02-28")
        self.assertEqual(len(month["days"]), 28)

    def test_search_is_the_pages_own(self) -> None:
        ordinals = bridge.call("liturgy", "search", "roman-1962", "Ad te levavi")
        catalogue = bridge.call("liturgy", "catalogue", "roman-1962")
        self.assertIn("advent-1", [catalogue["rows"][one]["key"] for one in ordinals])
        self.assertEqual(bridge.call("liturgy", "search", "roman-1962", "zzzz no such words"), [])


@unittest.skipUnless(NODE, "node is not installed; the reader's derivations run the browser's models under node")
class PortedPageLogicTests(unittest.TestCase):
    """What the History and Law adapters carry as `PORT:` lines (page logic held
    in a closure no slice can reach) is pinned here, so a drift fails rather
    than reads as the page."""

    def test_one_number_in_two_bodies_of_law_is_two_canons(self) -> None:
        view = bridge.call("law", "lookup", "87", "")
        self.assertEqual(view["view"], "choices")
        self.assertEqual(sorted(choice["line"] for choice in view["choices"]), ["johanno-pauline", "pio-benedictine"])

    def test_a_number_the_record_lacks_is_searched_as_text_and_says_so(self) -> None:
        view = bridge.call("law", "lookup", "100", "")
        self.assertIn("carries no canon numbered 100", view["fell_through"])
        self.assertEqual([choice["citation"] for choice in view["choices"]], ["c. 1008", "c. 1009"])

    def test_an_exact_canon_is_one_canon(self) -> None:
        view = bridge.call("law", "lookup", "1008", "")
        self.assertEqual((view["view"], view["line"]), ("canon", "johanno-pauline"))

    def test_the_timeline_opens_on_the_pages_window(self) -> None:
        state = bridge.call("history", "timeline", {})["state"]
        self.assertEqual((state["start"], state["end"]), (1550, 2050))
        self.assertFalse(state["leads"])

    def test_the_catalogue_shows_every_record_unfiltered(self) -> None:
        view = bridge.call("history", "catalogue", {})
        self.assertIn("2008", json.dumps(view["tally"]) + json.dumps(view["status"]))

    def test_the_reading_plan_keeps_its_tracks_and_never_ships_a_period_key(self) -> None:
        opening = bridge.call("scripture", "opening")
        self.assertEqual([track["count"] for track in opening["tracks"]], [36, 111, 357])
        said = json.dumps(opening)
        for key in ("desert-wanderings", "royal-kingdom", "divided-kingdom", "messianic-fulfilment", "the-church"):
            self.assertNotIn(key, said)


@unittest.skipUnless(NODE, "node is not installed; the reader's derivations run the browser's models under node")
class BridgeTests(unittest.TestCase):
    def test_an_adapter_name_cannot_reach_another_file(self) -> None:
        with self.assertRaises(Refused):
            bridge.call("../bridge", "view")

    def test_an_unknown_function_is_refused(self) -> None:
        with self.assertRaises(Refused):
            bridge.call("catena", "constructor")

    def test_the_page_document_reads_only_what_is_shown(self) -> None:
        script = (
            "const d = require(process.argv[1]); const p = d.document.createElement('p');"
            "const h = d.document.createElement('span'); h.className = 'visually-hidden';"
            "h.textContent = 'Verse 1. '; p.appendChild(h); p.appendChild(d.document.createTextNode('words'));"
            "process.stdout.write(JSON.stringify(d.read(p)));"
        )
        done = subprocess.run([NODE, "-e", script, str(ROOT / "scripts" / "lectern" / "dom.js")],
                              capture_output=True, text=True, check=True)
        blocks = json.loads(done.stdout)
        self.assertEqual("".join(run["text"] for run in blocks[0]["runs"]), "words")


@unittest.skipUnless(TEXTUAL, "Textual is not installed (python-textual); the reader's drawing is not tested here")
class PlainTierTests(unittest.TestCase):
    def test_every_legend_keeps_its_marks_apart_in_ascii(self) -> None:
        from _tooling import fold_to_ascii
        from lectern.snapshot import DRAWING, LEGENDS

        for legend, marks in LEGENDS.items():
            with self.subTest(legend=legend):
                folded = [fold_to_ascii(mark.translate(DRAWING)) for mark in marks]
                self.assertEqual(len(set(folded)), len(folded), dict(zip(marks, folded)))
                for mark, ascii_mark in zip(marks, folded):
                    if mark != "?":
                        self.assertNotIn("?", ascii_mark, mark)


class ReferenceTests(unittest.TestCase):
    BOOKS = [
        {"token": "Gen", "name": "Genesis", "chapters": 50},
        {"token": "John", "name": "John", "chapters": 21},
        {"token": "1John", "name": "1 John", "chapters": 5},
        {"token": "1Cor", "name": "1 Corinthians", "chapters": 16},
    ]

    def test_a_book_and_chapter(self) -> None:
        book, chapter = refs.parse("1 Cor 13", self.BOOKS)
        self.assertEqual((book["token"], chapter), ("1Cor", 13))

    def test_a_name_that_is_also_a_prefix_is_the_book_itself(self) -> None:
        book, chapter = refs.parse("John 3", self.BOOKS)
        self.assertEqual((book["token"], chapter), ("John", 3))

    def test_a_chapter_out_of_range_is_passed_on_to_be_refused(self) -> None:
        book, chapter = refs.parse("Gen 99", self.BOOKS)
        self.assertEqual(chapter, 99)

    def test_nothing_is_guessed_for_an_unknown_book(self) -> None:
        self.assertIsNone(refs.parse("Hezekiah 1", self.BOOKS))


WITHDRAWN = "liturgy/roman-rite/1962/propers/temporal/54-fourteenth-after-pentecost"


@unittest.skipUnless(NODE, "node is not installed; the reader's derivations run the browser's models under node")
class TextsAdapterTests(unittest.TestCase):
    def test_the_held_treatment_carries_no_route_and_no_reason(self) -> None:
        found = bridge.call("texts", "locate", WITHDRAWN, "claude")
        record = bridge.call("texts", "record", found["work"], found["edition"])
        row = record["treatment"]
        self.assertEqual((row["web"], row["pdf"], row["pdfAbsent"], row["status"]), ("", "", "", "hold"))
        self.assertEqual(record["browser"]["label"], "Not rendered")

    def test_a_work_not_in_the_catalogue_is_refused_with_its_path(self) -> None:
        found = bridge.call("texts", "locate", "no/such-work", "gpt")
        self.assertIn("“no/such-work”", found["problem"])
        self.assertNotIn("work", found)

    def test_the_tally_is_the_models(self) -> None:
        found = bridge.call("texts", "find", {"edition": "claude", "reading": "browser", "find": "origen"})
        self.assertEqual(found["tally"], "1 work · 1 document · 18 pages of 213")


@unittest.skipUnless(NODE, "node is not installed; the reader's derivations run the browser's models under node")
class SourcesAdapterTests(unittest.TestCase):
    DOVER = "edition.matthew-arnold.dover-beach.macmillan-1867-uva-lic"
    FORTESCUE = "edition.adrian-fortescue.ceremonies-of-the-roman-rite-described.burns-oates-washbourne-1917"

    def test_a_missing_passage_is_refused_never_rounded_to_the_first(self) -> None:
        found = bridge.call("sources", "follow", self.DOVER, "passage.no-such-passage")
        self.assertIn("“passage.no-such-passage”", found["problem"])
        self.assertNotIn("at", found)

    def test_a_licensed_passage_carries_its_licence_and_one_passage_counts_one_of_one(self) -> None:
        found = bridge.call("sources", "follow", self.DOVER, "")
        passage = bridge.call("sources", "passage", found["work"], found["edition"], 0)
        self.assertTrue(passage["acknowledgement"])
        self.assertEqual(passage["count"], "Passage 1 of 1")
        self.assertEqual(passage["provenance"]["basis"], "")  # shown as the licence instead

    def test_a_withheld_passage_has_its_reason_and_provenance_and_no_words(self) -> None:
        found = bridge.call("sources", "follow", self.FORTESCUE, "")
        passage = bridge.call("sources", "passage", found["work"], found["edition"], 0)
        self.assertFalse(passage["readable"])
        self.assertTrue(passage["reason"].startswith("The rights record states"))
        self.assertNotIn("paragraphs", passage)
        self.assertTrue(passage["provenance"]["controller"])


def _markdown_at_the_pin() -> bool:
    pinned = next(line.split("==")[1].strip() for line in
                  (ROOT / "requirements-public-alpha.txt").read_text().splitlines() if line.startswith("Markdown=="))
    try:
        return importlib.metadata.version("Markdown") == pinned
    except importlib.metadata.PackageNotFoundError:
        return False


class WebEditionTests(unittest.TestCase):
    @unittest.skipUnless(_markdown_at_the_pin() and shutil.which("pandoc"),
                         "the pinned Markdown (requirements-public-alpha.txt) or pandoc is not installed, "
                         "so a web edition is not set here")
    def test_a_web_edition_is_set_whole(self) -> None:
        done = webedition.set_for_terminal("web/claude/biographies/origen.html", 80)
        text = "".join(run for run, _ in done["runs"])
        self.assertIn("Last revised (UTC):", text)
        self.assertIn("Reuse and rights.", text)

    @unittest.skipIf(_markdown_at_the_pin(), "the pinned Markdown is installed, so there is no refusal to see")
    def test_the_renderer_refuses_any_markdown_but_the_pinned_one(self) -> None:
        with self.assertRaises(Refused):
            webedition.set_for_terminal("web/claude/biographies/origen.html", 80)

    def test_a_path_outside_web_is_refused(self) -> None:
        with self.assertRaises(Refused):
            webedition.source_of("web/claude/../../etc/passwd.html")


@unittest.skipUnless(TEXTUAL, "Textual is not installed (python-textual); the reader's drawing is not tested here")
@unittest.skipUnless(NODE, "node is not installed; the reader's derivations run the browser's models under node")
class DrawingTests(unittest.TestCase):
    def snapshot(self, *arguments: str) -> str:
        done = subprocess.run(
            [sys.executable, str(ROOT / "tools" / "lectern"), "snapshot", "--size", "140x40", *arguments],
            capture_output=True, text=True, cwd=ROOT, timeout=300,
        )
        self.assertEqual(done.returncode, 0, done.stderr)
        return done.stdout

    def test_a_bare_invocation_opens_the_reader_with_its_defaults(self) -> None:
        from importlib.machinery import SourceFileLoader
        from importlib.util import module_from_spec, spec_from_loader
        from unittest.mock import patch

        from lectern.app import TriptychApp

        loader = SourceFileLoader("lectern_tool", str(ROOT / "tools" / "lectern"))
        tool = module_from_spec(spec_from_loader(loader.name, loader))
        loader.exec_module(tool)
        opened = {}

        def run(app) -> None:
            opened.update(start=app.start, theme=app.theme, intent=app.intent)

        with patch.object(sys.stdout, "isatty", return_value=True), patch.object(TriptychApp, "run", run):
            self.assertEqual(tool.main([]), 0)
        self.assertEqual(opened, {"start": "day", "theme": "triptych", "intent": {}})

    def test_the_base_surface_keeps_what_the_shell_asks_of_every_surface(self) -> None:
        from lectern.surface import Pending, Surface

        for name in ("open", "build", "follow", "where", "refocus"):
            with self.subTest(method=name):
                self.assertIn(name, vars(Surface))
        self.assertEqual(Pending.where(Pending.__new__(Pending)), "")

    # What each surface shows only once its data has arrived, so that a surface
    # that opened onto its own refusal does not pass for one that opened.
    LANDMARKS = {
        "day": "a feria after Pentecost",
        "propers": "form-qualified formularies",
        "catena": "▸ Basil of Caesarea",
        "scripture": "The Full Account",
        "texts": "152 works",
        "sources": "1,064",
        "history": "How the Missal Changed",
        "law": "The Code, Canon by Canon",
    }

    def test_every_surface_opens_onto_its_data(self) -> None:
        from lectern.surfaces import ORDER

        for kind in ORDER:
            with self.subTest(surface=kind.label):
                drawn = self.snapshot("--surface", kind.surface_id(), "--date", "2026-10-22", "--ref", "Gen 1")
                self.assertNotIn("could not be opened", drawn)
                self.assertNotIn("Traceback", drawn)
                self.assertIn(self.LANDMARKS[kind.surface_id()], drawn)

    def test_a_drawing_depends_on_its_arguments_and_not_the_clock(self) -> None:
        first = self.snapshot("--surface", "day", "--date", "2026-10-22")
        second = self.snapshot("--surface", "day", "--date", "2026-10-22")
        self.assertEqual(first, second)

    def test_the_day_says_what_the_page_says(self) -> None:
        drawn = self.snapshot("--surface", "day", "--date", "2026-10-22", "--calendar", "roman-1962")
        self.assertIn("a feria after Pentecost", drawn)
        self.assertIn("Bible reconstruction", drawn)

    def test_the_chain_arrives_with_every_author_closed(self) -> None:
        closed = self.snapshot("--surface", "catena", "--ref", "Gen 1")
        self.assertIn("▸ Basil of Caesarea", closed)
        self.assertNotIn("Homiliae in Hexaemeron", closed)
        opened = self.snapshot("--surface", "catena", "--ref", "Gen 1", "--keys", "enter")
        self.assertIn("▾ Basil of Caesarea", opened)
        self.assertIn("Homiliae in Hexaemeron", opened)

    def test_an_open_choice_is_drawn_open(self) -> None:
        drawn = self.snapshot("--surface", "day", "--date", "2026-10-22", "--calendar", "postconciliar")
        self.assertIn("Nothing is selected for you by order", drawn)
        self.assertIn("No day is settled here", drawn)
        # Enter before the reader has moved to an option chooses nothing: the
        # dialog stays, and leaving it leaves the day open.
        pressed = self.snapshot("--surface", "day", "--date", "2026-10-22", "--calendar", "postconciliar",
                                "--keys", "s,enter")
        self.assertIn("Nothing is chosen by order", pressed)
        left = self.snapshot("--surface", "day", "--date", "2026-10-22", "--calendar", "postconciliar",
                             "--keys", "s,enter,escape")
        self.assertIn("No day is settled here", left)


if __name__ == "__main__":
    unittest.main()
