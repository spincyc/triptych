"""Mechanical projection receipts refuse stale identities and never adopt drift.

Use a two-file deterministic generator fixture at the existing build boundary;
these tests exercise the real receipt writer, inventory and descriptor-anchored
installed-output comparison without replaying the entire source corpus per
mutation. The complete corpus replay is the separate explicit integration gate.
"""
from __future__ import annotations

import importlib.machinery
import importlib.util
from contextlib import contextmanager, redirect_stderr, redirect_stdout
import io
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
from types import SimpleNamespace
import unittest
from unittest import mock


ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))
import _act_history_projection_receipt as receipt


def load_tool():
    loader = importlib.machinery.SourceFileLoader(
        "test_act_history_projection_receipt_tool", str(ROOT / "tools/act-history")
    )
    spec = importlib.util.spec_from_loader(loader.name, loader)
    module = importlib.util.module_from_spec(spec)
    loader.exec_module(module)
    return module


class ActHistoryProjectionReceiptTests(unittest.TestCase):
    def setUp(self):
        scratch = ROOT / ".scratch/next-act-receipt"
        scratch.mkdir(parents=True, exist_ok=True)
        self.held = tempfile.TemporaryDirectory(prefix="mutation-", dir=scratch)
        self.addCleanup(self.held.cleanup)
        self.root = Path(self.held.name)
        subprocess.run(["git", "init", "-q", str(self.root)], check=True)
        self.source = self.write("src/sources/inventories/fixture-acts-v1.toml", "fixture = 1\n")
        self.generator = self.write("scripts/generator.py", "GENERATOR = 1\n")
        self.rights = self.write("guidance/rights.md", "Fixture rights policy.\n")
        self.write("src/gpt/fixture/research/source-bindings.toml", "bindings = []\n")
        self.contents = {"index.json": ("file", b'{"fixture":1}\n'),
                         "fixture/unit.json": ("file", b'{"text":"source"}\n')}
        self.data = self.root / ".scratch/verified-products/data"
        self.projection = self.data / receipt.PROJECTION
        for name, (_, body) in self.contents.items():
            self.write((self.projection / name).relative_to(self.root).as_posix(), body)
        @contextmanager
        def products(root, *, cache_root=None):
            self.assertEqual(self.root, root)
            yield SimpleNamespace(data_root=self.data)
        self.products_patch = mock.patch.object(receipt, "_products", side_effect=products)
        self.products_patch.start()
        self.addCleanup(self.products_patch.stop)
        self.tool = load_tool()
        self.patch = mock.patch.object(receipt, "_tool", return_value=self.tool)
        self.patch.start()
        self.addCleanup(self.patch.stop)
        self.sources_patch = mock.patch.object(self.tool, "structure_sources", return_value=(self.source,))
        self.sources_patch.start()
        self.addCleanup(self.sources_patch.stop)
        self.build_patch = mock.patch.object(self.tool, "build_structure_projection", side_effect=self.derive)
        self.build = self.build_patch.start()
        self.addCleanup(self.build_patch.stop)

    def write(self, relative, body):
        path = self.root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(body if isinstance(body, bytes) else body.encode())
        return path

    def derive(self, sources, out):
        self.assertEqual((self.source,), sources)
        self.assertTrue(out.is_relative_to(self.root / receipt.SCRATCH))
        self.assertNotEqual(self.projection, out)
        for name, (_, body) in self.contents.items():
            target = out / receipt.PROJECTION / name
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(body)
        # The normal build returns captured bytes from an exclusive empty tree.
        return {"contents": dict(self.contents), "files": 2, "slices": ["fixture"],
                "stations": 1, "lines": 1, "default": "fixture"}

    def record(self):
        return receipt.record(self.root)

    def test_record_replays_then_check_only_hashes_and_writes_nothing(self):
        expected = self.record()
        self.assertEqual(1, self.build.call_count)
        self.assertFalse(expected["editorial_approval"])
        self.assertEqual(set(self.contents), set(expected["outputs"]["files"]))
        path = self.root / receipt.RECEIPT
        before = path.read_bytes()
        with mock.patch.object(receipt, "_replay", side_effect=AssertionError("cheap gate replayed")):
            self.assertEqual(expected, receipt.check(self.root))
        self.assertEqual(before, path.read_bytes())
        self.assertEqual(1, self.build.call_count)

    def test_missing_receipt_fails_without_replay_or_write(self):
        with self.assertRaisesRegex(receipt.ReceiptError, "missing.*receipt"):
            receipt.check(self.root)
        self.assertFalse((self.root / receipt.RECEIPT).exists())
        self.build.assert_not_called()

    def test_cold_replay_needs_no_legacy_data_or_committed_product(self):
        out = self.root / receipt.SCRATCH / "cold-data"
        sibling = out / "structure/sources/other.json"
        sibling.parent.mkdir(parents=True)
        sibling.write_bytes(b'{"other":true}\n')
        with mock.patch.object(receipt, "_products", side_effect=AssertionError("producer read products")):
            summary = receipt._replay(self.root, out)
        self.assertEqual(2, summary["files"])
        for name, (_, body) in self.contents.items():
            self.assertEqual(body, (out / receipt.PROJECTION / name).read_bytes())
        self.assertEqual(b'{"other":true}\n', sibling.read_bytes())
        self.assertFalse((self.root / "src/web/data").exists())
        self.assertFalse((self.root / receipt.RECEIPT).exists())

    def test_cold_replay_refuses_nonempty_family_without_adopting_it(self):
        out = self.root / receipt.SCRATCH / "cold-data"
        sentinel = out / receipt.PROJECTION / "old.json"
        sentinel.parent.mkdir(parents=True)
        sentinel.write_bytes(b'{"unreviewed":true}\n')
        with self.assertRaisesRegex(receipt.ReceiptError, "absent or empty"):
            receipt._replay(self.root, out)
        self.assertEqual(b'{"unreviewed":true}\n', sentinel.read_bytes())
        self.build.assert_not_called()

    def test_cold_api_suppresses_source_bytecode_even_for_importing_callers(self):
        source = self.write("src/gpt/fixture/schema/validator.py", "VALUE = 1\n")
        original = self.derive

        def import_source(sources, out):
            loader = importlib.machinery.SourceFileLoader("act_cold_source_fixture", str(source))
            spec = importlib.util.spec_from_loader(loader.name, loader)
            module = importlib.util.module_from_spec(spec)
            loader.exec_module(module)
            self.assertEqual(1, module.VALUE)
            return original(sources, out)

        with mock.patch.object(self.tool, "build_structure_projection", side_effect=import_source), \
                mock.patch.object(sys, "dont_write_bytecode", False), \
                mock.patch.object(sys, "pycache_prefix", None):
            receipt._replay(self.root, self.root / receipt.SCRATCH / "cold-data")
            self.assertFalse(sys.dont_write_bytecode)
            self.assertIsNone(sys.pycache_prefix)
        self.assertFalse((source.parent / "__pycache__").exists())

    def test_receipt_check_refuses_missing_product_proof_despite_legacy_data(self):
        self.record()
        for name, (_, body) in self.contents.items():
            self.write((Path("src/web/data") / receipt.PROJECTION / name).as_posix(), body)
        self.products_patch.stop()
        with self.assertRaisesRegex(receipt.ReceiptError, "browser products are unavailable or stale"):
            receipt.check(self.root)
        self.assertEqual(1, self.build.call_count)

    def test_structure_default_writes_unsealed_working_root(self):
        self.tool.ROOT = self.root
        summary = {"files": 2, "slices": ["fixture"], "stations": 1, "lines": 1,
                   "default": "fixture", "written": "fixture"}
        with mock.patch.dict(os.environ, {"TRIPTYCH_BROWSER_DATA_ROOT": ".scratch/sealed-cache"}), \
                mock.patch.object(self.tool, "structure_all", return_value=summary) as build, \
                mock.patch.object(self.tool, "print_json"), \
                redirect_stdout(io.StringIO()), redirect_stderr(io.StringIO()):
            self.assertEqual(0, self.tool.main(["structure", "--json"]))
        build.assert_called_once_with(self.root / ".scratch/sealed-cache-work", check_only=False)

    def test_structure_default_check_holds_verified_products(self):
        self.tool.ROOT = self.root
        summary = {"files": 2, "slices": ["fixture"], "stations": 1, "lines": 1,
                   "default": "fixture", "current": "fixture"}
        @contextmanager
        def products(root, *, product_ids):
            self.assertEqual(self.root, root)
            self.assertEqual(["act-history"], product_ids)
            yield SimpleNamespace(data_root=self.data)
        with mock.patch.object(self.tool, "verified_products", side_effect=products) as held, \
                mock.patch.object(self.tool, "structure_all", return_value=summary) as build, \
                mock.patch.object(self.tool, "print_json"), \
                redirect_stdout(io.StringIO()), redirect_stderr(io.StringIO()):
            self.assertEqual(0, self.tool.main(["structure", "--check", "--json"]))
        self.assertEqual(1, held.call_count)
        build.assert_called_once_with(self.data, check_only=True)

    def test_structure_writer_refuses_explicit_sealed_cache_output(self):
        self.tool.ROOT = self.root
        with mock.patch.dict(os.environ, {"TRIPTYCH_BROWSER_DATA_ROOT": ".scratch/sealed-cache"}), \
                mock.patch.object(self.tool, "structure_all") as build, \
                redirect_stdout(io.StringIO()), redirect_stderr(io.StringIO()) as errors:
            self.assertEqual(1, self.tool.main([
                "structure", "--out", str(self.root / ".scratch/sealed-cache/identity/data"), "--json"
            ]))
        build.assert_not_called()

    def test_changed_text_with_preserved_mtime_is_stale(self):
        self.record()
        original = self.source.stat()
        self.source.write_text("fixture = 2\n")
        os.utime(self.source, ns=(original.st_atime_ns, original.st_mtime_ns))
        self.assertEqual(original.st_size, self.source.stat().st_size)
        with self.assertRaisesRegex(receipt.ReceiptError, "identity has changed"):
            receipt.check(self.root)

    def test_changed_generator_policy_binding_or_unknown_input_fails(self):
        for kind in ("generator", "policy", "binding", "unknown-source", "unknown-code", "missing"):
            with self.subTest(kind=kind):
                self.record()
                target = None
                original = None
                if kind in ("generator", "policy", "binding", "missing"):
                    target = {"generator": self.generator, "policy": self.rights,
                              "binding": self.root / "src/gpt/fixture/research/source-bindings.toml",
                              "missing": self.source}[kind]
                    original = target.read_bytes()
                    if kind == "missing":
                        # Track this file so Git still enumerates it after deletion.
                        subprocess.run(["git", "add", str(target)], cwd=self.root, check=True)
                        target.unlink()
                    else:
                        target.write_bytes(original + b"# changed\n")
                else:
                    target = self.write("src/sources/inventories/unknown.toml" if kind == "unknown-source"
                                        else "scripts/unknown.py", "unknown = 1\n")
                try:
                    with self.assertRaises(receipt.ReceiptError):
                        receipt.check(self.root)
                finally:
                    if original is None:
                        target.unlink()
                    else:
                        target.write_bytes(original)

    def test_changed_missing_extra_and_unsafe_outputs_fail(self):
        self.record()
        path = self.projection / "fixture/unit.json"
        original = path.read_bytes()
        for kind in ("changed", "missing", "extra", "symlink", "directory-symlink", "fifo"):
            with self.subTest(kind=kind):
                extra = None
                if kind == "changed":
                    path.write_bytes(b'{"changed":true}\n')
                elif kind == "missing":
                    path.unlink()
                else:
                    extra = self.projection / ("extra" if kind == "directory-symlink" else "extra.json")
                    if kind == "extra":
                        extra.write_bytes(b"{}\n")
                    elif kind == "symlink":
                        extra.symlink_to(path)
                    elif kind == "directory-symlink":
                        extra.symlink_to(self.projection / "fixture", target_is_directory=True)
                    else:
                        os.mkfifo(extra)
                try:
                    with self.assertRaises(receipt.ReceiptError):
                        receipt.check(self.root)
                finally:
                    if extra is not None:
                        extra.unlink()
                    path.write_bytes(original)

    def test_unknown_fifo_input_omitted_by_git_is_rejected(self):
        self.record()
        fifo = self.root / "src/sources/inventories/untracked.toml"
        os.mkfifo(fifo)
        listed = subprocess.check_output(["git", "ls-files", "--others"], cwd=self.root, text=True)
        self.assertNotIn("untracked.toml", listed)
        with self.assertRaises(receipt.ReceiptError):
            receipt.check(self.root)
        with self.assertRaises(receipt.ReceiptError):
            self.record()
        self.assertEqual(1, self.build.call_count)

    def test_record_refuses_projection_drift_and_preserves_existing_receipt(self):
        self.record()
        path = self.root / receipt.RECEIPT
        before = path.read_bytes()
        changed = self.projection / "index.json"
        changed.write_bytes(b'{"unreviewed":true}\n')
        with self.assertRaisesRegex(receipt.ReceiptError, "has drifted"):
            self.record()
        self.assertEqual(before, path.read_bytes())
        self.assertEqual(b'{"unreviewed":true}\n', changed.read_bytes())

    def test_record_refuses_failed_replay_without_creating_a_receipt(self):
        with mock.patch.object(self.tool, "build_structure_projection", side_effect=ValueError("invalid source")):
            with self.assertRaisesRegex(ValueError, "invalid source"):
                self.record()
        self.assertFalse((self.root / receipt.RECEIPT).exists())

    def test_cold_source_errors_are_mapped_before_leaving_the_tool_instance(self):
        with mock.patch.object(self.tool, "build_structure_projection",
                               side_effect=self.tool.Problem("invalid canonical history")):
            with self.assertRaisesRegex(receipt.ReceiptError, "invalid canonical history"):
                receipt._replay(self.root, self.root / receipt.SCRATCH / "cold-data")
        self.assertFalse((self.root / receipt.RECEIPT).exists())

    def test_record_writes_nothing_if_verified_product_exit_check_fails(self):
        @contextmanager
        def failing_products(root, *, cache_root=None):
            yield SimpleNamespace(data_root=self.data)
            raise receipt.ReceiptError("product descriptor changed during operation")
        with mock.patch.object(receipt, "_products", side_effect=failing_products):
            with self.assertRaisesRegex(receipt.ReceiptError, "descriptor changed"):
                self.record()
        self.assertFalse((self.root / receipt.RECEIPT).exists())

    def test_record_refuses_inputs_changed_during_replay(self):
        original = self.derive

        def mutate(sources, out):
            result = original(sources, out)
            self.source.write_text("fixture = 2\n")
            return result

        with mock.patch.object(self.tool, "build_structure_projection", side_effect=mutate):
            with self.assertRaisesRegex(receipt.ReceiptError, "changed during independent replay"):
                self.record()
        self.assertFalse((self.root / receipt.RECEIPT).exists())

    def test_record_refuses_outputs_changed_after_the_replay_comparison(self):
        replay = receipt._compare_replay

        def mutate(root, target, tool):
            summary = replay(root, target, tool)
            (self.projection / "index.json").write_bytes(b'{"changed":true}\n')
            return summary

        with mock.patch.object(receipt, "_compare_replay", side_effect=mutate):
            with self.assertRaisesRegex(receipt.ReceiptError, "outputs changed during independent replay"):
                self.record()
        self.assertFalse((self.root / receipt.RECEIPT).exists())

    def test_invalid_or_nonmechanical_receipt_is_rejected(self):
        original = self.record()
        for key, value in (("schema", "unknown/v1"), ("editorial_approval", True),
                           ("proof", "hashes-only"), ("outputs", {})):
            with self.subTest(key=key):
                changed = {**original, key: value}
                (self.root / receipt.RECEIPT).write_text(json.dumps(changed))
                with self.assertRaises(receipt.ReceiptError):
                    receipt.check(self.root)

    def test_receipt_symlink_is_never_followed_or_overwritten(self):
        self.record()
        path = self.root / receipt.RECEIPT
        sentinel = self.write("sentinel", "outside receipt\n")
        path.unlink()
        path.symlink_to(sentinel)
        with self.assertRaises(receipt.ReceiptError):
            receipt.check(self.root)
        with self.assertRaises(receipt.ReceiptError):
            self.record()
        self.assertEqual("outside receipt\n", sentinel.read_text())


if __name__ == "__main__":
    unittest.main()
