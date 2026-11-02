"""Exact artifact delivery preserves bytes and never fetches implicitly."""
from __future__ import annotations

import copy
import hashlib
import io
import json
from pathlib import Path
import subprocess
import sys
import tarfile
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))
import _artifact_store as store


class ArtifactStoreTests(unittest.TestCase):
    def setUp(self):
        scratch = ROOT / ".scratch/artifact-store/tests"
        scratch.mkdir(parents=True, exist_ok=True)
        self.temporary = tempfile.TemporaryDirectory(dir=scratch)
        self.root = Path(self.temporary.name)
        self.source = "src/sources/works/author/book/editions/1900-print/artifacts/scan/scan.djvu"
        self.publication = "pdf/gpt/history/main.pdf"
        self.payloads = {self.source: b"AT&TFORM\x00source scan\n" * 100,
                         self.publication: b"%PDF-1.4\nexact historical bytes\n" * 560}
        for relative, content in self.payloads.items():
            target = self.root / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(content)
        self.manifest = self.root / Path(self.source).parent / "artifact.toml"
        content = self.payloads[self.source]
        self.manifest.write_text(
            f'path = "{self.source}"\nsha256 = "{hashlib.sha256(content).hexdigest()}"\n'
            f'byte_size = {len(content)}\nmedia_type = "image/vnd.djvu"\n'
            'source_url = "https://example.org/original.djvu"\n', encoding="utf-8")
        self.git("init", "-q")
        self.git("add", "pdf", "src")
        self.git("-c", "user.name=Artifact test", "-c", "user.email=artifact@example.invalid", "commit", "-qm", "fixture")
        self.out = self.root / ".scratch/artifact-store/pack"

    def tearDown(self):
        self.temporary.cleanup()

    def git(self, *args):
        subprocess.run(["git", *args], cwd=self.root, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    def pack(self, **kwargs):
        return store.pack(self.root, self.out, release="fixture-v1", **kwargs)

    def write_index(self, data):
        store._json(self.root / store.INDEX_PATH, data)

    def remove_originals(self):
        for relative in self.payloads:
            (self.root / relative).unlink()

    def malicious_archive(self, members):
        data = self.pack()
        target = self.out / "malicious.tar"
        with tarfile.open(target, "w", format=tarfile.PAX_FORMAT) as archive:
            for info, content in members:
                archive.addfile(info, io.BytesIO(content) if content is not None else None)
        with target.open("ab") as stream:
            stream.write(b"\0" * max(0, 30_720 - target.stat().st_size))
        digest = store._digest(target)
        archive = {"id": digest, "name": target.name, "sha256": digest,
                   "bytes": target.stat().st_size, "urls": ["https://example.org/malicious.tar"]}
        data["archives"] = [archive]
        for entry in data["artifacts"]:
            entry["archive"] = digest
        self.write_index(data)
        self.remove_originals()
        return data, target

    def test_inventory_selects_evidence_and_all_pdfs_but_preserves_product_assets(self):
        for relative in ("assets/logo.png", "src/sources/works/author/book/text.txt"):
            path = self.root / relative
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(b"ordinary retained input")
        self.git("add", "assets", "src")
        entries = store._inventory(self.root)
        self.assertEqual({e["path"] for e in entries}, self.payloads.keys())
        self.assertEqual(next(e for e in entries if e["path"] == self.source)["media_type"], "image/vnd.djvu")

    def test_pack_is_deterministic_bounded_and_self_contained(self):
        data = self.pack(max_archive_bytes=20_480)
        hashes = [item["sha256"] for item in data["archives"]]
        self.assertEqual(len(hashes), 2)
        self.assertTrue(all(item["bytes"] <= 20_480 for item in data["archives"]))
        self.assertEqual(hashes, [item["sha256"] for item in self.pack(max_archive_bytes=20_480)["archives"]])
        for archive in data["archives"]:
            path = self.out / archive["name"]
            self.assertEqual(store._digest(path), archive["sha256"])
            store._read_archive(path, [e for e in data["artifacts"] if e["archive"] == archive["id"]])
        self.assertTrue((self.out / "artifact-store.py").is_file())
        self.assertEqual(json.loads((self.out / "artifact-delivery.json").read_text()), data)
        self.assertTrue((self.out / "SHA256SUMS").is_file())
        self.assertEqual(self.manifest.read_text().count("source_url"), 1)

    def test_source_manifest_mismatch_refuses_preservation(self):
        (self.root / self.source).write_bytes(b"different bytes")
        with self.assertRaisesRegex(store.ArtifactStoreError, "disagrees"):
            self.pack()
        self.assertFalse((self.root / store.INDEX_PATH).exists())

    def test_impossible_chunk_bound_refuses_before_index_write(self):
        with self.assertRaisesRegex(store.ArtifactStoreError, "cannot fit"):
            self.pack(max_archive_bytes=10_240)
        self.assertFalse((self.root / store.INDEX_PATH).exists())

    def test_missing_bytes_resolve_without_network_is_explicit(self):
        self.pack()
        self.remove_originals()
        with patch.object(store, "urlopen", side_effect=AssertionError("network forbidden")):
            self.assertEqual(store.validate_index(self.root, local_bytes=True), [])
            with self.assertRaises(FileNotFoundError):
                store.resolve(self.root, self.source)
            with self.assertRaises(FileNotFoundError):
                store.hydrate(self.root, [self.source])

    def test_offline_hydration_preserves_bytes_in_cache_without_fake_originals(self):
        self.pack()
        self.remove_originals()
        with patch.object(store, "urlopen", side_effect=AssertionError("network forbidden")):
            paths = store.hydrate(self.root, list(self.payloads), archive_dir=self.out)
            self.assertEqual(len(paths), 2)
            for relative, expected in self.payloads.items():
                path = store.resolve(self.root, relative)
                self.assertIn(".scratch/artifact-cache/", str(path))
                self.assertEqual(path.read_bytes(), expected)
                self.assertFalse((self.root / relative).exists())
        self.assertEqual(store.validate_index(self.root, local_bytes=True), [])

    def test_inventory_retains_external_entries_after_git_removal(self):
        self.pack()
        self.git("rm", self.source, self.publication)
        self.assertEqual({e["path"] for e in store._inventory(self.root)}, self.payloads.keys())
        with self.assertRaises(FileNotFoundError):
            self.pack()
        self.assertEqual(len(store.delivery_entries(self.root)), 2)
        store.hydrate(self.root, list(self.payloads), archive_dir=self.out)
        self.assertEqual(len(self.pack()["artifacts"]), 2)

    def test_tampered_member_never_installs_partial_cache_file(self):
        info = tarfile.TarInfo(self.source)
        info.size = len(self.payloads[self.source])
        self.malicious_archive([(info, b"x" * info.size)])
        with self.assertRaisesRegex(store.ArtifactStoreError, "hash mismatch"):
            store.hydrate(self.root, [self.source], archive_dir=self.out)
        entry = store.known_external(self.root, self.source)
        self.assertFalse(store.cache_path(self.root, entry).exists())
        self.assertFalse(list((self.root / ".scratch/artifact-cache").rglob(".hydrate-*")))

    def test_original_tampering_fails_even_when_offline_archive_exists(self):
        self.pack()
        original = self.root / self.source
        original.write_bytes(b"x" * original.stat().st_size)
        with self.assertRaisesRegex(store.ArtifactStoreError, "mismatch"):
            store.resolve(self.root, self.source)
        self.assertTrue(store.validate_index(self.root, local_bytes=True))

    def test_cache_tampering_is_detected(self):
        self.pack()
        self.remove_originals()
        store.hydrate(self.root, [self.source], archive_dir=self.out)
        cached = store.resolve(self.root, self.source)
        cached.chmod(0o644)
        cached.write_bytes(b"corrupt cache")
        with self.assertRaisesRegex(store.ArtifactStoreError, "mismatch"):
            store.resolve(self.root, self.source)

    def test_archive_tampering_is_detected_before_hydration(self):
        data = self.pack()
        self.remove_originals()
        path = self.out / data["archives"][0]["name"]
        with path.open("r+b") as stream:
            stream.write(b"X")
        with self.assertRaisesRegex(store.ArtifactStoreError, "mismatch"):
            store.hydrate(self.root, list(self.payloads), archive_dir=self.out)
        self.assertFalse((self.root / ".scratch/artifact-cache").exists())

    def test_unknown_and_unsafe_paths_are_refused(self):
        self.pack()
        self.assertIsNone(store.known_external(self.root, "missing.pdf"))
        with self.assertRaises(FileNotFoundError):
            store.resolve(self.root, "missing.pdf")
        for relative in ("../escape.pdf", "/absolute.pdf", "a/../b.pdf", "a//b.pdf", "a/./b.pdf", "C:/escape.pdf", "a\\b.pdf"):
            with self.subTest(relative=relative), self.assertRaises(store.ArtifactStoreError):
                store.resolve(self.root, relative)

    def test_index_traversal_and_duplicate_entries_are_refused(self):
        original = self.pack()
        for bad in ("../escape.pdf", "/absolute.pdf", "a/../b.pdf"):
            data = copy.deepcopy(original)
            data["artifacts"][0]["path"] = data["artifacts"][0]["member"] = bad
            self.write_index(data)
            self.assertTrue(store.validate_index(self.root))
        data = copy.deepcopy(original)
        data["artifacts"].append(data["artifacts"][0])
        self.write_index(data)
        self.assertTrue(store.validate_index(self.root))

    def test_malformed_sidecar_is_not_treated_as_unknown_path(self):
        self.pack()
        (self.root / store.INDEX_PATH).write_text('{"schema":"bad"}', encoding="utf-8")
        with self.assertRaises(store.ArtifactStoreError):
            store.known_external(self.root, "not-declared.pdf")
        self.assertTrue(store.validate_index(self.root))

    def test_duplicate_json_keys_are_refused(self):
        self.pack()
        (self.root / store.INDEX_PATH).write_text('{"schema":"bad","schema":"bad"}', encoding="utf-8")
        self.assertIn("duplicate", store.validate_index(self.root)[0])

    def test_malformed_field_types_report_diagnostics(self):
        original = self.pack()
        for key in ("path", "sha256", "bytes", "kind", "media_type", "archive", "member"):
            data = copy.deepcopy(original)
            data["artifacts"][0][key] = []
            self.write_index(data)
            with self.subTest(key=key):
                self.assertTrue(store.validate_index(self.root))

    def test_malformed_url_reports_index_diagnostic(self):
        data = self.pack()
        data["archives"][0]["urls"] = ["https://[invalid"]
        self.write_index(data)
        self.assertTrue(store.validate_index(self.root))
        with self.assertRaises(store.ArtifactStoreError):
            store.load_index(self.root)

    def test_legacy_checkout_without_index_has_no_external_entries(self):
        self.assertEqual(store.delivery_entries(self.root), [])
        self.assertEqual(store.validate_index(self.root), [])
        self.assertIsNone(store.known_external(self.root, self.source))
        self.assertEqual(store.resolve(self.root, self.source), self.root / self.source)

    def test_symlinked_original_or_cache_parent_is_refused(self):
        data = self.pack()
        (self.root / self.source).unlink()
        (self.root / self.source).symlink_to(self.root / self.publication)
        with self.assertRaisesRegex(store.ArtifactStoreError, "symlinks"):
            store.resolve(self.root, self.source)
        (self.root / self.source).unlink()
        (self.root / ".scratch/artifact-cache").symlink_to(self.out)
        with self.assertRaisesRegex(store.ArtifactStoreError, "symlinks"):
            store.hydrate(self.root, [self.source], archive_dir=self.out)

    def test_tar_traversal_is_refused_without_writing_outside_cache(self):
        info = tarfile.TarInfo("../../escape.pdf")
        info.size = 3
        self.malicious_archive([(info, b"bad")])
        with self.assertRaisesRegex(store.ArtifactStoreError, "unsafe"):
            store.hydrate(self.root, list(self.payloads), archive_dir=self.out)
        self.assertFalse((self.root / "escape.pdf").exists())

    def test_symlink_hardlink_and_unexpected_tar_members_are_refused(self):
        for member_type in (tarfile.SYMTYPE, tarfile.LNKTYPE, tarfile.DIRTYPE):
            with self.subTest(member_type=member_type):
                info = tarfile.TarInfo(self.source)
                info.type = member_type
                info.linkname = "../../escape"
                self.malicious_archive([(info, None)])
                with self.assertRaisesRegex(store.ArtifactStoreError, "nonregular"):
                    store.hydrate(self.root, list(self.payloads), archive_dir=self.out)
                for relative, content in self.payloads.items():
                    (self.root / relative).write_bytes(content)

    def test_missing_archive_members_are_refused(self):
        data, archive = self.malicious_archive([])
        with self.assertRaisesRegex(store.ArtifactStoreError, "missing"):
            store._read_archive(archive, data["artifacts"])

    def test_explicit_fetch_verifies_before_caching(self):
        data = self.pack()
        self.remove_originals()
        body = (self.out / data["archives"][0]["name"]).read_bytes()
        with patch.object(store, "urlopen", return_value=io.BytesIO(body)) as fetch:
            path = store.resolve(self.root, self.source, fetch=True)
            self.assertEqual(path.read_bytes(), self.payloads[self.source])
            fetch.assert_called_once()
        self.assertFalse(list((self.root / ".scratch/artifact-cache").rglob(".download-*")))

    def test_oversized_download_does_not_install_an_archive(self):
        data = self.pack()
        self.remove_originals()
        body = (self.out / data["archives"][0]["name"]).read_bytes() + b"unexpected"
        with patch.object(store, "urlopen", return_value=io.BytesIO(body)):
            with self.assertRaisesRegex(store.ArtifactStoreError, "exceeds"):
                store.resolve(self.root, self.source, fetch=True)
        self.assertFalse(list((self.root / ".scratch/artifact-cache").rglob("*.tar")))

    def test_cli_default_check_does_not_require_or_fetch_bytes(self):
        self.pack()
        self.remove_originals()
        with patch.object(store, "urlopen", side_effect=AssertionError("network forbidden")):
            self.assertEqual(store.main(["check", "--root", str(self.root), "--json"]), 0)
            self.assertEqual(store.main(["check", "--root", str(self.root), "--require-local", "--json"]), 1)
            self.assertEqual(store.main(["check", "--root", str(self.root), "--archives", "--archive-dir", str(self.out), "--json"]), 0)


if __name__ == "__main__":
    unittest.main()
