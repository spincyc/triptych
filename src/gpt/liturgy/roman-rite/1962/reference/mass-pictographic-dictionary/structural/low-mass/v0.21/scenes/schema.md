# Scene record schema — spoken 1962 Low Mass structural corpus

This document defines the machine-readable scene records under
[`sections/`](sections/) and the controlled vocabularies they draw on. It is
the contract that [`../validate.py`](../validate.py) enforces.

The corpus exists so that a later artistic-rendering agent can stage every
approved scene of the spoken 1962 Roman Low Mass deterministically, **without**
re-deriving choreography from prose, from review images, or from the older
sibling `altar-server-guides/` tree.

## Provenance and authority

Every file here is **repository-authored recovery**, not transported bytes.
It is derived only from:

1. [`../handoff/HANDOFF-SUMMARY.md`](../handoff/HANDOFF-SUMMARY.md), the
   approval record for checkpoint v0.21; and
2. [`../recovery/approved-choreography-baseline.md`](../recovery/approved-choreography-baseline.md),
   the verbatim approved choreography supplied with the recovery task.

The older `altar-server-guides/` tree is **not** an input. Where the approved
material leaves a cue to the serving profile, the scene records it as an
`unresolved` parameter rather than inventing a choreography. See
[`../recovery/recovery-notes.md`](../recovery/recovery-notes.md).

## Files

| File | Contents |
| --- | --- |
| `schema.md` | This contract. |
| `geometry.yaml` | Sanctuary coordinate frame, levels, anchors, mensa positions, viewpoints. |
| `invariants.yaml` | Global invariants, the cluster ranges they govern, and the stale contradiction each one rejects. |
| `conditions.yaml` | Branch conditions a scene may be gated on. |
| `inventory.yaml` | The canonical ordered registry: every scene ID exactly once, with its cluster, section, file, title, and condition. |
| `sections/NN-slug.yaml` | The scene records themselves, one file per section. |
| `../MANIFEST-AUTHORED.sha256` | Checksums of the whole authored layer: `scenes/`, `recovery/`, `storyboards/` and the generator. Separate from the transport manifest. |

`inventory.yaml` is the spine. `sections/` must implement it exactly: the
validator fails if a scene appears in one and not the other, or if order,
cluster, title, condition, or file assignment disagree.

## Scene identity

A **cluster** is `LM-NNN` — one coherent moment, the natural unit of a
storyboard panel. A **scene** is `LM-NNNX` — one distinct depictable state
within that cluster. `LM-136` is a cluster; `LM-136A` is a scene.

Numbering rules:

- Scene IDs already committed in this checkpoint are **never renumbered**.
  `LM-134A`–`LM-134C`, `LM-135A`–`LM-135C`, `LM-137A`, `LM-137C`,
  `LM-138A`–`LM-138D`, `LM-139A`–`LM-139B` and `LM-140A`–`LM-140C` are fixed.
- `LM-137B` is **deliberately unassigned**. It is absent from the approved
  storyboard, and the recovery does not invent it.
- Clusters `LM-113` through `LM-127` are a **reserved gap**, recorded in
  `inventory.yaml`. Leaving them empty is what allows later insertion without
  renumbering a committed late scene. A gap is not missing coverage; coverage
  is proved by `inventory.yaml`'s ordering, not by numeric contiguity.
- `order` is a dense 1-based integer over the whole corpus and is the real
  reading order. Sort by `order`, never by scene ID.

## Scene record fields

Every record in a `sections/` file is a mapping with these keys. Required
unless marked optional.

| Field | Type | Meaning |
| --- | --- | --- |
| `scene_id` | `LM-NNNX` | Unique across the corpus. |
| `cluster` | `LM-NNN` | The cluster this scene belongs to. |
| `order` | integer | Position in the whole-Mass reading order. |
| `title` | quoted string | Short human label. |
| `kind` | enum | See **kind**. |
| `liturgical_moment` | quoted string | The rite's own name for the moment. |
| `text_cue` | quoted string, optional | The words the scene is pinned to. |
| `voice` | enum | Voice of the priest's words in this scene. |
| `condition` | condition id | From `conditions.yaml`. `ALWAYS` for the default path. |
| `predecessor` | scene id or `null` | Previous scene on the default path. |
| `successor` | scene id or `null` | Next scene on the default path. |
| `bypass_successor` | scene id, optional | Only on the scene immediately before a conditional block: where the order resumes when the condition fails. |
| `camera` | mapping | `view` (a `geometry.yaml` viewpoint id) and optional `note`. |
| `actors` | list | See **actor**. Always includes `priest`, `AC1`, `AC2`. |
| `objects` | list | See **object**. May be empty. |
| `transitions` | list of quoted strings | Ordered movements or state changes this scene effects. |
| `responses` | list, optional | Server or congregational words: `actor`, `text`, `voice`. |
| `bells` | list, optional | Bell actions: `actor`, `count`, `cue`. `count` is `null` when the number belongs to the serving profile rather than the approved baseline; such a scene must also record the shortfall in `unresolved`. |
| `invariants` | list of invariant ids | Which global invariants this scene must be checked against. |
| `variants` | list, optional | See **variant**. |
| `unresolved` | list, optional | Explicit serving-profile parameters the approved material deliberately did not fix. |
| `notes` | quoted string, optional | Anything a renderer needs that no field carries. |

### actor

Every scene lists all three actors, even when one is merely kneeling, so a
renderer never has to infer an absent figure.

| Field | Type | Meaning |
| --- | --- | --- |
| `id` | `priest` \| `AC1` \| `AC2` | |
| `role` | quoted string | `celebrant`, `acolyte-epistle-side`, `acolyte-gospel-side`. |
| `anchor` | anchor id | From `geometry.yaml`. |
| `side` | `gospel` \| `centre` \| `epistle` | World-space side, never view-space. |
| `depth_rank` | integer | Ordering along the depth axis: **smaller is nearer the viewer, larger is further away, toward the altar**. Equal ranks mean equal depth. See `INV-GEO-03` and the note below. |
| `posture` | enum | See **posture**. |
| `bow` | enum | See **bow**. |
| `facing` | enum | Where the body/head is turned. |
| `gaze` | enum | Where the eyes rest. |
| `hands` | mapping | `joined` (bool), `left` (enum), `right` (enum). |
| `gestures` | list of enum | Discrete gestures performed in this scene. |
| `path` | mapping, optional | `from` and `to` anchor ids, plus optional `via` list and `note`, when the actor moves. |

`depth_rank` is the field that keeps the corpus honest about depth, so its
direction is fixed. An actor described as *behind* another — a server kneeling
slightly behind the priest at the predella, or the acolyte who follows on a
crossing — stands further from the altar and therefore **nearer the viewer**,
and takes the **smaller** rank. Two actors at anchors with different depth must
rank in the same order as those anchors; the validator checks this against
`geometry.yaml`. Two actors at anchors of equal depth may still differ in rank,
and that is exactly how a front-and-behind relation with no anchor difference —
the two post-ablution crossings — is recorded structurally rather than in prose.

### object

| Field | Type | Meaning |
| --- | --- | --- |
| `id` | enum | See **object ids**. |
| `placement` | anchor / mensa position / quoted string | Where it is at the end of the scene. |
| `orientation` | enum, optional | See **orientation**. |
| `state_before` | quoted string | Its state entering the scene. |
| `state_after` | quoted string | Its state leaving the scene. |
| `handled_by` | `priest` \| `AC1` \| `AC2` \| `both-acolytes` \| `none` | Who touches it in this scene. |

### variant

| Field | Type | Meaning |
| --- | --- | --- |
| `id` | quoted string | Stable within the scene. |
| `kind` | `requiem` \| `seasonal` \| `local-custom` \| `profile-parameter` \| `circumstantial` \| `exposition` | `circumstantial` covers a branch turning on what surrounds the Mass, such as a procession following it. |
| `applies_when` | condition id or quoted string | |
| `description` | quoted string | |
| `baseline` | bool | Always `false`. A variant is by definition not the baseline. |

A variant records a departure that must **not** contaminate the baseline. It
never weakens the baseline into "one possible custom".

## Controlled vocabularies

The validator rejects any value outside these lists. It reads them **out of
this document**: each entry below runs from its bolded name to the next blank
line, and every backticked token in it is a permitted value. So this file is
the single source of truth, and editing it changes what validates. If a scene
genuinely needs a value that is absent, add it here deliberately; do not
smuggle a free-text value into an enumerated field.

**kind** — `action`, `state`, `response`, `transition`, `branch-point`

**voice** — `audible`, `low`, `secret`, `silent`, `none`

**posture** — `standing`, `kneeling`, `kneeling-erect`, `genuflecting`,
`walking`, `stooping`, `bowing-low-over-altar`

**bow** — `none`, `head-slight`, `head-moderate`, `head-profound`,
`body-medium`, `body-profound`

`head-*` bows incline the head only. `body-medium` and `body-profound` are the
medium and profound bows of the body. The approved record's "slight bow" is
`head-slight` and its "moderate bow" is `head-moderate`.

Two conventions keep `posture` and `bow` from overlapping. The altar kiss is
`posture: bowing-low-over-altar` with `bow: none`: `bow` records a *prescribed*
head or body bow, while the inclination a physical action requires belongs to
`posture`. And `hands` records the **depicted instant** of a scene, not its end
state, so a scene whose action is "extend, elevate, join, lower" records the
moment the panel shows and says which in `notes`. `placement` on an object, by
contrast, is always its state at the end of the scene.

**facing** — `altar`, `altar-cross`, `missal`, `people`, `centre`,
`gospel-side`, `epistle-side`, `inward-to-priest`, `inward-to-centre`,
`credence`, `gospel`, `last-gospel-card`, `host`, `chalice`, `oblations`,
`nave`

**gaze** — `cross`, `host`, `chalice`, `paten`, `missal`, `people`,
`downcast`, `heaven`, `oblations`, `inward-to-priest`, `hands`, `altar`,
`forward`, `last-gospel-card`

**hand state**, used for both hands.left and hands.right — `joined`,
`joined-before-breast`, `joined-at-mensa-edge`, `joined-at-chin-height`, `joined-between-breast-and-altar`,
`extended`, `elevated`, `on-breast`, `at-side`, `palm-on-mensa-outside-corporal`,
`palm-on-corporal`, `on-missal`, `on-altar-outside-corporal`,
`raising-alb-hem`, `lifting-chasuble-edge`, `holding-bell`, `holding-cruet`,
`holding-towel`, `holding-lavabo-dish`, `holding-veil`, `holding-pall`,
`holding-purificator`, `rubbing-fingers-over-chalice`, `holding-paten`, `holding-host`, `holding-host-and-paten`,
`holding-particle`, `holding-chalice-node`, `holding-chalice-foot`,
`holding-chalice-both-hands`, `holding-chalice-under-node`,
`supporting-chalice-base`, `at-chalice-base`, `at-chalice-node`,
`holding-missal`, `holding-chalice-cloth`, `holding-biretta`, `signing`,
`striking-breast`, `blessing`, `raising-host-edge`, `pushing-host`,
`extended-over-oblations`, `turning-missal-leaves`, `scraping-corporal`

**gesture** — `sign-of-the-cross`, `small-cross-forehead`, `small-cross-lips`,
`small-cross-breast`, `sign-text-with-thumb`, `strike-breast`,
`cross-over-host`, `cross-over-chalice`, `cross-over-host-and-chalice`,
`greek-cross-over-oblations`, `cross-with-paten`, `cross-with-chalice`,
`cross-with-host`, `cross-with-particle`, `bless-water`, `bless-people`,
`altar-kiss`, `kiss-missal-text`, `kiss-paten-edge`, `kiss-cruet`,
`genuflect`, `elevate-host`, `elevate-chalice`, `minor-elevation`,
`ring-bell`, `turn-right`, `turn-left`, `turn-inward`, `ascend`, `descend`,
`extend-hands`, `elevate-hands`, `join-hands`, `lower-hands`, `separate-hands`,
`raise-eyes`, `lower-eyes`, `fraction`, `break-particle`, `commingle`,
`consume-host`, `consume-precious-blood`, `purify-paten`, `purify-chalice`,
`wash-fingertips`, `fold-veil`, `remove-pall`, `replace-pall`,
`rub-fingers-over-chalice`, `rub-fingers-over-paten`,
`raise-chalice-slightly`, `pour-ablution`

**object id** — `missal`, `missal-stand`, `altar-cards`, `epistle-altar-card`,
`gospel-altar-card`, `last-gospel-card`, `lavabo-card`, `corporal`, `pall`,
`purificator`, `paten`, `host`, `host-halves`, `particle`, `chalice`,
`chalice-veil`, `chalice-cloth`, `burse`, `wine-cruet`, `water-cruet`,
`lavabo-dish`, `towel`, `bell`, `altar-cross`, `candles`, `credence-table`,
`biretta`, `alb`, `chasuble`, `catafalque`

**orientation** — `priest-reads-facing-left`, `open-toward-priest`,
`concave-toward-gospel-side`, `open-ends-toward-back`, `handle-toward-priest`,
`upright`, `horizontal`, `nearly-horizontal`, `folded`, `unfolded`,
`flat-on-mensa`, `not-applicable`

## Rules the validator enforces

1. Every scene ID appears exactly once in `inventory.yaml` and exactly once
   across `sections/`, and the two agree on cluster, order, title, condition,
   and file.
2. `order` is dense and 1-based over the whole corpus, with no duplicates or
   gaps.
3. `predecessor` and `successor` form one coherent chain: each scene's
   `successor` names the next scene by `order`, except at a conditional
   boundary, and each `predecessor` is the inverse of its target's
   `successor`.
4. Every conditional block reconnects: the scene before a block whose
   `condition` is not `ALWAYS` declares a `bypass_successor` naming the first
   scene after that block on the default path.
5. Every `condition`, invariant id, anchor, viewpoint, and enumerated value
   resolves.
6. Every scene cites at least one invariant, and a cited invariant's
   `applies_to` range contains that scene's cluster.
7. Every scene lists all three actors exactly once.
8. Scenes governed by `INV-POS-01` give the priest, AC1 and AC2 the same
   `depth_rank`.
9. Wherever the Missal appears with a reading function, its `orientation` is
   `priest-reads-facing-left`, on either side.
10. No scene asserts any contradiction named in an invariant's `rejects`
    field; the named-contradiction guard in `../validate.py` is authoritative.

## Authoring rules

- **Quote every scalar carrying liturgical text, a title, an incipit, a name,
  a note, or a citation.** Ordinary Latin punctuation silently breaks an
  unquoted YAML scalar.
- Write Latin cues in their ordinary liturgical spelling. Call a `Gloria
  Patri` a doxology explicitly; an unqualified `Gloria` means the Gloria in
  excelsis.
- Record only what the approved material settles. A cue the approved material
  left to the serving profile belongs in `unresolved`, never in a posture or
  gesture field.
- Do not weaken approved baseline choreography into vague "one possible
  custom" language, and do not promote a variant into the baseline.
