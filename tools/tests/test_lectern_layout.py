"""Reading and navigation remain usable when the terminal changes size."""
from __future__ import annotations

import datetime as dt
import importlib.util
import shutil
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))

AVAILABLE = importlib.util.find_spec("textual") is not None and shutil.which("node")


@unittest.skipUnless(AVAILABLE, "Textual and node are required for actual reader layout")
class ReaderLayoutTests(unittest.IsolatedAsyncioTestCase):
    def app(self, surface="day", **intent):
        from lectern.app import TriptychApp

        return TriptychApp(start=surface, intent={"calendar": "roman-1962", **intent},
                           today=dt.date(2026, 5, 24))

    async def settle(self, app, pilot):
        from lectern.snapshot import _settle

        await _settle(app, pilot)

    async def test_small_day_swaps_panes_and_preserves_reading_position(self):
        from lectern.surface import shown

        app = self.app(date="2026-05-24")
        async with app.run_test(size=(80, 30)) as pilot:
            await self.settle(app, pilot)
            left, reading = app.query_one("#day-left"), app.query_one("#day-reading-a")
            self.assertFalse(shown(left))
            self.assertTrue(reading.has_focus)
            self.assertGreaterEqual(reading.region.width, 76)
            reading.scroll_relative(y=10, animate=False)
            await pilot.pause()
            position = reading.scroll_y
            self.assertGreater(position, 0)

            await pilot.press("f")
            await self.settle(app, pilot)
            self.assertTrue(shown(left))
            self.assertGreaterEqual(left.region.width, 76)
            self.assertFalse(shown(reading))
            self.assertIn(left, app.focused.ancestors)

            await pilot.press("f")
            await self.settle(app, pilot)
            self.assertTrue(reading.has_focus)
            self.assertEqual(reading.scroll_y, position)

    async def test_wide_day_and_resize_keep_focus_on_a_visible_pane(self):
        from lectern.surface import shown

        app = self.app(date="2026-05-24")
        async with app.run_test(size=(140, 42)) as pilot:
            await self.settle(app, pilot)
            left, reading = app.query_one("#day-left"), app.query_one("#day-reading-a")
            self.assertTrue(shown(left))
            self.assertLessEqual(app.query_one("#day-text-a").size.width, 78)
            await pilot.press("f")
            await self.settle(app, pilot)
            self.assertFalse(shown(left))
            self.assertTrue(reading.has_focus)
            await pilot.press("f")
            await self.settle(app, pilot)
            app.query_one("#day-missal-list").focus()
            await pilot.resize_terminal(80, 30)
            await self.settle(app, pilot)
            self.assertTrue(reading.has_focus)
            self.assertTrue(shown(app.focused))

    async def test_small_day_compare_stacks_matching_sides(self):
        app = self.app(date="2026-10-25")
        async with app.run_test(size=(80, 36)) as pilot:
            await self.settle(app, pilot)
            await pilot.press("v")
            await self.settle(app, pilot)
            pairs = [widget for widget in app.query("#day-compare-body Horizontal")
                     if len(widget.children) == 2]
            self.assertTrue(pairs)
            for pair in pairs:
                first, second = pair.children
                self.assertGreaterEqual(first.region.width, 65)
                self.assertGreaterEqual(second.region.y, first.region.bottom)

    async def test_small_propers_browses_then_shows_the_selected_text(self):
        from lectern.surface import shown

        app = self.app("propers")
        async with app.run_test(size=(80, 30)) as pilot:
            await self.settle(app, pilot)
            left, reading = app.query_one("#propers-left"), app.query_one("#propers-reading")
            self.assertTrue(shown(left))
            self.assertGreaterEqual(left.region.width, 76)
            self.assertFalse(shown(reading))
            listing = app.query_one("#propers-list")
            previous = listing.highlighted
            await pilot.press("down")
            self.assertNotEqual(listing.highlighted, previous)
            await pilot.press("enter")
            await self.settle(app, pilot)
            self.assertFalse(shown(left))
            self.assertTrue(reading.has_focus)
            self.assertIsNotNone(app.current().reading)
            await pilot.press("f")
            await self.settle(app, pilot)
            self.assertTrue(shown(left))
            self.assertTrue(app.query_one("#propers-list").has_focus)

    async def test_initial_catena_focus_opens_the_author_with_enter(self):
        from lectern.snapshot import _text

        app = self.app("catena", ref="Gen 1")
        async with app.run_test(size=(140, 42)) as pilot:
            await self.settle(app, pilot)
            self.assertEqual(app.focused.id, "catena-chain-list")
            await pilot.press("enter")
            await self.settle(app, pilot)
            self.assertIn("▾ Basil of Caesarea", _text(app, styles=False))
            listing = app.query_one("#catena-chain-list")
            await pilot.press("down")
            selected = listing.highlighted
            app.action_surface("day")
            await self.settle(app, pilot)
            app.action_surface("catena")
            await self.settle(app, pilot)
            self.assertEqual(listing.highlighted, selected)
            self.assertTrue(listing.has_focus)

    async def test_catalogues_keep_their_explicit_initial_focus(self):
        for surface in ("texts", "sources"):
            with self.subTest(surface=surface):
                app = self.app(surface)
                async with app.run_test(size=(140, 42)) as pilot:
                    await self.settle(app, pilot)
                    listing = app.query_one(f"#{surface}-list")
                    self.assertTrue(listing.has_focus)
                    before = listing.highlighted
                    await pilot.press("down")
                    await self.settle(app, pilot)
                    self.assertNotEqual(listing.highlighted, before)
                    self.assertTrue(listing.has_focus)
                    selected = listing.highlighted
                    app.action_surface("day")
                    await self.settle(app, pilot)
                    app.action_surface(surface)
                    await self.settle(app, pilot)
                    self.assertTrue(listing.has_focus)
                    self.assertEqual(listing.highlighted, selected)

    async def test_section_and_command_bars_fit_at_supported_widths(self):
        from lectern.app import ReaderFooter, TopBar

        app = self.app(date="2026-05-24")
        async with app.run_test(size=(120, 40)) as pilot:
            await self.settle(app, pilot)
            for width in (120, 80, 60):
                with self.subTest(width=width):
                    await pilot.resize_terminal(width, 30)
                    await self.settle(app, pilot)
                    for line in app.query_one(TopBar).render().split("\n"):
                        self.assertLessEqual(line.cell_len, width - 2)
                    footer = app.query_one(ReaderFooter)
                    commands = [child for child in footer.children if hasattr(child, "action")]
                    self.assertIn("help", [child.action for child in commands])
                    self.assertIn("focus_reading", [child.action for child in commands])
                    for child in commands:
                        self.assertGreaterEqual(child.region.x, 0)
                        self.assertLessEqual(child.region.right, width)

    async def test_reading_dialog_advertises_only_its_available_default_actions(self):
        from textual.containers import VerticalScroll
        from lectern.dialogs import Reading

        app = self.app(date="2026-05-24")
        async with app.run_test(size=(80, 30)) as pilot:
            await self.settle(app, pilot)
            for walks, supplied, expected in (
                (False, "", "esc close"),
                (True, "", "esc close · n next · p previous"),
                (False, "Source account · esc close", "Source account · esc close"),
            ):
                with self.subTest(walks=walks, subtitle=supplied):
                    result = []
                    dialog = Reading("Study", "Held source context", supplied, walks=walks)
                    app.push_screen(dialog, result.append)
                    await pilot.pause()
                    self.assertEqual(dialog.query_one(VerticalScroll).border_subtitle, expected)
                    await pilot.press("n")
                    await pilot.pause()
                    if walks:
                        self.assertEqual(result, ["next"])
                    else:
                        self.assertIs(app.screen, dialog)
                        await pilot.press("escape")
                        await pilot.pause()

    async def test_search_reveals_hidden_catalogue_before_typing(self):
        from lectern.surface import shown

        for surface, term in (("sources", "alcuin"), ("texts", "origen")):
            for width in (80, 140):
                with self.subTest(surface=surface, width=width):
                    app = self.app(surface)
                    async with app.run_test(size=(width, 30)) as pilot:
                        await self.settle(app, pilot)
                        owner = app.current()
                        left = owner.query_one(f"#{surface}-left")
                        before = len(owner.found["rows"])
                        await pilot.press("f")
                        await self.settle(app, pilot)
                        self.assertFalse(shown(left))
                        await pilot.press("slash")
                        await self.settle(app, pilot)
                        query = owner.query_one(f"#{surface}-query")
                        self.assertTrue(shown(query))
                        self.assertTrue(query.has_focus)
                        self.assertGreater(query.region.intersection(app.screen.region).area, 0)
                        await pilot.press(*term)
                        await self.settle(app, pilot)
                        self.assertEqual(query.value, term)
                        self.assertEqual(owner.found["state"]["find"], term)
                        self.assertTrue(owner.found["rows"])
                        self.assertLess(len(owner.found["rows"]), before)

    async def test_sources_back_reveals_hidden_catalogue_before_list_navigation(self):
        from lectern.surface import shown

        edition = "edition.alcuin-of-york.interrogationes-et-responsiones-in-genesim.latin-migne-pl-100"
        for width in (80, 140):
            with self.subTest(width=width):
                app = self.app("sources", edition=edition)
                async with app.run_test(size=(width, 30)) as pilot:
                    await self.settle(app, pilot)
                    owner = app.current()
                    self.assertIsNotNone(owner.open_edition)
                    self.assertNotIn("problem", owner.open_edition)
                    await pilot.press("f")
                    await self.settle(app, pilot)
                    self.assertFalse(shown(owner.query_one("#sources-left")))
                    await pilot.press("b")
                    await self.settle(app, pilot)
                    listing = owner.query_one("#sources-list")
                    self.assertIsNone(owner.open_edition)
                    self.assertTrue(shown(listing))
                    self.assertTrue(listing.has_focus)
                    self.assertGreater(listing.region.intersection(app.screen.region).area, 0)
                    before = listing.highlighted
                    await pilot.press("down")
                    await self.settle(app, pilot)
                    self.assertNotEqual(listing.highlighted, before)


if __name__ == "__main__":
    unittest.main()
