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
numbering: vulgate
numbering_note: ...
numbering_unrecorded_count: 3
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

## Key spaces

The index and the propers do not speak the same key space, and the bridge
between them is `discover`'s, not the index's.

- **The index is keyed by chapter locus, and by nothing else.** All 490 keys are
  one chapter (`Psalms 24`), because the harvest is run `--by-chapter` and a
  locus is one chapter, never wider. It once also held 7 verse ranges left by
  the pilot runs (`Psalms 24:1-24:3`), and the two granularities disagreed:
  `Psalms 24:4` carried 19 works of which 7 appeared on no chapter row, and
  `Luke 21:25-21:33` carried 27 of which 14 did not. A consumer keyed on
  chapters lost those silently; a consumer keyed on the pilot loci saw a
  different corpus for the same text; both answers looked complete. Promotion
  now derives every key with `chapter_loci`, so a pilot run's answer about
  `Psalms 24:4` is that run's answer about Psalms 24 — widened, which is sound,
  and never narrowed, which would not be. `overlapping_keys` refuses to write an
  index where two keys cover the same text.
- **A proper cites a verse range** (`Psalm 24:1-3`, `Baruch 3:9-15, 32-4:4`).
  Of the 1600 distinct references the corpus carries, 6 name a bare chapter and
  so meet an index key as a string; the other 1594 reach the index only through
  the bridge below, which is `discover`'s and not the index's.

Three rules close the gap, all of them in `commentary-work-index`:

**The key is derived, never the spelling.** `tools/citations` keeps the citation
verbatim in `ref` while parsing its book to the canonical `Psalms`, so a lookup
renders its key from the parsed book and ranges instead. Without that, 926 of
the 2190 references missed the index outright — 888 of them psalms, purely
because the missals write "Psalm" and the index is keyed "Psalms". The citation
as written is still reported, as `cited`.

**A psalm lookup must name its numbering.** `discover` takes
`--numbering {vulgate,hebrew}` and refuses a psalm without it. Vulgate 50 is
Hebrew 51, and the two missals disagree by declaration: `roman-1962` is vulgate,
`postconciliar` is hebrew. Guessing returns a real, confident, wrong psalm,
which is worse than the miss it replaces. `build-corpus` needs no flag — it
reads `psalm_numbering` off each calendar. Conversion runs through
`scripts/_psalms.py` and the tracked concordance; nothing is renumbered by hand,
and a reference that does not exist in its declared system is reported
`unconvertible` rather than moved.

## Numbering

That flag asks what the *citation* is in. Until 31 July 2026 nothing asked what
the *index* was in, and the index said nothing: 524 keys spelled `Psalms 24`
with no statement of whose Psalm 24 that is. Vulgate 24 is Ad te levavi and
Hebrew 24 is Domini est terra; both resolve, and a lookup on the wrong one
returns real commentary attached to the wrong text.

**The keys are `vulgate`, and the file now says so.** Not asserted — derived.
Every psalm key comes through `_canonical_passage`, which converts each
calendar's citations out of the system that calendar declares, so all 130 psalm
keys are exactly the set that conversion produces; the no-conversion hypothesis
differs from the tracked keys on twenty of them, which is what proves it. The
eleven antiphons the postconciliar file prints in Vulgate numbers under a Hebrew
declaration never reach a key at all: each exceeds its Hebrew psalm and is
refused as `unconvertible`, so the psalter half of the index is clean by
construction.

**The rest of the canon is not converted, so the file is mixed.** A non-psalm
citation's chapter becomes the key as printed, which is the Vulgate's division
for `roman-1962` and the Lectionary's for `postconciliar`. Where the two divide
a book differently the calendar's own `citation_divergences` says so, and three
keys turn out to name no chapter of this canon at all:

| Key | Reached only by | Which means | Vulgate's own chapter is |
| --- | --- | --- | --- |
| `Joel 3` | `Joel 3:1-5` | `Joel 2:28-32` | the valley of Josaphat |
| `Esther 4` | `Esther 4:17` | `Esther 13:9-11` | Mardochai going away as Esther asked |
| `Isaiah 8` | `Isaiah 8:23-9:3` | `Isaiah 9:1-4` | the darkness before the great light |

Each carries `numbering: unrecorded` and a `numbering_basis`, and every lookup
refuses it with that reason rather than answering. `unrecorded` and not
`nova-vulgata`: the harvest ledger records no numbering for any run, so which
system the works under those keys were named for cannot be derived, and naming
one would be the guess this whole chain exists to refuse.

`Malachi 3` is deliberately *not* in that list. Two citations reach it —
`Malachi 3:1`, which means Vulgate Malachi 3, and `Malachi 3:19-20a`, which
means Vulgate Malachi 4. The key is sound and the second citation is misrouted,
which is a fact about resolution rather than about the key, so the corpus
reports it under `misrouted_citations` instead. A key is foreign only when
*every* citation reaching it means somewhere else.

Three gates hold the line, all derived and none hand-typed:

- `_load_discovery` refuses an index with no `numbering`, or one whose
  declaration is outside the vocabulary. The vocabulary is wider than
  vulgate-or-hebrew on purpose: `guidance/versification.md` §3.3 records that
  the Vulgate and the Greek disagree with each other and not merely with the
  Hebrew, and Septuagint-derived commentary will be keyed here.
- `harvest promote` re-derives the overrides from the calendars on every run,
  so an override the calendars stop supporting disappears and a new divergence
  gains one. `tools/tests/test_commentary_index.py` asserts the tracked rows
  equal a fresh derivation in both directions.
- `harvest promote` also refuses a key that cannot exist in the declared
  system, measured against `_psalms` for the psalter and against the canonical
  witness's own chapter counts for everything else. Nova Vulgata Joel runs to
  four chapters; a `Joel 4` key would stop the promotion.

`fragment-loci.yaml` already had this right and keeps it: `scripts/_catena.py`
refuses the file, and every fragment in it, unless both declare
`_projection.CANONICAL`. That is `guidance/catena.md` Rule 3.

**A range crossing a chapter boundary resolves to every chapter it touches.**
It is never collapsed to one. 43 distinct references cross a boundary — the
Passions, the Vigil, the Sunday epistles, `Baruch 3:32-4:4`. Each chapter's
works are interleaved by rank rather than taken in a block, because a block
let the first chapter fill the result alone: `Genesis 1:1-2:2` returned twenty
works from Genesis 1 and none at all from Genesis 2, and `Matthew 26:14-27:66`
returned nineteen from chapter 26 against one from chapter 27. Interleaving
keeps each chapter's own confidence order and guarantees no named chapter is
starved by the cut at `--max-results`. A work found under several chapters is
one work carrying several loci.

A chapter-level hit is labelled `matched: chapter` with `matched_loci`, and the
corpus counts it under `chapter_matched_passage_count` rather than as coverage.
Widening is not a loosening — a commentary on a chapter is what was asked for
and what was recorded — but it is broader than the citation that reached it,
and a reader deciding whether to open the book is owed the difference between
"commented on these verses" and "commented on the chapter they are in".

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
- `canonical_titles` names a group by the whole work rather than by the part.
  Derivation takes the most-used title, so Aquinas's one commentary over ten
  Pauline epistles was named *Super Epistolam ad Romanos lectura* — Romans is
  what the missals quote. An entry gives the author, a title the group holds
  (`instead_of`) and the name to use, and is refused if no group holds that
  title, so an override cannot go on looking honoured after the grouping moves.

Loading validates that no title reaches two groups, that no name declared
ambiguous still groups a work, that no chain of aliases has re-joined works
declared distinct, and that no group's canonical title names a book its own
other names do not share. That last is `guidance/catena.md` Rule 8, and the
words that count as book names are derived from the ledger — an attribution
already ties a title to a locus, and a locus already names its book — so a
genre word like *explanatio*, which heads titles on the Psalms, the Apocalypse
and John, does not qualify. The check is sound where it is incomplete: a word
it cannot prove is a book name is never read as one. `evidence_sha256` covers the alias claims alone, so
recording a run that asserts a new alias ages the table and `promote` refuses
until the new grouping has been looked at. A merge is invisible once promoted
and cannot be undone from the index, so nothing is merged on resemblance.

## Review

Nothing enters the source library on a harvest alone. Candidates are reviewed
into the vault under `../../../guidance/sources.md`, the way a `trace-scan`
family presence is promoted to `reviewed`.
