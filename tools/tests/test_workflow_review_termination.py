#!/usr/bin/env python3
"""When to stop reviewing a document that is not getting worse.

Run `6fb5fba4867eb8cf` -- `proper-finish` v5, the Fifteenth Sunday after
Pentecost, provider `claude` -- blocked with its leaf in good shape. Its
instrumentation, read afterwards, says exactly what happened:

    stage_iterations  content-evaluation: 8
    stage_failures    content-evaluation: 8
    stage_repeats     content-evaluation: 1
    unrepaired_for    {}

Eight consecutive evaluations, eight failures, and one round in the whole run
that raised something an earlier round had raised. `unrepaired_for` empty at
every one of them: the reviser repaired everything it was ever handed and never
once reported a repair it could not make. Seven of the eight rounds found
something new, and true, in prose no reviser had been near.

The repeat budget was right not to fire -- repair was working. The absolute
ceiling fired instead, four rounds and some nine million subagent tokens after
the point where the answer had stopped changing, and reported it in the shape
of a verdict on the document.

A document that is not converging and a review that is not terminating want
opposite responses, and the engine already held both counters needed to tell
them apart. These tests hold the four things that follow from that: a third
counter that stops a purely-novel streak and says a person must decide; a
review scope, so the cold full read happens once instead of once a round; a
severity for a defect that is real and not worth a repair round, which binds
the rest of the run; and a second repair owner for the seam between two
editions, so a finding that reached a reviser forbidden to repair it now
reaches one that may.
"""
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from _workflow import (  # noqa: E402
    NOT_REPAIRED,
    PASS,
    REPAIRED,
    WorkflowError,
)
from test_workflow_convergence import (  # noqa: E402
    EVALUATION,
    BudgetCase,
)
from test_workflow_repair_routing import AUTHORING, blocking  # noqa: E402
from test_workflow_research_fanout import CONTENT_LANES  # noqa: E402


def finding(fid, severity, **extra):
    """A well-formed finding at any severity."""
    body = {
        "id": fid,
        "severity": severity,
        "location": extra.pop("location", "sections/30-commentary.tex line 8"),
        "problem": "probe",
        "required_result": "probe",
    }
    body.update(extra)
    return body


class NovelRoundsAreNotConvergenceFailuresTests(BudgetCase):
    """`max_novel_iterations`: the counter run 6fb5fba4867eb8cf needed."""

    def test_three_rounds_of_new_work_still_run(self):
        """The policy the earlier runs bought is not undone by this one.

        Two runs blocked while converging and the fix was to stop charging the
        repeat budget for repairs that worked. That must still hold: three
        rounds of genuine new work are progress and the run stays drivable.
        """
        run_id = self.drive_to(EVALUATION)
        for round_no in range(3):
            ids = [f"CON-EVI-{round_no}{n}" for n in range(2)]
            self.round_trip(run_id, ids, {fid: REPAIRED for fid in ids})
        state = self.engine.load_state(run_id)
        self.assertIsNone(state["disposition"])
        self.assertEqual(state["stage_novel"][EVALUATION], 2)

    def test_the_fourth_purely_novel_round_stops_the_run(self):
        run_id = self.drive_to(EVALUATION)
        for round_no in range(4):
            ids = [f"CON-EVI-{round_no}{n}" for n in range(2)]
            out = self.round_trip(run_id, ids, {fid: REPAIRED for fid in ids})
        state = self.engine.load_state(run_id)
        self.assertEqual(state["disposition"], "BLOCKED")
        self.assertEqual(
            state["stage_failures"][EVALUATION], 4,
            "four rounds, not the ten the absolute ceiling would have allowed")

    def test_the_stop_says_it_is_a_question_and_not_a_verdict(self):
        """The message is the whole point of the counter.

        `6fb5fba4867eb8cf` stopped with 'iteration limit exceeded', which reads
        as a document that ran out of chances. It was a document nobody could
        find a standing fault in.
        """
        run_id = self.drive_to(EVALUATION)
        reason = None
        for round_no in range(4):
            ids = [f"CON-EVI-{round_no}{n}" for n in range(2)]
            out = self.round_trip(run_id, ids, {fid: REPAIRED for fid in ids})
            reason = out.get("reason") or out.get("block_reason") or reason
        state = self.engine.load_state(run_id)
        text = json.dumps(state) + json.dumps(out)
        self.assertIn("review did not terminate", text)
        self.assertIn("question for a person", text)
        self.assertNotIn("iteration limit exceeded for content-evaluation",
                         text)

    def test_a_repeated_finding_resets_the_novel_counter(self):
        """A streak of new work is broken by anything coming back.

        The counter must mean 'consecutive', or a run that alternates between
        novel rounds and real repeat failures would be stopped by the wrong
        one of the two budgets.
        """
        run_id = self.drive_to(EVALUATION)
        self.round_trip(run_id, ["CON-EVI-01"], {"CON-EVI-01": REPAIRED})
        self.round_trip(run_id, ["CON-EVI-02"], {"CON-EVI-02": REPAIRED})
        state = self.engine.load_state(run_id)
        self.assertEqual(state["stage_novel"][EVALUATION], 1)
        self.round_trip(run_id, ["CON-EVI-03"], {"CON-EVI-03": NOT_REPAIRED})
        # The reviser's report reaches the counter at the *next* evaluation:
        # it is written when the revision result is recorded, which is after
        # the evaluation that raised the finding has already been charged.
        self.evaluate(run_id, ["CON-EVI-04"])
        state = self.engine.load_state(run_id)
        self.assertEqual(
            state["stage_novel"][EVALUATION], 0,
            "a repair the reviser could not make is not a novel round")
        self.assertEqual(state["stage_repeats"][EVALUATION], 2)

    def test_a_pass_clears_the_novel_counter(self):
        run_id = self.drive_to(EVALUATION)
        self.round_trip(run_id, ["CON-EVI-01"], {"CON-EVI-01": REPAIRED})
        self.round_trip(run_id, ["CON-EVI-02"], {"CON-EVI-02": REPAIRED})
        self.assertEqual(
            self.engine.load_state(run_id)["stage_novel"][EVALUATION], 1)
        self.engine.advance(
            run_id, lane_results=self.content_submissions(run_id))
        self.assertEqual(
            self.engine.load_state(run_id)["stage_novel"][EVALUATION], 0)

    def test_both_evaluations_declare_the_bound(self):
        for name in ("proper.json", "proper-finish.json"):
            workflow = json.loads(
                (ROOT / "workflows" / "pipelines" / name)
                .read_text(encoding="utf-8"))
            declared = {
                stage["id"]: stage.get("max_novel_iterations")
                for stage in workflow["stages"]
                if "max_novel_iterations" in stage
            }
            self.assertEqual(
                declared,
                {"content-evaluation": 3, "synthesis-evaluation": 3},
                f"{name}: both evaluations of the leaf bound novel rounds")


class ReviewScopeTests(BudgetCase):
    """The cold full read is worth paying for once, not once a round."""

    def test_the_first_evaluation_carries_no_scope(self):
        run_id = self.drive_to(EVALUATION)
        packet = (ROOT / self.engine.load_state(run_id)
                  ["packet_hashes"][-1]["path"]).read_text(encoding="utf-8")
        self.assertNotIn(
            "REVIEW_SCOPE:", packet,
            "nothing has been read yet, so there is nothing to scope against")

    def test_a_later_evaluation_carries_one(self):
        run_id = self.drive_to(EVALUATION)
        self.round_trip(run_id, ["CON-EVI-01"], {"CON-EVI-01": REPAIRED})
        state = self.engine.load_state(run_id)
        if not (state.get("stage_scope_baseline") or {}).get(EVALUATION):
            self.skipTest("no document tree under this fixture to scope over")
        packet = (ROOT / state["packet_hashes"][-1]["path"]).read_text(
            encoding="utf-8")
        self.assertEqual(state["current_stage"], EVALUATION)
        self.assertIn("REVIEW_SCOPE:", packet)

    def test_the_scope_is_stored_in_state_so_replay_stays_deterministic(self):
        """`replay` recompiles the current packet and compares hashes.

        A header read off the working tree would be an input the run state does
        not carry, and two replays either side of an edit would disagree about
        bytes that are fixed. So the diff is computed when a result is recorded
        and stored, and the packet restates state exactly as DOCUMENT_ROOT
        restates the arguments.
        """
        run_id = self.drive_to(EVALUATION)
        self.round_trip(run_id, ["CON-EVI-01"], {"CON-EVI-01": REPAIRED})
        state = self.engine.load_state(run_id)
        if not (state.get("stage_scope_baseline") or {}).get(EVALUATION):
            self.skipTest("no document tree under this fixture to scope over")
        self.assertIn("stage_scope_changed", state)
        report = self.engine.replay(run_id)
        self.assertTrue(report["deterministic"], report)


class ScopeDisciplineTests(BudgetCase):
    """A blocking finding against text that moved is free; elsewhere, say why.

    These runs drive a published leaf that no stage of the test actually edits,
    so the honest diff between two evaluations is empty. An empty diff is
    deliberately exempt -- nothing moving is the reviser's business and not the
    evaluator's, and the novel-round counter is what ends that loop. To reach
    the rule itself the baseline is doctored so that one file reads as changed,
    which is what a real revision produces.
    """

    def submit(self, run_id, findings):
        return self.engine.advance(
            run_id,
            lane_results=self.content_submissions(
                run_id, {CONTENT_LANES[0]: findings}))

    def with_one_file_moved(self, run_id, moved="sections/90-scope.tex"):
        """Make the recorded diff name exactly one file."""
        state = self.engine.load_state(run_id)
        state.setdefault("stage_scope_baseline", {})[EVALUATION] = {
            moved: "0" * 64}
        state.setdefault("stage_scope_changed", {})[EVALUATION] = [moved]
        self.engine.save_state(run_id, state)
        return moved

    def test_a_finding_on_what_moved_needs_no_explanation(self):
        run_id = self.drive_to(EVALUATION)
        self.round_trip(run_id, ["CON-EVI-01"], {"CON-EVI-01": REPAIRED})
        moved = self.with_one_file_moved(run_id)
        entry = blocking("CON-EVI-99", AUTHORING)
        entry["location"] = f"{moved} line 220"
        self.submit(run_id, [entry])
        self.assertIsNone(self.engine.load_state(run_id)["disposition"])

    def test_an_unexplained_finding_outside_the_scope_is_refused(self):
        run_id = self.drive_to(EVALUATION)
        self.round_trip(run_id, ["CON-EVI-01"], {"CON-EVI-01": REPAIRED})
        self.with_one_file_moved(run_id)
        entry = blocking("CON-EVI-99", AUTHORING)
        entry["location"] = "sections/30-commentary.tex line 8"
        with self.assertRaises(WorkflowError) as caught:
            self.submit(run_id, [entry])
        self.assertIn("out_of_scope_reason", str(caught.exception))

    def test_the_reason_is_all_that_is_asked(self):
        run_id = self.drive_to(EVALUATION)
        self.round_trip(run_id, ["CON-EVI-01"], {"CON-EVI-01": REPAIRED})
        self.with_one_file_moved(run_id)
        entry = blocking("CON-EVI-99", AUTHORING)
        entry["location"] = "sections/30-commentary.tex line 8"
        entry["out_of_scope_reason"] = (
            "unchanged in itself; the sentence it depends on moved this round")
        self.submit(run_id, [entry])
        self.assertIsNone(self.engine.load_state(run_id)["disposition"])

    def test_a_standing_id_is_exempt(self):
        """A finding already standing is not a new lens on settled prose."""
        run_id = self.drive_to(EVALUATION)
        entry = blocking("CON-EVI-01", AUTHORING)
        entry["location"] = "sections/30-commentary.tex line 8"
        self.submit(run_id, [entry])
        self.revise(run_id, {"CON-EVI-01": NOT_REPAIRED})
        self.engine.advance(run_id, run_gate=True)
        self.with_one_file_moved(run_id)
        self.submit(run_id, [entry])
        self.assertIsNone(self.engine.load_state(run_id)["disposition"])

    def test_an_empty_scope_refuses_nothing(self):
        run_id = self.drive_to(EVALUATION)
        self.round_trip(run_id, ["CON-EVI-01"], {"CON-EVI-01": REPAIRED})
        state = self.engine.load_state(run_id)
        self.assertEqual(
            (state.get("stage_scope_changed") or {}).get(EVALUATION), [],
            "nothing was edited between the two evaluations")
        self.submit(run_id, [blocking("CON-EVI-99", AUTHORING)])
        self.assertIsNone(self.engine.load_state(run_id)["disposition"])


class AcceptedIsAVerdictTests(BudgetCase):
    """True, checked, and not worth a repair round."""

    def submit(self, run_id, findings, disposition=PASS):
        """Lane submissions at a disposition this test chooses.

        An accepted finding does not ask for a change, so a lane carrying only
        accepted findings passes. The shared helper infers CHANGES_REQUIRED
        from a non-empty findings list, which was true while every severity
        that reached a result either blocked or was advisory.
        """
        packet = self.engine.load_state(run_id)["packet_hashes"][-1]
        emitted = {entry["lane"]: entry for entry in packet["lanes"]}
        pairs = []
        for lane in CONTENT_LANES:
            carried = findings if lane == CONTENT_LANES[0] else []
            body = {
                "stage": packet["stage"], "iteration": packet["iteration"],
                "lane": lane, "lane_packet_hash": emitted[lane]["hash"],
                "disposition": disposition if carried else PASS,
                "summary": f"{lane} judged its criteria",
                "findings": carried,
            }
            pairs.append((lane, self.write(f"content-{lane}", body)))
        return self.engine.advance(run_id, lane_results=pairs)

    def test_an_accepted_finding_does_not_block(self):
        run_id = self.drive_to(EVALUATION)
        self.submit(run_id, [finding("CON-EVI-01", "accepted",
                                     accepted_because="costs a paragraph")])
        state = self.engine.load_state(run_id)
        self.assertIsNone(state["disposition"])
        self.assertNotEqual(state["current_stage"], "content-revision")

    def test_it_must_say_why(self):
        run_id = self.drive_to(EVALUATION)
        with self.assertRaises(WorkflowError) as caught:
            self.submit(run_id, [finding("CON-EVI-01", "accepted")])
        self.assertIn("accepted_because", str(caught.exception))

    def test_it_may_not_name_a_repair_owner(self):
        run_id = self.drive_to(EVALUATION)
        with self.assertRaises(WorkflowError) as caught:
            self.submit(run_id, [finding("CON-EVI-01", "accepted",
                                         accepted_because="probe",
                                         repair_target=AUTHORING)])
        self.assertIn("accepted", str(caught.exception))

    def back_at_the_evaluator(self, run_id, findings):
        """Submit a failing evaluation and drive around to the next one."""
        self.submit(run_id, findings, disposition="CHANGES_REQUIRED")
        blocking_ids = [entry["id"] for entry in findings
                        if entry.get("severity") == "blocking"]
        self.revise(run_id, {fid: REPAIRED for fid in blocking_ids})
        self.engine.advance(run_id, run_gate=True)

    def test_an_accepted_id_may_not_come_back_as_blocking(self):
        """The mirror of the rule against promoting an advisory.

        A later round that blocks on an accepted id has not found anything; it
        has disagreed with a judgement already recorded, and it spends a round
        doing so. Disagreement about what is worth repairing is what the
        escalation route is for.
        """
        run_id = self.drive_to(EVALUATION)
        self.back_at_the_evaluator(run_id, [
            blocking("CON-EVI-09", AUTHORING),
            finding("CON-EVI-01", "accepted", accepted_because="probe"),
        ])
        with self.assertRaises(WorkflowError) as caught:
            self.submit(run_id, [blocking("CON-EVI-01", AUTHORING)],
                        disposition="CHANGES_REQUIRED")
        self.assertIn("already accepted", str(caught.exception))

    def test_the_judgement_outlives_the_round_that_made_it(self):
        run_id = self.drive_to(EVALUATION)
        self.back_at_the_evaluator(run_id, [
            blocking("CON-EVI-09", AUTHORING),
            finding("CON-EVI-01", "accepted", accepted_because="probe"),
        ])
        held = self.engine.load_state(run_id)["accepted_ids"][EVALUATION]
        self.assertEqual(held, ["CON-EVI-01"])
        self.submit(run_id, [])
        self.assertEqual(
            self.engine.load_state(run_id)["accepted_ids"][EVALUATION],
            ["CON-EVI-01"],
            "a judgement does not stop holding because a later lane did not "
            "restate it")


class TheRecordCarriesTheVerdictsTests(AcceptedIsAVerdictTests):
    """An advisory that dies with its run is met again as though new."""

    def test_the_record_is_schema_three(self):
        run_id = self.drive_to(EVALUATION)
        self.submit(run_id, [
            finding("CON-EVI-01", "accepted",
                    accepted_because="costs more than it saves"),
            finding("CON-EVI-02", "advisory"),
        ])
        record = self.standing_record(run_id)
        if record is None:
            self.skipTest("no standing findings root under this fixture")
        self.assertEqual(record["standing_findings_schema"], 3)

    def test_accepted_and_advisory_both_reach_the_tree(self):
        run_id = self.drive_to(EVALUATION)
        self.submit(run_id, [
            finding("CON-EVI-01", "accepted",
                    accepted_because="costs more than it saves"),
            finding("CON-EVI-02", "advisory"),
        ])
        record = self.standing_record(run_id)
        if record is None:
            self.skipTest("no standing findings root under this fixture")
        self.assertEqual(
            [entry["id"] for entry in record.get("accepted", [])],
            ["CON-EVI-01"])
        self.assertEqual(
            [entry["id"] for entry in record.get("advisories", [])],
            ["CON-EVI-02"])
        self.assertEqual(
            record["accepted"][0]["accepted_because"],
            "costs more than it saves",
            "the reason is the whole of what a later reader judges it by")

    def standing_record(self, run_id):
        import tomllib
        state = self.engine.load_state(run_id)
        root = self.engine.standing_findings_root
        if root is None:
            return None
        document_root = state.get("document_root")
        if not document_root:
            return None
        path = (root / document_root / "evaluations"
                / "blocking-findings-v1.toml")
        if not path.is_file():
            return None
        return tomllib.loads(path.read_text(encoding="utf-8"))


class TheSeamHasAnOwnerTests(unittest.TestCase):
    """A defect in canonical prose that only the companion makes visible.

    Run `da04e65ca4ec963b` raised nine blocking findings against one companion.
    Three were sentences in `sections/20-themes.tex`,
    `sections/35-source-grounded-synthesis.tex`, `sections/50-interpretive.tex`
    and `sections/90-scope.tex` -- files both editions input -- sending a reader
    to element subsections and an appointed-text section the profile forbids the
    companion. Twenty-four locators resolve in the canonical build and dangle in
    the companion's.

    They routed to `synthesis-revision`, whose remit is the companion alone and
    which is told not to revise settled canonical prose. It reported them
    unrepaired, which was the honest answer, and under v5 the next evaluation
    would have raised them again until the budget ran out.
    """

    def stages(self, name):
        workflow = json.loads(
            (ROOT / "workflows" / "pipelines" / name)
            .read_text(encoding="utf-8"))
        return {stage["id"]: stage for stage in workflow["stages"]}

    def test_both_pipelines_route_a_seam_repair(self):
        for name in ("proper.json", "proper-finish.json"):
            stages = self.stages(name)
            self.assertEqual(
                stages["synthesis-evaluation"]["repair_routes"],
                [{"repair_target": "derivation",
                  "transition": "synthesis-revision"},
                 {"repair_target": "seam",
                  "transition": "synthesis-revision"}],
                name)

    def test_the_reviser_declares_it_owns_the_seam(self):
        for name in ("proper.json", "proper-finish.json"):
            stages = self.stages(name)
            self.assertEqual(
                stages["synthesis-revision"]["repairs"],
                ["derivation", "seam"],
                f"{name}: a route needs an owner that says it owns it")

    def test_the_schema_admits_the_owner(self):
        schema = json.loads(
            (ROOT / "workflows" / "schema"
             / "synthesis-evaluation-result.json").read_text(encoding="utf-8"))
        self.assertEqual(schema["finding_enums"]["repair_target"],
                         ["derivation", "seam"])


if __name__ == "__main__":
    unittest.main()
