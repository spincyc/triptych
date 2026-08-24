"""Tests for the deterministic workflow engine: packet compilation, hashing,
determinism, fragment ordering, and run-state reload.

These tests use synthetic fixtures in a temporary directory so they do not
depend on the real propers workflow or a live AI provider.
"""

from __future__ import annotations

import hashlib
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
    PASS,
    CHANGES_REQUIRED,
    FAIL,
)


def _make_synthetic_repo() -> tuple[Path, Path]:
    """Create a temp repo with a synthetic workflow, fragments, and schemas.

    Returns (repo_root, runs_parent).
    """
    repo = Path(tempfile.mkdtemp(prefix="tpt-wf-test-"))
    workflows = repo / "workflows"
    fragments = workflows / "fragments" / "synthetic"
    pipelines = workflows / "pipelines"
    schemas = workflows / "schema"
    for d in (fragments, pipelines, schemas):
        d.mkdir(parents=True, exist_ok=True)

    # Schemas
    (schemas / "worker-result.json").write_text(json.dumps({
        "name": "worker-result",
        "required_fields": ["disposition", "summary"],
        "valid_dispositions": ["PASS"],
        "finding_fields": [],
    }), encoding="utf-8")
    (schemas / "evaluator-result.json").write_text(json.dumps({
        "name": "evaluator-result",
        "required_fields": ["disposition", "findings"],
        "valid_dispositions": ["PASS", "CHANGES_REQUIRED", "BLOCKED"],
        "finding_fields": ["id", "severity", "location", "problem", "required_result"],
    }), encoding="utf-8")
    (schemas / "gate-result.json").write_text(json.dumps({
        "name": "gate-result",
        "required_fields": ["disposition", "findings"],
        "valid_dispositions": ["PASS", "FAIL"],
        "finding_fields": ["id", "severity", "check", "problem", "required_result"],
    }), encoding="utf-8")

    # Fragments
    for name, content in [
        ("brief.md", "# Brief\n\nYou are a test worker."),
        ("format.md", "# Format\n\nReturn JSON."),
        ("work-a.md", "# Stage A\n\nDo work A."),
        ("work-b.md", "# Stage B\n\nDo work B."),
        ("eval.md", "# Evaluator\n\nEvaluate the work."),
        ("revise.md", "# Revision\n\nFix the findings."),
    ]:
        (fragments / name).write_text(content, encoding="utf-8")

    # Workflow definition: a simple linear→evaluator→revision→gate→accept pipeline
    workflow = {
        "id": "test-wf",
        "version": 1,
        "description": "Synthetic test workflow",
        "argument_schema": {
            "doc": {"type": "string", "required": True, "description": "doc id"},
            "provider": {"type": "string", "required": False, "default": "gpt",
                         "description": "provider"},
        },
        "stages": [
            {
                "id": "stage-a",
                "type": "linear",
                "fragments": ["synthetic/brief.md", "synthetic/format.md", "synthetic/work-a.md"],
                "result_schema": "worker-result.json",
                "next": "stage-b",
            },
            {
                "id": "stage-b",
                "type": "linear",
                "fragments": ["synthetic/brief.md", "synthetic/format.md", "synthetic/work-b.md"],
                "result_schema": "worker-result.json",
                "next": "eval-stage",
            },
            {
                "id": "eval-stage",
                "type": "evaluator",
                "fragments": ["synthetic/brief.md", "synthetic/format.md", "synthetic/eval.md"],
                "result_schema": "evaluator-result.json",
                "pass_transition": "gate-stage",
                "fail_transition": "revise-stage",
                "max_iterations": 2,
            },
            {
                "id": "revise-stage",
                "type": "bounded-revision",
                "revision_target": "stage-b",
                "fragments": ["synthetic/brief.md", "synthetic/format.md", "synthetic/revise.md",
                              "synthetic/work-b.md"],
                "result_schema": "worker-result.json",
                "next": "eval-stage",
            },
            {
                "id": "gate-stage",
                "type": "gate",
                "checks": [
                    {"id": "true-check", "command": "true",
                     "required_result": "must pass"},
                ],
                "pass_transition": "final",
                "fail_transition": "gate-revise",
                "max_iterations": 2,
            },
            {
                "id": "gate-revise",
                "type": "bounded-revision",
                "revision_target": "stage-b",
                "fragments": ["synthetic/brief.md", "synthetic/format.md", "synthetic/revise.md",
                              "synthetic/work-b.md"],
                "result_schema": "worker-result.json",
                "next": "gate-stage",
            },
            {
                "id": "final",
                "type": "linear",
                "fragments": ["synthetic/brief.md", "synthetic/format.md"],
                "result_schema": "worker-result.json",
                "next": "ACCEPTED",
            },
        ],
    }
    (pipelines / "test-wf.json").write_text(
        json.dumps(workflow, sort_keys=True, indent=2), encoding="utf-8"
    )

    # Initialize as a git repo so get_repo_commit works
    subprocess.run(["git", "init"], cwd=repo, capture_output=True)  # noqa
    subprocess.run(["git", "add", "."], cwd=repo, capture_output=True)  # noqa
    subprocess.run(["git", "commit", "-m", "init"], cwd=repo,
                   capture_output=True, env={**os.environ, "GIT_AUTHOR_NAME": "test",
                                             "GIT_AUTHOR_EMAIL": "test@test",
                                             "GIT_COMMITTER_NAME": "test",
                                             "GIT_COMMITTER_EMAIL": "test@test"})

    return repo, repo / "build" / "tpt-runs"


def _write_result(path: Path, disposition: str,
                  findings: list | None = None, summary: str = "test",
                  packet_hash: str | None = None) -> str:
    """Write a structured result to a file and return its path.

    A result must name the packet it answers, so `packet_hash` is normally
    supplied. It is optional only so that a test can deliberately omit it.
    """
    result = {"disposition": disposition, "summary": summary}
    if findings is not None:
        result["findings"] = findings
    if packet_hash is not None:
        result["packet_hash"] = packet_hash
    path.write_text(json.dumps(result), encoding="utf-8")
    return str(path)


def _answer(engine, run_id: str, path: Path, disposition: str,
            findings: list | None = None, summary: str = "test") -> str:
    """Write a result that answers the packet currently awaiting an answer."""
    state = engine.load_state(run_id)
    return _write_result(
        path, disposition, findings=findings, summary=summary,
        packet_hash=state["packet_hashes"][-1]["hash"],
    )


class PacketDeterminismTests(unittest.TestCase):
    """Tests 1-3: identical state → byte-identical packet, identical hash,
    stable fragment order."""

    @classmethod
    def setUpClass(cls):
        cls.repo, cls.runs_dir = _make_synthetic_repo()
        cls.engine = WorkflowEngine(cls.repo, cls.repo / "workflows")

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.repo, ignore_errors=True)

    def setUp(self):
        # Clean runs between tests
        runs = self.repo / "build" / "tpt-runs"
        if runs.exists():
            shutil.rmtree(runs)

    def test_identical_state_byte_identical_packet(self):
        """Test 1: same inputs → byte-identical packet bytes."""
        r1 = self.engine.seed("test-wf", {"doc": "test-doc", "provider": "gpt"})
        pkt1 = Path(r1["packet_abs_path"]).read_bytes()
        run_id = r1["run_id"]
        shutil.rmtree(self.repo / "build" / "tpt-runs" / run_id)

        r2 = self.engine.seed("test-wf", {"doc": "test-doc", "provider": "gpt"})
        pkt2 = Path(r2["packet_abs_path"]).read_bytes()

        self.assertEqual(pkt1, pkt2,
                         "identical inputs must produce byte-identical packets")

    def test_identical_state_identical_hash(self):
        """Test 2: same inputs → identical SHA-256."""
        r1 = self.engine.seed("test-wf", {"doc": "test-doc", "provider": "gpt"})
        h1 = r1["packet_hash"]
        run_id = r1["run_id"]
        shutil.rmtree(self.repo / "build" / "tpt-runs" / run_id)

        r2 = self.engine.seed("test-wf", {"doc": "test-doc", "provider": "gpt"})
        h2 = r2["packet_hash"]

        self.assertEqual(h1, h2,
                         "identical inputs must produce identical SHA-256 hashes")

    def test_fragment_order_is_stable(self):
        """Test 3: fragment order in the packet matches the declared order."""
        result = self.engine.seed("test-wf", {"doc": "test-doc", "provider": "gpt"})
        packet = Path(result["packet_abs_path"]).read_text(encoding="utf-8")

        # The fragments for stage-a are: brief.md, format.md, work-a.md
        idx_brief = packet.find("FRAGMENT: synthetic/brief.md")
        idx_format = packet.find("FRAGMENT: synthetic/format.md")
        idx_work = packet.find("FRAGMENT: synthetic/work-a.md")

        self.assertGreater(idx_brief, 0, "brief.md not found in packet")
        self.assertGreater(idx_format, 0, "format.md not found in packet")
        self.assertGreater(idx_work, 0, "work-a.md not found in packet")
        self.assertLess(idx_brief, idx_format, "brief.md must come before format.md")
        self.assertLess(idx_format, idx_work, "format.md must come before work-a.md")

    def test_different_args_different_hash(self):
        """Different arguments produce different hashes (negative test)."""
        r1 = self.engine.seed("test-wf", {"doc": "doc-a", "provider": "gpt"})
        shutil.rmtree(self.repo / "build" / "tpt-runs" / r1["run_id"])
        r2 = self.engine.seed("test-wf", {"doc": "doc-b", "provider": "gpt"})

        self.assertNotEqual(r1["packet_hash"], r2["packet_hash"],
                            "different args must produce different hashes")

    def test_hash_is_sha256(self):
        """The recorded hash matches an independent SHA-256 computation."""
        result = self.engine.seed("test-wf", {"doc": "test-doc", "provider": "gpt"})
        pkt_bytes = Path(result["packet_abs_path"]).read_bytes()
        independent = hashlib.sha256(pkt_bytes).hexdigest()
        self.assertEqual(result["packet_hash"], independent)


class FailClosedTests(unittest.TestCase):
    """Test 4: malformed result → fail closed."""

    @classmethod
    def setUpClass(cls):
        cls.repo, cls.runs_dir = _make_synthetic_repo()
        cls.engine = WorkflowEngine(cls.repo, cls.repo / "workflows")

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.repo, ignore_errors=True)

    def setUp(self):
        runs = self.repo / "build" / "tpt-runs"
        if runs.exists():
            shutil.rmtree(runs)

    def test_malformed_json_fails_closed(self):
        """Malformed JSON result causes an error, not a transition."""
        result = self.engine.seed("test-wf", {"doc": "test-doc", "provider": "gpt"})
        run_id = result["run_id"]
        bad = self.repo / "bad.json"
        bad.write_text("{not valid json", encoding="utf-8")
        with self.assertRaises(WorkflowError):
            self.engine.advance(run_id, result_path=str(bad))

    def test_missing_disposition_fails_closed(self):
        """Result missing required field causes an error."""
        result = self.engine.seed("test-wf", {"doc": "test-doc", "provider": "gpt"})
        run_id = result["run_id"]
        bad = self.repo / "bad.json"
        bad.write_text(json.dumps({"summary": "no disposition"}), encoding="utf-8")
        with self.assertRaises(WorkflowError):
            self.engine.advance(run_id, result_path=str(bad))

    def test_invalid_disposition_fails_closed(self):
        """Result with invalid disposition value causes an error."""
        result = self.engine.seed("test-wf", {"doc": "test-doc", "provider": "gpt"})
        run_id = result["run_id"]
        bad = self.repo / "bad.json"
        bad.write_text(json.dumps({"disposition": "MAYBE", "summary": "x"}), encoding="utf-8")
        with self.assertRaises(WorkflowError):
            self.engine.advance(run_id, result_path=str(bad))

    def test_missing_result_file_fails_closed(self):
        """Non-existent result file causes an error."""
        result = self.engine.seed("test-wf", {"doc": "test-doc", "provider": "gpt"})
        run_id = result["run_id"]
        with self.assertRaises(WorkflowError):
            self.engine.advance(run_id, result_path="/no/such/file.json")


class TransitionTests(unittest.TestCase):
    """Tests 5-6: PASS selects correct next state, CHANGES_REQUIRED selects
    bounded revision."""

    @classmethod
    def setUpClass(cls):
        cls.repo, cls.runs_dir = _make_synthetic_repo()
        cls.engine = WorkflowEngine(cls.repo, cls.repo / "workflows")

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.repo, ignore_errors=True)

    def setUp(self):
        runs = self.repo / "build" / "tpt-runs"
        if runs.exists():
            shutil.rmtree(runs)

    def _seed_and_advance_to(self, target_stage: str) -> str:
        """Seed and advance through linear stages until reaching target_stage."""
        result = self.engine.seed("test-wf", {"doc": "test-doc", "provider": "gpt"})
        run_id = result["run_id"]

        # Advance through stages until we reach the target
        while result["stage"] != target_stage:
            if result.get("disposition") in (ACCEPTED, BLOCKED):
                self.fail(f"reached terminal state before {target_stage}")
            rfile = self.repo / f"result-{result['stage']}.json"
            _answer(self.engine, run_id, rfile, PASS)
            result = self.engine.advance(run_id, result_path=str(rfile))
        return run_id

    def test_pass_selects_next_linear_stage(self):
        """Test 5: PASS on a linear stage selects the correct next state."""
        result = self.engine.seed("test-wf", {"doc": "test-doc", "provider": "gpt"})
        run_id = result["run_id"]
        self.assertEqual(result["stage"], "stage-a")

        rfile = self.repo / "r.json"
        _answer(self.engine, run_id, rfile, PASS)
        result = self.engine.advance(run_id, result_path=str(rfile))
        self.assertEqual(result["stage"], "stage-b",
                         "PASS on stage-a must advance to stage-b")

    def test_pass_on_evaluator_selects_pass_transition(self):
        """Test 5b: PASS on an evaluator selects pass_transition."""
        run_id = self._seed_and_advance_to("eval-stage")
        rfile = self.repo / "r.json"
        _answer(self.engine, run_id, rfile, PASS, findings=[])
        result = self.engine.advance(run_id, result_path=str(rfile))
        self.assertEqual(result["stage"], "gate-stage",
                         "PASS on eval-stage must advance to gate-stage")

    def test_changes_required_selects_revision(self):
        """Test 6: CHANGES_REQUIRED on evaluator selects bounded revision."""
        run_id = self._seed_and_advance_to("eval-stage")
        rfile = self.repo / "r.json"
        _answer(self.engine, run_id, rfile, CHANGES_REQUIRED, findings=[
            {"id": "CON-001", "severity": "blocking", "location": "p1",
             "problem": "bad", "required_result": "fix it"}
        ])
        result = self.engine.advance(run_id, result_path=str(rfile))
        self.assertEqual(result["stage"], "revise-stage",
                         "CHANGES_REQUIRED must select the revision stage")


class RevisionForwardingTests(unittest.TestCase):
    """Test 7: revision findings are forwarded without paraphrase."""

    @classmethod
    def setUpClass(cls):
        cls.repo, cls.runs_dir = _make_synthetic_repo()
        cls.engine = WorkflowEngine(cls.repo, cls.repo / "workflows")

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.repo, ignore_errors=True)

    def setUp(self):
        runs = self.repo / "build" / "tpt-runs"
        if runs.exists():
            shutil.rmtree(runs)

    def test_findings_forwarded_verbatim(self):
        """Blocking findings appear in the revision packet's PRIOR_FINDINGS."""
        result = self.engine.seed("test-wf", {"doc": "test-doc", "provider": "gpt"})
        run_id = result["run_id"]

        # Advance to eval-stage
        for _ in range(2):
            rfile = self.repo / f"r-{result['stage']}.json"
            _answer(self.engine, run_id, rfile, PASS)
            result = self.engine.advance(run_id, result_path=str(rfile))

        self.assertEqual(result["stage"], "eval-stage")

        # Submit CHANGES_REQUIRED with specific findings
        findings = [
            {"id": "CON-001", "severity": "blocking", "location": "page 3",
             "problem": "Missing patristic witness for Introit",
             "required_result": "Add at least one direct patristic citation"},
            {"id": "CON-002", "severity": "blocking", "location": "page 5",
             "problem": "Unverified lead presented as fact",
             "required_result": "Label as exploratory or remove"},
        ]
        rfile = self.repo / "r-eval.json"
        _answer(self.engine, run_id, rfile, CHANGES_REQUIRED, findings=findings)
        result = self.engine.advance(run_id, result_path=str(rfile))
        self.assertEqual(result["stage"], "revise-stage")

        # Read the revision packet and check PRIOR_FINDINGS
        packet = Path(result["packet_abs_path"]).read_text(encoding="utf-8")
        self.assertIn("PRIOR_FINDINGS:", packet)
        # Both finding IDs must appear verbatim
        self.assertIn("CON-001", packet)
        self.assertIn("CON-002", packet)
        self.assertIn("Missing patristic witness for Introit", packet)
        self.assertIn("Unverified lead presented as fact", packet)


class IterationLimitTests(unittest.TestCase):
    """Test 8: revision loops stop at the configured limit."""

    @classmethod
    def setUpClass(cls):
        cls.repo, cls.runs_dir = _make_synthetic_repo()
        cls.engine = WorkflowEngine(cls.repo, cls.repo / "workflows")

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.repo, ignore_errors=True)

    def setUp(self):
        runs = self.repo / "build" / "tpt-runs"
        if runs.exists():
            shutil.rmtree(runs)

    def test_revision_stops_at_limit(self):
        """The revision loop enters BLOCKED after max_iterations."""
        result = self.engine.seed("test-wf", {"doc": "test-doc", "provider": "gpt"})
        run_id = result["run_id"]

        # Advance to eval-stage (2 linear stages)
        for _ in range(2):
            rfile = self.repo / f"r-{result['stage']}.json"
            _answer(self.engine, run_id, rfile, PASS)
            result = self.engine.advance(run_id, result_path=str(rfile))

        # eval-stage has max_iterations=2
        # Iteration 1: CHANGES_REQUIRED → revise → PASS → eval
        for i in range(2):
            self.assertEqual(result["stage"], "eval-stage")
            rfile = self.repo / f"r-eval-{i}.json"
            _answer(self.engine, run_id, rfile, CHANGES_REQUIRED, findings=[
                {"id": "CON-001", "severity": "blocking", "location": "p1",
                 "problem": "bad", "required_result": "fix"}
            ])
            result = self.engine.advance(run_id, result_path=str(rfile))
            if result.get("disposition") == BLOCKED:
                break
            self.assertEqual(result["stage"], "revise-stage")
            rfile = self.repo / f"r-rev-{i}.json"
            _answer(self.engine, run_id, rfile, PASS)
            result = self.engine.advance(run_id, result_path=str(rfile))

        self.assertEqual(result["disposition"], BLOCKED,
                         "must reach BLOCKED after max_iterations")

    def test_blocked_disposition_stops_immediately(self):
        """An evaluator returning BLOCKED stops immediately."""
        result = self.engine.seed("test-wf", {"doc": "test-doc", "provider": "gpt"})
        run_id = result["run_id"]

        for _ in range(2):
            rfile = self.repo / f"r-{result['stage']}.json"
            _answer(self.engine, run_id, rfile, PASS)
            result = self.engine.advance(run_id, result_path=str(rfile))

        self.assertEqual(result["stage"], "eval-stage")
        rfile = self.repo / "r.json"
        _answer(self.engine, run_id, rfile, "BLOCKED", findings=[
            {"id": "CON-001", "severity": "blocking", "location": "p1",
             "problem": "impossible", "required_result": "cannot fix"}
        ])
        result = self.engine.advance(run_id, result_path=str(rfile))
        self.assertEqual(result["disposition"], BLOCKED)


class ReloadTests(unittest.TestCase):
    """Test 11: run state can be reloaded and produces the same next packet."""

    @classmethod
    def setUpClass(cls):
        cls.repo, cls.runs_dir = _make_synthetic_repo()
        cls.engine = WorkflowEngine(cls.repo, cls.repo / "workflows")

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.repo, ignore_errors=True)

    def setUp(self):
        runs = self.repo / "build" / "tpt-runs"
        if runs.exists():
            shutil.rmtree(runs)

    def test_reload_produces_same_packet(self):
        """Reloading state and recompiling produces the same packet hash."""
        result = self.engine.seed("test-wf", {"doc": "test-doc", "provider": "gpt"})
        run_id = result["run_id"]
        original_hash = result["packet_hash"]

        # Reload and replay
        replay_result = self.engine.replay(run_id)
        self.assertTrue(replay_result["deterministic"],
                        "reloaded state must produce the same packet hash")
        self.assertEqual(replay_result["recompiled_hash"], original_hash)


class DownstreamGateReentryTests(unittest.TestCase):
    """Test 12: downstream gates are re-entered after revisions that can
    invalidate them."""

    @classmethod
    def setUpClass(cls):
        cls.repo, cls.runs_dir = _make_synthetic_repo()
        cls.engine = WorkflowEngine(cls.repo, cls.repo / "workflows")

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.repo, ignore_errors=True)

    def setUp(self):
        runs = self.repo / "build" / "tpt-runs"
        if runs.exists():
            shutil.rmtree(runs)

    def test_visual_revision_reenters_mechanical_gates(self):
        """After a gate revision, the workflow re-enters the gate stage."""
        # Advance to eval-stage, PASS it, enter gate-stage
        result = self.engine.seed("test-wf", {"doc": "test-doc", "provider": "gpt"})
        run_id = result["run_id"]

        for _ in range(2):
            rfile = self.repo / f"r-{result['stage']}.json"
            _answer(self.engine, run_id, rfile, PASS)
            result = self.engine.advance(run_id, result_path=str(rfile))

        # PASS the evaluator → gate-stage
        rfile = self.repo / "r-eval.json"
        _answer(self.engine, run_id, rfile, PASS, findings=[])
        result = self.engine.advance(run_id, result_path=str(rfile))
        self.assertEqual(result["stage"], "gate-stage")

        # Run the gate (it passes with 'true')
        result = self.engine.advance(run_id, run_gate=True)
        self.assertEqual(result["stage"], "final",
                         "gate PASS must advance to final")

        # Now test gate failure → revision → gate re-entry
        # Need a new run with a failing gate
        runs = self.repo / "build" / "tpt-runs"
        shutil.rmtree(runs)

        # Create a workflow with a failing gate
        wf_path = self.repo / "workflows" / "pipelines" / "test-wf.json"
        wf = json.loads(wf_path.read_text(encoding="utf-8"))
        # Change the gate command to 'false' so it fails
        for stage in wf["stages"]:
            if stage["id"] == "gate-stage":
                stage["checks"][0]["command"] = "false"
        wf_path.write_text(json.dumps(wf, sort_keys=True, indent=2), encoding="utf-8")

        result = self.engine.seed("test-wf", {"doc": "test-doc", "provider": "gpt"})
        run_id = result["run_id"]

        for _ in range(2):
            rfile = self.repo / f"r-{result['stage']}.json"
            _answer(self.engine, run_id, rfile, PASS)
            result = self.engine.advance(run_id, result_path=str(rfile))

        rfile = self.repo / "r-eval.json"
        _answer(self.engine, run_id, rfile, PASS, findings=[])
        result = self.engine.advance(run_id, result_path=str(rfile))
        self.assertEqual(result["stage"], "gate-stage")

        # Run the gate (it fails)
        result = self.engine.advance(run_id, run_gate=True)
        self.assertEqual(result["stage"], "gate-revise",
                         "gate FAIL must go to revision")

        # Complete revision → must re-enter gate
        rfile = self.repo / "r-revise.json"
        _answer(self.engine, run_id, rfile, PASS)
        result = self.engine.advance(run_id, result_path=str(rfile))
        self.assertEqual(result["stage"], "gate-stage",
                         "after gate revision, must re-enter gate-stage")


class InterventionTests(unittest.TestCase):
    """Test workflow debt / interventions."""

    @classmethod
    def setUpClass(cls):
        cls.repo, cls.runs_dir = _make_synthetic_repo()
        cls.engine = WorkflowEngine(cls.repo, cls.repo / "workflows")

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.repo, ignore_errors=True)

    def setUp(self):
        runs = self.repo / "build" / "tpt-runs"
        if runs.exists():
            shutil.rmtree(runs)

    def test_intervention_recorded_and_debt_shown(self):
        """Intervening records the text and debt shows it as unencoded."""
        result = self.engine.seed("test-wf", {"doc": "test-doc", "provider": "gpt"})
        run_id = result["run_id"]

        self.engine.intervene(run_id, "Check the Latin collation against page 412")

        debt = self.engine.debt(run_id)
        self.assertEqual(debt["unencoded_count"], 1)
        self.assertEqual(debt["interventions"][0]["text"],
                         "Check the Latin collation against page 412")
        self.assertFalse(debt["interventions"][0].get("encoded", False))


if __name__ == "__main__":
    unittest.main()
