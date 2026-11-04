"""The cold act-history replay derives its family without adopting old bytes.

Use a two-file deterministic generator fixture at the existing build boundary;
these tests exercise the real replay and structure CLI without replaying the
entire source corpus. The complete corpus replay is the separate explicit
integration gate, and the browser-product descriptor binds the bytes.
"""
from __future__ import annotations

import importlib.machinery
import importlib.util
from contextlib import contextmanager, redirect_stderr, redirect_stdout
import io
import os
from pathlib import Path
import sys
import tempfile
from types import SimpleNamespace
import unittest
from unittest import mock


ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))
import _act_history_replay as replay


def load_tool():
    loader = importlib.machinery.SourceFileLoader(
        "test_act_history_replay_tool", str(ROOT / "tools/act-history")
    )
    spec = importlib.util.spec_from_loader(loader.name, loader)
    module = importlib.util.module_from_spec(spec)
    loader.exec_module(module)
    return module


class ActHistoryReplayTests(unittest.TestCase):
    def setUp(self):
        scratch = ROOT / ".scratch/act-history-replay"
        scratch.mkdir(parents=True, exist_ok=True)
        self.held = tempfile.TemporaryDirectory(prefix="mutation-", dir=scratch)
        self.addCleanup(self.held.cleanup)
        self.root = Path(self.held.name)
        self.source = self.write("src/sources/inventories/fixture-acts-v1.toml", "fixture = 1\n")
        self.contents = {"index.json": ("file", b'{"fixture":1}\n'),
                         "fixture/unit.json": ("file", b'{"text":"source"}\n')}
        self.data = self.root / ".scratch/verified-products/data"
        self.projection = self.data / replay.PROJECTION
        for name, (_, body) in self.contents.items():
            self.write((self.projection / name).relative_to(self.root).as_posix(), body)
        self.tool = load_tool()
        self.patch = mock.patch.object(replay, "_tool", return_value=self.tool)
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
        self.assertTrue(out.is_relative_to(self.root / replay.SCRATCH))
        self.assertNotEqual(self.projection, out)
        for name, (_, body) in self.contents.items():
            target = out / replay.PROJECTION / name
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(body)
        # The normal build returns captured bytes from an exclusive empty tree.
        return {"contents": dict(self.contents), "files": 2, "slices": ["fixture"],
                "stations": 1, "lines": 1, "default": "fixture"}

    def test_cold_replay_needs_no_legacy_data_or_committed_product(self):
        out = self.root / replay.SCRATCH / "cold-data"
        sibling = out / "structure/sources/other.json"
        sibling.parent.mkdir(parents=True)
        sibling.write_bytes(b'{"other":true}\n')
        with mock.patch("_browser_products.verified_products", side_effect=AssertionError("producer read products")):
            summary = replay._replay(self.root, out)
        self.assertEqual(2, summary["files"])
        for name, (_, body) in self.contents.items():
            self.assertEqual(body, (out / replay.PROJECTION / name).read_bytes())
        self.assertEqual(b'{"other":true}\n', sibling.read_bytes())
        self.assertFalse((self.root / "src/web/data").exists())

    def test_cold_replay_refuses_nonempty_family_without_adopting_it(self):
        out = self.root / replay.SCRATCH / "cold-data"
        sentinel = out / replay.PROJECTION / "old.json"
        sentinel.parent.mkdir(parents=True)
        sentinel.write_bytes(b'{"unreviewed":true}\n')
        with self.assertRaisesRegex(replay.ReplayError, "absent or empty"):
            replay._replay(self.root, out)
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
            replay._replay(self.root, self.root / replay.SCRATCH / "cold-data")
            self.assertFalse(sys.dont_write_bytecode)
            self.assertIsNone(sys.pycache_prefix)
        self.assertFalse((source.parent / "__pycache__").exists())

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

    def test_cold_source_errors_are_mapped_before_leaving_the_tool_instance(self):
        with mock.patch.object(self.tool, "build_structure_projection",
                               side_effect=self.tool.Problem("invalid canonical history")):
            with self.assertRaisesRegex(replay.ReplayError, "invalid canonical history"):
                replay._replay(self.root, self.root / replay.SCRATCH / "cold-data")


if __name__ == "__main__":
    unittest.main()
