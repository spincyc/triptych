"""Regression fixtures require prepared products and never discover old data."""

import os
from pathlib import Path
import sys
import tempfile
import unittest
from unittest import mock

sys.path.insert(0, str(Path(__file__).resolve().parent))
import _product_data as fixtures


class ProductDataFixtures(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        self.environment = mock.patch.dict(os.environ, {"TRIPTYCH_TEST_BROWSER_DATA_ROOT": ""})
        self.environment.start()
        self.addCleanup(self.environment.stop)

    def test_explicit_sparse_fixture_requires_no_descriptor_or_generation(self):
        data = self.root / "fixture"
        data.mkdir()
        (data / "held.json").write_text("{}\n")
        with mock.patch.dict(os.environ, {"TRIPTYCH_TEST_BROWSER_DATA_ROOT": "fixture"}):
            self.assertEqual(fixtures.browser_data_root(self.root), data)
            self.assertEqual(fixtures.data_path("missing.json", self.root), data / "missing.json")
        self.assertFalse((self.root / "release").exists())
        self.assertFalse((self.root / "build").exists())

    def test_legacy_tree_does_not_substitute_for_missing_descriptor(self):
        (self.root / "src/web/data").mkdir(parents=True)
        with self.assertRaisesRegex(RuntimeError, "tools/browser-products build"):
            fixtures.browser_data_root(self.root)
        self.assertFalse((self.root / "build").exists())

    def test_missing_explicit_fixture_fails_with_preparation_instruction(self):
        with mock.patch.dict(os.environ, {"TRIPTYCH_TEST_BROWSER_DATA_ROOT": "absent"}):
            with self.assertRaisesRegex(RuntimeError, "browser test data is absent.*tools/browser-products build"):
                fixtures.browser_data_root(self.root)

    def test_product_paths_cannot_escape_the_selected_fixture(self):
        for relative in ("../outside.json", "/outside.json"):
            with self.subTest(relative=relative), self.assertRaises(ValueError):
                fixtures.data_path(relative, self.root)


if __name__ == "__main__":
    unittest.main()
