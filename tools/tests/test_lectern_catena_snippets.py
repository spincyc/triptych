"""Matched commentary excerpts retain complete context and source navigation."""
from __future__ import annotations

import importlib.util
from pathlib import Path
import sys
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))
TEXTUAL = importlib.util.find_spec("textual") is not None


@unittest.skipUnless(TEXTUAL, "Textual is required for commentary reading controls")
class CatenaExcerptReadingTests(unittest.IsolatedAsyncioTestCase):
    async def ready(self, app, pilot):
        from lectern.snapshot import _settle
        await _settle(app, pilot)
        return app.current()

    def fragment(self):
        return {
            "id": "passage.fixture.commentary.edition.section", "author": "Commentator",
            "date": 400, "work": "Commentary", "locator": "Section 3", "extent": "Philippians 1:18–24",
            "spans": False, "chip": "English translation", "text_words": 100,
            "edition": "Source edition", "edition_published": "1900", "translators": ["Translator"],
            "rights": "licensed-free", "attribution": "Source attribution", "rights_basis": "Fixture licence",
            "reviewNote": "inspected, not collated",
        }

    def body(self):
        text = "Exact excerpt with ⛪ and [bold] literal text.\nSecond line."
        return {
            "missing": False, "said": "Whole source opening.\n" + text + "\nWhole source ending.",
            "acknowledgement": "Required fixture acknowledgement", "basis": "Natural extent basis",
            "date_basis": "Composition basis", "snippets": [{
                "id": "verse-21", "extent": "Philippians 1:21", "locator": "Section 3, verse 21",
                "basis": "The source explicitly discusses verse 21 here.", "text": text,
            }],
        }

    def set_current(self, owner, fragment):
        owner.current = {
            "chain": {"fragments": [fragment]}, "reference": "Philippians 1:21",
            "bible": {"label": "Fixture Bible"}, "tally": {"spoken": "1 fragment"},
        }

    async def test_excerpt_full_context_toggle_and_source_action_at_both_sizes(self):
        from lectern.app import TriptychApp
        from lectern.surfaces.catena import Catena, FragmentReading

        for size in ((80, 24), (140, 40)):
            with self.subTest(size=size), patch.object(Catena, "start", lambda owner: None):
                app = TriptychApp(start="catena")
                async with app.run_test(size=size) as pilot:
                    owner = await self.ready(app, pilot)
                    fragment, body = self.fragment(), self.body()
                    self.set_current(owner, fragment)
                    owner.open_reading(0, fragment, body)
                    await pilot.pause()
                    self.assertIsInstance(app.screen, FragmentReading)
                    excerpt = str(app.screen.body)
                    self.assertIn(body["snippets"][0]["text"], excerpt)
                    self.assertIn(body["snippets"][0]["basis"], excerpt)
                    self.assertIn("Section 3, verse 21", excerpt)
                    self.assertIn(body["acknowledgement"], excerpt)
                    self.assertNotIn("Whole source opening.", excerpt)
                    self.assertIn("c full context", app.screen.subtitle)

                    await pilot.press("c")
                    await pilot.pause()
                    self.assertIn(body["said"], str(app.screen.body))
                    self.assertIn(body["acknowledgement"], str(app.screen.body))
                    self.assertIn("Complete source passage", str(app.screen.body))
                    self.assertIn("c excerpts", app.screen.subtitle)
                    await pilot.press("c")
                    await pilot.pause()
                    self.assertEqual(str(app.screen.body), excerpt)
                    with patch.object(app, "action_surface") as source:
                        await pilot.press("s")
                        await pilot.pause()
                        source.assert_called_once_with("sources", passage=fragment["id"])

    async def test_without_matching_excerpts_full_fragment_remains_available(self):
        from lectern.app import TriptychApp
        from lectern.surfaces.catena import Catena

        with patch.object(Catena, "start", lambda owner: None):
            app = TriptychApp(start="catena")
            async with app.run_test(size=(80, 30)) as pilot:
                owner = await self.ready(app, pilot)
                fragment, body = self.fragment(), self.body()
                body["snippets"] = []
                self.set_current(owner, fragment)
                owner.open_reading(0, fragment, body)
                await pilot.pause()
                screen = app.screen
                self.assertIn(body["said"], str(screen.body))
                self.assertNotIn("Matched commentary excerpts", str(screen.body))
                self.assertNotIn("c full context", screen.subtitle)
                await pilot.press("c")
                self.assertIs(app.screen, screen)

    async def test_refused_body_never_displays_excerpts_or_offers_context(self):
        from lectern.app import TriptychApp
        from lectern.surfaces.catena import Catena

        with patch.object(Catena, "start", lambda owner: None):
            app = TriptychApp(start="catena")
            async with app.run_test(size=(80, 30)) as pilot:
                owner = await self.ready(app, pilot)
                fragment, body = self.fragment(), self.body()
                body.update(missing=True, said="The excerpt metadata is invalid.")
                self.set_current(owner, fragment)
                owner.open_reading(0, fragment, body)
                await pilot.pause()
                self.assertIn(body["said"], str(app.screen.body))
                self.assertNotIn(body["snippets"][0]["text"], str(app.screen.body))
                self.assertFalse(app.screen.excerpts)

    async def test_finder_filters_chapters_opens_reference_and_cancels(self):
        from lectern.app import TriptychApp
        from lectern.catena_find import CommentaryFinder
        from lectern.surfaces.catena import Catena

        for size in ((60, 16), (140, 40)):
            with self.subTest(size=size), patch.object(Catena, "start", lambda owner: None):
                app = TriptychApp(start="catena")
                async with app.run_test(size=size) as pilot:
                    owner = await self.ready(app, pilot)
                    owner.books = [{"token": "Mark", "name": "Mark"}]
                    owner.holdings = [{**owner.books[0], "chapters": [
                        {"chapter": 1, "fragments": 9, "english": 0}, {"chapter": 10, "fragments": 4, "english": 2},
                    ]}]
                    owner.voice = "original"
                    owner.verses = "1-3"
                    owner.hidden_authors = {"Excluded author"}
                    with patch.object(owner, "load") as load:
                        await pilot.press("i")
                        self.assertIsInstance(app.screen, CommentaryFinder)
                        self.assertEqual(len(app.screen.matches), 2)
                        await pilot.press("tab", "space")
                        self.assertEqual(app.screen.matches, [("Mark", 10)])
                        await pilot.press("tab", "enter")
                        self.assertEqual((owner.token, owner.chapter, owner.verses, owner.voice), ("Mark", 10, "", ""))
                        self.assertEqual(owner.hidden_authors, {"Excluded author"})
                        load.assert_called_once()
                        await pilot.press("i", "m", "a", "r", "k", "space", "1")
                        self.assertEqual(app.screen.matches, [("Mark", 1)])
                        await pilot.press("0", "enter")
                        self.assertEqual(load.call_count, 2)
                        await pilot.press("i", "z")
                        self.assertEqual(app.screen.matches, [])
                        await pilot.press("enter", "escape")
                        self.assertEqual(load.call_count, 2)

    async def test_scripture_and_commentary_choices_are_independent(self):
        from lectern.app import TriptychApp
        from lectern.dialogs import Pick
        from lectern.surfaces.catena import Catena

        with patch.object(Catena, "start", lambda owner: None):
            app = TriptychApp(start="catena")
            async with app.run_test(size=(80, 24)) as pilot:
                owner = await self.ready(app, pilot)
                self.set_current(owner, self.fragment())
                owner.current["voices"] = [{"value": "", "label": "Everything held"},
                                           {"value": "translation:en", "label": "English translation"}]
                owner.bibles = [{"id": "first", "label": "Edition One", "languageName": "English",
                                 "numberingLabel": "hebrew numbering, psalm titles unnumbered"},
                                {"id": "second", "label": "Edition Two", "languageName": "Latin",
                                 "numberingLabel": "vulgate numbering"}]
                owner.bible, owner.voice = "first", ""
                with patch.object(owner, "load") as load:
                    await pilot.press("B")
                    self.assertIsInstance(app.screen, Pick)
                    self.assertIn("Latin · vulgate numbering", str(app.screen.options[1][1]))
                    await pilot.press("down", "down", "enter")
                    self.assertEqual((owner.bible, owner.voice), ("second", ""))
                    await pilot.press("V", "down", "down", "enter")
                    self.assertEqual((owner.bible, owner.voice), ("second", "translation:en"))
                    await pilot.press("b", "v")
                    self.assertEqual((owner.bible, owner.voice), ("first", ""))
                    await pilot.press("B", "escape", "V", "escape")
                    self.assertEqual(load.call_count, 4)

    async def test_linked_version_reads_its_own_edition_and_returns_to_original(self):
        from lectern.app import TriptychApp
        from lectern.dialogs import Pick
        from lectern.surfaces.catena import Catena, FragmentReading

        original = dict(self.fragment(), chip="Latin — the author’s own", translators=[], edition="Latin edition")
        english = dict(self.fragment(), id="passage.fixture.english", edition="English edition")
        original["englishVersions"] = [{"fragment": english, "basis": "These sections correspond.", "coverage": "excerpt"}]
        original_body = dict(self.body(), snippets=[], said="Original wording.")
        english_body = dict(self.body(), snippets=[], said="Translated wording.", acknowledgement="English credit.")
        with patch.object(Catena, "start", lambda owner: None):
            app = TriptychApp(start="catena")
            async with app.run_test(size=(80, 24)) as pilot:
                owner = await self.ready(app, pilot)
                self.set_current(owner, original)
                owner.current.update(book={"token": "Phil"}, chapter=1, voice="original", verses="21")
                with patch("lectern.bridge.call", return_value=english_body) as fetch:
                    owner.open_reading(0, original, original_body)
                    await pilot.pause()
                    screen = app.screen
                    await pilot.press("p", "n")
                    self.assertIs(app.screen, screen)
                    await pilot.press("e")
                    await self.ready(app, pilot)
                    self.assertIsInstance(app.screen, FragmentReading)
                    fetch.assert_called_once_with("catena", "body", "Phil", 1, "original", english["id"], "21")
                    for expected in ("Translated wording.", "English credit.", english["id"], "English edition",
                                     "Translated by Translator", "English version · excerpt", "These sections correspond."):
                        self.assertIn(expected, str(app.screen.body))
                    self.assertNotIn("Original wording.", str(app.screen.body))
                    await pilot.press("escape")
                    self.assertIn("Original wording.", str(app.screen.body))
                    self.assertEqual(fetch.call_count, 1)
                    second = dict(english, id="passage.fixture.second", extent="Philippians 1:30")
                    original["englishVersions"].append(dict(fragment=second, basis="Complete correspondence.", coverage="whole"))
                    await pilot.press("e")
                    self.assertIsInstance(app.screen, Pick)
                    self.assertIn(english["extent"], str(app.screen.options[0][1]))
                    self.assertIn(second["extent"], str(app.screen.options[1][1]))
                    await pilot.press("escape")
                    self.assertIn("Original wording.", str(app.screen.body))
                    second["extent"] = english["extent"]
                    await pilot.press("e")
                    self.assertIn("Complete correspondence.", str(app.screen.options[1][1]))
                    await pilot.press("down", "down", "enter")
                    await self.ready(app, pilot)
                    self.assertIn("English version · whole passage", str(app.screen.body))
                    with patch.object(app, "action_surface") as source:
                        await pilot.press("s")
                        source.assert_called_once_with("sources", passage=second["id"])


if __name__ == "__main__":
    unittest.main()
