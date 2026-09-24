#!/usr/bin/env python3
"""A shell decides what a shell can decide, before five AI lanes are spent.

Two rounds of a production run spent a five-lane content evaluation
discovering References entries the body never cites, a cited source
identifier that resolved to nothing, a manifest relation the brief restated
with the wrong element keys, and a witness quoted in a guide that says four
times it does not quote him. None of those is a judgment. `content-preflight`
runs between `author-proper` and `content-evaluation` and settles them by exit
code, so the evaluation behind it spends its budget on what only judgment can
settle.

Its failures go to `content-revision` and never to research. A mechanical
defect in the leaf is repaired in the leaf; nothing about it says the evidence
under the leaf is wrong, and routing it to `research` would re-run seven lanes
over a defect grep found.

A third round did it again, over one leaf and one class of defect. Three
successive max-effort evaluations found about 96 sentences whose grammatical
subject was the guide, its sweep, its apparatus or the repository, then about
10, then 22; each pass repaired the ones it named and the next found a fresh
subset of the same forms, and the run terminated BLOCKED with its whole
evaluation budget spent on them. The same run lost a real defect in the
opposite way: one exploratory proposal of six had replaced a required field
with a heading of the author's own, and it fell between two lanes' criteria
with no lane owning it. `house-voice` and `proposal-fields` are those two,
made mechanical.
"""
import json
import shlex
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from _audited_corpus import AUDITED_COMMIT, audited_tree  # noqa: E402
from _parallel import gather  # noqa: E402

from _workflow import (  # noqa: E402
    BLOCKED,
    FAIL,
    PASS,
    PROGRAM,
    _current_packet,
    _substitute_args,
)
from test_workflow_research_fanout import (  # noqa: E402
    DOC,
    workflow_json,
)
from test_workflow_repair_routing import (  # noqa: E402
    RESEARCH,
    RoutingCase,
    blocking,
)

STAGE = "content-preflight"
TOOL = "check-content-preflight"
ERROR = f"{TOOL} error: "
# The check that holds the leaf against the run producing it, and the six
# that read only the tree. It is kept apart because everything about how it is
# run is different: it takes the run's own identity, the gate supplies that
# identity from the engine, and no published leaf can satisfy it outside the
# run that wrote its provenance record.
RUN_CHECK = "provenance-matches-run"
LEAF_CHECKS = ("references-used", "identifiers-resolve", "bindings-valid",
               "restricted-not-reproduced", "relation-coverage",
               "unquoted-not-quoted")
# The one check that reads more than the leaf: `bindings-valid` runs the
# source library's own validator over `research/source-bindings.toml`. The
# probe tree below is a synthetic leaf with no binding record and no
# `src/sources/` beside it, so the probe is driven without this one; the
# published leaf and the real gate below run it like any other.
PROBE_ONLY_ABSENT = ("bindings-valid",)
# The three that hold the leaf against the Scripture chronology corpus. They
# read only the tree, like LEAF_CHECKS, but they are named apart because what
# they do over a leaf depends on the workflow version that leaf states: the
# contract binds from `proper` v17, and every leaf published before it is
# reported out of scope rather than refused for work that was correct when it
# was done. See tools/tests/test_workflow_chronology.py, which drives them
# over a leaf that IS bound.
CHRONOLOGY_CHECKS = ("chronology-record-current",
                     "chronology-annotations-current",
                     "chronology-claims-supported")
# The two that read the reader-facing prose rather than the records under it.
# They are named apart because they were written after this corpus was, and
# what they find in it is a fact about the corpus rather than about them:
# `house-voice` once refused eight of the twelve leaves that carried a
# manifest, every refusal a form `guidance/editorial.md` names, and
# `proposal-fields` two. The 2026-09-24 audit repaired every one, so the
# published leaves now pass both; `ProseCheckTests` below records that, and
# holds each detection over the corpus as the audit found it.
PROSE_CHECKS = ("house-voice", "proposal-fields")
# This check is also tree-only and version-bound. It is named separately
# because it binds at two production entry points: `proper` v24 and
# `proper-finish` v2.
STRUCTURAL_CHECKS = ("structural-meta-labels",)
TREE_CHECKS = (LEAF_CHECKS + STRUCTURAL_CHECKS + CHRONOLOGY_CHECKS
               + PROSE_CHECKS)
PROBE_CHECKS = tuple(check for check in TREE_CHECKS
                     if check not in PROBE_ONLY_ABSENT)
CHECKS = (LEAF_CHECKS + STRUCTURAL_CHECKS + (RUN_CHECK,)
          + CHRONOLOGY_CHECKS + PROSE_CHECKS)
# The five names a gate command may substitute from the run itself, and the
# option each is handed to the tool as.
RUN_PLACEHOLDERS = {
    "{run.workflow_id}": "--run-workflow",
    "{run.workflow_version}": "--run-workflow-version",
    "{run.workflow_digest}": "--run-workflow-digest",
    "{run.run_id}": "--run-id",
    "{run.repo_commit}": "--run-seed-commit",
}
# A leaf the whole evaluation loop has already accepted and every check still
# passes, in the provider the rest of the workflow suite drives runs against.
# Found by suffix rather than written down, for the reason `DOC` gives: the
# corpus renumbers. It is NOT `DOC`, which is the ninth Sunday: that leaf
# carried two real `house-voice` loci -- "Their architecture is this guide's
# source-grounded synthesis" and "Complete English verses are shown so the
# project does not manufacture its own stitched translation" -- until the
# 2026-09-24 audit repaired them (e8217e665), and a test may not rewrite a
# published leaf to get a check past it.
PROVIDER_ROOT = ROOT / "src" / "gpt"


def _leaf_every_check_passes() -> str:
    """The thirteenth Sunday, found the way `DOC` finds the ninth."""
    for manifest in sorted(PROVIDER_ROOT.glob(
            "liturgy/roman-rite/1962/propers/*/*/proper-components.toml")):
        if manifest.parent.name.endswith("-thirteenth-after-pentecost"):
            return manifest.parent.relative_to(PROVIDER_ROOT).as_posix()
    raise AssertionError("no thirteenth-after-pentecost leaf under src/gpt")


PUBLISHED = ("gpt", _leaf_every_check_passes())


def stage() -> dict:
    return {s["id"]: s for s in workflow_json()["stages"]}[STAGE]


def check_commands() -> dict[str, str]:
    return {check["id"]: check["command"] for check in stage()["checks"]}


class TopologyTests(unittest.TestCase):
    """Where the gate sits, and where a failure of it may go."""

    def test_the_gate_sits_between_the_author_and_the_evaluation(self):
        """Where this gate stands, and nothing about the other stages.

        The whole stage list is asserted once, by
        `test_workflow_research_fanout.TopologyTests`, which owns
        `STAGE_ORDER`. It used to be asserted here as well, and a second copy
        of one rule is a second place to update: the list is a literal, so a
        stage added anywhere in the pipeline failed this file too and said
        nothing about content-preflight while doing it.
        """
        order = [s["id"] for s in workflow_json()["stages"]]
        self.assertEqual(order[order.index("author-proper") + 1], STAGE)
        self.assertEqual(order[order.index(STAGE) + 1], "content-evaluation")
        stages = {s["id"]: s for s in workflow_json()["stages"]}
        self.assertEqual(stages["author-proper"]["next"], STAGE)

    def test_it_is_a_program_gate_with_a_bounded_loop(self):
        declared = stage()
        self.assertEqual(declared["type"], "gate")
        self.assertEqual(declared["execution"], {"mode": PROGRAM})
        self.assertEqual(declared["pass_transition"], "content-evaluation")
        self.assertEqual(declared["fail_transition"], "content-revision")
        self.assertEqual(declared["max_iterations"], 3)
        self.assertNotIn("fragments", declared,
                         "a program gate asks no agent anything")
        self.assertNotIn("repair_routes", declared,
                         "a mechanical defect has one owner, so it needs no "
                         "classification")

    def test_a_preflight_failure_never_reaches_research(self):
        """The repair is in the leaf, so it is made in the leaf.

        Reachability, not just the declared transition: whatever
        `content-revision` does next must not be a research stage either, or
        the gate would be a slow road back to the seven lanes.
        """
        stages = {s["id"]: s for s in workflow_json()["stages"]}
        failure = stages[STAGE]["fail_transition"]
        self.assertEqual(failure, "content-revision")
        revision = stages[failure]
        self.assertEqual(revision["type"], "bounded-revision")
        self.assertEqual(revision["revision_target"], "author-proper")
        # The reviser re-enters the gate, not the evaluation behind it, so a
        # mechanical defect's repair is checked mechanically. Sending it
        # straight to `content-evaluation` would spend five AI lanes on a
        # document whose preflight failure may still stand.
        self.assertEqual(revision["next"], STAGE)
        for key in ("next", "pass_transition", "fail_transition"):
            self.assertNotEqual(revision.get(key), "research")
            self.assertNotEqual(revision.get(key), "research-synthesis")

    def test_the_gate_declares_every_check_the_tool_implements(self):
        """The tool is the authority on what checks there are.

        Written against `--list` rather than against a tuple here, because a
        check the tool implements and no gate runs is the defect the gate
        exists to catch: it reads exactly like a check that passes.
        """
        listed = subprocess.run(
            [str(ROOT / "tools" / TOOL), "--list"],
            capture_output=True, text=True, cwd=ROOT).stdout.split()
        self.assertEqual(sorted(listed), sorted(CHECKS),
                         "the tool's own listing and this suite disagree "
                         "about which checks exist")
        self.assertEqual(
            sorted(check_commands()), sorted(listed),
            "the content-preflight gate and the tool disagree about which "
            "checks run; a check the tool implements and the pipeline does "
            "not declare never runs at all")

    def test_every_check_is_one_command_over_the_run_s_own_arguments(self):
        commands = check_commands()

        self.assertEqual(list(commands), list(CHECKS),
                         "the checks the design names, in order")
        registry = json.loads(
            (ROOT / "tmt.json").read_text(encoding="utf-8"))["tools"]
        for check_id, command in commands.items():
            with self.subTest(check=check_id):
                self.assertIn(f"tools/tpt {TOOL} ", command)
                self.assertIn(TOOL, registry,
                              "a gate may only run a registered tool")
                self.assertIn(f"--check {check_id}", command)
                residue = command.replace("{proper}", "").replace(
                    "{provider}", "")
                for placeholder in RUN_PLACEHOLDERS:
                    residue = residue.replace(placeholder, "")
                self.assertNotRegex(
                    residue, r"\{[A-Za-z_][A-Za-z0-9_.]*\}",
                    "the gate takes a name the run supplies nothing for")
                for shell in ("&&", "||", ";", "|"):
                    self.assertNotIn(
                        shell, command,
                        "each check is one command, judged by its own exit "
                        "code")

    PAYLOADS = (
        "x`touch /tmp/triptych-preflight-escape`",
        "x$(touch /tmp/triptych-preflight-escape)",
        "x; touch /tmp/triptych-preflight-escape",
        "x' ; touch /tmp/triptych-preflight-escape ; '",
    )

    def test_a_hostile_identity_survives_as_data(self):
        """The property fab7db40b established, held for the new checks too.

        A template that wraps its own placeholder in quotes cancels the
        shell-quoting `_substitute_args` applies, and the rest of the id is
        read as shell. The suite asserts this over every gate; it is asserted
        here as well because these commands are the newest place it could be
        got wrong.
        """
        for check_id, command in check_commands().items():
            for payload in self.PAYLOADS:
                with self.subTest(check=check_id, payload=payload):
                    rendered = _substitute_args(
                        command, {"proper": payload, "provider": "claude"},
                        quote=True)
                    tokens = shlex.split(rendered)
                    self.assertTrue(
                        any(payload in token for token in tokens),
                        "the id did not survive substitution as inert data")
                    self.assertNotIn("touch", tokens,
                                     "part of the id became a shell word")

    def test_a_hostile_run_identity_survives_as_data_too(self):
        """The run's own facts are quoted for the same reason a document is.

        They are engine-generated -- two hashes, a workflow id, an integer and
        a commit sha -- and nothing here relies on that. A value's provenance
        is not a security property, and the day one of these is computed from
        something a worker wrote is not the day to discover the difference.
        """
        for check_id, command in check_commands().items():
            for placeholder in RUN_PLACEHOLDERS:
                if placeholder not in command:
                    continue
                for payload in self.PAYLOADS:
                    with self.subTest(check=check_id, name=placeholder,
                                      payload=payload):
                        rendered = _substitute_args(
                            command,
                            {"proper": DOC, "provider": "claude",
                             placeholder.strip("{}"): payload},
                            quote=True)
                        tokens = shlex.split(rendered)
                        self.assertIn(
                            payload, tokens,
                            "the run fact did not survive as inert data")
                        self.assertNotIn(
                            "touch", tokens,
                            "part of the run fact became a shell word")

    def test_a_hostile_argument_cannot_smuggle_a_run_placeholder(self):
        """A value is data, and data is never scanned for names.

        Substituting name after name over the growing result re-reads what
        the last substitution wrote, so a document id holding the text
        `{run.run_id}` would have the engine expand it: a supplied value
        deciding what a later name expands to, inside a template the workflow
        wrote. One pass is what forecloses it.
        """
        command = check_commands()[RUN_CHECK]
        smuggled = "x{run.run_id}y"
        rendered = _substitute_args(
            command,
            {"proper": smuggled, "provider": "claude",
             "run.run_id": "deadbeefdeadbeef",
             "run.workflow_id": "proper", "run.workflow_version": "16",
             "run.workflow_digest": "d" * 64, "run.repo_commit": "c" * 40},
            quote=True)
        tokens = shlex.split(rendered)
        self.assertIn(smuggled, tokens,
                      "the argument was rewritten by a later name")
        self.assertEqual(
            [token for token in tokens if token == "deadbeefdeadbeef"],
            ["deadbeefdeadbeef"],
            "the run id reached the command once, where the template asked "
            "for it")

    def test_the_run_check_names_the_run_and_never_an_argument(self):
        """Where the identity comes from, stated in the command itself.

        Text, and deliberately only text: what the engine actually puts in
        each of these places is executed in `RunIdentitySubstitutionTests` in
        test_workflow_engine.py, and the whole chain again in
        `DrivenRunTests` below.
        """
        command = check_commands()[RUN_CHECK]
        for placeholder, option in RUN_PLACEHOLDERS.items():
            with self.subTest(option=option):
                self.assertIn(f"{option} {placeholder}", command)
        self.assertNotIn("--run-install-commit", command,
                         "install_commit does not exist while the document "
                         "is being written")


class CheckBehaviourTests(unittest.TestCase):
    """Each check, over a leaf that satisfies it and one that does not.

    The passing case is a real published leaf every time. A check that only
    ever ran against a fixture would be free to be wrong about the corpus.
    """

    maxDiff = None

    def setUp(self):
        self.tree = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, self.tree, ignore_errors=True)
        self.leaf = self.tree / "src" / "claude" / "probe"
        self.leaf.mkdir(parents=True)
        library = self.tree / "src" / "sources" / "works" / "probe"
        library.mkdir(parents=True)
        (library / "work.toml").write_text(
            'id = "work.catholic-church.missale-romanum"\n', encoding="utf-8")
        self.write_library()
        self.write_leaf()
        self.write_manifest(['"introit"', '"collect"'])
        self.write_bindings()

    # One public-domain witness and one restricted one, each reached the way
    # a real binding reaches it: the public-domain artifact directly, the
    # restricted one through the passage record that names its artifact.
    PUBLIC_ARTIFACT = ("artifact.english-college-of-douay.douay-rheims-bible."
                       "challoner-1749.verse-text")
    RESTRICTED_PASSAGE = (
        "passage.united-states-conference-of-catholic-bishops."
        "new-american-bible-revised-edition.usccb-web-2026-08-21.galatians")
    RESTRICTED_ARTIFACT = (
        "artifact.united-states-conference-of-catholic-bishops."
        "new-american-bible-revised-edition.usccb-web-2026-08-21.galatians")

    def write_library(self):
        library = self.tree / "src" / "sources" / "works" / "probe"
        (library / "douay.toml").write_text(
            'record_type = "artifact"\n'
            f'id = "{self.PUBLIC_ARTIFACT}"\n'
            'storage = "tracked"\n'
            'rights_status = "public-domain"\n', encoding="utf-8")
        (library / "nabre-artifact.toml").write_text(
            'record_type = "artifact"\n'
            f'id = "{self.RESTRICTED_ARTIFACT}"\n'
            'storage = "restricted"\n'
            'rights_status = "restricted"\n', encoding="utf-8")
        (library / "nabre-passage.toml").write_text(
            'record_type = "passage"\n'
            f'id = "{self.RESTRICTED_PASSAGE}"\n'
            f'artifact_id = "{self.RESTRICTED_ARTIFACT}"\n', encoding="utf-8")

    def write_bindings(self, restricted_role="context"):
        research = self.leaf / "research"
        research.mkdir(exist_ok=True)
        (research / "source-bindings.toml").write_text(
            'schema = 1\nrecord_type = "bindings"\n\n'
            '[[bindings]]\n'
            f'source_id = "{self.PUBLIC_ARTIFACT}"\n'
            'role = "translation-control"\n\n'
            '[[bindings]]\n'
            f'source_id = "{self.RESTRICTED_PASSAGE}"\n'
            f'role = "{restricted_role}"\n', encoding="utf-8")

    GOOD_TRANSLATION = "English: Douay--Rheims (Challoner), Ps. 8:2"
    GOOD_ID = "work.catholic-church.missale-romanum"

    def write_leaf(self, translation=None, identifier=None, extra="", body=""):
        (self.leaf / "main.tex").write_text(f"""\\section*{{Commentary}}
Augustine, \\work{{Enarrationes in Psalmos}} 8, is read at the Introit.
Guéranger is summarised for the devotional reception only.
{body}
\\begin{{namedtranslation}}{{{translation or self.GOOD_TRANSLATION}}}
O Lord our Lord, how admirable is thy name.
\\end{{namedtranslation}}

\\section*{{References}}
\\begin{{itemize}}
\\item Augustine, \\work{{Enarrationes in Psalmos}} 8. Registered in the
repository's source library as \\texttt{{{identifier or self.GOOD_ID}}}.
\\item Prosper Guéranger, \\work{{The Liturgical Year}}, vol.~II.
\\textit{{Cited only as a witness to devotional reception; it supplies no
English printed in this guide.}}
{extra}\\end{{itemize}}
""", encoding="utf-8")

    def write_production(self, workflow="proper", version=24):
        (self.leaf / "generation-metadata.tex").write_text(
            f"\\AIGenerationProvenance{{{workflow}}}{{{version}}}"
            "{digest}{run}{commit}{unknown}\n",
            encoding="utf-8",
        )

    def write_manifest(self, relation_keys):
        (self.leaf / "proper-components.toml").write_text(f"""schema = 1
record_type = "proper-components"
element_keys = ["introit", "collect", "gospel"]

[[components]]
key = "source-grounded-synthesis"
kind = "source-grounded-synthesis"
path = "main.tex"
element_keys = ["introit", "collect"]

[[relations]]
key = "probe-relation"
element_keys = [{", ".join(relation_keys)}]
evidence = ["source-grounded-synthesis"]
""", encoding="utf-8")

    def probe(self, check):
        return subprocess.run(
            [str(ROOT / "tools" / TOOL), "--root", str(self.tree),
             "--provider", "claude", "--document", "probe", "--check", check],
            capture_output=True, text=True, cwd=ROOT)

    def published(self, check):
        provider, document = PUBLISHED
        return subprocess.run(
            [str(ROOT / "tools" / TOOL), "--provider", provider,
             "--document", document, "--check", check],
            capture_output=True, text=True, cwd=ROOT)

    def test_every_check_passes_on_a_published_leaf(self):
        for check in TREE_CHECKS:
            with self.subTest(check=check):
                result = self.published(check)
                self.assertEqual(
                    result.returncode, 0,
                    f"{check} refused src/{PUBLISHED[0]}/{PUBLISHED[1]}, a "
                    f"leaf the whole loop has accepted: {result.stderr}")
                self.assertTrue(result.stdout.startswith(f"{check}: "),
                                "a passing check says what it counted")

    def test_the_whole_preflight_over_every_leaf_with_a_manifest(self):
        """Not one leaf: every published one the manifest era produced.

        The record era's checks pass on all of them, which is the property
        this test has always held. The two prose checks are newer than the
        corpus and refuse some of it, so what is held about them here is
        narrower and exact: a refusal may come only from one of those two,
        and never from a check these leaves were written against.
        """
        leaves = [
            (provider, manifest.parent.relative_to(ROOT / "src" / provider).as_posix())
            for provider in ("claude", "gpt")
            for manifest in sorted(
                (ROOT / "src" / provider / "liturgy/roman-rite/1962/propers")
                .glob("*/*/proper-components.toml")
            )
        ]
        # One cold preflight per leaf, and no leaf's verdict depends on
        # another's, so the waiting is shared and the judging is not.
        results = gather(
            lambda leaf: subprocess.run(
                [str(ROOT / "tools" / TOOL), "--provider", leaf[0],
                 "--document", leaf[1]],
                capture_output=True, text=True, cwd=ROOT),
            leaves,
        )
        for (provider, document), result in zip(leaves, results):
            with self.subTest(leaf=f"{provider}/{document}"):
                older = [line for line in result.stderr.splitlines()
                         if line.startswith(ERROR)
                         and not any(line.startswith(f"{ERROR}{check}: ")
                                     for check in PROSE_CHECKS)]
                self.assertEqual(older, [], "\n".join(older))
                for check in TREE_CHECKS:
                    if check in PROSE_CHECKS:
                        continue
                    self.assertIn(f"{check}: ", result.stdout,
                                  f"{check} did not report on this leaf")
        self.assertGreater(len(leaves), 0, "no published leaf was checked")

    def test_the_probe_leaf_passes_before_anything_is_broken(self):
        # Probed once per check, not twice: the failure message used to re-run
        # the whole command to have something to print.
        probed = gather(self.probe, PROBE_CHECKS)
        for check, result in zip(PROBE_CHECKS, probed):
            with self.subTest(check=check):
                self.assertEqual(result.returncode, 0, result.stderr)

    def test_references_used_refuses_an_entry_the_body_never_names(self):
        self.write_leaf(extra=(
            "\\item Francis Blomefield, \\work{An Essay towards a "
            "Topographical History of the County of Norfolk}, vol.~4.\n"))
        result = self.probe("references-used")
        self.assertEqual(result.returncode, 1)
        self.assertIn("cited nowhere in the body", result.stderr)
        self.assertIn("Blomefield", result.stderr,
                      "the refusal names the entry it refused")
        for other in ("identifiers-resolve", "relation-coverage",
                      "unquoted-not-quoted"):
            with self.subTest(check=other):
                self.assertEqual(self.probe(other).returncode, 0,
                                 "one defect refused one check")

    # A guide's own prose names the Mass's parts and its calendar whatever it
    # cites. GPT 50 and 51's synthesis editions passed three entries they
    # never name on "Book", "Historical", "Postcommunion" and "Sunday".
    GENERIC_ENTRY = ("\\item H.~Q. Zebedee, \\work{The Historical Book of "
                     "the Sunday Postcommunion}, p.~3.\n")
    GENERIC_BODY = ("The Sunday Postcommunion closes the Mass, and the "
                    "Historical Book of the feast is not named.")

    def test_references_used_is_not_satisfied_by_generic_words(self):
        self.write_leaf(extra=self.GENERIC_ENTRY, body=self.GENERIC_BODY)
        result = self.probe("references-used")
        self.assertEqual(result.returncode, 1)
        self.assertIn("cited nowhere in the body", result.stderr)
        self.assertIn("Zebedee", result.stderr,
                      "the refusal names the entry it refused")

    def test_references_used_still_accepts_an_entry_named_in_the_body(self):
        self.write_leaf(extra=self.GENERIC_ENTRY,
                        body=self.GENERIC_BODY + " Zebedee dates it.")
        result = self.probe("references-used")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("3 entries, every one used in the body", result.stdout)

    # An entry made only of words the check treats as common used to be
    # skipped; four GPT leaves printed an Internet Archive entry their bodies
    # never name, and it passed.
    COMMON_ENTRY = ("\\item Internet Archive, \\sourceurl{https://archive.org/"
                    "details/probe}{1962 missal item} and OCR aid.\n")

    def test_references_used_refuses_an_entry_of_common_words_only(self):
        self.write_leaf(extra=self.COMMON_ENTRY)
        result = self.probe("references-used")
        self.assertEqual(result.returncode, 1)
        self.assertIn("cited nowhere in the body: Internet Archive",
                      result.stderr)

    def test_references_used_accepts_a_common_word_entry_the_body_names(self):
        self.write_leaf(extra=self.COMMON_ENTRY,
                        body="The Internet Archive scan located the page.")
        result = self.probe("references-used")
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_references_used_wants_every_word_of_a_common_word_entry(self):
        """One common word is not a name.

        GPT M01's gallery cites the National Archives, and its Internet
        Archive entry passed on "archive" alone.
        """
        self.write_leaf(extra=self.COMMON_ENTRY,
                        body="The National Archives hold the register.")
        result = self.probe("references-used")
        self.assertEqual(result.returncode, 1)
        self.assertIn("cited nowhere in the body: Internet Archive",
                      result.stderr)

    # --- restricted-not-reproduced --------------------------------------

    def test_restricted_refuses_a_restricted_translation_control(self):
        """The leaf declares the reproduction, in its own binding record.

        `translation-control` is the role that says the published English is
        this witness's words. Against an artifact registered `restricted` it
        is a contradiction between two files, and neither file shows it.
        """
        self.write_bindings(restricted_role="translation-control")
        result = self.probe("restricted-not-reproduced")
        self.assertEqual(result.returncode, 1)
        self.assertIn("bound as translation-control", result.stderr)
        self.assertIn("registered restricted", result.stderr)
        self.assertIn(self.RESTRICTED_PASSAGE, result.stderr,
                      "the refusal names the source it refused")

    def test_restricted_refuses_a_set_passage_credited_to_restricted_bytes(self):
        """The leaf prints it, whatever role the binding claims.

        The binding still says `context` — summarised, not reproduced — and
        the leaf prints a passage over the witness's name anyway. This is the
        shape the earlier production's rights violation actually had.
        """
        self.write_leaf(translation="New American Bible, Revised Edition, "
                                    "Gal. 5:16--24")
        result = self.probe("restricted-not-reproduced")
        self.assertEqual(result.returncode, 1)
        self.assertIn("a set passage is attributed to", result.stderr)
        self.assertIn("may not be reproduced", result.stderr)

    def test_restricted_reads_the_rights_through_the_passage_record(self):
        """The rights are on the artifact; the leaf never names the artifact.

        The binding names a passage, and only the passage's `artifact_id`
        reaches the record that carries `storage`. A check that stopped at the
        bound id would find no rights at all and pass everything.
        """
        library = self.tree / "src" / "sources" / "works" / "probe"
        (library / "nabre-artifact.toml").write_text(
            'record_type = "artifact"\n'
            f'id = "{self.RESTRICTED_ARTIFACT}"\n'
            'storage = "tracked"\n'
            'rights_status = "public-domain"\n', encoding="utf-8")
        self.write_bindings(restricted_role="translation-control")
        self.assertEqual(
            self.probe("restricted-not-reproduced").returncode, 0,
            "with the artifact unrestricted the same binding is lawful")

    def test_restricted_passes_a_public_domain_translation_control(self):
        """The Douay is bound as the translation control and printed. Fine."""
        result = self.probe("restricted-not-reproduced")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("2 bound sources, 1 of them restricted, none reproduced",
                      result.stdout)

    def test_restricted_ignores_a_word_two_bound_sources_share(self):
        """An attribution that cannot say which source it means says nothing.

        Both bound sources become "bible" here. A word that does not
        discriminate between the leaf's own bindings cannot be evidence that
        the restricted one was the one reproduced.
        """
        self.write_leaf(translation="Bible, Ps. 8:2")
        self.assertEqual(
            self.probe("restricted-not-reproduced").returncode, 0,
            "a shared word must not convict either source")

    def test_a_leaf_local_alias_of_a_printed_passage_is_still_read(self):
        """`format.tex` renames the environment; the passage is still printed.

        Six of the twenty published propers wrap `sourcecard` in a name of
        their own, `54-fourteenth-after-pentecost` — the leaf both production
        runs were producing — among them. A check matching only the base names
        saw zero printed passages in those six. It was not passing them; it
        was not reading them.
        """
        (self.leaf / "format.tex").write_text(
            "\\newenvironment{fulltextenglish}[1]"
            "{\\begin{sourcecard}{#1}\\small}{\\end{sourcecard}}\n",
            encoding="utf-8")
        (self.leaf / "main.tex").write_text(
            (self.leaf / "main.tex").read_text(encoding="utf-8")
            .replace("namedtranslation", "fulltextenglish")
            .replace(self.GOOD_TRANSLATION,
                     "New American Bible, Revised Edition, Gal. 5:16--24"),
            encoding="utf-8")
        result = self.probe("restricted-not-reproduced")
        self.assertEqual(result.returncode, 1,
                         "the alias must not hide the printed passage")
        self.assertIn("a set passage is attributed to", result.stderr)

    def test_identifiers_resolve_refuses_an_unregistered_identifier(self):
        self.write_leaf(identifier="edition.no-such-house.no-such-book.1861")
        result = self.probe("identifiers-resolve")
        self.assertEqual(result.returncode, 1)
        self.assertIn("registered nowhere in src/sources", result.stderr)
        self.assertIn("edition.no-such-house.no-such-book.1861",
                      result.stderr)
        self.assertEqual(self.probe("references-used").returncode, 0)

    def test_an_identifier_broken_for_the_typesetter_is_still_one_id(self):
        """`\\allowbreak` and a line end split the id, not the source.

        A line-at-a-time reader sees `edition.eugene-cummiskey` and calls a
        registered source unregistered. Four published leaves print an id
        this way.
        """
        self.write_leaf(
            identifier="work.catholic-church.\\allowbreak\nmissale-romanum")
        result = self.probe("identifiers-resolve")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("1 source identifiers", result.stdout)

    def test_relation_coverage_refuses_an_element_the_unit_does_not_claim(self):
        self.write_manifest(['"introit"', '"collect"', '"gospel"'])
        result = self.probe("relation-coverage")
        self.assertEqual(result.returncode, 1)
        self.assertIn("probe-relation", result.stderr)
        self.assertIn("'gospel'", result.stderr,
                      "the refusal names the element that is unclaimed")
        self.assertEqual(self.probe("unquoted-not-quoted").returncode, 0)

    def test_unquoted_not_quoted_refuses_a_contradicted_attribution(self):
        self.write_leaf(translation=(
            "English: Guéranger, \\work{The Liturgical Year}, p.~224"))
        result = self.probe("unquoted-not-quoted")
        self.assertEqual(result.returncode, 1)
        self.assertIn("References declare unquoted", result.stderr)
        self.assertIn("gueranger", result.stderr)
        self.assertEqual(self.probe("references-used").returncode, 0)

    # --- A numbered References heading ------------------------------------

    def number_the_headings(self):
        """Every `\\section*` made `\\section`, as claude/48 prints them."""
        main = self.leaf / "main.tex"
        main.write_text(main.read_text(encoding="utf-8")
                        .replace("\\section*{", "\\section{"),
                        encoding="utf-8")

    def test_a_numbered_references_heading_is_read(self):
        """claude/48 numbers every section, `\\section{References}` among them.

        A starred-only pattern read that leaf as printing no References at
        all and refused it twice, once in each check that reads the section,
        although all twenty-three of its entries are used and none is declared
        unquoted.
        """
        self.number_the_headings()
        result = self.probe("references-used")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("2 entries, every one used in the body", result.stdout)
        result = self.probe("unquoted-not-quoted")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("1 sources declared unquoted", result.stdout)

    def test_an_unused_entry_under_a_numbered_heading_is_still_refused(self):
        """Reading the heading must not stop the check from judging entries."""
        self.write_leaf(extra=(
            "\\item Francis Blomefield, \\work{An Essay towards a "
            "Topographical History of the County of Norfolk}, vol.~4.\n"))
        self.number_the_headings()
        result = self.probe("references-used")
        self.assertEqual(result.returncode, 1)
        self.assertIn("cited nowhere in the body", result.stderr)
        self.assertIn("Blomefield", result.stderr,
                      "the refusal names the entry it refused")
        self.assertNotIn("prints no References section", result.stderr)

    def test_a_contradicted_attribution_under_a_numbered_heading(self):
        self.write_leaf(translation=(
            "English: Guéranger, \\work{The Liturgical Year}, p.~224"))
        self.number_the_headings()
        result = self.probe("unquoted-not-quoted")
        self.assertEqual(result.returncode, 1)
        self.assertIn("References declare unquoted", result.stderr)
        self.assertIn("gueranger", result.stderr)

    def test_proposals_under_a_numbered_heading_are_read(self):
        """The same leaf numbers `The Propers: Interpretive Possibilities`.

        A starred-only pattern reported its proposals out of scope, as though
        the leaf declared none, so a missing field went unread.
        """
        (self.leaf / "main.tex").write_text(
            (self.leaf / "main.tex").read_text(encoding="utf-8")
            + "\n\\section{The Propers: Interpretive Possibilities}\n"
            "Everything below is exploratory editorial and AI proposal.\n\n"
            "\\begin{proposal}{The Introit and the Collect}\n"
            "\\pfield{Anchors}{Introit and Collect.}\n"
            "\\pfield{Mechanism}{One address, made twice.}\n"
            "\\pfield{Fruit}{The day's prayer is read as a single act.}\n"
            "\\pfield{Strongest limit}{The Collect is older.}\n"
            "\\end{proposal}\n",
            encoding="utf-8")
        result = self.probe("proposal-fields")
        self.assertEqual(result.returncode, 1, result.stdout)
        self.assertIn("what the ordinary element-by-element reading misses",
                      result.stderr)

    # --- relation-coverage and the leaves that predate the manifest -------

    def test_a_leaf_that_predates_the_manifest_is_out_of_scope(self):
        """Legacy, not defective, and said outright rather than passed.

        Both proper profiles hold that leaves authored before the component
        architecture remain valid until their next substantive revision.
        Every published leaf with no manifest states `unknown` for the
        production that made it; the probe is tried that way and with no
        record at all.
        """
        (self.leaf / "proper-components.toml").unlink()
        for stated in (None, ("unknown", "unknown")):
            with self.subTest(stated=stated):
                if stated:
                    self.write_production(*stated)
                result = self.probe("relation-coverage")
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertTrue(result.stdout.startswith(
                    "relation-coverage: not in scope: the leaf states no "
                    "recognized provenance record and carries no "
                    "proper-components.toml, so it predates the component "
                    "manifest"), result.stdout)

    def test_a_missing_manifest_is_a_refusal_when_the_production_writes_one(
            self):
        """Not a vacuous pass: every production workflow writes a manifest.

        A run that forgot to write one states its own workflow and version,
        and `provenance-matches-run` holds that statement to the run.
        """
        (self.leaf / "proper-components.toml").unlink()
        for workflow in ("proper", "proper-finish", "proper-study"):
            with self.subTest(workflow=workflow):
                self.write_production(workflow, 1)
                result = self.probe("relation-coverage")
                self.assertEqual(result.returncode, 1, result.stdout)
                self.assertIn("carries no proper-components.toml",
                              result.stderr)

    def test_a_coverage_gap_is_refused_whatever_the_leaf_states(self):
        """The legacy exemption is for a leaf with no manifest, and no other.

        A leaf that carries a manifest is checked exactly as before, even when
        it states no production -- as every schema-1 leaf of the first
        production era does.
        """
        self.write_manifest(['"introit"', '"collect"', '"gospel"'])
        for stated in (None, ("unknown", "unknown"), ("proper", 24)):
            with self.subTest(stated=stated):
                if stated:
                    self.write_production(*stated)
                result = self.probe("relation-coverage")
                self.assertEqual(result.returncode, 1, result.stdout)
                self.assertIn("probe-relation", result.stderr)
                self.assertIn("'gospel'", result.stderr)

    def test_current_proper_shape_is_refused_as_a_box_title(self):
        """The Proper 55 regression shape, copied into a synthetic leaf."""
        self.write_production()
        (self.leaf / "main.tex").write_text(
            "\\sectionguard\n"
            "\\section*{The Propers: Themes and Movement}\n"
            "\\begin{studybox}{Governing thesis}\n"
            "The Introit gathers exile into the Church's petition.\n"
            "\\end{studybox}\n",
            encoding="utf-8",
        )
        result = self.probe("structural-meta-labels")
        self.assertEqual(result.returncode, 1)
        self.assertIn("'governing thesis'", result.stderr)
        self.assertIn("studybox box title", result.stderr)

    def test_a_direct_unlabelled_thesis_is_accepted(self):
        self.write_production()
        (self.leaf / "main.tex").write_text(
            "\\section*{The Propers: Themes and Movement}\n"
            "The Introit gathers exile into the Church's petition, and the "
            "Gospel answers it with restored life.\n\n"
            "Augustine's thesis about pilgrimage supplies the next step; "
            "the phrase argument map occurs here as ordinary prose.\n",
            encoding="utf-8",
        )
        result = self.probe("structural-meta-labels")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("with no forbidden structural meta-label", result.stdout)

    def test_each_narrow_structural_surface_is_refused(self):
        self.write_production()
        fixtures = {
            "heading": "\\subsection*{Thesis}\nThe Introit opens.\n",
            "run-in": "\\textbf{Key takeaway.} The Introit opens.\n",
            "plain run-in": "Reading order: Introit, Collect, Gospel.\n",
            "table heading": (
                "\\begin{longtable}{ll}\n\\toprule\n"
                "\\textbf{Argument map} & \\textbf{Evidence}\\\\\n"
                "\\midrule\nIntroit & Psalm\\\\\n\\end{longtable}\n"
            ),
            "plain table heading": (
                "\\begin{tabular}{ll}\n"
                "Reading order & Evidence\\\\\n"
                "Introit & Psalm\\\\\n\\end{tabular}\n"
            ),
            "house table heading": (
                "\\begin{threestable}{Proper}{Reading order}{Evidence}\n"
                "Introit & first & Psalm\\\\\n\\end{threestable}\n"
            ),
        }
        for surface, source in fixtures.items():
            with self.subTest(surface=surface):
                (self.leaf / "main.tex").write_text(source, encoding="utf-8")
                result = self.probe("structural-meta-labels")
                self.assertEqual(result.returncode, 1, result.stderr)
                self.assertIn("forbidden reader-facing structural meta-label",
                              result.stderr)

    def test_the_structural_contract_binds_at_both_entry_points(self):
        (self.leaf / "main.tex").write_text(
            "\\section*{Thesis}\nThe Introit opens.\n", encoding="utf-8"
        )
        for workflow, version, expected in (
                ("proper", 23, 0), ("proper", 24, 1),
                ("proper-finish", 1, 0), ("proper-finish", 2, 1)):
            with self.subTest(workflow=workflow, version=version):
                self.write_production(workflow, version)
                self.assertEqual(
                    self.probe("structural-meta-labels").returncode, expected
                )

    def test_malformed_structural_tex_fails_closed_when_bound(self):
        self.write_production()
        (self.leaf / "main.tex").write_text(
            "\\begin{studybox}{Governing thesis\nThe Introit opens.\n",
            encoding="utf-8",
        )
        result = self.probe("structural-meta-labels")
        self.assertEqual(result.returncode, 1)
        self.assertIn("could not parse a structural surface", result.stderr)


class ProseCheckTests(unittest.TestCase):
    """The two checks over reader-facing prose, against the real corpus.

    What each rule sees and what it deliberately refuses to see is held in
    tools/tests/test_house_voice.py, string by string, against the loci an
    evaluation lane actually reported and the prose the same lanes read and
    left standing. What is held here is the tool: which published leaves it
    refuses, which it passes, and what it says when it cannot read a leaf at
    all.

    Its refusals are held over the corpus as the 2026-09-24 house-voice audit
    found it, at `AUDITED_COMMIT` (see tools/tests/_audited_corpus.py). The
    specimens were live leaves until that audit repaired them: pinned to the
    tree, the refusal tests failed on the repair, and the quotation test,
    looping over refusals that no longer came, passed while checking nothing.
    """

    # Two leaves of the audited tree. Pins to live leaves moved as the corpus
    # was repaired -- claude/54 carried both habits first -- and on 2026-09-24
    # there was no live leaf left to move them to.
    SPECIMEN = ("claude", "liturgy/roman-rite/1962/propers/temporal/"
                          "51-eleventh-after-pentecost")
    PROPOSAL_SPECIMEN = ("gpt", "liturgy/roman-rite/1962/propers/temporal/"
                                "52-twelfth-after-pentecost")
    # A leaf of the audited tree that both refuses and has a section the
    # house-voice screen cannot read. gpt/54 was this until its voice was
    # repaired; the audit repaired gpt/49 (e8217e665).
    UNSCREENED_SPECIMEN = ("gpt", "liturgy/roman-rite/1962/propers/temporal/"
                                  "49-ninth-after-pentecost")

    @classmethod
    def setUpClass(cls):
        cls.audited = audited_tree(cls)

    def run_check(self, provider, document, check, root=None):
        return subprocess.run(
            [str(ROOT / "tools" / TOOL),
             *(["--root", str(root)] if root is not None else []),
             "--provider", provider, "--document", document,
             "--check", check],
            capture_output=True, text=True, cwd=ROOT)

    def leaves(self, root=ROOT):
        for provider in ("claude", "gpt"):
            base = root / "src" / provider / "liturgy/roman-rite/1962/propers"
            for manifest in sorted(base.glob("*/*/proper-components.toml")):
                yield provider, manifest.parent.relative_to(
                    root / "src" / provider).as_posix()

    def test_house_voice_passes_a_leaf_that_keeps_the_voice(self):
        provider, document = PUBLISHED
        result = self.run_check(provider, document, "house-voice")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("no sentence taking the guide", result.stdout)

    def test_neither_prose_check_refuses_a_published_leaf(self):
        """Which published leaves carry either habit: none, since 2026-09-24.

        The house-voice count fell as leaves were repaired -- eight over
        claude/54, gpt/54 and the specimen of the day, then six -- and the
        2026-09-24 audit repaired the last six, and gpt/52's five proposals
        that stated no "what the element-by-element reading misses" field
        (e11d8b618). The list is held empty rather than dropped, so a leaf that
        takes either habit up again is a failure here and not a new count.
        """
        leaves = list(self.leaves())
        self.assertTrue(leaves, "found no published leaf: checked nothing")
        jobs = [(provider, document, check) for check in PROSE_CHECKS
                for provider, document in leaves]
        results = gather(lambda job: self.run_check(*job), jobs)
        refused = {check: [] for check in PROSE_CHECKS}
        for (provider, document, check), result in zip(jobs, results):
            if result.returncode:
                refused[check].append(
                    f"{provider}/{document.rsplit('/', 1)[-1]}")
        self.assertEqual(refused, {check: [] for check in PROSE_CHECKS})

    def test_house_voice_refuses_the_corpus_it_was_written_against(self):
        """Which leaves carried it when the audit began, recorded.

        A check written from one leaf's defects could be measuring that leaf.
        Five of the six leaves refused here are not the specimen and two are
        in the other provider, and every refusal is a form the guidance names,
        so the habit was the corpus's and not the specimen's. Measured over
        the published tree until the 2026-09-24 audit repaired all six; over
        the audited tree now, so that the finding stays a test rather than a
        claim in a docstring.
        """
        refused = sorted(
            f"{provider}/{document.rsplit('/', 1)[-1]}"
            for provider, document in self.leaves(self.audited)
            if self.run_check(provider, document, "house-voice",
                              self.audited).returncode)
        self.assertEqual(len(refused), 6, refused)
        self.assertIn("claude/52-twelfth-after-pentecost", refused)
        self.assertEqual(
            [one for one in refused if one.startswith("gpt/")],
            ["gpt/49-ninth-after-pentecost",
             "gpt/51-eleventh-after-pentecost"])

    def test_house_voice_names_the_file_and_the_line_and_the_repair(self):
        """The refusal a reviser is handed, over a leaf that carries it."""
        result = self.run_check(*self.SPECIMEN, "house-voice", self.audited)
        self.assertEqual(result.returncode, 1)
        lines = [line for line in result.stderr.splitlines()
                 if line.startswith(f"{ERROR}house-voice: ")
                 and "not screened:" not in line]
        self.assertEqual(len(lines), 20)
        self.assertTrue(
            any("sections/05-appointed-text.tex:37" in line
                and "the guide's own apparatus is the subject" in line
                for line in lines),
            "the refusal locates the sentence in the file and on the line")
        for line in lines:
            self.assertIn("delete nothing it was about", line,
                          "a refusal a worker acts on says what the repair "
                          "is, or the worker deletes the clause")
            self.assertNotIn("which already carries it", line,
                             "the screen never opens the appendix and cannot "
                             "say what is in it")

    def test_house_voice_quotes_a_string_that_is_in_the_file(self):
        """A refusal a worker cannot search for is a refusal it guesses at.

        The quotation used to be cut out of the masked text at fifty
        characters either side of the match, so it began and ended mid-word
        and carried spaces where the markup had been.
        """
        result = self.run_check(*self.SPECIMEN, "house-voice", self.audited)
        leaf = self.audited / "src" / self.SPECIMEN[0] / self.SPECIMEN[1]
        quoted = 0
        for line in result.stderr.splitlines():
            if (not line.startswith(f"{ERROR}house-voice: ")
                    or "not screened:" in line):
                continue
            body = line.split(f"{ERROR}house-voice: ", 1)[1]
            where = body.split(":", 1)[0]
            quotation = body.split(': "', 1)[1].rsplit(
                '". Rewrite the sentence', 1)[0]
            source = " ".join(
                (leaf / where).read_text(encoding="utf-8").split())
            with self.subTest(locus=where):
                self.assertIn(quotation, source)
            quoted += 1
        self.assertEqual(quoted, 20, "a loop over no refusals checks nothing")

    def test_house_voice_says_which_sections_it_could_not_read(self):
        """Six of the twelve leaves drop the field markup entirely.

        Nothing else marks where the protected exploratory notice ends and
        the proposals begin, so the section is cut whole and no rule runs over
        it. Reported rather than passed over in silence, or dropping the
        markup would take half a leaf's discovery prose out of the reach of
        this check and of `proposal-fields` at once.
        """
        provider, document = PUBLISHED
        result = self.run_check(provider, document, "house-voice")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("not screened", result.stdout)
        self.assertIn("The Propers: Interpretive Possibilities",
                      result.stdout)
        self.assertIn("marks no \\pfield", result.stdout)

    def test_house_voice_says_it_on_a_leaf_it_is_refusing_too(self):
        """A summary is printed on a pass, and never on a refusal.

        Leaves with an unread section are among the leaves this check
        refuses, so a scope statement carried only by the summary would be
        invisible on exactly the leaves a reviser is reading. It is added to a
        refusal that already exists and never makes one.

        Pinned to gpt/54 until that leaf's voice was repaired and it stopped
        refusing at all, then to gpt/49, which did both until the 2026-09-24
        audit repaired it; held over gpt/49 as the audit found it.
        """
        result = self.run_check(*self.UNSCREENED_SPECIMEN, "house-voice",
                                self.audited)
        self.assertEqual(result.returncode, 1)
        self.assertIn("not screened", result.stderr)
        self.assertIn("still has to be read by hand", result.stderr)

    def test_proposal_fields_reads_a_proposal_whose_title_has_a_macro(self):
        """What a check cannot read it must not report as read.

        The title group was `[^{}]*`, so a proposal titled `The Gospel's last
        clause and the Secret's \\latin{quóties} share one grammar` was not
        seen at all: a leaf carrying five proposals was reported as "4
        exploratory proposals, every one stating the five required parts".
        """
        for document in ("liturgy/roman-rite/1962/propers/temporal/"
                         "49-ninth-after-pentecost",
                         "liturgy/roman-rite/1962/propers/temporal/"
                         "53-thirteenth-after-pentecost"):
            with self.subTest(document=document):
                result = self.run_check("claude", document,
                                        "proposal-fields")
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertIn("5 exploratory proposals", result.stdout)

    def test_proposal_fields_catches_the_field_no_lane_owned(self):
        """Five proposals of one leaf, and no lane owned the field.

        The claude/54 proposal this was pinned to -- one of six, missing the
        field four sweeps had read past -- has been repaired. The habit had
        not been: the last leaf in the corpus still carrying it dropped the
        same field from every proposal it stated, which is the same finding at
        a different scale. The 2026-09-24 audit wrote that field into all five
        (e11d8b618), so the leaf is held as the audit found it.
        """
        result = self.run_check(*self.PROPOSAL_SPECIMEN, "proposal-fields",
                                self.audited)
        self.assertEqual(result.returncode, 1)
        self.assertIn("Ministry begins where the traveller leaves",
                      result.stderr)
        self.assertIn("what the ordinary element-by-element reading misses",
                      result.stderr)
        self.assertEqual(
            len([line for line in result.stderr.splitlines()
                 if line.startswith(ERROR)]), 5,
            "every proposal the leaf states drops the same field")

    def test_proposal_fields_reads_the_field_by_role_not_by_string(self):
        """Three headings for one field across the published leaves.

        `What the ordinary reading misses`, `What the ordinary
        element-by-element reading misses` and `What the element-by-element
        reading misses` are all the profile's fourth field, and `Strongest
        limit`, `Controlling limit` and `Limit` are all its fifth. A check
        matching strings would refuse most of the corpus.
        """
        passed = [f"{provider}/{document.rsplit('/', 1)[-1]}"
                  for provider, document in self.leaves()
                  if not self.run_check(
                      provider, document, "proposal-fields").returncode]
        for leaf in ("claude/49-ninth-after-pentecost",
                     "claude/51-eleventh-after-pentecost",
                     "claude/52-twelfth-after-pentecost",
                     "claude/53-thirteenth-after-pentecost"):
            self.assertIn(leaf, passed)

    def test_proposal_fields_says_when_it_cannot_read_the_fields(self):
        """Out of scope, said outright, rather than passed in silence.

        Five published leaves write their proposals as running prose with no
        field markup, and the profile does not require the markup. What a
        check cannot read it must not report as read.
        """
        provider, document = PUBLISHED
        result = self.run_check(provider, document, "proposal-fields")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("not in scope", result.stdout)
        self.assertIn("marks no proposal", result.stdout)


class LegacyLeafTests(unittest.TestCase):
    """The published leaves that predate the manifest, or number their headings.

    Each rule is held over the synthetic probe in `CheckBehaviourTests`; what
    is held here is that the corpus leaves those rules were written for are
    read, and not refused for their age or their heading style.
    """

    NUMBERED = ("claude", "liturgy/roman-rite/1962/propers/temporal/"
                          "48-eighth-after-pentecost")

    def run_check(self, provider, document, check):
        return subprocess.run(
            [str(ROOT / "tools" / TOOL), "--provider", provider,
             "--document", document, "--check", check],
            capture_output=True, text=True, cwd=ROOT)

    @unittest.skipUnless(
        (ROOT / "src" / NUMBERED[0] / NUMBERED[1]).is_dir(),
        "the numbered-heading leaf is not in the tree")
    def test_the_numbered_leaf_s_references_and_proposals_are_read(self):
        checks = ("references-used", "unquoted-not-quoted", "proposal-fields")
        for check, result in zip(checks, gather(
                lambda check: self.run_check(*self.NUMBERED, check), checks)):
            with self.subTest(check=check):
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertNotIn("not in scope", result.stdout)

    def test_every_leaf_without_a_manifest_is_out_of_scope(self):
        """Every proper leaf of both providers and both calendar families.

        Every one of them states no recognized production, so each is legacy
        under its profile. A leaf that stated a production and carried no
        manifest would be refused here, and would be a real defect.
        """
        leaves = [
            (provider, leaf.relative_to(ROOT / "src" / provider).as_posix())
            for provider in ("claude", "gpt")
            for main in sorted((ROOT / "src" / provider / "liturgy").glob(
                "roman-rite/**/propers/*/*/main.tex"))
            for leaf in (main.parent,)
            if not (leaf / "proper-components.toml").is_file()
        ]
        results = gather(
            lambda leaf: self.run_check(*leaf, "relation-coverage"), leaves)
        for (provider, document), result in zip(leaves, results):
            with self.subTest(leaf=f"{provider}/{document}"):
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertIn("relation-coverage: not in scope: ",
                              result.stdout)


class ProvenanceCheckTests(unittest.TestCase):
    """The leaf's record of what produced it, held against the run.

    Every test here runs the tool. The record is the only place a document
    states which workflow, at which version and digest, under which run and
    from which seed commit it was written, and until this check nothing read
    it: the instruction to copy those five facts off the packet header was
    obeyed or ignored to exactly the same effect. One leaf that already had a
    record stated `v10` through a v11 pass, because the value was copied out
    of the prose of an earlier `\\AIModelContribution` rather than off the
    header -- which is the case `a_stale_version` is.
    """

    RUN = {
        "--run-workflow": "proper",
        "--run-workflow-version": "16",
        "--run-workflow-digest": "a" * 64,
        "--run-id": "0123456789abcdef",
        "--run-seed-commit": "b" * 40,
    }

    def setUp(self):
        self.tree = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, self.tree, ignore_errors=True)
        self.leaf = self.tree / "src" / "claude" / "probe"
        self.leaf.mkdir(parents=True)
        self.write_record()

    def write_record(self, workflow="proper", version="16", digest="a" * 64,
                     run_id="0123456789abcdef", seed="b" * 40,
                     install="unknown", body=None):
        record = (
            f"\\AIGenerationProvenance{{{workflow}}}{{{version}}}"
            f"{{{digest}}}{{{run_id}}}{{{seed}}}{{{install}}}"
        ) if body is None else body
        (self.leaf / "generation-metadata.tex").write_text(
            "\\AIDocumentRevisionTimestamp{2026-09-01T00:00:00Z}\n"
            f"{record}\n"
            "\\AIModelContribution{a-model}{unexposed}{an agent}\n",
            encoding="utf-8")

    def check(self, **overrides):
        run = dict(self.RUN)
        for option, value in overrides.items():
            if value is None:
                run.pop(option, None)
            else:
                run[option] = value
        argv = [str(ROOT / "tools" / TOOL), "--root", str(self.tree),
                "--provider", "claude", "--document", "probe",
                "--check", RUN_CHECK]
        for option, value in run.items():
            argv += [option, value]
        return subprocess.run(argv, capture_output=True, text=True, cwd=ROOT)

    def test_a_record_of_this_run_passes(self):
        result = self.check()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertTrue(result.stdout.startswith(f"{RUN_CHECK}: "))
        self.assertIn(self.RUN["--run-id"], result.stdout,
                      "a passing check says which run it read")

    def test_a_stale_version_is_refused(self):
        """The defect this check was written for, exactly as it happened."""
        self.write_record(version="10")
        result = self.check()
        self.assertEqual(result.returncode, 1)
        self.assertIn("workflow_version '10'", result.stderr,
                      "the refusal names what the leaf states")
        self.assertIn("workflow_version '16'", result.stderr,
                      "and what the run producing it states")

    def test_a_stale_run_id_is_refused(self):
        self.write_record(run_id="feedfacefeedface")
        result = self.check()
        self.assertEqual(result.returncode, 1)
        self.assertIn("run_id 'feedfacefeedface'", result.stderr)
        self.assertIn(f"run_id '{self.RUN['--run-id']}'", result.stderr)

    def test_a_stale_digest_or_seed_commit_is_refused(self):
        for option, kwargs, stated in (
                ("--run-workflow-digest", {"digest": "c" * 64}, "c" * 64),
                ("--run-seed-commit", {"seed": "d" * 40}, "d" * 40),
                ("--run-workflow", {"workflow": "not-this-workflow"},
                 "not-this-workflow")):
            with self.subTest(field=option):
                self.write_record(**kwargs)
                result = self.check()
                self.assertEqual(result.returncode, 1)
                self.assertIn(stated, result.stderr)

    def test_a_leaf_with_no_record_at_all_is_refused(self):
        self.write_record(body="")
        result = self.check()
        self.assertEqual(result.returncode, 1)
        self.assertIn("carries no", result.stderr)
        self.assertIn("AIGenerationProvenance", result.stderr)

    def test_a_commented_out_record_states_nothing(self):
        """A record behind a `%` is not a record, and never a pass."""
        self.write_record(body=(
            "% \\AIGenerationProvenance{proper}{16}{" + "a" * 64
            + "}{0123456789abcdef}{" + "b" * 40 + "}{unknown}"))
        result = self.check()
        self.assertEqual(result.returncode, 1)
        self.assertIn("AIGenerationProvenance", result.stderr)

    def test_a_leaf_with_no_generation_metadata_is_refused(self):
        (self.leaf / "generation-metadata.tex").unlink()
        result = self.check()
        self.assertEqual(result.returncode, 1)
        self.assertIn("no generation-metadata.tex", result.stderr)

    def test_an_unknown_field_is_a_mismatch_like_any_other(self):
        """`unknown` is a record of a fact nobody could read.

        Every one of these five is on the packet header the stage was handed,
        so none of them is unreadable, and a leaf that says otherwise about
        the run producing it is refused exactly as a wrong value is.
        """
        self.write_record(digest="unknown")
        result = self.check()
        self.assertEqual(result.returncode, 1)
        self.assertIn("workflow_digest 'unknown'", result.stderr)

    def test_install_commit_is_not_compared(self):
        """It states where the artifact entered the tree; it has not yet."""
        for install in ("unknown", "e" * 40):
            with self.subTest(install_commit=install):
                self.write_record(install=install)
                self.assertEqual(self.check().returncode, 0)

    def test_two_records_are_refused(self):
        record = ("\\AIGenerationProvenance{proper}{16}{" + "a" * 64
                  + "}{0123456789abcdef}{" + "b" * 40 + "}{unknown}")
        self.write_record(body=f"{record}\n{record}")
        result = self.check()
        self.assertEqual(result.returncode, 1)
        self.assertIn("2 ", result.stderr)

    def test_the_check_is_refused_rather_than_skipped_without_a_run(self):
        """A check passing for want of an answer is worth less than none."""
        result = self.check(**{option: None for option in self.RUN})
        self.assertEqual(result.returncode, 1)
        for option in self.RUN:
            self.assertIn(option, result.stderr,
                          "the refusal names what it needs")

    def test_a_partial_identity_is_refused_rather_than_partly_checked(self):
        for option in self.RUN:
            with self.subTest(missing=option):
                result = self.check(**{option: None})
                self.assertEqual(result.returncode, 1)
                self.assertIn(option, result.stderr)

    def test_the_sweep_over_a_published_leaf_neither_runs_nor_passes_it(self):
        """A published leaf's record names the run that wrote it, not this one.

        So the whole-preflight invocation cannot include this check, and the
        thing to prove is that it is left out rather than answered: the
        listing names it, and the sweep does not report it as passing.
        """
        provider, document = PUBLISHED
        sweep = subprocess.run(
            [str(ROOT / "tools" / TOOL), "--provider", provider,
             "--document", document],
            capture_output=True, text=True, cwd=ROOT)
        self.assertEqual(sweep.returncode, 0, sweep.stderr)
        self.assertNotIn(RUN_CHECK, sweep.stdout)
        listed = subprocess.run(
            [str(ROOT / "tools" / TOOL), "--list"],
            capture_output=True, text=True, cwd=ROOT)
        self.assertEqual(listed.stdout.split(), sorted(CHECKS))


class DrivenRunTests(RoutingCase):
    """The gate as a run actually meets it."""

    # `house-voice` is the second check this harness cannot honestly satisfy,
    # and `PropersCase` filters it for the same reason it filters
    # `provenance-matches-run`: these runs drive over a published leaf, the
    # ninth Sunday carries two real `house-voice` loci, and a test may not
    # rewrite a published leaf to get a check past it. The filter is stated
    # there and not repeated here, so that a harness which stopped filtering
    # it would surface as a failure rather than be masked by this subclass.
    # What the check decides is held in `ProseCheckTests` above, by running
    # the tool over that leaf and every other leaf in the corpus.

    def drive_to_preflight(self, run_id: str | None = None) -> str:
        """Seed if needed, then advance until the run is waiting at the gate."""
        if run_id is None:
            run_id, _ = self.advance_to("research")
            out = self.engine.advance(
                run_id, lane_results=self.lane_submissions(run_id))
            self.assertEqual(out["stage"], "research-synthesis")
        out = self.engine.advance(
            run_id, result_path=self.worker_pass(run_id, "research-synthesis"))
        self.assertEqual(out["stage"], "source-registration")
        out = self.engine.advance(
            run_id,
            result_path=self.worker_pass(run_id, "source-registration"))
        self.assertEqual(out["stage"], "author-proper")
        out = self.engine.advance(
            run_id, result_path=self.worker_pass(run_id, "author-proper"))
        self.assertEqual(out["stage"], STAGE,
                         "the author hands the leaf to the preflight")
        return run_id

    def stub_failure(self, check: str, finding_id: str):
        """Answer only this gate with FAIL, leaving every other gate real."""
        real = self.engine._run_gate

        def run_gate(workflow, declared, state, rid):
            if declared["id"] != STAGE:
                return real(workflow, declared, state, rid)
            return {
                "disposition": FAIL, "stage": STAGE,
                "iteration": _current_packet(state, STAGE)["iteration"],
                "findings": [{
                    "id": finding_id, "severity": "blocking", "check": check,
                    "problem": "command exited 1",
                    "required_result": f"{check} must pass",
                }],
            }

        self.engine._run_gate = run_gate

    def test_the_gate_runs_for_real_and_passes_the_published_leaf(self):
        """The nine checks the tree can answer, over a real published leaf.

        The tenth is filtered out by the harness, for the reason
        `PropersCase` gives: these runs submit a synthetic `author-proper`
        result, so no author writes the provenance record, and the leaf they
        drive over states the run that really did write it. What the gate does
        when it is not filtered is the next test.
        """
        run_id = self.drive_to_preflight()
        out = self.engine.advance(run_id, run_gate=True)
        self.assertEqual(out["stage"], "content-evaluation")
        state = self.engine.load_state(run_id)
        self.assertEqual(state["transitions"][-1],
                         {"from": STAGE, "to": "content-evaluation",
                          "disposition": PASS})
        logs = sorted(
            path.name for path in
            (self.engine.run_dir(run_id) / "gate-logs").glob(f"{STAGE}-*"))
        # Read off the pipeline rather than a tuple here: the harness filters
        # two checks out of this run, and a hand-kept list would have to be
        # edited every time the gate gains one.
        self.assertEqual(
            [name.split("-", 3)[-1] for name in logs],
            sorted(f"{check['id']}.log" for check in stage()["checks"]
                   if check["id"] not in self.unsatisfiable_checks),
            "every declared check ran and left its untouched log")
        for name in logs:
            text = (self.engine.run_dir(run_id) / "gate-logs" / name
                    ).read_text(encoding="utf-8")
            self.assertIn("exit 0", text)
            self.assertIn(f"tools/tpt {TOOL}", text)

    def test_the_gate_refuses_a_leaf_that_states_another_run(self):
        """The whole chain, unstubbed, over a leaf that really is stale.

        The published leaf this suite drives runs against records `unknown`
        for all five run fields: it was installed before any run wrote a
        provenance record. That is precisely the leaf a stage which ignored
        the instruction would leave behind, so the gate must refuse it, and
        refusing it proves every link at once -- the engine substituted its
        own run identity into the check command, the tool compared the record
        against it, and the mismatch came back as a blocking finding routed to
        the reviser.
        """
        # Only this one comes back. `house-voice` stays filtered because it
        # is unsatisfiable over the same leaf for an unrelated reason, and
        # letting it in would put a second finding beside the one this test
        # is about -- and then the assertion below would no longer be able to
        # say that the run check is what refused the leaf.
        self.unsatisfiable_checks.discard(RUN_CHECK)
        run_id = self.drive_to_preflight()
        out = self.engine.advance(run_id, run_gate=True)
        self.assertEqual(out["stage"], "content-revision",
                         "a leaf stating another run is a leaf defect")
        state = self.engine.load_state(run_id)
        self.assertEqual(state["transitions"][-1],
                         {"from": STAGE, "to": "content-revision",
                          "disposition": FAIL})

        log = next(
            (self.engine.run_dir(run_id) / "gate-logs").glob(
                f"{STAGE}-*-{RUN_CHECK}.log")).read_text(encoding="utf-8")
        self.assertIn("exit 1", log)
        for value in (run_id, state["workflow_digest"], state["repo_commit"],
                      str(state["workflow_version"])):
            self.assertIn(str(value), log,
                          "the command the gate ran carried the run's own "
                          "identity, not a placeholder")
        self.assertNotIn("{run.", log,
                         "a name the engine did not substitute would have "
                         "been compared as literal text")

        packet = Path(out["packet_abs_path"]).read_text(encoding="utf-8")
        forwarded = json.loads(next(
            line for line in packet.splitlines()
            if line.startswith("PRIOR_FINDINGS: "))[len("PRIOR_FINDINGS: "):])
        self.assertEqual([finding["id"] for finding in forwarded],
                         [f"GATE-{RUN_CHECK.upper()}"])
        self.assertIn("the record states workflow_id 'unknown'",
                      forwarded[0]["problem"],
                      "the reviser is told which field disagrees and what "
                      "the leaf says about it")

    def test_a_failing_gate_sends_the_run_to_content_revision(self):
        """The wiring, with the checks themselves stubbed out.

        What the checks decide is held above, against real leaves. What is
        held here is where a decision of FAIL takes the run, which no leaf in
        the tree currently produces.
        """
        run_id = self.drive_to_preflight()
        self.stub_failure("references-used", "GATE-REFERENCES-USED")
        out = self.engine.advance(run_id, run_gate=True)
        self.assertEqual(out["stage"], "content-revision")
        self.assertNotEqual(out["stage"], RESEARCH)
        state = self.engine.load_state(run_id)
        self.assertEqual(state["transitions"][-1],
                         {"from": STAGE, "to": "content-revision",
                          "disposition": FAIL})
        packet = Path(out["packet_abs_path"]).read_text(encoding="utf-8")
        forwarded = json.loads(next(
            line for line in packet.splitlines()
            if line.startswith("PRIOR_FINDINGS: "))[len("PRIOR_FINDINGS: "):])
        self.assertEqual([f["id"] for f in forwarded],
                         ["GATE-REFERENCES-USED"],
                         "the reviser is handed the check's own output")

    def test_three_consecutive_refusals_block_the_run(self):
        """The cheap loop is cheap, and bounded like every other.

        The reviser returns to the gate directly, so a refusal costs one
        worker and one gate run. Nothing upstream is disturbed: no evaluation
        lane, no research lane, no synthesis. Three consecutive refusals end
        the run.
        """
        run_id = self.drive_to_preflight()
        self.stub_failure("relation-coverage", "GATE-RELATION-COVERAGE")
        for _ in range(2):
            out = self.engine.advance(run_id, run_gate=True)
            self.assertEqual(out["stage"], "content-revision")
            out = self.engine.advance(
                run_id,
                result_path=self.worker_pass(run_id, "content-revision"))
            self.assertEqual(
                out["stage"], STAGE,
                "the reviser goes back to the gate that refused it")
        out = self.engine.advance(run_id, run_gate=True)
        self.assertEqual(out["disposition"], BLOCKED)
        self.assertIn("iteration limit exceeded", out["message"])
        self.assertIn(STAGE, out["message"])


if __name__ == "__main__":
    unittest.main()
