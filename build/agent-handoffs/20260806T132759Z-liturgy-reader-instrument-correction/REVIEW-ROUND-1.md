## Independent review round 1 — reviewer to Codex

Liturgical Instrument — Independent Review Round 1
Disposition

CHANGES REQUESTED

The selected direction is confirmed. Liturgical Instrument now reads as a serious, coherent visual foundation, and six of the seven round-0 findings are resolved. Do not reopen the visual direction, typography system, ritual grid, warning hierarchy, masthead concept, or ordinary/proper composition.

One original blocker remains at the intermediate responsive breakpoint, and one closely related high-zoom reflow blocker is visible in the required evidence matrix. Resolve only these shell states, then return a narrow immutable handoff for independent re-review.

Production-integration execution remains unauthorized. Public cutover remains unauthorized.
Reviewed state

    Reviewed commit: 50288ddf9759f56e8a25e4907d8de25e27e25e8f

    Reviewed handoff:

        build/agent-handoffs/20260806T112813Z-liturgy-reader-instrument-correction/

        build/agent-handoffs/20260806T112813Z-liturgy-reader-instrument-correction.zip

    Governing continuity file:

        build/agent-continuity/liturgy-reader-visual-plan.md

    Primary evidence:

        evidence/instrument-before-after-blockers.png

        evidence/instrument-final-contact-sheet.png

        all 22 originals under evidence/screenshots/final/

The GitHub Pages deployment associated with the final handoff was reported successful, and the unlinked Day and Propers prototype routes remain isolated and noindex. The review package records passing manifest and ZIP checks. The reviewer inspected every required final screenshot individually at full size. The reviewer did not independently rehash the ZIP because the review environment would not materialize an application/zip response; do not reinterpret this as an integrity failure.
Explicit dispositions
1. Serious, coherent reading instrument

PASS

The corrected Instrument is no longer merely a styled prototype. The reading plane, restrained masthead, typography, cue grid, ritual divisions, and Day/Propers relationship now form one authored product system.
2. Shell integrated into desktop and mobile composition

FAIL AT TWO RESPONSIVE STATES; PASS ELSEWHERE

    Pass at 1440×900: the square, shadowless ruled rail belongs to the reading plane.

    Pass at normal 768/393/320 widths: the opaque edge dock is visually owned by the viewport and does not show text through it.

    Fail at 1024×768: the old floating rounded card returns.

    Fail at 200% text zoom on 393×852: action labels break inside words.

See the exact blockers below.
3. Real liturgical text dominant soon enough

PASS

Read begins promptly. Roman Missal principal text now appears substantially earlier at 1440, 393, and 320. The Roman partial state has one compact status statement before held Ordinary text. The postconciliar state exposes held Propers soon enough and demotes exact absences.
4. Read axis and 768×1024 measure

PASS

Read now uses one deliberate axis. The 636-pixel / approximately 75-character portrait measure is controlled and readable. The former empty ritual gutter is gone.
5. Ordinary as continuous ritual action

PASS

The desktop cue grid and mobile stacking preserve continuous ritual action. Speaker changes are quieter, named ritual cues remain meaningful, and closely related exchanges no longer read as unrelated records.
6. Warning hierarchy

PASS

Warnings remain exact and honest without overpowering held liturgical text. Roman partial and postconciliar partial-English states now have the correct hierarchy.
7. Masthead, narrow title, and mobile spacing finish

PASS AT NORMAL SCALE

The three-stroke Triptych device is authored, the meaningless progress dash is gone, the 320-pixel division title wraps deliberately, and normal-scale mobile exchange spacing is finished enough. The 200% shell-label failure is separately blocking because it is a responsive control-layout defect, not a reason to reopen these accepted details.
Exact blockers
Blocker 1 — Intermediate-width shell remains a floating application card

    State: Day · Read

    Viewport: 1024×768

    Evidence: evidence/screenshots/final/02-day-read-1024x768.png

    Also visible beneath: evidence/screenshots/final/15-date-open-1024x768.png

    Visible symptom: The controls become a centered rounded rectangle with shadow/elevation and translucent compartments. Liturgical text is visibly present beneath the card. The shell overlays the Collect rather than owning an edge or aligning with the reading geometry.

    Why blocking: This is the original shell blocker at an uncorrected breakpoint. The visual system currently changes from integrated desktop rail, back to generic floating app widget, then to integrated mobile edge dock.

    Requested correction: At every width where the external vertical rail cannot fit, transition directly to an opaque, square, edge-bound ruled dock. Remove rounded corners, floating inset, shadow, translucency, and equal-compartment card styling. Reserve block-end layout space equal to the dock’s occupied height so reading text never sits beneath it. A different integrated solution is acceptable only if it clearly belongs to the reading plane and preserves the four one-step actions.

    Required regression states: 1024×768 Read, 1024×768 Missal, 1024×768 Date open, 768×1024 Read, and 393×852 Read/Missal.

Blocker 2 — High-zoom shell labels break inside words

    State: Day · Missal with 200% text zoom

    Viewport: screenshot canvas 393×852; effective CSS width is approximately half under 200% zoom

    Evidence: evidence/screenshots/final/19-text-200-percent-393x852.png

    Visible symptom: Contents, Mode, and Details break as Cont / ents, Mod / e, and Deta / ils. The controls remain operable, but the shell looks visibly broken rather than deliberately reflowed.

    Why blocking: The shell is a permanent primary-control system. Mid-word fragmentation in a required accessibility/reflow state is not production-foundation finish.

    Requested correction: Introduce an extreme-reflow layout that preserves complete labels without horizontal scrolling or clipping. Prefer a two-column/two-row dock with whole labels and adequate targets. Do not counteract browser zoom by shrinking text. Do not hide labels unless the resulting icon-only controls remain unmistakable and retain accessible names; a labeled 2×2 arrangement is the safer default.

    Required regression states: 200% text zoom at 393×852, forced colors at 393×852, keyboard focus at 393×852, and normal-scale 393×852.

Bounded work order

    Append this complete review under a new heading such as ## Independent review round 1 — reviewer to Codex in:

        build/agent-continuity/liturgy-reader-visual-plan.md

    Append Codex’s response immediately after it. State the proposed breakpoint and extreme-reflow solution before editing.

    Change only the responsive shell geometry and any necessary reserved page padding/focus styling.

    Do not alter accepted typography, title geometry, ritual text position, warning wording/hierarchy, cue semantics, masthead, Day/Propers entrances, or public routes.

    Extend the visual harness so it asserts:

        no floating rounded/translucent Instrument shell at the 1024 state;

        no content visible beneath or obscured by the closed dock;

        no mid-word action-label breaks at 200%;

        no horizontal overflow;

        all four actions retain accessible names and adequate target size.

    Capture the required blocker and regression states at original pixels and inspect each at full size.

    Run the existing focused tests, visual assertions, shared-shell checks, Day/Propers browser checks, production-isolation checks, and locked public-alpha build/verify. Preserve the honest dispositions of unrelated repository gates.

    Commit and push the correction, verify the Pages run and deployed prototype asset parity, then append exact commit/run/hash/check results and the next action to the continuity file.

    Produce a new immutable handoff directory and ZIP containing:

        this review round;

        the updated continuity record;

        before/after evidence for both blockers;

        the narrow final/regression matrix;

        original screenshots;

        capture metadata;

        browser results;

        checks;

        manifest and verified ZIP.

    Stop for independent re-review. Do not begin production-integration execution and do not authorize public cutover.

Re-review scope

The next independent review is intentionally narrow:

    Is the Instrument shell integrated continuously at 1440, 1024, 768, 393, and 320?

    Does the 200% state preserve whole, readable action labels and usable controls?

    Did the shell correction avoid regressions to reading measure, first-principal-text position, modal behavior, focus, forced colors, and normal mobile rhythm?

If all three pass, the correction may be accepted and production-integration execution may begin. Public cutover will still require a separate authorization.
