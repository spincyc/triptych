# GPT Nineteenth Sunday production

Run `b686b7a44f0e35e7`, `proper-study` v7, provider `gpt`, identity
`liturgy/roman-rite/1962/propers/temporal/59-nineteenth-after-pentecost`,
date `2026-10-04`, audience `adult parish assembly`.

The run is pinned to seed commit
`a1320fb62298ed6b1cf10d82d252212a03a484d0` and workflow digest
`9c0b654d981692c0a1d4592beae5a00764180378d63ba80185d3ce7a23f5be38`.
Its terminal disposition is **ACCEPTED**, returned by the engine on
28 September 2026. All three PDFs and the canonical web edition are installed
at their independently reviewed hashes.

## Transitions

| Stage | Iteration | Result | Evidence |
| --- | ---: | --- | --- |
| scope-gate | 0 | PASS | Exact provider and permanent-identity authorization passed. |
| resolve-context | 0 | PASS | Dated FSSP Ordo, six controlling Missal page images, ten-element inventory, ordinary framing and branch dispositions; research source plan recorded. |
| research | 0 | PASS | Textual collation, rights, chronology, bounded reception, two interpretations, exact bindings and declared dependencies recorded. |
| research-preflight | 0 | PASS | Engine's research contract and receipt checks passed. |
| research-review | 0 | CHANGES_REQUIRED | RES-001 requires the controlling author-standing registry in review dependencies; RES-002 advises precise wording for Gregory's weaving analogy. |
| research | 1 | PASS | Declared the author-standing dependency and corrected Gregory's weaving analogy. |
| research-preflight | 1 | PASS | Research checks pass; live next-review packet includes the current author-standing bytes. |
| research-review | 1 | PASS | Fresh focused review cleared RES-001 and confirmed the Gregory correction; all 141 sealed inputs match, no blocking findings. |
| author-study | 0 | PASS | Complete 20-page study, approximately 6,930 substantive words, two interpretations and all ten elements; author inspected every page. |
| study-preflight | 0 | PASS | All workflow-declared study program checks passed. |
| study-review | 0 | CHANGES_REQUIRED | STU-CHR-001 requires a current Ephesians authorship/composition account in research and the study dossier; STU-CIT-001 advises correcting Gregory's source URL. |
| research | 2 | PASS | Verified current USCCB Ephesians introduction, added a conditional critical-profile corpus assertion and generated comparison, and recorded study-owner follow-through. |
| research-preflight | 2 | PASS | Research contract and current source bindings pass. |
| research-review | 2 | PASS | New comparison and supporting evidence checked; all 144 sealed inputs match, no findings. |
| author-study | 1 | PASS | Incorporated the reviewed Ephesians account and corrected the Gregory URL; rebuilt 20-page proof and inspected all pages. |
| study-preflight | 1 | PASS | All workflow-declared study program checks passed after repair. |
| study-review | 1 | PASS | Complete study, source loci, proper texts and chronology checked; all 17 sealed files unchanged, no blocking findings. |
| derive-synthesis | 0 | PASS | Complete 10-page concise study with 3,719 substantive words, required four-page opening and full author page inspection. |
| synthesis-preflight | 0 | PASS | All workflow-declared synthesis program checks passed. |
| synthesis-review | 0 | PASS | Complete concise prose and all 10 pages checked against the expansive study and exact cited loci; all 14 sealed inputs unchanged, no findings. |
| derive-homily | 0 | PASS | Complete 1,301-word spoken homily and separate apparatus; three-page proof, estimated 10.4–11.3 minutes before pauses, all pages author-inspected. |
| homily-preflight | 0 | PASS | All workflow-declared homily program checks passed. |
| homily-review | 0 | PASS | Complete speech, three proof pages, source support and exact 1,301-word count checked; no findings. |
| build-artifacts | 0 | PASS | Normal Make builds produced 20/10/3 pages; logs, structure, embedded fonts and extracted texts pass; exact snapshot and all 33 rasters prepared without source changes. |
| artifact-gates | 0 | PASS | Artifact snapshot, physical-page evidence and all upstream accepted review seals match. |
| visual-review | 0 | PASS | All 33 pages inspected individually at full raster size; all 30 sealed inputs match, no findings. |
| generate-web | 0 | PASS | Complete canonical Markdown and exact receipt generated after a tested repair for body-imported chronology; existing web editions remain byte-current. |
| web-review | 0 | PASS | Complete conversion, 38 exact notes, desktop/mobile rendering and local reference navigation checked at the sealed Markdown hash; no findings. Remote URL availability and a deployed site were not audited. |
| install-publication | 0 | PASS | Normal Make installation reproduced all three accepted PDF hashes; exact web bytes, catalog row, three release records, scoped bindings and owning inventories installed. |
| publication-gates | 0 | PASS | Engine publication checks, release bindings, scoped public-alpha and document-library checks, global catalogue structure and web currency passed; terminal ACCEPTED with no escalations. |

Every agent stage used a fresh worker with no
inherited authoring conversation and the packet's declared reasoning effort.
Author stages use `high`; review stages use `xhigh`. No nested workers are
authorized by this workflow.

**Model provenance.** The contributing workers identify themselves as GPT-6,
with `high` for the context, research, authorship, artifact, conversion and
installation stages and `xhigh` for the independent reviews. The coordinator
identifies as GPT-6; its reasoning setting is unexposed. Exact model variants,
other model qualifiers, client version and server revision are unexposed.
The generation metadata records these actual configurations without inventing
an installation commit. No production metadata changed after the final
artifact snapshot; later review and installation work is recorded here and
in the actual engine submissions.

## Validation baseline

Before publication authoring, `make check-sources`, `make check-release-bindings`
and `tmt check` passed. The release binding check reported zero stale bindings.
The promise-ledger check has identical failures against the seed ledger and
the newly registered target: ignored older PDFs are absent from a fresh clone.
Those failures are not new-target acceptance and remain separately identified.

After research, the canonical source graph, refreshed structural inventory and
family ledger validate. The new publication is broadly source-categorized;
the family ledger remains honestly pending and claims no completed family
screening. The first integrated `make check-sources` stopped because
`web-edition.toml` was absent beside the deliberate research-stage source
placeholder. Authoring has since supplied it; the full integrated source
check remains required after publication wiring and derived catalog refresh.
The research-2 integrated attempt reaches the next unfinished entrypoint,
`homily.tex`; focused research, source-library and chronology checks pass.
At this checkpoint, `make check-release-bindings` reports exactly one stale
binding: this target's ungenerated canonical web edition. Existing publication
bindings are unchanged; the new binding belongs to the installation stage.

After homily authoring, the coordinator refreshed the document catalogue,
source projection, structural inventory and family ledger with their owning
tools. The complete `make check-sources` passes. The projected source changes
correspond to the registered witnesses, checked public-domain English passages
and target bindings; protected USCCB wording remains withheld. The refreshed
reader-facing catalogue and projection require their scoped release-binding
refresh during installation. The generation audit additionally records the
actual research, reviewer and coordinator configurations without changing
rendered prose, the finalized timestamp or production identity.

The expansive-study checkpoint's full staged whitespace check reported an
extra blank line at EOF in `sections/00-opening.tex` and
`sections/10-appointed-text.tex`; the earlier unstaged check did not include
those newly added files. These cosmetic source warnings have no rendered
effect. No sealed study input was changed during cold review to clear them.
After that review returned CHANGES_REQUIRED and the engine routed a research
repair, the coordinator removed only those trailing blank lines. The subsequent
fresh authoring and study-review passes accepted the corrected source.

## Web converter repair

The first conversion attempt reported a missing introit chronology annotation.
The definitions were present in the reviewed body component; the converter
only read preamble definitions. The generation worker repaired that lookup,
removed generated definitions from the rendered body, and limited its helper
scan exception to the exact generated dispatcher. Regression coverage checks
body imports, duplicate keys across preamble/body and refusal of an altered
helper containing an unknown command. The 131-test converter suite passed;
the stricter rejection assertion added afterward passed in its focused test.
The coordinator inspected the complete diff and `tmt check` passed. No accepted
publication source, metadata or PDF changed. The fidelity contract now records
the supported body import. The full web-current check reports no stale existing
edition, only the new edition awaiting review and installation.

## Scope

The target has three PDFs and one canonical web edition. Work is integrated
on the workspace branch `feature/propers/codex`; no main-branch merge or live
deployment is claimed. The source owner retains the actual workflow
packets, results, terminal status and review evidence in the terminal archive.

## Terminal evidence and installed artifacts

The leaf's `evaluations/proper-study-results/b686b7a44f0e35e7/` contains all
30 exact engine packets, all 30 accepted submissions (including the two
CHANGES_REQUIRED results), the seed manifest and bootstrap, terminal state,
status and replay output, plus a hash index. Every copied packet and result
matches the engine's recorded SHA-256. The terminal replay reports
`recorded_file_intact: true` and `deterministic: null`; it is a terminal
integrity report, not a fresh deterministic reexecution.

| Artifact | Extent | SHA-256 |
| --- | --- | --- |
| Expansive study | 20 pages; 6,930 substantive words | `52b155c7e4366f0ef8304871ac1dabbbc56733aaaaa589f12085b396d7f18d43` |
| Concise study | 10 pages; 3,719 substantive words | `7681fbd92d4301f3138f5512d97f6273119a7364f2e02bbff2edb2ea115c1848` |
| Homily | 3 pages; 1,301 spoken words | `75f155ca5c86429a1f487e6d076bffe3faf3026a4a6dbb9274be822344da963c` |
| Canonical web Markdown | 38 exact notes | `dc4948bdc26ab27a24d562018196b556298903d256b7364bf918997b38c25eb5` |

The homily estimate is 10.4–11.3 minutes at 115–125 words per minute before
pauses; no timed human delivery is claimed. Source reviews checked the cited
loci, not a new collation of complete critical editions. Manual bibliography
checks supplied the evidence that the formal-entry citation tool cannot
provide for description-list bibliographies. The existing concise chronology
formatter drops the word “around”; the source-owned Ephesians title explicitly
retains “approximate,” and the research record identifies that separate
tooling limitation. The web review checked local presentation and navigation;
remote URL availability and live deployment remain outside its claims.

The installer passed full `make check-sources` and web currency. The terminal
publication gate passed all its declared checks. The release binding diff
changes exactly the 16 reconciled task-owned site inputs, including ten new
inputs; all 22,137 other site-source hashes are preserved. There are zero
stale release bindings. Installed PDFs are intentionally ignored under the
repository's PDF migration policy; their sources, receipts and release records
are tracked.

The whole promise-ledger check retains 23 errors, all present in the untouched
baseline and all concerning older absent PDFs. One baseline missing-directory
error disappeared when this family was installed. There are no new ledger
errors. After the terminal archive and final production audit were written,
the two source inventories were refreshed and full `make check-sources`
passed again. Staged whitespace and added-text privacy checks pass. The
coordinator rechecked all three build/install PDF pairs and installed web
against the accepted hashes. Publication checkpoint
`86f187baf9d477ae65f7144911707c312e3fc28a` is committed and pushed to
`origin/feature/propers/codex`. The final bookkeeping commit closes the target
ledger against that concrete accepted-publication checkpoint.

The isolated target ledger passes `check-promised-deliverables` with
`--require-complete gpt-1962-nineteenth-three-documents-2026-09-28`:
one tracked deliverable, one complete. A separate full-register check confirms
exactly one marker for each of the 50 ledger entries. The final whole-ledger
check still reports only the 23 inherited older-PDF errors described above.
