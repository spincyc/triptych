#!/usr/bin/env python3
"""Two owners, one reviser: every finding the reviser will repair is its to report.

`synthesis-evaluation` in both propers pipelines routes two owners to the same
stage: a `derivation` defect (the companion misstates the canonical edition)
and a `seam` defect (a clause true in one edition and false in the other) both
go to `synthesis-revision`. The route is chosen by declaration order, so a
round carrying both kinds takes the `derivation` route, and the engine
forwarded only the findings naming the winning target. The seam findings
still reached the reviser, but as `CARRIED_FINDINGS`. A carried finding is
owed no `finding_dispositions` entry, and where a reviser reports, the repeat
budget reads nothing but those dispositions. A seam repair that failed round
after round was therefore invisible to the budget, and the runs it happened
to stopped on their novelty or absolute ceilings. A 10 September cold review
of `proper-finish` named this as item 4.1; the review is preserved under
`workflows/reviews/claude-loop-recovery-2026-09-18/`.

These tests hold the repair: a finding travels as a forwarded finding whenever
its own route leads to the stage the winning route chose, and a finding for an
owner reached by a different transition still does not travel.
"""
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))

from _workflow import (  # noqa: E402
    CHANGES_REQUIRED,
    NOT_REPAIRED,
    PASS,
    REPAIR_ROUTES,
    REPAIR_TARGET,
    REPAIRED,
    WorkflowEngine,
    WorkflowError,
    _repair_route,
)

EVALUATOR = "synthesis-evaluation"
REVISER = "synthesis-revision"


def pipeline(name: str) -> dict:
    return json.loads(
        (ROOT / "workflows" / "pipelines" / f"{name}.json")
        .read_text(encoding="utf-8"))


def stage_of(workflow: dict, stage_id: str) -> dict:
    return next(s for s in workflow["stages"] if s["id"] == stage_id)


def blocking(finding_id: str, target: str) -> dict:
    return {
        "id": finding_id, "severity": "blocking", "location": "page 3",
        "problem": "a defect", "required_result": "repair it",
        "repair_target": target,
    }


MIXED = {
    "stage": EVALUATOR, "iteration": 0, "disposition": CHANGES_REQUIRED,
    "summary": "derivation and seam defects in one round",
    "findings": [
        blocking("SYN-DER-001", "derivation"),
        blocking("SYN-SEAM-001", "seam"),
        blocking("SYN-SEAM-002", "seam"),
        {"id": "SYN-ADV-001", "severity": "advisory", "location": "page 4",
         "problem": "a nicety", "required_result": "consider it"},
    ],
}


class SharedReviserTests(unittest.TestCase):
    """The two propers pipelines that route two owners to one reviser."""

    def setUp(self):
        self.engine = WorkflowEngine(ROOT, ROOT / "workflows")

    def test_both_owners_share_the_one_reviser(self):
        for name in ("proper", "proper-finish"):
            with self.subTest(pipeline=name):
                routes = stage_of(pipeline(name), EVALUATOR)[REPAIR_ROUTES]
                self.assertEqual(
                    {r[REPAIR_TARGET]: r["transition"] for r in routes},
                    {"derivation": REVISER, "seam": REVISER})

    def test_a_mixed_round_forwards_the_seam_findings_too(self):
        for name in ("proper", "proper-finish"):
            with self.subTest(pipeline=name):
                stage = stage_of(pipeline(name), EVALUATOR)
                self.assertEqual(
                    _repair_route(stage, MIXED)[REPAIR_TARGET], "derivation",
                    "declaration order still chooses the derivation route")
                forwarded = self.engine._extract_prior_findings(MIXED, stage)
                self.assertEqual(
                    sorted(f["id"] for f in forwarded),
                    ["SYN-DER-001", "SYN-SEAM-001", "SYN-SEAM-002"],
                    "every blocking finding bound for the reviser is "
                    "forwarded, and the advisory is not")

    def test_a_forwarded_seam_finding_is_not_also_carried(self):
        for name in ("proper", "proper-finish"):
            with self.subTest(pipeline=name):
                workflow = pipeline(name)
                stage = stage_of(workflow, EVALUATOR)
                forwarded = self.engine._extract_prior_findings(MIXED, stage)
                state = {"result_hashes": [{
                    "stage": EVALUATOR, "iteration": 0,
                    "disposition": CHANGES_REQUIRED,
                    "path": "unused", "hash": "unused"}]}
                carried = self.engine._carried_findings(
                    "unused", workflow, state, stage_of(workflow, REVISER),
                    forwarded, fresh=MIXED)
                self.assertEqual(carried, [])

    def test_the_reviser_owes_a_disposition_for_each_seam_finding(self):
        stage = stage_of(pipeline("proper-finish"), EVALUATOR)
        reviser = stage_of(pipeline("proper-finish"), REVISER)
        self.assertTrue(reviser.get("reports_repairs"))
        forwarded = self.engine._extract_prior_findings(MIXED, stage)
        ids = sorted({f["id"] for f in forwarded})

        def state():
            # Exactly what `advance` records on the transition to the reviser.
            return {"findings_forwarded_by": {REVISER: EVALUATOR},
                    "findings_forwarded_ids": {REVISER: ids}}

        silent_on_seam = {
            "stage": REVISER, "iteration": 0, "disposition": PASS,
            "summary": "repaired the derivation defect",
            "finding_dispositions": [
                {"id": "SYN-DER-001", "outcome": REPAIRED}],
        }
        with self.assertRaisesRegex(WorkflowError, "SYN-SEAM-001"):
            self.engine._record_repair_outcomes(
                state(), reviser, silent_on_seam)

        reported = dict(silent_on_seam, finding_dispositions=[
            {"id": "SYN-DER-001", "outcome": REPAIRED},
            {"id": "SYN-SEAM-001", "outcome": NOT_REPAIRED,
             "note": "the clause is shared and cannot be split here"},
            {"id": "SYN-SEAM-002", "outcome": REPAIRED},
        ])
        recorded = state()
        self.engine._record_repair_outcomes(recorded, reviser, reported)
        self.assertEqual(recorded["unrepaired_for"][EVALUATOR],
                         ["SYN-SEAM-001"],
                         "a failed seam repair now reaches the repeat budget")

    def test_a_finding_for_another_transition_still_does_not_travel(self):
        stage = {
            "id": "an-evaluator", "type": "evaluator",
            REPAIR_ROUTES: [
                {"repair_target": "research", "transition": "research"},
                {"repair_target": "derivation", "transition": REVISER},
                {"repair_target": "seam", "transition": REVISER},
            ],
        }
        result = dict(MIXED, findings=MIXED["findings"] + [
            blocking("SYN-RES-001", "research")])
        forwarded = self.engine._extract_prior_findings(result, stage)
        self.assertEqual([f["id"] for f in forwarded], ["SYN-RES-001"],
                         "the research route wins, and carries only its own")

    def test_no_proper_study_route_shares_a_reviser(self):
        """The successor is untouched: each owner there has its own stage."""
        for stage in pipeline("proper-study")["stages"]:
            transitions = [r["transition"]
                           for r in stage.get(REPAIR_ROUTES, [])]
            with self.subTest(stage=stage["id"]):
                self.assertEqual(len(transitions), len(set(transitions)))


if __name__ == "__main__":
    unittest.main()
