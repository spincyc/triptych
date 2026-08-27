# Handoff — to the artistic rendering agent

You are receiving a **render specification and a set of skeletons**, not an
invitation to restage the Mass.

## What you are given

- **Structural baseline:** `d2e97b5ca` on `feature/pictographic`.
- **Approved choreography:** `structural/low-mass/v0.21/` — 197 scenes,
  `LM-001A` to `LM-140C`, in `scenes/inventory.yaml` order. Unchanged by this
  lane and not revisable by yours.
- **Render contract:** this directory, `render-contract/low-mass/v1/`.
- **Compiled contracts:** `contracts/<SCENE>.yaml`, one per scene.
- **Skeletons:** `skeletons/<SCENE>.svg`, one per scene.
- **Verification sheet:** `review/verification-sheet-v1.svg`.

## Commands

```sh
./tools/tpt pictographic readiness roman-1962 low-mass
./tools/tpt pictographic readiness roman-1962 low-mass --blocked
./tools/tpt pictographic render-contract roman-1962 low-mass LM-001A
./tools/tpt pictographic skeleton roman-1962 low-mass LM-001A
```

Regenerate everything, and prove the tracked output is current:

```sh
cd src/gpt/liturgy/roman-rite/1962/reference/mass-pictographic-dictionary/render-contract/low-mass/v1
./compile.py && ./skeleton.py && ./review.py
./compile.py --check && ./skeleton.py --check && ./review.py --check
./validate.py
```

## Where to start

**140 of the 197 scenes are art-ready.** Begin with `LM-001A`, the scene whose
first plate failed. Its skeleton shows the whole contract in one panel: the
altar's three steps and predella, the three figures in a side-to-side line at
one depth, and the Missal open on the Epistle side at reading yaw 135°.

**57 scenes are blocked for art.** Do not draw them, and do not resolve what
blocks them. `art-readiness.yaml` names the exact cue for each. Resolving a cue
is human work, and it is never done from the `altar-server-guides/` tree, which
is fenced and superseded.

## What you may change

Graphite texture and mark-making. Shading and value. Facial naturalism. Fabric
and vestment realism. Architectural detailing that moves nothing. Visual
refinement of any kind.

## What you may not change

Actor positions. Actor facing. Object placement. Object orientation — the
Missal's above all. The number of altar steps. The ordering of actions.
Crossing precedence. Panel count. Camera projection. The presence or absence of
any object the scene requires.

If a plate deviates from its compiled contract, the verdict is **ART FAIL**,
however good the drawing is.

## Three traps, named

1. **The Missal is never mirrored.** Its reading yaw is 135° on the Gospel side
   and 135° on the Epistle side — one number, both sides. The priest turns
   toward the Gospel side to read, wherever the book stands. A yaw of 45° is
   the mirrored value and is forbidden.
2. **Panels are closed.** Each contract lists its panels and sets
   `additional_panels: forbidden`. Do not add an inset, a key, a locator, or a
   plan, however useful one would be. Two scenes declare a second panel; they
   say so.
3. **A projection is not a place.** `nave-front` is a preset resolving to
   projection `perspective` at position `nave-centre`. A label like
   `TOP VIEW (NAVE)` names a projection and a place as one thing and cannot be
   written in this vocabulary.

## What is still open

Four directional phrases have no determinable frame and block their scenes;
`frame-vocabulary.yaml` names each and what a human must decide. Two structural
observations are recorded there too: the mensa depth axis is compiled here
rather than in v0.21, and `mensa-inner-gospel` is defined in the structural
geometry but unused by any scene.
