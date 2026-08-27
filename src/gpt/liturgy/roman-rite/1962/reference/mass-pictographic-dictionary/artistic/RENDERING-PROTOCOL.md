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

## The pipeline

```text
approved structural corpus
        ↓
compiled render contract
        ↓
deterministic skeleton
        ↓
STRUCTURE acceptance gate
        ↓
artistic rendering constrained by the skeleton
        ↓
ART acceptance gate
        ↓
approved artistic plate
```

The structural corpus describes approved **choreography**. The compiled render
contract and its skeleton describe what may actually be **drawn**. These are
different questions, and the second is the artist's input.

## 1. The only valid artistic input path

An artistic plate may be generated from exactly three things:

1. an **art-ready** scene or scene cluster;
2. its **compiled render contract**;
3. its **deterministic skeleton**.

These are forbidden as canonical production paths:

```text
structural YAML      → free-form image prompt        FORBIDDEN
human prose summary  → free-form image prompt        FORBIDDEN
```

A future agent may read structural material for context, and should: knowing
what the moment *is* makes a better drawing. But the geometry it draws comes
from the compiled contract and the skeleton, never from a paraphrase of them.

The sanctioned way to obtain those three things is the seed command documented
in the handoff. It exists so that assembling the input package by hand — and
quietly omitting a part of it — is not the easy path.

## 2. Art-readiness is a hard gate

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

## 3. Two independent approval gates

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

## 4. What the artist owns

The skeleton is the geometric truth. An artist may beautify it. An artist may
not restage it.

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

## 5. No invented panels or viewpoints

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

## 6. The Missal is a known failure mode

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

## 7. LM-001A is the pipeline canary

`LM-001A` — the arrival at the foot of the altar, the opening state of the Mass
— is the canary for the whole artistic pipeline.

Before a fresh artistic lane begins style development, `LM-001A` is rendered
from its current compiled render contract and its current deterministic
skeleton, and checked for:

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

## 8. Provenance for every plate

Every canonical artistic plate is traceable back to the geometry it claims to
depict. The field set is defined in
[`plate-provenance.yaml`](plate-provenance.yaml), which the later persistence
lane and the web lane both use so that they mean the same things by the same
words.

No plate registry is built yet, and building one before there are plates would
be premature. The contract is defined now so that when plates arrive they are
recorded consistently rather than retrofitted.

## 9. Fail closed

The canonical entry path refuses rather than degrades. It will not seed an
artistic lane when the scene is blocked, when the render contract cannot
compile, when skeleton generation fails, when the declared and drawn panel
manifests disagree, when a render-critical transform is unresolved, or when
provenance is missing.

There is no `--force`. A human who needs to override any of this resolves the
underlying cue in the proper lane, where the decision is recorded and reviewed.
An override that leaves no trace is indistinguishable from the failure it
bypasses.
