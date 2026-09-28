# GPT Nineteenth Sunday production

Run `b686b7a44f0e35e7`, `proper-study` v7, provider `gpt`, identity
`liturgy/roman-rite/1962/propers/temporal/59-nineteenth-after-pentecost`,
date `2026-10-04`, audience `adult parish assembly`.

The run is pinned to seed commit
`a1320fb62298ed6b1cf10d82d252212a03a484d0` and workflow digest
`9c0b654d981692c0a1d4592beae5a00764180378d63ba80185d3ce7a23f5be38`.
Its disposition is pending. No artifact has been accepted or installed.

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

Visual review is active. Every agent stage uses a fresh worker with no
inherited authoring conversation and the packet's declared reasoning effort.
Author stages use `high`; review stages use `xhigh`. No nested workers are
authorized by this workflow.

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

## Scope

The target has three PDFs and one canonical web edition. Work is integrated
on the workspace branch `feature/propers/codex`; no main-branch merge or live
deployment is claimed. The source owner will archive the actual workflow
packets, results, terminal status and review evidence at completion.
