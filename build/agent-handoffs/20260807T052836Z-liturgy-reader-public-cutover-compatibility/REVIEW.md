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
