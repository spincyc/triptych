from __future__ import annotations

import copy
import hashlib
import json
from pathlib import Path
import tempfile
import sys
from urllib.parse import urljoin
import unittest
from unittest import mock

from . import test_public_alpha_source_first as fixtures

sys.path.insert(0, str(fixtures.fixtures.REPOSITORY_ROOT / "scripts"))
from _native_tex_publication import (
    INPUT_PATHS, NativeTeXPublicationError, RUNTIME_ROUTE, build_catalog,
)

SCRATCH = fixtures.fixtures.REPOSITORY_ROOT / ".scratch/tex-print-publication/tests"


def digest(body):
    return hashlib.sha256(body).hexdigest()


class NativeTeXPublicationTest(unittest.TestCase):
    def setUp(self):
        SCRATCH.mkdir(parents=True, exist_ok=True)
        temporary = tempfile.TemporaryDirectory(dir=SCRATCH)
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        for relative in (*INPUT_PATHS, "src/gpt/work/main.tex"):
            path = self.root / relative
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text("Canonical input.\n")
        self.revision = "a" * 40
        self.identity = "publication:gpt/work"
        self.documents = {self.identity: {"document": self.identity, "edition": "main"}}
        self.bundle = {"schema": "triptych-native-print-source-bundle/v1",
                       "output_id": self.identity, "document": self.identity,
                       "edition": "main", "source_revision": self.revision,
                       "files": [{"path": "src/gpt/work/main.tex", "content": "Original TeX."}]}
        body = json.dumps(self.bundle).encode()
        route = "native-tex/sources/" + digest(body) + ".json"
        self.source_catalog = {"schema": "triptych-native-print-source-catalog/v1",
                               "source_revision": self.revision,
                               "bundles": {self.identity: {"route": route, "sha256": digest(body), "bytes": len(body)}},
                               "assets": {route: body}, "source_paths": ["src/gpt/work/main.tex"]}
        payload = b"\0asm\1\0\0\0"
        self.runtime_file = self.root / ".scratch/engine.wasm"
        self.runtime_file.parent.mkdir()
        self.runtime_file.write_bytes(payload)
        self.runtime_route = "native-tex/engine/engine.wasm"
        self.runtime = {"schema": "triptych-native-tex-runtime/v1", "id": "engine",
                        "engines": {"pdflatex": {"wasm": {"url": self.runtime_route,
                            "sha256": digest(payload), "bytes": len(payload)}}},
                        "correspondingSource": {"url": "https://example.org/source.tar.gz",
                            "sha256": "b" * 64, "bytes": 123}}
        self.paths = {self.runtime_route: self.runtime_file}

    def build(self, **overrides):
        arguments = {"documents": self.documents, "revision": self.revision,
                     "source_catalog": self.source_catalog,
                     "runtime_manifest": self.runtime, "runtime_paths": self.paths}
        arguments.update(overrides)
        return build_catalog(self.root, **arguments)

    def test_exact_admitted_bundle_and_pinned_runtime_are_the_only_public_files(self):
        catalog = self.build()
        self.assertEqual(set(catalog["assets"]), {RUNTIME_ROUTE, self.runtime_route,
                         self.source_catalog["bundles"][self.identity]["route"]})
        self.assertEqual(set(catalog["selections"]), set(self.documents))
        self.assertEqual(catalog["selections"][self.identity]["bundle_bytes"],
                         len(next(iter(self.source_catalog["assets"].values()))))
        self.assertNotIn("https://example.org/source.tar.gz", catalog["assets"])
        self.assertTrue(set(INPUT_PATHS) <= set(catalog["source_paths"]))
        published_runtime = json.loads(catalog["assets"][RUNTIME_ROUTE]["body"])
        base = urljoin("https://example.org/triptych/native-tex/runtime.json",
                       published_runtime["asset_base"])
        self.assertEqual(urljoin(base, self.runtime_route),
                         "https://example.org/triptych/" + self.runtime_route)

    def test_held_extra_and_missing_source_selections_are_refused(self):
        sources = copy.deepcopy(self.source_catalog)
        sources["bundles"]["publication:gpt/held"] = sources["bundles"][self.identity]
        with self.assertRaisesRegex(NativeTeXPublicationError, "admissions"):
            self.build(source_catalog=sources)
        sources = copy.deepcopy(self.source_catalog)
        sources["bundles"].clear()
        with self.assertRaisesRegex(NativeTeXPublicationError, "admissions"):
            self.build(source_catalog=sources)

    def test_stale_revision_and_companion_substitution_are_refused(self):
        for key, value in (("source_revision", "b" * 40), ("edition", "synthesis"),
                           ("document", "publication:gpt/other")):
            sources = copy.deepcopy(self.source_catalog)
            changed = dict(self.bundle, **{key: value})
            body = json.dumps(changed).encode()
            route = next(iter(sources["assets"]))
            sources["assets"][route] = body
            sources["bundles"][self.identity].update(sha256=digest(body), bytes=len(body))
            with self.subTest(key=key), self.assertRaisesRegex(NativeTeXPublicationError, "substitutes"):
                self.build(source_catalog=sources)

    def test_unowned_or_tampered_source_payload_is_refused(self):
        sources = copy.deepcopy(self.source_catalog)
        sources["assets"]["native-tex/sources/unowned.json"] = b"{}"
        with self.assertRaisesRegex(NativeTeXPublicationError, "unowned"):
            self.build(source_catalog=sources)
        sources = copy.deepcopy(self.source_catalog)
        route = next(iter(sources["assets"]))
        sources["assets"][route] += b" "
        with self.assertRaisesRegex(NativeTeXPublicationError, "byte identity"):
            self.build(source_catalog=sources)

    def test_shared_artwork_is_owned_by_bundle_file_hashes_and_published_once(self):
        sources = copy.deepcopy(self.source_catalog)
        artwork = b"\x89PNG\r\n\x1a\nselected original picture"
        target = "native-tex/assets/" + digest(artwork) + ".png"
        bundle = copy.deepcopy(self.bundle)
        bundle["files"] = [{"path": "src/gpt/work/picture.png", "encoding": "url",
                            "href": "../assets/" + digest(artwork) + ".png",
                            "bytes": len(artwork), "sha256": digest(artwork)}]
        body = json.dumps(bundle).encode()
        route = next(iter(sources["assets"]))
        sources["assets"][route] = body
        sources["bundles"][self.identity].update(bytes=len(body), sha256=digest(body))
        sources["assets"][target] = artwork
        catalog = self.build(source_catalog=sources)
        self.assertEqual(catalog["assets"][target]["body"], artwork)
        sources["assets"][target] += b"changed"
        with self.assertRaisesRegex(NativeTeXPublicationError, "artwork differs"):
            self.build(source_catalog=sources)
    def test_runtime_membership_hash_and_redirected_files_are_refused(self):
        with self.assertRaisesRegex(NativeTeXPublicationError, "inventory"):
            self.build(runtime_paths={})
        with self.assertRaisesRegex(NativeTeXPublicationError, "inventory"):
            self.build(runtime_paths={**self.paths, "native-tex/extra.bin": self.runtime_file})
        self.runtime_file.write_bytes(b"changed")
        with self.assertRaisesRegex(NativeTeXPublicationError, "pinned bytes"):
            self.build()
        alias = self.runtime_file.with_suffix(".alias")
        alias.symlink_to(self.runtime_file)
        with self.assertRaisesRegex(NativeTeXPublicationError, "redirected"):
            self.build(runtime_paths={self.runtime_route: alias})

    def test_public_runtime_has_no_external_executable_fallback_or_pdf(self):
        for route in ("https://example.org/engine.wasm", "native-tex/../escape.bin",
                      "native-tex/print.pdf", "native-tex/engine/source.tex"):
            runtime = copy.deepcopy(self.runtime)
            runtime["engines"]["pdflatex"]["wasm"]["url"] = route
            with self.subTest(route=route), self.assertRaisesRegex(NativeTeXPublicationError, "route"):
                self.build(runtime_manifest=runtime, runtime_paths={route: self.runtime_file})

    def test_canonical_input_inventory_rejects_scratch_and_symlinks(self):
        sources = copy.deepcopy(self.source_catalog)
        for path in (".scratch/engine.wasm", "src/gpt/alias.tex"):
            sources["source_paths"] = [path]
            if path.endswith("alias.tex"):
                (self.root / path).symlink_to(self.root / "src/gpt/work/main.tex")
            with self.subTest(path=path), self.assertRaises(NativeTeXPublicationError):
                self.build(source_catalog=sources)


class PublicAlphaNativeTeXTest(unittest.TestCase):
    def setUp(self):
        self.base = fixtures.PublicAlphaSourceFirstTest(methodName="runTest")
        self.base.setUp()
        self.addCleanup(self.base.doCleanups)
        self.tool = self.base.tool
        self.root = self.base.root
        self.identity = "publication:gpt/work"
        self.body = b'{"schema":"test-native-bundle","body":"Exact canonical TeX"}\n'
        self.wasm = b"\0asm\1\0\0\0"
        self.catalog = {"schema": "triptych-native-tex-publication/v1", "source_revision": "a" * 40,
                        "documents": {self.identity: {"document": self.identity, "edition": "main"}},
                        "runtime": {"href": RUNTIME_ROUTE, "sha256": digest(b"{}\n"), "bytes": 3},
                        "selections": {self.identity: {"bundle_href": "native-tex/sources/work.json",
                            "bundle_sha256": digest(self.body), "bundle_bytes": len(self.body)}},
                        "assets": {}, "source_paths": ["scripts/_native_tex_publication.py"]}
        for route, body in (("native-tex/sources/work.json", self.body),
                            ("native-tex/engine/engine.wasm", self.wasm), (RUNTIME_ROUTE, b"{}\n")):
            self.catalog["assets"][route] = {"body": body, "bytes": len(body), "sha256": digest(body)}
        self.base.write("scripts/_native_tex_publication.py", b"# fixture native transport\n")
        module = type("NativePublication", (), {"catalog": lambda _, root: self.catalog})()
        patch = mock.patch.dict("sys.modules", {"_native_tex_publication": module})
        patch.start()
        self.addCleanup(patch.stop)

    def test_source_first_site_build_and_independent_verification_include_exact_native_payloads(self):
        publications, output = self.base.build_verified()
        self.assertEqual((output / "native-tex/engine/engine.wasm").read_bytes(), self.wasm)
        self.assertEqual((output / "native-tex/sources/work.json").read_bytes(), self.body)
        self.assertFalse(list(output.rglob("*.pdf")))
        manifest = json.loads((output / "PUBLICATION-MANIFEST.json").read_text())
        self.assertTrue(manifest["source_included"])
        self.assertEqual(manifest["native_print"]["source_scope"], "admitted-native-print-bundles")
        self.assertEqual(manifest["native_print"]["editions"], 1)
        self.assertFalse(manifest["native_print"]["stored_pdfs"])
        (output / "native-tex/engine/engine.wasm").write_bytes(b"changed")
        self.tool.write_checksums(output)
        with self.assertRaisesRegex(self.tool.ReleaseError, "native TeX asset differs"):
            self.tool.verify_output(self.base.manifest, publications, output, False)

    def test_native_asset_allowlist_does_not_admit_unowned_wasm_or_any_pdf(self):
        with self.tool.held_repository_inputs():
            self.assertTrue(self.tool.declared_native_tex_asset("native-tex/engine/engine.wasm"))
            self.assertFalse(self.tool.declared_native_tex_asset("native-tex/unowned.wasm"))
            self.assertFalse(self.tool.declared_native_tex_asset("native-tex/print.pdf"))

    def test_url_backed_tex_keeps_privacy_scanning_despite_binary_transport_suffix(self):
        body = b"Original TeX with an accidental /home/private-user/private path.\n"
        self.catalog["assets"]["native-tex/assets/source.bin"] = {
            "body": body, "bytes": len(body), "sha256": digest(body), "kind": "source-text",
        }
        with self.assertRaisesRegex(self.tool.ReleaseError, "home-directory path"):
            self.base.build_verified()

    def test_served_publication_catalog_names_native_pdf_without_editing_generated_input(self):
        corpus = {"works": [{"editions": [{"id": "gpt/work", "print_mode": "manual",
                  "targets": {"reader": "web/gpt/work.html"},
                  "also": [{"id": "gpt/held", "status": "hold", "targets": {}}]}]}]}
        original = json.dumps(corpus).encode()
        relative = "src/web/data/structure/documents/corpus.json"
        self.base.write(relative, original)
        with mock.patch.object(self.tool, "web_print_declared", return_value=True):
            projected = self.tool.projected_document_catalogue(
                "browse/structure/documents/corpus.json", self.root / relative,
                {"pdf/gpt/work.pdf": "web/gpt/work.html"},
            )
        row = json.loads(projected)["works"][0]["editions"][0]
        self.assertEqual(row["print_mode"], "native-pdf")
        self.assertEqual(row["targets"]["print"], "print/gpt/work.html?print=1")
        self.assertEqual(row["also"], corpus["works"][0]["editions"][0]["also"])
        self.assertEqual((self.root / relative).read_bytes(), original)

    def test_legacy_pdf_catalog_action_generates_native_pdf_and_preserves_query_and_fragment(self):
        rewritten = self.tool.rewrite_links(
            "library/test.md", "library/test.html",
            "[PDF](../pdf/gpt/work.pdf?view=print#edition)\n", {("gpt", "work")},
        )
        self.assertEqual(rewritten,
            "[Generate PDF](../print/gpt/work.html?print=1&view=print#edition)\n")
        self.assertIsNone(self.tool.source_to_output(
            "library/test.md", "library/test.html", "../pdf/gpt/held.pdf", {("gpt", "work")},
        ))

    def install_reviewed_loader(self, extra=""):
        route = "native-tex/wasmtex-2026-47ff73bab1a2e548/wasmtex-pdftex.js"
        text = ('FS.mkdir("/home/web_user");var env={"HOME":"/home/web_user"};'
                'function isFileURI(filename){return filename.startsWith("file://")}' + extra)
        body = text.encode()
        identity = digest(body), len(body)
        self.catalog["assets"][route] = {"body": body, "sha256": identity[0],
                                         "bytes": identity[1], "kind": "runtime"}
        # A tiny synthetic core exercises the exact path/pin policy without
        # checking generated engine binaries into Git or requiring an archive.
        patch = mock.patch.dict(self.tool.PUBLIC_NATIVE_LOADER_PRIVACY_IDENTITIES, {route: identity})
        patch.start()
        self.addCleanup(patch.stop)
        return route, text

    def test_reviewed_virtual_home_and_uri_predicate_pass_privacy_verification(self):
        route, text = self.install_reviewed_loader()
        with self.tool.held_repository_inputs():
            filtered = self.tool.public_native_loader_privacy_text(route, text)
        self.assertNotIn("/home/web_user", filtered)
        self.assertNotIn("file://", filtered)
        self.base.build_verified()

    def test_additional_private_paths_and_local_urls_still_fail_inside_pinned_runtime(self):
        for extra, label in (( ';var leaked="/home/private-user/secret";', "home-directory path"),
                             (';var leaked="file:///private/path";', "local file URL"),
                             (';var leaked="ghp_private";', "GitHub token pattern")):
            # Recompute the synthetic reviewed pin: this proves the narrow
            # masking preserves the scanners, rather than only rejecting hashes.
            self.install_reviewed_loader(extra)
            with self.subTest(extra=extra), self.assertRaisesRegex(self.tool.ReleaseError, label):
                self.base.build_verified()

    def test_unregistered_path_wrong_pin_or_modified_bytes_do_not_receive_runtime_exception(self):
        route, text = self.install_reviewed_loader()
        with self.tool.held_repository_inputs():
            self.assertEqual(self.tool.public_native_loader_privacy_text(
                route.replace("wasmtex-pdftex.js", "unreviewed.js"), text), text)
            changed = text + ';var leaked="/home/private-user/secret";'
            self.assertEqual(self.tool.public_native_loader_privacy_text(route, changed), changed)
            self.catalog["assets"][route]["sha256"] = "b" * 64
            self.assertEqual(self.tool.public_native_loader_privacy_text(route, text), text)

    def test_virtual_home_and_file_scheme_in_other_contexts_remain_scanned(self):
        self.install_reviewed_loader(';var path="/home/web_user/private";var uri="file://";')
        with self.assertRaises(self.tool.ReleaseError) as failure:
            self.base.build_verified()
        self.assertIn("home-directory path", str(failure.exception))
        self.assertIn("local file URL", str(failure.exception))


if __name__ == "__main__":
    unittest.main()
