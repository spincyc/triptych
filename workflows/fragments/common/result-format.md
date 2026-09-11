# Result Format

Your structured result must be valid JSON. The required schema depends on
your stage type.

## Name the packet you are answering

Every result must repeat, exactly, the `STAGE` and `ITERATION` values from
this packet's header:

```json
{
  "stage": "<the STAGE line of this packet>",
  "iteration": <the ITERATION line of this packet, as a number>
}
```

The engine rejects a result that names any other packet. That is how it tells
your work from a result submitted for a different stage, or from an earlier
result resubmitted.

## Name your lane, when this packet is a lane packet

If this packet's header carries `LANE` and `LANE_INDEX` lines, you are one
lane of a fan-out stage. Your result must also repeat, exactly:

```json
{
  "lane": "<the LANE line of this packet>",
  "lane_packet_hash": "<the lane_packet_hash the parent driver gave you>"
}
```

The parent driver states your lane's `lane_packet_hash` when it dispatches
you; it is the digest of this packet's exact bytes, and echoing it is how the
engine tells your result from one written against a packet it has replaced.
The engine rejects a lane result that names another lane, or a packet hash
other than the one it emitted for your lane. Report only on the criteria your
lane fragment gives you. Do not answer for another lane, and do not merge your
findings with anyone else's: `tpt` joins the lanes itself, in the order the
workflow declares.

## Worker (linear or revision) stages

```json
{
  "stage": "author-proper",
  "iteration": 0,
  "disposition": "PASS",
  "summary": "One or two sentences describing what you did.",
  "artifact_path": "src/gpt/liturgy/roman-rite/1962/propers/temporal/49-ninth-after-pentecost/main.tex"
}
```

Use `disposition: "PASS"` when you completed the stage's work. If you could
not complete it, use `disposition: "BLOCKED"` with a `summary` naming what
stopped you: the run stops there. Do not report `PASS` for work you did not
do; the engine has no other way to tell the difference.

### Say what happened to each finding you were given

Some stages owe the engine a repair report and some cannot give one. The
pipeline decides, with `reports_repairs` on the stage, and your own stage
fragment tells you whether yours is one. **Where it is, and your packet's
`PRIOR_FINDINGS` header carries blocking findings, a `PASS` result must also
carry `finding_dispositions`.** One entry per forwarded finding, and no result
without it advances:

```json
{
  "finding_dispositions": [
    {"id": "CON-CIT-003", "outcome": "repaired"},
    {"id": "CON-PRO-001", "outcome": "not-repaired",
     "note": "Why it could not be cleared, in a sentence."}
  ]
}
```

- `id` is the finding id **exactly as `PRIOR_FINDINGS` gives it**. You are
  not minting these; you are answering the ones you were handed.
- `outcome` is `repaired` or `not-repaired`. There is no third value.
- `note` is optional to the engine and needed in practice on a
  `not-repaired`: it is what the run quotes back when a stage blocks, and an
  unrepaired finding with no note tells the next reader nothing.

What the engine enforces, on a stage that reports and was given findings:

- **Every forwarded blocking finding appears exactly once.** Leaving one out
  is refused, and so is naming one twice. A dropped finding reads exactly
  like a repaired one, and the iteration budget would score an abandoned
  defect as progress.
- **A finding the engine did not forward you is refused.** The set it holds
  you to is the blocking ids it recorded when it routed them into your stage,
  which is what `PRIOR_FINDINGS` states: one more or one fewer is refused.
- **`CARRIED_FINDINGS` is not part of this report.** Where your packet has
  that header it holds findings you must still address — they are yours and
  unaddressed — but they reached you from an earlier transition and the
  engine does not expect them here.
- **`ADVISORY_FINDINGS` is not part of this report either, and naming one is
  refused.** That header holds findings the evaluation did *not* block on.
  They gate nothing and spend no iteration budget. Clear the ones you can
  while you are already in those files — that is why they are handed to you —
  and leave the rest. You owe the engine no account of them, and an entry for
  one is rejected exactly as a finding the engine never forwarded is.

Two things the engine does not check, and you should still get right. A
stage handed no blocking findings has nothing to report and the engine
returns before reading the field, so a report volunteered there is accepted
and silently ignored — a first authoring pass is not a failed repair. And the
shape check is by schema, not by stage, so a worker-shape stage that does not
report may carry the field without being refused. Neither reaches the budget.
Return the field when you were given findings and told to account for them,
and not otherwise.

The declaration is per stage because two stages receive blocking findings and
cannot answer for them. A fan-out `research` re-entry returns a result the
engine composed by joining its lanes: no agent wrote it, and no lane can speak
for the whole. `research-synthesis` returns an evaluator shape. Neither may
carry the field at all — their schemas do not define it, and the engine
refuses a result that carries it.

`not-repaired` is a legitimate outcome and reporting it is not a failure. It
does not by itself block the run and it is not held against you; it is the
honest answer whenever you attempted a finding and are not confident you
cleared it. Where your stage reports, this is the only channel through which
the engine learns whether repair is working — the evaluator cannot supply it,
because re-reading a changed document it sees defects and not the history of
attempts on them. A production's central defect survived three rounds for
exactly that reason: each round reported it repaired, and the run spent its
budget re-finding it.

## Research lane stages

A read-only research lane returns evidence, not prose and not an artifact:

```json
{
  "stage": "research",
  "iteration": 0,
  "lane": "scripture-context",
  "lane_packet_hash": "the lane_packet_hash the parent driver gave you",
  "disposition": "PASS",
  "summary": "One or two sentences on what you swept and what you found.",
  "findings": [
    {
      "id": "SCR-001",
      "claim": "What you are asserting, in one sentence.",
      "evidence": ["Each source named precisely enough to be checked."],
      "notes": "Uncertainty, disagreement, negative results, evidence state."
    }
  ]
}
```

Every finding carries all four of `id`, `claim`, `evidence`, and `notes`.
`evidence` is a list of strings. A sweep that found nothing is itself a
finding: record the negative result rather than omitting it.

A research lane has only two dispositions. `PASS` means you did your lane's
sweep and these are its results, whether or not it found much. `BLOCKED` means
you could not do the sweep at all, and the run stops there. There is no
`CHANGES_REQUIRED` for a research lane; the engine rejects one.

`tpt` joins every lane itself and forwards the joined findings, each
tagged with the lane that raised it, into the next stage's packet. Do not
write anything into the repository, and do not answer for another lane.

## Evaluator stages

```json
{
  "stage": "content-evaluation",
  "iteration": 0,
  "disposition": "PASS" | "CHANGES_REQUIRED" | "BLOCKED",
  "summary": "One or two sentences.",
  "findings": [
    {
      "id": "VIS-001",
      "severity": "blocking",
      "location": "page 4",
      "problem": "Description of the issue.",
      "required_result": "What the reviser must produce to resolve this finding."
    }
  ]
}
```

- `PASS`: no blocking findings. The workflow advances. A `PASS` that still
  carries one is refused, because nothing downstream can resolve it.
- `CHANGES_REQUIRED`: blocking findings present. The workflow enters a
  bounded loop back to the stage that owns the repair — a reviser, or an
  earlier stage that must run again. Findings are forwarded verbatim to it.
  A `CHANGES_REQUIRED` carrying no blocking finding is refused: it asks for a
  change while naming none.
- `BLOCKED`: a finding cannot be resolved by revision. The workflow stops.

Finding IDs must be stable across iterations (e.g., `VIS-001` refers to the
same issue every time it appears). Use the prefix your own stage fragment
gives you; `CON-` for content evaluation and `VIS-` for visual evaluation are
two of them, and a stage that names another means it.

Only `blocking` severity findings trigger revision. `accepted` and `advisory`
findings are recorded but do not block.

### An advisory is a verdict, not a waiting room

**Severity is decided once, on the evidence, at the iteration you first see
the defect. It is not a queue position.** If a defect would justify blocking
the run at any iteration, it is `blocking` the first time you report it. If it
would not, it is `advisory` and it stays advisory for the life of the run.

Raising as `blocking` an id you filed as `advisory` in an earlier iteration is
the failure this rule exists to stop, and it is forbidden. Nothing about the
defect changed between the two reports; only your patience did. What the
practice actually does is hide the true size of the repair from the run:
the blocking count falls round after round while the backlog behind it does
not, so the iteration budget is spent draining a queue the engine cannot see.

This is not hypothetical. In run `e4aebcbd941b6b1a`, **19 of 62 blocking
findings — 31% — were the same lane's own advisories from a previous round,
promoted a mean of 1.1 rounds later.** One lane filed four advisories at
iteration 0 and raised those exact four as blocking at iteration 1; another
filed four at iteration 4 and raised those exact four at iteration 5. The
production's blocking counts read 18, 12, 10, 8, 7, 5, 7 and looked like
convergence. They were slices off a backlog that refilled itself every round,
and the run reached its absolute ceiling with the document in good shape.

So: report the defect at the severity it deserves, immediately. A round that
honestly returns twelve blocking findings converges; a round that returns four
and warehouses eight does not. Do not soften a real defect to advisory because
the round already carries several — the count is not a budget you are spending.

Where a defect genuinely does not merit blocking, an advisory now reaches the
reviser anyway: the `content-revision` packet carries the standing advisories
under `ADVISORY_FINDINGS`, and the reviser clears what it can without the
finding ever gating the run. An advisory is no longer a channel that reaches
nobody, so there is no longer any reason to promote one to be heard.

### `accepted`: true, and not worth a repair round

Blocking and advisory were the only two answers a lane had for a real defect,
and neither says the thing a careful reader most often wants to say: *this is
true, I checked it, and repairing it would cost the document more than the
defect costs the reader.* Forced to choose, lanes blocked. One lane wrote in
its own report that it doubted a one-clause rewording deserved to block and
raised it blocking anyway, because it read the rule above as forbidding
anything else. That is a round spent on a clause.

So there is a fourth severity:

```json
"severity": "accepted",
"accepted_because": "the guide states the bound correctly two lines later; moving it costs a paragraph of settled prose to save a reader nothing"
```

Use it when **all** of these hold. The defect is real and you have checked it.
Repairing it would touch settled prose, or move pagination, or trade one true
sentence for another. And a reader who never learns of it is not misled.

`accepted` carries no `repair_target` — accepting a defect is deciding it needs
no owner, and the engine refuses a finding that claims both. It does not block,
does not spend the iteration budget, and does not stop acceptance.

**An accepted finding binds the rest of the run.** The engine refuses a later
round that raises the same id as blocking, whichever evaluator you are and
whether or not anything of yours reaches a tracked file. Where the stage is
the one the pipeline declares as recording standing findings, your verdict is
also written to `<document_root>/evaluations/blocking-findings-v1.toml` under
`[[accepted]]` with your reason, and the advisories beside it under
`[[advisories]]`. That is the point of it: the judgement outlives the round
that made it, so the next cold read of the same passage meets the decision
instead of the bare defect. Where the stage is not one of those — on the
propers pipelines `visual-evaluation` and `web-evaluation` are not, and no
recording stage runs after them — the judgement binds this run and stops
there. It is held in the run directory under `build/`, which is gitignored,
which `make clean` and a workspace tidy delete, and which no later run reads:
what you accepted is a decision this run will honour and not a record the leaf
carries forward.

If you believe an earlier round accepted something it should not have, do not
raise it blocking. Escalate it: a disagreement about what is worth repairing is
a question for a person, and the escalation route is how one reaches them.

### Reading `REVIEW_SCOPE`

An evaluation packet after the first carries `REVIEW_SCOPE`: the leaf-relative
files that changed since this stage last read the document. An empty list means
nothing changed.

Read the whole document the first time. After that, **read what moved, and read
the passages your own standing findings name.** You are not being asked to skim
the rest; you are being asked not to re-derive fresh blocking findings from
settled prose that no reviser has been near.

This is not a formality. A run of this pipeline blocked with its document in
good shape after eight consecutive evaluations, eight failures, one repeated
finding, and not one round in which the reviser failed to repair what it was
given. Seven of the eight rounds found something new and true in prose nobody
had touched, because a cold reader of a dense document at maximum effort never
runs out of true things to say. The document was converging. The review was
not terminating, and it cost some nine million subagent tokens to discover.

A blocking finding against a file outside `REVIEW_SCOPE`, whose id is not
already standing, must carry:

```json
"out_of_scope_reason": "unchanged in itself, but the sentence it depends on moved in sections/90-scope.tex this round, and its claim is now false"
```

Say what makes it true now and what kept it from being raised before. The
engine refuses a blocking finding of that shape without one, and refuses the
whole submission with it — on a fan-out stage that is every lane's work — so
supply the field or choose a different severity. It is not a ban: a defect
really can become true because another file changed, and that sentence is all
that is asked of you.

### Five fields on every finding, whatever its severity

**Every finding carries `id`, `severity`, `location`, `problem` and
`required_result`. All five, on every finding, at every severity.** There is
no reduced shape for a finding that does not block. `required_result` in
particular is required on an `advisory` and on an `escalation` exactly as it
is on a `blocking` finding, and the engine refuses a result that omits it.

That is a rule about the report and also about the thinking behind it. A
finding that cannot say what would satisfy it has not identified a defect: it
has recorded a misgiving. An advisory saying only that a passage "could be
stronger" leaves the next reader nothing to act on and nothing to close, so
the field is demanded of it. For an advisory, `required_result` states what
would resolve it if anyone chose to act on it; for an escalation, it states
what the maintainer is being asked to decide. Neither is a promise that the
run will do the work.

The refusal is total. A malformed finding fails the whole result, and on a
fan-out stage the whole submission — every lane's result is refused, not only
the one that carried it, and the run is untouched. One advisory missing
`required_result` has cost a five-lane submission a full round trip.

Two fields, and only two, depend on severity:

| Field | When it is required |
| --- | --- |
| `id` | always |
| `severity` | always |
| `location` | always |
| `problem` | always |
| `required_result` | always — `blocking`, `accepted`, `advisory` and `escalation` alike |
| `repair_target` | `blocking` only |
| `accepted_because` | `accepted` only |
| `escalated_to` | `escalation` only |
| `out_of_scope_reason` | a `blocking` finding outside `REVIEW_SCOPE` whose id is not already standing |

`repair_target` is carried only where your stage's own fragment says the
stage routes repairs by owner, and only on a blocking finding. It is refused
on an escalation, because an escalation is precisely a defect no stage in
this run may repair and naming an owner would make it a blocking finding
wearing a severity that exempts it. An advisory does not carry it.
`escalated_to` belongs to an escalation and only to a stage whose fragment
admits that severity.

Nothing else on a finding varies with severity. If your stage's fragment
gives you a field this table does not name, it is that fragment's to explain.

### `observations`: something real that your criteria do not reach

An evaluator result may also carry observations:

```json
{
  "observations": [
    {"location": "sections/50-interpretive.tex P4",
     "note": "carries no 'what the element-by-element reading misses' field"}
  ]
}
```

Both `location` and `note` are required on each entry, and there are no
other fields. An observation has **no severity, no `required_result`, and no
`repair_target`**: it routes nothing, blocks nothing, spends no iteration
budget, and stops no acceptance. `location` names the file and the place in
it to the same standard a finding's does. `note` states what you saw, in a
sentence.

It exists so that a real sighting a lane's own criteria do not reach reaches
the run at all, instead of dying in the lane's hand-back prose. `tpt` joins
observations in canonical lane order exactly as it joins findings and tags
each with the lane that raised it. Where the stage is the one the pipeline
declares as recording standing findings, they are written beside the blocking
findings into a tracked file in the document's own tree, which outlives the
run — a record for a person to read; no later run reads it back.

An observation is not a lesser finding and not a shortcut. If your own
criteria reach the defect, raise it as a finding under them; if your stage's
fragment names the class as another lane's, leave it to that lane rather than
observing it. And a kind of thing that keeps arriving as an observation is a
missing criterion in some lane's fragment, not a fact about the document —
say so in the `note` when you think you have found one.

Only stages whose schema defines observations may return them; the engine
refuses the field from a stage that does not, and your own fragment says
whether yours is one. A worker stage and a research lane have none.

A stage that also writes an artifact returns `artifact_path` alongside these
fields on a `PASS`, exactly as a worker stage does. Its own fragment says so
where that applies.

## Naming who repairs a blocking finding

Some evaluator stages route a repair by owner. Where the stage's own fragment
says so, every **blocking** finding must also carry:

```json
{
  "repair_target": "research" | "brief" | "authoring"
}
```

- `research`: the evidence is not there, and getting it needs a fresh sweep.
- `brief`: the evidence is there and the research brief states it wrongly, or
  drops a bound the brief itself recorded. No retrieval is required.
- `authoring`: the brief is adequate; the canonical leaf's prose, structure,
  or use of citations is not.

The stage's own fragment names the values it admits and how to tell them
apart; a stage that routes by owner may declare fewer than these three.

`tpt` reads the field and chooses the repair route itself, in the order the
workflow declares its routes, so one blocking finding naming the earlier owner
sends the whole run that way. You are not choosing the route and neither is
the driver: you are stating who owns the defect. The set of values is closed,
and the engine rejects a blocking finding that omits the field or names
anything outside it. Advisory findings do not carry it.

## Gate stages

Gates are run by `tpt` directly. No AI worker result is needed. The parent
driver runs `tpt ... advance <run-id> --run-gate`.

## Fail closed

A malformed or missing result, or one naming a different packet, causes the
workflow to stop with an error. No transition occurs. The run remains
inspectable but cannot advance until a valid result for the current packet is
submitted.

A refused result is not recorded: it is not copied into the run and its hash
does not enter the run's state. Nothing later reads it. Correct it and submit
it again for the same packet.
