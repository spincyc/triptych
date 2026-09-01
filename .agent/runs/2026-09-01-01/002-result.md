---
protocol: relay-v1
run: 2026-09-01-01
turn: 002
role: executor
agent: codex
branch: feature/catena-omnia/b0-b1-selector-oracle
base: 74b95c04fafa82af5f4b0979e74cc316d0199309
answers: .agent/runs/2026-09-01-01/002-brief.md
---

status: complete
work: none
B0_B1_DISPOSITION: ACCEPT

## Files touched

- `.agent/runs/2026-09-01-01/002-claim.md` — relay claim, committed and
  published before review work.
- `.agent/runs/2026-09-01-01/002-result.md` — this independent result.
- No implementation or production path is changed. Three temporary mutations
  of `tools/tests/site_chrome_selector_oracle.mjs` were applied one at a time
  for adversarial checks and restored immediately; the candidate is clean.

## Verification

### Exact target and topology

- Fetched `origin/main` is
  `09437907472581df4a8969010bd494249a3539a5`. The exact candidate is
  `639b9a6fc84b9a169948b951b59972acae24b0a2`; its merge base with
  `origin/main` is that fetched main commit, and `origin/main...candidate` is
  `0 / 15` (candidate fifteen ahead, zero behind).
- The review-branch head after the claim was
  `74b95c04fafa82af5f4b0979e74cc316d0199309`. The candidate is its ancestor.
  The only commits above the candidate before this result were relay-only:
  `788a132bd` (turn-001 brief), `180991c81` (turn-002 rebrief), and
  `74b95c04f` (turn-002 claim).
- `373ce7f98b5d5c05a3b3d5df6acaeaf610bff60b..639b9a6fc84b9a169948b951b59972acae24b0a2`
  is one non-merge commit and changes exactly `PROJECT-WORK.md`,
  `guidance/corpus-browser-implementation.md`,
  `tools/tests/site_chrome_selector_oracle.mjs`, and
  `tools/tests/test_browser_collisions.py`. It contains no production CSS or
  JavaScript, protected Liturgy, Catena, Makefile, release-binding, merge,
  deployment, or signing change.

### Four rereview corrections

- The durable record now states the one-user-state-at-a-time bound and names
  the real `a:focus ~ .site-footer:hover` witness. The changed-path statement
  is truthfully narrowed to the two changed non-record paths.
- Fresh real-Chromium classification refused both required arms and treated
  each as unsafe:
  - `a:focus ~ .site-footer:hover`
  - `.skip-link:focus ~ .site-footer:hover a`
  Each refusal names two distinct stateful compounds and states that the walk
  holds one user state at a time.
- The rule is not a blanket dynamic-selector refusal. `a:hover` remained
  unrefused and unsafe with neutral-shell hover witnesses;
  `.track-page a:hover` remained unrefused and safe in neutral shells; and
  same-compound `a:hover:focus` remained unrefused and reached the skip link
  under the active substate.
- The controller stores the `init` measurements and the test asserts
  `interactive == []` for all 36 shells. The fresh production scan found no
  nonempty interactive measurement.

### Browser authority and production scan

- Chromium, not Python, parses and evaluates selector reach. The page-side
  oracle uses `CSSRule.STYLE_RULE`, `document.querySelectorAll`, CDP selector
  queries, and recorded browser states; the removed Python DOM matcher and
  route-name safety scan are absent. Refusals feed the unsafe verdict.
- Browser: `Chrome/152.0.7977.64` at `/usr/bin/chromium` (Node `v26.8.1`,
  Python `3.14.7`). The fresh scan used one browser session and one batch over
  36 shells: 15 stylesheets, 1,721 arm occurrences, 1,193 unique arms, zero
  refusals, 72 navigations, 433 evaluations, and 2,358 ms scan elapsed after a
  705 ms startup. It walked hover, active, focus, focus-visible, focus-within,
  and target in exactly the two neutral states plus the Scripture preview
  state.
- The only nonzero unsafe inventories were shared `browser-core.css` 10 (the
  furniture owner) and the four protected Liturgy records. All other
  instrument stylesheets, including accepted Scripture scoping, were clean.
  The exact ordered protected inventories, including duplicates, remain:

  ```text
  liturgy/day-missal.css (12):
    body > .site-header
    body > .site-header .triptych-mark
    body > .site-header .triptych-mark i
    body > .site-header .triptych-mark i:nth-child(2)
    body > .site-header .brand a
    body > .site-header .brand span
    body > .site-header nav
    body > .site-header
    body > .site-header .brand span
    body > .site-header nav
    body > .site-header nav a
    body > .site-header
  liturgy/reader-shell.css (3): :root, html, html
  liturgy/reader-instrument.css (2): :root, :root
  liturgy/reader-visual-reset.css (3): :root, a:focus-visible, :root
  ```

- Blocker A remains closed. `check` requires `check-browser-models`, that target
  requires `check-browser-model-coverage`, and its recipe executes
  `test_browser_model_gate`; both the independent Makefile assertions and
  `make -n check-browser-models` reproduce that ordering.

### Adversarial checks

All three were performed against the current candidate with real Chromium and
restored before the next check.

1. Raising the distinct-compound refusal threshold from `> 1` to `> 99` made
   `SelectorOracleSemanticsTest.test_two_simultaneous_user_states_are_refused_rather_than_called_safe`
   fail both required witness subtests: one test run, two failures. Both arms
   lost their refusal and therefore failed open.
2. Injecting a false `interactive` item for the public neutral shell made
   `SelectorOracleSemanticsTest.test_the_states_the_walk_does_not_force_cannot_become_true`
   fail: one test run, one failure identifying `chrome-model (public)` and the
   injected measurement.
3. Forcing the page-side `reach()` authority to return `null` made the complete
   `SelectorOracleSemanticsTest` class materially red: 11 tests run, 43
   failures. Observed identities included
   `test_the_oracle_agrees_with_an_independent_browser_observation` and the
   ordinary `a:hover` reach assertion in the two-state regression test.

### Unmutated commands

- `PYTHONDONTWRITEBYTECODE=1 TRIPTYCH_CHROME=/usr/bin/chromium python -m unittest tools.tests.test_browser_collisions`
  — 36 tests, OK, 9.130 s; no browser skip.
- `PYTHONDONTWRITEBYTECODE=1 python -m unittest tools.tests.test_browser_model_gate`
  — 22 tests, OK, 1.200 s.
- `make check-browser-static` — 6 tests, OK, 0.664 s.
- `make check-browser-models` — its coverage prerequisite passed 22 tests, then
  the fail-fast model loop passed 18, 69, and 60 tests before reaching the
  documented release-integrity sentinel. `test_day_reader_integration` ran 21
  tests with exactly one failure:
  `DayReaderIntegrationTests.test_accepted_shell_and_visual_oracle_hashes_are_current`.
  I then ran every downstream model module the fail-fast target did not reach;
  all seven passed (14, 13, 12, 9, 48, 44, and 39 tests), while the collision
  module independently passed its 36 tests. Thus the gate plus all twelve model
  modules total 405 tests with exactly that one failure and no second identity.
- `git diff --check`, `git status --short`, and `git stash list` were clean after
  restoration and before result preparation.

The one aggregate failure is the review specification's known, unchanged
release-binding oracle, not a selector/model regression. Running
`tools/release-bindings status` independently reported exactly two stale paths
and no third:

```text
src/web/browser/scripture/scripture.css
  recorded c2f974b78d773417736de86980c1caddea88b2c6d3da41b2fbe2435ded1e314b
  actual   e10a02f664099c3681721a346897481384d37f7a7faed97b6133e412430b7075
src/web/browser/sources/sources.css
  recorded a78f8cf835ab9c4486c8664745900fc910474941260faedad0d9d6e1bb8a3ee4
  actual   b039d50e613b9f185acbe8bbc4310b9e05b1913b157e16f4257aaa1fe0b9fa66
```

Neither digest nor either production source changed in the reviewed correction
commit. The governing rereview explicitly requires this exact stale set to
remain unrefreshed and says not to mark B0/B1 defective merely because the same
binding oracle appears inside `check-browser-models`.

## Decisions and deviations

- `B0_B1_DISPOSITION: ACCEPT` because the four prior corrections are genuinely
  closed, their tests are load-bearing, browser authority survives independent
  sabotage, and no new substantive blocker or live production hazard was found.
- An initial timing wrapper used `/usr/bin/time`, which is absent on this host;
  those wrappers exited 127 before running a test. Every required command was
  rerun directly, and only the direct results above are evidence.
- I did not refresh bindings, edit the candidate, merge, deploy, sign, change
  protected ownership, or exercise any Catena Omnia/integration authority.

## Open questions / next step

No review question remains. The later integration/release owner may consume the
`ACCEPT` disposition under separate authority, preserving the existing binding
refresh/signing and protected-owner stop lines.
