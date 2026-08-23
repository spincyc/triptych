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

### Seed a new run

```bash
tools/tpt proper <proper-id> seed [--provider <gpt|claude>]
```

Example:

```bash
tools/tpt proper liturgy/roman-rite/1962/propers/temporal/46-ninth-after-pentecost seed --provider gpt
```

This creates a run directory under `build/tpt-runs/<run-id>/` and emits the
first guidance packet. The output includes:

- `run_id`: the deterministic run identifier
- `packet_hash`: SHA-256 of the compiled packet bytes
- `packet_path`: path to the packet file
- `instructions`: the driver instructions for the parent agent

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

### Check run status

```bash
tools/tpt proper <proper-id> status <run-id>
```

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

## Structured result formats

### Worker (linear or revision) stages

```json
{
  "disposition": "PASS",
  "summary": "What you did, in one or two sentences.",
  "artifact_path": "path/to/main.tex"
}
```

### Evaluator stages

```json
{
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

## Run state directory

Each run has a durable state directory:

```
build/tpt-runs/<run-id>/
    manifest.json          # immutable run metadata
    state.json             # mutable run state
    events.jsonl           # append-only event log
    packets/               # compiled guidance packets
    results/               # submitted structured results
    artifacts/             # worker-produced artifacts (by reference)
    interventions/         # recorded manual interventions
```

The run can be inspected at any time. The state file records the current
stage, iteration counts, packet hashes, result hashes, transitions, and
final disposition.

## Determinism

Given the same repository commit, workflow version, document type, arguments,
workflow state, and prior structured results, `tpt` emits the same next
guidance packet byte-for-byte. The packet SHA-256 is recorded in the run
state and can be verified by recompilation.

No timestamps, run IDs, or filesystem paths appear in the hashed packet
material. Only the workflow definition, repository commit, stage, iteration,
normalized arguments, and forwarded findings determine the packet bytes.

## Promoting workflow debt

When an ad hoc intervention has been applied enough times to be worth
promoting, an operator:

1. Edits the workflow definition (`workflows/pipelines/proper.json`) or
   fragments (`workflows/fragments/`) to encode the instruction as a
   permanent part of the workflow.
2. Marks the intervention as `encoded: true` in its JSON file under
   `interventions/`.

The engine never auto-promotes interventions. Promotion is a deliberate
human act.

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
final-acceptance
  ↓
ACCEPTED
```

Mechanical gates use existing Triptych tools:
- `tools/tpt check-proper-components`
- `make doc DOC=<proper> PROVIDER=<provider>`
- `make doc DOC=<proper>-synthesis PROVIDER=<provider>`

Visual evaluation is performed by a fresh AI evaluator who inspects rendered
page rasters produced by `tools/tpt pdf-review`.
