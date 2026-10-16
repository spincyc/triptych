# Every cycle the Claude Twenty-ninth Sunday production entered

Run `4d16b5e19d25dad9`, `proper-study` v11, provider `claude`, identity
`liturgy/roman-rite/postconciliar/roman-missal-third-edition-en-us-2011/propers/temporal/pc-s55-twenty-ninth-sunday-in-ordinary-time-year-a`,
date 2026-10-18, audience "adult parish assembly". Seeded at the
authorization commit `fd99f7289`. Terminal disposition **ACCEPTED**, with no
escalations: 33 packets, 33 accepted results, 1 intervention. The engine's
own record is archived in the leaf under
`evaluations/proper-study-results/4d16b5e19d25dad9/` by
`tools/proper-study-run-archive`. This file is the driver's account of why the
run went round, which the run directory does not state.

The GPT leaf for the same identity was published on 2026-10-14. This run is
an independent Claude production under its own edition tree: no stage opened
that leaf or its workflow records. Three workers disclosed that a
repository-wide search or listing printed a GPT file name or line; each used
nothing from it.

## Where the rounds went

| Stage | Results | Failing rounds |
| --- | ---: | ---: |
| research-review | 3 | 2 |
| study-review | 2 | 1 |
| synthesis-review | 2 | 1 |
| homily-review | 1 | 0 |
| visual-review | 1 | 0 |
| web-review | 1 | 0 |
| every gate | one per round | 0 |

Four cycles in all, which are the run's non-PASS transitions. No stage came
near its iteration budget, no finding was raised twice, and every program
gate passed at its first attempt.

## The cycles, in order

| # | Stage that found it | Owner | What it was |
| ---: | --- | --- | --- |
| 1 | research-review 0 | research | Four blocking findings. RES-001: Schuster and Fromage both give Ps 16:6 *Ego clamavi*, this formulary's Entrance antiphon, as their Communion; the research recorded the Communion as not read and the formulary as sharing only the Gospel. RES-002: a generated orientation row gave the Gospel acclamation, Phil 2:15d, 16a, an "Event: date unresolved" relation, and the record explained the cause wrongly. The cause is a shared-tool prefix match: `orientation_rows` in `scripts/_proper_chronology.py` tests `element.key.startswith("gospel")`, which catches the key `gospel-acclamation`. RES-003: interpretation 3 set Augustine against Chrysostom on a point their cited passages share. RES-004: the page-2 place phrases had no research behind them (1 Thessalonians: the Athens subscription against Corinth). Research iteration 1 repaired all four. For RES-002 it re-keyed the leaf's acclamation element `acclamation` in the manifest, `verified.md`, `context.md` and the chronology inputs, and recorded the tool defect for its owner rather than editing a sealed input. |
| 2 | research-review 1 | research | RES-009: interpretation 3's turning difficulty said the questioners of Mt 22:15 "consulted openly", where the text says they took counsel among themselves, and `scope.md` §3.1 credited Chrysostom, Hom. 70.1, with the opposite of his premise. Research iteration 2 corrected both and cleared the four advisories RES-010 to RES-013, marking the *maiestas* lexical claim unverified because the library holds no Latin lexicon. Research review 2 passed with two advisories. |
| 3 | study-review 0 | study | Three blocking findings. STU-001: about forty-five sentences narrated the study's own caution ("the join is the editor's", "nothing is claimed here", disclaimers that a text was designed). STU-002: the study gave Augustine's psalter as reading "worship and honour", where his Latin has *gloriam et honorem* and "worship" is the NPNF translator's word. STU-003: one comparison cell credited four Fathers with the editor's Cyrus–Caesar link. The reviewer accepted the same Augustine error in `interpretations.md` as STU-004, so research did not reopen. Author-study iteration 1 repaired all three and cleared STU-005 to STU-009. Study review 1 passed with four advisories. |
| 4 | synthesis-review 0 | synthesis | SYN-001: the concise References listed four loci the concise never uses: Ps 145:2, Augustine on Ps 95.5 and on Ps 118 (Schin), and Aquinas's *Postilla* on Ps 16. The synthesis preflight checks References at the level of the whole work, so it passed them. Derive-synthesis iteration 1 removed them and cited GIRM 61 and 62 where two relations rest on them (SYN-003). It answered SYN-002, bare Latin without English, by replacing most Latin with the expansive study's English, because a proof that set English beside every Latin phrase ran to 12 pages. Synthesis review 1 passed with two advisories. |

Each was a real defect that no mechanical gate caught. Cycle 4 points at a
gate: the References check counts loci across the whole leaf, so a concise
bibliography can carry entries the concise never uses. Cycle 3's STU-001 points
at another. The house-voice screen passed iteration 0's self-narrating
sentences, and the reviewer recorded the missing lexical forms as an
observation.

## Findings that did not gate

Across ten cold reviews the run raised 9 blocking findings, 28 distinct
advisories and 3 accepted findings. Those that stand are in the leaf's
`evaluations/blocking-findings-v1.toml`: 13 advisories, 3 accepted findings
and 6 observations. The driver adds no findings of its own. Three classes are
worth a first revision:

- **The research records lag the reviewed studies (STU-004, RES-014,
  HOM-002).** `research/interpretations.md` still carries the "worship and
  honour" parenthesis that STU-002 removed from the study. `scope.md` §8.3,
  lead 8 and the Souvay binding describe an earlier reading state.
  `scope.md` §2 says Ps 96:8 is "not sung" where every other record gives
  the verse whole. No stage after research review may write research records,
  and the three documents follow the sources at each point.
- **Reader-facing wording (STU-012, WEB-001, VIS-001, VIS-003).** The scope
  appendix's whited-wall sentence can be misread as aimed at Jews when its
  target is the Donatists. The same appendix names a production stage in
  reader text ("at the stage that resolved this Sunday's context"). The
  comparison's closing paragraph sits alone at the top of study p. 28. A
  bracket in the appointed texts reads "life[ to my glory" because
  `\notread{ to my glory…}` opens with a space.
- **Generated chronology rows.** The orientation generator prints input refs
  verbatim: ASCII hyphens in verse ranges, and Vulgate and Hebrew psalm
  numbering side by side with no marker. The site's dossier rules lay this
  three-column table out on the four-column phone grid. All of this is shared
  generator and stylesheet behaviour, outside this leaf.

## Host interventions and events

| # | Stage | What |
| ---: | --- | --- |
| 0000 | resolve-context | The dispatch envelope. Every agent stage ran as a fresh Claude Code harness subagent with no inherited conversation, at exactly the effort its packet's `EFFORT` line declares, through the harness's per-dispatch effort control. Each worker received its packet by exact path and SHA-256 and read it in full. The driver added only the result path, a worker-owned scratch directory, the checkout path, the model identity and effort for the generation record, and the pinned-Markdown host note with the scratch virtualenv's path. It also said that the driver alone runs git and `advance`, that nothing outside the packet's assignment may be edited (no tool, script or registry, because the research seal covers them), and that the GPT leaf for this identity and its workflow records stay closed. Applying those last two, research 1 and 2 were told to repair what their stage owns when a finding traces to a shared tool and to record the defect. From visual review on, workers were told not to open the GPT leaf even as a layout precedent. |
| — | install-publication 0 | The packet requires the installed web Markdown staged before `publication-gates`. Git was reserved to the driver, so the installer listed the path and hash instead. The driver checked the bytes against the reviewed conversion (`f7b4a079…2a40`) and staged them before running the gate. |
| — | web-review 0 | The host's permission policy refused the reviewer's run of `scripts/_proper_study.py seal`. The reviewer checked the artifact's bytes against `REVIEW_INPUTS` and `web-artifact.json` instead, and regenerated identical bytes from the current sources. |
| — | research 0 to 2; research-review 1 | The United States GIRM chapter pages, and later the dated readings page, returned HTTP 403 on re-read. Research registered the three chapter states the context stage had read, under the hashes it recorded, and the records say so. Research review 1 re-fetched and hash-matched chapters II and VII; chapter VIII and the dated readings page stayed unavailable. |
| — | after ACCEPTED | The host's permission policy refused the installer's refresh of the Claude publication inventory, a shared record that is not part of the terminal gate. The driver's own refresh, with the leaf's classification row, waited for the maintainer's explicit confirmation. |

**Model provenance.** Every agent stage ran as `claude-opus-5-5[1m]`, the
driver's model, at its declared effort: `high` for the author, derive, build,
web and install stages, `xhigh` for the ten reviews. The leaf's
`generation-metadata.tex` declares that model and effort for each author and
derive stage. Build, web and install stages changed no rendered source and
declare nothing.

The host carries Python Markdown 3.11, and `requirements-public-alpha.txt`
pins 3.10.3. Every web, probe, install and gate command therefore ran under a
scratch virtual environment built from the two requirements files. Before the
run, the checkout's `pdf/` tree was compared with the live site's
`SHA256SUMS`, and no published PDF was missing.

## What this run leaves for the owner

| Item | Evidence | Why it is not done here |
| --- | --- | --- |
| `orientation_rows` in `scripts/_proper_chronology.py` (about line 1465) gives any element keyed `gospel…` a narrated-event row, `gospel-acclamation` included. This leaf avoided it only by re-keying, and no generator test covers it. | RES-002; research-review observation | A sealed shared tool; changing it during a live run stales every live research seal |
| The synthesis References check counts loci across the whole leaf, not per document | SYN-001 | A shared check; the concise was repaired by hand |
| The house-voice screen misses the forms "the editor joins", "the interpretation does not" and "No commentary on" | study-review observation | A shared check |
| The orientation generator prints ASCII hyphens in verse ranges and mixes Vulgate and Hebrew psalm numbering without a marker. The phone-width dossier rules do not fit its three-column table. | visual-review and web-review observations | Shared generator and stylesheet |
| The research records lag the reviewed studies (STU-004, RES-014, HOM-002), and the scope appendix carries the STU-012 and WEB-001 wording | `evaluations/blocking-findings-v1.toml` | Only a research or study stage may write them, and reopening research reruns every document and review |
| The GIRM chapter VIII state and the dated readings page are registered from the context stage's hashes, not re-read. The NABRE Psalms introduction and the Gelasian and Verona page images were read in unregistered states. | research 0 to 2 notes | Server refusals and shared source-library work |
| No dated witness was sought for a mission observance on 18 October 2026, so that branch stays conditional and unsupplied | research-review observation | Calendar data outside this leaf |
