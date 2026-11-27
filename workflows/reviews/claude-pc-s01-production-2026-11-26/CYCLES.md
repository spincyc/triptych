# Every cycle the Claude postconciliar First Sunday of Advent, Year B production entered

Run `99f04ef5cf9b711b`, `proper-study` v20, provider `claude`, identity
`liturgy/roman-rite/postconciliar/roman-missal-third-edition-en-us-2011/propers/temporal/pc-s01-first-sunday-of-advent-year-b`,
date 2026-11-29, audience "adult parish assembly". It was seeded at `cbccbfcb3b`,
the authorization commit.

Terminal disposition **ACCEPTED**, with no escalations: 41 packets, 41 submitted
results and 17 recorded interventions. The engine's own record is archived in
the leaf under `evaluations/proper-study-results/99f04ef5cf9b711b/`, written by
`tools/proper-study-run-archive`. This file is the driver's account of why the
run went round, which the run directory does not state.

Sunday, 29 November 2026 is the First Sunday of Advent and opens Lectionary
Year B: violet, Psalter Week I, Lectionary no. 2 (Is 63:16b-17, 19b; 64:2-7 /
Ps 80 / 1 Cor 1:3-9 / Mk 13:33-37). The Gloria is omitted and the Creed is said;
the Missal appoints Preface I of Advent, and the Advent solemn blessing is
optional. Under the Universal Norms a Sunday of Advent yields to no feast; Saint
Andrew falls on Monday 30 November. Twelve appointed elements are keyed.

A GPT leaf exists for this identity and is published. This production is
independent of it. Every brief closed that leaf, its release records and its
production records, the GPT 1962 Advent record a profile links, and the 1962
First Sunday of Advent leaves of either provider.

## Commits

| Commit | What |
| --- | --- |
| `cbccbfcb3b` | The production-plan authorization line and paragraph bounding this production to identity `pc-s01` for provider `claude`, the work-register section and the promised deliverable. |
| `431fac11e1` | Source registrations, the Chrysostom 1 Cor 1:7-9 passage and fragment-loci edge, the source-family ledger snapshot, the edition registry rows for `PC-S01-B` and the shared Missal formulary owner, committed after artifact-gates 0. |
| `c861ed623d` | The leaf: the reviewed source checkpoint. All three editions carry the stamp `2026-11-26T23:01:57Z`. |
| `1409c698c5` | Generate-web 0's receipt and the engine's evaluation record. |
| `8320587711` | The installation. |

The browser products for the committed base were built cold in a clean,
detached worktree (13 products, 30,454 files), because the run's uncommitted
leaf would have changed family inputs in the working checkout. The pinned
pandoc 3.11 and Markdown 3.10.3 were installed outside the checkout, and the
native TeX runtime cache (`wasmtex-2026-47ff73bab1a2e548`) was verified before
seeding. At the base `make -k check-sources` failed only in
`check-source-containment`, on the two inherited periodical-issue records.

## Where the rounds went

| Stage | Results | Failing rounds |
| --- | ---: | ---: |
| research, source-registration, research-preflight | 3 each | 0 |
| research-review | 3 | 2 |
| author-study, study-preflight | 3 each | 0 |
| study-review | 3 | 2 |
| derive-synthesis, synthesis-preflight | 2 each | 0 |
| synthesis-review | 2 | 1 |
| derive-homily, homily-preflight | 2 each | 0 |
| homily-review | 2 | 1 |
| every other stage | one | 0 |

Six cycles, all real defects that cold reviewers found. No seal went stale and
no stage reopened an upstream owner. The web review passed on its first try.

## The cycles, in order

| # | Stage that found it | Owner | What it was |
| ---: | --- | --- | --- |
| 1 | research-review 0 | research | **RES-CHR-001:** the chronology record and annotations fingerprinted an earlier `propers/verified.md`. **RES-ATT-001:** two comments on Mark 13:32-33 credited to Bede are verbatim Jerome, *In Matthaeum* IV on Mt 24:36 and 24:42-43 (PL 26 cols. 181-182). **RES-TXT-001:** the psalm-to-first-reading row said the refrain and Isaiah 63:17b ask the same thing; *Converte nos* asks God to turn us, *Convertere* asks God to return. Research 1 and source-registration 1 repaired all three. |
| 2 | research-review 1 | research | **RES-TXT-003:** the RES-TXT-001 repair overcorrected. It denied a join the witnesses make: Jerome reads 63:17b "Convertere ... sive converte nos" (PL 24 col. 643), and Aquinas sets Lam 5:21 *converte nos* beside Ps 89 under Isaiah's *convertere* ([85023]). Research 2 kept the textual distinction and recorded both joins; research-review 2 passed. Source-registration 2 also replaced a disposition criterion research 2 had invented (`appointed-passage-comment`) with the existing `exposition-of-the-extent`. |
| 3 | study-review 0 | study | Nine blocking findings. **STU-001:** each interpretation closed on a "rest of the Mass" roll call giving the other texts invented roles. **STU-002 to STU-005:** the prose narrated its own method and caution, credited texts with moves they do not make, used emphatic fragments, and closed paragraphs on restating maxims. **STU-006:** Aquinas's literal sense of *Descendisti* is the Exodus from Egypt, not Sinai. **STU-007:** Chrysostom's Homily 2 on 1 Cor was misordered. **STU-008:** the study's own torn-heavens inference was credited to Cyril. **STU-009:** the Clementine *et orate* was given as the Gospel's words; the Ordo reads *Videte, vigilate*. |
| 4 | study-review 1 | study | **STU-015:** "Augustine's comment is four words" misreported En. in Ps. 84.9, which answers the study's own question (Christ given as man, to be given as God). **STU-016:** the STU-001 repair produced the opposite defect: removing the roll calls removed the clause by which the Alleluia verse, the Prayer over the Offerings and the solemn blessing contributed to interpretation 2, and the Preface to interpretation 3. **STU-017:** repeated author lists, a shared "Taken together" closer and refrains. Author-study 2 made contained repairs and study-review 2 passed. |
| 5 | synthesis-review 0 | concise study | **SYN-001:** the concise invented a contrast between Augustine and Bellarmine on Ps 84's "earth"; Augustine reads it first of Christ born of the Virgin and gives confession as his second sense. **SYN-002:** it said the Entrance antiphon departs from "both Latin psalters"; Augustine's psalter reads *qui te exspectant*, and the research claims only a difference from the Clementine and the Nova Vulgata. **SYN-003:** the Missal-prayers section was a roll call with restating closers. Derive-synthesis 1 repaired them; synthesis-review 1 passed. |
| 6 | homily-review 0 | homily | **HOM-001:** the homily's English of Augustine on the Communion verse, "unless he gives it to whom you confess", lost the sense of *nisi ille dederit cui confiteris*: the one confessed to is the one who gives. Derive-homily 1 spoke its own English of the Latin and cleared HOM-002 to HOM-006; homily-review 1 passed. |

## Host interventions and events

| # | Stage | What |
| ---: | --- | --- |
| 0000 | resolve-context | The dispatch envelope. Every agent stage ran as a fresh Claude Code harness subagent (`claude-opus-5-5`) with no inherited conversation, at its packet's declared effort: authors `high`, reviews `xhigh`. Each worker received its packet by exact path and SHA-256, a result path and a worker-owned scratch directory, the pinned environment, provenance, the reservation of git and `advance` to the driver, no tool or shared-calendar edits, and the independence terms. |
| 0001-0006 | research 0-2, source-registration 0-2 | Host notes (sealed products for the base, working projections at the producers' default destination, base state, toolchain); the accepted earlier results and receipts as read-only context; reminders of defect classes earlier Claude research reviews blocked on. Research 2's note named the second round on the same row. Research 0's note clarified that the envelope's "registry" ban did not cover edition registry rows the packet assigns. |
| 0007-0009 | author-study 0-2 | The own-contribution-line reminder, the review results as read-only context, and the study defect classes of earlier Claude runs, including the 1962 Advent run's stock-formula overcorrection. Iteration 2 named the two-sided-rule overcorrection (STU-001, then STU-016) and asked for contained repairs. |
| 0010-0011 | derive-synthesis 0-1 | The accepted reviews, the standing study advisories, the sealed research rows the study corrects, the corrections a compression could undo, and, in iteration 1, the observed matching overstatement in the sealed study. |
| 0012-0013 | derive-homily 0-1 | The accepted reviews and standing advisories (SYN-006 among them), the settled corrections, earlier Claude homily defect classes and, in iteration 1, the studies' matching English of Augustine. |
| 0014 | build-artifacts 0 | The provenance check covering every authoring iteration; the checkpoint commit to follow. |
| 0015 | generate-web 0 | The checkpoint commits and the edition sources closed. |
| 0016 | install-publication 0 | The installer brief: browser-products `record` and `check`, not `prune`; serial scoped binding refreshes; only the Claude cell of the Year B row of `library/novus-ordo-liturgy.md` and this provider's inventory rows; the primary-provider marker rule; the GPT entries preserved without opening the GPT leaf. |

Driver additions the engine did not record as interventions: the constant host
note given to every review (sealed products, working projections read-only, the
base state, the toolchain), and the generate-web note given again to web review.
None of them, and none of the recorded interventions, supplied a content
conclusion; each finding reached its owner through the packet's own route.

Two host events. Research 0's worker left a shell wait loop on its own log
running after hand-back; the driver confirmed it was that worker's and stopped
it. One worker ran repository Python without `PYTHONDONTWRITEBYTECODE`, leaving
bytecode caches under `scripts/` and `tools/` (none under `src/`); the driver
removed them before the checkpoint commit.

## Sources the run settled

- **Latin.** The Missal formulary and the *Ordo lectionum Missae* govern; the
  Nova Vulgata for the readings, the Clementine Vulgate for comparison.
- **English.** Douay-Rheims for Scripture, with both chapter numberings for
  Isaiah. The approved U.S. Missal and Lectionary English is treated by
  description and locus only.
- **Registered by the run (`431fac11e1`):** restricted artifact records for the
  Nova Vulgata Isaiah, NABRE Isaiah 64, the USCCB readings page for 29 November
  2026, GIRM chapter II, the Book of Blessings Advent wreath, and New Advent
  pages of Chrysostom, Augustine and Cyril; Chrysostom's Homily 2 on 1 Cor at
  1:7-9 as a verified passage.

## Findings that did not gate

Across eleven cold reviews the run raised twenty distinct blocking findings,
all repaired. Standing advisories are recorded in the leaf's
`evaluations/blocking-findings-v1.toml` and the review results:
- research: RES-NEG-002;
- study: STU-023 to STU-030;
- concise: SYN-006;
- homily: HOM-007 and HOM-008;
- web: WEB-001.

Worth a first revision, in this order:
- **WEB-001 and SYN-006.** The expansive study describes the solemn blessing's
  second invocation three times as "firm in faith, glad in hope and active in
  charity" (`sections/05-appointed-texts.tex`, `10-texts-in-setting.tex`,
  `40-clay-and-faithful-potter.tex`), and the concise study once
  (`sections/concise/10-commentary.tex`). That is the approved English with one
  word changed, which the postconciliar profile forbids. Three reviewers judged it
  advisory; the fix is the map table's own description ("strengthen them in
  faith, hope and charity"). The approved wording was checked only in a
  secondary transcription.
- **The study's psalter claim.** `sections/10-texts-in-setting.tex` (Entrance
  Antiphon) still says the antiphon is not a straight quotation of "either Latin
  psalter"; the concise study was corrected (SYN-002) and now differs from it.
- **The studies' English of Augustine, En. in Ps. 84.15.** Both studies print
  "unless he gives it to whom you confess" beside the Latin; the homily was
  corrected (HOM-001).
- **Sealed research rows.** `research/interpretations.md` Reading 1 still credits
  Sinai to Aquinas, and `scope.md` and `interpretations.md` summarise En. in Ps.
  84.9 without "given as man, to be given as God". The studies follow the sources.

## What this run leaves for the owner

| Item | Evidence | Why it is not done here |
| --- | --- | --- |
| `src/sources/calendars/postconciliar/propers.yaml` gives the `advent-1` Entrance antiphon as `Psalm 25:1-3`, with no `Cf.` and no psalm-numbering flag; the Missal prints Cf. Ps 24, 1-3. | resolve-context 0; research 0; source-registration 0-2 | Shared calendar record. |
| The `work.bede.in-marci-evangelium-expositio` locus pattern admits only Mark 10, so no Mark 13 passage record can be made. | research 0-1; source-registration 0-2 | Shared source library. |
| Research 0 reported a tracked Feltoe payload absent from the checkout; the driver did not verify it. | research 0 | Shared source library. |
| The generated Scriptural Date and Location page prints Isaiah in Clementine numbering with no key, gives 1 Cor 1:3-9 no place, numbers the psalms inconsistently, and prints article titles with a right quote at both ends. | research-review 1-2; synthesis-review 0-1; web-review 0 | Shared chronology generator and corpus. |
| The scope appendix's record paths render as unlinked code text on the site, as in about fifty Claude proper leaves. | web-review 0 | The web-edition converter. |
| A lead: in PL 24 Jerome answers "none calls on your name" with "let us call on his name and confess", close to the homily's central move; the research records do not note it. | homily-review 0 (raw OCR only) | A research lead for a revision. |
| The DCO Jerome site's TLS certificate had expired, and the USCCB readings page answered 403 or a bot check; workers read Migne page images and registered copies instead. | resolve-context 0; research 0; reviews | External availability. |

## After acceptance

The run is archived in the leaf. Integration with `main` and publication are
outside the authorization recorded for this production.
