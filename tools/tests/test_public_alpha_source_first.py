from __future__ import annotations

from contextlib import contextmanager
import json
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest
from unittest import mock

try:
    from . import test_public_alpha as fixtures
except ImportError:
    import test_public_alpha as fixtures


SCRATCH = fixtures.REPOSITORY_ROOT / ".scratch/public-source/tests"


class PublicAlphaSourceFirstTest(unittest.TestCase):
    """Exercise source publication without inheriting the legacy PDF suite."""

    def setUp(self) -> None:
        SCRATCH.mkdir(parents=True, exist_ok=True)
        temporary_directory = tempfile.TemporaryDirectory
        self.fixture = fixtures.PublicAlphaTest(methodName="runTest")
        self.addCleanup(self.fixture.doCleanups)
        with mock.patch.object(
            fixtures.tempfile, "TemporaryDirectory",
            side_effect=lambda: temporary_directory(dir=SCRATCH),
        ):
            self.fixture.setUp()
        self.root = self.fixture.root
        self.tool = self.fixture.tool
        self.manifest = self.fixture.manifest
        self.write = self.fixture.write
        self.write_reader("work")
        shutil.rmtree(self.root / "pdf")

    def write_reader(self, leaf: str) -> None:
        self.write(
            f"src/gpt/{leaf}/web-edition.toml",
            b'eligibility = "eligible"\nblocking = []\n'
            b'rationale = "The complete prose survives reflow."\n',
        )
        self.write(
            f"web/gpt/{leaf}.md",
            (
                f"# Reviewed {leaf}\n\n"
                "## Complete section {#complete-section}\n\n"
                "The opening paragraph of the reviewed edition survives.\n\n"
                "[Read the appendix](#complete-appendix).\n\n"
                "| Witness | Finding |\n| --- | --- |\n"
                "| Retained witness | Complete table cell |\n\n"
                "## Complete appendix {#complete-appendix}\n\n"
                "The terminal appendix and its source qualification survive.\n"
            ).encode(),
        )

    @contextmanager
    def without_pdf_dependencies(self):
        forbidden = {"pdflatex", "pdfinfo", "pdftotext"}
        original_popen = subprocess.Popen

        def guarded_popen(argv, *arguments, **keywords):
            command = argv if isinstance(argv, (list, tuple)) else str(argv).split()
            self.assertFalse(
                forbidden.intersection(Path(str(part)).name for part in command),
                f"source publication invoked PDF tooling: {argv!r}",
            )
            return original_popen(argv, *arguments, **keywords)

        with (
            mock.patch.object(subprocess, "Popen", side_effect=guarded_popen),
        ):
            yield

    def build_verified(self, *, preview: bool = False):
        self.fixture.authorize_current_inputs()
        publications = self.tool.validate_manifest(self.manifest)
        output = self.tool.build_site(self.manifest, publications, preview=preview)
        self.tool.verify_output(self.manifest, publications, output, preview=preview)
        return publications, output

    def write_print_archive(self, *leaves: str) -> dict:
        snapshot = "1" * 40
        rows = []
        for leaf in leaves:
            filename = Path(self.tool.public_pdf_path("gpt", leaf)).name
            rows.append({
                "id": f"gpt/{leaf}", "legacy_pdf": f"pdf/gpt/{leaf}.pdf",
                "filename": filename, "sha256": fixtures.digest(b"prior print bytes\n"),
                "bytes": len(b"prior print bytes\n"),
                "url": f"https://github.com/spincyc/triptych-artifacts/releases/download/prints-{snapshot[:7]}/{filename}",
            })
        index = {
            "schema": "triptych-print-archive/v1", "snapshot": snapshot,
            "source_manifest_url": f"{self.tool.SITE_ORIGIN}/PUBLICATION-MANIFEST.json",
            "source_manifest_sha256": fixtures.digest(b"historical manifest\n"),
            "publications": rows,
        }
        self.fixture.write_json("release/print-archive.json", index)
        return index

    def write_archive_pages(self, index: dict) -> dict:
        receipt = {
            "schema": "triptych-print-archive-pages/v1",
            "archive_manifest_sha256": fixtures.digest((self.root / "release/print-archive.json").read_bytes()),
            "method": "Synthetic page-count fixture; no PDF acquisition.",
            "publications": [{
                "id": row["id"], "legacy_pdf": row["legacy_pdf"],
                "pdf_sha256": row["sha256"], "pages": 23,
            } for row in index["publications"]],
        }
        self.fixture.write_json("release/print-archive-pages.json", receipt)
        return receipt

    def test_admitted_source_builds_and_verifies_with_no_pdf_tree_or_pdf_tools(self) -> None:
        with self.without_pdf_dependencies():
            publications, output = self.build_verified()
            candidate = self.tool.candidate_inventory_data(self.manifest, publications)

        self.assertFalse((self.root / "pdf").exists())
        self.assertFalse(list(output.rglob("*.pdf")))
        artifact = json.loads((output / "PUBLICATION-MANIFEST.json").read_text())
        self.assertEqual(artifact["publication_model"], "source-first")
        self.assertEqual(artifact["publications"][0]["reader"], "web/gpt/work.html")
        self.assertEqual(artifact["publications"][0]["print"], "print/gpt/work.html")
        self.assertEqual(
            artifact["publications"][0]["source_identity"],
            self.tool.publication_source_identity("gpt", "work"),
        )
        self.assertNotIn("pdf_sha256", artifact["publications"][0])
        self.assertEqual(candidate["publications"][0]["source"], "src/gpt/work/main.tex")

    def test_legacy_pdf_link_resolves_to_existing_reader_without_pdf_inventories(self) -> None:
        with self.without_pdf_dependencies():
            _, output = self.build_verified()

        catalog = (output / "library/test.html").read_text()
        self.assertIn('href="../web/gpt/work.html"', catalog)
        self.assertNotIn("pdf/gpt/work.pdf", catalog)
        self.assertTrue((output / "web/gpt/work.html").is_file())
        self.assertEqual(self.tool.verify_links(output), [])

    def test_print_route_preserves_complete_reviewed_markdown_and_anchors(self) -> None:
        with self.without_pdf_dependencies():
            _, output = self.build_verified()

        for route in ("web/gpt/work.html", "print/gpt/work.html"):
            with self.subTest(route=route):
                page = (output / route).read_text()
                self.assertIn("The opening paragraph of the reviewed edition survives.", page)
                self.assertIn("Complete table cell", page)
                self.assertIn("The terminal appendix and its source qualification survive.", page)
                self.assertIn('id="complete-section"', page)
                self.assertIn('id="complete-appendix"', page)
                self.assertIn('href="#complete-appendix"', page)
                self.assertNotIn("A browser reading edition is not available", page)

    def test_fixed_layout_output_has_honest_print_information_without_reading_claim(self) -> None:
        (self.root / "web/gpt/work.md").unlink()
        self.write(
            "src/gpt/work/web-edition.toml",
            b'eligibility = "ineligible"\nblocking = ["duplex-cards"]\n'
            b'rationale = "The fixed page geometry carries the meaning."\n',
        )
        with self.without_pdf_dependencies():
            _, output = self.build_verified()

        for route in ("web/gpt/work.html", "print/gpt/work.html"):
            with self.subTest(route=route):
                page = (output / route).read_text()
                self.assertIn("A browser reading edition is not available for this output.", page)
                self.assertIn("Generate the PDF from a local copy of Triptych:", page)
                self.assertIn("print-document build --document publication:gpt/work", page)
                self.assertNotIn('href="work.pdf"', page)
                self.assertNotIn("Download PDF", page)
                self.assertNotIn("Complete table cell", page)
        self.assertFalse(list(output.rglob("*.pdf")))

    def test_held_source_and_reviewed_edition_leak_into_neither_public_nor_preview(self) -> None:
        self.fixture.add_unapproved_publication("held-work", "hold")
        self.write_reader("held-work")
        self.write("web/gpt/held-work.md", b"# Secret held reader\n\nHeld-only prose.\n")
        for preview in (False, True):
            with self.subTest(preview=preview), self.without_pdf_dependencies():
                _, output = self.build_verified(preview=preview)
                files = {path.relative_to(output).as_posix() for path in output.rglob("*") if path.is_file()}
                for route in ("web/gpt/held-work.html", "print/gpt/held-work.html"):
                    self.assertNotIn(route, files)
                for relative in files:
                    if relative.endswith((".html", ".json")):
                        text = (output / relative).read_text()
                        self.assertNotIn("held-work", text, relative)
                        self.assertNotIn("Held-only prose.", text, relative)

    def test_source_mutation_changes_identity_and_rejects_prior_site_binding(self) -> None:
        with self.without_pdf_dependencies():
            publications, output = self.build_verified()
            before = self.tool.publication_source_identity("gpt", "work")
            self.write("src/gpt/work/main.tex", b"Changed canonical source.\n")
            after = self.tool.publication_source_identity("gpt", "work")
            self.assertNotEqual(before["content"]["sha256"], after["content"]["sha256"])
            self.assertNotEqual(before["output"]["sha256"], after["output"]["sha256"])
            with self.assertRaises(self.tool.ReleaseError) as failure:
                self.tool.verify_output(self.manifest, publications, output, preview=False)

        self.assertIn("src/gpt/work/main.tex does not match its approved SHA-256", str(failure.exception))

    def test_manifest_mutation_changes_identity_and_rejects_prior_site_binding(self) -> None:
        with self.without_pdf_dependencies():
            publications, output = self.build_verified()
            before = self.tool.publication_source_identity("gpt", "work")
            path = self.root / "src/gpt/work/publication.toml"
            original = path.read_text()
            self.assertIn('role = "body"', original)
            path.write_text(original.replace('role = "body"', 'role = "body"\nkey = "reviewed-body"'))
            after = self.tool.publication_source_identity("gpt", "work")
            self.assertNotEqual(before["content"]["sha256"], after["content"]["sha256"])
            self.assertNotEqual(before["output"]["sha256"], after["output"]["sha256"])
            with self.assertRaises(self.tool.ReleaseError) as failure:
                self.tool.verify_output(self.manifest, publications, output, preview=False)

        self.assertIn("src/gpt/work/publication.toml does not match its approved SHA-256", str(failure.exception))

    def test_missing_or_unknown_publication_declaration_is_rejected(self) -> None:
        path = self.root / "src/gpt/work/publication.toml"
        original = path.read_bytes()
        path.unlink()
        with self.assertRaisesRegex(self.tool.ReleaseError, "missing publication.toml"):
            self.tool.publication_source_records()
        path.write_bytes(b'reader_title = "Undeclared override"\n' + original)
        with self.assertRaisesRegex(self.tool.ReleaseError, "unknown fields: reader_title"):
            self.tool.publication_source_records()

    def test_source_reader_inventory_without_declared_catalogues_is_empty(self) -> None:
        from _print_catalog import source_pages

        with self.without_pdf_dependencies():
            self.assertEqual(source_pages(self.root), {})

    def test_bare_source_entrypoint_provides_print_recipe_and_readable_title_fallback(self) -> None:
        from _print_document import publication_recipe

        with self.without_pdf_dependencies():
            recipe = publication_recipe("gpt", "work", root=self.root)
            self.assertEqual(recipe["entrypoint"], "src/gpt/work/main.tex")
            self.assertIsNone(recipe["title"])
            self.assertEqual(recipe["formats"], ["pdf"])
            (self.root / "web/gpt/work.md").unlink()
            page = self.tool.render_publication_print_page("gpt", "work", "print/gpt/work.html", False, {})

        self.assertRegex(page, r"<h1(?: [^>]*)?>Work</h1>")
        self.assertIn("A browser reading edition is not available for this output.", page)

    def test_successive_prepare_commands_refresh_source_inventory(self) -> None:
        from _document_schema import discover

        self.fixture.authorize_current_inputs()
        with mock.patch("_document_schema.discover", wraps=discover) as source_scan:
            first_result, first_json, first_error = self.fixture.run_main("prepare")
            self.assertEqual((first_result, first_error), (0, ""))
            self.assertEqual(source_scan.call_count, 1)
            self.write("src/gpt/work/main.tex", b"Changed between actual prepare commands.\n")
            second_result, second_json, second_error = self.fixture.run_main("prepare")
            self.assertEqual((second_result, second_error), (0, ""))
            self.assertEqual(source_scan.call_count, 2)

        first = json.loads(first_json)["publications"][0]
        second = json.loads(second_json)["publications"][0]
        self.assertNotEqual(first["content"]["sha256"], second["content"]["sha256"])

    def test_source_inventories_are_reused_within_command_and_refreshed_next_command(self) -> None:
        from _document_schema import discover
        from _print_catalog import source_pages

        self.write("src/web/data/bibles.json", b'{"bibles": []}\n')
        with (
            mock.patch("_document_schema.discover", wraps=discover) as source_scan,
            mock.patch("_print_catalog.source_pages", wraps=source_pages) as reader_scan,
        ):
            with self.tool.held_repository_inputs():
                before = self.tool.publication_source_identity("gpt", "work")
                self.tool.publication_source_records()
                self.tool.source_print_pages()
                self.tool.source_reader_routes()
                self.tool.source_print_pages()
                self.assertEqual(source_scan.call_count, 1)
                self.assertEqual(reader_scan.call_count, 1)
            self.write("src/gpt/work/main.tex", b"New command sees this source revision.\n")
            with self.tool.held_repository_inputs():
                after = self.tool.publication_source_identity("gpt", "work")
                self.tool.source_reader_routes()
                self.assertEqual(source_scan.call_count, 2)
                self.assertEqual(reader_scan.call_count, 2)

        self.assertNotEqual(before["content"]["sha256"], after["content"]["sha256"])
        self.assertEqual(self.tool._HELD_SOURCE_INVENTORIES, [])
        self.write("src/gpt/work/main.tex", b"Outside a command also observes new bytes.\n")
        outside = self.tool.publication_source_identity("gpt", "work")
        self.assertNotEqual(after["content"]["sha256"], outside["content"]["sha256"])

    def test_source_research_and_archive_bytes_are_never_copied(self) -> None:
        markers = {
            "src/gpt/work/main.tex": b"PRIVATE-CANONICAL-SOURCE-SENTINEL\n",
            "src/gpt/work/research/source-audit.md": b"PRIVATE-RESEARCH-SENTINEL\n",
            "src/sources/artifacts/evidence-archive.zip": b"PRIVATE-ARCHIVE-SENTINEL\n",
        }
        for relative, payload in markers.items():
            self.write(relative, payload)
        with self.without_pdf_dependencies():
            _, output = self.build_verified()

        for path in output.rglob("*"):
            if not path.is_file():
                continue
            relative = path.relative_to(output)
            self.assertNotIn("src", relative.parts)
            self.assertNotIn("research", relative.parts)
            self.assertNotEqual(path.suffix, ".zip")
            payload = path.read_bytes()
            for sentinel in markers.values():
                self.assertNotIn(sentinel.strip(), payload, relative.as_posix())

    def test_archived_print_index_is_optional_and_rejects_unbound_byte_identities(self) -> None:
        self.assertEqual(self.tool.archived_prints(), {})
        original = self.write_print_archive("work")
        self.assertEqual(self.tool.archived_prints()["gpt/work"]["snapshot"], original["snapshot"])
        for mutation in ("snapshot", "url", "filename", "digest", "bytes", "duplicate", "unknown"):
            with self.subTest(mutation=mutation):
                index = json.loads(json.dumps(original))
                row = index["publications"][0]
                if mutation == "snapshot":
                    index["snapshot"] = "short"
                elif mutation == "url":
                    row["url"] = "https://example.invalid/unverified.pdf"
                elif mutation == "filename":
                    row["filename"] = "other-publication.pdf"
                elif mutation == "digest":
                    row["sha256"] = "unknown"
                elif mutation == "bytes":
                    row["bytes"] = True
                elif mutation == "duplicate":
                    index["publications"].append(dict(row))
                else:
                    row["verified"] = True
                self.fixture.write_json("release/print-archive.json", index)
                with self.assertRaises(self.tool.ReleaseError):
                    self.tool.archived_prints()

    def test_archived_print_link_names_prior_snapshot_without_fetching_pdf(self) -> None:
        index = self.write_print_archive("work")
        (self.root / "web/gpt/work.md").unlink()
        self.write("src/gpt/work/web-edition.toml", b'eligibility = "ineligible"\n')
        with (
            self.without_pdf_dependencies(),
            mock.patch("urllib.request.urlopen", side_effect=AssertionError("site build fetched an archive")),
        ):
            _, output = self.build_verified()

        row = index["publications"][0]
        for route in ("web/gpt/work.html", "print/gpt/work.html"):
            page = (output / route).read_text()
            self.assertIn(f'href="{row["url"]}">Archived PDF</a>', page)
            self.assertIn(f'published snapshot <code>{index["snapshot"][:7]}</code>', page)
            self.assertIn("This preserved printing may precede the current source revision.", page)
        artifact = json.loads((output / "PUBLICATION-MANIFEST.json").read_text())
        self.assertEqual(artifact["publications"][0]["archived_pdf"], {
            "url": row["url"], "sha256": row["sha256"], "bytes": row["bytes"],
            "snapshot": index["snapshot"],
        })
        self.assertIn("release/print-archive.json", self.tool.site_source_paths(self.manifest))
        self.assertFalse(list(output.rglob("*.pdf")))
        self.assertFalse((output / "release/print-archive.json").exists())

    def test_archive_index_never_exposes_held_prints(self) -> None:
        self.fixture.add_unapproved_publication("held-work", "hold")
        self.write_reader("held-work")
        index = self.write_print_archive("work", "held-work")
        with self.without_pdf_dependencies():
            _, output = self.build_verified()

        held = index["publications"][1]
        for path in output.rglob("*"):
            if path.is_file() and path.suffix in {".html", ".json"}:
                text = path.read_text()
                self.assertNotIn(held["url"], text, path.relative_to(output).as_posix())
                self.assertNotIn(held["filename"], text, path.relative_to(output).as_posix())

    def test_archive_index_mutation_invalidates_approved_site_binding(self) -> None:
        index = self.write_print_archive("work")
        with self.without_pdf_dependencies():
            publications, output = self.build_verified()
            index["publications"][0]["sha256"] = fixtures.digest(b"different archived bytes\n")
            self.fixture.write_json("release/print-archive.json", index)
            with self.assertRaises(self.tool.ReleaseError) as failure:
                self.tool.verify_output(self.manifest, publications, output, preview=False)

        self.assertIn("release/print-archive.json does not match its approved SHA-256", str(failure.exception))

    def test_archive_page_receipt_binds_historical_count_without_reading_pdf(self) -> None:
        index = self.write_print_archive("work")
        self.write_archive_pages(index)
        original_read_bytes = Path.read_bytes

        def read_without_pdf(path):
            if path.suffix.lower() == ".pdf":
                raise AssertionError("site build read archived PDF bytes")
            return original_read_bytes(path)

        with (
            self.without_pdf_dependencies(),
            mock.patch.object(Path, "read_bytes", new=read_without_pdf),
            mock.patch("urllib.request.urlopen", side_effect=AssertionError("site build fetched archived PDF bytes")),
        ):
            _, output = self.build_verified()
            archived = self.tool.archived_prints()["gpt/work"]

        self.assertEqual(archived["pages"], 23)
        artifact = json.loads((output / "PUBLICATION-MANIFEST.json").read_text())
        self.assertEqual(artifact["publications"][0]["archived_pdf"]["pages"], 23)
        self.assertEqual(artifact["publications"][0]["archived_pdf"]["snapshot"], index["snapshot"])
        receipt_path = "release/print-archive-pages.json"
        self.assertIn(receipt_path, self.tool.site_source_paths(self.manifest))
        self.assertEqual(
            self.manifest["authorizations"]["test-authorization"]["site_sources"][receipt_path],
            fixtures.digest((self.root / receipt_path).read_bytes()),
        )
        self.assertFalse((self.root / "pdf").exists())
        self.assertFalse(list(output.rglob("*.pdf")))

    def test_archive_page_receipt_rejects_stale_incomplete_or_unsafe_identity(self) -> None:
        index = self.write_print_archive("work")
        original = self.write_archive_pages(index)
        mutations = ("index", "id", "legacy", "pdf-digest", "zero", "boolean", "duplicate", "missing", "unknown", "method")
        for mutation in mutations:
            with self.subTest(mutation=mutation):
                receipt = json.loads(json.dumps(original))
                row = receipt["publications"][0]
                if mutation == "index":
                    receipt["archive_manifest_sha256"] = "0" * 64
                elif mutation == "id":
                    row["id"] = "gpt/unknown"
                elif mutation == "legacy":
                    row["legacy_pdf"] = "pdf/gpt/other.pdf"
                elif mutation == "pdf-digest":
                    row["pdf_sha256"] = "0" * 64
                elif mutation == "zero":
                    row["pages"] = 0
                elif mutation == "boolean":
                    row["pages"] = True
                elif mutation == "duplicate":
                    receipt["publications"].append(dict(row))
                elif mutation == "missing":
                    receipt["publications"] = []
                elif mutation == "unknown":
                    row["verified"] = True
                else:
                    receipt["method"] = " "
                self.fixture.write_json("release/print-archive-pages.json", receipt)
                with self.assertRaises(self.tool.ReleaseError):
                    self.tool.archived_prints()

        self.fixture.write_json("release/print-archive-pages.json", original)
        for relative in ("release/print-archive.json", "release/print-archive-pages.json"):
            with self.subTest(symlink=relative):
                path = self.root / relative
                payload = path.read_bytes()
                evidence = self.root / ".scratch" / path.name
                evidence.parent.mkdir(exist_ok=True)
                evidence.write_bytes(payload)
                path.unlink()
                path.symlink_to(evidence)
                with self.assertRaisesRegex(self.tool.ReleaseError, "must not be a symlink"):
                    self.tool.archived_prints()
                path.unlink()
                path.write_bytes(payload)
        (self.root / "release/print-archive.json").unlink()
        with self.assertRaisesRegex(self.tool.ReleaseError, "no controlling archive index"):
            self.tool.archived_prints()

    def test_archive_page_receipt_change_independently_invalidates_site_binding(self) -> None:
        index = self.write_print_archive("work")
        receipt = self.write_archive_pages(index)
        with self.without_pdf_dependencies():
            publications, output = self.build_verified()
            artifact = json.loads((output / "PUBLICATION-MANIFEST.json").read_text())
            receipt["method"] = "A revised synthetic measurement description."
            self.fixture.write_json("release/print-archive-pages.json", receipt)
            self.assertEqual(self.tool.artifact_manifest_data(self.manifest, publications, False), artifact)
            with self.assertRaises(self.tool.ReleaseError) as failure:
                self.tool.verify_output(self.manifest, publications, output, preview=False)

        self.assertIn("release/print-archive-pages.json does not match its approved SHA-256", str(failure.exception))

    def test_dedicated_scratch_output_builds_and_verifies_without_changing_sources(self) -> None:
        self.tool.OUTPUT_ROOT = self.root / ".scratch/site-artifacts"
        self.write(".scratch/unrelated/keep.txt", b"unrelated scratch sentinel\n")
        self.fixture.authorize_current_inputs()
        before = self.fixture.tracked_bytes()
        with self.without_pdf_dependencies():
            publications = self.tool.validate_manifest(self.manifest)
            output = self.tool.build_site(self.manifest, publications, preview=False)
            self.tool.verify_output(self.manifest, publications, output, preview=False)

        self.assertEqual(output, self.root / ".scratch/site-artifacts/site")
        self.assertTrue((output / "PUBLICATION-MANIFEST.json").is_file())
        self.assertFalse((self.root / "build").exists())
        outside_output = {
            path: data for path, data in self.fixture.tracked_bytes().items()
            if not path.startswith(".scratch/site-artifacts/")
        }
        self.assertEqual(outside_output, before)

    def test_output_root_rejects_source_root_scratch_root_and_lexical_traversal(self) -> None:
        self.write(".scratch/keep.txt", b"scratch root sentinel\n")
        self.fixture.authorize_current_inputs()
        publications = self.tool.validate_manifest(self.manifest)
        before = self.fixture.tracked_bytes()
        forbidden = (
            self.root,
            self.root / "src",
            self.root / ".scratch",
            self.root / ".scratch/site-artifacts/../escape",
        )
        for output_root in forbidden:
            with self.subTest(output_root=output_root):
                self.tool.OUTPUT_ROOT = output_root
                with self.assertRaises(self.tool.ReleaseError):
                    self.tool.build_site(self.manifest, publications, preview=False)
                with self.assertRaises(self.tool.ReleaseError):
                    self.tool.verify_output(self.manifest, publications, output_root / "site", preview=False)
                self.assertEqual(self.fixture.tracked_bytes(), before)

    def test_output_root_rejects_external_directory_without_touching_sentinel(self) -> None:
        external = tempfile.TemporaryDirectory(dir=SCRATCH)
        self.addCleanup(external.cleanup)
        destination = Path(external.name)
        sentinel = destination / "keep.txt"
        sentinel.write_bytes(b"external output sentinel\n")
        self.tool.OUTPUT_ROOT = destination
        self.fixture.authorize_current_inputs()
        publications = self.tool.validate_manifest(self.manifest)
        before = self.fixture.tracked_bytes()
        with self.assertRaisesRegex(self.tool.ReleaseError, "beneath the repository"):
            self.tool.build_site(self.manifest, publications, preview=False)
        with self.assertRaisesRegex(self.tool.ReleaseError, "beneath the repository"):
            self.tool.verify_output(self.manifest, publications, destination / "site", preview=False)

        self.assertEqual(sentinel.read_bytes(), b"external output sentinel\n")
        self.assertEqual(set(destination.iterdir()), {sentinel})
        self.assertEqual(self.fixture.tracked_bytes(), before)

    def test_scratch_output_rejects_symlinked_ancestor_and_preserves_external_tree(self) -> None:
        external = tempfile.TemporaryDirectory(dir=SCRATCH)
        self.addCleanup(external.cleanup)
        destination = Path(external.name)
        sentinel = destination / "keep.txt"
        sentinel.write_bytes(b"symlink destination sentinel\n")
        self.write(".scratch/keep.txt", b"scratch sibling sentinel\n")
        link = self.root / ".scratch/link"
        link.symlink_to(destination, target_is_directory=True)
        self.tool.OUTPUT_ROOT = link / "site-artifacts"
        self.fixture.authorize_current_inputs()
        publications = self.tool.validate_manifest(self.manifest)
        before = self.fixture.tracked_bytes()
        with self.assertRaisesRegex(self.tool.ReleaseError, "is a symlink"):
            self.tool.build_site(self.manifest, publications, preview=False)
        with self.assertRaisesRegex(self.tool.ReleaseError, "is a symlink"):
            self.tool.verify_output(self.manifest, publications, self.tool.OUTPUT_ROOT / "site", preview=False)

        self.assertTrue(link.is_symlink())
        self.assertEqual(sentinel.read_bytes(), b"symlink destination sentinel\n")
        self.assertEqual(set(destination.iterdir()), {sentinel})
        self.assertEqual(self.fixture.tracked_bytes(), before)


class PublicAlphaSourceReaderIntegrationTest(unittest.TestCase):
    def test_real_source_readers_fit_page_budget_and_ship_full_volume_controller(self) -> None:
        tool = fixtures.load_tool()
        controller = "src/web/browser/shared/print-volume.js"
        expected_roots = {
            "reading-plans/narrative-spine-full-account-douay-rheims.html",
            "reading-plans/narrative-spine-full-account-king-james-version.html",
        }
        with (
            tool.held_repository_inputs(),
            mock.patch.object(subprocess, "Popen", side_effect=AssertionError("source-reader regression invoked a subprocess")),
        ):
            pages = tool.source_print_pages()
            self.assertTrue(pages, "real source-reader inventory is empty")
            self.assertTrue(expected_roots <= pages.keys(), "full-account source roots are missing")
            files = tool.web_data_files()
            self.assertEqual(files["shared/print-volume.js"], tool.ROOT / controller)
            for relative, page in pages.items():
                with self.subTest(page=relative):
                    rendered = tool.render_source_print_page(relative, page, False, {})
                    self.assertLessEqual(len(rendered.encode("utf-8")), tool.PREVIEW_DOCUMENT_LIMIT)
                    if relative in expected_roots:
                        self.assertIn(controller, page["source_paths"])
                        self.assertIn('src="../shared/print-volume.js"', page["html"])


if __name__ == "__main__":
    unittest.main()
