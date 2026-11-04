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

    def extra_source(self):
        relative = "src/sources/works/author/second/editions/1901-print/artifacts/pages/source.pdf"
        content = b"%PDF-1.4\nexact focused evidence\n" * 400
        target = self.root / relative
        target.parent.mkdir(parents=True)
        target.write_bytes(content)
        manifest = target.with_name("artifact.toml")
        manifest.write_text(
            f'path = "{relative}"\nsha256 = "{hashlib.sha256(content).hexdigest()}"\n'
            f'byte_size = {len(content)}\nmedia_type = "application/pdf"\n', encoding="utf-8")
        self.git("add", relative, str(manifest.relative_to(self.root)))
        return relative, content, manifest

    def append_offline(self, paths, **kwargs):
        return store.pack(self.root, self.out / "addition", release="local-evidence",
                          paths=paths, append=True, offline_only=True, **kwargs)

    def test_scoped_append_preserves_legacy_records_without_resolving_old_bytes(self):
        previous = self.pack()
        self.remove_originals()
        relative, content, manifest = self.extra_source()
        manifest_before = manifest.read_bytes()
        resolve = store.resolve
        def selected_only(root, path, **kwargs):
            self.assertEqual(path, relative)
            return resolve(root, path, **kwargs)
        with patch.object(store, "resolve", side_effect=selected_only), patch.object(
                store, "urlopen", side_effect=AssertionError("network forbidden")):
            data = self.append_offline([relative])
        self.assertEqual(data["snapshot"], previous["snapshot"])
        self.assertEqual(data["archives"][:-1], previous["archives"])
        self.assertEqual(data["artifacts"][:-1], previous["artifacts"])
        self.assertEqual(data["archives"][-1]["delivery"], "offline-only")
        self.assertEqual(data["archives"][-1]["urls"], [])
        self.assertEqual(data["artifacts"][-1]["sha256"], hashlib.sha256(content).hexdigest())
        self.assertEqual(manifest.read_bytes(), manifest_before)
        self.assertEqual(store.validate_index(self.root), [])

    def test_offline_append_hydrates_exact_bytes_without_network_or_original(self):
        self.pack()
        relative, content, _ = self.extra_source()
        data = self.append_offline([relative])
        (self.root / relative).unlink()
        with patch.object(store, "urlopen", side_effect=AssertionError("network forbidden")):
            with self.assertRaisesRegex(FileNotFoundError, "offline-only"):
                store.hydrate(self.root, [relative], fetch=True)
            self.assertEqual(store.validate_index(self.root), [])
            paths = store.hydrate(self.root, [relative], archive_dir=self.out / "addition")
            self.assertEqual(paths[0].read_bytes(), content)
            self.assertFalse((self.root / relative).exists())
        self.assertEqual(store.validate_index(self.root, local_bytes=True), [])
        archive = data["archives"][-1]
        self.assertEqual(store._digest(self.out / "addition" / archive["name"]), archive["sha256"])

    def test_repeated_scoped_append_keeps_index_archive_and_checksums_identical(self):
        self.pack()
        relative, _, _ = self.extra_source()
        first = self.append_offline([relative])
        addition = self.out / "addition"
        before = {path.name: path.read_bytes() for path in addition.iterdir() if path.is_file()}
        self.assertEqual(self.append_offline([relative]), first)
        self.assertEqual({path.name: path.read_bytes() for path in addition.iterdir() if path.is_file()}, before)

    def test_offline_state_is_explicit_and_cannot_advertise_a_route(self):
        original = self.pack()
        for update, message in (({"urls": []}, "at least one"),
                                ({"delivery": "offline-only"}, "must not advertise"),
                                ({"delivery": "future-upload", "urls": []}, "unknown archive")):
            data = copy.deepcopy(original)
            data["archives"][0].update(update)
            self.write_index(data)
            self.assertIn(message, store.validate_index(self.root)[0])

    def test_scoped_append_requires_explicit_complete_selection(self):
        original = self.pack()
        relative, _, _ = self.extra_source()
        for options in ({"append": True}, {"offline_only": True}, {"paths": [relative]},
                        {"append": True, "offline_only": True}):
            with self.subTest(options=options), self.assertRaisesRegex(store.ArtifactStoreError, "requires"):
                store.pack(self.root, self.out / "refused", release="local", **options)
            self.assertEqual(store.load_index(self.root), original)
        for selected in (["src/sources/works/untracked/source.pdf"], ["../escape.pdf"],
                         [self.publication], [str(self.manifest.relative_to(self.root))]):
            with self.subTest(selected=selected), self.assertRaises(store.ArtifactStoreError):
                self.append_offline(selected)
            self.assertEqual(store.load_index(self.root), original)

    def test_scoped_append_refuses_changed_or_missing_source_before_index_change(self):
        original = self.pack()
        relative, content, _ = self.extra_source()
        target = self.root / relative
        target.write_bytes(content + b"changed")
        with self.assertRaisesRegex(store.ArtifactStoreError, "disagrees"):
            self.append_offline([relative])
        self.assertEqual(store.load_index(self.root), original)
        target.unlink()
        with self.assertRaisesRegex(store.ArtifactStoreError, "missing tracked binary"):
            self.append_offline([relative])
        self.assertEqual(store.load_index(self.root), original)

    def test_scoped_append_checks_selected_existing_artifact_bytes(self):
        self.pack()
        relative, _, _ = self.extra_source()
        original = self.append_offline([relative])
        (self.root / relative).write_bytes(b"tampered")
        with self.assertRaisesRegex(store.ArtifactStoreError, "mismatch"):
            self.append_offline([relative])
        self.assertEqual(store.load_index(self.root), original)

    def test_cli_scoped_append_creates_only_selected_offline_addition(self):
        original = self.pack()
        relative, _, _ = self.extra_source()
        self.assertEqual(store.main(["pack", "--root", str(self.root), "--out", str(self.out / "cli"),
                                     "--release", "local-evidence", "--append", "--offline-only",
                                     "--path", relative, "--json"]), 0)
        data = store.load_index(self.root)
        self.assertEqual(data["archives"][:-1], original["archives"])
        self.assertEqual([entry["path"] for entry in data["artifacts"][len(original["artifacts"]):]], [relative])

    def test_shared_validator_requires_domain_opt_in_for_offline_archives(self):
        import _snapshot_store as snapshots

        self.pack()
        relative, _, _ = self.extra_source()
        source_index = self.append_offline([relative])
        store._validate(source_index)
        with self.assertRaisesRegex(store.ArtifactStoreError, "archive fields"):
            store.validate_delivery_index(source_index)
        store.validate_delivery_index(source_index, allow_offline=True)

        original_index = (self.root / store.INDEX_PATH).read_bytes()
        content = b'{"historical":"unchanged"}\n'
        digest = hashlib.sha256(content).hexdigest()
        path = self.root / snapshots.PREFIX / (digest + ".json")
        path.parent.mkdir(parents=True)
        path.write_bytes(content)
        snapshot_index = snapshots.pack(self.root, self.out / "snapshots", release="snapshot-fixture")
        snapshots._validate(snapshot_index)
        self.assertEqual((self.root / store.INDEX_PATH).read_bytes(), original_index)
        snapshot_index["archives"][0].update(delivery="offline-only", urls=[])
        with self.assertRaisesRegex(store.ArtifactStoreError, "archive fields"):
            snapshots._validate(snapshot_index)

    def test_shared_packer_defaults_public_and_validates_before_writing(self):
        entries = store._inventory(self.root)
        target = self.out / "shared"
        with self.assertRaisesRegex(store.ArtifactStoreError, "URL template"):
            store.pack_delivery_archives(self.root, target, entries, resolver=store.resolve,
                                         release="fixture", url_template="http://example.org/{archive}")
        self.assertFalse(target.exists())
        with self.assertRaisesRegex(store.ArtifactStoreError, "positive integer"):
            store.pack_delivery_archives(self.root, target, entries, resolver=store.resolve,
                                         release="fixture", start_ordinal=0)
        self.assertFalse(target.exists())
        archives, packed = store.pack_delivery_archives(
            self.root, target, entries, resolver=store.resolve, release="fixture")
        self.assertNotIn("delivery", archives[0])
        self.assertTrue(archives[0]["urls"])
        self.assertTrue(archives[0]["name"].startswith("triptych-binaries-0001-"))
        self.assertEqual({entry["path"] for entry in packed}, self.payloads.keys())
        self.assertFalse((self.root / store.INDEX_PATH).exists())

    def test_scoped_append_keeps_archive_ordinal_with_shared_packer(self):
        previous = self.pack()
        relative, _, _ = self.extra_source()
        data = self.append_offline([relative])
        expected = len(previous["archives"]) + 1
        self.assertTrue(data["archives"][-1]["name"].startswith(f"triptych-binaries-{expected:04d}-"))


class GitHistoryDeliveryTests(unittest.TestCase):
    """A committed JSON inventory replaces its tracked copy by exact reference."""

    def setUp(self):
        scratch = ROOT / ".scratch/artifact-store/tests"
        scratch.mkdir(parents=True, exist_ok=True)
        self.temporary = tempfile.TemporaryDirectory(dir=scratch)
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.path = "src/sources/works/project/inputs/editions/snapshot/artifacts/input/frozen-inventory.json"
        self.payload = (json.dumps({"affected_units": [{"unit_id": "a"}, {"unit_id": "b"}], "documents": [],
                                    "revision": "2026-10-26T16:11:07Z"}, indent=2, sort_keys=True) + "\n").encode()
        target = self.root / self.path
        target.parent.mkdir(parents=True)
        target.write_bytes(self.payload)
        self.git("init", "-q")
        self.git("add", "src")
        self.git("-c", "user.name=Artifact test", "-c", "user.email=artifact@example.invalid", "commit", "-qm", "snapshot")
        self.commit = subprocess.run(["git", "rev-parse", "HEAD"], cwd=self.root, check=True, text=True,
                                     stdout=subprocess.PIPE).stdout.strip()
        self.git("rm", "-q", self.path)
        self.git("-c", "user.name=Artifact test", "-c", "user.email=artifact@example.invalid", "commit", "-qm", "reference")
        self.entry = {"path": self.path, "sha256": hashlib.sha256(self.payload).hexdigest(),
                      "bytes": len(self.payload), "kind": "source-evidence", "media_type": "application/json",
                      "git_commit": self.commit, "items": {"affected_units": 2, "documents": 0}}
        self.write_index([self.entry])

    def git(self, *args):
        subprocess.run(["git", *args], cwd=self.root, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    def write_index(self, entries):
        store._json(self.root / store.INDEX_PATH, {"schema": store.SCHEMA, "archives": [], "artifacts": entries})

    def test_reference_resolves_offline_to_exact_bytes(self):
        self.assertFalse((self.root / self.path).exists())
        with patch.object(store, "urlopen", side_effect=AssertionError("network forbidden")):
            resolved = store.resolve(self.root, self.path)
        self.assertIn(".scratch/artifact-cache/", str(resolved))
        self.assertEqual(resolved.read_bytes(), self.payload)
        self.assertEqual(store.hydrate(self.root, [self.path]), [resolved])
        self.assertEqual(store.validate_index(self.root, local_bytes=True), [])

    def test_tampered_reference_fails_and_installs_nothing(self):
        cases = {"sha256": dict(self.entry, sha256="0" * 64),
                 "bytes": dict(self.entry, bytes=self.entry["bytes"] + 1),
                 "items": dict(self.entry, items={"affected_units": 3, "documents": 0}),
                 "commit": dict(self.entry, git_commit="1" * 40),
                 "path": dict(self.entry, path=self.path.replace("frozen-inventory", "other"))}
        for name, entry in cases.items():
            with self.subTest(name=name):
                self.write_index([entry])
                with self.assertRaises((store.ArtifactStoreError, FileNotFoundError)):
                    store.resolve(self.root, entry["path"])
                self.assertFalse((self.root / ".scratch/artifact-cache").exists())

    def test_reference_requires_full_commit_counts_and_json(self):
        for change in ({"git_commit": "HEAD"}, {"git_commit": self.commit[:12]}, {"items": {}},
                       {"items": {"affected_units": -1}}, {"media_type": "application/pdf"},
                       {"archive": "a" * 64}, {"derivation": {"projection_of": self.path, "git_commit": self.commit,
                                                              "sha256": "a" * 64, "input_history": 0}}):
            with self.subTest(change=change):
                self.write_index([dict(self.entry, **change)])
                with self.assertRaises(store.ArtifactStoreError):
                    store.load_index(self.root)
        domain = {"schema": store.SCHEMA, "archives": [], "artifacts": [self.entry]}
        with self.assertRaises(store.ArtifactStoreError):
            store.validate_delivery_index(domain)

    def test_pack_never_repacks_a_git_reference(self):
        data = store.pack(self.root, self.root / ".scratch/pack", release="fixture-v1")
        self.assertEqual(data["archives"], [])
        self.assertEqual(data["artifacts"], [self.entry])


if __name__ == "__main__":
    unittest.main()
