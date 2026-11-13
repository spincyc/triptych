"""Build-time web editions: the reader universe, companion selection, and forks.

The converter's long-standing audits are tested in test_web_edition_conversion
and the conditional constructs in test_web_edition_constructs; this module
covers which outputs have readers, how a companion selects its own edition,
and how each output converts in its own fork of a pristine parent.
"""
from __future__ import annotations

import functools
import importlib.machinery
import importlib.util
from contextlib import nullcontext
import io
import json
import os
import signal
import subprocess
import sys
import tempfile
import threading
import time
import tomllib
import types
import unittest
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))
LOADER = importlib.machinery.SourceFileLoader("triptych_web_edition_build", str(ROOT / "tools/web-edition"))
SPEC = importlib.util.spec_from_loader(LOADER.name, LOADER)
DRIVER = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = DRIVER
SPEC.loader.exec_module(DRIVER)

class EditionSelectionTests(unittest.TestCase):
    """A companion is the edition its own entrypoint selects."""

    TEXT = ("Common.\n\\ifdefined\\TriptychSynthesisEdition\nConcise.\n\\else\nResearch.\n\\fi\n"
            "\\ifdefined\\TriptychHomilyEdition Spoken\\else Written\\fi{} close.\n"
            "\\ifdefined\\TriptychPrintEdition\nPrint.\n\\else\nWeb.\n\\fi\n")

    def test_each_edition_keeps_its_own_branches_and_never_the_print_one(self):
        self.assertEqual(DRIVER.select_edition_branches(self.TEXT, "main"),
                         "Common.\nResearch.\nWritten{} close.\nWeb.\n")
        self.assertEqual(DRIVER.select_edition_branches(self.TEXT, "synthesis"),
                         "Common.\nConcise.\nWritten{} close.\nWeb.\n")
        self.assertEqual(DRIVER.select_edition_branches(self.TEXT, "homily"),
                         "Common.\nResearch.\nSpoken{} close.\nWeb.\n")

    def test_nested_switches_and_newif_are_balanced(self):
        text = ("\\ifdefined\\TriptychSynthesisEdition\\newif\\ifkept"
                "\\ifdefined\\TriptychPrintEdition P\\else W\\fi{}\\else R\\fi{}")
        # The empty group an inline \\fi{} leaves sets nothing, as in select_branch.
        self.assertEqual(DRIVER.select_edition_branches(text, "synthesis"), "\\newif\\ifkeptW{}{}")
        with self.assertRaises(DRIVER.ConversionError):
            DRIVER.select_edition_branches("\\ifdefined\\TriptychSynthesisEdition open", "synthesis")
        with self.assertRaises(DRIVER.ConversionError):
            DRIVER.select_edition_branches("x", "print")

    def test_edition_selection_inlines_its_own_inputs_and_keeps_the_shared_preamble(self):
        with tempfile.TemporaryDirectory() as temporary:
            src = Path(temporary) / "src"
            leaf = src / "test/studies/subject"
            (leaf / "sections").mkdir(parents=True)
            (leaf / "sections/one.tex").write_text(
                "\\ifdefined\\TriptychSynthesisEdition\nShort.\n\\else\nLong.\n\\fi\n")
            (leaf / "synthesis.tex").write_text(
                "\\def\\TriptychSynthesisEdition{1}\n\\input{common/preamble}\n"
                "\\begin{document}\n\\input{studies/subject/sections/one}\n\\end{document}\n")
            with mock.patch.object(DRIVER, "SRC", src):
                selected = DRIVER.edition_selection("test", leaf / "synthesis.tex", "synthesis")
        self.assertIn("\\input{common/preamble}", selected["source"])
        self.assertIn("Short.", selected["body"])
        self.assertNotIn("Long.", selected["body"])
        self.assertIn("Long.", selected["canonical_body"])  # the raw files, for paragraph audits
        self.assertEqual(selected["edition"], "synthesis")


class ReaderUniverseTests(unittest.TestCase):
    """Every eligible and conditional leaf has readers, companions included."""

    def test_reader_outputs_are_exactly_the_admitted_eligible_and_conditional_outputs(self):
        rows = DRIVER.reader_outputs()
        ids = {row["id"] for row in rows}
        self.assertEqual(len(ids), len(rows))
        for row in rows:
            declaration = row["declaration"]
            self.assertIn(declaration["eligibility"], {"eligible", "conditional"})
            self.assertNotIn("withdrawn", declaration)
            self.assertEqual(row["release_status"], "alpha")
        companions = [row for row in rows if row["edition"] != "main"]
        self.assertTrue(companions)
        for row in companions:
            self.assertTrue(row["entrypoint"].endswith(f"/{row['edition']}.tex"))
        for path in (ROOT / "src").glob("*/**/web-edition.toml"):
            declaration = tomllib.loads(path.read_text(encoding="utf-8"))
            if declaration["eligibility"] == "ineligible":
                provider = path.relative_to(ROOT / "src").parts[0]
                self.assertNotIn(f"publication:{provider}/{declaration['document']}", ids)

    def test_curriculum_readers_take_their_kind_from_the_owning_path(self):
        # Manifests state no kind once the schema derives it from the path; a
        # curriculum leaf read as kind-less would reach the generic converter,
        # which refuses the course's TeX program.
        rows = [row for row in DRIVER.reader_outputs()
                if row["canonical"].startswith("curriculums/")]
        self.assertTrue(rows)
        for row in rows:
            self.assertTrue(row["kind"].startswith("curriculum-"), row["id"])
            self.assertTrue(DRIVER.curriculum_adapter().applies(row["kind"]), row["id"])

    def test_no_copy_of_a_web_edition_is_tracked(self):
        import subprocess
        tracked = subprocess.run(["git", "ls-files", "--", "web"], cwd=ROOT, check=True,
                                 capture_output=True, text=True).stdout
        self.assertEqual(tracked, "")


class ForkedConversionTests(unittest.TestCase):
    """Each output converts in its own fork of a parent that converted no leaf."""

    ROWS = [{"provider": "test", "document": f"leaf-{index}"} for index in range(6)]

    def convert(self, product_record, *, jobs=3):
        # The mechanics only: the real warm-up and the parent's own state are
        # covered by ParentStateTests, in a fresh interpreter.
        with mock.patch.object(DRIVER, "product_record", product_record), \
                mock.patch.object(DRIVER, "share_parent_state", lambda: None), \
                mock.patch.object(DRIVER, "parent_leaf_state", lambda: []):
            return DRIVER.convert_rows(self.ROWS, jobs=jobs)

    def test_records_are_collected_in_row_order(self):
        def product_record(row):
            index = int(row["document"].rpartition("-")[2])
            time.sleep(0.05 * (len(self.ROWS) - index))  # the last row finishes first
            return {"id": row["document"]}
        records = self.convert(product_record)
        self.assertEqual([record["id"] for record in records], [row["document"] for row in self.ROWS])

    def test_each_output_converts_in_a_fresh_fork_of_its_own(self):
        seen = []

        def product_record(row):
            seen.append(row["document"])  # leaf state, as a conversion's macro table is
            return {"pid": os.getpid(), "seen": list(seen)}
        records = self.convert(product_record)
        self.assertEqual([record["seen"] for record in records],
                         [[row["document"]] for row in self.ROWS])
        pids = [record["pid"] for record in records]
        self.assertEqual(len(set(pids)), len(pids))
        self.assertNotIn(os.getpid(), pids)
        self.assertEqual(seen, [])

    def test_a_child_imports_as_a_fresh_interpreter_without_the_working_directory(self):
        # Under the cold recipe harness the parent runs as `python -c`, whose
        # "" entry would make distribution lookups list the repository root.
        with mock.patch.object(sys, "path", ["", *sys.path]):
            records = self.convert(lambda row: {"cwd_on_path": "" in sys.path})
            self.assertIn("", sys.path)  # the parent's own path is untouched
        self.assertEqual({record["cwd_on_path"] for record in records}, {False})

    def test_every_failing_output_is_named_and_the_family_fails(self):
        def product_record(row):
            if row["document"] in {"leaf-1", "leaf-4"}:
                raise DRIVER.ConversionError(f"cannot convert {row['document']}")
            if row["document"] == "leaf-2":
                raise KeyError("unexpected")
            return {"id": row["document"]}
        with self.assertRaises(DRIVER.ConversionError) as raised:
            self.convert(product_record)
        message = str(raised.exception)
        self.assertTrue(message.startswith("3 web edition(s) failed:\n"), message)
        self.assertIn("test/leaf-1: cannot convert leaf-1", message)
        self.assertIn("test/leaf-4: cannot convert leaf-4", message)
        self.assertIn("test/leaf-2: Traceback (most recent call last):", message)
        self.assertIn("KeyError: 'unexpected'", message)
        self.assertNotIn("leaf-0", message)

    def test_a_child_killed_by_a_signal_fails_the_family(self):
        def product_record(row):
            if row["document"] == "leaf-3":
                os.kill(os.getpid(), signal.SIGKILL)
            return {"id": row["document"]}
        with self.assertRaises(DRIVER.ConversionError) as raised:
            self.convert(product_record)
        self.assertIn("1 web edition(s) failed:\ntest/leaf-3: conversion killed by signal SIGKILL",
                      str(raised.exception))

    def test_a_multithreaded_parent_never_forks(self):
        release = threading.Event()
        helper = threading.Thread(target=release.wait)
        helper.start()
        try:
            with self.assertRaises(DRIVER.ConversionError) as raised:
                self.convert(lambda row: self.fail("forked from a multi-threaded parent"))
        finally:
            release.set()
            helper.join()
        self.assertIn("single-threaded", str(raised.exception))

    def test_a_parent_holding_leaf_state_never_forks(self):
        with mock.patch.object(DRIVER, "parent_leaf_state", lambda: ["somewhere._leaf_cache"]), \
                mock.patch.object(DRIVER, "share_parent_state", lambda: None), \
                mock.patch.object(DRIVER, "product_record",
                                  lambda row: self.fail("forked from a parent holding leaf state")):
            with self.assertRaises(DRIVER.ConversionError) as raised:
                DRIVER.convert_rows(self.ROWS, jobs=2)
        self.assertIn("parent holding leaf state: somewhere._leaf_cache", str(raised.exception))


class ParentStateTests(unittest.TestCase):
    """The parent the conversions fork from holds only the shared caches."""

    def test_a_converted_leaf_or_an_unshared_cache_is_leaf_state(self):
        module = types.ModuleType("triptych_test_leaf_cache")
        module.__file__ = str(ROOT / "scripts" / "_triptych_test_leaf_cache.py")

        @functools.lru_cache(maxsize=None)
        def remembered(leaf):
            return leaf
        remembered.__module__ = module.__name__
        module.remembered = remembered
        with mock.patch.dict(sys.modules, {module.__name__: module}), \
                mock.patch.dict(DRIVER._SHARED, clear=True):
            baseline = DRIVER.parent_leaf_state()
            self.assertNotIn("triptych_test_leaf_cache.remembered", baseline)
            remembered("claude/some/leaf")
            self.assertIn("triptych_test_leaf_cache.remembered", DRIVER.parent_leaf_state())
            DRIVER._SHARED["converted"] = True
            self.assertIn("a leaf was converted in this process", DRIVER.parent_leaf_state())

    def test_the_warmed_parent_holds_only_shared_state(self):
        # A fresh interpreter, as the producer starts: list the readers,
        # share the parent state, and ask what a fork would inherit.
        program = (
            "import importlib.machinery, importlib.util, json, sys\n"
            f"sys.path.insert(0, {str(ROOT / 'scripts')!r})\n"
            f"loader = importlib.machinery.SourceFileLoader('web_edition', {str(ROOT / 'tools/web-edition')!r})\n"
            "module = importlib.util.module_from_spec(importlib.util.spec_from_loader(loader.name, loader))\n"
            "sys.modules[loader.name] = module\n"
            "loader.exec_module(module)\n"
            "module.reader_outputs()\n"
            "module.share_parent_state()\n"
            "import _document_schema, _proper_chronology_page\n"
            "print(json.dumps({'held': module.parent_leaf_state(),\n"
            "                  'index': bool(_document_schema._SOURCE_INDEX),\n"
            "                  'records': _proper_chronology_page._source_records.cache_info().currsize,\n"
            "                  'repository': module._SHARED.get('repository') is not None}))\n")
        finished = subprocess.run([sys.executable, "-B", "-c", program], cwd=ROOT,
                                  capture_output=True, text=True, check=False)
        self.assertEqual(finished.returncode, 0, finished.stderr[-3000:])
        state = json.loads(finished.stdout)
        self.assertEqual(state["held"], [])
        self.assertTrue(state["index"])
        self.assertEqual(state["records"], 1)
        self.assertTrue(state["repository"])


class WorkerSelectionTests(unittest.TestCase):
    """Workers recheck one selection, retaining the fresh converter process."""

    def setUp(self):
        self.row = {"id": "publication:gpt/articles/faith/example", "provider": "gpt",
                    "document": "articles/faith/example", "release_status": "alpha",
                    "declaration": {"eligibility": "eligible"}}
        self.identity = "gpt/articles/faith/example"

    def run_worker(self, row, current=None):
        with (mock.patch.object(DRIVER.sys, "stdin", io.StringIO(json.dumps(row))),
              mock.patch.object(DRIVER.sys, "stdout", io.StringIO()) as output,
              mock.patch.object(DRIVER.sys, "stderr", io.StringIO()) as errors,
              mock.patch("_print_document.publication_recipe", return_value={}) as recipe,
              mock.patch.object(DRIVER, "publication_output", return_value=current or self.row),
              mock.patch.object(DRIVER, "reader_outputs", side_effect=AssertionError("whole corpus")),
              mock.patch.object(DRIVER, "product_record", return_value={"id": self.identity}) as convert):
            status = DRIVER.product_row_json(self.identity)
        return status, output.getvalue(), errors.getvalue(), recipe, convert

    def test_worker_rechecks_the_selected_output_without_corpus_discovery(self):
        status, output, errors, recipe, convert = self.run_worker(self.row)
        self.assertEqual(status, 0, errors)
        self.assertEqual(json.loads(output), {"id": self.identity})
        recipe.assert_called_once_with("gpt", "articles/faith/example", root=ROOT)
        convert.assert_called_once_with(self.row)

    def test_worker_refuses_stale_or_unadmitted_selections_before_conversion(self):
        for changes in ({"release_status": "hold"}, {"release_status": None},
                        {"declaration": {"eligibility": "ineligible"}},
                        {"declaration": {"eligibility": "eligible", "withdrawn": "2026-11-12"}},
                        {"entrypoint": "src/gpt/articles/faith/other/main.tex"}):
            with self.subTest(changes=changes):
                status, output, errors, _, convert = self.run_worker(self.row, {**self.row, **changes})
                self.assertEqual(status, 1)
                self.assertEqual(output, "")
                self.assertTrue(errors)
                convert.assert_not_called()
        status, _, _, recipe, convert = self.run_worker(None)
        self.assertEqual(status, 1)
        recipe.assert_not_called()
        convert.assert_not_called()

    def test_indexed_worker_captures_canonical_reads_and_checks_converter_pin(self):
        dependencies = {"src/gpt/articles/faith/example/main.tex": "source-hash"}
        index = mock.Mock()
        index.verified_reads.return_value = nullcontext(dependencies)
        with (mock.patch("_corpus_index.CorpusIndex", return_value=index) as factory,
              mock.patch.object(DRIVER.sys, "stdin", io.StringIO(json.dumps(self.row))),
              mock.patch.object(DRIVER.sys, "stdout", io.StringIO()) as output,
              mock.patch.object(DRIVER, "pinned_pandoc") as pinned,
              mock.patch.object(DRIVER, "selected_product_record", return_value={"id": self.identity}) as selected):
            self.assertEqual(DRIVER.product_row_json(self.identity, indexed=True), 0)
        factory.assert_called_once_with(ROOT)
        pinned.assert_called_once()
        selected.assert_called_once_with(self.identity, self.row)
        self.assertEqual(json.loads(output.getvalue()),
                         {"record": {"id": self.identity}, "dependencies": dependencies})


if __name__ == "__main__":
    unittest.main()
