# Unresolved blockers — what this lane did not touch, and whose they are

Each item below is open, is recorded rather than repaired, and belongs to an
owner other than this lane. None was worked around, whitelisted, weakened,
expect-marked, or counted as a V6 result.

## 1. Four stale release bindings — the release owner

`python3 tools/tpt release-bindings status` exits 1 with four stale bindings,
including the digest of `src/web/browser/catena/catena-model.js`, which this correction changed. That
is the guard working: a changed route asset whose binding has not been
re-approved is supposed to fail closed. **No binding was re-signed and
`refresh-release-bindings` / `approve-release` were not run.** Re-signing is the
release owner's act and is not authorized by any disposition on this lane.

This is also why `check-examples` diverges: its captured
`tools/public-alpha verify --preview` invocation reports the same unsigned
condition.

## 2. The `src/web/data/` test contradiction — the Day-reader owner

`test_day_reader_integration.DayReaderIntegrationTests` fails two tests
(`test_data_legacy_shell_css_and_visual_oracle_are_frozen` and
`test_candidate_does_not_leak_fixture_or_discovery_records`) because a guard
asserts that **no** path under `src/web/data/` has changed since `af6c0c8df`,
while a prior review separately authorized exactly one such change. The two
records contradict each other.

V6 changed nothing under `src/web/data/` — `git diff --name-only` against the
parent lists three files, none of them data — so this lane neither caused the
contradiction nor is entitled to resolve it. **Both failures reproduce
identically at the parent**, which is recorded in `checks.txt` with both runs.
See `DATA-TEST-CONTRADICTION.md`.

## 3. The common browser-gate failure population — the shared shell

The gate reports 226 failing assertions at both the parent and this head, and
the two whole reports are deep-equal excluding four volatile fields. The
failures are `primary-controls-meet-target-size` (82),
`single-main-element` (117) and `skip-link-targets-existing-element` (27), and
they are properties of the shared shell and the common gate, not of the Catena
route. This lane did not repair them and must not: the gate is commonly owned
and a Catena-local fix would move a shared failure into one route's history.

## 4. `check-tool-registry` — the tool-registry owner

`tmt check` exits non-zero at the parent and at this head, unchanged. V6 adds
no file to `tools/` and registers nothing; the sealer and the probe ship inside
the handoff package as lane-local instruments, following the precedent V4 set,
precisely so that this target is not touched.

## 5. Real-device and assistive-technology evidence — the accessibility owner

No AT bus or screen reader was available. The probe reads `aria-busy`, the
status region's text, the visible failure paragraph and
`document.activeElement` in real Chromium; **it does not prove what a screen
reader announces.** V4's AT-limitation record is not superseded. This is stated
again in `LIMITATIONS.md` §3, where the exact instrument is described, because
V5's equivalent record over-stated an instrument that read no focus at all.

## 6. Protected Liturgy, PDFs, B0/shared-shell cutover — separate lanes

Untouched. No file under those owners appears in the V6 diff.

## 7. The disposition itself

E1 remains **awaiting fresh independent review**. This lane records no
acceptance of its own work, and nothing in this package is offered as one.
