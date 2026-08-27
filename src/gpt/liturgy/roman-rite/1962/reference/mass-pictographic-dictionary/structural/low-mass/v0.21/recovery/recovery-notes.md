# Recovery notes — the detailed Low Mass scene corpus

## The gap this closes

Checkpoint `f6169de` preserved the human-approved v0.21 structural pass
faithfully, and in doing so exposed one material incompleteness: the transport
archive carried **standalone detailed assets only for LM-134 through LM-140**.
Everything earlier — the Prayers at the Foot, the ascent, the Ordinary, the
readings, the Offertory, the Canon, the Consecration, the Communion rite — was
attested only by prose in
[`../handoff/HANDOFF-SUMMARY.md`](../handoff/HANDOFF-SUMMARY.md).

Prose is not enough to stage an illustration from. This recovery turns the
whole approved spoken Low Mass into machine-readable scene records under
[`../scenes/`](../scenes/), so the artistic lane can consume the repository
alone.

## What the recovery drew on, and what it did not

Two sources, and only two:

1. the approved handoff summary; and
2. [`approved-choreography-baseline.md`](approved-choreography-baseline.md),
   the verbatim approved choreography supplied with the recovery task and
   preserved here as a durable record.

The older sibling `altar-server-guides/` tree was **not** used. That fence was
already binding, and it matters: an audit of the repository found that tree
asserts an elevation-concentrated bell grouping, a conditional *Domine, non sum
dignus* ring, a wine-and-water second ablution, and a chalice **veil** as the
post-ablution transfer object — four choices the approved baseline rejects.
Each of those records now carries a `Historical / pre-v0.21` notice in its own
text, so a reader who arrives at one by search learns immediately that it is
not an input to this lane.

Nothing in that tree was rewritten, corrected, or republished. Its content
remains exactly as it was; only the provenance notice was added.

## Where the authored corpus lives, and why

The `v0.21` directory holds two different kinds of thing, and the distinction
is load-bearing:

| Layer | Directories | Nature |
| --- | --- | --- |
| Transported | `handoff/`, `sources/`, `review/`, `review-history/`, `transport-originals/` | Supplied bytes, preserved unchanged. |
| Repository-owned | `README.md`, `VALIDATION.md`, `corpus.yaml`, `MANIFEST.sha256`, `validate.py`, and now `scenes/`, `recovery/`, `storyboards/`, `render-storyboards.py` | Written here: routing, classification, checksums, validation, and this recovery. |

A reasonable objection was raised during this work: v0.21 is a preservation
checkpoint, and adding roughly two hundred newly authored files inside it risks
blurring *what was supplied and approved* against *what was then written*. That
objection was weighed and not taken, for three reasons.

First, a new `v0.22` directory would imply a newly approved version. No human
approved a v0.22; the approval is v0.21, and the recovery adds detail to it
rather than superseding it. Naming it otherwise would overclaim.

Second, the repository-owned layer inside v0.21 already exists and is already
mutable — `corpus.yaml`, `MANIFEST.sha256` and `validate.py` were all written
by the checkpoint commit, not transported.

Third, the distinction is preserved by construction rather than by directory
name: every authored file carries
`provenance: repository-recovery-from-approved-baseline`, the authored corpus
is checksummed separately in [`../MANIFEST-AUTHORED.sha256`](../MANIFEST-AUTHORED.sha256)
rather than being folded into the transport manifest, and no transported byte
was touched. `validate.py` proves all three.

## What is deliberately left open

The approved material settles a great deal and deliberately leaves a few cues
to the serving profile. Those are recorded in each scene's `unresolved` list
and are **not** resolved here. Turning a local serving custom into a universal
rubric to make the data look complete would be a worse failure than the gap it
closed.

Equally, an approved baseline is not weakened into "one possible custom".
Where the approved record is definite, the scene record is definite.

## What is deliberately absent

- **`LM-137B`** is unassigned. The approved storyboard has `LM-137A` and
  `LM-137C` and no `LM-137B`; the recovery preserves that absence instead of
  inventing a scene to close the letter sequence.
- **Clusters `LM-113` to `LM-127`** are a reserved gap, so that a later
  insertion cannot force the renumbering of a committed late scene. Coverage is
  proved by the dense `order` field in
  [`../scenes/inventory.yaml`](../scenes/inventory.yaml), never by numeric
  contiguity.

## Regenerating and validating

```sh
# rewrite the structural storyboards from the scene corpus
./render-storyboards.py

# prove the storyboards match the corpus
./render-storyboards.py --check

# validate the whole checkpoint, transported and authored
./validate.py
```

The storyboards are **generated**, never hand-edited. They are structural
review projections — they carry labels on purpose, which is what distinguishes
them from the wordless publication plates the artistic lane will produce.

## What this recovery is not

It is not artistic rendering, and it does not begin it. It does not revise the
approved choreography. It does not touch High Mass, Missa cantata, Solemn Mass,
Pontifical Mass, postconciliar Mass, the object compendium, or web and manual
integration, all of which remain unstarted.
