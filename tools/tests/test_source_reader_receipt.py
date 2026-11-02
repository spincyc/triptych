#!/usr/bin/env python3
"""A fast projection proof fails closed when its source or output set changes."""
from __future__ import annotations

import argparse
from contextlib import contextmanager
import hashlib
import importlib.machinery
import importlib.util
import json
import os
from pathlib import Path
import py_compile
import shutil
import subprocess
import sys
import tempfile
from types import SimpleNamespace
import unittest
from unittest import mock

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))
import _source_projection_receipt as proof

loader = importlib.machinery.SourceFileLoader("receipt_reader_under_test", str(ROOT / "tools/source-reader"))
spec = importlib.util.spec_from_loader(loader.name, loader)
reader = importlib.util.module_from_spec(spec)
sys.modules[loader.name] = reader
loader.exec_module(reader)


class ProjectionReceiptTests(unittest.TestCase):
    def setUp(self):
        scratch = ROOT / ".scratch/next-source-receipt"
        scratch.mkdir(parents=True, exist_ok=True)
        self.temporary = tempfile.TemporaryDirectory(dir=scratch, prefix="test-")
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        subprocess.run(["git", "init", "-q", str(self.root)], check=True)
        self.source = "src/sources/works/example/work/work.toml"
        for name, value in {
            self.source: "source identity and rights\n",
            "tools/source-reader": "generator\n",
            "scripts/policy.py": "rights helper\n",
            "guidance/sources.md": "rights and ownership policy\n",
            "workflows/reviews/authority.json": "{}\n",
            "src/gpt/example/research/source-bindings.toml": "binding\n",
            "src/gpt/example/main.tex": "provider source\n",
            "src/web/browser/sources/reader-model.js": "browser schema\n",
        }.items():
            self.write(name, value)
        self.target = self.root / ".scratch/committed-products/structure/sources"
        self.write(".scratch/committed-products/structure/sources/index.json", '{"schema":"fixture"}\n')
        self.write(".scratch/committed-products/structure/sources/text/passage.example.json", '{"text":"Held wording"}\n')
        (self.root / "src/sources/inventories").mkdir(parents=True)
        subprocess.run(["git", "-C", str(self.root), "add", "."], check=True)

    def write(self, name, value):
        path = self.root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(value, encoding="utf-8")
        return path

    def make_receipt(self):
        receipt = {"schema": proof.RECEIPT_SCHEMA, "projection_schema": reader.SCHEMA,
                   "proof": "independent-full-structure-check", "editorial_approval": False,
                   "inputs": proof.input_identity(self.root),
                   "outputs": proof.output_identity(self.root, self.target),
                   "counted": {"works": 1, "editions": 1, "artifacts": 1, "passages": 1, "readable": 1}}
        self.write(proof.RECEIPT_PATH, json.dumps(receipt))
        return receipt

    def check(self):
        return proof.check_receipt(self.root, self.target, reader.SCHEMA)

    @contextmanager
    def verified(self, root, *, cache_root=None, product_ids=None):
        self.assertEqual(root, self.root)
        self.assertEqual(product_ids, ["sources"])
        self.verified_live = True
        try:
            yield SimpleNamespace(data_root=self.target.parent.parent, products_identity="a" * 64)
        finally:
            self.verified_live = False

    def arguments(self, **values):
        return argparse.Namespace(**{"out": None, "cache_root": None, "check": False,
                                     "check_receipt": False, "record_receipt": False, **values})

    def test_fast_check_never_loads_graph_or_launches_full_replay(self):
        self.make_receipt()
        arguments = self.arguments(check_receipt=True, cache_root=".scratch/selected-cache")
        with mock.patch.object(reader, "ROOT", self.root), mock.patch.object(reader, "load", side_effect=AssertionError("graph loaded")), mock.patch.object(proof, "record_receipt", side_effect=AssertionError("full replay")), mock.patch("_browser_products.verified_products", side_effect=self.verified) as held:
            answer = reader.run_structure(arguments)
        held.assert_called_once_with(self.root, cache_root=".scratch/selected-cache", product_ids=["sources"])
        self.assertEqual(answer["status"], "ok")
        self.assertEqual(answer["files"], 2)
        self.assertEqual(answer["current"], "structure/sources")
        self.assertEqual(answer["products_identity"], "a" * 64)
        self.assertFalse(answer["editorial_approval"])

    def test_record_cli_holds_verified_selected_family_for_the_full_operation(self):
        candidate = self.make_receipt()

        def record(root, target, schema, *, write):
            self.assertTrue(self.verified_live)
            self.assertEqual((root, target, schema), (self.root, self.target, reader.SCHEMA))
            self.assertFalse(write)
            return candidate

        def commit(root, value):
            self.assertFalse(self.verified_live)
            self.assertEqual((root, value), (self.root, candidate))

        with mock.patch.object(reader, "ROOT", self.root), mock.patch("_browser_products.verified_products", side_effect=self.verified), mock.patch.object(proof, "record_receipt", side_effect=record), mock.patch.object(proof, "write_receipt", side_effect=commit) as written:
            answer = reader.run_structure(self.arguments(record_receipt=True))
        written.assert_called_once()
        self.assertFalse(self.verified_live)
        self.assertTrue(answer["receipt_recorded"])

    def test_bad_committed_cache_never_falls_back_to_working_or_legacy_data(self):
        from _browser_products import ProductError
        self.make_receipt()
        with mock.patch.object(reader, "ROOT", self.root), mock.patch("_browser_products.verified_products", side_effect=ProductError("committed cache is corrupt")), mock.patch.object(proof, "check_receipt", side_effect=AssertionError("unverified fallback")), self.assertRaisesRegex(reader.ReaderError, "committed cache is corrupt"):
            reader.run_structure(self.arguments(check_receipt=True))

    def test_receipt_check_uses_a_real_committed_family_without_old_snapshot(self):
        import _browser_products as products
        self.make_receipt()
        shutil.rmtree(self.target.parent.parent)
        (self.root / "release").mkdir()
        cache = self.root / ".scratch/sealed-cache"
        recipes = [{"id": "sources", "version": 1, "output_prefixes": ["structure/sources"],
                    "argv": ["tools/source-reader", "structure", "--strict"],
                    "input_trees": ["src/sources", "src/gpt"], "input_files": [], "exclude_paths": []}]

        def generate(root, out, product_ids=None):
            self.assertEqual(product_ids, ["sources"])
            for name, body in (("index.json", '{"schema":"fixture"}\n'),
                               ("text/passage.example.json", '{"text":"Held wording"}\n')):
                target = out / "structure/sources" / name
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_text(body)

        with mock.patch.object(products, "_recipes", return_value=recipes), mock.patch.object(products, "_generate", side_effect=generate):
            manifest = products.record(self.root, cache_root=cache)
            with mock.patch.object(reader, "ROOT", self.root), mock.patch.object(reader, "load", side_effect=AssertionError("graph loaded")), mock.patch.object(products, "_generate", side_effect=AssertionError("implicit generation")):
                answer = reader.run_structure(self.arguments(check_receipt=True, cache_root=str(cache)))
        self.assertEqual(answer["status"], "ok")
        self.assertEqual(answer["products_identity"], products.products_identity(manifest))
        self.assertFalse(self.target.exists())
        self.assertFalse((self.root / "src/web/data").exists())

    def test_verification_failure_on_context_exit_prevents_success(self):
        from _browser_products import ProductError
        self.make_receipt()

        @contextmanager
        def changed(*args, **kwargs):
            with self.verified(*args, **kwargs) as held:
                yield held
            raise ProductError("cache changed during receipt check")

        with mock.patch.object(reader, "ROOT", self.root), mock.patch("_browser_products.verified_products", side_effect=changed), self.assertRaisesRegex(reader.ReaderError, "cache changed"):
            reader.run_structure(self.arguments(check_receipt=True))

    def test_failed_product_context_never_commits_a_prepared_receipt(self):
        from _browser_products import ProductError
        candidate = self.make_receipt()
        prior = (self.root / proof.RECEIPT_PATH).read_bytes()

        @contextmanager
        def changed(*args, **kwargs):
            with self.verified(*args, **kwargs) as held:
                yield held
            raise ProductError("descriptor changed before commit")

        with mock.patch.object(reader, "ROOT", self.root), mock.patch("_browser_products.verified_products", side_effect=changed), mock.patch.object(proof, "record_receipt", return_value=candidate), mock.patch.object(proof, "write_receipt") as written, self.assertRaisesRegex(reader.ReaderError, "descriptor changed before commit"):
            reader.run_structure(self.arguments(record_receipt=True))
        written.assert_not_called()
        self.assertEqual((self.root / proof.RECEIPT_PATH).read_bytes(), prior)

    def test_receipt_flags_reject_an_arbitrary_working_output(self):
        for flag in ("check_receipt", "record_receipt"):
            with self.subTest(flag=flag), self.assertRaisesRegex(reader.ReaderError, "use --cache-root"):
                reader.run_structure(self.arguments(out="unverified-output", **{flag: True}))

    def test_output_and_receipt_options_keep_their_values_before_the_verb(self):
        def parse(**values):
            return values["parser"].parse_args(values["argv"])

        with mock.patch.object(reader, "run_verb_cli", side_effect=parse):
            selected = reader.main(["--cache-root", "chosen-cache", "--check-receipt", "structure"])
            output = reader.main(["--out", "chosen-output", "structure"])
        self.assertEqual(selected.cache_root, "chosen-cache")
        self.assertTrue(selected.check_receipt)
        self.assertEqual(output.out, "chosen-output")

    def test_cold_producer_needs_no_descriptor_or_previous_projection(self):
        target = self.root / ".scratch/new-working-data"
        with mock.patch.object(reader, "ROOT", self.root), mock.patch.object(reader, "load", return_value=object()), mock.patch.object(reader, "corpus", return_value=[]), mock.patch("_browser_products.load_manifest", side_effect=AssertionError("old descriptor required")):
            answer = reader.run_structure(self.arguments(out=str(target)))
            checked = reader.run_structure(self.arguments(out=str(target), check=True))
        self.assertEqual(answer["status"], "ok")
        self.assertEqual(checked["status"], "ok")
        self.assertEqual(answer["files"], 1)
        self.assertTrue((target / "structure/sources/index.json").is_file())
        self.assertFalse((self.root / "src/web/data").exists())

    def test_default_producer_uses_the_shared_unsealed_working_root(self):
        selected = self.root / ".scratch/selected-cache"
        with mock.patch.dict(os.environ, {"TRIPTYCH_BROWSER_DATA_ROOT": str(selected)}), mock.patch.object(reader, "ROOT", self.root), mock.patch.object(reader, "load", return_value=object()), mock.patch.object(reader, "corpus", return_value=[]):
            reader.run_structure(self.arguments())
        self.assertTrue((selected.with_name("selected-cache-work") / "structure/sources/index.json").is_file())
        self.assertFalse(selected.exists())

    def test_ordinary_producer_cannot_modify_sealed_cache(self):
        selected = self.root / ".scratch/selected-cache"
        with mock.patch.dict(os.environ, {"TRIPTYCH_BROWSER_DATA_ROOT": str(selected)}), mock.patch.object(reader, "ROOT", self.root), mock.patch.object(reader, "load", side_effect=AssertionError("generator should not run")), self.assertRaisesRegex(reader.ReaderError, "outside the sealed"):
            reader.run_structure(self.arguments(out=str(selected / "key/data")))
        self.assertFalse(selected.exists())

    def test_old_sealed_cache_stays_protected_after_environment_change(self):
        original = self.root / ".scratch/old-cache"
        self.write(".scratch/old-cache/.browser-products-cache-v1", "")
        with mock.patch.dict(os.environ, {"TRIPTYCH_BROWSER_DATA_ROOT": str(self.root / ".scratch/new-cache")}), mock.patch.object(reader, "ROOT", self.root), self.assertRaisesRegex(reader.ReaderError, "outside the sealed"):
            reader.run_structure(self.arguments(out=str(original / "key/data")))

    def test_product_descriptors_and_old_generated_snapshots_are_not_inputs(self):
        before = proof.input_identity(self.root)
        self.write("release/browser-products.json", '{"mechanical":"descriptor"}')
        self.write("src/web/data/structure/sources/old.json", '{"old":"snapshot"}')
        self.assertEqual(before, proof.input_identity(self.root))
        (self.root / "src/web/data/structure/sources/old.json").unlink()
        self.assertEqual(before, proof.input_identity(self.root))

    def test_same_size_source_edit_with_restored_mtime_is_stale(self):
        self.make_receipt()
        path = self.root / self.source
        previous = path.stat()
        path.write_text("SOURCE identity and rights\n")
        os.utime(path, ns=(previous.st_atime_ns, previous.st_mtime_ns))
        with self.assertRaisesRegex(proof.ReceiptError, "inputs changed"):
            self.check()

    def test_generator_policy_binding_and_authority_changes_are_stale(self):
        for name in ("tools/source-reader", "scripts/policy.py", "guidance/sources.md",
                     "workflows/reviews/authority.json", "src/gpt/example/main.tex",
                     "src/gpt/example/research/source-bindings.toml",
                     "src/web/browser/sources/reader-model.js"):
            with self.subTest(name=name):
                self.make_receipt()
                path = self.root / name
                original = path.read_text()
                path.write_text(original + "changed")
                with self.assertRaisesRegex(proof.ReceiptError, "inputs changed"):
                    self.check()
                path.write_text(original)

    def test_new_untracked_and_tracked_source_paths_invalidate_membership(self):
        self.make_receipt()
        path = self.write("src/sources/new-source.toml", "unknown source file\n")
        with self.assertRaisesRegex(proof.ReceiptError, "inputs changed"):
            self.check()
        subprocess.run(["git", "-C", str(self.root), "add", str(path)], check=True)
        with self.assertRaisesRegex(proof.ReceiptError, "inputs changed"):
            self.check()

    def test_local_ignore_rules_cannot_hide_new_source_inputs(self):
        self.write(".gitignore", "*.toml\n")
        (self.root / ".git/info/exclude").write_text("hidden-source.json\n")
        self.make_receipt()
        self.write("src/sources/hidden-source.json", "unknown ignored source\n")
        with self.assertRaisesRegex(proof.ReceiptError, "inputs changed"):
            self.check()
        (self.root / "src/sources/hidden-source.json").unlink()
        self.write("src/sources/new-hidden.toml", "new ignored manifest\n")
        with self.assertRaisesRegex(proof.ReceiptError, "inputs changed"):
            self.check()

    def test_missing_unknown_source_is_never_a_valid_external_absence(self):
        self.make_receipt()
        (self.root / self.source).unlink()
        with self.assertRaisesRegex(proof.ReceiptError, "missing or unsafe input"):
            self.check()

    def test_untracked_fifo_omitted_by_git_is_rejected_without_opening_it(self):
        self.make_receipt()
        name = "src/sources/unknown.toml"
        os.mkfifo(self.root / name)
        listed = subprocess.check_output(["git", "-C", str(self.root), "ls-files", "--others"])
        self.assertNotIn(name.encode(), listed)
        with self.assertRaisesRegex(proof.ReceiptError, "unsafe governing input"):
            self.check()

    def test_untracked_socket_omitted_by_git_is_rejected(self):
        self.make_receipt()
        # A relative bind keeps the UNIX address below its platform length
        # limit while the socket's filesystem entry stays in this fixture.
        subprocess.run([sys.executable, "-B", "-c",
                        "import socket; endpoint=socket.socket(socket.AF_UNIX); "
                        "endpoint.bind('src/sources/unknown.socket')"], cwd=self.root, check=True)
        with self.assertRaisesRegex(proof.ReceiptError, "unsafe governing input"):
            self.check()

    def test_physical_membership_catches_regular_files_git_omits(self):
        before = proof.input_identity(self.root)
        self.write("src/sources/unreported.toml", "present source")
        original_run = proof.subprocess.run

        def omit(command, **kwargs):
            result = original_run(command, **kwargs)
            return subprocess.CompletedProcess(result.args, result.returncode,
                stdout=result.stdout.replace(b"src/sources/unreported.toml\0", b""), stderr=result.stderr)

        with mock.patch.object(proof.subprocess, "run", side_effect=omit):
            self.assertNotEqual(before, proof.input_identity(self.root))

    def test_special_input_created_during_hash_is_rejected_by_final_preflight(self):
        original_hash = proof._file_hash
        injected = False

        def add_fifo(root, relative):
            nonlocal injected
            result = original_hash(root, relative)
            if not injected:
                os.mkfifo(self.root / "src/sources/late-unknown.toml")
                injected = True
            return result

        with mock.patch.object(proof, "_file_hash", side_effect=add_fifo), self.assertRaisesRegex(proof.ReceiptError, "unsafe governing input"):
            proof.input_identity(self.root)

    def test_all_output_bytes_and_membership_are_checked(self):
        for mutation in ("changed", "missing", "extra-json", "extra-other"):
            with self.subTest(mutation=mutation):
                self.make_receipt()
                path = self.target / "text/passage.example.json"
                original = path.read_text()
                extra = None
                if mutation == "changed":
                    path.write_text('{"text":"unapproved wording"}')
                elif mutation == "missing":
                    path.unlink()
                else:
                    extra = self.target / ("orphan.json" if mutation == "extra-json" else "orphan.txt")
                    extra.write_text("{}")
                with self.assertRaises(proof.ReceiptError):
                    self.check()
                path.write_text(original)
                if extra:
                    extra.unlink()

    def test_receipts_do_not_depend_on_each_other(self):
        self.make_receipt()
        self.write("src/sources/inventories/act-history-projection-receipt-v1.json", "{}").write_text("different proof")
        self.assertEqual(self.check()["schema"], proof.RECEIPT_SCHEMA)

    def test_regular_python_cache_files_remain_excluded(self):
        before = proof.input_identity(self.root)
        self.write("scripts/__pycache__/generated.cpython-314.pyc", "derived code cache")
        self.assertEqual(before, proof.input_identity(self.root))

    def test_receipt_schema_and_editorial_status_cannot_be_promoted(self):
        receipt = self.make_receipt()
        receipt["editorial_approval"] = True
        self.write(proof.RECEIPT_PATH, json.dumps(receipt))
        with self.assertRaisesRegex(proof.ReceiptError, "proof or schema"):
            self.check()

    def test_duplicate_receipt_keys_are_rejected(self):
        self.make_receipt()
        path = self.root / proof.RECEIPT_PATH
        path.write_text(path.read_text().replace('"schema":', '"schema":"forged", "schema":', 1))
        with self.assertRaises(proof.ReceiptError):
            self.check()

    def test_symlinked_input_file_and_parent_and_output_are_rejected(self):
        self.make_receipt()
        source = self.root / self.source
        original = source.read_text()
        source.unlink()
        source.symlink_to(self.root / "guidance/sources.md")
        with self.assertRaises(proof.ReceiptError):
            self.check()
        source.unlink()
        source.write_text(original)
        parent = source.parent
        retained = parent.with_name("retained")
        parent.rename(retained)
        parent.symlink_to(retained, target_is_directory=True)
        with self.assertRaises(proof.ReceiptError):
            proof.input_identity(self.root)
        parent.unlink()
        retained.rename(parent)
        (self.target / "orphan.json").symlink_to(self.root / "workflows/reviews/authority.json")
        with self.assertRaises(proof.ReceiptError):
            proof.output_identity(self.root, self.target)

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

        with mock.patch.object(proof.os, "read", side_effect=swap), self.assertRaisesRegex(proof.ReceiptError, "changed during operation"):
            proof.read_file(self.root, self.source)

    def test_output_walk_refuses_directory_exchange(self):
        real_hash = proof._file_hash_at
        child = self.target / "text"
        retained = self.target / "retained"
        swapped = False

        def swap(parent, name, relative):
            nonlocal swapped
            result = real_hash(parent, name, relative)
            if relative.endswith("text/passage.example.json") and not swapped:
                swapped = True
                child.rename(retained)
                child.mkdir()
            return result

        with mock.patch.object(proof, "_file_hash_at", side_effect=swap), self.assertRaisesRegex(proof.ReceiptError, "changed"):
            proof.output_identity(self.root, self.target)

    def test_atomic_write_refuses_existing_symlink_or_hardlink(self):
        destination = self.root / proof.RECEIPT_PATH
        outside = self.write("outside.txt", "preserved")
        destination.symlink_to(outside)
        with self.assertRaises(proof.ReceiptError):
            proof.atomic_write(self.root, proof.RECEIPT_PATH, b"new")
        destination.unlink()
        os.link(outside, destination)
        with self.assertRaises(proof.ReceiptError):
            proof.atomic_write(self.root, proof.RECEIPT_PATH, b"new")
        self.assertEqual(outside.read_text(), "preserved")

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
        return name, manifest_name, sidecar

    def test_exact_delivery_and_manifest_replace_only_known_binary_bytes(self):
        name, _, _ = self.external_binary()
        before = proof.input_identity(self.root)
        self.assertEqual(before["external_count"], 1)
        self.assertFalse((self.root / name).exists())
        self.write(name, "local hydration is outside the logical projection proof")
        self.assertEqual(before, proof.input_identity(self.root))
        subprocess.run(["git", "-C", str(self.root), "add", name], check=True)
        (self.root / name).unlink()
        self.assertEqual(before, proof.input_identity(self.root))

    def test_external_delivery_never_excuses_a_present_special_payload(self):
        name, _, _ = self.external_binary()
        os.mkfifo(self.root / name)
        with self.assertRaisesRegex(proof.ReceiptError, "unsafe governing input"):
            proof.input_identity(self.root)

    def test_external_manifest_sidecar_mismatch_is_not_accepted(self):
        _, manifest_name, _ = self.external_binary()
        path = self.root / manifest_name
        path.write_text(path.read_text().replace('byte_size = 22', 'byte_size = 23'))
        with self.assertRaisesRegex(proof.ReceiptError, "differs from delivery"):
            proof.input_identity(self.root)

    def test_external_payload_without_its_manifest_is_not_accepted(self):
        _, manifest_name, _ = self.external_binary()
        (self.root / manifest_name).unlink()
        with self.assertRaisesRegex(proof.ReceiptError, "exact binary artifact manifest"):
            proof.input_identity(self.root)

    def replay(self, *, fail=False, mutation=None):
        original_run = subprocess.run

        def run(command, **kwargs):
            if command[0] == "git":
                return original_run(command, **kwargs)
            self.assertIn("--check", command)
            self.assertIn("--strict", command)
            self.assertNotIn("--check-receipt", command)
            self.assertEqual(Path(command[command.index("--out") + 1]), self.target.parent.parent)
            self.assertIn("-B", command)
            self.assertIn("-X", command)
            self.assertTrue(any(value.startswith("pycache_prefix=") for value in command))
            self.assertEqual(kwargs["env"]["TRIPTYCH_LIBRARY_CACHE"], "0")
            self.assertEqual(kwargs["env"]["TRIPTYCH_CORPUS_CACHE"], "0")
            if mutation:
                mutation()
            return subprocess.CompletedProcess(command, 2 if fail else 0,
                stdout=json.dumps({"status": "ok", "files": 2, "works": 1,
                                   "editions": 1, "artifacts": 1, "passages": 1, "readable": 1}),
                stderr="inherited full-check failure" if fail else "")

        return mock.patch.object(proof.subprocess, "run", side_effect=run)

    def test_failed_full_replay_never_adopts_existing_projection(self):
        self.make_receipt()
        original = (self.root / proof.RECEIPT_PATH).read_bytes()
        with self.replay(fail=True), self.assertRaisesRegex(proof.ReceiptError, "full source projection check failed"):
            proof.record_receipt(self.root, self.target, reader.SCHEMA)
        self.assertEqual((self.root / proof.RECEIPT_PATH).read_bytes(), original)

    def test_record_replays_independently_and_fast_check_accepts_success(self):
        with self.replay():
            recorded = proof.record_receipt(self.root, self.target, reader.SCHEMA)
        self.assertEqual(recorded, self.check())

    def test_prepared_proof_does_not_write_until_its_owner_commits(self):
        with self.replay():
            candidate = proof.record_receipt(self.root, self.target, reader.SCHEMA, write=False)
        self.assertFalse((self.root / proof.RECEIPT_PATH).exists())
        proof.write_receipt(self.root, candidate)
        self.assertEqual(candidate, self.check())

    def test_record_refuses_source_mutation_during_full_check(self):
        with self.replay(mutation=lambda: self.write(self.source, "changed during replay")), self.assertRaisesRegex(proof.ReceiptError, "changed during replay"):
            proof.record_receipt(self.root, self.target, reader.SCHEMA)
        self.assertFalse((self.root / proof.RECEIPT_PATH).exists())

    def test_replay_executes_current_source_instead_of_stale_same_stamp_bytecode(self):
        module = self.write("scripts/fixture.py", "marker = 'BEFORE'\n")
        previous = module.stat()
        py_compile.compile(str(module), doraise=True)
        module.write_text("marker = 'AFTER!'\n")
        os.utime(module, ns=(previous.st_atime_ns, previous.st_mtime_ns))
        stale = subprocess.run(
            [sys.executable, "-B", "-c", "import fixture; print(fixture.marker)"],
            env={**os.environ, "PYTHONPATH": str(self.root / "scripts")},
            capture_output=True, text=True, check=True,
        )
        self.assertEqual(stale.stdout.strip(), "BEFORE")
        answer = {"status": "ok", "files": 2, "works": 1, "editions": 1,
                  "artifacts": 1, "passages": 1, "readable": 1}
        self.write("tools/source-reader",
                   "import sys\nfrom pathlib import Path\n"
                   "sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))\n"
                   "import fixture\nassert fixture.marker == 'AFTER!'\n"
                   f"print({json.dumps(json.dumps(answer))})\n")
        proof.record_receipt(self.root, self.target, reader.SCHEMA)
        self.assertEqual(self.check()["outputs"]["count"], 2)


if __name__ == "__main__":
    unittest.main()
