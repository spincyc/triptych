# Evidence index

Every path below resolves inside this package.

## Records

| File | What it establishes |
| --- | --- |
| `HANDOFF.md` | the task, the branch, the ancestry, the focused files, the inventory, and what is deliberately absent |
| `REVIEW_REQUEST.md` | the four blocking and four optional questions this lane could not settle for itself |
| `TYPED-PRESENTATION-BOUNDARY.md` | what the correction is, where it lives, and why the model rather than the page |
| `BASELINE-COMPARISON.md` | base against head for every suite, gate and measurement |
| `PROBE-DIFFERENCE.md` | the real-Chromium before/after, field by field, for all six probed states |
| `REGRESSIONS-FAIL-ON-PARENT.md` | that the new regressions fail on the code they were written to catch |
| `DATA-TEST-CONTRADICTION.md` | that no `src/web/data/` path changed and the guard was not weakened |
| `UNRESOLVED-BLOCKERS.md` | seven open items, each with its owner, none repaired here |
| `LIMITATIONS.md` | nine things this package does not prove |
| `PRIVACY-AUDIT.md` | the sanitization method, its result, and the sealer's own audited gaps |
| `SCREENSHOT-METHOD.md` | how the evidence was produced, and which parts of it are fabricated |
| `VISUAL-STATE-INDEX.md` | one row per PNG |
| `commits.txt` | the ancestry, and the proof that the records commit touches no code |
| `changed-files.txt` | `git diff --name-only` against the parent, bare |
| `changes.patch` | the exact parent→head diff |
| `checks.txt` | every command run, its numeric exit, its result, its qualification |
| `MANIFEST.sha256` | SHA-256 of every member except itself |

## Logs

| File | What it shows |
| --- | --- |
| `logs/focused-catena-head.log` | the 306-test focused suite at the head |
| `logs/focused-catena-base.log` | the 267-test focused suite at the base |
| `logs/all-tests-head.log` | full discovery at the head |
| `logs/all-tests-base.log` | full discovery at the base |
| `logs/names-head.txt`, `logs/names-base.txt` | the sorted FAIL/ERROR name sets the comparison is made over |
| `logs/make-k-check-head.log` | `make -k check` at the head |
| `logs/browser-gate-head.json`, `logs/browser-gate-base.json` | the two full gate reports |
| `logs/gate-comparison.log` | `compare-gate.py` over them |
| `logs/probe-head.json`, `logs/probe-base.json` | the live-DOM and resource-log reports from real Chromium |
| `logs/budgets-head.log` | the four gzip-9 measurements at the head |
| `logs/misc-checks-head.log` | catena check, promise ledger, release-binding status |
| `logs/public-site.log` | the build the probe and gate ran against |
| `logs/new-tests-against-base.log` | the V5 test file replayed against the parent implementation |

## Tools shipped as evidence

Lane-local, following the precedent V4 set with `sanitize-and-seal.py`.
`REVIEW_REQUEST.md` §7 asks whether they belong in `tools/` instead.

| File | What it is |
| --- | --- |
| `logs/probe-catena.mjs` | **new in V5.** Reads the live DOM and resource log in headless Chromium under injected malformed fixtures, at a base and a head, and optionally captures the states whose rendering visibly differs. The only instrument here that can evidence malformed-data behaviour at all. |
| `logs/sanitize-and-seal.py` | carried forward from V4.1 with six named additions; normalize → scan → index-check → manifest, refusing to write a manifest on any hit |
| `logs/capture-catena.mjs` | carried forward unmodified; visits only real corpus addresses, and therefore cannot reach any state under review here |
| `logs/capture-provenance.mjs` | carried forward unmodified; not re-run for V5 |
| `logs/compare-gate.py` | carried forward unmodified; deep-equals two gate reports, excluding four volatile keys |

## Screenshots

Twenty PNGs, five states × two viewports × before/after, plus two machine
indexes. Filenames follow the repository grammar
`<before--|after-->catena--<state>--<WxH>.png`; `before--` is the V4.1 base and
`after--` is this head.

Every image is a page under **fabricated adversarial data**. None shows a
holding of this project. `SCREENSHOT-METHOD.md` and `LIMITATIONS.md` §1 state
this in those words.

| Image | State |
| --- | --- |
| `screenshots/before--catena--malformed-language-everything-held--1440x900.png` | a language chip named from a value that is not a language code |
| `screenshots/before--catena--malformed-language-everything-held--393x852.png` | a language chip named from a value that is not a language code |
| `screenshots/after--catena--malformed-language-everything-held--1440x900.png` | a language chip named from a value that is not a language code |
| `screenshots/after--catena--malformed-language-everything-held--393x852.png` | a language chip named from a value that is not a language code |
| `screenshots/before--catena--mixed-collection-members--1440x900.png` | a null collection member replacing the whole page with a JavaScript error |
| `screenshots/before--catena--mixed-collection-members--393x852.png` | a null collection member replacing the whole page with a JavaScript error |
| `screenshots/after--catena--mixed-collection-members--1440x900.png` | a null collection member replacing the whole page with a JavaScript error |
| `screenshots/after--catena--mixed-collection-members--393x852.png` | a null collection member replacing the whole page with a JavaScript error |
| `screenshots/before--catena--typed-absence-findings--1440x900.png` | the absence summary, manufactured against typed |
| `screenshots/before--catena--typed-absence-findings--393x852.png` | the absence summary, manufactured against typed |
| `screenshots/after--catena--typed-absence-findings--1440x900.png` | the absence summary, manufactured against typed |
| `screenshots/after--catena--typed-absence-findings--393x852.png` | the absence summary, manufactured against typed |
| `screenshots/before--catena--malformed-word-tallies--1440x900.png` | word-count chips from a boolean and a fraction |
| `screenshots/before--catena--malformed-word-tallies--393x852.png` | word-count chips from a boolean and a fraction |
| `screenshots/after--catena--malformed-word-tallies--1440x900.png` | word-count chips from a boolean and a fraction |
| `screenshots/after--catena--malformed-word-tallies--393x852.png` | word-count chips from a boolean and a fraction |
| `screenshots/before--catena--malformed-canon-bootstrap--1440x900.png` | the page standing at "Loading…" for ever |
| `screenshots/before--catena--malformed-canon-bootstrap--393x852.png` | the page standing at "Loading…" for ever |
| `screenshots/after--catena--malformed-canon-bootstrap--1440x900.png` | the page standing at "Loading…" for ever |
| `screenshots/after--catena--malformed-canon-bootstrap--393x852.png` | the page standing at "Loading…" for ever |

The machine inventories are `screenshots/after--probe-index.json` and
`screenshots/before--probe-index.json`: file, state, address, viewport,
variant, media, what the image shows, and byte length.
