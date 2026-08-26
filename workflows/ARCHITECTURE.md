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
      research.md
      research-synthesis.md
      author-proper.md
      content-evaluation.md
      content-revision.md
      build-artifacts.md
      artifact-revision.md
      visual-evaluation.md
      visual-revision.md
      lanes/                   # one fragment per fan-out lane
        research-*.md
        content-*.md
        visual-*.md
  pipelines/                   # machine-readable workflow definitions
    proper.json
  schema/                      # machine-enforced contracts
    worker-result.json
    research-result.json
    evaluator-result.json
    gate-result.json
scripts/
  _workflow.py                 # workflow engine core (shared module)
tools/
  tpt                          # launcher (extended with workflow dispatch)
  tests/
    test_workflow_determinism.py
    test_workflow_engine.py
    test_workflow_execution_policy.py
    test_workflow_adversarial.py
    test_workflow_seed_idempotency.py
    test_workflow_research_fanout.py
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
    bootstrap.json         # immutable canonical seed response bytes
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
- `bootstrap`: fixed path, format version, and SHA-256 of the exact canonical
  bootstrap bytes

Every load of `state.json` checks it against this manifest and recomputes the
run id from the manifest's own inputs. A hand-edited state, a half-written
state, a run directory renamed or copied under another id, and a missing
manifest are all errors rather than runs that quietly claim to be something
else.

### bootstrap.json (immutable)

The first seed stores the exact UTF-8 JSON bytes that the launcher emits. The
response binds the run id, workflow id/version/source digest, repository
commit, normalized arguments, original stage and iteration, initial packet
hash and repository-relative path, and the exact controller instructions. Its
serialization is canonical and ends in one LF; it contains no timestamp,
absolute checkout path, hostname, user, process id, or environment-derived
formatting.

An identical later `seed` loads state and the bound workflow, verifies the
manifest bootstrap hash, the canonical response, and the recorded initial
packet, then writes the already-verified bytes directly to stdout. It never
derives seed output from current mutable state and never writes a packet,
event, result, transition, counter, or state. Consequently the response remains
byte-identical after any amount of run progress.

Missing bootstrap evidence is not reconstructed. A pre-fix run remains usable
through `status`, `replay`, and `advance`, but `seed` reports that the run
predates replayable bootstrap evidence. Corrupt evidence and workflow-source
or identity mismatches likewise fail closed.

### state.json (mutable)

Updated after every transition. Contains:

- `workflow_id`, `workflow_version`, `workflow_digest`, `repo_commit`,
  `normalized_args`: copied from the manifest and checked against it
- `current_stage`: stage id or `ACCEPTED` / `BLOCKED`
- `iteration`: global iteration counter
- `stage_iterations`: per-stage packet counts
- `stage_failures`: consecutive failures per evaluator/gate, reset on a pass
- `packet_hashes`: list of `{stage, iteration, hash, path}`; a fan-out
  stage's record also carries a `lanes` list of `{lane, index, hash, path}`
  in canonical lane order
- `result_hashes`: list of `{stage, iteration, hash, path, disposition}`; a
  fan-out stage's record also carries a `lanes` list of
  `{lane, index, hash, path, disposition}` in canonical lane order
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
   - `EXECUTION`: the stage's execution policy — `single`, `program`, or
     `fanout/host-max`
   - `LANES`: the stage's lane ids in canonical order as compact JSON, on a
     fan-out stage's packets only
   - `LANE`, `LANE_INDEX`: the lane's own id and canonical index, on a lane
     packet only
   - `ARGS`: normalized arguments as sorted JSON
   - `PRIOR_FINDINGS`: findings forwarded from the preceding stage — an
     evaluator's or gate's blocking findings into a revision packet, or a
     linear fan-out stage's joined lane findings into its successor's packet,
     and empty otherwise — serialized as sorted JSON on one line
4. **Assemble**: join header and fragments with a fixed separator.
5. **Encode**: UTF-8, no BOM, LF line endings.
6. **Hash**: SHA-256 of the exact bytes.

Compilation writes nothing. The compiled bytes are written to
`packets/<stage>-<iteration>.txt` by the commit that also records the state
they belong to, so a packet exists if and only if the run reached it.

### Workflow-source digest

The digest covers the canonicalized pipeline JSON plus the bytes of every
fragment and schema the pipeline references. It therefore covers the parts of
the guidance no packet quotes: transitions, iteration limits, gate commands,
result contracts, and the parts of an execution policy no single packet
carries — a fan-out stage's declared join, and the fragments of every lane
but the one a given lane packet quotes.

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
- the stage's execution policy, and a fan-out stage's lane roster in
  canonical order
- a lane packet's own lane id and canonical index
- normalized arguments
- forwarded findings, for a revision packet and for the successor of a linear
  fan-out stage
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

A result becomes part of the run only when the transition it produced is
committed. Until then it is a file the operator happens to have on disk: the
engine reads it, and copies it into `results/` and its hash into
`result_hashes` only alongside the state that acts on it.

Gate results are produced by the engine and carry the same two fields.

## Execution policy

Every stage declares, as workflow data, how its work is dispatched. The
`execution` object is required on every stage and validated by
`_validate_execution`:

- `{"mode": "single"}` — exactly one fresh subagent runs the stage, and the
  object declares nothing but `mode`.
- `{"mode": "program"}` — `tpt` runs the stage itself. It is required on every
  `gate` stage and permitted on no other: a gate whose result the engine
  composes from checks it ran may not have a subagent standing between it and
  those checks.
- `{"mode": "fanout", "parallelism": "host-max", "join": "strict-union",
  "lanes": [...]}` — exactly those four keys. `parallelism` must be
  `host-max`, `join` must be `strict-union`, and `lanes` declares at least two
  lanes, each an object with an `id` and optionally its own `fragments`. Lane
  ids are nonempty lowercase-kebab strings, unique within the stage. One lane
  would be a `single` stage, so two is the minimum.

Before this, the host decided whether a stage ran as one subagent or as five of
its own invention, and nothing in the run recorded which had happened. What
work is dispatched to whom is the decision the engine exists to own, so it is
workflow data now: covered by the workflow-source digest and named in every
packet's `EXECUTION` line. The host's one remaining choice is how many lanes
run at once.

### Which mode a stage gets

What a stage does to the repository decides how it is dispatched:

```
independent discovery    -> host-max fan-out
single synthesis owner   -> single
authoritative mutation   -> single
independent evaluation   -> host-max fan-out
programmatic validation  -> program
```

Fan-out is the mode for work that mutates nothing: lanes that only discover or
only judge write no artifact a sibling could conflict over, so the only cost of
running them at once is host capacity. Everything that writes — authoring,
revision, retrieval, and the one stage that integrates many lanes into one
brief — is `single`, because an authoritative artifact has exactly one owner at
a time and a synthesis reconciled by two agents is two syntheses. Checks a
program can run are `program`, so no agent stands between the engine and the
output it hashes into guidance.

The rule is about the work, not the stage type. `research` is a linear stage
that fans out and `content-evaluation` is an evaluator that fans out; both are
read-only, which is why both may.

### Lanes and lane packets

A lane is a workflow-defined share of one stage's work, and canonical lane
order is declaration order. `_stage_lanes` returns that list, and it is the
only order anything downstream uses — lane packets, lane results, the join, and
the successor packet all read it, and nothing reads the order lanes happened to
finish in.

`_compile_stage_packets` compiles the stage's own packet and then one packet
per lane, in canonical order, so lane ids, lane ordering, lane packet bytes,
and lane hashes are all fixed before any agent is launched. A lane packet
carries the stage's `EXECUTION` and `LANES` header lines plus its own `LANE`
and `LANE_INDEX`, and its body is the stage's fragments followed by that lane's
own fragments. Lane packets are written to
`packets/<stage>-<iteration>-lane-<index>-<lane-id>.txt` and lane results to
`results/<stage>-<iteration>-lane-<index>-<lane-id>.json`, keyed by lane
identity rather than by arrival, so an auditor reads which lane produced which
bytes without knowing when it finished.

Nothing host-varying reaches lane packet bytes: no worker process id, no launch
or completion timestamp, no scheduler slot, no completion order. Lane identity
comes from the workflow, so a host that runs every lane at once and a host that
runs them one at a time compile the same lane packets, byte for byte, and
record the same hashes.

### Fail-closed lane binding

A fan-out stage is advanced with one `--lane-result <lane-id>=<path>` per
declared lane. `_load_and_validate_lane_results` refuses, with the run
untouched: a lane the stage does not declare, a second result for a lane
already answered, a result whose own `lane` field disagrees with the flag that
carried it, a `lane_packet_hash` other than the one emitted for that lane, and
any declared lane left unanswered. Every declared lane is required — the
controller does not get to judge whether a missing lane was good enough. Each
lane result is also checked against the stage's schema and must name the packet
it answers, like any other result.

The flags are not interchangeable. `--result` on a fan-out stage is refused,
`--lane-result` on a `single` stage or on a gate is refused, and `--run-gate`
on anything but a gate is refused. The stage's declared policy, not the
operator's choice of flag, decides how the stage is answered.

### The strict-union join

`_join_lane_results` is the engine's own reduction over the lane results. The
parent controller is never asked to summarize several lane results into the
next prompt — a summary is guidance, and guidance is the engine's. The join:

- copies each lane's findings verbatim, adding a `lane` key naming the lane
  that raised them, and concatenates them in canonical lane order;
- takes as the joined `disposition` the worst any lane returned, by the fixed
  rank `PASS` < `CHANGES_REQUIRED` = `FAIL` < `BLOCKED`;
- writes as the joined `summary` a deterministic roll-call of
  `lane=disposition` in canonical lane order; and
- records a `lanes` list of each lane's id, canonical index, disposition, lane
  packet hash, and lane result hash.

The joined object is the stage's own result. It takes the stage's transition,
is written to `results/<stage>-<iteration>.json`, and is hashed into
`result_hashes` like the result of any other stage, with the lane results it
was built from written and hashed beside it. The engine composes it rather than
accepting it, so what the stage's schema governs is each lane's submission,
checked before the join. Blocking findings forwarded into a revision packet
keep their `lane` key, so the reviser reads which lane raised each one.

Nothing in the join reads completion order, so lanes finishing C, A, D, B join
exactly as A, B, C, D and the successor packet's bytes are the same either way.
That is why the join is the engine's: were it the controller's, the order its
agents happened to return in would be an input to the next packet that no
recorded state could reproduce, and the run's central invariant would hold only
by the host's good manners.

### Lane evidence

Lane packets and lane results are part of the run's record, and what reads the
record reads them too. `_verify_recorded_lane_files` requires every recorded
lane file to be present, named exactly as its lane id and canonical index
imply, not a symlink, and still hashing as recorded.
`_verify_lane_packet_evidence` compares a recorded lane roster against what the
bound workflow compiles now, so a lane renamed, reordered, added, or dropped
under a live run is an error rather than a run whose results answer packets
nobody can recompile; a seed replay checks the initial packet's roster that
way. `replay` recompiles the lane packets along with the stage's own and
reports a `lanes` list of
`{lane, index, last_recorded_hash, recompiled_hash, deterministic}`, and its
top-level `deterministic` is false if any lane diverges. Acceptance reads the
same evidence — see the audit conditions below.

### Controller guidance

`_driver_instructions` opens with the stage's policy, stated as `EXECUTION
POLICY: SINGLE`, `EXECUTION POLICY: FANOUT / HOST-MAX`, or `EXECUTION POLICY:
PROGRAM GATE`, so a controller is told what to dispatch rather than left to
infer it. The fan-out form lists every lane in canonical order with its packet
path and `lane_packet_hash`, gives the exact `advance` command with one
`--lane-result` flag per lane, and tells the host to run as many lanes at once
as it supports, up to all of them; where host capacity is lower than the lane
count, the lanes are taken in canonical order, one batch at the host maximum at
a time. Batching changes no lane id, no lane order, and no lane packet byte.

The same instructions forbid inventing, omitting, combining, or subdividing
lanes, and forbid the controller summarizing, merging, reordering, editing, or
supplementing any lane's work. A lane that cannot do its work returns `BLOCKED`
in its own structured result, and the workflow decides what that means. For the
seed stage these instructions are part of the canonical bootstrap bytes, so the
policy the first controller is given is as fixed as the packet it accompanies.

## Transition semantics

### Linear stage

A linear stage emits a packet, accepts a worker result, and transitions to
exactly one next stage. `disposition: "PASS"` advances it. A worker that could
not do the work reports `disposition: "BLOCKED"`, which is terminal: the engine
has no other way to tell finished work from unfinished. Any other disposition
fails closed.

A linear stage may fan out. When one does and the join's disposition is `PASS`,
`_extract_prior_findings` forwards the joined lane findings verbatim and in
full into the successor's `PRIOR_FINDINGS`, in canonical lane order, each
keeping the `lane` key the join gave it. Those findings are the whole of what
the stage produced: read-only lanes write no artifact between them, so the
joined result exists only inside the run, and the successor is the only place
it can go. Forwarding it is what makes the integrating worker's material the
engine's own join rather than something a controller retyped. An evaluator's
`PASS` still forwards nothing, because there `PASS` means there was nothing to
report.

A fan-out linear stage's lanes answer to the same two dispositions the stage
itself has. `research-result.json` accepts `PASS` and `BLOCKED` and no third
value: a lane either did its sweep — recording what it did not find as a finding
like anything else — or could not, and a linear stage's `BLOCKED` ends the run.
There is no `CHANGES_REQUIRED` because such a lane judges nothing and sends no
one back to revise.

### Reconstructing forwarded findings

Whatever `_extract_prior_findings` put in a packet has to be rebuildable from
the record alone, or a replay of that packet would recompile different bytes
than the run emitted. `_load_prior_findings_for_current`, which `replay` uses,
rebuilds it: if the last transition came from a linear fan-out stage that
passed, it re-reads that stage's recorded joined result; if the current stage is
a bounded revision, it walks back to the evaluator or gate result that triggered
the revision.

Both paths read through `_read_recorded_result`, which fails closed when the
recorded result file is missing or no longer hashes to what was recorded. A
packet whose forwarded findings cannot be reconstructed is an error, never a
packet recompiled without them.

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
Findings are forwarded verbatim into the revision packet. A gate declares
execution mode `program` and may declare no agent mode, and no other stage
type may declare `program` — the stage type and its execution policy have to
agree about who runs the work.

### Terminal states

- `ACCEPTED`: a gate stage whose `pass_transition` is `ACCEPTED` ran its checks
  and every one of them passed, and the run's own record satisfies the
  acceptance audit below.
- `BLOCKED`: an evaluator returns `BLOCKED`, a worker returns `BLOCKED`, or a
  revision loop reaches its `max_iterations` limit.

Both are final: the engine refuses any further `advance` on a terminal run.

## Acceptance

Acceptance is the engine's decision, and only a gate stage may name it.
`_validate_workflow` rejects a workflow in which a linear or evaluator stage
transitions to `ACCEPTED`, because such a stage would let an agent's own
`disposition: "PASS"` end the run — an AI attesting that the work it was asked
to produce is acceptable. It also rejects a workflow from which `ACCEPTED` is
unreachable.

Before recording `ACCEPTED`, `_verify_final_acceptance` re-reads the run's
record and refuses acceptance unless:

- the accepting stage is a gate whose checks all passed just now;
- every other evaluator and gate stage that ran last recorded `PASS`;
- every recorded result file is still present and still hashes to the digest
  recorded when it was accepted;
- no stage's latest result carries a blocking finding;
- every recorded packet file is present and unaltered; and
- every recorded lane packet and lane result file is present and still
  hashes to what was recorded.

A gate's checks speak only for the artifacts they inspect. The audit is what
makes acceptance mean the whole run passed, and it reads only files the engine
itself wrote and hashed, so editing a result or deleting a packet cannot buy an
acceptance — it prevents one.

## The advance transaction

An `advance` either completes or leaves the run exactly as it was. The engine
validates the submitted result, decides the transition against a copy of the
state, and compiles the successor packet, all without writing anything. Only
then does `_commit` write, in order: the successor packet and, where the
successor is a fan-out stage, its lane packets; the accepted result, and the
lane results a joined one was built from; and last of all the state file,
replaced atomically through a temporary file in the same directory.

Two properties follow, and the adversarial suite holds them:

- A refused submission leaves no trace. A result that is malformed, answers a
  packet the run has moved past, names another stage, duplicates one already
  recorded, or carries a disposition the stage does not admit is never written
  to `results/` and never hashed into `result_hashes`. Nothing downstream can
  read it, and `replay` is unaffected. A refused fan-out submission leaves no
  authoritative trace either, and no lane's result becomes part of the run
  because another lane's was acceptable.
- A run never advances past a packet it could not emit. If the successor packet
  cannot be compiled or written, the stage, iteration counters, transitions,
  packet and result records, and disposition are all untouched, and the result
  that was submitted is not authoritative. The operator repairs the cause and
  submits the same result again; the retry emits the byte-identical packet.

Seeding uses `state.json` as its publication marker. One per-run creation lock
under `build/tpt-seed-locks/` selects a single creator; that creator prepares
the manifest, initial packet, canonical bootstrap, and initial event evidence
before writing state last. A seed that fails before state publication removes
its unpublished directory and leaves no run to resume. A process interruption
can leave an incomplete, unpublished directory; a later seed fails closed until
an operator deliberately discards it. Concurrent or later identical callers
verify and replay the published bootstrap without appending duplicate evidence.

A commit that fails midway can leave a packet file, or a packet and a result
file, that the state does not reference. Nothing reads a file the state does not
record, and a successful retry rewrites both byte for byte.

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
tpt proper <proper-id> advance <run-id> --lane-result <lane-id>=<path> ...
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
