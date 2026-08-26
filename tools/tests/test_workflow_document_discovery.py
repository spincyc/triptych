#!/usr/bin/env python3
"""A document id you can find, and a name short enough to type.

`tpt proper --help` read `--help` as the document id and failed for want of an
action. Nothing listed the ids a workflow could run, so the only way to obtain
one was to go reading `src/`, and the whole 60-character path had to be typed
exactly. The workflow now declares where its documents live, the launcher can
list them, and any unique tail of an id stands for the id.
"""
import json
import shutil
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
LAUNCHER = ROOT / "tools" / "tpt"
sys.path.insert(0, str(ROOT / "scripts"))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from _workflow import WorkflowEngine, WorkflowError  # noqa: E402
from test_workflow_adversarial import (  # noqa: E402
    WORKFLOW,
    engine_for,
    make_repo,
)
from test_workflow_research_fanout import DOC  # noqa: E402

TAIL = DOC.rsplit("/", 1)[-1]

ACTIONS = ("seed", "advance", "status", "replay", "intervene", "debt")


def tpt(*argv: str) -> subprocess.CompletedProcess:
    return subprocess.run([str(LAUNCHER), *argv], capture_output=True,
                          text=True, cwd=ROOT)


class HelpTests(unittest.TestCase):
    """The help a workflow gives about itself."""

    def test_help_is_help_and_not_a_document_id(self):
        """The defect: `--help` was parsed as the document id."""
        for flag in ("--help", "-h", "help"):
            with self.subTest(flag=flag):
                done = tpt("proper", flag)
                self.assertEqual(done.returncode, 0, done.stderr)
                self.assertNotIn("missing action", done.stdout + done.stderr)
                self.assertNotIn("missing document id",
                                 done.stdout + done.stderr)
                self.assertIn("tpt proper", done.stdout)

    def test_bare_workflow_prints_help_rather_than_an_error(self):
        done = tpt("proper")
        self.assertEqual(done.returncode, 0, done.stderr)
        self.assertIn("usage:", done.stdout)

    def test_the_help_names_every_action_and_its_flags(self):
        done = tpt("proper", "--help")
        for action in ACTIONS:
            with self.subTest(action=action):
                self.assertIn(f"tpt proper <proper> {action}", done.stdout)
        for flag in ("--provider", "--result", "--lane-result", "--run-gate",
                     "--text", "--stage", "--json"):
            with self.subTest(flag=flag):
                self.assertIn(flag, done.stdout)

    def test_the_help_says_how_to_find_a_document_id(self):
        done = tpt("proper", "--help")
        self.assertIn("tpt proper list", done.stdout)
        self.assertIn("a full id:", done.stdout)
        self.assertIn("or any unique tail of one:", done.stdout)
        self.assertIn("liturgy/roman-rite/1962/propers/", done.stdout)

    def test_the_help_states_the_workflow_version(self):
        engine = WorkflowEngine(ROOT, ROOT / "workflows")
        version = engine.load_workflow("proper")["version"]
        self.assertIn(f"(v{version})", tpt("proper", "--help").stdout)

    def test_an_unknown_action_points_at_the_usage(self):
        done = tpt("proper", TAIL, "frobnicate")
        self.assertEqual(done.returncode, 2)
        self.assertIn("unknown workflow action", done.stderr)
        self.assertIn("tpt proper --help", done.stderr)


class ListingTests(unittest.TestCase):
    """`tpt <workflow> list`."""

    @classmethod
    def setUpClass(cls):
        cls.engine = WorkflowEngine(ROOT, ROOT / "workflows")
        cls.workflow = cls.engine.load_workflow("proper")
        cls.documents = cls.engine.list_documents(cls.workflow)

    def test_the_listing_is_every_discovered_document_in_order(self):
        done = tpt("proper", "list")
        self.assertEqual(done.returncode, 0, done.stderr)
        printed = done.stdout.split()
        self.assertEqual(printed, self.documents)
        self.assertEqual(printed, sorted(printed), "deterministic order")
        self.assertEqual(len(printed), len(set(printed)),
                         "one entry per document, not one per provider")

    def test_the_json_listing_is_the_same_set(self):
        done = tpt("proper", "list", "--json")
        self.assertEqual(done.returncode, 0, done.stderr)
        self.assertEqual(json.loads(done.stdout), self.documents)

    def test_an_unknown_listing_option_fails_closed(self):
        done = tpt("proper", "list", "--bogus")
        self.assertEqual(done.returncode, 2)
        self.assertIn("unknown option", done.stderr)

    def test_every_listed_document_really_exists(self):
        self.assertTrue(self.documents, "the propers workflow has documents")
        discovery = self.workflow["document_discovery"]
        for document in self.documents:
            with self.subTest(document=document):
                homes = sorted(
                    p for p in ROOT.glob(f"src/*/{document}")
                    if (p / discovery["marker"]).is_file())
                self.assertTrue(
                    homes, f"{document} has no {discovery['marker']}")

    def test_a_leaf_without_the_marker_is_not_listed(self):
        """Discovery names what can actually be run, not every directory."""
        engine = WorkflowEngine(ROOT, ROOT / "workflows")
        marker = self.workflow["document_discovery"]["marker"]
        without = [
            "/".join(p.relative_to(ROOT).parts[2:])
            for p in ROOT.glob(self.workflow["document_discovery"]["search"])
            if p.is_dir() and not (p / marker).is_file()
        ]
        for document in without:
            with self.subTest(document=document):
                self.assertNotIn(document, engine.list_documents(self.workflow))


class ShorthandTests(unittest.TestCase):
    """A unique tail of an id stands for the id."""

    @classmethod
    def setUpClass(cls):
        cls.engine = WorkflowEngine(ROOT, ROOT / "workflows")
        cls.workflow = cls.engine.load_workflow("proper")
        cls.documents = cls.engine.list_documents(cls.workflow)

    def resolve(self, token: str) -> str:
        return self.engine.resolve_document(self.workflow, token)

    def test_a_full_id_resolves_to_itself(self):
        for document in self.documents:
            with self.subTest(document=document):
                self.assertEqual(self.resolve(document), document)

    def test_every_leaf_slug_resolves_to_its_own_document(self):
        for document in self.documents:
            with self.subTest(document=document):
                self.assertEqual(
                    self.resolve(document.rsplit("/", 1)[-1]), document)

    def test_an_ambiguous_shorthand_is_refused_with_its_candidates(self):
        with self.assertRaises(WorkflowError) as caught:
            self.resolve("pentecost")
        message = str(caught.exception)
        self.assertIn("matches", message)
        matching = [d for d in self.documents if "pentecost" in d]
        self.assertGreater(len(matching), 1)
        for document in matching:
            self.assertIn(document, message)

    def test_an_unknown_shorthand_points_at_the_listing(self):
        with self.assertRaises(WorkflowError) as caught:
            self.resolve("no-such-proper-anywhere")
        self.assertIn("tools/tpt proper list", str(caught.exception))

    def test_an_unknown_shorthand_says_how_to_name_a_new_document(self):
        """Seeding a document that does not exist yet is a first-class case.

        The seed stage's own job is to report what a leaf is missing, so a
        shorthand that resolves only against what exists must say how to name
        what does not.
        """
        with self.assertRaises(WorkflowError) as caught:
            self.resolve("55-fifteenth-after-pentecost")
        message = str(caught.exception)
        self.assertIn("does not exist yet is named in full", message)
        self.assertIn(
            "liturgy/roman-rite/1962/propers/temporal/"
            "55-fifteenth-after-pentecost", message,
            "the full id is shown ready to copy")
        for parent in sorted({d.rsplit("/", 1)[0] for d in self.documents}):
            self.assertIn(f"{parent}/55-fifteenth-after-pentecost", message)

    def test_a_full_id_that_does_not_exist_yet_still_seeds(self):
        """And the path it points at really works."""
        runs = ROOT / "build" / "tpt-runs-newdoc-test"
        shutil.rmtree(runs, ignore_errors=True)
        self.addCleanup(shutil.rmtree, runs, ignore_errors=True)
        engine = WorkflowEngine(ROOT, ROOT / "workflows")
        engine.runs_dir = runs
        new = ("liturgy/roman-rite/1962/propers/temporal/"
               "55-fifteenth-after-pentecost")
        self.assertNotIn(new, self.documents)
        self.assertEqual(engine.resolve_document(self.workflow, new), new)
        seeded = json.loads(
            engine.seed_bytes("proper", {"proper": new, "provider": "gpt"}))
        self.assertEqual(seeded["normalized_args"]["proper"], new)
        self.assertEqual(seeded["stage"], "seed")

    def test_a_path_is_passed_through_untouched(self):
        """Strictly additive: what worked before still works."""
        for token in ("liturgy/roman-rite/1962/propers/temporal/99-invented",
                      "some/other/document"):
            with self.subTest(token=token):
                self.assertEqual(self.resolve(token), token)

    def test_a_workflow_without_discovery_resolves_nothing(self):
        repo = make_repo()
        self.addCleanup(shutil.rmtree, repo, ignore_errors=True)
        engine = engine_for(repo)
        workflow = engine.load_workflow("adv-wf")
        self.assertNotIn("document_discovery", workflow)
        self.assertEqual(engine.resolve_document(workflow, "d1"), "d1")
        with self.assertRaises(WorkflowError) as caught:
            engine.list_documents(workflow)
        self.assertIn("declares no 'document_discovery'", str(caught.exception))

    def test_the_shorthand_is_a_pure_alias(self):
        """Seeding by tail and by full id must be the same run, byte for byte."""
        runs = ROOT / "build" / "tpt-runs-shorthand-test"
        shutil.rmtree(runs, ignore_errors=True)
        self.addCleanup(shutil.rmtree, runs, ignore_errors=True)
        engine = WorkflowEngine(ROOT, ROOT / "workflows")
        engine.runs_dir = runs
        full = DOC
        by_full = engine.seed_bytes(
            "proper", {"proper": self.resolve(full), "provider": "gpt"})
        by_tail = engine.seed_bytes(
            "proper",
            {"proper": self.resolve(TAIL),
             "provider": "gpt"})
        self.assertEqual(by_full, by_tail)
        self.assertEqual(json.loads(by_full)["normalized_args"]["proper"], full)

    def test_the_launcher_resolves_the_shorthand_for_every_action(self):
        done = tpt("proper", TAIL, "status", "deadbeef")
        self.assertEqual(done.returncode, 2)
        self.assertIn("no such run", done.stderr,
                      "the shorthand resolved and the run lookup was reached")
        done = tpt("proper", "no-such-proper-anywhere", "status", "deadbeef")
        self.assertEqual(done.returncode, 2)
        self.assertIn("no proper matches", done.stderr)


    def test_a_misspelling_of_an_existing_document_is_named(self):
        typo = TAIL.replace("pentecost", "penecost")
        self.assertNotEqual(typo, TAIL, "the probe id contains 'pentecost'")
        with self.assertRaises(WorkflowError) as caught:
            self.resolve(typo)
        message = str(caught.exception)
        self.assertIn("did you mean:", message)
        self.assertIn(DOC, message)

    def test_a_new_name_from_the_same_family_suggests_nothing(self):
        """These ids share most of their text, so similarity alone is noise.

        A new ordinal in an existing series can score highly against its
        neighbours; a real typo leads by substantially more. Suggesting on
        similarity alone offered wrong answers to someone naming a document
        that simply did not exist yet.
        """
        for token in ("55-fifteenth-after-pentecost",
                      "55-fifteenth-after-penecost",
                      "99-something-entirely-else"):
            with self.subTest(token=token):
                with self.assertRaises(WorkflowError) as caught:
                    self.resolve(token)
                self.assertNotIn("did you mean", str(caught.exception))

    def test_a_misspelling_of_any_document_finds_that_document(self):
        """Derived from the corpus, so renumbering cannot invalidate it.

        Each id has one character dropped from its distinguishing head. That
        either still resolves outright, by the substring pass, or is refused
        with a suggestion — and in both cases it must land on the document it
        was made from, never on a neighbour.
        """
        for document in self.documents:
            tail = document.rsplit("/", 1)[-1]
            typo = tail[:3] + tail[4:]
            with self.subTest(document=document, typo=typo):
                try:
                    self.assertEqual(self.resolve(typo), document)
                except WorkflowError as error:
                    self.assertIn("did you mean:", str(error))
                    self.assertIn(document, str(error))
                    self.assertEqual(str(error).count("did you mean"), 1,
                                     "one answer, not a list to choose from")


class DeclarationTests(unittest.TestCase):
    """The workflow owns the rule, and a malformed one fails closed."""

    def test_the_propers_workflow_declares_where_its_documents_live(self):
        engine = WorkflowEngine(ROOT, ROOT / "workflows")
        discovery = engine.load_workflow("proper")["document_discovery"]
        self.assertEqual(set(discovery),
                         {"search", "marker", "id_drops_leading"})
        self.assertEqual(discovery["marker"], "main.tex")
        self.assertEqual(discovery["id_drops_leading"], 2,
                         "an id is the path under src/<provider>/")

    def test_a_malformed_declaration_fails_closed(self):
        import copy
        cases = {
            "not-an-object": "src/*",
            "no-search": {"marker": "main.tex", "id_drops_leading": 1},
            "empty-search": {"search": "", "id_drops_leading": 1},
            "no-drops": {"search": "src/*"},
            "negative-drops": {"search": "src/*", "id_drops_leading": -1},
            "wrong-type-drops": {"search": "src/*", "id_drops_leading": "2"},
            "extra-key": {"search": "src/*", "id_drops_leading": 1,
                          "depth": 3},
        }
        for name, discovery in cases.items():
            with self.subTest(case=name):
                workflow = copy.deepcopy(WORKFLOW)
                workflow["document_discovery"] = discovery
                repo = make_repo(workflow)
                self.addCleanup(shutil.rmtree, repo, ignore_errors=True)
                with self.assertRaises(WorkflowError) as caught:
                    engine_for(repo).load_workflow("adv-wf")
                self.assertIn("document_discovery", str(caught.exception))

    def test_the_registered_tool_surface_is_unchanged(self):
        self.assertEqual(tpt("--check").returncode, 0)
        listed = tpt("workflow", "list")
        self.assertEqual(listed.returncode, 0, listed.stderr)
        self.assertIn("proper", listed.stdout)
        parsed = tpt("citations", "parse", "Psalm 24:1-3", "--json")
        self.assertEqual(parsed.returncode, 0, parsed.stderr)


if __name__ == "__main__":
    unittest.main()
