#!/usr/bin/env python3
"""A leaf builds two documents, and the content evaluation now knows it.

`main.tex` builds the canonical guide and `synthesis.tex` builds the synthesis
edition beside it. Which prose reaches which reader is decided inside the
leaf: by `\\ifdefined\\TriptychSynthesisEdition` branches, and by section files
only one of the two documents inputs. Both are published.

The visual evaluator was told this from the start — its inspection method says
to inspect both the canonical and synthesis PDFs — and the content evaluator
was told the opposite by omission, being sent to read "the canonical proper
leaf". Run `ca03f1b357e7ec25` paid for the asymmetry: three evaluations across
five lanes read the canonical build, findings named sections rather than
files, and a reviser repaired whichever file a section name could be read as
naming while the same claim stood uncorrected in the edition nobody had
opened. No mechanical gate would have caught it, because both editions render.

Four rules are held here, in the bytes a worker is handed:

1. `content-evaluation` says how to find out what a leaf builds, rather than
   asserting a form. Leaves are in three states in this tree, so a rule
   written from the form would be false of most of them.
2. A finding names the file the defect is in, not the section. Two files
   answer to "the detailed commentary".
3. Each of the five content lanes says what its own criteria owe the edition
   the canonical build does not show.
4. `content-revision` re-reads both editions after an edit, and
   `author-proper` no longer calls the synthesis mechanically derived.

Every matcher is run against the text it replaced, so none can pass by
matching nothing, and against the stages that never had the rule, so none
passes by matching boilerplate.
"""
import re
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from test_workflow_research_fanout import (  # noqa: E402
    CONTENT_LANES,
    FRAGMENTS,
    RESEARCH_LANES,
    PropersCase,
    workflow_json,
)

AUTHOR = "author-proper"
EVALUATION = "content-evaluation"
REVISER = "content-revision"

# ---------------------------------------------------------------------------
# The text each rule replaced, quoted rather than fetched from history so the
# rules can be held to it in any checkout.
# ---------------------------------------------------------------------------

# content-evaluation.md's whole task before this change. One document, named
# in the singular, and the lanes read exactly what they were sent to read.
PRE_CHANGE_EVALUATION_TASK = """
You are a fresh evaluator. Evaluate the content and evidence quality of the
canonical proper leaf. Do not rediscover what mechanical gates will check
later (build success, PDF existence, undefined references). Focus on
scholarly content.
"""

# The nearest content-evaluation.md came to a finding-location rule: ids, not
# loci. It says where a finding is filed and never where the defect is.
PRE_CHANGE_FINDING_IDENTITY = """
Finding IDs must use the `CON-` prefix and be stable across iterations. This
is now load-bearing and not only tidy. So reuse an id for the same unrepaired
defect, never for a different one, and never mint a new id for a defect you
are restating.
"""

# author-proper.md's account of the second document before this change: true
# of the file and misleading about the document, which is the whole defect.
PRE_CHANGE_AUTHOR_SYNTHESIS = """
Author or revise the canonical proper leaf. The canonical leaf owns the
prose, research, and audit records. The synthesis artifact is mechanically
derived from it.

2. Create or update `synthesis.tex` as a 2-line stub that defines
   `\\TriptychSynthesisEdition` and inputs `main.tex`.
"""

# content-revision.md's step list before this change. It says to verify that
# a repair introduced no new violation, and never that the repair may have
# reached only one of the two places the claim is published in.
PRE_CHANGE_REVISION_STEPS = """
3. Do not paraphrase or reinterpret the findings. Address them as written.
4. After addressing all findings, verify that the changes do not introduce
   new violations of the evaluation criteria.
5. Follow the same authoring rules as the author-proper stage, including the
   house voice: this packet carries `author-proper.md` in full.
"""

# A rule written from the form rather than the mechanism. It reads correctly
# and is false of thirteen of this tree's leaves: ten build no synthesis
# edition at all, and three build one from a standalone `synthesis.tex` with
# no branch in `main.tex`. Rule 1 must not be satisfied by this.
FORM_ASSERTING_RULE = """
The leaf builds two editions. `synthesis.tex` is a two-line stub that inputs
`main.tex`, and `main.tex` branches on `\\ifdefined\\TriptychSynthesisEdition`
to choose between `sections/30-commentary` and
`sections/synthesis/20-integrated-commentary`. Read both.
"""


def sentences(text: str) -> list[str]:
    """Reconstruct hard-wrapped Markdown into sentences.

    The fragments wrap at 78 columns, so a rule routinely spans three lines
    and a line-based check would see half of it.
    """
    flat = " ".join(text.split())
    return [part for part in re.split(r"(?<=[.:;?])\s+", flat) if part]


def _hits(text: str, *patterns: re.Pattern) -> list[str]:
    """Sentences in which every pattern fires at once.

    Each rule below is a conjunction within one sentence: the two halves of
    a rule stated in different paragraphs are two facts, not a rule.
    """
    return [s for s in sentences(text)
            if all(pattern.search(s) for pattern in patterns)]


def _re(pattern: str) -> re.Pattern:
    return re.compile(pattern, re.IGNORECASE)


# Rule 1: the leaf builds more than one reader-facing document.
LEAF = _re(r"\bleaf\b|source tree")
MULTIPLE = _re(r"more than one|two (documents|editions)|second (published"
               r"|reader-facing)? ?document|both editions")
DOCUMENT = _re(r"\bdocuments?\b|\beditions?\b")

# Rule 1': and it is established by reading the leaf, not asserted as a form.
DERIVE = _re(r"\bread out of\b|follow the inputs|list the leaf's|establish"
             r"|decides? what|rather than inferred")
FILES = _re(r"\.tex|\binputs?\b|branch\w*|files")

# Rule 2: a finding names the file, not only the section.
NAME = _re(r"\bname\b|\bnaming\b|\bnames\b")
FINDING = _re(r"\bfinding\b")
FILE_NOT_SECTION = _re(r"file .{0,40}(not|never|rather than) .{0,20}section"
                       r"|not .{0,20}the section it belongs to"
                       r"|file the (defect|claim|citation|sentence) ")

# Rule 3: reading one edition is not reading the document.
ONE_EDITION_INSUFFICIENT = _re(
    r"read only the canonical|canonical build alone|reading `main\.tex`"
    r" ?alone|has not read the document|edition nobody opened"
    r"|does not show|never inputs")

# Rule 4: a repair to one edition is not a repair to the other.
REPAIR = _re(r"repair\w*|correct\w*|edit\b|fix\w*")
NOT_THE_OTHER = _re(r"not a repair to the other|leaves the other"
                    r"|one corrected edition and one uncorrected"
                    r"|published and wrong")

# Negative control: the fragments must not assert the stub-and-branch form as
# the shape every leaf has. Ten leaves have no synthesis edition.
ASSERTS_THE_FORM = _re(
    r"(the leaf|every leaf|a leaf) (builds|has) two (editions|documents)\b")


def builds_more_than_one_document(text: str) -> list[str]:
    return _hits(text, LEAF, MULTIPLE, DOCUMENT)


def derived_from_the_leaf_not_asserted(text: str) -> list[str]:
    return _hits(text, DERIVE, FILES)


def a_finding_names_the_file(text: str) -> list[str]:
    return _hits(text, NAME, FINDING, FILE_NOT_SECTION)


def one_edition_is_not_the_document(text: str) -> list[str]:
    return _hits(text, ONE_EDITION_INSUFFICIENT)


def a_repair_to_one_is_not_a_repair_to_both(text: str) -> list[str]:
    return _hits(text, REPAIR, NOT_THE_OTHER)


def asserts_the_form(text: str) -> list[str]:
    return _hits(text, ASSERTS_THE_FORM)


def fragment(name: str) -> str:
    return (FRAGMENTS / "propers" / f"{name}.md").read_text(encoding="utf-8")


def lane_fragment(family: str, lane: str) -> str:
    return (FRAGMENTS / "propers" / "lanes"
            / f"{family}-{lane}.md").read_text(encoding="utf-8")


class MatcherTests(unittest.TestCase):
    """Each rule is proved to discriminate before it is used to assert."""

    RULES = (
        ("builds-more-than-one", builds_more_than_one_document),
        ("derived-not-asserted", derived_from_the_leaf_not_asserted),
        ("finding-names-the-file", a_finding_names_the_file),
        ("one-edition-insufficient", one_edition_is_not_the_document),
        ("repair-reaches-both", a_repair_to_one_is_not_a_repair_to_both),
        ("asserts-the-form", asserts_the_form),
    )

    def assert_rejects(self, rule, samples, label):
        for text in samples:
            with self.subTest(rule=label, rejects=" ".join(text.split())[:70]):
                self.assertEqual(
                    rule(text), [],
                    f"{label} fires on text that does not state it")

    def assert_accepts(self, rule, samples, label):
        for text in samples:
            with self.subTest(rule=label, accepts=" ".join(text.split())[:70]):
                self.assertTrue(
                    rule(text), f"{label} misses a real statement of it")

    def test_no_rule_fires_on_nothing(self):
        for label, rule in self.RULES:
            with self.subTest(rule=label):
                self.assertEqual(rule(""), [])
                self.assertEqual(rule("The propers are appointed texts."), [])

    def test_the_rules_reject_the_task_they_replaced(self):
        for label, rule in self.RULES:
            with self.subTest(rule=label):
                self.assert_rejects(
                    rule, [PRE_CHANGE_EVALUATION_TASK], label)

    def test_the_file_rule_rejects_the_id_rule_it_sits_beside(self):
        self.assert_rejects(
            a_finding_names_the_file,
            [PRE_CHANGE_FINDING_IDENTITY,
             # A stable id says which finding this is; it says nothing about
             # which of two published files carries the defect.
             "Finding IDs must be stable across iterations."],
            "finding-names-the-file")

    def test_the_author_rules_reject_the_account_they_replaced(self):
        self.assert_rejects(
            builds_more_than_one_document,
            [PRE_CHANGE_AUTHOR_SYNTHESIS], "builds-more-than-one")
        self.assert_rejects(
            a_repair_to_one_is_not_a_repair_to_both,
            [PRE_CHANGE_AUTHOR_SYNTHESIS], "repair-reaches-both")

    def test_the_revision_rule_rejects_the_steps_it_replaced(self):
        self.assert_rejects(
            a_repair_to_one_is_not_a_repair_to_both,
            [PRE_CHANGE_REVISION_STEPS,
             # The reading that cost the run: one file, verified once.
             "After addressing a finding, re-read the file you changed and "
             "check that the correction introduced no new violation."],
            "repair-reaches-both")

    def test_the_rules_accept_the_statements_that_carry_them(self):
        self.assert_accepts(
            builds_more_than_one_document,
            ["A leaf is one source tree, and it may build more than one "
             "reader-facing document out of it."],
            "builds-more-than-one")
        self.assert_accepts(
            derived_from_the_leaf_not_asserted,
            ["List the leaf's top-level `.tex` files and follow the inputs "
             "both ways."],
            "derived-not-asserted")
        self.assert_accepts(
            a_finding_names_the_file,
            ["Name in every finding the file the defect is in, never only "
             "the section it belongs to."],
            "finding-names-the-file")
        self.assert_accepts(
            a_repair_to_one_is_not_a_repair_to_both,
            ["A repair to one edition's prose is not a repair to the other."],
            "repair-reaches-both")

    def test_the_form_control_fires_on_a_form_asserting_rule(self):
        """The control that keeps rule 1 from becoming what it must not be.

        Ten of this tree's leaves build no synthesis edition and three build
        one with no branch in `main.tex`. A rule stating the stub-and-branch
        form as fact would be false for most of the corpus and would send a
        lane looking for a branch that is not there.
        """
        self.assert_accepts(
            asserts_the_form,
            [FORM_ASSERTING_RULE,
             "Every leaf builds two editions from one `main.tex`."],
            "asserts-the-form")
        self.assert_rejects(
            asserts_the_form,
            ["A leaf is one source tree, and it may build more than one "
             "reader-facing document out of it.",
             "Where `synthesis.tex` is a document in its own right, its "
             "`\\input` list decides."],
            "asserts-the-form")


class FragmentTests(unittest.TestCase):
    """The rules, in the fragment sources that carry them."""

    def test_the_evaluation_says_the_leaf_builds_more_than_one_document(self):
        self.assertTrue(builds_more_than_one_document(fragment(EVALUATION)))

    def test_the_evaluation_derives_the_form_and_does_not_assert_it(self):
        text = fragment(EVALUATION)
        self.assertTrue(
            derived_from_the_leaf_not_asserted(text),
            "the evaluator must be told to read what the leaf builds out of "
            "its own files; three forms exist in this tree")
        self.assertEqual(
            asserts_the_form(text), [],
            "a rule asserting the stub-and-branch form is false of the ten "
            "leaves that build no synthesis edition")

    def test_the_evaluation_requires_a_finding_to_name_its_file(self):
        self.assertTrue(a_finding_names_the_file(fragment(EVALUATION)))

    def test_the_evaluation_says_one_edition_is_not_the_document(self):
        self.assertTrue(one_edition_is_not_the_document(fragment(EVALUATION)))

    def test_every_content_lane_carries_the_rule_for_its_own_criteria(self):
        for lane in CONTENT_LANES:
            with self.subTest(lane=lane):
                text = lane_fragment("content", lane)
                self.assertTrue(
                    builds_more_than_one_document(text),
                    "the lane owns criteria, and it must be told those "
                    "criteria are asked of every edition")
                self.assertTrue(
                    a_finding_names_the_file(text),
                    "a lane's finding is what reaches the reviser; it names "
                    "the file or the reviser guesses")
                self.assertEqual(
                    asserts_the_form(text), [],
                    "the lane must not be sent looking for a branch that "
                    "this leaf may not have")

    def test_no_research_lane_carries_the_rule(self):
        """A matcher that fires everywhere proves nothing where it matters.

        The research lanes sweep evidence and never read the built prose, so
        the rule has no work to do there and its presence would mean the
        matcher is catching boilerplate.
        """
        for lane in RESEARCH_LANES:
            with self.subTest(lane=lane):
                text = lane_fragment("research", lane)
                self.assertEqual(builds_more_than_one_document(text), [])
                self.assertEqual(a_finding_names_the_file(text), [])

    def test_the_reviser_is_told_a_repair_may_reach_only_one_edition(self):
        self.assertTrue(
            a_repair_to_one_is_not_a_repair_to_both(fragment(REVISER)))

    def test_the_author_no_longer_calls_the_synthesis_merely_derived(self):
        text = fragment(AUTHOR)
        self.assertTrue(
            builds_more_than_one_document(text),
            "the author writes both editions and must be told so")
        self.assertNotIn(
            "The synthesis artifact is mechanically\nderived from it.", text,
            "'mechanically derived' is what let a second authored document "
            "read as a by-product of the first")

    def test_the_reviser_still_loads_the_author_fragment(self):
        """The rules the author carries must keep reaching the reviser."""
        stages = {s["id"]: s for s in workflow_json()["stages"]}
        self.assertIn(f"propers/{AUTHOR}.md", stages[REVISER]["fragments"])

    def test_the_visual_evaluation_still_inspects_both_pdfs(self):
        """The instruction the content side was missing, left where it is.

        This is the asymmetry version 19 closed, and a regression here would
        mean the visual side lost it while the content side gained it.
        """
        self.assertRegex(
            fragment("visual-evaluation"),
            _re(r"both the canonical and synthesis PDFs"))


class EmittedPacketTests(PropersCase):
    """The same rules, in the bytes the workers are actually handed."""

    def compiled_packets(self) -> dict[str, str]:
        run_id, _ = self.advance_to("research")
        workflow = self.engine.load_workflow("proper")
        state = self.engine.load_state(run_id)
        packets = {}
        for stage in workflow["stages"]:
            compiled = self.engine._compile_stage_packets(
                workflow, stage, state, self.engine.run_dir(run_id), [])
            packets[stage["id"]] = compiled["bytes"].decode("utf-8")
            for lane in compiled.get("lanes", []):
                packets[f"{stage['id']}/{lane['lane']}"] = \
                    lane["bytes"].decode("utf-8")
        return packets

    def setUp(self):
        super().setUp()
        self.packets = self.compiled_packets()

    def test_every_content_lane_packet_carries_the_rule(self):
        for lane in CONTENT_LANES:
            with self.subTest(lane=lane):
                text = self.packets[f"{EVALUATION}/{lane}"]
                self.assertTrue(builds_more_than_one_document(text))
                self.assertTrue(derived_from_the_leaf_not_asserted(text))
                self.assertTrue(a_finding_names_the_file(text))
                self.assertTrue(one_edition_is_not_the_document(text))
                self.assertEqual(asserts_the_form(text), [])

    def test_the_author_packet_carries_the_two_document_account(self):
        self.assertTrue(builds_more_than_one_document(self.packets[AUTHOR]))

    def test_the_reviser_packet_carries_the_repair_rule(self):
        self.assertTrue(
            a_repair_to_one_is_not_a_repair_to_both(self.packets[REVISER]))

    def test_the_rule_is_not_in_every_packet(self):
        """A matcher that fires everywhere proves nothing where it matters."""
        for stage in ("source-audit", "build-artifacts", "generate-web"):
            with self.subTest(stage=stage):
                text = self.packets[stage]
                self.assertEqual(
                    a_finding_names_the_file(text), [],
                    "the finding-location rule is reaching a packet that "
                    "never had it; the matcher is catching boilerplate")
                self.assertEqual(
                    a_repair_to_one_is_not_a_repair_to_both(text), [])

    def test_the_workflow_declares_the_version_that_carries_this(self):
        self.assertGreaterEqual(int(workflow_json()["version"]), 19)


if __name__ == "__main__":
    unittest.main()
