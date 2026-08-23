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
- `created_at`: human-readable timestamp (NOT used in packet hashes)

### state.json (mutable)

Updated after every transition. Contains:

- `current_stage`: stage id or `ACCEPTED` / `BLOCKED`
- `iteration`: global iteration counter
- `stage_iterations`: per-stage iteration counts
- `packet_hashes`: list of `{stage, iteration, hash, path}`
- `result_hashes`: list of `{stage, iteration, hash, path}`
- `transitions`: list of `{from, to, disposition, timestamp}`
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
   - `COMMIT`: repository commit
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
- stage id and iteration
- normalized arguments
- forwarded findings (for revision packets)
- all fragment contents in declared order

## Transition semantics

### Linear stage

A linear stage emits a packet, accepts a worker result, and transitions to
exactly one next stage. The result must have `disposition: "PASS"`. Any other
disposition fails closed.

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

### Terminal states

- `ACCEPTED`: the final stage's result has `disposition: "PASS"`.
- `BLOCKED`: an evaluator returns `BLOCKED`, or a revision loop reaches its
  `max_iterations` limit.

## Iteration tracking

Each stage tracks its own iteration count in `stage_iterations`. A revision
loop increments the originating evaluator's iteration count. The global
`iteration` counter increments on every packet emission for traceability.

When an evaluator's `stage_iterations` reaches `max_iterations`, the run
enters `BLOCKED` with a reason of `iteration_limit_exceeded`.

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
tpt proper <proper-id> seed [--provider <p>] [--workflow <id>]
tpt proper <proper-id> advance <run-id> --result <path>
tpt proper <proper-id> advance <run-id> --run-gate
tpt proper <proper-id> status <run-id>
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
