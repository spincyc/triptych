# Every cycle the Claude Twenty-eighth Sunday production entered

Run `0b0f756d95e3ee20`, `proper-study` v9, provider `claude`, identity
`liturgy/roman-rite/postconciliar/roman-missal-third-edition-en-us-2011/propers/temporal/pc-s54-twenty-eighth-sunday-in-ordinary-time-year-a`,
date 2026-10-11, audience "adult parish assembly". Seeded at the
authorization commit `643a137fb`. Terminal disposition **ACCEPTED**, with no
escalations: 48 packets, 48 accepted results, 4 interventions. The engine's
own record is archived in the leaf under
`evaluations/proper-study-results/0b0f756d95e3ee20/`. This file is the
driver's account of why the run went round, which the run directory does not
state.

The GPT leaf for the same identity was published on 2026-10-06. This run is
an independent Claude production under its own edition tree: no stage opened
that leaf. Provider-neutral library records were used as library evidence
only, and their pages were read afresh.

Two driver sessions drove the run. The first, on Anthropic Claude Code,
seeded it and drove it through the dispatch of synthesis review 1, then ended
after that reviewer had written its result and before it was submitted. The
second, on Factory Droid, resumed from the run's own state, submitted that
result unchanged and drove the run to ACCEPTED. Interventions 0002 and 0003
record the handover and the new dispatch envelope.

## Where the rounds went

| Stage | Results | Failing rounds |
| --- | ---: | ---: |
| research-review | 2 | 1 |
| study-review | 3 | 2 |
| synthesis-review | 4 | 2 |
| homily-review | 3 | 1 |
| visual-review | 2 | 1 |
| web-review | 1 | 0 |
| every gate | one per round | 0 |

Seven cycles in all, which are the run's non-PASS transitions. No stage came
near its iteration budget; the study's STU-003 was the only finding raised
twice, and it cleared at the second repair. The visual cycle returned the run
to the concise author, and the engine then reran the homily and its review
before rebuilding, as an upstream repair requires.

## The cycles, in order

| # | Stage that found it | Owner | What it was |
| ---: | --- | --- | --- |
| 1 | research-review 0 | research | RES-001: the manifest named the United States English GIRM (2011, with the 2021 emendations) as the governing General Instruction, but no stage had read it; the chant-branch authorities rested on the Latin *Institutio generalis* of the 2002 Missal, and the context labelled the Entrance and Communion row with United States adaptations while listing only the Latin options. Research iteration 1 bound the US GIRM chapters II and VII and restated the chant branches; research review 1 passed with one advisory (RES-007). |
| 2 | study-review 0 | study | Five blocking findings. STU-001: interpretation openings credited "the witnesses of this interpretation" as a group with the whole synthesis. STU-002: "most of them name it charity" for the wedding garment, when two of seven do. STU-003: the study denied that any witness reads Mt 22:14 as a count, against Augustine, *Sermo* 90.4. STU-004: claims resting on Mt 22:11 without the shorter-form mark the opening promises. STU-005: a disclaimer of the compiler's intention and other Masses of the present Missal named. Author-study iteration 1 repaired all five. |
| 3 | study-review 1 | study | STU-003 again: the repair reported Augustine and Hilary but still said Gregory and Aquinas "do not weigh the numbers", against Gregory, Hom. 38.8 and 38.14, Aquinas's joining of the verse to Mt 7:14 on the Venice page, and Irenaeus IV.36.6. Author-study iteration 2 reported each; study review 2 passed with one advisory (STU-015) and accepted two research-record lags (STU-016, STU-017). |
| 4 | synthesis-review 0 | synthesis | SYN-001: the concise scope note disclosed Schuster's other Mass, which decision D11 keeps to the research record and the expansive appendix. SYN-002: Aquinas's ways of putting on Christ were compressed and his *et si unum deficiat, malum* attached to them rather than to his closing triad. The reviewer also accepted SYN-008, that the page reads *illa*. Derive-synthesis iteration 1 repaired both, and on SYN-002's instruction printed *illa*. |
| 5 | synthesis-review 1 | synthesis | SYN-009: the Venice page reads *Quae est ista vestis? Christus*, printed with the long-s and t ligature; *illa* was the OCR's reading of that ligature, which had reached the research records and synthesis review 0. The reviewer settled it on a high-resolution render against *est* and *vestis* on the same line, after intervention 0001 told it the stages disagreed. Derive-synthesis iteration 2, the first stage under the second driver, restored *ista* and withdrew the wrong statements in the production audit; synthesis review 2 passed. |
| 6 | homily-review 0 | homily | HOM-001: "The Fathers who explained this parable agree that the king is God the Father and that the son is Christ", a consensus claim the bounded sweep does not support. Derive-homily iteration 1 credits the identification to Jerome alone, read on the PL 26 col. 159 page image, and cleared the three advisories (HOM-002 to HOM-004); homily review 1 passed with one advisory (HOM-005), which the iteration-2 audit then cleared. |
| 7 | visual-review 0 | synthesis | VIS-001: the concise study's last page was full, so the shared rights colophon ended 5.4 pt from the paper edge, where a printer would clip it; VIS-002 (advisory) noted the descriptive line set in the metadata slot. Derive-synthesis iteration 3 shortened four References entries without dropping a locus, edition, page or year, moving the colophon to 47.2 pt above the edge, and moved the line to the subtitle field. Synthesis review 3, the engine's downstream derive-homily 2 (no homily source changed) and homily review 2 passed; build-artifacts 1 rebuilt byte-identical PDFs, and visual review 1 passed with one advisory (VIS-003). |

Each was a real defect that no mechanical gate could see. Cycle 5 is the one
to learn from: a misreading in a machine-read text entered the research
records, a reviewer that trusted them raised it as a finding, and a repair
obeying that finding introduced it into a reviewed document. It was caught
only because a later reviewer read the page image.

## Findings that did not gate

Across fifteen cold reviews the run raised 12 blocking findings (11 distinct
ids, STU-003 twice), 27 distinct advisories and 3 accepted findings. Those
that stand are in the leaf's `evaluations/blocking-findings-v1.toml`: 4
advisories, 2 accepted findings and 5 observations. The driver adds no
findings of its own. Three classes are worth a first revision:

- **The research records lag the reviewed studies (STU-016, STU-017, SYN-007,
  RES-007).** `research/scope.md` and `research/interpretations.md` still quote
  *illa* where the page reads *ista*, still summarize Mt 22:14 as the study did
  before STU-003 was repaired, omit Origen as Aquinas's source for *homo rex*,
  date the Fromage volume to 1900 rather than its 1909 second edition, attach
  Aquinas's *et si unum deficiat, malum* to the wrong list, and quote Gregory's
  *apertius atque securius* without its omitted *ergo*. No stage after research
  review may write research records; the three documents follow the page at
  each point.
- **SYN-008 is accepted on a false premise.** The engine holds it accepted
  from synthesis review 0. Its required result, to print *illa* when the
  expansive study is next revised, must not be acted on. It is not in the
  tracked ledger, because synthesis review rewrote its own entries when it
  passed, but it remains in the run's state.
- **Furniture (VIS-003; the colophon class).** The homily's note page still
  runs under the "Homily" head set for the spoken pages, as in the
  Twenty-fifth and Twenty-sixth Sunday homilies; and the shared colophon macro
  lets the rights notice descend to about 5 pt from the edge whenever a final
  page is full, which the installed Twenty-fifth Sunday study also shows at
  786.6 pt. Both reviewers who saw these asked for a mechanical check.

Observations outside this leaf's owners: the Davidic-attribution bindings do
not reach Vulgate Psalm 22 though its Clementine title reads *Psalmus David*;
the formulary-loci tool returns only Fromage and Blunt for `ot-28`, so
Schuster's and the Sicard and Honorius loci were found only by literal search;
the Nova Vulgata web states and the NABRE Psalms introduction are outside the
research seal; and the author-study 2 gate log stored with the run records its
provenance check exiting 1 on unexpanded placeholders, so the author's own
passing check is unevidenced, though the engine's study preflight 2 passed the
same check against this run.

## Host interventions and events

| # | Stage | What |
| ---: | --- | --- |
| 0000 | resolve-context | The first dispatch envelope: every agent stage ran as a fresh Claude Code harness subagent with no inherited conversation, at exactly the effort its packet's `EFFORT` line declares, through the harness's per-dispatch effort control. Each worker received its packet by exact path and SHA-256 and read it in full; the driver added only the result path, a worker-owned scratch directory, the checkout path, the model identity and effort for the generation record, the pinned-Markdown host note, and that the driver alone runs git and `advance`. |
| 0001 | synthesis-review 1 | An operator pointer beside the unchanged packet: the stages disagreed on one reading at Venice p. 282, the typeface's long-s and t ligature can resemble *ll* at low resolution, and the reading should be settled from a high-resolution render against *est* and *vestis* on the same line. No verdict was supplied. |
| 0002 | synthesis-review 1 | Driver handover. The first driver session ended after the synthesis review 1 worker had written its result and before it was submitted. The second session confirmed with `status` that the run awaited exactly that result, found it complete and well-formed, looked at the reviewer's retained page crops only to confirm the result was not the fragment of an interrupted turn, and submitted it unchanged. |
| 0003 | derive-synthesis 2 | The second dispatch envelope, from derive-synthesis 2 to the end. Each agent stage ran as one fresh Factory Droid general-purpose worker subagent with no inherited conversation, on the model the host labels `Opus 5.5`. Host deviation: Factory Droid exposes no exact per-dispatch effort control, only complexity tiers capped at the session's own level, so every remaining agent stage was dispatched at its highest tier, `heavy`, whether its packet declared `high` or `xhigh`. The driver's additions were otherwise those of 0000; the installer was additionally allowed the one `git add` its packet requires. |
| — | homily-review 1 | The derive-homily 1 author left its proof files in its own scratch directory, though its production-audit entry cites the run's `artifacts/derive-homily-0001/` for them. The driver copied them unchanged to that location, verified against the author's own `SHA256SUMS`, and told the reviewer so. Nothing was edited. |
| — | after ACCEPTED | The source records this production's research registered left the source-family migration ledger's `canonical_catalog_snapshot` stale, so `make check-sources` failed; it is not a member of the terminal gate, and the installer reported it rather than re-pinning. Following `guidance/sources.md`, the driver ran `tools/tpt source-family-migration refresh --audited-on 2026-10-08`, which refused on the stale pin, confirmed the ledger has no families whose membership needs review, and then ran it with `--accept-canonical-catalog`. Only `audited_on` and the two snapshots changed; the new catalog pin equals the value the installer computed, and `make check-sources` passes. |

**Model provenance.** The 23 results through synthesis review 1 were produced
by fresh Claude Code subagents running `claude-opus-5-5[1m]`, the first
driver's model, at their declared efforts: `high` for author and derive
stages, `xhigh` for reviews. The 25 results from derive-synthesis 2 onward
were produced by fresh Factory Droid worker subagents on the model the host
labels `Opus 5.5`, on Factory Droid CLI 0.236.0, all at the host's `heavy`
tier; that host does not expose the exact API model identifier, context
window, reasoning budget or server revision. The leaf's
`generation-metadata.tex` declares the two separately: two
`claude-opus-5-5[1m]` contributions (author-study 0 to 2; derive-synthesis 0
and 1) and one `Opus 5.5` contribution with `host-dispatch-tier=heavy`
(derive-synthesis 2 and 3; derive-homily 0 and 1). Build, web and install
stages changed no rendered source and declare nothing; derive-homily 2 changed
only the audit.

The host carries Python Markdown 3.11 and `requirements-public-alpha.txt`
pins 3.10.3, so every web, install and gate command ran under a scratch
virtual environment built from the two requirements files.

## What this run leaves for the owner

| Item | Evidence | Why it is not done here |
| --- | --- | --- |
| The research records lag the reviewed studies (STU-016, STU-017, SYN-007, RES-007), including the *illa* misreading | `evaluations/blocking-findings-v1.toml` | Only a research stage may write them, and reopening research reruns every document and review |
| SYN-008, accepted on a false premise, should be retired and never acted on | `results/synthesis-review-0001.json` observations | Accepted ids live in run state that no stage can withdraw |
| The Venice 1745 Aquinas OCR record warns of long s read as f but not of the st ligature read as *ll* or *li* | `results/synthesis-review-0001.json` observations | A shared source record outside this leaf |
| VIS-003, the homily note's running head, and a guard for the colophon on a full final page | `evaluations/blocking-findings-v1.toml` | Shared typesetting, and changing reviewed bytes needs a new run or an authorized revision |
| Anthony of Padua and Cyril of Alexandria have no row in `author-standing-v1.toml`; neither carries a reading | `make check-sources` informational line | A shared inventory outside this leaf |
| The formulary-loci tool under-covers `ot-28`, and the Davidic bindings miss Vulgate Psalm 22 | research-review observations | Shared tools and corpus outside this leaf |
