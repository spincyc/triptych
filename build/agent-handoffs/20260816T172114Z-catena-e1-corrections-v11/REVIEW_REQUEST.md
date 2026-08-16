# Review request — Catena E1 V11

Questions only. Each blocker names the acceptance decision that cannot be
made without its answer, and the artifact that carries the state it is
about. Nothing here is an implementation summary and nothing here asks
whether the work looks good.

## Blockers

### 1. Is the conservative sentence truthful and neutral enough to accept?

**The decision gated:** acceptance of the truthful-presentation half of this
correction — the V10 review's finding that one sentence was asserting two
facts most of its states had not established.

The new sentence is `No text reference is established for this fragment, so
no text is shown.` It is asserted byte-exactly at the rendered row, driven
to the visible and the request sinks, and swept for false claims.
`CLAIM-CLOSURE.md` states the three-state contract; the vectors and the
sweep are in `changes.patch`, and the rendered strings read back out of the
DOM are recorded per image in `screenshots/capture-metadata.json`.

Does it state only what an unestablished member establishes — no holdings
claim, no file-existence claim, no request-failure claim, no accusation —
and is it distinct enough from both the absence sentence and the refusal
sentence that a reader can tell the three states apart?

### 2. Is fail-closed the right disposition for a partly-inherited contract?

**The decision gated:** acceptance of the claim-boundary closure.

Where the claim's own three-member contract is partly written above it — a
valid own statement beside an inherited refusal marker — the claim fails
closed rather than being adjudicated. The alternative considered and
rejected was to ignore inherited values and adjudicate on the own half. It
was rejected because the route's own directions require that an own valid
state beside an inherited refusal marker make no request, and the cost of
the choice is real: a polluted object prototype closes every valid row on
the page rather than one contradictory row. The contract, the reasoning and
the cost are in `CLAIM-CLOSURE.md`; the fourteen-case inherited and accessor
matrix that drives it is in `changes.patch`, and its run is in the focused
Catena log named in `logs/LOG-INDEX.md`.

Is fail-closed the right disposition, or is the page-wide failure mode worse
than the contradiction it refuses?

### 3. Is the 36-field terminal vector now complete?

**The decision gated:** closure of the review's finding that the
genuinely-late vector stated expected values for 13 of 36 guarded fields.

The vector now states an expected value for all 36, at both ends of the
release, with the release pinned as the one thing permitted to move, named
by sequence and address; a coverage test fails the moment a field joins the
guard without joining the proof. `CLAIM-CLOSURE.md` describes it and
`changes.patch` carries it.

Is any material sink still unpinned, or pinned to a value a reviewer would
not accept as the expected one? The coverage test binds the vector to the
guard, not to the route — is the guard itself the right set of 36?

### 4. Does the corrected package protocol answer the review's findings?

**The decision gated:** closure of the V10 review's package, provenance and
privacy findings, which are a precondition for this package being usable as
evidence at all.

The corrections are in the shipped pipeline under `logs/` and in its
products: `HANDOFF.md` now contains all ten of the protocol's required
contents as content rather than delegating two of them, and a new inventory
tool checks that mechanically; the artifact inventory names every member and
every sibling; provenance is read per command; log identity is allocated
from an append-only attempt ledger; P8 executes no archive code, uses an
out-of-archive anchor with per-tool digests, and rehashes the archive after
every check. `PROVENANCE.md`, `PRIVACY-AUDIT.md`, `EVIDENCE-INDEX.md` and
`checks.txt` carry the results.

Is each finding answered as the review meant it, or does any of them need a
different mechanism? In particular: is a per-tool SHA-256 anchor an
acceptable substitute for a commit-pinned one, given that the pipeline is
not under version control in this workspace (`LIMITATIONS.md` §5)?

## Optional feedback

### 5. Should the unestablished and refused rows carry a machine-readable marker?

The three no-text states are distinguished for a reader by their sentences
and pinned byte-exactly by them; for a machine, by the projected claim's
`said` and refusal fields. No `data-state` token or dedicated class was
added to the rendered row, because the page has 20 gzipped bytes of
headroom. Is a machine-readable row marker worth spending bytes on in a
later lane, or is the pinned sentence plus the projected field sufficient?

### 6. The uncapped model payload, re-asked

The sentence selection and the boundary logic live in the model because the
page has almost no ceiling left; the model has none at all and grew from
29,741 to 32,406 gzipped whole in this lane. The standing question — whether
the model and the combined route payload need a governed ceiling — remains
the budget owner's and is re-asked here, not answered.
