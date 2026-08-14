# Review request — Catena E1 V6

Exact head `83cb63b61e366fac07b298fee77f63d1658086f7`, above the exact reviewed V5 head
`19982ab433dd25704ed60b1ac6ddb678bc3a98f9`. The review answered is
`fa5b2f601565508acee2b1b236b0c69138af07a3` (**CHANGES REQUIRED**), whose
evidence `fe71d03e51bc3a89f01b9262cd3a4d9077bb0cef` and package digest
`18500400ce617365ef8322e41f011f44dc5a0a88dc39fbbcb5deb1abd78b75ea` were
re-verified byte-exact before this lane started. That review is a **sibling**
of this line at the reviewed parent and is deliberately not merged into it.

`checks.txt` carries a per-check SHA column. Every number below is attributed
to the commit it was measured at, because V5's blanket claim that all
measurements came from one commit was falsified by its own promise-ledger
output.

## Blockers — decisions a reviewer should make

### 1. A record that contradicts itself is declined rather than resolved

`absenceRows` gathers the recognized findings across all same-language records
for one work. **One** distinct recognized finding is the record speaking. **Two
different ones** — say `none-published` beside `partial-public-domain` — are a
record contradicting itself, and V6 declines: the row carries no finding, enters
no class count, and is spoken as "a finding this page cannot read".

The alternative was a stated precedence. I rejected it because every precedence
I could write picks a claim about someone's property rights out of two
incompatible statements, and the harsher one is the one a precedence tends to
favour. But declining discards two records that are each individually valid.

**A reviewer should decide** whether declining is right, or whether the contract
should name a precedence — and if so, which.

### 2. Which record's prose stands for a row is a deterministic arbitrary choice

Where several records carry the chosen finding, V6 picks the one that states the
most (longest `reason` + `partial`), breaking ties lexically. That is
order-independent, which is what §7 required, and it is arbitrary: nothing in
the contract says the longest reason is the truest one.

**A reviewer should decide** whether a deterministic arbitrary rule is an
improvement on first-match, or whether duplicate same-finding records should
themselves be treated as a contradiction and declined.

### 3. A fragment counts where a lead or a blocked row does not

`mixed-collection` tallies `3 fragments held · 2 works held, not renderable yet ·
2 lead entries`. The asymmetry is deliberate: the third fragment states its
author, work, date and extent and only its **id** is unreadable, so it renders a
row and is a fragment held here minus one fact. The rejected lead and blocked
records state nothing at all.

V5 argued the opposite — "a malformed RECORD is still a record the spine wrote,
so it counts and renders nothing of itself" — and the review rejected that
argument. V6 draws the line at *can this record render anything of itself*.

**A reviewer should decide** whether that is the right line, or whether a
fragment with no usable identity should also fall out of the count.

### 4. A refusal now requires a stated reason

`refusalNote` accepts a refusal member only if it carries a sound `note`. Every
one of the 112 tracked refusal rows does, and `kind` is `displaced` on all of
them, so nothing real is refused by the narrowing. But it IS a narrowing: a
record carrying a recognized `kind` and no note refuses nothing now, where V5
would have printed "Boundary not established." over it.

**A reviewer should decide** whether the note is the right thing to require, or
whether `kind` alone should establish the refusal with the note as refinement.

### 5. Padded verse keys are rejected, not normalized

§9 of the brief allowed either. V6 rejects: only `^[1-9][0-9]*$` numbers a
verse, so `"01"` renders nothing rather than folding onto `"1"`. Folding would
silently merge two records that disagree about which is verse 1 — the same
failure mode the passage commentary index is already recorded as having.

**A reviewer should decide** whether rejection is right for an edition that
consistently pads, which would render as an empty chapter rather than a
mis-numbered one.

### 6. Two identity grammars, because the corpus writes two

`ident` is lowercase alphanumeric joined by `.` or `-`, and gates fragment ids,
work ids, edition ids and canon paths. `bookToken` additionally admits upper
case, because the canon writes `Gen`, `1Kings`, `Philem` and the published hash
grammar carries them verbatim. Both are closed; both admit every tracked value
unchanged.

**A reviewer should decide** whether two grammars at one seam is a faithful
record of two real conventions or an inconsistency that belongs in the
generator.

## A defect the review did not name

Judged against an empty canon, the page answered **"book=Gen is not a book of
this canon"** — a claim about the canon, drawn from a parse failure, presented
to the reader as a fault in their own address. It appeared only while writing
§12's required regression, because a null index reached `hashProblems` before it
reached the render funnel. V6 ends the bootstrap before the address is judged.

**A reviewer should decide** whether correcting an unnamed defect found this way
is inside a bounded correction, or whether it should have been reported for a
successor. The same question was asked of V5's three and was not answered.

## Optional feedback

### 7. Prose in the model, again

V5's review request asked whether visible prose belongs in `src/web/browser/catena/catena-model.js`
beside the chapter-membership rule, and the review did not answer. V6 moved
**more** there: `languageChip` and the `Partly public domain — …` offer. The
reason is unchanged and arithmetic — `src/web/browser/catena/catena.js` finished this correction with
seven gzipped bytes of margin — but the question is now larger, so it is asked
again rather than treated as settled by silence.

### 7b. The model grew 4,593 gzipped bytes, and 3,504 of them are prose

`src/web/browser/catena/catena-model.js` goes from 11,171 to 15,764 gzipped
bytes whole, and the combined page-plus-model payload from 23,449 to 28,025 —
**+4,576**. Stripped of comments the model grows only 1,089 bytes, so roughly
three quarters of the growth is explanation.

The file carries no ceiling by design and this lane did not raise one, so
formal compliance is real. It is also **not the same statement as unchanged
practical load**, and the V5 review said so about a smaller relocation. The
prose is deliberate — this repository's model files argue for their own
predicates, and a boundary that cannot say why it refuses a value is a boundary
the next lane will quietly widen — but four and a half kilobytes is a real
number a reader downloads.

**A reviewer should decide** whether the explanatory density in the unbudgeted
model is correct, whether some of it belongs in `guidance/` instead, or whether
the model should carry a ceiling of its own so this question stops recurring
one correction at a time.

### 8. Lane-local tooling, a third time

`logs/sanitize-and-seal.py` (V4), the V4.1 capture tool (V4.1), `logs/probe-catena.mjs`
(V5) and now `logs/test-sanitize-and-seal.py` and `logs/pair-audit.py` all ship inside
handoff packages rather than in `tools/`, because `tools/` requires registry
entries and `check-tool-registry` is separately owned and separately red.
`logs/pair-audit.py` has the strongest claim yet to promotion: it is the instrument
that would have caught V5's five byte-identical pairs, and it is useful to any
package, not to this one.

### 9. The `released` counter

The harness now counts parked requests actually let go, so "nothing stale
survived" is a measurement rather than an argument. It exists because a late
completion that changes nothing is otherwise indistinguishable from one that
never happened — which is precisely how V5's "nothing stale" case passed while
releasing its payload before navigating. If that reasoning is sound it probably
belongs in other route harnesses too.
