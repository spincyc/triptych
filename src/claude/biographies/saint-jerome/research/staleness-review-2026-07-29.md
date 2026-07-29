# Staleness review — 2026-07-29

## Exact trigger

`scripts/research-staleness explain claude biographies/saint-jerome` reported
the following changed inputs:

- `src/claude/biographies/saint-jerome/research/staleness-review-2026-07-27.md`;
- USCCB-second-2019 Catechism passage records 270; 277; 391–395; 550;
  1667–1673; 1700–1706; 1734–1735; 1857–1859; 2111; 2116–2117; and
  2846–2854 under
  `src/sources/works/catholic-church/catechism/editions/english-usccb-second-2019/passages/`.

The ignored research-first rewrite was drafted from the edition-local and
paired-provider research records before the current Claude publication prose
was consulted. The current prose was then inspected, an unchanged minimal
modified treatment was prepared, and old, modified, and rewritten treatments
were compared claim by claim under
`build/staleness/claude/biographies/saint-jerome/`.

## Claim comparison

| Consequential claim | Old | Modified | Rewritten | Effect of changed inputs |
|---|---|---|---|---|
| Jerome's birth and death require competing chronologies rather than false precision | c. 347 working date with 331 preserved; death in 419 or 420 | Identical | Retained | None |
| Stridon remains unidentified and cannot establish a modern nationality | Explicit | Identical | Retained | None |
| The Ciceronian dream is a later, rhetorically situated self-report contested by Rufinus | Explicit | Identical | Retained | None |
| Service to Damasus does not make Jerome a fourth-century cardinal | Explicit | Identical | Retained | None |
| Paula, Eustochium, Marcella, Jewish teachers, scribes, patrons, and assistants were agents in the work | Explicit | Identical | Retained in more compressed form | None |
| The sources establish pressure surrounding the 385 departure, not a recoverable formal trial | Explicit | Identical | Retained | None |
| Jerome was the decisive individual contributor to, but not the solitary translator of, the composite Vulgate | Explicit | Identical | Retained | None |
| Jerome's learning and scriptural devotion must be narrated together with ascetic hierarchy, invective, and partisan self-presentation | Explicit | Identical | Retained | None |
| The Origenist, ascetic, Augustinian, and Pelagian controversies require sequenced, source-identified treatment | Explicit | Identical | Retained in synthesis | None |
| The 416 violence is multiply reported while responsibility remains attributed rather than judicially proved | Explicit | Identical | Retained | None |
| CCC 133 documents reception of Jerome's scriptural maxim rather than his whole life or every doctrine | Explicitly bounded | Identical | Retained as bounded official reception | None |
| Official Catholic reception does not authenticate disputed dates, legends, relics, tactics, or every attribution | Explicit | Identical | Retained | None |
| Lion, cardinal, and relic traditions belong to reception history with their actual source limits | Explicit | Identical | Retained in more compressed form | None |

The modified treatment differs from the old edition in neither wording nor
substance. The rewritten treatment differs in organization and compression
but not in any consequential claim. The prior review adds no new Jerome
evidence. The new Catechism loci concern divine power, demons and temptation,
exorcism and sacramentals, human dignity and freedom, responsibility, mortal
sin, superstition, and occult practices. None supplies evidence for Jerome's
life, chronology, biblical work, collaborators, controversies, or reception,
and none changes the edition's bounded use of CCC 133. The changed inputs add,
remove, strengthen, weaken, and contradict no reader-facing conclusion.

## Verdict

**No material change.** No publication source, PDF, web edition, binding,
catalog, release, currentness, or review-state revision is warranted. The
staleness ledger was not changed and this review does not rebaseline the
edition.
