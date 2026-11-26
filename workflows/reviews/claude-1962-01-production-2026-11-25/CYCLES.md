# Every cycle the Claude First Sunday of Advent production entered

Run `77c1ca91ef2d5e93`, `proper-study` v20, provider `claude`, identity
`liturgy/roman-rite/1962/propers/temporal/01-first-sunday-of-advent`, date
2026-11-29, audience "adult parish assembly". It was seeded at `81696af683`,
the authorization commit.

Terminal disposition **ACCEPTED**, with no escalations: 50 packets, 50 submitted
results and 18 recorded interventions. The engine's own record is archived in
the leaf under `evaluations/proper-study-results/77c1ca91ef2d5e93/`, written by
`tools/proper-study-run-archive`. This file is the driver's account of why the
run went round, which the run directory does not state.

Sunday, 29 November 2026 is the First Sunday of Advent: I class, violet, the
first formulary of the Proper of Time, printed pp. 1-2 of the 1962 Missal,
nos. 1-10. St Saturninus has an ordinary commemoration, which an I-class
Sunday does not admit at any Mass (RG 109, 111 a; RGMR 434 a). The dated FSSP
France and ICRSP France Ordos name none. One formulary and one set of orations
serve every Mass, so the publication mode is `complete`.

A GPT leaf exists for this identity and is published. This production is
independent of it. Every brief closed that leaf, its release records and its
workflow records to every stage.

## Before seeding and during the run

| Commit | What |
| --- | --- |
| `81696af683` | The production-plan authorization line and paragraph bounding this production to identity `01` for provider `claude`, the work-register section and the promised deliverable. |
| `df614e24db` | The byte-exact regeneration, at the base, of `src/sources/commentary/mass-commentary-corpus.yaml`, which was stale on main, so that `check-commentary-corpus` passed. A regeneration in a clean worktree at the base matched it. |
| `6284b8727e` | Source registrations and the chronology corpus, committed after artifact-gates 0. |
| `7d290f7814` | The leaf: the first reviewed source checkpoint. |
| `8e60db2893` | The WEB-001 repair checkpoint (cycle 6). All three editions carry the stamp `2026-11-26T01:51:31Z`. |
| `0a7d731bf1` | Generate-web 1's receipt and the engine's evaluation record. |
| `a7612f0561` | The installation. |

The browser products for the committed base were built cold in a clean,
detached worktree: 13 products, 30,437 files. The run's uncommitted leaf
changes alter family inputs, so a build in the working checkout would have
refused. The pinned pandoc 3.11 and Markdown 3.10.3 were installed outside the
checkout. The native TeX runtime cache was verified
(`wasmtex-2026-47ff73bab1a2e548`) before the run reached installation; its
absence was run 68's install blocker.

## Where the rounds went

| Stage | Results | Failing rounds |
| --- | ---: | ---: |
| research | 2 | 1 required changes |
| research-review | 2 | 1 |
| source-registration | 2 | 0 |
| author-study | 5 | 3 required changes, 1 routed from web review |
| study-review | 5 | 3 |
| derive-synthesis | 3 | 1 required change |
| synthesis-review | 3 | 1 |
| derive-homily | 2 | 0 |
| homily-review | 2 | 0 |
| build-artifacts, artifact-gates, generate-web | 2 each | 0 |
| web-review | 2 | 1 |
| every other stage | one per round | 0 |

There were seven cycles:
- six were real defects that cold reviewers found in the content (cycles 1-6);
- one was the driver's own session restart during installation (cycle 7).

No research, author or content-review seal went stale. The study took all four
of its first review rounds. Web review 0 then reopened it through the packet's
own route, and the study's next review counter began afresh.

## The cycles, in order

| # | Stage that found it | Owner | What it was |
| ---: | --- | --- | --- |
| 1 | research-review 0 | research | **RES-001:** the research said Gregory's Homily I on the Gospels has five sections and narrowed its bindings to 1.1-5. The tracked artifact prints §6 inline after *in laqueo ruinae deprehensi?*. **RES-002:** reading 2 merged Augustine's and Ambrose's figures. For Augustine (Ep. 199.39) sun, moon and stars are all the Church; Ambrose has his own figure. **RES-003:** the controlling claim said "the Fathers call two comings" what Augustine (En. Ps. 84.9) calls Christ given as man and to be given as God; no cited locus makes that identification. Research 1 and source-registration 1 repaired all three, and research-review 1 passed. |
| 2 | study-review 0 | study | **STU-001:** no interpretation engaged the whole appointed Mass, although the manifest declares all ten elements in every lane. **STU-002:** Augustine's reasons in Ep. 199 for reading the signs of the Church were missing; only his conclusion was given. **STU-003:** the third interpretation credited the Collect with rousing the sleeper; it asks the Lord to rouse his own power and come (Ps 79:3). **STU-004:** the first interpretation had no distinct allegorical sense. **STU-005 and STU-006:** the study narrated its own refusal to harmonize, and closers restated the paragraph. |
| 3 | study-review 1 | study | **STU-015:** the STU-001 repair produced the overcorrection that failed run 68. Before most links the prose told the reader what a Father did not say, then labelled the join with a rotating stock formula. Author-study 2 stated each link once in the study's own voice with its reason. |
| 4 | study-review 2 | study | **STU-020:** the fourth interpretation named the Mass Sicard and Rupert knew, whose Gospel was the entry into Jerusalem. The three-document profile allows a commentator's other Gospel in at most one clause of the scope appendix. Author-study 3 made a contained repair, and study-review 3 passed in the fourth and last round. |
| 5 | synthesis-review 0 | concise study | **SYN-001:** three places recapped the interpretations in successive blocks instead of making them meet on a question. **SYN-002:** compression moved the study's words into an author's mouth or dropped a qualification. **SYN-003:** the commentary restated the themes pages. On SYN-002(a) the reviewer had checked Aquinas's charity clause only against the research records. The author read the registered Super Ps. 24 page (hash-matched), where n. 4 reads *maxime per praeceptum caritatis*. The clause stands, now visibly Aquinas's. Synthesis-review 1 passed. |
| 6 | web-review 0 | study | **WEB-001:** in all four interpretations, five of the study's own links between Mass texts were stated as facts about a proper text, unmarked, beside marked neighbours. STU-015's repair had removed disclaimers and labels, and these five lost the one plain marker the rule still wants. Author-study 4 marked each once. It also cleared advisories WEB-002 (an unnumbered appendix reference), half of WEB-003 (the Offertory's *confído*) and WEB-004 (Bede's *igitur*). Study-review 4 passed. Because the study changed, the engine re-ran the dependent stages; each passed on its first try: derive-synthesis 2 and synthesis-review 2, derive-homily 1 and homily-review 1, build-artifacts 1 and artifact-gates 1, generate-web 1 and web-review 1. Derive-homily 1 also settled homily-review 0's advisories HOM-001 to HOM-005. Among them were Chrysostom's neighbours, where the text had said a household; Gregory's order; and a sung-Mass assumption untrue at a Low Mass. |
| 7 | install-publication 0 | driver | The driver's own session ended while the installer was running its publication check. The installer had written the release records, the catalog cell, the inventories and the inspection record; the source-family ledger refresh was interrupted. The driver resumed the same worker on the same packet. It was told that its edits were intact, that the browser-products `record` then running on the host belonged to another workspace, and that it should re-verify rather than assume. It re-verified every partial edit and the five review seals, reran the ledger refresh, and finished. One result was submitted. |

## Host interventions and events

| # | Stage | What |
| ---: | --- | --- |
| 0000 | resolve-context | The dispatch envelope. Every agent stage ran as a fresh Claude Code harness subagent (`claude-opus-5-5`) with no inherited conversation, at its packet's declared effort: authors `high`, reviews `xhigh`. Each worker received:<br>- its packet by exact path and SHA-256;<br>- a result path and a worker-owned scratch directory;<br>- the environment and provenance;<br>- the reservation of git and `advance` to the driver;<br>- no tool or shared-calendar edits;<br>- the independence terms closing the GPT leaf for this identity. |
| 0001-0004 | research 0-1, source-registration 0-1 | Host notes: products built in a clean worktree, working projections at the producers' default destination, sidecar evidence not tracked. Also the base-state commit `df614e24db`, and the defect classes runs 66-68's research reviews found. Iteration 1 named where each finding's repair belongs. |
| 0005-0008 | author-study 0-3 | The own-contribution-line reminder, the review results as read-only context, and the study defect classes of runs 66-68, including the fixed-formula overcorrection. Iterations 2 and 3 named the round count, and iteration 3 asked for a contained repair. |
| 0009-0010 | derive-synthesis 0-1 | The accepted reviews, and the standing advisories the compression must not inherit. For SYN-002(a), the author was to decide from the registered Super Ps. 24 page. |
| 0011 | derive-homily 0 | The accepted reviews, the settled corrections, and earlier Claude homily defect classes. |
| 0012, 0016 | generate-web 0-1 | The checkpoint commits, and the edition sources closed. |
| 0013-0015 | author-study 4, derive-synthesis 2, derive-homily 1 | The WEB-001 route and a contained repair at each stage. |
| 0017 | install-publication 0 | The installer brief:<br>- browser-products `record` and `check`, but not `prune`;<br>- serial, scoped binding refreshes;<br>- only the Claude cell of this Sunday's catalog row;<br>- the GPT entries preserved without opening the GPT leaf. |

The table omits three driver additions that the engine did not record as interventions:
- the constant host note given to every review (sealed products, the working-projection location, the base state, the host toolchain);
- the build-artifacts 0-1 host notes (the provenance check covering every authoring iteration, and the stale receipt to be left alone);
- the resumption message to install-publication 0 (cycle 7).

None of them, and none of the recorded interventions, supplied a content
conclusion. Each review finding reached its author through the packet's own
route.

The host carries a different Python Markdown. Every stage, web probe and gate
ran under a scratch virtualenv with the pinned Markdown 3.10.3 and PyYAML
6.0.3, the pinned pandoc 3.11 and `PYTHONDONTWRITEBYTECODE=1`.

## Sources the run settled

- **Latin.** The 1962 Missal governs, read on the page images (pp. 1-2,
  nos. 1-10).
- **English.** Lasance 1945 (pp. 103-106) for every element, read on page
  images; Douay-Rheims for other Scripture.
- **Registered by the run (`6284b8727e`):**
  - the chronology event, binding and orientation for the Lucan Gospel;
  - Augustine's *Enarrationes* on Psalm 84 (9, 15) and on Psalm 24, as verified passages;
  - the corrected Gregory Homily I loci, with six sections;
  - the fragment-loci rows the study cites.

## Findings that did not gate

Across fourteen cold reviews the run raised fifteen distinct blocking findings,
all repaired. Thirteen standing advisories remain, recorded in the leaf's
`evaluations/blocking-findings-v1.toml`:
- study: STU-017, STU-019, STU-021, STU-024, STU-025 and STU-026;
- synthesis: SYN-010 to SYN-014;
- homily: HOM-006;
- web: WEB-003.

STU-025 and STU-024 are worth a first revision:
- **STU-025:** the expansive study's `sections/40-hour-to-rise.tex` still calls Chrysostom's scene on Rom 13:12 "a household before dawn". His own words are about neighbours, and the concise study and homily now say so.
- **STU-024:** that file also keeps one unmarked link of the WEB-001 kind, at the Alleluia. The concise study keeps the same wording (SYN-013) so that it still matches the study.

Two more research rows record readings that the study later corrected; research records are sealed:
- **STU-017** and **STU-019** are rows in `research/interpretations.md` and `research/scope.md`.

## What this run leaves for the owner

| Item | Evidence | Why it is not done here |
| --- | --- | --- |
| No Latin-ledger row, passage record or collation covers the First Sunday of Advent's chants and Gospel (nos. 1-10). | resolve-context 0; research 0 | Shared ledger. |
| `formulary-loci.yaml` lacks the medieval commentators' loci for this Mass; there are no harvest alias groups for them. | research 0; source-registration 0-1 | Shared harvest records. |
| There is no Bernard author-standing row and no Leo work record. The NPNF I.7 and I.10 edition records name no translator, and no lawful Latin of Augustine's En. Ps. 24 is tracked. | source-registration 0-1 | Shared source registry. |
| The generated date notes print article titles with a closing quote at both ends, and refer the Psalm 84 chants to "As under Introit: Ps. 24". | generate-web 1; web-review 0-1 | Shared chronology generator. |
| `src/common/propers-format.tex` has no ℟ response sign. `tools/print-document` refuses an edition while a sibling entrypoint is absent. | author-study 0; derive-synthesis 1-2 | Shared typesetting and the print tool. |
| The `\ref{sec:date-location}` pattern that the three-documents profile licenses renders "(9)" or "()" in unnumbered study sections. | author-study 4; web-review 0 | `guidance/liturgy/propers-three-documents.md` and the packet. |
| A study rule that removes disclaimers and stock labels needs to say plainly that one marker per link of the study's own stays (STU-015, then WEB-001). Otherwise each repair invites the opposite defect. | study-review 1; web-review 0 | The proper-study packet and `guidance/editorial.md`. |
| `src/sources/chronology/profile-contract-rereview-manifest.tsv` was stale at the base (575 rows against 578 derived). | research 0 | Its owner regenerates it with `scripts/build_profile_contract_manifest.py`. |
| A driver session that ends mid-stage leaves no record the engine can see. A resumed worker's added message is not an intervention unless the driver records it. | install-publication 0 | `workflows/OPERATOR.md`. |

## After acceptance

Main gained ten commits during the run, all tooling and performance work. A
trial merge before acceptance was clean, and main's converter reproduced the
reviewed web conversion except for one line. Main changed shared chronology
scripts that are in the edition's source closure, so a merge commit moves the
study's derived "Last revised" stamp to the merge time. The branch is
reconciled with main after the archive commit, as run 68's was. The reviewed
conversion therefore stands for the commit the run accepted.
