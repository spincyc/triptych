# Every cycle the Claude Twenty-sixth Sunday production entered

Run `ed9acebf389f8706`, `proper-study` v7, provider `claude`, identity
`liturgy/roman-rite/postconciliar/roman-missal-third-edition-en-us-2011/propers/temporal/pc-s52-twenty-sixth-sunday-in-ordinary-time-year-a`,
date 2026-09-27, audience "adult parish assembly". Seeded at commit
`8f5a1fa0f`. Terminal disposition **ACCEPTED**, with no escalations: 24
packets, 24 accepted results, 2 interventions. The engine's own record is
archived in the leaf under
`evaluations/proper-study-results/ed9acebf389f8706/`. This file is the
driver's account of why the run went round, which the run directory does not
state.

This was the first Claude run of `proper-study` v7, the version that makes the
authority contract mandatory and has the research reviewer confirm each
liturgical commentator's element comparison and standing.

## Where the rounds went

| Stage | Results | Failing rounds |
| --- | ---: | ---: |
| research-review | 2 | 1 |
| study-review | 1 | 0 |
| synthesis-review | 1 | 0 |
| homily-review | 1 | 0 |
| visual-review | 1 | 0 |
| web-review | 1 | 0 |
| every gate | one each | 0 |

The run entered one cycle, which is its one non-PASS transition. No gate
failed and no stage came near a budget.

## The cycle

| # | Stage that found it | Owner it went to | What it was |
| ---: | --- | --- | --- |
| 1 | research-review 0 | research | RES-001: the interpretation record reported Augustine's "be ye sheep" (*In Ioh. ev. tract.* 48.4) as addressed to the unbelievers of John 10:26 and cited it for the two-peoples reading's Alleluia contribution. In the tracked NPNF text the exhortation is to his own hearers, and of those addressed at 10:26 he says they were "predestined to everlasting destruction". The row reversed what the author says at the verse it cited. Research iteration 1 repaired it and cleared the six advisories; research-review iteration 1 passed with two advisories. |

The finding was a real defect in the work, visible to no mechanical gate. It
was caught before any prose was written, so no document reran.

## Findings that did not gate

Across its seven cold reviews the run raised 1 blocking finding and 27
advisories. Those that stand are in the leaf's
`evaluations/blocking-findings-v1.toml`. Two study advisories concern
accuracy rather than presentation, and the reviewer chose not to block on
them:

- STU-002: a Psalm 17 quotation attributed through Augustine matches neither
  the NPNF wording nor the Douay-Rheims the study uses.
- STU-010: the study says Ezekiel 18:25 opens with the people's words rather
  than the Lord's, where the verse opens with the Lord's "And you have said".

The driver adds no findings of its own, so neither was forced back through the
study. Both are candidates for the leaf's first revision.

**A research-owned record gap stands**, the same class the Twenty-fifth Sunday
run ended with. The derive-synthesis worker reported that
`research/interpretations.md` still carries the points STU-001, STU-007 and
STU-008 corrected in the study, and that RES-008 and RES-009 remain open there.
No stage after research-review writes research records. None of these changes
a claim in the three documents or the web edition, and the concise study
follows the corrected reading at each point.

The visual review's VIS-001 (the Gospel's dossier entry splits across study
pages 27-28) and the web review's WEB-001 (the Responsorial Psalm's response
and verses render as one quotation block, a converter behaviour the published
Twenty-fifth Sunday edition shares) are layout advisories.

## Host interventions

| # | Stage | What |
| ---: | --- | --- |
| 0000 | resolve-context | The host exposes no per-dispatch effort control and no pinned-effort agent definition was loaded, so every agent stage ran at the driver session's effort whatever it declared. The subagent model was inherited from the driver, `claude-opus-5-5[1m]`. |
| 0001 | derive-synthesis | The first dispatch stopped on the host's weekly usage limit (HTTP 429) while reading, before writing anything. After the reset one fresh worker ran the same packet from an empty scratch directory. |

**Model provenance.** Every agent stage ran as `claude-opus-5-5[1m]`. The
leaf's `generation-metadata.tex` declares that model for each author and
derive stage, with the packet-declared effort and the host deviation.

## What was repaired because of this run

The workflow definition did not change. Before seeding, the driver corrected
the postconciliar calendar's Twenty-fifth Sunday cell, where the Claude links
followed the ChatGPT edition's unlabelled ones and read as the same edition's,
and added the check that now refuses such a cell to the proper-study
publication gate (`ba4e08822`). This run's install stage wired the
Twenty-sixth Sunday cell under that check, with every label naming Claude.

After acceptance the driver regenerated the source-reader projection the
research checkpoint had left stale, and re-recorded its fourteen release
bindings (`5e92eaba6`). The Twenty-fifth Sunday run met the same gap.

## What this run leaves for the owner

| Item | Evidence | Why it is not done here |
| --- | --- | --- |
| The source-family migration ledger's `canonical_catalog_snapshot` is stale, so `make check-sources` and `check-deployment-sources` fail | `tools/source-family-migration check` | The re-pin (`refresh --audited-on <date> --accept-canonical-catalog`, as in `a8182ac36`) was refused by the host's permission policy as a check bypass. It needs the maintainer's decision. |
| The registered 2002 Missal passage `dominica-xxvi-per-annum` gives artifact pp. 302-303, which are the end of Christ the King; the Week XXVI heading is at physical p. 289 | resolve-context 0 result | Owned by the source records; only the GPT 1962 leaf 50 binds it. The Twenty-fifth Sunday run reported the same record. |
| `titulos-liturgicos-septiembre` and the PC-S51-A row of `occurrences-2026.md` give printed p. 55; the September list is on p. 56 | resolve-context 0 result | Owned by the Twenty-fifth Sunday leaf and the source record |
| The `ot-26` entry of `src/sources/calendars/postconciliar/propers.yaml` lacks the Communion antiphon's Cf., says both antiphons follow *Vel*, and mixes numbering in "25:4bc-5" | resolve-context 0 result | Owned by the calendar index |
