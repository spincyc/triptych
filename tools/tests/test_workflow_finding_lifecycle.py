#!/usr/bin/env python3
"""What becomes of a finding nobody was routed to, and one nobody can repair.

Two production runs driven to completion left three defects in the same place:
the space between a finding being raised and somebody acting on it.

Run b68cca80edb75854 raised eight blocking findings at its first content
evaluation. One named `brief`, seven named `authoring`. Declaration order sent
the run to `research-synthesis`, which corrected the brief in thirty-four
minutes, and `author-proper` then re-authored the whole leaf from a packet
whose `PRIOR_FINDINGS` was `[]` — the seven findings against the document it
was rewriting had reached nobody. The next evaluation spent five lanes
rediscovering one of them.

The same run's `profile-conformance` lane found that the governing profile
states its macro-order twice and incompatibly, so that no leaf can satisfy
both. It filed the finding advisory, wrote in the finding's own prose "no
repair_target, because none of research, brief or authoring owns guidance",
and restated it verbatim at every iteration. Nothing outlived the run to act
on it.

And the run then blocked at three consecutive failures with four of five lanes
passing and one finding standing, which the lane that raised it recorded as its
own miss at the earlier iterations rather than a regression. The budget could
not tell a stage that was looping from one that was working.

These tests hold the three answers: a finding waits for its owner, a defect no
stage owns leaves the run as an escalation, and the budget charges repetition.
"""
import copy
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from _workflow import (  # noqa: E402
    CHANGES_REQUIRED,
    ESCALATION,
    PASS,
    REPAIRS,
    WorkflowEngine,
    WorkflowError,
    _validate_workflow,
)
from test_workflow_repair_routing import (  # noqa: E402
    AUTHORING,
    BRIEF,
    RESEARCH,
    SYNTHESIS,
    RoutingCase,
    blocking,
)
from test_workflow_research_fanout import (  # noqa: E402
    CONTENT_LANES,
    workflow_json,
)

EVALUATION = "content-evaluation"
REGISTRATION = "source-registration"
AUTHOR = "author-proper"
REVISION = "content-revision"
PREFLIGHT = "content-preflight"

# The shape of the run this file is about: one `brief` defect, raised beside
# several `authoring` ones, wins the route on declaration order.
BRIEF_AND_AUTHORING = {
    CONTENT_LANES[2]: [blocking("CON-SYN-001", BRIEF, "wrong locus")],
    CONTENT_LANES[0]: [blocking("CON-EVI-001", AUTHORING, "unattributed"),
                       blocking("CON-EVI-002", AUTHORING, "unattributed")],
    CONTENT_LANES[3]: [blocking("CON-CIT-016", AUTHORING, "no edition")],
}


def escalation(finding_id: str, target: str = "guidance/liturgy/x.md 117"):
    """A defect in an artifact no stage of this workflow may write."""
    return {
        "id": finding_id, "severity": ESCALATION, "location": "the profile",
        "problem": "the profile states its macro-order twice, incompatibly",
        "required_result": "the maintainer reconciles the two statements",
        "escalated_to": target,
    }


def headers(packet_text: str, field: str) -> list[dict]:
    prefix = f"{field}: "
    line = next(l for l in packet_text.splitlines() if l.startswith(prefix))
    return json.loads(line[len(prefix):])


class SynthesisToAuthorMixin:
    """Both classes below drive the brief's writer through to the author.

    v22 put `source-registration` between the two, so the step that used to be
    one advance is two. Shared here rather than repeated, because the next
    stage inserted into that chain should break one helper and not eleven
    call sites.
    """

    def pass_synthesis_to_author(self, run_id: str) -> None:
        """Advance the brief's writer and stop with the author waiting.

        v22 put `source-registration` between the two. It owns no repair
        target, so it is carried nothing and it answers nothing: the findings
        the route passed over are still owed to the author, and are computed
        when the author's packet is compiled.
        """
        self.engine.advance(
            run_id, result_path=self.worker_pass(run_id, SYNTHESIS))
        if self.engine.load_state(run_id)["current_stage"] == REGISTRATION:
            packet = self.engine.load_state(run_id)["packet_hashes"][-1]
            text = (ROOT / packet["path"]).read_text(encoding="utf-8")
            self.assertEqual(
                headers(text, "CARRIED_FINDINGS"), [],
                "registration repairs nothing, so it is told nothing")
            self.engine.advance(
                run_id, result_path=self.worker_pass(run_id, REGISTRATION))



class CarriedFindingTests(SynthesisToAuthorMixin, RoutingCase):
    """A finding reaches its owner, whoever won the route."""

    def ids_at(self, run_id: str, field: str) -> list[str]:
        packet = self.engine.load_state(run_id)["packet_hashes"][-1]
        text = (ROOT / packet["path"]).read_text(encoding="utf-8")
        return sorted(f["id"] for f in headers(text, field))

    def drive_the_b68_shape(self) -> str:
        """Reproduce the transition that lost seven findings."""
        run_id = self.drive_to(EVALUATION)
        out = self.engine.advance(run_id, lane_results=self.content_submissions(
            run_id, BRIEF_AND_AUTHORING))
        self.assertEqual(out["stage"], SYNTHESIS,
                         "declaration order still sends the run to the brief")
        return run_id

    def test_the_winning_route_still_carries_only_its_own_findings(self):
        """Routing is untouched: this is about who hears, not where it goes."""
        run_id = self.drive_the_b68_shape()
        self.assertEqual(self.ids_at(run_id, "PRIOR_FINDINGS"),
                         ["CON-SYN-001"])
        self.assertEqual(self.ids_at(run_id, "CARRIED_FINDINGS"), [],
                         "the brief's own finding travelled the route, so it "
                         "is not also carried")

    def test_the_author_hears_the_findings_the_route_passed_over(self):
        """The packet that was empty in b68cca80edb75854."""
        run_id = self.drive_the_b68_shape()
        self.pass_synthesis_to_author(run_id)
        self.assertEqual(self.engine.load_state(run_id)["current_stage"],
                         AUTHOR)
        self.assertEqual(
            self.ids_at(run_id, "PRIOR_FINDINGS"), [],
            "an evaluator's PASS still forwards nothing of its own")
        self.assertEqual(
            self.ids_at(run_id, "CARRIED_FINDINGS"),
            ["CON-CIT-016", "CON-EVI-001", "CON-EVI-002"],
            "every authoring finding the route passed over reaches the author")

    def test_a_carried_finding_is_the_evaluator_s_own_bytes(self):
        run_id = self.drive_the_b68_shape()
        self.pass_synthesis_to_author(run_id)
        packet = self.engine.load_state(run_id)["packet_hashes"][-1]
        text = (ROOT / packet["path"]).read_text(encoding="utf-8")
        carried = {f["id"]: f for f in headers(text, "CARRIED_FINDINGS")}
        self.assertEqual(
            carried["CON-EVI-001"],
            dict(blocking("CON-EVI-001", AUTHORING, "unattributed"),
                 lane=CONTENT_LANES[0]),
            "carried exactly as the join recorded it, lane tag and all")

    def test_delivery_is_once_and_to_whichever_owner_runs_first(self):
        """`author-proper` and `content-revision` both own `authoring`."""
        run_id = self.drive_the_b68_shape()
        self.pass_synthesis_to_author(run_id)
        self.assertEqual(len(self.ids_at(run_id, "CARRIED_FINDINGS")), 3)
        # The author answers. Its result is recorded, so the debt is paid.
        self.engine.advance(
            run_id, result_path=self.worker_pass(run_id, AUTHOR))
        self.assertEqual(self.engine.load_state(run_id)["current_stage"],
                         PREFLIGHT)
        self.assertEqual(
            self.ids_at(run_id, "CARRIED_FINDINGS"), [],
            "a gate owns no repair target, so nothing is carried to it")

    def test_the_fresh_evaluation_still_starts_clean(self):
        """Carrying findings forward must not leak into the evaluator."""
        run_id = self.drive_the_b68_shape()
        self.pass_synthesis_to_author(run_id)
        self.engine.advance(
            run_id, result_path=self.worker_pass(run_id, AUTHOR))
        self.engine.advance(run_id, run_gate=True)
        self.assertEqual(self.engine.load_state(run_id)["current_stage"],
                         EVALUATION)
        self.assertEqual(self.ids_at(run_id, "PRIOR_FINDINGS"), [])
        self.assertEqual(
            self.ids_at(run_id, "CARRIED_FINDINGS"), [],
            "an evaluator repairs nothing, so it is told nothing")

    def test_a_later_evaluation_supersedes_an_earlier_one_entirely(self):
        """Only the most recent result of an evaluator can still be owed."""
        run_id = self.drive_the_b68_shape()
        self.pass_synthesis_to_author(run_id)
        self.engine.advance(
            run_id, result_path=self.worker_pass(run_id, AUTHOR))
        self.engine.advance(run_id, run_gate=True)
        # A second evaluation, naming a brief defect and one new authoring one.
        out = self.engine.advance(run_id, lane_results=self.content_submissions(
            run_id, {
                CONTENT_LANES[2]: [blocking("CON-SYN-009", BRIEF, "still")],
                CONTENT_LANES[0]: [blocking("CON-EVI-050", AUTHORING, "new")],
            }))
        self.assertEqual(out["stage"], SYNTHESIS)
        self.pass_synthesis_to_author(run_id)
        self.assertEqual(
            self.ids_at(run_id, "CARRIED_FINDINGS"), ["CON-EVI-050"],
            "the first evaluation's findings are gone: the document was "
            "re-authored and judged again, and that judgment is the current "
            "one")

    def test_replay_recompiles_a_carried_packet_byte_for_byte(self):
        """Derived from the record, never consumed, or replay would drift."""
        run_id = self.drive_the_b68_shape()
        self.pass_synthesis_to_author(run_id)
        report = self.engine.replay(run_id)
        self.assertTrue(report["deterministic"],
                        f"replay diverged: {report}")
        self.assertEqual(report["recompiled_hash"],
                         report["last_recorded_hash"])

    def test_a_carried_finding_survives_a_second_replay(self):
        """Idempotent: reading it does not spend it."""
        run_id = self.drive_the_b68_shape()
        self.pass_synthesis_to_author(run_id)
        first = self.engine.replay(run_id)
        self.assertEqual(self.engine.replay(run_id), first)
        self.assertEqual(len(self.ids_at(run_id, "CARRIED_FINDINGS")), 3)


class TheRunThatShouldNotHaveBlockedTests(SynthesisToAuthorMixin, RoutingCase):
    """Run b68cca80edb75854's own blocking-finding history, replayed.

    Taken from that run's three `content-evaluation` results, by finding id:

        iteration 0   CON-EVI-001..004, CON-CIT-016, CON-CIT-017,
                      CON-PRO-001 (authoring), CON-SYN-001 (brief)
        iteration 1   CON-EVI-002
        iteration 2   CON-EVI-008

    Eight blocking findings, then one, then one. Iteration 1 repeated exactly
    one id and repaired the other seven. Iteration 2 repeated none: CON-EVI-008
    was a fourth instance of the rule behind CON-EVI-002, and the lane that
    raised it wrote into the finding that it was "my lane's miss at iterations
    0 and 1 and not a defect introduced by the CON-EVI-002 repair". The old
    budget counted three failures and blocked, with four of five lanes passing.
    """

    HISTORY = (
        {CONTENT_LANES[0]: ["CON-EVI-001", "CON-EVI-002", "CON-EVI-003",
                            "CON-EVI-004"],
         CONTENT_LANES[3]: ["CON-CIT-016", "CON-CIT-017"],
         CONTENT_LANES[4]: ["CON-PRO-001"]},
        {CONTENT_LANES[0]: ["CON-EVI-002"]},
        {CONTENT_LANES[0]: ["CON-EVI-008"]},
    )

    def evaluate(self, run_id: str, by_lane: dict) -> dict:
        return self.engine.advance(run_id, lane_results=self.content_submissions(
            run_id, {lane: [blocking(fid, AUTHORING) for fid in ids]
                     for lane, ids in by_lane.items()}))

    def test_the_run_survives_its_own_history(self):
        run_id = self.drive_to(EVALUATION)
        for iteration, by_lane in enumerate(self.HISTORY):
            with self.subTest(iteration=iteration):
                out = self.evaluate(run_id, by_lane)
                self.assertEqual(
                    out["stage"], REVISION,
                    f"iteration {iteration} ended the run; it should not have")
                self.engine.advance(
                    run_id, result_path=self.worker_pass(run_id, REVISION))
                self.engine.advance(run_id, run_gate=True)

        state = self.engine.load_state(run_id)
        self.assertEqual(state["current_stage"], EVALUATION,
                         "a fourth evaluation is reached, which is the whole "
                         "of the fix: the defects were shrinking")
        self.assertIsNone(state["disposition"])
        self.assertEqual(state["stage_failures"][EVALUATION], 3,
                         "three consecutive failures, as before")
        self.assertEqual(
            state["stage_repeats"][EVALUATION], 2,
            "the first, and the one repeating CON-EVI-002; the round that "
            "moved from CON-EVI-002 to CON-EVI-008 was new work")

    def test_the_same_history_would_have_blocked_before(self):
        """The old rule, stated as arithmetic, against the same three rounds.

        Not a test of dead code — a statement of what changed, so that a
        revert to counting failures is visible here and not only in a
        production run six hours in.
        """
        consecutive = len(self.HISTORY)
        legacy_limit = 3
        self.assertGreaterEqual(
            consecutive, legacy_limit,
            "counting failures, this history reached the limit exactly")
        declared = {s["id"]: s for s in workflow_json()["stages"]}[
            EVALUATION]["max_iterations"]
        self.assertGreater(
            declared, legacy_limit,
            "v22 separately widens the three-owner evaluation route")

    def test_the_authoring_findings_reach_an_author_at_the_first_round(self):
        """The other half: iteration 0's brief defect no longer loses them."""
        run_id = self.drive_to(EVALUATION)
        by_lane = {lane: [blocking(fid, AUTHORING) for fid in ids]
                   for lane, ids in self.HISTORY[0].items()}
        by_lane[CONTENT_LANES[2]] = [blocking("CON-SYN-001", BRIEF)]
        out = self.engine.advance(
            run_id, lane_results=self.content_submissions(run_id, by_lane))
        self.assertEqual(out["stage"], SYNTHESIS)
        self.pass_synthesis_to_author(run_id)
        packet = self.engine.load_state(run_id)["packet_hashes"][-1]
        text = (ROOT / packet["path"]).read_text(encoding="utf-8")
        self.assertEqual(
            sorted(f["id"] for f in headers(text, "CARRIED_FINDINGS")),
            ["CON-CIT-016", "CON-CIT-017", "CON-EVI-001", "CON-EVI-002",
             "CON-EVI-003", "CON-EVI-004", "CON-PRO-001"],
            "all seven, to the author that re-authored blind")


class MixedOwnerCitationBudgetTests(RoutingCase):
    """The three-owner route has room to dispatch its final owner.

    Run ce4ecd514b64d2f9 used two repeat-budget slots before a new citation
    finding entered the loop. Research supplied that finding's missing
    evidence; the next evaluation then assigned the remaining leaf repair to
    authoring under the same stable id. That fourth evaluation selected the
    right route, but v21's 3/3 ceiling blocked before emitting its packet.
    """

    def evaluate(self, run_id: str, findings_by_lane: dict) -> dict:
        return self.engine.advance(
            run_id,
            lane_results=self.content_submissions(run_id, findings_by_lane),
        )

    def return_from_research(self, run_id: str) -> None:
        """Drive the research route back to the evaluation.

        Driven by the workflow's own topology rather than a fixed list, so that
        a stage inserted into the chain -- as v23 inserted
        `source-registration` between the brief and the author -- does not stop
        this test exercising the round trip it is about.
        """
        self.engine.advance(
            run_id, lane_results=self.research_submissions(run_id))
        for _ in range(12):
            stage_id = self.engine.load_state(run_id)["current_stage"]
            if stage_id == EVALUATION:
                return
            self.pass_stage(run_id, stage_id)
        self.fail("the run never came back to the evaluation")

    def return_from_authoring(self, run_id: str) -> None:
        self.engine.advance(
            run_id, result_path=self.worker_pass(run_id, REVISION))
        self.engine.advance(run_id, run_gate=True)
        self.assertEqual(
            self.engine.load_state(run_id)["current_stage"], EVALUATION)

    def test_ce4_history_reaches_authoring_on_the_fourth_evaluation(self):
        run_id = self.drive_to(EVALUATION)

        # Evaluation 0: the initial failure spends the first repeat slot and
        # research wins over the authoring findings beside it.
        out = self.evaluate(run_id, {
            CONTENT_LANES[0]: [blocking("CON-EVI-001", RESEARCH)],
            CONTENT_LANES[3]: [blocking("CON-CIT-001", AUTHORING)],
            CONTENT_LANES[4]: [blocking("CON-PRO-001", AUTHORING)],
        })
        self.assertEqual(out["stage"], RESEARCH)
        self.return_from_research(run_id)

        # Evaluation 1: one standing authoring defect repeats, spending the
        # second slot, while the other findings are new work.
        out = self.evaluate(run_id, {
            CONTENT_LANES[0]: [blocking("CON-EVI-002", AUTHORING)],
            CONTENT_LANES[3]: [blocking("CON-CIT-002", AUTHORING)],
            CONTENT_LANES[4]: [blocking("CON-PRO-001", AUTHORING)],
        })
        self.assertEqual(out["stage"], REVISION)
        self.return_from_authoring(run_id)

        # Evaluation 2: CON-CIT-007 is new and correctly routes the missing
        # evidence to research; no previous id repeats in this round.
        out = self.evaluate(run_id, {
            CONTENT_LANES[3]: [
                blocking("CON-CIT-007", RESEARCH),
                blocking("CON-CIT-008", AUTHORING),
            ],
            CONTENT_LANES[4]: [blocking("CON-PRO-002", AUTHORING)],
        })
        self.assertEqual(out["stage"], RESEARCH)
        self.return_from_research(run_id)

        # Evaluation 3: the evidence now exists and the same citation defect
        # has progressed to its leaf repair. V21 blocked at this point. V22
        # must honor the newly selected route and give the finding to the
        # authoring owner, and does so by two independent margins since v23:
        # the widened budget, and the charge that is no longer made.
        out = self.evaluate(run_id, {
            CONTENT_LANES[3]: [blocking("CON-CIT-007", AUTHORING)],
        })
        self.assertEqual(out["stage"], REVISION)
        self.assertIsNone(out["disposition"])
        packet = Path(out["packet_abs_path"]).read_text(encoding="utf-8")
        self.assertEqual(
            [f["id"] for f in headers(packet, "PRIOR_FINDINGS")],
            ["CON-CIT-007"],
        )
        state = self.engine.load_state(run_id)
        self.assertEqual(state["stage_failures"][EVALUATION], 4)
        self.assertEqual(
            state["stage_repeats"][EVALUATION], 2,
            "three under v22, which charged CON-CIT-007's return even though "
            "it came back naming a different owner. v23 does not charge that, "
            "so this history spends the first failure of the streak and "
            "CON-PRO-001's genuine repeat, and nothing else")
        self.assertEqual(
            {s["id"]: s for s in workflow_json()["stages"]}
            [EVALUATION]["max_iterations"],
            4,
            "v22's widened ceiling is kept: the two fixes are independent, "
            "and a run that really does stop converging still has a bound")


class RepairOwnershipDeclarationTests(unittest.TestCase):
    """`repairs` is the reciprocal of `repair_routes`, and it is checked."""

    def test_the_propers_pipeline_declares_every_owner(self):
        stages = {s["id"]: s for s in workflow_json()["stages"]}
        self.assertEqual(stages[RESEARCH][REPAIRS], [RESEARCH])
        self.assertEqual(stages[SYNTHESIS][REPAIRS], [BRIEF])
        self.assertEqual(stages[REVISION][REPAIRS], [AUTHORING])
        self.assertEqual(
            stages[AUTHOR][REPAIRS], [AUTHORING],
            "the author owns authoring defects too, though no route points "
            "at it: after a brief repair it is the next stage to write the "
            "leaf, and it was the stage that re-authored blind")

    def test_every_route_points_at_a_stage_that_admits_to_owning_it(self):
        routes = [(stage["id"], route)
                  for stage in workflow_json()["stages"]
                  for route in stage.get("repair_routes") or []]
        self.assertTrue(routes)
        stages = {s["id"]: s for s in workflow_json()["stages"]}
        for owner, route in routes:
            with self.subTest(stage=owner, target=route["repair_target"]):
                self.assertIn(route["repair_target"],
                              stages[route["transition"]].get(REPAIRS, []))

    def test_a_route_to_a_stage_that_owns_nothing_is_refused_at_load(self):
        engine = WorkflowEngine(ROOT, ROOT / "workflows")
        workflow = copy.deepcopy(workflow_json())
        for stage in workflow["stages"]:
            if stage["id"] == SYNTHESIS:
                del stage[REPAIRS]
        with self.assertRaises(WorkflowError) as caught:
            engine._validate_repair_route_coverage(
                workflow, ROOT / "workflows" / "pipelines" / "proper.json")
        self.assertIn("does not declare", str(caught.exception))
        self.assertIn(BRIEF, str(caught.exception))

    def test_a_malformed_repairs_list_is_refused_at_load(self):
        path = ROOT / "workflows" / "pipelines" / "proper.json"
        for bad in ([], "authoring", [""], [AUTHORING, AUTHORING]):
            with self.subTest(repairs=bad):
                workflow = copy.deepcopy(workflow_json())
                for stage in workflow["stages"]:
                    if stage["id"] == REVISION:
                        stage[REPAIRS] = bad
                with self.assertRaises(WorkflowError):
                    _validate_workflow(workflow, path)


class EscalationTests(RoutingCase):
    """A defect no stage may repair leaves the run instead of dying in it."""

    def submissions(self, run_id, escalating: list, blocking_by_lane=None):
        """Lane results where the escalating lane still returns PASS.

        An escalation is not a failure of the lane's own criteria: the leaf
        satisfies them as well as anything could. The lane passes and files the
        escalation alongside, which is why an evaluation carrying nothing but
        escalations is a PASS and the run continues.
        """
        blocking_by_lane = blocking_by_lane or {}
        packet = self.engine.load_state(run_id)["packet_hashes"][-1]
        emitted = {e["lane"]: e for e in packet["lanes"]}
        pairs = []
        for lane in CONTENT_LANES:
            findings = list(blocking_by_lane.get(lane, []))
            if lane == CONTENT_LANES[4]:
                findings += escalating
            pairs.append((lane, self.write(f"esc-{lane}", {
                "stage": packet["stage"], "iteration": packet["iteration"],
                "lane": lane, "lane_packet_hash": emitted[lane]["hash"],
                "disposition": (CHANGES_REQUIRED
                                if blocking_by_lane.get(lane) else PASS),
                "summary": f"{lane} judged its criteria",
                "findings": findings,
            })))
        return pairs

    def test_an_escalation_does_not_block_a_run_whose_leaf_is_correct(self):
        run_id = self.drive_to(EVALUATION)
        out = self.engine.advance(
            run_id, lane_results=self.submissions(
                run_id, [escalation("CON-PRO-002")]))
        self.assertEqual(
            out["stage"], "build-artifacts",
            "the profile is wrong and the leaf is right, so the run goes on")
        self.assertIsNone(out["disposition"])

    def test_an_escalation_is_recorded_where_it_outlives_the_run(self):
        run_id = self.drive_to(EVALUATION)
        self.engine.advance(run_id, lane_results=self.submissions(
            run_id, [escalation("CON-PRO-002")]))
        ledger = self.engine.load_state(run_id)["escalations"]
        self.assertEqual(len(ledger), 1)
        self.assertEqual(ledger[0]["stage"], EVALUATION)
        self.assertEqual(ledger[0]["escalated_to"], "guidance/liturgy/x.md 117")
        self.assertEqual(ledger[0]["finding"]["id"], "CON-PRO-002")
        self.assertEqual(self.engine.status(run_id)["escalations"], ledger)

    def test_restating_an_escalation_does_not_multiply_it(self):
        """The lane restated the same defect at every iteration of the run."""
        run_id = self.drive_to(EVALUATION)
        self.engine.advance(run_id, lane_results=self.submissions(
            run_id, [escalation("CON-PRO-002")],
            {CONTENT_LANES[0]: [blocking("CON-EVI-001", AUTHORING)]}))
        self.engine.advance(
            run_id, result_path=self.worker_pass(run_id, REVISION))
        self.engine.advance(run_id, run_gate=True)
        self.engine.advance(run_id, lane_results=self.submissions(
            run_id,
            [escalation("CON-PRO-002",
                        "guidance/liturgy/x.md 117 and 204")]))
        ledger = self.engine.load_state(run_id)["escalations"]
        self.assertEqual(len(ledger), 1, "one defect, one slot")
        self.assertEqual(ledger[0]["escalated_to"],
                         "guidance/liturgy/x.md 117 and 204",
                         "the latest restatement is the one that is kept")

    def test_an_escalation_may_not_also_name_a_repair_owner(self):
        """Having no owner in this run is what makes it an escalation."""
        run_id = self.drive_to(EVALUATION)
        claiming = dict(escalation("CON-PRO-002"), repair_target=AUTHORING)
        with self.assertRaises(WorkflowError) as caught:
            self.engine.advance(
                run_id, lane_results=self.submissions(run_id, [claiming]))
        self.assertIn("escalation", str(caught.exception))
        self.assertIn("repair_target", str(caught.exception))

    def test_an_escalation_must_name_the_artifact_it_escalates_to(self):
        run_id = self.drive_to(EVALUATION)
        vague = {k: v for k, v in escalation("CON-PRO-002").items()
                 if k != "escalated_to"}
        with self.assertRaises(WorkflowError) as caught:
            self.engine.advance(
                run_id, lane_results=self.submissions(run_id, [vague]))
        self.assertIn("escalated_to", str(caught.exception))

    def test_an_escalation_is_not_forwarded_to_any_stage(self):
        """It is addressed to a maintainer, not to a worker."""
        run_id = self.drive_to(EVALUATION)
        out = self.engine.advance(run_id, lane_results=self.submissions(
            run_id, [escalation("CON-PRO-002")],
            {CONTENT_LANES[0]: [blocking("CON-EVI-001", AUTHORING)]}))
        self.assertEqual(out["stage"], REVISION)
        text = Path(out["packet_abs_path"]).read_text(encoding="utf-8")
        self.assertEqual([f["id"] for f in headers(text, "PRIOR_FINDINGS")],
                         ["CON-EVI-001"])
        self.assertEqual(headers(text, "CARRIED_FINDINGS"), [])
        self.assertNotIn("CON-PRO-002", text)

    def test_an_escalation_does_not_spend_the_iteration_budget(self):
        run_id = self.drive_to(EVALUATION)
        self.engine.advance(run_id, lane_results=self.submissions(
            run_id, [escalation("CON-PRO-002")]))
        state = self.engine.load_state(run_id)
        self.assertEqual(state["stage_failures"].get(EVALUATION, 0), 0)
        self.assertEqual(state["stage_repeats"].get(EVALUATION, 0), 0)

    def test_the_schema_admits_exactly_three_severities(self):
        schema = json.loads(
            (ROOT / "workflows" / "schema" / "content-evaluation-result.json")
            .read_text(encoding="utf-8"))
        self.assertEqual(schema["finding_enums"]["severity"],
                         ["blocking", ESCALATION, "advisory"])
        self.assertEqual(schema["escalation_finding_fields"], ["escalated_to"])
        self.assertEqual(
            schema["finding_enums"]["repair_target"],
            [RESEARCH, BRIEF, AUTHORING],
            "no fourth repair target: a target that routes nowhere would be "
            "the false choice the severity exists to replace")


class LaneFragmentDigestTests(unittest.TestCase):
    """A run is bound to the bytes of every fragment, lane fragments included.

    ARCHITECTURE.md claimed this before the code did. `workflow_source_digest`
    walked `stage["fragments"]` and never `execution.lanes[*].fragments`, so
    sixteen lane fragments — the most substantive instructions the propers
    pipeline has — could be rewritten under a live run without the digest
    moving.
    """

    def setUp(self):
        self.engine = WorkflowEngine(ROOT, ROOT / "workflows")
        self.workflow = self.engine.load_workflow("proper")

    def test_editing_a_lane_fragment_moves_the_digest(self):
        before = self.engine.workflow_source_digest(self.workflow)
        path = (ROOT / "workflows" / "fragments" / "propers" / "lanes"
                / "content-profile-conformance.md")
        original = path.read_bytes()
        try:
            path.write_bytes(original + b"\nan edit under a live run\n")
            during = self.engine.workflow_source_digest(self.workflow)
        finally:
            path.write_bytes(original)
        self.assertNotEqual(
            before, during,
            "a lane fragment is guidance a run is driven by; changing it "
            "mid-run must stop the run, as ARCHITECTURE.md says it does")
        self.assertEqual(before,
                         self.engine.workflow_source_digest(self.workflow))

    def test_every_lane_fragment_is_covered(self):
        """Not one of them: all sixteen, named from the workflow itself."""
        lane_fragments = sorted({
            fragment
            for stage in self.workflow["stages"]
            for lane in (stage.get("execution", {}).get("lanes") or [])
            for fragment in lane.get("fragments", [])
        })
        self.assertGreaterEqual(len(lane_fragments), 16)
        base = self.engine.workflow_source_digest(self.workflow)
        for name in lane_fragments:
            with self.subTest(fragment=name):
                path = ROOT / "workflows" / "fragments" / name
                original = path.read_bytes()
                try:
                    path.write_bytes(original + b"\n.\n")
                    self.assertNotEqual(
                        base, self.engine.workflow_source_digest(self.workflow),
                        f"{name} is outside the digest")
                finally:
                    path.write_bytes(original)


class CarriedFindingFragmentTests(unittest.TestCase):
    """The stages that receive the new header are told about it."""

    def fragment(self, name: str) -> str:
        return (ROOT / "workflows" / "fragments" / name).read_text(
            encoding="utf-8")

    def test_every_repairing_stage_s_fragment_names_the_header(self):
        stages = {s["id"]: s for s in workflow_json()["stages"]}
        for stage_id in (AUTHOR, REVISION, SYNTHESIS):
            with self.subTest(stage=stage_id):
                text = "".join(self.fragment(name)
                               for name in stages[stage_id]["fragments"])
                self.assertIn(
                    "CARRIED_FINDINGS", text,
                    f"{stage_id} owns a repair target, so it can be handed "
                    f"findings under this header and must be told what they "
                    f"are")

    def test_the_evaluator_no_longer_promises_rediscovery(self):
        """The old rationale for dropping a finding is now false."""
        text = self.fragment("propers/content-evaluation.md")
        self.assertNotIn("That is intended, not a loss", text)
        self.assertIn("CARRIED_FINDINGS", text)

    def test_the_evaluator_says_an_escalating_lane_still_passes(self):
        """Its criteria are met; the defect is in something else entirely."""
        text = " ".join(
            self.fragment("propers/content-evaluation.md").split())
        self.assertIn(
            "An escalation does not change your lane's disposition", text)
        self.assertIn("the lane returns `PASS`", text)

    def test_the_evaluator_teaches_the_escalation_severity(self):
        text = self.fragment("propers/content-evaluation.md")
        for phrase in ('"escalation"', "escalated_to",
                       "no stage of this workflow may write"):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, text)

    def test_the_evaluator_says_why_a_finding_id_is_load_bearing(self):
        text = " ".join(
            self.fragment("propers/content-evaluation.md").split())
        self.assertIn("reuse an id for the same unrepaired defect", text)


class PriorProductionCarryForwardTests(unittest.TestCase):
    """Re-seeding starts an empty run; one stage is placed to remember."""

    def setUp(self):
        self.text = (ROOT / "workflows" / "fragments" / "propers"
                     / "research-synthesis.md").read_text(encoding="utf-8")
        self.flat = " ".join(self.text.split())

    def test_the_brief_must_carry_a_prior_production_s_findings(self):
        self.assertIn("Prior-production carry-forward", self.text)
        self.assertIn("build/tpt-runs", self.text,
                      "the stage is told where a prior run's record is")
        self.assertIn("result_hashes", self.text)

    def test_an_absent_prior_production_must_still_be_stated(self):
        """Silence and an empty history must be distinguishable afterwards."""
        self.assertIn("say so in one line under that heading", self.flat)

    def test_the_carry_forward_is_a_condition_of_passing(self):
        self.assertIn(
            "Do not pass before the `Prior-production carry-forward` heading "
            "is in the brief", self.flat)

    def test_the_heading_is_written_into_the_brief_itself(self):
        """It has to land in `research/scope.md`, not only in a summary."""
        writes = self.flat.split("Write into `research/scope.md`:", 1)
        self.assertEqual(len(writes), 2, "the write list is still there")
        self.assertIn("`Prior-production carry-forward`", writes[1][:600])


if __name__ == "__main__":
    unittest.main()


class OwnerChangeIsNotARepeatTests(RoutingCase):
    """A defect that changes hands is converging, and must not be charged.

    Run ce4ecd514b64d2f9 (Proper 55, v21) blocked with four of five evaluation
    lanes passing and one finding standing. CON-CIT-007 was raised against the
    NABRE and Gadenz citations naming `research`, because the brief carried
    neither the target URLs nor the edition. Research retrieved them and wrote
    them into `research/scope.md`. The next evaluation raised CON-CIT-007
    again — correctly, and saying so in its own prose: "The evidence retrieval
    requested for this standing defect is now complete in research/scope.md,
    but the leaf has not carried it into References." It named `authoring`.

    That was the run converging. The defect had moved from the brief to the
    leaf, which is what a repair looks like when the evidence lands first and
    the citation follows. The budget read it as the same id coming back and
    charged the third of three, and the run ended holding a document whose
    every other lane passed.

    The rule is not that a repeated id is free. CON-PRO-001 repeated in the
    same run, to the same owner, unrepaired, and was charged exactly as before.
    """

    CITATION = CONTENT_LANES[3]
    PROFILE = CONTENT_LANES[4]

    def evaluate(self, run_id: str, by_lane: dict) -> dict:
        return self.engine.advance(
            run_id, lane_results=self.content_submissions(run_id, by_lane))

    def round_trip_through_research(self, run_id: str) -> None:
        """Everything the run does between one evaluation and the next.

        Driven by the workflow's own topology rather than a list written here,
        so that inserting a stage into the chain -- as v22 inserted
        `source-registration` -- does not silently stop this test exercising
        the round trip it is about.
        """
        for _ in range(12):
            stage_id = self.engine.load_state(run_id)["current_stage"]
            if stage_id == EVALUATION:
                return
            if stage_id == RESEARCH:
                self.engine.advance(
                    run_id, lane_results=self.research_submissions(run_id))
            else:
                self.pass_stage(run_id, stage_id)
        self.fail("the run never came back to the evaluation")

    def test_a_finding_that_changes_owner_does_not_spend_the_budget(self):
        run_id = self.drive_to(EVALUATION)

        out = self.evaluate(
            run_id, {self.CITATION: [blocking("CON-CIT-007", RESEARCH,
                                              "the brief lacks the loci")]})
        self.assertEqual(out["stage"], RESEARCH,
                         "a research-owned finding routes to research")
        self.round_trip_through_research(run_id)

        out = self.evaluate(
            run_id, {self.CITATION: [blocking("CON-CIT-007", AUTHORING,
                                              "the leaf has not cited them")]})
        self.assertEqual(
            out["stage"], REVISION,
            "the same defect, now the leaf's, goes to the leaf's reviser "
            "instead of ending the run")
        state = self.engine.load_state(run_id)
        self.assertIsNone(state["disposition"])
        self.assertEqual(
            state["stage_repeats"][EVALUATION], 1,
            "only the first failure of the streak; the owner change is the "
            "repair working, not the repair failing")
        self.assertEqual(
            state["stage_failures"][EVALUATION], 2,
            "both rounds are still consecutive failures, and still bounded "
            "by max_total_iterations")

    def test_the_same_id_to_the_same_owner_is_still_charged(self):
        run_id = self.drive_to(EVALUATION)
        for _ in range(2):
            out = self.evaluate(
                run_id, {self.PROFILE: [blocking("CON-PRO-001", AUTHORING)]})
            self.assertEqual(out["stage"], REVISION)
            self.engine.advance(
                run_id, result_path=self.worker_pass(run_id, REVISION))
            self.engine.advance(run_id, run_gate=True)
        self.assertEqual(
            self.engine.load_state(run_id)["stage_repeats"][EVALUATION], 2,
            "unrepaired, to the same owner, twice: that is the repetition the "
            "budget exists to stop")

    def test_the_engine_records_the_owner_each_standing_id_named(self):
        run_id = self.drive_to(EVALUATION)
        self.evaluate(
            run_id, {self.CITATION: [blocking("CON-CIT-007", RESEARCH)]})
        self.assertEqual(
            self.engine.load_state(run_id)["stage_blocking_targets"][EVALUATION],
            {"CON-CIT-007": RESEARCH},
            "the comparison the charge makes has to be recorded to be replayed")

    def test_a_pass_clears_the_recorded_owners_with_the_ids(self):
        run_id = self.drive_to(EVALUATION)
        self.evaluate(
            run_id, {self.CITATION: [blocking("CON-CIT-007", AUTHORING)]})
        self.engine.advance(
            run_id, result_path=self.worker_pass(run_id, REVISION))
        self.engine.advance(run_id, run_gate=True)
        self.evaluate(run_id, {})
        state = self.engine.load_state(run_id)
        self.assertNotIn(EVALUATION, state["stage_blocking_targets"],
                         "cleared with the ids, or a later run of the stage "
                         "would compare against a document that passed")

    def test_a_finding_with_no_owner_charges_exactly_as_before(self):
        """Gates and unrouted evaluators raise findings with no owner at all.

        Both sides of the comparison are then absent, which must read as the
        same owner rather than as a change, or every such stage would have
        quietly lost its budget.
        """
        run_id = self.drive_to(EVALUATION)
        for _ in range(2):
            self.engine.advance(run_id, lane_results=self.content_submissions(
                run_id, {self.PROFILE: [dict(
                    blocking("CON-PRO-009", AUTHORING),
                    repair_target=AUTHORING)]}))
            self.engine.advance(
                run_id, result_path=self.worker_pass(run_id, REVISION))
            self.engine.advance(run_id, run_gate=True)
        self.assertEqual(
            self.engine.load_state(run_id)["stage_repeats"][EVALUATION], 2)


class CompoundRequiredResultTests(unittest.TestCase):
    """The rule the citation lane broke, and the incident that shows the cost.

    The split rule predates run ce4ecd514b64d2f9 and would have saved it. What
    the fragment lacked was the shape of the violation: a `required_result`
    joined by `then`, which reads like one instruction and is two.
    """

    FRAGMENT = (ROOT / "workflows" / "fragments" / "propers"
                / "content-evaluation.md")

    def setUp(self):
        self.text = self.FRAGMENT.read_text(encoding="utf-8")
        # The fragment is hard-wrapped, so every rule in it spans line breaks.
        self.flat = " ".join(self.text.split())

    def test_the_rule_still_binds_one_finding_to_one_owner(self):
        self.assertIn(
            "One blocking finding names one defect and one repair owner.",
            self.flat)
        self.assertIn("Do not hide two owners behind a single "
                      "`required_result`", self.flat)

    def test_the_fragment_names_the_word_that_gives_a_compound_away(self):
        self.assertIn("The word that gives a compound away is `then`.",
                      self.flat)

    def test_the_fragment_carries_the_run_that_paid_for_the_rule(self):
        self.assertIn("ce4ecd514b64d2f9", self.text,
                      "a rule with no incident behind it is the one that gets "
                      "reasoned away at three in the morning")

    def test_the_fragment_says_what_the_split_would_have_done(self):
        self.assertIn("CARRIED_FINDINGS", self.text,
                      "the lane has to know the second half is delivered, or "
                      "splitting looks like extra work for nothing")
