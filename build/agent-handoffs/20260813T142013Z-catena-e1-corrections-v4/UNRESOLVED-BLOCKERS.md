# Separately owned prerequisites — open, and not touched by this lane

None of these is closed, worked around, or affected by V4. They are recorded
here so they cannot disappear between packages. Each is owned elsewhere.

## Generator / data

- Psalm projection.
- Lead reconciliation and its missing confidence.
- Full licence projection.
- Any broader generator or data correction **not** required by the exact
  Catena voice-key projection.

The voice-key index seam is the **one** generator/data seam this lane entered,
and only because the V3 independent review authorised it explicitly. See
`VOICE-KEY-PROJECTION.md`.

## Release

- Three stale Catena bindings at the V3 head — `catena.js`, `catena.css` and
  one further site source. **V4 makes a fourth binding stale**, because it
  changes `catena-model.js` for the reasons recorded in `HANDOFF.md`. No
  release record was re-signed, refreshed, or edited by this lane;
  `check-release-bindings` reports them, and that report is the intended
  outcome, not a failure to fix.
- The deterministic Catena data root.

## Common browser gate

- The common-gate voice-sample decision.

## B0 / shared shell

- The nested `main` finding.
- Target-size findings.
- Skip-target findings.
- Shared history and visible-focus findings.
- Shared reflow findings.

`src/web/browser/shared/` is byte-identical at this head. The Catena route
calls into it and changes nothing in it.

## Real device / assistive technology

- Real-device or successful real-AT evidence, which remains a pre-release
  prerequisite. See `AT-LIMITATION.md`, and read its negatives as
  session-scoped.
- Genuine system forced colors. The forced-colors evidence here is emulated
  and is disclosed as such.

## Inherited repository debt

- The registry and example failures that stand at the base and still stand at
  the head. They are unrelated to Catena and are not this lane's to fix; they
  are classified in `BASELINE-COMPARISON.md`.

## Not entered at all

Protected Liturgy and the PDFs were not entered by this lane.
