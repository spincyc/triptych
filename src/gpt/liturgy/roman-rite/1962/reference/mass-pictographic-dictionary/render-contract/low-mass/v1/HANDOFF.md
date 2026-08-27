# Handoff — current state of the pictographic lane

**Operational continuation document.** It records where the work stands right
now and how to pick it up. It deliberately does **not** restate the rules.

The durable rules live in
[`../../../artistic/RENDERING-PROTOCOL.md`](../../../artistic/RENDERING-PROTOCOL.md).
**Read that first.** It is the timeless protocol: the only valid artistic input
path, the four artifacts and which of them the artist draws from, the rule that
raw art carries no publication furniture, the readiness gate, the two approval
gates, what the artist owns and does not own, the panel rule, the Missal
failure mode, the canary rule, and fail-closed behaviour. Nothing in this file
overrides it.

## Where things stand

| Layer | Path | State |
| --- | --- | --- |
| Structural choreography | `structural/low-mass/v0.21/` | Complete and human-approved. Sealed. |
| Render contract | `render-contract/low-mass/v1/` | Complete. Compiles every scene to explicit world geometry. |
| Render underlay | `render-contract/low-mass/v1/underlay.py` | Projects a compiled contract into the line drawing the artist edits. Required by `art-seed`. |
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

That writes one package, at `build/art-seed/<SCENE>/` unless `--out` names
somewhere else, holding exactly these files:

| File | What it is |
| --- | --- |
| `render-underlay.png` | **The edit source.** The projected line drawing, no text anywhere in it. |
| `render-underlay.svg` | The same drawing as vectors, if the tool prefers them. |
| `render-contract.yaml` | The compiled geometry in numbers. Supporting authority for review. |
| `skeleton.svg` | The diagnostic schematic, with its labels and angles. Supporting authority only, never the conditioning image. |
| `provenance.yaml` | Plate identity, baseline commit, panel manifest, readiness, and the underlay's hash and dimensions. |
| `ART-AGENT-INSTRUCTIONS.md` | The generated brief, including the canary note where it applies. |

Give the artistic agent **that package**, and nothing else — not the structural
YAML, not a prose summary. Hand `render-underlay.png` to the image tool as the
**EDIT SOURCE**, and ask for an image edit onto that exact geometry rather than
a picture in its manner.

**If the web tool cannot perform an image edit from the supplied PNG, the lane
STOPS and reports that limitation.** Do not substitute text-to-image
generation, however carefully the prompt is written from the contract. That
substitution is what failed the canary, most recently with a correct contract
and a correct skeleton behind it, and another correct-looking failure costs
more than a reported limitation.

The command fails closed. A blocked scene refuses with its exact cue and
exit status 2, and writes no package. A scene whose underlay cannot be
generated or rasterized, or which holds a visible object with no recognizable
underlay geometry, refuses the same way and leaves nothing behind. There is no
force path.

Then, per the protocol: render `LM-001A`, decide `STRUCTURE` before `ART`, and
do not begin style development until `LM-001A` reaches `STRUCTURE = PASS`. If
it fails structurally, stop and diagnose the pipeline.

## Looking at an underlay on its own

```sh
./tools/tpt pictographic underlay roman-1962 low-mass LM-001A
```

That writes `render-underlay.svg` and `render-underlay.png` under
`build/underlay/<SCENE>/`, or under `--out`. It is for inspecting geometry
without seeding a lane; `art-seed` generates its own copy and never reads this
one, so an underlay written here is not an artistic input package.

The raster is produced by `rsvg-convert`. Where that is missing, `underlay.py`
and `art-seed` both fail rather than shipping the vector alone, because the
edit source is the PNG.

## Regenerating and checking

```sh
cd src/gpt/liturgy/roman-rite/1962/reference/mass-pictographic-dictionary/render-contract/low-mass/v1
./compile.py && ./skeleton.py && ./underlay.py && ./review.py     # regenerate
./compile.py --check && ./skeleton.py --check && ./underlay.py --check \
    && ./review.py --check
./validate.py
```

The verification sheet for the regression fixtures is at
`review/verification-sheet-v1.svg`.

`./underlay.py --check` regenerates every art-ready scene's underlay in memory
and fails when the tracked SVG differs, so an underlay cannot drift away from
the contract it was projected from without the check saying so.

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
