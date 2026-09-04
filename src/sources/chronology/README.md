# Scripture chronology

When a biblical text was written or finally formed, when the event it narrates
happened, when the words it quotes were spoken, what later event tradition
reads it as prophesying, and (only as a last resort) when an exact textual
witness attests it — held once, keyed to Scripture loci, so that no publication
has to find out for itself.

`guidance/scripture-chronology.md` owns the contract. This file is the layout
only; where the two appear to disagree, the guidance is right.

## Layout

| File | Holds |
| --- | --- |
| `profiles.yaml` | evidence policies, the declared default, and deterministic cascade order |
| `events.yaml` | reusable temporal subjects, each dated once |
| `composition.yaml` | composition chronology by textual unit, which inherits |
| `bindings.yaml` | locus ranges joined to events by a relation; **no dates** |
| `gaps.yaml` | where one evidence profile knowingly says nothing dated, and why |
| `coverage.tsv` | **derived** — one row a run of verses answering alike |

The review record, which asserts nothing about Scripture and is read by no tool:

| File | Holds |
| --- | --- |
| `cold-audit-manifest.tsv` | the deterministic sample the cold audit reviewed, and the predicate that regenerates it |
| `cold-audit-report.md` | the cold independent source audit of `2330d63a5` — **immutable review evidence** |
| `cold-audit-findings.tsv` | its 104 standing findings — **immutable review evidence** |
| `post-audit-corrections.tsv` | one row per standing finding, and what was done about it |
| `post-audit-rereview-manifest.tsv` | every claim, scope and gap row the correction lane changed; the next cold reviewer inspects all of it |
| `post-audit-correction-report.md` | what the correction lane changed, and what it left open |
| `post-audit-rereview-findings.tsv` | the targeted cold re-review of every one of those changes, one row each — **immutable review evidence** |
| `post-audit-rereview-report.md` | its disposition, and what still fails — **immutable review evidence** |
| `final-rereview-corrections.tsv` | the 23 failed re-review rows, one row each, and what was done about them |
| `final-acceptance-manifest.tsv` | **derived** — every case a genuinely cold acceptance reviewer must review, over both correction lanes |
| `final-repair-report.md` | what the repair lane changed, the head references by sha, and the cold-review requirement |
| `final-acceptance-review.md` | the genuinely cold acceptance review of `5b4fe31c0`, its verdict, and the correction queue — **immutable review evidence** |
| `final-acceptance-findings.tsv` | its ruling on all 156 cases, one row each, PASS rows included — **immutable review evidence** |
| `final-acceptance-howlett.md` | the whole-artifact appendix: every claim citing Howlett, with its grounding sentence, source voice and admissibility ruling |
| `final-acceptance-sloet.md` | the whole-artifact appendix for Sloet, separating the Petavius table from Sloet's own |
| `final-acceptance-stub-evidence.md` | every conclusion that could have rested on the broken `--bible` stub, re-resolved through the real machinery |

`coverage.tsv` is written by `tools/tpt scripture-chronology build` and gated
by `check`, which refuses a stale table rather than rebuilding it. Do not
hand-edit it.

The two manifests are derived too, and by tracked scripts rather than by hand:
`post-audit-rereview-manifest.tsv` from `scripts/build_rereview_manifest.py` and
`final-acceptance-manifest.tsv` from `scripts/build_final_acceptance_manifest.py`,
both over `scripts/chronology_review_diff.py`, which loads each revision's corpus
through that revision's own loader and diffs the loaded objects.
`scripts/check_final_acceptance_manifest.py` proves the final manifest complete
in both directions and proves that no prior review id was dropped.

## Chain

| Stage | Command | Reads | Writes |
| --- | --- | --- | --- |
| Validate | `tools/tpt scripture-chronology validate` | the five authored files | nothing |
| Ask | `tools/tpt scripture-chronology query <locus>` | the corpus | nothing |
| Count | `tools/tpt scripture-chronology coverage [--universe distinct-content\|addresses] [--require-date]` | the corpus and tracked enumerable witnesses | nothing |
| Derive | `tools/tpt scripture-chronology build` | the corpus | `coverage.tsv` |
| Gate | `tools/tpt scripture-chronology check` | both | nothing |

`make check-scripture-chronology` runs the first and the last, and is part of
`make check`.

## The three rules a new row must obey

**One declared system per row.** Shared chronology is authored in `vulgate`,
the system `scripts/_projection.py` projects into. A locus in another system
reaches it through the psalm or deuterocanon concordance. Text that genuinely
exists only in another tracked witness may carry a native-system row instead;
the file declares that system, and the loader proves the address is present in
that witness rather than pretending it maps to the Vulgate.

**One date, many loci.** An event is dated in `events.yaml` and bound from
`bindings.yaml`. A binding carries no date, and the loader refuses one that
tries to. Four Gospels narrating one Crucifixion is four bindings and one date.

**Every claim says what grounds it.** A `basis` line, in prose, on every claim,
plus the source-library record ids it rests on. A basis that merely restates
this repository's own prose is not a basis.

**Every enumerable locus has a positional answer in the default cascade.** Run
both `coverage --profile catholic-comprehensive-v1 --universe distinct-content
--require-date` and its `--universe addresses` counterpart. Named systems for
which the repository has no enumerable witness are disclosed in the report and
are outside that exhaustive claim.

## What does not live here

Book names, chapter counts and canon order (`scripts/_canon.py`, from the
canonical edition's own index); the psalm correspondence
(`psalm-numbering.tsv`); the deuterocanon correspondence
(`deuterocanon-numbering.tsv`); an edition's departures from canonical
numbering (that edition's `verse-aliases.tsv`); and the identity, rights and
provenance of any source (`../works/`, under `guidance/sources.md`). This tree
names those; it never restates them.
