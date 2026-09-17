# Independent implementation cold review

**Verdict: PASS for the reviewed implementation. No unresolved blocking finding remains.** This approves the state-machine and publication-infrastructure changes for use; it does not approve the still-to-be-produced studies, homilies or rendered publications.

Base: `b27036f9b856bd8f662f51b6e6128bd90a5ed633`. Branch: `feature/codex/propers/homily`. The reviewed state contains uncommitted changes. `workflows/reviews/propers-three-documents-implementation-hashes-2026-09-17.json` records exact SHA-256 values for the 46 reviewed files; `final-reviewed-tracked.patch` captures their tracked diff against the base. Untracked implementation files are identified by their exact hashes. `workflows/reviews/propers-three-documents-implementation-initial-hashes-2026-09-17.json` identifies the earlier state against which the original findings were reproduced. Subject files were not edited or committed by this reviewer.

## Findings and verified dispositions

| Priority | Finding | Final disposition |
| --- | --- | --- |
| P1 | Accepted source/artifact judgments were not bound to the reviewed bytes. Replacing a leaf snapshot could admit changed PDFs or web bytes; research evidence edits were outside render snapshots. | **Fixed.** `scripts/_workflow.py:2255` captures an engine-owned input seal in the hash-bound review packet, verifies it when PASS arrives, and stores it in the retained result. `scripts/_workflow.py:2271` checks current input identity; final acceptance checks it again at line 2741. `scripts/_proper_study.py:208` separately projects research, study, concise, homily, visual and web evidence. Research includes local research/propers/instance records, declared same-family owners and exact bound source-record ancestry/payloads. Nominally refreshing a leaf receipt cannot refresh the engine's accepted seal. |
| P2 | Late stale-input failures returned only to an installation worker forbidden to repair/review them. | **Fixed.** `workflows/pipelines/proper-study.json:740` enables review-input verification and ordered owner repair routes. Independent engine fault injection verified that a changed accepted source returns to its author, receives a fresh review, and then reaches ACCEPTED. During-review mutation also prevents PASS. Homily review now admits a synthesis-owned defect. |
| P2 | The terminal global public-alpha check required installing212 unrelated PDFs in this source-only clone. | **Fixed.** `tools/public-alpha:2486` resolves exactly the canonical schema-2 output triple; pipeline line 722 invokes its scoped check. All three selected PDFs remain required; unrelated absence is permitted only by this scoped check. Global source/release/authorization policy remains checked. Build/prepare/verify cannot use the scope. Nine targeted tests verify these boundaries. |
| P2, found by coordinator | A brand-new proper's research binding validation required main.tex before author-study had created it. | **Fixed.** resolve-context explicitly reserves a comment-only canonical-owner scaffold without claiming prose, a build or acceptance. Author-study replaces it and must satisfy the full content graph. The new-leaf regression passes. |
| Contract clarification | Every interpretation must have at least two substantive authors. | **Aligned.** `scripts/_proper_components.py:283` requires at least two distinct normalized author names; author/research/study review instructions require substantive compatible contributions, not nominal citations. Semantic compatibility remains a cold-review judgment. |

The original receipt defect was independently reproduced by `probe_review_binding.py` and logged in `probe_review_binding.txt` before repair. That diagnostic uses synthetic results and explicitly stubbed program checks; it proves the missing binding in that earlier implementation, not semantic acceptance of a publication.

## Whole-proper family separation

The 1962 and postconciliar canonical IDs root research, source components, studies and homilies in distinct liturgical trees; their PDF/web paths mirror that ancestry. There is no new shared Sunday or interpretation owner. Shared postconciliar Missal owners stay under the selected postconciliar edition/locale.

`validate_liturgical_family` (`scripts/_proper_components.py:31`) checks resolved ancestry rather than an element name. It protects appointed prayers, chants, readings and imported components equally. Direct imports, differing postconciliar locales and recorded inputs are tested. `probe_family_ancestry.py` additionally compiles six real fixture PDFs with pdflatex: an opposite-family Collect hidden behind a generic common bridge is rejected from the actual .fls recorder in both directions. The research dependency seal also checks every declared owner and selected descendant against the family boundary. Bound provider-neutral primary sources remain independently citeable.

Completeness and correct selection of declared evidence dependencies still require the research review. A path validator cannot prove that a passage actually belongs to the appointed formulary, that an author supports a claim, or that two differently spelled names identify different historical people. The fragments explicitly retain those semantic duties rather than treating flags as evidence.

## Checks performed

- `python3 .scratch/implementation-cold-review/run_focused_tests.py`: **exit 0, 156 tests passed**. Includes proper-study workflow, schema 2 components/preflight, legacy components, seed-idempotency/engine/evaluator-route coverage,7 catalogue-fallback tests and9 scoped-publication tests. Log: `final-focused-tests.txt`. All temporary fixtures were redirected into this review directory.
- `python3 .scratch/implementation-cold-review/probe_engine_seals.py`: **exit 0**. Independently verifies changed inputs during review, changed accepted inputs at the final gate, repair/fresh-review/acceptance, unchanged acceptance, refusal of a manufactured reviewer seal, and deterministic historical replay after current bytes change. Log: `probe_engine_seals.txt`.
- `python3 .scratch/implementation-cold-review/probe_family_ancestry.py`: **exit 0**. Actual pdflatex recorder rejection of indirect opposite-family Collect imports in all three outputs, in both directions. Log: `probe_family_ancestry.txt`.
- `tools/tpt --check`: **exit 0**,41 registered tools.
- `tools/tpt check-proper-components --provider gpt`: **exit 0**,12 existing manifests; corresponding Claude check: **exit 0**,8 manifests. No current schema 1 regression found.
- A shell-metacharacter date probe remained one quoted scalar, exited1 for invalid date, and created no injected file. The new seed flags do not bypass the engine's single-pass shell quoting.
- The source-only document-catalogue fallback retains only historical artifact facts for matching freshly derived edition metadata/identity. It does not certify absent PDFs. The live catalogue check remains candid about absence.

## Limits and operational facts

No production run was seeded by this reviewer. No content, theological, visual, oral-performance or final publication acceptance is claimed. Real runs must still complete all independent reviews and inspect every rendered page. No test fixture verdict is evidence for a real deliverable.

Unscoped public-alpha validation still fails in this clone because unrelated installed PDFs are absent; `public-alpha-global.txt` preserves that observed failure. This is not a deployment approval. The scoped check intentionally retains global source/release inventory consistency, so concurrent new-leaf publication wiring must be coordinated before final acceptance.

This verdict applies only to the hashes recorded here. Later changes require proportionate re-review. The broader task's newly prepared source witnesses and document content are outside this implementation review except where needed to understand source ownership and gate behavior.

## Preservation note

The coordinator promoted this independent report and both hash inventories into
the tracked review record. Diagnostic scripts, patches and logs named above were
created under `.scratch/implementation-cold-review/`; they are transient review
evidence, not production run receipts. Durable regression coverage is in
`tools/tests/test_workflow_proper_study.py`,
`tools/tests/test_proper_components_v2.py`,
`tools/tests/test_content_preflight_study.py`,
`tools/tests/test_document_library.py`, and `tools/tests/test_public_alpha.py`.
The preservation note and inventory path spellings do not amend the reviewer's
findings or verdict.
