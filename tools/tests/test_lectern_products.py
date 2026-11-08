"""Lectern prepares exact cache misses before starting its reading session."""
from __future__ import annotations

import io
import os
import shutil
import unittest
from unittest.mock import patch

import test_browser_products as store_tests
from test_lectern import TEXTUAL, _lectern_tool
import _browser_products as products
from lectern.repo import Refused


class LecternPreparationTests(unittest.TestCase):
    def setUp(self):
        # Reuse the store's two-family fixture, including its real descriptor,
        # filesystem checks and offline generation; only the producer is tiny.
        fixture = store_tests.BrowserProductsTests()
        self.addCleanup(fixture.doCleanups)
        fixture.setUp()
        self.fixture = fixture
        self.tool = _lectern_tool()
        self.enterContext(patch.object(self.tool, "ROOT", fixture.root))
        self.enterContext(patch.dict(os.environ, {"TRIPTYCH_BROWSER_DATA_ROOT": str(fixture.cache)}))
        self.stdout, self.stderr = io.StringIO(), io.StringIO()
        self.enterContext(patch("sys.stdout", self.stdout))
        self.enterContext(patch("sys.stderr", self.stderr))

    def test_first_run_rebuilds_exact_missing_products_and_warm_run_reuses(self):
        fixture = self.fixture
        descriptor = (fixture.root / products.MANIFEST_RELATIVE).read_bytes()
        shutil.rmtree(fixture.cache)
        self.tool._prepare_products()
        self.assertEqual(fixture.generated, [("a", "b")])
        with products.verified_products(fixture.root) as held:
            self.assertEqual(held.files["structure/a/index.json"].read_bytes(), fixture.payload().read_bytes())
        with patch.object(products, "build", wraps=products.build) as build:
            self.tool._prepare_products()
        build.assert_not_called()
        self.assertEqual(fixture.generated, [("a", "b")])
        self.assertEqual((fixture.root / products.MANIFEST_RELATIVE).read_bytes(), descriptor)
        self.assertEqual(self.stdout.getvalue(), "")
        self.assertIn("first build may take several minutes", self.stderr.getvalue())

    def test_warm_preparation_can_share_an_existing_reader_lock(self):
        with products.verified_products(self.fixture.root):
            self.tool._prepare_products()
        self.assertEqual(self.fixture.generated, [])

    def test_corrupt_cache_is_refused_without_rebuild(self):
        self.fixture.payload().write_text("corrupt")
        with self.assertRaisesRegex(Refused, "could not be prepared.*differ"):
            self.tool._prepare_products()
        self.assertEqual(self.fixture.generated, [])
        self.assertEqual(self.fixture.payload().read_text(), "corrupt")

    def test_unsafe_cache_is_refused_without_rebuild(self):
        fixture = self.fixture
        payload = fixture.payload()
        payload.unlink()
        payload.symlink_to(fixture.root / "src/a/input.txt")
        with self.assertRaisesRegex(Refused, "could not be prepared.*unsafe"):
            self.tool._prepare_products()
        self.assertEqual(fixture.generated, [])
        self.assertTrue(payload.is_symlink())

    def test_stale_descriptor_is_refused_without_recording_or_rebuilding(self):
        fixture = self.fixture
        descriptor = (fixture.root / products.MANIFEST_RELATIVE).read_bytes()
        (fixture.root / "src/a/input.txt").write_text("changed")
        with self.assertRaisesRegex(Refused, "could not be prepared.*inputs changed"):
            self.tool._prepare_products()
        self.assertEqual(fixture.generated, [])
        self.assertEqual((fixture.root / products.MANIFEST_RELATIVE).read_bytes(), descriptor)

    def test_wrong_rebuild_does_not_replace_committed_expectations(self):
        fixture = self.fixture
        descriptor = (fixture.root / products.MANIFEST_RELATIVE).read_bytes()
        shutil.rmtree(fixture.cache)
        with (patch.object(products, "_generate", side_effect=lambda root, out, ids: fixture.generate_bad(out)),
              self.assertRaisesRegex(Refused, "could not be prepared.*differ")):
            self.tool._prepare_products()
        self.assertEqual((fixture.root / products.MANIFEST_RELATIVE).read_bytes(), descriptor)


@unittest.skipUnless(TEXTUAL, "Textual is required for reader entry points")
class LecternStartupTests(unittest.TestCase):
    def test_both_verbs_prepare_before_starting_the_reader(self):
        from lectern import bridge, snapshot
        from lectern.app import TriptychApp

        for arguments in ([], ["open"], ["snapshot"]):
            with self.subTest(arguments=arguments):
                tool = _lectern_tool()
                events = []
                with (patch.object(tool, "_prepare_products", side_effect=lambda: events.append("prepare")),
                      patch.object(TriptychApp, "run", side_effect=lambda: events.append("open")),
                      patch.object(snapshot, "render", side_effect=lambda **kwargs: events.append("snapshot") or "screen\n"),
                      patch.object(bridge.BRIDGE_PROCESS, "close"),
                      patch("sys.stdout", new_callable=io.StringIO) as out,
                      patch.object(out, "isatty", return_value=True)):
                    self.assertEqual(tool.main(arguments), 0)
                self.assertEqual(events, ["prepare", "snapshot" if arguments == ["snapshot"] else "open"])

    def test_failed_preparation_returns_a_cli_error_before_rendering(self):
        from lectern import snapshot
        from lectern.app import TriptychApp

        for arguments in (["open"], ["snapshot"]):
            with self.subTest(arguments=arguments):
                tool = _lectern_tool()
                with (patch.object(products, "check", side_effect=products.ProductError("controlled corruption")),
                      patch.object(products, "build", side_effect=products.ProductError("controlled corruption")),
                      patch.object(TriptychApp, "run") as opened,
                      patch.object(snapshot, "render") as rendered,
                      patch("sys.stdout", new_callable=io.StringIO) as out,
                      patch("sys.stderr", new_callable=io.StringIO) as err,
                      patch.object(out, "isatty", return_value=True)):
                    self.assertEqual(tool.main(arguments), 2)
                opened.assert_not_called()
                rendered.assert_not_called()
                self.assertEqual(out.getvalue(), "")
                self.assertIn("published browser data could not be prepared: controlled corruption", err.getvalue())


if __name__ == "__main__":
    unittest.main()
