# Limitations of this package

Each heading is a full sentence, so a reader who scans only the headings
still reads the limitation. Nothing here is a defect found by review; these
are the boundaries of what this lane did, stated by the lane that did it.

## 1. The projection is made per raw chapter object, so two fetches of one chapter are two projections.

`chapterProjection` holds its result against the raw record in a `WeakMap`,
which keys on the object the page received and not on the address it came
from. One raw chapter load is one normalization however many consumers ask,
and that is the claim `chapterPasses()` makes and the identity test pins. It
is **not** the claim that one chapter address is normalized once for the life
of the page: a second fetch of the same address yields a second raw record
and therefore a second projection, and the census counts two.

That is the honest answer for this page, whose own cache holds one record per
address and hands the same record back on a voice change, an arrow step or a
re-render. It would stop being the honest answer if the cache were bypassed,
and no part of this correction prevents that.

## 2. Freezing a projected row changes what a holder of a row may do with it.

A row is now frozen where it is made, together with its `extent` and its
`translators`, and the chapter projection that carries the rows is frozen
too. That is a deliberate seal on the only channel across the model/page
boundary, and it is also a capability removed: a row cannot be adjusted in
place by a later lane, by a consumer, or by a test. The replay harness's own
`forceRow` hook had to change from assigning onto a row to copying it, and
that change is in `changes.patch` rather than hidden behind the assertion it
supports. A future harness that needs to perturb a row must copy it as well.

## 3. The `WeakMap` ties a projection's lifetime to the page's own cache.

A projection lives exactly as long as something else holds the raw chapter,
and the page's chapter cache holds every loaded chapter for the life of the
page. So nothing is retained here that the page was not already retaining —
and nothing is released early either. A page that loaded many chapters holds
a projection for each of them for as long as it holds the chapters. That is
stated rather than measured; this lane took no memory figure, and none is
claimed.

## 4. The bounded chapter projection is not the full sole-source semantic projection.

It was deliberately not broadened into all Catena semantics. What is
normalized is one chapter's request-critical state — the members that decide
whether a request happens, where it goes, who owns the answer, whether the
chapter is readable, which voices are offered, which works an absence is
stated about, and what refusal was recorded. The wide fragment and edition
contracts are still validated field by field; orphan raw sources still
manufacture offers and rows; the CLI and browser surfaces still implement the
same semantics twice. Those are recorded open in `UNRESOLVED-BLOCKERS.md`,
and projection is not yet the sole semantic source for this route.

## 5. A polluted `Object.prototype` still closes every row on the page, not one.

This is the V12 contamination policy, which the V12 review accepted as a
design and this lane did not reopen. Its cost is unchanged with it: with any
of the five request-critical names reachable on `Object.prototype`, every
fragment of every chapter resolves to the conservative
malformed/unestablished state, which is a wider blast radius than the failure
it refuses. The reasoning is in `CLAIM-CLOSURE.md` §4. Nothing in this lane
narrows it and nothing in this lane widens it.

## 6. Final authority is a sidecar outside the archive, and the archive cannot contain it.

The V12 review refused a terminal `authoritative` row written before P7 and
P8, because a later archive or verification failure left the sealed bytes
still claiming authority. The progression here is attempt started, package
sealed, P7/P8 verification, post-P8 size and hash confirmed, then final
authority established — so an in-package row may claim at most `sealed`, and
the record that establishes authority names the attempt, the exact head, the
archive's basename, byte size and SHA-256, the P8 result and the post-P8
rehash, each recomputed from the archive rather than carried forward.

The limitation is structural and it is not removable: an archive cannot
contain its own digest, so the binding runs one way and the authority record
lives beside the package rather than inside it. A reviewer who has only the
ZIP has the sealed candidate, not the authority. `REVIEW_REQUEST.md` asks
whether one-way external binding is acceptable.

## 7. The model is unbudgeted, and it grew again.

`src/web/browser/catena/catena-model.js` has no governing ceiling. It grew
from 34,367 to 36,679 gzipped whole and from 8,258 to 8,873 stripped in this
lane, and this is the third consecutive lane to put a correction where the
ceiling is not. `src/web/browser/catena/catena.css` is byte-identical at both endpoints and
`src/web/browser/catena/catena.js` is smaller at both, so the route's governed measures improve
while its ungoverned one grows. That is disclosed, not governed, and the
question of whether the model and the combined route payload need a ceiling
remains the budget owner's and is re-asked rather than answered.

## 8. Nothing here shows an adversarial state rendered by a browser engine.

The six walking scenarios are asserted in a Node replay of the page, against a
stub DOM and a stub network. That is where the rendered sentence, the request,
the cache disposition and the ownership row are read, and it is not a browser.

The real-browser gate does run headless Chromium, but it runs over the built
public artifact, whose corpus is entirely present-valid: a record that answers
a second read differently is a property of a JavaScript object and not of a
JSON document, so the tracked corpus cannot carry one and the gate covers the
route rather than these states. No file under `src/web/data/` was read,
written or altered to produce any evidence here, and no capture of an
adversarial state ships — `HANDOFF.md` §10 states that omission and its
reason. What stands in its place is a DOM-level assertion per scenario beside
a journalled request per scenario, which record what rendered and what was
asked for rather than a raster of it.

## 9. Headless Chromium is not a device and is not an assistive technology.

The browser gate runs headless Chromium. No real-device and no
assistive-technology evidence exists for this route. That gap is separately
owned, is unchanged by this lane, and remains open whether or not any capture
ships.

## 10. The batteries measure two endpoints, and the failure sets are compared rather than the exit codes.

`make -k check`, full discovery, the browser gate and the release-bindings
check are red at this head and were red at the parent, for reasons no part of
this correction causes. Every one of them is measured at **both** endpoints in
this package and compared as a failure set, because an exit code alone cannot
distinguish an inherited failure from a caused one. Where a figure is quoted,
the log it came from is named. A battery refuses to start on a tree that is
not clean, and records tree state per command rather than inheriting a
preflight's verdict.

## 11. The assembly pipeline is not under version control in this workspace.

The tools shipped under `logs/` run from a trusted directory outside both
checkouts, so no commit pins them. What is recorded instead is the SHA-256 of
the exact bytes of every tool invocation immediately **before** it runs, and
P8 compares executed against trusted against shipped and fails hard on
divergence. That closes the V12 review's finding that present equality with a
mutable anchor does not prove which historical bytes ran; it does not make
the pipeline versioned, and this limitation is inherited from the previous
lanes and unchanged by this one.

## 12. This lane did not review itself.

No disposition is recorded here, no separately owned prerequisite is marked
complete, and nothing in this package is an acceptance. The sole next action
is a fresh independent review of the exact head this package names.
