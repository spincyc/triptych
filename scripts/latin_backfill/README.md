# The 1962 Latin backfill toolkit

These four scripts landed 1,034 Latin bodies in
`src/sources/calendars/roman-1962/propers.yaml` on 2026-09-03/04. They are kept
because the same work remains to be done for the 2,176 sung propers of that
calendar and for the whole postconciliar one, and because rebuilding them from
the commit history would be slower than reading them.

They are deliberately NOT registered tools. Each is a step in a human-driven
sequence rather than one question with a byte-stable answer, and `tmt.json` is
for the latter. Run them from the repository root.

## The sequence

    python3 scripts/latin_backfill/apply_lane.py  <lane>     # proposal -> source records
    python3 scripts/latin_backfill/land.py        <lane>...  # records  -> calendar + ledger
    python3 scripts/latin_backfill/reconcile.py             # ledger <-> calendar

A research lane writes `.scratch/backfill/<lane>/proposal.json`: one entry per
oration, carrying the 1962 reading, the public-domain antecedent's locus, the
differences between them, and a verdict. `apply_lane` turns the `matched`
entries into the passage, artifact and ledger records the source library
requires; `land` writes the bodies into the calendar and the rows into the
provenance ledger; `reconcile` puts the two back into agreement afterwards.

`orthography.py` normalises consonantal i to the calendar's declared j, by an
explicit map that REFUSES a word it has not been taught rather than guessing.
That refusal is a feature: it caught `Iob`, `iucundemur`, `Iosaphat` and a dozen
more, one lane at a time.

## What each guard is for, and what it cost to learn

`apply_lane` refuses to land a body that fails
`scripts/_latin_body_damage.py`, which `check-calendar-masses` also runs. It
imports that module rather than keeping a copy: the two drifted once, the
applier still refusing a question mark after the committed screen had learned
to allow a real one.

It also checks each body against the calendar's own `incipit` for that proper,
which is how a body landed against the wrong slot is caught, and resolves the
`occurrence` of a proper whose name repeats — palm-sunday prints seven
Procession Antiphons and the ledger keys on which one.

`land` replaces either an unavailable `text_status` block or a body this
backfill already landed, the second being the repair case. It retypes an
`absent` verdict from `rights-withheld` to `witness-gap` ONLY where the ledger
row is a bare stub: a row carrying a collated finding is destroyed by the
retype, and that discarded St Albert's `collated-exact` reading of the 1962
facsimile before it was caught.

`reconcile` uses the checker's own `body_owners` walk rather than re-deriving
it, because a hand-rolled walk missed a form-bearing proper and dropped a row
the checker then demanded. It collapses duplicate keys in favour of the landed
row over a leftover stub, and names any row it drops that carried a collated
finding.

## What is NOT in here, and belongs to the repository proper

  * `scripts/_latin_body_damage.py` — refuses a body that is a recogniser
    reading rather than a page reading. Run by `check-calendar-masses`.
  * `tools/audit-latin-body-substitutions` — finds the damage that screen
    cannot: a token that becomes a known word under one substitution. Reports,
    never edits.

## The rules these scripts assume

All in `guidance/propers-for-agents.md`:

  * a transformation changes how a word is spelled; a variant changes which
    word is said;
  * an order is not a contribution, and neither is filling a rubrical blank;
  * reproduce the conclusion the target prints, at the length it prints it;
  * a chant body carries the sung words, not the Missal's printed citation.

And the rights position they rest on is
`src/sources/inventories/missale-romanum-1962-facsimile-rights-v1.toml`:
17 U.S.C. 103(b) plus a public-domain witness, never an assertion about the
1962 book.
