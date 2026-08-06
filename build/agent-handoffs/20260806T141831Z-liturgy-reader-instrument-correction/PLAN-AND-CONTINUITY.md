# Liturgy reader visual plan and continuity

## Resume header

- Current branch: `main`
- Current commit: `c388ab42dfc4f5c7d49abc71596d6bb511af5742` plus post-deployment immutable handoff/tracking staging
- Reviewed visual baseline: `0f3567dc509a2d5b42fd58a0e4c77c8f5e5dc113` (visual implementation `7233879350ff00c92fa2029ca04f481125daa519`; task base `842333af79bd560ad6607b91b087ed8ff71e7477`)
- Selected direction: Liturgical Instrument
- Current phase: Round 1 shell correction, deployed parity, and post-deployment immutable evidence complete; candidate is stopped for narrow independent re-review
- Last completed work unit: successful Pages deployment, direct Day/Propers noindex and CSS/JS parity, and final immutable handoff settlement
- Next exact action: independent reviewer answers the three bounded questions in the latest handoff; do not begin production-integration execution or public cutover beforehand
- Open blockers: independent Round 1 re-review only; the two requested product blockers are internally resolved and corrected deployed parity passes, while production-integration execution and public cutover remain unauthorized
- Latest pushed commit: `c388ab42dfc4f5c7d49abc71596d6bb511af5742` — immutable Round 1 re-review handoff
- Latest successful Pages run: `31109086658`, success for `c388ab42dfc4f5c7d49abc71596d6bb511af5742` at 2026-08-06T14:17:40Z
- Latest handoff directory: `build/agent-handoffs/20260806T141831Z-liturgy-reader-instrument-correction/`
- Latest handoff ZIP: `build/agent-handoffs/20260806T141831Z-liturgy-reader-instrument-correction.zip`

## Fixed decisions and scope boundaries

- Liturgical Instrument is the selected production visual foundation. Quiet Folio and Contemporary Reader are frozen comparison references; this correction does not merge them or create another direction.
- Public cutover and public navigation links are not authorized. Production-integration planning is authorized; execution remains deferred until this correction passes independent visual review.
- Accepted M1–M3 and W3 state, production assembly, renderer reuse, one Ordinary seating path, fail-closed behavior, semantic-location restoration, focus behavior, render-race ownership, responsive action reachability, and production isolation remain binding.
- Day and Propers remain distinct Date and Browse entrances to one product. Propers Missal, Study, Compare, search, source or recension expansion, and print redesign remain out of scope.
- Product corrections stay in the selected prototype presentation layer unless evidence proves an accepted behavioral seam must change. No such conflict is presently known.
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
