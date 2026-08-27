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
| Sanctuary geometry | `render-contract/low-mass/v1/sanctuary-master.yaml` | The single definition of the sanctuary, and the authority resolving the structural level ordinals into elevations. |
| Composition review | `render-contract/low-mass/v1/sanctuary-master.yaml` | `underlay_visual_review:` **approved**, against the current geometry digest. `art-seed` refuses when it goes stale. |
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
underlay geometry, refuses the same way and leaves nothing behind. So does a
composition nobody has looked at, or one whose geometry has moved since it was
looked at — see the next section. There is no force path.

Then, per the protocol: render `LM-001A`, decide `STRUCTURE` before `ART`, and
do not begin style development until `LM-001A` reaches `STRUCTURE = PASS`. If
it fails structurally, stop and diagnose the pipeline.

## The composition review gate

`art-seed` will not hand out a picture nobody has inspected.
`sanctuary-master.yaml` carries `underlay_visual_review:` — a status, the canary
`LM-001A`, the preset, and a digest over the five files that decide what
the picture looks like: `sanctuary-master.yaml`, `camera-model.yaml`,
`underlay.py`, `underlay-objects.yaml` and `_contract.py`. The last two are in
it because the object library decides what the furniture is shaped like and
the compiler decides where the actors stand; leaving either out would let the
picture move under an approval still calling itself current. `require_visual_review()` in `scripts/_pictographic.py` refuses
on either an unapproved preset or an approval whose geometry has since moved.

```sh
./tools/tpt pictographic composition-review roman-1962 low-mass
./tools/tpt pictographic composition-review roman-1962 low-mass --refresh
```

Without `--refresh` it reports the recorded and current digests and exits 2
when the approval is stale or absent. With `--refresh` it records the current
composition as reviewed.

**Refresh only after actually rendering the canary and looking at it.**
Refreshing the digest without looking is the single move the gate exists to
prevent. `sanctuary-master.yaml` lists, under `underlay_visual_review:`, the
gate questions to answer and the regression scenes to re-render alongside the
canary whenever the sanctuary, the envelopes or the camera move: `LM-001A`,
`LM-039A`, `LM-009A`, `LM-014A`, `LM-035A`, `LM-061A`. Between them they put a
change of level, a kneeling figure, a figure in profile and a full mensa on
screen, none of which the canary alone can show.

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

## The sanctuary, the Missal, the stand, and the camera

The sanctuary is defined once, in `sanctuary-master.yaml`, and everything reads
it: level elevations and standing depths, the in-plano floor, the steps and
predella, the altar and its superstructure, the fixed anchors of cross and
candlesticks, the foot-contact bound, the composition guardrails, and the
recorded visual review. It is also where the approved structural corpus's
evenly spaced level ordinals are resolved. In height, the mensa goes to 1.55
rather than 1.35 and the predella to 0.64 rather than 1.00. In depth,
`level_depths:` puts each level at a standing depth on its own tread — the
predella at 1.29 rather than 1.5 — because taken literally an actor on step-3
stands past the predella's leading edge and a priest at the predella stands
inside the altar. Every level's identity and order is preserved, and the depth
mapping is monotonic. `_contract.py` applies it in `standing_depth()`, keyed on
the level and its canonical depth together, so an anchor merely on a level
without standing at its depth — the credence, beside the steps — is left as
authored. `README.md` records the argument; nothing in
`structural/low-mass/v0.21` was touched.

The step run is 0.30 of tread against a 0.16 riser, first leading edge at 0.22,
bounded altarward by the mensa and its corporal nave fold at 1.38, which is why
the altar body's front sits at 1.46. The tread is sized for a turned figure
rather than a walking one: a pair of soles rotated 45 degrees spans about 0.32.

The burse and the paten were remodelled while this was done — the burse pitched
78 degrees, standing upright against the gradine as a stiff square case does;
the flat paten narrowly exempted from the legibility floor. Both are recorded
in `README.md` and `VALIDATION-UNDERLAY.md`. Neither was fixed by moving the
camera.

The Missal rests on an inclined stand and is pitched toward the priest. The
stand declares the inclination; the book inherits it through a declared parent,
so the two cannot drift apart. A carried Missal is not on a stand and carries no
pitch. The compiled contract publishes `support_pitch_deg`, `supported_by`,
`page_up_vector_pitched` and `page_normal_world`, so nothing downstream needs a
hard-coded value.

The canonical plate camera is a **publication nave-front viewpoint** at an eye
of 1.52, 6.9 from the altar, behind a 1520 px lens, documented in
`camera-model.yaml` with its height, distance, focal length and projection. The
focal length belongs to the preset and reaches each panel as
`focal_length_px`; a renderer does not choose its own. The eye is a standing
worshipper's, and it is not an overhead engineering view. It was briefly raised
to 2.35 and then to 3.6 to make a flat Missal readable; that was compensating
for the object with the viewpoint, and the pitched model removed the need. It
came back down to 1.85, and then to its present height and distance when the
sanctuary elevations were resolved. The two raises are the error this lane
keeps having to name; every move since has been downward or backward.

Look at an underlay on its own with:

```sh
./tools/tpt pictographic underlay roman-1962 low-mass LM-001A
```

## Regenerating and checking

```sh
cd src/gpt/liturgy/roman-rite/1962/reference/mass-pictographic-dictionary/render-contract/low-mass/v1
./compile.py && ./skeleton.py && ./underlay.py && ./review.py \
    && ./camera-calibration.py                                    # regenerate
./compile.py --check && ./skeleton.py --check && ./underlay.py --check \
    && ./review.py --check && ./camera-calibration.py --check
./validate.py
```

The verification sheet for the regression fixtures is at
`review/verification-sheet-v1.svg`. The camera calibration sheet is at
`review/camera-calibration-v1.svg`: six candidate cameras on the same scene,
the published one boxed, the rejected raises to 2.35 and 3.60 kept for the
argument they make. It is a debug artifact — never a panel, never part of an
art-seed package, and never shown to an artistic agent.

`./underlay.py --check` regenerates every art-ready scene's underlay in memory
and fails when the tracked SVG differs, so an underlay cannot drift away from
the contract it was projected from without the check saying so.

## Known deferred underlay issues

Recorded rather than fixed, because this lane was narrow and these are art
direction rather than geometry:

- the figure envelopes are blocking solids, not anatomy. They now carry two
  outlines a body depth apart tied together, a head in two planes, a cincture, a
  hem, feet with soles resting on the level the figure stands on, and a chasuble
  for the priest — enough that a figure facing along the view axis no longer
  collapses to a vertical spike, which is what a single flat cut-out did.
  Standing, kneeling and genuflecting figures all carry explicit contact
  patches, and `validate.py` proves each patch lies on its actor's own tread,
  so a figure standing on air is now a refusal rather than an oversight.
  Kneeling and walking figures remain the weakest of them as drawings;
- the sanctuary architecture is still only the altar and its approach: mensa,
  gradine, tabernacle, a crowning band, the cross and four candlesticks, over
  the predella, three steps and the floor in front of them. There is no
  surrounding building;
- the step band is bounded rather than solved. The crop composes around the
  subject and the guardrails in `sanctuary-master.yaml` under `composition:`
  cap what share of the frame the steps may take, but an artist still owes the
  steps the treatment a stepped altar deserves.

None of these blocks an artistic canary. All of them are places an artist adds
realism inside geometry that is already fixed.

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
