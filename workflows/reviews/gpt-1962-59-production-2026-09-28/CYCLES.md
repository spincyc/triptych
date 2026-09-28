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

Study-review iteration 1 is active. Every agent stage uses a fresh worker with no
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

The expansive-study checkpoint's full staged whitespace check reported an
extra blank line at EOF in `sections/00-opening.tex` and
`sections/10-appointed-text.tex`; the earlier unstaged check did not include
those newly added files. These cosmetic source warnings have no rendered
effect. No sealed study input was changed during cold review to clear them.
After that review returned CHANGES_REQUIRED and the engine routed a research
repair, the coordinator removed only those trailing blank lines; the study
will receive its required fresh authoring and review passes after research.

## Scope

The target has three PDFs and one canonical web edition. Work is integrated
on the workspace branch `feature/propers/codex`; no main-branch merge or live
deployment is claimed. The source owner will archive the actual workflow
packets, results, terminal status and review evidence at completion.
