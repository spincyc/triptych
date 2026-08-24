"""Tests for tpt workflow CLI integration, collision detection, and the
propers workflow definition.

These tests exercise the launcher through subprocess (matching the pattern
in test_tool_registry.py) and verify that existing tool dispatch remains
compatible alongside the new workflow dispatch.
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
LAUNCHER = ROOT / "tools" / "tpt"
sys.path.insert(0, str(ROOT / "scripts"))

from _workflow import WorkflowEngine, WorkflowError  # noqa: E402


def _run(*argv: str, cwd: Path | None = None) -> subprocess.CompletedProcess:
    return subprocess.run(
        [str(LAUNCHER), *argv],
        capture_output=True, text=True, cwd=cwd or ROOT,
    )


def _run_json(*argv: str) -> tuple[int, dict | None, str]:
    """Run tpt and parse JSON output. Returns (exit_code, parsed_json, stderr)."""
    result = _run(*argv)
    if result.stdout.strip():
        try:
            return result.returncode, json.loads(result.stdout), result.stderr
        except json.JSONDecodeError:
            return result.returncode, None, result.stderr
    return result.returncode, None, result.stderr


class CompatibilityTests(unittest.TestCase):
    """Test 9: existing tpt tool dispatch remains compatible."""

    def test_list_still_works(self):
        result = _run("--list")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("launcher:", result.stdout)

    def test_list_json_still_works(self):
        result = _run("--list", "--json")
        self.assertEqual(result.returncode, 0, result.stderr)
        rows = json.loads(result.stdout)
        self.assertGreater(len(rows), 10, "tool list should have many tools")

    def test_check_still_works(self):
        result = _run("--check")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("registry ok", result.stdout)

    def test_info_still_works(self):
        result = _run("--info", "tpt", "--json")
        self.assertEqual(result.returncode, 0, result.stderr)
        entry = json.loads(result.stdout)
        self.assertEqual(entry["name"], "tpt")

    def test_path_still_works(self):
        result = _run("--path", "tpt")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertTrue(result.stdout.strip().endswith("tools/tpt"))

    def test_tool_dispatch_still_works(self):
        """A registered tool can still be dispatched through tpt."""
        result = _run("citations", "parse", "Psalm 24:1-3", "--json")
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_unknown_tool_still_fails(self):
        """An unknown name still fails with exit 2 and no traceback."""
        result = _run("no-such-tool-anywhere")
        self.assertEqual(result.returncode, 2)
        self.assertNotIn("Traceback", result.stderr)

    def test_examples_section_still_present(self):
        """The --help output still has the examples heading."""
        result = _run("--help")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("examples (real invocations", result.stdout)


class CollisionDetectionTests(unittest.TestCase):
    """Test 10: workflow/tool identifier collisions are rejected."""

    def test_no_collision_between_workflows_and_tools(self):
        """The 'proper' workflow id must not collide with any tool id."""
        registry = json.loads((ROOT / "tmt.json").read_text(encoding="utf-8"))
        tool_ids = set(registry["tools"])
        engine = WorkflowEngine(ROOT, ROOT / "workflows")
        workflow_ids = {w["id"] for w in engine.list_workflows()}
        collisions = tool_ids & workflow_ids
        self.assertEqual(collisions, set(),
                         f"collision between tool and workflow ids: {collisions}")

    def test_collision_detected_at_engine_level(self):
        """The engine's check_collisions raises on a collision."""
        engine = WorkflowEngine(ROOT, ROOT / "workflows")
        # "proper" is a registered workflow id; simulate it also being a tool
        with self.assertRaises(WorkflowError):
            engine.check_collisions({"proper"})


class WorkflowMetaTests(unittest.TestCase):
    """Tests for `tpt workflow list` and `tpt workflow show`."""

    def test_workflow_list(self):
        result = _run("workflow", "list")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("proper", result.stdout)

    def test_workflow_show(self):
        result = _run("workflow", "show", "proper")
        self.assertEqual(result.returncode, 0, result.stderr)
        data = json.loads(result.stdout)
        self.assertEqual(data["id"], "proper")
        on_disk = json.loads(
            (ROOT / "workflows" / "pipelines" / "proper.json").read_text(
                encoding="utf-8")
        )
        self.assertEqual(data["version"], on_disk["version"])
        self.assertGreaterEqual(data["version"], 1)

    def test_workflow_show_unknown(self):
        result = _run("workflow", "show", "no-such-workflow")
        self.assertEqual(result.returncode, 2)

    def test_workflow_no_subcommand(self):
        result = _run("workflow")
        self.assertEqual(result.returncode, 2)


class PropersWorkflowTests(unittest.TestCase):
    """Tests that the propers workflow can compile and advance through
    representative states without requiring a live AI provider."""

    def setUp(self):
        # A private runs directory per test. These tests must never touch
        # build/tpt-runs: that is an operator's live run state.
        self.runs = Path(tempfile.mkdtemp(prefix="tpt-runs-test-"))
        self.engine = WorkflowEngine(ROOT, ROOT / "workflows", runs_dir=self.runs)

    def tearDown(self):
        shutil.rmtree(self.runs, ignore_errors=True)

    def test_propers_workflow_loads(self):
        """The propers workflow definition loads and validates."""
        wf = self.engine.load_workflow("proper")
        self.assertEqual(wf["id"], "proper")
        self.assertGreater(len(wf["stages"]), 8,
                           "propers workflow should have many stages")

    def test_propers_workflow_has_required_stage_types(self):
        """The workflow includes linear, evaluator, bounded-revision, and gate."""
        wf = self.engine.load_workflow("proper")
        types = {s["type"] for s in wf["stages"]}
        self.assertIn("linear", types)
        self.assertIn("evaluator", types)
        self.assertIn("bounded-revision", types)
        self.assertIn("gate", types)

    def test_propers_workflow_has_terminal_stages(self):
        """The workflow has ACCEPTED as a terminal target."""
        wf = self.engine.load_workflow("proper")
        targets = set()
        for stage in wf["stages"]:
            for key in ("next", "pass_transition"):
                if key in stage:
                    targets.add(stage[key])
        self.assertIn("ACCEPTED", targets)

    def test_propers_workflow_has_visual_after_mechanical(self):
        """Visual evaluation comes after mechanical gates."""
        wf = self.engine.load_workflow("proper")
        gate_pass = None
        visual_id = None
        for stage in wf["stages"]:
            if stage["id"] == "mechanical-gates":
                gate_pass = stage.get("pass_transition")
            if stage["id"] == "visual-evaluation":
                visual_id = stage["id"]
        self.assertEqual(gate_pass, "visual-evaluation",
                         "mechanical gates must pass to visual evaluation")

    def test_propers_workflow_visual_revision_reenters_gates(self):
        """Visual revision must re-enter mechanical gates (downstream re-entry)."""
        wf = self.engine.load_workflow("proper")
        for stage in wf["stages"]:
            if stage["id"] == "visual-revision":
                self.assertEqual(stage["next"], "mechanical-gates",
                                 "visual revision must re-enter mechanical gates")

    def test_propers_seed_creates_run(self):
        """Seed creates a run with a deterministic first packet."""
        result = self.engine.seed("proper", {
            "proper": "liturgy/roman-rite/1962/propers/temporal/46-ninth-after-pentecost",
            "provider": "gpt",
        })
        self.assertFalse(result.get("already_exists", False))
        self.assertEqual(result["stage"], "seed")
        self.assertEqual(len(result["packet_hash"]), 64,
                         "packet hash must be a SHA-256 hex digest")

    def test_propers_seed_deterministic(self):
        """Two seeds with identical args produce identical packet hashes."""
        args = {
            "proper": "liturgy/roman-rite/1962/propers/temporal/46-ninth-after-pentecost",
            "provider": "gpt",
        }
        r1 = self.engine.seed("proper", args)
        h1 = r1["packet_hash"]
        shutil.rmtree(self.runs / r1["run_id"])

        r2 = self.engine.seed("proper", args)
        h2 = r2["packet_hash"]
        self.assertEqual(h1, h2,
                         "identical seed args must produce identical packet hashes")

    def test_propers_advance_through_linear_stages(self):
        """The workflow can advance through linear stages with PASS results."""
        result = self.engine.seed("proper", {
            "proper": "liturgy/roman-rite/1962/propers/temporal/46-ninth-after-pentecost",
            "provider": "gpt",
        })
        run_id = result["run_id"]

        # Advance through seed → resolve-context → source-audit → research-synthesis → author-proper
        expected_stages = [
            "seed", "resolve-context", "source-audit",
            "research-synthesis", "author-proper",
        ]
        for i, expected in enumerate(expected_stages):
            self.assertEqual(result["stage"], expected,
                             f"stage {i} should be {expected}, got {result['stage']}")
            if i < len(expected_stages) - 1:
                rfile = self.runs / run_id / f"result-{i}.json"
                rfile.parent.mkdir(parents=True, exist_ok=True)
                state = self.engine.load_state(run_id)
                rfile.write_text(json.dumps({
                    "disposition": "PASS", "summary": "test",
                    "packet_hash": state["packet_hashes"][-1]["hash"],
                }), encoding="utf-8")
                result = self.engine.advance(run_id, result_path=str(rfile))

    def test_propers_all_fragments_exist(self):
        """Every fragment referenced by the workflow exists on disk."""
        wf = self.engine.load_workflow("proper")
        for stage in wf["stages"]:
            for frag in stage.get("fragments", []):
                path = self.engine.fragments_dir / frag
                self.assertTrue(path.is_file(),
                                 f"missing fragment for {stage['id']}: {frag}")

    def test_propers_all_schemas_exist(self):
        """Every schema referenced by the workflow exists on disk."""
        wf = self.engine.load_workflow("proper")
        for stage in wf["stages"]:
            schema_name = stage.get("result_schema", "worker-result.json")
            path = self.engine.schemas_dir / schema_name
            self.assertTrue(path.is_file(),
                             f"missing schema for {stage['id']}: {schema_name}")

    def test_propers_gate_commands_have_substitutable_args(self):
        """Gate commands reference {provider} and {proper} placeholders."""
        wf = self.engine.load_workflow("proper")
        for stage in wf["stages"]:
            if stage["type"] == "gate":
                for check in stage.get("checks", []):
                    cmd = check["command"]
                    self.assertIn("{provider}", cmd,
                                  f"gate {stage['id']} check {check['id']} must use {{provider}}")
                    self.assertIn("{proper}", cmd,
                                  f"gate {stage['id']} check {check['id']} must use {{proper}}")


class GateExecutionTests(unittest.TestCase):
    """Tests for gate stage execution."""

    def setUp(self):
        # A private runs directory per test. These tests must never touch
        # build/tpt-runs: that is an operator's live run state.
        self.runs = Path(tempfile.mkdtemp(prefix="tpt-runs-test-"))
        self.engine = WorkflowEngine(ROOT, ROOT / "workflows", runs_dir=self.runs)

    def tearDown(self):
        shutil.rmtree(self.runs, ignore_errors=True)

    def test_gate_run_directly(self):
        """A gate stage can be run directly via advance(run_gate=True)."""
        # Use the synthetic test repo for this test
        import tempfile, subprocess as sp
        repo = Path(tempfile.mkdtemp(prefix="tpt-gate-test-"))
        try:
            # Create a minimal workflow with a gate
            wf_dir = repo / "workflows"
            (wf_dir / "fragments" / "synthetic").mkdir(parents=True, exist_ok=True)
            (wf_dir / "pipelines").mkdir(parents=True, exist_ok=True)
            (wf_dir / "schema").mkdir(parents=True, exist_ok=True)

            (wf_dir / "fragments" / "synthetic" / "brief.md").write_text("brief", encoding="utf-8")

            for name, content in [("worker-result.json", {
                "required_fields": ["disposition", "summary"],
                "valid_dispositions": ["PASS"], "finding_fields": [],
            }), ("gate-result.json", {
                "required_fields": ["disposition", "findings"],
                "valid_dispositions": ["PASS", "FAIL"], "finding_fields": [
                    "id", "severity", "check", "problem", "required_result"],
            })]:
                (wf_dir / "schema" / name).write_text(
                    json.dumps(content), encoding="utf-8")

            wf = {
                "id": "gate-test", "version": 1, "description": "gate test",
                "argument_schema": {"doc": {"required": True, "type": "string"}},
                "stages": [
                    {"id": "gate", "type": "gate",
                     "checks": [{"id": "ok", "command": "true",
                                 "required_result": "must pass"}],
                     "pass_transition": "ACCEPTED",
                     "fail_transition": "BLOCKED", "max_iterations": 1},
                ],
            }
            (wf_dir / "pipelines" / "gate-test.json").write_text(
                json.dumps(wf), encoding="utf-8")

            sp.run(["git", "init"], cwd=repo, capture_output=True)
            sp.run(["git", "add", "."], cwd=repo, capture_output=True)
            sp.run(["git", "commit", "-m", "x"], cwd=repo, capture_output=True,
                   env={**os.environ, "GIT_AUTHOR_NAME": "t",
                        "GIT_AUTHOR_EMAIL": "t@t", "GIT_COMMITTER_NAME": "t",
                        "GIT_COMMITTER_EMAIL": "t@t"})

            engine = WorkflowEngine(repo, repo / "workflows")
            result = engine.seed("gate-test", {"doc": "test"})
            run_id = result["run_id"]

            # Run the gate
            result = engine.advance(run_id, run_gate=True)
            self.assertEqual(result["disposition"], "ACCEPTED")
        finally:
            shutil.rmtree(repo, ignore_errors=True)


if __name__ == "__main__":
    unittest.main()
