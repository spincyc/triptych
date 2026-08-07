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
