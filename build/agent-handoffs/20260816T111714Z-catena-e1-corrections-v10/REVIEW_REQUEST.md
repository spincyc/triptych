# Review request — Catena E1 V10

Questions only. Each blocker names the acceptance decision that cannot be
made without its answer and the artifact that carries the state.

## Blockers

### 1. Is the refused sentence truthful and neutral enough to accept?

The decision gated: acceptance of the refused-prefix presentation closure —
the V9 review's first required correction. The sentence is `A text
reference was supplied for this fragment, but it cannot be used as written,
so no text is shown.` It is asserted byte-exactly at the rendered row and
swept for false claims (`PRESENTATION-CLOSURE.md`, the contract;
`tools/tests/test_catena_wave_1.py`, `V10RefusedPresentationTest`, in
`changes.patch`). Does it state only what the refusal establishes, and is
it distinct enough from the absence sentence to end the state collapse the
review found?

### 2. Is the closed claim boundary the right closure?

The decision gated: acceptance of the contradictory-claim fail-closed
correction. Absence at the exported `fragmentRow` is now exactly
`{stated: false, trail: ''}`, and every other claim shape projects as
refused — including shapes like a bare `{}` that V9 resolved to no text but
classified as absence. The alternative was to refuse only the review's
named contradictory shape and leave the rest unclassified.
`PRESENTATION-CLOSURE.md` states the contract; the direct-drive evidence is
in `changes.patch` and `logs/01-focused-catena-head.log`. Is
classified-closed the right disposition for the unproducible shapes, or too
wide?

### 3. Do the four pinned vectors constitute the complete terminal proof?

The decision gated: closure of the review's `cold-prewarmed-late-proved-at-
the-sinks` requirement, which it flipped from pass to open. Each vector
pins expected values for: the whole owned request journal, row identity and
count, the rendered sentence or body with the wrong sentence proven absent,
tally, announcement journal and standing `statusText`, `aria-busy`, hash
and history journals, `history.state`, focus, error and failure sinks, and
the release at exactly zero-then-one with the 36-field guard retained
(`changes.patch`; `logs/11-request-journals-head.log`). Is any material
sink still unpinned, or pinned to a value the reviewer would not accept as
the expected one — in particular the focus values (`body` cold,
`chapter-select` after the reader's own walk)?

### 4. Does the corrected package protocol satisfy the seven findings?

The decision gated: closure of the V9 review's package/provenance findings.
The unique-log, contemporaneous-provenance, timestamp-refusal, label,
handoff-structure, review-request-structure, and P8-binding corrections are
in the shipped pipeline (`logs/battery.sh`, `logs/checks.py`,
`logs/assemble.sh`, `logs/derive-claims.py`,
`logs/verify-final-package.py`) and their products (`checks.txt`,
`logs/order-head.txt`, `logs/order-parent.txt`, and this package's own
post-seal verification transcript archived beside the ZIP on the evidence
branch). Is each of the seven answered as the
review meant it, or does any need a different mechanism?

## Optional feedback

### 5. Should the refused row carry a machine-readable marker?

The refused row is distinguished by its sentence and pinned by it; it
shares the muted `missing` style hook with absence, and no `data-state` or
class token was added, to stay inside the page's 13,000-byte ceiling
(headroom now 13 gzipped bytes). Is a machine-readable row marker worth
spending bytes on in a later lane, or is the pinned sentence sufficient?

### 6. The uncapped model payload, re-asked

The sentence and the boundary logic were placed in the model because the
page has almost no ceiling left; the model has none at all and grew again
(+562 gzipped whole, disclosed in `DERIVED-CLAIMS.md`). The standing
question from V8 and V9 — whether the model and the combined route payload
need a governed ceiling — remains the budget owner's and is re-asked, not
answered.
