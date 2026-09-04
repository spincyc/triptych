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

import copy
import difflib
import fcntl
import hashlib
import json
import os
import re
import shlex
import shutil
import subprocess
import time
import tomllib
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

# Execution modes. A stage declares exactly one, and the declaration is
# workflow data: the host that drives a run never decides whether a stage is
# run by one agent, by a fan-out over lanes, or by tpt itself.
SINGLE = "single"
FANOUT = "fanout"
PROGRAM = "program"
AGENT_MODES = (SINGLE, FANOUT)

# How hard the model dispatched to a stage is told to think, weakest first.
# This is workflow data for the same reason the execution mode is: an effort
# level chosen at the console is an input to the run that nothing records,
# and the same packet answered at two levels is two different runs wearing
# one id. A gate runs no agent and declares none.
EFFORT_LEVELS = ("low", "medium", "high", "xhigh", "max")

# The only parallelism a fan-out stage may request. The workflow owns the lane
# set; the host owns only how many of those lanes run at once.
HOST_MAX = "host-max"

# A repair route names, for one value of a blocking finding's repair target,
# the stage that owns the repair. Declaration order is priority order.
REPAIR_ROUTES = "repair_routes"
REPAIR_TARGET = "repair_target"

# The reciprocal of a repair route, declared on the stage that does the repair:
# the repair targets this stage is an owner of. A route says where a run goes
# next; this says who a finding is *for*, which is not the same question once
# more than one owner exists. A finding whose owner did not win the route is
# held until that owner next runs, rather than discarded because someone else
# was earlier in declaration order.
REPAIRS = "repairs"

# The only join a fan-out stage may request. Every declared lane is required,
# lane findings are preserved verbatim under their lane identity in the
# declared lane order, and the disposition is the worst any lane returned.
STRICT_UNION = "strict-union"


# The severity of a finding whose defect lies in an artifact no stage of the
# run may write — repository guidance, the source library, the workflow itself.
# It is not blocking, because the document under production is not at fault and
# no revision of it could help; it is not advisory, because something really is
# wrong and someone really must fix it. It leaves the run as a durable
# escalation record instead of dying inside it as a note nobody reads.
ESCALATION = "escalation"


# The namespace a gate command may name the run itself in. A gate check is a
# shell command over the run's normalized arguments; the run's own identity —
# which workflow, at which version and digest, under which run id and from
# which seed commit — was not nameable there at all, so a check could compare a
# document against its arguments but never against the run producing it.
#
# The dot is what makes the addition safe rather than merely convenient. An
# argument name is a plain identifier, so `{run.run_id}` cannot be written by
# any argument a workflow declares, and a workflow that declares an argument
# called `run_id` still gets `{run_id}` for its own value and `{run.run_id}`
# for the engine's. `_validate_workflow` refuses an argument name in this
# namespace outright, so the two can never mean the same placeholder.
RUN_IDENTITY_PREFIX = "run."

# Dispositions
PASS = "PASS"
CHANGES_REQUIRED = "CHANGES_REQUIRED"
FAIL = "FAIL"

# Worst-first ordering for the strict-union join. Wall-clock completion order
# never enters this: the reduction reads only dispositions, in lane order.
_DISPOSITION_RANK = {PASS: 0, CHANGES_REQUIRED: 1, FAIL: 1, BLOCKED: 2}

# Repair outcomes a reviser reports, per finding it was given.
#
# These exist because convergence is a fact only the reviser holds. An
# evaluator re-reading a document cannot tell a defect that resisted repair
# from a different defect that happens to carry the same finding id, and for
# three iterations of one production it did not: every id the iteration bound
# named as still unrepaired named a different defect in a different file each
# time, and the earlier ones had in fact been repaired.
REPAIRED = "repaired"
NOT_REPAIRED = "not-repaired"

# Where an evaluation's standing blocking findings are kept so that something
# outside the run holds them.
#
# `build/tpt-runs/<run-id>/` is ignored output: `.gitignore` line 1 is
# `/build/`, `make clean` is `rm -rf build`, and `wt tidy` deletes it without
# asking. A `content-evaluation` result therefore reached nothing tracked at
# all, which is why a rescue pipeline that starts after research has no
# carry-forward and why one authoring worker went and read a dead run's result
# directory to find out what was standing against the leaf it was rewriting.
# This is the tracked home those findings did not have.
STANDING_FINDINGS_PATH = "evaluations/blocking-findings-v1.toml"

# Schema names
SCHEMA_WORKER = "worker-result.json"
SCHEMA_EVALUATOR = "evaluator-result.json"
SCHEMA_GATE = "gate-result.json"

PROTOCOL_VERSION = 1

# Bumping this invalidates every recorded workflow digest, because it changes
# what the digest is computed over rather than what the guidance says. Recipe 2
# added the bytes of every lane fragment: recipe 1 read only `stage.fragments`,
# so a fan-out stage's lane guidance — sixteen files, and the most substantive
# instructions the propers pipeline has — could be rewritten under a live run
# without the digest moving, while ARCHITECTURE.md said it could not.
DIGEST_RECIPE = 2

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
        # Where the tracked standing-findings record for a document is read
        # and written. Its own attribute rather than `repo_root` because this
        # is the engine's one write outside `build/`, into the working tree a
        # person is editing: a harness driving runs over published leaves
        # points it somewhere disposable so that exercising the behaviour does
        # not dirty the repository, and setting it to None turns the record
        # off entirely.
        self.standing_findings_root: Path | None = self.repo_root

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
        self._validate_repair_route_coverage(data, path)
        self._validate_repair_reporting(data, path)
        return data

    def _validate_repair_reporting(
        self, workflow: dict[str, Any], path: Path
    ) -> None:
        """A stage cannot be required to report what its schema forbids.

        `reports_repairs` on a stage whose result schema defines no
        `finding_disposition_fields` is a deadlock nothing else catches:
        `_record_repair_outcomes` demands the report once findings are
        forwarded there, and `_validate_result` refuses a result carrying it
        because the schema does not define it. The run seeds, advances to that
        stage, and then cannot move in either direction. Caught at load, it is
        a typo in a pipeline; caught at run time it is a wedged production.
        """
        for stage in workflow["stages"]:
            if not stage.get("reports_repairs"):
                continue
            schema = self.load_schema(self.schema_name_for(stage))
            if "finding_disposition_fields" not in schema:
                raise WorkflowError(
                    f"{path}: {stage['id']}: declares 'reports_repairs' but "
                    f"its result schema {self.schema_name_for(stage)} defines "
                    f"no 'finding_disposition_fields', so a result carrying "
                    f"the report is refused and a result without one is "
                    f"refused too; the stage could never advance"
                )

    def _validate_repair_route_coverage(
        self, workflow: dict[str, Any], path: Path
    ) -> None:
        """A routed stage's schema and its routes must name the same owners.

        They are two lists in two files, and nothing else keeps them agreed. A
        target the schema admits but no route names would fall through to
        `fail_transition` in silence — a defect quietly routed to the wrong
        owner is exactly what naming the owner exists to prevent — and a route
        for a target the schema rejects can never fire.
        """
        for stage in workflow["stages"]:
            routes = stage.get(REPAIR_ROUTES)
            if not routes:
                continue
            schema_name = self.schema_name_for(stage)
            enums = self.load_schema(schema_name).get("finding_enums", {})
            admitted = enums.get(REPAIR_TARGET)
            if admitted is None:
                raise WorkflowError(
                    f"{path}: {stage['id']} declares {REPAIR_ROUTES}, so its "
                    f"schema {schema_name} must enumerate the values of "
                    f"{REPAIR_TARGET} its findings may carry"
                )
            declared = {route[REPAIR_TARGET] for route in routes}
            if set(admitted) != declared:
                raise WorkflowError(
                    f"{path}: {stage['id']} routes "
                    f"{', '.join(sorted(declared))} but {schema_name} admits "
                    f"{', '.join(sorted(admitted))}; every value a finding "
                    f"may carry needs a route, and every route needs a value"
                )
            self._validate_repair_ownership(workflow, stage, routes, path)

    @staticmethod
    def _validate_repair_ownership(
        workflow: dict[str, Any], stage: dict[str, Any],
        routes: list[dict[str, Any]], path: Path,
    ) -> None:
        """Every repair target has at least one stage that admits to owning it.

        A route says where the run goes; `repairs` says whose the finding is.
        They are two halves of one fact and nothing else keeps them agreed, so
        the stage a route points at must declare the target it is pointed at
        for. A target may have more owners than that — `authoring` is owned by
        `author-proper` as well as by `content-revision`, because both write
        the leaf and either may be the next to run — but it may not have fewer
        than the routes claim, or a finding would be held for a stage that
        never admits to being able to repair it.
        """
        owns: dict[str, set[str]] = {}
        for other in workflow["stages"]:
            for target in other.get(REPAIRS) or []:
                owns.setdefault(target, set()).add(other["id"])
        for route in routes:
            target = route[REPAIR_TARGET]
            destination = route["transition"]
            if destination in (ACCEPTED, BLOCKED):
                continue
            if destination not in owns.get(target, set()):
                raise WorkflowError(
                    f"{path}: {stage['id']} routes {REPAIR_TARGET} "
                    f"{target!r} to {destination}, which does not declare "
                    f"'{REPAIRS}': [\"{target}\"]. The stage a repair is sent "
                    f"to must say it owns that repair, or a finding held for "
                    f"its owner has no owner to be held for."
                )

    # --- Document discovery ---

    def list_documents(self, workflow: dict[str, Any]) -> list[str]:
        """Every document id this workflow can be seeded for, sorted.

        A document id is a path with no marker in the filesystem to say so,
        and until now the only way to obtain one was to go reading `src/`.
        The workflow declares where its documents live, because the workflow
        is what knows.
        """
        discovery = workflow.get("document_discovery")
        if not discovery:
            raise WorkflowError(
                f"workflow {workflow['id']} declares no 'document_discovery', "
                f"so it cannot list the documents it can run"
            )
        drops = discovery["id_drops_leading"]
        marker = discovery.get("marker")
        found: set[str] = set()
        for path in self.repo_root.glob(discovery["search"]):
            if not path.is_dir():
                continue
            if marker and not (path / marker).is_file():
                continue
            parts = path.relative_to(self.repo_root).parts
            if len(parts) > drops:
                found.add("/".join(parts[drops:]))
        return sorted(found)

    def resolve_document(self, workflow: dict[str, Any], token: str) -> str:
        """Accept a full document id, or an unambiguous shorthand for one.

        Strictly additive: anything that names a path is passed through
        untouched, so a token that worked before still works and a workflow
        that declares no discovery is unaffected. Only a bare token — the sort
        a person types from memory — is resolved, and only when exactly one
        document matches it.
        """
        if "/" in token or not workflow.get("document_discovery"):
            return token
        documents = self.list_documents(workflow)
        argument = workflow.get("document_argument", "document")
        for candidates in (
            [d for d in documents if d.rsplit("/", 1)[-1] == token],
            [d for d in documents if d.endswith("/" + token)],
            [d for d in documents if token in d],
        ):
            if len(candidates) == 1:
                return candidates[0]
            if len(candidates) > 1:
                raise WorkflowError(
                    f"{argument} {token!r} matches {len(candidates)} "
                    f"documents:\n  " + "\n  ".join(candidates) +
                    f"\nName one of them, or enough of its tail to be unique."
                )
        raise WorkflowError(
            self._unresolved_document(workflow, token, documents, argument)
        )

    @staticmethod
    def _unresolved_document(
        workflow: dict[str, Any], token: str, documents: list[str],
        argument: str,
    ) -> str:
        """Say what a bare token could have meant, and what it could not.

        A shorthand resolves against what exists, and a document that does not
        exist yet is exactly what `seed` is often reached for. Refusing a
        token without saying so sent a reader looking for a typo in a name
        that was simply new.
        """
        lines = [f"no {argument} matches {token!r}"]
        near = _nearest_document(token, documents)
        if near:
            lines.append("")
            lines.append(f"  did you mean:  {near}")
        parents = sorted({document.rsplit("/", 1)[0]
                          for document in documents if "/" in document})
        if parents:
            lines.append("")
            lines.append(
                f"  a {argument} that does not exist yet is named in full, so "
                f"seed it as one of:"
            )
            lines.extend(f"    {parent}/{token}" for parent in parents)
        lines.append("")
        lines.append(
            f"  every {argument} that does exist: "
            f"tools/tpt {workflow['id']} list"
        )
        return "\n".join(lines)

    def schema_name_for(self, stage: dict[str, Any]) -> str:
        """The result schema a stage's result is validated against."""
        if stage["type"] == GATE:
            return stage.get("result_schema", SCHEMA_GATE)
        if stage["type"] == EVALUATOR:
            return stage.get("result_schema", SCHEMA_EVALUATOR)
        return stage.get("result_schema", SCHEMA_WORKER)

    def workflow_source_digest(self, workflow: dict[str, Any]) -> str:
        """Digest every byte of guidance a run of this workflow can be driven by.

        A packet's bytes cover the fragments it quotes, but not the parts of
        the definition that decide what happens next: transitions, iteration
        limits, gate commands, schemas. A run is bound to this digest so that
        changing any of them mid-run is detected rather than silently obeyed.

        "Every fragment" means every lane fragment too. No single packet
        carries them all — a lane packet quotes its own lane's and no other's —
        which is precisely why the digest has to.
        """
        material = [
            f"recipe:{DIGEST_RECIPE}",
            "pipeline:" + json.dumps(
                workflow, sort_keys=True, separators=(",", ":")
            ),
        ]
        fragments: set[str] = set()
        schemas: set[str] = set()
        for stage in workflow["stages"]:
            fragments.update(stage.get("fragments", []))
            # A lane's own fragments are guidance a run is driven by exactly as
            # much as the stage's are, and for a fan-out stage they are most of
            # it. The pipeline JSON above covers their *names*; only this covers
            # their bytes.
            for lane in _stage_lanes(stage):
                fragments.update(lane.get("fragments", []))
            schemas.add(self.schema_name_for(stage))
        for name in sorted(fragments):
            material.append(f"fragment:{name}:{_lf(self.load_fragment(name))}")
        for name in sorted(schemas):
            path = self.schemas_dir / name
            if not path.is_file():
                raise WorkflowError(f"unknown schema: {name}")
            material.append(
                f"schema:{name}:{_lf(path.read_text(encoding='utf-8'))}"
            )
        return hashlib.sha256("\n".join(material).encode("utf-8")).hexdigest()

    def load_bound_workflow(self, state: dict[str, Any]) -> dict[str, Any]:
        """Load the workflow a run was seeded against, or fail closed.

        A run advances under the workflow source it started with. If the
        definition, a fragment, or a schema has changed since, the run cannot
        continue: it would claim continuity with a deterministic sequence it
        is no longer following.
        """
        workflow = self.load_workflow(state["workflow_id"])
        recorded = state.get("workflow_digest")
        if not recorded:
            raise WorkflowError(
                f"run {state['run_id']}: state records no workflow digest; "
                f"the run predates workflow-source binding and cannot advance"
            )
        if workflow["version"] != state["workflow_version"]:
            raise WorkflowError(
                f"run {state['run_id']} was seeded against "
                f"{state['workflow_id']} v{state['workflow_version']}; "
                f"the workflow on disk is v{workflow['version']}. "
                f"Seed a new run against the new version."
            )
        current = self.workflow_source_digest(workflow)
        if current != recorded:
            raise WorkflowError(
                f"workflow source changed since run {state['run_id']} was "
                f"seeded (recorded {recorded[:16]}, on disk {current[:16]}). "
                f"A run is bound to the pipeline, fragment, and schema bytes "
                f"it started with. Restore them, or seed a new run."
            )
        return workflow

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
        """Create or verify a run and return its original bootstrap."""
        response = json.loads(self.seed_bytes(workflow_id, raw_args))
        # Internal callers historically use this convenience path. It is not
        # persisted or emitted by the CLI because an absolute checkout path is
        # outside the deterministic bootstrap contract.
        response["packet_abs_path"] = str(
            self.repo_root / response["packet_path"]
        )
        return response

    def _validate_document_argument(
        self, workflow: dict[str, Any], args: dict[str, str],
    ) -> None:
        """Refuse a document the workflow's own registry does not know.

        Discovery answers which documents exist as authored leaves; a workflow
        that can start a document not yet authored needs a separate authority
        for whether the identity is real. `document_discovery.validator` names
        it, and a non-zero exit fails the seed closed.
        """
        discovery = workflow.get("document_discovery") or {}
        template = discovery.get("validator")
        doc_arg = workflow.get("document_argument")
        if not template or not doc_arg or doc_arg not in args:
            return
        # Shell-quoted for the same reason a gate command is: the document id
        # is data, never a place to continue the command from.
        command = _substitute_args(template, args, quote=True)
        try:
            proc = subprocess.run(
                command, shell=True, capture_output=True, text=True,
                cwd=self.repo_root, timeout=300,
            )
        except subprocess.TimeoutExpired:
            raise WorkflowError(
                f"document validator timed out: {command}"
            ) from None
        if proc.returncode != 0:
            detail = (proc.stderr or proc.stdout or "").strip()
            raise WorkflowError(
                f"{workflow['id']}: {args[doc_arg]!r} is not a document this "
                f"workflow may run"
                + (f": {detail}" if detail else "")
            )

    def seed_bytes(self, workflow_id: str,
                   raw_args: dict[str, str]) -> bytes:
        """Create a run or replay its verified canonical bootstrap bytes."""
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
        existing = self._existing_seed_bytes(
            run_dir, workflow, commit, args, creation_may_be_active=True
        )
        if existing is not None:
            return existing

        # A new run is where an identity is refused. The scope ledger is
        # written by the stage after this one, so an identity that no registry
        # knows has to fail before a run exists to write it: refusing at the
        # gate two stages later would already have let a worker record an
        # authorization for a proper that does not exist.
        self._validate_document_argument(workflow, args)

        # An atomic per-run creation lock makes simultaneous identical seeds
        # converge on one creator. Established runs never take this lock: their
        # replay path is wholly read-only.
        lock_fd = self._acquire_seed_lock(run_id)
        try:
            existing = self._existing_seed_bytes(
                run_dir, workflow, commit, args
            )
            if existing is not None:
                return existing
            return self._create_seed_bytes(
                run_id, run_dir, workflow, commit, args
            )
        finally:
            try:
                fcntl.flock(lock_fd, fcntl.LOCK_UN)
            finally:
                os.close(lock_fd)

    def _existing_seed_bytes(
        self, run_dir: Path, workflow: dict[str, Any], commit: str,
        args: dict[str, str], creation_may_be_active: bool = False,
    ) -> bytes | None:
        """Return a verified bootstrap for a published run, if one exists."""
        if run_dir.is_symlink():
            raise WorkflowError(
                f"run {run_dir.name}: run directory is a symlink and cannot "
                f"be trusted"
            )
        if not run_dir.exists():
            return None
        if not run_dir.is_dir():
            raise WorkflowError(
                f"run {run_dir.name}: run path is not a directory"
            )
        state_path = run_dir / "state.json"
        manifest_path = run_dir / "manifest.json"
        if state_path.is_symlink() or manifest_path.is_symlink():
            raise WorkflowError(
                f"run {run_dir.name}: state or manifest is a symlink and "
                f"cannot be trusted"
            )
        if not state_path.is_file():
            if creation_may_be_active:
                return None
            raise WorkflowError(
                f"run {run_dir.name}: state.json is missing; the run "
                f"directory is incomplete and cannot be repaired by seed"
            )
        state = self.load_state(run_dir.name)
        return self._load_verified_bootstrap(workflow, commit, args, state)

    def _acquire_seed_lock(self, run_id: str) -> int:
        """Serialize creation of one deterministic run across processes."""
        lock_dir = self.repo_root / "build" / "tpt-seed-locks"
        if lock_dir.is_symlink():
            raise WorkflowError("seed lock directory is a symlink")
        try:
            lock_dir.mkdir(parents=True, exist_ok=True)
        except OSError as error:
            raise WorkflowError(
                f"cannot create the seed lock directory: {error}"
            ) from error
        lock_path = lock_dir / f"{run_id}.lock"
        flags = os.O_RDWR | os.O_CREAT
        flags |= getattr(os, "O_NOFOLLOW", 0)
        try:
            fd = os.open(lock_path, flags, 0o600)
            fcntl.flock(fd, fcntl.LOCK_EX)
            return fd
        except OSError as error:
            if "fd" in locals():
                os.close(fd)
            raise WorkflowError(
                f"run {run_id}: cannot acquire seed lock: {error}"
            ) from error

    @staticmethod
    def _initial_seed_state(
        run_id: str, workflow: dict[str, Any], digest: str, commit: str,
        args: dict[str, str],
    ) -> dict[str, Any]:
        """The pristine state against which the first packet is compiled."""
        return {
            "run_id": run_id,
            "workflow_id": workflow["id"],
            "workflow_version": workflow["version"],
            "workflow_digest": digest,
            "repo_commit": commit,
            "normalized_args": args,
            "current_stage": workflow["stages"][0]["id"],
            "iteration": 0,
            "stage_iterations": {},
            "stage_failures": {},
            "stage_repeats": {},
            "stage_blocking_ids": {},
            "findings_forwarded_by": {},
            "findings_forwarded_ids": {},
            "unrepaired_for": {},
            "unrepaired_notes": {},
            # Resolved once, from values the run id already covers. Held in
            # state so that reading it never needs the workflow: `status` is
            # the one command that must keep working after the workflow on
            # disk has moved past the version this run is bound to, which is
            # exactly when an operator reaches for it.
            "document_root": _document_root(workflow, args),
            "escalations": [],
            "packet_hashes": [],
            "result_hashes": [],
            "transitions": [],
            "disposition": None,
        }

    def _create_seed_bytes(
        self, run_id: str, run_dir: Path, workflow: dict[str, Any],
        commit: str, args: dict[str, str],
    ) -> bytes:
        """Prepare and publish a new run, with state.json written last."""
        claimed = False
        try:
            if self.runs_dir.is_symlink():
                raise WorkflowError("the tpt runs directory is a symlink")
            self.runs_dir.mkdir(parents=True, exist_ok=True)
            run_dir.mkdir()
            claimed = True
            for subdir in ("packets", "results", "artifacts", "interventions"):
                (run_dir / subdir).mkdir()

            digest = self.workflow_source_digest(workflow)
            first_stage = workflow["stages"][0]["id"]
            state = self._initial_seed_state(
                run_id, workflow, digest, commit, args
            )
            stage = self._get_stage(workflow, first_stage)
            packet = self._compile_stage_packets(
                workflow, stage, state, run_dir, [], []
            )
            # Digesting and compilation read the same sources through separate
            # paths. Refuse a source edit that overlaps initial compilation.
            if self.workflow_source_digest(workflow) != digest:
                raise WorkflowError(
                    f"workflow source changed while run {run_id} was seeded; "
                    f"no run was published"
                )
            self._stage_packet(state, packet)
            bootstrap = self._bootstrap_response(
                workflow, commit, args, state, packet
            )
            bootstrap_bytes = _canonical_json_bytes(bootstrap)
            manifest = {
                "run_id": run_id,
                "workflow_id": workflow["id"],
                "workflow_version": workflow["version"],
                "workflow_digest": digest,
                "repo_commit": commit,
                "normalized_args": args,
                "created_at": _utc_timestamp(),
                "bootstrap": {
                    "version": 1,
                    "path": "bootstrap.json",
                    "sha256": hashlib.sha256(bootstrap_bytes).hexdigest(),
                },
            }
            seed_event = {
                "event": "seed",
                "workflow_id": workflow["id"],
                "workflow_version": workflow["version"],
                "stage": first_stage,
                "timestamp": _utc_timestamp(),
            }
            packet_event = {
                "event": "packet",
                "stage": packet["stage"],
                "iteration": packet["iteration"],
                "hash": packet["hash"],
                "size": packet["size"],
                "timestamp": _utc_timestamp(),
            }
            events = (
                json.dumps(seed_event, sort_keys=True, ensure_ascii=False)
                + "\n"
                + json.dumps(packet_event, sort_keys=True, ensure_ascii=False)
                + "\n"
            ).encode("utf-8")

            self._write_new_file(
                run_id, run_dir / "manifest.json",
                _canonical_json_bytes(manifest),
            )
            for path, payload in self._packet_writes(packet) + [
                (run_dir / "bootstrap.json", bootstrap_bytes),
                (run_dir / "events.jsonl", events),
            ]:
                self._write_new_file(run_id, path, payload)
            self.save_state(run_id, state)
            return bootstrap_bytes
        except OSError as error:
            raise WorkflowError(
                f"cannot create the run directory for {run_id}: {error}"
            ) from error
        finally:
            # Before state.json exists this invocation owns only an unpublished
            # directory. Remove it so a clean retry can create the run. Once
            # state exists, seed must never repair or rewrite the evidence.
            if claimed and not (run_dir / "state.json").exists():
                shutil.rmtree(run_dir, ignore_errors=True)

    def _write_new_file(self, run_id: str, path: Path, payload: bytes) -> None:
        """Create one seed artifact without following or replacing a path."""
        flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL
        flags |= getattr(os, "O_NOFOLLOW", 0)
        try:
            fd = os.open(path, flags, 0o666)
            with os.fdopen(fd, "wb") as stream:
                stream.write(payload)
        except OSError as error:
            raise WorkflowError(
                f"run {run_id}: cannot write {path.name}: {error}"
            ) from error

    def _bootstrap_response(
        self, workflow: dict[str, Any], commit: str, args: dict[str, str],
        state: dict[str, Any], packet: dict[str, Any],
    ) -> dict[str, Any]:
        """Build the portable, canonical original bootstrap response."""
        stage = self._get_stage(workflow, packet["stage"])
        return {
            "bootstrap_version": 1,
            "run_id": state["run_id"],
            "workflow_id": workflow["id"],
            "workflow_version": workflow["version"],
            "workflow_digest": state["workflow_digest"],
            "repo_commit": commit,
            "normalized_args": args,
            "stage": packet["stage"],
            "iteration": packet["iteration"],
            "packet_hash": packet["hash"],
            "packet_path": packet["path"].relative_to(
                self.repo_root
            ).as_posix(),
            "instructions": self._driver_instructions(
                workflow, stage, state, packet, portable_path=True
            ),
        }

    def _load_verified_bootstrap(
        self, workflow: dict[str, Any], commit: str, args: dict[str, str],
        state: dict[str, Any],
    ) -> bytes:
        """Verify immutable bootstrap and initial-packet evidence once."""
        run_id = state["run_id"]
        expected_identity = {
            "workflow_id": workflow["id"],
            "workflow_version": workflow["version"],
            "repo_commit": commit,
            "normalized_args": args,
        }
        for key, expected in expected_identity.items():
            if state.get(key) != expected:
                raise WorkflowError(
                    f"run {run_id}: seed invocation disagrees with the "
                    f"immutable run identity on {key}"
                )
        bound = self.load_bound_workflow(state)
        self._verify_seed_replay_state(bound, state)
        run_dir = self.run_dir(run_id)
        manifest_path = run_dir / "manifest.json"
        if manifest_path.is_symlink():
            raise WorkflowError(
                f"run {run_id}: manifest.json is a symlink and cannot be "
                f"trusted"
            )
        manifest = _read_json(manifest_path)
        binding = manifest.get("bootstrap")
        if binding is None:
            raise WorkflowError(
                f"run {run_id} predates replayable bootstrap evidence; use "
                f"status, replay, or advance, or deliberately discard the "
                f"old run before seeding again"
            )
        if not isinstance(binding, dict) \
                or set(binding) != {"version", "path", "sha256"} \
                or type(binding.get("version")) is not int \
                or binding["version"] != 1 \
                or binding.get("path") != "bootstrap.json" \
                or not _is_sha256(binding.get("sha256")):
            raise WorkflowError(
                f"run {run_id}: manifest has invalid bootstrap evidence"
            )
        path = run_dir / "bootstrap.json"
        if path.is_symlink() or not path.is_file():
            raise WorkflowError(
                f"run {run_id}: bootstrap.json is missing or not a regular "
                f"file; seed cannot reconstruct it"
            )
        try:
            payload = path.read_bytes()
        except OSError as error:
            raise WorkflowError(
                f"run {run_id}: cannot read bootstrap.json: {error}"
            ) from error
        if hashlib.sha256(payload).hexdigest() != binding["sha256"]:
            raise WorkflowError(
                f"run {run_id}: bootstrap.json disagrees with its immutable "
                f"manifest hash"
            )

        records = state.get("packet_hashes")
        if not isinstance(records, list) or not records:
            raise WorkflowError(
                f"run {run_id}: state records no initial packet"
            )
        initial = records[0]
        first_stage = bound["stages"][0]["id"]
        expected_path = (
            run_dir / "packets" / f"{first_stage}-0000.txt"
        ).relative_to(self.repo_root).as_posix()
        if not isinstance(initial, dict) or initial.get("stage") != first_stage \
                or initial.get("iteration") != 0 \
                or initial.get("path") != expected_path \
                or not isinstance(initial.get("hash"), str):
            raise WorkflowError(
                f"run {run_id}: initial packet evidence is invalid"
            )
        packet_path = self.repo_root / expected_path
        if packet_path.is_symlink() or not packet_path.is_file():
            raise WorkflowError(
                f"run {run_id}: initial packet is missing or not a regular "
                f"file"
            )
        try:
            packet_bytes = packet_path.read_bytes()
        except OSError as error:
            raise WorkflowError(
                f"run {run_id}: cannot read the initial packet: {error}"
            ) from error
        if hashlib.sha256(packet_bytes).hexdigest() != initial["hash"]:
            raise WorkflowError(
                f"run {run_id}: initial packet disagrees with its recorded "
                f"hash"
            )
        pristine = self._initial_seed_state(
            run_id, bound, state["workflow_digest"], commit, args
        )
        compiled = self._compile_stage_packets(
            bound, self._get_stage(bound, first_stage), pristine,
            run_dir, [], iteration=0,
        )
        if compiled["path"] != packet_path \
                or compiled["hash"] != initial["hash"] \
                or compiled["bytes"] != packet_bytes:
            raise WorkflowError(
                f"run {run_id}: initial packet does not match the bound "
                f"workflow and pristine seed state"
            )
        self._verify_lane_packet_evidence(run_id, compiled, initial)
        packet = {
            "path": packet_path,
            "stage": initial["stage"],
            "iteration": initial["iteration"],
            "hash": initial["hash"],
            "lanes": [
                {
                    "lane": lane["lane"],
                    "index": lane["index"],
                    "hash": lane["hash"],
                    "path": self.repo_root / lane["path"],
                }
                for lane in initial.get("lanes", [])
            ],
        }
        expected = _canonical_json_bytes(self._bootstrap_response(
            bound, commit, args, state, packet
        ))
        if payload != expected:
            raise WorkflowError(
                f"run {run_id}: bootstrap.json is not the canonical response "
                f"for the immutable run evidence"
            )
        return payload

    def _verify_recorded_lane_files(
        self, run_id: str, record: dict[str, Any], directory: Path,
        stem: str, suffix: str,
    ) -> None:
        """Every recorded lane file must be present, named, and unaltered."""
        lanes = record.get("lanes")
        if lanes is None:
            return
        if not isinstance(lanes, list) or not lanes:
            raise WorkflowError(
                f"run {run_id}: {record.get('stage')} records an invalid lane "
                f"roster"
            )
        for index, lane in enumerate(lanes):
            if not isinstance(lane, dict) or lane.get("index") != index \
                    or not isinstance(lane.get("lane"), str) \
                    or not _is_sha256(lane.get("hash")):
                raise WorkflowError(
                    f"run {run_id}: {record.get('stage')} lane evidence is "
                    f"inconsistent"
                )
            expected = (
                directory / f"{stem}-lane-{index:02d}-{lane['lane']}{suffix}"
            ).relative_to(self.repo_root).as_posix()
            if lane.get("path") != expected:
                raise WorkflowError(
                    f"run {run_id}: {record.get('stage')} lane evidence has an "
                    f"invalid path"
                )
            path = self.repo_root / expected
            if path.is_symlink() or not path.is_file():
                raise WorkflowError(
                    f"run {run_id}: recorded lane file is missing or symlinked"
                )
            try:
                actual = hashlib.sha256(path.read_bytes()).hexdigest()
            except OSError as error:
                raise WorkflowError(
                    f"run {run_id}: cannot read recorded lane file: {error}"
                ) from error
            if actual != lane["hash"]:
                raise WorkflowError(
                    f"run {run_id}: recorded lane file hash is inconsistent"
                )

    def _verify_lane_packet_evidence(
        self, run_id: str, compiled: dict[str, Any], record: dict[str, Any]
    ) -> None:
        """A recorded lane roster must match what the workflow compiles now.

        Lane identity is what a lane result is bound to, so a lane roster that
        the bound workflow no longer produces — a lane renamed, reordered,
        added, or dropped under a live run — has to be an error rather than a
        run whose results answer packets nobody can recompile.
        """
        recorded = record.get("lanes", [])
        expected = compiled.get("lanes", [])
        if not isinstance(recorded, list) or len(recorded) != len(expected):
            raise WorkflowError(
                f"run {run_id}: recorded lane roster for {record['stage']} "
                f"disagrees with the bound workflow"
            )
        for index, (entry, lane) in enumerate(zip(recorded, expected)):
            relative = str(lane["path"].relative_to(self.repo_root))
            if not isinstance(entry, dict) \
                    or entry.get("lane") != lane["lane"] \
                    or entry.get("index") != index \
                    or entry.get("hash") != lane["hash"] \
                    or entry.get("path") != relative:
                raise WorkflowError(
                    f"run {run_id}: recorded lane evidence for "
                    f"{record['stage']} lane {index} is inconsistent"
                )
            path = self.repo_root / relative
            if path.is_symlink() or not path.is_file():
                raise WorkflowError(
                    f"run {run_id}: lane packet {relative} is missing or "
                    f"symlinked"
                )
            if path.read_bytes() != lane["bytes"]:
                raise WorkflowError(
                    f"run {run_id}: lane packet {relative} does not match the "
                    f"bound workflow and recorded state"
                )

    def _verify_seed_replay_state(
        self, workflow: dict[str, Any], state: dict[str, Any]
    ) -> None:
        """Reject structurally or historically inconsistent progressed state."""
        run_id = state["run_id"]
        stages = {stage["id"]: stage for stage in workflow["stages"]}
        stage_ids = set(stages)
        allowed_stages = stage_ids | {ACCEPTED, BLOCKED}
        packets = state.get("packet_hashes")
        results = state.get("result_hashes")
        transitions = state.get("transitions")
        stage_iterations = state.get("stage_iterations")
        stage_failures = state.get("stage_failures")
        if not isinstance(packets, list) or not packets \
                or not isinstance(results, list) \
                or not isinstance(transitions, list) \
                or not isinstance(stage_iterations, dict) \
                or not isinstance(stage_failures, dict):
            raise WorkflowError(
                f"run {run_id}: state history has an invalid structure"
            )
        if type(state.get("iteration")) is not int \
                or state["iteration"] != len(packets):
            raise WorkflowError(
                f"run {run_id}: state iteration disagrees with packet history"
            )
        if len(results) != len(transitions):
            raise WorkflowError(
                f"run {run_id}: result and transition histories disagree"
            )

        run_dir = self.run_dir(run_id)
        packets_dir = run_dir / "packets"
        results_dir = run_dir / "results"
        if packets_dir.is_symlink() or results_dir.is_symlink():
            raise WorkflowError(
                f"run {run_id}: packet or result directory is a symlink"
            )
        counts: dict[str, int] = {}
        for record in packets:
            if not isinstance(record, dict):
                raise WorkflowError(
                    f"run {run_id}: packet history contains a non-object"
                )
            stage = record.get("stage")
            iteration = record.get("iteration")
            if stage not in stage_ids or type(iteration) is not int \
                    or iteration != counts.get(stage, 0) \
                    or not _is_sha256(record.get("hash")):
                raise WorkflowError(
                    f"run {run_id}: packet history is inconsistent"
                )
            expected_path = (
                packets_dir / f"{stage}-{iteration:04d}.txt"
            ).relative_to(self.repo_root).as_posix()
            if record.get("path") != expected_path:
                raise WorkflowError(
                    f"run {run_id}: packet history has an invalid path"
                )
            path = self.repo_root / expected_path
            if path.is_symlink() or not path.is_file():
                raise WorkflowError(
                    f"run {run_id}: recorded packet is missing or symlinked"
                )
            try:
                actual = hashlib.sha256(path.read_bytes()).hexdigest()
            except OSError as error:
                raise WorkflowError(
                    f"run {run_id}: cannot read recorded packet: {error}"
                ) from error
            if actual != record["hash"]:
                raise WorkflowError(
                    f"run {run_id}: recorded packet hash is inconsistent"
                )
            self._verify_recorded_lane_files(
                run_id, record, packets_dir, f"{stage}-{iteration:04d}", ".txt"
            )
            counts[stage] = iteration + 1
        if stage_iterations != counts:
            raise WorkflowError(
                f"run {run_id}: stage iteration counts disagree with packets"
            )
        for stage, count in stage_failures.items():
            if stage not in stage_ids or type(count) is not int or count < 0:
                raise WorkflowError(
                    f"run {run_id}: stage failure counts are inconsistent"
                )

        # The budget is replayed through the engine's own function rather than
        # recomputed here. Two implementations of one rule are two rules, and
        # this one only has to agree with the other forever.
        audit_state: dict[str, Any] = {
            "stage_failures": {}, "stage_repeats": {},
            "stage_blocking_ids": {},
            "findings_forwarded_by": {}, "findings_forwarded_ids": {},
            "unrepaired_for": {}, "unrepaired_notes": {}, "escalations": [],
        }
        for index, (result, transition) in enumerate(zip(results, transitions)):
            packet = packets[index]
            if not isinstance(result, dict) or not isinstance(transition, dict) \
                    or result.get("stage") != packet["stage"] \
                    or result.get("iteration") != packet["iteration"] \
                    or transition.get("from") != packet["stage"] \
                    or transition.get("to") not in allowed_stages \
                    or not _is_sha256(result.get("hash")):
                raise WorkflowError(
                    f"run {run_id}: result or transition history is inconsistent"
                )
            expected_path = (
                results_dir
                / f"{packet['stage']}-{packet['iteration']:04d}.json"
            ).relative_to(self.repo_root).as_posix()
            if result.get("path") != expected_path:
                raise WorkflowError(
                    f"run {run_id}: result history has an invalid path"
                )
            path = self.repo_root / expected_path
            if path.is_symlink() or not path.is_file():
                raise WorkflowError(
                    f"run {run_id}: recorded result is missing or symlinked"
                )
            try:
                actual = hashlib.sha256(path.read_bytes()).hexdigest()
            except OSError as error:
                raise WorkflowError(
                    f"run {run_id}: cannot read recorded result: {error}"
                ) from error
            if actual != result["hash"]:
                raise WorkflowError(
                    f"run {run_id}: recorded result hash is inconsistent"
                )
            self._verify_recorded_lane_files(
                run_id, result, results_dir,
                f"{packet['stage']}-{packet['iteration']:04d}", ".json",
            )
            body = _read_json(path)
            stage = stages[packet["stage"]]
            _validate_result(
                body, self.load_schema(self.schema_name_for(stage)),
                stage["type"],
            )
            self._record_escalations(
                audit_state, stage, body, packet["iteration"]
            )
            disposition = body.get("disposition")
            if body.get("stage") != packet["stage"] \
                    or body.get("iteration") != packet["iteration"] \
                    or result.get("disposition") != disposition \
                    or transition.get("disposition") != disposition:
                raise WorkflowError(
                    f"run {run_id}: result metadata disagrees with its "
                    f"recorded JSON"
                )
            if stage["type"] in (LINEAR, BOUNDED_REVISION):
                if disposition == PASS:
                    # Replayed for the same reason the live path runs it: the
                    # repeat budget below is charged from what a reviser
                    # reported, so an audit that skipped the report would
                    # re-derive different counters and refuse a sound run.
                    self._record_repair_outcomes(audit_state, stage, body)
                expected_target = (
                    stage["next"] if disposition == PASS else BLOCKED
                )
            elif stage["type"] == EVALUATOR:
                if disposition == PASS:
                    self._clear_failures(audit_state, stage)
                    expected_target = stage["pass_transition"]
                elif disposition == CHANGES_REQUIRED:
                    route = _repair_route(stage, body)
                    expected_target = (
                        BLOCKED
                        if self._failure_budget_spent(audit_state, stage, body)
                        else (route["transition"] if route is not None
                              else stage["fail_transition"])
                    )
                else:
                    expected_target = BLOCKED
            else:
                if disposition == PASS:
                    self._clear_failures(audit_state, stage)
                    expected_target = stage["pass_transition"]
                else:
                    expected_target = (
                        BLOCKED
                        if self._failure_budget_spent(audit_state, stage, body)
                        else stage["fail_transition"]
                    )
            target = transition["to"]
            if target != expected_target:
                raise WorkflowError(
                    f"run {run_id}: transition target disagrees with its "
                    f"recorded result"
                )
            # The same forwarding record the live path keeps, so the next
            # revision result replayed here is charged to the same owner.
            audit_prior = self._extract_prior_findings(body, stage)
            audit_blocking = [
                str(f.get("id", "(unidentified)")) for f in audit_prior
                if f.get("severity") == "blocking"
            ]
            if audit_blocking:
                audit_state.setdefault(
                    "findings_forwarded_by", {}
                )[target] = stage["id"]
                audit_state.setdefault(
                    "findings_forwarded_ids", {}
                )[target] = sorted(set(audit_blocking))
            else:
                audit_state.setdefault(
                    "findings_forwarded_by", {}
                ).pop(target, None)
                audit_state.setdefault(
                    "findings_forwarded_ids", {}
                ).pop(target, None)
            if target not in (ACCEPTED, BLOCKED):
                if index + 1 >= len(packets) \
                        or packets[index + 1]["stage"] != target:
                    raise WorkflowError(
                        f"run {run_id}: transition does not lead to its packet"
                    )
            elif index != len(transitions) - 1:
                raise WorkflowError(
                    f"run {run_id}: terminal transition is not last"
                )
        if stage_failures != audit_state["stage_failures"]:
            raise WorkflowError(
                f"run {run_id}: stage failure counts disagree with results"
            )
        if state.get("stage_repeats", {}) != audit_state["stage_repeats"]:
            raise WorkflowError(
                f"run {run_id}: stage repeat counts disagree with results"
            )
        # An escalation is the one thing a run produces that outlives it, so
        # the ledger has to be what the results actually said rather than
        # whatever the state file now holds.
        if state.get("escalations", []) != audit_state["escalations"]:
            raise WorkflowError(
                f"run {run_id}: the escalation ledger disagrees with results"
            )

        first_stage = workflow["stages"][0]["id"]
        if packets[0]["stage"] != first_stage:
            raise WorkflowError(
                f"run {run_id}: packet history does not start at {first_stage}"
            )
        expected_current = transitions[-1]["to"] if transitions else first_stage
        if state.get("current_stage") != expected_current:
            raise WorkflowError(
                f"run {run_id}: current stage disagrees with transition history"
            )
        terminal = expected_current in (ACCEPTED, BLOCKED)
        if state.get("disposition") != (expected_current if terminal else None):
            raise WorkflowError(
                f"run {run_id}: disposition disagrees with current stage"
            )
        expected_packets = len(transitions) if terminal else len(transitions) + 1
        if len(packets) != expected_packets:
            raise WorkflowError(
                f"run {run_id}: packet count disagrees with transition history"
            )

    def advance(self, run_id: str, result_path: str | None = None,
                run_gate: bool = False,
                lane_results: list[tuple[str, str]] | None = None,
                ) -> dict[str, Any]:
        """Validate a result and emit the next packet (or terminal state).

        For `single` linear/evaluator/bounded-revision stages: requires
        --result <path>. For `fanout` stages: requires one --lane-result per
        workflow-defined lane, and the engine performs the join itself.
        For gate stages: requires --run-gate (runs the gate checks directly).

        The whole successor is prepared before any of it is persisted: the
        result is validated, the transition determined, and the successor
        packet compiled against a copy of the state. Only then are the result,
        the packet, and the new state committed, state last. So a submission
        the engine refuses leaves no authoritative trace, and a run that could
        not be given its next packet stays at the stage it can still be driven
        from.
        """
        state = self.load_state(run_id)
        if state["disposition"] is not None:
            raise WorkflowError(
                f"run {run_id} has reached terminal state: "
                f"{state['disposition']}"
            )
        workflow = self.load_bound_workflow(state)
        stage = self._get_stage(workflow, state["current_stage"])

        lanes = _stage_lanes(stage)
        lane_bodies: list[tuple[dict[str, Any], dict[str, Any]]] = []
        if stage["type"] == GATE:
            if not run_gate:
                raise WorkflowError(
                    f"stage {stage['id']} is a gate; use --run-gate"
                )
            if result_path is not None:
                raise WorkflowError(
                    f"stage {stage['id']} is a gate; do not pass --result"
                )
            if lane_results:
                raise WorkflowError(
                    f"stage {stage['id']} is a gate; it has no lanes and takes "
                    f"no --lane-result"
                )
            result = self._run_gate(workflow, stage, state, run_id)
        elif lanes:
            if run_gate:
                raise WorkflowError(
                    f"stage {stage['id']} is not a gate; pass one "
                    f"--lane-result <lane-id>=<path> per declared lane"
                )
            if result_path is not None:
                raise WorkflowError(
                    f"stage {stage['id']} is a {FANOUT} stage; pass one "
                    f"--lane-result <lane-id>=<path> per declared lane, not "
                    f"--result. The engine joins the lane results itself."
                )
            lane_bodies = self._load_and_validate_lane_results(
                lane_results or [], stage, state
            )
            result = self._join_lane_results(stage, state, lane_bodies)
        else:
            if run_gate:
                raise WorkflowError(
                    f"stage {stage['id']} is not a gate; pass --result <path>"
                )
            if lane_results:
                raise WorkflowError(
                    f"stage {stage['id']} is a {SINGLE} stage; it declares no "
                    f"lanes and takes --result <path>, not --lane-result"
                )
            if result_path is None:
                raise WorkflowError(
                    f"stage {stage['id']} requires --result <path>"
                )
            result = self._load_and_validate_result(result_path, stage, state)

        # Everything below builds a candidate successor against a copy of the
        # state. Nothing durable changes until it is complete.
        pending = copy.deepcopy(state)
        transition, block_reason = self._determine_transition(
            workflow, stage, result, pending
        )
        if transition == ACCEPTED:
            self._verify_final_acceptance(workflow, stage, state)

        result_write = self._prepare_result(pending, result, stage)
        lane_writes = self._prepare_lane_results(pending, stage, lane_bodies)

        if transition in (ACCEPTED, BLOCKED):
            pending["disposition"] = transition
            pending["current_stage"] = transition
            # A terminal move is recorded like any other: the transition list is
            # the run's own account of how it got where it is, and the move that
            # ended it is the one an auditor asks about first.
            pending["transitions"].append({
                "from": stage["id"],
                "to": transition,
                "disposition": result["disposition"],
            })
            # Before the commit, not after. This write is outside the run's
            # transaction either way, and raising after the commit reported
            # failure on a run that had already advanced: the packet was on
            # disk and the state named the next stage, so the obvious retry
            # then failed on a stage mismatch. Failing first leaves nothing
            # recorded and a retry that works.
            #
            # The terminal transition is the case the record exists for: a run
            # that blocks is a run whose findings have nowhere else to go.
            # Writing only on transitions that continue left the last
            # evaluation -- the one that spent the budget -- unrecorded.
            self._record_standing_findings(workflow, pending, stage, result)
            self._commit(run_id, pending, [result_write] + lane_writes)
            self._emit_result_event(run_id, stage, result, transition)
            if transition == ACCEPTED:
                self._emit_event(run_id, {
                    "event": "accepted",
                    "timestamp": _utc_timestamp(),
                })
                return {
                    "run_id": run_id,
                    "disposition": ACCEPTED,
                    "stage": ACCEPTED,
                    "escalations": pending.get("escalations", []),
                    "message": "Workflow complete. All stages passed."
                    + _escalation_note(pending),
                }
            self._emit_event(run_id, {
                "event": "blocked",
                "reason": block_reason or "evaluator returned BLOCKED",
                "timestamp": _utc_timestamp(),
            })
            return {
                "run_id": run_id,
                "disposition": BLOCKED,
                "stage": BLOCKED,
                "escalations": pending.get("escalations", []),
                "message": (block_reason or
                            "Workflow blocked. Evaluator returned BLOCKED.")
                + _escalation_note(pending),
            }

        # Transition to the next stage: compile its packet first, so a run is
        # never recorded at a stage whose guidance could not be produced.
        next_stage = self._get_stage(workflow, transition)
        pending["current_stage"] = transition
        pending["transitions"].append({
            "from": stage["id"],
            "to": transition,
            "disposition": result["disposition"],
        })
        prior_findings = self._extract_prior_findings(result, stage)
        # Remember who owns the findings this transition hands on, so that the
        # receiving stage's repair report can be charged back to the stage that
        # raised them. Without this the reviser's account of what it could not
        # fix would have nowhere to land, and the budget would be back to
        # guessing from ids.
        blocking_forwarded = [
            str(f.get("id", "(unidentified)")) for f in prior_findings
            if f.get("severity") == "blocking"
        ]
        forwarded_by = pending.setdefault("findings_forwarded_by", {})
        forwarded_ids = pending.setdefault("findings_forwarded_ids", {})
        if blocking_forwarded:
            forwarded_by[transition] = stage["id"]
            forwarded_ids[transition] = sorted(set(blocking_forwarded))
        else:
            forwarded_by.pop(transition, None)
            forwarded_ids.pop(transition, None)
        carried_findings = self._carried_findings(
            run_id, workflow, pending, next_stage, prior_findings, fresh=result
        )
        packet = self._compile_stage_packets(
            workflow, next_stage, pending, self.run_dir(run_id),
            prior_findings, carried_findings,
        )
        self._stage_packet(pending, packet)
        # The packet is written before the result that produced it, so that a
        # commit which cannot store the successor leaves no record of the
        # submission either.
        self._record_standing_findings(workflow, pending, stage, result)
        self._commit(
            run_id, pending,
            self._packet_writes(packet) + [result_write] + lane_writes,
        )

        self._emit_result_event(run_id, stage, result, transition)
        self._emit_packet_event(run_id, packet)

        return {
            "run_id": run_id,
            "stage": transition,
            "iteration": packet["iteration"],
            "packet_hash": packet["hash"],
            "packet_path": str(packet["path"].relative_to(self.repo_root)),
            "packet_abs_path": str(packet["path"]),
            "disposition": None,
            "instructions": self._driver_instructions(
                workflow, next_stage, pending, packet
            ),
        }

    # --- Status and inspection ---

    def status(self, run_id: str) -> dict[str, Any]:
        """Return the current run status.

        A result has to name the packet it answers, so the status of a running
        run states that packet rather than only the global counter: an operator
        reading `iteration` here and writing it into a result would otherwise
        name a packet that does not exist.
        """
        state = self.load_state(run_id)
        packets = state["packet_hashes"]
        packet = packets[-1] if packets else None
        return {
            "run_id": run_id,
            "workflow_id": state["workflow_id"],
            "workflow_version": state["workflow_version"],
            "workflow_digest": state["workflow_digest"],
            "repo_commit": state["repo_commit"],
            "current_stage": state["current_stage"],
            "disposition": state["disposition"],
            "awaiting_result_for": (
                None if state["disposition"] is not None or packet is None
                else {"stage": packet["stage"], "iteration": packet["iteration"]}
            ),
            "packet_path": packet["path"] if packet else None,
            "packet_hash": packet["hash"] if packet else None,
            "iteration": state["iteration"],
            "stage_iterations": state["stage_iterations"],
            "stage_failures": state["stage_failures"],
            "stage_repeats": state.get("stage_repeats", {}),
            "escalations": state.get("escalations", []),
            # What the tracked record says stands against this document. Read
            # here and nowhere else: it reaches no packet, so an operator can
            # see it without a run depending on it.
            "standing_findings": [
                finding.get("id") for finding in _standing_findings(
                    self.standing_findings_root,
                    state.get("document_root"),
                )
            ],
            "packets_emitted": len(state["packet_hashes"]),
            "results_received": len(state["result_hashes"]),
            "transitions": state["transitions"],
        }

    def replay(self, run_id: str) -> dict[str, Any]:
        """Recompile the current packet from persisted state and compare hashes.

        Nothing is written: a replay that rewrote the packet it is checking
        would destroy the artifact whose bytes are in question.
        """
        state = self.load_state(run_id)
        last_pkt = state["packet_hashes"][-1] if state["packet_hashes"] else None
        report: dict[str, Any] = {
            "run_id": run_id,
            "stage": state["current_stage"],
            "last_recorded_hash": last_pkt["hash"] if last_pkt else None,
        }
        if last_pkt:
            recorded_file = self.repo_root / last_pkt["path"]
            report["recorded_file_intact"] = (
                recorded_file.is_file()
                and hashlib.sha256(recorded_file.read_bytes()).hexdigest()
                == last_pkt["hash"]
            )
        if state["disposition"] is not None:
            # A terminal run has no current packet to recompile.
            report.update({
                "disposition": state["disposition"],
                "recompiled_hash": None,
                "deterministic": None,
            })
            return report
        workflow = self.load_bound_workflow(state)
        stage = self._get_stage(workflow, state["current_stage"])
        prior_findings, carried_findings = \
            self._load_prior_findings_for_current(run_id, state, workflow)
        # stage_iterations was incremented after the last packet was compiled,
        # so recompile at the iteration that packet used.
        iteration = (
            last_pkt["iteration"]
            if last_pkt and last_pkt["stage"] == state["current_stage"]
            else state["stage_iterations"].get(state["current_stage"], 0)
        )
        packet = self._compile_stage_packets(
            workflow, stage, state, self.run_dir(run_id), prior_findings,
            carried_findings, iteration=iteration,
        )
        deterministic = (
            packet["hash"] == last_pkt["hash"] if last_pkt else True
        )
        lanes = []
        if packet.get("lanes"):
            recorded = {
                entry["lane"]: entry
                for entry in (last_pkt or {}).get("lanes", [])
            }
            for lane in packet["lanes"]:
                was = recorded.get(lane["lane"], {}).get("hash")
                matched = was is None or was == lane["hash"]
                deterministic = deterministic and matched
                lanes.append({
                    "lane": lane["lane"],
                    "index": lane["lane_index"],
                    "last_recorded_hash": was,
                    "recompiled_hash": lane["hash"],
                    "deterministic": matched,
                })
        report.update({
            "disposition": None,
            "recompiled_hash": packet["hash"],
            "deterministic": deterministic,
            "lanes": lanes,
        })
        return report

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

    def verify_document(self, run_id: str, doc_id: str) -> None:
        """Reject a command that names a different document than the run holds.

        The run id alone identifies a run, so a mistyped or stale document id
        used to pass unnoticed while the command acted on whatever run the id
        pointed at.
        """
        state = self.load_state(run_id)
        workflow = self.load_workflow(state["workflow_id"])
        doc_arg = workflow.get("document_argument")
        if not doc_arg:
            return
        actual = state["normalized_args"].get(doc_arg, "")
        if doc_id != actual:
            raise WorkflowError(
                f"run {run_id} is for {doc_arg} {actual!r}, not {doc_id!r}"
            )

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
        """Load the mutable state for a run, verified against its manifest.

        The manifest is written once and never rewritten. Checking the mutable
        state against it turns a hand-edited, half-written, or relocated run
        into an error instead of a run that quietly claims to be something
        else.
        """
        run_dir = self.run_dir(run_id)
        path = run_dir / "state.json"
        if not path.is_file():
            raise WorkflowError(f"no such run: {run_id}")
        state = _read_json(path)
        manifest_path = run_dir / "manifest.json"
        if not manifest_path.is_file():
            raise WorkflowError(
                f"run {run_id}: manifest.json is missing; the run directory is "
                f"incomplete and cannot be trusted"
            )
        manifest = _read_json(manifest_path)
        for key in ("run_id", "workflow_id", "workflow_version",
                    "workflow_digest", "repo_commit", "normalized_args"):
            if key not in manifest:
                raise WorkflowError(
                    f"run {run_id}: manifest.json is missing {key}"
                )
            if state.get(key) != manifest[key]:
                raise WorkflowError(
                    f"run {run_id}: state.json disagrees with the immutable "
                    f"manifest on {key} "
                    f"(state {state.get(key)!r}, manifest {manifest[key]!r})"
                )
        if manifest["run_id"] != run_id:
            raise WorkflowError(
                f"run {run_id}: manifest names run {manifest['run_id']}; the "
                f"run directory has been renamed or copied"
            )
        expected = self.compute_run_id(
            manifest["workflow_id"], manifest["workflow_version"],
            manifest["repo_commit"], manifest["normalized_args"],
        )
        if expected != run_id:
            raise WorkflowError(
                f"run {run_id}: manifest inputs hash to {expected}; the "
                f"manifest has been edited"
            )
        return state

    def save_state(self, run_id: str, state: dict[str, Any]) -> None:
        """Save the mutable state for a run, replacing it atomically."""
        path = self.run_dir(run_id) / "state.json"
        tmp = path.with_suffix(".tmp")
        try:
            path.parent.mkdir(parents=True, exist_ok=True)
            tmp.write_text(
                json.dumps(state, sort_keys=True, indent=2) + "\n",
                encoding="utf-8",
            )
            tmp.replace(path)
        except OSError as error:
            tmp.unlink(missing_ok=True)
            raise WorkflowError(
                f"run {run_id}: cannot save state: {error}"
            ) from error

    def _commit(
        self, run_id: str, state: dict[str, Any],
        writes: list[tuple[Path, bytes]],
    ) -> None:
        """Make a prepared transition durable, the state last.

        Every file the new state refers to is written before the state that
        refers to it, and state.json is replaced atomically. A commit that
        fails part way therefore leaves the previous authoritative state and
        some orphaned files under the run directory: nothing points at them,
        and the retry rewrites them byte for byte.
        """
        for path, payload in writes:
            try:
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_bytes(payload)
            except OSError as error:
                raise WorkflowError(
                    f"run {run_id}: cannot write {path.name}: {error}"
                ) from error
        self.save_state(run_id, state)

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
        carried_findings: list[dict[str, Any]] | None = None,
        iteration: int | None = None,
        lane: dict[str, Any] | None = None,
        lane_index: int | None = None,
    ) -> dict[str, Any]:
        """Deterministically compile a guidance packet, writing nothing.

        The caller decides when the bytes become durable, so that compiling a
        packet cannot itself advance a run, and replay can recompile the
        packet it is checking without destroying it.

        The packet bytes are assembled from:
        - A deterministic header (workflow, workflow-source digest, run id,
          commit, stage, iteration, execution policy, lane identity, args,
          prior findings)
        - Fragment contents in the declared order, with argument placeholders
          substituted

        With `lane`, this compiles that lane's own packet: the header names the
        lane and its canonical index, and the lane's own fragments follow the
        stage's. Lane identity comes from the workflow, so the same run state
        yields the same lane packets, byte for byte, however the lanes are
        scheduled. No worker process id, launch or completion timestamp,
        scheduler slot, or completion order reaches these bytes.

        No timestamps appear in the hashed bytes. Two things that look like
        exceptions are not: `DOCUMENT_ROOT` is a repository-relative path built
        from the workflow's own template and the normalized arguments, both
        already hashed, so it is a restatement of them and not a machine fact;
        and the run id does too, for the reason below. Nothing
        machine-specific — no absolute path, no scheduler state — reaches
        them. The run id: it is the engine's own hash of workflow, version, seed
        commit and normalized arguments, every one of which the header already
        carries, so it is a restatement of those bytes and not a new input, and
        the same run state still yields the same packet byte for byte. It is
        here because a worker that must record what produced the document it is
        writing cannot record the run it is part of unless the packet says
        which run that is; the packet is the whole instruction, and before this
        the four fields the header did carry were readable while the fifth was
        not. The hash is SHA-256 of the exact UTF-8 encoded packet text.
        """
        stage_iteration = (
            state["stage_iterations"].get(stage["id"], 0)
            if iteration is None else iteration
        )
        args = state["normalized_args"]

        # Build header
        header_lines = [
            f"WORKFLOW: {workflow['id']} v{workflow['version']}",
            f"WORKFLOW_DIGEST: {state['workflow_digest']}",
            f"RUN_ID: {state['run_id']}",
            f"COMMIT: {state['repo_commit']}",
            f"STAGE: {stage['id']}",
            f"ITERATION: {stage_iteration}",
            f"EXECUTION: {_execution_label(stage)}",
        ]

        effort = _stage_effort(workflow, stage, lane)
        if effort:
            header_lines.append(f"EFFORT: {effort}")

        lanes = _stage_lanes(stage)
        if lanes:
            header_lines.append(
                "LANES: " + json.dumps(
                    [entry["id"] for entry in lanes],
                    sort_keys=True, separators=(",", ":"),
                )
            )
        if lane is not None:
            header_lines.append(f"LANE: {lane['id']}")
            header_lines.append(f"LANE_INDEX: {lane_index}")

        header_lines.append(
            f"ARGS: {json.dumps(args, sort_keys=True, separators=(',', ':'))}"
        )

        # The resolved path of the thing under work, when the workflow declares
        # how to build it. `ARGS` carries the arguments and a worker is left to
        # assemble the path from them, which is one inference too many where a
        # leaf of the same name exists under more than one provider: a lane of
        # this pipeline swept `src/gpt/...` to completion, caught it only from
        # an unrelated `git status`, and discarded a finished max-effort sweep.
        # The arguments already decide the answer, so the engine states it.
        document_root = _document_root(workflow, args)
        if document_root:
            header_lines.append(f"DOCUMENT_ROOT: {document_root}")

        # The repair owners this stage's own schema admits. A shared fragment
        # names all three that exist, and a pipeline may admit fewer:
        # `proper-finish` begins after research and owns only `authoring`, so a
        # lane following the shared fragment and naming `brief` had its finding
        # refused -- and on a fan-out stage one refused finding fails the whole
        # five-lane submission. The packet states what this run will accept
        # rather than leaving a worker to infer it from a route table it cannot
        # see.
        admitted = (
            self.load_schema(self.schema_name_for(stage))
            .get("finding_enums", {})
            .get(REPAIR_TARGET)
        )
        if admitted:
            header_lines.append(
                "REPAIR_TARGETS: " + json.dumps(
                    list(admitted), separators=(",", ":")
                )
            )

        if prior_findings:
            header_lines.append(
                f"PRIOR_FINDINGS: {json.dumps(prior_findings, sort_keys=True, separators=(',', ':'))}"
            )
        else:
            header_lines.append("PRIOR_FINDINGS: []")

        # Two fields, because they are two different things and a worker acts
        # on them differently. PRIOR_FINDINGS came from the transition that
        # produced this packet. CARRIED_FINDINGS were raised earlier against
        # work this stage owns and never reached it, because another owner won
        # the route; they stand until this stage's own output is evaluated
        # again. Merging them into one list would tell a worker that everything
        # it is reading was just said, and that is not true.
        header_lines.append(
            "CARRIED_FINDINGS: " + json.dumps(
                carried_findings or [], sort_keys=True, separators=(",", ":")
            )
        )

        header = _FIELD_SEP.join(header_lines)

        # Load fragments in declared order. Argument placeholders are
        # substituted here so that no worker has to infer what {proper} or
        # {provider} meant; the packet is the whole instruction.
        fragment_paths = list(stage.get("fragments", []))
        if lane is not None:
            fragment_paths += list(lane.get("fragments", []))
        body = ""
        for frag_path in fragment_paths:
            content = _substitute_args(self.load_fragment(frag_path), args)
            body += f"{_PACKET_SEP}{frag_path} ---\n{content}"
        if not fragment_paths:
            body = (
                "\n(gate stage: run by tpt with --run-gate; no AI worker)"
                if stage["type"] == GATE
                else "\n(no fragments for this stage)"
            )

        packet_text = header + _HEADER_SEP + body

        # Ensure consistent line endings (LF)
        packet_text = packet_text.replace("\r\n", "\n").replace("\r", "\n")

        # Encode
        packet_bytes = packet_text.encode("utf-8")

        # Hash
        packet_hash = hashlib.sha256(packet_bytes).hexdigest()

        name = f"{stage['id']}-{stage_iteration:04d}"
        if lane is not None:
            name += f"-lane-{lane_index:02d}-{lane['id']}"
        path = run_dir / "packets" / f"{name}.txt"

        compiled = {
            "hash": packet_hash,
            "bytes": packet_bytes,
            "path": path,
            "stage": stage["id"],
            "iteration": stage_iteration,
            "size": len(packet_bytes),
        }
        if lane is not None:
            compiled["lane"] = lane["id"]
            compiled["lane_index"] = lane_index
        return compiled

    def _compile_stage_packets(
        self,
        workflow: dict[str, Any],
        stage: dict[str, Any],
        state: dict[str, Any],
        run_dir: Path,
        prior_findings: list[dict[str, Any]],
        carried_findings: list[dict[str, Any]] | None = None,
        iteration: int | None = None,
    ) -> dict[str, Any]:
        """Compile a stage's packet and, for a fan-out stage, its lane packets.

        The parent packet is the stage's own record — the one the run's state,
        replay, and result binding key on. A fan-out stage additionally gets
        one packet per workflow-defined lane, compiled here in canonical lane
        order so that lane ids, lane ordering, lane packet bytes, and lane
        hashes are all fixed before any agent is launched.
        """
        packet = self._compile_packet(
            workflow, stage, state, run_dir, prior_findings, carried_findings,
            iteration=iteration,
        )
        packet["lanes"] = [
            self._compile_packet(
                workflow, stage, state, run_dir, prior_findings,
                carried_findings,
                iteration=packet["iteration"], lane=lane, lane_index=index,
            )
            for index, lane in enumerate(_stage_lanes(stage))
        ]
        return packet

    def _packet_writes(self, packet: dict[str, Any]) -> list[tuple[Path, bytes]]:
        """The packet files a transition must store, parent first."""
        return [(packet["path"], packet["bytes"])] + [
            (lane["path"], lane["bytes"]) for lane in packet.get("lanes", [])
        ]

    def _stage_packet(
        self, state: dict[str, Any], packet: dict[str, Any]
    ) -> None:
        """Record a compiled packet in a state dict, persisting nothing."""
        record = {
            "stage": packet["stage"],
            "iteration": packet["iteration"],
            "hash": packet["hash"],
            "path": str(packet["path"].relative_to(self.repo_root)),
        }
        if packet.get("lanes"):
            record["lanes"] = [
                {
                    "lane": lane["lane"],
                    "index": lane["lane_index"],
                    "hash": lane["hash"],
                    "path": str(lane["path"].relative_to(self.repo_root)),
                }
                for lane in packet["lanes"]
            ]
        state["packet_hashes"].append(record)
        # Increment global iteration
        state["iteration"] += 1
        # Increment stage iteration
        stage_id = packet["stage"]
        state["stage_iterations"][stage_id] = (
            state["stage_iterations"].get(stage_id, 0) + 1
        )

    def _emit_packet_event(self, run_id: str, packet: dict[str, Any]) -> None:
        self._emit_event(run_id, {
            "event": "packet",
            "stage": packet["stage"],
            "iteration": packet["iteration"],
            "hash": packet["hash"],
            "size": packet["size"],
            "timestamp": _utc_timestamp(),
        })

    def _emit_result_event(
        self, run_id: str, stage: dict[str, Any],
        result: dict[str, Any], transition: str,
    ) -> None:
        self._emit_event(run_id, {
            "event": "result",
            "stage": stage["id"],
            "disposition": result["disposition"],
            "transition": transition,
            "timestamp": _utc_timestamp(),
        })

    # --- Internal: result handling ---

    def _load_and_validate_result(
        self,
        result_path: str,
        stage: dict[str, Any],
        state: dict[str, Any],
    ) -> dict[str, Any]:
        """Load a submitted result and check it, writing nothing.

        A submission is checked before any of it is kept: an unreadable file,
        malformed JSON, a shape the stage's schema refuses, and a result naming
        another packet all fail here, with the run untouched. Only a result the
        engine has accepted is ever written into the run's history, so a
        refused one cannot become the stage's result, alter a recorded hash, or
        reach a later replay.
        """
        result = self._read_result_file(result_path)
        schema = self.load_schema(self.schema_name_for(stage))
        _validate_result(result, schema, stage["type"])
        self._verify_result_answers_packet(result, stage, state)
        return result

    def _verify_result_answers_packet(
        self, result: dict[str, Any], stage: dict[str, Any],
        state: dict[str, Any],
    ) -> None:
        """A result must name the packet it answers.

        Without this the engine cannot tell a fresh result from the previous
        one resubmitted, from a result produced for a different stage, or from
        one written before the run advanced. Each of those would let a driver
        move the run without any worker doing the stage's work.
        """
        packet = _current_packet(state, stage["id"])
        declared_stage = result.get("stage")
        declared_iteration = result.get("iteration")
        if declared_stage != stage["id"]:
            raise WorkflowError(
                f"result declares stage {declared_stage!r}; the run is waiting "
                f"for stage {stage['id']!r} iteration {packet['iteration']}"
            )
        if declared_iteration != packet["iteration"]:
            raise WorkflowError(
                f"result declares iteration {declared_iteration!r} of stage "
                f"{stage['id']}; the emitted packet is iteration "
                f"{packet['iteration']}. A result must answer the packet the "
                f"engine last emitted."
            )

    def _load_and_validate_lane_results(
        self,
        submissions: list[tuple[str, str]],
        stage: dict[str, Any],
        state: dict[str, Any],
    ) -> list[tuple[dict[str, Any], dict[str, Any]]]:
        """Load one result per workflow-defined lane, writing nothing.

        Fail-closed in every direction the host could otherwise decide: an
        undeclared lane, a second result for a lane already answered, a result
        whose body names another lane than the flag that carried it, a result
        naming a lane packet hash the run did not emit, and a missing required
        lane are all refused here, with the run untouched. The controller does
        not get to judge whether a missing lane was good enough.

        The returned list is in canonical lane order, never submission order.
        """
        lanes = _stage_lanes(stage)
        declared = {lane["id"]: lane for lane in lanes}
        packet = _current_packet(state, stage["id"])
        emitted = {
            entry["lane"]: entry for entry in packet.get("lanes", [])
        }
        schema = self.load_schema(self.schema_name_for(stage))
        seen: dict[str, dict[str, Any]] = {}

        for lane_id, path_text in submissions:
            if lane_id not in declared:
                raise WorkflowError(
                    f"stage {stage['id']} declares no lane {lane_id!r}; its "
                    f"lanes are: {', '.join(sorted(declared))}. A host may "
                    f"not add a lane the workflow did not define."
                )
            if lane_id in seen:
                raise WorkflowError(
                    f"lane {lane_id} of stage {stage['id']} was submitted "
                    f"more than once"
                )
            body = self._read_result_file(path_text)
            _validate_result(body, schema, stage["type"])
            self._verify_result_answers_packet(body, stage, state)
            if body.get("lane") != lane_id:
                raise WorkflowError(
                    f"result submitted for lane {lane_id!r} declares lane "
                    f"{body.get('lane')!r}; a lane result must name its own "
                    f"lane"
                )
            expected = emitted[lane_id]["hash"]
            if body.get("lane_packet_hash") != expected:
                raise WorkflowError(
                    f"lane {lane_id} of stage {stage['id']} declares packet "
                    f"hash {body.get('lane_packet_hash')!r}; the emitted lane "
                    f"packet is {expected}. A lane result must answer the lane "
                    f"packet the engine emitted."
                )
            seen[lane_id] = body

        missing = [lane["id"] for lane in lanes if lane["id"] not in seen]
        if missing:
            raise WorkflowError(
                f"stage {stage['id']} cannot complete: no result for lane(s) "
                f"{', '.join(missing)}. Every workflow-defined lane is "
                f"required."
            )
        return [(lane, seen[lane["id"]]) for lane in lanes]

    def _join_lane_results(
        self,
        stage: dict[str, Any],
        state: dict[str, Any],
        ordered: list[tuple[dict[str, Any], dict[str, Any]]],
    ) -> dict[str, Any]:
        """The strict-union join: tpt's own reduction over the lane results.

        The parent controller is never asked to summarize several lane results
        into the next prompt, because a summary is guidance and guidance is the
        engine's. Each lane's structured findings are preserved verbatim under
        its lane identity, in canonical lane order, and the disposition is the
        worst any lane returned. Nothing here reads completion order, so lanes
        finishing C, A, D, B join exactly as A, B, C, D.
        """
        packet = _current_packet(state, stage["id"])
        emitted = {entry["lane"]: entry for entry in packet.get("lanes", [])}
        findings: list[dict[str, Any]] = []
        observations: list[dict[str, Any]] = []
        records: list[dict[str, Any]] = []
        parts: list[str] = []
        worst = PASS

        for index, (lane, body) in enumerate(ordered):
            disposition = body.get("disposition", "")
            if _DISPOSITION_RANK.get(disposition, 0) > \
                    _DISPOSITION_RANK.get(worst, 0):
                worst = disposition
            parts.append(f"{lane['id']}={disposition}")
            for finding in body.get("findings", []) or []:
                tagged = dict(finding)
                tagged["lane"] = lane["id"]
                findings.append(tagged)
            for observation in body.get("observations", []) or []:
                noted = dict(observation)
                noted["lane"] = lane["id"]
                observations.append(noted)
            records.append({
                "lane": lane["id"],
                "index": index,
                "disposition": disposition,
                "packet_hash": emitted[lane["id"]]["hash"],
                "result_hash": hashlib.sha256(
                    _result_bytes(body)
                ).hexdigest(),
            })

        return {
            "stage": stage["id"],
            "iteration": packet["iteration"],
            "disposition": worst,
            "summary": (
                f"{STRICT_UNION} join of {len(ordered)} workflow-defined "
                f"lanes: " + ", ".join(parts)
            ),
            "findings": findings,
            "observations": observations,
            "lanes": records,
        }

    def _prepare_lane_results(
        self,
        state: dict[str, Any],
        stage: dict[str, Any],
        ordered: list[tuple[dict[str, Any], dict[str, Any]]],
    ) -> list[tuple[Path, bytes]]:
        """Record each lane result under its lane identity; return its file.

        Keyed by lane, never by arrival: the file name and the state record
        both carry the lane id and its canonical index, so an auditor can read
        which lane produced which bytes without knowing when it finished.
        """
        if not ordered:
            return []
        stage_iter = _current_packet(state, stage["id"])["iteration"]
        run_dir = self.run_dir(state["run_id"])
        writes: list[tuple[Path, bytes]] = []
        records: list[dict[str, Any]] = []
        for index, (lane, body) in enumerate(ordered):
            dest = (
                run_dir / "results"
                / f"{stage['id']}-{stage_iter:04d}"
                  f"-lane-{index:02d}-{lane['id']}.json"
            )
            payload = _result_bytes(body)
            writes.append((dest, payload))
            records.append({
                "lane": lane["id"],
                "index": index,
                "hash": hashlib.sha256(payload).hexdigest(),
                "path": str(dest.relative_to(self.repo_root)),
                "disposition": body.get("disposition", ""),
            })
        state["result_hashes"][-1]["lanes"] = records
        return writes

    def _read_result_file(self, result_path: str) -> dict[str, Any]:
        """Read one submitted result file as a JSON object, or fail closed."""
        path = Path(result_path)
        if not path.is_file():
            raise WorkflowError(f"result file not found: {result_path}")
        try:
            body = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as error:
            raise WorkflowError(
                f"result is not valid JSON: {error}"
            ) from error
        except OSError as error:
            raise WorkflowError(
                f"result cannot be read: {error}"
            ) from error
        if not isinstance(body, dict):
            raise WorkflowError(
                f"result must be a JSON object, not {type(body).__name__}"
            )
        return body

    def _prepare_result(
        self, state: dict[str, Any],
        result: dict[str, Any], stage: dict[str, Any],
    ) -> tuple[Path, bytes]:
        """Record an accepted result in a state dict; return the file to write.

        The bytes recorded and the bytes hashed are the same bytes, and they
        are the result as submitted: nothing the engine derives afterwards is
        folded back into the run's copy of what a worker returned.
        """
        stage_iter = _current_packet(state, stage["id"])["iteration"]
        dest = (self.run_dir(state["run_id"]) / "results"
                / f"{stage['id']}-{stage_iter:04d}.json")
        payload = _result_bytes(result)
        state["result_hashes"].append({
            "stage": stage["id"],
            "iteration": stage_iter,
            "hash": hashlib.sha256(payload).hexdigest(),
            "path": str(dest.relative_to(self.repo_root)),
            "disposition": result.get("disposition", ""),
        })
        self._record_escalations(state, stage, result, stage_iter)
        return dest, payload

    @staticmethod
    def _record_escalations(
        state: dict[str, Any], stage: dict[str, Any],
        result: dict[str, Any], stage_iter: int,
    ) -> None:
        """Carry an unrepairable defect out of the run instead of losing it.

        An evaluator that finds a contradiction in repository guidance has
        nowhere to send it: no stage of this workflow may write `guidance/`,
        and neither blocking nor advisory is true of it. Blocking would end a
        run whose document is correct; advisory is where it went, and it was
        restated in every iteration of one real run and acted on in none,
        because nothing outlives the run to act on.

        So the run keeps a ledger. Escalations are held by `(stage, id)`, the
        latest restatement of each replacing the one before it — a lane that
        re-reports the same defect every iteration has not found a new one —
        and sorted, so the ledger is a function of what was found and not of
        when. It survives into `status`, into the terminal message, and into
        the state file an operator reads afterwards.
        """
        raised = [finding for finding in result.get("findings", []) or []
                  if finding.get("severity") == ESCALATION]
        if not raised:
            return
        ledger = {
            (entry["stage"], entry["finding"]["id"]): entry
            for entry in state.setdefault("escalations", [])
        }
        for finding in raised:
            key = (stage["id"], str(finding.get("id", "(unidentified)")))
            ledger[key] = {
                "stage": stage["id"],
                "iteration": stage_iter,
                "escalated_to": finding.get("escalated_to", ""),
                "finding": finding,
            }
        state["escalations"] = [ledger[key] for key in sorted(ledger)]

    # --- Internal: transitions ---

    def _determine_transition(
        self,
        workflow: dict[str, Any],
        stage: dict[str, Any],
        result: dict[str, Any],
        state: dict[str, Any],
    ) -> tuple[str, str | None]:
        """The next stage id, and the reason if that next state is BLOCKED.

        The reason is returned rather than written into the result: the result
        is the record of what a worker submitted, and the engine's account of
        why a run stopped is not part of it.

        Only the failure counters in the state passed here are mutated, and
        that state is the caller's uncommitted copy.
        """
        disposition = result.get("disposition", "")

        if stage["type"] in (LINEAR, BOUNDED_REVISION):
            if disposition == BLOCKED:
                return BLOCKED, (
                    f"worker at stage {stage['id']} returned BLOCKED: "
                    f"{result.get('summary', '(no summary)')}"
                )
            if disposition != PASS:
                kind = "linear" if stage["type"] == LINEAR else "revision"
                raise WorkflowError(
                    f"{kind} stage {stage['id']} requires disposition PASS or "
                    f"BLOCKED, got {disposition}"
                )
            self._record_repair_outcomes(state, stage, result)
            return stage["next"], None

        if stage["type"] == EVALUATOR:
            if disposition == PASS:
                # A PASS carrying a blocking finding passes the transition and
                # then fails the acceptance audit, at the one place the run
                # cannot be repaired from: no revision path re-enters an
                # upstream evaluator, so the run wedges rather than blocking.
                # Refuse it here, while the run is still drivable.
                standing = sorted(
                    str(finding.get("id", "(unidentified)"))
                    for finding in result.get("findings", []) or []
                    if finding.get("severity") == "blocking"
                )
                if standing:
                    raise WorkflowError(
                        f"evaluator {stage['id']} returned {PASS} while its "
                        f"own findings still stand as blocking: "
                        f"{', '.join(standing)}. Resolve them, or return "
                        f"{CHANGES_REQUIRED}."
                    )
                self._clear_failures(state, stage)
                return stage["pass_transition"], None
            if disposition == CHANGES_REQUIRED:
                if not any(
                    finding.get("severity") == "blocking"
                    for finding in result.get("findings", []) or []
                ):
                    raise WorkflowError(
                        f"evaluator {stage['id']} returned "
                        f"{CHANGES_REQUIRED} with no blocking finding; asking "
                        f"for a change while naming none spends an iteration "
                        f"dispatching a worker with nothing to read, and on a "
                        f"stage that routes by owner it names no owner either"
                    )
                spent = self._failure_budget_spent(state, stage, result)
                if spent:
                    return BLOCKED, spent
                route = _repair_route(stage, result)
                if route is not None:
                    return route["transition"], None
                return stage["fail_transition"], None
            if disposition == BLOCKED:
                return BLOCKED, None
            raise WorkflowError(
                f"evaluator {stage['id']} returned invalid disposition: "
                f"{disposition}"
            )

        if stage["type"] == GATE:
            if disposition == PASS:
                self._clear_failures(state, stage)
                return stage["pass_transition"], None
            if disposition == FAIL:
                spent = self._failure_budget_spent(state, stage, result)
                if spent:
                    return BLOCKED, spent
                return stage["fail_transition"], None
            raise WorkflowError(
                f"gate {stage['id']} returned invalid disposition: {disposition}"
            )

        raise WorkflowError(f"unknown stage type: {stage['type']}")

    def _verify_final_acceptance(
        self, workflow: dict[str, Any], stage: dict[str, Any],
        state: dict[str, Any],
    ) -> None:
        """The conditions tpt checks itself before a run may become ACCEPTED.

        Acceptance is the one transition no agent may attest. A worker's PASS
        says that a stage's own work was done; whether the run as a whole may
        be accepted is a question about the run's recorded state, and tpt
        answers it from that state rather than from a summary. Judgment stays
        where judgment belongs, in the evaluator stages upstream; what is
        machine-checkable is checked here.

        A gate whose commands fail takes its `fail_transition`, which is a
        bounded revision path. Reaching acceptance with a run whose own record
        contradicts it is not repairable by revision, so it fails closed.
        """
        problems: list[str] = []
        if stage["type"] != GATE:
            problems.append(
                f"stage {stage['id']} is a {stage['type']} stage; only a "
                f"program gate may accept a run"
            )

        latest: dict[str, dict[str, Any]] = {}
        for entry in state["result_hashes"]:
            latest[entry["stage"]] = entry

        for other in workflow["stages"]:
            if other["id"] == stage["id"]:
                continue
            if other["type"] not in (EVALUATOR, GATE):
                continue
            entry = latest.get(other["id"])
            if entry is None:
                problems.append(
                    f"{other['id']} has produced no result; a required check "
                    f"has not run"
                )
            elif entry["disposition"] != PASS:
                problems.append(
                    f"{other['id']} last recorded {entry['disposition']}, "
                    f"not {PASS}"
                )

        for entry in state["result_hashes"]:
            path = self.repo_root / entry["path"]
            if not path.is_file():
                problems.append(f"recorded result {entry['path']} is missing")
                continue
            recorded = path.read_bytes()
            if hashlib.sha256(recorded).hexdigest() != entry["hash"]:
                problems.append(
                    f"recorded result {entry['path']} no longer matches its "
                    f"recorded hash"
                )
                continue
            if entry is not latest.get(entry["stage"]):
                continue
            if entry["stage"] == stage["id"]:
                # The accepting gate's last recorded result is the refusal that
                # sent the run round for revision. Its checks have just been
                # rerun and passed; that run, not the record of the earlier
                # one, is what acceptance rests on.
                continue
            body = json.loads(recorded.decode("utf-8"))
            unresolved = sorted(
                str(f.get("id", "(unidentified)"))
                for f in body.get("findings", [])
                if f.get("severity") == "blocking"
            )
            if unresolved:
                problems.append(
                    f"{entry['stage']} still reports blocking findings: "
                    f"{', '.join(unresolved)}"
                )

        for entry in state["packet_hashes"]:
            path = self.repo_root / entry["path"]
            if (not path.is_file()
                    or hashlib.sha256(path.read_bytes()).hexdigest()
                    != entry["hash"]):
                problems.append(
                    f"the packet recorded for {entry['stage']} iteration "
                    f"{entry['iteration']} is missing or altered "
                    f"({entry['path']})"
                )

        # Lane evidence is part of the run's record, so acceptance rests on it
        # too: a lane packet or lane result edited after the fact would
        # otherwise leave a joined result nothing stands behind.
        for entry in state["packet_hashes"] + state["result_hashes"]:
            for lane in entry.get("lanes", []):
                if "path" not in lane or "hash" not in lane:
                    continue
                path = self.repo_root / lane["path"]
                if (not path.is_file()
                        or hashlib.sha256(path.read_bytes()).hexdigest()
                        != lane["hash"]):
                    problems.append(
                        f"the lane evidence recorded for {entry['stage']} "
                        f"lane {lane.get('lane')} is missing or altered "
                        f"({lane['path']})"
                    )

        if problems:
            raise WorkflowError(
                f"run {state['run_id']}: final acceptance refused by "
                f"{stage['id']}:\n  " + "\n  ".join(problems)
            )

    @staticmethod
    def _clear_failures(state: dict[str, Any], stage: dict[str, Any]) -> None:
        """A stage that passes starts its next revision loop from zero.

        All three counters reset together. The standing finding ids go with
        them: after a pass, a finding raised again is new work against a
        document that satisfied this stage in between, not a repeat.
        """
        state.setdefault("stage_failures", {})[stage["id"]] = 0
        state.setdefault("stage_repeats", {})[stage["id"]] = 0
        state.setdefault("stage_blocking_ids", {}).pop(stage["id"], None)
        state.setdefault("unrepaired_for", {}).pop(stage["id"], None)
        state.setdefault("unrepaired_notes", {}).pop(stage["id"], None)

    def _record_standing_findings(
        self, workflow: dict[str, Any], state: dict[str, Any],
        stage: dict[str, Any], result: dict[str, Any],
    ) -> None:
        """Write the evaluation's standing blocking findings to a tracked file.

        Written before the run's own commit, and outside it either way. After
        was the obvious order — a run that could not store its own result has
        no business publishing a claim about the leaf — and it was wrong: a
        failure here then reported failure on a run that had already advanced,
        leaving the packet on disk and the state naming the next stage, so the
        obvious retry failed on a stage mismatch. Failing first leaves nothing
        recorded and a retry that works.

        The file is rewritten whole on every evaluation, so it always states
        what stands now rather than accumulating history. A PASS writes an
        empty list rather than deleting the file, because "this leaf was
        evaluated and nothing stands" and "nobody has looked" are different
        facts and a later production reads them differently.
        """
        if self.standing_findings_root is None:
            return
        # Declared per stage. Every evaluator wrote this path, so a
        # `web-evaluation` that wanted changes replaced the leaf's content
        # findings with findings about generated HTML, and a
        # `research-synthesis` running before the author overwrote the previous
        # production's record with brief defects. The file says "standing
        # against this document"; only the stage that evaluates the document's
        # own prose may write it.
        if not stage.get("records_standing_findings"):
            return
        document_root = state.get("document_root") or _document_root(
            workflow, state["normalized_args"]
        )
        if not document_root:
            return
        root = self.standing_findings_root.resolve()
        target = root / document_root / STANDING_FINDINGS_PATH
        # `document_root` is a template filled from command-line arguments, and
        # `provider` is free text no validator constrains. A typo made a whole
        # `src/gtp/...` tree appear in the working copy; `..` in an argument
        # put it anywhere the user could write. Nothing here may leave the root
        # or pass through a symlink, which is the rule every other path this
        # engine trusts already follows.
        try:
            resolved = target.resolve()
            resolved.relative_to(root)
        except (OSError, ValueError):
            raise WorkflowError(
                f"run {state['run_id']}: the standing findings record for "
                f"{document_root} resolves outside {root}; refusing to write "
                f"it"
            ) from None
        if any(part.is_symlink() for part in
               (target, target.parent, target.parent.parent)):
            raise WorkflowError(
                f"run {state['run_id']}: the standing findings path for "
                f"{document_root} passes through a symlink; refusing to write "
                f"it"
            )
        findings = [
            f for f in result.get("findings", []) or []
            if f.get("severity") == "blocking"
        ]
        observations = list(result.get("observations", []) or [])

        lines = [
            "# Blocking findings standing against this publication, and the",
            "# observations its evaluation lanes recorded outside their own",
            "# criteria. Written by tpt after each evaluation of this leaf and",
            "# rewritten whole, so it states what stands now.",
            "#",
            "# It exists because a run's own results live under build/, which",
            "# is ignored, which `make clean` and `wt tidy` delete without",
            "# asking, and which nothing preserves between productions.",
            "#",
            "# Nothing reads this back into a run. Carrying findings from one",
            "# production into the next wants doing where the run's identity",
            "# can cover it -- a committed record, or this file's hash in the",
            "# run id and the acceptance audit -- and until then this is a",
            "# record for people.",
            "",
            "standing_findings_schema = 1",
            'record_type = "standing-blocking-findings"',
            f"document = {_toml_string(state['normalized_args'].get('proper', ''))}",
            f"provider = {_toml_string(state['normalized_args'].get('provider', ''))}",
            f"run_id = {_toml_string(state['run_id'])}",
            f"workflow = {_toml_string(str(workflow['id']))}",
            f"workflow_version = {int(workflow['version'])}",
            f"stage = {_toml_string(stage['id'])}",
            f"iteration = {int(result.get('iteration', 0))}",
            f"disposition = {_toml_string(str(result.get('disposition', '')))}",
            f"standing = {len(findings)}",
            "",
        ]
        for finding in findings:
            lines.append("[[findings]]")
            for key in (
                "id", "lane", "severity", "location", "problem",
                "required_result", "repair_target",
            ):
                if key in finding:
                    lines.append(f"{key} = {_toml_string(str(finding[key]))}")
            lines.append("")
        for observation in observations:
            lines.append("[[observations]]")
            for key in ("lane", "location", "note"):
                if key in observation:
                    lines.append(
                        f"{key} = {_toml_string(str(observation[key]))}"
                    )
            lines.append("")

        try:
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text("\n".join(lines), encoding="utf-8")
        except (OSError, ValueError, UnicodeError) as error:
            # Reported, never guessed at. `ValueError` and `UnicodeError` are
            # here because they are reachable from a worker's own result: a
            # lone surrogate in a finding's text is valid JSON and cannot be
            # encoded, and it escaped an `OSError`-only guard as a traceback.
            raise WorkflowError(
                f"run {state['run_id']}: could not write standing findings to "
                f"{document_root}/{STANDING_FINDINGS_PATH}: {error}"
            ) from error

    @staticmethod
    def _record_repair_outcomes(
        state: dict[str, Any], stage: dict[str, Any],
        result: dict[str, Any],
    ) -> None:
        """Record what a reviser says it attempted and could not repair.

        This is the only place the engine learns whether a repair worked. The
        evaluator that raised the finding cannot tell it: re-reading a changed
        document, it sees defects, not the history of attempts on them. The
        reviser holds that fact and nothing else does, which is why the
        convergence budget in `_failure_budget_spent` reads what this writes.

        The report is charged back to the stage whose findings were routed
        here, recorded at the transition that forwarded them. A stage that
        received no blocking findings has nothing to report on and is skipped:
        a first authoring pass is not a failed repair.

        Every forwarded finding must be accounted for exactly once. A reviser
        that silently drops one is the failure this cannot afford to accept,
        because a dropped finding reads exactly like a repaired one and the
        budget would then treat an abandoned defect as progress.

        Only a stage that declares `reports_repairs` is held to this, and the
        declaration is in the pipeline because not every repairing stage can
        make the report. A fan-out `research` re-entry receives blocking
        findings and produces a result the engine composed by joining its
        lanes: no agent wrote it, and no lane can speak for the whole. Demanding
        the report there failed every research re-entry unconditionally. Where
        a stage cannot report, the repeat budget gets no signal from that route
        and `max_total_iterations` is what bounds it, which is the honest
        outcome rather than a guessed one.
        """
        if not stage.get("reports_repairs"):
            return
        owner = state.get("findings_forwarded_by", {}).get(stage["id"])
        if owner is None:
            return
        expected = set(state.get("findings_forwarded_ids", {}).get(
            stage["id"], []
        ))
        if not expected:
            return

        entries = result.get("finding_dispositions") or []
        seen: dict[str, dict[str, Any]] = {}
        for entry in entries:
            if not isinstance(entry, dict):
                continue
            fid = str(entry.get("id", ""))
            if fid in seen:
                raise WorkflowError(
                    f"stage {stage['id']} reports finding {fid} twice in "
                    f"finding_dispositions; each finding is accounted for "
                    f"exactly once"
                )
            seen[fid] = entry

        missing = sorted(expected - set(seen))
        if missing:
            raise WorkflowError(
                f"stage {stage['id']} returned {PASS} without accounting for "
                f"every finding it was given: {', '.join(missing)}. Report "
                f"each one in finding_dispositions as {REPAIRED!r} or "
                f"{NOT_REPAIRED!r}. A finding left out reads exactly like a "
                f"repaired one, and the iteration budget would score an "
                f"abandoned defect as progress."
            )
        unknown = sorted(set(seen) - expected)
        if unknown:
            raise WorkflowError(
                f"stage {stage['id']} reports on findings it was not given: "
                f"{', '.join(unknown)}"
            )

        unrepaired = sorted(
            fid for fid, entry in seen.items()
            if entry.get("outcome") == NOT_REPAIRED
        )
        state.setdefault("unrepaired_for", {})[owner] = unrepaired
        state.setdefault("unrepaired_notes", {})[owner] = {
            fid: str(seen[fid].get("note", "")) for fid in unrepaired
        }

    @staticmethod
    def _failure_budget_spent(
        state: dict[str, Any], stage: dict[str, Any],
        result: dict[str, Any],
    ) -> str | None:
        """Charge `max_iterations` for repair that was tried and failed.

        Returns the block reason once a budget is spent, otherwise None.

        Counting visits let a stage that keeps passing spend its own revision
        budget: a run that re-entered a gate three times on its way through an
        unrelated revision loop was blocked by that gate's first real failure,
        with no revision attempted. Counting failures fixed that and left a
        second confusion in place: it could not tell a loop from progress. A
        real run repaired nine of ten findings, raised different ones against a
        substantially rewritten document, and was scored exactly as if it had
        raised the same ten again.

        Charging repetition instead was the next attempt, and it read the
        repetition off finding ids. That is the version this replaces, and it
        was wrong in a way that looked exactly like a verdict on the document.
        Run `90dcdddcb6780e60` converged the whole way -- seven blocking
        findings, then eleven, then seven, each iteration clearing the set
        before it and reaching further into the leaf -- and blocked at 3/3 with
        four ids named as still unrepaired. Every one of those four named a
        different defect in a different file each iteration, and the earlier
        ones were gone from the document. It was stopped at half the
        allowance its own ceiling granted it.

        Nothing the lanes did caused that and nothing they could have done
        would have prevented it. A fan-out evaluator's lane packets carry an
        empty `PRIOR_FINDINGS` by design, and lanes are told not to read
        earlier results, so **no lane can know which ids an earlier iteration
        used**. Id collision across iterations is guaranteed by the
        architecture. An id is a handle a lane minted for its own report; it
        is not an identity for a defect, and comparing ids across iterations
        compares nothing.

        So the signal moves to the only actor that can hold it. An evaluator
        re-reading a document cannot distinguish a defect that resisted repair
        from a different defect wearing the same id. The reviser can: it was
        given the findings, it attempted them, and it knows which it could not
        clear. `finding_dispositions` on a revision result carries that per
        finding, `_record_repair_outcomes` records it against the stage whose
        findings were routed there, and this reads it back.

        Two counters, both consecutive and both cleared by a pass:

        `stage_repeats` is what `max_iterations` bounds. An iteration charges
        it when the reviser reported at least one finding it attempted and
        could not repair. Findings that were repaired, and fresh findings
        raised against a changed document, cost nothing -- that is progress,
        and progress is what the budget exists to permit. The first failure of
        a streak is charged, because it has no repair report behind it and
        because leaving it free would quietly loosen every `max_iterations` in
        every workflow by one iteration.

        Where no report exists the id comparison stays, because it is the only
        signal there is and removing it would bound such a stage by
        `max_total_iterations` alone -- silently doubling every limit an
        operator declared. Ground truth displaces the heuristic exactly where
        it exists and nowhere else. `content-revision` reports, so the stage
        this was all about no longer reads ids; a fan-out `research` re-entry
        does not, so it still does, with the same unreliability it always had.
        The way to retire the heuristic for a route is to make its repairing
        stage able to report, not to delete the only bound it has.

        A gate keeps the id comparison whatever a reviser says, and here the
        heuristic is not a heuristic. What makes an id untrustworthy is that an
        AI evaluator mints it for its own report and cannot know what an
        earlier iteration used. A gate's findings are a program's: the id is a
        check id, the same check refusing the same leaf produces it again, and
        a repeat is the tool re-running and refusing again after a repair was
        claimed. That is better evidence of a loop than the claim is of
        progress, and it is the one place where the reviser's word should not
        displace a measurement.

        `stage_failures` counts every consecutive failure and is bounded by
        `max_total_iterations`, default twice `max_iterations`. Without it a
        stage whose reviser reports total success forever never terminates,
        and an optimistic reviser is now the failure mode this has to catch.
        Twice is chosen because the repeat budget ends any stage whose repairs
        are failing, so this ceiling is reached only by a stage doing genuine
        new work every time; doubling grants that stage as many iterations
        again as the operator already declared, and no more. For
        `content-evaluation` that is six under `proper-finish`, which declares
        three, and eight under `proper`, which declares four — around nine to
        twelve hours and some fifteen to twenty million subagent tokens for one
        document, which is a real bound; three was demonstrably too few and
        unbounded is not a bound.
        """
        stage_id = stage["id"]
        standing = state.setdefault("stage_blocking_ids", {})
        previous = standing.get(stage_id)
        current = _blocking_ids(result)
        standing[stage_id] = current

        failures = state.setdefault("stage_failures", {})
        count = failures.get(stage_id, 0) + 1
        failures[stage_id] = count

        # What charges the repeat budget is a repair that was attempted and
        # reported failed, by the reviser this stage's findings were routed to.
        #
        # Where no such report exists the old comparison of finding ids is
        # still the only signal there is, and it stays. Removing it everywhere
        # was wrong in the other direction: a stage whose repairs are invisible
        # would then be bounded only by `max_total_iterations`, silently
        # doubling every limit an operator had declared. So ground truth
        # displaces the heuristic exactly where it exists, and nowhere else --
        # and for the case that prompted all this, `content-revision` reports,
        # so `content-evaluation` no longer reads ids at all.
        unrepaired_map = state.get("unrepaired_for", {})
        reported = stage_id in unrepaired_map and stage["type"] != GATE
        unrepaired = sorted(unrepaired_map.get(stage_id) or [])
        notes = state.get("unrepaired_notes", {}).get(stage_id) or {}
        repeated = sorted(set(current) & set(previous or []))
        looping = unrepaired if reported else repeated
        repeats = state.setdefault("stage_repeats", {})
        spent = repeats.get(stage_id, 0)
        if previous is None or looping:
            spent += 1
        repeats[stage_id] = spent
        # Consumed. A reviser's report charges the budget once; leaving it in
        # place would charge every later failure for one stale admission.
        state.setdefault("unrepaired_for", {}).pop(stage_id, None)
        state.setdefault("unrepaired_notes", {}).pop(stage_id, None)

        max_iter = stage.get("max_iterations", 3)
        ceiling = stage.get("max_total_iterations", 2 * max_iter)
        label = "gate " if stage["type"] == GATE else ""
        if spent >= max_iter:
            if reported and unrepaired:
                detail = "; ".join(
                    f"{fid}: {notes[fid]}" if notes.get(fid) else fid
                    for fid in unrepaired
                )
                why = (
                    f" The reviser reported these findings attempted and not "
                    f"repaired: {detail}"
                )
            elif repeated and stage["type"] == GATE:
                why = (
                    f" The same checks refused again after a repair was "
                    f"reported: {', '.join(repeated)}. These ids are the "
                    f"gate's own check ids, so this is the check re-running "
                    f"and refusing, not two workers colliding on a name"
                )
            elif repeated:
                why = (
                    f" No stage on this route reports what it repaired, so "
                    f"this counts findings raised again by id: "
                    f"{', '.join(repeated)}. An id is a handle a worker minted "
                    f"for its own report and two iterations can put different "
                    f"defects behind the same one, so read the findings "
                    f"themselves before treating this as a loop"
                )
            else:
                why = (
                    " The first failure of a stage charges the budget, and "
                    "nothing since has reported a repair"
                )
            return (
                f"iteration limit exceeded for {label}{stage_id}: "
                f"{spent}/{max_iter} failures that did not converge." + why
            )
        if count >= ceiling:
            if not repeated:
                seen = ""
            elif stage["type"] == GATE:
                seen = (
                    f" Checks refused in consecutive rounds: "
                    f"{', '.join(repeated)}."
                )
            else:
                seen = (
                    f" Finding ids seen in consecutive iterations: "
                    f"{', '.join(repeated)} -- diagnostic only, and not "
                    f"evidence of a repeat: lanes cannot know which ids an "
                    f"earlier iteration used, so an id says nothing about "
                    f"which defect wears it."
                )
            budget = (
                "no round reported a repair it could not make"
                if reported else
                "no round raised what the round before it raised"
            )
            return (
                f"iteration limit exceeded for {label}{stage_id}: "
                f"{count}/{ceiling} consecutive failures. The repeat budget "
                f"({spent}/{max_iter}) never ran out because {budget}; the "
                f"absolute ceiling stops a stage that finds something new "
                f"forever." + seen
            )
        return None

    def _extract_prior_findings(
        self,
        result: dict[str, Any],
        stage: dict[str, Any],
    ) -> list[dict[str, Any]]:
        """Extract findings to forward into the next stage's packet.

        For evaluator/gate stages that trigger a revision, the blocking
        findings are forwarded verbatim.

        For a linear fan-out stage, the joined lane findings are forwarded
        verbatim on PASS. Such a stage's findings are the whole of what it
        produced: read-only research lanes write no artifact between them, so
        the joined result exists only inside the run, and its successor is the
        only place it can go. Forwarding it is what keeps the
        integration worker's material the engine's own join rather than
        something a controller retyped. An evaluator's PASS still forwards
        nothing, because there its PASS means there was nothing to report.

        For all other transitions, no findings are forwarded.
        """
        if stage["type"] in (EVALUATOR, GATE):
            if result.get("disposition") in (CHANGES_REQUIRED, FAIL):
                findings = result.get("findings", [])
                # Forward only blocking findings, verbatim
                forwarded = [
                    f for f in findings
                    if f.get("severity") == "blocking"
                ]
                route = _repair_route(stage, result)
                if route is not None:
                    # Only the findings that chose this route travel it. A
                    # finding for another owner is not carried across the
                    # regeneration its own route would trigger; the fresh
                    # evaluation afterwards raises it again if it still holds,
                    # which is the whole reason the evaluation is fresh.
                    forwarded = [
                        f for f in forwarded
                        if f.get(REPAIR_TARGET) == route[REPAIR_TARGET]
                    ]
                return forwarded
        if stage["type"] == LINEAR and _stage_lanes(stage) \
                and result.get("disposition") == PASS:
            return list(result.get("findings", []) or [])
        return []

    def _carried_findings(
        self,
        run_id: str,
        workflow: dict[str, Any],
        state: dict[str, Any],
        stage: dict[str, Any],
        forwarded: list[dict[str, Any]],
        fresh: dict[str, Any] | None = None,
    ) -> list[dict[str, Any]]:
        """Blocking findings this stage owns that no run of it has yet seen.

        Routing decides where a run goes next. It also, before this, decided
        who never heard about the defect at all: `_extract_prior_findings`
        keeps only the findings whose target won the route, so with three
        owners a `brief` finding sent the run to `research-synthesis` and the
        seven `authoring` findings raised in the same breath reached nobody.
        The author then re-authored with an empty packet and the next
        evaluation rediscovered them, which is a five-lane evaluation and a
        third of a failure budget spent learning what the run already knew.
        That happened, in run b68cca80edb75854, at its first evaluation.

        The old defence — the downstream regenerates, so it is rediscovered,
        intended and not a loss — is true of `research`, which re-runs seven
        lanes and writes a new brief. It was never true of `brief`, where the
        only intervening stage corrects a sentence and hands the same document
        back to the same author.

        So a finding waits for its owner instead of dying at the route. This
        computes, from the recorded run alone, which findings are still
        waiting for the stage about to run:

        - only from each routed evaluator's *most recent* result, because a
          later evaluation of the same document supersedes an earlier one
          entirely;
        - only findings whose `repair_target` this stage declares in
          `repairs`;
        - never a finding the transition is already forwarding, which would
          list it twice;
        - and only while no owner of that target has run since. Delivery is
          once, to whichever owner reaches it first: `author-proper` and
          `content-revision` both write the leaf, and a finding delivered to
          the one is not owed to the other.

        Routing is untouched. This changes who hears, not where the run goes.
        """
        targets = set(stage.get(REPAIRS) or [])
        if not targets:
            return []
        results = state.get("result_hashes") or []
        if not results:
            return []
        owners: dict[str, set[str]] = {}
        for other in workflow["stages"]:
            for target in other.get(REPAIRS) or []:
                owners.setdefault(target, set()).add(other["id"])

        seen = {str(finding.get("id")) for finding in forwarded}
        carried: list[dict[str, Any]] = []
        for evaluator in workflow["stages"]:
            if not evaluator.get(REPAIR_ROUTES):
                continue
            index = None
            for position, entry in enumerate(results):
                if entry["stage"] == evaluator["id"]:
                    index = position
            if index is None:
                continue
            if results[index]["disposition"] != CHANGES_REQUIRED:
                continue
            body = (
                fresh if fresh is not None and index == len(results) - 1
                else self._read_recorded_result(
                    run_id, results[index], stage["id"]
                )
            )
            for finding in body.get("findings", []) or []:
                if finding.get("severity") != "blocking":
                    continue
                target = finding.get(REPAIR_TARGET)
                if target not in targets:
                    continue
                finding_id = str(finding.get("id"))
                if finding_id in seen:
                    continue
                answered = any(
                    entry["stage"] in owners.get(target, set())
                    for entry in results[index + 1:]
                )
                if answered:
                    continue
                seen.add(finding_id)
                carried.append(finding)
        return carried

    def _load_prior_findings_for_current(
        self, run_id: str, state: dict[str, Any], workflow: dict[str, Any]
    ) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
        """Rebuild both finding lists the current packet was compiled with.

        Whatever `_extract_prior_findings` and `_carried_findings` put in the
        packet has to be reconstructible from the record alone, or a replay of
        that packet would recompile different bytes than the run emitted. So
        this asks those same functions the same questions, about the transition
        that produced the current stage: one rule decides what is forwarded,
        and one rule reproduces it. Two rules that had to agree did not stay
        agreed.

        The carried list is derived, never consumed. Delivering a finding does
        not mark it delivered anywhere; what makes it stop being outstanding is
        its owner producing a result, which is already in the record. A store
        that emptied as packets were compiled would make every packet that read
        it unreplayable.
        """
        current = state["current_stage"]
        stage = self._get_stage(workflow, current)
        transitions = state.get("transitions") or []
        results = state.get("result_hashes") or []
        if not transitions or not results \
                or transitions[-1].get("to") != current:
            return [], []
        source = self._get_stage(workflow, transitions[-1]["from"])
        # Whether anything can be forwarded at all is decided by the stage and
        # its disposition, before the recorded result is opened. Otherwise a
        # replay of a stage that forwards nothing fails on a file it would
        # never have read, and `replay` is the tool an operator reaches for
        # when a run is already in trouble.
        if _may_forward(source, transitions[-1].get("disposition")):
            result = self._read_recorded_result(run_id, results[-1], current)
            prior = self._extract_prior_findings(result, source)
        else:
            result, prior = None, []
        carried = self._carried_findings(
            run_id, workflow, state, stage, prior, fresh=result
        )
        return prior, carried

    def _read_recorded_result(
        self, run_id: str, entry: dict[str, Any], current: str
    ) -> dict[str, Any]:
        """Read a recorded result a packet must forward from, or fail closed."""
        result_path = self.repo_root / entry["path"]
        if not result_path.is_file():
            raise WorkflowError(
                f"run {run_id}: the recorded result "
                f"{entry['path']} that triggered "
                f"{current} is missing; the findings this packet must "
                f"forward cannot be reconstructed"
            )
        recorded = result_path.read_bytes()
        if hashlib.sha256(recorded).hexdigest() != entry["hash"]:
            raise WorkflowError(
                f"run {run_id}: the recorded result {entry['path']} no "
                f"longer matches its recorded hash; it has been "
                f"replaced since the run received it"
            )
        return json.loads(recorded.decode("utf-8"))

    # --- Internal: gates ---

    def _run_gate(
        self,
        workflow: dict[str, Any],
        stage: dict[str, Any],
        state: dict[str, Any],
        run_id: str,
    ) -> dict[str, Any]:
        """Run deterministic gate checks and return a structured result.

        Only the untouched per-check logs are written here. The result itself
        is persisted with the transition it produces, like any other result.
        """
        checks = stage.get("checks", [])
        # A gate command names the run's arguments and, under the reserved
        # `run.` namespace, the run itself: a check that must hold a document
        # against the run producing it has no other way to know which run that
        # is.
        args = _gate_substitutions(workflow, state)
        findings = []
        all_passed = True
        stage_iter = _current_packet(state, stage["id"])["iteration"]
        log_dir = self.run_dir(run_id) / "gate-logs"

        for check in checks:
            check_id = check["id"]
            command_template = check["command"]
            # Arguments are shell-quoted: a document id is data, never a place
            # to continue the command from.
            command = _substitute_args(command_template, args, quote=True)
            try:
                proc = subprocess.run(
                    command,
                    shell=True,
                    capture_output=True,
                    text=True,
                    cwd=self.repo_root,
                    timeout=300,
                )
                log_dir.mkdir(parents=True, exist_ok=True)
                (log_dir / f"{stage['id']}-{stage_iter:04d}-{check_id}.log"
                 ).write_text(
                    f"$ {command}\nexit {proc.returncode}\n"
                    f"--- stdout ---\n{proc.stdout}\n"
                    f"--- stderr ---\n{proc.stderr}\n",
                    encoding="utf-8",
                )
                if proc.returncode != 0:
                    all_passed = False
                    detail = (self._portable_output(proc.stderr)
                              or self._portable_output(proc.stdout))
                    findings.append({
                        "id": f"GATE-{check_id.upper()}",
                        "severity": "blocking",
                        "check": check_id,
                        "problem": (
                            f"command exited {proc.returncode}: {detail[:500]}"
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

        return {
            "disposition": PASS if all_passed else FAIL,
            "findings": findings,
            "stage": stage["id"],
            "iteration": stage_iter,
        }

    def _portable_output(self, text: str) -> str:
        """Strip host-specific detail out of subprocess output.

        Gate findings are forwarded into the next packet, so anything a check
        prints is hashed guidance. An absolute path made the same repository
        at two locations emit two different packets for the same failure. The
        untouched output is kept under the run's gate-logs/ instead.
        """
        text = text.replace("\r\n", "\n").replace("\r", "\n")
        for actual, token in (
            (str(self.repo_root), "<repo>"),
            (str(Path.home()), "<home>"),
        ):
            if actual not in ("", "/"):
                text = text.replace(actual, token)
        return "\n".join(line.rstrip() for line in text.strip().split("\n"))

    def _driver_instructions(
        self, workflow: dict[str, Any], stage: dict[str, Any],
        state: dict[str, Any], packet: dict[str, Any],
        portable_path: bool = False,
    ) -> str:
        """The exact next command, so no driver has to choose one."""
        run_id = state["run_id"]
        packet_path = (
            packet["path"].relative_to(self.repo_root).as_posix()
            if portable_path else str(packet["path"])
        )
        doc_arg = workflow.get("document_argument")
        doc = state["normalized_args"].get(doc_arg, "<doc-id>") if doc_arg \
            else "<doc-id>"
        prefix = f"tools/tpt {workflow['id']} {shlex.quote(doc)}"
        if stage["type"] == GATE:
            return (
                f"EXECUTION POLICY: PROGRAM GATE\n"
                f"\n"
                f"This stage is run by tpt. Do not start any subagent for it.\n"
                f"\n"
                f"1. This stage is a program gate. No AI worker runs it.\n"
                f"2. Run: {prefix} advance {run_id} --run-gate\n"
                f"3. Follow the next packet tpt emits.\n"
                f"4. Stop only at ACCEPTED or BLOCKED."
            )

        effort = _stage_effort(workflow, stage)
        at_effort = f" at reasoning effort {effort}" if effort else ""
        effort_rule = (
            f"Run it at reasoning effort {effort}. That level is workflow "
            f"data, not a host choice: do not raise or lower it.\n"
            if effort else ""
        )

        lanes = packet.get("lanes") or []
        if not lanes:
            return (
                f"EXECUTION POLICY: SINGLE\n"
                f"\n"
                f"Start exactly one fresh subagent.\n"
                f"{effort_rule}"
                f"Give it exactly the packet specified below.\n"
                f"Do not launch additional agents for this stage.\n"
                f"\n"
                f"1. Start exactly one fresh subagent{at_effort}.\n"
                f"2. Give it exactly the contents of {packet_path}.\n"
                f"3. Require its structured result as JSON at a path you "
                f"choose. The result must carry \"stage\": \"{stage['id']}\" "
                f"and \"iteration\": {packet['iteration']}.\n"
                f"4. Run: {prefix} advance {run_id} --result <path>\n"
                f"5. Follow the next packet tpt emits.\n"
                f"6. Stop only at ACCEPTED or BLOCKED."
            )

        count = len(lanes)
        lane_effort = {
            entry["id"]: _stage_effort(workflow, stage, entry)
            for entry in _stage_lanes(stage)
        }
        roster = "\n".join(
            f"  {lane['lane_index']}. {lane['lane']}\n"
            + (f"     effort: {lane_effort[lane['lane']]}\n"
               if lane_effort.get(lane["lane"]) else "")
            + f"     packet: {self._packet_display_path(lane, portable_path)}\n"
            f"     lane_packet_hash: {lane['hash']}"
            for lane in lanes
        )
        flags = " ".join(
            f"--lane-result {lane['lane']}=<path>" for lane in lanes
        )
        return (
            f"EXECUTION POLICY: FANOUT / HOST-MAX\n"
            f"\n"
            f"Launch one fresh subagent for each workflow-defined lane.\n"
            f"Run each lane at the reasoning effort its roster entry names. "
            f"That level is workflow data, not a host choice: do not raise or "
            f"lower it, and do not level the lanes to one effort because they "
            f"run together.\n"
            f"Use the maximum concurrent subagent capacity supported by this "
            f"host.\n"
            f"If all lanes cannot run simultaneously, execute them in "
            f"deterministic batches.\n"
            f"Do not invent, omit, combine, or subdivide lanes.\n"
            f"Associate every result with its declared lane id.\n"
            f"Completion order must not affect result ordering or successor "
            f"guidance.\n"
            f"\n"
            f"LANES ({count}, in canonical order):\n"
            f"{roster}\n"
            f"\n"
            f"1. Start exactly {count} fresh subagents, one per lane listed "
            f"above and none besides, each at the reasoning effort its roster "
            f"entry names. Give each one exactly the contents of its own lane "
            f"packet, and nothing else.\n"
            f"2. Run as many of those lanes at once as this host supports, up "
            f"to all {count} simultaneously. If this host supports fewer "
            f"concurrent subagents than there are lanes, take the lanes in the "
            f"canonical order above, run one batch at the host maximum, then "
            f"the next batch, until every lane has completed. Batching changes "
            f"no lane id, no lane order, and no lane packet byte.\n"
            f"3. Require each lane's structured result as JSON at a path you "
            f"choose. Each result must carry \"stage\": \"{stage['id']}\", "
            f"\"iteration\": {packet['iteration']}, \"lane\": its own lane id, "
            f"and \"lane_packet_hash\": that lane's lane_packet_hash above.\n"
            f"4. Run: {prefix} advance {run_id} {flags}\n"
            f"5. Follow the next packet tpt emits.\n"
            f"6. Stop only at ACCEPTED or BLOCKED.\n"
            f"\n"
            f"tpt performs the join itself, in the canonical lane order above. "
            f"Do not summarize, merge, reconcile, reorder, or edit any lane "
            f"result, and do not supplement a lane's work yourself. A lane "
            f"that cannot do its work returns BLOCKED in its own structured "
            f"result; the workflow decides what that means."
        )

    def _packet_display_path(
        self, packet: dict[str, Any], portable_path: bool
    ) -> str:
        """A packet path as guidance names it: portable for the bootstrap."""
        return (
            packet["path"].relative_to(self.repo_root).as_posix()
            if portable_path else str(packet["path"])
        )

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

    _validate_effort(path, data["id"], "default_effort",
                     data.get("default_effort"))

    for arg_name in data.get("argument_schema", {}):
        if str(arg_name).startswith(RUN_IDENTITY_PREFIX):
            raise WorkflowError(
                f"{path}: argument {arg_name!r} is in the reserved "
                f"`{RUN_IDENTITY_PREFIX}` namespace, which a gate command "
                f"uses to name the run's own identity"
            )

    doc_arg = data.get("document_argument")
    if doc_arg is not None and doc_arg not in data.get("argument_schema", {}):
        raise WorkflowError(
            f"{path}: document_argument {doc_arg!r} is not in argument_schema"
        )

    discovery = data.get("document_discovery")
    if discovery is not None:
        if not isinstance(discovery, dict) \
                or set(discovery) - {"search", "marker", "id_drops_leading",
                                     "validator"} \
                or not isinstance(discovery.get("search"), str) \
                or not discovery.get("search") \
                or type(discovery.get("id_drops_leading")) is not int \
                or discovery["id_drops_leading"] < 0 \
                or ("validator" in discovery
                    and not (isinstance(discovery["validator"], str)
                             and discovery["validator"])):
            raise WorkflowError(
                f"{path}: 'document_discovery' declares a 'search' glob, an "
                f"integer 'id_drops_leading', and optionally a 'marker' file "
                f"and a 'validator' command"
            )

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

        _validate_effort(path, sid, "effort", stage.get("effort"))

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
            if "effort" in stage:
                raise WorkflowError(
                    f"{path}: {sid}: a gate runs no agent, so it declares no "
                    f"reasoning 'effort'"
                )
            for key in ("pass_transition", "fail_transition", "max_iterations"):
                if key not in stage:
                    raise WorkflowError(
                        f"{path}: {sid}: gate stage requires '{key}'"
                    )
            if "checks" not in stage or not isinstance(stage["checks"], list):
                raise WorkflowError(f"{path}: {sid}: gate stage requires 'checks' list")

        _validate_execution(path, sid, stype, stage)
        _validate_repair_routes(path, sid, stype, stage)
        _validate_repairs(path, sid, stage)
        _validate_iteration_bounds(path, sid, stage)
        _validate_stage_flags(path, sid, stage)

    # Validate transitions point to valid stages or terminal states
    accepting = []
    for stage in data["stages"]:
        sid = stage["id"]
        targets = [
            (tkey, stage[tkey])
            for tkey in ("next", "pass_transition", "fail_transition")
            if tkey in stage
        ]
        targets += [
            (f"{REPAIR_ROUTES}[{index}].transition", route["transition"])
            for index, route in enumerate(stage.get(REPAIR_ROUTES) or [])
        ]
        for tkey, target in targets:
            if target not in stage_ids and target not in (ACCEPTED, BLOCKED):
                raise WorkflowError(
                    f"{path}: {sid}.{tkey} points to unknown stage: {target}"
                )
            if target == ACCEPTED:
                accepting.append((sid, tkey, stage["type"]))

    # Acceptance is the one transition no agent may attest. A stage whose
    # result comes from an AI worker cannot name ACCEPTED, because then the
    # worker's own PASS would be the whole of the acceptance decision. Only a
    # program gate, whose result tpt composes from checks it ran itself, may.
    for sid, tkey, stype in accepting:
        if stype != GATE:
            raise WorkflowError(
                f"{path}: {sid}.{tkey} is {ACCEPTED}, but {sid} is a {stype} "
                f"stage; only a {GATE} stage may accept a run"
            )
    if not accepting:
        raise WorkflowError(
            f"{path}: no stage transitions to {ACCEPTED}; the workflow has no "
            f"way to succeed"
        )


def _validate_repairs(
    path: Path, sid: str, stage: dict[str, Any]
) -> None:
    """A stage's declared repair ownership is a list of distinct targets."""
    if REPAIRS not in stage:
        return
    repairs = stage[REPAIRS]
    if not isinstance(repairs, list) or not repairs:
        raise WorkflowError(
            f"{path}: {sid}: '{REPAIRS}' must be a nonempty list of repair "
            f"targets this stage owns"
        )
    seen: set[str] = set()
    for index, target in enumerate(repairs):
        if not isinstance(target, str) or not target:
            raise WorkflowError(
                f"{path}: {sid}: {REPAIRS}[{index}] must be a nonempty string"
            )
        if target in seen:
            raise WorkflowError(
                f"{path}: {sid}: duplicate repair ownership: {target}"
            )
        seen.add(target)


def _validate_stage_flags(
    path: Path, sid: str, stage: dict[str, Any]
) -> None:
    """The two per-stage declarations this engine reads are booleans."""
    for key in ("reports_repairs", "records_standing_findings"):
        if key in stage and not isinstance(stage[key], bool):
            raise WorkflowError(
                f"{path}: {sid}: '{key}' must be true or false"
            )


def _validate_iteration_bounds(
    path: Path, sid: str, stage: dict[str, Any]
) -> None:
    """The two budgets a looping stage is bounded by, if it declares them.

    `max_iterations` bounds repetition; `max_total_iterations` is the absolute
    ceiling on consecutive failures and defaults to twice it. A ceiling below
    the repeat budget could never be reached by anything the repeat budget did
    not stop first, so declaring one is a mistake worth refusing at load.
    """
    if "max_iterations" not in stage and "max_total_iterations" not in stage:
        return
    max_iter = stage.get("max_iterations", 3)
    if type(max_iter) is not int or max_iter < 1:
        raise WorkflowError(
            f"{path}: {sid}: 'max_iterations' must be a positive integer"
        )
    if "max_total_iterations" not in stage:
        return
    ceiling = stage["max_total_iterations"]
    if type(ceiling) is not int or ceiling < max_iter:
        raise WorkflowError(
            f"{path}: {sid}: 'max_total_iterations' must be an integer of at "
            f"least 'max_iterations' ({max_iter}); a lower ceiling can never "
            f"be reached, because the repeat budget stops the stage first"
        )


def _validate_effort(
    path: Path, sid: str, field: str, value: Any
) -> None:
    """A declared reasoning effort is one of the levels, or is not declared.

    A level the engine does not know reaches a host as a word it will either
    ignore or guess at, and a stage silently run at the host's own default is
    the ungoverned dispatch this file exists to prevent.
    """
    if value is None:
        return
    if not isinstance(value, str) or value not in EFFORT_LEVELS:
        raise WorkflowError(
            f"{path}: {sid}: {field} must be one of: "
            f"{', '.join(EFFORT_LEVELS)}"
        )


def _validate_execution(
    path: Path, sid: str, stype: str, stage: dict[str, Any]
) -> None:
    """Every stage declares, as workflow data, who executes it and how many.

    Leaving this to the host left the one decision the engine exists to own —
    what work is dispatched to whom — outside the deterministic sequence. A
    host could run an evaluator as one agent or as five of its own invention,
    and nothing recorded which had happened.
    """
    execution = stage.get("execution")
    if not isinstance(execution, dict):
        raise WorkflowError(
            f"{path}: {sid}: stage requires an 'execution' policy object"
        )
    mode = execution.get("mode")

    if stype == GATE:
        # A gate is run by tpt. Letting one name an agent mode would put a
        # subagent between the engine and a check the engine runs itself.
        if mode != PROGRAM:
            raise WorkflowError(
                f"{path}: {sid}: a {GATE} stage must declare execution mode "
                f"{PROGRAM!r}, not {mode!r}; a program gate is run by tpt and "
                f"may not declare an agent execution mode"
            )
        if set(execution) != {"mode"}:
            raise WorkflowError(
                f"{path}: {sid}: a {PROGRAM} execution policy declares "
                f"nothing but 'mode'"
            )
        return

    if mode == PROGRAM:
        raise WorkflowError(
            f"{path}: {sid}: execution mode {PROGRAM!r} is for {GATE} stages "
            f"only; {sid} is a {stype} stage"
        )
    if mode not in AGENT_MODES:
        raise WorkflowError(
            f"{path}: {sid}: execution mode must be one of: "
            f"{', '.join(AGENT_MODES)}"
        )

    if mode == SINGLE:
        if set(execution) != {"mode"}:
            raise WorkflowError(
                f"{path}: {sid}: a {SINGLE} execution policy declares nothing "
                f"but 'mode'"
            )
        return

    if set(execution) != {"mode", "parallelism", "join", "lanes"}:
        raise WorkflowError(
            f"{path}: {sid}: a {FANOUT} execution policy declares exactly "
            f"'mode', 'parallelism', 'join', and 'lanes'"
        )
    if execution["parallelism"] != HOST_MAX:
        raise WorkflowError(
            f"{path}: {sid}: fan-out parallelism must be {HOST_MAX!r}"
        )
    if execution["join"] != STRICT_UNION:
        raise WorkflowError(
            f"{path}: {sid}: fan-out join must be {STRICT_UNION!r}"
        )
    lanes = execution["lanes"]
    if not isinstance(lanes, list) or len(lanes) < 2:
        raise WorkflowError(
            f"{path}: {sid}: a {FANOUT} stage declares at least two lanes; "
            f"one lane is a {SINGLE} stage"
        )
    seen: set[str] = set()
    for index, lane in enumerate(lanes):
        if not isinstance(lane, dict) \
                or set(lane) - {"id", "fragments", "effort"} \
                or "id" not in lane:
            raise WorkflowError(
                f"{path}: {sid}: lanes[{index}] declares an 'id' and "
                f"optionally 'fragments' and 'effort', and nothing else"
            )
        lane_id = lane["id"]
        if not isinstance(lane_id, str) or not lane_id \
                or not all(c in _LANE_ID_CHARS for c in lane_id):
            raise WorkflowError(
                f"{path}: {sid}: lanes[{index}].id must be a nonempty "
                f"lowercase-kebab identifier"
            )
        if lane_id in seen:
            raise WorkflowError(
                f"{path}: {sid}: duplicate lane id: {lane_id}"
            )
        seen.add(lane_id)
        _validate_effort(
            path, sid, f"lanes[{index}].effort", lane.get("effort")
        )
        fragments = lane.get("fragments", [])
        if not isinstance(fragments, list) or not all(
            isinstance(name, str) and name for name in fragments
        ):
            raise WorkflowError(
                f"{path}: {sid}: lanes[{index}].fragments must be a list of "
                f"fragment paths"
            )


# A misspelling of an existing name and a new name from the same family score
# almost alike, because these ids share most of their text. Two things tell
# them apart, and a token needs only one: a near-certain match stands on its
# own, and short of that the best match must lead the next by a distance. A
# one-character slip scores about 0.98 against the name it came from, while a
# genuinely new name in the same family tops out around 0.89 and is barely
# ahead of its neighbours.
_NEAREST_FLOOR = 0.6
_NEAREST_CERTAIN = 0.9
_NEAREST_MARGIN = 0.1


def _nearest_document(token: str, documents: list[str]) -> str | None:
    """The one document a token is probably a misspelling of, if any."""
    scored = sorted(
        (
            difflib.SequenceMatcher(
                None, token, document.rsplit("/", 1)[-1]
            ).ratio(),
            document,
        )
        for document in documents
    )
    if not scored or scored[-1][0] < _NEAREST_FLOOR:
        return None
    if scored[-1][0] >= _NEAREST_CERTAIN:
        return scored[-1][1]
    if len(scored) > 1 and scored[-1][0] - scored[-2][0] < _NEAREST_MARGIN:
        return None
    return scored[-1][1]


def _may_forward(stage: dict[str, Any], disposition: Any) -> bool:
    """Whether this stage, ending this way, forwards anything to its successor.

    The mirror of the cases `_extract_prior_findings` acts on, decided from
    the transition record alone.
    """
    if stage["type"] in (EVALUATOR, GATE):
        return disposition in (CHANGES_REQUIRED, FAIL)
    return (
        stage["type"] == LINEAR
        and bool(_stage_lanes(stage))
        and disposition == PASS
    )


def _escalation_note(state: dict[str, Any]) -> str:
    """The one line a terminal message owes the escalation ledger.

    A run that ends without saying it found something only a maintainer can
    fix has lost the finding as surely as discarding it would have.
    """
    escalations = state.get("escalations") or []
    if not escalations:
        return ""
    named = ", ".join(
        f"{entry['finding'].get('id', '(unidentified)')} "
        f"-> {entry.get('escalated_to') or '(unnamed artifact)'}"
        for entry in escalations
    )
    return (
        f" {len(escalations)} escalation"
        f"{'' if len(escalations) == 1 else 's'} stand for a maintainer, in "
        f"no artifact this run may write: {named}."
    )


def _document_root(
    workflow: dict[str, Any], args: dict[str, Any]
) -> str | None:
    """The repo-relative root of the thing under work, or None.

    Built from the workflow's own `document_root` template, so the engine
    states a path without knowing anything about what a proper leaf is. A
    workflow that declares no template gets no header line rather than a
    guessed one.
    """
    template = workflow.get("document_root")
    if not template:
        return None
    try:
        return template.format(**args)
    except (KeyError, IndexError):
        return None


def _standing_findings(
    repo_root: Path | None, document_root: str | None
) -> list[dict[str, Any]]:
    """Blocking findings a previous production left standing, or [].

    An absent file means no previous production recorded anything, and is not
    an error: it is the ordinary state of a leaf nobody has evaluated.

    **Nothing in the engine reads this into a packet, deliberately.** It was
    briefly read at seed, to give a pipeline beginning after research the
    carry-forward it has no stage for. That was wrong three ways at once and a
    cold review found all three: the pristine recompile in
    `_load_verified_bootstrap` did not know about the argument, so a run seeded
    against a non-empty record could never be seeded again -- breaking the
    idempotency `OPERATOR.md` promises and a whole suite tests; the file is
    untracked working-tree state that no `repo_commit` moves with and no
    `workflow_source_digest` covers, so the same run id could produce different
    bootstrap bytes; and on the full pipeline the findings reached only the
    `seed` stage's packet, unfiltered by `repair_target`.

    Carrying findings between productions still wants doing. It wants doing
    where the run's identity can cover it: either an operator subcommand whose
    output is committed, so `repo_commit` moves with it, or the record's own
    hash in `compute_run_id` and in the acceptance audit. Until then this is a
    record for people to read, and the format it defines.
    """
    if not document_root or repo_root is None:
        return []
    path = repo_root / document_root / STANDING_FINDINGS_PATH
    if not path.is_file():
        return []
    try:
        data = tomllib.loads(path.read_text(encoding="utf-8"))
    except (OSError, tomllib.TOMLDecodeError):
        # A record this run cannot read is a record it must not guess at. The
        # run proceeds with nothing carried, which is the state it would have
        # been in without the file at all.
        return []
    standing = []
    for entry in data.get("findings", []) or []:
        if not isinstance(entry, dict):
            continue
        standing.append({
            key: entry[key] for key in (
                "id", "lane", "severity", "location", "problem",
                "required_result", "repair_target",
            ) if key in entry
        })
    return standing


def _toml_string(value: str) -> str:
    """One TOML basic string, for prose nobody sanitized on the way in.

    The values here are a lane's own finding text. It quotes the document, so
    it arrives carrying quotation marks, backslashes out of LaTeX, and
    newlines, and it is written to a file another run has to parse. An escaper
    that is merely usually right produces a record that parses as something
    else, or not at all.

    Every quote is escaped in both forms, so the closing delimiter can never be
    read out of the content. That is more escaping than a multi-line string
    strictly needs and it is the reason this is short enough to be obviously
    correct: the earlier version tried to escape only `\"\"\"` and mangled a
    value ending in one.
    """
    text = str(value).replace("\r\n", "\n").replace("\r", "\n")
    # Control characters other than tab and newline are not permitted raw, and
    # `>= 0x20` is not that test: U+007F (DEL) satisfies it and TOML refuses it
    # anyway, so one stray byte in a quoted source made the whole record
    # unparseable -- and the reader, catching the parse error, discarded every
    # well-formed finding in it without a word. A lone surrogate is excluded
    # for the same reason one layer down: it is `str` that cannot be encoded.
    text = "".join(
        ch if ch in "\t\n" or (0x20 <= ord(ch) < 0x7F) or (
            0xA0 <= ord(ch) and not 0xD800 <= ord(ch) <= 0xDFFF
        )
        else "\\u%04x" % ord(ch)
        for ch in text
    )
    escaped = text.replace("\\", "\\\\").replace('"', '\\"')
    if "\n" not in text:
        return '"' + escaped + '"'
    return '"""\n' + escaped + '"""'


def _blocking_ids(result: dict[str, Any]) -> list[str]:
    """Every blocking finding id in a result, sorted and unique.

    Sorted because the set is compared and reported, never read in the order
    lanes happened to finish in.
    """
    return sorted({
        str(finding.get("id", "(unidentified)"))
        for finding in result.get("findings", []) or []
        if finding.get("severity") == "blocking"
    })


def _repair_route(
    stage: dict[str, Any], result: dict[str, Any]
) -> dict[str, Any] | None:
    """The declared route this result's blocking findings select, or None.

    An evaluator can find two different kinds of defect, and they are not
    repaired in the same place. Which one a run goes to is read from a field
    the evaluator set on each blocking finding, not from prose, a filename, a
    finding-id prefix, or anything a controller decides.

    Declaration order is priority order: the first declared target that any
    blocking finding names wins, so a result carrying both kinds takes the
    earlier route. Nothing here reads finding order or completion order, so
    the same result always selects the same route.
    """
    routes = stage.get(REPAIR_ROUTES)
    if not routes:
        return None
    named = {
        finding.get(REPAIR_TARGET)
        for finding in result.get("findings", []) or []
        if finding.get("severity") == "blocking"
    }
    for route in routes:
        if route[REPAIR_TARGET] in named:
            return route
    return None


def _validate_repair_routes(
    path: Path, sid: str, stype: str, stage: dict[str, Any]
) -> None:
    """Repair ownership is a closed, ordered list, declared by the workflow.

    An evaluator that can find two kinds of defect needs somewhere to send
    each. Leaving that to a controller reading finding prose would put the
    one decision the routing exists to make back where it started.
    """
    if REPAIR_ROUTES not in stage:
        return
    if stype != EVALUATOR:
        raise WorkflowError(
            f"{path}: {sid}: only an {EVALUATOR} stage may declare "
            f"'{REPAIR_ROUTES}'; {sid} is a {stype} stage"
        )
    routes = stage[REPAIR_ROUTES]
    if not isinstance(routes, list) or not routes:
        raise WorkflowError(
            f"{path}: {sid}: '{REPAIR_ROUTES}' must be a nonempty list"
        )
    seen: set[str] = set()
    for index, route in enumerate(routes):
        if not isinstance(route, dict) \
                or set(route) != {REPAIR_TARGET, "transition"}:
            raise WorkflowError(
                f"{path}: {sid}: {REPAIR_ROUTES}[{index}] declares exactly "
                f"'{REPAIR_TARGET}' and 'transition'"
            )
        target = route[REPAIR_TARGET]
        if not isinstance(target, str) or not target:
            raise WorkflowError(
                f"{path}: {sid}: {REPAIR_ROUTES}[{index}].{REPAIR_TARGET} "
                f"must be a nonempty string"
            )
        if target in seen:
            raise WorkflowError(
                f"{path}: {sid}: duplicate repair target: {target}"
            )
        seen.add(target)


def _stage_execution(stage: dict[str, Any]) -> dict[str, Any]:
    """A stage's declared execution policy."""
    execution = stage.get("execution")
    return execution if isinstance(execution, dict) else {}


def _stage_lanes(stage: dict[str, Any]) -> list[dict[str, Any]]:
    """The workflow-defined lanes of a fan-out stage, in canonical order.

    Canonical order is declaration order, and it is the only order anything
    downstream uses: lane packets, lane results, the join, and the successor
    packet all read this list, never the order lanes happened to finish in.
    """
    execution = _stage_execution(stage)
    if execution.get("mode") != FANOUT:
        return []
    return list(execution["lanes"])


def _stage_effort(
    workflow: dict[str, Any], stage: dict[str, Any],
    lane: dict[str, Any] | None = None,
) -> str | None:
    """The reasoning effort the agent for this packet is dispatched at.

    Most specific wins: the lane's own declaration, then the stage's, then
    the workflow default. A gate is run by tpt and has no effort at all.
    """
    if stage.get("type") == GATE:
        return None
    if lane is not None and lane.get("effort"):
        return str(lane["effort"])
    if stage.get("effort"):
        return str(stage["effort"])
    default = workflow.get("default_effort")
    return str(default) if default else None


def _execution_label(stage: dict[str, Any]) -> str:
    """The execution policy as it appears in hashed packet material."""
    execution = _stage_execution(stage)
    mode = execution.get("mode", "")
    if mode == FANOUT:
        return f"{FANOUT}/{execution.get('parallelism', '')}"
    return str(mode)


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
        # A field the engine branches on is required only where it is read.
        # Demanding it of an advisory finding would reject a legitimate note;
        # accepting a blocking finding without it would leave the engine to
        # guess at the one thing it must not guess at.
        blocking_fields = schema.get("blocking_finding_fields", [])
        escalation_fields = schema.get("escalation_finding_fields", [])
        finding_enums = schema.get("finding_enums", {})
        for i, finding in enumerate(findings):
            if not isinstance(finding, dict):
                raise WorkflowError(f"findings[{i}] must be an object")
            for field in finding_fields:
                if field not in finding:
                    raise WorkflowError(
                        f"findings[{i}] missing required field: {field}"
                    )
            if finding.get("severity") == "blocking":
                for field in blocking_fields:
                    if field not in finding:
                        raise WorkflowError(
                            f"findings[{i}] is blocking and missing required "
                            f"field: {field}"
                        )
            elif finding.get("severity") == ESCALATION:
                for field in escalation_fields:
                    if field not in finding:
                        raise WorkflowError(
                            f"findings[{i}] is an escalation and missing "
                            f"required field: {field}"
                        )
                # An escalation is precisely a defect no stage in this run may
                # repair. Naming a repair owner would make it a blocking
                # finding wearing a severity that exempts it from the audit.
                for field in blocking_fields:
                    if field in finding:
                        raise WorkflowError(
                            f"findings[{i}] is an escalation and carries "
                            f"'{field}'; an escalation has no repair owner in "
                            f"this run, which is what makes it an escalation. "
                            f"Name one and it is blocking."
                        )
            for field in sorted(finding_enums):
                if field in finding \
                        and finding[field] not in finding_enums[field]:
                    raise WorkflowError(
                        f"findings[{i}].{field} is {finding[field]!r}; "
                        f"expected one of: "
                        f"{', '.join(finding_enums[field])}"
                    )

    # An observation is a lane's record of something real it saw and its own
    # criteria do not reach. It carries no severity and routes no repair: it
    # exists so that such a sighting reaches the run at all. Before it, the
    # only route from a lane to the record was the driver writing a finding of
    # its own, which the fan-out policy forbids and which is what made an
    # earlier run unreplayable — so four defects that four max-effort sweeps
    # located were seen, correctly declined, and lost.
    if "observations" in result:
        observations = result["observations"]
        if not isinstance(observations, list):
            raise WorkflowError("result.observations must be a list")
        observation_fields = schema.get("observation_fields", [])
        if not observation_fields and observations:
            raise WorkflowError(
                "result carries observations, which this stage's schema does "
                "not define"
            )
        for i, observation in enumerate(observations):
            if not isinstance(observation, dict):
                raise WorkflowError(f"observations[{i}] must be an object")
            for field in observation_fields:
                if field not in observation:
                    raise WorkflowError(
                        f"observations[{i}] missing required field: {field}"
                    )

    # A reviser's account of what it did with each finding it was given. The
    # engine's convergence budget is charged from this and from nothing else,
    # so a malformed report is refused rather than read past.
    if "finding_dispositions" in result:
        dispositions = result["finding_dispositions"]
        if not isinstance(dispositions, list):
            raise WorkflowError("result.finding_dispositions must be a list")
        disposition_fields = schema.get("finding_disposition_fields", [])
        if not disposition_fields and dispositions:
            raise WorkflowError(
                "result carries finding_dispositions, which this stage's "
                "schema does not define"
            )
        disposition_enums = schema.get("finding_disposition_enums", {})
        for i, entry in enumerate(dispositions):
            if not isinstance(entry, dict):
                raise WorkflowError(
                    f"finding_dispositions[{i}] must be an object"
                )
            for field in disposition_fields:
                if field not in entry:
                    raise WorkflowError(
                        f"finding_dispositions[{i}] missing required field: "
                        f"{field}"
                    )
            for field in sorted(disposition_enums):
                if field in entry \
                        and entry[field] not in disposition_enums[field]:
                    raise WorkflowError(
                        f"finding_dispositions[{i}].{field} is "
                        f"{entry[field]!r}; expected one of: "
                        f"{', '.join(disposition_enums[field])}"
                    )

    # Malformed results fail closed: if we got here without raising,
    # the result is structurally valid.


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _utc_timestamp() -> str:
    """A human-readable UTC timestamp. Never used in packet hashes."""
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())


# One placeholder: a brace pair with no brace inside it. The name between the
# braces is looked up, and a name nothing supplies is left exactly as written.
_PLACEHOLDER = re.compile(r"\{([^{}]*)\}")


def _substitute_args(template: str, args: dict[str, str],
                     quote: bool = False) -> str:
    """Substitute {name} placeholders in a template, in one pass.

    With quote=True the value is shell-quoted, for a gate command that runs
    through a shell.

    One pass is the security property, not an optimisation. Substituting each
    name in turn re-reads what the previous substitution wrote, so a value
    holding the text of another placeholder had that placeholder expanded
    inside it — a supplied value deciding what a later name expands to, inside
    a template the workflow wrote. Nothing in this repository exploited it and
    nothing needs to: a value is data, and data is never scanned for names. A
    name no caller supplies is still left alone, so a template may say
    `{example}` and mean it.
    """
    def replace(match: re.Match[str]) -> str:
        key = match.group(1)
        if key not in args:
            return match.group(0)
        return shlex.quote(args[key]) if quote else args[key]

    return _PLACEHOLDER.sub(replace, template)


def _run_identity(workflow: dict[str, Any],
                  state: dict[str, Any]) -> dict[str, str]:
    """The run's own facts, under the reserved `run.` namespace.

    These are exactly the five identifying facts the packet header states —
    workflow, version, source digest, run id, seed commit — and they are
    stated here for the same reason the header states them: a check that must
    hold a document against the run that produced it cannot do it from the
    document's arguments, which say nothing about which run is holding them.

    Every one is engine-generated: two are hashes, one is a workflow id the
    definition declares, one an integer, one a commit sha. None of that is
    relied on. They are substituted as data and shell-quoted exactly like an
    argument, because a value's provenance is not a security property.
    """
    return {
        f"{RUN_IDENTITY_PREFIX}workflow_id": str(workflow["id"]),
        f"{RUN_IDENTITY_PREFIX}workflow_version": str(workflow["version"]),
        f"{RUN_IDENTITY_PREFIX}workflow_digest": str(state["workflow_digest"]),
        f"{RUN_IDENTITY_PREFIX}run_id": str(state["run_id"]),
        f"{RUN_IDENTITY_PREFIX}repo_commit": str(state["repo_commit"]),
    }


def _gate_substitutions(workflow: dict[str, Any],
                        state: dict[str, Any]) -> dict[str, str]:
    """What a gate command may name: the run's arguments and the run itself.

    A collision here would let an argument decide what a run fact expands to,
    which is the whole of what this namespace exists to prevent, so it is a
    refusal and not a precedence rule. `_validate_workflow` refuses such an
    argument when the definition is loaded; this refuses it again at the point
    of use, because an argument may reach a run without being declared.
    """
    args = state["normalized_args"]
    identity = _run_identity(workflow, state)
    collisions = sorted(set(args) & set(identity))
    if collisions:
        raise WorkflowError(
            f"run {state['run_id']}: argument "
            f"{', '.join(repr(name) for name in collisions)} is in the "
            f"reserved `{RUN_IDENTITY_PREFIX}` namespace, which names the "
            f"run's own identity to a gate command; an argument may not "
            f"decide what a run fact expands to"
        )
    return {**args, **identity}


def _result_bytes(result: dict[str, Any]) -> bytes:
    """The canonical bytes a result is both stored and hashed as."""
    return (
        json.dumps(result, sort_keys=True, indent=2) + "\n"
    ).encode("utf-8")


def _canonical_json_bytes(value: dict[str, Any]) -> bytes:
    """Canonical JSON object bytes used for persisted protocol evidence."""
    return (
        json.dumps(
            value, sort_keys=True, indent=2, ensure_ascii=True,
            allow_nan=False, separators=(",", ": "),
        ) + "\n"
    ).encode("utf-8")


_LANE_ID_CHARS = frozenset("abcdefghijklmnopqrstuvwxyz0123456789-")


def _is_sha256(value: Any) -> bool:
    """Whether value is one lowercase 64-character SHA-256 hex digest."""
    return (
        isinstance(value, str) and len(value) == 64
        and all(char in "0123456789abcdef" for char in value)
    )


def _read_json(path: Path) -> dict[str, Any]:
    """Read a run's JSON, reporting a half-written file as a workflow error."""
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as error:
        raise WorkflowError(f"{path}: invalid JSON: {error}") from error
    except OSError as error:
        raise WorkflowError(f"{path}: cannot read: {error}") from error
    if not isinstance(value, dict):
        raise WorkflowError(
            f"{path}: expected a JSON object, not {type(value).__name__}"
        )
    return value


def _lf(text: str) -> str:
    """Normalize line endings, so a checkout's newlines cannot change a hash."""
    return text.replace("\r\n", "\n").replace("\r", "\n")


def _current_packet(state: dict[str, Any], stage_id: str) -> dict[str, Any]:
    """The packet record the run is currently waiting on an answer for."""
    packets = state.get("packet_hashes") or []
    if not packets:
        raise WorkflowError(
            f"run {state.get('run_id')}: no packet has been emitted for stage "
            f"{stage_id}"
        )
    last = packets[-1]
    if last["stage"] != stage_id:
        raise WorkflowError(
            f"run {state.get('run_id')}: the last emitted packet is for stage "
            f"{last['stage']}, not {stage_id}; the run state is inconsistent"
        )
    return last
