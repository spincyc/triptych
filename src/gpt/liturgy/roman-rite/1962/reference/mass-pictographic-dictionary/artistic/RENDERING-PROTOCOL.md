# Artistic rendering protocol — Mass pictographic dictionary

Durable project architecture. This document states the rules that govern every
artistic rendering lane for this owner, and it is meant to outlive any
particular lane, agent, or conversation.

It is deliberately **timeless**. It carries no scene counts, no commit hashes,
and no current status: those live in tooling and in the continuation handoff,
where they can be regenerated instead of going stale. See
[`../render-contract/low-mass/v1/HANDOFF.md`](../render-contract/low-mass/v1/HANDOFF.md)
for the current operational state.

## Why this exists

A first artistic plate was generated from the approved structural corpus. It
was attractive, and it was wrong twice: it drew the Missal mirrored, and it
invented an auxiliary inset labelled `TOP VIEW (NAVE)`.

Neither was a failure of skill. The renderer was handed prose — an
`orientation:` string and a scene description — and prose admits
interpretation. It resolved "left" against the priest's body instead of the
world, and nothing told it that the set of panels was closed.

The render-contract layer answered that by compiling the approved semantics
into explicit geometry. This protocol answers the remaining half: making the
compiled geometry the **only** door into the artistic stage, so that no future
lane can reach an image generator by a path that skips it.

A later attempt went wrong with the contract right. The compiled geometry was
correct and the deterministic skeleton was correct, and the drawing still put
the book on the wrong side, because the skeleton was never a picture: it draws
every object as the same small mark and lets a text label carry the meaning, so
the Missal, the burse, the chalice and the corporal arrive as four identical
squares. An image model given that must reconstruct what an open book looks
like and guess which square it was. The render underlay closes that last hop by
projecting the same compiled geometry into a drawing whose shapes say what they
are, so the artist edits the scene instead of reassembling it.

## The pipeline

```text
approved structural corpus
        ↓
compiled render contract
        ↓
deterministic skeleton                 coordinate verification
        ↓
render underlay, SVG and raster        the drawing the artist edits
        ↓
artistic image edit of that raster
        ↓
raw scene art
        ↓
STRUCTURE acceptance gate
        ↓
ART acceptance gate
        ↓
publication compositor
        ↓
approved artistic plate
```

The structural corpus describes approved **choreography**. The compiled render
contract and its skeleton describe what may actually be **drawn**. These are
different questions, and the second is the artist's input.

The underlay is that second answer made visible. It is generated from the same
compiled contract, projected through the contract's own declared camera, so it
cannot disagree with the contract about what is being looked at or from where.
The artist receives a picture of the scene rather than a description of one.

## 1. The only valid artistic input path

An artistic plate may be generated from exactly four things:

1. an **art-ready** scene or scene cluster;
2. its **compiled render contract**;
3. its **deterministic skeleton**;
4. its **render underlay**, vector and raster.

The underlay raster is the mandatory conditioning input, and the artistic step
is an image **edit** of it. The finished art is that same drawing raised to
publication quality on the geometry it already carries. Where the tool in use
cannot take an image as an edit source, the lane stops and reports that
limitation; it does not fall back to composing a fresh picture.

These are forbidden as canonical production paths:

```text
structural YAML       → free-form image prompt            FORBIDDEN
human prose summary   → free-form image prompt            FORBIDDEN
diagnostic skeleton   → image model, with no underlay     FORBIDDEN
any description       → text-to-image restaging           FORBIDDEN
```

A diagnostic skeleton alone is not sufficient visual conditioning. It is a
coordinate schematic whose objects are told apart by their labels, so a model
working from it decides for itself which anonymous mark was the open book, and
a model that decides that wrongly is indistinguishable from one that never saw
the contract.

Text-to-image restaging is not a canonical path either, however careful the
description and however faithfully it was derived from the compiled contract. A
description of geometry is prose again, and prose admitting interpretation is
the defect this whole layer was built to remove. A picture generated beside the
underlay rather than out of it has been staged by the model, not by the
contract, whatever it happens to resemble.

A future agent may read structural material for context, and should: knowing
what the moment *is* makes a better drawing. But the geometry it draws comes
from the compiled contract, its underlay and its skeleton, never from a
paraphrase of them.

The sanctioned way to obtain those four things is the seed command documented
in the handoff. It generates the underlay itself and refuses to write a package
without it, so that assembling the input by hand — and quietly omitting a part
of it — is not the easy path.

## 2. Four artifacts, and they are not interchangeable

The pipeline produces four visual things, and a hurried reader will conflate
them. They have different readers, different rules about text, and only one of
them is what the artist draws from.

| Artifact | Its reader | Text | Role in the artistic step |
| --- | --- | --- | --- |
| Diagnostic skeleton | A human checking coordinates | Labels, angles and banners | Supporting reference only |
| Render underlay, SVG and PNG | The image model | None at all | The mandatory edit source |
| Raw scene art | The reviewers, at both gates | None | What the artist returns |
| Publication plate | The reader of the finished work | Deterministic typography | Composed after both gates, without the artist |

**The diagnostic skeleton may remain schematic and labelled precisely because
it is not what the artist draws from.** Its reader is a human verifying that a
number in the contract reached the drawing, and that reader is helped by seeing
the yaw written beside the mark it belongs to. Making the skeleton prettier
would cost the reviewer clarity and buy the artist nothing.

The underlay carries no text of any kind, for the mirror-image reason. Its
reader will render whatever it is shown, so a label on the conditioning image
comes back baked into the plate as pixels nobody can correct. The underlay
therefore says everything through geometry: an open Missal is a spread of two
page planes with a spine, a burse is a flat closed case, a chalice is a cup on
a stem, an actor is a body envelope with readable facing, and the altar's steps
and predella are volumes with depth. A viewer who reads nothing can name each
one, and can see which side of the altar the book stands on.

Raw scene art is the scene and nothing around it. The publication plate is that
art after a deterministic composition step, defined in
[`publication-compositor.md`](publication-compositor.md). The two are recorded
separately in provenance because they are approved separately: the gates are
decided on the raw art, and the plate is what publication does with an approved
one.

## 3. Raw art carries no publication furniture

The image model returns the drawn scene. It does not produce a title, a
caption, a plate identifier, metadata, a source citation, a border, a header, a
footer or pagination, and it does not write descriptive prose into the image.

The reason is not tidiness. Every one of those is deterministic typography set
from data that already exists: the plate identifier and the baseline commit are
in the provenance record, the caption is authored and reviewed as text, and the
border and measure belong to a template the whole edition shares. A model that
invents them instead produces sentences nobody wrote and no review pass caught,
rendered as pixels where they cannot be corrected, checked, translated or
diffed. Unreviewable text is worse than absent text, because it reads as
authoritative.

This also keeps the project's governing artwork rule, in
`guidance/liturgy/roman-1962-pictorial-dictionaries.md`, which requires
generated artwork to contain no words, letters, arrows or numerals at all.
Publication furniture is added afterwards, by the compositor, to a plate that
has already passed both gates.

## 4. Art-readiness is a hard gate

> A scene marked `BLOCKED_FOR_ART`, or otherwise not `ready`, must not be
> artistically rendered.

The readiness status itself is `ready` or `blocked`. The seed command refuses a
blocked scene with the token `BLOCKED_FOR_ART`, and a blocked scene's skeleton
carries the banner `BLOCKED FOR ART` with its cue count. All three name the same
state.

**Blocked means stop.** It does not mean proceed carefully.

A renderer facing a blocked scene may not:

- infer the missing cue;
- resolve it from an older fenced guide, and the `altar-server-guides/` tree is
  fenced and superseded;
- make an aesthetic guess;
- substitute a likely custom, however common.

A blocked scene names the exact cue that blocks it. Resolving that cue is human
work, done in the structural or render-contract lane, and the scene becomes
art-ready by that resolution — never by an artist deciding it looked fine.

Readiness is discoverable from tooling, and only from tooling. Do not copy
counts of ready and blocked scenes into prose: they will drift, and a stale
count is worse than no count because it invites trust.

## 5. Two independent approval gates

Every artistic plate carries two statuses, decided separately.

| Gate | Question | Values |
| --- | --- | --- |
| `STRUCTURE` | Is it faithful to the compiled render contract and skeleton? | `PASS` · `FAIL` · `PENDING` |
| `ART` | Is it publication quality, in the project's visual language? | `PASS` · `FAIL` · `PENDING` |

A plate is approved only when:

```text
STRUCTURE = PASS
ART       = PASS
```

A beautiful image with the wrong actor position, actor facing, object
placement, object orientation, Missal orientation, path, crossing order, step
geometry, camera, projection, or panel count is `STRUCTURE = FAIL`. It does not
proceed to aesthetic review, and it is not rescued by being good.

**There is no "approved with notes" for a structural violation.** That verdict
exists for taste, where reasonable people differ. Geometry is checkable, and a
plate that fails the check is simply not the scene it claims to be.

The verdict tokens are uppercase because that is how the tooling prints them.
Where a plate record is validated alongside this repository's artwork
manifests, whose review values are `pending`, `passed`, `failed` and
`not-applicable`, `PENDING`/`PASS`/`FAIL` map onto the first three; a gate that
genuinely does not apply is recorded as `not-applicable` rather than forced to
a verdict.

Order matters: `STRUCTURE` is decided first. Reviewing the art of a plate that
depicts the wrong thing wastes the reviewer and flatters the error.

## 6. What the artist owns

The compiled contract is the geometric truth, and the underlay is that truth
drawn. An artist may beautify it. An artist may not restage it.

**Owned by the artist** — graphite and pencil texture; line quality and weight;
shading and value; facial naturalism; fabric and vestment realism;
architectural detail that moves nothing; surface finish; artistic polish;
visual hierarchy within the declared panel.

**Owned by the render contract, and not the artist** — choreography; actor
anchors; actor facing; object transforms; Missal orientation; object
possession; crossing precedence; the number of altar steps; the world-side
mapping of Gospel and Epistle; camera projection; declared panel count;
required visible objects; branch selection.

The division is not about authority for its own sake. Everything in the second
list was decided by a human against the rubrics and approved once; re-deciding
it in a drawing discards that review silently.

## 7. No invented panels or viewpoints

A plate contains exactly the panels its compiled contract declares. One
declared panel means one panel in the finished plate.

No generator may add a top-view inset, a detail inset, a decorative vignette,
an alternate angle, or a "helpful" diagram unless it appears in the panel
manifest. Every contract states `additional_panels: forbidden`, and that is
the whole rule.

If an extra panel would genuinely help, it is added to the contract and
reviewed there. A panel nobody declared is geometry nobody checked.

This is the rule that the invalid inset violated. That label also conflated a
projection with a camera position, which the camera model now makes
unspellable; the label is recorded here only as the defect it was, and is not
an accepted taxonomy anywhere in this project.

## 8. The Missal is a known failure mode

Call it out by name, because it failed first and will fail first again.

The approved rule is that wherever the Missal is placed, the priest reading it
turns toward the left of the canonical world frame. It is **not** mirrored when
it changes side. The render contract compiles that rule to one fixed
world-space reading orientation, identical on the Epistle and Gospel sides, and
that compiled value is authoritative — it is not restated numerically here,
because a number in two places is a number that will eventually disagree with
itself.

The artist must not mirror the Missal, must not rotate it for composition, and
must not infer its orientation from which side of the altar it stands on. The
skeleton's Missal transform is preserved exactly enough that the priest's
reading orientation stays correct.

The underlay now embodies that compiled orientation as drawn geometry rather
than as an annotation beside it. The book arrives in the conditioning image
already open, already turned the compiled way, and already projected through
the contract's own camera, so the artist preserves the orientation by editing
what is there instead of by reading a number and applying it. A plate in which
the book has changed side but kept its reading orientation is right; one in
which it has mirrored is `STRUCTURE = FAIL`, and set beside the underlay that
difference is visible without measuring anything.

## 9. LM-001A is the pipeline canary

`LM-001A` — the arrival at the foot of the altar, the opening state of the Mass
— is the canary for the whole artistic pipeline.

Before a fresh artistic lane begins style development, `LM-001A` is rendered by
editing its current render underlay, generated from its current compiled render
contract, and checked for:

- the declared panel count, and no other panel;
- no invented inset;
- the correct camera and projection;
- correct Missal placement;
- correct Missal orientation;
- correct AC1 and AC2 sides;
- correct altar, step and predella geometry.

The lane proceeds only once `LM-001A` reaches `STRUCTURE = PASS`. It need not
reach `ART = PASS` first — the canary is a fine subject for style experiments —
but the geometry passes before style work begins.

**If `LM-001A` fails structurally, stop the artistic lane and diagnose the
pipeline.** It is the simplest scene in the corpus: three figures in a line, an
open book, an altar. A pipeline that cannot draw it correctly will not draw the
Consecration correctly, and pressing on only produces more plates to throw away.

## 10. Provenance for every plate

Every canonical artistic plate is traceable back to the geometry it claims to
depict. The field set is defined in
[`plate-provenance.yaml`](plate-provenance.yaml), which the later persistence
lane and the web lane both use so that they mean the same things by the same
words.

No plate registry is built yet, and building one before there are plates would
be premature. The contract is defined now so that when plates arrive they are
recorded consistently rather than retrofitted.

## 11. Fail closed

The canonical entry path refuses rather than degrades. It will not seed an
artistic lane when the scene is blocked, when the render contract cannot
compile, when skeleton generation fails, when the declared and drawn panel
manifests disagree, when a render-critical transform is unresolved, or when
provenance is missing.

It refuses on the same terms for the conditioning image. A scene whose underlay
cannot be generated or rasterized is not seeded, and neither is one holding a
visible object with no recognizable underlay geometry, because the alternative
is shipping that object as an anonymous mark and inviting the artist to guess
what it was. The remedy is to give the object a silhouette in the underlay
library, not to seed the lane without one. A refusal leaves no partial package
behind, since a package missing its edit source is exactly the weak package
that invites restaging.

There is no `--force`. A human who needs to override any of this resolves the
underlying cue in the proper lane, where the decision is recorded and reviewed.
An override that leaves no trace is indistinguishable from the failure it
bypasses.
