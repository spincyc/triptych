# Every cycle the Claude Christ the King production entered

Run `7397c12187517ff2`, `proper-study` v12, provider `claude`, identity
`liturgy/roman-rite/1962/propers/temporal/f01-christ-the-king`, date
2026-10-25, audience "adult parish assembly". Seeded at the authorization
commit `9b87d598b`. Terminal disposition **ACCEPTED**, with no escalations:
33 packets, 33 accepted results, 4 interventions. The engine's own record is
archived in the leaf under `evaluations/proper-study-results/7397c12187517ff2/`,
written by `tools/proper-study-run-archive`. This file is the driver's account
of why the run went round, which the run directory does not state.

This is the first `F`-series leaf either provider has produced: the feast of
Our Lord Jesus Christ the King, which RG 17 d assigns to the last Sunday of
October and which displaces the Twenty-second Sunday after Pentecost with no
commemoration. No GPT leaf exists for the identity, and no stage opened any
GPT-provider leaf or record.

## Where the rounds went

| Stage | Results | Failing rounds |
| --- | ---: | ---: |
| research-review | 3 | 2 |
| study-review | 2 | 1 |
| synthesis-review | 2 | 1 |
| homily-review | 1 | 0 |
| artifact-gates | 1 | 0 |
| visual-review | 1 | 0 |
| web-review | 1 | 0 |
| every other gate | one per round | 0 |

Four cycles, all real defects found by cold reviewers. No seal went stale: the
driver changed shared data only before the research seal was taken, and
nothing outside the leaf after it.

## The cycles, in order

| # | Stage that found it | Owner | What it was |
| ---: | --- | --- | --- |
| 1 | research-review 0 | research | RES-001: the sweep for Pss 2, 28 and 71 and Col 1 listed held direct commentaries as "held and not read". The tracked Bellarmine bears on all three readings. RES-002: Reading B answered the formulary's subjection of kings and nations only from *Quas primas*, and omitted Augustine's own *En. in Ps.* 71.13. RES-003: the calendar entry lists the votive Tract as an ordinary proper and omits the paschal Alleluia, so the orientation gate would print the Tract's Ps 88 rows on page 2, and the research told authoring the opposite. The finding offered a calendar correction or a research-only branch. The driver chose the second (intervention 0003). Research iteration 1 read Bellarmine, Cassiodorus, Aquinas *Super Psalmos* and *Super Col.*, Basil and Theodoret, found Schuster's *Sacramentary* V pp. 200–204, rebuilt Reading B on *En. in Ps.* 71.13–14 and *Letter* 185, and labelled the Tract rows "printed for votive Masses after Septuagesima, never said on this feast". |
| 2 | research-review 1 | research | RES-008: `interpretations.md` credited Schuster with links between elements that he never makes. His only join is the Gradual with the Alleluia as "the double chant" (p. 203). Research iteration 2 split his comments element by element and labelled every other grouping as editorial synthesis. It also cleared RES-009 to RES-011 (Chrysostom's Jn 5:26 rule, Cassiodorus's *Complexiones* on Colossians, the Lapide and Athanasius holdings). |
| 3 | study-review 0 | study | STU-001: author-facing instructions from `scope.md` and `interpretations.md` reached reader prose in about eight places ("Both are kept here, each under its own witness", "the one witness read"). The house-voice screen passed every one. STU-002: the comparison section misplaced the sharpest difference between Readings A and B, gave Reading C's internal differences as its strongest objection, defined Reading B's cross wrongly, and omitted Hilary from Reading B. Author-study iteration 1 rewrote each sentence to state the material, rebuilt the comparison, and cleared STU-003, STU-004 and STU-006. The study grew from 32 to 33 pages. |
| 4 | synthesis-review 0 | synthesis | SYN-001: page 4 said the flood clause of Ps 28:10 stands "between" the Communion's two sung half-verses. It stands before them; "The Lord will give strength to his people" stands between. The expansive study and the concise study's own commentary had it right. Derive-synthesis iteration 1 corrected the sentence at the same length, keeping the themes on pp. 3–4. It also cleared SYN-002 to SYN-005, including the Douay References, which now use the Challoner numbering. |

## Shared data the driver changed

| Commit | When | What | Why |
| --- | --- | --- | --- |
| `aa94dd3b4` | after resolve-context 0, before research | `christ-the-king` Communion `Psalms 28:10` → `Psalms 28:10-11` in `src/sources/calendars/roman-1962/propers.yaml`; derived `src/web/data/structure/propers/roman-1962.json` and `roman-pre-1955.json` regenerated | The Missal (printed p. 698) prints *Ps. 28, 10 et 11*. The auto-mode classifier refused the edit as a shared-resource change; the maintainer authorized it explicitly. Made before the research seal, so no stage reran (intervention 0001). |
| `0fc5dce93` | after research 0, before research-preflight | Rebuilt the Clementine, both Douay-Rheims and the Catholic Public Domain Version Bible indexes | **Driver miss.** The indexes are keyed by calendar reference strings, so `aa94dd3b4` staled all four and `mass-propers show` printed no Communion text. The driver had verified that commit with `make check-sources`, which does not reach `check-bible-indexes`. The research worker reported it (intervention 0002). |
| this production's commit | install-publication 0 | `release/public-alpha.json` bindings for the two propers JSON files | **Second driver miss of the same kind.** `aa94dd3b4` never refreshed those files' release bindings, and `check-release-bindings` is outside `check-sources` too. The installer adopted exactly those two paths with its own five; the driver confirmed them as this production's change. |

A calendar fix needs `make check-bible-indexes check-release-bindings
check-propers-structure` as well as `check-sources` before it is committed.

## Findings that did not gate

Across 10 cold reviews the run raised 7 blocking findings and about 30
advisories. What still stands is in the leaf's
`evaluations/blocking-findings-v1.toml`: 15 advisories and 2 accepted
findings, with the reviewers' observations. The driver adds no findings of its
own. Four classes are worth a first revision:

- **The homily (HOM-001 to HOM-005).** These are the ones a preacher using the
  text should read first. HOM-003 says the soldiers' prayer comes "a few
  minutes after a Gospel", but the Credo, Offertory, Canon and Communion stand
  between. HOM-004's "We shall not see this kingdom complete" needs "in this
  life". HOM-001 says "born a King" without saying which birth, and Chrysostom
  means the eternal one. HOM-002 is a note-versus-text mismatch on
  Chrysostom's "received nothing in addition". HOM-005 names Schuster
  unidentified, in a dense sentence that cannot be read aloud.
- **Sealed research records lag the reviewed study** (RES-012 to RES-014,
  STU-007 (c), STU-010). `interpretations.md` §5 still holds the comparison
  wording STU-002 found untrue, and `scope.md` §8.4 lacks the Haydock
  qualification of the Tract's Babylonian setting. No stage after the research
  seal may write research records, and the study-review observation notes
  that the pipeline has no route for a research-owned advisory once the seal
  is set. The Seventeenth through Twenty-first Sunday runs ended with the same
  class.
- **Prose precision** (STU-005, STU-008, STU-009, SYN-006, SYN-007): repeated
  quotations, "a dominion that needs nothing given", an added *et* in the
  Aquinas Latin, Augustine's alternative reading of Ps 2:9 given as his
  reading, and a Lasance page range that supports nothing in the concise.
- **Typography** (VIS-001, VIS-002): the eleven-row element map on study
  pp. 3–4 splits 10/1. The running head takes the first mark on a page, so a
  page where a section begins lower down carries that section's head. That
  behaviour lives in the shared `src/common/propers-format.tex`.

## Host interventions and events

| # | Stage | What |
| ---: | --- | --- |
| 0000 | resolve-context | The dispatch envelope. Every agent stage ran as a fresh Claude Code harness subagent with no inherited conversation, at exactly the effort its packet's `EFFORT` line declares, through the harness's per-dispatch effort control. Each worker received its packet by exact path and SHA-256 and read it in full. The driver added only the result path, a worker-owned scratch directory, the checkout path, the model identity and effort for the generation record, the pinned-Markdown host note with the scratch virtualenv's path, that the driver alone runs git and `advance`, and the independence terms. |
| 0001 | research | The `aa94dd3b4` calendar correction, above. |
| 0002 | research-preflight | The `0fc5dce93` index rebuild, above. `scope.md` §10's "index stale" statement described the state when research 0 ran; research 1 marked it resolved. |
| 0003 | research | The RES-003 decision. The calendar stayed unchanged, because `propers.yaml` records that it has no way to say when a proper is said. Encoding the Tract's votive condition is a schema and tooling change, and adding the paschal Alleluia unconditionally would repeat the defect in the reader. |
| — | author-study 0 | The driver's brief said not to edit `research/`, while the packet assigns `research/production-review.md` to the author. The worker followed the packet: that file is excluded from the research seal, and it recomputed the seal to confirm. Later briefs named the exception. |
| — | web-review 0 | The worker stopped on an API rate limit (HTTP 429) before writing its result. After the reset, the same worker was resumed with SendMessage instead of dispatching a second reviewer. It re-verified every sealed hash before relying on its earlier work. |
| — | web-review 0 | The reviewer created one temporary file in the system temp directory, outside its scratch directory, and deleted it at once. Nothing in the checkout was affected. |
| — | install-publication 0 | The brief reserved git to the driver, so the installer left the installed web Markdown unstaged. The driver checked its bytes against the reviewed conversion (`e7bc1c59…`), and staged it with the new AAS 17 source-projection file before running `publication-gates`. |

**Model provenance.** Every agent stage ran as `claude-opus-5-5[1m]`, the
driver's model, at its declared effort: `high` for the author, build, web and
install stages, `xhigh` for the ten reviews. The leaf's
`generation-metadata.tex` declares that model and effort for each author and
derive stage. No other agent contributed.

The host carries Python Markdown 3.11, and `requirements-public-alpha.txt`
pins 3.10.3. Every web, probe, install and gate command therefore ran under a
scratch virtual environment built from the two requirements files. Before
the run, every `pdf/` entry of the live `SHA256SUMS` was already present
locally with a matching hash, so nothing was restored.

## Sources the run settled

- **Latin.** The formulary dates from 1925, after every tracked older Missal.
  The research stage registered *Acta Apostolicae Sedis* 17 (1925),
  fascicle 15, pp. 666–668, from an Internet Archive microfilm scan
  (`src/sources/works/holy-see/acta-apostolicae-sedis/editions/volume-17-1925/`).
  It collated every element and the Preface word for word against the 1962
  page images. The basis is 17 U.S.C. 103(b) over a pre-1931 public-domain
  first printing. The Holy See's own vatican.va PDF was rejected: it is an OCR
  reconstruction without page images.
- **English.** The scriptural elements use the Douay-Rheims. The orations and
  the Preface use the Lasance 1945 English, read on its page images, and its
  pre-1960 rubrics are disclosed as not the 1962 order.

## What this run leaves for the owner

| Item | Evidence | Why it is not done here |
| --- | --- | --- |
| `propers.yaml` cannot say when a proper is said. `christ-the-king` stores the votive Tract as a chant of the day and omits the paschal Alleluia (no. 3944, Apoc 19:16), so page 2 prints the Tract's Ps 88 rows under a label, and the reader shows a Tract for an October feast. The entry's own notes and the file's F-series header note are stale. | RES-003; resolve-context 0; intervention 0003 | A calendar schema and chronology-tool change. |
| No verse alias maps the Missal's Ps 71:1. In the tracked Bibles 71:1 is the title, so `mass-propers show` serves "A psalm on Solomon." as the Introit verse. | resolve-context 0; research-review 0 | Shared versification data. |
| `tools/web-edition` refuses `\textit`/`\emph` in an orientation place phrase that preflight allows: `normalize_audit_text` unwraps `\textbf` only. | author-study 0 | Two shared tools that disagree. The author used quotation marks. |
| The chronology generator's Passage cells mix "Ps 71:1" with "Psalms 71:8,11", with no space after the comma. | research-review 0 to visual-review 0 | A shared generator. |
| The house-voice screen passed every STU-001 process sentence. `references-used` checks neither that quoted verses are listed nor page ranges on non-commentary entries. | STU-001; synthesis-review 0 and 1 observations | Preflight criteria. |
| The pipeline cannot route a research-owned advisory once the research seal is set. | study-review 1 observation | Engine behaviour. |
| `commentary-work-index discover` reports a work as "held" without saying whether the held item reaches the passage (Lapide, Hugh of Saint-Cher, Athanasius). | research-review 2 | A missing tool criterion. |
| The Schuster edition record dates the set 1927, but volume V's imprint reads 1930. Schuster vol. V, Augustine *Letter* 185, Theodoret on Colossians, Aquinas *Super Col.* and the newer Cassiodorus pages are unregistered. `author-standing-v1.toml` has no rows for Cyril of Alexandria, Cyril of Jerusalem, Hippolytus or Victorinus. The Latin provenance and translation ledgers have no rows for this formulary. | research 0 to 2; research-review 1 and 2 | Shared source-library records and inventories. |
| The chronology corpus binds no event to Jn 18:28–19:16, has no critical composition claim for Daniel, and has no rows for Dan 7:1 or Ps 28's title. | research-review 0; research 1 | The neutral chronology corpus. |
| At phone width, the opening element map and the four-column comparison scroll inside their frames. The no-clip treatment approved for the date table does not cover them. | web-review 0 observation | The site stylesheet. |
| The visual-review fragment names no destination for rasters the reviewer generates itself. | visual-review 0 observation | Workflow fragment. |
