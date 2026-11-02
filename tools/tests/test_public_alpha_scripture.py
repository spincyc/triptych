"""Public Catena Scripture dependencies follow the edition the reader selects."""

from __future__ import annotations

from contextlib import ExitStack
import hashlib
import importlib.machinery
import importlib.util
import json
import os
from pathlib import Path
import tempfile
import unittest
from unittest import mock

try:
    from .test_public_alpha_quarantine import install_test_quarantine
except ImportError:
    from test_public_alpha_quarantine import install_test_quarantine


REPOSITORY = Path(__file__).resolve().parents[2]


class PublicAlphaScriptureTest(unittest.TestCase):
    def setUp(self) -> None:
        scratch = Path(os.environ.get(
            "PUBLIC_ALPHA_SCRIPTURE_TEST_SCRATCH", ".scratch/tests/public-alpha-scripture"
        ))
        if not scratch.is_absolute():
            scratch = REPOSITORY / scratch
        scratch.mkdir(parents=True, exist_ok=True)
        temporary = tempfile.TemporaryDirectory(dir=scratch)
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        loader = importlib.machinery.SourceFileLoader(
            "test_public_alpha_scripture_tool", str(REPOSITORY / "tools/public-alpha")
        )
        spec = importlib.util.spec_from_loader(loader.name, loader)
        self.assertIsNotNone(spec)
        self.tool = importlib.util.module_from_spec(spec)
        loader.exec_module(self.tool)
        self.tool.ROOT = self.root
        self.quarantined = "PROJECT-CREATED QUARANTINED SCRIPTURE TEST PAYLOAD"
        install_test_quarantine(self.tool, self.root, self.quarantined)
        for directory in self.tool.WEB_BROWSER_DIRECTORIES:
            self.write(f"src/web/browser/{directory}/fixture.css", b"/* fixture */\n")
        self.write_json("src/web/data/bibles.json", {"bibles": [
            {"id": "king-james-version", "numbering": "hebrew",
             "loci": "hebrew-unnumbered-titles"},
            {"id": "vulgate", "numbering": "vulgate"},
        ]})
        self.prefix = "src/web/data/structure/catena/"
        self.write_json(self.prefix + "index.json", {
            "scripture": "structure/catena/scripture/", "canon": [],
        })
        self.daniel = {
            "schema": "triptych-catena-scripture/v1", "token": "Dan",
            "chapters": {"13": {
                "token": "Dan", "numbering": "vulgate", "ref": "Daniel 13",
                "loci": {"vulgate": [{"chapter": 13}],
                         "hebrew-unnumbered-titles": [{"chapter": 13}]},
                "edition_loci": {"king-james-version": [
                    {"book": "Sus", "chapter": 1},
                    {"book": "Bel", "chapter": 1},
                ]},
                "unresolved": None,
            }},
        }
        self.write_json(self.prefix + "scripture/32-dan.json", self.daniel)
        self.write_json(self.prefix + "scripture/21-ps.json", {
            "schema": "triptych-catena-scripture/v1", "token": "Ps",
            "chapters": {"50": {
                "token": "Ps", "numbering": "vulgate", "ref": "Psalm 50",
                "loci": {"vulgate": [{"chapter": 50}],
                         "hebrew": [{"chapter": 50}],
                         "hebrew-unnumbered-titles": [{"chapter": 51}]},
                "unresolved": None,
            }},
        })
        for edition, chapters in {
            "king-james-version": (("Dan", 13), ("Sus", 1), ("Bel", 1), ("Ps", 50), ("Ps", 51)),
            "vulgate": (("Dan", 13), ("Ps", 50)),
        }.items():
            for token, chapter in chapters:
                self.write_json(f"src/sources/bibles/{edition}/chapters/{token}/{chapter}.json", {
                    "book": token, "chapter": chapter, "verses": {"1": "fixture"},
                })

    def write(self, relative: str, data: bytes) -> Path:
        path = self.root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(data)
        return path

    def write_json(self, relative: str, data: object) -> Path:
        return self.write(relative, (json.dumps(data) + "\n").encode())

    def assemble(self) -> Path:
        output = self.root / "assembled"
        with mock.patch.object(self.tool, "web_browser_pages", return_value={}):
            self.tool.assemble_web_data(output, True, {})
        return output

    def test_book_projection_is_copied_bound_and_verified(self) -> None:
        relative = (self.tool.SITE_DATA_ROOT / "structure/catena/scripture/32-dan.json").as_posix()
        source = self.root / (self.prefix + "scripture/32-dan.json")
        self.assertEqual(self.tool.web_data_files()[relative], source)
        with ExitStack() as stack:
            for name, result in {
                "publication_map": {}, "included_publications": {},
                "included_document_pages": {}, "pictorial_gallery_source_paths": set(),
                "reading_plan_pdfs": {}, "web_browser_pages": {},
            }.items():
                stack.enter_context(mock.patch.object(self.tool, name, return_value=result))
            stack.enter_context(mock.patch.object(self.tool, "SITE_SOURCE_PATHS", set()))
            self.assertIn(source.relative_to(self.root).as_posix(), self.tool.site_source_paths({}))
        output = self.assemble()
        self.assertEqual((output / relative).read_bytes(), source.read_bytes())
        self.assertEqual(self.tool.verify_web_data(output), [])

    def test_missing_cross_book_native_chapters_are_rejected(self) -> None:
        output = self.assemble()
        for token in ("Sus", "Bel"):
            (output / self.tool.SITE_DATA_ROOT / f"king-james-version/chapters/{token}/1.json").unlink()
        errors = self.tool.verify_web_data(output)
        self.assertTrue(any("Sus 1" in error and "Bel 1" in error for error in errors), errors)

    def test_an_edition_departure_does_not_require_its_unused_base_chapter(self) -> None:
        output = self.assemble()
        (output / self.tool.SITE_DATA_ROOT / "king-james-version/chapters/Dan/13.json").unlink()
        self.assertEqual(self.tool.verify_web_data(output), [])

    def test_manifest_addressing_selects_the_untitled_hebrew_chapter(self) -> None:
        output = self.assemble()
        (output / self.tool.SITE_DATA_ROOT / "king-james-version/chapters/Ps/50.json").unlink()
        self.assertEqual(self.tool.verify_web_data(output), [])
        (output / self.tool.SITE_DATA_ROOT / "king-james-version/chapters/Ps/51.json").unlink()
        errors = self.tool.verify_web_data(output)
        self.assertTrue(any("Ps 51" in error for error in errors), errors)

    def test_refused_edition_does_not_fall_back_to_the_base_or_departure(self) -> None:
        self.daniel["chapters"]["13"]["refused"] = {
            "king-james-version": "The boundary is not established.",
        }
        self.write_json(self.prefix + "scripture/32-dan.json", self.daniel)
        output = self.assemble()
        for token, chapter in (("Dan", 13), ("Sus", 1), ("Bel", 1)):
            (output / self.tool.SITE_DATA_ROOT / f"king-james-version/chapters/{token}/{chapter}.json").unlink()
        self.assertEqual(self.tool.verify_web_data(output), [])

    def test_native_book_tokens_remain_safe(self) -> None:
        self.daniel["chapters"]["13"]["edition_loci"]["king-james-version"][0]["book"] = "../Sus"
        self.write_json(self.prefix + "scripture/32-dan.json", self.daniel)
        errors = self.tool.verify_web_data(self.assemble())
        self.assertTrue(any("unsafe book token" in error for error in errors), errors)

    def test_malformed_edition_maps_are_reported_as_invalid_structure(self) -> None:
        for field in ("refused", "edition_loci"):
            with self.subTest(field=field):
                citation = {"token": "Dan", "loci": {}, field: ["invalid"]}
                with self.assertRaisesRegex(self.tool.ReleaseError, "must be objects"):
                    self.tool.structure_loci(citation, {}, {"vulgate": "vulgate"})

    def test_legacy_manifest_and_numbering_collection_remain_supported(self) -> None:
        manifest = self.tool.parse_bible_manifest(
            self.root / "src/web/data/bibles.json", "fixture manifest",
        )
        self.assertEqual(manifest["vulgate"], "vulgate")
        found = {}
        self.tool.structure_loci({"token": "Ps", "loci": {
            "vulgate": [{"chapter": 50}],
        }}, found)
        self.assertEqual(found, {"vulgate": {("Ps", 50)}})

    def test_new_book_schema_does_not_bypass_the_quarantine_scan(self) -> None:
        self.daniel["chapters"]["13"]["ref"] = self.quarantined
        self.write_json(self.prefix + "scripture/32-dan.json", self.daniel)
        with self.assertRaisesRegex(self.tool.ReleaseError, "quarantined English body"):
            self.tool.web_data_files()


if __name__ == "__main__":
    unittest.main()
