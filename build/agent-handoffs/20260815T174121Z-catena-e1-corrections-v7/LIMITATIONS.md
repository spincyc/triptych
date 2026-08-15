# Limitations — what this package does not prove

The V6 package's limitations record named none of the seven evidence faults
its independent review then found. A limitations record that omits the
evidence's own faults is not a limitations record, so §§1–3 below are those
faults and what V7 did about them, stated before anything about the
correction.

### 1. Every claim a machine could derive is derived, and the ones that are not are named

The V6 review found the package mechanically intact and descriptively untrue:
`REVIEW_REQUEST.md` named `83cb63b61` as the exact head of a package sealed for
`4639b139f`; three members said 45 sealer tests where the shipped log says 46;
one said four commits where five exist; one said three changed files where six
exist; four said sixteen raster pairs where fifteen exist. Every one of those
numbers was available to a program and was typed by a person instead.

`logs/derive-claims.py` computes them and writes `claims.json` and
`DERIVED-CLAIMS.md` **from the same pass**, so the machine-readable record and
the readable one cannot disagree. `logs/head-consistency.py` then reads
`claims.json` back and refuses a package whose prose names a commit those
claims do not entitle it to name, calls the head a parent, or names a
package-relative path the package does not contain.

**What that does not cover.** A judgement is not a derivation. Every sentence
in this package that says a thing is *right* — that a line was drawn in the
correct place, that a sentence is the truthful one, that a limitation is
acceptable — is a claim by this lane and is not machine-checked by anything.
The checker catches a number that moved. It cannot catch an argument that is
wrong.

### 2. There are no screenshots, and that is measured rather than asserted

`src/web/browser/catena/catena.css` and `src/web/browser/catena/index.html` are byte-identical to the parent; the changed
file list is derived, not typed. This correction changes what the page *says*
in states a valid corpus cannot produce. A raster of a valid chapter would be
identical at both ends and could not bear on any claim here.

What replaces it is stronger: the V7 test file replayed against the
**parent's** production files — same scenarios, same oracles, other code — in
`logs/v7-tests-against-parent.log`. Every assertion that distinguishes the two
heads is in that log by name, and the class decomposition is derived from it
rather than described.

`logs/derive-claims.py` counts PNGs and pairs from the sealed directory anyway
and reports zero, because "no screenshots" in prose and "zero screenshots"
counted by a program are different kinds of claim, and V6's screenshot counts
are the reason to prefer the second.

**What that does not cover.** No real browser ran against this head. The
evidence is the DOM shim's, and the shim is a hand-written model of a browser:
it reflects `lang` and `id`, implements `<select>` value semantics, dispatches
`toggle` and `change`, and records `document.activeElement` — and it is not
Chromium. The browser gate did run, in real Chromium, over the built site, and
its report is here; it asserts nothing specific to this route.

### 3. The sealer's two defects are fixed, and the fix found a third

`--check-only` deleted `MANIFEST.sha256` on failure, in a mode documented as
never rewriting a member and which this package's own instructions tell a
reviewer to run. `verify()` never opened the ZIP, so the archive a reviewer
actually receives was the one artifact whose contents nothing checked. Both
are corrected, with tests; `PRIVACY-AUDIT.md` sets out both and the third
thing writing the second check immediately caught.

**What that does not cover.** The ZIP's *construction* is still not
reproducible: entry timestamps are local mtimes, so two seals of one tree give
two different archive digests. `MANIFEST.sha256` is the content proof and
survives repacking; the sidecar proves transport only.

### 4. `startFailed()` is not reached

The review asked for a pending render driven through it. It is not reachable
from a settled route in this page, for a reason that is a property of the page
rather than of the harness, set out in `UNRESOLVED-BLOCKERS.md`. What is
supplied instead is the same claim through the terminal transaction a route
can reach. That substitution is named as a substitution.

### 5. Every figure was measured at the sealed head, and only at it

V5 claimed all its measurements came from one commit and its own
promise-ledger output falsified it. This lane could have made the same claim
cheaply — the records commit touches only Markdown and TOML, so almost nothing
it reports could move — and did not, because "almost nothing" is the shape of
that defect rather than an answer to it. The promise-ledger count DOES move
with a records commit, and a package that measured it at the commit before
would be reporting a number that is not true of the head it is sealed for.

So the whole battery was re-run at the sealed head, after the records landed,
and every figure in `claims.json` and `DERIVED-CLAIMS.md` comes from that one
run. Earlier partial batteries at superseded heads were kept, separated by
head, and none of them is used as evidence here.

**What that does not cover.** It makes the figures consistent with one commit.
It does not make them reproducible on another machine — see §6.

### 6. The parent and head measurements are sequential and separate, and that is all they are

Each battery ran in its own clean checkout, one command at a time, never in
parallel and never in the background, with an ordering ledger recording the
start time, end time and exit of every command. V6 disclosed that its first
head-side round let `make -k check` and the browser gate run concurrently with
full discovery in one checkout, and discarded it; V7 never produced such a
round.

**What that does not cover.** Sequential is not hermetic. Both batteries ran
on one machine, against one Python, one node and one Chromium, and the exact
versions are recorded rather than the environment being reproduced.

### 7. No literal test-count identity is claimed

The head runs more tests than the parent. What is compared is the SET of
fully-qualified FAIL/ERROR identities, derived and diffed by
`logs/derive-claims.py` in both directions, with any entry present at only one
end named. A count identity would be a weaker claim and this does not make it.

### 8. Nothing here proves what a screen reader says

The evidence is rendering and DOM evidence: `aria-busy`, the live region's
text and its current contents, `document.activeElement`, and what was
requested. No AT bus and no real device were available. That prerequisite
remains open with its owner and nothing in this package supersedes it.

### 9. The fixture corpus is on a different, older contract

`src/web/browser/fixture/structure/catena/` predates the shared-source fold:
its fragments are flat, carry a literal `text_path`, and its index has no
`voices` and no `absences`. This correction preserves it — that is the whole
of the reason a carried `text_path` is accepted at all, under the constraint
`REVIEW_REQUEST.md` §2 asks about. Regenerating it is generator and data
ownership this lane does not hold, and it is recorded rather than done.

### 10. Two confirmed adversarial findings are not fixed

`{"source": "0"}` is counted as a fragment held here. `REVIEW_REQUEST.md` §1
sets out why closing it means moving a line the V6 review left standing, and
asks.

`src/web/data/bibles.json` arriving unreadable is reported as "lists no translations" — the
same manufactured negative, at the one seam this correction cannot reach,
because the sentence is composed in `loadBibles` in the shared shell.
`UNRESOLVED-BLOCKERS.md` §7 names the seam and the one-line fix its owner
would make.

Both are real findings, both are recorded as unfixed, and neither is
characterised as a smaller thing than it is.

**And the shape of the three passes is itself a limitation, and the most
useful thing in this document.** Every pass found real defects — nineteen in
all — and each round was mostly the same class one level under the last: the
payload, then its contents; the container, then its members; one sentinel
corrected, then three more like it; the root's failed fetch caught, then the
optional file's beneath it. `TYPED-PROJECTION.md` §6 tabulates it and states
the generalisation a successor can check directly.

A fourth pass would probably find a fourth level. This package says which
levels were examined and by what method; it does not say the bottom was
reached, and no reader should take three passes for a proof that it was. That
is the reason the process ends in an independent review rather than in a lane
declaring itself finished.

### 11. What this correction did not touch

Four stale Catena release bindings, the `src/web/data/` guard contradiction
and its two Day-reader failures, the common-gate failure population,
`check-tool-registry` and `check-examples`. Each fails identically at both
ends. None was worked around, whitelisted, weakened, expect-marked or skipped.
`UNRESOLVED-BLOCKERS.md` records each with its owner.

### 12. An earlier V7 package was sealed, pushed, and superseded

It is on the evidence branch and it is not deleted, because deleting it would
make this record unverifiable.

Its figures are the same figures — the same battery, at the same head, at the
exact commit this package is sealed for. What was wrong was the RECORD of how
they were obtained: the head battery's ordering ledger captured each command's
start, end and exit and not the command itself, so `checks.txt` composed from
it said `command : (not recorded)` ten times. The correction brief requires
"the exact command", and a package whose own thesis is that claims are derived
rather than typed cannot answer that by typing the commands in afterwards.

So the head battery was run again, at the same unchanged head, with the
command recorded as it ran, and this package is sealed from that. The cause
was mine and is worth naming precisely: the instruction template for the head
battery omitted the line that records the command, which the parent battery
had included on its own initiative — the two halves of the comparison were
gathered to two different standards and only one of them met the brief.

The other process fact worth recording: the first package was pushed before
its sealed contents had been read end to end. Sealing verified that every
claim was internally consistent, which it was; nothing verified that the
ledger it was composed from was complete.

### 13. This lane does not review its own work

Nothing here is an acceptance. Two adversarial passes over this lane's own
diff are included in the record and they found real defects — five in the
first, and whatever the second reports — which is evidence that self-review
finds things, not evidence that it finds everything. The disposition on this
head is owed by a fresh independent review, and no measurement in this package
is offered as a substitute for one.
