# TPT Workflow Engine — Operator Documentation

## Overview

The deterministic AI-guidance workflow engine drives a cycle of fresh AI
workers, each given exactly one compiled instruction packet, each required to
return a structured result. The engine owns fragment selection, packet
composition, transitions, iteration bounds, and stop conditions. No AI agent
decides what instructions its successor receives.

## Commands

### List available workflows

```bash
tools/tpt workflow list
```

### Show a workflow definition

```bash
tools/tpt workflow show proper
```

### Create or replay a run bootstrap

```bash
tools/tpt proper <proper-id> seed [--provider <gpt|claude>]
```

Example:

```bash
tools/tpt proper liturgy/roman-rite/1962/propers/temporal/46-ninth-after-pentecost seed --provider gpt
```

The first invocation creates a run directory under
`build/tpt-runs/<run-id>/`, persists the canonical bootstrap response, and
emits it. Every later identical invocation verifies the run and emits those
same stored bytes when the repository commit, workflow identity, and normalized
arguments are unchanged, even after the run has advanced. A repeated seed
writes no packet, event, result, transition, counter, or state. The output
includes:

- `bootstrap_version`: the bootstrap protocol version
- `run_id`: the deterministic run identifier
- `workflow_id`, `workflow_version`, `workflow_digest`: the bound workflow
  identity
- `repo_commit`, `normalized_args`: the other deterministic run inputs
- `stage`, `iteration`: the original seed-stage packet identity
- `packet_hash`: SHA-256 of the compiled packet bytes
- `packet_path`: repository-relative path to the original packet file
- `instructions`: the exact next controller action and command

`seed` is not a status or resume command. Use `status` for current state,
`replay` to verify and reproduce the current packet, and `advance` to perform a
transition. A repeated seed fails closed if the workflow source, manifest,
state, bootstrap, or original packet no longer matches the run. Pre-fix runs
that lack stored bootstrap evidence cannot replay it; continue them with
`status`, `replay`, or `advance`, or deliberately discard the old run before
seeding again.

### Advance a run

After a fresh AI worker has processed the packet and produced a structured
JSON result:

```bash
tools/tpt proper <proper-id> advance <run-id> --result <path-to-json>
```

For gate stages (mechanical checks), the engine runs the checks directly:

```bash
tools/tpt proper <proper-id> advance <run-id> --run-gate
```

The output includes the next packet (if the workflow continues) or a
terminal disposition (`ACCEPTED` or `BLOCKED`).

Every command after `seed` names the document as well as the run id, and the
document is checked against the run. A command naming a different document is
refused.

### Check run status

```bash
tools/tpt proper <proper-id> status <run-id>
```

### Verify the current packet

```bash
tools/tpt proper <proper-id> replay <run-id>
```

Recompiles the current packet from the persisted state and compares it with the
recorded hash, writing nothing. It also reports whether the packet file on disk
still matches what was recorded. Exit status is non-zero if the recompiled
bytes differ.

### Record a manual intervention

```bash
tools/tpt proper <proper-id> intervene <run-id> --text "Check the Latin collation against page 412"
```

Interventions are stored under the run's `interventions/` directory with
`encoded: false`. They represent workflow debt: ad hoc instructions that
have not yet been promoted into reusable fragments, evaluator criteria,
deterministic gates, or document-specific rules.

### Show unencoded workflow debt

```bash
tools/tpt proper <proper-id> debt <run-id>
```

Lists all interventions with `encoded: false`.

## The driver cycle

The parent agent (Claude or Codex session) follows this cycle:

1. **Seed**: Run `tpt proper <id> seed` to create a run and get the first packet.
2. **Dispatch**: Start a clean AI worker. Give it exactly the packet contents.
   Require its structured result as JSON at a path you choose.
3. **Advance**: Run `tpt proper <id> advance <run-id> --result <path>`.
4. **Follow**: Read the next packet emitted by `tpt`. Go to step 2.
5. **Stop**: Stop only when the disposition is `ACCEPTED` or `BLOCKED`.

For gate stages, step 2 is replaced by `tpt proper <id> advance <run-id>
--run-gate` (no AI worker needed).

An `advance` that fails changes nothing: the run stays on the stage it was on,
and the result it refused is not part of the run. Read the error, fix what it
names — a malformed result, a full or read-only run directory — and run the
same command again. Never hand-edit `state.json` to get past one; a run whose
state or recorded files were edited fails its next command, and cannot be
accepted.

## Structured result formats

Every result repeats the `STAGE` and `ITERATION` of the packet it answers. The
engine rejects a result naming any other packet, which is what makes a
resubmitted, stale, or wrong-stage result an error instead of a transition.

### Worker (linear or revision) stages

```json
{
  "stage": "author-proper",
  "iteration": 0,
  "disposition": "PASS | BLOCKED",
  "summary": "What you did, in one or two sentences.",
  "artifact_path": "path/to/main.tex"
}
```

`BLOCKED` is how a worker reports that it could not do the stage's work; the run
stops there rather than advancing on work that did not happen.

### Evaluator stages

```json
{
  "stage": "content-evaluation",
  "iteration": 0,
  "disposition": "PASS | CHANGES_REQUIRED | BLOCKED",
  "summary": "One or two sentences.",
  "findings": [
    {
      "id": "CON-001",
      "severity": "blocking",
      "location": "page 4",
      "problem": "Description of the issue.",
      "required_result": "What the reviser must produce."
    }
  ]
}
```

Only `blocking` findings trigger revision. `advisory` findings are recorded
but do not block.

Finding IDs must be stable across iterations. Use `CON-` prefix for content
evaluation and `VIS-` for visual evaluation.

### Gate stages

Gates are run by `tpt` directly. No AI worker result is needed. The gate
produces:

```json
{
  "stage": "mechanical-gates",
  "iteration": 0,
  "disposition": "PASS | FAIL",
  "findings": [
    {
      "id": "GATE-BUILD-CANONICAL",
      "severity": "blocking",
      "check": "build-canonical",
      "problem": "command exited 1: ...",
      "required_result": "canonical PDF must build without fatal errors"
    }
  ]
}
```

A finding quotes what the check printed, with the repository root and home
directory replaced by `<repo>` and `<home>` so the same failure reads the same
on any machine. The untouched output of every check is kept under the run's
`gate-logs/`.

## Run state directory

Each run has a durable state directory:

```
build/tpt-runs/<run-id>/
    manifest.json          # immutable run metadata
    bootstrap.json         # immutable canonical seed response bytes
    state.json             # mutable run state
    events.jsonl           # append-only event log
    packets/               # compiled guidance packets
    results/               # submitted structured results, named for the packet
    gate-logs/             # untouched output of every gate check
    artifacts/             # worker-produced artifacts (by reference)
    interventions/         # recorded manual interventions
```

The run can be inspected at any time. The state file records the current
stage, iteration counts, packet hashes, result hashes, transitions, and
final disposition. It is checked against the immutable manifest on every load,
so an edited, truncated, or relocated run reports an error instead of
advancing.

## Determinism

Given the same repository commit, workflow version, document type, arguments,
workflow state, and prior structured results, `tpt` emits the same next
guidance packet byte-for-byte. The packet SHA-256 is recorded in the run
state and can be verified with `replay`.

No timestamps, run IDs, or filesystem paths appear in the hashed packet
material. Only the workflow source (definition, fragments, schemas), the
repository commit, the stage, the iteration, the normalized arguments, and the
forwarded findings determine the packet bytes.

A run is bound to the workflow source it was seeded against. Editing
`workflows/pipelines/proper.json`, a fragment, or a schema stops every existing
run with an error; the changed workflow applies to new runs. That is deliberate:
a run cannot claim continuity with a deterministic sequence it is no longer
following.

## Promoting workflow debt

When an ad hoc intervention has been applied enough times to be worth
promoting, an operator:

1. Edits the workflow definition (`workflows/pipelines/proper.json`) or
   fragments (`workflows/fragments/`) to encode the instruction as a
   permanent part of the workflow.
2. Marks the intervention as `encoded: true` in its JSON file under
   `interventions/`.

The engine never auto-promotes interventions, and a recorded intervention never
reaches a packet: nothing in packet compilation reads `interventions/`. An
intervention is a note about guidance the workflow does not yet give, and it
changes no packet and no recorded hash. Promotion is a deliberate human act,
and it applies to runs seeded after it.

## The propers workflow

The first real workflow is `proper` (1962 propers synthesis production).
Its stages are:

```
seed
  ↓
resolve-context
  ↓
source-audit
  ↓
research-synthesis
  ↓
author-proper
  ↓
content-evaluation
  ├─ CHANGES_REQUIRED → content-revision → reevaluate
  ├─ PASS ↓
build-artifacts
  ↓
mechanical-gates (programmatic)
  ├─ FAIL → artifact-revision → rebuild → re-gate
  ├─ PASS ↓
visual-evaluation (AI)
  ├─ CHANGES_REQUIRED → visual-revision → rebuild → mechanical-gates → visual
  ├─ PASS ↓
final-acceptance (programmatic)
  ├─ FAIL → artifact-revision → rebuild → mechanical-gates → visual → accept
  ├─ PASS ↓
ACCEPTED
```

Mechanical gates use existing Triptych tools:
- `tools/tpt check-proper-components`
- `make doc DOC=<proper> PROVIDER=<provider>`
- `make doc DOC=<proper>-synthesis PROVIDER=<provider>`

Visual evaluation is performed by a fresh AI evaluator who inspects rendered
page rasters produced by `tools/tpt pdf-review`.

Final acceptance is a gate, not a stage any agent is asked about. Advance it
with `tpt proper <id> advance <run-id> --run-gate <doc>` like any other gate.
It rechecks, on the artifacts as they now stand, the four things the stage used
to ask a worker to confirm:

- `build/{provider}/{proper}.pdf` exists;
- `build/{provider}/{proper}-synthesis.pdf` exists;
- `tpt check-proper-components --aux` passes, so the component manifest matches
  the built artifacts and the brief synthesis occupies exactly two pages; and
- `tpt check-generation-metadata --pdf` passes, so the tracked revision and AI
  provenance in the source agree with the rendered PDF.

A failed check sends the run to `artifact-revision` with the check's own output
as findings, and the revised artifacts come back through the mechanical gates
and visual evaluation before acceptance is attempted again. That loop is
bounded: three refusals block the run.

Passing the checks is necessary, not sufficient. Before it records `ACCEPTED`
the engine audits the run: every evaluator and gate that ran must last have
recorded `PASS`, every recorded result and packet must still be present and
hash as recorded, and no stage's latest result may carry a standing blocking
finding. A run whose files were edited cannot be accepted; discard it
deliberately before seeding anew.
