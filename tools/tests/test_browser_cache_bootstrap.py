"""Untrusted bootstrap archives never supply authority or repair existing data."""
from __future__ import annotations

import copy
import gzip
import hashlib
import io
import json
import os
from pathlib import Path
import sys
import tarfile
import tempfile
import unittest
from unittest import mock

import yaml

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))
import _browser_cache_bootstrap as bootstrap
import _install_web_print_pandoc as pandoc


class BrowserCacheBootstrapTests(unittest.TestCase):
    def setUp(self):
        scratch = ROOT / ".scratch/cache-bootstrap-fix"
        scratch.mkdir(parents=True, exist_ok=True)
        temporary = tempfile.TemporaryDirectory(prefix="test-", dir=scratch)
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        self.archive = self.root / "pack.tar.gz"
        self.metadata = self.root / "bootstrap.json"
        self.cache = self.root / "cache"
        self.key = "a" * 64
        self.other_key = "b" * 64
        self.files = {self.key: {"structure/example.json": b'{"example":true}\n'},
                      self.other_key: {"structure/other.json": b'{"other":true}\n'}}

    def members(self, files=None):
        files = self.files if files is None else files
        index = {"schema": bootstrap.products.CANDIDATE_SCHEMA, "entries": {}}
        for key, rows in files.items():
            identities = {name: {"sha256": hashlib.sha256(body).hexdigest(), "bytes": len(body)}
                          for name, body in rows.items()}
            index["entries"][key] = bootstrap.products.candidate_hint(identities)
        members = [(bootstrap.MARKER, b""),
                   (bootstrap.products.CANDIDATE_INDEX, json.dumps(index, sort_keys=True).encode())]
        return members + [(key + "/data/" + name, body) for key, rows in files.items() for name, body in rows.items()]

    def pack(self, members=None, *, special=None, pax=None, raw=None):
        members = self.members() if members is None else members
        if raw is None:
            output = io.BytesIO()
            with tarfile.open(fileobj=output, mode="w", format=tarfile.PAX_FORMAT) as archive:
                for name, body in members:
                    info = tarfile.TarInfo(name)
                    info.size, info.mode, info.mtime = len(body), 0o644, 0
                    if pax and name == members[-1][0]:
                        info.pax_headers = pax
                    archive.addfile(info, io.BytesIO(body))
                if special:
                    info = tarfile.TarInfo(special[0])
                    info.type = special[1]
                    info.linkname = "outside" if info.islnk() or info.issym() else ""
                    archive.addfile(info)
            raw = output.getvalue()
        body = gzip.compress(raw, mtime=0)
        self.archive.write_bytes(body)
        declaration = {"schema": bootstrap.SCHEMA, "archive": {
            "url": "https://github.com/example/artifacts/releases/download/candidates-v1/pack.tar.gz",
            "sha256": hashlib.sha256(body).hexdigest(), "bytes": len(body),
            "unpacked_bytes": sum(len(payload) for _, payload in members)}}
        self.metadata.write_text(json.dumps(declaration))
        return declaration

    def run_bootstrap(self):
        return bootstrap.bootstrap(self.root, self.metadata, cache_root=self.cache, archive=self.archive)

    def rejected(self):
        with self.assertRaises((bootstrap.BootstrapError, bootstrap.products.ProductError, OSError, EOFError, tarfile.TarError)):
            self.run_bootstrap()
        self.assertFalse(self.cache.exists(), "invalid archive must not create a destination cache")

    def test_valid_pack_merges_complete_entries_and_only_typed_root_metadata(self):
        self.pack()
        with mock.patch.object(bootstrap, "download", side_effect=AssertionError("local import must not fetch")):
            result = self.run_bootstrap()
        self.assertEqual((result["added"], result["files"]), (2, 2))
        self.assertEqual(set(p.name for p in self.cache.iterdir()),
                         {self.key, self.other_key, bootstrap.MARKER, bootstrap.products.CANDIDATE_INDEX})
        index = bootstrap.products.load_candidate_index(self.cache)
        for key, hint in index["entries"].items():
            bootstrap.products.validate_candidate_entry(self.cache, key, hint)

    def test_long_pax_paths_are_safe_and_supported(self):
        name = "structure/" + "x" * 220 + ".json"
        self.pack(self.members({self.key: {name: b"{}\n"}}))
        self.assertEqual(self.run_bootstrap()["added"], 1)
        self.assertEqual((self.cache / self.key / "data" / name).read_bytes(), b"{}\n")

    def test_valid_existing_entries_keep_their_original_inodes_and_bytes(self):
        self.pack()
        self.run_bootstrap()
        path = self.cache / self.key / "data/structure/example.json"
        original = path.stat().st_ino, path.read_bytes()
        result = self.run_bootstrap()
        self.assertEqual((result["added"], result["preserved"]), (0, 2))
        self.assertEqual((path.stat().st_ino, path.read_bytes()), original)

    def test_corrupt_or_empty_existing_entries_are_not_repaired(self):
        for empty in (False, True):
            with self.subTest(empty=empty):
                self.pack()
                entry = self.cache / self.key
                entry.mkdir(parents=True)
                target = entry / "data/structure/example.json"
                if not empty:
                    target.parent.mkdir(parents=True)
                    target.write_bytes(b"corrupt")
                with self.assertRaises((bootstrap.BootstrapError, bootstrap.products.ProductError, OSError)):
                    self.run_bootstrap()
                self.assertFalse((self.cache / self.other_key).exists())
                if not empty:
                    self.assertEqual(target.read_bytes(), b"corrupt")
                import shutil
                shutil.rmtree(self.cache)

    def test_existing_index_contradictions_and_links_fail_without_repair(self):
        self.pack()
        self.run_bootstrap()
        index_path = self.cache / bootstrap.products.CANDIDATE_INDEX
        original = index_path.read_bytes()
        index = json.loads(original)
        index["entries"][self.key]["bytes"] += 1
        index_path.write_text(json.dumps(index))
        with self.assertRaises(bootstrap.BootstrapError):
            self.run_bootstrap()
        self.assertEqual(json.loads(index_path.read_text()), index)
        index_path.unlink()
        outside = self.root / "outside.json"
        outside.write_bytes(original)
        index_path.symlink_to(outside)
        with self.assertRaises((bootstrap.products.ProductError, OSError)):
            self.run_bootstrap()
        self.assertEqual(outside.read_bytes(), original)

    def test_atomic_promotion_never_replaces_even_an_empty_directory(self):
        source, destination = self.root / "source", self.root / "destination"
        (source / self.key).mkdir(parents=True)
        (destination / self.key).mkdir(parents=True)
        (source / self.key / "test").write_text("candidate")
        src = os.open(source, os.O_RDONLY | os.O_DIRECTORY)
        dst = os.open(destination, os.O_RDONLY | os.O_DIRECTORY)
        try:
            with self.assertRaises(FileExistsError):
                bootstrap._rename_absent(src, dst, self.key)
        finally:
            os.close(src)
            os.close(dst)
        self.assertEqual(list((destination / self.key).iterdir()), [])
        self.assertTrue((source / self.key / "test").is_file())

    def test_links_directories_and_special_members_are_rejected(self):
        for kind in (tarfile.SYMTYPE, tarfile.LNKTYPE, tarfile.DIRTYPE, tarfile.FIFOTYPE, tarfile.CHRTYPE, tarfile.GNUTYPE_SPARSE):
            with self.subTest(kind=kind):
                self.pack(special=(self.key + "/data/unsafe.json", kind))
                self.rejected()

    def test_traversal_absolute_and_noncanonical_member_paths_are_rejected(self):
        for name in ("../escaped.json", "/tmp/escaped.json", self.key + "/data/../escaped.json",
                     self.key + "/data//escaped.json", self.key + "/data/./escaped.json", self.key + "\\data\\escaped.json",
                     self.key + "/other/escaped.json", "not-a-key/data/escaped.json"):
            with self.subTest(name=name):
                self.pack(self.members() + [(name, b"{}")])
                self.rejected()
        self.assertFalse((self.root / "escaped.json").exists())

    def test_pax_only_accepts_one_safe_path_field(self):
        for pax in ({"path": "../escaped.json"}, {"size": "999999999999"},
                    {"GNU.sparse.map": "0,1"}, {"linkpath": "outside"}):
            with self.subTest(pax=pax):
                self.pack(pax=pax)
                self.rejected()

    def test_duplicate_missing_extra_or_modified_members_fail_before_merge(self):
        original = self.members()
        variants = [original + [original[-1]], original[1:], [m for m in original if m[0] != bootstrap.products.CANDIDATE_INDEX],
                    original[:-1], original + [(self.key + "/data/extra.json", b"{}")],
                    original[:-1] + [(original[-1][0], b"changed")]]
        for members in variants:
            with self.subTest(names=[name for name, _ in members]):
                self.pack(members)
                self.rejected()

    def test_candidate_index_is_strictly_typed_and_closed(self):
        original = self.members()
        parsed = json.loads(original[1][1])
        bad = []
        unknown = copy.deepcopy(parsed)
        unknown["approval"] = True
        bad.append(json.dumps(unknown).encode())
        boolean = copy.deepcopy(parsed)
        boolean["entries"][self.key]["count"] = True
        bad.append(json.dumps(boolean).encode())
        bad.append(b'{"schema":"x","schema":"y","entries":{}}')
        for raw in bad:
            with self.subTest(raw=raw):
                self.pack([original[0], (original[1][0], raw), *original[2:]])
                self.rejected()

    def test_archive_hash_extent_and_unpacked_extent_are_exact(self):
        for field, value in (("sha256", "f" * 64), ("bytes", 1), ("unpacked_bytes", 1)):
            with self.subTest(field=field):
                declaration = self.pack()
                declaration["archive"][field] = value
                self.metadata.write_text(json.dumps(declaration))
                self.rejected()

    def test_member_and_tar_header_limits_are_enforced_before_payload_reads(self):
        for field, limit in (("MAX_MEMBER_BYTES", 1), ("MAX_INDEX_BYTES", 1), ("MAX_HEADERS", 1)):
            with self.subTest(field=field):
                self.pack()
                with mock.patch.object(bootstrap, field, limit):
                    self.rejected()

    def test_truncated_gzip_and_nonzero_trailing_data_are_rejected(self):
        self.pack(raw=b"invalid TAR" + bytes(2048))
        self.rejected()
        raw = io.BytesIO()
        with tarfile.open(fileobj=raw, mode="w", format=tarfile.PAX_FORMAT) as archive:
            for name, body in self.members():
                info = tarfile.TarInfo(name)
                info.size = len(body)
                archive.addfile(info, io.BytesIO(body))
        self.pack(raw=raw.getvalue() + b"unexpected")
        self.rejected()
        declaration = self.pack()
        data = self.archive.read_bytes()[:-5]
        self.archive.write_bytes(data)
        declaration["archive"].update(bytes=len(data), sha256=hashlib.sha256(data).hexdigest())
        self.metadata.write_text(json.dumps(declaration))
        self.rejected()

    def test_metadata_fields_types_urls_and_limits_are_strict(self):
        original = self.pack()
        variants = []
        for field, value in (("bytes", True), ("bytes", bootstrap.MAX_ARCHIVE_BYTES + 1),
                             ("unpacked_bytes", bootstrap.MAX_UNPACKED_BYTES + 1),
                             ("url", "http://github.com/example/x/releases/download/v1/x.tar.gz"),
                             ("url", "https://localhost/pack.tar.gz"), ("url", "file:///tmp/pack.tar.gz"),
                             ("url", original["archive"]["url"] + "?token=x")):
            bad = copy.deepcopy(original)
            bad["archive"][field] = value
            variants.append(bad)
        bad = copy.deepcopy(original)
        bad["archive"]["unknown"] = True
        variants.append(bad)
        for value in variants:
            with self.subTest(value=value):
                self.metadata.write_text(json.dumps(value))
                self.rejected()

    def test_network_access_is_explicit_and_unavailability_falls_back_cold(self):
        self.pack()
        with mock.patch.object(bootstrap, "download", side_effect=AssertionError("fetch was not requested")):
            result = bootstrap.bootstrap(self.root, self.metadata, cache_root=self.cache)
        self.assertEqual(result["status"], "unavailable")
        with mock.patch.object(bootstrap, "download", side_effect=bootstrap.Unavailable("offline")):
            result = bootstrap.bootstrap(self.root, self.metadata, cache_root=self.cache, fetch=True)
        self.assertEqual(result["status"], "unavailable")
        self.assertFalse(self.cache.exists())
        with self.assertRaises(bootstrap.BootstrapError):
            bootstrap.bootstrap(self.root, self.metadata, archive=self.archive, fetch=True)

    def test_disabled_placeholder_performs_no_fetch(self):
        self.metadata.write_text(json.dumps({"schema": bootstrap.SCHEMA, "archive": None}))
        with mock.patch.object(bootstrap, "download", side_effect=AssertionError("disabled")):
            self.assertEqual(bootstrap.bootstrap(self.root, self.metadata, fetch=True)["status"], "unavailable")

    def test_unsafe_redirects_are_not_followed(self):
        handler = bootstrap._Redirects()
        request = bootstrap.urllib.request.Request("https://github.com/example")
        for url in ("http://github.com/example", "https://localhost/file", "https://user:password@github.com/file", "file:///tmp/file"):
            with self.subTest(url=url), self.assertRaises(bootstrap.BootstrapError):
                handler.redirect_request(request, None, 302, "redirect", {}, url)

    def test_workflow_bootstraps_explicitly_and_saves_before_independent_verification(self):
        workflow = yaml.safe_load((ROOT / ".github/workflows/pages.yml").read_text())
        job = workflow["jobs"]["build"]
        self.assertEqual(job["timeout-minutes"], 60)
        steps = job["steps"]
        names = [step["name"] for step in steps]
        positions = [names.index(name) for name in ("Restore browser product candidates", "Bootstrap optional browser product candidates",
                     "Validate sources and build public artifact", "Retain verified current browser products", "Save verified browser products",
                     "Verify artifact and GitHub Pages compatibility", "Configure Pages", "Upload verified artifact")]
        self.assertEqual(positions, sorted(positions))
        bootstrap_step = steps[names.index("Bootstrap optional browser product candidates")]
        self.assertEqual(bootstrap_step["run"], "python scripts/_browser_cache_bootstrap.py --fetch")
        self.assertEqual(bootstrap_step["if"], "steps.browser-cache.outputs.cache-hit != 'true'")
        self.assertNotIn("if", steps[names.index("Verify artifact and GitHub Pages compatibility")])


class PinnedHtmlCompilerTests(unittest.TestCase):
    def setUp(self):
        scratch = ROOT / ".scratch/web-print-ci"
        scratch.mkdir(parents=True, exist_ok=True)
        temporary = tempfile.TemporaryDirectory(prefix="installer-test-", dir=scratch)
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        self.destination = self.root / "bin"
        self.archive = self.root / "pandoc.tar.gz"
        self.pin = copy.deepcopy(pandoc.load_lock(ROOT))

    def write_lock(self, *, extra=None):
        path = self.root / pandoc.LOCK
        path.parent.mkdir(parents=True, exist_ok=True)
        lines = ["schema_version = 1", 'record_type = "browser-print-toolchain"']
        lines.extend(f"{key} = {json.dumps(value)}" for key, value in (extra or {}).items())
        lines.append("[pandoc]")
        lines.extend(f"{key} = {json.dumps(value)}" for key, value in self.pin.items())
        path.write_text("\n".join(lines) + "\n")

    def pack(self, *, kind=tarfile.REGTYPE, duplicate=False, version="3.11"):
        body = ("#!/bin/sh\nprintf 'pandoc " + version + "\\n'\n").encode()
        stream = io.BytesIO()
        with tarfile.open(fileobj=stream, mode="w", format=tarfile.PAX_FORMAT) as archive:
            info = tarfile.TarInfo(self.pin["member"])
            info.type = kind
            info.size = len(body) if info.isreg() else 0
            info.linkname = "outside" if info.issym() or info.islnk() else ""
            archive.addfile(info, io.BytesIO(body) if info.isreg() else None)
            if duplicate:
                archive.addfile(info, io.BytesIO(body))
            other = tarfile.TarInfo("../../not-installed")
            other.size = 7
            archive.addfile(other, io.BytesIO(b"ignored"))
        raw = gzip.compress(stream.getvalue(), mtime=0)
        self.archive.write_bytes(raw)
        self.pin.update(archive_bytes=len(raw), archive_sha256=hashlib.sha256(raw).hexdigest(),
                        binary_bytes=len(body), binary_sha256=hashlib.sha256(body).hexdigest())
        self.write_lock()

    def install(self, **kwargs):
        return pandoc.install(self.root, self.destination, archive=self.archive, **kwargs)

    def test_reads_frozen_toolchain_lock_and_copies_only_selected_binary(self):
        self.assertEqual(self.pin["version"], "3.11")
        self.pack()
        with mock.patch.object(pandoc.urllib.request, "build_opener", side_effect=AssertionError("offline install fetched")):
            result = self.install()
        self.assertEqual(result["binary_sha256"], self.pin["binary_sha256"])
        self.assertEqual([path.name for path in self.destination.iterdir()], ["pandoc"])
        self.assertEqual((self.destination / "pandoc").stat().st_mode & 0o777, 0o755)
        self.assertFalse((self.root.parent / "not-installed").exists())

    def test_package_hash_precedes_tar_interpretation_and_binary_hash_precedes_execution(self):
        for field in ("archive_sha256", "binary_sha256"):
            with self.subTest(field=field):
                self.pack()
                self.pin[field] = "f" * 64
                self.write_lock()
                boundary = mock.patch.object(pandoc.tarfile, "open", side_effect=AssertionError("unverified archive")) if field == "archive_sha256" else mock.patch.object(pandoc.subprocess, "run", side_effect=AssertionError("unverified binary"))
                with boundary, self.assertRaises(pandoc.InstallError):
                    self.install()
                self.assertFalse((self.destination / "pandoc").exists())

    def test_nonregular_or_duplicate_selected_binary_is_rejected(self):
        for kind in (tarfile.SYMTYPE, tarfile.LNKTYPE, tarfile.DIRTYPE):
            with self.subTest(kind=kind):
                self.pack(kind=kind)
                with self.assertRaises(pandoc.InstallError):
                    self.install()
        self.pack(duplicate=True)
        with self.assertRaises(pandoc.InstallError):
            self.install()
        self.assertFalse((self.destination / "pandoc").exists())

    def test_version_is_checked_before_publication(self):
        self.pack(version="wrong")
        with self.assertRaises(pandoc.InstallError):
            self.install()
        self.assertFalse((self.destination / "pandoc").exists())

    def test_existing_binary_and_symlinked_install_parent_are_never_replaced(self):
        self.pack()
        self.destination.mkdir()
        existing = self.destination / "pandoc"
        existing.write_text("existing")
        with self.assertRaises(pandoc.InstallError):
            self.install()
        self.assertEqual(existing.read_text(), "existing")
        existing.unlink()
        self.destination.rmdir()
        outside = self.root / "outside"
        outside.mkdir()
        self.destination.symlink_to(outside, target_is_directory=True)
        with self.assertRaises(pandoc.InstallError):
            self.install()
        self.assertEqual(list(outside.iterdir()), [])

    def test_network_requires_explicit_exclusive_selection(self):
        self.pack()
        with mock.patch.object(pandoc.urllib.request, "build_opener", side_effect=AssertionError("implicit network")):
            with self.assertRaises(pandoc.InstallError):
                pandoc.install(self.root, self.destination)
            with self.assertRaises(pandoc.InstallError):
                self.install(fetch=True)

    def test_closed_lock_requires_official_versioned_release_and_bounded_strict_pins(self):
        original = copy.deepcopy(self.pin)
        for field, value in (("archive_bytes", True), ("binary_bytes", 0), ("binary_bytes", pandoc.MAX_BINARY_BYTES + 1),
                             ("archive_sha256", "not-a-digest"), ("binary_sha256", "A" * 64),
                             ("archive_url", "https://example.com/pandoc.tar.gz"),
                             ("member", "../pandoc"), ("version", "latest"), ("extra", 1)):
            with self.subTest(field=field, value=value):
                self.pin = {**original, field: value}
                self.write_lock()
                with self.assertRaises(pandoc.InstallError):
                    pandoc.load_lock(self.root)
        self.pin = original
        self.write_lock(extra={"unexpected": "field"})
        with self.assertRaises(pandoc.InstallError):
            pandoc.load_lock(self.root)

    def test_fetch_uses_locked_url_and_rejects_unsafe_redirects_or_http_extent(self):
        self.pack()
        response = io.BytesIO(self.archive.read_bytes())
        response.headers = {"Content-Length": str(self.pin["archive_bytes"] + 1)}
        opener = mock.Mock()
        opener.open.return_value = response
        with mock.patch.object(pandoc.urllib.request, "build_opener", return_value=opener):
            with self.assertRaises(pandoc.InstallError):
                pandoc.install(self.root, self.destination, fetch=True)
        self.assertEqual(opener.open.call_args.args[0].full_url, self.pin["archive_url"])
        handler = pandoc.Redirects()
        request = pandoc.urllib.request.Request(self.pin["archive_url"])
        for url in ("http://github.com/asset", "https://example.com/asset", "https://user@github.com/asset", "https://github.com:444/asset"):
            with self.subTest(url=url), self.assertRaises(pandoc.InstallError):
                handler.redirect_request(request, None, 302, "redirect", {}, url)


if __name__ == "__main__":
    unittest.main()
