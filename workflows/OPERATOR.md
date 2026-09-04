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

The reasoning effort is declared too, and is not one of your choices. Each
agent stage or lane resolves to a level — `low`, `medium`, `high`, `xhigh` or
`max` — which `tpt` prints in the instructions and carries in the packet's
`EFFORT` header line. Dispatch each agent at the level named for it, and change
a level by changing the workflow rather than the invocation: the level is
hashed into the packet, so a run answered at some other level is not the run
its record describes. A program gate names none, because no agent runs it.

### Single

`EXECUTION POLICY: SINGLE`. Start exactly one fresh subagent at the reasoning
effort the instructions name, give it exactly the packet contents, and advance
with the result it returns:

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
canonical order with its own packet path, `lane_packet_hash`, and reasoning
effort. Start one fresh subagent per listed lane and none besides, each at its
own lane's effort — lanes of one stage need not share a level, and running them
together is no reason to level them — give each exactly the contents of its own
lane packet, and require one structured JSON result per lane. Then advance with
one `--lane-result` flag per lane:

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

#### Accounting for the findings you were given

A stage that declares `reports_repairs` in the pipeline, and whose packet's
`PRIOR_FINDINGS` header carries blocking findings, must on `PASS` say what
became of each one:

```json
{
  "stage": "content-revision",
  "iteration": 1,
  "disposition": "PASS",
  "summary": "One or two sentences.",
  "artifact_path": "src/claude/.../main.tex",
  "finding_dispositions": [
    {"id": "CON-PRO-002", "outcome": "repaired"},
    {"id": "CON-CIT-021", "outcome": "not-repaired",
     "note": "why it could not be cleared"}
  ]
}
```

Every forwarded blocking finding appears exactly once, and no others. A result
that omits one is refused, because a dropped finding reads exactly like a
repaired one and the engine would score an abandoned defect as progress. The
engine holds the stage to the blocking ids it recorded when it routed them
there, so a report naming an id it did not forward is refused too.

`reports_repairs` is declared per stage — on the five bounded-revision stages
of both propers pipelines and nowhere else — because not every repairing stage
can make the report. A fan-out `research` re-entry receives blocking findings
and returns a result the engine composed by joining its lanes: no agent wrote
it and no lane can speak for the whole, and requiring the report there failed
every research re-entry unconditionally. `research-synthesis` returns an
evaluator shape, whose schema defines no such field. Where a stage cannot
report, its findings' owner keeps the id comparison described under Iteration
bounds below; the report displaces that heuristic exactly where it exists.

Two things the engine does not enforce, whatever a fragment asks for. A stage
handed no blocking findings has nothing to report and the check returns before
reading the field, so a `finding_dispositions` volunteered there is accepted
and ignored — a first authoring pass is not a failed repair, and the run's
budget never sees the report. And the field's shape is validated by schema
rather than by stage, so any stage returning the worker shape may carry it
without refusal, reporting or not.

`not-repaired` is a legitimate outcome and is not a failure of the worker. On
a stage that reports, it is the only way the engine learns that the stage has
stopped converging — see Iteration bounds below — and the mechanism depends on
revisers using it rather than claiming repairs they are not confident in. One
production's central defect survived three rounds precisely because each round
reported it repaired.

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

#### Observations: what a lane saw and its criteria do not reach

An evaluator result may carry, beside its findings, entries whose schema
defines `observation_fields` — `content-evaluation` and the other evaluators,
never a worker stage or a research lane:

```json
{
  "observations": [
    {"location": "sections/50-interpretive.tex P4",
     "note": "carries no 'what the element-by-element reading misses' field"}
  ]
}
```

An observation has no severity and routes no repair. It exists so that a real
defect a lane saw outside its own criteria reaches the run at all. Before it,
the only route from a lane to the record was the driver writing a finding of
its own, which the fan-out policy forbids — so in one production four genuine
defects, in three classes, were located by max-effort lanes, correctly
declined by every lane that saw them, and lost. `tpt` joins observations in
canonical lane order like findings, and the stage that records standing
findings writes them to the tracked record beside them.

An observation is not a way around lane ownership. A class of defect that
keeps appearing in observations is a fragment that needs to give some lane the
criterion.

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

The retry loop is bounded by this stage's own `max_iterations`. No stage on
its route reports what it repaired, so what charges that budget is a blocking
finding id this stage already had standing from its previous failure — see
Iteration bounds below — and the third such failure blocks the run, which
`advance` reports as `iteration limit exceeded for research-synthesis: 3/3
failures that did not converge`. A `PASS` resets the count. The budget is this
stage's alone: `content-evaluation` has its own, and a run that evaluator sends
back to `research` spends nothing here.

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

## Iteration bounds

A looping stage carries two budgets, and they answer different questions.

`max_iterations` bounds **repair that was attempted and failed**. What charges
it is a repair report: where the stage that this stage's findings were routed
to declares `reports_repairs` and returned at least one finding as
`not-repaired`, the failure that follows costs an iteration. Repairs that
succeeded cost nothing, and neither do fresh findings raised against a changed
document — that is progress, and permitting it is what the budget exists for.
The first failure of a streak is charged whatever happens, because it has no
repair report behind it and because exempting it would loosen every declared
limit by one.

**Where no report exists the budget still compares finding ids, and that is
deliberate.** It reads the blocking ids this stage has just raised against the
ids it had standing from its previous failure, and charges the budget when any
of them repeat. That is what happens wherever the stage a failure's findings
were routed to does not declare `reports_repairs`: two of
`content-evaluation`'s three repair routes, `research` and `brief`, whose
repairing stages cannot supply a report; `research-synthesis`, whose failure
re-enters the `research` fan-out; and every gate. Deleting the comparison there
would leave such a stage bounded by
`max_total_iterations` alone, silently doubling every limit an operator
declared. Ground truth displaces the heuristic exactly where it exists and
nowhere else, and the way to retire it for a route is to make that route's
repairing stage able to report, not to remove the only bound it has.

**A gate keeps the id comparison whatever its reviser reports**, and there it
is not a heuristic at all. What makes an id untrustworthy is that an AI
evaluator mints it for its own report and cannot know which ids an earlier
iteration used. A gate's ids belong to a program: the id is a check id, the
same check refusing the same leaf produces it again, and a repeat means the
tool re-ran and refused again after a repair was claimed. That is better
evidence of a loop than the claim is of progress, and it is the one place a
reviser's word should not displace a measurement.

`max_total_iterations` bounds **consecutive failures** whatever they name, and
defaults to twice `max_iterations`. It is the bound that catches an optimistic
reviser, which is the failure mode this design accepts in exchange for never
again scoring a fresh defect as an unrepaired one. `content-evaluation`
declares `max_iterations: 4` in `proper.json`, so its ceiling there is eight;
it declares 3 in `proper-finish.json`, so its ceiling there is six.

Both counters, and the standing ids the comparison reads, reset when the stage
passes. `advance` names which bound stopped a run: `N/M failures that did not
converge` is the repeat budget, and `N/M consecutive failures` the absolute
ceiling.

## Run state directory

Each run has a state directory, and nothing about it is durable:

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

`.gitignore` line 1 is `/build/`, `make clean` is `rm -rf build`, and in a
`wt` agent workspace `wt tidy` deletes everything the clone ignores, without
asking. No run state has ever been tracked, and none of it survives a routine
cleanup. Read this directory as the working notes of a run in flight, never as
a record anything later may depend on.

What stands against the document itself has a tracked home instead. The stage
that declares `records_standing_findings` — `content-evaluation`, in both
propers pipelines, and no other stage — writes the blocking findings still
standing against the leaf, and the observations its lanes recorded, to

```
<document_root>/evaluations/blocking-findings-v1.toml
```

rewritten whole each time, so it states what stands now rather than
accumulating history. A `PASS` writes an empty list rather than deleting the
file: "this leaf was evaluated and nothing stands" and "nobody has looked" are
different facts. It is written before the run's commit, so a write that fails
aborts the advance and the obvious retry works; and it is written on a
terminal transition too, which is the case it exists for, a run that blocks
being a run whose findings have nowhere else to go. The declaration is per
stage because every evaluator used to write this path: a `web-evaluation`
asking for changes replaced the leaf's content findings with findings about
generated HTML.

**Nothing reads it back.** It is a record for a person, and the format such a
record has. Carrying a previous production's standing findings into a new run
automatically is still owed, and it is owed somewhere the run's identity can
cover it, because this file is untracked working-tree state that no
`repo_commit` moves with and no `workflow_source_digest` covers. Two designs
would do it: an operator subcommand whose output is committed, so that
`repo_commit` carries the findings the way it carries everything else a run is
bound to; or the record's own hash in `compute_run_id` and in the acceptance
audit, so that a run seeded against one set of standing findings is a
different run from one seeded against another. Reading the file at seed
without either was tried and backed out — it broke seed idempotency, which
`tpt proper seed` promises in terms and a whole test suite protects, because
the pristine recompile that verifies a re-seed knew nothing about the extra
argument.

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

No timestamp, and no absolute or machine-specific path, appears in the hashed
packet material. What determines the packet bytes is the workflow source
(definition, fragments, schemas), the repository commit, the stage, the
iteration, the stage's execution policy and lane identity, the reasoning
effort, the normalized arguments, the repo-relative `DOCUMENT_ROOT` the
workflow's own template resolves from them, the repair owners the stage's
schema admits, and the forwarded and carried findings.

Two of those are worth saying plainly, because a reader who expects them
excluded will be wrong. `RUN_ID` is in the header and is hashed: it is the
engine's own digest of the workflow, version, seed commit and normalized
arguments the header already carries, so it restates hashed bytes rather than
adding an input, and it is there because a worker that must record what
produced the document it is writing cannot otherwise read the run off its
packet. `DOCUMENT_ROOT` is a path, and it is hashed: it is repo-relative and
built from the arguments, so it varies with the run's identity and never with
the machine.

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
lane is told which questions belong to the other six. `research-synthesis`
bounds its repeat loop at three; `content-evaluation` bounds its three-owner
repair loop at four from version 22. `research` has no revision loop of its own
— a lane that cannot sweep returns `BLOCKED` and the run stops, and a re-entry,
whether routed from `content-evaluation` or sent back by
`research-synthesis`, is a fresh visit to the stage on the budget of the
evaluator that sent it.

The `proper` workflow is at version 23. The `proper-finish` workflow is at
version 2.
**Neither number is in the file yet: this entry is written against the versions
this change requires, and the bump to `workflows/pipelines/proper.json` and
`workflows/pipelines/proper-finish.json` is outstanding.** Until it lands, a
changed definition is running under a version that already names something
else, which is the one thing the digest rule exists to prevent.

Version 23 is what runs `ca03f1b357e7ec25` and `90dcdddcb6780e60` asked for,
and it changes the content loop in five places.

Both pipelines declare `document_root`, `src/{provider}/{proper}`, and the
packet header carries the resolved path as `DOCUMENT_ROOT`, where the hash
covers it. The arguments already decided that path, and a worker asked to
assemble it from `ARGS` makes one inference too many where a leaf of the same
name exists under more than one provider: a max-effort evaluation lane swept
`src/gpt/...` to completion against a packet reading `"provider": "claude"`,
and an unrelated `git status` is what caught it.

The five bounded-revision stages declare `reports_repairs` and return
`finding_dispositions`, one entry per blocking finding they were given,
`repaired` or `not-repaired`. That is what the repeat budget reads where it
exists; Iteration bounds above says what still reads finding ids and why. The
declaration is per stage because not every repairing stage can make the
report — a fan-out `research` re-entry returns a result the engine composed
from its lanes, and no agent wrote it.

`content-evaluation` declares `records_standing_findings` and writes the
blocking findings and observations standing against the leaf to
`<document_root>/evaluations/blocking-findings-v1.toml` after each evaluation,
terminal ones included. Only that stage writes it: every evaluator used to, so
a `web-evaluation` asking for changes could replace a leaf's content findings
with findings about generated HTML. Nothing reads the file back into a run.
Carrying it forward is owed work, on the terms the run-state section above
sets out.

`content-preflight` gains `house-voice` and `proposal-fields`, making eleven
checks. Both are prose screens and both sit in the gate rather than in the
evaluation behind it because the evaluation demonstrably cannot afford them:
three successive max-effort evaluations of one leaf spent an entire iteration
budget draining the house-voice class one layer at a time, and a proposal that
substituted a heading of its own for one the profile fixes was located by four
separate max-effort sweeps and reported by none, because it sat between two
lanes' criteria.

Evaluator results may carry `observations`, and the content lanes gain owners
for three classes that had none: the mandated proposal fields to criterion 5,
stated counts to criterion 7 — now "Citations and stated counts" — and the
appointed Latin's orthography against `propers/verified.md` to criterion 2.
Criterion 12's scope ambiguity is settled in favour of its governing sentence,
with the enumerated sections demoted to a checklist that is explicitly not the
boundary.

`proper-finish` version 2 takes the same `document_root`, the same two
preflight checks, the same five `reports_repairs` declarations and the same
`records_standing_findings` on its own `content-evaluation`. A run seeded
against `proper` version 22 or `proper-finish` version 1 fails closed and is
seeded again.

The `proper` workflow was at version 22. Version 22 gives
`content-evaluation` four repeat-budget slots for its three ordered repair
owners. The first failed evaluation spends one slot before any repair owner has
run, so the former ceiling of three could stop a defect before its third owner
was dispatched. Run `ce4ecd514b64d2f9` demonstrated the failure: its fourth
content evaluation found that research had supplied the evidence requested by
`CON-CIT-007` and assigned the remaining bibliography correction to
`authoring`, but the evaluator reached 3/3 repeats before `tpt` could take the
declared route to `content-revision`. Four retains a hard repeat bound while
admitting the initial finding and one visit to each declared owner. The
regression replays that run's four evaluation results and requires the fourth
to emit the authoring packet rather than `BLOCKED`. A run seeded against
version 21 or earlier fails closed; seed it again.

The `proper` workflow was at version 21. Version 21 closes the citation-handoff
gap proved by run `dae51f4a7715c7f9`. The cultural-afterlife lane had gathered
exact titles, institutions, stable URLs and loci for the retained online
witnesses. Synthesis reduced those records to generic labels in the immutable
brief while directing the author to carry stable links "from this brief". The
citation evaluator then combined leaf omissions with those absent brief values
in one `authoring` finding and said the brief held details it did not hold. The
author correctly refused to retrieve around its immutable input and the run
ended `BLOCKED`.

The cultural lane now returns a complete citation bundle for every retained
online witness and corroborant; synthesis must preserve each bundle in
`research/scope.md` and compare it with the lane finding before `PASS`;
content evaluation must find every requested value in the brief before naming
`authoring`, and must split a mixed evidence-and-leaf defect by repair owner.
The regression checks both the source fragments and the packets workers
receive. A run seeded against version 20 or earlier fails closed; seed it
again. A terminal v20 run is evidence, not a resumable v21 run.

The `proper` workflow was at version 20. Version 20 closes the fresh-leaf gap in
`resolve-context`. That stage runs before `source-audit`, which is ordinarily
the first stage to create a new provider leaf. Version 19 invoked
`proper-chronology record --write` while the leaf did not exist, treated the
writer's refusal as an answer, and could report `PASS`; `source-audit` then
created the leaf, leaving `research/chronology.toml` absent until
`research-synthesis` correctly stopped the run.

`resolve-context` now creates `src/<provider>/<proper>/research/` before
invoking the chronology writer and verifies that the generated record exists.
Directory creation, writer refusal, and a missing record are required-work
failures: the stage returns `BLOCKED`, never `PASS`. The regression starts
with no provider leaf, materializes only that directory, runs the real writer,
and proves the record can be created. A run seeded against version 19 or
earlier fails closed; seed it again.

The `proper` workflow was at version 19. Version 19 told the content evaluation
that the leaf builds two documents. It always had: `main.tex` builds the
canonical guide, `synthesis.tex` builds the synthesis edition beside it, and
which prose reaches which reader is decided by `\ifdefined` branches and by
section files only one of them inputs. The visual evaluator was told this from
the beginning — its inspection method says in as many words to inspect both the
canonical and synthesis PDFs — and the content evaluator was told the opposite
by omission, being sent to read "the canonical proper leaf".

Run `ca03f1b357e7ec25` shows the cost. Three content evaluations across five
lanes read the canonical build, raised findings against sections by name, and a
reviser repaired the file each finding could be read as naming. The same claims
stood uncorrected in the synthesis edition's own section files, which no lane
had opened, and nothing downstream would have caught it: the mechanical gates
measure rendered pages, and both editions render.

Two rules answer it, and neither is a hint. `content-evaluation` now opens with
how to find out what a leaf builds — list the top-level `.tex` files, follow the
inputs and the branches both ways, and write down what each document puts in
front of a reader — and requires every finding to name the file the defect is
in rather than the section it belongs to, because two files answer to "the
detailed commentary" and a reviser told only the section repairs one of them.
Each of the five content lanes carries what its own criteria must do with that:
a rendering composed in the edition nobody opened is still composed, a short
form reaching only the synthesis can stand flat a lead the canonical prose
bounded, reader order is a property of a built document so a second edition has
its own, voice and disagreement live in prose written at two lengths on two
passes, and the synthesis lane can leave the very synthesis it judges unread.
`content-revision` is told that a repair to one edition's prose is not a repair
to the other and that it re-reads both after every edit, and `author-proper` no
longer describes the synthesis as mechanically derived — it is the same build,
and the prose that reaches one edition alone is prose the author wrote for that
edition and must keep true.

Version 19 also owns the process fact behind that repair, since the fragments
are where a rule has to go. During the run a lane needed the two-editions rule,
and it reached the lane as an instruction added to a brief at the console
rather than as a fragment. Nothing in the packet carried it, the digest did not
move, and the run cannot be replayed into the state it actually ran in. A lane
that needs something its packet does not carry has found a fragment defect, and
it is repaired here, at a version, or escalated — never supplied beside the
packet.

The same version closes the last input a console still owned: how hard the
dispatched model thinks. Every other dispatch decision was already declared and
hashed — which stage runs, by one agent or by five lanes, on which fragments,
against which schema — while the reasoning effort was whatever the driver
picked. Two hosts could answer identical packet bytes at two levels and the run
recorded neither.

Stages now declare `effort`, resolved most specific first: the lane's own, then
the stage's, then the workflow's `default_effort`. It rides in the packet
header, where the packet hash covers it, and it is printed in the driver
instructions beside the lane it belongs to. A gate declares none and is
refused if it tries: tpt runs a gate, no agent does. The levels are `low`,
`medium`, `high`, `xhigh` and `max`, and a word outside that set fails the
workflow at load rather than reaching a host that would ignore or guess at it.

What `proper` declares, and why:

- `xhigh` is the default, and what the long-horizon stages run at: seed
  through the brief, the authoring, and every revision. It is the level tuned
  for work that has to hold a whole document in view.
- `max` is paid for at one judgment, in the two places that judgment is made:
  deciding what this repository does not hold. `source-audit` collates the
  appointed text against the controlling witness, and the research lane
  `source-citation-coverage` decides what is attested and what is still a
  lead; `content-evaluation` is then the pass that gates publication on the
  scholarship, and all five of its lanes run there. This is where the corpus
  actually fails — the Fourteenth Sunday spent three revision rounds stripping
  claims resting on witnesses the repository does not hold — and it is the
  only place the extra cost buys anything.
- `high` covers the mechanical stretch, where the answer is checkable rather
  than judged: `build-artifacts` and `artifact-revision`, the page-by-page
  `visual-evaluation` and its revision, `publish-artifacts`, the web
  conversion, evaluation and revision, and `install-publication`.
- `low` is declared by no stage. It is the level for a single locus or a
  single hash check, and no stage of this workflow is one; a driver's own
  narrow lookups are not stages and are not governed here.

Raising a level is a version bump like any other, because it moves the digest
and invalidates every run in flight. That is the intended cost: an effort
level chosen per run, at the console, is exactly the unrecorded input this
version exists to remove.

A run seeded against version 18 or earlier fails closed; seed it again.

The `proper` workflow was at version 18. Version 18 settled who owes a source
record, because a run had just ended over one nobody owed. Run
`5f2d2447ee8d4445` reached `author-proper` with a complete brief — five
audited gallery entries carrying both texts, exact loci, wording checks and
rights status, and a page-2 dossier resting on witnesses the lanes had
opened — and blocked, correctly under the instructions it had, because the
brief told it to register and bind those witnesses before publishing them.
Nothing in this workflow may register a source: `src/sources/` is written
outside a run, the research lanes are read-only, and the author may not
retrieve. Another pass through the lanes could not have met the request
either, so the run had one disposition available and took it.

The demand starts in `source-citation-coverage`, a diagnostic lane, so the
correction is in what that lane may call a defect. A witness no lane reached
is missing evidence, and the lanes can be sent back for it. A witness a lane
checked, whose work, edition and locus are known, is a claim the guide may
print on that citation, and that the library holds no record for it is a
provenance note rather than a bar. `guidance/sources.md` had said so all along
— a schema version 1 binding file requires no machine ID for every sentence,
and stable ids do not replace intelligible citations — and this Sunday's own
published gallery was printed on exactly such citations: its three entries
name Milton, Burnett and Keynes by work and locus, while the leaf's binding
file holds thirteen entries, not one of them a cultural witness. The lane, the
brief and the author now each carry that distinction in those words, so a
coverage finding can no longer reach the author as a bar it is forbidden to
clear.

Version 18 also gives `research/source-bindings.toml` a producer. The source
system requires the file of a publication and `content-preflight`'s
`restricted-not-reproduced` reads it to hold the guide's own text against the
rights recorded in `src/sources/`, but no stage was told to write it and no
fragment has ever named the file. Every leaf that carries one got it beside
the run rather than from it, and a leaf this workflow produced from scratch
would have failed that check with no repair target able to fix it.
`author-proper` now owns the file, bound twice over. It binds only ids
`tools/source-library fingerprint` resolves, taking the fingerprint from the
tool rather than typing one, and its `states` and `verified_on` may go no
further than the brief and the leaf's own `propers/verified.md` provenance
support. Registering a source stays outside the run.

`content-preflight` carries a ninth check for the same reason.
`bindings-valid` runs the source library's own validator and reports the lines
naming this leaf's file: every id one the library registers, every role and
state a word the schema knows, every reviewed state carrying the fingerprint
its bound record computes to now. Until this version the only thing in a run
that read the file was `restricted-not-reproduced`, which reads two of its
fields, and the tree shows what that costs — a published leaf carries a
binding whose fingerprint moved with its source and which no gate saw. An
error in another publication's file is counted and left to it, because failing
a production over a defect it did not write and may not repair is not a check;
and a fingerprint the validator refuses is not a value to paste back, since it
says the bound record moved and what the leaf rests on it for is read again.

Two things stay outside the run, and the second is worth saying because the
file is new to it. Registering a source in `src/sources/` is one. The
inventory sequence `guidance/sources.md` prescribes for a source-bearing
change is the other — `tools/tpt source-inventory refresh`, the provider's
classification review, `source-family-migration refresh`, then `make
check-sources` — and no stage runs any of it. That was already true of every
source surface a run writes, `main.tex` included; the binding record joins
them, and the refresh is the maintainer's after a production, not the
production's.

A run seeded against version 17 or earlier fails closed; seed it again.

The `proper` workflow was at version 17. Version 17 wired the propers to the
Scripture chronology corpus, which is now the only place a proper guide may
get a biblical date from. `guidance/scripture-chronology.md` §14 states the
rule — a publication that needs biblical chronology MUST read the corpus and
MUST NOT independently infer, research, harmonize or assign a replacement —
and until this version nothing carried it into a proper. Each guide found its
own dates, from whichever commentary or chronological table a research lane
reached, and a wrong year read exactly like a right one on the page.

`resolve-context` now writes the corpus's answer for the formulary's own
appointed verses to `src/<provider>/<proper>/research/chronology.toml`,
through `tools/tpt proper-chronology record --write`. The record is generated
from the calendar's citation encoding and `scripts/_chronology.py`, and it
carries the stable ids §14 asks a consumer to hold — event or
composition-unit id, relation, profile — beside the source's own label.
`research-scripture-context` reads it instead of researching a date;
`research-synthesis` restates it in the brief as the
`Scriptural chronology audit`; `author-proper` prints from it through two
macros, `\chronology{subject}{relation}{label}` for one assertion and
`\chronodate{element-keys}{content}` for one dossier row's date cell.

`content-preflight` carries two further checks, making eight, and version 18's
`bindings-valid` a ninth; the two prose screens described below bring it to
eleven.
`chronology-record-current` regenerates the record from the corpus and
refuses a leaf whose copy has drifted — the record is generated, so the
repair is to rewrite it and re-read the prose that rested on it, never to
edit it toward the guide. `chronology-claims-supported` refuses a
`\chronology` claim the corpus does not make at the verses that element
appoints, and, from this version, refuses a date cell that prints any figure
outside such a claim or an appointed Scripture with no cell at all. Where the
corpus answers `undated-in-tradition` or `research-pending` there is nothing
to print, and the guide states the absence rather than filling it.

The contract binds from v17 and the leaf says which version produced it, so
the five leaves published before this wiring — which state `proper` v11 or
`unknown` — are reported out of scope rather than refused for work that was
correct when it was done. The two checks interlock with
`provenance-matches-run`: a stage cannot dodge the chronology contract by
understating its version without failing the check that holds that version
against the run driving it. A leaf that carries a chronology record is held
to it whatever version it states, so deleting the record is not an escape
either. A run seeded against version 16 or earlier fails closed; seed it
again.

The `proper` workflow was at version 16. Version 16 gave that producer a
verifier. Version 15 told `author-proper` to copy the run's identity off its
own packet header into the `\AIGenerationProvenance` record, and nothing read
what it wrote: an instruction obeyed and an instruction ignored left the same
tree, and the one leaf that already had a record stated the version of the run
before the one that wrote it, because a `v10` in the prose of an
`\AIModelContribution` survived a v11 pass and became a structured fact.
`content-preflight` now carries a sixth check, `provenance-matches-run`, which
holds the record's workflow, version, source digest, run id and seed commit
against the run driving the stage; any one of them wrong fails the gate to
`content-revision` with the mismatch named. `install_commit` is not compared —
it is legitimately `unknown` while the document is being written, since the
commit the artifact enters the tree on does not exist yet.

Only the run can settle this, and until now a gate command could not name the
run at all: a check command was substituted from the run's normalized
arguments and nothing else. Gate commands are now substituted from those
arguments *and* the run's own identity, under a reserved `run.` namespace —
`{run.workflow_id}`, `{run.workflow_version}`, `{run.workflow_digest}`,
`{run.run_id}`, `{run.repo_commit}`. The dot is what keeps the two apart: an
argument name is a plain identifier, so a workflow that declares an argument
called `run_id` still gets `{run_id}` for its value and `{run.run_id}` for the
engine's, and an argument in the reserved namespace is refused when the
definition loads and again when a gate runs. Run facts are shell-quoted
exactly as arguments are, and substitution is now a single pass, so no
supplied value can smuggle a placeholder into what a later name expands to. A
run seeded against version 15 or earlier fails closed; seed it again.

The `proper` workflow was at version 15. Version 15 gave the workflow a
producer for the record every document is required to carry. The
`\AIGenerationProvenance` record states which workflow, at which version and
which source digest, under which run and from which seed commit, produced a
document; `check-generation-metadata` requires exactly one of them in every
leaf; and nothing wrote it. The engine held all five facts from the moment a
run was seeded and handed the worker four of them in the packet header, so
`author-proper` — and `content-revision`, which quotes the same fragment — now
names the header fields to copy and forbids taking any of them from the leaf's
existing record or from the prose of an earlier contribution, which is how the
one leaf that had a record came to state the version of the run before the one
that wrote it. The fifth fact, the run id, was the one the header did not
carry, so the packet header now carries `RUN_ID`; it is the engine's own hash
of the workflow, version, seed commit and arguments the header already states,
so it adds no input and no packet's determinism changes. `install_commit`
stays `unknown` at authoring time: the commit an artifact enters the tree on
does not exist while the artifact is being written.

The `proper` workflow was at version 14. Version 14 made `seed` refuse an
identity the 1962 calendar does not register, by giving `document_discovery` a
`validator` the engine runs before a run exists. Discovery answers which
documents are authored; it cannot answer whether an unauthored identity is
real, and `authorize-target` — the stage that writes the scope ledger — runs
before the `scope-gate` that used to be the first deterministic refusal. So a
mistyped or invented id could get a worker as far as recording an
authorization for a proper that does not exist. The registry decides, the
workflow keeps no list of its own, and a registered but unauthored identity
still seeds exactly as before.

The `proper` workflow was at version 13. Version 13 made `publication-gates`
verify the publication rather than its shape. The gate had twelve checks and
every one of them asked whether a file was in place; nine more now ask whether
what is in place is right. `installed-pdf-matches-accepted` compares each
installed PDF byte for byte against the build artifact `final-acceptance`
accepted, which `publish-artifacts` used to ask a worker to confirm.
`release-record-valid` reads both release records and holds their
`schema_version`, `id`, `catalog`, `status` and `authorization` against this
publication instead of testing that the files exist.
`catalog-read-link-resolves` binds the catalog's `Read` link to the tracked
Markdown the site renders it from — `web/<provider>/<proper>.html` is generated
at site-build time from `web/<provider>/<proper>.md` and is never tracked, so
the source is what can be proved — and requires the link to sit in the same row
as this provider's PDF link. `other-provider-cell-unchanged` requires this
identity to own exactly one catalog row, exactly one cell in it to name this
provider, and every other provider's cell in that row to hold its own
well-formed state: the bare word `Planned` or links of its own.
`publication-marker` requires the row's stable marker in the form the release
tooling reads, the bare leaf id for the manifest's primary provider and the
`<provider>:` prefixed form for any other. And four site checks —
`check-release-bindings`, `check-public-alpha`, `check-document-catalogue` and
`check-web-editions-current` — are now gate checks judged by exit code rather
than steps `install-publication` asked a worker to run and report on. The
fragment keeps the one thing in that step that writes,
`make refresh-release-bindings ADOPT=1`. No stage, lane or transition changed;
what changed is that no worker's account of a check now stands between a run
and `ACCEPTED`.

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
still terminates: at this version `content-evaluation` declared
`max_iterations: 3`, so its ceiling was six. (Version 22 raised the repeat
allowance to four and the ceiling with it to eight; six is now
`proper-finish`'s figure, that pipeline's `content-evaluation` still declaring
three.) Run
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
are as they were at version 5. A run seeded against version 12 or any earlier
version is bound to that source and fails closed rather than continuing under
fragments it never started with; seed it again.

`content-preflight` is a gate like any other: advance it with
`tpt proper <id> advance <run-id> --run-gate <doc>`. Each of its eleven checks
is one invocation of `tools/tpt check-content-preflight --check <name>`, judged
by exit code, and the tool prints what it counted on a pass and names the
entry, identifier, relation, quotation, restricted reproduction, provenance
mismatch, chronology defect, house-voice site or missing proposal field it
refused on a failure. It was four until version 11 added
`restricted-not-reproduced` and version 16 added `provenance-matches-run`.
All but one read only the repository and can be run over a published leaf at
any time; `provenance-matches-run` also takes the run's identity, which the
gate supplies from the engine, so running the tool with no `--check` runs the
rest and never passes that one for want of an answer.

The two most recent are prose screens, and they are here rather than in the
evaluation behind them because the evaluation demonstrably cannot afford them.
`house-voice` refuses the lexically marked forms of the defect
`guidance/editorial.md` names — the guide, its sweep, its apparatus or this
repository as a grammatical subject, retrieval mechanics in the body, a count
labelled instead of stated — after masking the regions that rule protects.
Three successive max-effort evaluations of one leaf spent an entire iteration
budget on that single class, each pass clearing the sites it named and the
next finding a fresh subset; a gate loop drains it at no evaluator cost.
`proposal-fields` refuses a proposal that substitutes a heading of its own for
one the profile fixes, which is a defect four separate max-effort sweeps
located and none reported, because it fell between two lanes' criteria.

Both are partial, and `house-voice` most of all: a leaf it accepts has not
been found compliant, only found to carry none of the forms it knows. It also
refuses most leaves in the corpus today, which is a finding about the corpus
rather than a settled verdict — see `PROJECT-WORK.md`. What either reports is
a sentence to rewrite and never a sentence to delete: every difference,
negative result, bound and attribution stands after the repair. It
exists so the five-lane evaluation behind it spends its budget on judgment
rather than on things grep can settle; it does not replace any of that
judgment. A failed check sends the run to `content-revision` with the check's
own output as findings, and that loop is bounded at three consecutive failures
like every other.

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
artifacts.

Since version 13 it also verifies that each installed PDF is byte-identical to
the accepted build artifact; that both release records name this leaf, this
catalog, status `alpha` and a standing authorization; that the catalog's `Read`
link sits in this provider's own row and the tracked Markdown the site renders
it from exists; that this identity owns exactly one row, that exactly one cell
in it names this provider, and that every other provider's cell in that row
still holds `Planned` or links of its own; that the row carries this
publication's stable marker; and that `check-release-bindings`,
`check-public-alpha`, `check-document-catalogue` and
`check-web-editions-current` all pass. Those four are whole-repository checks,
so the terminal gate refuses a publication that is wired correctly into a site
that is not.

A failed check sends the run to `publication-revision`, which
repairs the wiring at `install-publication` and re-gates, and that loop is
bounded at three refusals as well.

Passing the checks is necessary, not sufficient. Before it records `ACCEPTED`
the engine audits the run: every evaluator and gate that ran must last have
recorded `PASS`, every recorded result and packet must still be present and
hash as recorded — lane packets and lane results included — and no stage's
latest result may carry a standing blocking finding. A run whose files were
edited cannot be accepted; discard it deliberately before seeding anew.
