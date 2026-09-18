# September 20 production recovery

The interrupted work was recovered on 18 September 2026 from checkpoint
`6f552cc63729bfa2a6970c13bdf92bf1257651db` and its uncommitted changes.
This record distinguishes preserving and deploying accepted publications from
completing the later pagination requirement.

## Publication boundary

The accepted proper-study v1 productions remain the publication candidates:

| Owner | Research PDF | Concise PDF | Homily |
| --- | ---: | ---: | ---: |
| 1962, Seventeenth Sunday after Pentecost | 23 pages | 5 pages | 4 pages |
| U.S. 2011, Twenty-fifth Sunday in Ordinary Time, Year A | 20 pages | 5 pages | 4 pages |

Their six exact PDF identities and two canonical web identities are recorded in
the [prior integration review](../propers-three-documents-integration-checkpoint-2026-09-17/REPORT.md).
That acceptance does not cover the requested 10–12-page concise revision.
The promise remains blocked, with its unmet criteria preserved.

A fresh sandboxed production-runner availability probe was refused by an
account usage limit. The reported reset was 20 September, 06:23, without a
timezone. No new v3 run was seeded, no author or review verdict was fabricated,
and no earlier accepted state or verdict was rewritten.

## Recovered contract

`guidance/REPORT.md` and `guidance/final/` retain the previous independent
guidance review and its frozen subjects. All 23 subject hashes were checked
against both the recovered worktree and the retained snapshot. The report
explicitly excludes implementation acceptance and revised Sunday production.
The supporting implementation hashes identify the seams that reviewer read;
they do not substitute for implementation regression tests.

## Integration checks performed during recovery

- The 12 incoming feature commits contained 717 distinct added or modified
  blobs. A bounded disclosure screen found no private checkout path, private-key
  header, GitHub-token pattern or API-key pattern. This is not a general secret
  scanner or a new source-rights determination; the existing source and rights
  reviews remain controlling.
- All 210 approved PDFs outside the two Sunday families were rebuilt and
  installed through their ordinary Make targets: 152 GPT and 58 Claude.
  Every previously installed PDF in that set retained its exact hash.
  The two held Claude proper-54 outputs were not built or published.
- Both Sunday component artifact checks passed under historical schema-2
  validation. The new presentation contract was not assigned retrospectively.
- The focused scoped-metadata and web-edition regression run passed all
  **89 tests**.
- The broader metadata/web run executed **124 tests** and failed in one
  historical install-commit test, with 187 reported assertion/subtest failures.
  That test class is byte-identical on `origin/main`; main already carries
  186 recorded install commits but no reachable provider-PDF installation
  history after the authorized PDF-history removal. Its hard-coded expected
  count is also 187. This inherited test defect was not weakened or treated
  as a successful check.

The initial deployment-source check failed on catalogue drift. After the full
corpus rebuild, normal catalogue regeneration changed only the current
workflow version and digest. Its existing `preserve_uninstalled_facts` rule
retains the unchanged held publication's historical 77-page extent without
creating a PDF route or installing it. A comparison generated into an empty
scratch destination had no prior catalogue from which to retain that fact;
its 6,143-page total was not the normal tracked projection. The reconciled
catalogue remains 142 works, 194 documents, 218 issues and 6,220 recorded
canonical pages. Final deployment gates are separate from this diagnostic.

The inherited Pages failure was run
[34624274546](https://github.com/spincyc/triptych/actions/runs/34624274546),
at main commit `b27036f9b856bd8f662f51b6e6128bd90a5ed633`.
It failed while typesetting the held proper-54 synthesis, before deployment.
The repair must derive build and cache targets from the renderer's existing
publication selection, not waive the held document's failed pagination gate.

After catalogue reconciliation, `make check-deployment-sources` exited **0**.
The final local identity check again matched all six accepted PDF hashes and
both accepted canonical Markdown hashes. Both component artifact gates passed.
Recomputing each historical-default review seal matched all **12/12** accepted
`review_inputs` records, without assigning the v3 review contract retroactively.
`tools/tpt check-promised-deliverables` and `tmt check` also exited **0**.
These checks establish the preserved publication boundary, not a deployment
result or acceptance of the blocked revised documents.

## Recovered implementation and deployment review

The [implementation review](implementation/IMPLEMENTATION_REVIEW.md) found and
corrected invalid citation endpoints being lost during cross-chapter expansion
and whole-leaf chronology checks mixing research and concise coverage. Its
final eleven hashes are retained in `implementation/SHA256SUMS`. The coordinator
inspected both corrective patches and independently reran their three focused
tests, exit **0**, before freezing these bytes.

The implementation's final focused run passed **49/49** tests, including real
TeX pagination. Its broader runs were not wholly green: **333/334** extended
tests and **928/929** workflow tests, each with the same inherited 15-versus-16
leaf-count assertion; **322/324** chronology/component tests, with two tests
requiring an absent historical Git object. Exact commands, timing boundaries
and baseline comparisons remain in the retained review and `checks.txt`.
These inherited defects were neither waived nor silently repaired.

The independent [Pages review](pages-review.md) accepted the exact scoped fix:
**154** scoped tests and **10** independent adversarial tests passed. Real
selection and Make install edges agree on **158 GPT + 58 Claude** PDFs,
excluding exactly the two held proper-54 outputs. Normal validation remains
in both cache paths. Its expanded 195-test run has the same inherited
187-assertion install-history failure; it is not described as green.

Final local gates all exited **0**:

```sh
make check-sources
make check-release-bindings
make check-deployment-sources
make public-site
tools/tpt public-alpha verify --deployment-target github-pages
```

The scoped release refresh changed only the reviewed component helper and
current-workflow catalogue hashes, their two generated rights-table rows and
the rights-record hash. It changed no approval text, publication status,
source-rights determination or reading-plan PDF binding.

Both review transport directories were created, and both sibling ZIPs were
created and verified, under ignored `build/agent-handoffs/`:

- `20260918T123800Z-sunday-recovery-pages`
- `20260918T124634Z-proper-study-v3-implementation`

The latter preserves the reviewer's earlier scratch package and records the
coordinator's corrective-patch inspection. Neither package is committed.
Actual main integration, Pages execution and live-route verification remain
pending at this checkpoint. New v3 productions remain quota-blocked.

## Main publication verified

The preparation above was followed by a fast-forward push of
`362cd5d1a42b7ed2b255748750a0aa7ca1ca70c8` to `main`, without rewriting history.
The exact 15-commit outgoing range was inspected, including a bounded screen
of **836 blobs** with no private-path or credential-pattern finding. The
working tree was clean; no ignored transport package entered the range.

[Pages run 35346638189](https://github.com/spincyc/triptych/actions/runs/35346638189)
completed successfully at **2026-09-18 12:59:35 UTC**, exercising the real pinned
container path, deployment-source gate, site build and Pages compatibility
verification before successful deployment.

[The retained evidence](deployment-evidence.json) records live verification
after that run: all **six PDFs and two canonical web routes returned HTTP 200**
and matched the local verified artifact byte-for-byte. All six PDF hashes are
the previously accepted identities, not newly accepted replacements. Both held
proper-54 PDF routes returned **404** and are absent from the local artifact.

This completes the recovery/main/Pages requirement only. It does not meet or
close the 10–12-page concise-document revision, waive the required fresh
productions, or convert any inherited broad-suite failure into a pass.
