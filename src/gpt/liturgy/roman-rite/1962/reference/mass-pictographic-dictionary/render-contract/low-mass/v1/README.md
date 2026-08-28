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
render underlay, SVG and raster    render-contract/low-mass/v1/underlays/
        ↓
human structural and render review
        ↓
artistic image edit of the underlay raster
        ↓
artistic acceptance against the contract
```

The structural corpus is the choreography. This layer is the geometry. Art
comes after both, and is bound by both.

The skeleton and the underlay are different artifacts for different readers.
The skeleton is a coordinate schematic with labels and angles, for verification
and regression; it is not what an artist draws from. The underlay is a
projected line drawing with no text at all, in which the geometry itself says
which object is which, and it is the mandatory conditioning input for any
artistic step.

## Files

### Vocabularies

| File | Contents |
| --- | --- |
| `world-frame.yaml` | The one absolute coordinate frame: signed axes, named direction vectors, the yaw convention, and which reference frame each ambiguous phrase belongs to. |
| `frame-vocabulary.yaml` | The frames a directional word can belong to, each ambiguous corpus phrase resolved against them, and the phrases a human must still decide. |
| `missal-orientation.yaml` | The Missal invariant compiled to a single yaw that is identical on both sides, plus the mirrored value that is now forbidden. |
| `sanctuary-master.yaml` | The sanctuary, defined once: the elevation and the standing depth of every named level, the in-plano floor region, the step count, tread and setback, the predella, the altar's body, mensa, gradine, tabernacle and reredos, the fixed anchors of the altar cross and candlesticks, the foot-contact bound, the composition guardrails, and the recorded visual review. It is the authority on how tall a level is and on how far onto its own tread a figure standing there stands; see the next section. |
| `camera-model.yaml` | Projections and camera positions as independent vocabularies, page-direction requirements, named presets with the focal length each preset owns, and the forbidden projection names. |
| `object-model.yaml` | Canonical definitions for every liturgical object the corpus places: scale class, orientation semantics, attachment, and the states each may take. |
| `placement-map.yaml` | The corpus's free-text placements, quoted verbatim, each resolved to held by an actor, positioned at a place the world frame can express, or an explicit refusal to fix either. |
| `panel-contract.yaml` | The default panel manifest and the rule that closes it. |
| `readiness-policy.yaml` | The art gate. It lists only the exceptions: cues judged incapable of changing anything a viewer could see. Everything else blocks. |

### Code

| File | Contents |
| --- | --- |
| `_contract.py` | The shared model. Loads the vocabularies and the approved structural corpus and resolves symbolic scene values — elevations included — into explicit world geometry. |
| `compile.py` | The compiler: symbolic scene → compiled render contract. |
| `skeleton.py` | Deterministic SVG skeleton generator from compiled contracts. |
| `underlay.py` | Projects a compiled contract into a recognizable line drawing, and rasterizes it. |
| `underlay-objects.yaml` | Object geometry: an open Missal is a spread with a spine, a burse a flat case. |
| `review.py` | Generates the verification sheet for the regression fixtures. |
| `validate.py` | Render-contract acceptance checks, including the Missal and panel regressions, foot contact, and the composition guardrails. |
| `camera-calibration.py` | Draws the publication camera beside the alternatives it was chosen over, including the two rejected raises. A debug artifact; see below. |

### Derived output and records

| File | Contents |
| --- | --- |
| `art-readiness.yaml` | Derived inventory of art-ready and art-blocked scenes, with the exact unresolved cue blocking each. |
| `contracts/` | One compiled contract per scene. Generated; never hand-edited. |
| `skeletons/` | One deterministic skeleton per art-ready scene. Generated; never hand-edited. |
| `underlays/` | One render underlay per art-ready scene. Rasters are made on demand by `art-seed`. |
| `review/` | Render-contract verification sheets for the regression fixtures, and the camera calibration sheet. |
| `MANIFEST-AUTHORED.sha256` | Checksums of the authored inputs above. The generated output is deliberately not hashed here, because its `--check` modes prove a stronger thing: that it still matches the inputs it came from. |
| `HANDOFF.md` | Operational record: where the lane stands and how to pick it up. |
| `VALIDATION-UNDERLAY.md` | The underlay validation record, with the camera and geometry history and the measurements behind each decision. |

## Structural ordinals, resolved elevations

The approved structural geometry fixes which sanctuary levels exist, what they
are called, and their order: the floor, three steps, the predella, and the
mensa above them. It gives each a `z` — 0.0, 0.25, 0.50, 0.75, 1.00, and 1.35
for the mensa. Those values are evenly spaced because they are an ordering
device, not a measurement.

Read as measurements they describe a sanctuary nobody has built. The platform
stands at 61 per cent of a standing actor's height, where a real one is nearer
39; and only 0.35 is left between the predella and the mensa, where a priest
working at his altar needs roughly 55 per cent of his own height. That is why
the first full plate read as three figures in front of a large staircase with a
thin slab on top, and why no camera move fixed it. The fault was in the model,
and a camera cannot repair a model.

`sanctuary-master.yaml` resolves the ordinals into elevations:

| Level | Structural `z` | Resolved elevation |
| --- | --- | --- |
| floor | 0.00 | 0.00 |
| step-1 | 0.25 | 0.16 |
| step-2 | 0.50 | 0.32 |
| step-3 | 0.75 | 0.48 |
| predella | 1.00 | 0.64 |
| mensa | 1.35 | 1.55 |

Every level keeps its identity and its order, and only its height changes. One
unit is about 1.06 m against a standing actor of 1.65: a riser of 0.16 is about
17 cm, the platform reaches 39 per cent of an actor, and the mensa stands 0.91
above the predella — 55 per cent of the priest who works at it — so a figure in
plano meets the altar table just below his head.

`_contract.py` applies the table in `elevation()`, `anchor_position()` and
`mensa_z`, so contracts, skeletons and underlays cannot disagree about where a
level is. `underlay.py` and `skeleton.py` read the same file for the rest of
the sanctuary, so nothing rebuilds it independently.

No structural file is touched. `structural/low-mass/v0.21` remains sealed, and
resolving an approved ordinal into an explicit elevation is exactly the work
this layer exists to do.

### The depths are ordinals in the same way

The anchor depths are the same kind of value in the other axis: plano at 0.0,
step-1 at 0.5, step-3 at 1.2, the predella at 1.5, in a sanctuary whose mensa
carries the corporal's nave fold at `y` 1.38. Read as measurements they put an
actor on step-3 past the predella's leading edge, and a priest at the predella
inside the altar.

`sanctuary-master.yaml` resolves each level to a standing depth on its own
tread under `level_depths:`:

| Level | Structural `y` | Standing depth |
| --- | --- | --- |
| plano | 0.00 | 0.00 |
| step-1 | 0.50 | 0.37 |
| step-2 | 0.85 | 0.67 |
| step-3 | 1.20 | 0.97 |
| predella | 1.50 | 1.29 |

`_contract.py` applies the table in `standing_depth()`, keyed on the anchor's
level **and** its canonical depth together. An anchor that shares a level
without standing at that level's depth — the credence, which is on the floor
but beside the steps — is left exactly where it was authored. The mapping is
monotonic, so every depth ordering the corpus relies on survives it.

### The step run

`tread_depth` is 0.30 against a riser of 0.16, with the first leading edge at
0.22. That proportion is an altar's rather than a staircase's, and 0.30 is
also what a *turned* figure needs: a pair of soles rotated 45 degrees spans
about 0.32, so a shallower tread left the priest at the predella standing half
off it. The run is bounded altarward by the mensa, which carries the corporal's
nave fold at `y` 1.38, and that bound is why the altar body's front sits at
1.46.

### The camera moved with the elevations

The `nave-front` preset's station point, `nave-centre`, is now at
`[0.0, -5.6, 1.52]`, 6.9 from the altar, behind a 1520 px lens; it was
`[0.0, -4.2, 1.85]` at 1180. The focal length
belongs to the preset, flows through `compile.py` into each panel as
`focal_length_px`, and is read by `underlay.py` rather than chosen there, so
the composition the contract fixes is the one that gets drawn.

A camera expresses a viewpoint. It must never be moved to compensate for
geometry that is modelled inadequately — that is the error this lane has
already made twice, raising the eye to 2.35 and then 3.6 to rescue a Missal
that was modelled flat. This change is the opposite move: it lowers the eye to
a standing worshipper's height and pulls it back behind a longer lens. It
raises nothing to rescue anything.

The crop is composed around the subject — the altar and the actors — and the
in-plano floor is allowed to run past the frame. Fitting to the widest element
instead let the emptiest one set the scale. The bounds the composition must
hold are numbers in `sanctuary-master.yaml` under `composition:`, so changing
them means arguing with a threshold rather than with a preference.

## Feet on the treads

Standing, kneeling and genuflecting actors all carry explicit flat contact
patches: soles for a standing figure, knees and tucked toes for a kneeling
one, the down knee and the standing foot for a genuflection. `validate.py`'s
`check_foot_contact` proves that every patch lies in the plane of its actor's
level, and that the patch's centre falls on that level's own tread rather than
on the one below. A figure whose foot has left its tread is standing on air,
which is what the earlier flat envelopes did without anyone noticing.

Some overhang is real — altar treads are barely deeper than a foot, and a
turned figure does project past the edge — so it is bounded rather than
forbidden, by `foot_contact.max_overhang_fraction_of_tread`, 0.25. The bound is
measured against the **tread**, not against the patch: a knee, a tucked toe
and a standing sole are very different sizes, and a fraction of the patch would
hold the smallest of them to the tightest tolerance for no reason.

Actors in transit are counted, never silently skipped. A walking figure is
mid-stride between two levels and is standing on neither, so its patches are
reported on their own line in the validator's output.

## Composition guardrails

Fidelity and legibility say nothing about proportion. A drawing can put every
object exactly where the contract compiled it, keep every orientation
readable, and still hand an artistic agent a picture in which the steps take
two-thirds of the height and the altar is a band across the top.

`validate.py`'s `check_composition`, over `panel_composition`, measures five
quantities per panel as fractions of the drawn subject height — the step band,
the altar band, the superstructure band, the floor visible below the lowest
foot, and the tallest actor's height — against thresholds authored in
`sanctuary-master.yaml` under `composition:`. The thresholds live there so that
a later change has to argue with a number rather than with a preference.

`min_superstructure_band_fraction` is the one with teeth, and it exists because
`min_altar_band_fraction` turned out not to have any. Once the elevations are
resolved the altar body is tall by construction, so the altar bound carries a
great deal of slack: flattening the gradine, tabernacle, reredos, cross and
candlesticks onto the mensa still passes it. What can actually vanish is the
mass *above* the mensa, and it is what makes the shape read as an altar rather
than as a table, so it is measured separately at a floor of 0.28 — a bound that
sits between the built value and the flattened one and therefore fires.
`VALIDATION-UNDERLAY.md` records the measurements.

In-sanctuary panels — the over-the-shoulder presets, whose eye already stands
altarward of the first step — are exempt by design, because they show neither
the full step run nor the floor below the servers' feet, and they are counted
rather than skipped.

## The visual review gate

Every automated check in this layer passed while the picture was wrong. They
compared world-space numbers to world-space numbers and never asked what
reached the page, and a threshold only refuses the failures somebody already
thought of. So the publication composition is additionally gated on someone
having looked at the canary.

`sanctuary-master.yaml` records that review under `underlay_visual_review:` —
its status, the canary `LM-001A`, the preset, and a digest over the five
files that decide what the picture looks like: `sanctuary-master.yaml`,
`camera-model.yaml`, `underlay.py`, `underlay-objects.yaml` and
`_contract.py`. `scripts/_pictographic.py`'s
`require_visual_review()` makes `art-seed` refuse both an unapproved preset and
an approval whose geometry has since moved, so a preset nobody has looked at is
treated exactly like a preset somebody rejected.

```sh
./tools/tpt pictographic composition-review roman-1962 low-mass
./tools/tpt pictographic composition-review roman-1962 low-mass --refresh
```

The first reports; the second records the current composition as reviewed.
Refreshing the digest without re-rendering the canary and looking at it is the
one move this gate exists to prevent.

## Two objects remodelled, not re-lit

Two objects were found to be modelled as something other than what they are.
Both were fixed in the object, which is the only instrument this layer permits;
neither was fixed by moving the camera.

The **burse** now declares a support pitch of 78 degrees, standing upright
against the gradine as a stiff square case does, rather than lying flat on the
altar cloth. Modelled flat it collapsed to 2.9 degrees from collinear at a nave
eye, and the legibility check duly advised raising the camera — the move this
layer forbids. Separately, `projected_orientation()` used to build its expected
direction from yaw alone whenever an object published no pitched vector, so the
drawing applied the pitch and the expectation did not; it now builds from the
yaw **and** the declared support pitch.

The **paten** lying flat is exempted from the legibility floor by
`legibility.exempt_when_flat` in `underlay-objects.yaml`. A disc has no readable
page-up in the picture because it has none in the room: turn it on the corporal
and nothing about it looks different. The exemption is narrow on purpose — it
never applies to fidelity, it dies the moment the paten is pitched or picked
up, and held under the chin at the Communion the same paten measures 90 degrees
of separation. Flat unpitched objects taking the exemption are counted in the
validator's output, so it can never be silent.

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
**`STRUCTURE = FAIL`**, however good the drawing is. Aesthetic quality is not a
defence for moved geometry. The contract is checkable; the check governs.

`STRUCTURE` and `ART` are two independent gates, defined in
[`../../../artistic/RENDERING-PROTOCOL.md`](../../../artistic/RENDERING-PROTOCOL.md).
`STRUCTURE` asks whether the plate is faithful to this contract; `ART` asks
whether it is publication quality. Deviating geometry fails the first, and
never reaches the second.

## Art readiness

A scene compiles to a contract only if every visible thing in it is resolved.
The structural corpus deliberately left serving-profile cues open rather than
inventing them, and some of those cues would change what a viewer sees.

Any such scene is marked `BLOCKED_FOR_ART` with the exact cue naming what a
human must decide. A blocked scene is not a defect and must not be cleared by
guessing, and never from the fenced pre-v0.21 guides. `art-readiness.yaml` is
derived by the compiler, so the block cannot drift from the reason for it.

## Seeding an artistic lane

`art-seed` emits the entire fresh-web handoff, the prompt included. A human used
to write that prompt by hand, restating the repository, the commit, the scene's
readiness, its panel manifest and what is visibly true in it. Written by hand it
was rewritten every time, and a prompt nobody can diff is a prompt nobody
reviewed. It is now generated from the compiled contract and from git.

```sh
./tools/tpt pictographic art-seed roman-1962 low-mass LM-001A
```

The operator workflow is six steps and does not vary by scene:

1. run the command above;
2. attach the entire emitted package to a fresh ChatGPT web conversation;
3. open `WEB-AGENT-PROMPT.md` and paste it verbatim;
4. the web agent **edits** `render-underlay.png`, and never composes a fresh
   picture;
5. it generates exactly one candidate and stops;
6. a human reviews `STRUCTURE`, and only once `STRUCTURE` passes does anyone
   review `ART`.

This README does not reproduce the prompt. It is generated per scene from that
scene's contract, and a copy kept here would be a second version to keep in
step with the first.

### What the package holds

Eight files, written to `build/art-seed/<SCENE>/` unless `--out` names
somewhere else:

| File | What it is |
| --- | --- |
| `render-underlay.png` | The mandatory image-edit source, and the authority on what is visible. |
| `render-underlay.svg` | The same drawing as vectors. |
| `render-contract.yaml` | The compiled geometry in numbers: the numeric and semantic authority when a plate is reviewed. |
| `skeleton.svg` | The diagnostic schematic, with its labels and angles. Supporting reference only, and never the conditioning image. |
| `ART-AGENT-INSTRUCTIONS.md` | The generated scene-art rules, with the canary note where it applies. |
| `provenance.yaml` | Plate identity, readiness, panel manifest, seed commit, and the underlay's hash and dimensions. |
| `PACKAGE-MANIFEST.yaml` | The machine-readable inventory: `schema`, `package_type`, `canonical`, `repository`, `branch`, `seed_commit`, `plate_id`, `scene_ids`, `structural_baseline_commit`, `render_contract_version`, `art_readiness`, `is_pipeline_canary`, `mandatory_edit_source`, `generation_mode`, `web_prompt`, `panel_manifest`, `additional_panels`, `structure_review`, `art_review`, and a `files` list of path, `sha256` and role. Both review gates start `PENDING` and are never auto-approved. |
| `WEB-AGENT-PROMPT.md` | The generated fresh-web prompt: the one document the operator opens and pastes. |

That order is the order of authority, and the prompt states it as well.
`render-underlay.png` owns what is visible; `render-contract.yaml` settles a
numeric question during review; `skeleton.svg` is a debugging view and is never
the image the model conditions on.

### The prompt generator knows nothing about Low Mass

`scripts/_pictographic_web.py` writes the prompt. It is handed a compiled
contract, the camera model and the sanctuary master, and it knows nothing about
Low Mass, two servers, one panel or `LM-001A`. Every scene-specific sentence —
where each actor stands and faces, which page side that lands on, what each
actor holds or carries, where every visible object sits and what supports it —
is generated from scene data, so the same generator serves the sung and
pontifical forms as soon as their contracts exist.

The division of labour with the protocol is deliberate.
[`../../../artistic/RENDERING-PROTOCOL.md`](../../../artistic/RENDERING-PROTOCOL.md)
holds the timeless rules, and must never carry a commit hash or a scene-specific
fact. `WEB-AGENT-PROMPT.md` holds the current facts: repository, branch, the
exact seed commit, scene identity, readiness, the panel manifest, canary status,
and a visible-invariant summary of this scene. The two bolded lists in the
protocol's section 6 — what the artist owns, and what the render contract
reserves — are read out of the protocol rather than restated in the generator,
so the two cannot drift. If the protocol ever stops stating them in a form the
generator can read, generation fails rather than inventing the rule.

### The package names an exact commit

A canonical package claims a seed commit, and the claim has to be worth
something: a reader must be able to check that commit out and regenerate the
same package. So `art-seed` refuses a dirty working tree rather than naming a
commit whose tree is not the tree that was packaged.

`--development` seeds from an uncommitted tree and produces an explicitly
NONCANONICAL package, labelled as such in the console output, in the prompt's
banner, in `PACKAGE-MANIFEST.yaml` (`package_type:
pictographic-art-seed-development`, `canonical: false`) and in provenance. It is
for working on the pipeline, and must never be used for a real plate.

### Fail closed

`art-seed` refuses, writing nothing, when:

- the scene is `BLOCKED_FOR_ART`;
- the composition review is unapproved or stale;
- the render contract will not compile;
- a render-critical placement is unresolved;
- a visible object has no recognizable underlay geometry;
- the panel manifest disagrees with the skeleton;
- rasterization fails;
- the working tree is dirty, in canonical mode;
- the scene summary cannot be generated for a render-critical field;
- the summary contradicts the contract;
- a required prompt section is missing;
- a file in the package has no declared role.

Any failure reached after the package directory exists deletes the partial
package. A half-valid seed — every file but the prompt, say — is exactly the
package that sends a human back to writing a prompt by hand, so none is ever
left attachable.

### What the console prints

`ART SEED READY: <scene>`, the package path, the commit, branch and repository,
the panel manifest, the canary line where it applies, and the six-step
fresh-web workflow. It deliberately does not dump the prompt to stdout: the
prompt is a file to attach and paste, and a copy scrolled past in a terminal is
the copy somebody edits.

## The camera calibration sheet

`camera-calibration.py` writes `review/camera-calibration-v1.svg`: six
candidate cameras drawn against the same scene and the same sanctuary, with the
published one boxed, and the rejected raises to 2.35 and 3.60 kept on the sheet
on purpose. They are the argument against moving a camera to rescue an object,
and it is much easier to make when the raised camera is beside the published
one. The cells are drawn by `underlay.py` and styled by it, so the sheet cannot
drift away from what the plate draws.

It is a **debug artifact**. It is never a panel, never part of an art-seed
package, and never shown to an artistic agent. Like the other generators it has
a `--check` mode.

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
./tools/tpt pictographic art-seed roman-1962 low-mass LM-001A
```

To regenerate and to prove the tracked output is current:

```sh
./compile.py && ./skeleton.py && ./underlay.py && ./review.py \
    && ./camera-calibration.py
./compile.py --check && ./skeleton.py --check && ./underlay.py --check \
    && ./review.py --check && ./camera-calibration.py --check
```
