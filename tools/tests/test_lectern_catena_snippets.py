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
                    owner = app.current()
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
                owner = app.current()
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
                owner = app.current()
                fragment, body = self.fragment(), self.body()
                body.update(missing=True, said="The excerpt metadata is invalid.")
                self.set_current(owner, fragment)
                owner.open_reading(0, fragment, body)
                await pilot.pause()
                self.assertIn(body["said"], str(app.screen.body))
                self.assertNotIn(body["snippets"][0]["text"], str(app.screen.body))
                self.assertFalse(app.screen.excerpts)


if __name__ == "__main__":
    unittest.main()
