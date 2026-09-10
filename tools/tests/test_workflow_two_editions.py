#!/usr/bin/env python3
"""A leaf builds two documents, and it builds them in order: largest first.

`main.tex` builds the canonical guide and `synthesis.tex` builds the synthesis
companion beside it. Both are published, and which prose reaches which reader
is decided inside the leaf.

The hazard this module has always guarded is one claim published twice and
corrected once: a defect repaired in the edition a finding named while the
same claim stands wrong in the edition nobody opened. Run `ca03f1b357e7ec25`
paid for it when the content evaluator read only the canonical build.

The first answer was to send every content lane into both documents at once.
It closed that hole and opened a worse one. Run `e4aebcbd941b6b1a` authored
and evaluated both editions together for seven rounds: every lane read two
documents, every finding was repaired in two places, findings of the form
"repaired in one edition, published in the other" recurred anyway, and prose
duplicated between the editions was recorded as an *unowned observation at six
consecutive iterations* by two different lanes, both saying plainly that no
criterion reached it. Nothing could adjudicate two documents in flight at
once. The run reached its absolute iteration ceiling.

The answer now is a sequence. The canonical edition is authored and settled
alone; `derive-synthesis` then writes the companion from it; and
`synthesis-evaluation` reads the two together, with the larger one fixed,
which is the only arrangement in which "does the companion agree with the
canonical edition" is a decidable question with an owner.

Five rules are held here, in the bytes a worker is handed:

1. `content-evaluation` sends its lanes into the canonical edition alone, and
   says so rather than leaving it to be inferred.
2. `author-proper` does not write the companion and says whose it is.
3. The pipeline really is a sequence: the canonical loop's pass transition is
   the derivation, and the companion's evaluation stands between it and the
   artifact build.
4. `derive-synthesis` derives the leaf's form rather than asserting one, and
   adds nothing the canonical edition does not carry.
5. `synthesis-evaluation` is where both documents are read together, and
   `synthesis-revision` may not touch the settled canonical prose.

Every matcher is run against the text it replaced, so none can pass by
matching nothing, and against stages that never had the rule, so none passes
by matching boilerplate.
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
    SYNTHESIS_LANES,
    PropersCase,
    workflow_json,
)

AUTHOR = "author-proper"
EVALUATION = "content-evaluation"
REVISER = "content-revision"
DERIVE = "derive-synthesis"
SYNTH_EVAL = "synthesis-evaluation"
SYNTH_REVISER = "synthesis-revision"

# ---------------------------------------------------------------------------
# The text each rule replaced, quoted rather than fetched from history so the
# rules can be held to it in any checkout.
# ---------------------------------------------------------------------------

# content-evaluation.md's task in the original defect: one document, named in
# the singular, and the lanes read exactly what they were sent to read.
PRE_CHANGE_EVALUATION_TASK = """
You are a fresh evaluator. Evaluate the content and evidence quality of the
canonical proper leaf. Do not rediscover what mechanical gates will check
later (build success, PDF existence, undefined references). Focus on
scholarly content.
"""

# The intermediate answer, which this module now exists to prevent returning
# to: both editions in front of every lane, at the same time.
PRE_CHANGE_BOTH_AT_ONCE = """
Follow the inputs both ways and write down what each document puts in front
of a reader. Prose that reaches only one of them is parallel prose: the same
claim is made twice, in two places, and a lane that read only the canonical
build has not read the document. Read both editions.
"""

# author-proper.md's account of the second document while it still wrote one.
PRE_CHANGE_AUTHOR_SYNTHESIS = """
Author or revise the canonical proper leaf. The canonical leaf owns the
prose, research, and audit records. The synthesis artifact is mechanically
derived from it.

2. Create or update `synthesis.tex` as a 2-line stub that defines
   `\\TriptychSynthesisEdition` and inputs `main.tex`.
"""

# A rule written from the form rather than the mechanism. It reads correctly
# and is false of thirteen of this tree's leaves: ten build no synthesis
# edition at all, and three build one from a standalone `synthesis.tex` with
# no branch in `main.tex`. Rule 4 must not be satisfied by this.
FORM_ASSERTING_RULE = """
The leaf builds two editions. `synthesis.tex` is a two-line stub that inputs
`main.tex`, and `main.tex` branches on `\\ifdefined\\TriptychSynthesisEdition`
to choose between `sections/30-commentary` and
`sections/synthesis/20-integrated-commentary`. Write both.
"""


def sentences(text: str) -> list[str]:
    """Reconstruct hard-wrapped Markdown into sentences.

    The fragments wrap at 78 columns, so a rule routinely spans three lines
    and a line-based check would see half of it.
    """
    flat = " ".join(text.split())
    return [part for part in re.split(r"(?<=[.:;?])\s+", flat) if part]


def flat(text: str) -> str:
    return " ".join(text.split())


def fragment(name: str) -> str:
    return (FRAGMENTS / "propers" / f"{name}.md").read_text(encoding="utf-8")


def lane_fragment(name: str) -> str:
    return (FRAGMENTS / "propers" / "lanes" / f"{name}.md").read_text(
        encoding="utf-8")


# ---------------------------------------------------------------------------
# Matchers
# ---------------------------------------------------------------------------

def says_canonical_only(text: str) -> bool:
    """The reader is told to work on one edition, and which one.

    Deliberately not anchored on a period: the sentence that carries this
    rule routinely contains `main.tex`, and a matcher built from `[^.]` spans
    stops dead on the filename.
    """
    body = flat(text)
    return bool(
        re.search(r"canonical edition.{0,120}?"
                  r"(alone|and nothing else|only that)", body)
        or re.search(r"(alone|only).{0,60}?canonical edition", body)
    )


def says_companion_is_not_mine(text: str) -> bool:
    """The reader is told the companion belongs to another stage."""
    body = flat(text)
    return bool(
        re.search(r"companion is not yours|do not write it here|"
                  r"belongs? to `?derive-synthesis", body)
        and "derive-synthesis" in body
    )


def derives_the_form(text: str) -> bool:
    """The reader is told to find out what the leaf builds, not assume it."""
    body = flat(text)
    return bool(
        re.search(r"Do not assume a form|three states", body)
        and re.search(r"no companion", body)
    )


def adds_nothing(text: str) -> bool:
    """The companion may say less than the canonical edition, never else."""
    body = flat(text)
    return bool(
        re.search(r"the companion says less", body)
        or re.search(r"may add a claim.{0,160}?does not already carry", body)
    )


def reads_both_together(text: str) -> bool:
    """This stage reads the two documents against each other."""
    body = flat(text)
    mentions_both = "companion" in body and "canonical" in body
    compares = re.search(
        r"against the (settled )?canonical|side by side|"
        r"canonical edition it was derived from", body)
    return bool(mentions_both and compares)


def protects_canonical_prose(text: str) -> bool:
    """A companion repair may not edit the settled canonical edition."""
    body = flat(text)
    return bool(re.search(
        r"may not revise (it|the canonical)|"
        r"may not.{0,40}?revise the canonical|"
        r"not revise the canonical edition", body))


def names_the_file(text: str) -> bool:
    body = flat(text)
    return bool(re.search(
        r"[Nn]ame in every finding the file the defect is in", body))


RULES = {
    "canonical-only": says_canonical_only,
    "not-mine": says_companion_is_not_mine,
    "derives-form": derives_the_form,
    "adds-nothing": adds_nothing,
    "reads-both": reads_both_together,
    "protects-canonical": protects_canonical_prose,
    "names-file": names_the_file,
}


class MatcherTests(unittest.TestCase):
    """The matchers must be able to fail, and must reject what they replaced."""

    def test_no_rule_fires_on_nothing(self):
        for name, rule in RULES.items():
            with self.subTest(rule=name):
                self.assertFalse(rule(""), f"{name} matches empty text")
                self.assertFalse(
                    rule("The quick brown fox jumps over the lazy dog."),
                    f"{name} matches unrelated prose")

    def test_the_rules_reject_the_evaluation_task_they_replaced(self):
        for name in ("canonical-only", "not-mine", "reads-both"):
            with self.subTest(rule=name):
                self.assertFalse(RULES[name](PRE_CHANGE_EVALUATION_TASK))

    def test_the_canonical_only_rule_rejects_reading_both_at_once(self):
        """The intermediate answer must not satisfy the rule that replaced it.

        `Read both editions.` is exactly what the canonical evaluation no
        longer does, and a matcher that accepted it would let the pipeline
        slide back without a test failing.
        """
        self.assertFalse(says_canonical_only(PRE_CHANGE_BOTH_AT_ONCE))

    def test_the_author_rule_rejects_the_account_it_replaced(self):
        self.assertFalse(says_companion_is_not_mine(PRE_CHANGE_AUTHOR_SYNTHESIS))

    def test_the_form_control_fires_on_a_form_asserting_rule(self):
        """Rule 4 must not be satisfied by a rule written from one leaf's shape."""
        self.assertFalse(derives_the_form(FORM_ASSERTING_RULE))
        self.assertFalse(adds_nothing(FORM_ASSERTING_RULE))

    def test_the_rules_accept_the_statements_that_carry_them(self):
        self.assertTrue(says_canonical_only(
            "You evaluate the canonical edition -- the document `main.tex` "
            "builds -- and nothing else."))
        self.assertTrue(says_companion_is_not_mine(
            "The synthesis companion is not yours and you do not write it "
            "here. It is derived by `derive-synthesis` afterwards."))
        self.assertTrue(derives_the_form(
            "Do not assume a form. Leaves in this tree are in three states. "
            "Where the profile requires no companion, write nothing."))
        self.assertTrue(adds_nothing(
            "Where the two must differ, the companion says less -- never "
            "something else."))
        self.assertTrue(reads_both_together(
            "You evaluate the companion, against the settled canonical "
            "edition it was derived from."))
        self.assertTrue(protects_canonical_prose(
            "The canonical edition is settled and you may not revise it."))


class FragmentTests(unittest.TestCase):
    """The rules are in the fragment bytes a worker is handed."""

    def test_the_canonical_evaluation_reads_one_edition(self):
        self.assertTrue(says_canonical_only(fragment(EVALUATION)))

    def test_the_canonical_evaluation_no_longer_sends_lanes_into_both(self):
        body = flat(fragment(EVALUATION))
        self.assertNotIn("Read both editions.", body)

    def test_the_canonical_evaluation_requires_a_finding_to_name_its_file(self):
        self.assertTrue(names_the_file(fragment(EVALUATION)))

    def test_no_content_lane_still_claims_both_editions(self):
        """The five canonical lanes read one document now.

        Each carried a `Both editions are yours` section under the previous
        contract. Leaving one behind would send that lane into a document the
        stage cannot repair, and route its findings to a stage that has not
        run.
        """
        for lane in CONTENT_LANES:
            with self.subTest(lane=lane):
                text = lane_fragment(f"content-{lane}")
                self.assertNotIn("Both editions are yours", text)
                self.assertTrue(
                    says_canonical_only(text),
                    f"{lane} must say it reads the canonical edition alone")

    def test_the_author_does_not_write_the_companion(self):
        self.assertTrue(says_companion_is_not_mine(fragment(AUTHOR)))

    def test_the_derivation_derives_the_form_and_does_not_assert_one(self):
        self.assertTrue(derives_the_form(fragment(DERIVE)))

    def test_the_derivation_may_not_add_to_the_canonical_edition(self):
        self.assertTrue(adds_nothing(fragment(DERIVE)))

    def test_the_derivation_may_not_revise_the_canonical_edition(self):
        self.assertTrue(protects_canonical_prose(fragment(DERIVE)))

    def test_the_companion_evaluation_reads_both_documents(self):
        """The cross-edition comparison did not vanish; it moved.

        It is the whole point of the sequence that somebody still reads the
        two documents against each other. That somebody is this stage, and it
        does it with the larger edition already fixed.
        """
        self.assertTrue(reads_both_together(fragment(SYNTH_EVAL)))

    def test_the_fidelity_lane_owns_the_duplication_class(self):
        """The class two lanes observed six times with no owner now has one."""
        text = lane_fragment("synthesis-fidelity")
        self.assertTrue(reads_both_together(text))
        self.assertRegex(flat(text), r"verbatim runs?")

    def test_the_companion_reviser_may_not_touch_canonical_prose(self):
        self.assertTrue(protects_canonical_prose(fragment(SYNTH_REVISER)))

    def test_no_research_lane_carries_any_of_these_rules(self):
        """A control: these rules belong to the leaf's stages, not discovery."""
        for lane in RESEARCH_LANES:
            text = lane_fragment(f"research-{lane}")
            for name, rule in RULES.items():
                with self.subTest(lane=lane, rule=name):
                    self.assertFalse(rule(text))

    def test_the_visual_evaluation_still_inspects_both_pdfs(self):
        """Unchanged by the sequence: by then both editions exist and are built."""
        text = flat(fragment("visual-evaluation"))
        self.assertIn("synthesis", text.lower())


class TopologyTests(unittest.TestCase):
    """The pipeline is a sequence, not two things at once."""

    def setUp(self):
        self.stages = {stage["id"]: stage
                       for stage in workflow_json()["stages"]}
        self.order = [stage["id"] for stage in workflow_json()["stages"]]

    def test_the_canonical_loop_hands_off_to_the_derivation(self):
        self.assertEqual(
            self.stages[EVALUATION]["pass_transition"], DERIVE,
            "the canonical edition must be settled before the companion "
            "is written")

    def test_the_companion_is_written_after_the_canonical_edition_passes(self):
        self.assertLess(self.order.index(EVALUATION), self.order.index(DERIVE))
        self.assertLess(self.order.index(DERIVE),
                        self.order.index(SYNTH_EVAL))

    def test_the_companion_is_judged_before_the_artifacts_are_built(self):
        self.assertLess(self.order.index(SYNTH_EVAL),
                        self.order.index("build-artifacts"))
        self.assertEqual(
            self.stages[SYNTH_EVAL]["pass_transition"], "build-artifacts")

    def test_the_companion_admits_a_derivation_owner_and_a_seam_owner(self):
        """A companion defect, and a defect the companion only makes visible.

        Nine blocking findings against one companion in run da04e65ca4ec963b
        split two ways. Six were the derivation's. Three were sentences in the
        canonical prose both editions input -- twenty-four locators sending a
        reader to element subsections the profile forbids the companion -- and
        they reached a reviser whose remit was the companion alone. It reported
        them unrepaired, which was the honest answer and left the defect with
        no owner at all.
        """
        self.assertEqual(
            self.stages[SYNTH_EVAL]["repair_routes"],
            [{"repair_target": "derivation",
              "transition": SYNTH_REVISER},
             {"repair_target": "seam",
              "transition": SYNTH_REVISER}])
        self.assertEqual(self.stages[SYNTH_REVISER]["repairs"],
                         ["derivation", "seam"])
        self.assertEqual(self.stages[SYNTH_REVISER]["revision_target"], DERIVE)

    def test_the_companion_evaluation_fans_out_over_its_own_lanes(self):
        execution = self.stages[SYNTH_EVAL]["execution"]
        self.assertEqual([lane["id"] for lane in execution["lanes"]],
                         SYNTHESIS_LANES)

    def test_the_workflow_declares_the_version_that_carries_this(self):
        self.assertGreaterEqual(workflow_json()["version"], 26)


class EmittedPacketTests(PropersCase):
    """The rules survive into the bytes the engine actually emits."""

    def packet_for(self, stage_id: str) -> str:
        stage = {s["id"]: s for s in workflow_json()["stages"]}[stage_id]
        parts = []
        for name in stage.get("fragments", []):
            parts.append((FRAGMENTS / name).read_text(encoding="utf-8"))
        return "\n".join(parts)

    def test_the_canonical_evaluation_packet_reads_one_edition(self):
        self.assertTrue(says_canonical_only(self.packet_for(EVALUATION)))

    def test_every_content_lane_packet_reads_one_edition(self):
        for lane in CONTENT_LANES:
            with self.subTest(lane=lane):
                text = (self.packet_for(EVALUATION)
                        + lane_fragment(f"content-{lane}"))
                self.assertTrue(says_canonical_only(text))
                self.assertNotIn("Both editions are yours", text)

    def test_the_author_packet_says_the_companion_is_not_its_work(self):
        self.assertTrue(says_companion_is_not_mine(self.packet_for(AUTHOR)))

    def test_the_derivation_packet_carries_its_rules(self):
        text = self.packet_for(DERIVE)
        self.assertTrue(derives_the_form(text))
        self.assertTrue(adds_nothing(text))

    def test_the_companion_evaluation_packet_reads_both(self):
        self.assertTrue(reads_both_together(self.packet_for(SYNTH_EVAL)))

    def test_the_rules_are_not_in_every_packet(self):
        """A control: a rule in every packet is boilerplate, not a rule."""
        text = self.packet_for("research-synthesis")
        self.assertFalse(says_canonical_only(text))
        self.assertFalse(derives_the_form(text))


if __name__ == "__main__":
    unittest.main()
