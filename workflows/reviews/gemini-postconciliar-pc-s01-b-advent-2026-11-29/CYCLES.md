# Gemini Postconciliar First Sunday of Advent (Year B) Production

Run `6360bf57cd7d36ba`, `proper-study` v20, provider `gemini`, identity
`liturgy/roman-rite/postconciliar/roman-missal-third-edition-en-us-2011/propers/temporal/pc-s01-first-sunday-of-advent-year-b`,
date `2026-11-29`, audience `adult parish assembly`.

The run is pinned to seed commit
`0f8fb307cde69819014f3d26a7f0cd77cb6ce9a9` and workflow digest
`9829722276b1a1f662a2c7a4f5e7e2562394d5ef83911bb94d8b729393f1feec`.
Its terminal disposition is **ACCEPTED**, returned by the engine on
26 November 2026 across 57 packets and 57 results with zero standing
findings and zero manual interventions. All three source/HTML outputs
(expansive study, concise study, and homily) are installed under
`rights-limited` discipline with their three alpha release records and
`library/novus-ordo-liturgy.md` catalog links.

## Transitions

| Stage | Iteration | Result | Evidence |
| --- | ---: | --- | --- |
| scope-gate | 0 | PASS | Exact provider (`gemini`) and postconciliar permanent identity (`pc-s01-first-sunday-of-advent-year-b`) authorization passed. |
| resolve-context | 0 | PASS | Verified Sunday 29 November 2026 (Liturgical Year 2027, Sunday Cycle B / Weekday Cycle I, U.S. Roman Missal 3rd ed. / U.S. Lectionary No. 2) in `rights-limited` mode; wrote `research/context.md` and reserved `main.tex`. |
| research | 0 | PASS | Created edition-locale shared Missal owner (`shared/formularies/pc-s01-first-sunday-of-advent/propers/verified.md`), leaf `propers/retrieved.txt` and `verified.md`, `instance/manifest.md`, `research/scope.md`, `interpretations.md`, chronology records, and 90 source bindings. |
| source-registration | 0 | PASS | Reconciled 90 bindings into `research/source-dispositions.toml` and registered new patristic passages under `src/sources/works/`. |
| research-preflight | 0 | PASS | Engine research contract, chronology, source-disposition, and binding checks passed. |
| research-review | 0 | CHANGES_REQUIRED | Cold review returned 5 blocking findings (`RES-001`–`RES-005`) and 3 advisories (`RES-006`–`RES-008`). |
| research | 1 | PASS | Repaired all 5 blocking findings and cleared all 3 advisories; expanded bindings to 117. |
| source-registration | 1 | PASS | Re-audited and reconciled all 117 bindings across 121 disposition entries; refreshed source inventories and validated source graph and strict working projection. |
| research-preflight | 1 | PASS | Engine research preflight passed on repaired research bundle. |
| research-review | 1 | PASS | Independent cold review passed with 0 blocking findings and 1 non-blocking advisory (`RES-009`). |
| author-study | 0 | PASS | Authored complete schema-2 expansive study (`sections/10`–`95`, `publication.toml`, `proper-components.toml`, `generation-metadata.tex`, `web-edition.toml`) covering all 12 appointed elements and 3 interpretive lanes. |
| study-preflight | 0 | PASS | All 15 study program checks (including `study-web-conversion`) passed. |
| study-review | 0 | CHANGES_REQUIRED | Cold review returned 7 blocking findings (`STU-001`–`STU-007`) and 1 advisory (`STU-008`). |
| author-study | 1 | PASS | Repaired `STU-001`–`STU-007` and cleared `STU-008` in study-owned files without altering sealed research. |
| study-preflight | 1 | PASS | All study program checks passed. |
| study-review | 1 | CHANGES_REQUIRED | Cold review returned 3 blocking findings (`STU-009`–`STU-011`) and 1 advisory (`STU-012`). |
| author-study | 2 | PASS | Surgically repaired `STU-009`–`STU-011` and cleared `STU-012` directly against held witnesses and rights inventory. |
| study-preflight | 2 | PASS | All study program checks passed. |
| study-review | 2 | PASS | Independent cold review passed with 0 blocking findings. |
| derive-synthesis | 0 | PASS | Declared `[document.synthesis]` and authored five concise-study components (`sections/synthesis/10`–`90`). |
| synthesis-preflight | 0 | PASS | All synthesis program checks passed. |
| synthesis-review | 0 | CHANGES_REQUIRED | Cold review returned 4 blocking findings (`SYN-001`–`SYN-004`) and 1 advisory (`SYN-005`). |
| derive-synthesis | 1 | PASS | Repaired `SYN-001`–`SYN-004` and cleared `SYN-005` inside `sections/synthesis/`. |
| synthesis-preflight | 1 | PASS | All synthesis program checks passed. |
| synthesis-review | 1 | PASS | Independent cold review passed with 0 blocking findings. |
| derive-homily | 0 | PASS | Authored verbatim spoken homily (`sections/homily/10-homily.tex`) and terminal apparatus (`90-note.tex`). |
| homily-preflight | 0 | PASS | All homily program checks passed. |
| homily-review | 0 | CHANGES_REQUIRED | Cold review returned 5 blocking findings (`HOM-001`–`HOM-005`). |
| derive-homily | 1 | PASS | Repaired `HOM-001`–`HOM-005` inside `sections/homily/`. |
| homily-preflight | 1 | PASS | All homily program checks passed. |
| homily-review | 1 | PASS | Independent cold review passed with 0 blocking findings. |
| build-artifacts | 0 | PASS | Validated all three source outputs (`main.tex`, `synthesis.tex`, `homily.tex`) and recorded source identities in source/HTML mode. |
| artifact-gates | 0 | PASS | Source identities, schema/component checks, and all upstream accepted review seals matched. |
| generate-web | 0 | PASS | Confirmed clean committed sources (`05d2b274b7`) and converted canonical expansive study to Markdown; recorded `research/web-artifact.json`. |
| web-review | 0 | CHANGES_REQUIRED | Cold web review identified 3 blocking findings: `WEB-001` (shared converter nested-emphasis bug inside `latinproper` `\notread{...}`), `WEB-002` (doubled brackets and `64:1` span in `20-appointed-texts.tex`), and `WEB-003` (Psalm/Isaiah 64 numbering consistency in study sections). |
| author-study | 3 | PASS | Repaired `WEB-002` and `WEB-003` across study sections (`20`–`70`) while preserving sealed research. |
| study-preflight | 3 | PASS | All study program checks passed on repaired expansive study. |
| study-review | 3 | PASS | Independent cold review passed with 0 findings. |
| derive-synthesis | 2 | PASS | Audited and harmonized concise study against `WEB-002`/`WEB-003` repairs. |
| synthesis-preflight | 2 | PASS | All synthesis program checks passed. |
| synthesis-review | 2 | PASS | Independent cold review passed with 0 blocking findings (1 accepted `SYN-007`). |
| derive-homily | 2 | PASS | Audited homily against updated study/synthesis and aligned Isaiah 64 citation. |
| homily-preflight | 2 | PASS | All homily program checks passed. |
| homily-review | 2 | CHANGES_REQUIRED | Cold review returned 1 blocking finding (`HOM-007`: pre-Gospel acclamation identification in `10-homily.tex`). |
| derive-homily | 3 | PASS | Repaired `HOM-007` in `sections/homily/10-homily.tex` (1,478 spoken words). |
| homily-preflight | 3 | PASS | All homily program checks passed. |
| homily-review | 3 | PASS | Independent cold review passed with 0 findings. |
| build-artifacts | 1 | PASS | Re-validated all three source outputs and updated source identities in `research/production-review.md`. |
| artifact-gates | 1 | PASS | All source-artifact gates and upstream review seals matched. |
| generate-web | 1 | PASS | Re-converted canonical study at `d721fd26d6` after `tools/web-edition` nested-`Emph` fix (`0a2817c897`), confirming `WEB-001` resolved (`sha256: 61307d96607693a402126bf71103f2c2f3775fdf915bb10c578b2ebeb850e9d0`). |
| web-review | 1 | PASS | Independent cold web review passed with 0 findings. |
| install-publication | 0 | PASS | Recorded web review in `web-edition.toml`, created 3 alpha release records, wired `library/novus-ordo-liturgy.md`, refreshed inventories, recorded browser products, and refreshed release bindings. |
| publication-gates | 0 | FAIL | Returned `STALE-WEB-REVIEW` after converter commit `2f96ab50c1` narrowed the italic-inside-italic audit in `tools/web-edition` (a sealed web-review input), routing cleanly back to `generate-web`. |
| generate-web | 2 | PASS | Re-converted canonical study at `HEAD` `2f96ab50c1` (source commit `d721fd26d6`), confirming byte-identical Markdown (`sha256: 61307d96607693a402126bf71103f2c2f3775fdf915bb10c578b2ebeb850e9d0`) and refreshed `research/web-artifact.json`. |
| web-review | 2 | PASS | Independent cold web review passed with 0 findings on current converter bytes. |
| install-publication | 1 | PASS | Updated `web-edition.toml` inspection record, refreshed `gemini-publications-v1.toml`, recorded/checked browser products, refreshed release bindings, and verified all 5 publication gates and all 5 review seals. |
| publication-gates | 1 | PASS | All 5 terminal publication gates and every upstream review seal matched; terminal disposition **ACCEPTED** with 0 standing findings and 0 escalations. |

## Execution Policy and Provenance

Every stage ran in a fresh subagent with zero inherited authoring context for
evaluators and at the packet's declared reasoning effort (`high` for authoring,
research, and installation stages; `xhigh` for all independent cold reviews).
All workers and evaluators ran on `gemini-4-neon` through Google Antigravity CLI,
recorded in `generation-metadata.tex` with exact workflow run headers.

## Web Converter Repairs and Post-Acceptance Integration

1. **Nested emphasis in `tools/web-edition` (`WEB-001`):** `\notread{...}` inside
   `\begin{latinproper}` previously emitted nested `*...*` Markdown that toggled
   `<em>` off and on under locked Python-Markdown (`<em>[</em>...<em>]</em>`).
   `TABLE_FILTER` in `tools/web-edition` now flattens nested `Emph`/`Strong`
   nodes (skipping `Note` bodies), paired with a narrowed italic-inside-italic
   rendered-HTML audit and regression tests in
   `tools/tests/test_web_edition_conversion.py`.
2. **Stage B lane execution and integration:** Stage B ran to terminal `ACCEPTED`
   in a dedicated worktree branched from the Stage A commit so upstream merges
   on `feature/triptych/propers` could not invalidate sealed `proper-study-v5`
   research inputs mid-run, and the accepted commit (`07dddeafb1`) was then
   merged into `feature/triptych/propers` with refreshed inventories, browser
   products, release bindings, and corpus index.
3. **Archive audit and native print proof:** After acceptance, the archiver's
   path scan in `tools/proper-study-run-archive` was updated to recognize HTML
   closing tags (`</em>`, `</a>`, `</span>`) quoted in `WEB-001` review findings
   as markup rather than POSIX paths, allowing run `6360bf57cd7d36ba` to archive
   byte-exact without redaction. All three declared editions were locally
   proof-built via `tools/print-document` after making `POSTCONCILIAR_US_FORMAT`
   optional via `$(wildcard ...)` in `Makefile` for providers starting directly
   on `proper-study-v1` and adding `\phantomsection` before `\section*{References}`
   in `sections/95-references.tex` (fixing a `check-pdf-anchors` collision with
   `\subsection{Canonical Audit Records}` with zero prose or web-reader change):
   canonical expansive study (`32` pages, Letter), concise study (`12` pages,
   Letter, settled 4-page opening verified), and homily (`5` pages, Letter), all
   building with zero errors and verified by `tools/tpt web-edition check`
   (`3 reader output(s), 0 figure(s)`).
