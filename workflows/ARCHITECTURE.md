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
- `workflow_digest`: digest of the workflow source the run is bound to
- `repo_commit`: repository commit SHA at seed time
- `normalized_args`: sorted, string-valued argument map
- `created_at`: human-readable timestamp (NOT used in packet hashes)

Every load of `state.json` checks it against this manifest and recomputes the
run id from the manifest's own inputs. A hand-edited state, a half-written
state, a run directory renamed or copied under another id, and a missing
manifest are all errors rather than runs that quietly claim to be something
else.

### state.json (mutable)

Updated after every transition. Contains:

- `workflow_id`, `workflow_version`, `workflow_digest`, `repo_commit`,
  `normalized_args`: copied from the manifest and checked against it
- `current_stage`: stage id or `ACCEPTED` / `BLOCKED`
- `iteration`: global iteration counter
- `stage_iterations`: per-stage packet counts
- `stage_failures`: consecutive failures per evaluator/gate, reset on a pass
- `packet_hashes`: list of `{stage, iteration, hash, path}`
- `result_hashes`: list of `{stage, iteration, hash, path, disposition}`
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
   Read each file from `workflows/fragments/` in the declared order, and
   substitute `{argument}` placeholders from the run's normalized arguments.
   A packet is the whole instruction; nothing in it is left for a worker to
   interpolate.
3. **Build header**: a deterministic preamble containing:
   - `WORKFLOW`: workflow id and version
   - `WORKFLOW_DIGEST`: digest of the workflow source (below)
   - `COMMIT`: repository commit
   - `STAGE`: stage id
   - `ITERATION`: iteration number for this stage
   - `ARGS`: normalized arguments as sorted JSON
   - `PRIOR_FINDINGS`: forwarded findings from the last evaluator/gate result
     (empty for non-revision stages), serialized as sorted JSON on one line
4. **Assemble**: join header and fragments with a fixed separator.
5. **Encode**: UTF-8, no BOM, LF line endings.
6. **Hash**: SHA-256 of the exact bytes.
7. **Write**: to `packets/<stage>-<iteration>.txt`.

### Workflow-source digest

The digest covers the canonicalized pipeline JSON plus the bytes of every
fragment and schema the pipeline references. It therefore covers the parts of
the guidance no packet quotes: transitions, iteration limits, gate commands,
and result contracts.

A run records the digest at seed time, in both the manifest and the state, and
every `advance` and `replay` recomputes it. If the workflow source has changed
since the run was seeded, the run fails closed rather than continuing under
guidance it never started with. A changed workflow means a new run.

### Hashing boundary

The hash covers the packet bytes only. It does NOT cover:
- the run_id (unique per run, not per state)
- timestamps (nondeterministic)
- filesystem paths (machine-specific)
- the state file itself (contains timestamps)

The hash DOES cover:
- workflow id and version, and the workflow-source digest
- repository commit
- stage id and iteration
- normalized arguments
- forwarded findings (for revision packets)
- all fragment contents in declared order, with arguments substituted

Gate findings quote what a check printed, so that output is hashed guidance.
It is made portable first: the repository root and home directory are replaced
with `<repo>` and `<home>`, line endings normalized, trailing whitespace
dropped. The untouched output of every check is kept under the run's
`gate-logs/`, which nothing hashes.

Host-varying output a check itself emits — a wall-clock time, a random
temporary path outside the repository — would still reach the packet. Gate
commands should not print such things.

## Every result answers one packet

A result must repeat the `stage` and `iteration` of the packet the engine last
emitted. The engine rejects anything else. Without that binding it could not
tell a fresh result from the previous one resubmitted, from a result produced
for another stage, or from one written before the run advanced — and each of
those would move the run without a worker having done the stage's work.

Gate results are produced by the engine and carry the same two fields.

## Transition semantics

### Linear stage

A linear stage emits a packet, accepts a worker result, and transitions to
exactly one next stage. `disposition: "PASS"` advances it. A worker that could
not do the work reports `disposition: "BLOCKED"`, which is terminal: the engine
has no other way to tell finished work from unfinished. Any other disposition
fails closed.

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
- `BLOCKED`: an evaluator returns `BLOCKED`, a worker returns `BLOCKED`, or a
  revision loop reaches its `max_iterations` limit.

## Iteration tracking

Each stage tracks its own packet count in `stage_iterations`; the global
`iteration` counter increments on every packet emission for traceability.
Neither bounds a loop.

`max_iterations` bounds *consecutive failures* of one evaluator or gate,
recorded in `stage_failures` and reset whenever that stage passes. Counting
visits instead let a stage spend its own budget on success: a run that
re-entered `mechanical-gates` three times on its way around the visual
revision loop was blocked by that gate's first real failure, with no revision
attempted.

## Downstream gate re-entry

A visual revision's `next` points at `mechanical-gates`, not at
`visual-evaluation`: every visual change re-enters the mechanical gates, and
only a passing gate returns to visual evaluation. The reviser rebuilds, and the
gate's own commands rebuild again and check the result, so no visual change can
reach acceptance without the mechanical invariants being rechecked on the
artifacts that changed.

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
existing tool can be shadowed.

Every command after the first names the document as well as the run. The
document is checked against the run's own arguments — the run id alone
identifies a run, so a stale or mistyped document id used to act on whatever
run the id pointed at.

## Identifier collision detection

Before any dispatch, and again under `tpt --check`, the set of workflow ids is
compared against the set of registered tool ids. If any id appears in both, tpt
refuses to run rather than silently resolving the name to the tool and leaving
the workflow unreachable.

## Schema validation

Results are validated against schemas in `workflows/schema/`. Validation is
structural and dependency-free:

- Required fields are present, including the `stage` and `iteration` naming the
  packet answered.
- Enum fields have valid values.
- `findings` is a list of objects with required sub-fields.
- Malformed, missing, stale, duplicate, and wrong-stage results fail closed
  (exit non-zero, no transition).

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
