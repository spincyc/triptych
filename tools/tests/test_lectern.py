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

import importlib.util
import json
import shutil
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))

from lectern import bridge, refs  # noqa: E402
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
        self.assertTrue(view["unresolvedChoices"])
        self.assertEqual(view["events"], [])
        self.assertIsNone(view["mass"])

    def test_the_choice_once_made_is_read(self) -> None:
        options = {"orations": "en", "mass": "ot-29-thursday"}
        view = bridge.call("liturgy", "day", "postconciliar", "2026-10-22", options)
        self.assertEqual(view["unresolvedChoices"], [])
        self.assertEqual(view["mass"]["key"], options["mass"])
        self.assertTrue(any(event["kind"] == "proper" for event in view["events"]))

    def test_a_missing_translation_is_said_at_the_text_and_the_latin_kept(self) -> None:
        view = bridge.call("liturgy", "day", "roman-1962", "2026-10-22", {"orations": "en"})
        collect = next(event for event in view["events"] if event.get("slot") == "Collect")
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

    def test_every_surface_opens(self) -> None:
        from lectern.surfaces import ORDER

        for kind in ORDER:
            with self.subTest(surface=kind.label):
                drawn = self.snapshot("--surface", kind.surface_id(), "--date", "2026-10-22")
                self.assertNotIn("could not be opened", drawn)
                self.assertNotIn("Traceback", drawn)

    def test_a_drawing_depends_on_its_arguments_and_not_the_clock(self) -> None:
        first = self.snapshot("--surface", "day", "--date", "2026-10-22")
        second = self.snapshot("--surface", "day", "--date", "2026-10-22")
        self.assertEqual(first, second)

    def test_the_day_says_what_the_page_says(self) -> None:
        drawn = self.snapshot("--surface", "day", "--date", "2026-10-22", "--calendar", "roman-1962")
        self.assertIn("Twenty-first Sunday after Pentecost", drawn)
        self.assertIn("Bible reconstruction", drawn)

    def test_an_open_choice_is_drawn_open(self) -> None:
        drawn = self.snapshot("--surface", "day", "--date", "2026-10-22", "--calendar", "postconciliar")
        self.assertIn("Nothing is selected for you by order", drawn)
        self.assertIn("No single Mass is read here yet", drawn)


if __name__ == "__main__":
    unittest.main()
