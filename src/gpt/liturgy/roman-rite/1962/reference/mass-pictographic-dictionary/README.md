# Mass pictographic dictionary

This non-publishable owner holds the canonical structured action state and
review history for the Mass pictographic dictionary. It is upstream of later
instructional artwork, object-compendium extraction, and publication or web
integration.

## Current boundary

**The structural pass for the spoken 1962 Roman Low Mass with two servers is
complete, human-approved, and its detailed scene corpus is complete.**

**A render-contract layer now sits between the approved corpus and any
artwork**, at `render-contract/low-mass/v1/`. It compiles the approved
semantics into explicit world geometry, so that an artistic generator cannot
mirror the Missal, cannot invent a panel, and cannot restage approved geometry.
The choreography remains v0.21 and is not revised there.

**The artistic rendering protocol is in force**, at
[`artistic/RENDERING-PROTOCOL.md`](artistic/RENDERING-PROTOCOL.md). It is
durable project architecture rather than advice: a plate may be generated only
from an art-ready scene's compiled render contract and deterministic skeleton,
a blocked scene must not be rendered at all, undeclared panels are forbidden,
and structural fidelity and artistic quality are separate approval gates.

**The publication-quality artistic rendering pass has not started.** No
canonical artistic plate is approved. Work state for all three layers is
tracked in `promised-deliverables.toml` and `PROJECT-WORK.md` rather than
asserted here.

The v0.21 checkpoint belongs under
`structural/low-mass/v0.21/`. Its imported handoff summary is the authority for
the approved choreography and explicit corrections. Earlier or conflicting
review projections are retained only as labelled history and must not control
new render work.

The checkpoint as first committed carried standalone detailed assets only for
LM-134 through LM-140; every earlier approved scene was attested by prose in
the handoff summary alone. That gap is now closed. The whole Mass, from the
Prayers at the Foot of the Altar to the Leonine prayers appendix, exists as
machine-readable scene records under
`structural/low-mass/v0.21/scenes/`, registered in order in
`scenes/inventory.yaml`. A rendering agent asking for every structural scene
needed to draw the 1962 spoken Low Mass, in order, gets a complete answer from
that registry without consulting review images or an older server manual.

Existing assets and ceremonial records under the sibling
`altar-server-guides/` predate this checkpoint and have not been reconciled to
v0.21. They are not an alternate source of truth for this pictographic lane;
the relationship and known contrasts are also recorded in
`guidance/liturgy/roman-1962-server-training.md`. Each such record now carries
a `Historical / pre-v0.21` notice in its own text, so the fence is visible to a
reader who arrives at one of them directly rather than through this owner.

## Architecture

Three layers, each downstream of the last. A fresh agent should read them in
this order.

```text
structural/low-mass/v0.21/          approved choreography — what happens
        |
        v
render-contract/low-mass/v1/        compiled world geometry — what may be drawn
        |
        v
artistic/RENDERING-PROTOCOL.md      the rules governing any artistic lane
        |
        v
./tools/tpt pictographic art-seed   the only sanctioned input package
        |
        v
human-guided web artistic lane      STRUCTURE gate, then ART gate
```

| Layer | Path | Holds |
| --- | --- | --- |
| Structural | `structural/low-mass/v0.21/` | The approved scene corpus, its registry, invariants and branch conditions. |
| Render contract | `render-contract/low-mass/v1/` | The world frame, camera and panel model, object and actor transforms, compiled contracts, deterministic skeletons, and the current [handoff](render-contract/low-mass/v1/HANDOFF.md). |
| Artistic | [`artistic/RENDERING-PROTOCOL.md`](artistic/RENDERING-PROTOCOL.md) | The durable protocol, and the [plate provenance contract](artistic/plate-provenance.yaml). |

The full pipeline, from the rubric outward:

```text
liturgical action or rubric
-> canonical structured scene/action state
-> deterministic structural skeleton
-> human approval
-> compiled render contract and deterministic render skeleton
-> artistic rendering, bound by that skeleton and gated twice
-> derivatives, object compendium, web and manual use
```

## Canonical CLI flow

```sh
./tools/tpt pictographic readiness roman-1962 low-mass
./tools/tpt pictographic readiness roman-1962 low-mass --blocked
./tools/tpt pictographic art-seed roman-1962 low-mass LM-001A
```

`art-seed` prepares the only sanctioned input for an artistic agent, and fails
closed: a scene that is not art-ready is refused with its exact blocking cue,
and no package is written. Readiness counts are not recorded in prose anywhere
in this owner — ask the tooling, so the answer cannot go stale.

The future graphite or pencil plates remain downstream of the approved
structured data. They must retain links to the structural scene IDs and
metadata; image prompts are not a replacement for that data.

The deterministic structural skeleton stage is what `scenes/` and the generated
`storyboards/` now hold. Those storyboards carry labels because their job is
review, not publication; the wordless plate rules of
`guidance/liturgy/roman-1962-pictorial-dictionaries.md` govern the artistic
stage that follows, not this one.

## Later work

The next fresh, human-guided lane begins with a style-anchor plate and then
proceeds scene by scene, consuming `scenes/inventory.yaml` in `order`. The 1962 sung forms, pontifical forms,
postconciliar forms, object compendium, and final site/manual integration all
remain future work.
