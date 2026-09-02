#!/usr/bin/env python3
"""Publication-local bindings for the Immaculate Heart notification."""

from __future__ import annotations

import importlib.machinery
import importlib.util
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
DOCUMENT = (
    "liturgy/roman-rite/postconciliar/"
    "roman-missal-third-edition-en-us-2011/reference/liturgical-calendar"
)
HTML_PASSAGE_ID = (
    "passage.congregation-for-divine-worship-and-the-discipline-of-the-sacraments."
    "notificatio-de-occurrentia-memoriae-immaculati-cordis-1998."
    "latin-vatican-web-2026-08-26.operative-occurrence-rule"
)
NOTITIAE_PASSAGE_ID = (
    "passage.congregation-for-divine-worship-and-the-discipline-of-the-sacraments."
    "notificatio-de-occurrentia-memoriae-immaculati-cordis-1998."
    "latin-notitiae-392-393.operative-occurrence-rule"
)
SOURCE_IDS = {HTML_PASSAGE_ID, NOTITIAE_PASSAGE_ID}
BINDING_PATHS = {
    ROOT / "src" / provider / DOCUMENT / "research/source-bindings.toml"
    for provider in ("gpt", "claude")
}


def load_source_library():
    path = ROOT / "tools/source-library"
    loader = importlib.machinery.SourceFileLoader(
        "_postconciliar_notification_source_library", str(path)
    )
    spec = importlib.util.spec_from_loader(loader.name, loader)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


SOURCE_LIBRARY = load_source_library()


class PostconciliarNotificationBindingTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.library = SOURCE_LIBRARY.load_library(ROOT)
        if cls.library.errors:
            raise AssertionError("; ".join(cls.library.errors))

    def test_each_provider_publication_binds_both_exact_passages(self) -> None:
        bindings_by_path = {
            path: {
                binding.source_id: binding
                for binding in self.library.bindings
                if binding.path == path and binding.source_id in SOURCE_IDS
            }
            for path in BINDING_PATHS
        }
        for path, bindings in bindings_by_path.items():
            with self.subTest(path=path):
                self.assertTrue(path.is_file())
                self.assertEqual(set(bindings), SOURCE_IDS)
                for source_id, binding in bindings.items():
                    self.assertEqual(binding.schema, 2)
                    self.assertEqual(binding.document, DOCUMENT)
                    self.assertIn("verified", binding.data["states"])
                    self.assertEqual(binding.data["verified_on"], "2026-08-26")
                    self.assertEqual(
                        binding.data["source_fingerprint"],
                        SOURCE_LIBRARY.source_fingerprint(self.library, source_id),
                    )


if __name__ == "__main__":
    unittest.main()
