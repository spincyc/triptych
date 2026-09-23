# Every cycle the Claude Eighteenth Sunday production entered

Run `71b6f89518984232`, `proper-study` v6, provider `claude`, identity
`liturgy/roman-rite/1962/propers/temporal/58-eighteenth-after-pentecost`,
date 2026-09-27, audience "adult parish assembly". The run was seeded at
commit `fa5355745`, and its terminal disposition is **ACCEPTED**, with one
standing escalation (STU-005). 57 packets, 57 accepted results, 3
interventions. The engine's own record is archived in the leaf under
`evaluations/proper-study-results/71b6f89518984232/`. This file is the
driver's account of why the run went round, which the run directory does
not state.

## Where the rounds went

| Stage | Results | Failing rounds |
| --- | ---: | ---: |
| research-review | 8 | 5 |
| study-review | 4 | 3 |
| synthesis-review | 2 | 1 |
| homily-review | 2 | 1 |
| every gate, visual-review, web-review | 1 each | 0 |

Ten cycles in all, which are the run's non-PASS transitions. No stage
exhausted a budget. The closest approach was research-review at three
consecutive purely novel failing rounds against `max_novel_iterations` of
four.

## The cycles, in order

| # | Stage that found it | Owner | What it was |
| ---: | --- | --- | --- |
| 1 | research-review 0 | research | The sweep called witnesses unreachable that the library registers (Cassiodorus tracked in the checkout, Jerome in PL 26, Hilary in CSEL 22). The comparison invented a conflict over Mt 9:8. A controlling English-rights inventory sat outside the seal, and no dated Ordo witnessed 27 September. |
| 2 | research-review 1 | research | The same class again, for the principal witnesses: Augustine's registered NPNF delivery and his tracked Latin, and PL 70. A Catena sentence was attributed to Jerome. |
| 3 | research-review 2 | research | The same class a third time: Bellarmine, Chrysostom in PG 55, Theodoret in PG 80/82, Aquinas in the Venice tomus. Rupert of Deutz and the *Liturgical Year* continuation read the Gospel ministerially, against the record's negative. |
| 4 | research-review 3 | research | Theophylact in PG 124; six registered liturgical commentators, Bl. Schuster among them, that no step sweeps; the continuation attributed to Guéranger; an unsupported claim that the Gospel–Offertory pairing is recent. |
| 5 | study-review 0 | research, then study | Hilary and Rabanus quoted only as the Catena reports them (STU-001); a manufactured city conflict, a Chrysostom sentence on the wrong verse, duplicated anagogical senses, and an undated Ecclesiasticus (STU-002 to STU-005). |
| 6 | research-review 5 | research | Inserting the new Ambrose paragraph displaced a sentence, so Aquinas's tropology read as Ambrose's. |
| 7 | study-review 1 | study | The comparison no longer matched the revised readings (STU-014). STU-005 was escalated. |
| 8 | study-review 2 | research | The interpretation record lagged the reviewed study on Mt 9:8, the anagogical senses and a Chrysostom placement (STU-020). |
| 9 | synthesis-review 0 | synthesis | A second disagreement asserted where the study has one; a gloss extended from Aquinas to two others; the critics' range for Matthew dropped from page 2. |
| 10 | homily-review 0 | homily | One sentence made humility the one gift not received from God (HOM-001), against the Collect and Orange canon 6. |

## What the recurring class was, and what repaired it

Cycles 1 to 4 were one defect. The commentary index maps works, and nothing
linked those works to the Migne volumes, collected-works tomes and
translation anthologies that hold them, or to liturgical commentaries keyed
by Mass. Each research round swept by work record, and each cold review
found more holdings by other means. Two changes repaired it; the maintainer
authorized both mid-run, and each merged while the run was held between
stages, so no reviewer's sealed inputs moved under it:

- `src/sources/inventories/source-containment-v1.toml` and `discover`
  holdings, stated as Rule 13 of `guidance/catena.md`;
- `src/sources/commentary/formulary-loci.yaml`, the author-standing registry
  and the `formulary` verb, stated as Rule 14.

Research iteration 4 swept with both, and research-review accepted it on the
next round.

## Host interventions

| # | Stage | What |
| ---: | --- | --- |
| 0000 | resolve-context | The host could not dispatch at a packet's declared effort. The first six agent stages inherited `xhigh`, above the declared `high` of their author stages. |
| 0001 | research-review 2 | The driver session restarted; the reviewer stopped without a result. It was reconciled and one fresh reviewer relaunched on the same packet. From here, pinned-effort agent definitions dispatched every stage at its declared level. The model changed from `claude-opus-5[1m]` to `claude-opus-5-5[1m]`. |
| 0002 | research-review 7 | A host usage limit stopped the reviewer before it wrote a result. It was reconciled after the reset and the same reviewer resumed from its transcript. |

**Model provenance.** The context and research stages through
research-review iteration 1 ran as `claude-opus-5[1m]`; everything after, as
`claude-opus-5-5[1m]`. Every render-relevant source was written after the
switch. The one Opus 5 file in the render path was a 74-byte `main.tex`
placeholder, since replaced. The leaf's `generation-metadata.tex` therefore
declares `claude-opus-5-5[1m]` for every author and derive stage, and
following the leaf-57 precedent it declares no research-stage contribution,
because research records are not render sources.

## Maintainer decisions taken during the run

Decisions D1 to D12, their timing and their reasons are in
[the plan](../../../guidance/liturgy/liturgical-commentators-plan-2026-09-22.md).
Two of them landed mid-run, each at a moment when the file they change was
not sealed into any accepted review:

- D1, the Blessed as anchored second authors, in the hold before research
  iteration 4;
- D11, a different-Gospel commentator cited only for shared elements, in
  the hold before research iteration 5, when every downstream document was
  already rerunning.

The artifact gate re-verified every accepted seal after both.

## Lessons, promoted or declined

- **Promoted:** containment and Mass-keyed discovery (Rules 13 and 14); the
  staleness writer that no longer drops hand-written obligations; a
  scratch copy of the repository kept inside a clone needs its own `.git`,
  since without one its git commands reach the live checkout. The last is
  recorded in `PROJECT-WORK.md`.
- **Declined:** reopening the accepted study for HOM-011, one clause, at the
  cost of three documents' reviews. The homily's HOM-010, the Introit's
  date and Chrysologus are instead recorded as this leaf's revision
  obligations in the research-staleness ledger.
