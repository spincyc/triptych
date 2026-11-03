"""Cold regeneration, content identity, and hostile cache filesystem contracts."""
from contextlib import ExitStack
import copy
import json
import os
from pathlib import Path
import shutil
import sys
import tempfile
import subprocess
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "scripts"))
import _browser_products as products


class BrowserProductsTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(dir=Path(__file__).resolve().parents[2] / ".scratch")
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.cache = self.root / ".scratch/cache"
        for name in ("src/a/input.txt", "src/b/input.txt", "scripts/generator.py", "requirements-tools.txt"):
            target = self.root / name
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text("one\n")
        (self.root / "release").mkdir()
        self.recipes = [{"id": name, "version": 1, "output_prefixes": ["structure/" + name], "argv": [["offline", name]],
                         "input_trees": ["src/" + name], "input_files": [], "exclude_paths": [],
                         "delivery": "browser-data"} for name in ("a", "b")]
        self.generated = []
        stack = self.enterContext(ExitStack())
        stack.enter_context(patch.object(products, "_recipes", side_effect=lambda: copy.deepcopy(self.recipes)))
        stack.enter_context(patch.object(products, "_generate", side_effect=self.generate))
        self.manifest = products.record(self.root, cache_root=self.cache)
        self.generated.clear()

    def generate(self, root, out, product_ids=None):
        self.generated.append(tuple(product_ids or ("a", "b")))
        self.assertFalse((root / "src/web/data").exists())
        for family in product_ids or ("a", "b"):
            path = out / "structure" / family / "index.json"
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(json.dumps({"value": (root / "src" / family / "input.txt").read_text()}, sort_keys=True))

    def family(self, name="a"):
        return next(item for item in self.manifest["products"] if item["id"] == name)

    def payload(self, name="a"):
        return self.cache / self.family(name)["key"] / "data/structure" / name / "index.json"

    def write_manifest(self, value):
        (self.root / products.MANIFEST_RELATIVE).write_text(json.dumps(value))

    def test_record_is_two_independent_cold_builds(self):
        shutil.rmtree(self.cache)
        products.record(self.root, cache_root=self.cache)
        self.assertEqual(self.generated, [("a", "b"), ("a", "b")])
        self.assertIs(self.manifest["editorial_approval"], False)

    def test_check_hit_never_generates(self):
        products.check(self.root, cache_root=self.cache)
        products.build(self.root, cache_root=self.cache)
        self.assertEqual(self.generated, [])

    def test_cold_miss_builds_only_missing_family(self):
        shutil.rmtree(self.cache / self.family()["key"])
        products.build(self.root, cache_root=self.cache)
        self.assertEqual(self.generated, [("a",)])
        products.check(self.root, cache_root=self.cache)

    def test_check_missing_cache_does_not_build(self):
        shutil.rmtree(self.cache)
        with self.assertRaises(products.ProductError):
            products.check(self.root, cache_root=self.cache)
        self.assertEqual(self.generated, [])

    def test_corrupt_entry_fails_closed_without_rebuild(self):
        self.payload().write_text("bad")
        with self.assertRaisesRegex(products.ProductError, "differ"):
            products.build(self.root, cache_root=self.cache)
        self.assertEqual(self.generated, [])

    def test_missing_and_extra_outputs(self):
        self.payload().unlink()
        with self.assertRaisesRegex(products.ProductError, "no outputs|missing|empty"):
            products.check(self.root, cache_root=self.cache)
        self.payload().write_text("restored")
        extra = self.payload().parent / "extra.json"
        extra.write_text("{}")
        with self.assertRaises(products.ProductError):
            products.check(self.root, cache_root=self.cache)

    def test_wrong_cold_generation_cannot_adopt_output(self):
        shutil.rmtree(self.cache)
        with patch.object(products, "_generate", side_effect=lambda root, out, ids: self.generate_bad(out)):
            with self.assertRaisesRegex(products.ProductError, "differ"):
                products.build(self.root, cache_root=self.cache)
        self.assertEqual(products.load_manifest(self.root), self.manifest)

    def generate_bad(self, out):
        path = out / "bad.json"
        path.parent.mkdir(parents=True)
        path.write_text("{}")

    def test_same_size_restored_mtime_input_invalidates(self):
        path = self.root / "src/a/input.txt"
        before = path.stat()
        path.write_text("two\n")
        os.utime(path, ns=(before.st_atime_ns, before.st_mtime_ns))
        with self.assertRaisesRegex(products.ProductError, "inputs changed"):
            products.check(self.root, cache_root=self.cache)

    def test_current_unknown_member_invalidates(self):
        (self.root / "src/a/new.txt").write_text("new")
        with self.assertRaisesRegex(products.ProductError, "inputs changed"):
            products.check(self.root, cache_root=self.cache)

    def test_generator_and_lock_change_invalidate(self):
        for name in ("scripts/generator.py", "requirements-tools.txt"):
            with self.subTest(name=name):
                path = self.root / name
                original = path.read_bytes()
                path.write_bytes(original + b"changed")
                with self.assertRaisesRegex(products.ProductError, "inputs changed"):
                    products.check(self.root, cache_root=self.cache)
                path.write_bytes(original)

    def test_hold_withdrawal_and_rights_are_current_inputs(self):
        for name in ("release/publications/a.json", "src/a/web-edition.toml", "src/a/rights.toml"):
            with self.subTest(name=name):
                path = self.root / name
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text("hold")
                with self.assertRaisesRegex(products.ProductError, "inputs changed"):
                    products.check(self.root, cache_root=self.cache)
                path.unlink()

    def test_family_refresh_reuses_exact_prior_mechanical_proof(self):
        (self.root / "src/a/input.txt").write_text("two")
        refreshed = products.record(self.root, cache_root=self.cache)
        self.assertEqual(self.generated, [("a",), ("a",)])
        self.assertEqual(self.family("b")["key"], refreshed["products"][1]["key"])
        self.assertNotEqual(self.family("a")["key"], refreshed["products"][0]["key"])

    def test_private_snapshot_is_stable_after_cache_swap(self):
        with products.verified_products(self.root, cache_root=self.cache) as held:
            original = held.files["structure/a/index.json"].read_bytes()
            self.payload().write_text("changed behind the snapshot")
            self.assertEqual(held.files["structure/a/index.json"].read_bytes(), original)
            with products.verified_products(self.root, cache_root=self.cache) as nested:
                self.assertIs(nested, held)
            self.assertEqual(products.require_products(self.root, cache_root=self.cache), held)
        self.assertFalse(held.data_root.exists())
        with self.assertRaises(products.ProductError):
            products.require_products(self.root, cache_root=self.cache)

    def test_selected_context_needs_only_selected_cache(self):
        shutil.rmtree(self.cache / self.family("b")["key"])
        with products.verified_products(self.root, cache_root=self.cache, product_ids=["a"]) as held:
            self.assertEqual(set(held.files), {"structure/a/index.json"})

    def test_input_edit_during_context_rejected(self):
        with self.assertRaisesRegex(products.ProductError, "inputs changed"):
            with products.verified_products(self.root, cache_root=self.cache):
                (self.root / "src/a/input.txt").write_text("changed")

    def test_descriptor_edit_during_context_rejected(self):
        with self.assertRaisesRegex(products.ProductError, "descriptor changed"):
            with products.verified_products(self.root, cache_root=self.cache):
                (self.root / products.MANIFEST_RELATIVE).write_text("{}")

    def test_snapshot_edit_during_context_rejected(self):
        with self.assertRaisesRegex(products.ProductError, "differ"):
            with products.verified_products(self.root, cache_root=self.cache) as held:
                held.files["structure/a/index.json"].write_text("tampered")

    def test_unsafe_paths_and_unknown_descriptor_fields(self):
        for name in ("../bad.json", "/bad.json", "structure/../bad.json", "a\\b.json", "a//b.json"):
            with self.subTest(name=name):
                value = copy.deepcopy(self.manifest)
                value["products"][0]["files"] = {name: {"sha256": "0" * 64, "bytes": 0}}
                self.write_manifest(value)
                with self.assertRaises(products.ProductError):
                    products.load_manifest(self.root)
        value = copy.deepcopy(self.manifest)
        value["unknown"] = "not ignored"
        self.write_manifest(value)
        with self.assertRaises(products.ProductError):
            products.load_manifest(self.root)

    def test_symlink_and_fifo_outputs_rejected_without_blocking(self):
        path = self.payload()
        original = path.read_bytes()
        path.unlink()
        path.symlink_to(self.root / "src/a/input.txt")
        with self.assertRaises(products.ProductError):
            products.check(self.root, cache_root=self.cache)
        path.unlink()
        os.mkfifo(path)
        with self.assertRaises(products.ProductError):
            products.check(self.root, cache_root=self.cache)
        path.unlink()
        path.write_bytes(original)

    def test_symlink_canonical_and_cache_ancestry_rejected(self):
        path = self.root / "src/a/link"
        path.symlink_to(self.root / "requirements-tools.txt")
        with self.assertRaises(products.ProductError):
            products.check(self.root, cache_root=self.cache)
        path.unlink()
        self.cache.rename(self.cache.with_name("real-cache"))
        self.cache.symlink_to("real-cache", target_is_directory=True)
        with self.assertRaises(products.ProductError):
            products.check(self.root, cache_root=self.cache)

    def test_no_receipt_or_descriptor_self_reference(self):
        before = products.input_identity(self.root)
        self.write_manifest({"irrelevant": True})
        for name in products.receipt.MECHANICAL_RECEIPTS:
            path = self.root / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text("different")
        self.assertEqual(before, products.input_identity(self.root))

    def test_two_build_disagreement_never_writes_descriptor(self):
        before = (self.root / products.MANIFEST_RELATIVE).read_bytes()
        shutil.rmtree(self.cache)
        def nondeterministic(root, out, ids):
            self.generate(root, out, ids)
            (out / "structure/a/index.json").write_text(str(len(self.generated)))
        with patch.object(products, "_generate", side_effect=nondeterministic):
            with self.assertRaises(products.ProductError):
                products.record(self.root, cache_root=self.cache)
        self.assertEqual(before, (self.root / products.MANIFEST_RELATIVE).read_bytes())

    def test_source_paths_are_canonical_minimal_binding(self):
        with products.verified_products(self.root, cache_root=self.cache) as held:
            self.assertIn(products.MANIFEST_RELATIVE, held.source_paths)
            self.assertIn("scripts/generator.py", held.source_paths)
            self.assertNotIn("src/a/input.txt", held.source_paths)
            self.assertFalse(any(".scratch" in name for name in held.source_paths))

    def test_policy_projection_no_cycle_and_no_unknown_fields(self):
        auth = {"basis": "user-attested", "authority_role": "owner", "authority_scope": [], "rights_record": "release/rights/test.md", "rights_record_sha256": "0" * 64,
                "site_sources": {}, "approved_on": "2026-01-01", "duration": "perpetual", "effective_at": "2026-01-01", "expires_at": None, "timezone": "UTC", "conditions": []}
        policy = {"schema_version": 2, "release_id": "alpha", "provider": "gpt", "providers": ["gpt"], "authorizations": {"standing": auth}}
        first = products._policy(json.dumps(policy).encode())
        auth["site_sources"] = {"release/browser-products.json": "1" * 64}
        auth["rights_record_sha256"] = "2" * 64
        self.assertEqual(first, products._policy(json.dumps(policy).encode()))
        auth["unknown"] = True
        with self.assertRaises(products.ProductError):
            products._policy(json.dumps(policy).encode())

    def test_rights_projection_preserves_prose(self):
        first = b"policy\n## Exact approved reader-facing site sources\n\n| Repository path | SHA-256 |\n| --- | --- |\n"
        row = ("| `release/browser-products.json` | `" + "a" * 64 + "` |\n").encode()
        self.assertEqual(products._rights(first), products._rights(first + row))
        self.assertNotEqual(products._rights(first), products._rights(first + row + b"condition changed\n"))

    def test_stable_aggregate_and_cache_writer_guard(self):
        aggregate = products.committed_data_root(self.root, cache_root=self.cache)
        self.assertTrue((aggregate / "structure/a/index.json").is_file())
        with patch.dict(os.environ, {"TRIPTYCH_BROWSER_DATA_ROOT": str(self.root / "different-cache")}):
            with self.assertRaises(products.ProductError):
                products.assert_working_output(self.root, aggregate / "new")
        self.assertEqual(products.assert_working_output(self.root, self.root / ".scratch/work"), self.root / ".scratch/work")

    def test_corrupt_stable_aggregate_rejected(self):
        aggregate = products.committed_data_root(self.root, cache_root=self.cache)
        (aggregate / "structure/a/index.json").write_text("bad")
        with self.assertRaises(products.ProductError):
            products.check(self.root, cache_root=self.cache)

    def test_hash_each_shared_input_once_per_phase(self):
        real = products._read
        paths = []
        def reading(root, name):
            paths.append(name)
            return real(root, name)
        with patch.object(products, "_read", side_effect=reading):
            products._identity_batch(self.root)
        self.assertEqual(paths.count("scripts/generator.py"), 1)
        self.assertEqual(paths.count("requirements-tools.txt"), 1)

    def test_unknown_lock_member_invalidates(self):
        (self.root / "new.lock").write_text("changed")
        with self.assertRaisesRegex(products.ProductError, "inputs changed"):
            products.check(self.root, cache_root=self.cache)

    def test_empty_extra_directory_rejected(self):
        (self.payload().parent / "extra").mkdir()
        with self.assertRaises(products.ProductError):
            products.check(self.root, cache_root=self.cache)

    def test_prune_retains_all_current_keys_and_removes_obsolete(self):
        obsolete = self.cache / ("a" * 64)
        obsolete.mkdir()
        (obsolete / "scratch.txt").write_text("disposable")
        products.prune(self.root, cache_root=self.cache)
        self.assertFalse(obsolete.exists())
        products.check(self.root, cache_root=self.cache)

    def test_prune_refuses_unknown_or_unsafe_entries(self):
        for name, link in (("unknown", False), ("a" * 64, True)):
            path = self.cache / name
            if link:
                path.symlink_to(self.root / "src", target_is_directory=True)
            else:
                path.mkdir()
            with self.assertRaises(products.ProductError):
                products.prune(self.root, cache_root=self.cache)
            if link:
                path.unlink()
            else:
                path.rmdir()

    def test_prune_cannot_remove_anything_when_current_cache_corrupt(self):
        obsolete = self.cache / ("a" * 64)
        obsolete.mkdir()
        self.payload().write_text("bad")
        with self.assertRaises(products.ProductError):
            products.prune(self.root, cache_root=self.cache)
        self.assertTrue(obsolete.exists())

    def test_reader_lock_rejects_nested_mutation(self):
        with products.verified_products(self.root, cache_root=self.cache):
            with self.assertRaisesRegex(products.ProductError, "read-only"):
                products.prune(self.root, cache_root=self.cache)
            with self.assertRaisesRegex(products.ProductError, "read-only"):
                products.build(self.root, cache_root=self.cache)

    def test_cache_lock_blocks_external_writer_and_releases(self):
        script = "import fcntl,os,sys; fd=os.open(sys.argv[1],os.O_RDWR); fcntl.flock(fd,fcntl.LOCK_EX|fcntl.LOCK_NB)"
        with products._cache_lock(self.root, self.cache):
            lock_path = self.root / ".scratch/next-product-store" / ("cache-" + products._sha(str(self.cache).encode()) + ".lock")
            blocked = subprocess.run([sys.executable, "-B", "-c", script, str(lock_path)], capture_output=True)
            self.assertNotEqual(blocked.returncode, 0)
        released = subprocess.run([sys.executable, "-B", "-c", script, str(lock_path)], capture_output=True)
        self.assertEqual(released.returncode, 0, released.stderr)

    def test_extra_cache_root_files_and_obsolete_key_links_rejected(self):
        for name, link in (("unexpected.json", False), ("a" * 64, True)):
            path = self.cache / name
            if link:
                path.symlink_to(self.root / "src", target_is_directory=True)
            else:
                path.write_text("{}")
            with self.assertRaises(products.ProductError):
                products.check(self.root, cache_root=self.cache)
            path.unlink()

    def test_check_never_starts_a_producer_network_or_evidence_fetch(self):
        with patch("subprocess.run", side_effect=AssertionError("producer/research command")), \
             patch("urllib.request.urlopen", side_effect=AssertionError("network")), \
             patch.object(products.receipt._artifact_store, "hydrate", side_effect=AssertionError("evidence fetch")):
            products.check(self.root, cache_root=self.cache)
        self.assertEqual(self.generated, [])

    def test_descriptor_change_during_record_is_not_overwritten(self):
        changed = self.root / products.MANIFEST_RELATIVE
        original_generate = self.generate
        def editing(root, out, ids):
            original_generate(root, out, ids)
            changed.write_text("concurrent descriptor edit")
        shutil.rmtree(self.cache)
        with patch.object(products, "_generate", side_effect=editing):
            with self.assertRaisesRegex(products.ProductError, "descriptor changed"):
                products.record(self.root, cache_root=self.cache)
        self.assertEqual(changed.read_text(), "concurrent descriptor edit")

    def test_hardlinked_product_is_rejected(self):
        linked = self.root / ".scratch/linked-product"
        os.link(self.payload(), linked)
        with self.assertRaises(products.ProductError):
            products.check(self.root, cache_root=self.cache)

    def declare_archived_snapshot(self):
        self.recipes[0]["input_trees"].append("release/papal-documents")
        body = b'{"historical":"unchanged"}\n'
        digest = products._sha(body)
        relative = "release/papal-documents/inputs/" + digest + ".json"
        reference = {"path": relative, "sha256": digest, "bytes": len(body)}
        metadata = {
            "release/papal-documents/input-delivery.json": {"schema": "triptych-papal-input-delivery/v1", "artifacts": [reference]},
            "release/papal-documents/input-records.json": {"schema": "fixture-record-attestation/v1", "originals": [reference]},
            "release/papal-documents/input-records/record.json": {"title": "attested source record"},
            "release/papal-documents/reports/report.json": {"status": "recorded"},
        }
        for name, value in metadata.items():
            path = self.root / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(json.dumps(value))
        self.manifest = products.record(self.root, cache_root=self.cache)
        return relative, body, metadata

    def test_optional_declared_original_snapshot_does_not_change_any_identity(self):
        relative, body, _ = self.declare_archived_snapshot()
        before = products._identity_batch(self.root)
        path = self.root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(body)
        self.assertEqual(before, products._identity_batch(self.root))
        products.check(self.root, cache_root=self.cache)
        path.unlink()
        self.assertEqual(before, products._identity_batch(self.root))
        products.check(self.root, cache_root=self.cache)
        self.assertTrue(all(relative not in identity["source_paths"] for identity in before.values()))

    def test_snapshot_delivery_attestation_records_and_reports_remain_bound(self):
        _, _, metadata = self.declare_archived_snapshot()
        before = products._identity_batch(self.root)
        for name in metadata:
            with self.subTest(name=name):
                path = self.root / name
                original = path.read_bytes()
                path.write_bytes(original + b" ")
                after = products._identity_batch(self.root)
                self.assertNotEqual(before[None]["sha256"], after[None]["sha256"])
                self.assertNotEqual(before["a"]["sha256"], after["a"]["sha256"])
                with self.assertRaisesRegex(products.ProductError, "inputs changed"):
                    products.check(self.root, cache_root=self.cache)
                path.write_bytes(original)
        unknown = self.root / "release/papal-documents/new-canonical-metadata.json"
        unknown.write_text("{}")
        with self.assertRaisesRegex(products.ProductError, "inputs changed"):
            products.check(self.root, cache_root=self.cache)

    def test_only_regular_code_cache_bytecode_is_ignored(self):
        before = products._identity_batch(self.root)
        for scope, suffix in (("scripts", ".pyc"), ("tools", ".pyo")):
            path = self.root / scope / "__pycache__" / ("generated" + suffix)
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(b"disposable bytecode")
        self.assertEqual(before, products._identity_batch(self.root))
        products.check(self.root, cache_root=self.cache)

    def test_nonbytecode_cache_members_remain_governed(self):
        before = products._identity_batch(self.root)
        for name in ("scripts/__pycache__/metadata.json", "tools/__pycache__/notes.txt",
                     "scripts/__pycache__/nested.pyc/source.txt", "scripts/not-a-cache.pyc",
                     "src/a/__pycache__/source.pyc"):
            with self.subTest(name=name):
                path = self.root / name
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text("governed input")
                after = products._identity_batch(self.root)
                self.assertIn(name, after[None]["source_paths"])
                self.assertNotEqual(before[None]["sha256"], after[None]["sha256"])
                with self.assertRaisesRegex(products.ProductError, "inputs changed"):
                    products.check(self.root, cache_root=self.cache)
                path.unlink()
                self.assertEqual(before, products._identity_batch(self.root))

    def test_bytecode_named_symlinks_and_fifos_are_rejected_before_exclusion(self):
        for scope in ("scripts", "tools"):
            for kind in ("symlink", "fifo"):
                with self.subTest(scope=scope, kind=kind):
                    relative = scope + "/__pycache__/unsafe.pyc"
                    path = self.root / relative
                    path.parent.mkdir(parents=True, exist_ok=True)
                    if kind == "symlink":
                        path.symlink_to(self.root / "requirements-tools.txt")
                    else:
                        os.mkfifo(path)
                    try:
                        with self.assertRaises(products.ProductError):
                            products.check(self.root, cache_root=self.cache)
                        with self.assertRaises(products.ProductError):
                            products._paths(self.root, trees=(), files=(relative,))
                    finally:
                        path.unlink()

    def test_excluded_mechanical_receipts_still_receive_filesystem_preflight(self):
        for name in products.receipt.MECHANICAL_RECEIPTS - {products.MANIFEST_RELATIVE}:
            for kind in ("symlink", "fifo"):
                with self.subTest(name=name, kind=kind):
                    path = self.root / name
                    path.parent.mkdir(parents=True, exist_ok=True)
                    if kind == "symlink":
                        path.symlink_to(self.root / "requirements-tools.txt")
                    else:
                        os.mkfifo(path)
                    try:
                        with self.assertRaises(products.ProductError):
                            products.input_identity(self.root)
                    finally:
                        path.unlink()

    def test_working_root_never_points_at_sealed_cache(self):
        with patch.dict(os.environ, {"TRIPTYCH_BROWSER_DATA_ROOT": ".scratch/browser-data"}):
            self.assertEqual(products.working_data_root(self.root), self.root / ".scratch/browser-data-work")


class BrowserDeliveryTests(unittest.TestCase):
    family = BrowserProductsTests.family
    payload = BrowserProductsTests.payload

    def setUp(self):
        BrowserProductsTests.setUp(self)

    def generate(self, root, out, product_ids=None):
        ids = product_ids or [recipe["id"] for recipe in self.recipes]
        public = [name for name in ids if name != "print-editions"]
        if public:
            BrowserProductsTests.generate(self, root, out, public)
        if "print-editions" in ids:
            self.generated.append(("print-editions",))
            target = out / "print/preparation/editions.json"
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text('{"html":"<p>Prepared from canonical source</p>"}')

    def add_print_family(self):
        self.recipes.append({"id": "print-editions", "version": 1,
                             "output_prefixes": ["print/preparation"], "delivery": "print-preparation",
                             "argv": ["scripts/_web_print_products.py", "--root", "{root}", "--out", "{out}"],
                             "input_trees": ["src/common"], "input_files": [], "exclude_paths": []})
        self.manifest = products.record(self.root, cache_root=self.cache)

    def test_every_full_and_selected_snapshot_has_exact_explicit_deliveries(self):
        self.add_print_family()
        with products.verified_products(self.root, cache_root=self.cache) as held:
            self.assertEqual(set(held.delivery_by_path), set(held.files))
            self.assertEqual(held.delivery_by_path["structure/a/index.json"], "browser-data")
            self.assertEqual(held.delivery_by_path["print/preparation/editions.json"], "print-preparation")
        with products.verified_products(self.root, cache_root=self.cache, product_ids=["print-editions"]) as held:
            self.assertEqual(held.delivery_by_path, {"print/preparation/editions.json": "print-preparation"})
            self.assertEqual(set(held.delivery_by_path), set(held.files))
        with products.verified_products(self.root, cache_root=self.cache, product_ids=["a"]) as held:
            self.assertEqual(held.delivery_by_path, {"structure/a/index.json": "browser-data"})

    def test_missing_unknown_and_untyped_delivery_are_rejected_without_defaults(self):
        for value in (None, True, "private", "browser-data "):
            recipes = copy.deepcopy(self.recipes)
            recipes[0]["delivery"] = value
            with self.subTest(value=value), self.assertRaises(products.ProductError):
                products._validate_recipes(recipes)
        recipes = copy.deepcopy(self.recipes)
        del recipes[0]["delivery"]
        with self.assertRaises(products.ProductError):
            products._validate_recipes(recipes)
        descriptor = copy.deepcopy(self.manifest)
        del descriptor["recipes"][0]["delivery"]
        with self.assertRaises(products.ProductError):
            products._validate_manifest(descriptor)

    def test_ambiguous_private_prefix_and_unknown_owners_are_rejected(self):
        self.add_print_family()
        recipes = copy.deepcopy(self.recipes)
        recipes[0]["output_prefixes"] = ["print"]
        with self.assertRaisesRegex(products.ProductError, "prefixes overlap"):
            products._validate_recipes(recipes)
        selected = [{"id": "unknown", "files": {"print/preparation/unowned.json": {}}}]
        with self.assertRaisesRegex(products.ProductError, "no delivery owner"):
            products._deliveries(self.manifest, selected)
        selected = [{"id": "a", "files": {"print/preparation/unowned.json": {}}}]
        with self.assertRaisesRegex(products.ProductError, "delivery ownership"):
            products._deliveries(self.manifest, selected)

    def test_asset_manifest_is_bound_but_browser_style_is_not_a_print_input(self):
        self.add_print_family()
        before = products.input_identity(self.root, "print-editions")
        global_before = products.input_identity(self.root)
        style = self.root / "src/web/browser/shared/print.css"
        style.parent.mkdir(parents=True)
        style.write_text("body { color: black; }")
        self.assertEqual(before, products.input_identity(self.root, "print-editions"))
        self.assertNotEqual(global_before, products.input_identity(self.root))
        asset_manifest = self.root / "src/common/browser-print-assets.json"
        asset_manifest.parent.mkdir(parents=True)
        asset_manifest.write_text('{"assets":[]}')
        after = products.input_identity(self.root, "print-editions")
        self.assertIn("src/common/browser-print-assets.json", after["source_paths"])
        self.assertNotEqual(before["sha256"], after["sha256"])


class BrowserCandidateReuseTests(unittest.TestCase):
    """New input keys may reuse bytes, never another input proof."""

    generate = BrowserProductsTests.generate
    family = BrowserProductsTests.family
    payload = BrowserProductsTests.payload

    def setUp(self):
        BrowserProductsTests.setUp(self)
        self.old_manifest = copy.deepcopy(self.manifest)
        self.old_family = next(item for item in self.old_manifest["products"] if item["id"] == "a")
        self.old_data = self.cache / self.old_family["key"] / "data"
        self.index_path = self.cache / products.CANDIDATE_INDEX

    def new_input_epoch(self, *, changed_bytes=False):
        path = self.root / ("src/a/input.txt" if changed_bytes else "scripts/generator.py")
        path.write_text("new source bytes\n" if changed_bytes else "changed generator; same output bytes\n")
        self.generated.clear()
        self.manifest = products.record(self.root, cache_root=self.cache)
        self.generated.clear()
        current_a = self.family()
        self.assertNotEqual(current_a["key"], self.old_family["key"])
        shutil.rmtree(self.cache / current_a["key"])
        shutil.rmtree(self.cache / products.products_identity(self.manifest))
        return current_a

    def write_index(self, value):
        self.index_path.write_text(json.dumps(value))

    def test_new_input_key_reuses_only_current_committed_identical_bytes(self):
        current = self.new_input_epoch()
        before = (self.root / products.MANIFEST_RELATIVE).read_bytes()
        products.build(self.root, cache_root=self.cache)
        self.assertEqual(self.generated, [])
        self.assertEqual(products.last_build_stats(), {"reused_families": ["a"], "generated_families": []})
        self.assertEqual(before, (self.root / products.MANIFEST_RELATIVE).read_bytes())
        self.assertEqual(products.validate_candidate_entry(self.cache, current["key"], products.candidate_hint(current["files"])), current["files"])

    def test_changed_expected_bytes_generate_only_the_changed_family(self):
        self.new_input_epoch(changed_bytes=True)
        products.build(self.root, cache_root=self.cache)
        self.assertEqual(self.generated, [("a",)])
        self.assertEqual(products.last_build_stats(), {"reused_families": [], "generated_families": ["a"]})

    def test_unhinted_bytes_and_unrelated_hints_are_not_opened(self):
        self.new_input_epoch()
        index = products.load_candidate_index(self.cache)
        index["entries"][self.old_family["key"]]["files_sha256"] = "0" * 64
        self.write_index(index)
        with patch.object(products, "validate_candidate_entry", side_effect=AssertionError("unrelated candidate opened")):
            products.build(self.root, cache_root=self.cache)
        self.assertEqual(self.generated, [("a",)])

    def test_current_corruption_is_fatal_with_a_matching_alternate(self):
        current = self.new_input_epoch()
        shutil.copytree(self.old_data.parent, self.cache / current["key"])
        self.payload().write_text("bad current bytes")
        with self.assertRaisesRegex(products.ProductError, "differ"):
            products.build(self.root, cache_root=self.cache)
        self.assertEqual(self.generated, [])

    def test_matching_candidate_missing_extra_or_changed_bytes_are_fatal(self):
        for kind in ("missing", "extra", "hash", "size", "envelope"):
            with self.subTest(kind=kind), tempfile.TemporaryDirectory(dir=self.root / ".scratch") as backup:
                saved = Path(backup) / "entry"
                shutil.copytree(self.old_data.parent, saved)
                current = self.new_input_epoch() if kind == "missing" else self.family()
                target = self.old_data / "structure/a/index.json"
                original = target.read_bytes()
                if kind == "missing": target.unlink()
                elif kind == "extra": (self.old_data / "extra.json").write_text("{}")
                elif kind == "hash":
                    stamp = target.stat()
                    target.write_bytes(b"x" * len(original))
                    os.utime(target, ns=(stamp.st_atime_ns, stamp.st_mtime_ns))
                elif kind == "size": target.write_bytes(original + b" ")
                else: (self.old_data.parent / "receipt.json").write_text("{}")
                with self.assertRaises(products.ProductError):
                    products.build(self.root, cache_root=self.cache)
                self.assertFalse((self.cache / current["key"]).exists())
                self.assertEqual(self.generated, [])
                shutil.rmtree(self.old_data.parent)
                shutil.copytree(saved, self.old_data.parent)

    def test_matching_candidate_links_and_special_files_are_never_followed(self):
        current = self.new_input_epoch()
        target = self.old_data / "structure/a/index.json"
        original = target.read_bytes()
        outside = self.root / ".scratch/outside.json"
        outside.write_bytes(original)
        for kind in ("symlink", "hardlink", "fifo"):
            with self.subTest(kind=kind):
                target.unlink()
                if kind == "symlink": target.symlink_to(outside)
                elif kind == "hardlink": os.link(outside, target)
                else: os.mkfifo(target)
                try:
                    with self.assertRaises(products.ProductError):
                        products.build(self.root, cache_root=self.cache)
                    self.assertFalse((self.cache / current["key"]).exists())
                    self.assertEqual(outside.read_bytes(), original)
                    self.assertEqual(self.generated, [])
                finally:
                    target.unlink()
                    target.write_bytes(original)

    def test_matching_missing_entry_hint_is_fatal(self):
        current = self.new_input_epoch()
        shutil.rmtree(self.old_data.parent)
        with self.assertRaises(products.ProductError):
            products.build(self.root, cache_root=self.cache)
        self.assertFalse((self.cache / current["key"]).exists())
        self.assertEqual(self.generated, [])

    def test_candidate_membership_race_cannot_promote_a_current_key(self):
        current = self.new_input_epoch()
        before = self.index_path.read_bytes()
        reading = products._read
        def mutate(root, name):
            body = reading(root, name)
            if root == self.old_data:
                (self.old_data / "raced.json").write_text("{}")
            return body
        with patch.object(products, "_read", side_effect=mutate):
            with self.assertRaisesRegex(products.ProductError, "differ"):
                products.build(self.root, cache_root=self.cache)
        self.assertFalse((self.cache / current["key"]).exists())
        self.assertEqual(self.index_path.read_bytes(), before)
        self.assertEqual(self.generated, [])

    def test_candidate_reuse_still_brackets_current_inputs_and_descriptor(self):
        self.new_input_epoch()
        reading = products._read
        def mutate(root, name):
            body = reading(root, name)
            if root == self.old_data:
                (self.root / "src/a/input.txt").write_text("concurrent source edit")
            return body
        with patch.object(products, "_read", side_effect=mutate):
            with self.assertRaisesRegex(products.ProductError, "inputs changed"):
                products.build(self.root, cache_root=self.cache)

    def test_hint_schema_rejects_unknown_fields_types_and_duplicate_keys(self):
        self.new_input_epoch()
        good = products.load_candidate_index(self.cache)
        for field, value in (("count", True), ("bytes", True), ("files_sha256", "bad"), ("unknown", "ignored")):
            index = copy.deepcopy(good)
            index["entries"][self.old_family["key"]][field] = value
            self.write_index(index)
            with self.subTest(field=field), self.assertRaises(products.ProductError):
                products.build(self.root, cache_root=self.cache)
        self.index_path.write_text('{"schema":"triptych-browser-product-candidates/v1","entries":{},"entries":{}}')
        with self.assertRaisesRegex(products.ProductError, "duplicate"):
            products.load_candidate_index(self.cache)

    def test_record_with_changed_inputs_still_runs_two_fresh_producers(self):
        (self.root / "scripts/generator.py").write_text("new input, unchanged bytes")
        with patch.object(products, "_reuse_candidate", side_effect=AssertionError("record reused candidate bytes")):
            products.record(self.root, cache_root=self.cache)
        self.assertEqual(self.generated, [("a", "b"), ("a", "b")])

    def test_prune_keeps_only_current_hints_and_still_rejects_arbitrary_files(self):
        self.new_input_epoch()
        products.build(self.root, cache_root=self.cache)
        products.prune(self.root, cache_root=self.cache)
        expected = {products.products_identity(self.manifest), *(item["key"] for item in self.manifest["products"])}
        self.assertEqual(set(products.load_candidate_index(self.cache)["entries"]), expected)
        self.assertTrue(self.index_path.is_file())
        (self.cache / "arbitrary.json").write_text("{}")
        with self.assertRaises(products.ProductError):
            products.prune(self.root, cache_root=self.cache)


if __name__ == "__main__":
    unittest.main()
