"""The terminal manifest consumer reads only a held verified Bible product."""
from contextlib import contextmanager
import importlib.machinery
import importlib.util
import json
from pathlib import Path
import sys
import tempfile
from types import SimpleNamespace
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))
loader = importlib.machinery.SourceFileLoader("mass_today_products", str(ROOT / "tools/mass-today"))
spec = importlib.util.spec_from_loader(loader.name, loader)
today = importlib.util.module_from_spec(spec)
loader.exec_module(today)


class BibleManifestProducts(unittest.TestCase):
    def setUp(self):
        scratch = ROOT / ".scratch/next-product-consumers"
        scratch.mkdir(parents=True, exist_ok=True)
        self.temporary = tempfile.TemporaryDirectory(dir=scratch)
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.data = self.root / "verified"
        self.data.mkdir()
        self.active = False

    @contextmanager
    def products(self, root, *, product_ids):
        self.assertEqual(root, self.root)
        self.assertEqual(product_ids, ["bibles"])
        self.active = True
        try:
            yield SimpleNamespace(data_root=self.data)
        finally:
            self.active = False

    def test_verified_manifest_controls_language_and_named_selection(self):
        rows = [{"id": "latin", "language": "la"}, {"id": "english", "language": "en"}]
        (self.data / "bibles.json").write_text(json.dumps({"bibles": rows}))
        legacy = self.root / "src/web/data"
        legacy.mkdir(parents=True)
        (legacy / "bibles.json").write_text('{"bibles":[{"id":"unverified","language":"en"}]}')
        read_text = Path.read_text

        def read(path, *args, **kwargs):
            if path == self.data / "bibles.json":
                self.assertTrue(self.active)
            return read_text(path, *args, **kwargs)

        with (patch.object(today, "ROOT", self.root),
              patch.object(today, "verified_products", self.products),
              patch.object(Path, "read_text", read)):
            self.assertEqual(today.indexed_bibles(), rows)
            self.assertEqual(today.default_bible("en"), rows[1])
            self.assertEqual(today.indexed_bible("latin"), rows[0])
        self.assertFalse(self.active)

    def test_missing_or_invalid_manifest_is_refused_instead_of_empty(self):
        for body in (None, "{", "{}", '{"bibles":null}'):
            with self.subTest(body=body):
                target = self.data / "bibles.json"
                if body is None:
                    target.unlink(missing_ok=True)
                else:
                    target.write_text(body)
                with (patch.object(today, "ROOT", self.root),
                      patch.object(today, "verified_products", self.products),
                      self.assertRaisesRegex(today.Refused, "published browser data is unavailable")):
                    today.indexed_bibles()
                self.assertFalse(self.active)

    def test_failed_verification_never_returns_a_smaller_library(self):
        with (patch.object(today, "verified_products", side_effect=today.ProductError("stale descriptor")),
              self.assertRaisesRegex(today.Refused, "stale descriptor")):
            today.indexed_bibles()


if __name__ == "__main__":
    unittest.main()
