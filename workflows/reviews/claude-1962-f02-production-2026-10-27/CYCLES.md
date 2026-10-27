# Every cycle the Claude All Saints production entered

Run `427e2f58bb897a16`, `proper-study` v15, provider `claude`, identity
`liturgy/roman-rite/1962/propers/temporal/f02-all-saints`, date 2026-11-01,
audience "adult parish assembly". Seeded at the authorization commit
`c7dfb84c7`. Terminal disposition **ACCEPTED**, with no escalations: 45
packets, 45 accepted results, 1 recorded intervention. The engine's own
record is archived in the leaf under
`evaluations/proper-study-results/427e2f58bb897a16/`, written by
`tools/proper-study-run-archive`. This file is the driver's account of why
the run went round, which the run directory does not state.

This is the second `F`-series leaf: All Saints, a first-class feast that in
2026 falls on Sunday, 1 November, displacing the Twenty-third Sunday after
Pentecost, which is commemorated. A published GPT leaf exists for the same
identity; under the production plan this is an independent Claude
production, and no stage opened any GPT-provider file or record for the
identity, not even as a precedent.

## Where the rounds went

| Stage | Results | Failing rounds |
| --- | ---: | ---: |
| research | 4 | 2 required changes |
| research-review | 4 | 2 |
| study-preflight | 4 | 1 |
| author-study | 4 | 3 required changes |
| study-review | 3 | 2 |
| derive-homily | 2 | 1 required change |
| homily-review | 2 | 1 |
| every other stage | one per round | 0 |

Six cycles, all real defects found by program gates or cold reviewers. No
seal went stale: the driver changed nothing the research seal covers after
it was taken, and the one commit that landed mid-run touched a different
collection entirely.

## The cycles, in order

| # | Stage that found it | Owner | What it was |
| ---: | --- | --- | --- |
| 1 | research-review 0 | research | RES-001: the 1570 Missal's Offertory was misreported (1570 reads *tormentum mortis*, no alleluia; the cited lines belong to other Masses). RES-002: the Offertory collation against Wis 3:1–3 was wrong. RES-003: the psalm numbering conflated NPNF, Vulgate and Douay conventions for Ps 33. RES-004: Pustet 1862 was reported read but had not been read. Research 1 repaired all four and bound the 1604, 1862 and 1889 text layers; the Offertory's alleluia was found first in Mame 1922 and the entry records the question as unresolved. |
| 2 | research-review 1 | research | RES-011: the Lasance English was quoted from unsealed artifacts. RES-012: dated web witnesses (ICRSP, FSSP, FSSPX, Missale Meum, Divinum Officium) were used unregistered. Research 2 sealed the Lasance records at their page images, withdrew the web witnesses from the evidence base, and set the authoring rule for the unresolved Preface: name both candidates (Trinity no. 1082, common no. 1086), assert neither. Source-registration 2 then registered the read web witnesses and Murphy 1960 as context-only restricted bindings; the Divinum Officium response was an access-block page and was not registered. |
| 3 | study-preflight 0 | study | The house-voice screen refused four sentences that narrated the work's own process ("that page is quoted on the Lasance's own attribution and has not been checked..."). Author-study 1 rewrote each with a source, text or fact as subject; the study held at 29 pages. |
| 4 | study-review 0 | research and study | STU-001 (research): the sweep reported Victorinus of Pettau's commentary does not reach Apoc 7 — a false negative caused by the containment inventory listing his extent as Rev 1, 5 and 19 only — so Reading A rested on Bede alone. STU-002..007 (study): no interpretation covered the whole Mass; a false claim of patristic agreement on the beatitude tenses; "Bellarmine alone" false (Aquinas *Super Ps.* 33 n. 10 says the same); the Fathers credited with the study's own thesis; the body narrated the study's procedure; maxim closers. Research 3 read Victorinus at chapters 7 and 12:6, Augustine's three brief loci, and Cyprian's dissent (martyrs only), and registered the PL 35 *Expositio in Apocalypsim*; author-study 2 rebuilt the readings at 30 pages. |
| 5 | study-review 1 | study | STU-013: the STU-001 research repair never reached the study prose — the false sentence still stood, Victorinus and Cyprian were absent, and the comparison row omitted the disagreement. The reviewer observed that a cross-owner finding routes to one owner only. Author-study 3 carried the repaired research into section 20, the comparison and the apparatus; 32 pages. |
| 6 | homily-review 0 | homily | HOM-001: the terminal note listed Gal 3:29 among the Douay quotations, but the spoken words are E. Marshall's 1878 English of the verse as Bede cites it. Derive-homily 1 corrected the note's route account; the spoken body is untouched. |

## Shared data the driver changed

| When | What | Why |
| --- | --- | --- |
| between research 1 and source-registration 1 | The branch gained `9dcebd258`, the Claude Four Last Things register revision, driven in a parallel worktree of the same branch | Maintainer-authorized concurrent work. It touches only `src/claude/articles/`, which the run's seal does not cover; the run's seals were verified after it landed. |
| install-publication 0 | Release bindings re-recorded for eleven of this production's own paths (the catalog page, the web Markdown, `corpus.json`, and eight source-structure files this run's registrations created) | The installer's scoped refresh. The driver confirmed every re-recorded binding belongs to this production before committing. |

A mid-run `origin/main` advance (`da270a039`, later `59a9862cc`) was never
merged into the run checkout before ACCEPTED, so no seal could go stale; it
merges at publication.

## Findings that did not gate

Across 12 cold reviews the run raised 11 blocking findings and 5 standing
advisories. What stands is in the leaf's
`evaluations/blocking-findings-v1.toml`, with the reviewers' observations.
The driver adds no findings of its own. Three classes are worth a first
revision:

- **Which authors carry Readings B and C** (RES-019, SYN-001).
  `proper-components.toml`'s `carrying_authors` names Aquinas and Hilary
  (B) and Augustine and Aquinas (C) where the reviewed `interpretations.md`
  marks those four "Supporting reception (not carrying)". The study text
  follows `interpretations.md`; the synthesis's apparatus propagated the
  manifest's side into prose. The records must be made to tell one story,
  and the synthesis sentence restated when they do.
- **Contained fidelity slips in the accepted study** (STU-014, SYN-002): a
  Hilary quotation drops *scilicet* (PL 9 col. 934 reads *in paternae
  scilicet majestatis*), and "the seven orations" appears twice where six
  orations exist. Both are contained and self-correcting in context; the
  synthesis already quotes Hilary with *scilicet* and counts nothing.
- **Typography** (VIS-001): the study's final page carries only the
  four-line rights colophon.

## Host interventions and events

| # | Stage | What |
| ---: | --- | --- |
| 0000 | resolve-context | The dispatch envelope. Every agent stage ran as a fresh Factory Droid worker subagent with no inherited conversation. The host exposes no per-dispatch effort control, so each brief carried the packet's declared `EFFORT` as workflow data and the host dispatch tier (`heavy`) as the record of what the host could set. Each worker received its packet by exact path and SHA-256 and read it in full. The driver added only the result path, a worker-owned scratch directory, the checkout path, the model identity and provenance form, the pinned-Markdown host note with the scratch virtualenv's path, that the driver alone runs git and `advance`, and the independence terms. |
| — | research-review 0 | The first dispatch died before writing a result: the packet's REVIEW_INPUTS line is ~259 KB. The driver verified the seal itself (1,764 files, 0 mismatches) and dispatched a fresh reviewer told to parse that line by script. |
| — | research 1 | The result used the key `disposition` where the schema requires `outcome`; the engine refused it. The same worker was resumed to rename the field only, then the result was accepted. |
| — | research 2 | Under the independence rule the worker did not open the FSSPX ordo edition the GPT All Saints production had registered; the run's own web witnesses were withdrawn from evidence instead (cycle 2). |
| — | research-review 3 | The first dispatch ended with a rejected model request after rendering four PL 35 page images. A fresh reviewer took the same packet and was told the surviving images were unverified. |
| — | author-study 1 | The worker ran `rm -rf` on its own web-probe directory under `build/` (generated output only). Later briefs forbade `rm -rf` outright. |
| — | author-study 3 | The first dispatch ended with a rejected model request before writing anything; a fresh worker took the same packet. |
| — | derive-synthesis 0 | The first dispatch ended with a rejected model request before writing anything; a fresh worker took the same packet. |
| — | install-publication 0 | The brief reserved git to the driver, so the installer left the installed web Markdown unstaged. The driver checked its bytes against the reviewed conversion (`2fd1fa16…`) and staged it before running `publication-gates`. |

**Model provenance: correction of 27 October 2026.** This paragraph first
said that every agent stage ran as `Opus 5.5`, the reviews at `xhigh`, and
that no other agent contributed. That was wrong. Without notice, the host
ran part of the driver's session, which wrote this record, and some workers
on kimi-k3 in place of the Claude model: all of source-registration 0, the
first dispatch of research-review 0, part of research 0 and of
source-registration 3, and every dispatch from research-review 3 onward.
The Claude workers ran as `claude-opus-5-5` at reasoning effort `high`, the
reviews included. On the maintainer's decision of that day the run is
superseded. The study goes back to its text after author-study 1, and a new
run rebuilds the research and makes every later revision; its
[handoff](../claude-1962-f02-revision-2026-10-27/HANDOFF.md) says what
carries over. This record and the archived run stay as the account of this
run and are not evidence.

The host carries Python Markdown 3.11, and `requirements-public-alpha.txt`
pins 3.10.3. Every web, probe, install and gate command therefore ran under
a scratch virtual environment built from the two requirements files.

## Sources the run settled

- **Latin.** The 1962 Missal governs, read on the published RGMR facsimile
  page images; the 1570, 1604, 1862 and 1889 layers were collated for the
  textual notes. The Offertory's alleluia is first held in Mame 1922, and
  the entry records the point as unresolved rather than smoothing it. The
  Preface is deliberately unsettled by instruction: both candidates
  (Trinity no. 1082, common no. 1086) are named and neither asserted, and
  nothing is built on either.
- **English.** The scriptural elements use the Douay-Rheims (Challoner).
  The orations and the remaining formulary English use the Lasance 1945
  text, sealed at its page images. One homily quotation is E. Marshall's
  1878 English of Gal 3:29 exactly as Bede cites the verse, and the
  homily's note says so (cycle 6).
- **Context witnesses.** The ICRSP, FSSP and FSSPX ordos and Missale Meum
  pages read during research, and Murphy 1960, are registered as
  context-only restricted bindings with no retained bytes. The Divinum
  Officium response was an access-block page and is not registered.
- **Patristic additions.** Victorinus of Pettau on Apoc 7 and 12:6 (ANF
  VII, under the editors' recension caution), Cyprian's rival martyrs-only
  reading, and Augustine's three brief loci entered at research 3; the
  anonymous PL 35 *Expositio in Apocalypsim* was registered as a tracked
  four-page facsimile excerpt with the Internet Archive OCR layer as a
  finding aid.

## What this run leaves for the owner

| Item | Evidence | Why it is not done here |
| --- | --- | --- |
| `source-containment-v1.toml` lists Victorinus's extent as Rev 1, 5 and 19, though the registered ANF VII text comments on Apoc 7 and 12:6; the same inventory has no constituent for the anonymous PL 35 *Expositio*. | STU-001 root cause; research-review 3 observation | A shared inventory, and the false negative it caused is the run's costliest cycle. |
| `propers.yaml` `omnium-sanctorum` ranges run wider than the said text (Gradual, Gospel, Offertory), there is no Preface case, the scriptural Latin bodies are not encoded, and the chronology loci inherit the ranges. | research; scope.md §10 | Shared calendar data and its derived projections. |
| `tools/tests/test_ordinary_appointments.py` `allSaintsSunday1962` asserts the common Preface without authority. | research; scope.md §10 | A shared test asserting what the sources leave open. |
| The Latin-provenance ledger has no rows for this formulary's six scriptural bodies; the translations ledger has no row for the Lasance scriptural artifact `ff92e98e`; `formulary-loci.yaml` has no rows for this formulary. | research; scope.md §10 | Shared ledgers. |
| `author-standing-v1.toml` has no rows for Bernard, Victorinus, Cyprian, Gregory of Nyssa, Alphonsus, Athanasius, Peter of Celle or Murphy. | research; scope.md §10 | A shared standing inventory. |
| `work.fsspx.ordo` declares English, but its responses are French. | source-registration 2 | A shared source record. |
| Bede's *Explanatio Apocalypsis* has no passage records for Apoc 7:2–3. | research; scope.md §10 | Shared passage records. |
| `scope.md` omits the Aquinas *necessitate* clause the study needed. | author-study 2 report | The research records are sealed; a next revision of this leaf. |
| The study twice says "the seven orations" (SYN-002), and one Hilary quotation drops *scilicet* (STU-014). | synthesis-review 0; study-review 2 | Standing advisories against this leaf; a next revision. |
| A cross-owner finding routes to one owner only: STU-001's research repair never reached the study prose until a second finding (STU-013) caught the gap. | study-review 1 observation | Engine behaviour. |
| `manifest carrying_authors` and `interpretations.md` disagree on who carries Readings B and C (RES-019), and the concise apparatus propagated the manifest's side (SYN-001). | research-review 3; synthesis-review 0 | The alignment is the research owner's call, then a leaf revision. |
