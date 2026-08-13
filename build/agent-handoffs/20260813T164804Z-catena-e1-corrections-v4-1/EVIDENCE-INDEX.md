# Evidence index

Every path below resolves inside this package.

## Records

| File | What it establishes |
| --- | --- |
| `HANDOFF.md` | task, branch, SHAs, changed files, startup commands, inventory |
| `REVIEW_REQUEST.md` | the questions needing external judgment, as Blockers and Optional feedback |
| `REFUSAL-COPY.md` | the verbatim review requirement, the before/after strings, why each old string failed, and the regression that pins the fix |
| `SCREENSHOT-METHOD.md` | that headless capture is possible here, the probe output proving it, the exact commands, and the honest limits |
| `VISUAL-STATE-INDEX.md` | for all 53 images: exact head, route/state, viewport, browser mode, requirement demonstrated |
| `BASELINE-COMPARISON.md` | base vs head, every difference classified |
| `DATA-TEST-CONTRADICTION.md` | the preserved `src/web/data/` conflict and the question it leaves |
| `UNRESOLVED-BLOCKERS.md` | separately owned blockers and their owners |
| `LIMITATIONS.md` | what this package does not prove |
| `PRIVACY-AUDIT.md` | sanitization method and result |
| `checks.txt` | every check, exact command, numeric exit |
| `commits.txt` | base / head / review SHAs |
| `changes.patch`, `changed-files.txt` | the exact diff |
| `MANIFEST.sha256` | SHA-256 of every member |

## Logs

| File | What it shows |
| --- | --- |
| `logs/focused-catena-suite.log` | 267 tests, OK — 266 inherited + 1 new regression |
| `logs/all-tests-base.log` | base full discovery: 1,617 / 14F / 13E / 11S |
| `logs/all-tests-head.log` | head full discovery: 1,618 / 14F / 13E / 11S |
| `logs/browser-gate-base.json` | base gate report, 2,290 assertions |
| `logs/browser-gate-head.json` | head gate report, 2,290 assertions |
| `logs/gate-comparison.log` | the object-for-object comparison and its key-by-key table |
| `logs/make-k-check-base.log` | base `make -k check`, exit 2, three targets |
| `logs/make-k-check-head.log` | head `make -k check`, exit 2, the same three |
| `logs/budgets-head.log` | the four gzip measurements against their ceilings |
| `logs/misc-checks-head.log` | promised deliverables, catena replay, release bindings, PayloadTest |
| `logs/public-site.log` | the head site build |

## Tools shipped as evidence

| File | Why it is here |
| --- | --- |
| `logs/capture-catena.mjs` | produced the route-state images; lane-local because the shared gate carries no fail-closed Catena address |
| `logs/capture-provenance.mjs` | produced the two focused-region provenance images |
| `logs/compare-gate.py` | produced the gate comparison; the repository has no gate-comparison tool |
| `logs/sanitize-and-seal.py` | carried forward from the V4 package; sealed this one |

## Screenshots

53 PNGs in `screenshots/`, plus `after--capture-index.json`,
`before--capture-index.json` and `after--provenance-index.json`, which record
for each image its route, viewport, variant, emulated media and the URL the page
held after load. `VISUAL-STATE-INDEX.md` is the human-readable index.

Naming follows `guidance/external-review-handoffs.md`:
`<before--|after--><surface>--<state>--<WxH>[--<variant>].png`.
