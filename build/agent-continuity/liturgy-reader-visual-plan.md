# Liturgy reader visual plan and continuity

## Resume header

- Current branch: `main`
- Current commit: `85abf971e70e7d1acc8bfa1c29c61ff8c1ff26b3`; pushed emergency takeover checkpoint for Live Reader — Ritual Flow & Orientation
- Reviewed visual baseline: `0f3567dc509a2d5b42fd58a0e4c77c8f5e5dc113` (visual implementation `7233879350ff00c92fa2029ca04f481125daa519`; task base `842333af79bd560ad6607b91b087ed8ff71e7477`)
- Selected direction: Liturgical Instrument
- Current phase: Live Reader — Ritual Flow & Orientation; takeover checkpoint after RF-A and the first RF-B/RF-C implementation
- Last completed work unit: RF-A canonical baseline and source-owned semantic inventory; first persistent-locus and Contents-map implementation is present but not yet a review candidate
- Next exact action: rebuild the locked preview, rerun Day/Propers/shared-shell/governed browser gates after the final locus simplification, capture corrected matrix v3, and inspect every original at full size before deciding whether RF-D/RF-E need further presentation changes
- Open blockers: the final one-line major-only locus simplification has not yet been rerun through browser gates; mobile overlap measurement needs review; unresolved Roman conditional forms lack safe applicability metadata and remain visible; the unrelated governed example replay remains non-green
- Latest pushed commit: `85abf971e70e7d1acc8bfa1c29c61ff8c1ff26b3` — ritual-flow implementation/takeover checkpoint; not a review candidate
- Latest successful Pages run: `31175722949`, success for exact cutover SHA `9b5f21c0ca26bf02af03d207ddd2617021e16fb3`
- Latest Pages attempt: run `31181413147` succeeded for acceptance-handoff commit `e647d1ababdc399da7296dfb6b87cd2b8e90e8e4`; it is a post-acceptance documentation deployment and does not replace qualifying cutover run `31175722949`
- Current ritual-flow Pages attempt: run `31188364101` for checkpoint `85abf971e70e7d1acc8bfa1c29c61ff8c1ff26b3` was `in_progress` at shutdown; verify its final disposition and do not treat it as final phase evidence
- Latest handoff directory: `build/agent-handoffs/20260807T130808Z-liturgy-reader-instrument-public-cutover-acceptance/` (six payload files plus manifest; committed and pushed)
- Latest handoff ZIP: `build/agent-handoffs/20260807T130808Z-liturgy-reader-instrument-public-cutover-acceptance.zip`, SHA-256 `d44843a2a90971816e7fa35bb49b3e6b44b649edf35231c459709db8788901a4` (verified, committed, and pushed)

## Fixed decisions and scope boundaries

- Liturgical Instrument is the selected production visual foundation. Quiet Folio and Contemporary Reader are frozen comparison references; this correction does not merge them or create another direction.
- Independent Round 1 review accepted Liturgical Instrument as the production visual foundation and authorized production-integration execution. Public cutover and public navigation links remain unauthorized.
- Accepted M1–M3 and W3 state, production assembly, renderer reuse, one Ordinary seating path, fail-closed behavior, semantic-location restoration, focus behavior, render-race ownership, responsive action reachability, and production isolation remain binding.
- Day and Propers remain distinct Date and Browse entrances to one product. Propers Missal, Study, Compare, search, source or recension expansion, and print redesign remain out of scope.
- Production integration is CSS-first and must preserve the isolated accepted prototype as its comparison oracle. No accepted behavioral-seam conflict is presently known; any conflict must be proved and appended before reconsideration.
- The public `liturgy/day.html` and `liturgy/index.html` routes remain unchanged and unlinked from the prototype.

## Independent review round 0 — reviewer to Codex

Disposition: Liturgical Instrument is selected as the production visual foundation, but corrected screenshots must pass another independent visual review before production-integration execution. Public cutover is not authorized.

1. The permanent control shell still looks like a detachable application widget rather than part of the reading instrument.
2. Missal mode begins the rite too far below the first viewport.
3. Read mode incorrectly retains an empty ritual gutter.
4. The 768-pixel portrait reading measure is too broad.
5. Partial and postconciliar coverage warnings repeat and overpower available liturgical text.
6. The masthead’s isolated progress dash and generic circular T feel provisional.
7. Mobile ritual micro-spacing and narrow division-title wrapping need an editorial pass.

## Codex response to review round 0

1. Integrate the persistent controls with the Instrument grid: remove floating-card elevation and equal-compartment styling, align the wide rail to the text/cue geometry, and make the mobile dock visually opaque while retaining the accepted four actions and interaction controller.
2. Compress Instrument identity-to-rite spacing in Missal mode and measure the first principal text against the reviewed 1440, 393, and 320 pixel baselines. The correction will retain meaningful identity and target at least an 80-pixel earlier start without collisions.
3. Give Read mode its own single reading axis: Proper headings, references, and prose will not inherit the Missal cue gutter.
4. Constrain the 768×1024 Read measure to approximately 40–42rem and 65–75 approximate characters, rather than the reviewed 726 pixels/about 86 characters.
5. Keep one compact identity-level coverage statement, reduce repeated missing units to restrained inline absence notation, and verify that held Ordinary/Proper text dominates both Roman partial and postconciliar partial-English views. Source honesty and exact absence semantics remain unchanged.
6. Replace the generic text-in-circle mark with a project-owned inline SVG/CSS triptych device and make semantic progress an intelligible labeled meter. If measurement shows the progress object remains ornamental or misleading, the visible meter will be removed while internal semantic state remains available.
7. Tighten related response/rubric spacing, rely less on repeated red micro-labels where the grid already supplies meaning, and add deliberate narrow division-title wrapping at 320 pixels.

No proposed correction presently needs to differ from the review request. All changes are planned in prototype HTML/CSS/JavaScript and its evidence harness, leaving accepted production behavior untouched.

## Visual work plan

1. Work unit A — capture reviewed baselines; separate Read and Missal geometry; constrain portrait measure; advance Missal principal text; record measurements and before/after evidence.
2. Work unit B — integrate the desktop rail and compact dock; refine masthead mark and semantic progress; re-prove accessibility and accepted surface behavior.
3. Work unit C — consolidate warnings; subordinate individual absences; tune ritual exchanges and 320-pixel division wrapping; preserve provenance.
4. Work unit D — exercise the complete Day/Propers and interaction matrix; correct only exposed finish regressions; run all governed checks and public-alpha verification; assemble the immutable independent-review handoff.

Each completed checkpoint will append its exact code/evidence paths, measurements, checks, commit, push, Pages run, deployed route verification, and next action. Earlier entries will not be rewritten.

## Measurement baselines and targets

Reviewed baselines supplied by round 0:

| State | Reviewed baseline | Correction target |
| --- | ---: | ---: |
| Read at 768×1024 | 726 px / about 86 characters | about 40–42rem / 65–75 characters |
| Missal first principal text at 1440×900 | 474.6 px | at least about 80 px earlier |
| Missal first principal text at 393×852 | 441.8 px | at least about 80 px earlier |
| Missal first principal text at 320×852 | 458.8 px | at least about 80 px earlier |

Harness-captured baseline geometry will be appended after the pre-change run. Measurements must distinguish the first liturgical container from the first principal spoken/passage text and record exact URL/hash, viewport, scroll, overflow, focus, semantic state, and error counts.

### Work unit A measured result — 2026-08-06

The untouched baseline was captured from the preview bound to reviewed commit
`0f3567dc509a2d5b42fd58a0e4c77c8f5e5dc113` in
`build/agent-continuity/liturgy-reader-instrument-baseline/`. The settled
corrected capture is
`build/agent-continuity/liturgy-reader-instrument-work-unit-a-corrected-v3/`.
Two intermediate corrected directories are retained locally but are not
evidence: the first straddled a preview rebuild; the second correctly exposed a
`data-mode` selector collision in one assertion. The v3 run is the sole Work
unit A corrected evidence owner.

| State | Baseline | Corrected | Delta / disposition |
| --- | ---: | ---: | --- |
| Read text width, 768×1024 | 726 px / about 86 characters | 636 px / about 75 characters | −90 px / −11 characters; target passes at about 39.75rem |
| Missal first principal text, 1440×900 | 474.58 px | 316.98 px | −157.60 px; at least 80 px earlier |
| Missal first principal text, 393×852 | 441.77 px | 324.97 px | −116.80 px; at least 80 px earlier |
| Missal first principal text, 320×852 | 458.83 px | 342.03 px | −116.80 px; at least 80 px earlier |

The 1440 Read measure is 636 px/about 69 characters. The 393 Read measure
remains 351 px/about 41 characters, and the 320 Missal measure remains 278
px/about 39 characters. Required Work unit A rows have zero horizontal
overflow. Full-size inspection found one coherent system: Read no longer keeps
the eight-rem ritual gutter, while Missal retains the wide cue grid and stacks
it without collision on mobile. Identity remains complete in every measured
first viewport.

### Work units B/C measured result — 2026-08-06

The complete corrected run is
`build/agent-continuity/liturgy-reader-instrument-finish-corrected-v3/`.
It records 53 captures and 13/13 passing Chromium assertions with no console,
failed-request, HTTP, unnamed-interactive, duplicate-ID, or required horizontal
overflow result. Earlier `finish-corrected` directories stopped before a fresh
preview rebuild or a complete persistent run and are not evidence.

| Finding | Baseline | Corrected | Delta / disposition |
| --- | ---: | ---: | --- |
| Desktop shell, 1440×900 | 76.8 px rounded card at x=144 with shadow | 68 px ruled rail at x=184.5, transparent, square, no shadow | aligned immediately outside the 896 px ritual plane; card elevation removed |
| Mobile dock, 393×852 | translucent rounded dock | opaque `rgb(250, 248, 242)` edge dock with 2 px top rule | underlying text no longer shows through; all four targets remain at least 73.19 px high |
| Roman partial first held text, 393×852 | 591.14 px | 393.75 px | −197.39 px; one exact identity-level status replaces the separate generic notice plus uncompiled paragraph |
| Postconciliar first held text, 1440×900 | 741.11 px | 542.45 px | −198.66 px; exact missing-language notices become quiet inline pairs rather than full-width bars |
| Narrow first division, 320×852 | uncontrolled single-line pressure | deliberate balanced two-line title, 53.17 px high | no orphan fragment and no horizontal overflow |

The generic circular `T` is replaced in Instrument only by a three-stroke CSS
triptych device. The visually meaningless progress dash is removed for
Instrument while `data-semantic-progress` and semantic-current calculation
remain intact. Speaker-change labels remain exact but shift from repeated red
accents to quiet gray; named ritual cues remain in the semantic gutter.

## Decision log

- 2026-08-06 — Confirmed `main`, local `HEAD`, and `origin/main` all equal reviewed end commit `0f3567dc509a2d5b42fd58a0e4c77c8f5e5dc113`; no reset, pull, merge, or preservation workaround is required. Worktree was clean.
- 2026-08-06 — Treat Instrument selection as fixed and the seven findings as the complete governing visual diagnosis for this correction. Frozen comparison directions remain useful only as baseline evidence.
- 2026-08-06 — Use the existing Chromium harness as the measurement and capture owner, extending it to emit explicit baseline/corrected deltas and the requested matrix.
- 2026-08-06 — Added a presentation-only `data-reader-mode` hook derived from the committed visible outcome, not from URL state. The initial name `data-mode` collided with the mode-button selector and was superseded immediately by `data-reader-mode`; the passing v3 run uses only the corrected name.
- 2026-08-06 — Set the Read measure to 39.75rem rather than the initial 42rem correction. The initial correction produced 672 px/about 79 characters at 768×1024; 39.75rem produces 636 px/about 75 and meets the reviewed target without narrowing mobile.
- 2026-08-06 — Retained the stronger Missal advance because full-size review shows no identity, division, cue-grid, or mobile collision. The correction moves principal ritual text 116.8–157.6 px earlier, exceeding the approximately 80 px minimum without deleting content.
- 2026-08-06 — Removed Instrument's visible progress meter because its isolated dash was neither labeled nor sufficiently legible as semantic progress. Internal semantic progress ownership is unchanged and remains exercised by the browser harness.
- 2026-08-06 — Replaced the Instrument-only circular text mark with a CSS three-stroke triptych device; frozen Folio and Contemporary Reader marks are unchanged and no asset, request, font, or external dependency was added.
- 2026-08-06 — Consolidated Roman partial status by moving the renderer-owned uncompiled node contents, unchanged, into the existing identity-level `role="note"`. Postconciliar element notices retain their exact renderer-owned text and DOM semantics inside presentation-only inline groups. No missing text was inferred or manufactured.
- 2026-08-06 — Flattened and grid-aligned the desktop rail and made the mobile dock opaque. The existing shared shell controller continues to own action reachability, surfaces, inertness, Escape, focus, and semantic restoration.
- 2026-08-06 — Extended the governed harness by one required postconciliar 393×852 row and explicit shell, warning, division, focus, semantic, and error measurements. The final handoff normalizes only the ephemeral local origin while preserving exact route, query, hash, viewport, and scroll state.
- 2026-08-06 — Corrected the two task-owned captured examples for the promised-deliverable ledger from 14 tracked/9 complete to the current 21/15. The remaining full-gate example divergences are unrelated, substantially pre-existing, and were not recaptured or blessed.

## Checkpoint history

- 2026-08-06T03:10:21Z — Pre-edit reconciliation complete. `tools/tpt check-promised-deliverables` exited 0 with `20 tracked, 14 complete`. No task checkpoint has yet been committed or pushed.
- 2026-08-06T03:22:04Z — Untouched baseline capture completed: 52 screenshots, 12/12 Chromium assertions passing, no console/network/HTTP/accessibility-name failures.
- 2026-08-06T03:34:57Z — Work unit A v3 corrected capture completed after an exact preview rebuild: 52 screenshots, 12/12 Chromium assertions passing, no console/network/HTTP/accessibility-name failures, and the four requested geometry targets met. Commit, push, Pages, and deployed-route verification are the next checkpoint actions.
- 2026-08-06T03:38:40Z — Work unit A committed as `a2542c88fe9b811d58b8691fdfdfdb515d1342fa` and pushed to `origin/main`. GitHub Pages run `31069000038` completed successfully at 2026-08-06T03:40:40Z. Direct checks returned HTTP 200 and the required noindex metadata for both deployed unlinked prototype routes: `/triptych/liturgy/reader-visual-reset-day.html?design=instrument` and `/triptych/liturgy/reader-visual-reset-propers.html?design=instrument`.
- 2026-08-06T10:46:47Z — Work units B/C complete capture `finish-corrected-v3` finished: 53 captures, 13/13 assertions passing, Chrome 151, no console/network/HTTP/accessibility-name failures. Full-size blocker inspection confirms an integrated desktop rail, opaque mobile edge dock, authored three-stroke masthead, one compact Roman partial statement, quiet postconciliar inline absences, earlier held text, tighter exchanges, and deliberate 320 px division wrapping. Focused checks, checkpoint commit/push, and deployment verification remain next.
- 2026-08-06T10:48Z — Work units B/C focused validation passed: the exact requested seven-module Python command ran 140 tests with exit 0; JavaScript syntax checks for the prototype and harness, `tools/tpt check-promised-deliverables` (21 tracked/15 complete), `tools/tpt --check` (34 tools), `make check-release-bindings` (0 stale), and `git diff --check` all exited 0. The candidate ledger remains candidate with independent review open.
- 2026-08-06T10:50:46Z — Instrument finish checkpoint `62e712a1962080d1dc3c6e106651c41afbf7531b` pushed to `origin/main`. Pages run `31094868150` completed success at 2026-08-06T11:00:15Z. Both unlinked prototype routes returned HTTP 200 with noindex; deployed CSS `337a8ce54b0af40eacc8c03425df3bddedb793b804afc49a16aee8cbe73d24eb` and JavaScript `eb1c1dd5c0c9c7076b74f2187627dc56e39963429212c0a51872df0ea98a9679` byte-match task sources.
- 2026-08-06T11:00Z — Existing browser harness dispositions: Propers 27/27 pass; shared shell 18/18 pass; Day 33/34 with only its date-dependent first-visit assertion failing because 2026-08-06 correctly shows material coverage instead of the test's expected hidden notice. All Day behavior, race, focus, reflow, print, production parity, network, and accessibility assertions passed.
- 2026-08-06T11:20Z — Governed `make check` stopped with exit 2 at the existing example-replay gate after preceding checks passed: 23 divergences and 35 known-stale transcripts across calendar, citation, corpus, source-library, and research-staleness work. The two task-owned promised-deliverable count transcripts were corrected afterward; unrelated examples were not recaptured or blessed. System-Python public-alpha build stopped on Markdown 3.10.3 versus locked 3.10.2, while the repository's locked environment successfully checked, built, and verified the exact GitHub Pages artifact.
- 2026-08-06T11:28Z — Final handoff assembled at `build/agent-handoffs/20260806T112813Z-liturgy-reader-instrument-correction/`: 22 required full-size final states, 5 reviewed-baseline blocker counterparts, two labeled contact sheets, explicit combined metadata, browser results, print smoke, focused source snapshots, compact runnable candidate, checks, and review documents. Every required screenshot and both contact sheets were inspected at full size. Manifest/ZIP integrity follows after this continuity file is copied byte-for-byte.

## Codex visual self-review and message to the next reviewer

Visible changes resolve the seven round-0 findings as follows:

1. **Shell integration:** the desktop floating card is now a transparent,
   square, shadowless ruled rail aligned immediately outside the ritual plane;
   the mobile dock is opaque and edge-bound. Date/Browse, Contents, Mode, and
   Details remain one action away with the accepted controller and touch size.
2. **Missal opening:** first principal text advances 157.60px at 1440, 117.68px
   at 393, and 118.55px at 320, without removing identity or cue semantics.
3. **Read gutter:** Read has one axis; no ritual gutter remains.
4. **Portrait measure:** 768×1024 is 636px/about 75 characters, down from
   726px/about 86.
5. **Warnings:** Roman partial status is one exact compact note and held text
   begins 197.39px earlier. Postconciliar exact absences are quiet inline pairs
   and first held text begins 198.66px earlier at 1440; held Propers dominate.
6. **Masthead:** the generic circular T is a CSS three-stroke triptych device;
   the meaningless visible progress dash is gone while semantic progress stays.
7. **Mobile finish:** speaker-change labels are quieter, related exchanges are
   tighter, and the 320px division uses a deliberate balanced two-line wrap.

Look first at `evidence/instrument-before-after-blockers.png`, then inspect the
Roman partial mobile, postconciliar desktop/mobile, 320px Missal, 768px Read,
deep-scroll provenance, and all four open surfaces at full size. The only
provisional status is review acceptance itself: no known visual blocker is
being withheld, but Codex does not claim independent acceptance.

Please decide exactly whether the corrected Instrument is coherent and serious,
whether the shell and warning hierarchy are now integrated and subordinate,
whether Read and Ordinary rhythm are ready, and whether the masthead/narrow
finish is sufficient to authorize production-integration execution. If not,
name each remaining blocker by state, viewport, symptom, and requested change.
Public cutover remains unauthorized regardless of this review.

## Open questions for the next independent review

- Does the corrected Instrument now feel like a serious, coherent reading instrument rather than a styled prototype?
- Is the shell integrated into the composition on desktop and mobile?
- Is real liturgical text dominant soon enough in Read, Missal, partial, and postconciliar states?
- Does Read use one deliberate axis and a controlled measure at 768×1024?
- Does the Ordinary read as continuous ritual action on desktop and mobile?
- Are warnings honest but subordinate?
- Are the masthead, narrow division titles, and mobile exchange spacing finished enough to authorize production-integration execution?
- What exact blockers remain?

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

## Codex response to independent review round 1

The two failures are accepted as the complete and intentionally narrow Round 1 scope. The six passing dispositions remain frozen.

1. **Intermediate shell:** Instrument will stop inheriting the shared floating-card shell as soon as the external rail no longer fits. At `max-width: 71.999rem`, its four-action control becomes an edge-to-edge, block-end dock bounded by safe-area insets, with an opaque panel, square corners, a two-pixel top rule, and no shadow, blur, inset, or translucent compartment treatment. This applies continuously at 1024, 768, 393, and 320 pixels; the accepted ruled external rail remains unchanged at `min-width: 72rem`. Existing block-end document and shell reserve will be measured at maximum scroll and increased only if the dock can obscure the final readable content.
2. **Extreme reflow:** the reader shell will become a named inline-size container. When its available measure falls to at most `18rem` in the current root-font measure—covering the required 393×852 state at 200% text while excluding normal-scale 393 and 320—the Instrument dock will reflow to a labeled two-column/two-row grid. Labels will remain whole with normal word breaking and no forced wrapping; text size will not be counter-scaled. Each action will retain its visible label, accessible name, and a target of at least 44×44 CSS pixels.
3. **Regression ownership:** the Chromium harness will assert square/opaque/shadowless edge geometry at 1024, unobscured end content with an explicit dock reserve, whole label boxes at 200%, no horizontal overflow, four accessible names, and adequate targets. It will capture 1024 Read/Missal/Date, 768 Read, normal 393 Read/Missal, 200% 393, forced colors, and keyboard focus at original pixels.
4. **Frozen seams:** no typography, title, identity, ritual text, warning, cue, masthead, entrance, state, adapter, renderer, seating, modal-controller, or public-route change is proposed. If CSS containment affects accepted geometry or focus, it will be rejected rather than expanding scope.

The next code edit is limited to `reader-visual-reset.css` and its visual/static test coverage. Production-integration execution and public cutover remain unauthorized.

## Round 1 correction measurements and visual self-review

The authoritative corrected run is
`build/agent-continuity/liturgy-reader-instrument-round1-corrected-v4/`.
The first run accidentally exercised the already-built reviewed preview after a
site-tree rather than preview-tree rebuild; the second correctly exercised the
new CSS and exposed one assertion comparing the dock to `innerWidth` instead of
the scrollbar-exclusive layout viewport. Neither is evidence. The v3 run uses
the exact rebuilt preview and passes 15/15 assertions across 54 captures with
zero console, failed-request, HTTP, unnamed-interactive, duplicate-ID, or
horizontal-overflow failures.

| State | Reviewed Round 1 evidence | Corrected v4 | Disposition |
| --- | --- | --- | --- |
| 1024×768 Read shell | x 232.5, width 544, y 686; 12.8px radius; translucent 97% panel; 12×40px shadow | x 0, width 1009 layout px, y 698; 0 radius; opaque `rgb(250, 248, 242)`; no shadow; 2px top rule | Direct transition from rail to edge dock; four named targets are 239.05–239.06×68px and final content clears the dock at maximum scroll |
| 1024×768 Read text | first principal text y 299.23, width 636 | y 299.23, width 636 | accepted reading measure and first-text position unchanged |
| 768×1024 Read | edge dock with shadow; first text y 267.39, width 636/about 75 characters | same dock geometry without shadow; first text y 267.39, width 636/about 75 | accepted measure and hierarchy unchanged |
| 393×852 at 200% text | one 393×144.39px four-column dock; `Contents`, `Mode`, and `Details` split inside words | opaque square 393×245.19px two-column/two-row dock; four 178.91×104px targets; every label is one line with no clip | complete visible labels, no text shrinking, no horizontal overflow |
| 393×852 at 200% first text | y 1027.28, width 311 | y 1027.28, width 311 | accepted high-zoom reading geometry unchanged |

Full-size inspection covered 1024 Read, 1024 Missal, 1024 Date open, 768 Read,
393 Read, 393 Missal, 320 Missal, 200% text, forced colors, keyboard focus, and
the unchanged 1440 rail. The 1024 dock is square, edge-owned, opaque, and free
of compartment borders; text ends visibly above it in the first viewport and
the final content clears it at maximum scroll. The 200% dock reads as a
deliberate 2×2 primary-control system with whole labels. Normal mobile rhythm,
the 320 division wrap, modal treatment, focus indication, Read measure, and
Missal text position remain visually unchanged.

## Round 1 correction decision and checkpoint additions

- 2026-08-06 — Use `max-width: 71.999rem` for the Instrument-only edge dock so the accepted external rail at 72rem and above transitions directly to the same opaque square block-end system used at normal tablet/mobile widths. Frozen Folio and Contemporary Reader shells remain unchanged.
- 2026-08-06 — Use a named inline-size container at `max-width: 18rem` in the current root-font measure. This selects 393px at 200% text while excluding normal 393px and 320px, and reflows only the Instrument action grid to labeled 2×2 controls without counter-scaling text.
- 2026-08-06T12:50:59Z — Non-evidence run `round1-corrected` stopped 13/15 because the wrong already-built preview tree was exercised. The product preview was rebuilt with `public-alpha build --preview`; no product correction was derived from that stale run.
- 2026-08-06T12:52:58Z — Non-evidence run `round1-corrected-v2` passed the extreme-reflow assertion and stopped 14/15 only because the new edge assertion compared 1009 scrollbar-exclusive layout pixels to 1024 `innerWidth`. The assertion was corrected to compare `documentElement.clientWidth`; product CSS was unchanged.
- 2026-08-06T12:54:09Z — Passing v3 Chromium run completed: 15/15 assertions and 54 captures. Full-size inspection passed every narrow regression state. Its opacity assertion rejected only transparent backgrounds and was intentionally strengthened before settlement.
- 2026-08-06T13:05:12Z — Authoritative v4 Chromium run completed after requiring the exact opaque Instrument color `rgb(250, 248, 242)`: 15/15 assertions, 54 captures, Chrome 151, and clean console/network/HTTP/accessibility/overflow results. Product CSS and inspected pixels are unchanged from v3.
- 2026-08-06T12:58Z — Focused validation: 141/141 Python tests; Propers Chromium 27/27; shared shell 18/18; Day 33/34 with only the unchanged current-date first-visit expectation; locked preview build/verify and exact public-alpha site build/GitHub Pages verification passed; release bindings report zero stale entries.
- 2026-08-06T13:05:59Z — Correction checkpoint `ab89758e3f3ee165e0141e3605be88051450134b` pushed to `origin/main`. The outgoing commit contains only Round 1 continuity/tracking, responsive Instrument CSS, static/Chromium coverage, and exact public-alpha rights/release hashes.
- 2026-08-06T13:17:56Z — Pages run `31104342722` failed only in `actions/deploy-pages@v5` after checkout, locked dependency setup, source verification, public build, GitHub Pages compatibility verification, configuration, and artifact upload all passed. Deployment `ab89758e3f3ee165e0141e3605be88051450134b` remained `deployment_queued` for the action's 600-second timeout and was canceled by the action. Direct Day/Propers routes remain HTTP 200/noindex but still serve reviewed CSS `337a8ce54b0af40eacc8c03425df3bddedb793b804afc49a16aee8cbe73d24eb`, not corrected CSS `850e1acacb6f487a5c2f3118388b3fce7b96f9db667e783ba35cdef7d9918b48`; deployment parity is therefore explicitly not claimed.
- 2026-08-06T13:28Z — Governed `make check` exited 2 at `check-examples` after all preceding repository checks passed. The exact unrelated transcript disposition is 200 captured, 188 replayed, 21 diverged, 35 known stale, 6 never run, 6 unrunnable, and 2 volatile lines; no task-owned example diverged and no unrelated transcript was recaptured or blessed.
- 2026-08-06T13:42:20Z — Pages run `31106008011` for continuity checkpoint `c6b7f7f0a79468cfa1a503235044c92bd88c27b2` repeated the same external stop: checkout, locked setup, source verification, public build, Pages compatibility verification, configuration, and verified-artifact upload passed; `actions/deploy-pages@v5` then timed out after 600 seconds of deployment polling. Day and Propers remain HTTP 200/noindex and still serve reviewed CSS `337a8ce54b0af40eacc8c03425df3bddedb793b804afc49a16aee8cbe73d24eb`; corrected parity remains explicitly open. GitHub Status reported Actions and Pages operational, so no broader service diagnosis is inferred.
- 2026-08-06T13:58:58Z — Pages run `31107294462` for checkpoint `3873bd99cb308432404378c665dbcb3246144c9e` again passed every repository-owned build/upload step. Its deploy step ran from 13:49:32Z until GitHub canceled the job at its 15-minute maximum; the run concluded `cancelled`, not success. Direct deployed CSS remains `337a8ce54b0af40eacc8c03425df3bddedb793b804afc49a16aee8cbe73d24eb`, so corrected parity is still not claimed. No manual rerun or broader deployment action was taken; the immutable-handoff push will supply the next ordinary automatic attempt.
- 2026-08-06T14:17:40Z — Pages run `31109086658` for immutable-handoff commit `c388ab42dfc4f5c7d49abc71596d6bb511af5742` completed successfully after every repository-owned build/upload step and deployment passed. Direct Day and Propers routes return HTTP 200 with noindex metadata. Deployed CSS `850e1acacb6f487a5c2f3118388b3fce7b96f9db667e783ba35cdef7d9918b48` and JS `eb1c1dd5c0c9c7076b74f2187627dc56e39963429212c0a51872df0ea98a9679` byte-match source. Corrected deployed parity is resolved; independent re-review is the only remaining gate.

## Message to the next independent reviewer

Liturgical Instrument remains the confirmed direction. Review only the two
Round 1 shell states: the intermediate dock and the 200% labeled reflow. At
1024 the former rounded translucent card is now a square, opaque, shadowless
edge dock; at 200% the four controls deliberately reflow to a labeled 2×2 grid
with whole words and large targets. Begin with
`evidence/round1-shell-before-after.png`, then inspect all originals in
`evidence/screenshots/after/`, especially 01, 03, 08, 09, and 10. The accepted
reading measure, first-text position, modal behavior, focus, forced colors,
and normal mobile rhythm are measured unchanged. The earlier deployment-polling
stop is resolved: Pages run `31109086658` succeeded and direct unlinked/noindex
Day/Propers CSS/JS byte-match source. Decide exactly: (1) shell continuity across
1440/1024/768/393/320, (2) whole usable labels at 200%, and (3) absence of the
listed regressions. Production-integration execution may begin only if all
three pass. Public cutover remains unauthorized regardless.

## Independent review round 1 acceptance — reviewer to Codex

Liturgical Instrument — Independent Round 1 Acceptance
Disposition

ACCEPTED

The two responsive-shell blockers from Independent Review Round 1 are resolved. Liturgical Instrument is accepted as the production visual foundation, and production-integration execution may begin.

Public cutover remains unauthorized.

Do not reopen the accepted visual direction, typography system, reading measure, ritual grid, warning hierarchy, masthead, Ordinary/Proper composition, Day/Propers entrance model, or the seven Round 0 dispositions unless production integration exposes a concrete conflict with an accepted behavioral seam.
Reviewed state

    Correction implementation checkpoint: ab89758e3f3ee165e0141e3605be88051450134b

    Successful deployed-parity handoff checkpoint: c388ab42dfc4f5c7d49abc71596d6bb511af5742

    Post-deployment evidence commit: 4daf7d8

    Reviewed handoff:

        build/agent-handoffs/20260806T141831Z-liturgy-reader-instrument-correction/

        build/agent-handoffs/20260806T141831Z-liturgy-reader-instrument-correction.zip

    Reviewed ZIP SHA-256:

        b766a270abbff30e1fd9b79a7360b5f6fa8bd0ac7f10600fc621f6c9e7701fa1

    Governing continuity file:

        build/agent-continuity/liturgy-reader-visual-plan.md

The reviewer independently:

    tested the uploaded ZIP successfully;

    verified all 109 MANIFEST.sha256 entries;

    confirmed the archive has one top-level directory;

    confirmed candidate CSS byte-matches the included corrected source at
    850e1acacb6f487a5c2f3118388b3fce7b96f9db667e783ba35cdef7d9918b48;

    inspected the before/after sheet, regression matrix, and all 11 corrected original-pixel screenshots.

Three requested dispositions
1. Continuous shell integration across 1440, 1024, 768, 393, and 320

PASS

At 1440 pixels, the accepted external ruled rail remains part of the reading plane.

At 1024 pixels, the prior floating rounded/translucent card is gone. Read, Missal, and Date-open states use a square, opaque, shadowless, edge-bound dock. The dock no longer appears as a detachable application widget, and the page reserves its occupied block-end space.

At 768, 393, and 320 pixels, the same edge-owned dock grammar continues without a visual breakpoint reversal. Normal mobile text remains visible above rather than through the dock.

Accepted evidence:

    evidence/screenshots/after/01-day-read-1024x768.png

    evidence/screenshots/after/02-day-missal-1024x768.png

    evidence/screenshots/after/03-date-open-1024x768.png

    evidence/screenshots/after/04-day-read-768x1024.png

    evidence/screenshots/after/05-day-read-393x852.png

    evidence/screenshots/after/06-day-missal-393x852.png

    evidence/screenshots/after/07-day-missal-320x852.png

    evidence/screenshots/after/11-day-read-1440x900.png

2. Whole, readable, usable controls at 200% text

PASS

The extreme-reflow state now uses a deliberate labeled two-column/two-row dock. Date, Contents, Mode, and Details remain whole words, readable, unclipped, and visually balanced. Text is not counter-scaled. No horizontal scrolling is introduced, and the included measurements record four large named targets.

Accepted evidence:

    evidence/screenshots/after/08-text-200-percent-393x852.png

    evidence/round1-shell-before-after.png

3. No regression to accepted geometry or behavior

PASS

The correction remains confined to responsive shell geometry and associated reserve/test ownership.

The evidence preserves:

    the 636-pixel / approximately 75-character 768×1024 Read measure;

    the accepted first-principal-text positions;

    the normal 393 and 320 mobile rhythm;

    the deliberate narrow Missal title wrap;

    Date modal presentation;

    visible keyboard focus;

    forced-colors readability;

    the 1440 external rail;

    no required horizontal overflow;

    four one-step named actions.

Accepted evidence:

    evidence/screenshots/after/03-date-open-1024x768.png

    evidence/screenshots/after/04-day-read-768x1024.png

    evidence/screenshots/after/09-forced-colors-393x852.png

    evidence/screenshots/after/10-keyboard-focus-393x852.png

    evidence/baseline-corrected-measurements.json

    evidence/browser-results.json

    checks.txt

Validation disposition

The package records:

    141/141 focused Python tests;

    15/15 governed visual assertions across 54 captures;

    27/27 Propers browser checks;

    18/18 shared-shell browser checks;

    Day 33/34, with only the unchanged date-dependent first-visit expectation;

    locked public-alpha check/build/verify passing;

    no console, failed-request, HTTP, unnamed-control, duplicate-ID, or required-overflow failures.

The governed full gate remains honestly stopped by unrelated example transcript divergence. That does not block this visual acceptance and must not be represented as a green full-repository gate.
Deployment qualification

GitHub Pages run 31110517661 for commit 4daf7d8 is not a successful run. GitHub reports failure after actions/deploy-pages reached its polling timeout. Record it exactly as a deployment-polling stop.

This does not reverse visual acceptance:

    the handoff records successful Pages run 31109086658 for
    c388ab42dfc4f5c7d49abc71596d6bb511af5742;

    that run deployed the corrected CSS and unchanged JavaScript;

    the package records HTTP 200, noindex, and deployed/source byte parity;

    commit 4daf7d8 records the post-deployment evidence/handoff rather than a new visual correction.

Do not claim that run 31110517661 succeeded. Before any eventual public cutover, the exact intended production commit must have a successful Pages/deployment result and direct deployed-asset verification.
Required continuity update

Append this entire acceptance verbatim under:

## Independent review round 1 acceptance — reviewer to Codex

in:

build/agent-continuity/liturgy-reader-visual-plan.md

Then append Codex’s response with:

    acknowledgment that all three Round 1 questions passed;

    the exact production-integration work-unit plan;

    the behavioral seams that remain frozen;

    the first production file(s) proposed for change;

    the evidence matrix that will prove prototype-to-production parity;

    explicit confirmation that public cutover and public navigation remain unauthorized.

Commit and push the continuity update as part of the build tree. Include this acceptance and the updated continuity record in every subsequent production-integration handoff.
Next phase

Production-integration execution is authorized.

The first integration checkpoint should:

    inventory the accepted Instrument prototype presentation hooks against the existing production Day and Propers reader shell;

    identify the smallest shared production presentation seam;

    preserve accepted state adapters, renderer reuse, Ordinary seating, fail-closed behavior, semantic-location restoration, focus, race ownership, and one-step actions;

    move the accepted visual system into production code without yet changing public navigation or removing the isolated prototype;

    capture production-vs-accepted-prototype parity at the governing desktop, intermediate, mobile, 200%, forced-colors, focus, modal, Read, Missal, Roman partial, and postconciliar states;

    stop for independent integration review before public cutover.

Final authorization

    Liturgical Instrument visual correction: accepted

    Production visual foundation: accepted

    Production-integration execution: authorized

    Public navigation change: unauthorized

    Public cutover: unauthorized

## Codex response to independent review round 1 acceptance

All three bounded Round 1 questions passed: shell integration is continuous from the accepted 1440-pixel rail through 1024, 768, 393, and 320; the 200% state retains whole readable labels and usable targets; and the shell correction did not regress accepted geometry or behavior. The visual correction deliverable can therefore close as accepted, and production-integration execution can begin.

### Production-integration work-unit plan

1. **PI-A — hook inventory and smallest shared seam.** Map every accepted Instrument presentation hook, token, responsive rule, and surface state against the existing production Day and Propers reader DOM and styles. Record any missing hook or selector conflict before mutation. The first production file proposed for change is `src/web/browser/liturgy/reader-shell.css`, which owns the shared persistent actions, open surfaces, reserve, focus treatment, forced-colors response, and responsive dock. No controller or state change is proposed.
2. **PI-B — shared shell and Day presentation.** Move the accepted masthead/action-shell/open-surface grammar into the shared production CSS, then move the accepted Day reading plane, Missal cue grid, first-viewport hierarchy, warning hierarchy, and ritual rhythm through `src/web/browser/liturgy/day-missal.css` and `src/web/browser/liturgy/day-reader.css`. Production assembly, renderer output, Ordinary seating, and event ordering remain owners of content and semantics. Production HTML will change only if the inventory proves an existing semantic element lacks a stable presentation hook; such a conflict must be recorded before editing.
3. **PI-C — Propers presentation parity.** Apply the same accepted identity, reading-axis, Browse, masthead, action, and surface grammar through `src/web/browser/liturgy/propers-reader.css`, preserving the distinct Browse entrance and the prohibition on Propers Missal. JavaScript remains unchanged unless a concrete accepted-seam conflict is demonstrated and logged.
4. **PI-D — parity, gates, and immutable integration handoff.** Capture accepted-prototype and production-reader pairs, compare measured geometry and semantic state, run the focused and governed checks with honest unrelated-gate dispositions, verify the locked public-alpha artifact and unlinked/noindex routes, and assemble a new immutable production-integration handoff containing this acceptance. Stop for independent integration review; do not change public navigation, remove the isolated prototype, or begin public cutover.

### Frozen behavioral and visual seams

The accepted M1 URL/state owners, production Day and Propers adapters, production Proper and Ordinary renderers, single Ordinary seating path, edition-specific option validity, fail-closed invalid and unsupported outcomes, semantic-location preservation and restoration, modal entry/Escape/inert/focus restoration, committed-render and race ownership, four one-step named actions, reduced-motion and forced-colors behavior, source honesty, explicit absences, release isolation, and noindex/unlinked status remain frozen. The accepted visual direction, typography, 39.75rem/636-pixel portrait reading measure, ritual cue grid, first-principal-text hierarchy, warning treatment, masthead, narrow-title wrap, mobile exchange rhythm, Ordinary/Proper composition, and Date/Browse entrance model are likewise frozen. Any concrete integration conflict must be proved and appended before a seam is reconsidered.

### Prototype-to-production parity evidence matrix

The integration evidence will pair the accepted prototype with the production reader at the same route state, query/hash, viewport, scroll position, semantic location, and open surface:

- Day Read at 1440×900, 1024×768, 768×1024, and 393×852.
- Day Missal at 1440×900, 1024×768, 393×852, and 320×852, plus 1440×900 deep scroll.
- Roman 1962 partial coverage at 393×852 and postconciliar partial-English coverage at 1440×900 and 393×852.
- Propers Read at 1440×900 and 393×852, and Propers Browse at 393×852.
- Date open at 1024×768, Contents and Mode open at 393×852, and Details open at 1440×900.
- 200% text, forced colors, reduced motion, and keyboard focus at 393×852.

Each pair will record reading measure, first-principal-text position, rail/dock edge ownership, opacity, radius, shadow, block-end reserve, whole-label line boxes, target size, horizontal overflow, focus owner, semantic state, console errors, failed requests, HTTP errors, and production/prototype asset hashes. The 768×1024 Read target remains 636 pixels/about 75 characters; accepted Missal positions and normal mobile rhythm must not move absent a recorded conflict.

Public navigation changes and public cutover remain explicitly unauthorized. The isolated prototype remains available as the accepted comparison oracle throughout integration.

## Acceptance decision and checkpoint additions

- 2026-08-06 — Independent Round 1 acceptance resolves all three bounded shell questions and all seven Round 0 findings. Liturgical Instrument is now the accepted production visual foundation; Quiet Folio and Contemporary Reader remain frozen references.
- 2026-08-06 — Production-integration execution is authorized through the bounded PI-A–PI-D plan above. Integration begins at the shared production CSS presentation seam and does not itself authorize public navigation or cutover.
- 2026-08-06 — GitHub Pages run `31110517661` for post-deployment evidence commit `4daf7d8a1e1c509edb81a738cc71223170bbbd2d` failed after `actions/deploy-pages` reached its polling timeout. The accepted deployed-parity owner remains successful run `31109086658` for `c388ab42dfc4f5c7d49abc71596d6bb511af5742`; direct HTTP 200/noindex and CSS/JS parity evidence from that run remains controlling.
- 2026-08-06 — This acceptance checkpoint changes only durable continuity and the delivery trackers. No production CSS, HTML, JavaScript, public route, navigation, or prototype file is changed; the next exact action is the PI-A hook inventory.
- 2026-08-06 — Acceptance-record validation passed: `tools/tpt check-promised-deliverables` reports 21 tracked/16 complete, `tools/tpt --check` reports 34 registered tools, and `git diff --check` exits 0. Product/browser suites are unchanged from the independently accepted package because this checkpoint has no product-code delta.
- 2026-08-06T15:09:11Z — Pages run `31113461987` for acceptance-record commit `1608f0ee0ee61df956247072a91647147548c5ad` failed only after `actions/deploy-pages` polled a `deployment_in_progress` result for 600 seconds and timed out. Checkout, locked dependency setup, deployable-source verification, public build, Pages compatibility verification, configuration, and verified-artifact upload all passed. Direct Day and Propers Instrument routes remain HTTP 200 with `noindex, nofollow, noarchive, nosnippet, noimageindex`; deployed/source CSS SHA-256 remains `850e1acacb6f487a5c2f3118388b3fce7b96f9db667e783ba35cdef7d9918b48` and JavaScript remains `eb1c1dd5c0c9c7076b74f2187627dc56e39963429212c0a51872df0ea98a9679`. The run is a deployment-polling stop, not success, and does not replace successful deployed-parity run `31109086658`.

## Production integration PI-A — hook inventory and seam decision

### Inventory result before product mutation

The accepted Instrument prototype and the two production candidates already
share the semantic reading hooks emitted by the production renderers:
`.reader-identity`, `.reader-context`, `.celebration-title`, `.entry-title`,
`.entry-meta`, `.coverage-notice`, `.reader-document`, `.proper`,
`.proper-name`, `.proper-ref`, `.passage`, `.composed`, `.ordinary-frame`,
`.ordinary-division`, `.ordinary-element`, `.speaker-tag`, and the existing
semantic-location attributes. The existing `[data-reader-shell]`,
`[data-reader-action]`, `[data-reader-surface]`, and `[data-reader-contents]`
contract likewise already owns the four actions, dialogs, Contents state,
modal focus entry, Escape, inert background, and semantic-location restoration.
No controller, renderer, seating, state-contract, or state-adapter rewrite is
needed.

The smallest production presentation seam is one new last-loaded stylesheet,
`src/web/browser/liturgy/reader-instrument.css`, scoped through a shared
`.reader-instrument` class on the existing candidate shell. This supersedes the
earlier PI-A expectation that `reader-shell.css` would be the first file
changed. The earlier statement remains above; this appended correction is
controlling because inventory proved that `reader-shell.css` is already the
accepted interaction-neutral base and that a scoped override avoids a broad
refactor. It also avoids `day-missal.css`, which public Day and Propers routes
load and therefore cannot change under the current isolation boundary.

The production HTML needs only stable presentation hooks: the accepted
masthead, `.reader-instrument`, `data-reader-mode`, `.action-label`, and
project-owned icon hosts with hidden decorative marks. The existing candidate
flags remain truthful in the DOM and become visually hidden. The accepted
short dock labels are Date or Browse, Contents, Mode, and Details; surface
headings may retain their explicit edition wording.

### Proved presentation-adapter conflict and bounded resolution

Two accepted outcomes are not achievable through CSS alone. First, the
production renderers emit a source-owned top-level `.uncompiled` node and
direct `.notice` children within Ordinary elements, while the accepted warning
hierarchy moves the existing uncompiled content into the identity-level
coverage notice and groups direct absence notices as
`.ordinary-absence-inline`. Second, the accepted Read/Missal geometry requires
an authoritative `data-reader-mode` styling hook. The prototype supplies both
through post-render observers, but importing that prototype controller would
also import `?design=` URL ownership, duplicate semantic-progress and mode
observers, and title-filter behavior that is expressly out of scope as search.

The bounded production resolution is generation-safe adapter composition:

- Day exposes its already authoritative committed mode on the existing shell
  during `commitOutcomePresentation()`; it does not derive or own another mode.
- Day and Propers move the renderer-owned uncompiled node's existing children
  into `#coverage-notice` before the winning render is committed, preserving
  every word and absence while eliminating a second dominant warning.
- Day groups only direct renderer-owned `.notice` children inside their
  already-rendered Ordinary element. The wrapper adds no ID, focus target,
  semantic location, or invented content.

These are presentation hooks inside the existing committed render path, not a
change to state, assembly, rendering, seating, semantic order, or race
ownership. `reader-shell.js`, `reader-state.js`, `reader-state-adapters.js`,
`ordinary-seating.js`, `assembly-model.js`, shared renderer code, production
data, and public Day/Propers routes remain frozen.

The prototype's title-filter Browse UI is not ported because search remains an
explicitly deferred capability. Propers retains its accepted distinct Browse
entrance and canonical production form while receiving the accepted Instrument
masthead, shell, surface, typography, and responsive composition. This is the
only planned production/prototype visual difference and will be stated and
shown in the integration handoff rather than hidden.

### PI-A decision and next action

- 2026-08-06 — Hook inventory complete; smallest seam is the new scoped
  `reader-instrument.css` loaded last by both unlinked production candidates.
- 2026-08-06 — The only justified adapter changes are authoritative mode
  exposure and generation-safe composition of renderer-owned absence nodes.
- 2026-08-06 — Pages run `31114653517` for settlement commit
  `b3ae6bddaab631661d342380f61365d851be160c` is recorded as another 600-second
  deployment-polling failure after repository-owned build and upload passed;
  successful deployed correction parity remains run `31109086658`.
- Next exact action: implement the scoped stylesheet and stable HTML hooks,
  make the bounded adapter composition changes, update task-owned tests, and
  extend the existing visual-reset harness into paired prototype/production
  evidence. Public navigation and public cutover remain unauthorized.

## Production integration PI-B–PI-D — local candidate checkpoint

### Implemented production presentation seam

The new `src/web/browser/liturgy/reader-instrument.css` is loaded last only by
the existing unlinked, noindex `day-reader.html` and `propers-reader.html`
candidates. It carries the accepted Instrument masthead, typography, Read
axis, Missal cue grid, compact warnings and absence notation, external ruled
rail, opaque square intermediate/mobile dock, extreme-reflow 2×2 dock, open
surfaces, focus treatment, forced-colors behavior, reduced-motion behavior,
and print preservation. The existing public `day.html` and `index.html` do not
load it and have not changed.

Both candidate pages now expose the accepted masthead and stable action-label
hooks with project-owned inline SVG icons. Day exposes the already-committed
mode as `data-reader-mode`; Day and Propers relocate the existing source-owned
uncompiled message into the identity coverage notice; and Day groups direct
Ordinary absence notices without changing their text, semantic event,
location, or renderer ownership. No state, adapter, renderer, seating, shared
shell controller, production data, or public route was changed.

Propers Browse deliberately retains the existing production selector rather
than importing the accepted prototype's title-filter control. Search remains
out of scope. The Date/Browse entrance distinction, all four one-step actions,
and the common Instrument composition remain visually explicit.

### Prototype-to-production measurements

The final Chromium run captured 23 accepted-prototype/production pairs at the
same state, viewport, scroll, and open surface, plus the complete existing
direction matrix: 100 captures in all, with 19/19 governed assertions.

| Governing state | Accepted prototype | Production candidate | Delta/disposition |
| --- | --- | --- | --- |
| Day Read 768×1024 | 636 px, about 75 characters; first text 267.39 px | 636 px, about 75 characters; first text 268.03 px | measure exact; first text +0.64 px |
| Day Missal 393×852 | 351 px text plane; first principal text 324.09 px | 351 px text plane; first principal text 320.66 px | width exact; production 3.43 px earlier |
| 200% text at 393×852 | four 178.91×104 px targets; all labels one line | same four target boxes; all labels one line | exact shell geometry; no mid-word breaks |
| Intermediate 1024 dock | square, opaque, shadowless, edge-bound | same computed shell properties and reserved block end | pass |

The harness also records zero required horizontal overflow, unnamed
interactive controls, duplicate IDs, console errors, failed requests, or HTTP
errors. Final source hashes are: accepted oracle CSS
`850e1acacb6f487a5c2f3118388b3fce7b96f9db667e783ba35cdef7d9918b48`;
production Instrument CSS
`64a566758f20df72f53f0f1dfc90ba82fe4ad28cf0ed55a346066f6c1ed5ee02`;
Day HTML `5bc859042e907565afb304beaf0d5ae099c571933c474760c77730a9245531b9`;
Day JavaScript `405069b81214d3598d568433b68440ac3433d7ceef09d64a05506b907ebc8320`;
Propers HTML `9d30a46afc8d890e95a3e1dd8aab04a164eea906b0b88f520f2c70e878b9560b`;
and Propers JavaScript
`135f1864bb227ab35058a3fad614d9c7855d1c78aff048dae4bdae3fc69f4ad0`.

### Full-size visual self-review

Every one of the 23 production originals was inspected at original pixels,
and the paired contact sheet was inspected as a complete system.

- Read at 1440, 1024, 768, and 393 keeps one deliberate axis. The 1024 dock is
  edge-owned and text ends above it; the portrait measure is the accepted 636
  pixels; mobile does not become a different composition.
- Missal at 1440, 1024, 393, and 320 begins with real ritual text promptly,
  retains the wide cue grid and coherent mobile stacking, and preserves the
  deliberate narrow division-title wrap. Deep scroll retains the ruled rail
  and subordinate provenance.
- Roman partial coverage has one compact identity statement before held
  Ordinary text. Postconciliar partial-English coverage exposes held Propers
  before restrained grouped absences at desktop and mobile.
- Propers Read shares the same masthead, measure, typography, shell, and
  surfaces. Propers Browse remains visibly the distinct production entrance;
  its form is the disclosed out-of-scope search difference, not an accidental
  parity gap.
- Date, Contents, Mode, and Details surfaces retain coherent geometry,
  backdrop, focus entry, and reading context. The 200% state uses whole labels
  in a 2×2 dock; forced colors remains legible; keyboard focus is explicit;
  reduced motion changes no content or control reachability.

No visual, behavioral, accessibility, or isolation blocker was found in local
self-review. This is not independent acceptance.

### Local validation before checkpoint commit

- Focused Python suite: 142/142 passed after the historic prototype-isolation
  guard was narrowed to exclude exactly the newly authorized
  `reader-instrument.css` candidate seam; frozen public/shared files remain
  byte-checked.
- Day browser harness: 33/34, with only the unchanged date-dependent
  first-visit expectation; every task-owned assertion passed.
- Propers browser harness: 27/27 passed.
- Shared-shell browser harness: 18/18 passed.
- Governed visual harness: 19/19 assertions, 100 captures, zero browser or
  accessibility failures.
- Node syntax checks passed for Day, Propers, the accepted visual oracle, and
  the extended visual harness.
- `tools/tpt public-alpha check`, locked build, and
  `verify --deployment-target github-pages` passed. Release bindings are exact,
  including the newly adopted Instrument CSS source and updated Day/Propers
  hashes.
- `tools/tpt check-promised-deliverables`, `tools/tpt --check`, and
  `git diff --check` pass. `tmt` is unavailable both on `PATH` and at the
  documented personal fallback, so the requested repeatable-tool note could
  not be recorded.

### PI-D checkpoint status

- Implementation and local parity are complete; no task-owned check is
  presently failing.
- Exact checkpoint commit, push, Pages run, deployed source parity, handoff
  manifest, and ZIP verification remain to be appended after those events.
- Independent production-integration review remains the gate. Public
  navigation and public cutover remain unauthorized.

## Production integration implementation checkpoint — push and clean gate

- 2026-08-06 — Commit `3cd46072b164ff39b00639bb67ad6b8943a255dc`
  records the candidate-scoped Instrument CSS, Day and Propers presentation
  hooks, bounded generation-safe absence composition, 19-assertion/100-capture
  parity harness, release bindings, tests, roadmap, work register, promised
  deliverable, and this continuity record. It was pushed normally to
  `origin/main`; no force, amend, rebase, remote change, public navigation, or
  cutover occurred.
- The exact clean-tree `make check` invocation passed all preceding governed
  checks and stopped at `check-examples` with exit 2: 200 captured examples,
  188 replayed, 23 divergent, 35 known stale, 6 never run, 6 unrunnable here,
  and 2 declared volatile lines. This is the repository's unrelated transcript
  divergence and is not green. No example was recaptured or blessed.
- The final local public-alpha policy/build/Pages-target verify and the private
  preview build/verify pass with the locked Markdown environment. Release
  bindings are exact, including Instrument CSS SHA-256
  `64a566758f20df72f53f0f1dfc90ba82fe4ad28cf0ed55a346066f6c1ed5ee02`.
- As of 2026-08-06T18:04:26Z, `origin/main` resolves to the implementation
  commit, but GitHub's Actions API returns no run for that head SHA. This is a
  pending workflow-event observation, not a successful run and not a failed
  run. No manual workflow was dispatched because the task authorizes only the
  normal push-triggered deployment attempt.
- Next exact action: commit this truthful post-push record, push it as the
  continuity checkpoint, observe the resulting automatic Pages run, verify
  the unlinked Day and Propers candidates, the noindex visual oracle, and
  deployed source hashes, then finalize the immutable integration-review
  handoff.

## Production integration deployment observation and handoff boundary

- 2026-08-06 — Continuity checkpoint
  `e35f81c1e67c744aead0e4eaa73e079516751e66` was pushed normally to
  `origin/main`. As of 2026-08-06T18:08:35Z, the GitHub Actions API exposed no
  run for either that head or implementation head
  `3cd46072b164ff39b00639bb67ad6b8943a255dc`.
- Direct deployed Day and Propers candidate routes return HTTP 200 but serve
  the prior artifact: their HTML SHA-256 values differ from the integrated
  source, and deployed Day does not reference `reader-instrument.css`.
  Therefore production deployed parity is open. The routes retain their
  pre-existing public-alpha robots policy; the separate accepted visual-reset
  oracle remains unlinked and noindex.
- No manual workflow was dispatched. The normal push-triggered workflow is the
  only deployment authority granted by this task, so the absent workflow event
  is an external-state blocker rather than permission to invoke another
  deployment mechanism.
- The new local review package is
  `build/agent-handoffs/20260806T171432Z-liturgy-reader-instrument-production-integration/`
  with a same-name ZIP. The original correction task's force-add exception is
  path- and slug-bounded and does not authorize tracking this new production-
  integration handoff. The package is therefore assembled and verified as an
  ignored local artifact; the already-tracked canonical continuity remains the
  durable pushed record.

## Message to the next independent production-integration reviewer

The production Day and Propers candidates now visibly use the accepted
Liturgical Instrument masthead, reading axis, Missal cue grid, warning
hierarchy, rail/dock, 200% reflow, surfaces, and accessibility finish. Begin
with the labeled `evidence/prototype-production-parity-contact-sheet.png`, then
inspect all 23 production originals at full size beside the accepted originals.
Look first at Day Read 768×1024, Day Missal 393×852, Day partial 393×852,
postconciliar Missal at both sizes, Propers Browse 393×852, the 1024 Date
surface, and the 200%/forced-colors/focus states.

One difference is deliberate and provisional only in the sense of scope:
Propers keeps its canonical production Browse selector; the prototype title
filter is search and was not integrated. No accepted visual or behavioral seam
is otherwise reopened. Local parity and task-owned gates pass, but deployed
parity is not established because GitHub did not materialize either automatic
Pages run and the deployed routes still serve the prior artifact.

The requested decisions are exact: does production match the accepted
Instrument across the matrix; is retaining production Browse the correct
out-of-scope-search disposition; did the bounded presentation composition
preserve every frozen behavior; and, only after a successful Pages run and
direct asset parity exist, is production integration accepted? Public
navigation and public cutover remain unauthorized regardless of the review
disposition.

## Delayed Pages run observation

- GitHub materialized automatic Pages run `31125352169` for implementation
  commit `3cd46072b164ff39b00639bb67ad6b8943a255dc` at
  2026-08-06T18:11:51Z, after the first immutable local handoff had been sealed
  at its truthful no-run cutoff.
- Codex monitored the run continuously through 2026-08-06T18:27:03Z. The
  workflow and its `deploy` job remained `queued`; `startedAt` was recorded as
  2026-08-06T18:11:52Z by the API, but no runner step, log, build, upload, or
  deployment action began, `updatedAt` remained 2026-08-06T18:11:54Z, and no
  conclusion existed.
- This is a queued external-state result, neither success nor failure. It does
  not establish deployed parity and does not supersede the last successful
  accepted-correction run `31109086658`.
- Because the earlier integration handoff is immutable, the latest handoff is
  a fresh successor at
  `build/agent-handoffs/20260806T182703Z-liturgy-reader-instrument-production-integration/`
  and its same-name ZIP. It contains this exact observation and points the next
  reviewer/agent to run `31125352169` first.

## Successful production-integration deployment and parity

- 2026-08-06 — Automatic Pages run `31125352169` for implementation commit
  `3cd46072b164ff39b00639bb67ad6b8943a255dc` ultimately completed with failure
  after its deploy job was cancelled before any repository step ran. Follow-up
  run `31125595375` for continuity commit
  `e35f81c1e67c744aead0e4eaa73e079516751e66` completed cancelled. These runs
  are not deployment successes and are retained here as exact chronology.
- Automatic Pages run `31125898045` succeeded for exact intended production
  commit `5444d89fc9b379a1babef5b2220323fe1508b2b3`. The workflow was created at
  2026-08-06T18:26:07Z, its deploy job ran from 18:28:11Z through 18:29:54Z,
  and the run completed at 18:29:55Z. Checkout, Python setup, dependency
  installation, deployable-source verification, site build, GitHub Pages
  verification, Pages configuration, artifact upload, and deployment all
  passed.
- Direct verification after that run returned HTTP 200 for the Day production
  reader candidate, Propers production reader candidate, and both accepted
  visual-reset oracle routes. Day and Propers load `reader-instrument.css`.
  The oracle routes retain `noindex, nofollow, noarchive, nosnippet,
  noimageindex`; the production candidates retain the existing public-alpha
  robots policy and remain absent from public navigation.
- Deployed/source SHA-256 parity is exact for Instrument CSS
  `64a566758f20df72f53f0f1dfc90ba82fe4ad28cf0ed55a346066f6c1ed5ee02`,
  Day JavaScript
  `405069b81214d3598d568433b68440ac3433d7ceef09d64a05506b907ebc8320`,
  Propers JavaScript
  `135f1864bb227ab35058a3fad614d9c7855d1c78aff048dae4bdae3fc69f4ad0`,
  accepted-oracle CSS
  `850e1acacb6f487a5c2f3118388b3fce7b96f9db667e783ba35cdef7d9918b48`,
  and accepted-oracle JavaScript
  `eb1c1d06274dfaf99165a72735670c372c524f95363f5e104669b72f7d01ba0d`.
- This supersedes the deployment-open qualification in the earlier reviewer
  message without rewriting that append-preserved history. The new immutable
  deployed-parity successor is
  `build/agent-handoffs/20260806T183040Z-liturgy-reader-instrument-production-integration/`
  and its same-name ZIP. The original correction task did not authorize
  force-adding a new production-integration handoff slug, so this package is a
  verified ignored local artifact; this canonical continuity file remains the
  pushed durable record.

## Superseding message to the next independent production-integration reviewer

Production integration and deployed/source parity are complete. Begin with
`evidence/prototype-production-parity-contact-sheet.png`, then inspect the 23
production originals at full size beside their accepted prototype counterparts.
Look first at Day Read 768×1024, Day Missal 393×852, Roman partial 393×852,
postconciliar Missal at desktop and mobile, Propers Browse 393×852, Date open
at 1024×768, and the 200%, forced-colors, and focus states.

The exact decisions requested are: does the integrated production presentation
match the accepted Instrument across the governing matrix; is retaining the
canonical production Browse selector the correct disposition because the
prototype title filter is out-of-scope search; did the bounded CSS and
generation-safe composition preserve every frozen behavioral seam; and is this
production integration accepted? No known implementation, evidence,
deployment, asset-parity, accessibility, or isolation blocker remains. The
governed full gate is still honestly non-green only at unrelated stored example
transcript divergence. Public navigation and public cutover remain unauthorized
regardless of the integration-review disposition.

## Successful deployment record checkpoint

- 2026-08-06 — Commit `0d683db725219e258f3444720b33908d4cf01e63`
  records successful Pages run `31125898045`, the direct deployed/source hash
  verification, the completed deployment-evidence requirement, and the exact
  remaining independent-review gate. It was pushed normally to `origin/main`.
- The next exact action is to seal the fresh immutable deployed-parity handoff,
  verify its byte-identical continuity copy, manifest, ZIP, and one-top-level
  archive shape, and stop for independent production-integration review.
- This final continuity append is a record-only handoff boundary. It changes no
  candidate code, accepted visual detail, behavioral seam, public route, or
  navigation.

## Deployed hash transcription correction

- 2026-08-06 — A final direct HTTP verification found that the accepted-oracle
  JavaScript hash written in **Successful production-integration deployment and
  parity** above was transcribed incorrectly. The deployed file and source are
  byte-identical at the correct SHA-256
  `eb1c1dd5c0c9c7076b74f2187627dc56e39963429212c0a51872df0ea98a9679`.
  This appended correction supersedes only the earlier mistyped
  `eb1c1d06274dfaf99165a72735670c372c524f95363f5e104669b72f7d01ba0d`
  statement; it does not change the parity disposition, code, evidence, or
  review gate.

## Independent production-integration review — reviewer to Codex

Liturgical Instrument — Independent Production-Integration Review
Disposition

PRODUCT INTEGRATION ACCEPTED — ONE DURABLE-HANDOFF CLOSEOUT REQUIRED

The production Day and Propers reader candidates successfully carry the accepted Liturgical Instrument presentation into the existing production architecture. All six requested integration questions pass.

No product-code, visual-design, screenshot, browser-harness, or deployment correction is requested.

One repository-process requirement remains unresolved: the sealed production-integration handoff directory and ZIP reviewed here were uploaded to the reviewer but were not committed and pushed under build/agent-handoffs/. This violates the maintainer's explicit requirement that the plan, reviewer/Codex exchange, and handoff artifacts remain recoverable by a clean agent from the pushed build tree.

Production integration is accepted on its merits. Its tracked deliverable must not be marked fully closed, and cutover planning must not begin, until the exact reviewed handoff is pushed unchanged and this review is appended to the canonical continuity record.

Public navigation remains unauthorized. Public cutover remains unauthorized.
Reviewed state

    Integration implementation commit:
    3cd46072b164ff39b00639bb67ad6b8943a255dc

    Exact successfully deployed production commit:
    5444d89fc9b379a1babef5b2220323fe1508b2b3

    Final pushed continuity boundary reviewed:
    0059e501dc535f4546f3966143c8af21e1e119c8

    Successful GitHub Pages run:
    31125898045

    Reviewed handoff directory:
    20260806T183040Z-liturgy-reader-instrument-production-integration/

    Reviewed transport ZIP:
    20260806T183040Z-liturgy-reader-instrument-production-integration.zip

    Independently calculated ZIP SHA-256:
    ebf0361309ac33b4580cbb535e4bbd3eabd144756e6c078aa140e716c748f05f

Independent package verification

The reviewer independently verified:

    the ZIP integrity test reports no bad member;

    the ZIP contains exactly one top-level directory;

    all 216 entries in MANIFEST.sha256 verify;

    the archive contains 257 total entries including directories;

    the candidate and included source copies of reader-instrument.css agree with the recorded source hash;

    the parity contact sheet, regression contact sheet, and all 23 production originals were inspected;

    the bounded JavaScript changes and their ownership implications were reviewed from changes.patch;

    the continuity record, prototype-to-production map, measurements, isolation statement, checks, browser results, and deployment record agree.

Requested integration dispositions
1. Production Day parity

PASS

The production Day candidate belongs to the accepted Instrument system in all reviewed governing states:

    Read at 1440×900, 1024×768, 768×1024, and 393×852;

    Missal at 1440×900, 1024×768, 393×852, and 320×852;

    deep-scroll Missal;

    Roman partial coverage;

    postconciliar partial-English coverage at desktop and mobile.

The production integration preserves the accepted hierarchy, reading plane, desktop cue grid, mobile ritual stacking, first-viewport text timing, compact warning treatment, and rail-to-dock behavior.

The small measured differences are benign and favorable: the 768-pixel Read measure remains exactly 636 pixels/about 75 characters, and production mobile Missal begins its principal text about 3.43 pixels earlier than the accepted oracle.
2. Production Propers parity and canonical Browse

PASS

Production Propers Read shares the accepted masthead, typography, reading axis, Proper hierarchy, rail/dock, surfaces, and responsive behavior.

Retaining the canonical production Browse & edition selector is the correct scoped decision. The prototype title filter is search functionality, and search was explicitly outside this integration. The production selector remains visually coherent with the Instrument and preserves the distinct Propers entrance without importing unapproved behavior.

This is an intentional scope difference, not a parity failure.
3. Shell, reflow, accessibility, and surfaces

PASS

The reviewed evidence preserves:

    the external ruled rail at desktop;

    the opaque, square, edge-bound dock at intermediate and mobile widths;

    reserved block-end space so text is not obscured;

    the labeled 2×2 extreme-reflow dock at 200%;

    whole Date/Browse, Contents, Mode, and Details labels;

    adequate target sizes;

    no required horizontal overflow;

    visible keyboard focus;

    usable forced-colors presentation;

    reduced-motion behavior;

    coherent Date, Browse, Contents, Mode, and Details surfaces;

    modal backdrop, focus entry, Escape, inertness, and context preservation through the established shared shell.

The 1024 state does not regress to the rejected floating card, and the 200% state does not fragment labels.
4. Accepted reading and ritual geometry

PASS

Integration preserves:

    the 636-pixel/about-75-character portrait Read measure;

    one deliberate Read axis;

    the accepted first-principal-text hierarchy;

    subordinate coverage warnings;

    continuous Ordinary action;

    semantic cue alignment;

    deliberate narrow mobile division-title wrapping;

    normal-scale mobile rhythm;

    deep-scroll shell access and provenance hierarchy.

The production presentation is not merely similar to the oracle; it carries the same compositional system through production-owned DOM and content.
5. Frozen behavior and source ownership

PASS

The integration uses one last-loaded, candidate-scoped presentation stylesheet and minimal stable HTML hooks. It does not replace production state, adapters, renderers, Ordinary seating, shared shell behavior, data, sources, editions, or translations.

The reviewed JavaScript changes are bounded:

    Day exposes the authoritative committed mode as a styling attribute and updates the masthead label from that same committed state.

    Day and Propers relocate the existing uncompiled message into the identity coverage notice without inventing or weakening source text.

    Day groups existing direct Ordinary notice nodes for presentation without replacing their IDs, text, semantic events, locations, renderer ownership, or generation checks.

The package records passing task-owned tests for state/URL ownership, renderer reuse, fail-closed behavior, semantic-location restoration, focus, race ownership, source honesty, and four one-step actions. The accepted visual oracle remains unchanged, unlinked, and noindex; the public Day and Propers routes remain unchanged and unlinked from these candidates.

The Day browser's 33/34 result remains the disclosed, unchanged date-dependent first-visit expectation. The governed full repository gate remains non-green only at the unrelated stored example-transcript divergence. Neither is represented as a task-owned pass.
6. Final integration decision

PASS — PRODUCTION INTEGRATION ACCEPTED

No visual, behavioral, accessibility, deployment, source-ownership, or production-isolation blocker remains in the integrated reader candidates.

The successful Pages run is tied to exact intended production commit
5444d89fc9b379a1babef5b2220323fe1508b2b3, and the package records direct HTTP and deployed/source asset parity for Day, Propers, the Instrument stylesheet, and the accepted oracle assets.
Required durable-handoff closeout
Finding

At pushed boundary 0059e501dc535f4546f3966143c8af21e1e119c8, the repository's build/agent-handoffs/ directory contains the three earlier correction handoffs and ZIPs, but it does not contain:

    build/agent-handoffs/20260806T183040Z-liturgy-reader-instrument-production-integration/

    build/agent-handoffs/20260806T183040Z-liturgy-reader-instrument-production-integration.zip

The package's own continuity record explains that the production-integration handoff was left as an ignored local artifact because the earlier force-add authority was slug-bounded to the correction handoff.

That caution was correct under the prior wording. This review now supplies the missing exact authority.
Explicit build-tree authorization

The maintainer's continuity requirement authorizes Codex to use git add -f for exactly these two already-sealed artifacts:

build/agent-handoffs/20260806T183040Z-liturgy-reader-instrument-production-integration/
build/agent-handoffs/20260806T183040Z-liturgy-reader-instrument-production-integration.zip

Do not force-add any other ignored handoff, cache, build output, or generated file under this authority.

The pushed directory and ZIP must be byte-identical to the reviewed package:

ZIP SHA-256:
ebf0361309ac33b4580cbb535e4bbd3eabd144756e6c078aa140e716c748f05f

Before staging, rerun:

    ZIP integrity test;

    one-top-level-directory check;

    sha256sum -c MANIFEST.sha256;

    transport ZIP SHA-256;

    comparison of the local sealed artifacts against the reviewed values.

Canonical continuity update

Append this complete review verbatim under:

## Independent production-integration review — reviewer to Codex

in:

build/agent-continuity/liturgy-reader-visual-plan.md

Append Codex's response immediately after it. The response must:

    acknowledge that all six product-integration questions passed;

    record the exact reviewed ZIP hash;

    explain that the only remaining action is durable artifact closeout;

    state that no product or evidence bytes were changed;

    record the commit that force-adds the exact handoff directory and ZIP;

    confirm main, origin/main, and the remote agree;

    retain the honest dispositions of the Day date-dependent assertion and unrelated example transcript divergence;

    retain the prohibition on public navigation and cutover.

Update PROJECT-WORK.md, guidance/liturgy-browser-roadmap.md, and
promised-deliverables.toml so they distinguish:

    production integration: independently accepted;

    durable handoff closeout: complete only after the artifacts are pushed;

    public navigation/cutover: still unauthorized.

Closeout boundary

Do not modify:

    reader-instrument.css;

    Day or Propers HTML/JavaScript;

    the accepted prototype;

    browser evidence;

    screenshots;

    the reviewed handoff directory contents;

    the reviewed ZIP contents.

No new visual capture or full integration re-review is required if the only changes are:

    appending this review and Codex response to continuity;

    truthful tracking-state updates;

    force-adding the exact unchanged reviewed handoff directory and ZIP.

Return the closeout commit SHA, repository paths, manifest result, and ZIP hash for a narrow archival verification.
Authorization after closeout

    Liturgical Instrument production integration: accepted

    Production visual foundation: accepted

    Existing candidate implementation: accepted

    Durable handoff closeout: required before the phase is marked complete

    Separate public-cutover planning: may begin only after closeout

    Public navigation change: unauthorized

    Public cutover execution: unauthorized

## Codex response to independent production-integration review

All six product-integration questions passed. The production Day and Propers
candidates are independently accepted as faithful integrations of the accepted
Liturgical Instrument foundation, including their visual parity, canonical
Propers Browse scope, responsive shell and accessibility behavior, reading and
ritual geometry, frozen behavioral ownership, and production isolation.

The exact reviewed transport ZIP SHA-256 is
`ebf0361309ac33b4580cbb535e4bbd3eabd144756e6c078aa140e716c748f05f`.
Before staging, Codex reran the ZIP integrity test, proved one top-level
directory, verified all 216 `MANIFEST.sha256` entries, and matched that exact
transport hash. Dedicated archival commit
`8c6e1270f692ca4136f2f6a60002bacd3af0440c` force-adds only the exact reviewed
handoff directory and ZIP. That commit was pushed normally to `origin/main`;
immediately after the push, local `main`, `origin/main`, and the remote ref
agreed at `8c6e1270f692ca4136f2f6a60002bacd3af0440c`.

Durable artifact closeout was the only remaining action. No product code,
accepted prototype, browser evidence, screenshot, handoff-directory byte, or
ZIP byte changed. This continuity append and the matching tracking updates are
record-only closeout work.

The Day browser remains honestly 33/34 solely because of its unchanged
date-dependent first-visit expectation. The governed full repository gate
remains non-green solely at unrelated stored example-transcript divergence;
neither result is represented as a task-owned pass. Public navigation and
public cutover remain unauthorized. Separate cutover planning may begin only
after this closeout record is pushed and the remote ref is verified.

## Public cutover planning — reviewer to Codex

Starting boundary: clean `main` at
`7b7044dea7f5c35a2d32ff85f26eb5b182bf40ef`, with local `HEAD`, local
`main`, `origin/main`, and remote `refs/heads/main` required to agree before
planning. Production integration and its durable handoff are accepted and
complete. Exact deployed integration remains commit
`5444d89fc9b379a1babef5b2220323fe1508b2b3`, Pages run `31125898045`; the
accepted archived handoff is
`build/agent-handoffs/20260806T183040Z-liturgy-reader-instrument-production-integration/`
and its ZIP at reviewed SHA-256
`ebf0361309ac33b4580cbb535e4bbd3eabd144756e6c078aa140e716c748f05f`.

Authorization is planning and pre-cutover readiness only. The eventual target
routes are canonical Day `/liturgy/day.html` and canonical Propers
`/liturgy/index.html`; accepted candidates are `/liturgy/day-reader.html` and
`/liturgy/propers-reader.html`. This phase must inventory actual load graphs,
state and URL contracts, navigation, indexing, publication, caching, and Pages
behavior; select the smallest reversible mechanism; prove compatibility in
human- and machine-readable matrices; make the known date-dependent Day test
deterministic only if its disclosed cause is exactly confirmed; produce but
not apply an exact cutover patch; define rollback and acceptance gates; and
seal a tracked immutable planning handoff for independent review.

Frozen decisions include the Liturgical Instrument foundation, one Read axis
and accepted 636-pixel/about-75-character portrait measure, Missal cue grid and
mobile stacking, desktop rail, opaque square intermediate/mobile dock, whole
labels at 200%, compact warnings, masthead and 320-pixel title treatment,
Date/Browse entrance model, canonical production Propers Browse selector, and
all production-owned state adapters, renderers, Ordinary seating, semantic
locations, focus/modal/race ownership, sources, editions, translations, and
fail-closed behavior. The visual-reset Instrument remains the comparison
oracle. Search, redesign, source expansion, renderer changes, prototype or
candidate cleanup, public navigation changes, canonical-route replacement,
and cutover execution are outside this phase.

Required durable artifacts are the route map, mechanism decision and rejected
options, Markdown and JSON state matrix, navigation map, exact unapplied public
cutover patch, rollback procedure, cutover gates, any bounded deterministic Day
test evidence, truthful tracking records, and a timestamped tracked handoff
directory and ZIP with byte-identical continuity/instructions, manifest, and
archive verification. The stopping point is a clean pushed review candidate
whose `main`, `origin/main`, and remote main agree. Independent review may
request changes or authorize a later execution phase; a good plan does not
itself authorize public navigation or public cutover.

## Public cutover planning — Codex response

At kickoff, `git status --short` was empty and `HEAD`, local `main`,
`origin/main`, and remote `refs/heads/main` all resolved exactly to
`7b7044dea7f5c35a2d32ff85f26eb5b182bf40ef`.

Before source inspection, the current canonical-route ownership is believed to
begin at `src/web/browser/liturgy/day.html` plus `day.js`/Day styles for Day,
and `src/web/browser/liturgy/index.html` plus `liturgy.js`/shared styles for
Propers. The accepted candidates are believed to begin at
`day-reader.html`/`day-reader.js`/`day-reader.css` and
`propers-reader.html`/`propers-reader.js`/`propers-reader.css`, both last-loading
`reader-instrument.css` and reusing `reader-shell.js`, reader state/adapters,
production Day/Proper rendering, assembly, and Ordinary seating. These are
initial hypotheses, not the route map.

Analysis will proceed as CO-A canonical/candidate load, URL, publication, SEO,
and navigation inventory; CO-B mechanism comparison and one reversible
decision; CO-C machine-readable state compatibility proof; CO-D exact diagnosis
and, only if safe, test-only deterministic Day correction; CO-E exact proposed
cutover patch built outside canonical working files; CO-F operational rollback;
and CO-G local, canonical-route, oracle, deployment, indexing, and rollback
acceptance gates followed by the immutable planning handoff.

Source inspection must resolve the actual script/style graph, relative fetch
bases, hash/query parsing differences, default-date contract, history and
semantic restoration ownership, robots/title behavior, release-copy rules,
navigation references, service-worker or cache behavior, and whether canonical
HTML replacement can directly reuse candidate modules without redirects or
duplicated state. No public route, public navigation, candidate route, or
accepted prototype will be modified in this planning phase.

## Public cutover planning checkpoint CO-A through CO-C — Codex report

Source tracing confirms there is no hidden route or build alias. Canonical Day
is `day.html` plus the legacy `day.js` DOM/controller; canonical Propers is
`index.html` plus `liturgy.js`. The accepted readers are separate static HTML
entry points loading the accepted state/adapters/shell/controllers and
last-loaded Instrument CSS. All four pages share the same directory and
`../browse` data base, and `tools/public-alpha` renders every top-level liturgy
HTML while copying every top-level liturgy CSS/JS asset.

CO-B selects source-level in-place promotion of the accepted DOM/load graphs
behind the unchanged `day.html` and `index.html` filenames. Redirects,
renames/aliases, build-only copies, and destructive controller replacement are
rejected. The selected mechanism preserves path, query/hash text, relative
assets, source/deployed ownership, and one-commit rollback while reusing the
accepted production implementation.

The complete route, mechanism, navigation, and human/machine state maps are:

- `build/agent-continuity/liturgy-reader-cutover-route-map.md`
- `build/agent-continuity/liturgy-reader-cutover-decision.md`
- `build/agent-continuity/liturgy-reader-cutover-state-matrix.md`
- `build/agent-continuity/liturgy-reader-cutover-state-matrix.json`
- `build/agent-continuity/liturgy-reader-cutover-navigation-map.md`

The inventory records seven cutover blockers rather than obscuring them as
parity: current empty Day defaults to the first rubrics row (postconciliar)
while the accepted reader uses the declared Propers default (Roman 1962);
`why=1` and multi-territorial outcomes currently link back to `day.html` and
would self-link after promotion; production-reachable Propers option states
still write provisional `_candidate-*` keys; deployed candidate raw HTML is
currently `index, follow` with public social URLs because runtime noindex cannot
override the layout's existing robots meta; candidate/internal runtime wording
cannot reach canonical titles; and direct cross-entrance/context footer links
would disappear because Instrument hides generated chrome and offers only
Home. Independent review must resolve these exact dispositions before cutover
execution is authorized.

No service worker, Cache API, webmanifest, sitemap, rewrite layer, or external
runtime dependency exists. GitHub Pages serves unversioned HTML/CSS/JS with
`Cache-Control: max-age=600`; the forward and rollback plans therefore require
mixed-cache-compatible bytes, cache-bypassed parity, and a second verification
after the freshness window. The operational rollback and full later-execution
gate are recorded in:

- `build/agent-continuity/liturgy-reader-public-cutover-rollback.md`
- `build/agent-continuity/liturgy-reader-public-cutover-gates.md`

The Day browser failure was reproduced at exactly 33/34 with zero browser
hygiene failures. The sole failure is the first-visit test's assumption that
the coverage notice is hidden on the wall-clock date; 2026-08-06 correctly has
partial Roman coverage. A test-only browser-clock fixture targeting local noon
2026-08-02 is drafted separately, keeps the URL empty, and adds an exact civil
date assertion. Product Date/default behavior is untouched. Its commit and
34/34 result will be appended after validation.

## Public cutover planning checkpoint CO-D — Codex report

The known Day failure was exactly the disclosed date dependency. Test-only
commit `5e1b82b51` installs a Chrome DevTools Protocol new-document clock fixture
only around the first-visit assertion, keeps the URL empty, and adds the exact
`civilDate === "2026-08-02"` assertion. The fixture is removed in `finally`.
No product, calendar, default-date, canonical-route, candidate-route, or oracle
byte changed.

The Day browser harness now passes 34/34 with zero console, required-request,
HTTP, unnamed-control, duplicate-ID, or overflow failures. The exact diagnosis,
test boundary, and commands are recorded in
`build/agent-continuity/liturgy-reader-day-deterministic-test.md`.

The full governed gate still exits 2 at the unrelated stored example transcript
divergence: 23 of 188 replayed examples diverge and 35 are already declared
known-stale. The two promised-deliverable transcripts are task-owned count
changes, so their exact expected count is updated from 21/15 to 23/17 and
replayed independently 2/2; no unrelated example is recaptured or blessed.

## Public cutover planning checkpoint CO-E through CO-G — Codex report

The selected mechanism remains source-level same-path promotion: a later
authorized execution would put the already accepted reader DOM/load graphs
behind `src/web/browser/liturgy/day.html` and
`src/web/browser/liturgy/index.html`, preserving canonical URLs and avoiding
redirect, rename, rewrite, or build-alias semantics. The exact mechanical
promotion is recorded—but not applied—in
`build/agent-continuity/liturgy-reader-public-cutover-proposed.patch`. Its
header prohibits applying the draft alone: route-neutral wording, Day deferred
reasoning/territorial behavior, stable public Propers option names, and direct
counterpart/context navigation require the review dispositions recorded in the
decision before the patch can be regenerated as an executable cutover diff.

Rollback is an ordinary revert of the bounded later cutover commit, followed
by an exact Pages deployment and canonical-route verification. The gate names
the local suites, actual-canonical-filename matrix, accepted production-reader
and Instrument oracles, metadata, static-hosting, mixed-cache, 600-second
second-pass, asset-parity, accessibility, and immediate rollback conditions.
Candidate routes and the visual oracle remain deployed and unmodified through
the acceptance window; their cleanup is deliberately postponed.

Planning validation records:

- focused non-publication Python: 142/142 pass;
- locked-publication Python: 82/82 pass with Markdown 3.10.2; the system Python
  run honestly errors in 8 publication tests because it has Markdown 3.10.3;
- Day browser 34/34, Propers 27/27, shared shell 18/18;
- governed Instrument 19/19, zero console/request/HTTP/accessibility/overflow
  failures, 0 captures because no visual or product byte changed;
- promised ledger 23 tracked/17 complete, tool registry 34, release bindings
  exact with 0 stale, locked public-alpha check/build/Pages-verify pass;
- governed `make check` exits 2 at 23 unrelated divergent and 35 known-stale
  stored examples; the two task-owned ledger examples replay 2/2 after exact
  count updates and no unrelated transcript is recaptured.

Canonical Day hash
`bc5a98de6b718431f3b91e6a133bb847c2dcdf4d21fce6f45aae3ad4984de868`
and canonical Propers hash
`f630f4a66f3f525144336f183b1485c698030c7531ff679375b3a7aa00150c65`
are byte-identical to the starting boundary. Public navigation, candidate
HTML/JavaScript, Instrument CSS, and oracle files are likewise unchanged.

## Message to the independent public-cutover-plan reviewer

Start with `CUTOVER-DECISION.md`, then compare `ROUTE-MAP.md` and
`STATE-COMPATIBILITY.md` to `PROPOSED-CUTOVER.patch`. The plan selects the
smallest same-path mechanism and makes the Day gate deterministic, but it does
not smuggle unresolved public-contract choices into “parity.” Please give an
exact disposition on: Roman-1962 versus legacy manifest-order empty-Day
default; preserved production treatment for `why=1` and territorial choice;
stable public `cycle`, `alternative`, and `translation-witness` keys;
source-static noindex and route-neutral metadata for retained candidates;
public titles and non-candidate diagnostics; and quiet direct Day↔Propers plus
context access. Also decide whether the draft patch must be regenerated with
all accepted dispositions before execution can be authorized (Codex recommends
yes).

No public-route, public-navigation, candidate, oracle, visual, renderer,
source, or coverage byte changed in this phase. Public navigation and public
cutover execution remain explicitly unauthorized. If the plan is accepted, a
separate clean execution agent must still apply only the reviewed final patch,
pass every named local/canonical/oracle/deployment/cache gate, and stop for
independent cutover acceptance before any cleanup.

## Independent public-cutover-plan review — reviewer to Codex

Disposition

PLAN DIRECTION ACCEPTED — COMPATIBILITY CLOSURE REQUIRED BEFORE CUTOVER EXECUTION

The same-path cutover architecture is accepted. The rollback model, canonical-route test matrix, static-hosting analysis, indexing plan, deterministic Day gate, and accepted visual-oracle strategy are sufficient.

Public cutover execution is not yet authorized.

The planning package correctly identifies public-contract differences that cannot be silently folded into “parity.” This review resolves those decisions and authorizes one bounded compatibility-closure phase on the accepted candidate/shared reader implementation only, followed by regeneration of the final executable cutover patch and a narrow independent re-review.

Do not modify canonical day.html or index.html in the compatibility-closure phase.

Do not change public navigation.

Do not remove or redirect candidate or oracle routes.

Reviewed package

Reviewed archive:

20260806T212148Z-liturgy-reader-instrument-public-cutover-plan.zip

Independent archive verification:

    ZIP integrity: pass

    top-level directories: exactly one

    MANIFEST.sha256: 48/48 entries pass

    ZIP SHA-256:
    3309d02ea32110b957111d4a893e081b28e5663e51f5669c9eb3ffef5e1f6889

    STATE-COMPATIBILITY.json: valid JSON

    PROPOSED-CUTOVER.patch: mechanically applies with
    git apply --check --unidiff-zero against the included exact source snapshots

The proposed patch remains non-executable by design. It must be regenerated after the dispositions below are implemented and evidenced.

Eight requested review dispositions

1. Same-path promotion behind day.html and index.html

PASS

Use source-level in-place promotion behind the unchanged canonical filenames:

    src/web/browser/liturgy/day.html

    src/web/browser/liturgy/index.html

Do not redirect to internal reader filenames. Do not rename candidates. Do not add a client router, build-only alias, or rewrite layer.

This is the smallest mechanism, preserves existing external paths and hash/query text, keeps relative data/assets stable, and gives the cleanest ordinary-revert rollback.

2. Existing Day and Propers URL/state contracts

CONDITIONAL PASS — dispositions below are binding

Valid core Day/Propers deep links, Bible/oration state, Read/Missal state, reload, Back/Forward, malformed-state fail-closed behavior, and canonical Browse behavior are adequately covered.

The following public-contract decisions are now resolved:

2A. Empty Day default

ACCEPT ROMAN 1962 AS THE PUBLIC EMPTY-DAY DEFAULT.

The accepted reader's repository-declared default is preferable to preserving accidental manifest ordering.

The eventual canonical empty Day route should therefore use:

    local civil date;

    repository-declared default missal, currently Roman 1962;

    existing declared/default Bible and language rules;

    Read mode.

Record this as an intentional public behavior change.

Do not preserve postconciliar merely because it is currently first in an index.

2B. why=1

PRESERVE THE EXISTING PUBLIC STATE. NARROWING IS REJECTED.

A valid public why=1 link must not become a recursive self-link and must not become a generic fail-closed message.

Implement a bounded compatibility path inside the accepted Instrument reader:

    keep the existing public why=1 spelling;

    use the existing production-derived reasoning/rubrical data;

    do not create a parallel reasoning engine;

    do not infer missing facts;

    when why=1, render the requested reasoning as subordinate apparatus associated with the affected Mass/Proper/branch;

    the apparatus must be actually visible/reachable on the page without sending the reader to another route;

    default why remains off.

Preferred presentation:

    native/subordinate details-style apparatus titled Why this Mass or the existing precise production heading;

    present it after the affected liturgical unit/branch rather than before the first prayer;

    when why=1 was explicitly supplied in the URL, the requested apparatus must not be silently omitted;

    do not reintroduce the old wall-of-boxes composition.

This compatibility content may use existing legacy reasoning classes/data or bounded route CSS. Do not alter reader-instrument.css merely to accommodate it unless a concrete visual conflict is proved.

2C. Multiple territorial branches

PRESERVE THE EXISTING PRODUCTION OUTCOMES. NARROWING IS REJECTED.

Do not invent a locality, choose by array order, choose by geography, or add an unreviewed public locality key merely for cutover.

For a date whose production assembly contains more than one territorial branch:

    render every held production branch;

    give each branch a clear territorial heading using its existing source identity/label;

    do not imply that one branch is selected;

    preserve the existing branch-specific winner/readable/formulary result;

    preserve source/rubrical reasoning when why=1;

    preserve exact source ownership and fail closed only if a branch itself cannot be faithfully adapted.

This matches the current canonical reader's core semantic behavior—showing all held branches—without retaining the rejected old visual composition.

The accepted Instrument remains the shell. A rare multi-branch state may be longer, but it must remain readable and explicit.

2D. Propers cycle/alternative/translation-witness keys

ACCEPT STABLE PUBLIC KEYS:

cycle
alternative
translation-witness

Canonical public routes may parse and write these exact additive names.

Rules:

    canonical routes must never emit _candidate-*;

    unknown keys remain inert/fail safely according to the accepted state contract;

    retained candidate routes may continue to accept legacy _candidate-cycle,
    _candidate-alternative, and _candidate-translation-witness during the
    initial acceptance window solely for old candidate evidence/deep links;

    newly generated candidate state should prefer the stable public names after
    the compatibility change, unless doing so would invalidate an accepted
    candidate fixture—in that case accept both but document the exact direction;

    add exact parse/serialize/reload/Back-Forward browser fixtures for all three
    stable names;

    do not change renderer ownership.

reader-state.js may be changed only as required to establish these stable state names.

3. Proposed diff limited to cutover

PASS AS A DRAFT; FAIL AS AN EXECUTABLE PATCH

The current PROPOSED-CUTOVER.patch is correctly bounded and correctly labels itself non-executable.

After compatibility closure, regenerate the patch from the then-current candidate/shared implementation.

The final proposed execution patch must include only the exact accepted cutover/runtime/metadata/test/release/tracking paths.

Do not carry the current draft forward as the executable patch.

4. Relative paths, indexing, caching, GitHub Pages, and mixed-cache behavior

PASS

The plan correctly identifies same-directory relative-path stability, static Pages publication, the absence of a service-worker/rewrite layer, unversioned asset caching, and the need to verify both cache-bypassed and post-freshness-window behavior.

Retained candidate indexing

APPROVED.

Both retained candidate source pages must carry the repository's full static non-indexing directive:

<meta name="robots" content="noindex, nofollow, noarchive, nosnippet, noimageindex">

Do not rely on JavaScript to alter robots metadata after publication.

Candidate/oracle routes must not advertise themselves with canonical/Open Graph metadata as the public entrance.

Canonical day.html and index.html remain indexable.

Canonical metadata

APPROVED WITH ROUTE-NEUTRAL WORDING.

Remove all user-visible internal and candidate wording when the shared reader controllers run on canonical routes.

Use route/product titles such as:

Day — Triptych
Propers — Triptych

and dynamic forms in substance:

<celebration> — Day — Triptych
<formulary> — Propers — Triptych
Selection unavailable — Day — Triptych
Selection unavailable — Propers — Triptych

Exact punctuation may follow the project's existing metadata convention, but no canonical title, visible diagnostic, failure explanation, mode description, or status line may call the public reader a candidate/internal prototype.

Debug/test object names need not be renamed solely for cosmetics if they are not user-visible and remain useful to the accepted harness.

5. Rollback

PASS

Ordinary git revert of the bounded cutover commit/series is the correct mechanism.

Keep:

    candidates;

    visual oracle;

    legacy controllers;

    legacy styles;

    data;

    compatibility tests

through the initial acceptance window.

The rollback plan's exact-SHA Pages requirement and cache-bypassed plus post-window verification are required.

If compatibility closure is committed separately before cutover, a cutover rollback does not need to revert that candidate-only compatibility commit unless it independently causes a problem. Reverting the canonical promotion must restore the old public routes immediately.

6. Local, visual, accessibility, publication, deployment, and post-cache gates

PASS

The named gates are sufficient, with the additional compatibility evidence below.

Continue to require:

    Day 34/34;

    Propers all green;

    shared shell all green;

    governed Instrument all green;

    focused Python all green;

    exact release bindings;

    locked public-alpha check/build/verify;

    actual canonical-filename browser matrix;

    accepted production-reader candidate as the immediate parity oracle;

    Instrument visual oracle for composition;

    exact intended Pages SHA;

    cache-bypass verification;

    second verification after the observed freshness window;

    ordinary rollback on mixed-cache incompatibility.

The unrelated stored example-transcript divergence remains an honest qualification and must not be recaptured/blessed.

7. Deterministic Day first-visit test

PASS

The test-only clock fixture is acceptable.

It:

    keeps the URL empty;

    freezes only the browser test clock;

    exercises actual default-date behavior;

    asserts the exact committed civil date;

    does not alter product behavior;

    restores the fixture afterward.

Retain the 34/34 result as a cutover precondition.

8. Exact enough for a later clean execution agent

NOT YET

The architecture is exact enough. The public-contract decisions are now exact enough. The executable bytes are not yet exact enough because the required compatibility behavior does not exist and the draft patch intentionally omits it.

Therefore:

Do not authorize or execute canonical promotion yet.

First complete the bounded compatibility-closure work below, seal it, and return for narrow independent re-review.

Navigation disposition

Day ↔ Propers counterpart access

PRESERVE IT, BUT DO NOT ADD A FIFTH PRIMARY SHELL ACTION.

Use the existing Details surface.

Add a small route-neutral navigation section near the end of Details:

On Day

First related-reader link:

Browse the Propers

→ index.html with no fabricated state.

On Propers

First related-reader link:

Open the Day reader

→ day.html with no fabricated date/state unless an already-held meaningful state mapping exists and is explicitly tested.

This is a direct route link; it does not detour through Home.

The fact that it requires opening Details is an accepted intentional difference from the legacy bottom footer. It preserves the four primary actions and keeps the first reading viewport clean.

Context links

Place the longer current contextual destinations in the same Details surface under a restrained heading such as:

Elsewhere in Triptych

Preserve the existing legitimate local destinations from the current canonical footers:

    Law where currently offered;

    Texts;

    Scripture where currently offered;

    History/Sources where currently offered.

Do not restore the generic site footer or add a dashboard/navigation bar.

Capture the Details surface at desktop and mobile after this addition.

Compatibility-closure work order

CC-A — Update continuity first

Append this review verbatim under:

## Independent public-cutover-plan review — reviewer to Codex

in:

build/agent-continuity/liturgy-reader-visual-plan.md

Immediately append:

## Public-cutover compatibility closure — Codex response

Codex's response must state:

    all eight review dispositions;

    acceptance of Roman 1962 as the public empty-Day default;

    preservation—not narrowing—of why=1;

    preservation of all held territorial branches;

    adoption of the three stable Propers public keys;

    static noindex for retained candidates;

    route-neutral canonical wording;

    Details-based counterpart/context navigation;

    confirmation that canonical Day/Propers HTML remains untouched during compatibility closure;

    the exact files proposed for compatibility changes.

CC-B — Implement candidate/shared compatibility only

Authorized product paths are limited to those actually needed from:

src/web/browser/liturgy/day-reader.js
src/web/browser/liturgy/day-reader.css
src/web/browser/liturgy/day-reader.html
src/web/browser/liturgy/propers-reader.js
src/web/browser/liturgy/propers-reader.css
src/web/browser/liturgy/propers-reader.html
src/web/browser/liturgy/reader-state.js

and narrowly necessary task-owned tests.

reader-instrument.css, reader-shell.js, adapters, assembly, Ordinary seating, source data, translations, and oracle files remain frozen unless a concrete incompatibility is proved before changing them.

Canonical:

src/web/browser/liturgy/day.html
src/web/browser/liturgy/index.html

must remain byte-identical throughout CC-B.

Required compatibility outcomes

    why=1 renders production-derived reasoning in the accepted shell with no self-link.

    multi-territorial dates expose every held branch without inference.

    stable cycle, alternative, translation-witness state round-trips.

    retained candidates are source-static noindex/noarchive.

    user-visible controller wording is route-neutral.

    Details includes direct counterpart and existing contextual links.

    default candidate behavior outside these explicit states remains visually identical to the accepted production integration.

CC-C — Evidence

Add governing evidence for:

Day reasoning

At least one real held why=1 state:

    1440×900 Read;

    393×852 Read;

    if why=1 materially interacts with Missal, 1440×900 Missal too.

Prove:

    requested reasoning is visible/reachable;

    first principal text remains appropriately dominant;

    no wall-of-boxes regression;

    exact source/rubrical loci remain present;

    URL retains why=1;

    reload and Back/Forward preserve the state.

Territorial state

Use a real repository fixture whose assembly has more than one territorial branch.

Capture:

    1440×900;

    393×852.

Prove:

    every held branch appears;

    labels are unambiguous;

    no branch is silently preferred;

    no geography is inferred;

    no recursive link exists;

    browser/reload behavior is stable;

    no content is fabricated.

Propers public option state

For each:

cycle
alternative
translation-witness

prove:

    parse;

    validation;

    serialization;

    direct load;

    reload;

    Back/Forward;

    invalid explicit value fail-closed behavior.

Prove canonical-form serialization never emits _candidate-*.

Details/navigation

Capture Day and Propers Details at:

    1440×900;

    393×852.

Prove counterpart and contextual links are readable, restrained, keyboard reachable, and do not alter the closed-shell composition.

Indexing/metadata

Build the public artifact and prove retained candidate HTML contains the static noindex directive before JavaScript runs.

Prove route-neutral runtime strings contain no user-visible candidate/internal language.

CC-D — Validation

Rerun at minimum:

    focused Python suites covering Day, Propers, state, shell, visual reset, public alpha;

    Day browser: 34/34;

    Propers browser: all green;

    shared-shell browser: all green;

    governed Instrument visual assertions: all green;

    syntax checks for every changed JS/test file;

    release binding checks;

    locked public-alpha check/build/verify;

    git diff --check;

    exact canonical Day/Propers source hash comparison against this planning package.

Do not call the unrelated full repository gate green if stored examples still diverge.

CC-E — Regenerate the final proposed cutover patch

After compatibility closure is committed and pushed, regenerate:

build/agent-continuity/liturgy-reader-public-cutover-proposed.patch

The regenerated patch must be based on the compatibility-closed candidate/shared bytes and must no longer contain a warning that unresolved decisions remain.

It still must not be applied to canonical routes yet.

The regenerated patch must show exactly the later execution change set, including:

    canonical HTML promotion;

    any already-reviewed route metadata changes that truly belong in cutover;

    release-binding/publication changes expected at execution;

    canonical-ownership test adjustments expected at execution.

Do not duplicate compatibility changes in the cutover patch if they were already committed separately.

Run git apply --check --unidiff-zero against a clean copy of the exact execution baseline.

Required narrow handoff

Create and push:

build/agent-handoffs/<UTC>-liturgy-reader-public-cutover-compatibility/
build/agent-handoffs/<UTC>-liturgy-reader-public-cutover-compatibility.zip

The maintainer's continuity requirement authorizes force-adding only this exact new compatibility handoff directory and matching ZIP if ignored.

Include:

    this review;

    updated continuity snapshot;

    Codex response;

    changed-files list;

    exact compatibility diff;

    regenerated proposed cutover patch;

    Day why=1 evidence;

    territorial evidence;

    Propers stable-key evidence;

    Details/navigation evidence;

    indexing/metadata evidence;

    browser results;

    measurements;

    validation logs;

    source hashes proving canonical day.html/index.html unchanged;

    MANIFEST.sha256.

Generate the manifest last, create the ZIP, verify integrity, one top-level directory, manifest, and ZIP SHA-256, then commit/push all durable artifacts.

Narrow re-review questions

Return for independent review answering only:

    Does why=1 preserve the existing public behavior without reintroducing the old visual wall?

    Are multiple territorial branches faithfully exposed without inference or silent preference?

    Do cycle, alternative, and translation-witness form a stable, tested public Propers contract?

    Are retained candidates statically noindex and all shared user-visible strings route-neutral?

    Is Details-based Day↔Propers/context navigation visually subordinate and usable?

    Are canonical day.html and index.html still byte-unchanged?

    Is the regenerated cutover patch complete, mechanically applicable, and free of unresolved public-contract choices?

    If all seven pass, is public-cutover execution safe to authorize as a separate phase?

Authorization boundary

    Same-path cutover mechanism: accepted

    Public-cutover planning architecture: accepted

    Roman 1962 empty-Day default: accepted

    Stable Propers public keys: accepted

    Static candidate noindex/noarchive: accepted

    Route-neutral canonical wording: accepted

    Details-based counterpart/context access: accepted

    Narrowing/removing why=1: rejected

    Narrowing/removing territorial outcomes: rejected

    Compatibility-closure implementation on candidate/shared reader: authorized

    Canonical day.html or index.html modification: unauthorized

    Public navigation modification: unauthorized

    Public-cutover execution: unauthorized pending compatibility re-review

    Candidate/oracle cleanup: unauthorized

## Public-cutover compatibility closure — Codex response

All eight review dispositions are accepted as binding. Same-path promotion is
the accepted architecture; core URL/state compatibility remains conditionally
accepted; the current patch remains a draft; static-hosting/indexing, rollback,
local/oracle/deployment gates, and the deterministic Day fixture pass; and the
plan is not yet executable until compatibility closure and narrow re-review.

Roman 1962 is accepted as the intentional repository-declared public empty-Day
default. `why=1` will be preserved, not narrowed: the accepted reader will use
production-derived reasoning and expose it as subordinate, reachable apparatus
without a self-link or parallel reasoning engine. Every held territorial branch
will be rendered with its production identity and branch result, without
geographic inference, array-order preference, or a new locality key. Propers
will parse and emit stable `cycle`, `alternative`, and `translation-witness`
keys while accepting legacy `_candidate-*` aliases only for retained candidate
deep links during the initial window.

Retained candidate HTML will carry the full static noindex/noarchive directive.
User-visible titles, diagnostics, status, failure, and mode text will be
route-neutral. The existing Details surfaces will gain subordinate direct
Day↔Propers counterpart links and the legitimate current contextual links,
without adding a fifth shell action or restoring generic chrome.

CC-B proposes changes only to:

- `src/web/browser/liturgy/day-reader.js`
- `src/web/browser/liturgy/day-reader.css`
- `src/web/browser/liturgy/day-reader.html`
- `src/web/browser/liturgy/propers-reader.js`
- `src/web/browser/liturgy/propers-reader.css` only if Details or option-state
  evidence proves a local layout need
- `src/web/browser/liturgy/propers-reader.html`
- `src/web/browser/liturgy/reader-state.js` only if the stable public names
  cannot remain controller-owned
- narrowly necessary Day, Propers, state, visual, shell, and publication tests
  and browser harnesses.

`reader-instrument.css`, `reader-shell.js`, adapters, assembly, Ordinary
seating, sources, translations, data, and oracle files remain frozen unless a
specific incompatibility is first proved and appended. Canonical
`src/web/browser/liturgy/day.html` and `src/web/browser/liturgy/index.html`
remain byte-identical throughout compatibility closure, as does repository-owned
public navigation. Public cutover execution, canonical promotion, candidate or
oracle cleanup, and public navigation changes remain unauthorized.

### Compatibility-closure implementation checkpoint — pre-commit

The bounded implementation now exists only in the retained production-reader
candidates and the shared URL contract. The canonical public route sources have
not changed: `src/web/browser/liturgy/day.html` remains SHA-256
`bc5a98de6b718431f3b91e6a133bb847c2dcdf4d21fce6f45aae3ad4984de868`
and `src/web/browser/liturgy/index.html` remains SHA-256
`f630f4a66f3f525144336f183b1485c698030c7531ff679375b3a7aa00150c65`.

Implemented compatibility outcomes:

- Day preserves `why=1` as collapsed, subordinate “Why this Mass” apparatus
  built from the existing production assembly branch and rubrical records. It
  appears after the affected branch, preserves source loci, and contains no
  route/self-link or parallel reasoning inference.
- Day renders every held territorial branch under its source identity and
  branch winner. Branch DOM and semantic locations are namespaced without
  adding a public territory key or selecting a geography. Read↔Missal and
  Back↔Forward regression coverage owns the namespaced restoration seam.
- Propers accepts and canonically writes `cycle`, `alternative`, and
  `translation-witness`; retained `_candidate-*` spellings are input-only.
  Held cycles and translation witnesses round-trip. Because production exposes
  no stable generated alternative identity, an explicit `alternative` remains
  preserved in the URL and fails closed rather than fabricating a selection;
  its direct-load, reload, and history lifecycle is tested.
- Both retained candidate HTML sources carry the exact static
  `noindex, nofollow, noarchive, nosnippet, noimageindex` directive. Visible
  titles, failures, modes, and status copy are route-neutral.
- Details keeps Selection and resolved information first, then presents the
  direct counterpart as the first link in a near-end Related reader section,
  followed by the restrained existing contextual destinations. The four
  primary shell actions are unchanged.

The accepted `reader-instrument.css`, shared shell, adapters, assembly,
Ordinary seating, data, translations, and visual oracle are unchanged. Release
bindings were refreshed only for the candidate/shared assets changed here.

Local validation so far records 148/148 focused Python tests, Day browser
37/37 before the added territorial restoration assertion, Propers browser 29/29
before the added complete public-key lifecycle assertions, shared shell 18/18,
and governed visual reset 24/24 across 108 captures. The corrected visual run
opens and scrolls the requested Why apparatus into the 1440 and 393 screenshots;
full-size inspection found readable source loci, dominant liturgical text, and
no wall-of-boxes regression. Final browser totals and immutable evidence paths
will be appended after the post-edit reruns finish. No success is yet claimed
for a compatibility commit, push, Pages run, regenerated cutover patch, or
handoff.

### Compatibility-closure implementation checkpoint — final local validation

This entry supersedes only the preliminary totals in the preceding pre-commit
checkpoint; it does not delete that chronology. The final source-bound preview
uses Day JavaScript SHA-256
`c6aa7842d12613419cef5a3b28d527472dafa573b62276b352ed036c0685efa2`
and Propers JavaScript SHA-256
`51cc1286f6baf61c20501a8a2b59a3dcf41720b7715e28ac978b97f4111ddf51`.
The source and rebuilt preview copies match byte for byte.

Two audit corrections were made before this checkpoint. First, Details opened
while a territorial Day result or Propers structure was still loading now
updates the same open surface only after the winning outcome commits, without
focus loss or stale cached selection text. Second, the real 15 January 2026
Roman commemoration fixture has no held relative oration seat: its apparatus
now uses neutral “Second oration” wording, makes no `What follows …` claim,
and still retains the held Latin incipit `Intercessio nos, quaesumus`. This is
the fail-closed/source-honest result; no seat or text was fabricated.

Final local commands and dispositions at this boundary:

- Focused Python: 148/148 pass.
- Day Chromium: 40/40 pass, including deterministic empty visit, ordinary and
  transferred `why=1`, no-slot Latin preservation, selected postconciliar
  Ordinary notes, every held territorial branch, territorial `why=1`, reload,
  Back/Forward, modal/focus, race ownership, and static privacy.
- Propers Chromium: 32/32 pass, including stable public-key direct load,
  validation, serialization, reload, Back/Forward, legacy input-only aliases,
  and early-open Details refresh.
- Shared shell Chromium: 18/18 pass.
- Governed visual assertions: 24/24 pass over 112 current-source captures; no
  console, failed-request, HTTP, required-overflow, or unnamed-control failure.
- `tools/tpt check-promised-deliverables`: pass, 23 tracked / 17 complete.
- `tools/tpt --check`: pass, 34 tools.
- `make check-release-bindings`: pass, zero stale bindings.
- Locked public-alpha policy, build, preview build, preview verify, and
  GitHub-Pages-target verify: pass.
- `git diff --check` and all changed JavaScript/harness syntax checks: pass.

Final evidence is rooted at
`/tmp/triptych-compatibility-sealed.IBk9wT/` until copied into the immutable
handoff. Its compatibility subset contains 12 original-pixel states: ordinary
Day Why desktop/mobile, territorial branches desktop/mobile, Day Details
desktop/mobile plus the scrolled mobile links, Propers Details desktop/mobile,
the rare no-slot Why mobile state, postconciliar Missal Why desktop, and
territorial Why desktop.

Blocker-by-blocker full-size self-review:

- `why=1`: the liturgical document remains primary; one native disclosure
  follows each affected branch. Expanded apparatus is linear, source-labeled,
  and unboxed. It retains Latin, exact rubrical loci, transfers, Proper seating,
  and only the selected Ordinary variant note. No self-link or old wall of
  cards appears.
- Territorial outcomes: both real Epiphany branches are plainly headed and
  fully separated; no branch is styled as selected and no location is inferred.
  The longer state remains one readable Instrument document at 1440 and 393.
- Details/navigation: counterpart and contextual links are subordinate to
  selection/result details, keyboard-accessible, and readable on desktop and
  mobile. The additional scrolled mobile capture proves the Day links rather
  than relying on offscreen inference.
- Stable Propers state and retained routes: visible copy is route-neutral and
  retained candidate HTML is statically noindex/noarchive before JavaScript.
- Accepted composition: the masthead, reading measure, ritual grid, rail/dock,
  warnings, first-principal-text timing, and normal mobile rhythm remain
  unchanged. `reader-instrument.css` and the visual oracle are byte-frozen.

Canonical source hashes remain exactly
`bc5a98de6b718431f3b91e6a133bb847c2dcdf4d21fce6f45aae3ad4984de868`
for `src/web/browser/liturgy/day.html` and
`f630f4a66f3f525144336f183b1485c698030c7531ff679375b3a7aa00150c65`
for `src/web/browser/liturgy/index.html`. Public navigation and cutover have not
been modified or authorized. The next exact action is the coherent
compatibility checkpoint commit and push, followed by Pages/deployed-candidate
parity verification; only then will the execution patch and handoff be sealed.

The governed `make check` was also rerun to its terminal result. It exited 2 at
`Makefile:725: check-examples` after replaying 188 of 200 captured examples:
21 diverged, 35 are recorded known-stale, 6 were never run, and 6 are unrunnable
in this checkout. The divergence spans unrelated calendar, citation, commentary,
source-library, research-staleness, and tool transcript records; the exact
output still identifies `tools/public-alpha prepare` and release-status examples
as stale transcripts even though the task-owned policy/build/binding gates above
pass. No example was recaptured or blessed, and the full repository gate is not
represented as green.

### Compatibility implementation deployment and evidence-hardening checkpoint

Compatibility implementation commit
`3f3949617a04ffa68a1070058d0f7bc5ac74dc93` was pushed to `origin/main`.
GitHub Pages run `31148986910` completed successfully for that exact commit.
The older planning-only run `31128301816` for `5e1b82b51` had remained in a
waiting state since the prior day and blocked the current workflow; it was
cancelled without changing repository or deployment bytes. Direct verification
after the successful run returned HTTP 200 for both retained readers, their
changed controllers/styles, `reader-state.js`, and both still-legacy canonical
routes. Deployed candidate HTML byte-matches the locked public-alpha build;
changed JavaScript and CSS byte-match source. Retained candidates carry the
full static noindex directive, while canonical Day and Propers remain indexable.

An evidence audit then required literal full-document reload assertions for
ordinary and territorial `why=1`, not only Back/Forward coverage. The first
attempt correctly failed because assigning the current URL to `location.href`
does not guarantee a reload. The harness now invokes `Page.reload`, waits for a
new document token and the winning committed render, and proves the same URL and
apparatus after reload. Day passes 40/40 with these stronger assertions. The
governed visual harness passes 24/24 over 113 captures and adds
`compatibility/13-day-territorial-second-branch-393x852.png`, a full-size mobile
view deliberately scrolled to the second held branch. Inspection confirms its
territorial heading, identity, held Proper text, and edge dock are readable;
the branch is not inferred from a count or hidden below the evidence crop.

The eight-suite focused Python command passes 230/230 under the repository's
locked environment. Running the same command first with the ambient interpreter
produced 8 errors because installed Python Markdown was 3.10.3 while the release
lock requires 3.10.2; all 8 errors were dependency-lock refusals inside
`test_public_alpha`, not assertion failures. Repeating unchanged tests with
`build/visual-reset-venv/bin/python` (Markdown 3.10.2) passed 230/230. This
environment qualification is retained rather than calling the ambient run
green. Promised-deliverable validation (23 tracked / 17 complete), the 34-tool
registry, release bindings, JSON parsing, JavaScript syntax, and diff whitespace
checks also pass.

This hardening changes only the Day and visual browser harnesses plus planning
records. It changes no product, canonical route, public navigation, release,
oracle, or accepted presentation byte. The next exact action is a coherent
evidence-baseline commit/push, followed by regeneration of the normal-context
cutover patch. That patch will promote the compatibility-closed candidate load
graphs behind the unchanged canonical filenames, omit retained-candidate robots
metadata, use source titles `Day` and `Propers` so the static builder produces
the established ` · Triptych` suffix exactly once, and include only the
execution-owned release, test, and tracking changes. It will remain unapplied
until narrow independent review authorizes a separate execution phase.

### Regenerated cutover patch and narrow-review stopping point

Evidence-hardening commit
`998648c341691c0807b0c209f93fbae16d641d48` was pushed and its automatic
GitHub Pages run `31150296458` completed successfully. That commit changes no
product or public route byte. It is the exact execution baseline for the newly
regenerated patch.

`build/agent-continuity/liturgy-reader-public-cutover-proposed.patch` is now a
normal-context, unapplied patch with SHA-256
`cd11518ba7b20d198cbd16d08cc153d3f3053afeba8a230441c57312318a7566`.
`git apply --check` passes without `--unidiff-zero` against exact execution
baseline `e62a226fc661100a2427a4193213c7dadcf24225`, which owns the final
plan/tracking content immediately before the sealed handoff. The patch
contains exactly 17 files: canonical `day.html` and `index.html`; the public
manifest and rights record; seven focused Python owners; three Chromium
harnesses; and the three required tracking records. It contains no hunk for a
retained candidate, controller, shared state, stylesheet, shell, renderer,
adapter, data/source file, public-navigation entry, or visual oracle.

The proposed canonical source titles are `Day` and `Propers`, which the static
builder will suffix once as ` · Triptych`; descriptions are route-neutral and
robots metadata is intentionally omitted so canonical output remains indexable.
Prospective source hashes are
`9a119a6aa87e900d6fc4c3e236191fe8a036abc305236eb576c09f823c7b7972`
for Day and
`a6527316266365b79ff2ecdc193da3ab1034b1daa63408b869b192d2aeb85600`
for Propers. The prospective rights-record digest is
`5a4b4d4f8bfbcf8d5fd54249c0d8664be7215b4bee9e82ccc8a37f400e3cf31e`.
The existing `/liturgy/` GitHub Pages alias remains accepted for the same
Propers document; cutover does not expand into build-pipeline canonical-link
logic.

No canonical patch has been applied. Canonical source hashes at this stopping
point remain `bc5a98de…` and `f630f4a6…`; public navigation is unchanged; both
retained candidates and both visual-oracle routes remain present and noindex.
The next reviewer is asked to answer only the seven review questions in the
compatibility handoff. Even a favorable answer authorizes only a later,
separate cutover execution phase. It does not itself modify navigation, remove
fallback routes, or accept a deployed cutover.

### Message to the next independent reviewer

Begin with the ordinary and territorial Why screenshots, then inspect the
mobile second-branch state and both Day/Propers Details pairs. The visible
change is deliberately rare-state compatibility inside the already accepted
Instrument: source-owned reasoning is subordinate, all held branches remain
explicit, and related/context navigation stays inside Details. Stable Propers
state and static candidate privacy are primarily browser/source-contract
questions rather than a new visual direction.

What remains provisional is only authorization to promote the already accepted
implementation behind `day.html` and `index.html`. Please decide the seven
questions in `REVIEW_REQUEST.md`, especially whether the normal-context future
patch is complete and contains no unresolved contract choice. Do not treat a
pass as deployed cutover acceptance: public navigation, canonical execution,
and candidate/oracle cleanup remain separate and unauthorized at this boundary.

## Independent compatibility-closure acceptance — reviewer to Codex

Liturgical Instrument — Compatibility Closure Acceptance and Public-Cutover Execution Authorization

Disposition

ALL SEVEN COMPATIBILITY QUESTIONS PASS.

The bounded compatibility closure is accepted.

Public-cutover execution is now authorized as a separate, tightly bounded phase.

This is not final acceptance of the live public cutover. The execution agent may promote the accepted compatibility-closed readers onto the canonical filenames, deploy them, run the exact local/deployed/cache-window gates, and seal the resulting evidence. It must then stop for independent post-deployment cutover acceptance.

Public navigation redesign remains unauthorized.

Candidate/oracle cleanup remains unauthorized.

Do not reopen visual design, state ownership, renderer ownership, source/translation scope, Ordinary seating, or the accepted compatibility decisions.

Reviewed package

Reviewed archive:

20260807T052836Z-liturgy-reader-public-cutover-compatibility.zip

Independent verification:

    ZIP integrity: PASS

    top-level directories: exactly one

    MANIFEST.sha256: 61/61 payload entries PASS

    uploaded ZIP SHA-256:

2222dada68a66a98a9fc029b8d7c0550d7d4de3c36634f19bbec1e24d150b31c

    regenerated cutover patch SHA-256:

cd11518ba7b20d198cbd16d08cc153d3f3053afeba8a230441c57312318a7566

Reviewed compatibility implementation:

3f3949617a04ffa68a1070058d0f7bc5ac74dc93

Reviewed evidence hardening:

998648c341691c0807b0c209f93fbae16d641d48

Exact cutover-patch execution baseline:

e62a226fc661100a2427a4193213c7dadcf24225

Sealed compatibility handoff on main:

e69d91f

Successful compatibility Pages runs:

31148986910
31150296458

The unrelated governed example-transcript gate remains honestly non-green. It is not a cutover-owned failure and must not be recaptured or blessed.

Seven requested dispositions

1. why=1

PASS

why=1 now preserves the public reasoning capability without restoring the rejected legacy visual wall.

The accepted reader:

    keeps the exact public why=1 URL spelling;

    derives the apparatus from the production assembly/rubrical result already owned by the application;

    creates no parallel reasoning engine;

    creates no recursive link back to day.html;

    exposes a native subordinate Why this Mass disclosure after the affected liturgical content;

    preserves exact rubrical/source loci;

    includes rejected/omitted observances and their reasons where production data supplies them;

    preserves Ordinary-placement reasoning and source honesty;

    supports Roman, postconciliar, territorial, and missing-seat cases;

    preserves the URL and apparatus across reload and browser history.

The disclosure remains collapsed by default. That is accepted. The direct why=1 state visibly exposes the Why this Mass apparatus as an intentional part of the page; opening it reveals the requested source-owned reasoning in place. This satisfies the prior requirement that the reasoning be visible/reachable without making it dominate the first reading viewport.

The 1440 and mobile evidence is visually successful: the reasoning is linear, typographic, and subordinate rather than a second dashboard.

No further why=1 design work is requested before cutover.

2. Multiple territorial branches

PASS

The reader faithfully exposes all held source-defined territorial outcomes without inventing locality or silently selecting one.

The reviewed implementation/evidence proves:

    multiple held branches remain present simultaneously;

    each branch has a clear territorial identity;

    no territory query parameter is invented;

    no geographic lookup or user-locality inference is performed;

    no array-order winner is silently promoted as universal;

    semantic locations are namespaced per territorial branch;

    each branch retains its own production winner/formulary result;

    why=1 can explain each branch independently;

    if an individual branch cannot be faithfully seated/rendered in a mode, that branch fails closed with an explicit no-substitution message rather than poisoning or replacing the other held branch.

The Epiphany evidence is especially important: the second held branch is visibly present as Epiphany transferred to Sunday, not merely asserted by a test fixture.

No territorial compatibility blocker remains.

3. Stable Propers public keys

PASS

These exact names are accepted as the canonical public contract:

cycle
alternative
translation-witness

The implementation and browser evidence cover their parsing, validation, serialization, direct loading, reload, and Back/Forward lifecycle.

Canonical-form state does not emit:

_candidate-cycle
_candidate-alternative
_candidate-translation-witness

The retained candidate accepts those legacy aliases during the initial compatibility window, which is the correct backward-compatible boundary.

Where the current corpus does not provide a stable selectable alternative identity, explicit alternative state fails closed rather than fabricating a choice. That is accepted as the honest behavior of the stable key, not a defect in the contract.

Renderer ownership is unchanged.

4. Candidate indexing and route-neutral wording

PASS

Both retained candidate source pages statically contain:

<meta name="robots" content="noindex, nofollow, noarchive, nosnippet, noimageindex">

This is present in HTML before JavaScript runs.

The retained candidates do not become the indexed canonical entrance.

User-visible titles, diagnostics, limitation/failure copy, state descriptions, and shell copy are route-neutral. Internal class names, debug keys, function names, and error-code identifiers may still contain terms such as candidate; they are implementation/debug vocabulary, not public product copy, and were explicitly permitted by the prior review.

No indexing/metadata blocker remains.

5. Details-based reader/context navigation

PASS

The accepted four-action shell remains intact.

Day Details now provides the subordinate direct related-reader action:

Browse the Propers

Propers Details provides:

Open the Day reader

The longer legitimate Triptych destinations remain grouped beneath restrained contextual navigation rather than returning as permanent page chrome.

The reviewed desktop/mobile Details evidence is visually subordinate, readable, and keyboard-compatible. It does not pollute the first reading viewport or create a fifth primary shell action.

This intentional difference from the old footer is accepted.

6. Canonical pages remained byte-unchanged during closure

PASS — INDEPENDENTLY CROSS-CHECKED AGAINST THE PRIOR PLANNING PACKAGE

The compatibility package records:

src/web/browser/liturgy/day.html
bc5a98de6b718431f3b91e6a133bb847c2dcdf4d21fce6f45aae3ad4984de868

src/web/browser/liturgy/index.html
f630f4a66f3f525144336f183b1485c698030c7531ff679375b3a7aa00150c65

I independently hashed the canonical snapshots in the previous
20260806T212148Z-liturgy-reader-instrument-public-cutover-plan package and
obtained the same two hashes.

Therefore CC-B/CC-C did not modify the public canonical entry points.

This is the last phase in which those hashes are expected to remain unchanged:
the separately authorized execution below intentionally changes those two files.

7. Regenerated cutover patch

PASS

The sealed patch is now complete enough to execute.

Patch:

build/agent-continuity/liturgy-reader-public-cutover-proposed.patch

SHA-256:

cd11518ba7b20d198cbd16d08cc153d3f3053afeba8a230441c57312318a7566

Declared exact execution baseline:

e62a226fc661100a2427a4193213c7dadcf24225

It contains exactly 17 paths:

PROJECT-WORK.md
guidance/liturgy-browser-roadmap.md
promised-deliverables.toml
release/public-alpha.json
release/rights/public-alpha-2026-07-15.md
src/web/browser/liturgy/day.html
src/web/browser/liturgy/index.html
tools/tests/day_reader_integration_browser.mjs
tools/tests/liturgy_reader_visual_reset_browser.mjs
tools/tests/propers_reader_integration_browser.mjs
tools/tests/test_day_missal_integration.py
tools/tests/test_day_reader_integration.py
tools/tests/test_liturgy_reader_shell.py
tools/tests/test_liturgy_reader_visual_reset.py
tools/tests/test_mass_ordinary.py
tools/tests/test_propers_reader_integration.py
tools/tests/test_public_alpha.py

The patch:

    promotes the compatibility-closed readers behind the unchanged canonical filenames;

    uses no redirect;

    does not alter public navigation;

    does not alter candidate routes;

    does not alter the oracle;

    does not alter candidate/shared compatibility implementation;

    updates exact publication/rights hashes;

    moves governed browser/test ownership onto the actual canonical routes;

    updates truthful phase tracking;

    contains no unresolved why, territorial, state-key, indexing, or navigation decision.

The handoff records a successful normal-context git apply --check.

Execution-baseline safeguard

The execution agent must not blindly apply or hand-merge this patch merely because it was accepted.

Current main contains the later sealed-handoff commit, so before applying:

    verify the clean starting commit and remote agreement;

    verify e62a226fc661100a2427a4193213c7dadcf24225 is an ancestor;

    verify the patch remains exactly the accepted SHA-256 above;

    run git apply --check against the actual current worktree;

    verify no patch-owned target has materially drifted from the accepted context.

If any of those checks fail, stop for review. Do not use git apply --3way, fuzzy manual reconstruction, or a regenerated patch without separate approval.

If they pass, apply the exact accepted patch.

Compatibility validation disposition

The reviewed package records:

    focused locked Python: 230/230

    Day Chromium: 40/40

    Propers Chromium: 32/32

    shared shell Chromium: 18/18

    governed Instrument visual assertions: 24/24 over 113 captures

    changed-JS/browser syntax checks: PASS

    promised-deliverables registry: PASS

    tool registry: PASS

    release bindings: 0 stale

    locked public-alpha check/build/verify: PASS

    patch applicability: PASS

    required console/request/HTTP/control/ID/overflow assertions: PASS

The ambient Python run's Markdown-version mismatch is not a product failure; the project-locked environment is the governing environment.

The governed full repository check still stops at unrelated stored example transcript divergence. Continue to disclose it exactly.

Deployment disposition

The compatibility implementation and evidence checkpoints both have successful GitHub Pages deployments.

That proves the compatibility-closed candidate assets can deploy, but it does not qualify the future canonical cutover SHA.

The execution phase must obtain its own successful Pages result for the exact public-cutover commit.

PUBLIC-CUTOVER EXECUTION — AUTHORIZED WORK ORDER

EX-A — Begin from the pushed sealed boundary

Start from the latest clean main.

At minimum:

git status --short
git rev-parse HEAD
git rev-parse main
git rev-parse origin/main
git ls-remote origin refs/heads/main
git merge-base --is-ancestor e62a226fc661100a2427a4193213c7dadcf24225 HEAD
sha256sum build/agent-continuity/liturgy-reader-public-cutover-proposed.patch
git apply --check build/agent-continuity/liturgy-reader-public-cutover-proposed.patch

Expected patch hash:

cd11518ba7b20d198cbd16d08cc153d3f3053afeba8a230441c57312318a7566

If local/remote main disagree, the ancestor check fails, the patch hash differs,
or git apply --check fails: stop.

EX-B — Append continuity before applying

Append this complete review verbatim under:

## Independent compatibility-closure acceptance — reviewer to Codex

in:

build/agent-continuity/liturgy-reader-visual-plan.md

Then append:

## Public-cutover execution — Codex response

Before touching canonical files, record:

    exact starting SHA;

    clean worktree;

    main/origin/remote agreement;

    accepted compatibility ZIP hash;

    accepted cutover patch hash;

    exact execution baseline/ancestor result;

    git apply --check result;

    confirmation that all seven compatibility questions passed;

    proposed cutover commit sequence;

    explicit confirmation that public navigation and candidate/oracle cleanup remain out of scope.

Keep the continuity record current through deployment and rollback decisions.

EX-C — Apply the exact sealed patch

Apply:

build/agent-continuity/liturgy-reader-public-cutover-proposed.patch

Do not regenerate it.

Do not hand-edit the promoted canonical reader merely to “improve” it.

After applying, verify exactly the authorized 17 patch paths changed, aside from
the continuity and later handoff records required by this execution protocol.

The product effect must be limited to:

src/web/browser/liturgy/day.html
src/web/browser/liturgy/index.html

plus the exact release/test/tracking ownership changes already present in the
accepted patch.

Expected prospective canonical source hashes from the sealed package:

day.html
9a119a6aa87e900d6fc4c3e236191fe8a036abc305236eb576c09f823c7b7972

index.html
a6527316266365b79ff2ecdc193da3ab1034b1daa63408b869b192d2aeb85600

release/rights/public-alpha-2026-07-15.md
5a4b4d4f8bfbcf8d5fd54249c0d8664be7215b4bee9e82ccc8a37f400e3cf31e

If the post-apply hashes do not equal those exact values, stop.

EX-D — Local cutover gates before commit

Run the full task-owned gate set against the actual canonical filenames.

At minimum:

Python

Use the repository-locked environment and run the complete focused suite that
produced 230/230 in the compatibility handoff, plus any exact cutover-owned
tests introduced by the accepted patch.

All must pass.

Chromium/browser

Require:

    Day: all green, no qualification;

    Propers: all green;

    shared shell: all green;

    governed Instrument visual assertions: all green.

The canonical browser harnesses must now exercise:

/liturgy/day.html
/liturgy/index.html

as the public implementation, while retained candidate routes remain separate
fallback/noindex states.

Canonical visual/behavior matrix

Capture actual canonical-route states, not internal candidate aliases.

At minimum include:

Day

    Read 1440×900

    Read 1024×768

    Read 768×1024

    Read 393×852

    Missal 1440×900

    Missal 1024×768

    Missal 393×852

    Missal 320×852

    deep Missal scroll

    Roman partial

    postconciliar partial-English

    why=1 desktop

    why=1 mobile

    real multi-territorial desktop

    real multi-territorial mobile

    Date open

    Contents open

    Mode open

    Details open desktop/mobile

    200% text

    forced colors

    keyboard focus

    reduced motion

Propers

    Read desktop/mobile

    Browse desktop/mobile

    Contents/Mode/Details where governed

    stable cycle

    stable translation-witness

    explicit unsupported/stable alternative fail-closed state

    direct load/reload/Back-Forward for public option keys

Oracle

For equivalent states, compare canonical screenshots directly with the retained
accepted production candidate and the Liturgical Instrument visual oracle.

There should be no meaningful visual difference caused by changing the filename.

Static/indexing

Before deployment prove:

    canonical Day and Propers are indexable;

    retained candidate routes remain statically noindex/noarchive;

    oracle remains noindex;

    canonical pages do not emit user-visible candidate/internal wording;

    no candidate URL is advertised as canonical/Open Graph public URL.

Publication

Require:

make check-release-bindings
locked public-alpha check
locked public-alpha build
locked public-alpha verify --deployment-target github-pages
git diff --check

and exact expected source hashes.

Do not bless unrelated stored example transcripts.

EX-E — Cutover commit

Prefer one bounded cutover execution commit for the accepted 17-path patch
plus the already-required continuity phase transition, unless repository tracking
conventions force a second documentation-only checkpoint.

Do not combine unrelated cleanup.

The cutover commit message should describe same-path promotion, not visual redesign.

Push only after all EX-D gates pass.

Record the exact SHA in continuity.

EX-F — Exact-SHA GitHub Pages deployment gate

The cutover is not provisionally successful until GitHub Pages reports Success
for the exact cutover SHA.

Verify:

    Pages run is triggered by that SHA;

    build succeeds;

    deploy succeeds;

    artifact exists;

    deployed environment points at that SHA.

If the exact cutover run fails or times out, do not substitute an earlier run.

Diagnose only bounded deployment issues. If public canonical routes are left in
a mixed or uncertain state, invoke the rollback rule below.

EX-G — Immediate deployed verification

After the exact-SHA Pages success, verify the actual public routes directly.

At minimum:

/liturgy/day.html
/liturgy/day.html#date=2026-08-05&missal=roman-1962&bible=douay-rheims
/liturgy/index.html
/liturgy/index.html#missal=roman-1962&type=seasonal&mass=advent-1&bible=douay-rheims

Plus the compatibility states:

    why=1;

    real territorial date;

    postconciliar Day;

    stable Propers cycle;

    stable translation-witness;

    stable explicit alternative fail-closed fixture.

Prove:

    HTTP 200;

    correct canonical/indexable robots behavior;

    exact deep-link state;

    reload;

    Back/Forward;

    no redirect to *-reader.html;

    no required failed requests;

    no console errors;

    no duplicate IDs;

    no unnamed controls;

    no required horizontal overflow;

    no visible candidate/internal product language;

    expected Day↔Propers Details links;

    deployed/source byte parity for changed canonical HTML and all changed bound
    publication records/assets where direct byte parity is meaningful.

Capture canonical screenshots at original pixels.

EX-H — Cache-window verification

The public-cutover plan identified an observed static freshness window of roughly
600 seconds.

Perform two deployed passes:

Pass 1 — immediate/cache-bypassed

Use cache-bypassing requests/browser state and verify exact new source/assets.

Pass 2 — after more than the observed freshness window

After the window, re-run the key canonical URL/state/browser checks without
relying on cache-busting.

The purpose is to catch an old-HTML/new-JS or new-HTML/old-JS mixed generation.

The second pass must include at least:

    canonical Day default;

    canonical Day deep link;

    canonical Day Missal;

    canonical Propers deep link;

    one shell surface;

    one compatibility state;

    console/request/HTTP checks.

Do not declare the deployed cutover ready for independent acceptance before this
second pass is green.

Immediate rollback rule

If any material canonical-route, deployment, state, source, accessibility, or
mixed-cache gate fails after the public cutover is pushed, prefer immediate
rollback over live debugging.

Use ordinary:

git revert <CUTOVER_COMMIT>
git push origin main

Do not rewrite history.

Then require:

    successful Pages deployment for the exact revert SHA;

    HTTP 200 on canonical Day/Propers;

    restored legacy canonical source hashes/behavior;

    cache-bypassed verification;

    post-freshness-window verification.

Keep the compatibility-closed candidate and oracle routes intact throughout.

The separately committed candidate compatibility closure does not need to be
reverted merely because canonical promotion is reverted.

EX-I — Immutable public-cutover execution handoff

After all immediate and cache-window deployment checks pass, create:

build/agent-handoffs/<UTC>-liturgy-reader-instrument-public-cutover-execution/
build/agent-handoffs/<UTC>-liturgy-reader-instrument-public-cutover-execution.zip

The maintainer's continuity requirement authorizes force-adding only that exact
new execution handoff directory and its matching ZIP if ignored.

Include at minimum:

START-HERE.md
HANDOFF.md
INSTRUCTIONS.md
REVIEW.md
CODEX-RESPONSE.md
PLAN-AND-CONTINUITY.md
CUTOVER-DIFF.patch
CHANGED-FILES.txt
SOURCE-HASHES.txt
DEPLOYMENT.md
CACHE-WINDOW.md
ROLLBACK.md
checks.txt
MANIFEST.sha256

and:

    all canonical-route browser results;

    original-pixel canonical screenshots;

    accepted-candidate/oracle comparison evidence;

    stable-key evidence;

    why/territorial evidence;

    indexing/metadata evidence;

    exact Pages run evidence;

    deployed source/parity results;

    immediate and post-cache-window checks;

    exact pre-cutover and cutover SHAs.

Generate MANIFEST.sha256 last.

Then:

sha256sum -c MANIFEST.sha256
zip ...
unzip -t <zip>
# verify exactly one top-level directory
sha256sum <zip>

Commit and push the durable handoff.

Update continuity and tracking with the exact artifact paths/hash.

Worktree must be clean and main, origin/main, and remote main must agree.

Hard stopping point

Once:

    the accepted patch has been applied exactly;

    all local canonical gates pass;

    the bounded cutover commit is pushed;

    exact-SHA Pages deployment succeeds;

    immediate deployed verification passes;

    post-freshness-window verification passes;

    the immutable execution handoff is pushed;

    continuity/tracking is current;

    worktree and remote state are clean/synchronized;

STOP FOR INDEPENDENT PUBLIC-CUTOVER ACCEPTANCE.

Do not continue into cleanup.

Next independent review questions

The post-deployment reviewer must answer:

    Are the canonical Day and Propers URLs now serving the accepted Liturgical
    Instrument with no redirect or state-contract regression?

    Do legacy deep links, default Day state, why=1, territorial branches, and
    stable Propers keys behave as accepted?

    Is canonical visual output materially identical to the accepted production
    candidate/oracle across governing desktop/mobile/accessibility states?

    Are canonical pages correctly indexable while candidate/oracle routes remain
    nonindexable?

    Are release bindings, deployed bytes, and the exact Pages SHA correct?

    Did both immediate and post-freshness-window checks pass without mixed-cache
    incompatibility?

    Did public navigation remain unchanged and candidate/oracle fallbacks remain
    intact?

    Is the public cutover safe to accept and mark complete?

Only after that review may the cutover be marked accepted/complete.

Candidate/oracle cleanup, navigation redesign, search, source expansion, and
other visual/product work remain later independent decisions.

Final authorization boundary

    Compatibility closure: ACCEPTED

    why=1 compatibility: ACCEPTED

    territorial compatibility: ACCEPTED

    stable Propers public keys: ACCEPTED

    retained-candidate static noindex: ACCEPTED

    route-neutral public wording: ACCEPTED

    Details-based related/context navigation: ACCEPTED

    regenerated sealed cutover patch: ACCEPTED

    same-path public-cutover execution: AUTHORIZED

    canonical day.html / index.html modification by the exact sealed patch:
    AUTHORIZED

    exact release/test/tracking changes in the sealed patch: AUTHORIZED

    public navigation changes: UNAUTHORIZED

    candidate/oracle cleanup: UNAUTHORIZED

    visual redesign/refactor/source expansion: UNAUTHORIZED

    final public-cutover acceptance: PENDING POST-DEPLOYMENT REVIEW

## Public-cutover execution — Codex response

Starting boundary is clean `main` at
`e69d91ffff5823dc2970f867f1be8c9eb5b6363b`; `HEAD`, local `main`,
`origin/main`, and remote `refs/heads/main` all agree exactly. Accepted
compatibility ZIP SHA-256 is
`2222dada68a66a98a9fc029b8d7c0550d7d4de3c36634f19bbec1e24d150b31c`.
Accepted cutover patch SHA-256 is
`cd11518ba7b20d198cbd16d08cc153d3f3053afeba8a230441c57312318a7566`.
Exact execution baseline `e62a226fc661100a2427a4193213c7dadcf24225`
is an ancestor of the starting boundary, and normal-context `git apply --check`
passes against the actual worktree. No patch-owned target has drifted.

All seven compatibility questions passed: source-owned `why=1`, every held
territorial branch, stable public Propers keys, static retained-candidate
privacy, route-neutral wording, subordinate Details navigation, unchanged
closure-phase canonical sources, and the complete regenerated patch are all
accepted.

The execution sequence is: apply the exact reviewed patch; verify the 17-path
scope and three prospective hashes; run locked focused, browser, visual,
release, publication, indexing, and isolation gates against the canonical
filenames; commit and push the same-path promotion; require Pages success for
that exact SHA; perform immediate cache-bypassed public verification; wait more
than the observed 600-second freshness window and repeat the required public
checks without cache busting; then seal and push the immutable execution
handoff and stop for independent acceptance. Material post-push failure invokes
the ordinary-revert rollback plan.

Public navigation redesign, candidate/oracle cleanup, visual redesign, state or
renderer refactoring, source/translation expansion, and any work beyond the
accepted patch and execution evidence remain out of scope.

### Execution checkpoint — sealed patch gate blocker

The exact sealed patch was applied locally after every EX-A safeguard passed.
Its three required prospective hashes matched exactly:

- `day.html`: `9a119a6aa87e900d6fc4c3e236191fe8a036abc305236eb576c09f823c7b7972`
- `index.html`: `a6527316266365b79ff2ecdc193da3ab1034b1daa63408b869b192d2aeb85600`
- rights record: `5a4b4d4f8bfbcf8d5fd54249c0d8664be7215b4bee9e82ccc8a37f400e3cf31e`

The mandatory pre-commit gates then proved that the accepted patch is not an
executable green cutover patch. The locked focused command ran all 230 tests
and stopped with five task-owned failures: stale canonical-boundary assertions
in `test_liturgy_reader_state.py` and `test_public_alpha.py`, two undefined
variables plus one stale Instrument-surface assertion in
`test_mass_ordinary.py`. The shared-shell Chromium harness independently ran
17/18 and timed out because its canonical-route assertion still waits for the
legacy `#reading` DOM instead of the promoted reader readiness/document.

These are cutover-owned test and harness defects, not the disclosed unrelated
example-transcript divergence. Correcting them would require bytes outside the
exact accepted patch: at least a new change to
`tools/tests/liturgy_reader_shell_browser.mjs`, which is not one of the 17
authorized paths, plus modifications beyond the accepted hunks in three
patch-owned test files. The execution authorization expressly permits the
exact sealed release/test/tracking changes and forbids regenerating or
reconstructing the patch without review. Codex therefore did not alter those
tests, did not commit or push the canonical promotion, and did not trigger a
Pages deployment.

The exact patch was reversed locally, so the repository returned to the
pre-cutover product boundary while this append-only continuity record was
preserved. Public navigation, canonical public readers, retained candidates,
and the oracle remain unchanged. Next exact action: obtain narrow reviewer
authorization for a corrected execution patch (or for the specifically bounded
test/harness repairs), then repeat EX-A from the synchronized main boundary.

Correction to the preceding checkpoint: its phrase “stale canonical-boundary
assertions in `test_liturgy_reader_state.py` and `test_public_alpha.py`” is too
broad. The state failure is a stale legacy production-boundary assertion; the
public-alpha failure is the existing link-preview test comparing an unescaped
source apostrophe with the builder's correctly HTML-escaped metadata. The exact
five failures were: one state boundary failure, three stale/undefined
`test_mass_ordinary.py` failures, and one public-alpha metadata-escaping
failure. This correction supersedes only that diagnostic phrase, not the gate
result or stop decision.

Durable-stop commit `90fe6572dac8721237ea9a82b147c6e7666bc180`
pushed the complete review, Codex response, and blocker record. Its automatic
GitHub Pages run `31169018372` succeeded. That commit contains no public product
change; it rebuilt and deployed the unchanged legacy canonical Day/Propers
sources with hashes `bc5a98de6b718431f3b91e6a133bb847c2dcdf4d21fce6f45aae3ad4984de868`
and `f630f4a66f3f525144336f183b1485c698030c7531ff679375b3a7aa00150c65`.

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

## Cutover-gate repair — Codex response

Record:

    exact starting SHA;

    clean worktree;

    HEAD, local main, origin/main, and remote-main agreement;

    the old rejected patch hash;

    the six known gate failures;

    the exact authorized 19-path replacement-patch scope;

    confirmation that canonical Day/Propers will remain unchanged on committed
    main during this repair phase;

    confirmation that no Pages cutover deployment will be attempted;

    the scratch-validation method;

    the intended handoff/stopping point.

Do not use a Git worktree. If isolation is needed, use a separate temporary
checkout/copy in its own directory.
GR-B — Build the corrected patch in scratch, not on live main

The goal is to test the prospective post-cutover tree without committing that
tree to public main.

Use a disposable separate checkout/copy rooted at the synchronized repair
baseline.

In that scratch tree:

    apply the old accepted cutover patch as the starting draft;

    make only the authorized gate corrections below;

    run the full pre-deployment gates;

    iterate only within the authorized 19 paths;

    once green, generate a new complete replacement cutover patch relative to
    the unchanged public baseline.

The scratch tree must never be pushed or deployed.

The real repository's canonical:

src/web/browser/liturgy/day.html
src/web/browser/liturgy/index.html

must remain at their legacy hashes throughout this phase.
GR-C — Exact test/harness repair requirements
C1. State public-boundary test

Replace the stale post-cutover expectation:

canonical routes do not load reader-state.js / reader-state-adapters.js

with an assertion that describes the accepted post-cutover ownership.

The prospective canonical Day and Propers pages must load the shared reader
contract they actually use.

At minimum, after the replacement patch is applied in scratch:

day.html
index.html

must both load:

reader-state.js
reader-state-adapters.js

Do not simply delete the public-boundary test.

Prefer renaming it to communicate the new contract, e.g. in substance:

test_promoted_production_routes_load_the_shared_reader_contract

Also retain the existing proof that synthetic fixture IDs do not enter public
data and that contract modules are release-bound.

The assertion should prove ownership, not merely search for an arbitrary token.
C2. test_mass_ordinary.py

Fix the incomplete migration; do not weaken the hierarchy tests.
Day hierarchy

The accepted Day static hierarchy is:

celebration identity
coverage notice
reader document
reader actions / dialog surfaces

Remove orphan assertions involving legacy:

settings
settings-disclosure
controls
</details>

when they no longer exist in the promoted Instrument markup.

Retain explicit checks for:

celebration-title
coverage-notice
reader-document
reader-actions
contents surface
details surface

and their intended order.
Propers hierarchy

Likewise remove orphan legacy references to:

settings
notices
controls
legacy details

Retain the accepted Propers identity → notice → reader document → actions/surfaces
ordering and the Browse/Details surface presence.
Contents closed-state test

Do not keep assertions against old <details> markup.

For each promoted canonical page:

    locate reader-document;

    locate the Contents <dialog>;

    locate the page controller script;

    prove the static ordering expected by the accepted reader;

    inspect the actual opening <dialog ...> tag and assert it does not contain
    the open attribute;

    do not search for </details>.

The test must still prove that Contents begins closed; it may not be reduced to
“the string exists.”
C3. Public-alpha metadata escaping

The source description is human-authored text. The built HTML metadata is
serialized HTML.

Do not alter the canonical description merely to avoid an apostrophe.

Do not weaken link-preview validation.

Fix the assertion by comparing at the correct representation boundary.

Acceptable approaches include:

    HTML-escaping the declared source value using the same standard semantics
    expected for an HTML attribute before asserting serialized output; or

    parsing the generated head/attribute and comparing the decoded value to the
    source declaration.

Prefer the approach that proves both:

    semantic equality of the declared description;

    valid safe serialized metadata.

Do not duplicate the public-alpha builder implementation inside the test.
C4. Shared-shell canonical-route Chromium assertion

Replace the legacy production-route assertion around the old #reading DOM.

For canonical Day after prospective promotion, require in substance:

window.dayReaderReady === true
#reader-document[aria-busy="false"]
rendered Proper/content exists
exactly one accepted reader shell exists

For canonical Propers require:

window.propersReaderReady === true
#reader-document[aria-busy="false"]
rendered Proper/content exists
exactly one accepted reader shell exists

Continue to verify the actual canonical filenames:

day.html
index.html

Do not turn this into a candidate-route test.

Do not merely change the timeout.

Do not retain the old assertion:

reader-shell count === 0

The post-cutover contract is the opposite: canonical routes are the accepted
reader shell.

Rename the test to reflect the new ownership, e.g. in substance:

canonical Day and Propers routes render the accepted shared shell

GR-D — Preserve old-patch product hashes

The gate repair does not authorize new product bytes.

After applying the corrected replacement patch in scratch, the prospective
canonical source hashes must remain exactly the values already accepted:

day.html
9a119a6aa87e900d6fc4c3e236191fe8a036abc305236eb576c09f823c7b7972

index.html
a6527316266365b79ff2ecdc193da3ab1034b1daa63408b869b192d2aeb85600

The prospective rights record must remain:

5a4b4d4f8bfbcf8d5fd54249c0d8664be7215b4bee9e82ccc8a37f400e3cf31e

If any of these hashes differ, stop. A gate repair must not mutate the accepted
product promotion.
GR-E — Required green scratch gates

Before sealing a replacement patch, the scratch post-cutover tree must pass all
pre-deployment gates that previously blocked execution.
Focused locked Python

Require:

230/230 or greater if a legitimate new test is added
0 failures

No xfail/skip may be added to hide these six defects.

Specifically record the individual results for:

test_liturgy_reader_state.py
test_mass_ordinary.py
test_public_alpha.py

Chromium

Require:

Day: all green
Propers: all green
Shared shell: 18/18 or greater
Governed Instrument: all green

The repaired shared-shell test must prove the canonical promoted shell rather
than candidate-only behavior.
Syntax/static

Run syntax checks for every changed Python/JavaScript test/harness.

Require:

git diff --check

Publication/release

Require:

make check-release-bindings
locked public-alpha check
locked public-alpha build
locked public-alpha verify --deployment-target github-pages

All must pass.
Product/evidence invariants

Require:

    exact prospective Day hash;

    exact prospective Propers hash;

    exact prospective rights hash;

    candidate/oracle routes unchanged;

    no new product code path;

    no public navigation change;

    no source/data/renderer/state change;

    no console/request/HTTP/control/ID/required-overflow failures in governed
    browser runs.

The unrelated governed stored-example divergence remains an honest qualification.
Do not recapture or bless it.
GR-F — Audit the repaired assertions for strength

Before accepting a green run, explicitly review each repair for accidental
weakening.

Answer in the handoff:
State test

Does it now prove the promoted canonical pages own the same shared reader contract
that the accepted candidate uses?
Ordinary static tests

Do they still prove hierarchy and surfaces, or did the repair merely remove old
assertions?
Metadata test

Does it prove semantic description parity across source and escaped output rather
than accepting any metadata?
Shell browser test

Does it prove canonical route, readiness, rendered content, and one accepted shell,
rather than merely waiting for a page to stop loading?

If any answer is no, the gate repair is not complete.
GR-G — Replace, do not amend-in-place conceptually, the old sealed patch

Generate a new complete file:

build/agent-continuity/liturgy-reader-public-cutover-proposed.patch

It supersedes the old rejected executable patch.

At its header, record:

# CORRECTED PROPOSED PUBLIC CUTOVER PATCH — UNAPPLIED
# Gate-repair baseline: e20b2f542ab51a2b4f0807e6394ca5ecb313699c
# Supersedes rejected patch:
# cd11518ba7b20d198cbd16d08cc153d3f3053afeba8a230441c57312318a7566

Record:

    exact path count;

    exact path list;

    new SHA-256;

    prospective canonical source hashes;

    scratch validation totals.

The patch must be a clean normal-context patch applicable to the synchronized
repository state.

Run:

git apply --check build/agent-continuity/liturgy-reader-public-cutover-proposed.patch

against a clean copy of the actual synchronized main.

Do not use:

git apply --3way
fuzzy manual reconstruction

A green scratch tree is not enough; the sealed patch itself must be mechanically
applicable.
GR-H — Do not execute the repaired patch

This phase stops before canonical promotion.

On the real pushed main:

    day.html remains at
    bc5a98de6b718431f3b91e6a133bb847c2dcdf4d21fce6f45aae3ad4984de868;

    index.html remains at
    f630f4a66f3f525144336f183b1485c698030c7531ff679375b3a7aa00150c65.

Do not commit the scratch-promoted test files themselves as live changes.

The only committed outputs of this phase should be:

    the replacement sealed patch artifact;

    continuity;

    truthful tracking/diagnostic records if needed;

    the immutable gate-repair handoff.

If a tracking file is already part of the future cutover patch, avoid creating
a conflicting live edit merely to narrate this repair. Continuity is the
authoritative append-only record.
GR-I — Immutable gate-repair handoff

Create:

build/agent-handoffs/<UTC>-liturgy-reader-public-cutover-gate-repair/
build/agent-handoffs/<UTC>-liturgy-reader-public-cutover-gate-repair.zip

The maintainer's continuity requirement authorizes force-adding only this exact
new handoff directory and its matching ZIP if ignored.

Include at minimum:

START-HERE.md
HANDOFF.md
INSTRUCTIONS.md
REVIEW-AUTHORIZATION.md
CODEX-RESPONSE.md
PLAN-AND-CONTINUITY.md
OLD-PATCH-SHA256.txt
CORRECTED-CUTOVER.patch
CORRECTED-PATCH-SHA256.txt
CHANGED-PATCH-PATHS.txt
GATE-FAILURES-BEFORE.txt
GATE-RESULTS-AFTER.txt
TEST-REPAIR-DIFF.patch
SCRATCH-METHOD.md
SOURCE-HASHES.txt
checks.txt
MANIFEST.sha256

Also include exact evidence/output for:

    focused locked Python;

    the three formerly failing Python test modules;

    Day Chromium;

    Propers Chromium;

    shared-shell Chromium;

    governed Instrument assertions;

    release binding;

    locked public-alpha check/build/verify;

    patch apply-check;

    real-repository canonical-source hashes proving no public promotion occurred.

Generate MANIFEST.sha256 last.

Verify:

sha256sum -c MANIFEST.sha256
unzip -t <zip>
# exactly one top-level directory
sha256sum <zip>

Commit and push the handoff, replacement patch, and continuity.

Require clean worktree and:

HEAD == main == origin/main == remote main

Narrow independent re-review

Stop and request independent review answering only:

    Are the six pre-deployment failures repaired at the correct test/harness
    boundary rather than by changing accepted reader behavior?

    Does the replacement patch contain only the authorized 19 paths?

    Are prospective canonical Day/Propers/rights bytes identical to the previously
    accepted cutover product bytes?

    Does focused locked Python now pass completely?

    Do Day, Propers, shared-shell, and governed Instrument browser gates all pass
    against the prospective canonical routes?

    Are the repaired tests at least as strong as the contracts they replace?

    Does the replacement patch apply cleanly to current synchronized main?

    Did real canonical day.html and index.html remain unchanged and undeployed
    throughout this repair phase?

    If all eight pass, may the replacement patch proceed directly into the
    previously defined cutover execution/deployment/cache-window protocol?

Only the reviewer may reauthorize execution.
Final authorization boundary

    Previous execution stop: ACCEPTED

    Old sealed patch as executable artifact: REJECTED / SUPERSEDED

    Accepted reader product bytes: FROZEN

    Test/harness gate repair in scratch: AUTHORIZED

    Replacement 19-path cutover patch generation: AUTHORIZED

    test_liturgy_reader_state.py corrected cutover assertion: AUTHORIZED

    test_mass_ordinary.py incomplete migration repair: AUTHORIZED

    test_public_alpha.py metadata escaping expectation repair: AUTHORIZED

    liturgy_reader_shell_browser.mjs canonical Instrument assertion: AUTHORIZED

    Canonical source modification on committed main: UNAUTHORIZED

    Cutover commit: UNAUTHORIZED PENDING RE-REVIEW

    Pages cutover deployment: UNAUTHORIZED PENDING RE-REVIEW

    Public navigation changes: UNAUTHORIZED

    Candidate/oracle cleanup: UNAUTHORIZED

    Visual/product/state/renderer/source changes: UNAUTHORIZED

## Cutover-gate repair — Codex response

Gate repair starts from exact synchronized SHA
e20b2f542ab51a2b4f0807e6394ca5ecb313699c. The worktree was clean, and HEAD,
local main, origin/main, and remote refs/heads/main all agreed at that SHA
before this continuity append.

The previously sealed executable patch, SHA-256
cd11518ba7b20d198cbd16d08cc153d3f3053afeba8a230441c57312318a7566, is
rejected and will not be executed again. Its prospective trial exposed six
task-owned gate defects: one stale shared-state public-boundary assertion;
three incomplete Ordinary static-test migrations (two orphan legacy hierarchy
references and one obsolete <details> closed-state check); one public-alpha
metadata assertion comparing unescaped source text to correctly escaped
serialized HTML; and one shared-shell Chromium assertion that still expects
legacy #reading and no shell on the canonical routes.

The replacement patch is limited to the exact authorized 19 paths listed in
the reviewer authorization: the original 17 cutover paths plus
tools/tests/test_liturgy_reader_state.py and
tools/tests/liturgy_reader_shell_browser.mjs. No repair outside that set will
be made.

Validation will occur in a disposable separate checkout/copy rooted at this
synchronized boundary, never in a Git worktree and never pushed or deployed.
The rejected patch will be applied there as a draft; only the authorized
test/harness corrections will be made; the full locked Python, Chromium,
syntax, release, public-alpha, hash, scope, and assertion-strength gates will
run there. A new normal-context 19-path patch will then be generated relative
to the unchanged public baseline and separately apply-checked against a clean
copy of synchronized main.

On committed main, canonical src/web/browser/liturgy/day.html and
src/web/browser/liturgy/index.html will remain at their legacy hashes. No
Pages cutover deployment, public navigation change, candidate/oracle cleanup,
or product-byte change will be attempted in this repair phase. The stopping
point is a pushed, immutable gate-repair handoff and corrected unapplied patch,
followed by narrow independent review; only that reviewer may reauthorize
cutover execution.

### Gate-repair validation checkpoint

The scratch tree exposed one additional stale harness selector beyond the six
known failures: the Day current-style latent-state parity assertion still read
canonical Proper text from legacy `#reading`. Because
`tools/tests/day_reader_integration_browser.mjs` is already one of the exact 19
authorized paths, Codex changed only that selector to the accepted
`#reader-document` and recorded the added defect rather than masking it.

All repaired assertions remain substantive. The state test requires one shared
state contract, adapter, and route controller in dependency order on each
canonical page. The Ordinary tests retain identity, coverage, reading-plane,
action, dialog, accessibility, initial-closed-state, and script/style-order
proofs alongside the unchanged event-sequence digests. The metadata test
requires safe serialized equality across description, Open Graph, and Twitter
fields. The shared-shell browser test requires canonical readiness, settled
rendered Proper content, exactly one accepted shell, and the correct entrance
identity for both canonical filenames.

Final scratch gates are green: formerly failing Python modules 157/157; full
locked focused Python 230/230; Day Chromium 40/40; Propers Chromium 32/32;
shared-shell Chromium 18/18; governed Instrument Chromium 24/24; syntax,
`git diff --check`, promised-deliverables, tool registry, release bindings (zero
stale), and locked public-alpha check/build/GitHub-Pages verification all pass.
Browser reports contain no console, required-request, HTTP, unnamed-control, or
required-overflow failure.

The corrected complete patch contains exactly the authorized 19 paths and has
SHA-256
`ce43cef0621e3e1bdf6eb53eb4ce62e479e54977bd739a26385068bcaa33b0e5`.
Normal-context `git apply --check` passes against synchronized real main. Its
prospective Day, Propers, and rights hashes remain exactly `9a119a6a…`,
`a6527316…`, and `5a4b4d4f…`. Real committed canonical sources remain unchanged
at `bc5a98de…` and `f630f4a6…`; no public cutover commit or deployment occurred.

The immutable review package is
`build/agent-handoffs/20260807T105259Z-liturgy-reader-public-cutover-gate-repair/`
with matching ZIP. The next exact action is the nine-question narrow review in
its `HANDOFF.md`. Cutover execution, public navigation changes, and
candidate/oracle cleanup remain unauthorized.

The handoff manifest verifies all 268 payload entries, the directory contains
269 files including `MANIFEST.sha256`, and the ZIP integrity and exactly-one-
top-level-directory checks pass. The canonical continuity snapshot and
corrected-patch copy were byte-identical to their tracked sources at sealing.
The replacement patch's context-prefix spaces necessarily appear as trailing
spaces when the patch artifact itself is treated as prose by `git diff
--check`; strict `git apply --check --whitespace=error-all` passes, and the
scratch target diff itself passes `git diff --check`. Repository diff checking
therefore excludes only the generated patch envelope, not any prospective
target path.

### Post-seal push checkpoint

Commit `a996a82a68163dd5f7a2af24ae63f100244d6bc0` pushed the corrected
unapplied patch, continuity through sealing, and the immutable handoff directory
and ZIP. Automatic Pages run `31172425199` succeeded for that exact commit. It
is a handoff-only/continuity publication result: canonical source hashes remain
`bc5a98de…` and `f630f4a6…`, so it must not be cited as a cutover deployment.

The pushed corrected patch SHA-256 is
`ce43cef0621e3e1bdf6eb53eb4ce62e479e54977bd739a26385068bcaa33b0e5`.
The pushed ZIP SHA-256 is
`01181404404d8e6b87f6746588866f0f56a2f3a1aa9018f60d6d9ae287961823`;
its 268-entry manifest, ZIP integrity, and one-top-level-directory checks pass.
The disposable scratch checkout was deleted after evidence was copied and
sealed. The next action remains narrow independent gate-repair review; no
execution authorization is inferred.

## Independent gate-repair acceptance — reviewer to Codex

Liturgical Instrument — Gate-Repair Acceptance and Public-Cutover Reauthorization
Disposition

GATE REPAIR ACCEPTED. PUBLIC-CUTOVER EXECUTION REAUTHORIZED.

The corrected 19-path cutover patch repairs the pre-deployment gate failures at
the test/harness ownership boundary without altering the previously accepted
reader product bytes.

The replacement patch may now proceed directly into the already-defined
same-path public-cutover execution, deployment, cache-window verification, and
post-deployment independent-acceptance protocol.

This is execution authorization, not final cutover acceptance.

Public navigation redesign remains unauthorized.

Candidate/oracle cleanup remains unauthorized.

Visual redesign, renderer/state refactoring, Ordinary changes, source expansion,
translation expansion, and unrelated cleanup remain unauthorized.
Reviewed sealed package

Reviewed archive:

20260807T105259Z-liturgy-reader-public-cutover-gate-repair.zip

Independent archive verification:

    ZIP integrity: PASS

    exactly one top-level directory: PASS

    MANIFEST.sha256: 268/268 payload entries PASS

    ZIP SHA-256:

01181404404d8e6b87f6746588866f0f56a2f3a1aa9018f60d6d9ae287961823

Pushed immutable handoff:

build/agent-handoffs/20260807T105259Z-liturgy-reader-public-cutover-gate-repair/
build/agent-handoffs/20260807T105259Z-liturgy-reader-public-cutover-gate-repair.zip

Pushed handoff/seal commit:

a996a82a68163dd5f7a2af24ae63f100244d6bc0

The handoff-only Pages run for that commit:

31172425199

succeeded, but canonical readers were unchanged. It is not a cutover deployment
and must never be used as evidence that the public cutover succeeded.
Corrected replacement patch

Canonical replacement patch:

build/agent-continuity/liturgy-reader-public-cutover-proposed.patch

Reviewed copy:

CORRECTED-CUTOVER.patch

SHA-256:

ce43cef0621e3e1bdf6eb53eb4ce62e479e54977bd739a26385068bcaa33b0e5

It supersedes and invalidates the old executable patch:

cd11518ba7b20d198cbd16d08cc153d3f3053afeba8a230441c57312318a7566

Never execute the old patch again.
Nine narrow review dispositions
1. Were the pre-deployment defects repaired at the test/harness boundary?

PASS

No accepted reader implementation byte was changed.

The repair correctly updates stale tests/harness ownership after same-path
promotion rather than distorting the product to satisfy legacy assertions.

The scratch run exposed one additional stale #reading selector in
tools/tests/day_reader_integration_browser.mjs. That file was already within
the authorized 19-path scope, and changing it to the accepted
#reader-document contract was the correct bounded repair.
2. Is the replacement patch limited to the authorized scope?

PASS

The patch contains exactly 19 paths:

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

This is exactly the authorized replacement scope.

No reader JavaScript/CSS, shared state/adapter/shell implementation, source data,
Ordinary implementation, candidate page, oracle, or public-navigation path is
present.
3. Are prospective product/release bytes identical to the accepted cutover?

PASS

The corrected patch preserves the previously accepted prospective hashes:

src/web/browser/liturgy/day.html
9a119a6aa87e900d6fc4c3e236191fe8a036abc305236eb576c09f823c7b7972

src/web/browser/liturgy/index.html
a6527316266365b79ff2ecdc193da3ab1034b1daa63408b869b192d2aeb85600

release/rights/public-alpha-2026-07-15.md
5a4b4d4f8bfbcf8d5fd54249c0d8664be7215b4bee9e82ccc8a37f400e3cf31e

The gate repair therefore did not reopen product design or implementation.
4. Does locked focused Python pass completely?

PASS

Prospective scratch state:

formerly failing Python modules: 157/157
complete focused locked Python: 230/230

No skip or xfail was introduced to conceal the defects.
5. Do all four browser gates pass against the prospective canonical state?

PASS

Day Chromium:             40/40
Propers Chromium:         32/32
shared-shell Chromium:    18/18
governed Instrument:      24/24

The browser reports also record:

console problems:                 0
required failed requests:         0
HTTP problems:                    0
unnamed controls:                 0
required horizontal overflow:     0

The prospective canonical Day and Propers screenshots remain materially the
accepted Liturgical Instrument. No visual re-review blocker is introduced by
the gate repair.
6. Are the repaired assertions still strong?

PASS
Shared state ownership

The replacement test does not merely delete the pre-cutover negative assertion.
For each canonical page it requires exactly one:

reader-state.js
reader-state-adapters.js
route controller

and proves dependency order:

state → adapters → controller

That is the correct promoted production contract.
Ordinary/page hierarchy

The repaired tests now prove the actual accepted hierarchy and interaction
surfaces, including:

    reader identity/title;

    coverage notice;

    reader-document;

    action rail/dock;

    four exact actions;

    aria-controls;

    collapsed aria-expanded;

    dialog presence and closed initial state;

    accessibility attributes;

    Browse/Date/Contents/Mode/Details structure;

    expected script/style dependency ordering.

They also retain the existing semantic/event/order tests.

This is stronger than keeping stale <details>, settings, notices, and
#reading assertions.
Metadata serialization

The metadata repair checks the declared browser description against the safely
serialized form used by:

description
og:description
twitter:description

It accounts for HTML escaping instead of weakening the content contract or
changing source copy to avoid apostrophes.
Shared-shell browser ownership

The canonical-route browser test now requires:

    the actual canonical filenames;

    route-specific ready flag;

    settled #reader-document;

    rendered Proper content;

    exactly one [data-reader-shell];

    the correct day or propers shell entrance.

It no longer waits for legacy #reading or asserts that the canonical pages
have no shell.

The Day parity harness likewise reads the prospective canonical content from
the actual accepted reading document.

No repaired gate was made vacuous.
7. Does the patch mechanically apply?

PASS AT THE SEALED BOUNDARY; MUST BE RECHECKED IMMEDIATELY BEFORE EXECUTION

The package records a normal-context:

git apply --check

pass against synchronized real main at the gate-repair baseline.

Current pushed main subsequently adds the sealed patch/continuity/handoff
commit a996a82...; that commit is archival/build-tree work rather than a
cutover-target modification.

The execution agent must nevertheless re-run all pre-apply checks against the
actual synchronized current main. No inference substitutes for this check.

If normal-context git apply --check fails, stop. Do not use --3way, fuzz,
or manual reconstruction.
8. Did the real canonical readers remain unchanged and undeployed?

PASS

During gate repair the real committed canonical sources remained:

day.html
bc5a98de6b718431f3b91e6a133bb847c2dcdf4d21fce6f45aae3ad4984de868

index.html
f630f4a66f3f525144336f183b1485c698030c7531ff679375b3a7aa00150c65

No public cutover commit or deployment occurred.

The successful Pages run 31172425199 only rebuilt those unchanged canonical
readers.
9. May the replacement patch enter the execution/deployment/cache protocol?

YES. AUTHORIZED.

The replacement patch has cleared the exact gate that stopped the previous
attempt.

Proceed directly to the bounded execution protocol below.
EXECUTION PROTOCOL
EX-1 — Start from current synchronized main

Before any canonical modification:

git status --short
git rev-parse HEAD
git rev-parse main
git rev-parse origin/main
git ls-remote origin refs/heads/main

Require:

HEAD == main == origin/main == remote main

Record the actual starting SHA.

Verify the pushed patch:

sha256sum build/agent-continuity/liturgy-reader-public-cutover-proposed.patch

Expected:

ce43cef0621e3e1bdf6eb53eb4ce62e479e54977bd739a26385068bcaa33b0e5

Verify the gate-repair baseline is an ancestor:

git merge-base --is-ancestor e20b2f542ab51a2b4f0807e6394ca5ecb313699c HEAD

Run:

git apply --check build/agent-continuity/liturgy-reader-public-cutover-proposed.patch

Then verify none of the 19 patch-owned target paths has drifted in a way that
changes the accepted prospective result.

If any precondition fails: STOP FOR REVIEW.

Do not use:

git apply --3way
manual fuzzy application
patch regeneration

EX-2 — Append continuity before promotion

Append this review verbatim under:

## Independent gate-repair acceptance — reviewer to Codex

in:

build/agent-continuity/liturgy-reader-visual-plan.md

Then append:

## Public-cutover execution retry — Codex response

Record before applying:

    synchronized starting SHA;

    clean worktree;

    replacement patch SHA;

    successful ancestor check;

    successful normal-context apply check;

    all nine gate-repair review dispositions;

    exact intended commit/deploy sequence;

    rollback trigger;

    confirmation that navigation and candidate/oracle cleanup remain forbidden.

EX-3 — Apply exactly the replacement patch

Apply:

git apply build/agent-continuity/liturgy-reader-public-cutover-proposed.patch

Do not regenerate or hand-edit the promoted product.

Immediately verify:

day.html
9a119a6aa87e900d6fc4c3e236191fe8a036abc305236eb576c09f823c7b7972

index.html
a6527316266365b79ff2ecdc193da3ab1034b1daa63408b869b192d2aeb85600

release/rights/public-alpha-2026-07-15.md
5a4b4d4f8bfbcf8d5fd54249c0d8664be7215b4bee9e82ccc8a37f400e3cf31e

Verify the patch effect consists of the accepted 19 paths plus only the
continuity/handoff bookkeeping explicitly required by this protocol.

If any prospective product/release hash differs: stop and reverse the uncommitted
application.
EX-4 — Repeat the full local canonical pre-deployment gate

The scratch proof authorizes execution; it does not waive a real-tree run.

Before committing, require the actual promoted working tree to pass:

focused locked Python:          230/230 or greater, zero failures
Day Chromium:                   all green
Propers Chromium:               all green
shared-shell Chromium:          all green
governed Instrument:            all green
changed Python/JS syntax:       pass
git diff --check:               pass
promised-deliverables:          pass
tool registry:                  pass
release bindings:               zero stale
locked public-alpha check:      pass
locked public-alpha build:      pass
locked public-alpha verify:     pass

The browser suites must run the actual canonical:

/liturgy/day.html
/liturgy/index.html

and preserve all previously accepted compatibility states:

    Roman and postconciliar;

    Read and Missal;

    empty Day default;

    direct deep links;

    reload and Back/Forward;

    partial coverage;

    why=1;

    multi-territorial outcomes;

    stable Propers cycle;

    stable alternative fail-closed behavior where unsupported;

    stable translation-witness;

    Date/Browse/Contents/Mode/Details;

    200% text;

    keyboard focus;

    forced colors;

    reduced motion;

    deep scroll.

The unrelated governed stored-example replay may remain non-green and must be
disclosed honestly. Do not recapture/bless it.

If any cutover-owned gate fails, reverse the uncommitted application and stop.
EX-5 — Commit and push the bounded public cutover

Once the actual promoted tree is fully green, create one bounded cutover commit
unless repository mechanics require a second documentation-only checkpoint.

The cutover commit must not include:

    public navigation changes;

    candidate/oracle cleanup;

    visual redesign;

    reader implementation changes outside the accepted promotion;

    source/data changes;

    unrelated refactoring.

Push to origin/main.

Record the exact cutover SHA.
EX-6 — Exact-SHA Pages gate

The cutover is not even provisionally successful until GitHub Pages reports
Success for the exact cutover SHA.

Require:

    workflow source SHA == cutover SHA;

    build succeeds;

    deploy succeeds;

    deployed artifact corresponds to that SHA.

Do not substitute:

    31172425199;

    31169274928;

    any compatibility run;

    any earlier successful reader deployment.

If the exact cutover deployment fails and the pushed canonical state could be
publicly uncertain or mixed, follow the rollback rule below.
EX-7 — Immediate live canonical verification

After exact-SHA Pages success, verify the real public URLs, including:

https://spincyc.github.io/triptych/liturgy/day.html
https://spincyc.github.io/triptych/liturgy/day.html#date=2026-08-05&missal=roman-1962&bible=douay-rheims
https://spincyc.github.io/triptych/liturgy/index.html
https://spincyc.github.io/triptych/liturgy/index.html#missal=roman-1962&type=seasonal&mass=advent-1&bible=douay-rheims

Also verify representative live states for:

    empty-Day Roman 1962 default;

    postconciliar Day;

    Read/Missal mode;

    why=1;

    real multi-territorial date;

    Propers cycle;

    translation-witness;

    explicit unsupported alternative;

    Details counterpart/context links.

Require:

    HTTP 200;

    no redirect to *-reader.html;

    correct hash/query state;

    reload;

    Back/Forward;

    correct canonical/indexing metadata;

    candidates/oracle remain statically noindex;

    no user-visible candidate/internal product language;

    no console problems;

    no required failed requests;

    no unexpected HTTP failure;

    no duplicate IDs;

    no unnamed controls;

    no required horizontal overflow;

    canonical visual output materially matches the accepted production candidate.

Capture original-pixel evidence.

Verify deployed/source byte parity for the changed canonical/release assets where
the publication model permits direct byte comparison.
EX-8 — Cache-window gate

The accepted cutover plan identified an observed freshness window of roughly
600 seconds.

Do not request final independent acceptance based only on cache-bypassed checks.

Run:
Immediate pass

Cache-bypassed/fresh verification of the new deployment.
Post-window pass

After more than the observed freshness window, run the key canonical checks
without cache-busting.

At minimum:

    Day empty/default;

    Day deep link;

    Day Missal;

    Propers deep link;

    one modal/shell surface;

    one compatibility state such as why=1 or territorial;

    console/request/HTTP checks.

The purpose is to detect old-HTML/new-JS or new-HTML/old-JS mixtures.

If mixed-generation behavior appears, rollback rather than debug against live
canonical routes.
Immediate rollback rule

For any material post-push canonical failure, prefer immediate ordinary revert.

Use:

git revert <CUTOVER_COMMIT>
git push origin main

Do not rewrite history.

Then require:

    successful Pages deployment for exact revert SHA;

    canonical Day/Propers HTTP 200;

    restored legacy public route behavior;

    cache-bypassed verification;

    post-freshness-window verification.

The compatibility-closed candidate and oracle routes remain intact and must not
be reverted merely because canonical promotion is reverted.
EX-9 — Seal the execution handoff

Only after:

    real-tree local gates are green;

    exact cutover SHA deploys successfully;

    immediate live checks pass;

    post-cache-window checks pass;

create and push:

build/agent-handoffs/<UTC>-liturgy-reader-instrument-public-cutover-execution/
build/agent-handoffs/<UTC>-liturgy-reader-instrument-public-cutover-execution.zip

The maintainer's continuity requirement authorizes force-adding only that exact
new execution handoff directory and its matching ZIP if ignored.

Include at minimum:

START-HERE.md
HANDOFF.md
INSTRUCTIONS.md
REVIEW-AUTHORIZATION.md
CODEX-RESPONSE.md
PLAN-AND-CONTINUITY.md
CUTOVER-DIFF.patch
CHANGED-FILES.txt
SOURCE-HASHES.txt
LOCAL-GATES.txt
DEPLOYMENT.md
LIVE-VERIFICATION.md
CACHE-WINDOW.md
ROLLBACK.md
checks.txt
MANIFEST.sha256

Also include:

    exact pre-cutover and cutover SHAs;

    exact Pages run;

    canonical browser JSON;

    canonical screenshots;

    accepted-candidate/oracle comparison evidence;

    why/territorial/stable-key evidence;

    indexing evidence;

    deployed byte-parity evidence;

    immediate and post-window checks.

Generate MANIFEST.sha256 last.

Verify:

sha256sum -c MANIFEST.sha256
unzip -t <zip>
# exactly one top-level directory
sha256sum <zip>

Push the sealed artifacts and final continuity checkpoint.

Require:

clean worktree
HEAD == main == origin/main == remote main

HARD STOP

After the execution handoff is durably pushed:

STOP FOR INDEPENDENT PUBLIC-CUTOVER ACCEPTANCE.

Do not:

    delete day-reader.html or propers-reader.html;

    remove the visual-reset oracle;

    alter navigation;

    perform cleanup;

    start search;

    add source/translation content;

    redesign the reader.

Final post-deployment review questions

The next reviewer should answer only:

    Are canonical Day and Propers now serving the accepted Liturgical Instrument?

    Are canonical URLs and all accepted public state contracts preserved?

    Is live visual output materially identical to the accepted candidate/oracle?

    Are canonical pages indexable while candidate/oracle routes remain nonindexable?

    Is the exact cutover SHA the successfully deployed Pages SHA?

    Do deployed bytes match the intended cutover?

    Did both immediate and post-cache-window checks pass?

    Did public navigation remain unchanged and fallback candidate/oracle routes remain intact?

    May the public cutover be accepted and marked complete?

Only that review may close the cutover.
Authorization boundary

    Gate repair: ACCEPTED

    Corrected patch SHA ce43cef...: ACCEPTED

    Old patch SHA cd11518...: REJECTED / DO NOT EXECUTE

    Corrected same-path cutover execution: AUTHORIZED

    Exact 19-path promoted product/test/release change: AUTHORIZED

    Exact-SHA public Pages deployment after local gates: AUTHORIZED

    Immediate/post-cache-window live verification: AUTHORIZED

    Ordinary rollback on material failure: AUTHORIZED

    Final public-cutover acceptance: PENDING POST-DEPLOYMENT REVIEW

    Public navigation changes: UNAUTHORIZED

    Candidate/oracle cleanup: UNAUTHORIZED

    Visual/product redesign: UNAUTHORIZED

    State/renderer/source/translation expansion: UNAUTHORIZED

## Public-cutover execution retry — Codex response

Execution retry begins at synchronized starting SHA
`6bb0d02e50794b1cfe89faa5424e6eea42e55872`. Before this continuity append,
the worktree was clean and `HEAD`, local `main`, `origin/main`, and remote
`refs/heads/main` all agreed at that SHA.

The canonical replacement patch at
`build/agent-continuity/liturgy-reader-public-cutover-proposed.patch` has the
accepted SHA-256
`ce43cef0621e3e1bdf6eb53eb4ce62e479e54977bd739a26385068bcaa33b0e5`.
The gate-repair baseline ancestor check against
`e20b2f542ab51a2b4f0807e6394ca5ecb313699c` exited 0, and normal-context
`git apply --check` exited 0. No `--3way`, fuzz, regeneration, or manual
reconstruction will be used.

All nine gate-repair dispositions are recorded as accepted: the repairs are at
the test/harness boundary; scope is exactly 19 paths; accepted prospective
product/release bytes are unchanged; focused locked Python passes; all four
browser gates pass; repaired assertions remain strong; mechanical application
passed and was rechecked at this execution boundary; real canonical readers
remained unchanged and undeployed during repair; and entry into the bounded
execution/deployment/cache protocol is authorized.

The intended sequence is exact: append this continuity record; apply only the
accepted patch; verify the three frozen product/release hashes and exact scope;
run the complete real-tree canonical gate; create and push one bounded cutover
commit; require Pages success for that exact cutover SHA; run immediate live
canonical and byte-parity verification; wait beyond the observed cache window
and repeat the required non-cache-busted checks; then seal and push the execution
handoff and stop for independent public-cutover acceptance.

Any cutover-owned failure before commit triggers reversal of the uncommitted
application and review. Any material post-push canonical failure or uncertain
mixed deployment triggers an ordinary `git revert <CUTOVER_COMMIT>` followed by
push, exact-revert-SHA Pages success, restored-route verification, and immediate
and post-freshness checks; history will not be rewritten.

Public navigation changes and candidate/oracle cleanup remain forbidden.
Visual/product redesign, renderer/state refactoring, Ordinary changes,
source/translation expansion, and unrelated cleanup likewise remain outside
this execution authorization.

### Real-tree canonical pre-deployment checkpoint

The corrected patch was applied without regeneration or hand editing. Its
effect is exactly the accepted 19 paths plus this append-only continuity file.
The promoted source hashes are unchanged from the independently accepted
prospective values: Day `9a119a6aa87e900d6fc4c3e236191fe8a036abc305236eb576c09f823c7b7972`,
Propers `a6527316266365b79ff2ecdc193da3ab1034b1daa63408b869b192d2aeb85600`,
and the rights record
`5a4b4d4f8bfbcf8d5fd54249c0d8664be7215b4bee9e82ccc8a37f400e3cf31e`.

The actual promoted working tree passes locked focused Python 230/230; Day
Chromium 40/40; Propers Chromium 32/32; shared-shell Chromium 18/18; governed
Instrument Chromium 24/24; syntax checks for all changed Python and JavaScript
tests; promised-deliverables and tool registries; release bindings with zero
stale entries; `git diff --check`; and locked public-alpha policy, build, and
GitHub-Pages-target verification. The governed Instrument run initially found
the expected pre-cutover generated preview still on disk; after the required
locked preview build and verification, the same unmodified harness passed
24/24 against the promoted canonical filenames.

The governed full `make check` remains honestly non-green at `check-examples`
with exit 2. It replayed 200 captured examples, ran 188, and reported 21
divergences, 35 known-stale cases, six deliberately unrun network/mutating
examples, and six unavailable built-artifact examples. This is the already
disclosed unrelated stored-example transcript divergence; no transcript was
recaptured or blessed. No task-owned gate failed.

The next exact action is to commit and push this bounded cutover, then accept
only a successful Pages run whose source SHA equals that cutover commit. Public
navigation and retained candidate/oracle bytes remain outside the change.

### Exact-SHA deployment and immediate live checkpoint

Commit `9b5f21c0ca26bf02af03d207ddd2617021e16fb3` pushed the exact accepted
19-path promotion plus continuity. GitHub Pages run `31175722949` names that
exact source SHA and completed successfully; every build, verification, upload,
and deploy step passed. Earlier continuity and handoff runs remain explicitly
nonqualifying.

The immediate cache-bypassed live verifier completed at
`2026-08-07T12:16:10.158Z`: 936/936 assertions across 36 original-pixel states,
with zero console, required-request, HTTP, unnamed-control, duplicate-ID, or
required-overflow problem. It proves canonical HTTP 200/no-redirect behavior,
indexing metadata, empty-Day Roman 1962 default, Read/Missal, deep links,
why=1, two held territorial branches, Propers public option keys, fail-closed
alternative state, Details links, accessibility/reflow states, reload and
Back/Forward, retained candidate/oracle full noindex, and byte parity for 15
deployed HTML/JS/CSS assets against the locked build.

The governed original-pixel evidence is also green: Day 40/40 with 77 captures;
Propers 32/32; shared shell 18/18 with 94 captures; Instrument 24/24 with 113
captures. The immediate matrix was visually inspected as a labeled sheet and at
full size for the portrait Read measure, 200% dock, territorial branch, and
mobile Details states; no filename-change visual regression is visible.

The verifier enforces at least 601 seconds after the immediate completion before
the post-window pass. That pass may not begin before
`2026-08-07T12:26:11Z`. No rollback trigger has fired.

### Post-freshness-window checkpoint

The required ordinary-cache pass began after 613 elapsed seconds and completed
at `2026-08-07T12:26:32.943Z`: 216/216 assertions across the six required
canonical states, with zero console, request, HTTP, accessibility-name,
duplicate-ID, or overflow problem. It used a fresh Chrome profile, plain URLs,
normal cache behavior, and no cache-busting query or headers. Canonical default,
deep link, Missal, Propers deep link, Details, and territorial Why all settled;
all 15 checked deployed assets remained HTTP 200, unredirected, and byte-equal
to the locked build. No mixed-generation behavior appeared, and the ordinary
rollback trigger did not fire.

The exact execution handoff is
`build/agent-handoffs/20260807T115341Z-liturgy-reader-instrument-public-cutover-execution/`
with a matching ZIP to be sealed. The cutover remains pending independent
post-deployment acceptance; public navigation redesign, candidate/oracle
cleanup, and all other excluded work remain unauthorized.

### Immutable execution handoff seal

The new handoff contains 441 payload files and `MANIFEST.sha256`; all 441
manifest entries verify. The ZIP contains 462 entries including directories,
passes `unzip -t`, and has exactly one top-level directory. Its SHA-256 is
`06752126a3a3235a342f54ec08811faaf4fc2622924008c4362dda519624c410`.

At sealing, `PLAN-AND-CONTINUITY.md` byte-matched this canonical file at
SHA-256 `3259be77a04f2871ec07dbb250c2b2d362bc5f6e25c6a55eff58f51a0e43311d`.
`INSTRUCTIONS.md` and `REVIEW-AUTHORIZATION.md` are byte-identical at SHA-256
`7a3dac46eb8a85ccdacaa1403e3fe17ccec547a03a4e095180c5e74e2e1c23de`.
This post-seal paragraph necessarily succeeds the immutable continuity snapshot
so that the canonical record can name the finalized ZIP hash; the package is
not rebuilt around its own transport hash.

The next reviewer should begin with the latest handoff and answer only the nine
questions in `REVIEW_REQUEST.md`. Visibly, canonical Day and Propers now match
the accepted Instrument candidate/oracle at desktop, intermediate, mobile, and
accessibility states. Provisionally, the cutover remains unaccepted until that
review. The requested decisions are exact route/state preservation, live visual
parity, indexing boundaries, exact-SHA deployment, deployed-byte parity, both
cache passes, unchanged navigation/fallbacks, and whether the cutover may close.

### Durable push and archival Pages checkpoint

Commit `1d60b49bcf2a46e5ee43d6326af3e13a43265b72` pushed the exact immutable
execution-handoff directory, its verified ZIP, and the post-seal continuity
record. GitHub Pages run `31178547337` for that exact handoff-only commit
completed successfully at `2026-08-07T12:33:52Z`; every build, artifact,
verification, upload, and deploy step passed. That run changed no reader product
bytes and is not the qualifying public-cutover deployment. The qualifying run
remains `31175722949` for exact cutover commit
`9b5f21c0ca26bf02af03d207ddd2617021e16fb3`.

The durable archive paths are
`build/agent-handoffs/20260807T115341Z-liturgy-reader-instrument-public-cutover-execution/`
and
`build/agent-handoffs/20260807T115341Z-liturgy-reader-instrument-public-cutover-execution.zip`.
The ZIP SHA-256 remains
`06752126a3a3235a342f54ec08811faaf4fc2622924008c4362dda519624c410`;
its 441 manifest payloads, one-top-level-directory shape, and transport integrity
were verified before push. No rollback trigger fired.

This is the final Codex execution checkpoint. The next exact action is independent
public-cutover acceptance review from the immutable handoff. The cutover must not
be marked accepted or complete before that disposition. Public navigation remains
unchanged; candidate and oracle fallbacks remain intact and nonindexable; cleanup,
redesign, search, and source/translation expansion remain unauthorized.


## Independent public-cutover acceptance — reviewer to Codex

Liturgical Instrument — Final Public-Cutover Acceptance
Disposition

PUBLIC CUTOVER ACCEPTED.

The same-path promotion of the accepted Liturgical Instrument readers onto the
canonical public Day and Propers URLs is independently accepted and may be
marked complete.

The cutover is no longer a candidate.

No rollback is required.

No remaining cutover blocker exists.

This acceptance closes the visual-reset → correction → production-integration →
compatibility → gate-repair → canonical-cutover sequence.

It does not authorize:

    candidate/oracle deletion;

    public-navigation redesign;

    search work;

    source or translation expansion;

    Ordinary or renderer refactoring;

    a new visual redesign under the guise of cleanup.

After the archival closeout below, further reader work should begin as a new
production phase against the live canonical Day and Propers pages.
Reviewed execution package

Reviewed archive:

20260807T115341Z-liturgy-reader-instrument-public-cutover-execution.zip

Independent package verification:

    ZIP integrity: PASS

    top-level directories: exactly one

    total ZIP entries: 462

    MANIFEST.sha256: 441/441 payload entries PASS

    files in the extracted handoff including MANIFEST.sha256: 442

    independently calculated uploaded ZIP SHA-256:

06752126a3a3235a342f54ec08811faaf4fc2622924008c4362dda519624c410

The immutable execution handoff is also present in the repository build tree:

build/agent-handoffs/20260807T115341Z-liturgy-reader-instrument-public-cutover-execution/
build/agent-handoffs/20260807T115341Z-liturgy-reader-instrument-public-cutover-execution.zip

Accepted deployment boundary

Pre-cutover SHA:

6bb0d02e50794b1cfe89faa5424e6eea42e55872

Accepted public-cutover SHA:

9b5f21c0ca26bf02af03d207ddd2617021e16fb3

Qualifying GitHub Pages run:

31175722949

The run is a success for the exact cutover SHA.

Earlier compatibility, continuity, handoff, and gate-repair Pages runs remain
nonqualifying as cutover evidence.
Nine final review dispositions
1. Are canonical Day and Propers serving the accepted Liturgical Instrument?

PASS

The canonical filenames are now the accepted production readers:

/liturgy/day.html
/liturgy/index.html

There is no redirect to day-reader.html or propers-reader.html.

The reviewed live evidence shows the accepted Liturgical Instrument composition
at the canonical filenames across Day Read, Day Missal, Propers Read, Browse,
desktop, intermediate, portrait-tablet, mobile, accessibility/reflow, modal,
deep-scroll, partial-coverage, postconciliar, Why, and territorial states.

The independently inspected live screenshots retain:

    the accepted Triptych masthead;

    one-axis Read composition;

    1440 external control rail;

    square opaque edge dock on mobile/intermediate;

    200% deliberate reflow;

    accepted Missal cue/ritual composition;

    compact warning hierarchy;

    canonical Propers Browse entrance.

No filename-promotion visual regression is visible.
2. Are canonical URLs and accepted public state contracts preserved?

PASS

The live verifier passes the canonical Day and Propers paths with no redirect and
the exact requested hashes.

Accepted public behavior is present for:
Day

    empty route;

    local civil-date behavior;

    Roman 1962 public default;

    explicit date;

    Roman 1962;

    postconciliar;

    Bible/oration state;

    Read/Missal;

    reload;

    direct deep links;

    Back/Forward;

    partial coverage;

    why=1;

    multiple held territorial branches;

    modal/surface interaction;

    accessibility/reflow states.

Propers

    existing canonical seasonal deep link;

    canonical Browse;

    stable cycle;

    stable translation-witness;

    stable explicit alternative state with honest fail-closed behavior where no
    selectable stable alternative exists;

    reload;

    Back/Forward;

    direct links;

    route-owned Details/context navigation.

The required governing links remain valid in the evidence:

/liturgy/day.html#date=2026-08-05&missal=roman-1962&bible=douay-rheims

/liturgy/index.html#missal=roman-1962&type=seasonal&mass=advent-1&bible=douay-rheims

No accepted public-contract blocker remains.
3. Is live visual output materially identical to the accepted candidate/oracle?

PASS

The governed visual run reports:

24/24 assertions
113 captures

The canonical/candidate/oracle parity evidence remains green.

The independent visual inspection included:

    immediate live contact sheet;

    post-window contact sheet;

    canonical Day Read 1440×900;

    canonical Day Missal 393×852;

    canonical Day Why/mobile;

    canonical territorial/mobile;

    canonical Propers Read/mobile;

    governing shell/accessibility states.

The canonical output belongs to the same accepted Instrument system. No cutover
artifact, legacy shell, transient route chrome, changed reading measure, broken
dock, or reverted warning hierarchy appears.
4. Are canonical pages indexable while candidate/oracle routes remain nonindexable?

PASS

The canonical Day and Propers sources contain no static robots=noindex
directive.

The live verifier explicitly passes:

canonical page is indexable
canonical Open Graph URL is route-correct

for canonical states.

The retained surfaces are separately verified as:

day-reader.html
propers-reader.html
reader-visual-reset-day.html
reader-visual-reset-propers.html

with:

noindex, nofollow, noarchive, nosnippet, noimageindex

and no public Open Graph URL.

This is the correct initial post-cutover indexing boundary.
5. Is the exact cutover SHA the successfully deployed Pages SHA?

PASS

Cutover:

9b5f21c0ca26bf02af03d207ddd2617021e16fb3

Pages run:

31175722949

The workflow is recorded as Success for that exact pushed SHA, with build,
artifact upload, and deploy completed.

No earlier successful run is being substituted.
6. Do deployed bytes match the intended cutover?

PASS

The independently rehashed source snapshots match the already accepted
prospective product/release values:

src/web/browser/liturgy/day.html
9a119a6aa87e900d6fc4c3e236191fe8a036abc305236eb576c09f823c7b7972

src/web/browser/liturgy/index.html
a6527316266365b79ff2ecdc193da3ab1034b1daa63408b869b192d2aeb85600

release/rights/public-alpha-2026-07-15.md
5a4b4d4f8bfbcf8d5fd54249c0d8664be7215b4bee9e82ccc8a37f400e3cf31e

The execution diff contains exactly the accepted 19 patch paths.

The immediate and post-window evidence both report 15/15 deployed assets
byte-identical to the locked public-alpha build, including canonical pages,
candidate/oracle pages, reader controllers, state/adapters, shell assets, and
Instrument CSS.

No deployed/source parity blocker remains.
7. Did immediate and post-cache-window checks pass?

PASS
Immediate live pass

Completed:

2026-08-07T12:16:10.158Z

Result:

936/936 assertions
36 original-pixel screenshots
0 console problems
0 required failed requests
0 HTTP problems
0 unnamed controls
0 duplicate IDs
0 required horizontal overflow

Post-freshness-window pass

The verifier refused to begin before the required window and started after:

613 seconds

Completed:

2026-08-07T12:26:32.943Z

Result:

216/216 assertions
6 governing screenshots
0 console problems
0 required failed requests
0 HTTP problems
0 accessibility-name problems
0 duplicate IDs
0 required horizontal overflow

It used ordinary cache behavior with no cache-busting query or headers.

No mixed-generation behavior appeared.

The rollback trigger did not fire.

This satisfies the static GitHub Pages mixed-cache gate.
8. Did public navigation remain unchanged and fallback surfaces remain intact?

PASS

The accepted cutover diff does not include repository-owned public-navigation
files.

The existing top-level public links continue to target the same canonical Day
and Propers URLs, which is the principal benefit of same-path promotion.

The candidate and visual-oracle routes remain present, HTTP-tested in the live
evidence, and full-noindex.

No cleanup was folded into cutover.

This is the correct rollback/acceptance posture.
9. May the public cutover be accepted and marked complete?

YES — PASS.

The public cutover is independently accepted.

The deliverable may now be recorded as complete.
Validation disposition

Accepted task-owned local gates:

focused locked Python:       230/230
Day Chromium:                40/40
Propers Chromium:            32/32
shared shell:                18/18
governed Instrument:         24/24
changed syntax:              PASS
promised-deliverables:       PASS
tool registry:               PASS
release bindings:            0 stale
git diff --check:            PASS
public-alpha check:          PASS
public-alpha build:          PASS
public-alpha GitHub Pages
verification:                PASS

The governed full repository check remains honestly non-green only at the
previously disclosed unrelated stored-example transcript replay.

No transcript should be recaptured or blessed as part of cutover acceptance.

That unrelated repository condition does not block this task-owned cutover
acceptance.
Reviewer note on independent live observation

The review environment's generic web text crawler currently exposes a cached
pre-cutover parse of the canonical Day/Propers HTML and labels that parse as
having been crawled before this cutover deployment.

It is therefore not suitable as the authority for the post-cutover JavaScript
reader state.

This acceptance instead rests on:

    independent verification of the sealed package and manifest;

    independent inspection of the original-pixel immediate/post-window evidence;

    independent parsing of the live-verifier results;

    independent rehashing of the sealed source snapshots;

    independent confirmation of the exact GitHub cutover commit and successful
    exact-SHA Pages run;

    the package's fresh-Chrome immediate and ordinary-cache post-window browser
    verification, which includes direct HTTP/source parity.

The stale crawler snapshot is not interpreted as a contradictory live result.
Archival acceptance closeout — authorized

Codex may now perform one non-product closeout.

No product byte needs to change.
AC-A — Append final reviewer acceptance

Append this complete review under:

## Independent public-cutover acceptance — reviewer to Codex

in:

build/agent-continuity/liturgy-reader-visual-plan.md

Immediately append:

## Public-cutover acceptance closeout — Codex response

Record:

    all nine final dispositions as PASS;

    accepted cutover SHA 9b5f21c0ca26bf02af03d207ddd2617021e16fb3;

    qualifying Pages run 31175722949;

    execution handoff path;

    execution ZIP SHA-256
    06752126a3a3235a342f54ec08811faaf4fc2622924008c4362dda519624c410;

    immediate 936/936;

    post-window 216/216;

    final cutover state: accepted/complete;

    unrelated example-transcript qualification;

    confirmation that candidate/oracle cleanup and navigation redesign remain
    outside this acceptance.
AC-B — Close tracking truthfully

Update only the necessary tracking/roadmap records so they state:

Liturgical Instrument production integration: accepted and complete
Compatibility closure: accepted and complete
Public cutover: independently accepted and complete
Canonical Day/Propers: accepted Liturgical Instrument
Public navigation redesign: not part of cutover
Candidate/oracle cleanup: deferred

Mark the existing public-cutover promised deliverable complete.

Do not invent a new product deliverable merely for archival acceptance.

Preserve the unrelated full-repository example replay qualification.
AC-C — Preserve this review durably

Track this review as:

build/agent-continuity/liturgy-reader-public-cutover-final-acceptance.md

The bytes should be identical to this supplied review artifact.

The existing execution handoff remains immutable. Do not rewrite it merely to
insert the acceptance that occurred after sealing.

For the maintainer's clean-agent continuity requirement, create a small
acceptance-closeout handoff, not another copy of the 43 MB execution evidence:

build/agent-handoffs/<UTC>-liturgy-reader-instrument-public-cutover-acceptance/
build/agent-handoffs/<UTC>-liturgy-reader-instrument-public-cutover-acceptance.zip

Include only:

START-HERE.md
FINAL-ACCEPTANCE.md
CODEX-RESPONSE.md
PLAN-AND-CONTINUITY.md
TRACKING-DIFF.patch
EXECUTION-HANDOFF-REFERENCE.md
MANIFEST.sha256

EXECUTION-HANDOFF-REFERENCE.md must point to the already-pushed immutable
execution handoff and record:

cutover SHA
Pages run
execution handoff directory
execution ZIP name/hash
execution MANIFEST result
immediate/post-window result

Do not duplicate screenshots/browser payloads into this closeout package.

The maintainer's continuity policy authorizes force-adding only this exact new
acceptance-closeout directory and its matching ZIP if ignore rules require it.
AC-D — Closeout checks

Require:

    product/evidence byte changes: zero

    canonical Day source hash remains the accepted value

    canonical Propers source hash remains the accepted value

    candidate/oracle bytes unchanged

    public-navigation bytes unchanged

    continuity contains reviewer acceptance + Codex response

    tracking truthfully marks cutover complete

    promised-deliverables registry passes

    release bindings remain current

    git diff --check passes

Generate the closeout manifest last.

Verify:

sha256sum -c MANIFEST.sha256
unzip -t <acceptance-closeout.zip>
# exactly one top-level directory
sha256sum <acceptance-closeout.zip>

Commit and push.

If that documentation-only push triggers Pages, record the run honestly as a
post-acceptance documentation deployment. Do not replace 31175722949 as the
qualifying cutover run.

Require a clean final worktree and:

HEAD == main == origin/main == remote main

No additional independent visual review is required for this archival closeout
if product/evidence/public-navigation bytes remain unchanged.
What comes after closeout

Do not make candidate/oracle cleanup the automatic next development phase.

The reason those surfaces still exist is useful: they provide a known-good
fallback and a visual regression oracle while the newly canonical reader gains
real use.

The next substantive reader phase should start from the live canonical pages and
ask what would make the reading experience materially better now that migration
mechanics are finished.

That phase should be separately planned and may consider such things as:

    deeper first-viewport and long-reading polish;

    ritual navigation and orientation during a long Missal;

    typography and spacing refinements revealed by real content;

    richer but still subordinate source/apparatus interaction;

    handling of unusually long or unusual liturgical structures;

    production accessibility refinement;

    eventual search/study capabilities only if they strengthen rather than clutter
    the reading instrument.

No item in that list is authorized by this acceptance itself.
Final state

    Liturgical Instrument visual direction: ACCEPTED

    Responsive correction: ACCEPTED

    Production integration: ACCEPTED

    Compatibility closure: ACCEPTED

    Cutover gate repair: ACCEPTED

    Canonical Day public cutover: ACCEPTED

    Canonical Propers public cutover: ACCEPTED

    Public cutover overall: COMPLETE

    Rollback: NOT REQUIRED

    Public navigation redesign: NOT AUTHORIZED

    Candidate/oracle cleanup: DEFERRED / NOT AUTHORIZED

    Next product/visual phase: SEPARATE FUTURE AUTHORIZATION

## Public-cutover acceptance closeout — Codex response

All nine final review dispositions pass. The independent reviewer accepted the
canonical Day and Propers readers, URL and state contracts, live visual parity,
indexing boundary, exact-SHA Pages deployment, deployed-byte parity, immediate
and post-freshness verification, unchanged public navigation and retained
fallback surfaces, and final completion of the public cutover.

The accepted cutover SHA is
`9b5f21c0ca26bf02af03d207ddd2617021e16fb3`; qualifying GitHub Pages run
`31175722949` succeeded for that exact SHA. The immutable execution handoff is
`build/agent-handoffs/20260807T115341Z-liturgy-reader-instrument-public-cutover-execution/`,
and its matching ZIP SHA-256 is
`06752126a3a3235a342f54ec08811faaf4fc2622924008c4362dda519624c410`.
The immediate live pass is 936/936 across 36 original-pixel states, and the
ordinary-cache post-window pass is 216/216 across six governing states after
613 seconds.

The Liturgical Instrument visual direction, responsive correction, production
integration, compatibility closure, gate repair, canonical Day cutover,
canonical Propers cutover, and overall public cutover are accepted and complete.
No rollback is required. The unrelated governed full repository check remains
honestly non-green only at the previously disclosed stored-example transcript
replay; no transcript was recaptured or blessed.

This acceptance changes no product, evidence, candidate, oracle, public
navigation, source, renderer, Ordinary, or translation byte. Candidate/oracle
cleanup remains deferred and unauthorized, and public-navigation redesign
remains outside this acceptance. Any further reader work begins as a separately
authorized production phase against the live canonical pages.

### Acceptance tracking and immutable closeout checkpoint

Commit `96b371a8ae4f8af3eefff792462e7222ce17f887` pushes the verbatim final
acceptance, its append-only continuity exchange, and truthful updates to
`PROJECT-WORK.md`, `guidance/liturgy-browser-roadmap.md`, and
`promised-deliverables.toml`. The existing public-cutover deliverable is
complete: both prior review requirements pass and the added final-acceptance
requirement records exact-SHA deployment and both live cache gates. GitHub
Pages run `31180924173` succeeded for that exact documentation-only commit at
`2026-08-07T13:06:11Z`. It changes no reader bytes and does not supersede
qualifying cutover run `31175722949`.

The small archival closeout is
`build/agent-handoffs/20260807T130403Z-liturgy-reader-instrument-public-cutover-acceptance/`
with matching ZIP
`build/agent-handoffs/20260807T130403Z-liturgy-reader-instrument-public-cutover-acceptance.zip`.
Its six manifest payloads verify, the ZIP contains eight entries including its
single top-level directory, `unzip -t` passes, and ZIP SHA-256 is
`98b21deb273de839db77c49f2cb92eef54aa66f8f8ee4dad0dbde49105932173`.
At sealing, `PLAN-AND-CONTINUITY.md` byte-matched the canonical continuity file
at SHA-256
`010f55def6042fab6889cb947f3701f0054f9abe49e4a165d25cb8e1397f3e0e`;
`FINAL-ACCEPTANCE.md` byte-matched the tracked verbatim review at SHA-256
`fbfda03948f7e0c426fa1cd2ff6766864e96cc199bf96bb112fdccbb40e605e9`.
This paragraph necessarily follows the immutable snapshot so the canonical
record can name the transport hash; the package is not rebuilt around its own
ZIP hash.

The final closeout changes zero product, execution-evidence, candidate/oracle,
or public-navigation bytes. The next exact action after the archive push is no
automatic cleanup phase: further reader work requires separate authorization
against the live canonical pages.

### Acceptance archive pre-commit correction and final seal

The preceding `20260807T130403Z` package statement is superseded before any
commit or push. The staged whitespace audit found that its ordinary-context
`TRACKING-DIFF.patch` necessarily carried patch context-prefix spaces that made
the staged whitespace check noisy. That unpushed local directory and ZIP were
removed; no corresponding Git object or public artifact exists. No product,
tracking, acceptance, or evidence byte was changed to resolve the packaging
defect.

The fresh immutable closeout is
`build/agent-handoffs/20260807T130808Z-liturgy-reader-instrument-public-cutover-acceptance/`
with matching ZIP
`build/agent-handoffs/20260807T130808Z-liturgy-reader-instrument-public-cutover-acceptance.zip`.
It uses the same exact focused tracking diff in zero-context form. All six
manifest payloads verify; `unzip -t` passes; the ZIP contains eight entries
including exactly one top-level directory; and the final ZIP SHA-256 is
`d44843a2a90971816e7fa35bb49b3e6b44b649edf35231c459709db8788901a4`.
At the final seal, `PLAN-AND-CONTINUITY.md` byte-matched the canonical record
at SHA-256
`571c1fbb4051eb6bb1ab8dd084e58904e75c488de59790dac5f92c4d045f9b33`,
and `FINAL-ACCEPTANCE.md` still byte-matched the tracked reviewer artifact at
SHA-256
`fbfda03948f7e0c426fa1cd2ff6766864e96cc199bf96bb112fdccbb40e605e9`.
This post-seal correction necessarily follows the package snapshot so the
canonical record can name its transport hash; the package remains immutable.

### Final acceptance archive push

Commit `e647d1ababdc399da7296dfb6b87cd2b8e90e8e4` pushes exactly the final
acceptance-closeout directory, matching ZIP, and append-only post-seal
continuity record. GitHub Pages run `31181413147` succeeded for that exact
commit; every source verification, public build, artifact verification, upload,
and deploy step passed. This is a post-acceptance documentation deployment, not
new product or cutover evidence. Qualifying cutover deployment remains run
`31175722949` for `9b5f21c0ca26bf02af03d207ddd2617021e16fb3`.

The cutover sequence is closed. No rollback or further acceptance review is
required. The next agent should begin from the live canonical readers and must
obtain separate authority for any substantive phase; candidate/oracle cleanup
and public-navigation redesign remain unauthorized.

## Live ritual-flow phase — reviewer to Codex

The migration/cutover sequence is finished. Begin a new production phase,
**Live Reader — Ritual Flow & Orientation**, from clean synchronized commit
`1bca6a0ee862fce5873d6b0c2d92389e78ca018b`, against canonical
`/liturgy/day.html` and `/liturgy/index.html`. The accepted first viewport and
Liturgical Instrument foundation are protected. The problem is sustained
reading: once identity and headings scroll away, the reader must retain a quiet
source-owned answer to “where am I,” Contents must open as a live map, and
principal ritual action must remain visually stronger than rubric,
provenance, and conditional/reference apparatus without dashboard chrome.

The phase is bounded to RF-A through RF-E: capture a focused live/canonical
baseline and map actual semantic ownership; integrate a persistent semantic
locus with the existing rail/dock; place the current accessible Contents row
into view on open; refine only classifications already proved by production
state; then tune long-form desktop/mobile typography while measuring the
accepted first viewport and 636-pixel Read measure. Required evidence spans
Roman and postconciliar Day top/deep/Ordinary states, Day and Propers Read,
Contents at beginning/middle/end/mobile/200%, why, territorial, partial
coverage, accessibility states, 320-pixel mobile, and governing first-view
regressions. Measurements must include locus and dock geometry, zero obscured
text, current-row position, semantic state, block classes, focus/targets,
overflow, and browser/network errors; every original must be inspected at full
size.

Orientation must use existing semantic-location ownership rather than scroll
percentage and must not flicker, become stale across render/mode/date/history,
change the URL, cover text, add a fifth primary action, or generate aria-live
noise. Contents retains grouping, focus restoration, Escape and inert behavior.
No CSS/JavaScript rule may infer liturgical applicability. Positively current
material remains principal; positively reference/non-current material may be
subordinate; unresolved conditional material remains explicitly available;
unknown material remains visible and is recorded. Search, Study, Compare,
print redesign, source/translation/recension/corpus expansion, navigation
redesign, candidate/oracle cleanup, and another visual direction are excluded.

Create deliverable `liturgy-reader-live-ritual-flow-2026-08-07`, preserve the
cutover record, extend governed browser evidence, run every accepted focused,
browser, release, public-alpha and whitespace gate, verify pushed Pages and the
live routes, then seal a fresh immutable
`<UTC>-liturgy-reader-live-ritual-flow` directory and ZIP. Stop for independent
review of deep orientation, Instrument coherence, Contents mapping, ritual
hierarchy, inference/source honesty, desktop/mobile calm, cross-route coherence,
and protected first-view/accessibility/state behavior. Do not continue into a
later phase automatically.

## Live ritual-flow phase — Codex response

The synchronized starting SHA is
`1bca6a0ee862fce5873d6b0c2d92389e78ca018b`; `HEAD`, local `main`,
`origin/main`, and remote `refs/heads/main` agree, and the starting worktree is
clean. Canonical source hashes are Day
`9a119a6aa87e900d6fc4c3e236191fe8a036abc305236eb576c09f823c7b7972`
and Propers
`a6527316266365b79ff2ecdc193da3ab1034b1daa63408b869b192d2aeb85600`.

Initial ownership inspection finds:

- `src/web/browser/liturgy/reader-shell.js` owns current semantic location,
  the one `aria-current="location"` Contents row, scroll/resize coalescing,
  surface focus/inert/Escape behavior, and semantic restoration.
- `src/web/browser/liturgy/day-reader.js` maps production Proper and Ordinary
  events into semantic nodes and Contents groups; it uses production assembly,
  Ordinary seating and the shared renderer rather than owning liturgical
  selection.
- `src/web/browser/liturgy/propers-reader.js` maps production Proper events and
  their source-owned labels into the Propers outline.
- the production Ordinary renderer's existing classes distinguish proved
  rubrics and selected source-defined choices; `day-reader.js` owns the
  already-accepted source-derived why and territorial presentation hooks.
- `src/web/browser/liturgy/reader-shell.css` owns generic shell/surface
  interaction geometry, while `src/web/browser/liturgy/reader-instrument.css`
  is the final accepted rail/dock, reading-plane, mobile identity, Ordinary,
  Proper, warning, and accessibility presentation layer.
- canonical HTML supplies route identity and mobile metadata; the controllers
  update committed mode/outcome wording from existing state.

Work unit RF-A will extend the governed capture path, preserve an original-pixel
pre-change baseline, and finish the exact DOM/data classification inventory.
RF-B will expose a quiet locus from the shell's already-current outline entry,
using only source-owned group/label values and the existing stable animation-
frame boundary. RF-C will keep the accessible current row and place it near the
useful center of Contents on open with nonanimated scrolling. RF-D will style
only already-proved rubric, provenance, selected-option, and conditional/
reference hooks; unknown blocks remain visible. RF-E will tune sustained rhythm
only after those behaviors settle and will remeasure protected top geometry.

The requested “current unit” cannot be safely named for every Ordinary element
today: the outline currently holds source-named divisions and appointed
Propers, while some individual elements expose only internal keys. Likewise,
not every long alternative-looking block carries a proved non-current flag.
Neither gap will be filled by inference. This phase will use a source-owned
public element label only where production already holds one, otherwise retain
the current division, and will conservatively keep unknown material visible.

The initial evidence baseline is the accepted cutover package plus a new
same-run RF-A capture from the canonical routes; its matrix and protected
measurements are recorded in
`build/agent-continuity/liturgy-reader-ritual-flow-baseline.md`. The first
bounded implementation checkpoint is baseline, semantic inventory, harness
extensions, continuity and truthful tracking only; the first product checkpoint
will then pair persistent orientation with current-map Contents and its focused
evidence. No public navigation, candidate/oracle cleanup, source selection,
renderer ownership, or invented liturgical inference is included.

## Live ritual-flow emergency takeover checkpoint — Codex to next agent

Recorded at `2026-08-07T14:33:26Z` because the maintainer needed to shut down.
This is deliberately a resumable work-in-progress checkpoint, not a visual
acceptance request and not a claim that RF-B through RF-E are complete.

Completed and present in this checkpoint:

- RF-A is documented in
  `build/agent-continuity/liturgy-reader-ritual-flow-baseline.md` and
  `build/agent-continuity/liturgy-reader-ritual-flow-semantics.md`.
  The authoritative pre-change capture is the ignored local directory
  `build/agent-continuity/liturgy-reader-ritual-flow-baseline-captures-v4/`:
  61 original-pixel captures, governed assertions 24/24, and no recorded
  console, request, HTTP, unnamed-control, duplicate-ID, or overflow problems.
- Canonical and retained candidate HTML now carry one static, aria-hidden locus
  hook. Day and Propers controllers expose only source-owned division, Proper,
  Ordinary element, seating-anchor, and territorial labels. No percentage or
  applicability inference was added.
- `reader-shell.js` derives the persistent locus at the same stable reading
  boundary used by semantic location. It chooses the geometrically nearest
  source-owned locus above the boundary, avoiding DOM-order errors introduced
  by Ordinary seating. The locus hides while identity or its major division
  heading is visible and simplifies to the major division while the current
  unit heading is visible. It has no live region and no URL ownership.
- Contents keeps the existing `aria-current="location"` row and now scrolls the
  actual `.surface-body` owner so that row is centered where possible and
  clamped visibly near either list end. Focus entry, Escape, inertness, and
  document scroll restoration remain on the existing shell path.
- `reader-instrument.css` integrates the wide locus as ruled marginalia above
  the accepted rail and uses the existing compact masthead line on mobile. It
  also quiets proved rubric cue labels and existing source/apparatus notes. The
  global rubric typography was intentionally restored after it moved accepted
  first-viewport geometry.
- The governed visual harness has a dedicated `--ritual-flow-dir` profile,
  semantic-location capture, locus and Contents geometry, hierarchy counts,
  per-capture error deltas, and the 61-state required matrix. Focused static
  Python integration tests passed 49/49. A governed non-capture run passed
  25/25 with zero console/request/HTTP problems before the last small
  major-only simplification.
- `build/agent-continuity/liturgy-reader-ritual-flow-corrected-v2/` is the latest
  ignored local corrected capture: 61 originals and 25/25 governed assertions,
  with unchanged accepted top geometry (Read 1440 first text 306.09 px and
  width 636 px; Read 768 width 636 px; Roman Missal 1440 first text 316.98 px;
  Roman Missal 393 first text 320.66 px; Roman Missal 320 first text 336.84 px).
  It predates the final major-only locus simplification and therefore is
  diagnostic evidence, not the final matrix.

Visual inspection completed before shutdown:

- wide Epistle and Gospel originals show a quiet two-line marginal locus that
  aligns with the rail and leaves the reading plane untouched;
- mobile Epistle and Preface show the locus as a single compact masthead line
  without changing dock height;
- mobile Canon revealed that hiding the whole locus when an element heading was
  visible removed the major division. The final unvalidated edit now keeps the
  major division while omitting the redundant unit, which implements the brief's
  “disappear or simplify” rule;
- mobile Contents opens with Canon selected and visible in the useful center of
  the sheet while retaining focus on Close Contents.

Honest unfinished state:

- The post-fix Day and Propers browser rerun was interrupted for shutdown. The
  previous run found only test-side issues: smooth scrolling in the new Day
  scan and use of the list rather than `.surface-body` in centering assertions;
  those assertions were corrected, but the complete runs must be repeated.
- Rebuild `build/public-alpha/preview` before testing the final shell edit. Run
  Day, Propers, shared-shell, governed Instrument, focused locked Python, syntax,
  registry, release, public-alpha, and whitespace gates. No release hashes have
  yet been updated for this phase.
- Capture a fresh corrected-v3 directory. Inspect all 61 originals at full
  size. The v2 metric reports geometric overlap between the sticky mobile locus
  and one underlying text range in several deep states; determine whether the
  measurement is counting text hidden behind the already-opaque accepted
  masthead or whether presentation must change. Do not waive the requested
  zero-obscured-text outcome without evidence.
- Roman Preface and other alternative-looking forms remain visually
  conservative because current data does not safely distinguish their
  applicability. Do not classify from names or liturgical knowledge. Any new
  metadata/assembly/source change requires the reviewer stop required by the
  brief.
- No phase handoff, ZIP, final contact sheet, Pages verification, or deployment
  verification exists yet. Do not request independent review until RF-B through
  RF-E, all required gates, deployed evidence, continuity, and the immutable
  handoff are complete.

Exact next command sequence:

1. `PATH="$PWD/build/visual-reset-venv/bin:$PATH" tools/tpt public-alpha build --preview`
2. syntax-check the changed JavaScript harnesses and controllers;
3. rerun Day, Propers, shared-shell, and governed Instrument browser suites;
4. if green, capture `liturgy-reader-ritual-flow-corrected-v3`, inspect the
   mobile locus/overlap and every original, and continue only with bounded RF-D
   or RF-E corrections supported by the semantic inventory.

Do not force-add the ignored v1/v2/v3 exploratory capture directories. The
final immutable handoff remains the only authorized large build-tree evidence
exception for this phase.
