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
import re
import shutil
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
        # The catalogue grows, so the tripwire is that the loop ran at all.
        # The exact companion count is asserted, derived from the sources
        # rather than written down here, by
        # test_a_synthesis_companion_is_given_no_origin_of_its_own.
        self.assertGreater(seen, 0)

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
        problems, skipped, _ = tool.replay_browser_model(built)
        self.assertEqual((problems, skipped), ([], ""))
        built["counted"]["documents"] += 1
        problems, _, _ = tool.replay_browser_model(built)
        self.assertTrue(problems)
        self.assertIn("documents", problems[0])



def _load_tool():
    import importlib.machinery
    import importlib.util

    loader = importlib.machinery.SourceFileLoader("document_library", str(TOOL))
    spec = importlib.util.spec_from_loader(loader.name, loader)
    module = importlib.util.module_from_spec(spec)
    loader.exec_module(module)
    return module


class ProductionProvenanceTests(unittest.TestCase):
    """What produced each document, carried from its own record into the page.

    The catalogue is where a provenance record stops being a line in a `.tex`
    file nobody reads and becomes something a reader is shown. Every assertion
    here stands for a way that carry could succeed and be wrong: a field that
    arrived as an empty string and reads as a fact, an absence filled in on the
    way through, a synthesis companion given an origin it does not have.
    """

    @classmethod
    def setUpClass(cls) -> None:
        cls.catalogue = json.loads(TRACKED.read_text(encoding="utf-8"))
        cls.documents = _corpus.documents(extents=False)

    def test_the_record_round_trips_from_the_source_into_the_catalogue(self) -> None:
        """Read each leaf's own file again and hold the catalogue to it."""
        editions = {
            (edition["provider"], work["leaf"]): edition.get("produced", {})
            for work in self.catalogue["works"]
            for edition in work["editions"]
        }
        self.assertEqual(len(editions), len(self.documents))
        for document in self.documents:
            produced = document.provenance.produced
            carried = editions[(document.provider, document.leaf)]
            with self.subTest(document=f"{document.provider}/{document.leaf}"):
                self.assertIsNotNone(produced)
                for field in _corpus.PRODUCTION_FIELDS:
                    stated = getattr(produced, field)
                    if stated is None:
                        self.assertNotIn(field, carried)
                    else:
                        self.assertEqual(carried[field], stated)

    def test_an_absent_fact_is_omitted_and_never_filled_in(self) -> None:
        """No empty string, no zero, no plausible substitute for an unread fact."""
        for work in self.catalogue["works"]:
            for edition in work["editions"]:
                for field, value in edition.get("produced", {}).items():
                    with self.subTest(leaf=work["leaf"], field=field):
                        self.assertIn(field, _corpus.PRODUCTION_FIELDS)
                        self.assertIsInstance(value, str)
                        self.assertTrue(value.strip())
                        self.assertNotEqual(value, _corpus.UNKNOWN)

    def test_a_synthesis_companion_is_given_no_origin_of_its_own(self) -> None:
        """It is a cut of the document beside it, not a second production."""
        seen = 0
        for work in self.catalogue["works"]:
            for edition in work["editions"]:
                for issue in edition.get("also", ()):
                    seen += 1
                    self.assertNotIn("produced", issue)
        companions = sum(
            1
            for document in self.documents
            for issue in document.issues
            if issue.kind != _corpus.FULL
        )
        self.assertEqual(seen, companions)
        self.assertGreater(seen, 0)

    def test_the_catalogue_states_what_a_claim_is_measured_against(self) -> None:
        """The right-hand side travels with the left, or the comparison is guesswork."""
        declared = self.catalogue["workflows"]
        self.assertTrue(declared)
        for row in declared:
            with self.subTest(workflow=row["id"]):
                definition = json.loads(
                    (_corpus.PIPELINE_ROOT / f"{row['id']}.json").read_text("utf-8")
                )
                self.assertEqual(row["version"], str(definition["version"]))

    def test_the_declared_digest_is_the_engine_s_own_and_not_a_second_recipe(
        self,
    ) -> None:
        """The digest a run binds itself to is the digest the catalogue compares.

        Two derivations of one value is the pairing this repository keeps being
        bitten by. The catalogue asks the engine rather than recomputing, so a
        change to the digest recipe cannot leave the page comparing against a
        number no run would ever record.
        """
        sys.path.insert(0, str(ROOT / "scripts"))
        from _workflow import WorkflowEngine  # noqa: PLC0415

        engine = WorkflowEngine(ROOT, ROOT / "workflows")
        for row in self.catalogue["workflows"]:
            with self.subTest(workflow=row["id"]):
                definition = json.loads(
                    (_corpus.PIPELINE_ROOT / f"{row['id']}.json").read_text("utf-8")
                )
                self.assertEqual(
                    row["digest"], engine.workflow_source_digest(definition)
                )

    def test_a_rewritten_fragment_moves_the_declared_digest(self) -> None:
        """The property the whole comparison rests on, demonstrated."""
        sys.path.insert(0, str(ROOT / "scripts"))
        from _workflow import WorkflowEngine  # noqa: PLC0415

        definition = json.loads(
            (_corpus.PIPELINE_ROOT / "proper.json").read_text("utf-8")
        )
        # Against a copy of `workflows/`, because this edits a fragment to show
        # the digest moves. Edited in place it was a tracked source file rewritten
        # under every other test for the length of one write --- harmless while
        # the suite ran one test at a time, and a wrong digest for whoever else
        # was reading it once the suite ran tests at once. The engine takes its
        # workflows directory as an argument, so the copy needs no other change.
        workflows = Path(tempfile.mkdtemp(prefix="workflow-digest-"))
        self.addCleanup(shutil.rmtree, workflows, ignore_errors=True)
        shutil.copytree(ROOT / "workflows", workflows / "workflows",
                        symlinks=True)
        engine = WorkflowEngine(ROOT, workflows / "workflows")
        before = engine.workflow_source_digest(definition)
        fragment = "propers/author-proper.md"
        original = engine.load_fragment(fragment)
        edited = workflows / "workflows" / "fragments" / fragment
        edited.write_text(original + "\nOne further sentence.\n", encoding="utf-8")
        after = engine.workflow_source_digest(definition)
        edited.write_text(original, encoding="utf-8")
        self.assertNotEqual(before, after)
        self.assertEqual(engine.workflow_source_digest(definition), before)

    def test_an_unpublished_edition_does_not_erase_a_published_catalog(self) -> None:
        """Where a work is catalogued is stated by whichever edition states it.

        The catalog is read from each edition's own release record, and an
        edition with no release record states nothing rather than states None.
        Taking the first edition's answer let an unpublished Claude edition
        blank the catalog its published GPT sibling declares, and the published
        edition silently lost its "Catalogued in" link.
        """
        tool = _load_tool()
        by_leaf: dict[str, list] = {}
        for document in _corpus.documents(extents=False):
            by_leaf.setdefault(document.leaf, []).append(document)
        catalogued = {
            work["leaf"]: work["catalog"] for work in self.catalogue["works"]
        }
        mixed = 0
        for leaf, editions in by_leaf.items():
            stated = {document.catalog for document in editions if document.catalog}
            with self.subTest(leaf=leaf):
                self.assertEqual(catalogued[leaf], stated.pop() if stated else None)
            if stated is not None and any(
                document.catalog is None for document in editions
            ) and catalogued[leaf]:
                mixed += 1
        self.assertGreater(
            mixed,
            0,
            "no work in this corpus pairs a catalogued edition with an "
            "uncatalogued one, so this test proves nothing; find one or "
            "construct it",
        )
        self.assertIsNone(tool.work_catalog(()))

    def test_the_catalogue_carries_the_caution_that_belongs_with_it(self) -> None:
        self.assertIn("never an authority", self.catalogue["advisory"])
        self.assertIn("nothing in this repository gates on it", self.catalogue["advisory"])


class DriftVerdictTests(unittest.TestCase):
    """The one derivation of drift, asked directly, in the browser that runs it."""

    HARNESS = """
const fs = require('fs');
const holder = { exports: {} };
new Function('module', 'exports', fs.readFileSync(process.argv[1], 'utf8'))(
  holder, holder.exports
);
const input = JSON.parse(fs.readFileSync(process.argv[2], 'utf8'));
process.stdout.write(JSON.stringify(
  input.editions.map(function (edition) {
    return holder.exports.driftOf(edition, input.workflows);
  })
));
"""

    def setUp(self) -> None:
        if not MODEL.is_file():
            self.skipTest("the browser model is absent")
        try:
            subprocess.run(["node", "--version"], capture_output=True, check=True)
        except (FileNotFoundError, subprocess.CalledProcessError):
            self.skipTest("node is not installed")

    def verdicts(self, editions: list, workflows: list) -> list:
        with tempfile.TemporaryDirectory() as scratch:
            payload = Path(scratch) / "input.json"
            payload.write_text(
                json.dumps({"editions": editions, "workflows": workflows}), "utf-8"
            )
            result = subprocess.run(
                ["node", "-e", self.HARNESS, str(MODEL), str(payload)],
                capture_output=True,
                text=True,
                check=False,
            )
        self.assertEqual(result.returncode, 0, result.stderr)
        return json.loads(result.stdout)

    def test_an_unknown_origin_makes_no_claim(self) -> None:
        """Three ways to have no comparison, and all three stay silent.

        Not "current", not "unknown drift", not a neutral mark a reader would
        take for no news: nothing at all, because there is nothing to say.
        """
        workflows = [{"id": "proper", "version": "14"}]
        editions = [
            {},
            {"produced": {}},
            {"produced": {"install_commit": "c" * 40}},
            {"produced": {"workflow_id": "proper"}},
            {"produced": {"workflow_version": "10"}},
            {"produced": {"workflow_id": "retired", "workflow_version": "3"}},
        ]
        self.assertEqual(self.verdicts(editions, workflows), [None] * len(editions))
        self.assertEqual(self.verdicts(editions[:1], []), [None])

    def test_a_recorded_origin_names_both_sides_of_the_comparison(self) -> None:
        workflows = [{"id": "proper", "version": "14", "digest": "a" * 64}]
        behind, level = self.verdicts(
            [
                {
                    "produced": {
                        "workflow_id": "proper",
                        "workflow_version": "10",
                        "workflow_digest": "b" * 64,
                    }
                },
                {
                    "produced": {
                        "workflow_id": "proper",
                        "workflow_version": "14",
                        "workflow_digest": "a" * 64,
                    }
                },
            ],
            workflows,
        )
        self.assertEqual(
            behind,
            {
                "workflow": "proper",
                "recorded": "10",
                "current": "14",
                "recordedDigest": "b" * 64,
                "currentDigest": "a" * 64,
                "behind": True,
                "ahead": False,
                "revised": True,
            },
        )
        self.assertEqual(
            level,
            {
                "workflow": "proper",
                "recorded": "14",
                "current": "14",
                "recordedDigest": "a" * 64,
                "currentDigest": "a" * 64,
                "behind": False,
                "ahead": False,
                "revised": False,
            },
        )

    def test_a_rewritten_fragment_is_visible_though_the_version_did_not_move(
        self,
    ) -> None:
        """The requirement this comparison exists to meet.

        The version is an integer somebody types and nothing forces them to.
        The workflow-source digest covers the pipeline, every stage and lane
        fragment and every schema, so it moves the moment guidance is edited.
        Carrying only the version meant a fragment could be rewritten under a
        whole corpus and every document still read as current — which is to say
        the stated purpose, knowing which documents are behind the guidance as
        it evolves, was not being served at all.
        """
        (verdict,) = self.verdicts(
            [
                {
                    "produced": {
                        "workflow_id": "proper",
                        "workflow_version": "14",
                        "workflow_digest": "b" * 64,
                    }
                }
            ],
            [{"id": "proper", "version": "14", "digest": "a" * 64}],
        )
        self.assertFalse(verdict["behind"])
        self.assertFalse(verdict["ahead"])
        self.assertTrue(verdict["revised"])

    def test_a_missing_digest_on_either_side_makes_no_claim_about_revision(
        self,
    ) -> None:
        """An absence is not a comparison, and never resolves to False."""
        for produced_digest, declared_digest in (
            (None, "a" * 64),
            ("a" * 64, None),
            (None, None),
        ):
            produced = {"workflow_id": "proper", "workflow_version": "14"}
            if produced_digest:
                produced["workflow_digest"] = produced_digest
            declared = {"id": "proper", "version": "14"}
            if declared_digest:
                declared["digest"] = declared_digest
            with self.subTest(produced=bool(produced_digest), declared=bool(declared_digest)):
                (verdict,) = self.verdicts([{"produced": produced}], [declared])
                self.assertIsNone(verdict["revised"])

    def test_a_document_ahead_of_the_declared_version_is_not_called_behind(
        self,
    ) -> None:
        """String inequality answered "behind" to a document recorded ahead.

        v9 against v14 and v20 against v14 are different situations and only
        one of them is the document trailing the repository. Versions are whole
        numbers, so they are compared as whole numbers; where either side is
        not a whole number the model falls back to plain inequality rather than
        inventing an order over strings.
        """
        workflows = [{"id": "proper", "version": "14"}]
        nine, twenty, same = self.verdicts(
            [
                {"produced": {"workflow_id": "proper", "workflow_version": "9"}},
                {"produced": {"workflow_id": "proper", "workflow_version": "20"}},
                {"produced": {"workflow_id": "proper", "workflow_version": "14"}},
            ],
            workflows,
        )
        self.assertEqual((nine["behind"], nine["ahead"]), (True, False))
        self.assertEqual((twenty["behind"], twenty["ahead"]), (False, True))
        self.assertEqual((same["behind"], same["ahead"]), (False, False))

    def test_a_version_that_is_not_a_whole_number_falls_back_to_inequality(
        self,
    ) -> None:
        (verdict,) = self.verdicts(
            [{"produced": {"workflow_id": "proper", "workflow_version": "2026.1"}}],
            [{"id": "proper", "version": "14"}],
        )
        self.assertTrue(verdict["behind"])
        self.assertFalse(verdict["ahead"])

    def test_the_real_catalogue_claims_nothing_it_cannot_support(self) -> None:
        catalogue = json.loads(TRACKED.read_text(encoding="utf-8"))
        editions = [
            edition
            for work in catalogue["works"]
            for edition in work["editions"]
        ]
        declared = {row["id"]: row["version"] for row in catalogue["workflows"]}
        for edition, verdict in zip(
            editions, self.verdicts(editions, catalogue["workflows"])
        ):
            produced = edition.get("produced", {})
            comparable = (
                produced.get("workflow_id") in declared
                and produced.get("workflow_version") is not None
            )
            with self.subTest(edition=edition.get("title")):
                self.assertEqual(verdict is not None, comparable)


class DriftIsAdvisoryTests(unittest.TestCase):
    """Nothing gates on drift, and this is what would notice if something did."""

    def test_a_corpus_entirely_behind_still_passes_the_catalogue_check(self) -> None:
        """Put every document behind its workflow and the gate must not care."""
        tool = _load_tool()
        built = json.loads(TRACKED.read_text(encoding="utf-8"))
        built["workflows"] = [{"id": "proper", "version": "9999"}]
        for work in built["works"]:
            for edition in work["editions"]:
                edition.setdefault("produced", {})
                edition["produced"]["workflow_id"] = "proper"
                edition["produced"]["workflow_version"] = "1"
        problems, _, drift = tool.replay_browser_model(built)
        self.assertEqual(problems, [])
        self.assertEqual(drift["behind"], drift["editions"])
        self.assertEqual(drift["silent"], 0)

    #: Every name by which the verdict, or a count derived from it, can be
    #: referred to. Derived from the model and the tool rather than written
    #: down, so a new verdict field cannot be added without this list growing
    #: with it — a two-literal list was the whole evidence for "nothing gates
    #: on it", and it would not have noticed a third name being introduced.
    def verdict_names(self) -> set[str]:
        model = MODEL.read_text(encoding="utf-8")
        names = set(re.findall(r"\b(drift[A-Z][A-Za-z]*|compareVersions)\b", model))
        tool = TOOL.read_text(encoding="utf-8")
        names |= {
            name
            for name in re.findall(r'"([a-z_]*(?:drift|workflow|produced)[a-z_]*)"', tool)
            if name.startswith(("produced_under", "production_", "workflows_"))
        }
        names |= {"driftOf", "produced_under_a_superseded_workflow"}
        return {name for name in names if len(name) > 4}

    def test_no_gate_command_and_no_make_recipe_reads_the_verdict(self) -> None:
        """The comparison exists in one file and is consumed by one page.

        Two things are checked and the second is the one that matters. First,
        that no pipeline command and no Make recipe names the verdict or any
        count derived from it — the names being derived from the model and the
        tool, so a field added later is covered without anyone remembering to
        add it here. Second, that the tool that computes the verdict still
        exits zero when every edition in the corpus is behind: a grep proves a
        name is absent, and only running the check proves nothing acts on it.
        """
        watched = self.verdict_names()
        self.assertGreaterEqual(len(watched), 3, watched)
        pipelines = sorted(_corpus.PIPELINE_ROOT.glob("*.json"))
        self.assertTrue(pipelines)
        for path in pipelines + [ROOT / "Makefile"]:
            text = path.read_text(encoding="utf-8")
            for needle in watched:
                with self.subTest(path=path.name, needle=needle):
                    self.assertNotIn(needle, text)

    def test_the_gate_commands_that_do_run_still_pass_over_a_drifted_corpus(
        self,
    ) -> None:
        """Absence of a name proves nothing; running the checks proves it.

        `document-library check` and `check-generation-metadata` are the two
        commands a pipeline actually runs over these records. Neither may
        change its verdict because a document is behind its workflow.
        """
        library = run("check")
        self.assertEqual(library.returncode, 0, library.stderr)
        self.assertIn("advisory; nothing gates on it", library.stdout)
        metadata = subprocess.run(
            [sys.executable, str(ROOT / "tools" / "check-generation-metadata"),
             "--provider", "claude"],
            capture_output=True, text=True, cwd=ROOT,
        )
        self.assertEqual(metadata.returncode, 0, metadata.stderr)

    def test_the_comparison_cannot_go_dark_with_the_check_still_green(self) -> None:
        """Silence for want of a right-hand side is not silence for want of a claim.

        Emptying the declared-workflow list made every verdict null, every
        edition "silent", and the check green — indistinguishable from a corpus
        that records no origin, which is what "silent" is supposed to mean. The
        feature could be switched off and nothing would say so.
        """
        tool = _load_tool()
        built = json.loads(TRACKED.read_text(encoding="utf-8"))
        built["workflows"] = []
        problems, _, drift = tool.replay_browser_model(built)
        self.assertTrue(problems, "an empty declared-workflow list passed silently")
        self.assertTrue(
            any("no workflows" in problem for problem in problems), problems
        )
        self.assertEqual(drift["silent"], drift["editions"])

    def test_a_pipeline_that_declares_no_identity_is_refused_not_skipped(self) -> None:
        """Skipping it removed one side of every comparison without saying so."""
        with tempfile.TemporaryDirectory(dir=ROOT / "build") as scratch:
            pipelines = Path(scratch) / "pipelines"
            pipelines.mkdir()
            (pipelines / "nameless.json").write_text('{"stages": []}\n', "utf-8")
            with self.assertRaises(_corpus.CorpusError):
                _corpus.declared_workflows(pipelines)
            empty = Path(scratch) / "empty" / "pipelines"
            empty.mkdir(parents=True)
            with self.assertRaises(_corpus.CorpusError):
                _corpus.declared_workflows(empty)

    def test_the_verdict_borrows_no_vocabulary_from_the_staleness_ledger(self) -> None:
        """A different question of different inputs keeps its own words.

        `guidance/staleness.md` owns "stale", "staleness" and "rebaseline", and
        one of them means a review happened. This comparison means nothing of
        the kind and must not be read as though it did.
        """
        page = (ROOT / "src/web/browser/texts/texts.js").read_text(encoding="utf-8")
        shown = re.findall(r"'([^'\\]{4,})'", page) + re.findall(r'"([^"\\]{4,})"', page)
        self.assertTrue(shown)
        for literal in shown:
            for word in ("stale", "rebaseline"):
                with self.subTest(literal=literal[:40], word=word):
                    self.assertNotIn(word, literal.lower())


if __name__ == "__main__":
    unittest.main()
