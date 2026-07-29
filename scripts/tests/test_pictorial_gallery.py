from __future__ import annotations

import hashlib
import importlib.machinery
import importlib.util
from pathlib import Path
import tempfile
import unittest
from unittest import mock


REPOSITORY_ROOT = Path(__file__).resolve().parents[2]
TOOL_PATH = REPOSITORY_ROOT / "scripts/public-alpha"


def load_tool():
    loader = importlib.machinery.SourceFileLoader(
        "test_pictorial_gallery_tool", str(TOOL_PATH)
    )
    spec = importlib.util.spec_from_loader(loader.name, loader)
    if spec is None:
        raise RuntimeError("could not load scripts/public-alpha")
    module = importlib.util.module_from_spec(spec)
    loader.exec_module(module)
    return module


class PictorialGalleryTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.tool = load_tool()
        cls.cards = cls.tool.pictorial_gallery_data()

    def test_release_ready_union_is_exactly_deduplicated(self) -> None:
        self.assertEqual(len(self.cards), 100)
        self.assertEqual(len({card["source_relative"] for card in self.cards}), 100)
        self.assertEqual(len({card["destination"] for card in self.cards}), 100)
        self.assertEqual(
            sum(len(card["artwork_ids"]) for card in self.cards),
            105,
            "full and compact records should merge five duplicate identities",
        )

    def test_every_card_has_checked_definition_and_accessible_image_data(self) -> None:
        for card in self.cards:
            self.assertGreater(card["width"], 0)
            self.assertGreater(card["height"], 0)
            self.assertRegex(card["sha256"], r"^[0-9a-f]{64}$")
            self.assertTrue(card["definitions"])
            for definition in card["definitions"]:
                self.assertTrue(definition["name"].strip())
                self.assertTrue(definition["definition"].strip())
        under_audit = [
            definition
            for card in self.cards
            for definition in card["definitions"]
            if definition["under_audit"]
        ]
        self.assertTrue(under_audit)
        self.assertTrue(
            all(
                definition["definition"]
                == self.tool.PICTORIAL_UNAVAILABLE_DEFINITION
                for definition in under_audit
            )
        )

    def test_admitted_assets_are_exact_bytes_and_bound_site_sources(self) -> None:
        bound = self.tool.pictorial_gallery_source_paths()
        for card in self.cards:
            data = card["source"].read_bytes()
            self.assertEqual(hashlib.sha256(data).hexdigest(), card["sha256"])
            self.assertEqual(len(data), card["source"].stat().st_size)
            self.assertIn(card["source_relative"], bound)
        self.assertIn(
            self.tool.PICTORIAL_MANIFEST_RELATIVE.as_posix(),
            bound,
        )
        self.assertTrue(self.tool.pictorial_object_source_paths() <= bound)

    def test_expected_artifact_is_exhaustive_for_gallery_pngs(self) -> None:
        expected = self.tool.expected_artifact_files({}, {}, False, {})
        expected_pngs = {
            path
            for path in expected
            if path.startswith(self.tool.PICTORIAL_GALLERY_ASSET_ROOT.as_posix() + "/")
        }
        self.assertEqual(
            expected_pngs,
            {card["destination"] for card in self.cards},
        )
        self.assertEqual(len(expected_pngs), 100)
        self.assertIn(self.tool.PICTORIAL_GALLERY_OUTPUT, expected)

    def test_tlm_shelf_gallery_link_resolves_to_generated_route(self) -> None:
        self.assertEqual(
            self.tool.source_to_output(
                "library/traditional-latin-mass.md",
                "library/traditional-latin-mass.html",
                "sanctuary-picture-dictionary.html",
                set(),
            ),
            "sanctuary-picture-dictionary.html",
        )

    def test_gallery_markup_is_semantic_accessible_and_has_no_backlink(self) -> None:
        rendered = self.tool.render_pictorial_gallery(False, {})
        self.assertEqual(rendered.count('class="gallery-card"'), 100)
        self.assertEqual(rendered.count('loading="lazy"'), 100)
        self.assertEqual(rendered.count("<figure"), 100)
        self.assertEqual(rendered.count("<figcaption>"), 100)
        self.assertNotIn("Return to", rendered)
        self.assertIn("Definitions are drawn only from verified claims", rendered)
        self.assertIn('href="../license.html"', rendered)
        self.assertIn('href="../third-party.html"', rendered)
        self.assertIn("Each image follows its tracked artwork audit", rendered)
        self.assertIn("Public Domain Open Access image", rendered)
        self.assertIn("Public Domain Rijksmuseum image", rendered)

    def test_gallery_css_blends_image_boundaries_in_both_color_schemes(self) -> None:
        css = (
            REPOSITORY_ROOT / "release/public-alpha/assets/site.css"
        ).read_text(encoding="utf-8")
        self.assertIn("mix-blend-mode: multiply", css)
        self.assertIn("mix-blend-mode: screen", css)

    def test_asset_resolution_rejects_traversal_and_symlinks(self) -> None:
        with self.assertRaises(self.tool.ReleaseError):
            self.tool._resolve_pictorial_asset_path("../outside.png", "test asset")
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            dictionary = root / "dictionary"
            dictionary.mkdir()
            target = root / "target.png"
            target.write_bytes(b"png")
            (dictionary / "link.png").symlink_to(target)
            with (
                mock.patch.object(self.tool, "ROOT", root),
                mock.patch.object(self.tool, "PICTORIAL_ROOT", dictionary),
            ):
                with self.assertRaises(self.tool.ReleaseError):
                    self.tool._resolve_pictorial_asset_path("link.png", "test asset")


if __name__ == "__main__":
    unittest.main()
