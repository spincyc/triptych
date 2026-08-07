# Liturgy reader visual plan and continuity

## Resume header

- Current branch: `main`
- Current commit: `e62a226fc661100a2427a4193213c7dadcf24225` (local exact cutover-patch execution baseline); sealed patch header and handoff artifacts are local and uncommitted
- Reviewed visual baseline: `0f3567dc509a2d5b42fd58a0e4c77c8f5e5dc113` (visual implementation `7233879350ff00c92fa2029ca04f481125daa519`; task base `842333af79bd560ad6607b91b087ed8ff71e7477`)
- Selected direction: Liturgical Instrument
- Current phase: bounded public-cutover compatibility closure; canonical promotion and public navigation remain unauthorized
- Last completed work unit: CC-B/CC-C compatibility implementation, deployed parity, literal-reload/second-branch evidence hardening, and exact normal-context future cutover patch checkpoint
- Next exact action: seal, verify, force-add, commit, and push the immutable compatibility handoff; then stop for the seven-question independent re-review
- Open blockers: narrow independent review must accept the compatibility closure and regenerated patch before public cutover execution can be authorized; the unrelated governed example replay remains non-green
- Latest pushed commit: `998648c341691c0807b0c209f93fbae16d641d48` — compatibility evidence-hardening baseline
- Latest successful Pages run: `31150296458`, success for exact evidence baseline `998648c341691c0807b0c209f93fbae16d641d48`; compatibility product deployment run `31148986910` also succeeded for `3f3949617a04ffa68a1070058d0f7bc5ac74dc93`
- Latest Pages attempt: run `31148986910` succeeded; older planning-only run `31128301816` for `5e1b82b51` was cancelled after remaining queued/waiting since the prior day and blocking the current run
- Latest handoff directory: `build/agent-handoffs/20260807T052836Z-liturgy-reader-public-cutover-compatibility/` (assembled locally; verification and push pending)
- Latest handoff ZIP: `build/agent-handoffs/20260807T052836Z-liturgy-reader-public-cutover-compatibility.zip` (creation, verification, and push pending)

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
