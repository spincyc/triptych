# Handoff — current state of the pictographic lane

**Operational continuation document.** It records where the work stands right
now and how to pick it up. It deliberately does **not** restate the rules.

The durable rules live in
[`../../../artistic/RENDERING-PROTOCOL.md`](../../../artistic/RENDERING-PROTOCOL.md).
**Read that first.** It is the timeless protocol: the only valid artistic input
path, the readiness gate, the two approval gates, what the artist owns and does
not own, the panel rule, the Missal failure mode, the canary rule, and
fail-closed behaviour. Nothing in this file overrides it.

## Where things stand

| Layer | Path | State |
| --- | --- | --- |
| Structural choreography | `structural/low-mass/v0.21/` | Complete and human-approved. Sealed. |
| Render contract | `render-contract/low-mass/v1/` | Complete. Compiles every scene to explicit world geometry. |
| Artistic protocol | `artistic/RENDERING-PROTOCOL.md` | In force. |
| Artistic rendering | — | **Not started.** No canonical plate is approved. |

Current base commit and readiness counts are not written here, because they go
stale. Get them from git and from the tooling:

```sh
git log --oneline -1
./tools/tpt pictographic readiness roman-1962 low-mass
./tools/tpt pictographic readiness roman-1962 low-mass --blocked
```

## Starting an artistic lane

Seed the canary first. This is the only sanctioned way to hand a scene to an
artistic agent:

```sh
./tools/tpt pictographic art-seed roman-1962 low-mass LM-001A
```

That writes a package containing the compiled render contract, the
deterministic skeleton, the provenance record, and the generated art-agent
instructions. Give the artistic agent **that package**, and nothing else — not
the structural YAML, not a prose summary.

The command fails closed. A blocked scene refuses with its exact cue and
exit status 2, and writes no package. There is no force path.

Then, per the protocol: render `LM-001A`, decide `STRUCTURE` before `ART`, and
do not begin style development until `LM-001A` reaches `STRUCTURE = PASS`. If
it fails structurally, stop and diagnose the pipeline.

## Regenerating and checking

```sh
cd src/gpt/liturgy/roman-rite/1962/reference/mass-pictographic-dictionary/render-contract/low-mass/v1
./compile.py && ./skeleton.py && ./review.py     # regenerate
./compile.py --check && ./skeleton.py --check && ./review.py --check
./validate.py
```

The verification sheet for the regression fixtures is at
`review/verification-sheet-v1.svg`.

## Current blockers to human review

A scene is blocked when an unresolved serving-profile cue could change
something visible, or when a directional phrase names no reference frame. The
live list, with each blocking cue, comes from:

```sh
./tools/tpt pictographic readiness roman-1962 low-mass --blocked
```

Resolving any of them is human work in the structural or render-contract lane.
Four frame-ambiguous phrases and what a human must decide about each are
recorded in `frame-vocabulary.yaml` under `undetermined_phrases`.

## Next lane recommendation

Begin with the canary, then the opening cluster at the foot of the altar, which
is the most art-ready stretch of the corpus. Keep every plate's provenance per
`artistic/plate-provenance.yaml` from the first plate onward; retrofitting
provenance later is how it stops being true.
