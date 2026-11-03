"""Cold readers use exact original row extracts without archive hydration."""
from __future__ import annotations

import copy
import hashlib
import json
from pathlib import Path
import sys
import unittest
from unittest.mock import patch

if __package__:
    from . import test_print_catalog as fixtures
else:
    import test_print_catalog as fixtures
sys.path.insert(0, str(fixtures.ROOT / "scripts"))
import _papal_input_receipt as receipts
import _papal_install as installer
import _snapshot_store as store


class InputReceiptTests(unittest.TestCase):
    def setUp(self):
        scratch = fixtures.ROOT / ".scratch/next-snapshot-consumers"
        scratch.mkdir(parents=True, exist_ok=True)
        self.fixture = fixtures.SourceFixture("runTest")
        with patch.object(fixtures, "ROOT", scratch):
            self.fixture.setUp()
        self.addCleanup(self.fixture.doCleanups)
        self.root = self.fixture.root
        f = self.fixture
        released = f.release["documents"][0]
        manifest = copy.deepcopy(f.manifest)
        manifest["documents"] = [dict(f.source, id="unused.first"), dict(f.source, id="unused.second"), f.source]
        mf = f.freeze(released["manifest"]["path"], manifest)
        rendered = json.loads((self.root / released["receipt"]["path"]).read_bytes())
        rendered["input_manifest_sha256"] = mf["sha256"]
        rf = f.freeze(released["receipt"]["path"], rendered)
        audit = json.loads((self.root / released["review"]["audit"]["path"]).read_bytes())
        audit["frozen_receipt_sha256"] = rf["sha256"]
        audit["review_scope"] = {"limits": "Complete synthetic page; no historical claim."}
        af = f.freeze(released["review"]["audit"]["path"], audit)
        released["manifest"] = dict(mf, row_index=2)
        released["receipt"] = dict(rf, row_index=0)
        released["review"].update(audit=dict(af, row_index=0), current_receipt_sha256=rf["sha256"], original_receipt_sha256=rf["sha256"])
        released["bytes"] = 1234
        released["pdf"] = installer._filename(f.source)
        f.reader["pdf"] = released["pdf"]
        self.originals = {}
        refs = [f.release["source_plan"], released["manifest"], released["receipt"], released["review"]["audit"]]
        for ref in refs:
            raw = (self.root / ref["path"]).read_bytes()
            ref["path"] = f"release/papal-documents/inputs/{ref['sha256']}.json"
            (self.root / ref["path"]).write_bytes(raw)
            self.originals[ref["path"]] = raw
        for item in f.plan["selection_plan"]["inputs"]:
            raw = (self.root / item["path"]).read_bytes()
            logical = f"release/papal-documents/inputs/{item['sha256']}.json"
            (self.root / logical).write_bytes(raw)
            self.originals[logical] = raw
        f.release.update(schema=installer.RELEASE_SCHEMA, generator="typeset-papal install", delivery_states=[])
        f.release["evidence"] = [
            {"path": path, "sha256": hashlib.sha256(raw).hexdigest(), "bytes": len(raw)}
            for path, raw in self.originals.items()
        ]
        f.save_release()
        f.save_index()
        archive_sha = "e" * 64
        index = {"schema": store.SCHEMA, "archives": [{
            "id": archive_sha, "name": "snapshots.tar", "sha256": archive_sha,
            "bytes": 1_000_000, "urls": ["https://example.org/snapshots.tar"],
        }], "artifacts": [{
            "path": path, "member": path, "sha256": hashlib.sha256(raw).hexdigest(), "bytes": len(raw),
            "kind": store.KIND, "media_type": "application/json", "archive": archive_sha,
        } for path, raw in self.originals.items()]}
        f.write(store.INDEX_PATH, json.dumps(index))
        receipts.record(self.root, scratch=self.root / ".scratch/record")

    def cold(self):
        for path in (self.root / "release/papal-documents/inputs").iterdir():
            path.unlink()

    def test_original_indices_headers_and_complete_plan_are_retained(self):
        records = receipts.InputRecords(self.root)
        row = self.fixture.release["documents"][0]
        self.assertEqual(self.fixture.source, records.row(row["manifest"], 2))
        self.assertEqual(["2"], list(records._record(row["manifest"])["rows"]))
        self.assertEqual(3, records._record(row["manifest"])["documents_count"])
        self.assertEqual({"limits": "Complete synthetic page; no historical claim."}, records.header(row["review"]["audit"])["review_scope"])
        self.assertEqual(self.fixture.plan["documents"], records.plan_rows(self.fixture.release["source_plan"]))
        for index in (True, -1, 3):
            with self.assertRaises(receipts.InputReceiptError):
                records.row(row["manifest"], index)
        with self.assertRaisesRegex(receipts.InputReceiptError, "no retained extraction"):
            records.row(row["manifest"], 0)

    def test_cold_html_and_full_release_metadata_do_not_read_or_hydrate_originals(self):
        self.cold()
        original_open = Path.open
        def metadata_only(path, *args, **kwargs):
            self.assertNotIn("release/papal-documents/inputs/", str(path))
            self.assertNotEqual(".pdf", path.suffix)
            return original_open(path, *args, **kwargs)
        with patch.object(Path, "open", metadata_only), patch.object(store, "resolve", side_effect=AssertionError("no hydration")):
            pages = fixtures.catalog.source_pages(self.root)
            self.assertEqual(1, len(pages))
            self.assertFalse(any(path.startswith(store.PREFIX) for path in next(iter(pages.values()))["source_paths"]))
            with patch.object(installer, "ROOT", self.root), patch.object(installer.collection, "ROOT", self.root), patch.object(installer, "_fresh_plan", return_value=(self.fixture.plan, self.fixture.release["source_plan"]["sha256"])):
                result = installer.check_release_metadata(self.root / "unused-plan.json")
                self.assertEqual(1, result["installed"])
                self.assertEqual("mechanically-attested-release-metadata", result["verification"])

    def test_generated_data_root_keeps_canonical_input_declarations(self):
        data = self.root / ".scratch/verified-data"
        (data / "encyclicals").mkdir(parents=True)
        (data / "encyclicals/index.json").write_bytes((self.root / "src/web/data/encyclicals/index.json").read_bytes())
        (self.root / "src/web/data/encyclicals/index.json").unlink()
        self.cold()
        pages = fixtures.catalog.source_pages(self.root, data_root=data, data_source_paths=("release/browser-products.json",))
        paths = next(iter(pages.values()))["source_paths"]
        self.assertIn("release/browser-products.json", paths)
        self.assertFalse(any(".scratch/verified-data" in path for path in paths))
        (data / "encyclicals/index.json").unlink()
        with self.assertRaisesRegex(fixtures.catalog.PrintCatalogError, "omit.*encyclicals"):
            fixtures.catalog.source_pages(self.root, data_root=data)

    def test_missing_changed_records_and_changed_release_fail(self):
        self.cold()
        index = json.loads((self.root / receipts.INDEX).read_bytes())
        pin = index["records"][self.fixture.release["documents"][0]["manifest"]["path"]]
        shard = self.root / pin["path"]
        raw = shard.read_bytes()
        shard.write_bytes(raw + b" ")
        with self.assertRaisesRegex(receipts.InputReceiptError, "hash/size"):
            fixtures.catalog.source_pages(self.root)
        shard.unlink()
        with self.assertRaisesRegex(receipts.InputReceiptError, "physical shard membership"):
            fixtures.catalog.source_pages(self.root)
        shard.write_bytes(raw)
        self.fixture.release["documents"][0]["manifest"]["row_index"] = 0
        self.fixture.save_release()
        with self.assertRaisesRegex(receipts.InputReceiptError, "different release"):
            fixtures.catalog.source_pages(self.root)

    def test_review_semantics_are_rerun_even_if_metadata_hashes_match(self):
        self.cold()
        index = json.loads((self.root / receipts.INDEX).read_bytes())
        logical = self.fixture.release["documents"][0]["review"]["audit"]["path"]
        pin = index["records"][logical]
        path = self.root / pin["path"]
        shard = json.loads(path.read_bytes())
        shard["rows"]["0"]["individually_inspected_pages"] = []
        raw = receipts._bytes(shard)
        path.write_bytes(raw)
        index["records"][logical] = receipts._pin(raw, pin["path"])
        (self.root / receipts.INDEX).write_bytes(receipts._bytes(index))
        with self.assertRaisesRegex(fixtures.catalog.PrintCatalogError, "cover every page"):
            fixtures.catalog.source_pages(self.root)

    def test_explicit_original_audit_requires_verified_local_bytes(self):
        self.cold()
        records = receipts.InputRecords(self.root)
        with self.assertRaises(FileNotFoundError):
            records.audit_originals()
        for entry in store.load_index(self.root)["artifacts"]:
            target = store.cache_path(self.root, entry)
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(self.originals[entry["path"]])
        self.assertEqual(len(self.originals), records.audit_originals()["originals"])
        target.write_bytes(b"changed")
        with self.assertRaises(ValueError):
            records.audit_originals()

    def test_recording_refuses_tampered_original_and_missing_external_extract(self):
        logical, raw = next(iter(self.originals.items()))
        (self.root / logical).write_bytes(raw + b"changed")
        with self.assertRaises(ValueError):
            receipts.record(self.root, scratch=self.root / ".scratch/record")
        (self.root / receipts.INDEX).unlink()
        with self.assertRaisesRegex(receipts.InputReceiptError, "requires.*extract"):
            fixtures.catalog.source_pages(self.root)

    def test_membership_rejects_boolean_indices_and_unknown_envelope_fields(self):
        path = self.root / receipts.INDEX
        original = path.read_bytes()
        index = json.loads(original)
        logical = self.fixture.release["documents"][0]["receipt"]["path"]
        index["required_rows"][logical] = [False]
        path.write_bytes(receipts._bytes(index))
        with self.assertRaisesRegex(receipts.InputReceiptError, "integer row indices"):
            receipts.InputRecords(self.root)
        index = json.loads(original)
        index["approval"] = True
        path.write_bytes(receipts._bytes(index))
        with self.assertRaisesRegex(receipts.InputReceiptError, "ownership envelope"):
            receipts.InputRecords(self.root)

    def replacement_plan(self):
        previous = json.loads((self.root / receipts.INDEX).read_bytes())
        old_logical = self.fixture.release["source_plan"]["path"]
        plan = copy.deepcopy(self.fixture.plan)
        plan["scope"] = "A new exact source-plan header; source selections stay unchanged."
        raw = receipts._bytes(plan)
        logical = f"release/papal-documents/inputs/{hashlib.sha256(raw).hexdigest()}.json"
        (self.root / logical).write_bytes(raw)
        ref = receipts._pin(raw, logical)
        self.fixture.release["source_plan"] = ref
        self.fixture.release["evidence"].append(ref)
        self.fixture.save_release()
        delivery = json.loads((self.root / store.INDEX_PATH).read_bytes())
        delivery["artifacts"].append({
            **ref, "member": logical, "kind": store.KIND, "media_type": "application/json",
            "archive": delivery["archives"][0]["id"],
        })
        self.fixture.write(store.INDEX_PATH, json.dumps(delivery))
        return previous, old_logical, logical

    def test_record_prunes_only_previous_owned_plan_shard_after_new_outputs_verify(self):
        previous, old_logical, logical = self.replacement_plan()
        obsolete = self.root / previous["records"][old_logical]["path"]
        obsolete_bytes = obsolete.read_bytes()
        unchanged = next(pin for path, pin in previous["records"].items() if path != old_logical)
        unchanged_path = self.root / unchanged["path"]
        unchanged_stamp = unchanged_path.stat().st_mtime_ns
        result = receipts.record(self.root, scratch=self.root / ".scratch/record")
        self.assertEqual(1, result["pruned"])
        self.assertFalse(obsolete.exists())
        current = receipts.InputRecords(self.root)
        self.assertIn(old_logical, current.index["originals"])
        self.assertNotIn(old_logical, current.index["records"])
        self.assertIn(logical, current.index["records"])
        self.assertEqual(unchanged_stamp, unchanged_path.stat().st_mtime_ns)
        self.assertTrue(obsolete_bytes)
        self.assertEqual(1, len(fixtures.catalog.source_pages(self.root)))

    def test_unknown_symlink_and_nonregular_shard_entries_are_preserved_and_refused(self):
        original_index = (self.root / receipts.INDEX).read_bytes()
        extra = self.root / receipts.DIRECTORY / "unowned.json"
        for kind in ("file", "symlink", "directory"):
            with self.subTest(kind=kind):
                if kind == "file":
                    extra.write_text("unowned user material")
                elif kind == "symlink":
                    extra.symlink_to(self.root / receipts.INDEX)
                else:
                    extra.mkdir()
                with self.assertRaises(receipts.InputReceiptError):
                    receipts.InputRecords(self.root)
                with self.assertRaises(receipts.InputReceiptError):
                    receipts.record(self.root, scratch=self.root / ".scratch/record")
                self.assertTrue(extra.exists())
                self.assertEqual(original_index, (self.root / receipts.INDEX).read_bytes())
                extra.rmdir() if kind == "directory" else extra.unlink()

    def test_tampered_previous_owned_shard_is_preserved_before_any_record_write(self):
        previous, old_logical, _ = self.replacement_plan()
        obsolete = self.root / previous["records"][old_logical]["path"]
        tampered = obsolete.read_bytes() + b" changed user bytes"
        obsolete.write_bytes(tampered)
        original_index = (self.root / receipts.INDEX).read_bytes()
        with self.assertRaisesRegex(receipts.InputReceiptError, "hash/size.*preserved"):
            receipts.record(self.root, scratch=self.root / ".scratch/record")
        self.assertEqual(tampered, obsolete.read_bytes())
        self.assertEqual(original_index, (self.root / receipts.INDEX).read_bytes())

    def test_new_output_verification_failure_preserves_obsolete_shards(self):
        previous, old_logical, logical = self.replacement_plan()
        obsolete = self.root / previous["records"][old_logical]["path"]
        saved = obsolete.read_bytes()
        original = receipts.InputRecords._record
        def fail_new(records, ref):
            if ref["path"] == logical:
                raise receipts.InputReceiptError("new output verification refused")
            return original(records, ref)
        with patch.object(receipts.InputRecords, "_record", fail_new):
            with self.assertRaisesRegex(receipts.InputReceiptError, "new output verification"):
                receipts.record(self.root, scratch=self.root / ".scratch/record")
        self.assertEqual(saved, obsolete.read_bytes())

    def test_identical_record_preserves_existing_metadata_mtimes(self):
        files = [self.root / receipts.INDEX, *(self.root / receipts.DIRECTORY).iterdir()]
        before = {path: (path.read_bytes(), path.stat().st_mtime_ns) for path in files}
        result = receipts.record(self.root, scratch=self.root / ".scratch/record")
        self.assertEqual(0, result["pruned"])
        self.assertEqual(before, {path: (path.read_bytes(), path.stat().st_mtime_ns) for path in files})


if __name__ == "__main__":
    unittest.main()
