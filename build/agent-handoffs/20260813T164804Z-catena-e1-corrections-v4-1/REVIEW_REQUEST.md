# Review request — Catena E1 V4.1

Exact head `f93757854b54c19e50bdcb97ca0fed9b48d22bb7`, one commit above
`e40720d5d622e8b0528b8c714cc5caee0b21cee3`.

## Blockers

### 1. Is the replacement umbrella copy actually neutral, and is it enough?

The review asked for "neutral umbrella copy or a typed unsupported reason".
This lane chose **neutral umbrella copy**, keeping the existing typed detail:

    reference  Address not used
    heading    This address cannot be used as written
    status     The address is unchanged; the values not used are listed.
    detail     voice=translation:grc is not a voice this corpus holds

Judgment needed on two points:

- **"cannot be used as written"** still makes a claim about the address. Is
  that within "describes the state neutrally", or does it read as a verdict on
  the reader's input? The alternative considered and rejected was a *typed*
  heading that differs between malformed and unsupported, which would have
  ended the shared umbrella the review said was acceptable to keep.
- **"the values not used are listed"** deliberately avoids "invalid". Does it
  lose necessary information for a screen-reader user, who gets only the status
  write and must then navigate to the detail rows?

### 2. Was limiting the correction to three strings the right boundary?

The page carries other phrasing that a broad neutrality standard would likely
also fail — for example `Believed to comment here — the acquisition list`,
`which omits its confidence`, `held, not renderable yet` (a committed future),
`no <language> this project may publish` (a legal conclusion), `not yet taken`,
and `a data or connection fault` (a diagnosis the page cannot make). An
investigation lane surfaced roughly a dozen such items.

**None was touched.** The reasoning: the review's finding named the fail-closed
presentation, this is a micro-correction lane, and general wording cleanup was
explicitly out of scope — a fifteen-string diff would also have been far harder
to review than a three-string one.

If the reviewer considers the neutrality requirement to be page-wide rather than
fail-closed-specific, this lane got the boundary wrong and a follow-up is owed.
**That is a judgment about scope, and it is put here rather than assumed.**

### 3. The `src/web/data/` contradiction — unchanged and unresolved

`test_candidate_does_not_leak_fixture_or_discovery_records` forbids every
`src/web/data/` change; the V3 review authorised exactly one. Both cannot hold.
This lane wrote nothing under `src/web/data/`, did not weaken, delete, rewrite
or whitelist the test, did not back out the authorised projection, and did not
mark anything expected. The failure is identical at base and head, with the same
four forbidden paths — two from V4's authorised seam, two predating V4 entirely.

**A reviewer should decide** whether the guard needs an exemption, whether its
`BASE` should simply be re-based by its owning lane, or whether the seam should
have been carried some other way. See `DATA-TEST-CONTRADICTION.md`.

### 4. Is screenshot evidence now sufficient, given what it does not prove?

53 PNGs from real headless Chromium over a real built artifact, covering the
nine route states at three viewports plus forced-colors and print emulation,
with `before--`/`after--` pairs for the two states whose copy changed.

It does **not** prove announcement. No screen reader or AT bus ran. V4's
`AT-LIMITATION.md` still stands and is not superseded by pictures. If the review
intended "capture of the visible refusal change" to include AT verification,
that remains open and is not this lane's to close.

## Optional feedback

### 5. The record discrepancy this lane did not repair

The V3 review commit `9b1c2368` is **not an ancestor** of this branch — V4
branched from the reviewed head `f2c9bc49`, so the reviewer's own durable
records (the finding matrix, the reopened deliverable statuses, the progress
ledger row, the master-plan row) do not exist at this head. V4 wrote its own
paraphrase instead.

One visible consequence: the reviewer set
`unsupported-voice-distinguished-from-shape` and `displayed-provenance-typed`
to `open`, but at this head both read `pass`, carried over from the V3 lane.
V4's package says it "left them open anyway", which is not what the file shows.

This lane did **not** touch `promised-deliverables.toml` and did not
self-certify either criterion. Repairing the branch topology is a records
decision above a micro-correction's authority, but the reviewer should know the
ledger at this head does not reflect the review.

### 6. The new regression's shape

`TypedStateTest.test_the_shared_refusal_umbrella_stays_neutral` asserts a
**negative over a substring list** (`could not be read`, `not recognised`,
`invalid`, `does not have`, `unreadable`) rather than pinning exact strings.
That was chosen so a future rewrite cannot reintroduce a diagnosis under
different words, but it is a blunter instrument than an equality assertion and
will need extending if a new non-neutral formulation is invented. Is that the
right trade?

### 7. Lane-local tooling shipped as evidence

`logs/capture-catena.mjs`, `logs/capture-provenance.mjs` and
`logs/compare-gate.py` are lane-local, shipped inside this package rather than
added to `tools/`, following the precedent V4 set with `sanitize-and-seal.py`.
The capture scripts exist only because the shared gate's route list carries no
fail-closed Catena address, and extending the common gate is another owner's
call. Should any of these be promoted to repository tooling?
