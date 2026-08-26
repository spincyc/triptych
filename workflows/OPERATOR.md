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

For fan-out stages, pass one flag per workflow-defined lane; the engine joins
the lane results itself:

```bash
tools/tpt proper <proper-id> advance <run-id> --lane-result <lane-id>=<path-to-json> ...
```

For gate stages (mechanical checks), the engine runs the checks directly:

```bash
tools/tpt proper <proper-id> advance <run-id> --run-gate
```

Which of the three forms a stage takes is fixed by its execution policy, not by
you, and `tpt` prints the exact command with every packet. See Execution policy
below.

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

1. **Seed**: Run `tpt proper <id> seed` to create a run and get the first
   packet.
2. **Dispatch**: Read the execution policy `tpt` states at the top of the
   `instructions` it just printed, and do exactly what it says:
   - `SINGLE`: start one clean AI worker, give it exactly the packet contents,
     and require its structured result as JSON at a path you choose.
   - `FANOUT / HOST-MAX`: start one clean AI worker per listed lane and none
     besides, give each exactly its own lane packet, and require one structured
     result per lane.
   - `PROGRAM GATE`: start no worker; `tpt` runs the stage itself.
3. **Advance**: Run the command `tpt` printed — `advance <run-id> --result
   <path>`, one `--lane-result <lane-id>=<path>` per lane, or `--run-gate`.
4. **Follow**: Read the next packet emitted by `tpt`. Go to step 2.
5. **Stop**: Stop only when the disposition is `ACCEPTED` or `BLOCKED`.

The next section states each policy in full.

An `advance` that fails changes nothing: the run stays on the stage it was on,
and the result it refused is not part of the run. Read the error, fix what it
names — a malformed result, a full or read-only run directory — and run the
same command again. Never hand-edit `state.json` to get past one; a run whose
state or recorded files were edited fails its next command, and cannot be
accepted.

## Execution policy

Every stage declares how its work is dispatched, and `tpt` states that policy at
the top of the `instructions` it prints with each packet. The only thing you
choose is how many lanes of a fan-out stage run at once.

### Single

`EXECUTION POLICY: SINGLE`. Start exactly one fresh subagent, give it exactly
the packet contents, and advance with the result it returns:

```bash
tools/tpt proper <proper-id> advance <run-id> --result <path-to-json>
```

Launch no additional agents for the stage, and add no work of your own to what
the packet asks for.

### Program gate

`EXECUTION POLICY: PROGRAM GATE`. Start no subagent at all. `tpt` runs the
stage's checks itself:

```bash
tools/tpt proper <proper-id> advance <run-id> --run-gate
```

### Fanout / host-max

`EXECUTION POLICY: FANOUT / HOST-MAX`. The instructions list every lane in
canonical order with its own packet path and `lane_packet_hash`. Start one
fresh subagent per listed lane and none besides, give each exactly the contents
of its own lane packet, and require one structured JSON result per lane. Then
advance with one `--lane-result` flag per lane:

```bash
tools/tpt proper <proper-id> advance <run-id> \
  --lane-result evidence-discipline=<path> \
  --lane-result reception-sweep=<path> \
  --lane-result synthesis-argument=<path> \
  --lane-result citation-integrity=<path> \
  --lane-result profile-conformance=<path>
```

A lane result repeats the `stage` and `iteration` like any other result, and
adds two fields binding it to its own lane packet:

```json
{
  "stage": "content-evaluation",
  "iteration": 0,
  "lane": "citation-integrity",
  "lane_packet_hash": "the lane_packet_hash tpt printed for this lane",
  "disposition": "PASS | CHANGES_REQUIRED | BLOCKED",
  "summary": "One or two sentences.",
  "findings": []
}
```

- `lane`: the lane's own id, exactly as the instructions and the lane packet's
  `LANE` header line name it
- `lane_packet_hash`: the `lane_packet_hash` the instructions printed for that
  lane

Run as many lanes at once as your host supports, up to all of them. If it
supports fewer concurrent subagents than there are lanes, take the lanes in the
canonical order the instructions list them, run one batch at your host's
maximum, then the next, until every lane has finished. Batching changes no lane
id, no lane order, and no lane packet byte.

`tpt` performs the join. Do not invent, omit, combine, or subdivide lanes; do
not summarize, merge, reconcile, reorder, or edit a lane result; and do not
supplement a lane's work yourself. A lane that cannot do its work returns
`BLOCKED` in its own structured result, and the workflow decides what that
means.

The submission is all or nothing. A lane the stage does not declare, the same
lane submitted twice, a result whose `lane` disagrees with the flag that
carried it, a `lane_packet_hash` other than the one emitted for that lane, and
any declared lane left out are each refused with the run untouched — no lane's
result becomes part of the run because another lane's was acceptable. Fix what
the error names and submit the whole set again.

The flags are not interchangeable either: `--result` on a fan-out stage,
`--lane-result` on a single stage or a gate, and `--run-gate` on anything but a
gate are all refused.

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

A lane of a fan-out evaluator returns this same shape plus `lane` and
`lane_packet_hash`, and uses its own lane's finding-ID prefix; see Execution
policy above. Each lane reports only on the criteria its own lane fragment
gives it. `tpt` writes the joined result to `results/<stage>-<iteration>.json`:
every lane's findings verbatim, each tagged with the `lane` that raised it, in
canonical lane order, with the worst disposition any lane returned and a
`summary` that rolls the lanes' dispositions up in that same order.

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

A fan-out stage adds one packet and one result per lane beside the stage's
own, named for the lane's canonical index and id:

```
packets/content-evaluation-0000.txt
packets/content-evaluation-0000-lane-00-evidence-discipline.txt
packets/content-evaluation-0000-lane-01-reception-sweep.txt
results/content-evaluation-0000.json
results/content-evaluation-0000-lane-00-evidence-discipline.json
results/content-evaluation-0000-lane-01-reception-sweep.json
```

The stage's own `results/<stage>-<iteration>.json` is the joined result `tpt`
composed; each `-lane-` file is exactly the bytes that lane returned. The state
records both, so a run whose lane packet or lane result was edited afterwards
fails its next command and cannot be accepted.

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
repository commit, the stage, the iteration, the stage's execution policy and
lane identity, the normalized arguments, and the forwarded findings determine
the packet bytes.

Nothing about how your host scheduled a fan-out stage reaches those bytes: no
worker process id, launch or completion timestamp, scheduler slot, or
completion order. Running five lanes at once and running them one at a time
compile the same lane packets, and lanes that finish C, A, D, B are joined
exactly as A, B, C, D, so the same lane work yields the same successor packet
whatever your host's capacity. `replay` reports each lane's recompiled hash
beside the one recorded, and calls the run non-deterministic if any lane
diverges.

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

Visual evaluation is performed by fresh AI evaluators who inspect rendered
page rasters produced by `tools/tpt pdf-review`.

Each stage declares how it is run:

- `single`, one fresh subagent: `seed`, `resolve-context`, `source-audit`,
  `research-synthesis`, `author-proper`, `content-revision`, `build-artifacts`,
  `artifact-revision`, `visual-revision`. Every authoring and revision stage
  mutates the canonical leaf, and `source-audit` may retrieve and write the
  provenance files, so each of them owns an authoritative artifact that exactly
  one agent may hold.
- `program`, run by `tpt` itself: `mechanical-gates`, `final-acceptance`.
- `fanout/host-max`: `content-evaluation` and `visual-evaluation`. Both are
  read-only judgment stages that mutate no authoritative artifact, so their
  criteria are partitioned across lanes that can run at the same time.

`content-evaluation` declares five lanes, in canonical order:

1. `evidence-discipline`, finding IDs `CON-EVI-`
2. `reception-sweep`, finding IDs `CON-REC-`
3. `synthesis-argument`, finding IDs `CON-SYN-`
4. `citation-integrity`, finding IDs `CON-CIT-`
5. `profile-conformance`, finding IDs `CON-PRO-`

`visual-evaluation` declares four, in canonical order:

1. `density-and-hierarchy`, finding IDs `VIS-DEN-`
2. `page-rhythm`, finding IDs `VIS-RHY-`
3. `fixed-pagination`, finding IDs `VIS-FIX-`
4. `clipping-and-apparatus`, finding IDs `VIS-APP-`

Each lane's fragment under `workflows/fragments/propers/lanes/` partitions the
numbered criteria of the shared stage fragment — no criterion was invented or
dropped — and mandates that lane's distinct finding-ID prefix, so the joined
findings keep stable, non-colliding ids. Both stages still bound their revision
loops at three consecutive `CHANGES_REQUIRED` joins, as before.

The `proper` workflow is at version 3. A run seeded against version 2 is bound
to that source and cannot be continued under this policy; seed it again.

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
hash as recorded — lane packets and lane results included — and no stage's
latest result may carry a standing blocking finding. A run whose files were
edited cannot be accepted; discard it deliberately before seeding anew.
