"""Build-time web editions: the reader universe and companion selection.

The converter's long-standing audits are tested in test_web_edition_conversion
and the conditional constructs in test_web_edition_constructs; this module
covers which outputs have readers and how a companion selects its own edition.
"""
from __future__ import annotations

import importlib.machinery
import importlib.util
import sys
import tempfile
import tomllib
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

    def test_no_copy_of_a_web_edition_is_tracked(self):
        import subprocess
        tracked = subprocess.run(["git", "ls-files", "--", "web"], cwd=ROOT, check=True,
                                 capture_output=True, text=True).stdout
        self.assertEqual(tracked, "")


if __name__ == "__main__":
    unittest.main()
