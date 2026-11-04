from __future__ import annotations

from contextlib import contextmanager
import json
from pathlib import Path
import shutil
import sys
import tempfile
from types import SimpleNamespace
import unittest
from unittest import mock

try:
    from . import test_public_alpha_source_first as source_fixtures
except ImportError:
    import test_public_alpha_source_first as source_fixtures


class ProductError(ValueError):
    pass


class PublicAlphaBrowserProductsTest(unittest.TestCase):
    """Test publisher boundaries against the verified-products protocol.

    Cache-key construction, offline regeneration and safe cache installation
    belong to the product store's tests. This fixture supplies its promised
    private immutable snapshot, including fresh contexts for build and verify.
    """

    def setUp(self):
        self.base = source_fixtures.PublicAlphaSourceFirstTest(methodName="runTest")
        self.base.setUp()
        self.addCleanup(self.base.doCleanups)
        self.fixture = self.base.fixture
        self.root, self.tool = self.fixture.root, self.fixture.tool
        self.manifest = self.fixture.manifest
        self.seed = self.root / ".scratch/browser-products/seed"
        self.seed.mkdir(parents=True)
        self.write_product("bibles.json", {"bibles": [{
            "id": "offered", "label": "Offered", "language": "la",
            "numbering": "vulgate", "psalter": "gallican",
            "rights": "public-domain",
        }]})
        self.write_product("structure/sources/index.json", {"works": []})
        self.fixture.write("src/sources/bibles/offered/chapters/Ps/1.json", b"{}\n")
        self.fixture.write("src/web/browser/shared/browser-core.js", b"// shared fixture\n")
        self.fixture.write("src/web/browser/shared/fixture.css", b"body {}\n")
        for entrance in self.tool.WEB_BROWSER_ENTRANCES:
            self.fixture.write(f"src/web/browser/{entrance}/index.html", (
                f'<html><head><title>{entrance} reader</title>'
                '<link rel="stylesheet" href="../shared/fixture.css"></head>'
                '<body><main>Reader fixture</main>'
                '<script src="../shared/browser-core.js"></script></body></html>\n'
            ).encode())
        for relative in ("release/browser-products.json", "scripts/_browser_products.py",
                         "scripts/_browser_product_recipes.py"):
            self.fixture.write(relative, b"fixture product contract\n")
        self.fixture.write_json("release/browser-products.json", {"products": []})
        self.bindings = {"release/browser-products.json", "scripts/_browser_products.py",
                         "scripts/_browser_product_recipes.py"}
        self.held = None
        self.failure = None
        self.snapshots = []
        self.prepared = []
        self.delivery = {}

        @contextmanager
        def verified_products(root, cache_root=None):
            self.assertEqual(root, self.root)
            if self.failure:
                raise ProductError(self.failure)
            if self.held is not None:
                yield self.held
                return
            with tempfile.TemporaryDirectory(dir=self.seed.parent) as temporary:
                data_root = Path(temporary) / "data"
                shutil.copytree(self.seed, data_root)
                self.snapshots.append(data_root)
                product = SimpleNamespace(
                    data_root=data_root,
                    files={p.relative_to(data_root).as_posix(): p for p in data_root.rglob("*.json")},
                    delivery_by_path={p.relative_to(data_root).as_posix(): self.delivery.get(p.relative_to(data_root).as_posix(), "browser-data")
                                      for p in data_root.rglob("*.json")},
                    source_paths=set(self.bindings),
                    projected_source_paths=set(),
                    products_identity="a" * 64,
                )
                self.held = product
                try:
                    yield product
                finally:
                    self.held = None

        def require_products(root):
            if self.held is None:
                raise ProductError("verified products require a held context")
            return self.held

        module = SimpleNamespace(ProductError=ProductError,
                                 verified_products=verified_products,
                                 require_products=require_products,
                                 build=lambda root: self.prepared.append(root))
        self.modules = mock.patch.dict(sys.modules, {"_browser_products": module})
        self.modules.start()
        self.addCleanup(self.modules.stop)
        self.pages = mock.patch("_print_catalog.source_pages", return_value={})
        self.source_pages = self.pages.start()
        self.addCleanup(self.pages.stop)

    def write_product(self, relative, value):
        path = self.seed / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(value, sort_keys=True) + "\n")

    def build(self):
        self.fixture.authorize_current_inputs()
        publications = self.tool.validate_manifest(self.manifest)
        output = self.tool.build_site(self.manifest, publications, False)
        return publications, output

    def test_build_and_independent_verify_use_products_without_tracked_data(self):
        self.assertFalse((self.root / "src/web/data").exists())
        publications, output = self.build()
        count_after_build = len(self.snapshots)
        self.assertEqual(self.prepared, [self.root])
        self.tool.verify_output(self.manifest, publications, output, False)
        self.assertGreater(len(self.snapshots), count_after_build)
        self.assertEqual(self.prepared, [self.root], "independent verify generated products")
        self.assertTrue((output / "browse/bibles.json").is_file())
        self.assertTrue((output / "browse/structure/sources/index.json").is_file())
        self.assertTrue((output / "sources/index.html").is_file())
        recorded = self.manifest["authorizations"]["test-authorization"]["site_sources"]
        self.assertTrue(self.bindings <= recorded.keys())
        self.assertFalse(any(path.startswith((".scratch/", "build/", "src/web/data/"))
                             for path in recorded))
        artifact = json.loads((output / "PUBLICATION-MANIFEST.json").read_text())
        self.assertEqual(artifact["browser_products"], {
            "manifest": "release/browser-products.json", "identity": "a" * 64,
            "editorial_approval": False,
        })

    def test_rewriting_artifact_checksums_cannot_hide_changed_product_bytes(self):
        publications, output = self.build()
        (output / "browse/structure/sources/index.json").write_text('{"works":["tampered"]}\n')
        self.tool.write_checksums(output)
        with self.assertRaisesRegex(self.tool.ReleaseError, "copied browser/data file does not match"):
            self.tool.verify_output(self.manifest, publications, output, False)

    def test_product_without_public_data_delivery_is_refused(self):
        relative = "unusual/private-preparation.json"
        self.write_product(relative, {"html": "Private preparation serialization"})
        self.delivery[relative] = "print-preparation"
        with self.assertRaisesRegex(self.tool.ReleaseError, "unknown delivery ownership"):
            self.build()

    def test_product_failure_is_checked_again_by_direct_independent_verify(self):
        publications, output = self.build()
        self.failure = "cache output hash changed"
        with self.assertRaisesRegex(self.tool.ReleaseError, "cache output hash changed"):
            self.tool.verify_output(self.manifest, publications, output, False)

    def test_restricted_payload_in_product_snapshot_is_independently_refused(self):
        self.write_product("structure/ordinary/roman-1962.json", {
            "ordinary": [{"text": "A permission-scoped text", "rights": "permission"}],
        })
        with self.assertRaisesRegex(self.tool.ReleaseError, "permission-scoped rights"):
            with self.tool.held_repository_inputs():
                self.tool.web_data_files()

    def test_unoffered_edition_in_products_is_refused(self):
        self.write_product("unoffered/chapters/Ps/1.json", {})
        with self.assertRaisesRegex(self.tool.ReleaseError, "editions absent from bibles.json"):
            with self.tool.held_repository_inputs():
                self.tool.web_data_files()

    def test_missing_declared_catalogues_cannot_mean_empty_browser(self):
        (self.seed / "bibles.json").unlink()
        with self.assertRaisesRegex(self.tool.ReleaseError, "missing bibles.json"):
            with self.tool.held_repository_inputs():
                self.tool.web_browser_pages()
        self.write_product("bibles.json", {"bibles": []})
        with self.assertRaisesRegex(self.tool.ReleaseError, "missing encyclicals/index.json"):
            with self.tool.held_repository_inputs():
                self.tool.encyclicals_catalogue_path()

    def test_source_reader_receives_verified_root_and_canonical_declaration(self):
        self.fixture.write("src/sources/fixture/text.txt", b"Complete lawful source text.\n")
        self.source_pages.return_value = {"papal-documents/fixture.html": {
            "title": "Fixture", "html": "<h1>Fixture</h1><p>Complete lawful source text.</p>",
            "source_paths": ["release/browser-products.json", "src/sources/fixture/text.txt"],
        }}
        with self.tool.held_repository_inputs():
            pages = self.tool.source_print_pages()
            self.assertIn("papal-documents/fixture.html", pages)
            self.source_pages.assert_called_once_with(
                self.root, data_root=self.held.data_root,
                data_source_paths=["release/browser-products.json"],
            )

    def test_product_cache_paths_cannot_enter_canonical_input_closure(self):
        self.bindings.add(".scratch/browser-products/seed/bibles.json")
        with self.assertRaisesRegex(self.tool.ReleaseError, "not a canonical input"):
            self.tool.site_source_paths(self.manifest)


if __name__ == "__main__":
    unittest.main()
