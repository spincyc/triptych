# Commentary discovery

Maps a scripture passage to the commentary works worth pulling into the source
library, then unions those mappings across every proper to produce the corpus
of works the vault should acquire.

## Chain

| Stage | Tool | Input | Output |
| --- | --- | --- | --- |
| Lookup | `tools/tpt commentary-work-index discover` | `passage-commentary-index.yaml` | works for one passage |
| Union | `tools/tpt commentary-work-index build-corpus` | the index plus `../calendars/*/propers.yaml` | `mass-commentary-corpus.yaml` |
| Harvest | not yet built | a passage | candidate works, appended to the index |

Only the harvest stage consults a model. Everything downstream reads the
tracked index, so the chain reproduces exactly from a given index: two runs of
`build-corpus` over one index are byte-identical, and the corpus header records
the index's `discovery_sha256`.

## Index format

`passage-commentary-index.yaml` is the tracked lookup. Each entry keys a
passage to a ranked list of works.

```yaml
schema: triptych-commentary-work-index/v1
updated: 2026-07-30
passages:
  - passage: John 3:16
    works:
      - work_id: work.augustine.tractates-on-john
        author: Augustine of Hippo
        title: Tractates on the Gospel of John
        date: 407
        role: church-father
        confidence: 1.0
        source_hint: CCSL 36
```

`role` is one of `church-father`, `saint`, `saintly`, `pope`, `doctor`;
`patristic` and `tradition` are accepted aliases normalising to
`church-father` and `saintly`. Absent fields degrade rather than fail: a
missing `author` becomes `Unknown`, a missing `role` becomes `church-father`,
and a missing `confidence` sorts as `1.0`.

**Give every work a `work_id`.** Deduplication falls back to
`"author | title"` when it is absent, so two spellings of one work become two
works. Ids should reconcile to the `work.*` identities `source-library` already
uses, which is what lets a harvested candidate become a vault record without a
second identity reconciliation.

## Ranking

Two weights combine, and both are already implemented:

- `confidence` orders works within a single passage.
- `build-corpus` accumulates `score = Σ 1/(rank + 1)` for a work across every
  passage in a mass, then ranks by descending score with a casefolded
  author/title tiebreak.

So a work recurring at good rank through many propers outranks one appearing
once at high rank — the property that matters when choosing what to acquire.
`--max-results-per-passage` and `--max-results-per-mass` both default to 20.

## Harvest contract

A model-ranked list is not a measured citation count, and its variance is
largest for exactly the passages that dominate by volume: 426 of the 1301
distinct references are Psalms, and Psalms account for 572 of the 1630
passage occurrences, many of them ferial antiphon fragments. The
harvester therefore records what it is:

- Write to a dated ledger, never straight to the index, and record the model
  identity and an `--audited-on` date, as `source-inventory` and
  `research-staleness` do for their own ledgers.
- Key the harvest on the encoded citation from `tools/tpt citations`, which is
  already canonical, so re-runs cost nothing and only new passages consult the
  model.
- Derive `confidence` from agreement across repeated runs — appearances
  divided by runs — rather than asking for a score. The stability of the head
  of the list is then measured rather than assumed, and low-agreement works
  identify themselves for review.
- Carry the author's death year as a field so the pre-1900 rule is checkable.
  A cutoff that lives only in a prompt cannot be verified afterwards.

Nothing enters the source library on a harvest alone. Candidates are reviewed
into the vault under `../../../guidance/sources.md`, the way a `trace-scan`
family presence is promoted to `reviewed`.
