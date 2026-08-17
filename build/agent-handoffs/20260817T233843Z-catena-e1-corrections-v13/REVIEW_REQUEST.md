# Review request — Catena E1 V13

Questions only. Each blocker names the acceptance decision that cannot be
made without its answer, and the artifact that carries the state it is about.
Nothing here is an implementation summary and nothing here asks whether the
work looks good.

## Blockers

### 1. Is one projection per raw chapter load the contract the review meant?

**The decision gated:** acceptance of the stable-projection half of this
correction — the V12 review's finding that one raw spine and its fragments
were projected three times, so the reported descriptor counts proved no source
revisit.

The contract this lane chose, stated rather than left to be inferred:

- **one raw chapter load is one normalization**, however many consumers ask,
  and however many times the reader changes voice, steps an arrow or forces a
  re-render;
- what each consumer receives is **the same instance**, not an equal value,
  and that is checked as an instance rather than compared as an output;
- the request is owned by **the projection that produced the row carrying its
  address**, because the page composes no text address of its own.

The unit is the raw chapter object. `chapterProjection` holds its result in a
`WeakMap` keyed on the record the page received, so two fetches of one chapter
address are two raw records, two projections and two passes of the census.
This lane does **not** deliver one projection per chapter address, and does
not prevent a cache bypass from producing a second raw record.

`CLAIM-CLOSURE.md` §2 states the contract; `changes.patch` carries
`normalizeChapter`, `chapterProjection` and `chapterPasses`; the identity
tests compare recorded projection ids across every named consumer.

Is one projection per raw chapter load the required raw-object → one
projection → all request/cache/body/ownership flow, or does acceptance require
the unit to be the chapter address, or the whole render?

### 2. Is freezing every projected row acceptable, given what it removes?

**The decision gated:** acceptance of the projection's shape, and whether a
seal applied at the model boundary is a cost the route should carry.

Each projected row is frozen where it is made, together with its `extent` and
its `translators`, and the chapter projection carrying the rows is frozen
around them. The intent is that the row — the only channel across the
model/page boundary — cannot be adjusted after the projection that validated
it, by a consumer, by a later lane, or by a test.

The cost is a capability removed rather than a check added. The replay
harness's own `forceRow` hook had to change from assigning onto a row to
copying it, and that change ships in `changes.patch` rather than sitting
behind the assertion it supports. Any future harness that needs to perturb a
row must copy it too, which makes some kinds of adversarial evidence more
expensive to write than they were.

Is a frozen row the right boundary, or does it foreclose evidence a later
review will need?

### 3. Is `WeakMap` retention right when the page's own cache already retains the raw chapter?

**The decision gated:** acceptance of the projection's lifetime, which is not
a behaviour any test in this package pins.

The projection lives exactly as long as something else holds the raw chapter.
The page's chapter cache holds every loaded chapter for the life of the page,
so in practice every projection a page makes survives until the page is left.
Nothing is retained that the page was not already retaining, and nothing is
released early either.

Two things follow, and neither is measured here. A page that walks many
chapters holds a projection per chapter for as long as it holds the chapters.
And the `WeakMap` buys nothing against the page's own cache — it buys
something only against a chapter the page has let go of. This lane took no
memory figure and claims none; `LIMITATIONS.md` §3 states that plainly.

Is holding the projection against the raw record the right lifetime, or should
the projection be owned by the same thing that owns the cache, so that one
eviction releases both?

### 4. Is authority as an external sidecar, bound one way to the archive, acceptable?

**The decision gated:** closure of the V12 review's finding that marking a
package authoritative before P7 and P8 is not acceptable in this
implementation — a precondition for this package being usable as evidence at
all.

The progression is now attempt started, package sealed, P7/P8 verification,
post-P8 size and hash confirmed, then final authority established. An
in-package row may claim at most `sealed`. Final authority is a structured
record beside the package naming the attempt, the exact head, the archive's
basename, byte size and SHA-256, the P8 result and the post-P8 rehash result,
each recomputed from the archive rather than carried forward. If P8 fails, the
attempt stays non-authoritative and nothing anywhere calls it otherwise.

The structural consequence is that the binding runs **one way**. An archive
cannot contain its own digest, so the record that establishes authority cannot
be a member, and a reviewer holding only the ZIP holds a sealed candidate
rather than an authoritative package. The authority gate consumes the archive,
the sidecar, the P8 transcript, the complete external ledger and the sibling
markers, and refuses on each of the six contradictions the V12 gate accepted;
run against the V12 package it refuses it.

`PROVENANCE.md` states the phase ordering and the state machine; the sidecar
and the gate transcript are siblings, named in `HANDOFF.md` §10.

Is one-way external binding the right resolution, or must an authoritative
package be self-describing even at the cost of the ordering problem that
produced the V12 finding?

## Optional feedback

### 5. The uncapped model payload, re-asked

The projection lives in `src/web/browser/catena/catena-model.js` because the
page stands at its ceiling and the model has none. The model grew from 34,367
to 36,679 gzipped whole and 8,258 to 8,873 stripped in this lane, which is the
third consecutive lane to put a correction where the ceiling is not — while
`src/web/browser/catena/catena.css` is byte-identical at both endpoints and `src/web/browser/catena/catena.js` is smaller at
both, so the route's governed measures improve as its ungoverned one grows.

The standing question — whether the model and the combined route payload need
a governed ceiling — remains the budget owner's and is re-asked here, not
answered. Is the disclosure still a sufficient answer at this size?
