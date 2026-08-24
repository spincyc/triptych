"""Adversarial regression tests for the deterministic guidance engine.

Each test here corresponds to a defect found by attacking the engine rather
than by exercising it. They guard the invariant the engine exists to hold:

    Given the same repository commit, workflow version, document type,
    arguments, workflow state, and prior structured results, tpt emits the
    same next guidance packet byte-for-byte, and no AI agent decides what
    guidance its successor receives.

Every test uses a synthetic repository in a temporary directory and a private
runs directory, so none of them can see or touch an operator's run state.
"""

from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))

from _workflow import (  # noqa: E402
    WorkflowEngine,
    WorkflowError,
    ACCEPTED,
    BLOCKED,
)

sys.path.insert(0, str(Path(__file__).resolve().parent))

from test_workflow_determinism import (  # noqa: E402
    _answer,
    _make_synthetic_repo,
    _write_result,
)


def _git_init(repo: Path) -> None:
    env = {**os.environ,
           "GIT_AUTHOR_NAME": "test", "GIT_AUTHOR_EMAIL": "test@test",
           "GIT_COMMITTER_NAME": "test", "GIT_COMMITTER_EMAIL": "test@test"}
    subprocess.run(["git", "init"], cwd=repo, capture_output=True)
    subprocess.run(["git", "add", "."], cwd=repo, capture_output=True)
    subprocess.run(["git", "commit", "-m", "init"], cwd=repo,
                   capture_output=True, env=env)


class SyntheticRepoTest(unittest.TestCase):
    """A synthetic repo and a private runs directory per test."""

    def setUp(self):
        self.repo, _ = _make_synthetic_repo()
        self.runs = Path(tempfile.mkdtemp(prefix="tpt-adv-runs-"))
        self.engine = WorkflowEngine(
            self.repo, self.repo / "workflows", runs_dir=self.runs
        )
        self.work = Path(tempfile.mkdtemp(prefix="tpt-adv-work-"))

    def tearDown(self):
        for path in (self.repo, self.runs, self.work):
            shutil.rmtree(path, ignore_errors=True)

    def seed(self, **args):
        merged = {"doc": "test-doc"}
        merged.update(args)
        return self.engine.seed("test-wf", merged)

    def state(self, run_id):
        return self.engine.load_state(run_id)


class AdvanceAtomicityTests(SyntheticRepoTest):
    """LEAD-01: a run must never be recorded at a stage it never issued."""

    def test_result_refused_for_stage_with_no_packet(self):
        run_id = self.seed()["run_id"]
        # Simulate the window the old advance left open: the state names a
        # stage that no packet was ever emitted for.
        state = self.state(run_id)
        state["current_stage"] = "stage-b"
        self.engine.save_state(run_id, state)

        rf = self.work / "r.json"
        _answer(self.engine, run_id, rf, "PASS")
        with self.assertRaises(WorkflowError) as caught:
            self.engine.advance(run_id, result_path=str(rf))
        self.assertIn("no packet was ever emitted", str(caught.exception))

    def test_failed_compilation_leaves_the_stage_unchanged(self):
        run_id = self.seed()["run_id"]
        frag = self.repo / "workflows" / "fragments" / "synthetic" / "work-b.md"
        frag.unlink()

        rf = self.work / "r.json"
        _answer(self.engine, run_id, rf, "PASS")
        with self.assertRaises(WorkflowError):
            self.engine.advance(run_id, result_path=str(rf))

        state = self.state(run_id)
        self.assertEqual(state["current_stage"], "stage-a",
                         "a failed advance must not move the run")
        self.assertEqual(state["transitions"], [],
                         "a failed advance must record no transition")
        issued = {p["stage"] for p in state["packet_hashes"]}
        self.assertEqual(issued, {"stage-a"})


class SourcePinningTests(SyntheticRepoTest):
    """LEAD-02: a run is bound to the guidance source it was seeded from."""

    def _pass_stage_a(self, run_id):
        rf = self.work / "a.json"
        _answer(self.engine, run_id, rf, "PASS")
        return self.engine.advance(run_id, result_path=str(rf))

    def test_packet_header_records_the_source_digest(self):
        seeded = self.seed()
        packet = Path(seeded["packet_abs_path"]).read_text(encoding="utf-8")
        digest = self.state(seeded["run_id"])["source_digest"]
        self.assertIn(f"SOURCE_DIGEST: {digest}", packet,
                      "the packet must state which guidance source produced it")

    def test_edited_fragment_stops_the_run(self):
        run_id = self.seed()["run_id"]
        frag = self.repo / "workflows" / "fragments" / "synthetic" / "work-b.md"
        frag.write_text("# Stage B\n\nDo something else entirely.",
                        encoding="utf-8")
        rf = self.work / "a.json"
        _answer(self.engine, run_id, rf, "PASS")
        with self.assertRaises(WorkflowError) as caught:
            self.engine.advance(run_id, result_path=str(rf))
        self.assertIn("guidance source changed", str(caught.exception))

    def test_edited_pipeline_without_a_version_bump_stops_the_run(self):
        run_id = self.seed()["run_id"]
        path = self.repo / "workflows" / "pipelines" / "test-wf.json"
        wf = json.loads(path.read_text(encoding="utf-8"))
        for stage in wf["stages"]:
            if stage["id"] == "stage-a":
                stage["next"] = "final"
        path.write_text(json.dumps(wf, sort_keys=True, indent=2),
                        encoding="utf-8")
        rf = self.work / "a.json"
        _answer(self.engine, run_id, rf, "PASS")
        with self.assertRaises(WorkflowError) as caught:
            self.engine.advance(run_id, result_path=str(rf))
        self.assertIn("guidance source changed", str(caught.exception))

    def test_edited_schema_stops_the_run(self):
        run_id = self.seed()["run_id"]
        path = self.repo / "workflows" / "schema" / "worker-result.json"
        schema = json.loads(path.read_text(encoding="utf-8"))
        schema["valid_dispositions"] = ["PASS", "WHATEVER"]
        path.write_text(json.dumps(schema), encoding="utf-8")
        rf = self.work / "a.json"
        _answer(self.engine, run_id, rf, "PASS")
        with self.assertRaises(WorkflowError):
            self.engine.advance(run_id, result_path=str(rf))

    def test_manifest_is_load_bearing(self):
        run_id = self.seed()["run_id"]
        state = self.state(run_id)
        state["normalized_args"]["doc"] = "some-other-doc"
        self.engine.save_state(run_id, state)
        rf = self.work / "a.json"
        _answer(self.engine, run_id, rf, "PASS")
        with self.assertRaises(WorkflowError) as caught:
            self.engine.advance(run_id, result_path=str(rf))
        self.assertIn("disagrees with its manifest", str(caught.exception))

    def test_untouched_source_still_advances(self):
        run_id = self.seed()["run_id"]
        out = self._pass_stage_a(run_id)
        self.assertEqual(out["stage"], "stage-b",
                         "an unmodified source must not be treated as drift")


class WorkerRefusalTests(SyntheticRepoTest):
    """LEAD-03: a worker that cannot do the work must be able to say so."""

    def test_worker_blocked_stops_the_run(self):
        run_id = self.seed()["run_id"]
        path = self.repo / "workflows" / "schema" / "worker-result.json"
        schema = json.loads(path.read_text(encoding="utf-8"))
        schema["valid_dispositions"] = ["PASS", "BLOCKED"]
        path.write_text(json.dumps(schema), encoding="utf-8")
        # Re-seed so the run is bound to the amended schema.
        self.engine = WorkflowEngine(
            self.repo, self.repo / "workflows", runs_dir=self.runs
        )
        shutil.rmtree(self.runs / run_id)
        run_id = self.seed()["run_id"]

        rf = self.work / "a.json"
        state = self.engine.load_state(run_id)
        rf.write_text(json.dumps({
            "packet_hash": state["packet_hashes"][-1]["hash"],
            "disposition": "BLOCKED",
            "summary": "the source material does not exist",
            "block_reason": "the source material does not exist",
        }), encoding="utf-8")
        out = self.engine.advance(run_id, result_path=str(rf))
        self.assertEqual(out["disposition"], BLOCKED)
        self.assertIn("source material", out["message"])


class GateBudgetTests(unittest.TestCase):
    """LEAD-04: a gate's budget is spent by its own failures, not by every
    time some other revision loop happens to re-enter it."""

    def setUp(self):
        self.repo = Path(tempfile.mkdtemp(prefix="tpt-gatebudget-"))
        self.runs = Path(tempfile.mkdtemp(prefix="tpt-gatebudget-runs-"))
        self.work = Path(tempfile.mkdtemp(prefix="tpt-gatebudget-work-"))
        wf_dir = self.repo / "workflows"
        (wf_dir / "fragments" / "s").mkdir(parents=True, exist_ok=True)
        (wf_dir / "pipelines").mkdir(parents=True, exist_ok=True)
        (wf_dir / "schema").mkdir(parents=True, exist_ok=True)
        (wf_dir / "fragments" / "s" / "f.md").write_text("f", encoding="utf-8")
        (wf_dir / "schema" / "worker-result.json").write_text(json.dumps({
            "required_fields": ["disposition", "summary"],
            "valid_dispositions": ["PASS", "BLOCKED"], "finding_fields": [],
        }), encoding="utf-8")
        (wf_dir / "schema" / "evaluator-result.json").write_text(json.dumps({
            "required_fields": ["disposition", "findings"],
            "valid_dispositions": ["PASS", "CHANGES_REQUIRED", "BLOCKED"],
            "finding_fields": ["id", "severity", "problem"],
        }), encoding="utf-8")
        frags = ["s/f.md"]
        workflow = {
            "id": "budget", "version": 1, "description": "gate budget",
            "argument_schema": {"doc": {"required": True, "type": "string"}},
            "stages": [
                {"id": "work", "type": "linear", "fragments": frags,
                 "result_schema": "worker-result.json", "next": "gate"},
                {"id": "gate", "type": "gate",
                 "checks": [{"id": "marker", "command": "test -f marker",
                             "required_result": "marker must exist"}],
                 "pass_transition": "vis", "fail_transition": "gate-rev",
                 "max_iterations": 3},
                {"id": "gate-rev", "type": "bounded-revision",
                 "revision_target": "work", "fragments": frags,
                 "result_schema": "worker-result.json", "next": "gate"},
                {"id": "vis", "type": "evaluator", "fragments": frags,
                 "result_schema": "evaluator-result.json",
                 "pass_transition": "ACCEPTED", "fail_transition": "vis-rev",
                 "max_iterations": 3},
                {"id": "vis-rev", "type": "bounded-revision",
                 "revision_target": "work", "fragments": frags,
                 "result_schema": "worker-result.json", "next": "gate"},
            ],
        }
        (wf_dir / "pipelines" / "budget.json").write_text(
            json.dumps(workflow, sort_keys=True, indent=2), encoding="utf-8")
        (self.repo / "marker").write_text("present", encoding="utf-8")
        _git_init(self.repo)
        self.engine = WorkflowEngine(
            self.repo, self.repo / "workflows", runs_dir=self.runs)

    def tearDown(self):
        for path in (self.repo, self.runs, self.work):
            shutil.rmtree(path, ignore_errors=True)

    def _pass(self, run_id):
        rf = self.work / "w.json"
        _answer(self.engine, run_id, rf, "PASS")
        return self.engine.advance(run_id, result_path=str(rf))

    def _evaluator(self, run_id, disposition):
        rf = self.work / "e.json"
        state = self.engine.load_state(run_id)
        rf.write_text(json.dumps({
            "packet_hash": state["packet_hashes"][-1]["hash"],
            "disposition": disposition,
            "summary": "x",
            "findings": [] if disposition == "PASS" else [
                {"id": "V-1", "severity": "blocking", "problem": "off"}],
        }), encoding="utf-8")
        return self.engine.advance(run_id, result_path=str(rf))

    def test_gate_budget_survives_an_unrelated_revision_loop(self):
        out = self.engine.seed("budget", {"doc": "d"})
        run_id = out["run_id"]
        self.assertEqual(out["stage"], "work")

        out = self._pass(run_id)                       # work -> gate
        self.assertEqual(out["stage"], "gate")

        # The gate passes; the visual evaluator refuses twice. Each refusal
        # re-enters the gate, which passes again. The gate has failed nothing.
        for _ in range(2):
            out = self.engine.advance(run_id, run_gate=True)
            self.assertEqual(out["stage"], "vis")
            out = self._evaluator(run_id, "CHANGES_REQUIRED")
            self.assertEqual(out["stage"], "vis-rev")
            out = self._pass(run_id)
            self.assertEqual(out["stage"], "gate")

        state = self.engine.load_state(run_id)
        self.assertGreaterEqual(state["stage_iterations"]["gate"], 3,
                                "the gate has been entered at least 3 times")
        self.assertEqual(state["stage_failures"].get("gate", 0), 0,
                         "but it has failed nothing")

        # Now the gate genuinely fails for the first time. It must be allowed
        # its own revision loop, not blocked on someone else's iterations.
        (self.repo / "marker").unlink()
        out = self.engine.advance(run_id, run_gate=True)
        self.assertEqual(out["stage"], "gate-rev",
                         "a gate's first real failure must enter its revision "
                         "loop, not exhaust a budget spent elsewhere")

    def test_gate_still_blocks_on_its_own_repeated_failures(self):
        out = self.engine.seed("budget", {"doc": "d"})
        run_id = out["run_id"]
        self._pass(run_id)
        (self.repo / "marker").unlink()

        # max_iterations=3 means the third consecutive failure blocks.
        for _ in range(2):
            out = self.engine.advance(run_id, run_gate=True)
            self.assertEqual(out["stage"], "gate-rev")
            out = self._pass(run_id)
            self.assertEqual(out["stage"], "gate")
        out = self.engine.advance(run_id, run_gate=True)
        self.assertEqual(out["disposition"], BLOCKED,
                         "max_iterations=3 must still bound a gate that keeps "
                         "failing")
        self.assertIn("iteration limit exceeded", out["message"])


class GateExecutionSafetyTests(unittest.TestCase):
    """LEAD-05: gate checks are argv, never a shell command line."""

    def setUp(self):
        self.repo = Path(tempfile.mkdtemp(prefix="tpt-gatesafe-"))
        self.runs = Path(tempfile.mkdtemp(prefix="tpt-gatesafe-runs-"))

    def tearDown(self):
        for path in (self.repo, self.runs):
            shutil.rmtree(path, ignore_errors=True)

    def _build(self, check_command):
        wf_dir = self.repo / "workflows"
        (wf_dir / "fragments" / "s").mkdir(parents=True, exist_ok=True)
        (wf_dir / "pipelines").mkdir(parents=True, exist_ok=True)
        (wf_dir / "schema").mkdir(parents=True, exist_ok=True)
        (wf_dir / "fragments" / "s" / "f.md").write_text("f", encoding="utf-8")
        (wf_dir / "schema" / "worker-result.json").write_text(json.dumps({
            "required_fields": ["disposition", "summary"],
            "valid_dispositions": ["PASS"], "finding_fields": [],
        }), encoding="utf-8")
        workflow = {
            "id": "safe", "version": 1, "description": "gate safety",
            "argument_schema": {"doc": {"required": True, "type": "string"}},
            "stages": [
                {"id": "gate", "type": "gate",
                 "checks": [{"id": "c", "command": check_command,
                             "required_result": "must pass"}],
                 "pass_transition": "ACCEPTED", "fail_transition": "BLOCKED",
                 "max_iterations": 1},
            ],
        }
        (wf_dir / "pipelines" / "safe.json").write_text(
            json.dumps(workflow, sort_keys=True, indent=2), encoding="utf-8")
        _git_init(self.repo)
        return WorkflowEngine(
            self.repo, self.repo / "workflows", runs_dir=self.runs)

    def test_hostile_argument_value_is_refused_at_seed(self):
        engine = self._build("echo {doc}")
        with self.assertRaises(WorkflowError) as caught:
            engine.seed("safe", {"doc": "ok; touch pwned"})
        self.assertIn("unacceptable value", str(caught.exception))
        self.assertFalse((self.repo / "pwned").exists(),
                         "no part of a refused argument may be executed")

    def test_gate_command_metacharacters_are_not_shell_syntax(self):
        # If a shell ran this, `pwned` would be created. Under argv it is
        # simply an argument to echo.
        engine = self._build("echo a; touch pwned")
        run_id = engine.seed("safe", {"doc": "d"})["run_id"]
        out = engine.advance(run_id, run_gate=True)
        self.assertEqual(out["disposition"], ACCEPTED)
        self.assertFalse((self.repo / "pwned").exists(),
                         "gate checks must not be interpreted by a shell")

    def test_argument_value_cannot_split_into_extra_argv_words(self):
        engine = self._build("echo {doc}")
        # A space is outside the accepted argument shape, so it never gets
        # as far as the command line.
        with self.assertRaises(WorkflowError):
            engine.seed("safe", {"doc": "one two"})

    def test_legitimate_path_argument_still_works(self):
        engine = self._build("test -f {doc}")
        (self.repo / "present.txt").write_text("x", encoding="utf-8")
        run_id = engine.seed("safe", {"doc": "present.txt"})["run_id"]
        out = engine.advance(run_id, run_gate=True)
        self.assertEqual(out["disposition"], ACCEPTED,
                         "an ordinary path argument must still reach the check")


class RefusedResultResidueTests(SyntheticRepoTest):
    """LEAD-06: a result the engine refuses leaves no trace in the run."""

    def test_refused_result_is_not_written_or_hashed(self):
        # Point stage-a at the evaluator schema so a CHANGES_REQUIRED result
        # passes schema validation but is refused by the transition rules.
        path = self.repo / "workflows" / "pipelines" / "test-wf.json"
        wf = json.loads(path.read_text(encoding="utf-8"))
        for stage in wf["stages"]:
            if stage["id"] == "stage-a":
                stage["result_schema"] = "evaluator-result.json"
        path.write_text(json.dumps(wf, sort_keys=True, indent=2),
                        encoding="utf-8")

        run_id = self.seed()["run_id"]
        rf = self.work / "bad.json"
        state = self.engine.load_state(run_id)
        rf.write_text(json.dumps({
            "packet_hash": state["packet_hashes"][-1]["hash"],
            "disposition": "CHANGES_REQUIRED",
            "summary": "not my job",
            "findings": [{"id": "X-1", "severity": "blocking",
                          "location": "here", "problem": "p",
                          "required_result": "r"}],
        }), encoding="utf-8")

        with self.assertRaises(WorkflowError):
            self.engine.advance(run_id, result_path=str(rf))

        state = self.state(run_id)
        self.assertEqual(state["result_hashes"], [],
                         "a refused result must not be recorded")
        results_dir = self.runs / run_id / "results"
        written = sorted(p.name for p in results_dir.glob("*.json")) \
            if results_dir.is_dir() else []
        self.assertEqual(written, [],
                         "a refused result must not be left in results/")


class RunStateIsolationTests(unittest.TestCase):
    """LEAD-07: the engine's runs directory is explicit, so a test run can
    never destroy an operator's run state."""

    def test_runs_dir_is_overridable(self):
        elsewhere = Path(tempfile.mkdtemp(prefix="tpt-elsewhere-"))
        try:
            engine = WorkflowEngine(ROOT, ROOT / "workflows",
                                    runs_dir=elsewhere)
            self.assertEqual(engine.runs_dir, elsewhere.resolve())
            self.assertNotEqual(engine.runs_dir,
                                (ROOT / "build" / "tpt-runs").resolve())
        finally:
            shutil.rmtree(elsewhere, ignore_errors=True)

    def test_default_runs_dir_is_unchanged(self):
        engine = WorkflowEngine(ROOT, ROOT / "workflows")
        self.assertEqual(engine.runs_dir,
                         (ROOT / "build" / "tpt-runs").resolve())

    def test_workflow_suites_leave_live_run_state_alone(self):
        """Running the workflow suites must not destroy an operator's runs."""
        live = ROOT / "build" / "tpt-runs"
        sentinel = live / "0000000000000000-sentinel"
        sentinel.mkdir(parents=True, exist_ok=True)
        (sentinel / "state.json").write_text("{}\n", encoding="utf-8")
        try:
            proc = subprocess.run(
                [sys.executable, "-m", "unittest",
                 "tools.tests.test_workflow_engine",
                 "tools.tests.test_workflow_determinism"],
                cwd=ROOT, capture_output=True, text=True,
            )
            self.assertEqual(proc.returncode, 0, proc.stderr[-2000:])
            self.assertTrue(
                sentinel.is_dir(),
                "the workflow test suites deleted live run state under "
                "build/tpt-runs"
            )
        finally:
            shutil.rmtree(sentinel, ignore_errors=True)


class ResultBindingTests(SyntheticRepoTest):
    """LEAD-08: a result must answer the packet that was actually issued.

    Without this the parent driver decides, in effect, which guidance a stage
    was answering: it can hold a result produced for one packet and submit it
    against another.
    """

    def test_result_without_a_packet_hash_is_refused(self):
        run_id = self.seed()["run_id"]
        rf = self.work / "a.json"
        _write_result(rf, "PASS")  # deliberately omits packet_hash
        with self.assertRaises(WorkflowError) as caught:
            self.engine.advance(run_id, result_path=str(rf))
        self.assertIn("does not say which packet it answers",
                      str(caught.exception))

    def test_result_for_a_different_packet_is_refused(self):
        run_id = self.seed()["run_id"]
        rf = self.work / "a.json"
        _write_result(rf, "PASS", packet_hash="0" * 64)
        with self.assertRaises(WorkflowError) as caught:
            self.engine.advance(run_id, result_path=str(rf))
        self.assertIn("answers packet", str(caught.exception))

    def test_a_stale_result_cannot_be_resubmitted_after_advancing(self):
        run_id = self.seed()["run_id"]
        stale = self.work / "stale.json"
        _answer(self.engine, run_id, stale, "PASS")
        out = self.engine.advance(run_id, result_path=str(stale))
        self.assertEqual(out["stage"], "stage-b")

        # The same file, now answering guidance already answered.
        with self.assertRaises(WorkflowError) as caught:
            self.engine.advance(run_id, result_path=str(stale))
        self.assertIn("answers packet", str(caught.exception))
        state = self.state(run_id)
        self.assertEqual(state["current_stage"], "stage-b",
                         "a replayed result must not move the run")
        self.assertEqual(len(state["result_hashes"]), 1,
                         "a replayed result must not be recorded twice")

    def test_driver_instructions_state_the_packet_hash(self):
        seeded = self.seed()
        self.assertIn(seeded["packet_hash"], seeded["instructions"],
                      "the driver must be told the hash the worker has to "
                      "repeat")

    def test_a_valid_answer_still_advances(self):
        run_id = self.seed()["run_id"]
        rf = self.work / "a.json"
        _answer(self.engine, run_id, rf, "PASS")
        out = self.engine.advance(run_id, result_path=str(rf))
        self.assertEqual(out["stage"], "stage-b")


class LauncherSurfaceTests(unittest.TestCase):
    """Capabilities the documentation promises must actually be reachable,
    and an ambiguous name must be refused rather than silently resolved."""

    LAUNCHER = ROOT / "tools" / "tpt"

    def _tpt(self, *argv):
        return subprocess.run([str(self.LAUNCHER), *argv],
                              cwd=ROOT, capture_output=True, text=True)

    def test_replay_is_reachable_from_the_cli(self):
        proc = self._tpt("proper", "x", "replay")
        self.assertNotIn("unknown workflow action", proc.stderr,
                         "replay must be a real action, not documentation only")
        self.assertIn("replay: missing run-id", proc.stderr)

    def test_actions_list_matches_the_actions_implemented(self):
        proc = self._tpt("proper", "x", "no-such-action")
        for action in ("seed", "advance", "status", "replay", "intervene",
                       "debt"):
            self.assertIn(action, proc.stderr,
                          f"the action list must name {action}")

    def test_exact_collision_is_refused_before_tool_dispatch(self):
        """A workflow id equal to a tool id must be reported, not shadowed."""
        pipelines = ROOT / "workflows" / "pipelines"
        colliding = pipelines / "check-proper-components.json"
        self.assertFalse(colliding.exists(),
                         "test would clobber a real pipeline")
        colliding.write_text(json.dumps({
            "id": "check-proper-components", "version": 1,
            "description": "collision fixture",
            "stages": [{"id": "s", "type": "linear",
                        "fragments": [], "next": "ACCEPTED"}],
        }), encoding="utf-8")
        try:
            proc = self._tpt("check-proper-components", "--help")
            self.assertNotEqual(proc.returncode, 0,
                                "an ambiguous id must not silently run the tool")
            self.assertIn("collides with registered tool id", proc.stderr)
        finally:
            colliding.unlink()


class PropersWorkflowRefusalTests(unittest.TestCase):
    """LEAD-03 in the shipped pipeline: final acceptance must be able to
    refuse, and no fragment may tell a worker to claim success falsely."""

    @classmethod
    def setUpClass(cls):
        cls.workflow = json.loads(
            (ROOT / "workflows" / "pipelines" / "proper.json").read_text(
                encoding="utf-8"))
        cls.stages = {s["id"]: s for s in cls.workflow["stages"]}

    def test_final_acceptance_can_refuse(self):
        stage = self.stages["final-acceptance"]
        self.assertEqual(stage["type"], "evaluator",
                         "final acceptance must be able to return something "
                         "other than PASS")
        self.assertEqual(stage["pass_transition"], "ACCEPTED")
        self.assertIn(stage["fail_transition"], self.stages,
                      "a refusal must route to a real revision stage")

    def test_final_acceptance_refusal_re_enters_the_gates(self):
        target = self.stages[self.stages["final-acceptance"]["fail_transition"]]
        self.assertEqual(target["next"], "mechanical-gates",
                         "work revised after a refused acceptance must be "
                         "re-checked mechanically")

    def test_every_terminal_path_is_reachable(self):
        targets = set()
        for stage in self.workflow["stages"]:
            for key in ("next", "pass_transition", "fail_transition"):
                if key in stage:
                    targets.add(stage[key])
        self.assertIn(ACCEPTED, targets)

    def test_worker_schema_admits_refusal(self):
        schema = json.loads(
            (ROOT / "workflows" / "schema" / "worker-result.json").read_text(
                encoding="utf-8"))
        self.assertIn("BLOCKED", schema["valid_dispositions"],
                      "a worker that cannot do the work must be able to say so")

    def test_result_format_does_not_instruct_a_false_pass(self):
        text = (ROOT / "workflows" / "fragments" / "common" /
                "result-format.md").read_text(encoding="utf-8")
        self.assertNotIn('set\n`disposition` to `"PASS"` with a `summary` '
                         'explaining the partial state', text)
        self.assertIn("BLOCKED", text,
                      "workers must be told how to refuse")


if __name__ == "__main__":
    unittest.main()
