"""Native source shard handoff must reproduce the direct full catalog exactly."""
from __future__ import annotations

import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))
import _native_print_bundles as bundles
import _native_print_compile as gate
import _native_print_reference as reference

REVISION = "f" * 40


class NativeReferenceTests(unittest.TestCase):
    def setUp(self):
        base = ROOT / ".scratch/native-print-reference-tests"
        base.mkdir(parents=True, exist_ok=True)
        temporary = tempfile.TemporaryDirectory(dir=base)
        self.addCleanup(temporary.cleanup)
        self.work = Path(temporary.name)
        self.docs = {name: {"document": name, "edition": "main", "title": name.title()}
                     for name in ("alpha", "beta", "delta", "gamma")}
        self.source = self.work / "tracked.jpg"
        self.source.write_bytes(b"\xff\xd8\x00\x11")
        self.full = self.catalog(sorted(self.docs))
        self.shards = self.work / "shards"
        self.keys = {}
        for number in (1, 2):
            shard = self.catalog(gate.partition(self.docs, number, 2))
            self.keys[str(number)] = reference.write_reference_catalog(
                self.shards / str(number), shard, run_id="123", run_attempt="1", shard=(number, 2))
        self.out = self.work / "merged"

    def catalog(self, selected):
        # alpha and beta land in distinct shards but share text, so the direct
        # catalog and shard source transports necessarily differ. A second
        # shared file exercises gzip packs that already exist within shards.
        prepared, assets = {}, {}
        source_row = bundles._fingerprints(self.work, ["tracked.jpg"])[0]
        for name in selected:
            files = {"src/test/main.tex": ("Some words about " + name + ".\n").encode(),
                     "src/test/art.jpg": self.source.read_bytes(),
                     "src/test/common.tex": b"Common source for every edition.\n" * 50,
                     "src/test/pair.tex": ((b"repeated pair source\n" * 70)
                                           if name in {"alpha", "beta"} else name.encode())}
            bundle = {**self.docs[name], "schema": bundles.SCHEMA, "output_id": name,
                      "source_revision": REVISION, "engine": "pdftex", "format": "pdflatex",
                      "entrypoint": "src/test/main.tex", "cwd": "src/test", "environment": {},
                      "options": dict(gate.OPTIONS), "computed_source_inputs": [],
                      "source_inputs": [source_row], "files": [bundles._file(k, v) for k, v in sorted(files.items())]}
            bundle["render_sha256"] = bundles.render_identity(bundle)
            prepared[name] = bundles._externalize(bundle, assets)
        return bundles.package_catalog(prepared, assets, REVISION)

    def merge(self, **override):
        values = dict(root=self.work, documents=self.docs, revision=REVISION, run_id="123",
                      run_attempt="2", shards=2, expected_keys=self.keys)
        return reference.merge_reference_catalogs(self.shards, **{**values, **override})

    def write_merged(self):
        return reference.write_reference_catalog(self.out, self.merge(), run_id="123", run_attempt="2")

    def load(self, digest, **override):
        values = dict(root=self.work, documents=self.docs, revision=REVISION, run_id="123",
                      run_attempt="2", expected_sha256=digest)
        return reference.load_reference_catalog(self.out, **{**values, **override})

    def test_roundtrip_matches_direct_catalog_with_different_transport(self):
        shard = json.loads((self.shards / "1/catalog.json").read_bytes())
        self.assertNotEqual(self.full["bundles"]["alpha"], shard["bundles"]["alpha"])
        self.assertIn("tracked.jpg", shard["checkout_assets"].values())
        self.assertFalse(any(self.shards.rglob("*.jpg")))
        self.assertTrue(list(self.shards.rglob("source-packs/*.bin")))
        self.assertEqual(self.full, self.merge())
        self.assertEqual(self.full, self.load(self.write_merged()))

    def test_export_and_compile_index_describe_the_same_preparation(self):
        selected = gate.partition(self.docs, 2, 2)
        canonical = self.catalog(selected)
        work = self.work / "compile"
        handoff = self.work / "handoff"
        with patch("_native_print.admitted_documents", return_value=self.docs), \
             patch("_native_print.source_revision", return_value=REVISION), \
             patch.object(subprocess, "run", return_value=subprocess.CompletedProcess([], 0, stdout="100")), \
             patch.object(bundles, "prepare_catalog", return_value=canonical) as prepare:
            index = gate.prepare(self.work, work, shard=(2, 2), export_reference=handoff,
                                 run_id="123", run_attempt="1")
        prepare.assert_called_once_with(self.work, documents=self.docs, revision=REVISION, output_ids=selected)
        exported = (handoff / "catalog.json").read_bytes()
        self.assertEqual(index, json.loads((work / "index.json").read_bytes()))
        self.assertEqual(index["reference_sha256"], bundles._sha(exported))
        for key, descriptor in json.loads(exported)["bundles"].items():
            self.assertEqual(descriptor["sha256"], index["editions"][key]["bundle_sha256"])
            self.assertEqual(descriptor["route"], index["editions"][key]["bundle_route"])

    def test_each_shard_and_merged_digest_run_revision_attempt_are_bound(self):
        for values in (dict(expected_keys={"1": self.keys["1"]}),
                       dict(expected_keys={"1": self.keys["2"], "2": self.keys["1"]}),
                       dict(revision="e" * 40), dict(run_id="124")):
            with self.subTest(values=values), self.assertRaises(ValueError):
                self.merge(**values)
        digest = self.write_merged()
        for values in (dict(expected_sha256="0" * 64), dict(run_id="124"), dict(revision="e" * 40),
                       dict(run_attempt="1"), dict(run_attempt="3")):
            with self.subTest(values=values), self.assertRaises(ValueError):
                self.load(digest, **values)
        path = self.shards / "1/catalog.json"
        value = json.loads(path.read_bytes())
        value["run_attempt"] = "3"
        path.write_bytes(bundles.canonical(value) + b"\n")
        self.keys["1"] = bundles._sha(path.read_bytes())
        with self.assertRaisesRegex(ValueError, "attempt"):
            self.merge()

    def test_missing_extra_and_wrongly_assigned_editions_fail(self):
        with self.assertRaisesRegex(ValueError, "admissions or partition"):
            self.merge(documents={**self.docs, "extra": self.docs["beta"]})
        with self.assertRaisesRegex(ValueError, "admitted edition"):
            self.merge(documents={**self.docs, "alpha": self.docs["gamma"]})
        shard = self.shards / "2"
        shard.rename(self.shards / "3")
        with self.assertRaisesRegex(ValueError, "incomplete shard set"):
            self.merge()
        (self.shards / "3").rename(shard)
        shutil.rmtree(shard)
        with self.assertRaisesRegex(ValueError, "incomplete shard set"):
            self.merge()

    def test_rehashed_reference_cannot_add_an_unowned_route_or_unsafe_checkout_path(self):
        folder = self.shards / "1"
        addition = folder / "native-tex/assets" / ("0" * 64 + ".bin")
        addition.write_bytes(b"x")
        with self.assertRaisesRegex(ValueError, "unowned"):
            self.merge()
        addition.unlink()
        path = folder / "catalog.json"
        value = json.loads(path.read_bytes())
        route = next(iter(value["checkout_assets"]))
        value["checkout_assets"][route] = "../tracked.jpg"
        path.write_bytes(bundles.canonical(value) + b"\n")
        self.keys["1"] = bundles._sha(path.read_bytes())
        with self.assertRaisesRegex(ValueError, "unsafe native source path"):
            self.merge()

    def test_corrupt_bundle_pack_or_raw_asset_and_changed_checkout_fail(self):
        for group in ("sources", "source-packs", "assets"):
            path = next((self.shards / "1/native-tex" / group).iterdir())
            raw = path.read_bytes()
            path.write_bytes(bytes([raw[0] ^ 1]) + raw[1:])
            with self.subTest(group=group), self.assertRaisesRegex(ValueError, "changed reference asset"):
                self.merge()
            path.write_bytes(raw)
        digest = self.write_merged()
        self.source.write_bytes(b"\xff\xd8\x00\x12")
        with self.assertRaisesRegex(ValueError, "changed reference asset"):
            self.merge()
        with self.assertRaisesRegex(ValueError, "source fingerprint differs"):
            self.load(digest)

    def test_symlink_and_unrelated_destination_fail(self):
        folder = self.shards / "1"
        asset = next((folder / "native-tex/assets").iterdir())
        actual = self.work / "other"
        asset.rename(actual)
        asset.symlink_to(actual)
        with self.assertRaisesRegex(ValueError, "redirected reference file"):
            self.merge()
        self.out.mkdir()
        (self.out / "keep").write_bytes(b"keep")
        with self.assertRaisesRegex(ValueError, "refusing to replace"):
            reference.write_reference_catalog(self.out, self.full, run_id="123", run_attempt="1")
        self.assertEqual((self.out / "keep").read_bytes(), b"keep")


if __name__ == "__main__":
    unittest.main()
