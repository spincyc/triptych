"""Ordinary reading validates a thin index without preparing all products."""
from __future__ import annotations

import io
import unittest
from unittest.mock import patch

from test_lectern import TEXTUAL, _lectern_tool
import _browser_products as products
from lectern.repo import Refused


class LecternPreparationTests(unittest.TestCase):
    def setUp(self):
        self.tool = _lectern_tool()
        self.stdout, self.stderr = io.StringIO(), io.StringIO()
        self.enterContext(patch("sys.stdout", self.stdout))
        self.enterContext(patch("sys.stderr", self.stderr))

    def test_first_and_warm_launch_check_index_without_product_generation(self):
        with (patch("_corpus_index.CorpusIndex") as index,
              patch.object(products, "check") as check,
              patch.object(products, "build") as build):
            self.tool._prepare_products()
            self.tool._prepare_products()
        self.assertEqual(index.call_count, 2)
        check.assert_not_called()
        build.assert_not_called()
        self.assertEqual(self.stdout.getvalue(), "")
        self.assertIn("checking the corpus index", self.stderr.getvalue())

    def test_stale_index_refuses_without_rewriting_or_rebuilding(self):
        from _corpus_index import CorpusIndexError
        with (patch("_corpus_index.CorpusIndex", side_effect=CorpusIndexError("stale corpus index")),
              patch.object(products, "build") as build,
              self.assertRaisesRegex(Refused, "indexed reading data is unavailable: stale corpus index")):
            self.tool._prepare_products()
        build.assert_not_called()

    def test_converter_is_not_needed_to_open_a_nonpublication_reading(self):
        with (patch("_corpus_index.CorpusIndex"),
              patch("_markdown_render.require_locked_markdown_dependency") as converter):
            self.tool._prepare_products()
        converter.assert_not_called()


@unittest.skipUnless(TEXTUAL, "Textual is required for reader entry points")
class LecternStartupTests(unittest.TestCase):
    def test_index_cli_refusal_is_concise_and_does_not_build(self):
        from _corpus_index import CorpusIndexError
        tool = _lectern_tool()
        with (patch("_corpus_index.CorpusIndex", side_effect=CorpusIndexError("stale corpus index")),
              patch.object(products, "build") as build,
              patch("sys.stdout", new_callable=io.StringIO) as out,
              patch("sys.stderr", new_callable=io.StringIO) as err):
            self.assertEqual(tool.main(["snapshot", "--surface", "day"]), 2)
        build.assert_not_called()
        self.assertEqual(out.getvalue(), "")
        self.assertIn("stale corpus index", err.getvalue())
        self.assertNotIn("Traceback", err.getvalue())

    def test_open_defers_preparation_to_loading_screen_but_snapshot_prepares_first(self):
        from lectern import bridge, preparation, snapshot
        from lectern.app import TriptychApp

        for arguments in ([], ["open"], ["snapshot"]):
            with self.subTest(arguments=arguments):
                tool = _lectern_tool()
                events = []

                def run(app):
                    self.assertIs(app.prepare, preparation.prepare_products)
                    events.append("open")

                with (patch.object(tool, "_prepare_products", side_effect=lambda: events.append("prepare")),
                      patch.object(TriptychApp, "run", run),
                      patch.object(snapshot, "render", side_effect=lambda **kwargs: events.append("snapshot") or "screen\n"),
                      patch.object(bridge.BRIDGE_PROCESS, "close"),
                      patch("sys.stdout", new_callable=io.StringIO) as out,
                      patch.object(out, "isatty", return_value=True)):
                    self.assertEqual(tool.main(arguments), 0)
                self.assertEqual(events, ["prepare", "snapshot"] if arguments == ["snapshot"] else ["open"])

    def test_failed_preparation_keeps_the_cli_error_contract(self):
        from lectern import snapshot
        from lectern.app import TriptychApp

        for arguments in (["open"], ["snapshot"]):
            with self.subTest(arguments=arguments):
                tool = _lectern_tool()

                def run(app):
                    try:
                        tool._prepare_products(announce=False)
                    except Refused as error:
                        app.startup_error = error

                from _corpus_index import CorpusIndexError
                with (patch("_corpus_index.CorpusIndex", side_effect=CorpusIndexError("controlled corruption")),
                      patch("_markdown_render.require_locked_markdown_dependency"),
                      patch.object(TriptychApp, "run", run),
                      patch.object(snapshot, "render") as rendered,
                      patch("sys.stdout", new_callable=io.StringIO) as out,
                      patch("sys.stderr", new_callable=io.StringIO) as err,
                      patch.object(out, "isatty", return_value=True)):
                    self.assertEqual(tool.main(arguments), 2)
                rendered.assert_not_called()
                self.assertEqual(out.getvalue(), "")
                self.assertIn("indexed reading data is unavailable: controlled corruption", err.getvalue())


if __name__ == "__main__":
    unittest.main()
