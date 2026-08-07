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

