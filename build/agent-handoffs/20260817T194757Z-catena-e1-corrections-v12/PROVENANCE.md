# Provenance

What ran, where it ran, in what order, and which record wins where two could
disagree.

**The authority is `logs/attempts.json`.** Where this file and that ledger
could be read as disagreeing, the ledger is right and this file is a defect.
That sentence exists because the previous package's prose and its ledger did
disagree about exactly the thing the ledger exists to settle, and the review
found it.

No figure here is typed. `checks.txt` carries each command with its exit
code, its start and end, its tree state before and after, its attempt, and
its log; `claims.json` carries the identity arithmetic; `DERIVED-CLAIMS.md`
renders both.

## 1. Two vocabularies, because there are two facts

The V11 ledger marked **three** attempts `authoritative`: the head battery,
the parent battery, and a package attempt that had already been superseded —
while the attempt that actually shipped carried the status string
`unresolved: the ledger carries no terminal row for this attempt`. A reader
could not count to one, and only prose repaired it.

The cause was one word doing two jobs. "This validation battery ran to
completion" and "this is the package to review" are different facts, and
writing both `authoritative` makes the authoritative count uncountable by
construction. So:

**A validation battery** (`side: head`, `side: parent`):

    started ──▶ complete
            └─▶ failed

**A package attempt** (`side: package`):

    started ──▶ sealing ──▶ authoritative ──▶ superseded
                        └─▶ discarded

`authoritative` is reserved for a package attempt. **At most one package
attempt in a lane may hold it, and this package's ledger must contain
exactly one.** A battery that is written `authoritative` is a refusal, not a
row.

No attempt may be authoritative and superseded, unresolved and final, or
discarded and authoritative. Each is a distinct refusal in the coherence
gate, and each has a test that proves the refusal fires.

## 2. When the terminal row can honestly be written

Nothing may write inside the package directory after the manifest is taken.
The sealing attempt's terminal row is therefore written immediately before
the manifest — after the freeze, the derivation and the consistency audit,
and **before** the archive is built and verified.

What that row claims is what is true at that instant: **the package
directory is sealed**, complete and about to be manifested. It carries the
attempt id, `status: authoritative`, the package basename, the exact head,
and `result: sealed <package>`. It does not claim a ZIP digest, a byte
count, or a P8 verdict, because none of those exists yet; those live in the
.zip.sha256 sidecar and in the P8 transcript.

The backstop that keeps this from being a forward promise: **if the archive
or the final verification fails, a discard marker is written into the
package directory, and the coherence gate refuses any package carrying
one.** A package that reaches an evidence branch with an authoritative row
and no marker is one whose archive and verification passed, and the sidecar
and the outer log say so independently.

This is the one judgement in the design that a reviewer should weigh rather
than accept; `REVIEW_REQUEST.md` §4 asks it as a question.

## 3. One log root per attempt

The V11 package had one package-phase transcript — its gate comparison —
claimed by **six** attempts, and another — its sealer's own test run — by
**five**, both at the top of `logs/` with no attempt in their names. A failed attempt's logs did not
stay with that attempt; the next attempt overwrote them, so the evidence for
why an assembly was abandoned was destroyed by the assembly that replaced
it.

Every attempt now writes beneath its own root, named by the ordinal the
ledger allocates. An existing log target is still refused outright, never
overwritten. `logs/LOG-INDEX.md` is derived mechanically from what is on
disk rather than written by hand.

Package validation refuses:

- an unexplained zero-byte log claimed by an attempt;
- a log an attempt claims that is not there;
- a log claimed by two attempts;
- a log present in the package that no attempt claims;
- an attempt referencing a log outside its own root.

Each has a focused test.

## 4. The attempt ledger lives outside every package

The append-only ledger is written outside the package directory, so an
ordinal is allocated once for the whole lane and a rerun cannot reproduce a
previous attempt's log identity. An attempt id is
`<side>-<UTC stamp>-<ordinal><nonce>`, and the nonce is drawn from an
alphabet with no hex letter in it, so an attempt id can never be misread as
an abbreviated commit SHA by the identity audit.

`logs/attempts.json` is the ledger's rows for this lane, copied into the
package. The copy is taken as late as the phase contract allows, so that the
sealing attempt's own terminal row is inside it.

## 5. Two endpoints, and failure sets rather than exit codes

Every validation ran twice: once at this head, once at the parent — the
exact reviewed V11 head. That is the only way to tell an inherited failure
from a caused one, and this repository's own guidance requires comparing
failure sets rather than exit codes.

The parent battery additionally replays **this head's test file against the
parent**, which is the non-vacuity proof of the whole lane: regressions that
pass everywhere prove nothing, and these fail where the correction is
absent. `checks.txt` names that step, its log and its exit.

Tree state is read **per command**, before and after, rather than inherited
from one preflight, so a step that dirtied the tree would be recorded dirty
on its own row.

## 6. What was discarded

Every assembly attempt under this lane's name is in `logs/attempts.json`,
discarded ones included, each with its own terminal disposition and its one
reason. The filter ships them all: a discarded assembly is by definition not
an attempt the package was built from, and filtering to "the attempts this
package was built from" is precisely how the previous lane's ledger came to
name none of them.

## 7. Four earlier battery runs were set aside, and why

Before the batteries whose logs are in this package, four earlier runs were
**set aside**. None is in this package's ledger and none of their transcripts
are members; the unedited ledgers they wrote are retained outside this
package, beside the live one, together with their log roots. None produced a
figure used anywhere here.

Every one of them was caught by a gate rather than by someone noticing, and
three of the four are this lane's own subject — a claim resting on something
never actually established — arriving in this lane's own apparatus. They are
recorded here rather than smoothed over, because a package that shows only
the run that worked is a package that has hidden how it knows.

**Two wrote a transcript that was empty.** The browser gate's stdout is
deliberately discarded — it is the same ~590KB JSON the report member already
carries — and the note explaining the discard was joined to the command with
`&&`, so it printed only when the gate exited 0; this route's inherited
failures make it exit 1, so the note printed only when there was nothing to
explain. That is the same finding the V11 review made against V11, in the
same member. Later, the step that restores the substituted test file wrote an
empty transcript too, for the opposite reason: `git status --porcelain`
prints nothing when a tree is clean, so a successful restore left a file
whose emptiness a reader would have to know how to interpret. Both steps now
state their outcome in words, and the attempt-log audit refuses an
unexplained empty log so that neither can recur silently.

**One measured a head this package does not name.** It ran cleanly, and its
figures were right in a way that mattered: they showed the durable record
understating how many ways this head's test file fails when replayed against
the uncorrected parent. Correcting the record moved the implementation head,
and a package binds to the head its batteries actually measured, so they ran
again.

**One measured a tree no commit names.** The parent battery substitutes the
head's test file to produce the non-vacuity replay, and it did not put the
file back. The next parent battery began on a checkout still carrying it and
reported **544 focused and 1,895 discovered as the parent's counts** — the
head's numbers wearing the parent's name. Every figure it produced was
plausible; that is the whole difficulty. What caught it was the per-command
tree reading the V11 lane added, which recorded `DIRTY` from the preflight
onward. Recording was not enough, because a reader who trusts the figures
never reaches the tree line, so two things changed: restoring the file is now
its own recorded step, and **a battery refuses to start** on a tree that is
not clean, naming the files that made it dirty. A battery measures a commit,
and the commit it names is only its subject if the tree is that commit's.

## 8. What is not claimed here

That the pipeline is under version control — it is not, in this workspace,
and P8 records each tool's trusted and shipped SHA-256 instead and fails
hard on divergence. That any earlier package was corrected — none was
touched; both V11 packages remain exactly as their review left them on their
own evidence branch. That this lane reviewed itself — it did not.
