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
import re
import shlex
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

# Argument values reach gate command lines and packet headers. Anything
# outside this set is refused at seed time rather than quoted downstream,
# so a value can never carry shell syntax into a check.
_ARG_SAFE = re.compile(r"\A[A-Za-z0-9][A-Za-z0-9._/-]{0,199}\Z")

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

    def __init__(self, repo_root: Path, workflows_dir: Path,
                 runs_dir: Path | None = None) -> None:
        self.repo_root = repo_root.resolve()
        self.workflows_dir = workflows_dir.resolve()
        self.pipelines_dir = self.workflows_dir / "pipelines"
        self.fragments_dir = self.workflows_dir / "fragments"
        self.schemas_dir = self.workflows_dir / "schema"
        if runs_dir is None:
            runs_dir = self.repo_root / "build" / "tpt-runs"
        self.runs_dir = Path(runs_dir).resolve()

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

    # --- Guidance source pinning ---

    def source_digest(self, workflow: dict[str, Any]) -> str:
        """Digest every byte of guidance source this workflow can emit.

        A run is bound to this digest at seed time. The workflow version is
        an operator's promise; the digest is the machine's check on it, so a
        fragment edited between two stages of one run cannot pass unnoticed
        as the same guidance.
        """
        material: dict[str, str] = {}
        path = self.pipelines_dir / f"{workflow['id']}.json"
        material["pipeline"] = hashlib.sha256(path.read_bytes()).hexdigest()
        for stage in workflow["stages"]:
            for frag in stage.get("fragments", []):
                key = f"fragment:{frag}"
                if key in material:
                    continue
                frag_path = self.fragments_dir / frag
                if not frag_path.is_file():
                    raise WorkflowError(f"missing fragment: {frag}")
                material[key] = hashlib.sha256(
                    frag_path.read_bytes()
                ).hexdigest()
            schema_name = stage.get("result_schema")
            if schema_name:
                key = f"schema:{schema_name}"
                if key not in material:
                    schema_path = self.schemas_dir / schema_name
                    if not schema_path.is_file():
                        raise WorkflowError(f"unknown schema: {schema_name}")
                    material[key] = hashlib.sha256(
                        schema_path.read_bytes()
                    ).hexdigest()
        encoded = json.dumps(
            material, sort_keys=True, separators=(",", ":")
        ).encode("utf-8")
        return hashlib.sha256(encoded).hexdigest()

    def _verify_run_binding(
        self, run_id: str, state: dict[str, Any], workflow: dict[str, Any]
    ) -> None:
        """Refuse to advance a run whose source or manifest has drifted."""
        manifest_path = self.run_dir(run_id) / "manifest.json"
        if not manifest_path.is_file():
            raise WorkflowError(
                f"run {run_id} has no manifest.json; it cannot be advanced"
            )
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        if "source_digest" not in manifest:
            raise WorkflowError(
                f"run {run_id} was seeded before its guidance source was "
                f"pinned and cannot be advanced; seed a new run"
            )
        for key in ("workflow_id", "workflow_version", "repo_commit",
                    "normalized_args", "source_digest"):
            if manifest.get(key) != state.get(key):
                raise WorkflowError(
                    f"run {run_id} state disagrees with its manifest on "
                    f"{key}: manifest {manifest.get(key)!r}, "
                    f"state {state.get(key)!r}"
                )
        if manifest["workflow_version"] != workflow["version"]:
            raise WorkflowError(
                f"run {run_id} was seeded from {workflow['id']} "
                f"v{manifest['workflow_version']} but the definition on disk "
                f"is v{workflow['version']}; seed a new run"
            )
        current = self.source_digest(workflow)
        if current != manifest["source_digest"]:
            raise WorkflowError(
                f"guidance source changed since run {run_id} was seeded "
                f"(digest {manifest['source_digest'][:12]} -> "
                f"{current[:12]}); bump the workflow version and seed a new "
                f"run rather than advancing this one"
            )

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

    def _display_path(self, path: Path) -> str:
        """A repo-relative path where possible, absolute when the runs
        directory lies outside the repository."""
        try:
            return str(path.relative_to(self.repo_root))
        except ValueError:
            return str(path)

    def _stage_was_issued(self, state: dict[str, Any], stage_id: str) -> bool:
        """Whether the last packet emitted was for the run's current stage."""
        packets = state.get("packet_hashes", [])
        if not packets:
            return False
        return packets[-1]["stage"] == stage_id

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

        _validate_arg_values(args, arg_schema)
        digest = self.source_digest(workflow)

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
            "source_digest": digest,
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
            "source_digest": digest,
            "current_stage": first_stage,
            "iteration": 0,
            "stage_iterations": {},
            "stage_failures": {},
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
            "packet_path": self._display_path(packet["path"]),
            "packet_abs_path": str(packet["path"]),
            "instructions": _driver_instructions(
                packet["path"], packet["hash"]),
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
        self._verify_run_binding(run_id, state, workflow)
        stage = self._get_stage(workflow, state["current_stage"])
        if not self._stage_was_issued(state, stage["id"]):
            raise WorkflowError(
                f"run {run_id} is at stage {stage['id']} but no packet was "
                f"ever emitted for it; the run state is inconsistent and no "
                f"result for it can be accepted"
            )

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

        # Determine the transition before anything is persisted. A result the
        # engine refuses must leave no trace in the run: otherwise a rejected
        # result stays in results/ and result_hashes, where the prior-findings
        # lookup can later pick it up as though it had been accepted.
        transition = self._determine_transition(
            workflow, stage, result, state
        )

        # Record the result
        self._record_result(run_id, state, result, stage)

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

        # Transition to next stage. The packet is compiled first and the
        # advance is persisted with it: a run must never be recorded at a
        # stage whose guidance was never issued, because the next advance
        # would then accept a result for guidance no agent ever received.
        next_stage = self._get_stage(workflow, transition)
        prior_findings = self._extract_prior_findings(
            result, stage, next_stage, workflow
        )
        packet = self._compile_packet(
            workflow, next_stage, state, self.run_dir(run_id), prior_findings
        )
        state["current_stage"] = transition
        state["transitions"].append({
            "from": stage["id"],
            "to": transition,
            "disposition": result["disposition"],
        })
        self._record_packet(run_id, state, packet)

        return {
            "run_id": run_id,
            "stage": transition,
            "iteration": state["stage_iterations"].get(transition, 0),
            "packet_hash": packet["hash"],
            "packet_path": self._display_path(packet["path"]),
            "packet_abs_path": str(packet["path"]),
            "disposition": None,
            "instructions": _driver_instructions(
                packet["path"], packet["hash"]),
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
        self._verify_run_binding(run_id, state, workflow)
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
                        "path": self._display_path(path),
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
            f"SOURCE_DIGEST: {state['source_digest']}",
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
            "path": self._display_path(packet["path"]),
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
        self._check_answers_current_packet(run_id, state, stage, result)
        return result

    def _check_answers_current_packet(
        self, run_id: str, state: dict[str, Any],
        stage: dict[str, Any], result: dict[str, Any],
    ) -> None:
        """Require a result to name the packet it answers.

        Without this, nothing distinguishes a worker's answer to the guidance
        just issued from a result produced for some other packet and submitted
        later. The driver would then be choosing, in effect, which guidance a
        stage was answering.
        """
        packets = state.get("packet_hashes", [])
        if not packets:
            raise WorkflowError(
                f"run {run_id} has emitted no packet to answer"
            )
        expected = packets[-1]["hash"]
        claimed = result.get("packet_hash")
        if claimed is None:
            raise WorkflowError(
                f"result for {stage['id']} does not say which packet it "
                f"answers; add \"packet_hash\": \"{expected}\""
            )
        if claimed != expected:
            raise WorkflowError(
                f"result for {stage['id']} answers packet {claimed}, but the "
                f"packet awaiting an answer is {expected}"
            )

    def _record_result(
        self, run_id: str, state: dict[str, Any],
        result: dict[str, Any], stage: dict[str, Any]
    ) -> None:
        """Persist a result into the run and record its hash in the state."""
        results_dir = self.run_dir(run_id) / "results"
        results_dir.mkdir(parents=True, exist_ok=True)
        stage_iter = state["stage_iterations"].get(stage["id"], 0)
        dest = results_dir / f"{stage['id']}-{stage_iter:04d}.json"
        stored = {k: v for k, v in result.items() if not k.startswith("_")}
        result_bytes = (
            json.dumps(stored, sort_keys=True, indent=2) + "\n"
        ).encode("utf-8")
        dest.write_bytes(result_bytes)
        result_path = self._display_path(dest)
        result["_recorded_path"] = result_path
        result_hash = hashlib.sha256(result_bytes).hexdigest()
        state["result_hashes"].append({
            "stage": stage["id"],
            "iteration": stage_iter,
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

        if stage["type"] in (LINEAR, BOUNDED_REVISION):
            if disposition == BLOCKED:
                result.setdefault(
                    "block_reason",
                    f"{stage['id']} reported it could not complete the work: "
                    f"{result.get('summary', '')}".strip()
                )
                return BLOCKED
            if disposition != PASS:
                kind = "linear" if stage["type"] == LINEAR else "revision"
                raise WorkflowError(
                    f"{kind} stage {stage['id']} requires disposition PASS or "
                    f"BLOCKED, got {disposition}"
                )
            self._clear_failures(state, stage["id"])
            return stage["next"]

        if stage["type"] == EVALUATOR:
            if disposition == PASS:
                self._clear_failures(state, stage["id"])
                return stage["pass_transition"]
            if disposition == CHANGES_REQUIRED:
                return self._bounded_fail_transition(stage, result, state)
            if disposition == BLOCKED:
                return BLOCKED
            raise WorkflowError(
                f"evaluator {stage['id']} returned invalid disposition: "
                f"{disposition}"
            )

        if stage["type"] == GATE:
            if disposition == PASS:
                self._clear_failures(state, stage["id"])
                return stage["pass_transition"]
            if disposition == FAIL:
                return self._bounded_fail_transition(stage, result, state)
            raise WorkflowError(
                f"gate {stage['id']} returned invalid disposition: {disposition}"
            )

        raise WorkflowError(f"unknown stage type: {stage['type']}")

    def _failures(self, state: dict[str, Any], stage_id: str) -> int:
        return state.setdefault("stage_failures", {}).get(stage_id, 0)

    def _clear_failures(self, state: dict[str, Any], stage_id: str) -> None:
        state.setdefault("stage_failures", {})[stage_id] = 0

    def _bounded_fail_transition(
        self, stage: dict[str, Any], result: dict[str, Any],
        state: dict[str, Any],
    ) -> str:
        """Route a failing evaluator or gate, bounded by its own failures.

        The budget counts this stage's consecutive failures, not how often it
        has been entered. A stage re-entered because some other loop revised
        the work has spent none of its own budget, so a genuine first failure
        is never mistaken for an exhausted one.
        """
        max_iter = stage.get("max_iterations", 3)
        failures = self._failures(state, stage["id"]) + 1
        if failures >= max_iter:
            result["block_reason"] = (
                f"iteration limit exceeded for {stage['id']}: "
                f"{failures}/{max_iter} consecutive failures"
            )
            return BLOCKED
        state.setdefault("stage_failures", {})[stage["id"]] = failures
        return stage["fail_transition"]

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
                # No shell. The command template is split once, before any
                # argument is substituted, so a value can only ever become a
                # single argv element and never shell syntax.
                argv = _gate_argv(command_template, args)
                proc = subprocess.run(
                    argv,
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

        # The caller persists the result once the transition is settled.
        return {
            "disposition": PASS if all_passed else FAIL,
            "findings": findings,
        }

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


def _gate_argv(template: str, args: dict[str, str]) -> list[str]:
    """Build a gate command's argv without ever consulting a shell.

    The template is tokenized first and substitution happens inside each
    token, so an argument value cannot introduce a word boundary, a
    redirection, or a second command.
    """
    try:
        tokens = shlex.split(template)
    except ValueError as error:
        raise WorkflowError(
            f"gate command is not a valid command line: {template}: {error}"
        ) from error
    if not tokens:
        raise WorkflowError("gate command is empty")
    return [_substitute_args(token, args) for token in tokens]


def _validate_arg_values(
    args: dict[str, str], arg_schema: dict[str, Any]
) -> None:
    """Refuse argument values that could not be safely substituted.

    Values reach gate command lines and hashed packet headers. Checking their
    shape once, at seed time, is what keeps both surfaces honest.
    """
    for name in sorted(args):
        value = args[name]
        pattern = arg_schema.get(name, {}).get("pattern")
        matcher = re.compile(pattern) if pattern else _ARG_SAFE
        if not matcher.fullmatch(value):
            raise WorkflowError(
                f"argument {name} has an unacceptable value: {value!r}; "
                f"expected {pattern or _ARG_SAFE.pattern}"
            )


def _driver_instructions(packet_path: Path, packet_hash: str) -> str:
    """The instructions a parent agent follows for each packet."""
    return (
        f"1. Start a clean agent.\n"
        f"2. Give it exactly the contents of {packet_path}, and tell it the\n"
        f"   packet hash {packet_hash}.\n"
        f"3. Require its structured result as JSON at a path you choose. The\n"
        f"   result must repeat that packet hash verbatim; tpt refuses a\n"
        f"   result that answers any other packet.\n"
        f"4. When it finishes, run: tpt ... advance <run-id> --result <path>\n"
        f"5. Follow the next packet emitted by tpt. Do not summarise it, add\n"
        f"   to it, or choose a different one.\n"
        f"6. Stop only at ACCEPTED or BLOCKED."
    )
