# Commentary discovery

Maps a scripture passage to the commentary works worth pulling into the source
library, then unions those mappings across every proper to produce the corpus
of works the vault should acquire.

## Chain

| Stage | Tool | Input | Output |
| --- | --- | --- | --- |
| Lookup | `tools/tpt commentary-work-index discover` | `passage-commentary-index.yaml` | works for one passage |
| Union | `tools/tpt commentary-work-index build-corpus` | the index plus `../calendars/*/propers.yaml` | `mass-commentary-corpus.yaml` |
| Harvest | `tools/tpt harvest {plan,record}` | a passage | one run's candidates, into `harvest-ledger.yaml` |
| Identity | `tools/tpt harvest aliases` | the ledger | `work-aliases.yaml` |
| Promote | `tools/tpt harvest promote` | the ledger and the alias table | `passage-commentary-index.yaml` |

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

`role` is one of `church-father`, `saint`, `saintly`, `pope`, `doctor`,
`ecclesiastical-writer`; `patristic` and `tradition` are accepted aliases
normalising to `church-father` and `saintly`.

Use `ecclesiastical-writer` — patrology's own *scriptor ecclesiasticus* — for an
orthodox writer who is not venerated as a saint: Cassiodorus, Peter Lombard,
Nicholas of Lyra, Cornelius a Lapide, Theophylact. Before it existed the
vocabulary had no slot for them and runs fell back to `saintly`, which is why
4098 of the 7297 attributions already promoted carry that role against 333 for
`saint`. Those are not re-tagged: whether a given writer is venerated is a fact
about that person, and asserting it wrongly in either direction is worse than
leaving a coarse tag visible for what it is. Absent fields degrade rather than fail: a
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

## Work identity

Confidence here is agreement across independent runs, so it is only worth what
work identity is worth: two runs naming one commentary differently look like
disagreement, and the work splits into fragments each scoring below what it
earned. Measured across three 491-locus runs, attributions corroborated by two
or more runs were 35.3% on author and title as written against 78.3% on author
alone — a 43-point gap that was naming, not disagreement about who commented.

`work-aliases.yaml` closes it, and `harvest promote` will not run without it.
The table is derived, not hand-typed: `harvest aliases --rebuild` takes the
alias claims the runs themselves made, treats each as an edge between two
names, and groups each author's names into connected components. On the same
three runs that lifts corroboration to 70.7%, and of the 5095 loci where the
runs agree on the author, 5004 now also agree on the work.

What cannot be derived is whether a group is one work, so the table carries a
`review` block and each entry states its reason:

- `ambiguous_titles` drops a name that denotes two of its author's works.
  Closure alone merged Peter Lombard's psalm gloss with his Pauline
  *Collectanea*, because "Magna Glossatura" names both and two of the three
  runs offered it as an alias of each. Corroboration would not have caught
  that: both runs were right about the name and wrong about what it picks out.
- `not_aliases` denies a join the works do not support. Jerome's
  *Commentarioli in Psalmos* and *Tractatus in Psalmos* are two works, not one.
- `also_aliases` adds a join no run happened to assert, needed where denying an
  edge orphans a name that reached its group only through it.

Loading validates that no title reaches two groups, that no name declared
ambiguous still groups a work, and that no chain of aliases has re-joined works
declared distinct. `evidence_sha256` covers the alias claims alone, so
recording a run that asserts a new alias ages the table and `promote` refuses
until the new grouping has been looked at. A merge is invisible once promoted
and cannot be undone from the index, so nothing is merged on resemblance.

## Review

Nothing enters the source library on a harvest alone. Candidates are reviewed
into the vault under `../../../guidance/sources.md`, the way a `trace-scan`
family presence is promoted to `reviewed`.
