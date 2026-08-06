Codex task: advance the Triptych liturgy reader visually

You are a clean Codex agent working directly in the Triptych repository. Execute this task on the current main branch in the existing checkout. Do not create a worktree, secondary checkout, replacement repository, or feature branch. Do not rewrite published history.

This is a visual correction and evidence task, not another design exploration and not a public cutover. Make visible product progress early, preserve the accepted liturgical and interaction architecture, and leave a complete pushed record that another clean agent or external reviewer can resume without reconstructing the conversation.
1. Task authority and reviewed starting point

The independent review of the visual-reset package selected Liturgical Instrument as the production visual foundation. Quiet Folio and Contemporary Reader remain frozen comparison references; do not merge the three directions into a compromise and do not begin a fourth direction.

The reviewed package identified:

    task base: 842333af79bd560ad6607b91b087ed8ff71e7477

    visual implementation: 7233879350ff00c92fa2029ca04f481125daa519

    reviewed end commit: 0f3567dc509a2d5b42fd58a0e4c77c8f5e5dc113

    selected direction: Liturgical Instrument

    public cutover: not authorized

    production-integration planning: authorized

    production-integration execution: deferred until corrected screenshots pass another independent visual review

First confirm that 0f3567dc509a2d5b42fd58a0e4c77c8f5e5dc113 is contained by current main. Do not reset current main to that commit. Reconcile current local state with origin/main, preserve unrelated work, and continue from the current validated tip.

The accepted M1–M3 and W3 behavior remains binding: state, production assembly, renderer reuse, Ordinary seating, fail-closed behavior, semantic-location restoration, focus behavior, render-race ownership, responsive action reachability, and production isolation are not reopened by this task.
2. Read before editing

Read and reconcile, at minimum:

    AGENTS.md

    PROJECT-WORK.md

    promised-deliverables.toml

    guidance/promised-deliverables.md

    guidance/liturgy-browser-vision.md

    guidance/liturgy-browser-roadmap.md

    guidance/liturgy-reader-shell-prototype.md

    guidance/liturgy-reader-state.md

    guidance/external-review-handoffs.md

    the current visual-reset HTML, CSS, JavaScript, tests, browser harness, and release bindings

Run git status, identify the current branch and exact local/origin relationship, and inspect recent commits touching the reader. Do not discard, overwrite, stage, or commit unrelated changes.

Treat the following independent-review findings as the governing visual diagnosis:

    The permanent control shell still looks like a detachable application widget rather than part of the reading instrument.

    Missal mode begins the rite too far below the first viewport.

    Read mode incorrectly retains an empty ritual gutter.

    The 768-pixel portrait reading measure is too broad.

    Partial and postconciliar coverage warnings repeat and overpower available liturgical text.

    The masthead’s isolated progress dash and generic circular T feel provisional.

    Mobile ritual micro-spacing and narrow division-title wrapping need an editorial pass.

Do not reopen the direction choice. Correct these blockers in Liturgical Instrument.
3. Required durable Codex ↔ reviewer communication

The repository must carry the complete plan and the exact back-and-forth between Codex and the independent reviewer. Chat history is not the durable record.
3.1 Canonical continuity file

Before changing product code, create:

build/agent-continuity/liturgy-reader-visual-plan.md

This task has explicit maintainer authorization to track and push this selected build/ file despite the ordinary ignore rule. Use git add -f only where this instruction explicitly authorizes tracked build/ artifacts.

The continuity file is the canonical shared mailbox and execution plan. It must be append-preserving: never delete or rewrite earlier reviewer messages, Codex reports, decisions, measurements, or commit references. Corrections are appended and cross-reference the superseded statement.

Start it with this structure:

# Liturgy reader visual plan and continuity

## Resume header
- Current branch:
- Current commit:
- Reviewed visual baseline:
- Selected direction: Liturgical Instrument
- Current phase:
- Last completed work unit:
- Next exact action:
- Open blockers:
- Latest pushed commit:
- Latest successful Pages run:
- Latest handoff directory:
- Latest handoff ZIP:

## Fixed decisions and scope boundaries

## Independent review round 0 — reviewer to Codex

## Codex response to review round 0

## Visual work plan

## Measurement baselines and targets

## Decision log

## Checkpoint history

## Open questions for the next independent review

Record the seven findings above in Independent review round 0 — reviewer to Codex. In Codex response to review round 0, state how the implementation plan addresses each finding and identify any reason a proposed correction must differ.
3.2 Back-and-forth protocol

For every independent-review round:

    Append the reviewer’s disposition faithfully under Reviewer to Codex; do not silently paraphrase away qualifiers or blockers.

    Append Codex’s concrete response under Codex to reviewer, mapping every blocker to code, evidence, or an explicit unresolved status.

    Update the Resume header, current plan, measurements, decision log, and next exact action.

    Commit and push the continuity update with the code/evidence it describes.

    Copy the exact continuity file into the new handoff as PLAN-AND-CONTINUITY.md.

    Prove the two copies are byte-identical with cmp and record their SHA-256 in HANDOFF.md and checks.txt.

At the end of this task, the continuity file must contain a concise message to the next reviewer explaining what visibly changed, where to look first, what is still provisional, and the exact decisions requested. That message is the handoff between Codex and ChatGPT; do not rely only on the final terminal response.
3.3 Preserve this instruction

Copy this instruction file verbatim to:

build/agent-instructions/liturgy-reader-instrument-correction.md

Track and push it with git add -f. Include an exact copy as INSTRUCTIONS.md in the final handoff and record its SHA-256. This allows a clean agent to recover both the authority and the execution history.
4. Product objective

Advance Liturgical Instrument from a promising prototype to a visibly coherent, serious reading instrument. The result should feel designed around the action and hierarchy of the liturgy, not around generic app chrome, a centered fragment list, or a faux facsimile.

The corrected prototype must:

    preserve Day and Propers as one product with distinct Date and Browse entrances;

    let Read mode behave as a strong long-form reading page;

    let Missal mode behave as continuous ritual action with useful semantic cues;

    make real liturgical text dominant sooner;

    integrate controls into the composition without hiding them;

    handle missing coverage honestly but quietly;

    feel intentionally composed at desktop, tablet, narrow mobile, enlarged text, deep scroll, and open-surface states.

Make visible progress before undertaking optional cleanup. Prefer direct, bounded composition corrections in the existing visual layer over a broad refactor.
5. Bounded implementation plan

Execute the following work units in order. A work unit is complete only when its visual evidence, measurements, checks, continuity update, commit, push, Pages result, and affected deployed prototype verification agree.
Work unit A — reading plane and first-viewport hierarchy

Correct the basic geometry first.
Read mode

    Remove the unused ritual gutter from Read mode.

    Put identity, Proper headings, references, and prose on one deliberate primary axis.

    Preserve a centered readable measure rather than stretching text merely because space exists.

    At the recorded 768×1024 portrait state, target approximately 40–42rem or about 65–75 characters per line; the reviewed baseline was 726 px and approximately 86 characters.

    Verify that 1440×900, 1024×768, 768×1024, and 393×852 look like the same reading system, not four unrelated breakpoints.

Missal mode

    Keep the identity, but compress the dead interval between identity and ritual action.

    Bring the opening rubric and first spoken prayer at least about 80 px earlier than the reviewed baseline at 1440×900, 393×852, and 320×852, without deleting meaningful identity or creating cramped collisions.

    Reviewed first principal text baselines were approximately:

        474.6 px at 1440×900

        441.8 px at 393×852

        458.8 px at 320×852

    Preserve the semantic cue grid at wide widths and coherent stacked cues on mobile.

Produce before/after screenshots and measurements for this unit before moving to optional polish.
Work unit B — integrated shell and masthead

Make the controls feel native to the composition.

    Flatten the desktop rail and compact bar: remove or greatly reduce the floating-card shadow, excessive elevation, and equal compartment-box feeling.

    Align the desktop rail precisely with the ritual/reading grid rather than leaving it visually detached.

    Make the mobile dock opaque enough that liturgical text does not visibly show through it.

    Retain one-action access to Date or Browse, Contents, Mode, and Details.

    Preserve at least 44 px touch targets, keyboard access, visible focus, safe-area handling, Escape behavior, modal focus entry/restoration, inert background, and semantic location.

    Refine the masthead as one authored system. Replace the generic/provisional mark using existing project-owned inline SVG/CSS only, or simplify it. Do not add an external logo, font, icon service, CDN, or runtime request.

    Either make semantic progress visibly intelligible and accessibly labeled or remove the meaningless dash from the visible masthead while preserving any required internal state.

    Keep Quiet Folio’s restraint as an influence, not its centered Ordinary composition.

Work unit C — warnings, ritual rhythm, and narrow-width finish

    Consolidate partial-coverage status into one compact, honest statement near identity.

    Do not stack a top notice, a second explanatory card, and repeated full-width missing-text bars before available text.

    Demote individual missing elements to restrained inline notation or disclosure while preserving exact source honesty and absence semantics.

    For the recorded Roman 1962 partial mobile state, make available Ordinary text materially more prominent than the warning treatment.

    For the postconciliar Missal state, prevent repeated missing-English bars from becoming the main visual object before the held Propers.

    Tighten spacing among short, closely related call-and-response elements so they read as exchanges rather than database records.

    Reduce dependence on repeated red micro-labels where alignment already communicates speaker/action.

    Give long division titles a deliberate 320 px wrap; avoid awkward orphan fragments.

    Preserve provenance at the end of the rite as subordinate explanatory material.

Work unit D — cross-entrance polish and final evidence

    Confirm that Day Read, Day Missal, Propers Read, and Propers Browse share one unmistakable visual system.

    Confirm that all required open surfaces remain visually coherent.

    Correct only regressions or finish defects exposed by the full matrix; do not add Study, Compare, search, Propers Missal mode, source expansion, recension expansion, or print redesign.

    Do not alter public liturgy/day.html or public liturgy/index.html and do not add links to the prototype.

6. Visual evidence matrix

Use the existing Chromium visual-reset harness as the source of truth. Extend it rather than replacing it with manual-only screenshots. Capture real supported states and record exact URL/hash, viewport, scroll position, key geometry, overflow, focus, semantic state, console errors, failed requests, and HTTP errors.

At minimum, produce comparable before/after evidence for:
Core reading states

    Day Read: 1440×900

    Day Read: 1024×768

    Day Read: 768×1024

    Day Read: 393×852

    Day Missal: 1440×900

    Day Missal: 393×852

    Day Missal: 320×852

    Day Missal deep scroll: 1440×900

    Roman 1962 partial coverage: 393×852

    Postconciliar Missal partial-English coverage: 1440×900

    Postconciliar Missal partial-English coverage: 393×852

    Propers Read: 1440×900

    Propers Read: 393×852

    Propers Browse: 393×852

Interaction and resilience states

    Date open: 1024×768

    Contents open: 393×852

    Mode open: 393×852

    Details open: 1440×900

    200% text: 393×852

    forced colors: 393×852

    reduced motion: 393×852

    keyboard focus: 393×852

Create:

    a labeled final Instrument contact sheet;

    a compact labeled before/after blocker contact sheet;

    capture-metadata.json with explicit baseline and corrected measurements;

    a short MEASUREMENTS.md that reports deltas rather than only final numbers.

Do not manufacture data or fill missing liturgical text for visual completeness.
7. Implementation constraints
Must preserve

    one semantic DOM and one interaction foundation across directions;

    production Day and Propers adapters;

    production Proper and Ordinary rendering paths;

    one Ordinary seating path;

    M1 state and URL ownership;

    fail-closed invalid/unsupported state;

    edition-specific option validity;

    semantic-location preservation;

    race ownership;

    existing public-route isolation and noindex behavior;

    source honesty and explicit absences;

    no horizontal overflow in required states;

    accessibility names and focus behavior;

    reduced-motion and forced-color support;

    no new external runtime dependency.

Out of scope

    another visual direction;

    public cutover or public navigation links;

    replacing public Day or Propers;

    Study, Compare, search, or Propers Missal mode;

    new calendars, sources, editions, recensions, translations, or Bible data;

    fabricating missing Ordinary or Proper text;

    print redesign beyond preserving smoke behavior;

    broad shell, state, adapter, renderer, or seating rewrites;

    unrelated repository cleanup.

When a visual correction appears to require changing an accepted behavioral seam, first prove that the change is actually necessary and record the conflict in the continuity file. Prefer a presentation-layer solution.
8. Tests and validation

Run the repository-required checks for every affected layer. At minimum, run and record exact commands and exit codes for:

python3 -m unittest -v \
  tools.tests.test_day_missal_integration \
  tools.tests.test_day_reader_integration \
  tools.tests.test_liturgy_reader_shell \
  tools.tests.test_liturgy_reader_state \
  tools.tests.test_mass_ordinary \
  tools.tests.test_propers_reader_integration \
  tools.tests.test_liturgy_reader_visual_reset

node --check src/web/browser/liturgy/reader-visual-reset.js
node --check tools/tests/liturgy_reader_visual_reset_browser.mjs
node tools/tests/liturgy_reader_visual_reset_browser.mjs

tools/tpt check-promised-deliverables
tools/tpt --check
make check-release-bindings
git diff --check

Also run the existing Day, Propers, and shared-shell browser harnesses; discover and record their exact current commands rather than guessing stale names.

Run the governed full gate:

make check

If it fails for unrelated known transcript divergence, record the exact stop, exit code, and bounded diagnosis. Do not recapture unrelated examples, bless unrelated changes, or describe the full gate as passing. If the failure is task-owned, correct it.

Build and verify the exact public-alpha preview using the current repository commands and guidance, including:

tools/tpt public-alpha check
tools/tpt public-alpha build
tools/tpt public-alpha verify --deployment-target github-pages

No automated check proves visual quality. Inspect every required screenshot at full size and write a blocker-by-blocker visual self-review into the continuity file before asking for independent review.
9. Tracking records

Update tracked owners so current repository state is truthful:

    PROJECT-WORK.md

    guidance/liturgy-browser-roadmap.md

    promised-deliverables.toml

Create or revise a bounded deliverable for the Liturgical Instrument correction pass. Do not mark it complete merely because code was written, tests passed, a commit was pushed, Pages deployed, or a handoff was assembled. The deliverable remains candidate/pending until independent visual review resolves every blocker.

Record exact commit SHAs, Pages runs, handoff paths, selected direction, open review state, and public-cutover prohibition.
10. Commit and push discipline

Use ordinary coherent commits on current main. Do not force-push, amend published commits, change remotes, or rewrite history.

Recommended checkpoint shape:

    Visual geometry checkpoint — Work unit A plus continuity/tracking updates and evidence.

    Instrument finish checkpoint — Work units B and C plus evidence and updated continuity.

    Review handoff checkpoint — Work unit D, final checks, final evidence, handoff, and exact tracking state.

Combine or split only when the repository state makes another coherent boundary more truthful. Do not create a plan-only checkpoint while visual work remains untouched; the first pushed task checkpoint must contain visible product progress.

Before each commit and push:

    inspect git status;

    inspect the exact staged diff;

    confirm no unrelated changes are included;

    run the checks required by the unit;

    update the continuity resume header and checkpoint history;

    inspect the exact outgoing commit range;

    confirm every newly reachable object is intended for public disclosure.

After each push:

    verify the resulting GitHub Pages run;

    verify the affected deployed unlinked/noindex prototype routes directly;

    record the run, result, routes, and verification time in the continuity file;

    never represent the checkpoint as deployed until Pages succeeds.

11. Final handoff — explicitly tracked build exception

Create a new immutable handoff using guidance/external-review-handoffs.md, with a fresh UTC timestamp and slug:

build/agent-handoffs/<UTC_TIMESTAMP>-liturgy-reader-instrument-correction/
build/agent-handoffs/<UTC_TIMESTAMP>-liturgy-reader-instrument-correction.zip

Do not overwrite or refresh an earlier handoff.

This task has explicit maintainer authorization to force-add, commit, and push the following normally ignored build artifacts:

build/agent-instructions/liturgy-reader-instrument-correction.md
build/agent-continuity/liturgy-reader-visual-plan.md
build/agent-handoffs/<UTC_TIMESTAMP>-liturgy-reader-instrument-correction/
build/agent-handoffs/<UTC_TIMESTAMP>-liturgy-reader-instrument-correction.zip

Do not force-add caches, virtual environments, general build outputs, unrelated handoffs, or other ignored files.

The handoff must include at least:

    START-HERE.md

    HANDOFF.md

    REVIEW_REQUEST.md

    CLEAN-CHATGPT-REVIEW-PROMPT.md

    INSTRUCTIONS.md — exact copy of this task instruction

    PLAN-AND-CONTINUITY.md — exact copy of the canonical continuity file

    CONTEXT.md

    VISUAL-DECISIONS.md

    BEFORE-AFTER.md

    MEASUREMENTS.md

    PRODUCTION-ISOLATION.md

    checks.txt

    changes.patch

    changed-files.txt

    MANIFEST.sha256

    focused source/ snapshots

    compact runnable candidate/

    evidence/screenshots/

    evidence/capture-metadata.json

    evidence/browser-results.json

    bounded relevant logs/

The review request must ask for exact blocker dispositions, not “does it look good?” At minimum ask:

    Does the corrected Instrument now feel like a serious, coherent reading instrument rather than a styled prototype?

    Is the shell integrated into the composition on desktop and mobile?

    Is real liturgical text dominant soon enough in Read, Missal, partial, and postconciliar states?

    Does Read use one deliberate axis and a controlled measure at 768×1024?

    Does the Ordinary read as continuous ritual action on desktop and mobile?

    Are warnings honest but subordinate?

    Are the masthead, narrow division titles, and mobile exchange spacing finished enough to authorize production-integration execution?

    What exact blockers remain?

The handoff must state clearly that public cutover remains unauthorized and that acceptance of this correction pass is the gate for beginning production-integration execution.

Create MANIFEST.sha256 last, verify every entry, test the ZIP, confirm the archive has one top-level directory, and record both directory and ZIP verification.
12. Completion standard

Do not stop at “CSS changed” or “tests pass.” This task is complete only when all of the following are true:

    Liturgical Instrument visibly resolves the seven reviewed blockers or records an explicit remaining blocker.

    Required before/after evidence and measurements exist.

    Behavioral, accessibility, isolation, and release checks are honestly recorded.

    The continuity file contains the full reviewer-to-Codex input, Codex response, current plan, checkpoint history, exact stopping point, and message to the next reviewer.

    The instruction file, continuity file, complete timestamped handoff directory, and verified ZIP are committed and pushed as the authorized build-tree exception.

    PROJECT-WORK.md, roadmap, and promised-deliverables state agree with code, evidence, push, Pages, and review status.

    Current main and origin/main agree for the task commits.

    The final response reports exact commit SHAs, Pages result, prototype routes verified, handoff directory, handoff ZIP, and remaining review gate.

Do not claim independent acceptance. End with a candidate ready for a clean visual review and enough durable state that the next agent can begin by reading build/agent-continuity/liturgy-reader-visual-plan.md and the latest handoff without reconstructing this conversation.
