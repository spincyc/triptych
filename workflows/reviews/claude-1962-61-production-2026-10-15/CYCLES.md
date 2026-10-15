# Every cycle the Claude Twenty-first Sunday production entered

Run `a8bcc37ea3420a07`, `proper-study` v11, provider `claude`, identity
`liturgy/roman-rite/1962/propers/temporal/61-twenty-first-after-pentecost`,
date 2026-10-18, audience "adult parish assembly". Seeded at the
authorization commit `cc2e96832`. Terminal disposition **ACCEPTED**, with no
escalations: 59 packets, 59 accepted results, 2 interventions. The engine's
own record is archived in the leaf under
`evaluations/proper-study-results/a8bcc37ea3420a07/`, written by
`tools/proper-study-run-archive`. This file is the driver's account of why
the run went round, which the run directory does not state.

The GPT leaf for the same identity was published before this run was seeded.
This run is an independent Claude production, and no stage borrowed from that
leaf. Two contacts with it are recorded under "Host interventions and events"
below.

## Where the rounds went

| Stage | Results | Failing rounds |
| --- | ---: | ---: |
| research-review | 4 | 2 |
| study-review | 4 | 2 |
| synthesis-review | 3 | 0 |
| homily-review | 4 | 1 |
| artifact-gates | 3 | 1 |
| visual-review | 2 | 1 |
| web-review | 1 | 0 |
| every other gate | one per round | 0 |

There were seven cycles, which are the run's non-PASS transitions. Six were
real defects that cold reviewers found. The seventh was the driver's own
fault: a stale research seal, which made the run pass through research, every
document stage and every review a second time with no content change. The
visual-review cycle then routed through the concise study, the homily and the
build once more. That is why 59 results stand where a clean run has about 30.

## The cycles, in order

| # | Stage that found it | Owner | What it was |
| ---: | --- | --- | --- |
| 1 | research-review 0 | research | RES-001: the scope record reported Bellarmine as doubting the Mosaic title of Ps 89 beside Augustine. In fact his manuscript Preface II calls Moses' authorship of the titled psalms "not unlikely", and Preface I calls it acceptable. RES-002: reading 3's title, question and page-1 note rested on "Quot sunt dies servi tui?" (Ps 118:84a) and Ps 89's "numerare dies", which the Communion does not sing. Neither was labelled as unsung context. Research iteration 1 reported both of Bellarmine's judgments against Augustine, made "unsung context" a labelled rule, and re-founded reading 3 on the sung "quando facies … iudicium". It also read Theodoret (PG 80), Cassiodorus (through Corpus Corporum) and Alphonsus's Sunday sermon for advisories RES-003 to RES-007. |
| 2 | research-review 1 | research | RES-008: the record quoted "Judicium non hic poscitur extremum … sed virtus qua diabolus … conteratur" and "Salutaris Jesus" as Hilary's words. On the PL 9 scan (col. 573C) they are the Maurist editors' italic paragraph summaries, and Hilary's own "now, not the last judgment" rests on the unsung v. 84a. RES-009: Theodoret, added at iteration 1, stands censured in `author-standing-v1.toml` (Constantinople II, 553). The profile allows such a writer only structural and contextual work, but the record made him a direct witness and "the Greek tradition". Research iteration 2 quoted only Hilary's own text, labelled his dependence on v. 84a, and recorded the censure. It cut Theodoret to context and read the PG 27 expositions printed under Athanasius's name as contributing witnesses that carry no reading. |
| 3 | study-review 0 | study | STU-001: the Gospel row of the date appendix said the NABRE Matthew introduction gives no place of writing. It offers Antioch as a plausible suggestion, as the repository's own passage record says, and the concise page 2 draws its place phrases from that appendix. Author-study iteration 1 repaired the row and the Matthew note, and cleared advisories STU-002 to STU-010. Among them, two quotations in reading 2 had been given to the wrong speaker, and the comparison had said Aquinas serves only two readings. |
| 4 | study-review 1 | study | STU-011: two sentences, one of them rewritten in iteration 1, claimed that Hilary and Augustine "differ in the time, not in the object" of the Communion's plea, and that they "do not differ about the persecutors". Hilary asks for present power against the devil and his ministers. Augustine hears the martyrs' cry for the last judgment on the Church's persecutors. Author-study iteration 2 let each witness keep his own answer in sections 20, 40 and 50. |
| 5 | homily-review 0 | homily | HOM-001: the homily never carried the king's pardon through Christ's death and Resurrection to Baptism and the Eucharist. The Homiletic Directory movement that the three-document contract names requires it. "Baptism" first appeared unprepared, the only Eucharistic sentence was a moral warning, and the Secret's own bridge was left to the studies. Derive-homily iteration 1 proclaimed the debt paid on the Cross and received at the font (Augustine, Sermon 83.7), prepared Communion from the Secret and Postcommunion, and cut quotation from 33 spans to 24 (HOM-005). |
| 6 | artifact-gates 0 | research (seal) | STALE-RESEARCH-REVIEW, caused by the driver. While the homily was being written, the driver committed `b9786e912`, which registered `tools/proper-study-run-archive`. That changed the GROUPS and REACHES tables in `scripts/_tooling.py`. The chronology computation compiles that module, so the `proper-study-v4` research seal lists it among `chronology_computation_inputs`, and its digest moved. Nothing in the leaf changed. The linear pipeline then reran research 3, research-review 3, author-study 3, study-review 3, derive-synthesis 1, synthesis-review 1, derive-homily 2, homily-review 2 and build-artifacts 1. Every author confirmed its sealed inputs unchanged and made no content edit, every reviewer re-verified and passed, and the PDFs came out byte-identical. Intervention 0001 records the cause. |
| 7 | visual-review 0 | synthesis | VIS-001: on concise page 2 the rows of the psalm group ran together. Multi-line cells left no space between rows, so a reader could not pair the Communion's passages with their dates at a glance. The generated row ending `\\[.25em]` adds nothing when a cell wraps. Derive-synthesis iteration 2 put `\addlinespace` between neighbouring orientation rows and capitalized the concise title line (VIS-004). The pipeline then routed synthesis-review 2, derive-homily 3, homily-review 3 and build-artifacts 2. Only the shared generation timestamp moved in the study and the homily. |

Cycles 1 to 5 and 7 were real defects that no mechanical gate could see. Cycle
6 cost nine agent stages and about two and a half hours for one changed
digest.

## Findings that did not gate

Across 18 cold reviews the run raised 8 blocking findings and about 40
advisories, and the artifact gate raised one refusal. What still stands is in
the leaf's `evaluations/blocking-findings-v1.toml`: 19 advisories, 1 accepted
finding and 7 observations. The driver adds no findings of its own. Three
classes are worth a first revision:

- **The research brief lags the reviewed study (RES-012 to RES-015).** The
  scope record still lists Bellarmine "for Moses" and against Augustine on
  Ps 89. Both of his prefaces and his own Ps 89 exposition prefer David, with
  Augustine. `interpretations.md` §4.1 still limits Aquinas to two readings.
  It also describes reading 3 inconsistently, and the St Luke collation table
  misses one comma and one accent. No stage after research-review may write
  research records, and the three documents state these points correctly.
  The Seventeenth through Twentieth Sunday runs ended with the same class.
- **Prose precision.** STU-005: the Hilary–Augustine difference on the
  Communion is told three times. STU-013: "the Fathers" includes Bellarmine
  and Cassiodorus. STU-015 (accepted): an "if then" in Augustine lost its
  "then". SYN-001 to SYN-006 cover a misread join, a column range, an
  unmarked unsung verse, Fromage unidentified, one self-referring sentence,
  and Rupert credited with an editor's "(Rom. ix)". The study and
  `scope.md` carry the same clause. HOM-006 to HOM-008: Augustine's "both
  men", Chrysostom named first by surname alone, and "He is given the whole
  debt" where "forgiven" is meant. HOM-008 is the one a preacher using this
  text should attend to first.
- **Typography (VIS-002, VIS-003, VIS-005).** The closing quotation marks are
  reversed on study pp. 11, 14 and 17. The study's appendix table (p. 33)
  has the same row-spacing defect that VIS-001 repaired in the concise. The
  generated passage labels mix "Ps" with "Psalm" and hyphens with en dashes,
  and let "c." break from "A.D.".

## Host interventions and events

| # | Stage | What |
| ---: | --- | --- |
| 0000 | resolve-context | The dispatch envelope. Every agent stage ran as a fresh Claude Code harness subagent with no inherited conversation, at exactly the effort its packet's `EFFORT` line declares, through the harness's per-dispatch effort control. Each worker received its packet by exact path and SHA-256 and read it in full. The driver added only the result path, a worker-owned scratch directory, the checkout path, the model identity and effort for the generation record, the pinned-Markdown host note with the scratch virtualenv's path, and that the driver alone runs git and `advance`. |
| 0001 | research 3 | The cause of cycle 6, as above. From research 3 through build-artifacts 2, each brief carried that fact as one to be verified rather than trusted, and told authors to make no edit their packet did not call for. Every worker verified it independently against the seals. |
| — | research 0 | A repository-wide grep by the research worker printed one line of the GPT leaf's `source-bindings.toml`. Nothing was used, and `scope.md` says so. |
| — | visual-review 0 | The visual reviewer's repair suggestion for VIS-001 noted that "the sibling GPT leaf already does it". The reviewer had opened that leaf's typesetting as a layout precedent. The repair is the standard booktabs `\addlinespace`, and no content passed. From then on, the visual-review 1 and derive-synthesis 2 briefs told the worker not to open that leaf. |
| — | install-publication 0 | The packet requires the installed web Markdown to be staged before the publication gate. The brief had reserved git to the driver, so the worker left it unstaged. The driver checked its bytes against the reviewed conversion (`9681daa5…`) and staged it before running `publication-gates`. |

**Model provenance.** Every agent stage ran as `claude-opus-5-5[1m]`, the
driver's model, at its declared effort: `high` for the author, build, web and
install stages, `xhigh` for the eighteen reviews. The leaf's
`generation-metadata.tex` declares that model and effort for each author and
derive stage. One further subagent, outside the workflow, built
`tools/proper-study-run-archive` (commit `b9786e912`) as `claude-opus-5-5[1m]`
at `high`. It touched no leaf file.

The host carries Python Markdown 3.11, and `requirements-public-alpha.txt`
pins 3.10.3. Every web, probe, install and gate command therefore ran under a
scratch virtual environment built from the two requirements files. Before
the run, ten installed PDFs that `main` had published since this checkout's
last sync were restored from the live site's `SHA256SUMS` and hash-checked,
so that `check-sources` could see the published catalog.

## What this run leaves for the owner

| Item | Evidence | Why it is not done here |
| --- | --- | --- |
| The tracked Bellarmine *Commentary on the Psalms* text claims to be wholly John O'Sullivan's public-domain 1866 translation. Its own line 53 says the manuscript Preface II "is that of Michael J. Miller", a modern translation. | `src/sources/works/robert-bellarmine/commentary-on-the-book-of-psalms/editions/2026-09-05-osullivan-ecatholic2000/artifacts/historical-text-357551e1/` (`artifact.toml` `rights_status`, `text.txt` line 53); study reviews 0 to 3 | A rights decision for the source-library owner and the maintainer. This leaf paraphrases both prefaces, and only `research/scope.md` quotes about two lines of Preface II. |
| Any tool registration during a live run stales every live `proper-study` research seal, because the v4 seal covers `scripts/_tooling.py` | Cycle 6; intervention 0001; research-review 3 observation | A workflow-seal design question. Narrowing the seal is a workflow version change. |
| The chronology generator's row ending `\\[.25em]` (`scripts/_proper_chronology.py`, about line 2013) leaves wrapped rows unseparated. Its passage labels are inconsistent. | VIS-001, VIS-003, VIS-005 | A shared generator. The concise was repaired per leaf. |
| The chronology preflight accepts `\textit` in a place phrase that the web converter's payload audit then refuses | author-study 0 production audit | Two shared tools that disagree. The author removed the italics. |
| RGMR 453's Mission Sunday prayer (*pro Fidei propagatione*, the penultimate Sunday of October) has no rule in `calendar-rubrics` or `rubrics.yaml`, so their computed prayer lists for 18 October are incomplete | resolve-context 0 | Shared calendar data. |
| A routed repair's packet does not forward the routing stage's standing advisories from other stages. SYN-006 never reached derive-synthesis 2. | synthesis-review 2 observation | Engine behaviour. |
| Alphonsus Liguori and Athanasius have no row in `author-standing-v1.toml`. The PL 9 edition record carries no warning that the Maurist italic summaries are not Hilary's words. | research 1 and 2; `scope.md` §10 | Shared inventories. |
| The Latin ledger's St Luke rows cite 1922 Mame pages aligned with other formularies. There are no rows for the Introit, the five scriptural chants or the mission prayers. No passage record covers the 1861 Cummiskey English of the Introit, Offertory and Communion, its St Luke English, or the Lasance *pro Fidei propagatione* English. | resolve-context 0; homily reviews | Shared registries. |
| Fresh downloads of the Catholic Encyclopedia articles behind the chronology no longer match their registered hashes. The chronology corpus has no attribution for Ps 89 (Moses) or Job, and the Esther composition date does not separate the Greek additions. | research 0; research-review 0 observation | The neutral chronology corpus. |
| At phone width, the at-a-glance and comparison tables scroll inside their frames, as the installed editions do | web-review 0 observation | The site stylesheet. |
