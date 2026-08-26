# Scripture chronology

When a biblical text was written, when the event it narrates happened, when
the words it quotes were spoken, and what later event tradition reads it as
prophesying — held once, keyed to canonical Scripture loci, so that no
publication has to find out for itself.

`guidance/scripture-chronology.md` owns the contract. This file is the layout
only; where the two appear to disagree, the guidance is right.

## Layout

| File | Holds |
| --- | --- |
| `profiles.yaml` | whose testimony wins, and what the profile refuses |
| `events.yaml` | reusable temporal subjects, each dated once |
| `composition.yaml` | composition chronology by textual unit, which inherits |
| `bindings.yaml` | locus ranges joined to events by a relation; **no dates** |
| `gaps.yaml` | where the corpus knowingly says nothing dated, and why |
| `coverage.tsv` | **derived** — one row a run of verses answering alike |

`coverage.tsv` is written by `tools/tpt scripture-chronology build` and gated
by `check`, which refuses a stale table rather than rebuilding it. Do not
hand-edit it.

## Chain

| Stage | Command | Reads | Writes |
| --- | --- | --- | --- |
| Validate | `tools/tpt scripture-chronology validate` | the five authored files | nothing |
| Ask | `tools/tpt scripture-chronology query <locus>` | the corpus | nothing |
| Count | `tools/tpt scripture-chronology coverage` | the corpus | nothing |
| Derive | `tools/tpt scripture-chronology build` | the corpus | `coverage.tsv` |
| Gate | `tools/tpt scripture-chronology check` | both | nothing |

`make check-scripture-chronology` runs the first and the last, and is part of
`make check`.

## The three rules a new row must obey

**One system.** Every locus is numbered in `vulgate`, the system
`scripts/_projection.py` projects into, and each locus-bearing file declares it
at the top. A locus in another system reaches the corpus through the psalm or
deuterocanon concordance, or is refused.

**One date, many loci.** An event is dated in `events.yaml` and bound from
`bindings.yaml`. A binding carries no date, and the loader refuses one that
tries to. Four Gospels narrating one Crucifixion is four bindings and one date.

**Every claim says what grounds it.** A `basis` line, in prose, on every claim,
plus the source-library record ids it rests on. A basis that merely restates
this repository's own prose is not a basis.

## What does not live here

Book names, chapter counts and canon order (`scripts/_canon.py`, from the
canonical edition's own index); the psalm correspondence
(`psalm-numbering.tsv`); the deuterocanon correspondence
(`deuterocanon-numbering.tsv`); an edition's departures from canonical
numbering (that edition's `verse-aliases.tsv`); and the identity, rights and
provenance of any source (`../works/`, under `guidance/sources.md`). This tree
names those; it never restates them.
