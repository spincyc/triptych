# Live Reader — Ritual Flow & Orientation takeover

Recorded: `2026-08-07T14:33:26Z`

Read first:

1. `build/agent-continuity/liturgy-reader-visual-plan.md`, especially
   `Live ritual-flow emergency takeover checkpoint — Codex to next agent`.
2. `build/agent-continuity/liturgy-reader-ritual-flow-baseline.md`.
3. `build/agent-continuity/liturgy-reader-ritual-flow-semantics.md`.

## Boundary

Work began clean and synchronized at
`1bca6a0ee862fce5873d6b0c2d92389e78ca018b`. This checkpoint is an intentional
work in progress created for an immediate maintainer shutdown. It is not an
independent-review candidate.

The implementation/takeover checkpoint is
`85abf971e70e7d1acc8bfa1c29c61ff8c1ff26b3`. It was pushed to `origin/main`;
the automatic Pages run is `31188364101` and was still `in_progress` when this
record was closed. It is not final ritual-flow deployment evidence. Verify and
record its actual disposition before relying on the deployed canonical routes.

The live canonical first viewport, Instrument foundation, four-action shell,
URL/state ownership, renderers, Ordinary seating, source data, candidate/oracle
routes, and public navigation remain frozen as stated in the governing brief.
No liturgical applicability was inferred.

## Implemented

- A static aria-hidden locus hook exists on canonical and retained Day/Propers.
- Day exposes source-held division, element, Proper, seating-anchor, and
  territorial labels; Propers exposes source-held Proper labels.
- The shared shell selects the nearest stable semantic locus above the reading
  boundary, updates it through the existing rAF scroll/resize owner, and never
  writes URL state or emits live announcements.
- The current Contents row remains `aria-current="location"`; opening Contents
  scrolls the real `.surface-body` to center that row when possible, with
  correct end clamping and unchanged focus/Escape/restoration behavior.
- Instrument CSS presents a ruled marginal locus above the desktop rail and a
  compact line in the accepted mobile masthead. Proved rubric cue labels and
  source/apparatus notes are quieter; unresolved conditional forms remain
  visible.
- The governed harness has semantic-location capture, locus/Contents geometry,
  hierarchy/error measurements, targeted assertions, and a 61-state ritual-flow
  capture profile. Day and Propers behavioral harnesses include focused locus
  and Contents ownership assertions.

## Evidence and validation already obtained

- Authoritative baseline (ignored local artifact):
  `build/agent-continuity/liturgy-reader-ritual-flow-baseline-captures-v4/`
  — 61 originals, governed 24/24, zero captured console/request/HTTP/control/ID/
  overflow problems.
- Latest corrected diagnostic matrix (ignored local artifact):
  `build/agent-continuity/liturgy-reader-ritual-flow-corrected-v2/`
  — 61 originals, governed 25/25, zero captured console/request/HTTP problems.
- Focused Python integration tests: 49/49 pass.
- A governed non-capture run: 25/25 pass with zero console/request/HTTP problems.
- Protected geometry in v2 remains exact: Read width 636 px at 1440 and 768;
  first principal text 306.09 px (Read 1440), 316.98 px (Roman Missal 1440),
  320.66 px (Roman Missal 393), and 336.84 px (Roman Missal 320).

The corrected-v2 matrix predates the final small shell edit. That edit changes
heading-visible behavior from hiding the locus entirely to showing the major
division alone when the current unit heading is already visible. It fixed the
observed mobile Canon loss of major context but has not yet been rerun.

## Must be done next

1. Rebuild the locked preview:

   `PATH="$PWD/build/visual-reset-venv/bin:$PATH" tools/tpt public-alpha build --preview`

2. Run syntax checks, then complete Day, Propers, shared-shell and governed
   Instrument browser suites. The last combined Day/Propers run was interrupted
   for shutdown after its discovered test-side smooth-scroll/scroller-owner
   defects were fixed.
3. Capture a new corrected-v3 61-state matrix and inspect every original at full
   size. Do not treat v2 as final.
4. Resolve the mobile `locus.obscuredTextCount` evidence. V2 reports one
   geometrically intersecting underlying text range in several sticky-masthead
   states. Prove zero actual obscuration or change the presentation; do not
   silently redefine the requested measurement.
5. Complete bounded RF-D/RF-E only where the semantic inventory proves the
   classification. Roman alternative-looking Preface/forms cannot currently be
   subordinated by inferred applicability.
6. Update release hashes, run all locked local gates, commit/push coherent
   checkpoints, verify exact Pages runs and deployed canonical routes, produce
   final sheets/measurements, and seal the authorized immutable ritual-flow
   handoff directory and ZIP.

## Do not do

- Do not add source, selection, assembly, Ordinary seating, renderer, Bible,
  territorial, translation, or applicability logic.
- Do not redesign the first viewport, shell actions, Date/Browse, navigation,
  candidate/oracle routes, or public state.
- Do not force-add exploratory capture directories. Only the final immutable
  handoff and its ZIP have large ignored-artifact authority.
- Do not claim the unrelated stored-example replay is green or recapture it.

## Files currently in scope

Product/presentation:

- `src/web/browser/liturgy/day.html`
- `src/web/browser/liturgy/day-reader.html`
- `src/web/browser/liturgy/index.html`
- `src/web/browser/liturgy/propers-reader.html`
- `src/web/browser/liturgy/day-reader.js`
- `src/web/browser/liturgy/propers-reader.js`
- `src/web/browser/liturgy/reader-shell.js`
- `src/web/browser/liturgy/reader-instrument.css`

Tests/evidence ownership:

- `tools/tests/day_reader_integration_browser.mjs`
- `tools/tests/propers_reader_integration_browser.mjs`
- `tools/tests/liturgy_reader_visual_reset_browser.mjs`
- the three corresponding focused Python integration modules.

Tracking/continuity:

- `PROJECT-WORK.md`
- `guidance/liturgy-browser-roadmap.md`
- `promised-deliverables.toml`
- the four ritual-flow continuity documents.
