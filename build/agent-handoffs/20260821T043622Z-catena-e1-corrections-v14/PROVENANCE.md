# Provenance

This package was produced by attempt `package-20260821T043622Z-13j6mmhy`, which is the
authoritative package attempt for `20260821T043622Z-catena-e1-corrections-v14`. Its identity is fixed
BEFORE the run rather than minted during it, so this member can name it: an
attempt id carrying a nonce invented at P0 could never appear in a document
authored beforehand and frozen at P6, and a package whose prose cannot say
which attempt it is cannot settle the question it exists to settle. The ordinal
is still allocated by the lane ledger and still refused if the lane has ever
spent it. What makes the attempt authoritative is not this sentence: it is the
`.authority.json` sibling, written only after P8 passed and bound to the
archive's recomputed size and digest. The shipped `logs/attempts.json` says
`sealed`, which is the most a member written before P8 may say about itself.

What ran, where it ran, in what order, and which record wins where two could
disagree.

**The authority is the lane ledger, and the lane ledger ships beside this
package.** `logs/attempts.json` is the copy of this lane's rows taken as late
as the phase contract allows; the complete append-only ledger is a sibling,
named in `HANDOFF.md` §10, so a reviewer can read every attempt this lane made
without reaching for a record outside the handoff. Where this file and the
ledger could be read as disagreeing, the ledger is right and this file is a
defect.

No figure here is typed. `checks.txt` carries each command with its exit code,
its start and end, its tree state before and after, its attempt, and its log;
`claims.json` carries the identity arithmetic; `DERIVED-CLAIMS.md` renders
both.

## 0. The link this lane does not have

Every earlier lane in this series named the independent review it answered by
its commit. **This one cannot.** `origin` carries no
`review/catena-wave-1-e1-corrections-v13-independent`; a branch of that name
exists only in a local reviewer checkout, standing at the reviewed head
`6cc85e1a1dea317a48c0bfcfd6f774201ea3a6c3` with no review commit on it. So
`claims.json` carries `review_addressed` as the empty string and
`DERIVED-CLAIMS.md` renders it as an em dash, rather than either omitting the
field or filling it with a SHA nobody can fetch.

That is a genuine break in the provenance chain and it is stated here, in
`HANDOFF.md` §1, in `LIMITATIONS.md` and as the first blocker in
`REVIEW_REQUEST.md`. What survives it is everything a reviewer can check
without the review: the parent is a real commit, the replay of this head's
tests against it fails where the correction is absent, and every figure is
measured at both endpoints. What does not survive it is any claim that this
lane's account of the disposition is checkable against the disposition itself.

One tool changed for this lane, and the reason is that gap. `logs/assemble.sh` read
its review SHA as `${REVIEW:-<a default>}`, and `:-` substitutes the default
for an **empty** value as well as an unset one — so a lane answering an
unpublished review could not say so, and would have silently claimed to answer
the previous lane's review instead. It is `${REVIEW-}` now: one character,
committed in the tool anchor so the anchor stays clean and versioned, and
re-copied into the shipped `logs/` so the executed bytes and the shipped bytes
agree. Its digest therefore differs from the previous lane's; every other
tool's is byte-identical, and P8's table says which is which.

## 1. Two vocabularies, because there are two facts

"This validation battery ran to completion" and "this is the package to
review" are different facts, and writing both `authoritative` makes the
authoritative count uncountable by construction. So:

**A validation battery** (`side: head`, `side: parent`):

    started ──▶ complete
            ├─▶ set aside
            └─▶ failed

**A package attempt** (`side: package`):

    started ──▶ sealing ──▶ sealed ──▶ authoritative ──▶ superseded
                        └─▶ discarded

`authoritative` is reserved for a package attempt. At most one package attempt
in a lane may hold it, and this package's records must resolve to exactly one.
A battery written `authoritative` is a refusal, not a row.

**Every non-authoritative terminal state carries its reason.** A terminal row
with an empty reason is refused, so a supersession, a discard and a set-aside
each say what happened in their own row rather than in a document beside it.

**This lane's first ledger is retired, and the reason is an operator error the
gate caught.** A parent battery appeared to have died when the shell that
launched it was torn down; the operator read it as dead, closed it out by hand
as `failed` with that reason, and removed its transcripts. The process was in
fact still alive. It went on running, its later steps failed because their log
root had been deleted underneath them, and it wrote its own terminal
`complete` row — so that one attempt ended up carrying two dispositions. The
head battery running beside it was killed rather than allowed to finish into a
record that could not be sealed against, and was closed out as `failed` with
that reason.

Run against that file, the ledger audit refuses it with four problems, by name:
one attempt with more than one terminal row, an illegal `failed -> complete`
transition, two terminal dispositions where one attempt gets one, and — before
the head attempt was closed out — an attempt with no terminal row at all. That
is the gate doing exactly what the previous lane's review asked it to do, to
this lane, and it is recorded rather than worked around.

Nothing was deleted to fix it. **The incoherent ledger is kept in the
workspace, complete, under a retired name**, and a fresh lane ledger was opened
with the allocator's `--fresh` assertion. **No figure in this package comes
from any attempt in the retired file**: both batteries were rerun end to end,
sequentially, in the fresh ledger, and the transcripts this package ships are
theirs.

**Two rows were removed from the fresh ledger, and that is disclosed too.** A
discarded package attempt's transcripts stay in its own discarded package
directory, and the audit's channel for saying so is a later row carrying
`log_root_elsewhere`. The operator's first two such rows were built by copying
the attempt's terminal row, so they repeated its `discarded` disposition and
gave those attempts two terminal rows each — which the ledger audit refused,
correctly, within the minute. They recorded no event, nothing had read them,
and an append-only file cannot un-say a disposition, so exactly those two lines
were removed and replaced with `record=step` notes that carry the same
`log_root_elsewhere` and no disposition at all. That is a rewrite of the record
rather than an append, it is the only one in this file, and it is stated here
rather than left for a reviewer to find by counting.

One ordinal is shared between the two files, and it is stated rather than
claimed away. The retired ledger spent three — a parent battery, a head battery
and a third parent attempt that was refused at preflight because a log target
already existed, ran nothing and wrote no log root. The fresh ledger begins at
the third. So the number three names one attempt in each file; they carry
different attempt ids, different UTC stamps and different nonces, no ledger
carries an ordinal twice within itself, and no two attempts share a log root,
because the retired third wrote none. The property this lane can prove is that
one ordinal names one attempt *within* a ledger, which is the rule the
allocator enforces; the stronger property of uniqueness *across* a retired file
and its replacement is not proved here, and pretending to it would be the same
class of over-claim the previous review found.

No attempt may be authoritative and superseded, unresolved and final, or
discarded and authoritative. Each is a distinct refusal in the coherence gate,
and each has a test that proves the refusal fires.

## 2. Authority is established after verification, and it binds the archive

The order is:

1. the attempt starts and is recorded started;
2. the package directory is sealed, and the strongest thing any in-package row
   may claim is `sealed`;
3. the manifest is taken and the archive is built;
4. P8 verifies the archive, read-only, executing no archive code;
5. the archive's byte size and SHA-256 are recomputed after P8;
6. **and only then** is final authority established.

The authority record is a structured sidecar naming the attempt, the exact
head, the archive's basename, its byte size and SHA-256, the P8 result and the
post-P8 rehash result — **each recomputed from the archive rather than carried
forward from an earlier phase.** If P8 fails, the attempt stays
non-authoritative and no record anywhere calls it otherwise.

The binding runs one way and the archive carries no such record, so there is no
self-reference and no ordering problem. What it costs is that an authoritative
package cannot be self-describing: an archive cannot contain its own digest.

## 3. What the authority gate consumes, and what it refuses

The gate consumes the archive, the digest-and-size sidecar, the P8 transcript,
the complete external ledger, the sibling markers and the package's own prose,
and its negative roster covers each contradiction a previous gate accepted: a
second authoritative state row, an authoritative winner followed by a discarded
state, multiline and uppercase contradictory prose, a wrong package on the
authoritative outer-log line, and prose that never names the winner.

This lane did not reopen that roster and does not claim to have re-derived it.
The V13 disposition as this lane received it does not name the negative roster
either way, so the corresponding requirement in the promise ledger is left
**open** rather than marked passed — recorded in `LIMITATIONS.md`.

## 4. One ledger, one lane, ordinals that are never reused

**This lane's ledger is a new file.** It was opened once, deliberately, with
the allocator's `--fresh` assertion, which refuses to open over an existing
ledger; and the allocator refuses to append to, or read as its own, a ledger
declaring a different lane. The previous lane's ledger is neither reused nor
extended, and it is not modified by this lane at all.

Ordinals are **monotonic and never reused**, and a rerun cannot reproduce a
previous attempt's log identity. An attempt id is
`<side>-<UTC stamp>-<ordinal><nonce>`, and the nonce is drawn from an alphabet
with no hex letter in it, so an attempt id can never be misread as an
abbreviated commit SHA by the identity audit.

**Chronology is checked.** A row whose time precedes the row before it, an
attempt whose embedded timestamp postdates its own last row, and a supersession
stamped inside a file that claims to have been frozen before it are each
refused rather than left for a reader to notice.

**The previous lane's package is not modified by this one.** Its ledger slice
is published evidence on its own evidence branch, and appending a supersession
row to it would rewrite an artifact a reviewer may already hold. Each lane
keeps its own ledger; the cross-lane disposition — that the V13 candidate
received CHANGES REQUIRED and that this candidate answers it — is recorded
where cross-lane dispositions have always been recorded, in the durable
records, and in `HANDOFF.md` §3.

## 5. One log root per attempt

Every attempt writes beneath its own root, named by the ordinal the ledger
allocates. An existing log target is refused outright, never overwritten, so a
failed attempt's transcripts stay with that attempt and cannot be destroyed by
the attempt that replaces it. `logs/LOG-INDEX.md` is derived mechanically from
what is on disk rather than written by hand.

Package validation refuses an unexplained zero-byte log claimed by an attempt;
a log an attempt claims that is not there; a log claimed by two attempts; a log
present in the package that no attempt claims; and an attempt referencing a log
outside its own root. Each has a focused test.

## 6. What the complete ledger contains, and where to read it

- the ledger is **append-only** and lane-pinned, so an attempt that is written
  cannot later be removed from it;
- the **complete** ledger — not a filter of it — is copied out as a sibling of
  this package at the end of the run;
- `logs/attempts.json` inside the package is this lane's rows taken as late as
  the phase contract allows, so the sealing attempt's own row is inside it;
- the inventory tool counts the ledger's rows mechanically and the authority
  gate reads the external ledger, so a package whose in-package copy and
  external ledger disagree is refused rather than published.

A reviewer counts those rows rather than reading a count here.

**One omission, stated rather than glossed.** The per-package ledger slice is
derived at P9, and the two post-seal gates run at P10 — after it. Unlike P11,
which copies its own row across into the slice, P10 has no such copy. So P10's
rows appear in the lane ledger, which ships as a sibling, and **not** in the
slice inside the archive. This lane's scope is semantic authority, not
packaging tooling, so it states the omission rather than changing the tool: the
in-package record that P10 ran is the pair of gate transcripts named in
`HANDOFF.md` §10, and the sibling ledger carries the rows. `LIMITATIONS.md`
records it.

## 7. Which bytes actually ran

**Every tool invocation records the SHA-256 of the exact bytes immediately
before it runs.** The table distinguishes shipped-and-executed from
shipped-and-not-executed, external system tool, and reviewer-only helper, so a
tool that shipped without running says so instead of borrowing the claim of one
that ran. P8 compares executed against trusted against shipped and fails hard
on divergence. Both records are siblings, named in `HANDOFF.md` §10.

**The trust anchor is versioned for this lane.** The previous package could not
claim that, and named it as a limitation; here the out-of-package tool
directory is a clean git checkout, its working tree empty, so P8's anchor check
reports it versioned and clean rather than raising an unversioned-anchor
problem. The one commit in it is the `${REVIEW-}` change described in §0.

## 8. Two endpoints, and failure sets rather than exit codes

Every validation ran twice: once at this head, once at the exact reviewed
parent `6cc85e1a1dea317a48c0bfcfd6f774201ea3a6c3`. That is the only way to tell
an inherited failure from a caused one, and this repository's own guidance
requires comparing failure sets rather than exit codes.

The parent battery additionally replays **this head's test file against the
parent**, which is the non-vacuity proof of the whole lane: regressions that
pass everywhere prove nothing, and these fail where the correction is absent.
`checks.txt` names that step, its log and its exit. The substituted file is
copied in and restored by the battery's own recorded steps, and a battery
refuses to start on a tree that is not clean, naming the files that made it
dirty — because a battery measures a commit, and the commit it names is only
its subject if the tree is that commit's.

**And it must be told which commit.** The battery requires an expected SHA and
refuses terminally when the checkout's HEAD does not match it, so a clean
checkout of the wrong commit cannot be labelled `parent`; it also refuses
terminally on a dirty postflight rather than recording the dirt and continuing.
Both refusals go through the discard path and leave a terminal ledger row
carrying its reason.

Tree state is read **per command**, before and after, rather than inherited
from one preflight.

## 9. What is not claimed here

That the review this lane answers can be checked — it cannot; see §0. That any
earlier package was corrected — none was touched; the V11, V12 and V13 packages
remain exactly as their reviews left them on their own evidence branches, and
this lane appended nothing to any of them. That P10's rows are in the archive
— they are not; see §6. That a gate refusing a contradiction proves no
contradiction exists that the gate does not model. And that this lane reviewed
itself — it did not.
