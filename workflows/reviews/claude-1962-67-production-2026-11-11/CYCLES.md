# Every cycle the Claude resumed Sixth Sunday production entered

Run `decbd44ee5bcce3b`, `proper-study` v19, provider `claude`, identity
`liturgy/roman-rite/1962/propers/temporal/67-resumed-sixth-after-epiphany`,
date 2026-11-15, audience "adult parish assembly". Seeded at `99791e370c`,
after the authorization commit `53abdfa479` and one pre-seed tool fix.
Terminal disposition **ACCEPTED**, with no escalations: 53 packets, 53
submitted results, 16 recorded interventions. One further worker result, a
BLOCKED from the first installer at install-publication 1, was held back and
never submitted (cycle 9). The engine's own record is
archived in the leaf under
`evaluations/proper-study-results/decbd44ee5bcce3b/`, written by
`tools/proper-study-run-archive`. This file is the driver's account of why the
run went round, which the run directory does not state.

Sunday, 15 November 2026 is the Sixth Sunday after the Epiphany resumed after
Pentecost (II class, green), permanent identity `67`. St Albert the Great
(III class) is not commemorated at any Mass under RG 111 b. The Mass is
printed on pp. 421-422 of the 1962 Missal, nos. 1759-1768. Its five chants
are the Twenty-third Sunday's (RGMR 298), and its orations and lessons are
those of the Sixth Sunday after the Epiphany. A parallel session was producing
the GPT edition of the same identity in another clone. Under the production
plan this is an independent Claude production. The briefs closed the GPT
leaf, its release records and its workflow records to every stage, even as a
layout precedent.

## Before seeding

| Commit | What |
| --- | --- |
| `53abdfa479` | The production-plan authorization line and the paragraph that bounds this production to identity `67`. |
| `16a02b41c8` | Revision stamps during staged authoring. The v19 study preflight's web probe asked for a revision stamp of the expansive edition while `synthesis.tex` and `homily.tex` did not yet exist, and the manifest loader required every structure path to exist. It stopped every author-study preflight. `load_manifest` now takes the entrypoint being stamped and checks only that edition's paths. The change is the parallel GPT session's `1b68bd930e`, applied unchanged, so the two branches carry one fix. |
| `99791e370c` | Browser products re-recorded and the bindings that fix staled refreshed, so that the run sealed a clean base. |

## Where the rounds went

| Stage | Results | Failing rounds |
| --- | ---: | ---: |
| research | 3 | 2 required changes |
| research-review | 3 | 2 |
| author-study | 4 | 3 required changes |
| study-review | 4 | 3 |
| derive-synthesis | 3 | 2 required changes |
| synthesis-review | 3 | 2 |
| derive-homily | 2 | 1 required change |
| homily-review | 2 | 1 |
| install-publication | 3 | 0 |
| generate-web | 2 | 0 |
| web-review | 2 | 0 |
| publication-gates | 3 | 2 |
| every other stage | one per round | 0 |

There were ten cycles. The first eight were real defects that cold reviewers
found in the content. The study review passed in round four, the last the
workflow allows. The last two came from the publication gate and touched no
content. Its runner could not finish two checks that pass (cycle 9). The
driver's fix to that runner then staled the web review's seal (cycle 10). No
research, author or content-review seal went stale. The driver committed the
source registrations and the leaf after the artifact gates. Its one other
commit inside a seal was the runner fix `306cb81ea4`, and it checked first
that the fix staled only the web review.

## The cycles, in order

| # | Stage that found it | Owner | What it was |
| ---: | --- | --- | --- |
| 1 | research-review 0 | research | **RES-001:** the records bound Ambrose, *Exp. in Luc.* VII.176-190, but they turned the readings he reports (the leaven as Christ, which *plerique putant*; the three measures as Law, Prophets and Gospel) into his own. They also missed his own preference at VII.190-191: the leaven is the Church's spiritual teaching, which leavens body, soul and spirit. **RES-002:** the research said the Communion's edge words came from Mk 11:23, a derivation it had itself recorded as unresolved. The antiphon's close does not even match v. 23. Research 1 read VII.176-194 and stated only the textual fact, that in Mark the appointed verse follows the mountain-moving saying. |
| 2 | research-review 1 | research | **RES-006:** two passages credited to Rabanus, *In Mt.* IV, "in his own name" (the mustard seed as the buried and risen Lord; the three measures as the thirty-, sixty- and hundredfold, with charity hidden until it leavens the whole mind) are Bede's, *In Luc.* IV, word for word. Research 2 re-attributed them and checked every attribution to a compiler, or to a writer who reports others, against its locus (scope section 13.4). That check corrected the rows for Bede, Jerome, Ambrose, Aquinas and Durandus and added Sicard, *Mitrale* VIII.23. |
| 3 | study-review 0 | study | **STU-001:** the study wrote its own links between texts as what a prayer asks or what a Father said (Hilary's reading "answers the difficulty about herb and tree"). **STU-002:** where it joined two texts, the body narrated the joining and its reason instead of stating the claim. |
| 4 | study-review 1 | study | **STU-007:** Jerome, *In Hier.* V (PL 24 col. 893), was quoted correctly (*ut quod promissum est, mereantur accipere*) and restated elsewhere as something he does not say. The sealed research's gloss "prayer commanded" was the source. **STU-008:** Aquinas, *Super I Thess.* c. 1 l. 1, on *in virtute* was cut to his opening contrast, and the study drew a conclusion that his full sentence does not carry. **STU-009:** paragraphs ended on a maxim or a paradox, or stated the study's own link as a fact about a text. |
| 5 | study-review 2 | study | **STU-016:** the scope appendix said the record held no date for the telling of the parables. The generated Scriptural Date and Location page dates it to A.D. 27, after Maas, so the sentence contradicted the page beside it. The repair removed the sentence. The authors write no date prose about the generated page. |
| 6 | synthesis-review 0 | synthesis | **SYN-001:** three compressions credited a Father with more than his locus says, among them Chrysostom on Ps 129:1 with the study's own leaven comparison. **SYN-002:** a Chrysostom sentence was cited to Hom. 2 on 1 Thessalonians; it is in Hom. 1. **SYN-003:** References named Bede on Mk 4:30-32, which the concise study never uses. |
| 7 | synthesis-review 1 | synthesis | **SYN-009:** compression dropped a qualifier. "The medieval commentators on the Mass who expound these four chants" became a claim about the commentators generally, but only Rupert, Sicard and Durandus were read. |
| 8 | homily-review 0 | homily | **HOM-001:** three sentences in the exegetical middle addressed the source record rather than the listener. One gave Augustine's variant count of heart, soul and mind, which the argument never uses. One restated Bede's method as a closer. One was an inference marker that the guidance calls "a footnote spoken aloud". |
| 9 | publication-gates 0 | publication (tooling) | **GATE-RELEASE-BINDINGS** and **GATE-DOCUMENT-CATALOGUE** timed out. Both commands exit 0 but take longer than the runner's fixed 300 s budget: `make check-release-bindings` about 786 s alone, because `release-bindings status` traces one chronology computation per publication, and the catalogue check about 316 s. The runner killed only the shell, so the orphaned `release-bindings status` kept running beside the later checks until the driver killed it. The first fresh installer timed both commands on a quiet host and returned BLOCKED. The driver did not submit that result and committed the runner fix `306cb81ea4` (see below). A second fresh installer re-recorded the three browser-product families whose generator code includes the engine, refreshed the two affected bindings (`6816627004`), and passed. |
| 10 | publication-gates 1 | publication | **STALE-WEB-REVIEW**, caused by `306cb81ea4` alone. The render digest of the web review's identity covers every `scripts/*.py`, so the engine change moved it; the content and evidence digests did not change. The gate routed to generate-web, whose conversion was byte-identical (`293ceca2…9410`, same stamp), and then to a fresh cold web review, which passed. Install-publication 2 then brought the leaf's records up to that review (`2eee3c95a7`): `web-edition.toml` names web review 1 as the inspection, the engine's ledger records it, and the production review explains the return. The inventory, the browser products and the two diverged bindings were refreshed. Publication gates 2 ran all five checks, each exiting 0, and the run was ACCEPTED. |

## Host interventions and events

| # | Stage | What |
| ---: | --- | --- |
| 0000 | resolve-context | The dispatch envelope. Every agent stage ran as a fresh Claude Code harness subagent (`claude-opus-5-5`) with no inherited conversation, at its packet's declared effort through the harness's per-dispatch effort control: authors `high`, reviews `xhigh`. Each worker received its packet by exact path and SHA-256. The driver added the result path, a worker-owned scratch directory, the environment, provenance, the reservation of git and `advance` to the driver, no tool or shared-calendar edits, and the independence terms. |
| 0001 | source-registration 0 | Each worker's scratch directory is closed to the others. The registration brief opened the research worker's download receipts read-only and required every hash to be re-verified. |
| 0002 | research 2 | Both research reviews had found one defect class: credit "in his own name" for words an author only reports or copies. The brief named the class and asked for every compiler attribution to be checked against its locus. |
| 0003-0006 | author-study 0-3 | The briefs named the accepted research review's advisories, the register rules on which run 66's study reviews failed, and run 66's overcorrection between rounds. They passed on the reviews' unroutable observations: the sealed research glosses of Jerome and Aquinas, and Douay-Rheims quoted at verses without a binding. The last brief noted that review four was the final allowed round. |
| 0007-0009 | derive-synthesis 0-2 | The briefs listed the research glosses that the study reviews had found wrong, with the rule that the quoted source governs, and named the study advisories as context. The repairs were to stay contained: no new source, no new locus, and group claims limited to the authors actually read. |
| 0010 | derive-homily 0 | The same research-gloss list, the study and synthesis review results as context, and the defect classes found by earlier homily and study reviews. |
| 0011 | install-publication 0 | The edition sources were committed and closed to the installer. Only this provider's shared entries were to be touched, because the GPT production was in another clone. A harness permission refusal was to be returned, not worked around. |
| 0012 | install-publication 1 | The first installer brief: both gate findings were timeouts, and the timed-out command's child had run orphaned for about 12.5 minutes. The installer was to time each command alone and change nothing if nothing needed repair. |
| 0013 | install-publication 1 | The second installer on the same packet. The driver held back the first worker's BLOCKED result and committed `306cb81ea4` to shared tooling: gate commands get 1800 s, and a timeout kills the whole process group. The driver checked first that the change stales only the web review, by computing the engine's stale-review set with and without it. |
| 0014 | generate-web 1 | Why the web review was stale, the current commits, and closed edition sources. |
| 0015 | install-publication 2 | The identity was already installed (`ec3acfca58`, `6816627004`). The brief gave the reason for the return and asked the installer to bring the records up to web review 1, recreating nothing current. It set the order: leaf records, inventory and ledger, then the browser-product record and scoped binding refreshes, one at a time. |
| — | publication-gates 0 | Mid-run tooling commit `306cb81ea4`. The research and author seals do not cover `scripts/_workflow.py`, but the web review's render digest does. |
| — | artifact-gates 0 | The driver committed the source registrations (`e6db2956f5`) and the leaf (`5704d9e52d`) before `generate-web`, so the reader carries the stamp `2026-11-11T20:40:01Z`. |
| — | install-publication 0 | The installer re-recorded browser products (13 products, 27,924 files, 12 families rekeyed) and adopted bindings for exactly 49 attributable paths. The driver committed the installation (`ec3acfca58`) before the terminal gate. |
| — | install-publication 1 | The second installer re-recorded the three browser-product families whose generator code includes the engine and refreshed the two bindings the runner fix moved. The driver committed them as `6816627004`. |
| — | install-publication 2 | The installer's leaf records, inventory, browser products and two bindings were committed as `2eee3c95a7` before the terminal gate. |

None of the interventions supplied a content conclusion. Each review finding
reached its author through the packet's own route.

The host carries Python Markdown 3.11 and the repository pins 3.10.3. Every
stage, web probe and gate ran under a scratch virtualenv built from the two
requirements files, with `PYTHONDONTWRITEBYTECODE=1`.

## Sources the run settled

- **Latin.** The 1962 Missal governs, read on the page images of the resumed
  printing (pp. 421-422, nos. 1759-1768). Every word also stands in Pustet
  1862, read on page images, so the publication mode is `complete`. The
  Collect, Secret and Postcommunion end with the short *Per Dominum.* of the
  resumed printing. The resumed printing cites the Epistle as *1 Thess. 1,
  1-20*, a misprint: the text runs 1:2-10, and the Epiphany-season printing
  (no. 338) reads *2-10*.
- **English.** Douay-Rheims for Scripture, with the Missal's Latin and a
  description where the Douay's verse is not the Missal's form. For the
  orations and chants, Lasance 1945.
- **Witnesses added by review.** Ambrose's own reading at *Exp. in Luc.*
  VII.190-191; Bede, *In Luc.* IV, as the source of the leaven passages that
  Rabanus copies; Sicard, *Mitrale* VIII.23; Jerome to the end of his
  sentences (PL 26 col. 93; PL 24 col. 894); the Matthean parallel of the
  Communion (Mt 21:21-22) in Chrysostom, Jerome and Hilary. `e6db2956f5`
  registered Augustine's *Quaestiones Euangeliorum* I.11 and I.12 as
  verified passages, with their Mt 13:31-33 fragment loci. It also
  registered a new delivery of the Catholic Encyclopedia's Thessalonians page,
  and the FSSP and ICRSP France Ordos for the date (restricted, metadata
  only).

## Findings that did not gate

Across fourteen cold reviews the run raised 14 blocking findings, all
repaired. Eleven standing advisories remain, recorded in the leaf's
`evaluations/blocking-findings-v1.toml`:

- research: RES-009 to RES-011;
- study: STU-022 to STU-024;
- synthesis: SYN-008 and SYN-011;
- homily: HOM-004 and HOM-005;
- web: WEB-001.

SYN-008 is the one worth a first revision. Three synthesis reviews raised it
and none made it blocking. The expansive study's run of Chrysostom citations
in `sections/20-crushed-seed.tex` (lines 175-191) carries the same Hom. 1/2
uncertainty that SYN-002 fixed in the concise study. WEB-001 asks for a
rewording in the same section. The concise study also has one doctrinal
sentence on the sacrifice of the Mass with no locus, an observation that
reached the homily brief as context.

## What this run leaves for the owner

| Item | Evidence | Why it is not done here |
| --- | --- | --- |
| The resumed printing's Epistle citation *1 Thess. 1, 1-20* (p. 421, PDF 502) is a misprint for 1:2-10. `propers.yaml` gives the Collect and Postcommunion the long Epiphany-season ending, where the resumed printing has *Per Dominum.* | resolve-context 0; research 0 | Shared calendar and propers records. |
| The Latin-provenance ledger has no rows for nos. 1759-1768. It does not record that the chants are shared with the Twenty-third Sunday and the lessons with the Sixth after the Epiphany. | resolve-context 0 | Shared ledger. |
| `formulary-loci.yaml` lacks Rupert XII.23, Durandus VI.140 and VI.23, and Sicard VIII.23-25 for this Mass. `discover` does not link Aquinas on 1 Thessalonians to 1 Thess 1. | research 0-2; source-registration 0-2 | Shared harvest records and tool. |
| There are no work records for Hilary *In Mt.*, Rabanus *In Mt.*, Jerome *In Hier.*, or Theodoret and Theophylact on 1 Thessalonians. Bede *In Marc.* accepts loci only in Mark 10. Ambrose *Exp. in Luc.* accepts no ranges. The NPNF I.10 Chrysostom Matthew edition names no translator. | research 0-2 | Shared records. |
| Wikisource's Ambrose prints "Matth. XVI, 33" at VII.188 and "Esai. XIII, 2" at VII.183. Rabanus's leaven block has a reading of Noah's sons that is not in Jerome. Run 66's leaf labels Sicard VI.23, which is VIII.23. | research 2; study-review 1 | A source transcription; the 66 leaf's next revision. |
| Douay-Rheims bindings are missing at Mt 16:6 and 17:19, 1 Cor 2:4, 5:7 and 5:8, and 1 Thess 2:2 and 3:1-7. The bindings-valid and `references-used` checks do not test whether a verse lies inside a binding. `references-used` misses abbreviated titles ("In Marcum III"). | study-review 2; synthesis-review 0 | Shared tool. |
| The chronology corpus prints David's regnal range beside the proposed occasion of Ps 129 and omits the Maccabean dating of Ps 43. Catholic Encyclopedia pages 11567b and 14629d have drifted from their registered hashes. | research 0-1 | The shared chronology corpus and source registry. |
| The generated Scriptural Date and Location page sets Catholic Encyclopedia titles from straight-quoted locators ("article ’David, King,’"; web review 1 counted 32 files in the two providers, not counting the GPT leaf of this identity), and its Jeremias label prints an ASCII "...". | web-review 0-1 observation | Shared source locators and chronology projection. |
| Lasance heads the Communion "Mark 11, 34" and repeats a phrase in the Latin Epistle. | research 0 | A source's own slips; recorded for the translations overlay. |
| `tools/print-document` refuses to print the synthesis while `homily.tex` is absent. `\runninghead` uses `\markright`, so the page-11 head is wrong. | build-artifacts 0 | Shared tool and print format. |
| Gate commands outgrew the runner's budget. `release-bindings status` traces one uncached chronology computation per publication (about 790 s for 292 publications). `document-library structure --check` takes about 320 s. `306cb81ea4` raises the budget to 1800 s; making the checks cheaper is still open. | publication-gates 0; install-publication 1 | Shared tools; this run fixed only the runner. |
| The render digest of a web review covers every `scripts/*.py`, so an edit to the workflow engine alone stales every accepted web review. | publication-gates 1 | Shared identity rule (`render_patterns` in `scripts/_document_schema.py`). |
| `test_the_gate_refuses_none_of_the_twenty_eight_manifest_leaves` hard-codes 28 manifest leaves. `main` already has 30, and this leaf makes 31. | driver's test run before `306cb81ea4` | Shared test census, also moved by the parallel GPT leaf. |
| `research/scope.md` and `research/interpretations.md` still carry the research glosses of Jerome (*In Hier.* V, "prayer commanded") and Aquinas (*in virtute*, truncated) that the study corrects. | study-review 1-2 | The research records are sealed; a next revision of this leaf. |
