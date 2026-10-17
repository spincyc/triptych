# The Claude Twenty-ninth Sunday revision

Run `821c824684b0c7a7`, `proper-study` v12, provider `claude`, identity
`liturgy/roman-rite/postconciliar/roman-missal-third-edition-en-us-2011/propers/temporal/pc-s55-twenty-ninth-sunday-in-ordinary-time-year-a`,
date 2026-10-18, audience "adult parish assembly", research handoff
[`HANDOFF.md`](HANDOFF.md). Seeded at `d5abae027`. Terminal disposition
**ACCEPTED**, with no escalations: 21 packets, 21 accepted results, 1
intervention. The engine's record is archived in the leaf under
`evaluations/proper-study-results/821c824684b0c7a7/`, beside the first run's
`4d16b5e19d25dad9`, whose account is
[`../claude-pc-s55-production-2026-10-16/CYCLES.md`](../claude-pc-s55-production-2026-10-16/CYCLES.md).

On 16 October 2026, after the first run was published, the maintainer asked
for its standing issues and its sourcing to be fixed and the result pushed to
`main`. The maintainer then chose to fix every shared tool the first run had
exposed, with display changes gated to new runs. Those changes landed before
seeding:

| Commit | Change |
| --- | --- |
| `6cd55152a` | The three-column page-2 table at phone width; the dossier rules also name the `historical-appendix` id. |
| `13423ec4c` | Locus-aware `references-used`; the house-voice screen extended to the forms STU-001 found. |
| `1b7eba7e0` | `orientation-v2` (Gospel-pericope event rows, en-dash ranges, explicit psalm numbering) and `proper-study` version 12. |

Every review in this run passed at its first round, so the run entered no
repair cycle. Its one host event is below.

## What became of the 22 standing findings

| Finding | Outcome |
| --- | --- |
| STU-004 (Augustine's "worship and honour" in `interpretations.md`) | Repaired by research; confirmed by research review 0 |
| RES-014, RES-015 (lagging scope statements; "whether their purpose was known") | Repaired by research; confirmed |
| HOM-001, HOM-002 (the aside beside Mark 10:45; Ps 96:8 "not sung") | Cleared; confirmed by homily review 0 |
| STU-010, STU-011, STU-012, STU-013 | Repaired or no repair needed in the study; confirmed by study review 0. STU-011's residue is new advisory STU-014. |
| WEB-001 (a production stage named in reader text) | Removed; confirmed by web review 0 |
| VIS-001, VIS-002, VIS-003 (p. 28 paragraph; table row spacing; "life[ to") | Cleared or repaired; confirmed by visual review 0 |
| SYN-004, SYN-005 (a Hilary phrase in Latin only; a rendering count) | Cleared |
| **VIS-004** (the homily's stretched first movement break) | **Open.** The shared `properhomily` environment sets flush-bottom columns for all 17 published homilies, so the fix re-renders every one of them. That is its own reviewed job, and changing it during a run would have staled this run's homily seals. |
| Observation: the generator's `gospel` prefix match | Fixed in `orientation-v2` |
| Observation: no dated witness for a mission observance | The Holy See's message dates the 100th World Mission Day to 18 October 2026; registered. It changes no appointed text, and the Mass for the Evangelization of Peoples stays conditional and unselected. |
| Observations: unmarked psalm numbering; ASCII hyphens | Fixed in `orientation-v2`, except a chronology-corpus title ("Isaiah 40-55"), which the generator prints verbatim |
| Observation: the house-voice screen's missing forms | Fixed (`13423ec4c`) |
| Observation: the three-column table at phone width | Fixed (`6cd55152a`); cleared by web review 0 |

## What became of the sourcing

| Defect | Outcome |
| --- | --- |
| US GIRM chapters II, VII, VIII | II re-read live, byte-identical to its registered state. VII and VIII are registered from Internet Archive captures (2026-06-13, 2026-06-18) that re-fetch byte-identically; the publisher's bot challenge was not bypassed. |
| Dated readings page (Lectionary 145) | Registered from an Internet Archive capture of 2026-03-15. The handoff misstated the earlier registration, which was a direct acquisition. |
| NABRE Psalms and Isaiah introductions | The new states are registered as metadata only (`restricted`). |
| Gelasian (Wilson 1894) and Verona (Feltoe 1896) | Pages 105, 229 and 237 of Wilson are retained as public-domain facsimiles. The whole Feltoe scan (19.9 MB) is retained under the library's retain-locally default. |
| Schuster, Fromage, Honorius read in OCR | Every locus was checked on page images, and all read as the OCR gave them. Retained as public-domain page-image excerpts: Schuster 1927 vol. 3 pp. 182–185, and Fromage, *The Liturgical Year* XI (1883, catalogued under Guéranger's work) pp. 472–485. Honorius, *Gemma animae* IV.49 and IV.92–94, was read in the registered restricted facsimile of the 1854 Migne print. The study no longer says Schuster and Fromage were read in a text layer only. |
| World Mission Sunday | Two Holy See pages and the Pontifical Mission Societies page are registered (metadata only) |
| *maiestas* | Checked in Lewis and Short (1879): the title page and p. 1101 are retained. |

## Findings this run raised that stand

Fresh reviews of a revised text find new things. This run's six reviews raised
no blocking finding and 13 advisories, which stand in the leaf's
`evaluations/blocking-findings-v1.toml` with 8 observations:

- **Research records:** RES-016 (Aquinas's lemma reads *malitia*), RES-017
  (Bellarmine's referent), RES-018 (the Chrysostom and Augustine sentences
  are not quoted), RES-019 (statements made stale by this run's own
  re-reads), RES-020 (the Ordo's no. 146 titulus), RES-021 (the 1 Par 16
  parallel).
- **Study:** STU-014 (Augustine's side of the possession question), STU-015
  (bare Vulgate psalm numbers against the study's own convention), STU-016
  (two Latin spelling differences at Mt 22:20, not one), STU-017 (the
  antiphon's *Domine*).
- **Concise:** SYN-006 (page 2 lost its pointer to the full evidence when the
  taller v2 rows forced the note out).
- **Homily:** HOM-003 (the note's account of what the speech takes from the
  second interpretation).
- **Web:** WEB-002 (the five-column branches table overflows the desktop
  reading column by about 23 px). This is shared stylesheet work and is
  repaired after acceptance in a separate commit, which leaves the reviewed
  bytes unchanged.

Observations on shared code and data that a later owner should take up:
- The response citation (Ps 96:7b) prints unlabelled after the verses.
- The chronology corpus title prints "Isaiah 40-55" with an ASCII hyphen.
- Psalm 16 lacks the Davidic-attribution binding that Psalm 32 has.
- The Holy See pages return different bytes on different deliveries.
- The house-voice screen misses a closing "claim disclaimed" clause.

Each of the first three changes this leaf's generated page-2 rows, so its fix
needs a new run.

## Host interventions and events

| # | Stage | What |
| ---: | --- | --- |
| 0000 | resolve-context | The dispatch envelope, as in the first run. Every agent stage ran as a fresh Claude Code harness subagent with no inherited conversation, at its packet's declared effort. The driver added the result path, a scratch directory, the checkout, provenance, and the pinned-Markdown note. Its standing instructions were: the driver alone runs git and `advance`, and an installer lists paths and hashes to stage; edit nothing outside the packet's assignment, and record shared-tool defects rather than fix them; keep the GPT leaf closed, even as a precedent. |
| — | install-publication 0 | The host's permission policy refused the installer's `make refresh-release-bindings ADOPT=1 ONLY=…` for the 15 site sources this revision regenerated: the reviewed web Markdown, the document catalogue, the source index and 12 source-edition projections. The installer wrote a BLOCKED result and stopped; the driver did not submit it. The driver put the exact command and its 15 paths to the maintainer, who authorized it. The driver ran it (17 binding changes, 0 stale) and resumed the same installer, which re-verified every gate and seal and rewrote its result as PASS. Nothing else changed between the two writes. |

**Model provenance.** Every agent stage ran as `claude-opus-5-5[1m]`, the
driver's model, at its declared effort: `high` for authors, derive, build,
web and install stages, `xhigh` for the six reviews. The leaf's
`generation-metadata.tex` declares that model and effort for each author and
derive stage. Three further subagents, outside the workflow, built the
shared-tool commits before seeding, each as `claude-opus-5-5[1m]`:
- `orientation-v2` and version 12, at `high`;
- the preflight checks, at `high`;
- the stylesheet, at `medium`.

All web, probe, install and gate commands ran under a scratch virtual
environment pinned to Markdown 3.10.3.

## After acceptance

On the maintainer's earlier explicit confirmation for this kind of update,
the driver refreshed the Claude publication inventory (the leaf's ten source
categories are unchanged). It also re-pinned the source-family ledger's
catalog snapshot; the ledger has no families.
