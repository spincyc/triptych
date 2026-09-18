# Proper-study v3 implementation recovery review

**Verdict: ready to freeze the reviewed implementation and seed fresh v3
productions.** No unresolved implementation blocker was found. This is not
acceptance of either Sunday's documents, a source/rights review, visual
acceptance, or authorization to reuse historical production verdicts.

## Independence and boundary

This reviewer did not author the abandoned implementation and received none of
its authoring conversation. The review recovered the existing guidance PASS
and pagination/chronology probes, then examined the uncommitted implementation
and exercised its regressions. It authored the two corrective patches below;
their validation is the reviewer's own testing, not a second independent review
of those patches.

Recovery base: `6f552cc63729bfa2a6970c13bdf92bf1257651db`. The packaged
`SHA256SUMS` identifies the exact final implementation and test bytes.
Guidance, workflow definitions, documents, installed artifacts, production runs,
commits, and remote refs were not changed by this review.

## Findings and dispositions

| Finding | Disposition |
| --- | --- |
| Prior pagination: repeated direct/indirect annotation imports escaped the source gate. | Resolved before recovery; exact-once tests pass. |
| Prior pagination: valid `\include` child auxiliary labels were rejected or omitted from the visual seal. | Resolved before recovery; safe child traversal, child-byte seal invalidation, and real TeX physical-page tests pass. |
| Prior chronology/guidance: research required an authoring manifest, presentation-only edits invalidated dates, or computation drift escaped the research seal. | Resolved before recovery; research-before-manifest, byte stability, explicit v3 computation sealing, and historical seal isolation pass. |
| Recovered unresolved chronology defect: `Matthew 20:100-21:2`, `20:1-21:0`, and `20:100-21:0` were accepted after expansion silently lost invalid endpoints. | Fixed in `scripts/_proper_chronology_inputs.py`: validate original endpoints through the existing spelling/concordance and canonical bounds before expansion. Six invalid cases refuse in the API and CLI; valid cross-chapter and whole-chapter queries retain all verses. No 1962 expansion behavior changed. |
| New verified preflight defect: the default whole-leaf check counted research and concise date cells together, falsely rejecting separate historical treatment while allowing a research cell to conceal an omitted concise row. | Fixed in `tools/check-content-preflight`: opted-in v3 whole-leaf chronology checks each reading experience separately. Research reuse passes; missing/duplicate concise cells still refuse. Historical contracts are unchanged. |

## Verification

Exact commands and numeric exits are in `checks.txt`; fixture outputs are not
production approvals.

| Check | Result |
| --- | --- |
| Final adapter, pagination, artifact-routing suites | **49/49 passed**, exit 0; real TeX/Poppler pagination test ran, not skipped. |
| Extended proper/component/chronology/preflight suites | **333/334 passed**, exit 1; sole failure is the inherited 15-leaf assertion below. |
| Complete workflow test discovery | **928/929 passed**, exit 1; same inherited 15-leaf assertion, no additional failure. |
| Components, annotations, chronology corpus, derivation suites | **322/324 passed**, exit 1; two inherited missing-history failures below. |
| Explicit comparison with recovery base | Four 1962 records and all four annotation projections byte-identical; dated and undated historical research seals identical; historical artifact seal identical. |
| Workflow definition load; `tmt check`; focused `git diff --check` | Exit 0 each. |

The initial broad workflow attempt timed out after 240 seconds; the completed
rerun above supersedes it.

### Inherited failures, not hidden passes

- `test_workflow_synthesis_preflight.CorpusTests.test_the_gate_refuses_six_of_the_fifteen_manifest_leaves`
  asserts 15 while both the recovery base and worktree contain 16 1962
  component-manifest leaves. Its test owner is unchanged.
- `test_chronology.RemediationTests.test_the_cold_review_manifest_is_not_stale`
  and `test_the_command_the_manifest_advertises_does_not_collapse_it` require
  absent Git object `c1dee9fc0ddfea3ea06d951c7ad25d05b75b0341`.
  The tests, manifest builder, historical extractor, and chronology corpus are
  unchanged from the recovery base. No tests were weakened and no history was
  fetched or manufactured to hide these failures.

## Follow-up

The parent can retain this concise review and final hash manifest as the durable
review record. It should inspect the two corrective patches, freeze the v3
definition, and seed **new, separate** 1962 and postconciliar production runs.
Every research, study, concise, homily, visual, web, and publication verdict
must still be earned on current artifacts. The inherited corpus-count fixture
and missing historical object need separate maintenance if an entirely green
broad test run is required.
