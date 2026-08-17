# Provenance

This package was produced by attempt `package-20260817T233843Z-18once13`, which is the authoritative package attempt for `20260817T233843Z-catena-e1-corrections-v13`. Its identity is fixed BEFORE the run rather than minted during it, so this member can name it: an attempt id carrying a nonce invented at P0 could never appear in a document authored beforehand and frozen at P6, and a package whose prose cannot say which attempt it is cannot settle the question it exists to settle. The ordinal is still allocated by the lane ledger and still refused if the lane has ever spent it. What makes the attempt authoritative is not this sentence: it is `20260817T233843Z-catena-e1-corrections-v13.authority.json`, written only after P8 passed and bound to the archive's recomputed size and digest. The shipped `logs/attempts.json` says `sealed`, which is the most a member written before P8 may say about itself.

What ran, where it ran, in what order, and which record wins where two could
disagree.

**The authority is the lane ledger, and the lane ledger ships beside this
package.** `logs/attempts.json` is the copy of this lane's rows taken as late
as the phase contract allows; the complete append-only ledger is a sibling,
named in `HANDOFF.md` §10, so a reviewer can read every attempt this lane made
without reaching for a record outside the handoff. Where this file and the
ledger could be read as disagreeing, the ledger is right and this file is a
defect. That sentence exists because a previous package's prose and its ledger
did disagree about exactly the thing the ledger exists to settle, and the
review found it — twice.

No figure here is typed. `checks.txt` carries each command with its exit code,
its start and end, its tree state before and after, its attempt, and its log;
`claims.json` carries the identity arithmetic; `DERIVED-CLAIMS.md` renders
both.

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

**Set aside is a terminal state a battery may honestly reach.** The previous
lane had no such state, so four cohorts it described in prose as set aside
stood in the ledger as `complete` with empty reasons — the review's finding.
A battery that is put aside is now recorded put aside, with its reason, rather
than forced into a word that means something else.

**Every non-authoritative terminal state carries its reason.** A terminal row
with an empty reason is refused, so a supersession, a discard and a set-aside
each say what happened in their own row rather than in a document beside it.

No attempt may be authoritative and superseded, unresolved and final, or
discarded and authoritative. Each is a distinct refusal in the coherence gate,
and each has a test that proves the refusal fires.

## 2. Authority is established after verification, and it binds the archive

The V12 review refused a terminal `authoritative` row written before P7 and
P8: a later archive or verification failure could write only best-effort
sibling markers while the sealed bytes kept their claim, and a durable
false-authority state would then need external reinterpretation.

The order is now:

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

The binding runs one way and the archive carries no such record, so there is
no self-reference and no ordering problem. What it costs is that an
authoritative package cannot be self-describing: an archive cannot contain its
own digest. `REVIEW_REQUEST.md` §4 asks whether that trade is acceptable, and
`LIMITATIONS.md` §6 states it as a limitation rather than a feature.

## 3. What the authority gate consumes, and what it refuses

The previous gate consumed only the shipped ledger and the outer log, and its
positive fixture passed without an archive or a P8 result — so it returned a
clean verdict for a package whose archive it had never seen. It now consumes
the archive, the digest-and-size sidecar, the P8 transcript, the complete
external ledger, the sibling markers and the package's own prose, and its
negative roster covers each contradiction it previously accepted: a second
authoritative state row, an authoritative winner followed by a discarded
state, multiline and uppercase contradictory prose, a wrong package on the
authoritative outer-log line, and prose that never names the winner.

Run against the V12 package it **refuses** it, naming the in-package authority
claims, the missing authority record, the two authoritative attempts, the
terminal reasons left empty and the sibling supersession marker. A gate that
has only ever been run against a package that passes is a gate nobody has seen
refuse.

## 4. One ledger, one lane, ordinals that are never reused

The ledger identity is pinned to this lane, and a foreign or restarted ledger
is refused rather than continued — which is what allowed a previous epoch's
ordinals 03, 04 and 05 to be reissued while the record claimed an ordinal is
allocated once for the lane. Ordinals are now **monotonic and never reused**,
and a rerun cannot reproduce a previous attempt's log identity.

An attempt id is `<side>-<UTC stamp>-<ordinal><nonce>`, and the nonce is drawn
from an alphabet with no hex letter in it, so an attempt id can never be
misread as an abbreviated commit SHA by the identity audit.

**Chronology is checked.** A row whose time precedes the row before it, an
attempt whose embedded timestamp postdates its own last row, and a
supersession stamped inside a file that claims to have been frozen before it
are each refused rather than left for a reader to notice. The previous ledger
carried all three.

## 5. One log root per attempt

Every attempt writes beneath its own root, named by the ordinal the ledger
allocates. An existing log target is refused outright, never overwritten, so a
failed attempt's transcripts stay with that attempt and cannot be destroyed by
the attempt that replaces it. `logs/LOG-INDEX.md` is derived mechanically from
what is on disk rather than written by hand.

Package validation refuses:

- an unexplained zero-byte log claimed by an attempt;
- a log an attempt claims that is not there;
- a log claimed by two attempts;
- a log present in the package that no attempt claims;
- an attempt referencing a log outside its own root.

Each has a focused test.

## 6. What the complete ledger contains, and where to read it

The previous package's prose asserted that every attempt and every retained
ledger was present, and the review established that four discarded package
attempts and four battery cohorts were absent from every surviving ledger
while three package members said otherwise. The mechanism, not the outcome, is
what this file states:

- the ledger is **append-only** and lane-pinned, so an attempt that is written
  cannot later be removed from it;
- the **complete** ledger — not a filter of it — is copied out as a sibling of
  this package at the end of the run;
- `logs/attempts.json` inside the package is this lane's rows taken as late as
  the phase contract allows, so the sealing attempt's own row is inside it;
- the inventory tool counts the ledger's rows mechanically and the authority
  gate reads the external ledger, so a package whose in-package copy and
  external ledger disagree is refused rather than published.

Whatever the run produced — every attempt that started, and every terminal
disposition it reached, discarded and set aside included — is therefore what
the sibling ledger carries. A reviewer counts those rows rather than reading a
count here.

## 7. Which bytes actually ran

The previous package recorded executed-against-shipped digests for four tools
of fifteen and took them at P8, which proves shipped against trusted rather
than executed against shipped. Two of the missing eleven were the tools that
write the records under review.

**Every tool invocation now records the SHA-256 of the exact bytes immediately
before it runs.** The table distinguishes shipped-and-executed from
shipped-and-not-executed, external system tool, and reviewer-only helper, so a
tool that shipped without running says so instead of borrowing the claim of
one that ran. P8 compares executed against trusted against shipped and fails
hard on divergence. Both records are siblings, named in `HANDOFF.md` §10.

## 8. Two endpoints, and failure sets rather than exit codes

Every validation ran twice: once at this head, once at the exact reviewed V12
parent. That is the only way to tell an inherited failure from a caused one,
and this repository's own guidance requires comparing failure sets rather than
exit codes.

The parent battery additionally replays **this head's test file against the
parent**, which is the non-vacuity proof of the whole lane: regressions that
pass everywhere prove nothing, and these fail where the correction is absent.
`checks.txt` names that step, its log and its exit. The substituted file is
restored by its own recorded step, and a battery refuses to start on a tree
that is not clean, naming the files that made it dirty — because a battery
measures a commit, and the commit it names is only its subject if the tree is
that commit's.

**And it must be told which commit.** `logs/battery.sh` now requires an expected
SHA and refuses terminally when the checkout's HEAD does not match it, so a
clean checkout of the wrong commit can no longer be labelled `parent`; it also
refuses terminally on a dirty postflight rather than recording the dirt and
continuing. Both refusals go through the discard path and leave a terminal
ledger row carrying its reason, and both are covered by fixtures in the
packaged `logs/test-attempt-history.py`.

Tree state is read **per command**, before and after, rather than inherited
from one preflight.

## 9. What is not claimed here

That the pipeline is under version control — it is not, in this workspace, and
the executed, trusted and shipped digests are what stands in its place. That
any earlier package was corrected — none was touched; the V11 and V12 packages
remain exactly as their reviews left them on their own evidence branches. That
a gate refusing a contradiction proves no contradiction exists that the gate
does not model. And that this lane reviewed itself — it did not.
