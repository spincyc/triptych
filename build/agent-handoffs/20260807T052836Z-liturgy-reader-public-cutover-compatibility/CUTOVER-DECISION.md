# Liturgical Instrument public-cutover decision

## Decision status

**Architecture accepted; compatibility-closed candidate awaiting narrow
independent review; execution remains unauthorized.** Option A, source-level
in-place promotion behind the unchanged canonical filenames, is the selected
smallest architecture. Independent plan review resolved every public-contract
choice, and compatibility commit `3f3949617a04ffa68a1070058d0f7bc5ac74dc93`
implements those decisions without changing the canonical route sources.

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

The separately committed compatibility closure already makes retained
candidate HTML statically noindex, route-neutralizes visible controller copy,
preserves `why=1` and every held territorial branch, adopts stable Propers keys,
and adds Details navigation. The eventual cutover must reuse those exact bytes;
it must not duplicate or reopen them. Candidate and oracle routes remain
deployed, unlinked, and unmodified in visual composition during the initial
acceptance window.

This mechanism has the best rollback property: an ordinary revert restores the
two canonical HTML source files and any bounded route-neutral metadata changes;
no redirect cache, renamed data root, deleted legacy controller, or build-only
alias must be reconstructed.

## Exact expected later execution paths

Product route paths:

- `src/web/browser/liturgy/day.html`
- `src/web/browser/liturgy/index.html`

The later execution copies the accepted Day/Propers reader DOM and load graphs
behind those two filenames while omitting the retained-candidate robots meta.
It does not change `day-reader.html`, `propers-reader.html`, either controller,
or `reader-state.js`; those compatibility bytes are already committed and are
the execution baseline.

Cutover-owned tests and publication records:

- `tools/tests/test_day_reader_integration.py`;
- `tools/tests/test_day_missal_integration.py`;
- `tools/tests/test_propers_reader_integration.py`;
- `tools/tests/test_liturgy_reader_visual_reset.py`;
- `tools/tests/test_liturgy_reader_shell.py`;
- `tools/tests/test_mass_ordinary.py`;
- `tools/tests/test_public_alpha.py`;
- `tools/tests/day_reader_integration_browser.mjs`;
- `tools/tests/propers_reader_integration_browser.mjs`;
- `tools/tests/liturgy_reader_shell_browser.mjs`;
- `tools/tests/liturgy_reader_visual_reset_browser.mjs`;
- `release/public-alpha.json` and
  `release/rights/public-alpha-2026-07-15.md`, refreshed only for explicitly
  authorized changed bytes;
- `PROJECT-WORK.md`, `guidance/liturgy-browser-roadmap.md`, and
  `promised-deliverables.toml`, recording an execution candidate—not public
  acceptance—plus a fresh execution continuity/handoff.

Files that must not change include accepted Instrument/shell CSS, shell
controller, state adapters unless a proved URL-name conflict requires it,
assembly, renderers, Ordinary seating, liturgical/calendar/Bible data, sources,
translations, public README/library/navigation hrefs, and visual oracle files.

## Resolved public-contract dispositions

### 1. Empty Day default

Accepted: the public empty-Day default is local civil date, the
repository-declared default missal (currently Roman 1962), declared/default
Bible and language rules, and Read mode. This is an intentional public behavior
change from accidental manifest ordering and is covered by the deterministic
empty-URL browser fixture.

### 2. Existing `why=1` and territorial outcomes

Accepted and implemented: `why=1` renders production-derived, subordinate
branch apparatus after the affected unit with no route/self-link. Every held
territorial branch renders under its source identity without inferred locality,
array-order preference, or public locality key. Branch-specific unrenderable
content fails closed without suppressing another held branch. The exact
apparatus, multi-branch, reload, history, and source-honesty states are governed.

### 3. Propers cycle/alternative/witness URL names

Accepted and implemented: `cycle`, `alternative`, and `translation-witness`
are stable public names. The retained route accepts `_candidate-*` aliases only
as input during the initial window and never emits them. Direct load,
validation, serialization, reload, Back/Forward, alias conflict, and invalid
explicit values are governed without changing renderer ownership.

### 4. Direct cross-entrance/context navigation

Accepted and implemented: Details contains a first related-reader link followed
by restrained existing contextual destinations. It preserves the four primary
actions, adds no generic footer or dashboard, and is governed at desktop,
mobile, keyboard, and early-open asynchronous states.

### 5. Retained indexing and canonical wording

Accepted and implemented: retained candidates carry the complete static
noindex/nofollow/noarchive/nosnippet/noimageindex directive. Visible runtime
titles, failures, status, and mode copy are route-neutral. Canonical pages will
omit candidate robots metadata and remain indexable; retained/oracle pages do
not advertise themselves as public canonical surfaces. The future canonical
source titles are exactly `Day` and `Propers`: the public-alpha builder appends
its single ` · Triptych` site suffix, avoiding the doubled product name that
would result from copying the candidate titles verbatim. Runtime celebration
and formulary titles continue to use the already accepted route-neutral
`… — Day — Triptych` and `… — Propers — Triptych` forms.

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

The regenerated normal-context patch is
`build/agent-continuity/liturgy-reader-public-cutover-proposed.patch`, SHA-256
`cd11518ba7b20d198cbd16d08cc153d3f3053afeba8a230441c57312318a7566`
against exact execution baseline
`e62a226fc661100a2427a4193213c7dadcf24225`.
`git apply --check` passes without `--unidiff-zero`. It changes exactly two
product entry points, two release-binding records, seven focused Python tests,
three Chromium harnesses, and three tracking files. It contains no candidate,
controller, shared-state, stylesheet, data, navigation, or oracle hunk.

The proposed canonical source hashes are
`9a119a6aa87e900d6fc4c3e236191fe8a036abc305236eb576c09f823c7b7972`
for `day.html` and
`a6527316266365b79ff2ecdc193da3ab1034b1daa63408b869b192d2aeb85600`
for `index.html`; the corresponding prospective rights-record digest is
`5a4b4d4f8bfbcf8d5fd54249c0d8664be7215b4bee9e82ccc8a37f400e3cf31e`.

1. Obtain narrow independent acceptance of compatibility commit `3f3949617`,
   evidence checkpoint `998648c34`, and the regenerated mechanically
   applicable execution patch.
2. In one cutover commit, promote both canonical HTML entry points, update
   canonical-ownership assertions, refresh exact release bindings, and record
   execution-candidate tracking state. Do not touch compatibility product bytes.
3. Build and exercise actual canonical filenames locally against the accepted
   candidate/oracle matrix.
4. Push once; require successful Pages deployment for that exact commit and
   complete cache-bypassed plus post-600-second parity checks.
5. Stop for independent cutover acceptance. Do not remove candidates, oracle,
   legacy controllers, or compatibility tests.

If any post-deployment gate fails, ordinarily revert the cutover commit and
verify the rollback deployment as specified in the rollback plan. Public
navigation changes and cutover execution remain unauthorized until an
independent plan disposition and separate maintainer authorization are both
recorded.
