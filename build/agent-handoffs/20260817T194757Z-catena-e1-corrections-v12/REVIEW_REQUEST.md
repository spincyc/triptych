# Review request — Catena E1 V12

Questions only. Each blocker names the acceptance decision that cannot be
made without its answer, and the artifact that carries the state it is
about. Nothing here is an implementation summary and nothing here asks
whether the work looks good.

## Blockers

### 1. Is the read-once contract the right contract, and is it stated strongly enough?

**The decision gated:** acceptance of the stable request-snapshot half of
this correction — the V11 review's finding that the carried `text_path`
descriptor was read twice, so the address that passed validation and the
address handed to `fetch` could be two different strings.

The contract this lane chose, stated rather than left to be inferred:

- a request-critical field answered by an **accessor** is declined without
  being called, so the invocation count is **zero**, not one;
- a request-critical field answered by a **data descriptor** is read
  **exactly once per projection**, and that one captured value is what
  validation, projection, the request decision, the ownership journal and
  the renderer state all use.

The directions permitted either zero reads or exactly one. This lane takes
both halves — zero accessor invocations *and* one descriptor read — because
V11 had already proved ordinary accessors need never be invoked and losing
that would be a regression. `CLAIM-CLOSURE.md` states the contract;
`changes.patch` carries `requestSnapshot` and the six-descriptor matrix that
drives it.

Is that the contract the review meant, and is one descriptor read per
projection sufficient — or does the acceptance criterion require that a
whole page render ask a request-critical descriptor exactly once, which this
lane does **not** deliver? See blocker 5, which is the same question from
the other side.

### 2. Is page-wide fail-closed the right cost for prototype contamination?

**The decision gated:** acceptance of the contamination disposition.

V11 asked `Object.prototype` about the claim's three members. V12 asks about
five names — `text_prefix`, the carried `text_path`, `text_refused`,
`stated`, `trail` — and asks it of the spine record and of every fragment
record, not only of the claim. The consequence is deliberate and is the cost
of the choice: with `Object.prototype.text_refused = true` set by anything
at all, **every row on the page** resolves to the conservative
malformed/unestablished state, rather than one contradictory row doing so.
That is a wider blast radius than V11's, and it is wider than the failure it
refuses.

The alternative considered and rejected was to contaminate only the record
that actually carries the polluted read. It was rejected because a
prototype is not a property of one record: a page that renders one row from
a polluted realm and refuses another is a page deciding, per row, which half
of a contradiction to believe.

`CLAIM-CLOSURE.md` states the reasoning and the cost. Is fail-closed still
right at this width, or is a realm-wide refusal worse than the request it
prevents?

### 3. Are the three corrected expected values right?

**The decision gated:** closure of the review's first finding, and
confidence that this lane did not simply move a pin to make a test pass.

Three committed assertions required an answer this lane now calls wrong, and
all three are corrected in `changes.patch` with their reasons written beside
them:

- the spine's inherited valid `text_prefix` was pinned **equal to genuine
  absence** — the review named this assertion directly;
- an inherited carried `text_path` and an accessor-backed carried
  `text_path` were pinned as ordinary no-text rows (`refused: false`,
  `unestablished: false`);
- an inherited `id` was pinned the same way.

Each now reaches the same conservative state as every other contaminated
claim. Every change makes a closure stricter rather than looser, and no
other expected value in the file moved.

Is each of the three new values the one the review intended? In particular:
should an inherited or accessor-backed carried path be **unestablished**, or
should it remain an ordinary absence row on the ground that the fragment
genuinely states no usable address of its own?

### 4. Does the authority ledger answer the finding, given when it can be written?

**The decision gated:** closure of the V11 package's authority-coherence
failure, which is a precondition for this package being usable as evidence
at all.

The V11 ledger called the superseded attempt authoritative and the shipped
attempt unresolved. The root cause was a vocabulary collision: a completed
validation battery and a sealing package attempt were both written
`authoritative`, so the count could never be one. V12 separates the two
vocabularies, reserves `authoritative` for a package attempt, permits
exactly one, and gates publication on a coherence check.

One judgement in that design needs a reviewer. The attempt's terminal
`authoritative` row must be written **before** the manifest, because nothing
may write inside the package directory after P6 — so at the instant it is
written, P7 (archive) and P8 (verification) have not run. The row therefore
claims that the package **directory** is sealed, which is true at that
instant; the ZIP identity and the P8 verdict live in the sidecar and the
outer invocation log, and the coherence check binds all three together. The
backstop is that a P7 or P8 failure writes a discard marker into the
directory, and the coherence check refuses any package carrying one.

`PROVENANCE.md` states the state machine and the phase ordering;
`logs/attempts.json` carries the ledger; the coherence transcript is in
`logs/`. Run against the V11 package unaided, the check reproduces the
review's own finding — three authoritative attempts, and the shipped one
unresolved.

Is a terminal row written at P6 with a P7/P8 discard-marker backstop
acceptable, or must the terminal word wait until after verification even at
the cost of living outside the sealed bytes?

## Optional feedback

### 5. The page projects one spine three times per render

Measured, not inferred: opening a chapter asks each fragment's
request-critical descriptor three times, because `chapterFile` projects the
spine through `spineUnreadable`, the tally projects it again, and
`renderChain` projects it a third time. The read-once contract is a claim
about one projection, and this lane pins it exactly there and pins the
page-level count at three so that a change to the projection count fails
loudly.

Three projections of one document is not a defect this lane found and not
one the review named, but it is the reason the page-level answer to "how
many times was this descriptor asked?" is not one. Is collapsing it to a
single projection per render worth a later lane?

### 6. The uncapped model payload, re-asked

The snapshot lives in `src/web/browser/catena/catena-model.js` because `src/web/browser/catena/catena.js` stands at 20
gzipped bytes of ceiling and the model has none. The model grew from 32,406
to 34,367 gzipped whole and 7,973 to 8,258 stripped in this lane. The
standing question — whether the model and the combined route payload need a
governed ceiling — remains the budget owner's and is re-asked here, not
answered.
