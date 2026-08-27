# Render contract — spoken 1962 Low Mass, two servers, v1

Status: **render contract v1**, downstream of the approved structural corpus.

Structural choreography: **still v0.21, unchanged**. Nothing in this directory
revises the approved Mass. Sealed structural baseline: `d2e97b5ca`.

Artistic rendering: **not started**, and this lane does not start it.

## Why this layer exists

The structural corpus records that the Missal is
`orientation: priest-reads-facing-left`. That sentence is true, approved, and
insufficient. The first generated artistic plate read it, resolved "left"
against the priest's own body rather than the world, and drew the book
mirrored. The same plate invented an inset labelled `TOP VIEW (NAVE)` — a
label that names a projection and a place as if they were one thing, which was
possible only because nothing said a panel list is closed.

Both failures share a cause: the corpus expressed geometry as prose, and prose
admits interpretation. This layer removes the interpretation. It compiles the
approved semantics into explicit world geometry, so that the wrong picture is
not a misreading a renderer could make but a different number the validator
rejects.

## The pipeline

```text
rubric and approved choreography
        ↓
structural scene corpus            structural/low-mass/v0.21/scenes/
        ↓
render-contract compiler           render-contract/low-mass/v1/compile.py
        ↓
compiled per-scene render contract render-contract/low-mass/v1/contracts/
        ↓
deterministic skeleton SVG         render-contract/low-mass/v1/skeletons/
        ↓
human structural and render review
        ↓
art generation, using the skeleton as its reference
        ↓
artistic acceptance against the contract
```

The structural corpus is the choreography. This layer is the geometry. Art
comes after both, and is bound by both.

## Files

| File | Contents |
| --- | --- |
| `world-frame.yaml` | The one absolute coordinate frame: signed axes, named direction vectors, the yaw convention, and which reference frame each ambiguous phrase belongs to. |
| `missal-orientation.yaml` | The Missal invariant compiled to a single yaw that is identical on both sides, plus the mirrored value that is now forbidden. |
| `camera-model.yaml` | Projections and camera positions as independent vocabularies, page-direction requirements, named presets, and the forbidden projection names. |
| `object-model.yaml` | Canonical definitions for every liturgical object the corpus places: scale class, orientation semantics, attachment, and the states each may take. |
| `panel-contract.yaml` | The default panel manifest and the rule that closes it. |
| `compile.py` | The compiler: symbolic scene → compiled render contract. |
| `skeleton.py` | Deterministic SVG skeleton generator from compiled contracts. |
| `validate.py` | Render-contract acceptance checks, including the Missal and panel regressions. |
| `art-readiness.yaml` | Derived inventory of art-ready and art-blocked scenes, with the exact unresolved cue blocking each. |
| `contracts/` | One compiled contract per scene. Generated; never hand-edited. |
| `skeletons/` | One deterministic skeleton per art-ready scene. Generated; never hand-edited. |
| `review/` | Render-contract verification sheets for the regression fixtures. |

## What the artist may and may not change

The skeleton is the geometric truth. An art generator may beautify it. It may
not restage it.

**Allowed** — graphite texture and mark-making; shading and value; facial
naturalism; fabric and vestment realism; architectural detailing that does not
move anything; general visual refinement.

**Not allowed** — actor positions; actor facing; object placement; object
orientation, the Missal's above all; the number of altar steps; the ordering of
actions; crossing precedence; panel count; camera projection; adding or
removing any object the scene requires.

### Failure policy

If a generated plate deviates from its compiled render contract, the verdict is
**ART FAIL**, however good the drawing is. Aesthetic quality is not a defence
for moved geometry. The contract is checkable; the check governs.

## Art readiness

A scene compiles to a contract only if every visible thing in it is resolved.
The structural corpus deliberately left serving-profile cues open rather than
inventing them, and some of those cues would change what a viewer sees.

Any such scene is marked `BLOCKED_FOR_ART` with the exact cue naming what a
human must decide. A blocked scene is not a defect and must not be cleared by
guessing, and never from the fenced pre-v0.21 guides. `art-readiness.yaml` is
derived by the compiler, so the block cannot drift from the reason for it.

## Versioning

This is `render-contract/low-mass/v1`. The structural corpus remains
`structural/low-mass/v0.21`. The two version independently on purpose: a
render-contract revision does not touch approved choreography, and a
choreography revision would require human approval that this lane does not
have. Nothing here is `structural v0.22`.

## Commands

From the repository root:

```sh
./tools/tpt pictographic render-contract roman-1962 low-mass LM-001A
./tools/tpt pictographic skeleton roman-1962 low-mass LM-001A
./tools/tpt pictographic readiness roman-1962 low-mass
```

To regenerate and to prove the tracked output is current:

```sh
./tools/tpt pictographic compile-all roman-1962 low-mass
./tools/tpt pictographic compile-all roman-1962 low-mass --check
```
