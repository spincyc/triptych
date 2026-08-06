# Liturgy reader visual plan and continuity

## Resume header

- Current branch: `main`
- Current commit: `62e712a1962080d1dc3c6e106651c41afbf7531b` plus final evidence/handoff staging
- Reviewed visual baseline: `0f3567dc509a2d5b42fd58a0e4c77c8f5e5dc113` (visual implementation `7233879350ff00c92fa2029ca04f481125daa519`; task base `842333af79bd560ad6607b91b087ed8ff71e7477`)
- Selected direction: Liturgical Instrument
- Current phase: Work unit D evidence and validation complete; immutable review handoff staged
- Last completed work unit: Work unit D — cross-entrance polish and final evidence
- Next exact action: independent reviewer reads this file and the latest handoff, inspects full-size evidence, and appends an exact blocker disposition as review round 1
- Open blockers: independent correction review is the only remaining gate; production-integration execution and public cutover remain unauthorized
- Latest pushed commit: `62e712a1962080d1dc3c6e106651c41afbf7531b` — Instrument finish implementation
- Latest successful Pages run: `31094868150`, success for `62e712a1962080d1dc3c6e106651c41afbf7531b` at 2026-08-06T11:00:15Z
- Latest handoff directory: `build/agent-handoffs/20260806T112813Z-liturgy-reader-instrument-correction/`
- Latest handoff ZIP: `build/agent-handoffs/20260806T112813Z-liturgy-reader-instrument-correction.zip`

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
