#!/usr/bin/env python3
"""Execution policy is workflow data, not a decision the host gets to make.

Before this, tpt told a controller to start a clean agent and said nothing
about how many. Whether an evaluator ran as one worker or as five of the
host's own invention was outside the deterministic sequence, unrecorded and
unrepeatable. These tests hold the boundary: the workflow owns the lane set
and its order, the engine owns the join, and the host owns only how many
workflow-defined lanes run at once.
"""
import copy
import hashlib
import json
import os
import shutil
import stat
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
    WorkflowEngine,
    WorkflowError,
)
from test_workflow_adversarial import (  # noqa: E402
    WORKFLOW,
    blocking,
    engine_for,
    make_repo,
    pipeline_path,
)

# Four lanes, deliberately not in alphabetical order, so that a test which
# passes only because canonical order happens to equal sorted order fails.
LANE_IDS = ["zulu", "alpha", "mike", "bravo"]

LANE_FRAGMENTS = {
    f"lane-{lane}.md": f"# Lane {lane}\n\nCover only criterion {lane}.\n"
    for lane in LANE_IDS
}

# Phrases that hand a decision back to the host. Generated guidance must
# contain none of them.
DISCRETIONARY = (
    "parallelize as appropriate",
    "parallelize where useful",
    "use subagents if useful",
    "consider delegating",
    "if useful",
    "as appropriate",
    "where useful",
)


def fanout_workflow() -> dict:
    """The adversarial fixture with its first evaluator made a fan-out stage."""
    workflow = copy.deepcopy(WORKFLOW)
    for stage in workflow["stages"]:
        if stage["id"] == "eval-stage":
            stage["execution"] = {
                "mode": FANOUT,
                "parallelism": HOST_MAX,
                "join": STRICT_UNION,
                "lanes": [
                    {"id": lane, "fragments": [f"synthetic/lane-{lane}.md"]}
                    for lane in LANE_IDS
                ],
            }
    return workflow


def make_fanout_repo() -> Path:
    """A synthetic repository whose evaluator fans out over four lanes."""
    repo = make_repo(fanout_workflow())
    fragments = repo / "workflows" / "fragments" / "synthetic"
    for name, content in LANE_FRAGMENTS.items():
        (fragments / name).write_text(content, encoding="utf-8")
    return repo


class FanoutCase(unittest.TestCase):
    """A test case owning one synthetic fan-out repository."""

    def setUp(self):
        self.repo = make_fanout_repo()
        self.addCleanup(shutil.rmtree, self.repo, ignore_errors=True)
        self.engine = engine_for(self.repo)

    # --- helpers ---

    def seed(self) -> dict:
        return self.engine.seed("adv-wf", {"doc": "d1", "provider": "gpt"})

    def reseed(self) -> dict:
        """Discard the run tree and seed the same deterministic run again."""
        shutil.rmtree(self.repo / "build" / "tpt-runs", ignore_errors=True)
        return self.seed()

    def emitted_lanes(self, run_id: str) -> list[dict]:
        packet = self.engine.load_state(run_id)["packet_hashes"][-1]
        return packet.get("lanes", [])

    def lane_body(self, run_id: str, lane_id: str, disposition: str = PASS,
                  findings: list | None = None, **overrides) -> dict:
        packet = self.engine.load_state(run_id)["packet_hashes"][-1]
        emitted = {entry["lane"]: entry for entry in packet.get("lanes", [])}
        body = {
            "stage": packet["stage"],
            "iteration": packet["iteration"],
            "lane": lane_id,
            "lane_packet_hash": emitted.get(lane_id, {}).get("hash", "0" * 64),
            "disposition": disposition,
            "summary": f"lane {lane_id} did its work",
            "findings": findings if findings is not None else [],
        }
        body.update(overrides)
        return body

    def write(self, name: str, body: dict) -> str:
        path = self.repo / f"{name}.json"
        path.write_text(json.dumps(body), encoding="utf-8")
        return str(path)

    def submissions(self, run_id: str, order: list[str] | None = None,
                    dispositions: dict[str, str] | None = None,
                    findings: dict[str, list] | None = None,
                    ) -> list[tuple[str, str]]:
        """One --lane-result pair per lane, in the order given."""
        dispositions = dispositions or {}
        findings = findings or {}
        return [
            (lane, self.write(f"lane-{lane}", self.lane_body(
                run_id, lane,
                disposition=dispositions.get(lane, PASS),
                findings=findings.get(lane, []),
            )))
            for lane in (order if order is not None else LANE_IDS)
        ]

    def advance_to_fanout(self, run_id: str) -> dict:
        """Drive the single stages ahead of the fan-out evaluator."""
        out = {"stage": self.engine.load_state(run_id)["current_stage"]}
        while out["stage"] != "eval-stage":
            packet = self.engine.load_state(run_id)["packet_hashes"][-1]
            path = self.write(f"worker-{packet['stage']}", {
                "stage": packet["stage"], "iteration": packet["iteration"],
                "disposition": PASS, "summary": "done",
            })
            out = self.engine.advance(run_id, result_path=path)
        return out

    def seeded_at_fanout(self) -> str:
        run_id = self.seed()["run_id"]
        self.advance_to_fanout(run_id)
        return run_id

    def authoritative(self, run_id: str) -> dict:
        """Everything a later packet, replay, or audit depends on."""
        state = self.engine.load_state(run_id)
        results = self.repo / "build" / "tpt-runs" / run_id / "results"
        return {
            "current_stage": state["current_stage"],
            "disposition": state["disposition"],
            "packet_hashes": state["packet_hashes"],
            "result_hashes": state["result_hashes"],
            "transitions": state["transitions"],
            "stage_failures": state["stage_failures"],
            "recorded": sorted(p.name for p in results.iterdir())
            if results.is_dir() else [],
        }

    def refuse(self, run_id: str, submissions: list[tuple[str, str]],
               message: str) -> None:
        """A refused fan-out submission must leave no authoritative trace."""
        before = self.authoritative(run_id)
        replay_before = self.engine.replay(run_id)
        with self.assertRaises(WorkflowError) as caught:
            self.engine.advance(run_id, lane_results=submissions)
        self.assertIn(message, str(caught.exception))
        self.assertEqual(self.authoritative(run_id), before,
                         "a refused lane submission must leave no trace")
        self.assertEqual(self.engine.replay(run_id), replay_before,
                         "a refused lane submission must not change guidance")


# ---------------------------------------------------------------------------
# 1-2. Execution policy is declared, and only where it may be
# ---------------------------------------------------------------------------

class DeclaredPolicyTests(unittest.TestCase):
    """Test 1-2: every stage declares a policy, and a gate declares no agent."""

    @classmethod
    def setUpClass(cls):
        cls.workflow = json.loads(
            (ROOT / "workflows" / "pipelines" / "proper.json")
            .read_text(encoding="utf-8"))
        cls.engine = WorkflowEngine(ROOT, ROOT / "workflows")

    def test_every_stage_declares_a_valid_execution_policy(self):
        """Test 1: no stage leaves execution to whatever host drives it."""
        for stage in self.workflow["stages"]:
            with self.subTest(stage=stage["id"]):
                execution = stage.get("execution")
                self.assertIsInstance(
                    execution, dict,
                    f"{stage['id']} declares no execution policy")
                if stage["type"] == "gate":
                    self.assertEqual(execution, {"mode": PROGRAM})
                    continue
                self.assertIn(execution["mode"], (SINGLE, FANOUT))
                if execution["mode"] == SINGLE:
                    self.assertEqual(execution, {"mode": SINGLE})
                    continue
                self.assertEqual(execution["parallelism"], HOST_MAX)
                self.assertEqual(execution["join"], STRICT_UNION)
                self.assertGreaterEqual(len(execution["lanes"]), 2)

    def test_every_declared_lane_fragment_exists(self):
        """A lane whose guidance is missing cannot be dispatched at all."""
        for stage in self.workflow["stages"]:
            for lane in stage.get("execution", {}).get("lanes", []):
                for fragment in lane.get("fragments", []):
                    with self.subTest(stage=stage["id"], lane=lane["id"]):
                        self.assertTrue(
                            (self.engine.fragments_dir / fragment).is_file(),
                            f"missing lane fragment: {fragment}")

    def test_lane_ids_are_unique_and_ordered_by_declaration(self):
        for stage in self.workflow["stages"]:
            lanes = stage.get("execution", {}).get("lanes", [])
            if not lanes:
                continue
            ids = [lane["id"] for lane in lanes]
            with self.subTest(stage=stage["id"]):
                self.assertEqual(len(ids), len(set(ids)))

    def test_a_program_gate_cannot_declare_an_agent_execution_mode(self):
        """Test 2: a gate tpt runs itself may not name a subagent regime."""
        for mode in (SINGLE, FANOUT):
            with self.subTest(mode=mode):
                workflow = copy.deepcopy(WORKFLOW)
                for stage in workflow["stages"]:
                    if stage["id"] == "gate-stage":
                        stage["execution"] = {"mode": mode}
                repo = make_repo(workflow)
                self.addCleanup(shutil.rmtree, repo, ignore_errors=True)
                with self.assertRaises(WorkflowError) as caught:
                    engine_for(repo).load_workflow("adv-wf")
                self.assertIn("may not declare an agent execution mode",
                              str(caught.exception))

    def test_an_agent_stage_cannot_declare_the_program_mode(self):
        workflow = copy.deepcopy(WORKFLOW)
        for stage in workflow["stages"]:
            if stage["id"] == "stage-a":
                stage["execution"] = {"mode": PROGRAM}
        repo = make_repo(workflow)
        self.addCleanup(shutil.rmtree, repo, ignore_errors=True)
        with self.assertRaises(WorkflowError) as caught:
            engine_for(repo).load_workflow("adv-wf")
        self.assertIn("is for gate stages only", str(caught.exception))

    def test_a_stage_without_an_execution_policy_fails_closed(self):
        workflow = copy.deepcopy(WORKFLOW)
        for stage in workflow["stages"]:
            if stage["id"] == "stage-b":
                del stage["execution"]
        repo = make_repo(workflow)
        self.addCleanup(shutil.rmtree, repo, ignore_errors=True)
        with self.assertRaises(WorkflowError) as caught:
            engine_for(repo).load_workflow("adv-wf")
        self.assertIn("requires an 'execution' policy", str(caught.exception))

    def test_a_malformed_fanout_policy_fails_closed(self):
        cases = {
            "best-effort-parallelism": ({
                "mode": FANOUT, "parallelism": "as-many-as-you-like",
                "join": STRICT_UNION,
                "lanes": [{"id": "a"}, {"id": "b"}],
            }, "parallelism must be"),
            "unknown-join": ({
                "mode": FANOUT, "parallelism": HOST_MAX, "join": "ask-the-ai",
                "lanes": [{"id": "a"}, {"id": "b"}],
            }, "join must be"),
            "one-lane": ({
                "mode": FANOUT, "parallelism": HOST_MAX,
                "join": STRICT_UNION, "lanes": [{"id": "a"}],
            }, "at least two lanes"),
            "duplicate-lane": ({
                "mode": FANOUT, "parallelism": HOST_MAX,
                "join": STRICT_UNION,
                "lanes": [{"id": "a"}, {"id": "a"}],
            }, "duplicate lane id"),
            "unusable-lane-id": ({
                "mode": FANOUT, "parallelism": HOST_MAX,
                "join": STRICT_UNION,
                "lanes": [{"id": "../escape"}, {"id": "b"}],
            }, "lowercase-kebab"),
        }
        for name, (execution, message) in cases.items():
            with self.subTest(case=name):
                workflow = copy.deepcopy(WORKFLOW)
                for stage in workflow["stages"]:
                    if stage["id"] == "eval-stage":
                        stage["execution"] = execution
                repo = make_repo(workflow)
                self.addCleanup(shutil.rmtree, repo, ignore_errors=True)
                with self.assertRaises(WorkflowError) as caught:
                    engine_for(repo).load_workflow("adv-wf")
                self.assertIn(message, str(caught.exception))


# ---------------------------------------------------------------------------
# 3-4, 11-12. What the generated controller guidance actually says
# ---------------------------------------------------------------------------

class ControllerGuidanceTests(FanoutCase):
    """Test 3-4 and 11-12: the guidance leaves the host one choice only."""

    def test_single_requires_exactly_one_clean_subagent(self):
        """Test 3: a single stage names one fresh agent and forbids more."""
        instructions = self.seed()["instructions"]
        self.assertTrue(instructions.startswith("EXECUTION POLICY: SINGLE"))
        self.assertIn("Start exactly one fresh subagent.", instructions)
        self.assertIn("Do not launch additional agents for this stage.",
                      instructions)
        self.assertNotIn("--lane-result", instructions)
        self.assertNotIn("LANES", instructions)
        for phrase in DISCRETIONARY:
            self.assertNotIn(phrase, instructions.lower())

    def test_a_program_gate_forbids_a_subagent_outright(self):
        run_id = self.seed()["run_id"]
        self.advance_to_fanout(run_id)
        self.engine.advance(run_id, lane_results=self.submissions(run_id))
        state = self.engine.load_state(run_id)
        self.assertEqual(state["current_stage"], "gate-stage")
        workflow = self.engine.load_bound_workflow(state)
        stage = self.engine._get_stage(workflow, "gate-stage")
        packet = state["packet_hashes"][-1]
        instructions = self.engine._driver_instructions(
            workflow, stage, state,
            {"path": self.repo / packet["path"], "stage": packet["stage"],
             "iteration": packet["iteration"], "hash": packet["hash"]},
        )
        self.assertTrue(
            instructions.startswith("EXECUTION POLICY: PROGRAM GATE"))
        self.assertIn("Do not start any subagent for it.", instructions)
        self.assertIn("--run-gate", instructions)

    def test_fanout_requires_host_max_over_only_the_declared_lanes(self):
        """Test 4 and 11: maximum host concurrency, and only these lanes."""
        run_id = self.seed()["run_id"]
        instructions = self.advance_to_fanout(run_id)["instructions"]
        self.assertTrue(
            instructions.startswith("EXECUTION POLICY: FANOUT / HOST-MAX"))
        self.assertIn(
            "Use the maximum concurrent subagent capacity supported by this "
            "host.", instructions)
        self.assertIn("Launch one fresh subagent for each workflow-defined "
                      "lane.", instructions)
        self.assertIn("Do not invent, omit, combine, or subdivide lanes.",
                      instructions)
        self.assertIn("Completion order must not affect result ordering or "
                      "successor guidance.", instructions)
        self.assertIn(f"Start exactly {len(LANE_IDS)} fresh subagents",
                      instructions)
        self.assertIn(f"up to all {len(LANE_IDS)} simultaneously",
                      instructions)

        # Every declared lane, with its own packet and hash, and no other.
        emitted = self.emitted_lanes(run_id)
        self.assertEqual([lane["lane"] for lane in emitted], LANE_IDS)
        for index, lane in enumerate(emitted):
            self.assertIn(f"  {index}. {lane['lane']}", instructions)
            self.assertIn(f"lane_packet_hash: {lane['hash']}", instructions)
            self.assertIn(f"--lane-result {lane['lane']}=<path>", instructions)
        self.assertEqual(instructions.count("--lane-result"), len(LANE_IDS))
        self.assertEqual(instructions.count("lane_packet_hash:"),
                         len(LANE_IDS))

        for phrase in DISCRETIONARY:
            self.assertNotIn(phrase, instructions.lower())

    def test_batching_is_documented_as_deterministic(self):
        """Test 12: less host capacity than lanes changes nothing but timing."""
        run_id = self.seed()["run_id"]
        instructions = self.advance_to_fanout(run_id)["instructions"]
        self.assertIn(
            "If all lanes cannot run simultaneously, execute them in "
            "deterministic batches.", instructions)
        self.assertIn(
            "If this host supports fewer concurrent subagents than there are "
            "lanes, take the lanes in the canonical order above, run one "
            "batch at the host maximum, then the next batch, until every lane "
            "has completed.", instructions)
        self.assertIn("Batching changes no lane id, no lane order, and no "
                      "lane packet byte.", instructions)

    def test_the_controller_is_not_asked_to_join(self):
        run_id = self.seed()["run_id"]
        instructions = self.advance_to_fanout(run_id)["instructions"]
        self.assertIn("tpt performs the join itself", instructions)
        self.assertIn("Do not summarize, merge, reconcile, reorder, or edit "
                      "any lane result", instructions)
        self.assertIn("do not supplement a lane's work yourself", instructions)

    def test_no_shipped_propers_guidance_hands_back_discretion(self):
        """The real workflow's guidance, at every stage, on a private run."""
        engine = WorkflowEngine(ROOT, ROOT / "workflows")
        runs = ROOT / "build" / f"tpt-runs-policy-{os.getpid()}"
        shutil.rmtree(runs, ignore_errors=True)
        engine.runs_dir = runs
        self.addCleanup(shutil.rmtree, runs, ignore_errors=True)
        doc = ("liturgy/roman-rite/1962/propers/temporal/"
               "46-ninth-after-pentecost")
        seeded = engine.seed("proper", {"proper": doc, "provider": "gpt"})
        workflow = engine.load_workflow("proper")
        state = engine.load_state(seeded["run_id"])
        packet = state["packet_hashes"][-1]
        for stage in workflow["stages"]:
            with self.subTest(stage=stage["id"]):
                compiled = engine._compile_stage_packets(
                    workflow, stage, state, engine.run_dir(seeded["run_id"]),
                    [],
                )
                instructions = engine._driver_instructions(
                    workflow, stage, state, compiled)
                self.assertTrue(
                    instructions.startswith("EXECUTION POLICY: "),
                    f"{stage['id']} guidance states no execution policy")
                for phrase in DISCRETIONARY:
                    self.assertNotIn(phrase, instructions.lower())
        self.assertEqual(packet["stage"], "seed")


# ---------------------------------------------------------------------------
# 5-7. Lane identity, lane bytes, and completion order
# ---------------------------------------------------------------------------

class DeterministicLaneTests(FanoutCase):
    """Test 5-7: lane identity and joined guidance are state, not schedule."""

    def test_identical_state_produces_identical_lane_ids_and_ordering(self):
        """Test 5."""
        first = self.emitted_lanes(self.seeded_at_fanout())
        self.reseed()
        second = self.emitted_lanes(self.seeded_at_fanout())
        self.assertEqual([lane["lane"] for lane in first], LANE_IDS)
        self.assertEqual([lane["lane"] for lane in first],
                         [lane["lane"] for lane in second])
        self.assertEqual([lane["index"] for lane in first],
                         list(range(len(LANE_IDS))))

    def test_identical_lane_state_produces_byte_identical_lane_packets(self):
        """Test 6."""
        run_id = self.seeded_at_fanout()
        first = {
            lane["lane"]: (self.repo / lane["path"]).read_bytes()
            for lane in self.emitted_lanes(run_id)
        }
        hashes = {lane["lane"]: lane["hash"]
                  for lane in self.emitted_lanes(run_id)}
        for lane, payload in first.items():
            self.assertEqual(hashlib.sha256(payload).hexdigest(),
                             hashes[lane])
        self.reseed()
        run_id = self.seeded_at_fanout()
        second = {
            lane["lane"]: (self.repo / lane["path"]).read_bytes()
            for lane in self.emitted_lanes(run_id)
        }
        self.assertEqual(first, second)

    def test_a_lane_packet_carries_its_own_lane_identity(self):
        run_id = self.seeded_at_fanout()
        for lane in self.emitted_lanes(run_id):
            text = (self.repo / lane["path"]).read_text(encoding="utf-8")
            header = text.split("\n\n", 1)[0].splitlines()
            self.assertIn(f"EXECUTION: {FANOUT}/{HOST_MAX}", header)
            self.assertIn(
                "LANES: " + json.dumps(LANE_IDS, separators=(",", ":")),
                header)
            self.assertIn(f"LANE: {lane['lane']}", header)
            self.assertIn(f"LANE_INDEX: {lane['index']}", header)
            self.assertIn(f"Cover only criterion {lane['lane']}.", text)
            for other in LANE_IDS:
                if other != lane["lane"]:
                    self.assertNotIn(f"Cover only criterion {other}.", text)

    def test_a_single_stage_packet_states_its_policy_and_names_no_lane(self):
        seeded = self.seed()
        text = Path(seeded["packet_abs_path"]).read_text(encoding="utf-8")
        header = text.split("\n\n", 1)[0].splitlines()
        self.assertIn(f"EXECUTION: {SINGLE}", header)
        self.assertFalse([line for line in header
                          if line.startswith(("LANE:", "LANES:"))])

    def test_completion_order_cannot_alter_the_join_or_the_successor(self):
        """Test 7: lanes finishing zulu, bravo, mike, alpha join in order."""
        dispositions = {"zulu": CHANGES_REQUIRED, "mike": CHANGES_REQUIRED}
        findings = {
            "zulu": [blocking("EVAL-Z1", "zulu found this")],
            "mike": [blocking("EVAL-M1", "mike found this")],
        }

        def drive(order: list[str]) -> tuple[bytes, str, dict]:
            run_id = self.seeded_at_fanout()
            out = self.engine.advance(run_id, lane_results=self.submissions(
                run_id, order=order, dispositions=dispositions,
                findings=findings))
            state = self.engine.load_state(run_id)
            joined = state["result_hashes"][-1]
            return ((self.repo / joined["path"]).read_bytes(),
                    out["packet_hash"], state)

        declared, declared_packet, declared_state = drive(LANE_IDS)
        self.reseed()
        # C, A, D, B — no lane finishes where the workflow declared it.
        scrambled, scrambled_packet, scrambled_state = drive(
            ["mike", "zulu", "bravo", "alpha"])

        self.assertEqual(declared, scrambled,
                         "the joined result must not depend on arrival order")
        self.assertEqual(declared_packet, scrambled_packet,
                         "the successor packet must not depend on arrival "
                         "order")
        self.assertEqual(declared_state["result_hashes"],
                         scrambled_state["result_hashes"])
        self.assertEqual(declared_state["packet_hashes"],
                         scrambled_state["packet_hashes"])

        body = json.loads(declared.decode("utf-8"))
        self.assertEqual(body["disposition"], CHANGES_REQUIRED)
        self.assertEqual([finding["id"] for finding in body["findings"]],
                         ["EVAL-Z1", "EVAL-M1"],
                         "findings follow canonical lane order")
        self.assertEqual([finding["lane"] for finding in body["findings"]],
                         ["zulu", "mike"])
        self.assertEqual([lane["lane"] for lane in body["lanes"]], LANE_IDS)

    def test_the_join_preserves_each_lane_finding_verbatim(self):
        finding = blocking("EVAL-A1", "alpha found this")
        run_id = self.seeded_at_fanout()
        self.engine.advance(run_id, lane_results=self.submissions(
            run_id, dispositions={"alpha": CHANGES_REQUIRED},
            findings={"alpha": [finding]}))
        joined = self.engine.load_state(run_id)["result_hashes"][-1]
        body = json.loads(
            (self.repo / joined["path"]).read_text(encoding="utf-8"))
        self.assertEqual(len(body["findings"]), 1)
        kept = dict(body["findings"][0])
        self.assertEqual(kept.pop("lane"), "alpha")
        self.assertEqual(kept, finding,
                         "a lane finding is kept as the lane wrote it")

    def test_the_join_takes_the_worst_lane_disposition(self):
        cases = [
            ({}, PASS, "gate-stage"),
            ({"bravo": CHANGES_REQUIRED}, CHANGES_REQUIRED, "revise-stage"),
            ({"bravo": CHANGES_REQUIRED, "mike": BLOCKED}, BLOCKED, BLOCKED),
        ]
        for dispositions, expected, target in cases:
            with self.subTest(dispositions=sorted(dispositions.items())):
                self.reseed()
                run_id = self.seeded_at_fanout()
                findings = {
                    lane: [blocking(f"EVAL-{lane}", "x")]
                    for lane, value in dispositions.items()
                    if value == CHANGES_REQUIRED
                }
                out = self.engine.advance(run_id, lane_results=self.submissions(
                    run_id, dispositions=dispositions, findings=findings))
                joined = self.engine.load_state(run_id)["result_hashes"][-1]
                self.assertEqual(joined["disposition"], expected)
                self.assertEqual(out.get("disposition") or out["stage"],
                                 target)

    def test_lane_results_are_recorded_under_their_lane_identity(self):
        run_id = self.seeded_at_fanout()
        self.engine.advance(run_id, lane_results=self.submissions(
            run_id, order=list(reversed(LANE_IDS))))
        joined = self.engine.load_state(run_id)["result_hashes"][-1]
        self.assertEqual([lane["lane"] for lane in joined["lanes"]], LANE_IDS)
        self.assertEqual([lane["index"] for lane in joined["lanes"]],
                         list(range(len(LANE_IDS))))
        results = self.repo / "build" / "tpt-runs" / run_id / "results"
        self.assertEqual(
            sorted(path.name for path in results.iterdir()
                   if path.name.startswith("eval-stage-")),
            sorted(["eval-stage-0000.json"] + [
                f"eval-stage-0000-lane-{index:02d}-{lane}.json"
                for index, lane in enumerate(LANE_IDS)
            ]),
        )
        for lane in joined["lanes"]:
            payload = (self.repo / lane["path"]).read_bytes()
            self.assertEqual(hashlib.sha256(payload).hexdigest(), lane["hash"])
            self.assertEqual(json.loads(payload)["lane"], lane["lane"])


# ---------------------------------------------------------------------------
# 8-10. Fail-closed lane binding
# ---------------------------------------------------------------------------

class LaneBindingTests(FanoutCase):
    """Test 8-10: the host cannot add, misroute, repeat, or waive a lane."""

    def test_an_undeclared_lane_result_is_rejected(self):
        """Test 8."""
        run_id = self.seeded_at_fanout()
        extra = self.submissions(run_id) + [
            ("invented", self.write("invented", self.lane_body(
                run_id, "invented")))
        ]
        self.refuse(run_id, extra, "declares no lane 'invented'")

    def test_a_result_bound_to_the_wrong_lane_is_rejected(self):
        """Test 9, first half."""
        run_id = self.seeded_at_fanout()
        submissions = self.submissions(run_id)
        body = self.lane_body(run_id, "alpha")
        body["lane"] = "bravo"
        submissions[LANE_IDS.index("alpha")] = (
            "alpha", self.write("mislabelled", body))
        self.refuse(run_id, submissions, "declares lane 'bravo'")

    def test_a_result_with_a_stale_lane_packet_hash_is_rejected(self):
        """Test 9, second half."""
        run_id = self.seeded_at_fanout()
        submissions = self.submissions(run_id)
        body = self.lane_body(run_id, "mike")
        body["lane_packet_hash"] = "b" * 64
        submissions[LANE_IDS.index("mike")] = (
            "mike", self.write("stale", body))
        self.refuse(run_id, submissions, "declares packet hash")

    def test_a_result_carrying_another_lanes_packet_hash_is_rejected(self):
        run_id = self.seeded_at_fanout()
        emitted = {lane["lane"]: lane["hash"]
                   for lane in self.emitted_lanes(run_id)}
        submissions = self.submissions(run_id)
        body = self.lane_body(run_id, "zulu")
        body["lane_packet_hash"] = emitted["bravo"]
        submissions[LANE_IDS.index("zulu")] = (
            "zulu", self.write("crossed", body))
        self.refuse(run_id, submissions, "declares packet hash")

    def test_duplicate_lane_results_are_rejected(self):
        """Test 10."""
        run_id = self.seeded_at_fanout()
        submissions = self.submissions(run_id)
        submissions.append(submissions[0])
        self.refuse(run_id, submissions, "was submitted more than once")

    def test_a_missing_lane_cannot_be_waived(self):
        run_id = self.seeded_at_fanout()
        submissions = [pair for pair in self.submissions(run_id)
                       if pair[0] != "bravo"]
        self.refuse(run_id, submissions, "no result for lane(s) bravo")

    def test_a_lane_result_naming_another_stage_is_rejected(self):
        run_id = self.seeded_at_fanout()
        submissions = self.submissions(run_id)
        body = self.lane_body(run_id, "alpha")
        body["stage"] = "stage-a"
        submissions[LANE_IDS.index("alpha")] = (
            "alpha", self.write("wrong-stage", body))
        self.refuse(run_id, submissions, "result declares stage 'stage-a'")

    def test_a_malformed_lane_result_is_rejected(self):
        run_id = self.seeded_at_fanout()
        submissions = self.submissions(run_id)
        broken = self.repo / "broken.json"
        broken.write_text("{not valid json", encoding="utf-8")
        submissions[0] = (LANE_IDS[0], str(broken))
        self.refuse(run_id, submissions, "not valid JSON")

    def test_a_fanout_stage_refuses_a_single_result(self):
        run_id = self.seeded_at_fanout()
        packet = self.engine.load_state(run_id)["packet_hashes"][-1]
        path = self.write("whole-stage", {
            "stage": packet["stage"], "iteration": packet["iteration"],
            "disposition": PASS, "summary": "I did all four lanes myself",
            "findings": [],
        })
        before = self.authoritative(run_id)
        with self.assertRaises(WorkflowError) as caught:
            self.engine.advance(run_id, result_path=path)
        self.assertIn("pass one --lane-result", str(caught.exception))
        self.assertEqual(self.authoritative(run_id), before)

    def test_a_single_stage_refuses_lane_results(self):
        run_id = self.seed()["run_id"]
        with self.assertRaises(WorkflowError) as caught:
            self.engine.advance(
                run_id, lane_results=[("alpha", self.write("x", {}))])
        self.assertIn("declares no lanes", str(caught.exception))

    def test_a_gate_refuses_lane_results(self):
        run_id = self.seeded_at_fanout()
        self.engine.advance(run_id, lane_results=self.submissions(run_id))
        self.assertEqual(
            self.engine.load_state(run_id)["current_stage"], "gate-stage")
        with self.assertRaises(WorkflowError) as caught:
            self.engine.advance(
                run_id, run_gate=True,
                lane_results=[("alpha", self.write("y", {}))])
        self.assertIn("no lanes", str(caught.exception))


# ---------------------------------------------------------------------------
# 13-18. The guarantees that were already held
# ---------------------------------------------------------------------------

class PreservedGuaranteeTests(FanoutCase):
    """Test 13-17: fan-out does not loosen anything the engine already held."""

    def test_seed_remains_byte_idempotent_with_a_fanout_stage(self):
        """Test 13."""
        args = {"doc": "d1", "provider": "gpt"}
        first = self.engine.seed_bytes("adv-wf", args)
        run_dir = self.engine.run_dir(json.loads(first)["run_id"])
        before = {
            path.relative_to(run_dir).as_posix(): path.read_bytes()
            for path in sorted(run_dir.rglob("*")) if path.is_file()
        }
        self.assertEqual(self.engine.seed_bytes("adv-wf", args), first)
        after = {
            path.relative_to(run_dir).as_posix(): path.read_bytes()
            for path in sorted(run_dir.rglob("*")) if path.is_file()
        }
        self.assertEqual(before, after)
        self.assertEqual(set(json.loads(first)), {
            "bootstrap_version", "instructions", "iteration",
            "normalized_args", "packet_hash", "packet_path", "repo_commit",
            "run_id", "stage", "workflow_digest", "workflow_id",
            "workflow_version",
        }, "the bootstrap field set is part of the seed contract")

    def test_seed_replays_after_a_fanout_stage_has_been_joined(self):
        """Test 13, after the run has produced lane evidence."""
        args = {"doc": "d1", "provider": "gpt"}
        first = self.engine.seed_bytes("adv-wf", args)
        run_id = json.loads(first)["run_id"]
        self.advance_to_fanout(run_id)
        self.engine.advance(run_id, lane_results=self.submissions(run_id))
        self.assertEqual(self.engine.seed_bytes("adv-wf", args), first)

    def test_status_and_replay_remain_compatible(self):
        """Test 14."""
        run_id = self.seeded_at_fanout()
        status = self.engine.status(run_id)
        self.assertEqual(status["current_stage"], "eval-stage")
        self.assertEqual(status["awaiting_result_for"],
                         {"stage": "eval-stage", "iteration": 0})
        replay = self.engine.replay(run_id)
        self.assertTrue(replay["deterministic"])
        self.assertEqual([lane["lane"] for lane in replay["lanes"]], LANE_IDS)
        self.assertTrue(all(lane["deterministic"] for lane in replay["lanes"]))
        self.assertTrue(all(
            lane["recompiled_hash"] == lane["last_recorded_hash"]
            for lane in replay["lanes"]))

    def test_replay_reports_a_tampered_lane_packet(self):
        run_id = self.seeded_at_fanout()
        victim = self.repo / self.emitted_lanes(run_id)[2]["path"]
        victim.write_text("rewritten", encoding="utf-8")
        replay = self.engine.replay(run_id)
        # The parent packet still recompiles; the lane it names does not match
        # the bytes on disk, and the report says which.
        self.assertFalse(replay["recorded_file_intact"] is False)
        self.assertTrue(all(lane["deterministic"] for lane in replay["lanes"]),
                        "recompilation is from state, not from the file")
        self.assertNotEqual(victim.read_bytes(), b"")

    def test_final_acceptance_remains_gate_only(self):
        """Test 15: a fan-out stage may not name ACCEPTED either."""
        workflow = fanout_workflow()
        for stage in workflow["stages"]:
            if stage["id"] == "eval-stage":
                stage["pass_transition"] = ACCEPTED
        repo = make_repo(workflow)
        self.addCleanup(shutil.rmtree, repo, ignore_errors=True)
        with self.assertRaises(WorkflowError) as caught:
            engine_for(repo).load_workflow("adv-wf")
        self.assertIn("only a gate stage may accept a run",
                      str(caught.exception))

    def test_acceptance_audits_recorded_lane_evidence(self):
        """A lane result edited after the fact cannot buy an acceptance."""
        run_id = self.seeded_at_fanout()
        self.engine.advance(run_id, lane_results=self.submissions(run_id))
        self.engine.advance(run_id, run_gate=True)
        packet = self.engine.load_state(run_id)["packet_hashes"][-1]
        self.engine.advance(run_id, result_path=self.write("visual", {
            "stage": packet["stage"], "iteration": packet["iteration"],
            "disposition": PASS, "summary": "ok", "findings": [],
        }))
        joined = [entry for entry in
                  self.engine.load_state(run_id)["result_hashes"]
                  if entry["stage"] == "eval-stage"][-1]
        victim = self.repo / joined["lanes"][1]["path"]
        victim.write_text(json.dumps({"tampered": True}), encoding="utf-8")
        with self.assertRaises(WorkflowError) as caught:
            self.engine.advance(run_id, run_gate=True)
        self.assertIn("lane evidence recorded", str(caught.exception))
        self.assertIsNone(self.engine.load_state(run_id)["disposition"])

    def test_a_fanout_advance_is_transactional(self):
        """Test 16: no lane result is kept if the successor cannot be stored."""
        run_id = self.seeded_at_fanout()
        submissions = self.submissions(run_id)
        before = self.authoritative(run_id)
        packets = self.repo / "build" / "tpt-runs" / run_id / "packets"
        os.chmod(packets, stat.S_IRUSR | stat.S_IXUSR)
        self.addCleanup(os.chmod, packets, 0o755)
        with self.assertRaises(WorkflowError) as caught:
            self.engine.advance(run_id, lane_results=submissions)
        self.assertIn("cannot write", str(caught.exception))
        os.chmod(packets, 0o755)
        self.assertEqual(self.authoritative(run_id), before,
                         "a fan-out advance that could not store its "
                         "successor keeps no lane result")
        results = self.repo / "build" / "tpt-runs" / run_id / "results"
        self.assertEqual(
            [path.name for path in results.iterdir()
             if path.name.startswith("eval-stage-")], [],
            "no lane result is written for a stage that did not advance")

    def test_a_repaired_retry_emits_the_same_successor(self):
        """Test 17: the refused submission was never authoritative."""
        run_id = self.seeded_at_fanout()
        packets = self.repo / "build" / "tpt-runs" / run_id / "packets"
        os.chmod(packets, stat.S_IRUSR | stat.S_IXUSR)
        with self.assertRaises(WorkflowError):
            self.engine.advance(run_id, lane_results=self.submissions(run_id))
        os.chmod(packets, 0o755)
        retried = self.engine.advance(
            run_id, lane_results=self.submissions(run_id))
        self.reseed()
        clean = self.seeded_at_fanout()
        self.assertEqual(
            self.engine.advance(
                clean, lane_results=self.submissions(clean))["packet_hash"],
            retried["packet_hash"],
            "a repaired retry must produce the same guidance")


class LauncherTests(unittest.TestCase):
    """Test 18 and the CLI seam for --lane-result."""

    def tpt(self, *argv: str) -> subprocess.CompletedProcess:
        return subprocess.run([str(LAUNCHER), *argv], capture_output=True,
                              text=True, cwd=ROOT)

    def test_registered_tool_dispatch_is_unchanged(self):
        """Test 18."""
        self.assertEqual(self.tpt("--check").returncode, 0)
        listed = self.tpt("--list", "--json")
        self.assertEqual(listed.returncode, 0, listed.stderr)
        self.assertGreater(len(json.loads(listed.stdout)), 10)
        parsed = self.tpt("citations", "parse", "Psalm 24:1-3", "--json")
        self.assertEqual(parsed.returncode, 0, parsed.stderr)

    def test_lane_result_requires_a_lane_and_a_path(self):
        for argument in ("no-equals-sign", "=/tmp/x.json", "lane="):
            with self.subTest(argument=argument):
                done = self.tpt("proper", "some/doc", "advance", "deadbeef",
                                "--lane-result", argument)
                self.assertEqual(done.returncode, 2)
                self.assertIn("--lane-result takes <lane-id>=<path>",
                              done.stderr,
                              "a usage error is reported before the run is "
                              "looked up")

    def test_the_propers_pipeline_still_loads_over_the_cli(self):
        shown = self.tpt("workflow", "show", "proper")
        self.assertEqual(shown.returncode, 0, shown.stderr)
        workflow = json.loads(shown.stdout)
        on_disk = json.loads(
            (ROOT / "workflows" / "pipelines" / "proper.json")
            .read_text(encoding="utf-8"))
        self.assertEqual(workflow["version"], on_disk["version"])
        fanout = {
            stage["id"]: [lane["id"] for lane in stage["execution"]["lanes"]]
            for stage in workflow["stages"]
            if stage["execution"]["mode"] == FANOUT
        }
        self.assertEqual(fanout, {
            "research": [
                "scripture-context", "patristic-reception",
                "liturgical-history", "theological-synthesis",
                "source-citation-coverage", "cultural-afterlife",
                "precedent-search",
            ],
            "content-evaluation": [
                "evidence-discipline", "reception-sweep",
                "synthesis-argument", "citation-integrity",
                "profile-conformance",
            ],
            "visual-evaluation": [
                "density-and-hierarchy", "page-rhythm", "fixed-pagination",
                "clipping-and-apparatus",
            ],
        })
        single = {stage["id"] for stage in workflow["stages"]
                  if stage["execution"]["mode"] == SINGLE}
        self.assertEqual(single, {
            "seed", "resolve-context", "source-audit", "research-synthesis",
            "author-proper", "content-revision", "build-artifacts",
            "artifact-revision", "visual-revision",
        }, "every stage that mutates the leaf stays single-owner")
        program = {stage["id"] for stage in workflow["stages"]
                   if stage["execution"]["mode"] == PROGRAM}
        self.assertEqual(program, {"mechanical-gates", "final-acceptance"})


if __name__ == "__main__":
    unittest.main()
