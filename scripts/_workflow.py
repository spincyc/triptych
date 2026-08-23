#!/usr/bin/env python3
"""Deterministic AI-guidance workflow engine for tpt.

This module implements the core workflow engine that compiles deterministic
guidance packets, validates structured results, and drives stage transitions.
It is imported by tools/tpt and never instantiated directly by an operator.

The invariant:

    Given the same repository commit, workflow version, document type,
    arguments, workflow state, and prior structured results, tpt must emit
    the same next AI guidance packet byte-for-byte.

No AI agent decides what instructions its successor receives. The engine owns
fragment selection, ordering, packet composition, transitions, iteration
bounds, and stop conditions.
"""
from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
import time
from pathlib import Path
from typing import Any

# Stage types
LINEAR = "linear"
EVALUATOR = "evaluator"
BOUNDED_REVISION = "bounded-revision"
GATE = "gate"

# Terminal states
ACCEPTED = "ACCEPTED"
BLOCKED = "BLOCKED"

# Dispositions
PASS = "PASS"
CHANGES_REQUIRED = "CHANGES_REQUIRED"
FAIL = "FAIL"

# Schema names
SCHEMA_WORKER = "worker-result.json"
SCHEMA_EVALUATOR = "evaluator-result.json"
SCHEMA_GATE = "gate-result.json"

PROTOCOL_VERSION = 1

# Separator for packet assembly. Fixed bytes, never varies.
_PACKET_SEP = "\n--- FRAGMENT: "
_HEADER_SEP = "\n\n"
_FIELD_SEP = "\n"


class WorkflowError(RuntimeError):
    """A workflow engine error worth reporting as one line."""


# ---------------------------------------------------------------------------
# Loading
# ---------------------------------------------------------------------------

class WorkflowEngine:
    """The deterministic workflow engine.

    All methods are pure with respect to their inputs: given the same
    workflow definition, state, and arguments, they produce the same output.
    The only nondeterministic value is the run_id, which is derived from
    inputs and therefore also deterministic for the same inputs.
    """

    def __init__(self, repo_root: Path, workflows_dir: Path) -> None:
        self.repo_root = repo_root.resolve()
        self.workflows_dir = workflows_dir.resolve()
        self.pipelines_dir = self.workflows_dir / "pipelines"
        self.fragments_dir = self.workflows_dir / "fragments"
        self.schemas_dir = self.workflows_dir / "schema"
        self.runs_dir = self.repo_root / "build" / "tpt-runs"

    # --- Workflow definitions ---

    def list_workflows(self) -> list[dict[str, Any]]:
        """List all available workflow definitions, sorted by id."""
        workflows = []
        if not self.pipelines_dir.is_dir():
            return workflows
        for path in sorted(self.pipelines_dir.glob("*.json")):
            try:
                data = json.loads(path.read_text(encoding="utf-8"))
                workflows.append({
                    "id": data["id"],
                    "version": data["version"],
                    "description": data.get("description", ""),
                })
            except (json.JSONDecodeError, KeyError, OSError):
                continue
        return workflows

    def load_workflow(self, workflow_id: str) -> dict[str, Any]:
        """Load a workflow definition by id."""
        path = self.pipelines_dir / f"{workflow_id}.json"
        if not path.is_file():
            available = ", ".join(
                p.stem for p in sorted(self.pipelines_dir.glob("*.json"))
            )
            raise WorkflowError(
                f"unknown workflow: {workflow_id}\navailable: {available}"
            )
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as error:
            raise WorkflowError(f"{path}: invalid JSON: {error}") from error
        _validate_workflow(data, path)
        return data

    def load_schema(self, schema_name: str) -> dict[str, Any]:
        """Load a schema definition by filename."""
        path = self.schemas_dir / schema_name
        if not path.is_file():
            raise WorkflowError(f"unknown schema: {schema_name}")
        return json.loads(path.read_text(encoding="utf-8"))

    def load_fragment(self, fragment_path: str) -> str:
        """Load a fragment file from the fragments directory."""
        path = self.fragments_dir / fragment_path
        if not path.is_file():
            raise WorkflowError(f"missing fragment: {fragment_path}")
        return path.read_text(encoding="utf-8")

    # --- Collision detection ---

    def check_collisions(self, tool_ids: set[str]) -> None:
        """Reject any workflow id that collides with a registered tool id."""
        workflow_ids = {w["id"] for w in self.list_workflows()}
        collisions = workflow_ids & tool_ids
        if collisions:
            raise WorkflowError(
                f"workflow id collides with registered tool id: "
                f"{', '.join(sorted(collisions))}"
            )

    # --- Normalization ---

    def normalize_args(self, raw_args: dict[str, str]) -> dict[str, str]:
        """Normalize arguments to a deterministic, sorted, string-valued map."""
        normalized = {}
        for key in sorted(raw_args):
            value = raw_args[key]
            if value is not None:
                normalized[str(key)] = str(value)
        return normalized

    def get_repo_commit(self) -> str:
        """Get the current repository commit SHA."""
        try:
            result = subprocess.run(
                ["git", "rev-parse", "HEAD"],
                capture_output=True, text=True, cwd=self.repo_root,
            )
            if result.returncode != 0:
                raise WorkflowError(f"git rev-parse failed: {result.stderr.strip()}")
            return result.stdout.strip()
        except FileNotFoundError as error:
            raise WorkflowError("git not found") from error

    # --- Run management ---

    def compute_run_id(self, workflow_id: str, workflow_version: int,
                       commit: str, normalized_args: dict[str, str]) -> str:
        """Compute a deterministic run id from inputs."""
        material = json.dumps({
            "workflow_id": workflow_id,
            "workflow_version": workflow_version,
            "commit": commit,
            "args": normalized_args,
        }, sort_keys=True, separators=(",", ":"))
        return hashlib.sha256(material.encode("utf-8")).hexdigest()[:16]

    def run_dir(self, run_id: str) -> Path:
        return self.runs_dir / run_id

    def seed(self, workflow_id: str, raw_args: dict[str, str]) -> dict[str, Any]:
        """Create a new run and emit the first packet.

        Returns a dict with run_id, stage, packet_hash, packet_path, and
        instructions for the parent agent.
        """
        workflow = self.load_workflow(workflow_id)
        commit = self.get_repo_commit()
        args = self.normalize_args(raw_args)

        # Validate required arguments
        arg_schema = workflow.get("argument_schema", {})
        for arg_name, arg_spec in arg_schema.items():
            if arg_spec.get("required") and arg_name not in args:
                default = arg_spec.get("default")
                if default is not None:
                    args[arg_name] = str(default)
                else:
                    raise WorkflowError(
                        f"missing required argument: {arg_name}"
                    )
        # Fill defaults
        for arg_name, arg_spec in arg_schema.items():
            if arg_name not in args and "default" in arg_spec:
                args[arg_name] = str(arg_spec["default"])

        run_id = self.compute_run_id(
            workflow["id"], workflow["version"], commit, args
        )
        run_dir = self.run_dir(run_id)

        # Don't clobber an existing run
        if run_dir.exists() and (run_dir / "state.json").exists():
            state = self.load_state(run_id)
            return {
                "run_id": run_id,
                "already_exists": True,
                "state": state,
            }

        # Create run directory structure
        for subdir in ("packets", "results", "artifacts", "interventions"):
            (run_dir / subdir).mkdir(parents=True, exist_ok=True)

        # Write manifest (immutable)
        manifest = {
            "run_id": run_id,
            "workflow_id": workflow["id"],
            "workflow_version": workflow["version"],
            "repo_commit": commit,
            "normalized_args": args,
            "created_at": _utc_timestamp(),
        }
        (run_dir / "manifest.json").write_text(
            json.dumps(manifest, sort_keys=True, indent=2) + "\n",
            encoding="utf-8",
        )

        # Initialize state
        first_stage = workflow["stages"][0]["id"]
        state = {
            "run_id": run_id,
            "workflow_id": workflow["id"],
            "workflow_version": workflow["version"],
            "repo_commit": commit,
            "normalized_args": args,
            "current_stage": first_stage,
            "iteration": 0,
            "stage_iterations": {},
            "packet_hashes": [],
            "result_hashes": [],
            "transitions": [],
            "disposition": None,
        }
        self.save_state(run_id, state)

        # Emit first event
        self._emit_event(run_id, {
            "event": "seed",
            "workflow_id": workflow["id"],
            "workflow_version": workflow["version"],
            "stage": first_stage,
            "timestamp": _utc_timestamp(),
        })

        # Compile and emit the first packet
        stage = self._get_stage(workflow, first_stage)
        prior_findings = []
        packet = self._compile_packet(
            workflow, stage, state, run_dir, prior_findings
        )
        self._record_packet(run_id, state, packet)

        return {
            "run_id": run_id,
            "already_exists": False,
            "stage": first_stage,
            "iteration": 0,
            "packet_hash": packet["hash"],
            "packet_path": str(packet["path"].relative_to(self.repo_root)),
            "packet_abs_path": str(packet["path"]),
            "instructions": _driver_instructions(packet["path"]),
        }

    def advance(self, run_id: str, result_path: str | None = None,
                run_gate: bool = False) -> dict[str, Any]:
        """Validate a result and emit the next packet (or terminal state).

        For linear/evaluator/bounded-revision stages: requires --result <path>.
        For gate stages: requires --run-gate (runs the gate checks directly).
        """
        state = self.load_state(run_id)
        if state["disposition"] is not None:
            raise WorkflowError(
                f"run {run_id} has reached terminal state: "
                f"{state['disposition']}"
            )
        workflow = self.load_workflow(state["workflow_id"])
        stage = self._get_stage(workflow, state["current_stage"])

        if stage["type"] == GATE:
            if not run_gate:
                raise WorkflowError(
                    f"stage {stage['id']} is a gate; use --run-gate"
                )
            if result_path is not None:
                raise WorkflowError(
                    f"stage {stage['id']} is a gate; do not pass --result"
                )
            result = self._run_gate(workflow, stage, state, run_id)
        else:
            if run_gate:
                raise WorkflowError(
                    f"stage {stage['id']} is not a gate; pass --result <path>"
                )
            if result_path is None:
                raise WorkflowError(
                    f"stage {stage['id']} requires --result <path>"
                )
            result = self._load_and_validate_result(
                result_path, stage, run_id, state
            )

        # Record the result
        self._record_result(run_id, state, result, stage)

        # Determine transition
        transition = self._determine_transition(
            workflow, stage, result, state
        )

        # Apply transition
        self._emit_event(run_id, {
            "event": "result",
            "stage": stage["id"],
            "disposition": result["disposition"],
            "transition": transition,
            "timestamp": _utc_timestamp(),
        })

        if transition == ACCEPTED:
            state["disposition"] = ACCEPTED
            state["current_stage"] = ACCEPTED
            self.save_state(run_id, state)
            self._emit_event(run_id, {
                "event": "accepted",
                "timestamp": _utc_timestamp(),
            })
            return {
                "run_id": run_id,
                "disposition": ACCEPTED,
                "stage": ACCEPTED,
                "message": "Workflow complete. All stages passed.",
            }

        if transition == BLOCKED:
            state["disposition"] = BLOCKED
            state["current_stage"] = BLOCKED
            self.save_state(run_id, state)
            self._emit_event(run_id, {
                "event": "blocked",
                "reason": result.get("block_reason", "evaluator returned BLOCKED"),
                "timestamp": _utc_timestamp(),
            })
            return {
                "run_id": run_id,
                "disposition": BLOCKED,
                "stage": BLOCKED,
                "message": result.get(
                    "block_reason",
                    "Workflow blocked. Evaluator returned BLOCKED."
                ),
            }

        # Transition to next stage
        next_stage = self._get_stage(workflow, transition)
        state["current_stage"] = transition
        state["transitions"].append({
            "from": stage["id"],
            "to": transition,
            "disposition": result["disposition"],
        })
        self.save_state(run_id, state)

        # Compile next packet
        prior_findings = self._extract_prior_findings(
            result, stage, next_stage, workflow
        )
        packet = self._compile_packet(
            workflow, next_stage, state, self.run_dir(run_id), prior_findings
        )
        self._record_packet(run_id, state, packet)

        return {
            "run_id": run_id,
            "stage": transition,
            "iteration": state["stage_iterations"].get(transition, 0),
            "packet_hash": packet["hash"],
            "packet_path": str(packet["path"].relative_to(self.repo_root)),
            "packet_abs_path": str(packet["path"]),
            "disposition": None,
            "instructions": _driver_instructions(packet["path"]),
        }

    # --- Status and inspection ---

    def status(self, run_id: str) -> dict[str, Any]:
        """Return the current run status."""
        state = self.load_state(run_id)
        return {
            "run_id": run_id,
            "workflow_id": state["workflow_id"],
            "workflow_version": state["workflow_version"],
            "repo_commit": state["repo_commit"],
            "current_stage": state["current_stage"],
            "disposition": state["disposition"],
            "iteration": state["iteration"],
            "stage_iterations": state["stage_iterations"],
            "packets_emitted": len(state["packet_hashes"]),
            "results_received": len(state["result_hashes"]),
            "transitions": state["transitions"],
        }

    def replay(self, run_id: str) -> dict[str, Any]:
        """Reload state and recompile the current packet to prove determinism."""
        state = self.load_state(run_id)
        workflow = self.load_workflow(state["workflow_id"])
        stage = self._get_stage(workflow, state["current_stage"])
        prior_findings = self._load_prior_findings_for_current(
            run_id, state, workflow
        )
        # The stage_iterations was incremented after the last packet was
        # compiled, so temporarily restore the iteration the last packet
        # used, so recompilation produces the same bytes.
        last_pkt = state["packet_hashes"][-1] if state["packet_hashes"] else None
        if last_pkt and last_pkt["stage"] == state["current_stage"]:
            saved = state["stage_iterations"].get(state["current_stage"], 0)
            state["stage_iterations"][state["current_stage"]] = last_pkt["iteration"]
        else:
            saved = None
        packet = self._compile_packet(
            workflow, stage, state, self.run_dir(run_id), prior_findings
        )
        if saved is not None:
            state["stage_iterations"][state["current_stage"]] = saved
        # The recompiled hash must match the last emitted packet hash
        last_hash = last_pkt["hash"] if last_pkt else None
        return {
            "run_id": run_id,
            "stage": state["current_stage"],
            "recompiled_hash": packet["hash"],
            "last_recorded_hash": last_hash,
            "deterministic": packet["hash"] == last_hash if last_hash else True,
        }

    # --- Interventions ---

    def intervene(self, run_id: str, text: str, stage: str | None = None) -> dict[str, Any]:
        """Record a manual intervention during a run."""
        state = self.load_state(run_id)
        if stage is None:
            stage = state["current_stage"]
        run_dir = self.run_dir(run_id)
        interventions_dir = run_dir / "interventions"
        interventions_dir.mkdir(parents=True, exist_ok=True)
        existing = sorted(interventions_dir.glob("*.json"))
        next_num = len(existing)
        path = interventions_dir / f"{next_num:04d}.json"
        record = {
            "stage": stage,
            "text": text,
            "encoded": False,
            "timestamp": _utc_timestamp(),
        }
        path.write_text(
            json.dumps(record, sort_keys=True, indent=2) + "\n",
            encoding="utf-8",
        )
        self._emit_event(run_id, {
            "event": "intervene",
            "stage": stage,
            "text": text,
            "timestamp": _utc_timestamp(),
        })
        return {"run_id": run_id, "intervention_path": str(path), "record": record}

    def debt(self, run_id: str) -> dict[str, Any]:
        """Show unencoded workflow debt (interventions with encoded=false)."""
        run_dir = self.run_dir(run_id)
        interventions_dir = run_dir / "interventions"
        unencoded = []
        if interventions_dir.is_dir():
            for path in sorted(interventions_dir.glob("*.json")):
                record = json.loads(path.read_text(encoding="utf-8"))
                if not record.get("encoded", False):
                    unencoded.append({
                        "path": str(path.relative_to(self.repo_root)),
                        "stage": record.get("stage", ""),
                        "text": record.get("text", ""),
                    })
        return {
            "run_id": run_id,
            "unencoded_count": len(unencoded),
            "interventions": unencoded,
        }

    # --- State persistence ---

    def load_state(self, run_id: str) -> dict[str, Any]:
        """Load the mutable state for a run."""
        path = self.run_dir(run_id) / "state.json"
        if not path.is_file():
            raise WorkflowError(f"no such run: {run_id}")
        return json.loads(path.read_text(encoding="utf-8"))

    def save_state(self, run_id: str, state: dict[str, Any]) -> None:
        """Save the mutable state for a run."""
        path = self.run_dir(run_id) / "state.json"
        path.parent.mkdir(parents=True, exist_ok=True)
        # Write atomically
        tmp = path.with_suffix(".tmp")
        tmp.write_text(
            json.dumps(state, sort_keys=True, indent=2) + "\n",
            encoding="utf-8",
        )
        tmp.replace(path)

    # --- Internal: stage lookup ---

    def _get_stage(self, workflow: dict[str, Any], stage_id: str) -> dict[str, Any]:
        """Look up a stage by id in the workflow definition."""
        for stage in workflow["stages"]:
            if stage["id"] == stage_id:
                return stage
        if stage_id in (ACCEPTED, BLOCKED):
            raise WorkflowError(f"stage {stage_id} is terminal, no definition")
        raise WorkflowError(
            f"unknown stage: {stage_id} in workflow {workflow['id']}"
        )

    # --- Internal: packet compilation ---

    def _compile_packet(
        self,
        workflow: dict[str, Any],
        stage: dict[str, Any],
        state: dict[str, Any],
        run_dir: Path,
        prior_findings: list[dict[str, Any]],
    ) -> dict[str, Any]:
        """Deterministically compile a guidance packet.

        The packet bytes are assembled from:
        - A deterministic header (workflow, commit, stage, iteration, args,
          prior findings)
        - Fragment contents in the declared order

        No timestamps, no run_id, no filesystem paths appear in the hashed
        bytes. The hash is SHA-256 of the exact UTF-8 encoded packet text.
        """
        stage_iteration = state["stage_iterations"].get(stage["id"], 0)

        # Build header
        header_lines = [
            f"WORKFLOW: {workflow['id']} v{workflow['version']}",
            f"COMMIT: {state['repo_commit']}",
            f"STAGE: {stage['id']}",
            f"ITERATION: {stage_iteration}",
            f"ARGS: {json.dumps(state['normalized_args'], sort_keys=True, separators=(',', ':'))}",
        ]

        if prior_findings:
            header_lines.append(
                f"PRIOR_FINDINGS: {json.dumps(prior_findings, sort_keys=True, separators=(',', ':'))}"
            )
        else:
            header_lines.append("PRIOR_FINDINGS: []")

        header = _FIELD_SEP.join(header_lines)

        # Load fragments in declared order
        fragment_paths = stage.get("fragments", [])
        fragments = []
        for frag_path in fragment_paths:
            content = self.load_fragment(frag_path)
            fragments.append(f"{_PACKET_SEP}{frag_path} ---\n{content}")

        # Assemble packet
        packet_text = header + _HEADER_SEP + _PACKET_SEP.join([])  # no-op for join safety
        # Actually assemble: header, then each fragment section
        body = ""
        for frag_label, frag_content in zip(fragment_paths, fragments):
            body += frag_content
        if not fragment_paths:
            body = "\n(no fragments for this stage)"

        packet_text = header + _HEADER_SEP + body

        # Ensure consistent line endings (LF)
        packet_text = packet_text.replace("\r\n", "\n").replace("\r", "\n")

        # Encode
        packet_bytes = packet_text.encode("utf-8")

        # Hash
        packet_hash = hashlib.sha256(packet_bytes).hexdigest()

        # Write to packets/
        packets_dir = run_dir / "packets"
        packets_dir.mkdir(parents=True, exist_ok=True)
        filename = f"{stage['id']}-{stage_iteration:04d}.txt"
        path = packets_dir / filename
        path.write_bytes(packet_bytes)

        return {
            "hash": packet_hash,
            "path": path,
            "stage": stage["id"],
            "iteration": stage_iteration,
            "size": len(packet_bytes),
        }

    def _record_packet(
        self, run_id: str, state: dict[str, Any], packet: dict[str, Any]
    ) -> None:
        """Record a packet in the run state and emit an event."""
        state["packet_hashes"].append({
            "stage": packet["stage"],
            "iteration": packet["iteration"],
            "hash": packet["hash"],
            "path": str(packet["path"].relative_to(self.repo_root)),
        })
        # Increment global iteration
        state["iteration"] += 1
        # Increment stage iteration
        stage_id = packet["stage"]
        state["stage_iterations"][stage_id] = (
            state["stage_iterations"].get(stage_id, 0) + 1
        )
        self.save_state(run_id, state)
        self._emit_event(run_id, {
            "event": "packet",
            "stage": packet["stage"],
            "iteration": packet["iteration"],
            "hash": packet["hash"],
            "size": packet["size"],
            "timestamp": _utc_timestamp(),
        })

    # --- Internal: result handling ---

    def _load_and_validate_result(
        self,
        result_path: str,
        stage: dict[str, Any],
        run_id: str,
        state: dict[str, Any],
    ) -> dict[str, Any]:
        """Load a result file and validate it against the stage's schema."""
        path = Path(result_path)
        if not path.is_file():
            raise WorkflowError(f"result file not found: {result_path}")

        try:
            result = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as error:
            raise WorkflowError(
                f"result is not valid JSON: {error}"
            ) from error

        # Determine which schema to use
        if stage["type"] == EVALUATOR:
            schema_name = stage.get("result_schema", SCHEMA_EVALUATOR)
        else:
            schema_name = stage.get("result_schema", SCHEMA_WORKER)

        schema = self.load_schema(schema_name)
        _validate_result(result, schema, stage["type"])

        # Copy result into the run directory
        results_dir = self.run_dir(run_id) / "results"
        results_dir.mkdir(parents=True, exist_ok=True)
        stage_iter = state["stage_iterations"].get(stage["id"], 0)
        dest = results_dir / f"{stage['id']}-{stage_iter:04d}.json"
        dest.write_text(
            json.dumps(result, sort_keys=True, indent=2) + "\n",
            encoding="utf-8",
        )
        result["_recorded_path"] = str(dest.relative_to(self.repo_root))
        return result

    def _record_result(
        self, run_id: str, state: dict[str, Any],
        result: dict[str, Any], stage: dict[str, Any]
    ) -> None:
        """Record a result hash in the run state."""
        result_path = result.get("_recorded_path", "")
        if result_path:
            path = self.repo_root / result_path
            result_bytes = path.read_bytes()
        else:
            result_bytes = json.dumps(
                result, sort_keys=True, separators=(",", ":")
            ).encode("utf-8")
        result_hash = hashlib.sha256(result_bytes).hexdigest()
        state["result_hashes"].append({
            "stage": stage["id"],
            "iteration": state["stage_iterations"].get(stage["id"], 0),
            "hash": result_hash,
            "path": result_path,
            "disposition": result.get("disposition", ""),
        })
        self.save_state(run_id, state)

    # --- Internal: transitions ---

    def _determine_transition(
        self,
        workflow: dict[str, Any],
        stage: dict[str, Any],
        result: dict[str, Any],
        state: dict[str, Any],
    ) -> str:
        """Determine the next stage id based on the stage type and result."""
        disposition = result.get("disposition", "")

        if stage["type"] == LINEAR:
            if disposition != PASS:
                raise WorkflowError(
                    f"linear stage {stage['id']} requires disposition PASS, "
                    f"got {disposition}"
                )
            return stage["next"]

        if stage["type"] == EVALUATOR:
            if disposition == PASS:
                return stage["pass_transition"]
            if disposition == CHANGES_REQUIRED:
                # Check iteration limit
                max_iter = stage.get("max_iterations", 3)
                current_iter = state["stage_iterations"].get(stage["id"], 0)
                if current_iter >= max_iter:
                    result["block_reason"] = (
                        f"iteration limit exceeded for {stage['id']}: "
                        f"{current_iter}/{max_iter}"
                    )
                    return BLOCKED
                return stage["fail_transition"]
            if disposition == BLOCKED:
                return BLOCKED
            raise WorkflowError(
                f"evaluator {stage['id']} returned invalid disposition: "
                f"{disposition}"
            )

        if stage["type"] == BOUNDED_REVISION:
            if disposition != PASS:
                raise WorkflowError(
                    f"revision stage {stage['id']} requires disposition PASS, "
                    f"got {disposition}"
                )
            return stage["next"]

        if stage["type"] == GATE:
            if disposition == PASS:
                return stage["pass_transition"]
            if disposition == FAIL:
                max_iter = stage.get("max_iterations", 3)
                current_iter = state["stage_iterations"].get(stage["id"], 0)
                if current_iter >= max_iter:
                    result["block_reason"] = (
                        f"iteration limit exceeded for gate {stage['id']}: "
                        f"{current_iter}/{max_iter}"
                    )
                    return BLOCKED
                return stage["fail_transition"]
            raise WorkflowError(
                f"gate {stage['id']} returned invalid disposition: {disposition}"
            )

        raise WorkflowError(f"unknown stage type: {stage['type']}")

    def _extract_prior_findings(
        self,
        result: dict[str, Any],
        stage: dict[str, Any],
        next_stage_id: str,
        workflow: dict[str, Any],
    ) -> list[dict[str, Any]]:
        """Extract findings to forward into the next revision packet.

        For evaluator/gate stages that trigger a revision, the blocking
        findings are forwarded verbatim. For all other transitions, no
        findings are forwarded.
        """
        if stage["type"] in (EVALUATOR, GATE):
            if result.get("disposition") in (CHANGES_REQUIRED, FAIL):
                findings = result.get("findings", [])
                # Forward only blocking findings, verbatim
                forwarded = [
                    f for f in findings
                    if f.get("severity") == "blocking"
                ]
                return forwarded
        return []

    def _load_prior_findings_for_current(
        self, run_id: str, state: dict[str, Any], workflow: dict[str, Any]
    ) -> list[dict[str, Any]]:
        """Load prior findings for the current stage by replaying transitions."""
        # For revision stages, find the evaluator/gate that triggered this
        # revision and load its findings from the results directory.
        current = state["current_stage"]
        stage = self._get_stage(workflow, current)
        if stage["type"] != BOUNDED_REVISION:
            return []

        # Find the last result that triggered a transition to this revision stage
        results_dir = self.run_dir(run_id) / "results"
        if not results_dir.is_dir():
            return []

        # Walk backwards through results to find the triggering evaluator/gate
        for entry in reversed(state["result_hashes"]):
            if entry["disposition"] in (CHANGES_REQUIRED, FAIL):
                result_path = self.repo_root / entry["path"]
                if result_path.is_file():
                    result = json.loads(result_path.read_text(encoding="utf-8"))
                    findings = result.get("findings", [])
                    return [
                        f for f in findings
                        if f.get("severity") == "blocking"
                    ]
        return []

    # --- Internal: gates ---

    def _run_gate(
        self,
        workflow: dict[str, Any],
        stage: dict[str, Any],
        state: dict[str, Any],
        run_id: str,
    ) -> dict[str, Any]:
        """Run deterministic gate checks and return a structured result."""
        checks = stage.get("checks", [])
        args = state["normalized_args"]
        findings = []
        all_passed = True

        for check in checks:
            check_id = check["id"]
            command_template = check["command"]
            # Substitute arguments
            command = _substitute_args(command_template, args)
            try:
                proc = subprocess.run(
                    command,
                    shell=True,
                    capture_output=True,
                    text=True,
                    cwd=self.repo_root,
                    timeout=300,
                )
                if proc.returncode != 0:
                    all_passed = False
                    findings.append({
                        "id": f"GATE-{check_id.upper()}",
                        "severity": "blocking",
                        "check": check_id,
                        "problem": (
                            f"command exited {proc.returncode}: "
                            f"{proc.stderr.strip()[:500] or proc.stdout.strip()[:500]}"
                        ),
                        "required_result": check.get(
                            "required_result",
                            f"command must exit 0: {command}"
                        ),
                    })
            except subprocess.TimeoutExpired:
                all_passed = False
                findings.append({
                    "id": f"GATE-{check_id.upper()}",
                    "severity": "blocking",
                    "check": check_id,
                    "problem": f"command timed out after 300s: {command}",
                    "required_result": check.get(
                        "required_result",
                        f"command must complete within 300s: {command}"
                    ),
                })
            except OSError as error:
                all_passed = False
                findings.append({
                    "id": f"GATE-{check_id.upper()}",
                    "severity": "blocking",
                    "check": check_id,
                    "problem": f"command failed to execute: {error}",
                    "required_result": check.get(
                        "required_result",
                        f"command must be executable: {command}"
                    ),
                })

        # Record the gate result
        results_dir = self.run_dir(run_id) / "results"
        results_dir.mkdir(parents=True, exist_ok=True)
        stage_iter = state["stage_iterations"].get(stage["id"], 0)
        result = {
            "disposition": PASS if all_passed else FAIL,
            "findings": findings,
        }
        dest = results_dir / f"{stage['id']}-{stage_iter:04d}.json"
        dest.write_text(
            json.dumps(result, sort_keys=True, indent=2) + "\n",
            encoding="utf-8",
        )
        result["_recorded_path"] = str(dest.relative_to(self.repo_root))
        return result

    # --- Internal: events ---

    def _emit_event(self, run_id: str, event: dict[str, Any]) -> None:
        """Append an event to the run's events.jsonl."""
        path = self.run_dir(run_id) / "events.jsonl"
        path.parent.mkdir(parents=True, exist_ok=True)
        line = json.dumps(event, sort_keys=True, ensure_ascii=False)
        with open(path, "a", encoding="utf-8") as f:
            f.write(line + "\n")


# ---------------------------------------------------------------------------
# Validation
# ---------------------------------------------------------------------------

def _validate_workflow(data: dict[str, Any], path: Path) -> None:
    """Validate the structural integrity of a workflow definition."""
    required_keys = {"id", "version", "stages"}
    missing = required_keys - set(data)
    if missing:
        raise WorkflowError(f"{path}: missing keys: {', '.join(sorted(missing))}")

    if not isinstance(data["id"], str) or not data["id"]:
        raise WorkflowError(f"{path}: id must be a nonempty string")
    if not isinstance(data["version"], int) or data["version"] < 1:
        raise WorkflowError(f"{path}: version must be a positive integer")
    if not isinstance(data["stages"], list) or not data["stages"]:
        raise WorkflowError(f"{path}: stages must be a nonempty list")

    stage_ids = set()
    for i, stage in enumerate(data["stages"]):
        if not isinstance(stage, dict):
            raise WorkflowError(f"{path}: stages[{i}] must be an object")
        sid = stage.get("id")
        if not isinstance(sid, str) or not sid:
            raise WorkflowError(f"{path}: stages[{i}].id must be a nonempty string")
        if sid in stage_ids:
            raise WorkflowError(f"{path}: duplicate stage id: {sid}")
        stage_ids.add(sid)

        stype = stage.get("type")
        if stype not in (LINEAR, EVALUATOR, BOUNDED_REVISION, GATE):
            raise WorkflowError(
                f"{path}: stages[{i}].type must be one of: "
                f"{LINEAR}, {EVALUATOR}, {BOUNDED_REVISION}, {GATE}"
            )

        if stype == LINEAR:
            if "next" not in stage:
                raise WorkflowError(f"{path}: {sid}: linear stage requires 'next'")
        elif stype == EVALUATOR:
            for key in ("pass_transition", "fail_transition", "max_iterations"):
                if key not in stage:
                    raise WorkflowError(
                        f"{path}: {sid}: evaluator stage requires '{key}'"
                    )
        elif stype == BOUNDED_REVISION:
            for key in ("revision_target", "next"):
                if key not in stage:
                    raise WorkflowError(
                        f"{path}: {sid}: bounded-revision stage requires '{key}'"
                    )
        elif stype == GATE:
            for key in ("pass_transition", "fail_transition", "max_iterations"):
                if key not in stage:
                    raise WorkflowError(
                        f"{path}: {sid}: gate stage requires '{key}'"
                    )
            if "checks" not in stage or not isinstance(stage["checks"], list):
                raise WorkflowError(f"{path}: {sid}: gate stage requires 'checks' list")

    # Validate transitions point to valid stages or terminal states
    for stage in data["stages"]:
        sid = stage["id"]
        for tkey in ("next", "pass_transition", "fail_transition"):
            if tkey in stage:
                target = stage[tkey]
                if target not in stage_ids and target not in (ACCEPTED, BLOCKED):
                    raise WorkflowError(
                        f"{path}: {sid}.{tkey} points to unknown stage: {target}"
                    )


def _validate_result(
    result: dict[str, Any], schema: dict[str, Any], stage_type: str
) -> None:
    """Validate a result against a schema (structural, dependency-free)."""
    required_fields = schema.get("required_fields", [])
    for field in required_fields:
        if field not in result:
            raise WorkflowError(
                f"result missing required field: {field}"
            )

    # Validate disposition
    disposition = result.get("disposition")
    valid_dispositions = schema.get("valid_dispositions", [])
    if valid_dispositions and disposition not in valid_dispositions:
        raise WorkflowError(
            f"result has invalid disposition: {disposition}; "
            f"expected one of: {', '.join(valid_dispositions)}"
        )

    # Validate findings
    if "findings" in result:
        findings = result["findings"]
        if not isinstance(findings, list):
            raise WorkflowError("result.findings must be a list")
        finding_fields = schema.get("finding_fields", [])
        for i, finding in enumerate(findings):
            if not isinstance(finding, dict):
                raise WorkflowError(f"findings[{i}] must be an object")
            for field in finding_fields:
                if field not in finding:
                    raise WorkflowError(
                        f"findings[{i}] missing required field: {field}"
                    )

    # Malformed results fail closed: if we got here without raising,
    # the result is structurally valid.


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _utc_timestamp() -> str:
    """A human-readable UTC timestamp. Never used in packet hashes."""
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())


def _substitute_args(template: str, args: dict[str, str]) -> str:
    """Substitute {arg_name} placeholders in a command template."""
    result = template
    for key, value in args.items():
        result = result.replace(f"{{{key}}}", value)
    return result


def _driver_instructions(packet_path: Path) -> str:
    """The instructions a parent agent follows for each packet."""
    return (
        f"1. Start a clean agent.\n"
        f"2. Give it exactly the contents of {packet_path}.\n"
        f"3. Require its structured result as JSON at a path you choose.\n"
        f"4. When it finishes, run: tpt ... advance <run-id> --result <path>\n"
        f"5. Follow the next packet emitted by tpt.\n"
        f"6. Stop only at ACCEPTED or BLOCKED."
    )
