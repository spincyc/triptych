"""Tests for tpt workflow CLI integration, collision detection, and the
propers workflow definition.

These tests exercise the launcher through subprocess (matching the pattern
in test_tool_registry.py) and verify that existing tool dispatch remains
compatible alongside the new workflow dispatch.
"""

from __future__ import annotations

import json
import os
import shlex
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
LAUNCHER = ROOT / "tools" / "tpt"
sys.path.insert(0, str(ROOT / "scripts"))

from _workflow import (  # noqa: E402
    RUN_IDENTITY_PREFIX,
    WorkflowEngine,
    WorkflowError,
    _gate_substitutions,
    _substitute_args,
)


def _run(*argv: str, cwd: Path | None = None) -> subprocess.CompletedProcess:
    return subprocess.run(
        [str(LAUNCHER), *argv],
        capture_output=True, text=True, cwd=cwd or ROOT,
    )


def _private_runs_dir(case: unittest.TestCase) -> Path:
    """A per-test run directory under the ignored build tree."""
    name = case.id().rsplit(".", 1)[-1]
    runs = ROOT / "build" / f"tpt-runs-test-{os.getpid()}-{name}"
    shutil.rmtree(runs, ignore_errors=True)
    runs.mkdir(parents=True, exist_ok=True)
    return runs


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
        # The launcher must report the definition on disk, whatever version
        # that is; the bump itself is asserted where a bump is the subject.
        on_disk = json.loads(
            (ROOT / "workflows" / "pipelines" / "proper.json")
            .read_text(encoding="utf-8"))
        self.assertEqual(data["version"], on_disk["version"])

    def test_workflow_show_unknown(self):
        result = _run("workflow", "show", "no-such-workflow")
        self.assertEqual(result.returncode, 2)

    def test_workflow_no_subcommand(self):
        result = _run("workflow")
        self.assertEqual(result.returncode, 2)


class PropersWorkflowTests(unittest.TestCase):
    """Tests that the propers workflow can compile and advance through
    representative states without requiring a live AI provider."""

    @classmethod
    def setUpClass(cls):
        cls.engine = WorkflowEngine(ROOT, ROOT / "workflows")

    def setUp(self):
        # Never touch build/tpt-runs: an operator's live run lives there, and a
        # test run of the suite would delete it.
        self.runs = _private_runs_dir(self)
        self.engine.runs_dir = self.runs

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
            "proper": "liturgy/roman-rite/1962/propers/temporal/49-ninth-after-pentecost",
            "provider": "gpt",
        })
        self.assertFalse(result.get("already_exists", False))
        self.assertEqual(result["stage"], "seed")
        self.assertEqual(len(result["packet_hash"]), 64,
                         "packet hash must be a SHA-256 hex digest")

    def test_propers_seed_deterministic(self):
        """Two seeds with identical args produce identical packet hashes."""
        args = {
            "proper": "liturgy/roman-rite/1962/propers/temporal/49-ninth-after-pentecost",
            "provider": "gpt",
        }
        r1 = self.engine.seed("proper", args)
        h1 = r1["packet_hash"]
        shutil.rmtree(self.runs / r1["run_id"])

        r2 = self.engine.seed("proper", args)
        h2 = r2["packet_hash"]
        self.assertEqual(h1, h2,
                         "identical seed args must produce identical packet hashes")

    def test_propers_advance_through_single_stages(self):
        """The workflow advances through its single stages with PASS results.

        The walk covers the head of the v9 lifecycle: the seed, the
        authorization stage, the scope gate that must run as a gate, and the
        two context stages. It stops at `research`, which is a fan-out stage
        answered with one result per declared lane rather than one for the
        stage; that path is held by test_workflow_research_fanout.py.

        `scope-gate` is answered directly rather than run, because its
        checks read a maintainer's authorization out of
        `guidance/liturgy/propers-production-plan.md` and no test may write
        one there. The gate's own commands are held to their real behaviour
        in test_workflow_scope_and_publication.py.
        """
        result = self.engine.seed("proper", {
            "proper": "liturgy/roman-rite/1962/propers/temporal/49-ninth-after-pentecost",
            "provider": "gpt",
        })
        run_id = result["run_id"]

        real_run_gate = self.engine._run_gate

        def run_gate(workflow, stage, state, run_id):
            if stage["id"] != "scope-gate":
                return real_run_gate(workflow, stage, state, run_id)
            return {"disposition": "PASS", "findings": [],
                    "stage": stage["id"], "iteration": 0}

        self.engine._run_gate = run_gate

        expected_stages = [
            "seed", "authorize-target", "scope-gate", "resolve-context",
            "source-audit", "research",
        ]
        for i, expected in enumerate(expected_stages):
            self.assertEqual(result["stage"], expected,
                             f"stage {i} should be {expected}, got {result['stage']}")
            if i == len(expected_stages) - 1:
                break
            if expected == "scope-gate":
                result = self.engine.advance(run_id, run_gate=True)
                continue
            rfile = self.runs / run_id / f"result-{i}.json"
            rfile.parent.mkdir(parents=True, exist_ok=True)
            rfile.write_text(json.dumps({
                "stage": expected, "iteration": 0,
                "disposition": "PASS", "summary": "test"
            }), encoding="utf-8")
            result = self.engine.advance(run_id, result_path=str(rfile))

        with self.assertRaises(WorkflowError) as caught:
            self.engine.advance(run_id, result_path=str(rfile))
        self.assertIn("pass one --lane-result", str(caught.exception),
                      "a fan-out stage is not answered by one stage result")

    def test_propers_all_lane_fragments_exist(self):
        """Every lane fragment the workflow declares exists on disk."""
        wf = self.engine.load_workflow("proper")
        declared = 0
        for stage in wf["stages"]:
            for lane in stage.get("execution", {}).get("lanes", []):
                for frag in lane.get("fragments", []):
                    declared += 1
                    self.assertTrue(
                        (self.engine.fragments_dir / frag).is_file(),
                        f"missing lane fragment for {stage['id']}/"
                        f"{lane['id']}: {frag}")
        self.assertEqual(declared, 16,
                         "seven research, five content, four visual lanes")

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
        """A gate command is parameterized by the run, and by nothing else.

        Every check names at least one of the run's two normalized arguments,
        so no check is a constant that would pass or fail alike for every
        target; and no check names a placeholder the run has not normalized,
        so nothing is left for a host to fill in. A single check may name
        just one of the two — the identity check asks about the proper and
        the provider check asks about the provider — but each gate as a whole
        is bound to both.
        """
        wf = self.engine.load_workflow("proper")
        known = ("{proper}", "{provider}")
        gates = [stage for stage in wf["stages"] if stage["type"] == "gate"]
        self.assertTrue(gates)
        for stage in gates:
            named = set()
            for check in stage.get("checks", []):
                cmd = check["command"]
                with self.subTest(gate=stage["id"], check=check["id"]):
                    used = [token for token in known if token in cmd]
                    self.assertTrue(
                        used,
                        f"gate {stage['id']} check {check['id']} names "
                        f"neither {{proper}} nor {{provider}}")
                    named.update(used)
                    residue = cmd
                    for token in known:
                        residue = residue.replace(token, "")
                    # A placeholder is `{name}`. A gate command may legitimately
                    # contain other braces -- an awk program body is all braces --
                    # so look for the placeholder shape, not for the character.
                    self.assertNotRegex(
                        residue, r"\{[A-Za-z_][A-Za-z0-9_]*\}",
                        f"gate {stage['id']} check {check['id']} takes an "
                        f"argument the run has not normalized")
            self.assertEqual(
                named, set(known),
                f"gate {stage['id']} must be bound to both the proper and "
                f"the provider across its checks")


class GateExecutionTests(unittest.TestCase):
    """Tests for gate stage execution."""

    @classmethod
    def setUpClass(cls):
        cls.engine = WorkflowEngine(ROOT, ROOT / "workflows")

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
                     "execution": {"mode": "program"},
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


class RunIdentitySubstitutionTests(unittest.TestCase):
    """What a gate command may name, and what it may never be made to mean.

    A gate check is a shell command over the run's normalized arguments. That
    let a check compare a document against its own arguments and never against
    the run producing it, which is the one comparison a document's provenance
    record needs: the record states which run wrote it, and only the run can
    say whether that is this one. So the substitution namespace carries the
    run's own identity as well, under a reserved `run.` prefix.

    The prefix is the whole of the safety. Argument names are plain
    identifiers, so `{run.run_id}` is not a name any workflow can declare, and
    a workflow that declares `run_id` gets `{run_id}` for its value while the
    engine keeps `{run.run_id}`. These tests run a real gate in a real
    repository and read what the shell was actually given.
    """

    ARGS = {"doc": "a-document", "run_id": "an argument, not the run"}

    def setUp(self):
        self.repo = Path(tempfile.mkdtemp(prefix="tpt-run-identity-"))
        self.addCleanup(shutil.rmtree, self.repo, ignore_errors=True)
        workflows = self.repo / "workflows"
        (workflows / "fragments" / "synthetic").mkdir(parents=True)
        (workflows / "pipelines").mkdir(parents=True)
        (workflows / "schema").mkdir(parents=True)
        (workflows / "fragments" / "synthetic" / "brief.md").write_text(
            "brief", encoding="utf-8")
        for name, content in (
            ("worker-result.json", {
                "required_fields": ["disposition", "summary"],
                "valid_dispositions": ["PASS"], "finding_fields": []}),
            ("gate-result.json", {
                "required_fields": ["disposition", "findings"],
                "valid_dispositions": ["PASS", "FAIL"],
                "finding_fields": ["id", "severity", "check", "problem",
                                   "required_result"]}),
        ):
            (workflows / "schema" / name).write_text(
                json.dumps(content), encoding="utf-8")
        self.write_workflow()
        subprocess.run(["git", "init"], cwd=self.repo, capture_output=True)
        subprocess.run(["git", "add", "."], cwd=self.repo,
                       capture_output=True)
        subprocess.run(
            ["git", "commit", "-m", "x"], cwd=self.repo, capture_output=True,
            env={**os.environ, "GIT_AUTHOR_NAME": "t",
                 "GIT_AUTHOR_EMAIL": "t@t", "GIT_COMMITTER_NAME": "t",
                 "GIT_COMMITTER_EMAIL": "t@t"})
        self.engine = WorkflowEngine(self.repo, workflows)

    # The command writes one line per name, so the test reads exactly what
    # the shell was handed rather than what the template said.
    COMMAND = (
        "printf '%s\\n' {run.workflow_id} {run.workflow_version} "
        "{run.workflow_digest} {run.run_id} {run.repo_commit} {doc} "
        "{run_id} > substituted.txt"
    )

    def write_workflow(self, command=None, arguments=None):
        workflow = {
            "id": "identity-test", "version": 3,
            "description": "run identity in a gate command",
            "argument_schema": arguments if arguments is not None else {
                "doc": {"type": "string", "required": True},
                "run_id": {"type": "string", "required": True},
            },
            "stages": [{
                "id": "gate", "type": "gate",
                "execution": {"mode": "program"},
                "checks": [{"id": "substitute",
                            "command": command or self.COMMAND,
                            "required_result": "must pass"}],
                "pass_transition": "ACCEPTED",
                "fail_transition": "BLOCKED", "max_iterations": 1,
            }],
        }
        (self.repo / "workflows" / "pipelines"
         / "identity-test.json").write_text(
            json.dumps(workflow), encoding="utf-8")

    def run_the_gate(self, args=None):
        seeded = self.engine.seed("identity-test", args or dict(self.ARGS))
        out = self.engine.advance(seeded["run_id"], run_gate=True)
        written = (self.repo / "substituted.txt").read_text(encoding="utf-8")
        return seeded, out, written.splitlines()

    def test_a_gate_command_is_given_the_runs_own_identity(self):
        seeded, out, lines = self.run_the_gate()
        self.assertEqual(out["disposition"], "ACCEPTED")
        state = self.engine.load_state(seeded["run_id"])
        self.assertEqual(lines[:5], [
            "identity-test",
            str(state["workflow_version"]),
            state["workflow_digest"],
            seeded["run_id"],
            state["repo_commit"],
        ], "the five run facts the packet header states")

    def test_an_argument_called_run_id_is_not_the_runs_run_id(self):
        """The collision the dotted namespace exists to make impossible."""
        seeded, _, lines = self.run_the_gate()
        self.assertEqual(lines[5], self.ARGS["doc"])
        self.assertEqual(lines[6], self.ARGS["run_id"],
                         "the workflow's own argument keeps its value")
        self.assertEqual(lines[3], seeded["run_id"])
        self.assertNotEqual(lines[6], lines[3],
                            "an argument named after a run fact must not "
                            "become it, or shadow it")

    def test_a_hostile_argument_cannot_escape_a_run_naming_command(self):
        """The `fab7db40b` property, over the enlarged namespace.

        Every substituted value is shell-quoted, run facts included, so a
        hostile document id is one word of data however many names the
        template carries beside it.
        """
        payload = "x`touch escaped` $(touch escaped) ; touch escaped"
        _, out, lines = self.run_the_gate(
            {"doc": payload, "run_id": payload})
        self.assertEqual(out["disposition"], "ACCEPTED")
        self.assertEqual(lines[5], payload,
                         "the id did not survive as inert data")
        self.assertEqual(lines[6], payload)
        self.assertFalse((self.repo / "escaped").exists(),
                         "a substituted value ran as shell")

    def test_a_run_fact_is_quoted_like_any_other_value(self):
        """Not because these values are hostile: because quoting is the rule.

        Every one of them is engine-generated, and none of that is relied on.
        The property is asserted where it can be asserted -- over the
        substitution itself, with a hostile value put where a run fact goes.
        """
        payload = "x`touch /tmp/triptych-run-identity-escape`"
        rendered = _substitute_args(
            "check --run-id {run.run_id}",
            {"run.run_id": payload}, quote=True)
        self.assertEqual(shlex.split(rendered),
                         ["check", "--run-id", payload])

    def test_an_argument_in_the_reserved_namespace_is_refused_at_load(self):
        self.write_workflow(arguments={
            "doc": {"type": "string", "required": True},
            f"{RUN_IDENTITY_PREFIX}run_id": {"type": "string"},
        })
        with self.assertRaises(WorkflowError) as caught:
            self.engine.load_workflow("identity-test")
        self.assertIn("reserved", str(caught.exception))
        self.assertIn(RUN_IDENTITY_PREFIX, str(caught.exception))

    def test_a_reserved_argument_is_refused_again_at_the_point_of_use(self):
        """A definition is not the only way an argument reaches a run.

        Loading refuses a declared one; this refuses one that arrived any
        other way, at the moment it would decide what a run fact expands to.
        """
        workflow = {"id": "identity-test", "version": 3}
        state = {
            "run_id": "0123456789abcdef", "workflow_digest": "d" * 64,
            "repo_commit": "c" * 40,
            "normalized_args": {f"{RUN_IDENTITY_PREFIX}run_id": "mine"},
        }
        with self.assertRaises(WorkflowError) as caught:
            _gate_substitutions(workflow, state)
        self.assertIn("reserved", str(caught.exception))

    def test_a_name_nothing_supplies_is_left_exactly_as_written(self):
        self.assertEqual(
            _substitute_args("{doc} {run.nothing} {unknown}",
                             {"doc": "a", "run.run_id": "b"}),
            "a {run.nothing} {unknown}")


if __name__ == "__main__":
    unittest.main()
