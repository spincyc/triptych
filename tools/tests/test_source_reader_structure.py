#!/usr/bin/env python3
"""`source-reader structure` writes only unsealed working output."""
from __future__ import annotations

import argparse
import importlib.machinery
import importlib.util
import os
from pathlib import Path
import sys
import tempfile
import unittest
from unittest import mock

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))

loader = importlib.machinery.SourceFileLoader("structure_reader_under_test", str(ROOT / "tools/source-reader"))
spec = importlib.util.spec_from_loader(loader.name, loader)
reader = importlib.util.module_from_spec(spec)
sys.modules[loader.name] = reader
loader.exec_module(reader)


class StructureOutputTests(unittest.TestCase):
    """`structure` writes only an unsealed working root, never a sealed cache."""

    def setUp(self):
        scratch = ROOT / ".scratch/source-reader-structure-tests"
        scratch.mkdir(parents=True, exist_ok=True)
        self.temporary = tempfile.TemporaryDirectory(dir=scratch, prefix="test-")
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)

    def arguments(self, **values):
        return argparse.Namespace(**{"out": None, "check": False, **values})

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
        original.mkdir(parents=True)
        (original / ".browser-products-cache-v1").write_text("")
        with mock.patch.dict(os.environ, {"TRIPTYCH_BROWSER_DATA_ROOT": str(self.root / ".scratch/new-cache")}), mock.patch.object(reader, "ROOT", self.root), self.assertRaisesRegex(reader.ReaderError, "outside the sealed"):
            reader.run_structure(self.arguments(out=str(original / "key/data")))

    def test_output_option_keeps_its_value_before_the_verb(self):
        with mock.patch.object(reader, "run_verb_cli", side_effect=lambda **values: values["parser"].parse_args(values["argv"])):
            output = reader.main(["--out", "chosen-output", "structure"])
        self.assertEqual(output.out, "chosen-output")
        self.assertFalse(hasattr(output, "cache_root"))


