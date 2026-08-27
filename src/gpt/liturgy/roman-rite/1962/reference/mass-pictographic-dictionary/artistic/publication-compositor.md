# Publication compositor — Mass pictographic dictionary

Durable interface. This document defines the layer that turns approved raw
scene art into a finished plate, and it is written before that layer exists.

**No compositor is built yet, and building one before there are approved plates
would be premature.** The interface is defined now for the reason the
[plate provenance contract](plate-provenance.yaml) was: the human-guided web
lane and a later CLI lane must mean the same things by the same words, so that
nothing has to be retrofitted once plates start arriving. Until it is built, an
approved plate is its raw scene art together with its provenance record, and no
publication furniture is drawn anywhere by anyone.

The rules governing everything upstream are in
[`RENDERING-PROTOCOL.md`](RENDERING-PROTOCOL.md), which this document does not
restate. The one it depends on is the section on publication furniture: the
image model returns the scene and nothing around it.

## What it accepts

1. **Approved raw scene art**: the artist's image edit of the render underlay,
   scene only, with both gates decided on it.
2. The plate's **provenance record**, in the fields of
   [`plate-provenance.yaml`](plate-provenance.yaml): plate id, scene ids,
   structural baseline commit, render-contract version, panel manifest, and
   both gate verdicts.
3. A **publication template**: the typographic and layout decisions an edition
   shares, being typeface, measure, margins, border, caption placement and
   pagination.
4. The plate's **caption**, authored and reviewed as text, separately from the
   image and by a human.

## What it produces

One publication plate, and a record of what was applied to make it. The
composition is deterministic: the same art, record and template produce the
same plate, so a plate can be regenerated from its inputs rather than kept as
the only copy of a decision.

## What it may add

The plate identifier, the title, the separately authored caption, source and
provenance metadata, a border, pagination and layout framing.

Everything in that list is typography or geometry it was handed. The compositor
composes text; it does not write text. Nothing it adds may cover, crop,
recompose or otherwise alter the approved scene art, because the art it was
given is the art that passed the gates.

## When it may run

Only after both gates have passed:

```text
STRUCTURE = PASS
ART       = PASS
```

Composing before that produces a finished-looking plate of an unreviewed image,
which is worse than no plate: publication furniture reads as a claim that the
thing inside the border was checked. A plate that fails either gate is not
composed, and the failure is fixed in the lane that owns it.

## What never invokes it

`art-seed` never invokes it. That command is the entrance to the artistic
stage, and the compositor is the exit from it; the two are separated so that a
lane cannot reach publication without passing the gates in between.

The image model never invokes it either, is never handed the template, and
never sees the caption. It does not write the caption and it does not typeset
the page. Those are separate acts of authorship and typography, done by a human
and by deterministic code, and an image model performing them silently would
put unreviewable words into a published plate.
