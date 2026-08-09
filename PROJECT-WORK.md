# Project Work Register

This is Triptych's provider-neutral operational memory. Read it together with
`promised-deliverables.toml` before starting or resuming work, after a context
handoff, and before reporting completion. “Published,” “built,” “committed,”
“pushed,” “review copy,” and “complete” are different states.

Last reconciled: 2026-08-08.

## Standing public-alpha authority

On 27 July 2026 the maintainer approved every Triptych document for
conspicuously labeled public-alpha distribution so that priests and other
qualified readers can review it from stable public links. This is a standing
workflow authorization: changed source may be researched, built, inspected,
installed, bound as an exact current public-review snapshot, validated, and
committed without requesting a new
document-by-document alpha approval.

A clean direct Codex session on `main` has standing authority to make ordinary
coherent commits for authorized work and regularly push validated checkpoints
to `origin/main` after each independently reviewable unit. Before each push,
run the checks required by the affected guidance, inspect the exact outgoing
range, and confirm that every newly reachable object is intended for public
disclosure. Because each `origin/main` push triggers GitHub Pages, this
authority includes the resulting automatic deployment attempt. It does not
authorize force-pushing, amending or otherwise rewriting published history,
changing remotes, integrating a retained worker, or triggering another
deployment mechanism. Never represent a snapshot as live until its Pages run
has succeeded and the affected production routes have been verified.

Public-alpha authorization is distribution authority only. It never records
or implies human, priestly, specialist, ecclesiastical, rights, intended-reader,
physical-print, or final editorial approval that has not actually occurred.

On 31 July 2026 the maintainer retired the six-concern alpha completion
assessment — source support, rights and distribution status, safety, artifact
consistency, mechanical correctness, every-page visual inspection — as
bookkeeping the project imposed on itself. No tool ever read those fields; they
were prose scoring prose. A publication is alpha when it is built, checked by
the gates that actually run, and published.

What that retirement does not touch, because none of it was ever the
bookkeeping: a known defect still stays explicit in the research records,
release inventory, catalogs, and this register — recording a defect is how a
reader learns of it, not a gate. Passing an internal check still does not imply
external approval, and the workflow still creates no placeholder gate for a
reviewer who is not coming. Those are statements about what is true, and
withdrawing a scoring scheme does not make them false.

## Research staleness is suspended

On 31 July 2026 the maintainer suspended the research-staleness signal. Nothing
is to be flagged stale, and **the papers are to be left exactly as they are**.
No research is re-read, no review record is written, and no edition is
rebaselined until the suspension is lifted.

Two reasons, and the second is the larger. The signal measures the wrong thing:
it reports a publication stale when any artifact appears under a work it cites,
not when an input it binds changes, so a paper on the virtues reported 156
changed inputs, every one a Clementine verse table it does not bind. And the
tooling under these papers is still moving — the calendars, the concordance, the
commentary chain and the source library all changed materially in a single day —
so anything this tooling will eventually invalidate, it has not finished
invalidating. A baseline taken now is taken against a moving one.

**Suspended, deliberately not rebaselined.** Rebaselining writes down that the
research was re-read against the changed inputs. That review did not happen, and
recording it would put a false statement in 24 editions to make a number go to
zero. Suspension records the true thing instead: measurement has stopped.

`make check-staleness` reports the suspension and exits clean;
`make measure-staleness` still runs the raw signal for anyone who wants to look
at it without acting on it. Nothing in the ledger or in any paper was touched.

**How this ends:** one full pass back through the research, when the tooling has
matured — not edition by edition as the flag fires. TASK-93 repairs what
staleness measures and is a prerequisite of that pass, not of lifting the
suspension.

Research is not limited to publicly reachable sources. On 31 July 2026 the
maintainer withdrew the rule that had forbidden purchasing an edition, using a
paid subscription, requesting credentials, or asking the maintainer to fund
source access, on the ground that it was never a requirement of anything — it
was a self-imposed limit that turned an ordinary cost question into a permanent
evidence gap. Where a witness would settle a question, name it and what it
would cost; the maintainer decides whether to obtain it.

Two things this does not change, because neither was ever a project rule.
Copyright and licence terms bind whatever the research budget is: a text the
project may read is not thereby a text it may republish, and the standing
public-alpha authorization is authority to distribute this project's own work,
never someone else's. And a witness that has not actually been consulted is
still unconsulted — record what was read, not what was reachable.

The maintainer authorizes creation and revision of project-owned AI artwork
for the sanctuary pictorial dictionaries and altar-server guide series. Each
asset must remain grounded in publicly reachable, source-controlled evidence;
carry its exact generation or edit provenance, references, hash, rights,
corrections, consumers, and review state; and remain visibly provisional where
review is open. Artwork may not invent or silently resolve an object's
identity, morphology, scale, arrangement, ceremonial use, historical state, or
an actor's liturgical action. AI creation supplies no human artwork,
liturgical, ceremonial, or ecclesiastical review.

No external human-review cycle will be available for some time. Human,
priestly, specialist, intended-reader, physical-use, and ecclesiastical review
are therefore neither promised workflow steps nor alpha completion gates.
Continue research, revision, artwork production, mechanical and AI-assisted
audit, building, installation, public-alpha binding, integration, push, and
deployment against the six concrete concerns above. Record an external review
only if it actually occurs, and never convert internal or AI checking into a
claim of human approval.

## Current integration and publication state

The repaired public-alpha snapshot is integrated on `main`; pull request 1 was
merged, and subsequent validated checkpoints have continued through the direct
`main` workflow. The stable review landing page, PDF, and web-edition routes
for the exorcism paper have resolved in production checks. The current
repository source, installed PDF, web edition, comprehensive plan, and exact-
snapshot audit agree on a completed bounded study of 116 physical pages,
including 103 substantive narrative pages. Each later `origin/main` checkpoint
requires its own successful Pages run and verification of the affected
production routes before it is represented as live.

## Clean direct-main workflow

For a clean direct Codex session started from current `main`, use this
instruction:

> Read `AGENTS.md`, `PROJECT-WORK.md`, `promised-deliverables.toml`,
> `guidance/promised-deliverables.md`, and the guidance and research records
> applicable to the first selected workstream. Reconcile the register against
> current `main` and production Pages before editing. Continue the highest
> actionable open requirement; do not infer completion from a commit, PDF,
> catalog link, push, or deployment. Update the register and ledger before each
> checkpoint commit. After validating each independently reviewable unit,
> inspect its exact outgoing range and push it to `origin/main`; then verify the
> resulting Pages run and affected production routes.

The restarting agent must then:

1. Run `git status`, confirm the current branch is `main`, reconcile it with
   `origin/main`, and preserve unrelated changes.
2. Confirm that `f6e9d2e2` is contained by `main`. If it is not, stop content
   work and report that integration remains open.
3. Run `tools/tpt check-promised-deliverables` and `make check`. Do **not** act
   on research staleness: it is suspended, `make check-staleness` reports the
   suspension, and the papers are left as they are until the tooling settles.
   `make check-source-family-screening` still fails, and honestly — 144 review
   units are unscreened and marking them screened would record a review that did
   not happen. Record the count; do not close it by writing it down.
4. Build and verify the public artifact with `tools/tpt public-alpha check`,
   `tools/tpt public-alpha build`, and `tools/tpt public-alpha verify
   --deployment-target github-pages`; separately verify the live production
   routes after Pages completes.
5. Resume in this order unless the maintainer gives a new priority:
   `task-2-exorcism-100-pages`; `project-recent-paper-hard-review`;
   `task-1-altar-server-guides`;
   `task-4-missa-cantata`; `task-5-solemn-mass`;
   `task-3-sanctuary-dictionaries`; `task-6-linen-restoration`; then the
   repository-wide staleness, source-family, exact-snapshot, and artwork queues.
6. For the exorcism work, begin with its tracked comprehensive expansion plan,
   scope, source audit, and final exact-snapshot review record. Acquire and
   verify research before drafting; preserve the 100 substantive-page
   requirement and the source, safety, law, PDF, web, and every-page gates.
7. Reconcile this file after each independently reviewable work unit. Keep
   completed facts, current evidence, open criteria, blockers, and superseded
   decisions distinct. Commit the coherent unit, run its required validation,
   inspect the exact outgoing range and public-exposure consequences, and push
   the checkpoint to `origin/main`. Verify the Pages result before calling that
   snapshot live, but never call the underlying deliverable complete unless
   its ledger gate passes.

Retained-worker integration, non-Pages deployment, remote changes,
force-pushing, and all other history rewriting remain separately authorized
operations.

## Promised work

### Corpus browser Wave 1 real-data design

<!-- promised-deliverable: corpus-browser-wave-1-design-2026-08-08 -->

**The Wave 1 design is a committed, pushed Candidate on `ux/corpus-wave-1`;
independent external review remains open.** The branch started from exact current
`origin/main` base `c27d6915319785686d1df6a1401a489aa9921f6f`. The
task-specific directions override the master plan's integration-branch
precursor, so no foundation-integration branch is claimed: accepted knowledge
and artifacts were carried selectively from Codex foundation SHA
`3b5938a0dba88831763ec09c762ae1572007a27e` and Claude foundation SHA
`af2c9613ccda48679face4e43f59c002f93056ef`. A0 and A1 are accepted; A2 is
accepted with amendments; A3 is accepted only as foundation direction, not as
pixel or production-route acceptance; and A4 is accepted with Jump bounded
pending J0--J2, Related typed, and the accepted liturgy boundary preserved.

The durable design authority is
[`guidance/corpus-browser-vision.md`](guidance/corpus-browser-vision.md); the
execution, evidence, and disposition register is
[`guidance/corpus-browser-roadmap.md`](guidance/corpus-browser-roadmap.md).

C0/C1, D0, E0, and F0 together form one real-data design candidate for Home,
the Publications catalogue at `/texts/`, the long-form Publication Reader,
Catena Omnia, and the Source Library. Its isolated `noindex` prototype is
injected over a real generated preview and exercises actual corpus content and
hard states. It changes no production source or route, canonical Day/Propers or
other liturgy behavior, PDF, release binding, deployment, or public navigation;
none of these candidate lanes is accepted or complete.

**Evidence and next handoff.** The immutable review record is
`build/agent-handoffs/20260809T000346Z-corpus-wave-1-design-review/`, with its
matching one-root ZIP. Its browser report covers 83 real-route cases and 1,979
assertions: 1,917 pass, 62 disclosed inherited findings are non-gating, and no
gate fails. It contains 83 main captures, all 25 required before/after pairs,
one 236-page Reader print PDF, and all 236 page rasters. The next action is
independent per-lane review of C0, C1, D0, E0, and F0, followed by recording the
actual disposition and any corrections. No merge, production implementation,
release, deployment, liturgy change, or PDF change is authorized by this
candidate.

### Live Reader — Ritual Flow & Orientation

<!-- promised-deliverable: liturgy-reader-live-ritual-flow-2026-08-07 -->

**In progress as a new production refinement phase against the independently
accepted live canonical Day and Propers readers.** The completed migration and
same-path cutover are not reopened. This phase protects the accepted first
viewport and Instrument foundation while improving sustained-reading
orientation, making Contents a current-place map, and restoring hierarchy
between principal ritual action and source-owned rubric, provenance, or
conditional/reference material.

The implementation may expose existing semantic and renderer state through
narrow shared presentation hooks. It may not manufacture liturgical
applicability, locality, selection, source, translation, or content. Search,
Study, Compare, print redesign, public-navigation redesign, candidate/oracle
cleanup, source/translation/recension expansion, and a new visual direction
remain separate and unauthorized. Exact baseline, decisions, checkpoints,
Pages runs, and the independent-review stopping point live in
`build/agent-continuity/liturgy-reader-visual-plan.md`.

### Liturgical Instrument public cutover

<!-- promised-deliverable: liturgy-reader-instrument-public-cutover-plan-2026-08-06 -->

**Complete; the canonical Day and Propers URLs serve the independently accepted
Liturgical Instrument, public navigation is unchanged, and retained candidate
and oracle cleanup is deferred.** Planning began from synchronized accepted-
integration boundary `7b7044dea7f5c35a2d32ff85f26eb5b182bf40ef`. It inventoried
the canonical `liturgy/day.html` and `liturgy/index.html` contracts against
the accepted `liturgy/day-reader.html` and `liturgy/propers-reader.html`
implementations, selected same-path promotion as the smallest reversible
mechanism, made the disclosed date-dependent Day gate deterministic without a
product change, and produced exact patch, rollback, acceptance, deployment,
and cache-window procedures.

Independent review accepted source-level same-path promotion behind the
unchanged canonical filenames, the rollback and static-hosting model, the
canonical-route and visual-oracle gates, and the deterministic Day fixture. It
also fixed the compatibility decisions: Roman 1962 is the intentional empty-Day
default; `why=1` and every held territorial branch are preserved; Propers uses
stable `cycle`, `alternative`, and `translation-witness` keys; retained
candidates are source-static noindex; visible controller wording is route-
neutral; and counterpart/context navigation belongs in Details without a fifth
primary action. Compatibility implementation
`3f3949617a04ffa68a1070058d0f7bc5ac74dc93` closes those contracts on the
authorized candidate/shared seams. Pages run `31148986910` succeeded for that
exact commit. Day passes 40/40, Propers 32/32, the shared shell 18/18, and
governed visual assertions 24/24 over 113 captures. Production integration,
compatibility closure, and their durable handoffs are independently accepted
and complete.

Planning checkpoint `c7124de25` records the route, state, navigation, static-
hosting, cache, mechanism, rollback, and execution-gate maps. Test-only commit
`5e1b82b51` proves and removes the disclosed wall-clock dependency while
keeping the first-visit URL empty. The obsolete first patch was superseded
after gate repair by the accepted 19-path patch. Its prospective 230/230 focused
Python, 40/40 Day, 32/32 Propers, 18/18 shared-shell, and 24/24 governed
Instrument gates were repeated successfully in the promoted real tree before
commit. Planning and compatibility packages remain at
`build/agent-handoffs/20260806T212148Z-liturgy-reader-instrument-public-cutover-plan/`
and
`build/agent-handoffs/20260807T052836Z-liturgy-reader-public-cutover-compatibility/`.

Independent post-deployment review passed all nine final questions and accepts
the public cutover as complete. Exact cutover SHA
`9b5f21c0ca26bf02af03d207ddd2617021e16fb3` owns qualifying successful Pages
run `31175722949`. Immediate live verification passed 936/936 across 36
original-pixel states; ordinary-cache verification passed 216/216 after 613
seconds without mixed-generation behavior. The immutable execution handoff is
`build/agent-handoffs/20260807T115341Z-liturgy-reader-instrument-public-cutover-execution/`;
its ZIP SHA-256 is
`06752126a3a3235a342f54ec08811faaf4fc2622924008c4362dda519624c410`.
Canonical Day and Propers now serve the accepted Instrument without redirects.
Public navigation was not redesigned; retained candidate and oracle routes
remain intact and nonindexable, and cleanup is deferred and unauthorized. The
governed full gate remains non-green only at the unrelated stored-example
transcript replay; no transcript was recaptured or blessed.

### Liturgical Instrument production integration

<!-- promised-deliverable: liturgy-reader-instrument-production-integration-2026-08-06 -->

**Complete; production integration is independently accepted and its exact
reviewed handoff is durably archived. The separately reviewed public cutover is
also complete; public-navigation redesign remains outside both phases.**
Independent Round 1 accepted the
Liturgical Instrument visual foundation and all seven correction dispositions.
Production integration begins from `b3ae6bddaab631661d342380f61365d851be160c`
through four bounded units: PI-A inventories the accepted hooks and selects the
smallest shared presentation seam; PI-B integrates the shell and Day
Read/Missal presentation; PI-C proves Propers Read/Browse parity; and PI-D
captures the full parity matrix, runs the governed checks, and assembles an
immutable integration-review candidate.

The completed inventory selects a new last-loaded, candidate-scoped
`src/web/browser/liturgy/reader-instrument.css` layer. This keeps public-loaded
`day-missal.css` unchanged and preserves `reader-shell.js`, the M1 state and
adapter owners, production renderers, Ordinary seating, invalid-state failure,
semantic-location restoration, focus, race ownership, and the four one-step
actions. Stable masthead and action-label hooks are added to the two production
candidate HTML files. Only generation-safe presentation composition may touch
the Day or Propers adapters: the authoritative Day commit exposes its current
mode as a styling attribute, and renderer-owned absence nodes may be grouped or
moved without replacing their text or semantics. The accepted comparison
prototype remains unmodified and available as the parity oracle. That seam is
now implemented in both unlinked candidates. The extended Chromium harness
passes 19/19 assertions over 100 captures and includes 23 exact
prototype/production pairs covering Read, Missal, partial coverage,
postconciliar coverage, Propers, all open surfaces, deep scroll, 200% text,
forced colors, reduced motion, and keyboard focus. The accepted 768×1024
636-pixel/~75-character measure is exact; production mobile Missal principal
text is 3.43 pixels earlier than the accepted oracle and otherwise retains the
same 351-pixel plane and action geometry.

Successful deployed correction parity remains Pages run `31109086658` for
`c388ab42dfc4f5c7d49abc71596d6bb511af5742`. Later runs
`31110517661`, `31113461987`, and `31114653517` each passed repository-owned
build/upload work and then failed at GitHub deployment polling; none is claimed
as successful. The production-integration deliverable remains open until its
own evidence, deployment record, and independent integration disposition are
complete. The implementation checkpoint is not represented as deployed until
its own push has a successful Pages result and direct asset verification.
Implementation commit `3cd46072b164ff39b00639bb67ad6b8943a255dc` is pushed
to `origin/main`. Its clean-tree full gate reached only the governed unrelated
example-replay divergence: 200 examples, 188 replayed, 23 divergent, 35 known
stale, 6 never run, and 6 unrunnable here. It exits 2 and is not represented as
green. As of 2026-08-06T18:04:26Z, GitHub had not materialized the automatic
Pages run for this push in the Actions API; this is recorded as a pending
workflow event, not a deployment success or failure.
Continuity checkpoint `e35f81c1e67c744aead0e4eaa73e079516751e66` is also
pushed. As of 2026-08-06T18:08:35Z GitHub likewise had no Actions record for
that head. Direct deployed Day and Propers candidates remain HTTP 200 at the
prior artifact, which does not contain `reader-instrument.css`; deployed
integration parity therefore remains explicitly open.
GitHub later materialized automatic run `31125352169` for implementation commit
`3cd46072b164ff39b00639bb67ad6b8943a255dc`, but at
2026-08-06T18:27:03Z it had remained queued for more than 15 minutes with no
runner or repository step started. This is a queued external-state result, not
a successful or failed deployment; deployed parity remains open.
The next delayed automatic run, `31125898045`, succeeded for exact intended
production commit `5444d89fc9b379a1babef5b2220323fe1508b2b3` at
2026-08-06T18:29:55Z. Every repository build, verification, upload, and deploy
step passed. Direct Day, Propers, and both accepted oracle routes return HTTP
200; Day/Propers reference the Instrument stylesheet, the oracle routes remain
noindex, and deployed Instrument CSS, Day/Propers JavaScript, and accepted
oracle CSS/JavaScript byte-match source. Deployed production-integration parity
is complete. The deliverable remains a candidate solely for independent
integration review; public navigation and cutover remain unauthorized.

Independent production-integration review passed all six requested questions:
Day parity, Propers parity with canonical Browse retained, responsive shell and
accessibility behavior, reading and ritual geometry, frozen behavioral/source
ownership, and final integration disposition. No product, visual, evidence,
harness, or deployment correction was requested. The only closeout finding was
that the exact reviewed handoff remained ignored locally.

Under the review's path-bounded force-add authority, archival commit
`8c6e1270f692ca4136f2f6a60002bacd3af0440c` pushes the byte-identical reviewed
directory and ZIP. All 216 manifest entries verify, the archive has one
top-level directory, and its SHA-256 remains
`ebf0361309ac33b4580cbb535e4bbd3eabd144756e6c078aa140e716c748f05f`.
The canonical continuity file carries the complete review and Codex response.
Production integration and durable handoff closeout are therefore complete.
At that integration boundary the Day browser remained 33/34 only at its
date-dependent expectation; the subsequent deterministic cutover fixture and
canonical execution pass 40/40. The full gate remains non-green only at
unrelated example transcript divergence. The separately reviewed public
cutover is now accepted and complete; public-navigation redesign was not part
of it.

### Liturgical Instrument visual correction accepted

<!-- promised-deliverable: liturgy-reader-instrument-correction-2026-08-05 -->

**Complete; independent Round 1 acceptance authorized the now-complete
production integration, but did not itself authorize navigation or cutover.**
Liturgical Instrument is the
accepted production visual foundation. Quiet Folio and Contemporary Reader
remain frozen comparison references, and the accepted visual and behavioral
seams are not reopened absent a concrete production-integration conflict.

The bounded correction owns seven findings: integrate the persistent controls
with the reading composition; advance the first principal Missal text; remove
the empty Read gutter; constrain the 768-pixel portrait measure; subordinate
partial and postconciliar coverage warnings to available text; replace or
simplify the provisional masthead mark and progress treatment; and finish
mobile ritual spacing and narrow division-title wrapping. The canonical plan,
review mailbox, measurements, checkpoint record, and resume state are tracked
at `build/agent-continuity/liturgy-reader-visual-plan.md` under this task's
explicit build-tree exception. Work units A–C now implement and measure the
bounded visual corrections: one 39.75rem Read axis, earlier Missal action,
integrated rail/dock, authored masthead, consolidated warnings, tighter ritual
rhythm, and deliberate 320-pixel wrapping. Work unit D now supplies the full
matrix, measured before/after package, honest governed-check record, verified
Pages deployment, and immutable tracked handoff at
`build/agent-handoffs/20260806T112813Z-liturgy-reader-instrument-correction/`.
Independent review round 1 passed six of seven original findings and confirmed
the direction, typography, ritual grid, warnings, masthead, and Ordinary/Proper
composition. It retained the original shell blocker only at 1024×768 and added
the related 200%-text mid-word label reflow blocker. The bounded follow-up now
uses the opaque square edge dock immediately below the 72rem rail breakpoint
and a labeled 2×2 dock only at extreme root-font reflow. The 54-capture run
passes 15/15 assertions, including end-content reserve, whole labels, accessible
names, target size, and overflow. Correction commit
`ab89758e3f3ee165e0141e3605be88051450134b`
is pushed. Its first Pages run passed every build/verification step but timed
out while GitHub held the deployment queued, so deployed corrected-asset parity
remains open and is not claimed. A second automatic run for continuity
checkpoint `c6b7f7f0a79468cfa1a503235044c92bd88c27b2` again built and uploaded the
verified artifact, then timed out only in deploy-pages polling; the durable
continuity record owns both exact stops. A third automatic run again passed all
repository-owned build/upload work and was canceled only when the job reached
its 15-minute ceiling during deploy polling. The following immutable-handoff
push succeeded as Pages run `31109086658`; direct Day/Propers routes are HTTP
200/noindex and deployed CSS/JS byte-match source. The final narrow immutable
re-review handoff is
`build/agent-handoffs/20260806T141831Z-liturgy-reader-instrument-correction/`.
Independent Round 1 acceptance passed shell continuity, 200% labeled reflow,
and absence of accepted-geometry regressions. It independently verified the
ZIP, all 109 manifest entries, candidate/source CSS parity, and all corrected
original-pixel screenshots. Production integration may now begin through the
shared presentation seam; it must stop for independent integration review
before any separately authorized public cutover. Pages run `31110517661` for
post-deployment evidence commit `4daf7d8a1e1c509edb81a738cc71223170bbbd2d`
failed at deployment polling and is not represented as successful; successful
deployed parity remains owned by run `31109086658` for
`c388ab42dfc4f5c7d49abc71596d6bb511af5742`.
The acceptance-record push at `1608f0ee0ee61df956247072a91647147548c5ad`
passed every repository-owned Pages build/upload step, then run `31113461987`
failed after 600 seconds of `deployment_in_progress` polling. Direct prototype
routes remain HTTP 200/noindex and their deployed CSS/JS still byte-match the
accepted source; the new run is not represented as successful.

Accepted M1–M3 and W3 state, assembly, renderers, Ordinary seating, failure,
location, focus, race, action-reachability, and isolation behavior remain
binding. This completed correction does not add Study, Compare, search, Propers
Missal, sources, editions, recensions, translations, or public links, and it
does not change `liturgy/day.html` or `liturgy/index.html`.

### Liturgy reader visual-reset direction candidate

<!-- promised-deliverable: liturgy-reader-visual-reset-candidate-2026-08-05 -->

**Complete as a direction-selection study; Liturgical Instrument selected.**
The completed M1–M3 and W3 records remain authoritative for state,
production assembly and rendering reuse, fail-closed behavior, focus and
semantic-location restoration, responsive access, and render-race ownership.
They were never a finding that the beige card, enlarged mobile-style command
bar, improvised glyphs, typography, spacing, or desktop composition constituted
a finished or world-class visual reader.

This distinct visual-design work item compared Quiet Folio, Liturgical
Instrument, and Contemporary Reader over one shared semantic DOM and interaction
foundation. It uses real production Day Read/Missal and Propers Read content at
unlinked, noindex prototype routes, while preserving the accepted state,
calendar, Ordinary seating, Proper rendering, source, and coverage boundaries.
Its external review selected Liturgical Instrument. The work does not reopen
the completed Day Missal engineering deliverable, alter public Day or Propers,
start Study/Compare/search, or authorize public cutover.

The visual-reset candidate was implemented and independently reviewed, with
**Liturgical Instrument selected as the production visual foundation**. Quiet
Folio is the calmest editorial leaf; Liturgical Instrument adds an edition-neutral
ritual cue grid, disciplined divisions, and a speaker/action gutter for actual
following; Contemporary Reader supplies the most compact application chrome
and polished title-led Propers Browse flow. All three are query-selected
presentations over the same HTML, SVG icon set, shared shell controller, and
accepted Day/Propers production adapters. The selection favors Instrument's
continuous ritual legibility. Folio and Reader remain frozen comparison
references rather than ingredients for a merged compromise. The review also
found seven bounded visual blockers, now owned by
`liturgy-reader-instrument-correction-2026-08-05`; selection does not make the
foundation world-class or authorize production integration.

The current evidence contains 52 same-run comparison captures at the required
desktop, tablet, mobile, enlarged-text, forced-color, reduced-motion, keyboard,
deep-scroll, surface, partial-coverage, and before/after states. Twelve focused
Chromium assertions pass with no console, failed-request, HTTP, overflow, or
unnamed-interactive-node result; a 26-page PDF is retained only as a print smoke
check, not a print redesign. Exact hashes prove the public Day and Propers
routes, both accepted candidates, shared shell, M1 state seams, production
seating, and accepted adapters unchanged. The implementation is this candidate
commit; its immutable visual-review handoff was created after the validated
push. The direction-selection decision is complete. Corrected visual review,
production-integration execution, and every public-cutover decision remain
open under the separate correction deliverable above.

### Liturgy Day Missal-mode W3 integration accepted

<!-- promised-deliverable: liturgy-day-missal-w3-candidate-2026-08-05 -->

This task extends the accepted internal Day reader at
`liturgy/day-reader.html` with the next bounded W3/M3 production-integration
slice: Read remains the default appointed-Propers view, and Missal presents the
continuous production Ordinary with those same propers seated at their actual
semantic locations. The candidate must reuse the accepted M1 Day state,
production calendar assembly, Ordinary data and renderer, Ordinary seating,
and shared Proper renderer. It may not create a second liturgical sequence,
renderer, seating engine, event-order engine, URL parser, or public route.

**Accepted** — the internal W3 Day Missal-mode integration has passing
implementation and independent external-review evidence. Its contract includes
Roman 1962 and postconciliar parity,
fail-closed Ordinary language and Eucharistic Prayer handling, explicit
coverage and absence,
semantic-location preservation across Read/Missal and history transitions,
race ownership, responsive and accessible interaction, continuous Missal
print, performance measurement, and production isolation. Study, Compare,
Propers Missal mode, search, new recension or source coverage, public route
cutover, and redesign of the accepted shell or complete print system remain
out of scope.

The implementation base is
`c4c071d6ba962524487bc8f4c6a4b781981851c7`. The initial candidate, two bounded
corrections, three immutable handoffs, and their successive review dispositions
remain recorded below as the durable audit trail. This acceptance does not
amend the accepted M1, M2, M3, or Propers Read records.

External review of implementation
`a1221755d4fac2a6b9a009a91b99cd1da82eee9e` and immutable handoff
`20260805T145914Z-day-missal-mode-integration` returned **changes requested**.
It passed the production-renderer, seating, edition, option-validity,
ergonomics, isolation, and scope boundaries, but identified three bounded
acceptance blockers: non-ready outcomes can retain history-dependent mode
chrome; an inline Eucharistic Prayer change replaces the focused radio without
restoring its semantic equivalent; and direct-load evidence can observe an old
ready flag before the new document's render commits. Correction work is limited
to deterministic outcome presentation, inline-option focus restoration, and
generation-safe browser assertions and replacement captures. The candidate and
its independent external-review requirement remain open; no acceptance,
closeout, public cutover, or deployment is authorized by the correction work.

The bounded correction is now implemented and locally proven, but remains
**pending independent correction review**. Every render outcome commits one
mode presentation (including a neutral, unchecked presentation for invalid
`ordinary` state); invalid, deferred, unresolved/territorial, and unrenderable
outcomes carry distinct diagnostics; and stale navigation, location, focus,
metadata, and selection state is cleared before an outcome commits. Keyboard
changes among the postconciliar Eucharistic Prayers restore focus to the newly
rendered checked radio without losing the semantic reading location. The
browser harness now distinguishes fresh documents by a unique non-semantic
query nonce and document token, and same-document transitions by an exact hash
and a greater committed render generation, followed by the UI's animation-frame
boundary. The complete browser and print evidence was regenerated with that
harness. These results resolve the three correction requirements for re-review;
they do not accept or close the candidate.

External review of correction
`ce5fce8364d24156e41c444c43673e7de31555d8` and immutable handoff
`20260805T183500Z-day-missal-mode-corrections` returned a second, narrowly
bounded **changes requested** disposition. The substantive product corrections
passed review: deterministic outcome chrome, neutral invalid-Ordinary state,
distinct failure classes, inline-option focus restoration, generation-safe
document navigation, and production isolation remain accepted correction
evidence. Acceptance is still blocked because the Chromium harness waited only
two animation frames while inherited smooth scrolling could remain in flight,
and because duplicate `ordinary` keys were not exercised directly in Chromium.
The evidence-settlement correction is limited to animation-frame scroll/target
stability, settled default- and reduced-motion Eucharistic Prayer focus proof,
both duplicate-key orderings from fresh and transitioned states, wholly
regenerated evidence, and a new independent handoff. Product reader and shared
shell behavior remain unchanged unless settled testing proves a real defect.
The candidate, completion count, and external-review requirement remain open.

The evidence-settlement micro-correction is now implemented and locally
proven, but remains **pending independent external review**. Committed-render
synchronization still requires exact document tokens and generations; a
separate animation-frame loop now requires five stable scroll/target/focus
frames, viewport intersection, cleared pending navigation, and a bounded
diagnostic timeout before assertion or capture. Default-motion keyboard changes
through EP I, III, IV, and II and a separate reduced-motion change preserve the
settled semantic event and checked-radio focus. The stabilized test exposed one
local Day-adapter defect: the correctly focused checked radio could settle above
the viewport. The adapter now aligns that inline option group deterministically
after semantic restoration, leaving the shared shell and global scrolling rules
unchanged. Both `ordinary=0&ordinary=1` and `ordinary=1&ordinary=0` now produce
neutral, unchecked mode chrome on fresh loads and transitions from Read and
Missal. All browser and print evidence was regenerated; the public routes,
Propers candidate, shared shell, M1 seams, seating, and production data remain
unchanged. These results satisfy the bounded proof requirement for re-review;
they do not accept, close, deploy, or cut over the candidate.

Independent external review now **accepts and closes this internal W3 Day
Missal-mode slice** at micro-correction
`86a9816c1bffdcbdd09469f5f8d005c666a8045e`; every blocking review question is
resolved and no further handoff is required. The complete reviewed sequence is
candidate `a1221755d4fac2a6b9a009a91b99cd1da82eee9e`, first correction
`ce5fce8364d24156e41c444c43673e7de31555d8`, and the accepted micro-correction
above, with immutable handoffs
`20260805T145914Z-day-missal-mode-integration`,
`20260805T183500Z-day-missal-mode-corrections`, and
`20260805T201722Z-day-missal-mode-evidence-corrections`. Acceptance covers
reuse of the production Ordinary presenter, Proper renderer, M1 event stream,
and single seating path; Roman 1962 and postconciliar structures;
deterministic fail-closed state; semantic location, history, and render-race
ownership; settled inline Eucharistic Prayer keyboard focus; responsive,
accessibility, performance, and print evidence; and production isolation. It
does not authorize public-route cutover, public links, Propers Missal mode,
Study, Compare, search, source or recension expansion, or print redesign.

### Liturgy Propers Read W3 integration accepted

<!-- promised-deliverable: liturgy-propers-read-w3-candidate-2026-08-04 -->

**Accepted** — the W3 Propers Read integration enters the same production
reader shell as the accepted Day candidate, preserves current valid formulary
semantics through the M1 Propers state and production Proper renderer, leaves
missing identity unresolved, fails closed on invalid state, preserves cycles
and alternatives independently, requests translation witnesses only when
formulary-specific translated material requires a choice, and remains isolated
from the public Day and Propers routes.

External review first requested bounded Browse witness, Browse-race, tracking,
and handoff corrections from candidate
`b0b1e5b63ba4a1d389b53276fa0bf9944c0ee909` and handoff
`20260804T212821Z-propers-reader-shell-integration`. It then accepted correction
`1e4587dfe04a11c18e996a16f7fbbdb54bc744a4` and immutable handoff
`20260804T225215Z-propers-reader-shell-corrections` after manifest verification.
The reviewed evidence records 84 focused M1/shell/Day/Propers tests, 90
public-alpha/gallery tests, and respectively 27, 25, and 18 Chromium assertions
for Propers, Day, and the shared shell. The exact shared-shell hashes are
`bf1c062453f8fcfd5a68c1fe30e31aca89ea1a3c8adeef9a5525d8081ae8c707`
for `reader-shell.js` and
`e7195cd86ed4fc4a8455e97369702239eb22d709a13d3d8462d7759c01fe814a`
for `reader-shell.css`.

Production-isolation evidence confirms that public Day and Propers, the
accepted Day candidate, navigation and selectors, M1 semantics, production
liturgical and generated data, and public URL behavior remain unchanged. The
approved example baseline remains the same 23 unrelated pre-existing records
and the same two promised-deliverable commands; acceptance changes only the
candidate count from 18 tracked, 12 complete to 18 tracked, 13 complete.
Public cutover, Missal, Study, Compare, search, and recension expansion remain
deferred. Excess cycle-choice print whitespace remains non-blocking debt for a
later print-refinement workstream.

### Liturgy Day reader-shell M3 accepted

<!-- promised-deliverable: liturgy-day-reader-shell-m3-candidate-2026-08-04 -->

The first W3 integration slice extracts the accepted quiet persistent reader
shell into a reusable production foundation and connects an unlinked, noindex
Day Read-mode candidate to the existing production assembly and rendering path
through the accepted M1 reader-state boundary. The candidate preserves
Read-compatible legacy URL meaning, fails closed on invalid explicit state,
and discloses later-mode state with an equivalent link to the unchanged live
Day route rather than silently dropping or partially rendering it.

This was an **M3 candidate pending external review**, not a production cutover.
The live Day and Propers routes, public navigation and selectors, M1 semantics,
liturgical and calendar data, and generated public data remain outside the
implementation boundary. Missal, Study, Compare, Propers integration, search,
and public release remain deferred.

The candidate is implemented at the unlinked `liturgy/day-reader.html` build
route. `reader-shell.js` and `reader-shell.css` contain only the accepted
persistent action bar, modal lifecycle, focus and scroll restoration, semantic
Contents tracking, responsive sheets, safe-area behavior, and print removal.
The separate Day adapter parses and validates M1 state, calls the existing
calendar assembly and M1 Day adapter, and renders the selected real production
Proper with the existing shared renderer. It supports date, missal, Bible,
oration language, and readable-formulary state; it preserves later-mode state
and links it intact to `day.html`, and it fails closed on invalid explicit
values.

Focused static, M1, current-route, Ordinary, public-alpha, and real-Chromium
checks cover both production-backed M1 Day fixtures, a readable displaced
formulary, typed partial coverage, invalid and deferred state, all four modal
surfaces, 320-pixel and 200% reflow, accessibility, deep-scroll reachability,
Back, lazy Details, print, and live-route parity. The immutable external-review
handoff is `20260804T154620Z-day-reader-shell-integration`. M3 remains a
candidate until external review accepts it.

External review accepted the W3 architecture and requested three bounded
corrections before M3 acceptance. The correction distinguishes inactive latent
Ordinary, rubric, and why preferences from active later-mode requests; clears
all selection-specific state before every render attempt so rejected,
unresolved, deferred, or failed navigation cannot expose an earlier result;
restores exact weekday presentation from the assembly model; and keeps raw
source-hook coordinates out of reader-facing Details. The compact correction
handoff is
`20260804T173010Z-day-reader-shell-integration-corrections`. M3 remains a
candidate pending correction review; the live Day and Propers routes remain
unchanged.

M3 is now **accepted**. Accepted — the production Day Read candidate reuses
the existing assembly and Proper renderer behind the shared persistent shell,
preserves Read-compatible legacy state, explicitly defers later-mode state,
fails closed across invalid and superseded asynchronous transitions, and
remains isolated from the live Day and Propers routes. The final serial-token
micro-fix is `c604edb8a1fffb1e5c0981798800ecb801258e7c`; deterministic Chromium
tests release delayed valid, malformed, invalid-destination, and history
requests only after the newer outcome is ready, then prove that identity,
Proper text, Contents, Date, Details, semantic state, and render counters do
not change.

Acceptance evidence comprises original candidate
`45a6b76249e015f68830495ca2971e9dbc4a4e14`, correction
`d0872545ccc92106cb457b448f37201381c5bb2d`, the final micro-fix above,
handoffs `20260804T154620Z-day-reader-shell-integration` and
`20260804T173010Z-day-reader-shell-integration-corrections`, the original W3
changes-requested review, and the W3 conditional-acceptance disposition. M3
acceptance does not replace or redirect live Day, integrate Propers, expose
public navigation, begin later modes, authorize public cutover, or begin the
1956–1960 recension.

### Liturgy reader-shell M2 accepted

<!-- promised-deliverable: liturgy-reader-shell-m2-candidate-2026-08-03 -->

The first W2 milestone is a visible, interactive, responsive shell prototype,
not a production-route integration. It will live in an unlinked nested
`src/web/browser/liturgy/prototypes/reader-shell/` route, which the existing
top-level-only public browser copier excludes. The candidate must reuse the
current Proper renderer, keep Day and Propers as distinct entrances to one
shared shell, compare quiet persistent and scroll-reveal reachability, and
measure wide, intermediate, mobile, 320-pixel reflow, accessibility,
performance, and print behavior. It may use clearly marked M1 contract-only
fixtures for Compare and unresolved-choice layout, but it must not implement
later semantic engines or change public generated data.

The candidate now has one shared shell, persistent and scroll-reveal variants,
real-renderer Day and Propers states, layout-only later-mode fixtures, semantic
Contents, a coherent Study apparatus, 94 responsive review captures, a tagged
four-page print review, and focused static and real-browser coverage. The
measured decision recommends the quiet persistent shell: every global action
remains one activation away at deep scroll while the shell occupies about
58–59 CSS pixels and causes no measured layout shift. The immutable handoff is
`20260804T101952Z-liturgy-reader-shell-prototype`.

External review of candidate `68becc59b396aca830c233b88ec74991563603d1`
in handoff `20260804T101952Z-liturgy-reader-shell-prototype` accepted that
persistent-shell direction and the shared Day/Propers model, but its *M2
prototype changes-requested disposition* required three bounded corrections.
Correction `75234e72c402f0b25a681fbe074da70d895f7274`, reviewed through handoff
`20260804T142747Z-liturgy-reader-shell-corrections`, removed complete-state
diagnostic noise, eliminated auxiliary-surface overflow and raw
machine-shaped Study output, and distinguished temporary Details from pinned
wide-desktop Study and reversible mobile Study sheets.

Accepted on 4 August 2026. The *M2 responsive reader-shell acceptance and
closeout disposition* records: **Accepted — the quiet persistent reader shell
is the M2 direction. Complete Read states are free of diagnostic noise, all
auxiliary surfaces reflow without internal horizontal scrolling, and
temporary Details is distinct from wide-desktop pinned Study and mobile Study
sheets. Production Day and Propers routes remain unchanged.** Focused shell,
M1, current-route, public-alpha, Chromium, print, syntax, registry, and
whitespace checks passed. The repository example comparison preserves the 23
pre-existing divergences and changes only the same two promised-deliverable
rows from `16 tracked, 10 complete` to `16 tracked, 11 complete`; no transcript
was modified or recaptured. Scroll-reveal remains prototype evidence only.
M2 acceptance does not start M3, W3, W4, W5, or production integration, and it
does not change M1 semantics, current URLs, calendar or liturgical data,
search, semantic comparison, or recension coverage.

### Liturgy reader-state M1 accepted

<!-- promised-deliverable: liturgy-reader-state-m1-2026-08-03 -->

The first W1/W9 integration slice defines one versioned, DOM-free semantic
reader-state and legacy-URL contract for the distinct Day and Propers
entrances. Production-backed and explicitly non-public synthetic fixtures hold
identity, calendar result, semantic event order, Proper and Ordinary seating,
text selection, provenance, typed coverage and absence, unresolved choices,
and Compare anchors across Day, Propers, and `mass-today --expanded` without a
second liturgical engine or a visible production change.

Accepted on 3 August 2026. The implementation at
`259573d393cd6a6bac09fc751ac1d14ec9477853`, the reviewed cycle and validation
correction at `c6b8070ae76e75153448895a19a0b916c18806ea`, and the final
property-presence micro-fix at `c1a590f5854215d68d167d9040e188f41762663e`
preserve Propers cycle alternatives and make explicit `sourceHooks` fail
closed unless they are arrays. The external review dispositions *M1 liturgy
reader-state contract*, *M1 reader-state corrections*, and *M1 acceptance
closeout count delta* accepted the resulting contract; the focused suite
passed all 38 tests. The full repository gate remains red only at the approved
23-entry example baseline and the same two promised-deliverable captures, whose
sole authorized closeout change is `15 tracked, 9 complete` to
`15 tracked, 10 complete`. No transcript was recaptured. The deployed Day and
Propers routes still do not load either M1 module, and this acceptance does not
begin W2, W3, or W7 or integrate visible reader behavior.

### GPT deep-research redevelopment

<!-- promised-deliverable: project-gpt-deep-research-redevelopment-2026-07-29 -->

The maintainer identified substantive underdevelopment—not merely stale dates
or presentation—in five GPT publication leaves: the 1962 Tenth Sunday after
Pentecost; Years A, B, and C of the postconciliar Eighteenth Sunday in Ordinary
Time; and *Catholic Exorcism: History, Discipline, and Pastoral Practice*. Each
requires a full source-first redevelopment that broadens the relevant source
families and deepens treatment of the strongest witnesses, material
disagreements, transmission, and limits. Existing prose is provisional, and
page count or repeated source summaries do not establish completion.

The authorized scope is GPT only. Claude publications may be inspected to
understand cross-provider staleness or dependencies, but they must not receive
material source, PDF, web, catalog, release, or baseline changes under this
work. Provider-neutral reusable evidence may be corrected or extended only
where the GPT research requires it; such a change does not authorize rebuilding
or revising a Claude consumer. Completion requires current publication-local
research records, source and rights gates, rebuilt and installed GPT PDFs and
web editions, every-page visual inspection, coherent release records, and
validated pushed checkpoints.

Completed 29 July 2026. The five GPT leaves now contain new comparative
research dossiers or synthesis, checked reusable source records and bindings,
superseding material-change reviews, and exact production records. Nine PDFs
(the five full publications and four proper syntheses) and five canonical web
editions were rebuilt, inspected page by page, installed with exact build
identity, and passed the repository's metadata, component, web-currentness,
source-library, source-inventory, source-family-screening, public-alpha, and
release-binding gates. The affected GPT staleness records are fresh. No file
under `src/claude`, `pdf/claude`, or `web/claude` changed.

### Exorcism reference

<!-- promised-deliverable: task-2-exorcism-100-pages -->

The requested result is a researched, substantive 100+ page Catholic exorcism
reference, not a padded PDF. The current public-alpha edition is 120 physical
pages, of which the first 108 numbered pages are substantive narrative under
the tracked exclusion rule. The comprehensive plan, delivery plan, source
audit, evidence map, scope record, and final exact-snapshot review agree that
the bounded representative study meets the promised extent and that its
source, evidence, rights, safety, jurisdiction, currentness, PDF/web anti-
drift, and every-page visual gates pass on one exact snapshot. The installed
PDF and reviewed build are byte-identical, as are the freshly generated and
tracked web editions. Protected critical editions, direct control of 1614
p. 220, exhaustive manuscript collation, additional local rites and cases,
and Eastern particular law remain explicit future-research ceilings; they do
not reopen the bounded completion verdict or imply ecclesiastical approval.
The controlling evidence is
`research/final-exact-snapshot-review-2026-07-29.md` beside the publication.

### Linen-cloths restoration

<!-- promised-deliverable: task-6-linen-restoration -->

Commit `242aa461` restored bounded burial-practice and material context in the
GPT paper and rebuilt its artifacts. Both provider editions now have one
reproduced exact-current snapshot: the GPT and Claude PDFs rebuild
byte-for-byte to the installed artifacts, their web conversions likewise
match, and all 46 pages have current visual-review evidence. Exact-byte
distribution clearance and internal review do not imply independent
exegetical, patristic, rabbinic, text-critical, or ecclesiastical approval.

### Altar-server guide series

<!-- promised-deliverable: task-1-altar-server-guides -->

Commit `be940904` repaired the seven guide/card PDFs and replaced the four
retained old Low Mass images. All are publicly discoverable review copies on
the branch. The current PDFs carry no reader-facing release-state strip or
label; page counts, card counts, maps, hashes, and production records agree,
and every page has been visually reviewed.
The remaining ledger requirement is exact-snapshot agreement among the Low
Mass and trainer PDFs, maps, hashes, artwork records, and every-page visual
evidence. Rights or liturgical-text permission uncertainty and any concrete
source, safety, artifact, mechanical, or visual defect remain open when
recorded; unavailable external review is not a placeholder gate.
The series-wide sequenced checklist is
`src/gpt/liturgy/roman-rite/1962/reference/altar-server-guides/research/delivery-work-plan-2026-07-27.md`;
it governs the shared Low Mass work and the Missa Cantata and Solemn Mass
deliverables without conflating their remaining gates.

### Sanctuary pictorial dictionaries

<!-- promised-deliverable: task-3-sanctuary-dictionaries -->

The six sanctuary pictorial dictionaries have current inventory, omission,
source, artwork, page-count, and review records that agree with their installed
PDFs. The artwork validator reports zero notices; unsupported identities or
uses remain omitted or held rather than being invented. These objective
records establish the current alpha state without implying human artwork,
priestly, or ecclesiastical approval.
The sequenced inventory, artwork, edition, and publication checklist is
`src/gpt/liturgy/roman-rite/1962/reference/roman-sanctuary-dictionary/research/delivery-work-plan-2026-07-27.md`.

### Missa Cantata guide and cards

<!-- promised-deliverable: task-4-missa-cantata -->

The rebuilt guide and cue cards are installed and linked as public-alpha
copies. Completion remains open until their source support, rights and
distribution status, safety, artifact consistency, mechanical correctness,
and every-page visual evidence agree on one exact snapshot. This does not
imply external ceremonial or ecclesiastical approval.

### Solemn Mass guide and cards

<!-- promised-deliverable: task-5-solemn-mass -->

The rebuilt guide and cue cards are installed and linked as public-alpha
copies. Completion remains open until their source support, rights and
distribution status, safety, artifact consistency, mechanical correctness,
and every-page visual evidence agree on one exact snapshot. This does not
imply external ceremonial or ecclesiastical approval.

### Review-publication discoverability

<!-- promised-deliverable: project-review-discoverability -->

Repository policy now keeps produced PDFs discoverable while honestly labeling
review state. Branch validation found 164 release publications, 14 review
publications, and no held publication in the generated public-alpha artifact.
Production-site route and review-label validation passed for the previously
deployed artifact. The current repository release inventory contains 164
release publications and 14 review publications, 178 total; the exorcism
source, installed PDF, web edition, and audit records agree on 116 physical
pages, including 103 substantive narrative pages.
The standing 27 July 2026 public-alpha authority permits future exact-current
snapshots to be installed and deployed without repeated document-by-document
authorization while preserving every concrete defect in the six alpha
concerns.

### Recently discussed paper hard review

<!-- promised-deliverable: project-recent-paper-hard-review -->

The required set is Catholic Exorcism, Last Supper, Abraham and the Daylight
Stars, John 6, and Linen Cloths. The exorcism and GPT linen work received
substantive repair, but the set has not passed one complete current-guidance
audit. Publication-local internal current-guidance audits now identify and
reconcile the exact installed, web, catalog, and release states for Last
Supper, both Abraham editions, and GPT John 6 while preserving all disclosed
evidence ceilings and without implying external approval. Exorcism and both Linen
editions remain separate exact-snapshot boundaries, and the set-level promise
remains open.

## Full repository discrepancy audit

The 2026-07-27 audit establishes the following actionable backlog:

| Audit ID | Finding | Current measure | Completion evidence |
| --- | --- | ---: | --- |
| `AUD-INTEGRATE-001` | Repair integration and Pages deployment | Integrated through `b93e64b4`; Pages run `30296605957` succeeded | passed; exact catalog-text discrepancy retained under the affected work |
| `AUD-STALE-001` | Rendered publications disagree with current inputs or records | 92 recovered baseline editions; 93 in this checkpoint because the exorcism source audit and delivery plan now correctly make that edition stale pending its later rebuild | `make check-staleness` passes |
| `AUD-SOURCES-001` | Reusable-source family screening | 140 of 140 review units screened across 229 source families; 806 reviewed owner-family presences; atomic citation coverage remains false | `make check-source-family-screening` passes |
| `AUD-REVIEW-001` | Public-alpha copies require exact-snapshot evidence or explicit concrete defects | 14 publications at the recorded checkpoint | each work-specific record resolves the six alpha concerns against its exact snapshot |
| `AUD-ART-001` | Dictionary artwork identification/resolution notices | 0 validator notices; held unsupported assets remain explicit | artwork validator passes without implying external approval |
| `AUD-MEMORY-001` | Conversation outcomes were not exhaustively represented in tracked work records | prior ledger had 8 broad items | every known agreement is represented here and in the ledger when criteria are known |

The audit findings promoted to acceptance-criterion work are tracked below.

<!-- promised-deliverable: project-integrate-and-deploy -->
<!-- promised-deliverable: project-stale-editions -->
<!-- promised-deliverable: project-source-family-screening -->
<!-- promised-deliverable: project-public-review-gates -->
<!-- promised-deliverable: project-dictionary-artwork-holds -->

The recovered baseline had 92 stale editions spanning articles, biographies,
histories, liturgy, Mariology, theology, curricula, and devotions. This
checkpoint intentionally changes two exorcism research records, so the current
working-tree audit reports 93 until that existing edition is rebuilt in its
queued source/drafting or public-artifact work. The immediately discussed
stale papers are named above; the authoritative reproducible inventory,
including the current provider split, is the output of `make
check-staleness`. Staleness is a work queue, not proof that every edition needs
the same substantive edit.

The source-family screening backlog is closed at the family level. Complete
semantic review of all 140 exact owner surfaces added 242 missing presences,
removed 13 false-positive or redundant presences, and retained 806 reviewed
owner-family relationships in total. This does not assert atomic citation
coverage, which remains explicitly false, and unsupported catalog-expansion
leads remain outside the ledger until their own family records are justified.

## Commentary discovery chain

The research algorithm maps a scripture passage to the commentary works worth
pulling into the source vault, then unions those mappings across every proper.
`commentary-work-index discover` is the repo-maintained lookup and
`build-corpus` the union. `tools/harvest` populates the index and
`src/sources/commentary/passage-commentary-index.yaml` now carries the result of
six harvest runs, so a lookup resolves to the works the harvest actually
recorded rather than to nothing.

Weighting is already implemented and needs no schema change. Each mapping
carries a `confidence` float that orders works within a passage, and
`build-corpus` accumulates a reciprocal-rank `score` across passages, so a work
recurring at good rank through many propers outranks one appearing once.

On 30 July 2026 the maintainer accepted the nondeterminism of a model-ranked
"top 20", judging the head of the list unlikely to differ materially between
runs. The concern was that a generated ranking is not a measured citation count
and that variance is largest for obscure passages, which is where the volume is
— 572 of 1301 distinct references are Psalms, many of them ferial antiphon
fragments. The accepted resolution is to define `confidence` as multi-run
agreement frequency rather than a model-asserted score, so the stability claim
is measured rather than assumed and low-agreement works self-identify for
review. Harvest results belong in a dated, tracked ledger; every downstream
tool reads that ledger, which is what keeps the chain repeatable even though
the harvest step is stochastic.

## Tool CLI consolidation backlog

The 2026-07-30 tool review left a deliberate remainder. Delivered: the layout
returned to `tools/<id>` so `tmt check` gates it; the launcher's controls became
dash-prefixed options that a registry id cannot shadow; every registered tool
gained a `tests/tools/<id>.test`; and registry drift, hardcoded paths, and
`usage` staleness are asserted in `tools/tests/test_tool_registry.py`.

The remainder changes interfaces the Makefile, guidance, and release records
depend on, so each needs its own scoped unit rather than an incidental edit:

| Item | Change | Blast radius |
| --- | --- | --- |
| Flag vocabulary | One meaning per flag: `--root` currently carries four, leaf identity has five spellings, `--provider` three shapes | ~20 tools, Makefile, guidance, source READMEs |
| Shared dispatcher | Adopt `scripts/_tooling.py`'s `run_verb_cli` beyond its four current users, giving every tool `--json` and one error contract | 17 tools |
| Verb vocabulary | Collapse 27 verbs onto a closed lifecycle set; `check`/`validate`/`verify` and `bootstrap`/`prepare`/`build-corpus` are synonyms today | 11 verb-bearing tools, Makefile, guidance |
| Id naming | Retire the `check-*` prefix into a `check` verb on the domain tool; `web-edition` and `check-web-edition` already declare the dependency | 7 registry ids, Makefile, guidance, release hash records |

Sequence the flag and dispatcher work first: neither renames an id, and both
make the verb and id changes mechanical. The id renames come last because they
move release hash records and every smoke-test filename together.

## Reconciliation history

- 2026-07-31: Twenty-two commits, none pushed. **Site shape.** The landing page
  became the library and its prose moved to `ABOUT.md`, which still opens
  "Don't Panic"; the separate Library page was retired as a second name for the
  same thing. The four reading pages were being copied into the artifact rather
  than rendered, so they alone carried no Triptych header, navigation, footer or
  robots metadata — they now render through `layout.html` like the other 131,
  and all 135 were audited. Two hand-copied duplicates of the site's section
  palette were deleted with that change. `doc/` became `pdf/`, so `src`, `pdf`
  and `web` read as the three forms of every publication.
  **Calendars.** Sixty commemorations folded into 1962 feast names became
  entries of their own, and `check-calendar-masses` now refuses the pattern;
  five absent celebrations were authored and three refused for want of a
  witness; eight masses that existed and no date could reach were dated. Both
  calendars are wholly reachable, 459 of 459 and 268 of 268.
  **Scripture.** Every publishable bible now typesets as a two-column volume
  carrying its own rights notice. 926 of 2190 propers citations were missing the
  commentary index, 888 of them because the lookup preferred "Psalm" over the
  parsed "Psalms". The Knox copyright question was settled from the primary
  record: the US registrations were renewed, R525394 and R646862, so it is
  protected until 2039 and 2043.
  **Policy.** The maintainer withdrew the research-conduct rule, the
  family-screening requirement and the six-concern alpha assessment, and
  suspended research staleness. Nothing was rebaselined and no paper was
  touched, because a cleared flag would have asserted a review that did not
  happen.
- 2026-07-31: Retired `PROJECT-HANDOFF-2026-07-30.md`. Every task in its "where
  to pick up" section had landed and its opening line, "nothing is committed,"
  had stopped being true. The two facts it held that no other artifact did — that
  no authorised bulk source exists for the NRSV or the NABRE, and what is lost by
  not having the NABRE — moved into `guidance/bibles-for-agents.md` as a recorded
  access boundary. Re-measured that document's open-work and
  fails-silently sections against the repository rather than against memory: the
  clamp in `Bible.span` is gone, `citation_divergences` covers twelve books
  rather than four, and the unresolved counts rose in every edition because a
  citation that used to be truncated into a neighbour now refuses.
  `guidance/liturgy/postconciliar-illustrated-dictionary-handoff.md` is a forward
  handoff for unstarted work and was left alone.
- 2026-07-29: Reorganized the public library into the seven approved portals:
  Faith, Scripture, Liturgy, History, Formation, Mary, and Law. Applied their
  muted white, gold, red, green, violet, rose, and black accents and distinct
  ornament pairs throughout the generated site, reserving ℣/℟ for Liturgy.
  Removed reader-facing release-state banners and document labels. Installed
  the expanded 16-page Tenth Sunday synthesis, the sparse lower-third exorcism
  title page with consolidated terminal endnote, and the exact reviewed
  no-label GPT PDF set; Claude publication sources and artifacts were not
  changed.
- 2026-07-29: Retired unavailable human, priestly, specialist,
  intended-reader, physical-use, and ecclesiastical review as placeholder
  alpha gates. Recast current completion tracking around source support, rights
  and distribution status, safety, artifact consistency, mechanical
  correctness, and every-page visual inspection. External approval is recorded
  only when it actually occurs and is never inferred from internal or AI
  review.
- 2026-07-28: Reconciled the exorcism promise ledger and work register to the
  exact bounded-completion evidence: 116 physical pages, 103 substantive
  narrative pages, and passing source, safety, rights, law/currentness,
  PDF/web anti-drift, and every-page review gates. Retained explicit future-
  research ceilings and the public-alpha non-approval boundary.
- 2026-07-28: Superseded the isolated-worker/final-maintainer-push boundary
  with the clean direct-`main` workflow. Authorized ordinary coherent commits
  and regular validated checkpoint pushes to `origin/main`, including their
  automatic Pages deployment attempts, while retaining exact outgoing-range
  review, public-disclosure checks, live-route verification, and the
  prohibition on force-pushing or rewriting published history.
- 2026-07-27: Reconstructed the altar-server, dictionary, exorcism, linen,
  discoverability, and recent-paper commitments from tracked evidence and
  current user direction. Confirmed five repair commits and the public-alpha
  binding commit are pushed but not integrated.
- 2026-07-27: Ran the repository-wide staleness, source-family, public-review,
  artwork, and integration audit. Recorded unresolved counts without promoting
  them to completion.
- 2026-07-27: Added the clean-agent post-merge restart sequence, priority
  queue, exact verification commands, exorcism re-entry point, and authority
  boundary.
- 2026-07-27: Confirmed that pull request 1 was merged, `main` contains the
  repair series through `b93e64b4`, and Pages workflow run `30296605957`
  successfully deployed that commit. Retained the exorcism landing page's
  20-versus-29-page discrepancy as open exact-production reconciliation.
- 2026-07-27: Completed the first bounded exorcism expansion tranche from
  already verified patristic bindings. The changed source builds to an
  uninstalled 32-page candidate; web regeneration, every-page review,
  installation, and all final completion gates remain open.
- 2026-07-27: Combined that tranche with bounded canon-law and safeguarding
  repairs, built and inspected all 32 pages, installed byte-identical PDF and
  web artifacts, corrected the landing-page extent, and bound the exact alpha
  snapshot. At that checkpoint the promised 100 substantive pages remained
  open; production would not change until maintainer integration and push.
- 2026-07-27: Recorded the maintainer's standing authority to publish every
  document as a conspicuously provisional public-alpha snapshot for priestly
  and qualified-reader review. This authorizes the ordinary build, install,
  exact-snapshot binding, validation, and worker-commit workflow without
  repeated alpha approvals, but supplies no human or ecclesiastical review and
  closes no substantive completion gate. Final integration into `main` and
  push are reserved to the maintainer.
- 2026-07-27: Limited all continued research to publicly reachable sources.
  Paid editions, subscriptions, credentials, and maintainer-funded acquisition
  are outside scope; inaccessible necessary witnesses remain explicit evidence
  gaps after proportionate public-source alternatives are pursued.
- 2026-07-27: Authorized project-owned AI artwork creation and revision for
  the sanctuary pictorial dictionaries and altar-server guides, subject to
  exact provenance, rights, source-control, consumer, and review records and
  without treating generated output as human factual or artistic review.
- 2026-07-27: Recorded the then-current expectation that external review would
  be deferred. The 2026-07-29 reconciliation supersedes its use as an alpha
  completion gate while retaining the non-approval boundary.
- 2026-07-27: Replaced the worker's earlier integration, push, and deployment
  authority with the maintainer's final boundary: complete and commit every
  predecessor step in the isolated worker, but leave integration into `main`
  and every push to the maintainer.
- Earlier conversation history is not itself a durable repository source.
  Any additional remembered agreement must be added here immediately and
  reconciled against the repository rather than inferred away.
