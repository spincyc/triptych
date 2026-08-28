#!/usr/bin/env python3
"""A thin sweep is a retry, not a funeral.

`research-synthesis` could return only `PASS` or `BLOCKED`, and as a linear
stage its `BLOCKED` was terminal — so an ordinary recoverable gap in the
seven-lane research ended the run for that document at that commit, and
re-seeding handed back the same dead run. The stage is now an evaluator: it
can say the research is insufficient but recoverable, name what is missing,
and send the lanes back for it, bounded like every other loop in the
pipeline. These tests hold the difference between "come back with more" and
"this cannot be done here".
"""
import json
import os
import re
import shutil
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
LAUNCHER = ROOT / "tools" / "tpt"
sys.path.insert(0, str(ROOT / "scripts"))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from _workflow import (  # noqa: E402
    ACCEPTED,
    BLOCKED,
    CHANGES_REQUIRED,
    FANOUT,
    HOST_MAX,
    PASS,
    PROGRAM,
    SINGLE,
    STRICT_UNION,
    WorkflowError,
)
from test_workflow_research_fanout import (  # noqa: E402
    CONTENT_LANES,
    DOC,
    FRAGMENTS,
    RESEARCH_LANES,
    VISUAL_LANES,
    PropersCase,
    assert_lane_owns_its_findings,
    workflow_json,
)

SYNTHESIS = "research-synthesis"
RESEARCH = "research"

# `max_iterations` counts consecutive CHANGES_REQUIRED and blocks when the
# count reaches it, so a limit of 3 grants two retries and refuses the third.
RETRY_LIMIT = 3
RETRIES_GRANTED = RETRY_LIMIT - 1


def deficiency(finding_id: str, lane: str, problem: str = "coverage is thin"):
    """A synthesis finding naming the lane that owes the work."""
    return {
        "id": finding_id, "severity": "blocking", "location": lane,
        "problem": problem,
        "required_result": f"{lane} returns the missing evidence",
    }


class RetryCase(PropersCase):
    """Drives the real propers workflow to research-synthesis."""

    def synthesis(self, run_id: str, disposition: str,
                  findings: list | None = None, name: str = "syn") -> str:
        packet = self.engine.load_state(run_id)["packet_hashes"][-1]
        body = {
            "stage": SYNTHESIS, "iteration": packet["iteration"],
            "disposition": disposition,
            "summary": "integrated the joined research",
            "findings": findings if findings is not None else [],
        }
        if disposition == PASS:
            body["artifact_path"] = "research/scope.md"
        return self.write(f"{name}-{packet['iteration']}", body)

    def drive_to_synthesis(self, run_id: str | None = None) -> str:
        """Seed if needed, then advance until synthesis is waiting."""
        if run_id is None:
            run_id = self.seed()["run_id"]
        for _ in range(24):
            stage_id = self.engine.load_state(run_id)["current_stage"]
            if stage_id == SYNTHESIS:
                return run_id
            if stage_id == RESEARCH:
                self.engine.advance(
                    run_id, lane_results=self.lane_submissions(run_id))
            else:
                self.pass_stage(run_id, stage_id)
        self.fail("could not reach research-synthesis")

    def forwarded(self, packet_text: str) -> list[dict]:
        line = next(l for l in packet_text.splitlines()
                    if l.startswith("PRIOR_FINDINGS: "))
        return json.loads(line[len("PRIOR_FINDINGS: "):])


# ---------------------------------------------------------------------------
# 1-12. The three dispositions and the bounded loop
# ---------------------------------------------------------------------------

class SynthesisDispositionTests(RetryCase):
    """Test 1-5 and 9: what the stage may say, and where each answer goes."""

    def test_pass_is_accepted_and_continues_to_authoring(self):
        """Test 1 and 2."""
        run_id = self.drive_to_synthesis()
        out = self.engine.advance(
            run_id, result_path=self.synthesis(run_id, PASS))
        self.assertEqual(out["stage"], "author-proper")
        self.assertIsNone(out["disposition"])
        self.assertEqual(self.engine.load_state(run_id)["transitions"][-1],
                         {"from": SYNTHESIS, "to": "author-proper",
                          "disposition": PASS})

    def test_changes_required_is_accepted_and_re_enters_research(self):
        """Test 3 and 5."""
        run_id = self.drive_to_synthesis()
        out = self.engine.advance(run_id, result_path=self.synthesis(
            run_id, CHANGES_REQUIRED,
            [deficiency("SYN-001", "patristic-reception")]))
        self.assertEqual(out["stage"], RESEARCH)
        self.assertEqual(self.engine.load_state(run_id)["transitions"][-1],
                         {"from": SYNTHESIS, "to": RESEARCH,
                          "disposition": CHANGES_REQUIRED})

    def test_changes_required_needs_a_blocking_finding(self):
        """Test 4."""
        run_id = self.drive_to_synthesis()
        before = self.authoritative(run_id)
        for findings in ([], [{"id": "SYN-A", "severity": "advisory",
                               "location": "patristic-reception",
                               "problem": "a nicety",
                               "required_result": "consider it"}]):
            with self.subTest(findings=len(findings)):
                with self.assertRaises(WorkflowError) as caught:
                    self.engine.advance(run_id, result_path=self.synthesis(
                        run_id, CHANGES_REQUIRED, findings, name="empty"))
                self.assertIn("no blocking finding", str(caught.exception))
        self.assertEqual(self.authoritative(run_id), before,
                         "a refused request leaves the run where it was")

    def test_blocked_still_terminates(self):
        """Test 9."""
        run_id = self.drive_to_synthesis()
        out = self.engine.advance(
            run_id, result_path=self.synthesis(run_id, BLOCKED))
        self.assertEqual(out["disposition"], BLOCKED)
        state = self.engine.load_state(run_id)
        self.assertEqual(state["current_stage"], BLOCKED)
        self.assertEqual(len(state["packet_hashes"]),
                         len(state["transitions"]),
                         "a blocked run was given no successor packet")
        with self.assertRaises(WorkflowError) as caught:
            self.engine.advance(
                run_id, result_path=self.synthesis(run_id, PASS, name="after"))
        self.assertIn(BLOCKED, str(caught.exception))

    def test_a_finding_must_name_a_real_research_lane(self):
        """The premise the loop rests on is in the schema, not only in prose."""
        run_id = self.drive_to_synthesis()
        before = self.authoritative(run_id)
        for location in ("the patristic sweep", "page 4", "evidence-discipline"):
            with self.subTest(location=location):
                with self.assertRaises(WorkflowError) as caught:
                    self.engine.advance(run_id, result_path=self.synthesis(
                        run_id, CHANGES_REQUIRED,
                        [dict(deficiency("SYN-001", "patristic-reception"),
                              location=location)], name="badloc"))
                self.assertIn("expected one of:", str(caught.exception))
        self.assertEqual(self.authoritative(run_id), before)

    def test_a_pass_may_not_carry_a_standing_blocking_finding(self):
        """Otherwise the run wedges at the one place it cannot be repaired."""
        run_id = self.drive_to_synthesis()
        before = self.authoritative(run_id)
        with self.assertRaises(WorkflowError) as caught:
            self.engine.advance(run_id, result_path=self.synthesis(
                run_id, PASS,
                [deficiency("SYN-999", "cultural-afterlife")], name="dirty"))
        self.assertIn("still stand as blocking", str(caught.exception))
        self.assertIn("SYN-999", str(caught.exception))
        self.assertEqual(self.authoritative(run_id), before)

    def test_an_unknown_disposition_is_still_refused(self):
        run_id = self.drive_to_synthesis()
        packet = self.engine.load_state(run_id)["packet_hashes"][-1]
        path = self.write("weird", {
            "stage": SYNTHESIS, "iteration": packet["iteration"],
            "disposition": "RETRY", "summary": "x", "findings": []})
        with self.assertRaises(WorkflowError) as caught:
            self.engine.advance(run_id, result_path=path)
        self.assertIn("invalid disposition", str(caught.exception))


class RetryLoopTests(RetryCase):
    """Test 6-8 and 10-12: the loop, what travels it, and where it stops."""

    def test_the_deficiencies_reach_every_research_lane_verbatim(self):
        """Test 6: through tpt, not through a controller's paraphrase."""
        run_id = self.drive_to_synthesis()
        findings = [
            deficiency("SYN-001", "patristic-reception",
                       "no Greek witness for the Communion antiphon"),
            deficiency("SYN-002", "cultural-afterlife",
                       "only two qualifying candidates were returned"),
        ]
        out = self.engine.advance(run_id, result_path=self.synthesis(
            run_id, CHANGES_REQUIRED, findings))
        self.assertEqual(out["stage"], RESEARCH)

        forwarded = self.forwarded(
            Path(out["packet_abs_path"]).read_text(encoding="utf-8"))
        self.assertEqual(forwarded, findings,
                         "the findings are forwarded exactly as written")

        lanes = self.engine.load_state(run_id)["packet_hashes"][-1]["lanes"]
        self.assertEqual(len(lanes), len(RESEARCH_LANES))
        for lane in lanes:
            with self.subTest(lane=lane["lane"]):
                text = (ROOT / lane["path"]).read_text(encoding="utf-8")
                self.assertIn("no Greek witness for the Communion antiphon",
                              text)
                self.assertIn("only two qualifying candidates were returned",
                              text)
        replay = self.engine.replay(run_id)
        self.assertTrue(replay["deterministic"],
                        "a forwarded retry must replay from the record alone")

    def test_the_loop_runs_the_lanes_and_returns_to_synthesis(self):
        """Test 7, 8 and 10."""
        run_id = self.drive_to_synthesis()
        out = self.engine.advance(run_id, result_path=self.synthesis(
            run_id, CHANGES_REQUIRED,
            [deficiency("SYN-001", "liturgical-history")]))
        self.assertEqual(out["stage"], RESEARCH)

        out = self.engine.advance(
            run_id, lane_results=self.lane_submissions(run_id))
        self.assertEqual(out["stage"], SYNTHESIS, "the loop closes")

        # The second synthesis packet is a fresh seven-lane join, not a diff:
        # the lanes' own findings, and none of the request that sent them back.
        packet = Path(out["packet_abs_path"]).read_text(encoding="utf-8")
        rejoined = self.forwarded(packet)
        self.assertEqual([f["lane"] for f in rejoined], RESEARCH_LANES)
        self.assertNotIn("SYN-001", packet,
                         "the request is answered by the resweep, not "
                         "carried alongside it")

        out = self.engine.advance(
            run_id, result_path=self.synthesis(run_id, PASS))
        self.assertEqual(out["stage"], "author-proper",
                         "a satisfied retry continues to authoring")

        state = self.engine.load_state(run_id)
        self.assertEqual(state["stage_iterations"][RESEARCH], 2)
        self.assertEqual(state["stage_iterations"][SYNTHESIS], 2)
        self.assertEqual(state["stage_failures"][SYNTHESIS], 0,
                         "passing clears the retry budget")

    def test_the_retries_are_bounded_and_fail_closed(self):
        """Test 11 and 12, against the budget that charges repetition.

        The same unmet request, three times. The first spends one of three
        because it has nothing to repeat; the second and third re-raise an id
        the stage already had standing, and the third exhausts the budget.
        """
        run_id = self.drive_to_synthesis()
        for attempt in range(RETRIES_GRANTED):
            with self.subTest(attempt=attempt):
                out = self.engine.advance(run_id, result_path=self.synthesis(
                    run_id, CHANGES_REQUIRED,
                    [deficiency("SYN-001", "scripture-context")]))
                self.assertEqual(out["stage"], RESEARCH)
                state = self.engine.load_state(run_id)
                self.assertEqual(state["stage_failures"][SYNTHESIS],
                                 attempt + 1)
                self.assertEqual(state["stage_repeats"][SYNTHESIS],
                                 attempt + 1)
                self.engine.advance(
                    run_id, lane_results=self.lane_submissions(run_id))

        out = self.engine.advance(run_id, result_path=self.synthesis(
            run_id, CHANGES_REQUIRED,
            [deficiency("SYN-001", "scripture-context")]))
        self.assertEqual(out["disposition"], BLOCKED)
        self.assertIn("iteration limit exceeded", out["message"])
        self.assertIn(SYNTHESIS, out["message"])
        self.assertIn("SYN-001", out["message"],
                      "the block names the finding that was never repaired")
        self.assertEqual(self.engine.load_state(run_id)["current_stage"],
                         BLOCKED)

    def test_a_request_naming_new_work_does_not_spend_the_repeat_budget(self):
        """Different ids are different work, and work is not a loop.

        The rule this replaces could not tell the two apart. Run
        b68cca80edb75854 repaired what it was told, raised different findings
        against a substantially rewritten document, and was blocked for it.
        """
        run_id = self.drive_to_synthesis()
        for attempt in range(RETRIES_GRANTED + 2):
            with self.subTest(attempt=attempt):
                out = self.engine.advance(run_id, result_path=self.synthesis(
                    run_id, CHANGES_REQUIRED,
                    [deficiency(f"SYN-{attempt:03d}", "scripture-context")]))
                self.assertEqual(
                    out["stage"], RESEARCH,
                    "a request naming work never asked for before is progress")
                state = self.engine.load_state(run_id)
                self.assertEqual(state["stage_failures"][SYNTHESIS],
                                 attempt + 1)
                self.assertEqual(
                    state["stage_repeats"][SYNTHESIS], 1,
                    "only the first failure of the streak was charged")
                self.engine.advance(
                    run_id, lane_results=self.lane_submissions(run_id))
        self.assertIsNone(self.engine.load_state(run_id)["disposition"])

    def test_one_repeat_among_new_work_still_spends_one(self):
        """Progress and a loop in the same result: the loop is charged."""
        run_id = self.drive_to_synthesis()
        for attempt, findings in enumerate((
            [deficiency("SYN-A", "scripture-context")],
            [deficiency("SYN-B", "scripture-context")],
            [deficiency("SYN-B", "scripture-context"),
             deficiency("SYN-C", "precedent-search")],
        )):
            self.engine.advance(run_id, result_path=self.synthesis(
                run_id, CHANGES_REQUIRED, findings))
            self.engine.advance(
                run_id, lane_results=self.lane_submissions(run_id))
        state = self.engine.load_state(run_id)
        self.assertEqual(state["stage_failures"][SYNTHESIS], 3)
        self.assertEqual(
            state["stage_repeats"][SYNTHESIS], 2,
            "the first failure, and the one re-raising SYN-B; the round that "
            "moved from SYN-A to SYN-B cost nothing")
        self.assertIsNone(state["disposition"])

    def test_the_absolute_ceiling_stops_a_stage_that_never_repeats(self):
        """New work forever is still not a run that may go on forever.

        `max_total_iterations` defaults to twice `max_iterations`, so six
        consecutive failures end the stage however novel each one is.
        """
        ceiling = 2 * RETRY_LIMIT
        run_id = self.drive_to_synthesis()
        for attempt in range(ceiling - 1):
            out = self.engine.advance(run_id, result_path=self.synthesis(
                run_id, CHANGES_REQUIRED,
                [deficiency(f"SYN-{attempt:03d}", "scripture-context")]))
            self.assertEqual(out["stage"], RESEARCH, f"at attempt {attempt}")
            self.engine.advance(
                run_id, lane_results=self.lane_submissions(run_id))
        out = self.engine.advance(run_id, result_path=self.synthesis(
            run_id, CHANGES_REQUIRED,
            [deficiency("SYN-FINAL", "scripture-context")]))
        self.assertEqual(out["disposition"], BLOCKED)
        self.assertIn(f"{ceiling}/{ceiling} consecutive failures",
                      out["message"])
        self.assertIn("never ran out", out["message"],
                      "the message says which budget stopped the run")

    def test_a_pass_clears_the_repeat_counter_and_the_standing_ids(self):
        """After a pass, the same id is new work against a new document."""
        run_id = self.drive_to_synthesis()
        self.engine.advance(run_id, result_path=self.synthesis(
            run_id, CHANGES_REQUIRED,
            [deficiency("SYN-001", "scripture-context")]))
        self.engine.advance(
            run_id, lane_results=self.lane_submissions(run_id))
        self.engine.advance(run_id, result_path=self.synthesis(run_id, PASS))
        state = self.engine.load_state(run_id)
        self.assertEqual(state["stage_repeats"][SYNTHESIS], 0)
        self.assertNotIn(SYNTHESIS, state["stage_blocking_ids"],
                         "a pass forgets what was standing, so the same id "
                         "later is not a repeat of anything")

    def test_the_budget_is_the_stages_own_and_counts_consecutively(self):
        """A pass between two requests clears the count."""
        run_id = self.drive_to_synthesis()
        for round_index in range(RETRIES_GRANTED + 1):
            self.engine.advance(run_id, result_path=self.synthesis(
                run_id, CHANGES_REQUIRED,
                [deficiency(f"SYN-{round_index}", "precedent-search")]))
            self.engine.advance(
                run_id, lane_results=self.lane_submissions(run_id))
            if round_index == 0:
                # Pass once, which resets the counter, then start again.
                self.engine.advance(
                    run_id, result_path=self.synthesis(run_id, PASS))
                self.assertEqual(
                    self.engine.load_state(run_id)["stage_failures"][SYNTHESIS],
                    0)
                self.engine.advance(
                    run_id, result_path=self.worker_pass(run_id,
                                                         "author-proper"))
                # v10 preflights the leaf before the evaluation reads it.
                self.engine.advance(run_id, run_gate=True)
                self.engine.advance(run_id, lane_results=[
                    (lane, self.write(f"ce-{lane}", {
                        "stage": "content-evaluation", "iteration": 0,
                        "lane": lane,
                        "lane_packet_hash": {
                            e["lane"]: e["hash"] for e in
                            self.engine.load_state(run_id)
                            ["packet_hashes"][-1]["lanes"]}[lane],
                        "disposition": CHANGES_REQUIRED if lane ==
                        CONTENT_LANES[0] else PASS,
                        "summary": "judged",
                        "findings": [{
                            "id": "CON-001", "severity": "blocking",
                            "location": "p1", "problem": "thin research",
                            "required_result": "resweep",
                            "repair_target": "research"}]
                        if lane == CONTENT_LANES[0] else [],
                    }))
                    for lane in CONTENT_LANES])
                self.engine.advance(
                    run_id, lane_results=self.lane_submissions(run_id))
        state = self.engine.load_state(run_id)
        self.assertEqual(
            state["stage_failures"][SYNTHESIS], RETRIES_GRANTED,
            "three requests were made and one pass fell between the first two "
            "of them, so only the two after the reset are counted; had the "
            "first carried over, the count would be 3 and the run blocked")
        self.assertIsNone(state["disposition"],
                          "and the run is still running")

    def test_completion_order_after_a_retry_still_cannot_matter(self):
        """Test 13, at the second visit to research."""
        def drive(order):
            run_id = self.drive_to_synthesis()
            self.engine.advance(run_id, result_path=self.synthesis(
                run_id, CHANGES_REQUIRED,
                [deficiency("SYN-001", "theological-synthesis")]))
            out = self.engine.advance(
                run_id, lane_results=self.lane_submissions(run_id, order))
            joined = self.engine.load_state(run_id)["result_hashes"][-1]
            return (out["stage"], out["packet_hash"], joined["hash"],
                    (ROOT / joined["path"]).read_bytes(),
                    [l["lane"] for l in joined["lanes"]])

        declared = drive(RESEARCH_LANES)
        self.discard_runs()
        scrambled = drive([
            "precedent-search", "liturgical-history", "cultural-afterlife",
            "scripture-context", "source-citation-coverage",
            "theological-synthesis", "patristic-reception"])
        self.assertEqual(declared, scrambled)
        self.assertEqual(declared[0], SYNTHESIS)
        self.assertEqual(declared[4], RESEARCH_LANES)


# ---------------------------------------------------------------------------
# 14-25. What must not have moved
# ---------------------------------------------------------------------------

class PreservedGuaranteeTests(RetryCase):
    """Test 14-24."""

    def test_synthesis_is_still_single_and_still_does_no_research(self):
        """Test 14."""
        stage = {s["id"]: s for s in workflow_json()["stages"]}[SYNTHESIS]
        self.assertEqual(stage["execution"], {"mode": SINGLE})
        run_id = self.drive_to_synthesis()
        path = self.engine.load_state(run_id)["packet_hashes"][-1]["path"]
        packet = (ROOT / path).read_text(encoding="utf-8")
        for forbidden in ("search the web",
                          "search the repository for precedent",
                          "acquire new sources", "hunt cultural afterlives",
                          "find new witnesses",
                          "fill a gap by doing your own research",
                          "silently supplement incomplete lane output"):
            with self.subTest(forbidden=forbidden):
                self.assertIn(forbidden, packet)

    def test_synthesis_is_still_the_sole_writer_of_the_brief(self):
        """Test 15 and 16."""
        text = (FRAGMENTS / "propers" / f"{SYNTHESIS}.md").read_text("utf-8")
        self.assertRegex(text, re.compile(r"sole writer", re.IGNORECASE))
        author = (FRAGMENTS / "propers" / "author-proper.md").read_text("utf-8")
        self.assertRegex(author, re.compile(r"immutable|read-only", re.I))

    def test_the_content_evaluation_routing_still_reaches_research(self):
        """Test 17 and 18.

        Version 10 added the `brief` owner between the two this test was
        written for. The guarantee it holds is the one the synthesis retry
        depends on: a `research` finding still re-enters `research`, and the
        stage is still the five-lane fan-out in canonical order.
        """
        stage = {s["id"]: s for s in
                 workflow_json()["stages"]}["content-evaluation"]
        self.assertEqual(stage["repair_routes"], [
            {"repair_target": "research", "transition": "research"},
            {"repair_target": "brief", "transition": "research-synthesis"},
            {"repair_target": "authoring", "transition": "content-revision"},
        ])
        self.assertEqual(stage["execution"]["mode"], FANOUT)
        self.assertEqual(stage["execution"]["parallelism"], HOST_MAX)
        self.assertEqual([l["id"] for l in stage["execution"]["lanes"]],
                         CONTENT_LANES)

    def test_the_visual_fanout_and_gates_are_unchanged(self):
        """Test 19 and 20."""
        stages = {s["id"]: s for s in workflow_json()["stages"]}
        visual = stages["visual-evaluation"]["execution"]
        self.assertEqual(visual["mode"], FANOUT)
        self.assertEqual(visual["parallelism"], HOST_MAX)
        self.assertEqual(visual["join"], STRICT_UNION)
        self.assertEqual([l["id"] for l in visual["lanes"]], VISUAL_LANES)
        accepting = [s for s in workflow_json()["stages"]
                     if ACCEPTED in (s.get("next"), s.get("pass_transition"))]
        self.assertEqual([s["id"] for s in accepting], ["publication-gates"])
        self.assertEqual(accepting[0]["execution"], {"mode": PROGRAM})
        self.assertEqual(stages["visual-evaluation"]["pass_transition"],
                         "final-acceptance",
                         "the visual fan-out still passes into artifact "
                         "acceptance, which now hands on to publication")

    def test_the_seven_research_lanes_are_declared_and_disjoint(self):
        """Sending the research back is only safe if the lanes still divide.

        A retry re-enters every lane at once, so two lanes sharing a finding
        space or a question would return the retry twice over.
        """
        stage = {s["id"]: s for s in workflow_json()["stages"]}[RESEARCH]
        self.assertEqual([l["id"] for l in stage["execution"]["lanes"]],
                         RESEARCH_LANES)
        self.assertEqual(stage["execution"]["parallelism"], HOST_MAX)
        self.assertEqual(stage["execution"]["join"], STRICT_UNION)
        for lane in RESEARCH_LANES:
            with self.subTest(lane=lane):
                assert_lane_owns_its_findings(self, f"research-{lane}")

    def test_seed_remains_byte_idempotent_across_a_retry(self):
        """Test 21 and 24."""
        args = {"proper": DOC, "provider": "gpt"}
        first = self.engine.seed_bytes("proper", args)
        run_id = json.loads(first)["run_id"]
        self.assertEqual(json.loads(first)["workflow_version"],
                         workflow_json()["version"])
        self.drive_to_synthesis(run_id)
        self.engine.advance(run_id, result_path=self.synthesis(
            run_id, CHANGES_REQUIRED, [deficiency("SYN-001", "precedent-search")]))
        run_dir = self.engine.run_dir(run_id)
        before = {p.relative_to(run_dir).as_posix(): p.read_bytes()
                  for p in sorted(run_dir.rglob("*")) if p.is_file()}
        self.assertEqual(self.engine.seed_bytes("proper", args), first)
        after = {p.relative_to(run_dir).as_posix(): p.read_bytes()
                 for p in sorted(run_dir.rglob("*")) if p.is_file()}
        self.assertEqual(before, after)
        self.assertTrue(self.engine.replay(run_id)["deterministic"])

    def test_a_retried_run_can_still_be_accepted(self):
        """Making this stage an evaluator put it inside the acceptance audit.

        `_verify_final_acceptance` requires every evaluator and gate to have
        last recorded `PASS` and to carry no standing blocking finding. A
        stage that asks for changes and is then satisfied must therefore leave
        a clean latest result behind it, or the retry would buy a run that can
        never be accepted.
        """
        run_id = self.drive_to_synthesis()
        self.engine.advance(run_id, result_path=self.synthesis(
            run_id, CHANGES_REQUIRED,
            [deficiency("SYN-001", "patristic-reception")]))
        self.engine.advance(
            run_id, lane_results=self.lane_submissions(run_id))
        self.engine.advance(
            run_id, result_path=self.synthesis(run_id, PASS))

        workflow = self.engine.load_workflow("proper")
        gate = next(s for s in workflow["stages"]
                    if s["id"] == "final-acceptance")
        state = self.engine.load_state(run_id)

        # The real audit, not a copy of it. The run has not built anything, so
        # it refuses — but it must refuse for the stages that genuinely have
        # not run, and say nothing about the stage that asked for a retry and
        # was then satisfied.
        with self.assertRaises(WorkflowError) as caught:
            self.engine._verify_final_acceptance(workflow, gate, state)
        complaint = str(caught.exception)
        self.assertNotIn(SYNTHESIS, complaint,
                         "a satisfied retry leaves nothing standing against "
                         "the stage at acceptance")
        self.assertIn("content-evaluation", complaint,
                      "the audit is really running")

    def test_the_audit_still_holds_this_stage_to_a_pass(self):
        """The twin: becoming an evaluator put it inside the audit's reach."""
        run_id = self.drive_to_synthesis()
        self.engine.advance(run_id, result_path=self.synthesis(
            run_id, CHANGES_REQUIRED,
            [deficiency("SYN-001", "patristic-reception")]))
        self.engine.advance(
            run_id, lane_results=self.lane_submissions(run_id))
        self.engine.advance(
            run_id, result_path=self.synthesis(run_id, PASS))

        workflow = self.engine.load_workflow("proper")
        gate = next(s for s in workflow["stages"]
                    if s["id"] == "final-acceptance")
        state = self.engine.load_state(run_id)
        for entry in state["result_hashes"]:
            if entry["stage"] == SYNTHESIS:
                entry["disposition"] = CHANGES_REQUIRED
        with self.assertRaises(WorkflowError) as caught:
            self.engine._verify_final_acceptance(workflow, gate, state)
        self.assertIn(f"{SYNTHESIS} last recorded {CHANGES_REQUIRED}",
                      str(caught.exception),
                      "the audit must actually check this stage")

    def test_a_failed_retry_advance_changes_nothing(self):
        """Test 22."""
        run_id = self.drive_to_synthesis()
        path = self.synthesis(run_id, CHANGES_REQUIRED,
                              [deficiency("SYN-001", "scripture-context")])
        before = self.authoritative(run_id)
        packets = self.runs / run_id / "packets"
        os.chmod(packets, 0o500)
        self.addCleanup(os.chmod, packets, 0o755)
        with self.assertRaises(WorkflowError):
            self.engine.advance(run_id, result_path=path)
        os.chmod(packets, 0o755)
        self.assertEqual(self.authoritative(run_id), before)
        self.assertEqual(self.engine.advance(run_id, result_path=path)["stage"],
                         RESEARCH, "the repaired retry emits the same move")

    def test_a_refused_retry_stays_non_authoritative(self):
        """Test 23."""
        run_id = self.drive_to_synthesis()
        before = self.authoritative(run_id)
        replay_before = self.engine.replay(run_id)
        packet = self.engine.load_state(run_id)["packet_hashes"][-1]
        bad = self.write("stale", {
            "stage": SYNTHESIS, "iteration": packet["iteration"] + 5,
            "disposition": CHANGES_REQUIRED, "summary": "x",
            "findings": [deficiency("SYN-001", "scripture-context")]})
        with self.assertRaises(WorkflowError):
            self.engine.advance(run_id, result_path=bad)
        self.assertEqual(self.authoritative(run_id), before)
        self.assertEqual(self.engine.replay(run_id), replay_before)


class LauncherTests(unittest.TestCase):
    """Test 25."""

    def tpt(self, *argv: str) -> subprocess.CompletedProcess:
        return subprocess.run([str(LAUNCHER), *argv], capture_output=True,
                              text=True, cwd=ROOT)

    def test_registered_tool_dispatch_is_unchanged(self):
        self.assertEqual(self.tpt("--check").returncode, 0)
        parsed = self.tpt("citations", "parse", "Psalm 24:1-3", "--json")
        self.assertEqual(parsed.returncode, 0, parsed.stderr)

    def test_the_retry_is_visible_in_the_definition(self):
        shown = self.tpt("workflow", "show", "proper")
        self.assertEqual(shown.returncode, 0, shown.stderr)
        stage = {s["id"]: s for s in json.loads(shown.stdout)["stages"]}[
            SYNTHESIS]
        self.assertEqual(stage["type"], "evaluator")
        self.assertEqual(stage["pass_transition"], "author-proper")
        self.assertEqual(stage["fail_transition"], RESEARCH)
        self.assertEqual(stage["max_iterations"], RETRY_LIMIT)
        self.assertEqual(stage["result_schema"],
                         "research-synthesis-result.json")
        self.assertNotIn("repair_routes", stage,
                         "one repair owner needs no routing table")


if __name__ == "__main__":
    unittest.main()
