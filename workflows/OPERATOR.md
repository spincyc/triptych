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

### Read a workflow's own help

```bash
tools/tpt proper --help
```

Prints the workflow's grammar, every action with its flags, and how to name a
document. `tools/tpt proper` with no arguments prints the same thing.

### Find a document id

```bash
tools/tpt proper list
tools/tpt proper list --json
```

Every document the workflow can be seeded for, one per line and in a stable
order. The workflow declares where its documents live, in
`document_discovery`, so the list is what is actually on disk rather than
something maintained by hand: for `proper`, every leaf under
`src/<provider>/liturgy/roman-rite/1962/propers/` that has a `main.tex`. A
leaf without one is not listed, because it cannot be run.

You do not have to type the whole id. Any unique tail of one stands for it,
so these are the same command:

```bash
tools/tpt proper liturgy/roman-rite/1962/propers/temporal/49-ninth-after-pentecost seed
tools/tpt proper 49-ninth-after-pentecost seed
```

A tail matching more than one document is refused with the candidates listed.
A tail matching none is refused with the full id it would have to be given as,
ready to copy — a document that does not exist yet is named in full, and
seeding one is an ordinary thing to do, since the seed stage's own job is to
report what a leaf is still missing. If the tail looks instead like a
misspelling of something that does exist, that one document is named.

Anything containing a `/` is taken as a full id and passed through untouched,
so a command that worked before still works, and so a leaf that has not been
created yet can still be seeded.

### Create or replay a run bootstrap

```bash
tools/tpt proper <proper-id> seed [--provider <gpt|claude>]
```

Example:

```bash
tools/tpt proper liturgy/roman-rite/1962/propers/temporal/49-ninth-after-pentecost seed --provider gpt
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

The rest of a lane result follows its own stage's contract: an evaluation lane
returns the evaluator shape, a `research` lane the research shape, and the
dispositions each admits differ. See Structured result formats below.

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

### Research lane stages

A lane of the read-only `research` stage returns evidence rather than an
artifact, and validates against `workflows/schema/research-result.json`:

```json
{
  "stage": "research",
  "iteration": 0,
  "lane": "scripture-context",
  "lane_packet_hash": "the lane_packet_hash tpt printed for this lane",
  "disposition": "PASS | BLOCKED",
  "summary": "One or two sentences on what was swept and what was found.",
  "findings": [
    {
      "id": "SCR-001",
      "claim": "What the lane asserts, in one sentence.",
      "evidence": ["Each source named precisely enough to be checked."],
      "notes": "Uncertainty, disagreement, negative results, evidence state."
    }
  ]
}
```

Every finding carries all four of `id`, `claim`, `evidence`, and `notes`, and
`evidence` is a list of strings. A sweep that found nothing records the negative
result as a finding rather than omitting it.

There are only two dispositions. `PASS` means the lane did its sweep, whether or
not it found much; `BLOCKED` means it could not, and because `research` is a
linear stage the run stops there. There is no `CHANGES_REQUIRED` for a research
lane and the engine rejects one — a research lane judges nothing and asks no one
to revise anything.

Finding IDs use the lane's own prefix, listed with the lanes under The propers
workflow below.

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
      "required_result": "What the reviser must produce.",
      "repair_target": "research | brief | authoring"
    }
  ]
}
```

Only `blocking` findings trigger revision. `advisory` findings are recorded
but do not block.

Finding IDs must be stable across iterations. Use `CON-` prefix for content
evaluation and `VIS-` for visual evaluation; `research-synthesis` is an
evaluator too and has its own prefix, below.

`content-evaluation` also names who repairs each defect. Every blocking finding
it returns carries `repair_target`, validated against
`workflows/schema/content-evaluation-result.json`, and it names one of three
owners: `research` when the evidence is not there and a sweep must go and get
it, `brief` when the evidence is there and `research/scope.md` states it
wrongly or drops a bound it recorded, and `authoring` when the brief is
adequate but the canonical leaf's prose, structure, or use of citations is not.
The set is closed, a blocking finding that omits the field is refused, and
advisory findings do not carry it. `visual-evaluation` and the gates route no
repairs and use no `repair_target`.

`tpt` reads the field and picks the route itself, in the order the workflow
declares its routes: one blocking finding naming `research`, from any lane,
sends the run to `research`; failing that, one naming `brief` sends it to
`research-synthesis`, the brief's sole writer; and a join whose blocking
findings all name `authoring` goes to `content-revision`. So a
`CHANGES_REQUIRED` content evaluation can print `"stage": "research"` or
`"stage": "research-synthesis"` as the next stage. That is correct, not a bug —
the run resweeps or restates, reauthors, and is evaluated fresh. Only the
findings that chose the route are forwarded, so the research lane packets carry
the `research` findings and none of the others. You neither choose the route
nor summarize anything into it.

A lane of a fan-out evaluator returns this same shape plus `lane` and
`lane_packet_hash`, and uses its own lane's finding-ID prefix; see Execution
policy above. Each lane reports only on the criteria its own lane fragment
gives it. `tpt` writes the joined result to `results/<stage>-<iteration>.json`:
every lane's findings verbatim, each tagged with the `lane` that raised it, in
canonical lane order, with the worst disposition any lane returned and a
`summary` that rolls the lanes' dispositions up in that same order.

### The research-synthesis stage

`research-synthesis` returns the evaluator shape above, validated against
`workflows/schema/evaluator-result.json`. Its judgment is about the research it
has just read rather than about a document, so its findings carry no
`repair_target`, and what you submit differs by disposition:

```json
{
  "stage": "research-synthesis",
  "iteration": 0,
  "disposition": "CHANGES_REQUIRED",
  "summary": "One or two sentences.",
  "findings": [
    {
      "id": "SYN-001",
      "severity": "blocking",
      "location": "patristic-reception",
      "problem": "What the joined research lacks.",
      "required_result": "What that lane must come back with."
    }
  ]
}
```

`PASS` carries `findings: []` and an `artifact_path` pointing at
`research/scope.md`. `advance` prints the `author-proper` packet.

`CHANGES_REQUIRED` means the research is insufficient but plausibly
recoverable: concrete missing or inadequate research that the existing seven
lanes could reasonably supply on another pass. Every such result must carry at
least one `blocking` finding, and the engine refuses one that names none. Each
blocking finding names in `location` the lane that owes the work — one of the
seven lane ids — and says in `required_result` what that lane must come back
with. Use the `SYN-` prefix for finding ids, stable across iterations.
`advance` prints the seven `research` lane packets again, each carrying these
findings verbatim on its `PRIOR_FINDINGS` line, and you dispatch the seven
lanes as you did the first time. You summarize nothing into them.

`BLOCKED` means genuinely unrecoverable within this workflow: another pass
through the same lanes cannot reasonably solve it — a required source
unavailable under current policy, irreconcilable identity or formulary
uncertainty, an authoritative witness that cannot be obtained, corruption.
`advance` prints the terminal `BLOCKED` disposition and the run ends. A thin
first sweep is not that, and asking for what no lane can supply is not
`CHANGES_REQUIRED`.

The retry loop is bounded by this stage's own `max_iterations`, counted
consecutively: two retries are granted, and the third `CHANGES_REQUIRED` in a
row from this stage blocks the run, which `advance` reports as `iteration limit
exceeded for research-synthesis: 3/3 consecutive failures`. A `PASS` resets the
count. The budget is this stage's alone: `content-evaluation` has its own, and
a run that evaluator sends back to `research` spends nothing here.

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

Forwarded findings are part of those bytes. When a fan-out stage is a linear
one — `research` is — and its join passes, `tpt` forwards the joined findings
into the next stage's packet: every lane's findings verbatim, each tagged with
the `lane` that raised it, in canonical lane order. The `research-synthesis`
worker reads the engine's own join on its packet's `PRIOR_FINDINGS` header line,
and you are never asked to summarize the seven lanes into it. A
`CHANGES_REQUIRED` content evaluation forwards the blocking findings that own
the route it took and no others. `replay` rebuilds whatever a packet was
compiled with by the same rule that forwarded it, reading the recorded result,
and fails closed if that file is missing or no longer hashes as recorded, so
the packet replays to the same bytes.

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
authorize-target
  ↓
scope-gate (programmatic)
  ├─ FAIL → BLOCKED (the target is not authorized; nothing is produced)
  ├─ PASS ↓
resolve-context
  ↓
source-audit
  ↓
research (fan-out, seven read-only lanes)
  ├─ scripture-context
  ├─ patristic-reception
  ├─ liturgical-history
  ├─ theological-synthesis
  ├─ source-citation-coverage
  ├─ cultural-afterlife
  ├─ precedent-search
  ↓ joined findings forwarded
research-synthesis
  ├─ CHANGES_REQUIRED → research → the seven lanes resweep → resynthesize
  ├─ BLOCKED → run ends
  ├─ PASS ↓
author-proper
  ↓
content-preflight (programmatic)
  ├─ FAIL → content-revision → reevaluate (never research: these are leaf defects)
  ├─ PASS ↓
content-evaluation
  ├─ CHANGES_REQUIRED, a research defect → research → synthesis → author → reevaluate
  ├─ CHANGES_REQUIRED, a brief defect → research-synthesis → author → reevaluate
  ├─ CHANGES_REQUIRED, authoring defects only → content-revision → reevaluate
  ├─ PASS ↓
build-artifacts
  ↓
mechanical-gates (programmatic)
  ├─ FAIL → artifact-revision → rebuild → re-gate
  ├─ PASS ↓
visual-evaluation (AI)
  ├─ CHANGES_REQUIRED → visual-revision → rebuild → mechanical-gates → visual
  ├─ PASS ↓
final-acceptance (programmatic; accepts the artifacts)
  ├─ FAIL → artifact-revision → rebuild → mechanical-gates → visual → accept
  ├─ PASS ↓
publish-artifacts
  ↓
generate-web
  ↓
web-evaluation (AI)
  ├─ CHANGES_REQUIRED → web-revision → generate-web → re-evaluate
  ├─ PASS ↓
install-publication
  ↓
publication-gates (programmatic; accepts the run)
  ├─ FAIL → publication-revision → install-publication → re-gate
  ├─ PASS ↓
ACCEPTED
```

### The lifecycle a run completes

A run is not finished when the PDFs build. The lifecycle is:

```
authorize -> produce -> artifact-accept -> publish -> catalog-wire
          -> publication-accept
```

Authorization comes first and is a separate decision from identity. The 1962
propers collections are closed, and `guidance/liturgy/propers-production-plan.md`
is the maintainer's record of that closure and of every target since reopened.
**A valid permanent identity is not authorization.** The registry and the
profile keep the identities complete and fixed so that a guide, if one is ever
written, can be placed; an identity with no guide is the normal state of the
collection, not a queue entry. `scope-gate` therefore asks three questions and
requires all three: that the identity is one the 1962 calendar registers, that
the provider is one this repository publishes for, and that the production plan
carries an authorization for **exactly** that provider and that identity. A
refusal is terminal — `BLOCKED`, not a revision loop — because a run whose
target was never authorized has nothing to revise.

Authorization is strictly per provider. Authorizing `gpt` for an identity
authorizes nothing for `claude`, and neither authorizes a neighbouring
identity or the series either belongs to. `authorize-target` writes one entry
per provider-and-identity pair and writes nothing at all when the pair is
already recorded.

Publication comes last and is gated in its own right. `final-acceptance`
accepts the *artifacts*; `publication-gates` accepts the *run*, and it is the
only stage that can produce `ACCEPTED`. What it verifies is set out under
Final acceptance below.

Mechanical gates use existing Triptych tools:
- `tools/tpt check-proper-components`
- `make doc DOC=<proper> PROVIDER=<provider>`
- `make doc DOC=<proper>-synthesis PROVIDER=<provider>`

Visual evaluation is performed by fresh AI evaluators who inspect rendered
page rasters produced by `tools/tpt pdf-review`.

Each stage declares how it is run:

- `single`, one fresh subagent: `seed`, `authorize-target`,
  `resolve-context`, `source-audit`, `research-synthesis`, `author-proper`,
  `content-revision`, `build-artifacts`, `artifact-revision`,
  `visual-revision`, `publish-artifacts`, `generate-web`, `web-evaluation`,
  `web-revision`, `install-publication`, `publication-revision`. Every
  authoring and revision stage mutates the canonical leaf, `source-audit` may
  retrieve and write the provenance files, and `research-synthesis` is the sole
  owner of `research/scope.md` and the only place the seven lanes' findings are
  reconciled, so each of them owns an authoritative artifact that exactly one
  agent may hold. The publication stages own authoritative artifacts too — the
  scope entry, the installed PDFs, the generated and the tracked web edition,
  the release records, and the catalog cell — one owner each.
  `web-evaluation` is `single` rather than a fan-out because there is one
  conversion to judge and one edition to judge it against; nothing partitions.
- `program`, run by `tpt` itself: `scope-gate`, `content-preflight`,
  `mechanical-gates`, `final-acceptance`, `publication-gates`.
- `fanout/host-max`: `research`, `content-evaluation`, and `visual-evaluation`.
  All three mutate no authoritative artifact — one discovers, two judge — so
  their work is partitioned across lanes that can run at the same time. Nothing
  a lane does can conflict with a sibling's, because no lane writes anything.

`research` declares seven lanes, in canonical order:

1. `scripture-context`, finding IDs `SCR-`
2. `patristic-reception`, finding IDs `PAT-`
3. `liturgical-history`, finding IDs `LIT-`
4. `theological-synthesis`, finding IDs `THE-`
5. `source-citation-coverage`, finding IDs `COV-`
6. `cultural-afterlife`, finding IDs `CUL-`
7. `precedent-search`, finding IDs `PRE-`

A research lane writes nothing in the repository. It does not touch the
canonical leaf, `propers/verified.md`, `propers/retrieved.txt`,
`research/scope.md`, or any shared source inventory; it typesets nothing,
revises no prose, and does not read or merge another lane's findings. Its only
product is the structured result it returns to `tpt`, and `tpt` forwards the
join of the seven to `research-synthesis`, which owns the integration.

`research-synthesis` integrates and does not research. It runs no web search,
no repository precedent search, and no source acquisition; it hunts no cultural
afterlives and looks for no new witnesses; and it may not fill a gap from model
memory. It selects the notable-and-quotable entries and the interpretive
proposals from what the `cultural-afterlife` and `precedent-search` lanes
returned rather than finding its own. It is an `evaluator` stage rather than a
linear one, so it has three answers about whether the joined seven-lane research
can be authored from: `PASS` sends the brief on, `CHANGES_REQUIRED` sends the
run back through the seven lanes, and `BLOCKED` ends it. See Structured result
formats above for what to submit for each.

`author-proper` reads that brief as immutable input and may not repair it. An
author that finds it insufficient, contradictory, or missing evidence it needs
returns `disposition: "BLOCKED"` naming what the brief lacks, and because
`author-proper` is a linear stage the run stops there: the `advance` that
submitted the result prints the terminal disposition, and the author's summary
is the record of what the research left out. The author has no route back into
`research` of its own: only `content-evaluation` sends a run to another sweep,
and only for a defect it found in work the author already produced. When the
run stops here instead, improve the research guidance or the sources it sweeps,
then seed a new run.

`content-evaluation` declares five lanes, in canonical order:

1. `evidence-discipline`, finding IDs `CON-EVI-`
2. `reception-sweep`, finding IDs `CON-REC-`
3. `synthesis-argument`, finding IDs `CON-SYN-`
4. `citation-integrity`, finding IDs `CON-CIT-`
5. `profile-conformance`, finding IDs `CON-PRO-`

`content-evaluation` is also the one stage that routes its own repairs. Each
blocking finding its lanes raise names `repair_target`, and `tpt` reads that
field to decide where a `CHANGES_REQUIRED` join sends the run — back to
`research` if any of them names `research`, to `research-synthesis` if any
names `brief`, and to `content-revision` otherwise. See Structured result
formats above.

`visual-evaluation` declares four, in canonical order:

1. `density-and-hierarchy`, finding IDs `VIS-DEN-`
2. `page-rhythm`, finding IDs `VIS-RHY-`
3. `fixed-pagination`, finding IDs `VIS-FIX-`
4. `clipping-and-apparatus`, finding IDs `VIS-APP-`

Each lane's fragment under `workflows/fragments/propers/lanes/` states what that
lane alone owns and mandates its distinct finding-ID prefix, so the joined
findings keep stable, non-colliding ids. For the two evaluators the fragments
partition the numbered criteria of the shared stage fragment, with no criterion
invented or dropped; for `research` they partition the questions asked, and each
lane is told which questions belong to the other six. Both evaluators still
bound their revision loops at three consecutive `CHANGES_REQUIRED` joins, as
before, whichever route those joins took, and `research` has no revision loop
of its own — a lane that cannot sweep returns `BLOCKED` and the run stops, and
a re-entry, whether routed from `content-evaluation` or sent back by
`research-synthesis`, is a fresh visit to the stage on the budget of the
evaluator that sent it.

The `proper` workflow is at version 12. Version 12 put the house voice into
the fragments a worker is handed: `author-proper` now carries the declarative
and tradition-inhabiting rules that `guidance/editorial.md` owns,
`content-revision` says a voice finding is repaired by rewriting the sentence
and never by deleting what the sentence was about, `content-evaluation` gained
criteria 11 and 12 and rewrote criterion 6 so it asks whether a disagreement is
present and attributed rather than whether the guide says it preserved one, and
the two lanes that own those criteria say so. Four instructions that were
producing the defect went with it: the research lane's "bounded and
correctable", which was right for a `notes` field and reached the printed page
in seven places; the afterlife lane's limiting qualification, which both
providers printed as a per-entry block; the synthesis brief's register, which
the author was inheriting along with the conclusions; and the profile's
requirement that a signpost-only scan recover the principal limits, which a
guide can satisfy only by printing the limits as signposts. It changed no
stage, no lane and no transition, and it needed no repair target of its own. A
voice defect is `authoring`: the material was researched and the prose is what
mishandled it. The one case the author cannot repair — a passage the evidence
gives no Catholic reception for at all — is `research`. Version 10's third
owner, `brief`, does not arise for criteria 11 and 12: a reception that was
swept and never carried into the brief is a criterion 3 defect, and the
ordinary discriminator already routes it.

The `proper` workflow is at version 11. Version 11 is what two production runs
driven to completion asked for, and it changes the content loop in five places.

`content-evaluation`'s iteration budget now charges repetition rather than
failure. `max_iterations` bounds the number of failures that re-raise a
blocking finding the stage already had standing; the first failure of a streak
is charged too, because it has nothing to repeat and because exempting it would
loosen every declared limit by one. An evaluation that raises different ids has
found different work and costs nothing against that budget. A second bound,
`max_total_iterations`, defaults to twice `max_iterations` and caps consecutive
failures however novel they are, so a stage that finds something new forever
still terminates: for `content-evaluation` that is six. Run
`b68cca80edb75854` blocked at three under the old rule with four of five lanes
passing and one finding standing, which the lane that raised it recorded as its
own miss at the earlier iterations rather than a regression.

A blocking finding now reaches its owner even when a different owner wins the
route. Each repairing stage declares the targets it owns in a `repairs` list —
`research` for `research`, `research-synthesis` for `brief`, and both
`author-proper` and `content-revision` for `authoring`, because either may be
the next to write the leaf — and a finding whose owner did not win the route is
carried in a new `CARRIED_FINDINGS` packet header to whichever owner runs next.
Routing itself is unchanged. Before this, one `brief` finding sent the run to
`research-synthesis` and seven `authoring` findings raised in the same
evaluation reached nobody; the author re-authored from an empty packet and the
next evaluation rediscovered them.

Findings carry a third severity, `escalation`, for a defect in an artifact no
stage of the workflow may write — repository guidance, the source library, the
tools. It takes no `repair_target`, and the engine refuses one that claims
both: having no owner is what makes it an escalation. It does not block, does
not spend the budget, and does not stop acceptance; it is recorded in a run
escalation ledger keyed by finding id, and reported in `status` and in the
terminal message. `profile-conformance` found a genuine contradiction in the
propers profile's macro-order and could only file it advisory, where it was
restated every iteration and acted on in none.

`content-preflight` gained a fifth check, `restricted-not-reproduced`, the
first in the pipeline that reads `src/sources/` rights at all. It refuses a
leaf that binds a `storage = "restricted"` artifact as its `translation-control`
and a leaf that attributes a set passage to a bound source whose bytes are
restricted. `unquoted-not-quoted` is a self-consistency check and always was:
an earlier production reproduced a restricted NABRE verbatim at ten loci and
passed every gate. The same change taught both checks to read a leaf's own
aliases of the printed-passage environments; six of the twenty published
propers wrap `sourcecard` in a local name, and `unquoted-not-quoted` had been
seeing no printed passages at all in those six.

And `research-synthesis` must now carry a prior production's standing findings
into the brief, under a `Prior-production carry-forward` heading, or state that
there was no prior production. Re-seeding starts a run with an empty history —
the run id is derived from workflow version, commit and arguments — and one
re-seed dropped fourteen standing findings, five recovered by hand and one
surviving verbatim into the next production because nobody carried it.

Version 10 changed two things about the
content loop. `content-evaluation` gained a third repair owner, `brief`, which
routes to `research-synthesis`: a defect the brief already holds the evidence
for is one sentence of `research/scope.md`, and sending it to `research`
discarded a sound brief and re-ran seven lanes to arrive back at the same
writer. And a programmatic `content-preflight` gate now sits between
`author-proper` and `content-evaluation`, running four checks a shell can
decide — that every References entry is cited in the body, that every source
identifier the leaf prints is registered, that every component-manifest
relation's element keys are claimed by the unit carrying its evidence, and that
no source the References declare unquoted is credited with a quotation. Its
failures go to `content-revision` and never to research: they are mechanical
defects in the leaf. Nothing else changed; research, the lanes, the other
evaluators and the publication phase are as they were at version 9.

Version 9 gave the workflow the whole
lifecycle: an `authorize-target` stage and a terminal-on-failure `scope-gate`
in front of the production phase, and `publish-artifacts`, `generate-web`,
`web-evaluation` with its `web-revision` loop, `install-publication`, and the
terminal `publication-gates` with its `publication-revision` loop behind it.
`final-acceptance` kept its id and its four checks and now passes to
`publish-artifacts`; the run is accepted by `publication-gates`, because the
acceptance audit requires every other evaluator and gate to have passed and
so the accepting gate can only be the last one. Nothing about research,
authoring, the lanes, the two evaluation fan-outs, or the mechanical gates
changed. Version 8 declared
`document_discovery`, so `tools/tpt proper list` can name the documents the
workflow runs and a unique tail of an id stands for the id; it changed no
stage, no packet and no transition, but the declaration is part of the bound
workflow source like everything else in the definition. Version 7 made
`research-synthesis` an evaluator stage, so research too thin to author a
safe brief from re-enters the seven lanes instead of ending the run at that
commit. Version 6 added the
`cultural-afterlife` and `precedent-search` research lanes, made
`research-synthesis` a pure integrator of what those and the other five lanes
returned, and gave `content-evaluation` a result schema of its own and the
repair routes that let a `CHANGES_REQUIRED` evaluation re-enter `research`. The
content and visual evaluation lanes, the gates, and every other `single` stage
are as they were at version 5. A run seeded against version 11 or any earlier
version is bound to that source and fails closed rather than continuing under
fragments it never started with; seed it again.

`content-preflight` is a gate like any other: advance it with
`tpt proper <id> advance <run-id> --run-gate <doc>`. Each of its four checks is
one invocation of `tools/tpt check-content-preflight --check <name>`, judged by
exit code, and the tool prints what it counted on a pass and names the entry,
identifier, relation or quotation it refused on a failure. It exists so the
five-lane evaluation behind it spends its budget on judgment rather than on
things grep can settle; it does not replace any of that judgment. A failed
check sends the run to `content-revision` with the check's own output as
findings, and that loop is bounded at three consecutive failures like every
other.

Artifact acceptance is a gate, not a stage any agent is asked about. Advance
it with `tpt proper <id> advance <run-id> --run-gate <doc>` like any other
gate. It rechecks, on the artifacts as they now stand, the four things the
stage used to ask a worker to confirm:

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

`publication-gates` is the terminal gate and the only stage that can produce
`ACCEPTED`. On the publication as it now stands it verifies that the scope
authorization still holds; that both PDFs are installed under
`pdf/<provider>/`; that `check-proper-components --aux` and
`check-generation-metadata` still pass, the latter against the installed
canonical PDF rather than the build tree; that the leaf declares a web
edition and `check-web-edition` accepts it; that the canonical web edition
exists at `web/<provider>/<proper>.md` and is tracked, not merely generated;
that no separate `-synthesis` web leaf exists, because the synthesis is a
derived companion and not a second prose authority; that a per-publication
release record exists for the canonical publication **and** for the
synthesis; and that this provider's catalog cell links all three published
artifacts. A failed check sends the run to `publication-revision`, which
repairs the wiring at `install-publication` and re-gates, and that loop is
bounded at three refusals as well.

Passing the checks is necessary, not sufficient. Before it records `ACCEPTED`
the engine audits the run: every evaluator and gate that ran must last have
recorded `PASS`, every recorded result and packet must still be present and
hash as recorded — lane packets and lane results included — and no stage's
latest result may carry a standing blocking finding. A run whose files were
edited cannot be accepted; discard it deliberately before seeding anew.
