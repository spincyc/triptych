# GPT PC-S53-A production record

This archive records the production of the U.S. postconciliar Twenty-seventh
Sunday in Ordinary Time, Year A, for 4 October 2026 and an adult parish
assembly. Its canonical owner is
`src/gpt/liturgy/roman-rite/postconciliar/roman-missal-third-edition-en-us-2011/propers/temporal/pc-s53-twenty-seventh-sunday-in-ordinary-time-year-a/`.

## Identity and current state

- Workflow: `proper-study`, version 7.
- Workflow digest: `9c0b654d981692c0a1d4592beae5a00764180378d63ba80185d3ce7a23f5be38`.
- Run: `17099e79f3655b7d`.
- Seed commit: `264879369f1710eb0600a74836cedc62abd1ff28`.
- Final engine state: **ACCEPTED**, with no escalations. All three PDFs and the
  canonical web edition are installed with their accepted bytes. This is
  repository installation and workflow acceptance, not a deployment claim.

The seed remains the seed when later unrelated commits advance the branch.
The engine-recorded packets and results are copied byte for byte and checked
against its recorded hashes. Each checkpoint preserves the exact state and
event stream then observed, with a separate archive manifest. A dispatched
packet without a result is pending work, not a completed stage.

## Completed cycles

| Stage | Iteration | Execution | Recorded outcome |
| --- | ---: | --- | --- |
| Scope gate | 0 | Program gate | PASS |
| Resolve context | 0 | Fresh Codex worker, high | PASS |
| Research | 0 | Fresh Codex worker, high | PASS |
| Research preflight | 0 | Program gate | PASS |
| Research review | 0 | Fresh cold Codex reviewer, xhigh | CHANGES_REQUIRED |
| Research repair | 1 | Fresh Codex worker, high | PASS |
| Research preflight | 1 | Program gate | PASS |
| Research review | 1 | Fresh cold Codex reviewer, xhigh | PASS, no findings |
| Author study | 0 | Fresh Codex worker, high | PASS |
| Study preflight | 0 | Program gate | PASS |
| Study review | 0 | Fresh cold Codex reviewer, xhigh | PASS, STU-001 advisory |
| Derive synthesis | 0 | Fresh Codex worker, high | PASS |
| Synthesis preflight | 0 | Program gate | PASS |
| Synthesis review | 0 | Fresh cold Codex reviewer, xhigh | PASS, SYN-CIT-001 advisory |
| Derive homily | 0 | Fresh Codex worker, high | PASS |
| Homily preflight | 0 | Program gate | PASS |
| Homily review | 0 | Fresh cold Codex reviewer, xhigh | PASS, no findings |
| Build artifacts | 0 | Fresh Codex worker, high | PASS |
| Artifact gates | 0 | Program gate | PASS |
| Visual review | 0 | Fresh cold Codex reviewer, xhigh | PASS, VIS-001 accepted |
| Generate web | 0 | Fresh Codex worker, high | PASS |
| Web review | 0 | Fresh cold Codex reviewer, xhigh | CHANGES_REQUIRED, WEB-001 |
| Generate web repair | 1 | Fresh Codex worker, high | PASS, WEB-001 reported repaired |
| Web review | 1 | Fresh cold Codex reviewer, xhigh | PASS, no findings |
| Install publication | 0 | Fresh Codex worker, high | PASS |
| Publication gates | 0 | Program gate | PASS; terminal ACCEPTED |

Every author and reviewer received its own compiled packet without inherited
authoring conversation. No author supplied the cold review of its work. The
coordinator ran program gates, advanced the engine with exact worker results,
and refreshed the source inventories; it did not author the required reviews.

The first review raised RES-001 for missing controlling ICEL policy records
and the 1854 Honorius transcription ancestry. It also raised advisory RES-002
for source-span endpoints and RES-003 for the local Honorius Mass comparison.
Research iteration 1 changed four local research records, completed the
ancestry, reconciled the spans, and recorded the comparison. Review iteration
1 passed against the fresh seal: 195 evidence files and 16 chronology
computation inputs. The failed review remains in this archive unchanged.

The author-study proof has 21 physical pages and 7,480 substantive words,
excluding reproduced Scripture, the map, apparatus and footnotes. Its SHA-256
is `aeccca67712fc12136f8f5eea370d88387a3a81688487b1733af2f159761ca27`.
The author recorded a settled build, embedded fonts, source-text correspondence
and inspection of all 21 pages. These are author checks, not cold content or
final visual approval. The `study-submitted` checkpoint preserves that boundary.

Cold study review subsequently passed with one advisory, STU-001: the
bibliography calls Alfred Durand's Catholic Encyclopedia article *The
Synoptics*, although its title is *The New Testament*. The exact cited article
and substantive chronology evidence were checked. No blocking finding opened
a study-repair route. The coordinator preserved the advisory and continued the
declared workflow rather than promote its severity, add an extra acceptance
gate or edit sealed content. Any ordinary later reentry into the study owner
can address it. The `study-accepted` checkpoint preserves the actual verdict.

The concise author proof has 11 physical pages and 3,491 substantive words:
853 in Themes and Movement and 2,638 in the developed commentary, excluding
notes, tables and apparatus. Its SHA-256 is
`79372a794f62ba744f508faf5171ef8180bec8c9c23e9474e90a41d6888211cb`.
The settled physical markers place inventory/overview on page 1, chronology
on page 2, themes on pages 3–4, and commentary from page 5. The author recorded
inspection of all eleven pages; the `synthesis-submitted` checkpoint preserves
the proof submission, not a final visual approval.

Cold synthesis review passed, confirming all eleven sealed inputs, all eleven
proof pages and the required physical markers. SYN-CIT-001 records the same
nonblocking Durand bibliography-title issue in the concise apparatus. The
reviewer checked the principal author loci; fresh live NABRE introduction
requests returned 403, recorded as a review access limit. No source was edited
to turn that review into a different verdict. The `synthesis-accepted`
checkpoint records the transition to homily authoring.

The homily author proof has three physical pages and 1,366 spoken words.
At an estimated 115–125 words per minute, delivery would take 10.9–11.9
minutes. This is a word-count estimate and silent textual rehearsal, not an
audible or human timing event. Its SHA-256 is
`b7fd7a87d99b7e7dd7c2b329b61d315854649c4860f14cfc66fd39cf6eafca97`.

A tooling limitation arose in this stage: narrowing the spoken component's
element declaration to the seven then discussed produced
`relation-coverage (homily edition): homily must declare coverage of every element key`.
The packet permits a homily without an inventory of every minor proper.
The author added 88 words of pertinent prayer and explicitly alternative
Communion references within the same gift-and-fruit argument, bringing its
actual coverage to all eleven elements and making the original declaration
truthful. Neither gate nor accepted upstream text changed. The tool/profile
tension remains recorded; cold review must judge the actual speech on its own.

Cold homily review passed without findings. The reviewer independently checked
all seven sealed inputs, the named Augustine, Chrysostom and Aquinas loci,
Scripture and prayer descriptions, all three proof pages and the spoken count.
The review judged the continuous gift-and-fruit argument suitable for the
stated assembly and retained the disclosed source and timing limits. The
`homily-accepted` checkpoint records entry to final artifact building.

Final artifact building made no source or layout changes. The shared final
metadata yields these exact PDFs, also recorded with their render inputs in
the leaf's `research/artifacts.json`:

| Artifact | Pages | SHA-256 |
| --- | ---: | --- |
| Expansive study | 21 | `57ce918f211983e2aef40cc572863f40f79fc4c0400f8bcdaa66bf2ea8a060cf` |
| Concise study | 11 | `f394f3f2081808e8470d416631638c64ef2e18a7fa3d2284c28ba3f6184a1729` |
| Homily | 3 | `b7fd7a87d99b7e7dd7c2b329b61d315854649c4860f14cfc66fd39cf6eafca97` |

Settled logs, extraction, font embedding and concise physical markers passed.
`qpdf` was unavailable; Ghostscript nullpage processing completed without
diagnostics. The artifact gates passed the current content seals and snapshot;
35 page rasters were prepared for fresh visual inspection. The
`artifacts-submitted` checkpoint records this review boundary.

Cold visual review passed after inspecting all 35 pages and four contact
sheets, verifying all sealed hashes and independently regenerating byte-identical
rasters. VIS-001 accepts the sparse final concise page: three complete source
entries, revision timestamp and rights colophon make it a substantive terminal
continuation within the eleven-page limit. No physical print or audible rehearsal
was claimed. The `visual-accepted` checkpoint retains the exact result.

Canonical conversion produced 77,606 bytes with SHA-256
`7d4109999858aab4efb433b0e95df5652edee458450e75c94eb9316a6196dac9`.
The worker checked eleven element anchors, both interpretations, eight sense
entries, 37 footnotes, source links, revision timestamp and rights colophon.
No source or converter repair was made. This is conversion completion, with
the exact bytes submitted for independent review at `web-submitted`.

Cold web review confirmed full text fidelity against the current 21-page PDF,
all 37 source notes and 75 fragment links, but raised blocking WEB-001. The
chronology appendix's generated heading is
`appendix-scriptural-date-and-location`; the site stylesheet recognized only
the two older dossier heading identifiers. Actual Chromium inspection at a
500-pixel viewport found six tables wider than their 437-pixel visible area
(Entrance 473 pixels; Corinthians 523 pixels), with Date content clipped behind
horizontal scrolling. The publication-owned finding requires the existing
responsive dossier presentation and owning test to cover this heading, followed
by regeneration and fresh review. The `web-repair-required` checkpoint preserves
the exact failed review and engine route.

The first browser launch encountered sandbox socket restrictions. Two escalated
capability calls remained pending and were interrupted, not rejected; an
approved direct Chromium invocation subsequently completed the actual browser
checks. No unavailable-browser claim replaced those checks, and no live review
process remained after the worker completed.

The coordinating root's separate tooling lane repaired the shared dossier
selectors and their owning regression check, with the web-edition guidance
updated to name the appendix identifier. It preserved the accepted source,
PDF and converter bytes. The handed-off stylesheet SHA-256 is
`a456caf21041256a1047560c0cee8638a99f7df819e6249ee3345e550b6b4060`.
This is supplementary rendering identity: the existing web receipt seals
Markdown, not the stylesheet. The exact iteration-1 conversion packet was
then dispatched to a fresh worker; renewed independent web review remains
required before installation.

The tooling lane's focused tests passed; the original stylesheet failed all ten
regression checks. Browser evidence covered all eight dossiers at actual
320-, 500- and 1440-pixel CSS widths, both legacy heading identifiers and
ordinary-table controls outside the dossier section. The root independently
inspected the narrow and desktop screenshots. The fresh conversion worker
regenerated identical Markdown, checked the owning heading test and independently
measured all eight dossiers at 500 and 1280 pixels, with focused visual checks.
Its production audit identifies blank long-document captures excluded from visual
claims and a further pending browser approval interrupted before successful
unwrapped Chromium verification. The `web-repair-submitted` checkpoint preserves
the actual repair report and dispatch to a new cold reviewer.

Fresh cold web review passed without findings. It independently checked 137
source paragraphs, all 37 source notes, PDF correspondence and links, and
inspected its own browser output. All eight chronology dossiers fit without
cell overflow at 500 and 1280 pixels with the required responsive modes.
Stylesheet identity remained supplementary to the Markdown seal. No capability
approval or live operation remained. The `web-accepted` checkpoint records
entry to ordinary three-document installation.

Normal Make installation retained every accepted PDF hash and copied the
canonical Markdown byte for byte. Three exact per-publication alpha records,
the Year A ChatGPT four-link catalog cell and single canonical marker, the
deterministic corpus projection, source inventories and scoped site bindings
were installed. Other provider/cycle entries and historical PDF rights
snapshots were preserved. The terminal program gate passed all five checks:
three-document publication, release bindings, target-scoped public-alpha,
document catalog/projection and global web freshness, after immutable review
seal verification. The observed terminal state has no escalations.

`checkpoints/terminal-accepted/` holds the final exact engine metadata and hash
manifest. The leaf's `evaluations/proper-study-results/17099e79f3655b7d/`
contains the actual terminal status and replay outputs plus a record of all
26 packet/result identities. Replay reports `recorded_file_intact: true`;
`deterministic: null` is the terminal packet-integrity behavior, not a fresh
reexecution of the scholarly work. The original seed identity remains intact.

## Scope clarification and source limits

`interventions/0000.json` records a wording clarification during research.
The packet explicitly designates the three-document profile as the deliverable
owner; its schema-2 contract supersedes the old mandatory cultural-gallery and
exploratory-proposal quotas. Each interpretation still requires its own four
senses. No workflow source or compiled packet was changed. The intervention
remains `encoded: false`; this archive does not represent the clarification as
a pipeline implementation change.

Research acceptance covers a bounded study, not complete collation of the
governing 2008 Latin and U.S. 2011 altar books, an established local calendar
overlay or enacted musical choices, exhaustive reception coverage, or fresh
collation of every historical facsimile. The shared owner and local evidence
records state the exact limits, including the unestablished approved-English
Prayer over the Offerings exemplar. Restricted source bodies are not retained
in this archive.

Source-library, chronology-record, chronology-annotation, containment and
source-inventory checks passed at the recorded research boundaries. The
family ledger remains explicitly pending: 155 review units, none claimed
family-screened. Initial `make check-sources` stopped at the expected absence
of `web-edition.toml` beside the reserved, unpublished source scaffold.
After study authoring supplied that declaration, the check passed source-library
validation but stopped at the still-unwritten `homily.tex` declared for a later
stage. After homily authoring, source-library and both source inventories
passed and the live document catalog check completed. The aggregate then
stopped at the expected deterministic document-catalog projection drift from
the new three issues; projection refresh was deferred to installation.

After terminal acceptance and the final leaf record, `make check-sources`
identified a further deterministic source-reader projection drift. A scratch
projection established exactly five affected files: the GIRM edition gained
the two newly registered restricted artifact metadata entries, three new
edition projections represented the two CCEL acquisitions and USCCB reading
page, and the index gained their rows and counts. The root granted the owning
refresh and exact scoped release binding adoption. No source, PDF, conversion
or accepted review seal changed, and the original terminal result was preserved.

Final `make check-sources` passed using the pinned Markdown dependency, as did
both target-scoped and full public-alpha checks and release binding validation
(`0 stale binding(s)`). Full policy covers 236 publications: 234 alpha and two
hold. The source reader's 4,085 files and document projection are current;
source-library totals are 2,825 artifacts, 1,019 editions, 5,199 passages,
89 segments, 735 works and 3,117 bindings. The GPT source inventory contains
144 publications, 2,462 source-surface files and eleven owners. Six curriculum
rights tests passed. The family ledger remains 155 pending, zero screened.

The passing aggregate reports its limits: the inherited held Claude 54 pair
has no installed PDFs; ten older workflow versions are advisory; four existing
calendar-mass exceptions remain recorded; the author-standing inventory covers
22 of 23 lane authors and has no Leo the Great row. These reports were not
silently converted into completed screening or unrelated production work.

## Archive boundary

The maintainer subsequently requested deployment to `main`. Local deployment
source checks, public-site construction, GitHub Pages artifact verification and
release bindings passed. The reviewed outgoing range reached `origin/main` by
ordinary fast-forward at `6f9894562c95ed021756782031dee3d5ccf3922c`; automatic
Pages run [36505173632](https://github.com/spincyc/triptych/actions/runs/36505173632)
succeeded. On 29 September 2026 UTC, all three live PDFs, canonical HTML,
postconciliar catalog and stylesheet returned HTTP 200 with hashes identical
to the verified local artifact. The catalog's four GPT Year A links and
separate provider headers were confirmed. The exact response identities and
workflow result are retained in [deployment-evidence.json](deployment-evidence.json).
This deployment record changes no accepted publication or review seal.

The durable archive retains exact compiled packets, engine-accepted results,
interventions and checkpoint metadata. Build logs, raster proofs, downloaded
source caches and unrecorded scratch notes remain disposable outputs. Their
omission does not change any recorded packet or result hash. Final artifact
identities and terminal disposition above were recorded only after the
corresponding stages actually ran. The terminal record retains both failed
cold-review cycles, every repair and the actual advisory/accepted findings.
