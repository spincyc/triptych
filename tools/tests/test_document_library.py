#!/usr/bin/env python3
"""The document catalogue: what it derives, and what it refuses to invent.

Every assertion here stands for a way this catalogue could resolve successfully
and wrongly. A title read out of the wrong file is fluent and plausible and
names the document something it is not; a summary the page derives differently
from the generator shows a reader a corpus that does not exist; a tracked
catalogue nobody regenerated serves last week's corpus under this week's counts.
None of those breaks anything, which is why each one is checked rather than
trusted.
"""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))

import _corpus  # noqa: E402

TOOL = ROOT / "tools" / "document-library"
TRACKED = ROOT / "src/web/data/structure/documents/corpus.json"
MODEL = ROOT / "src/web/browser/texts/catalogue-model.js"


def run(*argv: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, str(TOOL), *argv], capture_output=True, text=True, cwd=ROOT
    )


class CorpusReadingTests(unittest.TestCase):
    """The four records a document keeps, read once and read from the document."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.documents = _corpus.documents(extents=False)

    def test_every_leaf_with_a_main_is_carried(self) -> None:
        found = {(document.provider, document.leaf) for document in self.documents}
        expected = {
            (main.relative_to(_corpus.SRC).parts[0],
             main.parent.relative_to(_corpus.SRC / main.relative_to(_corpus.SRC).parts[0]).as_posix())
            for provider in _corpus.PROVIDERS
            for main in (_corpus.SRC / provider).glob("**/main.tex")
        }
        self.assertEqual(found, expected)

    def test_every_document_states_a_title_or_says_it_does_not(self) -> None:
        """Exactly one of the two, never neither and never both."""
        for document in self.documents:
            for issue in document.issues:
                with self.subTest(document=f"{document.provider}/{issue.stem}"):
                    stated = issue.title.text is not None
                    absent = issue.title.absent is not None
                    self.assertNotEqual(stated, absent)
                    if stated:
                        self.assertTrue(issue.title.source)

    def test_a_composed_title_records_the_template_it_was_composed_from(self) -> None:
        """The thirty-four curriculum titles are assembled by a shared shell.

        A composed title must carry the template, so a reader can see that the
        module's id and its own title were put together rather than printed as
        one string somewhere. A title that was not composed carries no template
        at all: a template identical to the title is a restatement.
        """
        composed = [
            issue
            for document in self.documents
            for issue in document.issues
            if issue.title.template
        ]
        self.assertEqual(len(composed), 34)
        for issue in composed:
            with self.subTest(stem=issue.stem):
                self.assertNotEqual(issue.title.template, issue.title.text)
                self.assertIn("\\", issue.title.template)

    def test_an_inherited_ledger_is_pointed_at_and_never_copied(self) -> None:
        inheriting = [d for d in self.documents if d.provenance.inherits]
        self.assertTrue(inheriting)
        for document in inheriting:
            with self.subTest(leaf=document.leaf):
                self.assertEqual(document.provenance.contributions, ())


class TitleAbsenceTests(unittest.TestCase):
    """A document with no title is carried, by path, with the reason.

    Nothing in this repository is in that state today, which is exactly why it
    is exercised here: a branch no data reaches is a branch that has never been
    shown to work, and the first document to lose its title would be the first
    to find out.
    """

    def test_a_preamble_with_no_pdftitle_yields_a_stated_absence(self) -> None:
        with tempfile.TemporaryDirectory(dir=ROOT / "build") as scratch:
            entry = Path(scratch) / "main.tex"
            entry.write_text(
                "\\newcommand{\\Nothing}{}\n\\begin{document}\nhello\n\\end{document}\n",
                encoding="utf-8",
            )
            title = _corpus.title_of(entry, "claude")
        self.assertIsNone(title.text)
        self.assertEqual(title.absent, _corpus.NO_TITLE)
        self.assertIsNone(title.source)

    def test_a_commented_out_title_states_nothing(self) -> None:
        """A `%`-commented declaration is not a declaration."""
        with tempfile.TemporaryDirectory(dir=ROOT / "build") as scratch:
            entry = Path(scratch) / "main.tex"
            entry.write_text(
                "% \\hypersetup{pdftitle={A Name Nobody Declared}}\n"
                "\\begin{document}\n\\end{document}\n",
                encoding="utf-8",
            )
            title = _corpus.title_of(entry, "claude")
        self.assertIsNone(title.text)

    def test_the_branch_a_flag_selects_is_the_one_read(self) -> None:
        """A synthesis issue must not be catalogued under the full issue's name."""
        with tempfile.TemporaryDirectory(dir=ROOT / "build") as scratch:
            body = (
                "\\ifdefined\\TriptychSynthesisEdition\n"
                "  \\hypersetup{pdftitle={Short Form}}\n"
                "\\else\n"
                "  \\hypersetup{pdftitle={Whole Thing}}\n"
                "\\fi\n"
                "\\begin{document}\n\\end{document}\n"
            )
            main = Path(scratch) / "main.tex"
            main.write_text(body, encoding="utf-8")
            synthesis = Path(scratch) / "synthesis.tex"
            synthesis.write_text(
                "\\def\\TriptychSynthesisEdition{1}\n" + body, encoding="utf-8"
            )
            self.assertEqual(_corpus.title_of(main, "claude").text, "Whole Thing")
            self.assertEqual(_corpus.title_of(synthesis, "claude").text, "Short Form")


class TrackedCatalogueTests(unittest.TestCase):
    """The file the page fetches, and the guard that keeps it current."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.catalogue = json.loads(TRACKED.read_text(encoding="utf-8"))

    def test_the_tracked_catalogue_is_what_the_sources_produce_now(self) -> None:
        result = run("structure", "--check")
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_structure_check_refuses_a_catalogue_that_has_drifted(self) -> None:
        """The guard has to fail on a real gap, not merely exist."""
        with tempfile.TemporaryDirectory(dir=ROOT / "build") as scratch:
            stale = Path(scratch) / "structure" / "documents" / "corpus.json"
            stale.parent.mkdir(parents=True)
            stale.write_text('{"schema": "stale"}\n', encoding="utf-8")
            result = run("structure", "--check", "--out", scratch)
        self.assertEqual(result.returncode, 2, result.stdout)
        self.assertIn("drifted", result.stderr)

    def test_a_synthesis_issue_writes_only_what_it_departs_on(self) -> None:
        """`also` carries the difference; a field it shares is not restated."""
        seen = 0
        for work in self.catalogue["works"]:
            for edition in work["editions"]:
                for issue in edition.get("also", ()):
                    seen += 1
                    with self.subTest(leaf=work["leaf"], kind=issue["kind"]):
                        for field in ("status", "authorization"):
                            if field in issue:
                                self.assertNotEqual(issue[field], edition[field])
                        self.assertNotEqual(issue.get("title"), edition["title"])
        self.assertEqual(seen, 8)

    def test_every_offered_choice_selects_something(self) -> None:
        """A control that offers an empty answer is a control that lies."""
        for kind in ("providers", "models", "sections"):
            self.assertTrue(self.catalogue[kind], kind)
            for row in self.catalogue[kind]:
                with self.subTest(kind=kind, id=row["id"]):
                    self.assertGreater(row.get("documents", row.get("works", 0)), 0)

    def test_the_catalogue_carries_its_own_caution(self) -> None:
        """A consumer that has the file has the warning that belongs with it."""
        self.assertIn("never given an invented name", self.catalogue["advisory"])


class BrowserModelTests(unittest.TestCase):
    """The page's own derivation, replayed, and proved able to fail."""

    def setUp(self) -> None:
        if not MODEL.is_file():
            self.skipTest("the browser model is absent")
        try:
            subprocess.run(["node", "--version"], capture_output=True, check=True)
        except (FileNotFoundError, subprocess.CalledProcessError):
            self.skipTest("node is not installed")

    def test_check_replays_the_model_and_agrees_with_it(self) -> None:
        result = run("check", "--provider", "claude")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("catalogue-model.js", result.stdout)

    def test_the_replay_fails_when_a_summary_disagrees_with_the_rows(self) -> None:
        """Corrupt one offered count and the comparison must catch it."""
        import importlib.machinery
        import importlib.util

        loader = importlib.machinery.SourceFileLoader("document_library", str(TOOL))
        spec = importlib.util.spec_from_loader(loader.name, loader)
        tool = importlib.util.module_from_spec(spec)
        loader.exec_module(tool)

        built = json.loads(TRACKED.read_text(encoding="utf-8"))
        self.assertEqual(tool.replay_browser_model(built), ([], ""))
        built["counted"]["documents"] += 1
        problems, _ = tool.replay_browser_model(built)
        self.assertTrue(problems)
        self.assertIn("documents", problems[0])


if __name__ == "__main__":
    unittest.main()
