"""Native TeX software hydration and publication reject changed or unsafe bytes."""
from __future__ import annotations

import copy
import io
import json
from pathlib import Path
import sys
import tarfile
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))
import _artifact_store as transport
import _native_tex_assets as assets


class NativeTeXAssetsTests(unittest.TestCase):
    def setUp(self):
        scratch = ROOT / ".scratch/native-tex-asset-tests"
        scratch.mkdir(parents=True, exist_ok=True)
        self.temporary = tempfile.TemporaryDirectory(dir=scratch)
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.pack = self.root / ".scratch/pack"
        self.pack.mkdir(parents=True)
        self.bodies = {}
        self.data = {"schema": assets.SCHEMA, "id": "test-runtime", "upstream": {"release": "test"},
                     "engines": {}, "texFiles": [], "texMissing": [{"format": 26, "name": "optional.cfg"}],
                     "notices": [], "payloads": {}, "delivery": {}, "correspondingSource": {
                         "url": "https://example.org/source.tar.xz", "sha256": "a" * 64, "bytes": 100}}
        for engine in ("pdflatex", "xelatex", "dvipdfmx"):
            refs = {}
            for role in ("worker", "core", "wasm", "format"):
                if engine == "dvipdfmx" and role == "format":
                    continue
                extension = "wasm" if role == "wasm" else "fmt" if role == "format" else "js"
                body = b"\0asm\x01\0\0\0" if role == "wasm" else (engine + role).encode()
                refs[role] = self.add("native-tex/test-runtime/" + engine + "-" + role + "." + extension,
                                      body, "engine-software", "application/wasm" if role == "wasm" else "application/octet-stream")
            self.data["engines"][engine] = refs
        body = b"A retained TeX package."
        ref = self.add("native-tex/test-runtime/tex/" + assets.digest(body) + ".bin", body, "tex-package")
        self.data["texFiles"].append(dict(ref, format=26, name="package.sty"))
        self.data["notices"].append(self.add("native-tex/test-runtime/notices/LICENSE.txt", b"Retained terms.", "license-notice"))
        self.write_archive()

    def add(self, url, body, kind, media="application/octet-stream"):
        self.bodies[url] = body
        row = {"sha256": assets.digest(body), "bytes": len(body), "kind": kind, "media_type": media}
        self.data["payloads"][url] = row
        return {"url": url, "sha256": row["sha256"], "bytes": row["bytes"]}

    def seal(self):
        self.data["registry_sha256"] = assets.digest(assets.canonical_json(
            {key: value for key, value in self.data.items() if key != "registry_sha256"}))
        path = self.root / assets.INDEX_PATH
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(self.data), encoding="utf-8")

    def write_archive(self, extra=None, omit=None, override=None):
        path = self.pack / "runtime.tar"
        with tarfile.open(path, "w") as archive:
            for url, body in reversed(list(self.bodies.items())):
                if url == omit:
                    continue
                body = override.get(url, body) if override else body
                info = tarfile.TarInfo(url)
                info.size = len(body)
                archive.addfile(info, io.BytesIO(body))
            if extra is not None:
                archive.addfile(extra, io.BytesIO(b"X") if extra.size else None)
        pin = assets.digest(path.read_bytes())
        self.data["delivery"] = {"schema": assets.DELIVERY_SCHEMA, "archives": [{"id": pin,
            "name": path.name, "sha256": pin, "bytes": path.stat().st_size,
            "urls": ["https://example.org/runtime.tar"]}], "artifacts": [dict(row, path=url,
                archive=pin, member=url) for url, row in self.data["payloads"].items()]}
        self.seal()

    def test_offline_hydration_and_complete_publication(self):
        with patch.object(transport, "urlopen", side_effect=AssertionError("network")):
            report = assets.hydrate(self.root, archive_dir=self.pack)
            paths = assets.payload_paths(self.root)
            public = assets.public_manifest(self.root)
            self.assertEqual(report["hydrated"], len(self.bodies))
            self.assertEqual(set(paths), set(self.bodies))
            self.assertNotIn("delivery", public)
            self.assertNotIn("upstream", public)
            self.assertEqual(public["correspondingSource"], self.data["correspondingSource"])
            site = self.root / ".scratch/site"
            result = assets.publish(self.root, site)
            self.assertEqual(set(result), set(self.bodies))
            for url, body in self.bodies.items():
                self.assertEqual((site / url).read_bytes(), body)
            self.assertEqual(assets.hydrate(self.root)["hydrated"], 0)

    def test_missing_archive_never_fetches_implicitly(self):
        with patch.object(transport, "urlopen", side_effect=AssertionError("network")):
            with self.assertRaises(FileNotFoundError):
                assets.hydrate(self.root)

    def test_changed_cached_bytes_are_not_silently_repaired(self):
        assets.hydrate(self.root, archive_dir=self.pack)
        path = next(iter(assets.payload_paths(self.root).values()))
        path.write_bytes(b"changed")
        with self.assertRaisesRegex(ValueError, "hash or size"):
            assets.hydrate(self.root, archive_dir=self.pack)

    def test_unknown_lookup_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "unknown"):
            assets.payload_path(self.root, "native-tex/test-runtime/unknown.bin")

    def test_registry_hash_is_authority(self):
        self.data["texFiles"][0]["name"] = "another.sty"
        path = self.root / assets.INDEX_PATH
        path.write_text(json.dumps(self.data))
        with self.assertRaisesRegex(ValueError, "registry digest"):
            assets.load_index(self.root)

    def test_lookup_traversal_and_duplicates_are_rejected(self):
        for name in ("../source", "dir/package.sty", "package%2f.sty", "file?download"):
            with self.subTest(name=name):
                value = copy.deepcopy(self.data)
                value["texFiles"][0]["name"] = name
                value["registry_sha256"] = assets.digest(assets.canonical_json({k: v for k, v in value.items() if k != "registry_sha256"}))
                with self.assertRaises(ValueError):
                    assets.validate_index(value)
        self.data["texFiles"].append(copy.deepcopy(self.data["texFiles"][0]))
        self.seal()
        with self.assertRaisesRegex(ValueError, "duplicate"):
            assets.load_index(self.root)

    def test_positive_and_negative_lookup_cannot_disagree(self):
        self.data["texMissing"].append({"format": 26, "name": "package.sty"})
        self.seal()
        with self.assertRaisesRegex(ValueError, "contradictory"):
            assets.load_index(self.root)

    def test_missing_or_unregistered_member_promotes_nothing(self):
        for mode in ("missing", "extra", "traversal", "symlink", "duplicate"):
            with self.subTest(mode=mode):
                extra = None
                omitted = next(iter(self.bodies)) if mode == "missing" else None
                if mode != "missing":
                    name = "../escape" if mode == "traversal" else next(iter(self.bodies)) if mode == "duplicate" else "unregistered"
                    extra = tarfile.TarInfo(name)
                    if mode == "symlink":
                        extra.type = tarfile.SYMTYPE
                        extra.linkname = "../escape"
                self.write_archive(extra=extra, omit=omitted)
                with self.assertRaises(ValueError):
                    assets.hydrate(self.root, archive_dir=self.pack)
                cache = self.root / ".scratch/native-tex-runtime/objects"
                self.assertFalse(cache.exists())

    def test_changed_archive_is_rejected_before_unpacking(self):
        with (self.pack / "runtime.tar").open("ab") as stream:
            stream.write(b"changed")
        with self.assertRaisesRegex(ValueError, "hash or size"):
            assets.hydrate(self.root, archive_dir=self.pack)

    def test_member_hash_is_independent_of_accepted_archive_hash(self):
        url = next(iter(self.bodies))
        self.write_archive(override={url: b"X" * len(self.bodies[url])})
        with self.assertRaisesRegex(ValueError, "hash or size"):
            assets.hydrate(self.root, archive_dir=self.pack)
        self.assertFalse((self.root / ".scratch/native-tex-runtime/objects").exists())

    def test_wasm_header_is_checked_before_promotion(self):
        url = self.data["engines"]["pdflatex"]["wasm"]["url"]
        self.bodies[url] = b"not wasm"
        self.data["payloads"][url]["sha256"] = assets.digest(self.bodies[url])
        self.data["engines"]["pdflatex"]["wasm"]["sha256"] = assets.digest(self.bodies[url])
        self.write_archive()
        with self.assertRaisesRegex(ValueError, "WASM header"):
            assets.hydrate(self.root, archive_dir=self.pack)
        self.assertFalse((self.root / ".scratch/native-tex-runtime/objects").exists())

    def test_symlinked_cache_and_publication_destinations_are_rejected(self):
        target = self.root / ".scratch/external"
        target.mkdir()
        cache = self.root / ".scratch/native-tex-runtime"
        cache.symlink_to(target, target_is_directory=True)
        with self.assertRaisesRegex(ValueError, "symlink"):
            assets.hydrate(self.root, archive_dir=self.pack)
        cache.unlink()
        assets.hydrate(self.root, archive_dir=self.pack)
        site = self.root / ".scratch/site"
        site.mkdir()
        (site / "native-tex").symlink_to(target, target_is_directory=True)
        with self.assertRaisesRegex(ValueError, "symlink"):
            assets.publish(self.root, site)


if __name__ == "__main__":
    unittest.main()
