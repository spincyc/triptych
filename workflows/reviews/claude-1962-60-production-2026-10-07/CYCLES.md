# Every cycle the Claude Twentieth Sunday production entered

Run `9c1136f1f8d1241c`, `proper-study` v9, provider `claude`, identity
`liturgy/roman-rite/1962/propers/temporal/60-twentieth-after-pentecost`,
date 2026-10-11, audience "adult parish assembly". Seeded at the
authorization commit `1fa591a03`. Terminal disposition **ACCEPTED**, with no
escalations: 30 packets, 30 accepted results, 1 intervention. The engine's
own record is archived in the leaf under
`evaluations/proper-study-results/9c1136f1f8d1241c/`. This file is the
driver's account of why the run went round, which the run directory does not
state.

The GPT leaf for the same identity was published on 2026-10-05. This run is
an independent Claude production: no stage opened that leaf. The context and
research stages used provider-neutral library records, including those
registered on 2026-10-05, as library evidence only, and read their pages
afresh.

## Where the rounds went

| Stage | Results | Failing rounds |
| --- | ---: | ---: |
| research-review | 2 | 1 |
| study-review | 2 | 1 |
| synthesis-review | 2 | 1 |
| homily-review | 1 | 0 |
| visual-review | 1 | 0 |
| web-review | 1 | 0 |
| every gate | one per round | 0 |

Three cycles in all, which are the run's non-PASS transitions. Each review
stage that failed passed at its first re-review, so no stage came near its
iteration budget.

## The cycles, in order

| # | Stage that found it | Owner | What it was |
| ---: | --- | --- | --- |
| 1 | research-review 0 | research | RES-001: the Introit's verse, Ps 118:1, had no direct exegesis checked, though Augustine, Hilary and Bellarmine on it sat in tracked files the stage had opened, and "not needed for any reading" is no ground the profile admits. RES-002: scope said the Offertory's *tui* stood in no witness read, but the bound PL 9 col. 777 prints it in Hilary's psalm heading, with Migne's note *Infra abest tui*. RES-003: the interpretations set Bellarmine's literal reading of Ps 136:7–9 against Augustine, but at the bound locus Bellarmine also reads the little ones dashed on the rock that is Christ, so the disagreement was invented; Hilary on those verses was called unread though the whole tractate was bound. Research iteration 1 read four direct witnesses on Ps 118:1 (Augustine and Hilary on page images, Cassiodorus in CCSL 98, Bellarmine), recorded every psalm heading and lemma as it stands, read Hilary §§ 12–14, restated Bellarmine's three senses, and cleared the six advisories. |
| 2 | study-review 0 | study | STU-001: the first reading, "The Word That Heals from Afar", never mentioned the Alleluia, though the opening said every element has a place in each reading and the interpretations had assigned it one (Augustine on Ps 56:8). STU-002: the comparison claimed four grounds common to all three readings, three of which one reading lacked, and credited the second reading with a "family's homecoming" it never describes. Author-study iteration 1 gave the Alleluia its place from Augustine and Bellarmine on Ps 56:8 and Schuster, restated the common ground as what all three hold, and corrected the medieval-commentator clause of the scope appendix (STU-003). |
| 3 | synthesis-review 0 | synthesis | SYN-001: the concise scope note said Sicard and Durandus are cited only for the chants this formulary shares with the Mass their books expound; the three-document profile allows that mention only in the expansive study. Derive-synthesis iteration 1 restated the clause without naming another Mass and cleared the four advisories (SYN-002 to SYN-005). |

Each was a real defect in the work that no mechanical gate could see, and
each was caught before the next document was written, so no downstream
document reran.

## Findings that did not gate

Across nine cold reviews the run raised 6 blocking findings and 25
advisories; the 14 that stand are in the leaf's
`evaluations/blocking-findings-v1.toml`. The driver adds no findings of its
own. Three classes are worth a first revision:

- **The research brief overstates the readings' common ground (STU-006).**
  `research/interpretations.md` §4.1 still states the shared ground STU-002
  removed from the study, contradicting its own §§2.1 and 2.5; RES-005 (a
  table row settling Gregory's *per spiritum* as the Holy Spirit), RES-010
  (Bellarmine's little ones summarised as vices, where in his spiritual senses
  they are people) and RES-011 and RES-012 (Berno's dependence on the
  wedding-feast Gospel left unbounded; Hilary's Ps 56 heading not recorded for
  the Alleluia) are of the same kind. No stage after research-review may write
  research records; the three documents follow the reviewed reading at each
  point. The Seventeenth through Nineteenth Sunday runs ended with the same
  class.
- **Homily precision (HOM-001 to HOM-005).** The words of Jn 4:49 are heard as
  the father's first request, before the rebuke of 4:48; the Communion's own
  last line is dropped; "What we see is bread and wine" should speak of
  appearances (Trent, sess. XIII); "the last prayer of this Mass will answer
  the first" ignores the Maternity Postcommunion at a low or conventual Mass;
  and the Introit's "for we have sinned", spoken after addressing the
  bereaved, wants a clause keeping it from sounding like a verdict on their
  loss. HOM-003 and HOM-005 are the ones a preacher using this text should
  attend to first.
- **Typography (VIS-001, VIS-002; STU-005).** "St" is never tied to the
  saint's name, so names split across lines in all three documents; one
  unspaced ellipsis in the homily; and three editorial self-labels the STU-001
  repair instruction invited.

Observations outside this leaf's owners: the chronology corpus records the
Catholic Encyclopedia's "long after the Exile" date for the Prayer of
Azarias as the traditional answer, though the same article reports that
nearly all Catholic writers date it to Daniel's time, so page 2 cannot name
that alternative (research reviews 0 and 1); the right-hand running head names
the last section that starts on a page, so a page that opens mid-section
carries the next section's title (study review 1, synthesis reviews 0 and 1,
visual review); the generated Offertory date cell prints "printed-page
verification still pending", a review-state phrase no review stage covers
(synthesis review 0); and on a phone the map and comparison tables scroll
inside their frames, as the installed Nineteenth Sunday edition does (web
review).

## Host interventions and events

| # | Stage | What |
| ---: | --- | --- |
| 0000 | research | The dispatch envelope: every agent stage ran as a fresh Claude Code harness subagent with no inherited conversation, at exactly the effort its packet's `EFFORT` line declares, through the harness's per-dispatch effort control. Each worker received its packet by exact path and SHA-256 and read it in full; the driver added only the result path, a worker-owned scratch directory, the checkout path, the model identity and effort for the generation record, the pinned-Markdown host note, and that the driver alone runs git and `advance`. |
| — | visual-review 0 | The reviewer's turn was cut off by an API rate-limit error (HTTP 429, account session limit) after it had confirmed all 31 study pages and before it wrote a result. Once the limit reset, the driver resumed the same worker, with its own evidence and the unchanged packet; no second reviewer was dispatched and the engine was not advanced on the error. The resumed review read every page of all three PDFs and passed. The run was terminal before this could be recorded as an engine intervention, so it is recorded here. |

**Model provenance.** Every agent stage ran as `claude-opus-5-5[1m]`, the
driver's model, at its declared effort: `high` for the author, build, web and
install stages, `xhigh` for the six reviews. This closes the host deviation
the Nineteenth Sunday run recorded, when no per-dispatch effort control was
available. The leaf's `generation-metadata.tex` declares that model and
effort for each author and derive stage.

The host carries Python Markdown 3.11 and `requirements-public-alpha.txt`
pins 3.10.3, so every web, install and gate command ran under a scratch
virtual environment built from the two requirements files.

## What this run leaves for the owner

| Item | Evidence | Why it is not done here |
| --- | --- | --- |
| The research brief lags the reviewed study (STU-006, RES-005, RES-010 to RES-012) | `evaluations/blocking-findings-v1.toml` | Only a research stage may write them, and reopening research reruns every document and review |
| The homily advisories HOM-001 to HOM-005 and the typography advisories | `evaluations/blocking-findings-v1.toml` | Changing reviewed bytes needs a new run or an authorized revision |
| Anthony of Padua and Cyril of Alexandria have no row in `author-standing-v1.toml`; neither carries a reading | `make check-sources` informational line | A shared inventory outside this leaf |
| The Latin publication ledger has no rows for the Introit and six scriptural chants, its Maternity rows cite a printing the 1862 record calls a misattribution, and the English translation list still marks bound orations unavailable | research 0 result | Shared registries outside this leaf |
| The commentary index lists no entry for this Mass and omits Gregory's Homily 28 under John 4 | research 0 result | The neutral commentary index, not this leaf |
| The chronology corpus's traditional answer for the Prayer of Azarias | research-review observations | The neutral chronology corpus and profile |
| `tools/check-generation-metadata --pdf` falls back to provider `gpt` unless `--provider claude` is passed | derive-synthesis 1 result | A shared tool; the leaf's checks pass with the flag |
