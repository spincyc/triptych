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

import argparse
import importlib.metadata
import importlib.util
import datetime as dt
import io
import json
import os
import shutil
import subprocess
import sys
import threading
import unittest
import warnings
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import AsyncMock, patch

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))

from lectern import bridge, refs, webedition  # noqa: E402
from lectern.repo import Refused  # noqa: E402

STRUCTURE = ROOT / "src" / "web" / "data" / "structure"

NODE = shutil.which("node")
TEXTUAL = importlib.util.find_spec("textual") is not None


def _lectern_tool():
    from importlib.machinery import SourceFileLoader
    from importlib.util import module_from_spec, spec_from_loader

    loader = SourceFileLoader("lectern_tool", str(ROOT / "tools" / "lectern"))
    tool = module_from_spec(spec_from_loader(loader.name, loader))
    loader.exec_module(tool)
    return tool


class SurfaceMetadataTests(unittest.TestCase):
    def test_the_parser_uses_the_shared_module_names(self) -> None:
        from lectern import SURFACES

        parser = argparse.ArgumentParser()
        _lectern_tool()._common(parser)
        action = next(action for action in parser._actions if action.dest == "surface")
        self.assertEqual(tuple(action.choices), tuple(module for _, _, module in SURFACES))

    def test_help_and_invalid_surfaces_need_no_site_packages(self) -> None:
        for arguments, status in ((["--help"], 0), (["open", "--help"], 0),
                                  (["snapshot", "--help"], 0),
                                  (["snapshot", "--surface", "no-such-surface"], 2)):
            with self.subTest(arguments=arguments):
                done = subprocess.run(
                    [sys.executable, "-S", str(ROOT / "tools" / "lectern"), *arguments],
                    capture_output=True, text=True, cwd=ROOT, timeout=30,
                )
                self.assertEqual(done.returncode, status, done.stderr)
                if status:
                    self.assertIn("invalid choice", done.stderr)
                    self.assertNotIn("needs Textual", done.stderr)

    @unittest.skipUnless(TEXTUAL, "Textual is required for runtime surface identities")
    def test_runtime_order_preserves_the_shared_identities(self) -> None:
        from lectern import SURFACES
        from lectern import surfaces

        self.assertIs(surfaces.SURFACES, SURFACES)
        self.assertEqual(
            tuple((kind.key, kind.label, kind.surface_id()) for kind in surfaces.ORDER),
            SURFACES,
        )


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
        catalogue = json.loads((STRUCTURE / "act-history" / "catalogue.json").read_text())
        expected = {row["id"] for row in catalogue["entries"]}
        shown = [row["id"] for section in view["sections"] for row in section["rows"]]
        self.assertCountEqual(shown, expected)
        self.assertEqual(view["status"], f"{len(expected)} of {len(expected)} source records shown.")
        self.assertTrue(view["tally"].startswith(f"{len(expected)} source records across "))

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
        from lectern.app import TriptychApp

        tool = _lectern_tool()
        opened = {}

        def run(app) -> None:
            opened.update(start=app.start, theme=app.theme, intent=app.intent)

        with (patch.dict(os.environ, {"TERM": "xterm-256color", "NO_COLOR": ""}),
              patch("_tooling.stream_carries_unicode", return_value=True),
              patch.object(sys.stdout, "isatty", return_value=True),
              patch.object(TriptychApp, "run", run)):
            self.assertEqual(tool.main([]), 0)
        self.assertEqual(opened, {"start": "day", "theme": "triptych", "intent": {}})

    def test_plain_and_dumb_terminals_keep_the_compline_palette(self) -> None:
        from lectern.app import TriptychApp

        tool = _lectern_tool()
        opened = []
        for term, arguments in (("dumb", []), ("xterm-256color", ["--plain"])):
            with (self.subTest(term=term, arguments=arguments),
                  patch.dict(os.environ, {"TERM": term, "NO_COLOR": ""}),
                  patch("_tooling.stream_carries_unicode", return_value=True),
                  patch.object(sys.stdout, "isatty", return_value=True),
                  patch.object(TriptychApp, "run", lambda app: opened.append(app.theme))):
                self.assertEqual(tool.main(arguments), 0)
                self.assertEqual(opened[-1], "triptych-compline")

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


@unittest.skipUnless(TEXTUAL and NODE, "Textual and node are required for the reader interaction regressions")
class ReaderInteractionTests(unittest.IsolatedAsyncioTestCase):
    async def wait_for(self, pilot, predicate, reason: str) -> None:
        for _ in range(200):
            if predicate():
                return
            await pilot.pause(0.05)
        self.fail("Timed out waiting for " + reason)

    async def idle(self, app, pilot) -> None:
        await self.wait_for(pilot, lambda: not any(not w.is_finished for w in app.workers)
                            and not bridge.BRIDGE_PROCESS.waiting, "reader workers")
        await pilot.pause(0.05)

    def test_month_padding_never_emits_a_chosen_date(self) -> None:
        from textual.geometry import Offset
        from lectern.month import Month

        month = Month()
        month.chosen = dt.date(2026, 10, 22)
        messages = []
        with patch.object(month, "post_message", side_effect=messages.append):
            month.on_click(SimpleNamespace(get_content_offset=lambda _: Offset(1, 2)))
            self.assertEqual(messages, [])
            month.on_click(SimpleNamespace(
                get_content_offset=lambda _: Offset(3 * month._cell() + 1, 2)))
        self.assertEqual([message.date for message in messages], [dt.date(2026, 10, 1)])
        self.assertEqual(month.chosen, dt.date(2026, 10, 22))

    async def test_sources_new_empty_edition_rejects_late_real_passage(self) -> None:
        from textual.widgets import Static
        from lectern.app import TriptychApp
        from lectern.surfaces.sources import Sources

        opening = bridge.call("sources", "opening")
        held = next((at, i) for at, work in enumerate(opening["works"])
                    for i, edition in enumerate(work["editions"]) if edition["readable"])
        empty = next((at, i) for at, work in enumerate(opening["works"])
                     for i, edition in enumerate(work["editions"]) if not edition["passages"])
        ready, release = threading.Event(), threading.Event()
        deliver = Sources.deliver

        def gated(owner, callback, *args, **kwargs):
            if callback.__name__ == "show_passage" and not release.is_set():
                ready.set()  # The real bridge response is complete; only delivery is held.
                if not release.wait(15):
                    raise AssertionError("Passage delivery barrier was not released")
            return deliver(owner, callback, *args, **kwargs)

        with patch.object(Sources, "start", lambda self: None), patch.object(Sources, "deliver", gated):
            app = TriptychApp(start="sources")
            async with app.run_test(size=(140, 42)) as pilot:
                try:
                    owner = app.current()
                    owner.opening = opening
                    owner.open_at(*held, 0)
                    await self.wait_for(pilot, ready.is_set, "real passage delivery barrier")
                    old_token = owner._token
                    owner.open_at(*empty, 0)
                    await self.wait_for(pilot, lambda: owner.open_edition is not None
                                        and owner.open_edition["at"] == list(empty), "empty edition")
                    self.assertGreater(owner._token, old_token)
                    self.assertEqual(owner.open_edition["passages"], [])
                    before = str(owner.query_one("#sources-reading-text", Static).render())
                    release.set()
                    await self.idle(app, pilot)
                    self.assertIsNone(owner.passage)
                    self.assertEqual(str(owner.query_one("#sources-reading-text", Static).render()), before)
                finally:
                    release.set()

    async def test_law_back_restores_the_displayed_acts_identity_and_state(self) -> None:
        from lectern.app import TriptychApp
        from lectern.surfaces.law import Law

        gratian = bridge.call("law", "act", "gratianus-decretum-1150")
        rex = bridge.call("law", "act", "rex-pacificus-1234")
        with patch.object(Law, "start", lambda self: None):
            app = TriptychApp(start="law")
            async with app.run_test(size=(140, 42)) as pilot:
                owner = app.current()
                owner.show_act(gratian, False)
                owner.show_act(rex, False)
                owner.action_back()
                self.assertEqual(owner.shown["act"]["id"], gratian["id"])
                self.assertEqual(owner.act["id"], gratian["id"])
                self.assertEqual(owner.where(), gratian["title"])
                with patch.object(owner, "fetch_state") as fetch_state:
                    owner.action_state()
                    fetch_state.assert_called_once_with(gratian["id"])

    async def test_history_next_and_previous_keep_full_record_overlays(self) -> None:
        from textual.widgets import OptionList
        from textual.widgets.option_list import Option
        from lectern.app import TriptychApp
        from lectern.dialogs import Reading
        from lectern.surfaces.history import History

        catalogue = bridge.call("history", "catalogue", {})
        ids = [row["id"] for section in catalogue["sections"] for row in section["rows"]][:2]
        self.assertEqual(len(ids), 2)
        titles = [bridge.call("history", "record", ident)["title"] for ident in ids]
        deliveries = []
        show = History.show_record

        def shown(owner, view, read):
            deliveries.append((view["title"], read))
            return show(owner, view, read)

        with patch.object(History, "start", lambda self: None), patch.object(History, "show_record", shown):
            app = TriptychApp(start="history")
            async with app.run_test(size=(140, 42)) as pilot:
                owner = app.current()
                owner.view = "catalogue"
                owner.show_views()
                owner.records = ids
                listing = owner.query_one("#history-record-list", OptionList)
                listing.add_options([Option(ident, id=f"rec-{i}") for i, ident in enumerate(ids)])
                listing.highlighted = 0
                await self.idle(app, pilot)
                owner.fetch_record(ids[0], True)
                await self.idle(app, pilot)
                self.assertIsInstance(app.screen, Reading)
                for key, index in (("n", 1), ("p", 0)):
                    before = len(deliveries)
                    await pilot.press(key)
                    await self.idle(app, pilot)
                    self.assertIsInstance(app.screen, Reading)
                    self.assertEqual(listing.highlighted, index)
                    self.assertEqual(deliveries[before:], [(titles[index], True)])

    async def test_texts_empty_results_reject_a_late_real_treatment_record(self) -> None:
        from textual.widgets import Static
        from lectern.app import TriptychApp
        from lectern.surfaces.texts import Texts

        opening = bridge.call("texts", "opening")
        at = next(i for i, work in enumerate(opening["works"]) if work["treatments"])
        ready, release = threading.Event(), threading.Event()
        deliver = Texts.deliver

        def gated(owner, callback, *args, **kwargs):
            if callback.__name__ == "draw_record" and not release.is_set():
                ready.set()
                if not release.wait(15):
                    raise AssertionError("Record delivery barrier was not released")
            return deliver(owner, callback, *args, **kwargs)

        with patch.object(Texts, "start", lambda self: None), patch.object(Texts, "deliver", gated):
            app = TriptychApp(start="texts")
            async with app.run_test(size=(140, 42)) as pilot:
                try:
                    owner = app.current()
                    owner.opening = opening
                    owner.cursor = (at, 0)
                    owner.load_record()
                    await self.wait_for(pilot, ready.is_set, "real treatment delivery barrier")
                    old_token = owner._token
                    owner.state["find"] = "NO-SUCH-LECTERN-REGRESSION-TREATMENT-27d6"
                    owner.refind()
                    await self.wait_for(pilot, lambda: bool(owner.found) and not owner.found["rows"],
                                        "empty treatment results")
                    self.assertIsNone(owner.cursor)
                    self.assertIsNone(owner.record)
                    self.assertGreater(owner._token, old_token)
                    before = str(owner.query_one("#texts-record-text", Static).render())
                    release.set()
                    await self.idle(app, pilot)
                    self.assertIsNone(owner.record)
                    self.assertEqual(str(owner.query_one("#texts-record-text", Static).render()), before)
                finally:
                    release.set()

    def test_scripture_rapid_steps_use_the_requested_sparse_track_position(self) -> None:
        from lectern.surfaces.scripture import Scripture

        opening = bridge.call("scripture", "opening")
        owner = Scripture()
        owner.tier = opening["tracks"][0]["tier"]
        owner.track = bridge.call("scripture", "track", owner.tier)
        orders = [row["order"] for row in owner.track["readings"]]
        self.assertEqual(orders[:3], [1, 3, 7])
        owner.view, owner.order, owner.reading = "reading", orders[0], {"index": 1}
        requests = []
        with patch.object(owner, "request", side_effect=lambda: requests.append(owner.order)):
            owner.action_step(1)
            owner.action_step(1)
            self.assertEqual(requests, orders[1:3])
            owner.order = orders[0]
            requests.clear()
            owner.action_step(1)
            owner.action_step(-1)
            self.assertEqual(requests, [orders[1], orders[0]])

    def test_scripture_steps_preserve_orientation_periods_and_track_changes(self) -> None:
        from lectern.surfaces.scripture import Scripture

        owner = Scripture()
        owner.opening = bridge.call("scripture", "opening")
        owner.tier = owner.opening["tracks"][0]["tier"]
        owner.track = bridge.call("scripture", "track", owner.tier)
        with patch.object(owner, "request") as request:
            owner.action_step(-1)
            request.assert_not_called()
            owner.action_step(1)
            self.assertEqual((owner.view, owner.order), ("reading", owner.track["begin"]["order"]))
            owner.view = "period"
            owner.n = owner.track["periods"][0]["n"]
            owner.action_step(1)
            self.assertEqual((owner.view, owner.n), ("period", owner.track["periods"][1]["n"]))
            owner.view = "reading"
            tier = owner.opening["tracks"][1]["tier"]
            owner.set_track(tier)
            request.assert_called_with(land=True)
            count = request.call_count
            owner.action_step(1)
            self.assertEqual(request.call_count, count)  # Do not send an old track's order to a new track.
            owner.track = bridge.call("scripture", "track", tier)
            owner.order = owner.track["readings"][0]["order"]
            owner.action_step(1)
            self.assertEqual(owner.order, owner.track["readings"][1]["order"])

    async def test_propers_finder_calendar_does_not_relabel_the_displayed_reading(self) -> None:
        from lectern.app import TriptychApp
        from lectern.surfaces.propers import Propers

        opening = bridge.call("liturgy", "opening")
        row = bridge.call("liturgy", "catalogue", "roman-1962")["rows"][0]
        short = next(one["short"] for one in opening["calendars"] if one["id"] == "roman-1962")
        with patch.object(Propers, "start", lambda self: None):
            app = TriptychApp(start="propers")
            async with app.run_test(size=(140, 42)) as pilot:
                owner = app.current()
                owner.opened_with(opening)
                await self.idle(app, pilot)
                owner.read("roman-1962", row["key"], None)
                await self.idle(app, pilot)
                owner.action_calendar()
                await self.idle(app, pilot)
                self.assertEqual(owner.calendar, "roman-pre-1955")
                self.assertEqual(owner.view["calendar"], "roman-1962")
                self.assertTrue(owner.where().startswith(short + " · "))
                owner.action_orations()
                await self.idle(app, pilot)
                self.assertEqual(owner.reading[0], "roman-1962")
                self.assertTrue(owner.where().startswith(short + " · "))

    async def test_initial_blank_and_unknown_catena_references_are_refused_not_defaulted(self) -> None:
        from lectern.app import TriptychApp
        from lectern.surfaces.catena import Catena

        opening = bridge.call("catena", "opening")
        for ref in ("   ", "Hezekiah 1"):
            with self.subTest(ref=ref), patch.object(Catena, "start", lambda self: None):
                app = TriptychApp(start="catena", intent={"ref": ref})
                async with app.run_test(size=(140, 42)) as pilot:
                    owner = app.current()
                    self.assertIsNone(owner.current)
                    with patch.object(app, "notify") as notify, patch.object(owner, "load") as load:
                        owner.opened_with(opening)
                        notify.assert_called_once()
                        self.assertIn("No book of this canon", notify.call_args.args[0])
                        load.assert_not_called()
                        self.assertIsNone(owner.current)
                        # A valid subsequent lookup still opens exactly what was asked.
                        owner.follow(ref="John 3")
                        self.assertEqual((owner.token, owner.chapter), ("John", 3))
                        load.assert_called_once_with()


@unittest.skipUnless(TEXTUAL, "Textual is required for snapshot settling")
class SnapshotSettlingTests(unittest.IsolatedAsyncioTestCase):
    async def test_default_budget_exhaustion_is_an_explicit_failure(self) -> None:
        from lectern.snapshot import _settle

        pilot = SimpleNamespace(pause=AsyncMock())
        app = SimpleNamespace(workers=[SimpleNamespace(is_finished=False)])
        with patch.object(bridge.BRIDGE_PROCESS, "waiting", 0):
            with self.assertRaisesRegex(TimeoutError, "400 polling rounds"):
                await _settle(app, pilot)
        self.assertEqual(pilot.pause.await_count, 400)
        pilot.pause.assert_awaited_with(0.05)

    async def test_bridge_waiting_also_exhausts_and_quiet_requires_three_polls(self) -> None:
        from lectern.snapshot import _settle

        pilot = SimpleNamespace(pause=AsyncMock())
        app = SimpleNamespace(workers=[])
        with patch.object(bridge.BRIDGE_PROCESS, "waiting", 1):
            with self.assertRaisesRegex(TimeoutError, "4 polling rounds"):
                await _settle(app, pilot, rounds=4)
        self.assertEqual(pilot.pause.await_count, 4)
        pilot.pause.reset_mock()
        with patch.object(bridge.BRIDGE_PROCESS, "waiting", 0):
            await _settle(app, pilot, rounds=3)
        self.assertEqual(pilot.pause.await_count, 3)


@unittest.skipUnless(TEXTUAL, "Textual is required for snapshot cleanup")
class SnapshotCLIRegressionTests(unittest.TestCase):
    def test_timeout_closes_the_bridge_exits_the_app_and_keeps_cli_error_contract(self) -> None:
        from lectern import snapshot
        from lectern.app import TriptychApp

        app = TriptychApp(start="day")
        out, err = io.StringIO(), io.StringIO()
        process = bridge.BRIDGE_PROCESS.process
        with (patch.object(TriptychApp, "on_mount", lambda self: None),
              patch.object(snapshot, "TriptychApp", return_value=app),
              patch.object(snapshot, "_settle", AsyncMock(side_effect=TimeoutError("snapshot did not settle"))),
              patch.object(bridge.BRIDGE_PROCESS, "close", wraps=bridge.BRIDGE_PROCESS.close) as close,
              patch.dict(os.environ, {"TPT_TRACEBACK": ""}),
              patch.object(sys, "stdout", out), patch.object(sys, "stderr", err)):
            self.assertEqual(_lectern_tool().main(["snapshot"]), 70)
        self.assertEqual(out.getvalue(), "")
        self.assertEqual(err.getvalue(), "lectern: snapshot did not settle\n")
        close.assert_called_once_with()
        self.assertFalse(app.is_running)
        if process is not None:
            self.assertIsNotNone(process.poll())
            self.assertTrue(process.stdin.closed)
            self.assertTrue(process.stdout.closed)


@unittest.skipUnless(TEXTUAL and NODE, "Textual and node are required for Texts ownership regressions")
class ResidualTextTests(unittest.IsolatedAsyncioTestCase):
    wait_for = ReaderInteractionTests.wait_for
    idle = ReaderInteractionTests.idle
    BAD_LEAF = "biographies/NO-SUCH-LECTERN-REVIEW-27d6"

    async def test_initial_bad_leaf_refusal_rejects_the_key_selected_late_real_record(self) -> None:
        from textual.widgets import OptionList, Static
        from lectern.app import TriptychApp
        from lectern.surfaces.texts import Texts

        lookup_ready, lookup_release = threading.Event(), threading.Event()
        record_ready, record_release = threading.Event(), threading.Event()
        deliver = Texts.deliver

        def gated(owner, callback, *args, **kwargs):
            if callback.__name__ == "located" and args[0].get("problem"):
                lookup_ready.set()
                if not lookup_release.wait(15):
                    raise AssertionError("Lookup delivery barrier was not released")
            if callback.__name__ == "draw_record":
                record_ready.set()
                if not record_release.wait(15):
                    raise AssertionError("Treatment delivery barrier was not released")
            return deliver(owner, callback, *args, **kwargs)

        with patch.object(Texts, "deliver", gated):
            app = TriptychApp(start="texts", intent={"leaf": self.BAD_LEAF, "provider": "gpt"})
            async with app.run_test(size=(140, 42)) as pilot:
                try:
                    owner = app.current()
                    await self.wait_for(pilot, lookup_ready.is_set, "initial real lookup refusal")
                    listing = owner.query_one("#texts-list", OptionList)
                    await self.wait_for(
                        pilot, lambda: listing.has_focus and listing.size.width > 0 and
                        owner._drawn_width == max(12, listing.size.width - 1),
                        "laid-out and focused initial catalogue")
                    await pilot.pause(0.05)
                    await pilot.press("down", "down")
                    await self.wait_for(pilot, record_ready.is_set,
                                        f"key-selected real treatment (cursor {owner.cursor!r}, "
                                        f"highlight {listing.highlighted!r})")
                    self.assertIsNotNone(owner.cursor[1])
                    old_token = owner._token
                    lookup_release.set()
                    await self.wait_for(pilot, lambda: owner.cursor is None and
                                        "This address cannot be followed" in str(
                                            owner.query_one("#texts-record-text", Static).render()),
                                        "initial refusal displayed")
                    self.assertGreater(owner._token, old_token)
                    self.assertIsNone(owner.record)
                    before = str(owner.query_one("#texts-record-text", Static).render())
                    record_release.set()
                    await self.idle(app, pilot)
                    self.assertIsNone(owner.cursor)
                    self.assertIsNone(owner.record)
                    self.assertEqual(str(owner.query_one("#texts-record-text", Static).render()), before)
                finally:
                    lookup_release.set()
                    record_release.set()

    async def test_lookup_refusal_clears_an_already_loaded_real_record(self) -> None:
        from textual.widgets import Static
        from lectern.app import TriptychApp

        app = TriptychApp(start="texts")
        async with app.run_test(size=(140, 42)) as pilot:
            owner = app.current()
            await self.wait_for(pilot, lambda: bool(owner.found), "real catalogue")
            await self.idle(app, pilot)
            await pilot.press("down", "down")
            await self.wait_for(pilot, lambda: owner.record is not None, "real treatment record")
            self.assertTrue(owner.record["heading"])
            old_token = owner._token
            owner.follow(leaf=self.BAD_LEAF, provider="gpt")
            await self.wait_for(pilot, lambda: owner.cursor is None, "lookup owner cleared")
            self.assertGreater(owner._token, old_token)
            self.assertIsNone(owner.record)
            self.assertIn("This address cannot be followed",
                          str(owner.query_one("#texts-record-text", Static).render()))


def _pipe_child(program: str):
    return subprocess.Popen([sys.executable, "-u", "-c", program], cwd=ROOT,
                            stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                            stderr=subprocess.DEVNULL, text=True, encoding="utf-8", bufsize=1)


@unittest.skipUnless(TEXTUAL and NODE, "Textual and node are required for live snapshot shutdown")
class SnapshotBusyBridgeTests(unittest.TestCase):
    def test_live_busy_child_preserves_timeout_cli_cleanup_and_restart(self) -> None:
        from lectern import snapshot
        from lectern.app import TriptychApp

        settle = snapshot._settle
        for mode in ("capture", "cli"):
            with self.subTest(mode=mode):
                owned = bridge.Bridge()
                children, apps, errors = [], [], []

                def start():
                    # A real owned pipe child consumes a request, then waits for
                    # more input without replying. No long sleep or mocked error.
                    child = _pipe_child("import sys; sys.stdin.readline(); sys.stdin.read()")
                    children.append(child)
                    return child

                call = owned.call

                def observed(*args):
                    try:
                        return call(*args)
                    except Exception as error:
                        errors.append(error)
                        raise

                def factory(**options):
                    app = TriptychApp(**options)
                    apps.append(app)
                    return app

                async def short_budget(app, pilot):
                    await ReaderInteractionTests.wait_for(
                        self, pilot, lambda: owned.waiting > 0, "live bridge reader")
                    await settle(app, pilot, rounds=4)

                out, err = io.StringIO(), io.StringIO()
                try:
                    with (warnings.catch_warnings(record=True) as caught,
                          patch.object(bridge, "BRIDGE_PROCESS", owned),
                          patch.object(owned, "_start", start),
                          patch.object(owned, "call", observed),
                          patch.object(snapshot, "TriptychApp", factory),
                          patch.object(snapshot, "_settle", short_budget),
                          patch.object(snapshot, "_text", side_effect=AssertionError("Unsettled capture")),
                          patch.dict(os.environ, {"TPT_TRACEBACK": ""}),
                          patch.object(sys, "stdout", out), patch.object(sys, "stderr", err)):
                        warnings.simplefilter("always", ResourceWarning)
                        if mode == "capture":
                            with self.assertRaisesRegex(TimeoutError, "4 polling rounds") as timeout:
                                snapshot.render(surface="day", intent={}, size=(120, 40), keys=[],
                                                form="text", theme="triptych")
                            self.assertIs(type(timeout.exception), TimeoutError)
                        else:
                            self.assertEqual(_lectern_tool().main(["snapshot"]), 70)
                            self.assertEqual(
                                err.getvalue(),
                                "lectern: snapshot did not settle within 4 polling rounds "
                                "(50 ms pauses); no snapshot was captured\n")
                        self.assertEqual(out.getvalue(), "")
                        self.assertEqual(len(children), 1)
                        self.assertTrue(errors)
                        self.assertTrue(all(isinstance(error, Refused) for error in errors), errors)
                        self.assertIsNone(owned.process)
                        self.assertEqual(owned.waiting, 0)
                        self.assertTrue(all(not app.is_running for app in apps))
                        for child in children:  # Before the test's safety cleanup.
                            self.assertIsNotNone(child.poll())
                            self.assertTrue(child.stdin.closed)
                            self.assertTrue(child.stdout.closed)
                    self.assertFalse([w for w in caught if issubclass(w.category, ResourceWarning)])
                    # Remove the controlled child factory and use the real model:
                    # shutdown must not poison a subsequent request or its ID.
                    self.assertTrue(owned.call("catena", "opening")["books"])
                    restarted = owned.process
                    owned.close()
                    self.assertIsNotNone(restarted.poll())
                    self.assertTrue(restarted.stdin.closed and restarted.stdout.closed)
                finally:
                    owned.close()
                    for child in children:
                        if child.poll() is None:
                            child.kill()
                        child.wait(timeout=5)
                        child.stdin.close()
                        child.stdout.close()


@unittest.skipUnless(NODE, "node is required to verify bridge restart against the real model")
class BridgeLifetimeTests(unittest.TestCase):
    def test_protocol_refusals_preserve_ids_disposal_and_normal_restart(self) -> None:
        for mode, message in (("json", "not JSON"), ("id", "out of turn"),
                              ("refusal", "controlled refusal")):
            with self.subTest(mode=mode):
                client = bridge.Bridge()
                program = (
                    "import json,sys\n"
                    "for line in sys.stdin:\n"
                    " r=json.loads(line)\n"
                    " answer={'id':r['id']" + ("+1" if mode == "id" else "") +
                    ",'ok':False,'error':'controlled refusal'}\n"
                    " print('not-json' if " + repr(mode) +
                    "=='json' else json.dumps(answer),flush=True)\n"
                )
                child = _pipe_child(program)
                try:
                    with patch.object(client, "_start", return_value=child):
                        with self.assertRaisesRegex(Refused, message):
                            client.call("catena", "opening")
                        if mode == "refusal":
                            self.assertIs(client.process, child)  # Ordinary model refusal keeps the session.
                            with self.assertRaisesRegex(Refused, message):
                                client.call("catena", "opening")  # A second, matching protocol ID.
                            client.close()
                        else:
                            self.assertIsNone(client.process)
                    self.assertIsNotNone(child.poll())
                    self.assertTrue(child.stdin.closed and child.stdout.closed)
                    self.assertTrue(client.call("catena", "opening")["books"])
                finally:
                    client.close()
                    if child.poll() is None:
                        child.kill()
                    child.wait(timeout=5)
                    child.stdin.close()
                    child.stdout.close()

    def test_response_timeout_remains_refused_and_the_next_call_restarts(self) -> None:
        client = bridge.Bridge()
        child = _pipe_child("import sys; sys.stdin.readline(); sys.stdin.read()")
        try:
            with patch.object(client, "_start", return_value=child), patch.object(bridge, "PATIENCE", 0.05):
                with self.assertRaisesRegex(Refused, "did not answer catena opening within"):
                    client.call("catena", "opening")
            self.assertIsNone(client.process)
            self.assertEqual(client.waiting, 0)
            self.assertIsNotNone(child.poll())
            self.assertTrue(child.stdin.closed and child.stdout.closed)
            self.assertTrue(client.call("catena", "opening")["books"])
        finally:
            client.close()
            if child.poll() is None:
                child.kill()
            child.wait(timeout=5)
            child.stdin.close()
            child.stdout.close()


@unittest.skipUnless(TEXTUAL and NODE, "Textual and node are required for shared Propers notice regressions")
class PropersCoverageNoticeTests(unittest.IsolatedAsyncioTestCase):
    async def test_real_page_notices_keep_language_ordinary_and_recension(self) -> None:
        from copy import deepcopy
        from lectern.app import TriptychApp
        from lectern.surfaces import propers
        from lectern.widgets import Ink
        from textual.widgets import Static

        captured = []

        class RecordedInk(Ink):
            def content(self):
                captured.append(self.parts[:])
                return super().content()

        notices = {}
        cases = (
            ("roman-1962", "advent-1", "en", False),
            ("roman-1962", "advent-1", "la", False),
            ("roman-1962", "advent-1", "en", True),
            ("roman-1962", "advent-1", "la", True),
            ("roman-pre-1955", "octava-nativitatis-domini", "la", False),
        )
        with patch.object(propers.Propers, "start", lambda self: None):
            app = TriptychApp(start="propers")
            async with app.run_test(size=(140, 42)):
                owner = app.current()
                for calendar, key, language, ordinary in cases:
                    with self.subTest(calendar=calendar, language=language, ordinary=ordinary):
                        view = bridge.call("liturgy", "propers", calendar, key,
                                           {"orations": language, "ordinary": ordinary})
                        before = deepcopy(view)
                        notice = view["notice"]
                        self.assertTrue(notice)
                        self.assertNotIn("coverage", view["mass"])
                        with (patch.object(propers, "Ink", RecordedInk),
                              patch.object(propers.missal, "choices", wraps=propers.missal.choices) as choices,
                              patch.object(propers.missal, "events", wraps=propers.missal.events) as events):
                            owner.show(view)
                        rendered = str(owner.query_one("#propers-text", Static).render())
                        self.assertEqual(captured[-1].count((notice, "italic $warning")), 1)
                        self.assertEqual(rendered.count(notice), 1)
                        recension = view["mass"].get("recension")
                        if recension:
                            self.assertTrue(notice.startswith(recension))
                            self.assertEqual(rendered.count(recension), 1)
                        advisory = (view.get("ordinary") or {}).get("advisory")
                        if ordinary and advisory:
                            self.assertIn(advisory, rendered)
                        for absence in view.get("explicitAbsences") or []:
                            reason = absence.get("reason") or ""
                            if " " in reason:
                                self.assertIn(reason, rendered)
                        choices.assert_called_once()
                        self.assertIs(choices.call_args.args[1], view)
                        events.assert_called_once()
                        self.assertIs(events.call_args.args[1], view)
                        self.assertEqual(events.call_args.kwargs,
                                         {"rubrics": owner.rubrics, "accent": "$propers-color"})
                        self.assertEqual(view, before)
                        notices[(calendar, language, ordinary)] = notice
                self.assertNotEqual(notices[("roman-1962", "en", False)],
                                    notices[("roman-1962", "la", False)])
                for language, label in (("en", "English"), ("la", "Latin")):
                    self.assertIn(f"{label} Propers:", notices[("roman-1962", language, False)])
                    self.assertNotIn(f"{label} Ordinary:", notices[("roman-1962", language, False)])
                    self.assertIn(f"{label} Ordinary:", notices[("roman-1962", language, True)])
                self.assertIn("Some Proper text is unavailable",
                              notices[("roman-pre-1955", "la", False)])

    async def test_empty_or_absent_notice_does_not_invent_or_repeat_mass_metadata(self) -> None:
        from copy import deepcopy
        from lectern.app import TriptychApp
        from lectern.surfaces.propers import Propers
        from textual.widgets import Static

        real = bridge.call("liturgy", "propers", "roman-1962", "advent-1", {"orations": "la"})
        with patch.object(Propers, "start", lambda self: None):
            app = TriptychApp(start="propers")
            async with app.run_test(size=(140, 42)):
                owner = app.current()
                for notice in ("", None, "absent"):
                    with self.subTest(notice=notice):
                        view = deepcopy(real)
                        if notice == "absent":
                            view.pop("notice")
                        else:
                            view["notice"] = notice
                        # Deliberately inconsistent, in-memory control only:
                        # neither obsolete nested field is a notice authority.
                        view["mass"]["recension"] = "CONTROL: obsolete nested recension"
                        view["mass"]["coverage"] = "CONTROL: obsolete nested coverage"
                        owner.show(view)
                        rendered = str(owner.query_one("#propers-text", Static).render())
                        self.assertNotIn("CONTROL:", rendered)
                        self.assertNotIn(real["notice"], rendered)


@unittest.skipUnless(TEXTUAL, "Textual is required for Law stop rendering")
class LawStopTextTests(unittest.TestCase):
    def test_stop_text_has_no_configurable_indent(self) -> None:
        import inspect
        from lectern.surfaces.law import stop_text

        self.assertEqual(tuple(inspect.signature(stop_text).parameters), ("ink", "stop"))

    def test_stop_branches_keep_fixed_indentation_markers_and_words(self) -> None:
        from lectern.surfaces.law import stop_text
        from lectern.timeline import Doc

        common = {"title": "Act", "what": "change", "meta": "date · source",
                  "basis": [{"kind": "Basis", "text": "checked   source\nrecord"}],
                  "marker": "Qualification"}
        cases = (
            ({"state": "interpreted", "note": "Meaning only",
              "interpretation": {"force": "Binding", "papal": "Confirmed", "withheld": "Held   back",
                                 "question": {"label": "Question", "text": "Asked"},
                                 "answer": {"label": "Answer", "text": "Replied"},
                                 "notes": ["Local   note"]}},
             ["  ◆ Act — change", "    date · source", "    Meaning only",
              "    Force  Binding", "    How the Pope disposed of it  Confirmed", "    ⊘ Held back",
              "    Question", "    Asked", "    Answer", "    Replied", "    Local note",
              "    Qualification", "    Basis checked source record"]),
            ({"state": "changed", "before": {"body": {"state": "present", "text": "Earlier"}},
              "after": {"nothing": "No later words"}, "fields": "Text changed"},
             ["  ● Act — change", "    date · source", "    Before", "      ┃ Earlier",
              "    After", "      No later words", "    Text changed",
              "    Qualification", "    Basis checked source record"]),
            ({"state": "standing", "standing": {
                "editions": [{"label": "Edition", "language": "Latin", "body": {
                    "state": "withheld", "lead": "Withheld: ", "reason": "Rights   reason",
                    "established": {"sentence": "Established by this act"}}}],
                "body": {"state": "unread", "text": "Not read"}}},
             ["  ● Act — change", "    date · source", "    Edition  Latin",
              "      ⊘ Withheld: Rights reason", "        ↳ Established by this act", "    ◌ Not read",
              "    Qualification", "    Basis checked source record"]),
            ({"state": "recorded"},
             ["  ● Act — change", "    date · source",
              "    Qualification", "    Basis checked source record"]),
        )
        for fields, expected in cases:
            with self.subTest(state=fields["state"]):
                doc = Doc()
                stop_text(doc, {**common, **fields})
                self.assertEqual(["".join(words for words, _ in p) for p in doc.paragraphs], expected)
                mark = "◆ " if fields["state"] == "interpreted" else "● "
                self.assertEqual(doc.paragraphs[0],
                                 [("  ", ""), (mark, "bold $law-color"), ("Act", "bold"),
                                  (" — change", "italic $law-color")])
                self.assertEqual(doc.paragraphs[-2],
                                 [("    ", ""), ("Qualification", "$warning")])
                self.assertEqual(doc.paragraphs[-1],
                                 [("    ", ""), ("Basis ", "bold $law-color"),
                                  ("checked source record", "$text-muted")])

@unittest.skipUnless(TEXTUAL, "Textual is required for reader helper contracts")
class ReaderOptionTrimTests(unittest.TestCase):
    def test_only_selected_rendering_options_remain(self) -> None:
        import inspect
        from lectern import missal
        from lectern.widgets import count

        self.assertEqual(tuple(inspect.signature(missal.events).parameters),
                         ("ink", "view", "rubrics", "accent"))
        self.assertEqual(tuple(inspect.signature(missal.choices).parameters), ("ink", "view"))
        self.assertEqual(tuple(inspect.signature(count).parameters), ("number", "word"))
        self.assertEqual(tuple(inspect.signature(webedition.set_for_terminal).parameters), ("web", "columns"))
        self.assertEqual(tuple(inspect.signature(webedition._runs).parameters), ("ansi",))

    def test_source_counts_keep_singular_regular_plural_and_commas(self) -> None:
        from lectern.widgets import count

        for word in ("edition", "artifact"):
            for number in (0, 1, 2, 1064, 1000000):
                with self.subTest(word=word, number=number):
                    self.assertEqual(count(number, word), f"{number:,} {word}" + ("" if number == 1 else "s"))

    def test_web_runs_keep_texts_theme_token_sgr_and_safe_links(self) -> None:
        styled = "\x1b[1;3;4;9;38;2;1;2;3mstyled\x1b[0m plain"
        self.assertEqual(webedition._runs(styled),
                         [("styled", "bold italic underline strike $texts-color"), (" plain", "")])
        for colour in ("31", "48;5;123", "38;5;12", "48;2;1;2;3"):
            self.assertEqual(webedition._runs(f"\x1b[{colour}mcolour\x1b[0m"),
                             [("colour", "$texts-color")])
        good = "https://example.invalid/reader"
        self.assertEqual(webedition._runs(f"\x1b]8;;{good}\x1b\\link\x1b]8;;\x1b\\"),
                         [("link", f'underline $texts-color link="{good}"')])
        for unsafe in ('https://example.invalid/"quoted', "https://example.invalid/with space",
                       "not-a-scheme"):
            with self.subTest(unsafe=unsafe):
                runs = webedition._runs(f"\x1b]8;;{unsafe}\x07label\x1b]8;;\x07")
                self.assertEqual(runs, [("label", "underline $texts-color")])

    @unittest.skipUnless(_markdown_at_the_pin() and shutil.which("pandoc"),
                         "the real locked Markdown and pandoc pipeline is required")
    def test_web_cache_keeps_source_mtime_columns_and_locked_pipeline(self) -> None:
        import tempfile
        from lectern.repo import _Cache

        lock = (ROOT / "requirements-public-alpha.txt").read_bytes()
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "web").mkdir()
            source = root / "web" / "reader-control.md"
            source.write_text("**Strong** and [link](https://example.invalid/reader).", encoding="utf-8")
            (root / "requirements-public-alpha.txt").write_bytes(lock)
            with patch.object(webedition, "ROOT", root), patch.object(webedition, "_SET", _Cache(24)):
                first = webedition.set_for_terminal("web/reader-control.html", 80)
                self.assertIs(webedition.set_for_terminal("web/reader-control.html", 80), first)
                self.assertEqual(first["source"], "web/reader-control.md")
                self.assertTrue(any("$texts-color" in style for _, style in first["runs"]))
                self.assertEqual(next(iter(webedition._SET.items)),
                                 (str(source), source.stat().st_mtime_ns, 80))
                other_width = webedition.set_for_terminal("web/reader-control.html", 81)
                self.assertIsNot(other_width, first)
                self.assertEqual(other_width["columns"], 81)
                before = source.stat()
                os.utime(source, ns=(before.st_atime_ns, before.st_mtime_ns + 1000000000))
                self.assertIsNot(webedition.set_for_terminal("web/reader-control.html", 80), first)
                other = root / "web" / "other-control.md"
                other.write_bytes(source.read_bytes())
                self.assertEqual(webedition.set_for_terminal("web/other-control.html", 80)["source"],
                                 "web/other-control.md")

    def test_locked_dependency_and_pandoc_refusals_have_no_fallback(self) -> None:
        import _markdown_render

        with patch.object(_markdown_render, "distribution_version", return_value="0"):
            with self.assertRaisesRegex(Refused, "renderer refused"):
                webedition._html("A control, not a publication.")
        with patch.dict(sys.modules, {"markdown": None}):
            with self.assertRaisesRegex(Refused, "renderer refused"):
                webedition._html("A control, not a publication.")
        with patch.object(webedition.shutil, "which", return_value=None):
            with self.assertRaisesRegex(Refused, "pandoc is not installed"):
                webedition._ansi("<p>A control.</p>", 80)


@unittest.skipUnless(NODE, "node is required for page slices and the actual model protocol")
class AdapterContextTrimTests(unittest.TestCase):
    def test_slice_exports_only_the_consumed_contract(self) -> None:
        script = (
            "const assert=require('assert'); const s=require(process.argv[1]);"
            "assert.deepStrictEqual(Object.keys(s).sort(), ['FN','LINE','history','law','slicePage']);"
            "assert.deepStrictEqual(s(), {});"
        )
        done = subprocess.run(
            [NODE, "-e", script, str(ROOT / "scripts/lectern/adapters/page-slice.js")],
            capture_output=True, text=True, cwd=ROOT, timeout=30,
        )
        self.assertEqual(done.returncode, 0, done.stderr)

    def test_real_history_law_liturgy_and_refusal_protocol_still_work(self) -> None:
        self.assertEqual(bridge.call("history", "timeline", {})["state"]["start"], 1550)
        self.assertEqual(bridge.call("law", "lookup", "1008", "")["view"], "canon")
        self.assertTrue(bridge.call("liturgy", "propers", "roman-1962", "advent-1",
                                    {"orations": "la"})["notice"])
        for adapter, function in (("../bridge", "view"), ("law", "constructor"),
                                  ("page-slice", "section"), ("page-slice", "TABLE")):
            with self.subTest(adapter=adapter, function=function), self.assertRaises(Refused):
                bridge.call(adapter, function)

if __name__ == "__main__":
    unittest.main()
