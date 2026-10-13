# Historical orientation and reader value, 12 October 2026

## Evidence and scope

The maintainer requested clearer date/location/occurrence tables, an examination
of recent GPT research, pedagogy and elegance, and completion of the 1962
Twenty-first Sunday after Pentecost for 18 October 2026. The initial audit used
the published GPT `59`, `60`, `PC-S53-A` and `PC-S54-A` families from
28 September through 6 October. It read all four concise chronology pages and
selected study, homily and research passages, with full-size review rasters for
the two most recent tables. This is an editorial comparison, not a new
verification of every source or a controlled comparison of model capability.

## Findings and disposition

| Observed defect | Cause | Required result |
| --- | --- | --- |
| `60`, concise p. 2: the Offertory date cell carries a long authority list, a pending-verification statement and several methodological sentences. | The generated annotation and its governing chronology contract require the complete evidence display inside a narrow date cell. | Separate the concise reader projection from the lossless evidence; keep necessary uncertainty visible in short form. |
| `60`, concise `03-chronology.tex`: the Psalm 118:1 Introit-verse row displays the composite Daniel-and-Psalm element's nonuniform-date message. | The element key is treated as the reader row's identity. | Bind each generated row to its actual passage scope and dated subject. |
| `PC-S54`, concise `synthesis-03-chronology.tex`: the long and short Gospel repeat the same six composition alternatives. | Overlapping appointment is treated as independent chronological information. | Consolidate identical answers while naming both appointments and distinguishing the dated literary objects. |
| Ministry eras and Psalter-wide composition bounds require prose explaining that they do not date the passage. | A generic date field obscures the date's subject and reach. | Name event, attribution/ministry and composition beside their own values. |
| Older `59` and `PC-S53` pages expose internal profile keys and the unexpanded month/day `01-14`. | Reader rendering does not consistently translate machine representation into reader language. | Guard new projections against opaque keys and preserve a named calendar for dates without a year. Historical snapshots are not restamped. |
| Tables fit but require reading tall blocks down one column to recover a simple answer. | Pagination acceptance substitutes for lookup usability. | Review the actual passage-to-occurrence/place/date lookup at ordinary reading size. |

The audit also found substantial strengths. In `59`, Augustine's elimination of
insufficient candidates for the wedding garment and Gregory's account of the
Bridegroom's love give different reasons for charity. In `60`, the father's
request that Jesus travel and Jesus' direction that the father travel make the
faith argument concrete; Gregory's imperfect believer and Augustine's initially
unbelieving petitioner remain distinct. In `PC-S54`, Gregory identifies the
present Church because expulsion cannot characterize the completed heavenly
feast. These are examples of useful reasoning, not merely names supporting a
theme. The sampled evidence does not justify a blanket verdict of shallow
research.

The repeatable teaching risk is loss of this specificity through recurring
general conclusions about grace, charity and fruitful reception. The remedy
belongs in selection and exposition: follow a consequential textual difficulty,
show each checked witness's inference, and teach what changes when that answer
is accepted. It does not require additional saints, invented disagreements or
more pages. The concise commentary must deepen its thematic opening instead of
repeating it.

## Implementation and validation

The schema-2 `orientation-v1` projection generates complete three-column rows:
passage, occurrence and place, and date. The author supplies a sourced short
place/context phrase; the generator owns the passage scope, dated subject,
relation and complete alternatives. Equal answers share a row, while the two
parts of a composite Introit retain their own answers. Row identities include
their exact passage coverage so a changed appointment cannot silently inherit
old geography. Detailed annotations remain available for the same family's
expansive historical appendix.

Optional source-owned titles, relative-date wording and qualifications remove
audit prose without changing underlying dates, profiles or source status.
The Exodus label now names the Temple as the interval's other end. Reported
Ussher figures retain their attribution; the David-at-Geth figure is attributed
to the Haydock edition's apparatus, not personally to its commentator. The
Esther source's conjectural early hypothesis and allowance of a later date
remain visible. Source inspection did not support narrowing that article's
whole-book hypothesis to Hebrew Esther or inventing a replacement date for the
Greek additions.

The owning profiles and proper-study v10 require the new presentation and the
passage-level reasoning and reader tests above. No stage order, declared effort,
source requirement or document extent was relaxed. New tables use 9.5-point type
on 11.5-point leading. Layout proofs of TLM `60`, TLM `61` and postconciliar
`PC-S54-A` each occupy one page with no layout warnings. These are layout proofs,
not reissued historical publications or accepted research for the new Sunday.

Validation before production:

- 176 focused and full web-conversion tests passed with the repository's bound
  Python Markdown 3.10.3 dependency. The earlier broad 609-test run exposed the
  local Markdown 3.11 mismatch, the semantic-manifest refresh required by the
  new metadata, and the existing missing Cyril of Alexandria author-registry
  entry in Claude `60`. The relevant web suite and manifest check pass after
  their respective corrections. The Cyril test, registry, loader and all proper
  manifests are unchanged from `3c5d403f5`; no unrelated registry ruling was
  added to this task.
- Fifty proper-study workflow tests passed. `make check-sources`, chronology
  currency, semantic-manifest currency, the tool registry, promised-deliverable
  validation and `git diff --check` passed. The semantic manifest was regenerated
  from its unchanged pinned base; no historical acceptance was renewed.
- An independent comparison against `3c5d403f5` found no generated record or
  annotation changes across all 19 existing dossiers. Fifteen older stored
  artifacts were already stale under both implementations; that existing drift
  was not hidden by rewriting them.
- An independent disposable `61` lifecycle exercised the real CLI write and
  currency checks, then the actual v4 research seal, before and after adding
  the component manifest. The generated artifact and complete 1,617-file seal
  stayed identical. Tampering with the annotation was refused.
- Independent conversion of the real shared table environment, generated-file
  import and schema-2 anchors preserved all 33, 27 and 33 rendered cells in the
  `60`, `61` and `PC-S54-A` proofs respectively, with no internal IDs exposed.

The independent final review found no remaining implementation blocker. Its
[report](FOUNDATION-REVIEW.md) and [reviewed file hashes](reviewed-state.json)
are retained here. It independently rechecked the derived-date marker,
research-pending occasion wording and reporting-exception attribution fixes,
ran 21 orientation tests, repeated the 19-dossier comparison, and inspected all
three final visual proofs. Illustrative locations in these proofs remain
unaccepted research examples.

The new Sunday's first actual production, `a72731c5491066a3`, passed research,
all three content reviews and the all-page visual review, then ended honestly
`BLOCKED` at canonical web conversion. All seventeen explicit schema-2 source
anchors were missing. The exact same late failure is documented in the GPT
`PC-S54` production of 6 October. The web guidance already states the
requirement; study authoring and preflight did not enforce it before accepted
sources became frozen. This is a separate, repeatable workflow defect exposed
by the real case. The corrected contract adds explicit author instructions and
an actual converter probe before cold study review, returning failures to the
study author. Version 11 changes only the pipeline, author fragment and
operator instructions, with focused regression tests; the converter and engine
remain unchanged. Twenty-nine implementation checks passed. The separate
[independent review](anchor-preflight/report.md) passed with no open findings
after nine new regression tests, 197 existing checks and two additional native
probes. It verified failure routing, missing/rendered-away anchors, dependency
failure, absent future companions and refusal to treat stale output as success.
The historical foundation review above is not restamped.

The engine has no supported resume or upstream route from a linear-stage
`BLOCKED` result. The first run's native evidence remains intact in the
[terminal archive](../gpt-1962-61-production-2026-10-12/run-a72731c5491066a3/README.md).
A replacement run must independently inspect reused research and manuscripts
and obtain fresh stage verdicts. Production completion remains pending.
