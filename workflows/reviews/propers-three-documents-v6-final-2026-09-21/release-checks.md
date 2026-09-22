# Local release checks

Final local candidate checked on 22 September 2026. Commands were run from the
repository root after both v6 archives, production records, inventories,
projections, generated web editions and scoped release bindings were settled.

| Check | Result |
| --- | --- |
| Four `scripts/_proper_study.py check --phase publication --require-presentation --require-format` invocations | PASS |
| Four scoped `tools/tpt public-alpha check` invocations | PASS |
| Four scoped `tools/tpt document-library check` invocations, run serially | PASS |
| `tools/tpt document-library structure --check` | PASS; 142 works, 196 documents, 224 issues, 6,281 pages |
| GPT publication source inventory | PASS; 142 publications, 2,360 source-surface files, 11 owners |
| Claude publication source inventory | PASS; 54 publications, 1,322 source-surface files, 5 owners |
| `tools/tpt source-library validate` | PASS; 2,746 artifacts, 992 editions, 5,182 passages, 726 works, 2,868 bindings |
| `tools/tpt source-family-migration check` | PASS; 153 review units remain honestly pending |
| `make check-web-editions-current` | PASS |
| `make check-publication-inventories` | PASS |
| `make check-release-bindings` | PASS; zero stale bindings |
| `make check-sources` | PASS |
| `make check-deployment-sources` | PASS |
| `make public-site` and `make verify-public-site` | PASS |
| `tools/tpt public-alpha verify --deployment-target github-pages` | PASS |
| `make check-promised-deliverables` | PASS; 40 tracked, 29 complete before deployment closure |
| `git diff --check` | PASS |
| `/home/ksh/.local/bin/tmt check --json` | PASS; no failures or warnings |
| Focused format/component/workflow/chronology modules | PASS; 224 tests |

One attempt ran four document-library checks concurrently. A shared disposable
`build/document-library-replay.json` was removed by a sibling command before a
Node comparison opened it, producing one `ENOENT`. Running the same four checks
serially immediately passed. No tracked byte or document result changed; the
final evidence is the serial run.

The exact candidate commit
`b048fa37e8e784fbcc351bce201f9e676d3d5008` was pushed to `main`.
GitHub Pages run
[35691184227](https://github.com/spincyc/triptych/actions/runs/35691184227)
completed successfully after fresh typesetting and all deployment checks.
Post-deployment retrieval verified HTTP 200 and byte identity against the
verified Pages artifact for four canonical HTML routes and twelve PDF routes;
the per-route evidence is retained in
[deployment-evidence.json](deployment-evidence.json).
