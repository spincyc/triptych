# Every cycle the Claude All Saints revision entered

Run `450355254538c1ba`, `proper-study` v15, provider `claude`, identity
`liturgy/roman-rite/1962/propers/temporal/f02-all-saints`, date 2026-11-01,
audience "adult parish assembly", research handoff
[`HANDOFF.md`](HANDOFF.md). Seeded at `4f52b9ade`. Terminal disposition
**ACCEPTED**, with no escalations: 52 packets, 52 accepted results, 1
recorded intervention. The engine's record is archived in the leaf under
`evaluations/proper-study-results/450355254538c1ba/`, written by
`tools/proper-study-run-archive --redact-repository-paths`, beside the first
run's `427e2f58bb897a16`, whose account is
[`../claude-1962-f02-production-2026-10-27/CYCLES.md`](../claude-1962-f02-production-2026-10-27/CYCLES.md)
and which is not evidence for this run. This file is the driver's account of
why the run went round and how its workers were dispatched.

On 27 October 2026 the maintainer asked that the Claude All Saints be
repaired on the Claude model before Sunday 1 November 2026, because part of
the first run had been served by a different model, kimi-k3, and credited to
the Claude model. The handoff carries over only leads; the research was
rebuilt from the sources and every document and review was made again. No
stage opened any GPT-provider file or record for this identity.

## Who did the work

Every agent stage whose result the engine accepted ran on `claude-opus-5-5`,
in a fresh session with no inherited conversation, at the reasoning effort
its packet declared (`high` for authors, `xhigh` for reviews).

- **Scope gate through study-preflight 0** (resolve-context, research 0–3,
  source-registration 0–3, research-review 0–3, author-study 0, and the
  program gates between them): each worker was a non-interactive Factory
  Droid session started with the model pinned to `claude-opus-5-5` and the
  packet's effort, under a watchdog that stopped the worker if any message
  in its session log came from another model. A result was accepted only
  after its whole session log showed the Claude model alone.
- **One rejected attempt.** The first research 0 worker was switched by the
  host to kimi-k3 eighteen minutes in, although the model was pinned. Its
result was never given to the engine, and its files were moved out of the
leaf: `research/context.md` went back to the resolve-context worker's
  last write, `proper-components.toml` to the seed commit, and the other
  research and `propers/` files it had written were removed. Research 0 was
  then dispatched again. The coordinating session that did this was itself
  on kimi-k3 at that moment; it made no other change, and the restoration
  was checked on the Claude model the same evening and again, against the
  session logs, on 28 October.
- **One set-aside result.** The first study-review 0 worker wrote its result
  on the Claude model, but the closing message of its session was served by
  kimi-k3. That result was set aside unread and study-review 0 was
  dispatched again.
- **Study-review 0 onwards.** On 28 October the driver became a Claude Code
  session. Every later stage ran as a fresh Anthropic Claude Code harness
  subagent (general-purpose) given exactly the packet, its SHA-256, a result
  path and a private scratch directory, at the packet's effort. The run's
  one intervention records this change of dispatch envelope.
- **Contribution lines.** Workers wrote none. The driver added one line to
  `generation-metadata.tex` for each accepted authoring result, naming the
  stage, iteration and dispatch host; reviews, builds and installs are
  recorded here and in the archive, not as contributions.

Three workers reported that a repository-wide content search had surfaced
lines from the first run's archive; each said it used nothing from it.

The host carries Python Markdown 3.11, and `requirements-public-alpha.txt`
pins 3.10.3. Every web, probe, install and gate command ran under a scratch
virtual environment built from the two requirements files.

## Where the rounds went

| Stage | Results | Rounds that required changes |
| --- | ---: | ---: |
| research | 4 | — (3 repairs) |
| source-registration | 4 | 0 |
| research-review | 4 | 3 |
| author-study | 2 | — (1 repair) |
| study-review | 2 | 1 |
| derive-synthesis | 3 | — (2 repairs) |
| synthesis-review | 3 | 1 |
| derive-homily | 3 | — (1 repair, 1 re-derivation) |
| homily-review | 3 | 1 |
| build-artifacts | 2 | 0 |
| visual-review | 2 | 1 |
| every other stage | one per round | 0 |

Seven cycles, each a real defect that a cold reviewer found. No seal went
stale: nothing the research seal covers changed while the run was live.

## The cycles, in order

| # | Stage that found it | Owner | What it was |
| --- | --- | --- | --- |
| 1 | research-review 0 | research | RES-001 to RES-008: the reception record was not passage by passage; the Introit and Offertory expositors were unread; the Durandus Collect wording was wrong; editorial joins were unmarked; chronology place phrases were unsourced; the 1962 Missal's p. 16 direction on the Preface was unrecorded. |
| 2 | research-review 1 | research | RES-011 to RES-013: Rabanus and Hilary on Mt 11:28 were held but reported not found, because literal searches fail on double-spaced OCR text (replayed whitespace-tolerant); the "Rome 1920" Missal text was not a typical edition and was redated to 1951–54. |
| 3 | research-review 2 | research | RES-015: *intercessionibus* is not the older Collect form; the Leonine (Feltoe 1896) and Gelasian (Wilson 1894) read *intercessoribus*. The research now records both readings without priority. |
| 4 | study-review 0 | study | STU-001 to STU-008: a repeated formula marking inferences; closing sections assigning invented roles to lightly used texts; Fathers credited with the study's thesis; a comparison row contradicting the interpretations; Chrysostom's "golden chain" given as a ladder; quotations repeated in full; meta-labels in headings; production talk about the translation register. |
| 5 | synthesis-review 0 | synthesis | SYN-001: the concise commentary followed the study's structure and wording (56% of its prose in copied eight-word runs) instead of setting the interpretations side by side at the texts they share. Rewritten around three shared questions. |
| 6 | homily-review 0 | homily | HOM-001 to HOM-004: the Gospel's qualifiers ("in spirit", "after justice") were dropped; Augustine was reported as granting the objector's point, which he refuses; the close handed each step to an authority too quickly to follow; a "went without … did not go without God" refrain. |
| 7 | visual-review 0 | synthesis | VIS-001: the concise study's page 9 carried the next section's running head. A guard before the apparatus fixed it; the concise and homily were reviewed again and the documents rebuilt. |

## What became of the twelve study findings of the first run

The first run's study review used the ids STU-001 to STU-012; this run's
study review reused STU-001 to STU-015 for new findings. This table uses the
handoff's ids; the later tables use this run's.

| Finding | Outcome |
| --- | --- |
| STU-001 (Victorinus; a second witness on Apoc 7) | Resolved. Victorinus is read at 7:2–9 and 12:6 with the recension caution (`research/scope.md` 3.4; `sections/20-sealed-number-uncounted-crowd.tex`). The second witness is the anonymous PL 35 *Expositio*, read on page images at cols. 2425–2426. Caesarius of Arles is recorded as a negative: no Apocalypse homilies are held under his name. |
| STU-002 (each interpretation reads the whole Mass) | Resolved. Each interpretation has a section on the remaining texts that names every element. Texts an interpretation uses lightly get a descriptive clause only, which this run's advisory STU-013 leaves standing. |
| STU-003 (the two-and-six tense pattern credited to four Fathers) | Resolved. The pattern is stated as an observation on the text, and each Father has his own position: Augustine "can indeed be fulfilled", Chrysostom "both here and there", Aquinas "begun", Hilary "changed by immortality". |
| STU-004 ("Bellarmine alone keeps a temporal sense") | Resolved. Aquinas, *Super Ps.* 33 n. 10, stands beside Bellarmine with "Item Deus quaerentibus se subvenit in necessitate" (`sections/40-no-want-just-in-gods-hand.tex`). |
| STU-005 (Fathers credited with the study's synthesis) | Resolved. Each interpretation's opening credits each author with his own clause and states the thesis once, as the study's; confirmed by this run's study review 1. |
| STU-006 (the study narrates its procedure) | Resolved. No narration of the study's procedure remains in the body; inferences are marked where they are drawn. |
| STU-007 (closing maxims; antitheses against positions nobody holds) | Mostly resolved. Four emphasis sentences and one denial of a link the study does not draw remain; they are this run's advisories STU-014 and STU-015(b). |
| STU-008 (Apoc 7:11 misread) | Resolved. The angels fall on their faces (`sections/20-sealed-number-uncounted-crowd.tex`; `sections/00-opening.tex`). |
| STU-009 (why the Communion repeats three beatitudes) | Resolved. Fromage's reason is quoted in French and rendered in the study's prose (`sections/30-beatitudes-way-of-the-saints.tex`). |
| STU-010 (the Offertory's history told twice) | Resolved. It is told once, in the Offertory note; the scope appendix gives only its source bound. |
| STU-011 (St Bernard not read) | Resolved. PL 183 and a work record for the All Saints sermons were registered, and the study cites sermon 1 nn. 9, 13–15 and sermon 5 nn. 2–3, 5. No English translation before 1931 is registered; reported to the library owner. |
| STU-012 (a finer locus for *Super Matt.* 5) | Resolved. Venice 1745 pp. 67 and 72 are cited, with a plain account of what Aquinas reports from Chrysostom. |

## What became of the research leads and other handoff points

| Lead or point | Outcome |
| --- | --- |
| Fromage on the Communion | Resolved. The French is quoted and the English rendering is not put in quotation marks. |
| Victorinus on 7:2 | Resolved. Elias as precursor and the number joined to the multitude are given; the remark about order is recorded as concerning the trumpets and phials and is not applied to the sealing. |
| Bellarmine on Ps 33:10–11 | Resolved: "essence of perfection", the Supreme Good and the humbler temporal sense. The added "he says nothing of the vision of God" is this run's advisory STU-015(b). |
| Aquinas, *Super Matt.* 5, Venice 1745 | Resolved by page (pp. 67, 72); the References add the Corpus Thomisticum text for the lecture number. |
| Hilary (*scilicet*; change by immortality) | Resolved. |
| Six orations, not seven | Resolved. |
| Cyprian kept out of the paragraph on Bede | Resolved. |
| Augustine on Ps 118:109 | Not applicable: the verse is not cited. |
| Register (production words, repeats, fixed formulas) | Resolved in the study. The concise study still repeats about ten points (this run's SYN-006). |
| Lead 1, the Victorinus containment bound | Resolved in the research by reading chapters 7 and 12. The bound in `src/sources/inventories/source-containment-v1.toml` is unchanged and is reported to its owner. |
| Lead 2, the 1570 Offertory, *malitiae* and *alleluia* | Resolved. 1570 reads *mortis*; 1604, 1862, 1889 and 1909 read *malitiae*; the *alleluia* is first found in Mame 1922, and 1909–1922 is unread. The "Rome 1920" witness was redated to 1951–54 (RES-013). |
| Lead 3, the Offertory against the Clementine Wis 3:1–3 | Resolved by collation. |
| Lead 4, Psalm 33 numbering | Resolved: Vulgate numbering with the Hebrew in parentheses, stated once. |
| Lead 5, Pustet 1862 | Resolved: read at 400 dpi, collated and bound. |
| Lead 6, Mame forms | Resolved. |
| Lead 7, Bede's order on 7:9 | Resolved. |
| Lead 8, chronology sources | Resolved: each cited source is named and recorded as read. |
| Lead 9, Lasance orations | Resolved: both artifacts are bound and have disposition rows. |
| Lead 10, dated web ordos | Mostly resolved. The ICRSP, FSSP and FSSPX ordos were fetched again and compared by hash; FSSPX matches its record, ICRSP differs from it. The study uses the ICRSP Trinity direction only as one institute's. The ICRSP record is declared in `research/review-dependencies.toml` but not bound. |
| Lead 11, the Preface | Resolved: both candidates named with their rubrical basis, neither asserted. |
| Lead 12, Augustine on Ps 32:12 | Resolved. |
| Lead 13, carrying authors | Resolved: the manifest and `research/interpretations.md` §5 agree. A note in §6 about Rabanus is now out of date. |
| Lead 14, the PL 35 *Expositio* | Resolved: bound with column loci and a disposition row. It has no work record; reported to the library owner. |
| Lead 15, Bernard | Resolved; see STU-011. |
| Lead 16, records hygiene | Resolved for paths. The opening of `research/production-review.md` still describes the first run (observation below). |
| Concise study and homily points | Resolved, except the standing advisories SYN-006 and HOM-011 below. |
| Layout: the last page held only the colophon | Resolved. |
| Layout: the opening map split 13/1 | Accepted (VIS-004). |
| Layout: chronology notes and "Revelation" | Notes resolved. "Revelation 7:2–12" and "Matthew 5:1–12" still print from the generator, which the leaf cannot edit. |
| Layout: running heads | The concise study's case was repaired in the leaf (VIS-001); the shared defect is reported to the format owner. |
| Left for others (calendar ranges and Preface case, the appointments test, oration ledgers, `author-standing-v1.toml`, the FSSPX ordo language, Bede passage records for 7:2–3) | Still standing; reported in `research/scope.md` §10. |

## Findings this run raised that stand

Every blocking finding this run raised was repaired. These advisories and
observations stand:

| Finding | Owner | Standing |
| --- | --- | --- |
| RES-018 | Research | The Collect search claims every tracked text file but skipped TOML records. |
| STU-013 | Study | Each interpretation's last element section ends in bare clauses on texts it does not use. |
| STU-014 | Study | A few sentences announce that a point is hard or a difference real before stating it. |
| STU-015 | Study | Aquinas's objection called "of St Paul"; "he says nothing of the vision of God"; "the Fathers do not divide" overstates the record; retrieval reasons in the scope appendix. |
| SYN-004(b), VIS-005 | Both studies | Four rows of the date-location table name no place and do not say the place is unknown. |
| SYN-005 | Concise study | Three framing clauses go beyond their sources. |
| SYN-006 | Concise study | About ten points from pp. 3–4 are repeated in the commentary. |
| SYN-007 | Concise study | "The promise is harder." announces the difficulty. |
| SYN-008 | Concise study | The concise study does not say how the three answers stand to one another. |
| HOM-009 (remaining part) | Research and both studies | The physician answer at *In Ps.* 33 n. 10 is Augustine's, as Aquinas reports it (*De serm. Dom.* II.17.58). The homily says so; the research and both studies still credit it to Aquinas. |
| HOM-011 | Homily | "Beatitude" is used both for the Gospel's sayings and for Bernard's "our whole beatitude". |
| VIS-002 | Study | The nested closing quotes of the Aquinas quotation on p. 16 are misordered. |
| VIS-004, VIS-006 | Study | Accepted: the opening map's last row on p. 4; the third interpretation's four senses split two and two across pp. 24–25. |
| Observation | Research | `research/scope.md` and `research/interpretations.md` call Chrysostom's image a "ladder"; it is a "golden chain" (Hom. 15.9). The study is correct. |
| Observation | Production record | The opening of `research/production-review.md` still describes the first run. |
| Observation | `author-standing-v1.toml` owner | No rows for Bernard, Bonaventure, Alphonsus, Cyprian, Victorinus, Bruno of Würzburg or Peter of Celle, so the study cites them in support only. |
| Observation | Chronology generator and corpus owners | Generated cells print "Revelation" and "Matthew 5:1–12", and hyphens in two Wisdom ranges. |
| Observation | `src/common/propers-format.tex` owner | `\runninghead` marks the page before a section that moves to the next page. |
| Observation | `tools/source-library` owner | Phrase search is literal per line, which misses phrases on double-spaced text layers. |
| Observation | Source-library owner | Several excerpt records are not named in their work records; Wilson 1894 sits under two works; Feltoe has no text artifact. |

## A shared tool fixed after acceptance

`tools/proper-study-run-archive` refused this run: its privacy audit read a
TeX thin space quoted in a packet's JSON findings line (`\\,`, as JSON
escaping writes it) as the start of a UNC path. Commit `b38044fe8` makes the
audit decode JSON header values before checking them, with tests; the run
then archived. The fix landed after the run was accepted, so no seal was
affected.

## Publication

Publication is recorded in `PROJECT-WORK.md` and, once verified, in
[`deployment-evidence.json`](deployment-evidence.json).
