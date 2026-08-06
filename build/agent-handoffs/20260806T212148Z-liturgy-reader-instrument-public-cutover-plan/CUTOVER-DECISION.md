# Liturgical Instrument public-cutover decision

## Decision status

**Planning candidate; execution remains unauthorized.** Select Option A,
source-level in-place promotion behind the unchanged canonical filenames, as
the smallest architecture. The mechanism is fixed; four compatibility
dispositions below remain independent-review blockers before its proposed patch
can be authorized for execution.

## Selected mechanism — canonical filenames load the accepted implementation

The later cutover replaces only the DOM/load graph at:

- `src/web/browser/liturgy/day.html`
- `src/web/browser/liturgy/index.html`

with the accepted reader structure already exercised at `day-reader.html` and
`propers-reader.html`. Canonical paths remain `/liturgy/day.html` and
`/liturgy/index.html`; query and hash text is not redirected or rewritten by a
forwarder. Day continues to load legacy `day.js` solely for its production
Ordinary renderer export; its existing DOM guard prevents a second controller.
All accepted state, adapter, seating, renderer, shell, and Instrument assets are
reused by filename.

The same cutover commit must make the retained candidate HTML pages statically
noindex and route-neutralize public titles/diagnostics in the shared candidate
controllers. Candidate and oracle routes remain deployed, unlinked, and
unmodified in visual composition during the initial acceptance window.

This mechanism has the best rollback property: an ordinary revert restores the
two canonical HTML source files and any bounded route-neutral metadata changes;
no redirect cache, renamed data root, deleted legacy controller, or build-only
alias must be reconstructed.

## Exact expected later execution paths

Product route/runtime paths:

- `src/web/browser/liturgy/day.html`
- `src/web/browser/liturgy/index.html`
- `src/web/browser/liturgy/day-reader.html` (static noindex only)
- `src/web/browser/liturgy/propers-reader.html` (static noindex only)
- `src/web/browser/liturgy/day-reader.js` (route-neutral title/diagnostics and
  resolved deferred-state disposition)
- `src/web/browser/liturgy/propers-reader.js` (route-neutral title/diagnostics
  and resolved public option-key disposition)
- `src/web/browser/liturgy/reader-state.js` only if independent review accepts
  stable public cycle/alternative/witness key names

Cutover-owned tests and publication records:

- focused Day/Propers/state/visual/static Python tests;
- Day, Propers, shared-shell, and governed visual Chromium harnesses adapted to
  assert canonical ownership while retaining candidate/oracle parity;
- `release/public-alpha.json` and
  `release/rights/public-alpha-2026-07-15.md`, refreshed only for explicitly
  authorized changed bytes;
- the three tracking owners and a fresh cutover-execution continuity/handoff.

Files that must not change include accepted Instrument/shell CSS, shell
controller, state adapters unless a proved URL-name conflict requires it,
assembly, renderers, Ordinary seating, liturgical/calendar/Bible data, sources,
translations, public README/library/navigation hrefs, and visual oracle files.

## Required dispositions before execution authorization

### 1. Empty Day default

Current canonical Day chooses the first rubrics calendar, currently
postconciliar. The accepted reader chooses the repository-declared Propers
default, currently Roman 1962. Recommendation: accept Roman 1962 as the
intentional reader default because it is the accepted candidate’s tested
repository default and avoids preserving accidental manifest ordering. This
is reader-visible and requires independent approval; it is not silently folded
into “parity.”

### 2. Existing `why=1` and territorial fallback

The accepted Day reader currently defers these states and links to `day.html`.
After promotion that link is recursive. Recommendation: do **not** ship a
self-link, redirect, or hidden automatic fallback. Before cutover, either:

- authorize a bounded compatibility integration that presents the existing
  production reasoning/territorial result inside the accepted shell without
  changing its source owner; or
- expressly accept a narrower public state and remove the recursive link while
  retaining a fail-closed explanation.

The first is preferred for preserving valid public behavior, but it is a new
bounded implementation unit and requires its own evidence. Until one choice is
accepted, public cutover is blocked.

### 3. Propers cycle/alternative/witness URL names

`_candidate-*` keys cannot become a public API by accident. Recommendation:
approve stable additive public names `cycle`, `alternative`, and
`translation-witness`, keep unknown keys inert, accept old `_candidate-*` only
on retained candidate routes during the review window, and add exact state
round-trip/browser fixtures. This is the smallest honest public contract; it
does not change renderer ownership. Until reviewed, affected states are a
cutover blocker.

### 4. Direct cross-entrance/context navigation

Current reader footers link Day↔Propers and to contextual sections. Instrument
hides the generated site header/footer and offers Triptych Home only.
Recommendation: add one quiet route-neutral Day/Propers counterpart link and
place the longer contextual destinations in Details, using existing local
URLs. This preserves product entrance reachability without restoring generic
site chrome or reopening composition. Because it changes accepted surface
content, independent review must approve its exact location. Until then the
plan classifies two-step Home navigation as insufficient parity.

## Rejected options

### Option B — redirect/forward canonical pages

Rejected. GitHub Pages has no native rewrite layer here. Client redirects add
flash, hash/query/history risk, duplicate indexing, accessibility ambiguity,
and a rollback surface while exposing internal filenames.

### Option C — rename candidates and preserve aliases

Rejected. Renames add deletion/alias work, disturb release bindings, make
rollback multi-path, and risk relative-path/cache divergence while gaining
nothing over same-directory in-place promotion.

### Option D — build-time alias or controller replacement

Rejected. A build-only copy would make source routes disagree with deployed
routes. Renaming `day-reader.js` over `day.js` is destructive because the
accepted Day still imports the legacy renderer export. A new router/loader is
larger than two static entry-point changes.

## Smallest reversible execution sequence

1. Resolve and record all four dispositions above; update this plan if the
   reviewer selects a different bounded answer.
2. Commit any separately reviewed state-compatibility implementation and its
   green focused evidence without changing canonical HTML.
3. In one cutover commit, promote both canonical HTML entry points, add static
   noindex to retained candidates, route-neutralize labels, update cutover
   assertions, and refresh only exact authorized release bindings.
4. Build and exercise actual canonical filenames locally against the accepted
   candidate/oracle matrix.
5. Push once; require successful Pages deployment for that exact commit and
   complete cache-bypassed plus post-600-second parity checks.
6. Stop for independent cutover acceptance. Do not remove candidates, oracle,
   legacy controllers, or compatibility tests.

If any post-deployment gate fails, ordinarily revert the cutover commit and
verify the rollback deployment as specified in the rollback plan. Public
navigation changes and cutover execution remain unauthorized until an
independent plan disposition and separate maintainer authorization are both
recorded.
