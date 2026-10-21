"""Exercise the explicit single-character font's publication boundary."""

from __future__ import annotations

from contextlib import ExitStack
import importlib.machinery
import importlib.util
import os
from pathlib import Path
import shutil
import tempfile
import unittest
from unittest import mock


REPOSITORY = Path(__file__).resolve().parents[2]


class PublicAlphaFontTest(unittest.TestCase):
    def setUp(self) -> None:
        scratch = Path(os.environ.get(
            "PUBLIC_ALPHA_FONT_TEST_SCRATCH", ".scratch/tests/public-alpha-fonts"
        ))
        if not scratch.is_absolute():
            scratch = REPOSITORY / scratch
        scratch.mkdir(parents=True, exist_ok=True)
        temporary = tempfile.TemporaryDirectory(dir=scratch)
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        loader = importlib.machinery.SourceFileLoader(
            "test_public_alpha_font_tool", str(REPOSITORY / "tools/public-alpha")
        )
        spec = importlib.util.spec_from_loader(loader.name, loader)
        self.assertIsNotNone(spec)
        self.tool = importlib.util.module_from_spec(spec)
        loader.exec_module(self.tool)
        self.tool.ROOT = self.root
        quarantine = self.tool.POSTCONCILIAR_TRANSLATIONS_RELATIVE
        self.write(quarantine.as_posix(), (REPOSITORY / quarantine).read_bytes())
        for directory in self.tool.WEB_BROWSER_DIRECTORIES:
            self.write(f"src/web/browser/{directory}/fixture.css", b"/* fixture */\n")
        self.core = self.write(
            "src/web/browser/shared/browser-core.css",
            (REPOSITORY / "src/web/browser/shared/browser-core.css").read_bytes(),
        )
        for source in self.tool.WEB_BROWSER_FONT_ASSETS.values():
            self.write(source.as_posix(), (REPOSITORY / source).read_bytes())
        self.write(
            "src/web/data/bibles.json",
            b'{"bibles":[{"id":"fixture","numbering":"fixture"}]}\n',
        )
        (self.root / "src/sources/bibles/fixture/chapters").mkdir(parents=True)

    def write(self, relative: str, data: bytes) -> Path:
        path = self.root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(data)
        return path

    def font_path(self, suffix: str) -> Path:
        return next(
            self.root / source
            for source in self.tool.WEB_BROWSER_FONT_ASSETS.values()
            if source.suffix == suffix
        )

    def test_exact_assets_join_scan_source_binding_and_artifact_set(self) -> None:
        assets = self.tool.browser_font_files()
        self.assertEqual(set(assets), {
            "shared/fonts/triptych-punctus-elevatus.woff2",
            "shared/fonts/OFL-Junicode.txt",
        })
        self.assertTrue(set(assets).issubset(self.tool.web_data_files()))
        with ExitStack() as stack:
            for name, result in {
                "publication_map": {}, "included_publications": {},
                "included_document_pages": {}, "pictorial_gallery_source_paths": set(),
                "reading_plan_pdfs": {}, "web_browser_pages": {},
                "public_pdf_aliases": {}, "artifact_license_source_paths": set(),
                "requires_unadvertised_controls": False,
            }.items():
                stack.enter_context(mock.patch.object(self.tool, name, return_value=result))
            stack.enter_context(mock.patch.object(self.tool, "SITE_SOURCE_PATHS", set()))
            stack.enter_context(mock.patch.object(self.tool, "PAGE_MAP", {}))
            bound = self.tool.site_source_paths({})
            expected = self.tool.expected_artifact_files({}, {}, True, {})
        self.assertTrue({p.relative_to(self.root).as_posix() for p in assets.values()} <= bound)
        self.assertTrue(set(assets) <= expected)

    def test_old_css_fixture_does_not_silently_activate_a_new_font(self) -> None:
        self.core.write_text("/* no source punctuation font in this fixture */\n")
        shutil.rmtree(self.core.parent / "fonts")
        self.assertEqual(self.tool.browser_font_files(), {})

    def test_active_css_requires_font_and_licence(self) -> None:
        for suffix in (".woff2", ".txt"):
            with self.subTest(suffix=suffix):
                path = self.font_path(suffix)
                data = path.read_bytes()
                path.unlink()
                with self.assertRaisesRegex(self.tool.ReleaseError, "font input is missing"):
                    self.tool.browser_font_files()
                path.write_bytes(data)

    def test_font_and_licence_cannot_be_symlinked(self) -> None:
        for suffix in (".woff2", ".txt"):
            with self.subTest(suffix=suffix):
                path = self.font_path(suffix)
                data = path.read_bytes()
                other = self.write("elsewhere/" + path.name, data)
                path.unlink()
                path.symlink_to(other)
                with self.assertRaisesRegex(self.tool.ReleaseError, "font input is a symlink"):
                    self.tool.browser_font_files()
                path.unlink()
                path.write_bytes(data)

    def test_font_directory_cannot_be_symlinked(self) -> None:
        directory = self.font_path(".woff2").parent
        other = self.root / "elsewhere"
        directory.rename(other)
        directory.symlink_to(other, target_is_directory=True)
        with self.assertRaisesRegex(self.tool.ReleaseError, "font input is a symlink"):
            self.tool.browser_font_files()

    def test_malformed_font_and_empty_licence_are_rejected(self) -> None:
        font = self.font_path(".woff2")
        data = font.read_bytes()
        font.write_bytes(b"not a WOFF2 font")
        with self.assertRaisesRegex(self.tool.ReleaseError, "font input is not WOFF2"):
            self.tool.browser_font_files()
        font.write_bytes(data)
        self.font_path(".txt").write_bytes(b"")
        with self.assertRaisesRegex(self.tool.ReleaseError, "font input is empty"):
            self.tool.browser_font_files()

    def test_copy_and_parity_cover_font_and_licence_bytes(self) -> None:
        output = self.root / "assembled"
        with mock.patch.object(self.tool, "web_browser_pages", return_value={}):
            self.tool.assemble_web_data(output, True, {})
        self.assertEqual(self.tool.verify_web_data(output), [])
        for relative, source in self.tool.browser_font_files().items():
            with self.subTest(relative=relative):
                artifact = output / relative
                self.assertEqual(artifact.read_bytes(), source.read_bytes())
                artifact.write_bytes(artifact.read_bytes() + b"tampered")
                # Artifact-local hashes cannot authenticate a substituted font/licence.
                self.tool.write_checksums(output)
                errors = self.tool.verify_web_data(output)
                self.assertEqual(len(errors), 1, errors)
                self.assertIn(relative + ": copied browser/data file", errors[0])
                artifact.write_bytes(source.read_bytes())

    def test_woff2_admission_is_an_exact_path_exception(self) -> None:
        known = self.font_path(".woff2")
        relative = "shared/fonts/triptych-punctus-elevatus.woff2"
        self.assertEqual(self.tool._artifact_topology_errors({relative: known.stat()}), [])
        for relative in ("shared/fonts/other.woff2", "assets/triptych-punctus-elevatus.woff2"):
            with self.subTest(relative=relative):
                errors = self.tool._artifact_topology_errors({relative: known.stat()})
                self.assertEqual(errors, ["artifact contains an unexpected file type: " + relative])


if __name__ == "__main__":
    unittest.main()
