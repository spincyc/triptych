"""Compact panes remain readable without changing the held text or its route."""
from __future__ import annotations

import importlib.util
from pathlib import Path
import shutil
import sys
import unittest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))
AVAILABLE = importlib.util.find_spec("textual") is not None and shutil.which("node")


@unittest.skipUnless(AVAILABLE, "Textual and node are required")
class CompactReaderTests(unittest.IsolatedAsyncioTestCase):
    async def settle(self, app, pilot):
        from lectern.snapshot import _settle
        await _settle(app, pilot)

    async def test_propers_missal_names_fit_without_an_orphan_hotkey(self):
        from lectern.app import TriptychApp
        for width in (80, 120, 180):
            with self.subTest(width=width):
                app = TriptychApp(start="propers", intent={"calendar": "roman-1962"})
                async with app.run_test(size=(width, 40)) as pilot:
                    await self.settle(app, pilot)
                    self.assertEqual(app.query_one("#propers-missals").region.height, 1)
                    self.assertIn("Postconciliar", str(app.query_one("#propers-missals").render()))
                    await pilot.press("c")
                    await self.settle(app, pilot)
                    self.assertNotEqual(app.current().calendar, "roman-1962")

    async def test_catena_compact_reading_and_focus_survive_resize(self):
        from lectern.app import TriptychApp
        from lectern.surface import shown
        app = TriptychApp(start="catena", intent={"ref": "Phil 1"})
        async with app.run_test(size=(80, 30)) as pilot:
            await self.settle(app, pilot)
            owner = app.current()
            scripture = app.query_one("#catena-scripture")
            chain = app.query_one("#catena-chain")
            self.assertGreaterEqual(scripture.size.width, 70)
            self.assertGreaterEqual(chain.size.width, 70)
            self.assertGreaterEqual(chain.region.y, scripture.region.bottom)
            self.assertTrue(shown(app.query_one("#catena-instruction")))
            scripture.scroll_relative(y=3, animate=False)
            await pilot.pause()
            position = scripture.scroll_y
            await pilot.press("enter")
            groups = set(owner.opened_groups)
            self.assertTrue(groups)
            await pilot.press("f")
            await self.settle(app, pilot)
            self.assertFalse(shown(app.query_one("#catena-leads")))
            self.assertEqual(scripture.scroll_y, position)
            for width in (120, 180, 80):
                await pilot.resize_terminal(width, 40 if width > 80 else 30)
                await self.settle(app, pilot)
                self.assertTrue(shown(app.focused))
                self.assertEqual(owner.opened_groups, groups)
                self.assertEqual(owner.current["reference"], "Philippians 1")
            await pilot.press("f")
            await self.settle(app, pilot)
            self.assertTrue(shown(app.query_one("#catena-leads")))
            self.assertTrue(shown(app.query_one("#catena-strip-box")))

    async def test_catena_enter_walk_and_source_keep_the_selected_fragment(self):
        from lectern.app import TriptychApp
        from lectern.dialogs import Reading
        app = TriptychApp(start="catena", intent={"ref": "Phil 1"})
        async with app.run_test(size=(80, 30)) as pilot:
            await self.settle(app, pilot)
            first = app.current().current["chain"]["fragments"][0]
            await pilot.press("enter", "down", "enter")
            await self.settle(app, pilot)
            self.assertIsInstance(app.screen, Reading)
            body = str(app.screen.body)
            self.assertIn(first["id"], body)
            self.assertIn("Composition date not established", body)
            await pilot.press("n")
            await self.settle(app, pilot)
            self.assertIsInstance(app.screen, Reading)
            self.assertNotEqual(str(app.screen.body), body)
            await pilot.press("p")
            await self.settle(app, pilot)
            self.assertEqual(str(app.screen.body), body)
            await pilot.press("s")
            await self.settle(app, pilot)
            self.assertEqual(app.current().surface_id(), "sources")
            self.assertEqual(app.current().passage["id"], first["id"])

    async def test_cramped_catena_keeps_the_author_and_selected_fragment_visible(self):
        from lectern.app import TriptychApp
        from lectern.dialogs import Reading
        from lectern.snapshot import _text
        from lectern.surface import shown

        app = TriptychApp(start="catena", intent={"ref": "Phil 1"})
        async with app.run_test(size=(80, 24)) as pilot:
            await self.settle(app, pilot)
            listing = app.query_one("#catena-chain-list")
            chain = app.query_one("#catena-chain")

            def visible_list():
                self.assertTrue(listing.has_focus)
                self.assertTrue(shown(listing))
                self.assertGreaterEqual(listing.region.height, min(3, listing.option_count))
                self.assertGreaterEqual(listing.region.y, chain.content_region.y)
                self.assertLessEqual(listing.region.bottom, chain.content_region.bottom)

            visible_list()
            self.assertIn("John Chrysostom", _text(app, styles=False))
            await pilot.press("enter", "down")
            await self.settle(app, pilot)
            self.assertEqual(listing.highlighted_option.id, "frag-0")
            visible_list()
            extent = app.current().current["chain"]["fragments"][0]["extent"]
            self.assertIn(extent, _text(app, styles=False))
            await pilot.press("enter")
            await self.settle(app, pilot)
            self.assertIsInstance(app.screen, Reading)
            body = str(app.screen.body)
            self.assertIn(app.current().current["chain"]["fragments"][0]["id"], body)
            await pilot.press("escape")
            for _ in range(2):
                await pilot.press("f")
                await self.settle(app, pilot)
                visible_list()
                self.assertEqual(listing.highlighted_option.id, "frag-0")
                self.assertIn(extent, _text(app, styles=False))
            for width, height in ((80, 30), (120, 40), (180, 40), (80, 24)):
                await pilot.resize_terminal(width, height)
                await self.settle(app, pilot)
                visible_list()
                self.assertEqual(listing.highlighted_option.id, "frag-0")
            await pilot.press("enter")
            await self.settle(app, pilot)
            self.assertEqual(str(app.screen.body), body)


if __name__ == "__main__":
    unittest.main()
