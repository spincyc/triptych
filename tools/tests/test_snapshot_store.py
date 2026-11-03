"""Frozen release input delivery is exact, narrowly owned, and opt-in."""
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
import _artifact_store as transport
import _snapshot_store as store


class SnapshotStoreTests(unittest.TestCase):
    def setUp(self):
        scratch = ROOT / ".scratch/next-snapshot-store/tests"
        scratch.mkdir(parents=True, exist_ok=True)
        self.temporary = tempfile.TemporaryDirectory(dir=scratch)
        self.root = Path(self.temporary.name)
        contents = [
            (json.dumps({"schema": "example/v1", "revision": "1900", "documents": [
                {"id": "first", "text": "x" * 17_000}, {"id": "second", "text": "unaltered"}]}).encode() + b"\n", ".json"),
            (b'{"schema":"receipt/v1","status":"PASS"}\n', ".json"),
            (b'["whole", "array", {"number": 3}]\r\n', ".json"),
            (b'{"line":1}\n{"line":2}\n', ".jsonl"),
        ]
        self.payloads = {}
        for content, suffix in contents:
            digest = hashlib.sha256(content).hexdigest()
            relative = store.PREFIX + digest + suffix
            path = self.root / relative
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(content)
            self.payloads[relative] = content
        self.first = next(iter(self.payloads))
        self.ref = {"path": self.first, "sha256": hashlib.sha256(self.payloads[self.first]).hexdigest(),
                    "bytes": len(self.payloads[self.first]), "row_index": 1}
        self.release = {"schema": "example-release/v1", "source_plan": self.ref,
                        "documents": [{"manifest": self.ref}], "evidence": [self.ref]}
        self.release_path = self.root / store.RELEASE_PATH
        self.release_path.write_text(json.dumps(self.release), encoding="utf-8")
        self.binary = self.root / transport.INDEX_PATH
        self.binary.parent.mkdir(parents=True)
        self.binary.write_bytes(b"frozen binary index must not be touched\n")
        self.git("init", "-q")
        self.git("add", "release", "src")
        self.git("-c", "user.name=Snapshot test", "-c", "user.email=snapshot@example.invalid", "commit", "-qm", "fixture")
        self.out = self.root / ".scratch/packs"

    def tearDown(self):
        self.temporary.cleanup()

    def git(self, *args):
        subprocess.run(["git", *args], cwd=self.root, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    def pack(self, **kwargs):
        return store.pack(self.root, self.out, release="fixture-v1", **kwargs)

    def write_index(self, data):
        transport._json(self.root / store.INDEX_PATH, data)

    def remove_originals(self):
        for relative in self.payloads:
            (self.root / relative).unlink()

    def test_inventory_preserves_json_jsonl_array_and_unreferenced_snapshots(self):
        entries = store._inventory(self.root)
        self.assertEqual({entry["path"] for entry in entries}, self.payloads.keys())
        self.assertEqual(len(entries), 4)
        self.assertEqual({e["media_type"] for e in entries}, {"application/json", "application/x-ndjson"})

    def test_bounded_deterministic_pack_leaves_originals_and_binary_index_unchanged(self):
        binary = self.binary.read_bytes()
        release = self.release_path.read_bytes()
        data = self.pack(max_archive_bytes=20_480)
        self.assertGreater(len(data["archives"]), 1)
        self.assertTrue(all(a["bytes"] <= 20_480 for a in data["archives"]))
        self.assertEqual([a["sha256"] for a in data["archives"]],
                         [a["sha256"] for a in self.pack(max_archive_bytes=20_480)["archives"]])
        self.assertEqual(self.binary.read_bytes(), binary)
        self.assertEqual(self.release_path.read_bytes(), release)
        for relative, original in self.payloads.items():
            self.assertEqual((self.root / relative).read_bytes(), original)
        self.assertEqual(store.validate_index(self.root, local_bytes=True), [])

    def test_metadata_only_checks_never_read_snapshot_payloads_or_fetch(self):
        self.pack()
        self.remove_originals()
        with patch.object(transport, "_verify", side_effect=AssertionError("payload read")), \
             patch.object(transport, "urlopen", side_effect=AssertionError("network")):
            self.assertEqual(store.validate_index(self.root), [])
            self.assertEqual(store.validate_ref(self.root, self.ref)["sha256"], self.ref["sha256"])
            self.assertEqual(store.main(["check", "--root", str(self.root), "--json"]), 0)

    def test_metadata_acceptance_is_distinct_from_byte_access(self):
        self.pack()
        self.remove_originals()
        self.assertEqual(store.validate_index(self.root, local_bytes=True), [])
        with self.assertRaises(FileNotFoundError):
            store.validate_ref(self.root, self.ref, require_bytes=True)
        with self.assertRaises(FileNotFoundError):
            store.resolve(self.root, self.first)

    def test_reference_hash_or_size_mismatch_is_refused_without_hydration(self):
        self.pack()
        self.remove_originals()
        for replacement in ({"sha256": "f" * 64}, {"bytes": self.ref["bytes"] + 1}, {"bytes": True}):
            ref = dict(self.ref, **replacement)
            with self.subTest(replacement=replacement), self.assertRaises(store.SnapshotStoreError):
                store.validate_ref(self.root, ref)

    def test_release_reference_drift_is_rejected_by_metadata_gate(self):
        self.pack()
        release = copy.deepcopy(self.release)
        release["source_plan"]["bytes"] += 1
        self.release_path.write_text(json.dumps(release), encoding="utf-8")
        self.assertIn("mismatch", store.validate_index(self.root)[0])

    def test_undeclared_missing_ref_never_gets_metadata_acceptance(self):
        self.pack()
        ref = dict(self.ref, path=store.PREFIX + "f" * 64 + ".json", sha256="f" * 64)
        with self.assertRaises(store.SnapshotStoreError):
            store.validate_ref(self.root, ref)

    def test_unlisted_local_file_cannot_bypass_an_existing_index(self):
        self.pack()
        content = b'{"unlisted":"local"}\n'
        digest = hashlib.sha256(content).hexdigest()
        relative = store.PREFIX + digest + ".json"
        (self.root / relative).write_bytes(content)
        ref = {"path": relative, "sha256": digest, "bytes": len(content)}
        with self.assertRaisesRegex(store.SnapshotStoreError, "not declared"):
            store.validate_ref(self.root, ref)
        with self.assertRaisesRegex(store.SnapshotStoreError, "not declared"):
            store.resolve(self.root, relative)
        self.assertIn("unregistered", store.validate_index(self.root)[0])
        self.git("add", relative)
        self.assertEqual(len(self.pack()["artifacts"]), 5)

    def test_older_local_fixtures_are_verified_against_their_pins(self):
        self.assertIsNone(store.known_external(self.root, self.first))
        self.assertEqual(store.validate_ref(self.root, self.ref)["bytes"], self.ref["bytes"])
        with self.assertRaises(store.SnapshotStoreError):
            store.validate_ref(self.root, dict(self.ref, bytes=1))
        self.remove_originals()
        with self.assertRaises(FileNotFoundError):
            store.validate_ref(self.root, self.ref)

    def test_only_the_narrow_frozen_input_prefix_is_resolvable(self):
        self.pack()
        for relative in ("src/authored.json", "release/papal-documents/reports/a.json", "../escape.json",
                         store.PREFIX + "nested/file.json", store.PREFIX + "file.md",
                         store.PREFIX + "../escape.json", "/absolute.json"):
            with self.subTest(relative=relative), self.assertRaises(store.SnapshotStoreError):
                store.resolve(self.root, relative)

    def test_filename_and_scope_are_closed_in_the_index(self):
        original = self.pack()
        replacements = [
            {"path": "src/authored.json", "member": "src/authored.json"},
            {"path": store.PREFIX + "wrong.json", "member": store.PREFIX + "wrong.json"},
            {"kind": "source-evidence"}, {"media_type": "text/plain"},
            {"origin_url": "https://example.org/not-a-source-witness"},
        ]
        for replacement in replacements:
            data = copy.deepcopy(original)
            data["artifacts"][0].update(replacement)
            self.write_index(data)
            with self.subTest(replacement=replacement):
                self.assertTrue(store.validate_index(self.root))

    def test_unknown_authored_file_cannot_be_silently_packed(self):
        path = self.root / store.PREFIX / "authored.json"
        path.write_bytes(b"{}")
        self.git("add", str(path.relative_to(self.root)))
        with self.assertRaisesRegex(store.SnapshotStoreError, "filename"):
            self.pack()
        self.assertFalse((self.root / store.INDEX_PATH).exists())

    def test_offline_roundtrip_restores_all_exact_bytes_without_original_paths(self):
        self.pack()
        self.remove_originals()
        with patch.object(transport, "urlopen", side_effect=AssertionError("network")):
            store.hydrate(self.root, list(self.payloads), archive_dir=self.out)
            for relative, original in self.payloads.items():
                restored = store.resolve(self.root, relative)
                self.assertEqual(restored.read_bytes(), original)
                self.assertFalse((self.root / relative).exists())
            self.assertEqual(store.validate_ref(self.root, self.ref, require_bytes=True)["sha256"], self.ref["sha256"])

    def test_repack_never_loses_previous_declarations_after_git_removal(self):
        self.pack()
        self.git("rm", *self.payloads)
        self.assertEqual(len(store._inventory(self.root)), 4)
        with self.assertRaises(FileNotFoundError):
            self.pack()
        self.assertEqual(len(store.load_index(self.root)["artifacts"]), 4)
        store.hydrate(self.root, list(self.payloads), archive_dir=self.out)
        self.assertEqual(len(self.pack()["artifacts"]), 4)

    def test_append_ignored_snapshot_preserves_prior_and_unreferenced_declarations(self):
        self.pack()
        self.git("rm", *self.payloads)
        store.hydrate(self.root, list(self.payloads), archive_dir=self.out)
        (self.root / ".gitignore").write_text(store.PREFIX + "\n", encoding="utf-8")
        content = b'{"new":1}\n{"new":2}\n'
        digest = hashlib.sha256(content).hexdigest()
        relative = store.PREFIX + digest + ".jsonl"
        (self.root / relative).parent.mkdir(parents=True, exist_ok=True)
        (self.root / relative).write_bytes(content)
        self.git("check-ignore", "--quiet", relative)
        self.assertEqual(subprocess.check_output(["git", "ls-files", "--", relative], cwd=self.root), b"")
        ref = {"path": relative, "sha256": digest, "bytes": len(content)}
        release = copy.deepcopy(self.release)
        release["evidence"].append(ref)
        self.release_path.write_text(json.dumps(release), encoding="utf-8")
        self.assertEqual({entry["path"] for entry in store._inventory(self.root)}, {*self.payloads, relative})
        data = self.pack()
        self.assertEqual({entry["path"] for entry in data["artifacts"]}, {*self.payloads, relative})
        self.assertEqual(store.validate_index(self.root, local_bytes=True), [])
        self.assertEqual(store.resolve(self.root, relative).read_bytes(), content)

    def test_new_unpreserved_release_reference_cannot_overwrite_existing_index(self):
        self.pack()
        before = (self.root / store.INDEX_PATH).read_bytes()
        release = copy.deepcopy(self.release)
        release["evidence"].append({"path": store.PREFIX + "f" * 64 + ".json", "sha256": "f" * 64, "bytes": 12})
        self.release_path.write_text(json.dumps(release), encoding="utf-8")
        with self.assertRaisesRegex(store.SnapshotStoreError, "not preserved"):
            self.pack()
        self.assertEqual((self.root / store.INDEX_PATH).read_bytes(), before)

    def test_inventory_refuses_untracked_symlinks_and_nonregular_entries(self):
        link = self.root / store.PREFIX / ("f" * 64 + ".json")
        link.symlink_to(self.release_path)
        with self.assertRaisesRegex(store.SnapshotStoreError, "nonregular"):
            store._inventory(self.root)
        link.unlink()
        link.mkdir()
        with self.assertRaisesRegex(store.SnapshotStoreError, "nonregular"):
            store._inventory(self.root)

    def test_local_and_cache_tampering_are_detected(self):
        self.pack()
        original = self.root / self.first
        original.write_bytes(b"x" * len(self.payloads[self.first]))
        self.assertEqual(store.validate_index(self.root), [])  # metadata does not claim byte replay
        self.assertTrue(store.validate_index(self.root, local_bytes=True))
        with self.assertRaises(store.SnapshotStoreError):
            store.resolve(self.root, self.first)
        self.remove_originals()
        store.hydrate(self.root, [self.first], archive_dir=self.out)
        cached = store.resolve(self.root, self.first)
        cached.chmod(0o644)
        cached.write_bytes(b"bad cache")
        with self.assertRaises(store.SnapshotStoreError):
            store.resolve(self.root, self.first)

    def test_tampered_archive_is_rejected_before_cache_creation(self):
        data = self.pack()
        self.remove_originals()
        path = self.out / data["archives"][0]["name"]
        with path.open("r+b") as stream:
            stream.write(b"X")
        with self.assertRaises(store.SnapshotStoreError):
            store.hydrate(self.root, list(self.payloads), archive_dir=self.out)
        self.assertFalse((self.root / ".scratch/artifact-cache").exists())

    def test_malformed_and_duplicate_key_indexes_are_not_missing_indexes(self):
        self.pack()
        for bad in ('{"schema":"wrong"}', '{"schema":"wrong","schema":"wrong"}'):
            (self.root / store.INDEX_PATH).write_text(bad, encoding="utf-8")
            with self.assertRaises(store.SnapshotStoreError):
                store.known_external(self.root, self.first)
            self.assertTrue(store.validate_index(self.root))

    def test_symlink_original_and_cache_parents_are_refused(self):
        self.pack()
        original = self.root / self.first
        original.unlink()
        original.symlink_to(self.release_path)
        with self.assertRaises(store.SnapshotStoreError):
            store.resolve(self.root, self.first)
        original.unlink()
        (self.root / ".scratch/artifact-cache").symlink_to(self.out)
        with self.assertRaises(store.SnapshotStoreError):
            store.hydrate(self.root, [self.first], archive_dir=self.out)

    def _malicious_archive(self, info, payload):
        data = self.pack()
        archive = self.out / "malicious.tar"
        with tarfile.open(archive, "w") as stream:
            stream.addfile(info, io.BytesIO(payload) if payload is not None else None)
        with archive.open("ab") as stream:
            stream.write(b"\0" * max(0, 30_720 - archive.stat().st_size))
        digest = transport._digest(archive)
        data["archives"] = [{"id": digest, "sha256": digest, "name": archive.name,
                            "bytes": archive.stat().st_size, "urls": ["https://example.org/malicious.tar"]}]
        for entry in data["artifacts"]:
            entry["archive"] = digest
        self.write_index(data)
        self.remove_originals()

    def test_archive_traversal_is_refused(self):
        info = tarfile.TarInfo("../../escape.json")
        info.size = 2
        self._malicious_archive(info, b"{}")
        with self.assertRaisesRegex(store.SnapshotStoreError, "unsafe"):
            store.hydrate(self.root, list(self.payloads), archive_dir=self.out)
        self.assertFalse((self.root / "escape.json").exists())

    def test_archive_links_are_refused(self):
        info = tarfile.TarInfo(self.first)
        info.type = tarfile.SYMTYPE
        info.linkname = "../../escape.json"
        self._malicious_archive(info, None)
        with self.assertRaisesRegex(store.SnapshotStoreError, "nonregular"):
            store.hydrate(self.root, list(self.payloads), archive_dir=self.out)

    def test_member_hash_mismatch_never_installs_partial_file(self):
        info = tarfile.TarInfo(self.first)
        info.size = len(self.payloads[self.first])
        self._malicious_archive(info, b"x" * info.size)
        with self.assertRaisesRegex(store.SnapshotStoreError, "hash mismatch"):
            store.hydrate(self.root, [self.first], archive_dir=self.out)
        self.assertFalse(store.cache_path(self.root, store.known_external(self.root, self.first)).exists())
        self.assertFalse(list((self.root / ".scratch/artifact-cache").rglob(".hydrate-*")))

    def test_fetch_is_explicit_and_hash_verified(self):
        data = self.pack()
        self.remove_originals()
        body = (self.out / data["archives"][0]["name"]).read_bytes()
        with patch.object(transport, "urlopen", return_value=io.BytesIO(body)) as fetch:
            result = store.resolve(self.root, self.first, fetch=True)
            self.assertEqual(result.read_bytes(), self.payloads[self.first])
            fetch.assert_called_once()

    def test_portable_pack_contains_both_stdlib_only_python_dependencies(self):
        data = self.pack()
        clone = self.root / ".scratch/offline-clone"
        transport._json(clone / store.INDEX_PATH, data)
        command = [sys.executable, str(self.out / "snapshot-store.py")]
        for args in (["check", "--archives"], ["hydrate", "--all"], ["check", "--require-local"]):
            run = subprocess.run([*command, *args, "--root", str(clone), "--archive-dir", str(self.out), "--json"],
                                 cwd=clone, capture_output=True, text=True)
            self.assertEqual(run.returncode, 0, run.stderr + run.stdout)
        for relative, content in self.payloads.items():
            self.assertEqual(store.resolve(clone, relative).read_bytes(), content)
        self.assertEqual((self.out / "_artifact_store.py").read_bytes(), Path(transport.__file__).read_bytes())

    def test_bad_archive_template_refuses_before_writing(self):
        for template in ("http://example.org/{archive}", "https://example.org/{unknown}", "https://user:secret@example.org/{archive}"):
            with self.subTest(template=template), self.assertRaises(store.SnapshotStoreError):
                self.pack(url_template=template)
        self.assertFalse((self.root / store.INDEX_PATH).exists())


if __name__ == "__main__":
    unittest.main()
