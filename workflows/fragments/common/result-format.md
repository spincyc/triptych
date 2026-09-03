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

Stability binds both ways. An id belongs to one defect for the life of the
run, so a defect you have not raised before takes the next unused number and
never a number already spent on a different one. The engine cannot read your
prose semantically to decide that two differently stated defects are really
the same, so a stage's budget remains a count of repeated ids rather than a
comparison invented by the engine. Recycling an id would spend a failure the
run did not earn, and enough of them would block a run that was converging.

Every evaluator packet carries `PREVIOUS_FINDINGS`, the distinct finding ids
this evaluator has already used during the run. A fan-out lane packet carries
only that lane's previous findings; the parent packet carries the union. Read
the header before assigning a number. The engine also enforces the identity:
if an old id returns with a different lane, problem, or required result, the
engine refuses the submission without advancing the run. A moved location is
permitted, because repairing or repaginating the artifact can move the same
defect without changing what it is. A moved repair owner is permitted too:
one defect can progress from research to brief or authoring, and the engine
tracks that owner movement separately so it is not charged as an unrepaired
repeat. If the work actually contains two defects with different problems or
required results, split them and give each its own id.

Only `blocking` severity findings trigger revision. `advisory` findings are
recorded but do not block.

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
