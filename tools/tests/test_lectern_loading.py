"""Startup reveals a complete reading after one index check."""
from __future__ import annotations

import asyncio
import threading
import unittest
from unittest.mock import patch

from test_lectern import ROOT, TEXTUAL
from lectern import preparation
from lectern.repo import Refused


async def until(predicate):
    async with asyncio.timeout(10):
        while not predicate():
            await asyncio.sleep(0.02)


@unittest.skipUnless(TEXTUAL, "Textual is required for the loading screen")
class LoadingTests(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        from textual import work
        from textual.widgets import Button
        from lectern.app import TriptychApp
        from lectern.surface import Surface

        self.opened, self.reading = threading.Event(), threading.Event()
        self.addCleanup(self.opened.set)
        self.addCleanup(self.reading.set)
        owner = self

        class Day(Surface):
            label, key, FIRST = "Day", "1", "#ready"

            def build(self):
                self.mount(Button("Unfinished reading", id="ready"))
                self.opening()

            @work(thread=True)
            def opening(self):
                owner.opened.wait(10)
                self.deliver(self.load)

            @work(thread=True)
            def load(self):
                owner.reading.wait(10)
                self.deliver(self.show)

            def show(self):
                self.query_one(Button).label = "Complete reading"

        self.enterContext(patch("lectern.app.surfaces", return_value=[Day]))
        self.enterContext(patch("lectern.app.bridge.BRIDGE_PROCESS.close"))
        self.App = TriptychApp

    async def test_loader_covers_preparation_and_chained_load_then_restores_focus(self):
        from lectern.snapshot import _text, _settle

        for size in ((60, 16), (120, 36)):
            with self.subTest(size=size):
                self.opened.clear()
                self.reading.clear()
                prepared = asyncio.Event()
                app = self.App(prepare=prepared.wait)
                async with app.run_test(size=size) as pilot:
                    await pilot.pause()
                    self.assertIn("Checking the corpus index", _text(app, styles=False))
                    self.assertNotIn("Unfinished reading", _text(app, styles=False))
                    self.assertIsNone(app.current())
                    await pilot.press("1", "2", "question_mark", "ctrl+p", "T", "tab")
                    self.assertEqual(len(app.screen_stack), 1)
                    self.assertEqual(app.theme, "triptych")
                    self.assertIsNone(app.current())
                    prepared.set()
                    await until(lambda: app.current() is not None)
                    await pilot.pause()
                    self.assertIn("Opening Day", _text(app, styles=False))
                    self.opened.set()
                    await until(lambda: any(w.name == "load" for w in app.workers))
                    await pilot.pause(0.25)
                    self.assertTrue(app.starting)
                    self.assertNotIn("Unfinished reading", _text(app, styles=False))
                    self.reading.set()
                    await _settle(app, pilot)
                    self.assertFalse(app.starting)
                    self.assertFalse(app.query_one("#loading").display)
                    self.assertIn("Complete reading", _text(app, styles=False))
                    self.assertNotIn("Opening Day", _text(app, styles=False))
                    self.assertEqual(app.focused.id, "ready")

    async def test_failure_keeps_reading_hidden_and_can_close(self):
        from lectern.snapshot import _text

        async def refuse():
            raise Refused("controlled corrupt cache")

        app = self.App(prepare=refuse)
        async with app.run_test() as pilot:
            await until(lambda: app.startup_error is not None)
            await pilot.pause()
            self.assertIn("controlled corrupt cache", _text(app, styles=False))
            self.assertIsNone(app.current())
            self.assertTrue(app.query_one("#reader").disabled)
            await pilot.press("q")
            self.assertTrue(app._quitting)

    async def test_cancel_waits_for_preparation_cleanup(self):
        for key in ("q", "ctrl+c"):
            with self.subTest(key=key):
                entered, cleaned = asyncio.Event(), asyncio.Event()

                async def prepare():
                    try:
                        entered.set()
                        await asyncio.Event().wait()
                    finally:
                        await asyncio.sleep(0.05)
                        cleaned.set()

                app = self.App(prepare=prepare)
                async with app.run_test() as pilot:
                    await entered.wait()
                    await pilot.press(key)
                    self.assertTrue(cleaned.is_set())
                    self.assertIsNone(app.current())

    async def test_long_refusal_can_scroll_without_losing_the_close_hint(self):
        from lectern.snapshot import _text

        async def refuse():
            raise Refused("Diagnostic context. " * 100 + "ACTIONABLE END")

        for size in ((60, 16), (80, 24)):
            with self.subTest(size=size):
                app = self.App(prepare=refuse)
                async with app.run_test(size=size) as pilot:
                    await until(lambda: app.startup_error is not None)
                    await pilot.pause()
                    self.assertIn("q / ctrl+c  close", _text(app, styles=False))
                    self.assertEqual(app.focused.id, "loading-detail-scroll")
                    await pilot.press("end")
                    await pilot.pause()
                    self.assertIn("ACTIONABLE END", _text(app, styles=False))
                    self.assertIn("q / ctrl+c  close", _text(app, styles=False))
                    self.assertTrue(app.query_one("#reader").disabled)
                    await pilot.press("q")

    async def test_snapshot_waits_for_the_initial_reading_and_omits_loader(self):
        from lectern.snapshot import capture

        self.opened.set()
        self.reading.set()
        drawing = await capture(surface="day", intent={}, size=(80, 24), keys=[],
                                form="text", theme="triptych")
        self.assertIn("Complete reading", drawing)
        self.assertNotIn("Loading the initial reading", drawing)

    async def test_surfaces_retain_their_explicit_initial_list_focus(self):
        from lectern.snapshot import _settle
        from lectern.surfaces.scripture import Scripture
        from lectern.surfaces.sources import Sources
        from lectern.surfaces.texts import Texts

        for kind, target in ((Texts, "texts-list"), (Sources, "sources-list"),
                             (Scripture, "scripture-reading-list")):
            with (self.subTest(surface=kind.label),
                  patch("lectern.app.surfaces", return_value=[kind]),
                  patch.object(kind, "start")):
                app = self.App(start=kind.surface_id())
                async with app.run_test() as pilot:
                    await _settle(app, pilot)
                    self.assertEqual(app.focused.id, target)


class PreparationTests(unittest.IsolatedAsyncioTestCase):
    async def test_one_check_off_the_event_loop_opens_the_reading_session(self):
        checked, threads = object(), []

        def index(root):
            threads.append(threading.current_thread())
            return checked

        with (patch("_corpus_index.CorpusIndex", side_effect=index) as constructed,
              patch("lectern.bridge.BRIDGE_PROCESS.adopt") as adopt):
            await preparation.prepare_products()
        self.assertEqual(constructed.call_count, 1)
        self.assertEqual(constructed.call_args.args, (ROOT,))
        self.assertIsNot(threads[0], threading.main_thread())
        adopt.assert_called_once_with(checked)

    async def test_refusal_keeps_its_wording_and_opens_nothing(self):
        from _corpus_index import CorpusIndexError

        with (patch("_corpus_index.CorpusIndex", side_effect=CorpusIndexError("stale corpus index")),
              patch("lectern.bridge.BRIDGE_PROCESS.adopt") as adopt,
              self.assertRaisesRegex(Refused, "indexed reading data is unavailable: stale corpus index")):
            await preparation.prepare_products()
        adopt.assert_not_called()


if __name__ == "__main__":
    unittest.main()
