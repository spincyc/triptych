#!/usr/bin/env python3
"""Safe file reads, replacements and external identities fail closed."""
from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import sys
import tempfile
import unittest
from unittest import mock

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))
import _safe_files as safe_files


class SafeFileTests(unittest.TestCase):
    def setUp(self):
        scratch = ROOT / ".scratch/safe-files-tests"
        scratch.mkdir(parents=True, exist_ok=True)
        self.temporary = tempfile.TemporaryDirectory(dir=scratch, prefix="test-")
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.source = "src/sources/works/example/work/work.toml"
        self.write(self.source, "source identity and rights\n")

    def write(self, name, value):
        path = self.root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(value, encoding="utf-8")
        return path

    def test_read_refuses_symlinked_file_or_parent(self):
        source = self.root / self.source
        outside = self.write("outside.txt", "redirected")
        source.unlink()
        source.symlink_to(outside)
        with self.assertRaises(safe_files.SafeFileError):
            safe_files.read_file(self.root, self.source)
        source.unlink()
        source.write_text("source identity and rights\n")
        parent = source.parent
        retained = parent.with_name("retained")
        parent.rename(retained)
        parent.symlink_to(retained, target_is_directory=True)
        with self.assertRaises(safe_files.SafeFileError):
            safe_files.read_file(self.root, self.source)

    def test_read_refuses_ancestor_exchange_during_read(self):
        source = self.root / self.source
        parent = source.parent
        retained = parent.with_name("retained")
        real_read = os.read
        swapped = False

        def swap(descriptor, size):
            nonlocal swapped
            if not swapped:
                swapped = True
                parent.rename(retained)
                parent.mkdir()
                (parent / source.name).write_text("substituted source")
            return real_read(descriptor, size)

        with mock.patch.object(safe_files.os, "read", side_effect=swap), \
                self.assertRaisesRegex(safe_files.SafeFileError, "changed during operation"):
            safe_files.read_file(self.root, self.source)

    def test_atomic_write_refuses_existing_symlink_or_hardlink(self):
        name = "release/descriptor.json"
        destination = self.root / name
        destination.parent.mkdir(parents=True)
        outside = self.write("outside.txt", "preserved")
        scratch = self.root / ".scratch/writes"
        destination.symlink_to(outside)
        with self.assertRaises(safe_files.SafeFileError):
            safe_files.atomic_write(self.root, name, b"new", scratch=scratch)
        destination.unlink()
        os.link(outside, destination)
        with self.assertRaises(safe_files.SafeFileError):
            safe_files.atomic_write(self.root, name, b"new", scratch=scratch)
        self.assertEqual(outside.read_text(), "preserved")
        destination.unlink()
        safe_files.atomic_write(self.root, name, b"new", scratch=scratch)
        self.assertEqual(destination.read_bytes(), b"new")
        self.assertEqual(list(scratch.iterdir()), [])

    def external_binary(self):
        name = "src/sources/works/example/work/editions/1900/artifacts/scan/witness.pdf"
        digest = hashlib.sha256(b"exact retained witness").hexdigest()
        manifest_name = str(Path(name).parent / "artifact.toml")
        manifest = {"schema": 1, "record_type": "artifact", "id": "artifact.example.scan",
                    "storage": "tracked", "rights_status": "public-domain",
                    "media_type": "application/pdf", "path": name,
                    "sha256": digest, "byte_size": 22}
        self.write(manifest_name, "\n".join(f"{key} = {json.dumps(value)}" for key, value in manifest.items()))
        archive_hash = "a" * 64
        sidecar = {"schema": "triptych-artifact-delivery/v1",
                   "archives": [{"id": archive_hash, "name": "witnesses.tar", "sha256": archive_hash,
                                 "bytes": 10240, "urls": ["https://example.org/witnesses.tar"]}],
                   "artifacts": [{"path": name, "member": name, "sha256": digest,
                                  "bytes": 22, "kind": "source-evidence",
                                  "media_type": "application/pdf", "archive": archive_hash}]}
        self.write("src/sources/artifact-delivery.json", json.dumps(sidecar))
        names = {"src/sources/artifact-delivery.json", manifest_name}
        return name, manifest_name, digest, names

    def test_exact_delivery_and_manifest_identify_unhydrated_binary(self):
        name, manifest_name, digest, names = self.external_binary()
        expected = {name: {"manifest": manifest_name, "sha256": digest, "bytes": 22}}
        self.assertFalse((self.root / name).exists())
        self.assertEqual(expected, safe_files._external_identities(self.root, names))
        self.write(name, "local hydration is not part of the logical identity")
        self.assertEqual(expected, safe_files._external_identities(self.root, names))
        self.assertEqual({}, safe_files._external_identities(self.root, {manifest_name}))

    def test_external_manifest_sidecar_mismatch_is_not_accepted(self):
        _, manifest_name, _, names = self.external_binary()
        path = self.root / manifest_name
        path.write_text(path.read_text().replace('byte_size = 22', 'byte_size = 23'))
        with self.assertRaisesRegex(safe_files.SafeFileError, "differs from delivery"):
            safe_files._external_identities(self.root, names)

    def test_external_payload_without_its_manifest_is_not_accepted(self):
        _, manifest_name, _, names = self.external_binary()
        with self.assertRaisesRegex(safe_files.SafeFileError, "exact binary artifact manifest"):
            safe_files._external_identities(self.root, names - {manifest_name})


if __name__ == "__main__":
    unittest.main()
