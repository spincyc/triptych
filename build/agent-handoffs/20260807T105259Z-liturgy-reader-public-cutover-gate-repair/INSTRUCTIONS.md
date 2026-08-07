## Independent cutover-gate repair authorization — reviewer to Codex

Liturgical Instrument — Cutover Gate-Repair Authorization
Disposition

THE EXECUTION STOP WAS CORRECT.

The public cutover was not executed, the canonical public reader bytes remain unchanged, and the successful Pages run after the stop was continuity-only. Treat this as a pre-deployment gate defect in the sealed cutover patch, not as a product rollback or a failed public cutover.

This document authorizes one narrow phase:

    Repair and reseal the cutover patch so that the exact promoted canonical state passes all task-owned pre-deployment gates.

This phase does not authorize canonical promotion, a public deployment, navigation changes, candidate/oracle cleanup, visual redesign, renderer/state refactoring, source expansion, or any live product change.

After the replacement patch is proved green and sealed, stop for narrow independent review before attempting execution again.
Verified stop boundary

Current synchronized boundary:

e20b2f542ab51a2b4f0807e6394ca5ecb313699c

Durable stop record:

90fe6572dac8721237ea9a82b147c6e7666bc180

Diagnostic clarification:

e20b2f542ab51a2b4f0807e6394ca5ecb313699c

The canonical public sources remain:

src/web/browser/liturgy/day.html
bc5a98de6b718431f3b91e6a133bb847c2dcdf4d21fce6f45aae3ad4984de868

src/web/browser/liturgy/index.html
f630f4a66f3f525144336f183b1485c698030c7531ff679375b3a7aa00150c65

Successful continuity-only Pages run:

31169274928

That run does not qualify a cutover SHA and must never be cited as a public-cutover deployment.

Previously accepted compatibility package:

build/agent-handoffs/20260807T052836Z-liturgy-reader-public-cutover-compatibility/
build/agent-handoffs/20260807T052836Z-liturgy-reader-public-cutover-compatibility.zip

Compatibility ZIP SHA-256:

2222dada68a66a98a9fc029b8d7c0550d7d4de3c36634f19bbec1e24d150b31c

Rejected-as-executable sealed cutover patch SHA-256:

cd11518ba7b20d198cbd16d08cc153d3f3053afeba8a230441c57312318a7566

That old patch remains useful as provenance, but must not be executed again.
Exact gate failures to repair

The trial-applied cutover produced:

Locked focused Python: 225/230
Shared-shell Chromium: 17/18

The six failures are bounded and understood.
1. tools/tests/test_liturgy_reader_state.py

One stale legacy production-boundary assertion still requires canonical
day.html and index.html not to load:

reader-state.js
reader-state-adapters.js

That assertion is correct before cutover and incorrect after the accepted same-path promotion.
2. tools/tests/test_mass_ordinary.py

Three failures come from an incomplete test migration in the old cutover patch:

    orphan references to legacy settings / <details> state after those variables and structures were removed;

    orphan references to legacy notices / controls state after the Propers hierarchy was migrated;

    the Contents test still references the old <details> opening/closing structure after the accepted reader uses a closed <dialog> surface.

These are test defects. Do not change reader HTML to satisfy them.
3. tools/tests/test_public_alpha.py

The link-preview test compares the raw source description against serialized HTML.

The source contains an apostrophe and the public-alpha builder correctly HTML-escapes it in metadata.

Repair the test expectation, not the source description and not the builder.
4. tools/tests/liturgy_reader_shell_browser.mjs

The canonical-route browser assertion still waits for the legacy:

#reading

DOM and asserts no reader shell.

After same-path promotion it must instead wait for the accepted production-reader readiness and document, and assert the accepted shell exists.

This harness path was missing entirely from the old 17-path sealed patch.
Authorization boundary
Authorized corrected execution-patch paths

The replacement patch may contain the original 17 paths plus exactly these two newly authorized paths:

tools/tests/test_liturgy_reader_state.py
tools/tests/liturgy_reader_shell_browser.mjs

Therefore the replacement cutover patch should contain exactly 19 paths unless a test proves one of the original 17 is no longer necessary.

The expected 19-path set is:

PROJECT-WORK.md
guidance/liturgy-browser-roadmap.md
promised-deliverables.toml
release/public-alpha.json
release/rights/public-alpha-2026-07-15.md
src/web/browser/liturgy/day.html
src/web/browser/liturgy/index.html
tools/tests/day_reader_integration_browser.mjs
tools/tests/liturgy_reader_shell_browser.mjs
tools/tests/liturgy_reader_visual_reset_browser.mjs
tools/tests/propers_reader_integration_browser.mjs
tools/tests/test_day_missal_integration.py
tools/tests/test_day_reader_integration.py
tools/tests/test_liturgy_reader_shell.py
tools/tests/test_liturgy_reader_state.py
tools/tests/test_liturgy_reader_visual_reset.py
tools/tests/test_mass_ordinary.py
tools/tests/test_propers_reader_integration.py
tools/tests/test_public_alpha.py

If a repair requires any path outside this list, stop for review.
Product paths remain frozen

Do not change any accepted reader implementation other than the already accepted
same-path day.html / index.html promotion contained in the proposed patch.

In particular, do not change:

src/web/browser/liturgy/day-reader.js
src/web/browser/liturgy/day-reader.css
src/web/browser/liturgy/propers-reader.js
src/web/browser/liturgy/propers-reader.css
src/web/browser/liturgy/reader-state.js
src/web/browser/liturgy/reader-state-adapters.js
src/web/browser/liturgy/reader-shell.js
src/web/browser/liturgy/reader-shell.css
src/web/browser/liturgy/reader-instrument.css
src/web/browser/liturgy/ordinary-seating.js

Do not change source data, translations, assembly, renderers, the visual oracle, candidate pages, or navigation.
GR-A — Continuity kickoff

Append this complete authorization verbatim under:

## Independent cutover-gate repair authorization — reviewer to Codex

in:

build/agent-continuity/liturgy-reader-visual-plan.md

Immediately append:
