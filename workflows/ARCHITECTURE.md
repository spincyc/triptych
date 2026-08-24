# TPT Deterministic Guidance Workflow Engine — Architecture Note

## Purpose

This note describes the architecture of the deterministic AI-guidance workflow
engine implemented behind `tools/tpt`. The engine owns the guidance sequence
so that no AI agent decides what instructions its successor receives.

The invariant:

> Given the same repository commit, workflow version, document type,
> arguments, workflow state, and prior structured results, `tpt` must emit
> the same next AI guidance packet byte-for-byte.

## Directory structure

```
workflows/
  ARCHITECTURE.md              # this note
  OPERATOR.md                  # operator documentation
  fragments/                   # inert instruction fragments (not agent guidance)
    common/                    # shared across workflows
      agent-brief.md
      result-format.md
    propers/                   # propers-specific fragments
      seed.md
      resolve-context.md
      source-audit.md
      research-synthesis.md
      author-proper.md
      content-evaluation.md
      content-revision.md
      build-artifacts.md
      artifact-revision.md
      visual-evaluation.md
      visual-revision.md
      final-acceptance.md
  pipelines/                   # machine-readable workflow definitions
    proper.json
  schema/                      # machine-enforced contracts
    worker-result.json
    evaluator-result.json
    gate-result.json
scripts/
  _workflow.py                 # workflow engine core (shared module)
tools/
  tpt                          # launcher (extended with workflow dispatch)
  tests/
    test_workflow_determinism.py
    test_workflow_engine.py
```

## Why workflow files cannot become ambient agent guidance

Fragments live under `workflows/fragments/`, never under `guidance/`. The
repository's agent guidance is served from `guidance/` and referenced by
`AGENTS.md`. No `AGENTS.md` or agent instruction file references
`workflows/fragments/` as ambient guidance. Fragments are read only by the
workflow engine when it compiles a packet, and they reach an AI worker only
as part of that compiled packet. A developer browsing the repository will
never read them as instructions unless they are inside a run.

## State model

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

### manifest.json (immutable)

Written once at seed time. Contains:

- `run_id`: deterministic identifier
- `workflow_id`, `workflow_version`: workflow definition reference
- `repo_commit`: repository commit SHA at seed time
- `normalized_args`: sorted, string-valued argument map
- `source_digest`: SHA-256 over the pipeline definition and every fragment
  and schema it references, as they stood at seed time
- `created_at`: human-readable timestamp (NOT used in packet hashes)

The manifest is load-bearing, not a record. Every `advance` and `replay`
re-reads it, recomputes `source_digest`, and refuses to continue if the
guidance source has changed or if `state.json` disagrees with it. A run is
therefore bound to the exact bytes of guidance it was seeded from; an edited
fragment cannot reach a run in progress under the same workflow version.

### state.json (mutable)

Updated after every transition. Contains:

- `current_stage`: stage id or `ACCEPTED` / `BLOCKED`
- `iteration`: global iteration counter
- `stage_iterations`: per-stage iteration counts (how often each stage has
  been entered)
- `stage_failures`: per-stage consecutive failure counts, reset on a pass;
  this, not `stage_iterations`, is what bounds a loop
- `packet_hashes`: list of `{stage, iteration, hash, path}`
- `result_hashes`: list of `{stage, iteration, hash, path}`
- `transitions`: list of `{from, to, disposition}`
- `disposition`: `null` while running, `ACCEPTED` or `BLOCKED` at terminal

### events.jsonl

Append-only, one JSON object per line. Each event records a state transition,
packet emission, result submission, or intervention. Timestamps are included
for human inspection but are never part of packet hash inputs.

## Packet compilation algorithm

The packet is the complete instruction set given to a fresh AI worker. It is
compiled deterministically from the workflow definition and the current run
state.

1. **Select stage**: look up `current_stage` in the workflow definition.
2. **Select fragments**: the stage declares an ordered list of fragment paths.
   Read each file from `workflows/fragments/` in the declared order.
3. **Build header**: a deterministic preamble containing:
   - `WORKFLOW`: workflow id and version
   - `COMMIT`: repository commit at seed time
   - `SOURCE_DIGEST`: digest of the guidance source this packet was
     compiled from
   - `STAGE`: stage id
   - `ITERATION`: iteration number for this stage
   - `ARGS`: normalized arguments as sorted JSON
   - `PRIOR_FINDINGS`: forwarded findings from the last evaluator/gate result
     (empty for non-revision stages), serialized as sorted JSON
4. **Assemble**: join header and fragments with a fixed separator.
5. **Encode**: UTF-8, no BOM, LF line endings.
6. **Hash**: SHA-256 of the exact bytes.
7. **Write**: to `packets/<stage>-<iteration>.txt`.

### Hashing boundary

The hash covers the packet bytes only. It does NOT cover:
- the run_id (unique per run, not per state)
- timestamps (nondeterministic)
- filesystem paths (machine-specific)
- the state file itself (contains timestamps)

The hash DOES cover:
- workflow id and version
- repository commit
- the guidance source digest
- stage id and iteration
- normalized arguments
- forwarded findings (for revision packets)
- all fragment contents in declared order

## Binding a result to its packet

Every worker and evaluator result must carry `packet_hash`, repeating the hash
of the packet it answers. `advance` compares it to the hash of the packet
awaiting an answer and refuses anything else.

This is what removes the last piece of parent-agent discretion over
successor guidance. Without it, a driver holding results from several stages
chooses which guidance a stage is treated as having answered, and a stale
result can be resubmitted after the run has moved on. Gate results are exempt:
the engine composes them itself and no agent is involved.

## Transition semantics

### Linear stage

A linear stage emits a packet, accepts a worker result, and transitions to
exactly one next stage. The result must have `disposition: "PASS"` to
advance, or `disposition: "BLOCKED"` to stop the run when the worker cannot
do the work at all. Any other disposition fails closed. A worker is never
asked to report success for work it did not do: nothing downstream reads its
`summary`, so a false `PASS` would advance the run silently.

### Evaluator stage

An evaluator stage emits a packet (the evaluation criteria), accepts an
evaluator result, and transitions based on disposition:

- `PASS` → `pass_transition` target
- `CHANGES_REQUIRED` → `fail_transition` target (a bounded-revision stage)
- `BLOCKED` → terminal `BLOCKED` state

The evaluator's blocking findings are forwarded verbatim into the next
revision packet's `PRIOR_FINDINGS`. The parent agent never paraphrases them.

### Bounded revision stage

A bounded revision stage emits a packet that includes the forwarded findings
and sends the worker back to the revision target's work. After the worker
produces a result, the workflow returns to the evaluator that triggered the
revision. The revision loop is bounded by `max_iterations` on the originating
evaluator. When the limit is reached, the run enters `BLOCKED`.

### Gate stage

A gate stage runs deterministic programmatic checks (shell commands) and
transitions based on the collective result:

- All checks pass → `pass_transition` target
- Any check fails → `fail_transition` target (a bounded-revision stage)

Gate commands are run by `tpt` directly, not by an AI worker. The gate
produces a structured result with blocking findings for each failed check.
Findings are forwarded verbatim into the revision packet.

Check commands are argv, not shell command lines. The template is tokenized
before any argument is substituted, and argument values are constrained at
seed time to a conservative shape, so an argument can only ever become a
single argv element. No gate check is ever handed to a shell.

### Terminal states

- `ACCEPTED`: the final stage passes. The final stage is an evaluator, so it
  can also refuse: acceptance is a judgment the workflow can decline, not a
  formality the pipeline makes unfailable.
- `BLOCKED`: an evaluator or worker returns `BLOCKED`, or a stage reaches its
  `max_iterations` in consecutive failures.

## Iteration tracking

Each stage tracks how often it has been entered in `stage_iterations`, and
how many times in a row it has failed in `stage_failures`. The global
`iteration` counter increments on every packet emission for traceability.

A loop is bounded by consecutive failures, not by entries. When a stage's
`stage_failures` reaches its `max_iterations`, the run enters `BLOCKED` and
the result records a `block_reason` naming the stage and the count. A pass
clears that stage's count.

The distinction matters where two loops share a stage. `mechanical-gates` is
re-entered by both `artifact-revision` and `visual-revision`, so counting
entries would let an unrelated visual loop spend the gate's budget and make
the gate's first genuine failure block the run under a misattributed
reason.

## Downstream gate re-entry

When a visual revision triggers a rebuild, the workflow returns to
`build-artifacts` and then re-enters `mechanical-gates` followed by
`visual-evaluation`. This is encoded in the workflow definition by having the
visual revision stage's `next` point to `mechanical-gates`, ensuring all
downstream gates that could have been invalidated are re-run.

## CLI integration

The `tpt` launcher's `dispatch()` function is extended: if the first argument
is not a registered tool and not a launcher option, it is checked against
registered workflow identifiers. If it matches, `tpt` dispatches to the
workflow engine in `scripts/_workflow.py`.

```
tpt proper <proper-id> seed [--provider <p>]
tpt proper <proper-id> advance <run-id> --result <path>
tpt proper <proper-id> advance <run-id> --run-gate
tpt proper <proper-id> status <run-id>
tpt proper <proper-id> replay <run-id>
tpt proper <proper-id> intervene <run-id> --text "..."
tpt proper <proper-id> debt <run-id>
tpt workflow list
tpt workflow show <id>
```

Existing tool dispatch (`tpt <tool> [args]`) is unchanged. Workflow
identifiers are checked only after the tool registry lookup fails, so no
existing tool can be shadowed. A startup check rejects any workflow id that
collides with a registered tool id.

## Identifier collision detection

At engine load time, the set of workflow ids is compared against the set of
registered tool ids. If any id appears in both, the engine refuses to start
with an error. This is deterministic and fails closed.

## Schema validation

Results are validated against schemas in `workflows/schema/`. Validation is
structural and dependency-free:

- Required fields are present.
- Enum fields have valid values.
- `findings` is a list of objects with required sub-fields.
- Malformed or missing results fail closed (exit non-zero, no transition).

No JSON Schema library is used; the validator is a small Python function that
checks the required structure. This keeps the engine dependency-free and
deterministic.

## Workflow debt

Manual interventions are recorded via `tpt proper <id> intervene <run-id>
--text "..."`. The intervention is stored under `interventions/` with:

- `stage`: current stage at intervention time
- `text`: the operator's instruction
- `encoded`: `false` (promoted interventions set this to `true`)

`tpt proper <id> debt <run-id>` lists interventions with `encoded: false`,
showing the workflow debt that has not yet been promoted into a reusable
fragment, evaluator criterion, deterministic gate, or document-specific rule.

Promotion is manual: an operator edits the workflow definition or fragments
and marks the intervention as `encoded`. The engine never auto-promotes.
