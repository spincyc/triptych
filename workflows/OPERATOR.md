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
JSON result. The result must repeat the packet's hash in a `packet_hash`
field, so pass the hash to the worker along with the packet; `tpt` refuses a
result that answers a different packet, including a stale one resubmitted
after the run has advanced:

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

### Verify a packet by recompilation

```bash
tools/tpt proper <proper-id> replay <run-id>
```

This reloads the run state, recompiles the current packet, and compares the
result to the hash recorded when the packet was issued. It exits non-zero if
they differ.

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
    manifest.json          # immutable run metadata, checked on every advance
    state.json             # mutable run state
    events.jsonl           # append-only event log
    packets/               # compiled guidance packets
    results/               # submitted structured results
    artifacts/             # worker-produced artifacts (by reference)
    interventions/         # recorded manual interventions
```

The run can be inspected at any time. The state file records the current
stage, iteration counts, consecutive failure counts, packet hashes, result
hashes, transitions, and final disposition.

`manifest.json` is not merely a record. Every `advance` and `replay` re-reads
it and refuses to continue if `state.json` disagrees with it, or if the
guidance source (the pipeline definition and every fragment and schema it
references) has changed since the run was seeded. Editing a fragment during a
run is therefore not a silent act: the run stops and tells you to bump the
workflow version and seed a new run.

## Determinism

Given the same repository commit, workflow version, document type, arguments,
workflow state, and prior structured results, `tpt` emits the same next
guidance packet byte-for-byte. The packet SHA-256 is recorded in the run
state; `replay` verifies it by recompilation.

No timestamps or run IDs appear in the hashed packet material. Only the
workflow definition, its source digest, the repository commit, the stage,
the iteration, the normalized arguments, and the forwarded findings determine
the packet bytes.

One caveat worth knowing: a gate's findings quote the failing command's
output, and that output can contain absolute paths from the machine that ran
the gate. Those findings are forwarded into the next revision packet, so a
revision packet's bytes are reproducible only on a machine whose gate output
matches. The guidance the engine composes is machine-independent; what a
failing build says about itself is not.

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
final-acceptance (AI)
  ├─ CHANGES_REQUIRED → visual-revision → rebuild → mechanical-gates → visual
  ├─ BLOCKED → BLOCKED
  ├─ PASS ↓
ACCEPTED
```

Final acceptance is an evaluator, not a formality. It can refuse, and a
refusal re-enters revision and the mechanical gates rather than accepting the
run.

Mechanical gates use existing Triptych tools:
- `tools/tpt check-proper-components`
- `make doc DOC=<proper> PROVIDER=<provider>`
- `make doc DOC=<proper>-synthesis PROVIDER=<provider>`

Visual evaluation is performed by a fresh AI evaluator who inspects rendered
page rasters produced by `tools/tpt pdf-review`.
