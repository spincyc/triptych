# Every cycle the Claude Nineteenth Sunday production entered

Run `a27462e34ec9c09a`, `proper-study` v7, provider `claude`, identity
`liturgy/roman-rite/1962/propers/temporal/59-nineteenth-after-pentecost`,
date 2026-10-04, audience "adult parish assembly". Seeded at the
authorization commit `56d8c30f2`. Terminal disposition **ACCEPTED**, with no
escalations: 30 packets, 30 accepted results, 2 interventions. The engine's
own record is archived in the leaf under
`evaluations/proper-study-results/a27462e34ec9c09a/`. This file is the
driver's account of why the run went round, which the run directory does not
state.

The GPT leaf for the same identity was published on 2026-09-28. This run is
an independent Claude production: no stage opened that leaf. The context and
research stages used two provider-neutral library records the GPT production
had registered (the Pustet 1862 extraction and the checked Cummiskey English)
as library evidence, and read their pages afresh.

## Where the rounds went

| Stage | Results | Failing rounds |
| --- | ---: | ---: |
| research-review | 3 | 2 |
| study-review | 2 | 1 |
| synthesis-review | 1 | 0 |
| homily-review | 1 | 0 |
| visual-review | 1 | 0 |
| web-review | 1 | 0 |
| every gate | one each | 0 |

Three cycles in all, which are the run's non-PASS transitions. No stage came
near a budget: research-review reached two consecutive novel rounds of the
four `max_novel_iterations` allows, with no repeat.

## The cycles, in order

| # | Stage that found it | Owner | What it was |
| ---: | --- | --- | --- |
| 1 | research-review 0 | research | RES-001: the five authored chronology corpus files and the canon and concordance data the chronology tool opens were outside the seal, while `scope.md` §7.3 said they were sealed; the Ordo Missae and Preface passage records `context.md` relied on were neither bound nor declared. RES-002: located witnesses left unread, above all Hilary on Ps 140:2, the Gradual verse (lifted hands as works of mercy), with Hilary's Ps 118 negative bounded to the wrong source and Bellarmine, Chrysostom and Aquinas unread at their loci. RES-003: a Hilary clause about the prepared feast (Mt 22:4) applied to the filled hall (v. 10). RES-004: an Israel-then-nations consensus that Gregory and Augustine do not share. Research iteration 1 repaired all four and cleared RES-005 to RES-007; re-reading the Ordo Missae corrected one row of `context.md` (no. 1024 is the Kyrie, no. 1025 the Gloria). |
| 2 | research-review 1 | research | RES-008: the rewritten scope said Augustine gives no answer on the highways, but his *Quaestiones evangeliorum* I.31, held, tracked and mapped by the commentary index, reads them as *dogmata Gentium*; Rabanus on Ephesians and Rolle on Ps 104 were also unrecorded. The reviewer noted that its own iteration-0 wording ("Augustine's silence") had invited the error. Research iteration 2 read I.31 against a page image of PL 35 col. 1329, registered PL 35 (1845) with a two-page excerpt and a containment entry, and gave every `discover` lead a disposition. |
| 3 | study-review 0 | study | STU-001: Honorius, whose Mass had another Gospel and Alleluia, had been given a "third answer" in the second reading. STU-002: the Gospel and Epistle dossier rows omitted the places of writing the declared `composition.yaml` supplies, and did not say that c. A.D. 50 is Durand's date for the Aramaic Matthew. STU-003: Schuster was credited with "the feast is the Church now", where his own p. 173 reads the banquet as the heavenly one. Author-study iteration 1 repaired all three, cleared STU-004 to STU-007, and corrected one Schuster page reference (p. 174). |

Each was a real defect in the work, visible to no mechanical gate, and each
was caught before the next document was written, so no downstream document
reran.

## Findings that did not gate

Across nine cold reviews the run raised 8 blocking findings and 23
advisories; those that stand are in the leaf's
`evaluations/blocking-findings-v1.toml`. The driver adds no findings of its
own. Two classes are worth a first revision:

- **Research records lag the reviewed study (STU-011, STU-012).**
  `research/interpretations.md` still names Schuster as a carrying author of
  the third reading and keeps Honorius in the second, and
  `research/source-bindings.toml` binds neither the Douay verse texts the
  documents print nor Ps 104:1 in the NPNF1-8 binding. No stage after
  research-review may write research records; the three documents follow the
  corrected reading at each point. The Seventeenth, Eighteenth and
  Twenty-sixth Sunday runs ended with the same class.
- **Accuracy advisories.** STU-008 (the opening's "these Fathers carry it"
  sentences credit more than each says), STU-009 (the Postcommunion said to
  name the sacrament; the Introit antiphon called the Church's own
  composition), SYN-001 (page 1 credits Augustine with Gregory's clause on
  the Bridegroom's garment of charity), HOM-002 ("this morning's Collect" at
  a later Mass) and HOM-003 (psalm citations without their Hebrew numbers).

The chronology corpus carries no modern critical date for Matthew or
Ephesians, so page 2 of the concise study gives only the traditional
profile; two reviews recorded this as an observation outside this leaf's
owners. The homily's size per page (84.5 KiB, over the 75 KiB review
trigger) is embedded fonts, not images.

## Host interventions

| # | Stage | What |
| ---: | --- | --- |
| 0000 | resolve-context | The host exposes no per-dispatch effort control and no pinned-effort agent definition was loaded, so every agent stage ran at the driver session's effort whatever it declared. Each worker received its packet by exact path and SHA-256 and read it in full; the driver added only the result path, a worker-owned scratch directory, the checkout path and, for author stages, the model identity for the generation record. |
| 0001 | publication-gates | Before the gate ran, the driver fixed the converter defect below, merged `origin/main` and ran the gate under the pinned Markdown. See the next section. |

**Model provenance.** Every agent stage ran as `claude-opus-5-5[1m]`, the
driver's model. The leaf's `generation-metadata.tex` declares that model for
each author and derive stage, with the declared effort and the host
deviation.

## What was repaired because of this run

`make check-web-editions-current`, one of the terminal gate's checks, failed
at the seed base on a leaf this run does not own: the Claude angelology
draft, declared eligible and on release hold, with its unwritten sections
commented out and no tracked web edition. Two changes cleared it:

- `d8c32cf92`: `tools/web-edition` matched `\input` in raw TeX, so a
  commented-out `%\input{...}` was treated as live input. It now finds
  inputs in a comment-masked copy, as `tools/check-web-edition` already did;
  a regression test fails without the fix. With it alone, the check still
  failed, now for the held draft's missing tracked edition.
- `7c5faf256`: `origin/main` at `af0929127` had meanwhile published that
  leaf and declared it conditional. Before merging, the driver confirmed that
  none of the 230 paths main changed is among the 2,064 paths sealed into
  this run's reviews, and that main's converter (with `cfc03a354`)
  reproduces this leaf's reviewed web Markdown byte for byte. The six
  conflicted derived records were regenerated with their owning tools and
  the install stage's five release bindings re-recorded, scoped.

The gate then passed on its first run. The host carries Python Markdown
3.11 and `requirements-public-alpha.txt` pins 3.10.3, so generate-web,
web-review, install-publication and the gate ran under a scratch virtual
environment built from the two requirements files.

After acceptance, registering PL 35 had changed one recorded example of
`tools/commentary-work-index` (`discover --passage 'John 3:16'`), which
passes on `main`; its transcripts were recaptured from real runs, and the
tool's 13 examples replay clean.

## What this run leaves for the owner

| Item | Evidence | Why it is not done here |
| --- | --- | --- |
| The research records lag the reviewed study (STU-011, STU-012) | `evaluations/blocking-findings-v1.toml` | Only a research stage may write them, and reopening research reruns every document and review |
| The FSSP France *Ordo du mois* is registered under two work identities | resolve-context 0 result | A library record outside this leaf |
| The chronology corpus has no modern critical date for Matthew or Ephesians | study-review 0 observation | The neutral chronology corpus, not this leaf |
| No traditional date for the five psalms, no event date for the Gospel, no Latin-provenance rows for the six scriptural elements, and four stale translation-overlay rows | research 0 result | Shared registries outside this leaf |
| `make check-examples` still diverges on 36 transcripts of other tools whose recorded output predates this run, among them the document-library counts ("143 works, 197 documents") and public-alpha checks that need every installed PDF | replay at `af0929127` and on this branch | Unrelated tools' transcripts |
