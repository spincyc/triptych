# The claim closure — contract, mechanism, evidence

This document replaces the V10 package's presentation-closure record. The
V10 lane closed the exported claim boundary's SHAPES; the independent review
proved it had not closed its MEMBERS, and that one sentence was asserting
two facts most of the states it was given had not established. This is the
account of what V11 did about both, and of what it deliberately did not do.

## 1. What the review found, in its own terms

`bag()` established that a record had arrived. Ordinary property lookup then
answered from wherever it found an answer. Three consequences followed, and
the review demonstrated each:

- `Object.create({stated: false, trail: ''})` presented itself as this
  route's own absence and opened the carried fallback door with
  `text_refused: false` — an absence the page never derived.
- An inherited `{stated: true, trail: 'structure/catena/text/deeper/'}`
  composed a usable text address, again never derived by this page.
- Mixed own-and-inherited forms did the same, and an accessor on the claim
  could run — and could throw — merely because the boundary read it.

The committed matrix that was supposed to prove the boundary closed was
eight plain object literals. It probed no inherited claim, no hybrid claim
and no accessor-backed claim at all.

Separately, the refused sentence `A text reference was supplied for this
fragment, but it cannot be used as written, so no text is shown.` asserts
two facts of its own: that a reference was supplied, and that it was written
unusably. V10 gave that sentence to every state that resolved no text — a
`text_prefix` that was `null`, a record, a list, a number, a flag, `''` or
whitespace, and every bare, contradictory, inherited or accessor-backed
direct claim. None of those states establishes either fact.

## 2. The contract now

Three no-text terminal states, three claims, because they are three
different facts:

    ABSENT           No text reference was supplied. The row says:
                     "This fragment carries no text file, so nothing of it
                     can be shown."

    UNESTABLISHED    New at V11. A member is present but is not a written
                     textual value, or the claim's own contract is not
                     wholly its own. The row says: "No text reference is
                     established for this fragment, so no text is shown."
                     It makes no holdings claim, no file-existence claim,
                     no request-failure claim and no accusation; it does
                     not say a reference was supplied, and it does not say
                     how anything was written.

    REFUSED          A non-empty textual reference was supplied and was
                     declined before use — a real `structure/paragraphs/`
                     prefix, or the right namespace wrapped in whitespace.
                     The row keeps the stronger sentence, because for these
                     two states it is true.

    PRESENT-VALID    Unchanged: the composed request is made, the body
                     renders, and none of the three sentences appears
                     anywhere on the row.

The projected claim now carries `said` — whether a non-empty textual value
was supplied at all — beside `stated` and `trail`, and the model chooses
between the two no-text sentences. The choice lives in the model rather
than the page because `src/web/browser/catena/catena.js` stood at 13
gzipped bytes of ceiling and the model file has no budget; the page's whole
diff for this correction is one line.

## 3. The mechanism — own data, read once, never invoked

Every semantic member of the claim is read once, as an own DATA property,
through `Object.getOwnPropertyDescriptor`:

- Nothing inherited is seen. A value written on a prototype is not this
  route's own statement and is not treated as one.
- An own ACCESSOR is never invoked. A getter with a side effect does not
  run, and a getter that would answer differently on a second read has no
  second read with which to disagree. The proof asserts the planted
  accessors were invoked **zero** times, which is a stronger statement than
  reading them once and trusting the answer.
- Where the claim's own three-member contract — `stated`, `said`, `trail` —
  is partly written above it (a valid own statement beside an inherited
  refusal marker, for instance), the claim **fails closed** rather than
  being adjudicated. Deciding which half of a contradiction to believe is
  not this page's to do.

The same own-data reading is applied to the spine's own `text_prefix`, the
carried `text_path`, the fragment's `id` and `source`, the edition join, and
the extent members.

**Why fail-closed rather than ignoring the inherited half.** This was a real
design choice and it has a real cost. The route's own directions require
that an own valid state beside an inherited refusal marker make no request;
simply ignoring inherited values would satisfy that rule for this shape, but
it would also mean a page whose object prototype had been polluted with a
refusal marker resolves nothing at all, closing every valid row on the page
rather than the one contradictory row. Fail-closed makes that failure mode
loud and uniform instead of silent and selective. `REVIEW_REQUEST.md`
asks whether that trade is the right one; this document states it rather
than assuming it was obvious.

## 4. The boundary this correction does NOT reach

The own-data closure is applied to the CLAIM's small fixed contract and to
the members that compose a request. The wide fragment and edition contracts
remain **field-validated**, field by field, and are not prototype-hardened.
That is a deliberate boundary of this correction, not a completed hardening,
and it is stated again in `LIMITATIONS.md` rather than glossed.

## 5. The proof, where it was thin

- **A fourteen-case inherited and accessor matrix** drives the exported
  boundary and pins that no such claim creates a request, reopens the
  carried door, composes a text path, changes the refusal or absence state,
  renders body text, or alters ownership — and that the planted accessors
  ran zero times. The ordinary absent, valid and refused dispositions are
  asserted beside it as positive controls, and the projection is asserted to
  carry only own data properties.
- **Every unestablished prefix is driven to the visible AND the request
  sink**, against the same planted carried body the earlier lanes use. The
  V10 neutrality test blacklisted nine phrases inside the exported constant
  and drove no state anywhere; this one drives the states.
- **The genuinely-late terminal vector states an expected value for all 36
  guarded fields**, at both ends of the release, rather than 13 of them, and
  a coverage test fails the moment a field joins the guard without joining
  the proof. The release is pinned as the one thing permitted to move, named
  by sequence and address.
- **A `forceRow` harness hook** pins the renderer's before-the-sink
  ordering, using the normalized `{text_refused: true, text_path: <usable>}`
  row the model never emits, against a control that really does fetch. The
  review's point was that moving the check below `fragmentText()` changed no
  journal and left every wave-1 method green; this hook is what makes that
  ordering falsifiable.

Throughout, a pinned expected value is a **vector**: a value written down in
advance and asserted, never a second snapshot compared against a first.

## 6. The packaged journal now reproduces ownership

The live harness recorded request ownership and the dump threw it away: a
fourteen-name whitelist kept the flat path list and dropped `requests`,
`fragmentIds`, `historyState` and `replacedStates`. The journal row now
carries the five facts a reader needs without rerunning the harness —
sequence, address, the kind of record that address holds, the phase that
owned the request, and what became of it: completed, held while parked,
released once let go, or failed. It is printed as a human-readable table
beside the JSON, and a name the harness stops emitting is now a hard failure
instead of a silent `null`.

## 7. Real corpus, kept apart from the adversarial half

Every tracked spine in the production corpus emits exactly one prefix and is
PRESENT-VALID, so no real row can show any of the three no-text sentences
unless its text genuinely cannot be resolved. Every refused, unestablished
or absent prefix in this package is an **adversarial test input, not a
corpus claim**. The adversarial screenshot fixtures render the literal
string `ADVERSARIAL TEST FIXTURE — NOT REAL CORPUS DATA` in their own bytes,
so each such image is self-identifying, and `src/web/data/` was neither read
nor written in either checkout for any of it.

## 8. What the correction measured

Focused Catena is 534 green, up from V10's 522. `scripts/_catena.py check`
passes at 1,351 fragments / 1 book / 73 canon entries. Budgets are
unraised: `src/web/browser/catena/catena.css` is byte-identical to the
parent at 7,629/8,000 whole and 2,676/2,700 stripped, and
`src/web/browser/catena/catena.js` is 12,980/13,000 whole and 7,554/8,800
stripped — smaller than V10's 12,987, so the page's whole-file headroom
improves from 13 gzipped bytes to 20. The
unbudgeted model grows from 29,741 to 32,406 gzipped whole and from 7,664 to
7,973 stripped; that growth is disclosed here and in `DERIVED-CLAIMS.md`
rather than presented as unchanged load, and whether the model and the
combined route payload need a governed ceiling remains the budget owner's
question, re-asked in `REVIEW_REQUEST.md`.

`checks.txt` carries every command with its exact invocation and numeric
exit; `claims.json` and `DERIVED-CLAIMS.md` are the authority for every
figure wherever this prose and the derivation could disagree.
