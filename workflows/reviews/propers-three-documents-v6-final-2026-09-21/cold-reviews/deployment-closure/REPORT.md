# Final deployment closure cold review

**Verdict: PASS**

Reviewed the deployment-closure working tree at `HEAD` `b048fa37e8e784fbcc351bce201f9e676d3d5008`. This review made no tracked edits.

## Remote and workflow identity

- `git ls-remote origin refs/heads/main` returned exactly `b048fa37e8e784fbcc351bce201f9e676d3d5008`.
- GitHub Actions run `35691184227` is the `Publish GitHub Pages` workflow, triggered by a push to `main`, with `headSha` exactly `b048fa37e8e784fbcc351bce201f9e676d3d5008`, status `completed`, and conclusion `success`.
- Its recorded creation/start and completion/update times agree with `deployment-evidence.json`: `2026-09-22T05:33:38Z` through `2026-09-22T05:44:33Z`. The sole deploy job completed successfully; its conditional restored-corpus installation step was skipped after fresh container typesetting succeeded, exactly as the evidence limit states.

## Deployment evidence and artifacts

Parsed all 16 route records in `deployment-evidence.json`. For every record, the retained `.scratch/live-route-00` through `live-route-15` response and the named `build/public-alpha/site/...` file have the recorded byte count and SHA-256 digest and are byte-identical to one another. URL paths map exactly to their local artifact paths. The aggregate is correctly stated as four HTML routes and twelve PDF routes, all HTTP 200 and all byte-identical.

All twelve deployed PDF identities also match the corresponding records in `artifact-identities.json`. All sixteen installed canonical artifacts (twelve PDFs and four canonical Markdown web editions) match that durable identity record. The distinct canonical-Markdown and rendered-site-HTML digests are correctly associated with their respective layers.

## Closure records and promises

The working-tree diff is limited to the new deployment evidence and four closure documents: `PROJECT-WORK.md`, `promised-deliverables.toml`, the final review `README.md`, and `release-checks.md`. The prose consistently identifies the exact commit, Pages run, route count, HTTP result, and byte-identity result.

The promise diff changes only two deliverable states from `in_progress` to `complete` and their two deployment-dependent requirements from `open` to `pass`: `format-main-deployment` and `recovered-main-and-pages`. Every other requirement in both deliverables was already `pass`; both now have zero non-passing requirements. `make check-promised-deliverables` passes with 40 tracked and 31 complete. The closure therefore records newly observed facts rather than relaxing any criterion.

## Rite isolation

Direct scans of the four active leaf trees, excluding inert historical evaluation packets, found no path from either 1962 leaf into the postconciliar tree and no path from either postconciliar leaf into the 1962 tree. Each leaf retains its own document identity and calendar (`roman-1962` or `postconciliar`), while postconciliar shared-formulary paths remain inside the exact U.S. 2011 tree. The focused component/workflow suite passed 71 tests, including opposite-calendar content rejection, postconciliar locale separation, cross-family research evidence rejection, recorder-input rejection, release-catalog rejection, and exact family catalog resolution.

## Final checks

- `git diff --check`: PASS.
- `make check-promised-deliverables`: PASS; 40 tracked, 31 complete.
- Focused proper component and proper-study workflow suite: PASS; 71 tests.
- Origin/main exact-SHA check: PASS.
- Pages exact-SHA/conclusion check: PASS.
- Sixteen retained live/build byte comparisons: PASS; zero mismatches.
- Artifact identity reconciliation: PASS; 16 checked, zero mismatches.

No deployment-closure blocker was found.
