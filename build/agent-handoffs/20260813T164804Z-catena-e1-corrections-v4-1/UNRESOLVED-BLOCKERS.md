# Unresolved blockers, and who owns them

None of these is this lane's to close. Each is listed so the reviewer can see it
was left deliberately rather than missed.

## Owned by release

- **Four stale Catena site-source bindings**, unchanged in count from the base:
  `catena-model.js`, `catena.css`, `catena.js`, `index.html`. `catena.js`'s
  *actual* hash moves with this correction, but it was **already stale at the
  base**, so the count stays 4 and no new binding is made stale.
- **No release record was re-signed, refreshed or edited by this lane.**
  `check-release-bindings` reporting `stale: 4` is the intended state, not a
  failure to fix.

## Owned by the day-reader / liturgy lane

- `test_candidate_does_not_leak_fixture_or_discovery_records` and its two
  siblings. See `DATA-TEST-CONTRADICTION.md`. Untouched here.

## Owned by the common browser gate

- `single-main-element` (117), `primary-controls-meet-target-size` (82) and
  `skip-link-targets-existing-element` (27) fail across the whole site at both
  base and head, identically. They are shared-shell/gate defects, not Catena's,
  and this lane changed nothing about them.

## Owned by the tool registry and examples lanes

- `check-tool-registry` and `check-examples` fail at base and head identically.

## Owned by B0 / shared shell

- `src/web/browser/shared/` is byte-identical to the base. Nothing here.

## Still open from V4, and NOT closed by this lane

- The deterministic Catena data root.
- Real assistive-technology validation. V4's `AT-LIMITATION.md` stands: this lane
  produced screenshots, which prove rendering, not announcement. No screen
  reader or AT bus was exercised. See `SCREENSHOT-METHOD.md`.
- The two deliverables the V3 reviewer reopened
  (`unsupported-voice-distinguished-from-shape`,
  `displayed-provenance-typed`). Note the record discrepancy inherited from V4:
  the reviewer's `open` status lives on the review branch, which is **not an
  ancestor of this branch**, so at this head both already read `pass` from the
  V3 lane. This lane did not touch `promised-deliverables.toml` and did not
  self-certify either criterion.

## E1 status

**Awaiting fresh independent review.** Not accepted, not integrable, not merged,
not re-signed, not deployed.
