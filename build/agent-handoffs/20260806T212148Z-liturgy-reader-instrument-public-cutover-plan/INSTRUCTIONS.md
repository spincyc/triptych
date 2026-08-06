# Clean Codex Brief — Liturgical Instrument Public-Cutover Planning

## Mission

You are a clean Codex agent starting from the accepted, durably archived Liturgical Instrument production integration.

Your task is to prepare a complete, independently reviewable public-cutover plan for moving the accepted production Day and Propers readers onto the canonical public routes:

    Day: /liturgy/day.html

    Propers: /liturgy/index.html

The accepted production-reader candidates are:

    /liturgy/day-reader.html

    /liturgy/propers-reader.html

The accepted visual oracle remains the isolated Liturgical Instrument prototype.

This phase is planning and pre-cutover readiness only.

Do not change public navigation. Do not replace the canonical public pages. Do not execute the public cutover.

The purpose of this phase is to make the eventual cutover boring: small, reversible, URL-compatible, visually identical to the accepted production candidates, and backed by exact preflight and rollback procedures.

## Starting boundary

Start from a clean checkout of:

7b7044dea7f5c35a2d32ff85f26eb5b182bf40ef

Before doing anything else, verify:

git status --short
git rev-parse HEAD
git rev-parse main
git rev-parse origin/main
git ls-remote origin refs/heads/main

All local and remote main references must agree before planning begins.

Known accepted history:

    Liturgical Instrument visual foundation: accepted.

    Responsive correction round: accepted.

    Production integration: accepted.

    Durable integration handoff closeout:

        archival commit 8c6e1270f692ca4136f2f6a60002bacd3af0440c

        final closeout commit 7b7044dea7f5c35a2d32ff85f26eb5b182bf40ef

    Exact successfully deployed integrated production state:
    5444d89fc9b379a1babef5b2220323fe1508b2b3

    Successful Pages run for that state:
    31125898045

    Accepted production-integration handoff:
    build/agent-handoffs/20260806T183040Z-liturgy-reader-instrument-production-integration/

    Accepted handoff ZIP:
    build/agent-handoffs/20260806T183040Z-liturgy-reader-instrument-production-integration.zip

    Accepted ZIP SHA-256:
    ebf0361309ac33b4580cbb535e4bbd3eabd144756e6c078aa140e716c748f05f

Known honest non-green results:

    Day browser suite: 33/34 solely because of the existing date-dependent first-visit assertion.

    Governed full repository gate: still stops at unrelated stored example-transcript divergence.

Do not recapture or bless unrelated example transcripts.

## 1. Mandatory read order

Read these before proposing a cutover:

    build/agent-continuity/liturgy-reader-visual-plan.md

    build/agent-handoffs/20260806T183040Z-liturgy-reader-instrument-production-integration/START-HERE.md

    .../HANDOFF.md

    .../PROTOTYPE-TO-PRODUCTION.md

    .../PRODUCTION-ISOLATION.md

    .../REVIEW_REQUEST.md

    the independent production-integration review and Codex response in the continuity record

    PROJECT-WORK.md

    guidance/liturgy-browser-roadmap.md

    promised-deliverables.toml

    release/public-alpha.json

    the Pages/build/deploy workflow(s)

    canonical public Day HTML/JS/CSS and all assets they load

    canonical public Propers HTML/JS/CSS and all assets they load

    accepted candidate Day HTML/JS/CSS and all assets they load

    accepted candidate Propers HTML/JS/CSS and all assets they load

    shared reader shell/state/adapter/renderer modules involved in either route

Do not infer route behavior from filenames. Trace the actual loading graph and state ownership.

## 2. Continuity protocol — required

The reviewer/Codex exchange must remain recoverable from Git.

Before product analysis, append a new section to:

build/agent-continuity/liturgy-reader-visual-plan.md

with this heading:

## Public cutover planning — reviewer to Codex

Under it, preserve the substance of this brief, including:

    the starting commit;

    planning-only authorization;

    the canonical routes;

    candidate routes;

    frozen accepted decisions;

    required questions;

    required artifacts;

    stopping point;

    explicit prohibition on public navigation/cutover execution.

Immediately after that, append:

## Public cutover planning — Codex response

Codex's first response must record:

    exact starting SHA and clean-worktree status;

    the files/modules believed to own the current canonical routes;

    the files/modules believed to own the accepted candidates;

    the proposed analysis work units;

    any uncertainty requiring source inspection;

    confirmation that no public route or navigation will be modified in this phase.

Update this continuity record after every meaningful checkpoint. Do not save the real plan only in chat or terminal output.

## 3. Freeze the accepted visual/product decisions

These are no longer open design questions:

    Liturgical Instrument is the production visual foundation.

    Read uses one deliberate reading axis.

    The accepted Read measure remains approximately 636 px / 75 characters at 768×1024.

    Missal uses the accepted ritual cue/grid system and mobile stacking.

    The 1440 external rail is accepted.

    Intermediate/mobile use the square, opaque, edge-bound dock.

    200% text uses the accepted deliberate reflow with whole action labels.

    Coverage warnings stay compact and subordinate.

    The masthead and 320 px title treatment are accepted.

    Day and Propers are one product with distinct Date/Browse entrances.

    Propers retains the canonical production Browse selector; prototype title search remains out of scope.

    Existing state adapters, renderers, Ordinary seating, semantic locations, focus ownership, modal ownership, winning-render/race checks, sources, editions, translations, and fail-closed behavior remain production-owned.

    The accepted prototype remains the comparison oracle through cutover review.

Do not use cutover planning as an excuse to redesign or refactor these.

## 4. Work Unit CO-A — Canonical-route inventory

Produce an exact inventory of what the current canonical pages do today.

For each of:

    /liturgy/day.html

    /liturgy/index.html

    /liturgy/day-reader.html

    /liturgy/propers-reader.html

record:

    source HTML path;

    JavaScript entry points;

    loaded CSS;

    shared shell dependencies;

    relative data paths;

    navigation links into and out of the page;

    robots/indexing metadata;

    document title/meta behavior;

    URL query/hash parsing;

    default-state behavior;

    history/back-forward behavior;

    deep-link restoration;

    any service-worker/cache implications if present;

    release/public-alpha bindings;

    build-copy/publication rules.

Create:

build/agent-continuity/liturgy-reader-cutover-route-map.md

This file must distinguish canonical public contract from implementation detail.

### Required canonical deep links

At minimum, prove the plan preserves these existing URLs exactly:

/liturgy/day.html#date=2026-08-05&missal=roman-1962&bible=douay-rheims
/liturgy/index.html#missal=roman-1962&type=seasonal&mass=advent-1&bible=douay-rheims

Also enumerate representative links for:

    another date;

    postconciliar/Novus Ordo Day state;

    Roman 1962 seasonal Proper;

    at least one sanctoral Proper if supported;

    back/forward state transitions;

    malformed/unsupported state;

    a state with incomplete English coverage.

Do not silently normalize away current public URL forms.

## 5. Work Unit CO-B — Decide the smallest cutover mechanism

Compare plausible mechanisms, then select one.

At minimum evaluate:

### Option A — Make canonical pages load the already accepted production-reader implementation

For example, retain canonical filenames while moving the accepted candidate markup/hooks and assets behind those filenames.

### Option B — Convert canonical pages into redirects/forwarders to reader pages

This is acceptable only if it preserves the complete external URL/state contract, history semantics, accessibility, indexing, and navigation behavior with no visible transitional flash or broken fragment state.

### Option C — Rename/move candidate pages into canonical paths and preserve compatibility aliases

Evaluate build/deploy and rollback consequences carefully.

### Option D — Any smaller architecture discovered from source

If the repository already has a routing/publication seam that makes the above unnecessary, document it.

Select the mechanism with the smallest blast radius and best rollback properties.

### Decision rule

Prefer:

    canonical URLs unchanged;

    no duplicated long-term state implementation;

    no new redirect semantics unless genuinely necessary;

    minimal product bytes changed;

    exact reuse of the already accepted production implementation;

    easy one-commit rollback;

    no dependency on a future cleanup step for correctness.

Create:

build/agent-continuity/liturgy-reader-cutover-decision.md

Include a short rejected-options section so a later clean agent does not reopen settled alternatives without evidence.

## 6. Work Unit CO-C — URL and state compatibility proof

Build a machine-readable compatibility matrix comparing canonical current behavior with the accepted production-reader candidate behavior.

The matrix must cover, at minimum:

### Day

    explicit date;

    first visit/default date;

    Roman 1962;

    postconciliar state;

    Bible selection;

    Read/Missal mode;

    reload;

    direct deep link;

    back/forward;

    malformed state;

    partial-coverage state;

    modal open/close with URL state intact;

    scroll/semantic-location restoration where currently governed.

### Propers

    seasonal mass;

    sanctoral mass if available;

    missal selection;

    Bible selection;

    Browse changes;

    reload;

    direct deep link;

    back/forward;

    malformed/unsupported selection;

    modal open/close;

    current canonical selector behavior.

Output both human-readable and machine-readable forms:

build/agent-continuity/liturgy-reader-cutover-state-matrix.md
build/agent-continuity/liturgy-reader-cutover-state-matrix.json

Every material difference must be classified as:

    exact match;

    accepted intentional difference;

    cutover blocker;

    unrelated pre-existing behavior.

No unexplained differences.

## 7. Work Unit CO-D — Make the Day gate deterministic if safely possible

The current 33/34 Day result is understood to be caused only by a date-dependent first-visit assertion.

For a public cutover, a task-owned test should not remain red merely because the clock moved.

You are authorized to inspect and, only if the cause is exactly the already-disclosed date dependency, make that browser assertion deterministic without changing product behavior.

Acceptable approaches include:

    freezing the test clock;

    explicitly supplying the intended date;

    deriving the expected first-visit state from the same documented calendar contract without weakening the assertion.

Not acceptable:

    deleting the assertion;

    broadening it until anything passes;

    changing production default-date semantics just to satisfy the test;

    blessing unrelated failures.

If this can be fixed narrowly, do it in a separate test-only commit and run the complete affected suites.

If the cause is not exactly the known date dependency, stop and record the new finding as a blocker instead of changing behavior.

Goal for cutover readiness:

Day task-owned browser suite: 34/34.

The unrelated example-transcript gate may remain honestly non-green.

## 8. Work Unit CO-E — Proposed cutover diff, without applying it

Produce an exact proposed public-cutover patch, but do not apply it to the repository's canonical public files in this phase.

Create it from temporary copies or another non-worktree scratch location.

Output:

build/agent-continuity/liturgy-reader-public-cutover-proposed.patch

The patch must show exactly what a later authorized cutover execution would change.

The proposed patch should be as small as possible.

It must not contain:

    visual redesign;

    new search;

    source/translation expansion;

    Ordinary renderer changes;

    unrelated refactoring;

    prototype cleanup;

    candidate cleanup;

    broad navigation redesign;

    unrelated transcript updates.

If the selected mechanism needs generated build/release changes, show those too.

## 9. Work Unit CO-F — Rollback design

Write an operational rollback plan.

Create:

build/agent-continuity/liturgy-reader-public-cutover-rollback.md

It must define:

### Immediate rollback trigger

Examples:

    canonical deep-link incompatibility;

    state-loss on reload/back-forward;

    visual divergence from accepted production candidate;

    modal/focus regression;

    missing assets/HTTP errors;

    public Pages deployment mismatch;

    accessibility regression;

    unexpected source/coverage behavior.

### Rollback mechanism

Prefer an ordinary revert of the cutover commit(s), not history rewriting.

Record:

    which commit(s) would be reverted;

    whether a release manifest/build artifact also needs rollback;

    how to confirm rollback assets are deployed;

    how to verify canonical Day and Propers URLs after rollback.

### Retained fallback surfaces

The candidate reader routes and accepted prototype should remain available and unmodified through the initial public-cutover acceptance window unless a later review explicitly authorizes removal.

Do not combine candidate/prototype cleanup with initial cutover.

## 10. Work Unit CO-G — Cutover acceptance gates

Define the exact gate the later execution agent must pass before the cutover can be independently accepted.

At minimum require:

### Repository/local

    clean starting tree;

    focused Python suites;

    Day browser 34/34 if CO-D safely makes it deterministic;

    Propers browser all green;

    shared-shell browser all green;

    governed Instrument visual assertions all green;

    JS syntax checks;

    release/publication checks;

    public-alpha build/verify;

    no unintended diff outside approved paths.

### Canonical-route browser matrix

Run against the actual canonical filenames in a local/staged build after the proposed patch is applied in the later authorized execution phase.

Required visual/behavior states must include:

    Day Read 1440×900;

    Day Read 1024×768;

    Day Read 768×1024;

    Day Read 393×852;

    Day Missal 1440×900;

    Day Missal 1024×768;

    Day Missal 393×852;

    Day Missal 320×852;

    Roman partial;

    postconciliar partial-English;

    deep Missal scroll;

    Propers Read desktop/mobile;

    Propers Browse desktop/mobile;

    Date open;

    Contents open;

    Mode open;

    Details open;

    200% text;

    keyboard focus;

    forced colors;

    reduced motion.

### Visual oracle requirement

The later cutover execution must compare canonical public-route screenshots to the already accepted production-reader candidate, not restart comparison from the old public reader.

For equivalent states, geometry and composition should be materially identical. Any intentional route-specific difference must be enumerated in advance.

### Deployment

The exact intended cutover commit must have:

    successful Pages build/deploy;

    HTTP 200 for canonical Day and Propers deep links;

    deployed/source byte parity for changed assets;

    direct verification of the canonical URLs;

    no console errors;

    no failed required requests;

    no unexpected HTTP failures;

    no duplicate IDs;

    no unnamed interactive controls;

    no required horizontal overflow.

### Search/index metadata

Verify intended robots/canonical/indexing metadata on the canonical public pages. Candidate and oracle routes should not accidentally become the indexed canonical surfaces.

## 11. Navigation inventory — planning only

Find every repository-owned navigation entry that points users to the canonical Day or Propers pages.

Record it in:

build/agent-continuity/liturgy-reader-cutover-navigation-map.md

Do not change navigation in this phase.

Classify each link as:

    already points to canonical URL and therefore needs no cutover edit;

    needs a later label/description update only;

    would need a route change;

    stale/unrelated.

The preferred cutover keeps canonical URLs stable so most navigation should require no change.

If your proposed cutover mechanism requires widespread navigation edits, treat that as evidence the mechanism is too invasive and reconsider it.

## 12. SEO, caching, and static-hosting checks

Because this is GitHub Pages/static hosting, explicitly investigate:

    relative asset resolution from canonical routes;

    cache behavior for reused filenames;

    whether query/hash state survives the selected cutover mechanism;

    canonical/robots metadata;

    whether redirects are even appropriate under Pages for this use case;

    whether stale HTML can briefly load incompatible cached JS/CSS;

    whether a cache-busting asset strategy is already used or needed.

Do not invent infrastructure that the project does not need. The goal is to identify real static-site cutover risks.

## 13. Planning deliverable and tracking entry

Add a new promised deliverable for the planning phase, with a stable ID such as:

liturgy-reader-instrument-public-cutover-plan-2026-08-06

Update:

    PROJECT-WORK.md

    guidance/liturgy-browser-roadmap.md

    promised-deliverables.toml

The state should say, in substance:

    production integration: accepted and complete;

    durable handoff: complete;

    public-cutover plan: in progress, then candidate for independent review;

    public navigation/cutover execution: unauthorized.

Do not mark public cutover complete.

## 14. Required handoff package

When the plan is complete, create an immutable handoff:

build/agent-handoffs/<UTC>-liturgy-reader-instrument-public-cutover-plan/
build/agent-handoffs/<UTC>-liturgy-reader-instrument-public-cutover-plan.zip

Because the maintainer explicitly requires plan/reviewer/Codex continuity and handoff artifacts to survive in the pushed build tree, you are authorized to force-add only the exact new cutover-plan handoff directory and its matching ZIP if the existing ignore rules require it.

Do not use that authority for caches, generic build output, previous ignored artifacts, or unrelated files.

The handoff must contain:

    START-HERE.md

    HANDOFF.md

    INSTRUCTIONS.md — this brief

    PLAN-AND-CONTINUITY.md — byte-identical snapshot of the canonical continuity file

    CUTOVER-DECISION.md

    ROUTE-MAP.md

    STATE-COMPATIBILITY.md

    STATE-COMPATIBILITY.json

    NAVIGATION-MAP.md

    ROLLBACK.md

    CUTOVER-GATES.md

    PROPOSED-CUTOVER.patch

    CHANGED-FILES.txt

    any CO-D deterministic-test patch/evidence, if applicable

    relevant current/candidate/canonical source snapshots

    local validation logs

    current deployment/publication observations

    MANIFEST.sha256

Generate MANIFEST.sha256 last.

Then create the ZIP and verify:

unzip -t <zip>
# exactly one top-level directory
sha256sum -c MANIFEST.sha256
sha256sum <zip>

Record exact counts and hashes.

The directory and ZIP themselves must be committed and pushed as part of this planning phase.

## 15. Required plan quality

The final cutover plan must be executable by another clean Codex agent without rediscovering architecture.

It must answer these questions explicitly:

    Which exact files change during cutover?

    Which exact files must not change?

    How are canonical Day URLs preserved?

    How are canonical Propers URLs preserved?

    How is hash/query state preserved?

    What happens to day-reader.html and propers-reader.html immediately after cutover?

    What happens to the visual-reset oracle immediately after cutover?

    What is the smallest reversible commit sequence?

    What exact test/evidence matrix must pass before deployment?

    What exact deployed checks must pass after deployment?

    What conditions cause immediate rollback?

    How is rollback performed and verified?

    Which cleanup tasks are deliberately postponed until after cutover acceptance?

    What remains explicitly unauthorized?

Avoid vague language such as "update routes", "verify functionality", or "test mobile". Name files, states, commands, and expected results.

## 16. Preferred commit structure

Keep planning commits understandable and reversible.

A reasonable structure is:

    Plan Instrument public cutover

        continuity kickoff

        route map

        architecture/cutover decision

        state matrix

        navigation map

    Make Day cutover gate deterministic

        only if the known 33/34 date dependency can be fixed safely

        test-only

        no product behavior change

    Seal Instrument cutover plan

        proposed patch

        rollback

        gates

        tracking state

        handoff directory and ZIP

        final continuity response

Adjust if repository conventions justify a different split, but do not mix public cutover execution into these commits.

Push each stable checkpoint to origin/main only after its scoped checks pass.

## 17. Independent-review request

The final handoff must request a narrow independent review answering:

    Is the selected cutover mechanism the smallest safe way to put the accepted readers on the canonical URLs?

    Does the plan preserve the existing Day and Propers URL/state contracts?

    Is the proposed diff limited to cutover rather than redesign/refactor?

    Are indexing, static-asset, cache, Pages, and relative-path risks handled?

    Is the rollback immediate, complete, and testable?

    Are the pre/post-deployment gates sufficient to detect visual and behavioral regression?

    If the Day first-visit test was changed, is it genuinely deterministic without weakening the contract?

    Is the plan sufficiently exact to authorize a later clean agent to execute it without new architectural decisions?

The reviewer may then:

    request planning changes, or

    accept the plan and authorize a separate public-cutover execution phase.

Do not infer authorization merely because the plan is good.

## 18. Hard stopping point

Stop when all of the following are true:

    cutover route/state/navigation inventories are complete;

    one cutover mechanism is selected and justified;

    proposed public-cutover patch exists but is not applied to canonical public files;

    rollback and acceptance gates are exact;

    the Day date-dependent test is either safely deterministic and green or explicitly recorded as an unresolved cutover blocker;

    continuity is current;

    tracking files truthfully describe planning state;

    immutable handoff directory and ZIP are pushed in the build tree;

    main, origin/main, and remote main agree;

    worktree is clean.

Then hand the package to the independent reviewer.

Do not modify the canonical public Day/Propers routes.
Do not alter public navigation.
Do not delete or repurpose the candidate routes.
Do not remove the accepted visual oracle.
Do not execute public cutover.
