# Staleness review — 2026-07-29

> **Historical / pre-v0.21.** This record predates the human-approved
> structural checkpoint for the spoken 1962 Low Mass at
> `src/gpt/liturgy/roman-rite/1962/reference/mass-pictographic-dictionary/`
> and has not been reconciled to it. Its elevation bell grouping,
> conditional `Domine, non sum dignus` rings, second-ablution liquid, and
> post-ablution transfer object are not inputs for that pictographic lane.
> See `guidance/liturgy/roman-1962-server-training.md`.
> In this file, a verification of 'no disagreement' means agreement
> with this guide's own declared teaching model, not with the v0.21
> pictographic baseline.

## Trigger and method

`scripts/research-staleness explain gpt
liturgy/roman-rite/1962/reference/altar-server-guides/01-low-mass` identified
this edition's `research/guide-map.md` as the sole changed input. No Claude
edition exists for this leaf.

Both required ignored candidates were prepared:

- `modified/` is an exact copy of the current source plus a candidate note,
  because the current render source already incorporates the changed map; and
- `rewritten/` is a new reader-facing treatment drafted from the changed guide
  map before the current publication prose was consulted. It preserves the
  shared response and ceremony owners rather than inventing received text.

“Old” below means the currently installed/source publication evaluated by this
review, not an earlier Git revision of the guide map. “Modified” means the
minimal candidate, and “rewritten” means the independent treatment.

## Per-claim comparison

| Consequential claim in the changed research | Effect of changed research | Old publication | Modified candidate | Rewritten candidate | Substantive result |
|---|---|---|---|---|---|
| At the principal Gospel opening, First remains by the book until the priest begins reading while Second stands laterally clear at the same level; corrected plate `ASG-ART-027` depicts that opening state. | Strengthens and clarifies the former finish-state description; supersedes the old plate. | Already states the waiting interval and renders `ASG-ART-027`. | Identical. | Independently assigns First to the book and Second laterally clear until the priest begins. | No disagreement. |
| The Offertory cruet service is side-by-side, represented by corrected plate `ASG-ART-028`. | Strengthens the spatial model and replaces a superseded scene. | Already gives the side-by-side service action and renders `ASG-ART-028`. | Identical. | Independently specifies First with wine and Second with water in the side-by-side formation. | No disagreement. |
| First alone serves both post-Communion cruets in sequence; corrected plate `ASG-ART-029` depicts both moments. | Corrects the role/object assignment and strengthens its visual account. | Already assigns both cruets and both ablution moments to First and renders `ASG-ART-029`. | Identical. | Independently assigns both sequential ablutions to First while Second remains clear. | No disagreement. |
| After the ablutions, First carries the folded chalice veil Epistle-to-Gospel while Second returns the Missal Gospel-to-Epistle; neither carries the chalice; the priest covers and centers it. Corrected plate `ASG-ART-031` depicts the simultaneous exchange. | Adds the veil handoff and coordinated exchange, and contradicts the superseded loose-veil route. | Already teaches the simultaneous exchange, center reverence, return to normal sides, and the priest-only chalice handling; it renders `ASG-ART-031`. | Identical. | Independently reconstructs the same object ownership, opposite-direction move, center reverence, and chalice boundary. | No disagreement. |
| Superseded plates `ASG-ART-012`, `013`, `017`, `018`, and `019` no longer render; selected corrected plates and `ASG-ART-026` do. | Removes obsolete visual evidence and strengthens correspondence between the model and its scenes. | Import inspection confirms the corrected scene macros and no Low Mass rendering of the superseded plates. | Identical. | Names the corrected ceremonial states in prose and makes no claim to reuse obsolete art. | No substantive disagreement; visual implementation is intentionally deferred in the rewrite. |
| The exact snapshot is a twenty-six-page installed Alpha whose build identity and every-page review are owned by the production manifest; it does not imply external, physical-use, or ecclesiastical review. | Strengthens production-state precision without enlarging the review claim. | The current map and installed artifact already have this bounded status; the publication makes no broader review claim. | Identical and intentionally carries no new metadata. | Explicitly disclaims new physical-use, external, ecclesiastical, or production review. | No reader-facing disagreement. |

The changed research adds no contrary response text, branch, role, object,
action, or qualification that is absent from the current render source. The
rewrite differs in compression and wording, and it omits finished visual
composition and the received Latin by reference to their canonical shared
owners; neither difference changes a consequential claim.

## Verdict

**No material change.** The changed guide map documents corrections already
present in the current paper and its shared render sources. The modified
candidate is therefore intentionally identical in render substance, while the
independent rewrite agrees with it claim by claim. This review does not
rebaseline the edition; ledger action remains outside this task.
