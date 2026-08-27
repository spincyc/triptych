#!/usr/bin/env python3
"""Evidence discipline the packets must carry, not the prose about them.

Three defects from run 7521f033d37e8997, each held here where it has to
hold: in the bytes a worker is actually handed.

1. The author needed page-2 date, place, and genre evidence; the brief did
   not carry it and did not say so; the author retrieved it itself, by
   direct fetch from a restricted source and from volumes this repository
   does not hold. That cost an entire seven-lane research round. The brief
   now certifies coverage section by section, and the author is told that
   needing evidence the brief lacks *is* an inadequate brief.
2. The long-form sections carried the brief's qualifications and the short
   forms dropped them — five instances across two evaluation rounds. A
   restatement now inherits the evidence state of what it restates.
3. Six lanes died to server errors at the moment of serialising a result
   after 20-40 minutes of retrieval. A lane now saves as it goes.

Every rule asserted here is also run against the text it replaced, so a
matcher cannot pass by matching nothing, and the coverage rule is run
against a quality bar it must *not* impose: a section with no citable
evidence in this repository is a legitimate PASS.
"""
import re
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from test_workflow_research_fanout import (  # noqa: E402
    FRAGMENTS,
    RESEARCH_LANES,
    PropersCase,
    workflow_json,
)

AUTHOR = "author-proper"
SYNTHESIS = "research-synthesis"
REVISER = "content-revision"

# ---------------------------------------------------------------------------
# The text each rule replaced, quoted rather than fetched from history so the
# rules can be held to it in any checkout. A matcher that does not reject
# these is not testing anything.
# ---------------------------------------------------------------------------

# author-proper.md's whole BLOCKED contract before this change. It already
# said to block on a brief "missing evidence you need", and the author still
# read a missing page-2 evidence base as a gap to fill rather than as the
# insufficiency this paragraph names.
PRE_CHANGE_BLOCKED_CONTRACT = """
If `research/scope.md` is insufficient, contradictory, missing evidence you
need, or otherwise unsuitable to author from safely, do not repair it and do
not author around it. Return `disposition: "BLOCKED"`, naming in the summary
exactly what the brief lacks. The run stops there, and the deficiency is on
the record where the workflow can act on it; a brief quietly patched by the
author would leave no such record.
"""

# The nearest author-proper.md came to the short-form rule: evidence states
# by reference, and the short forms named only as pagination.
PRE_CHANGE_SHORT_FORM_NEIGHBOURHOOD = """
9. Ensure the brief synthesis markers
   (`triptych:brief-synthesis:start`, `:end`, `:next`) are placed correctly
   for the two-page gate.
10. Follow `guidance/editorial.md` for evidence states, attribution,
    metadata, review, and publication standards.

- Themes and Movement: pages 3-4, exactly two complete readable pages
- Brief synthesis: must occupy exactly two physical pages (N and N+1)
"""

# research-synthesis.md's PASS before this change, with the one step that
# came closest to a coverage statement. Both name evidence gaps; neither
# ties a gap to the reader-facing section that will go without.
PRE_CHANGE_SYNTHESIS_COVERAGE = """
6. Name the missing evidence that should block or constrain authoring,
   drawing on the `source-citation-coverage` lane's findings.

`PASS` - the joined research supports a brief that can be authored from.
Return `findings: []`, `artifact_path` pointing at `research/scope.md`, and a
summary naming the overlaps reconciled, the cross-proper claims settled, the
exploratory proposals developed, and the evidence gaps found.
"""

# research.md's result contract before this change: a lane was told what to
# return and never when to save it.
PRE_CHANGE_LANE_RESULT = """
Return a research result validated against `research-result.json`, carrying
`stage`, `iteration`, `disposition`, `summary`, and `findings`, plus the
`lane` and `lane_packet_hash` that `common/result-format.md` explains. Use
`PASS` when your sweep completed and `BLOCKED` when something stopped it; a
research lane has no `CHANGES_REQUIRED`.
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


# Rule A: retrieving evidence is out of scope for the authoring stage.
RETRIEVAL = _re(r"retriev\w*|fetch\w*|download\w*|acquir\w*|gather\w*")
OUT_OF_SCOPE = _re(r"out of scope|not this stage's|never .{0,30}yourself")
# Rule A': and the scope does not widen because a source is easy to reach.
SOURCE_BLIND = _re(r"whatever the source|however easy|ease is not permission"
                   r"|one command away")

# Rule B: needing evidence the brief does not carry is an inadequate brief.
NEEDS = _re(r"\bneed\w*\b")
EVIDENCE = _re(r"\bevidence\b")
BRIEF = _re(r"\bbrief\b")
INADEQUACY = _re(r"insufficien\w*|inadequa\w*|deficien\w*|unsuitable")

# Rule C: a restatement inherits the evidence state of what it restates.
SHORT_FORM = _re(r"short form|restat\w*|briefly|compress\w*|shorter")
EVIDENCE_STATE = _re(r"evidence state|qualification\w*|unverified lead"
                     r"|\blead\b|\bbound\b|evidenced")

# Rule D: the brief certifies coverage per reader-facing section, before PASS.
PER_SECTION = _re(r"section by section|section-by-section"
                  r"|each reader-facing section|for each one")
COVERAGE = _re(r"\bevidence\b|\bcoverage\b")
PASS_GATE = _re(r"\bpass\b")
COVERAGE_GATE = _re(r"coverage statement|evidence position")

# Rule D': and coverage is a statement of fact, not a bar every section
# must clear. This one must NOT fire on the shipped text.
EVERY_SECTION = _re(r"\b(every|each|all|any|no)\b[^.;:]{0,60}\bsections?\b")
DEMANDED = _re(r"must (have|carry|supply|be supported|rest on)"
               r"|requires evidence|may not pass|cannot pass|no section may")
NO_EVIDENCE = _re(r"no citable evidence|no evidence")
LEGITIMATE = _re(r"legitimate")

# Rule E: a lane saves its result as the sweep proceeds.
SAVES = _re(r"\b(writ|sav|persist)\w*")
RESULT_FILE = _re(r"result file|result you hold|result path"
                  r"|path the parent driver gave you")
AS_YOU_GO = _re(r"as the sweep proceeds|each time|so far|early and often"
                r"|as .{0,30}(settled|established)"
                r"|rather than .{0,60}(the end|at the end)")


def retrieval_is_out_of_scope(text: str) -> list[str]:
    return _hits(text, RETRIEVAL, OUT_OF_SCOPE)


def missing_evidence_is_an_inadequate_brief(text: str) -> list[str]:
    return _hits(text, NEEDS, EVIDENCE, BRIEF, INADEQUACY)


def restatement_inherits_evidence_state(text: str) -> list[str]:
    return _hits(text, SHORT_FORM, EVIDENCE_STATE)


def certifies_coverage_per_section(text: str) -> list[str]:
    return _hits(text, PER_SECTION, COVERAGE)


def gates_pass_on_coverage(text: str) -> list[str]:
    return _hits(text, PASS_GATE, COVERAGE_GATE)


def demands_evidence_in_every_section(text: str) -> list[str]:
    return _hits(text, EVERY_SECTION, DEMANDED)


def admits_a_bounded_negative(text: str) -> list[str]:
    return _hits(text, NO_EVIDENCE, LEGITIMATE)


def saves_as_it_goes(text: str) -> list[str]:
    return _hits(text, SAVES, RESULT_FILE, AS_YOU_GO)


def fragment(name: str) -> str:
    return (FRAGMENTS / "propers" / f"{name}.md").read_text(encoding="utf-8")


class MatcherTests(unittest.TestCase):
    """Each rule is proved to discriminate before it is used to assert."""

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
        for label, rule in (
                ("retrieval-out-of-scope", retrieval_is_out_of_scope),
                ("missing-evidence-is-inadequacy",
                 missing_evidence_is_an_inadequate_brief),
                ("short-form-inheritance", restatement_inherits_evidence_state),
                ("per-section-coverage", certifies_coverage_per_section),
                ("pass-gated-on-coverage", gates_pass_on_coverage),
                ("bounded-negative-admitted", admits_a_bounded_negative),
                ("saves-as-it-goes", saves_as_it_goes),
                ("demands-evidence-everywhere",
                 demands_evidence_in_every_section)):
            with self.subTest(rule=label):
                self.assertEqual(rule(""), [])
                self.assertEqual(rule("The propers are appointed texts."), [])

    def test_the_blocked_rules_reject_the_contract_they_sharpened(self):
        self.assert_rejects(
            retrieval_is_out_of_scope,
            [PRE_CHANGE_BLOCKED_CONTRACT,
             "Return BLOCKED when the brief is unsuitable to author from."],
            "retrieval-out-of-scope")
        self.assert_rejects(
            missing_evidence_is_an_inadequate_brief,
            [PRE_CHANGE_BLOCKED_CONTRACT,
             # The reading that cost the run: a gap the author closes itself.
             "Where the brief lacks the evidence a section needs, supply it "
             "from the source library and cite what you used."],
            "missing-evidence-is-inadequacy")

    def test_the_blocked_rules_accept_the_contract_reworded(self):
        self.assert_accepts(
            retrieval_is_out_of_scope,
            ["Retrieving evidence is out of scope for this stage.",
             "Acquiring a source is out of scope here, whatever the source."],
            "retrieval-out-of-scope")
        self.assert_accepts(
            missing_evidence_is_an_inadequate_brief,
            ["A brief that lacks evidence you need is an insufficient brief.",
             "If you need a source the brief does not carry, its evidence "
             "base is inadequate."],
            "missing-evidence-is-inadequacy")

    def test_the_short_form_rule_rejects_what_stood_before_it(self):
        self.assert_rejects(
            restatement_inherits_evidence_state,
            [PRE_CHANGE_SHORT_FORM_NEIGHBOURHOOD,
             # A short-form instruction that says nothing about evidence: the
             # state the document was in when it dropped five qualifications.
             "Keep `The Propers: Themes and Movement` tight: it restates the "
             "commentary's argument across exactly two pages."],
            "short-form-inheritance")
        self.assert_accepts(
            restatement_inherits_evidence_state,
            ["A restatement carries the evidence state of what it restates.",
             "If it is an unverified lead at length it is a lead in the "
             "short form."],
            "short-form-inheritance")

    def test_the_coverage_rules_reject_what_stood_before_them(self):
        self.assert_rejects(
            certifies_coverage_per_section,
            [PRE_CHANGE_SYNTHESIS_COVERAGE,
             "Name the evidence gaps the brief leaves."],
            "per-section-coverage")
        self.assert_rejects(
            gates_pass_on_coverage,
            [PRE_CHANGE_SYNTHESIS_COVERAGE], "pass-gated-on-coverage")
        self.assert_accepts(
            certifies_coverage_per_section,
            ["State, section by section, whether the brief supplies that "
             "section's evidence."], "per-section-coverage")

    def test_the_quality_bar_rule_fires_on_a_quality_bar(self):
        """The control that keeps Change 3 from becoming what it must not be.

        A coverage certificate says what is there. Any of these would turn
        it into a requirement that every section have evidence, which would
        make a bounded negative — a real and publishable research result —
        into a blocker.
        """
        self.assert_accepts(
            demands_evidence_in_every_section,
            ["Every reader-facing section must have citable evidence before "
             "you may PASS.",
             "You may not pass while any section lacks evidence.",
             "Each reader-facing section must rest on evidence in the brief.",
             "No section may go without a source."],
            "demands-evidence-everywhere")
        self.assert_rejects(
            demands_evidence_in_every_section,
            ["Name every section whose evidence the brief does not supply.",
             "A section for which no citable evidence exists is a legitimate "
             "outcome and passes."],
            "demands-evidence-everywhere")

    def test_the_persistence_rule_rejects_saving_once_at_the_end(self):
        self.assert_rejects(
            saves_as_it_goes,
            [PRE_CHANGE_LANE_RESULT,
             # Exactly the behaviour that lost six lanes.
             "Write your findings into the result file when your sweep is "
             "complete."],
            "saves-as-it-goes")
        self.assert_accepts(
            saves_as_it_goes,
            ["Save to your result file as each finding is established.",
             "Write the result you hold so far to disk each time a finding "
             "is settled."],
            "saves-as-it-goes")


class FragmentTests(unittest.TestCase):
    """The rules, in the fragment sources that carry them."""

    def test_the_author_names_a_missing_evidence_base_as_inadequacy(self):
        text = fragment(AUTHOR)
        self.assertIn("BLOCKED", text)
        self.assertTrue(
            missing_evidence_is_an_inadequate_brief(text),
            "the author must be told that needing evidence the brief does "
            "not carry is itself an inadequate brief")

    def test_the_author_is_told_retrieval_is_out_of_scope(self):
        text = fragment(AUTHOR)
        self.assertTrue(retrieval_is_out_of_scope(text))
        self.assertRegex(text, SOURCE_BLIND,
                         "the scope must not widen because a source is easy "
                         "to reach; that is how a restricted source and an "
                         "unheld volume got cited")

    def test_the_author_states_the_short_form_inheritance_rule(self):
        self.assertTrue(restatement_inherits_evidence_state(fragment(AUTHOR)))

    def test_the_synthesis_certifies_coverage_and_gates_pass_on_it(self):
        text = fragment(SYNTHESIS)
        self.assertTrue(certifies_coverage_per_section(text))
        self.assertTrue(gates_pass_on_coverage(text))
        self.assertIn("Reader-Facing Order", text,
                      "the sections certified must be the profile's, not a "
                      "list this fragment invents and lets drift")

    def test_the_coverage_certificate_is_not_a_quality_bar(self):
        """Positive control: a bounded negative is a legitimate PASS."""
        text = fragment(SYNTHESIS)
        self.assertEqual(
            demands_evidence_in_every_section(text), [],
            "coverage is a statement of fact; requiring evidence in every "
            "section would make a bounded negative a blocker")
        self.assertTrue(
            admits_a_bounded_negative(text),
            "a section with no citable evidence must be named a legitimate "
            "outcome, not left for the reader of this fragment to guess")

    def test_the_shared_research_fragment_carries_the_persistence_rule(self):
        """One instruction, in the fragment every lane packet carries.

        `propers/research.md` is a stage fragment of `research`, so it is
        compiled into all seven lane packets. Saying this once there beats
        seven copies that can drift apart.
        """
        self.assertTrue(saves_as_it_goes(fragment("research")))

    def test_no_lane_fragment_repeats_the_persistence_rule(self):
        for lane in RESEARCH_LANES:
            with self.subTest(lane=lane):
                text = (FRAGMENTS / "propers" / "lanes"
                        / f"research-{lane}.md").read_text(encoding="utf-8")
                self.assertEqual(
                    saves_as_it_goes(text), [],
                    "the rule belongs once in the shared stage fragment; a "
                    "seventh copy here is a seventh thing to keep in step")

    def test_the_reviser_is_wired_to_the_author_rules(self):
        """`content-revision` inherits by loading the author fragment."""
        stages = {s["id"]: s for s in workflow_json()["stages"]}
        self.assertIn(f"propers/{AUTHOR}.md", stages[REVISER]["fragments"],
                      "the reviser must keep loading the author fragment, or "
                      "a revision may drop what authoring was told")


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

    def test_the_author_packet_carries_the_sharpened_blocked_contract(self):
        author = self.packets[AUTHOR]
        self.assertIn("BLOCKED", author)
        self.assertTrue(missing_evidence_is_an_inadequate_brief(author))
        self.assertTrue(retrieval_is_out_of_scope(author))
        self.assertRegex(author, SOURCE_BLIND)

    def test_the_author_packet_carries_the_short_form_rule(self):
        self.assertTrue(
            restatement_inherits_evidence_state(self.packets[AUTHOR]))

    def test_the_rules_are_not_in_every_packet(self):
        """A matcher that fires everywhere proves nothing where it matters."""
        for stage in ("source-audit", "build-artifacts", "generate-web"):
            with self.subTest(stage=stage):
                text = self.packets[stage]
                self.assertEqual(
                    missing_evidence_is_an_inadequate_brief(text), [],
                    "the author's BLOCKED contract is reaching a packet that "
                    "never had it; the rule is matching common boilerplate")
                self.assertEqual(saves_as_it_goes(text), [])

    def test_the_synthesis_packet_requires_coverage_before_pass(self):
        text = self.packets[SYNTHESIS]
        self.assertTrue(certifies_coverage_per_section(text))
        self.assertTrue(gates_pass_on_coverage(text))

    def test_the_synthesis_packet_still_admits_a_bounded_negative(self):
        text = self.packets[SYNTHESIS]
        self.assertEqual(demands_evidence_in_every_section(text), [])
        self.assertTrue(admits_a_bounded_negative(text))

    def test_every_research_lane_packet_saves_as_it_goes(self):
        for lane in RESEARCH_LANES:
            with self.subTest(lane=lane):
                text = self.packets[f"research/{lane}"]
                self.assertTrue(
                    saves_as_it_goes(text),
                    "an interrupted lane must leave partial evidence on disk")
                self.assertRegex(
                    text, _re(r"interrupted"),
                    "the lane is told why it saves early: the run has lost "
                    "lanes at the final serialisation")

    def test_the_reviser_packet_inherits_both_author_rules(self):
        text = self.packets[REVISER]
        self.assertTrue(missing_evidence_is_an_inadequate_brief(text))
        self.assertTrue(retrieval_is_out_of_scope(text))
        self.assertTrue(restatement_inherits_evidence_state(text))


if __name__ == "__main__":
    unittest.main()
