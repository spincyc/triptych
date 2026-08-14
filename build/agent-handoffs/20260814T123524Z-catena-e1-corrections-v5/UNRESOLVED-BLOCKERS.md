# Unresolved blockers — every one with its owner, none touched by this lane

This lane fixed nothing outside the Catena route/model/test seam, and worked
around nothing. Each entry below is open, owned elsewhere, and recorded rather
than repaired.

## 1. Four stale Catena release bindings — the release owner

`tools/tpt release-bindings status` reports four stale site sources and exits
non-zero:

| Path | State |
| --- | --- |
| `src/web/browser/catena/catena-model.js` | stale against a **new** digest, because V5 changed the file deliberately |
| `src/web/browser/catena/catena.js` | stale against a new digest |
| `src/web/browser/catena/catena.css` | stale, and **byte-identical to V4.1** — inherited, not caused here |
| `src/web/browser/catena/index.html` | stale, and byte-identical to V4.1 — inherited |

The count is unchanged from V4.1: four before, four after. **None was
re-signed.** `refresh-release-bindings` and `approve-release` were not run.
Failing closed here is the correct behaviour for a candidate awaiting review,
and repairing it would be re-signing a release record this lane does not own.

## 2. The `src/web/data/` test contradiction — the Day-reader owner

`test_candidate_does_not_leak_fixture_or_discovery_records` and
`test_candidate_and_contract_fixtures_do_not_leak_into_generated_data` fail
against paths under `src/web/data/`.

**V5 changed no data.** `git diff --name-only` against the parent lists three
files, none under `src/web/data/`. The failing paths are the Catena voice-key
projection the V3 review explicitly authorised through the owning generator,
plus two Propers paths that predate V4.

The V4.1 review classified this as **"C: a separate owner/test mismatch, with
an authorized exception"** and required the protected Liturgy/Day-reader owner
to re-review the integrated generated data and reform its historical `af6c0c8`
tripwire with an exact baseline and explicit acceptance status.

This lane did not weaken, delete, whitelist, expect-mark or otherwise
accommodate that test, and added no `src/web/data/` change of its own. See
`DATA-TEST-CONTRADICTION.md`.

## 3. The common browser-gate failure population — the shared shell owner

The gate reports 226 failures at both the base and the head, in an identical
set: `single-main-element` (117), `primary-controls-meet-target-size` (82) and
`skip-link-targets-existing-element` (27). These are shared-shell composition
facts, not Catena facts, and `logs/compare-gate.py` shows the whole report
deep-equal across the two runs.

## 4. `check-tool-registry` — the tool-registry owner

`tmt check` reports sibling-declaration findings: a tool body naming a sibling
id without declaring it in `requires`. Inherited, unrelated to this seam, and
identical at base and head.

## 5. `check-examples` — the tool-documentation owner

`scripts/replay_examples.py` reports transcript divergences, including the
already-recorded deliverable-count drift. Inherited. **Note that V5 changes the
tracked deliverable count from 29 to 30, so a divergence of that kind may shift
by one; `checks.txt` records the base and head sets so the reviewer can see
exactly which entries moved and why.**

## 6. Real-device or assistive-technology evidence — the accessibility owner

No AT bus or screen reader was available. `probe-catena.mjs` reads `aria-busy`,
the status region and the focused element in real Chromium; it does not prove
what a screen reader announces. V4's `AT-LIMITATION.md` is not superseded.

## 7. The `python-markdown` version mismatch — environment

The V4.1 review recorded local Python Markdown 3.10.3 against the locked
3.10.2. Environment-sensitive, unrelated to this seam, identical at base and
head.

---

None of the above is a reason to accept or reject V5. Each is listed so the
reviewer can tell what this lane owns from what it does not, and so no green
claim is made over a red repository.
