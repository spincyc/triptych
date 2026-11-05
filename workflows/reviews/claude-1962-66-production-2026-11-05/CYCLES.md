# Every cycle the Claude resumed Fifth Sunday production entered

Run `eb621aedbeee828e`, `proper-study` v17, provider `claude`, identity
`liturgy/roman-rite/1962/propers/temporal/66-resumed-fifth-after-epiphany`,
date 2026-11-08, audience "adult parish assembly". Seeded at `2629d99f48`,
after the authorization commit `f591cb68ee` and the pre-seed workflow fixes.
Terminal disposition **ACCEPTED**, with no escalations: 40 packets, 40
accepted results, 3 recorded interventions. The engine's own record is
archived in the leaf under
`evaluations/proper-study-results/eb621aedbeee828e/`, written by
`tools/proper-study-run-archive`. This file is the driver's account of why the
run went round, which the run directory does not state.

Sunday, 8 November 2026 is the Fifth Sunday after the Epiphany resumed after
Pentecost (II class, green), permanent identity `66`. The commemoration of
the Four Crowned Martyrs is omitted at every Mass under RG 111 b. A published
GPT leaf exists for the same identity. Under the production plan this is an
independent Claude production. The briefs closed the GPT leaf, its release
records and its workflow records to every stage, even as a layout precedent.

This is the first run at `proper-study` version 17, the source-and-reader path
of the no-PDF work. No run had been seeded at version 16 or 17.

## The workflow audit before seeding

The maintainer asked that the no-PDF work be checked for every part of this
workflow it should have updated. A read-only audit simulated a Claude leaf on
a scratch clone and ran each v17 gate. It found steps that no stage or driver
note stated, and three defects that would have stopped a run part-way. The
fixes landed before seeding, because the research seal covers the tooling:

| Commit | What |
| --- | --- |
| `600bffa461` | The native-print artwork loader and `render-sanctuary-dictionary` executed the sanctuary validator under `src/` through importlib, which wrote an ignored `__pycache__` there. Product keys govern bytecode outside `scripts/` and `tools/` by design, so the cache staled five browser-product families. Both loaders now execute the source without a cache. |
| `a7017bba3b` | `snapshot-web` and the publication gate refuse a reader converted from uncommitted sources, whose revision stamp is the conversion time. The catalogue gate no longer counts a `triptych-publication-reference` row as a second owning row; the GPT 66 gate already failed on its row-16 cross-reference. Source registration runs `make source-projection` instead of a mid-run `browser-products record`, which the documents producer refuses while the leaf is a scaffold. Installation names `make add-publication` and leaves the record and bindings to the driver. `OPERATOR.md` states the four driver steps, and the stale prose and tests are corrected. |
| `f8a555b7c0` | Four apparatus inventory hashes stale since `d151693267` were refreshed, so `make check-sources` passed at the base. |
| `2629d99f48` | Browser products re-recorded and the five changed site-source bindings refreshed. |

The `public-alpha verify` deploy gate refuses while the reserved scaffold
`main.tex` has no release record ("cannot read publication disposition"). No
run stage reaches it, so the pre-seed checkpoint push was skipped and the
deploy gates ran once, after installation.

One defect surfaced only at installation, and the fix stayed out of the
tooling. The v17 install fragment asks the installer to record the passed web
review in `web-edition.toml`. At this seed that file is an input of the
content and render identities that the web review binds. A scratch worktree
showed that the three inspection fields change content `0bcae686…` to
`980d2b12…`. No v17 gate requires the fields. The driver therefore had the
installer leave the file unchanged and recorded the inspection after
acceptance, once `858760b867` on `main` had put those fields outside the
reviewed identity (intervention 0002). A parallel GPT session found the same
gaps independently and published version 19 on `main` while this run was
live. Neither change was merged mid-run.

## Where the rounds went

| Stage | Results | Failing rounds |
| --- | ---: | ---: |
| research | 2 | 1 required change |
| research-review | 2 | 1 |
| author-study | 4 | 3 required changes |
| study-review | 4 | 3 |
| derive-synthesis | 2 | 1 required change |
| synthesis-review | 2 | 1 |
| derive-homily | 2 | 1 required change |
| homily-review | 2 | 1 |
| every other stage | one per round | 0 |

Six cycles, all real defects that cold reviewers found. No program gate
failed, and no seal went stale. The driver committed the leaf after the
artifact gates and changed nothing else that the seals cover.

## The cycles, in order

| # | Stage that found it | Owner | What it was |
| ---: | --- | --- | --- |
| 1 | research-review 0 | research | RES-001: Augustine's Sermo 73 and Ep. 93 (NPNF) and Hilary's tractate on Ps 129 (PL 9) were held but reported as not held; Ep. 93 bears directly on the coercion question. RES-002: Rupert (*De div. off.* XII.23), Durandus (*Rationale* VI.140–142) and Guéranger's *Liturgical Year* vol. 11, which prints this resumed Mass, were also held but reported absent. RES-003: scope claimed every held work was opened at its passage. RES-004: two dated Ordos were used unregistered. Research 1 read all of them, replaced the claim with a per-passage table, registered the Ordos and Aquinas's *Super Colossenses*, and the bindings went from 36 to 55. |
| 2 | study-review 0 | study | Seven findings on how the prose argued, not on its evidence. Closing roll calls gave each remaining text a part. Texts and Jerome were credited with the study's own links. "On this interpretation" and similar labels appeared about 18 times. Paragraphs ended by restating themselves. The third reading's anagogy duplicated the first's. Aquinas's *ne forte* was presented as his own when he takes it from Augustine, and his q. 11 a. 3 conclusion went unstated. A count of *de profundis* was wrong. |
| 3 | study-review 1 | study | The repair of cycle 2 overcorrected. Removing the roll calls dropped texts from two interpretations (STU-013) and left others beside quotations with no stated reason (STU-001). q. 11 a. 3 was now given the parable as its premise when Aquinas grounds it otherwise (STU-006). The third reading made the word the seed, against Mt 13:38 and Aquinas's *Super Mt.* c. 13 (STU-015). |
| 4 | study-review 2 | study | The repair of cycle 3 brought the label tic back: about 20 "this interpretation takes … as" labels, and five links resting on one shared word (STU-003). Revision 3, briefed on the two pulls together, removed both; the fourth and last allowed review passed with three advisories. |
| 5 | synthesis-review 0 | synthesis | SYN-001: the concise References listed two loci the text never uses. The `references-used` preflight passed them because it does not read *Enarr. in Ps.* as that entry's title, and any mention of Psalm 43 satisfies a single-verse locus. |
| 6 | homily-review 0 | homily | HOM-001: four paragraphs stacked Fathers on one point instead of the preacher making the step, and the Aquinas paragraph never drew its conclusion (God, not the servants, frees the wheat). |

## Host interventions and events

| # | Stage | What |
| ---: | --- | --- |
| 0000 | resolve-context | The dispatch envelope. Every agent stage ran as a fresh Claude Code harness subagent (`claude-opus-5-5`) with no inherited conversation, at its packet's declared effort through the harness's per-dispatch effort control: authors `high`, reviews `xhigh`. Each worker received its packet by exact path and SHA-256. The driver added the result path, a worker-owned scratch directory, the environment, provenance, the reservation of git and `advance` to the driver, no tool or shared-calendar edits, and the independence terms. |
| 0001 | author-study 0 | The accepted research review left advisories RES-008 to RES-013, including an anagogy that reversed Rabanus. The author brief named that review's result file as context and added no content instruction. Later author and reviewer briefs named the defect classes earlier rounds had found. |
| 0002 | install-publication 0 | The `web-edition.toml` inspection was deferred, for the identity reason above. |
| — | artifact-gates 0 | The driver committed the source registrations (`6445d32a78`) and the leaf (`9d88c8fe2c`) before `generate-web`, so the reader carries the stamp `2026-11-05T20:49:20Z`. |
| — | install-publication 0 | The driver committed the installation (`689e445e82`), re-recorded browser products (13 families, 27,690 files) and adopted bindings for exactly 59 attributable paths (`23374074fd`) before the terminal gate. |

The host carries Python Markdown 3.11 and the repository pins 3.10.3. Every
stage, web probe and gate ran under a scratch virtualenv built from the two
requirements files, with `PYTHONDONTWRITEBYTECODE=1`.

## Sources the run settled

- **Latin.** The 1962 Missal, read on the page images of the resumed printing
  (nos. 1749–1758), governs. Every word also stands in Pustet 1862, read on page
  images, so the publication mode is `complete`. The Postcommunion ends with
  the short *Per Dominum* of the resumed printing.
- **English.** Douay-Rheims for Scripture. For the chants and orations,
  Lasance 1945 "Supplementary Mass No. 2", which prints this exact resumed Mass.
- **Witnesses added by review.** Augustine's Sermo 73 and Ep. 93, Hilary on
  Ps 129, Rupert, Durandus, Guéranger, Aquinas *Super Colossenses* (Corpus
  Thomisticum, restricted, metadata only), and the FSSP and ICRSP Ordos for
  the date (restricted, metadata only). Augustine's *Quaestiones Euangeliorum*
  I.10 is admitted to the Catena with its Matt 13:25–30 edge.

## Findings that did not gate

Across eleven cold reviews the run raised 19 blocking findings, all repaired.
Fourteen standing advisories remain, recorded in the leaf's
`evaluations/blocking-findings-v1.toml`:

- research: RES-008 to RES-013;
- study: STU-019 to STU-021;
- synthesis: SYN-005;
- homily: HOM-003, HOM-006 and HOM-007;
- web: WEB-001.

Two are worth a first revision. STU-019: the study's claim that Jer 29:12's
promise to hear covers the prayer for the city (29:7) rests only on the two
standing in one letter. HOM-007: the homily's Bede line drops what is asked
for, and both studies compress it the same way.

## What this run leaves for the owner

| Item | Evidence | Why it is not done here |
| --- | --- | --- |
| The Latin-provenance ledger has no rows for the resumed printing (nos. 1749–1758), records a colon after *innititur* in the 1862 Collect where the page shows a comma, and the finding aid gives the Postcommunion the long Epiphany-season ending. | resolve-context 0; research 0 | Shared ledgers. |
| The translations overlay and the Lasance Secret passage call p. 746 "Supplementary Mass No. 3"; it is No. 2. | research 0 | Shared source records. |
| `formulary-loci.yaml` lacks Sicard, Schuster, Rupert, Durandus and Fromage on this Mass; `work-aliases.yaml` has no groups for Augustine's sermons and letters, the Summa, Rupert, Durandus, Sicard, Schuster or Honorius, which keeps Sermo 73 from admission. | source-registration 0–1 | Shared harvest records. |
| Bede's work record accepts loci only in Mark 10:32–45; Theodoret on Colossians and Theophylact's Pauline commentaries have no work records; `author-standing-v1.toml` has no Athanasius row; the Chrysostom Matthew CCEL edition names no translator; containment lists only 2 Cor and Ephesians for Aquinas's Dessain vol. II. | research 0–1; source-registration 1 | Shared records. |
| The shared chronology corpus lacks the Maccabean alternative for Ps 43; the date page's Jer 29 row has no year, and its Communion row (Mk 11:24) has only a composition date. | research 1; synthesis-review 0–1 | The shared chronology corpus. |
| `research/interpretations.md` still proposes the field "in which the word is sown" and the old third anagogy, which the study corrects. | author-study 1–2 | The research records are sealed; a next revision of this leaf. |
| `check-content-preflight references-used` misses abbreviated titles and lets any mention of a psalm satisfy a single-verse locus. | synthesis-review 0 observation | Shared tool. |
| `tools/document-schema check` prints "use --run-gates" even when the gates ran. | build-artifacts 0 | Shared tool. |
| Nested `'''` closing quotes print in the wrong order in the native PDF; the reader is correct. | web-review 0 observation | Shared print format. |
