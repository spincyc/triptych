# Every cycle the Claude Last Sunday after Pentecost production entered

Run `11c5af05fe374203`, `proper-study` v19, provider `claude`, identity
`liturgy/roman-rite/1962/propers/temporal/68-twenty-fourth-after-pentecost`,
date 2026-11-22, audience "adult parish assembly". Seeded at `8133098784`, the
authorization commit. Terminal disposition **ACCEPTED**, with no escalations:
36 packets, 36 submitted results, 16 recorded
interventions. One further worker result, a BLOCKED from install-publication 0
for a missing local runtime cache, was held back and never submitted; the same
worker finished the stage after the driver hydrated the cache (cycle 7). The
engine's own record is archived in the leaf under
`evaluations/proper-study-results/11c5af05fe374203/`, written by
`tools/proper-study-run-archive`. This file is the driver's account of why the
run went round, which the run directory does not state.

Sunday, 22 November 2026 is the Twenty-fourth and Last Sunday after Pentecost
(II class, green), permanent identity `68`, the twenty-sixth Sunday after
Pentecost of a year whose Easter fell on 5 April. St Cecilia (III class) is
outranked. The Mass is printed on pp. 422-424 of the 1962 Missal, nos.
1769-1778, the last formulary of the Proper of Time; its five chants are the
Twenty-third Sunday's. Every word also stands in Pustet 1862 (pp. 359-360),
read on page images, so the publication mode is `complete`. No GPT leaf exists
for this identity; the briefs closed any such leaf, its release records and its
workflow records to every stage all the same.

## Before seeding

| Commit | What |
| --- | --- |
| `8133098784` | The production-plan authorization line and paragraph bounding this production to identity `68`, the work-register section and the promised deliverable. |

The host lacked node, the repository-pinned pandoc 3.11 and TeX Live when the
run began. The maintainer installed node and TeX Live; the driver installed
pandoc with `scripts/_install_web_edition_pandoc.py` into the workspace
scratch. Browser products were built cold for the committed base in a clean
detached worktree, because the in-progress leaf changes family inputs and the
dirty checkout refused a build ("browser product inputs changed").

## Where the rounds went

| Stage | Results | Failing rounds |
| --- | ---: | ---: |
| research | 2 | 1 required changes |
| research-review | 2 | 1 |
| source-registration | 3 | 0 |
| research-preflight | 3 | 1 (cycle 2) |
| author-study | 3 | 2 required changes |
| study-review | 3 | 2 |
| derive-synthesis | 1 | 0 |
| synthesis-review | 1 | 0 |
| derive-homily | 2 | 1 required change |
| homily-review | 2 | 1 |
| install-publication | 1 (one result held back) | 0 |
| every other stage | one per round | 0 |

There were seven cycles. Four were real defects that cold reviewers found in
the content (cycles 1, 3, 4 and 6); one was a defect in the driver's own host
note (cycle 2); one was a driver correction to the provenance declarations
(cycle 5); and one was the local runtime cache (cycle 7). No research, author
or content-review seal went stale. The driver committed the source
registrations (`be0db94a74`) and the leaf (`df490fc32c`) after the artifact
gates, so the web reader carries the stamp `2026-11-16T22:24:00Z`.

## The cycles, in order

| # | Stage that found it | Owner | What it was |
| ---: | --- | --- | --- |
| 1 | research-review 0 | research | **RES-001:** the Gospel, Mt 24:15-35, had no narrated event in the chronology corpus, so the date page would print Matthew's composition alone, although the corpus's own Maas source closes the Tuesday of the last week with the Olivet prophecies. Research 1 added the event `life-of-christ.prophecies-on-mount-olivet`, its binding and orientation (A.D. 29 within Maas's harmony, derived) and registered the Maas passage. **RES-002:** the research recommended Lasance's English for the Epistle and Gospel, where the 1962 profile assigns the scriptural elements to the Douay-Rheims. **RES-003:** Sicard's *Mitrale* treats four of the chants at VIII.23 and VIII.25 as well as VIII.24, and neither locus was in the matrix, bindings or dispositions. |
| 2 | research-preflight 0 | driver | **GATE-SOURCE-PROJECTION-CURRENT.** The driver's host note told workers to generate working projections into their own scratch directories with `--out`; the gate checks the producers' default destination, `.scratch/browser-data-work`. The note was corrected and recorded (intervention 0003), and source-registration 1 regenerated the projection there. No content changed. |
| 3 | study-review 0 | study | **STU-001:** the Communion's difficulty was answered by crediting four Fathers with a condition only Bede states on Mk 11:25. **STU-002:** the body mentioned commentators' other Masses three times beyond the one clause the three-document rule allows. **STU-003:** in every interpretation a link the study draws between two texts was stated as what a text says. **STU-004:** the study supplied its own English for the Postcommunion beside Lasance's. |
| 4 | study-review 1 | study | **STU-003 (standing):** the repair replaced the credited links with two fixed formulas ("set beside", "heard ... as") about twenty times, the overcorrection run 66's reviews failed on; the iteration-0 example rewrites had supplied the frames. **STU-007:** Jerome's anagogy of the letter to the exiles (*In Hier.* V, PL 24 cols. 891-894) was reversed: the Church as the exile going home, where Jerome has penitent sinners brought back to their own place, the Church. **STU-008:** lane 3 said three times that no Father takes "this generation" as a date, and the oration glosses recurred across sections. Author-study 2 stated each link as the study's own claim with its reason; study-review 2 passed in round three of four. |
| 5 | build-artifacts 0 | driver | `generation-metadata.tex` had contribution lines only for the iteration-0 authoring runs; author-study 1-2 and derive-homily 1 produced the accepted files. Sibling leaves 66 and 67 record every revising iteration. The driver added the three lines in the existing form before submitting the stage; the review seals cover only the provenance row, so no review went stale, and the same build worker recomputed the identities (intervention 0012). |
| 6 | homily-review 0 | homily | **HOM-001:** four of twelve paragraphs ended one sentence late, on a closer that restated the paragraph or turned it into a maxim; one softened "do not believe him" to "you need not believe him", and one put the Communion's condition "in our own hands", beyond Mk 11:25 or Bede. Derive-homily 1 cut the four closers and cleared the advisory HOM-002 (oral clarity). |
| 7 | install-publication 0 | environment | The checkout had no native TeX runtime cache, so `release-bindings status` could not derive the `native-tex-catalog` site source and stopped after fifteen minutes. The worker returned BLOCKED rather than fetch or write outside its scratch. The driver held the result back, hydrated the cache with `scripts/_native_tex_assets.py hydrate --fetch` from the declared public archives (3,048 files, runtime `wasmtex-2026-47ff73bab1a2e548`, verified), and resumed the same worker on the same packet (intervention 0015). It refreshed exactly the 61 bindings the installation moved. |

## Host interventions and events

| # | Stage | What |
| ---: | --- | --- |
| 0000 | resolve-context | The dispatch envelope. Every agent stage ran as a fresh Claude Code harness subagent (`claude-opus-5-5`) with no inherited conversation, at its packet's declared effort: authors `high`, reviews `xhigh`. Each worker received its packet by exact path and SHA-256, a result path, a worker-owned scratch directory, the environment, provenance, the reservation of git and `advance` to the driver, no tool or shared-calendar edits, and the independence terms. |
| 0001 | research 0 | The products build restarted after the host gained node; the worker was not to build. Four defect classes from runs 66 and 67's research reviews were named. |
| 0002 | source-registration 0 | Scratch isolation; read-only download receipts with hash re-verification; products built in a clean worktree. |
| 0003 | source-registration 1 | The corrected projection note (cycle 2). |
| 0004 | research 1 | RES-001's repair in the shared chronology corpus is within the stage's assignment, as the Thirty-second Sunday research did in `8db7c9e4fc`. |
| 0005 | source-registration 2 | Sidecar-delivered binary evidence (the Gregory *Homiliae* EPUB) is not a tracked file. |
| 0006-0008 | author-study 0-2 | The accepted research review's advisories as context, the register rules on which runs 66 and 67's study reviews failed, and, for iteration 2, the reviewer's finding that the previous fix had become a fixed formula. The last brief noted that review four was the final allowed round. |
| 0009 | derive-synthesis 0 | The study advisories as context the compression must not inherit, the earlier source corrections, and run 67's synthesis defect classes. |
| 0010-0011 | derive-homily 0-1 | The study and synthesis review results as context, the earlier homily defect classes, and a contained HOM-001 repair. |
| 0012 | build-artifacts 0 | The provenance correction (cycle 5). |
| 0013 | generate-web 0 | The checkpoint commits and closed edition sources. |
| 0014-0015 | install-publication 0 | The installer brief (scoped, serial binding refreshes; only this provider's catalog cell), then the cache hydration and resumption (cycle 7). |
| — | artifact-gates 0 | The driver committed `be0db94a74` and `df490fc32c`; after generate-web, the receipt `fe747f2d1b`; after installation, `caefcd2666`. |

None of the interventions supplied a content conclusion. Each review finding
reached its author through the packet's own route.

The host carries Python Markdown 3.11 and the repository pins 3.10.3. Every
stage, web probe and gate ran under a scratch virtualenv built from the two
requirements files, with `PYTHONDONTWRITEBYTECODE=1`.

## Sources the run settled

- **Latin.** The 1962 Missal governs, read on the page images (pp. 422-424,
  nos. 1769-1778); Pustet 1862 carries every word.
- **English.** Douay-Rheims for the Epistle, Gospel and other Scripture
  (RES-002); Lasance 1945 for the orations and chants, never supplemented by
  the guide's own rendering (STU-004).
- **Witnesses added by review.** Sicard, *Mitrale* VIII.23 and VIII.25
  (RES-003); Jerome, *In Hier.* V, read to the end of his sentences (PL 24
  cols. 891-894). `be0db94a74` registered Augustine's *Quaestiones
  Euangeliorum* I.37-39 and I.42 and *Enarrationes* on Ps 43.8-9 and 84.3-5 as
  verified passages with their fragment loci, the Catholic Encyclopedia Maas
  passage dating the Olivet discourse, the chronology event, binding and
  orientation for it, and the FSSP and ICRSP France Ordos for the date
  (restricted, metadata only).

## Findings that did not gate

Across nine cold reviews the run raised ten distinct blocking findings, all
repaired. Twelve standing advisories and one accepted finding remain, recorded
in the leaf's `evaluations/blocking-findings-v1.toml`:

- research: RES-005, and RES-006 accepted;
- study: STU-012 to STU-016;
- synthesis: SYN-001 to SYN-005;
- homily: HOM-003.

SYN-001 and HOM-003 are the ones worth a first revision. Both name the same
slip about where the Gospel begins: the concise study calls it "the second half"
of the Lord's answer and "the fifteenth verse of the Lord's answer", the homily
says "the first part of his answer is about Judea", and the expansive study's
`sections/00-opening.tex` carries the second phrase. The reading begins at
chapter verse 15; the answer begins at v. 4. STU-012 (Hilary's "food of the true
bread" is the knowledge of God, so any Eucharistic application is the study's
own step) stands in the expansive study only; the concise study and homily do
not use it.

## What this run leaves for the owner

| Item | Evidence | Why it is not done here |
| --- | --- | --- |
| No Latin-ledger row, passage record or collation covers nos. 1769-1778 or the identical chants of the Twenty-third Sunday. | resolve-context 0; research 0 | Shared ledger. |
| `formulary-loci.yaml` lacks Sicard VIII.23-25, Durandus VI.141-142, Rupert XII.23 and Fromage for this Mass; `discover` does not join Gregory *Hom. in Ev.* I, Augustine *Quaest. Ev.* I.37-42 or Bede on Mk 13 to this Gospel; there are no harvest alias groups for Rupert, Durandus, Sicard or Fromage. | research 0; source-registration 0-2 | Shared harvest records and tool. |
| There are no work records for Jerome *In Hieremiam* or Hilary *In Matthaeum*; Bede *In Marc.*'s locus pattern cannot address line loci; the NPNF I.8 and I.10 editions lack translator credit; PL 26 cols. 177-181 are not retained as page images. | source-registration 0-2 | Shared source registry. |
| The Olivet binding covers Mt 24:15-35 only; widening it over the whole discourse (Mt 24:36-25:46) would change other productions' generated chronology. The Ps 129 orientation row prints David's regnal range beside a proposed occasion for an anonymous psalm. | research 1 | The chronology corpus owner. |
| The generated date notes print Catholic Encyclopedia titles with a closing curly quote at both ends ('David, King,'), and the scope appendix names repository files a web reader cannot open, as leaf 67 does. | web-review 0 | Shared chronology generator and the 1962 profile or converter. |
| Unnumbered study sections make `\ref{sec:date-location}` print a bare section sign; the profile does not say where glossing an oration English's departure from the Latin ends and the guide's own rendering begins. | author-study 0-1 | The proper-study packet and `guidance/liturgy/roman-1962-propers.md`. |
| Authoring workers do not add their own contribution lines on revising iterations unless told; nothing checks that every iteration that produced an accepted file is declared. | build-artifacts 0 | The proper-study packet and the generation gate. |
| A checkout without the native TeX runtime cache cannot compute release bindings; nothing earlier in the run checks for it. | install-publication 0 | Workflow preflight or `workflows/OPERATOR.md`. |
| `research/scope.md` and `research/interpretations.md` still carry the research's reading that the study corrects (Jerome on Jer 29; "all three keep Chrysostom's literal sense"). | study-review 1 | The research records are sealed; a next revision of this leaf. |
