#!/usr/bin/env python3
"""Online citations survive the research-to-author handoff with one owner.

Run ``dae51f4a7715c7f9`` proved two distinct contract failures. Its
``cultural-afterlife`` result held the exact titles and stable URLs for the
selected witnesses, but synthesis reduced them to generic labels in the
immutable brief. Content evaluation then combined missing brief evidence and
leaf omissions into one authoring finding while asserting that the brief held
the URLs. The author was forbidden to retrieve around the brief and correctly
blocked.

These tests hold the repair in the fragment sources and in the bytes workers
are handed. Each matcher is also checked against the pre-v21 wording, so a
matcher that accepts the old contract cannot make the regression pass.
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
    PropersCase,
    workflow_json,
)

CULTURAL = "research-cultural-afterlife"
SYNTHESIS = "research-synthesis"
EVALUATION = "content-evaluation"
CITATION = "content-citation-integrity"

PRE_V21_CULTURAL = """
Verify every verbal link and later context in a primary source or reliable
edition. Describe an echo as an echo unless dependence is documented, keep
protected excerpts brief, and treat quote aggregators and attribution sites
as leads only.
"""

PRE_V21_SYNTHESIS = """
Carry each selected candidate's evidence through as that lane recorded it:
both texts and loci, relationship strength, wording check, context,
translation and rights status, cultural payoff, limiting qualification, and
material negative results. You select; you do not go looking.
"""

PRE_V21_OWNERSHIP = """
`authoring` — is the brief adequate, and the leaf departing from it? The
prose, the structure, or the use of citations in the canonical leaf is
defective while the brief it was written from is right.
"""


def sentences(text: str) -> list[str]:
    flat = " ".join(text.split())
    return [part for part in re.split(r"(?<=[.:;?])\s+", flat) if part]


def _re(pattern: str) -> re.Pattern:
    return re.compile(pattern, re.IGNORECASE)


def _hits(text: str, *patterns: re.Pattern) -> list[str]:
    parts = sentences(text)
    found = []
    for index, sentence in enumerate(parts):
        windows = [sentence]
        if index + 1 < len(parts):
            windows.append(sentence + " " + parts[index + 1])
        if any(all(pattern.search(window) for pattern in patterns)
               for window in windows):
            found.append(sentence)
    return found


TITLE = _re(r"exact (page or work )?title")
RESPONSIBLE_PARTY = _re(r"creator or institution")
STABLE_URL = _re(r"stable (public )?url")
ACCESS_DATE = _re(r"access date")
EXACT_LOCUS = _re(r"exact .{0,45}locus")
SCOPE = _re(r"research/scope\.md|\bbrief\b")
WRITE = _re(r"write|carry through|preserve")
BEFORE_PASS = _re(r"before `?pass`?")
COMPARE = _re(r"compare")
REQUIRED_RESULT = _re(r"required_result")
VERIFY_PRESENT = _re(r"verify|must actually be present")
AUTHORING = _re(r"authoring")
SPLIT = _re(r"split|separately")
DIFFERENT_OWNERS = _re(r"different owners|one repair owner|mixed")
MISSING = _re(r"missing|absent")
RESEARCH = _re(r"research")


def complete_online_bundle(text: str) -> list[str]:
    return _hits(text, TITLE, RESPONSIBLE_PARTY, STABLE_URL, ACCESS_DATE,
                 EXACT_LOCUS)


def writes_bundle_to_scope(text: str) -> list[str]:
    return _hits(text, SCOPE, WRITE, STABLE_URL)


def compares_bundle_before_pass(text: str) -> list[str]:
    return _hits(text, BEFORE_PASS, COMPARE)


def verifies_requested_values_before_authoring(text: str) -> list[str]:
    return _hits(text, REQUIRED_RESULT, VERIFY_PRESENT, SCOPE, AUTHORING)


def splits_mixed_owners(text: str) -> list[str]:
    return _hits(text, SPLIT, DIFFERENT_OWNERS)


def routes_absent_values_to_research(text: str) -> list[str]:
    return _hits(text, MISSING, SCOPE, RESEARCH)


def fragment(name: str) -> str:
    return (FRAGMENTS / "propers" / f"{name}.md").read_text(
        encoding="utf-8")


def lane_fragment(name: str) -> str:
    return (FRAGMENTS / "propers" / "lanes" / f"{name}.md").read_text(
        encoding="utf-8")


class MatcherTests(unittest.TestCase):
    def test_no_matcher_fires_on_nothing(self):
        for rule in (complete_online_bundle, writes_bundle_to_scope,
                     compares_bundle_before_pass,
                     verifies_requested_values_before_authoring,
                     splits_mixed_owners, routes_absent_values_to_research):
            with self.subTest(rule=rule.__name__):
                self.assertEqual(rule(""), [])
                self.assertEqual(rule("The brief cites the proper."), [])

    def test_matchers_reject_the_pre_v21_contract(self):
        samples = (PRE_V21_CULTURAL, PRE_V21_SYNTHESIS,
                   PRE_V21_OWNERSHIP)
        for rule in (complete_online_bundle, writes_bundle_to_scope,
                     compares_bundle_before_pass,
                     verifies_requested_values_before_authoring,
                     splits_mixed_owners, routes_absent_values_to_research):
            for sample in samples:
                with self.subTest(rule=rule.__name__, sample=sample[:30]):
                    self.assertEqual(rule(sample), [])

    def test_matchers_accept_reworded_rules(self):
        samples = {
            complete_online_bundle:
                "Record the exact title, creator or institution, stable URL, "
                "access date, and exact page locus.",
            writes_bundle_to_scope:
                "Preserve the stable URL in research/scope.md.",
            compares_bundle_before_pass:
                "Before PASS, compare the bundle with the finding.",
            verifies_requested_values_before_authoring:
                "Inspect required_result and verify every requested value is "
                "present in the brief before naming authoring.",
            splits_mixed_owners:
                "Split a mixed defect between different owners.",
            routes_absent_values_to_research:
                "If a value is missing from the brief, route it to research.",
        }
        for rule, sample in samples.items():
            with self.subTest(rule=rule.__name__):
                self.assertTrue(rule(sample))


class FragmentTests(unittest.TestCase):
    def test_cultural_lane_returns_a_complete_online_bundle(self):
        self.assertTrue(complete_online_bundle(lane_fragment(CULTURAL)))

    def test_synthesis_preserves_and_checks_the_bundle(self):
        text = fragment(SYNTHESIS)
        self.assertTrue(complete_online_bundle(text))
        self.assertTrue(writes_bundle_to_scope(text))
        self.assertTrue(compares_bundle_before_pass(text))

    def test_evaluation_proves_authoring_owns_the_requested_repair(self):
        text = fragment(EVALUATION)
        self.assertTrue(verifies_requested_values_before_authoring(text))
        self.assertTrue(splits_mixed_owners(text))
        self.assertTrue(routes_absent_values_to_research(text))

    def test_citation_lane_applies_the_ownership_rule(self):
        text = lane_fragment(CITATION)
        self.assertTrue(splits_mixed_owners(text))
        self.assertTrue(routes_absent_values_to_research(text))

    def test_contract_change_bumps_the_workflow(self):
        """The pipeline and both manuals name the same version.

        The number moves whenever the contract does -- v22 raised the
        content-evaluation repeat budget for its three-owner route, v23 added
        the retrieval receipt, the `source-registration` stage, and the
        budget's owner-change rule -- and what this guards is that the manuals
        move with it, whatever the number now is.
        """
        version = workflow_json()["version"]
        self.assertGreaterEqual(version, 21, "the v21 contract still holds")
        for path in (ROOT / "workflows" / "ARCHITECTURE.md",
                     ROOT / "workflows" / "OPERATOR.md"):
            text = path.read_text(encoding="utf-8")
            self.assertIn(f"workflow is at version {version}", text)


class EmittedPacketTests(PropersCase):
    """The rules survive assembly into the actual worker packets."""

    def setUp(self):
        super().setUp()
        run_id, _ = self.advance_to("research")
        workflow = self.engine.load_workflow("proper")
        state = self.engine.load_state(run_id)
        self.packets = {}
        for stage in workflow["stages"]:
            compiled = self.engine._compile_stage_packets(
                workflow, stage, state, self.engine.run_dir(run_id), [])
            self.packets[stage["id"]] = compiled["bytes"].decode("utf-8")
            for lane in compiled.get("lanes", []):
                self.packets[f"{stage['id']}/{lane['lane']}"] = (
                    lane["bytes"].decode("utf-8"))

    def test_research_packets_carry_the_lossless_handoff(self):
        self.assertTrue(complete_online_bundle(
            self.packets["research/cultural-afterlife"]))
        self.assertTrue(writes_bundle_to_scope(self.packets[SYNTHESIS]))
        self.assertTrue(compares_bundle_before_pass(self.packets[SYNTHESIS]))

    def test_citation_packet_carries_the_repair_discriminator(self):
        text = self.packets["content-evaluation/citation-integrity"]
        self.assertTrue(verifies_requested_values_before_authoring(text))
        self.assertTrue(splits_mixed_owners(text))
        self.assertTrue(routes_absent_values_to_research(text))


if __name__ == "__main__":
    unittest.main()
