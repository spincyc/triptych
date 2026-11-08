"""Canonical verse focus selects identical, whole fragments in both readers."""
from __future__ import annotations

import json
import asyncio
import importlib.util
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[2]
NODE = shutil.which("node")
MODEL = ROOT / "src/web/browser/catena/catena-model.js"


def fragment(identifier, source, first, last, first_chapter=1, last_chapter=1):
    return {"id": identifier, "source": source, "locator": identifier,
            "text_words": 7, "review": "verified", "extent": {
                "token": "Gen", "first_chapter": first_chapter, "last_chapter": last_chapter,
                "first_verse": first, "last_verse": last}}


SPINE = {
    "_fixture": "Synthetic range cases; not source evidence",
    "token": "Gen", "chapter": 1, "text_prefix": "structure/catena/text/",
    "sources": {
        "latin": {"author": "Author A", "work": "Synthetic commentary", "date": 300,
                  "voice": "original", "language": "la", "rights": "public-domain"},
        "english": {"author": "Author B", "work": "Synthetic translation", "date": 400,
                    "voice": "translation", "language": "en", "rights": "public-domain"},
    },
    "fragments": [fragment("fixture.before", "latin", 1, 2),
                  fragment("fixture.touching", "latin", 2, 4),
                  fragment("fixture.english", "english", 3, 3),
                  fragment("fixture.after", "english", 7, 9),
                  fragment("fixture.crossing", "english", 8, 2, last_chapter=2)],
    "leads": [{"author": "Lead author", "title": "Chapter-level lead"}],
    "blocked": [], "refusals": {},
}


@unittest.skipUnless(NODE, "Node is required")
class PassageModelTest(unittest.TestCase):
    def probe(self, expression):
        code = "const M=require(process.argv[1]), spine=JSON.parse(process.argv[2]);" + expression
        done = subprocess.run([NODE, "-e", code, str(MODEL), json.dumps(SPINE)],
                              check=True, capture_output=True, text=True)
        return json.loads(done.stdout)

    def test_only_overlaps_survive_and_original_objects_and_extents_remain(self):
        result = self.probe("""
const rows=M.chapterFragments(spine), selected=M.passageSelection(spine,1,'3-4','',[]);
process.stdout.write(JSON.stringify({ids:selected.visible.map(row=>row.id),
  whole:selected.visible.every(row=>rows.includes(row)),
  extents:selected.visible.map(row=>M.formatExtent(row.extent,'Genesis')),
  english:selected.english}));
""")
        self.assertEqual(result["ids"], ["fixture.touching", "fixture.english"])
        self.assertTrue(result["whole"])
        self.assertEqual(result["extents"], ["Genesis 1:2-4", "Genesis 1:3"])
        self.assertEqual(result["english"], 1)

    def test_cross_chapter_fragment_only_overlaps_the_reached_verses(self):
        values = self.probe("""
const extent=spine.fragments.at(-1).extent;
process.stdout.write(JSON.stringify([[1,'7'],[1,'8'],[2,'1-2'],[2,'3'],[3,'1']]
  .map(([chapter,verses])=>M.touchesPassage(extent,chapter,verses))));
""")
        self.assertEqual(values, [False, True, True, False, False])

    def test_invalid_ranges_never_become_all_fragments(self):
        result = self.probe("""
const values=['0','-1','8-3','1:3-2:4','1,3','3-',' 3','3.5',{},'9007199254740993'];
process.stdout.write(JSON.stringify(values.map(value=>({parsed:M.parseVerses(value),
  count:M.passageSelection(spine,1,value,'',[]).visible.length}))));
""")
        self.assertEqual(result, [{"parsed": None, "count": 0}] * 10)

    def test_author_exclusions_and_voice_never_change_english_holdings_count(self):
        result = self.probe("""
const selected=M.passageSelection(spine,1,'3-4','original',['Author A']);
process.stdout.write(JSON.stringify({count:selected.visible.length,authors:selected.authors,
  english:selected.english,note:selected.empty,context:selected.contextNote}));
""")
        self.assertEqual(result["count"], 0)
        self.assertEqual(result["authors"], ["Author A"])
        self.assertEqual(result["english"], 1)
        self.assertIn("Every author is switched off", result["note"])
        self.assertIn("whole chapter", result["context"])


@unittest.skipUnless(NODE, "Node is required")
class PassageReadersTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        from . import test_catena_production as production
        from ._product_data import browser_data_root

        scratch = ROOT / ".scratch/reader-ui"
        scratch.mkdir(parents=True, exist_ok=True)
        cls.folder = tempfile.TemporaryDirectory(prefix="passage-", dir=scratch)
        cls.addClassCleanup(cls.folder.cleanup)
        cls.path = Path(cls.folder.name)
        data = browser_data_root()
        files = {"structure/catena/01-gen/001.json": SPINE}
        for row in SPINE["fragments"]:
            files["structure/catena/text/" + row["id"] + ".json"] = {
                "id": row["id"], "text": "Synthetic source text for " + row["id"],
                "basis": "Synthetic extent evidence", "date_basis": "Synthetic date evidence"}
        cls.fixture = cls.path / "data"
        for name, value in files.items():
            destination = cls.fixture / name
            destination.parent.mkdir(parents=True, exist_ok=True)
            destination.write_text(json.dumps(value))
        for name in ("bibles.json", "structure/catena/index.json", "structure/catena/scripture",
                     "structure/paragraphs"):
            (cls.fixture / name).symlink_to(data / name, target_is_directory=(data / name).is_dir())

        base = production.GEN1
        cls.base = base
        scenarios = [
            {"name": "focus", "hash": base + "&verses=3-4", "files": files,
             "steps": [{"do": "openEveryFragment", "label": "opened"}]},
            {"name": "voice", "hash": base + "&verses=3-4&voice=original", "files": files},
            {"name": "empty", "hash": base + "&verses=5-6", "files": files},
            {"name": "voice-empty", "hash": base + "&verses=1&voice=translation:en", "files": files},
            {"name": "hidden", "hash": base + "&verses=3-4", "files": files,
             "steps": [{"do": "toggleAuthor", "author": "Author A", "label": "hide-a"},
                       {"do": "toggleAuthor", "author": "Author B", "label": "hidden"}]},
            {"name": "history", "hash": base + "&verses=3-4", "files": files,
             "steps": [{"do": "hash", "value": base + "&verses=1", "label": "back"},
                       {"do": "hash", "value": base + "&verses=3-4", "label": "forward"}]},
            {"name": "invalid", "hash": base + "&verses=4-3", "files": files},
            {"name": "duplicate", "hash": base + "&verses=3&verses=4", "files": files},
            {"name": "outside", "hash": base + "&verses=999", "files": files},
            {"name": "input", "hash": base, "files": files,
             "steps": [{"do": "setVerses", "value": "3-4", "label": "focus"},
                       {"do": "setVerses", "value": "999", "label": "refused"},
                       {"do": "clearVerses", "label": "clear"}]},
            {"name": "chapter", "hash": base + "&verses=3-4", "files": files,
             "steps": [{"do": "selectChapter", "value": "2", "label": "next"}]},
        ]
        script, plan = cls.path / "replay.cjs", cls.path / "plan.json"
        script.write_text(production.REPLAY)
        plan.write_text(json.dumps(scenarios))
        done = subprocess.run([NODE, str(script), str(ROOT), str(plan)], check=True,
                              capture_output=True, text=True, timeout=60)
        cls.pages = json.loads(done.stdout)

    def adapter(self, fn, *args):
        request = {"id": 1, "adapter": "catena", "fn": fn, "args": args}
        done = subprocess.run([NODE, str(ROOT / "scripts/lectern/bridge.js"), str(self.fixture)],
                              input=json.dumps(request) + "\n", check=True, capture_output=True,
                              text=True, timeout=30)
        result = json.loads(done.stdout)
        self.assertTrue(result["ok"], result)
        return result["value"]

    def test_web_and_terminal_select_identical_fragments_and_keep_full_extents(self):
        for name, verses, voice in (("focus", "3-4", ""), ("voice", "3-4", "original"),
                                     ("empty", "5-6", ""), ("voice-empty", "1", "translation:en")):
            with self.subTest(name=name):
                page = self.pages[name]
                self.assertNotIn("error", page, page)
                view = self.adapter("view", "Gen", 1, "douay-rheims", voice, verses)
                self.assertEqual(page["fragmentIds"], [row["id"] for row in view["chain"]["fragments"]])
                self.assertEqual(page["referenceText"], view["reference"])
                for note in view["chain"]["notes"]:
                    self.assertIn(note, page["asideNotes"])
                self.assertTrue(all(not group["open"] for group in page["authorGroups"]))

    def test_empty_focus_is_not_an_empty_chapter_and_does_not_fetch_text(self):
        page = self.pages["empty"]
        self.assertIn("5 fragments held", page["tallyText"])
        self.assertIn("0 fragments match", page["tallyText"])
        self.assertTrue(any("No renderable fragment" in note for note in page["asideNotes"]))
        self.assertFalse(any("/catena/text/" in path for path in page["fetched"]))
        self.assertIn("1 fragment matches", self.pages["voice"]["tallyText"])

    def test_history_restores_focus_without_new_history_entries(self):
        page = self.pages["history"]
        self.assertEqual(page["snapshots"]["back"]["fragmentIds"], ["fixture.before"])
        self.assertEqual(page["snapshots"]["forward"]["fragmentIds"], ["fixture.touching", "fixture.english"])
        self.assertEqual(page["hashWrites"], [])
        self.assertEqual(page["replaced"], [])

    def test_invalid_and_duplicate_focus_preserve_address_and_refuse(self):
        for name in ("invalid", "duplicate", "outside"):
            self.assertTrue(self.pages[name]["errorSections"])
            self.assertEqual(self.pages[name]["hashWrites"], [])
            self.assertEqual(self.pages[name]["replaced"], [])
        self.assertTrue(self.adapter("view", "Gen", 1, "douay-rheims", "", "4-3")["problems"])
        self.assertIn("1-31", self.adapter("view", "Gen", 1, "douay-rheims", "", "999")["problems"][0]["note"])

    def test_input_applies_valid_ranges_and_preserves_reading_on_invalid_bounds(self):
        page = self.pages["input"]
        self.assertEqual(page["snapshots"]["focus"]["fragmentIds"], ["fixture.touching", "fixture.english"])
        self.assertEqual(page["snapshots"]["refused"]["fragmentIds"], ["fixture.touching", "fixture.english"])
        self.assertEqual(page["snapshots"]["refused"]["hash"], self.base + "&verses=3-4")
        self.assertEqual(len(page["snapshots"]["clear"]["fragmentIds"]), 5)
        self.assertNotIn("verses=", page["snapshots"]["clear"]["hash"])

    def test_excluding_every_author_has_equivalent_recovery_text(self):
        page = self.pages["hidden"]
        view = self.adapter("view", "Gen", 1, "douay-rheims", "", "3-4", ["Author A", "Author B"])
        self.assertEqual(view["chain"]["fragments"], [])
        self.assertEqual(view["chain"]["authors"], ["Author A", "Author B"])
        self.assertIn(view["chain"]["notes"][0], page["asideNotes"])
        self.assertTrue(page["authorFilterOpen"])
        self.assertTrue(all(row["hidden"] for row in page["authorGroups"]))

    def test_moving_chapter_clears_the_old_verse_range(self):
        page = self.pages["chapter"]["snapshots"]["next"]
        self.assertNotIn("verses=", page["hash"])
        self.assertEqual(page["referenceText"], "Genesis 2")

    def test_full_source_text_and_provenance_remain_accessible(self):
        page = self.pages["focus"]["snapshots"]["opened"]
        self.assertEqual(len(page["fragmentTexts"]), 2)
        self.assertIn("Genesis 1:2-4", page["extents"])
        for identifier in page["fragmentIds"]:
            body = self.adapter("body", "Gen", 1, "", identifier)
            self.assertFalse(body["missing"])
            self.assertEqual(body["said"], "Synthetic source text for " + identifier)
            self.assertEqual(body["basis"], "Synthetic extent evidence")

    @unittest.skipUnless(importlib.util.find_spec("textual"), "Textual is required")
    def test_terminal_keyboard_ranges_exclusions_disclosures_and_chapter_reset(self):
        from lectern.app import TriptychApp
        from lectern.surfaces.catena import Catena
        from textual.widgets import Input, OptionList

        opening = self.adapter("opening")

        def call(adapter, fn, *args):
            self.assertEqual(adapter, "catena")
            if fn == "density":
                return [{"fragments": 5, "leads": 1, "blocked": 0, "unreadable": False}] * 50
            return self.adapter(fn, *args)

        async def settled(app, pilot):
            for _ in range(100):
                if not any(not worker.is_finished for worker in app.workers):
                    await pilot.pause(0.05)
                    return
                await pilot.pause(0.05)
            self.fail("Catena terminal worker did not settle")

        async def exercise():
            with patch.object(Catena, "start", lambda _: None), patch("lectern.bridge.call", side_effect=call):
                app = TriptychApp(start="catena")
                async with app.run_test(size=(140, 42)) as pilot:
                    owner = app.current()
                    owner.opened_with(opening)
                    await settled(app, pilot)
                    self.assertEqual(owner.opened_groups, set())
                    await pilot.press("enter")
                    self.assertEqual(owner.opened_groups, {0})
                    await pilot.press("enter")
                    self.assertEqual(owner.opened_groups, set())
                    await pilot.press("r")
                    app.screen.query_one(Input).value = "3-4"
                    await pilot.press("enter")
                    await settled(app, pilot)
                    self.assertEqual(owner.verses, "3-4")
                    self.assertEqual([row["id"] for row in owner.current["chain"]["fragments"]],
                                     ["fixture.touching", "fixture.english"])
                    await pilot.press("r")
                    app.screen.query_one(Input).value = "999"
                    await pilot.press("enter")
                    await settled(app, pilot)
                    self.assertEqual(owner.verses, "3-4")
                    await pilot.press("x", "down", "down", "enter")
                    await settled(app, pilot)
                    self.assertEqual(owner.hidden_authors, {"Author A"})
                    self.assertEqual([row["id"] for row in owner.current["chain"]["fragments"]],
                                     ["fixture.english"])
                    await pilot.press("x", "down", "enter")
                    await settled(app, pilot)
                    self.assertEqual(owner.hidden_authors, set())
                    await pilot.press("right")
                    await settled(app, pilot)
                    self.assertEqual(owner.chapter, 2)
                    self.assertEqual(owner.verses, "")

        asyncio.run(exercise())


@unittest.skipUnless(NODE and shutil.which("chromium"), "Chromium and Node are required")
class PassageBrowserTest(unittest.TestCase):
    @unittest.skipUnless(importlib.util.find_spec("textual"), "Textual is required")
    def test_current_luke_fragment_precedes_chapter_translation_research_in_both_readers(self):
        from ._cdp_drive import act, drive, wait
        from ._product_data import browser_data_root
        from lectern.app import TriptychApp
        from lectern.surfaces.catena import Catena
        from textual.widgets import OptionList

        data = browser_data_root()
        request = {"id": 1, "adapter": "catena", "fn": "view",
                   "args": ["Luke", 24, "douay-rheims", "translation:en", "50-53"]}
        done = subprocess.run([NODE, str(ROOT / "scripts/lectern/bridge.js"), str(data)],
                              input=json.dumps(request) + "\n", capture_output=True, text=True, check=True)
        reply = json.loads(done.stdout)
        self.assertTrue(reply["ok"], reply)
        view = reply["value"]
        if not view.get("chain", {}).get("fragments"):
            self.skipTest("Selected fixture predates the admitted Luke English fragment")
        self.assertEqual(len(view["chain"]["fragments"]), 1)
        self.assertIn("Aquinas", view["chain"]["fragments"][0]["author"])
        self.assertTrue(any("Bede" in row["author"] for row in view["chain"]["absences"]["rows"]))

        route = "/src/web/browser/catena/index.html?data=/src/web/data#book=Luke&chapter=24&bible=douay-rheims&voice=translation%3Aen&verses=50-53"
        seen = drive({"acts": [{"do": "navigate", "url": route},
            wait("document.querySelector('.author') && document.querySelector('.absence-note')"),
            act("({author:document.querySelector('.author').textContent,absence:document.querySelector('.absence-note').textContent,order:!!(document.querySelector('.author').compareDocumentPosition(document.querySelector('.absence-note')) & Node.DOCUMENT_POSITION_FOLLOWING)})", "order")]})["order"]
        self.assertIn("Aquinas", seen["author"])
        self.assertIn("Bede", seen["absence"])
        self.assertTrue(seen["order"])

        async def terminal():
            with patch.object(Catena, "start", lambda _: None):
                app = TriptychApp(start="catena")
                async with app.run_test(size=(140, 42)) as pilot:
                    owner = app.current()
                    owner.show(view)
                    await pilot.pause()
                    listing = owner.query_one("#catena-chain-list", OptionList)
                    rows = [listing.get_option_at_index(i) for i in range(listing.option_count)]
                    author = next(i for i, row in enumerate(rows) if row.id == "grp-0")
                    absence = next(i for i, row in enumerate(rows) if "Bede" in str(row.prompt))
                    self.assertLess(author, absence)
                    self.assertEqual(owner.opened_groups, set())
        asyncio.run(terminal())

    def test_real_keyboard_focus_history_bounds_and_lazy_source_text(self):
        from ._cdp_drive import act, drive, wait

        ready = "document.querySelector('#reading[aria-busy=false] .chain')"
        route = "/src/web/browser/catena/index.html?data=/src/web/data#book=Gen&chapter=1&bible=douay-rheims"
        snapshot = """({hash:location.hash,reference:document.querySelector('#reference').textContent,
          ids:[...document.querySelectorAll('.fragment-whole')].map(a=>decodeURIComponent(a.hash.slice(9))),
          opened:document.querySelectorAll('.author-body[open],.fragment-body[open]').length,
          errors:document.querySelectorAll('.catena-error').length})"""
        result = drive({"acts": [
            {"do": "navigate", "url": route}, wait(ready), act(snapshot, "whole"),
            act("document.querySelector('#verse-input').value='3-4'; document.querySelector('#verse-input').focus()"),
            {"do": "key", "key": "Enter", "code": "Enter", "virtualKeyCode": 13, "text": "\r"},
            wait("document.querySelector('#reference').textContent==='Genesis 1:3-4' && location.hash.includes('verses=3-4')"),
            act(snapshot, "focus"), act("history.back()"),
            wait("document.querySelector('#reference').textContent==='Genesis 1' && !location.hash.includes('verses=')"),
            act(snapshot, "back"), act("history.forward()"),
            wait("document.querySelector('#reference').textContent==='Genesis 1:3-4' && location.hash.includes('verses=3-4')"),
            act(snapshot, "forward"),
            act("document.querySelector('#verse-input').value='999'; document.querySelector('#passage-focus').requestSubmit()"),
            wait("!document.querySelector('#verse-error').hidden"),
            act("document.querySelector('#verse-error').textContent", "error"), act(snapshot, "refused"),
            act("document.querySelector('#read-commentary').focus()"),
            {"do": "key", "key": "Enter", "code": "Enter", "virtualKeyCode": 13, "text": "\r"},
            wait("document.activeElement.classList.contains('chain-column')"),
            act("({hash:location.hash,role:document.activeElement.getAttribute('role'),name:document.activeElement.getAttribute('aria-label'),visibleFocus:getComputedStyle(document.activeElement).outlineStyle!=='none' && parseFloat(getComputedStyle(document.activeElement).outlineWidth)>0})", "commentary-focus"),
            act("document.querySelector('.author-body').open=true; document.querySelector('.fragment-body').open=true"),
            wait("document.querySelector('.fragment-text') && document.querySelector('.fragment-text').textContent.length > 30 && !document.querySelector('.fragment-text').classList.contains('missing')"),
            act("({text:document.querySelector('.fragment-text').textContent,source:document.querySelector('.fragment-whole').getAttribute('href')})", "source"),
        ]})
        self.assertGreater(len(result["whole"]["ids"]), len(result["focus"]["ids"]))
        self.assertGreater(len(result["focus"]["ids"]), 0)
        self.assertEqual(result["whole"]["opened"], 0)
        self.assertEqual(result["whole"], result["back"])
        self.assertEqual(result["focus"], result["forward"])
        self.assertEqual(result["focus"], result["refused"])
        self.assertIn("1-31", result["error"])
        self.assertEqual(result["commentary-focus"], {"hash": result["focus"]["hash"],
                         "role": "region", "name": "Commentary fragments", "visibleFocus": True})
        self.assertGreater(len(result["source"]["text"]), 30)
        self.assertTrue(result["source"]["source"].startswith("../sources/#passage="))


if __name__ == "__main__":
    unittest.main()
